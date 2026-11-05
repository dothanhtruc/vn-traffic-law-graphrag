"""Kiểm tra danh mục thật ``data/registry/documents.yaml`` (không cần ``data/raw``)."""

from collections import Counter
from datetime import date
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


EXCLUDED = {"LUAT26-2001", "LUAT23-2008", "ND100-2019"}


def test_33_documents(reg: Registry) -> None:
    # 36 văn bản của Phase 2 bỏ 3 văn bản đã hết hiệu lực (quyết định người dùng 05/11/2026).
    assert len(reg) == 33
    assert len({d.doc_id for d in reg}) == 33
    assert not EXCLUDED & {d.doc_id for d in reg}


def test_tiers_match_claude_md(reg: Registry) -> None:
    # Bảng mục 6: A 11 + B 9 + C 3 + historical 1 + vbhn 3, cộng 7 văn bản sửa đổi
    # (TT 13/2025 đã nằm trong danh sách B).
    primary = Counter(d.tier for d in reg if not d.is_amendment or d.doc_id == "TT13-2025-BCA")
    assert primary == {"A": 11, "B": 9, "C": 3, "historical": 1, "vbhn": 3}
    assert {d.doc_id for d in reg if d.is_amendment} == AMENDMENTS


def test_no_errors(issues: list[Issue]) -> None:
    errors = [str(i) for i in issues if i.level == "error"]
    assert errors == []


@pytest.mark.parametrize(
    ("doc_id", "field", "value"),
    [
        # Theo chính văn bản gốc (người dùng xác nhận 05/11/2026).
        ("TT12-2025-BCA", "ngay_ban_hanh", date(2025, 2, 28)),
        ("TT71-2024-BCA", "ngay_ban_hanh", date(2024, 11, 12)),
        ("TT72-2024-BCA", "ngay_ban_hanh", date(2024, 11, 13)),
        ("TT73-2024-BCA", "ngay_ban_hanh", date(2024, 11, 15)),
        ("ND218-2026", "hieu_luc_tu", date(2026, 8, 10)),
        # Theo bản tổng hợp Phase 2.
        ("TT52-2024-BGTVT", "ngay_ban_hanh", date(2024, 11, 15)),
        ("VBHN55-VPQH", "ngay_ban_hanh", date(2026, 3, 23)),
        # Ngày quy ước do người dùng chốt (Phase 2 chỉ ghi "~08/2026").
        ("VBHN65-2026-BXD", "ngay_ban_hanh", date(2026, 8, 1)),
    ],
)
def test_resolved_values(reg: Registry, doc_id: str, field: str, value: object) -> None:
    assert getattr(reg[doc_id], field) == value


def test_no_warnings(issues: list[Issue]) -> None:
    assert [str(i) for i in issues if i.level == "warning"] == []


def test_no_relation_to_excluded(reg: Registry) -> None:
    assert not {r.target for d in reg for r in d.relations} & EXCLUDED
    nd218 = reg["ND218-2026"].relations[0]
    assert nd218.effective_from == date(2026, 8, 10)


@pytest.mark.parametrize("doc_id", ["TT13-2025-BCA", "ND168-2024", "VBHN65-2026-BXD"])
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
    assert len(ids) == 23
    assert not ids & AMENDMENTS
    assert not any(i.startswith("VBHN") for i in ids)


def test_source_paths_unique_and_under_raw(reg: Registry) -> None:
    paths = [d.source_path for d in reg if d.source_path]
    assert len(paths) == len(set(paths)) == 33
    assert all(p.startswith("data/raw/") for p in paths)
