"""Kiểm tra danh mục thật ``data/registry/documents.yaml`` (không cần ``data/raw``)."""

from collections import Counter
from pathlib import Path

import pytest

from trafficlaw.registry.loader import Registry, load_registry
from trafficlaw.registry.validator import Issue, validate_registry

ROOT = Path(__file__).resolve().parents[2]
DOCUMENTS = ROOT / "data" / "registry" / "documents.yaml"

AMENDMENTS = {
    "ND184-2025",
    "ND236-2026",
    "ND238-2026",
    "ND241-2026",
    "ND218-2026",
    "TT13-2025-BCA",
    "TT17-2026-BXD",
}


@pytest.fixture(scope="module")
def reg() -> Registry:
    return load_registry(DOCUMENTS)


@pytest.fixture(scope="module")
def issues(reg: Registry) -> list[Issue]:
    return validate_registry(reg)


def test_36_documents(reg: Registry) -> None:
    assert len(reg) == 36
    assert len({d.doc_id for d in reg}) == 36


def test_tiers_match_claude_md(reg: Registry) -> None:
    # Bảng mục 6: A 11 + B 9 + C 3 + historical 4 + vbhn 3, cộng 7 văn bản sửa đổi
    # (TT 13/2025 đã nằm trong danh sách B).
    primary = Counter(d.tier for d in reg if not d.is_amendment or d.doc_id == "TT13-2025-BCA")
    assert primary == {"A": 11, "B": 9, "C": 3, "historical": 4, "vbhn": 3}
    assert {d.doc_id for d in reg if d.is_amendment} == AMENDMENTS


def test_no_errors(issues: list[Issue]) -> None:
    errors = [str(i) for i in issues if i.level == "error"]
    assert errors == []


@pytest.mark.parametrize(
    ("doc_id", "code", "field"),
    [
        ("ND218-2026", "MISSING_HIEU_LUC_TU", "hieu_luc_tu"),
        ("TT71-2024-BCA", "MISSING_NGAY_BAN_HANH", "ngay_ban_hanh"),
        ("TT72-2024-BCA", "MISSING_NGAY_BAN_HANH", "ngay_ban_hanh"),
        ("TT73-2024-BCA", "MISSING_NGAY_BAN_HANH", "ngay_ban_hanh"),
        ("TT12-2025-BCA", "MISSING_NGAY_BAN_HANH", "ngay_ban_hanh"),
        ("VBHN65-2026-BXD", "MISSING_NGAY_BAN_HANH", "ngay_ban_hanh"),
    ],
)
def test_known_missing_dates_reported_not_filled(
    reg: Registry, issues: list[Issue], doc_id: str, code: str, field: str
) -> None:
    assert getattr(reg[doc_id], field) is None
    assert any(i.doc_id == doc_id and i.code == code and i.level == "warning" for i in issues)


@pytest.mark.parametrize("doc_id", ["VBHN144-2026-LQ-VPQH", "TT13-2025-BCA"])
def test_known_issues_listed(issues: list[Issue], doc_id: str) -> None:
    assert any(i.doc_id == doc_id and i.code == "KNOWN_ISSUE" for i in issues)


def test_vbhn_targets(reg: Registry) -> None:
    targets = {d.doc_id: [r.target for r in d.relations] for d in reg if d.tier == "vbhn"}
    assert targets == {
        "VBHN55-VPQH": ["LUAT36-2024"],
        "VBHN144-2026-LQ-VPQH": ["LUAT35-2024"],
        "VBHN65-2026-BXD": ["ND165-2024"],
    }


def test_indexable_excludes_vbhn_and_amendments(reg: Registry) -> None:
    ids = {d.doc_id for d in reg.indexable()}
    assert len(ids) == 26
    assert not ids & AMENDMENTS
    assert not any(i.startswith("VBHN") for i in ids)


def test_source_paths_unique_and_under_raw(reg: Registry) -> None:
    paths = [d.source_path for d in reg if d.source_path]
    assert len(paths) == len(set(paths)) == 33
    assert all(p.startswith("data/raw/") for p in paths)
