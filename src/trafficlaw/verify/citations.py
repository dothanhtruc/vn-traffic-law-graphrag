"""Kiểm trích dẫn của câu trả lời (M12).

Câu trả lời RAG trích nguồn bằng mã ``S#`` (nguồn đã đưa vào ngữ cảnh), tuỳ chọn kèm nhãn
Điểm/Khoản bên trong chunk: ``S2``, ``S2/a``, ``S2/K3/a`` (chunk là Điều không chia Khoản).
:func:`resolve_citation` ánh xạ về ``unit_id``:

- ``S#`` không có trong ngữ cảnh → ``nguon_ngoai_ngu_canh`` (bỏ trích dẫn);
- nhãn không phải unit trong cây con của unit chunk → ``diem_khong_ton_tai`` (bỏ);
- nhãn trùng chính unit của chunk (``S2/K3`` khi S2 là khoản 3) → cả nguồn;
- nhãn (tương đối với Điều của chunk) là unit nêu một chế tài trong bảng con số của nguồn
  (``S2/K16/a`` — mức trừ điểm nêu tại khoản 16, nối bằng BI_TRU_DIEM) → ``ok_bang_so`` (hợp lệ:
  dữ liệu đồ thị đã kiểm, LLM đã thấy trong bảng);
- unit không có phiên bản hiệu lực tại ``as_of`` → ``het_hieu_luc`` (bỏ); cấu hình không lọc
  hiệu lực (A2) → giữ, ghi ``het_hieu_luc_khong_loc``.

Câu trả lời B0 (không RAG) tự khai trích dẫn có cấu trúc ``{van_ban, dieu, khoan, diem}``;
:func:`resolve_free_citation` chỉ đối chiếu với đồ thị để thống kê "trích dẫn bịa"
(``van_ban_khong_ro`` / ``khong_ton_tai`` / ``het_hieu_luc``).

Hàm thuần, đọc đồ thị qua ``GraphStore``.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from trafficlaw.graph.doc_names import norm_so_hieu
from trafficlaw.graph.store import BaseGraphStore

CitationStatus = Literal[
    "ok",
    "ok_bang_so",
    "het_hieu_luc_khong_loc",
    "sai_dinh_dang",
    "nguon_ngoai_ngu_canh",
    "diem_khong_ton_tai",
    "het_hieu_luc",
    "van_ban_khong_ro",
    "khong_ton_tai",
]
VALID_STATUSES = ("ok", "ok_bang_so", "het_hieu_luc_khong_loc")


class Citation(BaseModel):
    """Một trích dẫn đã kiểm."""

    model_config = ConfigDict(extra="forbid")
    ref: str
    """Chuỗi LLM viết (``S2/a``) hoặc dạng chuẩn của trích dẫn tự khai (B0)."""
    status: CitationStatus
    sid: str | None = None
    unit_id: str | None = None
    chunk_id: str | None = None
    label: str | None = None
    """Nhãn đọc được: ``điểm a khoản 4 Điều 6 Nghị định 168/2024/NĐ-CP``."""

    @property
    def valid(self) -> bool:
        return self.status in VALID_STATUSES


@dataclass(frozen=True)
class CitableSource:
    """Phần của nguồn mà kiểm trích dẫn cần. ``fact_units``: unit nêu chế tài trong bảng con số
    của nguồn này (nối qua BI_XU_PHAT/BI_TRU_DIEM, có thể nằm ngoài chunk — vd khoản 16 trừ
    điểm)."""

    sid: str
    chunk_id: str
    unit_id: str
    doc_label: str
    fact_units: frozenset[str] = frozenset()


# --------------------------------------------------------------------------- nhãn đọc được

_LOAI = {
    "luat": "Luật",
    "nghi_dinh": "Nghị định",
    "thong_tu": "Thông tư",
    "quyet_dinh": "Quyết định",
}


def doc_label(props: Mapping[str, object]) -> str:
    """``Nghị định 168/2024/NĐ-CP`` / ``Luật Đường bộ (35/2024/QH15)``."""
    so = str(props.get("so_hieu") or props.get("doc_id") or "")
    loai = str(props.get("loai") or "")
    if loai == "luat":
        ten = str(props.get("ten") or "Luật")
        return f"{ten} ({so})" if so else ten
    head = _LOAI.get(loai, "Văn bản")
    return f"{head} {so}".strip()


def unit_label(unit_id: str) -> str:
    """``ND168-2024/D6/K4/a`` → ``điểm a khoản 4 Điều 6``; ``…/PL1-2`` → ``Phụ lục 1 (phần 2)``."""
    parts = unit_id.split("/")[1:]
    out: list[str] = []
    for p in parts:
        if p.startswith("PL"):
            num, _, k = p[2:].partition("-")
            out.append(f"Phụ lục {num}" + (f" (phần {k})" if k else ""))
        elif re.fullmatch(r"D\d+[a-z]?", p):
            out.append(f"Điều {p[1:]}")
        elif re.fullmatch(r"K\d+[a-z]?", p):
            out.append(f"khoản {p[1:]}")
        elif re.fullmatch(r"[PCM]\d+", p):
            out.append({"P": "Phần", "C": "Chương", "M": "Mục"}[p[0]] + f" {p[1:]}")
        else:
            out.append(f"điểm {p}")
    return " ".join(reversed(out))


def full_label(unit_id: str, doc: str) -> str:
    u = unit_label(unit_id)
    return f"{u} {doc}".strip()


# --------------------------------------------------------------------------- RAG: S#

_REF_RE = re.compile(r"^\[?\s*(S\d+)\s*(?:/\s*([^\]]+?))?\s*\]?$")


def _label_to_suffix(label: str) -> str:
    """``a`` / ``K3`` / ``K3/a`` / ``khoản 3 điểm a`` → ``a`` / ``K3`` / ``K3/a``."""
    s = label.strip().strip("/").replace(" ", "")
    s = re.sub(r"(?i)^khoản(\d+[a-z]?)", r"K\1/", s)
    s = re.sub(r"(?i)điểm([a-zđ]\d*)", r"\1", s)
    s = re.sub(r"(?i)^k(\d)", r"K\1", s)
    return s.strip("/")


def label_candidates(base: str, label: str) -> list[str]:
    """Các ``unit_id`` mà nhãn có thể chỉ tới, tương đối với unit của chunk ``base``.

    Dạng LLM hay viết (quan sát trên val): ``a``, ``K3/a``, ``3/a`` (số trần = khoản), ``4``
    (chính khoản của chunk), ``K22/5`` hay ``D22/K5`` (số đầu trùng số Điều của chunk = Điều)."""
    suf = _label_to_suffix(label)
    parts = base.split("/")
    di = next((i for i, x in enumerate(parts) if re.fullmatch(r"D\d+[a-z]?", x)), None)
    cands = [f"{base}/{suf}"]
    if len(parts) >= 3 and suf.startswith(parts[-1] + "/"):
        cands.append(f"{base}/{suf[len(parts[-1]) + 1 :]}")
    if suf == parts[-1]:
        cands.append(base)
    if di is not None:
        dieu = parts[di]
        toks = [t for t in re.split(r"/", suf) if t]
        # bỏ tiền tố Điều: "D22", "Điều22", hoặc "K22" khi 22 là số Điều của chunk
        if toks and (
            re.fullmatch(rf"(?i)(?:D|Điều){dieu[1:]}", toks[0])
            or (len(toks) > 1 and re.fullmatch(rf"K{dieu[1:]}", toks[0]))
        ):
            toks = toks[1:]
        rel: list[str] = []
        for t in toks:
            if re.fullmatch(r"(?:K|khoản)?\d+[a-z]?", t, re.I) and not rel:
                rel.append("K" + re.sub(r"(?i)^(?:K|khoản)", "", t))
            elif re.fullmatch(r"[a-zđ]\d*", t):
                rel.append(t)
            else:
                rel = []
                break
        if rel and rel[0].startswith("K"):
            cands.append("/".join([*parts[: di + 1], *rel]))
    return list(dict.fromkeys(cands))


def resolve_citation(
    ref: str,
    sources: Mapping[str, CitableSource],
    store: BaseGraphStore,
    as_of: date,
    *,
    validity_filter: bool = True,
) -> Citation:
    m = _REF_RE.match(ref.strip())
    if not m:
        return Citation(ref=ref, status="sai_dinh_dang")
    sid, label = m.group(1), m.group(2)
    src = sources.get(sid)
    if src is None:
        return Citation(ref=ref, status="nguon_ngoai_ngu_canh", sid=sid)
    base = src.unit_id
    unit = base
    status: CitationStatus = "ok"
    if label:
        cands = label_candidates(base, label)
        sub = set(store.subtree(base, as_of=as_of if validity_filter else None))
        sub.add(base)
        hit = next((c for c in cands if c in sub), None)
        if hit is None and src.fact_units:
            hit = next((c for c in cands if c in src.fact_units), None)
            if hit is not None:
                status = "ok_bang_so"
        if hit is None:
            return Citation(
                ref=ref,
                status="diem_khong_ton_tai",
                sid=sid,
                chunk_id=src.chunk_id,
                unit_id=cands[0],
            )
        unit = hit
    lab = full_label(unit, src.doc_label)
    if store.version_at(unit, as_of) is None:
        return Citation(
            ref=ref,
            status="het_hieu_luc_khong_loc" if not validity_filter else "het_hieu_luc",
            sid=sid,
            unit_id=unit,
            chunk_id=src.chunk_id,
            label=lab,
        )
    return Citation(ref=ref, status=status, sid=sid, unit_id=unit, chunk_id=src.chunk_id, label=lab)


# --------------------------------------------------------------------------- B0: tự khai


class FreeCitationIn(BaseModel):
    """Trích dẫn B0 tự khai (schema gửi LLM)."""

    model_config = ConfigDict(extra="forbid")
    van_ban: str = Field(pattern=r"^[0-9]+[a-z]?/([0-9]{4}/)?[A-Za-zĐđ0-9-]+$")
    """Số hiệu văn bản, vd ``168/2024/NĐ-CP`` (mẫu ép qua guided decoding của vLLM)."""
    dieu: str = Field(pattern=r"^[0-9]+[a-z]?$")
    khoan: str | None = Field(default=None, pattern=r"^[0-9]+[a-z]?$")
    diem: str | None = Field(default=None, pattern=r"^[a-zđ][0-9]?$")


_SO_HIEU_IN_RE = re.compile(r"\d+[a-z]?/\d{4}/[A-ZĐa-zđ0-9\-]+|\d+/[A-ZĐ][A-ZĐ0-9\-]+")


class SoHieuTable:
    """``số hiệu chuẩn hoá`` → ``doc_id`` cho các VanBan trong đồ thị."""

    def __init__(self, store: BaseGraphStore) -> None:
        self.by_so: dict[str, str] = {}
        self.label: dict[str, str] = {}
        for n in store.nodes_by_label("VanBan"):
            so = n.props.get("so_hieu")
            if so:
                self.by_so[norm_so_hieu(str(so))] = n.id
            self.label[n.id] = doc_label(n.props)

    def find(self, text: str) -> str | None:
        m = _SO_HIEU_IN_RE.search(text.replace(" ", ""))
        return self.by_so.get(norm_so_hieu(m.group(0))) if m else None


def _clean_num(s: str | None) -> str | None:
    if s is None:
        return None
    s = re.sub(r"(?i)^(điều|khoản|điểm)\s*", "", s.strip())
    return s.strip().lower() or None


def resolve_free_citation(
    c: FreeCitationIn, table: SoHieuTable, store: BaseGraphStore, as_of: date
) -> Citation:
    dieu, khoan, diem = _clean_num(c.dieu), _clean_num(c.khoan), _clean_num(c.diem)
    ref = ", ".join(
        x
        for x in (
            f"điểm {diem}" if diem else "",
            f"khoản {khoan}" if khoan else "",
            f"Điều {dieu}",
            c.van_ban,
        )
        if x
    )
    doc = table.find(c.van_ban)
    if doc is None or not dieu:
        return Citation(ref=ref, status="van_ban_khong_ro")
    unit = f"{doc}/D{dieu}" + (f"/K{khoan}" if khoan else "") + (f"/{diem}" if diem else "")
    if store.get_node(unit) is None:
        return Citation(ref=ref, status="khong_ton_tai", unit_id=unit)
    lab = full_label(unit, table.label.get(doc, doc))
    if store.version_at(unit, as_of) is None:
        return Citation(ref=ref, status="het_hieu_luc", unit_id=unit, label=lab)
    return Citation(ref=ref, status="ok", unit_id=unit, label=lab)


__all__ = [
    "VALID_STATUSES",
    "CitableSource",
    "Citation",
    "CitationStatus",
    "FreeCitationIn",
    "SoHieuTable",
    "doc_label",
    "full_label",
    "label_candidates",
    "resolve_citation",
    "resolve_free_citation",
    "unit_label",
]
