"""Bộ chạy đánh giá M13: ba giai đoạn độc lập, resume được (CLAUDE.md mục 10).

1. ``retrieve`` — ``retrieve()`` (M11) mỗi cấu hình RAG → ``results/<run>/retrieve_<cfg>.jsonl``
   (``RetrievalResult``). Resume theo ``(config_name, qid)``; bản ghi có ``data_version`` /
   ``catalog_sha256`` / ``graph_data_hash`` lệch dữ liệu hiện hành → từ chối (``StaleResultError``).
2. ``generate`` — ``answer(…, retrieval=<giai đoạn 1>)`` (M12) qua ``pipeline.runner.run_answers``
   → ``answers_<cfg>.jsonl``; khoá ``(config_name, qid, model_id, prompt_hash)``; ``error``
   chạy lại.
3. ``score`` — chỉ số tất định (``answer_metrics``) + judge (``judge``) → ``scores_<cfg>.jsonl``
   (dựng lại toàn bộ mỗi lần, tất định), ``judge_<cfg>.jsonl`` (append, resume).

Tập câu: test đã qua validator (câu lỗi bị loại và liệt kê); tập con từ ``subsets.json`` — file này
phải khớp ``test_sha256`` hiện hành (``stale`` → ``StaleSubsetsError``).
"""

from __future__ import annotations

import hashlib
import logging
from collections import Counter, defaultdict
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from trafficlaw.eval.answer_metrics import GoldItem, score_row
from trafficlaw.eval.judge import JudgeRecord
from trafficlaw.eval.qa_schema import QAItem, split_of
from trafficlaw.eval.qa_subsets import file_sha256, qa_version, subsets_status
from trafficlaw.eval.qa_validate import ValidateConfig, validate_items
from trafficlaw.pipeline.answer import AnswerResult
from trafficlaw.pipeline.runner import DONE_STATUSES, latest_results
from trafficlaw.retrieval.catalog import ChunkCatalog
from trafficlaw.retrieval.retrieve import RetrievalContext, RetrievalResult
from trafficlaw.utils.jsonl import JsonlWriter, read_jsonl
from trafficlaw.verify.numbers import as_decimal

logger = logging.getLogger(__name__)

FULL = "full"
META_KEYS = ("data_version", "catalog_sha256", "graph_data_hash")


class StaleSubsetsError(RuntimeError):
    pass


class StaleResultError(RuntimeError):
    pass


# --------------------------------------------------------------------------- dữ liệu test


@dataclass
class EvalData:
    items: list[GoldItem]
    """Câu hợp lệ, theo thứ tự file test."""
    invalid: list[dict[str, Any]]
    """Câu bị loại vì lỗi validator: ``{qid, codes}``."""
    subsets: dict[str, list[str]]
    test_sha256: str
    qa_version: str
    n_warnings: int = 0
    by_qid: dict[str, GoldItem] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.by_qid = {it.qid: it for it in self.items}

    def select(self, set_name: str) -> list[GoldItem]:
        if set_name == FULL:
            return list(self.items)
        if set_name not in self.subsets:
            raise KeyError(f"tập con {set_name!r} không có trong subsets.json")
        keep = set(self.subsets[set_name])
        return [it for it in self.items if it.qid in keep]


def to_gold_items(resolved: Sequence[Mapping[str, Any]]) -> list[GoldItem]:
    items = [QAItem.model_validate(r) for r in resolved]
    pairs: dict[str, list[QAItem]] = defaultdict(list)
    for it in items:
        if it.pair_id:
            pairs[it.pair_id].append(it)
    out = []
    for it in items:
        partner: tuple[str, ...] = ()
        if it.pair_id:
            partner = tuple(u for o in pairs[it.pair_id] if o.qid != it.qid for u in o.gold_units)
        out.append(
            GoldItem(
                qid=it.qid,
                question=it.question,
                as_of=it.as_of,
                question_type=str(it.question_type),
                tier=it.tier,
                answer=it.answer,
                gold_units=tuple(it.gold_units),
                gold_versions=tuple(it.gold_versions),
                required_numbers=tuple(as_decimal(n.value) for n in it.required_numbers),
                source=it.source,
                pair_id=it.pair_id,
                partner_gold=partner,
            )
        )
    return out


def load_eval_data(
    test_path: Path,
    subsets_path: Path | None,
    store: Any,
    *,
    drafts: Mapping[str, Mapping[str, Any]] | None = None,
    require_subsets: bool = True,
) -> EvalData:
    """Validate test (M9) rồi giải gold; tập con phải khớp test hiện hành."""
    rows = list(read_jsonl(test_path))
    try:
        split = split_of(test_path)
    except ValueError:
        split = "test"  # fixture smoke (smoke_test.jsonl) kiểm như test
    res = validate_items(rows, split, store, ValidateConfig(), drafts=drafts)
    bad = res.bad_qids()
    codes: dict[str, list[str]] = defaultdict(list)
    for i in res.issues:
        if i.level == "error" and i.qid:
            codes[i.qid].append(i.code)
    if bad:
        logger.warning("loại %d câu test lỗi validator: %s", len(bad), sorted(bad))
    items = to_gold_items([r for r in res.resolved if str(r["qid"]) not in bad])
    subsets: dict[str, list[str]] = {}
    if subsets_path is not None:
        st = subsets_status(subsets_path, test_path)
        if st != "ok":
            if require_subsets or st == "stale":
                raise StaleSubsetsError(
                    f"{subsets_path}: {st} so với {test_path} — chạy `qa_tool subsets` trước"
                )
        else:
            import json

            raw = json.loads(subsets_path.read_text(encoding="utf-8"))
            subsets = {k: [q for q in v["qids"] if q not in bad] for k, v in raw["subsets"].items()}
    paths = [test_path] + ([subsets_path] if subsets_path is not None else [])
    return EvalData(
        items=items,
        invalid=[{"qid": q, "codes": sorted(set(codes[q]))} for q in sorted(bad)],
        subsets=subsets,
        test_sha256=file_sha256(test_path),
        qa_version=qa_version(paths),
        n_warnings=res.n_warnings,
    )


# --------------------------------------------------------------------------- giai đoạn 1


def retrieve_path(run_dir: Path, cfg: str) -> Path:
    return run_dir / f"retrieve_{cfg}.jsonl"


def answers_path(run_dir: Path, cfg: str, seed: int | None = None) -> Path:
    return run_dir / (
        f"answers_{cfg}_seed{seed}.jsonl" if seed is not None else f"answers_{cfg}.jsonl"
    )


def judge_path(run_dir: Path, cfg: str) -> Path:
    return run_dir / f"judge_{cfg}.jsonl"


def scores_path(run_dir: Path, cfg: str) -> Path:
    return run_dir / f"scores_{cfg}.jsonl"


def load_retrievals(path: Path, meta: Mapping[str, Any]) -> dict[str, RetrievalResult]:
    """qid → ``RetrievalResult`` (bản cuối). Hash dữ liệu lệch ``meta`` → ``StaleResultError``."""
    out: dict[str, RetrievalResult] = {}
    for r in read_jsonl(path):
        rr = RetrievalResult.model_validate(r)
        for k in META_KEYS:
            if getattr(rr, k) != meta.get(k):
                raise StaleResultError(
                    f"{path}: {k} của {rr.qid} lệch dữ liệu hiện hành — xoá file / dùng run_id mới"
                )
        out[str(rr.qid)] = rr
    return out


@dataclass
class StageStats:
    n_total: int = 0
    n_skipped: int = 0
    n_written: int = 0
    statuses: Counter[str] = field(default_factory=Counter)
    stopped: str | None = None


def run_retrieve(
    items: Sequence[GoldItem],
    config_name: str,
    rctx: RetrievalContext,
    out_path: Path,
    *,
    use_llm: bool = True,
    progress: Callable[[int, int], None] | None = None,
) -> StageStats:
    st = StageStats(n_total=len(items))
    done = load_retrievals(out_path, rctx.meta) if out_path.is_file() else {}
    todo = [it for it in items if it.qid not in done]
    st.n_skipped = len(items) - len(todo)
    with JsonlWriter(out_path) as w:
        for i, it in enumerate(todo, 1):
            r = rctx.retrieve(it.question, it.as_of, config_name, qid=it.qid, use_llm=use_llm)
            w.write(r.model_dump(mode="json"))
            st.n_written += 1
            st.statuses["ok"] += 1
            if progress:
                progress(i, len(todo))
    return st


# --------------------------------------------------------------------------- giai đoạn 2/3


def load_answers(path: Path) -> dict[str, AnswerResult]:
    """qid → bản ghi mới nhất (bản xong thắng ``error``) — mọi model/prompt trong file."""
    out: dict[str, AnswerResult] = {}
    for r in latest_results(path).values():
        a = AnswerResult.model_validate(r)
        prev = out.get(str(a.qid))
        if prev is None or prev.status not in DONE_STATUSES or a.status in DONE_STATUSES:
            out[str(a.qid)] = a
    return out


def check_single_run(answers: Mapping[str, AnswerResult], path: Path) -> tuple[str, str] | None:
    """Mọi bản ghi xong phải cùng ``(model_id, prompt_hash)`` (một run một model/prompt)."""
    keys = {(a.model_id, a.prompt_hash) for a in answers.values() if a.status in DONE_STATUSES}
    if len(keys) > 1:
        raise StaleResultError(f"{path}: nhiều (model_id, prompt_hash) {sorted(keys)} — tách run")
    return next(iter(keys)) if keys else None


def score_config(
    items: Sequence[GoldItem],
    answers: Mapping[str, AnswerResult],
    retrievals: Mapping[str, RetrievalResult],
    catalog: ChunkCatalog,
    judgements: Mapping[str, JudgeRecord] | None = None,
) -> list[dict[str, Any]]:
    """Một dòng/câu đã có ít nhất một kết quả (truy hồi hoặc câu trả lời xong)."""
    rows = []
    for it in items:
        res = answers.get(it.qid)
        if res is not None and res.status not in DONE_STATUSES:
            res = None
        ret = retrievals.get(it.qid)
        if res is None and ret is None:
            continue
        row = score_row(it, res, ret, catalog)
        if res is not None:
            row["answer"] = res.answer
        j = (judgements or {}).get(it.qid)
        if j is not None and j.status == "ok" and j.diem is not None:
            row["metrics"]["judge_diem"] = float(j.diem)
            row["metrics"]["judge_dung"] = 1.0 if j.diem == 2 else 0.0
            row["judge_source"] = j.judge_source
        rows.append(row)
    return rows


def answers_digest(answers: Mapping[str, AnswerResult]) -> str:
    h = hashlib.sha256()
    for q in sorted(answers):
        h.update(f"{q}\x1f{answers[q].prompt_hash}\x1f{answers[q].status}\n".encode())
    return h.hexdigest()


__all__ = [
    "FULL",
    "EvalData",
    "StageStats",
    "StaleResultError",
    "StaleSubsetsError",
    "answers_digest",
    "answers_path",
    "check_single_run",
    "judge_path",
    "load_answers",
    "load_eval_data",
    "load_retrievals",
    "retrieve_path",
    "run_retrieve",
    "score_config",
    "scores_path",
    "to_gold_items",
]
