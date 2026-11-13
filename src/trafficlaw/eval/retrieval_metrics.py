"""Chỉ số truy hồi tất định (M10, M13 dùng lại).

Với một câu hỏi: ``ranked`` = danh sách ``chunk_id`` đã xếp hạng; ``relevant`` = gold unit →
tập chunk đúng (chunk hiệu lực tại ``as_of`` chứa gold unit, xem
``ChunkCatalog.relevant``).

- ``recall@k`` = tỷ lệ gold unit có ít nhất một chunk đúng trong top-k (cấp unit: Điều gold có
  nhiều Khoản thì một Khoản đúng là đủ).
- ``mrr@k`` = 1 / hạng của chunk đúng đầu tiên trong top-k (0 nếu không có).
- ``ndcg@k`` nhị phân: DCG = Σ_{i ≤ k, chunk i đúng} 1 / log2(i + 1); IDCG = DCG của
  min(|chunk đúng|, k) chunk đúng xếp đầu.

Trung bình theo câu (macro); CI 95% bootstrap theo câu (1.000 lần, seed cố định).
"""

from __future__ import annotations

import math
import random
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

KS = (1, 5, 10, 20)


def recall_at(ranked: Sequence[str], relevant: Mapping[str, set[str]], k: int) -> float:
    if not relevant:
        return 0.0
    top = set(ranked[:k])
    return sum(1 for chunks in relevant.values() if chunks & top) / len(relevant)


def mrr_at(ranked: Sequence[str], relevant: Mapping[str, set[str]], k: int = 10) -> float:
    rel = set().union(*relevant.values()) if relevant else set()
    for i, c in enumerate(ranked[:k], 1):
        if c in rel:
            return 1.0 / i
    return 0.0


def ndcg_at(ranked: Sequence[str], relevant: Mapping[str, set[str]], k: int = 10) -> float:
    rel = set().union(*relevant.values()) if relevant else set()
    if not rel:
        return 0.0
    dcg = sum(1.0 / math.log2(i + 1) for i, c in enumerate(ranked[:k], 1) if c in rel)
    idcg = sum(1.0 / math.log2(i + 1) for i in range(1, min(len(rel), k) + 1))
    return dcg / idcg


@dataclass(frozen=True)
class QueryScore:
    qid: str
    values: dict[str, float]


def score_query(
    qid: str, ranked: Sequence[str], relevant: Mapping[str, set[str]], ks: Sequence[int] = KS
) -> QueryScore:
    v = {f"recall@{k}": recall_at(ranked, relevant, k) for k in ks}
    v["mrr@10"] = mrr_at(ranked, relevant, 10)
    v["ndcg@10"] = ndcg_at(ranked, relevant, 10)
    return QueryScore(qid, v)


def mean(scores: Sequence[QueryScore], metric: str) -> float:
    return sum(s.values[metric] for s in scores) / len(scores) if scores else 0.0


def bootstrap_ci(
    scores: Sequence[QueryScore], metric: str, *, n: int = 1000, seed: int = 42
) -> tuple[float, float] | None:
    """CI 95% (phân vị 2,5 / 97,5) của trung bình ``metric``, lấy mẫu lại câu có hoàn lại."""
    if not scores:
        return None
    vals = [s.values[metric] for s in scores]
    rng = random.Random(seed)
    m = len(vals)
    boots = sorted(sum(vals[rng.randrange(m)] for _ in range(m)) / m for _ in range(n))
    return boots[int(0.025 * n)], boots[min(n - 1, int(0.975 * n))]


def summarize(
    scores: Sequence[QueryScore], *, ci_metrics: Sequence[str] = ("recall@5",), seed: int = 42
) -> dict[str, object]:
    if not scores:
        return {"n": 0}
    out: dict[str, object] = {"n": len(scores)}
    for m in scores[0].values:
        out[m] = mean(scores, m)
    for m in ci_metrics:
        out[f"{m}_ci"] = bootstrap_ci(scores, m, seed=seed)
    return out


__all__ = [
    "KS",
    "QueryScore",
    "bootstrap_ci",
    "mean",
    "mrr_at",
    "ndcg_at",
    "recall_at",
    "score_query",
    "summarize",
]
