"""Con số pháp lý trong câu trả lời (M12; CLAUDE.md §2.6: không để LLM tự sinh).

Ba việc:

1. **Bảng con số** (:func:`build_number_table`): trước khi gọi LLM, mọi con số được phép dùng
   được liệt kê thành ``N1…Nm`` cho từng nguồn ``S#`` đưa vào ngữ cảnh:

   a. thuộc tính nút ``CheTai`` (``phat_tien`` → ``min_vnd``/``max_vnd``; ``tuoc_quyen``/
      ``dinh_chi`` → ``min_thang``/``max_thang``), ``DiemGPLX`` (``so_diem``),
      ``BienPhapBoSung`` (``thoi_han`` nếu có) — nút **nêu tại** một phiên bản của chunk
      (``props.version_id``) hoặc nối tới từ phiên bản đó bằng ``BI_XU_PHAT``/``BI_TRU_DIEM``
      (lọc theo ngày như M6);
   b. số có nguyên văn trong text chunk (``400.000``, ``1,35``, ``02``) kèm đơn vị liền sau và
      đoạn chữ quanh nó — **trừ** nhãn đầu dòng (``1.``), số sau ``Điều/khoản/điểm/Phụ lục/
      Mẫu số/…``, số hiệu văn bản (có ``/``), ngày tháng, và phần văn bản đã là span của một nút
      ở (a) (không trùng hai lần).

2. **Chỗ giữ chỗ** (:func:`render_numbers`): LLM chỉ viết ``{N3}``; renderer thay bằng giá trị
   định dạng kiểu Việt Nam (``từ 800.000 đồng đến 1.000.000 đồng``, ``02 điểm``).

3. **Dò số không kiểm được** (:func:`find_unverified_numbers`): quét văn bản LLM viết (đã che
   chỗ giữ chỗ). Hợp lệ: số Điều/Khoản/Điểm/Phụ lục…, số hiệu văn bản, số có trong chính câu hỏi,
   ngày có trong câu hỏi / ngày áp dụng / ngày hiệu lực của nguồn / ngày nêu trong nguồn. Còn lại
   là vi phạm: chữ số (``chu_so``), ngày không có căn cứ (``ngay``), số viết bằng chữ **dạng cơ
   bản** (``chu_viet``: chuỗi từ chỉ số một…chín, mười, mươi, trăm, nghìn/ngàn, triệu, tỷ… đứng
   ngay trước đơn vị đồng/điểm/tháng/ngày/giờ/phút/tuổi/năm/km/mét/tấn — "hai triệu đồng",
   "mười hai tháng"; cách viết khác không được dò).

Hàm thuần, không gọi LLM; đọc đồ thị qua ``GraphStore``.
"""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from trafficlaw.graph.store import BaseGraphStore, GraphNode

# --------------------------------------------------------------------------- số kiểu Việt Nam

NUM_RE = re.compile(r"\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+(?:,\d+)?")
"""Số kiểu Việt Nam: ``400.000``, ``0,25``, ``02`` (dùng chung với M9 ``qa_validate``)."""


def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def to_decimal(tok: str) -> Decimal | None:
    try:
        return Decimal(tok.replace(".", "").replace(",", ".")).normalize()
    except InvalidOperation:  # pragma: no cover - NUM_RE chỉ khớp chữ số
        return None


def parse_numbers(text: str) -> set[Decimal]:
    """Số trong văn bản tiếng Việt: ``400.000`` = 400000, ``0,25`` = 0.25, ``02`` = 2."""
    out: set[Decimal] = set()
    for m in NUM_RE.finditer(nfc(text)):
        d = to_decimal(m.group(0))
        if d is not None:
            out.add(d)
    return out


def as_decimal(v: int | float | str | Decimal) -> Decimal:
    return Decimal(str(v)).normalize()


def dec_str(d: Decimal) -> str:
    """Decimal → chuỗi không mũ: ``8E+5`` → ``800000``, ``0.25`` → ``0.25``."""
    return format(d.normalize(), "f")


def format_int_vn(n: int) -> str:
    """``1000000`` → ``1.000.000``."""
    return f"{n:,}".replace(",", ".")


def format_count(n: int) -> str:
    """Số tháng/điểm viết như văn bản gốc: ``2`` → ``02``, ``12`` → ``12``."""
    return f"{n:02d}"


# --------------------------------------------------------------------------- bảng con số

FactKind = Literal["phat_tien", "tuoc_quyen", "dinh_chi", "tru_diem", "thoi_han", "van_ban"]
SANCTION_EDGES = ("BI_XU_PHAT", "BI_TRU_DIEM")
NUMERIC_LABELS = ("CheTai", "DiemGPLX", "BienPhapBoSung")


class NumberFact(BaseModel):
    """Một con số được phép dùng trong câu trả lời (mã ``N#``)."""

    model_config = ConfigDict(extra="forbid")
    id: str
    kind: FactKind
    values: list[str]
    """Giá trị số (Decimal dạng chuỗi): ``[min, max]`` với khung, ``[v]`` với số đơn."""
    unit: str | None = None
    rendered: str
    """Chuỗi thay vào câu trả lời."""
    description: str
    """Nghĩa của con số (hiển thị cho LLM)."""
    source: str
    """``S#`` của nguồn chứa con số."""
    unit_id: str
    """Unit nêu con số (``stated_in``)."""
    version_id: str | None = None
    node_id: str | None = None
    """Nút ``CheTai``/``DiemGPLX``/``BienPhapBoSung`` (``None`` với số trong text)."""
    applies_to: list[str] = Field(default_factory=list)
    """Unit hành vi (trong nguồn) nối tới chế tài bằng ``BI_XU_PHAT``/``BI_TRU_DIEM``."""
    span: str
    """Nguyên văn trong văn bản."""


@dataclass(frozen=True)
class SourceText:
    """Phần của một nguồn mà bảng con số cần: mã ``S#``, text chunk, các phiên bản trong chunk,
    ngày dùng để lọc cạnh chế tài (as_of nếu chunk phủ ngày đó, ngược lại ngày bắt đầu chunk)."""

    sid: str
    text: str
    version_ids: tuple[str, ...]
    edge_as_of: date | None


def _num_props(n: GraphNode) -> tuple[FactKind, list[int], str | None, str, str] | None:
    """(kind, giá trị, đơn vị, chuỗi hiển thị, mô tả) của một nút có con số; ``None`` nếu nút
    không mang số (phạt cảnh cáo, tịch thu, biện pháp không thời hạn)."""
    p = n.props
    if n.label == "CheTai":
        loai = p.get("loai")
        who = p.get("doi_tuong")
        if loai == "phat_tien" and p.get("min_vnd") is not None and p.get("max_vnd") is not None:
            a, b = int(p["min_vnd"]), int(p["max_vnd"])
            r = (
                f"{format_int_vn(a)} đồng"
                if a == b
                else f"từ {format_int_vn(a)} đồng đến {format_int_vn(b)} đồng"
            )
            desc = "Phạt tiền" + (f" (đối với {who})" if who else "")
            return "phat_tien", [a, b], "đồng", r, desc
        if loai in ("tuoc_quyen", "dinh_chi") and p.get("min_thang") is not None:
            a, b = int(p["min_thang"]), int(p.get("max_thang") or p["min_thang"])
            r = (
                f"{format_count(a)} tháng"
                if a == b
                else f"từ {format_count(a)} tháng đến {format_count(b)} tháng"
            )
            head = "Tước quyền sử dụng" if loai == "tuoc_quyen" else "Đình chỉ hoạt động"
            desc = f"{head} {who}" if who else head
            return loai, [a, b], "tháng", r, desc  # type: ignore[return-value]
        return None
    if n.label == "DiemGPLX" and p.get("so_diem") is not None:
        k = int(p["so_diem"])
        cond = p.get("dieu_kien")
        desc = "Trừ điểm giấy phép lái xe" + (f" ({cond})" if cond else "")
        return "tru_diem", [k], "điểm", f"{format_count(k)} điểm", desc
    if n.label == "BienPhapBoSung" and p.get("thoi_han"):
        th = str(p["thoi_han"])
        return (
            "thoi_han",
            sorted(int(x) for x in re.findall(r"\d+", th)),
            None,
            th,
            (f"Thời hạn thực hiện biện pháp: {p.get('name') or ''}".strip()),
        )
    return None


class NumberIndex:
    """Chỉ mục nút có con số theo ``version_id`` (dựng một lần cho cả run)."""

    def __init__(self, store: BaseGraphStore) -> None:
        self.store = store
        self.by_version: dict[str, list[GraphNode]] = {}
        for lab in NUMERIC_LABELS:
            for n in store.nodes_by_label(lab):
                vid = n.props.get("version_id")
                if vid:
                    self.by_version.setdefault(str(vid), []).append(n)
        for v in self.by_version.values():
            v.sort(key=lambda n: n.id)

    def stated_at(self, version_id: str) -> list[GraphNode]:
        return self.by_version.get(version_id, [])

    def linked_from(self, version_id: str, as_of: date | None) -> list[tuple[GraphNode, str]]:
        """Nút chế tài nối từ phiên bản hành vi (``BI_XU_PHAT``/``BI_TRU_DIEM`` đi ra)."""
        out = []
        for e in self.store.out_edges(version_id, types=list(SANCTION_EDGES), as_of=as_of):
            n = self.store.get_node(e.dst)
            if n is not None:
                out.append((n, e.type))
        return out


# Số không đưa vào bảng (phần b): nhãn/dẫn chiếu cấu trúc, số hiệu, ngày.
_STRUCT_WORDS = (
    r"(?:Điều|điều|Khoản|khoản|Điểm|điểm|Phụ lục|phụ lục|PHỤ LỤC|Mẫu số|mẫu số|Mẫu|mẫu|"
    r"Chương|chương|Mục|mục|Phần|phần|Biểu mẫu|biểu mẫu|số|Số|STT|TT)"
)
_REF_CHAIN_RE = re.compile(
    _STRUCT_WORDS + r"\s+\d+[a-zđ]?(?:\s*(?:,|và|hoặc|đến|tới|-|–)\s*\d+[a-zđ]?)*"
)
_SO_HIEU_RE = re.compile(r"\d+[a-zA-Z]?(?:/\d{2,4})?/[A-ZĐa-zđ0-9][A-ZĐa-zđ0-9\-–/]*")
_DATE_RES = (
    re.compile(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b"),
    re.compile(r"\b(\d{1,2})-(\d{1,2})-(\d{4})\b"),
    re.compile(r"ngày\s+(\d{1,2})\s+tháng\s+(\d{1,2})\s+năm\s+(\d{4})", re.I),
)
_MONTH_YEAR_RE = re.compile(r"tháng\s+(\d{1,2})\s*(?:/|năm)\s*(\d{4})", re.I)
_YEAR_RE = re.compile(r"\bnăm\s+(\d{4})\b", re.I)
_LINE_LABEL_RE = re.compile(r"^\s*\d+[a-zđ]?\.(?=\s)", re.M)
_UNIT_RE = re.compile(
    r"\s?(%|phần trăm|đồng|km/h|km/giờ|ki-lô-mét|km|mét|m|cm|mm|tấn|kg|lít|tuổi|tháng|ngày|"
    r"giờ|phút|giây|năm|điểm|người|chỗ|lần|mg/l|miligam|tầng|trục|bánh)(?![\wÀ-ỹ])"
)


def dates_in(text: str) -> set[date]:
    """Các ngày viết dạng ``01/01/2026``, ``01-01-2026``, ``ngày 01 tháng 01 năm 2026``."""
    out: set[date] = set()
    t = nfc(text)
    for rx in _DATE_RES:
        for m in rx.finditer(t):
            try:
                out.add(date(int(m.group(3)), int(m.group(2)), int(m.group(1))))
            except ValueError:
                continue
    return out


def _masked_spans(text: str) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    for rx in (_REF_CHAIN_RE, _SO_HIEU_RE, *_DATE_RES, _MONTH_YEAR_RE, _YEAR_RE, _LINE_LABEL_RE):
        spans += [(m.start(), m.end()) for m in rx.finditer(text)]
    return spans


def _inside(pos: tuple[int, int], spans: Iterable[tuple[int, int]]) -> bool:
    return any(a <= pos[0] and pos[1] <= b for a, b in spans)


def _snippet(text: str, start: int, end: int, before: int = 60, after: int = 30) -> str:
    a = max(0, start - before)
    b = min(len(text), end + after)
    if a > 0:
        sp = text.find(" ", a)
        a = sp + 1 if 0 <= sp < start else a
    if b < len(text):
        sp = text.rfind(" ", end, b)
        b = sp if sp > end else b
    s = text[a:start] + "⟦" + text[start:end] + "⟧" + text[end:b]
    s = re.sub(r"\s+", " ", s).strip()
    return ("…" if a > 0 else "") + s + ("…" if b < len(text) else "")


def text_numbers(text: str, exclude: Sequence[tuple[int, int]] = ()) -> list[tuple[str, str, str]]:
    """Số trong text (phần b): ``(chuỗi hiển thị, giá trị, đoạn ngữ cảnh)`` theo thứ tự xuất
    hiện, bỏ trùng chuỗi hiển thị."""
    t = nfc(text)
    masked = _masked_spans(t) + list(exclude)
    seen: set[str] = set()
    out: list[tuple[str, str, str]] = []
    for m in NUM_RE.finditer(t):
        s, e = m.start(), m.end()
        if _inside((s, e), masked):
            continue
        # bỏ số dính chữ (mã, ký hiệu: "B1", "2a", "QH15") — không phải đại lượng
        if (s > 0 and t[s - 1].isalpha()) or (e < len(t) and t[e].isalpha() and t[e] != "%"):
            continue
        d = to_decimal(m.group(0))
        if d is None:
            continue
        u = _UNIT_RE.match(t, e)
        end = u.end() if u else e
        rendered = t[s:end].strip()
        rendered = re.sub(r"\s+", " ", rendered)
        if rendered in seen:
            continue
        seen.add(rendered)
        out.append((rendered, dec_str(d), _snippet(t, s, end)))
    return out


def _node_fact(n: GraphNode, sid: str) -> NumberFact | None:
    got = _num_props(n)
    if got is None:
        return None
    kind, vals, unit, rendered, desc = got
    return NumberFact(
        id="",
        kind=kind,
        values=[dec_str(as_decimal(v)) for v in vals],
        unit=unit,
        rendered=rendered,
        description=desc,
        source=sid,
        unit_id=str(n.props.get("unit_id")),
        version_id=str(n.props.get("version_id")),
        node_id=n.id,
        span=str(n.props.get("span") or ""),
    )


def build_number_table(
    sources: Sequence[SourceText],
    index: NumberIndex,
    *,
    max_text_numbers_per_source: int = 25,
    text_chars_budget: int | None = None,
) -> list[NumberFact]:
    """Bảng con số cho các nguồn (thứ tự nguồn; trong một nguồn: nút đồ thị trước, số trong text
    sau). Một nút chế tài nối từ nhiều Điểm của cùng nguồn chỉ có một mã (``applies_to`` gộp).
    Nút đồ thị luôn có mặt; số trong text bị giới hạn ``max_text_numbers_per_source`` mỗi nguồn và
    tổng ``text_chars_budget`` ký tự (mô tả + giá trị) cho mọi nguồn, theo thứ tự nguồn."""
    facts: list[NumberFact] = []
    left = text_chars_budget
    for src in sources:
        local: dict[str, NumberFact] = {}
        stated: list[GraphNode] = []
        for vid in src.version_ids:
            stated.extend(index.stated_at(vid))
        for n in sorted(stated, key=lambda x: x.id):
            f = local.get(n.id) or _node_fact(n, src.sid)
            if f is not None:
                local[n.id] = f
        for vid in src.version_ids:
            behaviour = vid.split("@", 1)[0]
            for n, _et in index.linked_from(vid, src.edge_as_of):
                f = local.get(n.id) or _node_fact(n, src.sid)
                if f is None:
                    continue
                local[n.id] = f
                if behaviour not in f.applies_to:
                    f.applies_to.append(behaviour)
        # phần text đã là span của nút nêu tại nguồn → không lặp lại
        t = nfc(src.text)
        exclude: list[tuple[int, int]] = []
        for f in local.values():
            sp = nfc(f.span)
            i = t.find(sp) if sp else -1
            while i >= 0:
                exclude.append((i, i + len(sp)))
                i = t.find(sp, i + 1)
        facts.extend(local.values())
        for rendered, val, snip in text_numbers(t, exclude)[:max_text_numbers_per_source]:
            if left is not None:
                cost = len(snip) + len(rendered) + 16
                if cost > left:
                    break
                left -= cost
            m = _UNIT_RE.search(rendered)
            facts.append(
                NumberFact(
                    id="",
                    kind="van_ban",
                    values=[val],
                    unit=m.group(1) if m else None,
                    rendered=rendered,
                    description=snip,
                    source=src.sid,
                    unit_id="",
                    span=rendered,
                )
            )
    for i, f in enumerate(facts, 1):
        f.id = f"N{i}"
    return facts


# --------------------------------------------------------------------------- chỗ giữ chỗ

PLACEHOLDER_RE = re.compile(r"\{\s*(N\d+)\s*\}")


def placeholders(text: str) -> list[str]:
    """Mã ``N#`` dùng trong text, theo thứ tự, không trùng."""
    out: list[str] = []
    for m in PLACEHOLDER_RE.finditer(text):
        if m.group(1) not in out:
            out.append(m.group(1))
    return out


#: "{Na} đến {Nb}" (có thể chen đơn vị "{Na} tháng đến {Nb}", "tới", gạch nối) — hai mã nối thành
#: một khoảng.
JOIN_RE = re.compile(
    r"\{\s*(N\d+)\s*\}\s*(?:(?:đồng|tháng|điểm|ngày|năm)\s*)?(?:đến|tới|[-–])\s*\{\s*(N\d+)\s*\}"
)


def _same_value(a: str, b: str, table: Mapping[str, NumberFact]) -> bool:
    fa, fb = table.get(a), table.get(b)
    return a == b or (fa is not None and fb is not None and fa.rendered == fb.rendered)


def is_range(f: NumberFact | None) -> bool:
    """Giá trị đã là cả khung "từ X đến Y" (phạt tiền, tước quyền… có min ≠ max)."""
    return f is not None and f.rendered.startswith("từ ") and " đến " in f.rendered


def collapse_same_range(text: str, table: Mapping[str, NumberFact]) -> str:
    """M13 (17/11/2026): "từ {N1} đến {N1}" với N1 đã là khung "từ X đến Y" → "từ {N1}" (render
    thành một khung). Chỉ cùng một mã; hai mã khác nhau là ``khoang_ghep`` (verify)."""

    def sub(m: re.Match[str]) -> str:
        a, b = m.group(1), m.group(2)
        return "{" + a + "}" if _same_value(a, b, table) and is_range(table.get(a)) else m.group(0)

    return JOIN_RE.sub(sub, text)


def range_join_issues(text: str, table: Mapping[str, NumberFact]) -> list[NumberIssue]:
    """M13 (17/11/2026): hai mã **khác nhau** nối thành một khoảng mà ít nhất một mã đã là cả
    khung ("từ {N1} đến {N2}", N1 = khung cá nhân, N2 = khung tổ chức; hoặc "{N1} đến {N2}" với
    N2 = "04 điểm") — render kiểu gì cũng tạo khoảng không có trong văn bản ⇒ vi phạm con số."""
    out = []
    for m in JOIN_RE.finditer(text):
        a, b = m.group(1), m.group(2)
        fa, fb = table.get(a), table.get(b)
        if fa is None or fb is None or _same_value(a, b, table):
            continue
        if is_range(fa) or is_range(fb):
            out.append(
                NumberIssue(kind="khoang_ghep", text=m.group(0), start=m.start(), end=m.end())
            )
    return out


def render_numbers(text: str, table: Mapping[str, NumberFact]) -> str:
    """Thay ``{N#}`` bằng ``rendered``; mã không có trong bảng giữ nguyên (đã bị verify loại
    trước khi render). Không lặp chữ quanh chỗ giữ chỗ: "phạt tiền từ {N1}" với N1 = "từ X đồng
    đến Y đồng" → bỏ "từ" của giá trị; "{N2} điểm" với N2 = "02 điểm" → bỏ "điểm" của giá trị."""
    text = collapse_same_range(text, table)
    out: list[str] = []
    pos = 0
    for m in PLACEHOLDER_RE.finditer(text):
        before = text[pos : m.start()]
        f = table.get(m.group(1))
        if f is None:
            out += [before, m.group(0)]
            pos = m.end()
            continue
        val = f.rendered
        first, _, rest = val.partition(" ")
        if rest and re.search(rf"(?:^|\s){re.escape(first)}\s*$", before, re.I):
            val = rest
        after = text[m.end() :]
        head, _, last = val.rpartition(" ")
        if head and re.match(rf"\s*{re.escape(last)}(?![\wÀ-ỹ])", after, re.I):
            val = head
        out += [before, val]
        pos = m.end()
    out.append(text[pos:])
    return "".join(out)


# --------------------------------------------------------------------------- dò số tự do

IssueKind = Literal["chu_so", "ngay", "chu_viet", "ma_so_khong_ton_tai", "khoang_ghep"]


class NumberIssue(BaseModel):
    model_config = ConfigDict(extra="forbid")
    kind: IssueKind
    text: str
    start: int
    end: int


@dataclass
class AllowedNumbers:
    """Ngữ cảnh cho phép: số trong câu hỏi, ngày có căn cứ (câu hỏi, as_of, hiệu lực nguồn, ngày
    nêu trong nguồn)."""

    question_numbers: set[Decimal] = field(default_factory=set)
    dates: set[date] = field(default_factory=set)

    @property
    def years(self) -> set[int]:
        return {d.year for d in self.dates}

    @classmethod
    def build(
        cls, question: str, as_of: date | None, extra_dates: Iterable[date], texts: Iterable[str]
    ) -> AllowedNumbers:
        ds = set(extra_dates) | dates_in(question)
        if as_of is not None:
            ds.add(as_of)
        for t in texts:
            ds |= dates_in(t)
        return cls(parse_numbers(question), ds)


_NUM_WORDS = (
    r"(?:một|hai|ba|bốn|tư|năm|lăm|sáu|bảy|tám|chín|mười|mươi|mốt|linh|lẻ|trăm|nghìn|ngàn|"
    r"triệu|tỷ|tỉ|rưỡi)"
)
_NUM_WORD_HEAD = r"(?:một|hai|ba|bốn|năm|sáu|bảy|tám|chín|mười)"
"""Từ mở đầu một số viết bằng chữ ("tư", "lăm", "mươi"… chỉ đứng sau — "đầu tư đồng bộ" không
phải số)."""
_WORD_NUM_RE = re.compile(
    rf"(?<![\wÀ-ỹ]){_NUM_WORD_HEAD}(?:\s+{_NUM_WORDS})*\s+"
    r"(?:đồng|điểm|tháng|ngày|giờ|phút|tuổi|năm|km|ki-lô-mét|mét|tấn)(?![\wÀ-ỹ])",
    re.I,
)
_DOC_NUM_RE = re.compile(
    r"(?:Nghị định|nghị định|Thông tư|thông tư|Luật|luật|Quyết định|quyết định|NĐ|TT|QĐ)"
    r"(?:\s+số)?\s+\d+(?:/\d{4})?"
)


def find_unverified_numbers(text: str, allowed: AllowedNumbers) -> list[NumberIssue]:
    """Số trong ``text`` (văn bản LLM viết, còn nguyên ``{N#}``) không đến từ chỗ giữ chỗ và
    không thuộc ngữ cảnh cho phép."""
    t = nfc(text)
    # che chỗ giữ chỗ bằng ký tự không phải số, giữ vị trí
    t = PLACEHOLDER_RE.sub(lambda m: "§" * len(m.group(0)), t)
    issues: list[NumberIssue] = []
    covered: list[tuple[int, int]] = []

    def dated(d: date | None, s: int, e: int) -> None:
        covered.append((s, e))
        if d is None or d not in allowed.dates:
            issues.append(NumberIssue(kind="ngay", text=t[s:e], start=s, end=e))

    for rx in _DATE_RES:
        for m in rx.finditer(t):
            if _inside((m.start(), m.end()), covered):
                continue
            try:
                d: date | None = date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
            except ValueError:
                d = None
            dated(d, m.start(), m.end())
    for m in _MONTH_YEAR_RE.finditer(t):
        if _inside((m.start(), m.end()), covered):
            continue
        covered.append((m.start(), m.end()))
        mon, yr = int(m.group(1)), int(m.group(2))
        if not any(d.year == yr and d.month == mon for d in allowed.dates):
            issues.append(NumberIssue(kind="ngay", text=m.group(0), start=m.start(), end=m.end()))
    for m in _YEAR_RE.finditer(t):
        if _inside((m.start(), m.end()), covered):
            continue
        covered.append((m.start(), m.end()))
        if int(m.group(1)) not in allowed.years:
            issues.append(NumberIssue(kind="ngay", text=m.group(0), start=m.start(), end=m.end()))
    for rx in (_REF_CHAIN_RE, _SO_HIEU_RE, _DOC_NUM_RE):
        covered += [(m.start(), m.end()) for m in rx.finditer(t)]
    for m in NUM_RE.finditer(t):
        if _inside((m.start(), m.end()), covered):
            continue
        s0, e0 = m.start(), m.end()
        # chữ số dính chữ cái là mã/ký hiệu (hạng GPLX "A1", "C1E", "QH15"), không phải đại lượng
        if (s0 > 0 and t[s0 - 1].isalpha()) or (e0 < len(t) and t[e0].isalpha()):
            continue
        d = to_decimal(m.group(0))
        if d is not None and d in allowed.question_numbers:
            continue
        issues.append(NumberIssue(kind="chu_so", text=m.group(0), start=m.start(), end=m.end()))
    for m in _WORD_NUM_RE.finditer(t):
        issues.append(NumberIssue(kind="chu_viet", text=m.group(0), start=m.start(), end=m.end()))
    return sorted(issues, key=lambda i: (i.start, i.end))


def unknown_placeholders(text: str, table: Mapping[str, NumberFact]) -> list[NumberIssue]:
    return [
        NumberIssue(kind="ma_so_khong_ton_tai", text=m.group(0), start=m.start(), end=m.end())
        for m in PLACEHOLDER_RE.finditer(text)
        if m.group(1) not in table
    ]


_SENT_END_RE = re.compile(r"[.!?;]+(?=\s|$)|\n")


def split_sentences(text: str) -> list[tuple[int, int]]:
    """Khoảng ``[start, end)`` của từng câu: kết thúc bằng ``. ! ? ;`` đứng trước khoảng trắng /
    cuối chuỗi, hoặc xuống dòng (dấu chấm trong ``900.000`` không phải ranh giới câu)."""
    out: list[tuple[int, int]] = []
    s = 0
    for m in _SENT_END_RE.finditer(text):
        out.append((s, m.end()))
        s = m.end()
    if s < len(text):
        out.append((s, len(text)))
    return [(a, b) for a, b in out if text[a:b].strip()]


def drop_sentences(text: str, issues: Sequence[NumberIssue]) -> tuple[str, int]:
    """Bỏ các câu chứa vị trí vi phạm. Trả (text, số câu bị bỏ)."""
    if not issues:
        return text, 0
    kept: list[str] = []
    dropped = 0
    for s, e in split_sentences(text):
        if any(s <= i.start < e for i in issues):
            dropped += 1
            continue
        kept.append(text[s:e])
    out = re.sub(r"[ \t]+", " ", "".join(kept)).strip()
    return out, dropped


__all__ = [
    "NUM_RE",
    "AllowedNumbers",
    "NumberFact",
    "NumberIndex",
    "NumberIssue",
    "PLACEHOLDER_RE",
    "SourceText",
    "as_decimal",
    "build_number_table",
    "dates_in",
    "dec_str",
    "drop_sentences",
    "find_unverified_numbers",
    "format_count",
    "format_int_vn",
    "parse_numbers",
    "placeholders",
    "render_numbers",
    "split_sentences",
    "text_numbers",
    "to_decimal",
    "unknown_placeholders",
    "range_join_issues",
    "collapse_same_range",
    "is_range",
]
