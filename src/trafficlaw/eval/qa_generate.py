"""M9: sinh câu hỏi train/val cho fine-tune embedding + reranker (M14).

Luồng ``qa_tool generate`` (cần GPU) rồi ``qa_tool build`` (không cần GPU, chạy lại được mỗi khi
``test.jsonl`` đổi):

1. ``select_chunks``: chunk = 1 phiên bản Khoản kèm Điểm, tiền tố tiêu đề Điều
   (``retrieval.chunking``), mọi văn bản ``indexable``; chunk trùng text → gọi một lần.
2. ``run_generate``: mỗi chunk một lượt gọi LLM (model tự host, khác họ với model trả lời), JSON
   ``{questions: [{question, question_type}]}`` ≤ N câu. Ghi ``raw.jsonl`` (append, flush từng
   dòng). Chunk xong = có bản ghi ``ok``/``format_error`` cùng ``(model_id, prompt_hash,
   schema_hash, chunk_key)``; ``error`` chạy lại; ``QuotaExhaustedError`` → dừng sạch.
3. ``build_splits``: lọc (``filter_questions``), bỏ trùng tuyệt đối, bỏ câu gần trùng câu test
   (TF-IDF cosine > ngưỡng — chống rò rỉ), đánh dấu ``in_test_gold`` (không loại — quyết định
   10/11/2026), chia val **theo Điều** (băm ``seed:dieu_id`` < ``val_fraction``) →
   ``train.jsonl``, ``val.jsonl``, ``train_manifest.json``, ``rejected.jsonl``.
"""

from __future__ import annotations

import hashlib
import json
import re
import statistics
import unicodedata
from collections import Counter
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any, Literal, Protocol

from pydantic import BaseModel, ConfigDict, Field, create_model

from trafficlaw.eval.qa_schema import QUESTION_TYPE_DOC, QAItem, item_dict
from trafficlaw.eval.qa_validate import parse_numbers
from trafficlaw.eval.textsim import near_pairs, normalize
from trafficlaw.graph.store import BaseGraphStore, canonical_json
from trafficlaw.llm import LLMResult, Prompt, QuotaExhaustedError, load_prompt
from trafficlaw.llm.parallel import map_parallel
from trafficlaw.retrieval.chunking import Chunk, iter_chunks
from trafficlaw.utils.jsonl import JsonlWriter, read_jsonl, write_jsonl

TRAIN_TYPES: tuple[str, ...] = (
    "muc_phat",
    "tru_diem",
    "bien_phap",
    "hanh_vi_cam_nghia_vu",
    "dinh_nghia",
    "thu_tuc_tham_quyen",
    "khac",
)
TrainType = Literal[
    "muc_phat",
    "tru_diem",
    "bien_phap",
    "hanh_vi_cam_nghia_vu",
    "dinh_nghia",
    "thu_tuc_tham_quyen",
    "khac",
]
DEFAULT_OUT_TOKENS_PER_CHUNK = 220.0


class Client(Protocol):
    @property
    def model_id(self) -> str: ...

    @property
    def provider_name(self) -> str: ...

    def generate(self, messages: Sequence[Any], **kw: Any) -> LLMResult: ...


class GenerateConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    provider: str | None = "local"
    model_id: str | None = "mistral-small-3.2"
    prompt: str = "qa_generate"
    n_questions: int = 3
    max_output_tokens: int = 1024
    max_chunk_chars: int = 6000
    """Chunk dài hơn bị cắt (đầu chunk giữ nguyên) trước khi đưa vào prompt."""
    min_words: int = 5
    max_words: int = 50
    max_chars: int = 300
    verbatim_ngram: int = 10
    min_coverage: float = 0.5
    """Tỷ lệ âm tiết nội dung của câu hỏi (bỏ hư từ) có trong chunk + tên văn bản; thấp hơn →
    ``khong_lien_quan`` (câu lạc đề, vd model chép ví dụ khi chunk quá ngắn)."""
    """Câu hỏi chứa ≥ N từ liên tiếp chép từ chunk → loại (``chep_nguyen_van``)."""
    near_dup: float = 0.9
    val_fraction: float = 0.05
    seed: int = 42
    as_of_cutoff: date = date(2026, 11, 3)


@dataclass(frozen=True)
class RunKey:
    model_id: str
    prompt_hash: str
    schema_hash: str


class GenQuestion(BaseModel):
    model_config = ConfigDict(extra="forbid")
    question: str
    question_type: TrainType


def output_schema(n: int) -> type[BaseModel]:
    """``{"questions": [...]}`` tối đa ``n`` câu (n nằm trong schema ⇒ đổi n là run mới)."""
    return create_model(
        "GenOut",
        __config__=ConfigDict(extra="forbid"),
        questions=(list[GenQuestion], Field(min_length=1, max_length=n)),
    )


def sha256(obj: Any) -> str:
    data = obj if isinstance(obj, str) else canonical_json(obj)
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def run_key(model_id: str, prompt: Prompt, cfg: GenerateConfig) -> RunKey:
    return RunKey(model_id, prompt.hash, sha256(output_schema(cfg.n_questions).model_json_schema()))


# --------------------------------------------------------------------------- chunk + prompt


@dataclass(frozen=True)
class GenChunk:
    chunk: Chunk
    doc_label: str
    """``Nghị định số 168/2024/NĐ-CP`` — đưa vào prompt làm ngữ cảnh."""

    @property
    def key(self) -> str:
        return self.chunk.key


LOAI_NAME = {
    "luat": "Luật",
    "nghi_dinh": "Nghị định",
    "thong_tu": "Thông tư",
    "quyet_dinh": "Quyết định",
}


def doc_label(props: Mapping[str, Any]) -> str:
    """``Luật Đường bộ số 35/2024/QH15``; ``Nghị định số 168/2024/NĐ-CP (Quy định xử phạt…)``."""
    ten = str(props.get("ten") or "").strip()
    so = str(props.get("so_hieu") or "").strip()
    loai = LOAI_NAME.get(str(props.get("loai")), "")
    if ten.startswith(("Luật", "Bộ luật")) or not loai:
        return f"{ten} số {so}".strip() if so else ten
    head = f"{loai} số {so}" if so else loai
    return f"{head} ({ten})" if ten else head


def select_chunks(store: BaseGraphStore, doc_ids: Sequence[str] | None = None) -> list[GenChunk]:
    docs = {n.id: n.props for n in store.nodes_by_label("VanBan")}
    return [GenChunk(c, doc_label(docs.get(c.doc_id, {}))) for c in iter_chunks(store, doc_ids)]


def unique_chunks(chunks: Sequence[GenChunk]) -> list[GenChunk]:
    """Một chunk cho mỗi text (chunk đầu tiên theo thứ tự văn bản)."""
    seen: set[str] = set()
    out = []
    for c in chunks:
        if c.key not in seen:
            seen.add(c.key)
            out.append(c)
    return out


def render_types() -> str:
    return "\n".join(f"- {t}: {QUESTION_TYPE_DOC[t]}" for t in TRAIN_TYPES)


def build_messages(prompt: Prompt, gc: GenChunk, cfg: GenerateConfig) -> list[dict[str, str]]:
    text = gc.chunk.text
    if len(text) > cfg.max_chunk_chars:
        text = text[: cfg.max_chunk_chars].rsplit("\n", 1)[0] + "\n…"
    return [
        {
            "role": "user",
            "content": prompt.render(
                n=str(cfg.n_questions), types=render_types(), doc=gc.doc_label, text=text
            ),
        }
    ]


# --------------------------------------------------------------------------- resume + ước tính


def _matches(rec: Mapping[str, Any], key: RunKey) -> bool:
    return (
        rec.get("model_id") == key.model_id
        and rec.get("prompt_hash") == key.prompt_hash
        and rec.get("schema_hash") == key.schema_hash
    )


def done_chunk_keys(raw: Path, key: RunKey, *, retry_format_error: bool = False) -> set[str]:
    ok = {"ok"} if retry_format_error else {"ok", "format_error"}
    return {
        str(r["chunk_key"]) for r in read_jsonl(raw) if _matches(r, key) and r.get("status") in ok
    }


def output_tokens_per_chunk(raw: Path, default: float = DEFAULT_OUT_TOKENS_PER_CHUNK) -> float:
    n = tok = 0
    for r in read_jsonl(raw):
        if r.get("status") == "ok" and not r.get("cached"):
            n += 1
            tok += int((r.get("usage") or {}).get("completion_tokens") or 0)
    return tok / n if n >= 20 and tok else default


def estimate(
    todo: Sequence[GenChunk],
    prompt: Prompt,
    cfg: GenerateConfig,
    *,
    out_per_chunk: float = DEFAULT_OUT_TOKENS_PER_CHUNK,
) -> dict[str, Any]:
    by: dict[str, dict[str, int]] = {}
    for gc in todo:
        tok = len(build_messages(prompt, gc, cfg)[0]["content"]) // 4
        for k in (f"tier:{gc.chunk.tier}", "total"):
            s = by.setdefault(k, {"calls": 0, "prompt_tokens": 0, "output_tokens": 0})
            s["calls"] += 1
            s["prompt_tokens"] += tok
            s["output_tokens"] += round(out_per_chunk)
    return dict(sorted(by.items()))


# --------------------------------------------------------------------------- chạy LLM


@dataclass
class RunOutcome:
    n_chunks: int = 0
    n_unique: int = 0
    n_todo: int = 0
    n_called: int = 0
    by_status: Counter[str] = field(default_factory=Counter)
    stopped: str | None = None
    hint: str = ""


def run_generate(
    chunks: Sequence[GenChunk],
    cfg: GenerateConfig,
    client: Client,
    raw: Path,
    *,
    max_calls: int | None = None,
    retry_format_error: bool = False,
    workers: int = 1,
    git_commit: str | None = None,
    run_meta: Mapping[str, Any] | None = None,
    resume_cmd: str = "uv run python -m scripts.qa_tool generate",
    progress: Callable[[int, int, GenChunk, LLMResult], None] | None = None,
) -> RunOutcome:
    prompt = load_prompt(cfg.prompt)
    key = run_key(client.model_id, prompt, cfg)
    uniq = unique_chunks(chunks)
    done = done_chunk_keys(raw, key, retry_format_error=retry_format_error)
    todo = [c for c in uniq if c.key not in done]
    out = RunOutcome(n_chunks=len(chunks), n_unique=len(uniq), n_todo=len(todo))
    if max_calls is not None:
        todo = todo[: max(0, max_calls)]
    schema = output_schema(cfg.n_questions)
    params = {"max_output_tokens": cfg.max_output_tokens}

    def call(gc: GenChunk) -> LLMResult:
        return client.generate(build_messages(prompt, gc, cfg), json_schema=schema, params=params)

    meta = dict(run_meta or {})
    with JsonlWriter(raw) as w:
        for gc, r in map_parallel(todo, call, workers):
            if isinstance(r, QuotaExhaustedError):
                out.stopped = "quota"
                out.hint = f"Hết quota ({r}); chạy lại để tiếp tục: {resume_cmd}"
                break
            w.write(
                {
                    "chunk_id": gc.chunk.chunk_id,
                    "chunk_key": gc.key,
                    "unit_id": gc.chunk.unit_id,
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
                    "repair_prompt_hash": r.repair_prompt_hash,
                    **({"serve": meta} if meta else {}),
                    "git_commit": git_commit,
                    "run_at": datetime.now().astimezone().isoformat(timespec="seconds"),
                }
            )
            out.n_called += 1
            out.by_status[r.status] += 1
            if progress is not None:
                progress(out.n_called, len(todo), gc, r)
    return out


# --------------------------------------------------------------------------- lọc


_VI_RE = re.compile(r"[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]")
_LEAD_RE = re.compile(r"^\s*(?:\d+[.)]|[-*•])\s*")
_CONTEXT_RE = re.compile(
    r"\b(?:điều|khoản|điểm|đoạn|văn bản|quy định|nội dung)\s+(?:này|trên|nêu trên|đã cho)\b"
    r"|\btheo đoạn\b|\bđoạn văn\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Rejected:
    chunk_id: str
    question: str
    reason: str
    detail: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "chunk_id": self.chunk_id,
            "question": self.question,
            "reason": self.reason,
            "detail": self.detail,
        }


def clean_question(q: str) -> str:
    q = unicodedata.normalize("NFC", q)
    q = _LEAD_RE.sub("", q)
    return re.sub(r"\s+", " ", q).strip().strip('"“”').strip()


def allowed_numbers(gc: GenChunk) -> set[Any]:
    """Số được phép trong câu hỏi: số trong chunk + số hiệu văn bản + số Điều/Khoản của unit."""
    return (
        parse_numbers(gc.chunk.text)
        | parse_numbers(gc.doc_label)
        | parse_numbers(gc.chunk.unit_id.replace("/", " ").replace("-", " "))
    )


STOPWORDS = frozenset(
    [
        "có",
        "không",
        "được",
        "bị",
        "thì",
        "là",
        "của",
        "và",
        "các",
        "những",
        "gì",
        "nào",
        "ai",
        "bao",
        "nhiêu",
        "như",
        "thế",
        "khi",
        "nếu",
        "phải",
        "cho",
        "với",
        "trong",
        "theo",
        "về",
        "để",
        "này",
        "đó",
        "một",
        "hay",
        "hoặc",
        "ở",
        "tại",
        "do",
        "bởi",
        "sao",
        "vậy",
        "ạ",
        "người",
    ]
)


def coverage(question: str, vocab: set[str]) -> float:
    w = [x for x in normalize(question).split() if x not in STOPWORDS]
    return sum(x in vocab for x in w) / len(w) if w else 0.0


def _word_ngrams(text: str, n: int) -> set[tuple[str, ...]]:
    w = normalize(text).split()
    return {tuple(w[i : i + n]) for i in range(len(w) - n + 1)}


def filter_questions(
    gc: GenChunk, questions: Sequence[Mapping[str, Any]], cfg: GenerateConfig
) -> tuple[list[tuple[str, str, int]], list[Rejected]]:
    """(câu giữ, loại câu, vị trí trong phản hồi LLM) + câu bị loại theo lý do. Thứ tự giữ
    nguyên; vị trí dùng làm ``qid`` (ổn định khi đổi bộ lọc)."""
    keep: list[tuple[str, str, int]] = []
    rej: list[Rejected] = []
    nums = allowed_numbers(gc)
    grams = _word_ngrams(gc.chunk.text, cfg.verbatim_ngram)
    vocab = set(normalize(f"{gc.chunk.text} {gc.doc_label}").split())
    cid = gc.chunk.chunk_id
    for pos, raw in enumerate(questions):
        q = clean_question(str(raw.get("question") or ""))
        qt = str(raw.get("question_type") or "khac")
        n_words = len(q.split())

        def bad(reason: str, detail: str = "", q: str = q) -> None:
            rej.append(Rejected(cid, q, reason, detail))

        if not q:
            bad("rong")
        elif not _VI_RE.search(q.lower()):
            bad("khong_phai_tieng_viet")
        elif n_words < cfg.min_words:
            bad("qua_ngan", f"{n_words} từ")
        elif n_words > cfg.max_words or len(q) > cfg.max_chars:
            bad("qua_dai", f"{n_words} từ / {len(q)} ký tự")
        elif extra := parse_numbers(q) - nums:
            bad("so_khong_co_trong_unit", ", ".join(sorted(str(x) for x in extra)))
        elif (cov := coverage(q, vocab)) < cfg.min_coverage:
            bad("khong_lien_quan", f"độ phủ từ {cov:.2f}")
        elif _CONTEXT_RE.search(q):
            bad("tham_chieu_ngu_canh", _CONTEXT_RE.search(q).group(0))  # type: ignore[union-attr]
        elif grams and _word_ngrams(q, cfg.verbatim_ngram) & grams:
            bad("chep_nguyen_van", f"≥ {cfg.verbatim_ngram} từ liên tiếp giống chunk")
        elif any(normalize(q) == normalize(k[0]) for k in keep):
            bad("trung_trong_chunk")
        else:
            keep.append((q, qt if qt in TRAIN_TYPES else "khac", pos))
    if len(keep) > 1:
        qs = [k[0] for k in keep]
        drop = {j for _i, j, _s in near_pairs(qs, qs, threshold=cfg.near_dup, same=True)}
        for j in sorted(drop):
            rej.append(Rejected(cid, keep[j][0], "trung_trong_chunk", "gần trùng"))
        keep = [k for j, k in enumerate(keep) if j not in drop]
    return keep, rej


# --------------------------------------------------------------------------- dựng split


def is_val_dieu(dieu_id: str, seed: int, fraction: float) -> bool:
    """Chia theo Điều, tất định, không phụ thuộc tập Điều khác (thêm/bớt Điều không đổi phép chia
    của Điều còn lại)."""
    h = int(hashlib.sha256(f"{seed}:{dieu_id}".encode()).hexdigest()[:8], 16)
    return h / 0x100000000 < fraction


def pick_as_of(c: Chunk, cutoff: date) -> date:
    """Ngày hỏi cho câu sinh từ chunk: mốc chốt nếu chunk còn hiệu lực; chunk đã hết → ngày cuối
    có hiệu lực; chunk tương lai → ngày bắt đầu."""
    if c.covers(cutoff):
        return cutoff
    if c.effective_to is not None and c.effective_to < cutoff:
        return c.effective_to
    return c.effective_from


def qid_for(chunk_id: str, i: int) -> str:
    return "gen-" + hashlib.sha1(f"{chunk_id}|{i}".encode()).hexdigest()[:12]


def _related(a: str, b: str) -> bool:
    return a == b or a.startswith(b + "/") or b.startswith(a + "/")


@dataclass
class BuildResult:
    train: list[QAItem]
    val: list[QAItem]
    rejected: list[Rejected]
    stats: dict[str, Any]


def latest_ok(raw: Path, key: RunKey) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    """Bản ghi ``ok`` mới nhất cho mỗi ``chunk_key`` + thống kê lượt gọi của khoá chạy."""
    last: dict[str, dict[str, Any]] = {}
    status: Counter[str] = Counter()
    usage: Counter[str] = Counter()
    lat: list[int] = []
    for r in read_jsonl(raw):
        if not _matches(r, key):
            continue
        status[str(r.get("status"))] += 1
        for k in ("prompt_tokens", "completion_tokens", "total_tokens"):
            usage[k] += int((r.get("usage") or {}).get(k) or 0)
        if not r.get("cached"):
            lat.append(int(r.get("latency_ms") or 0))
        if r.get("status") == "ok":
            last[str(r["chunk_key"])] = r
    stats = {
        "records_by_status": dict(sorted(status.items())),
        "usage": dict(usage),
        "latency_ms_median": statistics.median(lat) if lat else None,
        "latency_ms_max": max(lat) if lat else None,
        "n_http_calls": len(lat),
    }
    return last, stats


def build_splits(
    store: BaseGraphStore,
    chunks: Sequence[GenChunk],
    raw: Path,
    key: RunKey,
    cfg: GenerateConfig,
    *,
    test_items: Sequence[QAItem] = (),
) -> BuildResult:
    last, llm_stats = latest_ok(raw, key)
    test_gold = sorted({u for t in test_items for u in t.gold_units})
    test_q = [t.question for t in test_items]
    rows: list[tuple[GenChunk, str, str, int]] = []
    rejected: list[Rejected] = []
    seen_norm: set[str] = set()
    for gc in unique_chunks(chunks):
        rec = last.get(gc.key)
        if rec is None:
            continue
        qs = (rec.get("parsed") or {}).get("questions") or []
        keep, rej = filter_questions(gc, qs, cfg)
        rejected += rej
        for q, qt, i in keep:
            nq = normalize(q)
            if nq in seen_norm:
                rejected.append(Rejected(gc.chunk.chunk_id, q, "trung_lap"))
                continue
            seen_norm.add(nq)
            rows.append((gc, q, qt, i))
    leak = {i for i, _j, _s in near_pairs([r[1] for r in rows], test_q, threshold=cfg.near_dup)}
    train: list[QAItem] = []
    val: list[QAItem] = []
    for idx, (gc, q, qt, i) in enumerate(rows):
        c = gc.chunk
        if idx in leak:
            rejected.append(Rejected(c.chunk_id, q, "gan_trung_test"))
            continue
        d = pick_as_of(c, cfg.as_of_cutoff)
        v = store.version_at(c.unit_id, d)
        item = QAItem(
            qid=qid_for(c.chunk_id, i),
            question=q,
            as_of=d,
            question_type=qt,  # type: ignore[arg-type]
            tier=c.tier,  # type: ignore[arg-type]
            gold_units=[c.unit_id],
            gold_versions=[v.id] if v is not None else [],
            source=f"llm:{key.model_id}",
            chunk_id=c.chunk_id,
            in_test_gold=any(_related(c.unit_id, g) for g in test_gold),
        )
        (val if is_val_dieu(c.dieu_id, cfg.seed, cfg.val_fraction) else train).append(item)
    n_uniq = len(unique_chunks(chunks))
    stats = {
        "n_chunks": len(chunks),
        "n_chunks_unique": n_uniq,
        "n_chunks_done": sum(1 for gc in unique_chunks(chunks) if gc.key in last),
        "n_questions_raw": sum(
            len((r.get("parsed") or {}).get("questions") or []) for r in last.values()
        ),
        "n_train": len(train),
        "n_val": len(val),
        "n_in_test_gold": sum(bool(x.in_test_gold) for x in [*train, *val]),
        "n_dieu_train": len({_dieu(x.gold_units[0]) for x in train}),
        "n_dieu_val": len({_dieu(x.gold_units[0]) for x in val}),
        "rejected_by_reason": dict(sorted(Counter(r.reason for r in rejected).items())),
        "question_type": {
            s: dict(sorted(Counter(x.question_type for x in xs).items()))
            for s, xs in (("train", train), ("val", val))
        },
        "tier": {
            s: dict(sorted(Counter(str(x.tier) for x in xs).items()))
            for s, xs in (("train", train), ("val", val))
        },
        "llm": llm_stats,
    }
    return BuildResult(train, val, rejected, stats)


def _dieu(unit_id: str) -> str:
    return "/".join(unit_id.split("/")[:2])


def write_build(
    res: BuildResult,
    train_path: Path,
    val_path: Path,
    rejected_path: Path,
    manifest_path: Path,
    meta: Mapping[str, Any],
) -> dict[str, Any]:
    write_jsonl(train_path, [item_dict(x) for x in res.train])
    write_jsonl(val_path, [item_dict(x) for x in res.val])
    write_jsonl(rejected_path, [r.to_dict() for r in res.rejected])
    manifest = {
        **meta,
        "built_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "train_sha256": file_sha256(train_path),
        "val_sha256": file_sha256(val_path),
        **res.stats,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_bytes(
        (json.dumps(manifest, ensure_ascii=False, indent=2, default=str) + "\n").encode("utf-8")
    )
    return manifest


def file_sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else ""


def render_generate_summary(m: Mapping[str, Any]) -> str:
    llm = m.get("llm") or {}
    lines = [
        "# Sinh dữ liệu train/val (M9)",
        "",
        f"- Dựng lúc {m.get('built_at')} · commit `{m.get('git_commit')}` · model "
        f"`{m.get('model_id')}` · prompt `{str(m.get('prompt_hash'))[:12]}` · schema "
        f"`{str(m.get('schema_hash'))[:12]}`",
        f"- test.jsonl lúc dựng: `{str(m.get('test_sha256'))[:12]}` ({m.get('n_test')} câu) · "
        f"data_version `{str(m.get('data_version'))[:12]}`",
        f"- Chunk: {m.get('n_chunks'):,} ({m.get('n_chunks_unique'):,} text khác nhau), đã sinh "
        f"{m.get('n_chunks_done'):,}",
        f"- Câu thô: {m.get('n_questions_raw'):,} → train {m.get('n_train'):,} "
        f"({m.get('n_dieu_train')} Điều) · val {m.get('n_val'):,} ({m.get('n_dieu_val')} Điều)",
        f"- Positive thuộc gold_units của test (đánh dấu `in_test_gold`, không loại): "
        f"{m.get('n_in_test_gold'):,}",
        "",
        "## Bị loại",
        "",
        "| Lý do | Số |",
        "| --- | ---: |",
    ]
    rej = m.get("rejected_by_reason") or {}
    lines += [f"| {k} | {v:,} |" for k, v in rej.items()] or ["| — | 0 |"]
    lines += ["", "## Loại câu", "", "| Loại | train | val |", "| --- | ---: | ---: |"]
    qt = m.get("question_type") or {}
    for k in sorted(set(qt.get("train", {})) | set(qt.get("val", {}))):
        lines.append(
            f"| {k} | {qt.get('train', {}).get(k, 0):,} | {qt.get('val', {}).get(k, 0):,} |"
        )
    lines += ["", "## Tier", "", "| Tier | train | val |", "| --- | ---: | ---: |"]
    tr = m.get("tier") or {}
    for k in sorted(set(tr.get("train", {})) | set(tr.get("val", {}))):
        lines.append(
            f"| {k} | {tr.get('train', {}).get(k, 0):,} | {tr.get('val', {}).get(k, 0):,} |"
        )
    lines += [
        "",
        "## Lượt gọi LLM (khoá chạy hiện hành)",
        "",
        f"- Bản ghi theo trạng thái: {llm.get('records_by_status')}",
        f"- Lượt không cache: {llm.get('n_http_calls')} · latency median "
        f"{llm.get('latency_ms_median')} ms · max {llm.get('latency_ms_max')} ms",
        f"- Token: {llm.get('usage')}",
        "",
    ]
    for r in m.get("runs") or []:
        lines.append(
            f"- Lần chạy {r.get('started_at')}: {r.get('n_called')} lượt, {r.get('by_status')}, "
            f"{r.get('seconds')} s, workers {r.get('workers')}"
        )
    return "\n".join(lines) + "\n"


__all__ = [
    "TRAIN_TYPES",
    "BuildResult",
    "GenChunk",
    "GenQuestion",
    "GenerateConfig",
    "Rejected",
    "RunKey",
    "RunOutcome",
    "build_messages",
    "build_splits",
    "clean_question",
    "done_chunk_keys",
    "estimate",
    "file_sha256",
    "filter_questions",
    "is_val_dieu",
    "latest_ok",
    "output_schema",
    "output_tokens_per_chunk",
    "pick_as_of",
    "qid_for",
    "render_generate_summary",
    "run_generate",
    "run_key",
    "select_chunks",
    "unique_chunks",
    "write_build",
]
