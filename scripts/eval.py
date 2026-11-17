"""M13: bộ chạy đánh giá ba giai đoạn trên test (CLAUDE.md mục 10, "Quy ước bộ chạy đánh giá").

    uv run python -m scripts.eval smoke --fake                    # CI, < 60 s
    uv run --group tok python -m scripts.eval retrieve --dry-run  # analyzer + rerank: giờ GPU
    uv run python -m scripts.eval retrieve --analyze-only         # pha 1: LLM analyzer (tunnel)
    uv run --no-sync python -m scripts.eval retrieve --gpu        # pha 2 (máy thuê): encode+rerank
    uv run python -m scripts.eval retrieve                        # local: dựng lại từ cache
    uv run --group tok python -m scripts.eval generate --dry-run  # token thật, giờ GPU, VND
    uv run python -m scripts.eval generate [--workers 16] [--configs G,B3] [--no-variance]
    uv run --group tok python -m scripts.eval score --dry-run     # judge: giờ GPU, VND
    uv run python -m scripts.eval score --judge [--workers 16]    # judge mistral qua tunnel
    uv run python -m scripts.eval score                           # chỉ số + summary (không GPU)
    uv run python -m scripts.eval judge-check                     # phiếu 40 câu kiểm định judge
    uv run python -m scripts.eval regression [--write-baseline]   # Recall@5 G, regression_100

Kết quả ``results/<run_id>/`` (``run_id`` trong ``configs/eval.yaml``, ghi đè bằng ``--run-id``).
Test **chỉ để đo**: không chỉnh prompt/ngưỡng/tham số theo kết quả ở đây.

Mã thoát: 1 = lỗi; 2 = thiếu cache (vector / điểm rerank / LLM analyzer) hoặc thiếu kết quả giai
đoạn trước; 3 = dừng (quota); 4 = tập con lỗi thời / kết quả lệch dữ liệu.
"""

from __future__ import annotations

import argparse
import json
import logging
import statistics
import sys
import time
from collections.abc import Sequence
from datetime import date
from pathlib import Path
from typing import Any

from trafficlaw.eval.eval_config import EvalConfig, load_eval_config
from trafficlaw.eval.runner import (
    EvalData,
    StaleResultError,
    StaleSubsetsError,
    answers_path,
    load_eval_data,
    load_retrievals,
    retrieve_path,
)
from trafficlaw.pipeline.answer import load_answer_config
from trafficlaw.retrieval.analyze import MissingLLMAnalysisError
from trafficlaw.retrieval.config import load_retrieval_config
from trafficlaw.retrieval.index_pipeline import MissingVectorsError, now_iso
from trafficlaw.retrieval.rerank import MissingRerankScoresError
from trafficlaw.utils.env import load_dotenv
from trafficlaw.utils.git import git_commit
from trafficlaw.utils.jsonl import append_jsonl
from trafficlaw.utils.logging import setup_logging
from trafficlaw.utils.seed import set_seed

REPO_ROOT = Path(__file__).resolve().parents[1]
logger = logging.getLogger("eval")
MISSING = (MissingVectorsError, MissingRerankScoresError, MissingLLMAnalysisError)


# --------------------------------------------------------------------------- nạp


def _progress(tag: str, i: int, n: int) -> None:
    if i % 50 == 0 or i == n:
        logger.info("%s: %d/%d", tag, i, n)


def load_data(root: Path, ecfg: EvalConfig, store: Any) -> EvalData:
    from trafficlaw.eval.qa_test_draft import load_drafts

    drafts = load_drafts(root / ecfg.drafts) if ecfg.drafts else None
    sub = root / ecfg.subsets if ecfg.subsets else None
    data = load_eval_data(root / ecfg.test, sub, store, drafts=drafts)
    if data.invalid:
        print(f"loại {len(data.invalid)} câu test lỗi validator: {data.invalid}", file=sys.stderr)
    return data


def retrieval_env(root: Path, args: argparse.Namespace, *, llm: Any = None, strict: bool = True):
    from scripts.retrieve import llm_main_model
    from trafficlaw.retrieval.retrieve_env import build_analyzer, build_context

    rcfg = load_retrieval_config(root / "configs" / "retrieval.yaml")
    an = build_analyzer(
        root,
        rcfg,
        today=args.today,
        llm=llm,
        llm_model_id=llm_main_model(root),
        strict=strict and llm is None and not args.no_llm,
    )
    return rcfg, build_context(root, rcfg, an, gpu=args.gpu)


def log_run(run_dir: Path, rec: dict[str, Any]) -> None:
    append_jsonl(
        run_dir / "runs.jsonl",
        {**rec, "git_commit": git_commit(REPO_ROOT), "finished_at": now_iso()},
    )


def _gpu_meta(wall: float) -> dict[str, Any]:
    from trafficlaw.llm.serve import load_serve_config

    out: dict[str, Any] = {"wall_s": round(wall, 1)}
    try:
        import torch

        if torch.cuda.is_available():
            out.update(
                gpu=torch.cuda.get_device_name(0),
                peak_vram_gb=round(torch.cuda.max_memory_allocated() / 2**30, 3),
                torch=torch.__version__,
            )
    except ImportError:
        pass
    price = load_serve_config(REPO_ROOT / "configs" / "serve.yaml").remote.price_vnd_per_hour
    out["vnd"] = round(wall / 3600 * price)
    return out


# --------------------------------------------------------------------------- retrieve


def cmd_retrieve(root: Path, ecfg: EvalConfig, args: argparse.Namespace) -> int:
    from trafficlaw.eval.orchestrate import stage_retrieve

    rcfg, rctx = retrieval_env(root, args)
    data = load_data(root, ecfg, rctx.store)
    run_dir = ecfg.run_dir(root, args.run_id)
    t0 = time.perf_counter()
    try:
        stats = stage_retrieve(
            data,
            ecfg,
            rctx,
            run_dir,
            configs=args.configs,
            use_llm=not args.no_llm,
            limit=args.limit,
            progress=_progress,
        )
    except MISSING as e:
        print(f"thiếu cache: {e}", file=sys.stderr)
        return 2
    wall = time.perf_counter() - t0
    rec: dict[str, Any] = {
        "stage": "retrieve",
        "stats": {
            c: {"n_total": s.n_total, "n_skipped": s.n_skipped, "n_written": s.n_written}
            for c, s in stats.items()
        },
        "meta": rctx.meta,
        "rerank_totals": {k: v.to_dict() for k, v in rctx.rerank_totals.items()},
        "gpu": _gpu_meta(wall) if args.gpu else None,
        "wall_s": round(wall, 1),
    }
    log_run(run_dir, rec)
    if args.gpu:
        for key, st in rctx.rerank_totals.items():
            append_jsonl(
                root / rcfg.index_dir / "rerank" / key / "runs.jsonl",
                {
                    **st.to_dict(),
                    **(rec["gpu"] or {}),
                    "run_id": run_dir.name,
                    "finished_at": now_iso(),
                },
            )
    for c, s in stats.items():
        print(f"retrieve {c}: ghi {s.n_written}, bỏ qua {s.n_skipped} / {s.n_total}")
    return 0


def test_questions(data: EvalData, ecfg: EvalConfig, configs: Sequence[str] | None) -> list[Any]:
    from trafficlaw.eval.orchestrate import retrieve_plan

    seen: dict[tuple[str, date], Any] = {}
    for c, s in retrieve_plan(ecfg, configs).items():
        del c
        for it in data.select(s):
            seen.setdefault((it.question, it.as_of), it)
    return list(seen.values())


def cmd_analyze_only(root: Path, ecfg: EvalConfig, args: argparse.Namespace) -> int:
    from scripts._llm_local import check_local_server, resolve_model
    from trafficlaw.llm import build_client, load_llm_config
    from trafficlaw.llm.parallel import map_parallel

    llm_cfg = load_llm_config(root / "configs" / "llm.yaml")
    provider, model_id = resolve_model(llm_cfg, None, None)
    if not model_id:
        print("chưa chốt model_id (configs/llm.yaml main)", file=sys.stderr)
        return 1
    meta = check_local_server(llm_cfg, provider, model_id, root)
    if meta is None:
        return 1
    client = build_client(llm_cfg, provider, model_id=model_id, root=root)
    rcfg, rctx = retrieval_env(root, args, llm=client, strict=False)
    if not rcfg.analyze.llm_fallback:
        print("analyze.llm_fallback = false — không có gì để chạy")
        return 0
    data = load_data(root, ecfg, rctx.store)
    qs = test_questions(data, ecfg, args.configs)
    t0 = time.perf_counter()
    statuses: dict[str, int] = {}
    for _, res in map_parallel(
        qs, lambda it: rctx.analyzer.analyze(it.question, it.as_of), args.workers
    ):
        if isinstance(res, Exception):
            print(f"dừng: {res}", file=sys.stderr)
            return 3
        k = res.llm_status or "rule_chac"
        statuses[k] = statuses.get(k, 0) + 1
    rec = {
        "stage": "analyze",
        "model_id": model_id,
        "serve": meta,
        "n_questions": len(qs),
        "statuses": statuses,
        "wall_s": round(time.perf_counter() - t0, 1),
    }
    log_run(ecfg.run_dir(root, args.run_id), rec)
    print(json.dumps(rec, ensure_ascii=False))
    return 0 if statuses.get("error", 0) == 0 else 1


def cmd_retrieve_dry_run(root: Path, ecfg: EvalConfig, args: argparse.Namespace) -> int:
    """Như ``scripts.retrieve --dry-run`` nhưng trên câu test theo ma trận."""
    from scripts.retrieve import llm_main_model
    from trafficlaw.llm.prompt_loader import load_prompt
    from trafficlaw.llm.serve import gpu_hours, load_serve_config
    from trafficlaw.retrieval.analyze import analyze_rule, render_llm_messages
    from trafficlaw.retrieval.rerank import make_counter, pair_key, pair_windows
    from trafficlaw.retrieval.retrieve_env import build_analyzer, build_context

    scfg = load_serve_config(root / "configs" / "serve.yaml")
    price = scfg.remote.price_vnd_per_hour
    rcfg = load_retrieval_config(root / "configs" / "retrieval.yaml")
    an = build_analyzer(
        root, rcfg, today=args.today, llm_model_id=llm_main_model(root), strict=False
    )
    dry = rcfg.model_copy(deep=True)
    for sc in dry.configs.values():
        sc.reranker = False
    ctx = build_context(root, dry, an, gpu=False)
    data = load_data(root, ecfg, ctx.store)
    from trafficlaw.eval.orchestrate import retrieve_plan

    plan = retrieve_plan(ecfg, args.configs)
    allq = test_questions(data, ecfg, args.configs)
    tables = an.tables
    prompt = load_prompt(rcfg.analyze.prompt)
    unc = [q for q in allq if analyze_rule(q.question, q.as_of, tables, today=args.today).uncertain]
    llm_in = int(
        sum(
            len(render_llm_messages(prompt, q.question, q.as_of, tables)[0]["content"]) for q in unc
        )
        / 4
        * 2.3
    )
    llm_out = 80 * len(unc)
    h_llm, _ = gpu_hours(scfg, llm_main_model(root), llm_in, llm_out)
    print(
        f"{len(allq)} câu test (ma trận {plan}) · rule không chắc {len(unc)}"
        f" ({100 * len(unc) / max(1, len(allq)):.1f}%)"
        + f" → LLM ~{llm_in:,} token vào / ~{llm_out:,} ra ≈ {h_llm * 60:.1f} phút GPU"
    )
    missing_q = (
        len(ctx.encoder.missing(rcfg.model_key, [q.question for q in allq]))
        if rcfg.model_key
        else 0
    )
    print(f"vector câu hỏi thiếu trong cache ({rcfg.model_key}): {missing_q}")
    if missing_q:
        # chưa encode câu test ⇒ đếm cặp rerank trên pool BM25 + đồ thị (ước, cùng cỡ pool)
        for sc in dry.configs.values():
            sc.dense = False if sc.bm25 else sc.dense
        print("(đếm cặp rerank với pool không dense — số ước lượng)")
    tot_h = h_llm + 5 / 60
    rr_key = rcfg.reranker_key
    if rr_key:
        spec = rcfg.reranker(rr_key)
        try:
            counter = make_counter(spec)
        except ImportError:
            print(
                "cần nhóm tok: uv run --group tok python -m scripts.eval retrieve --dry-run",
                file=sys.stderr,
            )
            return 1
        cache = ctx.rerank_cache(rr_key)
        pairs: dict[str, tuple[str, str, str]] = {}
        per_cfg: dict[str, int] = {}
        for name, set_name in plan.items():
            sc = rcfg.system(name)
            if not sc.reranker or rcfg.reranker_key_for(sc) != rr_key:
                continue
            n0 = len(pairs)
            for q in data.select(set_name):
                r = ctx.retrieve(q.question, q.as_of, name, qid=q.qid, use_llm=True)
                for p in r.pool:
                    text = ctx.catalog.get(p.chunk_id).text
                    k = pair_key(rr_key, spec, q.question, text)
                    if cache.get(k) is None:
                        pairs.setdefault(k, (q.question, p.chunk_id, text))
            per_cfg[name] = len(pairs) - n0
        n_win = 0
        for question, cid, text in pairs.values():
            n_win += len(pair_windows(cid, question, text, counter.count_tokens, spec.max_length))
        h_rr = n_win / spec.pairs_per_s / 3600 + spec.load_min / 60
        tot_h += h_rr
        print(
            f"rerank {rr_key}: {len(pairs):,} cặp mới ({per_cfg}) · {n_win:,} cửa sổ ·"
            f" ~{h_rr * 60:.1f} phút GPU"
        )
    print(f"Tổng ~{tot_h:.2f} giờ GPU ≈ {round(tot_h * price):,} VND (chưa gồm setup, tải model)")
    return 0


# --------------------------------------------------------------------------- generate


def answer_env(root: Path, args: argparse.Namespace, *, need_server: bool):
    from scripts.answer import _env_key, build_actx, llm_setup

    _env_key()
    acfg = load_answer_config(root / "configs" / "answer.yaml")
    a2 = argparse.Namespace(
        model=None,
        cache_only=args.cache_only,
        today=args.today,
        no_llm_analyzer=True,
        gpu=False,
        run_id=args.run_id_resolved,
        profile="default",
    )
    client, model_id, serve = llm_setup(root, a2, need_server=need_server)
    actx = build_actx(root, acfg, a2, client=client, model_id=model_id, serve=serve)
    return acfg, actx, serve


def cmd_generate(root: Path, ecfg: EvalConfig, args: argparse.Namespace) -> int:
    from trafficlaw.eval.orchestrate import stage_generate

    _, actx, serve = answer_env(root, args, need_server=True)
    data = load_data(root, ecfg, actx.store)
    run_dir = ecfg.run_dir(root, args.run_id)
    t0 = time.perf_counter()
    try:
        stats = stage_generate(
            data,
            ecfg,
            actx,
            run_dir,
            configs=args.configs,
            variance=not args.no_variance,
            workers=args.workers,
            limit=args.limit,
            progress=_progress,
        )
    except FileNotFoundError as e:
        print(str(e), file=sys.stderr)
        return 2
    wall = time.perf_counter() - t0
    log_run(
        run_dir,
        {
            "stage": "generate",
            "model_id": actx.model_id,
            "serve": serve,
            "cache_only": bool(args.cache_only),
            "workers": args.workers,
            "stats": {
                t: {
                    "n_total": s.n_total,
                    "n_skipped": s.n_skipped,
                    "n_written": s.n_written,
                    "statuses": dict(s.statuses),
                }
                for t, s in stats.items()
            },
            "wall_s": round(wall, 1),
        },
    )
    code = 0
    for t, s in stats.items():
        print(
            f"generate {t}: ghi {s.n_written}, bỏ qua {s.n_skipped}/{s.n_total} {dict(s.statuses)}"
        )
        if s.stopped:
            print(f"dừng: {s.stopped}", file=sys.stderr)
            return 3
        if s.statuses.get("error"):
            code = 1
    return code


def _token_counter(root: Path, model_id: str, fallback_cpt: float):
    from trafficlaw.llm.serve import load_serve_config

    hit = load_serve_config(root / "configs" / "serve.yaml").by_served_name(model_id)
    try:
        from tokenizers import Tokenizer

        if hit:
            tok = Tokenizer.from_pretrained(hit[1].hf_repo, revision=hit[1].revision or "main")
            tok.no_truncation()
            return (lambda s: len(tok.encode(s).ids)), "tokenizer"
    except ImportError:
        print("(không có nhóm tok → ước token = len/1,74)", file=sys.stderr)
    return (lambda s: int(len(s) / fallback_cpt)), "len/1,74"


def cmd_generate_dry_run(root: Path, ecfg: EvalConfig, args: argparse.Namespace) -> int:
    """Prompt thật cho câu chưa xong. Thiếu kết quả truy hồi (chưa chạy pha GPU) ⇒ dựng nguồn từ
    truy hồi **không rerank** (cùng số nguồn, chỉ khác thứ tự) — ước token, không phải số cuối."""
    from trafficlaw.eval.orchestrate import generate_jobs
    from trafficlaw.llm.serve import gpu_hours, load_serve_config
    from trafficlaw.pipeline.answer import prepare
    from trafficlaw.pipeline.runner import done_answer_keys, latest_results
    from trafficlaw.retrieval.retrieve_env import build_analyzer, build_context

    acfg, actx, _ = answer_env(root, args, need_server=False)
    scfg = load_serve_config(root / "configs" / "serve.yaml")
    count, how = _token_counter(root, actx.model_id, acfg.context.chars_per_token)
    rcfg = load_retrieval_config(root / "configs" / "retrieval.yaml")
    dry = rcfg.model_copy(deep=True)
    for sc in dry.configs.values():
        sc.reranker = False
    an = build_analyzer(root, rcfg, today=args.today, llm_model_id=actx.model_id, strict=False)
    dctx = build_context(root, dry, an, gpu=False)
    data = load_data(root, ecfg, actx.store)
    run_dir = ecfg.run_dir(root, args.run_id)
    tot_in = tot_out = n_calls = 0
    approx = False
    for cfg, set_name, seed in generate_jobs(ecfg, args.configs, variance=not args.no_variance):
        items = data.select(set_name)[: args.limit] if args.limit else data.select(set_name)
        out = answers_path(run_dir, cfg, seed)
        ph = actx.prompt_hash(cfg)
        done = done_answer_keys(out)
        todo = [it for it in items if (cfg, it.qid, actx.model_id, ph) not in done]
        rp = retrieve_path(run_dir, cfg)
        rets = (
            load_retrievals(rp, actx.retrieval.meta)
            if rp.is_file() and not actx.is_no_rag(cfg)
            else {}
        )
        outs = [
            r["usage"]["completion_tokens"]
            for r in latest_results(out).values()
            if r.get("status") == "ok" and not r["usage"].get("estimated")
        ]
        per_out = statistics.fmean(outs) if outs else ecfg.output_tokens_estimate
        toks = []
        for it in todo:
            r = rets.get(it.qid)
            if r is None and not actx.is_no_rag(cfg):
                approx = True
                try:
                    r = dctx.retrieve(it.question, it.as_of, cfg, qid=it.qid, use_llm=True)
                except MissingVectorsError:
                    sc = dry.configs[cfg]
                    sc.dense = not sc.bm25  # B2 (chỉ dense) không ước được ⇒ giữ, sẽ lỗi lần nữa
                    if not sc.bm25:
                        sc.dense, sc.bm25 = False, True
                    r = dctx.retrieve(it.question, it.as_of, cfg, qid=it.qid, use_llm=True)
            p = prepare(it.question, it.as_of, cfg, actx, qid=it.qid, retrieval=r)
            toks.append(count(p.messages[0]["content"]) + 12)
        t_in, t_out = sum(toks), int(per_out * len(todo))
        tot_in, tot_out, n_calls = tot_in + t_in, tot_out + t_out, n_calls + len(todo)
        tag = cfg if seed is None else f"{cfg}_seed{seed}"
        print(
            f"{tag} × {set_name}: {len(todo)}/{len(items)} câu cần gọi · vào {t_in:,}"
            f" (TB {t_in / max(1, len(todo)):.0f}) · ra ~{t_out:,} ({per_out:.0f}/câu)"
        )
    h, vnd = gpu_hours(scfg, actx.model_id, tot_in, int(tot_out * 1.1))
    print(
        f"Tổng {n_calls:,} lượt (+~10% sửa số) · {tot_in:,} token vào ({how}) / ~{tot_out:,} ra"
        f" ≈ {h:.2f} giờ GPU ≈ {vnd:,} VND (chưa gồm khởi động vLLM; lượt dao động không cache)"
        + (" · nguồn ước từ truy hồi không rerank" if approx else "")
    )
    return 0


# --------------------------------------------------------------------------- score / judge


def judge_env(root: Path, ecfg: EvalConfig, args: argparse.Namespace, *, need_server: bool):
    from scripts._llm_local import check_local_server, family_of
    from trafficlaw.eval.judge import JudgeContext, check_judge_model
    from trafficlaw.llm import build_client, load_llm_config
    from trafficlaw.llm.prompt_loader import load_prompt

    llm_cfg = load_llm_config(root / "configs" / "llm.yaml")
    main = llm_cfg.main.model_id or ""
    jm = ecfg.judge.model_id
    fam = check_judge_model(jm, main, lambda m: family_of(m, root))
    client = serve = None
    if need_server:
        from scripts.answer import _env_key

        _env_key()
        serve = check_local_server(llm_cfg, llm_cfg.main.provider, jm, root)
        if serve is None:
            raise SystemExit(1)
        client = build_client(llm_cfg, llm_cfg.main.provider, model_id=jm, root=root)
    jctx = JudgeContext(
        client=client,
        prompt=load_prompt(ecfg.judge.prompt),
        model_id=jm,
        run_id=args.run_id_resolved,
        serve=serve,
        git_commit=git_commit(root),
        max_output_tokens=ecfg.judge.max_output_tokens,
    )
    return jctx, fam


def limitations(data: EvalData) -> list[str]:
    if not any("+" in it.source for it in data.items):
        return []  # không phải test (vd chạy thử trên val)
    kinds: dict[str, int] = {}
    for it in data.items:
        kinds[it.source_kind] = kinds.get(it.source_kind, 0) + 1
    return [
        "Không câu test nào do người viết hay sửa: "
        + ", ".join(f"{v} câu `+{k}`" for k, v in sorted(kinds.items()))
        + " (`+reviewed` = gpt-oss-20b viết, Claude rà đạt; `+claude` = Claude sửa từ nháp không"
        " đạt). Kết quả rà và câu sửa được người dùng xác nhận tổng thể 17/11/2026; đáp án tham"
        " chiếu có thể sai ở chỗ Claude đọc nhầm nguồn.",
        "Judge chấm theo đáp án tham chiếu đó; độ đúng của judge kiểm bằng 40 câu Claude chấm độc"
        " lập (người dùng xác nhận) — Claude cũng là người sửa 160 đáp án `+claude`.",
        "Một LLM sinh (qwen3-14b-awq) cho mọi cấu hình ⇒ so sánh giữa cấu hình hợp lệ, số tuyệt đối"
        " phản ánh model mở ~14B.",
    ]


def cmd_score(root: Path, ecfg: EvalConfig, args: argparse.Namespace) -> int:
    from trafficlaw.eval.orchestrate import score_all, stage_judge

    rcfg, rctx = retrieval_env(root, args)
    data = load_data(root, ecfg, rctx.store)
    run_dir = ecfg.run_dir(root, args.run_id)
    jctx = fam = None
    if not args.no_judge:
        jctx, fam = judge_env(root, ecfg, args, need_server=args.judge)
    if args.judge:
        assert jctx is not None
        t0 = time.perf_counter()
        st = stage_judge(
            data,
            ecfg,
            jctx,
            run_dir,
            configs=args.configs,
            workers=args.workers,
            progress=_progress,
        )
        log_run(
            run_dir,
            {
                "stage": "judge",
                "model_id": jctx.model_id,
                "serve": jctx.serve,
                "prompt_hash": jctx.prompt_hash,
                "stats": {
                    c: {
                        "n_total": s.n_total,
                        "n_skipped": s.n_skipped,
                        "n_written": s.n_written,
                        "statuses": dict(s.statuses),
                    }
                    for c, s in st.items()
                },
                "wall_s": round(time.perf_counter() - t0, 1),
            },
        )
        for c, s in st.items():
            print(
                f"judge {c}: ghi {s.n_written}, bỏ qua {s.n_skipped}/{s.n_total} {dict(s.statuses)}"
            )
            if s.stopped:
                return 3
    del rcfg
    s = score_all(
        data,
        ecfg,
        rctx.catalog,
        run_dir,
        rctx.meta,
        judge_model=jctx.model_id if jctx else None,
        judge_prompt_hash=jctx.prompt_hash if jctx else None,
        judge_family=fam,
        extra={"git_commit": git_commit(root), "limitations": limitations(data)},
    )
    print(f"→ {run_dir / 'summary.md'} ({len(s['configs'])} cấu hình)")
    return 0


def cmd_judge_dry_run(root: Path, ecfg: EvalConfig, args: argparse.Namespace) -> int:
    from trafficlaw.eval.judge import judge_messages, rule_verdict
    from trafficlaw.eval.orchestrate import current_judgements, judge_items
    from trafficlaw.eval.runner import load_answers
    from trafficlaw.llm.serve import gpu_hours, load_serve_config
    from trafficlaw.pipeline.runner import DONE_STATUSES

    rcfg, rctx = retrieval_env(root, args)
    del rcfg
    data = load_data(root, ecfg, rctx.store)
    jctx, _ = judge_env(root, ecfg, args, need_server=False)
    scfg = load_serve_config(root / "configs" / "serve.yaml")
    count, how = _token_counter(root, jctx.model_id, 1.74)
    run_dir = ecfg.run_dir(root, args.run_id)
    items = judge_items(data, ecfg)
    tot_in = n = n_rule = n_missing = 0
    for cfg in ecfg.judge.configs:
        p = answers_path(run_dir, cfg)
        ans = load_answers(p) if p.is_file() else {}
        have = current_judgements(
            run_dir / f"judge_{cfg}.jsonl", jctx.model_id, jctx.prompt_hash, ans
        )
        for it in items:
            a = ans.get(it.qid)
            if a is None or a.status not in DONE_STATUSES:
                n_missing += 1
                # chưa có câu trả lời: ước prompt với câu trả lời ~900 ký tự (M12: G val TB)
                tot_in += count(
                    jctx.prompt.render(
                        as_of="",
                        question=it.question,
                        reference=it.answer or "",
                        answer_status="",
                        answer="x" * 900,
                    )
                )
                n += 1
                continue
            if it.qid in have:
                continue
            if rule_verdict(it, a) is not None:
                n_rule += 1
                continue
            tot_in += count(judge_messages(jctx.prompt, it, a)[0]["content"])
            n += 1
    out = n * ecfg.judge.output_tokens_estimate
    h, vnd = gpu_hours(scfg, jctx.model_id, tot_in, out)
    print(
        f"judge {jctx.model_id}: {n} lượt LLM ({n_missing} chưa có câu trả lời, ước) + {n_rule}"
        " chấm"
        f" luật · {tot_in:,} token vào ({how}) / ~{out:,} ra ≈ {h:.2f} giờ GPU ≈ {vnd:,} VND"
        " (chưa gồm khởi động vLLM / tải model)"
    )
    return 0


def cmd_judge_check(root: Path, ecfg: EvalConfig, args: argparse.Namespace) -> int:
    from trafficlaw.eval.orchestrate import export_judge_check

    _, rctx = retrieval_env(root, args)
    data = load_data(root, ecfg, rctx.store)
    p = export_judge_check(data, ecfg, ecfg.run_dir(root, args.run_id))
    print(f"→ {p} + judge_check_labels.jsonl (Claude chấm, người dùng xác nhận)")
    return 0


# --------------------------------------------------------------------------- regression, smoke


def cmd_regression(root: Path, ecfg: EvalConfig, args: argparse.Namespace) -> int:
    """Recall@k G trên ``regression_100`` (truy hồi đầy đủ từ cache vector/rerank, không GPU)."""
    from trafficlaw.eval.answer_metrics import retrieval_scores
    from trafficlaw.eval.qa_subsets import file_sha256

    rg = ecfg.regression
    _, rctx = retrieval_env(root, args)
    data = load_data(root, ecfg, rctx.store)
    items = data.select(rg.subset)
    try:
        vals = [
            retrieval_scores(
                it, rctx.retrieve(it.question, it.as_of, rg.config, qid=it.qid), rctx.catalog
            )[f"r@{rg.k}"]
            for it in items
            if it.gold_units
        ]
    except MISSING as e:
        print(f"thiếu cache: {e}", file=sys.stderr)
        return 2
    rec = sum(v or 0 for v in vals) / len(vals)
    path = root / rg.baseline
    cur = {
        "config": rg.config,
        "subset": rg.subset,
        "k": rg.k,
        f"recall@{rg.k}": rec,
        "n": len(vals),
        "test_sha256": file_sha256(root / ecfg.test),
        **rctx.meta,
        "git_commit": git_commit(root),
        "created_at": now_iso(),
    }
    print(f"{rg.config} Recall@{rg.k} trên {rg.subset} ({len(vals)} câu): {100 * rec:.2f}%")
    if args.write_baseline:
        path.write_text(json.dumps(cur, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"→ {path}")
        return 0
    if not path.is_file():
        print(f"chưa có baseline {path} (--write-baseline)", file=sys.stderr)
        return 1
    base = json.loads(path.read_text(encoding="utf-8"))
    b = float(base[f"recall@{rg.k}"])
    drop = b - rec
    print(f"baseline {100 * b:.2f}% → hiện tại {100 * rec:.2f}% (giảm {100 * drop:.2f} điểm %)")
    return 1 if drop > rg.max_drop + 1e-12 else 0


def cmd_smoke(root: Path, ecfg: EvalConfig, args: argparse.Namespace) -> int:
    from trafficlaw.eval.smoke import run_smoke

    if not args.fake:
        print("smoke chỉ có chế độ --fake (model giả, không GPU)", file=sys.stderr)
        return 1
    s = run_smoke(
        root,
        ecfg,
        load_retrieval_config(root / "configs" / "retrieval.yaml"),
        load_answer_config(root / "configs" / "answer.yaml"),
        out_dir=Path(args.out) if args.out else None,
    )
    calls = s["smoke_llm_calls"]
    print(
        f"smoke: {len(s['configs'])} cấu hình · {s['smoke_seconds']} s · lượt LLM {calls}"
        f" → {s['run_dir']}"
    )
    for c, d in s["configs"].items():
        print(f"  {c}: {d['n_done']}/{d['n_total']} {d['statuses']}")
    if calls[0] == 0 or calls[1] != calls[0]:
        print("smoke lỗi: lần chạy thứ hai phải không gọi LLM (resume)", file=sys.stderr)
        return 1
    if any(d["n_done"] != d["n_total"] for d in s["configs"].values() if d["n_total"]):
        print("smoke lỗi: còn câu chưa xong", file=sys.stderr)
        return 1
    if s["smoke_seconds"] > 60:
        print("smoke lỗi: quá 60 s", file=sys.stderr)
        return 1
    return 0


# --------------------------------------------------------------------------- main


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "command", choices=["retrieve", "generate", "score", "judge-check", "regression", "smoke"]
    )
    ap.add_argument("--config", type=Path, default=REPO_ROOT / "configs" / "eval.yaml")
    ap.add_argument("--run-id")
    ap.add_argument("--configs", type=lambda s: [x for x in s.split(",") if x], default=None)
    ap.add_argument("--limit", type=int, default=None, help="chỉ N câu đầu mỗi tập (chạy thử)")
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--analyze-only", action="store_true")
    ap.add_argument(
        "--gpu", action="store_true", help="nạp embedder/reranker khi thiếu cache (máy thuê)"
    )
    ap.add_argument("--no-llm", action="store_true", help="tắt LLM dự phòng của analyzer")
    ap.add_argument("--cache-only", action="store_true", help="generate: chỉ đọc cache LLM")
    ap.add_argument("--no-variance", action="store_true")
    ap.add_argument("--judge", action="store_true", help="score: gọi judge (cần server judge)")
    ap.add_argument("--no-judge", action="store_true", help="score: bỏ hẳn chỉ số judge")
    ap.add_argument("--write-baseline", action="store_true")
    ap.add_argument("--fake", action="store_true")
    ap.add_argument("--out", help="smoke: thư mục kết quả (mặc định thư mục tạm)")
    args = ap.parse_args(argv)
    setup_logging()
    load_dotenv(REPO_ROOT / ".env")
    root = REPO_ROOT
    ecfg = load_eval_config(args.config)
    set_seed(ecfg.seed)
    args.today = ecfg.today
    args.run_id_resolved = args.run_id or ecfg.run_id
    try:
        if args.command == "smoke":
            return cmd_smoke(root, ecfg, args)
        if args.command == "retrieve":
            if args.dry_run:
                return cmd_retrieve_dry_run(root, ecfg, args)
            if args.analyze_only:
                return cmd_analyze_only(root, ecfg, args)
            return cmd_retrieve(root, ecfg, args)
        if args.command == "generate":
            return (
                cmd_generate_dry_run(root, ecfg, args)
                if args.dry_run
                else cmd_generate(root, ecfg, args)
            )
        if args.command == "score":
            if args.dry_run:
                return cmd_judge_dry_run(root, ecfg, args)
            return cmd_score(root, ecfg, args)
        if args.command == "judge-check":
            return cmd_judge_check(root, ecfg, args)
        return cmd_regression(root, ecfg, args)
    except (StaleSubsetsError, StaleResultError) as e:
        print(str(e), file=sys.stderr)
        return 4


if __name__ == "__main__":
    raise SystemExit(main())
