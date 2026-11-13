"""Cấu hình chỉ mục truy hồi (``configs/retrieval.yaml``), M10."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator


class EmbedModelSpec(BaseModel):
    """Một model embedding tự host (ghim ``hf_repo`` + ``revision`` như ``serve.yaml``)."""

    model_config = ConfigDict(extra="forbid")

    hf_repo: str
    revision: str | None = None
    """Commit trên HF Hub — bắt buộc trước run chính thức."""
    params_b: float | None = None
    license: str | None = None
    family: str | None = None
    query_prompt: str = ""
    """Tiền tố câu hỏi (model có instruction: Qwen3, e5-instruct)."""
    doc_prompt: str = ""
    max_seq_length: int = 512
    batch_size: int = 32
    dtype: str = "bf16"
    """bf16 (tự lùi fp16 khi GPU không hỗ trợ) | fp32."""
    trust_remote_code: bool = False
    encode_tps: float = 20_000.0
    """Token/giây khi encode (ước tính cho ``--dry-run``; thay bằng số đo trong ``runs.jsonl``)."""
    load_min: float = 2.0
    """Phút tải + nạp model (ước tính)."""

    def prompt(self, kind: str) -> str:
        return self.query_prompt if kind == "query" else self.doc_prompt


class BM25Params(BaseModel):
    model_config = ConfigDict(extra="forbid")
    k1: float = 1.5
    b: float = 0.75
    bigrams: bool = True


class EvalSetSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")
    val: str = "data/qa/val.jsonl"
    train: str = "data/qa/train.jsonl"
    train_sample: int = 1000
    seed: int = 42


class RegressionSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")
    n: int = 100
    seed: int = 42
    k: int = 5
    max_drop: float = 0.02
    baseline: str = "data/qa/retrieval_baseline.json"
    corpus: str = "tests/fixtures/retrieval/corpus.jsonl.gz"


class RetrievalConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    index_dir: str = "data/index"
    phu_luc_max_chars: int = 1500
    bm25: BM25Params = Field(default_factory=BM25Params)
    top_k: int = 20
    rrf_k: int = 60
    rrf_depth: int = 100
    """Số hit mỗi nguồn đưa vào RRF."""
    model_key: str | None = None
    """Model gốc đã chốt (M11/M13 dùng); ``None`` = chưa chốt."""
    candidates: list[str] = Field(default_factory=list)
    """Model so sánh ở bước chọn (``build_index --encode --all``, ``--evaluate``)."""
    models: dict[str, EmbedModelSpec] = Field(default_factory=dict)
    encode_flush_every: int = 512
    eval: EvalSetSpec = Field(default_factory=EvalSetSpec)
    regression: RegressionSpec = Field(default_factory=RegressionSpec)

    @model_validator(mode="after")
    def _check(self) -> RetrievalConfig:
        for k in [*self.candidates, *([self.model_key] if self.model_key else [])]:
            if k not in self.models:
                raise ValueError(f"model {k!r} không có trong models")
        return self

    def spec(self, key: str) -> EmbedModelSpec:
        if key not in self.models:
            raise KeyError(f"model {key!r} không có trong configs/retrieval.yaml")
        return self.models[key]

    def chunk_cfg_hash(self) -> str:
        """Hash phần cấu hình ảnh hưởng tới danh mục chunk."""
        return _hash({"phu_luc_max_chars": self.phu_luc_max_chars, "chunker": "m10-1"})


def _hash(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def load_retrieval_config(path: str | Path) -> RetrievalConfig:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    return RetrievalConfig.model_validate(raw)


__all__ = [
    "BM25Params",
    "EmbedModelSpec",
    "EvalSetSpec",
    "RegressionSpec",
    "RetrievalConfig",
    "load_retrieval_config",
]
