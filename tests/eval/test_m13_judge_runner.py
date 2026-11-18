"""M13 judge (FakeClient: ok, JSON lỗi → format_error, 500 → error rồi chạy lại; luật; từ chối
model cùng họ), runner (validate test, subsets lỗi thời, resume truy hồi, hash dữ liệu lệch),
smoke."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from tests.eval.test_m13_metrics import ans, cite, gold
from tests.retrieval.conftest import (  # noqa: F401
    cfg,
    make_ctx,
    mini_catalog,
    mini_dir,
    mini_store,
    tables,
)
from trafficlaw.eval.eval_config import load_eval_config
from trafficlaw.eval.judge import (
    JudgeContext,
    JudgeModelError,
    answer_hash,
    check_judge_model,
    judge_one,
    latest_judgements,
    render_for_judge,
    run_judge,
)
from trafficlaw.eval.qa_schema import QAItem
from trafficlaw.eval.qa_subsets import build_subsets, file_sha256
from trafficlaw.eval.runner import (
    StaleResultError,
    StaleSubsetsError,
    load_eval_data,
    load_retrievals,
    run_retrieve,
)
from trafficlaw.llm.client import LLMClient
from trafficlaw.llm.prompt_loader import load_prompt
from trafficlaw.llm.providers.fake import FakeClient, bad_json, ok, server_error
from trafficlaw.llm.retry import RetryPolicy
from trafficlaw.pipeline.answer import load_answer_config
from trafficlaw.retrieval.config import load_retrieval_config
from trafficlaw.utils.jsonl import read_jsonl

ROOT = Path(__file__).resolve().parents[2]
SMOKE = ROOT / "tests/fixtures/eval/smoke_test.jsonl"
K = "ND168-2024/D6"


def _jctx(steps) -> tuple[JudgeContext, FakeClient]:
    fake = FakeClient(steps, model_id="mistral-small-3.2")
    client = LLMClient(fake, retry=RetryPolicy(max_retries=0, sleep=lambda s: None))
    return JudgeContext(
        client=client, prompt=load_prompt("judge"), model_id="mistral-small-3.2"
    ), fake


def _j(d: int, dung: bool | None = None) -> str:
    return json.dumps(
        {"diem": d, "dung": d == 2 if dung is None else dung, "thieu": [], "sai": [], "ly_do": "r"}
    )


def test_render_hides_citations_and_config() -> None:
    a = ans(
        text="- Phạt 800.000 đồng [điểm a khoản 3 Điều 6 Nghị định 168/2024/NĐ-CP]\nKết luận: x"
    )
    t = render_for_judge(a)
    assert "[" not in t and "800.000 đồng" in t and "G" not in t.split()


def test_judge_ok_and_flags(tmp_path: Path) -> None:
    jctx, fake = _jctx([ok(_j(2)), ok(_j(1, dung=True))])
    it = gold()
    r1 = judge_one(it, ans(text="Phạt 800.000 đồng."), jctx)
    assert r1.status == "ok" and r1.diem == 2 and r1.dung and r1.judge_source == "llm"
    msg = fake.requests[0].messages[0].content
    assert "ĐÁP ÁN THAM CHIẾU" in msg and it.answer in msg and "Phạt 800.000 đồng." in msg
    r2 = judge_one(it, ans(text="khác"), jctx)
    assert r2.diem == 1 and r2.dung is False and r2.flags == ["dung_khong_khop"]


def test_judge_rules_without_llm() -> None:
    jctx, fake = _jctx([ok(_j(2))])
    oos = gold(question_type="ngoai_pham_vi", gold_units=(), tier=None)
    assert judge_one(oos, ans(answer_status="out_of_scope"), jctx).diem == 2
    assert judge_one(oos, ans(answer_status="answered"), jctx).diem == 0
    assert judge_one(gold(), ans(answer_status="insufficient"), jctx).diem == 0
    assert judge_one(gold(), ans(status="format_error"), jctx).diem == 0
    assert fake.n_calls == 0
    # gold rỗng (trước mốc) + từ chối ⇒ vẫn gọi LLM (đáp án tham chiếu quyết định)
    before = gold(question_type="theo_thoi_diem", gold_units=())
    assert judge_one(before, ans(answer_status="insufficient"), jctx).judge_source == "llm"


def test_judge_format_error_error_and_resume(tmp_path: Path) -> None:
    jctx, fake = _jctx([bad_json(), bad_json(), server_error(), ok(_j(2))])
    a1 = ans(text="câu một", cites=[cite(f"{K}/K3/a")])
    a2 = ans(text="câu hai").model_copy(update={"qid": "q2"})
    pairs = [(gold(), a1), (gold(qid="q2"), a2)]
    out = tmp_path / "judge_G.jsonl"
    st = run_judge(pairs, jctx, out)
    assert dict(st.statuses) == {"format_error": 1, "error": 1}
    n = fake.n_calls
    st2 = run_judge(pairs, jctx, out)  # chỉ chạy lại câu error
    assert st2.n_skipped == 1 and st2.n_written == 1 and fake.n_calls == n + 1
    st3 = run_judge(pairs, jctx, out)
    assert st3.n_written == 0 and fake.n_calls == n + 1
    latest = latest_judgements(out, model_id=jctx.model_id, prompt_hash=jctx.prompt_hash)
    assert latest[("q2", answer_hash(a2))].diem == 2
    assert latest[("q", answer_hash(a1))].status == "format_error"
    # câu trả lời đổi ⇒ answer_hash đổi ⇒ chấm lại
    a1b = ans(text="câu một sửa")
    assert answer_hash(a1b) != answer_hash(a1)


def test_check_judge_model() -> None:
    fam = {"qwen3-14b-awq": "qwen", "qwen3-8b": "qwen", "mistral-small-3.2": "mistral"}.get
    assert check_judge_model("mistral-small-3.2", "qwen3-14b-awq", fam) == "mistral"
    with pytest.raises(JudgeModelError):
        check_judge_model("qwen3-8b", "qwen3-14b-awq", fam)
    with pytest.raises(JudgeModelError):
        check_judge_model("qwen3-14b-awq", "qwen3-14b-awq", fam)
    with pytest.raises(JudgeModelError):
        check_judge_model("la-model", "qwen3-14b-awq", fam)


# --------------------------------------------------------------------------- runner


def _subsets(tmp: Path, test: Path) -> Path:
    items = [QAItem.model_validate(r) for r in read_jsonl(test)]
    p = tmp / "subsets.json"
    p.write_text(json.dumps(build_subsets(items, file_sha256(test))), encoding="utf-8")
    return p


def test_load_eval_data_validates_and_rejects_stale(tmp_path: Path, mini_store) -> None:  # noqa: F811
    test = tmp_path / "test.jsonl"
    shutil.copy(SMOKE, test)
    sub = _subsets(tmp_path, test)
    data = load_eval_data(test, sub, mini_store)
    assert len(data.items) == 20 and data.invalid == []
    pair = [it for it in data.items if it.pair_id == "sp-1"]
    assert {it.partner_gold for it in pair} == {(), (f"{K}/K1a",)}
    assert data.select("full") == data.items
    union = data.select("ablation_200|judge_200")
    assert {i.qid for i in union} == set(data.subsets["ablation_200"]) | set(
        data.subsets["judge_200"]
    )
    # câu lỗi validator bị loại + liệt kê
    bad = json.loads(SMOKE.read_text(encoding="utf-8").splitlines()[0])
    bad.update(qid="s-bad", gold_units=[f"{K}/K99"])
    with test.open("a", encoding="utf-8") as f:
        f.write(json.dumps(bad, ensure_ascii=False) + "\n")
    with pytest.raises(StaleSubsetsError):
        load_eval_data(test, sub, mini_store)
    sub = _subsets(tmp_path, test)
    data2 = load_eval_data(test, sub, mini_store)
    assert [x["qid"] for x in data2.invalid] == ["s-bad"]
    assert "s-bad" not in data2.by_qid and all("s-bad" not in v for v in data2.subsets.values())


def test_run_retrieve_resume_and_stale_meta(
    tmp_path: Path,
    cfg,  # noqa: F811
    mini_store,  # noqa: F811
    mini_catalog,  # noqa: F811
    tables,  # noqa: F811
) -> None:
    rctx = make_ctx(tmp_path, cfg, mini_store, mini_catalog, tables)
    test = tmp_path / "test.jsonl"
    shutil.copy(SMOKE, test)
    data = load_eval_data(test, None, mini_store)
    items = data.items[:5]
    out = tmp_path / "retrieve_G.jsonl"
    st = run_retrieve(items, "G", rctx, out, use_llm=False)
    assert st.n_written == 5
    st2 = run_retrieve(data.items[:7], "G", rctx, out, use_llm=False)
    assert st2.n_skipped == 5 and st2.n_written == 2
    assert len(load_retrievals(out, rctx.meta)) == 7
    with pytest.raises(StaleResultError):
        load_retrievals(out, {**rctx.meta, "data_version": "khac"})


def test_smoke_end_to_end(tmp_path: Path) -> None:
    from trafficlaw.eval.smoke import run_smoke

    ecfg = load_eval_config(ROOT / "configs/eval.yaml")
    s = run_smoke(
        ROOT,
        ecfg,
        load_retrieval_config(ROOT / "configs/retrieval.yaml"),
        load_answer_config(ROOT / "configs/answer.yaml"),
        out_dir=tmp_path / "smoke",
    )
    assert s["smoke_seconds"] < 60
    c1, c2 = s["smoke_llm_calls"]
    assert c1 > 0 and c2 == c1  # lần hai: resume, không gọi LLM
    for name, d in s["configs"].items():
        assert d["n_done"] == d["n_total"], name
    assert set(s["configs"]) == {"G", "B3", "B0", "B1", "B2", "A1", "A2"}
    assert "judge_dung" in s["configs"]["G"]["metrics"] and "r@5" in s["configs"]["B1"]["metrics"]
    assert "B0" in s["comparisons"] and s["variance"]["seeds"] == [42, 43, 44]
    rd = tmp_path / "smoke"
    v43 = [
        json.loads(x)
        for x in (rd / "answers_G_seed43.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert v43 and all(r["llm_params"] == {"seed": 43} for r in v43)
    assert all(r["llm_params"] is None for r in read_jsonl(rd / "answers_G.jsonl"))
    md = (rd / "summary.md").read_text(encoding="utf-8")
    assert "## Bảng chính" in md and "## So sánh G" in md and "Theo nguồn gốc" in md
    labels = list(read_jsonl(rd / "judge_check_labels.jsonl"))
    assert labels and all(r["claude_diem"] is None for r in labels)
    # phiếu kiểm định không lộ điểm/lý do của judge (judge giả ghi ly_do = "smoke")
    assert "smoke" not in (rd / "judge_check.md").read_text(encoding="utf-8")
    assert s["judge_check"]["status"] == "cho_xac_nhan"


def test_load_eval_data_oos_extra(tmp_path: Path, mini_store) -> None:  # noqa: F811
    """M13c: câu ngoai_pham_vi bổ sung (không đáp án) không qua validator test."""
    test = tmp_path / "test.jsonl"
    shutil.copy(SMOKE, test)
    oos = tmp_path / "oos.jsonl"
    row = {
        "qid": "oos-x",
        "question": "Thủ tục đăng ký tàu cá gồm những gì?",
        "as_of": "2026-11-03",
        "question_type": "ngoai_pham_vi",
        "gold_units": [],
        "required_numbers": [],
        "source": "llm:claude-opus-5-5",
    }
    oos.write_text(json.dumps(row, ensure_ascii=False) + "\n", encoding="utf-8")
    data = load_eval_data(test, None, mini_store, oos_path=oos)
    assert data.by_qid["oos-x"].question_type == "ngoai_pham_vi" and len(data.items) == 21
    oos.write_text(
        json.dumps({**row, "question_type": "muc_phat"}, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        load_eval_data(test, None, mini_store, oos_path=oos)
