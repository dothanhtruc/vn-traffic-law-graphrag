"""M8: I/O của trích xuất — gọi LLM theo lô (resume được), dựng nút/cạnh ứng viên, publish khi
đạt ngưỡng F1.

Luồng ``scripts.build_graph --extract``:

1. ``select_items`` + ``make_batches`` (lô = nhiều Điều cùng văn bản; bỏ item đã có kết quả
   ``ok``/``format_error`` cùng ``model_id`` + ``prompt_hash`` + ``schema_hash`` trong
   ``raw.jsonl``).
2. Mỗi lô: ``client.generate`` (JSON schema có enum danh mục) → một dòng ``raw.jsonl`` (flush
   ngay). ``QuotaExhaustedError`` → dừng sạch, in lệnh chạy tiếp.
3. ``assemble``: rule (toàn bộ phạm vi) + kết quả LLM đã có → ``candidates_{nodes,edges}.jsonl``,
   ``rejected.jsonl``, ``data/graph/extraction_report.jsonl`` (append), ``extraction_summary.md``.
4. ``publish``: chỉ khi ``eval_report.json`` (``scripts.eval_extraction``) đạt ngưỡng **trên đúng
   bản ứng viên hiện hành** (``candidates_sha256``) → ``data/graph/{nodes,edges}_semantic.jsonl``.
"""

from __future__ import annotations

import hashlib
import json
import logging
import shutil
import statistics
import time
from collections import Counter
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Protocol

import yaml

from trafficlaw.graph.extract import (
    Assembly,
    Batch,
    Catalog,
    ExtractConfig,
    Item,
    ItemResult,
    assemble_catalog,
    assemble_llm,
    assemble_rules,
    batch_schema,
    make_batches,
    map_batch_output,
    prune_dangling,
    render_catalog,
    render_items,
    select_items,
    sha256,
)
from trafficlaw.graph.schema import MAX_EDGES, MAX_NODES
from trafficlaw.graph.store import BaseGraphStore, canonical_json
from trafficlaw.llm import LLMResult, Prompt, QuotaExhaustedError, load_prompt
from trafficlaw.llm.parallel import map_parallel
from trafficlaw.utils.jsonl import JsonlWriter, append_jsonl, read_jsonl, write_jsonl

logger = logging.getLogger(__name__)

RESUME_HINT = "uv run python -m scripts.build_graph --extract"


class Client(Protocol):
    @property
    def model_id(self) -> str: ...

    @property
    def provider_name(self) -> str: ...

    def generate(self, messages: Sequence[Any], **kw: Any) -> LLMResult: ...


@dataclass(frozen=True)
class ExtractPaths:
    graph_dir: Path
    out_dir: Path
    catalog: Path

    @property
    def raw(self) -> Path:
        return self.out_dir / "raw.jsonl"

    @property
    def cand_nodes(self) -> Path:
        return self.out_dir / "candidates_nodes.jsonl"

    @property
    def cand_edges(self) -> Path:
        return self.out_dir / "candidates_edges.jsonl"

    @property
    def rejected(self) -> Path:
        return self.out_dir / "rejected.jsonl"

    @property
    def report(self) -> Path:
        return self.graph_dir / "extraction_report.jsonl"

    @property
    def summary(self) -> Path:
        return self.graph_dir / "extraction_summary.md"

    @property
    def sem_nodes(self) -> Path:
        return self.graph_dir / "nodes_semantic.jsonl"

    @property
    def sem_edges(self) -> Path:
        return self.graph_dir / "edges_semantic.jsonl"


# --------------------------------------------------------------------------- danh mục


CATALOG_HEADER = """\
# M8: danh mục đóng PhuongTien / ChuThe — BẢN NHÁP do rule dựng từ văn bản (graph/catalog.py).
# Người dùng duyệt: sửa/xoá mục, rồi đặt approved: true. Trích xuất thật và preannotate từ chối
# chạy khi approved: false. Alias chỉ thêm khi có căn cứ trong văn bản ("sau đây gọi là …").
# Sửa danh mục ⇒ schema/prompt đổi ⇒ các lô LLM chạy lại (khoá resume chứa schema_hash).
"""


def load_catalog(path: Path) -> Catalog | None:
    if not path.is_file():
        return None
    return Catalog.model_validate(yaml.safe_load(path.read_text(encoding="utf-8")) or {})


def write_catalog(path: Path, cat: Catalog) -> None:
    body = yaml.safe_dump(
        cat.model_dump(mode="json"), allow_unicode=True, sort_keys=False, width=100
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((CATALOG_HEADER + body).encode("utf-8"))


# --------------------------------------------------------------------------- khoá


@dataclass(frozen=True)
class RunKey:
    model_id: str
    prompt_hash: str
    schema_hash: str


def run_key(model_id: str, prompt: Prompt, catalog: Catalog) -> RunKey:
    schema = batch_schema(catalog).model_json_schema()
    return RunKey(model_id, prompt.hash, sha256(schema))


def build_messages(prompt: Prompt, batch: Batch, catalog: Catalog) -> list[dict[str, str]]:
    pt, ct = render_catalog(catalog)
    return [
        {
            "role": "user",
            "content": prompt.render(catalog_pt=pt, catalog_ct=ct, items=render_items(batch)),
        }
    ]


def _matches(rec: dict[str, Any], key: RunKey) -> bool:
    return (
        rec.get("model_id") == key.model_id
        and rec.get("prompt_hash") == key.prompt_hash
        and rec.get("schema_hash") == key.schema_hash
    )


def done_item_keys(raw: Path, key: RunKey, *, retry_format_error: bool = False) -> set[str]:
    """Item đã xong: có bản ghi ``ok`` (hoặc ``format_error`` — tính là sai, không gọi lại trừ
    khi ``retry_format_error``) cùng khoá chạy. ``error`` (hết retry) → chạy lại."""
    ok = {"ok"} if retry_format_error else {"ok", "format_error"}
    out: set[str] = set()
    for rec in read_jsonl(raw):
        if _matches(rec, key) and rec.get("status") in ok:
            out.update(rec.get("item_keys") or [])
    return out


# --------------------------------------------------------------------------- ước tính


DEFAULT_OUTPUT_TOKENS_PER_ITEM = 200
"""Token đầu ra / item khi chưa có bản ghi để hiệu chỉnh (đo thật 09/11/2026: ~193)."""


def output_tokens_per_item(raw: Path, default: float = DEFAULT_OUTPUT_TOKENS_PER_ITEM) -> float:
    """Hiệu chỉnh từ các bản ghi ``ok`` không cache đã có (mọi model); chưa có → ``default``."""
    n_items = 0
    n_tok = 0
    for rec in read_jsonl(raw):
        if rec.get("status") == "ok" and not rec.get("cached"):
            n_items += len(rec.get("item_keys") or [])
            n_tok += int((rec.get("usage") or {}).get("completion_tokens") or 0)
    return n_tok / n_items if n_items >= 20 and n_tok else default


def estimate(
    batches: Sequence[Batch],
    items: Sequence[Item],
    prompt: Prompt,
    catalog: Catalog,
    *,
    out_per_item: float = DEFAULT_OUTPUT_TOKENS_PER_ITEM,
) -> dict[str, Any]:
    """Số item/lô/token ước tính theo tier và văn bản (CLAUDE.md mục 11): token prompt =
    ``len/4`` (thận trọng), token đầu ra = ``out_per_item`` × số item."""
    by: dict[str, dict[str, Any]] = {}
    for b in batches:
        tok = len(build_messages(prompt, b, catalog)[0]["content"]) // 4
        doc = b.group_id.split("/")[0]
        tier = b.items[0].tier
        for k in (f"tier:{tier}", f"doc:{doc}", "total"):
            s = by.setdefault(k, {"batches": 0, "items": 0, "prompt_tokens": 0, "output_tokens": 0})
            s["batches"] += 1
            s["items"] += len(b.items)
            s["prompt_tokens"] += tok
            s["output_tokens"] += round(out_per_item * len(b.items))
    n_all = len(items)
    n_unique = len({i.key for i in items})
    return {"n_items": n_all, "n_unique": n_unique, "groups": dict(sorted(by.items()))}


# --------------------------------------------------------------------------- chạy LLM


@dataclass
class RunOutcome:
    n_items: int = 0
    n_todo_batches: int = 0
    n_called: int = 0
    by_status: Counter[str] = field(default_factory=Counter)
    stopped: str | None = None
    hint: str = ""


def run_llm(
    store: BaseGraphStore,
    cfg: ExtractConfig,
    catalog: Catalog,
    client: Client,
    paths: ExtractPaths,
    *,
    doc_ids: Sequence[str] | None = None,
    only_units: set[str] | None = None,
    max_calls: int | None = None,
    retry_format_error: bool = False,
    git_commit: str | None = None,
    resume_cmd: str = RESUME_HINT,
    progress: Callable[[int, int, Batch, LLMResult], None] | None = None,
    workers: int = 1,
    run_meta: Mapping[str, Any] | None = None,
) -> RunOutcome:
    """Gọi LLM cho các lô chưa xong. ``workers`` > 1: gọi song song (server vLLM tự host gộp
    batch); chỉ luồng này ghi ``raw.jsonl``. ``run_meta`` (model/revision/vLLM phục vụ) được ghi
    vào mỗi bản ghi để tái lập."""
    prompt = load_prompt(cfg.llm.prompt)
    key = run_key(client.model_id, prompt, catalog)
    items = select_items(store, cfg, doc_ids)
    if only_units is not None:
        items = [i for i in items if i.unit_id in only_units]
    done = done_item_keys(paths.raw, key, retry_format_error=retry_format_error)
    batches = make_batches(items, cfg.batch, skip_keys=done)
    out = RunOutcome(n_items=len(items), n_todo_batches=len(batches))
    todo = batches if max_calls is None else batches[: max(0, max_calls)]
    schema = batch_schema(catalog)
    params = {"max_output_tokens": cfg.llm.max_output_tokens}

    def call(b: Batch) -> LLMResult:
        return client.generate(
            build_messages(prompt, b, catalog), json_schema=schema, params=params
        )

    meta = dict(run_meta or {})
    with JsonlWriter(paths.raw) as w:
        for b, r in map_parallel(todo, call, workers):
            if isinstance(r, QuotaExhaustedError):
                out.stopped = "quota"
                out.hint = (
                    f"Hết quota ngày ({r}). Đã xong {out.n_called}/{len(todo)} lô của lần chạy "
                    f"này; chạy lại sau khi quota reset: {resume_cmd}"
                )
                logger.error(out.hint)
                break
            w.write(
                {
                    "batch_id": b.batch_id,
                    "batch_key": b.key,
                    "item_keys": b.keys,
                    "unit_ids": [it.unit_id for it in b.items],
                    "version_ids": [it.version_id for it in b.items],
                    "model_id": r.model_id,
                    "provider": r.provider,
                    "prompt_hash": key.prompt_hash,
                    "schema_hash": key.schema_hash,
                    "status": r.status,
                    "parsed": r.parsed,
                    "text": None if r.status == "ok" else r.text[:4000],
                    "error": r.error,
                    "usage": r.usage.model_dump(),
                    "latency_ms": r.latency_ms,
                    "attempts": r.attempts,
                    "cached": r.cached,
                    "repair_prompt_hash": r.repair_prompt_hash,
                    **({"serve": meta} if meta else {}),
                    "git_commit": git_commit,
                    "run_at": datetime.now().astimezone().isoformat(timespec="seconds"),
                }
            )
            out.n_called += 1
            out.by_status[r.status] += 1
            if progress is not None:
                progress(out.n_called, len(todo), b, r)
    return out


# --------------------------------------------------------------------------- dựng ứng viên


def load_results(
    raw: Path, key: RunKey, items: Sequence[Item], catalog: Catalog
) -> tuple[dict[str, ItemResult], list[Any], dict[str, Any]]:
    """Kết quả LLM đã hậu kiểm (bản ghi ``ok`` mới nhất của mỗi lô) + rejection + thống kê."""
    by_key = {}
    for it in items:
        by_key.setdefault(it.key, it)
    results: dict[str, ItemResult] = {}
    rejections: list[Any] = []
    usage = Counter[str]()
    lat: list[int] = []
    status = Counter[str]()
    last: dict[str, dict[str, Any]] = {}
    for rec in read_jsonl(raw):
        if _matches(rec, key):
            status[rec["status"]] += 1
            for k in ("prompt_tokens", "completion_tokens", "total_tokens"):
                usage[k] += int((rec.get("usage") or {}).get(k) or 0)
            if not rec.get("cached"):
                lat.append(int(rec.get("latency_ms") or 0))
            if rec["status"] == "ok":
                last[rec["batch_key"]] = rec
    for rec in last.values():
        its = [by_key[k] for k in rec["item_keys"] if k in by_key]
        if len(its) != len(rec["item_keys"]):
            continue  # lô của phạm vi cũ (item đã đổi) — bỏ qua
        b = Batch(rec["batch_id"], its[0].doc_id, its)
        res, rej = map_batch_output(b, rec["parsed"] or {}, catalog)
        results.update(res)
        rejections += rej
    stats = {
        "records_by_status": dict(sorted(status.items())),
        "usage": dict(usage),
        "latency_ms_median": statistics.median(lat) if lat else None,
        "latency_ms_max": max(lat) if lat else None,
        "n_http_calls": len(lat),
    }
    return results, rejections, stats


def _file_sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else ""


def candidates_sha256(paths: ExtractPaths) -> str:
    return hashlib.sha256(
        (_file_sha(paths.cand_nodes) + _file_sha(paths.cand_edges)).encode()
    ).hexdigest()


def assemble(
    store: BaseGraphStore,
    cfg: ExtractConfig,
    catalog: Catalog,
    paths: ExtractPaths,
    *,
    model_id: str,
    doc_ids: Sequence[str] | None = None,
    git_commit: str | None = None,
) -> dict[str, Any]:
    """Dựng toàn bộ ứng viên (rule cho mọi phạm vi + LLM đã có), ghi file + báo cáo."""
    t0 = time.monotonic()
    prompt = load_prompt(cfg.llm.prompt)
    key = run_key(model_id, prompt, catalog)
    items = select_items(store, cfg, doc_ids)
    asm = Assembly()
    assemble_catalog(asm, catalog)
    assemble_rules(store, cfg, asm, doc_ids)
    results, rej, llm_stats = load_results(paths.raw, key, items, catalog)
    asm.rejections += rej
    assemble_llm(asm, items, results, model_id=model_id)
    prune_dangling(asm, store)
    nodes, edges = asm.sorted_nodes(), asm.sorted_edges()
    write_jsonl(paths.cand_nodes, [n.to_dict() for n in nodes])
    write_jsonl(
        paths.cand_edges, [{k: v for k, v in e.to_dict().items() if k != "key"} for e in edges]
    )
    write_jsonl(paths.rejected, [r.to_dict() for r in asm.rejections])

    base = store.count()
    n_nodes = sum(base["nodes"].values()) + len(nodes)
    n_edges = sum(base["edges"].values()) + len(edges)
    cov: dict[str, list[int]] = {}
    for it in items:
        for k in (f"tier:{it.tier}", f"doc:{it.doc_id}", "total"):
            c = cov.setdefault(k, [0, 0])
            c[1] += 1
            c[0] += it.key in results
    problems = []
    if n_nodes > MAX_NODES or n_edges > MAX_EDGES:
        problems.append(f"vượt giới hạn AuraDB Free: {n_nodes} nút / {n_edges} cạnh")
    rec = {
        "run_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "git_commit": git_commit,
        "model_id": model_id,
        "prompt_hash": key.prompt_hash,
        "schema_hash": key.schema_hash,
        "catalog_hash": catalog.hash(),
        "catalog_approved": catalog.approved,
        "n_items": len(items),
        "n_items_unique": len({i.key for i in items}),
        "coverage": {k: {"done": v[0], "total": v[1]} for k, v in sorted(cov.items())},
        "nodes_by_label": dict(sorted(Counter(n.label for n in nodes).items())),
        "edges_by_type": dict(sorted(Counter(e.type for e in edges).items())),
        "edges_by_nguon": dict(
            sorted(Counter(f"{e.type}:{e.props.get('nguon')}" for e in edges).items())
        ),
        "rejections_by_reason": dict(
            sorted(Counter(f"{r.kind}:{r.reason}" for r in asm.rejections).items())
        ),
        "stats": dict(sorted(asm.stats.items())),
        "llm": llm_stats,
        "graph_total": {"nodes": n_nodes, "edges": n_edges},
        "candidates_sha256": candidates_sha256(paths),
        "problems": problems,
        "status": "ok" if not problems else "error",
        "seconds": round(time.monotonic() - t0, 1),
    }
    append_jsonl(paths.report, rec)
    paths.summary.write_bytes(render_summary(rec).encode("utf-8"))
    return rec


def render_summary(rec: dict[str, Any]) -> str:
    lines = [
        "# Tổng hợp trích xuất thực thể (M8)",
        "",
        f"- Chạy: {rec['run_at']} · commit `{rec['git_commit']}` · model `{rec['model_id']}`",
        f"- prompt `{rec['prompt_hash'][:12]}` · schema `{rec['schema_hash'][:12]}` · danh mục "
        f"`{rec['catalog_hash'][:12]}` ({'đã duyệt' if rec['catalog_approved'] else 'CHƯA duyệt'})",
        f"- Item: {rec['n_items']:,} ({rec['n_items_unique']:,} text khác nhau)",
        f"- Tổng đồ thị nếu nạp: {rec['graph_total']['nodes']:,} nút / "
        f"{rec['graph_total']['edges']:,} cạnh (giới hạn {MAX_NODES:,} / {MAX_EDGES:,})",
        "",
        "## Độ phủ LLM (item đã có kết quả / tổng)",
        "",
        "| Nhóm | Xong | Tổng | % |",
        "| --- | ---: | ---: | ---: |",
    ]
    for k, v in rec["coverage"].items():
        pct = 100 * v["done"] / v["total"] if v["total"] else 0
        lines.append(f"| {k} | {v['done']:,} | {v['total']:,} | {pct:.1f} |")
    lines += ["", "## Nút ứng viên", "", "| Nhãn | Số |", "| --- | ---: |"]
    lines += [f"| {k} | {v:,} |" for k, v in rec["nodes_by_label"].items()]
    lines += ["", "## Cạnh ứng viên theo nguồn", "", "| Loại:nguồn | Số |", "| --- | ---: |"]
    lines += [f"| {k} | {v:,} |" for k, v in rec["edges_by_nguon"].items()]
    lines += ["", "## Bị loại", "", "| Loại:lý do | Số |", "| --- | ---: |"]
    lines += [f"| {k} | {v:,} |" for k, v in rec["rejections_by_reason"].items()] or ["| — | 0 |"]
    llm = rec["llm"]
    lines += [
        "",
        "## Lượt gọi LLM (khoá chạy hiện hành)",
        "",
        f"- Bản ghi theo trạng thái: {llm['records_by_status']}",
        f"- Lượt không cache: {llm['n_http_calls']} · latency median {llm['latency_ms_median']} ms"
        f" · max {llm['latency_ms_max']} ms",
        f"- Token: {llm['usage']}",
        "",
    ]
    if rec["problems"]:
        lines += ["## Lỗi", ""] + [f"- {p}" for p in rec["problems"]] + [""]
    return "\n".join(lines)


# --------------------------------------------------------------------------- publish


@dataclass
class PublishOutcome:
    ok: bool
    message: str


def publish(
    paths: ExtractPaths, eval_report: Path, *, min_entity_f1: float, min_relation_f1: float
) -> PublishOutcome:
    """Chép ứng viên vào ``data/graph/*_semantic.jsonl`` khi báo cáo F1 đạt ngưỡng trên đúng
    bản ứng viên hiện hành."""
    if not eval_report.is_file():
        return PublishOutcome(False, f"chưa có {eval_report} — chạy scripts.eval_extraction")
    rep = json.loads(eval_report.read_text(encoding="utf-8"))
    cur = candidates_sha256(paths)
    if rep.get("candidates_sha256") != cur:
        return PublishOutcome(False, "báo cáo F1 không phải của bản ứng viên hiện hành — chấm lại")
    ef = rep.get("overall", {}).get("entity", {}).get("f1")
    rf = rep.get("overall", {}).get("relation", {}).get("f1")
    if rep.get("n_reviewed", 0) == 0 or ef is None or rf is None:
        return PublishOutcome(False, "chưa có mục gold reviewed")
    if ef < min_entity_f1 or rf < min_relation_f1:
        return PublishOutcome(
            False,
            f"chưa đạt ngưỡng: F1 thực thể {ef:.3f} (cần ≥ {min_entity_f1}), "
            f"F1 quan hệ {rf:.3f} (cần ≥ {min_relation_f1})",
        )
    shutil.copyfile(paths.cand_nodes, paths.sem_nodes)
    shutil.copyfile(paths.cand_edges, paths.sem_edges)
    return PublishOutcome(
        True, f"đã ghi {paths.sem_nodes.name}, {paths.sem_edges.name} (F1 {ef:.3f}/{rf:.3f})"
    )


def summarize_estimate(est: dict[str, Any]) -> list[str]:
    rows = [f"item: {est['n_items']:,} ({est['n_unique']:,} text khác nhau)"]
    for k, v in est["groups"].items():
        rows.append(
            f"  {k:<24} {v['batches']:>5} lượt  {v['items']:>6} item  "
            f"~{v['prompt_tokens']:>9,} token vào  ~{v['output_tokens']:>8,} token ra"
        )
    return rows


__all__ = [
    "CATALOG_HEADER",
    "ExtractPaths",
    "PublishOutcome",
    "RunKey",
    "RunOutcome",
    "assemble",
    "build_messages",
    "candidates_sha256",
    "canonical_json",
    "done_item_keys",
    "estimate",
    "output_tokens_per_item",
    "load_catalog",
    "load_results",
    "publish",
    "run_key",
    "run_llm",
    "summarize_estimate",
    "write_catalog",
]
