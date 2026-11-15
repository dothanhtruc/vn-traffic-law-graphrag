"""Fixture M11: mini_graph (M6) + nút/cạnh ngữ nghĩa M8 (``mini_graph/semantic``), danh mục chunk,
ngữ cảnh truy hồi với model giả (``HashEmbedder``, ``FakeReranker``)."""

from __future__ import annotations

import shutil
from datetime import date
from pathlib import Path

import pytest

from trafficlaw.graph.embedded import EmbeddedStore
from trafficlaw.retrieval.analyze import Analyzer, AnalyzerTables
from trafficlaw.retrieval.bm25 import BM25Index
from trafficlaw.retrieval.catalog import ChunkCatalog, build_catalog
from trafficlaw.retrieval.config import RetrievalConfig, load_retrieval_config
from trafficlaw.retrieval.dense import (
    FaissIndex,
    HashEmbedder,
    VectorCache,
    chunk_windows,
    encode_cached,
)
from trafficlaw.retrieval.rerank import FakeReranker
from trafficlaw.retrieval.retrieve import QueryEncoder, RetrievalContext
from trafficlaw.retrieval.retrieve_env import load_analyzer_tables

ROOT = Path(__file__).resolve().parents[2]
MINI = ROOT / "tests/fixtures/mini_graph"
DATES = (date(2025, 1, 1), date(2026, 1, 1), date(2026, 7, 1), date(2026, 8, 15))
TODAY = date(2026, 11, 3)


@pytest.fixture(scope="session")
def mini_dir(tmp_path_factory: pytest.TempPathFactory) -> Path:
    d = tmp_path_factory.mktemp("mini_sem")
    for f in [*MINI.glob("*.jsonl"), *(MINI / "semantic").glob("*.jsonl")]:
        shutil.copy(f, d / f.name)
    return d


@pytest.fixture(scope="session")
def mini_store(mini_dir: Path) -> EmbeddedStore:
    return EmbeddedStore.from_dir(mini_dir)


@pytest.fixture(scope="session")
def mini_catalog(mini_store: EmbeddedStore) -> ChunkCatalog:
    return ChunkCatalog(build_catalog(mini_store, phu_luc_max_chars=1500))


@pytest.fixture(scope="session")
def cfg() -> RetrievalConfig:
    return load_retrieval_config(ROOT / "configs/retrieval.yaml")


@pytest.fixture(scope="session")
def tables(cfg: RetrievalConfig) -> AnalyzerTables:
    return load_analyzer_tables(ROOT, cfg)


def make_ctx(
    tmp: Path,
    cfg: RetrievalConfig,
    store: EmbeddedStore,
    catalog: ChunkCatalog,
    tables: AnalyzerTables,
    *,
    analyzer: Analyzer | None = None,
    reranker: FakeReranker | None = None,
    with_models: bool = True,
) -> RetrievalContext:
    """Ngữ cảnh đầy đủ với model giả. ``with_models=False`` → chỉ đọc cache (như local)."""
    key = cfg.model_key
    assert key is not None
    spec = cfg.spec(key)
    emb = HashEmbedder()
    vec_root = tmp / "vectors"
    ws = chunk_windows([(c.chunk_id, c.text) for c in catalog.chunks], spec, emb.count_tokens)
    vecs, _ = encode_cached(
        emb, VectorCache(vec_root / key), key, spec, "doc", [w.text for w in ws]
    )
    fi = FaissIndex.build(vecs, [(w.chunk_id, w.k) for w in ws], f"dense:{key}")
    rr = reranker or FakeReranker()
    return RetrievalContext(
        cfg,
        catalog=catalog,
        bm25=BM25Index.build([(c.chunk_id, c.text) for c in catalog.chunks]),
        store=store,
        analyzer=analyzer or Analyzer(tables, today=TODAY),
        faiss_loader=lambda k: fi,
        encoder=QueryEncoder(cfg, lambda k: vec_root / k, (lambda k: emb) if with_models else None),
        rerank_dir=lambda k: tmp / "rerank" / k,
        reranker_factory=(lambda k: rr) if with_models else None,
        meta={"data_version": "test", "catalog_sha256": "test", "graph_data_hash": "test"},
    )
