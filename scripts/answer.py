"""M12: sinh câu trả lời + verify — một câu hỏi, chạy thử trên val / dev ngoài phạm vi, dry-run.

    uv run python -m scripts.answer --question "…" [--as-of D] [--config G] [--json]
    uv run --no-sync python -m scripts.answer --question "…" --gpu --profile shared   # máy thuê
    uv run --group tok python -m scripts.answer --dry-run [--eval val,dev_oos] [--configs G,B3,B0]
    uv run python -m scripts.answer --eval val,dev_oos --configs G,B3,B0 [--n 200] [--workers 16]
    uv run --no-sync python -m scripts.answer --retrieve-only --eval dev_oos --configs G,B3 --gpu
    uv run python -m scripts.answer --calibrate-tau     # τ từ điểm rerank top-1 (val vs dev_oos)
    uv run python -m scripts.answer --summarize | --review   # chỉ số / phiếu rà tay, không gọi LLM

**Không dùng ``data/qa/test.jsonl``** (mục 10). Tập: ``val`` (câu sinh từ một chunk, không có đáp án
vàng) và ``dev_oos`` (câu ngoài phạm vi do Claude viết, chỉ để hiệu chỉnh τ).

Truy hồi lấy từ ``data/answer/retrieval/<tập>/<cấu hình>.jsonl`` hoặc cache M11
``data/index/retrieval_eval/<tập>/<cấu hình>.jsonl`` (``RetrievalResult``; phải cùng
``data_version``/``catalog_sha256``); không có → chạy ``retrieve()`` (đọc cache vector/rerank).
Pha sinh chỉ cần vLLM ``qwen3-14b-awq`` qua ``tunnel.sh``. Kết quả: ``results/<run_id>/
answers_<tập>_<cấu hình>.jsonl`` (resume theo ``(config_name, qid, model_id, prompt_hash)``),
tổng hợp ``data/answer/dev_eval.{json,md}``.

Mã thoát: 1 = lỗi; 2 = thiếu cache (vector / điểm rerank / LLM analyzer); 3 = dừng (quota).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import statistics
import subprocess
import sys
import threading
import time
from collections import Counter
from collections.abc import Sequence
from datetime import date
from pathlib import Path
from typing import Any

from trafficlaw.eval.qa_schema import QAItem
from trafficlaw.eval.retrieval_eval import stratified_sample, to_queries
from trafficlaw.pipeline.answer import (
    AnswerConfig,
    AnswerContext,
    AnswerResult,
    answer,
    load_answer_config,
    prepare,
)
from trafficlaw.pipeline.runner import Query, latest_results, run_answers
from trafficlaw.retrieval.analyze import MissingLLMAnalysisError
from trafficlaw.retrieval.catalog import is_same_or_related
from trafficlaw.retrieval.config import load_retrieval_config
from trafficlaw.retrieval.index_pipeline import MissingVectorsError, now_iso
from trafficlaw.retrieval.rerank import MissingRerankScoresError
from trafficlaw.retrieval.retrieve import RetrievalResult
from trafficlaw.retrieval.retrieve_env import build_analyzer, build_context
from trafficlaw.utils.env import load_dotenv
from trafficlaw.utils.git import git_commit
from trafficlaw.utils.jsonl import append_jsonl, read_jsonl, write_jsonl
from trafficlaw.utils.logging import setup_logging
from trafficlaw.utils.seed import set_seed

REPO_ROOT = Path(__file__).resolve().parents[1]
logger = logging.getLogger("answer")
MISSING = (MissingVectorsError, MissingRerankScoresError, MissingLLMAnalysisError)
SETS = ("val", "dev_oos")


# --------------------------------------------------------------------------- nạp


def _env_key() -> None:
    """Máy thuê chỉ có ``VLLM_API_KEY`` (file env của ``gpu.sh``) — dùng làm khoá provider local."""
    if not os.environ.get("LOCAL_LLM_API_KEY") and os.environ.get("VLLM_API_KEY"):
        os.environ["LOCAL_LLM_API_KEY"] = os.environ["VLLM_API_KEY"]


def llm_setup(root: Path, args: argparse.Namespace, *, need_server: bool) -> tuple[Any, str, Any]:
    """(client | None, model_id, serve meta | None)."""
    from scripts._llm_local import check_local_server, resolve_model
    from trafficlaw.llm import build_client, load_llm_config

    llm_cfg = load_llm_config(root / "configs" / "llm.yaml")
    provider, model_id = resolve_model(llm_cfg, None, args.model)
    if not model_id:
        raise SystemExit("chưa chốt model_id (configs/llm.yaml main)")
    if not need_server:
        return None, model_id, None
    meta = check_local_server(llm_cfg, provider, model_id, root)
    if meta is None:
        raise SystemExit(1)
    return build_client(llm_cfg, provider, model_id=model_id, root=root), model_id, meta


def build_actx(
    root: Path,
    acfg: AnswerConfig,
    args: argparse.Namespace,
    *,
    client: Any,
    model_id: str,
    serve: dict[str, Any] | None,
    analyzer_llm: Any = None,
) -> AnswerContext:
    rcfg = load_retrieval_config(root / "configs" / "retrieval.yaml")
    an = build_analyzer(
        root,
        rcfg,
        today=args.today,
        llm=analyzer_llm,
        llm_model_id=model_id,
        strict=analyzer_llm is None and not args.no_llm_analyzer,
    )
    rctx = build_context(root, rcfg, an, gpu=args.gpu)
    return AnswerContext(
        acfg,
        store=rctx.store,
        catalog=rctx.catalog,
        retrieval=rctx,
        client=client,
        model_id=model_id,
        today=args.today,
        run_id=args.run_id or acfg.eval.run_id,
        git_commit=git_commit(root),
        data_version=rctx.meta.get("data_version"),
        serve=serve,
        budget_profile=args.profile,
    )


def load_items(root: Path, acfg: AnswerConfig, name: str) -> list[QAItem]:
    path = root / (acfg.eval.val if name == "val" else acfg.eval.dev_out_of_scope)
    if name not in SETS:
        raise SystemExit(f"tập {name!r} không có (có: {', '.join(SETS)}); test không được dùng")
    if not path.is_file():
        raise SystemExit(f"thiếu {path}")
    return [QAItem.model_validate(r) for r in read_jsonl(path)]


def select_items(items: list[QAItem], n: int | None, seed: int) -> list[QAItem]:
    if not n or n >= len(items):
        return items
    qs = stratified_sample(to_queries(items), n, seed=seed, name="m12_answer")
    keep = {q.qid for q in qs}
    return [it for it in items if it.qid in keep]


def retrieval_paths(root: Path, acfg: AnswerConfig, set_name: str, cfg: str) -> list[Path]:
    return [
        root / acfg.eval.out_dir / "retrieval" / set_name / f"{cfg}.jsonl",
        root / acfg.eval.retrieval_from / set_name / f"{cfg}.jsonl",
    ]


def load_retrievals(
    root: Path, acfg: AnswerConfig, set_name: str, cfg: str, meta: dict[str, Any]
) -> dict[str, RetrievalResult]:
    for p in retrieval_paths(root, acfg, set_name, cfg):
        if not p.is_file():
            continue
        out: dict[str, RetrievalResult] = {}
        for r in read_jsonl(p):
            rr = RetrievalResult.model_validate(r)
            for k in ("data_version", "catalog_sha256", "graph_data_hash"):
                if getattr(rr, k) != meta.get(k):
                    raise SystemExit(
                        f"{p}: {k} lệch dữ liệu hiện hành — chạy lại truy hồi (M11) trước"
                    )
            out[str(rr.qid)] = rr
        logger.info("truy hồi %s/%s: %d câu từ %s", set_name, cfg, len(out), p)
        return out
    return {}


def results_path(root: Path, acfg: AnswerConfig, run_id: str, set_name: str, cfg: str) -> Path:
    return root / acfg.eval.results_dir / run_id / f"answers_{set_name}_{cfg}.jsonl"


def _queries(items: Sequence[QAItem]) -> list[Query]:
    return [Query(it.qid, it.question, it.as_of) for it in items]


# --------------------------------------------------------------------------- một câu hỏi


class VramSampler:
    """Lấy mẫu ``nvidia-smi`` (bộ nhớ đã dùng toàn GPU, gồm vLLM) mỗi 0,2 giây."""

    def __init__(self) -> None:
        self.peak_mib = 0
        self.total_mib = 0
        self._stop = threading.Event()
        self._t = threading.Thread(target=self._run, daemon=True)

    def _q(self) -> tuple[int, int] | None:
        try:
            out = subprocess.run(
                [
                    "nvidia-smi",
                    "--query-gpu=memory.used,memory.total",
                    "--format=csv,noheader,nounits",
                ],
                capture_output=True,
                text=True,
                timeout=5,
                check=True,
            ).stdout.strip()
            used, total = (int(x) for x in out.splitlines()[0].split(","))
            return used, total
        except (OSError, subprocess.SubprocessError, ValueError):
            return None

    def _run(self) -> None:
        while not self._stop.is_set():
            got = self._q()
            if got:
                self.peak_mib = max(self.peak_mib, got[0])
                self.total_mib = got[1]
            time.sleep(0.2)

    def __enter__(self) -> VramSampler:
        self._t.start()
        return self

    def __exit__(self, *exc: object) -> None:
        self._stop.set()
        self._t.join(timeout=2)


def cmd_question(root: Path, acfg: AnswerConfig, args: argparse.Namespace) -> int:
    client, model_id, serve = llm_setup(root, args, need_server=True)
    actx = build_actx(
        root, acfg, args, client=client, model_id=model_id, serve=serve, analyzer_llm=client
    )
    as_of = date.fromisoformat(args.as_of) if args.as_of else None
    t0 = time.perf_counter()
    with VramSampler() as vs:
        try:
            res = answer(args.question, as_of, args.config, actx)
        except MISSING as e:
            print(f"thiếu cache: {e}", file=sys.stderr)
            return 2
    wall = time.perf_counter() - t0
    if args.gpu:
        rec: dict[str, Any] = {
            "profile": args.profile,
            "config": args.config,
            "serve": serve,
            "nvidia_smi_peak_mib": vs.peak_mib,
            "nvidia_smi_total_mib": vs.total_mib,
            "wall_s": round(wall, 2),
            "git_commit": git_commit(root),
            "finished_at": now_iso(),
        }
        try:
            import torch

            if torch.cuda.is_available():
                rec["torch_max_allocated_gib"] = round(torch.cuda.max_memory_allocated() / 2**30, 3)
                rec["gpu"] = torch.cuda.get_device_name(0)
        except ImportError:  # pragma: no cover
            pass
        append_jsonl(root / acfg.eval.out_dir / "vram.jsonl", rec)
        print(json.dumps(rec, ensure_ascii=False))
    if args.json:
        print(json.dumps(res.model_dump(mode="json"), ensure_ascii=False, indent=2))
        return 0
    print(f"[{res.config_name}] as_of {res.as_of} · {res.status} / {res.answer_status}")
    for s in res.sources:
        print(f"  {s.sid} {s.origin:5} {s.chunk_id}  ({s.label}, {s.doc_label})")
    print(res.answer)
    print("verify:", res.verify.flags, f"repaired={res.verify.repaired}")
    return 0 if res.status == "ok" else 1


# --------------------------------------------------------------------------- truy hồi riêng


def cmd_retrieve_only(root: Path, acfg: AnswerConfig, args: argparse.Namespace) -> int:
    an_llm = None
    model_id = None
    if args.analyzer_llm:
        an_llm, model_id, _ = llm_setup(root, args, need_server=True)
    else:
        _, model_id, _ = llm_setup(root, args, need_server=False)
    actx = build_actx(
        root, acfg, args, client=None, model_id=model_id, serve=None, analyzer_llm=an_llm
    )
    assert actx.retrieval is not None
    for set_name in args.sets:
        items = select_items(load_items(root, acfg, set_name), args.n, acfg.eval.seed)
        for cfg in args.configs:
            if actx.is_no_rag(cfg):
                continue
            rows = []
            try:
                for it in items:
                    rows.append(actx.retrieval.retrieve(it.question, it.as_of, cfg, qid=it.qid))
            except MISSING as e:
                print(f"[{set_name}] {cfg}: thiếu cache — {e}", file=sys.stderr)
                return 2
            p = retrieval_paths(root, acfg, set_name, cfg)[0]
            write_jsonl(p, rows)
            print(f"[{set_name}] {cfg}: {len(rows)} câu → {p}")
    return 0


# --------------------------------------------------------------------------- chạy thử


def cmd_eval(root: Path, acfg: AnswerConfig, args: argparse.Namespace) -> int:
    client, model_id, serve = llm_setup(root, args, need_server=True)
    actx = build_actx(root, acfg, args, client=client, model_id=model_id, serve=serve)
    assert actx.retrieval is not None
    run_id = actx.run_id
    code = 0
    for set_name in args.sets:
        items = select_items(load_items(root, acfg, set_name), args.n, acfg.eval.seed)
        for cfg in args.configs:
            rets = {}
            if not actx.is_no_rag(cfg):
                rets = load_retrievals(root, acfg, set_name, cfg, actx.retrieval.meta)
            out = results_path(root, acfg, run_id, set_name, cfg)
            t0 = time.perf_counter()
            try:
                st = run_answers(
                    _queries(items),
                    cfg,
                    actx,
                    out,
                    retrievals=rets,
                    workers=args.workers,
                    progress=lambda i, n, s=set_name, c=cfg: (
                        logger.info("[%s] %s: %d/%d", s, c, i, n) if i % 50 == 0 else None
                    ),
                )
            except MISSING as e:
                print(f"[{set_name}] {cfg}: thiếu cache — {e}", file=sys.stderr)
                return 2
            sec = round(time.perf_counter() - t0, 1)
            rec = {
                "set": set_name,
                "config": cfg,
                "run_id": run_id,
                "model_id": model_id,
                "serve": serve,
                "prompt_hash": actx.prompt_hash(cfg),
                "n_total": st.n_total,
                "n_skipped": st.n_skipped,
                "n_written": st.n_written,
                "statuses": dict(st.statuses),
                "seconds": sec,
                "workers": args.workers,
                "git_commit": git_commit(root),
                "finished_at": now_iso(),
            }
            append_jsonl(root / acfg.eval.out_dir / "runs.jsonl", rec)
            print(
                f"[{set_name}] {cfg}: ghi {st.n_written}, bỏ qua {st.n_skipped}"
                f" {dict(st.statuses)} ({sec} s)"
            )
            if st.stopped:
                print(f"dừng: {st.stopped}", file=sys.stderr)
                return 3
            if st.statuses.get("error"):
                code = 1
    cmd_summarize(root, acfg, args)
    return code


# --------------------------------------------------------------------------- dry-run


def cmd_dry_run(root: Path, acfg: AnswerConfig, args: argparse.Namespace) -> int:
    from trafficlaw.llm.serve import gpu_hours, load_serve_config
    from trafficlaw.pipeline.runner import done_answer_keys

    scfg = load_serve_config(root / "configs" / "serve.yaml")
    _, model_id, _ = llm_setup(root, args, need_server=False)
    actx = build_actx(root, acfg, args, client=None, model_id=model_id, serve=None)
    assert actx.retrieval is not None
    hit = scfg.by_served_name(model_id)
    count = None
    try:
        from tokenizers import Tokenizer

        if hit:
            tok = Tokenizer.from_pretrained(hit[1].hf_repo, revision=hit[1].revision or "main")
            tok.no_truncation()
            count = lambda s: len(tok.encode(s).ids)  # noqa: E731
    except ImportError:
        print("(không có nhóm tok → ước token = len/1,74)", file=sys.stderr)
    if count is None:
        count = lambda s: int(len(s) / acfg.context.chars_per_token)  # noqa: E731
    run_id = args.run_id or acfg.eval.run_id
    tot_in = tot_out = n_calls = 0
    for set_name in args.sets:
        items = select_items(load_items(root, acfg, set_name), args.n, acfg.eval.seed)
        for cfg in args.configs:
            rets = {}
            if not actx.is_no_rag(cfg):
                rets = load_retrievals(root, acfg, set_name, cfg, actx.retrieval.meta)
            out = results_path(root, acfg, run_id, set_name, cfg)
            done = done_answer_keys(out)
            ph = actx.prompt_hash(cfg)
            todo = [it for it in items if (cfg, it.qid, model_id, ph) not in done]
            outs = [
                r["usage"]["completion_tokens"]
                for r in latest_results(out).values()
                if r.get("status") == "ok" and not r["usage"].get("estimated")
            ]
            per_out = statistics.fmean(outs) if outs else acfg.eval.output_tokens_estimate
            toks = []
            n_src = []
            n_num = []
            try:
                for it in todo:
                    p = prepare(
                        it.question, it.as_of, cfg, actx, qid=it.qid, retrieval=rets.get(it.qid)
                    )
                    toks.append(count(p.messages[0]["content"]) + 12)
                    n_src.append(len(p.sources))
                    n_num.append(len(p.table))
            except MISSING as e:
                print(f"[{set_name}] {cfg}: thiếu cache — {e}", file=sys.stderr)
                return 2
            t_in, t_out = sum(toks), int(per_out * len(todo))
            tot_in += t_in
            tot_out += t_out
            n_calls += len(todo)
            mx = max(toks) if toks else 0
            print(
                f"[{set_name}] {cfg}: {len(todo)}/{len(items)} câu cần gọi · token vào {t_in:,}"
                f" (TB {t_in / max(1, len(todo)):.0f}, max {mx:,}) · ra ~{t_out:,}"
                f" ({per_out:.0f}/câu) · nguồn TB {statistics.fmean(n_src) if n_src else 0:.1f}"
                f" · mã số TB {statistics.fmean(n_num) if n_num else 0:.1f}"
            )
    h, vnd = gpu_hours(scfg, model_id, tot_in, int(tot_out * 1.1))
    print(
        f"Tổng {n_calls:,} lượt (+ ~10% lượt sửa số) · {tot_in:,} token vào / ~{tot_out:,} ra ≈"
        f" {h:.2f} giờ GPU ≈ {vnd:,} VND (prefix caching giảm prefill; chưa gồm khởi động vLLM)"
    )
    return 0


# --------------------------------------------------------------------------- chỉ số


def _pct(xs: Sequence[float], p: float) -> float | None:
    if not xs:
        return None
    s = sorted(xs)
    return round(s[min(len(s) - 1, int(p * len(s)))], 1)


def _rate(a: float, b: float) -> float | None:
    return round(a / b, 4) if b else None


def _related(unit: str | None, gold: Sequence[str]) -> bool:
    return bool(unit) and any(is_same_or_related(str(unit), g) for g in gold)


def summarize_rows(rows: Sequence[AnswerResult], gold: dict[str, list[str]]) -> dict[str, Any]:
    n = len(rows)
    st = Counter(r.status for r in rows)
    ok = [r for r in rows if r.status == "ok"]
    ans = Counter(r.answer_status for r in ok)
    res: dict[str, Any] = {
        "n": n,
        "status": dict(st),
        "format_error_rate": _rate(st["format_error"], st["ok"] + st["format_error"]),
        "error_rate": _rate(st["error"], n),
        "answer_status": dict(ans),
        "tu_choi": _rate(ans["insufficient"] + ans["out_of_scope"], len(ok)),
        "out_of_scope": _rate(ans["out_of_scope"], len(ok)),
    }
    with_gold = [r for r in ok if gold.get(str(r.qid))]
    if with_gold:
        cg = sum(any(_related(c.unit_id, gold[str(r.qid)]) for c in r.citations) for r in with_gold)
        ctx_g = sum(
            any(_related(s.unit_id, gold[str(r.qid)]) for s in r.sources) for r in with_gold
        )
        res["trich_gold"] = _rate(cg, len(with_gold))
        res["nguon_co_gold"] = _rate(ctx_g, len(with_gold)) if any(r.sources for r in ok) else None
    n_c = sum(r.verify.n_citations for r in ok)
    n_v = sum(r.verify.n_citations_valid for r in ok)
    res["trich_dan"] = {"n": n_c, "hop_le": _rate(n_v, n_c)}
    flags = Counter(i.code for r in ok for i in r.verify.issues)
    res["co"] = dict(flags.most_common())
    res["co_theo_cau"] = dict(Counter(f for r in ok for f in r.verify.flags).most_common())
    if ok and ok[0].verify.numbers_verifiable:
        res["con_so"] = {
            "cau_dung_ma_so": _rate(sum(1 for r in ok if r.numbers), len(ok)),
            "ma_so_dung_tb": round(statistics.fmean(len(r.numbers) for r in ok), 2),
            "cau_vi_pham_truoc_sua": _rate(
                sum(1 for r in ok if r.verify.n_violations_before), len(ok)
            ),
            "cau_vi_pham_sau_sua": _rate(
                sum(1 for r in ok if (r.verify.n_violations_after_repair or 0) > 0), len(ok)
            ),
            "vi_pham_truoc": sum(r.verify.n_violations_before for r in ok),
            "vi_pham_sau": sum(r.verify.n_violations_after_repair or 0 for r in ok),
            "luot_sua": sum(1 for r in ok if r.verify.repaired),
            "cau_bi_bo": sum(r.verify.dropped_sentences for r in ok),
            "bang_ma_so_tb": round(statistics.fmean(len(r.number_table) for r in ok), 1),
        }
        res["nguon"] = {
            "tb": round(statistics.fmean(len(r.sources) for r in ok), 2),
            "do_thi_tb": round(
                statistics.fmean(sum(s.origin == "graph" for s in r.sources) for r in ok), 2
            ),
            "trich_nguon_do_thi": _rate(
                sum(
                    1
                    for r in ok
                    for c in r.citations
                    if any(s.sid == c.sid and s.origin == "graph" for s in r.sources)
                ),
                n_v,
            ),
            "cat_ngan": sum(1 for r in ok for s in r.sources if s.truncated),
        }
    elif ok:
        bad = Counter(c.status for r in ok for p in r.points for c in p.citations)
        res["b0"] = {
            "so_khong_kiem_duoc_tb": round(
                statistics.fmean(r.verify.n_free_numbers for r in ok), 2
            ),
            "cau_co_so": _rate(sum(1 for r in ok if r.verify.n_free_numbers), len(ok)),
            "trich_dan_bia": _rate(bad["khong_ton_tai"] + bad["van_ban_khong_ro"], n_c),
            "trich_dan_het_hieu_luc": _rate(bad["het_hieu_luc"], n_c),
            "trang_thai_trich_dan": dict(bad),
        }
    if ok:
        res["y_tb"] = round(statistics.fmean(len(r.points) for r in ok), 2)
        res["do_dai_tb"] = round(statistics.fmean(len(r.answer) for r in ok), 1)
        res["token_vao_tb"] = round(statistics.fmean(r.usage.prompt_tokens for r in ok), 1)
        res["token_ra_tb"] = round(statistics.fmean(r.usage.completion_tokens for r in ok), 1)
        lat = [r.latency_ms for r in ok if not r.cached]
        res["latency_ms"] = {"p50": _pct(lat, 0.5), "p95": _pct(lat, 0.95)}
        res["goi_llm_tb"] = round(statistics.fmean(r.n_llm_calls for r in ok), 3)
        if ok[0].retrieval is not None and ok[0].retrieval.has_reranker:
            res["low_score"] = _rate(sum(1 for r in ok if r.low_retrieval_score), len(ok))
    return res


def load_rows(path: Path) -> list[AnswerResult]:
    return [AnswerResult.model_validate(r) for r in latest_results(path).values()]


def cmd_summarize(root: Path, acfg: AnswerConfig, args: argparse.Namespace) -> int:
    run_id = args.run_id or acfg.eval.run_id
    rdir = root / acfg.eval.results_dir / run_id
    report: dict[str, Any] = {"run_id": run_id, "sets": {}, "generated_at": now_iso()}
    for set_name in SETS:
        p = root / (acfg.eval.val if set_name == "val" else acfg.eval.dev_out_of_scope)
        if not p.is_file():
            continue
        gold = {str(r["qid"]): list(r.get("gold_units") or []) for r in read_jsonl(p)}
        for f in sorted(rdir.glob(f"answers_{set_name}_*.jsonl")):
            cfg = f.stem.removeprefix(f"answers_{set_name}_")
            rows = load_rows(f)
            if not rows:
                continue
            report["sets"].setdefault(set_name, {})[cfg] = summarize_rows(rows, gold)
            report["sets"][set_name][cfg]["model_id"] = rows[0].model_id
            report["sets"][set_name][cfg]["prompt_hash"] = rows[0].prompt_hash
            report["sets"][set_name][cfg]["serve"] = rows[0].serve
    runs = [
        r for r in read_jsonl(root / acfg.eval.out_dir / "runs.jsonl") if r.get("run_id") == run_id
    ]
    report["runs"] = runs
    report["gpu_seconds"] = round(sum(r.get("seconds", 0) for r in runs), 1)
    report["vram"] = list(read_jsonl(root / acfg.eval.out_dir / "vram.jsonl"))
    out = root / acfg.eval.out_dir / "dev_eval.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
        newline="\n",
    )
    md = render_md(report, examples=pick_examples(rdir, acfg.eval.seed, 10))
    out.with_suffix(".md").write_text(md, encoding="utf-8", newline="\n")
    print(f"→ {out.with_suffix('.md')}")
    return 0


def _rank(seed: int, name: str, qid: str) -> str:
    return hashlib.sha256(f"{seed}:{name}:{qid}".encode()).hexdigest()


def pick_examples(rdir: Path, seed: int, n: int, name: str = "m12_examples") -> list[AnswerResult]:
    p = rdir / "answers_val_G.jsonl"
    if not p.is_file():
        return []
    rows = [r for r in load_rows(p) if r.status == "ok"]
    rows.sort(key=lambda r: _rank(seed, name, str(r.qid)))
    return rows[:n]


def _f(x: object) -> str:
    return f"{100 * float(x):.1f}" if isinstance(x, (int, float)) else "—"


def render_answer_block(r: AnswerResult, gold: Sequence[str] = ()) -> list[str]:
    lines = [
        f"**{r.qid}** · as_of {r.as_of} · loại"
        f" `{r.retrieval.question_type if r.retrieval else '—'}`"
        f" · {r.answer_status} · gold {', '.join(f'`{g}`' for g in gold) or '—'}",
        "",
        f"> {r.question}",
        "",
        "Nguồn: " + "; ".join(f"{s.sid} `{s.chunk_id}` ({s.origin})" for s in r.sources),
        "",
        "```text",
        r.answer or "(rỗng)",
        "```",
        "",
        f"Mã số dùng: {', '.join(f'{n.id}={n.rendered} [{n.source}]' for n in r.numbers) or '—'}"
        f" · cờ verify: {', '.join(r.verify.flags) or '—'}"
        f"{' · đã sửa số' if r.verify.repaired else ''}",
        "",
    ]
    return lines


def render_md(report: dict[str, Any], examples: Sequence[AnswerResult]) -> str:
    out_lines = [
        "# M12 — chạy thử sinh câu trả lời (val + dev ngoài phạm vi — KHÔNG dùng test)",
        "",
        f"Run `{report['run_id']}` · sinh lúc {report['generated_at']} · tổng thời gian sinh"
        f" {report['gpu_seconds']} s.",
        "",
        "Val không có đáp án vàng ⇒ chỉ đo chỉ số không cần đáp án: **trích gold** = câu `ok`"
        " có ít nhất một trích dẫn hợp lệ tới unit gold (hoặc tổ tiên/con cháu); **nguồn có gold**"
        " = ngữ cảnh chứa gold; trích dẫn hợp lệ = trong ngữ cảnh + đúng unit + hiệu lực tại as_of."
        " Con số: vi phạm = chữ số/số viết bằng chữ/ngày không có căn cứ hoặc mã `{N#}` lạ trong"
        " phản hồi LLM. Độ đúng câu trả lời (LLM judge) là việc của M13.",
        "",
    ]
    for set_name, cfgs in report["sets"].items():
        out_lines += [
            f"## {set_name}",
            "",
            "| Cấu hình | n | ok | format_error | error | từ chối | trích gold | nguồn có gold |"
            " trích dẫn hợp lệ | câu dùng mã số | vi phạm trước sửa | sau sửa | câu bị bỏ |"
            " token vào/ra TB | latency p50 (ms) |",
            "| --- |" + " ---: |" * 14,
        ]
        for cfg, r in cfgs.items():
            s = r["status"]
            cs = r.get("con_so") or {}
            out_lines.append(
                f"| {cfg} | {r['n']} | {s.get('ok', 0)} | {s.get('format_error', 0)} |"
                f" {s.get('error', 0)} | {_f(r.get('tu_choi'))} | {_f(r.get('trich_gold'))} |"
                f" {_f(r.get('nguon_co_gold'))} | {_f(r['trich_dan']['hop_le'])} |"
                f" {_f(cs.get('cau_dung_ma_so'))} | {_f(cs.get('cau_vi_pham_truoc_sua'))} |"
                f" {_f(cs.get('cau_vi_pham_sau_sua'))} | {cs.get('cau_bi_bo', '—')} |"
                f" {r.get('token_vao_tb', '—')}/{r.get('token_ra_tb', '—')} |"
                f" {(r.get('latency_ms') or {}).get('p50', '—')} |"
            )
        out_lines.append("")
        for cfg, r in cfgs.items():
            extra = {k: r[k] for k in ("co_theo_cau", "nguon", "b0", "answer_status") if k in r}
            out_lines += [f"- **{cfg}**: `{json.dumps(extra, ensure_ascii=False)}`"]
        out_lines.append("")
    if report.get("vram"):
        out_lines += ["## VRAM (một câu online, hồ sơ serve + embedder + reranker cùng GPU)", ""]
        for v in report["vram"]:
            out_lines.append(
                f"- {v.get('finished_at')}: hồ sơ `{v.get('profile')}`, nvidia-smi đỉnh"
                f" {v.get('nvidia_smi_peak_mib')} / {v.get('nvidia_smi_total_mib')} MiB, torch"
                f" (embedder + reranker) {v.get('torch_max_allocated_gib')} GiB,"
                f" {v.get('wall_s')} s"
            )
        out_lines.append("")
    if examples:
        out_lines += ["## 10 ví dụ G (val, chọn theo `sha256(42:m12_examples:qid)`)", ""]
        for r in examples:
            out_lines += render_answer_block(r)
    return "\n".join(out_lines) + "\n"


def cmd_review(root: Path, acfg: AnswerConfig, args: argparse.Namespace) -> int:
    run_id = args.run_id or acfg.eval.run_id
    rdir = root / acfg.eval.results_dir / run_id
    rows = pick_examples(rdir, acfg.eval.seed, acfg.eval.review_n, name="m12_review")
    if not rows:
        print("chưa có kết quả G trên val", file=sys.stderr)
        return 1
    from trafficlaw.retrieval.catalog import ChunkCatalog

    rcfg = load_retrieval_config(root / "configs" / "retrieval.yaml")
    cat = ChunkCatalog.load(root / rcfg.index_dir / "chunks.jsonl")
    gold = {
        str(r["qid"]): list(r.get("gold_units") or []) for r in read_jsonl(root / acfg.eval.val)
    }
    out_lines = [
        f"# Rà tay M12 — {len(rows)} câu trả lời G trên val (`sha256(42:m12_review:qid)`)",
        "",
        "Mỗi câu: (1) **nguồn** đúng — ngữ cảnh có điều khoản trả lời được câu hỏi? (2) **số** —"
        " mọi con số trong câu trả lời đúng với nguyên văn nguồn được trích? (3) **trích dẫn** —"
        " mỗi ý trích đúng Khoản/Điểm chứa nội dung? (4) nhận xét. Claude rà trước (cột *Claude*),"
        " người dùng xác nhận/sửa (cột *Người dùng*).",
        "",
    ]
    for i, r in enumerate(rows, 1):
        g = gold.get(str(r.qid), [])
        out_lines += [f"## {i}. {r.qid}", ""]
        out_lines += render_answer_block(r, g)
        out_lines += ["<details><summary>Nguyên văn nguồn</summary>", ""]
        for s in r.sources:
            txt = cat.get(s.chunk_id).text if s.chunk_id in cat.by_id else ""
            out_lines += [
                f"**{s.sid}** {s.label} — {s.doc_label} ({s.origin})",
                "",
                "```text",
                txt,
                "```",
                "",
            ]
        out_lines += ["</details>", ""]
        out_lines += [
            "| Tiêu chí | Claude | Người dùng |",
            "| --- | --- | --- |",
            "| Nguồn đúng |  |  |",
            "| Số đúng |  |  |",
            "| Trích dẫn đúng Khoản/Điểm |  |  |",
            "| Nhận xét |  |  |",
            "",
        ]
    out = root / acfg.eval.out_dir / "review.md"
    out.write_text("\n".join(out_lines) + "\n", encoding="utf-8", newline="\n")
    print(f"→ {out}")
    return 0


# --------------------------------------------------------------------------- τ


def cmd_calibrate_tau(root: Path, acfg: AnswerConfig, args: argparse.Namespace) -> int:
    """τ trên điểm rerank top-1 của cấu hình G: câu val (dương) vs dev_oos (ngoài phạm vi).
    Chọn τ cực đại Youden J = TPR(oos < τ) − FPR(val < τ)."""
    cfg = args.configs[0] if args.configs else "G"

    def scores(set_name: str) -> list[float]:
        for p in retrieval_paths(root, acfg, set_name, cfg):
            if p.is_file():
                return [float(r["hits"][0]["score"]) for r in read_jsonl(p) if r.get("hits")]
        raise SystemExit(f"chưa có truy hồi {set_name}/{cfg} (chạy --retrieve-only trên máy thuê)")

    pos, neg = scores("val"), scores("dev_oos")
    cands = sorted(set(pos) | set(neg))
    best = (-2.0, None, 0.0, 0.0)
    rows = []
    for t in cands + [max(cands) + 1e-6]:
        tpr = sum(1 for x in neg if x < t) / len(neg)
        fpr = sum(1 for x in pos if x < t) / len(pos)
        rows.append((t, tpr, fpr))
        if tpr - fpr > best[0]:
            best = (tpr - fpr, t, tpr, fpr)
    j, tau, tpr, fpr = best
    q = statistics.quantiles
    rep = {
        "config": cfg,
        "n_val": len(pos),
        "n_dev_oos": len(neg),
        "val_top1": {"min": min(pos), "p05": q(pos, n=20)[0], "median": statistics.median(pos)},
        "dev_oos_top1": {
            "median": statistics.median(neg),
            "p95": q(neg, n=20)[-1],
            "max": max(neg),
        },
        "tau": round(float(tau), 4) if tau is not None else None,
        "youden_j": round(j, 4),
        "tpr_oos": round(tpr, 4),
        "fpr_val": round(fpr, 4),
        "generated_at": now_iso(),
    }
    out = root / acfg.eval.out_dir / "tau.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    print(json.dumps(rep, ensure_ascii=False, indent=2))
    print(f"→ {out} (đặt refusal.tau trong configs/answer.yaml sau khi người dùng duyệt)")
    return 0


# --------------------------------------------------------------------------- main


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--question")
    ap.add_argument("--as-of")
    ap.add_argument("--config", default="G")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--eval", dest="sets", type=lambda s: s.split(","), default=None)
    ap.add_argument("--configs", type=lambda s: s.split(","), default=["G", "B3", "B0"])
    ap.add_argument("--n", type=int, default=None, help="tập con phân tầng (mặc định cả tập)")
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--run-id")
    ap.add_argument("--model")
    ap.add_argument("--profile", choices=["default", "shared"], default="default")
    ap.add_argument("--gpu", action="store_true", help="nạp embedder/reranker khi thiếu cache")
    ap.add_argument("--no-llm-analyzer", action="store_true")
    ap.add_argument("--analyzer-llm", action="store_true", help="--retrieve-only: gọi LLM analyzer")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--retrieve-only", action="store_true")
    ap.add_argument("--summarize", action="store_true")
    ap.add_argument("--review", action="store_true")
    ap.add_argument("--calibrate-tau", action="store_true")
    ap.add_argument("--today", type=date.fromisoformat, default=date(2026, 11, 3))
    args = ap.parse_args(argv)
    setup_logging()
    set_seed(42)
    load_dotenv(REPO_ROOT / ".env")
    _env_key()
    root = REPO_ROOT
    acfg = load_answer_config(root / "configs" / "answer.yaml")
    if args.n is None:
        args.n = acfg.eval.sample_n
    if args.calibrate_tau:
        return cmd_calibrate_tau(root, acfg, args)
    if args.summarize:
        return cmd_summarize(root, acfg, args)
    if args.review:
        return cmd_review(root, acfg, args)
    if args.question:
        return cmd_question(root, acfg, args)
    args.sets = args.sets or ["val"]
    if args.dry_run:
        return cmd_dry_run(root, acfg, args)
    if args.retrieve_only:
        return cmd_retrieve_only(root, acfg, args)
    return cmd_eval(root, acfg, args)


if __name__ == "__main__":
    sys.exit(main())
