"""Phần I/O dùng chung cho script M14 (``mine_negatives``, ``train_embedding``,
``train_reranker``): đọc danh mục chunk, câu train (lọc), negative, val, pool."""

from __future__ import annotations

import hashlib
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from trafficlaw.eval.qa_schema import QAItem
from trafficlaw.eval.retrieval_eval import EvalQuery, to_queries
from trafficlaw.retrieval.catalog import ChunkCatalog
from trafficlaw.train.config import DataSpec
from trafficlaw.train.data import (
    FilterStats,
    TrainExample,
    WindowTable,
    build_examples,
    check_manifest,
    examples_sha256,
    file_sha256,
    filter_items,
    gold_units_of,
    load_items,
)
from trafficlaw.train.hard_negatives import negatives_map
from trafficlaw.utils.jsonl import read_jsonl


class MissingNegativesError(RuntimeError):
    pass


def rank_sample(items: Sequence[Any], n: int | None, name: str, key=lambda x: x.qid) -> list:
    """``n`` phần tử đầu theo ``sha256(42:name:qid)`` (tất định, không phụ thuộc thứ tự file),
    trả theo thứ tự đầu vào."""
    if n is None or n >= len(items):
        return list(items)

    def rank(q: str) -> str:
        return hashlib.sha256(f"42:{name}:{q}".encode()).hexdigest()

    keep = set(sorted((key(x) for x in items), key=rank)[:n])
    return [x for x in items if key(x) in keep]


def kept_items(
    root: Path, data: DataSpec, catalog: ChunkCatalog
) -> tuple[list[QAItem], FilterStats, str]:
    """Câu train sau khi loại theo gold test/dev; kiểm ``train_manifest`` khớp test hiện hành."""
    test_sha = check_manifest(root / data.train_manifest, root / data.test)
    exclude = {Path(p).stem: gold_units_of(root / p) for p in data.exclude_gold}
    items, st = filter_items(load_items(root / data.train), catalog, exclude)
    return items, st, test_sha


@dataclass
class TrainData:
    catalog: ChunkCatalog
    examples: list[TrainExample]
    stats: FilterStats
    val: list[EvalQuery]
    test_sha256: str
    negatives_sha256: str
    window_rows: list[dict[str, Any]]

    def fingerprint(self) -> dict[str, Any]:
        return {
            "examples_sha256": examples_sha256(self.examples),
            "n_examples": len(self.examples),
            "val": [q.qid for q in self.val][:5] + [str(len(self.val))],
            "test_sha256": self.test_sha256,
            "negatives_sha256": self.negatives_sha256,
        }

    def info(self) -> dict[str, Any]:
        return {
            "filter": self.stats.to_dict(),
            "n_val": len(self.val),
            "test_sha256": self.test_sha256,
            "negatives_sha256": self.negatives_sha256,
            "examples_sha256": examples_sha256(self.examples),
        }


def load_train_data(
    root: Path,
    data: DataSpec,
    n_neg: int,
    *,
    n_items: int | None = None,
    n_val: int | None = None,
    require_negatives: bool = True,
) -> TrainData:
    catalog = ChunkCatalog.load(root / data.chunks)
    items, st, test_sha = kept_items(root, data, catalog)
    items = rank_sample(items, n_items or data.max_items, "m14_train")
    neg_path = root / data.negatives
    if neg_path.is_file():
        negs = negatives_map(list(read_jsonl(neg_path)))
    elif require_negatives:
        raise MissingNegativesError(f"thiếu {neg_path} — chạy scripts.mine_negatives trước")
    else:
        negs = {}
    win_rows = list(read_jsonl(root / data.windows))
    examples = build_examples(items, catalog, WindowTable(win_rows), negs, n_neg)
    val = to_queries(load_items(root / data.val))
    val = rank_sample(val, n_val, "m14_val")
    return TrainData(
        catalog=catalog,
        examples=examples,
        stats=st,
        val=val,
        test_sha256=test_sha,
        negatives_sha256=file_sha256(neg_path),
        window_rows=win_rows,
    )


__all__ = ["MissingNegativesError", "TrainData", "kept_items", "load_train_data", "rank_sample"]
