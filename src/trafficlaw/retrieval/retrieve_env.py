"""Nạp ``RetrievalContext`` từ repo (I/O): ``data/index`` (M10), ``data/graph`` (M5 + M8),
danh mục PT/CT, registry, cache. Dùng cho ``scripts.retrieve``, M13, M15.

``gpu=False`` (mặc định, local): không import torch; vector câu hỏi / điểm rerank chỉ đọc cache.
``gpu=True`` (máy thuê): thiếu cache → nạp ``STEmbedder`` / ``STReranker`` (lười, lần đầu cần).
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

import yaml

from trafficlaw.eval.qa_subsets import data_version
from trafficlaw.graph.doc_names import DocNameTable, load_doc_aliases
from trafficlaw.graph.embedded import EmbeddedStore
from trafficlaw.graph.extract import Catalog
from trafficlaw.graph.store import data_hash
from trafficlaw.llm.prompt_loader import load_prompt
from trafficlaw.registry.loader import load_registry
from trafficlaw.retrieval.analyze import Analyzer, AnalyzerTables, LLMAnalysisStore
from trafficlaw.retrieval.bm25 import BM25Index
from trafficlaw.retrieval.catalog import ChunkCatalog
from trafficlaw.retrieval.config import RetrievalConfig
from trafficlaw.retrieval.dense import FaissIndex
from trafficlaw.retrieval.index_pipeline import IndexPaths, file_sha256, read_manifest
from trafficlaw.retrieval.retrieve import QueryEncoder, RetrievalContext


def paths_config(root: Path) -> dict[str, Any]:
    return yaml.safe_load((root / "configs" / "paths.yaml").read_text(encoding="utf-8")) or {}


def load_catalog_yaml(path: Path) -> Catalog:
    return Catalog.model_validate(yaml.safe_load(path.read_text(encoding="utf-8")) or {})


def load_analyzer_tables(root: Path, cfg: RetrievalConfig) -> AnalyzerTables:
    pc = paths_config(root)
    reg = load_registry(root / pc["documents"])
    names = DocNameTable(reg.documents, *load_doc_aliases(root / pc["doc_aliases"]))
    registry = {d.doc_id: (d.loai, d.so_hieu) for d in reg.documents if d.loai != "vbhn"}
    return AnalyzerTables(
        load_catalog_yaml(root / cfg.analyze.catalog), doc_names=names, registry=registry
    )


def rerank_dir(root: Path, cfg: RetrievalConfig, key: str) -> Path:
    return root / cfg.index_dir / "rerank" / key


def build_analyzer(
    root: Path,
    cfg: RetrievalConfig,
    *,
    today: date,
    llm: Any | None = None,
    llm_model_id: str | None = None,
    strict: bool = True,
    tables: AnalyzerTables | None = None,
) -> Analyzer:
    """``llm`` = client (pha analyze, cần server); ``None`` → chỉ đọc kết quả đã lưu của
    ``llm_model_id``. ``cfg.analyze.llm_fallback = false`` → không dùng LLM."""
    use = cfg.analyze.llm_fallback
    a = Analyzer(
        tables or load_analyzer_tables(root, cfg),
        today=today,
        llm=llm if use else None,
        store=LLMAnalysisStore(root / cfg.analyze.llm_cache) if use else None,
        prompt=load_prompt(cfg.analyze.prompt) if use else None,
        max_output_tokens=cfg.analyze.max_output_tokens,
        strict=strict,
    )
    a.set_model_id(llm_model_id if use else None)
    return a


def build_context(
    root: Path,
    cfg: RetrievalConfig,
    analyzer: Analyzer,
    *,
    gpu: bool = False,
) -> RetrievalContext:
    paths = IndexPaths(root / cfg.index_dir)
    pc = paths_config(root)
    graph_dir = root / pc["graph_dir"]
    man = read_manifest(paths)
    if man.get("catalog", {}).get("sha256") != file_sha256(paths.chunks):
        raise SystemExit("manifest lệch chunks.jsonl — chạy scripts.build_index trước")
    emb_factory = rr_factory = None
    if gpu:

        def emb_factory(key: str):  # type: ignore[no-redef]
            from trafficlaw.retrieval.st_embedder import STEmbedder

            return STEmbedder(cfg.spec(key))

        def rr_factory(key: str):  # type: ignore[no-redef]
            from trafficlaw.retrieval.rerank import STReranker

            return STReranker(cfg.reranker(key))

    store = EmbeddedStore.from_dir(graph_dir)
    meta = {
        "data_version": data_version(
            [root / pc[k] for k in ("documents", "unit_versions", "units_added")]
        ),
        "catalog_sha256": man["catalog"]["sha256"],
        "graph_data_hash": data_hash(graph_dir),
    }
    return RetrievalContext(
        cfg,
        catalog=ChunkCatalog.load(paths.chunks),
        bm25=BM25Index.load(paths.bm25),
        store=store,
        analyzer=analyzer,
        faiss_loader=lambda k: FaissIndex.load(paths.faiss(k)),
        encoder=QueryEncoder(cfg, paths.vectors, emb_factory),
        rerank_dir=lambda k: rerank_dir(root, cfg, k),
        reranker_factory=rr_factory,
        meta=meta,
    )


__all__ = [
    "build_analyzer",
    "build_context",
    "load_analyzer_tables",
    "load_catalog_yaml",
    "paths_config",
    "rerank_dir",
]
