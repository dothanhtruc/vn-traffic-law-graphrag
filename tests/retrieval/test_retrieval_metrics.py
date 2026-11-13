"""Chỉ số truy hồi (M10) so với giá trị tính tay; lấy mẫu tập đo tất định."""

from __future__ import annotations

import math
from datetime import date

import pytest

from trafficlaw.eval.retrieval_eval import EvalQuery, fixed_sample, stratified_sample
from trafficlaw.eval.retrieval_metrics import (
    QueryScore,
    bootstrap_ci,
    mrr_at,
    ndcg_at,
    recall_at,
    score_query,
    summarize,
)

RANKED = ["x", "a1", "y", "b1", "a2"]
REL = {"A": {"a1", "a2"}, "B": {"b1"}, "C": {"c9"}}


def test_recall_unit_level() -> None:
    assert recall_at(RANKED, REL, 1) == 0.0
    assert recall_at(RANKED, REL, 2) == pytest.approx(1 / 3)  # A có a1
    assert recall_at(RANKED, REL, 4) == pytest.approx(2 / 3)  # + B
    assert recall_at(RANKED, REL, 20) == pytest.approx(2 / 3)  # C không bao giờ thấy
    assert recall_at(RANKED, {}, 5) == 0.0


def test_mrr_ndcg_hand() -> None:
    assert mrr_at(RANKED, REL, 10) == pytest.approx(0.5)
    assert mrr_at(RANKED, REL, 1) == 0.0
    # chunk đúng ở hạng 2, 4, 5; |đúng| = 4 ⇒ IDCG = 1 + 1/log2 3 + 1/2 + 1/log2 5
    dcg = 1 / math.log2(3) + 1 / math.log2(5) + 1 / math.log2(6)
    idcg = 1 + 1 / math.log2(3) + 0.5 + 1 / math.log2(5)
    assert ndcg_at(RANKED, REL, 10) == pytest.approx(dcg / idcg)
    assert ndcg_at(["a1", "a2", "b1", "c9"], REL, 10) == pytest.approx(1.0)
    assert ndcg_at(RANKED, {"A": set()}, 10) == 0.0


def test_score_and_summary() -> None:
    s1 = score_query("q1", ["a"], {"G": {"a"}})
    s2 = score_query("q2", ["b", "a"], {"G": {"a"}})
    assert s1.values["recall@1"] == 1.0 and s2.values["recall@1"] == 0.0
    sm = summarize([s1, s2], ci_metrics=("recall@1",))
    assert sm["n"] == 2 and sm["recall@1"] == 0.5 and sm["mrr@10"] == pytest.approx(0.75)
    lo, hi = sm["recall@1_ci"]
    assert 0.0 <= lo <= 0.5 <= hi <= 1.0
    # CI tất định theo seed
    scores = [QueryScore(str(i), {"m": float(i % 2)}) for i in range(50)]
    assert bootstrap_ci(scores, "m", seed=1) == bootstrap_ci(scores, "m", seed=1)
    assert bootstrap_ci([], "m") is None


def _qs(n: int) -> list[EvalQuery]:
    tiers = ["A"] * 7 + ["B"] * 2 + ["C"]
    return [
        EvalQuery(f"q{i}", f"câu {i}", date(2026, 11, 3), ("U",), tiers[i % 10], "khac")
        for i in range(n)
    ]


def test_stratified_sample_proportional_deterministic() -> None:
    qs = _qs(200)
    s = stratified_sample(qs, 50, seed=42, name="t")
    assert len(s) == 50
    by = {t: sum(1 for q in s if q.tier == t) for t in "ABC"}
    assert by == {"A": 35, "B": 10, "C": 5}
    # không phụ thuộc thứ tự file
    assert {q.qid for q in s} == {
        q.qid for q in stratified_sample(list(reversed(qs)), 50, seed=42, name="t")
    }
    assert {q.qid for q in s} != {q.qid for q in stratified_sample(qs, 50, seed=7, name="t")}
    assert stratified_sample(qs[:10], 50, seed=42, name="t") == qs[:10]


def test_fixed_sample_stable_when_set_grows() -> None:
    qs = _qs(100)
    a = {q.qid for q in fixed_sample(qs, 10, seed=42, name="r")}
    b = {q.qid for q in fixed_sample(qs + _qs(120)[100:], 10, seed=42, name="r")}
    assert len(a) == 10 and len(a & b) >= 8
