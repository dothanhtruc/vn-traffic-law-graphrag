"""Chương hạn chế: trích **nguyên văn** từ CLAUDE.md / docs theo danh sách trong ``report.yaml``.

Không diễn giải, không thêm số: báo cáo chỉ chép đoạn văn bản tìm được, kèm file + dòng.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Limitation:
    module: str
    title: str
    source: str
    line: int | None
    items: tuple[str, ...]
    status: str  # ok | khong_tim_thay | trung_lap


def extract_span(text: str, start: str, end: str | None = None) -> tuple[int, str] | None | str:
    """Đoạn bắt đầu bằng ``start`` (phải có đúng một lần), tới ``end`` (gồm ``end``) hoặc hết dòng.

    Trả ``(dòng 1-based, đoạn)``; không thấy → ``None``; thấy nhiều lần → ``"trung_lap"``.
    """
    i = text.find(start)
    if i < 0:
        return None
    if text.find(start, i + 1) >= 0:
        return "trung_lap"
    eol = text.find("\n", i)
    eol = len(text) if eol < 0 else eol
    stop = eol
    if end is not None:
        j = text.find(end, i + len(start) - 1, eol)
        if j < 0:
            return None
        stop = j + len(end)
    return text.count("\n", 0, i) + 1, text[i:stop].strip()


def extract_section(text: str, heading: str) -> tuple[int, list[str]] | None:
    """Mọi gạch đầu dòng (nối dòng tiếp theo thụt lề) của mục Markdown có đúng tiêu đề."""
    lines = text.splitlines()
    try:
        k = next(i for i, x in enumerate(lines) if x.strip() == heading)
    except StopIteration:
        return None
    level = len(heading) - len(heading.lstrip("#"))
    items: list[str] = []
    for x in lines[k + 1 :]:
        s = x.strip()
        if s.startswith("#") and len(s) - len(s.lstrip("#")) <= level:
            break
        if s.startswith("- "):
            items.append(s[2:])
        elif s and items and x.startswith(" "):
            items[-1] += " " + s
    return k + 1, items


def collect(
    specs: Sequence[Mapping[str, Any]], texts: Mapping[str, str], paths: Mapping[str, str]
) -> list[Limitation]:
    out: list[Limitation] = []
    for sp in specs:
        src = str(sp["source"])
        text = texts.get(src, "")
        base = {
            "module": str(sp["module"]),
            "title": str(sp["title"]),
            "source": paths.get(src, src),
        }
        if "section" in sp:
            r = extract_section(text, str(sp["section"]))
            if r is None or not r[1]:
                out.append(Limitation(**base, line=None, items=(), status="khong_tim_thay"))
            else:
                out.append(Limitation(**base, line=r[0], items=tuple(r[1]), status="ok"))
            continue
        res = extract_span(text, str(sp["start"]), sp.get("end"))
        if res is None or isinstance(res, str):
            status = "trung_lap" if res == "trung_lap" else "khong_tim_thay"
            out.append(Limitation(**base, line=None, items=(), status=status))
        else:
            out.append(Limitation(**base, line=res[0], items=(res[1],), status="ok"))
    return out


__all__ = ["Limitation", "collect", "extract_section", "extract_span"]
