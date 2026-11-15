"""M11: truy hồi Graph RAG (``retrieve()``) — một câu hỏi, đánh giá trên val/train, dry-run.

    uv run python -m scripts.retrieve --question "…" --as-of 2026-01-01 --config G [--no-llm]
    uv run --group tok python -m scripts.retrieve --dry-run [--eval val,train_1000] [--configs …]
    uv run python -m scripts.retrieve --analyze-only [--eval val,train_1000] [--workers 16]
    uv run --no-sync python -m scripts.retrieve --eval val,train_1000 --gpu      # máy GPU thuê
    uv run python -m scripts.retrieve --eval val,train_1000                       # local, từ cache

**Không dùng ``data/qa/test.jsonl``** (mục 10): tập đo = val + tập con train (cách lấy mẫu M10).

Hai pha trên máy thuê (người dùng duyệt 15/11/2026, VRAM): (1) ``--analyze-only`` gọi LLM ``main``
qua tunnel cho các câu rule không chắc, lưu ``data/index/analyze/llm.jsonl`` (chạy ở local khi
``tunnel.sh`` + ``gpu.sh serve qwen3-14b-awq``); (2) ``stop-serve`` rồi ``--eval --gpu`` trên máy
thuê: encode câu hỏi thiếu vector + chấm rerank, cache ``data/index/rerank/<key>/``. Kéo cache về
⇒ ``--eval`` ở local tái lập y hệt, không cần GPU.

Mã thoát: 1 = lỗi; 2 = thiếu cache (vector / điểm rerank / kết quả LLM analyzer).
"""

from __future__ import annotations

import argparse
import json
import logging
import statistics
import sys
import time
from collections import Counter, defaultdict
from collections.abc import Sequence
from datetime import date
from pathlib import Path
from typing import Any

from trafficlaw.eval.qa_schema import QAItem
from trafficlaw.eval.retrieval_eval import EvalQuery, stratified_sample, to_queries
from trafficlaw.eval.retrieval_linked import linked_coverage
from trafficlaw.eval.retrieval_metrics import score_query, summarize
from trafficlaw.retrieval.analyze import MissingLLMAnalysisError
from trafficlaw.retrieval.config import RetrievalConfig, load_retrieval_config
from trafficlaw.retrieval.index_pipeline import MissingVectorsError, now_iso
from trafficlaw.retrieval.rerank import MissingRerankScoresError
from trafficlaw.retrieval.retrieve import RetrievalContext, RetrievalResult
from trafficlaw.retrieval.retrieve_env import build_analyzer, build_context
from trafficlaw.utils.git import git_commit
from trafficlaw.utils.jsonl import append_jsonl, read_jsonl, write_jsonl
from trafficlaw.utils.logging import setup_logging
from trafficlaw.utils.seed import set_seed

REPO_ROOT = Path(__file__).resolve().parents[1]
logger = logging.getLogger("retrieve")
MISSING = (MissingVectorsError, MissingRerankScoresError, MissingLLMAnalysisError)


def query_sets(
    root: Path, cfg: RetrievalConfig, names: Sequence[str]
) -> dict[str, list[EvalQuery]]:
    e = cfg.eval
    val = to_queries([QAItem.model_validate(r) for r in read_jsonl(root / e.val)])
    train = to_queries([QAItem.model_validate(r) for r in read_jsonl(root / e.train)])
    sample = stratified_sample(train, e.train_sample, seed=e.seed, name="retrieval_train")
    avail = {"val": val, f"train_{len(sample)}": sample}
    out = {}
    for n in names:
        if n not in avail:
            raise SystemExit(f"tập {n!r} không có (có: {', '.join(avail)}); test không được dùng")
        out[n] = avail[n]
    return out


def llm_main_model(root: Path) -> str | None:
    from trafficlaw.llm import load_llm_config

    return load_llm_config(root / "configs" / "llm.yaml").main.model_id


# --- một câu hỏi -----------------------------------------------------------------------------


def cmd_question(root: Path, cfg: RetrievalConfig, args: argparse.Namespace) -> int:
    an = build_analyzer(
        root, cfg, today=args.today, llm_model_id=llm_main_model(root), strict=False
    )
    ctx = build_context(root, cfg, an, gpu=args.gpu)
    as_of = date.fromisoformat(args.as_of) if args.as_of else None
    try:
        r = ctx.retrieve(args.question, as_of, args.config, use_llm=not args.no_llm)
    except MISSING as e:
        print(f"thiếu cache: {e}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(r.model_dump(mode="json"), ensure_ascii=False, indent=2))
        return 0
    a = r.analysis
    print(
        f"[{r.config_name}] as_of {r.as_of} ({a.as_of_source}) · loại {a.question_type}"
        f" {a.modifiers} · PT {a.vehicle_ids} · CT {a.subject_ids} · VB {a.doc_hints}"
        f" · analyzer {a.analyzer} {a.llm_status or ''} {a.uncertain}"
    )
    for h in r.hits:
        src = ", ".join(
            s.source if s.source != "graph" else f"graph:{s.edge_type}/h{s.hop}" for s in h.sources
        )
        c = ctx.catalog.get(h.chunk_id)
        print(f"{h.rank}. {h.chunk_id}  [{h.score:.4f}]  ({src})")
        print("   " + c.text.replace("\n", " ")[:220])
    print("timings_ms", r.timings_ms)
    return 0


# --- analyze (pha 1) -------------------------------------------------------------------------


def cmd_analyze_only(root: Path, cfg: RetrievalConfig, args: argparse.Namespace) -> int:
    from scripts._llm_local import check_local_server, resolve_model
    from trafficlaw.llm import build_client, load_llm_config
    from trafficlaw.llm.parallel import map_parallel

    if not cfg.analyze.llm_fallback:
        print("analyze.llm_fallback = false — không có gì để chạy")
        return 0
    llm_cfg = load_llm_config(root / "configs" / "llm.yaml")
    provider, model_id = resolve_model(llm_cfg, None, args.model)
    if not model_id:
        print("chưa chốt model_id (configs/llm.yaml main)", file=sys.stderr)
        return 1
    meta = check_local_server(llm_cfg, provider, model_id, root)
    if meta is None:
        return 1
    client = build_client(llm_cfg, provider, model_id=model_id, root=root)
    an = build_analyzer(root, cfg, today=args.today, llm=client, strict=False)
    qs = [q for s in query_sets(root, cfg, args.sets).values() for q in s]
    uniq = list({(q.question, q.as_of): q for q in qs}.values())
    t0 = time.perf_counter()
    statuses: Counter[str] = Counter()
    for _, res in map_parallel(uniq, lambda q: an.analyze(q.question, q.as_of), args.workers):
        if isinstance(res, Exception):
            print(f"dừng: {res}", file=sys.stderr)
            return 3
        statuses[res.llm_status or "rule_chac"] += 1
    rec = {
        "phase": "analyze",
        "model_id": model_id,
        "serve": meta,
        "n_questions": len(uniq),
        "statuses": dict(statuses),
        "seconds": round(time.perf_counter() - t0, 1),
        "git_commit": git_commit(root),
        "finished_at": now_iso(),
    }
    append_jsonl(root / cfg.index_dir / "analyze" / "runs.jsonl", rec)
    print(json.dumps(rec, ensure_ascii=False))
    return 0 if statuses.get("error", 0) == 0 else 1


# --- đánh giá --------------------------------------------------------------------------------


def _pct(xs: Sequence[float], p: float) -> float | None:
    if not xs:
        return None
    s = sorted(xs)
    return round(s[min(len(s) - 1, int(p * len(s)))], 2)


def summarize_runs(
    results: Sequence[RetrievalResult], qs: Sequence[EvalQuery], ctx: RetrievalContext
) -> dict[str, Any]:
    cat = ctx.catalog
    by_qid = {q.qid: q for q in qs}
    scores = []
    tiers: dict[str, list[Any]] = defaultdict(list)
    types: dict[str, list[Any]] = defaultdict(list)
    linked_items = []
    out_of_effect = 0
    graph_in_top = 0
    n_expanded = []
    for r in results:
        q = by_qid[str(r.qid)]
        rel = cat.relevant(list(q.gold_units), q.as_of)
        s = score_query(q.qid, r.ranked, rel)
        scores.append(s)
        tiers[str(q.tier)].append(s)
        types[q.question_type].append(s)
        linked_items.append((q.qid, list(q.gold_units), q.as_of, r.ranked))
        live = cat.ids_at(q.as_of)
        out_of_effect += sum(1 for h in r.hits if h.chunk_id not in live)
        graph_in_top += sum(1 for h in r.hits if all(x.source == "graph" for x in h.sources))
        n_expanded.append(sum(1 for p in r.pool if all(x.source == "graph" for x in p.sources)))
    res: dict[str, Any] = summarize(
        scores, ci_metrics=("recall@1", "recall@5", "recall@10", "mrr@10", "ndcg@10"), seed=42
    )
    res["recall@5_tier"] = {
        t: {"n": len(v), "recall@5": summarize(v)["recall@5"]} for t, v in sorted(tiers.items())
    }
    res["recall@5_loai"] = {
        t: {"n": len(v), "recall@5": summarize(v)["recall@5"]} for t, v in sorted(types.items())
    }
    res["lien_ket@5"] = linked_coverage(ctx.store, cat, linked_items, k=5)
    res["lien_ket@10"] = linked_coverage(ctx.store, cat, linked_items, k=10)
    n_hits = sum(len(r.hits) for r in results) or 1
    res["top5_ngoai_hieu_luc"] = out_of_effect / n_hits
    res["top5_chi_tu_do_thi"] = graph_in_top / n_hits
    res["pool_mo_rong_tb"] = statistics.fmean(n_expanded) if n_expanded else 0.0
    an = [r.analysis for r in results]
    res["analyzer"] = {
        "goi_llm": sum(1 for a in an if a.llm_reason) / len(an) if an else 0.0,
        "llm_status": dict(Counter(a.llm_status or "khong_goi" for a in an)),
        "ly_do": dict(Counter(x for a in an for x in a.uncertain)),
        "loai_cau": dict(Counter(a.question_type or "none" for a in an)),
        "analyzer": dict(Counter(a.analyzer for a in an)),
    }
    steps = sorted({k for r in results for k in r.timings_ms})
    res["latency_ms"] = {
        k: {
            "p50": _pct([r.timings_ms[k] for r in results if k in r.timings_ms], 0.5),
            "p95": _pct([r.timings_ms[k] for r in results if k in r.timings_ms], 0.95),
        }
        for k in steps
    }
    return res


def cmd_eval(root: Path, cfg: RetrievalConfig, args: argparse.Namespace) -> int:
    an = build_analyzer(
        root,
        cfg,
        today=args.today,
        llm_model_id=llm_main_model(root),
        strict=not args.no_llm,
    )
    ctx = build_context(root, cfg, an, gpu=args.gpu)
    sets = query_sets(root, cfg, args.sets)
    out_dir = root / cfg.index_dir / "retrieval_eval"
    t_start = time.perf_counter()
    report: dict[str, Any] = {"sets": {}, "configs": {}}
    for name in args.configs:
        sc = cfg.system(name)
        report["configs"][name] = {
            **sc.model_dump(),
            "dense_key": cfg.dense_key(sc),
            "reranker_key": cfg.reranker_key_for(sc),
        }
    for set_name, qs in sets.items():
        report["sets"][set_name] = {}
        for name in args.configs:
            t0 = time.perf_counter()
            rows: list[RetrievalResult] = []
            try:
                for i, q in enumerate(qs, 1):
                    rows.append(
                        ctx.retrieve(q.question, q.as_of, name, qid=q.qid, use_llm=not args.no_llm)
                    )
                    if i % 200 == 0:
                        logger.info("[%s] %s: %d/%d", set_name, name, i, len(qs))
            except MISSING as e:
                print(f"[{set_name}] {name}: thiếu cache — {e}", file=sys.stderr)
                return 2
            write_jsonl(out_dir / set_name / f"{name}.jsonl", rows)
            r = summarize_runs(rows, qs, ctx)
            r["seconds"] = round(time.perf_counter() - t0, 1)
            report["sets"][set_name][name] = r
            print(
                f"[{set_name}] {name}: R@5 {100 * r['recall@5']:.1f} · R@20"
                f" {100 * r['recall@20']:.1f} · MRR@10 {100 * r['mrr@10']:.1f} · liên kết@5"
                f" {_fmt(r['lien_ket@5']['do_phu'])} · ngoài hiệu lực"
                f" {100 * r['top5_ngoai_hieu_luc']:.1f}%"
                f" ({r['seconds']} s)"
            )
    wall = time.perf_counter() - t_start
    report["meta"] = run_meta(root, cfg, ctx, args, wall)
    if args.gpu:
        for key, st in ctx.rerank_totals.items():
            append_jsonl(
                root / cfg.index_dir / "rerank" / key / "runs.jsonl",
                {**st.to_dict(), **report["meta"]["gpu"], "finished_at": now_iso()},
            )
    path = root / cfg.index_dir / "retrieval_eval.json"
    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
        newline="\n",
    )
    md = render_md(report)
    path.with_suffix(".md").write_text(md, encoding="utf-8", newline="\n")
    print(f"→ {path.with_suffix('.md')}")
    return 0


def run_meta(
    root: Path, cfg: RetrievalConfig, ctx: RetrievalContext, args: argparse.Namespace, wall: float
) -> dict[str, Any]:
    gpu: dict[str, Any] = {"used": bool(args.gpu)}
    if args.gpu:
        try:
            import torch

            if torch.cuda.is_available():
                gpu.update(
                    name=torch.cuda.get_device_name(0),
                    peak_vram_gb=round(torch.cuda.max_memory_allocated() / 2**30, 3),
                    torch=torch.__version__,
                )
        except ImportError:  # pragma: no cover
            pass
        from trafficlaw.llm.serve import load_serve_config

        price = load_serve_config(root / "configs" / "serve.yaml").remote.price_vnd_per_hour
        gpu["wall_hours"] = round(wall / 3600, 4)
        gpu["vnd"] = round(wall / 3600 * price)
    an_runs = list(read_jsonl(root / cfg.index_dir / "analyze" / "runs.jsonl"))
    return {
        "generated_at": now_iso(),
        "git_commit": git_commit(root),
        "data_version": ctx.meta.get("data_version"),
        "catalog_sha256": ctx.meta.get("catalog_sha256"),
        "graph_data_hash": ctx.meta.get("graph_data_hash"),
        "n_chunks": len(ctx.catalog),
        "embedding": {
            k: cfg.spec(k).model_dump(include={"hf_repo", "revision"})
            for k in cfg.models
            if k == cfg.model_key
        },
        "reranker": {
            k: cfg.reranker(k).model_dump(include={"hf_repo", "revision", "max_length"})
            for k in cfg.rerankers
        },
        "llm_model": ctx.analyzer.model_id,
        "prompt_hash": ctx.analyzer.prompt.hash if ctx.analyzer.prompt else None,
        "no_llm": bool(args.no_llm),
        "expand": cfg.expand.model_dump(),
        "rerank_totals": {k: v.to_dict() for k, v in ctx.rerank_totals.items()},
        "analyze_runs": an_runs[-1:] if an_runs else [],
        "wall_s": round(wall, 1),
        "gpu": gpu,
    }


def _fmt(x: object) -> str:
    return f"{100 * float(x):.1f}" if isinstance(x, (int, float)) else "—"


def _ci(x: object) -> str:
    if isinstance(x, (tuple, list)) and len(x) == 2:
        return f"{100 * x[0]:.1f}–{100 * x[1]:.1f}"
    return "—"


COLS = (
    "Cấu hình",
    "R@1",
    "R@5",
    "CI R@5",
    "R@10",
    "R@20",
    "MRR@10",
    "CI MRR",
    "nDCG@10",
    "Liên kết@5 (n)",
    "Liên kết@10",
    "Top-5 ngoài hiệu lực",
    "Top-5 chỉ từ đồ thị",
    "Chunk mở rộng/câu",
)


def render_md(report: dict[str, Any]) -> str:
    m = report["meta"]
    lines = [
        "# Đánh giá truy hồi M11 (val + tập con train — KHÔNG dùng test)",
        "",
        f"Sinh lúc {m['generated_at']} · commit `{m['git_commit']}` · {m['n_chunks']} chunk"
        f" (catalog `{(m['catalog_sha256'] or '')[:12]}`) · data_version"
        f" `{(m['data_version'] or '')[:12]}`"
        f" · graph `{(m['graph_data_hash'] or '')[:12]}`",
        "",
        f"Embedding: {json.dumps(m['embedding'], ensure_ascii=False)} · reranker:"
        f" {json.dumps(m['reranker'], ensure_ascii=False)} · LLM analyzer: `{m['llm_model']}`"
        f" (prompt `{(m['prompt_hash'] or '')[:12]}`{', TẮT' if m['no_llm'] else ''}).",
        "",
        "Chunk đúng = chunk hiệu lực tại as_of chứa gold unit; R@k cấp unit; CI 95% bootstrap 1.000"
        " lần theo câu (seed 42). **Liên kết@k** = tỷ lệ đơn vị liên kết của gold (Khoản chế tài"
        " nối"
        " bằng BI_XU_PHAT/BI_TRU_DIEM `dan_chieu`; DAN_CHIEU sang Điều khác) có chunk trong top-k —"
        " đo lợi ích graph expand trên câu một chunk; đánh giá G chính thức là việc của M13 trên"
        " test."
        " Câu val/train do mistral-small-3.2 sinh từ chính chunk ⇒ thiên lệch từ vựng.",
        "",
    ]
    for set_name, systems in report["sets"].items():
        n = next(iter(systems.values()), {}).get("n", 0)
        lines += [
            f"## {set_name} ({n} câu)",
            "",
            "| " + " | ".join(COLS) + " |",
            "| --- |" + " ---: |" * (len(COLS) - 1),
        ]
        for name, r in systems.items():
            lk, lk10 = r["lien_ket@5"], r["lien_ket@10"]
            lines.append(
                f"| {name} | {_fmt(r['recall@1'])} | {_fmt(r['recall@5'])}"
                f" | {_ci(r['recall@5_ci'])}"
                f" | {_fmt(r['recall@10'])} | {_fmt(r['recall@20'])} | {_fmt(r['mrr@10'])}"
                f" | {_ci(r['mrr@10_ci'])} | {_fmt(r['ndcg@10'])}"
                f" | {_fmt(lk['do_phu'])} ({lk['n_cau_co_lien_ket']}) | {_fmt(lk10['do_phu'])}"
                f" | {_fmt(r['top5_ngoai_hieu_luc'])} | {_fmt(r['top5_chi_tu_do_thi'])}"
                f" | {r['pool_mo_rong_tb']:.1f} |"
            )
        tiers = sorted({t for r in systems.values() for t in r["recall@5_tier"]})
        lines += [
            "",
            "**R@5 theo tier** (n):",
            "",
            "| Cấu hình | " + " | ".join(tiers) + " |",
            "| --- |" + " ---: |" * len(tiers),
        ]
        for name, r in systems.items():
            rt = r["recall@5_tier"]
            lines.append(
                f"| {name} | "
                + " | ".join(
                    f"{_fmt(rt[t]['recall@5'])} ({rt[t]['n']})" if t in rt else "—" for t in tiers
                )
                + " |"
            )
        lines += ["", "**Liên kết theo loại** (top-5: độ phủ, số liên kết):", ""]
        for name, r in systems.items():
            tl = r["lien_ket@5"]["theo_loai"]
            lines.append(
                f"- {name}: "
                + "; ".join(f"{k} {_fmt(v['do_phu'])} (n={v['n']})" for k, v in tl.items())
            )
        lines += ["", "**Analyzer + latency (ms, p50/p95):**", ""]
        for name, r in systems.items():
            a = r["analyzer"]
            lat = ", ".join(f"{k} {v['p50']}/{v['p95']}" for k, v in r["latency_ms"].items())
            lines.append(f"- {name}: gọi LLM {_fmt(a['goi_llm'])}% · {a['llm_status']} · {lat}")
        lines.append("")
    g = m["gpu"]
    lines += [
        "## Chạy",
        "",
        f"- Bảng mở rộng: `{json.dumps(m['expand'], ensure_ascii=False)}`",
        f"- Rerank: `{json.dumps(m['rerank_totals'], ensure_ascii=False)}`",
        f"- Analyzer (pha 1): `{json.dumps(m['analyze_runs'], ensure_ascii=False)}`",
        f"- GPU: `{json.dumps(g, ensure_ascii=False)}` · tổng {m['wall_s']} s",
        "",
    ]
    return "\n".join(lines)


# --- dry-run ---------------------------------------------------------------------------------


def cmd_dry_run(root: Path, cfg: RetrievalConfig, args: argparse.Namespace) -> int:
    from trafficlaw.llm.prompt_loader import load_prompt
    from trafficlaw.llm.serve import gpu_hours, load_serve_config
    from trafficlaw.retrieval.analyze import analyze_rule, render_llm_messages
    from trafficlaw.retrieval.rerank import make_counter, pair_key, pair_windows

    scfg = load_serve_config(root / "configs" / "serve.yaml")
    price = scfg.remote.price_vnd_per_hour
    an = build_analyzer(
        root, cfg, today=args.today, llm_model_id=llm_main_model(root), strict=False
    )
    # Pool trước rerank: bật cùng cấu hình nhưng tắt reranker (không cần model).
    dry = cfg.model_copy(deep=True)
    for sc in dry.configs.values():
        sc.reranker = False
    ctx = build_context(root, dry, an, gpu=False)
    sets = query_sets(root, cfg, args.sets)
    tables = an.tables
    prompt = load_prompt(cfg.analyze.prompt)
    allq = list({(q.question, q.as_of): q for s in sets.values() for q in s}.values())
    unc = [q for q in allq if analyze_rule(q.question, q.as_of, tables, today=args.today).uncertain]
    llm_tok = sum(
        len(render_llm_messages(prompt, q.question, q.as_of, tables)[0]["content"]) for q in unc
    )
    llm_in = int(llm_tok / 4 * 2.3)  # tiếng Việt ≈ 2,3× ước len/4 (đo ở M9)
    llm_out = 80 * len(unc)
    h_llm, _ = gpu_hours(scfg, llm_main_model(root), llm_in, llm_out)
    print(
        f"{len(allq)} câu (val + tập con train) · rule không chắc {len(unc)}"
        f" ({100 * len(unc) / max(1, len(allq)):.1f}%) → LLM ~{llm_in:,} token vào (ước len/4×2,3,"
        f" prefix caching giảm thêm) / ~{llm_out:,} ra ≈ {h_llm * 60:.1f} phút GPU + khởi động vLLM"
    )
    missing_q = 0
    if cfg.model_key:
        missing_q = len(ctx.encoder.missing(cfg.model_key, [q.question for q in allq]))
    print(f"vector câu hỏi thiếu trong cache ({cfg.model_key}): {missing_q}")
    rr_key = cfg.reranker_key
    tot_h = h_llm + 5 / 60
    if rr_key:
        spec = cfg.reranker(rr_key)
        try:
            counter = make_counter(spec)
        except ImportError:
            print(
                "cần nhóm tok: uv run --group tok python -m scripts.retrieve --dry-run",
                file=sys.stderr,
            )
            return 1
        cache = ctx.rerank_cache(rr_key)
        pairs: dict[str, tuple[str, str, str]] = {}
        per_cfg: dict[str, int] = {}
        for name in args.configs:
            sc = cfg.system(name)
            if cfg.reranker_key_for(sc) != rr_key:
                continue
            n0 = len(pairs)
            for qs in sets.values():
                for q in qs:
                    r = ctx.retrieve(q.question, q.as_of, name, qid=q.qid, use_llm=True)
                    for p in r.pool:
                        text = ctx.catalog.get(p.chunk_id).text
                        k = pair_key(rr_key, spec, q.question, text)
                        if cache.get(k) is None:
                            pairs.setdefault(k, (q.question, p.chunk_id, text))
            per_cfg[name] = len(pairs) - n0
        n_win = n_tok = n_trunc = 0
        for question, cid, text in pairs.values():
            ws = pair_windows(cid, question, text, counter.count_tokens, spec.max_length)
            n_win += len(ws)
            n_trunc += sum(1 for w in ws if w.truncated)
            n_tok += sum(min(w.n_tokens, spec.max_length) for w in ws)
        h_rr = n_win / spec.pairs_per_s / 3600 + spec.load_min / 60
        tot_h += h_rr
        print(
            f"rerank {rr_key}@{(spec.revision or 'CHƯA GHIM')[:7]}: {len(pairs):,} cặp mới"
            f" (theo cấu hình, cộng dồn: {per_cfg}) · {n_win:,} cửa sổ ({n_trunc} còn cắt) ·"
            f" {n_tok:,} token · ~{h_rr * 60:.1f} phút GPU ({spec.pairs_per_s:.0f} cửa sổ/s + nạp"
            f" {spec.load_min} phút)"
        )
    print(
        f"Tổng ~{tot_h:.2f} giờ GPU ≈ {round(tot_h * price):,} VND (giá {price:,} VND/giờ; chưa gồm"
        " setup ~10–20 phút, tải model)"
    )
    return 0


# --- main ------------------------------------------------------------------------------------


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--config-file", type=Path, default=REPO_ROOT / "configs" / "retrieval.yaml")
    ap.add_argument("--question")
    ap.add_argument("--as-of", help="YYYY-MM-DD (thắng ngày trong câu hỏi)")
    ap.add_argument("--config", default="G")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--eval", dest="sets", default="val,train_1000")
    ap.add_argument("--configs", default="B1,B2,B3,G,A1,A2")
    ap.add_argument("--analyze-only", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-llm", action="store_true", help="tắt LLM dự phòng của analyzer")
    ap.add_argument("--gpu", action="store_true", help="nạp model khi thiếu cache (máy thuê)")
    ap.add_argument("--model", help="model LLM (mặc định main)")
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--today", type=date.fromisoformat, default=date.today())
    args = ap.parse_args(argv)
    setup_logging()
    set_seed(42)
    args.sets = [s for s in args.sets.split(",") if s]
    args.configs = [c for c in args.configs.split(",") if c]
    cfg = load_retrieval_config(args.config_file)
    for c in args.configs:
        cfg.system(c)
    root = REPO_ROOT
    if args.question:
        return cmd_question(root, cfg, args)
    if args.dry_run:
        return cmd_dry_run(root, cfg, args)
    if args.analyze_only:
        return cmd_analyze_only(root, cfg, args)
    return cmd_eval(root, cfg, args)


if __name__ == "__main__":
    raise SystemExit(main())
