"""Bước ``structure`` (M3): ``data/interim/<doc_id>.txt`` → ``data/processed/units.jsonl``.

- Chỉ xử lý văn bản có bản ghi manifest mới nhất ``status == "ok"`` (kể cả VBHN, văn bản sửa
  đổi — M4 cần). Không đọc lại ``data/raw``.
- Resume: khoá ``(doc_id, interim_sha256)`` của bản ghi ``ok`` trong ``structure_report.jsonl``.
  Khoá không chứa phiên bản parser ⇒ **sửa parser thì chạy lại với ``--force``**.
- Thứ tự ghi: toàn bộ unit của một văn bản rồi mới tới dòng report. Trước khi xử lý (lại) một
  văn bản, các unit cũ của nó bị xoá khỏi ``units.jsonl`` (ghi lại atomic) ⇒ crash giữa chừng
  hay ``--force`` đều không để lại unit trùng.
"""

from __future__ import annotations

import logging
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

from trafficlaw.ingest.manifest import latest_records, sha256_file
from trafficlaw.ingest.structure import StructureReport, parse_structure
from trafficlaw.utils.jsonl import JsonlWriter, done_keys, read_jsonl, write_jsonl

logger = logging.getLogger(__name__)

RESUME_KEY = ("doc_id", "interim_sha256")


class StructureRecord(BaseModel):
    """Một dòng ``structure_report.jsonl`` (append-only; bản ghi mới nhất của doc là hiện hành)."""

    model_config = ConfigDict(extra="forbid")

    doc_id: str
    interim_path: str
    interim_sha256: str | None
    status: Literal["ok", "error"]
    error: str | None = None
    n_units: int = 0
    report: StructureReport | None = None
    parsed_at: datetime
    git_commit: str | None


@dataclass(frozen=True)
class StructureOutcome:
    doc_id: str
    action: Literal["processed", "skipped"]
    record: StructureRecord | None


def latest_reports(path: str | Path) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for rec in read_jsonl(path):
        out[rec["doc_id"]] = rec
    return out


def _purge_units(units_path: Path, doc_ids: set[str]) -> int:
    """Xoá unit của ``doc_ids`` khỏi ``units.jsonl`` (ghi lại atomic). Trả về số dòng bị xoá."""
    if not doc_ids or not units_path.exists():
        return 0
    rows = list(read_jsonl(units_path))
    keep = [r for r in rows if r.get("doc_id") not in doc_ids]
    if len(keep) != len(rows):
        write_jsonl(units_path, keep)
    return len(rows) - len(keep)


def run_structure(
    *,
    repo_root: Path,
    manifest_path: Path,
    units_path: Path,
    report_path: Path,
    git_commit: str | None,
    doc_ids: Iterable[str] | None = None,
    force: bool = False,
) -> list[StructureOutcome]:
    manifest = latest_records(manifest_path)
    wanted = set(doc_ids) if doc_ids else None
    if wanted:
        unknown = wanted - set(manifest)
        if unknown:
            raise KeyError(f"doc_id không có trong manifest: {sorted(unknown)}")
    docs = [
        r
        for r in manifest.values()
        if r.get("status") == "ok"
        and r.get("output_path")
        and (not wanted or r["doc_id"] in wanted)
    ]
    done = (
        set() if force else done_keys(report_path, RESUME_KEY, where=lambda r: r["status"] == "ok")
    )

    plan: list[tuple[dict[str, Any], Path, str | None, bool]] = []
    for r in docs:
        path = repo_root / r["output_path"]
        sha = sha256_file(path) if path.is_file() else None
        plan.append((r, path, sha, (r["doc_id"], sha) in done and sha is not None))
    n_purged = _purge_units(units_path, {r["doc_id"] for r, _, _, skip in plan if not skip})
    if n_purged:
        logger.info("Xoá %d unit cũ của các văn bản sắp xử lý lại", n_purged)

    outcomes: list[StructureOutcome] = []
    with JsonlWriter(units_path) as uw, JsonlWriter(report_path) as rw:
        for r, path, sha, skip in plan:
            doc_id = r["doc_id"]
            if skip:
                outcomes.append(StructureOutcome(doc_id, "skipped", None))
                continue
            base: dict[str, Any] = {
                "doc_id": doc_id,
                "interim_path": r["output_path"],
                "interim_sha256": sha,
                "parsed_at": datetime.now(UTC),
                "git_commit": git_commit,
            }
            try:
                text = path.read_text(encoding="utf-8")
                result = parse_structure(doc_id, text, r.get("source_path"))
            except Exception as e:  # lỗi của một văn bản không dừng cả job
                logger.exception("Lỗi khi tách cấu trúc %s", doc_id)
                rec = StructureRecord(**base, status="error", error=f"{type(e).__name__}: {e}")
            else:
                for u in result.units:
                    uw.write(u)
                rec = StructureRecord(
                    **base, status="ok", n_units=len(result.units), report=result.report
                )
            rw.write(rec)
            outcomes.append(StructureOutcome(doc_id, "processed", rec))
    return outcomes
