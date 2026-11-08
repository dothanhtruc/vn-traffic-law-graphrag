"""Phiên bản điều khoản theo thời gian (``unit_versions.jsonl``) và hàm chuẩn ``get_version``.

Quy ước (CLAUDE.md mục 7):

- Khoảng hiệu lực ``[effective_from, effective_to]`` bao gồm cả hai đầu; ``effective_to=None``
  là còn hiệu lực; ``effective_from=None`` (thiếu ngày) → không bao giờ có hiệu lực.
- ``status``: ``active`` (phiên bản đang mở), ``amended`` (đã bị thay bởi phiên bản sau),
  ``repealed`` (unit bị bãi bỏ từ ``effective_from``; ``text`` rỗng).
- ``version``: 0 = bản gốc khi ban hành; unit do văn bản sửa đổi bổ sung bắt đầu từ 1.
- Unit bổ sung (chưa có trong ``units.jsonl``) nằm ở ``units_added.jsonl`` (:class:`AddedUnit`).
"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import date
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict

from trafficlaw.ingest.structure import Unit
from trafficlaw.utils.dates import in_effect
from trafficlaw.utils.jsonl import read_jsonl

VersionStatus = Literal["active", "amended", "repealed"]


class UnitVersion(BaseModel):
    """Một dòng ``unit_versions.jsonl``."""

    model_config = ConfigDict(extra="forbid")

    unit_id: str
    version: int
    text: str
    effective_from: date | None
    effective_to: date | None = None
    status: VersionStatus
    #: Điều khoản của văn bản gây ra phiên bản này (null với bản gốc).
    source_unit_id: str | None = None


class AddedUnit(Unit):
    """Unit do văn bản sửa đổi bổ sung (một dòng ``units_added.jsonl``).

    Cùng schema :class:`Unit` (``text`` = nội dung khi được bổ sung, ``source_path`` = file của
    văn bản sửa đổi), ``line_start`` = null, thêm vị trí trong cây và nguồn.
    """

    line_start: int | None = None  # type: ignore[assignment]
    #: Unit anh em đứng ngay trước / ngay sau (theo câu "vào sau/trước"); cả hai null → cuối.
    after_id: str | None = None
    before_id: str | None = None
    source_unit_id: str


def select_version(
    versions: Iterable[UnitVersion], as_of: date, *, include_repealed: bool = False
) -> UnitVersion | None:
    """Phiên bản có hiệu lực tại ``as_of`` trong danh sách phiên bản của **một** unit."""
    for v in versions:
        if in_effect(as_of, v.effective_from, v.effective_to):
            if v.status == "repealed" and not include_repealed:
                return None
            return v
    return None


class VersionStore:
    """Tra cứu phiên bản theo ``unit_id`` (nạp toàn bộ ``unit_versions.jsonl`` vào bộ nhớ)."""

    def __init__(self, versions: Iterable[UnitVersion]) -> None:
        self._by_unit: dict[str, list[UnitVersion]] = {}
        for v in versions:
            self._by_unit.setdefault(v.unit_id, []).append(v)
        for lst in self._by_unit.values():
            lst.sort(key=lambda v: v.version)

    @classmethod
    def load(cls, path: str | Path) -> VersionStore:
        return cls(UnitVersion.model_validate(r) for r in read_jsonl(path))

    def __contains__(self, unit_id: object) -> bool:
        return unit_id in self._by_unit

    def __len__(self) -> int:
        return len(self._by_unit)

    def unit_ids(self) -> list[str]:
        return list(self._by_unit)

    def versions_of(self, unit_id: str) -> list[UnitVersion]:
        return list(self._by_unit.get(unit_id, ()))

    def get_version(
        self, unit_id: str, as_of: date, *, include_repealed: bool = False
    ) -> UnitVersion | None:
        """Phiên bản của ``unit_id`` có hiệu lực tại ``as_of``.

        ``None`` khi unit chưa có hiệu lực, thiếu ngày, đã bị bãi bỏ (trừ khi
        ``include_repealed=True`` thì trả về bản ghi ``repealed``), hoặc không tồn tại.
        """
        return select_version(
            self._by_unit.get(unit_id, ()), as_of, include_repealed=include_repealed
        )
