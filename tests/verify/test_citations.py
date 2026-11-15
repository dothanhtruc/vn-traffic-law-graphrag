"""verify/citations.py: nguồn ngoài ngữ cảnh, Điểm không tồn tại, unit chưa/hết hiệu lực tại
as_of, nhãn đọc được, trích dẫn tự khai của B0."""

from __future__ import annotations

from datetime import date

import pytest

from trafficlaw.verify.citations import (
    CitableSource,
    FreeCitationIn,
    SoHieuTable,
    doc_label,
    resolve_citation,
    resolve_free_citation,
    unit_label,
)

ND = "Nghị định 168/2024/NĐ-CP"
K3 = "ND168-2024/D6/K3"
SRC = {
    "S1": CitableSource("S1", f"{K3}#2026-01-01", K3, ND),
    "S2": CitableSource("S2", "ND168-2024/D6/K1a#2026-08-15", "ND168-2024/D6/K1a", ND),
    "S3": CitableSource("S3", "LUAT36-2024/D77#2025-01-01", "LUAT36-2024/D77", "Luật"),
}


def test_labels() -> None:
    assert unit_label("ND168-2024/D6/K4/a") == "điểm a khoản 4 Điều 6"
    assert unit_label("LUAT36-2024/D9") == "Điều 9"
    assert unit_label("TT53-2024-BGTVT/PL1-2") == "Phụ lục 1 (phần 2)"
    assert doc_label({"so_hieu": "168/2024/NĐ-CP", "loai": "nghi_dinh"}) == ND
    assert (
        doc_label({"so_hieu": "35/2024/QH15", "loai": "luat", "ten": "Luật Đường bộ"})
        == "Luật Đường bộ (35/2024/QH15)"
    )


@pytest.mark.parametrize("ref", ["S1/a", "[S1/a]", "S1/ a", "S1/K3/a", "S1/điểm a"])
def test_resolve_diem(mini_store, ref: str) -> None:
    c = resolve_citation(ref, SRC, mini_store, date(2026, 1, 1))
    assert c.status == "ok" and c.unit_id == f"{K3}/a"
    assert c.label == f"điểm a khoản 3 Điều 6 {ND}"


def test_resolve_whole_chunk(mini_store) -> None:
    c = resolve_citation("S1", SRC, mini_store, date(2026, 1, 1))
    assert c.valid and c.unit_id == K3 and c.chunk_id == f"{K3}#2026-01-01"


def test_out_of_context_and_bad_format(mini_store) -> None:
    assert resolve_citation("S9", SRC, mini_store, date(2026, 1, 1)).status == (
        "nguon_ngoai_ngu_canh"
    )
    assert resolve_citation("Điều 6", SRC, mini_store, date(2026, 1, 1)).status == "sai_dinh_dang"


def test_diem_not_exists(mini_store) -> None:
    c = resolve_citation("S1/z", SRC, mini_store, date(2026, 1, 1))
    assert c.status == "diem_khong_ton_tai" and not c.valid


def test_diem_not_yet_in_effect(mini_store) -> None:
    # điểm m khoản 3 có hiệu lực từ 01/01/2026
    assert resolve_citation("S1/m", SRC, mini_store, date(2026, 1, 1)).status == "ok"
    assert resolve_citation("S1/m", SRC, mini_store, date(2025, 6, 1)).status == (
        "diem_khong_ton_tai"
    )
    # A2 (không lọc hiệu lực): giữ, gắn cờ
    c = resolve_citation("S1/m", SRC, mini_store, date(2025, 6, 1), validity_filter=False)
    assert c.status == "het_hieu_luc_khong_loc" and c.valid


def test_unit_not_in_effect(mini_store) -> None:
    # khoản 1a bổ sung từ 15/08/2026
    assert resolve_citation("S2", SRC, mini_store, date(2026, 8, 15)).status == "ok"
    c = resolve_citation("S2", SRC, mini_store, date(2026, 7, 1))
    assert c.status == "het_hieu_luc" and not c.valid


def test_free_citations_b0(mini_store) -> None:
    t = SoHieuTable(mini_store)
    d = date(2026, 1, 1)

    def r(**kw: str | None):
        return resolve_free_citation(FreeCitationIn(**kw), t, mini_store, d)  # type: ignore[arg-type]

    ok = r(van_ban="168/2024/NĐ-CP", dieu="6", khoan="3", diem="a")
    assert ok.status == "ok" and ok.unit_id == f"{K3}/a"
    assert r(van_ban="168/2024/NĐ-CP", dieu="6", khoan="3").unit_id == K3
    assert r(van_ban="168/2024/NĐ-CP", dieu="999").status == "khong_ton_tai"
    assert r(van_ban="100/2019/NĐ-CP", dieu="5").status == "van_ban_khong_ro"
    assert r(van_ban="168/2024/NĐ-CP", dieu="6", khoan="1a").status == "het_hieu_luc"
    with pytest.raises(ValueError):
        FreeCitationIn(van_ban="https://example.com/168", dieu="6")
    with pytest.raises(ValueError):
        FreeCitationIn(van_ban="168/2024/NĐ-CP", dieu="Điều 6")


def test_self_label_and_fact_unit(mini_store) -> None:
    d = date(2026, 1, 1)
    # S1 là khoản 3: "S1/K3" = cả nguồn
    c = resolve_citation("S1/K3", SRC, mini_store, d)
    assert c.status == "ok" and c.unit_id == K3
    # khoản 16 điểm a (nêu mức trừ điểm) ngoài chunk: chỉ hợp lệ khi có trong bảng con số
    assert resolve_citation("S1/K16/a", SRC, mini_store, d).status == "diem_khong_ton_tai"
    src = {
        "S1": CitableSource("S1", SRC["S1"].chunk_id, K3, ND, frozenset({"ND168-2024/D6/K16/a"}))
    }
    c = resolve_citation("S1/K16/a", src, mini_store, d)
    assert c.status == "ok_bang_so" and c.valid and c.unit_id == "ND168-2024/D6/K16/a"


@pytest.mark.parametrize(
    ("label", "want"),
    [
        ("a", f"{K3}/a"),
        ("K3/a", f"{K3}/a"),
        ("3/a", f"{K3}/a"),
        ("3", K3),
        ("K3", K3),
        ("K6/3/a", f"{K3}/a"),
        ("D6/K3/a", f"{K3}/a"),
        ("khoản 3 điểm a", f"{K3}/a"),
    ],
)
def test_label_forms(mini_store, label: str, want: str) -> None:
    c = resolve_citation(f"S1/{label}", SRC, mini_store, date(2026, 1, 1))
    assert c.status == "ok" and c.unit_id == want


def test_label_other_khoan_rejected(mini_store) -> None:
    # khoản khác của cùng Điều, không có trong nguồn, không có trong bảng con số → loại
    assert resolve_citation("S1/4/a", SRC, mini_store, date(2026, 1, 1)).status == (
        "diem_khong_ton_tai"
    )
