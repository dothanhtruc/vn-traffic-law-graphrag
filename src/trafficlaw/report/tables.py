"""Bảng Markdown từ ô đã định dạng (chuỗi)."""

from __future__ import annotations

from collections.abc import Sequence


def _esc(s: str) -> str:
    return s.replace("|", "\\|").replace("\n", " ")


def md_table(head: Sequence[str], rows: Sequence[Sequence[str]], align: str | None = None) -> str:
    """``align``: chuỗi ``l``/``r`` cho từng cột (mặc định cột đầu trái, còn lại phải)."""
    n = len(head)
    if align is None:
        align = "l" + "r" * (n - 1)
    if len(align) != n:
        raise ValueError("align phải cùng số cột với head")
    for r in rows:
        if len(r) != n:
            raise ValueError(f"hàng {list(r)!r} có {len(r)} cột, cần {n}")
    sep = ["---:" if a == "r" else "---" for a in align]
    lines = ["| " + " | ".join(_esc(h) for h in head) + " |", "| " + " | ".join(sep) + " |"]
    lines += ["| " + " | ".join(_esc(str(c)) for c in r) + " |" for r in rows]
    return "\n".join(lines)


__all__ = ["md_table"]
