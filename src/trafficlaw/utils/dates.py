"""Tiện ích ngày tháng.

Quy ước hiệu lực: khoảng ``[effective_from, effective_to]`` **bao gồm cả hai đầu**;
``effective_to = None`` nghĩa là còn hiệu lực. Phiên bản bị thay từ ngày D có
``effective_to = D - 1 ngày`` (xem :func:`day_before`).
"""

from __future__ import annotations

import re
import unicodedata
from datetime import date, timedelta

DATA_CUTOFF = date(2026, 11, 3)
"""Mốc chốt dữ liệu (CLAUDE.md mục 1)."""

_VN_LONG_RE = re.compile(
    r"^(?:ngày\s+)?(\d{1,2})\s+tháng\s+(\d{1,2})\s+năm\s+(\d{4})$", re.IGNORECASE
)
_DMY_RE = re.compile(r"^(\d{1,2})[/.\-](\d{1,2})[/.\-](\d{4})$")
_ISO_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")


def to_iso(d: date | None) -> str | None:
    return None if d is None else d.isoformat()


def parse_iso(s: str | None) -> date | None:
    """``YYYY-MM-DD`` → ``date``; ``None``/chuỗi rỗng → ``None``; sai → ``ValueError``."""
    if s is None or not s.strip():
        return None
    m = _ISO_RE.match(s.strip())
    if not m:
        raise ValueError(f"Không phải ngày ISO YYYY-MM-DD: {s!r}")
    return date(int(m[1]), int(m[2]), int(m[3]))


def parse_vn_date(s: str) -> date:
    """Parse ngày viết kiểu Việt Nam.

    Nhận: ``"ngày 15 tháng 11 năm 2024"``, ``"15/11/2024"``, ``"15-11-2024"``,
    ``"01.01.2026"``, ``"2024-11-15"``. Sai → ``ValueError``.
    """
    t = re.sub(r"\s+", " ", unicodedata.normalize("NFC", s)).strip().rstrip(".,;")
    try:
        if m := _ISO_RE.match(t):
            return date(int(m[1]), int(m[2]), int(m[3]))
        if m := (_VN_LONG_RE.match(t) or _DMY_RE.match(t)):
            return date(int(m[3]), int(m[2]), int(m[1]))
    except ValueError as e:
        raise ValueError(f"Ngày không tồn tại: {s!r}") from e
    raise ValueError(f"Không nhận dạng được ngày: {s!r}")


def day_before(d: date) -> date:
    return d - timedelta(days=1)


def in_effect(as_of: date, effective_from: date | None, effective_to: date | None) -> bool:
    """``as_of`` nằm trong ``[effective_from, effective_to]`` (bao gồm hai đầu).

    ``effective_from = None`` nghĩa là chưa rõ ngày bắt đầu → coi là không có hiệu lực
    (không tự điền ngày thiếu, CLAUDE.md mục 16).
    """
    if effective_from is None or as_of < effective_from:
        return False
    return effective_to is None or as_of <= effective_to
