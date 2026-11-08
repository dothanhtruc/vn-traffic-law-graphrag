"""M5 trên dữ liệu thật ``data/graph`` (skip nếu chưa chạy ``scripts.build_graph``)."""

from __future__ import annotations

from pathlib import Path

import pytest

from trafficlaw.graph.schema import MAX_EDGES, MAX_NODES
from trafficlaw.utils.jsonl import read_jsonl

REPO_ROOT = Path(__file__).resolve().parents[2]
GRAPH = REPO_ROOT / "data/graph"

pytestmark = pytest.mark.skipif(
    not (GRAPH / "edges_legal.jsonl").is_file(), reason="chưa có data/graph/edges_legal.jsonl"
)


@pytest.fixture(scope="module")
def legal() -> list[dict]:  # type: ignore[type-arg]
    return list(read_jsonl(GRAPH / "edges_legal.jsonl"))


def _has(edges: list[dict], etype: str, src: str, dst: str, **props: object) -> bool:  # type: ignore[type-arg]
    return any(
        e["type"] == etype
        and e["src"] == src
        and e["dst"] == dst
        and all(e["props"].get(k) == v for k, v in props.items())
        for e in edges
    )


def test_huong_dan_nd165(legal: list[dict]) -> None:  # type: ignore[type-arg]
    assert _has(legal, "HUONG_DAN", "ND165-2024", "LUAT35-2024", cap="van_ban")
    assert _has(legal, "HUONG_DAN", "ND165-2024", "LUAT36-2024/D77", cap="unit")


def test_sua_doi_nd238_dieu6_k3_m(legal: list[dict]) -> None:  # type: ignore[type-arg]
    assert _has(legal, "SUA_DOI", "ND238-2026", "ND168-2024/D6/K3/m", effective_from="2026-08-15")


def test_khong_canh_treo_va_trong_gioi_han(legal: list[dict]) -> None:  # type: ignore[type-arg]
    ids = {n["id"] for n in read_jsonl(GRAPH / "nodes.jsonl")}
    struct = list(read_jsonl(GRAPH / "edges_struct.jsonl"))
    assert len(ids) <= MAX_NODES
    assert len(struct) + len(legal) <= MAX_EDGES
    assert all(e["src"] in ids and e["dst"] in ids for e in [*struct, *legal])


def test_dan_chieu_to_tien(legal: list[dict]) -> None:  # type: ignore[type-arg]
    assert _has(legal, "DAN_CHIEU", "LUAT36-2024/D51/K6@v0", "LUAT36-2024/D51", quan_he="to_tien")


def test_khong_co_van_ban_khong_dung(legal: list[dict]) -> None:  # type: ignore[type-arg]
    bad = ("100/2019", "23/2008", "26/2001", "LUAT-GIAO-THONG-DUONG-BO")
    nodes = [n["id"] for n in read_jsonl(GRAPH / "nodes.jsonl")]
    assert not any(b in x for b in bad for x in nodes)
    assert not any(b in e["dst"] for b in bad for e in legal)
