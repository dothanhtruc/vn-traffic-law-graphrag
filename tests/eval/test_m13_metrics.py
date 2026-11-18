"""M13 chỉ số tất định theo câu (con số kiểu VN, citation P/R tổ tiên/con cháu, theo thời điểm,
từ chối, đa bước, B0) + tổng hợp/so sánh chỉ trên câu chung."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Any

import pytest

from tests.retrieval.conftest import mini_catalog, mini_dir, mini_store  # noqa: F401
from trafficlaw.eval.answer_metrics import (
    GoldItem,
    answer_scores,
    pair_correct,
    score_row,
)
from trafficlaw.eval.report import compare, config_summary, refusal_stats
from trafficlaw.pipeline.answer import AnswerResult
from trafficlaw.verify.citations import Citation

K = "ND168-2024/D6"
D = date(2026, 1, 1)


def gold(**kw: Any) -> GoldItem:
    base: dict[str, Any] = {
        "qid": "q",
        "question": "?",
        "as_of": D,
        "question_type": "muc_phat",
        "tier": "A",
        "answer": "x",
        "gold_units": (f"{K}/K3/a",),
        "gold_versions": (),
        "required_numbers": (),
        "source": "llm:gpt-oss-20b+claude",
    }
    base.update(kw)
    return GoldItem(**base)


def ans(
    *,
    text: str = "",
    status: str = "ok",
    answer_status: str | None = "answered",
    cites: list[Citation] | None = None,
    rag: bool = True,
    sources: list[dict[str, Any]] | None = None,
    as_of: date = D,
    **verify: Any,
) -> AnswerResult:
    cites = cites or []
    return AnswerResult.model_validate(
        {
            "run_id": "t",
            "config_name": "G" if rag else "B0",
            "qid": "q",
            "question": "?",
            "as_of": as_of,
            "as_of_param": as_of,
            "validity_filter": True,
            "retrieval": None,
            "sources": sources or [],
            "number_table": [],
            "answer": text,
            "points": [
                {
                    "text": text,
                    "raw_text": text,
                    "citations": [c.model_dump() for c in cites],
                    "numbers": [],
                }
            ]
            if cites
            else [],
            "citations": [c.model_dump() for c in cites if c.valid],
            "verify": {"numbers_verifiable": rag, **verify},
            "status": status,
            "answer_status": answer_status if status == "ok" else None,
            "model_id": "m",
            "prompt_hash": "p",
            "answer_prompt_hash": "p",
            "timestamp": "t",
        }
    )


def cite(unit: str, status: str = "ok", chunk: str | None = None) -> Citation:
    return Citation(ref=unit, status=status, unit_id=unit, chunk_id=chunk, label=unit)  # type: ignore[arg-type]


def test_numbers_vn_format(mini_catalog) -> None:  # noqa: F811
    it = gold(required_numbers=(Decimal(800000), Decimal(1000000)))
    a = ans(text="- Phạt tiền từ 800.000 đồng đến 1.000.000 đồng [điểm a khoản 3 Điều 6]")
    m = answer_scores(it, a, mini_catalog)
    assert m["so_du"] == 1.0 and m["so_recall"] == 1.0
    a2 = ans(text="- Phạt tiền 800.000 đồng [khoản 1.000.000]")  # số trong nhãn trích dẫn bị bỏ
    m2 = answer_scores(it, a2, mini_catalog)
    assert m2["so_recall"] == 0.5 and m2["so_du"] == 0.0
    it3 = gold(required_numbers=(Decimal(2),))
    assert answer_scores(it3, ans(text="Bị trừ 02 điểm."), mini_catalog)["so_du"] == 1.0


def test_citation_precision_recall_related(mini_catalog) -> None:  # noqa: F811
    it = gold(gold_units=(f"{K}/K3/a", f"{K}/K16/a"))
    a = ans(cites=[cite(f"{K}/K3"), cite(f"{K}/K1/b")])  # K3 là tổ tiên của gold K3/a
    m = answer_scores(it, a, mini_catalog)
    assert m["trich_p"] == 0.5 and m["trich_r"] == 0.5 and m["trich_gold"] == 1.0
    # trích con cháu của gold Khoản cũng khớp
    m2 = answer_scores(gold(gold_units=(f"{K}/K3",)), ans(cites=[cite(f"{K}/K3/b")]), mini_catalog)
    assert m2["trich_p"] == 1.0 and m2["trich_r"] == 1.0
    # không trích dẫn: P không xác định, R = 0
    m3 = answer_scores(it, ans(text="x"), mini_catalog)
    assert m3["trich_p"] is None and m3["trich_r"] == 0.0 and m3["n_trich"] == 0.0


def test_theo_thoi_diem_version(mini_catalog) -> None:  # noqa: F811
    it = gold(question_type="theo_thoi_diem", gold_units=(f"{K}/K3",), pair_id="p")
    old = f"{K}/K3#2025-01-01"
    new = f"{K}/K3#2026-01-01"
    assert (
        answer_scores(it, ans(cites=[cite(f"{K}/K3/a", chunk=new)]), mini_catalog)["phien_ban_dung"]
        == 1.0
    )
    assert (
        answer_scores(it, ans(cites=[cite(f"{K}/K3/a", chunk=old)]), mini_catalog)["phien_ban_dung"]
        == 0.0
    )
    # câu "trước mốc": gold rỗng, cặp với K1a (có hiệu lực từ 15/08/2026)
    before = gold(
        question_type="theo_thoi_diem",
        gold_units=(),
        as_of=date(2026, 8, 14),
        pair_id="p",
        partner_gold=(f"{K}/K1a",),
    )
    assert (
        answer_scores(before, ans(answer_status="insufficient"), mini_catalog)["phien_ban_dung"]
        == 1.0
    )
    assert (
        answer_scores(before, ans(cites=[cite(f"{K}/K1a")]), mini_catalog)["phien_ban_dung"] == 0.0
    )
    assert (
        answer_scores(before, ans(cites=[cite(f"{K}/K3")]), mini_catalog)["phien_ban_dung"] == 1.0
    )
    # B0: không có chunk ⇒ trích dẫn ok (unit có phiên bản hiệu lực) là đúng phiên bản
    b0 = ans(rag=False, cites=[cite(f"{K}/K3/a")])
    assert answer_scores(it, b0, mini_catalog)["phien_ban_dung"] == 1.0
    b0x = ans(rag=False, cites=[cite(f"{K}/K3/a", status="het_hieu_luc")])
    assert answer_scores(it, b0x, mini_catalog)["phien_ban_dung"] == 0.0


def test_pair_correct_requires_different_answers() -> None:
    rows = {
        "a": {"metrics": {"phien_ban_dung": 1.0}},
        "b": {"metrics": {"phien_ban_dung": 1.0}},
    }
    pairs = {"p": ["a", "b"]}
    assert pair_correct(rows, {"a": "x [S1]", "b": "y"}, pairs) == {"p": 1.0}
    assert pair_correct(rows, {"a": "X  [S1]", "b": "x"}, pairs) == {"p": 0.0}
    assert pair_correct({"a": rows["a"]}, {}, pairs) == {}


def test_refusal_and_format_error(mini_catalog) -> None:  # noqa: F811
    oos = gold(question_type="ngoai_pham_vi", gold_units=(), tier=None)
    assert (
        answer_scores(oos, ans(answer_status="out_of_scope"), mini_catalog)["tu_choi_dung"] == 1.0
    )
    assert answer_scores(oos, ans(answer_status="answered"), mini_catalog)["tu_choi_dung"] == 0.0
    it = gold(required_numbers=(Decimal(800000),))
    assert answer_scores(it, ans(answer_status="insufficient"), mini_catalog)["tu_choi_dung"] == 0.0
    fe = answer_scores(it, ans(status="format_error"), mini_catalog)
    assert fe["tu_choi_dung"] == 0.0 and fe["so_du"] == 0.0 and fe["trich_p"] == 0.0
    with pytest.raises(ValueError):
        answer_scores(it, ans(status="error"), mini_catalog)
    rows = [
        {"question_type": "ngoai_pham_vi", "metrics": {"tu_choi": 1.0}},
        {"question_type": "ngoai_pham_vi", "metrics": {"tu_choi": 0.0}},
        {"question_type": "muc_phat", "metrics": {"tu_choi": 1.0}},
        {"question_type": "muc_phat", "metrics": {"tu_choi": 0.0}},
    ]
    rs = refusal_stats(rows)
    assert rs["precision"] == 0.5 and rs["recall"] == 0.5 and rs["tu_choi_sai"] == 0.5
    empty = gold(question_type="theo_thoi_diem", gold_units=())
    for st in ("insufficient", "answered"):
        assert answer_scores(empty, ans(answer_status=st), mini_catalog)["tu_choi_dung"] is None
    # M13c: câu "trước mốc" gold rỗng — từ chối là đúng, không tính vào tu_choi_sai
    rows.append({"question_type": "theo_thoi_diem", "gold_rong": True, "metrics": {"tu_choi": 1.0}})
    rs = refusal_stats(rows)
    assert rs["precision"] == pytest.approx(2 / 3) and rs["precision_oos"] == pytest.approx(1 / 3)
    assert rs["tu_choi_sai"] == 0.5 and rs["tu_choi_gold_rong"] == 1.0 and rs["recall"] == 0.5


def test_da_buoc_and_b0(mini_catalog) -> None:  # noqa: F811
    it = gold(
        question_type="da_buoc", gold_units=(f"{K}/K3/h", f"{K}/K16/a"), as_of=date(2026, 11, 3)
    )
    src = {
        "sid": "S1",
        "chunk_id": f"{K}/K3#2026-08-15",
        "unit_id": f"{K}/K3",
        "doc_id": "ND168-2024",
        "version_ids": [],
        "effective_from": "2026-08-15",
        "effective_to": None,
        "origin": "top",
        "rank": 1,
        "score": 1.0,
        "edge_type": None,
        "label": "k3",
        "doc_label": "nd",
        "in_effect": True,
        "truncated": False,
    }
    a = ans(sources=[src], cites=[cite(f"{K}/K3/h")], as_of=date(2026, 11, 3))
    m = answer_scores(it, a, mini_catalog)
    assert m["db_ngu_canh"] == 0.5 and m["db_du"] == 0.0 and m["db_trich"] == 0.5
    assert m["hieu_luc_nguon"] == 1.0
    # B0: trích dẫn hiển thị gồm cả trích dẫn sai; trích dẫn bịa được đếm
    b0 = ans(rag=False, cites=[cite(f"{K}/K3/a"), cite("ND168-2024/D999", status="khong_ton_tai")])
    mb = answer_scores(gold(), b0, mini_catalog)
    assert mb["trich_p"] == 0.5 and mb["trich_bia"] == 1.0 and "vp_truoc" not in mb


def test_score_row_and_compare_common_only(mini_catalog) -> None:  # noqa: F811
    r = score_row(gold(), ans(cites=[cite(f"{K}/K3/a")]), None, mini_catalog)
    assert r["source_kind"] == "claude" and r["metrics"]["trich_gold"] == 1.0

    def row(q: str, **m: float) -> dict[str, Any]:
        return {
            "qid": q,
            "question_type": "muc_phat",
            "tier": "A",
            "source_kind": "claude",
            "metrics": m,
        }

    base = [row("a", judge_dung=1.0), row("b", judge_dung=1.0), row("c", judge_dung=0.0)]
    other = [row("a", judge_dung=0.0), row("b", judge_dung=1.0)]  # "c" chưa xong ở cấu hình khác
    res = compare(base, {"X": other}, metrics=["judge_dung"])
    d = res["X"]["judge_dung"]
    assert d["n"] == 2 and d["mean_base"] == 1.0 and d["mean_other"] == 0.5
    assert (d["b"], d["c"]) == (1, 0) and d["p"] == pytest.approx(1.0) and d["p_holm"] == d["p"]
    s = config_summary(base, {"p": 1.0})
    assert s["metrics"]["judge_dung"]["n"] == 3 and s["pairs"] == {"n": 1, "dung": 1.0}
    assert s["by_source"]["claude"]["judge_dung"]["n"] == 3
