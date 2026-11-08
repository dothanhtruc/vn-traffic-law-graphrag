"""M4: chú thích VBHN, chuẩn hoá khi so, đối chiếu Khoản và kiểm tra chéo."""

from __future__ import annotations

from datetime import date

from tests.ingest.m4_helpers import unit, units_of
from trafficlaw.ingest.vbhn import (
    VbhnEntry,
    compare_vbhn,
    is_repealed_placeholder,
    light_norm,
    parse_footnote,
    strong_norm,
)
from trafficlaw.ingest.versions import UnitVersion, VersionStore

SO_HIEU = {"241/2026/NĐ-CP": "ND241-2026", "165/2024/NĐ-CP": "ND165-2024"}


def test_parse_footnotes_from_vbhn65_fixture() -> None:
    [d4] = [u for u in units_of("VBHN65-2026-BXD", "vbhn65_dieu4.txt") if u.level == "dieu"]
    [(n, text)] = d4.footnotes.items()
    fn = parse_footnote(d4.id, n, text)
    assert (fn.subject, fn.op, fn.source_so_hieu) == ("dieu", "sua_doi", "241/2026/NĐ-CP")
    assert fn.effective_from == date(2026, 7, 1)
    fn = parse_footnote(
        "VBHN55-VPQH/D6/K3",
        "2",
        "Cụm từ “, Bộ Lao động, Thương binh và Xã hội,” được bỏ theo quy định tại điểm a khoản 22 "
        "Điều 7 của Luật số 118/2025/QH15 sửa đổi, bổ sung một số điều của 10 luật có liên quan "
        "đến an ninh, trật tự, có hiệu lực kể từ ngày 01 tháng 7 năm 2026.",
    )
    assert (fn.subject, fn.op, fn.source_so_hieu) == ("cum_tu", "bo", "118/2025/QH15")
    info = parse_footnote(
        "VBHN65-2026-BXD", "1", "Nghị định số 243/2025/NĐ-CP có căn cứ ban hành như sau:"
    )
    assert info.op == "quy_dinh"


def test_normalisation() -> None:
    a = "1. Cảng thuỷ nội địa[^3], hàng hoá; “Cấm”"
    b = '1. Cảng thủy nội địa, hàng hóa. "Cấm"'
    assert light_norm(a) != light_norm(b)
    assert strong_norm(a) == strong_norm(b)  # chỉ khác dấu câu / kiểu bỏ dấu
    assert strong_norm("phạt 4.000.000 đồng") != strong_norm("phạt 6.000.000 đồng")
    assert strong_norm("Bộ Giao thông vận tải") != strong_norm("Bộ Xây dựng")
    assert is_repealed_placeholder("d) (Được bãi bỏ)[^18]")
    assert not is_repealed_placeholder("d) Được bãi bỏ nếu không nộp hồ sơ")


def _ver(uid: str, text: str, start: date, src: str | None = None, v: int = 0) -> UnitVersion:
    return UnitVersion(
        unit_id=uid, version=v, text=text, effective_from=start, status="active", source_unit_id=src
    )


def test_compare_excludes_out_of_registry_and_crosschecks() -> None:
    entry = VbhnEntry(
        vbhn="VBHN65-2026-BXD",
        base_doc="ND165-2024",
        as_of=date(2026, 7, 1),
        out_of_registry_sources=["243/2025/NĐ-CP"],
        crosscheck_source="241/2026/NĐ-CP",
        known_issues=["VBHN65-2026-BXD/D9/K2"],
    )
    vb = [
        unit("VBHN65-2026-BXD/D9", "dieu", "Điều 9. A"),
        unit("VBHN65-2026-BXD/D9/K1", "khoan", "1. Bộ Xây dựng quản lý.[^7]"),
        unit("VBHN65-2026-BXD/D9/K2", "khoan", "2. Lỗi font."),
        unit("VBHN65-2026-BXD/D9/K3", "khoan", "3. Thêm bởi NĐ 243.[^8]"),
        unit("VBHN65-2026-BXD/D9/K4", "khoan", "4. Giữ nguyên, thuỷ nội địa."),
    ]
    vb[1].footnotes = {
        "7": "Cụm từ “Bộ Giao thông vận tải” được thay thế bởi cụm từ “Bộ Xây dựng” theo quy định "
        "tại khoản 1 Điều 25 Nghị định số 241/2026/NĐ-CP, có hiệu lực thi hành kể từ ngày 01 tháng "
        "7 năm 2026."
    }
    vb[3].footnotes = {
        "8": "Khoản này được bổ sung theo quy định tại Điều 79 Nghị định số 243/2025/NĐ-CP, "
        "có hiệu lực thi hành kể từ ngày 11 tháng 9 năm 2025."
    }
    base = [
        unit("ND165-2024/D9", "dieu", "Điều 9. A"),
        unit("ND165-2024/D9/K1", "khoan", "1. Bộ Giao thông vận tải quản lý."),
        unit("ND165-2024/D9/K2", "khoan", "2. Đúng."),
        unit("ND165-2024/D9/K4", "khoan", "4. Giữ nguyên, thủy nội địa."),
    ]
    d0, d1 = date(2025, 1, 1), date(2026, 7, 1)
    versions = [_ver(u.id, u.text, d0) for u in base]
    versions[1] = versions[1].model_copy(
        update={"effective_to": date(2026, 6, 30), "status": "amended"}
    )
    versions.append(_ver("ND165-2024/D9/K1", "1. Bộ Xây dựng quản lý.", d1, "ND241-2026/D25/K1", 1))
    res = compare_vbhn(entry, vb, base, [], VersionStore(versions), SO_HIEU)
    st = {r.unit_id: r.status for r in res.rows}
    assert st["ND165-2024/D9/K1"] == "khop"
    assert st["ND165-2024/D9/K2"] == "loai_loi_du_lieu"
    assert st["ND165-2024/D9/K3"] == "loai_ngoai_danh_muc"
    assert st["ND165-2024/D9/K4"] == "chi_khac_dinh_dang"
    assert res.crosscheck_checked == 1 and not res.crosscheck_failures


def test_crosscheck_fails_without_matching_version() -> None:
    entry = VbhnEntry(
        vbhn="VBHN65-2026-BXD",
        base_doc="ND165-2024",
        as_of=date(2026, 7, 1),
        crosscheck_source="241/2026/NĐ-CP",
    )
    vb = [
        unit("VBHN65-2026-BXD/D9", "dieu", "Điều 9. A"),
        unit("VBHN65-2026-BXD/D9/K1", "khoan", "1. B.[^2]"),
    ]
    vb[1].footnotes = {
        "2": "Khoản này được sửa đổi, bổ sung theo quy định tại khoản 1 Điều 4 Nghị định số "
        "241/2026/NĐ-CP, có hiệu lực thi hành kể từ ngày 01 tháng 7 năm 2026."
    }
    base = [unit("ND165-2024/D9", "dieu", "Điều 9. A"), unit("ND165-2024/D9/K1", "khoan", "1. B.")]
    store = VersionStore([_ver(u.id, u.text, date(2025, 1, 1)) for u in base])
    res = compare_vbhn(entry, vb, base, [], store, SO_HIEU)
    assert res.match_rate == 1.0
    assert len(res.crosscheck_failures) == 1  # khớp chữ nhưng không có phiên bản ND241
