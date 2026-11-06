"""M3: parser cấu trúc (hàm thuần) trên trích đoạn văn bản thật ở ``tests/fixtures``."""

from __future__ import annotations

from pathlib import Path

import pytest

from trafficlaw.ingest.structure import Unit, parse_structure, quote_scan

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def _fx(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def _by_id(units: list[Unit]) -> dict[str, Unit]:
    return {u.id: u for u in units}


def _kinds(result) -> list[str]:  # type: ignore[no-untyped-def]
    return [a.kind for a in result.report.anomalies]


# ---------------------------------------------------------------- Điều / Khoản / Điểm


def test_luat36_dieu9_khoan() -> None:
    res = parse_structure("LUAT36-2024", _fx("luat36_dieu9.txt"))
    u = _by_id(res.units)
    d9 = u["LUAT36-2024/D9"]
    assert d9.level == "dieu" and d9.number == "9"
    assert d9.title == "Các hành vi bị nghiêm cấm"
    assert d9.text == "Điều 9. Các hành vi bị nghiêm cấm"
    assert d9.parent_id == "LUAT36-2024"
    khoan = [x for x in res.units if x.level == "khoan"]
    assert [k.number for k in khoan] == [str(n) for n in range(1, len(khoan) + 1)]
    assert khoan[1].id == "LUAT36-2024/D9/K2" and khoan[1].parent_id == "LUAT36-2024/D9"
    assert khoan[1].text.startswith("2. Điều khiển phương tiện")
    assert khoan[1].title is None
    assert res.report.n_dieu == 1 and _kinds(res) == ["dieu_first_not_1"]  # trích đoạn


def test_nd168_dieu6_diem_dd() -> None:
    res = parse_structure("ND168-2024", _fx("nd168_dieu6_k1_k3.txt"))
    u = _by_id(res.units)
    assert "ND168-2024/D6/K1/đ" in u
    dd = u["ND168-2024/D6/K1/đ"]
    assert dd.level == "diem" and dd.number == "đ" and dd.parent_id == "ND168-2024/D6/K1"
    assert dd.text.startswith("đ) ")
    k1 = u["ND168-2024/D6/K1"]
    # Text của Khoản = câu dẫn trước điểm a, không chứa các Điểm.
    assert k1.text.startswith("1. Phạt tiền từ 400.000 đồng") and "\na)" not in k1.text
    diem_k1 = [x.number for x in res.units if x.parent_id == "ND168-2024/D6/K1"]
    assert diem_k1[:5] == ["a", "b", "c", "d", "đ"]
    # Thứ tự ghi = thứ tự trong văn bản.
    assert [x.line_start for x in res.units] == sorted(x.line_start for x in res.units)


def test_tt38_dieu7_khong_chia_khoan() -> None:
    res = parse_structure("TT38-2024-BGTVT", _fx("tt38_dieu7.txt"))
    u = _by_id(res.units)
    d7 = u["TT38-2024-BGTVT/D7"]
    assert not [x for x in res.units if x.parent_id == d7.id]
    assert "\n" in d7.text  # tiêu đề + đoạn nội dung (bảng) thuộc Điều
    # Dòng bảng "ô | ô" không bao giờ thành tiêu đề.
    assert all(" | " not in (x.title or "") for x in res.units)


def test_diem_directly_under_dieu() -> None:
    text = "Điều 1. Phạm vi\nĐiều 2. Đối tượng\nĐiều 3. Nguyên tắc\nVăn bản dẫn:\na) Một;\nb) Hai."
    u = _by_id(parse_structure("LUAT36-2024", text).units)
    assert u["LUAT36-2024/D3/b"].parent_id == "LUAT36-2024/D3"
    assert u["LUAT36-2024/D3"].text == "Điều 3. Nguyên tắc\nVăn bản dẫn:"


def test_vbhn65_dieu52a_footnote_in_title() -> None:
    res = parse_structure("VBHN65-2026-BXD", _fx("vbhn65_dieu52a.txt"))
    u = _by_id(res.units)
    d = u["VBHN65-2026-BXD/D52a"]
    assert d.number == "52a"
    assert d.title == "Đầu tư mở rộng trạm dừng nghỉ đã ký hợp đồng kinh doanh, khai thác"
    assert "[^73]" in d.text and "73" in d.footnotes
    assert [x.number for x in res.units if x.level == "dieu"] == ["52", "52a", "53"]
    assert "dieu_first_not_1" in _kinds(res)


def test_vbhn55_khoan_18a_and_footnotes() -> None:
    text = "Chương I\nQUY ĐỊNH CHUNG\n" + _fx("vbhn55_dieu9.txt")
    res = parse_structure("VBHN55-VPQH", text)
    u = _by_id(res.units)
    k18, k18a = u["VBHN55-VPQH/D9/K18"], u["VBHN55-VPQH/D9/K18a"]
    assert k18.number == "18" and k18a.number == "18a"
    assert k18.text.startswith("18.[^6] Làm gián đoạn")
    assert k18.footnotes["6"].startswith("Khoản này được sửa đổi, bổ sung")
    assert set(k18a.footnotes) == {"7"}
    assert "[^6] Khoản này" not in k18.text  # dòng chú thích không lọt vào text
    assert all("\n[^" not in x.text and not x.text.startswith("[^") for x in res.units)
    nums = [x.number for x in res.units if x.parent_id == "VBHN55-VPQH/D9"]
    assert nums[16:20] == ["17", "18", "18a", "19"]
    assert u["VBHN55-VPQH/C2"].title is not None
    assert u["VBHN55-VPQH/D9"].parent_id == "VBHN55-VPQH/C1"
    assert res.report.n_footnotes >= 2 and not res.report.orphan_footnotes


# ---------------------------------------------------------------- khung Phần/Chương/Mục


def test_tt35_phan_chuong_nested() -> None:
    res = parse_structure("TT35-2024-BGTVT", _fx("tt35_phan_chuong.txt"))
    u = _by_id(res.units)
    frames = [(x.id, x.parent_id, x.title) for x in res.units if x.level in ("phan", "chuong")]
    assert frames == [
        ("TT35-2024-BGTVT/P1", "TT35-2024-BGTVT", "QUY ĐỊNH CHUNG"),
        (
            "TT35-2024-BGTVT/P2",
            "TT35-2024-BGTVT",
            "ĐÀO TẠO, SÁT HẠCH, CẤP GIẤY PHÉP LÁI XE CƠ GIỚI ĐƯỜNG BỘ",
        ),
        ("TT35-2024-BGTVT/P2/C1", "TT35-2024-BGTVT/P2", "ĐÀO TẠO LÁI XE"),
        ("TT35-2024-BGTVT/P2/C2", "TT35-2024-BGTVT/P2", "SÁT HẠCH LÁI XE"),
        ("TT35-2024-BGTVT/P3", "TT35-2024-BGTVT", "CẤP, SỬ DỤNG GIẤY PHÉP LÁI XE QUỐC TẾ"),
        # Chương I lặp lại ở Phần III → mã khác nhờ chứa Phần.
        ("TT35-2024-BGTVT/P3/C1", "TT35-2024-BGTVT/P3", "CẤP GIẤY PHÉP LÁI XE QUỐC TẾ"),
    ]
    assert u["TT35-2024-BGTVT/D1"].parent_id == "TT35-2024-BGTVT/P1"
    assert u["TT35-2024-BGTVT/P1"].text == "Phần I\nQUY ĐỊNH CHUNG"
    # Trích đoạn bỏ Điều 3–4: Điều 5 sai thứ tự → không tạo unit, có anomaly.
    assert "TT35-2024-BGTVT/D5" not in u and "dieu_out_of_sequence" in _kinds(res)
    # Phần mở đầu thuộc unit văn bản.
    assert u["TT35-2024-BGTVT"].level == "van_ban"
    assert u["TT35-2024-BGTVT"].text.startswith("Căn cứ Nghị định số 56/2022")


def test_dieu_parent_is_deepest_frame() -> None:
    text = (
        "Chương I\nQUY ĐỊNH CHUNG\nĐiều 1. A\nChương II\nXỬ PHẠT\nMục 1. VI PHẠM QUY TẮC\n"
        "Điều 2. B\n1. Khoản một.\nMục 2\nVI PHẠM KHÁC\nĐiều 3. C\nChương III. THI HÀNH\nĐiều 4. D"
    )
    u = _by_id(parse_structure("ND168-2024", text).units)
    assert u["ND168-2024/D1"].parent_id == "ND168-2024/C1"
    assert u["ND168-2024/D2"].parent_id == "ND168-2024/C2/M1"
    assert u["ND168-2024/C2/M1"].title == "VI PHẠM QUY TẮC"
    assert u["ND168-2024/C2/M2"].title == "VI PHẠM KHÁC"
    assert u["ND168-2024/D3"].parent_id == "ND168-2024/C2/M2"
    assert u["ND168-2024/C3"].title == "THI HÀNH"
    assert u["ND168-2024/D4"].parent_id == "ND168-2024/C3"  # Mục đóng khi sang Chương mới


def test_nd165_multiline_chapter_title_not_phan() -> None:
    text = "Chương I\nQUY ĐỊNH CHUNG\nChương II\nPHÂN CẤP\n" + _fx("nd165_chuong3.txt")
    res = parse_structure("ND165-2024", text)
    u = _by_id(res.units)
    assert not [x for x in res.units if x.level == "phan"]  # "PHẦN ĐẤT…" không phải cấp Phần
    title = u["ND165-2024/C3"].title or ""
    assert title.startswith("PHẦN ĐẤT ĐỂ BẢO VỆ, BẢO TRÌ ĐƯỜNG BỘ; HÀNH LANG AN TOÀN ĐƯỜNG BỘ;")
    assert "PHẠM VI BẢO VỆ KẾT CẤU HẠ TẦNG ĐƯỜNG BỘ;" in title
    assert u["ND165-2024/D10"].parent_id == "ND165-2024/C3"


def test_frame_like_line_out_of_sequence_is_text() -> None:
    text = "Chương I\nCHUNG\nĐiều 1. A\n1. Danh mục:\nPhần II: Biểu mẫu kèm theo.\n2. Hai."
    res = parse_structure("ND151-2024", text)
    u = _by_id(res.units)
    assert "ND151-2024/P2" not in u
    assert "Phần II: Biểu mẫu kèm theo." in u["ND151-2024/D1/K1"].text
    assert u["ND151-2024/D1/K2"].parent_id == "ND151-2024/D1"


# ---------------------------------------------------------------- trích dẫn (văn bản sửa đổi)


def test_nd238_quoted_lines_do_not_create_units() -> None:
    res = parse_structure("ND238-2026", _fx("nd238_dieu1_2.txt"))
    u = _by_id(res.units)
    assert [x.number for x in res.units if x.level == "dieu"] == ["1", "2", "3"]
    k1 = u["ND238-2026/D2/K1"]
    assert k1.text.split("\n")[0] == "1. Bổ sung khoản 1a vào trước khoản 1 như sau:"
    assert k1.text.split("\n")[1].startswith('"1a. Phạt cảnh cáo')
    k2 = u["ND238-2026/D2/K2"]
    assert '"m) Chở trẻ em dưới 10 tuổi' in k2.text
    # Không có Khoản 1a hay Điểm m giả từ nội dung trích dẫn.
    assert "ND238-2026/D2/K1a" not in u and "ND238-2026/D2/K2/m" not in u
    assert not [x for x in res.units if x.level == "diem"]
    assert res.report.n_quote_blocks >= 3 and res.report.unclosed_quote_line is None


def test_nd218_multiline_quote_block() -> None:
    res = parse_structure("ND218-2026", _fx("nd218_trich.txt"))
    u = _by_id(res.units)
    assert [x.number for x in res.units if x.level == "dieu"] == ["1", "2", "3"]
    k3 = u["ND218-2026/D2/K3"]
    # “6. … mở khối; các dòng a)…đ) (không tự mở ngoặc) vẫn thuộc khối trích dẫn.
    lines = k3.text.split("\n")
    assert lines[1].startswith("“6. Ủy ban nhân dân cấp tỉnh")
    assert [ln[:2] for ln in lines[2:]] == ["a)", "b)", "c)", "d)", "đ)"]
    assert not [x for x in res.units if x.level == "diem"]
    assert res.report.n_quoted_lines == 9 and res.report.n_quote_blocks == 4


@pytest.mark.parametrize(
    ("line", "depth", "opener"),
    [
        ("“a) Tăng cường phương tiện;”.", 0, None),
        ('"1a. Phạt cảnh cáo đối với người điều khiển xe."', 0, None),
        ("“6. Ủy ban nhân dân cấp tỉnh", 1, "“"),
        ('c) đi ngược chiều đường có biển “Cấm đi ngược chiều";', 0, None),  # ND168: lẫn ngoặc
        ('"c) Thanh tra hàng hải Việt Nam;”.', 0, None),  # ND184: lẫn ngoặc
        ("biển cảnh báo “Chú ý xe đỗ” theo quy định", 0, None),
        ("1. Bổ sung khoản 1a như sau: “1a. Phạt", 1, "“"),
    ],
)
def test_quote_scan(line: str, depth: int, opener: str | None) -> None:
    assert quote_scan(line) == (depth, opener)


def test_inner_quoted_term_does_not_close_block() -> None:
    text = (
        "Điều 1. Sửa đổi\n1. Sửa đổi khoản 2 như sau:\n“2. Người lái xe phải:\n"
        "a) Đặt biển “Chú ý xe đỗ”;\nb) Bật đèn.”.\n2. Hai."
    )
    res = parse_structure("ND238-2026", text)
    u = _by_id(res.units)
    assert "ND238-2026/D1/K1/a" not in u
    assert u["ND238-2026/D1/K2"].text == "2. Hai."
    assert res.report.n_quoted_lines == 3


def test_unclosed_quote_force_closed_at_noi_nhan() -> None:
    text = "Điều 1. A\n1. Sửa như sau:\n“1a. Không đóng ngoặc\nĐiều 2. B\nNơi nhận: - Như trên;"
    res = parse_structure("ND238-2026", text)
    assert "unclosed_quote" in _kinds(res)
    assert res.report.body_end_reason == "noi_nhan"


def test_quote_in_preamble_is_ignored() -> None:
    # VBHN65: chú thích PDF tràn trang (“Căn cứ … không đóng) nằm trước Chương I.
    text = "Căn cứ Luật X;\n“Căn cứ Luật Y;\nChương I\nQUY ĐỊNH CHUNG\nĐiều 1. Phạm vi\n1. Một."
    u = _by_id(parse_structure("VBHN65-2026-BXD", text).units)
    assert u["VBHN65-2026-BXD/D1"].parent_id == "VBHN65-2026-BXD/C1"
    assert "VBHN65-2026-BXD/D1/K1" in u


# ---------------------------------------------------------------- thứ tự, nhảy số


def test_gap_of_one_is_accepted_with_anomaly() -> None:
    # TT12 Điều 3: bản gốc nhảy 3 → 5; TT79 Điều 34: n → p.
    text = "Điều 1. A\n1. Một.\n2. Hai.\n3. Ba.\n5. Năm.\n6. Sáu:\na) A;\nb) B;\nd) D;\nđ) Đ."
    res = parse_structure("TT12-2025-BCA", text)
    u = _by_id(res.units)
    assert "TT12-2025-BCA/D1/K5" in u and "TT12-2025-BCA/D1/K6/d" in u
    assert _kinds(res) == ["khoan_gap", "diem_gap"]


def test_diem_alphabet_has_dd_between_d_and_e() -> None:
    # Sau "d)" là "đ)"; "e)" ngay sau "d)" là thiếu một mục (gap), "f)" không phải ký hiệu Điểm.
    text = "Điều 1. A\n1. Một:\na) A;\nb) B;\nc) C;\nd) D;\ne) E;\nf) F."
    res = parse_structure("TT12-2025-BCA", text)
    u = _by_id(res.units)
    assert "TT12-2025-BCA/D1/K1/e" in u and "TT12-2025-BCA/D1/K1/f" not in u
    assert _kinds(res) == ["diem_gap"]


def test_duplicate_or_far_jump_is_rejected() -> None:
    # ND168 Điều 16: bản gốc ghi "đ)" hai lần; ND241: "11." sau khoản 8 (trích dẫn thiếu ngoặc).
    text = "Điều 1. A\n1. Một:\na) A;\nb) B;\nc) C;\nđ) Đ1;\nđ) Đ2.\n2. Hai.\n5. Năm."
    res = parse_structure("ND168-2024", text)
    u = _by_id(res.units)
    assert u["ND168-2024/D1/K1/đ"].text == "đ) Đ1;\nđ) Đ2."
    assert "ND168-2024/D1/K5" not in u
    assert "5. Năm." in u["ND168-2024/D1/K2"].text
    assert _kinds(res) == ["diem_gap", "diem_out_of_sequence", "khoan_out_of_sequence"]


def test_supplemented_khoan_before_base() -> None:
    text = "Điều 1. A\n1a. Bổ sung.\n1. Một.\n2. Hai."
    res = parse_structure("ND238-2026", text)
    assert [x.number for x in res.units if x.level == "khoan"] == ["1a", "1", "2"]
    assert not res.report.anomalies


def test_number_with_thousand_separator_is_not_khoan() -> None:
    text = "Điều 1. A\n1. Mức phạt:\n2.000.000 đồng đối với cá nhân."
    u = _by_id(parse_structure("ND168-2024", text).units)
    assert "2.000.000 đồng" in u["ND168-2024/D1/K1"].text


# ---------------------------------------------------------------- điểm dừng + phụ lục


def test_tt79_end_at_noi_nhan_and_appendices() -> None:
    res = parse_structure("TT79-2024-BCA", _fx("tt79_cuoi.txt"))
    u = _by_id(res.units)
    assert [x.number for x in res.units if x.level == "dieu"] == ["40"]
    assert res.report.body_end_reason == "noi_nhan"
    pls = [x for x in res.units if x.level == "phu_luc"]
    assert [p.id for p in pls] == ["TT79-2024-BCA/PL1", "TT79-2024-BCA/PL2"]
    assert pls[0].text.startswith("PHỤ LỤC 01") and pls[1].text.startswith("PHỤ LỤC SỐ 02")
    assert pls[0].title is not None and pls[0].parent_id == "TT79-2024-BCA"
    # "Điều 1./2./3." trong mẫu Quyết định (sau Nơi nhận) không thành Điều, bị bỏ.
    assert res.report.n_dropped_lines > 10
    assert "Điều 1." not in u["TT79-2024-BCA/D40"].text


def test_law_ends_at_passing_statement_and_signature() -> None:
    text = (
        "Điều 1. Hiệu lực\n1. Luật này có hiệu lực từ ngày 01 tháng 01 năm 2025.\n"
        "Luật này được Quốc hội nước Cộng hòa xã hội chủ nghĩa Việt Nam khóa XV thông qua.\n"
        "CHỦ TỊCH QUỐC HỘI\nTrần Thanh Mẫn"
    )
    res = parse_structure("LUAT36-2024", text)
    assert res.report.body_end_reason == "thong_qua" and res.report.n_dropped_lines == 3
    assert _by_id(res.units)["LUAT36-2024/D1/K1"].text.endswith("năm 2025.")


def test_decree_ends_at_signature_block() -> None:
    text = (
        "Điều 55. Trách nhiệm thi hành\nCác Bộ trưởng chịu trách nhiệm thi hành.\n"
        "TM. CHÍNH PHỦ\nKT. THỦ TƯỚNG"
    )
    res = parse_structure("ND168-2024", text)
    assert res.report.body_end_reason == "chu_ky"
    assert _by_id(res.units)["ND168-2024/D55"].text.endswith("thi hành.")


def test_noi_nhan_in_table_row_ends_body() -> None:
    text = "Điều 1. A\n1. Một.\nNơi nhận: | TM. CHÍNH PHỦ\n- Lưu: VT. | Trần Hồng Hà"
    res = parse_structure("ND238-2026", text)
    assert res.report.body_end_reason == "noi_nhan" and res.report.n_dropped_lines == 2


def test_appendix_unnumbered_and_duplicates() -> None:
    text = (
        "Điều 1. A\nNơi nhận: - Như trên;\nPHỤ LỤC\nVỀ VIỆC TÍNH TỔNG KHỐI LƯỢNG\nnội dung\n"
        "PHỤ LỤC\nMẪU TỜ KHAI\nPHỤ LỤC II[^5]\nMẪU KHÁC\nPhụ lục II\nLẶP SỐ\nPHỤ LỤC, BIỂU MẪU"
    )
    res = parse_structure("ND184-2025", text)
    pls = [x for x in res.units if x.level == "phu_luc"]
    assert [p.id for p in pls] == [
        "ND184-2025/PL1",
        "ND184-2025/PL2",
        "ND184-2025/PL2-2",
        "ND184-2025/PL2-3",
    ]
    assert pls[0].title == "VỀ VIỆC TÍNH TỔNG KHỐI LƯỢNG"
    assert pls[3].text.endswith("PHỤ LỤC, BIỂU MẪU")  # có dấu phẩy → không phải tiêu đề
    assert _kinds(res).count("phu_luc_unnumbered") == 2
    assert _kinds(res).count("phu_luc_duplicate") == 2
    assert "5" in res.report.missing_footnotes


def test_appendix_title_line_in_body_is_not_appendix() -> None:
    # TT79: "Chương III" có tên "PHỤ LỤC, BIỂU MẪU, …" nằm trong thân văn bản.
    text = (
        "Chương I\nA\nĐiều 1. A\nChương II\nB\nĐiều 2. B\nChương III\n"
        "PHỤ LỤC, BIỂU MẪU, THỜI HẠN SỬ DỤNG CHỨNG NHẬN ĐĂNG KÝ XE\nĐiều 3. Phụ lục và biểu mẫu"
    )
    res = parse_structure("TT79-2024-BCA", text)
    u = _by_id(res.units)
    assert (
        u["TT79-2024-BCA/C3"].title == "PHỤ LỤC, BIỂU MẪU, THỜI HẠN SỬ DỤNG CHỨNG NHẬN ĐĂNG KÝ XE"
    )
    assert u["TT79-2024-BCA/D3"].parent_id == "TT79-2024-BCA/C3"
    assert res.report.body_end_line is None


# ---------------------------------------------------------------- report


def test_report_counts_and_footnote_bookkeeping() -> None:
    text = (
        "Điều 1. A[^1]\n[^1] Điều này được sửa đổi.\n1. Một.\n2. Hai[^3].\n"
        "[^2] Chú thích không ai tham chiếu.\nĐiều 2. B"
    )
    res = parse_structure("VBHN55-VPQH", text)
    r = res.report
    assert r.counts == {"van_ban": 1, "dieu": 2, "khoan": 2}
    assert r.dieu_numbers == ["1", "2"] and r.last_dieu == "2" and r.dieu_missing == []
    assert r.n_footnotes == 2 and r.orphan_footnotes == ["2"] and r.missing_footnotes == ["3"]
    u = _by_id(res.units)
    assert u["VBHN55-VPQH/D1"].title == "A" and u["VBHN55-VPQH/D1"].footnotes == {
        "1": "Điều này được sửa đổi."
    }
