"""M9: công cụ bộ dữ liệu hỏi–đáp.

    uv run python -m scripts.qa_tool plan-test [--as-of D] [--factor F]     # phiếu viết test
    uv run python -m scripts.qa_tool show <unit_id> [--as-of D]             # tra cứu một unit
    uv run python -m scripts.qa_tool validate [--split test|train|val|all] [--strict]
    uv run python -m scripts.qa_tool generate --dry-run                     # ước tính lượt/giờ GPU
    uv run python -m scripts.qa_tool generate [--max-calls N] [--workers 16] [--model M]
    uv run python -m scripts.qa_tool build                                  # lọc + chia train/val
    uv run python -m scripts.qa_tool subsets [--force]                      # tập con cho M13
    uv run python -m scripts.qa_tool review [--n 50]                        # train_review.md
    uv run python -m scripts.qa_tool summary                                # qa_summary.md

Tập test do người dùng viết tay: công cụ chỉ đọc ``data/qa/test.jsonl`` (không tạo/sửa).
``generate`` cần server vLLM qua tunnel (provider ``local``); các lệnh khác không cần GPU.
Mã thoát: 1 = có lỗi (hoặc cảnh báo khi ``--strict``); 3 = dừng sạch giữa chừng (chạy lại để tiếp).
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
from datetime import date, datetime
from functools import cached_property
from pathlib import Path
from typing import Any

import yaml

from trafficlaw.eval.qa_generate import (
    GenerateConfig,
    build_messages,
    build_splits,
    done_chunk_keys,
    estimate,
    output_tokens_per_chunk,
    render_generate_summary,
    run_generate,
    run_key,
    select_chunks,
    unique_chunks,
    write_build,
)
from trafficlaw.eval.qa_plan import PlanConfig, plan_suggestions, render_worksheet, show_unit
from trafficlaw.eval.qa_schema import QAItem
from trafficlaw.eval.qa_subsets import (
    SubsetSpec,
    build_subsets,
    data_version,
    file_sha256,
    qa_version,
    subsets_status,
)
from trafficlaw.eval.qa_validate import (
    Targets,
    ValidateConfig,
    ValidateResult,
    parse_items,
    validate_items,
)
from trafficlaw.graph.embedded import EmbeddedStore
from trafficlaw.utils.dates import parse_iso
from trafficlaw.utils.git import git_commit
from trafficlaw.utils.jsonl import append_jsonl, read_jsonl, write_jsonl
from trafficlaw.utils.logging import setup_logging
from trafficlaw.utils.seed import set_seed

REPO_ROOT = Path(__file__).resolve().parents[1]


def _yaml(p: Path) -> dict[str, Any]:
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


class QAEnv:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.paths_cfg = _yaml(root / "configs" / "paths.yaml")
        self.cfg = _yaml(root / "configs" / "qa.yaml")

    def p(self, key: str) -> Path:
        return self.root / self.cfg["paths"][key]

    @cached_property
    def store(self) -> EmbeddedStore:
        return EmbeddedStore.from_dir(self.root / self.paths_cfg["graph_dir"])

    @property
    def milestones(self) -> tuple[date, ...]:
        return tuple(_date(x) for x in self.cfg.get("milestones") or [])

    @property
    def targets(self) -> Targets:
        t = self.cfg.get("targets") or {}
        return Targets(
            total=int(t.get("total", 500)),
            tier=dict(t.get("tier") or {}),
            question_type=dict(t.get("question_type") or {}),
            tolerance=float(t.get("tolerance", 0.1)),
        )

    @property
    def validate_cfg(self) -> ValidateConfig:
        return ValidateConfig(
            milestones=self.milestones,
            near_dup=float(self.cfg.get("near_dup", 0.9)),
            targets=self.targets,
        )

    @property
    def gen_cfg(self) -> GenerateConfig:
        return GenerateConfig.model_validate(self.cfg.get("generate") or {})

    @property
    def raw(self) -> Path:
        return self.p("gen_dir") / "raw.jsonl"

    def data_version(self) -> str:
        pc = self.paths_cfg
        return data_version(
            [
                self.root / pc["documents"],
                self.root / pc["unit_versions"],
                self.root / pc["units_added"],
            ]
        )

    def qa_version(self) -> str:
        return qa_version([self.p(k) for k in ("test", "train", "val", "subsets")])

    def test_items(self) -> list[QAItem]:
        items, _ = parse_items(list(read_jsonl(self.p("test"))))
        return items


def _date(v: Any) -> date:
    return v if isinstance(v, date) else parse_iso(str(v))  # type: ignore[return-value]


def _write_json(p: Path, obj: Any) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes((json.dumps(obj, ensure_ascii=False, indent=2, default=str) + "\n").encode())


# --------------------------------------------------------------------------- plan / show


def cmd_plan(env: QAEnv, args: argparse.Namespace) -> int:
    pc = env.cfg.get("plan") or {}
    cfg = PlanConfig(
        as_of=_date(args.as_of or env.cfg.get("as_of_default", "2026-11-03")),
        seed=int(env.cfg.get("seed", 42)),
        factor=float(args.factor if args.factor is not None else pc.get("factor", 1.0)),
        max_text_chars=int(pc.get("max_text_chars", 1200)),
        milestones=env.milestones,
    )
    t0 = time.monotonic()
    sugs, stats = plan_suggestions(env.store, env.targets, cfg)
    text = render_worksheet(sugs, env.store, env.targets, cfg, stats)
    out = env.p("worksheet")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(text.encode("utf-8"))
    by: dict[str, int] = {}
    for s in sugs:
        by[s.qtype] = by.get(s.qtype, 0) + 1
    print(f"plan-test: {len(sugs)} gợi ý → {out} ({time.monotonic() - t0:.1f} s)")
    for k, v in by.items():
        print(f"  {k:<22} {v:>4}  (hạn mức {env.targets.question_type.get(k)})")
    return 0


def cmd_show(env: QAEnv, args: argparse.Namespace) -> int:
    d = _date(args.as_of or env.cfg.get("as_of_default", "2026-11-03"))
    lines = show_unit(env.store, args.unit_id, d)
    print("\n".join(lines))
    return 1 if lines and lines[0].startswith("không có unit") else 0


# --------------------------------------------------------------------------- validate


def run_validate(env: QAEnv, split: str) -> ValidateResult:
    rows = list(read_jsonl(env.p(split)))
    tq = None
    other = None
    if split != "test":
        tq = [t.question for t in env.test_items()]
        o = "val" if split == "train" else "train"
        items, _ = parse_items(list(read_jsonl(env.p(o))))
        other = {"/".join(u.split("/")[:2]) for it in items for u in it.gold_units}
    res = validate_items(
        rows, split, env.store, env.validate_cfg, test_questions=tq, other_split_dieus=other
    )  # type: ignore[arg-type]
    if split != "test" and env.p("manifest").is_file():
        m = json.loads(env.p("manifest").read_text(encoding="utf-8"))
        if m.get("test_sha256") != file_sha256(env.p("test")):
            from trafficlaw.eval.qa_validate import Issue

            res.issues.append(
                Issue(
                    "warning",
                    "train_loi_thoi",
                    None,
                    "train/val dựng với test.jsonl cũ — chạy `qa_tool build` để lọc rò rỉ lại",
                )
            )
    vd = env.p("validate_dir")
    write_jsonl(vd / f"{split}_resolved.jsonl", res.resolved)
    _write_json(
        vd / f"validate_{split}.json",
        {
            "split": split,
            "validated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "file_sha256": file_sha256(env.p(split)),
            "data_version": env.data_version(),
            "n_lines": res.n_lines,
            "n_items": len(res.items),
            "n_errors": res.n_errors,
            "n_warnings": res.n_warnings,
            "issues_by_code": _count_codes(res),
            "distribution": res.distribution,
            "issues": [i.to_dict() for i in res.issues],
        },
    )
    return res


def _count_codes(res: ValidateResult) -> dict[str, int]:
    out: dict[str, int] = {}
    for i in res.issues:
        k = f"{i.level}:{i.code}"
        out[k] = out.get(k, 0) + 1
    return dict(sorted(out.items()))


def cmd_validate(env: QAEnv, args: argparse.Namespace) -> int:
    splits = ["test", "train", "val"] if args.split == "all" else [args.split]
    rc = 0
    for s in splits:
        res = run_validate(env, s)
        print(
            f"validate {s}: {res.n_lines} dòng, {len(res.items)} hợp schema · "
            f"{res.n_errors} lỗi · {res.n_warnings} cảnh báo"
        )
        shown = 0
        for i in res.issues:
            if i.level == "info" or (i.level == "warning" and not args.verbose and shown >= 40):
                continue
            if shown >= args.max_show:
                print(f"  … (xem {env.p('validate_dir')}/validate_{s}.json)")
                break
            print(f"  {i.level.upper():<7} {i.code:<26} {i.qid or '-':<14} {i.message}")
            shown += 1
        if s == "test":
            dist = res.distribution
            tgt = dist.get("targets") or {}
            print(f"  tiến độ: {dist['n']}/{tgt.get('total')} câu")
            for k, want in (tgt.get("question_type") or {}).items():
                print(f"    {k:<22} {dist['question_type'].get(k, 0):>4} / {want}")
            for k, want in (tgt.get("tier") or {}).items():
                print(f"    tier {k:<17} {dist['tier'].get(k, 0):>4} / {want:.0f}")
        if res.n_errors or (args.strict and res.n_warnings):
            rc = 1
    write_summary(env)
    return rc


# --------------------------------------------------------------------------- generate / build


def _model(env: QAEnv, args: argparse.Namespace) -> tuple[Any, str, str | None]:
    from scripts._llm_local import resolve_model
    from trafficlaw.llm import load_llm_config

    llm_cfg = load_llm_config(env.root / env.paths_cfg.get("llm_config", "configs/llm.yaml"))
    g = env.gen_cfg
    provider, model_id = resolve_model(
        llm_cfg, args.provider or g.provider, args.model or g.model_id
    )
    return llm_cfg, provider, model_id


def _family_guard(env: QAEnv, llm_cfg: Any, model_id: str) -> str | None:
    """Model sinh câu hỏi phải khác họ với model trả lời chính (giảm thiên lệch M12/M13)."""
    from scripts._llm_local import family_of

    main = llm_cfg.main.model_id
    if main and model_id == main:
        return f"model sinh '{model_id}' trùng model trả lời chính"
    fa, fb = family_of(model_id, env.root), family_of(main, env.root)
    if fa and fb and fa == fb:
        return f"model sinh '{model_id}' cùng họ '{fa}' với model trả lời chính '{main}'"
    return None


def cmd_generate(env: QAEnv, args: argparse.Namespace) -> int:
    from scripts._llm_local import check_local_server, is_local, serve_config
    from trafficlaw.llm import build_client, load_prompt
    from trafficlaw.llm.serve import gpu_hours
    from trafficlaw.utils.env import load_dotenv

    cfg = env.gen_cfg
    llm_cfg, provider, model_id = _model(env, args)
    if model_id is None:
        print("generate: chưa có model (generate.model_id trong configs/qa.yaml)", file=sys.stderr)
        return 1
    guard = _family_guard(env, llm_cfg, model_id)
    if guard and not args.dry_run:
        print(f"generate: {guard} — chọn model khác họ", file=sys.stderr)
        return 1
    prompt = load_prompt(cfg.prompt)
    key = run_key(model_id, prompt, cfg)
    chunks = select_chunks(env.store, args.doc_id)
    uniq = unique_chunks(chunks)
    done = done_chunk_keys(env.raw, key, retry_format_error=args.retry_format_error)
    todo = [c for c in uniq if c.key not in done]

    if args.dry_run:
        opc = output_tokens_per_chunk(env.raw)
        est = estimate(todo, prompt, cfg, out_per_chunk=opc)
        print(
            f"dry-run: model {provider}:{model_id} · prompt {prompt.hash[:12]} · schema "
            f"{key.schema_hash[:12]} · {len(chunks):,} chunk ({len(uniq):,} text khác nhau) · "
            f"đã xong {len(done):,} · {cfg.n_questions} câu/chunk · {opc:.0f} token ra/chunk"
        )
        if guard:
            print(f"  CẢNH BÁO: {guard}")
        for k, v in est.items():
            print(
                f"  {k:<16} {v['calls']:>6} lượt  ~{v['prompt_tokens']:>10,} token vào  "
                f"~{v['output_tokens']:>9,} token ra"
            )
        tot = est.get("total", {"prompt_tokens": 0, "output_tokens": 0, "calls": 0})
        scfg = serve_config(env.root)
        if scfg is not None and is_local(llm_cfg, provider):
            h, vnd = gpu_hours(scfg, model_id, tot["prompt_tokens"], tot["output_tokens"])
            print(
                f"  → GPU tự host: ~{h:.2f} giờ ≈ {vnd:,} VND (chưa gồm cài đặt/tải model; "
                f"{scfg.remote.price_vnd_per_hour:,} VND/giờ)"
            )
        if todo:
            sample = build_messages(prompt, todo[0], cfg)[0]["content"]
            print(f"  prompt mẫu ({todo[0].chunk.chunk_id}, {len(sample)} ký tự):")
            print("    " + sample[-400:].replace("\n", "\n    "))
        return 0

    load_dotenv(env.root / ".env")
    meta = None
    if args.max_calls != 0 and todo:
        if is_local(llm_cfg, provider):
            meta = check_local_server(llm_cfg, provider, model_id, env.root)
            if meta is None:
                return 1
        client = build_client(llm_cfg, provider, model_id=model_id, root=env.root)
        t0 = time.monotonic()
        started = datetime.now().astimezone().isoformat(timespec="seconds")

        def progress(i: int, n: int, gc: Any, r: Any) -> None:
            if i % 50 == 0 or i == n or r.status != "ok":
                print(
                    f"  [{i}/{n}] {gc.chunk.chunk_id:<40} {r.status:<12} {r.latency_ms:>6} ms "
                    f"{r.usage.total_tokens:>5} tok  {time.monotonic() - t0:,.0f}s",
                    flush=True,
                )

        out = run_generate(
            chunks,
            cfg,
            client,
            env.raw,
            max_calls=args.max_calls,
            retry_format_error=args.retry_format_error,
            workers=args.workers,
            git_commit=git_commit(env.root),
            run_meta=meta,
            progress=progress,
        )
        append_jsonl(
            env.p("gen_dir") / "runs.jsonl",
            {
                "started_at": started,
                "seconds": round(time.monotonic() - t0, 1),
                "model_id": model_id,
                "prompt_hash": key.prompt_hash,
                "schema_hash": key.schema_hash,
                "workers": args.workers,
                "n_todo": out.n_todo,
                "n_called": out.n_called,
                "by_status": dict(out.by_status),
                "serve": meta,
                "git_commit": git_commit(env.root),
            },
        )
        print(
            f"generate: {out.n_unique:,} chunk khác nhau · {out.n_todo:,} cần chạy · đã gọi "
            f"{out.n_called:,} · {dict(out.by_status)} · {time.monotonic() - t0:,.0f} s"
        )
        if out.stopped:
            print(out.hint, file=sys.stderr)
            return 3
    if args.no_build:
        return 0
    return cmd_build(env, args, model_id=model_id)


def cmd_build(env: QAEnv, args: argparse.Namespace, *, model_id: str | None = None) -> int:
    from trafficlaw.llm import load_prompt

    cfg = env.gen_cfg
    if model_id is None:
        _, _, model_id = _model(env, args)
    assert model_id is not None
    key = run_key(model_id, load_prompt(cfg.prompt), cfg)
    chunks = select_chunks(env.store)
    test = env.test_items()
    res = build_splits(env.store, chunks, env.raw, key, cfg, test_items=test)
    runs = [r for r in read_jsonl(env.p("gen_dir") / "runs.jsonl") if r.get("model_id") == model_id]
    meta = {
        "git_commit": git_commit(env.root),
        "model_id": model_id,
        "prompt_hash": key.prompt_hash,
        "schema_hash": key.schema_hash,
        "test_sha256": file_sha256(env.p("test")),
        "n_test": len(test),
        "data_version": env.data_version(),
        "config": cfg.model_dump(mode="json"),
        "runs": runs,
    }
    m = write_build(
        res,
        env.p("train"),
        env.p("val"),
        env.p("gen_dir") / "rejected.jsonl",
        env.p("manifest"),
        meta,
    )
    env.p("generate_summary").write_bytes(render_generate_summary(m).encode("utf-8"))
    print(
        f"build: train {m['n_train']:,} · val {m['n_val']:,} · bị loại "
        f"{sum(m['rejected_by_reason'].values()):,} {m['rejected_by_reason']} · chunk đã sinh "
        f"{m['n_chunks_done']:,}/{m['n_chunks_unique']:,} → {env.p('generate_summary')}"
    )
    write_summary(env)
    return 0


# --------------------------------------------------------------------------- subsets / review


def cmd_subsets(env: QAEnv, args: argparse.Namespace) -> int:
    path = env.p("subsets")
    st = subsets_status(path, env.p("test"))
    if st == "ok" and not args.force:
        print(f"subsets: {path} khớp test.jsonl hiện hành — bỏ qua (--force để dựng lại)")
        return 0
    res = run_validate(env, "test")
    bad = res.bad_qids()
    items = [it for it in res.items if it.qid not in bad]
    specs = {
        k: SubsetSpec(int(v["n"]), tuple(v.get("exclude_types") or ()))
        for k, v in (env.cfg.get("subsets") or {}).items()
    }
    out = build_subsets(items, file_sha256(env.p("test")), specs, int(env.cfg.get("seed", 42)))
    out["n_excluded_errors"] = len(res.items) - len(items)
    _write_json(path, out)
    print(f"subsets: {len(items)} câu hợp lệ (bỏ {len(res.items) - len(items)} câu lỗi) → {path}")
    for k, v in out["subsets"].items():
        print(f"  {k:<16} {v['n']:>4} / {v['n_target']}")
    write_summary(env)
    return 0


def cmd_review(env: QAEnv, args: argparse.Namespace) -> int:
    items = [QAItem.model_validate(r) for r in read_jsonl(env.p("train"))]
    if not items:
        print("review: train.jsonl rỗng — chạy generate/build trước", file=sys.stderr)
        return 1
    seed = int(env.cfg.get("seed", 42))
    n = args.n or int((env.cfg.get("review") or {}).get("n", 50))
    pick = sorted(random.Random(seed).sample(items, min(n, len(items))), key=lambda x: x.qid)
    chunks = {c.chunk.chunk_id: c for c in select_chunks(env.store)}
    lines = [
        "# Rà tay câu hỏi train (M9)",
        "",
        f"{len(pick)} câu ngẫu nhiên (seed {seed}) trong {len(items):,} câu train · "
        f"`{env.p('train').name}` sha256 `{file_sha256(env.p('train'))[:12]}`.",
        "",
        "Tiêu chí: **Đ** = chunk trả lời được câu hỏi (positive đúng); **T** = câu tự nhiên, "
        "tự đứng được, không chép nguyên văn; **L** = loại câu đúng. Ghi ✓/✗ và nhận xét.",
        "",
    ]
    for i, it in enumerate(pick, 1):
        gc = chunks.get(it.chunk_id or "")
        text = gc.chunk.text if gc else "(không tìm thấy chunk)"
        if len(text) > 900:
            text = text[:900].rsplit(" ", 1)[0] + " …"
        lines += [
            f"## {i}. `{it.qid}` · {it.question_type} · tier {it.tier} · `{it.chunk_id}`",
            "",
            f"**Câu hỏi:** {it.question}",
            "",
            *[f"> {ln}" for ln in text.split("\n")],
            "",
            "- Đ: · T: · L: · Nhận xét:",
            "",
        ]
    env.p("review").write_bytes("\n".join(lines).encode("utf-8"))
    print(f"review: {len(pick)} câu → {env.p('review')}")
    return 0


# --------------------------------------------------------------------------- summary


def write_summary(env: QAEnv) -> None:
    vd = env.p("validate_dir")
    lines = [
        "# Bộ dữ liệu hỏi–đáp (M9)",
        "",
        f"- Cập nhật: {datetime.now().astimezone().isoformat(timespec='seconds')} · commit "
        f"`{git_commit(env.root)}`",
        f"- `qa_version` = `{env.qa_version()[:16]}` (hash test/train/val/subsets) · "
        f"`data_version` = `{env.data_version()[:16]}`",
        f"- subsets: **{subsets_status(env.p('subsets'), env.p('test'))}**",
        "",
        "| Split | Dòng | sha256 | Kiểm tra lần cuối | Lỗi | Cảnh báo |",
        "| --- | ---: | --- | --- | ---: | ---: |",
    ]
    for s in ("test", "train", "val"):
        p = env.p(s)
        n = sum(1 for _ in read_jsonl(p)) if p.is_file() else 0
        rep = vd / f"validate_{s}.json"
        r = json.loads(rep.read_text(encoding="utf-8")) if rep.is_file() else {}
        fresh = r.get("file_sha256") == file_sha256(p)
        when = (r.get("validated_at", "—") + ("" if fresh else " (lỗi thời)")) if r else "—"
        lines.append(
            f"| {s} | {n:,} | `{file_sha256(p)[:12]}` | {when} | {r.get('n_errors', '—')} | "
            f"{r.get('n_warnings', '—')} |"
        )
    rep = vd / "validate_test.json"
    if rep.is_file():
        r = json.loads(rep.read_text(encoding="utf-8"))
        d = r.get("distribution") or {}
        t = d.get("targets") or {}
        lines += ["", "## Phân bổ test so với hạn mức", "", "| Loại | Có | Hạn mức |"]
        lines += ["| --- | ---: | ---: |"]
        for k, v in (t.get("question_type") or {}).items():
            lines.append(f"| {k} | {d.get('question_type', {}).get(k, 0)} | {v} |")
        lines += ["", "| Tier | Có | Hạn mức |", "| --- | ---: | ---: |"]
        for k, v in (t.get("tier") or {}).items():
            lines.append(f"| {k} | {d.get('tier', {}).get(k, 0)} | {v:.0f} |")
        lines += ["", "Tier × loại: " + json.dumps(d.get("tier_x_type") or {}, ensure_ascii=False)]
    if env.p("manifest").is_file():
        m = json.loads(env.p("manifest").read_text(encoding="utf-8"))
        stale = m.get("test_sha256") != file_sha256(env.p("test"))
        lines += [
            "",
            "## train/val",
            "",
            f"- Dựng {m.get('built_at')} bằng `{m.get('model_id')}`: train {m.get('n_train'):,}, "
            f"val {m.get('n_val'):,}; lọc rò rỉ theo test `{str(m.get('test_sha256'))[:12]}`"
            + (" — **test đã đổi, chạy `qa_tool build`**" if stale else ""),
            f"- Xem `{env.cfg['paths']['generate_summary']}`.",
        ]
    env.p("summary").parent.mkdir(parents=True, exist_ok=True)
    env.p("summary").write_bytes(("\n".join(lines) + "\n").encode("utf-8"))


def cmd_summary(env: QAEnv, args: argparse.Namespace) -> int:
    write_summary(env)
    print(f"summary: {env.p('summary')}")
    return 0


# --------------------------------------------------------------------------- main


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT, help=argparse.SUPPRESS)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan-test", help="phiếu viết tập test")
    p.add_argument("--as-of")
    p.add_argument("--factor", type=float)
    p = sub.add_parser("show", help="tra cứu một unit")
    p.add_argument("unit_id")
    p.add_argument("--as-of")
    p = sub.add_parser("validate", help="kiểm tra test/train/val")
    p.add_argument("--split", default="test", choices=["test", "train", "val", "all"])
    p.add_argument("--strict", action="store_true", help="cảnh báo cũng làm thoát mã 1")
    p.add_argument("--verbose", action="store_true")
    p.add_argument("--max-show", type=int, default=80)
    for name in ("generate", "build"):
        p = sub.add_parser(
            name, help="sinh câu hỏi train/val" if name == "generate" else "lọc + chia"
        )
        p.add_argument("--provider")
        p.add_argument("--model")
        if name == "generate":
            p.add_argument("--dry-run", action="store_true")
            p.add_argument("--doc-id", action="append")
            p.add_argument("--max-calls", type=int)
            p.add_argument("--workers", type=int, default=1)
            p.add_argument("--retry-format-error", action="store_true")
            p.add_argument("--no-build", action="store_true")
    p = sub.add_parser("subsets", help="tập con cố định cho M13")
    p.add_argument("--force", action="store_true")
    p = sub.add_parser("review", help="rà tay câu train")
    p.add_argument("--n", type=int)
    sub.add_parser("summary", help="qa_summary.md")
    args = ap.parse_args(argv)
    set_seed()
    setup_logging("WARNING")
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    env = QAEnv(args.repo_root)
    cmds = {
        "plan-test": cmd_plan,
        "show": cmd_show,
        "validate": cmd_validate,
        "generate": cmd_generate,
        "build": cmd_build,
        "subsets": cmd_subsets,
        "review": cmd_review,
        "summary": cmd_summary,
    }
    return cmds[args.cmd](env, args)


if __name__ == "__main__":
    raise SystemExit(main())
