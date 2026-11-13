"""Embedder thật bằng sentence-transformers (chỉ trên máy GPU thuê, nhóm dependency ``embed``)
và bộ đếm token bằng ``tokenizers`` (nhóm ``tok``, cho ``--dry-run`` ở local).

Import torch/sentence-transformers **lười** (trong hàm) ⇒ pipeline local và test không cần torch.
"""

from __future__ import annotations

import logging
from collections.abc import Sequence
from typing import Any

import numpy as np

from trafficlaw.retrieval.config import EmbedModelSpec
from trafficlaw.retrieval.dense import l2_normalize

logger = logging.getLogger(__name__)


class TokenCounter:
    """Đếm token bằng ``tokenizer.json`` của đúng ``hf_repo@revision`` (không cần torch)."""

    def __init__(self, spec: EmbedModelSpec) -> None:
        from tokenizers import Tokenizer

        self.tok = Tokenizer.from_pretrained(spec.hf_repo, revision=spec.revision or "main")
        self.tok.no_truncation()

    def count_tokens(self, text: str) -> int:
        return len(self.tok.encode(text).ids)


class STEmbedder:
    """``SentenceTransformer`` ghim revision, ``max_seq_length`` theo cấu hình, bf16 (lùi fp16 khi
    GPU không hỗ trợ bf16). CUDA OOM → giảm batch một nửa, ghi log, chạy tiếp."""

    def __init__(self, spec: EmbedModelSpec, *, device: str | None = None) -> None:
        import torch
        from sentence_transformers import SentenceTransformer

        self.torch = torch
        dev = device or ("cuda" if torch.cuda.is_available() else "cpu")
        dtype: Any = torch.float32
        if dev == "cuda" and spec.dtype == "bf16":
            dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
        self.dtype_name = str(dtype).removeprefix("torch.")
        self.model = SentenceTransformer(
            spec.hf_repo,
            revision=spec.revision,
            device=dev,
            trust_remote_code=spec.trust_remote_code,
            model_kwargs={"torch_dtype": dtype},
        )
        self.model.max_seq_length = spec.max_seq_length
        self.device = dev
        self._dim = int(self.model.get_sentence_embedding_dimension() or 0)

    @property
    def dim(self) -> int:
        return self._dim

    def count_tokens(self, text: str) -> int:
        tok = self.model.tokenizer
        return len(tok(text, add_special_tokens=True, truncation=False)["input_ids"])

    def encode(self, texts: Sequence[str], *, batch_size: int = 32) -> np.ndarray:
        bs = batch_size
        while True:
            try:
                v = self.model.encode(
                    list(texts),
                    batch_size=bs,
                    normalize_embeddings=True,
                    convert_to_numpy=True,
                    show_progress_bar=False,
                )
                return l2_normalize(np.asarray(v, dtype=np.float32))
            except self.torch.cuda.OutOfMemoryError:
                if bs <= 1:
                    raise
                self.torch.cuda.empty_cache()
                bs = max(1, bs // 2)
                logger.warning("CUDA OOM → giảm batch còn %d", bs)

    def peak_vram_gb(self) -> float | None:
        if self.device != "cuda":
            return None
        return round(self.torch.cuda.max_memory_allocated() / 2**30, 3)


__all__ = ["STEmbedder", "TokenCounter"]
