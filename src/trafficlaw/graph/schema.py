"""Schema đồ thị dạng JSONL (M5): ``nodes.jsonl``, ``edges_struct.jsonl``, ``edges_legal.jsonl``.

Mỗi dòng nút: ``{id, label, props}``; mỗi dòng cạnh: ``{type, src, dst, props}``. M6
(``GraphStore``) đọc các file này; mã nút là khóa ổn định:

- ``VanBan``: ``doc_id`` (unit ``van_ban`` của văn bản gộp vào nút này);
- ``Phan``/``Chuong``/``Muc``/``Dieu``/``Khoan``/``Diem``/``PhuLuc``: ``unit_id``;
- ``PhienBan``: ``<unit_id>@v<version>``;
- ``VanBanNgoai``: ``EXT:<số hiệu chuẩn hoá>`` hoặc ``EXT:<TEN-KHONG-DAU>``.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

NodeLabel = Literal[
    "VanBan",
    "VanBanNgoai",
    "Phan",
    "Chuong",
    "Muc",
    "Dieu",
    "Khoan",
    "Diem",
    "PhuLuc",
    "PhienBan",
]
StructEdgeType = Literal["THUOC", "KE_TIEP", "CO_PHIEN_BAN"]
LegalEdgeType = Literal["SUA_DOI", "THAY_THE", "BAI_BO", "HUONG_DAN", "DAN_CHIEU", "HOP_NHAT"]

NODE_LABEL_ORDER: tuple[str, ...] = (
    "VanBan",
    "VanBanNgoai",
    "Phan",
    "Chuong",
    "Muc",
    "Dieu",
    "Khoan",
    "Diem",
    "PhuLuc",
    "PhienBan",
)
STRUCT_EDGE_TYPES: tuple[str, ...] = ("THUOC", "KE_TIEP", "CO_PHIEN_BAN")
LEGAL_EDGE_TYPES: tuple[str, ...] = (
    "SUA_DOI",
    "BAI_BO",
    "THAY_THE",
    "HOP_NHAT",
    "HUONG_DAN",
    "DAN_CHIEU",
)

LEVEL_LABEL: dict[str, str] = {
    "van_ban": "VanBan",
    "phan": "Phan",
    "chuong": "Chuong",
    "muc": "Muc",
    "dieu": "Dieu",
    "khoan": "Khoan",
    "diem": "Diem",
    "phu_luc": "PhuLuc",
}

#: Giới hạn Neo4j AuraDB Free (CLAUDE.md mục 2).
MAX_NODES = 200_000
MAX_EDGES = 400_000


class Node(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    label: NodeLabel
    props: dict[str, Any] = {}


class Edge(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: StructEdgeType | LegalEdgeType
    src: str
    dst: str
    props: dict[str, Any] = {}


def version_node_id(unit_id: str, version: int) -> str:
    """``ND168-2024/D6/K3/m`` + 1 → ``ND168-2024/D6/K3/m@v1``."""
    return f"{unit_id}@v{version}"
