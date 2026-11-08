"""M4 trên dữ liệu thật ``data/processed`` (skip nếu chưa chạy ``scripts.apply_amendments``)."""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

import pytest

from trafficlaw.ingest.versions import VersionStore

REPO_ROOT = Path(__file__).resolve().parents[2]
PROC = REPO_ROOT / "data/processed"

pytestmark = pytest.mark.skipif(
    not (PROC / "unit_versions.jsonl").is_file(),
    reason="chưa có data/processed/unit_versions.jsonl",
)

MOC = [date(2025, 1, 1), date(2026, 1, 1), date(2026, 7, 1), date(2026, 8, 15)]


@pytest.fixture(scope="module")
def store() -> VersionStore:
    return VersionStore.load(PROC / "unit_versions.jsonl")


def _ver(store: VersionStore, uid: str, d: date) -> int | None:
    v = store.get_version(uid, d)
    return None if v is None else v.version


def test_four_dates(store: VersionStore) -> None:
    from trafficlaw.utils.dates import day_before

    def around(uid: str) -> list[tuple[int | None, int | None]]:
        return [(_ver(store, uid, day_before(d)), _ver(store, uid, d)) for d in MOC]

    assert around("ND168-2024/D6/K3/m") == [(None, None), (None, 0), (0, 0), (0, 1)]
    assert around("ND165-2024/D4/K1") == [(None, 0), (0, 0), (0, 1), (1, 1)]
    assert around("LUAT36-2024/D10/K3") == [(None, None), (None, 0), (0, 0), (0, 0)]
    assert _ver(store, "TT35-2024-BGTVT/D1", date(2025, 8, 31)) == 0
    assert _ver(store, "TT35-2024-BGTVT/D1", date(2025, 9, 1)) is None
    # ND238 Đ18 (effect_overrides, người dùng duyệt 08/11/2026)
    assert around("ND168-2024/D20/K5/l")[-1] == (0, 0)
    assert _ver(store, "ND168-2024/D20/K5/l", date(2028, 1, 1)) == 1
    assert _ver(store, "ND168-2024/D26/K7/k", date(2028, 12, 31)) is None
    assert _ver(store, "ND168-2024/D26/K7/k", date(2029, 1, 1)) == 1


def test_luat36_d9_k18_stays_original_and_listed_in_todo(store: VersionStore) -> None:
    # Quyết định 07/11/2026: Luật 118/2025 ngoài danh mục → không tạo phiên bản
    assert [v.version for v in store.versions_of("LUAT36-2024/D9/K18")] == [0]
    with (PROC / "amendment_todo.csv").open(encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    assert any(
        r["unit_id"] == "LUAT36-2024/D9/K18" and r["reason"] == "ngoai_danh_muc" for r in rows
    )


def test_no_vbhn_or_amending_documents_in_versions(store: VersionStore) -> None:
    bad = [u for u in store.unit_ids() if u.split("/")[0].startswith("VBHN")]
    bad += [
        u
        for u in store.unit_ids()
        if u.split("/")[0]
        in {
            "ND184-2025",
            "ND236-2026",
            "ND238-2026",
            "TT17-2026-BXD",
            "TT13-2025-BCA",
            "ND241-2026",
            "ND218-2026",
        }
    ]
    assert not bad
