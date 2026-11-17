"""Sinh câu trả lời + kiểm con số/trích dẫn (M12): ``answer()`` dùng chung cho M13 (giai đoạn
``generate``) và M15 (demo).

Luồng cấu hình RAG (B1, B2, B3, G, A1–A3)::

    retrieve() (M11)                      → hits top-5, pool
    select_sources (+ ≤3 chunk đồ thị)    → S1…Sk, nguyên văn đúng trạng thái
    build_number_table                    → N1…Nm (CheTai/DiemGPLX/BPBS + số trong text)
    LLM main (JSON AnswerOut)             → points[{text có {N#}, sources [S#/điểm], numbers}]
    dò số tự do / mã lạ                   → có vi phạm: 1 lượt sửa (answer_number_repair)
    còn vi phạm                           → bỏ câu chứa số, cờ so_khong_kiem_duoc
    kiểm trích dẫn                        → bỏ trích dẫn sai, bỏ ý không còn nguồn
    render {N#} → giá trị                 → answer (chuỗi), citations (unit_id), numbers

B0 (không RAG): prompt ``answer_no_rag``, LLM viết số tự do (mọi số đánh dấu
``khong_kiem_duoc``), trích dẫn tự khai ``{van_ban, dieu, khoan, diem}`` chỉ đối chiếu với đồ thị
để thống kê trích dẫn bịa.

``status`` (mục 10): ``ok`` | ``error`` (lỗi mạng/hết retry — không tính là sai, lần sau chạy
lại) | ``format_error`` (JSON hỏng sau 1 lượt sửa định dạng — tính là sai). ``answer_status``:
``answered`` | ``insufficient`` | ``out_of_scope`` do LLM chọn.
"""

from __future__ import annotations

import hashlib
import logging
import re
from collections.abc import Sequence
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from trafficlaw.graph.store import BaseGraphStore, canonical_json
from trafficlaw.llm.prompt_loader import Prompt, load_prompt
from trafficlaw.llm.types import LLMResult, Usage
from trafficlaw.pipeline.context import (
    ContextConfig,
    Source,
    render_number_table,
    render_sources,
    select_sources,
)
from trafficlaw.retrieval.catalog import ChunkCatalog
from trafficlaw.retrieval.retrieve import RetrievalContext, RetrievalResult
from trafficlaw.verify.citations import (
    Citation,
    FreeCitationIn,
    SoHieuTable,
    resolve_citation,
    resolve_free_citation,
)
from trafficlaw.verify.numbers import (
    AllowedNumbers,
    NumberFact,
    NumberIndex,
    NumberIssue,
    build_number_table,
    drop_sentences,
    find_unverified_numbers,
    placeholders,
    render_numbers,
    unknown_placeholders,
)

logger = logging.getLogger(__name__)

AnswerStatus = Literal["answered", "insufficient", "out_of_scope"]
MAX_POINTS = 8


# --------------------------------------------------------------------------- cấu hình


class NumbersConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    max_text_numbers_per_source: int = 25
    text_chars_budget: int = 4000
    """Tổng ký tự (mô tả + giá trị) cho số trong text của mọi nguồn; nút chế tài luôn có mặt."""
    repair: bool = True


class RefusalConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    tau: float | None = None
    """Điểm rerank top-1 < τ → thêm lưu ý khả năng thiếu nguồn vào prompt (null = tắt)."""
    note: str = (
        "Lưu ý: các nguồn dưới đây có độ liên quan thấp với câu hỏi. Kiểm tra kỹ; nếu không nguồn"
        " nào trả lời được câu hỏi thì chọn `insufficient` (hoặc `out_of_scope` nếu câu hỏi không"
        " thuộc giao thông đường bộ)."
    )


class AnswerEvalConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    val: str = "data/qa/val.jsonl"
    dev_out_of_scope: str = "data/qa/dev_out_of_scope.jsonl"
    retrieval_from: str = "data/index/retrieval_eval"
    results_dir: str = "results"
    out_dir: str = "data/answer"
    run_id: str = "m12-dev"
    sample_n: int | None = None
    seed: int = 42
    review_n: int = 30
    output_tokens_estimate: int = 350


class AnswerConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    prompt: str = "answer"
    prompt_no_rag: str = "answer_no_rag"
    number_repair_prompt: str = "answer_number_repair"
    no_rag_config: str = "B0"
    max_output_tokens: int = 1536
    max_points: int = Field(6, ge=1, le=MAX_POINTS)
    context: ContextConfig = Field(default_factory=ContextConfig)
    numbers: NumbersConfig = Field(default_factory=NumbersConfig)
    refusal: RefusalConfig = Field(default_factory=RefusalConfig)
    eval: AnswerEvalConfig = Field(default_factory=AnswerEvalConfig)

    def behaviour_dump(self) -> dict[str, Any]:
        """Phần cấu hình ảnh hưởng tới prompt/kết quả (vào ``prompt_hash``)."""
        return self.model_dump(exclude={"eval"})


def load_answer_config(path: str | Path) -> AnswerConfig:
    return AnswerConfig.model_validate(yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {})


# --------------------------------------------------------------------------- schema LLM


class PointOut(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str
    sources: list[str] = Field(default_factory=list, max_length=6)
    numbers: list[str] = Field(default_factory=list, max_length=12)


class AnswerOut(BaseModel):
    """Đầu ra LLM cho cấu hình RAG."""

    model_config = ConfigDict(extra="forbid")
    status: AnswerStatus
    points: list[PointOut] = Field(default_factory=list, max_length=MAX_POINTS)
    conclusion: str = ""


class PointNoRag(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str
    citations: list[FreeCitationIn] = Field(default_factory=list, max_length=6)


class AnswerOutNoRag(BaseModel):
    """Đầu ra LLM cho B0."""

    model_config = ConfigDict(extra="forbid")
    status: AnswerStatus
    points: list[PointNoRag] = Field(default_factory=list, max_length=MAX_POINTS)
    conclusion: str = ""


# --------------------------------------------------------------------------- kết quả


class VerifyIssue(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: str
    where: str
    """``p<i>`` (ý thứ i, từ 0) | ``conclusion``."""
    detail: str = ""


class VerifyReport(BaseModel):
    model_config = ConfigDict(extra="forbid")
    numbers_verifiable: bool
    """False với B0 (không có bảng con số)."""
    issues: list[VerifyIssue] = Field(default_factory=list)
    flags: list[str] = Field(default_factory=list)
    n_points_raw: int = 0
    n_points_kept: int = 0
    n_citations: int = 0
    n_citations_valid: int = 0
    n_numbers_used: int = 0
    n_violations_before: int = 0
    """Số tự do / mã lạ ở phản hồi đầu."""
    n_violations_after_repair: int | None = None
    repaired: bool = False
    repair_status: str | None = None
    dropped_sentences: int = 0
    n_free_numbers: int = 0
    """B0: số chuỗi số không kiểm được."""


class PointResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str
    """Đã điền con số."""
    raw_text: str
    citations: list[Citation]
    numbers: list[str]


class NumberUse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    rendered: str
    values: list[str]
    unit: str | None
    kind: str
    source: str
    unit_id: str
    version_id: str | None
    node_id: str | None


class SourceRef(BaseModel):
    """Nguồn đã đưa vào ngữ cảnh (không chép toàn văn — tra lại bằng ``chunk_id``)."""

    model_config = ConfigDict(extra="forbid")
    sid: str
    chunk_id: str
    unit_id: str
    doc_id: str
    version_ids: list[str]
    effective_from: date
    effective_to: date | None
    origin: str
    rank: int | None
    score: float | None
    edge_type: str | None
    label: str
    doc_label: str
    in_effect: bool
    truncated: bool
    amendments: list[str] = Field(default_factory=list)


class HitRef(BaseModel):
    model_config = ConfigDict(extra="forbid")
    chunk_id: str
    rank: int
    score: float


class RetrievalRef(BaseModel):
    model_config = ConfigDict(extra="forbid")
    config_name: str
    as_of: date
    as_of_param: date | None
    as_of_source: str
    validity_filter: bool
    question_type: str | None
    hits: list[HitRef]
    has_reranker: bool
    top1_score: float | None
    n_pool: int
    data_version: str | None
    catalog_sha256: str | None
    graph_data_hash: str | None
    llm_model: str | None
    prompt_hash: str | None


class AnswerResult(BaseModel):
    """Một câu trả lời — ghi JSONL (M13). Khoá resume ``(config_name, qid, model_id,
    prompt_hash)``."""

    model_config = ConfigDict(extra="forbid")
    run_id: str
    config_name: str
    qid: str | None
    question: str
    as_of: date
    as_of_param: date | None
    validity_filter: bool
    retrieval: RetrievalRef | None
    sources: list[SourceRef]
    number_table: list[NumberFact]
    low_retrieval_score: bool | None = None
    llm_text: str = ""
    llm_output: Any = None
    repair_text: str | None = None
    repair_output: Any = None
    answer: str = ""
    points: list[PointResult] = Field(default_factory=list)
    conclusion: str = ""
    citations: list[Citation] = Field(default_factory=list)
    numbers: list[NumberUse] = Field(default_factory=list)
    verify: VerifyReport
    status: Literal["ok", "error", "format_error"]
    answer_status: AnswerStatus | None = None
    error: str | None = None
    model_id: str
    serve: dict[str, Any] | None = None
    prompt_hash: str
    """Hash tổng: prompt chính + prompt sửa số + prompt sửa định dạng + cấu hình ``answer.yaml``
    (trừ ``eval``) + schema."""
    answer_prompt_hash: str
    repair_prompt_hash: str | None = None
    usage: Usage = Field(default_factory=Usage)
    latency_ms: int = 0
    attempts: int = 0
    cached: bool = False
    n_llm_calls: int = 0
    git_commit: str | None = None
    data_version: str | None = None
    timestamp: str
    llm_params: dict[str, Any] | None = None
    """Tham số LLM ghi đè của lần chạy (M13 dao động: ``{"seed": 43}``); ``None`` = mặc định."""


# --------------------------------------------------------------------------- ngữ cảnh chạy


class AnswerContext:
    """Nạp một lần: cấu hình, đồ thị, danh mục chunk, ngữ cảnh truy hồi (M11), client LLM,
    prompt, chỉ mục con số."""

    def __init__(
        self,
        cfg: AnswerConfig,
        *,
        store: BaseGraphStore,
        catalog: ChunkCatalog,
        retrieval: RetrievalContext | None,
        client: Any | None,
        model_id: str | None = None,
        today: date,
        run_id: str = "adhoc",
        git_commit: str | None = None,
        data_version: str | None = None,
        serve: dict[str, Any] | None = None,
        budget_profile: Literal["default", "shared"] = "default",
        prompts: dict[str, Prompt] | None = None,
        llm_params: dict[str, Any] | None = None,
        use_cache: bool = True,
    ) -> None:
        self.cfg = cfg
        self.llm_params = dict(llm_params or {})
        """Tham số LLM ghi đè (M13 đo dao động: ``seed``); ghi vào ``AnswerResult.llm_params``."""
        self.use_cache = use_cache
        self.store = store
        self.catalog = catalog
        self.retrieval = retrieval
        self.client = client
        self.model_id = model_id or (client.model_id if client is not None else "unknown")
        self.today = today
        self.run_id = run_id
        self.git_commit = git_commit
        self.data_version = data_version
        self.serve = serve
        self.budget = (
            cfg.context.token_budget_shared
            if budget_profile == "shared"
            else cfg.context.token_budget
        )
        self.budget_profile = budget_profile
        p = prompts or {}
        self.prompt = p.get("answer") or load_prompt(cfg.prompt)
        self.prompt_no_rag = p.get("no_rag") or load_prompt(cfg.prompt_no_rag)
        self.number_repair = p.get("number_repair") or load_prompt(cfg.number_repair_prompt)
        self.numbers = NumberIndex(store)
        self.so_hieu = SoHieuTable(store)
        self.docs = {n.id: dict(n.props) for n in store.nodes_by_label("VanBan")}

    def is_no_rag(self, config_name: str) -> bool:
        return config_name == self.cfg.no_rag_config

    def format_repair_hash(self) -> str | None:
        rp = getattr(self.client, "repair_prompt", None)
        return getattr(rp, "hash", None)

    def prompt_hash(self, config_name: str) -> str:
        schema = AnswerOutNoRag if self.is_no_rag(config_name) else AnswerOut
        main = self.prompt_no_rag if self.is_no_rag(config_name) else self.prompt
        return hashlib.sha256(
            canonical_json(
                {
                    "prompt": main.hash,
                    "number_repair": None
                    if self.is_no_rag(config_name)
                    else self.number_repair.hash,
                    "format_repair": self.format_repair_hash(),
                    "cfg": self.cfg.behaviour_dump(),
                    "budget_profile": self.budget_profile,
                    "schema": schema.model_json_schema(),
                }
            ).encode("utf-8")
        ).hexdigest()


# --------------------------------------------------------------------------- chuẩn bị prompt


class Prepared(BaseModel):
    """Prompt đã dựng (dùng cho ``answer`` và ``--dry-run``)."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    config_name: str
    as_of: date
    as_of_param: date | None
    validity_filter: bool
    retrieval: RetrievalResult | None
    sources: list[Source]
    table: list[NumberFact]
    low_score: bool | None
    allowed: Any
    messages: list[dict[str, str]]


def _retrieval_ref(r: RetrievalResult) -> RetrievalRef:
    return RetrievalRef(
        config_name=r.config_name,
        as_of=r.as_of,
        as_of_param=r.as_of_param,
        as_of_source=r.analysis.as_of_source,
        validity_filter=r.validity_filter,
        question_type=r.analysis.question_type,
        hits=[HitRef(chunk_id=h.chunk_id, rank=h.rank, score=h.score) for h in r.hits],
        has_reranker=r.reranker is not None,
        top1_score=r.hits[0].score if r.hits and r.reranker is not None else None,
        n_pool=len(r.pool),
        data_version=r.data_version,
        catalog_sha256=r.catalog_sha256,
        graph_data_hash=r.graph_data_hash,
        llm_model=r.llm_model,
        prompt_hash=r.prompt_hash,
    )


def _fmt_date(d: date) -> str:
    return d.strftime("%d/%m/%Y")


def prepare(
    question: str,
    as_of: date | None,
    config_name: str,
    ctx: AnswerContext,
    *,
    qid: str | None = None,
    retrieval: RetrievalResult | None = None,
    use_llm_analyzer: bool = True,
) -> Prepared:
    cfg = ctx.cfg
    if ctx.is_no_rag(config_name):
        eff = as_of or ctx.today
        msg = ctx.prompt_no_rag.render(
            as_of=_fmt_date(eff), question=question, max_points=str(cfg.max_points)
        )
        return Prepared(
            config_name=config_name,
            as_of=eff,
            as_of_param=as_of,
            validity_filter=False,
            retrieval=None,
            sources=[],
            table=[],
            low_score=None,
            allowed=AllowedNumbers.build(question, eff, [], []),
            messages=[{"role": "user", "content": msg}],
        )
    if retrieval is None:
        if ctx.retrieval is None:
            raise ValueError("cần RetrievalContext hoặc retrieval có sẵn")
        retrieval = ctx.retrieval.retrieve(
            question, as_of, config_name, qid=qid, use_llm=use_llm_analyzer
        )
    elif retrieval.config_name != config_name:
        raise ValueError(f"retrieval của {retrieval.config_name}, không phải {config_name}")
    eff = retrieval.as_of
    sources = select_sources(
        retrieval, ctx.catalog, ctx.store, cfg.context, docs=ctx.docs, budget=ctx.budget
    )
    table = build_number_table(
        [s.number_source(eff) for s in sources],
        ctx.numbers,
        max_text_numbers_per_source=cfg.numbers.max_text_numbers_per_source,
        text_chars_budget=cfg.numbers.text_chars_budget,
    )
    ref = _retrieval_ref(retrieval)
    tau = cfg.refusal.tau
    low = None
    if tau is not None and ref.top1_score is not None:
        low = ref.top1_score < tau
    if not retrieval.hits and tau is not None:
        low = True
    note = f"\n{cfg.refusal.note}\n" if low else ""
    msg = ctx.prompt.render(
        as_of=_fmt_date(eff),
        question=question,
        sources=render_sources(sources),
        numbers=render_number_table(table),
        note=note,
        max_points=str(cfg.max_points),
    )
    extra_dates: list[date] = [eff]
    for s in sources:
        extra_dates.append(s.effective_from)
        if s.effective_to:
            extra_dates.append(s.effective_to)
        extra_dates += [a.effective_from for a in s.amendments if a.effective_from]
    allowed = AllowedNumbers.build(question, as_of, extra_dates, [s.text for s in sources])
    return Prepared(
        config_name=config_name,
        as_of=eff,
        as_of_param=as_of,
        validity_filter=retrieval.validity_filter,
        retrieval=retrieval,
        sources=sources,
        table=table,
        low_score=low,
        allowed=allowed,
        messages=[{"role": "user", "content": msg}],
    )


# --------------------------------------------------------------------------- kiểm con số


def scan_numbers(
    out: AnswerOut, table: dict[str, NumberFact], allowed: AllowedNumbers
) -> dict[str, list[NumberIssue]]:
    """Vi phạm theo vị trí (``p<i>`` / ``conclusion``)."""
    res: dict[str, list[NumberIssue]] = {}
    parts = [(f"p{i}", p.text) for i, p in enumerate(out.points)] + [("conclusion", out.conclusion)]
    for where, text in parts:
        iss = find_unverified_numbers(text, allowed) + unknown_placeholders(text, table)
        if iss:
            res[where] = sorted(iss, key=lambda x: x.start)
    return res


def _n(viol: dict[str, list[NumberIssue]]) -> int:
    return sum(len(v) for v in viol.values())


def _parse(schema: type[BaseModel], res: LLMResult) -> BaseModel | None:
    if res.parsed is None:
        return None
    try:
        return schema.model_validate(res.parsed)
    except ValidationError:  # pragma: no cover - client đã validate
        return None


def _add_usage(a: Usage, b: Usage) -> Usage:
    return Usage(
        prompt_tokens=a.prompt_tokens + b.prompt_tokens,
        completion_tokens=a.completion_tokens + b.completion_tokens,
        total_tokens=a.total_tokens + b.total_tokens,
        estimated=a.estimated or b.estimated,
    )


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def _source_refs(sources: Sequence[Source]) -> list[SourceRef]:
    return [
        SourceRef(
            sid=s.sid,
            chunk_id=s.chunk_id,
            unit_id=s.unit_id,
            doc_id=s.doc_id,
            version_ids=s.version_ids,
            effective_from=s.effective_from,
            effective_to=s.effective_to,
            origin=s.origin,
            rank=s.rank,
            score=s.score,
            edge_type=s.edge_type,
            label=s.label,
            doc_label=s.doc_label,
            in_effect=s.in_effect,
            truncated=s.truncated,
            amendments=[f"{a.edge_type}:{a.doc_id}:{a.effective_from}" for a in s.amendments],
        )
        for s in sources
    ]


def render_answer(
    points: Sequence[PointResult], conclusion: str, *, show_invalid: bool = False
) -> str:
    """Chuỗi hiển thị/chấm: mỗi ý một dòng kèm nhãn trích dẫn hợp lệ (B0: mọi trích dẫn tự khai,
    ``show_invalid``), rồi kết luận."""
    lines = []
    for p in points:
        cs = [c for c in p.citations if show_invalid or c.valid]
        cites = "; ".join(dict.fromkeys(c.label or c.ref for c in cs))
        lines.append(f"- {p.text}" + (f" [{cites}]" if cites else ""))
    if conclusion:
        lines.append(f"Kết luận: {conclusion}" if points else conclusion)
    return "\n".join(lines)


# --------------------------------------------------------------------------- answer()


def answer(
    question: str,
    as_of: date | None,
    config_name: str,
    ctx: AnswerContext,
    *,
    qid: str | None = None,
    retrieval: RetrievalResult | None = None,
    use_llm_analyzer: bool = True,
) -> AnswerResult:
    """Trả lời một câu hỏi theo cấu hình ``config_name`` (B0 hoặc cấu hình truy hồi của M11).
    ``retrieval`` có sẵn (M13 tách giai đoạn) thì không gọi ``retrieve()``."""
    if ctx.client is None:
        raise ValueError("AnswerContext không có client LLM")
    prep = prepare(
        question,
        as_of,
        config_name,
        ctx,
        qid=qid,
        retrieval=retrieval,
        use_llm_analyzer=use_llm_analyzer,
    )
    no_rag = ctx.is_no_rag(config_name)
    schema: type[BaseModel] = AnswerOutNoRag if no_rag else AnswerOut
    params = {"max_output_tokens": ctx.cfg.max_output_tokens, **ctx.llm_params}
    res: LLMResult = ctx.client.generate(
        prep.messages, json_schema=schema, params=params, use_cache=ctx.use_cache
    )
    base = {
        "run_id": ctx.run_id,
        "config_name": config_name,
        "qid": qid,
        "question": question,
        "as_of": prep.as_of,
        "as_of_param": as_of,
        "validity_filter": prep.validity_filter,
        "retrieval": _retrieval_ref(prep.retrieval) if prep.retrieval else None,
        "sources": _source_refs(prep.sources),
        "number_table": prep.table,
        "low_retrieval_score": prep.low_score,
        "model_id": ctx.model_id,
        "serve": ctx.serve,
        "prompt_hash": ctx.prompt_hash(config_name),
        "answer_prompt_hash": (ctx.prompt_no_rag if no_rag else ctx.prompt).hash,
        "git_commit": ctx.git_commit,
        "data_version": ctx.data_version,
        "timestamp": _now(),
        "llm_params": ctx.llm_params or None,
    }
    usage, latency, attempts, cached, n_calls = (
        res.usage,
        res.latency_ms,
        res.attempts,
        res.cached,
        1,
    )
    if res.status != "ok":
        return AnswerResult(
            **base,
            llm_text=res.text,
            verify=VerifyReport(numbers_verifiable=not no_rag),
            status=res.status,
            error=res.error,
            repair_prompt_hash=res.repair_prompt_hash,
            usage=usage,
            latency_ms=latency,
            attempts=attempts,
            cached=cached,
            n_llm_calls=n_calls,
        )
    out = _parse(schema, res)
    assert out is not None
    if no_rag:
        assert isinstance(out, AnswerOutNoRag)
        return _finish_no_rag(base, out, res, prep, ctx)

    assert isinstance(out, AnswerOut)
    tmap = {f.id: f for f in prep.table}
    report = VerifyReport(numbers_verifiable=True, n_points_raw=len(out.points))
    viol = scan_numbers(out, tmap, prep.allowed)
    report.n_violations_before = _n(viol)
    repair_text: str | None = None
    repair_output: Any = None
    if viol and ctx.cfg.numbers.repair:
        lines = [
            f"- {w}: " + ", ".join(f"«{i.text}»" for i in iss) for w, iss in sorted(viol.items())
        ]
        msg = ctx.number_repair.render(violations="\n".join(lines))
        msgs2 = [
            *prep.messages,
            {"role": "assistant", "content": res.text},
            {"role": "user", "content": msg},
        ]
        res2: LLMResult = ctx.client.generate(
            msgs2, json_schema=AnswerOut, params=params, use_cache=ctx.use_cache
        )
        n_calls += 1
        usage = _add_usage(usage, res2.usage)
        latency += res2.latency_ms
        attempts += res2.attempts
        cached = cached and res2.cached
        report.repaired = True
        report.repair_status = res2.status
        repair_text = res2.text
        out2 = _parse(AnswerOut, res2) if res2.status == "ok" else None
        if isinstance(out2, AnswerOut):
            repair_output = res2.parsed
            out = out2
            report.n_points_raw = len(out.points)
            viol = scan_numbers(out, tmap, prep.allowed)
        report.n_violations_after_repair = _n(viol)
    points, conclusion = _verify_rag(out, viol, tmap, prep, ctx, report)
    used = list(dict.fromkeys(n for p in points for n in p.numbers))
    numbers = [
        NumberUse(
            id=n,
            rendered=tmap[n].rendered,
            values=tmap[n].values,
            unit=tmap[n].unit,
            kind=tmap[n].kind,
            source=tmap[n].source,
            unit_id=tmap[n].unit_id,
            version_id=tmap[n].version_id,
            node_id=tmap[n].node_id,
        )
        for n in used
        if n in tmap
    ]
    report.n_numbers_used = len(numbers)
    report.flags = sorted({i.code for i in report.issues})
    return AnswerResult(
        **base,
        llm_text=res.text,
        llm_output=res.parsed,
        repair_text=repair_text,
        repair_output=repair_output,
        answer=render_answer(points, conclusion),
        points=points,
        conclusion=conclusion,
        citations=[c for p in points for c in p.citations if c.valid],
        numbers=numbers,
        verify=report,
        status="ok",
        answer_status=out.status,
        repair_prompt_hash=res.repair_prompt_hash,
        usage=usage,
        latency_ms=latency,
        attempts=attempts,
        cached=cached,
        n_llm_calls=n_calls,
    )


def _verify_rag(
    out: AnswerOut,
    viol: dict[str, list[NumberIssue]],
    tmap: dict[str, NumberFact],
    prep: Prepared,
    ctx: AnswerContext,
    report: VerifyReport,
) -> tuple[list[PointResult], str]:
    facts_by_sid: dict[str, set[str]] = {}
    for f in prep.table:
        if f.unit_id and f.kind != "van_ban":
            facts_by_sid.setdefault(f.source, set()).add(f.unit_id)
    cites_by_sid = {s.sid: s.citable(facts_by_sid.get(s.sid, set())) for s in prep.sources}
    points: list[PointResult] = []
    for i, p in enumerate(out.points):
        where = f"p{i}"
        raw = p.text
        iss = viol.get(where, [])
        if iss:
            raw, nd = drop_sentences(raw, iss)
            report.dropped_sentences += nd
            for x in iss:
                report.issues.append(
                    VerifyIssue(code="so_khong_kiem_duoc", where=where, detail=f"{x.kind}:{x.text}")
                )
        if not raw.strip():
            report.issues.append(VerifyIssue(code="y_rong_sau_loc_so", where=where))
            continue
        cites = []
        for ref in p.sources:
            c = resolve_citation(
                ref, cites_by_sid, ctx.store, prep.as_of, validity_filter=prep.validity_filter
            )
            cites.append(c)
            report.n_citations += 1
            if c.valid:
                report.n_citations_valid += 1
            if c.status != "ok":
                report.issues.append(VerifyIssue(code=c.status, where=where, detail=ref))
        valid = [c for c in cites if c.valid]
        if not valid:
            report.issues.append(VerifyIssue(code="y_khong_nguon", where=where, detail=raw[:80]))
            continue
        used = placeholders(raw)
        for n in used:
            if len(re.findall(r"\{\s*" + n + r"\s*\}", raw)) > 1:
                # vd "từ {N4} đến {N4}": một khung phạt dùng làm cả hai đầu — chỉ gắn cờ
                report.issues.append(VerifyIssue(code="ma_so_lap", where=where, detail=n))
        sids = {c.sid for c in valid}
        for n in used:
            f = tmap.get(n)
            if f is not None and f.source not in sids:
                report.issues.append(
                    VerifyIssue(
                        code="so_khong_thuoc_nguon_trich", where=where, detail=f"{n}:{f.source}"
                    )
                )
        if set(used) != set(p.numbers):
            report.issues.append(
                VerifyIssue(
                    code="numbers_khong_khop",
                    where=where,
                    detail=f"text={used} numbers={p.numbers}",
                )
            )
        points.append(
            PointResult(text=render_numbers(raw, tmap), raw_text=raw, citations=cites, numbers=used)
        )
    concl = out.conclusion
    iss = viol.get("conclusion", [])
    if iss:
        concl, nd = drop_sentences(concl, iss)
        report.dropped_sentences += nd
        for x in iss:
            report.issues.append(
                VerifyIssue(
                    code="so_khong_kiem_duoc", where="conclusion", detail=f"{x.kind}:{x.text}"
                )
            )
    cited = {c.sid for p in points for c in p.citations if c.valid}
    for n in placeholders(concl):
        f = tmap.get(n)
        if f is not None and f.source not in cited:
            report.issues.append(
                VerifyIssue(code="so_khong_thuoc_nguon_trich", where="conclusion", detail=n)
            )
    if out.status == "answered" and not points:
        report.issues.append(VerifyIssue(code="khong_con_y_nao", where="answer"))
    report.n_points_kept = len(points)
    return points, render_numbers(concl, tmap)


def _finish_no_rag(
    base: dict[str, Any],
    out: AnswerOutNoRag,
    res: LLMResult,
    prep: Prepared,
    ctx: AnswerContext,
) -> AnswerResult:
    report = VerifyReport(numbers_verifiable=False, n_points_raw=len(out.points))
    points: list[PointResult] = []
    for i, p in enumerate(out.points):
        where = f"p{i}"
        cites = [resolve_free_citation(c, ctx.so_hieu, ctx.store, prep.as_of) for c in p.citations]
        for c in cites:
            report.n_citations += 1
            if c.valid:
                report.n_citations_valid += 1
            else:
                report.issues.append(VerifyIssue(code=c.status, where=where, detail=c.ref))
        if not cites:
            report.issues.append(VerifyIssue(code="y_khong_nguon", where=where))
        free = find_unverified_numbers(p.text, prep.allowed)
        report.n_free_numbers += len(free)
        for x in free:
            report.issues.append(
                VerifyIssue(code="so_khong_kiem_duoc", where=where, detail=f"{x.kind}:{x.text}")
            )
        points.append(PointResult(text=p.text, raw_text=p.text, citations=cites, numbers=[]))
    free = find_unverified_numbers(out.conclusion, prep.allowed)
    report.n_free_numbers += len(free)
    for x in free:
        report.issues.append(
            VerifyIssue(code="so_khong_kiem_duoc", where="conclusion", detail=f"{x.kind}:{x.text}")
        )
    report.n_points_kept = len(points)
    report.flags = sorted({i.code for i in report.issues})
    return AnswerResult(
        **base,
        llm_text=res.text,
        llm_output=res.parsed,
        answer=render_answer(points, out.conclusion, show_invalid=True),
        points=points,
        conclusion=out.conclusion,
        citations=[c for p in points for c in p.citations if c.valid],
        verify=report,
        status="ok",
        answer_status=out.status,
        repair_prompt_hash=res.repair_prompt_hash,
        usage=res.usage,
        latency_ms=res.latency_ms,
        attempts=res.attempts,
        cached=res.cached,
        n_llm_calls=1,
    )


__all__ = [
    "AnswerConfig",
    "AnswerContext",
    "AnswerOut",
    "AnswerOutNoRag",
    "AnswerResult",
    "AnswerStatus",
    "NumberUse",
    "PointOut",
    "PointResult",
    "Prepared",
    "RetrievalRef",
    "SourceRef",
    "VerifyIssue",
    "VerifyReport",
    "answer",
    "load_answer_config",
    "prepare",
    "render_answer",
    "scan_numbers",
]
