"""M8: phần ``--extract`` của ``scripts.build_graph`` (tách riêng cho gọn)."""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from scripts._llm_local import check_local_server, is_local, resolve_model, serve_config
from trafficlaw.eval.extraction_gold import SampleRow
from trafficlaw.graph.catalog import CatalogConfig, build_catalog
from trafficlaw.graph.extract import make_batches, select_items
from trafficlaw.graph.extract_env import ExtractEnv
from trafficlaw.graph.extract_pipeline import (
    assemble,
    done_item_keys,
    estimate,
    output_tokens_per_item,
    publish,
    run_key,
    run_llm,
    summarize_estimate,
    write_catalog,
)
from trafficlaw.llm import build_client, load_llm_config, load_prompt
from trafficlaw.llm.serve import gpu_hours
from trafficlaw.utils.env import load_dotenv
from trafficlaw.utils.git import git_commit
from trafficlaw.utils.jsonl import read_jsonl


def _gold_units(env: ExtractEnv) -> set[str] | None:
    path = env.p(env.gold.get("sample_path", "data/qa/gold_extraction_sample.jsonl"))
    rows = [SampleRow.model_validate(r) for r in read_jsonl(path)]
    if not rows:
        return None
    st = env.store
    return {u for r in rows for u in st.subtree(r.unit_id)}


def _resume_cmd(args: argparse.Namespace) -> str:
    cmd = "uv run python -m scripts.build_graph --extract"
    for d in args.doc_id or []:
        cmd += f" --doc-id {d}"
    if args.gold_only:
        cmd += " --gold-only"
    if args.provider:
        cmd += f" --provider {args.provider}"
    if args.model:
        cmd += f" --model {args.model}"
    if args.workers > 1:
        cmd += f" --workers {args.workers}"
    return cmd


def run_extract_cli(args: argparse.Namespace, root: Path) -> int:
    env = ExtractEnv(root)
    paths = env.paths
    if args.catalog:
        cur = env.catalog()
        if cur is not None and cur.approved and not args.force:
            print(
                f"catalog: {paths.catalog} đã duyệt (approved: true) — không ghi đè",
                file=sys.stderr,
            )
            return 1
        if cur is not None and not args.force:
            print(f"catalog: {paths.catalog} đã có — dùng --force để dựng lại", file=sys.stderr)
            return 1
        cat = build_catalog(
            env.store, CatalogConfig.model_validate(env.raw_cfg.get("catalog") or {})
        )
        write_catalog(paths.catalog, cat)
        print(
            f"catalog: {len(cat.phuong_tien)} PhuongTien, {len(cat.chu_the)} ChuThe → "
            f"{paths.catalog} (approved: false — cần người dùng duyệt)"
        )
        return 0
    if args.publish:
        ev = env.eval
        out = publish(
            paths,
            env.p(ev.get("report_path", "data/processed/extraction/eval_report.json")),
            min_entity_f1=float(ev.get("min_entity_f1", 0.85)),
            min_relation_f1=float(ev.get("min_relation_f1", 0.80)),
        )
        print(f"publish: {out.message}", file=sys.stdout if out.ok else sys.stderr)
        return 0 if out.ok else 1

    catalog = env.catalog()
    if catalog is None:
        print(
            f"extract: chưa có danh mục {paths.catalog} — chạy --extract --catalog", file=sys.stderr
        )
        return 1
    cfg = env.cfg
    only = _gold_units(env) if args.gold_only else None
    if args.gold_only and only is None:
        print("extract: chưa có mẫu gold — chạy scripts.extraction_gold sample", file=sys.stderr)
        return 1
    llm_cfg = load_llm_config(env.llm_config_path)
    provider, model_id = resolve_model(
        llm_cfg, args.provider or cfg.llm.provider, args.model or cfg.llm.model_id
    )
    calls_llm = not args.dry_run and args.max_calls != 0
    if model_id is None:
        if calls_llm:
            print(
                f"extract: chưa chốt model cho provider '{provider}' (main.model_id trong "
                "configs/llm.yaml) — dùng --model <served_model_name> khi chạy thử",
                file=sys.stderr,
            )
            return 1
        model_id = "(chua-chot)"
    prompt = load_prompt(cfg.llm.prompt)
    key = run_key(model_id, prompt, catalog)

    if args.dry_run:
        items = select_items(env.store, cfg, args.doc_id)
        if only is not None:
            items = [i for i in items if i.unit_id in only]
        done = done_item_keys(paths.raw, key, retry_format_error=args.retry_format_error)
        batches = make_batches(items, cfg.batch, skip_keys=done)
        opi = output_tokens_per_item(paths.raw)
        est = estimate(batches, items, prompt, catalog, out_per_item=opi)
        print(
            f"dry-run: model {provider}:{model_id} · prompt {prompt.hash[:12]} · schema "
            f"{key.schema_hash[:12]} · đã xong {len(done):,} item · {opi:.0f} token ra/item"
        )
        for line in summarize_estimate(est):
            print("  " + line)
        pc = llm_cfg.providers[provider]
        tot = est["groups"].get("total", {})
        n = tot.get("batches", 0)
        if pc.rpd:
            print(f"  → {n} lượt còn lại; rpd cấu hình {pc.rpd} ⇒ ~{-(-n // pc.rpd)} ngày quota")
        scfg = serve_config(root)
        if is_local(llm_cfg, provider) and scfg is not None:
            h, vnd = gpu_hours(
                scfg, model_id, tot.get("prompt_tokens", 0), tot.get("output_tokens", 0)
            )
            print(
                f"  → GPU tự host: ~{h:.2f} giờ ≈ {vnd:,} VND (chưa gồm khởi động/tải model; "
                f"{scfg.remote.price_vnd_per_hour:,} VND/giờ)"
            )
        return 0

    if not catalog.approved and args.max_calls != 0:
        print(
            f"extract: danh mục {paths.catalog} chưa duyệt (approved: false). Duyệt rồi đặt "
            "approved: true; hoặc chạy --dry-run.",
            file=sys.stderr,
        )
        return 1
    load_dotenv(root / ".env")
    commit = git_commit(root)
    stopped = False
    if args.max_calls != 0:
        meta = None
        if is_local(llm_cfg, provider):
            meta = check_local_server(llm_cfg, provider, model_id, root)
            if meta is None:
                return 1
        client = build_client(llm_cfg, provider, model_id=model_id, root=root)
        t0 = time.monotonic()

        def progress(i: int, n: int, b, r) -> None:  # type: ignore[no-untyped-def]
            print(
                f"  [{i}/{n}] {b.batch_id:<26} {len(b.items):>2} item  {r.status:<12} "
                f"{r.latency_ms:>6} ms  {r.usage.total_tokens:>6} tok"
                f"{'  (cache)' if r.cached else ''}  {time.monotonic() - t0:,.0f}s",
                flush=True,
            )

        out = run_llm(
            env.store,
            cfg,
            catalog,
            client,
            paths,
            doc_ids=args.doc_id,
            only_units=only,
            max_calls=args.max_calls,
            retry_format_error=args.retry_format_error,
            git_commit=commit,
            resume_cmd=_resume_cmd(args),
            progress=progress,
            workers=args.workers,
            run_meta=meta,
        )
        print(
            f"extract: {out.n_items:,} item · {out.n_todo_batches} lô cần chạy · đã gọi "
            f"{out.n_called} · {dict(out.by_status)}"
        )
        if out.stopped:
            stopped = True
            print(out.hint, file=sys.stderr)
    rec = assemble(env.store, cfg, catalog, paths, model_id=model_id, git_commit=commit)
    cov = rec["coverage"].get("total", {"done": 0, "total": 0})
    print(
        f"assemble: {sum(rec['nodes_by_label'].values()):,} nút, "
        f"{sum(rec['edges_by_type'].values()):,} cạnh ứng viên · LLM phủ {cov['done']:,}/"
        f"{cov['total']:,} item → {paths.cand_nodes.parent} · {paths.summary}"
    )
    for p in rec["problems"]:
        print(f"  LỖI: {p}", file=sys.stderr)
    if rec["status"] != "ok":
        return 1
    return 3 if stopped else 0  # 3 = dừng sạch vì hết quota ngày (chạy lại để tiếp tục)
