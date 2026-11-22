"""Định dạng số kiểu Việt Nam cho báo cáo (dấu phẩy thập phân, dấu chấm hàng nghìn).

Mọi con số hiển thị trong báo cáo phải đi qua các hàm này — văn bản mẫu (``texts.py``) không chứa
chữ số trần.
"""

from __future__ import annotations

from typing import Any

DASH = "—"


def _is_num(x: Any) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def vn_int(x: Any) -> str:
    """``20129`` → ``20.129``."""
    if not _is_num(x):
        return DASH
    return f"{round(x):,}".replace(",", ".")


def vn_dec(x: Any, nd: int = 1) -> str:
    """``0.8689, 3`` → ``0,869``; số lớn có dấu chấm hàng nghìn."""
    if not _is_num(x):
        return DASH
    s = f"{abs(float(x)):,.{nd}f}"
    s = s.replace(",", "\x00").replace(".", ",").replace("\x00", ".")
    return "−" + s if float(x) < 0 and s.strip("0,.") else s


def vn_pct(x: Any, nd: int = 1) -> str:
    """Tỷ lệ 0–1 → phần trăm không kèm ký hiệu: ``0.8434`` → ``84,3``."""
    return vn_dec(100 * float(x), nd) if _is_num(x) else DASH


def vn_signed_pct(x: Any, nd: int = 1) -> str:
    if not _is_num(x):
        return DASH
    s = vn_pct(abs(x), nd)
    return ("+" if x >= 0 else "−") + s


def vn_ci_pct(ci: Any, nd: int = 1) -> str:
    """``[0.81, 0.87]`` → ``81,4–87,3``."""
    if not ci or len(ci) != 2 or not all(_is_num(v) for v in ci):
        return DASH
    lo, hi = ci
    return f"{_signed_plain(100 * lo, nd)}…{_signed_plain(100 * hi, nd)}"


def vn_ci_dec(ci: Any, nd: int = 2) -> str:
    if not ci or len(ci) != 2 or not all(_is_num(v) for v in ci):
        return DASH
    return f"{_signed_plain(ci[0], nd)}…{_signed_plain(ci[1], nd)}"


def _signed_plain(x: float, nd: int) -> str:
    return vn_dec(x, nd)


def vn_p(x: Any) -> str:
    """p-value: ``<0,001`` hoặc ba chữ số thập phân."""
    if not _is_num(x):
        return DASH
    return "<0,001" if x < 0.001 else vn_dec(x, 3)


def short_hash(h: Any, n: int = 12) -> str:
    return str(h)[:n] if h else DASH


__all__ = [
    "DASH",
    "short_hash",
    "vn_ci_dec",
    "vn_ci_pct",
    "vn_dec",
    "vn_int",
    "vn_p",
    "vn_pct",
    "vn_signed_pct",
]
