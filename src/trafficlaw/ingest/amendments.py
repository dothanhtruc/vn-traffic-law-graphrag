"""Nhận diện chỉ dẫn sửa đổi trong văn bản sửa đổi (M4) → danh sách :class:`Instruction`.

Đầu vào là unit của văn bản sửa đổi (``units.jsonl``, M3 giữ khối trích dẫn trong ``text`` của
unit chứa câu sửa đổi). Hàm thuần; câu không chắc chắn → :class:`Todo`, **không đoán**.

Các bước cho mỗi Điều của văn bản sửa đổi:

1. **Văn bản đích**: số hiệu nêu trong tiêu đề Điều ("Sửa đổi, bổ sung một số điều của Nghị
   định số 151/2024/NĐ-CP…") khớp một đích ``SUA_DOI`` trong danh mục; tiêu đề không nêu số hiệu
   → đích duy nhất của văn bản. Số hiệu ngoài danh mục → bỏ qua cả Điều (todo ``ngoai_danh_muc``).
2. **Kế thừa ngữ cảnh** Điều → Khoản → Điểm: câu dẫn của nhóm ("Sửa đổi, bổ sung một số điểm,
   khoản của Điều 6", "…một số điểm của khoản 5 như sau:") chỉ đặt ngữ cảnh; câu con ("Sửa đổi,
   bổ sung điểm m khoản 3 như sau:") lấy Điều/Khoản còn thiếu từ ngữ cảnh.
3. **Câu sửa đổi** (dòng đầu của unit, bỏ nhãn): xem :func:`parse_sentence`.
4. **Nội dung mới**: các dòng sau câu dẫn (hoặc phần sau "như sau:" trên cùng dòng), bỏ ngoặc
   mở đầu khối và ngoặc đóng khối cuối dòng (``”.``/``".``). Khối được tách theo **nhãn của
   đích** theo đúng thứ tự (đích ``khoản 2, khoản 3`` → khối bắt đầu bằng ``2.`` rồi ``3.``);
   nhãn không khớp → todo ``nhan_khong_khop``. Bên trong khối, Khoản/Điểm con được tách lại
   bằng nhãn có kiểm tra thứ tự (như M3).
"""

from __future__ import annotations

import contextlib
import re
import unicodedata
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict

from trafficlaw.ingest.refs import (
    SELF,
    Ref,
    RefContext,
    RefError,
    common_context,
    header_context,
    normalize,
    parse_refs,
)
from trafficlaw.ingest.structure import DIEM_ALPHABET, Unit
from trafficlaw.registry.loader import Registry
from trafficlaw.registry.schema import DocumentMeta
from trafficlaw.utils.ids import make_appendix_id, make_unit_id, parse_unit_id, roman_to_int

OpKind = Literal[
    "replace",  # Sửa đổi (, bổ sung) X như sau
    "replace_title",  # Sửa đổi tên Điều/khoản
    "insert",  # Bổ sung X (vào sau/trước Y)
    "repeal",  # Bãi bỏ X
    "replace_phrase",  # Thay thế cụm từ A bằng cụm từ B tại …
    "remove_phrase",  # Bỏ / Bãi bỏ cụm từ A tại …
    "insert_phrase",  # Bổ sung cụm từ A vào sau/trước cụm từ B tại …
    "replace_appendix",  # Thay thế Phụ lục X bằng Phụ lục Y kèm theo văn bản này
    "add_appendix",  # Bổ sung Phụ lục X … bằng Phụ lục Y kèm theo văn bản này
]

TodoReason = Literal[
    "mau_khong_ro",  # câu không khớp mẫu nào / dẫn chiếu không đọc được
    "ngoai_danh_muc",  # sửa văn bản (hoặc do văn bản) ngoài danh mục
    "sua_van_ban_sua_doi",  # sửa/bãi bỏ chính văn bản sửa đổi
    "khong_xac_dinh_van_ban",  # Điều không nêu văn bản đích, văn bản có nhiều đích
    "thieu_noi_dung",  # câu sửa đổi/bổ sung không có khối nội dung
    "nhan_khong_khop",  # nhãn trong khối nội dung khác nhãn của đích
    "mau_phu_luc",  # sửa Mẫu trong Phụ lục (không có unit riêng)
    "khong_tim_thay_dich",
    "khong_tim_thay_phu_luc",
    "dich_da_ton_tai",
    "dich_da_bai_bo",
    "khong_tim_thay_cum_tu",
    "khac_cap",  # khối nội dung khác cấp với đích
    "hieu_luc_khong_ro",
    "hieu_luc_sua_doi",  # chỉ dẫn sửa Điều hiệu lực của văn bản đích (cần rà tay)
    "xung_dot_ngay",
    "thay_the_mot_phan",
]


class Block(BaseModel):
    """Nội dung mới dạng cây (một Điều/Khoản/Điểm/Phụ lục và các unit con)."""

    model_config = ConfigDict(extra="forbid")

    id: str
    level: str
    number: str | None = None
    title: str | None = None
    text: str
    children: list[Block] = []


class Instruction(BaseModel):
    """Một thao tác trên **một** unit đích."""

    model_config = ConfigDict(extra="forbid")

    source_unit_id: str
    seq: int
    target_doc: str
    op: OpKind
    target_id: str
    block: Block | None = None
    after_id: str | None = None
    before_id: str | None = None
    old: str | None = None
    new: str | None = None
    where: Literal["after", "before"] | None = None
    part: Literal["title", "can_cu"] | None = None
    source_appendix_id: str | None = None
    effective_from: date | None = None
    sentence: str


class Todo(BaseModel):
    """Một dòng ``amendment_todo.csv``."""

    model_config = ConfigDict(extra="forbid")

    doc_id: str | None
    unit_id: str | None = None
    source_unit_id: str | None = None
    reason: TodoReason
    detail: str


class LabelFix(BaseModel):
    """Sửa nhãn ghi sai trong **khối nội dung** của văn bản sửa đổi (người dùng duyệt).

    ``data/registry/amendment_overrides.yaml``: chỉ đổi nhãn đầu dòng ``label_in_source`` →
    ``label`` ở đúng một dòng của unit ``source_unit_id`` bắt đầu bằng ``text_starts_with``
    (sau nhãn). Không khớp đúng một dòng → báo ``unapplied``.
    """

    model_config = ConfigDict(extra="forbid")

    source_unit_id: str
    label_in_source: str
    label: str
    text_starts_with: str
    reason: str
    evidence: str


@dataclass
class Extraction:
    instructions: list[Instruction]
    todos: list[Todo]
    #: Mục sửa nhãn không áp được (source_unit_id).
    fixes_unapplied: list[str] = field(default_factory=list)


def apply_label_fixes(
    lines: list[str], fixes: Sequence[LabelFix]
) -> tuple[list[str], list[LabelFix]]:
    """Đổi nhãn theo ``fixes``; trả về (dòng mới, các mục không khớp đúng một dòng)."""
    out = list(lines)
    bad: list[LabelFix] = []
    for f in fixes:
        lab = re.escape(f.label_in_source)
        pat = re.compile(rf"^(?:{lab}\)|{lab}\.)\s*" + re.escape(normalize(f.text_starts_with)))
        hits = [i for i, ln in enumerate(out) if pat.match(normalize(ln))]
        if len(hits) != 1:
            bad.append(f)
            continue
        i = hits[0]
        out[i] = re.sub(rf"^{lab}(?=[.)])", f.label, out[i])
    return out, bad


# ---------------------------------------------------------------- câu dẫn

_VERB = re.compile(r"^(?:Sửa\s+đổi|Bổ\s+sung|Bãi\s+bỏ|Thay\s+thế|Bỏ)(?![\wÀ-ỹ])")
_NHU_SAU = re.compile(r"\s*(?:như\s+sau)?\s*[:.;]?\s*$")
_LABEL_PREFIX = re.compile(r"^(?:\d+[a-z]?\.|[a-zđ]\d*\))\s*")
_DIEU_HEAD = re.compile(r"^Điều\s+(\d+[a-z]?)\s*\.\s*(.*)$")
_Q = r"[“\"]([^”\"]*)[”\"]"
_DATE = re.compile(r"ngày\s+(\d{1,2})\s+tháng\s+(\d{1,2})\s+năm\s+(\d{4})")


def is_instruction(lead: str) -> bool:
    return bool(_VERB.match(normalize(lead)))


def _clean_lead(s: str) -> str:
    s = normalize(s)
    return _NHU_SAU.sub("", s).strip()


# ---------------------------------------------------------------- khối trích dẫn


def strip_quote_block(lines: Sequence[str]) -> list[str]:
    """Bỏ ngoặc mở khối ở đầu dòng và ngoặc đóng khối ở cuối dòng; giữ ngoặc bên trong câu.

    Ngoặc đóng khối = ngoặc đưa độ sâu về 0 ở cuối dòng (sau nó chỉ còn ``.;,``). Dòng mở
    lại không có ngoặc mở (lỗi bản gốc, ND241 Đ10 K8) vẫn được giữ làm nội dung.
    """
    out: list[str] = []
    depth = 0
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if depth == 0 and line[:1] in '“"':
            line = line[1:].lstrip()
            depth = 1
        # Quét phần còn lại để biết ngoặc cuối dòng có đóng khối không.
        d = depth
        close_at: int | None = None
        for i, ch in enumerate(line):
            if ch == "“" or (ch == '"' and d == 0):
                d += 1
            elif ch in '”"':
                if d <= 1:
                    close_at = i
                d = max(d - 1, 0)
        tail_ok = close_at is not None and not line[close_at + 1 :].strip(" .;,")
        if tail_ok and close_at is not None and (depth >= 1 or d == 0):
            line = line[:close_at].rstrip()
            depth = 0
        else:
            depth = 1 if d > 0 or depth else 0
        if line:
            out.append(line)
    return out


_K_LINE = re.compile(r"^(\d+[a-z]?)\.\s*\S")
_D_LINE = re.compile(r"^([a-zđ]\d*)\)\s*\S")


def _num_key(num: str) -> tuple[int, str]:
    m = re.match(r"(\d+)([a-z]?)", num)
    assert m
    return int(m[1]), m[2]


def _diem_key(label: str) -> tuple[int, int]:
    return DIEM_ALPHABET.index(label[0]), int(label[1:] or 0)


def _label_re(level: str, label: str) -> re.Pattern[str]:
    if level == "dieu":
        return re.compile(rf"^Điều\s+{re.escape(label)}\s*\.")
    if level == "khoan":
        return re.compile(rf"^{re.escape(label)}\.(?:\s|$)")
    if level == "diem":
        return re.compile(rf"^{re.escape(label)}\)(?:\s|$)")
    raise ValueError(level)


def split_by_labels(
    lines: Sequence[str], level: str, labels: Sequence[str]
) -> list[list[str]] | None:
    """Tách ``lines`` thành len(labels) khối, khối i bắt đầu bằng dòng mang nhãn ``labels[i]``."""
    if not lines:
        return None
    pats = [_label_re(level, lb) for lb in labels]
    if not pats[0].match(lines[0]):
        return None
    blocks: list[list[str]] = [[lines[0]]]
    for line in lines[1:]:
        j = len(blocks)
        if j < len(pats) and pats[j].match(line):
            blocks.append([line])
        else:
            blocks[-1].append(line)
    return blocks if len(blocks) == len(labels) else None


def build_block(unit_id: str, level: str, lines: Sequence[str]) -> Block:
    """Dựng cây cho khối nội dung (dòng đầu là dòng của chính unit)."""
    uid = parse_unit_id(unit_id)
    number = uid.diem if level == "diem" else uid.khoan if level == "khoan" else uid.dieu
    title = None
    if level == "dieu" and (m := _DIEU_HEAD.match(lines[0])):
        title = m[2] or None
    root = Block(id=unit_id, level=level, number=number, title=title, text=lines[0])
    own: list[str] = [lines[0]]
    cur_k: Block | None = None
    cur_d: Block | None = None
    own_k: list[str] = []
    own_d: list[str] = []
    prev_k: tuple[int, str] | None = None
    prev_d: tuple[int, int] | None = None

    def close_d() -> None:
        nonlocal cur_d
        if cur_d is not None:
            cur_d.text = "\n".join(own_d)
        cur_d = None

    def close_k() -> None:
        nonlocal cur_k
        close_d()
        if cur_k is not None:
            cur_k.text = "\n".join(own_k)
        cur_k = None

    for line in lines[1:]:
        mk = _K_LINE.match(line) if level == "dieu" else None
        md = _D_LINE.match(line) if level in ("dieu", "khoan") else None
        if mk and (prev_k is None or _num_key(mk[1]) > prev_k):
            close_k()
            prev_k, prev_d = _num_key(mk[1]), None
            cur_k = Block(
                id=make_unit_id(uid.doc_code, uid.dieu, mk[1]),
                level="khoan",
                number=mk[1],
                text="",
            )
            root.children.append(cur_k)
            own_k = [line]
            continue
        if md and md[1][0] in DIEM_ALPHABET and (prev_d is None or _diem_key(md[1]) > prev_d):
            close_d()
            prev_d = _diem_key(md[1])
            k = cur_k.number if cur_k is not None else uid.khoan
            cur_d = Block(
                id=make_unit_id(uid.doc_code, uid.dieu, k, md[1]),
                level="diem",
                number=md[1],
                text="",
            )
            (cur_k if cur_k is not None else root).children.append(cur_d)
            own_d = [line]
            continue
        if cur_d is not None:
            own_d.append(line)
        elif cur_k is not None:
            own_k.append(line)
        else:
            own.append(line)
    close_k()
    root.text = "\n".join(own)
    return root


# ---------------------------------------------------------------- văn bản đích

_SO_HIEU = re.compile(
    r"(?:Bộ\s+luật|Luật|Nghị\s+định|Thông\s+tư|Quyết\s+định)\s+(?:số\s*:?\s*)?"
    r"(\d+/\d{4}/[A-Za-zĐđ0-9\-]+)"
)


def _norm_so_hieu(s: str) -> str:
    return unicodedata.normalize("NFC", s).strip().rstrip(".,;").upper()


@dataclass(frozen=True)
class DocResolver:
    """Đối chiếu số hiệu ↔ ``doc_id`` cho một văn bản sửa đổi."""

    amending: DocumentMeta
    targets: tuple[str, ...]  # doc_id các đích SUA_DOI
    by_so_hieu: Mapping[str, str]  # số hiệu (chuẩn hoá) → doc_id, toàn danh mục

    @classmethod
    def build(cls, amending: DocumentMeta, registry: Registry) -> DocResolver:
        targets = tuple(r.target for r in amending.relations if r.type == "SUA_DOI")
        by = {_norm_so_hieu(d.so_hieu): d.doc_id for d in registry if d.so_hieu}
        return cls(amending, targets, by)

    def doc_of(self, so_hieu: str) -> str | None:
        return self.by_so_hieu.get(_norm_so_hieu(so_hieu))


# ---------------------------------------------------------------- câu sửa đổi


@dataclass
class _Ctx:
    target: str  # doc_id đích
    refs: RefContext


@dataclass
class _Sink:
    resolver: DocResolver
    effective: Mapping[str, date]  # unit_id văn bản sửa đổi → ngày hiệu lực riêng
    default_date: date | None
    instructions: list[Instruction]
    todos: list[Todo]
    seq: int = 0

    def date_for(self, source_unit_id: str) -> date | None:
        u: str | None = source_unit_id
        while u:
            if u in self.effective:
                return self.effective[u]
            p = parse_unit_id(u).parent()
            u = None if p is None else str(p)
        return self.default_date

    def add(self, **kw: object) -> None:
        self.seq += 1
        src = str(kw["source_unit_id"])
        self.instructions.append(
            Instruction(seq=self.seq, effective_from=self.date_for(src), **kw)  # type: ignore[arg-type]
        )

    def todo(
        self,
        reason: TodoReason,
        detail: str,
        *,
        doc_id: str | None,
        source_unit_id: str | None,
        unit_id: str | None = None,
    ) -> None:
        self.todos.append(
            Todo(
                doc_id=doc_id,
                unit_id=unit_id,
                source_unit_id=source_unit_id,
                reason=reason,
                detail=detail[:500],
            )
        )


def _ref_doc_ok(ref: Ref, ctx: _Ctx, sink: _Sink) -> str | None:
    """Lý do bỏ qua nếu dẫn chiếu trỏ ra ngoài văn bản đích (None = hợp lệ)."""
    if ref.doc is None:
        return None
    if ref.doc == SELF:
        return "mau_khong_ro"  # "Nghị định này" trong câu sửa văn bản khác: không rõ ý
    doc = sink.resolver.doc_of(ref.doc)
    if doc == ctx.target:
        return None
    if doc is None:
        return "ngoai_danh_muc"
    return "sua_van_ban_sua_doi"


def _resolve_targets(
    refs: Sequence[Ref], ctx: _Ctx, sink: _Sink, src: str, sentence: str
) -> list[tuple[Ref, str]] | None:
    out: list[tuple[Ref, str]] = []
    for r in refs:
        bad = _ref_doc_ok(r, ctx, sink)
        if bad:
            sink.todo(bad, sentence, doc_id=ctx.target, source_unit_id=src)  # type: ignore[arg-type]
            return None
        if r.mau is not None:
            sink.todo("mau_phu_luc", sentence, doc_id=ctx.target, source_unit_id=src)
            continue
        out.append((r, r.unit_id(ctx.target)))
    return out


# Thay thế cụm từ A bằng cụm từ B tại LOC  |  Thay thế cụm từ A tại LOC bằng cụm từ B
_REPL1 = re.compile(
    rf"^Thay\s+thế\s+(?:các\s+)?cụm\s+từ\s*{_Q}\s*bằng\s+cụm\s+từ\s*{_Q}\s*(?:tại\s*:?)?\s*(.+)$"
)
_REPL2 = re.compile(
    rf"^Thay\s+thế\s+(?:các\s+)?cụm\s+từ\s*{_Q}\s*tại\s*:?\s*(.+?)\s*bằng\s+cụm\s+từ\s*{_Q}$"
)
_INS_PHRASE = re.compile(
    rf"^Bổ\s+sung\s+cụm\s+từ\s*{_Q}\s*(?:vào\s+)?(sau|trước)\s+(?:cụm\s+)?từ\s*{_Q}\s*tại\s*:?\s*(.+)$"
)
_REMOVE = re.compile(r"^(?:Bỏ|Bãi\s+bỏ)\s+(?:các\s+)?(?:cụm\s+)?từ\s*[“\"]")
_PHRASE_ITEM = re.compile(rf"(?:các\s+)?(?:cụm\s+)?từ\s*{_Q}")
_HAS_PHRASE = re.compile(r"(?:cụm\s+từ|(?<![\wÀ-ỹ])từ\s*[“\"])")
_APPX_REPLACE = re.compile(
    r"^Thay\s+thế\s+Phụ\s+lục\s+([IVXLC]+|\d+)\s+(?:ban\s+hành\s+|quy\s+định\s+tại\s+)?"
    r"(?:kèm\s+theo\s+)?(?:Nghị\s+định|Thông\s+tư)\s+số\s+(\S+?)\s+bằng\s+Phụ\s+lục\s+"
    r"([IVXLC]+|\d+)\s+(?:ban\s+hành\s+)?kèm\s+theo\s+(?:Nghị\s+định|Thông\s+tư)\s+này$"
)
_APPX_ADD = re.compile(
    r"^Bổ\s+sung\s+Phụ\s+lục\s+([IVXLC]+|\d+)\s+vào\s+(?:Nghị\s+định|Thông\s+tư)\s+số\s+(\S+?)\s+"
    r"bằng\s+Phụ\s+lục\s+([IVXLC]+|\d+)\s+(?:ban\s+hành\s+)?kèm\s+theo\s+(?:Nghị\s+định|Thông\s+tư)\s+này$"
)
_REPEAL_LIST = re.compile(
    r"^Bãi\s+bỏ\s+các\s+điều,\s*khoản,\s*điểm,\s*cụm\s+từ\s+sau\s+của\s+"
    r"(?:Nghị\s+định|Thông\s+tư|Luật)\s+số\s+(\S+?)\s*:\s*(.+)$"
)
_REPEAL = re.compile(r"^Bãi\s+bỏ\s+(.+)$")
_WHOLE_DIEU = re.compile(r"^một\s+số\s+[^\d]*?của\s+Điều\s+(\d+[a-z]?)$")
_REPLACE = re.compile(r"^Sửa\s+đổi(?:,?\s+bổ\s+sung)?\s+(tên\s+)?(.+)$")
_INSERT = re.compile(r"^Bổ\s+sung\s+(.+?)(?:\s+vào\s+(?:(sau|trước)\s+)?(.+))?$")


def _pl(raw: str) -> str:
    return str(int(raw)) if raw.isdigit() else str(roman_to_int(raw))


def _parse_loc(
    loc: str, ctx: _Ctx, sink: _Sink, src: str, sentence: str
) -> list[tuple[Ref, str]] | None:
    try:
        refs = parse_refs(loc.strip().rstrip("."), ctx.refs)
    except RefError as e:
        sink.todo("mau_khong_ro", f"{sentence} ({e})", doc_id=ctx.target, source_unit_id=src)
        return None
    return _resolve_targets(refs, ctx, sink, src, sentence)


def _phrase_ops(sentence: str, ctx: _Ctx, sink: _Sink, src: str) -> None:
    s = sentence
    if m := _REPL1.match(s):
        old, new, loc = m[1], m[2], m[3]
    elif m := _REPL2.match(s):
        old, loc, new = m[1], m[2], m[3]
    else:
        old = new = loc = None
    if loc is not None:
        targets = _parse_loc(loc, ctx, sink, src, s)
        for r, uid in targets or ():
            sink.add(
                source_unit_id=src,
                target_doc=ctx.target,
                op="replace_phrase",
                target_id=uid,
                old=old,
                new=new,
                part=r.part,
                sentence=s,
            )
        return
    if m := _INS_PHRASE.match(s):
        added, where, anchor, loc = m[1], m[2], m[3], m[4]
        targets = _parse_loc(loc, ctx, sink, src, s)
        for r, uid in targets or ():
            sink.add(
                source_unit_id=src,
                target_doc=ctx.target,
                op="insert_phrase",
                target_id=uid,
                old=anchor,
                new=added,
                where="after" if where == "sau" else "before",
                part=r.part,
                sentence=s,
            )
        return
    if _REMOVE.match(s):
        items = list(_PHRASE_ITEM.finditer(s))
        segs: list[tuple[str, str]] = []
        for i, it in enumerate(items):
            end = items[i + 1].start() if i + 1 < len(items) else len(s)
            loc = s[it.end() : end].strip()
            loc = re.sub(r"^tại\s*:?\s*", "", loc)
            loc = re.sub(r"\s*(?:,|;|và)\s*$", "", loc).strip()
            if not loc:
                sink.todo("mau_khong_ro", s, doc_id=ctx.target, source_unit_id=src)
                return
            segs.append((it[1], loc))
        for phrase, loc in segs:
            targets = _parse_loc(loc, ctx, sink, src, s)
            for r, uid in targets or ():
                sink.add(
                    source_unit_id=src,
                    target_doc=ctx.target,
                    op="remove_phrase",
                    target_id=uid,
                    old=phrase,
                    part=r.part,
                    sentence=s,
                )
        return
    sink.todo("mau_khong_ro", s, doc_id=ctx.target, source_unit_id=src)


def _content_ops(
    op: Literal["replace", "replace_title", "insert"],
    refs: list[tuple[Ref, str]],
    content: list[str],
    ctx: _Ctx,
    sink: _Sink,
    src: str,
    sentence: str,
    after_id: str | None = None,
    before_id: str | None = None,
) -> None:
    if not content:
        sink.todo("thieu_noi_dung", sentence, doc_id=ctx.target, source_unit_id=src)
        return
    levels = {r.level for r, _ in refs}
    if len(levels) != 1:
        sink.todo("mau_khong_ro", f"{sentence} (nhiều cấp)", doc_id=ctx.target, source_unit_id=src)
        return
    level = levels.pop()
    if level not in ("dieu", "khoan", "diem"):
        sink.todo("mau_khong_ro", sentence, doc_id=ctx.target, source_unit_id=src)
        return
    if op == "replace_title":
        if len(refs) != 1:
            sink.todo("mau_khong_ro", sentence, doc_id=ctx.target, source_unit_id=src)
            return
        r, uid = refs[0]
        number = r.dieu if level == "dieu" else r.khoan if level == "khoan" else r.diem
        if split_by_labels(content, level, [number or ""]) is None:
            sink.todo(
                "nhan_khong_khop", sentence, doc_id=ctx.target, source_unit_id=src, unit_id=uid
            )
            return
        block = Block(id=uid, level=level, number=number, text="\n".join(content))
        sink.add(
            source_unit_id=src,
            target_doc=ctx.target,
            op="replace_title",
            target_id=uid,
            block=block,
            sentence=sentence,
        )
        return
    labels = [
        (r.dieu if level == "dieu" else r.khoan if level == "khoan" else r.diem) or ""
        for r, _ in refs
    ]
    parts = split_by_labels(content, level, labels)
    if parts is None:
        sink.todo(
            "nhan_khong_khop",
            f"{sentence} (nhãn đích {labels}, khối bắt đầu {content[0][:40]!r})",
            doc_id=ctx.target,
            source_unit_id=src,
            unit_id=refs[0][1],
        )
        return
    prev_after = after_id
    for (_r, uid), lines in zip(refs, parts, strict=True):
        block = build_block(uid, level, lines)
        sink.add(
            source_unit_id=src,
            target_doc=ctx.target,
            op=op,
            target_id=uid,
            block=block,
            after_id=prev_after if op == "insert" else None,
            before_id=before_id if op == "insert" else None,
            sentence=sentence,
        )
        if op == "insert" and before_id is None:
            prev_after = uid


def parse_sentence(sentence: str, content: list[str], ctx: _Ctx, sink: _Sink, src: str) -> None:
    """Một câu sửa đổi (đã bỏ nhãn) + khối nội dung → chỉ dẫn hoặc todo."""
    s = _clean_lead(sentence)
    if _HAS_PHRASE.search(s) and not _REPEAL_LIST.match(s):
        _phrase_ops(s, ctx, sink, src)
        return
    if re.search(r"(?i)mẫu\s+số", s) and not _REPEAL_LIST.match(s):
        sink.todo("mau_phu_luc", s, doc_id=ctx.target, source_unit_id=src)
        return
    for pat, op in ((_APPX_REPLACE, "replace_appendix"), (_APPX_ADD, "add_appendix")):
        if m := pat.match(s):
            if sink.resolver.doc_of(m[2]) != ctx.target:
                sink.todo("ngoai_danh_muc", s, doc_id=ctx.target, source_unit_id=src)
                return
            sink.add(
                source_unit_id=src,
                target_doc=ctx.target,
                op=op,
                target_id=make_appendix_id(ctx.target, _pl(m[1])),
                source_appendix_id=make_appendix_id(sink.resolver.amending.doc_id, _pl(m[3])),
                sentence=s,
            )
            return
    if re.search(r"Phụ\s+lục", s) and not _REPEAL_LIST.match(s):
        sink.todo("mau_phu_luc", s, doc_id=ctx.target, source_unit_id=src)
        return
    if m := _REPEAL_LIST.match(s):
        if sink.resolver.doc_of(m[1]) != ctx.target:
            sink.todo("ngoai_danh_muc", s, doc_id=ctx.target, source_unit_id=src)
            return
        for item in (x.strip() for x in m[2].rstrip(".").split(";")):
            if not item:
                continue
            if _HAS_PHRASE.search(item):
                parse_sentence("Bãi bỏ " + item, [], ctx, sink, src)
            elif re.search(r"Mẫu\s+số|Phụ\s+lục", item):
                sink.todo("mau_phu_luc", f"Bãi bỏ {item}", doc_id=ctx.target, source_unit_id=src)
            else:
                targets = _parse_loc(item, ctx, sink, src, s)
                for _r, uid in targets or ():
                    sink.add(
                        source_unit_id=src,
                        target_doc=ctx.target,
                        op="repeal",
                        target_id=uid,
                        sentence=s,
                    )
        return
    if m := _REPEAL.match(s):
        targets = _parse_loc(m[1], ctx, sink, src, s)
        for _r, uid in targets or ():
            sink.add(
                source_unit_id=src, target_doc=ctx.target, op="repeal", target_id=uid, sentence=s
            )
        return
    if m := _REPLACE.match(s):
        whole = _WHOLE_DIEU.match(m[2])
        if whole and content and _label_re("dieu", whole[1]).match(content[0]):
            # "Sửa đổi, bổ sung một số điểm, khoản của Điều 33" kèm toàn văn Điều 33.
            uid = make_unit_id(ctx.target, whole[1])
            _content_ops("replace", [(Ref(dieu=whole[1]), uid)], content, ctx, sink, src, s)
            return
        targets = _parse_loc(m[2], ctx, sink, src, s)
        if targets:
            op = "replace_title" if m[1] else "replace"
            _content_ops(op, targets, content, ctx, sink, src, s)
        return
    if m := _INSERT.match(s):
        anchor_txt = m[3]
        after_id = before_id = None
        refs_ctx = ctx.refs
        if anchor_txt:
            anchors = _parse_loc(anchor_txt, ctx, sink, src, s)
            if anchors is None:
                return
            if len(anchors) != 1:
                sink.todo("mau_khong_ro", s, doc_id=ctx.target, source_unit_id=src)
                return
            ar, aid = anchors[0]
            if m[2] == "sau":
                after_id = aid
                refs_ctx = RefContext(dieu=ar.dieu, khoan=ar.khoan if ar.diem else None)
            elif m[2] == "trước":
                before_id = aid
                refs_ctx = RefContext(dieu=ar.dieu, khoan=ar.khoan if ar.diem else None)
            else:  # "vào khoản 3", "vào Điều 5": đích là đơn vị cha
                refs_ctx = RefContext(dieu=ar.dieu, khoan=ar.khoan)
        targets = _parse_loc(m[1], _Ctx(ctx.target, refs_ctx), sink, src, s)
        if targets:
            _content_ops("insert", targets, content, ctx, sink, src, s, after_id, before_id)
        return
    sink.todo("mau_khong_ro", s, doc_id=ctx.target, source_unit_id=src)


# ---------------------------------------------------------------- duyệt văn bản


def _split_unit(u: Unit) -> tuple[str, list[str], str | None]:
    """→ (câu dẫn, khối nội dung, tiêu đề Điều nếu câu dẫn nằm ở thân Điều)."""
    lines = [ln for ln in u.text.split("\n") if ln.strip()]
    if not lines:
        return "", [], None
    if u.level == "dieu":
        title = u.title or ""
        body = lines[1:]
        if body and body[0][:1] not in '“"' and is_instruction(body[0]):
            lead, rest, header = body[0], body[1:], title
        else:
            lead, rest, header = title, body, None
    else:
        lead, rest, header = _LABEL_PREFIX.sub("", lines[0]), lines[1:], None
    m = re.search(r"như\s+sau\s*:\s*(\S.*)$", lead)
    if m:
        rest = [m[1], *rest]
        lead = lead[: m.start()]
    return lead, strip_quote_block(rest), header


def extract_instructions(
    amending: DocumentMeta,
    units: Sequence[Unit],
    registry: Registry,
    effective: Mapping[str, date] | None = None,
    label_fixes: Sequence[LabelFix] = (),
) -> Extraction:
    """Chỉ dẫn sửa đổi của một văn bản sửa đổi (``units`` theo thứ tự trong văn bản).

    ``effective``: ngày hiệu lực riêng của unit trong chính văn bản sửa đổi (từ Điều hiệu lực);
    mặc định dùng ``amending.hieu_luc_tu``.
    """
    resolver = DocResolver.build(amending, registry)
    sink = _Sink(resolver, effective or {}, amending.hieu_luc_tu, [], [])
    fixes_by_unit: dict[str, list[LabelFix]] = {}
    for f in label_fixes:
        fixes_by_unit.setdefault(f.source_unit_id, []).append(f)
    unapplied: list[str] = []
    children: dict[str, list[Unit]] = {}
    for u in units:
        if u.parent_id:
            children.setdefault(u.parent_id, []).append(u)

    def kids(u: Unit) -> list[Unit]:
        return [c for c in children.get(u.id, []) if c.level in ("khoan", "diem")]

    def visit(u: Unit, ctx: _Ctx) -> None:
        lead, content, header = _split_unit(u)
        sub = kids(u)
        if header is not None:
            ctx = _Ctx(ctx.target, header_context(header, ctx.refs))
        if not is_instruction(lead):
            for c in sub:
                visit(c, ctx)
            return
        sub_instr = [c for c in sub if is_instruction(_split_unit(c)[0])]
        if sub_instr and not content:
            hctx = header_context(lead, ctx.refs)
            if hctx == RefContext() or "một số" not in lead:
                with contextlib.suppress(RefError):
                    hctx = common_context(
                        parse_refs(_clean_lead(_strip_verb(lead)), ctx.refs), hctx
                    )
            for c in sub:
                visit(c, _Ctx(ctx.target, hctx))
            return
        if u.id in fixes_by_unit:
            content, bad = apply_label_fixes(content, fixes_by_unit.pop(u.id))
            unapplied.extend(f.source_unit_id for f in bad)
        parse_sentence(lead, content, ctx, sink, u.id)
        for c in sub:
            visit(c, ctx)

    for u in units:
        if u.level != "dieu":
            continue
        title = u.title or ""
        lead, _content, _header = _split_unit(u)
        looks_amending = (
            is_instruction(title)
            or is_instruction(lead)
            or any(is_instruction(_split_unit(c)[0]) for c in kids(u))
        )
        if not looks_amending:
            continue
        target = _target_of(title, resolver)
        if target is None:
            m = _SO_HIEU.search(title)
            if m and is_instruction(title):
                reason: TodoReason = (
                    "ngoai_danh_muc" if resolver.doc_of(m[1]) is None else "sua_van_ban_sua_doi"
                )
                sink.todo(reason, title, doc_id=None, source_unit_id=u.id)
                continue
            if len(resolver.targets) == 1:
                target = resolver.targets[0]
            else:
                sink.todo("khong_xac_dinh_van_ban", title, doc_id=None, source_unit_id=u.id)
                continue
        visit(u, _Ctx(target, RefContext()))
    unapplied.extend(fixes_by_unit)  # unit không có hoặc không phải câu sửa đổi
    return Extraction(sink.instructions, sink.todos, unapplied)


def _strip_verb(lead: str) -> str:
    s = normalize(lead)
    s = re.sub(r"^(?:Sửa\s+đổi(?:,?\s+bổ\s+sung)?|Bổ\s+sung|Bãi\s+bỏ|Thay\s+thế|Bỏ)\s+", "", s)
    return re.sub(r"\s+và\s+bổ\s+sung\s+", ", ", s)


def _target_of(title: str, resolver: DocResolver) -> str | None:
    m = _SO_HIEU.search(normalize(title))
    if not m:
        return None
    doc = resolver.doc_of(m[1])
    return doc if doc in resolver.targets else None


def parse_vn_date_in(text: str) -> date | None:
    m = _DATE.search(text)
    return date(int(m[3]), int(m[2]), int(m[1])) if m else None
