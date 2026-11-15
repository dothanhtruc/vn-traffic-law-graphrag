"""Sinh fixture ``tests/fixtures/mini_graph/`` (M6) từ ``data/graph`` thật — chạy lại khi M5 đổi.

    uv run python tests/fixtures/mini_graph/make_mini_graph.py

Chọn: cây con ND168 Đ6 (K3 m có 2 phiên bản, K1a bổ sung, K10 b có DAN_CHIEU ``to_tien``),
ND168 Đ12 K10 (dẫn chiếu vào Đ6), LUAT36 Đ6 / Đ7 K3 / Đ35 (``uy_quyen``) / Đ77 (đích HUONG_DAN
cấp unit), các VanBan liên quan (ND151, ND165 hướng dẫn; ND238 sửa đổi; ND218 → ND158 cặp cạnh
song song; VBHN144 → LUAT35 HOP_NHAT không có ngày). Giữ mọi cạnh có hai đầu nằm trong tập chọn,
cộng DAN_CHIEU từ phiên bản đã chọn tới VanBan/VanBanNgoai.

M11: thư mục con ``semantic/`` = nút/cạnh ngữ nghĩa M8 (``nodes_semantic.jsonl``,
``edges_semantic.jsonl``) của các phiên bản đã chọn (CheTai/DiemGPLX/BienPhapBoSung/HanhVi/
KhaiNiem nêu tại phiên bản đã chọn + PhuongTien/ChuThe được trỏ tới; cạnh có hai đầu trong tập).
Tách riêng để fixture M6 (3 file) không đổi; test M11 chép cả hai vào thư mục tạm.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "data/graph"
OUT = Path(__file__).resolve().parent
FILES = ("nodes.jsonl", "edges_struct.jsonl", "edges_legal.jsonl")

SUBTREES = ["ND168-2024/D6", "ND168-2024/D12/K10", "LUAT36-2024/D35"]
UNITS = ["LUAT36-2024/D6", "LUAT36-2024/D7/K3", "LUAT36-2024/D77"]
DOCS = [
    "ND168-2024",
    "ND238-2026",
    "LUAT36-2024",
    "LUAT35-2024",
    "ND151-2024",
    "ND165-2024",
    "ND218-2026",
    "ND158-2024",
    "VBHN144-2026-LQ-VPQH",
]


def read(name: str) -> list[dict]:
    return [json.loads(x) for x in (SRC / name).read_text(encoding="utf-8").splitlines() if x]


def main() -> None:
    nodes = read(FILES[0])
    struct, legal = read(FILES[1]), read(FILES[2])
    by_id = {n["id"]: n for n in nodes}
    parent = {e["src"]: e["dst"] for e in struct if e["type"] == "THUOC"}
    kids: dict[str, list[str]] = {}
    for c, p in parent.items():
        kids.setdefault(p, []).append(c)
    versions: dict[str, list[str]] = {}
    for e in struct:
        if e["type"] == "CO_PHIEN_BAN":
            versions.setdefault(e["src"], []).append(e["dst"])

    keep: set[str] = set(DOCS)
    for root in SUBTREES:
        stack = [root]
        while stack:
            u = stack.pop()
            keep.add(u)
            stack.extend(kids.get(u, []))
    keep.update(UNITS)
    for u in list(keep):  # tổ tiên
        cur = parent.get(u)
        while cur:
            keep.add(cur)
            cur = parent.get(cur)
    for e in legal:  # DAN_CHIEU từ phiên bản đã chọn tới văn bản
        src_unit = e["src"].rpartition("@v")[0]
        is_doc = by_id[e["dst"]]["label"] in ("VanBan", "VanBanNgoai")
        if e["type"] == "DAN_CHIEU" and src_unit in keep and is_doc:
            keep.add(e["dst"])
    for u in list(keep):
        keep.update(versions.get(u, []))

    out_nodes = [n for n in nodes if n["id"] in keep]
    for name, edges in ((FILES[1], struct), (FILES[2], legal)):
        rows = [e for e in edges if e["src"] in keep and e["dst"] in keep]
        write(OUT / name, rows)
        print(name, len(rows))
    write(OUT / FILES[0], out_nodes)
    print(FILES[0], len(out_nodes))
    write_semantic(keep)


def write_semantic(keep: set[str]) -> None:
    if not (SRC / "nodes_semantic.jsonl").is_file():
        print("không có file ngữ nghĩa — bỏ qua semantic/")
        return
    sn, se = read("nodes_semantic.jsonl"), read("edges_semantic.jsonl")
    by_id = {n["id"]: n for n in sn}
    stated = {n["id"] for n in sn if n["props"].get("version_id") in keep}
    edges = [e for e in se if e["src"] in keep and (e["dst"] in stated or e["dst"] in by_id)]
    # Cạnh tới nút ngữ nghĩa nêu ngoài tập chọn chỉ giữ khi nút đó là PT/CT (danh mục).
    edges = [
        e
        for e in edges
        if e["dst"] in stated or by_id[e["dst"]]["label"] in ("PhuongTien", "ChuThe")
    ]
    ids = stated | {e["dst"] for e in edges}
    out = OUT / "semantic"
    out.mkdir(exist_ok=True)
    write(out / "nodes_semantic.jsonl", [n for n in sn if n["id"] in ids])
    write(out / "edges_semantic.jsonl", edges)
    print("semantic", len(ids), "nút,", len(edges), "cạnh")


def write(path: Path, rows: list[dict]) -> None:
    text = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    path.write_bytes(text.encode("utf-8"))  # luôn LF (write_text trên Windows ghi CRLF)


if __name__ == "__main__":
    main()
