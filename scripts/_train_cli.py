"""CLI chung cho ``scripts.train_embedding`` và ``scripts.train_reranker`` (M14).

    --estimate              local (nhóm tok): bước/epoch, token/cặp, ước giờ GPU + VND cho cả lưới
    --dry-run --grid-id G   máy thuê: 20 bước thật trên 1.000 câu, đánh giá 60 câu val, in VRAM đỉnh
                            + thời gian/bước (dự báo thời gian run thật); đẩy checkpoint thử lên HF
    --grid-id G             máy thuê: huấn luyện một mục lưới (resume tự động từ checkpoint cục bộ
                            hoặc HF Hub ``<run>-ckpt``)
    --report                local: bảng chọn checkpoint (val) từ ``logs/train/*.jsonl``
                            → ``data/train/<kind>_selection.{json,md}``

Không dùng test (chỉ đọc ``gold_units`` của test/dev để loại câu train).
Mã thoát: 1 = lỗi; 2 = thiếu dữ liệu (negative, cửa sổ, pool).
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from trafficlaw.retrieval.config import RetrievalConfig, load_retrieval_config
from trafficlaw.train.config import TrainConfig, load_train_config
from trafficlaw.train.evaluate import selection_key
from trafficlaw.train.pipeline import MissingNegativesError, load_train_data
from trafficlaw.train.run_log import now_iso, read_events
from trafficlaw.utils.git import git_commit
from trafficlaw.utils.logging import setup_logging
from trafficlaw.utils.seed import set_seed

REPO_ROOT = Path(__file__).resolve().parents[1]
logger = logging.getLogger("train")


def price(root: Path) -> float:
    from trafficlaw.llm.serve import load_serve_config

    return load_serve_config(root / "configs" / "serve.yaml").remote.price_vnd_per_hour


def main(kind: str, default_config: str, argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--config", default=default_config)
    ap.add_argument("--retrieval-config", default="configs/retrieval.yaml")
    ap.add_argument("--grid-id")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--estimate", action="store_true")
    g.add_argument("--report", action="store_true")
    g.add_argument(
        "--push-best", action="store_true", help="đẩy bù best/ + final lên HF Hub (máy thuê)"
    )
    ap.add_argument("--no-hub", action="store_true", help="không đẩy/kéo HF Hub")
    ap.add_argument("--device", default=None)
    args = ap.parse_args(argv)
    setup_logging()
    set_seed(42)
    cfg = load_train_config(REPO_ROOT / args.config)
    if cfg.kind != kind:
        print(f"{args.config}: kind={cfg.kind}, cần {kind}", file=sys.stderr)
        return 1
    rcfg = load_retrieval_config(REPO_ROOT / args.retrieval_config)
    if args.push_best:
        return push_best(REPO_ROOT, cfg, args.grid_id)
    if args.report:
        return report(REPO_ROOT, cfg, rcfg)
    if args.estimate:
        return estimate(REPO_ROOT, cfg, rcfg)
    if args.grid_id is None and cfg.grid:
        print(f"cần --grid-id (một trong {sorted(cfg.grid)})", file=sys.stderr)
        return 1
    return train(REPO_ROOT, cfg, rcfg, args)


# --- huấn luyện -------------------------------------------------------------------------------


def train(root: Path, cfg: TrainConfig, rcfg: RetrievalConfig, args: argparse.Namespace) -> int:
    import torch

    from trafficlaw.train.checkpoint import HubSync
    from trafficlaw.train.loop import run_loop
    from trafficlaw.train.run_log import RunLog

    t0 = time.perf_counter()
    params = cfg.params(args.grid_id)
    set_seed(params.seed)
    dr = cfg.dry_run if args.dry_run else None
    try:
        data = load_train_data(
            root, cfg.data, params.n_neg,
            n_items=dr.n_items if dr else None, n_val=dr.n_val if dr else None,
        )  # fmt: skip
    except MissingNegativesError as e:
        print(str(e), file=sys.stderr)
        return 2
    device = args.device or ("cuda" if torch.cuda.is_available() else "cpu")
    run_name = cfg.run_name(args.grid_id, dry_run=args.dry_run)
    if cfg.kind == "embedding":
        spec = rcfg.spec(cfg.base_key)
        base = {"hf_repo": spec.hf_repo, "revision": spec.revision}
    else:
        rspec = rcfg.reranker(cfg.base_key)
        base = {"hf_repo": rspec.hf_repo, "revision": rspec.revision}
    if not base["revision"]:
        print(f"{cfg.base_key}: chưa ghim revision — từ chối chạy", file=sys.stderr)
        return 1
    fp = {"kind": cfg.kind, "base": base, "params": params.model_dump(), **data.fingerprint()}
    if cfg.kind == "embedding":
        from trafficlaw.train.embedding import build_embedding_task
        from trafficlaw.train.evaluate import windows_from_rows

        task = build_embedding_task(
            spec=spec, examples=data.examples, params=params, device=device,
            windows=windows_from_rows(data.window_rows), catalog=data.catalog, val=data.val,
            fingerprint=fp,
        )  # fmt: skip
    else:
        from trafficlaw.train.evaluate import load_pools
        from trafficlaw.train.reranker import build_reranker_task

        pool_path = root / cfg.eval_pool
        if not pool_path.is_file():
            print(f"thiếu pool val {pool_path}", file=sys.stderr)
            return 2
        task = build_reranker_task(
            spec=rspec, examples=data.examples, params=params, device=device,
            catalog=data.catalog, val=data.val, pools=load_pools(pool_path), fingerprint=fp,
        )  # fmt: skip
    load_s = time.perf_counter() - t0
    task.info.update(
        {
            "run_name": run_name,
            "grid_id": args.grid_id,
            "dry_run": bool(args.dry_run),
            "git_commit": git_commit(root),
            "torch": torch.__version__,
            "gpu": torch.cuda.get_device_name(0) if device == "cuda" else None,
            "load_s": round(load_s, 1),
            **data.info(),
        }
    )
    hub = HubSync(
        run_name,
        enabled=cfg.hub.enabled and not args.no_hub,
        private=cfg.hub.private,
        push_checkpoints=cfg.hub.push_checkpoints,
    )
    log = RunLog(root / cfg.log_dir / f"{run_name}.jsonl")
    print(
        f"{run_name}: {len(data.examples)} câu train · {len(task.plan)} bước · val"
        f" {len(data.val)} câu · thiết bị {device}"
    )
    summary = run_loop(
        task,
        params,
        run_dir=root / cfg.output_dir / run_name,
        log=log,
        hub=hub,
        device=device,
        max_steps=dr.steps if dr else None,
        push_best=not args.dry_run,
        price_vnd_per_hour=price(root),
    )
    if dr:
        steps = read_events(log.path, "step")
        sec = [e["elapsed_s"] for e in steps]
        per = (sec[-1] - sec[0]) / max(1, steps[-1]["step"] - steps[0]["step"]) if sec else 0.0
        n_full = len(task.plan) if dr is None else _full_steps(root, cfg, params)
        summary["sec_per_step"] = round(per, 3)
        summary["full_run_steps"] = n_full
        summary["full_run_est_h"] = round(per * n_full / 3600, 3)
    print(json.dumps(summary, ensure_ascii=False, default=str))
    return 0


def _full_steps(root: Path, cfg: TrainConfig, params) -> int:
    data = load_train_data(root, cfg.data, params.n_neg, require_negatives=False)
    from trafficlaw.train.data import no_dup_batches

    if cfg.kind == "embedding":
        return sum(
            len(no_dup_batches(data.examples, params.batch_size, seed=params.seed, epoch=ep))
            for ep in range(params.epochs)
        )
    n = sum(1 for e in data.examples if e.neg_texts)
    per = -(-n // (params.batch_size * params.grad_accum))
    return per * params.epochs


# --- ước tính ---------------------------------------------------------------------------------


def estimate(root: Path, cfg: TrainConfig, rcfg: RetrievalConfig) -> int:
    from trafficlaw.train.data import no_dup_batches

    p0 = cfg.train
    try:
        data = load_train_data(root, cfg.data, max(p0.n_neg, 7), require_negatives=False)
    except MissingNegativesError as e:  # pragma: no cover
        print(str(e), file=sys.stderr)
        return 2
    has_neg = any(e.neg_ids for e in data.examples)
    vnd_h = price(root)
    print(
        f"{cfg.kind}: câu train {data.stats.n_total} → giữ {data.stats.n_kept} (loại"
        f" {data.stats.n_excluded}: {data.stats.to_dict()['excluded_by_set']})"
        f" · val {len(data.val)}"
        f" · negative {'có' if has_neg else 'CHƯA khai thác — ước bằng độ dài positive trung bình'}"
    )
    if cfg.kind == "embedding":
        from trafficlaw.retrieval.st_embedder import TokenCounter

        spec = rcfg.spec(cfg.base_key)
        tc = TokenCounter(spec)

        def cnt(t: str) -> int:
            return min(tc.count_tokens(t), spec.max_seq_length)

        q_tok = sum(cnt(spec.query_prompt + e.question) for e in data.examples)
        p_tok = sum(cnt(spec.doc_prompt + e.pos_text) for e in data.examples)
        n_tok = sum(cnt(t) for e in data.examples for t in e.neg_texts[:1])
        avg_p = p_tok / max(1, len(data.examples))
        corpus = sum(min(int(r["n_tokens"]), spec.max_seq_length) for r in data.window_rows)
        val_tok = sum(cnt(q.question) for q in data.val)
        tot = 0.0
        for gid in cfg.grid or {None: {}}:
            p = cfg.params(gid)
            n_neg_tok = n_tok if has_neg else avg_p * len(data.examples)
            per_epoch = q_tok + p_tok + n_neg_tok * p.n_neg
            steps = [
                len(no_dup_batches(data.examples, p.batch_size, seed=p.seed, epoch=ep))
                for ep in range(p.epochs)
            ]
            h_train = p.epochs * per_epoch * cfg.train_factor / spec.encode_tps / 3600
            h_eval = p.epochs * (corpus + val_tok) / spec.encode_tps / 3600
            h = h_train + h_eval + spec.load_min / 60
            tot += h
            print(
                f"  {cfg.run_name(gid)}: {p.epochs} epoch × {steps} bước (batch {p.batch_size},"
                f" mini {p.mini_batch_size}) · token/epoch {per_epoch:,.0f} · train"
                f" {h_train * 60:.1f} phút + đánh giá {h_eval * 60:.1f} phút + nạp ≈ {h:.2f} giờ"
            )
    else:
        from trafficlaw.retrieval.rerank import make_counter

        rspec = rcfg.reranker(cfg.base_key)
        tot = 0.0
        pools = root / cfg.eval_pool
        n_eval_pairs = 0
        if pools.is_file():
            from trafficlaw.train.evaluate import load_pools

            n_eval_pairs = sum(len(v["pool"]) for v in load_pools(pools).values())
        _ = make_counter  # tokenizer chỉ cần khi đếm cửa sổ chính xác (dry-run trên GPU)
        for gid in cfg.grid or {None: {}}:
            p = cfg.params(gid)
            n_groups = sum(1 for e in data.examples if e.neg_ids) if has_neg else len(data.examples)
            pairs = n_groups * (1 + p.n_neg)
            steps = -(-n_groups // (p.batch_size * p.grad_accum)) * p.epochs
            h_train = p.epochs * pairs * cfg.train_factor / rspec.pairs_per_s / 3600
            h_eval = p.epochs * n_eval_pairs / rspec.pairs_per_s / 3600
            h = h_train + h_eval + rspec.load_min / 60
            tot += h
            print(
                f"  {cfg.run_name(gid)}: {p.epochs} epoch, {steps} bước ({n_groups} nhóm ×"
                f" {1 + p.n_neg} cặp = {pairs:,} cặp/epoch) · train {h_train * 60:.1f} phút +"
                f" đánh giá {h_eval * 60:.1f} phút ({n_eval_pairs:,} cặp pool val) ≈ {h:.2f} giờ"
            )
    print(
        f"Tổng lưới ≈ {tot:.2f} giờ GPU ≈ {round(tot * vnd_h):,} VND ({vnd_h:,.0f} VND/giờ;"
        f" ước bằng tốc độ suy luận × {cfg.train_factor} — dry-run 20 bước cho số thật)"
    )
    return 0


# --- báo cáo chọn checkpoint -----------------------------------------------------------------


def _pct(x: Any) -> str:
    return f"{100 * float(x):.1f}" if isinstance(x, (int, float)) else "—"


def _ci(x: Any) -> str:
    return f"{100 * x[0]:.1f}–{100 * x[1]:.1f}" if isinstance(x, (list, tuple)) else "—"


def base_metrics(root: Path, cfg: TrainConfig, rcfg: RetrievalConfig) -> dict[str, Any] | None:
    """Số của model gốc trên cùng tập val, tính ở local từ cache M10/M11 (không GPU)."""
    from trafficlaw.eval.retrieval_eval import run_retriever, to_queries
    from trafficlaw.eval.retrieval_metrics import summarize
    from trafficlaw.retrieval.catalog import ChunkCatalog
    from trafficlaw.train.data import load_items
    from trafficlaw.train.evaluate import CI_METRICS, load_pools, rerank_eval

    catalog = ChunkCatalog.load(root / cfg.data.chunks)
    val = to_queries(load_items(root / cfg.data.val))
    if cfg.kind == "reranker":
        p = root / cfg.eval_pool
        return (
            rerank_eval(None, None, load_pools(p), val, catalog, use_base=True)
            if p.is_file()
            else None
        )
    from trafficlaw.retrieval.dense import FaissIndex
    from trafficlaw.retrieval.index_pipeline import IndexPaths, MissingVectorsError, query_vectors

    paths = IndexPaths(root / rcfg.index_dir)
    try:
        idx = FaissIndex.load(paths.faiss(cfg.base_key))
        qv = query_vectors(paths, cfg.base_key, rcfg, [q.question for q in val])
    except (FileNotFoundError, MissingVectorsError, ValueError):
        return None

    def retr(qs, allowed):
        return idx.search(qv, 20, allowed=list(allowed))

    return summarize(run_retriever(retr, val, catalog, filtered=True), ci_metrics=CI_METRICS)


def push_best(root: Path, cfg: TrainConfig, grid_id: str | None) -> int:
    """Đẩy ``best/`` (repo ``<run>``) và trọng số checkpoint cuối (``<run>-ckpt/final``) của một
    run đã xong — dùng khi lần đẩy cuối run lỗi (vd token thiếu quyền ghi). Ghi sự kiện ``hub``
    vào log của run (``--report`` đọc commit từ đây)."""
    from trafficlaw.train.checkpoint import HubSync, latest_checkpoint
    from trafficlaw.train.run_log import RunLog

    name = cfg.run_name(grid_id)
    run_dir = root / cfg.output_dir / name
    ends = read_events(root / cfg.log_dir / f"{name}.jsonl", "end")
    if not ends or not (run_dir / "best").is_dir():
        print(f"{name}: chưa xong hoặc thiếu {run_dir / 'best'}", file=sys.stderr)
        return 2
    hub = HubSync(name, private=cfg.hub.private)
    log = RunLog(root / cfg.log_dir / f"{name}.jsonl")
    step = ends[-1].get("best_step")
    t0 = time.perf_counter()
    commit = hub.push_model(run_dir / "best", f"best step {step}")
    log.event("hub", what="best", step=step, commit=commit, repo=hub.model_repo,
              seconds=round(time.perf_counter() - t0, 1), late=True)  # fmt: skip
    last = latest_checkpoint(run_dir)
    if last is not None:
        c = hub.push_model(last / "model", f"final step {ends[-1].get('steps')}",
                           repo=hub.ckpt_repo, path_in_repo="final")  # fmt: skip
        log.event("hub", what="final", step=ends[-1].get("steps"), commit=c, late=True)
    hub.close()
    print(f"{name}: best bước {step} → {hub.model_repo}@{commit}")
    return 0


def report(root: Path, cfg: TrainConfig, rcfg: RetrievalConfig) -> int:
    rows: list[dict[str, Any]] = []
    for gid in cfg.grid or {None: {}}:
        name = cfg.run_name(gid)
        log = root / cfg.log_dir / f"{name}.jsonl"
        evs = read_events(log, "eval")
        hub = [e for e in read_events(log, "hub") if e.get("what") == "best"]
        ends = read_events(log, "end")
        starts = read_events(log, "start")
        for e in evs:
            if not e.get("step"):
                continue
            rows.append(
                {
                    "grid_id": gid,
                    "run": name,
                    "step": e["step"],
                    "epoch": e.get("epoch"),
                    "metrics": e["metrics"],
                    "repo": hub[-1].get("repo") if hub else None,
                    "commit": hub[-1].get("commit") if hub else None,
                    "best_step_run": ends[-1].get("best_step") if ends else None,
                    "lr": starts[-1]["params"]["lr"] if starts else None,
                    "end": ends[-1] if ends else None,
                }
            )
    if not rows:
        print("chưa có log đánh giá trong", cfg.log_dir)
        return 2
    order = {g: i for i, g in enumerate(cfg.grid or {None: {}})}
    # Chọn: R@5 → MRR@10 lớn nhất; hoà → bước sớm hơn → mục lưới khai báo trước.
    best = max(
        rows,
        key=lambda r: (*selection_key(r["metrics"]), -r["step"], -order[r["grid_id"]]),
    )
    base = base_metrics(root, cfg, rcfg)
    what = "dense-only" if cfg.kind == "embedding" else "rerank-only trên pool G cố định"
    lines = [
        f"# Chọn checkpoint {cfg.kind} (M14)",
        "",
        f"Sinh lúc {now_iso()} · commit `{git_commit(root)}`. Val ({what}, lọc as_of, cấp unit);"
        " **không dùng test**. Quy tắc chọn (khai báo trước): R@5 → MRR@10 → bước sớm hơn →"
        " mục lưới khai báo trước. CI 95% bootstrap 1.000 lần theo câu.",
        "",
        "| Run | lr | Bước | Epoch | R@1 | R@5 | CI R@5 | R@10 | MRR@10 | CI MRR | nDCG@10 |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    if base:
        lines.append(
            f"| gốc ({cfg.base_key}) | — | 0 | — | {_pct(base['recall@1'])} |"
            f" {_pct(base['recall@5'])} | {_ci(base.get('recall@5_ci'))} |"
            f" {_pct(base['recall@10'])} | {_pct(base['mrr@10'])} | {_ci(base.get('mrr@10_ci'))} |"
            f" {_pct(base['ndcg@10'])} |"
        )
    for r in rows:
        m = r["metrics"]
        mark = " **★**" if r is best else ""
        lines.append(
            f"| {r['run']}{mark} | {r['lr']} | {r['step']} | {r['epoch']} | {_pct(m['recall@1'])} |"
            f" {_pct(m['recall@5'])} | {_ci(m.get('recall@5_ci'))} | {_pct(m['recall@10'])} |"
            f" {_pct(m['mrr@10'])} | {_ci(m.get('mrr@10_ci'))} | {_pct(m['ndcg@10'])} |"
        )
    lines += [
        "",
        "## Run",
        "",
        "| Run | Bước tốt nhất | Repo HF | Commit | VRAM đỉnh (GB) | Giờ GPU | VND |",
        "| --- | ---: | --- | --- | ---: | ---: | ---: |",
    ]
    seen: set[str] = set()
    for r in rows:
        if r["run"] in seen:
            continue
        seen.add(r["run"])
        e = r["end"] or {}
        lines.append(
            f"| {r['run']} | {r['best_step_run']} | {r['repo'] or '—'} |"
            f" `{(r['commit'] or '—')[:12]}`"
            f" | {e.get('peak_vram_gb', '—')} | {e.get('gpu_hours', '—')} | {e.get('vnd', '—')} |"
        )
    lines += [
        "",
        f"**Chọn**: `{best['run']}` bước {best['step']} (R@5 {_pct(best['metrics']['recall@5'])},"
        f" MRR@10 {_pct(best['metrics']['mrr@10'])}). Checkpoint được đẩy lên HF là bản tốt nhất"
        " **của từng run**; nếu bước chọn khác bước tốt nhất của run thì không có trên HF.",
        "",
    ]
    out = root / "data" / "train" / f"{cfg.kind}_selection"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.with_suffix(".json").write_text(
        json.dumps({"rows": rows, "best": best, "base": base}, ensure_ascii=False, indent=2,
                   default=list),
        encoding="utf-8", newline="\n",
    )  # fmt: skip
    out.with_suffix(".md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print("\n".join(lines))
    print(f"→ {out}.md")
    return 0
