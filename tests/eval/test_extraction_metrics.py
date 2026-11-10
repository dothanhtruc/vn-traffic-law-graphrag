"""M8: P/R/F1 trích xuất so với giá trị tính tay; ghép cặp; bootstrap; tỷ lệ người sửa."""

from __future__ import annotations

from datetime import date

import pytest

from trafficlaw.eval.extraction_metrics import (
    Ent,
    PredIndex,
    Rel,
    aggregate,
    bootstrap_ci,
    edit_stats,
    gold_entities,
    pred_for_record,
    score_record,
    token_f1,
)

U, K, V = "X/D1/K1/a", "X/D1/K1", "X/D1/K2/b"


def E(i: str, t: str, unit: str, **a: object) -> Ent:  # noqa: N802
    return Ent(i, t, unit, tuple(sorted(a.items())))


def test_token_f1_by_hand() -> None:
    assert token_f1("a b c d", "a b x") == pytest.approx(4 / 7)
    assert token_f1("Xe gắn máy,", "xe GẮN máy") == 1.0
    assert token_f1("", "x") == 0.0


GOLD = [
    E("e1", "HanhVi", U, span="điều khiển xe lạng lách đánh võng"),
    E("e2", "CheTai", K, loai="phat_tien", min_vnd=40_000_000, max_vnd=50_000_000),
    E("e3", "PhuongTien", U, catalog_id="PT:xe-o-to"),
    E("e4", "DiemGPLX", K, so_diem=10),
]
GREL = [
    Rel("QUY_DINH_HANH_VI", U, "e1"),
    Rel("BI_XU_PHAT", U, "e2"),
    Rel("AP_DUNG_CHO", U, "e3"),
    Rel("BI_TRU_DIEM", U, "e4"),
]
PRED = [
    E(
        "p1", "HanhVi", U, span="điều khiển xe lạng lách"
    ),  # token-F1 = 2·1·(5/7)/(1+5/7) ≈ 0,83 ≥ 0,5 → khớp e1
    E("p2", "CheTai", K, loai="phat_tien", min_vnd=40_000_000, max_vnd=50_000_000),
    E("p3", "PhuongTien", U, catalog_id="PT:xe-gan-may"),  # xe gắn máy ≠ xe ô tô
    E("p4", "HanhVi", U, span="dùng chân điều khiển vô lăng"),
]
PREL = [
    Rel("QUY_DINH_HANH_VI", U, "p1"),
    Rel("BI_XU_PHAT", U, "p2"),
    Rel("AP_DUNG_CHO", U, "p3"),
    Rel("QUY_DINH_HANH_VI", U, "p4"),
    Rel("BI_XU_PHAT", V, "p2"),  # sai unit nguồn
]


def test_score_record_by_hand() -> None:
    rs = score_record("g", "A", "s", GOLD, GREL, PRED, PREL, 0.5)
    e, r = rs.total("entity").prf(), rs.total("relation").prf()
    # thực thể: TP 2 (e1, e2), FP 2 (p3, p4), FN 2 (e3, e4)
    assert (e["tp"], e["fp"], e["fn"]) == (2, 2, 2)
    assert e["precision"] == pytest.approx(0.5) and e["f1"] == pytest.approx(0.5)
    # quan hệ: TP 2, FP 3, FN 2 → P 0,4, R 0,5, F1 = 0,8/1,8
    assert (r["tp"], r["fp"], r["fn"]) == (2, 3, 2)
    assert r["precision"] == pytest.approx(0.4)
    assert r["recall"] == pytest.approx(0.5)
    assert r["f1"] == pytest.approx(2 * 0.4 * 0.5 / 0.9)
    assert rs.ent["HanhVi"].tp == 1 and rs.ent["HanhVi"].fp == 1
    assert rs.ent["DiemGPLX"].fn == 1


def test_numbers_must_match_exactly() -> None:
    g = [E("e", "CheTai", K, loai="phat_tien", min_vnd=400_000, max_vnd=600_000)]
    p = [E("p", "CheTai", K, loai="phat_tien", min_vnd=400_000, max_vnd=6_000_000)]
    assert score_record("g", "A", "s", g, [], p, [], 0.5).total("entity").tp == 0


def test_span_threshold() -> None:
    g = [E("e", "HanhVi", U, span="a b c d e f g h")]
    p = [E("p", "HanhVi", U, span="a x y z w v u t")]  # F1 1/8
    assert score_record("g", "A", "s", g, [], p, [], 0.5).total("entity").tp == 0
    assert score_record("g", "A", "s", g, [], p, [], 0.1).total("entity").tp == 1


def test_aggregate_and_bootstrap() -> None:
    a = score_record("g1", "A", "s1", GOLD, GREL, PRED, PREL, 0.5)
    b = score_record("g2", "B", "s2", GOLD[:1], GREL[:1], PRED[:1], PREL[:1], 0.5)
    rep = aggregate([a, b])
    assert rep["overall"]["entity"]["tp"] == 3
    assert rep["by_tier"]["B"]["entity"]["f1"] == 1.0
    assert set(rep["by_type"]["entity"]) == {"CheTai", "DiemGPLX", "HanhVi", "PhuongTien"}
    ci1 = bootstrap_ci([a, a, a], "entity", n=200, seed=42)
    assert ci1 == (pytest.approx(0.5), pytest.approx(0.5))
    assert bootstrap_ci([a, b], "entity", n=200, seed=42) == bootstrap_ci(
        [a, b], "entity", n=200, seed=42
    )
    lo, hi = bootstrap_ci([a, b], "entity", n=200, seed=42)  # type: ignore[misc]
    assert lo <= 0.6 <= hi  # F1 tổng: TP 3, FP 2, FN 2 → 0,6


def test_edit_stats() -> None:
    draft = {
        "entities": [
            {
                "id": "e1",
                "type": "HanhVi",
                "unit_id": U,
                "span": "lạng lách đánh võng",
                "ten": "lạng lách",
            },
            {"id": "e2", "type": "CheTai", "unit_id": K, "loai": "canh_cao"},
        ],
        "relations": [
            {"type": "QUY_DINH_HANH_VI", "src": f"unit:{U}", "dst": "e1"},
            {"type": "BI_XU_PHAT", "src": f"unit:{U}", "dst": "e2"},
        ],
    }
    final = {
        "entities": [
            {
                "id": "e1",
                "type": "HanhVi",
                "unit_id": U,
                "span": "lạng lách đánh võng",
                "ten": "lạng lách, đánh võng",
            },
            {"id": "e9", "type": "PhuongTien", "unit_id": U, "catalog_id": "PT:xe-o-to"},
        ],
        "relations": [
            {"type": "QUY_DINH_HANH_VI", "src": f"unit:{U}", "dst": "e1"},
            {"type": "AP_DUNG_CHO", "src": f"unit:{U}", "dst": "e9"},
        ],
    }
    s = edit_stats(draft, final, 0.5)
    assert (s["entities_added"], s["entities_removed"], s["entities_changed"]) == (1, 1, 1)
    assert (s["relations_added"], s["relations_removed"]) == (1, 1)


def test_pred_for_record_filters_scope_and_date() -> None:
    nodes = [
        {
            "id": "CHETAI:X/D1/K1@v0#0",
            "label": "CheTai",
            "props": {
                "unit_id": K,
                "version_id": f"{K}@v0",
                "loai": "phat_tien",
                "min_vnd": 1,
                "max_vnd": 2,
            },
        },
        {
            "id": "HV:X/D1/K1/a@v0#0",
            "label": "HanhVi",
            "props": {"unit_id": U, "version_id": f"{U}@v0", "name": "n", "span": "s"},
        },
        {
            "id": "HV:X/D9/K1@v0#0",
            "label": "HanhVi",
            "props": {"unit_id": "X/D9/K1", "version_id": "X/D9/K1@v0", "name": "n", "span": "s"},
        },
        {"id": "PT:xe-o-to", "label": "PhuongTien", "props": {"name": "xe ô tô"}},
    ]
    eff = {"effective_from": "2025-01-01", "effective_to": None}
    edges = [
        {"type": "BI_XU_PHAT", "src": f"{U}@v0", "dst": "CHETAI:X/D1/K1@v0#0", "props": eff},
        {
            "type": "BI_XU_PHAT",
            "src": f"{V}@v0",
            "dst": "CHETAI:X/D1/K1@v0#0",
            "props": {"effective_from": "2027-01-01", "effective_to": None},
        },
        {"type": "QUY_DINH_HANH_VI", "src": f"{U}@v0", "dst": "HV:X/D1/K1/a@v0#0", "props": eff},
        {"type": "AP_DUNG_CHO", "src": f"{U}@v0", "dst": "PT:xe-o-to", "props": eff},
    ]
    idx = PredIndex.build(nodes, edges)
    ents, rels = pred_for_record(idx, [f"{K}@v0", f"{U}@v0"], date(2026, 1, 1))
    assert sorted(e.type for e in ents) == ["CheTai", "HanhVi", "PhuongTien"]
    assert Rel("BI_XU_PHAT", U, "CHETAI:X/D1/K1@v0#0") in rels
    assert all(r.src_unit != V for r in rels)  # cạnh chưa hiệu lực tại as_of
    g_ents, g_rels = gold_entities(
        {
            "entities": [
                {"id": "e1", "type": "PhuongTien", "unit_id": U, "catalog_id": "PT:xe-o-to"}
            ],
            "relations": [{"type": "AP_DUNG_CHO", "src": f"unit:{U}", "dst": "e1"}],
        }
    )
    rs = score_record("g", "A", "s", g_ents, g_rels, ents, rels, 0.5)
    assert rs.ent["PhuongTien"].tp == 1 and rs.rel["AP_DUNG_CHO"].tp == 1


def test_vehicle_and_subject_scored_per_record() -> None:
    """Gold gắn ChuThe vào câu dẫn Khoản, hệ thống gắn vào từng Điểm → vẫn khớp (cấp Khoản)."""
    g = [E("e1", "ChuThe", K, catalog_id="CT:nguoi-di-bo")]
    gr = [Rel("AP_DUNG_CHO", K, "e1")]
    p = [
        E("p1", "ChuThe", U, catalog_id="CT:nguoi-di-bo"),
        E("p2", "ChuThe", V, catalog_id="CT:nguoi-di-bo"),
        E("p3", "PhuongTien", U, catalog_id="PT:xe-gan-may"),
    ]
    pr = [Rel("AP_DUNG_CHO", U, "p1"), Rel("AP_DUNG_CHO", V, "p2"), Rel("AP_DUNG_CHO", U, "p3")]
    rs = score_record("g", "A", "s", g, gr, p, pr, 0.5)
    assert (rs.ent["ChuThe"].tp, rs.ent["ChuThe"].fp) == (1, 0)
    assert rs.ent["PhuongTien"].fp == 1
    assert (rs.rel["AP_DUNG_CHO"].tp, rs.rel["AP_DUNG_CHO"].fp, rs.rel["AP_DUNG_CHO"].fn) == (
        1,
        1,
        0,
    )
