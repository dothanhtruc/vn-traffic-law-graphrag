"""Graph expand (M11): từ chunk seed (hybrid) → chunk liên kết qua đồ thị, kèm provenance.

Chỉ đi qua interface ``GraphStore`` (M6); mọi truy vấn nhận ``as_of`` (``None`` chỉ ở A2 — bỏ lọc
hiệu lực). Ánh xạ nút → chunk (người dùng duyệt 15/11/2026):

- **unit** (Điều/Khoản/Điểm/Phụ lục) → chunk chứa nó và hiệu lực tại ``as_of``
  (:meth:`ChunkCatalog.chunks_of_unit`: Điểm → Khoản chứa nó; Điều chia Khoản → các Khoản, tối đa
  ``per_node_max``);
- **CheTai / DiemGPLX / BienPhapBoSung** (M8) → ``props.unit_id`` (Khoản *nêu* chế tài); cạnh
  ``BI_XU_PHAT``/``BI_TRU_DIEM`` có ``stated_in`` (phiên bản nêu chế tài) → unit của phiên bản đó;
- **VanBan / VanBanNgoai** (HUONG_DAN cấp văn bản, DAN_CHIEU tới văn bản) → không thêm chunk, chỉ
  ghi provenance;
- nút ngữ nghĩa khác (HanhVi, PhuongTien, ChuThe, KhaiNiem) → bỏ.

**Chiều ngược chế tài** (``reverse_sanctions``): cạnh BI_XU_PHAT/BI_TRU_DIEM đi *từ phiên bản hành
vi tới nút chế tài*, nên ``GraphStore.expand`` từ Khoản nêu chế tài không thấy hành vi. Với mỗi
unit seed, các nút chế tài có ``props.unit_id`` = unit đó → ``in_edges`` (lọc ``as_of``) → phiên
bản hành vi (phải hiệu lực) → unit → chunk (hop 1, ``direction = nguoc``).

Seed = mọi unit trong cây con hiệu lực của unit chunk (chunk gồm Khoản + các Điểm). Chunk mở rộng
mới tối đa ``max_chunks`` (thứ tự: hạng seed → hop → chiều → mã nút); chunk đã có trong pool chỉ
được thêm provenance.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date

from trafficlaw.graph.store import (
    DOC_LABELS,
    UNIT_LABELS,
    VERSION_LABEL,
    BaseGraphStore,
    GraphEdge,
    unit_of_version_id,
    version_in_effect,
)
from trafficlaw.retrieval.catalog import ChunkCatalog
from trafficlaw.retrieval.config import ExpandRule

SANCTION_LABELS: tuple[str, ...] = ("CheTai", "DiemGPLX", "BienPhapBoSung")
SANCTION_EDGES: tuple[str, ...] = ("BI_XU_PHAT", "BI_TRU_DIEM")


@dataclass(frozen=True)
class Expansion:
    """Một lần đồ thị dẫn tới ``chunk_id`` (``None`` = nút văn bản, chỉ provenance)."""

    chunk_id: str | None
    seed: str
    """chunk_id seed."""
    node: str
    """Nút đích (unit, nút chế tài, hoặc VanBan)."""
    edge_type: str
    hop: int
    direction: str
    """``xuoi`` (GraphStore.expand) | ``nguoc`` (chế tài → hành vi)."""


def sanction_index(store: BaseGraphStore) -> dict[str, list[str]]:
    """unit nêu chế tài → id các nút CheTai/DiemGPLX/BienPhapBoSung (một lần khi nạp)."""
    out: dict[str, list[str]] = {}
    for label in SANCTION_LABELS:
        for n in store.nodes_by_label(label):
            u = n.props.get("unit_id")
            if u:
                out.setdefault(str(u), []).append(n.id)
    return {k: sorted(v) for k, v in sorted(out.items())}


def _edge_type_by_node(edges: Sequence[GraphEdge], nodes: Mapping[str, int]) -> dict[str, str]:
    """Nút đích → loại cạnh đầu tiên (theo thứ tự cạnh) chạm tới nó."""
    out: dict[str, str] = {}
    for e in edges:
        for end in (e.src, e.dst):
            u = unit_of_version_id(end)
            if u in nodes and nodes[u] > 0:
                out.setdefault(u, e.type)
    return out


def _stated_units(edges: Sequence[GraphEdge]) -> dict[str, set[str]]:
    """Nút chế tài → unit của ``stated_in`` trên cạnh BI_XU_PHAT/BI_TRU_DIEM."""
    out: dict[str, set[str]] = {}
    for e in edges:
        st = e.props.get("stated_in") if e.type in SANCTION_EDGES else None
        if st:
            out.setdefault(e.dst, set()).add(unit_of_version_id(str(st)))
    return out


def expand_seed(
    store: BaseGraphStore,
    seed_chunk: str,
    seed_unit: str,
    *,
    as_of: date | None,
    rule: ExpandRule,
    catalog: ChunkCatalog,
    sanctions: Mapping[str, Sequence[str]],
    per_node_max: int,
    reverse: bool,
) -> list[Expansion]:
    """Các lần mở rộng từ một chunk seed (chưa áp giới hạn tổng, chưa bỏ trùng)."""
    units = store.subtree(seed_unit, as_of=as_of)
    sub = store.expand(units, edge_types=rule.edge_types, as_of=as_of, hops=rule.hops)
    targets = {n: h for n, h in sub.nodes.items() if h > 0}
    nodes = store.get_nodes(sorted(targets))
    etype = _edge_type_by_node(sub.edges, sub.nodes)
    stated = _stated_units(sub.edges)
    out: list[Expansion] = []

    def add_unit(unit: str, node: str, et: str, hop: int, direction: str) -> None:
        for c in catalog.chunks_of_unit(unit, as_of)[:per_node_max]:
            out.append(Expansion(c, seed_chunk, node, et, hop, direction))

    for nid in sorted(targets, key=lambda n: (targets[n], n)):
        n = nodes.get(nid)
        if n is None:
            continue
        hop, et = targets[nid], etype.get(nid, "?")
        if n.label in UNIT_LABELS:
            add_unit(nid, nid, et, hop, "xuoi")
        elif n.label in SANCTION_LABELS:
            us = {str(n.props["unit_id"])} if n.props.get("unit_id") else set()
            for u in sorted(us | stated.get(nid, set())):
                add_unit(u, nid, et, hop, "xuoi")
        elif n.label in DOC_LABELS:
            out.append(Expansion(None, seed_chunk, nid, et, hop, "xuoi"))

    rev_types = [t for t in rule.edge_types if t in SANCTION_EDGES]
    if reverse and rev_types:
        seen: set[str] = set()
        for u in units:
            for sem in sanctions.get(u, ()):
                for e in store.in_edges(sem, types=rev_types, as_of=as_of):
                    src = store.get_node(e.src)
                    if src is None or src.label != VERSION_LABEL:
                        continue
                    if as_of is not None and not version_in_effect(src, as_of):
                        continue
                    beh = str(src.props.get("unit_id") or unit_of_version_id(src.id))
                    if beh in units or beh in seen:
                        continue
                    seen.add(beh)
                    add_unit(beh, sem, e.type, 1, "nguoc")
    return out


def expand_candidates(
    store: BaseGraphStore,
    seeds: Sequence[tuple[str, str]],
    *,
    as_of: date | None,
    rule: ExpandRule,
    catalog: ChunkCatalog,
    sanctions: Mapping[str, Sequence[str]],
    max_chunks: int = 30,
    per_node_max: int = 5,
    reverse: bool = True,
) -> list[Expansion]:
    """``seeds`` = [(chunk_id, unit_id)] theo hạng. Trả mọi provenance cho chunk seed + chunk
    mới (≤ ``max_chunks`` chunk mới) + nút văn bản, tất định."""
    seed_ids = {c for c, _ in seeds}
    new: set[str] = set()
    out: list[Expansion] = []
    seen: set[tuple[str | None, str, str]] = set()
    for chunk_id, unit in seeds:
        exps = expand_seed(
            store,
            chunk_id,
            unit,
            as_of=as_of,
            rule=rule,
            catalog=catalog,
            sanctions=sanctions,
            per_node_max=per_node_max,
            reverse=reverse,
        )
        exps.sort(key=lambda x: (x.hop, x.direction != "xuoi", x.node, x.chunk_id or ""))
        for x in exps:
            if x.chunk_id == chunk_id:
                continue  # đồ thị quay về chính seed
            k = (x.chunk_id, x.seed, x.node)
            if k in seen:
                continue
            if x.chunk_id is not None and x.chunk_id not in seed_ids and x.chunk_id not in new:
                if len(new) >= max_chunks:
                    continue
                new.add(x.chunk_id)
            seen.add(k)
            out.append(x)
    return out


__all__ = [
    "SANCTION_EDGES",
    "SANCTION_LABELS",
    "Expansion",
    "expand_candidates",
    "expand_seed",
    "sanction_index",
]
