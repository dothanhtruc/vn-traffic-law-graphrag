"""LLM judge (M13): chấm độ đúng câu trả lời so với đáp án tham chiếu của test.

- Model judge **khác họ** với model sinh (mục 10; ``check_judge_model``), tự host, temperature 0,
  cache LLM (M7). Prompt ``llm/prompts/judge.md``: câu hỏi + ngày áp dụng + đáp án tham chiếu + câu
  trả lời đã render (**không** có tên cấu hình, đã bỏ nhãn trích dẫn ``[...]`` để B0 và RAG trình
  bày giống nhau).
- Đầu ra ``JudgeOut{diem 0|1|2, dung, thieu[], sai[], ly_do}``; ``dung`` lưu theo LLM nhưng điểm
  dùng để tính là ``diem == 2`` (lệch → cờ ``dung_khong_khop``).
- **Luật tất định, không gọi LLM** (``judge_source = rule``): câu ``ngoai_pham_vi`` → 2 nếu hệ
  thống từ chối, 0 nếu không; câu trả lời ``format_error`` → 0; hệ thống từ chối câu có gold → 0.
- Khoá resume ``(config_name, qid, judge_model_id, judge_prompt_hash, answer_hash)`` —
  ``answer_hash`` = sha256(trạng thái + câu trả lời render) ⇒ câu trả lời đổi thì chấm lại.
  ``ok``/``format_error`` là xong; ``error`` (mạng/hết retry) chạy lại, không tính.
  ``format_error`` của judge (JSON hỏng sau lượt sửa) **không** tính vào độ đúng (không phải lỗi
  của hệ thống được chấm), đếm riêng trong báo cáo.
"""

from __future__ import annotations

import hashlib
import logging
import re
from collections import Counter
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from trafficlaw.eval.answer_metrics import REFUSALS, GoldItem
from trafficlaw.graph.store import canonical_json
from trafficlaw.llm.parallel import map_parallel
from trafficlaw.llm.prompt_loader import Prompt
from trafficlaw.llm.types import QuotaExhaustedError, Usage
from trafficlaw.pipeline.answer import AnswerResult
from trafficlaw.utils.jsonl import JsonlWriter, done_keys, read_jsonl

logger = logging.getLogger(__name__)

JUDGE_KEY_FIELDS = ("config_name", "qid", "judge_model_id", "judge_prompt_hash", "answer_hash")
DONE = ("ok", "format_error")
_CITE = re.compile(r"\s*\[[^\]]*\]")


class JudgeOut(BaseModel):
    model_config = ConfigDict(extra="forbid")
    diem: Literal[0, 1, 2]
    dung: bool
    thieu: list[str] = Field(default_factory=list, max_length=8)
    sai: list[str] = Field(default_factory=list, max_length=8)
    ly_do: str = ""


class JudgeRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")
    run_id: str
    config_name: str
    qid: str
    judge_model_id: str
    judge_prompt_hash: str
    answer_hash: str
    status: Literal["ok", "error", "format_error"]
    judge_source: Literal["llm", "rule"]
    diem: int | None = None
    dung: bool | None = None
    """``diem == 2`` (không lấy trường ``dung`` của LLM)."""
    dung_llm: bool | None = None
    flags: list[str] = Field(default_factory=list)
    thieu: list[str] = Field(default_factory=list)
    sai: list[str] = Field(default_factory=list)
    ly_do: str = ""
    error: str | None = None
    usage: Usage = Field(default_factory=Usage)
    latency_ms: int = 0
    cached: bool = False
    serve: dict[str, Any] | None = None
    git_commit: str | None = None
    timestamp: str


def render_for_judge(res: AnswerResult) -> str:
    """Câu trả lời như người đọc thấy, bỏ nhãn trích dẫn (ẩn khác biệt trình bày B0/RAG)."""
    lines = [_CITE.sub("", ln).rstrip() for ln in (res.answer or "").splitlines()]
    text = "\n".join(ln for ln in lines if ln.strip())
    return text or "(không có nội dung)"


def answer_hash(res: AnswerResult) -> str:
    raw = f"{res.status}\x1f{res.answer_status}\x1f{render_for_judge(res)}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def judge_messages(prompt: Prompt, item: GoldItem, res: AnswerResult) -> list[dict[str, str]]:
    status = {
        "answered": "trả lời",
        "insufficient": "từ chối — không đủ căn cứ",
        "out_of_scope": "từ chối — ngoài phạm vi",
    }.get(str(res.answer_status), "không rõ")
    msg = prompt.render(
        as_of=item.as_of.strftime("%d/%m/%Y"),
        question=item.question,
        reference=item.answer or "",
        answer_status=status,
        answer=render_for_judge(res),
    )
    return [{"role": "user", "content": msg}]


def rule_verdict(item: GoldItem, res: AnswerResult) -> tuple[int, str] | None:
    """(điểm, lý do) khi chấm được bằng luật; ``None`` → gọi LLM."""
    refused = res.status == "ok" and res.answer_status in REFUSALS
    if item.question_type == "ngoai_pham_vi":
        return (
            (2, "ngoài phạm vi, hệ thống từ chối")
            if refused
            else (0, "ngoài phạm vi, hệ thống trả lời")
        )
    if res.status == "format_error":
        return 0, "câu trả lời format_error"
    if refused and item.gold_units:
        return 0, "từ chối câu hỏi có điều khoản trả lời"
    return None


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


@dataclass
class JudgeContext:
    client: Any
    prompt: Prompt
    model_id: str
    run_id: str = "adhoc"
    serve: dict[str, Any] | None = None
    git_commit: str | None = None
    max_output_tokens: int = 1024

    @property
    def prompt_hash(self) -> str:
        """sha256(prompt + JSON schema + max_output_tokens) — đổi bất kỳ ⇒ chấm lại."""
        raw = canonical_json(
            {
                "prompt": self.prompt.hash,
                "schema": JudgeOut.model_json_schema(),
                "max_output_tokens": self.max_output_tokens,
            }
        )
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def judge_one(item: GoldItem, res: AnswerResult, jctx: JudgeContext) -> JudgeRecord:
    base: dict[str, Any] = {
        "run_id": jctx.run_id,
        "config_name": res.config_name,
        "qid": item.qid,
        "judge_model_id": jctx.model_id,
        "judge_prompt_hash": jctx.prompt_hash,
        "answer_hash": answer_hash(res),
        "serve": jctx.serve,
        "git_commit": jctx.git_commit,
        "timestamp": _now(),
    }
    rv = rule_verdict(item, res)
    if rv is not None:
        d, why = rv
        return JudgeRecord(**base, status="ok", judge_source="rule", diem=d, dung=d == 2, ly_do=why)
    out = jctx.client.generate(
        judge_messages(jctx.prompt, item, res),
        json_schema=JudgeOut,
        params={"max_output_tokens": jctx.max_output_tokens},
    )
    common = {
        "usage": out.usage,
        "latency_ms": out.latency_ms,
        "cached": out.cached,
        "judge_source": "llm",
    }
    if out.status != "ok" or out.parsed is None:
        return JudgeRecord(**base, **common, status=out.status, error=out.error)
    j = JudgeOut.model_validate(out.parsed)
    flags = [] if j.dung == (j.diem == 2) else ["dung_khong_khop"]
    return JudgeRecord(
        **base,
        **common,
        status="ok",
        diem=j.diem,
        dung=j.diem == 2,
        dung_llm=j.dung,
        flags=flags,
        thieu=j.thieu,
        sai=j.sai,
        ly_do=j.ly_do,
    )


@dataclass
class JudgeStats:
    n_total: int = 0
    n_skipped: int = 0
    n_written: int = 0
    statuses: Counter[str] = field(default_factory=Counter)
    stopped: str | None = None


def judge_key(rec: Mapping[str, Any]) -> tuple[Any, ...]:
    return tuple(rec.get(f) for f in JUDGE_KEY_FIELDS)


def run_judge(
    pairs: Sequence[tuple[GoldItem, AnswerResult]],
    jctx: JudgeContext,
    out_path: str | Path,
    *,
    workers: int = 1,
    progress: Callable[[int, int], None] | None = None,
) -> JudgeStats:
    st = JudgeStats(n_total=len(pairs))
    done = done_keys(out_path, JUDGE_KEY_FIELDS, where=lambda r: r.get("status") in DONE)
    todo = [
        (it, r)
        for it, r in pairs
        if (r.config_name, it.qid, jctx.model_id, jctx.prompt_hash, answer_hash(r)) not in done
    ]
    st.n_skipped = len(pairs) - len(todo)
    with JsonlWriter(out_path) as w:
        for i, (_job, rec) in enumerate(
            map_parallel(todo, lambda p: judge_one(p[0], p[1], jctx), workers), 1
        ):
            if isinstance(rec, QuotaExhaustedError):
                st.stopped = str(rec)
                break
            w.write(rec.model_dump(mode="json"))
            st.n_written += 1
            st.statuses[rec.status] += 1
            if progress:
                progress(i, len(todo))
    return st


def latest_judgements(
    path: str | Path, *, model_id: str, prompt_hash: str
) -> dict[tuple[str, str], JudgeRecord]:
    """(qid, answer_hash) → bản ghi mới nhất (bản xong thắng ``error``) của judge này."""
    out: dict[tuple[str, str], JudgeRecord] = {}
    for r in read_jsonl(path):
        if r.get("judge_model_id") != model_id or r.get("judge_prompt_hash") != prompt_hash:
            continue
        k = (str(r["qid"]), str(r["answer_hash"]))
        prev = out.get(k)
        if prev is None or prev.status not in DONE or r.get("status") in DONE:
            out[k] = JudgeRecord.model_validate(r)
    return out


class JudgeModelError(ValueError):
    pass


def check_judge_model(
    judge_model: str, main_model: str, family_of: Callable[[str], str | None]
) -> str:
    """Judge phải khác model và khác họ với model sinh (họ không biết → từ chối)."""
    if judge_model == main_model:
        raise JudgeModelError(f"judge {judge_model} trùng model sinh câu trả lời")
    fj, fm = family_of(judge_model), family_of(main_model)
    if fj is None or fm is None:
        raise JudgeModelError(
            f"không biết họ model (judge {judge_model}: {fj}, sinh {main_model}: {fm})"
            " — khai báo `family` trong configs/serve.yaml"
        )
    if fj == fm:
        raise JudgeModelError(f"judge {judge_model} cùng họ {fj} với model sinh {main_model}")
    return fj


__all__ = [
    "JUDGE_KEY_FIELDS",
    "JudgeContext",
    "JudgeModelError",
    "JudgeOut",
    "JudgeRecord",
    "JudgeStats",
    "answer_hash",
    "check_judge_model",
    "judge_key",
    "judge_messages",
    "judge_one",
    "latest_judgements",
    "render_for_judge",
    "rule_verdict",
    "run_judge",
]
