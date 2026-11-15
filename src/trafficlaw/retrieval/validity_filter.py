"""Lọc hiệu lực (M11), lớp mỏng quanh ``catalog.filter_as_of`` của M10.

Hai chốt chặn:

1. **Trước khi xếp hạng** (hybrid): ``allowed_ids`` = chunk có ``[effective_from, effective_to]``
   (gồm hai đầu) chứa ``as_of`` ⇒ BM25/FAISS chỉ xếp hạng trong tập này; graph expand nhận cùng
   ``as_of`` nên chỉ đi qua cạnh/phiên bản hiệu lực và chỉ ánh xạ ra chunk hiệu lực.
2. **Chunk cuối** (:func:`check_final`): chunk phải phủ ``as_of`` **và** unit gốc của chunk phải có
   phiên bản hiệu lực theo ``GraphStore.version_at`` (không ``repealed``). Phiên bản đó không nằm
   trong ``version_ids`` của chunk (chunk gộp hai trạng thái cùng text) → giữ, ghi cảnh báo
   ``phien_ban_khac``.

A2 (``validity_filter: false``) bỏ cả hai chốt.
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import date

from trafficlaw.graph.store import BaseGraphStore
from trafficlaw.retrieval.catalog import ChunkCatalog, Hit, filter_as_of


def allowed_ids(catalog: ChunkCatalog, as_of: date, enabled: bool) -> frozenset[str] | None:
    return catalog.ids_at(as_of) if enabled else None


def filter_hits(hits: Sequence[Hit], as_of: date, catalog: ChunkCatalog) -> list[Hit]:
    return filter_as_of(hits, as_of, catalog)


def check_final(
    chunk_ids: Sequence[str], as_of: date, catalog: ChunkCatalog, store: BaseGraphStore
) -> tuple[list[str], list[dict[str, str]]]:
    """(chunk giữ lại theo thứ tự, ghi chú ``[{chunk_id, reason}]``). ``reason``:
    ``ngoai_hieu_luc`` / ``unit_khong_hieu_luc`` (bị bỏ), ``phien_ban_khac`` (giữ)."""
    kept: list[str] = []
    notes: list[dict[str, str]] = []
    for cid in chunk_ids:
        c = catalog.by_id.get(cid)
        if c is None or not c.covers(as_of):
            notes.append({"chunk_id": cid, "reason": "ngoai_hieu_luc"})
            continue
        v = store.version_at(c.unit_id, as_of)
        if v is None:
            notes.append({"chunk_id": cid, "reason": "unit_khong_hieu_luc"})
            continue
        if v.id not in c.version_ids:
            notes.append({"chunk_id": cid, "reason": "phien_ban_khac"})
        kept.append(cid)
    return kept, notes


__all__ = ["allowed_ids", "check_final", "filter_hits"]
