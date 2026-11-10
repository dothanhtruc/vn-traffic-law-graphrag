"""M9: kiểm tra bộ hỏi–đáp (``qa_tool validate``). Hàm thuần trên ``GraphStore`` đã nạp.

Lỗi (``error`` → mã thoát 1):

- ``sai_schema``: dòng không đúng ``QAItem``; ``qid_trung``.
- ``unit_khong_ton_tai``, ``unit_khong_chi_muc`` (văn bản không ``indexable``),
  ``het_hieu_luc`` (không có phiên bản hiệu lực tại ``as_of``), ``gold_versions_lech``.
- ``tier_lech``: ``tier`` không thuộc tier văn bản của ``gold_units``; ``thieu_tier``.
- ``so_khong_co_trong_van_ban``: ``required_numbers`` không có trong text phiên bản (unit, tổ
  tiên, cây con) cũng không là thuộc tính ``CheTai``/``DiemGPLX`` nối với các phiên bản đó.
- ``ngoai_pham_vi_co_gold``; ``thieu_gold`` (loại khác mà ``gold_units`` rỗng);
  ``da_buoc_it_unit`` (< 2 unit).
- Cặp ``theo_thoi_diem``: ``cap_thieu`` (≠ 2 câu), ``cap_cung_ngay``, ``cap_khong_doi_phien_ban``
  (không có ngày đổi phiên bản nào trong ``(ngày trước, ngày sau]``), ``dap_an_giong_nhau``.
- ``trung_lap``: câu hỏi trùng sau chuẩn hoá (trừ hai câu cùng ``pair_id``).
- test: ``thieu_dap_an``, ``nguon_khong_phai_nguoi`` (test phải viết tay).
- train/val: ``ro_ri_test`` (cosine TF-IDF > ngưỡng với một câu test), ``val_tron_dieu``.

Cảnh báo (chặn khi ``--strict``): ``gan_trung`` (cosine > ngưỡng trong cùng split),
``moc_khong_chuan`` (cặp đổi phiên bản ở ngày ngoài 4 mốc), ``da_buoc_khong_noi`` (các unit
không nối bằng DAN_CHIEU/BI_XU_PHAT/BI_TRU_DIEM/HUONG_DAN), ``so_khong_co_trong_dap_an``,
``vuot_han_muc``/``lech_phan_bo``, ``pair_id_sai_loai``, ``train_loi_thoi``.
"""

from __future__ import annotations

import re
import unicodedata
from collections import Counter, defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date, timedelta
from decimal import Decimal, InvalidOperation
from typing import Any, Literal

from pydantic import ValidationError

from trafficlaw.eval.qa_schema import QAItem, Split
from trafficlaw.eval.textsim import near_pairs, normalize
from trafficlaw.graph.store import BaseGraphStore, GraphNode, unit_of_version_id
from trafficlaw.utils.dates import parse_iso

Level = Literal["error", "warning", "info"]

UNIT_LABELS = ("Dieu", "Khoan", "Diem", "PhuLuc")
LINK_TYPES = ("DAN_CHIEU", "BI_XU_PHAT", "BI_TRU_DIEM", "HUONG_DAN")
NUMERIC_LABELS = ("CheTai", "DiemGPLX", "BienPhapBoSung")
NUMERIC_PROPS = ("min_vnd", "max_vnd", "min_thang", "max_thang", "so_diem")


@dataclass(frozen=True)
class Issue:
    level: Level
    code: str
    qid: str | None
    message: str

    def to_dict(self) -> dict[str, Any]:
        return {"level": self.level, "code": self.code, "qid": self.qid, "message": self.message}


@dataclass
class Targets:
    total: int = 500
    tier: dict[str, int] = field(default_factory=dict)
    question_type: dict[str, int] = field(default_factory=dict)
    tolerance: float = 0.1
    """Lệch tương đối cho phép khi đã đủ ``total`` câu (tối thiểu 2 câu)."""

    def tier_expected(self) -> dict[str, float]:
        """Hạn mức tier áp cho câu có tier (``ngoai_pham_vi`` không có tier) — chia theo tỷ lệ."""
        n_scope = self.total - self.question_type.get("ngoai_pham_vi", 0)
        tot = sum(self.tier.values()) or 1
        return {k: v / tot * n_scope for k, v in self.tier.items()}


@dataclass
class ValidateConfig:
    milestones: tuple[date, ...] = (
        date(2025, 1, 1),
        date(2026, 1, 1),
        date(2026, 7, 1),
        date(2026, 8, 15),
    )
    near_dup: float = 0.9
    near_dup_within_max: int = 3000
    """Split lớn hơn → bỏ dò gần trùng nội bộ (chỉ trùng tuyệt đối), báo ``info``."""
    targets: Targets | None = None


@dataclass
class ValidateResult:
    split: str
    n_lines: int
    items: list[QAItem]
    issues: list[Issue]
    resolved: list[dict[str, Any]]
    distribution: dict[str, Any]

    @property
    def n_errors(self) -> int:
        return sum(i.level == "error" for i in self.issues)

    @property
    def n_warnings(self) -> int:
        return sum(i.level == "warning" for i in self.issues)

    def bad_qids(self) -> set[str]:
        return {i.qid for i in self.issues if i.level == "error" and i.qid}


# --------------------------------------------------------------------------- con số

_NUM_RE = re.compile(r"\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+(?:,\d+)?")


def parse_numbers(text: str) -> set[Decimal]:
    """Số trong văn bản tiếng Việt: ``400.000`` = 400000, ``0,25`` = 0.25, ``02`` = 2."""
    out: set[Decimal] = set()
    for m in _NUM_RE.finditer(unicodedata.normalize("NFC", text)):
        tok = m.group(0).replace(".", "").replace(",", ".")
        try:
            out.add(Decimal(tok).normalize())
        except InvalidOperation:  # pragma: no cover - regex chỉ khớp chữ số
            continue
    return out


def as_decimal(v: int | float) -> Decimal:
    return Decimal(str(v)).normalize()


# --------------------------------------------------------------------------- đồ thị


@dataclass
class GraphView:
    """Truy vấn phụ trên ``GraphStore`` cho validator/phiếu viết (cache theo unit)."""

    store: BaseGraphStore
    _docs: dict[str, dict[str, Any]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self._docs = {n.id: dict(n.props) for n in self.store.nodes_by_label("VanBan")}

    def doc(self, doc_id: str) -> dict[str, Any]:
        return self._docs.get(doc_id, {})

    def unit(self, unit_id: str) -> GraphNode | None:
        n = self.store.get_node(unit_id)
        return n if n is not None and n.label in UNIT_LABELS else None

    def tier_of(self, unit_id: str) -> str | None:
        n = self.unit(unit_id)
        return str(self.doc(str(n.props.get("doc_id"))).get("tier")) if n else None

    def text_at(self, unit_id: str, d: date) -> str:
        v = self.store.version_at(unit_id, d)
        return str(v.props.get("text") or "") if v is not None else ""

    def context_units(self, unit_id: str, d: date) -> list[str]:
        """Unit + tổ tiên (unit) + cây con hiệu lực tại ``d``."""
        anc = [a for a in self.store.ancestors(unit_id) if self.unit(a) is not None]
        return [*anc, *self.store.subtree(unit_id, as_of=d)]

    def numbers_for(self, unit_ids: Sequence[str], d: date) -> set[Decimal]:
        """Số kiểm được: text phiên bản (unit, tổ tiên, cây con) + thuộc tính chế tài M8 nối với
        các phiên bản đó (``BI_XU_PHAT``/``BI_TRU_DIEM`` đi ra, hoặc nút có ``unit_id`` trùng)."""
        nums: set[Decimal] = set()
        units = {c for u in unit_ids for c in self.context_units(u, d)}
        for u in sorted(units):
            v = self.store.version_at(u, d)
            if v is None:
                continue
            nums |= parse_numbers(str(v.props.get("text") or ""))
            for e in self.store.out_edges(v.id, types=["BI_XU_PHAT", "BI_TRU_DIEM"], as_of=d):
                n = self.store.get_node(e.dst)
                if n is not None:
                    nums |= _numeric_props(n)
            for lab in NUMERIC_LABELS:
                for n in self.semantic_by_unit(lab).get_many([u]):
                    if n.props.get("version_id") == v.id:
                        nums |= _numeric_props(n)
        return nums

    _sem: dict[str, _ByUnit] = field(default_factory=dict)

    def semantic_by_unit(self, label: str) -> _ByUnit:
        if label not in self._sem:
            idx: dict[str, list[GraphNode]] = defaultdict(list)
            for n in self.store.nodes_by_label(label):
                idx[str(n.props.get("unit_id"))].append(n)
            self._sem[label] = _ByUnit(dict(idx))
        return self._sem[label]

    def linked_units(self, unit_id: str, d: date) -> set[str]:
        """Unit nối 1 bước (hai chiều) qua ``LINK_TYPES`` tại ``d`` từ unit **hoặc cây con** của
        nó (cạnh chế tài đi ra từ phiên bản Điểm); nút chế tài → unit nêu nó."""
        own = set(self.store.subtree(unit_id, as_of=d))
        sub = self.store.expand(sorted(own), edge_types=LINK_TYPES, as_of=d, hops=1)
        out: set[str] = set()
        nodes = self.store.get_nodes(list(sub.nodes))
        for nid in sub.nodes:
            n = nodes.get(nid)
            if n is None:
                continue
            if n.label in NUMERIC_LABELS:
                out.add(str(n.props.get("unit_id")))
            elif n.label in UNIT_LABELS:
                out.add(nid)
        # Cạnh BI_XU_PHAT/BI_TRU_DIEM đi vào nút chế tài nêu ở cây con (hành vi ở unit khác).
        for lab in NUMERIC_LABELS:
            for n in self.semantic_by_unit(lab).get_many(own):
                for e in self.store.in_edges(n.id, as_of=d):
                    out.add(unit_of_version_id(e.src))
        return out - own

    def change_dates(self, unit_ids: Sequence[str]) -> list[date]:
        """Mọi ngày bắt đầu/kết thúc+1 phiên bản của unit và cây con (không lọc ngày)."""
        out: set[date] = set()
        for u in unit_ids:
            for s in self.store.subtree(u):
                for v in self.store.versions(s):
                    f = _d(v.props.get("effective_from"))
                    t = _d(v.props.get("effective_to"))
                    if f:
                        out.add(f)
                    if t:
                        out.add(t + timedelta(days=1))
        return sorted(out)

    def signature(self, unit_ids: Sequence[str], d: date) -> tuple[str | None, ...]:
        out: list[str | None] = []
        for u in sorted(set(unit_ids)):
            for s in self.store.subtree(u):
                v = self.store.version_at(s, d)
                out.append(v.id if v is not None else None)
        return tuple(out)


@dataclass
class _ByUnit:
    idx: dict[str, list[GraphNode]]

    def get_many(self, units: Sequence[str] | set[str]) -> list[GraphNode]:
        return [n for u in units for n in self.idx.get(u, ())]


def _d(v: Any) -> date | None:
    return v if isinstance(v, date) or v is None else parse_iso(str(v))


def _numeric_props(n: GraphNode) -> set[Decimal]:
    out: set[Decimal] = set()
    for k in NUMERIC_PROPS:
        v = n.props.get(k)
        if isinstance(v, int | float) and not isinstance(v, bool):
            out.add(as_decimal(v))
    return out


def _related(a: str, b: str) -> bool:
    """Cùng unit hoặc quan hệ tổ tiên/con cháu theo mã."""
    return a == b or a.startswith(b + "/") or b.startswith(a + "/")


# --------------------------------------------------------------------------- validator


def parse_items(rows: Sequence[Mapping[str, Any]]) -> tuple[list[QAItem], list[Issue]]:
    items: list[QAItem] = []
    issues: list[Issue] = []
    for i, r in enumerate(rows, 1):
        try:
            items.append(QAItem.model_validate(r))
        except ValidationError as e:
            qid = r.get("qid") if isinstance(r, Mapping) else None
            msg = "; ".join(f"{'.'.join(map(str, x['loc']))}: {x['msg']}" for x in e.errors()[:5])
            issues.append(Issue("error", "sai_schema", qid, f"dòng {i}: {msg}"))
    return items, issues


def _check_item(it: QAItem, split: Split, gv: GraphView) -> tuple[list[Issue], list[str]]:
    iss: list[Issue] = []
    q = it.qid

    def add(level: Level, code: str, msg: str) -> None:
        iss.append(Issue(level, code, q, msg))

    if split == "test":
        if not it.answer:
            add("error", "thieu_dap_an", "test phải có đáp án")
        if it.source != "human":
            add("error", "nguon_khong_phai_nguoi", f"test phải viết tay (source = {it.source!r})")
    if it.question_type == "ngoai_pham_vi":
        if it.gold_units:
            add("error", "ngoai_pham_vi_co_gold", "câu ngoài phạm vi không có gold_units")
        if it.required_numbers:
            add("error", "ngoai_pham_vi_co_gold", "câu ngoài phạm vi không có required_numbers")
        return iss, []
    if not it.gold_units and it.question_type != "theo_thoi_diem":
        add("error", "thieu_gold", "cần ít nhất một gold_unit")
    if it.tier is None:
        add("error", "thieu_tier", "chỉ câu ngoai_pham_vi được để tier null")
    if it.pair_id and it.question_type != "theo_thoi_diem":
        add("warning", "pair_id_sai_loai", "pair_id chỉ dùng cho theo_thoi_diem")

    versions: list[str] = []
    tiers: set[str] = set()
    ok_units: list[str] = []
    for u in it.gold_units:
        n = gv.unit(u)
        if n is None:
            add("error", "unit_khong_ton_tai", f"{u} không có trong đồ thị")
            continue
        doc = gv.doc(str(n.props.get("doc_id")))
        if not doc.get("indexable"):
            add("error", "unit_khong_chi_muc", f"{u}: văn bản không thuộc chỉ mục")
            continue
        tiers.add(str(doc.get("tier")))
        v = gv.store.version_at(u, it.as_of)
        if v is None:
            add("error", "het_hieu_luc", f"{u} không có phiên bản hiệu lực tại {it.as_of}")
            continue
        versions.append(v.id)
        ok_units.append(u)
    if it.gold_versions and it.gold_versions != versions and len(versions) == len(it.gold_units):
        add("error", "gold_versions_lech", f"ghi {it.gold_versions}, đúng là {versions}")
    if it.tier is not None and tiers and it.tier not in tiers:
        add("error", "tier_lech", f"tier {it.tier} nhưng gold_units thuộc tier {sorted(tiers)}")

    if it.question_type == "da_buoc":
        if len(set(it.gold_units)) < 2:
            add("error", "da_buoc_it_unit", "câu đa bước cần ≥ 2 gold_units")
        elif len(ok_units) >= 2 and not _connected(ok_units, it.as_of, gv):
            add(
                "warning",
                "da_buoc_khong_noi",
                "các gold_units không nối nhau bằng DAN_CHIEU/BI_XU_PHAT/BI_TRU_DIEM/HUONG_DAN",
            )

    if it.required_numbers and ok_units:
        ans_nums = parse_numbers(it.answer or "")
        for rn in it.required_numbers:
            scope = [rn.unit_id] if rn.unit_id else ok_units
            if rn.unit_id and gv.unit(rn.unit_id) is None:
                add("error", "unit_khong_ton_tai", f"required_numbers.unit_id {rn.unit_id}")
                continue
            val = as_decimal(rn.value)
            if val not in gv.numbers_for(scope, it.as_of):
                add(
                    "error",
                    "so_khong_co_trong_van_ban",
                    f"{rn.value} {rn.unit} không có trong text/chế tài của {scope} tại {it.as_of}",
                )
            elif it.answer is not None and val not in ans_nums:
                add("warning", "so_khong_co_trong_dap_an", f"đáp án không nêu {rn.value}")
    return iss, versions


def _connected(units: Sequence[str], d: date, gv: GraphView) -> bool:
    """Đồ thị vô hướng trên ``units`` (cạnh = nối 1 bước, khớp cả tổ tiên/con cháu) liên thông."""
    us = sorted(set(units))
    nb = {u: gv.linked_units(u, d) for u in us}
    adj: dict[str, set[str]] = {u: set() for u in us}
    for a in us:
        for b in us:
            if a != b and any(_related(x, b) for x in nb[a]):
                adj[a].add(b)
                adj[b].add(a)
    seen = {us[0]}
    stack = [us[0]]
    while stack:
        for y in adj[stack.pop()]:
            if y not in seen:
                seen.add(y)
                stack.append(y)
    return len(seen) == len(us)


def _check_pairs(items: Sequence[QAItem], gv: GraphView, cfg: ValidateConfig) -> list[Issue]:
    iss: list[Issue] = []
    groups: dict[str, list[QAItem]] = defaultdict(list)
    for it in items:
        if it.question_type == "theo_thoi_diem":
            if not it.pair_id:
                iss.append(Issue("error", "cap_thieu", it.qid, "theo_thoi_diem cần pair_id"))
                continue
            groups[it.pair_id].append(it)
    for pid, g in sorted(groups.items()):
        qids = ",".join(x.qid for x in g)
        if len(g) != 2:
            iss.append(Issue("error", "cap_thieu", qids, f"pair {pid} có {len(g)} câu (cần 2)"))
            continue
        a, b = sorted(g, key=lambda x: x.as_of)
        if a.as_of == b.as_of:
            iss.append(Issue("error", "cap_cung_ngay", qids, f"pair {pid}: hai câu cùng as_of"))
            continue
        units = [u for u in sorted({*a.gold_units, *b.gold_units}) if gv.unit(u) is not None]
        if not units:
            iss.append(Issue("error", "thieu_gold", qids, f"pair {pid}: không có gold_unit hợp lệ"))
            continue
        changes = [d for d in gv.change_dates(units) if a.as_of < d <= b.as_of]
        if gv.signature(units, a.as_of) == gv.signature(units, b.as_of) or not changes:
            iss.append(
                Issue(
                    "error",
                    "cap_khong_doi_phien_ban",
                    qids,
                    f"pair {pid}: phiên bản của {units} không đổi giữa {a.as_of} và {b.as_of}",
                )
            )
        elif not set(changes) & set(cfg.milestones):
            iss.append(
                Issue(
                    "warning",
                    "moc_khong_chuan",
                    qids,
                    f"pair {pid}: đổi phiên bản ngày {[d.isoformat() for d in changes]}, không "
                    f"thuộc 4 mốc {[m.isoformat() for m in cfg.milestones]}",
                )
            )
        if a.answer and b.answer and normalize(a.answer) == normalize(b.answer):
            iss.append(Issue("error", "dap_an_giong_nhau", qids, f"pair {pid}: đáp án giống nhau"))
    return iss


def _check_dups(items: Sequence[QAItem], cfg: ValidateConfig) -> list[Issue]:
    iss: list[Issue] = []
    by_norm: dict[str, list[QAItem]] = defaultdict(list)
    for it in items:
        by_norm[normalize(it.question)].append(it)

    def same_pair(x: QAItem, y: QAItem) -> bool:
        return bool(x.pair_id) and x.pair_id == y.pair_id

    for g in by_norm.values():
        for x in g[1:]:
            if not same_pair(g[0], x):
                iss.append(Issue("error", "trung_lap", x.qid, f"trùng câu hỏi với {g[0].qid}"))
    if len(items) > cfg.near_dup_within_max:
        iss.append(
            Issue("info", "bo_qua_gan_trung", None, f"{len(items)} câu > ngưỡng dò gần trùng")
        )
        return iss
    qs = [it.question for it in items]
    for i, j, s in near_pairs(qs, qs, threshold=cfg.near_dup, same=True):
        x, y = items[i], items[j]
        if same_pair(x, y) or normalize(x.question) == normalize(y.question):
            continue
        iss.append(Issue("warning", "gan_trung", y.qid, f"gần trùng {x.qid} (cosine {s:.3f})"))
    return iss


def distribution(items: Sequence[QAItem], targets: Targets | None) -> dict[str, Any]:
    tier = Counter(str(it.tier) for it in items if it.tier)
    qt = Counter(it.question_type for it in items)
    cross = Counter(f"{it.tier or '-'}|{it.question_type}" for it in items)
    out: dict[str, Any] = {
        "n": len(items),
        "tier": dict(sorted(tier.items())),
        "question_type": dict(sorted(qt.items())),
        "tier_x_type": dict(sorted(cross.items())),
    }
    if targets:
        out["targets"] = {
            "total": targets.total,
            "tier": {k: round(v, 1) for k, v in targets.tier_expected().items()},
            "question_type": dict(targets.question_type),
        }
    return out


def _check_distribution(items: Sequence[QAItem], targets: Targets) -> list[Issue]:
    iss: list[Issue] = []
    tier = Counter(str(it.tier) for it in items if it.tier)
    qt = Counter(it.question_type for it in items)
    complete = len(items) >= targets.total
    groups = [
        ("tier", tier, targets.tier_expected()),
        ("question_type", qt, {k: float(v) for k, v in targets.question_type.items()}),
    ]
    for name, have, want in groups:
        for k in sorted(set(have) | set(want)):
            h, w = have.get(k, 0), want.get(k, 0.0)
            tol = max(2.0, targets.tolerance * w)
            if h > w + tol:
                iss.append(
                    Issue("warning", "vuot_han_muc", None, f"{name} {k}: {h} câu > hạn mức {w:.0f}")
                )
            elif complete and h < w - tol:
                iss.append(
                    Issue("warning", "lech_phan_bo", None, f"{name} {k}: {h} câu < hạn mức {w:.0f}")
                )
    return iss


def check_leakage(
    items: Sequence[QAItem], test_questions: Sequence[str], threshold: float
) -> list[Issue]:
    iss = []
    hits: dict[int, float] = {}
    for i, _j, s in near_pairs([it.question for it in items], test_questions, threshold=threshold):
        hits[i] = max(s, hits.get(i, 0.0))
    for i, s in sorted(hits.items()):
        iss.append(
            Issue("error", "ro_ri_test", items[i].qid, f"gần trùng một câu test (cosine {s:.3f})")
        )
    return iss


def validate_items(
    rows: Sequence[Mapping[str, Any]],
    split: Split,
    store: BaseGraphStore,
    cfg: ValidateConfig | None = None,
    *,
    test_questions: Sequence[str] | None = None,
    other_split_dieus: set[str] | None = None,
) -> ValidateResult:
    """Kiểm tra mọi bản ghi của một split. ``test_questions`` (train/val): dò rò rỉ;
    ``other_split_dieus``: Điều của split còn lại (train ↔ val) để kiểm tra chia theo Điều."""
    cfg = cfg or ValidateConfig()
    gv = GraphView(store)
    items, issues = parse_items(rows)
    seen: Counter[str] = Counter(it.qid for it in items)
    for q, c in sorted(seen.items()):
        if c > 1:
            issues.append(Issue("error", "qid_trung", q, f"qid xuất hiện {c} lần"))
    resolved: list[dict[str, Any]] = []
    for it in items:
        iss, versions = _check_item(it, split, gv)
        issues += iss
        d = it.model_dump(mode="json")
        d["gold_versions"] = versions if len(versions) == len(it.gold_units) else it.gold_versions
        resolved.append(d)
    issues += _check_pairs(items, gv, cfg)
    issues += _check_dups(items, cfg)
    if test_questions is not None and split != "test":
        issues += check_leakage(items, test_questions, cfg.near_dup)
    if other_split_dieus is not None and split != "test":
        mine = {_dieu(u) for it in items for u in it.gold_units}
        both = sorted(mine & other_split_dieus)
        if both:
            issues.append(
                Issue(
                    "error",
                    "val_tron_dieu",
                    None,
                    f"{len(both)} Điều có ở cả train và val (vd {both[:3]})",
                )
            )
    if split == "test" and cfg.targets is not None:
        issues += _check_distribution(items, cfg.targets)
    return ValidateResult(
        split=split,
        n_lines=len(rows),
        items=items,
        issues=issues,
        resolved=resolved,
        distribution=distribution(items, cfg.targets if split == "test" else None),
    )


def _dieu(unit_id: str) -> str:
    parts = unit_id.split("/")
    return "/".join(parts[:2]) if len(parts) >= 2 else unit_id


__all__ = [
    "GraphView",
    "Issue",
    "Targets",
    "ValidateConfig",
    "ValidateResult",
    "as_decimal",
    "check_leakage",
    "distribution",
    "parse_items",
    "parse_numbers",
    "validate_items",
]
