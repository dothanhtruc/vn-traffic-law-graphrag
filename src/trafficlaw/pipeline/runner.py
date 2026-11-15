"""Chạy ``answer()`` hàng loạt, resume được (M12 chạy thử trên val; M13 giai đoạn ``generate``).

- Khoá kết quả (CLAUDE.md mục 10): ``(config_name, qid, model_id, prompt_hash)``. Bản ghi ``ok`` /
  ``format_error`` là xong; ``error`` (lỗi mạng/hết retry) chạy lại ở lần sau.
- Truy hồi chạy **tuần tự** trước (``RetrievalContext`` không dùng chung giữa luồng; local chỉ đọc
  cache); gọi LLM song song ``workers`` luồng, chỉ luồng chính ghi JSONL (flush từng dòng).
- ``AnswerCache`` (demo M15, mục 12): khoá ``(câu hỏi chuẩn hoá, as_of, config, model_id,
  prompt_hash, data_version)``, JSONL append.
"""

from __future__ import annotations

import hashlib
import logging
import re
import unicodedata
from collections import Counter
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

from trafficlaw.llm.parallel import map_parallel
from trafficlaw.llm.types import QuotaExhaustedError
from trafficlaw.pipeline.answer import AnswerContext, AnswerResult, answer
from trafficlaw.retrieval.retrieve import RetrievalResult
from trafficlaw.utils.jsonl import JsonlWriter, done_keys, read_jsonl

logger = logging.getLogger(__name__)

KEY_FIELDS = ("config_name", "qid", "model_id", "prompt_hash")
DONE_STATUSES = ("ok", "format_error")


@dataclass(frozen=True)
class Query:
    qid: str
    question: str
    as_of: date | None


@dataclass
class RunStats:
    n_total: int = 0
    n_skipped: int = 0
    n_written: int = 0
    statuses: Counter[str] = field(default_factory=Counter)
    stopped: str | None = None


def done_answer_keys(path: str | Path) -> set[tuple[Any, ...]]:
    return done_keys(path, KEY_FIELDS, where=lambda r: r.get("status") in DONE_STATUSES)


def latest_results(path: str | Path) -> dict[tuple[Any, ...], dict[str, Any]]:
    """Bản ghi mới nhất theo khoá (bản ``ok``/``format_error`` thắng ``error`` cũ)."""
    out: dict[tuple[Any, ...], dict[str, Any]] = {}
    for r in read_jsonl(path):
        k = tuple(r.get(f) for f in KEY_FIELDS)
        prev = out.get(k)
        if (
            prev is None
            or prev.get("status") not in DONE_STATUSES
            or r.get("status") in (DONE_STATUSES)
        ):
            out[k] = r
    return out


def run_answers(
    queries: Sequence[Query],
    config_name: str,
    ctx: AnswerContext,
    out_path: str | Path,
    *,
    retrievals: Mapping[str, RetrievalResult] | None = None,
    workers: int = 1,
    use_llm_analyzer: bool = True,
    progress: Callable[[int, int], None] | None = None,
) -> RunStats:
    """Trả lời các câu chưa có kết quả xong; ghi ``AnswerResult`` vào ``out_path``."""
    st = RunStats(n_total=len(queries))
    ph = ctx.prompt_hash(config_name)
    done = done_answer_keys(out_path)
    todo = [q for q in queries if (config_name, q.qid, ctx.model_id, ph) not in done]
    st.n_skipped = len(queries) - len(todo)
    jobs: list[tuple[Query, RetrievalResult | None]] = []
    for q in todo:
        r = None
        if not ctx.is_no_rag(config_name):
            r = (retrievals or {}).get(q.qid)
            if r is None:
                if ctx.retrieval is None:
                    raise ValueError(
                        f"{q.qid}: thiếu kết quả truy hồi và không có RetrievalContext"
                    )
                r = ctx.retrieval.retrieve(
                    q.question, q.as_of, config_name, qid=q.qid, use_llm=use_llm_analyzer
                )
        jobs.append((q, r))

    def work(job: tuple[Query, RetrievalResult | None]) -> AnswerResult:
        q, r = job
        return answer(q.question, q.as_of, config_name, ctx, qid=q.qid, retrieval=r)

    with JsonlWriter(out_path) as w:
        for i, (_job, res) in enumerate(map_parallel(jobs, work, workers), 1):
            if isinstance(res, QuotaExhaustedError):
                st.stopped = str(res)
                break
            w.write(res.model_dump(mode="json"))
            st.n_written += 1
            st.statuses[res.status] += 1
            if progress:
                progress(i, len(jobs))
    return st


# --------------------------------------------------------------------------- cache demo


def normalize_question(q: str) -> str:
    s = unicodedata.normalize("NFC", q).lower()
    return re.sub(r"\s+", " ", s).strip()


def demo_key(
    question: str,
    as_of: date | None,
    config_name: str,
    model_id: str,
    prompt_hash: str,
    data_version: str | None,
) -> str:
    raw = "\x1f".join(
        [
            normalize_question(question),
            as_of.isoformat() if as_of else "",
            config_name,
            model_id,
            prompt_hash,
            data_version or "",
        ]
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


class AnswerCache:
    """Cache câu trả lời cho demo (M15): chỉ lưu ``status = ok``."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self._d: dict[str, dict[str, Any]] = {}
        for r in read_jsonl(self.path):
            self._d[str(r["key"])] = r["result"]

    def get(self, key: str) -> AnswerResult | None:
        r = self._d.get(key)
        return AnswerResult.model_validate(r) if r is not None else None

    def put(self, key: str, res: AnswerResult) -> None:
        if res.status != "ok":
            return
        rec = {"key": key, "result": res.model_dump(mode="json")}
        self._d[key] = rec["result"]
        with JsonlWriter(self.path) as w:
            w.write(rec)


def answer_cached(
    question: str,
    as_of: date | None,
    config_name: str,
    ctx: AnswerContext,
    cache: AnswerCache,
) -> tuple[AnswerResult, bool]:
    """Demo: trả từ cache nếu có (khoá gồm ``as_of`` tham số — ``None`` = hôm nay của ctx)."""
    eff = as_of or ctx.today
    key = demo_key(
        question, eff, config_name, ctx.model_id, ctx.prompt_hash(config_name), ctx.data_version
    )
    hit = cache.get(key)
    if hit is not None:
        return hit, True
    res = answer(question, eff, config_name, ctx)
    cache.put(key, res)
    return res, False


__all__ = [
    "DONE_STATUSES",
    "KEY_FIELDS",
    "AnswerCache",
    "Query",
    "RunStats",
    "answer_cached",
    "demo_key",
    "done_answer_keys",
    "latest_results",
    "normalize_question",
    "run_answers",
]
