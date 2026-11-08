"""M5: dựng nút + cạnh (hàm thuần) trên trích đoạn thật + vài unit/phiên bản dựng tay."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from tests.ingest.m4_helpers import registry, unit, units_of
from trafficlaw.graph.build import GraphData, build_graph, dangling_edges
from trafficlaw.graph.doc_names import DocNameTable, load_doc_aliases
from trafficlaw.graph.schema import Edge
from trafficlaw.ingest.structure import Unit
from trafficlaw.ingest.versions import AddedUnit, UnitVersion

REPO_ROOT = Path(__file__).resolve().parents[2]
D0 = date(2025, 1, 1)
D1 = date(2026, 8, 15)


def _v0(u: Unit) -> UnitVersion:
    return UnitVersion(unit_id=u.id, version=0, text=u.text, effective_from=D0, status="active")


def _inputs() -> tuple[list[Unit], list[AddedUnit], list[UnitVersion]]:
    units = [
        *units_of("ND168-2024", "nd168_dieu6_k1_k3.txt"),
        *units_of("ND165-2024", "nd165_mo_dau_dieu1.txt"),
        *units_of("ND151-2024", "nd151_mo_dau_dieu1.txt"),
        *units_of("LUAT36-2024", "luat36_dieu7.txt"),
        unit("LUAT36-2024/D6", "dieu", "Điều 6. Giáo dục kiến thức pháp luật", "Giáo dục"),
        unit("LUAT36-2024/D77", "dieu", "Điều 77. Hệ thống quản lý giao thông", "Hệ thống"),
        unit("TT35-2024-BGTVT/D1", "dieu", "Điều 1. Phạm vi điều chỉnh", "Phạm vi"),
    ]
    added = [
        AddedUnit(
            id="ND168-2024/D6/K1a",
            doc_id="ND168-2024",
            level="khoan",
            number="1a",
            text="1a. Phạt cảnh cáo …",
            parent_id="ND168-2024/D6",
            before_id="ND168-2024/D6/K1",
            source_unit_id="ND238-2026/D2/K1",
        )
    ]
    versions = [_v0(u) for u in units]
    by_id = {u.id: u for u in units}

    def close(uid: str) -> None:
        v = next(x for x in versions if x.unit_id == uid and x.version == 0)
        versions[versions.index(v)] = v.model_copy(
            update={"effective_to": date(2026, 8, 14), "status": "amended"}
        )

    # ND238 Đ2 K2 thay cả khoản 2 (khoản + điểm a có phiên bản mới cùng ngày, cùng nguồn).
    for uid in ("ND168-2024/D6/K2", "ND168-2024/D6/K2/a"):
        close(uid)
        versions.append(
            UnitVersion(
                unit_id=uid,
                version=1,
                text=by_id[uid].text + " (sửa)",
                effective_from=D1,
                status="active",
                source_unit_id="ND238-2026/D2/K2",
            )
        )
    close("ND168-2024/D6/K2/b")
    versions.append(
        UnitVersion(
            unit_id="ND168-2024/D6/K2/b",
            version=1,
            text="",
            effective_from=D1,
            status="repealed",
            source_unit_id="ND238-2026/D2/K3",
        )
    )
    versions.append(
        UnitVersion(
            unit_id="ND168-2024/D6/K1a",
            version=1,
            text="1a. Phạt cảnh cáo …",
            effective_from=D1,
            status="active",
            source_unit_id="ND238-2026/D2/K1",
        )
    )
    # TT14/2025 bãi bỏ toàn bộ TT35/2024 → chỉ cạnh cấp văn bản.
    close("TT35-2024-BGTVT/D1")
    versions.append(
        UnitVersion(
            unit_id="TT35-2024-BGTVT/D1",
            version=1,
            text="",
            effective_from=date(2025, 9, 1),
            status="repealed",
            source_unit_id="TT14-2025-BXD/D50/K2",
        )
    )
    return units, added, versions


@pytest.fixture(scope="module")
def graph() -> GraphData:
    reg = registry()
    names = DocNameTable(reg, *load_doc_aliases(REPO_ROOT / "data/registry/doc_aliases.yaml"))
    return build_graph(reg, *_inputs(), names)


def _edges(g: GraphData, etype: str, src: str | None = None, dst: str | None = None) -> list[Edge]:
    return [
        e
        for e in [*g.edges_struct, *g.edges_legal]
        if e.type == etype and (src is None or e.src == src) and (dst is None or e.dst == dst)
    ]


def test_khong_canh_treo_khong_loi(graph: GraphData) -> None:
    assert dangling_edges(graph.nodes, [*graph.edges_struct, *graph.edges_legal]) == []
    assert graph.errors == []


def test_nut_van_ban_sua_doi_va_vbhn_chi_co_van_ban(graph: GraphData) -> None:
    ids = {n.id: n for n in graph.nodes}
    assert ids["ND238-2026"].label == "VanBan" and ids["ND238-2026"].props["is_amendment"]
    assert ids["VBHN55-VPQH"].props["indexable"] is False
    assert not any(n.id.startswith("ND238-2026/") for n in graph.nodes)
    assert ids["ND168-2024/D6/K1a"].props["bo_sung"] is True


def test_cau_truc_thuoc_ke_tiep_phien_ban(graph: GraphData) -> None:
    assert _edges(graph, "THUOC", "ND168-2024/D6/K1/a", "ND168-2024/D6/K1")
    kids = [
        (e.src, e.dst)
        for e in _edges(graph, "KE_TIEP")
        if e.src.startswith("ND168-2024/D6/K") and e.src.count("/") == 2
    ]
    assert kids == [
        ("ND168-2024/D6/K1", "ND168-2024/D6/K2"),
        ("ND168-2024/D6/K1a", "ND168-2024/D6/K1"),  # unit bổ sung "vào trước khoản 1"
        ("ND168-2024/D6/K2", "ND168-2024/D6/K3"),
    ]
    assert _edges(graph, "CO_PHIEN_BAN", "ND168-2024/D6/K2", "ND168-2024/D6/K2@v1")
    n_versions = sum(n.label == "PhienBan" for n in graph.nodes)
    assert len(_edges(graph, "CO_PHIEN_BAN")) == n_versions


def test_sua_doi_bai_bo_cap_unit(graph: GraphData) -> None:
    [k2] = _edges(graph, "SUA_DOI", "ND238-2026", "ND168-2024/D6/K2")
    assert k2.props["effective_from"] == "2026-08-15"
    assert k2.props["source_unit_id"] == "ND238-2026/D2/K2"
    assert k2.props["thao_tac"] == "sua_doi"
    # Điểm a được viết lại cùng chỉ dẫn với khoản cha → cạnh của khoản đã bao.
    assert _edges(graph, "SUA_DOI", "ND238-2026", "ND168-2024/D6/K2/a") == []
    [k1a] = _edges(graph, "SUA_DOI", "ND238-2026", "ND168-2024/D6/K1a")
    assert k1a.props["thao_tac"] == "bo_sung"
    assert _edges(graph, "BAI_BO", "ND238-2026", "ND168-2024/D6/K2/b")


def test_bai_bo_toan_bo_chi_cap_van_ban(graph: GraphData) -> None:
    assert _edges(graph, "BAI_BO", dst="TT35-2024-BGTVT/D1") == []
    [e] = _edges(graph, "BAI_BO", "TT14-2025-BXD", "TT35-2024-BGTVT")
    assert e.props["cap"] == "van_ban" and e.props["scope"] == "toan_bo"
    assert _edges(graph, "SUA_DOI", "ND238-2026", "ND168-2024")  # quan hệ danh mục


def test_dan_chieu_tu_phien_ban(graph: GraphData) -> None:
    [e] = _edges(graph, "DAN_CHIEU", "ND168-2024/D6/K1/a@v0", "ND168-2024/D6/K2/a")
    assert e.props["pham_vi"] == "noi_bo"
    assert e.props["effective_from"] == "2025-01-01"
    # Đích ngoài trích đoạn (khoản 4 trở đi) → không phân giải, không tạo cạnh.
    assert _edges(graph, "DAN_CHIEU", dst="ND168-2024/D6/K4/đ") == []
    assert any(
        u["source_unit_id"] == "ND168-2024/D6/K2/đ" and u["reason"] == "dich_khong_ton_tai"
        for u in graph.unresolved
    )
    # Phiên bản bị bãi bỏ (text rỗng) không có cạnh.
    assert _edges(graph, "DAN_CHIEU", "ND168-2024/D6/K2/b@v1") == []


def test_can_cu_va_van_ban_ngoai(graph: GraphData) -> None:
    [e] = _edges(graph, "DAN_CHIEU", "ND165-2024@v0", "EXT:LUAT-XAY-DUNG")
    assert e.props["can_cu"] is True and e.props["pham_vi"] == "ngoai"
    ext = {n.id: n for n in graph.nodes if n.label == "VanBanNgoai"}
    assert ext["EXT:LUAT-XAY-DUNG"].props["n_refs"] >= 1


def test_huong_dan(graph: GraphData) -> None:
    hd = {(e.src, e.dst, e.props["cap"]) for e in _edges(graph, "HUONG_DAN")}
    assert ("ND165-2024", "LUAT35-2024", "van_ban") in hd
    assert ("ND165-2024", "LUAT36-2024/D77", "unit") in hd
    assert ("ND151-2024", "LUAT36-2024", "van_ban") in hd
    assert ("ND151-2024", "LUAT36-2024/D6", "unit") in hd  # "1. Điều 6 về …" dưới Điều 1
    assert not any(src.startswith("LUAT") for src, _, _ in hd)
    # Danh sách dưới Điều 1 ND151 là dẫn chiếu tới Luật 36 (phạm vi từ câu dẫn).
    [e] = _edges(graph, "DAN_CHIEU", "ND151-2024/D1/K1@v0", "LUAT36-2024/D6")
    assert e.props["pham_vi_tu"] == "ND151-2024/D1"


def test_uy_quyen(graph: GraphData) -> None:
    ids = {n.id: n for n in graph.nodes}
    assert ids["LUAT36-2024/D7/K1"].props["uy_quyen"] == [
        {"co_quan": "Chính phủ", "source_unit_id": "LUAT36-2024/D7/K3"}
    ]


def test_tat_dinh() -> None:
    reg = registry()
    names = DocNameTable(reg, *load_doc_aliases(REPO_ROOT / "data/registry/doc_aliases.yaml"))
    a = build_graph(reg, *_inputs(), names)
    b = build_graph(reg, *_inputs(), names)
    assert a.nodes == b.nodes and a.edges_legal == b.edges_legal
    assert a.edges_struct == b.edges_struct


def test_phien_ban_khong_co_unit_la_loi() -> None:
    reg = registry()
    names = DocNameTable(reg)
    units, added, versions = _inputs()
    versions.append(
        UnitVersion(
            unit_id="ND168-2024/D99", version=0, text="x", effective_from=D0, status="active"
        )
    )
    g = build_graph(reg, units, added, versions, names)
    assert any("ND168-2024/D99" in e for e in g.errors)


def test_van_ban_khong_dung_khong_co_nut_canh() -> None:
    """ND168 Đ52 sửa NĐ 100/2019 (không dùng, CLAUDE.md mục 6): không nút/cạnh tới NĐ 100."""
    reg = registry()
    names = DocNameTable(reg, *load_doc_aliases(REPO_ROOT / "data/registry/doc_aliases.yaml"))
    assert "EXT:100/2019/NĐ-CP" in names.excluded
    units = units_of("ND168-2024", "nd168_dieu52.txt")
    g = build_graph(reg, units, [], [_v0(u) for u in units], names)
    assert not any("100/2019" in n.id for n in g.nodes)
    assert not any("100/2019" in e.dst for e in g.edges_legal)
    # "điểm d khoản 6 Điều 28" trong Điều 52 thuộc NĐ 100, không bị gán sang ND168 Đ28.
    assert not any(e.dst.startswith("ND168-2024/D28") for e in g.edges_legal)
    assert g.ref_stats["ND168-2024"]["van_ban_khong_dung"] >= 4
