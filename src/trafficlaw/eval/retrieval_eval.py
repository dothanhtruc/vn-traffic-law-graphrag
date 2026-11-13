"""Đánh giá truy hồi sơ bộ (M10): tập đo, chạy hệ thống, báo cáo chọn model embedding.

**Không dùng ``data/qa/test.jsonl``** (CLAUDE.md mục 10): chỉ ``val.jsonl`` (chia theo Điều) và
một tập con train lấy mẫu phân tầng theo tier (chỉ để kiểm độ ổn định — model được chọn theo val).

Hai chế độ: ``loc`` (lọc chunk hiệu lực tại ``as_of`` **trước** khi xếp hạng — như hệ thống G)
là chỉ số chính; ``khong_loc`` (xếp hạng trên mọi trạng thái) để tham khảo. Chunk chỉ tính là
đúng khi có hiệu lực tại ``as_of`` ở cả hai chế độ.
"""

from __future__ import annotations

import hashlib
from collections import defaultdict
from collections.abc import Callable, Collection, Sequence
from dataclasses import dataclass
from datetime import date
from typing import Any

from trafficlaw.eval.qa_schema import QAItem
from trafficlaw.eval.retrieval_metrics import QueryScore, score_query, summarize
from trafficlaw.retrieval.catalog import ChunkCatalog, Hit


@dataclass(frozen=True)
class EvalQuery:
    qid: str
    question: str
    as_of: date
    gold_units: tuple[str, ...]
    tier: str | None
    question_type: str


def to_queries(items: Sequence[QAItem]) -> list[EvalQuery]:
    """Bỏ câu không có gold (``ngoai_pham_vi``)."""
    return [
        EvalQuery(i.qid, i.question, i.as_of, tuple(i.gold_units), i.tier, str(i.question_type))
        for i in items
        if i.gold_units
    ]


def _rank_key(seed: int, name: str, qid: str) -> str:
    return hashlib.sha256(f"{seed}:{name}:{qid}".encode()).hexdigest()


def stratified_sample(
    items: Sequence[EvalQuery], n: int, *, seed: int, name: str
) -> list[EvalQuery]:
    """Lấy ``n`` câu phân tầng theo tier (tỷ lệ, phần dư lớn nhất); trong tầng xếp theo
    ``sha256(seed:name:qid)`` ⇒ tất định, không phụ thuộc thứ tự file. Trả theo thứ tự đầu vào."""
    if n >= len(items):
        return list(items)
    groups: dict[str, list[EvalQuery]] = defaultdict(list)
    for q in items:
        groups[str(q.tier)].append(q)
    total = len(items)
    quota = {t: n * len(g) / total for t, g in groups.items()}
    alloc = {t: int(v) for t, v in quota.items()}
    rest = n - sum(alloc.values())
    for t in sorted(quota, key=lambda t: (-(quota[t] - alloc[t]), t))[:rest]:
        alloc[t] += 1
    chosen: set[str] = set()
    for t, g in groups.items():
        g2 = sorted(g, key=lambda q: _rank_key(seed, name, q.qid))
        chosen.update(q.qid for q in g2[: alloc[t]])
    return [q for q in items if q.qid in chosen]


def fixed_sample(items: Sequence[EvalQuery], n: int, *, seed: int, name: str) -> list[EvalQuery]:
    """``n`` câu đầu theo ``sha256(seed:name:qid)`` (tập regression cố định)."""
    return sorted(items, key=lambda q: _rank_key(seed, name, q.qid))[:n]


Retriever = Callable[[Sequence[EvalQuery], Sequence[Collection[str] | None]], list[list[Hit]]]
"""(câu hỏi, tập chunk được phép theo câu — ``None`` = mọi chunk) → hit đã xếp hạng."""


def run_retriever(
    retriever: Retriever,
    queries: Sequence[EvalQuery],
    catalog: ChunkCatalog,
    *,
    filtered: bool,
) -> list[QueryScore]:
    allowed: list[Collection[str] | None] = [
        catalog.ids_at(q.as_of) if filtered else None for q in queries
    ]
    hits = retriever(queries, allowed)
    out = []
    for q, hs in zip(queries, hits, strict=True):
        rel = catalog.relevant(list(q.gold_units), q.as_of)
        out.append(score_query(q.qid, [h.chunk_id for h in hs], rel))
    return out


def evaluate_system(
    retriever: Retriever, queries: Sequence[EvalQuery], catalog: ChunkCatalog, *, seed: int = 42
) -> dict[str, Any]:
    """Chỉ số chính (lọc as_of) + Recall@5 không lọc + Recall@5 theo tier."""
    sc = run_retriever(retriever, queries, catalog, filtered=True)
    res: dict[str, Any] = summarize(sc, ci_metrics=("recall@5", "mrr@10"), seed=seed)
    unf = run_retriever(retriever, queries, catalog, filtered=False)
    res["recall@5_khong_loc"] = summarize(unf)["recall@5"] if unf else 0.0
    by_tier: dict[str, list[QueryScore]] = defaultdict(list)
    tier_of = {q.qid: str(q.tier) for q in queries}
    for s in sc:
        by_tier[tier_of[s.qid]].append(s)
    res["recall@5_tier"] = {
        t: {"n": len(v), "recall@5": summarize(v)["recall@5"]} for t, v in sorted(by_tier.items())
    }
    res["n_khong_co_chunk_dung"] = sum(
        1 for q in queries if not any(catalog.relevant(list(q.gold_units), q.as_of).values())
    )
    return res


def _pct(x: object) -> str:
    return f"{100 * float(x):.1f}" if isinstance(x, (int, float)) else "—"


def _ci(x: object) -> str:
    if isinstance(x, (tuple, list)) and len(x) == 2:
        return f"{100 * x[0]:.1f}–{100 * x[1]:.1f}"
    return "—"


def render_selection_md(
    results: dict[str, dict[str, dict[str, Any]]],
    model_info: dict[str, dict[str, Any]],
    *,
    header: Sequence[str] = (),
) -> str:
    """``results[tập][hệ thống]`` → bảng Markdown (đơn vị %)."""
    lines = ["# Chọn model embedding gốc (M10)", "", *header, ""]
    for set_name, systems in results.items():
        n = next(iter(systems.values()), {}).get("n", 0)
        lines += [
            f"## {set_name} ({n} câu, lọc as_of trước khi xếp hạng)",
            "",
            "| Hệ thống | R@1 | R@5 | CI 95% R@5 | R@10 | R@20 | MRR@10 | nDCG@10 "
            "| R@5 không lọc |",
            "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        ]
        for name, r in systems.items():
            lines.append(
                f"| {name} | {_pct(r.get('recall@1'))} | {_pct(r.get('recall@5'))} | "
                f"{_ci(r.get('recall@5_ci'))} | {_pct(r.get('recall@10'))} | "
                f"{_pct(r.get('recall@20'))} | {_pct(r.get('mrr@10'))} | "
                f"{_pct(r.get('ndcg@10'))} | {_pct(r.get('recall@5_khong_loc'))} |"
            )
        tiers = sorted({t for r in systems.values() for t in r.get("recall@5_tier", {})})
        if tiers:
            lines += [
                "",
                "**R@5 theo tier** (số câu trong ngoặc):",
                "",
                "| Hệ thống | " + " | ".join(f"{t} (n)" for t in tiers) + " |",
                "| --- |" + " ---: |" * len(tiers),
            ]
            for name, r in systems.items():
                rt = r.get("recall@5_tier", {})
                cells = [
                    f"{_pct(rt[t]['recall@5'])} ({rt[t]['n']})" if t in rt else "—" for t in tiers
                ]
                lines.append(f"| {name} | " + " | ".join(cells) + " |")
        lines.append("")
    if model_info:
        lines += [
            "## Model",
            "",
            "| Khoá | HF repo @ revision | Tham số (B) | dim | License | Token/s | VRAM đỉnh (GB) "
            "| Chunk tách cửa sổ | Cửa sổ còn bị cắt |",
            "| --- | --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |",
        ]
        for k, m in model_info.items():
            rev = (m.get("revision") or "?")[:7]
            lines.append(
                f"| {k} | `{m.get('hf_repo')}@{rev}` | {m.get('params_b', '—')} | "
                f"{m.get('dim', '—')} | {m.get('license', '—')} | {m.get('tokens_per_s', '—')} | "
                f"{m.get('peak_vram_gb', '—')} | {m.get('n_windowed', '—')} | "
                f"{m.get('n_truncated', '—')} |"
            )
        lines.append("")
    return "\n".join(lines)


__all__ = [
    "EvalQuery",
    "Retriever",
    "evaluate_system",
    "fixed_sample",
    "render_selection_md",
    "run_retriever",
    "stratified_sample",
    "to_queries",
]
