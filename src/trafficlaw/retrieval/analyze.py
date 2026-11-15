"""Phân tích câu hỏi (M11): **rule trước, LLM dự phòng** (người dùng chốt 14/11/2026).

Rule (hàm thuần, :func:`analyze_rule`):

- **Ngày/mốc**: ``1/1/2026``, ``01-07-2026``, ``ngày 15 tháng 8 năm 2026``, ``tháng 8/2026`` /
  ``tháng 8 năm 2026`` (→ ngày 1 của tháng). Từ chỉ hướng ngay trước ngày: "trước (ngày)" → D − 1,
  "sau (ngày)" → D + 1, "từ / kể từ / bắt đầu từ" → D. **Ngày tham số luôn thắng** ngày đọc từ câu
  hỏi (``as_of_source = tham_so``); không có cả hai → ``today`` (``mac_dinh``).
- **Phương tiện / chủ thể** theo danh mục đóng M8 (``extract_catalog.yaml``: tên + alias), khớp
  theo ranh giới từ, **cụm dài nhất thắng, không chồng nhau** ⇒ "xe gắn máy" ≠ "xe mô tô", "xe tương
  tự xe mô tô" không sinh thêm "xe mô tô". Không gộp đồng nghĩa ngoài danh mục ("xe máy" không tự
  đổi thành mục nào → để LLM quyết định).
- **Loại câu** theo từ khoá (10 loại của M9). ``theo_thoi_diem`` và ``so_sanh`` là *bổ ngữ*: loại
  nội dung (mức phạt, định nghĩa…) thắng khi cùng có mặt, bổ ngữ ghi vào ``modifiers``.
- **Gợi ý văn bản**: ``DocNameTable`` (số hiệu đầy đủ, tên luật) + dạng rút gọn "Nghị định 168",
  "NĐ 168/2024", "Thông tư 38" (chỉ nhận khi khớp đúng một văn bản danh mục).

**Rule không chắc** (``uncertain``) ⇒ gọi LLM ``main`` (nếu bật):

- ``thoi_gian_tuong_doi`` ("năm ngoái", "trước khi … có hiệu lực"), ``chi_co_nam``,
  ``nhieu_ngay``, ``ngay_khong_hop_le`` — **chỉ khi không có ngày tham số** (có tham số thì ngày
  trong câu không ảnh hưởng truy hồi);
- ``phuong_tien_ngoai_danh_muc`` / ``chu_the_ngoai_danh_muc``: còn từ chỉ loại xe/chủ thể sau khi
  đã bỏ các cụm khớp danh mục;
- ``loai_cau_mo_ho``: ≥ 2 loại nội dung khác nhóm cạnh cùng điểm cao nhất; ``khong_ro_loai_cau``:
  không loại nào khớp. (Các loại cùng nhóm cạnh — ``muc_phat``/``tru_diem``/``bien_phap`` — không
  tính là mơ hồ vì cho cùng một hàng trong bảng graph expand.)

LLM chỉ được sửa đúng phần rule không chắc; mọi id phải thuộc danh mục/registry (id lạ bị bỏ);
LLM **không** sinh con số pháp lý (schema không có trường số). LLM lỗi/``format_error`` → giữ kết
quả rule (``analyzer = rule``, ghi ``llm_status``).
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
import threading
import time
import unicodedata
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from trafficlaw.eval.qa_schema import QUESTION_TYPES
from trafficlaw.graph.doc_names import DocNameTable
from trafficlaw.graph.extract import Catalog, CatalogEntry
from trafficlaw.utils.jsonl import JsonlWriter, read_jsonl

logger = logging.getLogger(__name__)

AsOfSource = Literal["tham_so", "cau_hoi", "mac_dinh"]

#: Loại câu "nội dung" (khác bổ ngữ), theo thứ tự ưu tiên khi đồng điểm cùng nhóm.
CONTENT_TYPES: tuple[str, ...] = (
    "muc_phat",
    "tru_diem",
    "bien_phap",
    "dinh_nghia",
    "thu_tuc_tham_quyen",
    "hanh_vi_cam_nghia_vu",
    "da_buoc",
    "ngoai_pham_vi",
)
MODIFIER_TYPES: tuple[str, ...] = ("so_sanh", "theo_thoi_diem")
#: Nhóm cạnh: các loại cùng nhóm dùng chung một hàng của bảng graph expand.
TYPE_GROUP: dict[str, str] = {"muc_phat": "che_tai", "tru_diem": "che_tai", "bien_phap": "che_tai"}

_TYPE_PATTERNS: dict[str, tuple[str, ...]] = {
    "muc_phat": (
        r"mức phạt",
        r"bị phạt",
        r"phạt tiền",
        r"phạt (?:bao nhiêu|thế nào|như thế nào|ra sao|gì)",
        r"bao nhiêu tiền",
        r"phạt cảnh cáo",
        r"bị xử phạt",
        r"xử phạt (?:bao nhiêu|thế nào|như thế nào|ra sao)",
    ),
    "tru_diem": (
        r"trừ điểm",
        r"bị trừ",
        r"(?:mấy|bao nhiêu) điểm",
        r"điểm giấy phép",
        r"phục hồi điểm",
    ),
    "bien_phap": (
        r"tước (?:quyền|giấy phép|bằng)",
        r"tịch thu",
        r"tạm giữ",
        r"khắc phục hậu quả",
        r"biện pháp",
        r"\bbuộc\b",
    ),
    "dinh_nghia": (
        r"là gì",
        r"được hiểu",
        r"khái niệm",
        r"định nghĩa",
        r"thế nào là",
        r"(?:bao )?gồm những (?:gì|loại|thành phần)",
        r"là (?:loại|những) (?:xe|phương tiện) (?:nào|gì)",
        r"được coi là",
    ),
    "thu_tuc_tham_quyen": (
        r"thủ tục",
        r"hồ sơ",
        r"trình tự",
        r"thẩm quyền",
        r"cơ quan nào",
        r"\bai (?:có|chịu|được|là người|phải|sẽ)\b",
        r"đơn vị nào",
        r"cấp (?:đổi|lại|mới)",
        r"đăng ký",
        r"lệ phí",
        r"thời hạn",
        r"làm (?:sao|thế nào) để",
        r"nhiệm vụ",
        r"chức năng",
        r"ở đâu",
        r"bao lâu",
    ),
    "hanh_vi_cam_nghia_vu": (
        r"có được (?:phép )?",
        r"được phép",
        r"không được",
        r"bị cấm",
        r"nghiêm cấm",
        r"\bcấm\b",
        r"nghĩa vụ",
        r"trách nhiệm",
        r"bắt buộc",
        r"\bphải\b(?! (?:là|không)\b)",
        r"yêu cầu",
        r"điều kiện",
        r"được hưởng",
        r"có quyền",
        r"cần (?:có|tuân thủ|đáp ứng|bảo đảm|đảm bảo|thực hiện)",
        r"quy định (?:gì|như thế nào|thế nào) về",
    ),
    "so_sanh": (r"so sánh", r"khác nhau", r"giống nhau", r"khác gì", r"khác biệt", r"so với"),
    "theo_thoi_diem": (
        r"thời điểm",
        r"(?:trước|sau|từ|kể từ) ngày",
        r"có hiệu lực (?:từ|khi|vào)",
        r"áp dụng từ",
    ),
}
_TYPE_RE = {t: [re.compile(p) for p in ps] for t, ps in _TYPE_PATTERNS.items()}

# --- ngày ------------------------------------------------------------------------------------

_DMY = re.compile(r"(?<![\d/])(\d{1,2})\s*[/.\-]\s*(\d{1,2})\s*[/.\-]\s*(\d{4})(?![\d/])")
_DMY_WORDS = re.compile(r"ngày\s+(\d{1,2})\s+tháng\s+(\d{1,2})\s+năm\s+(\d{4})")
_MY = re.compile(r"tháng\s+(\d{1,2})\s*(?:/|-|\s+năm\s+)\s*(\d{4})(?![\d/])")
_YEAR = re.compile(r"(?<![\d/])năm\s+(\d{4})(?![\d/])")
_BEFORE = re.compile(r"(?:trước|tới trước)\s+(?:(?:ngày|thời điểm|thời gian|tháng)\s+)?$")
_AFTER = re.compile(r"\bsau\s+(?:(?:ngày|thời điểm|tháng)\s+)?$")
_RELATIVE = re.compile(
    r"năm (?:ngoái|trước|tới|sau|nay)|tháng (?:trước|tới|sau|này)|tuần (?:trước|tới)"
    r"|hôm qua"
    r"|(?:trước|sau) khi [^?.,;]{0,60}(?:có hiệu lực|ban hành|sửa đổi|thay thế)"
    r"|(?:luật|quy định|nghị định|thông tư) cũ|khi [^?.,;]{0,40}chưa có hiệu lực"
)

# --- từ chỉ phương tiện / chủ thể còn lại sau khi bỏ cụm khớp danh mục -------------------------

_STOP_PHRASES = re.compile(
    r"giấy phép lái xe|bằng lái xe|lái xe(?= )|đào tạo lái xe|sát hạch lái xe|bến xe|bãi đỗ xe"
    r"|điểm đỗ xe|trạm dừng nghỉ|dừng xe|đỗ xe|kiểm định xe|đăng ký xe|biển số xe"
)
_VEHICLE_CUE = re.compile(
    r"\b(?:ô tô|mô tô|xe máy|xe tải|xe khách|xe con|xe container|xe công-te-nơ|xe ben|xe đầu kéo"
    r"|xe ba gác|xe lôi|xe ôm|xe bán tải|xe điện|xe kéo|xe chở|xe cứu|xe chữa cháy|xe tang"
    r"|xe taxi|taxi|xe hợp đồng|xe du lịch|xe giường nằm|xe khách|xe đưa đón|xe tập lái|xe sát hạch"
    r"|xe cẩu|xe lu|xe ủi|xe nâng|máy kéo|rơ moóc|xích lô|xe đạp|xe lăn|xe buýt|xe ưu tiên)\b"
)
_SUBJECT_CUE = re.compile(
    r"\b(?:tài xế|người lái|chủ xe|chủ phương tiện|chủ sở hữu|học viên|doanh nghiệp|công ty"
    r"|hợp tác xã|hộ kinh doanh|cảnh sát|công an|thanh tra|người nước ngoài|trẻ em|người khuyết tật"
    r"|người cao tuổi|người say rượu|phụ xe|lái xe taxi|người đi xe|người ngồi sau|người chở)\b"
)
_SHORT_DOC = re.compile(
    r"\b(nghị định|nđ|thông tư|tt|quyết định|qđ|luật)\s*(?:số\s*)?(\d{1,3})(?:\s*/\s*(\d{4}))?\b",
    re.I,
)
_LOAI_OF = {
    "nghị định": "nghi_dinh",
    "nđ": "nghi_dinh",
    "thông tư": "thong_tu",
    "tt": "thong_tu",
    "quyết định": "quyet_dinh",
    "qđ": "quyet_dinh",
    "luật": "luat",
}


def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def norm_text(s: str) -> str:
    """NFC, chữ thường, gộp khoảng trắng (giữ dấu tiếng Việt)."""
    return re.sub(r"\s+", " ", nfc(s).lower()).strip()


# --- kết quả ---------------------------------------------------------------------------------


class QueryAnalysis(BaseModel):
    """Kết quả phân tích một câu hỏi (ghi vào ``RetrievalResult``)."""

    model_config = ConfigDict(extra="forbid")

    as_of: date
    as_of_source: AsOfSource
    question_dates: list[date] = Field(default_factory=list)
    """Ngày đọc được từ câu hỏi (đã áp "trước/sau")."""
    vehicle_ids: list[str] = Field(default_factory=list)
    subject_ids: list[str] = Field(default_factory=list)
    question_type: str | None = None
    modifiers: list[str] = Field(default_factory=list)
    type_scores: dict[str, int] = Field(default_factory=dict)
    doc_hints: list[str] = Field(default_factory=list)
    analyzer: Literal["rule", "llm"] = "rule"
    uncertain: list[str] = Field(default_factory=list)
    """Lý do rule không chắc (đã bỏ lý do về ngày khi có ngày tham số)."""
    llm_reason: list[str] = Field(default_factory=list)
    """Lý do đã gọi LLM (rỗng = không gọi)."""
    llm_status: str | None = None
    """``ok`` | ``format_error`` | ``error`` | ``missing`` (pha 2 không có kết quả pha 1) |
    ``disabled``."""
    llm_model: str | None = None
    prompt_hash: str | None = None
    llm_cached: bool | None = None


# --- bảng rule -------------------------------------------------------------------------------


@dataclass(frozen=True)
class _Term:
    key: str
    pattern: re.Pattern[str]
    entry_id: str
    kind: Literal["phuong_tien", "chu_the"]


@dataclass
class AnalyzerTables:
    """Danh mục PT/CT (M8), bảng tên văn bản, registry (``doc_id`` → (loại, số hiệu))."""

    catalog: Catalog
    doc_names: DocNameTable | None = None
    registry: dict[str, tuple[str, str | None]] = field(default_factory=dict)
    terms: list[_Term] = field(init=False)

    def __post_init__(self) -> None:
        terms: list[_Term] = []
        for kind in ("phuong_tien", "chu_the"):
            entries: Sequence[CatalogEntry] = getattr(self.catalog, kind)
            for e in entries:
                for name in {e.name, *e.aliases}:
                    k = norm_text(name)
                    if not k:
                        continue
                    body = r"\s+".join(map(re.escape, k.split(" ")))
                    pat = re.compile(rf"(?<!\w){body}(?!\w)")
                    terms.append(_Term(k, pat, e.id, kind))  # type: ignore[arg-type]
        # Cụm dài trước (dài nhất thắng), đồng độ dài → id (tất định).
        self.terms = sorted(terms, key=lambda t: (-len(t.key), t.entry_id, t.key))

    def catalog_hash(self) -> str:
        return self.catalog.hash()

    def ids(self, kind: str) -> set[str]:
        return set(self.catalog.ids(kind))  # type: ignore[arg-type]


def match_catalog(text: str, tables: AnalyzerTables) -> tuple[list[str], list[str], str]:
    """(PT ids, CT ids, text đã thay các cụm khớp bằng khoảng trắng). Cụm dài nhất thắng, không
    chồng nhau; thứ tự id theo vị trí xuất hiện."""
    t = norm_text(text)
    covered = [False] * len(t)
    found: dict[str, list[str]] = {}
    # Hai lượt riêng: "người điều khiển xe gắn máy" = CT "người điều khiển xe" + PT "xe gắn máy".
    for kind in ("phuong_tien", "chu_the"):
        taken = [False] * len(t)
        hits: list[tuple[int, str]] = []
        for term in tables.terms:
            if term.kind != kind:
                continue
            for m in term.pattern.finditer(t):
                if any(taken[m.start() : m.end()]):
                    continue
                for i in range(m.start(), m.end()):
                    taken[i] = covered[i] = True
                hits.append((m.start(), term.entry_id))
        ids: list[str] = []
        for _, eid in sorted(hits):
            if eid not in ids:
                ids.append(eid)
        found[kind] = ids
    rest = "".join(" " if covered[i] else ch for i, ch in enumerate(t))
    return found["phuong_tien"], found["chu_the"], rest


def _safe_date(y: int, m: int, d: int) -> date | None:
    try:
        return date(y, m, d)
    except ValueError:
        return None


def parse_question_dates(text: str) -> tuple[list[date], list[str]]:
    """Ngày trong câu hỏi (đã áp "trước"/"sau") + lý do không chắc về thời gian."""
    t = norm_text(text)
    reasons: list[str] = []
    found: list[tuple[int, date]] = []
    taken = [False] * len(t)

    def mark(m: re.Match[str]) -> bool:
        if any(taken[m.start() : m.end()]):
            return False
        for i in range(m.start(), m.end()):
            taken[i] = True
        return True

    def shift(start: int, d: date, *, month: bool = False) -> date:
        before = t[max(0, start - 40) : start]
        # "ngày" thuộc chính cụm ngày (``ngày 15 tháng 8``) không có trong ``before``.
        if _BEFORE.search(before):
            return d - timedelta(days=1)
        if _AFTER.search(before) and not month:
            return d + timedelta(days=1)
        return d

    for rx in (_DMY_WORDS, _DMY):
        for m in rx.finditer(t):
            if not mark(m):
                continue
            d = _safe_date(int(m[3]), int(m[2]), int(m[1]))
            if d is None:
                reasons.append("ngay_khong_hop_le")
                continue
            start = m.start()
            if rx is _DMY:  # "ngày 01/07/2026": bỏ chữ "ngày" khi xét từ chỉ hướng
                pre = t[:start].rstrip()
                if pre.endswith("ngày"):
                    start = len(pre) - len("ngày")
            found.append((m.start(), shift(start, d)))
    for m in _MY.finditer(t):
        if not mark(m):
            continue
        d = _safe_date(int(m[2]), int(m[1]), 1)
        if d is None:
            reasons.append("ngay_khong_hop_le")
            continue
        found.append((m.start(), shift(m.start(), d, month=True)))
    for m in _YEAR.finditer(t):
        if not any(taken[m.start() : m.end()]):
            reasons.append("chi_co_nam")
            break
    if _RELATIVE.search(t):
        reasons.append("thoi_gian_tuong_doi")
    dates = sorted({d for _, d in found})
    if len(dates) > 1:
        reasons.append("nhieu_ngay")
    return dates, sorted(set(reasons))


def score_types(text: str) -> dict[str, int]:
    t = norm_text(text)
    out: dict[str, int] = {}
    for typ, rxs in _TYPE_RE.items():
        n = sum(1 for rx in rxs if rx.search(t))
        if n:
            out[typ] = n
    return out


def pick_type(scores: dict[str, int], has_dates: bool) -> tuple[str | None, list[str], list[str]]:
    """(loại câu, bổ ngữ, lý do không chắc)."""
    mods = [m for m in MODIFIER_TYPES if scores.get(m)]
    if has_dates and "theo_thoi_diem" not in mods:
        mods.append("theo_thoi_diem")
    content = {t: s for t, s in scores.items() if t in CONTENT_TYPES}
    if not content:
        if mods:
            return mods[0], mods, []
        return None, [], ["khong_ro_loai_cau"]
    best = max(content.values())
    top = [t for t in CONTENT_TYPES if content.get(t) == best]
    groups = {TYPE_GROUP.get(t, t) for t in top}
    reasons = ["loai_cau_mo_ho"] if len(groups) > 1 else []
    return top[0], mods, reasons


def doc_hints(text: str, tables: AnalyzerTables) -> list[str]:
    out: list[str] = []
    t = nfc(text)
    if tables.doc_names is not None:
        for mnt in tables.doc_names.find_all(t):
            if mnt.kind == "registry" and mnt.doc and mnt.doc not in out:
                out.append(mnt.doc)
    for m in _SHORT_DOC.finditer(t):
        loai = _LOAI_OF[m[1].lower()]
        num, year = m[2], m[3]
        cands = [
            d
            for d, (lo, sh) in sorted(tables.registry.items())
            if lo == loai
            and sh
            and sh.split("/")[0].lstrip("0") == num.lstrip("0")
            and (year is None or f"/{year}/" in sh + "/")
        ]
        if len(cands) == 1 and cands[0] not in out:
            out.append(cands[0])
    return out


def analyze_rule(
    question: str, as_of_param: date | None, tables: AnalyzerTables, *, today: date
) -> QueryAnalysis:
    """Phân tích bằng rule (thuần, tất định)."""
    dates, date_reasons = parse_question_dates(question)
    if as_of_param is not None:
        as_of, src = as_of_param, "tham_so"
        date_reasons = []  # ngày tham số thắng — ngày trong câu không ảnh hưởng truy hồi
    elif dates and "nhieu_ngay" not in date_reasons:
        as_of, src = dates[0], "cau_hoi"
    else:
        as_of, src = today, "mac_dinh"
    pt, ct, rest = match_catalog(question, tables)
    rest = _STOP_PHRASES.sub(" ", rest)
    reasons = list(date_reasons)
    if _VEHICLE_CUE.search(rest):
        reasons.append("phuong_tien_ngoai_danh_muc")
    if _SUBJECT_CUE.search(rest):
        reasons.append("chu_the_ngoai_danh_muc")
    scores = score_types(question)
    qtype, mods, type_reasons = pick_type(scores, bool(dates))
    reasons += type_reasons
    return QueryAnalysis(
        as_of=as_of,
        as_of_source=src,  # type: ignore[arg-type]
        question_dates=dates,
        vehicle_ids=pt,
        subject_ids=ct,
        question_type=qtype,
        modifiers=mods,
        type_scores=dict(sorted(scores.items())),
        doc_hints=doc_hints(question, tables),
        uncertain=sorted(set(reasons)),
    )


# --- LLM dự phòng ----------------------------------------------------------------------------

DATE_REASONS = frozenset({"thoi_gian_tuong_doi", "chi_co_nam", "nhieu_ngay", "ngay_khong_hop_le"})
ENTITY_REASONS = frozenset({"phuong_tien_ngoai_danh_muc", "chu_the_ngoai_danh_muc"})
TYPE_REASONS = frozenset({"loai_cau_mo_ho", "khong_ro_loai_cau"})


class AnalyzeLLMOut(BaseModel):
    """Schema JSON gửi LLM. Không có trường số pháp lý."""

    model_config = ConfigDict(extra="ignore")
    as_of: str | None = None
    """Ngày áp dụng ISO ``YYYY-MM-DD`` suy từ câu hỏi, hoặc null."""
    vehicle_ids: list[str] = Field(default_factory=list)
    subject_ids: list[str] = Field(default_factory=list)
    question_type: str | None = None
    doc_hints: list[str] = Field(default_factory=list)


def render_llm_messages(
    prompt_template: Any, question: str, ref_date: date, tables: AnalyzerTables
) -> list[dict[str, str]]:
    def lines(kind: str) -> str:
        entries: Sequence[CatalogEntry] = getattr(tables.catalog, kind)
        return "\n".join(
            f"- {e.id}: {e.name}" + (f" (còn gọi: {', '.join(e.aliases)})" if e.aliases else "")
            for e in entries
        )

    docs = "\n".join(
        f"- {d}: {sh or '(chưa có số hiệu)'}" for d, (_, sh) in tables.registry.items()
    )
    text = prompt_template.render(
        question=nfc(question).strip(),
        ref_date=ref_date.isoformat(),
        vehicles=lines("phuong_tien"),
        subjects=lines("chu_the"),
        types=", ".join(t for t in QUESTION_TYPES if t != "khac"),
        docs=docs,
    )
    return [{"role": "user", "content": text}]


def merge_llm(
    rule: QueryAnalysis, out: AnalyzeLLMOut, tables: AnalyzerTables, *, as_of_param: date | None
) -> QueryAnalysis:
    """Chỉ sửa phần rule không chắc; id lạ bị bỏ."""
    r = set(rule.uncertain)
    upd: dict[str, Any] = {"analyzer": "llm"}
    if as_of_param is None and r & DATE_REASONS and out.as_of:
        try:
            d = date.fromisoformat(out.as_of.strip()[:10])
            upd.update(as_of=d, as_of_source="cau_hoi")
        except ValueError:
            pass
    if r & ENTITY_REASONS:
        pts, cts = tables.ids("phuong_tien"), tables.ids("chu_the")
        upd["vehicle_ids"] = _union(rule.vehicle_ids, [x for x in out.vehicle_ids if x in pts])
        upd["subject_ids"] = _union(rule.subject_ids, [x for x in out.subject_ids if x in cts])
    if r & TYPE_REASONS and out.question_type in QUESTION_TYPES and out.question_type != "khac":
        upd["question_type"] = out.question_type
    upd["doc_hints"] = _union(rule.doc_hints, [x for x in out.doc_hints if x in tables.registry])
    return rule.model_copy(update=upd)


def _union(a: Iterable[str], b: Iterable[str]) -> list[str]:
    out: list[str] = []
    for x in [*a, *b]:
        if x not in out:
            out.append(x)
    return out


def _sha(obj: Any) -> str:
    return hashlib.sha256(
        json.dumps(obj, ensure_ascii=False, sort_keys=True, default=str).encode()
    ).hexdigest()


class LLMAnalysisStore:
    """Kết quả LLM của analyzer (JSONL append-only, resume). Chỉ lưu ``ok``/``format_error``
    (lỗi mạng chạy lại lần sau)."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self._rows: dict[str, dict[str, Any]] = {}
        for r in read_jsonl(self.path):
            self._rows[str(r["key"])] = r
        self._lock = threading.Lock()

    @staticmethod
    def key(
        model_id: str, prompt_hash: str, schema_hash: str, catalog_hash: str, q: str, ref: date
    ) -> str:
        return _sha([model_id, prompt_hash, schema_hash, catalog_hash, nfc(q).strip(), ref])

    def get(self, key: str) -> dict[str, Any] | None:
        return self._rows.get(key)

    def put(self, row: dict[str, Any]) -> None:
        with self._lock:
            self._rows[row["key"]] = row
            with JsonlWriter(self.path) as w:
                w.write(row)

    def __len__(self) -> int:
        return len(self._rows)


class MissingLLMAnalysisError(RuntimeError):
    """Pha retrieve cần kết quả LLM của analyzer nhưng chưa có (chạy ``--analyze-only``)."""


class Analyzer:
    """Ghép rule + LLM dự phòng. ``llm = None`` → chỉ đọc ``store`` (pha 2 / chạy lại ở local):
    thiếu → ``MissingLLMAnalysisError`` nếu ``strict``, ngược lại giữ rule (``llm_status =
    missing``)."""

    def __init__(
        self,
        tables: AnalyzerTables,
        *,
        today: date,
        llm: Any | None = None,
        store: LLMAnalysisStore | None = None,
        prompt: Any | None = None,
        max_output_tokens: int = 512,
        strict: bool = False,
    ) -> None:
        self.tables = tables
        self.today = today
        self.llm = llm
        self.store = store
        self.prompt = prompt
        self.max_output_tokens = max_output_tokens
        self.strict = strict
        self.schema_hash = _sha(AnalyzeLLMOut.model_json_schema())
        self.stats: dict[str, int] = {}

    @property
    def model_id(self) -> str | None:
        if self.llm is not None:
            return str(self.llm.model_id)
        return getattr(self, "_model_id", None)

    def set_model_id(self, model_id: str | None) -> None:
        """Model của các kết quả trong ``store`` khi không có client (pha 2)."""
        self._model_id = model_id

    def _bump(self, k: str) -> None:
        self.stats[k] = self.stats.get(k, 0) + 1

    def analyze(
        self, question: str, as_of_param: date | None, *, use_llm: bool = True
    ) -> QueryAnalysis:
        rule = analyze_rule(question, as_of_param, self.tables, today=self.today)
        if not rule.uncertain:
            self._bump("rule_chac")
            return rule
        if not use_llm or self.prompt is None or (self.llm is None and self.store is None):
            self._bump("llm_tat")
            return rule.model_copy(update={"llm_status": "disabled"})
        model_id = self.model_id
        if model_id is None:
            self._bump("llm_tat")
            return rule.model_copy(update={"llm_status": "disabled"})
        ref = as_of_param or self.today
        key = LLMAnalysisStore.key(
            model_id, self.prompt.hash, self.schema_hash, self.tables.catalog_hash(), question, ref
        )
        base = {
            "llm_reason": rule.uncertain,
            "llm_model": model_id,
            "prompt_hash": self.prompt.hash,
        }
        row = self.store.get(key) if self.store is not None else None
        cached = row is not None
        if row is None:
            if self.llm is None:
                self._bump("llm_thieu")
                if self.strict:
                    raise MissingLLMAnalysisError(
                        "thiếu kết quả LLM của analyzer — chạy scripts.retrieve --analyze-only"
                    )
                return rule.model_copy(update={**base, "llm_status": "missing"})
            row = self._call(question, ref, key)
            if row is None:  # lỗi mạng/hết retry — không lưu, giữ rule
                self._bump("llm_loi")
                return rule.model_copy(update={**base, "llm_status": "error"})
        self._bump(f"llm_{row['status']}")
        upd = {**base, "llm_status": row["status"], "llm_cached": cached}
        if row["status"] != "ok":
            return rule.model_copy(update=upd)
        merged = merge_llm(
            rule, AnalyzeLLMOut.model_validate(row["parsed"]), self.tables, as_of_param=as_of_param
        )
        return merged.model_copy(update=upd)

    def _call(self, question: str, ref: date, key: str) -> dict[str, Any] | None:
        assert self.llm is not None and self.prompt is not None
        msgs = render_llm_messages(self.prompt, question, ref, self.tables)
        t0 = time.perf_counter()
        res = self.llm.generate(
            msgs,
            json_schema=AnalyzeLLMOut,
            params={"max_output_tokens": self.max_output_tokens},
        )
        if res.status == "error":
            logger.warning("analyzer LLM lỗi: %s", res.error)
            return None
        row = {
            "key": key,
            "model_id": res.model_id,
            "prompt_hash": self.prompt.hash,
            "schema_hash": self.schema_hash,
            "question": nfc(question).strip(),
            "ref_date": ref.isoformat(),
            "status": res.status,
            "parsed": res.parsed if res.status == "ok" else None,
            "text": res.text if res.status != "ok" else None,
            "usage": res.usage.model_dump() if hasattr(res.usage, "model_dump") else None,
            "latency_ms": res.latency_ms,
            "attempts": res.attempts,
            "cached": res.cached,
            "wall_ms": round((time.perf_counter() - t0) * 1000, 1),
        }
        if self.store is not None:
            self.store.put(row)
        return row


__all__ = [
    "AnalyzeLLMOut",
    "Analyzer",
    "AnalyzerTables",
    "CONTENT_TYPES",
    "LLMAnalysisStore",
    "MODIFIER_TYPES",
    "MissingLLMAnalysisError",
    "QueryAnalysis",
    "analyze_rule",
    "doc_hints",
    "match_catalog",
    "merge_llm",
    "parse_question_dates",
    "pick_type",
    "render_llm_messages",
    "score_types",
]
