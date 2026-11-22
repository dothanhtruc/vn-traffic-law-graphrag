"""M11: ``retrieve()`` end-to-end với model giả cho mọi cấu hình B1..A3 trên mini_graph."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest

from trafficlaw.graph.embedded import EmbeddedStore
from trafficlaw.retrieval.analyze import AnalyzerTables
from trafficlaw.retrieval.catalog import ChunkCatalog
from trafficlaw.retrieval.config import RetrievalConfig
from trafficlaw.retrieval.index_pipeline import MissingVectorsError
from trafficlaw.retrieval.rerank import FakeReranker, MissingRerankScoresError
from trafficlaw.retrieval.retrieve import RetrievalResult

from .conftest import DATES, make_ctx

CONFIGS = ("B1", "B2", "B3", "G", "A1", "A2", "A3")
Q_CHILD = (
    "Chở trẻ em dưới 10 tuổi không sử dụng thiết bị an toàn phù hợp cho trẻ em bị phạt bao nhiêu?"
)
Q_LANE = "Chuyển làn đường không có tín hiệu báo trước bị phạt tiền bao nhiêu?"


@pytest.fixture()
def ctx(tmp_path: Path, cfg, mini_store, mini_catalog, tables):
    return make_ctx(tmp_path, cfg, mini_store, mini_catalog, tables)


@pytest.mark.parametrize("name", CONFIGS)
@pytest.mark.parametrize("d", DATES)
def test_all_configs_run(ctx, mini_catalog: ChunkCatalog, name: str, d: date) -> None:
    r = ctx.retrieve(Q_LANE, d, name)
    sc = ctx.cfg.system(name)
    assert r.config_name == name and r.as_of == d and r.analysis.as_of_source == "tham_so"
    assert 0 < len(r.hits) <= sc.final_k
    assert [h.rank for h in r.hits] == list(range(1, len(r.hits) + 1))
    assert r.ranked[: len(r.hits)] == [h.chunk_id for h in r.hits]
    if sc.validity_filter:
        live = mini_catalog.ids_at(d)
        assert set(r.ranked) <= live, "chunk ngoài hiệu lực lọt vào kết quả"
        assert all(p.chunk_id in live for p in r.pool)
    assert (r.reranker is not None) == sc.reranker
    assert (r.embedding is not None) == sc.dense
    if not sc.graph_expand:
        assert not any(s.source == "graph" for p in r.pool for s in p.sources)


@pytest.mark.parametrize("d", [date(2025, 6, 1), date(2026, 7, 1)])
def test_filter_vs_a2(ctx, mini_catalog: ChunkCatalog, d: date) -> None:
    """Câu hỏi khớp nguyên văn Khoản chỉ có ở trạng thái sau (Đ6 K3 m từ 01/01/2026, K1a từ
    15/08/2026): G/B3 không bao giờ trả chunk ngoài hiệu lực; A2 (bỏ lọc) thì có."""
    live = mini_catalog.ids_at(d)
    for name in ("G", "B3", "B1", "A1"):
        r = ctx.retrieve(Q_CHILD, d, name)
        assert set(r.ranked) <= live
    a2 = ctx.retrieve(Q_CHILD, d, "A2")
    assert not a2.validity_filter
    assert set(a2.ranked) - live, "A2 phải có thể trả chunk ngoài hiệu lực"


def test_graph_provenance(ctx, mini_catalog: ChunkCatalog) -> None:
    d = date(2026, 1, 1)
    q = "Điều khiển xe không quan sát gây tai nạn giao thông bị trừ bao nhiêu điểm?"
    g = ctx.retrieve(q, d, "G")
    assert g.analysis.question_type == "tru_diem"
    graph = [p for p in g.pool if any(s.source == "graph" for s in p.sources)]
    assert graph, "G phải có chunk/provenance từ đồ thị"
    for p in graph:
        for s in p.sources:
            if s.source == "graph":
                assert s.edge_type and s.hop in (1, 2) and s.seed and s.node
    a1 = ctx.retrieve(q, d, "A1")
    assert not any(s.source == "graph" for p in a1.pool for s in p.sources)


def test_question_date_used_without_param(ctx) -> None:
    r = ctx.retrieve("Từ ngày 15/08/2026 " + Q_CHILD[0].lower() + Q_CHILD[1:], None, "G")
    assert r.as_of == date(2026, 8, 15) and r.analysis.as_of_source == "cau_hoi"
    r2 = ctx.retrieve("Từ ngày 15/08/2026 chở trẻ em thế nào?", date(2025, 6, 1), "G")
    assert r2.as_of == date(2025, 6, 1)


def test_roundtrip_json(ctx) -> None:
    r = ctx.retrieve(Q_LANE, date(2026, 8, 15), "G", qid="q1")
    line = json.dumps(r.model_dump(mode="json"), ensure_ascii=False)
    back = RetrievalResult.model_validate(json.loads(line))
    assert back == r


def test_deterministic(ctx) -> None:
    a = ctx.retrieve(Q_LANE, date(2026, 1, 1), "G")
    b = ctx.retrieve(Q_LANE, date(2026, 1, 1), "G")
    assert a.ranked == b.ranked and [h.score for h in a.hits] == [h.score for h in b.hits]


def test_rerank_reorders(ctx) -> None:
    b3 = ctx.retrieve(Q_LANE, date(2026, 1, 1), "B3")
    assert all(p.rerank_score is not None for p in b3.pool)
    scores = [h.score for h in b3.hits]
    assert scores == sorted(scores, reverse=True)


def test_offline_reads_cache(
    tmp_path: Path,
    cfg: RetrievalConfig,
    mini_store: EmbeddedStore,
    mini_catalog,
    tables: AnalyzerTables,
) -> None:
    rr = FakeReranker()
    online = make_ctx(tmp_path, cfg, mini_store, mini_catalog, tables, reranker=rr)
    r1 = online.retrieve(Q_LANE, date(2026, 1, 1), "G")
    n = rr.n_pairs
    offline = make_ctx(tmp_path, cfg, mini_store, mini_catalog, tables, with_models=False)
    r2 = offline.retrieve(Q_LANE, date(2026, 1, 1), "G")
    assert r2.ranked == r1.ranked and rr.n_pairs == n
    with pytest.raises(MissingVectorsError):
        offline.retrieve("câu hỏi chưa encode", date(2026, 1, 1), "G")
    # Câu mới đã có vector (encode trên "máy thuê") nhưng chưa có điểm rerank → lỗi rõ ràng.
    b3_key = cfg.dense_key(cfg.system("B3"))  # B3 dùng model gốc (M14)
    assert b3_key
    online.encoder.encode(b3_key, ["câu mới về dừng xe"])
    fresh = make_ctx(tmp_path, cfg, mini_store, mini_catalog, tables, with_models=False)
    with pytest.raises(MissingRerankScoresError):
        fresh.retrieve("câu mới về dừng xe", date(2026, 1, 1), "B3")
    assert fresh.retrieve("câu mới về dừng xe", date(2026, 1, 1), "B1").hits


def test_a3_uses_base_models_g_uses_finetuned(ctx) -> None:
    """M14: G dùng model_key/reranker_key (bản fine-tune); A3, B3 ghi tường minh model gốc."""
    cfg = ctx.cfg
    g = ctx.retrieve(Q_LANE, date(2026, 1, 1), "G")
    a3 = ctx.retrieve(Q_LANE, date(2026, 1, 1), "A3")
    b3 = ctx.retrieve(Q_LANE, date(2026, 1, 1), "B3")
    assert g.embedding.key == cfg.model_key == "aiteamvn-vi-emb-ft"
    assert g.reranker.key == cfg.reranker_key == "aiteamvn-reranker-ft"
    for r in (a3, b3):
        assert r.embedding.key == "aiteamvn-vi-emb" and r.reranker.key == "aiteamvn-reranker"
    assert g.embedding.revision != a3.embedding.revision


def test_reserve_graph_slots_unit() -> None:
    from trafficlaw.retrieval.retrieve import SourceInfo, reserve_graph_slots

    g, b = [SourceInfo(source="graph")], [SourceInfo(source="rrf")]
    src = {"a": b, "b": b, "c": g, "d": b, "e": g}
    ranked = ["a", "b", "c", "d", "e"]
    assert reserve_graph_slots(ranked, src, 3, 0) == ranked
    assert reserve_graph_slots(ranked, src, 3, 1) == ["a", "b", "c", "d", "e"]
    assert reserve_graph_slots(["a", "b", "d", "c", "e"], src, 3, 1) == ["a", "b", "c", "d", "e"]
    assert reserve_graph_slots(["a", "b", "d", "c", "e"], src, 3, 2) == ["a", "c", "e", "b", "d"]


def test_reserved_slot_in_config(ctx, mini_catalog: ChunkCatalog) -> None:
    d = date(2026, 1, 1)
    q = "Điều khiển xe không quan sát gây tai nạn giao thông bị trừ bao nhiêu điểm?"
    ctx.cfg = ctx.cfg.model_copy(deep=True)
    ctx.cfg.configs["G"].reserved_graph_slots = 1
    r = ctx.retrieve(q, d, "G")
    graph_only = {p.chunk_id for p in r.pool if all(s.source == "graph" for s in p.sources)}
    if graph_only:
        assert any(h.chunk_id in graph_only for h in r.hits)
    assert set(r.ranked) <= mini_catalog.ids_at(d)


def test_per_config_expand_override(tmp_path: Path, cfg, mini_store, mini_catalog, tables) -> None:
    """M13c: ``SystemSpec.expand`` ghi đè bảng expand chung cho riêng cấu hình đó."""
    from trafficlaw.retrieval.config import ExpandRule, ExpandSpec

    c = cfg.model_copy(deep=True)
    only_dc = c.system("G").model_copy(
        update={"expand": ExpandSpec(default=ExpandRule(edge_types=["DAN_CHIEU"]), by_type={})}
    )
    c.configs["XT"] = only_dc
    ctx = make_ctx(tmp_path, c, mini_store, mini_catalog, tables)
    q = "Điều khiển xe không quan sát gây tai nạn giao thông bị trừ bao nhiêu điểm?"
    d = date(2026, 1, 1)
    g = ctx.retrieve(q, d, "G")
    x = ctx.retrieve(q, d, "XT")
    assert g.analysis.question_type == x.analysis.question_type == "tru_diem"
    edges = lambda r: {s.edge_type for p in r.pool for s in p.sources if s.source == "graph"}  # noqa: E731
    assert edges(g) & {"BI_XU_PHAT", "BI_TRU_DIEM"}
    assert edges(x) <= {"DAN_CHIEU"}


def test_dev_variants_declared(cfg) -> None:
    """Biến thể M13c chỉ khác G ở expand / reserved_graph_slots."""
    g = cfg.system("G").model_dump(exclude={"description", "expand", "reserved_graph_slots"})
    for name in ("XG_r1", "XG_all2", "XG_all2_r1"):
        x = cfg.system(name).model_dump(exclude={"description", "expand", "reserved_graph_slots"})
        assert x == g, name
    assert cfg.system("XG_all2").expand.rule_for("muc_phat").hops == 2
