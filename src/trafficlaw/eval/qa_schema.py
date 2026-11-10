"""M9: schema bộ dữ liệu hỏi–đáp, dùng chung cho test (viết tay), train/val (sinh tự động).

Một dòng JSONL = một ``QAItem``. ``split`` không lưu trong bản ghi — suy từ tên file
(``test.jsonl`` / ``train.jsonl`` / ``val.jsonl``).

Tập test do người dùng viết tay (CLAUDE.md mục 10, 16): công cụ chỉ đọc + kiểm tra, không sửa.
"""

from __future__ import annotations

import unicodedata
from datetime import date
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

Split = Literal["test", "train", "val"]
SPLITS: tuple[Split, ...] = ("test", "train", "val")

Tier = Literal["A", "B", "C", "historical"]
TIERS: tuple[str, ...] = ("A", "B", "C", "historical")

QuestionType = Literal[
    "muc_phat",
    "tru_diem",
    "bien_phap",
    "hanh_vi_cam_nghia_vu",
    "dinh_nghia",
    "thu_tuc_tham_quyen",
    "theo_thoi_diem",
    "da_buoc",
    "so_sanh",
    "ngoai_pham_vi",
    "khac",
]
QUESTION_TYPES: tuple[str, ...] = QuestionType.__args__  # type: ignore[attr-defined]

#: Mô tả ngắn từng loại (in ra phiếu viết, prompt sinh dữ liệu). ``khac`` chỉ dùng cho train/val.
QUESTION_TYPE_DOC: dict[str, str] = {
    "muc_phat": "mức phạt tiền / phạt cảnh cáo cho một hành vi",
    "tru_diem": "số điểm bị trừ trên giấy phép lái xe",
    "bien_phap": "tước quyền sử dụng giấy phép, tịch thu, biện pháp khắc phục hậu quả",
    "hanh_vi_cam_nghia_vu": "hành vi bị cấm / nghĩa vụ, quy tắc phải tuân thủ",
    "dinh_nghia": "khái niệm, thuật ngữ được giải thích",
    "thu_tuc_tham_quyen": "thủ tục, hồ sơ, điều kiện, thẩm quyền, cơ quan có trách nhiệm",
    "theo_thoi_diem": "câu trả lời khác nhau trước/sau một mốc sửa đổi (đi theo cặp)",
    "da_buoc": "cần ≥ 2 điều khoản nối bằng dẫn chiếu / chế tài",
    "so_sanh": "so sánh giữa loại xe hoặc chủ thể",
    "ngoai_pham_vi": "ngoài phạm vi dữ liệu — hệ thống phải từ chối",
    "khac": "loại khác (chỉ dùng cho câu sinh tự động)",
}

NumberUnit = Literal[
    "vnd", "diem", "thang", "ngay", "nam", "gio", "km_h", "km", "m", "tan", "cho", "phan_tram",
    "mg", "khac",
]  # fmt: skip


class RequiredNumber(BaseModel):
    """Con số pháp lý mà câu trả lời đúng phải nêu (mức phạt, điểm trừ, thời hạn, …).

    Phải kiểm được từ văn bản: có trong text phiên bản của ``gold_units`` (hoặc cây con/tổ tiên)
    hoặc thuộc tính ``CheTai``/``DiemGPLX`` của M8. ``unit_id`` (tuỳ chọn) thu hẹp chỗ tìm.
    """

    model_config = ConfigDict(extra="forbid")
    value: int | float
    unit: NumberUnit
    unit_id: str | None = None


class QAItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    qid: str = Field(min_length=1)
    question: str = Field(min_length=1)
    as_of: date
    question_type: QuestionType
    tier: Tier | None = None
    """Tier văn bản của câu (khớp tier của ``gold_units``); ``null`` chỉ cho ``ngoai_pham_vi``."""
    answer: str | None = None
    """Bắt buộc với test; train/val sinh tự động không có đáp án."""
    gold_units: list[str] = Field(default_factory=list)
    gold_versions: list[str] = Field(default_factory=list)
    """Mã PhienBan tại ``as_of`` theo thứ tự ``gold_units``; để trống thì validator tự điền vào
    bản ``*_resolved.jsonl`` (không sửa file gốc)."""
    required_numbers: list[RequiredNumber] = Field(default_factory=list)
    source: str = "human"
    """``human`` (test) | ``llm:<model_id>`` (train/val)."""
    pair_id: str | None = None
    """Câu ``theo_thoi_diem``: hai câu (trước/sau mốc) cùng ``pair_id``."""
    notes: str | None = None
    # ---- chỉ train/val (sinh tự động) ----
    chunk_id: str | None = None
    in_test_gold: bool | None = None
    """Positive nằm trong ``gold_units`` của test (đánh dấu, không loại — quyết định 10/11/2026)."""

    @field_validator("question", "answer")
    @classmethod
    def _nfc(cls, v: str | None) -> str | None:
        return None if v is None else unicodedata.normalize("NFC", v).strip()


def split_of(path: str | Path) -> Split:
    """``data/qa/test.jsonl`` → ``test``."""
    stem = Path(path).stem
    for s in SPLITS:
        if stem == s:
            return s
    raise ValueError(f"không suy được split từ tên file {path} (cần test/train/val.jsonl)")


def item_dict(item: QAItem) -> dict[str, Any]:
    """Bản ghi JSONL gọn: bỏ trường rỗng/None của train/val để file nhỏ."""
    d = item.model_dump(mode="json")
    return {k: v for k, v in d.items() if v not in (None, [], "") or k in ("gold_units",)}


__all__ = [
    "QUESTION_TYPES",
    "QUESTION_TYPE_DOC",
    "SPLITS",
    "TIERS",
    "NumberUnit",
    "QAItem",
    "QuestionType",
    "RequiredNumber",
    "Split",
    "Tier",
    "item_dict",
    "split_of",
]
