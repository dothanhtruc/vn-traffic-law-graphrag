"""Điều phối ba giai đoạn M13 (dùng chung cho ``scripts.eval`` và smoke).

Hàm ở đây nhận ngữ cảnh đã dựng (``RetrievalContext``, ``AnswerContext``, ``JudgeContext``) — việc
nạp model/server, dry-run, máy thuê thuộc ``scripts/eval.py``.
"""

from __future__ import annotations

import copy
import hashlib
import json
import logging
from collections import Counter, defaultdict
from collections.abc import Callable, Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from trafficlaw.eval.answer_metrics import GoldItem, pair_correct
from trafficlaw.eval.eval_config import EvalConfig
from trafficlaw.eval.judge import (
    JudgeContext,
    JudgeRecord,
    answer_hash,
    latest_judgements,
    render_for_judge,
    run_judge,
)
from trafficlaw.eval.report import compare, config_summary, render_summary_md, variance_summary
from trafficlaw.eval.runner import (
    FULL,
    EvalData,
    StageStats,
    answers_path,
    check_single_run,
    judge_path,
    load_answers,
    load_retrievals,
    retrieve_path,
    run_retrieve,
    score_config,
    scores_path,
)
from trafficlaw.eval.stats import cohen_kappa
from trafficlaw.pipeline.answer import AnswerContext, AnswerResult
from trafficlaw.pipeline.runner import DONE_STATUSES, Query, run_answers
from trafficlaw.retrieval.catalog import ChunkCatalog
from trafficlaw.retrieval.retrieve import RetrievalContext, RetrievalResult
from trafficlaw.utils.jsonl import read_jsonl, write_jsonl

logger = logging.getLogger(__name__)
Progress = Callable[[str, int, int], None]


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def _limit(items: list[GoldItem], limit: int | None) -> list[GoldItem]:
    return items[:limit] if limit else items


# --------------------------------------------------------------------------- 1. retrieve


def retrieve_plan(ecfg: EvalConfig, configs: Sequence[str] | None = None) -> dict[str, str]:
    """Cấu hình → tập câu cho giai đoạn truy hồi: mọi cấu hình RAG của ``retrieve`` (tập
    ``retrieve.set``) ∪ cấu hình RAG của ``generate`` (khác tập ⇒ lấy ``full``)."""
    plan = {c: ecfg.retrieve.set for c in ecfg.retrieve.configs}
    for c, s in ecfg.generate.items():
        if c == "B0":
            continue
        if c not in plan:
            plan[c] = s
        elif plan[c] != s and FULL in (plan[c], s):
            plan[c] = FULL
    if configs:
        plan = {c: plan.get(c, FULL) for c in configs if c != "B0"}
    return plan


def stage_retrieve(
    data: EvalData,
    ecfg: EvalConfig,
    rctx: RetrievalContext,
    run_dir: Path,
    *,
    configs: Sequence[str] | None = None,
    use_llm: bool = True,
    limit: int | None = None,
    progress: Progress | None = None,
) -> dict[str, StageStats]:
    out = {}
    for cfg, set_name in retrieve_plan(ecfg, configs).items():
        items = _limit(data.select(set_name), limit)
        out[cfg] = run_retrieve(
            items,
            cfg,
            rctx,
            retrieve_path(run_dir, cfg),
            use_llm=use_llm,
            progress=(lambda i, n, c=cfg: progress(c, i, n)) if progress else None,
        )
    return out


# --------------------------------------------------------------------------- 2. generate


def generate_jobs(
    ecfg: EvalConfig, configs: Sequence[str] | None = None, *, variance: bool = True
) -> list[tuple[str, str, int | None]]:
    """(cấu hình, tập, seed | None): ma trận chính rồi các lượt dao động."""
    jobs: list[tuple[str, str, int | None]] = [
        (c, s, None) for c, s in ecfg.generate.items() if not configs or c in configs
    ]
    v = ecfg.variance
    if variance and v.seeds and (not configs or v.config in configs):
        jobs += [(v.config, v.subset, s) for s in v.seeds]
    return jobs


def variant_ctx(actx: AnswerContext, seed: int | None) -> AnswerContext:
    if seed is None:
        return actx
    c = copy.copy(actx)
    c.llm_params = {**actx.llm_params, "seed": seed}
    c.use_cache = False
    return c


def stage_generate(
    data: EvalData,
    ecfg: EvalConfig,
    actx: AnswerContext,
    run_dir: Path,
    *,
    configs: Sequence[str] | None = None,
    variance: bool = True,
    workers: int = 1,
    limit: int | None = None,
    progress: Progress | None = None,
) -> dict[str, Any]:
    out: dict[str, Any] = {}
    meta = actx.retrieval.meta if actx.retrieval is not None else {}
    for cfg, set_name, seed in generate_jobs(ecfg, configs, variance=variance):
        items = _limit(data.select(set_name), limit)
        rets: dict[str, RetrievalResult] = {}
        if not actx.is_no_rag(cfg):
            p = retrieve_path(run_dir, cfg)
            rets = load_retrievals(p, meta) if p.is_file() else {}
            missing = [it.qid for it in items if it.qid not in rets]
            if missing:
                raise FileNotFoundError(
                    f"{cfg}: thiếu kết quả truy hồi của {len(missing)} câu ({missing[:3]}…) —"
                    " chạy `scripts.eval retrieve` trước"
                )
        tag = cfg if seed is None else f"{cfg}_seed{seed}"
        st = run_answers(
            [Query(it.qid, it.question, it.as_of) for it in items],
            cfg,
            variant_ctx(actx, seed),
            answers_path(run_dir, cfg, seed),
            retrievals=rets,
            workers=workers,
            progress=(lambda i, n, t=tag: progress(t, i, n)) if progress else None,
        )
        out[tag] = st
        if st.stopped:
            break
    return out


# --------------------------------------------------------------------------- 3. score


def judge_items(data: EvalData, ecfg: EvalConfig) -> list[GoldItem]:
    return data.select(ecfg.judge.subset)


def current_judgements(
    path: Path, jctx_model: str, jctx_hash: str, answers: Mapping[str, AnswerResult]
) -> dict[str, JudgeRecord]:
    """qid → bản chấm khớp câu trả lời hiện hành (cùng ``answer_hash``)."""
    if not path.is_file():
        return {}
    allj = latest_judgements(path, model_id=jctx_model, prompt_hash=jctx_hash)
    out = {}
    for q, a in answers.items():
        rec = allj.get((q, answer_hash(a)))
        if rec is not None:
            out[q] = rec
    return out


def stage_judge(
    data: EvalData,
    ecfg: EvalConfig,
    jctx: JudgeContext,
    run_dir: Path,
    *,
    configs: Sequence[str] | None = None,
    workers: int = 1,
    progress: Progress | None = None,
) -> dict[str, Any]:
    out: dict[str, Any] = {}
    items = judge_items(data, ecfg)
    for cfg in ecfg.judge.configs:
        if configs and cfg not in configs:
            continue
        ans = load_answers(answers_path(run_dir, cfg))
        pairs = [
            (it, ans[it.qid])
            for it in items
            if it.qid in ans and ans[it.qid].status in DONE_STATUSES
        ]
        out[cfg] = run_judge(
            pairs,
            jctx,
            judge_path(run_dir, cfg),
            workers=workers,
            progress=(lambda i, n, c=cfg: progress(f"judge {c}", i, n)) if progress else None,
        )
    return out


def _pairs_map(items: Sequence[GoldItem]) -> dict[str, list[str]]:
    m: dict[str, list[str]] = defaultdict(list)
    for it in items:
        if it.pair_id:
            m[it.pair_id].append(it.qid)
    return dict(m)


def score_all(
    data: EvalData,
    ecfg: EvalConfig,
    catalog: ChunkCatalog,
    run_dir: Path,
    meta: Mapping[str, Any],
    *,
    judge_model: str | None = None,
    judge_prompt_hash: str | None = None,
    judge_family: str | None = None,
    extra: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Chỉ số mọi cấu hình có kết quả → ``scores_<cfg>.jsonl`` + ``summary.{json,md}``."""
    cfg_sets: dict[str, str] = dict(retrieve_plan(ecfg))
    for c, s in ecfg.generate.items():
        cfg_sets[c] = s
    pairs = _pairs_map(data.items)
    summary: dict[str, Any] = {
        "run_id": run_dir.name,
        "generated_at": _now(),
        "data_version": meta.get("data_version"),
        "catalog_sha256": meta.get("catalog_sha256"),
        "graph_data_hash": meta.get("graph_data_hash"),
        "qa_version": data.qa_version,
        "test_sha256": data.test_sha256,
        "n_test": len(data.items),
        "invalid": data.invalid,
        "compare_to": ecfg.stats.compare_to,
        "configs": {},
        **(extra or {}),
    }
    all_rows: dict[str, list[dict[str, Any]]] = {}
    jsum: dict[str, Any] = {}
    for cfg, set_name in cfg_sets.items():
        rp, ap = retrieve_path(run_dir, cfg), answers_path(run_dir, cfg)
        rets = load_retrievals(rp, meta) if rp.is_file() else {}
        ans = load_answers(ap) if ap.is_file() else {}
        if not rets and not ans:
            continue
        mp = check_single_run(ans, ap)
        judgements: dict[str, JudgeRecord] = {}
        if judge_model and judge_prompt_hash and cfg in ecfg.judge.configs:
            jitems = {it.qid for it in judge_items(data, ecfg)}
            judgements = {
                q: r
                for q, r in current_judgements(
                    judge_path(run_dir, cfg), judge_model, judge_prompt_hash, ans
                ).items()
                if q in jitems
            }
            c = Counter(r.status for r in judgements.values())
            jsum[cfg] = {
                "llm": sum(
                    1 for r in judgements.values() if r.judge_source == "llm" and r.status == "ok"
                ),
                "rule": sum(1 for r in judgements.values() if r.judge_source == "rule"),
                "format_error": c.get("format_error", 0),
                "error": c.get("error", 0),
                "dung_khong_khop": sum(
                    1 for r in judgements.values() if "dung_khong_khop" in r.flags
                ),
                "n_items": len(jitems),
            }
        rows = score_config(data.items, ans, rets, catalog, judgements)
        write_jsonl(scores_path(run_dir, cfg), rows)
        all_rows[cfg] = rows
        gen_items = data.select(set_name)
        statuses = Counter(ans[it.qid].status for it in gen_items if it.qid in ans)
        n_done = sum(statuses[s] for s in DONE_STATUSES)
        texts = {q: a.answer for q, a in ans.items() if a.status in DONE_STATUSES}
        rmap = {r["qid"]: r for r in rows}
        flags = pair_correct(rmap, texts, pairs) if ans else {}
        summary["configs"][cfg] = {
            "set": set_name if ans else f"{ecfg.retrieve.set} (chỉ truy hồi)",
            "n_total": len(gen_items) if ans else 0,
            "n_done": n_done,
            "n_retrieved": len(rets),
            "statuses": dict(statuses),
            "model_id": mp[0] if mp else None,
            "prompt_hash": mp[1] if mp else None,
            "serve": next((a.serve for a in ans.values() if a.serve), None),
            **config_summary(rows, flags, n_boot=ecfg.stats.bootstrap, seed=ecfg.stats.seed),
        }
    base = ecfg.stats.compare_to
    if base in all_rows:
        summary["comparisons"] = compare(
            all_rows[base],
            {c: r for c, r in all_rows.items() if c != base},
            n_boot=ecfg.stats.bootstrap,
            seed=ecfg.stats.seed,
        )
    v = ecfg.variance
    per_seed: dict[int, list[dict[str, Any]]] = {}
    texts_seed: dict[int, dict[str, str]] = {}
    vitems = data.select(v.subset) if v.subset in data.subsets or v.subset == FULL else []
    for s in v.seeds:
        p = answers_path(run_dir, v.config, s)
        if not p.is_file():
            continue
        ans = load_answers(p)
        per_seed[s] = score_config(vitems, ans, {}, catalog)
        texts_seed[s] = {q: a.answer for q, a in ans.items() if a.status in DONE_STATUSES}
    if per_seed:
        summary["variance"] = {
            "config": v.config,
            "subset": v.subset,
            **variance_summary(per_seed, texts_seed),
        }
    if jsum:
        summary["judge"] = {
            "model_id": judge_model,
            "prompt_hash": judge_prompt_hash,
            "family": judge_family,
            "subset": ecfg.judge.subset,
            "configs": jsum,
        }
    jc = judge_check_summary(data, ecfg, run_dir, judge_model, judge_prompt_hash)
    if jc:
        summary["judge_check"] = jc
    (run_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8"
    )
    (run_dir / "summary.md").write_text(render_summary_md(summary), encoding="utf-8")
    return summary


# --------------------------------------------------------------------------- kiểm định judge


def judge_check_items(data: EvalData, ecfg: EvalConfig) -> list[GoldItem]:
    """``n`` câu của tập judge, xếp theo ``sha256(seed:seed_key:qid)``, bỏ câu chấm bằng luật
    ``ngoai_pham_vi`` (judge LLM không chấm chúng)."""
    jc = ecfg.judge_check
    pool = [it for it in judge_items(data, ecfg) if it.question_type != "ngoai_pham_vi"]
    pool.sort(
        key=lambda it: hashlib.sha256(f"{ecfg.seed}:{jc.seed_key}:{it.qid}".encode()).hexdigest()
    )
    return pool[: jc.n]


def export_judge_check(data: EvalData, ecfg: EvalConfig, run_dir: Path) -> Path:
    """Phiếu chấm độc lập (KHÔNG chứa điểm judge): ``judge_check.md`` + mẫu nhãn
    ``judge_check_labels.jsonl`` (không ghi đè nhãn đã có)."""
    cfg = ecfg.judge_check.config
    ans = load_answers(answers_path(run_dir, cfg))
    items = [it for it in judge_check_items(data, ecfg) if it.qid in ans]
    lines = [
        f"# Phiếu kiểm định judge — {len(items)} câu {cfg} (`sha256({ecfg.seed}:"
        f"{ecfg.judge_check.seed_key}:qid)` trong `{ecfg.judge.subset}`)",
        "",
        "Chấm theo **cùng rubric** với `llm/prompts/judge.md` (0 sai · 1 đúng một phần · 2 đúng"
        " hoàn toàn so với đáp án tham chiếu), **không xem điểm judge**. Ghi điểm vào"
        " `judge_check_labels.jsonl` (`claude_diem`, `ly_do`); người dùng xác nhận bằng"
        " `user_confirmed: true`.",
        "",
    ]
    for i, it in enumerate(items, 1):
        a = ans[it.qid]
        lines += [
            f"## {i}. `{it.qid}` · {it.question_type} · `{it.source_kind}` · as_of {it.as_of}",
            "",
            f"**Câu hỏi:** {it.question}",
            "",
            f"**Đáp án tham chiếu:** {it.answer}",
            "",
            f"**Câu trả lời ({a.status}/{a.answer_status}):**",
            "",
            "```text",
            render_for_judge(a) if a.status == "ok" else "(format_error)",
            "```",
            "",
        ]
    md = run_dir / "judge_check.md"
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    lab = run_dir / "judge_check_labels.jsonl"
    have = {str(r["qid"]) for r in read_jsonl(lab)} if lab.is_file() else set()
    new = [
        {
            "qid": it.qid,
            "source_kind": it.source_kind,
            "answer_hash": answer_hash(ans[it.qid]),
            "claude_diem": None,
            "ly_do": "",
            "user_confirmed": False,
        }
        for it in items
        if it.qid not in have
    ]
    if new:
        write_jsonl(lab, [*read_jsonl(lab), *new] if lab.is_file() else new)
    return md


def judge_check_summary(
    data: EvalData,
    ecfg: EvalConfig,
    run_dir: Path,
    judge_model: str | None,
    judge_prompt_hash: str | None,
) -> dict[str, Any] | None:
    lab = run_dir / "judge_check_labels.jsonl"
    if not lab.is_file():
        return None
    labels = list(read_jsonl(lab))
    if not labels:
        return None
    pending = [r for r in labels if r.get("claude_diem") is None or not r.get("user_confirmed")]
    if pending:
        return {
            "status": "cho_xac_nhan",
            "note": f"{len(pending)}/{len(labels)} nhãn chưa chấm hoặc chưa được xác nhận",
        }
    if not judge_model or not judge_prompt_hash:
        return {"status": "chua_co_judge", "note": "chưa có kết quả judge"}
    cfg = ecfg.judge_check.config
    ans = load_answers(answers_path(run_dir, cfg))
    js = current_judgements(judge_path(run_dir, cfg), judge_model, judge_prompt_hash, ans)
    pairs: dict[str, list[tuple[int, int]]] = defaultdict(list)
    stale = 0
    for r in labels:
        q = str(r["qid"])
        j = js.get(q)
        if j is None or j.diem is None or q not in ans:
            continue
        if r.get("answer_hash") != answer_hash(ans[q]):
            stale += 1
            continue
        p = (int(r["claude_diem"]), int(j.diem))
        pairs["tat_ca"].append(p)
        pairs[str(r.get("source_kind"))].append(p)
    parts = {}
    for name, ps in pairs.items():
        a = [x for x, _ in ps]
        b = [y for _, y in ps]
        ab = [x == 2 for x in a]
        bb = [y == 2 for y in b]
        parts[name] = {
            "n": len(ps),
            "agree": sum(1 for x, y in ps if x == y) / len(ps),
            "kappa": cohen_kappa(a, b),
            "agree_binary": sum(1 for x, y in zip(ab, bb, strict=True) if x == y) / len(ps),
            "kappa_binary": cohen_kappa(ab, bb),
        }
    return {
        "status": "ok",
        "parts": dict(sorted(parts.items(), key=lambda kv: kv[0] != "tat_ca")),
        "n_stale": stale,
        "note": "Claude chấm độc lập (không xem điểm judge) theo cùng rubric; người dùng xác nhận."
        " Hạn chế: 160 đáp án tham chiếu (`+claude`) do chính Claude sửa ⇒ ở phần `claude`, Claude"
        " chấm trên đáp án mình viết. Không chỉnh prompt judge theo kết quả này.",
    }


__all__ = [
    "export_judge_check",
    "generate_jobs",
    "judge_check_items",
    "judge_check_summary",
    "retrieve_plan",
    "score_all",
    "stage_generate",
    "stage_judge",
    "stage_retrieve",
    "variant_ctx",
]
