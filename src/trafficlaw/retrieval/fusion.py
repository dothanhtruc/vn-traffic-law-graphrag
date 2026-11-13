"""Reciprocal Rank Fusion (Cormack và cs., 2009): ``score(d) = Σ_i 1 / (k + rank_i(d))``.

M10 dùng để đo mốc hybrid BM25 + vector; M11 dùng lại trong ``hybrid``.
"""

from __future__ import annotations

from collections.abc import Sequence

from trafficlaw.retrieval.catalog import Hit


def rrf(lists: Sequence[Sequence[Hit]], *, k: int = 60, top_k: int = 20, source: str = "rrf"):
    """Gộp các danh sách hit (đã xếp hạng). Đồng điểm → ``chunk_id`` tăng dần."""
    acc: dict[str, float] = {}
    for hits in lists:
        for h in hits:
            acc[h.chunk_id] = acc.get(h.chunk_id, 0.0) + 1.0 / (k + h.rank)
    ranked = sorted(acc.items(), key=lambda x: (-x[1], x[0]))[:top_k]
    return [Hit(c, s, i, source) for i, (c, s) in enumerate(ranked, 1)]


__all__ = ["rrf"]
