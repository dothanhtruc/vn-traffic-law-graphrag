"""M16: báo cáo kết quả tự động từ file có sẵn (không GPU, không LLM, không mạng).

    uv run --group report python -m scripts.report [--run-id m14-test] [--out DIR]
                                                   [--config configs/report.yaml] [--no-figures]
                                                   [--strict]

Ghi ``<out>/report.md``, ``<out>/figures/*.png`` (cần nhóm uv ``report`` = matplotlib; thiếu thì
bỏ hình và ghi chú), ``<out>/sources.json`` (sha256 + trường đã đọc của từng file nguồn).

Mã thoát: 0; 1 nếu ``--strict`` và có nguồn thiếu hoặc kiểm tra nhất quán lệch.
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from trafficlaw.report.build import build_report, load_config
from trafficlaw.utils.git import git_commit
from trafficlaw.utils.seed import set_seed

REPO_ROOT = Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--run-id", default=None, help="mặc định: run_id trong configs/report.yaml")
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--config", type=Path, default=REPO_ROOT / "configs" / "report.yaml")
    ap.add_argument("--no-figures", action="store_true")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    set_seed(42)

    cfg = load_config(args.config)
    res = build_report(
        REPO_ROOT,
        cfg,
        run_id=args.run_id,
        out_dir=args.out,
        git_commit=git_commit(REPO_ROOT),
        draw=not args.no_figures,
    )
    print(f"Báo cáo: {res.report_path}")
    print(f"Hình: {len(res.figures)} vẽ, {len(res.skipped_figures)} bỏ qua")
    for sid, p in sorted(res.missing.items()):
        print(f"THIẾU nguồn {sid}: {p}")
    if res.lech:
        print(f"Kiểm tra nhất quán: {res.lech} dòng lệch (xem chương Tổng quan)")
    for e in res.errors:
        print(f"LỖI chương {e}")
    if args.strict and (res.missing or res.lech or res.errors):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
