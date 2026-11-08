"""Tiện ích chung cho test M4: dựng unit từ trích đoạn văn bản thật ở ``tests/fixtures``."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from trafficlaw.ingest.structure import Unit, parse_structure
from trafficlaw.registry.loader import Registry, load_registry

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = REPO_ROOT / "tests" / "fixtures"


def registry() -> Registry:
    return load_registry(REPO_ROOT / "data" / "registry" / "documents.yaml")


def units_of(doc_id: str, *fixtures: str) -> list[Unit]:
    """Unit của ``doc_id`` từ một hay nhiều trích đoạn (mỗi trích đoạn tách riêng)."""
    out: list[Unit] = []
    seen: set[str] = set()
    for name in fixtures:
        text = (FIXTURES / name).read_text(encoding="utf-8")
        for u in parse_structure(doc_id, text).units:
            if u.id not in seen:
                seen.add(u.id)
                out.append(u)
    return out


def unit(uid: str, level: str, text: str, title: str | None = None) -> Unit:
    """Unit dựng tay (cho câu đơn lẻ lấy nguyên văn từ văn bản)."""
    parent = uid.rsplit("/", 1)[0] if "/" in uid else None
    return Unit(
        id=uid,
        doc_id=uid.split("/")[0],
        level=level,  # type: ignore[arg-type]
        title=title,
        text=text,
        parent_id=parent,
        line_start=1,
    )


D = date
