from pathlib import Path

import docx
import pytest
import yaml

from scripts import ingest as ingest_script
from trafficlaw.ingest.manifest import IngestConfig, latest_records
from trafficlaw.ingest.pipeline import run_normalize
from trafficlaw.registry.loader import load_registry
from trafficlaw.utils.jsonl import read_jsonl

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


def _docx(path: Path, text: str) -> None:
    d = docx.Document()
    for line in text.strip().split("\n"):
        d.add_paragraph(line)
    path.parent.mkdir(parents=True, exist_ok=True)
    d.save(str(path))


def _doc_entry(doc_id: str, so_hieu: str, source: str) -> dict:
    return {
        "doc_id": doc_id,
        "so_hieu": so_hieu,
        "loai": "luat" if doc_id.startswith("LUAT") else "nghi_dinh",
        "co_quan": "Quốc hội" if doc_id.startswith("LUAT") else "Chính phủ",
        "tier": "A",
        "source_path": source,
    }


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """Repo giả: 2 văn bản .docx từ fixture thật + danh mục + config."""
    l36 = "QUỐC HỘI\nLuật số: 36/2024/QH15\n" + (FIXTURES / "luat36_dieu9.txt").read_text(
        encoding="utf-8"
    ).replace("Điều 9.", "Điều 1.", 1)
    nd = "CHÍNH PHỦ\nSố: 168/2024/NĐ-CP\nĐiều 1. Phạm vi\n" + (
        FIXTURES / "nd168_dieu6_k1_k3.txt"
    ).read_text(encoding="utf-8")
    _docx(tmp_path / "data/raw/Luat/luật 36.docx", l36)
    _docx(tmp_path / "data/raw/NghiDinh/nghị định 168.docx", nd)
    reg = {
        "documents": [
            _doc_entry("LUAT36-2024", "36/2024/QH15", "data/raw/Luat/luật 36.docx"),
            _doc_entry("ND168-2024", "168/2024/NĐ-CP", "data/raw/NghiDinh/nghị định 168.docx"),
        ]
    }
    (tmp_path / "data/registry").mkdir(parents=True)
    (tmp_path / "data/registry/documents.yaml").write_text(
        yaml.safe_dump(reg, allow_unicode=True), encoding="utf-8"
    )
    return tmp_path


def _run(repo: Path, **kw) -> list:
    return run_normalize(
        load_registry(repo / "data/registry/documents.yaml"),
        repo_root=repo,
        interim_dir=repo / "data/interim",
        manifest_path=repo / "data/interim/manifest.jsonl",
        cfg=IngestConfig(),
        git_commit="abc123",
        **kw,
    )


def _actions(outcomes: list) -> dict[str, str]:
    return {o.doc_id: o.action for o in outcomes}


def test_first_run_writes_interim_and_manifest(repo: Path) -> None:
    out = _run(repo)
    assert _actions(out) == {"LUAT36-2024": "processed", "ND168-2024": "processed"}
    text = (repo / "data/interim/LUAT36-2024.txt").read_bytes()
    assert b"\r" not in text and text.endswith(b"\n")
    assert "Điều 1. Các hành vi bị nghiêm cấm" in text.decode("utf-8")
    recs = list(read_jsonl(repo / "data/interim/manifest.jsonl"))
    assert len(recs) == 2
    r = recs[0]
    assert r["status"] == "ok" and r["reader"] == "docx"
    assert r["so_hieu_found"] and r["has_dieu_1"]
    assert r["output_path"] == "data/interim/LUAT36-2024.txt"
    assert r["git_commit"] == "abc123" and len(r["source_sha256"]) == 64
    assert recs[1]["n_dieu_headings"] == 2


def test_second_run_skips_everything(repo: Path) -> None:
    _run(repo)
    out = _run(repo)
    assert set(_actions(out).values()) == {"skipped"}
    assert len(list(read_jsonl(repo / "data/interim/manifest.jsonl"))) == 2


def test_changed_source_only_reruns_that_document(repo: Path) -> None:
    _run(repo)
    _docx(repo / "data/raw/NghiDinh/nghị định 168.docx", "Số: 168/2024/NĐ-CP\nĐiều 1. Mới")
    out = _run(repo)
    assert _actions(out) == {"LUAT36-2024": "skipped", "ND168-2024": "processed"}
    latest = latest_records(repo / "data/interim/manifest.jsonl")
    assert latest["ND168-2024"]["n_dieu_headings"] == 1
    assert (repo / "data/interim/ND168-2024.txt").read_text(encoding="utf-8").endswith("Mới\n")


def test_force_and_missing_interim_file(repo: Path) -> None:
    _run(repo)
    assert set(_actions(_run(repo, force=True)).values()) == {"processed"}
    (repo / "data/interim/LUAT36-2024.txt").unlink()
    assert _actions(_run(repo)) == {"LUAT36-2024": "processed", "ND168-2024": "skipped"}


def test_doc_id_filter(repo: Path) -> None:
    assert _actions(_run(repo, doc_ids=["ND168-2024"])) == {"ND168-2024": "processed"}
    with pytest.raises(KeyError):
        _run(repo, doc_ids=["KHONG-CO"])


def test_truncated_manifest_line_is_recovered(repo: Path) -> None:
    _run(repo)
    manifest = repo / "data/interim/manifest.jsonl"
    lines = manifest.read_text(encoding="utf-8").split("\n")
    manifest.write_text(lines[0] + "\n" + lines[1][:40], encoding="utf-8")  # crash khi đang ghi
    out = _run(repo)
    assert _actions(out) == {"LUAT36-2024": "skipped", "ND168-2024": "processed"}
    assert [r["doc_id"] for r in read_jsonl(manifest)] == ["LUAT36-2024", "ND168-2024"]


def test_error_is_recorded_and_retried(repo: Path) -> None:
    src = repo / "data/raw/Luat/luật 36.docx"
    good = src.read_bytes()
    src.write_bytes(b"not a docx")
    out = _run(repo, doc_ids=["LUAT36-2024"])
    assert out[0].record is not None and out[0].record.status == "error"
    src.write_bytes(good)
    assert _actions(_run(repo, doc_ids=["LUAT36-2024"])) == {"LUAT36-2024": "processed"}


def test_missing_so_hieu_policy(repo: Path) -> None:
    _docx(repo / "data/raw/NghiDinh/nghị định 168.docx", "Số: /2024/NĐ-CP\nĐiều 1. Phạm vi")
    cfg = IngestConfig(so_hieu_unsigned=frozenset({"ND168-2024"}))
    out = run_normalize(
        load_registry(repo / "data/registry/documents.yaml"),
        repo_root=repo,
        interim_dir=repo / "data/interim",
        manifest_path=repo / "data/interim/manifest.jsonl",
        cfg=cfg,
        git_commit=None,
    )
    rec = {o.doc_id: o.record for o in out}["ND168-2024"]
    assert rec is not None and rec.status == "ok"
    assert not rec.so_hieu_found and not rec.so_hieu_required
    assert any("chưa ghi số" in w for w in rec.warnings)


def test_script_exit_codes(repo: Path) -> None:
    cfg = repo / "configs/ingest.yaml"
    cfg.parent.mkdir()
    cfg.write_text("so_hieu_unsigned: []\n", encoding="utf-8")
    argv = ["--repo-root", str(repo), "--config", str(cfg)]
    assert ingest_script.main(argv) == 0
    assert ingest_script.main(argv) == 0  # lần 2: bỏ qua hết
    summary = (repo / "data/interim/ingest_summary.md").read_text(encoding="utf-8")
    assert "| LUAT36-2024 | ok | docx |" in summary
    # Văn bản bắt buộc có số hiệu mà không thấy → mã 1.
    _docx(repo / "data/raw/Luat/luật 36.docx", "Điều 1. Không có số hiệu")
    assert ingest_script.main(argv) == 1
