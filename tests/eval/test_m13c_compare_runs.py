"""M13c: so biến thể giữa các lượt chạy trên tập dev."""

from __future__ import annotations

from trafficlaw.eval.report import compare_runs, render_compare_runs_md


def row(qid: str, qt: str, **m: float | None) -> dict:
    return {"qid": qid, "question_type": qt, "metrics": m}


def test_compare_runs_refusal_and_filter() -> None:
    base = [
        row("a", "da_buoc", tu_choi=1.0, tu_choi_dung=0.0, so_du=0.0),
        row("b", "da_buoc", tu_choi=0.0, tu_choi_dung=1.0, so_du=1.0),
        row("c", "muc_phat", tu_choi=0.0, tu_choi_dung=1.0, so_du=1.0),
        row("o", "ngoai_pham_vi", tu_choi=1.0, tu_choi_dung=1.0),
    ]
    other = [
        row("a", "da_buoc", tu_choi=0.0, tu_choi_dung=1.0, so_du=1.0),
        row("b", "da_buoc", tu_choi=0.0, tu_choi_dung=1.0, so_du=1.0),
        row("c", "muc_phat", tu_choi=0.0, tu_choi_dung=1.0, so_du=1.0),
        row("o", "ngoai_pham_vi", tu_choi=0.0, tu_choi_dung=0.0),
    ]
    res = compare_runs(base, {"v": other}, n_boot=50)
    # tu_choi chỉ trên câu trả lời được (3 câu): base 1/3, v 0/3
    assert res["describe"]["base"]["tu_choi"]["n"] == 3
    assert abs(res["describe"]["base"]["tu_choi"]["mean"] - 1 / 3) < 1e-9
    assert res["describe"]["v"]["tu_choi"]["mean"] == 0.0
    # từ chối: base precision 1/2, recall 1; v recall 0
    assert res["refusal"]["base"]["precision"] == 0.5 and res["refusal"]["base"]["recall"] == 1.0
    assert res["refusal"]["v"]["recall"] == 0.0
    assert res["compare"]["v"]["so_du"]["n"] == 3
    sub = compare_runs(base, {"v": other}, question_types=["da_buoc"], n_boot=50)
    assert sub["n_base"] == 2 and sub["refusal"]["base"]["n_ngoai_pham_vi"] == 0
    md = render_compare_runs_md(res, {"base": "G"})
    assert "| Chỉ số | G | v |" in md
