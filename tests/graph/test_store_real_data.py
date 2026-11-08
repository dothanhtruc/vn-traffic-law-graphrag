"""M6 trên dữ liệu thật ``data/graph`` (skip nếu chưa chạy ``scripts.build_graph``)."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from trafficlaw.graph.embedded import EmbeddedStore
from trafficlaw.graph.store import UNIT_LABELS, count_items, load_graph_dir, pick_version
from trafficlaw.ingest.versions import VersionStore

REPO_ROOT = Path(__file__).resolve().parents[2]
GRAPH = REPO_ROOT / "data/graph"
VERSIONS = REPO_ROOT / "data/processed/unit_versions.jsonl"
DATES = (date(2025, 1, 1), date(2026, 1, 1), date(2026, 7, 1), date(2026, 8, 15))

pytestmark = pytest.mark.skipif(
    not (GRAPH / "edges_legal.jsonl").is_file() or not VERSIONS.is_file(),
    reason="chưa có data/graph hoặc unit_versions.jsonl",
)


@pytest.fixture(scope="module")
def real() -> EmbeddedStore:
    return EmbeddedStore.from_dir(GRAPH)


@pytest.fixture(scope="module")
def vstore() -> VersionStore:
    return VersionStore.load(VERSIONS)


def test_counts_match_jsonl(real: EmbeddedStore) -> None:
    nodes, edges = load_graph_dir(GRAPH)
    assert real.count() == count_items(nodes, edges)


@pytest.mark.parametrize("include_repealed", [False, True])
def test_version_at_matches_version_store(
    real: EmbeddedStore, vstore: VersionStore, include_repealed: bool
) -> None:
    """Toàn bộ unit × 4 mốc: phiên bản của GraphStore trùng ``VersionStore.get_version``."""
    uids = vstore.unit_ids()
    vm = real.versions_map(uids)
    bad = []
    for uid in uids:
        for d in DATES:
            got = pick_version(vm[uid], d, include_repealed=include_repealed)
            exp = vstore.get_version(uid, d, include_repealed=include_repealed)
            if (got.props["version"] if got else None) != (exp.version if exp else None):
                bad.append((uid, d))
    assert len(uids) > 9000
    assert bad == []


def test_version_at_api_text(real: EmbeddedStore, vstore: VersionStore) -> None:
    for uid in vstore.unit_ids()[::97]:
        for d in DATES:
            got = real.version_at(uid, d)
            exp = vstore.get_version(uid, d)
            assert (got.props["text"] if got else None) == (exp.text if exp else None)


def test_subtree_covers_all_units(real: EmbeddedStore) -> None:
    """Mỗi văn bản: duyệt cây con từ VanBan phủ đúng mọi unit của nó (chuỗi KE_TIEP không đứt)."""
    for doc in real.nodes_by_label("VanBan"):
        st = real.subtree(doc.id)
        assert len(st) == len(set(st))
        units = {n.id for lb in UNIT_LABELS for n in real.nodes_by_label(lb, doc_id=doc.id)}
        assert set(st) - {doc.id} == units, doc.id
