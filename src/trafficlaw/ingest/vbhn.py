"""Đối chiếu phiên bản điều khoản với văn bản hợp nhất (VBHN) — kiểm chứng M4.

- **Chú thích VBHN** (``Unit.footnotes``) có cấu trúc đều: "<Khoản|Điểm|Điều|Cụm từ “A”|Mẫu|
  Phụ lục> này được <sửa đổi, bổ sung|bổ sung|bãi bỏ|bỏ|thay thế …> theo quy định tại <dẫn
  chiếu> (của) <Luật|Nghị định> số X, có hiệu lực (thi hành) kể từ ngày D". :func:`parse_footnote`
  đọc ra loại thao tác, văn bản nguồn và ngày.
- **Đơn vị so** là Khoản: toàn bộ cây con (Khoản + Điểm) của phiên bản có hiệu lực tại
  ``as_of`` so với cây con tương ứng trong VBHN (mã ánh xạ thẳng: ``VBHN55-VPQH/D9/K18`` ↔
  ``LUAT36-2024/D9/K18``). Điều không chia Khoản được so cả Điều.
- **Khớp** = bằng nhau sau chuẩn hoá mạnh (:func:`strong_norm`: NFC, bỏ ``[^N]`` và nhãn, chữ
  thường, chỉ giữ chữ và số). Khoản khớp được chia ``khop`` (bằng nhau cả sau chuẩn hoá nhẹ) và
  ``chi_khac_dinh_dang``; tỷ lệ ``difflib`` chỉ để chẩn đoán Khoản lệch.
- **Loại khỏi mẫu số**: Khoản có chú thích từ văn bản ngoài danh mục (``loai_ngoai_danh_muc``),
  Khoản thuộc lỗi dữ liệu đã biết (``loai_loi_du_lieu``, liệt kê trong ``vbhn_map.yaml``).
"""

from __future__ import annotations

import difflib
import re
import unicodedata
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict

from trafficlaw.ingest.amendments import parse_vn_date_in
from trafficlaw.ingest.structure import Unit
from trafficlaw.ingest.versions import AddedUnit, VersionStore

# ---------------------------------------------------------------- vbhn_map.yaml


class VbhnEntry(BaseModel):
    """Một VBHN trong ``data/registry/vbhn_map.yaml``."""

    model_config = ConfigDict(extra="forbid")

    vbhn: str
    base_doc: str
    as_of: date
    #: Văn bản sửa đổi trong danh mục mà VBHN đã gộp (để kiểm tra chéo).
    in_registry_sources: list[str] = []
    #: Văn bản sửa đổi ngoài danh mục mà VBHN đã gộp (Khoản bị chúng sửa bị loại khỏi tỷ lệ).
    out_of_registry_sources: list[str] = []
    #: Mã unit VBHN có lỗi dữ liệu đã biết (M2/M3) → loại khỏi tỷ lệ.
    known_issues: list[str] = []
    #: Văn bản sửa đổi phải kiểm tra chéo: mọi chú thích nguồn này phải có phiên bản cùng ngày.
    crosscheck_source: str | None = None
    min_match_rate: float = 0.95
    notes: str | None = None


def load_vbhn_map(path: str | Path) -> list[VbhnEntry]:
    path = Path(path)
    if not path.is_file():
        return []
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return [VbhnEntry.model_validate(x) for x in data.get("vbhn") or []]


def map_id(vbhn_unit_id: str, vbhn_doc: str, base_doc: str) -> str:
    """``VBHN55-VPQH/D9/K18`` → ``LUAT36-2024/D9/K18``."""
    if vbhn_unit_id == vbhn_doc:
        return base_doc
    assert vbhn_unit_id.startswith(vbhn_doc + "/"), vbhn_unit_id
    return base_doc + vbhn_unit_id[len(vbhn_doc) :]


# ---------------------------------------------------------------- chú thích

FootnoteOp = Literal["sua_doi", "bo_sung", "bai_bo", "bo", "thay_the", "quy_dinh"]
FootnoteSubject = Literal["dieu", "khoan", "diem", "cum_tu", "mau", "phu_luc", "khac"]

_SUBJECT = (
    ("Khoản", "khoan"),
    ("Điểm", "diem"),
    ("Điều", "dieu"),
    ("Cụm từ", "cum_tu"),
    ("Mẫu", "mau"),
    ("Phụ lục", "phu_luc"),
)
_OP = re.compile(r"được\s+(sửa\s+đổi,\s*bổ\s+sung|bổ\s+sung|bãi\s+bỏ|bỏ|thay\s+thế)")
_OP_MAP = {"bổ sung": "bo_sung", "bãi bỏ": "bai_bo", "bỏ": "bo", "thay thế": "thay_the"}
_SOURCE = re.compile(
    r"theo\s+quy\s+định\s+tại\s+.*?(?:Luật|Nghị\s+định|Thông\s+tư)\s+(?:số\s+)?"
    r"(\d+/\d{4}/[A-Za-zĐđ0-9\-]+)"
)
_ANY_SOURCE = re.compile(
    r"(?:Luật|Nghị\s+định|Thông\s+tư)\s+(?:số\s+)?(\d+/\d{4}/[A-Za-zĐđ0-9\-]+)"
)
_EFFECT = re.compile(
    r"có\s+hiệu\s+lực\s+(?:thi\s+hành\s+)?(?:kể\s+)?từ\s+(ngày\s+\d+\s+tháng\s+\d+\s+năm\s+\d+)"
)


class FootnoteInfo(BaseModel):
    model_config = ConfigDict(extra="forbid")

    vbhn_unit_id: str
    n: str
    subject: FootnoteSubject
    op: FootnoteOp
    source_so_hieu: str | None
    effective_from: date | None
    text: str


def parse_footnote(vbhn_unit_id: str, n: str, text: str) -> FootnoteInfo:
    s = unicodedata.normalize("NFC", text).strip()
    subject: FootnoteSubject = "khac"
    for word, key in _SUBJECT:
        if s.startswith(word):
            subject = key  # type: ignore[assignment]
            break
    op: FootnoteOp = "quy_dinh"
    m = _OP.search(s)
    if m and "quy định như sau" not in s[: m.start()] and subject != "khac":
        raw = re.sub(r"\s+", " ", m[1])
        op = "sua_doi" if raw.startswith("sửa đổi") else _OP_MAP[raw]  # type: ignore[assignment]
    src = _SOURCE.search(s) or _ANY_SOURCE.search(s)
    eff = _EFFECT.search(s)
    return FootnoteInfo(
        vbhn_unit_id=vbhn_unit_id,
        n=n,
        subject=subject,
        op=op,
        source_so_hieu=src[1].rstrip(".,;") if src else None,
        effective_from=parse_vn_date_in(eff[1]) if eff else None,
        text=s,
    )


def footnotes_of(units: Iterable[Unit]) -> list[FootnoteInfo]:
    out: list[FootnoteInfo] = []
    for u in units:
        for n, t in u.footnotes.items():
            out.append(parse_footnote(u.id, n, t))
    return out


# ---------------------------------------------------------------- chuẩn hoá văn bản

_FN = re.compile(r"\s*\[\^\d+\]")
_LBL = re.compile(r"^(?:Điều\s+\d+[a-z]?\s*\.|\d+[a-z]?\.|[a-zđ]\d*\))\s*", re.M)
_QUOTES = str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'"})


def light_norm(text: str) -> str:
    s = unicodedata.normalize("NFC", text)
    s = _FN.sub("", s)
    s = _LBL.sub("", s)
    s = s.translate(_QUOTES)
    return re.sub(r"\s+", " ", s).strip()


# Kiểu bỏ dấu cũ → mới ("hoá" → "hóa", "thuỷ" → "thủy"): cùng một chữ, khác vị trí dấu.
_TONE = {
    "oà": "òa",
    "oá": "óa",
    "oả": "ỏa",
    "oã": "õa",
    "oạ": "ọa",
    "oè": "òe",
    "oé": "óe",
    "oẻ": "ỏe",
    "oẽ": "õe",
    "oẹ": "ọe",
    "uỳ": "ùy",
    "uý": "úy",
    "uỷ": "ủy",
    "uỹ": "ũy",
    "uỵ": "ụy",
}
_TONE_RE = re.compile("|".join(_TONE))


def strong_norm(text: str) -> str:
    """Chỉ giữ chữ và số (chữ thường, thống nhất kiểu bỏ dấu): miễn nhiễm dấu câu, khoảng
    trắng, hoa/thường, "hoá"/"hóa"; vẫn nhạy với mọi khác biệt về chữ và số."""
    s = _TONE_RE.sub(lambda m: _TONE[m[0]], light_norm(text).lower())
    return re.sub(r"[\W_]+", "", s)


_REPEALED_MARK = re.compile(r"^\(?\s*(?:được|đã được)\s+bãi\s+bỏ\s*\)?\s*[.;]?$", re.I)


def is_repealed_placeholder(text: str) -> bool:
    """VBHN giữ nhãn unit bị bãi bỏ kèm "(được bãi bỏ)" — coi như không có unit."""
    return bool(_REPEALED_MARK.match(light_norm(text)))


# ---------------------------------------------------------------- cây unit


def unit_tree(units: Sequence[Unit], added: Sequence[AddedUnit] = ()) -> dict[str, list[str]]:
    """``parent_id → [con theo thứ tự]``, gồm cả unit bổ sung.

    Unit bổ sung đặt theo ``after_id``/``before_id``; không có cả hai → cuối danh sách con.
    """
    children: dict[str, list[str]] = {}
    for u in units:
        if u.parent_id:
            children.setdefault(u.parent_id, []).append(u.id)
    for a in added:
        sib = children.setdefault(a.parent_id or a.doc_id, [])
        if a.id in sib:
            continue
        if a.before_id in sib:
            sib.insert(sib.index(a.before_id), a.id)
        elif a.after_id in sib:
            sib.insert(sib.index(a.after_id) + 1, a.id)
        else:
            sib.append(a.id)
    return children


# ---------------------------------------------------------------- so khớp

CompareStatus = Literal[
    "khop",
    "chi_khac_dinh_dang",
    "khac_noi_dung",
    "thieu_vbhn",  # có trong phiên bản tại as_of, không có trong VBHN
    "thieu_goc",  # có trong VBHN, không có phiên bản hiệu lực tại as_of
    "loai_ngoai_danh_muc",
    "loai_loi_du_lieu",
]
MATCH = ("khop", "chi_khac_dinh_dang")
EXCLUDED = ("loai_ngoai_danh_muc", "loai_loi_du_lieu")


class CompareRow(BaseModel):
    """Một dòng ``vbhn_compare.jsonl``."""

    model_config = ConfigDict(extra="forbid")

    vbhn: str
    unit_id: str
    status: CompareStatus
    ratio: float | None = None
    reason: str | None = None
    ours: str | None = None
    theirs: str | None = None


@dataclass
class CompareResult:
    vbhn: str
    rows: list[CompareRow]
    crosscheck_failures: list[str] = field(default_factory=list)
    crosscheck_checked: int = 0
    crosscheck_skipped: int = 0

    def count(self, status: str) -> int:
        return sum(r.status == status for r in self.rows)

    @property
    def n_compared(self) -> int:
        return sum(r.status not in EXCLUDED for r in self.rows)

    @property
    def n_match(self) -> int:
        return sum(r.status in MATCH for r in self.rows)

    @property
    def match_rate(self) -> float:
        return self.n_match / self.n_compared if self.n_compared else 0.0


def _subtree_text(
    uid: str, children: Mapping[str, list[str]], text_of: Mapping[str, str | None]
) -> str | None:
    own = text_of.get(uid)
    if own is None:
        return None
    parts = [own]
    for c in children.get(uid, ()):
        t = _subtree_text(c, children, text_of)
        if t:
            parts.append(t)
    return "\n".join(p for p in parts if p)


def _compare_items(
    dieu_ids: Iterable[str],
    children: Mapping[str, list[str]],
    level: Mapping[str, str],
    text: Mapping[str, str | None],
) -> list[str]:
    """Đơn vị so: Khoản (còn hiệu lực/còn nội dung) của mỗi Điều; Điều không chia Khoản → Điều."""
    out: list[str] = []
    for d in dieu_ids:
        ks = [c for c in children.get(d, ()) if level.get(c) == "khoan" and text.get(c)]
        out.extend(ks or [d])
    return out


def _khoan_of(uid: str) -> str:
    parts = uid.split("/")
    for i, p in enumerate(parts):
        if p.startswith("K") and p[1:2].isdigit():
            return "/".join(parts[: i + 1])
    return uid


def compare_vbhn(
    entry: VbhnEntry,
    vbhn_units: Sequence[Unit],
    base_units: Sequence[Unit],
    added: Sequence[AddedUnit],
    store: VersionStore,
    so_hieu_to_doc: Mapping[str, str],
) -> CompareResult:
    """So các Khoản của ``entry.base_doc`` tại ``entry.as_of`` với VBHN ``entry.vbhn``."""
    as_of = entry.as_of
    # --- phía VBHN (mã đã ánh xạ sang văn bản gốc)
    v_children_raw = unit_tree(vbhn_units)
    vmap = {u.id: map_id(u.id, entry.vbhn, entry.base_doc) for u in vbhn_units}
    v_children = {vmap[p]: [vmap[c] for c in cs] for p, cs in v_children_raw.items() if p in vmap}
    v_text: dict[str, str | None] = {
        vmap[u.id]: None if is_repealed_placeholder(u.text) else u.text for u in vbhn_units
    }
    v_level = {vmap[u.id]: u.level for u in vbhn_units}
    v_dieu = [vmap[u.id] for u in vbhn_units if u.level == "dieu" and v_text[vmap[u.id]]]
    # --- phía phiên bản
    o_children = unit_tree(base_units, added)
    o_level: dict[str, str] = {u.id: u.level for u in base_units}
    o_level.update({a.id: a.level for a in added})
    o_text: dict[str, str | None] = {}
    for uid in o_level:
        v = store.get_version(uid, as_of)
        o_text[uid] = None if v is None else v.text
    o_dieu = [u for u, lv in o_level.items() if lv == "dieu" and o_text.get(u) is not None]

    # --- loại trừ
    excluded: dict[str, tuple[CompareStatus, str]] = {}
    excluded_dieu: dict[str, tuple[CompareStatus, str]] = {}  # loại mọi Khoản của Điều
    out_reg = {s.upper() for s in entry.out_of_registry_sources}
    for fn in footnotes_of(vbhn_units):
        if fn.op == "quy_dinh" or fn.source_so_hieu is None:
            continue
        src = fn.source_so_hieu.upper()
        if src in out_reg or src not in so_hieu_to_doc:
            uid = vmap[fn.vbhn_unit_id]
            lv = v_level.get(uid)
            why = ("loai_ngoai_danh_muc", f"[^{fn.n}] {fn.source_so_hieu}")
            if lv == "dieu":
                excluded_dieu[uid] = why  # type: ignore[assignment]
            elif lv in ("khoan", "diem"):
                excluded[_khoan_of(uid)] = why  # type: ignore[assignment]
    for vid in entry.known_issues:
        uid = map_id(vid, entry.vbhn, entry.base_doc)
        excluded.setdefault(_khoan_of(uid), ("loai_loi_du_lieu", "lỗi dữ liệu đã biết"))

    items_v = _compare_items(v_dieu, v_children, v_level, v_text)
    items_o = _compare_items(o_dieu, o_children, o_level, o_text)

    def exclusion(uid: str) -> tuple[CompareStatus, str] | None:
        if uid in excluded:
            return excluded[uid]
        dieu = "/".join(uid.split("/")[:2])
        return excluded_dieu.get(dieu)

    seen: set[str] = set()
    rows: list[CompareRow] = []
    for uid in [*items_v, *[i for i in items_o if i not in set(items_v)]]:
        if uid in seen:
            continue
        seen.add(uid)
        theirs = _subtree_text(uid, v_children, v_text) if v_text.get(uid) else None
        ours = _subtree_text(uid, o_children, o_text) if uid in o_text else None
        exc = exclusion(uid)
        if exc is not None:
            st, why = exc
            rows.append(CompareRow(vbhn=entry.vbhn, unit_id=uid, status=st, reason=why))
            continue
        if theirs is None or ours is None:
            rows.append(
                CompareRow(
                    vbhn=entry.vbhn,
                    unit_id=uid,
                    status="thieu_vbhn" if theirs is None else "thieu_goc",
                    ours=ours,
                    theirs=theirs,
                )
            )
            continue
        if light_norm(ours) == light_norm(theirs):
            st2: CompareStatus = "khop"
        elif strong_norm(ours) == strong_norm(theirs):
            st2 = "chi_khac_dinh_dang"
        else:
            st2 = "khac_noi_dung"
        ratio = None
        if st2 == "khac_noi_dung":
            ratio = round(
                difflib.SequenceMatcher(None, light_norm(ours), light_norm(theirs)).ratio(), 4
            )
        rows.append(
            CompareRow(
                vbhn=entry.vbhn,
                unit_id=uid,
                status=st2,
                ratio=ratio,
                ours=ours if st2 == "khac_noi_dung" else None,
                theirs=theirs if st2 == "khac_noi_dung" else None,
            )
        )
    res = CompareResult(entry.vbhn, rows)
    if entry.crosscheck_source:
        _crosscheck(entry, vbhn_units, vmap, o_children, store, so_hieu_to_doc, res)
    return res


def _crosscheck(
    entry: VbhnEntry,
    vbhn_units: Sequence[Unit],
    vmap: Mapping[str, str],
    children: Mapping[str, list[str]],
    store: VersionStore,
    so_hieu_to_doc: Mapping[str, str],
    res: CompareResult,
) -> None:
    """Mọi chú thích nguồn ``crosscheck_source`` phải ứng với một phiên bản cùng ngày."""
    src_doc = so_hieu_to_doc.get((entry.crosscheck_source or "").upper())
    assert src_doc, f"crosscheck_source không có trong danh mục: {entry.crosscheck_source}"

    def subtree(u: str) -> list[str]:
        out = [u]
        for c in children.get(u, ()):
            out.extend(subtree(c))
        return out

    for fn in footnotes_of(vbhn_units):
        if (fn.source_so_hieu or "").upper() != entry.crosscheck_source.upper():  # type: ignore[union-attr]
            continue
        if fn.op == "quy_dinh":
            continue
        uid = vmap[fn.vbhn_unit_id]
        if fn.subject in ("mau", "khac") or (fn.subject == "phu_luc" and uid not in store):
            # Mẫu không có unit riêng; văn bản gốc không tách được Phụ lục (ND165) → không kiểm.
            res.crosscheck_skipped += 1
            continue
        res.crosscheck_checked += 1
        ok = any(
            v.source_unit_id is not None
            and v.source_unit_id.startswith(src_doc + "/")
            and v.effective_from == fn.effective_from
            for u in subtree(uid)
            for v in store.versions_of(u)
        )
        if not ok:
            res.crosscheck_failures.append(f"{uid} [^{fn.n}] {fn.text[:160]}")
