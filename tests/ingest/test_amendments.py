"""M4: nhận diện chỉ dẫn sửa đổi trên trích đoạn văn bản sửa đổi thật."""

from __future__ import annotations

from tests.ingest.m4_helpers import FIXTURES, registry, unit, units_of
from trafficlaw.ingest.amendments import (
    LabelFix,
    build_block,
    extract_instructions,
    split_by_labels,
    strip_quote_block,
)

REG = registry()


def _extract(doc_id: str, units, **kw):  # type: ignore[no-untyped-def]
    return extract_instructions(REG[doc_id], units, REG, **kw)


def test_strip_quote_block_keeps_inner_quotes() -> None:
    lines = [
        "“1. Nội dung kiểm tra, bao gồm:",
        "a) Kiểm tra theo biển “Cấm đi ngược chiều”;",
        "b) Kiểm tra kiến thức pháp luật (sau đây viết gọn là kiểm tra mô phỏng).”.",
    ]
    assert strip_quote_block(lines) == [
        "1. Nội dung kiểm tra, bao gồm:",
        "a) Kiểm tra theo biển “Cấm đi ngược chiều”;",
        "b) Kiểm tra kiến thức pháp luật (sau đây viết gọn là kiểm tra mô phỏng).",
    ]
    # ND241 Đ10 K8: khoản 11 thiếu ngoặc mở trong bản gốc, vẫn là nội dung
    assert strip_quote_block(["“10. A.”.", "11. B.”."]) == ["10. A.", "11. B."]
    # ASCII quote (ND238)
    assert strip_quote_block(['"i) Buộc lắp đặt;".']) == ["i) Buộc lắp đặt;"]


def test_split_and_build_block() -> None:
    lines = ["2. Lắp đặt:", "a) Xe ô tô;", "b) Xe mô tô.", "3. Quản lý:", "a) Chỉ được lắp."]
    parts = split_by_labels(lines, "khoan", ["2", "3"])
    assert parts is not None and [p[0][:2] for p in parts] == ["2.", "3."]
    blk = build_block("ND151-2024/D17/K2", "khoan", parts[0])
    assert blk.text == "2. Lắp đặt:"
    assert [c.id for c in blk.children] == ["ND151-2024/D17/K2/a", "ND151-2024/D17/K2/b"]
    assert split_by_labels(lines, "khoan", ["2", "4"]) is None


def test_nd238_header_context_and_insert_before() -> None:
    ex = _extract("ND238-2026", units_of("ND238-2026", "nd238_dieu1_2.txt"))
    by = {(i.source_unit_id, i.target_id): i for i in ex.instructions}
    # Đ1: "một số điểm của khoản 3 Điều 3" → câu con "Sửa đổi, bổ sung điểm i"
    assert ("ND238-2026/D1/K1", "ND168-2024/D3/K3/i") in by
    # Đ2 K1: "Bổ sung khoản 1a vào trước khoản 1" (Điều 6 lấy từ tiêu đề Điều)
    ins = by[("ND238-2026/D2/K1", "ND168-2024/D6/K1a")]
    assert ins.op == "insert" and ins.before_id == "ND168-2024/D6/K1"
    assert ins.block is not None and ins.block.text.startswith("1a. Phạt cảnh cáo")
    rep = by[("ND238-2026/D2/K2", "ND168-2024/D6/K3/m")]
    assert rep.op == "replace" and str(rep.effective_from) == "2026-08-15"
    # Đ3: chỉ dẫn nằm ở tiêu đề Điều, nội dung ngay dưới
    assert by[("ND238-2026/D3", "ND168-2024/D13/K8/b")].op == "replace"
    assert not ex.todos


def test_nd241_replace_whole_dieu() -> None:
    ex = _extract("ND241-2026", units_of("ND241-2026", "nd241_dieu1.txt"))
    [ins] = ex.instructions
    assert (ins.op, ins.target_id, ins.target_doc) == ("replace", "ND165-2024/D4", "ND165-2024")
    assert ins.block is not None
    assert ins.block.title == "Phân cấp để Ủy ban nhân dân cấp tỉnh quản lý quốc lộ"
    khoan = [c.id for c in ins.block.children]
    assert khoan == [f"ND165-2024/D4/K{n}" for n in range(1, 9)]
    k3 = ins.block.children[2]
    assert [c.number for c in k3.children] == ["a", "b", "c", "d", "đ"]
    # đoạn không nhãn sau khoản 5 thuộc khoản 5
    assert "bố trí vốn" in ins.block.children[4].text


def test_nd241_phrase_repeal_appendix_and_out_of_registry() -> None:
    ex = _extract("ND241-2026", units_of("ND241-2026", "nd241_dieu25_26.txt"))
    ops = [(i.op, i.target_id) for i in ex.instructions]
    assert ("replace_phrase", "ND165-2024/D6/K1") in ops
    assert ("replace_phrase", "ND165-2024/D69/K5/đ") in ops
    assert ("repeal", "ND165-2024/D17/K1/d") in ops
    assert ("replace_appendix", "ND165-2024/PL10") in ops
    k1 = next(i for i in ex.instructions if i.target_id == "ND165-2024/D6/K1")
    assert (k1.old, k1.new) == ("Bộ Giao thông vận tải", "Bộ Xây dựng")
    reasons = {(t.source_unit_id, t.reason) for t in ex.todos}
    assert ("ND241-2026/D25/K4/a", "mau_phu_luc") in reasons
    # Đ26 K2 bãi bỏ khoản của NĐ 140/2025 (ngoài danh mục)
    assert ("ND241-2026/D26/K2", "ngoai_danh_muc") in reasons


def test_nd218_repeal_list_mixed_items() -> None:
    lines = (FIXTURES / "nd218_dieu38_k8.txt").read_text(encoding="utf-8").splitlines()
    units = [
        unit("ND218-2026/D38", "dieu", lines[0], title=lines[0].split(". ", 1)[1]),
        unit("ND218-2026/D38/K8", "khoan", lines[1]),
    ]
    ex = _extract("ND218-2026", units)
    repeal = [i.target_id for i in ex.instructions if i.op == "repeal"]
    assert repeal[:3] == ["ND158-2024/D12/K8", "ND158-2024/D13/K2", "ND158-2024/D14/K2"]
    assert "ND158-2024/D68" in repeal and "ND158-2024/D73/K1/d" in repeal
    phrases = [(i.op, i.target_id, i.old) for i in ex.instructions if i.op == "remove_phrase"]
    assert ("remove_phrase", "ND158-2024/D17/K3", "Thanh tra đường bộ") in phrases
    assert ("remove_phrase", "ND158-2024/D67/K2", "Bộ Thông tin và Truyền thông") in phrases
    assert {t.reason for t in ex.todos} == {"mau_phu_luc"}  # các Mẫu trong Phụ lục


def test_dieu_amending_out_of_registry_document_is_skipped() -> None:
    ex = _extract("ND184-2025", units_of("ND184-2025", "nd184_dieu3.txt"))
    assert not ex.instructions
    assert [(t.source_unit_id, t.reason) for t in ex.todos] == [("ND184-2025/D3", "ngoai_danh_muc")]


def test_unclear_sentence_goes_to_todo() -> None:
    units = [
        unit(
            "ND238-2026/D17",
            "dieu",
            "Điều 17. Sửa đổi, bổ sung một số điểm, khoản của Điều 50",
            title="Sửa đổi, bổ sung một số điểm, khoản của Điều 50",
        ),
        unit(
            "ND238-2026/D17/K2",
            "khoan",
            "2. Sửa đổi, bổ sung đoạn thứ hai điểm a khoản 3 như sau:\n"
            '"Trường hợp Chủ tịch Ủy ban nhân dân cấp xã ra quyết định xử phạt;".',
        ),
    ]
    ex = _extract("ND238-2026", units)
    assert not ex.instructions
    assert [t.reason for t in ex.todos] == ["mau_khong_ro"]


def test_label_fix_applies_only_to_exact_line() -> None:
    units = [
        unit(
            "ND241-2026/D24",
            "dieu",
            "Điều 24. Sửa đổi, bổ sung một số khoản, điểm của Điều 64",
            title="Sửa đổi, bổ sung một số khoản, điểm của Điều 64",
        ),
        unit(
            "ND241-2026/D24/K1",
            "khoan",
            "1. Bổ sung các điểm đ, điểm e khoản 1 như sau:\n"
            "“d) An toàn giao thông và ứng cứu khẩn cấp;\ne) Quản lý bãi đỗ xe thông minh.”.",
        ),
    ]
    ex = _extract("ND241-2026", units)
    assert [t.reason for t in ex.todos] == ["nhan_khong_khop"]
    fix = LabelFix(
        source_unit_id="ND241-2026/D24/K1",
        label_in_source="d",
        label="đ",
        text_starts_with="An toàn giao thông",
        reason="r",
        evidence="e",
    )
    ex = _extract("ND241-2026", units, label_fixes=[fix])
    assert [i.target_id for i in ex.instructions] == ["ND165-2024/D64/K1/đ", "ND165-2024/D64/K1/e"]
    assert ex.instructions[0].block.text.startswith("đ) An toàn")  # type: ignore[union-attr]
    bad = fix.model_copy(update={"text_starts_with": "Không có dòng này"})
    assert _extract("ND241-2026", units, label_fixes=[bad]).fixes_unapplied == ["ND241-2026/D24/K1"]
