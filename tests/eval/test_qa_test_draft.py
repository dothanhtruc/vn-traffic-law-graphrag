"""Nháp câu test (LLM viết, người sửa — quyết định 17/11/2026): đầu vào từ gợi ý phiếu viết,
hậu kiểm/cờ, resume, kiểm tra ``draft_id`` trong validator, tỷ lệ sửa, chặn model cùng họ."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

import pytest

from scripts import qa_tool
from trafficlaw.eval.qa_plan import Suggestion
from trafficlaw.eval.qa_schema import QAItem
from trafficlaw.eval.qa_test_draft import (
    DraftConfig,
    StyleSpec,
    answer_flags,
    assemble,
    build_inputs,
    build_messages,
    draft_key,
    edit_stats,
    input_key,
    latest_parsed,
    pick_style,
    question_flags,
    run_drafts,
)
from trafficlaw.eval.qa_validate import check_drafts, validate_items
from trafficlaw.graph.embedded import EmbeddedStore
from trafficlaw.graph.store import GraphEdge, GraphNode
from trafficlaw.llm import LLMClient, load_llm_config, load_prompt
from trafficlaw.llm.providers.fake import FakeClient, ok, server_error
from trafficlaw.llm.retry import RetryPolicy
from trafficlaw.llm.types import LLMRequest
from trafficlaw.retrieval.chunking import iter_chunks
from trafficlaw.utils.jsonl import read_jsonl

ROOT = Path(__file__).resolve().parents[2]
MINI = ROOT / "tests/fixtures/mini_graph"
K5 = "ND168-2024/D6/K5"
AS_OF = date(2026, 11, 3)
CFG = DraftConfig(
    model_id="fake-model",
    personas=["tài xế xe tải", "sinh viên đi xe máy", "cán bộ phường"],
    styles=[
        StyleSpec(name="ngan", desc="một câu ngắn", weight=0.2),
        StyleSpec(name="tinh_huong", desc="tình huống bản thân", weight=0.8),
    ],
)


@pytest.fixture(scope="module")
def store() -> EmbeddedStore:
    """mini_graph + CheTai phạt tiền nêu ở ND168 Đ6 K5 (áp cho Điểm a)."""
    st = EmbeddedStore.from_dir(MINI)
    st.upsert_nodes(
        [
            GraphNode(
                f"CHETAI:{K5}@v0#0",
                "CheTai",
                {
                    "unit_id": K5,
                    "version_id": f"{K5}@v0",
                    "loai": "phat_tien",
                    "min_vnd": 4000000,
                    "max_vnd": 6000000,
                },
            )
        ]
    )
    st.upsert_edges(
        [
            GraphEdge.make(
                "BI_XU_PHAT",
                f"{K5}/a@v0",
                f"CHETAI:{K5}@v0#0",
                {"effective_from": "2025-01-01", "effective_to": None, "nguon": "ke_thua_khoan"},
            )
        ]
    )
    return st


@pytest.fixture(scope="module")
def k5_chunk(store: EmbeddedStore):  # type: ignore[no-untyped-def]
    return next(
        c for c in iter_chunks(store, ["ND168-2024"]) if c.unit_id == K5 and c.covers(AS_OF)
    )


def sug_muc_phat(chunk) -> Suggestion:  # type: ignore[no-untyped-def]
    return Suggestion("W-muc_phat-001", "muc_phat", "A", [chunk], [AS_OF])


def sug_time(chunk) -> Suggestion:  # type: ignore[no-untyped-def]
    d = chunk.effective_from
    return Suggestion(
        "W-theo_thoi_diem-001",
        "theo_thoi_diem",
        "A",
        [chunk],
        [date.fromordinal(d.toordinal() - 1), d],
        d,
        "trước mốc: chưa có hiệu lực",
    )


# --------------------------------------------------------------------------- đầu vào


def test_pick_style_deterministic_and_weighted() -> None:
    a = [pick_style(f"W-x-{i:03d}", CFG) for i in range(400)]
    b = [pick_style(f"W-x-{i:03d}", CFG) for i in range(400)]
    assert a == b
    share = sum(s.name == "ngan" for _, s in a) / len(a)
    assert 0.12 < share < 0.28
    assert {p for p, _ in a} == set(CFG.personas)


def test_build_inputs_muc_phat(store: EmbeddedStore, k5_chunk) -> None:  # type: ignore[no-untyped-def]
    (inp,) = build_inputs(store, [sug_muc_phat(k5_chunk)], CFG)
    assert inp.gold_default == [[K5]]
    assert K5 in inp.allowed_units and f"{K5}/a" in inp.allowed_units
    assert [(o.value, o.unit) for o in inp.numbers] == [(4000000, "vnd"), (6000000, "vnd")]
    msg = build_messages(load_prompt(CFG.prompt), inp)[0]["content"]
    assert "[0] 4.000.000 đồng" in msg and "[1] 6.000.000 đồng" in msg
    assert inp.persona in msg and inp.style.name in msg
    assert "$" not in msg  # mọi biến đã thay


def test_build_inputs_time_pair_not_yet_effective(store: EmbeddedStore, k5_chunk) -> None:  # type: ignore[no-untyped-def]
    (inp,) = build_inputs(store, [sug_time(k5_chunk)], CFG)
    assert inp.n_questions == 2
    assert inp.gold_default == [[], [K5]]
    msg = build_messages(load_prompt(CFG.prompt), inp)[0]["content"]
    assert "Chưa có hiệu lực" in msg
    assert inp.dates[0].isoformat() in msg and inp.dates[1].isoformat() in msg


def test_ngoai_pham_vi_not_drafted(store: EmbeddedStore, k5_chunk) -> None:  # type: ignore[no-untyped-def]
    s = Suggestion("W-ngoai_pham_vi-001", "ngoai_pham_vi", "A", [k5_chunk], [AS_OF])
    assert build_inputs(store, [s], CFG) == []


# --------------------------------------------------------------------------- hậu kiểm


def test_question_flags(store: EmbeddedStore, k5_chunk) -> None:  # type: ignore[no-untyped-def]
    (inp,) = build_inputs(store, [sug_muc_phat(k5_chunk)], CFG)
    words = inp.source_text.split("\n")[1].split()
    copied = " ".join(words[2:10])  # 8 từ liên tiếp của nguồn
    f = question_flags(f"Cho hỏi {copied} thì sao ạ?", inp, CFG)
    assert any(x.startswith("chep_nguyen_van") for x in f)
    assert "neu_dieu_khoan" in question_flags(
        "Theo khoản 5 Điều 6 thì tôi bị phạt bao nhiêu tiền vậy?", inp, CFG
    )
    assert "tham_chieu_ngu_canh" in question_flags(
        "Theo quy định này thì tôi bị phạt bao nhiêu tiền vậy?", inp, CFG
    )
    assert any(x.startswith("qua_ngan") for x in question_flags("Phạt bao nhiêu?", inp, CFG))
    assert (
        question_flags(
            "Em trai tôi đi xe máy chở ba người trên đường làng thì bị phạt thế nào?", inp, CFG
        )
        == []
    )


def test_answer_flags_strange_number(store: EmbeddedStore, k5_chunk) -> None:  # type: ignore[no-untyped-def]
    (inp,) = build_inputs(store, [sug_muc_phat(k5_chunk)], CFG)
    ok = "Bị phạt từ 4.000.000 đồng đến 6.000.000 đồng (khoản 5 Điều 6 Nghị định 168/2024/NĐ-CP)."
    assert answer_flags(ok, inp) == []
    bad = "Bị phạt từ 4.000.000 đồng đến 7.500.000 đồng."
    assert answer_flags(bad, inp) == ["so_la: 7500000"]


def _parsed(inp_sid: str, n_q: int, dates: list[date]) -> dict[str, Any]:
    qs = [
        {
            "as_of": "2020-01-01",  # sai → ép theo gợi ý
            "question": f"Anh tôi chạy xe chở hàng vào giờ cấm ở phố thì bị phạt thế nào? {j}",
            "answer": "Bị phạt từ 4.000.000 đồng đến 6.000.000 đồng."
            + (" Trước mốc chưa có." if j == 0 else ""),
            "gold_units": [f"{K5}/a", "LUAT36-2024/D9"],
            "required_numbers_idx": [0, 1, 7],
        }
        for j in range(n_q)
    ]
    return {"drafts": [{"questions": qs, "ghi_chu": "giả định cá nhân", "nghi_ngo": ""}]}


def test_assemble_flags_and_valid_item(store: EmbeddedStore, k5_chunk) -> None:  # type: ignore[no-untyped-def]
    (inp,) = build_inputs(store, [sug_muc_phat(k5_chunk)], CFG)
    key = draft_key("fake-model", load_prompt(CFG.prompt), CFG)
    (rec,) = assemble([inp], {inp.sid: _parsed(inp.sid, 1, inp.dates)}, key, CFG)
    it = rec.item
    assert it["as_of"] == AS_OF.isoformat()
    assert it["gold_units"] == [f"{K5}/a"]
    assert it["required_numbers"] == [
        {"value": 4000000, "unit": "vnd"},
        {"value": 6000000, "unit": "vnd"},
    ]
    assert it["source"] == "llm:fake-model+human" and it["draft_id"] == "W-muc_phat-001:1"
    assert it["qid"] == "t-muc_phat-001"
    assert any(f.startswith("as_of_sua") for f in rec.flags)
    assert "gold_ngoai_nguon: LUAT36-2024/D9" in rec.flags
    assert "chi_so_so_sai (7)" in rec.flags
    QAItem.model_validate(it)


def test_assemble_time_pair(store: EmbeddedStore, k5_chunk) -> None:  # type: ignore[no-untyped-def]
    (inp,) = build_inputs(store, [sug_time(k5_chunk)], CFG)
    key = draft_key("fake-model", load_prompt(CFG.prompt), CFG)
    recs = assemble([inp], {inp.sid: _parsed(inp.sid, 2, inp.dates)}, key, CFG)
    assert [r.draft_id for r in recs] == ["W-theo_thoi_diem-001:1a", "W-theo_thoi_diem-001:1b"]
    assert [r.item["qid"] for r in recs] == ["t-theo_thoi_diem-001a", "t-theo_thoi_diem-001b"]
    assert recs[0].item["gold_units"] == [] and recs[1].item["gold_units"] == [f"{K5}/a"]
    assert recs[0].item["pair_id"] == recs[1].item["pair_id"] == "p-001"
    assert [r.item["as_of"] for r in recs] == [d.isoformat() for d in inp.dates]


# --------------------------------------------------------------------------- chạy + resume


def _client(responder=None, script=None) -> LLMClient:  # type: ignore[no-untyped-def]
    fake = FakeClient(script, responder=responder)
    return LLMClient(fake, retry=RetryPolicy(max_retries=0, sleep=lambda s: None))  # type: ignore[arg-type]


def _responder(req: LLMRequest) -> str:
    n = 2 if "theo_thoi_diem" in req.messages[-1].content.split("Loại câu:")[1][:40] else 1
    return json.dumps(_parsed("x", n, []), ensure_ascii=False)


def test_run_resume_and_error_rerun(tmp_path: Path, store: EmbeddedStore, k5_chunk) -> None:  # type: ignore[no-untyped-def]
    inputs = build_inputs(store, [sug_muc_phat(k5_chunk), sug_time(k5_chunk)], CFG)
    prompt = load_prompt(CFG.prompt)
    raw = tmp_path / "raw.jsonl"
    script = [server_error(), ok(json.dumps(_parsed("x", 2, []), ensure_ascii=False))]
    out = run_drafts(inputs, CFG, _client(script=script), raw, prompt)
    assert out.n_called == 2 and out.by_status == {"error": 1, "ok": 1}
    out2 = run_drafts(inputs, CFG, _client(responder=_responder), raw, prompt)
    assert out2.n_todo == 1 and out2.by_status == {"ok": 1}
    out3 = run_drafts(inputs, CFG, _client(responder=_responder), raw, prompt)
    assert out3.n_todo == 0 and out3.n_called == 0
    key = draft_key("fake-model", prompt, CFG)
    parsed, status = latest_parsed(raw, key, {i.sid: input_key(prompt, i) for i in inputs})
    assert set(parsed) == {i.sid for i in inputs} and status == {"ok": 2}
    assert len(list(read_jsonl(raw))) == 3


# --------------------------------------------------------------------------- validator


def _draft_rec(store: EmbeddedStore, k5_chunk) -> dict[str, Any]:  # type: ignore[no-untyped-def]
    (inp,) = build_inputs(store, [sug_muc_phat(k5_chunk)], CFG)
    key = draft_key("fake-model", load_prompt(CFG.prompt), CFG)
    (rec,) = assemble([inp], {inp.sid: _parsed(inp.sid, 1, inp.dates)}, key, CFG)
    return rec.to_dict()


def _codes(issues) -> set[str]:  # type: ignore[no-untyped-def]
    return {i.code for i in issues if i.level == "error"}


def test_validator_draft_checks(store: EmbeddedStore, k5_chunk) -> None:  # type: ignore[no-untyped-def]
    d = _draft_rec(store, k5_chunk)
    drafts = {d["draft_id"]: d}
    unedited = dict(d["item"])
    res = validate_items([unedited], "test", store, drafts=drafts)
    assert "nhap_chua_sua" in _codes(res.issues)
    assert any(i.code == "dap_an_giu_nguyen_nhap" for i in res.issues)

    edited = dict(
        d["item"], question="Tôi lái xe tải nhỏ vào phố cấm giờ cao điểm thì bị xử phạt ra sao?"
    )
    edited["answer"] = (
        "Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng (khoản 5 Điều 6 Nghị định 168/2024/NĐ-CP)."
    )
    res = validate_items([edited], "test", store, drafts=drafts)
    assert not ({"nhap_chua_sua", "nguon_khong_khop", "nhap_khong_ton_tai"} & _codes(res.issues))

    items = [QAItem.model_validate(x) for x in (edited, dict(edited, qid="t-2"))]
    assert "nhap_dung_lai" in _codes(check_drafts(items, drafts))
    assert "nhap_khong_ton_tai" in _codes(check_drafts(items[:1], {}))
    wrong_model = QAItem.model_validate(dict(edited, source="llm:other+human"))
    assert "nguon_khong_khop" in _codes(check_drafts([wrong_model], drafts))

    human_with_draft = dict(edited, source="human")
    assert "nguon_khong_khop" in _codes(
        validate_items([human_with_draft], "test", store, drafts=drafts).issues
    )
    no_id = {k: v for k, v in edited.items() if k != "draft_id"}
    assert "thieu_draft_id" in _codes(validate_items([no_id], "test", store, drafts=drafts).issues)
    llm_only = dict(no_id, source="llm:fake-model")
    assert "nguon_khong_phai_nguoi" in _codes(validate_items([llm_only], "test", store).issues)


def test_edit_stats(store: EmbeddedStore, k5_chunk) -> None:  # type: ignore[no-untyped-def]
    d = _draft_rec(store, k5_chunk)
    drafts = {d["draft_id"]: d}
    same = QAItem.model_validate(d["item"])
    changed = QAItem.model_validate(
        dict(
            d["item"],
            qid="t-2",
            question="Câu hỏi khác hẳn về chuyện chở hàng giờ cấm?",
            gold_units=[K5],
        )
    )
    human = QAItem.model_validate(dict(d["item"], qid="t-3", source="human", draft_id=None))
    s = edit_stats([same, changed, human], drafts)
    assert s["n_from_draft"] == 2 and s["n_human"] == 1
    assert s["answer_unchanged"] == 1.0
    assert s["gold_changed"] == 0.5 and s["numbers_changed"] == 0.0
    assert 0.5 < s["question_similarity_mean"] < 1.0


# --------------------------------------------------------------------------- chặn model cùng họ


def test_draft_guard_families() -> None:
    env = qa_tool.QAEnv(ROOT)
    llm_cfg = load_llm_config(ROOT / "configs/llm.yaml")
    cfg = DraftConfig.model_validate(env.cfg["draft"])
    assert qa_tool.draft_guard(env, llm_cfg, "gemma3-12b", cfg) is None
    assert "cùng họ 'qwen'" in (qa_tool.draft_guard(env, llm_cfg, "qwen3-8b", cfg) or "")
    assert "trùng" in (qa_tool.draft_guard(env, llm_cfg, "mistral-small-3.2", cfg) or "")
    assert "không biết họ" in (qa_tool.draft_guard(env, llm_cfg, "model-la", cfg) or "")
