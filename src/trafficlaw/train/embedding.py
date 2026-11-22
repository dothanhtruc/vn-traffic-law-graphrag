"""Fine-tune embedding (M14): ``SentenceTransformer`` gốc (``AITeamVN/Vietnamese_Embedding``, ghim
revision) + :func:`losses.cached_mnrl_step` (``CachedMultipleNegativesRankingLoss``: batch hiệu
dụng 128, mini-batch 32, scale 20, in-batch + hard negatives) trên batch không trùng.

Không dùng ``SentenceTransformerTrainer`` (cần ``datasets`` + ``accelerate``, API đổi nhiều giữa
các bản): vòng huấn luyện tự viết (``loop.py``) để checkpoint đúng yêu cầu mục 9 và có test trên
CPU. Model lưu bằng ``SentenceTransformer.save`` ⇒ ``STEmbedder`` (M10) nạp trực tiếp từ HF Hub.
"""

from __future__ import annotations

import logging
from collections.abc import Sequence
from pathlib import Path
from typing import Any

import numpy as np
import torch
import torch.nn.functional as F  # noqa: N812

from trafficlaw.eval.retrieval_eval import EvalQuery
from trafficlaw.retrieval.catalog import ChunkCatalog
from trafficlaw.retrieval.config import EmbedModelSpec
from trafficlaw.retrieval.dense import Window
from trafficlaw.train.config import TrainParams
from trafficlaw.train.data import TrainExample, no_dup_batches, training_plan
from trafficlaw.train.evaluate import dense_eval
from trafficlaw.train.loop import StepCtx, Task
from trafficlaw.train.losses import cached_mnrl_step

logger = logging.getLogger(__name__)


def load_st(spec: EmbedModelSpec, device: str) -> Any:
    from sentence_transformers import SentenceTransformer

    m = SentenceTransformer(
        spec.hf_repo,
        revision=spec.revision,
        device=device,
        trust_remote_code=spec.trust_remote_code,
        model_kwargs={"torch_dtype": torch.float32},
    )
    m.max_seq_length = spec.max_seq_length
    return m


def features(model: Any, texts: Sequence[str], device: str) -> dict[str, Any]:
    """Token hoá bằng API của bản sentence-transformers đã khoá (6.x: ``preprocess``)."""
    fn = getattr(model, "preprocess", None) or model.tokenize
    f = fn(list(texts))
    return {k: (v.to(device) if isinstance(v, torch.Tensor) else v) for k, v in f.items()}


def embed(model: Any, feats: dict[str, Any]) -> torch.Tensor:
    return F.normalize(model(dict(feats))["sentence_embedding"].float(), dim=-1)


def build_embedding_task(
    *,
    spec: EmbedModelSpec,
    examples: Sequence[TrainExample],
    params: TrainParams,
    device: str,
    windows: Sequence[Window] | None,
    catalog: ChunkCatalog | None,
    val: Sequence[EvalQuery],
    fingerprint: dict[str, Any],
    model: Any = None,
    eval_batch: int = 64,
) -> Task:
    model = model if model is not None else load_st(spec, device)
    if params.gradient_checkpointing:
        model.gradient_checkpointing_enable()
    qp, dp = spec.query_prompt, spec.doc_prompt
    ex = list(examples)
    plan = training_plan(
        lambda ep: no_dup_batches(ex, params.batch_size, seed=params.seed, epoch=ep),
        params.epochs,
    )

    def step_fn(batch: list[int], micro: int, ctx: StepCtx) -> float:
        items = [ex[i] for i in batch]
        qs = [qp + e.question for e in items]
        ps = [dp + e.pos_text for e in items] + [dp + t for e in items for t in e.neg_texts]
        qb = [features(model, qs[i : i + micro], device) for i in range(0, len(qs), micro)]
        pb = [features(model, ps[i : i + micro], device) for i in range(0, len(ps), micro)]

        def emb(f: dict[str, Any]) -> torch.Tensor:
            with ctx.autocast():
                return embed(model, f)

        return cached_mnrl_step(emb, qb, pb, params.scale, backward=ctx.backward)

    def encode(texts: Sequence[str], kind: str) -> np.ndarray:
        p = qp if kind == "query" else dp
        out = []
        for i in range(0, len(texts), eval_batch):
            f = features(model, [p + t for t in texts[i : i + eval_batch]], device)
            with torch.no_grad():
                out.append(embed(model, f).cpu().numpy())
        return np.concatenate(out).astype(np.float32) if out else np.zeros((0, 1), np.float32)

    def evaluate(ctx: StepCtx) -> dict[str, Any]:
        assert windows is not None and catalog is not None

        def enc(texts: Sequence[str], kind: str) -> np.ndarray:
            with ctx.autocast():
                return encode(texts, kind)

        return dense_eval(enc, windows, catalog, val, seed=params.seed)

    def save_model(d: Path) -> None:
        model.save(str(d), create_model_card=False)

    def load_model(d: Path) -> None:
        from sentence_transformers import SentenceTransformer

        src = SentenceTransformer(str(d), device=device)
        model.load_state_dict(src.state_dict())

    return Task(
        model=model,
        plan=plan,
        step_fn=step_fn,
        evaluate=evaluate if (windows is not None and catalog is not None and val) else None,
        save_model=save_model,
        load_model=load_model,
        fingerprint=fingerprint,
        info={
            "kind": "embedding",
            "base": f"{spec.hf_repo}@{spec.revision}",
            "n_examples": len(ex),
            "n_batches": len(plan),
            "n_with_negative": sum(1 for e in ex if e.neg_ids),
        },
    )


__all__ = ["build_embedding_task", "embed", "features", "load_st"]
