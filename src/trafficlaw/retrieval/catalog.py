"""Danh mục chunk của chỉ mục truy hồi (M10).

Hai loại chunk (CLAUDE.md mục 7, "Quy ước chỉ mục (M10)"):

- ``khoan``: dùng lại :func:`trafficlaw.retrieval.chunking.iter_chunks` (M9) — 1 trạng thái Khoản
  kèm các Điểm (Điều không chia Khoản → cả Điều), tiền tố ``Điều N. Tiêu đề``, mã
  ``<unit_id>#<effective_from>``.
- ``phu_luc``: mỗi phiên bản của một Phụ lục cắt theo **ranh giới dòng** (không cắt giữa dòng
  bảng) thành các phần ≤ ``max_chars`` ký tự (tính cả tiền tố; một dòng dài hơn giới hạn đứng
  riêng một phần), tiền tố ``Phụ lục N. TIÊU ĐỀ``, mã ``<PL unit_id>#<effective_from>#p<k>``.

Danh mục chứa **mọi** trạng thái (đã hết hiệu lực, tương lai). Lọc theo ngày áp dụng là việc của
M11, qua hàm dùng chung :func:`filter_as_of`.
"""

from __future__ import annotations

import bisect
from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict

from trafficlaw.graph.store import BaseGraphStore
from trafficlaw.retrieval.chunking import iter_chunks
from trafficlaw.utils.dates import parse_iso
from trafficlaw.utils.jsonl import read_jsonl, write_jsonl

ChunkKind = Literal["khoan", "phu_luc"]


class ChunkRecord(BaseModel):
    """Một dòng ``data/index/chunks.jsonl``."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    chunk_id: str
    kind: ChunkKind
    unit_id: str
    doc_id: str
    tier: str
    dieu_id: str | None
    title: str
    """Tiền tố: ``Điều N. Tiêu đề`` hoặc ``Phụ lục N. TIÊU ĐỀ``."""
    text: str
    effective_from: date
    effective_to: date | None
    version_ids: tuple[str, ...]
    part: int | None = None
    """Số thứ tự phần (1, 2, …) của chunk Phụ lục; ``None`` với chunk Khoản."""

    def covers(self, d: date) -> bool:
        return self.effective_from <= d and (self.effective_to is None or d <= self.effective_to)


@dataclass(frozen=True)
class Hit:
    """Một kết quả truy hồi. ``rank`` bắt đầu từ 1; ``source`` = ``bm25`` | ``dense:<model>`` |
    ``rrf`` …"""

    chunk_id: str
    score: float
    rank: int
    source: str


def rerank(hits: Iterable[Hit]) -> list[Hit]:
    """Đánh lại ``rank`` 1..n theo thứ tự đầu vào."""
    return [Hit(h.chunk_id, h.score, i, h.source) for i, h in enumerate(hits, 1)]


# --- Phụ lục ---------------------------------------------------------------------------------


def split_lines(lines: Sequence[str], prefix: str, max_chars: int) -> list[list[str]]:
    """Gom dòng tham lam thành các phần sao cho ``len(prefix + "\\n" + "\\n".join(phần))`` ≤
    ``max_chars``. Không bao giờ cắt giữa dòng: một dòng quá dài đứng riêng một phần."""
    if max_chars <= 0:
        raise ValueError("max_chars phải > 0")
    parts: list[list[str]] = []
    cur: list[str] = []
    size = len(prefix)
    for line in lines:
        add = len(line) + 1
        if cur and size + add > max_chars:
            parts.append(cur)
            cur, size = [], len(prefix)
        cur.append(line)
        size += add
    if cur:
        parts.append(cur)
    return parts


def phu_luc_heading(number: object, title: object) -> str:
    t = str(title or "").strip()
    return f"Phụ lục {number}. {t}".strip() if t else f"Phụ lục {number}"


def _d(v: object) -> date | None:
    return v if isinstance(v, date) or v is None else parse_iso(str(v))


def phu_luc_chunks(
    store: BaseGraphStore, doc_id: str, tier: str, max_chars: int
) -> Iterator[ChunkRecord]:
    for pl in store.nodes_by_label("PhuLuc", doc_id=doc_id):
        heading = phu_luc_heading(pl.props.get("number"), pl.props.get("title"))
        for v in store.versions(pl.id):
            if v.props.get("status") == "repealed":
                continue
            start = _d(v.props.get("effective_from"))
            if start is None:
                continue
            lines = [x.strip() for x in str(v.props.get("text") or "").split("\n") if x.strip()]
            for k, part in enumerate(split_lines(lines, heading, max_chars), 1):
                yield ChunkRecord(
                    chunk_id=f"{pl.id}#{start.isoformat()}#p{k}",
                    kind="phu_luc",
                    unit_id=pl.id,
                    doc_id=doc_id,
                    tier=tier,
                    dieu_id=None,
                    title=heading,
                    text=heading + "\n" + "\n".join(part),
                    effective_from=start,
                    effective_to=_d(v.props.get("effective_to")),
                    version_ids=(v.id,),
                    part=k,
                )


# --- Danh mục --------------------------------------------------------------------------------


def build_catalog(
    store: BaseGraphStore, *, phu_luc_max_chars: int, doc_ids: Sequence[str] | None = None
) -> list[ChunkRecord]:
    """Chunk Khoản (thứ tự M9) rồi chunk Phụ lục (theo văn bản → Phụ lục → ngày → phần) của các
    văn bản ``indexable``. Tất định."""
    out: list[ChunkRecord] = [
        ChunkRecord(
            chunk_id=c.chunk_id,
            kind="khoan",
            unit_id=c.unit_id,
            doc_id=c.doc_id,
            tier=c.tier,
            dieu_id=c.dieu_id,
            title=c.text.split("\n", 1)[0],
            text=c.text,
            effective_from=c.effective_from,
            effective_to=c.effective_to,
            version_ids=c.version_ids,
        )
        for c in iter_chunks(store, doc_ids)
    ]
    docs = sorted(
        (n.id, str(n.props.get("tier")))
        for n in store.nodes_by_label("VanBan")
        if n.props.get("indexable") and (doc_ids is None or n.id in doc_ids)
    )
    for doc, tier in docs:
        out.extend(phu_luc_chunks(store, doc, tier, phu_luc_max_chars))
    ids = [c.chunk_id for c in out]
    if len(set(ids)) != len(ids):
        raise ValueError("Trùng chunk_id trong danh mục")
    return out


def write_catalog(path: str | Path, chunks: Sequence[ChunkRecord]) -> None:
    write_jsonl(path, chunks)


def read_catalog(path: str | Path) -> list[ChunkRecord]:
    return [ChunkRecord.model_validate(r) for r in read_jsonl(path)]


def is_same_or_related(chunk_unit: str, gold_unit: str) -> bool:
    """Chunk của ``chunk_unit`` chứa ``gold_unit`` (chính nó / con cháu) hoặc là một phần của nó
    (gold là Điều, chunk là Khoản). Mã unit là đường dẫn phân cấp (``…/D6/K3/m``)."""
    return (
        chunk_unit == gold_unit
        or gold_unit.startswith(chunk_unit + "/")
        or chunk_unit.startswith(gold_unit + "/")
    )


class ChunkCatalog:
    def __init__(self, chunks: Sequence[ChunkRecord]) -> None:
        self.chunks = list(chunks)
        self.by_id = {c.chunk_id: c for c in self.chunks}
        self._at: dict[date, frozenset[str]] = {}
        self._units: list[str] | None = None

    @classmethod
    def load(cls, path: str | Path) -> ChunkCatalog:
        return cls(read_catalog(path))

    def __len__(self) -> int:
        return len(self.chunks)

    def get(self, chunk_id: str) -> ChunkRecord:
        return self.by_id[chunk_id]

    def ids_at(self, as_of: date) -> frozenset[str]:
        """Mã các chunk có hiệu lực tại ``as_of`` (có cache theo ngày)."""
        got = self._at.get(as_of)
        if got is None:
            got = frozenset(c.chunk_id for c in self.chunks if c.covers(as_of))
            self._at[as_of] = got
        return got

    def _chunks_related(self, gold: str) -> list[str]:
        """Chunk (mọi trạng thái) của unit trùng / tổ tiên / con cháu của ``gold``."""
        if self._units is None:
            self._by_unit: dict[str, list[str]] = {}
            for c in self.chunks:
                self._by_unit.setdefault(c.unit_id, []).append(c.chunk_id)
            self._units = sorted(self._by_unit)
        out: list[str] = []
        parts = gold.split("/")
        for i in range(1, len(parts) + 1):  # chính nó + tổ tiên
            out.extend(self._by_unit.get("/".join(parts[:i]), []))
        pre = gold + "/"
        j = bisect.bisect_left(self._units, pre)
        while j < len(self._units) and self._units[j].startswith(pre):  # con cháu
            out.extend(self._by_unit[self._units[j]])
            j += 1
        return out

    def relevant(self, gold_units: Sequence[str], as_of: date) -> dict[str, set[str]]:
        """gold unit → các chunk hiệu lực tại ``as_of`` chứa nó (hoặc là phần của nó)."""
        live = self.ids_at(as_of)
        return {g: {c for c in self._chunks_related(g) if c in live} for g in gold_units}


def filter_as_of(hits: Iterable[Hit], as_of: date, catalog: ChunkCatalog) -> list[Hit]:
    """Giữ các hit có hiệu lực tại ``as_of`` (khoảng ``[from, to]`` gồm hai đầu), đánh lại
    ``rank``. Chunk không có trong danh mục bị bỏ."""
    live = catalog.ids_at(as_of)
    return rerank(h for h in hits if h.chunk_id in live)


__all__ = [
    "ChunkCatalog",
    "ChunkKind",
    "ChunkRecord",
    "Hit",
    "build_catalog",
    "filter_as_of",
    "is_same_or_related",
    "phu_luc_chunks",
    "phu_luc_heading",
    "read_catalog",
    "rerank",
    "split_lines",
    "write_catalog",
]
