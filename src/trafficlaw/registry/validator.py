"""Kiểm tra danh mục văn bản: báo vấn đề, **không tự sửa, không tự điền**.

Mức độ:
- ``error``: dữ liệu mâu thuẫn hoặc vi phạm quy ước (trùng mã, quan hệ trỏ tới văn bản
  không có, ngày lệch thứ tự…) → script trả mã lỗi 1.
- ``warning``: thiếu dữ liệu (ngày, số hiệu, file gốc) — vấn đề đã biết, cần người bổ sung.
- ``info``: ghi chú vấn đề đã biết được khai báo tay trong trường ``issues``.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Literal

from trafficlaw.registry.loader import Registry
from trafficlaw.registry.schema import DocumentMeta
from trafficlaw.utils.dates import DATA_CUTOFF, day_before

Level = Literal["error", "warning", "info"]
LEVELS: tuple[Level, ...] = ("error", "warning", "info")

RAW_PREFIX = "data/raw/"
_ENDING_TYPES = ("THAY_THE", "BAI_BO")


@dataclass(frozen=True)
class Issue:
    level: Level
    code: str
    doc_id: str
    message: str

    def __str__(self) -> str:
        return f"[{self.level.upper()}] {self.code} {self.doc_id}: {self.message}"


def _so_hieu_parts(so_hieu: str) -> tuple[int | None, int | None]:
    """``"168/2024/NĐ-CP"`` → (168, 2024); ``"55/VBHN-VPQH"`` → (55, None)."""
    m = re.match(r"^\s*(\d+)\s*/", so_hieu)
    num = int(m[1]) if m else None
    y = re.search(r"/((?:19|20)\d\d)/", so_hieu)
    return num, (int(y[1]) if y else None)


def _check_document(d: DocumentMeta, cutoff: date) -> list[Issue]:
    out: list[Issue] = []

    def add(level: Level, code: str, msg: str) -> None:
        out.append(Issue(level, code, d.doc_id, msg))

    # Số hiệu
    if d.so_hieu is None:
        add("warning", "MISSING_SO_HIEU", "thiếu số hiệu")
    else:
        num, year = _so_hieu_parts(d.so_hieu)
        m = re.match(r"^[A-Z]+(\d+)", d.doc_id)
        if num is None:
            add("warning", "SO_HIEU_NO_NUMBER", f"số hiệu {d.so_hieu!r} không có số thứ tự")
        elif m is None or int(m[1]) != num:
            add("error", "SO_HIEU_MISMATCH", f"số hiệu {d.so_hieu!r} không khớp mã văn bản")
        if year is not None and f"-{year}" not in d.doc_id:
            add("error", "SO_HIEU_MISMATCH", f"năm trong số hiệu {d.so_hieu!r} không khớp mã")

    # Loại / tier
    if (d.loai == "vbhn") != (d.tier == "vbhn"):
        add("error", "LOAI_TIER", f"loai={d.loai} nhưng tier={d.tier}")
    if d.is_amendment and d.tier == "vbhn":
        add("error", "LOAI_TIER", "VBHN không thể là văn bản sửa đổi")

    # Ngày
    if d.ngay_ban_hanh is None:
        add("warning", "MISSING_NGAY_BAN_HANH", "thiếu ngày ban hành/xác thực")
    if d.hieu_luc_tu is None and d.tier != "vbhn":
        add("warning", "MISSING_HIEU_LUC_TU", "thiếu ngày có hiệu lực")
    if d.ngay_ban_hanh and d.hieu_luc_tu and d.hieu_luc_tu < d.ngay_ban_hanh:
        add("error", "DATE_ORDER", "hieu_luc_tu trước ngay_ban_hanh")
    if d.hieu_luc_tu and d.hieu_luc_den and d.hieu_luc_den < d.hieu_luc_tu:
        add("error", "DATE_ORDER", "hieu_luc_den trước hieu_luc_tu")
    if d.hieu_luc_den and d.hieu_luc_den < cutoff and d.tier not in ("historical", "vbhn"):
        add("warning", "EXPIRED_NOT_HISTORICAL", "đã hết hiệu lực nhưng không ở tier historical")

    # File gốc (chỉ kiểm tra cú pháp ở đây; tồn tại file kiểm tra riêng)
    if d.source_path is None:
        add("warning", "MISSING_SOURCE", "chưa có file gốc trong data/raw/")
    elif not d.source_path.startswith(RAW_PREFIX):
        add("error", "SOURCE_OUTSIDE_RAW", f"source_path phải nằm trong {RAW_PREFIX}")

    for text in d.issues:
        add("info", "KNOWN_ISSUE", text)
    return out


def _check_relations(d: DocumentMeta, reg: Registry, cutoff: date) -> list[Issue]:
    out: list[Issue] = []

    def add(level: Level, code: str, msg: str) -> None:
        out.append(Issue(level, code, d.doc_id, msg))

    hop_nhat = [r for r in d.relations if r.type == "HOP_NHAT"]
    if d.tier == "vbhn":
        if len(hop_nhat) != 1:
            add("error", "VBHN_TARGET", f"VBHN phải HOP_NHAT đúng 1 văn bản (có {len(hop_nhat)})")
        if len(hop_nhat) != len(d.relations):
            add("error", "VBHN_RELATION", "VBHN chỉ được có quan hệ HOP_NHAT")
    elif hop_nhat:
        add("error", "VBHN_RELATION", "chỉ VBHN mới có quan hệ HOP_NHAT")

    amend_targets: list[DocumentMeta] = []
    for r in d.relations:
        if r.target == d.doc_id:
            add("error", "REL_SELF", f"{r.type} trỏ tới chính nó")
            continue
        target = reg.get(r.target)
        if target is None:
            add("error", "REL_TARGET", f"{r.type} → {r.target}: không có trong danh mục")
            continue
        if target.tier == "vbhn":
            add("error", "REL_TARGET", f"{r.type} → {r.target}: không được trỏ tới VBHN")
        if r.type in ("SUA_DOI", "BAI_BO"):
            amend_targets.append(target)
        if r.type in ("SUA_DOI", *_ENDING_TYPES) and r.effective_from is None:
            add("warning", "REL_NO_DATE", f"{r.type} → {r.target}: thiếu effective_from")
        if r.effective_from and d.hieu_luc_tu and r.effective_from < d.hieu_luc_tu:
            add("error", "REL_DATE", f"{r.type} → {r.target}: có hiệu lực trước văn bản nguồn")
        # Thay thế/bãi bỏ toàn bộ từ ngày D → văn bản đích hết hiệu lực ngày D − 1.
        if r.type in _ENDING_TYPES and r.scope == "toan_bo" and r.effective_from:
            expected = day_before(r.effective_from)
            if target.hieu_luc_den is None:
                add(
                    "warning",
                    "TARGET_NO_END",
                    f"{r.type} toàn bộ {r.target} từ {r.effective_from}: "
                    f"{r.target}.hieu_luc_den đang trống (theo quan hệ là {expected})",
                )
            elif target.hieu_luc_den != expected:
                add(
                    "error",
                    "TARGET_END_MISMATCH",
                    f"{r.target}.hieu_luc_den={target.hieu_luc_den}, theo {r.type} phải là "
                    f"{expected}",
                )

    if d.is_amendment:
        if not amend_targets:
            add("error", "AMEND_NO_TARGET", "văn bản sửa đổi nhưng không có SUA_DOI/BAI_BO")
        elif d.tier not in {t.tier for t in amend_targets}:
            add("error", "AMEND_TIER", "tier phải trùng tier của văn bản bị sửa")

    # Văn bản ban hành sau mốc chốt chỉ nhập khi sửa văn bản tier A (CLAUDE.md mục 1).
    amends_tier_a = d.is_amendment and any(t.tier == "A" for t in amend_targets)
    if d.ngay_ban_hanh and d.ngay_ban_hanh > cutoff and d.tier != "vbhn" and not amends_tier_a:
        add("error", "AFTER_CUTOFF", f"ban hành sau mốc {cutoff} và không sửa văn bản tier A")
    return out


def check_source_files(reg: Registry, repo_root: str | Path) -> list[Issue]:
    """Báo file gốc khai báo mà không có trên đĩa (``data/raw`` không commit)."""
    root = Path(repo_root)
    return [
        Issue("warning", "SOURCE_NOT_FOUND", d.doc_id, f"không thấy file {d.source_path}")
        for d in reg
        if d.source_path and not (root / d.source_path).is_file()
    ]


def validate_registry(
    reg: Registry,
    *,
    repo_root: str | Path | None = None,
    cutoff: date = DATA_CUTOFF,
) -> list[Issue]:
    """Toàn bộ vấn đề của danh mục; ``repo_root`` khác None → kiểm tra cả file gốc."""
    issues: list[Issue] = []
    for doc_id, n in Counter(d.doc_id for d in reg).items():
        if n > 1:
            issues.append(Issue("error", "DUP_DOC_ID", doc_id, f"doc_id xuất hiện {n} lần"))
    so_hieu = Counter(d.so_hieu for d in reg if d.so_hieu)
    for d in reg:
        if d.so_hieu and so_hieu[d.so_hieu] > 1:
            issues.append(
                Issue("error", "DUP_SO_HIEU", d.doc_id, f"số hiệu {d.so_hieu!r} bị trùng")
            )
    for d in reg:
        issues.extend(_check_document(d, cutoff))
        issues.extend(_check_relations(d, reg, cutoff))
    if repo_root is not None:
        issues.extend(check_source_files(reg, repo_root))
    return issues


def count_by_level(issues: list[Issue]) -> dict[Level, int]:
    c = Counter(i.level for i in issues)
    return {lv: c.get(lv, 0) for lv in LEVELS}
