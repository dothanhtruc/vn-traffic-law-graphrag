"""M9: hỗ trợ người dùng VIẾT TAY tập test — phiếu viết (``qa_tool plan-test``) và tra cứu một
unit (``qa_tool show``). Công cụ chỉ gợi ý **điều khoản** (lấy mẫu phân tầng, seed cố định) kèm
nguyên văn phiên bản và con số lấy bằng rule; không sinh câu hỏi hay đáp án.

Nguồn gợi ý theo loại câu (chunk hiệu lực tại ``as_of``, mặc định mốc chốt 03/11/2026):

- ``muc_phat`` / ``tru_diem`` / ``bien_phap``: chunk nêu hoặc bị áp ``CheTai`` (phạt tiền/cảnh
  cáo), ``DiemGPLX``, ``CheTai`` tước/tịch thu/đình chỉ hoặc ``BienPhapBoSung`` (đồ thị M8).
- ``dinh_nghia``: chunk có ``DINH_NGHIA``.
- ``hanh_vi_cam_nghia_vu``: chunk ngoài Điều xử phạt, có ``QUY_DINH_HANH_VI`` hoặc chữ "nghiêm
  cấm|cấm|phải|không được".
- ``thu_tuc_tham_quyen``: tiêu đề Điều/text về thủ tục, hồ sơ, thẩm quyền, trách nhiệm, cấp,
  đăng ký, sát hạch, kiểm định…
- ``theo_thoi_diem``: Khoản đổi nội dung ở một ngày (ưu tiên 4 mốc), in nguyên văn hai phía.
- ``da_buoc``: DAN_CHIEU (khác Điều, không phải "Căn cứ") hoặc ``BI_XU_PHAT`` qua dẫn chiếu.
- ``so_sanh``: hai chunk ở hai Điều xử phạt khác nhau của cùng văn bản, text giống nhau vừa phải
  (cùng hành vi, khác loại xe/chủ thể).
- ``ngoai_pham_vi``: không có gợi ý unit.
"""

from __future__ import annotations

import json
import math
import random
import re
from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Any

from trafficlaw.eval.qa_generate import doc_label
from trafficlaw.eval.qa_schema import QUESTION_TYPE_DOC
from trafficlaw.eval.qa_validate import UNIT_LABELS, GraphView, Targets
from trafficlaw.eval.textsim import near_pairs
from trafficlaw.graph.store import BaseGraphStore, GraphNode, unit_of_version_id
from trafficlaw.retrieval.chunking import Chunk, iter_chunks

SANCTION_TITLE = re.compile(r"^Xử phạt")
OBLIGATION_RE = re.compile(r"[Nn]ghiêm cấm|\b[Cc]ấm\b|\bphải\b|không được")
PROCEDURE_RE = re.compile(
    r"thủ tục|hồ sơ|trình tự|thẩm quyền|trách nhiệm|nhiệm vụ|quyền hạn|\bcấp\b|đăng ký|sát hạch|"
    r"kiểm định|đăng kiểm|điều kiện|cơ quan",
    re.IGNORECASE,
)
PLAN_TYPES = (
    "muc_phat",
    "tru_diem",
    "bien_phap",
    "hanh_vi_cam_nghia_vu",
    "dinh_nghia",
    "thu_tuc_tham_quyen",
    "theo_thoi_diem",
    "da_buoc",
    "so_sanh",
)


@dataclass
class PlanConfig:
    as_of: date = date(2026, 11, 3)
    seed: int = 42
    factor: float = 1.0
    """Số gợi ý = ``ceil(hạn mức × factor)`` mỗi loại."""
    max_text_chars: int = 1200
    milestones: tuple[date, ...] = (
        date(2025, 1, 1),
        date(2026, 1, 1),
        date(2026, 7, 1),
        date(2026, 8, 15),
    )
    so_sanh_min: float = 0.5
    so_sanh_max: float = 0.95


@dataclass
class Suggestion:
    sid: str
    qtype: str
    tier: str
    chunks: list[Chunk]
    """Một chunk; hai chunk cho ``da_buoc``/``so_sanh``."""
    dates: list[date]
    """Một ngày; hai ngày (trước, sau mốc) cho ``theo_thoi_diem``."""
    change_date: date | None = None
    note: str = ""
    gold_units: list[str] | None = None
    """Ghi đè ``gold_units`` của mẫu dòng (mặc định = unit của các chunk)."""


@dataclass
class ChunkFacts:
    chunk: Chunk
    sem: list[GraphNode] = field(default_factory=list)
    """CheTai/DiemGPLX/BienPhapBoSung nêu ở hoặc áp cho chunk (tại ``as_of``)."""
    has_def: bool = False
    has_hv: bool = False
    sanction_dieu: bool = False
    links: list[tuple[str, str]] = field(default_factory=list)
    """(unit đích, loại liên kết) sang Điều khác."""


# --------------------------------------------------------------------------- dữ kiện


def chunk_facts(gv: GraphView, chunks: Sequence[Chunk], d: date) -> list[ChunkFacts]:
    st = gv.store
    out = []
    by_vid: dict[str, list[GraphNode]] = defaultdict(list)
    for lab in ("CheTai", "DiemGPLX", "BienPhapBoSung"):
        for n in st.nodes_by_label(lab):
            by_vid[str(n.props.get("version_id"))].append(n)
    for c in chunks:
        f = ChunkFacts(c, sanction_dieu=bool(SANCTION_TITLE.search(c.dieu_title)))
        sem: dict[str, GraphNode] = {}
        for vid in c.version_ids:
            for n in by_vid.get(vid, ()):
                sem[n.id] = n
            for e in st.out_edges(vid, as_of=d):
                if e.type in ("BI_XU_PHAT", "BI_TRU_DIEM"):
                    n = st.get_node(e.dst)
                    if n is not None:
                        sem[n.id] = n
                elif e.type == "DINH_NGHIA":
                    f.has_def = True
                elif e.type == "QUY_DINH_HANH_VI":
                    f.has_hv = True
                elif (
                    e.type == "DAN_CHIEU"
                    and not e.props.get("can_cu")
                    and "quan_he" not in e.props
                    and _dieu(e.dst) != c.dieu_id
                    and gv.unit(e.dst) is not None
                    and st.version_at(e.dst, d) is not None
                ):
                    f.links.append((e.dst, "DAN_CHIEU"))
                if e.type == "BI_XU_PHAT" and e.props.get("nguon") == "dan_chieu":
                    n = st.get_node(e.dst)
                    stated = str(n.props.get("unit_id")) if n else ""
                    if (
                        stated
                        and not stated.startswith(c.unit_id)
                        and st.version_at(stated, d) is not None
                    ):
                        f.links.append((stated, "BI_XU_PHAT"))
        f.sem = [sem[k] for k in sorted(sem)]
        f.links = sorted(set(f.links))
        out.append(f)
    return out


def representative_chunks(chunks: Sequence[Chunk], as_of: date) -> list[tuple[Chunk, date]]:
    """Mỗi unit một trạng thái để gợi ý: trạng thái hiệu lực tại ``as_of``; unit đã hết hiệu
    lực (vd TT35, tier historical) → trạng thái cuối cùng, hỏi tại ngày cuối còn hiệu lực. Unit
    chỉ có hiệu lực sau ``as_of`` bị bỏ."""
    by_unit: dict[str, list[Chunk]] = defaultdict(list)
    for c in chunks:
        by_unit[c.unit_id].append(c)
    out: list[tuple[Chunk, date]] = []
    for u in sorted(by_unit):
        cs = sorted(by_unit[u], key=lambda c: c.effective_from)
        cur = [c for c in cs if c.covers(as_of)]
        if cur:
            out.append((cur[0], as_of))
            continue
        past = [c for c in cs if c.effective_to is not None and c.effective_to < as_of]
        if past and not any(c.effective_from > as_of for c in cs):
            out.append((past[-1], past[-1].effective_to))  # type: ignore[arg-type]
    return out


def _dieu(unit_id: str) -> str:
    return "/".join(unit_id.split("/")[:2])


def _loai(n: GraphNode) -> str:
    return str(n.props.get("loai") or n.label)


def eligible(f: ChunkFacts, qtype: str) -> bool:
    c = f.chunk
    if qtype == "muc_phat":
        return any(n.label == "CheTai" and _loai(n) in ("phat_tien", "canh_cao") for n in f.sem)
    if qtype == "tru_diem":
        return any(n.label == "DiemGPLX" for n in f.sem)
    if qtype == "bien_phap":
        return any(
            n.label == "BienPhapBoSung"
            or (n.label == "CheTai" and _loai(n) in ("tuoc_quyen", "tich_thu", "dinh_chi"))
            for n in f.sem
        )
    if qtype == "dinh_nghia":
        return f.has_def
    if qtype == "hanh_vi_cam_nghia_vu":
        return not f.sanction_dieu and (f.has_hv or bool(OBLIGATION_RE.search(c.text)))
    if qtype == "thu_tuc_tham_quyen":
        return not f.sanction_dieu and bool(
            PROCEDURE_RE.search(c.dieu_title) or PROCEDURE_RE.search(c.text[:400])
        )
    if qtype == "da_buoc":
        return bool(f.links)
    return False


# --------------------------------------------------------------------------- phân bổ


def allocate(n: int, weights: Mapping[str, float], caps: Mapping[str, int]) -> dict[str, int]:
    """Chia ``n`` theo ``weights`` (phần dư lớn nhất), không vượt ``caps``; phần thiếu chia lại
    cho nhóm còn chỗ."""
    keys = sorted(k for k in weights if caps.get(k, 0) > 0 and weights[k] > 0)
    out = dict.fromkeys(keys, 0)
    remaining = min(n, sum(caps[k] for k in keys))
    while remaining > 0:
        open_ = [k for k in keys if out[k] < caps[k]]
        tot = sum(weights[k] for k in open_)
        share = {k: remaining * weights[k] / tot for k in open_}
        add = {k: min(caps[k] - out[k], math.floor(share[k])) for k in open_}
        if sum(add.values()) == 0:
            for k in sorted(open_, key=lambda k: (-(share[k] - math.floor(share[k])), k)):
                if remaining == 0:
                    break
                out[k] += 1
                remaining -= 1
            continue
        for k, v in add.items():
            out[k] += v
            remaining -= v
    return out


def _sample(items: Sequence[Any], k: int, salt: str) -> list[Any]:
    if k >= len(items):
        return list(items)
    return random.Random(salt).sample(list(items), k)


def theo_thoi_diem_candidates(all_chunks: Sequence[Chunk]) -> list[tuple[Chunk | None, Chunk]]:
    """(trạng thái trước, trạng thái sau) của cùng unit, theo ngày đổi; trước ``None`` = unit
    mới có hiệu lực từ ngày đó (bổ sung / luật mới)."""
    by_unit: dict[str, list[Chunk]] = defaultdict(list)
    for c in all_chunks:
        by_unit[c.unit_id].append(c)
    out: list[tuple[Chunk | None, Chunk]] = []
    for u in sorted(by_unit):
        cs = sorted(by_unit[u], key=lambda c: c.effective_from)
        for i, c in enumerate(cs):
            prev = cs[i - 1] if i else None
            if prev is not None and prev.effective_to == c.effective_from - timedelta(days=1):
                out.append((prev, c))
            elif prev is None:
                out.append((None, c))
    return out


def plan_suggestions(
    store: BaseGraphStore, targets: Targets, cfg: PlanConfig
) -> tuple[list[Suggestion], dict[str, Any]]:
    gv = GraphView(store)
    all_chunks = list(iter_chunks(store))
    rep = representative_chunks(all_chunks, cfg.as_of)
    active = [c for c, _ in rep]
    date_of = {c.chunk_id: d for c, d in rep}
    facts: list[ChunkFacts] = []
    for d in sorted(set(date_of.values())):
        facts += chunk_facts(gv, [c for c, dd in rep if dd == d], d)
    by_unit = {f.chunk.unit_id: f for f in facts}
    tier_w = {k: float(v) for k, v in targets.tier.items()}
    used: set[str] = set()
    out: list[Suggestion] = []
    stats: dict[str, Any] = {"n_chunks_active": len(active), "pool": {}}

    def take(qtype: str, n: int, pool: dict[str, list[Any]]) -> list[Any]:
        stats["pool"][qtype] = {t: len(v) for t, v in sorted(pool.items())}
        alloc = allocate(n, tier_w, {t: len(v) for t, v in pool.items()})
        picked = []
        for t in sorted(alloc):
            picked += _sample(pool[t], alloc[t], f"{cfg.seed}:{qtype}:{t}")
        return picked

    for qtype in PLAN_TYPES:
        quota = targets.question_type.get(qtype, 0)
        if quota <= 0:
            continue
        n = math.ceil(quota * cfg.factor)
        if qtype == "theo_thoi_diem":
            out += _plan_time(all_chunks, math.ceil(n / 2), cfg, used, stats)
            continue
        if qtype == "so_sanh":
            out += _plan_compare(facts, n, cfg, used, stats, date_of)
            continue
        pool: dict[str, list[ChunkFacts]] = defaultdict(list)
        for f in facts:
            if f.chunk.unit_id not in used and eligible(f, qtype):
                pool[f.chunk.tier].append(f)
        for i, f in enumerate(take(qtype, n, pool), 1):
            used.add(f.chunk.unit_id)
            chunks = [f.chunk]
            note = ""
            gold: list[str] | None = None
            if qtype == "da_buoc":
                dst, kind = _sample(f.links, 1, f"{cfg.seed}:link:{f.chunk.chunk_id}")[0]
                other = by_unit.get(dst) or by_unit.get(_khoan_of(dst))
                if other is not None and other.chunk.unit_id != f.chunk.unit_id:
                    chunks.append(other.chunk)
                    gold = [f.chunk.unit_id, other.chunk.unit_id]
                else:  # đích là Điều có Khoản → in tối đa 3 Khoản đầu
                    kids = [x for x in facts if x.chunk.unit_id.startswith(dst + "/")]
                    chunks += [x.chunk for x in kids[:3]]
                    gold = [f.chunk.unit_id, dst]
                note = f"{kind} → {dst}"
            out.append(
                Suggestion(
                    f"W-{qtype}-{i:03d}",
                    qtype,
                    f.chunk.tier,
                    chunks,
                    [date_of[f.chunk.chunk_id]],
                    None,
                    note,
                    gold,
                )
            )
    return out, stats


def _khoan_of(unit_id: str) -> str:
    return "/".join(unit_id.split("/")[:3])


def _plan_time(
    all_chunks: Sequence[Chunk],
    n_pairs: int,
    cfg: PlanConfig,
    used: set[str],
    stats: dict[str, Any],
) -> list[Suggestion]:
    cands = [p for p in theo_thoi_diem_candidates(all_chunks) if p[1].unit_id not in used]
    groups: dict[str, list[tuple[Chunk | None, Chunk]]] = defaultdict(list)
    for p in cands:
        d = p[1].effective_from
        groups[d.isoformat() if d in cfg.milestones else "khac"].append(p)
    stats["pool"]["theo_thoi_diem"] = {k: len(v) for k, v in sorted(groups.items())}
    weights = {k: (1.0 if k != "khac" else 0.25) for k in groups}
    alloc = allocate(n_pairs, weights, {k: len(v) for k, v in groups.items()})
    out = []
    i = 0
    for k in sorted(alloc):
        for before, after in _sample(groups[k], alloc[k], f"{cfg.seed}:theo_thoi_diem:{k}"):
            i += 1
            used.add(after.unit_id)
            d = after.effective_from
            out.append(
                Suggestion(
                    f"W-theo_thoi_diem-{i:03d}",
                    "theo_thoi_diem",
                    after.tier,
                    [c for c in (before, after) if c is not None],
                    [d - timedelta(days=1), d],
                    d,
                    "trước mốc: chưa có hiệu lực" if before is None else "",
                )
            )
    return out


def _plan_compare(
    facts: Sequence[ChunkFacts],
    n: int,
    cfg: PlanConfig,
    used: set[str],
    stats: dict[str, Any],
    date_of: Mapping[str, date],
) -> list[Suggestion]:
    fs = [
        f
        for f in facts
        if f.sanction_dieu and f.chunk.unit_id not in used and eligible(f, "muc_phat")
    ]
    by_doc: dict[str, list[ChunkFacts]] = defaultdict(list)
    for f in fs:
        by_doc[f.chunk.doc_id].append(f)
    pairs: list[tuple[ChunkFacts, ChunkFacts, float]] = []
    for doc in sorted(by_doc):
        g = by_doc[doc]
        texts = [_body(f.chunk.text) for f in g]
        for i, j, s in near_pairs(texts, texts, threshold=cfg.so_sanh_min, same=True):
            if s <= cfg.so_sanh_max and g[i].chunk.dieu_id != g[j].chunk.dieu_id:
                pairs.append((g[i], g[j], s))
    stats["pool"]["so_sanh"] = {"pairs": len(pairs)}
    rng = random.Random(f"{cfg.seed}:so_sanh")
    rng.shuffle(pairs)
    out = []
    for a, b, s in pairs:
        if len(out) >= n:
            break
        if a.chunk.unit_id in used or b.chunk.unit_id in used:
            continue
        used |= {a.chunk.unit_id, b.chunk.unit_id}
        out.append(
            Suggestion(
                f"W-so_sanh-{len(out) + 1:03d}",
                "so_sanh",
                a.chunk.tier,
                [a.chunk, b.chunk],
                [date_of[a.chunk.chunk_id]],
                None,
                f"cosine TF-IDF {s:.2f}",
            )
        )
    return out


def _body(text: str) -> str:
    return "\n".join(text.split("\n")[1:]) or text


# --------------------------------------------------------------------------- hiển thị


def sem_line(n: GraphNode) -> str:
    p = n.props
    if n.label == "CheTai":
        loai = p.get("loai")
        if loai == "phat_tien":
            amt = f"{_vnd(p.get('min_vnd'))}–{_vnd(p.get('max_vnd'))} đồng"
        elif loai in ("tuoc_quyen", "dinh_chi"):
            amt = f"{p.get('min_thang')}–{p.get('max_thang')} tháng {p.get('doi_tuong') or ''}"
        else:
            amt = str(p.get("doi_tuong") or "")
        return f"CheTai {loai}: {amt.strip()} (nêu tại {p.get('unit_id')})"
    if n.label == "DiemGPLX":
        return f"DiemGPLX: trừ {p.get('so_diem')} điểm (nêu tại {p.get('unit_id')})"
    return f"{n.label}: {p.get('ten') or p.get('name') or ''} (nêu tại {p.get('unit_id')})"


def _vnd(v: Any) -> str:
    return f"{int(v):,}".replace(",", ".") if isinstance(v, int) else str(v)


def suggested_numbers(sem: Sequence[GraphNode]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for n in sem:
        p = n.props
        if n.label == "CheTai" and p.get("loai") == "phat_tien":
            out += [{"value": p.get(k), "unit": "vnd"} for k in ("min_vnd", "max_vnd")]
        elif n.label == "CheTai" and p.get("loai") in ("tuoc_quyen", "dinh_chi"):
            out += [{"value": p.get(k), "unit": "thang"} for k in ("min_thang", "max_thang")]
        elif n.label == "DiemGPLX":
            out.append({"value": p.get("so_diem"), "unit": "diem"})
    seen: set[str] = set()
    uniq = []
    for x in out:
        k = json.dumps(x, sort_keys=True)
        if x["value"] is not None and k not in seen:
            seen.add(k)
            uniq.append(x)
    return uniq


def _clip(text: str, n: int) -> str:
    return text if len(text) <= n else text[:n].rsplit(" ", 1)[0] + " …"


def _quote(text: str) -> list[str]:
    return [f"> {ln}" if ln else ">" for ln in text.split("\n")]


def render_worksheet(
    sugs: Sequence[Suggestion],
    store: BaseGraphStore,
    targets: Targets,
    cfg: PlanConfig,
    stats: Mapping[str, Any],
) -> str:
    gv = GraphView(store)
    facts_cache: dict[str, ChunkFacts] = {}

    def facts(c: Chunk, d: date) -> ChunkFacts:
        k = f"{c.chunk_id}|{d}"
        if k not in facts_cache:
            facts_cache[k] = chunk_facts(gv, [c], d)[0]
        return facts_cache[k]

    lines = [
        "# Phiếu viết tập test (M9)",
        "",
        "Phiếu này chỉ **gợi ý điều khoản** để bạn viết câu hỏi; công cụ không viết câu hỏi hay "
        "đáp án. Mỗi câu bạn viết là một dòng JSON trong `data/qa/test.jsonl` (mẫu dưới mỗi gợi "
        "ý đã điền sẵn `gold_units` và con số lấy bằng rule — sửa/bỏ tuỳ câu bạn viết). Kiểm tra "
        "bằng `uv run python -m scripts.qa_tool validate --split test`.",
        "",
        f"- Ngày áp dụng mặc định: {cfg.as_of} (mốc chốt dữ liệu) · seed {cfg.seed} · "
        f"{stats['n_chunks_active']:,} chunk hiệu lực.",
        "- Trường: `qid` (duy nhất, vd `t-0001`), `question`, `as_of`, `question_type`, `tier`, "
        "`answer`, `gold_units`, `required_numbers` (`{value, unit, unit_id?}`; unit ∈ vnd, diem, "
        "thang, ngay, nam, gio, km_h, km, m, tan, cho, phan_tram, mg, khac), `pair_id` (cặp "
        "theo_thoi_diem), `notes`. `source` mặc định `human`.",
        "- Con số trong `required_numbers` phải có trong text phiên bản tại `as_of` hoặc là thuộc "
        "tính chế tài của đồ thị; validator báo lỗi nếu không.",
        "- `theo_thoi_diem`: viết **hai** câu cùng `pair_id`, một ngày trước và một ngày sau mốc; "
        "đáp án phải khác nhau.",
        "- `ngoai_pham_vi`: `gold_units` rỗng, `tier` null; câu hỏi nằm ngoài dữ liệu (lĩnh vực "
        "khác, văn bản không có trong danh mục, …) — hệ thống phải từ chối.",
        "",
        "## Hạn mức",
        "",
        "| Loại | Hạn mức | Mô tả | Số gợi ý |",
        "| --- | ---: | --- | ---: |",
    ]
    n_by = defaultdict(int)
    for s in sugs:
        n_by[s.qtype] += 1
    for k, v in targets.question_type.items():
        lines.append(f"| {k} | {v} | {QUESTION_TYPE_DOC.get(k, '')} | {n_by.get(k, 0)} |")
    lines += [
        "",
        "Tier (câu có tier; `ngoai_pham_vi` không tính): "
        + ", ".join(f"{k} ≈ {v:.0f}" for k, v in targets.tier_expected().items()),
        "",
        "Kho ứng viên theo loại × tier: "
        + "; ".join(f"{k} {dict(v)}" for k, v in stats["pool"].items()),
        "",
    ]
    cur = None
    for s in sugs:
        if s.qtype != cur:
            cur = s.qtype
            lines += [f"## {cur} — {QUESTION_TYPE_DOC.get(cur, '')}", ""]
        lines += _render_one(s, gv, facts, cfg)
    return "\n".join(lines) + "\n"


def _render_one(s: Suggestion, gv: GraphView, facts: Any, cfg: PlanConfig) -> list[str]:
    head = s.chunks[-1]
    doc = gv.doc(head.doc_id)
    lines = [
        f"### {s.sid} · tier {s.tier} · {head.unit_id}",
        "",
        doc_label(doc)
        + (f" · {s.note}" if s.note else "")
        + (f" · ngày đổi {s.change_date}" if s.change_date else ""),
        "",
    ]
    sems: list[GraphNode] = []
    if s.qtype == "theo_thoi_diem":
        before = s.chunks[0] if len(s.chunks) == 2 else None
        for label, c, d in (("Trước mốc", before, s.dates[0]), ("Sau mốc", head, s.dates[1])):
            if c is None:
                lines += [f"**{label} ({d})**: chưa có hiệu lực (không có phiên bản).", ""]
                continue
            lines += [
                f"**{label} ({d})** · chunk `{c.chunk_id}` · hiệu lực {c.effective_from} → "
                f"{c.effective_to or 'nay'}",
                "",
                *_quote(_clip(c.text, cfg.max_text_chars)),
                "",
            ]
            for n in facts(c, d).sem:
                lines.append(f"- {sem_line(n)}")
            lines.append("")
        units = [head.unit_id]
        tmpl = [
            _template(s, units, s.dates[0], [], gv, pair=s.sid),
            _template(s, units, s.dates[1], [], gv, pair=s.sid),
        ]
    else:
        d = s.dates[0]
        for c in s.chunks:
            f = facts(c, d)
            lines += [
                f"`{c.chunk_id}` · hiệu lực {c.effective_from} → {c.effective_to or 'nay'}",
                "",
                *_quote(_clip(c.text, cfg.max_text_chars)),
                "",
            ]
            for n in f.sem:
                lines.append(f"- {sem_line(n)}")
            sems += f.sem
            lines.append("")
        units = s.gold_units or [c.unit_id for c in s.chunks]
        tmpl = [_template(s, units, d, suggested_numbers(sems), gv)]
    lines += ["Mẫu dòng:", "", "```json", *tmpl, "```", ""]
    return lines


def _template(
    s: Suggestion,
    units: Sequence[str],
    d: date,
    numbers: Sequence[Mapping[str, Any]],
    gv: GraphView,
    pair: str | None = None,
) -> str:
    rec: dict[str, Any] = {
        "qid": "",
        "question": "",
        "as_of": d.isoformat(),
        "question_type": s.qtype,
        "tier": s.tier,
        "answer": "",
        "gold_units": [u for u in units if gv.store.version_at(u, d) is not None],
        "required_numbers": list(numbers),
    }
    if pair:
        rec["pair_id"] = pair.replace("W-theo_thoi_diem-", "p-")
    return json.dumps(rec, ensure_ascii=False)


# --------------------------------------------------------------------------- show


def show_unit(store: BaseGraphStore, unit_id: str, as_of: date) -> list[str]:
    """Mọi thứ cần để viết câu hỏi về một unit tại một ngày."""
    gv = GraphView(store)
    n = store.get_node(unit_id)
    if n is None or n.label not in UNIT_LABELS:
        return [f"không có unit {unit_id}"]
    doc = gv.doc(str(n.props.get("doc_id")))
    lines = [
        f"{unit_id} ({n.label}) · {doc_label(doc)} · tier {doc.get('tier')} · as_of {as_of}",
        "",
        "Tổ tiên: " + " > ".join(store.ancestors(unit_id)),
    ]
    dieu = store.get_node(_dieu(unit_id))
    if dieu is not None:
        lines.append(f"Điều: {dieu.props.get('number')}. {dieu.props.get('title') or ''}")
    lines += ["", "Phiên bản:"]
    cur = store.version_at(unit_id, as_of)
    for v in store.versions(unit_id):
        p = v.props
        mark = " ← tại as_of" if cur is not None and v.id == cur.id else ""
        lines.append(
            f"  {v.id} [{p.get('status')}] {p.get('effective_from')} → "
            f"{p.get('effective_to') or 'nay'} · nguồn {p.get('source_unit_id') or 'bản gốc'}{mark}"
        )
    if cur is None:
        lines += ["", "(không có phiên bản hiệu lực tại as_of)"]
        return lines
    lines += ["", "Nội dung (cây con tại as_of):"]
    for u in store.subtree(unit_id, as_of=as_of):
        v = store.version_at(u, as_of)
        if v is not None:
            lines.append(f"  [{u}] {v.props.get('text')}")
    kids = store.children(unit_id, as_of=as_of)
    if kids:
        lines += ["", "Con: " + ", ".join(kids)]
    refs = store.references_from(unit_id, as_of)
    if refs:
        lines += ["", "Dẫn chiếu đi:"] + [
            f"  → {e.dst} ({e.props.get('pham_vi')}; “{e.props.get('span')}”)" for e in refs
        ]
    back = store.references_to(unit_id, as_of)
    if back:
        lines += ["", "Được dẫn chiếu bởi:"] + [f"  ← {unit_of_version_id(e.src)}" for e in back]
    chunk = [c for c in iter_chunks_for(store, unit_id) if c.covers(as_of)]
    facts = chunk_facts(gv, chunk, as_of) if chunk else []
    sem = [x for f in facts for x in f.sem]
    if sem:
        lines += ["", "Chế tài / điểm trừ (đồ thị M8):"] + [f"  - {sem_line(x)}" for x in sem]
        lines.append("  required_numbers gợi ý: " + json.dumps(suggested_numbers(sem)))
    return lines


def iter_chunks_for(store: BaseGraphStore, unit_id: str) -> list[Chunk]:
    """Chunk chứa ``unit_id`` (Khoản của nó, hoặc Điều nếu không chia Khoản)."""
    parts = unit_id.split("/")
    doc = parts[0]
    root = "/".join(parts[:3]) if len(parts) >= 3 and parts[2].startswith("K") else _dieu(unit_id)
    return [c for c in iter_chunks(store, [doc]) if c.unit_id in (root, _dieu(unit_id))]


__all__ = [
    "PLAN_TYPES",
    "ChunkFacts",
    "PlanConfig",
    "Suggestion",
    "allocate",
    "chunk_facts",
    "eligible",
    "iter_chunks_for",
    "plan_suggestions",
    "render_worksheet",
    "show_unit",
    "suggested_numbers",
    "theo_thoi_diem_candidates",
]
