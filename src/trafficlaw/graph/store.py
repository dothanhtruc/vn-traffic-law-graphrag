"""GraphStore (M6): một interface truy vấn đồ thị, hai cài đặt (``EmbeddedStore``, ``Neo4jStore``).

Đầu vào duy nhất là các file JSONL do M5 sinh (``nodes.jsonl``, ``edges_struct.jsonl``,
``edges_legal.jsonl``). Module này **không** import nội bộ của M5 (``build.py``,
``references.py``).

Thiết kế: mỗi store chỉ cài vài hàm *nguyên thuỷ* (lấy nút theo id, lấy cạnh vào/ra theo loại,
liệt kê theo nhãn/loại, ghi, xoá). Toàn bộ logic truy vấn và **ngữ nghĩa hiệu lực theo ngày**
nằm trong :class:`BaseGraphStore` và chạy bằng Python ⇒ hai store không thể khác nhau về ngữ
nghĩa; chỉ còn khác ở lớp lưu trữ, và lớp đó được kiểm tra bằng ``--verify-store``.

Ngữ nghĩa ``as_of`` (CLAUDE.md mục 8 "Quy ước GraphStore (M6)"):

- Phiên bản: :func:`pick_version` trùng ``ingest.versions.select_version`` — khoảng
  ``[effective_from, effective_to]`` gồm cả hai đầu, ``effective_from = null`` → không hiệu lực,
  phiên bản ``repealed`` → ``None`` (trừ khi ``include_repealed``).
- Cạnh có trường hiệu lực (khoá ``effective_from``/``effective_to`` có mặt trong ``props``, kể
  cả khi bằng ``null`` — tức mọi cạnh pháp lý) chỉ được giữ khi ``as_of`` nằm trong khoảng của
  cạnh. Cạnh cấu trúc (không có các khoá này) không bị lọc. ``as_of = None`` → không lọc.
- DAN_CHIEU đi từ PhienBan: ``references_from`` lấy phiên bản hiệu lực tại ``as_of`` rồi mới lấy
  cạnh. Cạnh có ``props.quan_he`` (``chinh_unit`` / ``to_tien``) bị bỏ mặc định.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from abc import ABC, abstractmethod
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from types import TracebackType
from typing import Any, Literal, Protocol, runtime_checkable

from trafficlaw.utils.dates import in_effect, parse_iso
from trafficlaw.utils.jsonl import read_jsonl

logger = logging.getLogger(__name__)

#: Đổi khi cách lưu trong store thay đổi → ``data_hash`` đổi → Neo4j nạp lại.
LOADER_VERSION = "m6-1"
GRAPH_FILES: tuple[str, ...] = ("nodes.jsonl", "edges_struct.jsonl", "edges_legal.jsonl")

UNIT_LABELS: tuple[str, ...] = ("Phan", "Chuong", "Muc", "Dieu", "Khoan", "Diem", "PhuLuc")
DOC_LABELS: tuple[str, ...] = ("VanBan", "VanBanNgoai")
VERSION_LABEL = "PhienBan"
AMENDMENT_TYPES: tuple[str, ...] = ("SUA_DOI", "BAI_BO", "THAY_THE")
SELF_REF_PROP = "quan_he"
EFFECT_KEYS: tuple[str, ...] = ("effective_from", "effective_to")
MAX_HOPS = 2

Direction = Literal["out", "in", "both"]


# --------------------------------------------------------------------------- model


def canonical_json(obj: Any) -> str:
    """JSON tất định (khoá sắp xếp, giữ Unicode) — dùng cho hash và so sánh."""
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)


def edge_key(etype: str, src: str, dst: str, props: Mapping[str, Any]) -> str:
    """Khoá phân biệt cạnh song song: ``sha1(type, src, dst, props)`` (16 ký tự hex)."""
    return hashlib.sha1(canonical_json([etype, src, dst, dict(props)]).encode()).hexdigest()[:16]


@dataclass(frozen=True)
class GraphNode:
    """Nút đồ thị. Không sửa ``props`` của đối tượng trả về từ store."""

    id: str
    label: str
    props: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "label": self.label, "props": self.props}

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> GraphNode:
        return cls(id=d["id"], label=d["label"], props=dict(d.get("props") or {}))


@dataclass(frozen=True)
class GraphEdge:
    """Cạnh có hướng; ``key`` phân biệt các cạnh song song cùng (type, src, dst)."""

    type: str
    src: str
    dst: str
    props: dict[str, Any]
    key: str

    @classmethod
    def make(
        cls, etype: str, src: str, dst: str, props: Mapping[str, Any] | None = None
    ) -> GraphEdge:
        p = dict(props or {})
        return cls(type=etype, src=src, dst=dst, props=p, key=edge_key(etype, src, dst, p))

    @classmethod
    def from_dict(cls, d: Mapping[str, Any]) -> GraphEdge:
        return cls.make(d["type"], d["src"], d["dst"], d.get("props"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "src": self.src,
            "dst": self.dst,
            "key": self.key,
            "props": self.props,
        }

    @property
    def sort_key(self) -> tuple[str, str, str, str]:
        return (self.type, self.src, self.dst, self.key)


@dataclass
class Subgraph:
    """Kết quả ``expand``: ``nodes`` = id → số hop nhỏ nhất (seed = 0); cạnh đã đi qua."""

    nodes: dict[str, int]
    edges: list[GraphEdge]

    def to_dict(self) -> dict[str, Any]:
        return {
            "nodes": [[k, self.nodes[k]] for k in sorted(self.nodes)],
            "edges": [e.to_dict() for e in self.edges],
        }


def sort_edges(edges: Iterable[GraphEdge]) -> list[GraphEdge]:
    return sorted(edges, key=lambda e: e.sort_key)


def sort_nodes(nodes: Iterable[GraphNode]) -> list[GraphNode]:
    return sorted(nodes, key=lambda n: n.id)


# --------------------------------------------------------------------------- hiệu lực


def _iso(v: Any) -> date | None:
    if v is None or isinstance(v, date):
        return v
    return parse_iso(str(v))


def has_effect(edge: GraphEdge) -> bool:
    """Cạnh có trường hiệu lực (mọi cạnh pháp lý của M5) → bị lọc theo ``as_of``."""
    return any(k in edge.props for k in EFFECT_KEYS)


def edge_in_effect(edge: GraphEdge, as_of: date | None) -> bool:
    """``as_of = None`` hoặc cạnh không có trường hiệu lực → True; ngược lại ``in_effect``."""
    if as_of is None or not has_effect(edge):
        return True
    return in_effect(
        as_of, _iso(edge.props.get("effective_from")), _iso(edge.props.get("effective_to"))
    )


def version_in_effect(node: GraphNode, as_of: date, *, include_repealed: bool = False) -> bool:
    p = node.props
    if not in_effect(as_of, _iso(p.get("effective_from")), _iso(p.get("effective_to"))):
        return False
    return include_repealed or p.get("status") != "repealed"


def pick_version(
    versions: Sequence[GraphNode], as_of: date, *, include_repealed: bool = False
) -> GraphNode | None:
    """Như ``ingest.versions.select_version``: phiên bản đầu tiên (theo ``version``) chứa
    ``as_of``; nếu đó là bản ``repealed`` mà không ``include_repealed`` → ``None``."""
    for v in sorted(versions, key=lambda n: int(n.props.get("version", 0))):
        p = v.props
        if in_effect(as_of, _iso(p.get("effective_from")), _iso(p.get("effective_to"))):
            if p.get("status") == "repealed" and not include_repealed:
                return None
            return v
    return None


def unit_of_version_id(node_id: str) -> str:
    """``ND168-2024/D6/K3/m@v1`` → ``ND168-2024/D6/K3/m``; id khác giữ nguyên."""
    base, sep, ver = node_id.rpartition("@v")
    return base if sep and ver.isdigit() else node_id


# --------------------------------------------------------------------------- file JSONL


def load_graph_dir(graph_dir: str | Path) -> tuple[list[GraphNode], list[GraphEdge]]:
    """Đọc ``nodes.jsonl`` + ``edges_struct.jsonl`` + ``edges_legal.jsonl``."""
    d = Path(graph_dir)
    missing = [n for n in GRAPH_FILES if not (d / n).is_file()]
    if missing:
        raise FileNotFoundError(f"Thiếu file đồ thị trong {d}: {missing}")
    nodes = [GraphNode.from_dict(r) for r in read_jsonl(d / GRAPH_FILES[0])]
    edges = [GraphEdge.from_dict(r) for n in GRAPH_FILES[1:] for r in read_jsonl(d / n)]
    return nodes, edges


def data_hash(graph_dir: str | Path) -> str:
    """sha256 của ``LOADER_VERSION`` + nội dung 3 file đồ thị."""
    d = Path(graph_dir)
    h = hashlib.sha256(LOADER_VERSION.encode())
    for name in GRAPH_FILES:
        h.update(name.encode())
        h.update(hashlib.sha256((d / name).read_bytes()).digest())
    return h.hexdigest()


def count_items(nodes: Iterable[GraphNode], edges: Iterable[GraphEdge]) -> dict[str, Any]:
    """Số nút theo nhãn, số cạnh theo loại (khoá sắp xếp) — cùng dạng ``GraphStore.count``."""
    nc: dict[str, int] = {}
    ec: dict[str, int] = {}
    for n in nodes:
        nc[n.label] = nc.get(n.label, 0) + 1
    for e in edges:
        ec[e.type] = ec.get(e.type, 0) + 1
    return {"nodes": dict(sorted(nc.items())), "edges": dict(sorted(ec.items()))}


# --------------------------------------------------------------------------- interface


@runtime_checkable
class GraphStore(Protocol):
    """Interface đọc/ghi đồ thị dùng chung cho M8, M11, M15."""

    def get_node(self, node_id: str) -> GraphNode | None: ...
    def get_nodes(self, ids: Sequence[str]) -> dict[str, GraphNode]: ...
    def nodes_by_label(self, label: str, *, doc_id: str | None = None) -> list[GraphNode]: ...
    def edges_by_type(self, etype: str) -> list[GraphEdge]: ...
    def count(self) -> dict[str, Any]: ...
    def parent(self, unit_id: str) -> str | None: ...
    def ancestors(self, unit_id: str) -> list[str]: ...
    def children(self, unit_id: str, *, as_of: date | None = None) -> list[str]: ...
    def subtree(self, unit_id: str, *, as_of: date | None = None) -> list[str]: ...
    def versions(self, unit_id: str) -> list[GraphNode]: ...
    def version_at(
        self, unit_id: str, as_of: date, *, include_repealed: bool = False
    ) -> GraphNode | None: ...
    def out_edges(
        self, node_id: str, *, types: Sequence[str] | None = None, as_of: date | None = None
    ) -> list[GraphEdge]: ...
    def in_edges(
        self, node_id: str, *, types: Sequence[str] | None = None, as_of: date | None = None
    ) -> list[GraphEdge]: ...
    def references_from(
        self, unit_id: str, as_of: date, *, include_self: bool = False
    ) -> list[GraphEdge]: ...
    def references_to(
        self, unit_id: str, as_of: date, *, include_self: bool = False
    ) -> list[GraphEdge]: ...
    def amendments_of(self, node_id: str, *, as_of: date | None = None) -> list[GraphEdge]: ...
    def guidance_for(self, node_id: str, *, as_of: date | None = None) -> list[GraphEdge]: ...
    def expand(
        self,
        seeds: Sequence[str],
        *,
        edge_types: Sequence[str],
        as_of: date | None = None,
        hops: int = 1,
        direction: Direction = "both",
        include_self: bool = False,
        through_documents: bool = False,
    ) -> Subgraph: ...
    def upsert_nodes(self, nodes: Sequence[GraphNode]) -> None: ...
    def upsert_edges(self, edges: Sequence[GraphEdge]) -> None: ...
    def clear(self) -> None: ...
    def meta(self) -> dict[str, Any] | None: ...
    def set_meta(self, meta: Mapping[str, Any]) -> None: ...
    def close(self) -> None: ...


class BaseGraphStore(ABC):
    """Logic truy vấn chung; lớp con chỉ cài các hàm nguyên thuỷ trừu tượng bên dưới."""

    # ---- nguyên thuỷ -------------------------------------------------------------------
    @abstractmethod
    def get_nodes(self, ids: Sequence[str]) -> dict[str, GraphNode]:
        """id → nút (id không tồn tại bị bỏ qua)."""

    @abstractmethod
    def _edges(
        self, ids: Sequence[str], types: Sequence[str] | None, direction: Literal["out", "in"]
    ) -> list[GraphEdge]:
        """Cạnh ra (``out``) / vào (``in``) của các nút ``ids``, lọc theo loại (chưa lọc ngày)."""

    @abstractmethod
    def nodes_by_label(self, label: str, *, doc_id: str | None = None) -> list[GraphNode]: ...

    @abstractmethod
    def edges_by_type(self, etype: str) -> list[GraphEdge]: ...

    @abstractmethod
    def count(self) -> dict[str, Any]: ...

    @abstractmethod
    def upsert_nodes(self, nodes: Sequence[GraphNode]) -> None: ...

    @abstractmethod
    def upsert_edges(self, edges: Sequence[GraphEdge]) -> None:
        """Ghi cạnh; đầu mút chưa có → ``KeyError`` (không tạo cạnh treo)."""

    @abstractmethod
    def clear(self) -> None: ...

    @abstractmethod
    def meta(self) -> dict[str, Any] | None: ...

    @abstractmethod
    def set_meta(self, meta: Mapping[str, Any]) -> None: ...

    def ensure_schema(self) -> None:  # noqa: B027 — mặc định không cần gì
        """Tạo ràng buộc/chỉ mục (Neo4j)."""

    def close(self) -> None:  # noqa: B027
        """Giải phóng kết nối (Neo4j)."""

    def versions_map(self, unit_ids: Sequence[str]) -> dict[str, list[GraphNode]]:
        """unit → các PhienBan (sắp theo ``version``). Neo4j ghi đè bằng một truy vấn."""
        es = self._edges(unit_ids, ["CO_PHIEN_BAN"], "out")
        nodes = self.get_nodes(sorted({e.dst for e in es}))
        out: dict[str, list[GraphNode]] = {u: [] for u in unit_ids}
        for e in es:
            if e.dst in nodes:
                out.setdefault(e.src, []).append(nodes[e.dst])
        return {u: _sort_versions(vs) for u, vs in out.items()}

    def __enter__(self) -> BaseGraphStore:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close()

    # ---- nút ---------------------------------------------------------------------------
    def get_node(self, node_id: str) -> GraphNode | None:
        return self.get_nodes([node_id]).get(node_id)

    # ---- cấu trúc ----------------------------------------------------------------------
    def parent(self, unit_id: str) -> str | None:
        """Cha theo THUOC (VanBan → None)."""
        dsts = sorted(e.dst for e in self._edges([unit_id], ["THUOC"], "out"))
        return dsts[0] if dsts else None

    def ancestors(self, unit_id: str) -> list[str]:
        """Tổ tiên từ gần tới xa (kết thúc ở VanBan)."""
        out: list[str] = []
        seen = {unit_id}
        cur = self.parent(unit_id)
        while cur is not None and cur not in seen:
            out.append(cur)
            seen.add(cur)
            cur = self.parent(cur)
        return out

    def _children_map(self, ids: Sequence[str], as_of: date | None) -> dict[str, list[str]]:
        """Con trực tiếp của mỗi id, thứ tự theo chuỗi KE_TIEP; lọc theo ``as_of`` nếu có."""
        by_parent: dict[str, set[str]] = {i: set() for i in ids}
        for e in self._edges(ids, ["THUOC"], "in"):
            by_parent.setdefault(e.dst, set()).add(e.src)
        kids = sorted({k for ks in by_parent.values() for k in ks})
        if not kids:
            return {i: [] for i in ids}
        nxt: dict[str, str] = {}
        for e in sort_edges(self._edges(kids, ["KE_TIEP"], "out")):
            nxt.setdefault(e.src, e.dst)
        keep: set[str] | None = None
        if as_of is not None:
            vm = self.versions_map(kids)
            keep = {k for k in kids if pick_version(vm.get(k, []), as_of) is not None}
        out: dict[str, list[str]] = {}
        for p in ids:
            sib = by_parent.get(p, set())
            ordered = _chain_order(sib, nxt)
            out[p] = [k for k in ordered if keep is None or k in keep]
        return out

    def children(self, unit_id: str, *, as_of: date | None = None) -> list[str]:
        """Con trực tiếp theo thứ tự văn bản (KE_TIEP); có ``as_of`` → bỏ con không có phiên
        bản hiệu lực (chưa được bổ sung hoặc đã bị bãi bỏ)."""
        return self._children_map([unit_id], as_of)[unit_id]

    def subtree(self, unit_id: str, *, as_of: date | None = None) -> list[str]:
        """Duyệt trước (gốc đầu tiên, luôn có mặt); con bị lọc theo ``as_of`` kéo theo cả cây
        con của nó."""
        cmap: dict[str, list[str]] = {}
        frontier = [unit_id]
        seen = {unit_id}
        while frontier:
            m = self._children_map(frontier, as_of)
            cmap.update(m)
            frontier = [c for f in frontier for c in m[f] if c not in seen]
            seen.update(frontier)
        out: list[str] = []
        stack = [unit_id]
        while stack:
            cur = stack.pop()
            out.append(cur)
            stack.extend(reversed(cmap.get(cur, [])))
        return out

    # ---- phiên bản ---------------------------------------------------------------------
    def versions(self, unit_id: str) -> list[GraphNode]:
        return self.versions_map([unit_id]).get(unit_id, [])

    def version_at(
        self, unit_id: str, as_of: date, *, include_repealed: bool = False
    ) -> GraphNode | None:
        return pick_version(self.versions(unit_id), as_of, include_repealed=include_repealed)

    # ---- cạnh --------------------------------------------------------------------------
    def out_edges(
        self, node_id: str, *, types: Sequence[str] | None = None, as_of: date | None = None
    ) -> list[GraphEdge]:
        es = self._edges([node_id], _types(types), "out")
        return sort_edges(e for e in es if edge_in_effect(e, as_of))

    def in_edges(
        self, node_id: str, *, types: Sequence[str] | None = None, as_of: date | None = None
    ) -> list[GraphEdge]:
        es = self._edges([node_id], _types(types), "in")
        return sort_edges(e for e in es if edge_in_effect(e, as_of))

    def references_from(
        self, unit_id: str, as_of: date, *, include_self: bool = False
    ) -> list[GraphEdge]:
        """DAN_CHIEU từ phiên bản của ``unit_id`` hiệu lực tại ``as_of``."""
        v = self.version_at(unit_id, as_of)
        if v is None:
            return []
        es = self.out_edges(v.id, types=["DAN_CHIEU"], as_of=as_of)
        return [e for e in es if include_self or SELF_REF_PROP not in e.props]

    def references_to(
        self, unit_id: str, as_of: date, *, include_self: bool = False
    ) -> list[GraphEdge]:
        """DAN_CHIEU trỏ tới ``unit_id`` từ các phiên bản hiệu lực tại ``as_of``."""
        es = self.in_edges(unit_id, types=["DAN_CHIEU"], as_of=as_of)
        return [e for e in es if include_self or SELF_REF_PROP not in e.props]

    def amendments_of(self, node_id: str, *, as_of: date | None = None) -> list[GraphEdge]:
        """SUA_DOI / BAI_BO / THAY_THE trỏ trực tiếp tới nút (unit hoặc VanBan)."""
        return self.in_edges(node_id, types=AMENDMENT_TYPES, as_of=as_of)

    def guidance_for(self, node_id: str, *, as_of: date | None = None) -> list[GraphEdge]:
        """HUONG_DAN trỏ trực tiếp tới nút (src = VanBan hướng dẫn)."""
        return self.in_edges(node_id, types=["HUONG_DAN"], as_of=as_of)

    # ---- mở rộng -----------------------------------------------------------------------
    def expand(
        self,
        seeds: Sequence[str],
        *,
        edge_types: Sequence[str],
        as_of: date | None = None,
        hops: int = 1,
        direction: Direction = "both",
        include_self: bool = False,
        through_documents: bool = False,
    ) -> Subgraph:
        """Mở rộng BFS ở mức unit, tối đa ``hops`` (≤ 2) bước.

        Mỗi bước, với mỗi unit ở biên: lấy cạnh thuộc ``edge_types`` đi ra/vào (theo
        ``direction``) từ chính unit **và** từ PhienBan của nó (có ``as_of`` → chỉ phiên bản hiệu
        lực). Cạnh có trường hiệu lực bị lọc theo ``as_of``; cạnh có ``props.quan_he`` bị bỏ trừ
        khi ``include_self``. Đầu kia là PhienBan → quy về unit của nó (có ``as_of`` → phiên bản
        đó phải hiệu lực). Đầu kia là VanBan/VanBanNgoai → ghi vào kết quả nhưng không mở rộng
        tiếp (trừ khi ``through_documents``). Seed là id PhienBan → quy về unit.
        """
        if not 1 <= hops <= MAX_HOPS:
            raise ValueError(f"hops phải trong [1, {MAX_HOPS}], nhận {hops}")
        if direction not in ("out", "in", "both"):
            raise ValueError(f"direction không hợp lệ: {direction!r}")
        types = sorted(set(edge_types))
        if not types:
            raise ValueError("edge_types rỗng")
        if "CO_PHIEN_BAN" in types:
            raise ValueError("expand không đi qua CO_PHIEN_BAN (phiên bản đã được gộp vào unit)")

        start = sorted({unit_of_version_id(s) for s in seeds})
        dist: dict[str, int] = dict.fromkeys(start, 0)
        edges: dict[str, GraphEdge] = {}
        frontier = start
        for hop in range(1, hops + 1):
            if not frontier:
                break
            vm = self.versions_map(frontier)
            anchors = set(frontier)
            for vs in vm.values():
                for v in vs:
                    if as_of is None or version_in_effect(v, as_of):
                        anchors.add(v.id)
            anchor_ids = sorted(anchors)
            cand: list[tuple[GraphEdge, str]] = []
            if direction in ("out", "both"):
                cand += [(e, e.dst) for e in self._edges(anchor_ids, types, "out")]
            if direction in ("in", "both"):
                cand += [(e, e.src) for e in self._edges(anchor_ids, types, "in")]
            cand = [
                (e, o)
                for e, o in cand
                if edge_in_effect(e, as_of) and (include_self or SELF_REF_PROP not in e.props)
            ]
            others = self.get_nodes(sorted({o for _, o in cand}))
            nxt: set[str] = set()
            for e, o in sorted(cand, key=lambda t: (t[0].sort_key, t[1])):
                n = others.get(o)
                if n is None:
                    continue
                if n.label == VERSION_LABEL:
                    if as_of is not None and not version_in_effect(n, as_of):
                        continue
                    target = str(n.props.get("unit_id") or unit_of_version_id(n.id))
                else:
                    target = n.id
                edges[e.key] = e
                if target not in dist:
                    dist[target] = hop
                    if through_documents or n.label not in DOC_LABELS:
                        nxt.add(target)
            frontier = sorted(nxt)
        return Subgraph(nodes=dict(sorted(dist.items())), edges=sort_edges(edges.values()))


def _types(types: Sequence[str] | None) -> list[str] | None:
    return None if types is None else sorted(set(types))


def _sort_versions(vs: Iterable[GraphNode]) -> list[GraphNode]:
    return sorted(vs, key=lambda n: (int(n.props.get("version", 0)), n.id))


def _chain_order(sib: set[str], nxt: Mapping[str, str]) -> list[str]:
    """Xếp anh em theo KE_TIEP: bắt đầu từ các đầu chuỗi (không có anh em đứng trước), phần
    không nằm trong chuỗi nào (dữ liệu lỗi) xếp cuối theo id."""
    has_prev = {nxt[s] for s in sib if s in nxt and nxt[s] in sib}
    out: list[str] = []
    seen: set[str] = set()
    for head in sorted(s for s in sib if s not in has_prev):
        cur: str | None = head
        while cur is not None and cur in sib and cur not in seen:
            out.append(cur)
            seen.add(cur)
            cur = nxt.get(cur)
    out.extend(sorted(sib - seen))
    return out


# --------------------------------------------------------------------------- nạp


@dataclass
class LoadOutcome:
    action: Literal["skipped", "loaded"]
    data_hash: str
    expected: dict[str, Any]
    actual: dict[str, Any]
    seconds: float

    @property
    def ok(self) -> bool:
        return self.expected == self.actual


def load_graph(
    store: BaseGraphStore,
    graph_dir: str | Path,
    *,
    force: bool = False,
    git_commit: str | None = None,
) -> LoadOutcome:
    """Nạp 3 file JSONL vào ``store`` — idempotent, resume được.

    ``meta().data_hash`` trùng và số đếm khớp → bỏ qua. Ngược lại (đổi dữ liệu, lần nạp trước bị
    ngắt — meta chỉ được ghi **sau cùng**) → ``clear()`` rồi nạp lại toàn bộ.
    """
    t0 = time.monotonic()
    h = data_hash(graph_dir)
    nodes, edges = load_graph_dir(graph_dir)
    expected = count_items(nodes, edges)
    meta = store.meta()
    if not force and meta and meta.get("data_hash") == h:
        actual = store.count()
        if actual == expected:
            return LoadOutcome("skipped", h, expected, actual, time.monotonic() - t0)
        logger.warning("meta khớp nhưng số đếm lệch → nạp lại")
    store.clear()
    store.ensure_schema()
    logger.info("nạp %d nút, %d cạnh", len(nodes), len(edges))
    store.upsert_nodes(nodes)
    store.upsert_edges(edges)
    actual = store.count()
    if actual == expected:
        store.set_meta(
            {
                "data_hash": h,
                "loader_version": LOADER_VERSION,
                "counts": expected,
                "git_commit": git_commit,
                "loaded_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            }
        )
    return LoadOutcome("loaded", h, expected, actual, time.monotonic() - t0)
