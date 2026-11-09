"""M5: pipeline dựng đồ thị — resume theo hash đầu vào, ``--force`` tất định, mã thoát."""

from __future__ import annotations

import shutil
from pathlib import Path

from scripts.build_graph import main as build_graph_main
from tests.graph.test_build import _inputs
from trafficlaw.graph.pipeline import GraphPaths, file_sha256, run_build_graph
from trafficlaw.utils.jsonl import read_jsonl, write_jsonl

REPO_ROOT = Path(__file__).resolve().parents[2]


def _setup(tmp: Path) -> GraphPaths:
    units, added, versions = _inputs()
    proc, reg, graph = tmp / "data/processed", tmp / "data/registry", tmp / "data/graph"
    reg.mkdir(parents=True)
    shutil.copy(REPO_ROOT / "data/registry/documents.yaml", reg / "documents.yaml")
    shutil.copy(REPO_ROOT / "data/registry/doc_aliases.yaml", reg / "doc_aliases.yaml")
    write_jsonl(proc / "units.jsonl", units)
    write_jsonl(proc / "units_added.jsonl", added)
    write_jsonl(proc / "unit_versions.jsonl", versions)
    return GraphPaths(
        units=proc / "units.jsonl",
        unit_versions=proc / "unit_versions.jsonl",
        units_added=proc / "units_added.jsonl",
        documents=reg / "documents.yaml",
        doc_aliases=reg / "doc_aliases.yaml",
        nodes=graph / "nodes.jsonl",
        edges_struct=graph / "edges_struct.jsonl",
        edges_legal=graph / "edges_legal.jsonl",
        unresolved=graph / "unresolved.jsonl",
        report=graph / "graph_report.jsonl",
        summary=graph / "graph_summary.md",
        review=graph / "review_sample.md",
    )


def _hashes(p: GraphPaths) -> list[str]:
    return [file_sha256(x) for x in [*p.outputs(), p.unresolved, p.review]]


def test_resume_va_force_tat_dinh(tmp_path: Path) -> None:
    p = _setup(tmp_path)
    first = run_build_graph(p)
    assert first.action == "processed" and first.record["status"] == "ok"
    h1 = _hashes(p)
    assert run_build_graph(p).action == "skipped"
    assert run_build_graph(p, force=True).action == "processed"
    assert _hashes(p) == h1
    assert len(list(read_jsonl(p.report))) == 2  # bản ghi bỏ qua không ghi thêm
    assert "Kiểm tra cụ thể" in p.review.read_text(encoding="utf-8")
    assert "Cạnh theo loại" in p.summary.read_text(encoding="utf-8")


def test_doi_dau_vao_hoac_sua_dau_ra_thi_chay_lai(tmp_path: Path) -> None:
    p = _setup(tmp_path)
    run_build_graph(p)
    p.edges_legal.write_text("", encoding="utf-8")  # đầu ra bị sửa tay
    assert run_build_graph(p).action == "processed"
    with p.doc_aliases.open("a", encoding="utf-8") as f:
        f.write("  - Luật Thủy lợi\n")
    assert run_build_graph(p).action == "processed"


def test_loi_du_lieu_bao_trong_record(tmp_path: Path) -> None:
    p = _setup(tmp_path)
    rows = list(read_jsonl(p.unit_versions))
    rows.append({**rows[0], "unit_id": "ND168-2024/D99", "version": 0})
    write_jsonl(p.unit_versions, rows)
    rec = run_build_graph(p).record
    assert rec["status"] == "error"
    assert any("ND168-2024/D99" in x for x in rec["problems"])


def test_script_extract_can_danh_muc(tmp_path: Path) -> None:
    """M8: --extract chưa có danh mục PT/CT → mã 1 (không gọi LLM)."""
    import shutil

    shutil.copytree(Path(__file__).resolve().parents[2] / "configs", tmp_path / "configs")
    assert build_graph_main(["--extract", "--repo-root", str(tmp_path)]) == 1
