"""M9: schema QAItem + validator bộ hỏi–đáp (unit/phiên bản, con số, cặp thời điểm, trùng lặp,
rò rỉ, phân bổ). Dùng mini_graph (ND168 Đ6, LUAT36 Đ6/Đ7/Đ35/Đ77)."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from trafficlaw.eval.qa_schema import QAItem, split_of
from trafficlaw.eval.qa_validate import (
    Targets,
    ValidateConfig,
    check_leakage,
    parse_numbers,
    validate_items,
)
from trafficlaw.graph.embedded import EmbeddedStore
from trafficlaw.graph.store import GraphNode

MINI = Path(__file__).resolve().parents[1] / "fixtures/mini_graph"
D6 = "ND168-2024/D6"
AS_OF = "2026-11-03"


@pytest.fixture(scope="module")
def store() -> EmbeddedStore:
    return EmbeddedStore.from_dir(MINI)


def q(qid: str = "t1", **kw: Any) -> dict[str, Any]:
    rec: dict[str, Any] = {
        "qid": qid,
        "question": f"Người lái ô tô vi phạm bị phạt bao nhiêu tiền? ({qid})",
        "as_of": AS_OF,
        "question_type": "muc_phat",
        "tier": "A",
        "answer": "Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng.",
        "gold_units": [f"{D6}/K5"],
        "required_numbers": [{"value": 4000000, "unit": "vnd"}],
    }
    rec.update(kw)
    return rec


def codes(
    rows: list[dict[str, Any]], store: EmbeddedStore, split: str = "test", **kw: Any
) -> list[str]:
    res = validate_items(rows, split, store, ValidateConfig(**kw))  # type: ignore[arg-type]
    return [f"{i.level}:{i.code}" for i in res.issues]


# --------------------------------------------------------------------------- schema


def test_schema_ok_and_forbid_extra() -> None:
    it = QAItem.model_validate(q())
    assert it.as_of == date(2026, 11, 3) and it.source == "human"
    with pytest.raises(ValidationError):
        QAItem.model_validate(q(extra_field=1))
    with pytest.raises(ValidationError):
        QAItem.model_validate(q(question_type="khong_co"))
    # NFC: "ô" tổ hợp → dựng sẵn
    assert QAItem.model_validate(q(question="xe ô tô ?")).question == "xe ô tô ?"


def test_split_of() -> None:
    assert split_of("data/qa/test.jsonl") == "test"
    assert split_of("x/val.jsonl") == "val"
    with pytest.raises(ValueError):
        split_of("data/qa/gold_extraction.jsonl")


def test_parse_numbers() -> None:
    assert parse_numbers("từ 400.000 đồng đến 1.000.000 đồng") == {Decimal(400000), Decimal(10**6)}
    assert parse_numbers("dưới 1,35 mét, từ 02 tháng") == {Decimal("1.35"), Decimal(2)}
    assert parse_numbers("không có số") == set()


# --------------------------------------------------------------------------- unit / phiên bản


def test_valid_item_no_issues(store: EmbeddedStore) -> None:
    res = validate_items([q()], "test", store, ValidateConfig())
    assert [i.code for i in res.issues] == []
    assert res.resolved[0]["gold_versions"] == [f"{D6}/K5@v0"]


def test_empty_file_ok(store: EmbeddedStore) -> None:
    res = validate_items([], "test", store, ValidateConfig(targets=Targets(total=500)))
    assert res.n_errors == 0 and res.distribution["n"] == 0


def test_unit_missing_and_not_in_effect(store: EmbeddedStore) -> None:
    assert "error:unit_khong_ton_tai" in codes([q(gold_units=[f"{D6}/K99"])], store)
    # K1a được bổ sung từ 15/08/2026 → trước đó chưa có hiệu lực
    bad = q(as_of="2026-08-01", gold_units=[f"{D6}/K1a"], required_numbers=[])
    assert "error:het_hieu_luc" in codes([bad], store)
    ok = q(as_of="2026-08-15", gold_units=[f"{D6}/K1a"], required_numbers=[])
    assert "error:het_hieu_luc" not in codes([ok], store)


def test_gold_versions_mismatch(store: EmbeddedStore) -> None:
    assert "error:gold_versions_lech" in codes([q(gold_versions=[f"{D6}/K5@v9"])], store)
    assert codes([q(gold_versions=[f"{D6}/K5@v0"])], store) == []


def test_tier_and_type_rules(store: EmbeddedStore) -> None:
    assert "error:tier_lech" in codes([q(tier="B")], store)
    assert "error:thieu_tier" in codes([q(tier=None)], store)
    assert "error:ngoai_pham_vi_co_gold" in codes([q(question_type="ngoai_pham_vi")], store)
    oos = q(question_type="ngoai_pham_vi", tier=None, gold_units=[], required_numbers=[])
    assert codes([oos], store) == []
    assert "error:thieu_gold" in codes([q(gold_units=[], required_numbers=[])], store)


def test_test_split_must_be_human_with_answer(store: EmbeddedStore) -> None:
    c = codes([q(answer=None, source="llm:x")], store)
    assert "error:thieu_dap_an" in c and "error:nguon_khong_phai_nguoi" in c
    # train/val không cần đáp án, nguồn LLM được
    assert codes([q(answer=None, source="llm:x")], store, split="train") == []


# --------------------------------------------------------------------------- con số


def test_number_not_in_text(store: EmbeddedStore) -> None:
    rn = [{"value": 123456, "unit": "vnd"}]
    assert "error:so_khong_co_trong_van_ban" in codes([q(required_numbers=rn)], store)


def test_number_from_parent_and_answer_warning(store: EmbeddedStore) -> None:
    # Mức phạt nằm ở câu dẫn Khoản 5 → gold là Điểm vẫn kiểm được (tổ tiên)
    it = q(gold_units=[f"{D6}/K5/a"], answer="Bị phạt tiền.")
    c = codes([it], store)
    assert "error:so_khong_co_trong_van_ban" not in c
    assert "warning:so_khong_co_trong_dap_an" in c


def test_number_from_semantic_props() -> None:
    st = EmbeddedStore.from_dir(MINI)
    st.upsert_nodes(
        [
            GraphNode(
                "CHETAI:x#0",
                "CheTai",
                {
                    "unit_id": f"{D6}/K5",
                    "version_id": f"{D6}/K5@v0",
                    "loai": "phat_tien",
                    "min_vnd": 777,
                    "max_vnd": 888,
                },
            )
        ]
    )
    rn = [{"value": 777, "unit": "vnd"}, {"value": 888, "unit": "vnd"}]
    assert "error:so_khong_co_trong_van_ban" not in codes([q(required_numbers=rn)], st)


def test_number_unit_scope(store: EmbeddedStore) -> None:
    rn = [{"value": 4000000, "unit": "vnd", "unit_id": f"{D6}/K1"}]
    assert "error:so_khong_co_trong_van_ban" in codes([q(required_numbers=rn)], store)


# --------------------------------------------------------------------------- cặp thời điểm


def pair(
    d1: str,
    d2: str,
    g1: list[str],
    g2: list[str],
    a1: str = "Chưa quy định.",
    a2: str = "Bị phạt tiền.",
) -> list[dict[str, Any]]:
    base = {
        "question_type": "theo_thoi_diem",
        "pair_id": "p1",
        "required_numbers": [],
        "question": "Chở trẻ em dưới 10 tuổi ngồi ghế trước có bị phạt không?",
    }
    return [
        q("a", as_of=d1, gold_units=g1, answer=a1, **base),
        q("b", as_of=d2, gold_units=g2, answer=a2, **base),
    ]


def test_pair_around_milestone_ok(store: EmbeddedStore) -> None:
    m = f"{D6}/K3/m"  # hiệu lực từ 01/01/2026 (mốc), sửa 15/08/2026 (mốc)
    assert codes(pair("2025-12-31", "2026-01-01", [], [m]), store) == []
    assert codes(pair("2026-08-14", "2026-08-15", [m], [m]), store) == []


def test_pair_errors(store: EmbeddedStore) -> None:
    m = f"{D6}/K3/m"
    assert "error:cap_khong_doi_phien_ban" in codes(
        pair("2026-02-01", "2026-03-01", [m], [m]), store
    )
    same = pair("2026-08-14", "2026-08-15", [m], [m], a1="Phạt.", a2="phạt")
    assert "error:dap_an_giong_nhau" in codes(same, store)
    assert "error:cap_thieu" in codes(pair("2026-08-14", "2026-08-15", [m], [m])[:1], store)
    both = pair("2026-08-15", "2026-08-15", [m], [m])
    assert "error:cap_cung_ngay" in codes(both, store)


def test_pair_non_milestone_warns(store: EmbeddedStore) -> None:
    m = f"{D6}/K3/m"
    c = codes(pair("2026-08-14", "2026-08-15", [m], [m]), store, milestones=(date(2025, 1, 1),))
    assert "warning:moc_khong_chuan" in c and not [x for x in c if x.startswith("error")]


# --------------------------------------------------------------------------- đa bước, trùng


def test_da_buoc(store: EmbeddedStore) -> None:
    base = {"question_type": "da_buoc", "required_numbers": []}
    one = q(gold_units=["LUAT36-2024/D35/K5"], **base)
    assert "error:da_buoc_it_unit" in codes([one], store)
    linked = q(gold_units=["LUAT36-2024/D35/K5", "LUAT36-2024/D35/K2"], **base)
    assert codes([linked], store) == []
    loose = q(gold_units=["LUAT36-2024/D35/K1", f"{D6}/K5"], **base)
    assert "warning:da_buoc_khong_noi" in codes([loose], store)


def test_duplicates(store: EmbeddedStore) -> None:
    a = q("t1", question="Vượt đèn đỏ khi lái ô tô bị phạt bao nhiêu tiền vậy?")
    b = q("t2", question="Vượt đèn đỏ khi lái ô tô bị phạt bao nhiêu tiền vậy ?")
    c = q("t3", question="Vượt đèn đỏ khi lái ô tô bị phạt bao nhiêu tiền vậy ạ?")
    got = codes([a, b, c], store)
    assert "error:trung_lap" in got and "warning:gan_trung" in got
    assert "error:qid_trung" in codes([q("t1"), q("t1")], store)


def test_schema_error_reported(store: EmbeddedStore) -> None:
    res = validate_items([{"qid": "x"}], "test", store)
    assert res.n_errors == 1 and res.issues[0].code == "sai_schema"


# --------------------------------------------------------------------------- rò rỉ, val, phân bổ


def test_leakage_and_val_split(store: EmbeddedStore) -> None:
    tr = [QAItem.model_validate(q("g1", question="Lái ô tô vượt đèn đỏ thì bị phạt bao nhiêu?"))]
    iss = check_leakage(tr, ["Lái ô tô vượt đèn đỏ thì bị phạt bao nhiêu ?"], 0.9)
    assert [i.code for i in iss] == ["ro_ri_test"]
    assert check_leakage(tr, ["Định nghĩa xe gắn máy là gì?"], 0.9) == []
    res = validate_items([q(answer=None, source="llm:x")], "train", store, other_split_dieus={D6})
    assert "val_tron_dieu" in [i.code for i in res.issues]


def test_distribution_warnings(store: EmbeddedStore) -> None:
    tg = Targets(total=5, tier={"A": 1}, question_type={"muc_phat": 1, "dinh_nghia": 5})
    rows = [q(f"t{i}", question=f"Câu hỏi khác nhau số {i * 1000}") for i in range(5)]
    c = codes(rows, store, targets=tg)
    assert "warning:vuot_han_muc" in c and "warning:lech_phan_bo" in c
