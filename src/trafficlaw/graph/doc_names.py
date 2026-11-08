"""Nhận diện tên/số hiệu văn bản trong câu văn xuôi → ``doc_id`` (danh mục) hoặc ``EXT:…``.

Ba cách một văn bản được nhắc tới:

- **"… này"** (``Luật này``, ``Nghị định này``) → chính văn bản chứa câu (``self``).
- **Số hiệu** (``Nghị định số 135/2021/NĐ-CP``, ``Thông tư 24/2023/TT-BCA``,
  ``Luật số 16/2023/QH15``)
  → so với ``so_hieu`` của danh mục sau chuẩn hoá (:func:`norm_so_hieu`); không có → văn bản
  ngoài danh mục ``EXT:<số hiệu chuẩn hoá>``.
- **Tên** (chỉ với Luật/Bộ luật/Pháp lệnh — nghị định, thông tư được gọi bằng số hiệu):
  so khớp **dài nhất** với bảng tên = ``ten`` của các Luật trong danh mục + ``aliases`` và
  ``external_names`` trong ``data/registry/doc_aliases.yaml``. Không có trong bảng → lấy các
  từ sau chữ "Luật" tới dấu câu hoặc từ chức năng (``ngày``, ``năm``, ``và``, ``theo``…) →
  ``EXT:<TEN-KHONG-DAU>``. Tên luật có dấu phẩy/"và"/"theo" ("Luật Phòng, chống thiên tai",
  "Luật Phí và lệ phí") phải nằm trong ``external_names``, nếu không sẽ bị cắt ngắn.
- ``Luật sửa đổi, bổ sung một số điều của Luật X …`` → một văn bản ngoài danh mục riêng (tên
  đầy đủ gồm cả các luật bị sửa).

Tên viết thường ("theo quy định của luật") không được nhận.
"""

from __future__ import annotations

import re
import unicodedata
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import yaml

from trafficlaw.registry.schema import DocumentMeta

MentionKind = Literal["self", "registry", "external"]

EXT_PREFIX = "EXT:"

_TYPE_WORDS: dict[str, str] = {
    "Bộ luật": "bo_luat",
    "Luật": "luat",
    "Pháp lệnh": "phap_lenh",
    "Nghị quyết": "nghi_quyet",
    "Nghị định": "nghi_dinh",
    "Thông tư liên tịch": "thong_tu_lien_tich",
    "Thông tư": "thong_tu",
    "Quyết định": "quyet_dinh",
}
_NAMED_TYPES = ("Bộ luật", "Luật", "Pháp lệnh")

_W = r"[\wÀ-ỹ]"
_END = rf"(?!{_W})"
_TYPE_RE = re.compile(
    rf"(?<!{_W})(Bộ luật|Thông tư liên tịch|"
    + "|".join(re.escape(t) for t in _TYPE_WORDS if t not in ("Bộ luật", "Thông tư liên tịch"))
    + rf"){_END}"
)
_SO_HIEU = r"\d+/\d{4}/[A-Za-zĐđ0-9&]+(?:-[A-Za-zĐđ0-9&]+)*"
_NUMBER_AFTER = re.compile(rf"\s+(?:số\s*:?\s*)?({_SO_HIEU})")
_SELF_AFTER = re.compile(rf"\s+này{_END}")
_AMEND_LAW = re.compile(
    r"\s+sửa\s+đổi,\s+bổ\s+sung\s+(?:một\s+số\s+điều\s+)?của\s+(?:các\s+)?(?=Luật|Bộ luật)"
)
_STOP_WORDS = frozenset(
    [
        "ngày",
        "năm",
        "số",
        "và",
        "hoặc",
        "để",
        "thì",
        "khi",
        "được",
        "có",
        "đã",
        "đang",
        "sẽ",
        "theo",
        "đối",
        "trong",
        "tại",
        "của",
        "về",
        "này",
        "sau",
        "trước",
        "thuộc",
        "như",
        "với",
        "do",
        "bởi",
        "các",
        "mà",
        "là",
        "nhằm",
        "cho",
        "phải",
        "gồm",
        "bao",
        "không",
        "nếu",
        "trừ",
        "hiện",
        "quy",
        "điều",
        "đến",
        "từ",
        "mới",
        "cũ",
        "đều",
        "cũng",
        "nhưng",
        "nên",
    ]
)
_WORD = re.compile(rf"\s+({_W}+)")


def _nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def norm_so_hieu(s: str) -> str:
    """``"168/2024/NĐ-CP"``, ``"168/2024/nd-cp "`` → ``"168/2024/NĐ-CP"`` (chữ hoa, bỏ khoảng)."""
    s = re.sub(r"\s+", "", _nfc(s)).upper().rstrip("-.")
    return re.sub(r"(?<=/)(N|Q)D(?=-)", lambda m: m[1] + "Đ", s)


def slug(name: str) -> str:
    """``"Luật Xử lý vi phạm hành chính"`` → ``"LUAT-XU-LY-VI-PHAM-HANH-CHINH"``."""
    s = _nfc(name).replace("đ", "d").replace("Đ", "D")
    s = "".join(ch for ch in unicodedata.normalize("NFD", s) if not unicodedata.combining(ch))
    return re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").upper()


def _name_key(name: str) -> str:
    return re.sub(r"\s+", " ", _nfc(name)).strip().lower()


@dataclass(frozen=True)
class DocMention:
    """Một lần nhắc tới văn bản trong câu: ``text[start:end]``."""

    start: int
    end: int
    text: str
    kind: MentionKind
    #: ``doc_id`` (danh mục) hoặc ``EXT:…``; ``None`` với ``self``.
    doc: str | None
    loai: str
    so_hieu: str | None = None
    ten: str | None = None


class DocNameTable:
    """Bảng tên/số hiệu văn bản (hàm thuần, không I/O)."""

    def __init__(
        self,
        documents: Iterable[DocumentMeta],
        aliases: Mapping[str, Sequence[str]] | None = None,
        external_names: Sequence[str] = (),
        excluded: Sequence[str] = (),
    ) -> None:
        self.by_so_hieu: dict[str, str] = {}
        self.names: dict[str, tuple[str, str]] = {}  # name_key → (doc|EXT, tên chuẩn)
        docs = list(documents)
        for d in docs:
            if d.so_hieu:
                self.by_so_hieu[norm_so_hieu(d.so_hieu)] = d.doc_id
            if d.loai == "luat" and d.ten:
                self.names[_name_key(d.ten)] = (d.doc_id, _nfc(d.ten))
        known = {d.doc_id for d in docs}
        for doc_id, names in (aliases or {}).items():
            if doc_id not in known:
                raise ValueError(f"doc_aliases: {doc_id!r} không có trong danh mục")
            for n in names:
                self.names[_name_key(n)] = (doc_id, _nfc(n))
        for n in external_names:
            key = _name_key(n)
            if key in self.names:
                raise ValueError(f"doc_aliases: tên ngoài danh mục trùng tên trong danh mục: {n!r}")
            self.names[key] = (EXT_PREFIX + slug(n), _nfc(n))
        #: Văn bản đã hết hiệu lực, không dùng (CLAUDE.md mục 6): vẫn nhận diện để dẫn chiếu
        #: không bị gán nhầm, nhưng không tạo nút/cạnh tới chúng.
        self.excluded: set[str] = set()
        for x in excluded:
            if "/" in x:
                self.excluded.add(EXT_PREFIX + norm_so_hieu(x))
            else:
                self.excluded.add(EXT_PREFIX + slug(x))
                self.names.setdefault(_name_key(x), (EXT_PREFIX + slug(x), _nfc(x)))
        # Tên dài trước: "Luật Quy hoạch đô thị và nông thôn" thắng "Luật Quy hoạch".
        ordered = sorted(self.names, key=len, reverse=True)
        self._name_re = (
            re.compile(
                "("
                + "|".join(r"\s+".join(map(re.escape, k.split(" "))) for k in ordered)
                + rf"){_END}",
                re.I,
            )
            if ordered
            else None
        )

    # ------------------------------------------------------------ tra cứu

    def doc_for_so_hieu(self, so_hieu: str) -> tuple[MentionKind, str]:
        norm = norm_so_hieu(so_hieu)
        if norm in self.by_so_hieu:
            return "registry", self.by_so_hieu[norm]
        return "external", EXT_PREFIX + norm

    def _known_name_at(self, text: str, pos: int) -> tuple[int, str, str] | None:
        if self._name_re is None:
            return None
        m = self._name_re.match(text, pos)
        if not m or not text[pos].isupper():
            return None
        doc, ten = self.names[_name_key(m[1])]
        return m.end(), doc, ten

    def _heuristic_name_end(self, text: str, pos: int) -> int | None:
        """Hết tên luật ngoài bảng: ``pos`` là đầu từ sau "Luật"; từ đầu phải viết hoa."""
        m = _WORD.match(text, pos)
        if not m or not m[1][0].isupper():
            return None
        end = m.end()
        while (m := _WORD.match(text, end)) and m[1].lower() not in _STOP_WORDS:
            end = m.end()
        return end

    def match_at(self, text: str, pos: int) -> DocMention | None:
        """Lần nhắc văn bản bắt đầu **đúng** tại ``pos`` ("Luật"/"Nghị định"…), hoặc ``None``."""
        m = _TYPE_RE.match(text, pos)
        if not m:
            return None
        word = m[1]
        loai = _TYPE_WORDS[word]
        after = m.end()
        if s := _SELF_AFTER.match(text, after):
            return DocMention(pos, s.end(), text[pos : s.end()], "self", None, loai)
        if n := _NUMBER_AFTER.match(text, after):
            kind, doc = self.doc_for_so_hieu(n[1])
            return DocMention(
                pos, n.end(), text[pos : n.end()], kind, doc, loai, so_hieu=norm_so_hieu(n[1])
            )
        if word not in _NAMED_TYPES:
            return None
        known = self._known_name_at(text, pos)
        if known is not None:
            end, doc, ten = known
            # "Luật Đường bộ số 35/2024/QH15": số hiệu đứng sau tên quyết định văn bản.
            if n := _NUMBER_AFTER.match(text, end):
                kind, doc2 = self.doc_for_so_hieu(n[1])
                return DocMention(pos, n.end(), text[pos : n.end()], kind, doc2, loai, ten=ten)
            kind = "external" if doc.startswith(EXT_PREFIX) else "registry"
            return DocMention(pos, end, text[pos:end], kind, doc, loai, ten=ten)
        if a := _AMEND_LAW.match(text, after):
            inner = self.match_at(text, a.end())
            if inner is not None and inner.kind != "self":
                end = inner.end
                # "… của Luật A và Luật B" → gồm cả luật thứ hai.
                while (j := re.match(r"\s+và\s+(?=Luật|Bộ luật)", text[end:])) and (
                    nxt := self.match_at(text, end + j.end())
                ):
                    end = nxt.end
                ten = re.sub(r"\s+", " ", text[pos:end])
                return DocMention(
                    pos, end, text[pos:end], "external", EXT_PREFIX + slug(ten), loai, ten=ten
                )
            return None
        end = self._heuristic_name_end(text, after)
        if end is None:
            return None
        ten = re.sub(r"\s+", " ", text[pos:end])
        if n := _NUMBER_AFTER.match(text, end):
            kind, doc = self.doc_for_so_hieu(n[1])
            return DocMention(pos, n.end(), text[pos : n.end()], kind, doc, loai, ten=ten)
        return DocMention(
            pos, end, text[pos:end], "external", EXT_PREFIX + slug(ten), loai, ten=ten
        )

    def find_all(self, text: str) -> list[DocMention]:
        """Mọi lần nhắc văn bản trong ``text`` (không chồng nhau, theo thứ tự)."""
        out: list[DocMention] = []
        pos = 0
        while (m := _TYPE_RE.search(text, pos)) is not None:
            mention = self.match_at(text, m.start())
            if mention is None:
                pos = m.end()
                continue
            out.append(mention)
            pos = mention.end
        return out


def load_doc_aliases(path: str | Path) -> tuple[dict[str, list[str]], list[str], list[str]]:
    """``doc_aliases.yaml`` → ``(aliases {doc_id: [tên]}, external_names, excluded)``."""
    p = Path(path)
    if not p.exists():
        return {}, [], []
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    aliases = {str(k): [_nfc(str(x)) for x in v] for k, v in (data.get("aliases") or {}).items()}
    external = [_nfc(str(x)) for x in data.get("external_names") or []]
    excluded = [_nfc(str(x)) for x in data.get("excluded") or []]
    return aliases, external, excluded
