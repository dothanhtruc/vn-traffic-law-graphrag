"""Chunk truy hồi (CLAUDE.md mục 7): **1 phiên bản Khoản kèm các Điểm, tiền tố tiêu đề Điều**.

Điều không chia Khoản → cả Điều (kèm Điểm nằm thẳng dưới Điều) là một chunk. Khoản và các Điểm
có thể đổi phiên bản ở những ngày khác nhau ⇒ một Khoản có nhiều **trạng thái**: mỗi khoảng ngày
mà cả cây con không đổi là một chunk ``<unit_id>#<effective_from>``; khoảng liền nhau cho cùng
nội dung được gộp. Khoảng mà mọi unit đã bị bãi bỏ/chưa có hiệu lực → không có chunk.

Đầu vào chỉ là ``GraphStore`` (``data/graph``). Dùng ở M9 (sinh câu hỏi) và M10 (chỉ mục).
"""

from __future__ import annotations

import hashlib
import unicodedata
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from datetime import date, timedelta

from trafficlaw.graph.store import BaseGraphStore, GraphNode
from trafficlaw.utils.dates import parse_iso

CHUNK_LEVELS = ("Khoan", "Dieu")


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    unit_id: str
    doc_id: str
    tier: str
    dieu_id: str
    dieu_title: str
    text: str
    """``Điều N. Tiêu đề`` + dòng Khoản + các Điểm (nguyên văn phiên bản, mỗi unit một dòng)."""
    effective_from: date
    effective_to: date | None
    version_ids: tuple[str, ...]
    """PhienBan của Khoản/Điều và các Điểm có trong chunk, thứ tự văn bản."""

    @property
    def key(self) -> str:
        """Khoá nội dung (NFC) — trùng text ⇒ gọi LLM một lần."""
        return hashlib.sha256(unicodedata.normalize("NFC", self.text).encode()).hexdigest()

    def covers(self, d: date) -> bool:
        return self.effective_from <= d and (self.effective_to is None or d <= self.effective_to)


def _d(v: object) -> date | None:
    return v if isinstance(v, date) or v is None else parse_iso(str(v))


def dieu_heading(dieu: GraphNode) -> str:
    n = dieu.props.get("number")
    t = str(dieu.props.get("title") or "").strip()
    return f"Điều {n}. {t}".strip() if t else f"Điều {n}."


def _boundaries(store: BaseGraphStore, units: Sequence[str]) -> list[date]:
    out: set[date] = set()
    for u in units:
        for v in store.versions(u):
            f, t = _d(v.props.get("effective_from")), _d(v.props.get("effective_to"))
            if f is not None:
                out.add(f)
            if t is not None:
                out.add(t + timedelta(days=1))
    return sorted(out)


def _compose(
    store: BaseGraphStore, root: str, d: date, *, skip_root_heading: bool
) -> tuple[str, tuple[str, ...]] | None:
    lines: list[str] = []
    vids: list[str] = []
    for u in store.subtree(root, as_of=d):
        v = store.version_at(u, d)
        if v is None:
            continue
        text = str(v.props.get("text") or "").strip()
        if u == root and skip_root_heading:
            # Điều không chia Khoản: dòng đầu là "Điều N. Tiêu đề" (đã có ở tiền tố).
            text = "\n".join(text.split("\n")[1:]).strip()
        if text:
            lines.append(text)
        vids.append(v.id)
    if not vids:
        return None
    return "\n".join(lines), tuple(vids)


def unit_chunks(
    store: BaseGraphStore, unit_id: str, dieu: GraphNode, doc_id: str, tier: str
) -> list[Chunk]:
    units = store.subtree(unit_id)
    heading = dieu_heading(dieu)
    is_dieu = unit_id == dieu.id
    states: list[tuple[date, str, tuple[str, ...]]] = []
    for b in _boundaries(store, units):
        got = _compose(store, unit_id, b, skip_root_heading=is_dieu)
        if got is None:
            states.append((b, "", ()))
            continue
        body, vids = got
        states.append((b, f"{heading}\n{body}".strip(), vids))
    out: list[Chunk] = []
    for i, (b, text, vids) in enumerate(states):
        if not vids:
            continue
        end = states[i + 1][0] - timedelta(days=1) if i + 1 < len(states) else None
        if out and out[-1].text == text and out[-1].effective_to == b - timedelta(days=1):
            prev = out.pop()
            out.append(
                Chunk(**{**prev.__dict__, "effective_to": end, "version_ids": prev.version_ids})
            )
            continue
        out.append(
            Chunk(
                chunk_id=f"{unit_id}#{b.isoformat()}",
                unit_id=unit_id,
                doc_id=doc_id,
                tier=tier,
                dieu_id=dieu.id,
                dieu_title=str(dieu.props.get("title") or ""),
                text=text,
                effective_from=b,
                effective_to=end,
                version_ids=vids,
            )
        )
    return out


def iter_chunks(store: BaseGraphStore, doc_ids: Sequence[str] | None = None) -> Iterator[Chunk]:
    """Mọi chunk của văn bản ``indexable`` (thứ tự văn bản → Điều → Khoản → ngày)."""
    docs = sorted(
        (n.id, str(n.props.get("tier")))
        for n in store.nodes_by_label("VanBan")
        if n.props.get("indexable") and (doc_ids is None or n.id in doc_ids)
    )
    for doc, tier in docs:
        for dieu in store.nodes_by_label("Dieu", doc_id=doc):
            kids = [k for k in store.children(dieu.id) if k.rsplit("/", 1)[-1].startswith("K")]
            for u in kids or [dieu.id]:
                yield from unit_chunks(store, u, dieu, doc, tier)


def chunks_at(chunks: Sequence[Chunk], d: date) -> list[Chunk]:
    return [c for c in chunks if c.covers(d)]


__all__ = ["CHUNK_LEVELS", "Chunk", "chunks_at", "dieu_heading", "iter_chunks", "unit_chunks"]
