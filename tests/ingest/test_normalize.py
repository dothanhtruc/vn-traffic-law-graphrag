import unicodedata
from pathlib import Path

import pytest

from trafficlaw.ingest.normalize import (
    count_dieu_headings,
    find_so_hieu,
    has_dieu_1,
    normalize_text,
    should_join,
    single_char_token_ratio,
)
from trafficlaw.ingest.readers import FOOTNOTE_PREFIX as FN

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def _fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def _wrap(text: str, width: int = 70) -> str:
    """Giả lập PDF: ngắt mỗi dòng thành nhiều dòng in ~``width`` ký tự (theo từ)."""
    out: list[str] = []
    for line in text.split("\n"):
        cur = ""
        for word in line.split(" "):
            if cur and len(cur) + 1 + len(word) > width:
                out.append(cur + " ")  # PyMuPDF để lại dấu cách cuối dòng
                cur = word
            else:
                cur = f"{cur} {word}" if cur else word
        out.append(cur)
    return "\n".join(out)


# --------------------------------------------------------------------------- phần chung


def test_nfd_to_nfc() -> None:
    nfd = unicodedata.normalize("NFD", "Điều 9. Các hành vi bị nghiêm cấm")
    assert nfd != unicodedata.normalize("NFC", nfd)
    res = normalize_text(nfd, source="word")
    assert res.text == "Điều 9. Các hành vi bị nghiêm cấm\n"
    assert unicodedata.is_normalized("NFC", res.text)


def test_special_spaces_and_invisible_chars() -> None:
    raw = "Điều 1. Phạm vi​ điều­chỉnh﻿\x07  \r\nLuật\t này quy định"
    res = normalize_text(raw, source="word")
    assert res.text == "Điều 1. Phạm vi điềuchỉnh\nLuật này quy định\n"


def test_line_endings_whitespace_blank_lines() -> None:
    raw = "  a  b   \r\n\r\n\r\n\r\n   c\rd\f e \n\n\n"
    assert normalize_text(raw, source="word").text == "a b\n\nc\nd\ne\n"


def test_word_does_not_join_lines() -> None:
    raw = "Điều 1. Phạm vi\nđiều chỉnh của\nLuật này"
    assert normalize_text(raw, source="word").text == raw + "\n"


def test_antiword_table_row() -> None:
    raw = "|CHÍNH PHỦ          |CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM |\n|          |Độc lập - Tự do |"
    res = normalize_text(raw, source="word")
    assert res.text == "CHÍNH PHỦ | CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\nĐộc lập - Tự do\n"


def test_replacement_and_symbol_chars_kept_and_counted() -> None:
    raw = "xe � mô tô  gắn máy �"
    res = normalize_text(raw, source="word")
    assert res.text.count("�") == 2 and "" in res.text
    assert res.n_replacement_chars == 2
    assert res.n_symbol_chars == 1
    assert any("U+FFFD" in w for w in res.warnings)
    assert any("symbol" in w for w in res.warnings)


def test_real_fixtures_are_fixed_points() -> None:
    for name in ("luat36_dieu9.txt", "nd168_dieu6_k1_k3.txt"):
        text = _fixture(name)
        assert normalize_text(text, source="word").text == text


# --------------------------------------------------------------------------- PDF


@pytest.mark.parametrize(
    "nxt",
    [
        "Điều 10. Quy tắc chung",
        "Điều 6a. Điều bổ sung",
        "1. Người tham gia giao thông",
        "12. Tai nạn giao thông",
        "a) Không chấp hành hiệu lệnh",
        "đ) Sử dụng còi",
        "đ1) Điểm bổ sung",
        "18.[^6] Làm gián đoạn hoạt động",
        "18a.[^7] Sử dụng dữ liệu",
        "c)[^3] Cơ sở dữ liệu",
        "Chương II",
        "Mục 2. ĐƯỜNG CAO TỐC",
        "[^3] Điểm này được sửa đổi",
        "- Như Điều 3;",
        "QUY TẮC GIAO THÔNG ĐƯỜNG BỘ",
    ],
)
def test_pdf_never_joins_before_protected_lines(nxt: str) -> None:
    assert not should_join("điều khiển xe chạy quá tốc độ quy định", nxt)
    res = normalize_text(f"điều khiển xe chạy quá tốc độ quy định \n{nxt}", source="pdf")
    assert res.text.split("\n")[1] == nxt


def test_pdf_join_rules() -> None:
    assert should_join("phương tiện giao thông", "đường bộ đi lại.")
    assert should_join("theo", "Luật số 118/2025/QH15")  # tên riêng giữa câu
    assert should_join("bao gồm:", "người điều khiển xe cơ giới")
    assert not should_join("bao gồm:", "Cảnh sát giao thông")
    assert not should_join("an toàn giao thông.", "bộ phận")
    # Tiêu đề Điều xuống dòng: chỉ nối phần tiếp chữ thường.
    assert should_join("Điều 47. Bảo đảm trật tự trong vận chuyển", "hành khách, hàng hóa")
    assert not should_join("Điều 1. Phạm vi điều chỉnh", "Luật này quy định về quy tắc")
    assert not should_join("Chương I", "NHỮNG QUY ĐỊNH CHUNG")
    assert not should_join("", "abc") and not should_join("abc", "")
    # "Chương/Phụ lục/Phần …" giữa câu, rơi vào đầu dòng in → vẫn nối.
    assert should_join(
        "vi phạm quy tắc giao thông đường bộ quy định tại", "Chương II của Luật này."
    )
    assert should_join("theo Mẫu số 01", "Phụ lục I ban hành kèm theo Thông tư này.")
    assert should_join("đi trên", "Phần đường xe chạy")
    assert not should_join("Thông tư này.", "PHỤ LỤC I")
    assert not should_join("Luật này.", "Phần thứ hai")


def test_pdf_rejoins_wrapped_real_fixture() -> None:
    text = _fixture("luat36_dieu9.txt")
    res = normalize_text(_wrap(text), source="pdf")
    assert res.text == text
    assert res.n_lines_joined > 0


def test_pdf_rejoins_wrapped_points_with_d() -> None:
    text = _fixture("nd168_dieu6_k1_k3.txt")
    assert normalize_text(_wrap(text, 60), source="pdf").text == text


def test_pdf_drops_page_numbers_and_signature_lines() -> None:
    pages = [
        "Người ký: CỤC THÔNG TIN\nEmail: x@chinhphu.vn\nCơ quan: VĂN PHÒNG\n"
        "Thời gian ký: 28.08.2026\nĐiều 1. Phạm vi\n1. Nội dung khoản",
        "2\nmột của trang trước.\n2. Khoản hai | 02",
        "3\n3. Khoản ba.\n02",  # "02" ở cuối trang không khớp số trang → giữ
    ]
    res = normalize_text("\f".join(pages), source="pdf")
    assert res.text == (
        "Điều 1. Phạm vi\n1. Nội dung khoản một của trang trước.\n2. Khoản hai | 02\n"
        "3. Khoản ba.\n02\n"
    )
    assert res.n_page_numbers_removed == 2
    assert res.n_signature_lines_removed == 4


def test_pdf_footnotes_moved_after_paragraph_split_across_pages() -> None:
    page1 = (
        "Quốc hội ban hành Luật này[^1].\n"
        "1. Đoạn văn bị ngắt qua\n \n"
        f"{FN}[^1] Luật số 118/2025/QH15 sửa đổi, bổ sung\n"
        f"{FN}một số điều."
    )
    page2 = "2\ntrang sau và kết thúc ở đây.\n2. Khoản tiếp theo."
    res = normalize_text(page1 + "\f" + page2, source="pdf")
    assert res.text == (
        "Quốc hội ban hành Luật này[^1].\n"
        "1. Đoạn văn bị ngắt qua trang sau và kết thúc ở đây.\n"
        "[^1] Luật số 118/2025/QH15 sửa đổi, bổ sung một số điều.\n"
        "2. Khoản tiếp theo.\n"
    )


def test_pdf_footnote_continued_on_next_page() -> None:
    page1 = f"1. Khoản một.\n{FN}[^1] Chú thích dài phần"
    page2 = f"2\n2. Khoản hai.\n{FN}đầu tràn sang trang sau.\n{FN}[^2] Chú thích hai."
    res = normalize_text(page1 + "\f" + page2, source="pdf")
    assert res.text == (
        "1. Khoản một.\n[^1] Chú thích dài phần đầu tràn sang trang sau.\n"
        "2. Khoản hai.\n[^2] Chú thích hai.\n"
    )


def test_pdf_keeps_replacement_char() -> None:
    res = normalize_text("xe � mô tô\ngắn máy", source="pdf")
    assert res.text == "xe � mô tô gắn máy\n"
    assert res.n_replacement_chars == 1


# --------------------------------------------------------------------------- đo đạc


def test_counts_on_real_fixture() -> None:
    text = _fixture("nd168_dieu6_k1_k3.txt")
    assert count_dieu_headings(text) == 1
    assert not has_dieu_1(text)
    assert has_dieu_1("Chương I\nĐiều 1. Phạm vi")
    assert not has_dieu_1("theo Điều 1. Phạm vi")  # không ở đầu dòng
    assert count_dieu_headings("Điều 6a. X\nĐiều 7. Y\nxem Điều 8. Z") == 2


def test_single_char_ratio() -> None:
    assert single_char_token_ratio("") == 0.0
    split = "Đi ề u 9 . C á c h à nh vi b ị nghi ê m c ấ m đ ến"
    assert single_char_token_ratio(split) > 0.3
    # Nhãn Điểm và "ô" không bị tính.
    labels = "điểm a, điểm b, c và d khoản 3; a) xe ô tô; đ) xe ô tô con"
    assert single_char_token_ratio(labels) == 0.0
    assert single_char_token_ratio(_fixture("luat36_dieu9.txt")) < 0.05


@pytest.mark.parametrize(
    ("text", "so_hieu", "found"),
    [
        ("Số: 168/2024/NĐ-CP", "168/2024/NĐ-CP", True),
        ("Số: 168 / 2024 / NĐ - CP", "168/2024/NĐ-CP", True),
        ("Số: 168/2024/ND-CP", "168/2024/NĐ-CP", True),
        ("Số: 79/2024/TT- BCA", "79/2024/TT-BCA", True),
        ("Số: 19/2024/qđ-ttg", "19/2024/QĐ-TTg", True),
        ("Số: 168/2024/NĐ-CP", "68/2024/NĐ-CP", False),  # không khớp giữa số
        ("Số:     /2024/TT-BGTVT", "52/2024/TT-BGTVT", False),
        ("bất kỳ", None, False),
    ],
)
def test_find_so_hieu(text: str, so_hieu: str | None, found: bool) -> None:
    assert find_so_hieu(text, so_hieu) is found
