"""M8: validator tập vàng, hậu kiểm bản nháp LLM (loại số lệch regex), lấy mẫu tất định."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

import pytest

from trafficlaw.eval.extraction_gold import (
    clean_draft,
    render_text,
    sample_gold,
    subtree_versions,
    validate_gold,
)
from trafficlaw.graph.embedded import EmbeddedStore
from trafficlaw.graph.extract import Catalog, CatalogEntry, ExtractConfig

MINI = Path(__file__).resolve().parents[1] / "fixtures/mini_graph"
D6 = "ND168-2024/D6"
AS_OF = date(2026, 11, 3)
CAT = Catalog(
    approved=True,
    phuong_tien=[CatalogEntry(id="PT:xe-o-to", name="xe ô tô")],
    chu_the=[CatalogEntry(id="CT:nguoi-dieu-khien-xe", name="người điều khiển xe")],
)


@pytest.fixture(scope="module")
def store() -> EmbeddedStore:
    return EmbeddedStore.from_dir(MINI)


def record(
    store: EmbeddedStore, unit: str = f"{D6}/K16", as_of: date = AS_OF, **kw: Any
) -> dict[str, Any]:
    pairs = subtree_versions(store, unit, as_of)
    rec = {
        "gold_id": f"{unit}@{as_of}",
        "unit_id": unit,
        "doc_id": "ND168-2024",
        "tier": "A",
        "stratum": "nd168_bo_sung_tru_diem",
        "as_of": as_of.isoformat(),
        "dieu_title": "t",
        "units": [{"unit_id": u, "version_id": v.id} for u, v in pairs],
        "text": render_text(pairs),
        "entities": [
            {"id": "e1", "type": "DiemGPLX", "unit_id": f"{D6}/K16/b", "so_diem": 4},
            {
                "id": "e2",
                "type": "PhuongTien",
                "unit_id": f"{D6}/K16/b",
                "catalog_id": "PT:xe-o-to",
            },
        ],
        "relations": [
            {"type": "BI_TRU_DIEM", "src": f"unit:{D6}/K5/h", "dst": "e1"},
            {"type": "AP_DUNG_CHO", "src": f"unit:{D6}/K16/b", "dst": "e2"},
        ],
        "annotator": "llm:test",
        "reviewed": False,
    }
    rec.update(kw)
    return rec


def msgs(store: EmbeddedStore, rec: dict[str, Any]) -> list[str]:
    return [f"{i['level']}:{i['message']}" for i in validate_gold([rec], store, CAT)]


def test_valid_record(store: EmbeddedStore) -> None:
    assert msgs(store, record(store)) == []


def test_unit_and_version_checks(store: EmbeddedStore) -> None:
    assert any(
        "không tồn tại" in m for m in msgs(store, record(store, unit_id="ND168-2024/D6/K99"))
    )
    old = record(store, as_of=date(2026, 11, 3))
    old["as_of"] = "2024-06-01"  # trước ngày hiệu lực của NĐ 168
    assert any("không có phiên bản hiệu lực" in m for m in msgs(store, old))
    stale = record(store)
    stale["units"] = stale["units"][:-1]
    assert any("units lệch" in m for m in msgs(store, stale))


def test_entity_and_relation_checks(store: EmbeddedStore) -> None:
    r = record(store)
    r["entities"] += [
        {"id": "e3", "type": "HanhVi", "unit_id": f"{D6}/K16/b", "span": "vượt đèn đỏ"},
        {"id": "e4", "type": "PhuongTien", "unit_id": f"{D6}/K16/b", "catalog_id": "PT:xe-mo-to"},
        {"id": "e5", "type": "DiemGPLX", "unit_id": f"{D6}/K16/b", "so_diem": 6},
        {"id": "e6", "type": "CheTai", "unit_id": f"{D6}/K5/h", "loai": "canh_cao"},
    ]
    r["relations"] += [
        {"type": "BI_TRU_DIEM", "src": f"unit:{D6}/K5/h", "dst": "e2"},
        {"type": "BI_XU_PHAT", "src": f"unit:{D6}/K99", "dst": "e1"},
    ]
    m = msgs(store, r)
    assert "error:e3: span HanhVi không nguyên văn" in m
    assert "error:e4: catalog_id ngoài danh mục: PT:xe-mo-to" in m
    assert "warning:e5: con số không khớp regex trên text unit" in m
    assert any(x.startswith("error:e6: unit") for x in m)
    assert "error:quan hệ BI_TRU_DIEM: dst e2 là PhuongTien" in m
    assert any("unit:ND168-2024/D6/K99 không có phiên bản" in x for x in m)


def test_schema_error(store: EmbeddedStore) -> None:
    r = record(store)
    r["entities"][0]["type"] = "Khac"
    assert any("sai schema" in m for m in msgs(store, r))


def test_clean_draft_drops_bad_numbers_and_spans(store: EmbeddedStore) -> None:
    pairs = subtree_versions(store, f"{D6}/K16", AS_OF)
    texts = {u: str(v.props["text"]) for u, v in pairs}
    parsed = {
        "entities": [
            {"id": "e1", "type": "DiemGPLX", "unit_id": f"{D6}/K16/b", "so_diem": 4},
            {"id": "e2", "type": "DiemGPLX", "unit_id": f"{D6}/K16/c", "so_diem": 5},  # văn bản: 06
            {
                "id": "e3",
                "type": "HanhVi",
                "unit_id": f"{D6}/K16/a",
                "span": "không có trong văn bản",
            },
            {
                "id": "e4",
                "type": "PhuongTien",
                "unit_id": f"{D6}/K16/a",
                "catalog_id": "PT:xe-o-to",
            },
            {"id": "e5", "type": "CheTai", "unit_id": f"{D6}/K5/h", "loai": "canh_cao"},
        ],
        "relations": [
            {"type": "BI_TRU_DIEM", "src": f"unit:{D6}/K5/h", "dst": "e1"},
            {"type": "BI_TRU_DIEM", "src": f"unit:{D6}/K5/h", "dst": "e2"},
            {"type": "AP_DUNG_CHO", "src": f"unit:{D6}/K16/a", "dst": "e4"},
            {"type": "BI_TRU_DIEM", "src": "ND168-2024/D6/K5/h", "dst": "e1"},
        ],
    }
    draft, dropped = clean_draft(
        parsed, texts, CAT, lambda u: store.version_at(u, AS_OF) is not None
    )
    assert [e.id for e in draft.entities] == ["e1", "e4"]
    assert [(r.type, r.dst) for r in draft.relations] == [
        ("BI_TRU_DIEM", "e1"),
        ("AP_DUNG_CHO", "e4"),
    ]
    reasons = sorted(d["reason"] for d in dropped)
    assert reasons == [
        "dich_khong_hop_le",
        "nguon_khong_hop_le",
        "so_lech_regex",
        "span_khong_nguyen_van",
        "unit_ngoai_khoan",
    ]


def test_sample_deterministic_and_disjoint(store: EmbeddedStore) -> None:
    strata = {"nd168_bo_sung_tru_diem": 2, "nd168_che_tai": 3}
    a = sample_gold(store, ExtractConfig(), strata, as_of=AS_OF, seed=42, max_units=30)
    b = sample_gold(store, ExtractConfig(), strata, as_of=AS_OF, seed=42, max_units=30)
    assert a == b
    ids = [r.unit_id for r in a]
    assert len(ids) == len(set(ids)) == 5
    bo_sung = {r.unit_id for r in a if r.stratum == "nd168_bo_sung_tru_diem"}
    assert bo_sung == {f"{D6}/K15", f"{D6}/K16"}
    c = sample_gold(store, ExtractConfig(), strata, as_of=AS_OF, seed=7, max_units=30)
    assert {r.stratum for r in c} == set(strata)


def test_clean_draft_strips_fields_not_valid_for_type(store: EmbeddedStore) -> None:
    """Model gán nháp điền thừa (vd ``loai: "HanhVi"`` cho HanhVi) → bỏ trường thừa, giữ
    thực thể."""
    pairs = subtree_versions(store, f"{D6}/K16", AS_OF)
    texts = {u: str(v.props["text"]) for u, v in pairs}
    span = texts[f"{D6}/K16/b"][3:40]
    parsed = {
        "entities": [
            {
                "id": "e1",
                "type": "HanhVi",
                "unit_id": f"{D6}/K16/b",
                "span": span,
                "ten": "x",
                "loai": "HanhVi",
                "so_diem": 4,
            },
            {
                "id": "e2",
                "type": "DiemGPLX",
                "unit_id": f"{D6}/K16/b",
                "so_diem": 4,
                "loai": "DiemGPLX",
                "catalog_id": "PT:xe-o-to",
            },
        ],
        "relations": [],
    }
    draft, dropped = clean_draft(parsed, texts, CAT, lambda u: True)
    assert [e.id for e in draft.entities] == ["e1", "e2"] and dropped == []
    assert draft.entities[0].loai is None and draft.entities[0].so_diem is None
    assert draft.entities[1].catalog_id is None and draft.entities[1].so_diem == 4
