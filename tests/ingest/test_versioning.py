"""M4: áp chỉ dẫn → phiên bản; ``get_version`` ở 4 mốc 01/01/2025, 01/01/2026, 01/07/2026,
15/08/2026 (trước và sau mỗi mốc) trên trích đoạn văn bản thật."""

from __future__ import annotations

from datetime import date

import pytest

from tests.ingest.m4_helpers import registry, units_of
from trafficlaw.ingest.amendments import extract_instructions
from trafficlaw.ingest.effect import parse_effects
from trafficlaw.ingest.versioning import Repeal, build_versions
from trafficlaw.ingest.versions import VersionStore

REG = registry()
BEFORE_AFTER = [
    date(2024, 12, 31),
    date(2025, 1, 1),
    date(2025, 12, 31),
    date(2026, 1, 1),
    date(2026, 6, 30),
    date(2026, 7, 1),
    date(2026, 8, 14),
    date(2026, 8, 15),
]


def _versions_nd168():  # type: ignore[no-untyped-def]
    base = units_of("ND168-2024", "nd168_dieu6_k1_k3.txt", "nd168_dieu53.txt")
    eff = parse_effects("ND168-2024", base)
    amend = units_of("ND238-2026", "nd238_dieu1_2.txt", "nd238_dieu18_20.txt")
    ex = extract_instructions(REG["ND238-2026"], amend, REG)
    return build_versions(REG["ND168-2024"], base, ex.instructions, special=eff.special), eff


def _versions_nd165():  # type: ignore[no-untyped-def]
    base = units_of("ND165-2024", "nd165_dieu4.txt", "nd165_dieu6.txt", "nd165_dieu17.txt")
    amend = units_of("ND241-2026", "nd241_dieu1.txt", "nd241_dieu25_26.txt")
    ex = extract_instructions(REG["ND241-2026"], amend, REG)
    return build_versions(REG["ND165-2024"], base, ex.instructions)


def _at(store: VersionStore, uid: str) -> list[int | None]:
    out: list[int | None] = []
    for d in BEFORE_AFTER:
        v = store.get_version(uid, d)
        out.append(None if v is None else v.version)
    return out


def test_nd168_special_effect_and_nd238_amendment_at_four_dates() -> None:
    res, eff = _versions_nd168()
    assert eff.general == date(2025, 1, 1)
    assert eff.special["ND168-2024/D6/K3/m"] == date(2026, 1, 1)
    st = VersionStore(res.versions)
    # điểm m khoản 3 Điều 6: chưa có hiệu lực trước 01/01/2026; ND238 sửa từ 15/08/2026
    assert _at(st, "ND168-2024/D6/K3/m") == [None, None, None, 0, 0, 0, 0, 1]
    m = st.versions_of("ND168-2024/D6/K3/m")
    assert m[0].effective_to == date(2026, 8, 14) and m[0].status == "amended"
    assert m[1].source_unit_id == "ND238-2026/D2/K2" and m[1].status == "active"
    # khoản 3 (cha) có hiệu lực từ 01/01/2025, không đổi
    assert _at(st, "ND168-2024/D6/K3") == [None, 0, 0, 0, 0, 0, 0, 0]
    # khoản 1a bổ sung "vào trước khoản 1"
    assert _at(st, "ND168-2024/D6/K1a") == [None] * 7 + [1]
    [k1a] = [a for a in res.added if a.id == "ND168-2024/D6/K1a"]
    assert (k1a.before_id, k1a.after_id, k1a.parent_id) == (
        "ND168-2024/D6/K1",
        None,
        "ND168-2024/D6",
    )


def test_nd238_adds_khoan_to_effect_article() -> None:
    res, _ = _versions_nd168()
    st = VersionStore(res.versions)
    assert st.get_version("ND168-2024/D53/K3", date(2026, 8, 15)) is not None
    k2 = st.get_version("ND168-2024/D53/K2", date(2026, 8, 15))
    assert k2 is not None and "điểm m khoản 3 Điều 6," not in k2.text  # ND238 Đ19 K15
    k1 = st.get_version("ND168-2024/D53/K1", date(2026, 8, 15))
    assert k1 is not None and "khoản 2, khoản 3, khoản 4 Điều này" in k1.text  # Đ19 K9


def test_nd241_replaces_whole_dieu4_of_nd165() -> None:
    res = _versions_nd165()
    st = VersionStore(res.versions)
    d4 = st.get_version("ND165-2024/D4", date(2026, 7, 1))
    assert d4 is not None and d4.text.startswith("Điều 4. Phân cấp để Ủy ban nhân dân")
    assert st.get_version("ND165-2024/D4", date(2026, 6, 30)).version == 0  # type: ignore[union-attr]
    # điểm a khoản 2 cũ không còn trong Điều 4 mới → bãi bỏ từ 01/07/2026
    assert _at(st, "ND165-2024/D4/K2/a") == [None, 0, 0, 0, 0, None, None, None]
    rep = st.get_version("ND165-2024/D4/K2/a", date(2026, 7, 1), include_repealed=True)
    assert rep is not None and rep.status == "repealed" and rep.text == ""
    # khoản 7, 8 mới
    assert {a.id for a in res.added} >= {"ND165-2024/D4/K7", "ND165-2024/D4/K8/a"}


def test_nd241_phrase_replacement_and_repeal() -> None:
    res = _versions_nd165()
    st = VersionStore(res.versions)
    old = st.get_version("ND165-2024/D6/K1", date(2026, 6, 30))
    new = st.get_version("ND165-2024/D6/K1", date(2026, 7, 1))
    assert old is not None and "Bộ Giao thông vận tải" in old.text
    assert new is not None and "Bộ Xây dựng" in new.text and "Bộ Giao thông vận tải" not in new.text
    assert new.source_unit_id == "ND241-2026/D25/K1"
    assert _at(st, "ND165-2024/D17/K1/d")[-3:] == [None, None, None]
    # các vị trí ngoài trích đoạn → todo không tìm thấy đích, không đoán
    assert any(t.reason == "khong_tim_thay_dich" for t in res.todos)


def test_unchanged_children_get_no_new_version() -> None:
    res = _versions_nd165()
    changed = {v.unit_id for v in res.versions if v.version > 0}
    assert "ND165-2024/D6" not in changed  # tiêu đề Điều 6 không đổi


def test_full_repeal_closes_every_unit() -> None:
    base = units_of("TT35-2024-BGTVT", "tt35_phan_chuong.txt")
    res = build_versions(
        REG["TT35-2024-BGTVT"], base, [], repeal=Repeal(date(2025, 9, 1), "TT14-2025-BXD/D33/K2")
    )
    st = VersionStore(res.versions)
    for u in base:
        assert st.get_version(u.id, date(2025, 8, 31)) is not None
        assert st.get_version(u.id, date(2025, 9, 1)) is None
        last = st.versions_of(u.id)[-1]
        assert last.status == "repealed" and last.source_unit_id == "TT14-2025-BXD/D33/K2"


@pytest.mark.parametrize("op", ["insert"])
def test_insert_existing_unit_is_todo(op: str) -> None:
    base = units_of("ND168-2024", "nd168_dieu6_k1_k3.txt")
    amend = units_of("ND238-2026", "nd238_dieu1_2.txt")
    ex = extract_instructions(REG["ND238-2026"], amend, REG)
    ins = next(i for i in ex.instructions if i.op == op)
    dup = ins.model_copy(update={"target_id": "ND168-2024/D6/K1", "seq": 999})
    res = build_versions(REG["ND168-2024"], base, [dup])
    assert [t.reason for t in res.todos] == ["dich_da_ton_tai"]


def test_delay_moves_amendment_version_start() -> None:
    from trafficlaw.ingest.versioning import Delay

    base = units_of("ND168-2024", "nd168_dieu6_k1_k3.txt")
    amend = units_of("ND238-2026", "nd238_dieu1_2.txt")
    ex = extract_instructions(REG["ND238-2026"], amend, REG)
    delays = [
        Delay("ND168-2024/D6/K3/m", "ND238-2026", date(2028, 1, 1), "X"),
        Delay("ND168-2024/D6/K1a", "ND238-2026", date(2029, 1, 1), "X"),
        Delay("ND168-2024/D99", "ND238-2026", date(2029, 1, 1), "X"),
    ]
    res = build_versions(REG["ND168-2024"], base, ex.instructions, delays=delays)
    st = VersionStore(res.versions)
    m = st.versions_of("ND168-2024/D6/K3/m")
    assert (m[0].effective_to, m[1].effective_from) == (date(2027, 12, 31), date(2028, 1, 1))
    assert st.get_version("ND168-2024/D6/K1a", date(2028, 12, 31)) is None
    assert st.get_version("ND168-2024/D6/K1a", date(2029, 1, 1)) is not None
    assert [t.reason for t in res.todos if t.unit_id == "ND168-2024/D99"] == ["khong_tim_thay_dich"]
