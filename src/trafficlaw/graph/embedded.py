"""EmbeddedStore: GraphStore trong bộ nhớ trên ``networkx.MultiDiGraph`` (test, demo không Neo4j).

Khoá cạnh của MultiDiGraph = :func:`trafficlaw.graph.store.edge_key` ⇒ cạnh song song cùng
(type, src, dst) nhưng khác props được giữ riêng; ghi lại cùng cạnh là idempotent.
"""

from __future__ import annotations

import copy
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, Literal

import networkx as nx

from trafficlaw.graph.store import (
    GRAPH_FILES,
    BaseGraphStore,
    GraphEdge,
    GraphNode,
    count_items,
    data_hash,
    load_graph,
    sort_edges,
)
from trafficlaw.utils.jsonl import read_jsonl


class EmbeddedStore(BaseGraphStore):
    def __init__(self) -> None:
        self.g: nx.MultiDiGraph = nx.MultiDiGraph()
        self._by_label: dict[str, set[str]] = {}
        self._meta: dict[str, Any] | None = None

    @classmethod
    def from_dir(cls, graph_dir: str | Path) -> EmbeddedStore:
        """Dựng store từ ``data/graph`` (hoặc thư mục fixture cùng dạng)."""
        s = cls()
        out = load_graph(s, graph_dir)
        if not out.ok:  # pragma: no cover - chỉ xảy ra khi có cạnh trùng khoá
            raise ValueError(f"Số đếm lệch sau khi nạp {graph_dir}: {out.actual} ≠ {out.expected}")
        assert out.data_hash == data_hash(graph_dir)
        return s

    @classmethod
    def from_dir_base(cls, graph_dir: str | Path) -> EmbeddedStore:
        """Chỉ 3 file M5 (bỏ file ngữ nghĩa M8 nếu đã publish) — đầu vào của trích xuất."""
        d = Path(graph_dir)
        s = cls()
        s.upsert_nodes([GraphNode.from_dict(r) for r in read_jsonl(d / GRAPH_FILES[0])])
        s.upsert_edges([GraphEdge.from_dict(r) for n in GRAPH_FILES[1:] for r in read_jsonl(d / n)])
        return s

    # ---- nguyên thuỷ -------------------------------------------------------------------
    def get_nodes(self, ids: Sequence[str]) -> dict[str, GraphNode]:
        out: dict[str, GraphNode] = {}
        for i in ids:
            if i in self.g:
                d = self.g.nodes[i]
                out[i] = GraphNode(i, d["label"], d["props"])
        return out

    def _edges(
        self, ids: Sequence[str], types: Sequence[str] | None, direction: Literal["out", "in"]
    ) -> list[GraphEdge]:
        tset = None if types is None else set(types)
        out: list[GraphEdge] = []
        for i in dict.fromkeys(ids):
            if i not in self.g:
                continue
            it = (
                self.g.out_edges(i, keys=True, data=True)
                if direction == "out"
                else self.g.in_edges(i, keys=True, data=True)
            )
            for s, d, k, data in it:
                if tset is None or data["type"] in tset:
                    out.append(GraphEdge(data["type"], s, d, data["props"], k))
        return out

    def nodes_by_label(self, label: str, *, doc_id: str | None = None) -> list[GraphNode]:
        ids = sorted(self._by_label.get(label, ()))
        nodes = self.get_nodes(ids)
        return [nodes[i] for i in ids if doc_id is None or nodes[i].props.get("doc_id") == doc_id]

    def edges_by_type(self, etype: str) -> list[GraphEdge]:
        return sort_edges(
            GraphEdge(d["type"], s, t, d["props"], k)
            for s, t, k, d in self.g.edges(keys=True, data=True)
            if d["type"] == etype
        )

    def count(self) -> dict[str, Any]:
        nodes = (GraphNode(i, d["label"]) for i, d in self.g.nodes(data=True))
        edges = (
            GraphEdge(d["type"], s, t, {}, k) for s, t, k, d in self.g.edges(keys=True, data=True)
        )
        return count_items(nodes, edges)

    def upsert_nodes(self, nodes: Sequence[GraphNode]) -> None:
        for n in nodes:
            if n.id in self.g:
                old = self.g.nodes[n.id]["label"]
                self._by_label.get(old, set()).discard(n.id)
            self.g.add_node(n.id, label=n.label, props=copy.deepcopy(n.props))
            self._by_label.setdefault(n.label, set()).add(n.id)

    def upsert_edges(self, edges: Sequence[GraphEdge]) -> None:
        missing = sorted({x for e in edges for x in (e.src, e.dst) if x not in self.g})
        if missing:
            raise KeyError(f"Cạnh trỏ tới nút chưa có: {missing[:5]} (tổng {len(missing)})")
        for e in edges:
            self.g.add_edge(e.src, e.dst, key=e.key, type=e.type, props=copy.deepcopy(e.props))

    def clear(self) -> None:
        self.g.clear()
        self._by_label.clear()
        self._meta = None

    def meta(self) -> dict[str, Any] | None:
        return None if self._meta is None else dict(self._meta)

    def set_meta(self, meta: Mapping[str, Any]) -> None:
        self._meta = dict(meta)
