"""M4: pipeline áp sửa đổi trên thư mục tạm (resume, xoá bản ghi cũ, todo CSV, bất biến)."""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

from tests.ingest.m4_helpers import registry, units_of
from trafficlaw.ingest.amendment_pipeline import latest_reports, run_amendments
from trafficlaw.ingest.vbhn import VbhnEntry
from trafficlaw.ingest.versions import AddedUnit, VersionStore
from trafficlaw.registry.loader import Registry
from trafficlaw.utils.jsonl import read_jsonl, write_jsonl

FULL = registry()
KEEP = {"ND168-2024", "ND238-2026", "ND165-2024", "ND241-2026", "VBHN65-2026-BXD"}


def _small_registry() -> Registry:
    return Registry([d for d in FULL if d.doc_id in KEEP])


def _write_units(path: Path, nd165_extra: bool = False) -> None:
    units = (
        units_of("ND168-2024", "nd168_dieu6_k1_k3.txt", "nd168_dieu53.txt")
        + units_of("ND238-2026", "nd238_dieu1_2.txt", "nd238_dieu18_20.txt")
        + units_of(
            "ND165-2024",
            "nd165_dieu4.txt",
            *(["nd165_dieu6.txt", "nd165_dieu17.txt"] if nd165_extra else ["nd165_dieu6.txt"]),
        )
        + units_of("ND241-2026", "nd241_dieu1.txt", "nd241_dieu25_26.txt")
        + units_of("VBHN65-2026-BXD", "vbhn65_dieu4.txt")
    )
    write_jsonl(path, units)


def _run(tmp: Path, **kw):  # type: ignore[no-untyped-def]
    vbhn = [
        VbhnEntry(
            vbhn="VBHN65-2026-BXD",
            base_doc="ND165-2024",
            as_of=date(2026, 7, 1),
            out_of_registry_sources=["243/2025/NĐ-CP"],
        )
    ]
    return run_amendments(
        units_path=tmp / "units.jsonl",
        versions_path=tmp / "unit_versions.jsonl",
        added_path=tmp / "units_added.jsonl",
        report_path=tmp / "amendment_report.jsonl",
        todo_path=tmp / "amendment_todo.csv",
        registry=_small_registry(),
        vbhn_map=vbhn,
        label_fixes=[],
        git_commit="abc",
        **kw,
    )


def test_run_resume_and_rerun_only_changed_target(tmp_path: Path) -> None:
    _write_units(tmp_path / "units.jsonl")
    out = _run(tmp_path)
    assert {o.doc_id: o.action for o in out} == {
        "ND168-2024": "processed",
        "ND165-2024": "processed",
    }
    n_versions = len(list(read_jsonl(tmp_path / "unit_versions.jsonl")))
    # lần 2: bỏ qua toàn bộ, không ghi thêm
    out2 = _run(tmp_path)
    assert {o.action for o in out2} == {"skipped"}
    assert len(list(read_jsonl(tmp_path / "unit_versions.jsonl"))) == n_versions
    # đổi unit của ND165 → chỉ ND165 chạy lại, bản ghi cũ của nó bị xoá trước
    _write_units(tmp_path / "units.jsonl", nd165_extra=True)
    out3 = _run(tmp_path)
    assert {o.doc_id: o.action for o in out3} == {
        "ND168-2024": "skipped",
        "ND165-2024": "processed",
    }
    rows = list(read_jsonl(tmp_path / "unit_versions.jsonl"))
    keys = [(r["unit_id"], r["version"]) for r in rows]
    assert len(keys) == len(set(keys))  # không trùng
    st = VersionStore.load(tmp_path / "unit_versions.jsonl")
    assert st.get_version("ND165-2024/D17/K1/d", date(2026, 7, 1)) is None  # bãi bỏ (ND241 Đ25 K5)
    assert st.get_version("ND165-2024/D17/K1/d", date(2026, 6, 30)) is not None


def test_outputs_are_consistent(tmp_path: Path) -> None:
    _write_units(tmp_path / "units.jsonl")
    _run(tmp_path)
    added = [AddedUnit.model_validate(r) for r in read_jsonl(tmp_path / "units_added.jsonl")]
    base = {r["id"] for r in read_jsonl(tmp_path / "units.jsonl")}
    ids = base | {a.id for a in added}
    assert all(r["unit_id"] in ids for r in read_jsonl(tmp_path / "unit_versions.jsonl"))
    assert "ND168-2024/D6/K1a" in {a.id for a in added}
    rep = latest_reports(tmp_path / "amendment_report.jsonl")
    assert rep["ND168-2024"]["instructions"]["ND238-2026"]["insert"][0] >= 1
    with (tmp_path / "amendment_todo.csv").open(encoding="utf-8-sig") as fh:
        todos = list(csv.DictReader(fh))
    reasons = {(t["doc_id"], t["reason"]) for t in todos}
    assert ("ND168-2024", "hieu_luc_sua_doi") in reasons  # ND238 Đ18 sửa Điều 53
    assert ("ND165-2024", "ngoai_danh_muc") in reasons  # ND241 Đ26 K2 (NĐ 140/2025)
