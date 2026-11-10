"""Danh mục đóng PhuongTien / ChuThe cho trích xuất (M8), dựng bằng rule từ văn bản luật.

- **PhuongTien**: (1) danh sách phân loại ("1. Xe cơ giới bao gồm:" + các Điểm) trong các Điều
  ``pt_list_dieu`` (LUAT36 Điều 34); (2) định nghĩa ``N. Xe … là/gồm/bao gồm …`` trong
  ``pt_def_docs`` (LUAT36, LUAT35); (3) ``pt_extra`` (vd "xe tương tự xe ô tô") — chỉ nhận khi cụm
  có nguyên văn trong một unit (ghi ``evidence``). Alias chỉ từ "(sau đây gọi là …)"; "gồm cả X"
  → ``bao_gom`` (không gộp thành alias). "Xe gắn máy" và "xe mô tô" là hai mục riêng.
- **ChuThe**: định nghĩa "N. Người … là …" trong ``pt_def_docs`` + ``ct_seed`` (cụm do người dùng
  duyệt), mỗi cụm phải có nguyên văn trong văn bản thuộc phạm vi.

Kết quả là bản nháp ``approved: false``; người dùng duyệt rồi đặt ``approved: true`` trước khi
chạy trích xuất thật.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from typing import Any

from pydantic import BaseModel, ConfigDict

from trafficlaw.graph.extract import Catalog, CatalogEntry, active_versions, nfc, norm_ws, slugify
from trafficlaw.graph.store import BaseGraphStore


class ExtraEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    nhom: str | None = None
    can_cu: str | None = None


class CatalogConfig(BaseModel):
    model_config = ConfigDict(extra="ignore")
    pt_list_dieu: list[str] = ["LUAT36-2024/D34"]
    pt_def_docs: list[str] = ["LUAT36-2024", "LUAT35-2024"]
    pt_extra: list[ExtraEntry] = []
    ct_seed: list[str] = []
    evidence_docs: list[str] = []
    """Văn bản tìm nguyên văn cho ``pt_extra``/``ct_seed`` (rỗng = mọi văn bản đọc được)."""


_LIST_HEAD_RE = re.compile(r"^\d+\.\s*(?P<name>[^:]{2,80}?) bao gồm:\s*$")
_LIST_ITEM_RE = re.compile(
    r"^[a-zđ]\d*\)\s*(?P<name>[^;:.()]{2,120}?)(?:,\s*gồm cả (?P<incl>[^,;]+?),)?"
    r"\s*(?:(?:là|gồm|bao gồm)(?=[\s:])|;|\.|$)"
)
_PT_DEF_RE = re.compile(
    r"^(?:\d+[a-z]?\.|[a-zđ]\))\s*(?P<name>(?:Xe|Phương tiện|Rơ moóc|Sơ mi rơ moóc|Máy kéo)"
    r"[^,.;:()]{0,80}?)\s*(?:\((?:sau đây )?gọi(?: tắt)? là (?P<alias>[^)]+)\)\s*)?"
    r"(?:là|gồm|bao gồm)(?=[\s:])"
)
_CT_DEF_RE = re.compile(
    r"^\d+[a-z]?\.\s*(?P<name>Người [^,.;:()]{2,80}?)\s*"
    r"(?:\((?:sau đây )?gọi(?: tắt)? là (?P<alias>[^)]+)\)\s*)?(?:là|bao gồm|gồm)(?=[\s:])"
)
_INNER_ALIAS_RE = re.compile(r"\(sau đây gọi(?: tắt)? là ([^)]+)\)")


def _lc(s: str) -> str:
    s = norm_ws(s)
    return s[:1].lower() + s[1:] if s else s


def _cur_text(store: BaseGraphStore, unit_id: str) -> str:
    vs = active_versions(store, unit_id)
    return nfc(str(vs[-1].props.get("text") or "")) if vs else ""


def _units_of(store: BaseGraphStore, docs: Sequence[str]) -> list[str]:
    out: list[str] = []
    for doc in docs:
        out += [u for u in store.subtree(doc) if u != doc]
    return out


def _add(
    out: dict[str, CatalogEntry],
    prefix: str,
    name: str,
    *,
    nhom: str | None = None,
    can_cu: str | None = None,
    aliases: Sequence[str] = (),
    bao_gom: Sequence[str] = (),
    evidence: str | None = None,
    lower: bool = True,
) -> None:
    """``lower``: viết thường chữ đầu (tên lấy từ đầu câu định nghĩa); tên do người dùng nhập
    (``pt_extra``/``ct_seed``) giữ nguyên (vd "Bộ Công an")."""
    name = _lc(name) if lower else norm_ws(name)
    eid = f"{prefix}:{slugify(name)}"
    if eid in out:
        e = out[eid]
        e.aliases = sorted(set(e.aliases) | {_lc(a) for a in aliases})
        return
    out[eid] = CatalogEntry(
        id=eid,
        name=name,
        nhom=nhom,
        can_cu=can_cu,
        aliases=sorted({_lc(a) for a in aliases if _lc(a) != name}),
        bao_gom=sorted({_lc(b) for b in bao_gom}),
        evidence=evidence[:240] if evidence else None,
    )


def _find_evidence(phrase: str, texts: dict[str, str]) -> tuple[str, str] | None:
    pat = re.compile(r"(?<!\w)" + r"\s+".join(map(re.escape, phrase.split())) + r"(?!\w)", re.I)
    for u in sorted(texts):
        m = pat.search(texts[u])
        if m:
            s = max(0, m.start() - 60)
            return u, norm_ws(texts[u][s : m.end() + 60])
    return None


def build_catalog(store: BaseGraphStore, cfg: CatalogConfig) -> Catalog:
    pt: dict[str, CatalogEntry] = {}
    ct: dict[str, CatalogEntry] = {}
    # (1) danh sách phân loại
    for dieu in cfg.pt_list_dieu:
        for k in store.children(dieu):
            head = _LIST_HEAD_RE.match(_cur_text(store, k).split("\n", 1)[0])
            if not head:
                continue
            group = _lc(head["name"])
            _add(pt, "PT", group, can_cu=k, evidence=_cur_text(store, k))
            for d in store.children(k):
                txt = _cur_text(store, d)
                m = _LIST_ITEM_RE.match(txt)
                if not m or "quy định tại" in txt.split(";")[0] or "tương tự" in m["name"]:
                    continue
                incl = [m["incl"]] if m["incl"] else []
                _add(pt, "PT", m["name"], nhom=slugify(group), can_cu=d, bao_gom=incl, evidence=txt)
    # (2) định nghĩa trong luật
    texts = {u: _cur_text(store, u) for u in _units_of(store, cfg.pt_def_docs)}
    for u in sorted(texts):
        first = texts[u].split("\n", 1)[0]
        for rx, out, prefix in ((_PT_DEF_RE, pt, "PT"), (_CT_DEF_RE, ct, "CT")):
            m = rx.match(first)
            if not m:
                continue
            aliases = [a for a in re.split(r",| hoặc ", m["alias"] or "") if a.strip()]
            _add(out, prefix, m["name"], can_cu=u, aliases=aliases, evidence=first)
        # alias khai báo giữa câu: "… phương tiện giao thông cơ giới đường bộ (sau đây gọi là
        # xe cơ giới) …" → gắn vào mục đã có tên đó (không tạo mục mới).
        for m in _INNER_ALIAS_RE.finditer(first):
            alias = _lc(m.group(1))
            eid = f"PT:{slugify(alias)}"
            before = first[: m.start()].rsplit(",", 1)[-1].rsplit(":", 1)[-1]
            full = _lc(before)
            if eid in pt and full and full != alias:
                pt[eid].aliases = sorted(set(pt[eid].aliases) | {full})
    # (3) mục bổ sung + chủ thể: phải có nguyên văn
    ev_texts = (
        {u: _cur_text(store, u) for u in _units_of(store, cfg.evidence_docs)}
        if cfg.evidence_docs
        else texts
    )
    for x in cfg.pt_extra:
        ev = _find_evidence(x.name, ev_texts)
        if ev is None:
            continue
        _add(
            pt,
            "PT",
            x.name,
            nhom=x.nhom,
            can_cu=x.can_cu or ev[0],
            evidence=f"{ev[0]}: {ev[1]}",
            lower=False,
        )
    for name in cfg.ct_seed:
        ev = _find_evidence(name, ev_texts)
        if ev is None:
            continue
        _add(ct, "CT", name, can_cu=None, evidence=f"{ev[0]}: {ev[1]}", lower=False)
    return Catalog(
        approved=False,
        phuong_tien=[pt[k] for k in sorted(pt)],
        chu_the=[ct[k] for k in sorted(ct)],
    )


def catalog_to_yaml_dict(cat: Catalog) -> dict[str, Any]:
    return cat.model_dump(mode="json")


__all__ = ["CatalogConfig", "ExtraEntry", "build_catalog", "catalog_to_yaml_dict"]
