"""Mã định danh đơn vị pháp lý.

Hai nhánh, nối bằng ``/`` sau mã văn bản (MaVB):

- Nội dung: ``<MaVB>/D<dieu>/K<khoan>/<diem>`` — ``ND168-2024/D6/K4/a``, ``LUAT36-2024/D9``.
- Khung (M3): ``<MaVB>[/P<phan>][/C<chuong>][/M<muc>]`` — ``TT35-2024-BGTVT/P2/C1``,
  ``ND168-2024/C2/M1``; Phụ lục ``<MaVB>/PL<n>``.

Quy tắc:
- MaVB: chữ in hoa + số, các phần nối bằng ``-`` (``LUAT36-2024``, ``TT38-2024-BGTVT``).
- Số Điều/Khoản/Phần/Chương/Mục: số nguyên, có thể kèm một chữ cái thường khi được bổ sung
  (``6a``). Số La Mã của Phần/Chương/Mục đổi sang số Ả Rập (``Chương II`` → ``C2``).
- Chương đánh số lại trong mỗi Phần, Mục đánh số lại trong mỗi Chương ⇒ mã khung là đường dẫn
  đầy đủ. Mã Điều **không** chứa khung (Điều đánh số liên tục trong cả văn bản); cha thực của
  Điều (Chương/Mục chứa nó) ghi ở ``parent_id`` của unit, không suy ra từ mã.
- Điểm: một chữ cái tiếng Việt (gồm ``đ``), có thể kèm số khi được bổ sung (``a1``, ``đ1``).
  Điểm có thể nằm thẳng dưới Điều khi Điều không chia Khoản (``.../D3/a``).
- Phụ lục: số theo tiêu đề (``PL1``); trùng số thì thêm hậu tố ``-2``, ``-3`` (``PL1-2``).
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from typing import Literal

Level = Literal["van_ban", "phan", "chuong", "muc", "dieu", "khoan", "diem", "phu_luc"]

_DOC_RE = re.compile(r"^[A-Z]+\d+(?:-[0-9A-Z]+)*$")
_NUM_RE = re.compile(r"^\d+[a-z]?$")
_DIEM_RE = re.compile(r"^[a-zđ]\d*$")
_PL_RE = re.compile(r"^\d+[a-z]?(?:-\d+)?$")
_ROMAN_RE = re.compile(r"^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$")
_ROMAN_VAL = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def _nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s).strip()


def roman_to_int(s: str) -> int:
    """``"XIV"`` → 14; không phải số La Mã chuẩn (chữ hoa) → ``ValueError``."""
    if not s or not _ROMAN_RE.match(s):
        raise ValueError(f"Không phải số La Mã: {s!r}")
    total = 0
    for ch, nxt in zip(s, [*s[1:], ""], strict=True):
        v = _ROMAN_VAL[ch]
        total += -v if nxt and _ROMAN_VAL[nxt] > v else v
    return total


@dataclass(frozen=True)
class UnitId:
    doc_code: str
    dieu: str | None = None
    khoan: str | None = None
    diem: str | None = None
    phan: str | None = None
    chuong: str | None = None
    muc: str | None = None
    phu_luc: str | None = None

    def __post_init__(self) -> None:
        if not _DOC_RE.match(self.doc_code):
            raise ValueError(f"Mã văn bản không hợp lệ: {self.doc_code!r}")
        for name, val in (("Phần", self.phan), ("Chương", self.chuong), ("Mục", self.muc)):
            if val is not None and not _NUM_RE.match(val):
                raise ValueError(f"Số {name} không hợp lệ: {val!r}")
        frame = any(v is not None for v in (self.phan, self.chuong, self.muc))
        content = self.dieu is not None or self.khoan is not None or self.diem is not None
        if self.phu_luc is not None:
            if frame or content:
                raise ValueError("Phụ lục nằm thẳng dưới văn bản")
            if not _PL_RE.match(self.phu_luc):
                raise ValueError(f"Số Phụ lục không hợp lệ: {self.phu_luc!r}")
        if frame and content:
            raise ValueError("Mã Điều/Khoản/Điểm không chứa Phần/Chương/Mục")
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
        if self.phu_luc is not None:
            return "phu_luc"
        if self.muc is not None:
            return "muc"
        if self.chuong is not None:
            return "chuong"
        if self.phan is not None:
            return "phan"
        return "van_ban"

    def parent(self) -> UnitId | None:
        """Cha theo mã. Với Điều trả về văn bản; cha thực (Chương/Mục) xem ``Unit.parent_id``."""
        d = self.doc_code
        if self.diem is not None:
            return UnitId(d, self.dieu, self.khoan)
        if self.khoan is not None:
            return UnitId(d, self.dieu)
        if self.muc is not None:
            return UnitId(d, phan=self.phan, chuong=self.chuong)
        if self.chuong is not None:
            return UnitId(d, phan=self.phan)
        if any(v is not None for v in (self.dieu, self.phan, self.phu_luc)):
            return UnitId(d)
        return None

    def __str__(self) -> str:
        parts = [self.doc_code]
        if self.phu_luc is not None:
            parts.append(f"PL{self.phu_luc}")
        for prefix, val in (("P", self.phan), ("C", self.chuong), ("M", self.muc)):
            if val is not None:
                parts.append(f"{prefix}{val}")
        if self.dieu is not None:
            parts.append(f"D{self.dieu}")
        if self.khoan is not None:
            parts.append(f"K{self.khoan}")
        if self.diem is not None:
            parts.append(self.diem)
        return "/".join(parts)


def _norm(v: str | int | None) -> str | None:
    return None if v is None else _nfc(str(v)).lower()


def make_unit_id(
    doc_code: str,
    dieu: str | int | None = None,
    khoan: str | int | None = None,
    diem: str | None = None,
) -> str:
    """Tạo mã Điều/Khoản/Điểm chuẩn (NFC, chữ thường); sai định dạng → ``ValueError``."""
    return str(UnitId(_nfc(doc_code).upper(), _norm(dieu), _norm(khoan), _norm(diem)))


def make_frame_id(
    doc_code: str,
    *,
    phan: str | int | None = None,
    chuong: str | int | None = None,
    muc: str | int | None = None,
) -> str:
    """Mã Phần/Chương/Mục, vd. ``make_frame_id("TT35-2024-BGTVT", phan=2, chuong=1)``."""
    return str(
        UnitId(_nfc(doc_code).upper(), phan=_norm(phan), chuong=_norm(chuong), muc=_norm(muc))
    )


def make_appendix_id(doc_code: str, number: str | int) -> str:
    """Mã Phụ lục, vd. ``make_appendix_id("TT53-2024-BGTVT", 1)`` → ``TT53-2024-BGTVT/PL1``."""
    return str(UnitId(_nfc(doc_code).upper(), phu_luc=_norm(number)))


_PREFIXES = (("PL", "phu_luc"), ("P", "phan"), ("C", "chuong"), ("M", "muc"))


def parse_unit_id(s: str) -> UnitId:
    """Parse mã định danh (nhánh nội dung hoặc khung); sai định dạng → ``ValueError``."""
    parts = _nfc(s).split("/")
    doc_code, rest = parts[0], parts[1:]
    fields: dict[str, str] = {}
    # Khung: PL / P / C / M theo đúng thứ tự, mỗi loại tối đa một lần.
    for prefix, name in _PREFIXES:
        if rest and rest[0].startswith(prefix) and rest[0][len(prefix) :][:1].isdigit():
            fields[name] = rest.pop(0)[len(prefix) :]
    if rest and rest[0].startswith("D"):
        fields["dieu"] = rest.pop(0)[1:]
    if rest and rest[0].startswith("K"):
        fields["khoan"] = rest.pop(0)[1:]
    if rest and not rest[0][:1].isupper():
        fields["diem"] = rest.pop(0)
    if rest or any(v == "" for v in fields.values()):
        raise ValueError(f"Mã định danh không hợp lệ: {s!r}")
    try:
        return UnitId(doc_code, **fields)
    except ValueError as e:
        raise ValueError(f"Mã định danh không hợp lệ: {s!r} ({e})") from e


def is_valid_unit_id(s: str) -> bool:
    try:
        parse_unit_id(s)
    except ValueError:
        return False
    return True


def parent_id(s: str) -> str | None:
    """Mã của đơn vị cha theo mã (Điểm → Khoản/Điều → Điều → Văn bản → None).

    Mục → Chương → Phần → Văn bản; Phụ lục → Văn bản. Điều → Văn bản (cha thực trong cây
    văn bản là Chương/Mục, lưu ở ``parent_id`` của unit).
    """
    p = parse_unit_id(s).parent()
    return None if p is None else str(p)
