"""Fixture GraphStore dùng chung cho test M6 (EmbeddedStore; Neo4jStore khi có biến môi trường)."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest

from trafficlaw.graph.embedded import EmbeddedStore
from trafficlaw.graph.neo4j_store import Neo4jStore
from trafficlaw.graph.store import BaseGraphStore, load_graph
from trafficlaw.utils.env import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[2]
MINI = REPO_ROOT / "tests/fixtures/mini_graph"
#: Không gian tên riêng cho test trên database Aura (không đụng dữ liệu thật).
TEST_PREFIX = "T_"


def neo4j_test_store() -> Neo4jStore | None:
    load_dotenv(REPO_ROOT / ".env")
    return Neo4jStore.from_env(label_prefix=TEST_PREFIX, batch_size=200)


@pytest.fixture(scope="session")
def embedded_mini() -> EmbeddedStore:
    return EmbeddedStore.from_dir(MINI)


@pytest.fixture(scope="session")
def neo4j_mini() -> Iterator[Neo4jStore]:
    store = neo4j_test_store()
    if store is None:
        pytest.skip("thiếu NEO4J_URI / NEO4J_USERNAME / NEO4J_PASSWORD")
    try:
        load_graph(store, MINI)
        yield store
    finally:
        store.clear()
        store.close()


@pytest.fixture(
    params=[
        pytest.param("embedded"),
        pytest.param("neo4j", marks=pytest.mark.slow),
    ]
)
def store(request: pytest.FixtureRequest) -> BaseGraphStore:
    name = "embedded_mini" if request.param == "embedded" else "neo4j_mini"
    return request.getfixturevalue(name)
