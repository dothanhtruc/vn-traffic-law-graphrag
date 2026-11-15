"""Độ phủ liên kết (M11, người dùng duyệt 15/11/2026): đo lợi ích graph expand trên val/train.

Câu val/train được sinh từ **một** chunk, nên Recall@k theo gold khó cho thấy lợi ích của việc
mở rộng đồ thị. Chỉ số phụ này hỏi: với câu mà gold có **liên kết sang chunk khác**, các chunk
liên kết đó có lọt top-k không?

Đơn vị liên kết của một câu (tại ``as_of``, từ cây con hiệu lực của mỗi gold unit):

- ``che_tai``: cạnh ``BI_XU_PHAT``/``BI_TRU_DIEM`` có ``nguon = dan_chieu`` từ phiên bản hiệu lực
  → unit của ``stated_in`` (Khoản nêu chế tài);
- ``dan_chieu``: ``DAN_CHIEU`` hiệu lực (không ``can_cu``, không ``quan_he``) tới unit thuộc
  **Điều khác**.

Bỏ đích trùng/tổ tiên/con cháu của gold (cùng chunk) và đích không có chunk hiệu lực. Độ phủ một
câu = tỷ lệ đơn vị liên kết có chunk đúng trong top-k; trung bình trên các câu có ít nhất một
liên kết. Đánh giá G chính thức là việc của M13 trên test.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from datetime import date
from typing import Any

from trafficlaw.graph.store import UNIT_LABELS, BaseGraphStore, unit_of_version_id
from trafficlaw.retrieval.catalog import ChunkCatalog, is_same_or_related

_DIEU = re.compile(r"^([^/]+/D\d+[a-z]?)")


def dieu_of(unit_id: str) -> str | None:
    m = _DIEU.match(unit_id)
    return m[1] if m else None


def linked_units(store: BaseGraphStore, gold_units: Sequence[str], as_of: date) -> dict[str, str]:
    """Đơn vị liên kết → loại (``che_tai`` | ``dan_chieu``), sắp theo mã."""
    out: dict[str, str] = {}
    for g in gold_units:
        gd = dieu_of(g)
        for u in store.subtree(g, as_of=as_of):
            v = store.version_at(u, as_of)
            if v is None:
                continue
            for e in store.out_edges(v.id, types=["BI_XU_PHAT", "BI_TRU_DIEM"], as_of=as_of):
                st = e.props.get("stated_in")
                if e.props.get("nguon") == "dan_chieu" and st:
                    out.setdefault(unit_of_version_id(str(st)), "che_tai")
            for e in store.references_from(u, as_of):
                if e.props.get("can_cu"):
                    continue
                n = store.get_node(e.dst)
                if n is None or n.label not in UNIT_LABELS:
                    continue
                if dieu_of(e.dst) and dieu_of(e.dst) != gd:
                    out.setdefault(e.dst, "dan_chieu")
    return {
        u: k
        for u, k in sorted(out.items())
        if not any(is_same_or_related(u, g) for g in gold_units)
    }


def linked_coverage(
    store: BaseGraphStore,
    catalog: ChunkCatalog,
    items: Sequence[tuple[str, Sequence[str], date, Sequence[str]]],
    *,
    k: int = 5,
) -> dict[str, Any]:
    """``items`` = [(qid, gold_units, as_of, ranked chunk_ids)]."""
    per: list[float] = []
    by_kind: dict[str, list[float]] = {"che_tai": [], "dan_chieu": []}
    n_links = 0
    for _qid, gold, d, ranked in items:
        links = linked_units(store, gold, d)
        top = set(ranked[:k])
        vals: list[float] = []
        for u, kind in links.items():
            rel = catalog.relevant([u], d)[u]
            if not rel:
                continue
            hit = 1.0 if rel & top else 0.0
            vals.append(hit)
            by_kind[kind].append(hit)
        if vals:
            per.append(sum(vals) / len(vals))
            n_links += len(vals)
    return {
        "k": k,
        "n_cau_co_lien_ket": len(per),
        "n_lien_ket": n_links,
        "do_phu": sum(per) / len(per) if per else None,
        "theo_loai": {
            kind: {"n": len(v), "do_phu": sum(v) / len(v) if v else None}
            for kind, v in by_kind.items()
        },
    }


__all__ = ["dieu_of", "linked_coverage", "linked_units"]
