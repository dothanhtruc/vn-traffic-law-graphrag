"""M8: nối chế tài ↔ hành vi qua cấu trúc + DAN_CHIEU (mini_graph = ND168 Điều 6 thật), ghi vào
EmbeddedStore và truy vấn theo as_of; danh mục PhuongTien từ LUAT36 Điều 34."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from trafficlaw.graph.catalog import CatalogConfig, build_catalog
from trafficlaw.graph.embedded import EmbeddedStore
from trafficlaw.graph.extract import (
    Assembly,
    ExtractConfig,
    assemble_catalog,
    assemble_rules,
    prune_dangling,
)
from trafficlaw.graph.store import GraphEdge, GraphNode, data_hash, graph_files, load_graph_dir
from trafficlaw.utils.jsonl import write_jsonl

MINI = Path(__file__).resolve().parents[1] / "fixtures/mini_graph"
D6 = "ND168-2024/D6"


@pytest.fixture(scope="module")
def store() -> EmbeddedStore:
    return EmbeddedStore.from_dir(MINI)


@pytest.fixture(scope="module")
def asm(store: EmbeddedStore) -> Assembly:
    a = Assembly()
    assemble_rules(store, ExtractConfig(), a)
    prune_dangling(a, store)
    return a


def _in(asm: Assembly, dst: str) -> list[GraphEdge]:
    return sorted((e for e in asm.edges.values() if e.dst == dst), key=lambda e: e.src)


def test_points_linked_through_dan_chieu(asm: Assembly) -> None:
    """K16 b "Thực hiện hành vi quy định tại điểm h khoản 5; khoản 6; điểm b khoản 7; điểm b,
    điểm c, điểm d khoản 9 … bị trừ … 04 điểm" → đúng các Điểm được dẫn chiếu (khoản 6 → mọi
    Điểm của nó), lấy từ cạnh DAN_CHIEU, không để LLM đoán."""
    nid = f"DIEM:{D6}/K16/b@v0#0"
    assert asm.nodes[nid].props["so_diem"] == 4
    srcs = [e.src for e in _in(asm, nid)]
    assert srcs == [
        f"{D6}/K5/h@v0",
        f"{D6}/K6/a@v0",
        f"{D6}/K6/b@v0",
        f"{D6}/K6/c@v0",
        f"{D6}/K6/d@v0",
        f"{D6}/K7/b@v0",
        f"{D6}/K9/b@v0",
        f"{D6}/K9/c@v0",
        f"{D6}/K9/d@v0",
    ]
    e = _in(asm, nid)[0]
    assert e.type == "BI_TRU_DIEM"
    assert e.props["nguon"] == "dan_chieu" and e.props["stated_in"] == f"{D6}/K16/b@v0"


def test_all_point_edges_come_from_k16(asm: Assembly) -> None:
    """DAN_CHIEU trong cụm ngoại lệ "trừ các hành vi … quy định tại …" (K1 a) không sinh cạnh."""
    stated = {e.props["stated_in"] for e in asm.edges.values() if e.type == "BI_TRU_DIEM"}
    assert stated == {f"{D6}/K16/{x}@v0" for x in "abcd"}
    assert {asm.nodes[f"DIEM:{D6}/K16/{x}@v0#0"].props["so_diem"] for x in "abcd"} == {
        2,
        4,
        6,
        10,
    }


def test_fine_inherited_by_points(asm: Assembly) -> None:
    nid = f"CHETAI:{D6}/K1@v0#0"
    p = asm.nodes[nid].props
    assert (p["loai"], p["min_vnd"], p["max_vnd"]) == ("phat_tien", 400_000, 600_000)
    es = _in(asm, nid)
    assert [e.src for e in es] == [f"{D6}/K1/{x}@v0" for x in ["a", "b", "c", "d", "đ"]]
    assert {e.props["nguon"] for e in es} == {"ke_thua_khoan"}


def test_direct_and_revocation(asm: Assembly) -> None:
    (e,) = _in(asm, f"CHETAI:{D6}/K13@v0#0")
    assert e.src == f"{D6}/K13@v0" and e.props["nguon"] == "truc_tiep"
    rev = asm.nodes[f"CHETAI:{D6}/K15/c@v0#0"].props
    assert (rev["loai"], rev["min_thang"], rev["max_thang"]) == ("tuoc_quyen", 22, 24)
    assert [e.src for e in _in(asm, f"CHETAI:{D6}/K15/c@v0#0")] == [
        f"{D6}/K11/a@v0",
        f"{D6}/K11/b@v0",
        f"{D6}/K11/c@v0",
        f"{D6}/K11/d@v0",
        f"{D6}/K13@v0",
        f"{D6}/K14@v0",
    ]


def test_effective_dates_follow_both_versions(asm: Assembly) -> None:
    """K3 m có hiệu lực riêng từ 01/01/2026 và được sửa từ 15/08/2026: cạnh BI_XU_PHAT của
    mức phạt K3 mang giao khoảng hiệu lực của hai phiên bản."""
    es = [e for e in _in(asm, f"CHETAI:{D6}/K3@v0#0") if e.src.startswith(f"{D6}/K3/m@")]
    got = sorted((e.src, e.props["effective_from"], e.props["effective_to"]) for e in es)
    assert got == [
        (f"{D6}/K3/m@v0", "2026-01-01", "2026-08-14"),
        (f"{D6}/K3/m@v1", "2026-08-15", None),
    ]


def test_upsert_and_query_as_of(store: EmbeddedStore, asm: Assembly) -> None:
    s = EmbeddedStore.from_dir(MINI)
    s.upsert_nodes(asm.sorted_nodes())
    s.upsert_edges(asm.sorted_edges())
    m = f"{D6}/K3/m"

    def fines(d: date) -> list[str]:
        v = s.version_at(m, d)
        if v is None:
            return []
        return [e.dst for e in s.out_edges(v.id, types=["BI_XU_PHAT"], as_of=d)]

    assert fines(date(2025, 6, 1)) == []  # chưa có hiệu lực
    assert fines(date(2026, 1, 1)) == [f"CHETAI:{D6}/K3@v0#0"]
    assert fines(date(2026, 8, 15)) == [f"CHETAI:{D6}/K3@v0#0"]
    sub = s.expand([f"{D6}/K5/h"], edge_types=["BI_TRU_DIEM"], as_of=date(2026, 1, 1))
    assert f"DIEM:{D6}/K16/b@v0#0" in sub.nodes
    # nút ngữ nghĩa là điểm dừng: hop 2 không đi tiếp sang các Điểm khác bị trừ cùng 4 điểm
    sub2 = s.expand([f"{D6}/K5/h"], edge_types=["BI_TRU_DIEM"], as_of=date(2026, 1, 1), hops=2)
    assert f"{D6}/K6/a" not in sub2.nodes


def test_dangling_edge_raises(store: EmbeddedStore) -> None:
    s = EmbeddedStore.from_dir(MINI)
    with pytest.raises(KeyError):
        s.upsert_edges([GraphEdge.make("BI_XU_PHAT", f"{D6}/K1/a@v0", "CHETAI:khong-co", {})])


def test_semantic_files_optional(tmp_path: Path, asm: Assembly) -> None:
    for n in ("nodes.jsonl", "edges_struct.jsonl", "edges_legal.jsonl"):
        (tmp_path / n).write_bytes((MINI / n).read_bytes())
    h0 = data_hash(tmp_path)
    assert h0 == data_hash(MINI)
    assert graph_files(tmp_path) == ["nodes.jsonl", "edges_struct.jsonl", "edges_legal.jsonl"]
    write_jsonl(tmp_path / "nodes_semantic.jsonl", [n.to_dict() for n in asm.sorted_nodes()])
    with pytest.raises(FileNotFoundError):
        graph_files(tmp_path)  # phải có đủ cả hai file
    write_jsonl(tmp_path / "edges_semantic.jsonl", [e.to_dict() for e in asm.sorted_edges()])
    assert data_hash(tmp_path) != h0
    nodes, edges = load_graph_dir(tmp_path)
    assert any(n.label == "DiemGPLX" for n in nodes)
    s = EmbeddedStore.from_dir(tmp_path)
    assert s.count()["nodes"]["DiemGPLX"] == 4
    base = EmbeddedStore.from_dir_base(tmp_path)
    assert "DiemGPLX" not in base.count()["nodes"]


# --------------------------------------------------------------------------- danh mục


def _tiny_store(units: list[tuple[str, str, str, str]]) -> EmbeddedStore:
    """(unit_id, label, parent, text) → store có VanBan, unit, PhienBan v0, THUOC, KE_TIEP."""
    s = EmbeddedStore()
    docs = sorted({u.split("/")[0] for u, *_ in units})
    s.upsert_nodes(
        [GraphNode(d, "VanBan", {"doc_id": d, "tier": "A", "indexable": True}) for d in docs]
    )
    nodes, edges = [], []
    prev: dict[str, str] = {}
    for uid, label, parent, text in units:
        nodes += [
            GraphNode(uid, label, {"doc_id": uid.split("/")[0]}),
            GraphNode(
                f"{uid}@v0",
                "PhienBan",
                {
                    "unit_id": uid,
                    "version": 0,
                    "text": text,
                    "effective_from": "2025-01-01",
                    "effective_to": None,
                    "status": "active",
                },
            ),
        ]
        edges += [
            GraphEdge.make("THUOC", uid, parent),
            GraphEdge.make("CO_PHIEN_BAN", uid, f"{uid}@v0"),
        ]
        if parent in prev:
            edges.append(GraphEdge.make("KE_TIEP", prev[parent], uid))
        prev[parent] = uid
    s.upsert_nodes(nodes)
    s.upsert_edges(edges)
    return s


L36 = "LUAT36-2024"


def test_catalog_from_law_text() -> None:
    s = _tiny_store(
        [
            (f"{L36}/D2", "Dieu", L36, "Điều 2. Giải thích từ ngữ"),
            (
                f"{L36}/D2/K2",
                "Khoan",
                f"{L36}/D2",
                "2. Phương tiện giao thông đường bộ là các loại xe, bao gồm: phương tiện giao "
                "thông cơ giới đường bộ (sau đây gọi là xe cơ giới), phương tiện giao thông thô "
                "sơ đường bộ (sau đây gọi là xe thô sơ), xe máy chuyên dùng và các loại xe "
                "tương tự.",
            ),
            (f"{L36}/D34", "Dieu", L36, "Điều 34. Phân loại phương tiện giao thông đường bộ"),
            (f"{L36}/D34/K1", "Khoan", f"{L36}/D34", "1. Xe cơ giới bao gồm:"),
            (
                f"{L36}/D34/K1/a",
                "Diem",
                f"{L36}/D34/K1",
                "a) Xe ô tô gồm: xe có từ bốn bánh trở lên …;",
            ),
            (
                f"{L36}/D34/K1/e",
                "Diem",
                f"{L36}/D34/K1",
                "e) Xe mô tô gồm: xe có hai hoặc ba bánh chạy bằng động cơ, …, trừ xe gắn máy;",
            ),
            (
                f"{L36}/D34/K1/g",
                "Diem",
                f"{L36}/D34/K1",
                "g) Xe gắn máy là xe có hai hoặc ba bánh chạy bằng động cơ, có vận tốc thiết kế "
                "không lớn hơn 50 km/h;",
            ),
            (
                f"{L36}/D34/K1/h",
                "Diem",
                f"{L36}/D34/K1",
                "h) Xe tương tự các loại xe quy định tại khoản này.",
            ),
            (f"{L36}/D34/K2", "Khoan", f"{L36}/D34", "2. Xe thô sơ bao gồm:"),
            (
                f"{L36}/D34/K2/b",
                "Diem",
                f"{L36}/D34/K2",
                "b) Xe đạp máy, gồm cả xe đạp điện, là xe đạp có trợ lực từ động cơ;",
            ),
            (
                f"{L36}/D34/K5",
                "Khoan",
                f"{L36}/D34",
                "5. Xe tương tự các loại xe cơ giới, xe thô sơ được quản lý, sử dụng theo quy định "
                "đối với loại xe cơ giới, xe thô sơ đó; người điều khiển xe tương tự xe ô tô …",
            ),
        ]
    )
    cfg = CatalogConfig(
        pt_list_dieu=[f"{L36}/D34"],
        pt_def_docs=[L36],
        pt_extra=[{"name": "xe tương tự xe ô tô", "nhom": "xe-co-gioi"}, {"name": "xe buýt"}],  # type: ignore[list-item]
        ct_seed=["người điều khiển xe", "Bộ Công an"],
    )
    cat = build_catalog(s, cfg)
    pt = {e.id: e for e in cat.phuong_tien}
    assert pt["PT:xe-gan-may"].can_cu == f"{L36}/D34/K1/g"
    assert pt["PT:xe-mo-to"].can_cu == f"{L36}/D34/K1/e"
    assert "xe gắn máy" not in pt["PT:xe-mo-to"].aliases  # không gộp đồng nghĩa
    assert pt["PT:xe-co-gioi"].aliases == ["phương tiện giao thông cơ giới đường bộ"]
    assert pt["PT:xe-dap-may"].bao_gom == ["xe đạp điện"]
    assert pt["PT:xe-o-to"].nhom == "xe-co-gioi"
    assert "PT:xe-tuong-tu-xe-o-to" in pt  # có nguyên văn trong K5
    assert "PT:xe-buyt" not in pt  # không có căn cứ trong văn bản → không thêm
    assert not any("quy-dinh-tai" in k for k in pt)
    assert {e.id for e in cat.chu_the} == {
        "CT:nguoi-dieu-khien-xe"
    }  # "Bộ Công an" không có nguyên văn
    assert cat.approved is False
    a = Assembly()
    assemble_catalog(a, cat)
    assert a.nodes["PT:xe-gan-may"].label == "PhuongTien"
