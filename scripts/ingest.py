"""M2: đọc + chuẩn hoá văn bản gốc → ``data/interim/<doc_id>.txt`` + manifest.

    uv run python -m scripts.ingest [--stage normalize] [--doc-id ID ...] [--force]
                                    [--registry PATH] [--config PATH]

Resume được: văn bản đã ``ok`` với cùng sha256 file gốc thì bỏ qua (``--force`` để chạy lại).
Mã thoát 0 nếu mọi văn bản ``ok`` và có số hiệu trong text (trừ ``so_hieu_unsigned``), 1 nếu
không. Bảng tổng hợp (UTF-8) ghi vào ``summary`` trong ``configs/ingest.yaml``.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

from trafficlaw.ingest.manifest import IngestConfig, latest_records
from trafficlaw.ingest.pipeline import run_normalize
from trafficlaw.registry.loader import load_registry
from trafficlaw.utils.git import git_commit
from trafficlaw.utils.logging import setup_logging
from trafficlaw.utils.seed import set_seed

REPO_ROOT = Path(__file__).resolve().parents[1]
STAGES = ("normalize",)  # M3 thêm "structure"


def _load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def summary_table(records: list[dict[str, Any]]) -> str:
    """Bảng Markdown: một dòng mỗi văn bản (bản ghi mới nhất trong manifest)."""
    head = (
        '| doc_id | status | reader | ký tự | trang | "Điều" | token 1 ký tự | U+FFFD '
        "| số hiệu | cảnh báo |\n|---|---|---|---:|---:|---:|---:|---:|---|---|"
    )
    rows = [head]
    for r in records:
        sh = (
            "có" if r.get("so_hieu_found") else ("thiếu*" if r.get("so_hieu_required") else "thiếu")
        )
        warns = "; ".join(r.get("warnings") or []) or (r.get("error") or "")
        rows.append(
            f"| {r['doc_id']} | {r['status']} | {r.get('reader') or ''} | {r.get('n_chars', 0)} "
            f"| {r.get('n_pages') or ''} | {r.get('n_dieu_headings', 0)} "
            f"| {r.get('single_char_ratio', 0):.4f} | {r.get('n_replacement_chars', 0)} "
            f"| {sh} | {warns.replace('|', '/')} |"
        )
    return "\n".join(rows) + "\n\n`thiếu*`: văn bản phải có số hiệu nhưng không thấy trong text.\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--stage", choices=STAGES, default="normalize")
    ap.add_argument("--doc-id", action="append", default=None, help="chỉ chạy văn bản này")
    ap.add_argument("--force", action="store_true", help="chạy lại cả văn bản đã xong")
    ap.add_argument("--registry", type=Path, default=None)
    ap.add_argument("--config", type=Path, default=REPO_ROOT / "configs" / "ingest.yaml")
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT, help=argparse.SUPPRESS)
    args = ap.parse_args(argv)
    set_seed()
    setup_logging("WARNING")
    # Console Windows (cp1252) không in được tiếng Việt: thay ký tự lỗi thay vì crash.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")

    root: Path = args.repo_root
    paths = _load_yaml(REPO_ROOT / "configs" / "paths.yaml")
    cfg = IngestConfig.model_validate(_load_yaml(args.config))
    registry = load_registry(args.registry or root / paths["documents"])
    manifest = root / cfg.manifest
    interim_dir = root / paths["interim_dir"]

    outcomes = run_normalize(
        registry,
        repo_root=root,
        interim_dir=interim_dir,
        manifest_path=manifest,
        cfg=cfg,
        git_commit=git_commit(root),
        doc_ids=args.doc_id,
        force=args.force,
    )
    n_proc = sum(o.action == "processed" for o in outcomes)
    n_skip = len(outcomes) - n_proc

    latest = latest_records(manifest)
    selected = [latest[o.doc_id] for o in outcomes if o.doc_id in latest]
    summary = root / cfg.summary
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(summary_table(selected), encoding="utf-8", newline="\n")

    bad_status = [r["doc_id"] for r in selected if r["status"] != "ok"]
    missing_sh = [
        r["doc_id"]
        for r in selected
        if r["status"] == "ok" and r["so_hieu_required"] and not r["so_hieu_found"]
    ]
    n_ok = sum(r["status"] == "ok" for r in selected)
    print(
        f"Stage {args.stage}: {len(outcomes)} văn bản — {n_proc} xử lý, {n_skip} bỏ qua (đã xong)"
    )
    for r in selected:
        flag = "" if r["status"] == "ok" else f"  <-- {r.get('error')}"
        print(
            f"  {r['doc_id']:<22} {r['status']:<7} {r.get('reader') or '-':<9}"
            f" {r.get('n_chars', 0):>7} ký tự  {r.get('n_dieu_headings', 0):>3} Điều"
            f"  {len(r.get('warnings') or [])} cảnh báo{flag}"
        )
    print(f"ok: {n_ok}/{len(selected)}  ·  bảng tổng hợp: {summary}")
    if missing_sh:
        print(f"Thiếu số hiệu trong text: {', '.join(missing_sh)}", file=sys.stderr)
    return 1 if bad_status or missing_sh else 0


if __name__ == "__main__":
    sys.exit(main())
