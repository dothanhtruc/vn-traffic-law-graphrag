"""Hybrid (M11): BM25 + vector (FAISS), gộp bằng RRF (k = 60), lấy ``pool_k`` (20) chunk seed.

``allowed`` (chunk hiệu lực tại ``as_of``) lọc **trước** khi xếp hạng ở cả hai nguồn (``None`` = A2,
không lọc). Mỗi nguồn lấy ``depth`` (``rrf_depth`` = 100) hit trước khi gộp — như đánh giá M10.
Chỉ một nguồn (B1, B2) → ``pool_k`` hit đầu của nguồn đó.
"""

from __future__ import annotations

from collections.abc import Collection
from dataclasses import dataclass, field

import numpy as np

from trafficlaw.retrieval.bm25 import BM25Index
from trafficlaw.retrieval.catalog import Hit, rerank
from trafficlaw.retrieval.dense import FaissIndex
from trafficlaw.retrieval.fusion import rrf


@dataclass
class HybridOut:
    seeds: list[Hit]
    lists: dict[str, list[Hit]] = field(default_factory=dict)
    """Nguồn (``bm25`` / ``dense:<model>``) → hit trước khi gộp."""


def hybrid_search(
    question: str,
    *,
    bm25: BM25Index | None,
    faiss: FaissIndex | None,
    qvec: np.ndarray | None,
    allowed: Collection[str] | None,
    depth: int,
    pool_k: int,
    rrf_k: int,
) -> HybridOut:
    lists: dict[str, list[Hit]] = {}
    if bm25 is not None:
        lists["bm25"] = bm25.search(question, depth, allowed=allowed)
    if faiss is not None:
        if qvec is None:
            raise ValueError("dense cần vector câu hỏi")
        lists[faiss.source] = faiss.search(qvec, depth, allowed=allowed)[0]
    if not lists:
        raise ValueError("hybrid cần ít nhất một nguồn")
    if len(lists) == 1:
        (only,) = lists.values()
        return HybridOut(rerank(only[:pool_k]), lists)
    return HybridOut(rrf(list(lists.values()), k=rrf_k, top_k=pool_k), lists)


__all__ = ["HybridOut", "hybrid_search"]
