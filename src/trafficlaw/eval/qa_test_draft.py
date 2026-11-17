"""Bản nháp câu test do LLM viết, người dùng sửa (quyết định người dùng 17/11/2026).

Luồng ``qa_tool draft-test`` (cần GPU) → người dùng chọn/sửa trong ``data/qa/test_drafts.md`` →
chép dòng đã sửa vào ``data/qa/test.jsonl`` → ``qa_tool validate --split test``.

- Đầu vào = đúng các gợi ý của phiếu viết (``qa_plan.plan_suggestions``, seed cố định), trừ
  ``ngoai_pham_vi`` (người dùng tự viết tay: LLM tự nghĩ câu ngoài phạm vi dễ đơn điệu).
- Model **khác họ** với model trả lời chính và model judge (giảm thiên lệch M13).
- Mỗi gợi ý một lượt gọi, ``n_drafts`` bản nháp khác nhau; vai người hỏi + kiểu câu gán tất
  định bằng ``sha256(seed:qa_test_draft:<sid>)`` để câu không cùng một giọng.
- LLM không tự viết con số vào ``required_numbers``: chỉ chọn chỉ số trong danh sách số lấy bằng
  rule (đồ thị M8). Số lạ trong đáp án, câu chép nguyên văn, nêu số Điều/Khoản… → **cờ** để người
  sửa chú ý (không loại: người dùng sửa mọi câu).
- Mỗi câu nháp có ``draft_id``; dòng test chép từ nháp có ``source = "llm:<model>+human"`` +
  ``draft_id``; validator báo lỗi nếu câu hỏi giống hệt nháp (chưa sửa) và đo tỷ lệ sửa.
"""

from __future__ import annotations

import difflib
import hashlib
import json
import re
from collections import Counter, defaultdict
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from trafficlaw.eval.qa_generate import _CONTEXT_RE, Client, doc_label
from trafficlaw.eval.qa_plan import ChunkFacts, Suggestion, chunk_facts
from trafficlaw.eval.qa_schema import DRAFT_SOURCE_RE, QUESTION_TYPE_DOC
from trafficlaw.eval.qa_validate import GraphView
from trafficlaw.eval.textsim import normalize
from trafficlaw.graph.store import (
    BaseGraphStore,
    GraphNode,
    canonical_json,
    unit_of_version_id,
)
from trafficlaw.llm import LLMResult, Prompt, QuotaExhaustedError
from trafficlaw.llm.parallel import map_parallel
from trafficlaw.retrieval.chunking import Chunk
from trafficlaw.utils.jsonl import JsonlWriter, read_jsonl
from trafficlaw.verify.numbers import dec_str, format_int_vn, parse_numbers

DEFAULT_OUT_TOKENS = 700.0
MAX_REFS = 3
"""Số điều khoản được dẫn chiếu tối đa đưa thêm vào nguồn của một chunk."""

#: Đoạn chèn theo loại câu (``$type_rules``). Đổi nội dung ⇒ ``prompt_hash`` đổi ⇒ run mới.
TYPE_RULES: dict[str, str] = {
    "muc_phat": "Hỏi về mức phạt mà người vi phạm phải chịu. Ít nhất một bản nháp mô tả hành vi "
    "qua một tình huống, không gọi tên hành vi.",
    "tru_diem": "Hỏi về số điểm giấy phép lái xe bị trừ. Ít nhất một bản nháp mô tả hành vi qua "
    "một tình huống, không gọi tên hành vi.",
    "bien_phap": "Hỏi về hình thức xử phạt bổ sung hoặc biện pháp khắc phục hậu quả (tước giấy "
    "phép, tịch thu, buộc khôi phục…). Ít nhất một bản nháp mô tả hành vi qua một tình huống.",
    "hanh_vi_cam_nghia_vu": "Hỏi 'có được … không' hoặc 'phải làm gì khi …'. Đáp án nói rõ được "
    "hay không được, rồi nêu điều kiện.",
    "dinh_nghia": "Không hỏi 'X là gì'. Hỏi 'trường hợp … có được coi là X không' hoặc phân biệt "
    "X với một khái niệm gần nghĩa có trong nguồn.",
    "thu_tuc_tham_quyen": "Hỏi theo nhu cầu thực tế (cần giấy tờ gì, nộp ở đâu, ai có quyền, mất "
    "bao lâu). Nếu nguồn liệt kê danh sách thì đáp án liệt kê đủ.",
    "theo_thoi_diem": "Nguồn có hai trạng thái của cùng điều khoản, kèm ngày hiệu lực. Viết hai "
    "câu gần như giống nhau, chỉ khác thời điểm (nêu ngày hoặc tháng trong câu). Phần tử thứ nhất "
    "có as_of = $date_before, phần tử thứ hai có as_of = $date_after. Hai đáp án phải khác nhau "
    "đúng ở phần nội dung đã thay đổi. Nếu trạng thái trước mốc là 'chưa có hiệu lực' thì đáp án "
    "thứ nhất ghi 'chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu' và gold_units "
    "của nó để rỗng.",
    "da_buoc": "Nguồn có từ hai điều khoản nối với nhau bằng dẫn chiếu. Câu hỏi phải cần cả hai "
    "mới trả lời được (thường là một bên mô tả hành vi, bên kia nêu chế tài). gold_units có ít "
    "nhất 2 mã. Đáp án dùng thông tin của cả hai.",
    "so_sanh": "Nguồn có hai điều khoản cho hai loại xe hoặc hai chủ thể. Hỏi sự khác nhau giữa "
    "hai bên. Đáp án nêu con số của cả hai bên và bên nào nặng hơn.",
}
DRAFT_TYPES: tuple[str, ...] = tuple(TYPE_RULES)

UNIT_NAMES = {"vnd": "đồng", "diem": "điểm", "thang": "tháng"}
_STRUCT_REF_RE = re.compile(r"\b(?:điều|khoản|điểm)\s+\d+[a-z]?\b|\bđiểm\s+[a-zđ]\b", re.IGNORECASE)


class StyleSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    desc: str
    weight: float = 1.0


class RoundSpec(BaseModel):
    """Vòng sinh thêm gợi ý (mã ``W<round>-…``), không dùng lại unit của các vòng trước."""

    model_config = ConfigDict(extra="forbid")
    round: int = Field(ge=2)
    question_type: dict[str, int]


class DraftConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    provider: str | None = "local"
    model_id: str | None = None
    exclude_families_of: list[str] = Field(default_factory=list)
    """Model (served_model_name) mà model viết nháp không được trùng họ: model trả lời, judge."""
    prompt: str = "qa_test_draft"
    n_drafts: int = 2
    max_output_tokens: int = 2048
    """Gồm cả token suy luận của model có reasoning (gpt-oss)."""
    reasoning_effort: str | None = None
    """gpt-oss: ``low`` để phần suy luận ngắn; ``None`` = không gửi."""
    max_source_chars: int = 1500
    chars_per_token: float = 1.74
    """Ước token tiếng Việt cho ``--dry-run`` (đo ở M12)."""
    min_words: int = 8
    max_words: int = 50
    verbatim_ngram: int = 6
    seed: int = 42
    personas: list[str] = Field(default_factory=list)
    styles: list[StyleSpec] = Field(default_factory=list)
    rounds: list[RoundSpec] = Field(default_factory=list)


# --------------------------------------------------------------------------- schema đầu ra


class DraftQuestion(BaseModel):
    model_config = ConfigDict(extra="forbid")
    as_of: str
    question: str
    answer: str
    gold_units: list[str]
    required_numbers_idx: list[int]


class Draft(BaseModel):
    model_config = ConfigDict(extra="forbid")
    questions: list[DraftQuestion] = Field(min_length=1, max_length=2)
    ghi_chu: str
    nghi_ngo: str


def output_schema(n: int) -> type[BaseModel]:
    from pydantic import create_model

    return create_model(
        "DraftOut",
        __config__=ConfigDict(extra="forbid"),
        drafts=(list[Draft], Field(min_length=1, max_length=n)),
    )


def sha256(obj: Any) -> str:
    data = obj if isinstance(obj, str) else canonical_json(obj)
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class DraftKey:
    model_id: str
    prompt_hash: str
    schema_hash: str


def draft_key(model_id: str, prompt: Prompt, cfg: DraftConfig) -> DraftKey:
    """``prompt_hash`` gồm prompt + đoạn theo loại + vai + kiểu câu (đổi bất kỳ ⇒ run mới)."""
    ph = sha256(
        {
            "prompt": prompt.hash,
            "type_rules": TYPE_RULES,
            "personas": cfg.personas,
            "styles": [s.model_dump() for s in cfg.styles],
            "reasoning_effort": cfg.reasoning_effort,
        }
    )
    return DraftKey(model_id, ph, sha256(output_schema(cfg.n_drafts).model_json_schema()))


# --------------------------------------------------------------------------- đầu vào


@dataclass(frozen=True)
class NumberOption:
    value: int
    unit: str
    desc: str
    unit_id: str | None
    as_of: date | None = None
    """Chỉ với ``theo_thoi_diem``: ngày của trạng thái nêu con số."""

    def required(self) -> dict[str, Any]:
        return {"value": self.value, "unit": self.unit}

    def display(self) -> str:
        v = format_int_vn(self.value) if self.unit == "vnd" else f"{self.value:02d}"
        when = f" — trạng thái tại {self.as_of}" if self.as_of else ""
        unit = UNIT_NAMES.get(self.unit, self.unit)
        return f"{v} {unit} ({self.desc}, nêu tại {self.unit_id}){when}"


@dataclass
class DraftInput:
    sid: str
    qtype: str
    tier: str
    dates: list[date]
    sources: str
    numbers: list[NumberOption]
    allowed_units: list[str]
    persona: str
    style: StyleSpec
    gold_default: list[list[str]]
    """``gold_units`` mặc định theo từng câu (1 câu; 2 câu cho ``theo_thoi_diem``)."""
    note: str = ""
    source_text: str = field(default="", repr=False)
    """Toàn văn các nguồn (dò số lạ, chép nguyên văn)."""

    @property
    def n_questions(self) -> int:
        return len(self.dates)


def _pick(sid: str, seed: int, salt: str, n: int) -> int:
    h = hashlib.sha256(f"{seed}:qa_test_draft:{salt}:{sid}".encode()).hexdigest()
    return int(h[:12], 16) % n


def pick_style(sid: str, cfg: DraftConfig) -> tuple[str, StyleSpec]:
    """Vai + kiểu câu tất định theo ``sid``; kiểu câu theo trọng số."""
    persona = (
        cfg.personas[_pick(sid, cfg.seed, "persona", len(cfg.personas))]
        if cfg.personas
        else "người dân"
    )
    styles = cfg.styles or [StyleSpec(name="tinh_huong", desc="tình huống của bản thân")]
    tot = sum(s.weight for s in styles)
    x = _pick(sid, cfg.seed, "style", 10**9) / 10**9 * tot
    acc = 0.0
    for s in styles:
        acc += s.weight
        if x < acc:
            return persona, s
    return persona, styles[-1]


def _clip(text: str, n: int) -> str:
    return text if len(text) <= n else text[:n].rsplit("\n", 1)[0] + "\n…"


def number_options(sem: Sequence[GraphNode], as_of: date | None = None) -> list[NumberOption]:
    out: list[NumberOption] = []
    for n in sem:
        p = n.props
        uid = p.get("unit_id")
        if n.label == "CheTai" and p.get("loai") == "phat_tien":
            for k, d in (
                ("min_vnd", "mức phạt tiền tối thiểu"),
                ("max_vnd", "mức phạt tiền tối đa"),
            ):
                if isinstance(p.get(k), int):
                    out.append(NumberOption(p[k], "vnd", d, uid, as_of))
        elif n.label == "CheTai" and p.get("loai") in ("tuoc_quyen", "dinh_chi"):
            what = "tước quyền sử dụng" if p.get("loai") == "tuoc_quyen" else "đình chỉ"
            for k, d in (("min_thang", "tối thiểu"), ("max_thang", "tối đa")):
                if isinstance(p.get(k), int):
                    out.append(NumberOption(p[k], "thang", f"thời hạn {what} {d}", uid, as_of))
        elif n.label == "DiemGPLX" and isinstance(p.get("so_diem"), int):
            out.append(NumberOption(p["so_diem"], "diem", "số điểm bị trừ", uid, as_of))
    seen: set[tuple[Any, ...]] = set()
    uniq = []
    for o in out:
        k = (o.value, o.unit, o.unit_id, o.as_of)
        if k not in seen:
            seen.add(k)
            uniq.append(o)
    return uniq


@dataclass
class _Acc:
    """Phần đầu vào gom dần từ các chunk của một gợi ý."""

    blocks: list[str] = field(default_factory=list)
    texts: list[str] = field(default_factory=list)
    numbers: list[NumberOption] = field(default_factory=list)
    allowed: list[str] = field(default_factory=list)

    def allow(self, units: Sequence[str]) -> None:
        for u in units:
            if u not in self.allowed:
                self.allowed.append(u)


def _add_chunk(
    acc: _Acc, gv: GraphView, title: str, c: Chunk, d: date, *, tag_date: bool, max_chars: int
) -> None:
    units = list(gv.store.subtree(c.unit_id, as_of=d)) or [c.unit_id]
    acc.allow(units)
    acc.texts.append(c.text)
    f: ChunkFacts = chunk_facts(gv, [c], d)[0]
    related: list[str] = []
    for x in number_options(f.sem, d if tag_date else None):
        if x not in acc.numbers:
            acc.numbers.append(x)
        if x.unit_id and x.unit_id not in units and x.unit_id not in related:
            related.append(x.unit_id)
    # Điều khoản được dẫn chiếu (vd "tái phạm hành vi quy định tại điểm a khoản 7 Điều này"):
    # thiếu nguyên văn thì model tự bịa hành vi (chạy thử 17/11/2026).
    refs: list[str] = []
    for vid in c.version_ids:
        for e in gv.store.references_from(unit_of_version_id(vid), d):
            u = e.dst
            if (
                not e.props.get("can_cu")
                and u not in units
                and u not in related
                and u not in refs
                and gv.unit(u) is not None
            ):
                refs.append(u)
    acc.blocks.append(
        f"### {title}\n"
        f"Văn bản: {doc_label(gv.doc(c.doc_id))}\n"
        f"Hiệu lực của trạng thái này: {c.effective_from} → {c.effective_to or 'nay'}\n"
        f"Mã điều khoản dùng được cho gold_units: {', '.join(units)}\n\n"
        f"{_clip(c.text, max_chars)}"
    )
    for u in related:
        text = related_text(gv.store, u, d)
        if not text:
            continue
        acc.allow([u])
        acc.texts.append(text)
        acc.blocks.append(
            f"### Điều khoản nêu chế tài áp cho hành vi trên ({u})\n"
            f"Mã điều khoản dùng được cho gold_units: {u}\n\n{_clip(text, max_chars)}"
        )
    for u in refs[:MAX_REFS]:
        text = related_text(gv.store, u, d)
        if not text:
            continue
        acc.allow([u])
        acc.texts.append(text)
        acc.blocks.append(
            f"### Điều khoản được nguồn trên dẫn chiếu tới ({u})\n"
            f"Mã điều khoản dùng được cho gold_units: {u}\n\n{_clip(text, max_chars)}"
        )


def related_text(store: BaseGraphStore, unit_id: str, d: date) -> str:
    """Nguyên văn unit tại ngày ``d`` kèm dòng đầu (câu dẫn) của các tổ tiên Khoản/Điều."""
    v = store.version_at(unit_id, d)
    if v is None:
        return ""
    lines = []
    for a in store.ancestors(unit_id):
        n = store.get_node(a)
        if n is None or n.label not in ("Dieu", "Khoan"):
            continue
        if n.label == "Dieu":
            lines.append(f"Điều {n.props.get('number')}. {n.props.get('title') or ''}".strip())
        else:
            av = store.version_at(a, d)
            if av is not None:
                lines.append(str(av.props.get("text") or "").split("\n")[0])
    return "\n".join([*reversed(lines), str(v.props.get("text") or "")])


def build_inputs(
    store: BaseGraphStore, suggestions: Sequence[Suggestion], cfg: DraftConfig
) -> list[DraftInput]:
    gv = GraphView(store)
    mc = cfg.max_source_chars
    out = []
    for s in suggestions:
        if s.qtype not in TYPE_RULES:
            continue
        persona, style = pick_style(s.sid, cfg)
        acc = _Acc()
        if s.qtype == "theo_thoi_diem":
            before = s.chunks[0] if len(s.chunks) == 2 else None
            after = s.chunks[-1]
            t0 = f"Trạng thái trước mốc (áp dụng tại {s.dates[0]})"
            if before is None:
                acc.blocks.append(f"### {t0}\nChưa có hiệu lực (không có phiên bản).")
            else:
                _add_chunk(acc, gv, t0, before, s.dates[0], tag_date=True, max_chars=mc)
            t1 = f"Trạng thái sau mốc (áp dụng tại {s.dates[1]})"
            _add_chunk(acc, gv, t1, after, s.dates[1], tag_date=True, max_chars=mc)
            gold = [[] if before is None else [after.unit_id], [after.unit_id]]
        else:
            for i, c in enumerate(s.chunks, 1):
                _add_chunk(acc, gv, f"Nguồn {i}", c, s.dates[0], tag_date=False, max_chars=mc)
            acc.allow(s.gold_units or [])
            gold = [list(s.gold_units or [c.unit_id for c in s.chunks])]
        out.append(
            DraftInput(
                sid=s.sid,
                qtype=s.qtype,
                tier=s.tier,
                dates=list(s.dates),
                sources="\n\n".join(acc.blocks),
                numbers=acc.numbers,
                allowed_units=acc.allowed,
                persona=persona,
                style=style,
                gold_default=gold,
                note=s.note,
                source_text="\n".join(acc.texts),
            )
        )
    return out


def render_numbers(inp: DraftInput) -> str:
    if not inp.numbers:
        return "(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)"
    return "\n".join(f"[{i}] {o.display()}" for i, o in enumerate(inp.numbers))


def build_messages(prompt: Prompt, inp: DraftInput) -> list[dict[str, str]]:
    from string import Template

    rules = TYPE_RULES[inp.qtype]
    if inp.qtype == "theo_thoi_diem":
        rules = Template(rules).safe_substitute(
            date_before=inp.dates[0].isoformat(), date_after=inp.dates[1].isoformat()
        )
    content = prompt.render(
        question_type=inp.qtype,
        type_desc=QUESTION_TYPE_DOC[inp.qtype],
        tier=inp.tier,
        as_of=" / ".join(d.isoformat() for d in inp.dates),
        persona=inp.persona,
        style=f"{inp.style.name} — {inp.style.desc}",
        type_rules=rules,
        sources=inp.sources,
        numbers=render_numbers(inp),
    )
    return [{"role": "user", "content": content}]


def input_key(prompt: Prompt, inp: DraftInput) -> str:
    return sha256(build_messages(prompt, inp)[0]["content"])


# --------------------------------------------------------------------------- chạy LLM


def _matches(r: Mapping[str, Any], key: DraftKey) -> bool:
    return (
        r.get("model_id") == key.model_id
        and r.get("prompt_hash") == key.prompt_hash
        and r.get("schema_hash") == key.schema_hash
    )


def done_input_keys(raw: Path, key: DraftKey, *, retry_format_error: bool = False) -> set[str]:
    ok = {"ok"} if retry_format_error else {"ok", "format_error"}
    return {
        str(r["input_key"]) for r in read_jsonl(raw) if _matches(r, key) and r.get("status") in ok
    }


def output_tokens_per_call(raw: Path, default: float = DEFAULT_OUT_TOKENS) -> float:
    n = tok = 0
    for r in read_jsonl(raw):
        if r.get("status") == "ok" and not r.get("cached"):
            n += 1
            tok += int((r.get("usage") or {}).get("completion_tokens") or 0)
    return tok / n if n >= 10 and tok else default


def estimate(
    todo: Sequence[DraftInput], prompt: Prompt, cfg: DraftConfig, *, out_per_call: float
) -> dict[str, dict[str, int]]:
    by: dict[str, dict[str, int]] = {}
    for inp in todo:
        tok = int(len(build_messages(prompt, inp)[0]["content"]) / cfg.chars_per_token) + 1
        for k in (f"type:{inp.qtype}", "total"):
            s = by.setdefault(k, {"calls": 0, "prompt_tokens": 0, "output_tokens": 0})
            s["calls"] += 1
            s["prompt_tokens"] += tok
            s["output_tokens"] += round(out_per_call)
    return dict(sorted(by.items()))


@dataclass
class DraftRunOutcome:
    n_inputs: int = 0
    n_todo: int = 0
    n_called: int = 0
    by_status: Counter[str] = field(default_factory=Counter)
    stopped: str | None = None
    hint: str = ""


def run_drafts(
    inputs: Sequence[DraftInput],
    cfg: DraftConfig,
    client: Client,
    raw: Path,
    prompt: Prompt,
    *,
    max_calls: int | None = None,
    retry_format_error: bool = False,
    workers: int = 1,
    git_commit: str | None = None,
    run_meta: Mapping[str, Any] | None = None,
    resume_cmd: str = "uv run python -m scripts.qa_tool draft-test",
    progress: Callable[[int, int, DraftInput, LLMResult], None] | None = None,
) -> DraftRunOutcome:
    key = draft_key(client.model_id, prompt, cfg)
    done = done_input_keys(raw, key, retry_format_error=retry_format_error)
    todo = [i for i in inputs if input_key(prompt, i) not in done]
    out = DraftRunOutcome(n_inputs=len(inputs), n_todo=len(todo))
    if max_calls is not None:
        todo = todo[: max(0, max_calls)]
    schema = output_schema(cfg.n_drafts)
    params: dict[str, Any] = {"max_output_tokens": cfg.max_output_tokens}
    if cfg.reasoning_effort:
        params["reasoning_effort"] = cfg.reasoning_effort

    def call(inp: DraftInput) -> LLMResult:
        return client.generate(build_messages(prompt, inp), json_schema=schema, params=params)

    with JsonlWriter(raw) as w:
        for inp, r in map_parallel(todo, call, workers):
            if isinstance(r, QuotaExhaustedError):
                out.stopped = "quota"
                out.hint = f"Dừng ({r}); chạy lại để tiếp tục: {resume_cmd}"
                break
            w.write(
                {
                    "sid": inp.sid,
                    "input_key": input_key(prompt, inp),
                    "model_id": r.model_id,
                    "provider": r.provider,
                    "prompt_hash": key.prompt_hash,
                    "schema_hash": key.schema_hash,
                    "status": r.status,
                    "parsed": r.parsed,
                    "text": None if r.status == "ok" else (r.text or "")[:4000],
                    "error": r.error,
                    "usage": r.usage.model_dump(),
                    "latency_ms": r.latency_ms,
                    "attempts": r.attempts,
                    "cached": r.cached,
                    **({"serve": dict(run_meta)} if run_meta else {}),
                    "git_commit": git_commit,
                    "run_at": datetime.now().astimezone().isoformat(timespec="seconds"),
                }
            )
            out.n_called += 1
            out.by_status[r.status] += 1
            if progress is not None:
                progress(out.n_called, len(todo), inp, r)
    return out


# --------------------------------------------------------------------------- hậu kiểm + ghép


def _word_ngrams(text: str, n: int) -> set[tuple[str, ...]]:
    w = normalize(text).split()
    return {tuple(w[i : i + n]) for i in range(len(w) - n + 1)}


def question_flags(q: str, inp: DraftInput, cfg: DraftConfig) -> list[str]:
    flags = []
    n_words = len(q.split())
    if n_words < cfg.min_words:
        flags.append(f"qua_ngan ({n_words} từ)")
    if n_words > cfg.max_words:
        flags.append(f"qua_dai ({n_words} từ)")
    common = _word_ngrams(q, cfg.verbatim_ngram) & _word_ngrams(inp.source_text, cfg.verbatim_ngram)
    if common:
        flags.append("chep_nguyen_van: “" + " ".join(sorted(common)[0]) + " …”")
    if _STRUCT_REF_RE.search(q):
        flags.append("neu_dieu_khoan")
    if _CONTEXT_RE.search(q):
        flags.append("tham_chieu_ngu_canh")
    return flags


def answer_flags(a: str, inp: DraftInput) -> list[str]:
    allowed = parse_numbers(inp.source_text) | parse_numbers(inp.sources)
    allowed |= {x for o in inp.numbers for x in parse_numbers(str(o.value))}
    # bỏ số hiệu văn bản ("168/2024/NĐ-CP") và chuỗi dẫn chiếu trước khi dò
    body = re.sub(r"\S*\d+/\d{4}\S*", " ", a)
    body = re.sub(r"\b(?:Điều|điều|khoản|điểm|Khoản|Điểm)\s+\d+[a-z]?", " ", body)
    strange = sorted(dec_str(x) for x in parse_numbers(body) - allowed)
    return [f"so_la: {', '.join(strange)}"] if strange else []


@dataclass
class DraftRecord:
    draft_id: str
    sid: str
    k: int
    j: int
    qtype: str
    tier: str
    persona: str
    style: str
    model_id: str
    prompt_hash: str
    item: dict[str, Any]
    flags: list[str]
    ghi_chu: str
    nghi_ngo: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "draft_id": self.draft_id,
            "sid": self.sid,
            "k": self.k,
            "j": self.j,
            "question_type": self.qtype,
            "tier": self.tier,
            "persona": self.persona,
            "style": self.style,
            "model_id": self.model_id,
            "prompt_hash": self.prompt_hash,
            "flags": self.flags,
            "ghi_chu": self.ghi_chu,
            "nghi_ngo": self.nghi_ngo,
            "item": self.item,
        }


def _sid_parts(sid: str) -> tuple[str, str]:
    """``W-muc_phat-001`` → ("", "muc_phat-001"); ``W2-muc_phat-001`` → ("2", "muc_phat-001")."""
    prefix, rest = sid.split("-", 1)
    return prefix[1:], rest


def qid_for(sid: str, j: int, n_questions: int) -> str:
    rnd, rest = _sid_parts(sid)
    return f"t{rnd}-{rest}" + ("ab"[j] if n_questions == 2 else "")


def pair_id_for(sid: str) -> str:
    rnd, rest = _sid_parts(sid)
    return f"p{rnd}-{rest.rsplit('-', 1)[1]}"


def assemble(
    inputs: Sequence[DraftInput],
    parsed_by_sid: Mapping[str, Mapping[str, Any]],
    key: DraftKey,
    cfg: DraftConfig,
) -> list[DraftRecord]:
    """Bản ghi nháp sẵn chép: ép ``as_of`` theo gợi ý, lọc ``gold_units`` về mã trong nguồn, đổi
    chỉ số con số thành ``required_numbers``; mọi chỗ sửa/nghi vấn ghi vào ``flags``."""
    out: list[DraftRecord] = []
    for inp in inputs:
        parsed = parsed_by_sid.get(inp.sid)
        if not parsed:
            continue
        for k, d in enumerate(parsed.get("drafts") or [], 1):
            qs = list(d.get("questions") or [])
            pair_flags: list[str] = []
            if len(qs) != inp.n_questions:
                pair_flags.append(f"so_cau_sai ({len(qs)}/{inp.n_questions})")
                qs = qs[: inp.n_questions]
            if (
                inp.n_questions == 2
                and len(qs) == 2
                and normalize(qs[0].get("answer", "")) == normalize(qs[1].get("answer", ""))
            ):
                pair_flags.append("dap_an_cap_giong_nhau")
            for j, q in enumerate(qs):
                flags = list(pair_flags)
                want = inp.dates[j].isoformat()
                if q.get("as_of") != want:
                    flags.append(f"as_of_sua ({q.get('as_of')} → {want})")
                gold = [u for u in q.get("gold_units") or [] if u in inp.allowed_units]
                bad = [u for u in q.get("gold_units") or [] if u not in inp.allowed_units]
                if bad:
                    flags.append(f"gold_ngoai_nguon: {', '.join(bad)}")
                if not gold and inp.gold_default[j]:
                    gold = list(inp.gold_default[j])
                    flags.append("gold_mac_dinh")
                if inp.qtype == "theo_thoi_diem" and not inp.gold_default[j]:
                    gold = []
                if inp.qtype == "da_buoc" and len(gold) < 2:
                    flags.append("da_buoc_it_hon_2_gold")
                nums = []
                for i in q.get("required_numbers_idx") or []:
                    if isinstance(i, int) and 0 <= i < len(inp.numbers):
                        o = inp.numbers[i]
                        if o.as_of is None or o.as_of == inp.dates[j]:
                            if o.required() not in nums:
                                nums.append(o.required())
                            continue
                    flags.append(f"chi_so_so_sai ({i})")
                question = str(q.get("question") or "").strip()
                answer = str(q.get("answer") or "").strip()
                flags += question_flags(question, inp, cfg)
                flags += answer_flags(answer, inp)
                draft_id = f"{inp.sid}:{k}" + ("ab"[j] if inp.n_questions == 2 else "")
                item: dict[str, Any] = {
                    "qid": qid_for(inp.sid, j, inp.n_questions),
                    "question": question,
                    "as_of": want,
                    "question_type": inp.qtype,
                    "tier": inp.tier,
                    "answer": answer,
                    "gold_units": gold,
                    "required_numbers": nums,
                    "source": f"llm:{key.model_id}+human",
                    "draft_id": draft_id,
                }
                if inp.n_questions == 2:
                    item["pair_id"] = pair_id_for(inp.sid)
                out.append(
                    DraftRecord(
                        draft_id=draft_id,
                        sid=inp.sid,
                        k=k,
                        j=j,
                        qtype=inp.qtype,
                        tier=inp.tier,
                        persona=inp.persona,
                        style=inp.style.name,
                        model_id=key.model_id,
                        prompt_hash=key.prompt_hash,
                        item=item,
                        flags=flags,
                        ghi_chu=str(d.get("ghi_chu") or ""),
                        nghi_ngo=str(d.get("nghi_ngo") or ""),
                    )
                )
    return out


def latest_parsed(
    raw: Path, key: DraftKey, keys_by_sid: Mapping[str, str]
) -> tuple[dict[str, Any], Counter[str]]:
    """Phản hồi ``ok`` mới nhất của mỗi gợi ý, chỉ khi ``input_key`` còn khớp đầu vào hiện hành."""
    parsed: dict[str, Any] = {}
    status: dict[str, str] = {}
    for r in read_jsonl(raw):
        sid = str(r.get("sid"))
        if not _matches(r, key) or keys_by_sid.get(sid) != r.get("input_key"):
            continue
        status[sid] = str(r.get("status"))
        if r.get("status") == "ok" and r.get("parsed"):
            parsed[sid] = r["parsed"]
    return parsed, Counter(status.values())


def render_markdown(
    inputs: Sequence[DraftInput], records: Sequence[DraftRecord], meta: Mapping[str, Any]
) -> str:
    by_sid: dict[str, list[DraftRecord]] = defaultdict(list)
    for r in records:
        by_sid[r.sid].append(r)
    lines = [
        "# Bản nháp câu test (LLM viết, người dùng sửa)",
        "",
        f"Model `{meta.get('model_id')}` · prompt `{str(meta.get('prompt_hash'))[:12]}` · "
        f"{len(by_sid)}/{len(inputs)} gợi ý có nháp · {len(records)} câu nháp.",
        "",
        "Cách dùng: với mỗi gợi ý, chọn **tối đa một** bản nháp, sửa câu hỏi + đáp án (bắt buộc — "
        "validator báo lỗi `nhap_chua_sua` nếu câu hỏi giữ nguyên), kiểm từng con số với nguồn, "
        "rồi chép **dòng JSON đã sửa** vào `data/qa/test.jsonl`. Giữ nguyên `source` và "
        "`draft_id` để đo tỷ lệ sửa. Cờ ⚠ là chỗ cần xem kỹ (không phải lỗi chắc chắn).",
        "",
        "Câu `ngoai_pham_vi` (35) không có nháp: tự viết tay, `source: human`.",
        "",
    ]
    cur = None
    for inp in inputs:
        if inp.qtype != cur:
            cur = inp.qtype
            lines += [f"## {cur} — {QUESTION_TYPE_DOC[cur]}", ""]
        lines += [
            f"### {inp.sid} · tier {inp.tier} · vai: {inp.persona} · kiểu: {inp.style.name}"
            + (f" · {inp.note}" if inp.note else ""),
            "",
            "<details><summary>Nguồn và con số</summary>",
            "",
            "```text",
            inp.sources,
            "",
            render_numbers(inp),
            "```",
            "",
            "</details>",
            "",
        ]
        recs = by_sid.get(inp.sid)
        if not recs:
            lines += ["_(chưa có nháp)_", ""]
            continue
        for k in sorted({r.k for r in recs}):
            group = [r for r in recs if r.k == k]
            lines.append(f"**Nháp {k}**")
            lines.append("")
            for r in group:
                it = r.item
                lines += [
                    f"- Hỏi ({it['as_of']}): {it['question']}",
                    f"- Đáp: {it['answer']}",
                ]
                if r.flags:
                    lines.append("- ⚠ " + "; ".join(r.flags))
            g = group[0]
            if g.ghi_chu:
                lines.append(f"- Ghi chú: {g.ghi_chu}")
            if g.nghi_ngo:
                lines.append(f"- Nghi ngờ: {g.nghi_ngo}")
            lines += [
                "",
                "```json",
                *(json.dumps(r.item, ensure_ascii=False) for r in group),
                "```",
                "",
            ]
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------- đo tỷ lệ sửa


def _ratio(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, normalize(a), normalize(b)).ratio()


def edit_stats(items: Sequence[Any], drafts: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    """So câu test với nháp gốc: độ giống (difflib trên chuỗi chuẩn hoá) câu hỏi/đáp án, tỷ lệ
    đổi ``gold_units``/``required_numbers``. ``items`` là ``QAItem``."""
    rows = []
    n_reviewed = 0
    for it in items:
        d = drafts.get(getattr(it, "draft_id", None) or "")
        if not d:
            continue
        m = DRAFT_SOURCE_RE.match(it.source)
        if m and m.group(2) == "reviewed":
            n_reviewed += 1
            continue
        di = d.get("item") or {}
        num = sorted(
            json.dumps(x.model_dump(exclude_none=True), sort_keys=True) for x in it.required_numbers
        )
        dnum = sorted(json.dumps(x, sort_keys=True) for x in di.get("required_numbers") or [])
        rows.append(
            {
                "q": _ratio(it.question, di.get("question", "")),
                "a": _ratio(it.answer or "", di.get("answer", "")),
                "gold": sorted(it.gold_units) != sorted(di.get("gold_units") or []),
                "num": num != dnum,
            }
        )
    n_human = sum(1 for it in items if not getattr(it, "draft_id", None))
    if not rows:
        return {"n_from_draft": 0, "n_human": n_human, "n_reviewed_unedited": n_reviewed}
    n = len(rows)
    return {
        "n_from_draft": n,
        "n_human": n_human,
        "n_reviewed_unedited": n_reviewed,
        "question_similarity_mean": round(sum(r["q"] for r in rows) / n, 4),
        "answer_similarity_mean": round(sum(r["a"] for r in rows) / n, 4),
        "question_similarity_ge_0_9": round(sum(r["q"] >= 0.9 for r in rows) / n, 4),
        "answer_unchanged": round(sum(r["a"] >= 0.999 for r in rows) / n, 4),
        "gold_changed": round(sum(r["gold"] for r in rows) / n, 4),
        "numbers_changed": round(sum(r["num"] for r in rows) / n, 4),
    }


def load_drafts(path: Path) -> dict[str, dict[str, Any]]:
    return {str(r["draft_id"]): r for r in read_jsonl(path)} if path.is_file() else {}


# --------------------------------------------------------------------------- nhập tự động

#: Cờ loại bỏ khi nhập tự động (``import-drafts --auto``, người dùng chọn "lọc chặt" 17/11/2026):
#: mọi cờ của hậu kiểm, kể cả chép nguyên văn (câu bám chữ luật có lợi cho BM25).
HEAVY_FLAGS: tuple[str, ...] = (
    "so_la",
    "chi_so_so_sai",
    "so_cau_sai",
    "dap_an_cap_giong_nhau",
    "da_buoc_it_hon_2_gold",
    "gold_mac_dinh",
    "gold_ngoai_nguon",
    "as_of_sua",
    "tham_chieu_ngu_canh",
    "neu_dieu_khoan",
    "chep_nguyen_van",
    "qua_ngan",
    "qua_dai",
)


def flag_code(flag: str) -> str:
    return flag.split(" ")[0].rstrip(":")


def select_auto(
    records: Sequence[Mapping[str, Any]], heavy: Sequence[str] = HEAVY_FLAGS
) -> tuple[list[dict[str, Any]], dict[str, list[str]]]:
    """Mỗi gợi ý lấy nháp ``k`` nhỏ nhất mà mọi câu của nó (1, hoặc 2 với cặp) không có cờ nặng.
    Trả (các dòng test với ``source = llm:<model>+reviewed``, {sid bị bỏ: cờ của các nháp})."""
    by: dict[str, dict[int, list[Mapping[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    for r in records:
        by[str(r["sid"])][int(r["k"])].append(r)
    out: list[dict[str, Any]] = []
    skipped: dict[str, list[str]] = {}
    for sid in sorted(by):
        chosen = None
        seen: list[str] = []
        for k in sorted(by[sid]):
            group = sorted(by[sid][k], key=lambda r: int(r.get("j", 0)))
            codes = sorted({flag_code(f) for r in group for f in r.get("flags") or []})
            bad = [c for c in codes if c in heavy]
            if not bad:
                chosen = group
                break
            seen.append(f"nháp {k}: {', '.join(bad)}")
        if chosen is None:
            skipped[sid] = seen
            continue
        for r in chosen:
            item = dict(r["item"])
            item["source"] = f"llm:{r['model_id']}+reviewed"
            out.append(item)
    return out, skipped


__all__ = [
    "DRAFT_SOURCE_RE",
    "DRAFT_TYPES",
    "HEAVY_FLAGS",
    "RoundSpec",
    "cap_quota",
    "pair_id_for",
    "flag_code",
    "select_auto",
    "TYPE_RULES",
    "Draft",
    "DraftConfig",
    "DraftInput",
    "DraftKey",
    "DraftQuestion",
    "DraftRecord",
    "NumberOption",
    "StyleSpec",
    "answer_flags",
    "assemble",
    "build_inputs",
    "build_messages",
    "done_input_keys",
    "draft_key",
    "edit_stats",
    "estimate",
    "input_key",
    "latest_parsed",
    "load_drafts",
    "number_options",
    "output_schema",
    "output_tokens_per_call",
    "pick_style",
    "question_flags",
    "render_markdown",
    "run_drafts",
]


def cap_quota(
    items: Sequence[Mapping[str, Any]], quota: Mapping[str, int]
) -> tuple[list[dict[str, Any]], list[str]]:
    """Giữ câu theo thứ tự (vòng 1 trước) tới hạn mức mỗi loại; cặp ``pair_id`` giữ/bỏ cùng nhau.
    Trả (câu giữ, qid bỏ vì đủ hạn mức)."""
    groups: dict[str, list[Mapping[str, Any]]] = {}
    order: list[str] = []
    for it in items:
        k = str(it.get("pair_id") or it["qid"])
        if k not in groups:
            groups[k] = []
            order.append(k)
        groups[k].append(it)
    count: Counter[str] = Counter()
    keep: list[dict[str, Any]] = []
    dropped: list[str] = []
    for k in order:
        g = groups[k]
        qt = str(g[0]["question_type"])
        if count[qt] + len(g) <= quota.get(qt, 0):
            count[qt] += len(g)
            keep += [dict(x) for x in g]
        else:
            dropped += [str(x["qid"]) for x in g]
    return keep, dropped
