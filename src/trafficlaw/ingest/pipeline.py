"""Bước ``normalize``: file gốc → ``data/interim/<doc_id>.txt`` + một dòng manifest.

Thứ tự ghi: file interim (atomic: file tạm + ``os.replace``) **rồi** mới tới dòng manifest.
Dừng giữa chừng thì văn bản đang làm chưa có bản ghi ``ok`` → lần sau chạy lại nó.
"""

from __future__ import annotations

import logging
import os
import tempfile
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from trafficlaw.ingest.manifest import (
    IngestConfig,
    ManifestRecord,
    done_ok,
    sha256_file,
)
from trafficlaw.ingest.normalize import (
    count_dieu_headings,
    find_so_hieu,
    has_dieu_1,
    normalize_text,
    single_char_token_ratio,
)
from trafficlaw.ingest.readers import ReaderError, ScannedPdfError, read_source
from trafficlaw.registry.loader import Registry
from trafficlaw.registry.schema import DocumentMeta
from trafficlaw.utils.jsonl import JsonlWriter

logger = logging.getLogger(__name__)

Action = Literal["processed", "skipped"]


@dataclass(frozen=True)
class IngestOutcome:
    doc_id: str
    action: Action
    record: ManifestRecord | None  # None khi skipped


def write_text_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise


def _rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def ingest_document(
    doc: DocumentMeta,
    *,
    repo_root: Path,
    interim_dir: Path,
    cfg: IngestConfig,
    git_commit: str | None,
    source_sha256: str | None = None,
) -> ManifestRecord:
    """Đọc + chuẩn hoá một văn bản, ghi file interim; trả về bản ghi manifest (chưa ghi)."""
    assert doc.source_path is not None
    src = repo_root / doc.source_path
    out_path = interim_dir / f"{doc.doc_id}.txt"
    base = {
        "doc_id": doc.doc_id,
        "source_path": doc.source_path,
        "source_sha256": source_sha256,
        "output_path": None,
        "reader": None,
        "so_hieu_required": doc.doc_id not in cfg.so_hieu_unsigned,
        "ingested_at": datetime.now(UTC),
        "git_commit": git_commit,
    }
    try:
        if base["source_sha256"] is None:
            base["source_sha256"] = sha256_file(src)
        raw = read_source(src, min_chars_per_page=cfg.min_chars_per_page)
    except ScannedPdfError as e:
        return ManifestRecord(**base, status="scanned", error=str(e))
    except (ReaderError, OSError) as e:
        return ManifestRecord(**base, status="error", error=str(e))

    norm = normalize_text(raw.text, source="pdf" if raw.reader == "pymupdf" else "word")
    text = norm.text
    warnings = list(raw.warnings) + norm.warnings

    ratio = single_char_token_ratio(text)
    if ratio > cfg.single_char_ratio_max:
        warnings.append(f"tỷ lệ token 1 ký tự {ratio:.3f} > {cfg.single_char_ratio_max}")
    if not has_dieu_1(text):
        warnings.append('không thấy dòng "Điều 1."')
    so_hieu_found = find_so_hieu(text, doc.so_hieu)
    if not so_hieu_found:
        note = " (bản chưa ghi số/ngày ký)" if not base["so_hieu_required"] else ""
        warnings.append(f"không thấy số hiệu {doc.so_hieu!r} trong text{note}")

    write_text_atomic(out_path, text)
    return ManifestRecord(
        **{**base, "output_path": _rel(out_path, repo_root), "reader": raw.reader},
        n_pages=raw.n_pages,
        n_chars=len(text),
        n_dieu_headings=count_dieu_headings(text),
        has_dieu_1=has_dieu_1(text),
        n_replacement_chars=norm.n_replacement_chars,
        n_symbol_chars=norm.n_symbol_chars,
        single_char_ratio=round(ratio, 5),
        so_hieu_found=so_hieu_found,
        warnings=warnings,
        status="ok",
    )


def run_normalize(
    registry: Registry,
    *,
    repo_root: Path,
    interim_dir: Path,
    manifest_path: Path,
    cfg: IngestConfig,
    git_commit: str | None,
    doc_ids: Iterable[str] | None = None,
    force: bool = False,
) -> list[IngestOutcome]:
    """Chạy bước normalize cho mọi văn bản có ``source_path`` (kể cả VBHN, văn bản sửa đổi).

    Bỏ qua văn bản đã có bản ghi ``ok`` với cùng ``source_sha256`` và file interim còn tồn
    tại, trừ khi ``force``.
    """
    wanted = set(doc_ids) if doc_ids else None
    if wanted:
        unknown = wanted - {d.doc_id for d in registry}
        if unknown:
            raise KeyError(f"doc_id không có trong danh mục: {sorted(unknown)}")
    done = set() if force else done_ok(manifest_path)
    outcomes: list[IngestOutcome] = []
    with JsonlWriter(manifest_path) as writer:
        for doc in registry:
            if doc.source_path is None or (wanted and doc.doc_id not in wanted):
                continue
            src = repo_root / doc.source_path
            sha = sha256_file(src) if src.is_file() else None
            out_path = interim_dir / f"{doc.doc_id}.txt"
            if (doc.doc_id, sha) in done and out_path.is_file():
                logger.info("Bỏ qua %s (đã xong, file gốc không đổi)", doc.doc_id)
                outcomes.append(IngestOutcome(doc.doc_id, "skipped", None))
                continue
            rec = ingest_document(
                doc,
                repo_root=repo_root,
                interim_dir=interim_dir,
                cfg=cfg,
                git_commit=git_commit,
                source_sha256=sha,
            )
            writer.write(rec)
            logger.info("%s: %s (%d ký tự)", doc.doc_id, rec.status, rec.n_chars)
            outcomes.append(IngestOutcome(doc.doc_id, "processed", rec))
    return outcomes
