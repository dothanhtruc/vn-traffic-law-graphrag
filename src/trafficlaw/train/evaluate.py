"""Đánh giá trong lúc huấn luyện M14 (không torch; model đưa vào qua hàm).

- **Embedder**: dense-only trên val (489 câu, chia theo Điều) — encode lại toàn bộ cửa sổ chunk
  (M10) + câu hỏi bằng model đang train, FAISS chính xác, lọc as_of **trước** khi xếp hạng, chỉ
  số cấp unit như M10 (R@k, MRR@10, nDCG@10, CI bootstrap).
- **Reranker**: rerank-only trên **pool cố định** của val (truy hồi G của M11, trước rerank) —
  tách khỏi thay đổi embedding. Điểm chunk = max cửa sổ cặp (như ``retrieval/rerank.py``); xếp
  pool theo điểm giảm dần (hoà → thứ tự pool), chỉ giữ chunk hiệu lực tại as_of.

Không dùng test.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Any

import numpy as np

from trafficlaw.eval.retrieval_eval import EvalQuery, run_retriever
from trafficlaw.eval.retrieval_metrics import QueryScore, score_query, summarize
from trafficlaw.retrieval.catalog import ChunkCatalog
from trafficlaw.retrieval.dense import FaissIndex, Window
from trafficlaw.retrieval.rerank import pair_windows
from trafficlaw.utils.dates import parse_iso
from trafficlaw.utils.jsonl import read_jsonl

EncodeFn = Callable[[Sequence[str], str], np.ndarray]
"""(text, ``"query"`` | ``"doc"``) → vector chuẩn hoá L2 (prompt do hàm tự gắn)."""

PairScoreFn = Callable[[Sequence[tuple[str, str]]], list[float]]

CI_METRICS = ("recall@5", "mrr@10")


def selection_key(m: Mapping[str, Any]) -> tuple[float, float]:
    """Thứ tự chọn checkpoint (khai báo trước): R@5 rồi MRR@10; hoà → checkpoint sớm hơn
    (so sánh ``>`` chặt ở vòng train)."""
    return (round(float(m["recall@5"]), 10), round(float(m["mrr@10"]), 10))


def dense_eval(
    encode: EncodeFn,
    windows: Sequence[Window],
    catalog: ChunkCatalog,
    queries: Sequence[EvalQuery],
    *,
    depth: int = 20,
    seed: int = 42,
) -> dict[str, Any]:
    vecs = encode([w.text for w in windows], "doc")
    idx = FaissIndex.build(vecs, [(w.chunk_id, w.k) for w in windows], "dense:train")
    qv = encode([q.question for q in queries], "query")

    def retr(qs, allowed):
        return idx.search(qv, depth, allowed=list(allowed))

    sc = run_retriever(retr, queries, catalog, filtered=True)
    return summarize(sc, ci_metrics=CI_METRICS, seed=seed)


def load_pools(path: str | Path) -> dict[str, dict[str, Any]]:
    """qid → {question, as_of, pool (chunk_id theo thứ tự pool), base (điểm rerank gốc)} từ
    ``RetrievalResult`` JSONL (M11)."""
    out: dict[str, dict[str, Any]] = {}
    for r in read_jsonl(path):
        out[str(r["qid"])] = {
            "question": r["question"],
            "as_of": parse_iso(str(r["as_of"])),
            "pool": [p["chunk_id"] for p in r["pool"]],
            "base": {p["chunk_id"]: p.get("rerank_score") for p in r["pool"]},
        }
    return out


def rank_pool(
    pool: Sequence[str], scores: Mapping[str, float | None], live: frozenset[str]
) -> list[str]:
    idx = {c: i for i, c in enumerate(pool)}
    keep = [c for c in pool if c in live and scores.get(c) is not None]
    return sorted(keep, key=lambda c: (-float(scores[c] or 0.0), idx[c]))


def rerank_eval(
    score_pairs: PairScoreFn | None,
    count_tokens: Callable[[str], int] | None,
    pools: Mapping[str, Mapping[str, Any]],
    queries: Sequence[EvalQuery],
    catalog: ChunkCatalog,
    *,
    max_length: int = 512,
    seed: int = 42,
    use_base: bool = False,
) -> dict[str, Any]:
    """``use_base`` → xếp bằng điểm rerank gốc đã lưu trong pool (không cần model)."""
    scores_all: list[QueryScore] = []
    n_pairs = 0
    for q in queries:
        p = pools.get(q.qid)
        if p is None:
            continue
        pool = list(p["pool"])
        if use_base:
            sc: dict[str, float | None] = dict(p["base"])
        else:
            assert score_pairs is not None and count_tokens is not None
            plan: list[tuple[str, Window]] = []
            for cid in pool:
                for w in pair_windows(
                    cid, q.question, catalog.get(cid).text, count_tokens, max_length
                ):
                    plan.append((cid, w))
            vals = score_pairs([(q.question, w.text) for _, w in plan])
            n_pairs += len(plan)
            sc = {}
            for (cid, _), v in zip(plan, vals, strict=True):
                cur = sc.get(cid)
                sc[cid] = v if cur is None else max(cur, v)
        ranked = rank_pool(pool, sc, catalog.ids_at(q.as_of))
        rel = catalog.relevant(list(q.gold_units), q.as_of)
        scores_all.append(score_query(q.qid, ranked, rel))
    res = summarize(scores_all, ci_metrics=CI_METRICS, seed=seed)
    res["n_pairs"] = n_pairs
    return res


def windows_from_rows(rows: Sequence[Mapping[str, Any]]) -> list[Window]:
    return [
        Window(str(r["chunk_id"]), int(r["k"]), str(r["text"]), int(r["n_tokens"]),
               bool(r["truncated"]))
        for r in rows
    ]  # fmt: skip


__all__ = [
    "CI_METRICS",
    "EncodeFn",
    "PairScoreFn",
    "dense_eval",
    "load_pools",
    "rank_pool",
    "rerank_eval",
    "selection_key",
    "windows_from_rows",
]
