"""M5: I/O dựng đồ thị → ``data/graph/`` (nodes, edges_struct, edges_legal) + báo cáo.

Resume theo ``input_sha256`` = hash nội dung ``units.jsonl``, ``unit_versions.jsonl``,
``units_added.jsonl``, ``documents.yaml``, ``doc_aliases.yaml``: bản ghi mới nhất trong
``graph_report.jsonl`` có cùng hash, ``status = ok`` và các file đầu ra còn nguyên (hash khớp)
→ bỏ qua. Khóa không chứa phiên bản code ⇒ **sửa code M5 thì chạy với ``--force``**.

Đầu ra ghi bằng ``write_jsonl`` (file tạm + ``os.replace``), đã sắp xếp → tất định.
"""

from __future__ import annotations

import hashlib
import random
from collections import Counter, defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Literal

from trafficlaw.graph.build import GraphData, build_graph, dangling_edges
from trafficlaw.graph.doc_names import DocNameTable, load_doc_aliases
from trafficlaw.graph.schema import (
    LEGAL_EDGE_TYPES,
    MAX_EDGES,
    MAX_NODES,
    NODE_LABEL_ORDER,
    STRUCT_EDGE_TYPES,
    Edge,
)
from trafficlaw.ingest.amendment_pipeline import load_units
from trafficlaw.ingest.versions import AddedUnit, UnitVersion
from trafficlaw.registry.loader import load_registry
from trafficlaw.utils.jsonl import append_jsonl, read_jsonl, write_jsonl


@dataclass(frozen=True)
class GraphPaths:
    units: Path
    unit_versions: Path
    units_added: Path
    documents: Path
    doc_aliases: Path
    nodes: Path
    edges_struct: Path
    edges_legal: Path
    unresolved: Path
    report: Path
    summary: Path
    review: Path

    def inputs(self) -> list[Path]:
        return [self.units, self.unit_versions, self.units_added, self.documents, self.doc_aliases]

    def outputs(self) -> list[Path]:
        return [self.nodes, self.edges_struct, self.edges_legal]


@dataclass
class GraphOutcome:
    action: Literal["processed", "skipped"]
    record: dict[str, Any]


def file_sha256(path: Path) -> str:
    if not path.exists():
        return "missing"
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def input_sha256(paths: Sequence[Path]) -> str:
    h = hashlib.sha256()
    for p in paths:
        h.update(p.name.encode("utf-8") + b"\0" + file_sha256(p).encode("ascii") + b"\0")
    return h.hexdigest()


def latest_report(path: Path) -> dict[str, Any] | None:
    last: dict[str, Any] | None = None
    if path.exists():
        for rec in read_jsonl(path):
            last = rec
    return last


def _ref_rate(c: Mapping[str, int], *, excl_appendix: bool = False) -> float | None:
    """Tỷ lệ span phân giải được; ``excl_appendix``: bỏ span tới Phụ lục chưa có unit (M3)."""
    n = c.get("spans", 0) - (c.get("phu_luc_khong_co_unit", 0) if excl_appendix else 0)
    return round(c.get("resolved", 0) / n, 4) if n else None


def make_record(data: GraphData, input_hash: str, git_commit: str | None) -> dict[str, Any]:
    nodes_by = Counter(n.label for n in data.nodes)
    struct_by = Counter(e.type for e in data.edges_struct)
    legal_by = Counter(e.type for e in data.edges_legal)
    dangling = dangling_edges(data.nodes, [*data.edges_struct, *data.edges_legal])
    n_edges = len(data.edges_struct) + len(data.edges_legal)
    problems = list(data.errors)
    if dangling:
        problems.append(f"{len(dangling)} cạnh trỏ tới nút không tồn tại")
    if len(data.nodes) > MAX_NODES:
        problems.append(f"{len(data.nodes)} nút > {MAX_NODES}")
    if n_edges > MAX_EDGES:
        problems.append(f"{n_edges} cạnh > {MAX_EDGES}")
    ext = sorted(
        (n for n in data.nodes if n.label == "VanBanNgoai"),
        key=lambda n: (-n.props["n_refs"], n.id),
    )
    total = Counter[str]()
    for c in data.ref_stats.values():
        total.update(c)
    return {
        "input_sha256": input_hash,
        "status": "error" if problems else "ok",
        "problems": problems,
        "n_nodes": len(data.nodes),
        "n_edges": n_edges,
        "nodes_by_label": {k: nodes_by[k] for k in NODE_LABEL_ORDER if nodes_by[k]},
        "edges_by_type": {
            **{k: struct_by[k] for k in STRUCT_EDGE_TYPES if struct_by[k]},
            **{k: legal_by[k] for k in LEGAL_EDGE_TYPES if legal_by[k]},
        },
        "dan_chieu_by_scope": dict(
            sorted(
                Counter(
                    e.props["pham_vi"] for e in data.edges_legal if e.type == "DAN_CHIEU"
                ).items()
            )
        ),
        "dan_chieu_by_quan_he": dict(
            sorted(
                Counter(
                    e.props["quan_he"]
                    for e in data.edges_legal
                    if e.type == "DAN_CHIEU" and "quan_he" in e.props
                ).items()
            )
        ),
        "ref_stats": {d: dict(sorted(c.items())) for d, c in sorted(data.ref_stats.items())},
        "ref_rate_total": _ref_rate(total),
        "ref_rate_excl_appendix": _ref_rate(total, excl_appendix=True),
        "n_unresolved": len(data.unresolved),
        "unresolved_by_reason": dict(sorted(Counter(u["reason"] for u in data.unresolved).items())),
        "n_uy_quyen": sum(len(n.props.get("uy_quyen", ())) for n in data.nodes),
        "top_external": [
            [n.id, n.props.get("ten") or n.props.get("so_hieu"), n.props["n_refs"]]
            for n in ext[:30]
        ],
        "n_dangling": len(dangling),
        "git_commit": git_commit,
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
    }


def summary_markdown(rec: Mapping[str, Any]) -> str:
    lines = [
        "# Đồ thị (M5) — tổng hợp",
        "",
        f"- Trạng thái: **{rec['status']}**"
        + (f" — {'; '.join(rec['problems'])}" if rec["problems"] else ""),
        f"- Nút: **{rec['n_nodes']:,}** (giới hạn {MAX_NODES:,}); "
        f"cạnh: **{rec['n_edges']:,}** (giới hạn {MAX_EDGES:,})",
        f"- Cạnh treo: {rec['n_dangling']}; dẫn chiếu không phân giải: {rec['n_unresolved']}; "
        f"thuộc tính uy_quyen: {rec['n_uy_quyen']}",
        f"- Tỷ lệ span dẫn chiếu phân giải được: **{_pct(rec['ref_rate_total'])}**; không tính "
        f"span tới Phụ lục chưa có unit (giới hạn M3): **{_pct(rec['ref_rate_excl_appendix'])}**",
        "",
        "## Nút theo nhãn",
        "",
        "| Nhãn | Số nút |",
        "| --- | ---: |",
        *[f"| {k} | {v:,} |" for k, v in rec["nodes_by_label"].items()],
        "",
        "## Cạnh theo loại",
        "",
        "| Loại | Số cạnh |",
        "| --- | ---: |",
        *[f"| {k} | {v:,} |" for k, v in rec["edges_by_type"].items()],
        "",
        "DAN_CHIEU theo phạm vi: "
        + ", ".join(f"{k} {v:,}" for k, v in rec["dan_chieu_by_scope"].items())
        + "; tới chính unit / tổ tiên (props.quan_he): "
        + ", ".join(f"{k} {v:,}" for k, v in rec["dan_chieu_by_quan_he"].items()),
        "",
        "## Dẫn chiếu theo văn bản nguồn",
        "",
        "Đếm theo phiên bản. `span` = cụm điểm/khoản/Điều/Phụ lục; "
        "`phân giải` = đọc được và mọi đích tồn tại.",
        "",
        "| Văn bản | span | phân giải | tỷ lệ | tỷ lệ (bỏ PL) | lỗi đọc | đích không tồn tại "
        "| PL chưa có unit | → chính unit | → tổ tiên | nhắc văn bản |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for d, c in rec["ref_stats"].items():
        lines.append(
            f"| {d} | {c.get('spans', 0)} | {c.get('resolved', 0)} | {_pct(_ref_rate(c))} | "
            f"{_pct(_ref_rate(c, excl_appendix=True))} | {c.get('loi_doc', 0)} | "
            f"{c.get('dich_khong_ton_tai', 0)} | {c.get('phu_luc_khong_co_unit', 0)} | "
            f"{c.get('chinh_unit', 0)} | {c.get('to_tien', 0)} | {c.get('nhac_van_ban', 0)} |"
        )
    lines += [
        "",
        "## Không phân giải theo lý do",
        "",
        *[f"- {k}: {v}" for k, v in rec["unresolved_by_reason"].items()],
        "",
        "## Văn bản ngoài danh mục được nhắc nhiều nhất",
        "",
        "| Mã | Tên/số hiệu | Số cạnh tới |",
        "| --- | --- | ---: |",
        *[f"| `{i}` | {t} | {n} |" for i, t, n in rec["top_external"]],
        "",
    ]
    return "\n".join(lines)


def _pct(x: float | None) -> str:
    return "—" if x is None else f"{x * 100:.2f}%".replace(".", ",")


# ------------------------------------------------------------------ rà tay


def _snippet(text: str, span: str, width: int = 90) -> str:
    i = text.find(span)
    if i < 0:
        return text[:width].replace("\n", " ⏎ ")
    a, b = max(0, i - width), min(len(text), i + len(span) + 40)
    s = text[a:i] + "**" + span + "**" + text[i + len(span) : b]
    return (
        ("…" if a else "")
        + s.replace("\n", " ⏎ ").replace("|", "\\|")
        + ("…" if b < len(text) else "")
    )


def _stratified(edges: Sequence[Edge], n: int, seed: int) -> list[Edge]:
    """``n`` cạnh ngẫu nhiên, phân tầng theo văn bản nguồn (tỷ lệ, mỗi văn bản ≥ 1)."""
    by_doc: dict[str, list[Edge]] = defaultdict(list)
    for e in edges:
        by_doc[e.src.split("/")[0].split("@")[0]].append(e)
    docs = sorted(by_doc)
    if not docs:
        return []
    total = len(edges)
    quota = {d: max(1, round(n * len(by_doc[d]) / total)) for d in docs}
    while sum(quota.values()) > n:
        d = max(docs, key=lambda d: (quota[d], d))
        quota[d] -= 1
    while sum(quota.values()) < n and sum(quota.values()) < total:
        d = max(docs, key=lambda d: (len(by_doc[d]) - quota[d], d))
        quota[d] += 1
    rng = random.Random(seed)
    out: list[Edge] = []
    for d in docs:
        out.extend(rng.sample(by_doc[d], min(quota[d], len(by_doc[d]))))
    return out


def review_markdown(data: GraphData, n: int = 50, seed: int = 42) -> str:
    texts: dict[str, str] = {}
    latest: dict[str, tuple[int, str]] = {}
    titles: dict[str, str] = {}
    for node in data.nodes:
        if node.label == "PhienBan":
            texts[node.id] = node.props["text"]
            uid, ver = node.props["unit_id"], node.props["version"]
            if node.props["text"] and ver >= latest.get(uid, (-1, ""))[0]:
                latest[uid] = (ver, node.props["text"])
        else:
            titles[node.id] = node.props.get("ten") or node.props.get("title") or ""

    def dst_text(dst: str) -> str:
        if dst in latest:
            return latest[dst][1][:160].replace("\n", " ⏎ ").replace("|", "\\|")
        return (titles.get(dst) or "")[:160]

    dc = [e for e in data.edges_legal if e.type == "DAN_CHIEU"]
    sample = _stratified(dc, n, seed)
    lines = [
        "# Rà tay M5",
        "",
        f"## {len(sample)} cạnh DAN_CHIEU ngẫu nhiên (seed {seed}, phân tầng theo văn bản nguồn)",
        "",
        "Đánh dấu cột **Đúng?** (✓/✗). Đúng = đích là đúng điều khoản/văn bản mà cụm in đậm "
        "chỉ tới.",
        "",
        "| # | Nguồn (phiên bản) | Ngữ cảnh | Đích | Nội dung đích | Đúng? |",
        "| ---: | --- | --- | --- | --- | --- |",
    ]
    for i, e in enumerate(sample, 1):
        ctx = _snippet(texts.get(e.src, ""), e.props.get("span", ""))
        tgt = e.dst + (f" ({e.props['target_ref']})" if e.props.get("target_ref") else "")
        lines.append(f"| {i} | `{e.src}` | {ctx} | `{tgt}` | {dst_text(e.dst)} | |")
    hd = [e for e in data.edges_legal if e.type == "HUONG_DAN"]
    lines += [
        "",
        f"## Toàn bộ HUONG_DAN ({len(hd)} cạnh)",
        "",
        "| # | Văn bản hướng dẫn | Đích | Cấp | Cụm trong câu | Nguồn | Đúng? |",
        "| ---: | --- | --- | --- | --- | --- | --- |",
    ]
    for i, e in enumerate(hd, 1):
        lines.append(
            f"| {i} | `{e.src}` | `{e.dst}` | {e.props['cap']} | {e.props['span']} | "
            f"`{e.props['source_unit_id']}` | |"
        )
    lines += ["", "## Kiểm tra cụ thể", ""]
    checks = [
        (
            "HUONG_DAN ND165 → LUAT35",
            any(e.src == "ND165-2024" and e.dst == "LUAT35-2024" for e in hd),
        ),
        (
            "HUONG_DAN ND165 → LUAT36/D77",
            any(e.src == "ND165-2024" and e.dst == "LUAT36-2024/D77" for e in hd),
        ),
        (
            "SUA_DOI ND238 → ND168/D6/K3/m từ 2026-08-15",
            any(
                e.type == "SUA_DOI"
                and e.src == "ND238-2026"
                and e.dst == "ND168-2024/D6/K3/m"
                and e.props.get("effective_from") == "2026-08-15"
                for e in data.edges_legal
            ),
        ),
    ]
    lines += [f"- {'✓' if ok else '✗'} {name}" for name, ok in checks]
    nd168: dict[tuple[str, str], list[str]] = defaultdict(list)
    for e in dc:
        if e.src.startswith("ND168-2024/D6/") and "này" in e.props.get("span", ""):
            nd168[(e.src, e.props["span"])].append(e.dst)
    lines += ["", f'### ND168 Đ6: dẫn chiếu "… này" ({len(nd168)} span)', ""]
    lines += [
        f"- `{src}` «{span}» → " + ", ".join(f"`{d.split('/', 1)[1]}`" for d in dsts)
        for (src, span), dsts in sorted(nd168.items())
    ]
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------------ chạy


def load_inputs(paths: GraphPaths) -> tuple[Any, ...]:
    registry = load_registry(paths.documents)
    units = [u for lst in load_units(paths.units).values() for u in lst]
    added = (
        [AddedUnit.model_validate(r) for r in read_jsonl(paths.units_added)]
        if paths.units_added.exists()
        else []
    )
    versions = [UnitVersion.model_validate(r) for r in read_jsonl(paths.unit_versions)]
    names = DocNameTable(registry, *load_doc_aliases(paths.doc_aliases))
    return registry, units, added, versions, names


def run_build_graph(
    paths: GraphPaths,
    *,
    git_commit: str | None = None,
    force: bool = False,
    review_n: int = 50,
    seed: int = 42,
) -> GraphOutcome:
    h = input_sha256(paths.inputs())
    last = latest_report(paths.report)
    if (
        not force
        and last is not None
        and last.get("status") == "ok"
        and last.get("input_sha256") == h
        and all(
            file_sha256(p) == last.get("output_sha256", {}).get(p.name) for p in paths.outputs()
        )
    ):
        return GraphOutcome("skipped", last)
    data = build_graph(*load_inputs(paths))
    rec = make_record(data, h, git_commit)
    write_jsonl(paths.nodes, data.nodes)
    write_jsonl(paths.edges_struct, data.edges_struct)
    write_jsonl(paths.edges_legal, data.edges_legal)
    write_jsonl(paths.unresolved, data.unresolved)
    rec["output_sha256"] = {p.name: file_sha256(p) for p in paths.outputs()}
    append_jsonl(paths.report, rec)
    paths.summary.write_text(summary_markdown(rec), encoding="utf-8", newline="\n")
    paths.review.write_text(review_markdown(data, review_n, seed), encoding="utf-8", newline="\n")
    return GraphOutcome("processed", rec)
