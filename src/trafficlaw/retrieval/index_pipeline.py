"""Dựng chỉ mục (M10), phần I/O: danh mục chunk, BM25, encode (GPU), FAISS, manifest.

Bố cục ``data/index/`` (gitignored)::

    chunks.jsonl                      danh mục chunk (ChunkRecord)
    bm25/index.json.gz                BM25Index
    vectors/<model_key>/part-*.npz    cache vector (append-only, resume)
    vectors/<model_key>/windows.jsonl cửa sổ của từng chunk (tính bằng tokenizer thật)
    vectors/<model_key>/runs.jsonl    mỗi lần encode: thời gian, token/s, VRAM đỉnh, GPU
    faiss/<model_key>/                index.faiss + ids.json + meta.json
    manifest.json                     hash đầu vào + thông tin từng artifact

**Build lại khi hash đổi**: danh mục khi ``data_version`` / ``data_hash`` đồ thị / cấu hình chunk
đổi; BM25 khi danh mục hoặc tham số đổi; FAISS khi danh mục, cửa sổ hoặc revision model đổi.
``--force`` dựng lại tất cả (cache vector giữ nguyên — khoá theo nội dung).
"""

from __future__ import annotations

import hashlib
import json
import logging
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np

from trafficlaw.graph.store import BaseGraphStore
from trafficlaw.retrieval.bm25 import BM25Index
from trafficlaw.retrieval.catalog import ChunkCatalog, ChunkRecord, build_catalog, write_catalog
from trafficlaw.retrieval.config import RetrievalConfig
from trafficlaw.retrieval.dense import (
    Embedder,
    EncodeStats,
    FaissIndex,
    VectorCache,
    Window,
    cache_key,
    chunk_windows,
    encode_cached,
)
from trafficlaw.utils.jsonl import append_jsonl, read_jsonl, write_jsonl

logger = logging.getLogger(__name__)

MANIFEST_FORMAT = "index-1"


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def file_sha256(p: Path) -> str:
    return sha256_bytes(p.read_bytes()) if p.is_file() else ""


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


@dataclass(frozen=True)
class IndexPaths:
    root: Path

    @property
    def chunks(self) -> Path:
        return self.root / "chunks.jsonl"

    @property
    def bm25(self) -> Path:
        return self.root / "bm25" / "index.json.gz"

    @property
    def manifest(self) -> Path:
        return self.root / "manifest.json"

    def vectors(self, key: str) -> Path:
        return self.root / "vectors" / key

    def windows(self, key: str) -> Path:
        return self.vectors(key) / "windows.jsonl"

    def runs(self, key: str) -> Path:
        return self.vectors(key) / "runs.jsonl"

    def faiss(self, key: str) -> Path:
        return self.root / "faiss" / key


# --- manifest ---------------------------------------------------------------------------------


def read_manifest(paths: IndexPaths) -> dict[str, Any]:
    if not paths.manifest.is_file():
        return {}
    return json.loads(paths.manifest.read_text(encoding="utf-8"))


def write_manifest(paths: IndexPaths, m: dict[str, Any]) -> None:
    paths.root.mkdir(parents=True, exist_ok=True)
    tmp = paths.manifest.with_suffix(".json.tmp")
    tmp.write_text(
        json.dumps(m, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8", newline="\n"
    )
    tmp.replace(paths.manifest)


def catalog_stats(chunks: Sequence[ChunkRecord]) -> dict[str, Any]:
    by: dict[str, dict[str, int]] = {}
    for c in chunks:
        by.setdefault(c.kind, {}).setdefault(c.tier, 0)
        by[c.kind][c.tier] += 1
    return {
        "n_chunks": len(chunks),
        "by_kind_tier": {k: dict(sorted(v.items())) for k, v in sorted(by.items())},
        "n_units": len({c.unit_id for c in chunks}),
        "n_chars": sum(len(c.text) for c in chunks),
    }


# --- danh mục + BM25 -------------------------------------------------------------------------


def step_catalog(
    store_factory: Callable[[], BaseGraphStore],
    cfg: RetrievalConfig,
    paths: IndexPaths,
    inputs: dict[str, str],
    manifest: dict[str, Any],
    *,
    force: bool = False,
) -> tuple[ChunkCatalog, bool]:
    """``inputs`` = {data_version, graph_data_hash}. Trả (danh mục, có dựng lại không)."""
    want = {**inputs, "chunk_cfg_hash": cfg.chunk_cfg_hash()}
    cur = manifest.get("catalog", {})
    fresh = (
        not force
        and paths.chunks.is_file()
        and all(cur.get(k) == v for k, v in want.items())
        and cur.get("sha256") == file_sha256(paths.chunks)
    )
    if fresh:
        logger.info("Danh mục chunk còn mới (%s chunk) — bỏ qua", cur.get("n_chunks"))
        return ChunkCatalog.load(paths.chunks), False
    chunks = build_catalog(store_factory(), phu_luc_max_chars=cfg.phu_luc_max_chars)
    write_catalog(paths.chunks, chunks)
    manifest["catalog"] = {
        **want,
        "sha256": file_sha256(paths.chunks),
        "phu_luc_max_chars": cfg.phu_luc_max_chars,
        **catalog_stats(chunks),
        "built_at": now_iso(),
    }
    logger.info("Danh mục chunk: %d chunk", len(chunks))
    return ChunkCatalog(chunks), True


def step_bm25(
    catalog: ChunkCatalog,
    cfg: RetrievalConfig,
    paths: IndexPaths,
    manifest: dict[str, Any],
    *,
    force: bool = False,
) -> tuple[BM25Index, bool]:
    prm = cfg.bm25.model_dump()
    cat_sha = manifest.get("catalog", {}).get("sha256")
    cur = manifest.get("bm25", {})
    if (
        not force
        and paths.bm25.is_file()
        and cur.get("catalog_sha256") == cat_sha
        and cur.get("params") == prm
        and cur.get("sha256") == file_sha256(paths.bm25)
    ):
        return BM25Index.load(paths.bm25), False
    idx = BM25Index.build(
        [(c.chunk_id, c.text) for c in catalog.chunks],
        k1=prm["k1"],
        b=prm["b"],
        bigrams=prm["bigrams"],
    )
    idx.save(paths.bm25)
    manifest["bm25"] = {
        "params": prm,
        "catalog_sha256": cat_sha,
        "sha256": file_sha256(paths.bm25),
        "n_terms": len(idx.postings),
        "avgdl": round(idx.avgdl, 3),
        "built_at": now_iso(),
    }
    return idx, True


# --- encode (GPU) ----------------------------------------------------------------------------


def windows_for(
    catalog: ChunkCatalog, cfg: RetrievalConfig, key: str, count_tokens: Callable[[str], int]
) -> list[Window]:
    return chunk_windows(
        [(c.chunk_id, c.text) for c in catalog.chunks], cfg.spec(key), count_tokens
    )


def window_rows(ws: Sequence[Window], catalog: ChunkCatalog) -> list[dict[str, Any]]:
    return [
        {
            "chunk_id": w.chunk_id,
            "chunk_sha256": sha256_bytes(catalog.get(w.chunk_id).text.encode()),
            "k": w.k,
            "n_tokens": w.n_tokens,
            "truncated": w.truncated,
            "text_sha256": sha256_bytes(w.text.encode()),
            "text": w.text,
        }
        for w in ws
    ]


def window_summary(ws: Sequence[Window], max_seq_length: int) -> dict[str, Any]:
    by_chunk: dict[str, int] = {}
    for w in ws:
        by_chunk[w.chunk_id] = by_chunk.get(w.chunk_id, 0) + 1
    return {
        "n_rows": len(ws),
        "n_chunks": len(by_chunk),
        "n_windowed": sum(1 for v in by_chunk.values() if v > 1),
        "n_truncated": sum(1 for w in ws if w.truncated),
        "doc_tokens": sum(min(w.n_tokens, max_seq_length) for w in ws),
        "max_windows": max(by_chunk.values(), default=0),
    }


def step_encode(
    embedder: Embedder,
    key: str,
    catalog: ChunkCatalog,
    queries: Sequence[str],
    cfg: RetrievalConfig,
    paths: IndexPaths,
    *,
    run_info: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Encode cửa sổ của mọi chunk + câu hỏi đánh giá vào cache (resume theo khoá nội dung);
    ghi ``windows.jsonl`` và một dòng ``runs.jsonl``."""
    spec = cfg.spec(key)
    ws = windows_for(catalog, cfg, key, embedder.count_tokens)
    write_jsonl(paths.windows(key), window_rows(ws, catalog))
    cache = VectorCache(paths.vectors(key))
    _, sd = encode_cached(
        embedder, cache, key, spec, "doc", [w.text for w in ws], flush_every=cfg.encode_flush_every
    )
    _, sq = encode_cached(
        embedder, cache, key, spec, "query", list(queries), flush_every=cfg.encode_flush_every
    )
    tot = EncodeStats(
        n_texts=sd.n_texts + sq.n_texts,
        n_cached=sd.n_cached + sq.n_cached,
        n_encoded=sd.n_encoded + sq.n_encoded,
        n_tokens=sd.n_tokens + sq.n_tokens,
        seconds=sd.seconds + sq.seconds,
    )
    rec = {
        "model_key": key,
        "hf_repo": spec.hf_repo,
        "revision": spec.revision,
        "max_seq_length": spec.max_seq_length,
        "dim": embedder.dim,
        "catalog_sha256": catalog_sha(catalog),
        "windows": window_summary(ws, spec.max_seq_length),
        "doc": sd.to_dict(),
        "query": sq.to_dict(),
        "total": tot.to_dict(),
        "n_queries": len(set(queries)),
        "finished_at": now_iso(),
        **(run_info or {}),
    }
    append_jsonl(paths.runs(key), rec)
    return rec


def catalog_sha(catalog: ChunkCatalog) -> str:
    h = hashlib.sha256()
    for c in catalog.chunks:
        h.update(c.chunk_id.encode())
        h.update(b"\0")
        h.update(c.text.encode())
        h.update(b"\0")
    return h.hexdigest()


# --- FAISS -----------------------------------------------------------------------------------


class MissingVectorsError(RuntimeError):
    pass


def load_windows(paths: IndexPaths, key: str, catalog: ChunkCatalog) -> list[Window]:
    """Cửa sổ đã encode; kiểm tra khớp danh mục hiện hành (đổi text ⇒ phải encode lại)."""
    p = paths.windows(key)
    if not p.is_file():
        raise MissingVectorsError(f"{key}: chưa encode (thiếu {p}) — chạy build_index --encode")
    rows = list(read_jsonl(p))
    got = {r["chunk_id"] for r in rows}
    if got != set(catalog.by_id):
        raise MissingVectorsError(
            f"{key}: cửa sổ lệch danh mục ({len(got)} vs {len(catalog)} chunk) — encode lại"
        )
    for r in rows:
        if r["chunk_sha256"] != sha256_bytes(catalog.get(r["chunk_id"]).text.encode()):
            raise MissingVectorsError(f"{key}: text chunk {r['chunk_id']} đã đổi — encode lại")
    return [
        Window(r["chunk_id"], int(r["k"]), r["text"], int(r["n_tokens"]), bool(r["truncated"]))
        for r in rows
    ]


def query_vectors(
    paths: IndexPaths, key: str, cfg: RetrievalConfig, queries: Sequence[str]
) -> np.ndarray:
    spec = cfg.spec(key)
    cache = VectorCache(paths.vectors(key))
    keys = [cache_key(key, spec, "query", q) for q in queries]
    miss = [q for q, k in zip(queries, keys, strict=True) if k not in cache]
    if miss:
        raise MissingVectorsError(f"{key}: {len(miss)} câu hỏi chưa có vector — encode lại")
    return np.stack([cache.get(k) for k in keys]).astype(np.float32)


def step_faiss(
    key: str,
    catalog: ChunkCatalog,
    cfg: RetrievalConfig,
    paths: IndexPaths,
    manifest: dict[str, Any],
    *,
    force: bool = False,
) -> tuple[FaissIndex, bool]:
    spec = cfg.spec(key)
    ws = load_windows(paths, key, catalog)
    win_sha = file_sha256(paths.windows(key))
    want = {
        "catalog_sha256": manifest.get("catalog", {}).get("sha256"),
        "windows_sha256": win_sha,
        "hf_repo": spec.hf_repo,
        "revision": spec.revision,
        "max_seq_length": spec.max_seq_length,
        "doc_prompt": spec.doc_prompt,
    }
    cur = manifest.setdefault("faiss", {}).get(key, {})
    d = paths.faiss(key)
    if (
        not force
        and (d / "index.faiss").is_file()
        and all(cur.get(k) == v for k, v in want.items())
    ):
        return FaissIndex.load(d), False
    cache = VectorCache(paths.vectors(key))
    keys = [cache_key(key, spec, "doc", w.text) for w in ws]
    miss = sum(1 for k in keys if k not in cache)
    if miss:
        raise MissingVectorsError(f"{key}: thiếu vector cho {miss}/{len(keys)} cửa sổ — encode")
    vecs = np.stack([cache.get(k) for k in keys])
    idx = FaissIndex.build(vecs, [(w.chunk_id, w.k) for w in ws], f"dense:{key}")
    info = {**want, **window_summary(ws, spec.max_seq_length), "dim": idx.dim}
    idx.save(d, meta=info)
    manifest["faiss"][key] = {**info, "built_at": now_iso()}
    return idx, True


def finalize_manifest(
    paths: IndexPaths, manifest: dict[str, Any], *, git_commit: str | None
) -> dict[str, Any]:
    manifest["format"] = MANIFEST_FORMAT
    manifest["updated_at"] = now_iso()
    manifest["git_commit"] = git_commit
    cat = manifest.get("catalog", {})
    manifest["data_version"] = cat.get("data_version")
    manifest["graph_data_hash"] = cat.get("graph_data_hash")
    manifest["n_chunks"] = cat.get("n_chunks")
    write_manifest(paths, manifest)
    return manifest


__all__ = [
    "IndexPaths",
    "MANIFEST_FORMAT",
    "MissingVectorsError",
    "catalog_sha",
    "catalog_stats",
    "file_sha256",
    "finalize_manifest",
    "load_windows",
    "query_vectors",
    "read_manifest",
    "step_bm25",
    "step_catalog",
    "step_encode",
    "step_faiss",
    "window_rows",
    "window_summary",
    "windows_for",
]
