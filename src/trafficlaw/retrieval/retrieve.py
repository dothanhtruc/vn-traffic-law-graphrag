"""``retrieve()`` (M11): hàm truy hồi dùng chung cho M12 (sinh câu trả lời), M13 (giai đoạn
``retrieve`` của bộ chạy đánh giá) và M15 (demo).

Luồng (CLAUDE.md mục 3)::

    analyze (rule → LLM dự phòng)                         → as_of, loại câu
    hybrid: BM25 + vector, RRF k=60, top pool_k (20)      (lọc as_of TRƯỚC khi xếp hạng)
    graph expand theo bảng loại câu (≤ max_chunks mới)    (lọc as_of trên cạnh/phiên bản/chunk)
    rerank cross-encoder trên toàn pool (seed + mở rộng)  (điểm = max cửa sổ)
    kiểm chunk cuối (phủ as_of + unit còn phiên bản)      → top final_k (5)

Cấu hình B1/B2/B3/G/A1/A2/A3 bật/tắt từng bước (``configs/retrieval.yaml`` → ``configs:``). Không
có reranker (B1, B2) → thứ tự pool = thứ tự hybrid, chunk mở rộng xếp sau.

Model (vector câu hỏi, điểm rerank, LLM analyzer) chạy trên máy GPU thuê; kết quả được cache nên
chạy lại ở local chỉ đọc cache (thiếu → ``MissingVectorsError`` / ``MissingRerankScoresError`` /
``MissingLLMAnalysisError``).
"""

from __future__ import annotations

import logging
import time
from collections.abc import Callable
from datetime import date
from pathlib import Path
from typing import Any

import numpy as np
from pydantic import BaseModel, ConfigDict, Field

from trafficlaw.graph.store import BaseGraphStore
from trafficlaw.retrieval.analyze import Analyzer, QueryAnalysis
from trafficlaw.retrieval.bm25 import BM25Index
from trafficlaw.retrieval.catalog import ChunkCatalog
from trafficlaw.retrieval.config import RetrievalConfig
from trafficlaw.retrieval.dense import (
    Embedder,
    FaissIndex,
    VectorCache,
    cache_key,
    encode_cached,
)
from trafficlaw.retrieval.graph_expand import expand_candidates, sanction_index
from trafficlaw.retrieval.hybrid import hybrid_search
from trafficlaw.retrieval.index_pipeline import MissingVectorsError
from trafficlaw.retrieval.rerank import RerankCache, Reranker, RerankStats, rerank_scores
from trafficlaw.retrieval.validity_filter import allowed_ids, check_final

logger = logging.getLogger(__name__)


# --- kết quả ---------------------------------------------------------------------------------


class SourceInfo(BaseModel):
    """Vì sao chunk vào pool: ``bm25`` / ``dense:<model>`` / ``rrf`` (hạng, điểm) hoặc ``graph``
    (loại cạnh, hop, seed, nút đích, chiều)."""

    model_config = ConfigDict(extra="forbid")
    source: str
    rank: int | None = None
    score: float | None = None
    edge_type: str | None = None
    hop: int | None = None
    seed: str | None = None
    node: str | None = None
    direction: str | None = None


class PoolItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    chunk_id: str
    unit_id: str
    effective_from: date
    effective_to: date | None
    sources: list[SourceInfo]
    rerank_score: float | None = None


class HitOut(BaseModel):
    model_config = ConfigDict(extra="forbid")
    chunk_id: str
    unit_id: str
    doc_id: str
    version_ids: list[str]
    effective_from: date
    effective_to: date | None
    score: float
    rank: int
    sources: list[SourceInfo]


class ModelInfo(BaseModel):
    model_config = ConfigDict(extra="forbid")
    key: str
    hf_repo: str
    revision: str | None


class RetrievalResult(BaseModel):
    """Một lần truy hồi — ghi JSONL được (M13)."""

    model_config = ConfigDict(extra="forbid")
    config_name: str
    qid: str | None = None
    question: str
    as_of_param: date | None
    as_of: date
    """Ngày dùng để lọc (= ``analysis.as_of``)."""
    validity_filter: bool
    analysis: QueryAnalysis
    hits: list[HitOut]
    """Top ``final_k``."""
    ranked: list[str]
    """Toàn bộ thứ tự cuối (để tính R@10/20)."""
    pool: list[PoolItem]
    """Pool trước rerank (seed theo hạng hybrid, rồi chunk mở rộng)."""
    graph_docs: list[SourceInfo] = Field(default_factory=list)
    """Nút văn bản gặp khi mở rộng (chỉ provenance)."""
    final_notes: list[dict[str, str]] = Field(default_factory=list)
    embedding: ModelInfo | None = None
    reranker: ModelInfo | None = None
    llm_model: str | None = None
    prompt_hash: str | None = None
    rerank_stats: dict[str, Any] | None = None
    timings_ms: dict[str, float]
    data_version: str | None = None
    catalog_sha256: str | None = None
    graph_data_hash: str | None = None


# --- vector câu hỏi --------------------------------------------------------------------------


class QueryEncoder:
    """Vector câu hỏi từ ``VectorCache`` của M10; thiếu → encode bằng ``embedder_factory`` (máy
    thuê) hoặc ``MissingVectorsError``."""

    def __init__(
        self,
        cfg: RetrievalConfig,
        vectors_dir: Callable[[str], Path],
        embedder_factory: Callable[[str], Embedder] | None = None,
    ) -> None:
        self.cfg = cfg
        self.vectors_dir = vectors_dir
        self.factory = embedder_factory
        self._caches: dict[str, VectorCache] = {}
        self._emb: dict[str, Embedder] = {}

    def cache(self, key: str) -> VectorCache:
        if key not in self._caches:
            self._caches[key] = VectorCache(self.vectors_dir(key))
        return self._caches[key]

    def embedder(self, key: str) -> Embedder | None:
        if self.factory is None:
            return None
        if key not in self._emb:
            self._emb[key] = self.factory(key)
        return self._emb[key]

    def missing(self, key: str, questions: list[str]) -> list[str]:
        spec, c = self.cfg.spec(key), self.cache(key)
        return [q for q in questions if cache_key(key, spec, "query", q) not in c]

    def encode(self, key: str, questions: list[str]) -> np.ndarray:
        spec, c = self.cfg.spec(key), self.cache(key)
        if self.missing(key, questions):
            emb = self.embedder(key)
            if emb is None:
                n = len(self.missing(key, questions))
                raise MissingVectorsError(f"{key}: {n} câu hỏi chưa có vector — chạy với --gpu")
            vecs, _ = encode_cached(
                emb, c, key, spec, "query", questions, flush_every=self.cfg.encode_flush_every
            )
            return vecs
        return np.stack([c.get(cache_key(key, spec, "query", q)) for q in questions])


# --- ngữ cảnh --------------------------------------------------------------------------------


class RetrievalContext:
    """Nạp một lần: danh mục chunk, BM25, FAISS (lười theo model), đồ thị (có nút ngữ nghĩa M8),
    analyzer, reranker (lười), cache."""

    def __init__(
        self,
        cfg: RetrievalConfig,
        *,
        catalog: ChunkCatalog,
        bm25: BM25Index,
        store: BaseGraphStore,
        analyzer: Analyzer,
        faiss_loader: Callable[[str], FaissIndex],
        encoder: QueryEncoder,
        rerank_dir: Callable[[str], Path],
        reranker_factory: Callable[[str], Reranker] | None = None,
        meta: dict[str, str | None] | None = None,
    ) -> None:
        self.cfg = cfg
        self.catalog = catalog
        self.bm25 = bm25
        self.store = store
        self.analyzer = analyzer
        self.faiss_loader = faiss_loader
        self.encoder = encoder
        self.rerank_dir = rerank_dir
        self.reranker_factory = reranker_factory
        self.meta = dict(meta or {})
        self.sanctions = sanction_index(store)
        self._faiss: dict[str, FaissIndex] = {}
        self._rr: dict[str, Reranker] = {}
        self._rr_cache: dict[str, RerankCache] = {}
        self.rerank_totals: dict[str, RerankStats] = {}

    def faiss(self, key: str) -> FaissIndex:
        if key not in self._faiss:
            self._faiss[key] = self.faiss_loader(key)
        return self._faiss[key]

    def rerank_cache(self, key: str) -> RerankCache:
        if key not in self._rr_cache:
            self._rr_cache[key] = RerankCache(self.rerank_dir(key))
        return self._rr_cache[key]

    def reranker(self, key: str) -> Reranker | None:
        if self.reranker_factory is None:
            return None
        if key not in self._rr:
            self._rr[key] = self.reranker_factory(key)
        return self._rr[key]

    def retrieve(
        self,
        question: str,
        as_of: date | None,
        config_name: str,
        *,
        qid: str | None = None,
        use_llm: bool = True,
    ) -> RetrievalResult:
        return retrieve(question, as_of, config_name, self, qid=qid, use_llm=use_llm)


def _ms(t0: float) -> float:
    return round((time.perf_counter() - t0) * 1000, 2)


def retrieve(
    question: str,
    as_of: date | None,
    config_name: str,
    ctx: RetrievalContext,
    *,
    qid: str | None = None,
    use_llm: bool = True,
) -> RetrievalResult:
    """Truy hồi một câu hỏi theo cấu hình ``config_name``. ``as_of`` (tham số / ``QAItem.as_of`` /
    ô "Áp dụng tại ngày") luôn thắng ngày đọc từ câu hỏi."""
    cfg = ctx.cfg
    sc = cfg.system(config_name)
    timings: dict[str, float] = {}
    t_all = time.perf_counter()

    t0 = time.perf_counter()
    analysis = ctx.analyzer.analyze(question, as_of, use_llm=use_llm and sc.analyzer_llm)
    timings["analyze"] = _ms(t0)
    eff = analysis.as_of
    flt = sc.validity_filter
    allowed = allowed_ids(ctx.catalog, eff, flt)

    dkey = cfg.dense_key(sc)
    qvec = None
    if dkey is not None:
        t0 = time.perf_counter()
        qvec = ctx.encoder.encode(dkey, [question])
        timings["encode"] = _ms(t0)
    t0 = time.perf_counter()
    hy = hybrid_search(
        question,
        bm25=ctx.bm25 if sc.bm25 else None,
        faiss=ctx.faiss(dkey) if dkey else None,
        qvec=qvec,
        allowed=allowed,
        depth=max(cfg.rrf_depth, sc.pool_k),
        pool_k=sc.pool_k,
        rrf_k=cfg.rrf_k,
    )
    timings["hybrid"] = _ms(t0)

    # pool: seed theo hạng hybrid
    order: list[str] = []
    sources: dict[str, list[SourceInfo]] = {}
    base_score: dict[str, float] = {}
    for h in hy.seeds:
        order.append(h.chunk_id)
        base_score[h.chunk_id] = h.score
        srcs = [SourceInfo(source=h.source, rank=h.rank, score=round(h.score, 6))]
        for name, hs in hy.lists.items():
            if h.source == name:
                continue
            for x in hs:
                if x.chunk_id == h.chunk_id:
                    srcs.append(SourceInfo(source=name, rank=x.rank, score=round(x.score, 6)))
                    break
        sources[h.chunk_id] = srcs

    graph_docs: list[SourceInfo] = []
    if sc.graph_expand:
        t0 = time.perf_counter()
        rule = cfg.expand.rule_for(analysis.question_type)
        seeds = [(c, ctx.catalog.get(c).unit_id) for c in order]
        exps = expand_candidates(
            ctx.store,
            seeds,
            as_of=eff if flt else None,
            rule=rule,
            catalog=ctx.catalog,
            sanctions=ctx.sanctions,
            max_chunks=cfg.expand.max_chunks,
            per_node_max=cfg.expand.per_node_max,
            reverse=cfg.expand.reverse_sanctions,
        )
        for x in exps:
            info = SourceInfo(
                source="graph",
                edge_type=x.edge_type,
                hop=x.hop,
                seed=x.seed,
                node=x.node,
                direction=x.direction,
            )
            if x.chunk_id is None:
                graph_docs.append(info)
                continue
            if x.chunk_id not in sources:
                order.append(x.chunk_id)
                sources[x.chunk_id] = []
            sources[x.chunk_id].append(info)
        timings["expand"] = _ms(t0)

    rkey = cfg.reranker_key_for(sc)
    rr_scores: dict[str, float] = {}
    rr_stats = None
    if rkey is not None:
        t0 = time.perf_counter()
        spec = cfg.reranker(rkey)
        rr_scores, st = rerank_scores(
            ctx.reranker(rkey),
            ctx.rerank_cache(rkey),
            rkey,
            spec,
            question,
            [(c, ctx.catalog.get(c).text) for c in order],
        )
        ctx.rerank_totals.setdefault(rkey, RerankStats()).add(st)
        rr_stats = st.to_dict()
        pos = {c: i for i, c in enumerate(order)}
        ranked = sorted(order, key=lambda c: (-rr_scores[c], pos[c]))
        timings["rerank"] = _ms(t0)
    else:
        ranked = list(order)

    notes: list[dict[str, str]] = []
    if flt:
        t0 = time.perf_counter()
        ranked, notes = check_final(ranked, eff, ctx.catalog, ctx.store)
        timings["final_check"] = _ms(t0)

    hits = []
    for i, c in enumerate(ranked[: sc.final_k], 1):
        ch = ctx.catalog.get(c)
        hits.append(
            HitOut(
                chunk_id=c,
                unit_id=ch.unit_id,
                doc_id=ch.doc_id,
                version_ids=list(ch.version_ids),
                effective_from=ch.effective_from,
                effective_to=ch.effective_to,
                score=round(rr_scores.get(c, base_score.get(c, 0.0)), 6),
                rank=i,
                sources=sources[c],
            )
        )
    pool = [
        PoolItem(
            chunk_id=c,
            unit_id=ctx.catalog.get(c).unit_id,
            effective_from=ctx.catalog.get(c).effective_from,
            effective_to=ctx.catalog.get(c).effective_to,
            sources=sources[c],
            rerank_score=round(rr_scores[c], 6) if c in rr_scores else None,
        )
        for c in order
    ]
    timings["total"] = _ms(t_all)

    def minfo(key: str | None, repo: str | None, rev: str | None) -> ModelInfo | None:
        return ModelInfo(key=key, hf_repo=repo, revision=rev) if key and repo else None

    es = cfg.spec(dkey) if dkey else None
    rs = cfg.reranker(rkey) if rkey else None
    return RetrievalResult(
        config_name=config_name,
        qid=qid,
        question=question,
        as_of_param=as_of,
        as_of=eff,
        validity_filter=flt,
        analysis=analysis,
        hits=hits,
        ranked=ranked,
        pool=pool,
        graph_docs=graph_docs,
        final_notes=notes,
        embedding=minfo(dkey, es.hf_repo if es else None, es.revision if es else None),
        reranker=minfo(rkey, rs.hf_repo if rs else None, rs.revision if rs else None),
        llm_model=analysis.llm_model,
        prompt_hash=analysis.prompt_hash,
        rerank_stats=rr_stats,
        timings_ms=timings,
        data_version=ctx.meta.get("data_version"),
        catalog_sha256=ctx.meta.get("catalog_sha256"),
        graph_data_hash=ctx.meta.get("graph_data_hash"),
    )


__all__ = [
    "HitOut",
    "ModelInfo",
    "PoolItem",
    "QueryEncoder",
    "RetrievalContext",
    "RetrievalResult",
    "SourceInfo",
    "retrieve",
]
