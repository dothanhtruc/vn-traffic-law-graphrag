"""Đọc cụm dẫn chiếu tiếng Việt ("điểm a, điểm b khoản 2, khoản 5 Điều 6") thành danh sách mã.

Hàm thuần, dùng ở M4 (đích của câu sửa đổi, câu hiệu lực) và M5 (quan hệ ``DAN_CHIEU``).

Quy tắc phân phối: đơn vị lớn hơn đứng **sau** áp cho các đơn vị nhỏ đứng trước nó.

- ``điểm a, điểm b khoản 2`` → ``K2/a``, ``K2/b``; ``điểm a khoản 1, khoản 3`` → ``K1/a``, ``K3``
  (khoản đầu tiên ngay sau danh sách điểm là khoản chứa chúng, các khoản sau là mục riêng).
- ``khoản 1, khoản 3 Điều 6; điểm a khoản 1 Điều 20`` → Điều đứng sau áp cho mọi mục đang chờ.
- Dấu ``;`` (hoặc hết chuỗi) kết thúc một cụm: mục còn thiếu Điều/Khoản lấy từ ngữ cảnh
  (:class:`RefContext`), ví dụ câu "Sửa đổi điểm m khoản 3" nằm trong Điều sửa đổi Điều 6.
- ``Nghị định số 165/2024/NĐ-CP`` gán văn bản cho mọi mục chưa có văn bản đứng trước nó;
  ``của Luật/Nghị định/Thông tư này`` → ``SELF``. Phần mô tả văn bản đứng sau (ngày, cơ quan,
  trích yếu) bị bỏ qua.
- Chữ không nhận diện được → :class:`RefError` (người gọi ghi todo, **không đoán**).
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, replace
from typing import Literal

from trafficlaw.utils.ids import make_appendix_id, make_unit_id, roman_to_int

SELF = "SELF"
"""Giá trị ``Ref.doc`` cho "văn bản này"."""

Part = Literal["title", "can_cu"]


class RefError(ValueError):
    """Cụm dẫn chiếu không đọc được chắc chắn."""


@dataclass(frozen=True)
class Ref:
    """Một mục dẫn chiếu. ``doc``: ``None`` (văn bản ngữ cảnh), :data:`SELF`, hoặc số hiệu."""

    dieu: str | None = None
    khoan: str | None = None
    diem: str | None = None
    doc: str | None = None
    #: ``title`` = "tên Điều/khoản"; ``can_cu`` = "phần căn cứ" (unit ``van_ban``).
    part: Part | None = None
    #: Số Phụ lục (Ả Rập) khi dẫn chiếu Phụ lục; ``mau`` = số Mẫu bên trong Phụ lục.
    appendix: str | None = None
    mau: str | None = None

    @property
    def level(self) -> str:
        if self.part == "can_cu":
            return "van_ban"
        if self.mau is not None:
            return "mau"
        if self.appendix is not None:
            return "phu_luc"
        if self.diem is not None:
            return "diem"
        if self.khoan is not None:
            return "khoan"
        return "dieu"

    def unit_id(self, doc_code: str) -> str:
        """Mã unit trong văn bản ``doc_code``; Mẫu không có mã riêng → ``RefError``."""
        if self.part == "can_cu":
            return doc_code
        if self.mau is not None:
            raise RefError("Mẫu trong Phụ lục không có mã unit riêng")
        if self.appendix is not None:
            return make_appendix_id(doc_code, self.appendix)
        if self.dieu is None:
            raise RefError("dẫn chiếu thiếu Điều")
        return make_unit_id(doc_code, self.dieu, self.khoan, self.diem)


@dataclass(frozen=True)
class RefContext:
    """Ngữ cảnh kế thừa cho mục thiếu Điều/Khoản (Điều → Khoản → Điểm)."""

    dieu: str | None = None
    khoan: str | None = None


_WS = re.compile(r"\s+")
_NUM = r"\d+[a-z]?"
_LABEL = r"[a-zđ]\d*"
_ROMAN = r"[IVXLC]+"
_END = r"(?![\wÀ-ỹ])"  # hết từ (không dính chữ cái/số tiếp theo)

_T_DIEM = re.compile(rf"(?:các\s+)?điểm\s+({_LABEL}){_END}", re.I)
_T_KHOAN = re.compile(rf"(?:các\s+)?khoản\s+({_NUM}){_END}", re.I)
_T_DIEU = re.compile(rf"(?:các\s+)?điều\s+({_NUM}){_END}", re.I)
_T_TITLE = re.compile(r"tên\s+", re.I)
_T_CAN_CU = re.compile(r"phần\s+căn\s+cứ" + _END, re.I)
_T_MAU = re.compile(rf"(?:các\s+)?mẫu\s+số\s+(\d+[a-z]?){_END}", re.I)
_T_PL = re.compile(rf"(?:các\s+)?phụ\s+lục\s+(?:số\s+)?({_ROMAN}|\d+){_END}", re.I)
_T_DOC = re.compile(
    r"(?:của\s+|tại\s+)?(?:Bộ\s+luật|Luật|Nghị\s+định|Thông\s+tư|Quyết\s+định)\s+"
    r"(?:số\s*:?\s*)?(\d+/\d{4}/[A-Za-zĐđ0-9\-]+)",
)
_T_SELF = re.compile(
    r"(?:của\s+|tại\s+)?(?:Bộ\s+luật|Luật|Nghị\s+định|Thông\s+tư|Quyết\s+định)\s+này" + _END,
    re.I,
)
_T_SEP = re.compile(r"(?:,|và|hoặc|;|:|\.)", re.I)
_T_FILLER = re.compile(
    r"(?:quy\s+định\s+tại|tại|của|thuộc|các|này|như\s+sau|(?:ban\s+hành\s+)?kèm\s+theo)" + _END,
    re.I,
)
# Mục tiếp nối trong danh sách số: ", 2", " và 6", ", khoản 3" (cùng loại).
_CONT_NUM = re.compile(rf"\s*(?:,|và|hoặc)\s*(?:(?:các\s+)?(khoản|điều)\s+)?({_NUM}){_END}", re.I)
_CONT_LABEL = re.compile(rf"\s*(?:,|và|hoặc)\s*(?:(?:các\s+)?(điểm)\s+)?({_LABEL}){_END}", re.I)


def normalize(s: str) -> str:
    return _WS.sub(" ", unicodedata.normalize("NFC", s)).strip()


def _num_list(
    text: str, pos: int, first: str, kind: str, cont: re.Pattern[str]
) -> tuple[list[str], int]:
    """Danh sách số/nhãn liền nhau cùng loại: ``khoản 1, 2 và 6``, ``điểm a, điểm b``."""
    items = [first.lower()]
    while True:
        m = cont.match(text, pos)
        if not m or (m[1] is not None and m[1].lower() != kind):
            break
        items.append(m[2].lower())
        pos = m.end()
    return items, pos


def parse_refs(text: str, ctx: RefContext | None = None) -> list[Ref]:
    """Đọc cụm dẫn chiếu; mục thiếu Điều/Khoản lấy từ ``ctx``.

    Không đọc được chắc chắn → :class:`RefError`.
    """
    ctx = ctx or RefContext()
    s = normalize(text)
    out: list[Ref] = []
    pend: list[Ref] = []  # mục đã có Khoản (± Điểm), chờ Điều
    pend_diem: list[tuple[str, Part | None]] = []  # Điểm chờ Khoản/Điều
    pend_mau: list[str] = []  # Mẫu chờ Phụ lục
    part: Part | None = None
    pos = 0

    def flush() -> None:
        nonlocal pend, pend_diem
        if pend_mau:
            raise RefError(f"Mẫu số không kèm Phụ lục: {s!r}")
        for r in pend:
            if ctx.dieu is None:
                raise RefError(f"thiếu Điều cho khoản {r.khoan}: {s!r}")
            out.append(replace(r, dieu=ctx.dieu))
        for d, p in pend_diem:
            if ctx.dieu is None:
                raise RefError(f"thiếu Điều cho điểm {d}: {s!r}")
            out.append(Ref(dieu=ctx.dieu, khoan=ctx.khoan, diem=d, part=p))
        pend, pend_diem = [], []

    while pos < len(s):
        if s[pos].isspace():
            pos += 1
            continue
        if m := _T_DOC.match(s, pos):
            flush()
            out[:] = [r if r.doc is not None else replace(r, doc=m[1]) for r in out]
            break  # phần còn lại là mô tả văn bản (ngày, cơ quan, trích yếu)
        if m := _T_SELF.match(s, pos):
            flush()
            out[:] = [r if r.doc is not None else replace(r, doc=SELF) for r in out]
            pos = m.end()
            continue
        if m := _T_TITLE.match(s, pos):
            part = "title"
            pos = m.end()
            continue
        if m := _T_CAN_CU.match(s, pos):
            out.append(Ref(part="can_cu"))
            pos = m.end()
            continue
        if m := _T_MAU.match(s, pos):
            pend_mau.append(m[1].lower())
            pos = m.end()
            continue
        if m := _T_PL.match(s, pos):
            pl = _pl_number(m[1])
            if pend_mau:
                out.extend(Ref(appendix=pl, mau=x) for x in pend_mau)
                pend_mau = []
            else:
                out.append(Ref(appendix=pl))
            pos = m.end()
            continue
        if m := _T_DIEM.match(s, pos):
            labels, pos = _num_list(s, m.end(), m[1], "điểm", _CONT_LABEL)
            pend_diem.extend((x, part) for x in labels)
            part = None
            continue
        if m := _T_KHOAN.match(s, pos):
            nums, pos = _num_list(s, m.end(), m[1], "khoản", _CONT_NUM)
            if pend_diem:
                pend.extend(Ref(khoan=nums[0], diem=d, part=p) for d, p in pend_diem)
                pend_diem = []
                rest = nums[1:]
            else:
                rest = nums
            pend.extend(Ref(khoan=n, part=part) for n in rest)
            part = None
            continue
        if m := _T_DIEU.match(s, pos):
            nums, pos = _num_list(s, m.end(), m[1], "điều", _CONT_NUM)
            if pend or pend_diem:
                out.extend(replace(r, dieu=nums[0]) for r in pend)
                out.extend(Ref(dieu=nums[0], diem=d, part=p) for d, p in pend_diem)
                pend, pend_diem = [], []
                rest = nums[1:]
            else:
                rest = nums
            out.extend(Ref(dieu=n, part=part) for n in rest)
            part = None
            continue
        if m := _T_SEP.match(s, pos):
            if m[0] == ";":
                flush()
            pos = m.end()
            continue
        if m := _T_FILLER.match(s, pos):
            pos = m.end()
            continue
        raise RefError(f"không đọc được dẫn chiếu tại {s[pos : pos + 30]!r} trong {s!r}")
    flush()
    if not out:
        raise RefError(f"không có dẫn chiếu: {s!r}")
    return out


def _pl_number(raw: str) -> str:
    return str(roman_to_int(raw.upper())) if not raw.isdigit() else str(int(raw))


_CTX_DIEU = re.compile(rf"(?<![\wÀ-ỹ])điều\s+({_NUM}){_END}", re.I)
_CTX_KHOAN = re.compile(rf"(?<![\wÀ-ỹ])khoản\s+({_NUM}){_END}", re.I)


def header_context(text: str, ctx: RefContext | None = None) -> RefContext:
    """Ngữ cảnh từ câu dẫn của một nhóm ("…một số điểm, khoản của Điều 6", "…của khoản 5").

    Lấy Điều nếu câu nhắc đúng một Điều; Khoản nếu câu nhắc đúng một Khoản. Câu nhắc tới
    văn bản khác (``… số 05/2003/NĐ-CP``) không tạo Điều/Khoản.
    """
    ctx = ctx or RefContext()
    s = normalize(text)
    s = _T_DOC.split(s)[0]  # bỏ phần mô tả văn bản
    dieus = {m[1].lower() for m in _CTX_DIEU.finditer(s)}
    khoans = {m[1].lower() for m in _CTX_KHOAN.finditer(s)}
    dieu = next(iter(dieus)) if len(dieus) == 1 else ctx.dieu
    if len(dieus) > 1:
        return RefContext()
    khoan = next(iter(khoans)) if len(khoans) == 1 else (ctx.khoan if not dieus else None)
    if len(khoans) > 1:
        khoan = None
    return RefContext(dieu=dieu, khoan=khoan)


def common_context(refs: list[Ref], ctx: RefContext | None = None) -> RefContext:
    """Ngữ cảnh chung của các mục (cùng Điều → Điều; cùng Khoản → Khoản)."""
    ctx = ctx or RefContext()
    dieus = {r.dieu for r in refs}
    if len(dieus) != 1 or None in dieus:
        return ctx
    dieu = next(iter(dieus))
    khoans = {r.khoan for r in refs}
    khoan = next(iter(khoans)) if len(khoans) == 1 else None
    return RefContext(dieu=dieu, khoan=khoan)
