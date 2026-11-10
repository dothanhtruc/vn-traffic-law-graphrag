"""M8: P/R/F1 trích xuất trên ``data/qa/gold_extraction.jsonl`` (chỉ mục ``reviewed: true``).

    uv run python -m scripts.eval_extraction

Dự đoán = ứng viên hiện hành ``data/processed/extraction/candidates_{nodes,edges}.jsonl`` (chạy
``build_graph --extract`` trước). In P/R/F1 thực thể + quan hệ (tổng, theo loại, tier, tầng),
CI 95% bootstrap theo bản ghi, độ phủ reviewed/total, tỷ lệ người sửa bản nháp. Ghi
``eval_report.json`` (kèm ``candidates_sha256`` để ``--publish`` kiểm tra) + ``eval_report.md``.
Mã 0 nếu đạt ngưỡng, 1 nếu chưa đạt / chưa có mục reviewed.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from scripts.extraction_gold import diff_summary
from trafficlaw.eval.extraction_metrics import (
    PredIndex,
    aggregate,
    bootstrap_ci,
    gold_entities,
    pred_for_record,
    score_record,
)
from trafficlaw.graph.extract_env import ExtractEnv
from trafficlaw.graph.extract_pipeline import candidates_sha256
from trafficlaw.utils.dates import parse_iso
from trafficlaw.utils.git import git_commit
from trafficlaw.utils.jsonl import read_jsonl
from trafficlaw.utils.logging import setup_logging
from trafficlaw.utils.seed import set_seed

REPO_ROOT = Path(__file__).resolve().parents[1]


def evaluate(
    gold: list[dict[str, Any]], idx: PredIndex, *, span_f1: float, n_boot: int, seed: int
) -> dict[str, Any]:
    scores = []
    for r in gold:
        ge, gr = gold_entities(r)
        as_of = parse_iso(str(r["as_of"]))
        assert as_of is not None
        pe, pr = pred_for_record(idx, [u["version_id"] for u in r["units"]], as_of)
        scores.append(score_record(r["gold_id"], r["tier"], r["stratum"], ge, gr, pe, pr, span_f1))
    rep = aggregate(scores)
    rep["ci95"] = {
        "entity_f1": bootstrap_ci(scores, "entity", n=n_boot, seed=seed),
        "relation_f1": bootstrap_ci(scores, "relation", n=n_boot, seed=seed),
    }
    rep["per_record"] = [
        {
            "gold_id": s.gold_id,
            "entity": s.total("entity").prf(),
            "relation": s.total("relation").prf(),
        }
        for s in scores
    ]
    return rep


def _fmt(x: Any) -> str:
    return "—" if x is None else f"{x:.3f}"


def render_md(rep: dict[str, Any]) -> str:
    lines = [
        "# Đánh giá trích xuất (M8)",
        "",
        f"- Chạy {rep['run_at']} · commit `{rep['git_commit']}` · ứng viên "
        f"`{rep['candidates_sha256'][:12]}`",
        f"- Gold reviewed {rep['n_reviewed']}/{rep['n_total']} bản ghi · ngưỡng span "
        f"{rep['span_f1']}",
        f"- Ngưỡng nạp: F1 thực thể ≥ {rep['min_entity_f1']}, F1 quan hệ ≥ "
        f"{rep['min_relation_f1']} → **{'ĐẠT' if rep['pass'] else 'CHƯA ĐẠT'}**",
        "",
        "| | P | R | F1 | CI 95% | TP | FP | FN |",
        "| --- | ---: | ---: | ---: | --- | ---: | ---: | ---: |",
    ]
    for k in ("entity", "relation"):
        o = rep["overall"][k]
        ci = rep["ci95"][f"{k}_f1"]
        cis = "—" if ci is None else f"{ci[0]:.3f}–{ci[1]:.3f}"
        lines.append(
            f"| {k} | {_fmt(o['precision'])} | {_fmt(o['recall'])} | {_fmt(o['f1'])} | "
            f"{cis} | {o['tp']} | {o['fp']} | {o['fn']} |"
        )
    for title, key in (
        ("Theo loại", "by_type"),
        ("Theo tier", "by_tier"),
        ("Theo tầng mẫu", "by_stratum"),
    ):
        lines += [
            "",
            f"## {title}",
            "",
            "| nhóm | P | R | F1 | TP | FP | FN |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
        if key == "by_type":
            rows = [(f"{k}:{t}", v) for k in ("entity", "relation") for t, v in rep[key][k].items()]
        else:
            rows = [(f"{g}:{k}", v[k]) for g, v in rep[key].items() for k in ("entity", "relation")]
        for name, o in rows:
            lines.append(
                f"| {name} | {_fmt(o['precision'])} | {_fmt(o['recall'])} | {_fmt(o['f1'])} "
                f"| {o['tp']} | {o['fp']} | {o['fn']} |"
            )
    d = rep.get("edits") or {}
    if d.get("n_reviewed_with_draft"):
        lines += [
            "",
            "## Tỷ lệ người sửa bản nháp LLM",
            "",
            f"- {d['n_reviewed_with_draft']} bản ghi · thực thể {d['entity_edit_rate']:.1%} "
            f"· quan hệ {d['relation_edit_rate']:.1%}",
            f"- {d['totals']}",
        ]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT, help=argparse.SUPPRESS)
    args = ap.parse_args(argv)
    set_seed()
    setup_logging("WARNING")
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")
    env = ExtractEnv(args.repo_root)
    ev = env.eval
    gpath = env.p(env.gold.get("path", "data/qa/gold_extraction.jsonl"))
    allrecs = list(read_jsonl(gpath))
    gold = [r for r in allrecs if r.get("reviewed")]
    print(f"eval_extraction: gold reviewed {len(gold)}/{len(allrecs)} bản ghi")
    paths = env.paths
    if not paths.cand_nodes.is_file():
        print("eval_extraction: chưa có ứng viên — chạy build_graph --extract", file=sys.stderr)
        return 1
    idx = PredIndex.build(read_jsonl(paths.cand_nodes), read_jsonl(paths.cand_edges))
    span_f1 = float(ev.get("span_f1", 0.5))
    rep = evaluate(
        gold,
        idx,
        span_f1=span_f1,
        n_boot=int(ev.get("bootstrap", 1000)),
        seed=int(ev.get("seed", 42)),
    )
    ef, rf = rep["overall"]["entity"]["f1"], rep["overall"]["relation"]["f1"]
    min_e, min_r = float(ev.get("min_entity_f1", 0.85)), float(ev.get("min_relation_f1", 0.80))
    rep.update(
        {
            "run_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "git_commit": git_commit(args.repo_root),
            "candidates_sha256": candidates_sha256(paths),
            "n_reviewed": len(gold),
            "n_total": len(allrecs),
            "span_f1": span_f1,
            "min_entity_f1": min_e,
            "min_relation_f1": min_r,
            "pass": bool(gold)
            and ef is not None
            and rf is not None
            and ef >= min_e
            and rf >= min_r,
            "edits": diff_summary(allrecs, span_f1),
        }
    )
    out = env.p(ev.get("report_path", "data/processed/extraction/eval_report.json"))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(json.dumps(rep, ensure_ascii=False, indent=2).encode("utf-8"))
    md = render_md(rep)
    out.with_suffix(".md").write_bytes(md.encode("utf-8"))
    print(md)
    return 0 if rep["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
