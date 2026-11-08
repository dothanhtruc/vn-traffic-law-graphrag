"""M5: dẫn chiếu regex (CLAUDE.md mục 13) trên trích đoạn văn bản thật ở ``tests/fixtures``."""

from __future__ import annotations

from pathlib import Path

import pytest

from trafficlaw.graph.doc_names import DocNameTable, load_doc_aliases
from trafficlaw.graph.references import (
    delegations,
    extract_references,
    find_spans,
    guidance_references,
    header_scope,
)
from trafficlaw.ingest.structure import Unit, parse_structure
from trafficlaw.registry.loader import load_registry

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = REPO_ROOT / "tests" / "fixtures"


@pytest.fixture(scope="module")
def names() -> DocNameTable:
    reg = load_registry(REPO_ROOT / "data/registry/documents.yaml")
    return DocNameTable(reg, *load_doc_aliases(REPO_ROOT / "data/registry/doc_aliases.yaml"))


def _units(doc_id: str, fixture: str) -> dict[str, Unit]:
    text = (FIXTURES / fixture).read_text(encoding="utf-8")
    return {u.id: u for u in parse_structure(doc_id, text).units}


def _line(fixture: str, prefix: str) -> str:
    lines = (FIXTURES / fixture).read_text(encoding="utf-8").split("\n")
    return next(x for x in lines if x.startswith(prefix))


def _ids(text: str, uid: str, names: DocNameTable) -> list[tuple[str, ...]]:
    return [r.unit_ids for r in extract_references(text, uid, names)]


# ------------------------------------------------------------------ Luật 36


def test_luat36_dieu9_khong_co_dan_chieu(names: DocNameTable) -> None:
    """Đ9 có 20+ câu "Điều khiển xe …": không câu nào là dẫn chiếu."""
    units = _units("LUAT36-2024", "luat36_dieu9.txt")
    assert len(units) > 20
    for u in units.values():
        assert extract_references(u.text, u.id, names) == [], u.id


def test_luat36_dieu7_khoan_dieu_nay_va_uy_quyen(names: DocNameTable) -> None:
    u = _units("LUAT36-2024", "luat36_dieu7.txt")["LUAT36-2024/D7/K3"]
    assert _ids(u.text, u.id, names) == [("LUAT36-2024/D7/K1", "LUAT36-2024/D7/K2")]
    dl = delegations(u.text, u.id, names)
    assert [(d.co_quan, d.ref.unit_ids) for d in dl] == [
        ("Chính phủ", ("LUAT36-2024/D7/K1", "LUAT36-2024/D7/K2"))
    ]


# ------------------------------------------------------------------ NĐ 168 Điều 6


def test_nd168_dieu6_danh_sach_nhieu_nhom_ket_thuc_dieu_nay(names: DocNameTable) -> None:
    """Các nhóm ngăn bằng ";" (cả "khoản 7" đứng riêng) dùng chung "Điều này" ở cuối."""
    u = _units("ND168-2024", "nd168_dieu6_k1_k3.txt")["ND168-2024/D6/K1/a"]
    groups = {
        "2": "a c d đ",
        "3": "a d đ e n o",
        "4": "a b đ e i k l",
        "5": "a b c d đ i k",
        "6": "a",
        "7": "",
        "9": "b d",
        "10": "a",
        "11": "đ",
    }
    want = [
        f"ND168-2024/D6/K{k}" + (f"/{d}" if d else "")
        for k, ds in groups.items()
        for d in (ds.split() or [""])
    ]
    [got] = _ids(u.text, u.id, names)
    assert sorted(got) == sorted(want)
    assert len(got) == 30


def test_nd168_dieu6_diem_khoan_dieu_nay(names: DocNameTable) -> None:
    units = _units("ND168-2024", "nd168_dieu6_k1_k3.txt")
    u = units["ND168-2024/D6/K2/đ"]
    assert _ids(u.text, u.id, names) == [("ND168-2024/D6/K4/đ", "ND168-2024/D6/K7/c")]
    u = units["ND168-2024/D6/K2/c"]
    assert _ids(u.text, u.id, names) == [("ND168-2024/D6/K5/n", "ND168-2024/D6/K5/o")]


def test_nd168_dieu47_ngoac_don_chua_dan_chieu(names: DocNameTable) -> None:
    """ "Điều 13 (điểm a khoản 4; …), Điều 14 (…)": Điểm/Khoản trong ngoặc thuộc Điều trước."""
    text = _line("nd168_dieu47_k3.txt", "a)")
    refs = extract_references(text, "ND168-2024/D47/K3/a", names)
    assert refs[0].unit_ids[:5] == (
        "ND168-2024/D13/K4/a",
        "ND168-2024/D13/K6/a",
        "ND168-2024/D13/K7/a",
        "ND168-2024/D13/K7/b",
        "ND168-2024/D13/K8/a",
    )
    assert "ND168-2024/D16/K2/đ" in refs[0].unit_ids
    assert refs[1].unit_ids[-1] == "ND168-2024/D32/K13/d"
    assert refs[2].unit_ids == ("ND168-2024/D32",)  # "Điều 32 của Nghị định này"


def test_nd168_dieu52_pham_vi_sua_doi_van_ban_khac(names: DocNameTable) -> None:
    """Điều 52 sửa NĐ 100/2019 (ngoài danh mục): dẫn chiếu trong Điều thuộc NĐ 100/2019."""
    units = _units("ND168-2024", "nd168_dieu52.txt")
    scope = header_scope(units["ND168-2024/D52"].text, "ND168-2024/D52", names)
    assert scope is not None
    assert (scope.doc_kind, scope.doc, scope.reason) == (
        "external",
        "EXT:100/2019/NĐ-CP",
        "sua_doi",
    )
    u = units["ND168-2024/D52/K2/a"]
    [ref] = extract_references(u.text, u.id, names, scope)
    assert (ref.doc, ref.unit_ids, ref.ref_text) == (
        "EXT:100/2019/NĐ-CP",
        (),
        "điểm d khoản 6 Điều 28",
    )


def test_luat35_dieu84_k4_pham_vi_trong_chinh_unit(names: DocNameTable) -> None:
    text = (FIXTURES / "luat35_dieu84_k4.txt").read_text(encoding="utf-8")
    scope = header_scope(text, "LUAT35-2024/D84/K4", names)
    assert scope is not None and scope.doc == "EXT:28/2004/QH11"
    refs = extract_references(text, "LUAT35-2024/D84/K4", names, scope)
    assert all(r.doc.startswith("EXT:") for r in refs)
    assert ("khoản 5 Điều 51", "EXT:28/2004/QH11") in [(r.ref_text, r.doc) for r in refs]


# ------------------------------------------------------------------ NĐ 165, NĐ 151: hướng dẫn


def test_nd165_mo_dau_huong_dan_luat35_va_dieu77_luat36(names: DocNameTable) -> None:
    units = _units("ND165-2024", "nd165_mo_dau_dieu1.txt")
    for uid in ("ND165-2024", "ND165-2024/D1"):
        # Phần mở đầu: trích yếu + câu ban hành cùng nêu → lặp; build khử trùng.
        refs = guidance_references(units[uid].text, uid, names)
        assert {(r.doc, r.unit_ids) for r in refs} == {
            ("LUAT35-2024", ()),
            ("LUAT36-2024", ("LUAT36-2024/D77",)),
        }, uid
    # Dòng "Căn cứ …" chỉ là dẫn chiếu (can_cu), không phải hướng dẫn.
    all_refs = extract_references(units["ND165-2024"].text, "ND165-2024", names)
    assert "EXT:LUAT-XAY-DUNG" in {r.doc for r in all_refs}
    assert header_scope(units["ND165-2024/D1"].text, "ND165-2024/D1", names) is None


def test_nd151_dieu1_pham_vi_huong_dan(names: DocNameTable) -> None:
    units = _units("ND151-2024", "nd151_mo_dau_dieu1.txt")
    scope = header_scope(units["ND151-2024/D1"].text, "ND151-2024/D1", names)
    assert scope is not None
    assert (scope.doc, scope.reason) == ("LUAT36-2024", "huong_dan")
    u = units["ND151-2024/D1/K2"]
    [ref] = extract_references(u.text, u.id, names, scope)
    assert ref.unit_ids == ("LUAT36-2024/D7/K3",)
    # Trích yếu bị ngắt dòng ("Luật Trật tự,\nan toàn …") vẫn nhận đủ tên.
    refs = guidance_references(units["ND151-2024"].text, "ND151-2024", names)
    assert {r.doc for r in refs} == {"LUAT36-2024"}


# ------------------------------------------------------------------ NĐ 158 Điều 7


def test_nd158_dieu7_dan_chieu_luat_theo_ten(names: DocNameTable) -> None:
    units = _units("ND158-2024", "nd158_dieu7.txt")
    u = units["ND158-2024/D7/K2/a"]
    assert _ids(u.text, u.id, names) == [("LUAT35-2024/D56/K10",)]
    u = units["ND158-2024/D7/K5"]
    assert _ids(u.text, u.id, names) == [("LUAT36-2024/D56/K1",)]
    u = units["ND158-2024/D7/K5/d"]
    assert _ids(u.text, u.id, names) == [
        ("ND158-2024/D7/K5/a", "ND158-2024/D7/K5/b", "ND158-2024/D7/K5/c")
    ]
    u = units["ND158-2024/D7/K2/b"]  # Mẫu số 06 Phụ lục XIII → Phụ lục chứa Mẫu
    assert _ids(u.text, u.id, names) == [("ND158-2024/PL13",)]


def test_nd158_dieu7_k8_trich_yeu_van_ban_khac_khong_la_huong_dan(names: DocNameTable) -> None:
    """ "… Nghị định số 151/2024/NĐ-CP … quy định chi tiết … Luật …": trích yếu của ND151."""
    u = _units("ND158-2024", "nd158_dieu7.txt")["ND158-2024/D7/K8"]
    refs = extract_references(u.text, u.id, names)
    assert [(r.doc, r.unit_ids) for r in refs] == [("ND151-2024", ()), ("LUAT36-2024", ())]
    assert guidance_references(u.text, u.id, names) == []


# ------------------------------------------------------------------ ca âm / ca biên (câu ngắn)


@pytest.mark.parametrize(
    "text",
    [
        "tại thời điểm này phải xuất trình",
        "các điểm kiểm tra tải trọng xe",
        "bị trừ điểm giấy phép lái xe 02 điểm",
        "theo Mẫu số 01 ban hành kèm theo Thông tư này",
        "Điều khiển xe chạy quá tốc độ",
        "theo quy định của luật",
    ],
)
def test_khong_phai_dan_chieu(text: str, names: DocNameTable) -> None:
    assert find_spans(text, names) == []


def test_so_tran_chi_nhan_dung_loai(names: DocNameTable) -> None:
    """ "và y tế": chữ "y" không được nhận là Điểm sau "Điều 5"."""
    refs = extract_references("tại khoản 2 Điều 5 và y tế", "ND168-2024/D6/K1", names)
    assert [r.unit_ids for r in refs] == [("ND168-2024/D5/K2",)]


def test_khoang_den(names: DocNameTable) -> None:
    refs = extract_references("từ khoản 1 đến khoản 3 Điều 5", "ND168-2024/D6/K1", names)
    assert refs[0].unit_ids == ("ND168-2024/D5/K1", "ND168-2024/D5/K2", "ND168-2024/D5/K3")
    refs = extract_references("điểm a đến điểm đ khoản 1", "ND168-2024/D6/K2", names)
    assert refs[0].unit_ids == tuple(f"ND168-2024/D6/K1/{x}" for x in ["a", "b", "c", "d", "đ"])


def test_dieu_nay_ket_thuc_span(names: DocNameTable) -> None:
    """ "khoản 1 Điều này và khoản 2 Điều 7 của Nghị định số 151/2024/NĐ-CP": hai văn bản."""
    text = "tại khoản 1 Điều này và khoản 2 Điều 7 của Nghị định số 151/2024/NĐ-CP"
    refs = extract_references(text, "ND168-2024/D6/K3", names)
    assert [(r.doc, r.unit_ids) for r in refs] == [
        ("ND168-2024", ("ND168-2024/D6/K1",)),
        ("ND151-2024", ("ND151-2024/D7/K2",)),
    ]


def test_khoan_thieu_dieu_trong_van_ban_khac_la_loi(names: DocNameTable) -> None:
    refs = extract_references("khoản 2 Luật Đường bộ", "ND165-2024/D5/K1", names)
    assert refs[0].error is not None and refs[0].doc == "LUAT35-2024"
