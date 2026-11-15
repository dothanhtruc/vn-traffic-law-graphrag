"""verify/numbers.py: bảng con số (CheTai/DiemGPLX theo phiên bản, 4 mốc), số kiểu VN, định dạng
VND, chỗ giữ chỗ, dò số không kiểm được."""

from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from trafficlaw.graph.embedded import EmbeddedStore
from trafficlaw.graph.store import GraphNode
from trafficlaw.retrieval.catalog import ChunkCatalog
from trafficlaw.verify.numbers import (
    AllowedNumbers,
    NumberIndex,
    SourceText,
    build_number_table,
    dates_in,
    drop_sentences,
    find_unverified_numbers,
    format_count,
    format_int_vn,
    parse_numbers,
    placeholders,
    render_numbers,
    text_numbers,
    unknown_placeholders,
)

K3 = "ND168-2024/D6/K3"


def _chunk_at(cat: ChunkCatalog, unit: str, d: date):
    got = [c for c in cat.chunks if c.unit_id == unit and c.covers(d)]
    assert len(got) <= 1
    return got[0] if got else None


def _table(store: EmbeddedStore, cat: ChunkCatalog, unit: str, d: date, **kw):
    c = _chunk_at(cat, unit, d)
    assert c is not None, (unit, d)
    src = SourceText("S1", c.text, c.version_ids, d)
    return build_number_table([src], NumberIndex(store), **kw), c


def test_vn_number_parsing_and_format() -> None:
    assert parse_numbers("phạt 400.000 đồng, 0,25 mét, 02 điểm") == {
        Decimal(400000),
        Decimal("0.25"),
        Decimal(2),
    }
    assert format_int_vn(1000000) == "1.000.000"
    assert format_int_vn(800) == "800"
    assert format_count(2) == "02"
    assert format_count(12) == "12"


@pytest.mark.parametrize(
    "d", [date(2025, 1, 1), date(2026, 1, 1), date(2026, 7, 1), date(2026, 8, 15)]
)
def test_table_k3_all_dates(mini_store, mini_catalog, d: date) -> None:
    facts, chunk = _table(mini_store, mini_catalog, K3, d)
    fine = [f for f in facts if f.kind == "phat_tien"]
    assert len(fine) == 1
    f = fine[0]
    assert f.values == ["800000", "1000000"]
    assert f.rendered == "từ 800.000 đồng đến 1.000.000 đồng"
    assert f.node_id == "CHETAI:ND168-2024/D6/K3@v0#0"
    assert f.unit_id == K3 and f.source == "S1"
    pts = [f for f in facts if f.kind == "tru_diem"]
    assert [p.rendered for p in pts] == ["02 điểm"]
    # nối bằng BI_TRU_DIEM từ điểm h, i (nêu tại khoản 16)
    assert pts[0].unit_id == "ND168-2024/D6/K16/a"
    assert {"ND168-2024/D6/K3/h", "ND168-2024/D6/K3/i"} <= set(pts[0].applies_to)
    # chuỗi "Phạt tiền từ 800.000 đồng …" không lặp lại thành số trong text
    texts = {f.rendered for f in facts if f.kind == "van_ban"}
    assert "800.000 đồng" not in texts and "1.000.000 đồng" not in texts
    assert "05 km/h" in texts
    # điểm m (trẻ em dưới 10 tuổi) chỉ có hiệu lực từ 01/01/2026
    assert ("10 tuổi" in texts) == (d >= date(2026, 1, 1))
    assert [f.id for f in facts] == [f"N{i}" for i in range(1, len(facts) + 1)]
    # đúng phiên bản: mọi nút chế tài nêu tại phiên bản của chunk tại ngày đó
    for f in facts:
        if f.kind != "van_ban" and f.unit_id == K3:
            assert f.version_id in chunk.version_ids


def test_table_canh_cao_has_no_number(mini_store, mini_catalog) -> None:
    # Khoản 1a (bổ sung từ 15/08/2026) chỉ có "Phạt cảnh cáo" → không có mã số
    assert _chunk_at(mini_catalog, "ND168-2024/D6/K1a", date(2026, 7, 1)) is None
    facts, _ = _table(mini_store, mini_catalog, "ND168-2024/D6/K1a", date(2026, 8, 15))
    assert not [f for f in facts if f.kind != "van_ban"]


def test_table_tuoc_quyen_and_budget(mini_store, mini_catalog) -> None:
    facts, _ = _table(mini_store, mini_catalog, "ND168-2024/D6/K15", date(2026, 1, 1))
    tq = [f for f in facts if f.kind == "tuoc_quyen"]
    assert tq and all(f.unit == "tháng" and f.rendered.startswith("từ ") for f in tq)
    # ngân sách 0 ký tự cho số trong text: nút chế tài vẫn có, số trong text bị bỏ
    facts0, _ = _table(mini_store, mini_catalog, K3, date(2026, 1, 1), text_chars_budget=0)
    assert {f.kind for f in facts0} == {"phat_tien", "tru_diem"}


def test_tru_diem_edge_filtered_by_date(mini_store) -> None:
    # BI_TRU_DIEM từ K3/h@v0 hết hiệu lực 14/08/2026
    idx = NumberIndex(mini_store)
    assert idx.linked_from("ND168-2024/D6/K3/h@v0", date(2026, 7, 1))
    assert not idx.linked_from("ND168-2024/D6/K3/h@v0", date(2026, 8, 15))
    assert idx.linked_from("ND168-2024/D6/K3/h@v1", date(2026, 8, 15))


def test_text_numbers_exclusions() -> None:
    t = (
        "1. Phạt tiền theo khoản 2 Điều 6 Nghị định số 168/2024/NĐ-CP từ ngày 01 tháng 01 năm"
        " 2026 hoặc 01/07/2026; xe chạy quá 05 km/h, chở quá 50% số người, cách 0,25 mét;"
        " xe hạng B1 năm 2025."
    )
    got = [r for r, _v, _s in text_numbers(t)]
    assert got == ["05 km/h", "50%", "0,25 mét"]


def test_node_without_numbers_skipped() -> None:
    from trafficlaw.verify.numbers import _num_props

    assert _num_props(GraphNode("X", "CheTai", {"loai": "tich_thu"})) is None
    got = _num_props(
        GraphNode("Y", "CheTai", {"loai": "phat_tien", "min_vnd": 500000, "max_vnd": 500000})
    )
    assert got is not None and got[3] == "500.000 đồng"


def test_placeholders_render() -> None:
    from trafficlaw.verify.numbers import NumberFact

    f = NumberFact(
        id="N2",
        kind="tru_diem",
        values=["2"],
        unit="điểm",
        rendered="02 điểm",
        description="Trừ điểm",
        source="S1",
        unit_id="u",
        span="x",
    )
    text = "Bị trừ {N2} và {  N2 }, mã lạ {N9}."
    assert placeholders(text) == ["N2", "N9"]
    assert render_numbers(text, {"N2": f}) == "Bị trừ 02 điểm và 02 điểm, mã lạ {N9}."
    assert [i.text for i in unknown_placeholders(text, {"N2": f})] == ["{N9}"]


def test_find_unverified_numbers() -> None:
    allowed = AllowedNumbers.build(
        "Xe chạy 70 km/h có bị phạt không?", date(2026, 1, 1), [date(2025, 1, 1)], []
    )
    ok = (
        "Theo điểm a khoản 4 Điều 6 Nghị định 168/2024/NĐ-CP (khoản 1, 2 và 3), xe chạy 70 km/h"
        " bị phạt {N1}; áp dụng từ ngày 01/01/2025, năm 2026."
    )
    assert find_unverified_numbers(ok, allowed) == []
    bad = "Bị phạt 800.000 đồng, tước 02 tháng từ 15/08/2027 năm 2030; hoặc hai triệu đồng."
    kinds = [(i.kind, i.text) for i in find_unverified_numbers(bad, allowed)]
    assert ("chu_so", "800.000") in kinds
    assert ("chu_so", "02") in kinds
    assert ("ngay", "15/08/2027") in kinds
    assert ("ngay", "năm 2030") in kinds
    assert ("chu_viet", "hai triệu đồng") in kinds
    words = find_unverified_numbers("tước bằng mười hai tháng; một số trường hợp", allowed)
    assert [i.text for i in words] == ["mười hai tháng"]


def test_dates_in_and_drop_sentences() -> None:
    assert dates_in("từ 01/01/2026 và ngày 15 tháng 8 năm 2026") == {
        date(2026, 1, 1),
        date(2026, 8, 15),
    }
    allowed = AllowedNumbers()
    text = "Câu một đúng. Câu hai phạt 500 đồng. Câu ba đúng"
    out, n = drop_sentences(text, find_unverified_numbers(text, allowed))
    assert n == 1 and out == "Câu một đúng. Câu ba đúng"


def test_render_no_duplicate_words() -> None:
    from trafficlaw.verify.numbers import NumberFact

    def fact(i: str, r: str) -> NumberFact:
        return NumberFact(
            id=i,
            kind="van_ban",
            values=["1"],
            rendered=r,
            description="",
            source="S1",
            unit_id="",
            span=r,
        )

    t = {"N1": fact("N1", "từ 800.000 đồng đến 1.000.000 đồng"), "N2": fact("N2", "02 điểm")}
    assert (
        render_numbers("phạt tiền từ {N1}.", t) == "phạt tiền từ 800.000 đồng đến 1.000.000 đồng."
    )
    assert render_numbers("phạt tiền {N1}.", t) == "phạt tiền từ 800.000 đồng đến 1.000.000 đồng."
    assert render_numbers("bị trừ {N2} điểm giấy phép", t) == "bị trừ 02 điểm giấy phép"
    assert render_numbers("bị trừ {N2} giấy phép", t) == "bị trừ 02 điểm giấy phép"
    assert render_numbers("mức {N1} đồng", t) == "mức từ 800.000 đồng đến 1.000.000 đồng"


def test_no_false_positive_codes_and_words() -> None:
    allowed = AllowedNumbers()
    ok = "Giấy phép lái xe hạng A1, B2, C1E; đầu tư đồng bộ; một số trường hợp."
    assert find_unverified_numbers(ok, allowed) == []
    bad = find_unverified_numbers("phạt hai mươi tư triệu đồng, 3 hạng", allowed)
    assert [(i.kind, i.text) for i in bad] == [
        ("chu_viet", "hai mươi tư triệu đồng"),
        ("chu_so", "3"),
    ]
