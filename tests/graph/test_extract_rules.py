"""M8: regex con số + mệnh đề dẫn chiếu trên trích đoạn thật (ND168, ND336, LUAT36)."""

from __future__ import annotations

from trafficlaw.graph.extract import (
    find_clauses,
    find_definition,
    find_points,
    find_remedies,
    find_sanctions,
    find_verbatim,
    norm_name,
    numbers_in,
    numbers_ok,
    slugify,
    verify_numeric_entity,
)

# ND168 Điều 6 (nguyên văn data/graph)
ND168_D6_K1 = (
    "1. Phạt tiền từ 400.000 đồng đến 600.000 đồng đối với người điều khiển xe thực hiện một "
    "trong các hành vi vi phạm sau đây:"
)
ND168_D6_K14 = (
    "14. Tịch thu phương tiện đối với người điều khiển xe tái phạm hành vi điều khiển xe lạng "
    "lách, đánh võng quy định tại khoản 12 Điều này."
)
ND168_D6_K15_B = (
    "b) Thực hiện hành vi quy định tại khoản 12 Điều này bị tước quyền sử dụng giấy phép lái xe "
    "từ 10 tháng đến 12 tháng;"
)
ND168_D6_K15_A = (
    "a) Thực hiện hành vi quy định tại điểm e khoản 5 Điều này còn bị tịch thu thiết bị phát tín "
    "hiệu ưu tiên lắp đặt, sử dụng trái quy định;"
)
ND168_D6_K16_B = (
    "b) Thực hiện hành vi quy định tại điểm h khoản 5; khoản 6; điểm b khoản 7; điểm b, điểm c, "
    "điểm d khoản 9 Điều này bị trừ điểm giấy phép lái xe 04 điểm;"
)
ND168_D21_K13_A = (
    "a) Thực hiện hành vi quy định tại điểm b, điểm c, điểm đ khoản 2; điểm a khoản 3; khoản 4; "
    "khoản 5; điểm c, điểm d, điểm đ khoản 6 Điều này bị trừ điểm giấy phép lái xe (khi điều "
    "khiển xe ô tô) 02 điểm;"
)
ND168_D26_K12 = (
    "12. Ngoài việc bị phạt tiền, cá nhân, tổ chức thực hiện hành vi vi phạm quy định tại điểm c "
    "khoản 2; điểm a, điểm b, điểm đ, điểm g khoản 4; điểm b, điểm c, điểm d, điểm đ, điểm e, "
    "điểm g khoản 7; điểm c khoản 8 Điều này còn bị áp dụng các hình thức xử phạt bổ sung tước "
    "quyền sử dụng phù hiệu từ 01 tháng đến 03 tháng (nếu có hoặc đã được cấp) đối với xe vi phạm."
)
ND168_D32_K18_D = (
    "đ) Thực hiện hành vi quy định tại khoản 5, khoản 6 Điều này trong trường hợp chở vượt trên "
    "50% số người quy định được phép chở của phương tiện còn bị tước quyền sử dụng phù hiệu từ 01 "
    "tháng đến 03 tháng (nếu có). Thực hiện hành vi quy định tại điểm a, điểm b khoản 11 Điều này "
    "còn bị tước quyền sử dụng giấy phép lái xe từ 01 tháng đến 03 tháng."
)
ND168_D32_K19_A = (
    "a) Thực hiện hành vi quy định tại điểm a khoản 1, điểm i khoản 7 Điều này buộc khôi phục lại "
    "nhãn hiệu, màu sơn ghi trong chứng nhận đăng ký xe theo quy định;"
)
LUAT36_D2_K10 = (
    "10. Người điều khiển giao thông đường bộ (sau đây gọi là người điều khiển giao thông) bao "
    "gồm: Cảnh sát giao thông và người được giao nhiệm vụ hướng dẫn giao thông trên đường bộ."
)
LUAT36_D2_K12 = (
    "12. Tai nạn giao thông đường bộ là va chạm liên quan đến người, phương tiện khi tham gia "
    "giao thông đường bộ, xảy ra ngoài ý muốn của người tham gia giao thông đường bộ."
)


def test_fine_range() -> None:
    (s,) = find_sanctions(ND168_D6_K1)
    assert (s.loai, s.min_vnd, s.max_vnd) == ("phat_tien", 400_000, 600_000)
    assert s.span == "Phạt tiền từ 400.000 đồng đến 600.000 đồng"
    assert ND168_D6_K1[s.start : s.end] == s.span


def test_warning_and_fine_together() -> None:
    t = "1. Phạt cảnh cáo hoặc phạt tiền từ 100.000 đồng đến 200.000 đồng đối với người đi bộ"
    assert [x.loai for x in find_sanctions(t)] == ["canh_cao", "phat_tien"]


def test_confiscation_stops_before_doi_voi() -> None:
    (s,) = find_sanctions(ND168_D6_K14)
    assert s.loai == "tich_thu" and s.doi_tuong == "phương tiện"
    (s2,) = find_sanctions(ND168_D6_K15_A)
    assert s2.doi_tuong == "thiết bị phát tín hiệu ưu tiên lắp đặt, sử dụng trái quy định"


def test_revocation_months() -> None:
    (s,) = find_sanctions(ND168_D6_K15_B)
    assert (s.loai, s.min_thang, s.max_thang, s.doi_tuong) == (
        "tuoc_quyen",
        10,
        12,
        "giấy phép lái xe",
    )
    (p,) = find_sanctions(ND168_D26_K12)
    assert (p.doi_tuong, p.min_thang, p.max_thang) == ("phù hiệu", 1, 3)


def test_points_plain_and_with_condition() -> None:
    (p,) = find_points(ND168_D6_K16_B)
    assert p.so_diem == 4 and p.dieu_kien is None
    (q,) = find_points(ND168_D21_K13_A)
    assert q.so_diem == 2 and q.dieu_kien == "khi điều khiển xe ô tô"


def test_points_ignores_generic_mentions() -> None:
    assert find_points("16. … còn bị trừ điểm giấy phép lái xe như sau:") == []
    assert find_points("a) trừ các hành vi vi phạm quy định tại điểm a khoản 2") == []


def test_remedy_and_bat_buoc() -> None:
    (r,) = find_remedies(ND168_D32_K19_A)
    assert r.name.startswith("buộc khôi phục lại nhãn hiệu, màu sơn")
    assert find_remedies("Người lái xe bắt buộc phải thắt dây đai an toàn;") == []


def test_clauses_split_two_sentences() -> None:
    cs = find_clauses(ND168_D32_K18_D)
    assert len(cs) == 2
    assert ND168_D32_K18_D[cs[0].refs_start :].startswith("khoản 5, khoản 6 Điều này")
    sanc = find_sanctions(ND168_D32_K18_D)
    assert [(s.doi_tuong, cs[0].start <= s.start < cs[0].end) for s in sanc] == [
        ("phù hiệu", True),
        ("giấy phép lái xe", False),
    ]


def test_clause_regex_not_triggered_by_exception() -> None:
    t = "a) Không chấp hành hiệu lệnh, trừ các hành vi vi phạm quy định tại điểm a khoản 2;"
    assert find_clauses(t) == []


def test_definition_with_alias() -> None:
    d = find_definition(LUAT36_D2_K10)
    assert d is not None
    assert d.term == "Người điều khiển giao thông đường bộ"
    assert d.aliases == ("người điều khiển giao thông",)
    d2 = find_definition(LUAT36_D2_K12)
    assert d2 is not None and d2.term == "Tai nạn giao thông đường bộ" and d2.aliases == ()


def test_definition_trims_scope_suffix() -> None:
    t = "3. Mức tiêu chuẩn khí thải bằng “0” quy định tại Quyết định này là mức …"
    d = find_definition(t)
    assert d is not None and d.term == "Mức tiêu chuẩn khí thải bằng “0”"


def test_definition_rejects_non_definition() -> None:
    assert find_definition("1. Phạt tiền từ 400.000 đồng đến 600.000 đồng đối với …") is None


def test_numbers_and_verbatim() -> None:
    assert numbers_in("trừ 02 điểm, phạt 400.000 đồng") == {2, 400_000}
    assert numbers_ok("chạy quá tốc độ 10 km/h", "vượt quá từ 10 km/h đến 20 km/h")
    assert not numbers_ok("chạy quá tốc độ 30 km/h", "vượt quá từ 10 km/h đến 20 km/h")
    assert find_verbatim("lạng  lách,\nđánh võng", ND168_D6_K14) == "lạng lách, đánh võng"
    assert find_verbatim("chạy quá tốc độ đuổi nhau", ND168_D6_K14) is None


def test_verify_numeric_entity_against_regex() -> None:
    ok = {"type": "CheTai", "loai": "phat_tien", "min_vnd": 400_000, "max_vnd": 600_000}
    bad = {**ok, "max_vnd": 6_000_000}
    assert verify_numeric_entity(ok, ND168_D6_K1) is None
    assert verify_numeric_entity(bad, ND168_D6_K1) == "so_lech_regex"
    assert verify_numeric_entity({"type": "DiemGPLX", "so_diem": 4}, ND168_D6_K16_B) is None
    assert verify_numeric_entity({"type": "DiemGPLX", "so_diem": 6}, ND168_D6_K16_B) == (
        "so_lech_regex"
    )


def test_name_normalisation_keeps_vehicle_types_apart() -> None:
    """ "xe gắn máy" ≠ "xe mô tô": chuẩn hoá chỉ bỏ dấu câu/hoa-thường, không gộp đồng nghĩa."""
    assert norm_name("Xe gắn máy,") == "xe gắn máy"
    assert norm_name("xe gắn máy") != norm_name("xe mô tô")
    assert slugify("Xe gắn máy") == "xe-gan-may" != slugify("Xe mô tô")
    assert slugify("Đường bộ") == "duong-bo"


# ND168 Đ26 K5 (nguyên văn) — mức riêng cho tổ chức không lặp chữ "Phạt tiền".
ND168_D26_K5 = (
    "5. Phạt tiền từ 4.000.000 đồng đến 5.000.000 đồng đối với cá nhân, từ 8.000.000 đồng đến "
    "10.000.000 đồng đối với tổ chức xếp hàng hóa lên mỗi xe ô tô (kể cả rơ moóc và sơ mi rơ moóc) "
    "vượt quá trọng tải (khối lượng hàng chuyên chở) cho phép tham gia giao thông được ghi trong "
    "chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe trên 100%."
)
# ND168 Đ32 K19 e (rút gọn danh sách dẫn chiếu) — biện pháp khắc phục viết "phải khôi phục".
ND168_D32_K19_E = (
    "e) Thực hiện hành vi vi phạm quy định tại điểm đ, điểm e, điểm g khoản 7 Điều này nếu gây "
    "hư hại cầu, đường phải khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành "
    "chính gây ra;"
)


def test_fine_for_individual_and_organization() -> None:
    a, b = find_sanctions(ND168_D26_K5)
    assert (a.min_vnd, a.max_vnd, a.doi_tuong) == (4_000_000, 5_000_000, "cá nhân")
    assert (b.min_vnd, b.max_vnd, b.doi_tuong) == (8_000_000, 10_000_000, "tổ chức")
    assert b.span == "từ 8.000.000 đồng đến 10.000.000 đồng đối với tổ chức"
    assert ND168_D26_K5[b.start : b.end] == b.span and a.end <= b.start
    org = {"type": "CheTai", "loai": "phat_tien", "min_vnd": 8_000_000, "max_vnd": 10_000_000}
    assert verify_numeric_entity(org, ND168_D26_K5) is None  # nhãn vàng mức tổ chức khớp regex
    (only,) = find_sanctions(ND168_D6_K1)  # câu thường: một mức, không gán đối tượng
    assert only.doi_tuong is None


def test_remedy_phai_khoi_phuc() -> None:
    (r,) = find_remedies(ND168_D32_K19_E)
    assert (
        r.name
        == "phải khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra"
    )
