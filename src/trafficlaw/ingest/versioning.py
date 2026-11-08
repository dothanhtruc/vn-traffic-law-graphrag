"""Áp chỉ dẫn sửa đổi lên unit bản gốc → phiên bản theo thời gian (hàm thuần, M4).

Quy tắc đóng/mở phiên bản:

- **Bản gốc** ``version=0``: ``effective_from`` = ngày hiệu lực riêng của unit (hoặc của unit
  tổ tiên gần nhất, theo Điều hiệu lực của chính văn bản), không có thì ``hieu_luc_tu``.
- Chỉ dẫn được gom theo ngày hiệu lực D, áp theo thứ tự (D, thứ tự trong văn bản sửa đổi)
  lên trạng thái hiện hành. Hết một ngày D, unit nào đổi (text hoặc trạng thái) thì đóng
  phiên bản cũ (``effective_to = D − 1``, ``status = amended``) và mở phiên bản mới từ D;
  unit không đổi text thì không có phiên bản mới.
- **Bãi bỏ**: unit và mọi unit con → phiên bản ``repealed`` (text rỗng) từ D.
- **Sửa cả Điều/Khoản**: unit con chỉ có ở bản cũ → bãi bỏ; chỉ có ở bản mới → unit bổ sung.
- **Bổ sung**: unit mới (``units_added``) có ``version=1`` từ D, vị trí theo "vào sau/trước";
  đích đã tồn tại và còn hiệu lực → todo ``dich_da_ton_tai``.
- **Cụm từ**: tìm trong text của đích và các unit con (``tên`` → chỉ dòng tiêu đề/câu dẫn
  của đích); khớp không phân biệt khoảng trắng. Không thấy → todo, không áp.
- **Bãi bỏ/thay thế toàn bộ văn bản** (``relations`` toàn bộ): mọi unit → ``repealed`` từ D.
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date

from trafficlaw.ingest.amendments import Block, Instruction, Todo, TodoReason
from trafficlaw.ingest.structure import Unit
from trafficlaw.ingest.versions import AddedUnit, UnitVersion
from trafficlaw.registry.schema import DocumentMeta
from trafficlaw.utils.dates import day_before
from trafficlaw.utils.ids import parse_unit_id


@dataclass
class _Node:
    id: str
    level: str
    number: str | None
    title: str | None
    parent: str | None
    children: list[str]
    text: str
    status: str = "active"


@dataclass
class VersionResult:
    versions: list[UnitVersion]
    added: list[AddedUnit]
    todos: list[Todo]
    #: Chỉ dẫn áp được (theo ``seq``) — dùng để thống kê.
    applied: set[int] = field(default_factory=set)
    #: Chỉ dẫn cụm từ không còn đối tượng vì đích đã bị chính văn bản sửa đổi viết lại/bãi bỏ
    #: trước đó trong cùng ngày (không phải lỗi; ghi để rà).
    superseded: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class Repeal:
    """Văn bản bị bãi bỏ/thay thế toàn bộ từ ``effective_from`` bởi ``source_unit_id``."""

    effective_from: date
    source_unit_id: str


_DASHES = re.compile(r"\\?[-–—]")  # re.escape("-") cho "\-"


def _phrase_re(phrase: str, *, ignore_case: bool = False) -> re.Pattern[str]:
    """Khớp cụm từ không phân biệt khoảng trắng và kiểu gạch nối (``-``/``–``/``—``)."""
    parts = [_DASHES.sub("[-–—]", re.escape(p)) for p in phrase.split()]
    return re.compile(r"\s+".join(parts), re.I if ignore_case else 0)


def _remove_phrase(text: str, pat: re.Pattern[str]) -> tuple[str, int]:
    n = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal n
        n += 1
        return ""

    out = pat.sub(repl, text)
    if n:
        out = re.sub(r"[ \t]{2,}", " ", out)
        out = re.sub(r"[ \t]+([,.;:)])", r"\1", out)
        out = re.sub(r"\([ \t]+", "(", out)
        out = "\n".join(ln.strip() for ln in out.split("\n"))
    return out, n


class _Applier:
    def __init__(
        self,
        doc: DocumentMeta,
        base_units: Sequence[Unit],
        special: Mapping[str, date],
        amending_appendices: Mapping[str, Unit],
        source_paths: Mapping[str, str | None],
    ) -> None:
        self.doc = doc
        self.nodes: dict[str, _Node] = {}
        self.order: list[str] = []
        self.amending_appendices = amending_appendices
        self.source_paths = source_paths
        for u in base_units:
            self.nodes[u.id] = _Node(u.id, u.level, u.number, u.title, u.parent_id, [], u.text)
            self.order.append(u.id)
        for u in base_units:
            if u.parent_id in self.nodes:
                self.nodes[u.parent_id].children.append(u.id)
        self.history: dict[str, list[UnitVersion]] = {}
        for u in base_units:
            self.history[u.id] = [
                UnitVersion(
                    unit_id=u.id,
                    version=0,
                    text=u.text,
                    effective_from=self._start_date(u.id, special),
                    status="active",
                )
            ]
        self.added: dict[str, AddedUnit] = {}
        self.todos: list[Todo] = []
        self.applied: set[int] = set()
        self.superseded: list[str] = []
        # Trạng thái trong ngày đang áp.
        self.touched: dict[str, str] = {}  # unit_id → source_unit_id

    def _start_date(self, uid: str, special: Mapping[str, date]) -> date | None:
        u: str | None = uid
        while u is not None:
            if u in special:
                return special[u]
            node = self.nodes.get(u)
            u = node.parent if node is not None else None
        return self.doc.hieu_luc_tu

    # ------------------------------------------------------------ tiện ích

    def todo(self, ins: Instruction, reason: TodoReason, detail: str = "") -> None:
        self.todos.append(
            Todo(
                doc_id=self.doc.doc_id,
                unit_id=ins.target_id,
                source_unit_id=ins.source_unit_id,
                reason=reason,
                detail=(detail or ins.sentence)[:500],
            )
        )

    def _touch(self, uid: str, src: str) -> None:
        # Nhiều thao tác cùng ngày trên một unit → nguồn là thao tác cuối (quyết định trạng thái).
        self.touched.pop(uid, None)
        self.touched[uid] = src

    def _set_text(self, uid: str, text: str, src: str) -> None:
        node = self.nodes[uid]
        if node.text != text or node.status != "active":
            node.text = text
            node.status = "active"
            self._touch(uid, src)

    def _repeal(self, uid: str, src: str) -> None:
        node = self.nodes[uid]
        for c in node.children:
            self._repeal(c, src)
        if node.status != "repealed":
            node.status = "repealed"
            node.text = ""
            self._touch(uid, src)

    def _subtree(self, uid: str) -> list[str]:
        out = [uid]
        for c in self.nodes[uid].children:
            if self.nodes[c].status == "active":
                out.extend(self._subtree(c))
        return out

    def _add(
        self,
        block: Block,
        parent: str,
        src: str,
        after_id: str | None,
        before_id: str | None,
    ) -> None:
        siblings = self.nodes[parent].children
        if before_id is not None and before_id in siblings:
            siblings.insert(siblings.index(before_id), block.id)
        elif after_id is not None and after_id in siblings:
            siblings.insert(siblings.index(after_id) + 1, block.id)
        else:
            if after_id is None and before_id is None and siblings:
                after_id = siblings[-1]
            siblings.append(block.id)
        self.nodes[block.id] = _Node(
            block.id, block.level, block.number, block.title, parent, [], block.text
        )
        self._touch(block.id, src)
        self.added[block.id] = AddedUnit(
            id=block.id,
            doc_id=self.doc.doc_id,
            level=block.level,  # type: ignore[arg-type]
            number=block.number,
            title=block.title,
            text=block.text,
            parent_id=parent,
            source_path=self.source_paths.get(src.split("/")[0]),
            after_id=after_id if before_id is None else None,
            before_id=before_id,
            source_unit_id=src,
        )
        prev: str | None = None
        for c in block.children:
            self._add(c, block.id, src, prev, None)
            prev = c.id

    def _sync(self, uid: str, block: Block, src: str) -> None:
        """Đưa unit ``uid`` (và cây con) về đúng ``block``."""
        self._set_text(uid, block.text, src)
        node = self.nodes[uid]
        if block.title is not None:
            node.title = block.title
        new_ids = [c.id for c in block.children]
        for c in list(node.children):
            if c not in new_ids and self.nodes[c].status == "active":
                self._repeal(c, src)
        prev: str | None = None
        for c in block.children:
            if c.id in self.nodes:
                self._sync(c.id, c, src)
            else:
                self._add(c, uid, src, prev, None)
            prev = c.id

    def _parent_for_new(self, ins: Instruction) -> str | None:
        uid = parse_unit_id(ins.target_id)
        if uid.level == "dieu":
            anchor = ins.after_id or ins.before_id
            if anchor and anchor in self.nodes:
                return self.nodes[anchor].parent
            # Điều bổ sung không nêu vị trí: cùng cha với Điều có số liền trước.
            return self.doc.doc_id
        p = uid.parent()
        return None if p is None else str(p)

    # ------------------------------------------------------------ thao tác

    def apply(self, ins: Instruction) -> None:
        node = self.nodes.get(ins.target_id)
        op = ins.op
        src = ins.source_unit_id
        if op == "insert":
            assert ins.block is not None
            if node is not None and node.status == "active":
                self.todo(ins, "dich_da_ton_tai")
                return
            if node is not None:  # bổ sung lại unit đã bị bãi bỏ
                self._sync(node.id, ins.block, src)
            else:
                parent = self._parent_for_new(ins)
                if parent is None or parent not in self.nodes:
                    self.todo(ins, "khong_tim_thay_dich", f"không có unit cha {parent}")
                    return
                if self.nodes[parent].status != "active":
                    self.todo(ins, "dich_da_bai_bo", f"unit cha {parent} đã bị bãi bỏ")
                    return
                self._add(ins.block, parent, src, ins.after_id, ins.before_id)
            self.applied.add(ins.seq)
            return
        if op == "add_appendix":
            appx = self.amending_appendices.get(ins.source_appendix_id or "")
            if appx is None:
                self.todo(ins, "khong_tim_thay_phu_luc", f"không có {ins.source_appendix_id}")
                return
            if node is not None and node.status == "active":
                self.todo(ins, "dich_da_ton_tai")
                return
            number = parse_unit_id(ins.target_id).phu_luc
            blk = Block(
                id=ins.target_id, level="phu_luc", number=number, title=appx.title, text=appx.text
            )
            if node is not None:
                self._sync(node.id, blk, src)
            else:
                self._add(blk, self.doc.doc_id, src, None, None)
            self.applied.add(ins.seq)
            return
        if node is None:
            missing_pl = parse_unit_id(ins.target_id).level == "phu_luc"
            self.todo(ins, "khong_tim_thay_phu_luc" if missing_pl else "khong_tim_thay_dich")
            return
        if node.status != "active":
            if op.endswith("_phrase") and self._superseded_today(node.id, ins):
                return
            self.todo(ins, "dich_da_bai_bo")
            return
        if op == "replace":
            assert ins.block is not None
            if ins.block.level != node.level:
                self.todo(ins, "khac_cap", f"{ins.block.level} ≠ {node.level}")
                return
            self._sync(node.id, ins.block, src)
        elif op == "replace_title":
            assert ins.block is not None
            if node.level == "dieu":
                lines = node.text.split("\n")
                lines[0] = ins.block.text.split("\n")[0]
                self._set_text(node.id, "\n".join(lines), src)
                if m := re.match(r"^Điều\s+\S+?\.\s*(.*)$", lines[0]):
                    node.title = m[1] or None
            elif node.level == "khoan" and any(
                self.nodes[c].status == "active" for c in node.children
            ):
                self._set_text(node.id, ins.block.text, src)
            else:
                self.todo(ins, "mau_khong_ro", "sửa 'tên' của unit không có tiêu đề riêng")
                return
        elif op == "repeal":
            self._repeal(node.id, src)
        elif op == "replace_appendix":
            appx = self.amending_appendices.get(ins.source_appendix_id or "")
            if appx is None:
                self.todo(ins, "khong_tim_thay_phu_luc", f"không có {ins.source_appendix_id}")
                return
            self._set_text(node.id, appx.text, src)
            node.title = appx.title
        elif op in ("replace_phrase", "remove_phrase", "insert_phrase"):
            if not self._phrase(ins, node):
                return
        else:  # pragma: no cover - OpKind đầy đủ ở trên
            raise ValueError(op)
        self.applied.add(ins.seq)

    def _superseded_today(self, uid: str, ins: Instruction) -> bool:
        """Đích đã bị chính văn bản sửa đổi này viết lại/bãi bỏ trong ngày, và cụm từ có ở
        phiên bản trước đó → chỉ dẫn cụm từ không còn đối tượng (ghi ``superseded``)."""
        amender = ins.source_unit_id.split("/")[0]
        assert ins.old is not None
        pat = _phrase_re(ins.old, ignore_case=True)
        for u in [uid, *self._all_desc(uid)]:
            src = self.touched.get(u)
            hist = self.history.get(u)
            if src and src.split("/")[0] == amender and hist and pat.search(hist[-1].text):
                self.superseded.append(f"{ins.source_unit_id} → {uid}: {ins.old!r}")
                self.applied.add(ins.seq)
                return True
        return False

    def _all_desc(self, uid: str) -> list[str]:
        out: list[str] = []
        for c in self.nodes[uid].children:
            out.append(c)
            out.extend(self._all_desc(c))
        return out

    def _phrase(self, ins: Instruction, node: _Node) -> bool:
        assert ins.old is not None
        title_only = ins.part == "title"
        scope = [node.id] if title_only or ins.part == "can_cu" else self._subtree(node.id)
        heads = [
            self.nodes[u].text.partition("\n")[0] if title_only else self.nodes[u].text
            for u in scope
        ]
        pat = _phrase_re(ins.old)
        if not any(pat.search(h) for h in heads):
            # Bản gốc khác chữ hoa/thường ("trung ương"/"Trung ương"): vẫn là cùng cụm từ.
            pat = _phrase_re(ins.old, ignore_case=True)
        total = 0
        for uid in scope:
            n = self.nodes[uid]
            text = n.text
            if title_only:
                head, _, rest = text.partition("\n")
            else:
                head, rest = text, None
            if ins.op == "replace_phrase":
                new_head, k = pat.subn(ins.new or "", head)
            elif ins.op == "remove_phrase":
                new_head, k = _remove_phrase(head, pat)
            else:
                add = ins.new or ""

                def ins_repl(m: re.Match[str], add: str = add) -> str:
                    if ins.where == "after":
                        sep = "" if add[:1] in ",;.)" else " "
                        return m[0] + sep + add
                    return add + " " + m[0]

                new_head, k = pat.subn(ins_repl, head)
            if k:
                total += k
                new_text = new_head if rest is None else new_head + ("\n" + rest if rest else "")
                self._set_text(uid, new_text, ins.source_unit_id)
        if total == 0:
            if self._superseded_today(node.id, ins):
                return False
            self.todo(ins, "khong_tim_thay_cum_tu", f"{ins.sentence} (cụm từ {ins.old!r})")
            return False
        return True

    # ------------------------------------------------------------ đóng/mở phiên bản

    def commit(self, day: date) -> None:
        for uid, src in self.touched.items():
            node = self.nodes[uid]
            hist = self.history.setdefault(uid, [])
            new_status = "repealed" if node.status == "repealed" else "active"
            if hist:
                last = hist[-1]
                if last.text == node.text and last.status == new_status:
                    continue
                if last.effective_from is not None and last.effective_from > day_before(day):
                    self.todos.append(
                        Todo(
                            doc_id=self.doc.doc_id,
                            unit_id=uid,
                            source_unit_id=src,
                            reason="xung_dot_ngay",
                            detail=(
                                f"phiên bản {last.version} có hiệu lực từ {last.effective_from}, "
                                f"bị sửa từ {day}"
                            ),
                        )
                    )
                last.effective_to = day_before(day)
                if last.status == "active":
                    last.status = "amended"
                version = last.version + 1
            else:
                version = 1
            hist.append(
                UnitVersion(
                    unit_id=uid,
                    version=version,
                    text=node.text,
                    effective_from=day,
                    status=new_status,  # type: ignore[arg-type]
                    source_unit_id=src,
                )
            )
        self.touched = {}

    def ordered_ids(self) -> list[str]:
        """Thứ tự duyệt cây (gốc trước, con theo vị trí) — để ghi file ổn định."""
        out: list[str] = []
        roots = [u for u in self.order if self.nodes[u].parent not in self.nodes]

        def walk(u: str) -> None:
            out.append(u)
            for c in self.nodes[u].children:
                walk(c)

        for r in roots:
            walk(r)
        seen = set(out)
        out.extend(u for u in self.nodes if u not in seen)
        return out


def build_versions(
    doc: DocumentMeta,
    base_units: Sequence[Unit],
    instructions: Sequence[Instruction],
    *,
    special: Mapping[str, date] | None = None,
    repeal: Repeal | None = None,
    amending_appendices: Mapping[str, Unit] | None = None,
    source_paths: Mapping[str, str | None] | None = None,
) -> VersionResult:
    """Phiên bản của mọi unit văn bản ``doc``. ``instructions`` chỉ gồm chỉ dẫn nhắm ``doc``.

    ``source_paths``: ``doc_id`` văn bản sửa đổi → ``source_path`` (ghi vào unit bổ sung).
    """
    ap = _Applier(doc, base_units, special or {}, amending_appendices or {}, source_paths or {})
    pending = [i for i in instructions if i.target_doc == doc.doc_id]
    for ins in pending:
        if ins.effective_from is None:
            ap.todo(
                ins, "hieu_luc_khong_ro", f"văn bản sửa đổi thiếu ngày hiệu lực: {ins.sentence}"
            )
    dated = sorted(
        (i for i in pending if i.effective_from is not None),
        key=lambda i: (i.effective_from, i.seq),
    )
    if repeal is not None:
        late = [i for i in dated if i.effective_from and i.effective_from >= repeal.effective_from]
        for ins in late:
            ap.todo(ins, "dich_da_bai_bo", f"văn bản đích hết hiệu lực từ {repeal.effective_from}")
        dated = [i for i in dated if i not in late]
    day: date | None = None
    for ins in dated:
        assert ins.effective_from is not None
        if day is not None and ins.effective_from != day:
            ap.commit(day)
        day = ins.effective_from
        ap.apply(ins)
    if day is not None:
        ap.commit(day)
    if repeal is not None:
        for uid in ap.ordered_ids():
            if ap.nodes[uid].status == "active":
                ap._repeal(uid, repeal.source_unit_id)
        ap.commit(repeal.effective_from)
    versions = [v for uid in ap.ordered_ids() for v in ap.history.get(uid, [])]
    added = [ap.added[u] for u in ap.ordered_ids() if u in ap.added]
    return VersionResult(versions, added, ap.todos, ap.applied, ap.superseded)
