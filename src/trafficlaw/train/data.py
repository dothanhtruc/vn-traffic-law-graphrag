"""Dữ liệu huấn luyện M14 (hàm thuần, không torch).

- Câu train (M9, ``data/qa/train.jsonl``): mỗi câu sinh từ đúng một chunk (``chunk_id``) ⇒
  cặp (câu hỏi, positive). **Loại** câu có positive là gold / tổ tiên / con cháu gold của test
  hoặc dev (người dùng chọn 18/11/2026) — chunk đó vẫn có thể làm negative cho câu khác.
- Text positive/negative = text chunk như lúc lập chỉ mục (tiền tố tiêu đề Điều). Chunk dài hơn
  512 token (144/3.853 chunk) → lấy **một cửa sổ** của model gốc (M10, ``windows.jsonl``): cửa sổ
  có nhiều âm tiết chung với câu hỏi nhất (hoà → cửa sổ đầu). Không cắt giữa chừng.
- Batch không trùng (``no_dup_batches``): trong một batch không có hai câu cùng câu hỏi, cùng
  chunk/unit positive, hay chunk/unit xuất hiện ở hai câu (positive của câu này là negative của câu
  kia) — tránh negative giả trong MNRL in-batch. Tất định theo ``seed:epoch``.
"""

from __future__ import annotations

import hashlib
import json
import random
import unicodedata
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

from trafficlaw.eval.qa_schema import QAItem
from trafficlaw.retrieval.bm25 import tokenize
from trafficlaw.retrieval.catalog import ChunkCatalog, is_same_or_related
from trafficlaw.utils.jsonl import read_jsonl


class StaleManifestError(RuntimeError):
    """``train_manifest.json`` dựng với test khác test hiện hành."""


def file_sha256(p: str | Path) -> str:
    p = Path(p)
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else ""


def load_items(path: str | Path) -> list[QAItem]:
    return [QAItem.model_validate(r) for r in read_jsonl(path)]


def gold_units_of(path: str | Path) -> set[str]:
    """Chỉ đọc ``gold_units`` (không dùng câu hỏi/đáp án)."""
    return {g for r in read_jsonl(path) for g in (r.get("gold_units") or [])}


def check_manifest(manifest: str | Path, test: str | Path) -> str:
    """``test_sha256`` của manifest train phải trùng test hiện hành; trả sha256 đó."""
    m = json.loads(Path(manifest).read_text(encoding="utf-8"))
    cur = file_sha256(test)
    if m.get("test_sha256") != cur:
        raise StaleManifestError(
            f"train_manifest.json dựng với test {str(m.get('test_sha256'))[:12]}, test hiện hành "
            f"{cur[:12]} — chạy qa_tool build trước"
        )
    return cur


def related_any(unit: str, golds: Iterable[str]) -> bool:
    return any(is_same_or_related(unit, g) for g in golds)


@dataclass
class FilterStats:
    n_total: int = 0
    n_kept: int = 0
    n_no_chunk: int = 0
    excluded: dict[str, int] = field(default_factory=dict)
    """Tên tập → số câu bị loại (một câu có thể thuộc nhiều tập)."""
    n_excluded: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "n_total": self.n_total,
            "n_kept": self.n_kept,
            "n_no_chunk": self.n_no_chunk,
            "n_excluded": self.n_excluded,
            "excluded_by_set": dict(sorted(self.excluded.items())),
        }


def filter_items(
    items: Sequence[QAItem], catalog: ChunkCatalog, exclude: Mapping[str, set[str]]
) -> tuple[list[QAItem], FilterStats]:
    """Bỏ câu không có ``chunk_id`` trong danh mục và câu có positive liên quan gold của một tập
    trong ``exclude`` (tên tập → gold unit)."""
    st = FilterStats(n_total=len(items), excluded={k: 0 for k in exclude})
    kept: list[QAItem] = []
    for it in items:
        if not it.chunk_id or it.chunk_id not in catalog.by_id:
            st.n_no_chunk += 1
            continue
        unit = catalog.get(it.chunk_id).unit_id
        hit = [name for name, golds in exclude.items() if related_any(unit, golds)]
        for name in hit:
            st.excluded[name] += 1
        if hit:
            st.n_excluded += 1
            continue
        kept.append(it)
    st.n_kept = len(kept)
    return kept, st


# --- cửa sổ ----------------------------------------------------------------------------------


class WindowTable:
    """``chunk_id`` → danh sách text cửa sổ (theo ``k``) từ ``windows.jsonl`` (M10)."""

    def __init__(self, rows: Iterable[Mapping[str, Any]]) -> None:
        by: dict[str, list[tuple[int, str]]] = {}
        for r in rows:
            by.setdefault(str(r["chunk_id"]), []).append((int(r["k"]), str(r["text"])))
        self.by_chunk = {c: [t for _, t in sorted(v)] for c, v in by.items()}

    @classmethod
    def load(cls, path: str | Path) -> WindowTable:
        return cls(read_jsonl(path))

    def windows(self, chunk_id: str) -> list[str]:
        return self.by_chunk.get(chunk_id, [])

    def text_for(self, chunk_id: str, question: str, catalog: ChunkCatalog) -> str:
        ws = self.windows(chunk_id)
        if len(ws) <= 1:
            return catalog.get(chunk_id).text
        return best_window(question, ws)


def best_window(question: str, windows: Sequence[str]) -> str:
    """Cửa sổ có nhiều âm tiết (khác nhau) chung với câu hỏi nhất; hoà → cửa sổ đầu."""
    q = set(tokenize(question, bigrams=False))
    best, best_n = windows[0], -1
    for w in windows:
        n = len(q & set(tokenize(w, bigrams=False)))
        if n > best_n:
            best, best_n = w, n
    return best


# --- ví dụ huấn luyện ------------------------------------------------------------------------


@dataclass(frozen=True)
class TrainExample:
    qid: str
    question: str
    as_of: date
    pos_id: str
    pos_unit: str
    pos_text: str
    neg_ids: tuple[str, ...]
    neg_units: tuple[str, ...]
    neg_texts: tuple[str, ...]


def build_examples(
    items: Sequence[QAItem],
    catalog: ChunkCatalog,
    windows: WindowTable,
    negatives: Mapping[str, Sequence[str]],
    n_neg: int,
) -> list[TrainExample]:
    """``negatives``: qid → chunk negative (khó nhất trước, đã lọc). Câu chưa khai thác negative
    → không có hard negative (vẫn dùng được với in-batch negatives của embedder)."""
    out: list[TrainExample] = []
    for it in items:
        assert it.chunk_id is not None
        pos = catalog.get(it.chunk_id)
        negs = [c for c in negatives.get(it.qid, []) if c in catalog.by_id][:n_neg]
        out.append(
            TrainExample(
                qid=it.qid,
                question=it.question,
                as_of=it.as_of,
                pos_id=pos.chunk_id,
                pos_unit=pos.unit_id,
                pos_text=windows.text_for(pos.chunk_id, it.question, catalog),
                neg_ids=tuple(negs),
                neg_units=tuple(catalog.get(c).unit_id for c in negs),
                neg_texts=tuple(windows.text_for(c, it.question, catalog) for c in negs),
            )
        )
    return out


def examples_sha256(examples: Sequence[TrainExample]) -> str:
    h = hashlib.sha256()
    for e in examples:
        h.update(
            json.dumps(
                [e.qid, e.question, e.pos_id, e.pos_text, list(e.neg_ids), list(e.neg_texts)],
                ensure_ascii=False,
            ).encode()
        )
        h.update(b"\n")
    return h.hexdigest()


def _norm_q(q: str) -> str:
    return " ".join(unicodedata.normalize("NFC", q).lower().split())


def _keys(e: TrainExample) -> set[str]:
    ks = {f"q:{_norm_q(e.question)}", f"c:{e.pos_id}", f"u:{e.pos_unit}"}
    ks.update(f"c:{c}" for c in e.neg_ids)
    ks.update(f"u:{u}" for u in e.neg_units)
    return ks


def epoch_order(n: int, seed: int, epoch: int) -> list[int]:
    order = list(range(n))
    random.Random(f"{seed}:{epoch}").shuffle(order)
    return order


def no_dup_batches(
    examples: Sequence[TrainExample], batch_size: int, *, seed: int, epoch: int
) -> list[list[int]]:
    """Chia (đã xáo theo ``seed:epoch``) thành batch ≤ ``batch_size`` không có khoá trùng (xem
    docstring module); câu xung đột dời sang batch sau. Mọi câu xuất hiện đúng một lần."""
    keys = [_keys(e) for e in examples]
    remaining = epoch_order(len(examples), seed, epoch)
    batches: list[list[int]] = []
    while remaining:
        batch: list[int] = []
        seen: set[str] = set()
        rest: list[int] = []
        for i in remaining:
            if len(batch) < batch_size and not (keys[i] & seen):
                batch.append(i)
                seen |= keys[i]
            else:
                rest.append(i)
        batches.append(batch)
        remaining = rest
    return batches


def plain_batches(n: int, batch_size: int, *, seed: int, epoch: int) -> list[list[int]]:
    order = epoch_order(n, seed, epoch)
    return [order[i : i + batch_size] for i in range(0, n, batch_size)]


def training_plan(batches_of_epoch, epochs: int) -> list[tuple[int, list[int]]]:
    """[(epoch, batch)] cho mọi epoch — số bước cố định, tính lại được khi resume."""
    return [(ep, b) for ep in range(epochs) for b in batches_of_epoch(ep)]


__all__ = [
    "FilterStats",
    "StaleManifestError",
    "TrainExample",
    "WindowTable",
    "best_window",
    "build_examples",
    "check_manifest",
    "epoch_order",
    "examples_sha256",
    "file_sha256",
    "filter_items",
    "gold_units_of",
    "load_items",
    "no_dup_batches",
    "plain_batches",
    "related_any",
    "training_plan",
]
