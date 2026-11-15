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


class TokenizerSpec(BaseModel):
    """Tokenizer ``tokenizer.json`` (thư viện ``tokenizers``) dùng để tách cửa sổ rerank — cùng
    một tokenizer ở local (``--dry-run``) và máy thuê ⇒ cửa sổ giống hệt nhau."""

    model_config = ConfigDict(extra="forbid")
    hf_repo: str
    revision: str | None = None


class RerankerSpec(BaseModel):
    """Cross-encoder tự host (M11), ghim ``hf_repo`` + ``revision``."""

    model_config = ConfigDict(extra="forbid")

    hf_repo: str
    revision: str | None = None
    params_b: float | None = None
    license: str | None = None
    family: str | None = None
    max_length: int = 512
    """Token của cặp (câu hỏi + cửa sổ, gồm token đặc biệt)."""
    batch_size: int = 32
    dtype: str = "bf16"
    count_tokenizer: TokenizerSpec | None = None
    """Tokenizer đếm token khi tách cửa sổ (``None`` → tokenizer của chính model)."""
    pairs_per_s: float = 150.0
    """Cặp/giây khi chấm (ước tính cho ``--dry-run``; thay bằng số đo)."""
    load_min: float = 1.5


class AnalyzeSpec(BaseModel):
    """Phân tích câu hỏi: rule trước, LLM ``main`` dự phòng khi rule không chắc."""

    model_config = ConfigDict(extra="forbid")
    catalog: str = "data/registry/extract_catalog.yaml"
    llm_fallback: bool = True
    prompt: str = "analyze_question"
    max_output_tokens: int = 512
    llm_cache: str = "data/index/analyze/llm.jsonl"
    """Kết quả LLM đã hậu kiểm (khoá: model, prompt, schema, câu hỏi, ngày tham chiếu) — pha 2
    và chạy lại ở local đọc file này, không cần server."""


class ExpandRule(BaseModel):
    model_config = ConfigDict(extra="forbid")
    edge_types: list[str]
    hops: int = 1


class ExpandSpec(BaseModel):
    """Graph expand (M11): bảng loại cạnh/số hop theo loại câu, giới hạn chunk mở rộng."""

    model_config = ConfigDict(extra="forbid")
    default: ExpandRule = Field(
        default_factory=lambda: ExpandRule(edge_types=["DAN_CHIEU"], hops=1)
    )
    by_type: dict[str, ExpandRule] = Field(default_factory=dict)
    max_chunks: int = 30
    """Tối đa chunk mở rộng thêm vào pool (theo thứ tự seed → hop → mã nút)."""
    per_node_max: int = 5
    """Tối đa chunk cho một nút đích (Điều có nhiều Khoản)."""
    reverse_sanctions: bool = True
    """Seed là Khoản nêu chế tài → thêm các hành vi bị xử phạt theo nó (in_edges của nút
    CheTai/DiemGPLX/BienPhapBoSung nêu tại seed)."""

    def rule_for(self, question_type: str | None) -> ExpandRule:
        return self.by_type.get(question_type or "", self.default)


class SystemSpec(BaseModel):
    """Một cấu hình truy hồi (B1, B2, B3, G, A1–A3; CLAUDE.md mục 10)."""

    model_config = ConfigDict(extra="forbid")
    description: str = ""
    bm25: bool = True
    dense: bool = True
    dense_model: str | None = None
    """Khoá model embedding; ``None`` → ``model_key`` (M14 thay bằng bản fine-tune)."""
    reranker: bool = False
    reranker_model: str | None = None
    """Khoá reranker; ``None`` → ``reranker_key``."""
    graph_expand: bool = False
    validity_filter: bool = True
    """Lọc as_of ở hybrid, expand, rerank (A2 = tắt)."""
    analyzer_llm: bool = True
    pool_k: int = 20
    reserved_graph_slots: int = 0
    """Số chỗ trong top ``final_k`` dành cho chunk chỉ đến từ đồ thị (cuối top-k, theo thứ tự
    rerank). 0 = rerank tự do (người dùng chốt 15/11/2026 sau đo val/train); M13 có thể so như
    biến thể khai báo trước."""
    final_k: int = 5

    @model_validator(mode="after")
    def _check(self) -> SystemSpec:
        if not (self.bm25 or self.dense):
            raise ValueError("cần ít nhất một nguồn: bm25 hoặc dense")
        return self


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
    reranker_key: str | None = None
    """Reranker gốc đã chốt (M11; M14 thay bằng bản fine-tune)."""
    rerankers: dict[str, RerankerSpec] = Field(default_factory=dict)
    analyze: AnalyzeSpec = Field(default_factory=AnalyzeSpec)
    expand: ExpandSpec = Field(default_factory=ExpandSpec)
    configs: dict[str, SystemSpec] = Field(default_factory=dict)
    eval: EvalSetSpec = Field(default_factory=EvalSetSpec)
    regression: RegressionSpec = Field(default_factory=RegressionSpec)

    @model_validator(mode="after")
    def _check(self) -> RetrievalConfig:
        for k in [*self.candidates, *([self.model_key] if self.model_key else [])]:
            if k not in self.models:
                raise ValueError(f"model {k!r} không có trong models")
        if self.reranker_key and self.reranker_key not in self.rerankers:
            raise ValueError(f"reranker {self.reranker_key!r} không có trong rerankers")
        for name, sc in self.configs.items():
            if sc.dense and (sc.dense_model or self.model_key) not in self.models:
                raise ValueError(f"configs.{name}: chưa có model embedding")
            if sc.reranker and (sc.reranker_model or self.reranker_key) not in self.rerankers:
                raise ValueError(f"configs.{name}: chưa có reranker")
        return self

    def system(self, name: str) -> SystemSpec:
        if name not in self.configs:
            raise KeyError(f"cấu hình {name!r} không có trong configs/retrieval.yaml (configs:)")
        return self.configs[name]

    def dense_key(self, sc: SystemSpec) -> str | None:
        return (sc.dense_model or self.model_key) if sc.dense else None

    def reranker_key_for(self, sc: SystemSpec) -> str | None:
        return (sc.reranker_model or self.reranker_key) if sc.reranker else None

    def reranker(self, key: str) -> RerankerSpec:
        if key not in self.rerankers:
            raise KeyError(f"reranker {key!r} không có trong configs/retrieval.yaml")
        return self.rerankers[key]

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
    "AnalyzeSpec",
    "BM25Params",
    "ExpandRule",
    "ExpandSpec",
    "RerankerSpec",
    "SystemSpec",
    "TokenizerSpec",
    "EmbedModelSpec",
    "EvalSetSpec",
    "RegressionSpec",
    "RetrievalConfig",
    "load_retrieval_config",
]
