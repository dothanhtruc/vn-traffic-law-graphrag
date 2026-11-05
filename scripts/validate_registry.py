"""M1: kiểm tra danh mục văn bản ``data/registry/documents.yaml``.

    uv run python -m scripts.validate_registry [--registry PATH] [--no-check-files]
                                               [--strict] [--json-out PATH]

Mã thoát: 0 nếu không có lỗi (``--strict``: không có cả cảnh báo), 1 nếu có, 2 nếu sai schema.
Script chỉ **báo** vấn đề, không sửa danh mục.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import asdict
from pathlib import Path

import yaml
from pydantic import ValidationError

from trafficlaw.registry.loader import load_registry
from trafficlaw.registry.schema import TIERS
from trafficlaw.registry.validator import LEVELS, count_by_level, validate_registry
from trafficlaw.utils.seed import set_seed

REPO_ROOT = Path(__file__).resolve().parents[1]


def _default_registry() -> Path:
    paths = yaml.safe_load((REPO_ROOT / "configs" / "paths.yaml").read_text(encoding="utf-8"))
    return REPO_ROOT / paths["documents"]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--registry", type=Path, default=None)
    ap.add_argument(
        "--no-check-files", action="store_true", help="bỏ qua kiểm tra file trong data/raw/"
    )
    ap.add_argument("--strict", action="store_true", help="coi cảnh báo là lỗi")
    ap.add_argument("--json-out", type=Path, default=None, help="ghi danh sách vấn đề ra JSON")
    args = ap.parse_args(argv)
    set_seed()

    path = args.registry or _default_registry()
    try:
        reg = load_registry(path)
    except (ValidationError, ValueError) as e:
        print(f"Sai schema trong {path}:\n{e}", file=sys.stderr)
        return 2

    issues = validate_registry(reg, repo_root=None if args.no_check_files else REPO_ROOT)
    counts = count_by_level(issues)

    tiers = Counter(d.tier for d in reg)
    print(f"Danh mục: {path}")
    print(f"Số văn bản: {len(reg)}  (" + ", ".join(f"{t}={tiers.get(t, 0)}" for t in TIERS) + ")")
    print(
        f"Văn bản sửa đổi: {sum(d.is_amendment for d in reg)}  ·  "
        f"Chỉ mục độc lập: {len(reg.indexable())}"
    )
    for level in LEVELS:
        group = [i for i in issues if i.level == level]
        if group:
            print(f"\n== {level.upper()} ({len(group)}) ==")
            for i in group:
                print(f"  {i.code:<24} {i.doc_id:<22} {i.message}")
    print(f"\nTổng: {counts['error']} lỗi, {counts['warning']} cảnh báo, {counts['info']} ghi chú.")

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(
            json.dumps([asdict(i) for i in issues], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    failed = counts["error"] > 0 or (args.strict and counts["warning"] > 0)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
