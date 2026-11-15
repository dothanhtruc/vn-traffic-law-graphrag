"""M11: graph expand trên mini_graph (ND168 Đ6 + Đ12 K10, nút ngữ nghĩa M8) ở 4 mốc."""

from __future__ import annotations

from datetime import date

import pytest

from trafficlaw.graph.embedded import EmbeddedStore
from trafficlaw.retrieval.catalog import ChunkCatalog
from trafficlaw.retrieval.config import ExpandRule
from trafficlaw.retrieval.graph_expand import expand_candidates, sanction_index

from .conftest import DATES

DC = ExpandRule(edge_types=["DAN_CHIEU"], hops=1)
SANC = ExpandRule(edge_types=["BI_XU_PHAT", "BI_TRU_DIEM", "DAN_CHIEU"], hops=1)


def _run(store, cat, seed_unit: str, as_of: date | None, rule: ExpandRule, **kw):
    seeds = [(c, seed_unit) for c in cat.chunks_of_unit(seed_unit, as_of)[:1]]
    assert seeds, f"không có chunk seed cho {seed_unit} tại {as_of}"
    return seeds[0][0], expand_candidates(
        store, seeds, as_of=as_of, rule=rule, catalog=cat, sanctions=sanction_index(store), **kw
    )


@pytest.mark.parametrize("d", DATES)
def test_dan_chieu_hop1(mini_store: EmbeddedStore, mini_catalog: ChunkCatalog, d: date) -> None:
    seed, exps = _run(mini_store, mini_catalog, "ND168-2024/D12/K10", d, DC)
    got = {x.chunk_id for x in exps if x.chunk_id}
    # Đ12 K10 dẫn chiếu điểm b, d khoản 11 Điều 6 → chunk Khoản 11 hiệu lực tại d.
    assert got == {c for c in mini_catalog.chunks_of_unit("ND168-2024/D6/K11", d)}
    assert all(x.edge_type == "DAN_CHIEU" and x.hop == 1 and x.seed == seed for x in exps)
    live = mini_catalog.ids_at(d)
    assert got <= live


@pytest.mark.parametrize("d", DATES)
def test_never_expired_chunks(
    mini_store: EmbeddedStore, mini_catalog: ChunkCatalog, d: date
) -> None:
    live = mini_catalog.ids_at(d)
    seeds = [(c, mini_catalog.get(c).unit_id) for c in sorted(live)]
    exps = expand_candidates(
        mini_store,
        seeds,
        as_of=d,
        rule=ExpandRule(edge_types=["DAN_CHIEU", "BI_XU_PHAT", "BI_TRU_DIEM", "HUONG_DAN"], hops=2),
        catalog=mini_catalog,
        sanctions=sanction_index(mini_store),
        max_chunks=1000,
    )
    assert exps
    assert {x.chunk_id for x in exps if x.chunk_id} <= live


def test_hop2_reaches_further(mini_store: EmbeddedStore, mini_catalog: ChunkCatalog) -> None:
    d = date(2026, 7, 1)
    _, h1 = _run(mini_store, mini_catalog, "ND168-2024/D12/K10", d, DC)
    _, h2 = _run(
        mini_store,
        mini_catalog,
        "ND168-2024/D12/K10",
        d,
        ExpandRule(edge_types=["DAN_CHIEU"], hops=2),
    )
    c1 = {x.chunk_id for x in h1 if x.chunk_id}
    c2 = {x.chunk_id for x in h2 if x.chunk_id}
    assert c1 <= c2
    assert all(x.hop in (1, 2) for x in h2)
    if c2 - c1:
        assert any(x.hop == 2 for x in h2)


def test_edge_types_respected(mini_store: EmbeddedStore, mini_catalog: ChunkCatalog) -> None:
    d = date(2026, 1, 1)
    _, only_dc = _run(mini_store, mini_catalog, "ND168-2024/D6/K10", d, DC, reverse=False)
    assert all(x.edge_type == "DAN_CHIEU" for x in only_dc)
    _, sanc = _run(mini_store, mini_catalog, "ND168-2024/D6/K10", d, SANC, reverse=False)
    # Hành vi Đ6 K10 a/b bị trừ điểm theo điểm d khoản 16 (cạnh BI_TRU_DIEM nguon=dan_chieu):
    # nút DiemGPLX → props.unit_id → chunk Khoản 16.
    k16 = set(mini_catalog.chunks_of_unit("ND168-2024/D6/K16", d))
    hit = [x for x in sanc if x.chunk_id in k16]
    assert hit and any(x.edge_type == "BI_TRU_DIEM" and x.node.startswith("DIEM:") for x in hit)
    # (K16 d cũng dẫn chiếu ngược vào K10 bằng DAN_CHIEU ⇒ only_dc cũng tới K16, nhưng không qua
    # nút ngữ nghĩa.)
    assert not any(x.node.startswith(("DIEM:", "CHETAI:", "BPBS:")) for x in only_dc)


def test_reverse_sanctions(mini_store: EmbeddedStore, mini_catalog: ChunkCatalog) -> None:
    d = date(2026, 1, 1)
    _, rev = _run(mini_store, mini_catalog, "ND168-2024/D6/K16", d, SANC)
    k10 = set(mini_catalog.chunks_of_unit("ND168-2024/D6/K10", d))
    back = [x for x in rev if x.direction == "nguoc"]
    assert k10 & {x.chunk_id for x in back}
    assert all(x.edge_type in ("BI_XU_PHAT", "BI_TRU_DIEM") and x.hop == 1 for x in back)
    _, no_rev = _run(mini_store, mini_catalog, "ND168-2024/D6/K16", d, SANC, reverse=False)
    assert not any(x.direction == "nguoc" for x in no_rev)


def test_versions_by_date(mini_store: EmbeddedStore, mini_catalog: ChunkCatalog) -> None:
    """Đ6 K3 đổi trạng thái 01/01/2026 và 15/08/2026: chunk ánh xạ phải đúng trạng thái."""
    want = {
        date(2025, 1, 1): "ND168-2024/D6/K3#2025-01-01",
        date(2026, 1, 1): "ND168-2024/D6/K3#2026-01-01",
        date(2026, 7, 1): "ND168-2024/D6/K3#2026-01-01",
        date(2026, 8, 15): "ND168-2024/D6/K3#2026-08-15",
    }
    for d, c in want.items():
        assert mini_catalog.chunks_of_unit("ND168-2024/D6/K3/m", d) == [c]
    # Khoản bổ sung 1a chỉ có từ 15/08/2026.
    assert mini_catalog.chunks_of_unit("ND168-2024/D6/K1a", date(2026, 7, 1)) == []
    assert mini_catalog.chunks_of_unit("ND168-2024/D6/K1a", date(2026, 8, 15))
    # Không lọc (A2) → mọi trạng thái.
    assert len(mini_catalog.chunks_of_unit("ND168-2024/D6/K3", None)) == 3
    # Điều chia Khoản → các Khoản, theo thứ tự danh mục.
    d6 = mini_catalog.chunks_of_unit("ND168-2024/D6", date(2026, 1, 1))
    assert d6[0].startswith("ND168-2024/D6/K1#")


def test_cap_and_determinism(mini_store: EmbeddedStore, mini_catalog: ChunkCatalog) -> None:
    d = date(2026, 1, 1)
    live = sorted(mini_catalog.ids_at(d))
    seeds = [(c, mini_catalog.get(c).unit_id) for c in live[:5]]
    kw = dict(as_of=d, rule=SANC, catalog=mini_catalog, sanctions=sanction_index(mini_store))
    a = expand_candidates(mini_store, seeds, max_chunks=2, **kw)
    b = expand_candidates(mini_store, seeds, max_chunks=2, **kw)
    assert a == b
    seed_ids = {c for c, _ in seeds}
    assert len({x.chunk_id for x in a if x.chunk_id and x.chunk_id not in seed_ids}) <= 2


def test_document_nodes_provenance_only(
    mini_store: EmbeddedStore, mini_catalog: ChunkCatalog
) -> None:
    d = date(2026, 1, 1)
    live = sorted(mini_catalog.ids_at(d))
    seeds = [(c, mini_catalog.get(c).unit_id) for c in live]
    exps = expand_candidates(
        mini_store,
        seeds,
        as_of=d,
        rule=ExpandRule(edge_types=["DAN_CHIEU", "HUONG_DAN"], hops=1),
        catalog=mini_catalog,
        sanctions={},
        max_chunks=1000,
    )
    docs = [x for x in exps if x.chunk_id is None]
    for x in docs:
        n = mini_store.get_node(x.node)
        assert n is not None and n.label in ("VanBan", "VanBanNgoai")
