import unicodedata

import pytest

from trafficlaw.utils.ids import UnitId, is_valid_unit_id, make_unit_id, parent_id, parse_unit_id


@pytest.mark.parametrize(
    ("s", "level"),
    [
        ("ND168-2024/D6/K4/a", "diem"),
        ("LUAT36-2024/D9/K2", "khoan"),
        ("TT12-2025-BCA/D3", "dieu"),
        ("VBHN55-VPQH", "van_ban"),
        ("TT38-2024-BGTVT/D7/K1/đ", "diem"),
        ("ND168-2024/D6/K4/đ1", "diem"),
        ("LUAT35-2024/D6a/K2a/a1", "diem"),
        ("LUAT36-2024/D3/b", "diem"),  # Điều không chia Khoản
    ],
)
def test_round_trip(s: str, level: str) -> None:
    uid = parse_unit_id(s)
    assert str(uid) == s
    assert uid.level == level


def test_make_unit_id() -> None:
    assert make_unit_id("ND168-2024", 6, 4, "a") == "ND168-2024/D6/K4/a"
    assert make_unit_id("nd168-2024", "6", None, "A") == "ND168-2024/D6/a"
    assert make_unit_id("LUAT36-2024") == "LUAT36-2024"


def test_nfc_and_whitespace() -> None:
    assert make_unit_id(" ND168-2024 ", " 6 ", 4, " Đ ") == "ND168-2024/D6/K4/đ"
    decomposed = unicodedata.normalize("NFD", "ND168-2024/D6/K4/đ")
    assert str(parse_unit_id(decomposed)) == "ND168-2024/D6/K4/đ"


def test_parent_chain() -> None:
    assert parent_id("ND168-2024/D6/K4/a") == "ND168-2024/D6/K4"
    assert parent_id("ND168-2024/D6/K4") == "ND168-2024/D6"
    assert parent_id("LUAT36-2024/D3/b") == "LUAT36-2024/D3"
    assert parent_id("ND168-2024/D6") == "ND168-2024"
    assert parent_id("ND168-2024") is None


@pytest.mark.parametrize(
    "s",
    [
        "",
        "nd168-2024/D6",  # mã VB chữ thường
        "ND168-2024/D",  # thiếu số Điều
        "ND168-2024/K4",  # Khoản không có Điều
        "ND168-2024/a",  # Điểm không có Điều
        "ND168-2024/D6/K4/a/b",  # thừa cấp
        "ND168-2024/D6/K4/ab",  # điểm sai
        "ND168-2024/D6/K4/ă",  # chữ có dấu không phải ký hiệu điểm
    ],
)
def test_invalid(s: str) -> None:
    assert not is_valid_unit_id(s)
    with pytest.raises(ValueError):
        parse_unit_id(s)


def test_unit_id_validates_on_construct() -> None:
    with pytest.raises(ValueError):
        UnitId("ND168-2024", khoan="4")


# --- M3: mã khung (Phần/Chương/Mục) và Phụ lục ---


@pytest.mark.parametrize(
    ("s", "level", "parent"),
    [
        ("TT35-2024-BGTVT/P1", "phan", "TT35-2024-BGTVT"),
        ("TT35-2024-BGTVT/P2/C1", "chuong", "TT35-2024-BGTVT/P2"),
        ("LUAT36-2024/C2", "chuong", "LUAT36-2024"),
        ("ND168-2024/C2/M1", "muc", "ND168-2024/C2"),
        ("TT35-2024-BGTVT/P2/C1/M3", "muc", "TT35-2024-BGTVT/P2/C1"),
        ("TT53-2024-BGTVT/PL1", "phu_luc", "TT53-2024-BGTVT"),
        ("ND184-2025/PL1-2", "phu_luc", "ND184-2025"),
        ("VBHN65-2026-BXD/D52a", "dieu", "VBHN65-2026-BXD"),
        ("VBHN55-VPQH/D9/K18a", "khoan", "VBHN55-VPQH/D9"),
    ],
)
def test_frame_round_trip(s: str, level: str, parent: str) -> None:
    uid = parse_unit_id(s)
    assert str(uid) == s
    assert uid.level == level
    assert parent_id(s) == parent


def test_make_frame_and_appendix() -> None:
    from trafficlaw.utils.ids import make_appendix_id, make_frame_id

    assert make_frame_id("TT35-2024-BGTVT", phan=2, chuong=1) == "TT35-2024-BGTVT/P2/C1"
    assert make_frame_id("ND168-2024", chuong="2", muc=1) == "ND168-2024/C2/M1"
    assert make_appendix_id("tt53-2024-bgtvt", 1) == "TT53-2024-BGTVT/PL1"


@pytest.mark.parametrize(
    "s",
    [
        "LUAT36-2024/C2/D9",  # mã Điều không chứa Chương
        "ND168-2024/M1/C2",  # sai thứ tự
        "ND168-2024/C",  # thiếu số
        "ND168-2024/PL",  # thiếu số Phụ lục
        "ND168-2024/PL1/D2",  # Phụ lục không chứa Điều
        "ND168-2024/C2/PL1",
        "ND168-2024/CII",  # La Mã phải đổi sang số Ả Rập
        "ND168-2024/C2/K1",
    ],
)
def test_frame_invalid(s: str) -> None:
    assert not is_valid_unit_id(s)


@pytest.mark.parametrize(
    ("roman", "n"), [("I", 1), ("IV", 4), ("IX", 9), ("XIV", 14), ("XL", 40), ("VII", 7)]
)
def test_roman_to_int(roman: str, n: int) -> None:
    from trafficlaw.utils.ids import roman_to_int

    assert roman_to_int(roman) == n


@pytest.mark.parametrize("bad", ["", "IIII", "iv", "VX", "ABC"])
def test_roman_invalid(bad: str) -> None:
    from trafficlaw.utils.ids import roman_to_int

    with pytest.raises(ValueError):
        roman_to_int(bad)
