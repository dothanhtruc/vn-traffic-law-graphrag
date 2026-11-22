"""Cấu hình M14 (fine-tune embedding + reranker): ``configs/hard_negatives.yaml``,
``configs/train_embedding.yaml``, ``configs/train_reranker.yaml``.

Lưới tham số (``grid``) khai báo **trước** khi chạy; mỗi mục lưới là một run (``run_name`` =
``<prefix>-<grid_id>``) ghi đè vài trường của ``train``. Chọn checkpoint bằng val (+ dev), không
dùng test (CLAUDE.md mục 10).
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator


class DataSpec(BaseModel):
    """Nguồn câu train + loại trừ."""

    model_config = ConfigDict(extra="forbid")
    train: str = "data/qa/train.jsonl"
    val: str = "data/qa/val.jsonl"
    train_manifest: str = "data/qa/train_manifest.json"
    test: str = "data/qa/test.jsonl"
    """Chỉ đọc ``gold_units`` để loại câu train (người dùng chọn 18/11/2026) và kiểm
    ``test_sha256`` của manifest — không đọc câu hỏi/đáp án test."""
    exclude_gold: list[str] = Field(
        default_factory=lambda: ["data/qa/test.jsonl", "data/qa/dev_multi.jsonl"]
    )
    """Câu train có positive là gold / tổ tiên / con cháu gold của các tập này bị loại."""
    chunks: str = "data/index/chunks.jsonl"
    windows: str = "data/index/vectors/aiteamvn-vi-emb/windows.jsonl"
    """Cửa sổ ≤ 512 token của model gốc (M10) — chunk dài lấy một cửa sổ làm text huấn luyện."""
    negatives: str = "data/train/hard_negatives.jsonl"
    max_items: int | None = None
    """Giới hạn số câu train (``None`` = tất cả); dry-run dùng ``DryRunSpec``."""


class MiningSpec(BaseModel):
    """Khai thác hard negative (``train/hard_negatives.py``) — khai báo trước khi chạy."""

    model_config = ConfigDict(extra="forbid")
    data: DataSpec = Field(default_factory=DataSpec)
    embed_key: str = "aiteamvn-vi-emb"
    """Model embedding **gốc** (khoá trong ``retrieval.yaml``) cho nguồn dense."""
    reranker_key: str = "aiteamvn-reranker"
    """Reranker **gốc** chấm điểm để loại negative giả."""
    bm25_k: int = 30
    dense_k: int = 30
    siblings_k: int = 5
    """Khoản cùng Điều (THUOC cùng cha trên đồ thị ≙ cùng ``dieu_id`` trong danh mục), gần vị trí
    positive nhất."""
    max_candidates: int = 20
    """Số ứng viên tối đa/câu đưa vào reranker (trộn vòng tròn dense → bm25 → anh em)."""
    delta: float = 1.0
    """Bỏ negative có điểm rerank ≥ điểm positive − delta (logit) — nghi là positive giả."""
    keep: int = 7
    """Số negative lưu cho mỗi câu (khó nhất trước); trainer lấy ``n_neg`` đầu."""
    seed: int = 42


class HubSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")
    enabled: bool = True
    private: bool = True
    push_checkpoints: bool = True
    """Đẩy checkpoint (model + optimizer + scheduler + RNG) lên repo ``<run>-ckpt`` (luồng nền;
    lần đẩy trước chưa xong thì bỏ qua lần này, ghi log). Bản tốt nhất (chỉ trọng số) đẩy lên
    repo ``<run>``, commit sha ghi vào log để ghim revision."""


class DryRunSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")
    steps: int = 20
    n_items: int = 1000
    n_val: int = 60
    """Số câu val cho lượt đánh giá thử."""


class TrainParams(BaseModel):
    """Tham số một run (sau khi áp mục lưới)."""

    model_config = ConfigDict(extra="forbid")
    epochs: int = 3
    lr: float = 2e-5
    warmup_ratio: float = 0.1
    weight_decay: float = 0.01
    max_grad_norm: float = 1.0
    batch_size: int = 128
    """Embedder: số câu/bước tối ưu (batch hiệu dụng). Reranker: số nhóm/lần tích luỹ."""
    mini_batch_size: int = 32
    """Embedder: mini-batch của GradCache (``CachedMultipleNegativesRankingLoss``). Reranker: số
    nhóm/lượt forward. CUDA OOM → giảm một nửa (toán học không đổi)."""
    grad_accum: int = 1
    """Reranker: số lần tích luỹ (CLAUDE.md mục 9: batch 16 + tích luỹ 2)."""
    n_neg: int = 1
    scale: float = 20.0
    """Embedder: hệ số nhân cosine trong MNRL (mặc định sentence-transformers)."""
    gradient_checkpointing: bool = False
    dtype: Literal["bf16", "fp32"] = "bf16"
    """bf16 autocast (tự lùi fp16 + GradScaler khi GPU không hỗ trợ bf16); trọng số giữ fp32."""
    save_steps: int = 50
    eval_steps: int | None = None
    """Đánh giá val mỗi N bước (``None`` = chỉ cuối mỗi epoch)."""
    eval_at_start: bool = False
    seed: int = 42
    log_steps: int = 5


class TrainConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: Literal["embedding", "reranker"]
    base_key: str
    """Khoá model gốc trong ``configs/retrieval.yaml`` (``models`` hoặc ``rerankers``)."""
    run_prefix: str
    data: DataSpec = Field(default_factory=DataSpec)
    train: TrainParams = Field(default_factory=TrainParams)
    grid: dict[str, dict[str, Any]] = Field(default_factory=dict)
    hub: HubSpec = Field(default_factory=HubSpec)
    dry_run: DryRunSpec = Field(default_factory=DryRunSpec)
    output_dir: str = "checkpoints"
    log_dir: str = "logs/train"
    eval_pool: str = "data/index/retrieval_eval/val/G.jsonl"
    """Reranker: pool cố định của val (truy hồi G M11, trước rerank) để đánh giá rerank-only."""
    train_factor: float = 4.0
    """Ước tính: chi phí một token khi huấn luyện ≈ ``train_factor`` × khi suy luận."""

    @model_validator(mode="after")
    def _check(self) -> TrainConfig:
        for gid, over in self.grid.items():
            bad = set(over) - set(TrainParams.model_fields)
            if bad:
                raise ValueError(f"grid.{gid}: trường lạ {sorted(bad)}")
        return self

    def params(self, grid_id: str | None) -> TrainParams:
        if grid_id is None:
            return self.train
        if grid_id not in self.grid:
            raise KeyError(f"grid {grid_id!r} không có (có: {sorted(self.grid)})")
        return self.train.model_copy(update=self.grid[grid_id])

    def run_name(self, grid_id: str | None, *, dry_run: bool = False) -> str:
        base = f"{self.run_prefix}-{grid_id}" if grid_id else self.run_prefix
        return f"{base}-dryrun" if dry_run else base


def params_hash(obj: Any) -> str:
    raw = json.dumps(obj, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(raw.encode()).hexdigest()


def _yaml(path: str | Path) -> dict[str, Any]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}


def load_train_config(path: str | Path) -> TrainConfig:
    return TrainConfig.model_validate(_yaml(path))


def load_mining_config(path: str | Path) -> MiningSpec:
    return MiningSpec.model_validate(_yaml(path))


__all__ = [
    "DataSpec",
    "DryRunSpec",
    "HubSpec",
    "MiningSpec",
    "TrainConfig",
    "TrainParams",
    "load_mining_config",
    "load_train_config",
    "params_hash",
]
