"""M4: đọc cụm dẫn chiếu tiếng Việt (câu lấy nguyên văn từ văn bản sửa đổi)."""

from __future__ import annotations

import pytest

from trafficlaw.ingest.refs import (
    SELF,
    Ref,
    RefContext,
    RefError,
    common_context,
    header_context,
    parse_refs,
)


def _ids(text: str, ctx: RefContext | None = None, doc: str = "ND168-2024") -> list[str]:
    return [r.unit_id(doc) for r in parse_refs(text, ctx)]


def test_points_distribute_to_following_khoan_and_dieu() -> None:
    # ND238 Đ19 K17
    assert _ids("điểm d, điểm đ, điểm e, điểm g khoản 17 Điều 32") == [
        "ND168-2024/D32/K17/d",
        "ND168-2024/D32/K17/đ",
        "ND168-2024/D32/K17/e",
        "ND168-2024/D32/K17/g",
    ]


def test_first_khoan_after_points_contains_them_rest_are_items() -> None:
    # ND218 Đ38 K1 (trích): "khoản 1, điểm b và điểm c khoản 2, …, khoản 5, điểm c khoản 8, Điều 22"
    got = _ids("khoản 1, điểm b và điểm c khoản 2, khoản 5, điểm c khoản 8, Điều 22")
    assert got == [
        "ND168-2024/D22/K1",
        "ND168-2024/D22/K2/b",
        "ND168-2024/D22/K2/c",
        "ND168-2024/D22/K5",
        "ND168-2024/D22/K8/c",
    ]


def test_number_lists_and_semicolon_groups() -> None:
    # ND236 Đ16 K4
    assert _ids(
        "khoản 7 Điều 11, khoản 3 Điều 12, khoản 4 Điều 17, Điều 18, khoản 1, 3 và 6 Điều 25"
    ) == [
        "ND168-2024/D11/K7",
        "ND168-2024/D12/K3",
        "ND168-2024/D17/K4",
        "ND168-2024/D18",
        "ND168-2024/D25/K1",
        "ND168-2024/D25/K3",
        "ND168-2024/D25/K6",
    ]
    # ND241 Đ25 K1 (trích): Điều đứng sau áp cho các mục trong cùng nhóm ";"
    assert _ids("khoản 1 và khoản 3 Điều 6; khoản 1 Điều 9; điểm a khoản 1 và khoản 3 Điều 20") == [
        "ND168-2024/D6/K1",
        "ND168-2024/D6/K3",
        "ND168-2024/D9/K1",
        "ND168-2024/D20/K1/a",
        "ND168-2024/D20/K3",
    ]


def test_context_fills_missing_dieu_khoan() -> None:
    ctx = RefContext(dieu="6")
    assert _ids("điểm m khoản 3", ctx) == ["ND168-2024/D6/K3/m"]
    assert _ids("khoản 1a", ctx) == ["ND168-2024/D6/K1a"]
    assert _ids("điểm i", RefContext(dieu="3", khoan="3")) == ["ND168-2024/D3/K3/i"]
    with pytest.raises(RefError):
        parse_refs("điểm m khoản 3")  # không có Điều


def test_title_part_can_cu_and_doc_mentions() -> None:
    refs = parse_refs("tên khoản 8 Điều 11")
    assert refs == [Ref(dieu="11", khoan="8", part="title")]
    assert parse_refs("phần căn cứ; điểm b khoản 3 Điều 4")[0].part == "can_cu"
    refs = parse_refs("khoản 1 và khoản 2 Điều 60 Nghị định số 165/2024/NĐ-CP")
    assert {r.doc for r in refs} == {"165/2024/NĐ-CP"}
    refs = parse_refs("điểm b khoản 6 Điều 8 Nghị định này")
    assert refs[0].doc == SELF


def test_appendix_and_mau() -> None:
    refs = parse_refs("Phụ lục III, Mẫu số 02 và Mẫu số 04 Phụ lục VII")
    assert refs[0] == Ref(appendix="3")
    assert [(r.appendix, r.mau) for r in refs[1:]] == [("7", "02"), ("7", "04")]
    assert refs[0].unit_id("ND158-2024") == "ND158-2024/PL3"
    with pytest.raises(RefError):
        refs[1].unit_id("ND158-2024")  # Mẫu không có unit riêng


def test_unreadable_text_raises() -> None:
    with pytest.raises(RefError):
        parse_refs("đoạn thứ hai điểm a khoản 3")  # ND238 Đ17 K2
    with pytest.raises(RefError):
        parse_refs("một số điểm, khoản của Điều 33")


def test_header_and_common_context() -> None:
    assert header_context("Sửa đổi, bổ sung một số điểm, khoản của Điều 6") == RefContext("6", None)
    assert header_context("Sửa đổi, bổ sung một số điểm của khoản 3 Điều 3") == RefContext("3", "3")
    assert header_context(
        "Sửa đổi, bổ sung một số điểm của khoản 5", RefContext("20")
    ) == RefContext("20", "5")
    # Số hiệu văn bản trong tiêu đề không phải dẫn chiếu Điều
    title = "Sửa đổi, bổ sung một số điều của Nghị định số 151/2024/NĐ-CP ngày 15 tháng 11 năm 2024"
    assert header_context(title) == RefContext()
    refs = parse_refs("điểm a, điểm c và điểm e khoản 1", RefContext("17"))
    assert common_context(refs) == RefContext("17", "1")
