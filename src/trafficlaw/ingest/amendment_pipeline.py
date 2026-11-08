"""Bước áp sửa đổi (M4): ``units.jsonl`` → ``unit_versions.jsonl`` + ``units_added.jsonl``.

- Văn bản đích = văn bản chỉ mục độc lập (``DocumentMeta.indexable``: bỏ VBHN, văn bản sửa đổi),
  gồm cả văn bản ``historical`` (TT 35/2024).
- Với mỗi đích: chỉ dẫn của các văn bản ``SUA_DOI`` nó, ngày hiệu lực riêng (Điều hiệu lực),
  bãi bỏ/thay thế toàn bộ (``relations`` toàn bộ), và todo ``ngoai_danh_muc`` từ chú thích VBHN
  của nó (Khoản do văn bản ngoài danh mục sửa — không tạo phiên bản, quyết định 07/11/2026).
- **Resume** theo ``(doc_id, input_sha256)``: hash gồm unit của đích, của văn bản sửa nó, của
  VBHN của nó, các mục danh mục liên quan, ``vbhn_map`` và ``amendment_overrides`` liên quan.
  Khoá không chứa phiên bản code ⇒ **sửa code M4 thì chạy lại với ``--force``**.
- Xử lý (lại) một đích: xoá bản ghi cũ của nó khỏi ``unit_versions.jsonl``/``units_added.jsonl``
  trước (ghi lại atomic), rồi ghi phiên bản → unit bổ sung → dòng report. ``amendment_todo.csv``
  được sinh lại từ report mới nhất của mọi đích sau mỗi lần chạy.
"""

from __future__ import annotations

import csv
import hashlib
import json
import logging
import re
from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict

from trafficlaw.ingest.amendments import (
    Extraction,
    LabelFix,
    Todo,
    extract_instructions,
)
from trafficlaw.ingest.effect import EffectOverride, parse_accepted_clause, parse_effects
from trafficlaw.ingest.structure import Unit
from trafficlaw.ingest.vbhn import VbhnEntry, footnotes_of, map_id
from trafficlaw.ingest.versioning import Delay, Repeal, build_versions
from trafficlaw.registry.loader import Registry
from trafficlaw.registry.schema import DocumentMeta
from trafficlaw.utils.jsonl import JsonlWriter, done_keys, read_jsonl, write_jsonl

logger = logging.getLogger(__name__)

RESUME_KEY = ("doc_id", "input_sha256")
TODO_COLUMNS = ("doc_id", "unit_id", "source_unit_id", "reason", "detail")
_EFFECT_TITLE = re.compile(r"hiệu\s+lực|thi\s+hành", re.I)


def load_label_fixes(path: str | Path) -> list[LabelFix]:
    path = Path(path)
    if not path.is_file():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return [LabelFix.model_validate(x) for x in data.get("label_fixes") or []]


def load_effect_overrides(path: str | Path) -> list[EffectOverride]:
    path = Path(path)
    if not path.is_file():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return [EffectOverride.model_validate(x) for x in data.get("effect_overrides") or []]


class AmendmentRecord(BaseModel):
    """Một dòng ``amendment_report.jsonl`` (append-only; bản ghi mới nhất của đích là hiện hành)."""

    model_config = ConfigDict(extra="forbid")

    doc_id: str
    input_sha256: str
    status: Literal["ok", "error"]
    error: str | None = None
    amending_docs: list[str] = []
    n_units: int = 0
    n_versions: int = 0
    n_added: int = 0
    n_changed_units: int = 0
    #: ``{văn bản sửa đổi: {op: [số chỉ dẫn, số áp được]}}``.
    instructions: dict[str, dict[str, list[int]]] = {}
    special_effects: dict[str, date] = {}
    #: Hiệu lực riêng của phần do văn bản sửa đổi đưa vào (effect_overrides đã duyệt).
    amendment_effects: dict[str, date] = {}
    general_effect: date | None = None
    todos: list[Todo] = []
    fixes_unapplied: list[str] = []
    #: Chỉ dẫn cụm từ không còn đối tượng (đích đã được chính văn bản sửa đổi viết lại).
    superseded: list[str] = []
    warnings: list[str] = []
    processed_at: datetime
    git_commit: str | None


@dataclass(frozen=True)
class AmendmentOutcome:
    doc_id: str
    action: Literal["processed", "skipped"]
    record: AmendmentRecord | None


def latest_reports(path: str | Path) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for rec in read_jsonl(path):
        out[rec["doc_id"]] = rec
    return out


def load_units(path: str | Path) -> dict[str, list[Unit]]:
    """``units.jsonl`` → ``{doc_id: [Unit]}`` (giữ thứ tự trong văn bản)."""
    out: dict[str, list[Unit]] = defaultdict(list)
    for r in read_jsonl(path):
        u = Unit.model_validate(r)
        out[u.doc_id].append(u)
    return dict(out)


def _sha(obj: object) -> str:
    blob = json.dumps(obj, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def _dump_units(units: Sequence[Unit]) -> list[dict[str, Any]]:
    return [u.model_dump(mode="json") for u in units]


@dataclass
class _Plan:
    doc: DocumentMeta
    amenders: list[DocumentMeta]
    full_repeal: list[tuple[DocumentMeta, date]]
    partial: list[DocumentMeta]
    vbhn: list[VbhnEntry]
    input_sha256: str


def _plans(
    registry: Registry,
    units: Mapping[str, Sequence[Unit]],
    vbhn_map: Sequence[VbhnEntry],
    label_fixes: Sequence[LabelFix],
    effect_overrides: Sequence[EffectOverride] = (),
) -> list[_Plan]:
    plans: list[_Plan] = []
    for doc in registry.indexable():
        amenders = [
            a
            for a in registry
            if a.is_amendment
            and any(r.type == "SUA_DOI" and r.target == doc.doc_id for r in a.relations)
        ]
        full: list[tuple[DocumentMeta, date]] = []
        partial: list[DocumentMeta] = []
        for other in registry:
            for r in other.relations:
                if r.target != doc.doc_id or r.type not in ("THAY_THE", "BAI_BO"):
                    continue
                if r.scope == "toan_bo" and r.effective_from is not None:
                    full.append((other, r.effective_from))
                else:
                    partial.append(other)
        vb = [e for e in vbhn_map if e.base_doc == doc.doc_id]
        a_ids = {a.doc_id for a in amenders}
        sha = _sha(
            {
                "doc": doc.model_dump(mode="json"),
                "units": _dump_units(units.get(doc.doc_id, ())),
                "amenders": [
                    {
                        "meta": a.model_dump(mode="json"),
                        "units": _dump_units(units.get(a.doc_id, ())),
                    }
                    for a in amenders
                ],
                "repeal": [(o.model_dump(mode="json"), d) for o, d in full],
                "partial": [o.model_dump(mode="json") for o in partial],
                "vbhn": [
                    {
                        "entry": e.model_dump(mode="json"),
                        "units": _dump_units(units.get(e.vbhn, ())),
                    }
                    for e in vb
                ],
                "fixes": [
                    f.model_dump() for f in label_fixes if f.source_unit_id.split("/")[0] in a_ids
                ],
                "effect_overrides": [
                    o.model_dump()
                    for o in effect_overrides
                    if o.unit_id.split("/")[0] == doc.doc_id
                ],
            }
        )
        plans.append(_Plan(doc, amenders, full, partial, vb, sha))
    return plans


def _repealing_unit(repealer: DocumentMeta, target: DocumentMeta, units: Sequence[Unit]) -> str:
    """Unit của văn bản bãi bỏ/thay thế có nhắc số hiệu đích (ưu tiên trong Điều hiệu lực)."""
    so = target.so_hieu or "\0"
    hits = [u for u in units if so in u.text and u.level in ("dieu", "khoan", "diem")]
    effect = [u for u in hits if re.search(r"hiệu\s+lực|bãi\s+bỏ|thay\s+thế", u.text)]
    best = effect or hits
    return best[-1].id if best else repealer.doc_id


def _vbhn_todos(
    entry: VbhnEntry, vbhn_units: Sequence[Unit], so_hieu_known: set[str]
) -> list[Todo]:
    out: list[Todo] = []
    out_reg = {s.upper() for s in entry.out_of_registry_sources}
    for fn in footnotes_of(vbhn_units):
        if fn.op == "quy_dinh" or fn.source_so_hieu is None:
            continue
        src = fn.source_so_hieu.upper()
        if src in out_reg or src not in so_hieu_known:
            out.append(
                Todo(
                    doc_id=entry.base_doc,
                    unit_id=map_id(fn.vbhn_unit_id, entry.vbhn, entry.base_doc),
                    source_unit_id=fn.vbhn_unit_id,
                    reason="ngoai_danh_muc",
                    detail=f"[^{fn.n}] {fn.text}"[:500],
                )
            )
    return out


def _dedupe(todos: Iterable[Todo]) -> list[Todo]:
    seen: set[tuple[Any, ...]] = set()
    out: list[Todo] = []
    for t in todos:
        k = (t.doc_id, t.unit_id, t.source_unit_id, t.reason, t.detail)
        if k not in seen:
            seen.add(k)
            out.append(t)
    return out


def _purge(path: Path, pred: Any) -> int:
    if not path.exists():
        return 0
    rows = list(read_jsonl(path))
    keep = [r for r in rows if not pred(r)]
    if len(keep) != len(rows):
        write_jsonl(path, keep)
    return len(rows) - len(keep)


def _belongs(unit_id: str, doc_ids: set[str]) -> bool:
    return unit_id.split("/")[0] in doc_ids


def process_target(
    plan: _Plan,
    units: Mapping[str, Sequence[Unit]],
    registry: Registry,
    label_fixes: Sequence[LabelFix],
    extraction_cache: dict[str, Extraction],
    effect_overrides: Sequence[EffectOverride] = (),
) -> tuple[AmendmentRecord, list[Any], list[Any]]:
    """Một văn bản đích → (report, phiên bản, unit bổ sung). Hàm không ghi file."""
    doc = plan.doc
    base = list(units.get(doc.doc_id, ()))
    todos: list[Todo] = []
    warnings: list[str] = []
    if not base:
        raise ValueError(f"không có unit của {doc.doc_id} trong units.jsonl")

    eff = parse_effects(doc.doc_id, base)
    todos.extend(eff.todos)
    if eff.general is not None and doc.hieu_luc_tu is not None and eff.general != doc.hieu_luc_tu:
        warnings.append(f"ngày hiệu lực trong văn bản {eff.general} ≠ danh mục {doc.hieu_luc_tu}")

    instructions = []
    stats: dict[str, dict[str, list[int]]] = {}
    fixes_unapplied: list[str] = []
    for a in plan.amenders:
        a_units = units.get(a.doc_id, ())
        if a.doc_id not in extraction_cache:
            a_eff = parse_effects(a.doc_id, a_units)
            fixes = [f for f in label_fixes if f.source_unit_id.split("/")[0] == a.doc_id]
            ex = extract_instructions(a, a_units, registry, a_eff.special, fixes)
            ex.todos.extend(a_eff.todos)
            if a_eff.general is not None and a.hieu_luc_tu and a_eff.general != a.hieu_luc_tu:
                ex.todos.append(
                    Todo(
                        doc_id=None,
                        source_unit_id=a.doc_id,
                        reason="hieu_luc_khong_ro",
                        detail=f"ngày trong văn bản {a_eff.general} ≠ danh mục {a.hieu_luc_tu}",
                    )
                )
            extraction_cache[a.doc_id] = ex
        ex = extraction_cache[a.doc_id]
        first_target = next(r.target for r in a.relations if r.type == "SUA_DOI")
        mine = [i for i in ex.instructions if i.target_doc == doc.doc_id]
        instructions.extend(mine)
        for t in ex.todos:
            if t.doc_id == doc.doc_id or (t.doc_id is None and first_target == doc.doc_id):
                todos.append(t.model_copy(update={"doc_id": doc.doc_id}))
        if first_target == doc.doc_id:
            fixes_unapplied.extend(ex.fixes_unapplied)
        st: dict[str, list[int]] = {}
        for i in mine:
            st.setdefault(i.op, [0, 0])[0] += 1
        stats[a.doc_id] = st

    # Câu hiệu lực riêng do văn bản sửa đổi đưa vào, người dùng đã duyệt (effect_overrides).
    delays: list[Delay] = []
    amendment_effects: dict[str, date] = {}
    accepted: set[tuple[str, str]] = set()
    for o in effect_overrides:
        if o.unit_id.split("/")[0] != doc.doc_id:
            continue
        src_ins = [
            i
            for i in instructions
            if i.target_id == o.unit_id and i.source_unit_id == o.source_unit_id and i.block
        ]
        if len(src_ins) != 1:
            raise ValueError(f"effect_overrides: không có chỉ dẫn {o.source_unit_id} → {o.unit_id}")
        block = src_ins[0].block
        assert block is not None
        ids, d, tail = parse_accepted_clause(doc.doc_id, block.text)
        accepted.add((o.unit_id, o.source_unit_id))
        src_doc = o.source_unit_id.split("/")[0]
        for uid in ids:
            delays.append(Delay(uid, src_doc, d, o.unit_id))
            amendment_effects[uid] = d
        if tail:
            todos.append(
                Todo(
                    doc_id=doc.doc_id,
                    unit_id=o.unit_id,
                    source_unit_id=o.source_unit_id,
                    reason="hieu_luc_khong_ro",
                    detail=f"đã áp từ {d}; điều kiện còn lại chưa biểu diễn: {tail}"[:500],
                )
            )

    # Chỉ dẫn sửa Điều hiệu lực của đích → cần rà tay (ngày hiệu lực riêng mới).
    effect_dieu = {u.id for u in base if u.level == "dieu" and _EFFECT_TITLE.search(u.title or "")}
    for i in instructions:
        if (i.target_id, i.source_unit_id) in accepted:
            continue
        if "/".join(i.target_id.split("/")[:2]) in effect_dieu:
            todos.append(
                Todo(
                    doc_id=doc.doc_id,
                    unit_id=i.target_id,
                    source_unit_id=i.source_unit_id,
                    reason="hieu_luc_sua_doi",
                    detail=f"chỉ dẫn sửa Điều hiệu lực, ngày riêng mới không được áp: {i.sentence}"[
                        :500
                    ],
                )
            )

    repeal = None
    if plan.full_repeal:
        other, d = min(plan.full_repeal, key=lambda x: x[1])
        repeal = Repeal(d, _repealing_unit(other, doc, units.get(other.doc_id, ())))
    for other in plan.partial:
        todos.append(
            Todo(
                doc_id=doc.doc_id,
                source_unit_id=other.doc_id,
                reason="thay_the_mot_phan",
                detail=(
                    f"{other.so_hieu} thay thế/bãi bỏ một phần {doc.so_hieu} nhưng không ghi rõ "
                    "điều khoản → không biểu diễn ở cấp Khoản"
                ),
            )
        )
    appendices = {
        u.id: u for a in plan.amenders for u in units.get(a.doc_id, ()) if u.level == "phu_luc"
    }
    res = build_versions(
        doc,
        base,
        instructions,
        special=eff.special,
        repeal=repeal,
        amending_appendices=appendices,
        source_paths={a.doc_id: a.source_path for a in plan.amenders},
        delays=delays,
    )
    todos.extend(res.todos)
    for i in instructions:
        if i.seq in res.applied:
            stats[i.source_unit_id.split("/")[0]][i.op][1] += 1
    so_known = {(d.so_hieu or "").upper() for d in registry}
    for e in plan.vbhn:
        todos.extend(_vbhn_todos(e, units.get(e.vbhn, ()), so_known))

    known = {u.id for u in base} | {a.id for a in res.added}
    stray = sorted({v.unit_id for v in res.versions} - known)
    if stray:
        raise ValueError(f"phiên bản của unit không có trong units/units_added: {stray[:5]}")
    changed = {v.unit_id for v in res.versions if v.version > 0}
    rec = AmendmentRecord(
        doc_id=doc.doc_id,
        input_sha256=plan.input_sha256,
        status="ok",
        amending_docs=[a.doc_id for a in plan.amenders],
        n_units=len(base),
        n_versions=len(res.versions),
        n_added=len(res.added),
        n_changed_units=len(changed),
        instructions=stats,
        special_effects=eff.special,
        amendment_effects=amendment_effects,
        general_effect=eff.general,
        todos=_dedupe(todos),
        fixes_unapplied=fixes_unapplied,
        superseded=res.superseded,
        warnings=warnings,
        processed_at=datetime.now(UTC),
        git_commit=None,
    )
    return rec, list(res.versions), list(res.added)


def run_amendments(
    *,
    units_path: Path,
    versions_path: Path,
    added_path: Path,
    report_path: Path,
    todo_path: Path,
    registry: Registry,
    vbhn_map: Sequence[VbhnEntry],
    label_fixes: Sequence[LabelFix],
    git_commit: str | None,
    effect_overrides: Sequence[EffectOverride] = (),
    doc_ids: Iterable[str] | None = None,
    force: bool = False,
) -> list[AmendmentOutcome]:
    units = load_units(units_path)
    plans = _plans(registry, units, vbhn_map, label_fixes, effect_overrides)
    wanted = set(doc_ids) if doc_ids else None
    if wanted:
        unknown = wanted - {p.doc.doc_id for p in plans}
        if unknown:
            raise KeyError(f"doc_id không phải văn bản đích: {sorted(unknown)}")
        plans = [p for p in plans if p.doc.doc_id in wanted]
    done = (
        set() if force else done_keys(report_path, RESUME_KEY, where=lambda r: r["status"] == "ok")
    )
    todo_plans = [p for p in plans if (p.doc.doc_id, p.input_sha256) not in done]
    redo = {p.doc.doc_id for p in todo_plans}
    if redo:
        n1 = _purge(versions_path, lambda r: _belongs(r["unit_id"], redo))
        n2 = _purge(added_path, lambda r: r["doc_id"] in redo)
        if n1 or n2:
            logger.info("Xoá %d phiên bản, %d unit bổ sung cũ của các đích sắp xử lý lại", n1, n2)

    outcomes: list[AmendmentOutcome] = []
    cache: dict[str, Extraction] = {}
    with (
        JsonlWriter(versions_path) as vw,
        JsonlWriter(added_path) as aw,
        JsonlWriter(report_path) as rw,
    ):
        for p in plans:
            if p not in todo_plans:
                outcomes.append(AmendmentOutcome(p.doc.doc_id, "skipped", None))
                continue
            try:
                rec, versions, added = process_target(
                    p, units, registry, label_fixes, cache, effect_overrides
                )
            except Exception as e:  # lỗi của một đích không dừng cả job
                logger.exception("Lỗi khi áp sửa đổi cho %s", p.doc.doc_id)
                rec = AmendmentRecord(
                    doc_id=p.doc.doc_id,
                    input_sha256=p.input_sha256,
                    status="error",
                    error=f"{type(e).__name__}: {e}",
                    processed_at=datetime.now(UTC),
                    git_commit=git_commit,
                )
            else:
                rec.git_commit = git_commit
                for v in versions:
                    vw.write(v)
                for a in added:
                    aw.write(a)
            rw.write(rec)
            outcomes.append(AmendmentOutcome(p.doc.doc_id, "processed", rec))
    write_todo_csv(
        todo_path,
        latest_reports(report_path),
        {p.doc.doc_id for p in _plans(registry, units, vbhn_map, label_fixes, effect_overrides)},
    )
    return outcomes


def write_todo_csv(path: Path, reports: Mapping[str, Mapping[str, Any]], doc_ids: set[str]) -> int:
    """Sinh lại ``amendment_todo.csv`` từ report mới nhất của các đích hiện có."""
    rows = [t for d, r in sorted(reports.items()) if d in doc_ids for t in r.get("todos") or []]
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".csv.tmp")
    with tmp.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=TODO_COLUMNS)
        w.writeheader()
        for t in rows:
            w.writerow({k: t.get(k) or "" for k in TODO_COLUMNS})
    tmp.replace(path)
    return len(rows)


def summary_markdown(reports: Mapping[str, Mapping[str, Any]]) -> str:
    """Bảng tổng hợp: theo văn bản đích, theo văn bản sửa đổi × op, và todo theo lý do."""
    lines = [
        "| đích | trạng thái | unit | phiên bản | unit đổi | unit bổ sung | todo | cảnh báo |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    by_amender: dict[tuple[str, str], list[int]] = {}
    reasons: Counter[str] = Counter()
    for d, r in sorted(reports.items()):
        lines.append(
            f"| {d} | {r['status']} | {r.get('n_units', 0)} | {r.get('n_versions', 0)} "
            f"| {r.get('n_changed_units', 0)} | {r.get('n_added', 0)} "
            f"| {len(r.get('todos') or [])} "
            f"| {'; '.join(r.get('warnings') or []) or (r.get('error') or '')} |"
        )
        for a, ops in (r.get("instructions") or {}).items():
            for op, (n, k) in ops.items():
                cur = by_amender.setdefault((a, op), [0, 0])
                cur[0] += n
                cur[1] += k
        for t in r.get("todos") or []:
            reasons[t["reason"]] += 1
    lines += ["", "| văn bản sửa đổi | thao tác | chỉ dẫn | áp được |", "|---|---|---:|---:|"]
    for (a, op), (n, k) in sorted(by_amender.items()):
        lines.append(f"| {a} | {op} | {n} | {k} |")
    lines += ["", "| lý do todo | số dòng |", "|---|---:|"]
    for reason, n in reasons.most_common():
        lines.append(f"| {reason} | {n} |")
    return "\n".join(lines) + "\n"
