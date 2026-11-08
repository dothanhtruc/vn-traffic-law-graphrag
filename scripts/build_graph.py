"""M5–M6: dựng đồ thị (JSONL) → ``data/graph/``; nạp Neo4j và so khớp hai GraphStore.

    uv run python -m scripts.build_graph [--force] [--review-n 50]
    uv run python -m scripts.build_graph --load-neo4j [--force-load]   # M6: nạp AuraDB
    uv run python -m scripts.build_graph --verify-store                # M6: Embedded ↔ Neo4j

Quan hệ cấu trúc (THUOC, KE_TIEP, CO_PHIEN_BAN) và pháp lý (SUA_DOI, BAI_BO, THAY_THE, HOP_NHAT,
HUONG_DAN, DAN_CHIEU) trích bằng rule/regex, không dùng LLM. Resume theo hash đầu vào
(``graph_report.jsonl``); **sửa code M5 thì chạy với ``--force``**.

``--load-neo4j``: nạp 3 file JSONL vào Neo4j (``NEO4J_URI``/``NEO4J_USERNAME``/``NEO4J_PASSWORD``
từ môi trường hoặc ``.env``). Idempotent: ``data_hash`` trùng nút ``_Meta`` → bỏ qua; khác → xoá
theo lô rồi nạp lại. ``--verify-store``: so mọi API đọc giữa EmbeddedStore và Neo4jStore trên
mẫu unit × 4 mốc ngày → ``data/graph/store_parity.jsonl``.

Mã thoát 1 nếu có cạnh treo, phiên bản không có unit, vượt giới hạn AuraDB Free (200k nút /
400k cạnh), số đếm Neo4j lệch JSONL, hoặc hai store lệch nhau. ``--extract`` (M8) chưa có (mã 2).
"""

from __future__ import annotations

import argparse
import sys
import time
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

from trafficlaw.graph.embedded import EmbeddedStore
from trafficlaw.graph.neo4j_store import Neo4jStore
from trafficlaw.graph.parity import build_checks, doc_ids, run_parity, sample_units
from trafficlaw.graph.pipeline import GraphPaths, run_build_graph
from trafficlaw.graph.store import data_hash, load_graph
from trafficlaw.utils.env import load_dotenv
from trafficlaw.utils.git import git_commit
from trafficlaw.utils.jsonl import write_jsonl
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
    ap.add_argument("--force-load", action="store_true", help="(M6) nạp lại Neo4j dù hash trùng")
    ap.add_argument(
        "--verify-store", action="store_true", help="(M6) so EmbeddedStore ↔ Neo4jStore"
    )
    ap.add_argument("--extract", action="store_true", help="(M8) trích xuất thực thể bằng LLM")
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT, help=argparse.SUPPRESS)
    args = ap.parse_args(argv)
    set_seed()
    setup_logging("WARNING")
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")
    if args.extract:
        print("build_graph: --extract (M8) chưa được cài đặt", file=sys.stderr)
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
    if rec["status"] != "ok":
        return 1
    if not (args.load_neo4j or args.verify_store):
        return 0

    paths = _load_yaml(REPO_ROOT / "configs" / "paths.yaml")
    cfg = _load_yaml(root / paths["graph_config"])
    load_dotenv(root / ".env")
    store = Neo4jStore.from_env(
        label_prefix=cfg["neo4j"].get("label_prefix", ""),
        batch_size=int(cfg["neo4j"]["batch_size"]),
        delete_batch_size=int(cfg["neo4j"]["delete_batch_size"]),
    )
    if store is None:
        print(
            "build_graph: thiếu NEO4J_URI / NEO4J_USERNAME / NEO4J_PASSWORD (môi trường hoặc .env)",
            file=sys.stderr,
        )
        return 1
    graph_dir = gp.nodes.parent
    with store:
        store.verify_connectivity()
        code = 0
        if args.load_neo4j:
            code |= _load(store, graph_dir, force=args.force_load, commit=git_commit(root))
        if args.verify_store and code == 0:
            code |= _verify(store, graph_dir, root / paths["graph_store_parity"], cfg["parity"])
    return code


def _load(store: Neo4jStore, graph_dir: Path, *, force: bool, commit: str | None) -> int:
    out = load_graph(store, graph_dir, force=force, git_commit=commit)
    verb = "bỏ qua — dữ liệu không đổi" if out.action == "skipped" else "đã nạp"
    print(f"neo4j: {verb} (data_hash {out.data_hash[:12]}, {out.seconds:.1f}s)")
    for kind in ("nodes", "edges"):
        for k, v in out.expected[kind].items():
            got = out.actual[kind].get(k, 0)
            mark = "" if got == v else f"  ≠ Neo4j {got:,}"
            print(f"  {'nút ' if kind == 'nodes' else 'cạnh'} {k:<12} {v:>7,}{mark}")
    extra = {
        k: v
        for kind in ("nodes", "edges")
        for k, v in out.actual[kind].items()
        if k not in out.expected[kind]
    }
    if extra:
        print(f"  Neo4j có thêm: {extra}")
    if not out.ok:
        print("neo4j: LỖI — số đếm lệch JSONL", file=sys.stderr)
        return 1
    return 0


def _verify(store: Neo4jStore, graph_dir: Path, out_path: Path, pcfg: dict[str, Any]) -> int:
    meta = store.meta()
    h = data_hash(graph_dir)
    if not meta or meta.get("data_hash") != h:
        print("verify-store: Neo4j chưa nạp dữ liệu hiện hành — chạy --load-neo4j", file=sys.stderr)
        return 1
    emb = EmbeddedStore.from_dir(graph_dir)
    dates = [d if isinstance(d, date) else date.fromisoformat(str(d)) for d in pcfg["dates"]]
    units = sample_units(emb, int(pcfg["n_units"]), int(pcfg["seed"]))
    docs = doc_ids(emb)
    c = emb.count()
    checks = build_checks(
        units, docs, dates, node_labels=list(c["nodes"]), edge_types=list(c["edges"])
    )
    print(
        f"verify-store: {len(units)} unit + {len(docs)} văn bản × {len(dates)} mốc "
        f"→ {len(checks):,} truy vấn"
    )
    t0 = time.monotonic()
    n_ok = 0
    by_api: dict[str, list[int]] = {}
    recs: list[dict[str, Any]] = []
    for rec in run_parity(emb, store, checks, workers=int(pcfg["workers"])):
        recs.append(rec)
        n_ok += rec["ok"]
        s = by_api.setdefault(rec["api"], [0, 0])
        s[0] += rec["ok"]
        s[1] += 1
    summary = {
        "kind": "summary",
        "data_hash": h,
        "n_units": len(units),
        "n_docs": len(docs),
        "dates": [d.isoformat() for d in dates],
        "n_checks": len(recs),
        "n_ok": n_ok,
        "by_api": {k: {"ok": v[0], "n": v[1]} for k, v in sorted(by_api.items())},
        "seconds": round(time.monotonic() - t0, 1),
        "run_at": datetime.now().astimezone().isoformat(timespec="seconds"),
    }
    write_jsonl(out_path, [summary, *recs])
    for k, v in summary["by_api"].items():
        print(f"  {k:<16} {v['ok']:>6,}/{v['n']:<6,}")
    pct = 100 * n_ok / max(1, len(recs))
    print(
        f"verify-store: {n_ok:,}/{len(recs):,} khớp ({pct:.2f}%), "
        f"{summary['seconds']}s → {out_path}"
    )
    return 0 if n_ok == len(recs) else 1


if __name__ == "__main__":
    raise SystemExit(main())
