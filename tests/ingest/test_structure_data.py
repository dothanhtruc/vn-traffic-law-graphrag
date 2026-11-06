"""M3 trên dữ liệu thật ``data/interim`` (skip nếu không có, vd. trên CI)."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from trafficlaw.ingest.manifest import IngestConfig
from trafficlaw.ingest.structure import parse_structure

REPO_ROOT = Path(__file__).resolve().parents[2]
INTERIM = REPO_ROOT / "data/interim"
CFG = IngestConfig.model_validate(
    yaml.safe_load((REPO_ROOT / "configs/ingest.yaml").read_text(encoding="utf-8"))
)

pytestmark = pytest.mark.skipif(
    not (INTERIM / "LUAT36-2024.txt").is_file(), reason="không có data/interim"
)


def test_expected_list_covers_33_documents() -> None:
    assert len(CFG.expected_dieu) == 33


@pytest.mark.parametrize("doc_id", sorted(CFG.expected_dieu))
def test_dieu_count_and_tree(doc_id: str) -> None:
    path = INTERIM / f"{doc_id}.txt"
    if not path.is_file():
        pytest.skip(f"không có {path.name}")
    res = parse_structure(doc_id, path.read_text(encoding="utf-8"))
    exp = CFG.expected_dieu[doc_id]
    r = res.report
    assert (r.n_dieu, r.last_dieu) == (exp.count, exp.last)
    assert r.dieu_missing == [] and r.unclosed_quote_line is None
    assert not [a for a in r.anomalies if a.kind == "unclosed_quote"]
    ids = [u.id for u in res.units]
    assert len(ids) == len(set(ids))
    known = set(ids)
    assert all(u.parent_id is None or u.parent_id in known for u in res.units)
    assert all(not ln.startswith("[^") for u in res.units for ln in u.text.split("\n"))


def test_nd168_dieu6_has_16_khoan_and_k5_a_to_q() -> None:
    res = parse_structure("ND168-2024", (INTERIM / "ND168-2024.txt").read_text(encoding="utf-8"))
    kids = [u for u in res.units if u.parent_id == "ND168-2024/D6"]
    assert [u.number for u in kids] == [str(n) for n in range(1, 17)]
    k5 = [u.number for u in res.units if u.parent_id == "ND168-2024/D6/K5"]
    assert k5 == list("abcd") + ["đ"] + list("eghiklmnopq")


def test_vbhn65_has_dieu_52a() -> None:
    res = parse_structure(
        "VBHN65-2026-BXD", (INTERIM / "VBHN65-2026-BXD.txt").read_text(encoding="utf-8")
    )
    assert "52a" in res.report.dieu_numbers
