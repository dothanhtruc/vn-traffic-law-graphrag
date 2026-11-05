import json
from pathlib import Path

from scripts.validate_registry import main

GOOD = """
documents:
  - doc_id: ND168-2024
    so_hieu: 168/2024/NĐ-CP
    loai: nghi_dinh
    co_quan: Chính phủ
    ngay_ban_hanh: 2024-12-26
    hieu_luc_tu: 2025-01-01
    tier: A
    source_path: data/raw/NghiDinh/168.doc
"""


def _write(tmp_path: Path, text: str) -> Path:
    p = tmp_path / "documents.yaml"
    p.write_text(text, encoding="utf-8")
    return p


def test_real_registry_passes() -> None:
    assert main(["--no-check-files"]) == 0


def test_ok_and_json_report(tmp_path: Path) -> None:
    out = tmp_path / "report.json"
    p = _write(tmp_path, GOOD)
    assert main(["--registry", str(p), "--no-check-files", "--json-out", str(out)]) == 0
    assert json.loads(out.read_text(encoding="utf-8")) == []


def test_warning_fails_only_in_strict(tmp_path: Path) -> None:
    p = _write(tmp_path, GOOD.replace("hieu_luc_tu: 2025-01-01", "hieu_luc_tu: null"))
    assert main(["--registry", str(p), "--no-check-files"]) == 0
    assert main(["--registry", str(p), "--no-check-files", "--strict"]) == 1


def test_error_exit_code(tmp_path: Path) -> None:
    p = _write(tmp_path, GOOD.replace("hieu_luc_tu: 2025-01-01", "hieu_luc_tu: 2024-01-01"))
    assert main(["--registry", str(p), "--no-check-files"]) == 1


def test_schema_error_exit_code(tmp_path: Path) -> None:
    p = _write(tmp_path, GOOD.replace("tier: A", "tier: Z"))
    assert main(["--registry", str(p), "--no-check-files"]) == 2
