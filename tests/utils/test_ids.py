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
