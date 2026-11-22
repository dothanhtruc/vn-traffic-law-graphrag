"""M16: chương test sinh đúng số từ summary, kết luận theo kiểm định, báo thiếu nguồn, tất định."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from trafficlaw.eval.report import compare, config_summary
from trafficlaw.report.build import build_report, load_config
from trafficlaw.report.sections import SECTIONS, Ctx, _verdict_phrase, sec_test
from trafficlaw.report.sources import SourceStore, parse_specs

REPO = Path(__file__).resolve().parents[2]
CFG = load_config(REPO / "configs" / "report.yaml")


def _row(qid: str, qt: str, **m: float | None) -> dict[str, Any]:
    return {
        "qid": qid,
        "question_type": qt,
        "tier": "A",
        "source_kind": "reviewed",
        "gold_rong": False,
        "metrics": {"tu_choi": 0.0, **m},
    }


def _summary() -> dict[str, Any]:
    g = [
        _row("q1", "muc_phat", **{"r@5": 1.0, "mrr@10": 1.0, "judge_dung": 1.0, "so_du": 1.0}),
        _row("q2", "muc_phat", **{"r@5": 1.0, "mrr@10": 0.5, "judge_dung": 0.0, "so_du": 1.0}),
        _row("q3", "da_buoc", **{"r@5": 1.0, "mrr@10": 0.5, "judge_dung": 1.0, "so_du": None}),
        _row("q4", "da_buoc", **{"r@5": 0.0, "mrr@10": 0.0, "judge_dung": 0.0, "so_du": 0.0}),
    ]
    a3 = [
        _row("q1", "muc_phat", **{"r@5": 1.0, "mrr@10": 1.0, "judge_dung": 1.0, "so_du": 1.0}),
        _row("q2", "muc_phat", **{"r@5": 0.0, "mrr@10": 0.0, "judge_dung": 1.0, "so_du": 1.0}),
        _row("q3", "da_buoc", **{"r@5": 0.0, "mrr@10": 0.0, "judge_dung": 0.0, "so_du": None}),
        _row("q4", "da_buoc", **{"r@5": 0.0, "mrr@10": 0.0, "judge_dung": 0.0, "so_du": 0.0}),
    ]
    cfgs = {}
    for name, rows in (("G", g), ("A3", a3)):
        cfgs[name] = {
            "set": "full",
            "n_total": 4,
            "n_done": 4,
            "statuses": {"ok": 4},
            **config_summary(rows, {}, n_boot=50),
        }
    comp = compare(g, {"A3": a3}, ("r@5", "mrr@10", "judge_dung", "so_du"), n_boot=50)
    # Ép kết quả kiểm định để kiểm phần kết luận (truy hồi có ý nghĩa, câu trả lời không).
    comp["A3"]["r@5"]["p_holm"] = 0.01
    comp["A3"]["mrr@10"]["p_holm"] = 0.03
    comp["A3"]["judge_dung"]["p_holm"] = 1.0
    comp["A3"]["so_du"]["p_holm"] = 1.0
    return {
        "run_id": "r1",
        "compare_to": "G",
        "limitations": ["Hạn chế ghi trong run."],
        "configs": cfgs,
        "comparisons": comp,
        "judge": {
            "model_id": "judge-x",
            "family": "fam",
            "subset": "judge_200",
            "configs": {"G": {"llm": 3, "rule": 1, "format_error": 0, "error": 0}},
        },
    }


def _write(root: Path, rel: str, obj: Any) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")


def _ctx(root: Path) -> Ctx:
    vars_ = {"run_id": "r1", "variance_run": "v", "dev_run": "d"}
    return Ctx(store=SourceStore(root=root, specs=parse_specs(CFG["sources"], vars_)), cfg=CFG)


def _line(md: str, prefix: str, after: str) -> str:
    """Dòng đầu tiên bắt đầu bằng ``prefix`` xuất hiện sau đoạn ``after``."""
    tail = md[md.index(after) :]
    return next(x for x in tail.splitlines() if x.startswith(prefix))


def test_sec_test_numbers_match_hand_computed(tmp_path: Path) -> None:
    _write(tmp_path, "results/r1/summary.json", _summary())
    ctx = _ctx(tmp_path)
    md = sec_test(ctx)
    ret = _line(md, "| G |", "Truy hồi trên test")
    # G: R@5 = 3/4, MRR@10 = (1 + 0,5 + 0,5 + 0)/4.
    assert "| 75,0 (" in ret and "[4]" in ret and "| 50,0 (" in ret
    ret_a3 = _line(md, "| A3 |", "Truy hồi trên test")
    assert "| 25,0 (" in ret_a3
    # judge G 2/4 = 50,0; so_du G 2/3 = 66,7 [3].
    ans = _line(md, "| G |", "Câu trả lời trên test")
    assert "50,0 (" in ans and "66,7 (" in ans and "[3]" in ans
    # So sánh: hiệu R@5 = 0,75 − 0,25 = +50,0.
    cmp_r5 = _line(md, "| A3 |", "**Recall@5**")
    assert "| 4 | 75,0 | 25,0 | +50,0 (" in cmp_r5 and cmp_r5.endswith("| G hơn |")
    assert "Hạn chế ghi trong run." in md
    assert "**không** cải thiện có ý nghĩa" in md
    assert "G hơn có ý nghĩa ở Recall@5, MRR@10" in md
    names = [f.name for f in ctx.figures]
    assert names == ["test_retrieval", "test_answer", "test_diff_forest", "test_r5_by_type"]


def test_verdict_phrase() -> None:
    comp = {
        "r@5": {"p_holm": 0.01, "diff": 0.03},
        "mrr@10": {"p_holm": 0.01, "diff": -0.02},
        "judge_dung": {"p_holm": 0.5, "diff": 0.1},
    }
    s = _verdict_phrase(comp, ["r@5", "mrr@10", "judge_dung", "so_du"], 0.05, "G")
    assert s == (
        "G hơn có ý nghĩa ở Recall@5; G **kém** có ý nghĩa ở MRR@10;"
        " không khác biệt có ý nghĩa ở Judge: đúng hoàn toàn"
    )
    assert _verdict_phrase(comp, ["judge_dung"], 0.05, "G") == (
        "không khác biệt có ý nghĩa ở chỉ số nào"
    )
    assert _verdict_phrase(comp, ["so_du"], 0.05, "G") == "không áp dụng"


def test_missing_sources_reported_and_deterministic(tmp_path: Path) -> None:
    out1 = build_report(tmp_path, CFG, out_dir=tmp_path / "o1", draw=False)
    out2 = build_report(tmp_path, CFG, out_dir=tmp_path / "o2", draw=False)
    a = (tmp_path / "o1" / "report.md").read_bytes()
    assert a == (tmp_path / "o2" / "report.md").read_bytes()
    assert (tmp_path / "o1" / "sources.json").read_bytes() == (
        tmp_path / "o2" / "sources.json"
    ).read_bytes()
    text = a.decode("utf-8")
    # Mọi chương dữ liệu đều báo thiếu nguồn, không tự điền số.
    assert text.count("**Thiếu nguồn**") == len(SECTIONS) - 1  # chương hạn chế vẫn sinh được
    assert out1.missing and out1.missing == out2.missing
    man = json.loads((tmp_path / "o1" / "sources.json").read_text(encoding="utf-8"))
    assert all(r["status"] == "missing" for r in man["sources"])
    assert "results/r1" not in text  # run_id mặc định từ cấu hình
    assert "m14-test" in text


def test_figures_deterministic(tmp_path: Path) -> None:
    pytest.importorskip("matplotlib")
    _write(tmp_path, "results/m14-test/summary.json", _summary())
    r1 = build_report(tmp_path, CFG, out_dir=tmp_path / "o1")
    r2 = build_report(tmp_path, CFG, out_dir=tmp_path / "o2")
    assert r1.figures == ["test_retrieval", "test_answer", "test_diff_forest", "test_r5_by_type"]
    for name in r1.figures:
        b1 = (tmp_path / "o1" / "figures" / f"{name}.png").read_bytes()
        assert b1 == (tmp_path / "o2" / "figures" / f"{name}.png").read_bytes()
    assert r1.report_path.read_bytes() == r2.report_path.read_bytes()
    # summary giả thiếu trường `serve` ⇒ chương tổng quan báo lỗi schema (không crash, không điền).
    assert [e.split(":")[0] for e in r1.errors] == ["tong_quan"]
    assert "**Lỗi đọc nguồn**" in r1.report_path.read_text(encoding="utf-8")


def test_without_matplotlib_figures_are_listed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from trafficlaw.report import figures

    monkeypatch.setattr(figures, "available", lambda: False)
    _write(tmp_path, "results/m14-test/summary.json", _summary())
    r = build_report(tmp_path, CFG, out_dir=tmp_path / "o")
    assert r.figures == [] and "test_retrieval" in r.skipped_figures
    assert "Hình chưa vẽ" in r.report_path.read_text(encoding="utf-8")
