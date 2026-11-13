"""M10: chỉ mục truy hồi (danh mục chunk, BM25, FAISS) + đánh giá chọn model embedding.

    uv run python -m scripts.build_index [--force] [--model K]   # chunk + BM25 + FAISS + manifest
    uv run --group tok python -m scripts.build_index --encode --dry-run [--all|--model K]
    uv run --group embed python -m scripts.build_index --encode [--all|--model K]   # máy GPU thuê
    uv run python -m scripts.build_index --evaluate                   # data/index/model_selection.*
    uv run python -m scripts.build_index --baseline                   # regression BM25 (CI)

Không cần GPU: mọi lệnh trừ ``--encode`` (không ``--dry-run``). ``--encode`` đọc
``data/index/chunks.jsonl`` có sẵn (đẩy lên máy thuê bằng ``gpu.sh push data/index``), ghi cache
vector ``data/index/vectors/<model>/`` (resume được) — kéo về bằng
``gpu.sh pull data/index/vectors``.
**Không dùng ``data/qa/test.jsonl``** (mục 10): tập đo = val + tập con train.
Mã thoát: 1 = lỗi; 2 = thiếu vector (cần ``--encode``).
"""

from __future__ import annotations

import argparse
import gzip
import json
import logging
import sys
import time
from collections.abc import Collection, Sequence
from pathlib import Path
from typing import Any

import yaml

from trafficlaw.eval.qa_schema import QAItem
from trafficlaw.eval.qa_subsets import data_version
from trafficlaw.eval.retrieval_eval import (
    EvalQuery,
    evaluate_system,
    fixed_sample,
    render_selection_md,
    run_retriever,
    stratified_sample,
    to_queries,
)
from trafficlaw.eval.retrieval_metrics import summarize
from trafficlaw.graph.embedded import EmbeddedStore
from trafficlaw.graph.store import data_hash
from trafficlaw.retrieval.bm25 import BM25Index
from trafficlaw.retrieval.catalog import ChunkCatalog, Hit
from trafficlaw.retrieval.config import RetrievalConfig, load_retrieval_config
from trafficlaw.retrieval.dense import FaissIndex
from trafficlaw.retrieval.fusion import rrf
from trafficlaw.retrieval.index_pipeline import (
    IndexPaths,
    MissingVectorsError,
    file_sha256,
    finalize_manifest,
    now_iso,
    query_vectors,
    read_manifest,
    step_bm25,
    step_catalog,
    step_encode,
    step_faiss,
    window_summary,
    windows_for,
)
from trafficlaw.utils.git import git_commit
from trafficlaw.utils.jsonl import read_jsonl
from trafficlaw.utils.logging import setup_logging
from trafficlaw.utils.seed import set_seed

REPO_ROOT = Path(__file__).resolve().parents[1]
logger = logging.getLogger("build_index")


def _yaml(p: Path) -> dict[str, Any]:
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


class Env:
    def __init__(self, root: Path, config: Path) -> None:
        self.root = root
        self.pc = _yaml(root / "configs" / "paths.yaml")
        self.cfg: RetrievalConfig = load_retrieval_config(config)
        self.paths = IndexPaths(root / self.cfg.index_dir)

    @property
    def graph_dir(self) -> Path:
        return self.root / self.pc["graph_dir"]

    def inputs(self) -> dict[str, str]:
        return {
            "data_version": data_version(
                [self.root / self.pc[k] for k in ("documents", "unit_versions", "units_added")]
            ),
            "graph_data_hash": data_hash(self.graph_dir),
        }

    def query_sets(self) -> dict[str, list[EvalQuery]]:
        e = self.cfg.eval
        val = to_queries([QAItem.model_validate(r) for r in read_jsonl(self.root / e.val)])
        train = to_queries([QAItem.model_validate(r) for r in read_jsonl(self.root / e.train)])
        sample = stratified_sample(train, e.train_sample, seed=e.seed, name="retrieval_train")
        return {"val": val, f"train_{len(sample)}": sample}

    def catalog(self) -> ChunkCatalog:
        if not self.paths.chunks.is_file():
            raise SystemExit(f"thiếu {self.paths.chunks} — chạy build_index (không --encode) trước")
        return ChunkCatalog.load(self.paths.chunks)

    def models(self, args: argparse.Namespace) -> list[str]:
        if args.model:
            return [args.model]
        if args.all or not self.cfg.model_key:
            return list(self.cfg.candidates)
        return [self.cfg.model_key]


# --- build (mặc định) ------------------------------------------------------------------------


def cmd_build(env: Env, args: argparse.Namespace) -> int:
    man = read_manifest(env.paths)
    t0 = time.perf_counter()
    cat, rebuilt = step_catalog(
        lambda: EmbeddedStore.from_dir_base(env.graph_dir),
        env.cfg,
        env.paths,
        env.inputs(),
        man,
        force=args.force,
    )
    print(f"chunks: {len(cat)} ({'dựng lại' if rebuilt else 'còn mới'}) → {env.paths.chunks}")
    print("  theo loại × tier:", json.dumps(man["catalog"]["by_kind_tier"], ensure_ascii=False))
    _, rb = step_bm25(cat, env.cfg, env.paths, man, force=args.force or rebuilt)
    print(f"bm25: {'dựng lại' if rb else 'còn mới'} · {man['bm25']['n_terms']} term")
    code = 0
    for key in env.models(args):
        try:
            idx, rf = step_faiss(key, cat, env.cfg, env.paths, man, force=args.force)
        except MissingVectorsError as e:
            print(f"faiss/{key}: bỏ qua — {e}")
            if args.model:
                code = 2
            continue
        m = man["faiss"][key]
        print(
            f"faiss/{key}: {'dựng lại' if rf else 'còn mới'} · dim {idx.dim} · {m['n_rows']} dòng"
            f" / {m['n_chunks']} chunk · tách cửa sổ {m['n_windowed']} · còn cắt {m['n_truncated']}"
        )
    finalize_manifest(env.paths, man, git_commit=git_commit(env.root))
    print(f"manifest → {env.paths.manifest} ({time.perf_counter() - t0:.1f} s)")
    return code


# --- encode ----------------------------------------------------------------------------------


def _all_queries(env: Env) -> list[str]:
    seen: dict[str, None] = {}
    for qs in env.query_sets().values():
        for q in qs:
            seen.setdefault(q.question, None)
    return list(seen)


def cmd_encode(env: Env, args: argparse.Namespace) -> int:
    cat = env.catalog()
    queries = _all_queries(env)
    keys = env.models(args)
    if args.dry_run:
        return encode_dry_run(env, cat, queries, keys)
    from trafficlaw.retrieval.st_embedder import STEmbedder

    for key in keys:
        spec = env.cfg.spec(key)
        if not spec.revision:
            print(f"{key}: chưa ghim revision — từ chối chạy", file=sys.stderr)
            return 1
        t0 = time.perf_counter()
        emb = STEmbedder(spec)
        load_s = time.perf_counter() - t0
        info = {
            "load_s": round(load_s, 1),
            "device": emb.device,
            "dtype": emb.dtype_name,
            "gpu": emb.torch.cuda.get_device_name(0) if emb.device == "cuda" else None,
            "torch": emb.torch.__version__,
            "git_commit": git_commit(env.root),
        }
        rec = step_encode(emb, key, cat, queries, env.cfg, env.paths, run_info=info)
        rec["peak_vram_gb"] = emb.peak_vram_gb()
        print(
            json.dumps(
                {k: rec[k] for k in ("model_key", "dim", "windows", "total")}, ensure_ascii=False
            )
        )
        print(f"  {key}: VRAM đỉnh {rec['peak_vram_gb']} GB, nạp {load_s:.0f} s")
        # Ghi lại VRAM đỉnh (sau encode) vào dòng runs vừa ghi.
        _patch_last_run(env.paths.runs(key), {"peak_vram_gb": rec["peak_vram_gb"]})
        del emb
        try:
            import torch

            torch.cuda.empty_cache()
            torch.cuda.reset_peak_memory_stats()
        except Exception:  # không có CUDA
            pass
    return 0


def _patch_last_run(path: Path, extra: dict[str, Any]) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    last = json.loads(lines[-1])
    last.update(extra)
    lines[-1] = json.dumps(last, ensure_ascii=False)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def encode_dry_run(env: Env, cat: ChunkCatalog, queries: Sequence[str], keys: Sequence[str]) -> int:
    from trafficlaw.llm.serve import load_serve_config
    from trafficlaw.retrieval.st_embedder import TokenCounter

    price = load_serve_config(env.root / "configs" / "serve.yaml").remote.price_vnd_per_hour
    tot_h = 0.0
    print(f"{len(cat)} chunk · {len(queries)} câu hỏi (val + tập con train) · giá {price} VND/giờ")
    for key in keys:
        spec = env.cfg.spec(key)
        tc = TokenCounter(spec)
        ws = windows_for(cat, env.cfg, key, tc.count_tokens)
        s = window_summary(ws, spec.max_seq_length)
        q_tok = sum(
            min(tc.count_tokens(spec.query_prompt + q), spec.max_seq_length) for q in queries
        )
        toks = s["doc_tokens"] + q_tok
        h = toks / spec.encode_tps / 3600 + spec.load_min / 60
        tot_h += h
        print(
            f"{key}: {s['n_rows']} cửa sổ ({s['n_windowed']} chunk tách,"
            f" {s['n_truncated']} còn cắt,"
            f" tối đa {s['max_windows']}/chunk) · token tài liệu {s['doc_tokens']:,} · câu hỏi"
            f" {q_tok:,} · ~{h * 60:.1f} phút GPU (encode {spec.encode_tps:,.0f} tok/s + nạp"
            f" {spec.load_min} phút) · rev {(spec.revision or 'CHƯA GHIM')[:7]}"
        )
    print(
        f"Tổng ~{tot_h:.2f} giờ GPU ≈ {round(tot_h * price):,} VND (chưa gồm setup/cài torch,"
        " thường 10–20 phút)"
    )
    return 0


# --- evaluate --------------------------------------------------------------------------------


def bm25_retriever(idx: BM25Index, depth: int):
    def run(qs: Sequence[EvalQuery], allowed: Sequence[Collection[str] | None]) -> list[list[Hit]]:
        return [idx.search(q.question, depth, allowed=a) for q, a in zip(qs, allowed, strict=True)]

    return run


def dense_retriever(env: Env, key: str, idx: FaissIndex, depth: int):
    memo: dict[tuple[str, ...], Any] = {}  # vector câu hỏi theo tập (đọc cache một lần)

    def run(qs: Sequence[EvalQuery], allowed: Sequence[Collection[str] | None]) -> list[list[Hit]]:
        texts = tuple(q.question for q in qs)
        if texts not in memo:
            memo[texts] = query_vectors(env.paths, key, env.cfg, list(texts))
        return idx.search(memo[texts], depth, allowed=list(allowed))

    return run


def hybrid_retriever(a, b, *, k: int, depth: int, top_k: int):
    def run(qs: Sequence[EvalQuery], allowed: Sequence[Collection[str] | None]) -> list[list[Hit]]:
        ha, hb = a(qs, allowed), b(qs, allowed)
        return [rrf([x[:depth], y[:depth]], k=k, top_k=top_k) for x, y in zip(ha, hb, strict=True)]

    return run


def model_info(env: Env, key: str, man: dict[str, Any]) -> dict[str, Any]:
    spec = env.cfg.spec(key)
    out: dict[str, Any] = {
        "hf_repo": spec.hf_repo,
        "revision": spec.revision,
        "params_b": spec.params_b,
        "license": spec.license,
    }
    f = man.get("faiss", {}).get(key, {})
    out.update({k: f.get(k) for k in ("dim", "n_windowed", "n_truncated")})
    runs = env.paths.runs(key)
    if runs.is_file():
        rs = [r for r in read_jsonl(runs) if r.get("doc", {}).get("n_encoded")]
        if rs:
            last = rs[-1]
            out["tokens_per_s"] = last["doc"].get("tokens_per_s")
            out["peak_vram_gb"] = last.get("peak_vram_gb")
            out["gpu"] = last.get("gpu")
            out["dtype"] = last.get("dtype")
    return out


def cmd_evaluate(env: Env, args: argparse.Namespace) -> int:
    cfg = env.cfg
    man = read_manifest(env.paths)
    cat = env.catalog()
    if man.get("catalog", {}).get("sha256") != file_sha256(env.paths.chunks):
        print("manifest lệch chunks.jsonl — chạy build_index trước", file=sys.stderr)
        return 1
    bm = BM25Index.load(env.paths.bm25)
    depth = max(cfg.top_k, cfg.rrf_depth)
    systems: dict[str, Any] = {"BM25 (B1)": bm25_retriever(bm, depth)}
    info: dict[str, dict[str, Any]] = {}
    for key in env.models(args):
        try:
            fi = FaissIndex.load(env.paths.faiss(key))
        except (FileNotFoundError, ValueError) as e:
            print(f"{key}: chưa có FAISS ({e}) — bỏ qua")
            continue
        d = dense_retriever(env, key, fi, depth)
        systems[f"dense {key}"] = d
        systems[f"RRF(BM25 + {key})"] = hybrid_retriever(
            systems["BM25 (B1)"], d, k=cfg.rrf_k, depth=cfg.rrf_depth, top_k=cfg.top_k
        )
        info[key] = model_info(env, key, man)
    results: dict[str, dict[str, Any]] = {}
    for set_name, qs in env.query_sets().items():
        results[set_name] = {}
        for name, fn in systems.items():
            t0 = time.perf_counter()

            def topk(qq, al, fn=fn):
                return [h[: cfg.top_k] for h in fn(qq, al)]

            try:
                results[set_name][name] = evaluate_system(topk, qs, cat, seed=cfg.eval.seed)
            except MissingVectorsError as e:
                print(f"{name}: {e}")
                continue
            r = results[set_name][name]
            print(
                f"[{set_name}] {name}: R@5 {100 * r['recall@5']:.1f} · MRR@10"
                f" {100 * r['mrr@10']:.1f} · nDCG@10 {100 * r['ndcg@10']:.1f}"
                f" ({time.perf_counter() - t0:.1f} s)"
            )
    header = [
        f"Sinh lúc {now_iso()} · commit `{git_commit(env.root)}` · {len(cat)} chunk"
        f" (`catalog sha256 {man['catalog']['sha256'][:12]}`) · data_version"
        f" `{(man.get('data_version') or '')[:12]}`",
        "",
        "Tập đo: val (chia theo Điều, câu do mistral-small-3.2 sinh từ chính chunk ⇒ thiên lệch"
        " từ vựng, có lợi cho BM25/model bám nguyên văn) và tập con train phân tầng theo tier"
        f" (seed {cfg.eval.seed}). **Không dùng test.** Chunk đúng = chunk hiệu lực tại as_of chứa"
        " gold unit; R@k cấp unit. CI 95% bootstrap 1.000 lần theo câu.",
        f"BM25 k1={cfg.bm25.k1}, b={cfg.bm25.b}, bigram={cfg.bm25.bigrams}; RRF k={cfg.rrf_k},"
        f" độ sâu {cfg.rrf_depth}; top_k {cfg.top_k}. Chunk dài: cửa sổ ≤ 512 token, điểm = max.",
    ]
    out = env.paths.root / "model_selection"
    out.with_suffix(".json").write_text(
        json.dumps(
            {"results": results, "models": info}, ensure_ascii=False, indent=2, default=list
        ),
        encoding="utf-8",
    )
    out.with_suffix(".md").write_text(render_selection_md(results, info, header=header), "utf-8")
    print(f"→ {out}.md")
    return 0


# --- baseline regression ---------------------------------------------------------------------


def write_gz_jsonl(path: Path, rows: Sequence[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows)
    with path.open("wb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", mtime=0) as gz:
        gz.write(data.encode())


def cmd_baseline(env: Env, args: argparse.Namespace) -> int:
    cfg, rg = env.cfg, env.cfg.regression
    cat = env.catalog()
    corpus = env.root / rg.corpus
    write_gz_jsonl(corpus, [c.model_dump(mode="json") for c in cat.chunks])
    val = env.query_sets()["val"]
    qs = fixed_sample(val, rg.n, seed=rg.seed, name="retrieval_regression")
    bm = BM25Index.build([(c.chunk_id, c.text) for c in cat.chunks], **cfg.bm25.model_dump())
    sc = run_retriever(bm25_retriever(bm, rg.k), qs, cat, filtered=True)
    r = summarize(sc)
    base = {
        "metric": f"recall@{rg.k}",
        "value": r[f"recall@{rg.k}"],
        "max_drop": rg.max_drop,
        "system": "bm25 (lọc as_of)",
        "bm25": cfg.bm25.model_dump(),
        "split": "val",
        "qids": [q.qid for q in qs],
        "corpus": rg.corpus,
        "corpus_sha256": file_sha256(corpus),
        "n_chunks": len(cat),
        "data_version": read_manifest(env.paths).get("data_version"),
        "created_at": now_iso(),
        "git_commit": git_commit(env.root),
    }
    (env.root / rg.baseline).write_text(
        json.dumps(base, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    kb = corpus.stat().st_size / 1024
    print(f"baseline Recall@{rg.k} = {100 * base['value']:.1f}% trên {len(qs)} câu val")
    print(f"→ {rg.baseline}, corpus {rg.corpus} ({kb:.0f} KB)")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--config", default="configs/retrieval.yaml")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--model", help="khoá model trong configs/retrieval.yaml")
    ap.add_argument("--all", action="store_true", help="mọi ứng viên (candidates)")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--encode", action="store_true", help="encode chunk + câu hỏi (GPU)")
    g.add_argument("--evaluate", action="store_true")
    g.add_argument("--baseline", action="store_true")
    ap.add_argument("--dry-run", action="store_true", help="với --encode: ước tính token/giờ GPU")
    args = ap.parse_args(argv)
    setup_logging()
    set_seed(42)
    env = Env(REPO_ROOT, REPO_ROOT / args.config)
    if args.model:
        env.cfg.spec(args.model)
    if args.encode:
        return cmd_encode(env, args)
    if args.evaluate:
        return cmd_evaluate(env, args)
    if args.baseline:
        return cmd_baseline(env, args)
    return cmd_build(env, args)


if __name__ == "__main__":
    sys.exit(main())
