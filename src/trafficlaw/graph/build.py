"""Dựng nút + cạnh của đồ thị từ danh mục, unit, unit bổ sung và phiên bản (hàm thuần, M5).

Quy tắc (CLAUDE.md "Quy ước đồ thị (M5)"):

- **Nút**: mọi văn bản trong danh mục → ``VanBan`` (văn bản sửa đổi, VBHN chỉ có nút này);
  unit của văn bản chỉ mục được (``DocumentMeta.indexable``) + unit bổ sung → nút theo cấp;
  mỗi phiên bản → ``PhienBan``; văn bản ngoài danh mục được nhắc tới → ``VanBanNgoai``.
- **THUOC** con → cha (``parent_id``; không có thì văn bản). **KE_TIEP** anh em liền nhau theo
  thứ tự trong văn bản, gồm unit bổ sung (``versions.unit_tree``). **CO_PHIEN_BAN** unit →
  phiên bản (unit ``van_ban`` ≡ nút ``VanBan``).
- **SUA_DOI / BAI_BO** (cấp unit): phiên bản ``version > 0`` có ``source_unit_id`` → cạnh từ
  ``VanBan`` của văn bản sửa đổi tới unit; ``repealed`` → ``BAI_BO``. Unit có cha cũng được
  chính chỉ dẫn đó (cùng ``source_unit_id``, cùng ngày) tạo phiên bản → bỏ (cạnh của cha
  đã bao). Bãi bỏ/thay thế **toàn bộ** văn bản (TT14 → TT35) chỉ có cạnh cấp văn bản.
- **SUA_DOI / BAI_BO / THAY_THE / HOP_NHAT cấp văn bản**: từ ``relations`` của danh mục
  (``props.cap = "van_ban"``).
- **DAN_CHIEU**: từ ``PhienBan`` (text đổi theo phiên bản) tới unit / ``VanBan`` /
  ``VanBanNgoai``; ``effective_from/to`` của phiên bản nguồn. Dẫn chiếu tới chính unit nguồn
  ("khoản này") hoặc tổ tiên ("Điều này" trong một Khoản) vẫn tạo cạnh, đánh dấu
  ``props.quan_he = "chinh_unit" | "to_tien"`` (quyết định 08/11/2026).
  Đích không tồn tại → ``unresolved`` (không tạo cạnh).
- **HUONG_DAN**: từ ``VanBan`` của nghị định/thông tư/quyết định tới văn bản (và unit cụ thể)
  mà phần mở đầu / Điều 1 nói là "quy định chi tiết / hướng dẫn thi hành".
- **uy_quyen** (thuộc tính nút): câu "<cơ quan> quy định chi tiết <REFS>" trong Luật.
"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from typing import Any

from trafficlaw.graph.doc_names import EXT_PREFIX, DocNameTable
from trafficlaw.graph.references import (
    DocScope,
    Reference,
    delegations,
    extract_references,
    guidance_references,
    header_scope,
)
from trafficlaw.graph.schema import (
    LEGAL_EDGE_TYPES,
    LEVEL_LABEL,
    NODE_LABEL_ORDER,
    STRUCT_EDGE_TYPES,
    Edge,
    Node,
    version_node_id,
)
from trafficlaw.ingest.structure import Unit
from trafficlaw.ingest.versions import AddedUnit, UnitVersion, unit_tree
from trafficlaw.registry.loader import Registry
from trafficlaw.utils.dates import to_iso


@dataclass
class GraphData:
    nodes: list[Node]
    edges_struct: list[Edge]
    edges_legal: list[Edge]
    #: ``{doc_id: Counter}``: spans, resolved, loi_doc, dich_khong_ton_tai,
    #: phu_luc_khong_co_unit, chinh_unit, to_tien, nhac_van_ban.
    ref_stats: dict[str, Counter[str]]
    unresolved: list[dict[str, Any]]
    #: Lỗi dữ liệu đầu vào (phiên bản không có unit…) — pipeline thoát mã 1.
    errors: list[str] = field(default_factory=list)


_CAN_CU = re.compile(r"\s*Căn\s+cứ")


def _is_can_cu(text: str, pos: int) -> bool:
    return bool(_CAN_CU.match(text, text.rfind("\n", 0, pos) + 1))


class _Builder:
    def __init__(
        self,
        registry: Registry,
        units: Sequence[Unit],
        added: Sequence[AddedUnit],
        versions: Sequence[UnitVersion],
        names: DocNameTable,
    ) -> None:
        self.registry = registry
        self.names = names
        self.docs = {d.doc_id: d for d in registry}
        self.indexable = {d.doc_id for d in registry if d.indexable}
        self.units: list[Unit] = [u for u in units if u.doc_id in self.indexable]
        self.added: list[AddedUnit] = [a for a in added if a.doc_id in self.indexable]
        self.unit_by_id: dict[str, Unit] = {u.id: u for u in [*self.units, *self.added]}
        self.parent: dict[str, str] = {}
        for u in self.unit_by_id.values():
            if u.level != "van_ban":
                self.parent[u.id] = u.parent_id or u.doc_id
        self.versions: dict[str, list[UnitVersion]] = defaultdict(list)
        for v in versions:
            self.versions[v.unit_id].append(v)
        for lst in self.versions.values():
            lst.sort(key=lambda v: v.version)
        self.errors: list[str] = []
        for uid in sorted(self.versions):
            if uid not in self.unit_by_id:
                self.errors.append(f"phiên bản của unit không có trong units/units_added: {uid}")
        self.children = unit_tree(self.units, self.added)
        self.node_ids: set[str] = set()
        self.ext: dict[str, dict[str, Any]] = {}
        self.legal: dict[tuple[str, ...], Edge] = {}
        self.ref_stats: dict[str, Counter[str]] = defaultdict(Counter)
        self.unresolved: list[dict[str, Any]] = []

    # ------------------------------------------------------------ nút + cấu trúc

    def nodes_and_struct(self) -> tuple[list[Node], list[Edge]]:
        nodes: list[Node] = []
        struct: list[Edge] = []
        for d in self.registry:
            nodes.append(
                Node(
                    id=d.doc_id,
                    label="VanBan",
                    props={
                        "doc_id": d.doc_id,
                        "so_hieu": d.so_hieu,
                        "ten": d.ten,
                        "loai": d.loai,
                        "co_quan": d.co_quan,
                        "tier": d.tier,
                        "hieu_luc_tu": to_iso(d.hieu_luc_tu),
                        "hieu_luc_den": to_iso(d.hieu_luc_den),
                        "is_amendment": d.is_amendment,
                        "indexable": d.indexable,
                    },
                )
            )
        for u in self.unit_by_id.values():
            if u.level == "van_ban":
                continue
            props: dict[str, Any] = {
                "doc_id": u.doc_id,
                "level": u.level,
                "number": u.number,
                "title": u.title,
            }
            if u.label_in_source is not None:
                props["label_in_source"] = u.label_in_source
            if isinstance(u, AddedUnit):
                props["bo_sung"] = True
                props["source_unit_id"] = u.source_unit_id
            nodes.append(Node(id=u.id, label=LEVEL_LABEL[u.level], props=props))  # type: ignore[arg-type]
            struct.append(Edge(type="THUOC", src=u.id, dst=self.parent[u.id]))
        for parent, kids in self.children.items():
            if parent.split("/")[0] not in self.indexable:
                continue
            for a, b in zip(kids, kids[1:], strict=False):
                struct.append(Edge(type="KE_TIEP", src=a, dst=b))
        for uid, vs in self.versions.items():
            for v in vs:
                vid = version_node_id(uid, v.version)
                nodes.append(
                    Node(
                        id=vid,
                        label="PhienBan",
                        props={
                            "unit_id": uid,
                            "version": v.version,
                            "text": v.text,
                            "effective_from": to_iso(v.effective_from),
                            "effective_to": to_iso(v.effective_to),
                            "status": v.status,
                            "source_unit_id": v.source_unit_id,
                        },
                    )
                )
                struct.append(Edge(type="CO_PHIEN_BAN", src=uid, dst=vid))
        self.node_ids = {n.id for n in nodes}
        return nodes, struct

    # ------------------------------------------------------------ cạnh pháp lý

    def _add(self, etype: str, src: str, dst: str, props: dict[str, Any], *key: Any) -> None:
        k = (etype, src, dst, *map(str, key))
        if k not in self.legal:
            self.legal[k] = Edge(type=etype, src=src, dst=dst, props=props)  # type: ignore[arg-type]

    def _ancestors(self, uid: str) -> set[str]:
        out: set[str] = set()
        while uid in self.parent:
            uid = self.parent[uid]
            out.add(uid)
        return out

    def registry_relations(self) -> None:
        for d in self.registry:
            for r in d.relations:
                eff = r.effective_from or d.hieu_luc_tu
                props = {
                    "cap": "van_ban",
                    "scope": r.scope,
                    "effective_from": to_iso(eff),
                    "effective_to": None,
                    "note": r.note,
                }
                self._add(r.type, d.doc_id, r.target, props)

    def amendment_edges(self) -> None:
        whole = {
            (d.doc_id, r.target)
            for d in self.registry
            for r in d.relations
            if r.scope == "toan_bo" and r.type in ("BAI_BO", "THAY_THE")
        }
        made: dict[str, set[tuple[str, str | None]]] = defaultdict(set)
        for uid, vs in self.versions.items():
            for v in vs:
                if v.version > 0 and v.source_unit_id:
                    made[uid].add((v.source_unit_id, to_iso(v.effective_from)))
        for uid in sorted(self.versions):
            vs = self.versions[uid]
            first = vs[0].version
            for v in vs:
                if v.version == 0 or not v.source_unit_id:
                    continue
                src_doc = v.source_unit_id.split("/")[0]
                if (src_doc, uid.split("/")[0]) in whole:
                    continue
                key = (v.source_unit_id, to_iso(v.effective_from))
                if key in made.get(self.parent.get(uid, ""), ()):
                    continue  # chỉ dẫn thay cả cha: cạnh của cha đã bao
                if v.status == "repealed":
                    etype, op = "BAI_BO", "bai_bo"
                else:
                    added = isinstance(self.unit_by_id.get(uid), AddedUnit)
                    etype, op = "SUA_DOI", "bo_sung" if added and v.version == first else "sua_doi"
                props = {
                    "cap": "unit",
                    "thao_tac": op,
                    "source_unit_id": v.source_unit_id,
                    "version": v.version,
                    "effective_from": to_iso(v.effective_from),
                    "effective_to": None,
                }
                self._add(etype, src_doc, uid, props, v.version)

    def _scopes(self) -> dict[str, DocScope | None]:
        """Phạm vi văn bản áp cho text của mỗi unit.

        Kế thừa từ câu dẫn của tổ tiên; câu dẫn sửa đổi của **chính** unit ("4. Sửa đổi khoản 5
        … Điều 51 của Luật Điện lực …" kèm khối trích dẫn) áp cho cả text của nó.
        """
        out: dict[str, DocScope | None] = {}
        stack: list[tuple[str, DocScope | None]] = [
            (d, None) for d in sorted(self.indexable) if d in self.unit_by_id
        ]
        while stack:
            uid, inherited = stack.pop()
            u = self.unit_by_id[uid]
            own = header_scope(u.text, uid, self.names) if u.level != "van_ban" else None
            out[uid] = own if own is not None and own.reason == "sua_doi" else inherited
            for kid in self.children.get(uid, ()):
                if kid in self.unit_by_id:
                    stack.append((kid, own or inherited))
        return out

    def _ext_node(self, ref: Reference) -> None:
        if ref.doc not in self.ext and ref.mention is not None:
            mn = ref.mention
            self.ext[ref.doc] = {"so_hieu": mn.so_hieu, "ten": mn.ten, "loai": mn.loai}

    def _targets(
        self, ref: Reference, src_unit: str
    ) -> tuple[list[tuple[str, str | None, str | None]], list[str]]:
        """``([(đích, target_ref, quan_he)], [đích không tồn tại])``.

        ``quan_he``: ``chinh_unit`` (đích là unit nguồn), ``to_tien`` (đích là tổ tiên của unit
        nguồn), ``None`` (còn lại).
        """
        if ref.doc_kind == "external":
            self._ext_node(ref)
            return [(ref.doc, ref.ref_text, None)], []
        if ref.doc not in self.indexable:  # văn bản sửa đổi / VBHN: chỉ có nút VanBan
            return [(ref.doc, ref.ref_text, None)], []
        if not ref.unit_ids:
            return ([(ref.doc, None, None)] if ref.doc != src_unit.split("/")[0] else []), []
        found: list[tuple[str, str | None, str | None]] = []
        missing: list[str] = []
        anc = self._ancestors(src_unit)
        for t in ref.unit_ids:
            if t not in self.node_ids:
                missing.append(t)
            elif t == src_unit:
                found.append((t, None, "chinh_unit"))
            elif t in anc:
                found.append((t, None, "to_tien"))
            else:
                found.append((t, None, None))
        return found, missing

    def reference_edges(self) -> None:
        scopes = self._scopes()
        for uid in sorted(self.versions):
            src_doc = uid.split("/")[0]
            stats = self.ref_stats[src_doc]
            scope = scopes.get(uid)
            for v in self.versions[uid]:
                if v.status == "repealed" or not v.text:
                    continue
                vid = version_node_id(uid, v.version)
                for ref in extract_references(v.text, uid, self.names, scope):
                    is_span = ref.ref_text is not None
                    stats["spans" if is_span else "nhac_van_ban"] += 1
                    base = {"source_unit_id": uid, "version": v.version, "span": ref.text}
                    if ref.error is not None:
                        stats["loi_doc"] += 1
                        self.unresolved.append({**base, "reason": "loi_doc", "detail": ref.error})
                        continue
                    if ref.doc in self.names.excluded:
                        # Văn bản không dùng (CLAUDE.md mục 6): đọc được nhưng không để dấu vết.
                        stats["resolved"] += is_span
                        continue
                    found, missing = self._targets(ref, uid)
                    if missing:
                        # Phụ lục chưa có unit (M3 chỉ tách Phụ lục có dòng tiêu đề đúng mẫu):
                        # giới hạn dữ liệu, thống kê riêng.
                        reason = (
                            "phu_luc_khong_co_unit"
                            if all("/PL" in m for m in missing)
                            else "dich_khong_ton_tai"
                        )
                        stats[reason] += 1
                        self.unresolved.append(
                            {**base, "reason": reason, "detail": ", ".join(missing)}
                        )
                    elif is_span:
                        stats["resolved"] += 1
                    for dst, target_ref, quan_he in found:
                        dst_doc = dst.split("/")[0]
                        pham_vi = (
                            "noi_bo"
                            if dst_doc == src_doc
                            else "ngoai"
                            if dst.startswith(EXT_PREFIX)
                            else "van_ban_khac"
                        )
                        props = {
                            "effective_from": to_iso(v.effective_from),
                            "effective_to": to_iso(v.effective_to),
                            "pham_vi": pham_vi,
                            "can_cu": _is_can_cu(v.text, ref.start),
                            "span": ref.text,
                        }
                        if target_ref:
                            props["target_ref"] = target_ref
                        if quan_he is not None:
                            props["quan_he"] = quan_he
                            stats[quan_he] += 1
                        if scope is not None and ref.mention is None:
                            props["pham_vi_tu"] = scope.source_unit_id
                        self._add("DAN_CHIEU", vid, dst, props)

    def guidance_edges(self) -> None:
        scopes = self._scopes()
        for d in self.registry:
            if not d.indexable or d.loai == "luat":
                continue
            heads = [d.doc_id, f"{d.doc_id}/D1"]
            refs: list[tuple[str, Reference]] = []
            for h in heads:
                for v in self.versions.get(h, ()):
                    if v.text and v.status != "repealed":
                        refs.extend((h, r) for r in guidance_references(v.text, h, self.names))
            # Danh sách dưới Điều 1 "… quy định chi tiết … Luật X bao gồm: 1. Điều 6 …"
            for uid, scope in sorted(scopes.items(), key=lambda kv: kv[0]):
                if scope is None or scope.reason != "huong_dan":
                    continue
                if scope.source_unit_id not in heads:
                    continue
                for v in self.versions.get(uid, ()):
                    if v.text and v.status != "repealed":
                        refs.extend(
                            (uid, r)
                            for r in extract_references(v.text, uid, self.names, scope)
                            if r.doc == scope.doc
                        )
            for src_unit, ref in refs:
                if ref.doc in self.names.excluded:
                    continue
                if ref.error is not None:
                    self.unresolved.append(
                        {
                            "source_unit_id": src_unit,
                            "version": None,
                            "span": ref.text,
                            "reason": "huong_dan_loi_doc",
                            "detail": ref.error,
                        }
                    )
                    continue
                if ref.doc_kind == "external":
                    self._ext_node(ref)
                dsts = [ref.doc] + [u for u in ref.unit_ids if u in self.node_ids and u != ref.doc]
                for u in ref.unit_ids:
                    if u not in self.node_ids and ref.doc in self.indexable:
                        self.unresolved.append(
                            {
                                "source_unit_id": src_unit,
                                "version": None,
                                "span": ref.text,
                                "reason": "huong_dan_dich_khong_ton_tai",
                                "detail": u,
                            }
                        )
                for dst in dsts:
                    props = {
                        "effective_from": to_iso(d.hieu_luc_tu),
                        "effective_to": to_iso(d.hieu_luc_den),
                        "cap": "van_ban" if dst == ref.doc else "unit",
                        "source_unit_id": src_unit,
                        "span": ref.text,
                    }
                    self._add("HUONG_DAN", d.doc_id, dst, props)

    def delegation_props(self, nodes: list[Node]) -> int:
        uy: dict[str, list[dict[str, str]]] = defaultdict(list)
        for d in self.registry:
            if not d.indexable or d.loai != "luat":
                continue
            for uid, vs in self.versions.items():
                if not uid.startswith(d.doc_id + "/"):
                    continue
                v = vs[-1]
                if not v.text or v.status == "repealed":
                    continue
                for dl in delegations(v.text, uid, self.names):
                    for t in dl.ref.unit_ids:
                        item = {"co_quan": dl.co_quan, "source_unit_id": uid}
                        if t in self.node_ids and item not in uy[t]:
                            uy[t].append(item)
        for n in nodes:
            if n.id in uy:
                items = uy[n.id]
                n.props["uy_quyen"] = sorted(
                    items, key=lambda x: (x["source_unit_id"], x["co_quan"])
                )
        return sum(len(v) for v in uy.values())

    def ext_nodes(self) -> list[Node]:
        n_refs = Counter(e.dst for e in self.legal.values() if e.dst.startswith(EXT_PREFIX))
        return [
            Node(id=k, label="VanBanNgoai", props={**v, "n_refs": n_refs[k]})
            for k, v in self.ext.items()
        ]


def _sort_nodes(nodes: Iterable[Node]) -> list[Node]:
    order = {lab: i for i, lab in enumerate(NODE_LABEL_ORDER)}
    return sorted(nodes, key=lambda n: (order[n.label], n.id))


def _sort_edges(edges: Iterable[Edge], types: Sequence[str]) -> list[Edge]:
    order = {t: i for i, t in enumerate(types)}
    return sorted(
        edges, key=lambda e: (order[e.type], e.src, e.dst, str(e.props.get("version", "")))
    )


def build_graph(
    registry: Registry,
    units: Sequence[Unit],
    added: Sequence[AddedUnit],
    versions: Sequence[UnitVersion],
    names: DocNameTable,
) -> GraphData:
    """Dựng toàn bộ đồ thị; kết quả tất định (đã sắp xếp)."""
    b = _Builder(registry, units, added, versions, names)
    nodes, struct = b.nodes_and_struct()
    b.registry_relations()
    b.amendment_edges()
    b.reference_edges()
    b.guidance_edges()
    b.delegation_props(nodes)
    nodes.extend(b.ext_nodes())
    unresolved = sorted(
        b.unresolved, key=lambda r: (r["source_unit_id"], r["version"] or 0, r["span"])
    )
    return GraphData(
        nodes=_sort_nodes(nodes),
        edges_struct=_sort_edges(struct, STRUCT_EDGE_TYPES),
        edges_legal=_sort_edges(b.legal.values(), LEGAL_EDGE_TYPES),
        ref_stats=dict(b.ref_stats),
        unresolved=unresolved,
        errors=b.errors,
    )


def dangling_edges(nodes: Iterable[Node], edges: Iterable[Edge]) -> list[Edge]:
    """Cạnh có đầu mút không phải nút (đồ thị hợp lệ → rỗng)."""
    ids = {n.id for n in nodes}
    return [e for e in edges if e.src not in ids or e.dst not in ids]
