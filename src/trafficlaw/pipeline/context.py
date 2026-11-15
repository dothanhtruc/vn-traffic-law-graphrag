"""Dựng ngữ cảnh cho LLM từ kết quả ``retrieve()`` (M12, người dùng duyệt 15/11/2026).

Nguồn = top ``final_k`` hit của M11 (``S1…S5``) + **nguồn bổ sung từ đồ thị**: tối đa
``max_graph_extra`` (3) chunk trong ``pool`` *chỉ* đến từ đồ thị (mọi provenance là ``graph``),
có seed thuộc top hit, khi loại câu ∈ ``graph_extra_types`` (``muc_phat``, ``tru_diem``,
``bien_phap``, ``da_buoc``). Thứ tự ưu tiên: loại cạnh theo ``graph_edge_priority``
(BI_XU_PHAT/BI_TRU_DIEM → DAN_CHIEU → khác), rồi điểm rerank, rồi thứ tự pool. Khi lọc hiệu lực,
chunk bổ sung phải phủ ``as_of`` và unit gốc còn phiên bản tại ``as_of`` (như chốt cuối M11).

Mỗi nguồn hiển thị: văn bản (số hiệu + tên), Điều/Khoản đọc được, khoảng hiệu lực của trạng thái,
có hiệu lực tại ngày áp dụng hay không, các lần sửa đổi/bãi bỏ (``amendments_of``) có hiệu lực
tới ngày áp dụng, nguyên văn chunk.

**Ngân sách token** đếm bằng ước lượng tất định ``ceil(len / chars_per_token)`` (tiếng Việt với
tokenizer Qwen3 ≈ 1,74 ký tự/token — M9 đo 2,3× ước ``len/4``) để ngữ cảnh, prompt và khoá cache
không phụ thuộc việc có cài ``tokenizers`` hay không; ``--dry-run`` đếm token thật. Nguồn top
vượt ngân sách bị cắt theo dòng (đánh dấu ``truncated``); nguồn bổ sung không vừa thì bỏ.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from trafficlaw.graph.store import BaseGraphStore
from trafficlaw.retrieval.catalog import ChunkCatalog
from trafficlaw.retrieval.retrieve import RetrievalResult
from trafficlaw.verify.citations import CitableSource, doc_label, unit_label
from trafficlaw.verify.numbers import NumberFact, SourceText


class ContextConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    graph_extra_types: list[str] = Field(
        default_factory=lambda: ["muc_phat", "tru_diem", "bien_phap", "da_buoc"]
    )
    max_graph_extra: int = 3
    graph_edge_priority: list[str] = Field(
        default_factory=lambda: ["BI_XU_PHAT", "BI_TRU_DIEM", "DAN_CHIEU"]
    )
    token_budget: int = 6000
    """Ngân sách cho phần nguồn + bảng con số (hồ sơ 16k)."""
    token_budget_shared: int = 4000
    """Hồ sơ serve ``qwen3-14b-awq-shared`` (``max_model_len`` 8192)."""
    chars_per_token: float = 1.74
    min_lines_truncated: int = 3


class AmendmentNote(BaseModel):
    model_config = ConfigDict(extra="forbid")
    edge_type: str
    doc_id: str
    so_hieu: str
    unit_id: str
    effective_from: date | None
    thao_tac: str | None = None


class Source(BaseModel):
    """Một nguồn ``S#`` đưa vào ngữ cảnh."""

    model_config = ConfigDict(extra="forbid")
    sid: str
    chunk_id: str
    unit_id: str
    doc_id: str
    kind: str
    version_ids: list[str]
    effective_from: date
    effective_to: date | None
    origin: str
    """``top`` (hit của retrieve) | ``graph`` (bổ sung từ đồ thị)."""
    rank: int | None = None
    score: float | None = None
    edge_type: str | None = None
    doc_label: str
    doc_name: str | None = None
    label: str
    """``khoản 4 Điều 6`` / ``Phụ lục 1 (phần 2)``."""
    in_effect: bool
    amendments: list[AmendmentNote] = Field(default_factory=list)
    text: str
    truncated: bool = False

    def citable(self) -> CitableSource:
        return CitableSource(self.sid, self.chunk_id, self.unit_id, self.doc_label)

    def number_source(self, as_of: date) -> SourceText:
        covers = self.effective_from <= as_of and (
            self.effective_to is None or as_of <= self.effective_to
        )
        return SourceText(
            self.sid, self.text, tuple(self.version_ids), as_of if covers else self.effective_from
        )


def est_tokens(text: str, chars_per_token: float) -> int:
    return math.ceil(len(text) / chars_per_token)


def _graph_only(sources: Sequence[object]) -> bool:
    return bool(sources) and all(getattr(s, "source", None) == "graph" for s in sources)


def pick_graph_extras(
    result: RetrievalResult, catalog: ChunkCatalog, store: BaseGraphStore, cfg: ContextConfig
) -> list[tuple[str, str]]:
    """(chunk_id, loại cạnh) bổ sung từ đồ thị theo thứ tự ưu tiên."""
    qtype = result.analysis.question_type
    if cfg.max_graph_extra <= 0 or qtype not in cfg.graph_extra_types:
        return []
    top = {h.chunk_id for h in result.hits}
    prio = {t: i for i, t in enumerate(cfg.graph_edge_priority)}
    cands = []
    for pos, p in enumerate(result.pool):
        if p.chunk_id in top or not _graph_only(p.sources):
            continue
        seeds = [s for s in p.sources if s.seed in top]
        if not seeds:
            continue
        if result.validity_filter:
            ch = catalog.get(p.chunk_id)
            if not ch.covers(result.as_of) or store.version_at(ch.unit_id, result.as_of) is None:
                continue
        best = min(seeds, key=lambda s: prio.get(str(s.edge_type), len(prio)))
        score = p.rerank_score if p.rerank_score is not None else float("-inf")
        cands.append((prio.get(str(best.edge_type), len(prio)), -score, pos, p.chunk_id, best))
    cands.sort(key=lambda x: x[:3])
    return [(c[3], str(c[4].edge_type)) for c in cands[: cfg.max_graph_extra]]


def amendment_notes(
    store: BaseGraphStore, unit_ids: Sequence[str], as_of: date, docs: dict[str, dict[str, object]]
) -> list[AmendmentNote]:
    """SUA_DOI/BAI_BO/THAY_THE cấp unit trỏ tới các unit của chunk, có hiệu lực từ ≤ ``as_of``."""
    out: list[AmendmentNote] = []
    seen: set[tuple[str, str, str]] = set()
    for u in unit_ids:
        for e in store.amendments_of(u):
            ef = e.props.get("effective_from")
            d = date.fromisoformat(str(ef)) if ef else None
            if d is None or d > as_of:
                continue
            key = (e.type, e.src, str(ef))
            if key in seen:
                continue
            seen.add(key)
            doc = docs.get(e.src, {})
            out.append(
                AmendmentNote(
                    edge_type=e.type,
                    doc_id=e.src,
                    so_hieu=str(doc.get("so_hieu") or e.src),
                    unit_id=u,
                    effective_from=d,
                    thao_tac=str(e.props.get("thao_tac")) if e.props.get("thao_tac") else None,
                )
            )
    return sorted(out, key=lambda a: (a.effective_from or date.min, a.doc_id, a.unit_id))


def _truncate(text: str, max_chars: int, min_lines: int) -> str | None:
    lines = text.split("\n")
    out: list[str] = []
    n = 0
    for ln in lines:
        if n + len(ln) + 1 > max_chars:
            break
        out.append(ln)
        n += len(ln) + 1
    if len(out) < min(min_lines, len(lines)):
        return None
    return "\n".join(out) + "\n[… phần còn lại của khoản bị lược bớt do giới hạn độ dài …]"


def select_sources(
    result: RetrievalResult,
    catalog: ChunkCatalog,
    store: BaseGraphStore,
    cfg: ContextConfig,
    *,
    docs: dict[str, dict[str, object]],
    budget: int | None = None,
) -> list[Source]:
    """Danh sách nguồn ``S1…`` (top hit trước, bổ sung đồ thị sau) trong ngân sách token."""
    budget = cfg.token_budget if budget is None else budget
    picks: list[tuple[str, str, int | None, float | None, str | None]] = [
        (h.chunk_id, "top", h.rank, h.score, None) for h in result.hits
    ]
    for cid, et in pick_graph_extras(result, catalog, store, cfg):
        rr = next((p.rerank_score for p in result.pool if p.chunk_id == cid), None)
        picks.append((cid, "graph", None, rr, et))
    out: list[Source] = []
    used = 0
    for cid, origin, rank, score, et in picks:
        ch = catalog.get(cid)
        doc = docs.get(ch.doc_id, {})
        units = sorted({v.split("@", 1)[0] for v in ch.version_ids})
        text = ch.text
        src = Source(
            sid=f"S{len(out) + 1}",
            chunk_id=cid,
            unit_id=ch.unit_id,
            doc_id=ch.doc_id,
            kind=ch.kind,
            version_ids=list(ch.version_ids),
            effective_from=ch.effective_from,
            effective_to=ch.effective_to,
            origin=origin,
            rank=rank,
            score=score,
            edge_type=et,
            doc_label=doc_label(doc) if doc else ch.doc_id,
            doc_name=str(doc.get("ten")) if doc.get("ten") else None,
            label=unit_label(ch.unit_id) or ch.title,
            in_effect=ch.covers(result.as_of),
            amendments=amendment_notes(store, units, result.as_of, docs),
            text=text,
        )
        cost = est_tokens(render_source(src), cfg.chars_per_token)
        if used + cost > budget:
            if origin != "top":
                continue
            left = max(0, budget - used) * cfg.chars_per_token - (
                len(render_source(src)) - len(text)
            )
            cut = _truncate(text, int(left), cfg.min_lines_truncated)
            if cut is None:
                continue
            src.text, src.truncated = cut, True
            cost = est_tokens(render_source(src), cfg.chars_per_token)
        used += cost
        out.append(src)
    return out


# --------------------------------------------------------------------------- hiển thị


def _d(d: date | None) -> str:
    return d.strftime("%d/%m/%Y") if d else "nay"


def render_source(s: Source) -> str:
    head = f"[{s.sid}] {s.doc_label}"
    if s.doc_name and not s.doc_label.startswith(s.doc_name):
        head += f" — {s.doc_name}"
    head += f"\nVị trí: {s.label}"
    eff = f"Trạng thái này áp dụng từ {_d(s.effective_from)} đến {_d(s.effective_to)}"
    eff += (
        " (có hiệu lực tại ngày áp dụng)"
        if s.in_effect
        else " (KHÔNG có hiệu lực tại ngày áp dụng)"
    )
    lines = [head, eff]
    if s.amendments:
        am = "; ".join(
            f"{'bãi bỏ' if a.edge_type == 'BAI_BO' else 'sửa đổi/bổ sung'} bởi {a.so_hieu}"
            f" (từ {_d(a.effective_from)}, {unit_label(a.unit_id)})"
            for a in s.amendments
        )
        lines.append(f"Lịch sử sửa đổi: {am}")
    if s.origin == "graph":
        lines.append("(Nguồn bổ sung qua liên kết pháp lý với nguồn khác)")
    lines.append("Nội dung:")
    lines.append(s.text)
    return "\n".join(lines)


def render_sources(sources: Sequence[Source]) -> str:
    return "\n\n".join(render_source(s) for s in sources) if sources else "(không có nguồn)"


def render_number_table(facts: Sequence[NumberFact]) -> str:
    if not facts:
        return "(không có con số nào trong nguồn)"
    lines = []
    for f in facts:
        where = f" — nêu tại {unit_label(f.unit_id)}" if f.unit_id else ""
        applies = ""
        if f.applies_to:
            applies = " — áp dụng cho hành vi tại " + ", ".join(
                unit_label(u) for u in f.applies_to[:6]
            )
            if len(f.applies_to) > 6:
                applies += f" và {len(f.applies_to) - 6} điểm khác"
        lines.append(f"{{{f.id}}} [{f.source}] {f.description}: {f.rendered}{where}{applies}")
    return "\n".join(lines)


__all__ = [
    "AmendmentNote",
    "ContextConfig",
    "Source",
    "amendment_notes",
    "est_tokens",
    "pick_graph_extras",
    "render_number_table",
    "render_source",
    "render_sources",
    "select_sources",
]
