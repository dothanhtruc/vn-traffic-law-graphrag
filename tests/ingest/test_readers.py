import shutil
from pathlib import Path

import docx
import pymupdf
import pytest

from trafficlaw.ingest.normalize import normalize_text
from trafficlaw.ingest.readers import (
    FOOTNOTE_PREFIX,
    ReaderError,
    ScannedPdfError,
    find_antiword,
    fix_lone_c2,
    read_doc,
    read_docx,
    read_pdf,
    read_source,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
LUAT36_DOC = REPO_ROOT / "data/raw/Luat/luat trật tự 36-2024-QH15.doc"


# --------------------------------------------------------------------------- .docx


def _make_docx(path: Path) -> None:
    d = docx.Document()
    d.add_paragraph("CHÍNH PHỦ")
    d.add_paragraph("Điều 1. Phạm vi điều chỉnh")
    t = d.add_table(rows=3, cols=3)
    a = t.cell(0, 0).merge(t.cell(0, 1))  # gộp ngang
    a.text = "Nơi nhận:"
    a.add_paragraph("- Như Điều 3;")
    t.cell(0, 2).text = "TM. CHÍNH PHỦ"
    t.cell(1, 0).merge(t.cell(2, 0)).text = "Gộp dọc"  # gộp dọc
    t.cell(1, 1).text = "b1"
    t.cell(1, 2).text = ""
    t.cell(2, 1).text = "c1"
    t.cell(2, 2).text = "c2"
    d.add_paragraph("Điều 2. Hiệu lực thi hành")
    d.save(str(path))


def test_docx_keeps_paragraph_table_order(tmp_path: Path) -> None:
    p = tmp_path / "văn bản.docx"
    _make_docx(p)
    raw = read_docx(p)
    assert raw.reader == "docx"
    assert raw.text.split("\n") == [
        "CHÍNH PHỦ",
        "Điều 1. Phạm vi điều chỉnh",
        "Nơi nhận: - Như Điều 3; | TM. CHÍNH PHỦ",
        "Gộp dọc | b1",
        "c1 | c2",
        "Điều 2. Hiệu lực thi hành",
    ]


def test_docx_line_break_and_tab(tmp_path: Path) -> None:
    d = docx.Document()
    para = d.add_paragraph()
    run = para.add_run("Điều 1.")
    run.add_tab()
    run.add_text("Phạm vi")
    run.add_break()
    run.add_text("dòng hai")
    p = tmp_path / "a.docx"
    d.save(str(p))
    assert read_docx(p).text == "Điều 1.\tPhạm vi\ndòng hai"


_W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def _make_docx_with_footnotes(path: Path) -> None:
    """python-docx không có API chú thích → thêm ``word/footnotes.xml`` vào zip bằng tay."""
    import zipfile

    d = docx.Document()
    d.add_paragraph("Điều 3. Giải thích từ ngữ@@1@@")
    d.add_paragraph("1. Khoản một@@2@@ có chú thích.")
    d.add_paragraph("2. Khoản hai.")
    tmp = path.with_suffix(".tmp.docx")
    d.save(str(tmp))
    footnotes = (
        f'<w:footnotes xmlns:w="{_W_NS}">'
        '<w:footnote w:type="separator" w:id="-1"><w:p><w:r><w:separator/></w:r></w:p></w:footnote>'
        '<w:footnote w:type="continuationSeparator" w:id="0"><w:p><w:r>'
        "<w:continuationSeparator/></w:r></w:p></w:footnote>"
        '<w:footnote w:id="1"><w:p><w:r><w:t>Điều này được sửa đổi.</w:t></w:r></w:p></w:footnote>'
        '<w:footnote w:id="2"><w:p><w:r><w:t>Khoản này được bổ sung</w:t></w:r></w:p>'
        "<w:p><w:r><w:t>theo Luật số 118/2025/QH15.</w:t></w:r></w:p></w:footnote>"
        "</w:footnotes>"
    )
    rel = (
        '<Relationship Id="rIdFn" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
        'relationships/footnotes" Target="footnotes.xml"/>'
    )
    ctype = (
        '<Override PartName="/word/footnotes.xml" ContentType="application/'
        'vnd.openxmlformats-officedocument.wordprocessingml.footnotes+xml"/>'
    )
    with zipfile.ZipFile(tmp) as zin, zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/document.xml":
                s = data.decode()
                for n in (1, 2):
                    s = s.replace(
                        f"@@{n}@@",
                        f'</w:t></w:r><w:r><w:footnoteReference w:id="{n}"/></w:r>'
                        '<w:r><w:t xml:space="preserve">',
                    )
                data = s.encode()
            elif item.filename == "word/_rels/document.xml.rels":
                data = data.replace(b"</Relationships>", rel.encode() + b"</Relationships>")
            elif item.filename == "[Content_Types].xml":
                data = data.replace(b"</Types>", ctype.encode() + b"</Types>")
            zout.writestr(item, data)
        zout.writestr("word/footnotes.xml", footnotes)
    tmp.unlink()


def test_docx_footnotes_synthetic(tmp_path: Path) -> None:
    p = tmp_path / "vbhn.docx"
    _make_docx_with_footnotes(p)
    raw = read_docx(p)
    assert raw.text.split("\n") == [
        "Điều 3. Giải thích từ ngữ[^1]",
        "[^1] Điều này được sửa đổi.",
        "1. Khoản một[^2] có chú thích.",
        "[^2] Khoản này được bổ sung theo Luật số 118/2025/QH15.",
        "2. Khoản hai.",
    ]
    assert not raw.warnings


def test_docx_footnotes_real_vbhn(tmp_path: Path) -> None:
    """VBHN 144 thật (nếu có file raw): chú thích nằm ngay sau đoạn chứa tham chiếu."""
    src = REPO_ROOT / "data/raw/VBHopNhat/2026_528-VBHN_144_2026_VBHN-LQ-VPQH.docx"
    if not src.is_file():
        pytest.skip("không có file raw VBHN 144")
    raw = read_docx(src)
    text = normalize_text(raw.text, source="word").text
    lines = text.split("\n")
    refs = [ln for ln in lines if "[^1]" in ln and not ln.startswith("[^1]")]
    notes = [ln for ln in lines if ln.startswith("[^1] ")]
    assert refs and len(notes) == 1
    assert lines.index(notes[0]) == lines.index(refs[0]) + 1  # chú thích ngay sau đoạn
    assert not raw.warnings


_NUMBERING_XML = f"""<w:numbering xmlns:w="{_W_NS}">
<w:abstractNum w:abstractNumId="0">
 <w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="decimal"/><w:lvlText w:val="%1."/></w:lvl>
 <w:lvl w:ilvl="1"><w:start w:val="1"/><w:numFmt w:val="lowerLetter"/>
  <w:lvlText w:val="%2)"/></w:lvl>
</w:abstractNum>
<w:abstractNum w:abstractNumId="1">
 <w:lvl w:ilvl="0"><w:start w:val="1"/><w:numFmt w:val="bullet"/><w:lvlText w:val="-"/></w:lvl>
</w:abstractNum>
<w:num w:numId="1"><w:abstractNumId w:val="0"/></w:num>
<w:num w:numId="2"><w:abstractNumId w:val="0"/>
 <w:lvlOverride w:ilvl="0"><w:startOverride w:val="5"/></w:lvlOverride></w:num>
<w:num w:numId="3"><w:abstractNumId w:val="1"/></w:num>
</w:numbering>"""


def _numbered(d: docx.document.Document, text: str, num_id: int | None, ilvl: int = 0) -> None:
    from docx.oxml import parse_xml

    p = d.add_paragraph(text)
    if num_id is not None:
        p._p.get_or_add_pPr().append(
            parse_xml(
                f'<w:numPr xmlns:w="{_W_NS}"><w:ilvl w:val="{ilvl}"/>'
                f'<w:numId w:val="{num_id}"/></w:numPr>'
            )
        )


def test_docx_auto_numbering_rendered(tmp_path: Path) -> None:
    """TT38/TT12/TT14: Khoản/Điểm đánh số tự động (``w:numPr``) phải có nhãn trong text."""
    from docx.oxml import parse_xml

    d = docx.Document()
    d.part.numbering_part._element = parse_xml(_NUMBERING_XML)
    _numbered(d, "Điều 5. Tốc độ thiết kế", None)
    _numbered(d, "Tốc độ thiết kế của đường bộ.", 1)
    _numbered(d, "Tốc độ thiết kế đường cao tốc:", 1)
    _numbered(d, "Đường đô thị;", 1, ilvl=1)
    _numbered(d, "Đường nông thôn.", 1, ilvl=1)
    _numbered(d, "Khoản ba.", 1)
    _numbered(d, "Khoản ba sau điểm: a) lại đếm từ đầu.", 1, ilvl=1)
    _numbered(d, "Bắt đầu từ 5.", 2)
    _numbered(d, "Gạch đầu dòng không có nhãn.", 3)
    p = tmp_path / "num.docx"
    d.save(str(p))
    raw = read_docx(p)
    assert raw.text.split("\n") == [
        "Điều 5. Tốc độ thiết kế",
        "1. Tốc độ thiết kế của đường bộ.",
        "2. Tốc độ thiết kế đường cao tốc:",
        "a) Đường đô thị;",
        "b) Đường nông thôn.",
        "3. Khoản ba.",
        "a) Khoản ba sau điểm: a) lại đếm từ đầu.",
        "5. Bắt đầu từ 5.",
        "Gạch đầu dòng không có nhãn.",
    ]
    assert raw.warnings == ["7 nhãn đánh số tự động (w:numPr)"]


def test_docx_auto_numbering_real_tt38() -> None:
    src = REPO_ROOT / "data/raw/ThongTu/Thông tư số 38.2024.TT-BGTVT.docx"
    if not src.is_file():
        pytest.skip("không có file raw TT 38/2024")
    lines = read_docx(src).text.split("\n")
    i = lines.index(next(ln for ln in lines if ln.startswith("Điều 5.")))
    assert [ln[:3] for ln in lines[i + 1 : i + 6]] == ["1. ", "2. ", "3. ", "4. ", "5. "]


# --------------------------------------------------------------------------- .pdf


def _make_pdf(path: Path, pages: list[tuple[str, str | None]]) -> None:
    """Mỗi trang: (HTML thân, HTML chú thích cuối trang | None)."""
    doc = pymupdf.open()
    for body, note in pages:
        page = doc.new_page()
        if body:
            page.insert_htmlbox(pymupdf.Rect(50, 40, 550, 650), body)
        if note:
            page.insert_htmlbox(pymupdf.Rect(50, 700, 550, 790), note)
    doc.save(str(path))


def test_pdf_with_text_layer(tmp_path: Path) -> None:
    p = tmp_path / "vb.pdf"
    body = (
        '<p style="font-size:14px">Điều 9. Các hành vi bị nghiêm cấm</p>'
        '<p style="font-size:14px">1. Điều khiển xe gắn máy trên đường bộ<sup>1</sup> '
        "khi không có giấy phép lái xe theo quy định của pháp luật hiện hành về trật tự, "
        "an toàn giao thông đường bộ.</p>"
    )
    note = (
        '<p style="font-size:10px"><span style="font-size:6px">1</span> Điểm này được sửa đổi.</p>'
    )
    _make_pdf(p, [(body, note), ('<p style="font-size:14px">Điều 10. Quy tắc chung</p>', None)])
    raw = read_pdf(p)
    assert raw.reader == "pymupdf" and raw.n_pages == 2
    assert "\f" in raw.text
    assert FOOTNOTE_PREFIX + "[^1] Điểm này được sửa đổi." in raw.text
    text = normalize_text(raw.text, source="pdf").text
    assert text.startswith("Điều 9. Các hành vi bị nghiêm cấm\n1. Điều khiển xe gắn máy")
    assert "đường bộ[^1] khi không có" in text
    assert "\n[^1] Điểm này được sửa đổi.\nĐiều 10. Quy tắc chung\n" in text


def test_pdf_blank_pages_are_scanned(tmp_path: Path) -> None:
    p = tmp_path / "scan.pdf"
    _make_pdf(p, [("", None), ("", None)])
    with pytest.raises(ScannedPdfError):
        read_pdf(p)
    with pytest.raises(ScannedPdfError):
        read_source(p)


# --------------------------------------------------------------------------- .doc


def test_fix_lone_c2() -> None:
    data = "vượt ".encode() + b"\xc2\r\n" + "xe ô tô".encode()
    fixed, n = fix_lone_c2(data)
    assert n == 1
    assert fixed.decode("utf-8") == "vượt  \r\nxe ô tô"


@pytest.mark.skipif(find_antiword() is None, reason="không có antiword")
@pytest.mark.skipif(not LUAT36_DOC.is_file(), reason="không có file raw Luật 36")
def test_doc_real_file_with_accented_path(tmp_path: Path) -> None:
    dst = tmp_path / "thư mục có dấu" / "luật trật tự 36.doc"
    dst.parent.mkdir()
    shutil.copyfile(LUAT36_DOC, dst)
    raw = read_doc(dst)
    assert raw.reader == "antiword"
    text = normalize_text(raw.text, source="word").text
    assert "�" not in text
    fixture = (REPO_ROOT / "tests/fixtures/luat36_dieu9.txt").read_text(encoding="utf-8")
    assert fixture in text


def test_doc_without_antiword(tmp_path: Path) -> None:
    p = tmp_path / "a.doc"
    p.write_bytes(b"x")
    with pytest.raises(ReaderError):
        read_doc(p, antiword=str(tmp_path / "khong-co-antiword"))


def test_unsupported_and_missing(tmp_path: Path) -> None:
    p = tmp_path / "a.rtf"
    p.write_text("x", encoding="utf-8")
    with pytest.raises(ReaderError, match="không hỗ trợ"):
        read_source(p)
    with pytest.raises(ReaderError, match="không thấy"):
        read_source(tmp_path / "missing.docx")


def test_extension_case_insensitive(tmp_path: Path) -> None:
    p = tmp_path / "A.DOCX"
    _make_docx(p)
    assert read_source(p).reader == "docx"
