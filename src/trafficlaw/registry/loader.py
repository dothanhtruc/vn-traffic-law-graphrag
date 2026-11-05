"""Nạp danh mục văn bản từ YAML."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import yaml

from trafficlaw.registry.schema import DocumentMeta


class Registry:
    """Danh sách văn bản giữ nguyên thứ tự trong file, tra cứu theo ``doc_id``.

    Không tự loại bản ghi trùng ``doc_id``: validator cần thấy để báo lỗi.
    """

    def __init__(self, documents: list[DocumentMeta]) -> None:
        self.documents = documents
        self._by_id: dict[str, DocumentMeta] = {}
        for d in documents:
            self._by_id.setdefault(d.doc_id, d)

    def __len__(self) -> int:
        return len(self.documents)

    def __iter__(self) -> Iterator[DocumentMeta]:
        return iter(self.documents)

    def __contains__(self, doc_id: object) -> bool:
        return doc_id in self._by_id

    def get(self, doc_id: str) -> DocumentMeta | None:
        return self._by_id.get(doc_id)

    def __getitem__(self, doc_id: str) -> DocumentMeta:
        return self._by_id[doc_id]

    def indexable(self) -> list[DocumentMeta]:
        """Văn bản được chỉ mục độc lập (bỏ VBHN và văn bản sửa đổi)."""
        return [d for d in self.documents if d.indexable]


def parse_registry(data: object) -> Registry:
    """``{"documents": [...]}`` → :class:`Registry`; sai schema → ``pydantic.ValidationError``."""
    if not isinstance(data, dict) or not isinstance(data.get("documents"), list):
        raise ValueError("Danh mục phải có dạng {documents: [...]}")
    return Registry([DocumentMeta.model_validate(d) for d in data["documents"]])


def load_registry(path: str | Path) -> Registry:
    with Path(path).open(encoding="utf-8") as fh:
        return parse_registry(yaml.safe_load(fh))
