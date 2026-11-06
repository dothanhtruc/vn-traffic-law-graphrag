"""M3: bước ``--stage structure`` — resume, không trùng unit, mã thoát của script."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from scripts import ingest as ingest_script
from trafficlaw.ingest.structure_pipeline import latest_reports, load_overrides, run_structure
from trafficlaw.utils.jsonl import append_jsonl, read_jsonl

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """Repo giả: 2 file interim (trích đoạn thật) + manifest + 1 văn bản lỗi ở M2."""
    interim = tmp_path / "data/interim"
    interim.mkdir(parents=True)
    l36 = (FIXTURES / "luat36_dieu9.txt").read_text(encoding="utf-8").replace("Điều 9.", "Điều 1.")
    (interim / "LUAT36-2024.txt").write_text(l36, encoding="utf-8")
    (interim / "ND238-2026.txt").write_text(
        (FIXTURES / "nd238_dieu1_2.txt").read_text(encoding="utf-8"), encoding="utf-8"
    )
    m = interim / "manifest.jsonl"
    for doc in ("LUAT36-2024", "ND238-2026"):
        append_jsonl(
            m,
            {
                "doc_id": doc,
                "status": "ok",
                "output_path": f"data/interim/{doc}.txt",
                "source_path": f"data/raw/{doc}.docx",
            },
        )
    append_jsonl(m, {"doc_id": "TT52-2024-BGTVT", "status": "error", "output_path": None})
    return tmp_path


def _run(repo: Path, **kw) -> list:  # type: ignore[no-untyped-def]
    return run_structure(
        repo_root=repo,
        manifest_path=repo / "data/interim/manifest.jsonl",
        units_path=repo / "data/processed/units.jsonl",
        report_path=repo / "data/processed/structure_report.jsonl",
        git_commit="abc123",
        **kw,
    )


def _actions(outcomes: list) -> dict[str, str]:
    return {o.doc_id: o.action for o in outcomes}


def _unit_ids(repo: Path) -> list[str]:
    return [r["id"] for r in read_jsonl(repo / "data/processed/units.jsonl")]


def test_first_run_writes_units_and_report(repo: Path) -> None:
    out = _run(repo)
    # Văn bản lỗi ở M2 không được xử lý.
    assert _actions(out) == {"LUAT36-2024": "processed", "ND238-2026": "processed"}
    ids = _unit_ids(repo)
    assert ids[0] == "LUAT36-2024" and "LUAT36-2024/D1/K28" in ids
    assert "ND238-2026/D2/K1" in ids and len(ids) == len(set(ids))
    units = list(read_jsonl(repo / "data/processed/units.jsonl"))
    assert units[1]["source_path"] == "data/raw/LUAT36-2024.docx"
    rep = latest_reports(repo / "data/processed/structure_report.jsonl")
    assert rep["LUAT36-2024"]["status"] == "ok" and rep["LUAT36-2024"]["git_commit"] == "abc123"
    assert len(rep["LUAT36-2024"]["interim_sha256"]) == 64
    assert rep["ND238-2026"]["report"]["n_dieu"] == 3
    assert rep["LUAT36-2024"]["n_units"] == sum(u["doc_id"] == "LUAT36-2024" for u in units)


def test_second_run_skips_everything(repo: Path) -> None:
    _run(repo)
    n = len(_unit_ids(repo))
    assert set(_actions(_run(repo)).values()) == {"skipped"}
    assert len(_unit_ids(repo)) == n


def test_changed_interim_reruns_only_that_doc_without_duplicates(repo: Path) -> None:
    _run(repo)
    p = repo / "data/interim/ND238-2026.txt"
    p.write_text("Điều 1. Mới\n1. Một khoản.\n", encoding="utf-8")
    assert _actions(_run(repo)) == {"LUAT36-2024": "skipped", "ND238-2026": "processed"}
    ids = _unit_ids(repo)
    assert [i for i in ids if i.startswith("ND238")] == [
        "ND238-2026",
        "ND238-2026/D1",
        "ND238-2026/D1/K1",
    ]
    assert len(ids) == len(set(ids))


def test_force_does_not_duplicate_units(repo: Path) -> None:
    _run(repo)
    n = len(_unit_ids(repo))
    assert set(_actions(_run(repo, force=True)).values()) == {"processed"}
    assert len(_unit_ids(repo)) == n


def test_crash_before_report_is_recovered(repo: Path) -> None:
    """Crash sau khi ghi unit nhưng trước dòng report: lần sau xử lý lại, không trùng."""
    _run(repo)
    report = repo / "data/processed/structure_report.jsonl"
    lines = report.read_text(encoding="utf-8").split("\n")
    report.write_text(lines[0] + "\n" + lines[1][:30], encoding="utf-8")  # dòng 2 bị cắt
    n = len(_unit_ids(repo))
    assert _actions(_run(repo)) == {"LUAT36-2024": "skipped", "ND238-2026": "processed"}
    assert len(_unit_ids(repo)) == n


def test_doc_id_filter(repo: Path) -> None:
    assert _actions(_run(repo, doc_ids=["ND238-2026"])) == {"ND238-2026": "processed"}
    with pytest.raises(KeyError):
        _run(repo, doc_ids=["KHONG-CO"])


def _cfg(repo: Path, expected: dict) -> Path:
    path = repo / "ingest.yaml"
    path.write_text(yaml.safe_dump({"expected_dieu": expected}), encoding="utf-8")
    return path


def test_script_exit_codes(repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    good = {"LUAT36-2024": {"count": 1, "last": "1"}, "ND238-2026": {"count": 3, "last": "3"}}
    argv = ["--stage", "structure", "--repo-root", str(repo), "--config", str(_cfg(repo, good))]
    assert ingest_script.main(argv) == 0
    out = capsys.readouterr().out
    assert "2 xử lý" in out and "đạt: 2/2" in out
    summary = (repo / "data/processed/structure_summary.md").read_text(encoding="utf-8")
    assert "| LUAT36-2024 | ok |" in summary
    # Lần 2: bỏ qua toàn bộ, vẫn đạt.
    assert ingest_script.main(argv) == 0
    assert "0 xử lý, 2 bỏ qua" in capsys.readouterr().out
    # Số Điều kỳ vọng sai → mã 1.
    bad = {**good, "ND238-2026": {"count": 4, "last": "4"}}
    argv_bad = ["--stage", "structure", "--repo-root", str(repo), "--config", str(_cfg(repo, bad))]
    assert ingest_script.main(argv_bad) == 1
    assert "≠ kỳ vọng 4" in capsys.readouterr().out


def _write_overrides(repo: Path, items: list[dict]) -> Path:
    path = repo / "data/registry/label_overrides.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump({"overrides": items}, allow_unicode=True), encoding="utf-8")
    return path


_OV = {
    "unit_id": "LUAT36-2024/D1/K2",
    "label_in_source": "2",
    "text_starts_with": "Điều khiển phương tiện",
    "reason": "thử",
    "evidence": "thử",
}


def test_changed_overrides_rerun_only_that_doc(repo: Path) -> None:
    _run(repo)
    path = _write_overrides(repo, [_OV])
    ovs = load_overrides(path)
    assert _actions(_run(repo, overrides=ovs)) == {
        "LUAT36-2024": "processed",
        "ND238-2026": "skipped",
    }
    assert set(_actions(_run(repo, overrides=ovs)).values()) == {"skipped"}
    rep = latest_reports(repo / "data/processed/structure_report.jsonl")
    assert rep["LUAT36-2024"]["report"]["overrides_applied"] == ["LUAT36-2024/D1/K2"]


def test_load_overrides_validation(tmp_path: Path) -> None:
    assert load_overrides(tmp_path / "khong-co.yaml") == {}
    with pytest.raises(ValueError):
        load_overrides(_write_overrides(tmp_path, [_OV, _OV]))  # trùng unit_id
    with pytest.raises(ValueError):
        load_overrides(_write_overrides(tmp_path, [{**_OV, "unit_id": "LUAT36-2024/D1"}]))
    with pytest.raises(ValueError):
        load_overrides(_write_overrides(tmp_path, [{**_OV, "ly_do": "thiếu trường"}]))


def test_script_fails_on_unapplied_override(repo: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _write_overrides(repo, [{**_OV, "text_starts_with": "Không khớp"}])
    good = {"LUAT36-2024": {"count": 1, "last": "1"}, "ND238-2026": {"count": 3, "last": "3"}}
    argv = ["--stage", "structure", "--repo-root", str(repo), "--config", str(_cfg(repo, good))]
    assert ingest_script.main(argv) == 1
    assert "sửa nhãn không áp dụng được: LUAT36-2024/D1/K2" in capsys.readouterr().out
