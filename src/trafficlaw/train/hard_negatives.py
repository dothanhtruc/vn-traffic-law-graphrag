"""Hard negative cho M14 (tính trước, lưu ``data/train/hard_negatives.jsonl``; không tính trong
vòng train — CLAUDE.md mục 9).

Nguồn ứng viên (đều lọc chunk hiệu lực tại ``as_of`` của câu):

1. **dense** top-k của model embedding **gốc** (FAISS M10, vector câu hỏi trong cache M10);
2. **bm25** top-k (M10);
3. **anh em**: Khoản cùng Điều (cạnh THUOC cùng cha trên đồ thị ≙ cùng ``dieu_id`` trong danh
   mục chunk), gần vị trí positive nhất.

Trộn vòng tròn dense → bm25 → anh em, bỏ trùng, tối đa ``max_candidates``. Loại **negative
giả** trước khi chấm: chunk ngoài hiệu lực, chunk của unit trùng / tổ tiên / con cháu của gold
hoặc positive, chunk cùng unit (trạng thái khác), chunk cùng text với positive. Sau đó chấm bằng
**reranker gốc** (cache điểm M11): bỏ negative có điểm ≥ điểm positive − ``delta``. Còn lại xếp
theo điểm giảm dần (khó nhất trước), hoà → ``chunk_id``; giữ ``keep`` negative.
"""

from __future__ import annotations

import unicodedata
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import date
from typing import Any

from trafficlaw.retrieval.catalog import ChunkCatalog
from trafficlaw.train.config import MiningSpec, params_hash
from trafficlaw.train.data import related_any

ScoreFn = Callable[[str, Sequence[tuple[str, str]]], Mapping[str, float]]
"""(câu hỏi, [(chunk_id, text)]) → điểm reranker theo chunk (logit, điểm chunk = max cửa sổ)."""

REASONS = ("ngoai_hieu_luc", "lien_quan_gold", "cung_unit", "trung_text")


@dataclass(frozen=True)
class Candidate:
    chunk_id: str
    sources: tuple[str, ...]


def sibling_chunks(catalog: ChunkCatalog, pos_id: str, as_of: date, k: int) -> list[str]:
    """Chunk Khoản cùng Điều với positive, hiệu lực tại ``as_of``, gần positive nhất theo thứ tự
    Khoản trong Điều (hoà → Khoản đứng trước)."""
    pos = catalog.get(pos_id)
    if pos.dieu_id is None or k <= 0:
        return []
    same = [c for c in catalog.chunks if c.dieu_id == pos.dieu_id]
    unit_pos: dict[str, int] = {}
    for c in same:
        unit_pos.setdefault(c.unit_id, len(unit_pos))
    live = catalog.ids_at(as_of)
    sib = [c for c in same if c.unit_id != pos.unit_id and c.chunk_id in live]
    p = unit_pos[pos.unit_id]
    sib.sort(key=lambda c: (abs(unit_pos[c.unit_id] - p), unit_pos[c.unit_id], c.chunk_id))
    return [c.chunk_id for c in sib[:k]]


def _norm_text(t: str) -> str:
    return " ".join(unicodedata.normalize("NFC", t).split())


def exclusion_reason(
    catalog: ChunkCatalog, cand: str, pos_id: str, gold_units: Sequence[str], as_of: date
) -> str | None:
    """Lý do ứng viên không được làm negative (``None`` = dùng được)."""
    c, pos = catalog.get(cand), catalog.get(pos_id)
    if not c.covers(as_of):
        return "ngoai_hieu_luc"
    if related_any(c.unit_id, [*gold_units, pos.unit_id]):
        return "cung_unit" if c.unit_id == pos.unit_id else "lien_quan_gold"
    if _norm_text(c.text) == _norm_text(pos.text):
        return "trung_text"
    return None


def merge_candidates(
    sources: Sequence[tuple[str, Sequence[str]]],
    max_n: int,
    reason: Callable[[str], str | None],
) -> tuple[list[Candidate], dict[str, int]]:
    """Trộn vòng tròn theo hạng; ứng viên bị loại được đếm theo lý do (mỗi chunk một lần)."""
    got: dict[str, list[str]] = {}
    order: list[str] = []
    dropped: dict[str, int] = {r: 0 for r in REASONS}
    bad: set[str] = set()
    depth = max((len(ids) for _, ids in sources), default=0)
    for i in range(depth):
        for name, ids in sources:
            if i >= len(ids):
                continue
            cid = ids[i]
            if cid in bad:
                continue
            if cid in got:
                if name not in got[cid]:
                    got[cid].append(name)
                continue
            r = reason(cid)
            if r is not None:
                bad.add(cid)
                dropped[r] += 1
                continue
            got[cid] = [name]
            order.append(cid)
    return [Candidate(c, tuple(got[c])) for c in order[:max_n]], dropped


def choose_negatives(
    pos_score: float, scored: Sequence[tuple[str, float]], delta: float, keep: int
) -> tuple[list[str], int]:
    """Bỏ ứng viên có điểm ≥ ``pos_score − delta``; còn lại xếp khó nhất trước. Trả (negative,
    số bị bỏ vì gần positive)."""
    ok = [(c, s) for c, s in scored if s < pos_score - delta]
    ok.sort(key=lambda x: (-x[1], x[0]))
    return [c for c, _ in ok[:keep]], len(scored) - len(ok)


def mining_params(spec: MiningSpec, extra: Mapping[str, Any] | None = None) -> str:
    """Hash tham số khai thác (khoá resume): đổi tham số ⇒ khai thác lại."""
    d = spec.model_dump(exclude={"data"})
    return params_hash({**d, **(extra or {}), "version": "m14-1"})


def mine_one(
    *,
    qid: str,
    question: str,
    as_of: date,
    pos_id: str,
    gold_units: Sequence[str],
    catalog: ChunkCatalog,
    dense_ids: Sequence[str],
    bm25_ids: Sequence[str],
    spec: MiningSpec,
    score: ScoreFn,
    phash: str,
) -> dict[str, Any]:
    """Một bản ghi ``hard_negatives.jsonl``."""
    sib = sibling_chunks(catalog, pos_id, as_of, spec.siblings_k)
    cands, dropped = merge_candidates(
        [("dense", dense_ids[: spec.dense_k]), ("bm25", bm25_ids[: spec.bm25_k]), ("anh_em", sib)],
        spec.max_candidates,
        lambda c: exclusion_reason(catalog, c, pos_id, gold_units, as_of),
    )
    texts = [(pos_id, catalog.get(pos_id).text)] + [
        (c.chunk_id, catalog.get(c.chunk_id).text) for c in cands
    ]
    sc = score(question, texts)
    pos_score = float(sc[pos_id])
    scored = [(c.chunk_id, float(sc[c.chunk_id])) for c in cands]
    negs, n_close = choose_negatives(pos_score, scored, spec.delta, spec.keep)
    dropped["gan_positive"] = n_close
    return {
        "qid": qid,
        "chunk_id": pos_id,
        "as_of": as_of.isoformat(),
        "params_hash": phash,
        "pos_score": pos_score,
        "candidates": [
            {"chunk_id": c.chunk_id, "sources": list(c.sources), "score": s}
            for c, (_, s) in zip(cands, scored, strict=True)
        ],
        "dropped": dropped,
        "negatives": negs,
    }


def negatives_map(rows: Sequence[Mapping[str, Any]], phash: str | None = None) -> dict[str, list]:
    """qid → negative (bản ghi mới nhất; ``phash`` → chỉ bản ghi cùng tham số)."""
    out: dict[str, list] = {}
    for r in rows:
        if phash is None or r.get("params_hash") == phash:
            out[str(r["qid"])] = list(r["negatives"])
    return out


def mining_stats(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    n = len(rows)
    drop: dict[str, int] = {}
    src: dict[str, int] = {}
    n_neg = [len(r["negatives"]) for r in rows]
    for r in rows:
        for k, v in r["dropped"].items():
            drop[k] = drop.get(k, 0) + int(v)
        negs = set(r["negatives"])
        for c in r["candidates"]:
            if c["chunk_id"] in negs:
                for s in c["sources"]:
                    src[s] = src.get(s, 0) + 1
    return {
        "n_questions": n,
        "n_candidates": sum(len(r["candidates"]) for r in rows),
        "n_negatives": sum(n_neg),
        "n_without_negative": sum(1 for x in n_neg if x == 0),
        "mean_negatives": round(sum(n_neg) / n, 3) if n else 0.0,
        "dropped": dict(sorted(drop.items())),
        "negative_sources": dict(sorted(src.items())),
        "mean_pos_score": round(sum(float(r["pos_score"]) for r in rows) / n, 4) if n else None,
    }


__all__ = [
    "Candidate",
    "REASONS",
    "ScoreFn",
    "choose_negatives",
    "exclusion_reason",
    "merge_candidates",
    "mine_one",
    "mining_params",
    "mining_stats",
    "negatives_map",
    "sibling_chunks",
]
