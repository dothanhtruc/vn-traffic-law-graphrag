"""Tập vàng trích xuất (M8): schema, lấy mẫu phân tầng, hậu kiểm bản nháp LLM, validator.

Quy trình (quyết định người dùng 09/11/2026):

1. ``sample``: ~60 Khoản phân tầng, seed 42, tất định → ``gold_extraction_sample.jsonl``.
2. ``preannotate``: model tự host KHÁC HỌ với model trích xuất gán nháp →
   ``gold_extraction.jsonl`` với
   ``annotator: "llm:<model_id>"``, ``reviewed: false`` và bản sao ``draft`` (để đo tỷ lệ sửa).
   Con số trong nháp phải khớp regex trên text unit, span phải nguyên văn, id danh mục phải hợp
   lệ — sai thì bỏ, ghi vào ``draft_dropped``.
3. Người dùng sửa ``entities``/``relations`` rồi đặt ``reviewed: true``. Claude không sửa nhãn
   vàng và không đặt ``reviewed``.
"""

from __future__ import annotations

import random
import re
from collections.abc import Mapping, Sequence
from datetime import date
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from trafficlaw.graph.extract import (
    Catalog,
    ExtractConfig,
    build_scope,
    find_clauses,
    find_verbatim,
    nfc,
    norm_ws,
    verify_numeric_entity,
)
from trafficlaw.graph.store import BaseGraphStore

EntityType = Literal[
    "HanhVi", "CheTai", "DiemGPLX", "BienPhapBoSung", "KhaiNiem", "PhuongTien", "ChuThe"
]
RelType = Literal["QUY_DINH_HANH_VI", "AP_DUNG_CHO", "BI_XU_PHAT", "BI_TRU_DIEM", "DINH_NGHIA"]

#: Loại thực thể hợp lệ ở đầu ``dst`` của từng loại quan hệ (``src`` luôn là ``unit:<id>``).
REL_DST: dict[str, tuple[str, ...]] = {
    "QUY_DINH_HANH_VI": ("HanhVi",),
    "AP_DUNG_CHO": ("PhuongTien", "ChuThe"),
    "DINH_NGHIA": ("KhaiNiem",),
    "BI_XU_PHAT": ("CheTai", "BienPhapBoSung"),
    "BI_TRU_DIEM": ("DiemGPLX",),
}
SANCTION_LOAI = ("phat_tien", "canh_cao", "tuoc_quyen", "tich_thu", "dinh_chi")


class GoldEntity(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    type: EntityType
    unit_id: str
    ten: str | None = None
    span: str | None = None
    dieu_kien: str | None = None
    catalog_id: str | None = None
    loai: Literal["phat_tien", "canh_cao", "tuoc_quyen", "tich_thu", "dinh_chi"] | None = None
    min_vnd: int | None = None
    max_vnd: int | None = None
    min_thang: int | None = None
    max_thang: int | None = None
    doi_tuong: str | None = None
    so_diem: int | None = None


class GoldRelation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: RelType
    src: str
    dst: str


class GoldUnit(BaseModel):
    model_config = ConfigDict(extra="forbid")
    unit_id: str
    version_id: str


class GoldDraft(BaseModel):
    model_config = ConfigDict(extra="forbid")
    entities: list[GoldEntity] = []
    relations: list[GoldRelation] = []


class GoldRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")
    gold_id: str
    unit_id: str
    doc_id: str
    tier: str
    stratum: str
    as_of: date
    dieu_title: str
    units: list[GoldUnit]
    text: str
    entities: list[GoldEntity] = []
    relations: list[GoldRelation] = []
    annotator: str
    reviewed: bool = False
    reviewer: str | None = None
    draft: GoldDraft | None = None
    draft_dropped: list[dict[str, Any]] = []
    draft_status: str | None = None
    notes: str | None = None


class SampleRow(BaseModel):
    model_config = ConfigDict(extra="forbid")
    gold_id: str
    unit_id: str
    doc_id: str
    tier: str
    stratum: str
    as_of: date


# --------------------------------------------------------------------------- lấy mẫu

_SANC_RE = re.compile(r"[Pp]hạt tiền|[Pp]hạt cảnh cáo")


def subtree_versions(store: BaseGraphStore, unit_id: str, as_of: date) -> list[tuple[str, Any]]:
    """(unit_id, PhienBan) theo thứ tự văn bản cho cây con hiệu lực tại ``as_of``."""
    out = []
    for u in store.subtree(unit_id, as_of=as_of):
        v = store.version_at(u, as_of)
        if v is not None:
            out.append((u, v))
    return out


def render_text(pairs: Sequence[tuple[str, Any]]) -> str:
    return "\n".join(f"[{u}] {norm_ws(str(v.props.get('text') or ''))}" for u, v in pairs)


def _candidates(
    store: BaseGraphStore, cfg: ExtractConfig, as_of: date, max_units: int
) -> list[dict[str, Any]]:
    scope = build_scope(store, cfg)
    loai = {n.id: n.props.get("loai") for n in store.nodes_by_label("VanBan")}
    hint = re.compile(cfg.selective_hint)
    dhint = re.compile(cfg.definition_hint)
    out = []
    for d in scope.dieus:
        doc = str(d.props["doc_id"])
        for k in store.children(d.id, as_of=as_of):
            if not k.rsplit("/", 1)[-1].startswith("K"):
                continue
            pairs = subtree_versions(store, k, as_of)
            if not pairs or len(pairs) > max_units:
                continue
            texts = [nfc(str(v.props.get("text") or "")) for _, v in pairs]
            joined = "\n".join(texts)
            out.append(
                {
                    "unit_id": k,
                    "doc_id": doc,
                    "tier": scope.docs[doc],
                    "loai": loai.get(doc),
                    "sanction_dieu": d.id in scope.sanction_dieus,
                    "definition_dieu": d.id in scope.definition_dieus,
                    "has_fine": bool(_SANC_RE.search(joined)),
                    "has_clause": any(find_clauses(t) for t in texts),
                    "hint": bool(hint.search(joined))
                    or any(dhint.search(x) for x in joined.split("\n")),
                }
            )
    return out


STRATA: dict[str, Any] = {
    "nd168_che_tai": lambda c: (
        c["doc_id"] == "ND168-2024" and c["sanction_dieu"] and c["has_fine"] and not c["has_clause"]
    ),
    "nd168_bo_sung_tru_diem": lambda c: (
        c["doc_id"] == "ND168-2024" and c["sanction_dieu"] and c["has_clause"]
    ),
    "dinh_nghia_luat": lambda c: (
        c["doc_id"] in ("LUAT36-2024", "LUAT35-2024") and c["definition_dieu"]
    ),
    "nd336": lambda c: c["doc_id"] == "ND336-2025" and c["sanction_dieu"],
    "tt_tier_a": lambda c: c["tier"] == "A" and c["loai"] == "thong_tu",
    "tier_b": lambda c: c["tier"] == "B" and (c["hint"] or c["definition_dieu"]),
}


def sample_gold(
    store: BaseGraphStore,
    cfg: ExtractConfig,
    strata: Mapping[str, int],
    *,
    as_of: date,
    seed: int = 42,
    max_units: int = 12,
) -> list[SampleRow]:
    """Mỗi tầng: ứng viên sắp theo mã, ``Random(seed).sample``; không trùng giữa các tầng
    (tầng khai báo trước được ưu tiên)."""
    cands = _candidates(store, cfg, as_of, max_units)
    taken: set[str] = set()
    out: list[SampleRow] = []
    for name, n in strata.items():
        if name not in STRATA:
            raise KeyError(f"tầng không xác định: {name}")
        pool = sorted(
            (c for c in cands if STRATA[name](c) and c["unit_id"] not in taken),
            key=lambda c: c["unit_id"],
        )
        rng = random.Random(f"{seed}:{name}")
        pick = rng.sample(pool, min(n, len(pool)))
        for c in sorted(pick, key=lambda c: c["unit_id"]):
            taken.add(c["unit_id"])
            out.append(
                SampleRow(
                    gold_id=f"{c['unit_id']}@{as_of.isoformat()}",
                    unit_id=c["unit_id"],
                    doc_id=c["doc_id"],
                    tier=c["tier"],
                    stratum=name,
                    as_of=as_of,
                )
            )
    return out


# --------------------------------------------------------------------------- bản nháp LLM


class DraftEntityOut(BaseModel):
    """Đầu ra của model gán nháp (lỏng hơn ``GoldEntity`` — hậu kiểm làm ở ``clean_draft``)."""

    model_config = ConfigDict(extra="ignore")
    id: str
    type: str
    unit_id: str
    ten: str | None = None
    span: str | None = None
    dieu_kien: str | None = None
    catalog_id: str | None = None
    loai: str | None = None
    min_vnd: int | None = None
    max_vnd: int | None = None
    min_thang: int | None = None
    max_thang: int | None = None
    doi_tuong: str | None = None
    so_diem: int | None = None


class DraftRelationOut(BaseModel):
    model_config = ConfigDict(extra="ignore")
    type: str
    src: str
    dst: str


class DraftOut(BaseModel):
    entities: list[DraftEntityOut] = Field(default_factory=list)
    relations: list[DraftRelationOut] = Field(default_factory=list)


def clean_draft(
    parsed: Mapping[str, Any],
    unit_texts: Mapping[str, str],
    catalog: Catalog,
    known_unit: Any,
) -> tuple[GoldDraft, list[dict[str, Any]]]:
    """Hậu kiểm bản nháp: trả về (bản nháp hợp lệ, danh sách mục bị bỏ kèm lý do).

    ``unit_texts``: unit trong Khoản → text tại ``as_of``; ``known_unit(id) -> bool``: unit tồn
    tại và có phiên bản hiệu lực (cho ``src`` của BI_XU_PHAT/BI_TRU_DIEM ở Khoản khác).
    """
    dropped: list[dict[str, Any]] = []
    ents: list[GoldEntity] = []
    valid_cat = {
        "PhuongTien": set(catalog.ids("phuong_tien")),
        "ChuThe": set(catalog.ids("chu_the")),
    }
    seen_ids: set[str] = set()

    def drop(kind: str, obj: Any, reason: str) -> None:
        dropped.append({"kind": kind, "value": obj, "reason": reason})

    for raw in parsed.get("entities") or []:
        try:
            e = DraftEntityOut.model_validate(raw)
        except Exception:  # noqa: BLE001 — nháp hỏng một mục thì bỏ mục đó
            drop("entity", raw, "sai_schema")
            continue
        d = e.model_dump()
        if (
            e.type
            not in REL_DST["QUY_DINH_HANH_VI"]
            + REL_DST["AP_DUNG_CHO"]
            + REL_DST["DINH_NGHIA"]
            + REL_DST["BI_XU_PHAT"]
            + REL_DST["BI_TRU_DIEM"]
        ):
            drop("entity", d, "loai_khong_hop_le")
            continue
        if e.id in seen_ids:
            drop("entity", d, "trung_id")
            continue
        text = unit_texts.get(e.unit_id)
        if text is None:
            drop("entity", d, "unit_ngoai_khoan")
            continue
        if e.type == "HanhVi":
            span = find_verbatim(e.span or "", text)
            if span is None:
                drop("entity", d, "span_khong_nguyen_van")
                continue
            d["span"] = span
        if e.type in ("CheTai", "DiemGPLX"):
            if e.type == "CheTai" and e.loai not in SANCTION_LOAI:
                drop("entity", d, "loai_che_tai_khong_hop_le")
                continue
            why = verify_numeric_entity(d, text)
            if why:
                drop("entity", d, why)
                continue
        if e.type in valid_cat and e.catalog_id not in valid_cat[e.type]:
            drop("entity", d, "ngoai_danh_muc")
            continue
        seen_ids.add(e.id)
        ents.append(
            GoldEntity.model_validate({k: v for k, v in d.items() if k in GoldEntity.model_fields})
        )
    by_id = {e.id: e for e in ents}
    rels: list[GoldRelation] = []
    seen_rel: set[tuple[str, str, str]] = set()
    for raw in parsed.get("relations") or []:
        try:
            r = DraftRelationOut.model_validate(raw)
        except Exception:  # noqa: BLE001
            drop("relation", raw, "sai_schema")
            continue
        d = r.model_dump()
        if r.type not in REL_DST:
            drop("relation", d, "loai_khong_hop_le")
            continue
        dst = by_id.get(r.dst)
        if dst is None or dst.type not in REL_DST[r.type]:
            drop("relation", d, "dich_khong_hop_le")
            continue
        if not r.src.startswith("unit:") or not known_unit(r.src[5:]):
            drop("relation", d, "nguon_khong_hop_le")
            continue
        k = (r.type, r.src, r.dst)
        if k in seen_rel:
            continue
        seen_rel.add(k)
        rels.append(GoldRelation(type=r.type, src=r.src, dst=r.dst))  # type: ignore[arg-type]
    return GoldDraft(entities=ents, relations=rels), dropped


# --------------------------------------------------------------------------- validator


def validate_gold(
    records: Sequence[Mapping[str, Any]], store: BaseGraphStore, catalog: Catalog | None
) -> list[dict[str, Any]]:
    """Lỗi/cảnh báo của từng bản ghi gold: schema; unit tồn tại + có phiên bản tại ``as_of``;
    ``units`` khớp cây con hiện hành; thực thể thuộc unit của Khoản; id danh mục hợp lệ; span
    HanhVi nguyên văn; quan hệ đúng loại đích; con số khớp regex (cảnh báo)."""
    issues: list[dict[str, Any]] = []
    seen: set[str] = set()

    def add(gid: str, level: str, msg: str) -> None:
        issues.append({"gold_id": gid, "level": level, "message": msg})

    cat_ids = (
        {"PhuongTien": set(catalog.ids("phuong_tien")), "ChuThe": set(catalog.ids("chu_the"))}
        if catalog
        else None
    )
    for raw in records:
        gid = str(raw.get("gold_id", "?"))
        try:
            rec = GoldRecord.model_validate(raw)
        except Exception as e:  # noqa: BLE001
            add(gid, "error", f"sai schema: {str(e)[:300]}")
            continue
        if gid in seen:
            add(gid, "error", "trùng gold_id")
        seen.add(gid)
        if store.get_node(rec.unit_id) is None:
            add(gid, "error", f"unit không tồn tại: {rec.unit_id}")
            continue
        if store.version_at(rec.unit_id, rec.as_of) is None:
            add(gid, "error", f"{rec.unit_id} không có phiên bản hiệu lực tại {rec.as_of}")
            continue
        pairs = subtree_versions(store, rec.unit_id, rec.as_of)
        cur = {u: v for u, v in pairs}
        if [(u.unit_id, u.version_id) for u in rec.units] != [(u, v.id) for u, v in pairs]:
            add(gid, "error", "units lệch cây con hiện hành (dữ liệu đã đổi → lấy mẫu lại)")
        texts = {u: str(v.props.get("text") or "") for u, v in cur.items()}
        ids: set[str] = set()
        types: dict[str, str] = {}
        for e in rec.entities:
            if e.id in ids:
                add(gid, "error", f"trùng id thực thể {e.id}")
            ids.add(e.id)
            types[e.id] = e.type
            if e.unit_id not in cur:
                add(gid, "error", f"{e.id}: unit {e.unit_id} không thuộc Khoản tại {rec.as_of}")
                continue
            if e.type == "HanhVi" and find_verbatim(e.span or "", texts[e.unit_id]) is None:
                add(gid, "error", f"{e.id}: span HanhVi không nguyên văn")
            if e.type in ("PhuongTien", "ChuThe"):
                if not e.catalog_id:
                    add(gid, "error", f"{e.id}: thiếu catalog_id")
                elif cat_ids is not None and e.catalog_id not in cat_ids[e.type]:
                    add(gid, "error", f"{e.id}: catalog_id ngoài danh mục: {e.catalog_id}")
            if e.type == "CheTai" and e.loai is None:
                add(gid, "error", f"{e.id}: CheTai thiếu loai")
            if e.type == "DiemGPLX" and e.so_diem is None:
                add(gid, "error", f"{e.id}: DiemGPLX thiếu so_diem")
            if e.type in ("CheTai", "DiemGPLX") and verify_numeric_entity(
                e.model_dump(), texts[e.unit_id]
            ):
                add(gid, "warning", f"{e.id}: con số không khớp regex trên text unit")
        for r in rec.relations:
            if r.dst not in types:
                add(gid, "error", f"quan hệ {r.type}: dst {r.dst} không phải thực thể của bản ghi")
            elif types[r.dst] not in REL_DST[r.type]:
                add(gid, "error", f"quan hệ {r.type}: dst {r.dst} là {types[r.dst]}")
            if not r.src.startswith("unit:"):
                add(gid, "error", f"quan hệ {r.type}: src phải là unit:<id>")
            elif store.version_at(r.src[5:], rec.as_of) is None:
                add(gid, "error", f"quan hệ {r.type}: {r.src} không có phiên bản tại {rec.as_of}")
    return issues


__all__ = [
    "REL_DST",
    "STRATA",
    "DraftOut",
    "GoldDraft",
    "GoldEntity",
    "GoldRecord",
    "GoldRelation",
    "GoldUnit",
    "SampleRow",
    "clean_draft",
    "render_text",
    "sample_gold",
    "subtree_versions",
    "validate_gold",
]
