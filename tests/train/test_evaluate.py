"""M14: đánh giá trong lúc train (dense-only, rerank-only trên pool cố định), log, cấu hình."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from trafficlaw.eval.retrieval_eval import EvalQuery
from trafficlaw.retrieval.catalog import ChunkCatalog
from trafficlaw.retrieval.dense import HashEmbedder, Window
from trafficlaw.train.config import TrainConfig, load_mining_config, load_train_config
from trafficlaw.train.evaluate import dense_eval, load_pools, rank_pool, rerank_eval, selection_key
from trafficlaw.train.run_log import RunLog, gpu_cost, read_events

from .conftest import AS_OF

ROOT = Path(__file__).resolve().parents[2]


def _queries() -> list[EvalQuery]:
    return [
        EvalQuery("v1", "Đỗ xe trên vỉa hè bị phạt tiền", AS_OF, ("VB/D3/K1",), "A", "muc_phat"),
        EvalQuery("v2", "Thời hạn giấy phép lái xe", AS_OF, ("VB/D2/K2",), "A", "khac"),
    ]


def test_dense_eval_with_hash_embedder(catalog: ChunkCatalog) -> None:
    emb = HashEmbedder(256)
    ws = [Window(c.chunk_id, 0, c.text, 10, False) for c in catalog.chunks]
    res = dense_eval(lambda t, kind: emb.encode(t), ws, catalog, _queries())
    assert res["n"] == 2 and res["recall@5"] == 1.0 and res["mrr@10"] == 1.0
    assert res["recall@5_ci"] is not None


def test_rerank_eval_fixed_pool(catalog: ChunkCatalog) -> None:
    pools = {
        "v1": {
            "pool": ["VB/D1/K1#2025-01-01", "VB/D1/K2#2025-01-01", "VB/D3/K1#2025-01-01"],
            "base": {"VB/D1/K1#2025-01-01": 3.0, "VB/D1/K2#2025-01-01": 9.0,
                     "VB/D3/K1#2025-01-01": 1.0},
        },
        "v2": {"pool": ["VB/D2/K2#2025-01-01"], "base": {"VB/D2/K2#2025-01-01": 0.5}},
    }  # fmt: skip
    base = rerank_eval(None, None, pools, _queries(), catalog, use_base=True)
    # v1: K2#2025 hết hiệu lực bị bỏ; D3/K1 hạng 2 ⇒ MRR 0,5.
    assert base["recall@1"] == 0.5 and base["mrr@10"] == pytest.approx(0.75)
    seen: list[int] = []

    def score(pairs):
        seen.append(len(pairs))
        return [10.0 if "vỉa hè" in p else 1.0 for _, p in pairs]

    res = rerank_eval(score, lambda t: len(t.split()) + 2, pools, _queries(), catalog)
    assert res["recall@1"] == 1.0 and res["n_pairs"] == sum(seen) == 4


def test_rank_pool_ties_keep_pool_order() -> None:
    live = frozenset({"a", "b", "c"})
    assert rank_pool(["a", "b", "c", "d"], {"a": 1.0, "b": 2.0, "c": 1.0, "d": 9.0}, live) == [
        "b",
        "a",
        "c",
    ]


def test_selection_key_order() -> None:
    a = {"recall@5": 0.9, "mrr@10": 0.7}
    b = {"recall@5": 0.9, "mrr@10": 0.71}
    c = {"recall@5": 0.91, "mrr@10": 0.1}
    assert selection_key(c) > selection_key(b) > selection_key(a)
    assert not selection_key(a) > selection_key(dict(a))  # hoà → giữ bản sớm hơn


def test_load_pools(tmp_path: Path) -> None:
    p = tmp_path / "G.jsonl"
    p.write_text(
        json.dumps({
            "qid": "v1", "question": "?", "as_of": "2026-11-03",
            "pool": [{"chunk_id": "a", "rerank_score": 1.5}, {"chunk_id": "b"}],
        }) + "\n",
        encoding="utf-8",
    )  # fmt: skip
    got = load_pools(p)["v1"]
    assert got["pool"] == ["a", "b"] and got["base"] == {"a": 1.5, "b": None}


def test_run_log(tmp_path: Path) -> None:
    log = RunLog(tmp_path / "r.jsonl")
    log.event("start", a=1)
    log.event("eval", step=3, metrics={"recall@5": 0.5})
    assert [e["event"] for e in read_events(tmp_path / "r.jsonl")] == ["start", "eval"]
    assert read_events(tmp_path / "r.jsonl", "eval")[0]["step"] == 3
    assert gpu_cost(1800, 17000) == {"gpu_hours": 0.5, "vnd": 8500}


def test_real_configs_load() -> None:
    emb = load_train_config(ROOT / "configs/train_embedding.yaml")
    rr = load_train_config(ROOT / "configs/train_reranker.yaml")
    mine = load_mining_config(ROOT / "configs/hard_negatives.yaml")
    assert emb.kind == "embedding" and rr.kind == "reranker"
    assert emb.train.batch_size == 128 and emb.train.mini_batch_size == 16  # dry-run 22/11
    assert rr.train.batch_size == 16 and rr.train.grad_accum == 2
    assert emb.grid and rr.grid
    for cfg in (emb, rr):
        for gid in cfg.grid:
            p = cfg.params(gid)
            assert p.lr > 0 and cfg.run_name(gid).startswith(cfg.run_prefix)
        assert set(cfg.data.exclude_gold) == {"data/qa/test.jsonl", "data/qa/dev_multi.jsonl"}
    assert mine.keep >= rr.train.n_neg >= emb.train.n_neg


def test_grid_rejects_unknown_field() -> None:
    with pytest.raises(ValueError):
        TrainConfig(kind="embedding", base_key="x", run_prefix="p", grid={"g": {"lr_typo": 1}})
