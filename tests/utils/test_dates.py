import unicodedata
from datetime import date

import pytest

from trafficlaw.utils.dates import (
    DATA_CUTOFF,
    day_before,
    in_effect,
    parse_iso,
    parse_vn_date,
    to_iso,
)

# Các mốc sửa đổi dùng trong test (CLAUDE.md mục 7).
MILESTONES = [date(2025, 1, 1), date(2026, 1, 1), date(2026, 7, 1), date(2026, 8, 15)]


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("ngày 15 tháng 11 năm 2024", date(2024, 11, 15)),
        ("Ngày 01 tháng 01 năm 2026", date(2026, 1, 1)),
        ("15 tháng 8 năm 2026", date(2026, 8, 15)),
        ("ngày  1  tháng 7   năm 2026.", date(2026, 7, 1)),
        ("15/11/2024", date(2024, 11, 15)),
        ("15-11-2024", date(2024, 11, 15)),
        ("01.01.2026", date(2026, 1, 1)),
        ("2024-11-15", date(2024, 11, 15)),
        (unicodedata.normalize("NFD", "ngày 3 tháng 11 năm 2026"), DATA_CUTOFF),
    ],
)
def test_parse_vn_date(s: str, expected: date) -> None:
    assert parse_vn_date(s) == expected


@pytest.mark.parametrize("s", ["", "tháng 11 năm 2024", "32/01/2025", "29/02/2025", "2024/11/15"])
def test_parse_vn_date_invalid(s: str) -> None:
    with pytest.raises(ValueError):
        parse_vn_date(s)


def test_iso_round_trip() -> None:
    assert to_iso(date(2026, 8, 15)) == "2026-08-15"
    assert parse_iso("2026-08-15") == date(2026, 8, 15)
    assert to_iso(None) is None
    assert parse_iso(None) is None
    assert parse_iso("") is None
    with pytest.raises(ValueError):
        parse_iso("15/08/2026")


@pytest.mark.parametrize("m", MILESTONES)
def test_in_effect_around_milestone(m: date) -> None:
    # Bản cũ hết hiệu lực ngày m-1, bản mới có hiệu lực từ m.
    old = (date(2024, 1, 1), day_before(m))
    new = (m, None)
    before, after = day_before(m), m
    assert in_effect(before, *old) and not in_effect(before, *new)
    assert in_effect(after, *new) and not in_effect(after, *old)
    # Đúng một phiên bản có hiệu lực tại mọi ngày.
    for d in (before, after, DATA_CUTOFF):
        assert in_effect(d, *old) + in_effect(d, *new) == 1


def test_in_effect_edges() -> None:
    assert not in_effect(date(2024, 12, 31), date(2025, 1, 1), None)
    assert in_effect(date(2025, 1, 1), date(2025, 1, 1), date(2025, 1, 1))
    assert not in_effect(date(2025, 1, 1), None, None)  # thiếu ngày → không tự coi là hiệu lực
