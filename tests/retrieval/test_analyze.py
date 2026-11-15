"""M11: analyzer rule (ngày, PT/CT theo danh mục M8, loại câu, gợi ý văn bản) + LLM dự phòng
(FakeClient: chỉ gọi khi rule không chắc, cache, tắt LLM, JSON lỗi)."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest

from trafficlaw.llm.client import LLMClient
from trafficlaw.llm.prompt_loader import load_prompt
from trafficlaw.llm.providers.fake import FakeClient, bad_json, ok, server_error
from trafficlaw.llm.retry import RetryPolicy
from trafficlaw.retrieval.analyze import (
    Analyzer,
    AnalyzerTables,
    LLMAnalysisStore,
    MissingLLMAnalysisError,
    analyze_rule,
    match_catalog,
    parse_question_dates,
)

from .conftest import TODAY

D = date


# --- ngày ------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("q", "want"),
    [
        ("Từ ngày 1/1/2026 vượt đèn đỏ bị phạt bao nhiêu?", [D(2026, 1, 1)]),
        ("Áp dụng tại 01/07/2026 thì sao?", [D(2026, 7, 1)]),
        ("Ngày 15-08-2026 quy định thế nào?", [D(2026, 8, 15)]),
        ("ngày 15 tháng 8 năm 2026 có gì thay đổi", [D(2026, 8, 15)]),
        ("Trong tháng 8/2026 mức phạt là bao nhiêu", [D(2026, 8, 1)]),
        ("tháng 7 năm 2026 áp dụng quy định nào", [D(2026, 7, 1)]),
        ("Trước ngày 01/01/2026 bị phạt thế nào?", [D(2025, 12, 31)]),
        ("trước 1/1/2026 thì sao", [D(2025, 12, 31)]),
        ("Sau ngày 31/12/2025 thì sao?", [D(2026, 1, 1)]),
        ("kể từ ngày 01/01/2026", [D(2026, 1, 1)]),
        ("Theo Nghị định 168/2024/NĐ-CP thì phạt bao nhiêu?", []),
    ],
)
def test_dates(q: str, want: list[date]) -> None:
    got, _ = parse_question_dates(q)
    assert got == want


def test_date_reasons() -> None:
    assert "thoi_gian_tuong_doi" in parse_question_dates("Năm ngoái phạt bao nhiêu?")[1]
    assert (
        "thoi_gian_tuong_doi"
        in parse_question_dates("Trước khi Nghị định 168 có hiệu lực thì phạt thế nào?")[1]
    )
    assert parse_question_dates("Năm 2026 phạt bao nhiêu?")[1] == ["chi_co_nam"]
    assert "nhieu_ngay" in parse_question_dates("So sánh 1/1/2025 và 1/1/2026")[1]
    assert parse_question_dates("ngày 31/02/2026")[1] == ["ngay_khong_hop_le"]


def test_param_date_wins(tables: AnalyzerTables) -> None:
    q = "Từ ngày 1/1/2026 vượt đèn đỏ bị phạt bao nhiêu?"
    a = analyze_rule(q, D(2025, 6, 1), tables, today=TODAY)
    assert (a.as_of, a.as_of_source) == (D(2025, 6, 1), "tham_so")
    assert a.question_dates == [D(2026, 1, 1)]
    b = analyze_rule(q, None, tables, today=TODAY)
    assert (b.as_of, b.as_of_source) == (D(2026, 1, 1), "cau_hoi")
    c = analyze_rule("Vượt đèn đỏ bị phạt bao nhiêu?", None, tables, today=TODAY)
    assert (c.as_of, c.as_of_source) == (TODAY, "mac_dinh")
    # Có ngày tham số → lý do không chắc về thời gian bị bỏ.
    r = analyze_rule("Năm ngoái phạt tiền bao nhiêu?", D(2026, 1, 1), tables, today=TODAY)
    assert "thoi_gian_tuong_doi" not in r.uncertain


# --- phương tiện / chủ thể ---------------------------------------------------------------------


def test_xe_gan_may_khac_xe_mo_to(tables: AnalyzerTables) -> None:
    pt, _, _ = match_catalog("Người điều khiển xe gắn máy vượt đèn đỏ", tables)
    assert pt == ["PT:xe-gan-may"]
    pt, _, _ = match_catalog("Điều khiển xe mô tô không đội mũ bảo hiểm", tables)
    assert pt == ["PT:xe-mo-to"]
    pt, _, _ = match_catalog("xe mô tô, xe gắn máy chở quá số người", tables)
    assert pt == ["PT:xe-mo-to", "PT:xe-gan-may"]


def test_longest_match_wins(tables: AnalyzerTables) -> None:
    pt, _, _ = match_catalog("Điều khiển xe tương tự xe mô tô không có đèn", tables)
    assert pt == ["PT:xe-tuong-tu-xe-mo-to"]
    pt, _, _ = match_catalog("xe ô tô tải chở quá tải", tables)
    assert pt == ["PT:xe-o-to-tai"]


def test_subject_alias(tables: AnalyzerTables) -> None:
    _, ct, _ = match_catalog("Người điều khiển xe phải mang theo giấy tờ gì?", tables)
    assert ct == ["CT:nguoi-dieu-khien-phuong-tien-tham-gia-giao-thong-duong-bo"]


def test_unknown_vehicle_is_uncertain(tables: AnalyzerTables) -> None:
    a = analyze_rule(
        "Đi xe máy không đội mũ bảo hiểm bị phạt bao nhiêu?", None, tables, today=TODAY
    )
    assert a.vehicle_ids == []
    assert "phuong_tien_ngoai_danh_muc" in a.uncertain
    b = analyze_rule(
        "Xe gắn máy không đội mũ bảo hiểm bị phạt bao nhiêu?", None, tables, today=TODAY
    )
    assert "phuong_tien_ngoai_danh_muc" not in b.uncertain
    # "giấy phép lái xe" không phải từ chỉ loại xe.
    c = analyze_rule("Bị trừ bao nhiêu điểm giấy phép lái xe?", None, tables, today=TODAY)
    assert "phuong_tien_ngoai_danh_muc" not in c.uncertain


# --- loại câu, văn bản -----------------------------------------------------------------------


@pytest.mark.parametrize(
    ("q", "want"),
    [
        ("Xe ô tô vượt đèn đỏ bị phạt bao nhiêu tiền?", "muc_phat"),
        ("Vượt đèn đỏ bị trừ bao nhiêu điểm giấy phép lái xe?", "tru_diem"),
        ("Khi nào bị tước giấy phép lái xe?", "bien_phap"),
        ("Xe cơ giới là gì?", "dinh_nghia"),
        ("Hồ sơ cấp đổi giấy phép lái xe gồm những gì?", "thu_tuc_tham_quyen"),
        ("Người đi bộ có được đi vào đường cao tốc không?", "hanh_vi_cam_nghia_vu"),
    ],
)
def test_question_type(tables: AnalyzerTables, q: str, want: str) -> None:
    assert analyze_rule(q, None, tables, today=TODAY).question_type == want


def test_type_modifiers_and_groups(tables: AnalyzerTables) -> None:
    a = analyze_rule(
        "Từ ngày 1/1/2026 mức phạt vượt đèn đỏ là bao nhiêu?", None, tables, today=TODAY
    )
    assert a.question_type == "muc_phat" and "theo_thoi_diem" in a.modifiers
    # Mức phạt + trừ điểm cùng nhóm cạnh → không mơ hồ.
    b = analyze_rule("Vượt đèn đỏ bị phạt tiền và trừ điểm thế nào?", None, tables, today=TODAY)
    assert "loai_cau_mo_ho" not in b.uncertain
    c = analyze_rule("Đường cao tốc có bao nhiêu làn?", None, tables, today=TODAY)
    assert c.question_type is None and "khong_ro_loai_cau" in c.uncertain


def test_doc_hints(tables: AnalyzerTables) -> None:
    a = analyze_rule("Theo Nghị định 168/2024/NĐ-CP thì phạt bao nhiêu?", None, tables, today=TODAY)
    assert a.doc_hints == ["ND168-2024"]
    b = analyze_rule("Theo NĐ 168 thì phạt bao nhiêu?", None, tables, today=TODAY)
    assert b.doc_hints == ["ND168-2024"]
    c = analyze_rule(
        "Luật Trật tự, an toàn giao thông đường bộ quy định gì?", None, tables, today=TODAY
    )
    assert c.doc_hints == ["LUAT36-2024"]


# --- LLM dự phòng ----------------------------------------------------------------------------


def _client(steps) -> tuple[LLMClient, FakeClient]:
    fake = FakeClient(steps, model_id="qwen3-14b-awq")
    return LLMClient(fake, retry=RetryPolicy(max_retries=0, sleep=lambda s: None)), fake


def _analyzer(tables: AnalyzerTables, tmp: Path, llm, *, strict: bool = False) -> Analyzer:
    a = Analyzer(
        tables,
        today=TODAY,
        llm=llm,
        store=LLMAnalysisStore(tmp / "llm.jsonl"),
        prompt=load_prompt("analyze_question"),
        strict=strict,
    )
    a.set_model_id("qwen3-14b-awq")
    return a


OUT = {
    "as_of": "2025-11-15",
    "vehicle_ids": ["PT:xe-mo-to", "PT:xe-gan-may", "PT:khong-co"],
    "subject_ids": [],
    "question_type": "muc_phat",
    "doc_hints": ["ND168-2024", "XYZ"],
}


def test_llm_only_when_uncertain(tables: AnalyzerTables, tmp_path: Path) -> None:
    llm, fake = _client([ok(json.dumps(OUT))])
    a = _analyzer(tables, tmp_path, llm)
    sure = a.analyze("Xe gắn máy vượt đèn đỏ bị phạt bao nhiêu tiền?", D(2026, 1, 1))
    assert fake.n_calls == 0 and sure.analyzer == "rule" and sure.llm_status is None
    r = a.analyze("Năm ngoái đi xe máy vượt đèn đỏ bị phạt bao nhiêu?", None)
    assert fake.n_calls == 1
    assert r.analyzer == "llm" and r.llm_status == "ok"
    assert set(r.llm_reason) >= {"thoi_gian_tuong_doi", "phuong_tien_ngoai_danh_muc"}
    assert r.as_of == D(2025, 11, 15) and r.as_of_source == "cau_hoi"
    assert r.vehicle_ids == ["PT:xe-mo-to", "PT:xe-gan-may"]  # id lạ bị bỏ
    assert r.doc_hints == ["ND168-2024"]
    assert r.prompt_hash == load_prompt("analyze_question").hash


def test_llm_param_date_still_wins(tables: AnalyzerTables, tmp_path: Path) -> None:
    llm, _ = _client([ok(json.dumps(OUT))])
    r = _analyzer(tables, tmp_path, llm).analyze("Đi xe máy bị phạt bao nhiêu?", D(2026, 7, 1))
    assert r.analyzer == "llm" and r.as_of == D(2026, 7, 1) and r.as_of_source == "tham_so"


def test_llm_cache_and_offline(tables: AnalyzerTables, tmp_path: Path) -> None:
    q = "Đi xe máy bị phạt bao nhiêu?"
    llm, fake = _client([ok(json.dumps(OUT))])
    first = _analyzer(tables, tmp_path, llm).analyze(q, D(2026, 7, 1))
    # Lần sau (pha 2, không có server): đọc kết quả đã lưu, không gọi.
    off = _analyzer(tables, tmp_path, None, strict=True).analyze(q, D(2026, 7, 1))
    assert fake.n_calls == 1
    assert off.vehicle_ids == first.vehicle_ids and off.llm_cached is True
    with pytest.raises(MissingLLMAnalysisError):
        _analyzer(tables, tmp_path, None, strict=True).analyze("Đi xe máy kéo theo xe khác?", None)
    lax = _analyzer(tables, tmp_path, None).analyze("Đi xe máy kéo theo xe khác?", None)
    assert lax.llm_status == "missing" and lax.analyzer == "rule"


def test_no_llm_flag(tables: AnalyzerTables, tmp_path: Path) -> None:
    llm, fake = _client([ok(json.dumps(OUT))])
    r = _analyzer(tables, tmp_path, llm).analyze("Đi xe máy bị phạt?", None, use_llm=False)
    assert fake.n_calls == 0 and r.analyzer == "rule" and r.llm_status == "disabled"


def test_llm_format_error_keeps_rule(tables: AnalyzerTables, tmp_path: Path) -> None:
    llm, fake = _client([bad_json(), bad_json()])
    a = _analyzer(tables, tmp_path, llm)
    r = a.analyze("Đi xe máy bị phạt bao nhiêu?", None)
    assert r.llm_status == "format_error" and r.analyzer == "rule" and r.vehicle_ids == []
    assert fake.n_calls == 2  # lần đầu + 1 lần sửa định dạng
    # format_error được lưu (tất định) → không gọi lại.
    a.analyze("Đi xe máy bị phạt bao nhiêu?", None)
    assert fake.n_calls == 2


def test_llm_error_not_cached(tables: AnalyzerTables, tmp_path: Path) -> None:
    llm, fake = _client([server_error(), ok(json.dumps(OUT))])
    a = _analyzer(tables, tmp_path, llm)
    r = a.analyze("Đi xe máy bị phạt bao nhiêu?", None)
    assert r.llm_status == "error" and r.analyzer == "rule"
    r2 = a.analyze("Đi xe máy bị phạt bao nhiêu?", None)
    assert r2.llm_status == "ok" and fake.n_calls == 2
