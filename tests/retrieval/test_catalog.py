"""Danh mục chunk (M10): cắt Phụ lục theo dòng, filter_as_of ở 4 mốc, chunk đúng của gold."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from trafficlaw.graph.embedded import EmbeddedStore
from trafficlaw.graph.store import GraphEdge, GraphNode
from trafficlaw.retrieval.catalog import (
    ChunkCatalog,
    Hit,
    build_catalog,
    filter_as_of,
    is_same_or_related,
    read_catalog,
    split_lines,
    write_catalog,
)

MINI = Path(__file__).resolve().parents[1] / "fixtures/mini_graph"
MILESTONES = [date(2025, 1, 1), date(2026, 1, 1), date(2026, 7, 1), date(2026, 8, 15)]


@pytest.fixture(scope="module")
def mini() -> EmbeddedStore:
    return EmbeddedStore.from_dir(MINI)


# --- Phụ lục ---------------------------------------------------------------------------------


def test_split_lines_limits() -> None:
    lines = ["a" * 10, "b" * 10, "c" * 10, "d" * 40, "e" * 5]
    parts = split_lines(lines, "P" * 5, 30)
    assert [len(p) for p in parts] == [2, 1, 1, 1]
    assert ["\n".join(p) for p in parts][0] == "a" * 10 + "\n" + "b" * 10
    for p in parts:
        size = len("P" * 5 + "\n" + "\n".join(p))
        assert size <= 30 or len(p) == 1  # dòng 40 ký tự đứng riêng
    assert [x for p in parts for x in p] == lines  # không mất / cắt dòng nào
    with pytest.raises(ValueError):
        split_lines(lines, "", 0)


def _pl_store() -> EmbeddedStore:
    s = EmbeddedStore()
    rows = [f"{i} | Tỉnh {i} | {10 + i}" for i in range(1, 41)]
    v0 = "PHỤ LỤC SỐ 02\nKÝ HIỆU BIỂN SỐ\n" + "\n".join(rows)
    v1 = "PHỤ LỤC SỐ 02\nKÝ HIỆU BIỂN SỐ\n" + "\n".join(rows[:5])
    s.upsert_nodes(
        [
            GraphNode("TT1", "VanBan", {"doc_id": "TT1", "indexable": True, "tier": "B"}),
            GraphNode("TT2", "VanBan", {"doc_id": "TT2", "indexable": False, "tier": "B"}),
            GraphNode("TT1/PL2", "PhuLuc", {"doc_id": "TT1", "number": "2", "title": "KÝ HIỆU"}),
            GraphNode("TT2/PL1", "PhuLuc", {"doc_id": "TT2", "number": "1", "title": "X"}),
            GraphNode(
                "TT1/PL2@v0",
                "PhienBan",
                {"unit_id": "TT1/PL2", "version": 0, "text": v0, "status": "amended",
                 "effective_from": "2025-01-01", "effective_to": "2026-06-30"},
            ),
            GraphNode(
                "TT1/PL2@v1",
                "PhienBan",
                {"unit_id": "TT1/PL2", "version": 1, "text": v1, "status": "active",
                 "effective_from": "2026-07-01", "effective_to": None},
            ),
            GraphNode(
                "TT2/PL1@v0",
                "PhienBan",
                {"unit_id": "TT2/PL1", "version": 0, "text": "y", "status": "active",
                 "effective_from": "2025-01-01", "effective_to": None},
            ),
        ]
    )  # fmt: skip
    s.upsert_edges(
        [
            GraphEdge.make("THUOC", "TT1/PL2", "TT1"),
            GraphEdge.make("THUOC", "TT2/PL1", "TT2"),
            GraphEdge.make("CO_PHIEN_BAN", "TT1/PL2", "TT1/PL2@v0"),
            GraphEdge.make("CO_PHIEN_BAN", "TT1/PL2", "TT1/PL2@v1"),
            GraphEdge.make("CO_PHIEN_BAN", "TT2/PL1", "TT2/PL1@v0"),
        ]
    )
    return s


def test_phu_luc_chunks_by_line() -> None:
    s = _pl_store()
    cat = build_catalog(s, phu_luc_max_chars=200)
    pl = [c for c in cat if c.kind == "phu_luc"]
    assert all(c.doc_id == "TT1" for c in pl)  # văn bản không indexable bị bỏ
    v0 = [c for c in pl if c.effective_from == date(2025, 1, 1)]
    v1 = [c for c in pl if c.effective_from == date(2026, 7, 1)]
    assert len(v0) > 2 and len(v1) == 1
    assert [c.chunk_id for c in v0] == [f"TT1/PL2#2025-01-01#p{k}" for k in range(1, len(v0) + 1)]
    assert v1[0].chunk_id == "TT1/PL2#2026-07-01#p1"
    full = s.versions("TT1/PL2")[0].props["text"].split("\n")
    body: list[str] = []
    for c in v0:
        assert len(c.text) <= 200
        head, *lines = c.text.split("\n")
        assert head == "Phụ lục 2. KÝ HIỆU" == c.title
        assert all(x in full for x in lines)  # không cắt giữa dòng
        body.extend(lines)
        assert c.effective_to == date(2026, 6, 30)
        assert c.version_ids == ("TT1/PL2@v0",)
        assert c.part is not None and c.dieu_id is None and c.tier == "B"
    assert body == full
    # tất định
    assert build_catalog(s, phu_luc_max_chars=200) == cat


# --- Khoản + filter_as_of trên mini_graph ----------------------------------------------------


def test_catalog_mini_reuses_m9_chunks(mini, tmp_path) -> None:
    cat = build_catalog(mini, phu_luc_max_chars=1500)
    k3 = [c for c in cat if c.unit_id == "ND168-2024/D6/K3"]
    assert [c.chunk_id for c in k3] == [
        "ND168-2024/D6/K3#2025-01-01",
        "ND168-2024/D6/K3#2026-01-01",
        "ND168-2024/D6/K3#2026-08-15",
    ]
    assert all(c.kind == "khoan" and c.dieu_id == "ND168-2024/D6" for c in k3)
    assert k3[0].title.startswith("Điều 6.")
    p = tmp_path / "chunks.jsonl"
    write_catalog(p, cat)
    assert read_catalog(p) == cat


@pytest.mark.parametrize(
    ("as_of", "expected", "has_m", "m_text_v1"),
    [
        (MILESTONES[0], "ND168-2024/D6/K3#2025-01-01", False, False),
        (MILESTONES[1], "ND168-2024/D6/K3#2026-01-01", True, False),
        (MILESTONES[2], "ND168-2024/D6/K3#2026-01-01", True, False),
        (MILESTONES[3], "ND168-2024/D6/K3#2026-08-15", True, True),
    ],
)
def test_filter_as_of_nd168_d6_k3_m(mini, as_of, expected, has_m, m_text_v1) -> None:
    """ND168 Đ6 K3 m: hiệu lực riêng từ 01/01/2026 (Đ53 K2), sửa bởi ND238 từ 15/08/2026."""
    cat = ChunkCatalog(build_catalog(mini, phu_luc_max_chars=1500))
    states = [c.chunk_id for c in cat.chunks if c.unit_id == "ND168-2024/D6/K3"]
    hits = [Hit(cid, 1.0 / i, i, "test") for i, cid in enumerate(reversed(states), 1)]
    hits.insert(0, Hit("KHONG-CO#2025-01-01", 9.0, 0, "test"))
    got = filter_as_of(hits, as_of, cat)
    assert [h.chunk_id for h in got] == [expected]
    assert got[0].rank == 1
    text = cat.get(expected).text
    assert ("\nm) Chở trẻ em" in text) is has_m
    assert ("(trừ xe ô tô chỉ có một hàng ghế);" in text) is m_text_v1
    assert ("không sử dụng thiết bị an toàn phù hợp cho trẻ em" in text) is (
        has_m and not m_text_v1
    )
    # chunk đúng của gold Điểm m tại as_of
    rel = cat.relevant(["ND168-2024/D6/K3/m"], as_of)
    assert rel == {"ND168-2024/D6/K3/m": {expected}}


def test_relevant_parent_and_children(mini) -> None:
    cat = ChunkCatalog(build_catalog(mini, phu_luc_max_chars=1500))
    d = date(2026, 11, 3)
    rel = cat.relevant(["ND168-2024/D6"], d)["ND168-2024/D6"]
    assert rel and all(cat.get(c).unit_id.startswith("ND168-2024/D6/K") for c in rel)
    assert all(cat.get(c).covers(d) for c in rel)
    assert cat.relevant(["ND168-2024/D60"], d) == {"ND168-2024/D60": set()}


def test_is_same_or_related() -> None:
    assert is_same_or_related("A/D6/K3", "A/D6/K3/m")
    assert is_same_or_related("A/D6/K3", "A/D6")
    assert is_same_or_related("A/D6/K3", "A/D6/K3")
    assert not is_same_or_related("A/D6/K3", "A/D6/K30")
    assert not is_same_or_related("A/D6/K3", "A/D6/K4/a")
