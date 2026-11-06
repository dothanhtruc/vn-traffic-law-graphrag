"""M3: tách cấu trúc văn bản đã chuẩn hoá → các unit Phần/Chương/Mục/Điều/Khoản/Điểm/Phụ lục.

Hàm chính ``parse_structure(doc_id, text, source_path)`` là hàm thuần: nhận nội dung
``data/interim/<doc_id>.txt``, trả về danh sách ``Unit`` (theo thứ tự trong văn bản) và
``StructureReport``. Không suy luận sửa đổi (việc của M4).

Quy tắc chính (giải thích chi tiết trong PR M3):

1. **Tiêu đề** chỉ được nhận khi ở ngoài trích dẫn và trước điểm dừng phần thân. Dòng bảng
   (chứa ``" | "``) không bao giờ là tiêu đề.
2. **Thứ tự**: Điều mới phải là Điều trước + 1 hoặc cùng số kèm chữ cái lớn hơn (52 → 52a → 53);
   Khoản/Điểm kiểm tra tương tự trong cha của nó (Điểm theo bảng chữ cái a b c d đ e g h …).
   Dòng trông như tiêu đề nhưng sai thứ tự → ghép vào text của unit đang mở + ghi ``anomalies``.
3. **Trích dẫn** (văn bản sửa đổi): dòng bắt đầu bằng ``“``/``"`` mở khối trích dẫn; ngoặc cong
   đóng khi số ``“`` − số ``”`` cộng dồn về 0, ngoặc thẳng đóng khi tổng số ``"`` chẵn. Dòng
   trong khối thuộc text của unit đang mở, không tạo unit. Ngoặc cong mở giữa dòng mà chưa
   đóng cũng mở khối.
4. **Điểm dừng phần thân** (điều kiện đầu tiên sau Điều đầu tiên, ngoài trích dẫn): dòng
   ``Nơi nhận``, câu thông qua của Luật, dòng chữ ký (TM./KT./CHỦ TỊCH/BỘ TRƯỞNG/…), tiêu đề
   Phụ lục. Từ đó không nhận Điều/Khoản/Điểm nữa.
5. **Phụ lục**: sau điểm dừng, mỗi dòng đúng dạng ``PHỤ LỤC [SỐ] <số>`` mở một unit
   ``phu_luc`` chứa nguyên văn tới Phụ lục kế tiếp. Phần giữa điểm dừng và Phụ lục đầu tiên
   (chữ ký, Nơi nhận) bị bỏ, chỉ đếm (``n_dropped_lines``).
6. **Chú thích** (VBHN): dòng ``[^N] …`` không vào text; nội dung gán vào ``footnotes`` của
   mọi unit có ``[^N]`` trong text. ``[^N]`` dính sau nhãn (``18.[^6]``, ``c)[^3]``) được bỏ
   khi lấy số; bỏ khỏi ``title`` nhưng giữ trong ``text``.
7. ``text`` của unit = phần riêng của nó, giữ nguyên nhãn (``"Điều 9. …"``, ``"1. …"``,
   ``"a) …"``); dòng trống bị bỏ. Unit ``van_ban`` (mã = ``doc_id``) chứa phần mở đầu.
8. **Sửa nhãn thủ công** (``LabelOverride``): nhãn Khoản/Điểm ghi sai trong bản gốc (ND168
   "đ)" thay "d)") được đổi số hiệu/mã unit; ``text`` giữ nguyên văn, ``label_in_source`` ghi
   nhãn gốc. Áp trước khi kiểm tra thứ tự.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from typing import Literal

from pydantic import BaseModel, ConfigDict

from trafficlaw.utils.ids import (
    Level,
    UnitId,
    make_appendix_id,
    make_unit_id,
    parse_unit_id,
    roman_to_int,
)

#: Thứ tự ký hiệu Điểm trong văn bản quy phạm pháp luật (không có f, j, w, z).
DIEM_ALPHABET = "abcdđeghiklmnopqrstuvxy"

_FN_REF = re.compile(r"\[\^(\d+)\]")
_FN_REF_STRIP = re.compile(r"\s*\[\^\d+\]")
_FN_LINE = re.compile(r"^\[\^(\d+)\]\s*(.*)$")
_FRAME = re.compile(
    r"^(Phần|PHẦN|Chương|CHƯƠNG|Mục|MỤC)\s+([IVXLC]+|\d+)(?:\s*[.:]\s*(.*)|\s+(.*))?$"
)
_DIEU = re.compile(r"^Điều\s+(\d+[a-z]?)\s*\.((?:\[\^\d+\])*)\s*(.*)$")
_KHOAN = re.compile(r"^(\d+[a-z]?)\.((?:\[\^\d+\])*)\s+\S")
_DIEM = re.compile(r"^([a-zđ]\d*)\)((?:\[\^\d+\])*)\s+\S")
_LABEL_PREFIX = re.compile(r"^(?:\d+[a-z]?\.|[a-zđ]\d*\))(?:\[\^\d+\])*\s+")
_APPENDIX = re.compile(
    r"^(?:PHỤ LỤC|Phụ lục)(?:\s+(?:SỐ|Số|số))?(?:\s+([IVXLC]+|\d+[a-z]?))?\s*[.:]?$"
)
_NOI_NHAN = re.compile(r"^Nơi\s+nhận")
_PASSED = re.compile(r"^(?:Luật|Bộ luật|Nghị quyết) này (?:đã )?được Quốc hội")
_SIGNATURE = re.compile(
    r"^(?:(?:TM|KT|TL|Q)\.\s*[A-ZĐ]|T/M\b|PHÓ CHỦ TỊCH|CHỦ TỊCH|PHÓ THỦ TƯỚNG|THỦ TƯỚNG"
    r"|BỘ TRƯỞNG|THỨ TRƯỞNG|CHÁNH VĂN PHÒNG|VĂN PHÒNG QUỐC HỘI|VAN PHONG QUOC|XÁC THỰC)"
)
_FRAME_LEVEL: dict[str, Level] = {"phần": "phan", "chương": "chuong", "mục": "muc"}

EndReason = Literal["noi_nhan", "thong_qua", "chu_ky", "phu_luc"]


class Unit(BaseModel):
    """Một đơn vị pháp lý bản gốc (một dòng ``units.jsonl``)."""

    model_config = ConfigDict(extra="forbid")

    id: str
    doc_id: str
    level: Level
    number: str | None = None
    title: str | None = None
    text: str
    parent_id: str | None = None
    source_path: str | None = None
    #: ``{N: nội dung}`` của các chú thích ``[^N]`` xuất hiện trong ``text`` (chỉ VBHN).
    footnotes: dict[str, str] = {}
    #: Dòng (1-based) trong ``data/interim/<doc_id>.txt`` nơi unit bắt đầu.
    line_start: int
    #: Nhãn ghi trong bản gốc khi số hiệu đã được sửa thủ công (``label_overrides.yaml``);
    #: ``text`` vẫn giữ nguyên văn nhãn gốc.
    label_in_source: str | None = None


class LabelOverride(BaseModel):
    """Sửa thủ công nhãn Khoản/Điểm ghi sai trong bản gốc (``data/registry/label_overrides.yaml``).

    Dòng được nhận diện bằng ``label_in_source`` + đầu câu ``text_starts_with`` (sau nhãn) trong
    Điều/Khoản cha của ``unit_id``; số hiệu mới = cấp cuối của ``unit_id``. Không khớp đúng
    một lần → ``overrides_unapplied`` (script thoát mã 1).
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    unit_id: str
    label_in_source: str
    text_starts_with: str
    reason: str
    evidence: str

    @property
    def doc_id(self) -> str:
        return self.unit_id.split("/", 1)[0]

    @property
    def label(self) -> str:
        uid = parse_unit_id(self.unit_id)
        label = uid.diem if uid.diem is not None else uid.khoan
        if label is None:
            raise ValueError(f"override chỉ áp dụng cho Khoản/Điểm: {self.unit_id}")
        return label


class Anomaly(BaseModel):
    model_config = ConfigDict(extra="forbid")

    line: int
    kind: str
    detail: str


class StructureReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    doc_id: str
    n_lines: int = 0
    counts: dict[str, int] = {}
    dieu_numbers: list[str] = []
    n_dieu: int = 0
    last_dieu: str | None = None
    dieu_missing: list[int] = []
    first_dieu_line: int | None = None
    body_end_line: int | None = None
    body_end_reason: EndReason | None = None
    n_preamble_lines: int = 0
    #: Dòng không thuộc unit nào: giữa điểm dừng phần thân và Phụ lục đầu tiên (chữ ký…).
    n_dropped_lines: int = 0
    n_quoted_lines: int = 0
    n_quote_blocks: int = 0
    max_quote_span: int = 0
    unclosed_quote_line: int | None = None
    n_footnotes: int = 0
    orphan_footnotes: list[str] = []
    missing_footnotes: list[str] = []
    anomalies: list[Anomaly] = []
    overrides_applied: list[str] = []
    overrides_unapplied: list[str] = []


@dataclass
class StructureResult:
    units: list[Unit]
    report: StructureReport


@dataclass
class _Builder:
    id: str
    level: Level
    number: str | None
    title: str | None
    parent_id: str | None
    line_start: int
    lines: list[str] = field(default_factory=list)
    label_in_source: str | None = None


def strip_footnote_refs(s: str) -> str:
    return _FN_REF_STRIP.sub("", s).strip()


def _is_upper_title(s: str) -> bool:
    return any(c.isalpha() for c in s) and not any(c.islower() for c in s)


def quote_scan(line: str, depth: int = 0) -> tuple[int, str | None]:
    """Quét ngoặc kép từng ký tự, trả về ``(độ sâu sau dòng, ký tự mở cuối còn chưa đóng)``.

    ``“`` luôn mở, ``”`` luôn đóng (không xuống dưới 0); ``"`` đóng nếu đang có ngoặc mở,
    ngược lại là mở. Nhờ vậy chịu được ngoặc gõ lẫn: ``biển “Cấm đi ngược chiều"`` (ND168),
    ``"c) Thanh tra hàng hải …;”.`` (ND184).
    """
    opener: str | None = None
    stack: list[str] = []
    for ch in line:
        if ch == "“" or (ch == '"' and depth == 0):
            depth += 1
            stack.append(ch)
        elif ch in '”"' and depth > 0:
            depth -= 1
            if stack:
                stack.pop()
    if stack:
        opener = stack[-1]
    return depth, opener


def _frame_number(raw: str) -> str:
    return str(roman_to_int(raw)) if raw.isalpha() else str(int(raw))


def _num_key(num: str) -> tuple[int, str]:
    m = re.match(r"^(\d+)([a-z]?)$", num)
    assert m is not None
    return int(m.group(1)), m.group(2)


def _diem_key(label: str) -> tuple[int, int]:
    return DIEM_ALPHABET.index(label[0]), int(label[1:] or 0)


Step = Literal["ok", "gap", "bad"]


def _step(prev: tuple[int, int | str], new: tuple[int, int | str], zero: object) -> Step:
    """Quan hệ thứ tự giữa ký hiệu ``prev`` và ``new`` cùng cấp.

    ``zero`` là hậu tố rỗng ("" với số, 0 với Điểm). ``ok``: ``n+1`` không hậu tố, cùng gốc
    với hậu tố lớn hơn (``18`` → ``18a``), hoặc trở về gốc sau mục bổ sung đứng trước
    (``1a`` → ``1``). ``gap``: thiếu **đúng một** mục (``3`` → ``5``, ``n`` → ``p``) — lỗi
    đánh số có trong bản gốc (TT12 Điều 3, TT79 Điều 34); vẫn tạo unit, ghi anomaly. Còn lại
    (trùng, lùi, nhảy xa) → ``bad``.
    """
    (pi, ps), (ni, ns) = prev, new
    if ni == pi + 1 and ns == zero:
        return "ok"
    if ni == pi and ns > ps:  # type: ignore[operator]
        return "ok"
    if ni == pi and ns == zero and ps != zero:
        return "ok"
    if ni == pi + 2 and ns == zero:
        return "gap"
    return "bad"


def _dieu_follows(prev: tuple[int, str] | None, new: tuple[int, str]) -> bool:
    """Điều: chặt (không cho thiếu số) — số Điều thân văn bản liên tục ở cả 33 văn bản."""
    return prev is None or _step(prev, new, "") == "ok"


class _Parser:
    def __init__(
        self,
        doc_id: str,
        text: str,
        source_path: str | None,
        overrides: Sequence[LabelOverride] = (),
    ) -> None:
        self.doc_id = doc_id
        self.overrides = [o for o in overrides if o.doc_id == doc_id]
        self.override_hits: dict[str, int] = {o.unit_id: 0 for o in self.overrides}
        self.source_path = source_path
        self.lines = text.split("\n")
        self.report = StructureReport(doc_id=doc_id, n_lines=len(self.lines))
        self.units: list[_Builder] = []
        self.ids: set[str] = set()
        self.footnotes: dict[str, str] = {}

        self.root = self._add(doc_id, "van_ban", None, None, None, 1)
        self.phase: Literal["body", "tail", "appendix"] = "body"
        # Khung đang mở.
        self.phan: _Builder | None = None
        self.chuong: _Builder | None = None
        self.muc: _Builder | None = None
        self.frame_title: Literal["first", "cont"] | None = None
        #: Số khung cuối cùng trong từng phạm vi (Chương đánh số lại trong Phần, Mục trong Chương).
        self.frame_last: dict[str, int] = {}
        # Nội dung đang mở.
        self.dieu: _Builder | None = None
        self.khoan: _Builder | None = None
        self.diem: _Builder | None = None
        self.prev_dieu: tuple[int, str] | None = None
        self.prev_khoan: tuple[int, str] | None = None
        self.prev_diem: tuple[int, int] | None = None
        self.target: _Builder = self.root
        # Trích dẫn.
        self.in_quote = False
        self.quote_depth = 0
        self.quote_start = 0

    # ---- tiện ích ----

    def _add(
        self,
        uid: str,
        level: Level,
        number: str | None,
        title: str | None,
        parent: str | None,
        line_no: int,
    ) -> _Builder:
        b = _Builder(uid, level, number, title, parent, line_no)
        self.units.append(b)
        self.ids.add(uid)
        return b

    def _anomaly(self, line_no: int, kind: str, detail: str) -> None:
        self.report.anomalies.append(Anomaly(line=line_no, kind=kind, detail=detail[:160]))

    def _frame_parent(self) -> str:
        for f in (self.muc, self.chuong, self.phan):
            if f is not None:
                return f.id
        return self.doc_id

    # ---- trích dẫn ----

    def _quote_open(self, line_no: int, depth: int = 0) -> None:
        self.in_quote = True
        self.quote_depth = depth
        self.quote_start = line_no
        self.report.n_quote_blocks += 1

    def _quote_close_span(self, line_no: int) -> None:
        span = line_no - self.quote_start + 1
        self.report.max_quote_span = max(self.report.max_quote_span, span)

    # ---- xử lý dòng ----

    def run(self) -> StructureResult:
        for i, raw in enumerate(self.lines, start=1):
            line = raw.strip()
            if not line:
                continue
            m = _FN_LINE.match(line)
            if m:
                n = m.group(1)
                if n in self.footnotes:
                    self._anomaly(i, "footnote_duplicate", line)
                else:
                    self.footnotes[n] = m.group(2).strip()
                continue
            if self.phase == "appendix":
                self._appendix_line(line, i)
            elif self.in_quote:
                self._quoted_line(line, i)
            elif self.phase == "tail":
                if self._appendix_heading(line, i) is None:
                    self.report.n_dropped_lines += 1
            else:
                self._body_line(line, i)
        if self.in_quote:
            self.report.unclosed_quote_line = self.quote_start
            self._anomaly(
                self.quote_start, "unclosed_quote", "trích dẫn không đóng tới hết văn bản"
            )
            self._quote_close_span(len(self.lines))
        return self._finish()

    def _quoted_line(self, line: str, i: int) -> None:
        if self.prev_dieu is not None and self._end_reason(line) in ("noi_nhan", "thong_qua"):
            # Ngoặc không đóng mà gặp Nơi nhận/chữ ký: đóng cưỡng bức, xử lý dòng như thường.
            self._anomaly(self.quote_start, "unclosed_quote", f"đóng cưỡng bức ở dòng {i}")
            self._quote_close_span(i - 1)
            self.in_quote = False
            self._body_line(line, i)
            return
        self.target.lines.append(line)
        self.report.n_quoted_lines += 1
        self.quote_depth, _ = quote_scan(line, self.quote_depth)
        if self.quote_depth == 0:
            self.in_quote = False
            self._quote_close_span(i)

    def _end_reason(self, line: str) -> EndReason | None:
        if _NOI_NHAN.match(line):
            return "noi_nhan"
        if _PASSED.match(line):
            return "thong_qua"
        if _SIGNATURE.match(line):
            return "chu_ky"
        if _APPENDIX.match(strip_footnote_refs(line)):
            return "phu_luc"
        return None

    def _body_line(self, line: str, i: int) -> None:
        # Trích dẫn chỉ theo dõi sau Điều đầu tiên: phần mở đầu không có nội dung sửa đổi, còn
        # chú thích PDF tràn trang (VBHN65: “Căn cứ … ở trang 1) không được nuốt Chương/Điều.
        if self.prev_dieu is not None and line[0] in '“"':
            self._quote_open(i)
            self._quoted_line(line, i)
            return
        is_table = " | " in line
        if self.prev_dieu is not None:
            reason = self._end_reason(line)
            if reason is not None:
                self.report.body_end_line = i
                self.report.body_end_reason = reason
                self.phase = "tail"
                if reason == "phu_luc":
                    self._appendix_heading(line, i)
                else:
                    self.report.n_dropped_lines += 1
                return
        if not is_table and self._heading(line, i):
            self._maybe_open_inline_quote(line, i)
            return
        if self.frame_title is not None and self.dieu is None and not is_table:
            frame = self.target
            if self.frame_title == "first" or _is_upper_title(line):
                t = strip_footnote_refs(line)
                frame.title = f"{frame.title} {t}" if frame.title else t
                self.frame_title = "cont"
            else:
                self.frame_title = None
        else:
            self.frame_title = None
        self.target.lines.append(line)
        if self.target is self.root:
            self.report.n_preamble_lines += 1
        self._maybe_open_inline_quote(line, i)

    def _maybe_open_inline_quote(self, line: str, i: int) -> None:
        """Ngoặc cong mở giữa dòng (``… như sau: “1a. …``) mà chưa đóng → vào khối trích dẫn.

        Chỉ ngoặc cong: ``"`` lẻ giữa dòng (vd. ký hiệu inch) không đủ căn cứ để mở khối.
        """
        depth, opener = quote_scan(line)
        if self.prev_dieu is not None and depth > 0 and opener == "“":
            self._quote_open(i, depth)

    # ---- tiêu đề ----

    def _heading(self, line: str, i: int) -> bool:
        bare = strip_footnote_refs(line)
        m = _FRAME.match(bare)
        if m and (m.group(3) is not None or m.group(4) is None or _is_upper_title(m.group(4))):
            return self._frame(m, line, i)
        m = _DIEU.match(line)
        if m:
            return self._dieu(m, line, i)
        if self.dieu is None:
            return False
        m = _KHOAN.match(line)
        if m:
            return self._khoan(m.group(1), line, i)
        m = _DIEM.match(line)
        if m and m.group(1)[0] in DIEM_ALPHABET:
            return self._diem(m.group(1), line, i)
        return False

    def _frame(self, m: re.Match[str], line: str, i: int) -> bool:
        level = _FRAME_LEVEL[m.group(1).lower()]
        try:
            number = _frame_number(m.group(2))
        except ValueError:
            return False
        if level == "phan":
            uid = UnitId(self.doc_id, phan=number)
        elif level == "chuong":
            uid = UnitId(self.doc_id, phan=self.phan.number if self.phan else None, chuong=number)
        else:
            uid = UnitId(
                self.doc_id,
                phan=self.phan.number if self.phan else None,
                chuong=self.chuong.number if self.chuong else None,
                muc=number,
            )
        sid = str(uid)
        parent = uid.parent()
        scope = f"{level}@{parent}"
        if sid in self.ids or int(number) != self.frame_last.get(scope, 0) + 1:
            self._anomaly(i, f"{level}_out_of_sequence", line)
            return False
        self.frame_last[scope] = int(number)
        title_raw = m.group(3) if m.group(3) is not None else m.group(4)
        title = strip_footnote_refs(title_raw) if title_raw else None
        b = self._add(sid, level, number, title or None, str(parent) if parent else None, i)
        b.lines.append(line)
        if level == "phan":
            self.phan, self.chuong, self.muc = b, None, None
        elif level == "chuong":
            self.chuong, self.muc = b, None
        else:
            self.muc = b
        self.dieu = self.khoan = self.diem = None
        self.target = b
        self.frame_title = "cont" if title else "first"
        return True

    def _dieu(self, m: re.Match[str], line: str, i: int) -> bool:
        number = m.group(1)
        key = _num_key(number)
        uid = make_unit_id(self.doc_id, number)
        if uid in self.ids or not _dieu_follows(self.prev_dieu, key):
            self._anomaly(i, "dieu_out_of_sequence", line)
            return False
        if self.prev_dieu is None:
            self.report.first_dieu_line = i
            if number != "1":
                self._anomaly(i, "dieu_first_not_1", line)
        title = strip_footnote_refs(m.group(3)) or None
        b = self._add(uid, "dieu", number, title, self._frame_parent(), i)
        b.lines.append(line)
        self.dieu, self.khoan, self.diem = b, None, None
        self.prev_dieu, self.prev_khoan, self.prev_diem = key, None, None
        self.target = b
        self.frame_title = None
        return True

    def _override(self, label: str, line: str, i: int, make_id: Callable[[str], str]) -> str:
        """Nhãn sau khi áp ``label_overrides`` (không khớp → giữ nguyên ``label``)."""
        content = _LABEL_PREFIX.sub("", line, count=1)
        for o in self.overrides:
            if o.label_in_source != label or not content.startswith(o.text_starts_with):
                continue
            if make_id(o.label) != o.unit_id:
                self._anomaly(i, "label_override_mismatch", f"{o.unit_id} ≠ {make_id(o.label)}")
                continue
            self.override_hits[o.unit_id] += 1
            self._anomaly(i, "label_override", f"{label} → {o.label}: {o.unit_id}")
            return o.label
        return label

    def _khoan(self, number: str, line: str, i: int) -> bool:
        assert self.dieu is not None
        dieu = self.dieu.number
        src = number
        number = self._override(number, line, i, lambda n: make_unit_id(self.doc_id, dieu, n))
        key = _num_key(number)
        uid = make_unit_id(self.doc_id, self.dieu.number, number)
        # Khoản đầu tiên: 1 hoặc mục bổ sung đứng trước nó (1a — "bổ sung khoản 1a vào trước").
        first = self.prev_khoan is None and key[0] == 1
        step = "ok" if first else _step(self.prev_khoan or (0, ""), key, "")
        if uid in self.ids or step == "bad":
            self._anomaly(i, "khoan_out_of_sequence", f"{self.dieu.id}: {line}")
            return False
        if step == "gap":
            self._anomaly(i, "khoan_gap", f"{self.dieu.id}: {line}")
        b = self._add(uid, "khoan", number, None, self.dieu.id, i)
        b.lines.append(line)
        b.label_in_source = src if src != number else None
        self.khoan, self.diem = b, None
        self.prev_khoan, self.prev_diem = key, None
        self.target = b
        return True

    def _diem(self, label: str, line: str, i: int) -> bool:
        assert self.dieu is not None
        dieu, khoan = self.dieu.number, self.khoan.number if self.khoan else None
        src = label
        label = self._override(label, line, i, lambda x: make_unit_id(self.doc_id, dieu, khoan, x))
        key = _diem_key(label)
        parent = self.khoan or self.dieu
        uid = make_unit_id(self.doc_id, dieu, khoan, label)
        first = self.prev_diem is None and key[0] == 0  # a hoặc a1
        step = "ok" if first else _step(self.prev_diem or (-1, 0), key, 0)
        if uid in self.ids or step == "bad":
            self._anomaly(i, "diem_out_of_sequence", f"{parent.id}: {line}")
            return False
        if step == "gap":
            self._anomaly(i, "diem_gap", f"{parent.id}: {line}")
        b = self._add(uid, "diem", label, None, parent.id, i)
        b.lines.append(line)
        b.label_in_source = src if src != label else None
        self.diem = b
        self.prev_diem = key
        self.target = b
        return True

    # ---- phụ lục ----

    def _appendix_heading(self, line: str, i: int) -> _Builder | None:
        m = _APPENDIX.match(strip_footnote_refs(line))
        if not m:
            return None
        n_existing = sum(u.level == "phu_luc" for u in self.units)
        raw = m.group(1)
        if raw is None:
            number = str(n_existing + 1)
            self._anomaly(i, "phu_luc_unnumbered", f"đánh số theo thứ tự: PL{number}")
        else:
            number = _frame_number(raw) if raw.isalpha() else raw.lstrip("0") or "0"
        uid = make_appendix_id(self.doc_id, number)
        k = 2
        while uid in self.ids:
            uid = make_appendix_id(self.doc_id, f"{number}-{k}")
            k += 1
        if k > 2:
            self._anomaly(i, "phu_luc_duplicate", f"{line} → {uid}")
        b = self._add(uid, "phu_luc", uid.rsplit("/PL", 1)[1], None, self.doc_id, i)
        b.lines.append(line)
        self.phase = "appendix"
        self.target = b
        return b

    def _appendix_line(self, line: str, i: int) -> None:
        if self._appendix_heading(line, i) is not None:
            return
        b = self.target
        if b.title is None and not b.lines[1:]:
            b.title = strip_footnote_refs(line) or None
        b.lines.append(line)

    # ---- kết thúc ----

    def _finish(self) -> StructureResult:
        units: list[Unit] = []
        referenced: set[str] = set()
        missing: set[str] = set()
        for b in self.units:
            text = "\n".join(b.lines)
            refs = list(dict.fromkeys(_FN_REF.findall(text)))
            fns = {n: self.footnotes[n] for n in refs if n in self.footnotes}
            referenced.update(fns)
            missing.update(n for n in refs if n not in self.footnotes)
            units.append(
                Unit(
                    id=b.id,
                    doc_id=self.doc_id,
                    level=b.level,
                    number=b.number,
                    title=b.title,
                    text=text,
                    parent_id=b.parent_id,
                    source_path=self.source_path,
                    footnotes=fns,
                    line_start=b.line_start,
                    label_in_source=b.label_in_source,
                )
            )
        r = self.report
        counts: dict[str, int] = {}
        for u in units:
            counts[u.level] = counts.get(u.level, 0) + 1
        r.counts = counts
        r.dieu_numbers = [u.number for u in units if u.level == "dieu" and u.number]
        r.n_dieu = len(r.dieu_numbers)
        r.last_dieu = r.dieu_numbers[-1] if r.dieu_numbers else None
        ints = {_num_key(n)[0] for n in r.dieu_numbers}
        r.dieu_missing = [n for n in range(1, max(ints, default=0) + 1) if n not in ints]
        r.n_footnotes = len(self.footnotes)
        r.orphan_footnotes = sorted(set(self.footnotes) - referenced, key=int)
        r.missing_footnotes = sorted(missing, key=int)
        r.overrides_applied = [k for k, n in self.override_hits.items() if n == 1]
        r.overrides_unapplied = [k for k, n in self.override_hits.items() if n != 1]
        return StructureResult(units, r)


def parse_structure(
    doc_id: str,
    text: str,
    source_path: str | None = None,
    overrides: Sequence[LabelOverride] = (),
) -> StructureResult:
    """Tách cấu trúc một văn bản (nội dung file interim, đã NFC). Hàm thuần.

    ``overrides``: sửa nhãn Khoản/Điểm ghi sai trong bản gốc (chỉ mục của ``doc_id`` được dùng).
    """
    return _Parser(doc_id, text, source_path, overrides).run()
