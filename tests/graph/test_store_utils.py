"""Hàm thuần của M6: khoá cạnh, hash dữ liệu, lọc hiệu lực, nạp idempotent, .env, Neo4j props."""

from __future__ import annotations

import logging
import os
import shutil
from datetime import date
from pathlib import Path

import pytest

from trafficlaw.graph.embedded import EmbeddedStore
from trafficlaw.graph.neo4j_store import Neo4jConfig, Neo4jStore, flat_props
from trafficlaw.graph.parity import build_checks, run_parity, sample_units
from trafficlaw.graph.store import (
    GraphEdge,
    GraphNode,
    data_hash,
    edge_in_effect,
    edge_key,
    load_graph,
    pick_version,
    unit_of_version_id,
)
from trafficlaw.ingest.versions import UnitVersion, select_version
from trafficlaw.utils.env import load_dotenv, parse_dotenv
from trafficlaw.utils.logging import SecretRedactFilter

MINI = Path(__file__).resolve().parents[1] / "fixtures/mini_graph"


def test_edge_key_stable_and_distinct() -> None:
    a = edge_key("SUA_DOI", "X", "Y", {"cap": "van_ban", "n": 1})
    assert a == edge_key("SUA_DOI", "X", "Y", {"n": 1, "cap": "van_ban"})  # thứ tự khoá
    assert a != edge_key("SUA_DOI", "X", "Y", {"cap": "unit", "n": 1})
    assert len(a) == 16


def test_unit_of_version_id() -> None:
    assert unit_of_version_id("ND168-2024/D6/K3/m@v1") == "ND168-2024/D6/K3/m"
    assert unit_of_version_id("ND168-2024/D6") == "ND168-2024/D6"
    assert unit_of_version_id("EXT:a@vb") == "EXT:a@vb"


def _v(version: int, f: str | None, t: str | None, status: str = "active") -> GraphNode:
    props = {
        "unit_id": "U",
        "version": version,
        "effective_from": f,
        "effective_to": t,
        "status": status,
        "text": "",
        "source_unit_id": None,
    }
    return GraphNode(f"U@v{version}", "PhienBan", props)


@pytest.mark.parametrize(
    "as_of",
    [date(2024, 12, 31), date(2025, 1, 1), date(2026, 6, 30), date(2026, 7, 1), date(2027, 1, 1)],
)
@pytest.mark.parametrize("include_repealed", [False, True])
def test_pick_version_matches_select_version(as_of: date, include_repealed: bool) -> None:
    nodes = [_v(0, "2025-01-01", "2026-06-30"), _v(1, "2026-07-01", None, "repealed")]
    uvs = [UnitVersion.model_validate(n.props) for n in nodes]
    got = pick_version(nodes, as_of, include_repealed=include_repealed)
    exp = select_version(uvs, as_of, include_repealed=include_repealed)
    assert (got.props["version"] if got else None) == (exp.version if exp else None)


def test_pick_version_null_from() -> None:
    assert pick_version([_v(0, None, None)], date(2026, 1, 1)) is None


def test_edge_in_effect() -> None:
    legal = GraphEdge.make(
        "SUA_DOI", "A", "B", {"effective_from": "2026-08-15", "effective_to": None}
    )
    assert not edge_in_effect(legal, date(2026, 8, 14))
    assert edge_in_effect(legal, date(2026, 8, 15))
    assert edge_in_effect(legal, None)
    nulls = GraphEdge.make("HOP_NHAT", "A", "B", {"effective_from": None, "effective_to": None})
    assert not edge_in_effect(nulls, date(2026, 1, 1))
    struct = GraphEdge.make("THUOC", "A", "B")
    assert edge_in_effect(struct, date(1990, 1, 1))
    closed = GraphEdge.make(
        "DAN_CHIEU", "A", "B", {"effective_from": "2025-01-01", "effective_to": "2026-08-14"}
    )
    assert edge_in_effect(closed, date(2026, 8, 14))
    assert not edge_in_effect(closed, date(2026, 8, 15))


def test_data_hash_changes_with_content(tmp_path: Path) -> None:
    for f in MINI.glob("*.jsonl"):
        shutil.copy(f, tmp_path / f.name)
    h1 = data_hash(tmp_path)
    assert h1 == data_hash(MINI)
    with (tmp_path / "edges_legal.jsonl").open("a", encoding="utf-8") as fh:
        fh.write("\n")
    assert data_hash(tmp_path) != h1


def test_load_graph_idempotent() -> None:
    s = EmbeddedStore()
    first = load_graph(s, MINI)
    assert first.action == "loaded" and first.ok
    meta = s.meta()
    assert meta is not None and meta["data_hash"] == first.data_hash
    assert load_graph(s, MINI).action == "skipped"
    assert load_graph(s, MINI, force=True).action == "loaded"
    # Lần nạp trước bị ngắt (meta không khớp) → nạp lại, không nhân đôi.
    s.set_meta({})
    again = load_graph(s, MINI)
    assert again.action == "loaded" and again.actual == first.expected


def test_upsert_edge_dangling_raises() -> None:
    s = EmbeddedStore()
    s.upsert_nodes([GraphNode("A", "Dieu")])
    with pytest.raises(KeyError):
        s.upsert_edges([GraphEdge.make("THUOC", "A", "B")])


def test_upsert_relabel() -> None:
    s = EmbeddedStore()
    s.upsert_nodes([GraphNode("A", "Dieu", {"x": 1})])
    s.upsert_nodes([GraphNode("A", "Khoan", {"x": 2})])
    assert s.nodes_by_label("Dieu") == []
    assert s.get_node("A") == GraphNode("A", "Khoan", {"x": 2})


def test_parity_detects_difference() -> None:
    a = EmbeddedStore.from_dir(MINI)
    b = EmbeddedStore.from_dir(MINI)
    n = b.get_node("ND168-2024/D6/K3/m@v1")
    assert n is not None
    b.upsert_nodes([GraphNode(n.id, n.label, {**n.props, "text": "khác"})])
    units = sample_units(a, 300)
    c = a.count()
    checks = build_checks(units, [], node_labels=list(c["nodes"]), edge_types=list(c["edges"]))
    bad = {(r["api"], r["args"].get("unit_id")) for r in run_parity(a, b, checks) if not r["ok"]}
    assert ("nodes_by_label", None) in bad
    assert ("version_at", "ND168-2024/D6/K3/m") in bad


def test_sample_units_deterministic_and_stratified() -> None:
    s = EmbeddedStore.from_dir(MINI)
    a, b = sample_units(s, 20, seed=42), sample_units(s, 20, seed=42)
    assert a == b and len(a) == 20
    assert {u.split("/")[0] for u in a} == {"LUAT36-2024", "ND168-2024"}


def test_flat_props() -> None:
    p = {
        "a": 1,
        "b": None,
        "c": [{"x": 1}],
        "d": ["x", "y"],
        "e": [1, "x"],
        "f": True,
        "id": "bad",
        "g": [],
        "h": 1.5,
    }
    assert flat_props(p) == {"a": 1, "d": ["x", "y"], "f": True, "h": 1.5}


def test_neo4j_config_from_env() -> None:
    assert Neo4jConfig.from_env({"NEO4J_URI": "neo4j+s://x"}) is None
    cfg = Neo4jConfig.from_env(
        {"NEO4J_URI": "neo4j+s://x", "NEO4J_USERNAME": "u", "NEO4J_PASSWORD": "secret-pw"}
    )
    assert cfg is not None and cfg.database is None
    assert "secret-pw" not in repr(cfg)


def test_neo4j_store_rejects_bad_prefix() -> None:
    cfg = Neo4jConfig("bolt://x", "u", "p")
    with pytest.raises(ValueError):
        Neo4jStore(cfg, label_prefix="T`) DETACH DELETE", driver=object())


def test_parse_dotenv() -> None:
    text = "# c\nexport A=1\nB = 'x y'\nC=\"q#z\"\nD=v # comment\nbad line\n"
    assert parse_dotenv(text) == {"A": "1", "B": "x y", "C": "q#z", "D": "v"}


def test_load_dotenv_no_override(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    p = tmp_path / ".env"
    p.write_text("M6_TEST_A=from_file\nM6_TEST_B=b\n", encoding="utf-8")
    monkeypatch.setenv("M6_TEST_A", "from_env")
    monkeypatch.delenv("M6_TEST_B", raising=False)
    assert load_dotenv(p) == ["M6_TEST_B"]
    assert os.environ["M6_TEST_A"] == "from_env" and os.environ["M6_TEST_B"] == "b"
    monkeypatch.delenv("M6_TEST_B")
    assert load_dotenv(tmp_path / "missing.env") == []


def test_neo4j_password_redacted(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NEO4J_PASSWORD", "super-secret-123")
    rec = logging.LogRecord("x", logging.INFO, "f", 1, "pw=%s", ("super-secret-123",), None)
    SecretRedactFilter().filter(rec)
    assert "super-secret-123" not in rec.getMessage()
