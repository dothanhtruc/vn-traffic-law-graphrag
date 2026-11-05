"""Mã định danh đơn vị pháp lý: ``<MaVB>/D<dieu>/K<khoan>/<diem>``.

Ví dụ: ``ND168-2024/D6/K4/a``, ``LUAT36-2024/D9``, ``VBHN55-VPQH``.

Quy tắc:
- MaVB: chữ in hoa + số, các phần nối bằng ``-`` (``LUAT36-2024``, ``TT38-2024-BGTVT``).
- Số Điều/Khoản: số nguyên, có thể kèm một chữ cái thường khi được bổ sung (``6a``).
- Điểm: một chữ cái tiếng Việt (gồm ``đ``), có thể kèm số khi được bổ sung (``a1``, ``đ1``).
- Điểm có thể nằm thẳng dưới Điều khi Điều không chia Khoản (``.../D3/a``).
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Literal

Level = Literal["van_ban", "dieu", "khoan", "diem"]

_DOC_RE = re.compile(r"^[A-Z]+\d+(?:-[0-9A-Z]+)*$")
_NUM_RE = re.compile(r"^\d+[a-z]?$")
_DIEM_RE = re.compile(r"^[a-zđ]\d*$")


def _nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s).strip()


@dataclass(frozen=True)
class UnitId:
    doc_code: str
    dieu: str | None = None
    khoan: str | None = None
    diem: str | None = None

    def __post_init__(self) -> None:
        if not _DOC_RE.match(self.doc_code):
            raise ValueError(f"Mã văn bản không hợp lệ: {self.doc_code!r}")
        if self.dieu is not None and not _NUM_RE.match(self.dieu):
            raise ValueError(f"Số Điều không hợp lệ: {self.dieu!r}")
        if self.khoan is not None:
            if self.dieu is None:
                raise ValueError("Khoản phải thuộc một Điều")
            if not _NUM_RE.match(self.khoan):
                raise ValueError(f"Số Khoản không hợp lệ: {self.khoan!r}")
        if self.diem is not None:
            if self.dieu is None:
                raise ValueError("Điểm phải thuộc một Điều hoặc Khoản")
            if not _DIEM_RE.match(self.diem):
                raise ValueError(f"Điểm không hợp lệ: {self.diem!r}")

    @property
    def level(self) -> Level:
        if self.diem is not None:
            return "diem"
        if self.khoan is not None:
            return "khoan"
        if self.dieu is not None:
            return "dieu"
        return "van_ban"

    def parent(self) -> UnitId | None:
        if self.diem is not None:
            return UnitId(self.doc_code, self.dieu, self.khoan)
        if self.khoan is not None:
            return UnitId(self.doc_code, self.dieu)
        if self.dieu is not None:
            return UnitId(self.doc_code)
        return None

    def __str__(self) -> str:
        parts = [self.doc_code]
        if self.dieu is not None:
            parts.append(f"D{self.dieu}")
        if self.khoan is not None:
            parts.append(f"K{self.khoan}")
        if self.diem is not None:
            parts.append(self.diem)
        return "/".join(parts)


def make_unit_id(
    doc_code: str,
    dieu: str | int | None = None,
    khoan: str | int | None = None,
    diem: str | None = None,
) -> str:
    """Tạo mã định danh chuẩn (NFC, điểm chữ thường); sai định dạng → ``ValueError``."""

    def norm(v: str | int | None) -> str | None:
        return None if v is None else _nfc(str(v)).lower()

    return str(UnitId(_nfc(doc_code).upper(), norm(dieu), norm(khoan), norm(diem)))


def parse_unit_id(s: str) -> UnitId:
    """Parse ``<MaVB>/D<dieu>/K<khoan>/<diem>``; sai định dạng → ``ValueError``."""
    parts = _nfc(s).split("/")
    doc_code, rest = parts[0], parts[1:]
    dieu = khoan = diem = None
    if rest and rest[0].startswith("D"):
        dieu = rest.pop(0)[1:]
    if rest and rest[0].startswith("K"):
        khoan = rest.pop(0)[1:]
    if rest:
        diem = rest.pop(0)
    if rest or (dieu == "" or khoan == ""):
        raise ValueError(f"Mã định danh không hợp lệ: {s!r}")
    try:
        return UnitId(doc_code, dieu, khoan, diem)
    except ValueError as e:
        raise ValueError(f"Mã định danh không hợp lệ: {s!r} ({e})") from e


def is_valid_unit_id(s: str) -> bool:
    try:
        parse_unit_id(s)
    except ValueError:
        return False
    return True


def parent_id(s: str) -> str | None:
    """Mã của đơn vị cha (Điểm → Khoản/Điều → Điều → Văn bản → None)."""
    p = parse_unit_id(s).parent()
    return None if p is None else str(p)
