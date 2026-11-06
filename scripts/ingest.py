"""M2–M3: văn bản gốc → ``data/interim/<doc_id>.txt`` → ``data/processed/units.jsonl``.

    uv run python -m scripts.ingest [--stage normalize|structure] [--doc-id ID ...] [--force]
                                    [--registry PATH] [--config PATH]

``normalize`` (M2): resume theo sha256 file gốc. Mã thoát 0 nếu mọi văn bản ``ok`` và có số
hiệu trong text (trừ ``so_hieu_unsigned``). Bảng tổng hợp: ``summary`` trong config.

``structure`` (M3): resume theo sha256 file interim. Mã thoát 0 nếu mọi văn bản ``ok``, số
Điều + Điều cuối khớp ``expected_dieu`` và không có trích dẫn chưa đóng. Bảng tổng hợp:
``structure_summary``.

``--force`` chạy lại cả văn bản đã xong (cần khi sửa reader/normalize/parser).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

from trafficlaw.ingest.manifest import IngestConfig, latest_records
from trafficlaw.ingest.pipeline import run_normalize
from trafficlaw.ingest.structure_pipeline import latest_reports, run_structure
from trafficlaw.registry.loader import load_registry
from trafficlaw.utils.git import git_commit
from trafficlaw.utils.logging import setup_logging
from trafficlaw.utils.seed import set_seed

REPO_ROOT = Path(__file__).resolve().parents[1]
STAGES = ("normalize", "structure")


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


_LEVEL_COLS = ("phan", "chuong", "muc", "dieu", "khoan", "diem", "phu_luc")


def structure_problems(rec: dict[str, Any], cfg: IngestConfig) -> list[str]:
    """Lý do làm script thoát mã 1 cho một văn bản (rỗng = đạt)."""
    if rec["status"] != "ok":
        return [rec.get("error") or "lỗi"]
    r = rec["report"]
    out: list[str] = []
    exp = cfg.expected_dieu.get(rec["doc_id"])
    if exp is not None and (r["n_dieu"] != exp.count or r["last_dieu"] != exp.last):
        out.append(
            f"số Điều {r['n_dieu']} (cuối {r['last_dieu']}) ≠ kỳ vọng {exp.count} (cuối {exp.last})"
        )
    if any(a["kind"] == "unclosed_quote" for a in r["anomalies"]):
        out.append("trích dẫn chưa đóng")
    return out


def structure_table(records: list[dict[str, Any]], cfg: IngestConfig) -> str:
    head = (
        "| doc_id | status | Phần | Chương | Mục | Điều | Khoản | Điểm | Phụ lục | Điều cuối "
        "| kỳ vọng | điểm dừng | dòng bỏ | dòng trích dẫn | chú thích | bất thường |\n"
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|---:|---:|---:|---|"
    )
    rows = [head]
    for rec in records:
        r = rec.get("report") or {}
        c = r.get("counts", {})
        exp = cfg.expected_dieu.get(rec["doc_id"])
        kinds: dict[str, int] = {}
        for a in r.get("anomalies", []):
            kinds[a["kind"]] = kinds.get(a["kind"], 0) + 1
        anom = ", ".join(f"{k} {v}" for k, v in sorted(kinds.items())) or ""
        end = f"{r.get('body_end_reason') or 'hết file'}@{r.get('body_end_line') or ''}"
        cells = [rec["doc_id"], rec["status"], *(str(c.get(k, 0)) for k in _LEVEL_COLS)]
        cells += [
            str(r.get("last_dieu") or ""),
            f"{exp.count}/{exp.last}" if exp else "—",
            end,
            str(r.get("n_dropped_lines", 0)),
            str(r.get("n_quoted_lines", 0)),
            str(r.get("n_footnotes", 0)),
            anom or (rec.get("error") or ""),
        ]
        rows.append("| " + " | ".join(x.replace("|", "/") for x in cells) + " |")
    note = (
        "\n`dòng bỏ`: dòng giữa điểm dừng phần thân và Phụ lục đầu tiên (chữ ký, Nơi nhận, "
        "biểu mẫu không có tiêu đề Phụ lục) — không thuộc unit nào.\n"
    )
    return "\n".join(rows) + "\n" + note


def _main_structure(
    args: argparse.Namespace, root: Path, paths: dict[str, Any], cfg: IngestConfig
) -> int:
    report_path = root / cfg.structure_report
    outcomes = run_structure(
        repo_root=root,
        manifest_path=root / cfg.manifest,
        units_path=root / paths["units"],
        report_path=report_path,
        git_commit=git_commit(root),
        doc_ids=args.doc_id,
        force=args.force,
    )
    n_proc = sum(o.action == "processed" for o in outcomes)
    latest = latest_reports(report_path)
    selected = [latest[o.doc_id] for o in outcomes if o.doc_id in latest]
    summary = root / cfg.structure_summary
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(structure_table(selected, cfg), encoding="utf-8", newline="\n")

    print(
        f"Stage structure: {len(outcomes)} văn bản — {n_proc} xử lý, "
        f"{len(outcomes) - n_proc} bỏ qua (đã xong)"
    )
    bad: list[str] = []
    for rec in selected:
        c = (rec.get("report") or {}).get("counts", {})
        probs = structure_problems(rec, cfg)
        if probs:
            bad.append(rec["doc_id"])
        n_anom = len((rec.get("report") or {}).get("anomalies", []))
        print(
            f"  {rec['doc_id']:<22} {rec['status']:<5} Điều {c.get('dieu', 0):>3}"
            f"  Khoản {c.get('khoan', 0):>4}  Điểm {c.get('diem', 0):>4}"
            f"  PL {c.get('phu_luc', 0):>2}  {n_anom:>2} bất thường"
            + (f"  <-- {'; '.join(probs)}" if probs else "")
        )
    missing_exp = [r["doc_id"] for r in selected if r["doc_id"] not in cfg.expected_dieu]
    if missing_exp:
        print(f"Chưa có số Điều kỳ vọng: {', '.join(missing_exp)}", file=sys.stderr)
    print(f"đạt: {len(selected) - len(bad)}/{len(selected)}  ·  bảng tổng hợp: {summary}")
    return 1 if bad else 0


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
    if args.stage == "structure":
        return _main_structure(args, root, paths, cfg)
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
