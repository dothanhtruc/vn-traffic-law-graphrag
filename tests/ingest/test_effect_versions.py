"""M4: Điều hiệu lực (ngày chung/riêng) và tra cứu phiên bản (khoảng bao gồm hai đầu)."""

from __future__ import annotations

from datetime import date

from tests.ingest.m4_helpers import unit, units_of
from trafficlaw.ingest.effect import parse_effects
from trafficlaw.ingest.versions import UnitVersion, VersionStore, select_version


def test_nd168_dieu53_general_special_and_unclear() -> None:
    eff = parse_effects("ND168-2024", units_of("ND168-2024", "nd168_dieu53.txt"))
    assert eff.general == date(2025, 1, 1)
    assert eff.special == {
        "ND168-2024/D6/K3/m": date(2026, 1, 1),
        "ND168-2024/D26/K4/e": date(2026, 1, 1),
        "ND168-2024/D27/K1/b": date(2026, 1, 1),
    }
    # "điểm b khoản 1 Điều 32 … có hiệu lực thi hành theo quy định của pháp luật bảo vệ môi trường"
    assert [t.reason for t in eff.todos] == ["hieu_luc_khong_ro"]


def test_luat_special_effect_whole_dieu_and_earlier_date() -> None:
    units = [
        unit("LUAT35-2024/D85", "dieu", "Điều 85. Hiệu lực thi hành", title="Hiệu lực thi hành"),
        unit(
            "LUAT35-2024/D85/K2",
            "khoan",
            "2. Điểm a và điểm b khoản 2 Điều 42, Điều 43, Điều 50, khoản 1 Điều 84 của Luật này "
            "có hiệu lực thi hành từ ngày 01 tháng 10 năm 2024.",
        ),
    ]
    eff = parse_effects("LUAT35-2024", units)
    assert eff.special == {
        "LUAT35-2024/D42/K2/a": date(2024, 10, 1),
        "LUAT35-2024/D42/K2/b": date(2024, 10, 1),
        "LUAT35-2024/D43": date(2024, 10, 1),
        "LUAT35-2024/D50": date(2024, 10, 1),
        "LUAT35-2024/D84/K1": date(2024, 10, 1),
    }


def test_general_with_replacement_clause_and_qualified_special() -> None:
    units = [
        unit("TT72-2024-BCA/D28", "dieu", "Điều 28. Hiệu lực thi hành", title="Hiệu lực thi hành"),
        unit(
            "TT72-2024-BCA/D28/K1",
            "khoan",
            "1. Thông tư này có hiệu lực thi hành kể từ ngày 01 tháng 01 năm 2025 và thay thế "
            "Thông tư số 63/2020/TT-BCA ngày 19 tháng 6 năm 2020.",
        ),
        unit(
            "TT72-2024-BCA/D28/K2",
            "khoan",
            "2. Quy định xây dựng Cơ sở dữ liệu tại khoản 2 Điều 2 Thông tư này có hiệu lực thi "
            "hành từ ngày 01 tháng 7 năm 2027.",
        ),
    ]
    eff = parse_effects("TT72-2024-BCA", units)
    assert eff.general == date(2025, 1, 1)
    # "Quy định xây dựng … tại" không phải dẫn chiếu thuần → không đoán phạm vi
    assert not eff.special and [t.reason for t in eff.todos] == ["hieu_luc_khong_ro"]


def _v(version: int, start: date | None, end: date | None, status: str = "active") -> UnitVersion:
    return UnitVersion(
        unit_id="X1-2024/D1",
        version=version,
        text="" if status == "repealed" else f"v{version}",
        effective_from=start,
        effective_to=end,
        status=status,  # type: ignore[arg-type]
    )


def test_select_version_inclusive_bounds() -> None:
    vs = [_v(0, date(2025, 1, 1), date(2026, 6, 30), "amended"), _v(1, date(2026, 7, 1), None)]
    assert select_version(vs, date(2024, 12, 31)) is None
    assert select_version(vs, date(2025, 1, 1)).version == 0  # type: ignore[union-attr]
    assert select_version(vs, date(2026, 6, 30)).version == 0  # type: ignore[union-attr]
    assert select_version(vs, date(2026, 7, 1)).version == 1  # type: ignore[union-attr]


def test_missing_start_date_never_in_effect_and_repealed_hidden() -> None:
    assert select_version([_v(0, None, None)], date(2026, 1, 1)) is None
    vs = [
        _v(0, date(2025, 1, 1), date(2025, 8, 31), "amended"),
        _v(1, date(2025, 9, 1), None, "repealed"),
    ]
    st = VersionStore(vs)
    assert st.get_version("X1-2024/D1", date(2025, 9, 1)) is None
    rep = st.get_version("X1-2024/D1", date(2025, 9, 1), include_repealed=True)
    assert rep is not None and rep.status == "repealed"
    assert st.get_version("KHONG-CO/D1", date(2025, 9, 1)) is None
