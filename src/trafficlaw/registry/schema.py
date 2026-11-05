"""Schema danh mục văn bản (``data/registry/documents.yaml``).

Schema chỉ kiểm tra **định dạng** (mã văn bản, kiểu ngày, giá trị enum). Các vấn đề
**chất lượng dữ liệu** (thiếu ngày, ngày lệch nhau, quan hệ trỏ sai…) để validator báo,
để một lỗi dữ liệu không làm hỏng việc nạp toàn bộ danh mục.
"""

from __future__ import annotations

import unicodedata
from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, field_validator

from trafficlaw.utils.ids import UnitId

Loai = Literal["luat", "nghi_dinh", "thong_tu", "quyet_dinh", "vbhn"]
Tier = Literal["A", "B", "C", "historical", "vbhn"]
RelationType = Literal["SUA_DOI", "THAY_THE", "BAI_BO", "HUONG_DAN", "HOP_NHAT"]
Scope = Literal["toan_bo", "mot_phan"]

TIERS: tuple[str, ...] = ("A", "B", "C", "historical", "vbhn")


def _nfc(v: object) -> object:
    return unicodedata.normalize("NFC", v).strip() if isinstance(v, str) else v


def _check_doc_code(v: str) -> str:
    UnitId(v)  # sai định dạng → ValueError
    return v


class Relation(BaseModel):
    """Quan hệ pháp lý cấp văn bản, đi **từ** văn bản chứa nó **tới** ``target``.

    Ví dụ trong mục của NĐ 238/2026: ``{type: SUA_DOI, target: ND168-2024}`` nghĩa là
    NĐ 238/2026 sửa đổi NĐ 168/2024. Quan hệ tới đúng Khoản/Điểm được trích ở M5.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    type: RelationType
    target: str
    scope: Scope = "mot_phan"
    effective_from: date | None = None
    note: str | None = None

    @field_validator("*", mode="before")
    @classmethod
    def _normalize(cls, v: object) -> object:
        return _nfc(v)

    @field_validator("target")
    @classmethod
    def _target_code(cls, v: str) -> str:
        return _check_doc_code(v)


class DocumentMeta(BaseModel):
    """Một văn bản trong danh mục.

    - ``is_amendment``: văn bản chỉ dùng để sửa văn bản khác → không chỉ mục độc lập,
      nội dung đi vào phiên bản mới của điều khoản bị sửa (CLAUDE.md mục 6).
    - ``issues``: vấn đề đã biết mà validator không tự phát hiện được (ghi bằng tay,
      validator in ra nguyên văn).
    - Ngày thiếu để ``null``, không tự điền.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    doc_id: str
    so_hieu: str | None
    ten: str | None = None
    loai: Loai
    co_quan: str
    ngay_ban_hanh: date | None = None
    hieu_luc_tu: date | None = None
    hieu_luc_den: date | None = None
    tier: Tier
    is_amendment: bool = False
    relations: tuple[Relation, ...] = ()
    source_path: str | None = None
    notes: str | None = None
    issues: tuple[str, ...] = ()

    @field_validator("*", mode="before")
    @classmethod
    def _normalize(cls, v: object) -> object:
        return _nfc(v)

    @field_validator("doc_id")
    @classmethod
    def _doc_code(cls, v: str) -> str:
        return _check_doc_code(v)

    @field_validator("source_path")
    @classmethod
    def _posix_path(cls, v: str | None) -> str | None:
        return None if v is None else v.replace("\\", "/")

    @field_validator("issues", mode="before")
    @classmethod
    def _nfc_issues(cls, v: object) -> object:
        return [_nfc(x) for x in v] if isinstance(v, list) else v

    @property
    def indexable(self) -> bool:
        """Được đưa vào chỉ mục/đồ thị như một văn bản độc lập."""
        return self.tier != "vbhn" and not self.is_amendment
