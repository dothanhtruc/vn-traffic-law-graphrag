"""So khớp hai GraphStore (``--verify-store``): cùng truy vấn phải cho cùng kết quả.

Gồm: số đếm, toàn bộ nút theo nhãn, toàn bộ cạnh theo loại (round-trip đầy đủ), và mọi API đọc
trên mẫu unit phân tầng theo văn bản (+ mọi VanBan) × các mốc ngày.
"""

from __future__ import annotations

import hashlib
import random
from collections.abc import Callable, Iterator, Sequence
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, is_dataclass
from datetime import date
from typing import Any

from trafficlaw.graph.store import (
    UNIT_LABELS,
    BaseGraphStore,
    GraphEdge,
    GraphNode,
    Subgraph,
    canonical_json,
)

PARITY_DATES: tuple[date, ...] = (
    date(2025, 1, 1),
    date(2026, 1, 1),
    date(2026, 7, 1),
    date(2026, 8, 15),
)
EXPAND_TYPES: tuple[str, ...] = ("DAN_CHIEU", "HUONG_DAN", "SUA_DOI", "BAI_BO")


def canon(x: Any) -> Any:
    """Kết quả API → JSON-able để so sánh."""
    if isinstance(x, GraphNode | GraphEdge | Subgraph):
        return x.to_dict()
    if isinstance(x, date):
        return x.isoformat()
    if isinstance(x, list | tuple):
        return [canon(v) for v in x]
    if isinstance(x, dict):
        return {str(k): canon(v) for k, v in x.items()}
    if is_dataclass(x) and not isinstance(x, type):
        return canon(asdict(x))
    return x


def _sha(x: Any) -> str:
    return hashlib.sha1(canonical_json(canon(x)).encode()).hexdigest()


def sample_units(store: BaseGraphStore, n: int, seed: int = 42) -> list[str]:
    """``n`` unit phân tầng theo văn bản: xáo từng văn bản (seed cố định), lấy vòng tròn."""
    by_doc: dict[str, list[str]] = {}
    for label in UNIT_LABELS:
        for node in store.nodes_by_label(label):
            by_doc.setdefault(str(node.props.get("doc_id")), []).append(node.id)
    rng = random.Random(seed)
    pools = []
    for doc in sorted(by_doc):
        ids = sorted(by_doc[doc])
        rng.shuffle(ids)
        pools.append(ids)
    out: list[str] = []
    i = 0
    while len(out) < n and any(i < len(p) for p in pools):
        for p in pools:
            if i < len(p) and len(out) < n:
                out.append(p[i])
        i += 1
    return sorted(out)


@dataclass(frozen=True)
class Check:
    api: str
    kwargs: dict[str, Any]

    def label(self) -> dict[str, Any]:
        return {"api": self.api, "args": canon(self.kwargs)}


def build_checks(
    units: Sequence[str],
    docs: Sequence[str],
    dates: Sequence[date] = PARITY_DATES,
    *,
    node_labels: Sequence[str],
    edge_types: Sequence[str],
) -> list[Check]:
    cs: list[Check] = [Check("count", {})]
    cs += [Check("nodes_by_label", {"label": lb}) for lb in node_labels]
    cs += [Check("edges_by_type", {"etype": t}) for t in edge_types]
    for u in units:
        cs += [
            Check("get_node", {"node_id": u}),
            Check("parent", {"unit_id": u}),
            Check("ancestors", {"unit_id": u}),
            Check("versions", {"unit_id": u}),
            Check("children", {"unit_id": u}),
            Check("out_edges", {"node_id": u}),
            Check("in_edges", {"node_id": u}),
            Check("amendments_of", {"node_id": u}),
            Check("guidance_for", {"node_id": u}),
        ]
        for d in dates:
            cs += [
                Check("version_at", {"unit_id": u, "as_of": d}),
                Check("version_at", {"unit_id": u, "as_of": d, "include_repealed": True}),
                Check("children", {"unit_id": u, "as_of": d}),
                Check("subtree", {"unit_id": u, "as_of": d}),
                Check("out_edges", {"node_id": u, "as_of": d}),
                Check("in_edges", {"node_id": u, "as_of": d}),
                Check("references_from", {"unit_id": u, "as_of": d}),
                Check("references_to", {"unit_id": u, "as_of": d}),
                Check("references_from", {"unit_id": u, "as_of": d, "include_self": True}),
                Check("amendments_of", {"node_id": u, "as_of": d}),
                Check(
                    "expand",
                    {"seeds": [u], "edge_types": list(EXPAND_TYPES), "as_of": d, "hops": 2},
                ),
            ]
    for doc in docs:
        cs += [
            Check("get_node", {"node_id": doc}),
            Check("children", {"unit_id": doc}),
            Check("versions", {"unit_id": doc}),
            Check("out_edges", {"node_id": doc}),
            Check("in_edges", {"node_id": doc}),
            Check("guidance_for", {"node_id": doc}),
        ]
        for d in dates:
            cs += [
                Check("children", {"unit_id": doc, "as_of": d}),
                Check("version_at", {"unit_id": doc, "as_of": d}),
                Check("out_edges", {"node_id": doc, "as_of": d}),
                Check("in_edges", {"node_id": doc, "as_of": d}),
                Check("amendments_of", {"node_id": doc, "as_of": d}),
                Check("guidance_for", {"node_id": doc, "as_of": d}),
                Check(
                    "expand",
                    {"seeds": [doc], "edge_types": ["HUONG_DAN", "SUA_DOI"], "as_of": d},
                ),
            ]
    return cs


def _call(store: BaseGraphStore, c: Check) -> Any:
    fn: Callable[..., Any] = getattr(store, c.api)
    return fn(**c.kwargs)


def run_parity(
    a: BaseGraphStore,
    b: BaseGraphStore,
    checks: Sequence[Check],
    *,
    workers: int = 8,
) -> Iterator[dict[str, Any]]:
    """Chạy từng check trên cả hai store (store ``b`` song song nhiều luồng); yield bản ghi."""

    def both(c: Check) -> tuple[Any, Any]:
        return _call(a, c), _call(b, c)

    with ThreadPoolExecutor(max_workers=max(1, workers)) as ex:
        for c, (ra, rb) in zip(checks, ex.map(both, checks), strict=True):
            ha, hb = _sha(ra), _sha(rb)
            rec: dict[str, Any] = {"kind": "check", **c.label(), "ok": ha == hb, "sha": ha}
            if ha != hb:
                rec["sha_b"] = hb
                rec["a"] = canonical_json(canon(ra))[:2000]
                rec["b"] = canonical_json(canon(rb))[:2000]
            yield rec


def doc_ids(store: BaseGraphStore) -> list[str]:
    return [n.id for n in store.nodes_by_label("VanBan")]


__all__ = [
    "EXPAND_TYPES",
    "PARITY_DATES",
    "Check",
    "build_checks",
    "canon",
    "doc_ids",
    "run_parity",
    "sample_units",
]
