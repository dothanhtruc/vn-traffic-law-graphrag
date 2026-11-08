"""Ngày hiệu lực chung và hiệu lực riêng cấp Điều/Khoản/Điểm (Điều "Hiệu lực thi hành").

Chỉ xét Điều có tiêu đề chứa "hiệu lực" hoặc "thi hành". Mỗi câu (tách theo ``.``/``;``) có
"có hiệu lực" được xếp vào một trong ba loại:

- **Chung**: ``<Luật|Nghị định|Thông tư> này có hiệu lực (thi hành) (kể) từ ngày D[, trừ …]``.
- **Riêng**: ``(Quy định tại)? <dẫn chiếu> (của) <Luật|Nghị định|Thông tư> này có hiệu lực
  (thi hành) (kể) từ ngày D`` — câu phải kết thúc ngay sau ngày. Dẫn chiếu đọc bằng
  :func:`trafficlaw.ingest.refs.parse_refs`.
- **Không rõ** (câu có ngày/điều kiện khác, câu riêng có mô tả "Quy định xử phạt … liên quan
  đến …", "và theo quy định của pháp luật…") → todo ``hieu_luc_khong_ro``, không áp.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import date

from trafficlaw.ingest.amendments import Todo, parse_vn_date_in
from trafficlaw.ingest.refs import SELF, RefContext, RefError, normalize, parse_refs
from trafficlaw.ingest.structure import Unit

_DOC = r"(?:Bộ\s+luật|Luật|Nghị\s+định|Thông\s+tư|Quyết\s+định)"
_D = r"ngày\s+\d{1,2}\s+tháng\s+\d{1,2}\s+năm\s+\d{4}"
_GENERAL = re.compile(
    rf"^{_DOC}\s+này\s+có\s+hiệu\s+lực\s+(?:thi\s+hành\s+)?(?:kể\s+)?từ\s+({_D})"
    r"(?:\s*,\s*trừ\s+(?:trường\s+hợp\s+)?quy\s+định\s+tại\s+.+"
    r"|\s*,?\s*và\s+thay\s+thế\s+.+)?$"
)
_SPECIAL = re.compile(
    rf"^(?:Quy\s+định\s+tại\s+)?(.+?)\s+(?:của\s+)?{_DOC}\s+này\s+có\s+hiệu\s+lực\s+"
    rf"(?:thi\s+hành\s+)?(?:kể\s+)?từ\s+({_D})$"
)
_EFFECT_TITLE = re.compile(r"hiệu\s+lực|thi\s+hành", re.I)
_HAS_EFFECT = re.compile(r"có\s+hiệu\s+lực")
_LABEL = re.compile(r"^(?:\d+[a-z]?\.|[a-zđ]\d*\))\s*")


@dataclass
class EffectResult:
    general: date | None = None
    special: dict[str, date] = field(default_factory=dict)
    todos: list[Todo] = field(default_factory=list)
    #: Unit có câu hiệu lực (để rà tay).
    sources: list[str] = field(default_factory=list)


def _sentences(text: str) -> list[str]:
    out: list[str] = []
    for line in text.split("\n"):
        line = _LABEL.sub("", line.strip())
        for s in re.split(r"(?<=[.;])\s+", line):
            s = s.strip().rstrip(".;").strip()
            if s:
                out.append(s)
    return out


def parse_effects(doc_id: str, units: Sequence[Unit]) -> EffectResult:
    """Ngày hiệu lực của văn bản ``doc_id`` theo Điều hiệu lực (``units`` của chính văn bản)."""
    res = EffectResult()
    effect_dieu = {u.id for u in units if u.level == "dieu" and _EFFECT_TITLE.search(u.title or "")}
    for u in units:
        dieu = u.id if u.level == "dieu" else None
        if dieu is None and u.level in ("khoan", "diem"):
            dieu = "/".join(u.id.split("/")[:2])
        if dieu not in effect_dieu:
            continue
        text = u.text
        if u.level == "dieu":
            text = "\n".join(text.split("\n")[1:])
        for s in _sentences(text):
            s = normalize(s)
            if not _HAS_EFFECT.search(s) or s.startswith("trước ngày"):
                continue
            if "trước ngày" in s and "có hiệu lực" in s.split("trước ngày", 1)[1][:40]:
                continue  # "… trước ngày Nghị định này có hiệu lực …" (chuyển tiếp)
            if m := _GENERAL.match(s):
                d = parse_vn_date_in(m[1])
                if res.general is None:
                    res.general = d
                res.sources.append(u.id)
                continue
            if m := _SPECIAL.match(s):
                d = parse_vn_date_in(m[2])
                try:
                    refs = parse_refs(m[1], RefContext())
                except RefError as e:
                    res.todos.append(_todo(doc_id, u.id, f"{s} ({e})"))
                    continue
                if any(r.doc not in (None, SELF) for r in refs) or any(
                    r.mau is not None or r.part is not None for r in refs
                ):
                    res.todos.append(_todo(doc_id, u.id, s))
                    continue
                assert d is not None
                for r in refs:
                    res.special[r.unit_id(doc_id)] = d
                res.sources.append(u.id)
                continue
            if re.search(r"có\s+hiệu\s+lực\s+(?:thi\s+hành\s+)?(?:kể\s+)?từ|theo\s+quy\s+định", s):
                res.todos.append(_todo(doc_id, u.id, s))
    return res


def _todo(doc_id: str, unit_id: str, detail: str) -> Todo:
    return Todo(
        doc_id=doc_id,
        unit_id=None,
        source_unit_id=unit_id,
        reason="hieu_luc_khong_ro",
        detail=detail[:500],
    )
