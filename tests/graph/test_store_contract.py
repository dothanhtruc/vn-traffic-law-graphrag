"""Hợp đồng GraphStore (M6) trên fixture nhỏ dựng từ dữ liệu thật.

Chạy cho EmbeddedStore; với Neo4jStore khi ``-m slow`` và có biến môi trường NEO4J_*.
"""

from __future__ import annotations

from datetime import date

import pytest

from trafficlaw.graph.embedded import EmbeddedStore
from trafficlaw.graph.parity import build_checks, doc_ids, run_parity, sample_units
from trafficlaw.graph.store import BaseGraphStore, GraphStore

M = "ND168-2024/D6/K3/m"
D6 = "ND168-2024/D6"
K10B = "ND168-2024/D6/K10/b"


def test_protocol(store: BaseGraphStore) -> None:
    assert isinstance(store, GraphStore)


def test_count(store: BaseGraphStore) -> None:
    c = store.count()
    assert c["nodes"]["PhienBan"] == 128
    assert c["edges"]["DAN_CHIEU"] == 153
    assert sum(c["nodes"].values()) == 262
    assert sum(c["edges"].values()) == 502


def test_get_node_roundtrip(store: BaseGraphStore) -> None:
    n = store.get_node("LUAT36-2024/D35/K2")
    assert n is not None and n.label == "Khoan"
    # list các dict + null giữ nguyên sau round-trip
    assert n.props["uy_quyen"] == [{"co_quan": "Chính phủ", "source_unit_id": "LUAT36-2024/D35/K5"}]
    assert n.props["title"] is None
    assert store.get_node("KHONG-CO") is None


def test_nodes_by_label(store: BaseGraphStore) -> None:
    docs = store.nodes_by_label("VanBan")
    assert [d.id for d in docs] == sorted(d.id for d in docs)
    assert "ND168-2024" in {d.id for d in docs}
    dieu = [n.id for n in store.nodes_by_label("Dieu", doc_id="LUAT36-2024")]
    assert dieu == ["LUAT36-2024/D35", "LUAT36-2024/D6", "LUAT36-2024/D7", "LUAT36-2024/D77"]


@pytest.mark.parametrize(
    ("as_of", "expected"),
    [
        (date(2025, 12, 31), None),  # điểm m có hiệu lực riêng từ 01/01/2026 (ND168 Đ53 K2)
        (date(2026, 1, 1), f"{M}@v0"),
        (date(2026, 8, 14), f"{M}@v0"),
        (date(2026, 8, 15), f"{M}@v1"),  # ND238 sửa từ 15/08/2026
    ],
)
def test_version_at(store: BaseGraphStore, as_of: date, expected: str | None) -> None:
    v = store.version_at(M, as_of)
    assert (v.id if v else None) == expected


def test_versions_sorted(store: BaseGraphStore) -> None:
    vs = store.versions(M)
    assert [v.props["version"] for v in vs] == [0, 1]
    assert vs[0].props["effective_to"] == "2026-08-14"
    assert vs[1].props["source_unit_id"] == "ND238-2026/D2/K2"


def test_structure(store: BaseGraphStore) -> None:
    assert store.parent(M) == "ND168-2024/D6/K3"
    assert store.parent("ND168-2024") is None
    assert store.ancestors(M) == [
        "ND168-2024/D6/K3",
        D6,
        "ND168-2024/C2/M1",
        "ND168-2024/C2",
        "ND168-2024",
    ]
    kids = store.children("ND168-2024/D6/K3")
    assert kids[:5] == [f"ND168-2024/D6/K3/{x}" for x in ("a", "b", "c", "d", "đ")]
    assert kids[-1] == "ND168-2024/D6/K3/p" and len(kids) == 15


def test_children_added_unit_by_date(store: BaseGraphStore) -> None:
    # K1a bổ sung "vào trước khoản 1" (ND238 Đ2 K1), hiệu lực 15/08/2026.
    assert store.children(D6)[:3] == [f"{D6}/K1a", f"{D6}/K1", f"{D6}/K2"]
    assert f"{D6}/K1a" not in store.children(D6, as_of=date(2026, 8, 14))
    assert store.children(D6, as_of=date(2026, 8, 15))[0] == f"{D6}/K1a"
    # Điểm m chưa có hiệu lực trước 01/01/2026
    assert M not in store.children("ND168-2024/D6/K3", as_of=date(2025, 6, 1))


def test_subtree(store: BaseGraphStore) -> None:
    st = store.subtree("ND168-2024/D6/K3")
    assert st[0] == "ND168-2024/D6/K3" and len(st) == 16
    full = store.subtree(D6)
    assert full.index(f"{D6}/K1a") < full.index(f"{D6}/K1") < full.index(f"{D6}/K1/a")
    assert f"{D6}/K1a" not in store.subtree(D6, as_of=date(2026, 1, 1))


def test_amendments_by_date(store: BaseGraphStore) -> None:
    es = store.amendments_of(M)
    assert [(e.type, e.src, e.props["thao_tac"]) for e in es] == [
        ("SUA_DOI", "ND238-2026", "sua_doi")
    ]
    assert store.amendments_of(M, as_of=date(2026, 8, 14)) == []
    assert len(store.amendments_of(M, as_of=date(2026, 8, 15))) == 1


def test_parallel_edges_kept(store: BaseGraphStore) -> None:
    es = store.out_edges("ND218-2026", types=["SUA_DOI"])
    assert {e.props["cap"] for e in es} == {"van_ban", "unit"}
    assert all(e.dst == "ND158-2024" for e in es) and len({e.key for e in es}) == 2


def test_guidance(store: BaseGraphStore) -> None:
    doc = store.guidance_for("LUAT36-2024", as_of=date(2025, 1, 1))
    assert [(e.src, e.props["cap"]) for e in doc] == [
        ("ND151-2024", "van_ban"),
        ("ND165-2024", "van_ban"),
    ]
    unit = store.guidance_for("LUAT36-2024/D77")
    assert [(e.src, e.props["cap"]) for e in unit] == [("ND165-2024", "unit")]
    assert store.guidance_for("LUAT36-2024", as_of=date(2024, 12, 31)) == []


def test_hop_nhat_without_date(store: BaseGraphStore) -> None:
    # effective_from = null → không bao giờ hiệu lực khi có as_of; as_of = None → vẫn thấy.
    assert len(store.out_edges("VBHN144-2026-LQ-VPQH")) == 1
    assert store.out_edges("VBHN144-2026-LQ-VPQH", as_of=date(2026, 8, 1)) == []


def test_struct_edges_not_filtered(store: BaseGraphStore) -> None:
    assert store.out_edges(M, types=["THUOC"], as_of=date(2020, 1, 1)) != []


def test_references_from_self(store: BaseGraphStore) -> None:
    d = date(2026, 1, 1)
    with_self = store.references_from(K10B, d, include_self=True)
    plain = store.references_from(K10B, d)
    assert [e.dst for e in with_self if "quan_he" in e.props] == [D6]
    assert len(with_self) == len(plain) + 1
    assert all(e.src == f"{K10B}@v0" for e in plain)
    # Trước khi điểm m có hiệu lực, không có phiên bản → không có dẫn chiếu.
    assert store.references_from(M, date(2025, 6, 1)) == []


def test_references_to(store: BaseGraphStore) -> None:
    src = [e.src for e in store.references_to("ND168-2024/D6/K11/b", date(2026, 1, 1))]
    assert src == ["ND168-2024/D12/K10@v0", "ND168-2024/D6/K15/c@v0"]


def test_expand(store: BaseGraphStore) -> None:
    sg = store.expand(
        ["ND168-2024/D12/K10"], edge_types=["DAN_CHIEU"], as_of=date(2026, 1, 1), hops=2
    )
    assert sg.nodes == {
        "ND168-2024/D12/K10": 0,
        "ND168-2024/D6/K11/b": 1,
        "ND168-2024/D6/K11/d": 1,
        "ND168-2024/D6/K15/c": 2,
    }
    assert len(sg.edges) == 4
    one = store.expand(["ND168-2024/D12/K10@v0"], edge_types=["DAN_CHIEU"], hops=1)
    assert set(one.nodes) == {"ND168-2024/D12/K10", "ND168-2024/D6/K11/b", "ND168-2024/D6/K11/d"}


def test_expand_self_and_documents(store: BaseGraphStore) -> None:
    d = date(2026, 1, 1)
    out = store.expand([K10B], edge_types=["DAN_CHIEU"], as_of=d, direction="out")
    assert D6 not in out.nodes
    out_self = store.expand(
        [K10B], edge_types=["DAN_CHIEU"], as_of=d, direction="out", include_self=True
    )
    assert out_self.nodes[D6] == 1
    # Văn bản được ghi nhận nhưng không mở rộng tiếp.
    g = store.expand(["LUAT36-2024/D77"], edge_types=["HUONG_DAN"], hops=2, as_of=d)
    assert g.nodes == {"LUAT36-2024/D77": 0, "ND165-2024": 1}
    g2 = store.expand(
        ["LUAT36-2024/D77"], edge_types=["HUONG_DAN"], hops=2, as_of=d, through_documents=True
    )
    assert g2.nodes["LUAT35-2024"] == 2 and g2.nodes["LUAT36-2024"] == 2


def test_expand_respects_date(store: BaseGraphStore) -> None:
    g = store.expand([M], edge_types=["SUA_DOI"], as_of=date(2026, 8, 14))
    assert g.nodes == {M: 0}
    g = store.expand([M], edge_types=["SUA_DOI"], as_of=date(2026, 8, 15))
    assert g.nodes == {M: 0, "ND238-2026": 1}


def test_expand_validation(store: BaseGraphStore) -> None:
    with pytest.raises(ValueError):
        store.expand([M], edge_types=["DAN_CHIEU"], hops=3)
    with pytest.raises(ValueError):
        store.expand([M], edge_types=["CO_PHIEN_BAN"])
    with pytest.raises(ValueError):
        store.expand([M], edge_types=[])


def test_parity_with_embedded(store: BaseGraphStore, embedded_mini: EmbeddedStore) -> None:
    units = sample_units(embedded_mini, 40, seed=42)
    c = embedded_mini.count()
    checks = build_checks(
        units,
        doc_ids(embedded_mini),
        node_labels=list(c["nodes"]),
        edge_types=list(c["edges"]),
    )
    bad = [r for r in run_parity(embedded_mini, store, checks, workers=4) if not r["ok"]]
    assert bad == []
