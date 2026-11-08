"""Tìm và phân giải dẫn chiếu trong câu văn xuôi (M5, quan hệ ``DAN_CHIEU``/``HUONG_DAN``).

Hàm thuần. Cụm dẫn chiếu được đọc bằng :func:`trafficlaw.ingest.refs.parse_refs` (M4); module
này chỉ (1) **tìm span** trong câu, (2) thay "Điều này/khoản này/điểm này" bằng số theo ngữ
cảnh, (3) gắn văn bản được nhắc ngay sau span.

**Span** bắt đầu ở một *neo*: ``điểm <nhãn>``, ``khoản <số>``, ``Điều <số>``, ``Phụ lục <số>``
(số La Mã hoặc Ả Rập), ``Mẫu số N`` đứng trước ``Phụ lục``, hoặc ``điểm/khoản/Điều này``.
Neo **phải có số/nhãn hoặc "này" ngay sau**, nên "Điều khiển", "điểm kiểm tra", "trừ điểm
giấy phép" không phải neo; "thời điểm này", "địa điểm này"… cũng bị loại. Span mở rộng qua:

- neo tiếp theo, số/nhãn trần sau dấu nối (``khoản 1, 2 và 6``, ``điểm a, b``);
- dấu nối ``,`` ``và`` ``hoặc`` ``;`` — chỉ khi ngay sau là neo hoặc số/nhãn trần;
- khoảng ``đến|tới`` (``từ khoản 1 đến khoản 3`` → khoản 1, 2, 3; ``điểm a đến điểm đ``);
- từ nối ``của`` / ``tại`` / ``thuộc`` / ``quy định tại`` / ``(ban hành) kèm theo`` khi ngay sau
  là neo hoặc tên văn bản;
- **tên văn bản** (:class:`DocNameTable`) — kết thúc span; áp cho mọi mục trong span.

Trong span, ``;`` được đọc như ``,``: Điều đứng cuối áp cho mọi nhóm đứng trước
("điểm a khoản 2; khoản 7; điểm b khoản 9 Điều này"). Nhóm cuối không có Điều → Điều chứa câu.

**Ngữ cảnh** lấy từ mã unit nguồn: "Điều này" → Điều chứa nguồn, "khoản này" → Khoản chứa
nguồn, "điểm này" → Điểm nguồn; mục thiếu Điều/Khoản (``khoản 3``, ``điểm c``) → Điều/Khoản
chứa nguồn — **chỉ khi** span không nhắc văn bản khác (span nhắc văn bản khác mà thiếu Điều →
lỗi, không đoán).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, replace
from typing import Literal

from trafficlaw.graph.doc_names import DocMention, DocNameTable
from trafficlaw.ingest.refs import RefContext, RefError, parse_refs
from trafficlaw.utils.ids import make_appendix_id, parse_unit_id

DocKind = Literal["self", "registry", "external"]

_W = r"[\wÀ-ỹ]"
_END = rf"(?!{_W})"
_NUM = r"\d+[a-z]?"
_LABEL = r"[a-zđ]\d*"
_ROMAN = r"[IVXLC]+"

_ANCHOR = re.compile(
    rf"(?<!{_W})(?:các\s+)?(?:"
    rf"(?P<diem>[đĐ]iểm)\s+(?:(?P<diem_n>{_LABEL})|(?P<diem_self>này)){_END}"
    rf"|(?P<khoan>[kK]hoản)\s+(?:(?P<khoan_n>{_NUM})|(?P<khoan_self>này)){_END}"
    rf"|(?P<dieu>[đĐ]iều)\s+(?:(?P<dieu_n>{_NUM})|(?P<dieu_self>này)){_END}"
    rf"|(?P<pl>[pP]hụ\s+lục)\s+(?:số\s+)?(?:{_ROMAN}|\d+){_END}"
    rf"|(?P<mau>[mM]ẫu)\s+số\s+\d+[a-z]?{_END}"
    rf"(?=\s+(?:(?:tại|của|thuộc)\s+)?[pP]hụ\s+lục\s+(?:số\s+)?(?:{_ROMAN}|\d+){_END})"
    rf")"
)
# Từ đứng trước "điểm này" không phải dẫn chiếu: "thời điểm này", "địa điểm này"…
_NOT_DIEM_PREV = frozenset(
    [
        "thời",
        "địa",
        "đặc",
        "quan",
        "trọng",
        "ưu",
        "nhược",
        "giao",
        "mốc",
        "tụ",
        "cực",
        "bến",
        "giám",
        "xuất",
    ]
)
_BARE_NUM = re.compile(rf"\s*({_NUM}){_END}")
_BARE_LABEL = re.compile(rf"\s*({_LABEL}){_END}")
_JOIN = re.compile(r"\s*(?:,|;|\bvà\b|\bhoặc\b)\s*")
_RANGE = re.compile(r"\s+(?:đến|tới)\s+")
_FILLER = re.compile(
    r"\s+(?:quy\s+định\s+tại|của|tại|thuộc|(?:được\s+)?ban\s+hành\s+kèm\s+theo|kèm\s+theo)\s+"
)
_DOC_GAP = re.compile(r"\s+")
_PAREN = re.compile(r"\s*\(([^()\n]{1,300})\)")
_TRU = re.compile(r"\s*trừ\s+")


@dataclass(frozen=True)
class SourceContext:
    """Unit chứa câu: dùng cho "Điều này/khoản này" và mục thiếu Điều/Khoản."""

    doc_id: str
    dieu: str | None = None
    khoan: str | None = None
    diem: str | None = None

    @classmethod
    def from_unit_id(cls, unit_id: str) -> SourceContext:
        u = parse_unit_id(unit_id)
        return cls(u.doc_code, u.dieu, u.khoan, u.diem)


@dataclass(frozen=True)
class RawSpan:
    start: int
    end: int
    text: str
    #: Phần dẫn chiếu (không gồm tên văn bản).
    refs_text: str
    mention: DocMention | None


@dataclass(frozen=True)
class Reference:
    """Một dẫn chiếu đã phân giải (hoặc lỗi).

    - ``unit_ids`` rỗng + ``error`` None → dẫn chiếu cấp văn bản.
    - ``doc_kind == "external"`` → ``unit_ids`` luôn rỗng, ``ref_text`` giữ cụm Điều/Khoản.
    """

    start: int
    end: int
    text: str
    doc_kind: DocKind
    #: ``doc_id`` hoặc ``EXT:…``.
    doc: str
    unit_ids: tuple[str, ...] = ()
    ref_text: str | None = None
    error: str | None = None
    mention: DocMention | None = None


# ------------------------------------------------------------------ tìm span


def _is_anchor(m: re.Match[str], text: str) -> bool:
    if m["diem"] is not None:
        prev = re.search(rf"({_W}+)\s+$", text[: m.start("diem")])
        if prev and prev[1].lower() in _NOT_DIEM_PREV:
            return False
    return True


def _anchor_at(text: str, pos: int) -> re.Match[str] | None:
    m = _ANCHOR.match(text, pos)
    return m if m and _is_anchor(m, text) else None


def _kind(m: re.Match[str]) -> str:
    for k in ("diem", "khoan", "dieu", "pl", "mau"):
        if m[k] is not None:
            return k
    raise AssertionError(m[0])


def _is_self(m: re.Match[str]) -> bool:
    return any(m[k] is not None for k in ("diem_self", "khoan_self", "dieu_self"))


def _bare_at(text: str, pos: int, kind: str) -> re.Match[str] | None:
    """Số/nhãn trần tiếp nối danh sách cùng loại: nhãn sau "điểm", số sau "khoản"/"Điều"."""
    pat = _BARE_LABEL if kind == "diem" else _BARE_NUM if kind in ("khoan", "dieu") else None
    return pat.match(text, pos) if pat else None


def _ref_like(inner: str) -> bool:
    """Ngoặc chứa dẫn chiếu: "(điểm a khoản 4; …)", "(trừ điểm a khoản 3, …)"."""
    s = inner.strip()
    t = _TRU.match(s)
    return _anchor_at(s, t.end() if t else 0) is not None


def _continues(text: str, pos: int, names: DocNameTable) -> bool:
    """Sau ``pos`` cụm dẫn chiếu còn tiếp (neo sau dấu nối/khoảng trắng, hoặc tên văn bản)."""
    for sep in (_JOIN, _DOC_GAP):
        if (j := sep.match(text, pos)) and _anchor_at(text, j.end()):
            return True
    if (f := _FILLER.match(text, pos)) and (
        _anchor_at(text, f.end()) or names.match_at(text, f.end())
    ):
        return True
    return bool((g := _DOC_GAP.match(text, pos)) and names.match_at(text, g.end()))


def find_spans(text: str, names: DocNameTable) -> list[RawSpan]:
    """Các span dẫn chiếu trong ``text`` theo thứ tự, không chồng nhau."""
    out: list[RawSpan] = []
    pos = 0
    while (m := _ANCHOR.search(text, pos)) is not None:
        if not _is_anchor(m, text):
            pos = m.end()
            continue
        start, end, kind = m.start(), m.end(), _kind(m)
        mention: DocMention | None = None
        done = _is_self(m)  # "Điều/khoản/điểm này" kết thúc span (văn bản chứa câu)
        while not done:
            nxt: re.Match[str] | None = None
            # Dấu nối (",", "và", "hoặc", ";", "đến") → neo hoặc số/nhãn trần cùng loại;
            # chỉ khoảng trắng → chỉ nhận neo ("điểm b khoản 5 Điều 6", "Mẫu số 01 Phụ lục II").
            for sep, allow_bare in ((_JOIN, True), (_RANGE, True), (_DOC_GAP, False)):
                if j := sep.match(text, end):
                    nxt = _anchor_at(text, j.end())
                    if nxt is not None:
                        kind, done = _kind(nxt), _is_self(nxt)
                        break
                    nxt = _bare_at(text, j.end(), kind) if allow_bare else None
                    if nxt is not None:
                        break
            if nxt is not None:
                end = nxt.end()
                continue
            # Ngoặc đơn: chứa dẫn chiếu ("Điều 13 (điểm a khoản 4; …)") hoặc chỉ giải thích
            # ("khoản 1 Điều 56 (đối với xe ô tô), khoản 2 Điều 56 (…) của Luật …") khi cụm
            # dẫn chiếu còn tiếp sau ngoặc.
            if (p := _PAREN.match(text, end)) and (
                _ref_like(p[1]) or _continues(text, p.end(), names)
            ):
                end = p.end()
                continue
            if f := _FILLER.match(text, end):
                if a := _anchor_at(text, f.end()):
                    end, kind, done = a.end(), _kind(a), _is_self(a)
                    continue
                if mn := names.match_at(text, f.end()):
                    mention = mn
                    break
            if (g := _DOC_GAP.match(text, end)) and (mn := names.match_at(text, g.end())):
                mention = mn
            break
        refs_text = text[start:end]
        span_end = mention.end if mention else end
        out.append(RawSpan(start, span_end, text[start:span_end], refs_text, mention))
        pos = span_end
    return out


# ------------------------------------------------------------------ phân giải

_DIEM_ALPHABET = [
    "a",
    "b",
    "c",
    "d",
    "đ",
    "e",
    "g",
    "h",
    "i",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "x",
    "y",
]
_RANGE_EXPAND = re.compile(
    rf"(điểm|khoản|điều)\s+({_NUM}|{_LABEL})\s+(?:đến|tới)\s+(?:(?:\1)\s+)?({_NUM}|{_LABEL}){_END}",
    re.I,
)


def _expand_ranges(s: str) -> str:
    def repl(m: re.Match[str]) -> str:
        kind, a, b = m[1], m[2].lower(), m[3].lower()
        if kind.lower() == "điểm":
            if a in _DIEM_ALPHABET and b in _DIEM_ALPHABET:
                i, j = _DIEM_ALPHABET.index(a), _DIEM_ALPHABET.index(b)
                if i < j:
                    return f"{kind} " + ", ".join(_DIEM_ALPHABET[i : j + 1])
        elif a.isdigit() and b.isdigit() and int(a) < int(b) <= int(a) + 200:
            return f"{kind} " + ", ".join(str(x) for x in range(int(a), int(b) + 1))
        return f"{kind} {a}, {b}"

    return _RANGE_EXPAND.sub(repl, s)


_DIEU_PAREN = re.compile(rf"((?:các\s+)?[đĐ]iều\s+{_NUM})\s*\(\s*(?!trừ)([^()]*)\)")
_ANY_PAREN = re.compile(r"\s*\([^()]*\)")


def _normalize_parens(s: str) -> str:
    """ "Điều 13 (điểm a khoản 4; điểm a khoản 6)" → "điểm a khoản 4; điểm a khoản 6 Điều 13";
    ngoặc khác (giải thích, "trừ …") bị bỏ — dẫn chiếu là tới đơn vị đứng ngoài ngoặc.
    """
    s = _DIEU_PAREN.sub(
        lambda m: f"{m[2].strip()} {m[1]}" if _anchor_at(m[2].strip(), 0) else m[0], s
    )
    return _ANY_PAREN.sub("", s)


_SELF_WORD = re.compile(r"(?<![\wÀ-ỹ])(điểm|khoản|điều)\s+này(?![\wÀ-ỹ])", re.I)


def _replace_self(s: str, ctx: SourceContext) -> str:
    def repl(m: re.Match[str]) -> str:
        kind = m[1].lower()
        val = {"điểm": ctx.diem, "khoản": ctx.khoan, "điều": ctx.dieu}[kind]
        if val is None:
            raise RefError(f"'{m[0]}' nhưng nguồn không nằm trong {kind} nào")
        return f"{m[1]} {val}"

    return _SELF_WORD.sub(repl, s)


@dataclass(frozen=True)
class DocScope:
    """Văn bản mặc định cho dẫn chiếu không nêu văn bản trong cây con của một câu dẫn.

    ``reason``: ``sua_doi`` ("Sửa đổi, bổ sung một số điều của Nghị định số 100/2019/NĐ-CP")
    hoặc ``huong_dan`` (Điều 1 "… quy định chi tiết … Luật X bao gồm:").
    """

    doc_kind: DocKind
    doc: str
    reason: Literal["sua_doi", "huong_dan"]
    source_unit_id: str


def resolve_span(span: RawSpan, ctx: SourceContext, scope: DocScope | None = None) -> Reference:
    """Span → :class:`Reference` (mã unit theo văn bản được nhắc, hoặc văn bản chứa câu).

    Trong ``scope`` (cây con của câu dẫn sửa đổi/hướng dẫn văn bản khác), span không nêu văn
    bản hoặc nêu "… này" thuộc văn bản của ``scope``; "Điều/khoản/điểm này" khi đó không xác
    định được (nằm trong nội dung trích dẫn của văn bản khác) → lỗi.
    """
    mention = span.mention
    doc_kind: DocKind
    if mention is None or mention.kind == "self":
        doc_kind, doc = (scope.doc_kind, scope.doc) if scope else ("self", ctx.doc_id)
    elif mention.kind == "registry" and mention.doc == ctx.doc_id:
        doc_kind, doc = "self", ctx.doc_id
    else:
        doc_kind, doc = mention.kind, mention.doc or ""
    base = dict(start=span.start, end=span.end, text=span.text, doc_kind=doc_kind, doc=doc)
    if doc_kind == "external":
        return Reference(**base, ref_text=span.refs_text, mention=mention)  # type: ignore[arg-type]
    try:
        if doc != ctx.doc_id and _SELF_WORD.search(span.refs_text):
            raise RefError("'… này' trong câu thuộc phạm vi văn bản khác")
        s = _replace_self(_normalize_parens(span.refs_text), ctx)
        s = _expand_ranges(s).replace(";", ",")
        rctx = RefContext(ctx.dieu, ctx.khoan) if doc_kind == "self" else RefContext()
        ids: list[str] = []
        for r in parse_refs(s, rctx):
            # Mẫu nằm trong Phụ lục, không có unit riêng → Phụ lục chứa nó.
            uid = make_appendix_id(doc, r.appendix) if r.mau and r.appendix else r.unit_id(doc)
            if uid not in ids:
                ids.append(uid)
    except (RefError, ValueError) as e:
        err = str(e)
        return Reference(**base, ref_text=span.refs_text, error=err, mention=mention)  # type: ignore[arg-type]
    return Reference(**base, unit_ids=tuple(ids), ref_text=span.refs_text, mention=mention)  # type: ignore[arg-type]


def _strip_heading(text: str) -> int:
    """Độ dài tiêu đề của chính unit ở đầu text (``Điều 9.`` / ``PHỤ LỤC I``) cần bỏ qua."""
    m = re.match(r"(?:Điều\s+\d+[a-z]?\.|PHỤ\s+LỤC\b[^\n]*|Phụ\s+lục\s+(?:số\s+)?\S+[^\n]*)", text)
    return m.end() if m else 0


_SOFT_BREAK = re.compile(r"\n(?=[a-zđà-ỹ])")


def _prepare(text: str) -> str:
    """Bỏ tiêu đề của chính unit; nối dòng bị ngắt giữa câu (dòng sau viết thường).

    Giữ nguyên độ dài để vị trí span khớp text gốc.
    """
    skip = _strip_heading(text)
    return _SOFT_BREAK.sub(" ", " " * skip + text[skip:])


def extract_references(
    text: str, source_unit_id: str, names: DocNameTable, scope: DocScope | None = None
) -> list[Reference]:
    """Mọi dẫn chiếu trong text một phiên bản: span (cấp unit) + văn bản nhắc riêng (cấp văn bản).

    Lần nhắc văn bản không nằm trong span nào → dẫn chiếu cấp văn bản (bỏ "… này" và chính
    văn bản nguồn).
    """
    ctx = SourceContext.from_unit_id(source_unit_id)
    body = _prepare(text)
    out: list[Reference] = []
    covered: list[tuple[int, int]] = []
    for sp in find_spans(body, names):
        out.append(resolve_span(sp, ctx, scope))
        covered.append((sp.start, sp.end))
    for mn in names.find_all(body):
        if any(a <= mn.start < b for a, b in covered):
            continue
        if mn.kind == "self" or mn.doc == ctx.doc_id:
            continue
        out.append(
            Reference(
                start=mn.start,
                end=mn.end,
                text=mn.text,
                doc_kind=mn.kind,
                doc=mn.doc or "",
                mention=mn,
            )
        )
    out.sort(key=lambda r: r.start)
    return out


# ------------------------------------------------------------------ phạm vi văn bản

_GUIDE_TRIGGER = re.compile(
    r"quy\s+định\s+chi\s+tiết|hướng\s+dẫn\s+(?:thi\s+hành|thực\s+hiện)", re.I
)
_AMEND_HEAD = re.compile(
    r"^[ 	]*(?:Điều\s+\d+[a-z]?\.\s*|\d+[a-z]?\.\s*|[a-zđ]\d*\)\s*)?"
    r"(?:Sửa\s+đổi|Bổ\s+sung|Bãi\s+bỏ|Thay\s+thế)[^\n]*?(?:của|tại)\s+",
    re.M,
)


def _other_mentions(line: str, doc_id: str, names: DocNameTable) -> list[DocMention]:
    return [mn for mn in names.find_all(line) if mn.kind != "self" and mn.doc != doc_id]


def header_scope(text: str, unit_id: str, names: DocNameTable) -> DocScope | None:
    """Câu dẫn của unit đặt văn bản mặc định cho cây con của nó (xem :class:`DocScope`).

    - ``sua_doi``: một dòng bắt đầu bằng "Sửa đổi|Bổ sung|Bãi bỏ|Thay thế … của|tại <văn bản
      khác>" (sau nhãn Điều/Khoản/Điểm) → văn bản đầu tiên được nhắc trên dòng đó.
    - ``huong_dan``: dòng có "quy định chi tiết|hướng dẫn thi hành", kết thúc bằng ":" và sau
      cụm đó nhắc **đúng một** văn bản khác (ND151 Đ1 "… thi hành Luật Trật tự, an toàn giao
      thông đường bộ bao gồm:"); nhắc hai văn bản (ND165 Đ1) → không đặt phạm vi.
    """
    doc_id = unit_id.split("/")[0]
    body = _prepare(text)
    for m in _AMEND_HEAD.finditer(body):
        line_end = body.find("\n", m.start())
        line = body[m.start() : line_end if line_end >= 0 else len(body)]
        others = _other_mentions(line, doc_id, names)
        if others:
            mn = others[0]
            return DocScope(mn.kind, mn.doc or "", "sua_doi", unit_id)
    for line in body.split("\n"):
        trig = _GUIDE_TRIGGER.search(line)
        if trig is None or not line.rstrip().endswith(":"):
            continue
        if _other_mentions(line[: trig.start()], doc_id, names):
            continue
        others = _other_mentions(line[trig.end() :], doc_id, names)
        if len({mn.doc for mn in others}) == 1:
            mn = others[0]
            return DocScope(mn.kind, mn.doc or "", "huong_dan", unit_id)
    return None


# ------------------------------------------------------------------ hướng dẫn, ủy quyền


def guidance_references(text: str, source_unit_id: str, names: DocNameTable) -> list[Reference]:
    """Dẫn chiếu tới văn bản **được hướng dẫn** trong phần mở đầu / Điều 1.

    Xét từng dòng: bỏ dòng "Căn cứ …"; dòng phải có cụm "quy định chi tiết" / "hướng dẫn thi
    hành|thực hiện", và trước cụm đó không nhắc văn bản khác (nếu có thì đó là trích yếu của
    văn bản được nhắc, vd "Nghị định số 151/2024/NĐ-CP … quy định chi tiết … Luật …"). Lấy các
    dẫn chiếu tới văn bản khác đứng sau cụm, tới hết dòng.
    """
    ctx = SourceContext.from_unit_id(source_unit_id)
    body = _prepare(text)
    out: list[Reference] = []
    offset = 0
    for line in body.split("\n"):
        line_start = offset
        offset += len(line) + 1
        if re.match(r"\s*Căn\s+cứ", line):
            continue
        trig = _GUIDE_TRIGGER.search(line)
        if trig is None:
            continue
        if _other_mentions(line[: trig.start()], ctx.doc_id, names):
            continue
        tail = " " * trig.end() + line[trig.end() :]
        for ref in extract_references(tail, source_unit_id, names):
            if ref.doc_kind == "self":
                continue
            out.append(_shift(ref, line_start))
    return out


def _shift(ref: Reference, by: int) -> Reference:
    return replace(ref, start=ref.start + by, end=ref.end + by)


_UY_QUYEN = re.compile(
    r"(?P<co_quan>Chính\s+phủ|Thủ\s+tướng\s+Chính\s+phủ|Bộ\s+trưởng\s+Bộ\s+[^\n,.;:]+?)"
    r"\s+quy\s+định\s+chi\s+tiết\s+(?=(?:các\s+)?(?:[đĐ]iểm|[kK]hoản|[đĐ]iều)\s)"
)


@dataclass(frozen=True)
class Delegation:
    """Câu ủy quyền "<cơ quan> quy định chi tiết <REFS>" trong Luật."""

    co_quan: str
    ref: Reference


def delegations(text: str, source_unit_id: str, names: DocNameTable) -> list[Delegation]:
    """Câu ủy quyền trong text: dẫn chiếu phải đứng **ngay sau** "quy định chi tiết"."""
    ctx = SourceContext.from_unit_id(source_unit_id)
    out: list[Delegation] = []
    for m in _UY_QUYEN.finditer(text):
        spans = find_spans(" " * m.end() + text[m.end() :], names)
        if not spans or spans[0].start != m.end():
            continue
        ref = resolve_span(spans[0], ctx)
        if ref.error is None and ref.doc_kind == "self":
            out.append(Delegation(re.sub(r"\s+", " ", m["co_quan"]), ref))
    return out
