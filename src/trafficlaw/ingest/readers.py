"""Đọc văn bản gốc (.docx, .doc, .pdf) thành chuỗi thô, giữ đúng thứ tự nội dung.

Reader chỉ *trích* chữ; việc làm sạch nằm ở :mod:`trafficlaw.ingest.normalize`.

Quy ước đầu ra (normalize dựa vào các quy ước này):

- Chú thích (footnote): vị trí tham chiếu trong thân văn bản → ``[^N]``; nội dung chú thích
  là một dòng bắt đầu bằng ``[^N] ``. N là số thứ tự hiển thị (1, 2, …).
- PDF: các trang ngăn cách bằng ``\\f``; dòng thuộc vùng chú thích cuối trang có tiền tố
  :data:`FOOTNOTE_PREFIX` để normalize không nối nó vào thân văn bản.
- Bảng (.docx): mỗi hàng một dòng ``ô | ô``.
"""

from __future__ import annotations

import logging
import re
import shutil
import subprocess
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

logger = logging.getLogger(__name__)

ReaderName = Literal["docx", "antiword", "pymupdf"]

#: Tiền tố (U+001E) đánh dấu dòng thuộc vùng chú thích cuối trang của PDF.
FOOTNOTE_PREFIX = "\x1e"


class RawText(BaseModel):
    model_config = ConfigDict(frozen=True)

    text: str
    reader: ReaderName
    n_pages: int | None = None
    warnings: list[str] = []


class ReaderError(RuntimeError):
    """Không đọc được file (thiếu công cụ, file hỏng, đuôi không hỗ trợ)."""


class ScannedPdfError(ReaderError):
    """PDF không có lớp chữ (bản scan) — M2 không OCR."""


def read_source(path: str | Path, *, min_chars_per_page: int = 50) -> RawText:
    """Chọn reader theo đuôi file (không phân biệt hoa thường)."""
    p = Path(path)
    if not p.is_file():
        raise ReaderError(f"không thấy file {p}")
    ext = p.suffix.lower()
    if ext == ".docx":
        return read_docx(p)
    if ext == ".doc":
        return read_doc(p)
    if ext == ".pdf":
        return read_pdf(p, min_chars_per_page=min_chars_per_page)
    raise ReaderError(f"đuôi file không hỗ trợ: {ext!r}")


# --------------------------------------------------------------------------- .docx

_W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def _local(tag: Any) -> str:
    return tag.rsplit("}", 1)[-1] if isinstance(tag, str) else ""


class _DocxState:
    def __init__(self, footnotes: dict[str, str]) -> None:
        self.footnotes = footnotes  # w:id → nội dung
        self.n_ref = 0
        self.n_sym = 0
        self.pending: list[str] = []  # chú thích chờ in sau đoạn hiện tại


def _load_footnotes(doc: Any) -> dict[str, str]:
    """``w:id`` → nội dung chú thích (bỏ separator). Rỗng nếu văn bản không có chú thích."""
    try:
        part = next(
            rel.target_part
            for rel in doc.part.rels.values()
            if rel.reltype.endswith("/footnotes") and not rel.is_external
        )
    except StopIteration:
        return {}
    from lxml import etree

    root = etree.fromstring(part.blob)
    out: dict[str, str] = {}
    for fn in root.iter(f"{_W}footnote"):
        if fn.get(f"{_W}type") in ("separator", "continuationSeparator", "continuationNotice"):
            continue
        st = _DocxState({})
        text = " ".join(t for p in fn.iter(f"{_W}p") if (t := _para_text(p, st).strip()))
        out[fn.get(f"{_W}id", "")] = text
    return out


def _para_text(p: Any, st: _DocxState) -> str:
    """Chữ của một ``w:p`` theo thứ tự run; chú thích → ``[^N]``."""
    parts: list[str] = []
    for el in p.iter():
        tag = _local(el.tag)
        if tag == "t":
            parts.append(el.text or "")
        elif tag == "tab":
            # w:tab trong w:pPr/w:tabs là định nghĩa điểm dừng tab, không phải ký tự.
            if _local(el.getparent().tag) != "tabs":
                parts.append("\t")
        elif tag in ("br", "cr"):
            parts.append("\n")
        elif tag == "noBreakHyphen":
            parts.append("-")
        elif tag == "sym":
            st.n_sym += 1
            ch = el.get(f"{_W}char", "")
            try:
                parts.append(chr(int(ch, 16)))
            except ValueError:
                parts.append("�")
        elif tag == "footnoteReference":
            st.n_ref += 1
            parts.append(f"[^{st.n_ref}]")
            body = st.footnotes.get(el.get(f"{_W}id", ""))
            if body is not None:
                st.pending.append(f"[^{st.n_ref}] {body}")
    return "".join(parts)


def _cell_text(tc: Any, st: _DocxState) -> str:
    """Các đoạn (và bảng lồng) trong một ô nối bằng dấu cách."""
    chunks: list[str] = []
    for child in tc:
        tag = _local(child.tag)
        if tag == "p":
            chunks.append(_para_text(child, st))
        elif tag == "tbl":
            chunks.extend(_table_lines(child, st))
    return " ".join(c.replace("\n", " ").strip() for c in chunks if c.strip())


def _table_lines(tbl: Any, st: _DocxState) -> list[str]:
    """Mỗi hàng một dòng ``ô | ô``.

    Duyệt trực tiếp ``w:tc`` (ô gộp ngang ``gridSpan`` chỉ có một ``w:tc``) và bỏ ô tiếp nối
    của gộp dọc (``w:vMerge`` không có ``val="restart"``) → không lặp nội dung ô gộp.
    """
    lines: list[str] = []
    for tr in tbl.iter(f"{_W}tr"):
        if tr.getparent() is not tbl:  # hàng của bảng lồng: xử lý trong _cell_text
            continue
        cells: list[str] = []
        for tc in tr.iterchildren(f"{_W}tc"):
            vm = tc.find(f"{_W}tcPr/{_W}vMerge")
            if vm is not None and vm.get(f"{_W}val") != "restart":
                continue
            text = _cell_text(tc, st)
            if text:
                cells.append(text)
        if cells:
            lines.append(" | ".join(cells))
    return lines


def _block_lines(container: Any, st: _DocxState) -> list[str]:
    lines: list[str] = []
    for child in container.iterchildren():
        tag = _local(child.tag)
        if tag == "p":
            lines.append(_para_text(child, st))
        elif tag == "tbl":
            lines.extend(_table_lines(child, st))
        elif tag == "sdt":
            content = child.find(f"{_W}sdtContent")
            if content is not None:
                lines.extend(_block_lines(content, st))
        else:
            continue
        if st.pending:
            lines.extend(st.pending)
            st.pending.clear()
    return lines


def read_docx(path: str | Path) -> RawText:
    """Duyệt ``document.element.body`` theo thứ tự: ``w:p`` và ``w:tbl`` xen kẽ.

    Không dùng ``doc.paragraphs`` / ``doc.tables`` riêng rẽ (bảng chữ ký, "Nơi nhận" sẽ bị
    đưa lên đầu). Chú thích được chèn ngay sau đoạn chứa tham chiếu.
    """
    import docx

    try:
        doc = docx.Document(str(path))
    except Exception as e:  # file hỏng, không phải docx
        raise ReaderError(f"python-docx không mở được {path}: {e}") from e
    st = _DocxState(_load_footnotes(doc))
    lines = _block_lines(doc.element.body, st)
    warnings: list[str] = []
    if st.n_sym:
        warnings.append(f"{st.n_sym} ký tự w:sym (symbol font)")
    if st.footnotes and st.n_ref != len(st.footnotes):
        warnings.append(f"{len(st.footnotes)} chú thích nhưng {st.n_ref} tham chiếu")
    return RawText(text="\n".join(lines), reader="docx", warnings=warnings)


# --------------------------------------------------------------------------- .doc


def find_antiword() -> str | None:
    return shutil.which("antiword")


_LONE_C2 = re.compile(rb"\xc2(?![\x80-\xbf])")


def fix_lone_c2(data: bytes) -> tuple[bytes, int]:
    """antiword đôi khi chỉ ghi byte đầu (0xC2) của NBSP ``C2 A0`` ở cuối đoạn.

    Byte 0xC2 không có byte tiếp nối là UTF-8 sai (vốn sẽ thành U+FFFD) → thay bằng dấu cách.
    """
    return _LONE_C2.subn(b" ", data)


def read_doc(path: str | Path, *, antiword: str | None = None) -> RawText:
    """Đọc .doc bằng ``antiword -m UTF-8.txt -w 0`` (không ngắt dòng).

    antiword trên Windows lỗi với đường dẫn có dấu → luôn copy sang file tạm tên ASCII.
    """
    exe = antiword or find_antiword()
    if exe is None:
        raise ReaderError("không tìm thấy antiword (Ubuntu: sudo apt-get install -y antiword)")
    with tempfile.TemporaryDirectory(prefix="trafficlaw-doc-") as tmp:
        src = Path(tmp) / "source.doc"
        shutil.copyfile(path, src)
        try:
            proc = subprocess.run(
                [exe, "-m", "UTF-8.txt", "-w", "0", str(src)],
                capture_output=True,
                timeout=300,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as e:
            raise ReaderError(f"không chạy được antiword ({exe}): {e}") from e
    if proc.returncode != 0:
        err = proc.stderr.decode("utf-8", errors="replace").strip()
        raise ReaderError(f"antiword lỗi (mã {proc.returncode}) với {path}: {err}")
    raw, n_lone = fix_lone_c2(proc.stdout)
    text = raw.decode("utf-8", errors="replace")
    warnings: list[str] = []
    if n_lone:
        warnings.append(f"{n_lone} byte 0xC2 lẻ (NBSP bị antiword cắt) → dấu cách")
    if err := proc.stderr.decode("utf-8", errors="replace").strip():
        warnings.append(f"antiword stderr: {err[:200]}")
    return RawText(text=text, reader="antiword", warnings=warnings)


# --------------------------------------------------------------------------- .pdf

_SUPERSCRIPT = 1  # bit cờ superscript của span PyMuPDF


def _is_digits(s: str) -> bool:
    return s.strip().isdigit()


def _body_size(doc: Any) -> float:
    """Cỡ chữ thân văn bản = cỡ chữ chiếm nhiều ký tự nhất."""
    sizes: Counter[float] = Counter()
    for page in doc:
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for sp in line["spans"]:
                    sizes[round(sp["size"] * 2) / 2] += len(sp["text"].strip())
    return sizes.most_common(1)[0][0] if sizes else 0.0


class _PdfLine:
    __slots__ = ("is_fn_start", "max_size", "text")

    def __init__(self, text: str, max_size: float, is_fn_start: bool) -> None:
        self.text = text
        self.max_size = max_size
        self.is_fn_start = is_fn_start


def _pdf_line(spans: list[dict[str, Any]], body: float) -> _PdfLine:
    """Ghép span của một dòng; số chú thích (superscript hoặc chữ số nhỏ) → ``[^N]``."""
    small = body * 0.75
    parts: list[str] = []
    is_fn_start = False
    first = True
    for sp in spans:
        t = sp["text"]
        if not t.strip():
            parts.append(t)
            continue
        digit_mark = _is_digits(t) and (sp["flags"] & _SUPERSCRIPT or sp["size"] <= small)
        if digit_mark and first:
            # Dòng mở đầu chú thích cuối trang: "¹ Luật số …"
            is_fn_start = True
            parts.append(f"[^{t.strip()}]")
        elif digit_mark:
            prev = "".join(parts).rstrip()
            # m², m³ (đơn vị), không phải chú thích
            if prev.endswith("m") and t.strip() in ("2", "3"):
                parts.append(t.strip())
            else:
                parts.append(f"[^{t.strip()}]")
        else:
            parts.append(t)
        first = False
    sizes = [sp["size"] for sp in spans if sp["text"].strip()]
    text = "".join(parts)
    if is_fn_start:
        text = text.replace("]", "] ", 1).replace("]  ", "] ", 1)
    return _PdfLine(text, max(sizes, default=0.0), is_fn_start)


def _footnote_zone_start(lines: list[_PdfLine], body: float, prev_had_zone: bool) -> int:
    """Chỉ số dòng đầu của vùng chú thích cuối trang (``len(lines)`` nếu không có).

    Vùng chú thích = dãy dòng cuối trang có cỡ chữ ≤ thân − 1,5 (bỏ qua dòng chỉ là số
    trang), và chứa ít nhất một dòng mở đầu chú thích — hoặc trang trước cũng kết thúc bằng
    vùng chú thích (chú thích dài tràn sang trang sau).
    """
    limit = body - 1.5
    i = len(lines)
    has_start = False
    while i > 0:
        ln = lines[i - 1]
        if not ln.text.strip() or (_is_digits(ln.text) and i == len(lines)):
            i -= 1
            continue
        if ln.max_size <= limit:
            has_start = has_start or ln.is_fn_start
            i -= 1
            continue
        break
    # Bỏ các dòng trống/ số trang ở đầu vùng tìm được để chúng thuộc thân.
    while i < len(lines) and not lines[i].text.strip():
        i += 1
    if i < len(lines) and (has_start or prev_had_zone):
        return i
    return len(lines)


def read_pdf(path: str | Path, *, min_chars_per_page: int = 50) -> RawText:
    """Đọc PDF có lớp chữ bằng PyMuPDF (pypdf tách ký tự kiểu "đ ến").

    Trung bình < ``min_chars_per_page`` ký tự/trang → :class:`ScannedPdfError`.
    """
    import pymupdf

    try:
        doc = pymupdf.open(str(path))
    except Exception as e:
        raise ReaderError(f"PyMuPDF không mở được {path}: {e}") from e
    with doc:
        n_pages = doc.page_count
        n_chars = sum(len(p.get_text().strip()) for p in doc)
        if n_pages == 0 or n_chars / n_pages < min_chars_per_page:
            raise ScannedPdfError(
                f"{path}: {n_chars} ký tự / {n_pages} trang — PDF scan, không có lớp chữ"
            )
        body = _body_size(doc)
        pages: list[str] = []
        prev_zone = False
        n_fn = 0
        for page in doc:
            lines = [
                _pdf_line(line["spans"], body)
                for block in page.get_text("dict")["blocks"]
                for line in block.get("lines", [])
            ]
            z = _footnote_zone_start(lines, body, prev_zone)
            prev_zone = z < len(lines)
            out = [ln.text for ln in lines[:z]]
            for ln in lines[z:]:
                if _is_digits(ln.text):  # số trang ở cuối trang
                    out.append(ln.text)
                elif ln.text.strip():
                    n_fn += ln.is_fn_start
                    out.append(FOOTNOTE_PREFIX + ln.text)
            pages.append("\n".join(out))
    warnings = [f"{n_fn} chú thích cuối trang"] if n_fn else []
    return RawText(text="\f".join(pages), reader="pymupdf", n_pages=n_pages, warnings=warnings)
