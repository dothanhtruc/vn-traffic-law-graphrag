"""Regression CI (CLAUDE.md mục 13): Recall@5 của BM25 (lọc as_of) trên 100 câu val cố định không
được giảm quá ``max_drop`` so với ``data/qa/retrieval_baseline.json``.

Chạy được trên CI (không cần ``data/graph``): corpus là bản chụp danh mục chunk
``tests/fixtures/retrieval/corpus.jsonl.gz`` (ghi cùng baseline bằng ``build_index --baseline``).
Bản regression trên 100 câu test (truy hồi đầy đủ) thuộc M13/M16.
"""

from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path

from trafficlaw.eval.qa_schema import QAItem
from trafficlaw.eval.retrieval_eval import run_retriever, to_queries
from trafficlaw.eval.retrieval_metrics import summarize
from trafficlaw.retrieval.bm25 import BM25Index
from trafficlaw.retrieval.catalog import ChunkCatalog, ChunkRecord
from trafficlaw.retrieval.config import load_retrieval_config
from trafficlaw.utils.jsonl import read_jsonl

ROOT = Path(__file__).resolve().parents[2]


def test_bm25_recall_at_5_no_regression() -> None:
    cfg = load_retrieval_config(ROOT / "configs/retrieval.yaml")
    rg = cfg.regression
    base = json.loads((ROOT / rg.baseline).read_text(encoding="utf-8"))
    corpus = ROOT / rg.corpus
    assert hashlib.sha256(corpus.read_bytes()).hexdigest() == base["corpus_sha256"], (
        "corpus đổi mà baseline chưa cập nhật — chạy build_index --baseline"
    )
    with gzip.open(corpus, "rt", encoding="utf-8") as f:
        cat = ChunkCatalog([ChunkRecord.model_validate(json.loads(x)) for x in f if x.strip()])
    assert len(cat) == base["n_chunks"]

    val = {
        q.qid: q
        for q in to_queries([QAItem.model_validate(r) for r in read_jsonl(ROOT / cfg.eval.val)])
    }
    qs = [val[i] for i in base["qids"]]
    assert len(qs) == rg.n

    bm = BM25Index.build([(c.chunk_id, c.text) for c in cat.chunks], **cfg.bm25.model_dump())

    def retr(queries, allowed):
        return [
            bm.search(q.question, rg.k, allowed=a) for q, a in zip(queries, allowed, strict=True)
        ]

    got = summarize(run_retriever(retr, qs, cat, filtered=True))[f"recall@{rg.k}"]
    assert got >= base["value"] - base["max_drop"] - 1e-9, (
        f"Recall@{rg.k} BM25 giảm: {got:.3f} < {base['value']:.3f} − {base['max_drop']}"
    )
