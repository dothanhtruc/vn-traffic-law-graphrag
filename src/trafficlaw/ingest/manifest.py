"""Manifest của bước ingest: ``data/interim/manifest.jsonl`` (append-only, resume được).

Mỗi lần xử lý một văn bản ghi thêm một bản ghi; bản ghi mới nhất của mỗi ``doc_id`` là trạng
thái hiện tại. Khoá resume: ``(doc_id, source_sha256)`` của các bản ghi ``status == "ok"``.
"""

from __future__ import annotations

import hashlib
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

from trafficlaw.utils.jsonl import done_keys, read_jsonl

Status = Literal["ok", "error", "scanned"]
RESUME_KEY = ("doc_id", "source_sha256")


class ExpectedDieu(BaseModel):
    """Số Điều thân văn bản kỳ vọng (đếm tay) và số hiệu Điều cuối."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    count: int
    last: str


class IngestConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    manifest: str = "data/interim/manifest.jsonl"
    summary: str = "data/interim/ingest_summary.md"
    min_chars_per_page: int = 50
    single_char_ratio_max: float = 0.05
    so_hieu_unsigned: frozenset[str] = frozenset()
    # M3 (--stage structure); units.jsonl lấy từ configs/paths.yaml.
    structure_report: str = "data/processed/structure_report.jsonl"
    structure_summary: str = "data/processed/structure_summary.md"
    expected_dieu: dict[str, ExpectedDieu] = {}


class ManifestRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")

    doc_id: str
    source_path: str
    source_sha256: str | None
    output_path: str | None
    reader: str | None
    n_pages: int | None = None
    n_chars: int = 0
    n_dieu_headings: int = 0
    has_dieu_1: bool = False
    n_replacement_chars: int = 0
    n_symbol_chars: int = 0
    single_char_ratio: float = 0.0
    so_hieu_found: bool = False
    #: Không thấy số hiệu ở văn bản *không* thuộc ``so_hieu_unsigned`` → script thoát mã 1.
    so_hieu_required: bool = True
    warnings: list[str] = []
    status: Status
    error: str | None = None
    ingested_at: datetime
    git_commit: str | None


def sha256_file(path: str | Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        while block := f.read(chunk):
            h.update(block)
    return h.hexdigest()


def done_ok(manifest: str | Path) -> set[tuple[Any, ...]]:
    return done_keys(manifest, RESUME_KEY, where=lambda r: r.get("status") == "ok")


def latest_records(manifest: str | Path) -> dict[str, dict[str, Any]]:
    """Bản ghi mới nhất của mỗi ``doc_id`` (theo thứ tự trong file)."""
    out: dict[str, dict[str, Any]] = {}
    for rec in read_jsonl(manifest):
        out[rec["doc_id"]] = rec
    return out
