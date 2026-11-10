"""M8: công cụ tập vàng trích xuất ``data/qa/gold_extraction.jsonl``.

    uv run python -m scripts.extraction_gold sample        # ~60 Khoản phân tầng, seed 42
    uv run python -m scripts.extraction_gold preannotate [--workers N] [--model M] [--max-calls N]
    uv run python -m scripts.extraction_gold validate      # kiểm tra schema/unit/phiên bản
    uv run python -m scripts.extraction_gold diff          # tỷ lệ người sửa (mục reviewed)
    uv run python -m scripts.extraction_gold review        # sinh lại bản đọc .md

``preannotate`` dùng model tự host KHÁC model trích xuất — khác họ (``family`` trong
configs/serve.yaml), cấu hình ở ``gold.preannotate`` trong configs/extract.yaml; server vLLM phải
đang chạy và tunnel SSH đã mở. Chỉ thêm bản ghi chưa có (không bao giờ ghi đè bản người dùng đã
sửa), resume được; hết quota → dừng sạch (mã 3). Claude không sửa nhãn và không đặt
``reviewed: true``.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from scripts._llm_local import check_local_server, family_of, is_local, resolve_model
from trafficlaw.eval.extraction_gold import (
    DraftOut,
    GoldRecord,
    SampleRow,
    clean_draft,
    render_text,
    sample_gold,
    subtree_versions,
    validate_gold,
)
from trafficlaw.eval.extraction_metrics import edit_stats
from trafficlaw.graph.extract import render_catalog
from trafficlaw.graph.extract_env import ExtractEnv
from trafficlaw.llm import (
    LLMResult,
    QuotaExhaustedError,
    build_client,
    load_llm_config,
    load_prompt,
)
from trafficlaw.llm.parallel import map_parallel
from trafficlaw.utils.dates import parse_iso
from trafficlaw.utils.env import load_dotenv
from trafficlaw.utils.jsonl import JsonlWriter, read_jsonl, write_jsonl
from trafficlaw.utils.logging import setup_logging
from trafficlaw.utils.seed import set_seed

REPO_ROOT = Path(__file__).resolve().parents[1]


def _gold_path(env: ExtractEnv) -> Path:
    return env.p(env.gold.get("path", "data/qa/gold_extraction.jsonl"))


def _sample_path(env: ExtractEnv) -> Path:
    return env.p(env.gold.get("sample_path", "data/qa/gold_extraction_sample.jsonl"))


def cmd_sample(env: ExtractEnv, args: argparse.Namespace) -> int:
    g = env.gold
    as_of = parse_iso(str(g.get("as_of", "2026-11-03")))
    assert as_of is not None
    rows = sample_gold(
        env.store,
        env.cfg,
        g.get("strata") or {},
        as_of=as_of,
        seed=int(g.get("seed", 42)),
        max_units=int(g.get("max_units", 12)),
    )
    path = _sample_path(env)
    old = [SampleRow.model_validate(r) for r in read_jsonl(path)]
    if old and [r.gold_id for r in old] != [r.gold_id for r in rows] and not args.force:
        print(f"sample: {path} đã có và khác mẫu mới — dùng --force để ghi đè", file=sys.stderr)
        return 1
    write_jsonl(path, [r.model_dump(mode="json") for r in rows])
    by = Counter(r.stratum for r in rows)
    n_units = sum(len(env.store.subtree(r.unit_id, as_of=as_of)) for r in rows)
    print(f"sample: {len(rows)} Khoản ({n_units} unit) → {path}")
    for k, v in by.items():
        print(f"  {k:<26} {v}")
    return 0


def cmd_preannotate(env: ExtractEnv, args: argparse.Namespace) -> int:
    catalog = env.catalog()
    if catalog is None or not catalog.approved:
        print("preannotate: danh mục chưa có hoặc chưa duyệt (approved: false)", file=sys.stderr)
        return 1
    rows = [SampleRow.model_validate(r) for r in read_jsonl(_sample_path(env))]
    if not rows:
        print("preannotate: chưa có mẫu — chạy sample trước", file=sys.stderr)
        return 1
    gpath = _gold_path(env)
    have = {str(r.get("gold_id")) for r in read_jsonl(gpath)}
    todo = [r for r in rows if r.gold_id not in have]
    if args.max_calls is not None:
        todo = todo[: args.max_calls]
    pre = env.gold.get("preannotate") or {}
    llm_cfg = load_llm_config(env.llm_config_path)
    provider, model_id = resolve_model(
        llm_cfg, args.provider or pre.get("provider"), args.model or pre.get("model_id")
    )
    if not model_id:
        print(f"preannotate: chưa có model cho provider '{provider}'", file=sys.stderr)
        return 1
    # Bản nháp phải do model KHÁC model trích xuất gán (khác họ khi tự host).
    ext = env.cfg.llm
    _, ext_model = resolve_model(llm_cfg, ext.provider, ext.model_id)
    if ext_model and (
        model_id == ext_model
        or (family_of(model_id) is not None and family_of(model_id) == family_of(ext_model))
    ):
        print(
            f"preannotate: model gán nháp '{model_id}' trùng model/họ với model trích xuất "
            f"'{ext_model}' — chọn model khác họ (configs/serve.yaml: family)",
            file=sys.stderr,
        )
        return 1
    prompt = load_prompt(pre.get("prompt", "gold_preannotate"))
    pt, ct = render_catalog(catalog)
    print(f"preannotate: {len(todo)} bản ghi cần gán (đã có {len(have)}), {provider}:{model_id}")
    if args.dry_run or not todo:
        return 0
    load_dotenv(env.root / ".env")
    if is_local(llm_cfg, provider) and check_local_server(llm_cfg, provider, model_id) is None:
        return 1
    client = build_client(llm_cfg, provider, model_id=model_id, root=env.root)
    st = env.store
    params = {"max_output_tokens": int(pre.get("max_output_tokens", 8192))}

    def context(row: SampleRow) -> tuple[list[Any], str, str]:
        pairs = subtree_versions(st, row.unit_id, row.as_of)
        dieu = st.get_node("/".join(row.unit_id.split("/")[:2]))
        return pairs, render_text(pairs), str((dieu.props.get("title") if dieu else "") or "")

    ctx = {row.gold_id: context(row) for row in todo}

    def call(row: SampleRow) -> LLMResult:
        _, text, dieu_title = ctx[row.gold_id]
        content = prompt.render(catalog_pt=pt, catalog_ct=ct, dieu_title=dieu_title, text=text)
        return client.generate(
            [{"role": "user", "content": content}], json_schema=DraftOut, params=params
        )

    n_ok = 0
    n_done = 0
    with JsonlWriter(gpath) as w:
        for row, r in map_parallel(todo, call, args.workers):
            if isinstance(r, QuotaExhaustedError):
                print(
                    f"preannotate: hết quota ({r}); đã xong {n_done}/{len(todo)}. Chạy lại: "
                    "uv run python -m scripts.extraction_gold preannotate",
                    file=sys.stderr,
                )
                return 3
            n_done += 1
            if r.status == "error":
                print(f"  [{n_done}/{len(todo)}] {row.gold_id}: error {r.error} — chạy lại sau")
                continue
            pairs, text, dieu_title = ctx[row.gold_id]
            texts = {u: str(v.props.get("text") or "") for u, v in pairs}

            def known(u: str, as_of: Any = row.as_of) -> bool:
                return st.version_at(u, as_of) is not None

            draft, dropped = clean_draft(r.parsed or {}, texts, catalog, known)
            rec = GoldRecord(
                gold_id=row.gold_id,
                unit_id=row.unit_id,
                doc_id=row.doc_id,
                tier=row.tier,
                stratum=row.stratum,
                as_of=row.as_of,
                dieu_title=dieu_title,
                units=[{"unit_id": u, "version_id": v.id} for u, v in pairs],  # type: ignore[misc]
                text=text,
                entities=draft.entities,
                relations=draft.relations,
                annotator=f"llm:{r.model_id}",
                reviewed=False,
                draft=draft,
                draft_dropped=dropped,
                draft_status=r.status,
                notes=None,
            )
            w.write(rec.model_dump(mode="json"))
            n_ok += 1
            print(
                f"  [{n_done}/{len(todo)}] {row.gold_id}: {r.status} · {len(draft.entities)} "
                f"thực thể, {len(draft.relations)} quan hệ, bỏ {len(dropped)} · "
                f"{r.latency_ms} ms · {r.usage.total_tokens} tok",
                flush=True,
            )
    print(f"preannotate: ghi {n_ok} bản ghi → {gpath}")
    write_review(env)
    return 0


def write_review(env: ExtractEnv) -> Path:
    """Bản đọc Markdown (sinh lại từ JSONL; sửa nhãn trong JSONL, không sửa file này)."""
    out = env.p(env.gold.get("review_path", "data/qa/gold_extraction_review.md"))
    lines = ["# Tập vàng trích xuất — bản đọc (sinh tự động, sửa trong gold_extraction.jsonl)", ""]
    for r in read_jsonl(_gold_path(env)):
        lines += [
            f"## {r['gold_id']} · {r['stratum']} · tier {r['tier']} · "
            f"{'ĐÃ DUYỆT' if r.get('reviewed') else 'chưa duyệt'}",
            "",
            f"Điều: {r['dieu_title']}",
            "",
            "```",
            r["text"],
            "```",
            "",
            "| id | loại | unit | nội dung |",
            "| --- | --- | --- | --- |",
        ]
        for e in r.get("entities") or []:
            val = {
                k: v for k, v in e.items() if k not in ("id", "type", "unit_id") and v is not None
            }
            lines.append(
                f"| {e['id']} | {e['type']} | {e['unit_id'].split('/', 1)[-1]} | "
                f"{json.dumps(val, ensure_ascii=False).replace('|', '/')} |"
            )
        lines += [""]
        for x in r.get("relations") or []:
            lines.append(f"- {x['type']}: {x['src']} → {x['dst']}")
        if r.get("draft_dropped"):
            lines += ["", f"Bản nháp bị bỏ {len(r['draft_dropped'])} mục:"]
            lines += [
                f"- {d['reason']}: {json.dumps(d['value'], ensure_ascii=False)[:200]}"
                for d in r["draft_dropped"]
            ]
        lines.append("")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes("\n".join(lines).encode("utf-8"))
    return out


def cmd_validate(env: ExtractEnv, args: argparse.Namespace) -> int:
    recs = list(read_jsonl(_gold_path(env)))
    issues = validate_gold(recs, env.store, env.catalog())
    n_rev = sum(1 for r in recs if r.get("reviewed"))
    for i in issues:
        print(f"  {i['level']:<7} {i['gold_id']}: {i['message']}")
    n_err = sum(1 for i in issues if i["level"] == "error")
    print(
        f"validate: {len(recs)} bản ghi ({n_rev} reviewed) · {n_err} lỗi · "
        f"{len(issues) - n_err} cảnh báo"
    )
    return 1 if n_err else 0


def diff_summary(recs: list[dict[str, Any]], span_f1: float) -> dict[str, Any]:
    tot: Counter[str] = Counter()
    per = []
    for r in recs:
        if not r.get("reviewed") or not r.get("draft"):
            continue
        s = edit_stats(r["draft"], r, span_f1)
        per.append({"gold_id": r["gold_id"], **s})
        tot.update(s)
    de = tot["draft_entities"] or 1
    dr = tot["draft_relations"] or 1
    return {
        "n_reviewed_with_draft": len(per),
        "totals": dict(tot),
        "entity_edit_rate": (
            tot["entities_added"] + tot["entities_removed"] + tot["entities_changed"]
        )
        / de,
        "relation_edit_rate": (tot["relations_added"] + tot["relations_removed"]) / dr,
        "per_record": per,
    }


def cmd_diff(env: ExtractEnv, args: argparse.Namespace) -> int:
    recs = list(read_jsonl(_gold_path(env)))
    out = diff_summary(recs, float(env.eval.get("span_f1", 0.5)))
    t = out["totals"]
    print(f"diff: {out['n_reviewed_with_draft']} bản ghi reviewed có bản nháp")
    if out["n_reviewed_with_draft"]:
        print(
            f"  thực thể: nháp {t['draft_entities']} → duyệt {t['final_entities']} · thêm "
            f"{t['entities_added']} · xoá {t['entities_removed']} · đổi {t['entities_changed']} "
            f"· tỷ lệ sửa {out['entity_edit_rate']:.1%}"
        )
        print(
            f"  quan hệ: nháp {t['draft_relations']} → duyệt {t['final_relations']} · thêm "
            f"{t['relations_added']} · xoá {t['relations_removed']} · tỷ lệ sửa "
            f"{out['relation_edit_rate']:.1%}"
        )
    return 0


def cmd_review(env: ExtractEnv, args: argparse.Namespace) -> int:
    print(f"review: {write_review(env)}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("command", choices=["sample", "preannotate", "validate", "diff", "review"])
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--max-calls", type=int, default=None)
    ap.add_argument("--provider", help="preannotate: ghi đè gold.preannotate.provider")
    ap.add_argument("--model", help="preannotate: ghi đè gold.preannotate.model_id")
    ap.add_argument("--workers", type=int, default=1, help="preannotate: số request song song")
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT, help=argparse.SUPPRESS)
    args = ap.parse_args(argv)
    set_seed()
    setup_logging("WARNING")
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")
    env = ExtractEnv(args.repo_root)
    fn = {
        "sample": cmd_sample,
        "preannotate": cmd_preannotate,
        "validate": cmd_validate,
        "diff": cmd_diff,
        "review": cmd_review,
    }[args.command]
    return fn(env, args)


if __name__ == "__main__":
    raise SystemExit(main())
