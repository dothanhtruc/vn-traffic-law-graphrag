"""M14: khai thác hard negative cho fine-tune (dense gốc + BM25 + Khoản anh em, lọc bằng reranker
gốc) → ``data/train/hard_negatives.jsonl`` (resume theo ``(qid, params_hash)``).

    uv run --group tok python -m scripts.mine_negatives --dry-run   # cặp rerank, giờ GPU, VND
    uv run --no-sync python -m scripts.mine_negatives --gpu         # máy thuê: encode + rerank
    uv run python -m scripts.mine_negatives                         # local: dựng lại từ cache

Đầu vào: ``data/index/{chunks.jsonl, bm25, faiss/<embed_key>, vectors/<embed_key>}``, cache rerank
M11 ``data/index/rerank/<reranker_key>/``, ``data/qa/{train,test,dev_multi}.jsonl`` (test/dev chỉ
lấy ``gold_units`` để loại câu train), ``data/qa/train_manifest.json``.
Mã thoát: 1 = lỗi; 2 = thiếu vector câu hỏi / điểm rerank (chạy với ``--gpu``).
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from collections.abc import Sequence
from pathlib import Path

from trafficlaw.retrieval.bm25 import BM25Index
from trafficlaw.retrieval.config import load_retrieval_config
from trafficlaw.retrieval.dense import FaissIndex, VectorCache, cache_key, encode_cached
from trafficlaw.retrieval.index_pipeline import IndexPaths, MissingVectorsError, file_sha256
from trafficlaw.retrieval.rerank import (
    MissingRerankScoresError,
    RerankCache,
    pair_key,
    rerank_scores,
)
from trafficlaw.train.config import load_mining_config
from trafficlaw.train.hard_negatives import mine_one, mining_params, mining_stats
from trafficlaw.train.pipeline import kept_items, rank_sample
from trafficlaw.train.run_log import gpu_cost, now_iso
from trafficlaw.utils.git import git_commit
from trafficlaw.utils.jsonl import JsonlWriter, append_jsonl, read_jsonl
from trafficlaw.utils.logging import setup_logging
from trafficlaw.utils.seed import set_seed

REPO_ROOT = Path(__file__).resolve().parents[1]
logger = logging.getLogger("mine_negatives")


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--config", default="configs/hard_negatives.yaml")
    ap.add_argument("--retrieval-config", default="configs/retrieval.yaml")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--gpu", action="store_true", help="nạp embedder/reranker gốc (máy thuê)")
    ap.add_argument("--limit", type=int, help="chỉ N câu (chạy thử)")
    args = ap.parse_args(argv)
    setup_logging()
    set_seed(42)
    root = REPO_ROOT
    spec = load_mining_config(root / args.config)
    rcfg = load_retrieval_config(root / args.retrieval_config)
    paths = IndexPaths(root / rcfg.index_dir)
    from trafficlaw.retrieval.catalog import ChunkCatalog

    catalog = ChunkCatalog.load(root / spec.data.chunks)
    items, st, test_sha = kept_items(root, spec.data, catalog)
    items = rank_sample(items, args.limit, "m14_mine")
    espec = rcfg.spec(spec.embed_key)
    rspec = rcfg.reranker(spec.reranker_key)
    phash = mining_params(
        spec,
        {
            "embed": [espec.hf_repo, espec.revision],
            "reranker": [rspec.hf_repo, rspec.revision],
            "catalog_sha256": file_sha256(root / spec.data.chunks),
        },
    )
    out = root / spec.data.negatives
    done = {
        r["qid"] for r in read_jsonl(out) if r.get("params_hash") == phash
    } if out.is_file() else set()  # fmt: skip
    todo = [it for it in items if it.qid not in done]
    print(
        f"câu train: {st.n_total} → giữ {st.n_kept} (loại {st.n_excluded}:"
        f" {st.to_dict()['excluded_by_set']}, thiếu chunk {st.n_no_chunk}) · đã khai thác"
        f" {len(items) - len(todo)} · còn {len(todo)} · params {phash[:12]}"
    )
    vcache = VectorCache(paths.vectors(spec.embed_key))
    rr_dir = paths.root / "rerank" / spec.reranker_key
    if args.dry_run:
        return dry_run(root, spec, rcfg, todo, vcache, RerankCache(rr_dir), catalog)

    t0 = time.perf_counter()
    gpu_info: dict = {}
    # 1) vector câu hỏi (model gốc) — cache M10.
    qtexts = list(dict.fromkeys(it.question for it in todo))
    miss = [q for q in qtexts if cache_key(spec.embed_key, espec, "query", q) not in vcache]
    if miss:
        if not args.gpu:
            print(f"{len(miss)} câu hỏi chưa có vector — chạy với --gpu", file=sys.stderr)
            return 2
        from trafficlaw.retrieval.st_embedder import STEmbedder

        emb = STEmbedder(espec)
        _, est = encode_cached(emb, vcache, spec.embed_key, espec, "query", miss)
        gpu_info["encode"] = {**est.to_dict(), "peak_vram_gb": emb.peak_vram_gb()}
        print(f"encode {len(miss)} câu hỏi: {est.to_dict()}")
        del emb
    faiss = FaissIndex.load(paths.faiss(spec.embed_key))
    bm25 = BM25Index.load(paths.bm25)
    reranker = None
    if args.gpu:
        from trafficlaw.retrieval.rerank import STReranker

        reranker = STReranker(rspec)
    cache = RerankCache(rr_dir)

    def score(question: str, chunks):
        sc, _ = rerank_scores(reranker, cache, spec.reranker_key, rspec, question, chunks)
        return sc

    n = 0
    try:
        with JsonlWriter(out) as w:
            for i in range(0, len(todo), 256):
                part = todo[i : i + 256]
                qv = [
                    vcache.get(cache_key(spec.embed_key, espec, "query", it.question))
                    for it in part
                ]
                import numpy as np

                dense = faiss.search(
                    np.stack(qv), spec.dense_k, allowed=[catalog.ids_at(it.as_of) for it in part]
                )
                for it, dh in zip(part, dense, strict=True):
                    bh = bm25.search(it.question, spec.bm25_k, allowed=catalog.ids_at(it.as_of))
                    assert it.chunk_id is not None
                    rec = mine_one(
                        qid=it.qid, question=it.question, as_of=it.as_of, pos_id=it.chunk_id,
                        gold_units=it.gold_units, catalog=catalog,
                        dense_ids=[h.chunk_id for h in dh], bm25_ids=[h.chunk_id for h in bh],
                        spec=spec, score=score, phash=phash,
                    )  # fmt: skip
                    w.write(rec)
                    n += 1
                logger.info("khai thác %d/%d câu", n, len(todo))
    except MissingRerankScoresError as e:
        print(f"{e}", file=sys.stderr)
        return 2
    except MissingVectorsError as e:
        print(f"{e}", file=sys.stderr)
        return 2
    secs = time.perf_counter() - t0
    rows = [r for r in read_jsonl(out) if r.get("params_hash") == phash]
    stats = mining_stats(rows)
    summary = {
        "finished_at": now_iso(),
        "git_commit": git_commit(root),
        "params_hash": phash,
        "params": spec.model_dump(exclude={"data"}),
        "filter": st.to_dict(),
        "test_sha256": test_sha,
        "n_new": n,
        "seconds": round(secs, 1),
        "gpu": bool(args.gpu),
        **({"cost": gpu_cost(secs, _price(root))} if args.gpu else {}),
        "gpu_info": gpu_info,
        "peak_vram_gb_rerank": reranker.peak_vram_gb() if reranker is not None else None,
        "stats": stats,
        "negatives_sha256": file_sha256(out),
    }
    append_jsonl(out.parent / "mine_runs.jsonl", summary)
    (out.parent / "hard_negatives_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps(stats, ensure_ascii=False))
    print(f"→ {out} ({len(rows)} câu, {secs:.0f} s)")
    return 0


def _price(root: Path) -> float:
    from trafficlaw.llm.serve import load_serve_config

    return load_serve_config(root / "configs" / "serve.yaml").remote.price_vnd_per_hour


def dry_run(root, spec, rcfg, todo, vcache, cache, catalog) -> int:
    """Ước tính: câu cần encode, cặp rerank tối đa (positive + ``max_candidates``; trừ cặp
    positive đã có trong cache), giờ GPU, VND."""
    espec, rspec = rcfg.spec(spec.embed_key), rcfg.reranker(spec.reranker_key)
    qs = list(dict.fromkeys(it.question for it in todo))
    miss = [q for q in qs if cache_key(spec.embed_key, espec, "query", q) not in vcache]
    pos_cached = sum(
        1
        for it in todo
        if cache.get(pair_key(spec.reranker_key, rspec, it.question, catalog.get(it.chunk_id).text))
    )
    pairs = len(todo) * (1 + spec.max_candidates) - pos_cached
    q_tok = sum(len(q) / 1.74 for q in miss)
    h_enc = (q_tok / espec.encode_tps + (espec.load_min * 60 if miss else 0)) / 3600
    h_rr = (pairs / rspec.pairs_per_s + rspec.load_min * 60) / 3600 if pairs else 0.0
    price = _price(root)
    tot = h_enc + h_rr
    print(
        f"encode {len(miss)} câu hỏi (~{q_tok:,.0f} token, {espec.hf_repo}@{espec.revision[:7]})"
        f" ≈ {h_enc * 60:.1f} phút"
    )
    print(
        f"rerank ≤ {pairs:,} cặp (≤ {spec.max_candidates} ứng viên + positive/câu,"
        f" {rspec.pairs_per_s:.0f} cặp/s ước tính thận trọng; M11 đo ~174 cửa sổ/s)"
        f" ≈ {h_rr * 60:.1f} phút"
    )
    print(f"Tổng ≈ {tot:.2f} giờ GPU ≈ {round(tot * price):,} VND (chưa gồm setup)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
