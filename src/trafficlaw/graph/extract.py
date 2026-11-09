"""Trích xuất thực thể ngữ nghĩa (M8): hàm thuần — regex con số, chọn item, gom lô, schema LLM,
hậu kiểm đầu ra LLM, ghép nút/cạnh ngữ nghĩa.

Nguyên tắc (CLAUDE.md mục 8 "Quy ước trích xuất (M8)"):

- **Rule trước**: CheTai (phạt tiền, cảnh cáo, tước quyền sử dụng, tịch thu, đình chỉ), DiemGPLX,
  BienPhapBoSung (biện pháp khắc phục hậu quả "buộc …") và KhaiNiem trong Điều "Giải thích từ ngữ"
  lấy bằng regex trên text phiên bản. **Con số pháp lý chỉ đến từ regex**; LLM không trả số.
- **Nối chế tài với hành vi bằng cấu trúc + DAN_CHIEU** (không để LLM đoán): mức phạt ở câu dẫn
  Khoản → mọi Điểm con (``ke_thua_khoan``); mệnh đề "Thực hiện hành vi quy định tại X … bị …" →
  các unit X lấy từ cạnh DAN_CHIEU có ``span`` nằm trong mệnh đề (``dan_chieu``); unit lá tự nêu
  chế tài → chính nó (``truc_tiep``). Cạnh đi từ PhienBan của unit hành vi, hiệu lực = giao của
  khoảng hiệu lực hai phiên bản.
- **LLM sau**: HanhVi (span nguyên văn, kiểm tra là chuỗi con), PhuongTien/ChuThe chọn id từ danh
  mục đóng, KhaiNiem ngoài mẫu chuẩn. Sai → loại, ghi lý do.

Module chỉ dùng API đọc của ``GraphStore`` (M6) — không import ``build.py``/``references.py``.
"""

from __future__ import annotations

import hashlib
import re
import unicodedata
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from trafficlaw.graph.store import (
    BaseGraphStore,
    GraphEdge,
    GraphNode,
    canonical_json,
    unit_of_version_id,
)
from trafficlaw.utils.dates import parse_iso

# =========================================================================== văn bản


def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def norm_ws(s: str) -> str:
    return re.sub(r"\s+", " ", nfc(s)).strip()


def norm_name(s: str) -> str:
    """So khớp tên: NFC, chữ thường, bỏ dấu câu, gộp khoảng trắng (giữ dấu tiếng Việt)."""
    s = nfc(s).lower()
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def slugify(s: str) -> str:
    """``Xe gắn máy`` → ``xe-gan-may`` (bỏ dấu, đ→d)."""
    s = nfc(s).lower().replace("đ", "d")
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def sha256(obj: Any) -> str:
    data = obj if isinstance(obj, str) else canonical_json(obj)
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def parse_vnd(s: str) -> int:
    """``400.000`` → 400000."""
    return int(re.sub(r"[.\s]", "", s))


_NUM_RE = re.compile(r"\d[\d.]*")


def numbers_in(s: str) -> set[int]:
    """Các số trong chuỗi (``02`` = 2, ``400.000`` = 400000)."""
    out: set[int] = set()
    for m in _NUM_RE.finditer(s):
        tok = m.group(0).rstrip(".")
        if tok:
            out.add(int(tok.replace(".", "")))
    return out


def numbers_ok(llm_text: str | None, source: str) -> bool:
    """Mọi số trong chuỗi LLM viết phải xuất hiện trong văn bản nguồn."""
    return not llm_text or numbers_in(llm_text) <= numbers_in(source)


def find_verbatim(span: str, text: str) -> str | None:
    """Tìm ``span`` trong ``text`` không phân biệt khoảng trắng (rồi hoa/thường). Trả về đoạn
    nguyên văn trong ``text`` hoặc ``None``."""
    span = norm_ws(span)
    if not span:
        return None
    parts = [re.escape(p) for p in span.split(" ")]
    pat = r"\s+".join(parts)
    m = re.search(pat, nfc(text)) or re.search(pat, nfc(text), flags=re.IGNORECASE)
    return m.group(0) if m else None


# =========================================================================== regex con số

SanctionKind = Literal["phat_tien", "canh_cao", "tuoc_quyen", "tich_thu", "dinh_chi"]

_FINE_RE = re.compile(
    r"[Pp]hạt tiền từ (?P<a>\d[\d.]*) đồng đến (?P<b>\d[\d.]*) đồng"
    r"(?: đối với (?P<who1>cá nhân))?"
    # Mức riêng cho tổ chức trong cùng câu: "…, từ Z đồng đến T đồng đối với tổ chức" (NĐ 168,
    # NĐ 336 — câu không lặp chữ "Phạt tiền").
    r"(?P<org>, từ (?P<c>\d[\d.]*) đồng đến (?P<d>\d[\d.]*) đồng đối với (?P<who2>tổ chức))?"
)
_WARN_RE = re.compile(r"[Pp]hạt cảnh cáo")
_REVOKE_RE = re.compile(
    r"[Tt]ước quyền sử dụng (?P<obj>(?:(?!tháng)[^;.:]){1,160}?) từ (?P<a>\d+) tháng đến "
    r"(?P<b>\d+) tháng"
)
_SUSPEND_RE = re.compile(
    r"[Đđ]ình chỉ hoạt động (?P<obj>(?:(?!tháng)[^;.:]){0,120}?)\s*từ (?P<a>\d+) tháng đến "
    r"(?P<b>\d+) tháng"
)
_CONFISCATE_RE = re.compile(r"[Tt]ịch thu (?P<obj>[^;.]{1,200}?)(?=;|\.(?:\s|$)|$| đối với )")
_POINTS_RE = re.compile(
    r"trừ điểm giấy phép lái(?: xe)?(?:\s*\((?P<cond>[^)]*)\))? (?P<n>\d+) điểm"
)
# Biện pháp khắc phục hậu quả: "buộc …" (không "bắt buộc"), và "phải khôi phục …" (NĐ 168 Đ32 K19 e
# viết không có chữ "buộc"). Chỉ áp trong ngữ cảnh "biện pháp khắc phục hậu quả".
_REMEDY_RE = re.compile(
    r"(?<!bắt )(?<![\w])(?:[Bb]uộc|[Pp]hải khôi phục) (?P<body>[^;]{2,400}?)(?=;|\.(?:\s|$)|$)"
)
REMEDY_CONTEXT_RE = re.compile(r"biện pháp khắc phục hậu quả")
_DEF_RE = re.compile(
    r"^\d+[a-z]?\.\s*(?P<term>[^.:;()]{2,160}?)\s*"
    r"(?:\((?:sau đây )?gọi(?: tắt)? là (?P<alias>[^)]+)\)\s*)?"
    r"(?:là|được hiểu là|bao gồm|gồm)(?=[\s:])"
)
_CLAUSE_RE = re.compile(r"[Tt]hực hiện (?:các |một trong các )?hành vi (?:vi phạm )?quy định tại ")


@dataclass(frozen=True)
class Sanction:
    """Một hình thức xử phạt tìm thấy bằng regex. Vị trí tính trên text phiên bản (NFC)."""

    loai: SanctionKind
    span: str
    start: int
    end: int
    min_vnd: int | None = None
    max_vnd: int | None = None
    min_thang: int | None = None
    max_thang: int | None = None
    doi_tuong: str | None = None

    def props(self) -> dict[str, Any]:
        return {
            "loai": self.loai,
            "min_vnd": self.min_vnd,
            "max_vnd": self.max_vnd,
            "min_thang": self.min_thang,
            "max_thang": self.max_thang,
            "doi_tuong": self.doi_tuong,
            "span": self.span,
        }


@dataclass(frozen=True)
class Points:
    so_diem: int
    span: str
    start: int
    end: int
    dieu_kien: str | None = None


@dataclass(frozen=True)
class Remedy:
    name: str
    span: str
    start: int
    end: int


@dataclass(frozen=True)
class Definition:
    term: str
    aliases: tuple[str, ...]
    span: str


def _clean_obj(s: str) -> str:
    s = re.sub(r"\s*\((?:nếu có|nếu có hoặc đã được cấp)\)\s*", " ", s)
    return norm_ws(s).rstrip(",")


def find_sanctions(text: str) -> list[Sanction]:
    """Mọi hình thức xử phạt trong ``text`` theo thứ tự xuất hiện."""
    t = nfc(text)
    out: list[Sanction] = []
    for m in _FINE_RE.finditer(t):
        end1 = m.start("org") if m["org"] else m.end()
        out.append(
            Sanction(
                "phat_tien",
                t[m.start() : end1],
                m.start(),
                end1,
                min_vnd=parse_vnd(m["a"]),
                max_vnd=parse_vnd(m["b"]),
                doi_tuong=m["who1"],
            )
        )
        if m["org"]:
            s0 = m.start("org") + 2  # bỏ ", "
            out.append(
                Sanction(
                    "phat_tien",
                    t[s0 : m.end()],
                    s0,
                    m.end(),
                    min_vnd=parse_vnd(m["c"]),
                    max_vnd=parse_vnd(m["d"]),
                    doi_tuong=m["who2"],
                )
            )
    for m in _WARN_RE.finditer(t):
        out.append(Sanction("canh_cao", m.group(0), m.start(), m.end()))
    for m in _REVOKE_RE.finditer(t):
        out.append(
            Sanction(
                "tuoc_quyen",
                m.group(0),
                m.start(),
                m.end(),
                min_thang=int(m["a"]),
                max_thang=int(m["b"]),
                doi_tuong=_clean_obj(m["obj"]),
            )
        )
    for m in _SUSPEND_RE.finditer(t):
        out.append(
            Sanction(
                "dinh_chi",
                m.group(0),
                m.start(),
                m.end(),
                min_thang=int(m["a"]),
                max_thang=int(m["b"]),
                doi_tuong=_clean_obj(m["obj"]) or None,
            )
        )
    for m in _CONFISCATE_RE.finditer(t):
        out.append(
            Sanction("tich_thu", m.group(0), m.start(), m.end(), doi_tuong=_clean_obj(m["obj"]))
        )
    return sorted(out, key=lambda s: (s.start, s.loai))


def find_points(text: str) -> list[Points]:
    t = nfc(text)
    return [
        Points(
            int(m["n"]), m.group(0), m.start(), m.end(), norm_ws(m["cond"]) if m["cond"] else None
        )
        for m in _POINTS_RE.finditer(t)
    ]


def find_remedies(text: str) -> list[Remedy]:
    """Cụm "buộc …" / "phải khôi phục …" (chỉ gọi khi ngữ cảnh là "biện pháp khắc phục hậu
    quả")."""
    t = nfc(text)
    out = []
    for m in _REMEDY_RE.finditer(t):
        span = m.group(0).strip()
        out.append(Remedy(norm_ws(span[0].lower() + span[1:]), span, m.start(), m.end()))
    return out


def find_definition(text: str) -> Definition | None:
    """``N. <Thuật ngữ> (sau đây gọi là <alias>) là …`` — alias chỉ lấy từ "(sau đây gọi là …)"."""
    first = nfc(text).split("\n", 1)[0]
    m = _DEF_RE.match(first)
    if not m:
        return None
    term = re.sub(r"\s+quy định tại (?:\S+ ){0,3}này$", "", norm_ws(m["term"]))
    if not term or term[0].islower() or len(term.split()) > 20:
        return None
    aliases = tuple(norm_ws(a) for a in re.split(r",| hoặc ", m["alias"])) if m["alias"] else ()
    return Definition(term=term, aliases=tuple(a for a in aliases if a), span=first)


@dataclass(frozen=True)
class Clause:
    """Mệnh đề "Thực hiện hành vi quy định tại X … bị …": ``[start, end)`` trên text;
    ``refs_start`` = vị trí bắt đầu cụm dẫn chiếu X."""

    start: int
    end: int
    refs_start: int


def find_clauses(text: str) -> list[Clause]:
    t = nfc(text)
    ms = list(_CLAUSE_RE.finditer(t))
    out = []
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(t)
        out.append(Clause(m.start(), end, m.end()))
    return out


# =========================================================================== cấu hình


class BatchConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    group_by: Literal["doc", "dieu"] = "doc"
    """``doc``: gom nhiều Điều cùng văn bản vào một lượt (quota Gemini free 20 lượt/ngày);
    ``dieu``: mỗi lượt chỉ một Điều."""
    max_items: int = 80
    max_chars: int = 40000


class ExtractLLMConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    provider: str | None = None
    model_id: str | None = None
    prompt: str = "extract_items"
    max_output_tokens: int = 32768


class ExtractConfig(BaseModel):
    """``configs/extract.yaml`` (phần trích xuất)."""

    model_config = ConfigDict(extra="ignore")
    tiers_full: list[str] = ["A"]
    tiers_selective: list[str] = ["B"]
    skip_dieu_title: str = (
        r"^(?:Sửa đổi|Bãi bỏ|Bổ sung|Thay thế)\b.*\b(?:số|Nghị định|Thông tư|Luật)\b"
    )
    sanction_dieu_title: str = r"^Xử phạt"
    definition_dieu_title: str = r"Giải thích từ ngữ"
    selective_hint: str = (
        r"[Pp]hạt tiền|[Pp]hạt cảnh cáo|trừ điểm giấy phép lái|[Tt]ước quyền sử dụng|"
        r"[Tt]ịch thu|biện pháp khắc phục hậu quả"
    )
    definition_hint: str = r"^\d+[a-z]?\.\s*[^.:;]{2,160}?\s(?:là|được hiểu là)\s"
    batch: BatchConfig = Field(default_factory=BatchConfig)
    llm: ExtractLLMConfig = Field(default_factory=ExtractLLMConfig)


# =========================================================================== danh mục


class CatalogEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    name: str
    nhom: str | None = None
    can_cu: str | None = None
    """Unit định nghĩa/căn cứ (vd ``LUAT36-2024/D34/K1/g``)."""
    aliases: list[str] = []
    """Chỉ thêm khi có căn cứ trong văn bản ("sau đây gọi là …")."""
    bao_gom: list[str] = []
    evidence: str | None = None


class Catalog(BaseModel):
    """Danh mục đóng PhuongTien/ChuThe (``data/registry/extract_catalog.yaml``)."""

    model_config = ConfigDict(extra="forbid")
    approved: bool = False
    phuong_tien: list[CatalogEntry] = []
    chu_the: list[CatalogEntry] = []

    def ids(self, kind: Literal["phuong_tien", "chu_the"]) -> list[str]:
        return [e.id for e in getattr(self, kind)]

    def hash(self) -> str:
        return sha256(self.model_dump(mode="json", exclude={"approved"}))


# =========================================================================== item


@dataclass(frozen=True)
class Item:
    """Một PhienBan lá (Điểm, Khoản không có Điểm, Điều không chia Khoản) kèm ngữ cảnh."""

    version_id: str
    unit_id: str
    doc_id: str
    tier: str
    dieu_id: str
    dieu_title: str
    parent_text: str | None
    text: str
    effective_from: str | None
    effective_to: str | None
    key: str

    @property
    def n_chars(self) -> int:
        return len(self.text) + len(self.parent_text or "") + len(self.dieu_title)


def item_key(dieu_title: str, parent_text: str | None, text: str) -> str:
    """Trùng ngữ cảnh + text (sau NFC) ⇒ cùng khoá ⇒ gọi LLM một lần."""
    return sha256([nfc(dieu_title), nfc(parent_text or ""), nfc(text)])


def dieu_of(unit_id: str) -> str:
    parts = unit_id.split("/")
    return "/".join(parts[:2]) if len(parts) >= 2 else unit_id


def _iso(v: Any) -> date | None:
    return v if isinstance(v, date) or v is None else parse_iso(str(v))


def active_versions(store: BaseGraphStore, unit_id: str) -> list[GraphNode]:
    return [v for v in store.versions(unit_id) if v.props.get("status") != "repealed"]


def overlap(a_from: Any, a_to: Any, b_from: Any, b_to: Any) -> tuple[date, date | None] | None:
    """Giao hai khoảng ``[from, to]`` (to null = vô hạn); from null → không có hiệu lực."""
    af, at, bf, bt = _iso(a_from), _iso(a_to), _iso(b_from), _iso(b_to)
    if af is None or bf is None:
        return None
    f = max(af, bf)
    tos = [x for x in (at, bt) if x is not None]
    t = min(tos) if tos else None
    if t is not None and t < f:
        return None
    return f, t


def _version_at_start(store: BaseGraphStore, unit_id: str, v: GraphNode) -> GraphNode | None:
    d = _iso(v.props.get("effective_from"))
    return store.version_at(unit_id, d) if d is not None else None


@dataclass
class Scope:
    """Văn bản trong phạm vi trích xuất + Điều theo vai trò."""

    docs: dict[str, str]  # doc_id → tier
    dieus: list[GraphNode]
    sanction_dieus: set[str]
    definition_dieus: set[str]


def build_scope(
    store: BaseGraphStore, cfg: ExtractConfig, doc_ids: Sequence[str] | None = None
) -> Scope:
    tiers = set(cfg.tiers_full) | set(cfg.tiers_selective)
    docs = {
        n.id: str(n.props.get("tier"))
        for n in store.nodes_by_label("VanBan")
        if n.props.get("indexable")
        and n.props.get("tier") in tiers
        and (doc_ids is None or n.id in doc_ids)
    }
    skip = re.compile(cfg.skip_dieu_title)
    sanc = re.compile(cfg.sanction_dieu_title)
    defi = re.compile(cfg.definition_dieu_title)
    dieus: list[GraphNode] = []
    for doc in sorted(docs):
        for d in store.nodes_by_label("Dieu", doc_id=doc):
            title = str(d.props.get("title") or "")
            if skip.search(title):
                continue
            dieus.append(d)
    return Scope(
        docs=docs,
        dieus=dieus,
        sanction_dieus={d.id for d in dieus if sanc.search(str(d.props.get("title") or ""))},
        definition_dieus={d.id for d in dieus if defi.search(str(d.props.get("title") or ""))},
    )


def _khoan_group(store: BaseGraphStore, unit_id: str, dieu_id: str) -> str:
    """Khoản chứa unit (Điểm → Khoản cha nếu có), dùng cho lọc tier B."""
    p = store.parent(unit_id)
    if p is not None and p.startswith(dieu_id + "/") and p.rsplit("/", 1)[-1].startswith("K"):
        return p
    return unit_id


def select_items(
    store: BaseGraphStore, cfg: ExtractConfig, doc_ids: Sequence[str] | None = None
) -> list[Item]:
    """Mọi item trong phạm vi, thứ tự văn bản → Điều → cây con. Tier B: chỉ Khoản (cả cây con)
    có chế tài hoặc định nghĩa (``selective_hint``/``definition_hint``/Điều giải thích từ ngữ)."""
    scope = build_scope(store, cfg, doc_ids)
    hint = re.compile(cfg.selective_hint)
    dhint = re.compile(cfg.definition_hint)
    out: list[Item] = []
    for d in scope.dieus:
        doc = str(d.props["doc_id"])
        tier = scope.docs[doc]
        title = norm_ws(str(d.props.get("title") or ""))
        units = store.subtree(d.id)
        kids = {u: store.children(u) for u in units}
        texts: dict[str, list[str]] = {
            u: [str(v.props.get("text") or "") for v in active_versions(store, u)] for u in units
        }
        selective_ok: dict[str, bool] = {}
        if tier in cfg.tiers_selective and tier not in cfg.tiers_full:
            for u in units:
                g = _khoan_group(store, u, d.id)
                if g not in selective_ok:
                    sub = store.subtree(g)
                    txt = "\n".join(t for s in sub for t in texts.get(s) or [])
                    selective_ok[g] = d.id in scope.definition_dieus or bool(
                        hint.search(txt) or any(dhint.search(x) for x in txt.split("\n"))
                    )
        for u in units:
            if kids[u] or (u == d.id and len(units) > 1):
                continue
            if selective_ok and not selective_ok.get(_khoan_group(store, u, d.id), False):
                continue
            parent = store.parent(u)
            for v in active_versions(store, u):
                ptext: str | None = None
                if parent and parent != d.id and parent.startswith(d.id + "/"):
                    pv = _version_at_start(store, parent, v)
                    ptext = str(pv.props.get("text")) if pv is not None else None
                text = str(v.props.get("text") or "")
                if u == d.id:
                    text = "\n".join(text.split("\n")[1:]) or text
                out.append(
                    Item(
                        version_id=v.id,
                        unit_id=u,
                        doc_id=doc,
                        tier=tier,
                        dieu_id=d.id,
                        dieu_title=title,
                        parent_text=ptext,
                        text=text,
                        effective_from=v.props.get("effective_from"),
                        effective_to=v.props.get("effective_to"),
                        key=item_key(title, ptext, text),
                    )
                )
    return out


@dataclass
class Batch:
    batch_id: str
    group_id: str
    """``doc_id`` (``group_by: doc``) hoặc mã Điều (``group_by: dieu``)."""
    items: list[Item]

    @property
    def keys(self) -> list[str]:
        return [i.key for i in self.items]

    @property
    def key(self) -> str:
        return sha256(self.keys)

    @property
    def n_chars(self) -> int:
        return sum(i.n_chars for i in self.items)


def make_batches(
    items: Iterable[Item], cfg: BatchConfig, *, skip_keys: set[str] | None = None
) -> list[Batch]:
    """Gom item cùng văn bản (hoặc cùng Điều, theo ``group_by``), giữ thứ tự gốc, bỏ khoá trùng
    (toàn cục) và khoá đã xong; mỗi lô ≤ ``max_items`` item và ≤ ``max_chars`` ký tự (item lớn
    hơn ngưỡng vẫn đi một mình). Lô không cắt giữa một Điều nếu Điều đó vừa một lô mới."""
    seen = set(skip_keys or ())
    groups: dict[str, list[Item]] = {}
    for it in items:
        if it.key in seen:
            continue
        seen.add(it.key)
        g = it.doc_id if cfg.group_by == "doc" else it.dieu_id
        groups.setdefault(g, []).append(it)
    out: list[Batch] = []
    for dieu, its in groups.items():
        cur: list[Item] = []
        size = 0
        n = 0
        for it in its:
            if cur and (len(cur) >= cfg.max_items or size + it.n_chars > cfg.max_chars):
                out.append(Batch(f"{dieu}#{n}", dieu, cur))
                n += 1
                cur, size = [], 0
            cur.append(it)
            size += it.n_chars
        if cur:
            out.append(Batch(f"{dieu}#{n}", dieu, cur))
    return out


# =========================================================================== schema LLM


class HanhViOut(BaseModel):
    span: str = Field(description="Đoạn chép NGUYÊN VĂN từ nội dung item mô tả một hành vi")
    ten: str = Field(description="Tên ngắn gọn của hành vi (≤ 15 từ), không thêm con số")
    dieu_kien: str | None = Field(None, description="Tình tiết/điều kiện đi kèm, nếu có")


class KhaiNiemOut(BaseModel):
    thuat_ngu: str
    dinh_nghia: str = Field(description="Đoạn nguyên văn định nghĩa thuật ngữ")


class DeXuatOut(BaseModel):
    loai: Literal["PhuongTien", "ChuThe"]
    ten: str


class ItemOut(BaseModel):
    id: str = Field(description="Mã item, vd I1")
    hanh_vi: list[HanhViOut] = []
    phuong_tien: list[str] = []
    chu_the: list[str] = []
    khai_niem: list[KhaiNiemOut] = []
    de_xuat_moi: list[DeXuatOut] = []


class BatchOut(BaseModel):
    items: list[ItemOut]


def _inline(schema: dict[str, Any]) -> dict[str, Any]:
    """Thay ``$ref`` bằng định nghĩa, bỏ ``title``/``default`` (Gemini responseJsonSchema)."""
    defs = schema.get("$defs", {})

    def walk(x: Any) -> Any:
        if isinstance(x, dict):
            if "$ref" in x:
                return walk(defs[x["$ref"].rsplit("/", 1)[-1]])
            return {k: walk(v) for k, v in x.items() if k not in ("title", "default", "$defs")}
        if isinstance(x, list):
            return [walk(v) for v in x]
        return x

    return walk(schema)


def batch_schema(catalog: Catalog) -> type[BatchOut]:
    """Lớp ``BatchOut`` mà JSON Schema gửi API có ``enum`` id danh mục (validate phía mình vẫn
    nhận chuỗi bất kỳ — id ngoài danh mục bị loại ở hậu kiểm, không làm hỏng cả lô)."""
    pt, ct = catalog.ids("phuong_tien"), catalog.ids("chu_the")

    class _BatchOut(BatchOut):
        @classmethod
        def model_json_schema(cls, *a: Any, **kw: Any) -> dict[str, Any]:  # type: ignore[override]
            s = _inline(BatchOut.model_json_schema())
            props = s["properties"]["items"]["items"]["properties"]
            if pt:
                props["phuong_tien"]["items"]["enum"] = pt
            if ct:
                props["chu_the"]["items"]["enum"] = ct
            props["hanh_vi"]["items"]["properties"]["dieu_kien"] = {"type": "string"}
            return s

    _BatchOut.__name__ = "BatchOut"
    return _BatchOut


def render_items(batch: Batch) -> str:
    """Khối item cho prompt: tiêu đề Điều in mỗi khi sang Điều mới; câu dẫn Khoản in lại khi
    đổi."""
    lines: list[str] = []
    last_dieu: str | None = None
    last_parent: str | None = None
    for i, it in enumerate(batch.items, 1):
        if it.dieu_id != last_dieu:
            lines += [f"## Điều: {it.dieu_title} ({it.dieu_id})", ""]
            last_dieu, last_parent = it.dieu_id, None
        if it.parent_text and it.parent_text != last_parent:
            lines += [f"[Câu dẫn của khoản] {norm_ws(it.parent_text)}", ""]
        last_parent = it.parent_text
        lines += [f"### I{i} — {it.unit_id}", it.text.strip(), ""]
    return "\n".join(lines).strip()


def render_catalog(catalog: Catalog) -> tuple[str, str]:
    def fmt(es: Sequence[CatalogEntry]) -> str:
        rows = []
        for e in es:
            extra = f" (còn gọi: {', '.join(e.aliases)})" if e.aliases else ""
            grp = f" [nhóm: {e.nhom}]" if e.nhom else ""
            rows.append(f"- {e.id}: {e.name}{extra}{grp}")
        return "\n".join(rows)

    return fmt(catalog.phuong_tien), fmt(catalog.chu_the)


# =========================================================================== hậu kiểm LLM


@dataclass
class Rejection:
    item_key: str
    unit_id: str
    kind: str
    value: str
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "item_key": self.item_key,
            "unit_id": self.unit_id,
            "kind": self.kind,
            "value": self.value,
            "reason": self.reason,
        }


@dataclass
class ItemResult:
    """Đầu ra LLM đã hậu kiểm cho một item."""

    hanh_vi: list[dict[str, Any]] = field(default_factory=list)
    phuong_tien: list[str] = field(default_factory=list)
    chu_the: list[str] = field(default_factory=list)
    khai_niem: list[dict[str, Any]] = field(default_factory=list)
    de_xuat_moi: list[dict[str, Any]] = field(default_factory=list)


# Hậu kiểm theo hướng dẫn gán nhãn (data/qa/gold_extraction_guide.md), áp cho mọi item:
# - span chỉ DẪN CHIẾU hành vi ở nơi khác ("Thực hiện hành vi quy định tại …", "Vi phạm quy định
#   tại … mà …", "hành vi vi phạm hành chính quy định tại …") không phải HanhVi;
# - cụm ngoại lệ ", trừ …" ở cuối span bị cắt bỏ (ngoại lệ không gán nhãn);
# - PhuongTien chung chung bị bỏ khi item đã có loại xe cụ thể (chọn mục cụ thể nhất).
_REF_ONLY_RE = re.compile(
    r"(?i)hành vi (?:vi phạm )?(?:hành chính )?quy định tại |(?<![\w])vi phạm quy định tại "
)
_EXCEPT_TAIL_RE = re.compile(r",?\s+trừ (?:các |hành vi |trường hợp |người |xe |loại )")
GENERIC_PT: frozenset[str] = frozenset(
    {"PT:phuong-tien-giao-thong-duong-bo", "PT:phuong-tien-tham-gia-giao-thong-duong-bo"}
)


def validate_item_output(
    item: Item, out: Mapping[str, Any], catalog: Catalog
) -> tuple[ItemResult, list[Rejection]]:
    """Kiểm tra một ``ItemOut`` (dict) với text của item:

    - HanhVi: ``span`` phải có nguyên văn trong text (không phân biệt khoảng trắng) → lưu đoạn
      nguyên văn; ``ten``/``dieu_kien`` có con số không có trong text → loại (``so_lech_van_ban``).
    - HanhVi chỉ dẫn chiếu hành vi nơi khác → loại (``chi_dan_chieu``); cụm ngoại lệ ", trừ …"
      cuối span → cắt bỏ.
    - PhuongTien/ChuThe: id ngoài danh mục → loại (``ngoai_danh_muc``); PhuongTien chung chung
      khi đã có loại xe cụ thể → loại (``pt_chung_chung``).
    - KhaiNiem: thuật ngữ + định nghĩa phải nguyên văn.
    """
    res = ItemResult()
    rej: list[Rejection] = []
    text = item.text

    def reject(kind: str, value: Any, reason: str) -> None:
        rej.append(Rejection(item.key, item.unit_id, kind, str(value)[:300], reason))

    for hv in out.get("hanh_vi") or []:
        span = find_verbatim(str(hv.get("span") or ""), text)
        if span is None:
            reject("HanhVi", hv.get("span"), "span_khong_nguyen_van")
            continue
        if _REF_ONLY_RE.search(span):
            reject("HanhVi", span, "chi_dan_chieu")
            continue
        m = _EXCEPT_TAIL_RE.search(span)
        if m and m.start() > 0:
            span = span[: m.start()].rstrip(" ,;")
        ten = norm_ws(str(hv.get("ten") or "")) or norm_ws(span)
        cond = norm_ws(str(hv.get("dieu_kien") or "")) or None
        if not numbers_ok(ten, text) or not numbers_ok(cond, text):
            reject("HanhVi", ten, "so_lech_van_ban")
            continue
        res.hanh_vi.append({"span": span, "ten": ten, "dieu_kien": cond})
    for kind in ("phuong_tien", "chu_the"):
        valid = set(catalog.ids(kind))  # type: ignore[arg-type]
        for x in dict.fromkeys(out.get(kind) or []):
            if x in valid:
                getattr(res, kind).append(x)
            else:
                reject("PhuongTien" if kind == "phuong_tien" else "ChuThe", x, "ngoai_danh_muc")
    if any(x not in GENERIC_PT for x in res.phuong_tien):
        for x in [x for x in res.phuong_tien if x in GENERIC_PT]:
            res.phuong_tien.remove(x)
            reject("PhuongTien", x, "pt_chung_chung")
    for kn in out.get("khai_niem") or []:
        term = find_verbatim(str(kn.get("thuat_ngu") or ""), text)
        span = find_verbatim(str(kn.get("dinh_nghia") or ""), text)
        if term is None or span is None:
            reject("KhaiNiem", kn.get("thuat_ngu"), "span_khong_nguyen_van")
            continue
        res.khai_niem.append({"term": norm_ws(term), "span": span})
    for dx in out.get("de_xuat_moi") or []:
        res.de_xuat_moi.append({"loai": dx.get("loai"), "ten": norm_ws(str(dx.get("ten") or ""))})
    return res, rej


def map_batch_output(
    batch: Batch, parsed: Mapping[str, Any], catalog: Catalog
) -> tuple[dict[str, ItemResult], list[Rejection]]:
    """``BatchOut`` → item_key → kết quả đã hậu kiểm. Item thiếu trong phản hồi → kết quả rỗng
    + rejection ``thieu_item`` (vẫn coi là đã xử lý để không gọi lại vô hạn)."""
    by_id = {str(o.get("id")): o for o in parsed.get("items") or []}
    res: dict[str, ItemResult] = {}
    rej: list[Rejection] = []
    for i, it in enumerate(batch.items, 1):
        o = by_id.get(f"I{i}")
        if o is None:
            rej.append(Rejection(it.key, it.unit_id, "item", f"I{i}", "thieu_item"))
            res[it.key] = ItemResult()
            continue
        r, rj = validate_item_output(it, o, catalog)
        res[it.key] = r
        rej += rj
    extra = sorted(set(by_id) - {f"I{i}" for i in range(1, len(batch.items) + 1)})
    for x in extra:
        rej.append(Rejection("", batch.group_id, "item", x, "item_khong_ton_tai"))
    return res, rej


def verify_numeric_entity(entity: Mapping[str, Any], text: str) -> str | None:
    """Kiểm tra con số của một thực thể do LLM viết (bản nháp gold) với regex trên text unit.

    Trả về lý do loại (``so_lech_regex``) hoặc ``None`` nếu khớp/không có số.
    """
    typ = entity.get("type")
    if typ == "CheTai":
        loai = entity.get("loai")
        for s in find_sanctions(text):
            if s.loai != loai:
                continue
            if (s.min_vnd, s.max_vnd, s.min_thang, s.max_thang) == (
                entity.get("min_vnd"),
                entity.get("max_vnd"),
                entity.get("min_thang"),
                entity.get("max_thang"),
            ):
                return None
        return "so_lech_regex"
    if typ == "DiemGPLX":
        return (
            None
            if entity.get("so_diem") in {p.so_diem for p in find_points(text)}
            else ("so_lech_regex")
        )
    return None


# =========================================================================== dựng nút/cạnh


@dataclass
class Assembly:
    nodes: dict[str, GraphNode] = field(default_factory=dict)
    edges: dict[str, GraphEdge] = field(default_factory=dict)
    rejections: list[Rejection] = field(default_factory=list)
    stats: dict[str, int] = field(default_factory=dict)

    def add_node(self, nid: str, label: str, props: Mapping[str, Any]) -> None:
        if nid not in self.nodes:
            self.nodes[nid] = GraphNode(nid, label, dict(props))

    def add_edge(self, etype: str, src: str, dst: str, props: Mapping[str, Any]) -> None:
        e = GraphEdge.make(etype, src, dst, props)
        self.edges.setdefault(e.key, e)

    def bump(self, k: str, n: int = 1) -> None:
        self.stats[k] = self.stats.get(k, 0) + n

    def sorted_nodes(self) -> list[GraphNode]:
        return [self.nodes[k] for k in sorted(self.nodes)]

    def sorted_edges(self) -> list[GraphEdge]:
        return sorted(self.edges.values(), key=lambda e: e.sort_key)


def _effect(f: Any, t: Any) -> dict[str, Any]:
    return {
        "effective_from": f.isoformat() if isinstance(f, date) else f,
        "effective_to": t.isoformat() if isinstance(t, date) else t,
    }


def _leaves(store: BaseGraphStore, unit_id: str) -> list[str]:
    """Unit lá theo cấu trúc trong cây con (unit không có con → chính nó). Không lọc theo ngày:
    thời gian do phép giao khoảng hiệu lực ở ``_link`` quyết định (Điểm có hiệu lực riêng hoặc
    được bổ sung sau vẫn nhận chế tài của Khoản trong khoảng chung)."""
    sub = store.subtree(unit_id)
    leaves = [u for u in sub if not store.children(u)]
    return leaves or [unit_id]


def _link(
    asm: Assembly,
    store: BaseGraphStore,
    etype: str,
    stated: GraphNode,
    targets: Sequence[str],
    dst: str,
    props: Mapping[str, Any],
) -> None:
    """Cạnh ``etype`` từ mọi phiên bản (còn hiệu lực) của các unit đích, hiệu lực = giao với
    phiên bản ``stated`` nêu chế tài."""
    sf, st = stated.props.get("effective_from"), stated.props.get("effective_to")
    for u in dict.fromkeys(targets):
        for tv in active_versions(store, u):
            ov = overlap(sf, st, tv.props.get("effective_from"), tv.props.get("effective_to"))
            if ov is None:
                continue
            asm.add_edge(etype, tv.id, dst, {**_effect(*ov), **props, "stated_in": stated.id})
            asm.bump(f"edge:{etype}:{props.get('nguon')}")


def _clause_targets(
    store: BaseGraphStore, version: GraphNode, text: str, clause: Clause
) -> list[str]:
    """Unit lá được mệnh đề dẫn chiếu (DAN_CHIEU của phiên bản có span nằm ngay sau "quy định
    tại"); unit có con → mọi lá của nó tại ngày bắt đầu phiên bản."""
    out: list[str] = []
    for e in store.out_edges(version.id, types=["DAN_CHIEU"]):
        span = str(e.props.get("span") or "")
        pos = text.find(span, clause.refs_start) if span else -1
        if pos != clause.refs_start:
            continue
        out += _leaves(store, e.dst)
    return sorted(dict.fromkeys(out))


def assemble_rules(
    store: BaseGraphStore, cfg: ExtractConfig, asm: Assembly, doc_ids: Sequence[str] | None = None
) -> None:
    """CheTai/DiemGPLX/BienPhapBoSung (Điều "Xử phạt …") + KhaiNiem (Điều "Giải thích từ ngữ")
    bằng regex, nối với hành vi bằng cấu trúc + DAN_CHIEU."""
    scope = build_scope(store, cfg, doc_ids)
    for d in scope.dieus:
        is_sanc = d.id in scope.sanction_dieus
        is_def = d.id in scope.definition_dieus
        if not (is_sanc or is_def):
            continue
        for u in store.subtree(d.id):
            if u == d.id:
                continue
            for v in active_versions(store, u):
                text = nfc(str(v.props.get("text") or ""))
                if is_sanc:
                    _rules_sanctions(store, asm, d.id, u, v, text)
                if is_def:
                    _rules_definition(asm, str(d.props["doc_id"]), u, v, text)


def _rules_sanctions(
    store: BaseGraphStore, asm: Assembly, dieu_id: str, unit_id: str, v: GraphNode, text: str
) -> None:
    clauses = find_clauses(text)
    own_kids = store.children(unit_id)
    own_targets = _leaves(store, unit_id) if own_kids else [unit_id]
    own_nguon = "ke_thua_khoan" if own_kids else "truc_tiep"
    parent = store.parent(unit_id)
    ctx = text
    if parent and parent != dieu_id:
        pv = _version_at_start(store, parent, v)
        if pv is not None:
            ctx = str(pv.props.get("text") or "") + "\n" + text
    remedies_ok = bool(REMEDY_CONTEXT_RE.search(ctx))
    base = {
        "unit_id": unit_id,
        "version_id": v.id,
        "doc_id": v.id.split("/")[0],
        "nguon_trich": "rule",
    }

    def scope_of(pos: int) -> tuple[list[str], str, str | None]:
        for c in clauses:
            if c.start <= pos < c.end:
                tg = _clause_targets(store, v, text, c)
                cond = None
                m = re.search(
                    r"\b(trong trường hợp [^;]+?|mà [^;]+?)(?= còn bị| bị| buộc|$)",
                    text[c.refs_start : pos],
                )
                if m:
                    cond = norm_ws(m.group(1))
                return tg, "dan_chieu", cond
        return own_targets, own_nguon, None

    for k, s in enumerate(find_sanctions(text)):
        nid = f"CHETAI:{v.id}#{k}"
        asm.add_node(nid, "CheTai", {**base, **s.props()})
        asm.bump("node:CheTai")
        tg, nguon, cond = scope_of(s.start)
        if nguon == "dan_chieu" and not tg:
            asm.rejections.append(
                Rejection("", unit_id, "CheTai", s.span, "dan_chieu_khong_phan_giai")
            )
        _link(asm, store, "BI_XU_PHAT", v, tg, nid, {"nguon": nguon, "dieu_kien": cond})
    for k2, p in enumerate(find_points(text)):
        nid = f"DIEM:{v.id}#{k2}"
        asm.add_node(
            nid,
            "DiemGPLX",
            {**base, "so_diem": p.so_diem, "dieu_kien": p.dieu_kien, "span": p.span},
        )
        asm.bump("node:DiemGPLX")
        tg, nguon, cond = scope_of(p.start)
        if nguon == "dan_chieu" and not tg:
            asm.rejections.append(
                Rejection("", unit_id, "DiemGPLX", p.span, "dan_chieu_khong_phan_giai")
            )
        _link(asm, store, "BI_TRU_DIEM", v, tg, nid, {"nguon": nguon, "dieu_kien": cond})
    if remedies_ok:
        for k3, r in enumerate(find_remedies(text)):
            nid = f"BPBS:{v.id}#{k3}"
            asm.add_node(
                nid, "BienPhapBoSung", {**base, "name": r.name, "thoi_han": None, "span": r.span}
            )
            asm.bump("node:BienPhapBoSung")
            tg, nguon, cond = scope_of(r.start)
            if nguon == "dan_chieu" and not tg:
                asm.rejections.append(
                    Rejection("", unit_id, "BienPhapBoSung", r.span, "dan_chieu_khong_phan_giai")
                )
            _link(asm, store, "BI_XU_PHAT", v, tg, nid, {"nguon": nguon, "dieu_kien": cond})


def khai_niem_id(doc_id: str, term: str) -> str:
    return f"KN:{doc_id}:{slugify(term)}"


def _rules_definition(asm: Assembly, doc_id: str, unit_id: str, v: GraphNode, text: str) -> None:
    if unit_id.rsplit("/", 1)[-1][:1] != "K":
        return
    df = find_definition(text)
    if df is None:
        return
    nid = khai_niem_id(doc_id, df.term)
    asm.add_node(
        nid,
        "KhaiNiem",
        {
            "name": df.term,
            "aliases": list(df.aliases),
            "doc_id": doc_id,
            "unit_id": unit_id,
            "nguon_trich": "rule",
        },
    )
    asm.bump("node:KhaiNiem")
    asm.add_edge(
        "DINH_NGHIA",
        v.id,
        nid,
        {
            **_effect(v.props.get("effective_from"), v.props.get("effective_to")),
            "nguon": "rule",
            "span": df.span,
        },
    )


def assemble_catalog(asm: Assembly, catalog: Catalog) -> None:
    for e in catalog.phuong_tien:
        asm.add_node(
            e.id,
            "PhuongTien",
            {
                "name": e.name,
                "aliases": e.aliases,
                "nhom": e.nhom,
                "can_cu": e.can_cu,
                "bao_gom": e.bao_gom,
            },
        )
    for e in catalog.chu_the:
        asm.add_node(
            e.id,
            "ChuThe",
            {"name": e.name, "aliases": e.aliases, "nhom": e.nhom, "can_cu": e.can_cu},
        )


def assemble_llm(
    asm: Assembly,
    items: Sequence[Item],
    results: Mapping[str, ItemResult],
    *,
    model_id: str,
) -> None:
    """HanhVi (một nút cho mỗi phiên bản × hành vi), AP_DUNG_CHO, KhaiNiem do LLM."""
    for it in items:
        r = results.get(it.key)
        if r is None:
            asm.bump("item:chua_trich")
            continue
        asm.bump("item:da_trich")
        eff = _effect(it.effective_from, it.effective_to)
        base = {
            "unit_id": it.unit_id,
            "version_id": it.version_id,
            "doc_id": it.doc_id,
            "nguon_trich": "llm",
            "model_id": model_id,
        }
        for k, hv in enumerate(r.hanh_vi):
            nid = f"HV:{it.version_id}#{k}"
            asm.add_node(
                nid,
                "HanhVi",
                {**base, "name": hv["ten"], "span": hv["span"], "dieu_kien": hv["dieu_kien"]},
            )
            asm.bump("node:HanhVi")
            asm.add_edge("QUY_DINH_HANH_VI", it.version_id, nid, {**eff, "nguon": "llm"})
        for x in [*r.phuong_tien, *r.chu_the]:
            asm.add_edge("AP_DUNG_CHO", it.version_id, x, {**eff, "nguon": "llm"})
            asm.bump("edge:AP_DUNG_CHO")
        for kn in r.khai_niem:
            nid = khai_niem_id(it.doc_id, kn["term"])
            asm.add_node(
                nid,
                "KhaiNiem",
                {
                    "name": kn["term"],
                    "aliases": [],
                    "doc_id": it.doc_id,
                    "unit_id": it.unit_id,
                    "nguon_trich": "llm",
                },
            )
            asm.add_edge(
                "DINH_NGHIA", it.version_id, nid, {**eff, "nguon": "llm", "span": kn["span"]}
            )


def prune_dangling(asm: Assembly, store: BaseGraphStore) -> None:
    """Bỏ cạnh có đầu mút không có trong store lẫn tập nút mới (vd id danh mục chưa có nút)."""
    known = set(asm.nodes)
    ids = sorted({x for e in asm.edges.values() for x in (e.src, e.dst)} - known)
    have = set(store.get_nodes(ids))
    for k in [
        k
        for k, e in asm.edges.items()
        if (e.src not in known and e.src not in have) or (e.dst not in known and e.dst not in have)
    ]:
        asm.bump("edge:treo_bo")
        del asm.edges[k]


__all__ = [
    "Assembly",
    "Batch",
    "BatchOut",
    "Catalog",
    "CatalogEntry",
    "Clause",
    "Definition",
    "ExtractConfig",
    "Item",
    "ItemResult",
    "Points",
    "Rejection",
    "Remedy",
    "Sanction",
    "assemble_catalog",
    "assemble_llm",
    "assemble_rules",
    "batch_schema",
    "build_scope",
    "find_clauses",
    "find_definition",
    "find_points",
    "find_remedies",
    "find_sanctions",
    "find_verbatim",
    "make_batches",
    "map_batch_output",
    "norm_name",
    "numbers_ok",
    "prune_dangling",
    "render_catalog",
    "render_items",
    "select_items",
    "slugify",
    "unit_of_version_id",
    "validate_item_output",
    "verify_numeric_entity",
]
