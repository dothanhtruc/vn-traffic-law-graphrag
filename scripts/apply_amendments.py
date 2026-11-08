"""M4: áp sửa đổi → ``data/processed/unit_versions.jsonl`` + ``units_added.jsonl``.

    uv run python -m scripts.apply_amendments [--doc-id ID ...] [--force] [--repo-root PATH]

Resume theo ``(doc_id đích, input_sha256)`` (unit của đích + văn bản sửa nó + VBHN của nó +
danh mục, ``vbhn_map``, ``amendment_overrides`` liên quan). **Sửa code M4 thì chạy với
``--force``**. Câu sửa đổi không chắc chắn → ``amendment_todo.csv`` (không đoán).

Mã thoát 1 nếu có đích lỗi hoặc mục ``amendment_overrides.yaml`` không áp được; todo không
làm script thất bại. Bảng tổng hợp: ``amendment_summary``.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

from trafficlaw.ingest.amendment_pipeline import (
    latest_reports,
    load_effect_overrides,
    load_label_fixes,
    run_amendments,
    summary_markdown,
)
from trafficlaw.ingest.vbhn import load_vbhn_map
from trafficlaw.registry.loader import load_registry
from trafficlaw.utils.git import git_commit
from trafficlaw.utils.logging import setup_logging
from trafficlaw.utils.seed import set_seed

REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--doc-id", action="append", default=None, help="chỉ chạy văn bản đích này")
    ap.add_argument("--force", action="store_true", help="chạy lại cả đích đã xong")
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT, help=argparse.SUPPRESS)
    args = ap.parse_args(argv)
    set_seed()
    setup_logging("WARNING")
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")

    root: Path = args.repo_root
    paths = _load_yaml(REPO_ROOT / "configs" / "paths.yaml")
    report_path = root / paths["amendment_report"]
    outcomes = run_amendments(
        units_path=root / paths["units"],
        versions_path=root / paths["unit_versions"],
        added_path=root / paths["units_added"],
        report_path=report_path,
        todo_path=root / paths["amendment_todo"],
        registry=load_registry(root / paths["documents"]),
        vbhn_map=load_vbhn_map(root / paths["vbhn_map"]),
        label_fixes=load_label_fixes(root / paths["amendment_overrides"]),
        effect_overrides=load_effect_overrides(root / paths["amendment_overrides"]),
        git_commit=git_commit(root),
        doc_ids=args.doc_id,
        force=args.force,
    )
    latest = latest_reports(report_path)
    selected = {o.doc_id: latest[o.doc_id] for o in outcomes if o.doc_id in latest}
    summary = root / paths["amendment_summary"]
    summary.parent.mkdir(parents=True, exist_ok=True)
    summary.write_text(summary_markdown(selected), encoding="utf-8", newline="\n")

    n_proc = sum(o.action == "processed" for o in outcomes)
    print(
        f"apply_amendments: {len(outcomes)} văn bản đích — {n_proc} xử lý, "
        f"{len(outcomes) - n_proc} bỏ qua (đã xong)"
    )
    bad: list[str] = []
    for d, r in selected.items():
        n_ins = sum(n for ops in (r.get("instructions") or {}).values() for n, _ in ops.values())
        n_ok = sum(k for ops in (r.get("instructions") or {}).values() for _, k in ops.values())
        probs = []
        if r["status"] != "ok":
            probs.append(r.get("error") or "lỗi")
        if r.get("fixes_unapplied"):
            probs.append(f"sửa nhãn không áp được: {', '.join(r['fixes_unapplied'])}")
        if probs:
            bad.append(d)
        if n_ins or r.get("n_changed_units") or probs:
            print(
                f"  {d:<20} chỉ dẫn {n_ok:>3}/{n_ins:<3} unit đổi {r.get('n_changed_units', 0):>4}"
                f"  bổ sung {r.get('n_added', 0):>3}  todo {len(r.get('todos') or []):>3}"
                + (f"  <-- {'; '.join(probs)}" if probs else "")
            )
    print(f"bảng tổng hợp: {summary}  ·  todo: {root / paths['amendment_todo']}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
