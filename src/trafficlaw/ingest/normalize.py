"""Chuẩn hoá chuỗi thô của reader → văn bản interim (UTF-8, LF, NFC).

Hàm thuần, không I/O. Không bao giờ xoá U+FFFD hay ký tự symbol-font: chỉ đếm và báo.

Với PDF (``source="pdf"``), ngoài phần chung còn:

- bỏ dòng chỉ là số trang (đầu/cuối trang) và các dòng chữ ký số;
- nối dòng bị ngắt do xuống dòng của trang in, trừ trước các dòng *được bảo vệ*
  (``Điều N.``, ``N.``, ``a)``/``đ)``, ``Chương``, ``Mục``, ``Phần``, chú thích ``[^N]``,
  gạch đầu dòng, dòng toàn chữ hoa);
- chú thích cuối trang (dòng có :data:`~trafficlaw.ingest.readers.FOOTNOTE_PREFIX`) không
  chen vào giữa đoạn: đoạn bị ngắt qua trang được nối liền, chú thích đặt ngay sau đoạn đó.
"""

from __future__ import annotations

import re
import unicodedata
from collections import Counter
from dataclasses import dataclass, field
from typing import Literal

from trafficlaw.ingest.readers import FOOTNOTE_PREFIX

SourceKind = Literal["word", "pdf"]

# Ký tự khoảng trắng đặc biệt → dấu cách; ký tự vô hình → xoá.
_TO_SPACE = dict.fromkeys(map(ord, "      \t\v"), " ")
_TO_DELETE = dict.fromkeys(map(ord, "​‌‍⁠﻿­\x07"), None)
_TRANSLATE = {**_TO_SPACE, **_TO_DELETE}

_PRIVATE_USE = re.compile("[-]")  # ký tự symbol-font (Wingdings, Symbol…)
_MULTI_SPACE = re.compile(r" {2,}")
_DIEU = re.compile(r"^Điều \d+[a-z]?\.", re.MULTILINE)

_PAGE_NUMBER = re.compile(r"^(?:Trang\s*)?\d{1,4}(?:\s*/\s*\d{1,4})?$", re.IGNORECASE)
_SIGNATURE = re.compile(r"^(?:Người ký|Cơ quan|Thời gian ký|Email)\s*:", re.IGNORECASE)

# Dòng không được nối vào dòng trước (đầu một đơn vị cấu trúc / chú thích / gạch đầu dòng).
_PROTECTED = re.compile(
    r"""^(?:
        Điều\s+\d+[a-z]?\.            # Điều 6. / Điều 6a.
      | \d+[a-z]?\.(?:\s|$|\[\^)      # 1. / 2a. / 18.[^6] (khoản có chú thích)
      | [a-zđ]\d*\)                   # a) đ) a1)
      | \[\^\d+\]                     # chú thích
      | [-+•*–—]\s                    # gạch đầu dòng
      | Nơi\s+nhận
    )""",
    re.VERBOSE,
)
# Tiêu đề Chương/Mục/Phần/Phụ lục: "Chương II", "Mục 2. ĐƯỜNG CAO TỐC", "PHỤ LỤC I".
# Phần sau số thứ tự phải trống hoặc không có chữ thường — "Chương II của Luật này" hay
# "Phụ lục I ban hành kèm theo" ở đầu dòng in là giữa câu, được nối bình thường.
_SECTION = re.compile(
    r"^(?:Chương|CHƯƠNG|Mục|MỤC|Phần|PHẦN|Phụ\s+lục|PHỤ\s+LỤC)"
    r"(?:\s+(?:[IVXLCD]+|\d+[a-z]?|thứ\s+\w+|THỨ\s+\w+))?\b\s*[.:–-]?\s*(?P<rest>.*)$"
)
_DIEU_HEADING = re.compile(r"^Điều\s+\d+[a-z]?\.")


def is_section_heading(line: str) -> bool:
    m = _SECTION.match(line)
    return m is not None and not any(c.islower() for c in m.group("rest"))


def _is_heading(line: str) -> bool:
    return _DIEU_HEADING.match(line) is not None or is_section_heading(line)


_END_PUNCT = re.compile(r"""[.:;!?]["”'’)]*$|\./\.$""")
_FN_START = re.compile(r"^\[\^\d+\]")


@dataclass
class NormalizeResult:
    text: str
    n_replacement_chars: int = 0
    n_symbol_chars: int = 0
    n_page_numbers_removed: int = 0
    n_signature_lines_removed: int = 0
    n_lines_joined: int = 0
    warnings: list[str] = field(default_factory=list)


# --------------------------------------------------------------------------- đo đạc


def count_replacement_chars(text: str) -> int:
    return text.count("�")


def count_symbol_font_chars(text: str) -> int:
    return len(_PRIVATE_USE.findall(text))


def count_dieu_headings(text: str) -> int:
    """Số dòng bắt đầu bằng ``Điều N.`` (kể cả Điều trong phụ lục / mẫu — M3 lọc)."""
    return len(_DIEU.findall(text))


def has_dieu_1(text: str) -> bool:
    return re.search(r"^Điều 1\.", text, re.MULTILINE) is not None


_WORD = re.compile(r"[^\W\d_]+")
# Token 1 ký tự hợp lệ: nhãn Điểm ("điểm a", "a)", "điểm a, b và c") và từ "ô" (ô tô).
_LABEL_BEFORE = re.compile(r"(?:điểm|Điểm|các|,|và|hoặc)\s*$")


def single_char_token_ratio(text: str) -> float:
    """Tỷ lệ token chữ dài đúng 1 ký tự — cao bất thường ⇒ chữ bị tách ("đ ến").

    Không tính token hợp lệ: nhãn Điểm (sau "điểm"/dấu phẩy/"và"/"hoặc", hoặc trước ")")
    và "ô" — văn bản sửa đổi liệt kê dày đặc "điểm a, điểm b…" sẽ bị báo nhầm.
    """
    n_tokens = 0
    singles = 0
    for m in _WORD.finditer(text):
        n_tokens += 1
        tok = m.group()
        if len(tok) != 1:
            continue
        if tok in "ôÔ" or text[m.end() : m.end() + 1] == ")":
            continue
        if _LABEL_BEFORE.search(text[max(0, m.start() - 8) : m.start()]):
            continue
        singles += 1
    return singles / n_tokens if n_tokens else 0.0


def _so_hieu_pattern(so_hieu: str) -> re.Pattern[str]:
    """Regex dễ dãi cho số hiệu: khoảng trắng quanh ``/`` và ``-``, NĐ≈ND, Đ≈D, hoa/thường."""
    s = unicodedata.normalize("NFC", so_hieu.strip())
    parts: list[str] = []
    for ch in s:
        if ch in "/-":
            parts.append(rf"\s*{re.escape(ch)}\s*")
        elif ch in "ĐđDd":
            parts.append("[ĐđDd]")
        elif ch.isspace():
            parts.append(r"\s*")
        else:
            parts.append(re.escape(ch))
    return re.compile(r"(?<!\d)" + "".join(parts), re.IGNORECASE)


def find_so_hieu(text: str, so_hieu: str | None) -> bool:
    if not so_hieu:
        return False
    return _so_hieu_pattern(so_hieu).search(text) is not None


# --------------------------------------------------------------------------- chuẩn hoá


def _clean_line(line: str) -> str:
    line = line.translate(_TRANSLATE)
    return _MULTI_SPACE.sub(" ", line).strip()


def _antiword_table_row(line: str) -> str:
    """``|ô 1   |ô 2 |`` (bảng của antiword) → ``ô 1 | ô 2``; dòng khác giữ nguyên."""
    if len(line) >= 2 and line.startswith("|") and line.endswith("|"):
        cells = [c.strip() for c in line[1:-1].split("|")]
        return " | ".join(c for c in cells if c)
    return line


def _collapse_blank_lines(lines: list[str]) -> list[str]:
    out: list[str] = []
    for ln in lines:
        if not ln and (not out or not out[-1]):
            continue
        out.append(ln)
    while out and not out[-1]:
        out.pop()
    return out


def _is_upper_line(line: str) -> bool:
    letters = [c for c in line if c.isalpha()]
    return len(letters) >= 2 and all(c.isupper() for c in letters)


def should_join(prev: str, nxt: str) -> bool:
    """Dòng ``nxt`` (PDF) có phải phần tiếp của dòng ``prev`` bị ngắt do xuống dòng in?"""
    if not prev or not nxt:
        return False
    if (
        _PROTECTED.match(nxt)
        or is_section_heading(nxt)
        or _is_upper_line(nxt)
        or _is_upper_line(prev)
    ):
        return False
    if _END_PUNCT.search(prev):
        # "… bao gồm:" + "người điều khiển xe cơ giới …": câu chạy tiếp (danh sách thật bắt đầu
        # bằng a) / 1. / gạch đầu dòng — đã bị chặn ở trên). Sau dấu chấm thì không nối.
        return prev[-1] in ":;" and nxt[0].islower()
    if _is_heading(prev):
        # "Điều 47. Bảo đảm … trong vận chuyển" + "hành khách, …" → nối;
        # "Điều 1. Phạm vi điều chỉnh" + "Luật này quy định …" → không.
        return nxt[0].islower()
    return True


def _drop_page_furniture(pages: list[list[str]], res: NormalizeResult) -> list[list[str]]:
    """Bỏ dòng chữ ký số và dòng số trang.

    Dòng số trang = dòng có chữ đầu tiên/cuối cùng của trang, chỉ gồm một số ``v`` với
    ``v − (chỉ số trang)`` bằng độ lệch phổ biến nhất của cả văn bản. Điều kiện độ lệch giúp
    không xoá nhầm ô số ở cuối bảng ("02", "93").
    """
    cleaned: list[list[str]] = []
    for lines in pages:
        kept = []
        for ln in lines:
            if _SIGNATURE.match(ln.lstrip(FOOTNOTE_PREFIX)):
                res.n_signature_lines_removed += 1
                continue
            kept.append(ln)
        cleaned.append(kept)

    candidates: list[tuple[int, int, int]] = []  # (trang, dòng, độ lệch)
    for p, kept in enumerate(cleaned):
        nonblank = [i for i, ln in enumerate(kept) if ln]
        for i in sorted(set(nonblank[:1] + nonblank[-1:])):
            if _PAGE_NUMBER.match(kept[i]):
                value = int(re.findall(r"\d+", kept[i])[0])
                candidates.append((p, i, value - (p + 1)))
    if not candidates:
        return cleaned
    offset = Counter(c[2] for c in candidates).most_common(1)[0][0]
    drop = {(p, i) for p, i, off in candidates if off == offset}
    res.n_page_numbers_removed += len(drop)
    return [
        [ln for i, ln in enumerate(kept) if (p, i) not in drop] for p, kept in enumerate(cleaned)
    ]


def _join_pdf_lines(lines: list[str | None], res: NormalizeResult) -> list[str]:
    """Nối dòng thân văn bản; chú thích dồn lại và in ngay sau đoạn đang mở.

    ``None`` trong ``lines`` = ranh giới trang (không phải dòng trống: đoạn được nối qua trang).
    """
    out: list[str] = []
    cur: str | None = None  # đoạn thân văn bản đang mở
    pending: list[str] = []  # chú thích chờ in
    last_fn: int | None = None  # chỉ số (trong out) của chú thích in gần nhất

    def flush() -> None:
        nonlocal cur, last_fn
        if cur is not None:
            out.append(cur)
            cur = None
        for fn in pending:
            out.append(fn)
            last_fn = len(out) - 1
        pending.clear()

    for raw in lines:
        if raw is None:
            continue
        if raw.startswith(FOOTNOTE_PREFIX):
            fn = raw[len(FOOTNOTE_PREFIX) :].strip()
            if not fn:
                continue
            if _FN_START.match(fn) or (not pending and last_fn is None):
                pending.append(fn)
            elif pending:
                pending[-1] += " " + fn
                res.n_lines_joined += 1
            else:  # chú thích tràn sang trang sau, phần đầu đã được in
                out[last_fn] += " " + fn  # type: ignore[index]
                res.n_lines_joined += 1
            continue
        line = raw
        if not line:
            flush()
            out.append("")
            continue
        if cur is not None and should_join(cur, line):
            cur += " " + line
            res.n_lines_joined += 1
            continue
        flush()
        cur = line
    flush()
    return out


def normalize_text(text: str, *, source: SourceKind) -> NormalizeResult:
    """Chuẩn hoá chuỗi thô của reader. ``source="pdf"`` bật các bước riêng cho PDF."""
    res = NormalizeResult(text="")
    text = unicodedata.normalize("NFC", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    pages_raw = text.split("\f")
    pages: list[list[str]] = []
    for page in pages_raw:
        lines = []
        for raw in page.split("\n"):
            is_fn = raw.startswith(FOOTNOTE_PREFIX)
            ln = _clean_line(raw.lstrip(FOOTNOTE_PREFIX))
            if source == "word":
                ln = _antiword_table_row(ln)
            lines.append(FOOTNOTE_PREFIX + ln if is_fn and ln else ln)
        pages.append(lines)

    if source == "pdf":
        pages = _drop_page_furniture(pages, res)
        flat: list[str | None] = []
        for i, lines in enumerate(pages):
            if i:
                flat.append(None)
            # Vùng chú thích luôn ở cuối trang. Dòng trống ở đầu/cuối phần thân chỉ là lề
            # trang (hoặc khoảng cách trước chú thích), không phải ranh giới đoạn.
            body = [ln for ln in lines if not ln.startswith(FOOTNOTE_PREFIX)]
            notes = [ln for ln in lines if ln.startswith(FOOTNOTE_PREFIX)]
            while body and not body[0]:
                body = body[1:]
            while body and not body[-1]:
                body = body[:-1]
            flat.extend(body + notes)
        out = _join_pdf_lines(flat, res)
    else:
        out = [ln for lines in pages for ln in lines]

    out = _collapse_blank_lines(out)
    while out and not out[0]:
        out.pop(0)
    res.text = "\n".join(out) + "\n" if out else ""
    res.text = unicodedata.normalize("NFC", res.text)

    res.n_replacement_chars = count_replacement_chars(res.text)
    res.n_symbol_chars = count_symbol_font_chars(res.text)
    if res.n_replacement_chars:
        res.warnings.append(f"{res.n_replacement_chars} ký tự U+FFFD")
    if res.n_symbol_chars:
        res.warnings.append(f"{res.n_symbol_chars} ký tự symbol-font (Private Use)")
    return res
