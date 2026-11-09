"""Chấm trích xuất (M8): ghép cặp thực thể 1–1, P/R/F1 thực thể + quan hệ, CI bootstrap, tỷ lệ
người sửa bản nháp.

**Khớp thực thể** (cùng loại, cùng ``unit_id``):

- HanhVi: token-F1 của ``span`` (sau ``norm_name``) ≥ ``span_f1``; BienPhapBoSung: token-F1 của
  ``ten`` ≥ ``span_f1``;
- CheTai: ``loai`` + ``min_vnd``, ``max_vnd``, ``min_thang``, ``max_thang`` bằng nhau tuyệt đối;
- DiemGPLX: ``so_diem`` bằng nhau; KhaiNiem: ``norm_name(ten)`` bằng nhau;
- PhuongTien/ChuThe: ``catalog_id`` bằng nhau.

Ghép tham lam theo điểm giảm dần (mỗi thực thể vàng/dự đoán dùng tối đa một lần). **Khớp quan hệ**
= cùng loại, cùng unit nguồn, đích là cặp thực thể đã ghép. Micro-average; CI 95% bootstrap theo
bản ghi (Khoản), seed cố định.
"""

from __future__ import annotations

import random
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date
from typing import Any

from trafficlaw.graph.extract import norm_name
from trafficlaw.graph.store import GraphEdge, edge_in_effect, unit_of_version_id

NUM_FIELDS = ("min_vnd", "max_vnd", "min_thang", "max_thang")
LABEL_PROPS = {"name": "ten"}


@dataclass(frozen=True)
class Ent:
    id: str
    type: str
    unit_id: str
    attrs: tuple[tuple[str, Any], ...] = ()

    def get(self, k: str) -> Any:
        return dict(self.attrs).get(k)


@dataclass(frozen=True)
class Rel:
    type: str
    src_unit: str
    dst: str


def token_f1(a: str | None, b: str | None) -> float:
    ta, tb = norm_name(a or "").split(), norm_name(b or "").split()
    if not ta or not tb:
        return 0.0
    ca: dict[str, int] = {}
    for t in ta:
        ca[t] = ca.get(t, 0) + 1
    common = 0
    for t in tb:
        if ca.get(t, 0) > 0:
            common += 1
            ca[t] -= 1
    if common == 0:
        return 0.0
    p, r = common / len(tb), common / len(ta)
    return 2 * p * r / (p + r)


def match_score(g: Ent, p: Ent, span_f1: float) -> float:
    """> 0 nếu khớp (giá trị càng lớn càng tốt), 0 nếu không."""
    if g.type != p.type or g.unit_id != p.unit_id:
        return 0.0
    t = g.type
    if t == "HanhVi":
        s = token_f1(g.get("span"), p.get("span"))
        return s if s >= span_f1 else 0.0
    if t == "BienPhapBoSung":
        s = token_f1(g.get("ten"), p.get("ten"))
        return s if s >= span_f1 else 0.0
    if t == "CheTai":
        ok = g.get("loai") == p.get("loai") and all(g.get(f) == p.get(f) for f in NUM_FIELDS)
        return 1.0 if ok else 0.0
    if t == "DiemGPLX":
        return 1.0 if g.get("so_diem") == p.get("so_diem") else 0.0
    if t == "KhaiNiem":
        return 1.0 if norm_name(g.get("ten") or "") == norm_name(p.get("ten") or "") else 0.0
    if t in ("PhuongTien", "ChuThe"):
        return 1.0 if g.get("catalog_id") == p.get("catalog_id") else 0.0
    return 0.0


def align(gold: Sequence[Ent], pred: Sequence[Ent], span_f1: float) -> dict[str, str]:
    """pred id → gold id (ghép tham lam 1–1 theo điểm giảm dần, hoà → theo thứ tự id)."""
    pairs = []
    for g in gold:
        for p in pred:
            s = match_score(g, p, span_f1)
            if s > 0:
                pairs.append((-s, g.id, p.id))
    pairs.sort()
    used_g: set[str] = set()
    out: dict[str, str] = {}
    for _, gid, pid in pairs:
        if gid in used_g or pid in out:
            continue
        used_g.add(gid)
        out[pid] = gid
    return out


@dataclass
class Counts:
    tp: int = 0
    fp: int = 0
    fn: int = 0

    def add(self, o: Counts) -> None:
        self.tp += o.tp
        self.fp += o.fp
        self.fn += o.fn

    def prf(self) -> dict[str, float | int | None]:
        p = self.tp / (self.tp + self.fp) if self.tp + self.fp else None
        r = self.tp / (self.tp + self.fn) if self.tp + self.fn else None
        f = (
            2 * p * r / (p + r)
            if p is not None and r is not None and p + r > 0
            else (0.0 if (p is not None or r is not None) else None)
        )
        return {"precision": p, "recall": r, "f1": f, "tp": self.tp, "fp": self.fp, "fn": self.fn}


@dataclass
class RecordScore:
    gold_id: str
    tier: str
    stratum: str
    ent: dict[str, Counts] = field(default_factory=dict)
    rel: dict[str, Counts] = field(default_factory=dict)

    def total(self, kind: str) -> Counts:
        c = Counts()
        for v in (self.ent if kind == "entity" else self.rel).values():
            c.add(v)
        return c


def score_record(
    gold_id: str,
    tier: str,
    stratum: str,
    gold_ents: Sequence[Ent],
    gold_rels: Sequence[Rel],
    pred_ents: Sequence[Ent],
    pred_rels: Sequence[Rel],
    span_f1: float,
) -> RecordScore:
    m = align(gold_ents, pred_ents, span_f1)
    rs = RecordScore(gold_id, tier, stratum)
    matched_g = set(m.values())
    for p in pred_ents:
        rs.ent.setdefault(p.type, Counts())
        if p.id in m:
            rs.ent[p.type].tp += 1
        else:
            rs.ent[p.type].fp += 1
    for g in gold_ents:
        rs.ent.setdefault(g.type, Counts())
        if g.id not in matched_g:
            rs.ent[g.type].fn += 1
    gset = {(r.type, r.src_unit, r.dst) for r in gold_rels}
    pset = {(r.type, r.src_unit, m.get(r.dst, "∅" + r.dst)) for r in pred_rels}
    for t, s, d in pset:
        rs.rel.setdefault(t, Counts())
        if (t, s, d) in gset:
            rs.rel[t].tp += 1
        else:
            rs.rel[t].fp += 1
    for t, s, d in gset:
        rs.rel.setdefault(t, Counts())
        if (t, s, d) not in pset:
            rs.rel[t].fn += 1
    return rs


# --------------------------------------------------------------------------- gold / dự đoán → Ent


def gold_entities(rec: Mapping[str, Any]) -> tuple[list[Ent], list[Rel]]:
    ents = []
    for e in rec.get("entities") or []:
        attrs = tuple(
            sorted(
                (k, v) for k, v in e.items() if k not in ("id", "type", "unit_id") and v is not None
            )
        )
        ents.append(Ent(str(e["id"]), str(e["type"]), str(e["unit_id"]), attrs))
    rels = [
        Rel(str(r["type"]), str(r["src"]).removeprefix("unit:"), str(r["dst"]))
        for r in rec.get("relations") or []
    ]
    return ents, rels


@dataclass
class PredIndex:
    """Chỉ mục nút/cạnh ứng viên để lấy dự đoán cho từng bản ghi gold."""

    nodes: dict[str, dict[str, Any]]
    by_version: dict[str, list[str]]
    out_edges: dict[str, list[GraphEdge]]
    in_edges: dict[str, list[GraphEdge]]

    @classmethod
    def build(
        cls, nodes: Iterable[Mapping[str, Any]], edges: Iterable[Mapping[str, Any]]
    ) -> PredIndex:
        nd = {str(n["id"]): dict(n) for n in nodes}
        bv: dict[str, list[str]] = {}
        for nid, n in nd.items():
            vid = (n.get("props") or {}).get("version_id")
            if vid:
                bv.setdefault(str(vid), []).append(nid)
        oe: dict[str, list[GraphEdge]] = {}
        ie: dict[str, list[GraphEdge]] = {}
        for e in edges:
            ge = GraphEdge.from_dict(e)
            oe.setdefault(ge.src, []).append(ge)
            ie.setdefault(ge.dst, []).append(ge)
        return cls(nd, bv, oe, ie)


_ENT_FIELDS = (
    "span",
    "dieu_kien",
    "loai",
    "min_vnd",
    "max_vnd",
    "min_thang",
    "max_thang",
    "doi_tuong",
    "so_diem",
)


def pred_for_record(
    idx: PredIndex, version_ids: Sequence[str], as_of: date
) -> tuple[list[Ent], list[Rel]]:
    vset = set(version_ids)
    ents: dict[str, Ent] = {}
    rels: set[Rel] = set()
    for vid in sorted(vset):
        for nid in idx.by_version.get(vid, []):
            n = idx.nodes[nid]
            p = n.get("props") or {}
            attrs = {k: p.get(k) for k in _ENT_FIELDS if p.get(k) is not None}
            if p.get("name") is not None:
                attrs["ten"] = p["name"]
            ents[nid] = Ent(
                nid, str(n["label"]), str(p.get("unit_id")), tuple(sorted(attrs.items()))
            )
            for e in idx.in_edges.get(nid, []):
                if e.type in ("BI_XU_PHAT", "BI_TRU_DIEM") and edge_in_effect(e, as_of):
                    rels.add(Rel(e.type, unit_of_version_id(e.src), nid))
        for e in idx.out_edges.get(vid, []):
            if not edge_in_effect(e, as_of):
                continue
            unit = unit_of_version_id(vid)
            dst = idx.nodes.get(e.dst)
            if dst is None:
                continue
            if e.type == "QUY_DINH_HANH_VI":
                rels.add(Rel(e.type, unit, e.dst))
            elif e.type in ("AP_DUNG_CHO", "DINH_NGHIA"):
                eid = f"{e.dst}|{vid}"
                attrs = (
                    {"catalog_id": e.dst}
                    if e.type == "AP_DUNG_CHO"
                    else {"ten": (dst.get("props") or {}).get("name")}
                )
                ents[eid] = Ent(eid, str(dst["label"]), unit, tuple(sorted(attrs.items())))
                rels.add(Rel(e.type, unit, eid))
    return sorted(ents.values(), key=lambda x: x.id), sorted(
        rels, key=lambda r: (r.type, r.src_unit, r.dst)
    )


# --------------------------------------------------------------------------- tổng hợp


def aggregate(scores: Sequence[RecordScore]) -> dict[str, Any]:
    def tot(kind: str, pick: Any = None) -> dict[str, Any]:
        c = Counts()
        for s in scores:
            if pick is None or pick(s):
                c.add(s.total(kind))
        return c.prf()

    def by_type(kind: str) -> dict[str, Any]:
        acc: dict[str, Counts] = {}
        for s in scores:
            for t, c in (s.ent if kind == "entity" else s.rel).items():
                acc.setdefault(t, Counts()).add(c)
        return {t: acc[t].prf() for t in sorted(acc)}

    tiers = sorted({s.tier for s in scores})
    strata = sorted({s.stratum for s in scores})
    return {
        "overall": {"entity": tot("entity"), "relation": tot("relation")},
        "by_type": {"entity": by_type("entity"), "relation": by_type("relation")},
        "by_tier": {
            t: {
                "entity": tot("entity", lambda s, t=t: s.tier == t),
                "relation": tot("relation", lambda s, t=t: s.tier == t),
            }
            for t in tiers
        },
        "by_stratum": {
            t: {
                "entity": tot("entity", lambda s, t=t: s.stratum == t),
                "relation": tot("relation", lambda s, t=t: s.stratum == t),
            }
            for t in strata
        },
    }


def bootstrap_ci(
    scores: Sequence[RecordScore], kind: str, *, n: int = 1000, seed: int = 42
) -> tuple[float, float] | None:
    """CI 95% (phân vị 2,5/97,5) của micro-F1, lấy mẫu lại bản ghi có hoàn lại."""
    if not scores:
        return None
    rng = random.Random(seed)
    vals = []
    totals = [s.total(kind) for s in scores]
    for _ in range(n):
        c = Counts()
        for _ in range(len(totals)):
            c.add(totals[rng.randrange(len(totals))])
        f = c.prf()["f1"]
        vals.append(0.0 if f is None else float(f))
    vals.sort()
    return vals[int(0.025 * (n - 1))], vals[int(0.975 * (n - 1))]


# --------------------------------------------------------------------------- tỷ lệ sửa nháp

_CMP_FIELDS = (
    "ten",
    "span",
    "dieu_kien",
    "catalog_id",
    "loai",
    *NUM_FIELDS,
    "doi_tuong",
    "so_diem",
)


def edit_stats(
    draft: Mapping[str, Any], final: Mapping[str, Any], span_f1: float
) -> dict[str, int]:
    """So bản nháp LLM với bản người sửa: thực thể thêm/xoá/đổi (ghép được nhưng khác trường),
    quan hệ thêm/xoá."""
    de, dr = gold_entities(draft)
    fe, fr = gold_entities(final)
    m = align(fe, de, span_f1)
    fmap = {e.id: e for e in fe}
    changed = sum(
        1 for d in de if d.id in m and any(d.get(k) != fmap[m[d.id]].get(k) for k in _CMP_FIELDS)
    )
    dset = {(r.type, r.src_unit, m.get(r.dst, "∅" + r.dst)) for r in dr}
    fset = {(r.type, r.src_unit, r.dst) for r in fr}
    return {
        "draft_entities": len(de),
        "final_entities": len(fe),
        "entities_removed": len(de) - len(m),
        "entities_added": len(fe) - len(m),
        "entities_changed": changed,
        "draft_relations": len(dr),
        "final_relations": len(fr),
        "relations_removed": len(dset - fset),
        "relations_added": len(fset - dset),
    }


__all__ = [
    "Counts",
    "Ent",
    "PredIndex",
    "RecordScore",
    "Rel",
    "aggregate",
    "align",
    "bootstrap_ci",
    "edit_stats",
    "gold_entities",
    "match_score",
    "pred_for_record",
    "score_record",
    "token_f1",
]
