"""Neo4jStore: GraphStore trên Neo4j (AuraDB Free).

Cách lưu:

- Nút: nhãn chung ``:<prefix>Node`` + nhãn riêng ``:<prefix><label>``; ràng buộc unique
  ``Node.id``. Thuộc tính: ``id``, ``label``, ``props_json`` (nguồn sự thật, đọc lại y hệt
  EmbeddedStore) + các thuộc tính phẳng của ``props`` (scalar / list scalar cùng kiểu, khác
  ``null``) để lọc/duyệt trong Neo4j Browser.
- Cạnh: loại = ``type`` (không prefix — mọi truy vấn neo vào nút ``:<prefix>Node``), thuộc tính
  ``key`` (phân biệt cạnh song song), ``props_json`` + thuộc tính phẳng.
- ``:<prefix>_Meta`` (một nút) giữ ``data_hash`` của lần nạp thành công gần nhất.

``label_prefix`` (vd. ``"T_"``) tách không gian tên cho test trên cùng database Aura Free (chỉ có
một database) mà không đụng tới dữ liệu thật. Kết nối đọc từ ``NEO4J_URI``, ``NEO4J_USERNAME``,
``NEO4J_PASSWORD`` (+ ``NEO4J_DATABASE``); mật khẩu không bao giờ được log.
"""

from __future__ import annotations

import json
import logging
import os
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any, Literal

from trafficlaw.graph.store import (
    BaseGraphStore,
    GraphEdge,
    GraphNode,
    _sort_versions,
    canonical_json,
    sort_edges,
)

logger = logging.getLogger(__name__)

_NAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")
_PREFIX_RE = re.compile(r"^[A-Za-z0-9_]*$")
_RESERVED = frozenset({"id", "label", "key", "props_json"})
ENV_VARS = ("NEO4J_URI", "NEO4J_USERNAME", "NEO4J_PASSWORD")


@dataclass(frozen=True)
class Neo4jConfig:
    uri: str
    username: str
    password: str = field(repr=False)
    database: str | None = None

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> Neo4jConfig | None:
        """Đọc từ biến môi trường; thiếu biến bắt buộc → ``None``."""
        e = os.environ if env is None else env
        if not all(e.get(k) for k in ENV_VARS):
            return None
        return cls(
            uri=e["NEO4J_URI"],
            username=e["NEO4J_USERNAME"],
            password=e["NEO4J_PASSWORD"],
            database=e.get("NEO4J_DATABASE") or None,
        )


def _scalar_type(v: Any) -> type | None:
    if isinstance(v, bool):
        return bool
    if isinstance(v, int | float | str):
        return type(v)
    return None


def flat_props(props: Mapping[str, Any]) -> dict[str, Any]:
    """Thuộc tính lưu được trực tiếp trong Neo4j (bỏ ``null``, dict, list lẫn kiểu/rỗng)."""
    out: dict[str, Any] = {}
    for k, v in props.items():
        if k in _RESERVED or not _NAME_RE.match(k):
            continue
        if _scalar_type(v) is not None:
            out[k] = v
        elif isinstance(v, list) and v:
            ts = {_scalar_type(x) for x in v}
            if len(ts) == 1 and None not in ts:
                out[k] = list(v)
    return out


def _name(s: str) -> str:
    if not _NAME_RE.match(s):
        raise ValueError(f"Tên nhãn/loại cạnh không hợp lệ: {s!r}")
    return s


def _chunks(seq: Sequence[Any], n: int) -> list[Sequence[Any]]:
    return [seq[i : i + n] for i in range(0, len(seq), n)]


class Neo4jStore(BaseGraphStore):
    def __init__(
        self,
        config: Neo4jConfig,
        *,
        label_prefix: str = "",
        batch_size: int = 1000,
        delete_batch_size: int = 5000,
        driver: Any = None,
    ) -> None:
        if not _PREFIX_RE.match(label_prefix):
            raise ValueError(f"label_prefix không hợp lệ: {label_prefix!r}")
        self.config = config
        self.database = config.database
        self.prefix = label_prefix
        self.batch_size = batch_size
        self.delete_batch_size = delete_batch_size
        self._node = f"{label_prefix}Node"
        self._meta_label = f"{label_prefix}_Meta"
        if driver is None:
            from neo4j import GraphDatabase

            driver = GraphDatabase.driver(config.uri, auth=(config.username, config.password))
        self._driver = driver

    @classmethod
    def from_env(cls, **kwargs: Any) -> Neo4jStore | None:
        cfg = Neo4jConfig.from_env()
        return None if cfg is None else cls(cfg, **kwargs)

    # ---- tiện ích ----------------------------------------------------------------------
    def _run(self, query: str, params: Mapping[str, Any] | None = None, *, write: bool = False):  # type: ignore[no-untyped-def]
        from neo4j import RoutingControl

        res = self._driver.execute_query(
            query,
            dict(params or {}),
            database_=self.database,
            routing_=RoutingControl.WRITE if write else RoutingControl.READ,
        )
        return res.records

    def _label(self, label: str) -> str:
        return f"{self.prefix}{_name(label)}"

    def verify_connectivity(self) -> None:
        self._driver.verify_connectivity()

    def close(self) -> None:
        self._driver.close()

    def ensure_schema(self) -> None:
        name = f"{self.prefix.lower()}node_id_unique"
        self._run(
            f"CREATE CONSTRAINT `{name}` IF NOT EXISTS "
            f"FOR (n:`{self._node}`) REQUIRE n.id IS UNIQUE",
            write=True,
        )

    # ---- nguyên thuỷ đọc ---------------------------------------------------------------
    def get_nodes(self, ids: Sequence[str]) -> dict[str, GraphNode]:
        out: dict[str, GraphNode] = {}
        q = (
            f"UNWIND $ids AS i MATCH (n:`{self._node}` {{id: i}}) "
            "RETURN n.id AS id, n.label AS label, n.props_json AS pj"
        )
        for chunk in _chunks(list(dict.fromkeys(ids)), self.batch_size):
            for r in self._run(q, {"ids": list(chunk)}):
                out[r["id"]] = GraphNode(r["id"], r["label"], json.loads(r["pj"]))
        return out

    def _edges(
        self, ids: Sequence[str], types: Sequence[str] | None, direction: Literal["out", "in"]
    ) -> list[GraphEdge]:
        if types is not None:
            types = [_name(t) for t in types]
        n = self._node
        pat = (
            f"(a:`{n}` {{id: i}})-[e]->(b:`{n}`)"
            if direction == "out"
            else f"(b:`{n}`)-[e]->(a:`{n}` {{id: i}})"
        )
        q = (
            f"UNWIND $ids AS i MATCH {pat} WHERE $types IS NULL OR type(e) IN $types "
            "RETURN type(e) AS t, startNode(e).id AS s, endNode(e).id AS d, "
            "e.key AS k, e.props_json AS pj"
        )
        out: list[GraphEdge] = []
        for chunk in _chunks(list(dict.fromkeys(ids)), self.batch_size):
            for r in self._run(q, {"ids": list(chunk), "types": types}):
                out.append(GraphEdge(r["t"], r["s"], r["d"], json.loads(r["pj"]), r["k"]))
        return out

    def versions_map(self, unit_ids: Sequence[str]) -> dict[str, list[GraphNode]]:
        n = self._node
        q = (
            f"UNWIND $ids AS i MATCH (:`{n}` {{id: i}})-[:CO_PHIEN_BAN]->(v:`{n}`) "
            "RETURN i AS u, v.id AS id, v.label AS label, v.props_json AS pj"
        )
        out: dict[str, list[GraphNode]] = {u: [] for u in unit_ids}
        for chunk in _chunks(list(dict.fromkeys(unit_ids)), self.batch_size):
            for r in self._run(q, {"ids": list(chunk)}):
                out[r["u"]].append(GraphNode(r["id"], r["label"], json.loads(r["pj"])))
        return {u: _sort_versions(vs) for u, vs in out.items()}

    def nodes_by_label(self, label: str, *, doc_id: str | None = None) -> list[GraphNode]:
        q = (
            f"MATCH (n:`{self._node}`:`{self._label(label)}`) "
            "WHERE $doc IS NULL OR n.doc_id = $doc "
            "RETURN n.id AS id, n.label AS label, n.props_json AS pj ORDER BY id"
        )
        nodes = [
            GraphNode(r["id"], r["label"], json.loads(r["pj"]))
            for r in self._run(q, {"doc": doc_id})
        ]
        # ORDER BY của Cypher có thể khác Python với chuỗi Unicode → sắp lại cho tất định.
        return sorted(nodes, key=lambda x: x.id)

    def edges_by_type(self, etype: str) -> list[GraphEdge]:
        n = self._node
        q = (
            f"MATCH (a:`{n}`)-[e:`{_name(etype)}`]->(b:`{n}`) "
            "RETURN a.id AS s, b.id AS d, e.key AS k, e.props_json AS pj"
        )
        return sort_edges(
            GraphEdge(etype, r["s"], r["d"], json.loads(r["pj"]), r["k"]) for r in self._run(q)
        )

    def count(self) -> dict[str, Any]:
        n = self._node
        nc = {
            r["l"]: r["c"] for r in self._run(f"MATCH (x:`{n}`) RETURN x.label AS l, count(*) AS c")
        }
        ec = {
            r["t"]: r["c"]
            for r in self._run(f"MATCH (:`{n}`)-[e]->(:`{n}`) RETURN type(e) AS t, count(*) AS c")
        }
        return {"nodes": dict(sorted(nc.items())), "edges": dict(sorted(ec.items()))}

    # ---- ghi ---------------------------------------------------------------------------
    def upsert_nodes(self, nodes: Sequence[GraphNode]) -> None:
        by_label: dict[str, list[dict[str, Any]]] = {}
        for x in nodes:
            props = flat_props(x.props)
            props.update(id=x.id, label=x.label, props_json=canonical_json(x.props))
            by_label.setdefault(x.label, []).append({"id": x.id, "props": props})
        for label in sorted(by_label):
            q = (
                f"UNWIND $rows AS r MERGE (n:`{self._node}` {{id: r.id}}) "
                f"SET n = r.props SET n:`{self._label(label)}`"
            )
            for chunk in _chunks(by_label[label], self.batch_size):
                self._run(q, {"rows": list(chunk)}, write=True)
            logger.info("nút %s: %d", label, len(by_label[label]))

    def upsert_edges(self, edges: Sequence[GraphEdge]) -> None:
        by_type: dict[str, list[dict[str, Any]]] = {}
        for e in edges:
            props = flat_props(e.props)
            props.update(key=e.key, props_json=canonical_json(e.props))
            by_type.setdefault(e.type, []).append(
                {"src": e.src, "dst": e.dst, "key": e.key, "props": props}
            )
        n = self._node
        for etype in sorted(by_type):
            q = (
                f"UNWIND $rows AS r MATCH (a:`{n}` {{id: r.src}}) MATCH (b:`{n}` {{id: r.dst}}) "
                f"MERGE (a)-[e:`{_name(etype)}` {{key: r.key}}]->(b) SET e = r.props "
                "RETURN count(e) AS c"
            )
            for chunk in _chunks(by_type[etype], self.batch_size):
                c = self._run(q, {"rows": list(chunk)}, write=True)[0]["c"]
                if c != len(chunk):
                    raise KeyError(
                        f"{etype}: {len(chunk) - c} cạnh trỏ tới nút chưa có (lô {len(chunk)})"
                    )
            logger.info("cạnh %s: %d", etype, len(by_type[etype]))

    def clear(self) -> None:
        """Xoá theo lô (cạnh trước, rồi nút, rồi meta) để giao dịch nhỏ."""
        n = self._node
        lim = {"lim": self.delete_batch_size}
        while True:
            c = self._run(
                f"MATCH (:`{n}`)-[e]->() WITH e LIMIT $lim DELETE e RETURN count(e) AS c",
                lim,
                write=True,
            )[0]["c"]
            if c == 0:
                break
        while True:
            c = self._run(
                f"MATCH (x:`{n}`) WITH x LIMIT $lim DETACH DELETE x RETURN count(x) AS c",
                lim,
                write=True,
            )[0]["c"]
            if c == 0:
                break
        self._run(f"MATCH (m:`{self._meta_label}`) DETACH DELETE m", write=True)

    def meta(self) -> dict[str, Any] | None:
        rs = self._run(f"MATCH (m:`{self._meta_label}`) RETURN m.data_json AS j LIMIT 1")
        return json.loads(rs[0]["j"]) if rs else None

    def set_meta(self, meta: Mapping[str, Any]) -> None:
        self._run(
            f"MERGE (m:`{self._meta_label}` {{singleton: true}}) "
            "SET m.data_json = $j, m.data_hash = $h",
            {"j": canonical_json(dict(meta)), "h": meta.get("data_hash")},
            write=True,
        )
