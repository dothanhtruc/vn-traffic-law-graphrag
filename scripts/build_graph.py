"""M5: dựng đồ thị (JSONL) từ units + unit_versions + units_added → ``data/graph/``.

    uv run python -m scripts.build_graph [--force] [--review-n 50] [--repo-root PATH]

Quan hệ cấu trúc (THUOC, KE_TIEP, CO_PHIEN_BAN) và pháp lý (SUA_DOI, BAI_BO, THAY_THE, HOP_NHAT,
HUONG_DAN, DAN_CHIEU) trích bằng rule/regex, không dùng LLM. Resume theo hash đầu vào
(``graph_report.jsonl``); **sửa code M5 thì chạy với ``--force``**.

Mã thoát 1 nếu có cạnh trỏ tới nút không tồn tại, phiên bản không có unit, hoặc vượt giới hạn
AuraDB Free (200k nút / 400k cạnh). ``--load-neo4j`` (M6) và ``--extract`` (M8) chưa có.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

from trafficlaw.graph.pipeline import GraphPaths, run_build_graph
from trafficlaw.utils.git import git_commit
from trafficlaw.utils.logging import setup_logging
from trafficlaw.utils.seed import DEFAULT_SEED, set_seed

REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def graph_paths(root: Path, paths: dict[str, Any]) -> GraphPaths:
    return GraphPaths(
        units=root / paths["units"],
        unit_versions=root / paths["unit_versions"],
        units_added=root / paths["units_added"],
        documents=root / paths["documents"],
        doc_aliases=root / paths["doc_aliases"],
        nodes=root / paths["graph_nodes"],
        edges_struct=root / paths["graph_edges_struct"],
        edges_legal=root / paths["graph_edges_legal"],
        unresolved=root / paths["graph_unresolved"],
        report=root / paths["graph_report"],
        summary=root / paths["graph_summary"],
        review=root / paths["graph_review"],
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--force", action="store_true", help="dựng lại dù đầu vào không đổi")
    ap.add_argument("--review-n", type=int, default=50, help="số cạnh DAN_CHIEU để rà tay")
    ap.add_argument("--load-neo4j", action="store_true", help="(M6) nạp vào Neo4j")
    ap.add_argument("--extract", action="store_true", help="(M8) trích xuất thực thể bằng LLM")
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT, help=argparse.SUPPRESS)
    args = ap.parse_args(argv)
    set_seed()
    setup_logging("WARNING")
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")
    if args.load_neo4j or args.extract:
        print("build_graph: --load-neo4j (M6) / --extract (M8) chưa được cài đặt", file=sys.stderr)
        return 2

    root: Path = args.repo_root
    gp = graph_paths(root, _load_yaml(REPO_ROOT / "configs" / "paths.yaml"))
    out = run_build_graph(
        gp, git_commit=git_commit(root), force=args.force, review_n=args.review_n, seed=DEFAULT_SEED
    )
    rec = out.record
    if out.action == "skipped":
        print(f"build_graph: bỏ qua — đầu vào không đổi (input_sha256 {rec['input_sha256'][:12]})")
    else:
        print(f"build_graph: {rec['n_nodes']:,} nút, {rec['n_edges']:,} cạnh — {rec['status']}")
        for k, v in rec["nodes_by_label"].items():
            print(f"  nút  {k:<12} {v:>7,}")
        for k, v in rec["edges_by_type"].items():
            print(f"  cạnh {k:<12} {v:>7,}")
        rate = rec["ref_rate_total"]
        print(
            f"  span dẫn chiếu phân giải được: {rate * 100:.2f}% "
            f"(bỏ Phụ lục chưa có unit: {rec['ref_rate_excl_appendix'] * 100:.2f}%)"
            f"  ·  không phân giải: "
            f"{rec['n_unresolved']}  ·  cạnh treo: {rec['n_dangling']}"
            if rate is not None
            else "  không có span dẫn chiếu"
        )
        print(f"bảng tổng hợp: {gp.summary}  ·  rà tay: {gp.review}")
    for p in rec.get("problems") or []:
        print(f"  LỖI: {p}", file=sys.stderr)
    return 0 if rec["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
