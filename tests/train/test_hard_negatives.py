"""M14: hard negative — nguồn, loại negative giả, ngưỡng delta, tất định."""

from __future__ import annotations

from datetime import date

from trafficlaw.retrieval.catalog import ChunkCatalog
from trafficlaw.train.config import MiningSpec
from trafficlaw.train.hard_negatives import (
    choose_negatives,
    exclusion_reason,
    merge_candidates,
    mine_one,
    mining_params,
    mining_stats,
    negatives_map,
    sibling_chunks,
)

from .conftest import AS_OF

POS = "VB/D1/K2#2026-01-01"


def test_siblings_nearest_live(catalog: ChunkCatalog) -> None:
    # K2 (trạng thái 2026) → anh em cùng Điều 1 còn hiệu lực, gần nhất trước; trạng thái cũ của
    # chính K2 hết hiệu lực nên không xuất hiện.
    assert sibling_chunks(catalog, POS, AS_OF, 5) == [
        "VB/D1/K1#2025-01-01",
        "VB/D1/K3#2025-01-01",
        "VB/D1/K4#2025-01-01",
    ]
    assert sibling_chunks(catalog, POS, AS_OF, 1) == ["VB/D1/K1#2025-01-01"]
    old = sibling_chunks(catalog, "VB/D1/K1#2025-01-01", date(2025, 6, 1), 5)
    assert "VB/D1/K2#2025-01-01" in old and POS not in old


def test_exclusion_reasons(catalog: ChunkCatalog) -> None:
    def r(c: str, gold=("VB/D1/K2",), as_of=AS_OF) -> str | None:
        return exclusion_reason(catalog, c, POS, list(gold), as_of)

    assert r("VB/D1/K2#2025-01-01") == "ngoai_hieu_luc"
    assert r("VB/D1/K2#2025-01-01", as_of=date(2025, 6, 1)) == "cung_unit"
    assert r("VB/D2/K1#2025-01-01", gold=("VB/D1/K2", "VB/D2")) == "lien_quan_gold"
    assert r("VB/D1/K1#2025-01-01") is None
    assert (
        exclusion_reason(catalog, "VB/D3/K2#2025-01-01", "VB/D1/K1#2025-01-01", ["VB/D1/K1"], AS_OF)
        == "trung_text"
    )


def test_merge_round_robin_cap_and_drops() -> None:
    bad = {"x": "lien_quan_gold", "y": "ngoai_hieu_luc"}
    cands, dropped = merge_candidates(
        [("dense", ["a", "x", "b", "c"]), ("bm25", ["b", "y", "d"]), ("anh_em", ["e", "a"])],
        4,
        bad.get,
    )
    assert [c.chunk_id for c in cands] == ["a", "b", "e", "d"]
    assert cands[0].sources == ("dense", "anh_em") and cands[1].sources == ("bm25", "dense")
    assert dropped["lien_quan_gold"] == 1 and dropped["ngoai_hieu_luc"] == 1


def test_choose_negatives_delta() -> None:
    scored = [("a", 4.5), ("b", 3.9), ("c", -1.0), ("d", 3.0), ("e", 3.0)]
    negs, n_close = choose_negatives(5.0, scored, delta=1.0, keep=3)
    assert negs == ["b", "d", "e"] and n_close == 1  # a ≥ 5 − 1 bị bỏ; hoà → chunk_id
    assert choose_negatives(5.0, scored, delta=0.0, keep=10)[0] == ["a", "b", "d", "e", "c"]


def test_mine_one_deterministic(catalog: ChunkCatalog) -> None:
    spec = MiningSpec(max_candidates=10, delta=1.0, keep=2)
    calls: list[list[str]] = []

    def score(q, pairs):
        calls.append([c for c, _ in pairs])
        base = {"VB/D1/K1#2025-01-01": 5.5, "VB/D3/K1#2025-01-01": 2.0}
        return {c: (6.0 if c == POS else base.get(c, 1.0)) for c, _ in pairs}

    kw = dict(
        qid="q", question="Mô tô vượt đèn đỏ?", as_of=AS_OF, pos_id=POS, gold_units=["VB/D1/K2"],
        catalog=catalog, dense_ids=["VB/D1/K2#2025-01-01", "VB/D1/K1#2025-01-01"],
        bm25_ids=["VB/D3/K1#2025-01-01", POS], spec=spec, score=score, phash="h",
    )  # fmt: skip
    r = mine_one(**kw)
    assert calls[0][0] == POS  # positive chấm cùng lượt
    assert r["pos_score"] == 6.0
    assert r["negatives"] == ["VB/D3/K1#2025-01-01", "VB/D1/K3#2025-01-01"]
    assert r["dropped"]["gan_positive"] == 1  # K1 điểm 5,5 ≥ 6 − 1
    assert r["dropped"]["ngoai_hieu_luc"] == 1
    assert mine_one(**kw) == r
    st = mining_stats([r])
    assert st["n_negatives"] == 2 and st["negative_sources"]["anh_em"] >= 1


def test_params_hash_and_map() -> None:
    a, b = MiningSpec(), MiningSpec(delta=0.5)
    assert mining_params(a) != mining_params(b)
    assert mining_params(a) == mining_params(MiningSpec())
    rows = [
        {"qid": "q", "negatives": ["x"], "params_hash": "old"},
        {"qid": "q", "negatives": ["y"], "params_hash": "new"},
    ]
    assert negatives_map(rows) == {"q": ["y"]}
    assert negatives_map(rows, "old") == {"q": ["x"]}
