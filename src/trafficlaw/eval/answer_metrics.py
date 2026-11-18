"""Chỉ số tất định theo câu cho M13 (không cần LLM; judge cộng thêm ở ``judge.py``).

Một câu → ``dict[str, float | None]``; ``None`` = không áp dụng (loại khỏi trung bình chỉ số đó).

**Trạng thái câu trả lời** (mục 10): ``error`` không có bản ghi điểm (chưa xong, không tính sai);
``format_error`` tính là **sai**: mọi chỉ số dựa trên câu trả lời = 0 (trích dẫn, con số, từ chối
đúng, phiên bản đúng), chỉ số truy hồi vẫn tính từ giai đoạn 1.

Chỉ số (khoá ``dict``):

- Truy hồi (câu có ``gold_units``; RAG): ``r@1/5/10/20``, ``mrr@10``, ``ndcg@10`` — như M10/M11:
  chunk đúng = chunk hiệu lực tại ``as_of`` chứa gold (unit / tổ tiên / con cháu); recall cấp unit.
- ``tu_choi_dung`` (mọi câu): ``ngoai_pham_vi`` → đúng ⇔ ``answer_status`` ∈ {insufficient,
  out_of_scope}; câu khác → đúng ⇔ ``answered``; câu gold rỗng ("trước mốc" của
  ``theo_thoi_diem``) → ``None`` (từ chối hay trả lời "chưa có quy định" đều đúng; sửa M13c).
  ``tu_choi`` = hệ thống từ chối (để tính precision/recall từ chối ở báo cáo).
- Con số (câu có ``required_numbers``): tập số tìm được = số trong câu trả lời đã render (bỏ nhãn
  trích dẫn ``[...]``; ``400.000`` = 400000, ``02`` = 2) ∪ giá trị của mã ``N#`` đã dùng; so theo
  **giá trị** (Decimal), không so đơn vị. ``so_recall`` = tỷ lệ số yêu cầu tìm được; ``so_du`` =
  1 khi đủ hết.
- Trích dẫn (câu có gold): trích dẫn **hiển thị** (RAG: hợp lệ sau verify; B0: mọi trích dẫn tự
  khai). Khớp = unit trích trùng / tổ tiên / con cháu gold. ``trich_p`` = tỷ lệ trích dẫn khớp
  (câu không trích dẫn → ``None``, đếm riêng); ``trich_r`` = tỷ lệ gold được trích khớp;
  ``trich_gold`` = 1 khi có ít nhất một trích dẫn khớp.
- Hiệu lực: ``hieu_luc_nguon`` = tỷ lệ nguồn ngữ cảnh có hiệu lực tại ``as_of``;
  ``hieu_luc_trich`` = tỷ lệ trích dẫn hiển thị có phiên bản hiệu lực tại ``as_of`` (trạng thái
  khác ``het_hieu_luc``/``het_hieu_luc_khong_loc``).
- ``phien_ban_dung`` (câu ``theo_thoi_diem``): gold khác rỗng → có trích dẫn khớp gold mà chunk
  được trích **phủ** ``as_of`` (đúng trạng thái của ngày hỏi; B0: trích dẫn ``ok`` = unit có
  phiên bản hiệu lực); gold rỗng (câu "trước mốc", điều khoản chưa có) → đúng khi hệ thống từ chối
  **hoặc** không trích điều khoản của câu cùng cặp. Cặp đúng (báo cáo) = cả hai câu đúng và hai
  câu trả lời khác nhau.
- Đa bước (``da_buoc``): ``db_top5`` / ``db_ngu_canh`` / ``db_trich`` = tỷ lệ gold unit có chunk
  đúng trong top-5 / trong nguồn ngữ cảnh / được trích khớp; ``db_du`` = 1 khi ngữ cảnh phủ hết.
- Verify M12: ``vp_truoc``, ``vp_sau`` (số vi phạm con số trước/sau lượt sửa), ``cau_bo`` (câu văn
  bị bỏ), ``trich_bia`` (B0: trích dẫn tới văn bản/điều khoản không tồn tại), ``so_tu_do`` (B0:
  số không kiểm được).
"""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import Any

from trafficlaw.eval.retrieval_metrics import mrr_at, ndcg_at, recall_at
from trafficlaw.pipeline.answer import AnswerResult
from trafficlaw.retrieval.catalog import ChunkCatalog, is_same_or_related
from trafficlaw.retrieval.retrieve import RetrievalResult
from trafficlaw.verify.citations import Citation
from trafficlaw.verify.numbers import as_decimal, parse_numbers

REFUSALS = ("insufficient", "out_of_scope")
OUT_OF_EFFECT = ("het_hieu_luc", "het_hieu_luc_khong_loc")
FABRICATED = ("khong_ton_tai", "van_ban_khong_ro")

#: Chỉ số đúng/sai (McNemar) — mọi chỉ số còn lại là liên tục (Wilcoxon).
BINARY_METRICS = (
    "tu_choi_dung",
    "so_du",
    "trich_gold",
    "phien_ban_dung",
    "db_du",
    "judge_dung",
)
RETRIEVAL_METRICS = ("r@1", "r@5", "r@10", "r@20", "mrr@10", "ndcg@10")


@dataclass(frozen=True)
class GoldItem:
    """Câu test đã giải (``gold_versions`` tại ``as_of``)."""

    qid: str
    question: str
    as_of: date
    question_type: str
    tier: str | None
    answer: str | None
    gold_units: tuple[str, ...]
    gold_versions: tuple[str, ...]
    required_numbers: tuple[Decimal, ...]
    source: str
    pair_id: str | None = None
    partner_gold: tuple[str, ...] = field(default=())
    """Gold của câu cùng cặp ``theo_thoi_diem`` (để chấm câu "trước mốc")."""

    @property
    def source_kind(self) -> str:
        """``reviewed`` | ``claude`` | ``human`` | … (hậu tố sau ``+``; ``human`` khi không có)."""
        return self.source.rsplit("+", 1)[1] if "+" in self.source else self.source


def related(unit: str | None, gold: Sequence[str]) -> bool:
    return bool(unit) and any(is_same_or_related(str(unit), g) for g in gold)


def _ratio(a: int, b: int) -> float | None:
    return a / b if b else None


_CITE_LABEL = re.compile(r"\[[^\]]*\]")


def answer_numbers(res: AnswerResult) -> set[Decimal]:
    text = _CITE_LABEL.sub(" ", res.answer or "")
    out = {as_decimal(x) for x in parse_numbers(text)}
    for nu in res.numbers:
        for v in nu.values:
            try:
                out.add(as_decimal(v))
            except Exception:  # noqa: BLE001 - giá trị lạ trong bảng → bỏ qua
                continue
    return out


def shown_citations(res: AnswerResult) -> list[Citation]:
    """Trích dẫn người đọc thấy: RAG = hợp lệ; B0 = mọi trích dẫn tự khai."""
    if res.verify.numbers_verifiable:
        return [c for c in res.citations if c.valid]
    return [c for p in res.points for c in p.citations]


def retrieval_scores(
    item: GoldItem, r: RetrievalResult, catalog: ChunkCatalog
) -> dict[str, float | None]:
    rel = catalog.relevant(list(item.gold_units), item.as_of)
    return {
        "r@1": recall_at(r.ranked, rel, 1),
        "r@5": recall_at(r.ranked, rel, 5),
        "r@10": recall_at(r.ranked, rel, 10),
        "r@20": recall_at(r.ranked, rel, 20),
        "mrr@10": mrr_at(r.ranked, rel, 10),
        "ndcg@10": ndcg_at(r.ranked, rel, 10),
    }


def answer_scores(
    item: GoldItem,
    res: AnswerResult,
    catalog: ChunkCatalog,
    retrieval: RetrievalResult | None = None,
) -> dict[str, float | None]:
    """Chỉ số của một câu trả lời ``ok``/``format_error`` (``error`` không chấm)."""
    if res.status == "error":
        raise ValueError(f"{item.qid}: bản ghi error không chấm (chạy lại generate)")
    ok = res.status == "ok"
    oos = item.question_type == "ngoai_pham_vi"
    refused = ok and res.answer_status in REFUSALS
    out: dict[str, float | None] = {
        "ok": 1.0 if ok else 0.0,
        "tu_choi": 1.0 if refused else 0.0,
        "tu_choi_dung": None
        if not oos and not item.gold_units
        else (1.0 if ok and (refused == oos) else 0.0),
    }
    gold = list(item.gold_units)
    cites = shown_citations(res) if ok else []
    # con số
    if item.required_numbers:
        found = answer_numbers(res) if ok else set()
        hit = sum(1 for v in item.required_numbers if v in found)
        out["so_recall"] = hit / len(item.required_numbers)
        out["so_du"] = 1.0 if hit == len(item.required_numbers) else 0.0
    # trích dẫn
    if gold:
        matched = [c for c in cites if related(c.unit_id, gold)]
        out["trich_p"] = _ratio(len(matched), len(cites)) if ok else 0.0
        out["trich_r"] = sum(1 for g in gold if any(related(c.unit_id, [g]) for c in cites)) / len(
            gold
        )
        out["trich_gold"] = 1.0 if matched else 0.0
    out["n_trich"] = float(len(cites))
    # hiệu lực
    if ok and res.sources:
        out["hieu_luc_nguon"] = sum(1 for s in res.sources if s.in_effect) / len(res.sources)
    if cites:
        out["hieu_luc_trich"] = sum(1 for c in cites if c.status not in OUT_OF_EFFECT) / len(cites)
    # theo thời điểm
    if item.question_type == "theo_thoi_diem":
        if not ok:
            out["phien_ban_dung"] = 0.0
        elif gold:
            good = False
            for c in cites:
                if not related(c.unit_id, gold):
                    continue
                if c.chunk_id:
                    ch = catalog.by_id.get(c.chunk_id)
                    good = good or (ch is not None and ch.covers(item.as_of))
                else:
                    good = good or c.status == "ok"
            out["phien_ban_dung"] = 1.0 if good else 0.0
        else:
            partner = list(item.partner_gold)
            bad = bool(partner) and any(related(c.unit_id, partner) for c in cites)
            out["phien_ban_dung"] = 1.0 if refused or not bad else 0.0
    # đa bước
    if item.question_type == "da_buoc" and gold:
        rel = catalog.relevant(gold, item.as_of)
        ctx_chunks = {s.chunk_id for s in res.sources} if ok else set()
        if retrieval is not None:
            top5 = set(retrieval.ranked[:5])
            out["db_top5"] = sum(1 for g in gold if rel[g] & top5) / len(gold)
        if res.verify.numbers_verifiable:
            in_ctx = sum(1 for g in gold if rel[g] & ctx_chunks)
            out["db_ngu_canh"] = in_ctx / len(gold)
            out["db_du"] = 1.0 if in_ctx == len(gold) else 0.0
        out["db_trich"] = out["trich_r"]
    # verify M12
    v = res.verify
    if v.numbers_verifiable:
        out["vp_truoc"] = float(v.n_violations_before)
        out["vp_sau"] = float(v.n_violations_after_repair or 0)
        out["cau_bo"] = float(v.dropped_sentences)
    else:
        allc = [c for p in res.points for c in p.citations]
        out["trich_bia"] = float(sum(1 for c in allc if c.status in FABRICATED))
        out["so_tu_do"] = float(v.n_free_numbers)
    return out


def score_row(
    item: GoldItem,
    res: AnswerResult | None,
    retrieval: RetrievalResult | None,
    catalog: ChunkCatalog,
) -> dict[str, Any]:
    """Bản ghi ``scores_<cfg>.jsonl``: thông tin câu + chỉ số (truy hồi và/hoặc câu trả lời)."""
    row: dict[str, Any] = {
        "qid": item.qid,
        "question_type": item.question_type,
        "tier": item.tier,
        "source_kind": item.source_kind,
        "pair_id": item.pair_id,
        "gold_rong": item.question_type != "ngoai_pham_vi" and not item.gold_units,
        "answer_status": res.answer_status if res else None,
        "status": res.status if res else None,
    }
    m: dict[str, float | None] = {}
    if retrieval is not None and item.gold_units:
        m.update(retrieval_scores(item, retrieval, catalog))
    if res is not None and res.status != "error":
        m.update(answer_scores(item, res, catalog, retrieval))
    row["metrics"] = m
    return row


def answers_differ(a: str, b: str) -> bool:
    norm = lambda s: re.sub(r"\s+", " ", _CITE_LABEL.sub(" ", s or "")).strip().lower()  # noqa: E731
    return norm(a) != norm(b)


def pair_correct(
    rows: Mapping[str, Mapping[str, Any]],
    answers: Mapping[str, str],
    pairs: Mapping[str, list[str]],
) -> dict[str, float]:
    """``pair_id`` → 1/0: cả hai câu ``phien_ban_dung`` và hai câu trả lời khác nhau. Chỉ cặp mà
    cả hai câu đã chấm."""
    out: dict[str, float] = {}
    for pid, qids in sorted(pairs.items()):
        if len(qids) != 2 or any(q not in rows for q in qids):
            continue
        vals = [rows[q]["metrics"].get("phien_ban_dung") for q in qids]
        if any(v is None for v in vals):
            continue
        ok = all(v == 1.0 for v in vals) and answers_differ(
            answers.get(qids[0], ""), answers.get(qids[1], "")
        )
        out[pid] = 1.0 if ok else 0.0
    return out


__all__ = [
    "BINARY_METRICS",
    "FABRICATED",
    "REFUSALS",
    "RETRIEVAL_METRICS",
    "GoldItem",
    "answer_numbers",
    "answer_scores",
    "answers_differ",
    "pair_correct",
    "related",
    "retrieval_scores",
    "score_row",
    "shown_citations",
]
