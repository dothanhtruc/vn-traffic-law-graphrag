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
    assert cfg.model_id == "gpt-oss-20b"
    assert qa_tool.draft_guard(env, llm_cfg, "gpt-oss-20b", cfg) is None
    assert qa_tool.draft_guard(env, llm_cfg, "gemma3-12b", cfg) is None
    assert "cùng họ 'qwen'" in (qa_tool.draft_guard(env, llm_cfg, "qwen3-8b", cfg) or "")
    assert "trùng" in (qa_tool.draft_guard(env, llm_cfg, "mistral-small-3.2", cfg) or "")
    assert "không biết họ" in (qa_tool.draft_guard(env, llm_cfg, "model-la", cfg) or "")


def test_reasoning_effort_sent_only_when_set(
    store: EmbeddedStore, k5_chunk, tmp_path: Path
) -> None:  # type: ignore[no-untyped-def]
    from trafficlaw.llm.providers.openai_compat import OpenAICompatProvider
    from trafficlaw.llm.types import LLMRequest, Message

    prov = OpenAICompatProvider(
        name="local", base_url="http://127.0.0.1:1/v1", model_id="m", api_key="k"
    )
    req = LLMRequest(
        messages=[Message(role="user", content="x")],
        params={"reasoning_effort": "low", "max_output_tokens": 9},
    )
    body = prov.build_body(req)
    assert body["reasoning_effort"] == "low" and body["max_tokens"] == 9
    assert "reasoning_effort" not in prov.build_body(LLMRequest(messages=req.messages, params={}))

    inputs = build_inputs(store, [sug_muc_phat(k5_chunk)], CFG)
    seen: list[dict[str, Any]] = []

    def resp(r: LLMRequest) -> str:
        seen.append(dict(r.params))
        return json.dumps(_parsed("x", 1, []), ensure_ascii=False)

    cfg = CFG.model_copy(update={"reasoning_effort": "low"})
    run_drafts(
        inputs, cfg, _client(responder=resp), tmp_path / "raw.jsonl", load_prompt(cfg.prompt)
    )
    assert seen and seen[0].get("reasoning_effort") == "low"


# --------------------------------------------------------------------------- nhập tự động


def _rec(sid: str, k: int, j: int, flags: list[str], qid: str) -> dict[str, Any]:
    return {
        "sid": sid,
        "k": k,
        "j": j,
        "flags": flags,
        "model_id": "fake-model",
        "draft_id": f"{sid}:{k}",
        "item": {"qid": qid, "source": "llm:fake-model+human"},
    }


def test_select_auto_strict() -> None:
    from trafficlaw.eval.qa_test_draft import select_auto

    recs = [
        _rec("W-a-001", 1, 0, ["chep_nguyen_van: “x …”"], "t-a-001"),
        _rec("W-a-001", 2, 0, [], "t-a-001"),
        _rec("W-a-002", 1, 0, ["so_la: 7"], "t-a-002"),
        _rec("W-a-002", 2, 0, ["qua_dai (60 từ)"], "t-a-002"),
        _rec("W-t-001", 1, 0, [], "t-t-001a"),
        _rec("W-t-001", 1, 1, ["as_of_sua (x → y)"], "t-t-001b"),
        _rec("W-t-001", 2, 1, [], "t-t-001b"),
        _rec("W-t-001", 2, 0, [], "t-t-001a"),
    ]
    items, skipped = select_auto(recs)
    assert [it["qid"] for it in items] == ["t-a-001", "t-t-001a", "t-t-001b"]
    assert all(it["source"] == "llm:fake-model+reviewed" for it in items)
    assert set(skipped) == {"W-a-002"} and len(skipped["W-a-002"]) == 2


def test_validator_reviewed(store: EmbeddedStore, k5_chunk) -> None:  # type: ignore[no-untyped-def]
    d = _draft_rec(store, k5_chunk)
    drafts = {d["draft_id"]: d}
    reviewed = dict(d["item"], source="llm:fake-model+reviewed")
    codes = _codes(validate_items([reviewed], "test", store, drafts=drafts).issues)
    assert not ({"nhap_chua_sua", "reviewed_nhung_da_sua", "nguon_khong_phai_nguoi"} & codes)
    changed = dict(reviewed, question="Câu hỏi đã được sửa khác hẳn bản nháp gốc rồi nhé?")
    codes = _codes(validate_items([changed], "test", store, drafts=drafts).issues)
    assert "reviewed_nhung_da_sua" in codes
    s = edit_stats([QAItem.model_validate(reviewed)], drafts)
    assert s["n_reviewed_unedited"] == 1 and s["n_from_draft"] == 0


def test_round_ids_and_quota_cap() -> None:
    from trafficlaw.eval.qa_test_draft import cap_quota, pair_id_for, qid_for

    assert qid_for("W-muc_phat-001", 0, 1) == "t-muc_phat-001"
    assert qid_for("W2-muc_phat-001", 0, 1) == "t2-muc_phat-001"
    assert qid_for("W2-theo_thoi_diem-007", 1, 2) == "t2-theo_thoi_diem-007b"
    assert pair_id_for("W-theo_thoi_diem-003") == "p-003"
    assert pair_id_for("W2-theo_thoi_diem-003") == "p2-003"
    items = [
        {"qid": "a", "question_type": "muc_phat"},
        {"qid": "b", "question_type": "muc_phat"},
        {"qid": "c1", "question_type": "theo_thoi_diem", "pair_id": "p-1"},
        {"qid": "c2", "question_type": "theo_thoi_diem", "pair_id": "p-1"},
        {"qid": "d1", "question_type": "theo_thoi_diem", "pair_id": "p-2"},
        {"qid": "d2", "question_type": "theo_thoi_diem", "pair_id": "p-2"},
    ]
    keep, dropped = cap_quota(items, {"muc_phat": 1, "theo_thoi_diem": 3})
    assert [x["qid"] for x in keep] == ["a", "c1", "c2"]
    assert dropped == ["b", "d1", "d2"]


def test_plan_round2_excludes_used_units() -> None:
    from dataclasses import replace

    from trafficlaw.eval.qa_plan import PlanConfig, plan_suggestions
    from trafficlaw.eval.qa_validate import Targets

    st = EmbeddedStore.from_dir(MINI)
    t = Targets(total=10, tier={"A": 1}, question_type={"hanh_vi_cam_nghia_vu": 3})
    used: set[str] = set()
    r1, _ = plan_suggestions(st, t, PlanConfig(), used)
    r2, _ = plan_suggestions(st, t, replace(PlanConfig(), sid_prefix="W2"), used)
    u1 = {c.unit_id for s in r1 for c in s.chunks}
    u2 = {c.unit_id for s in r2 for c in s.chunks}
    assert r1 and not (u1 & u2)
    assert all(s.sid.startswith("W2-") for s in r2)
    again, _ = plan_suggestions(st, t, PlanConfig())
    assert [s.sid for s in again] == [s.sid for s in r1]


def test_balance_quota_prefers_missing_tier() -> None:
    from trafficlaw.eval.qa_test_draft import balance_quota

    items = [
        {"qid": "a1", "question_type": "x", "tier": "A"},
        {"qid": "a2", "question_type": "x", "tier": "A"},
        {"qid": "a3", "question_type": "x", "tier": "A"},
        {"qid": "b1", "question_type": "x", "tier": "B"},
        {"qid": "p1", "question_type": "y", "tier": "B", "pair_id": "p"},
        {"qid": "p2", "question_type": "y", "tier": "B", "pair_id": "p"},
        {"qid": "o1", "question_type": "ngoai_pham_vi", "tier": None},
        {"qid": "o2", "question_type": "ngoai_pham_vi", "tier": None},
    ]
    keep, dropped = balance_quota(items, {"x": 3, "y": 2, "ngoai_pham_vi": 1}, {"A": 3.0, "B": 3.0})
    kept = {x["qid"] for x in keep}
    assert "b1" in kept and {"p1", "p2"} <= kept and "o1" in kept
    assert len([q for q in kept if q.startswith("a")]) == 2
    assert set(dropped) == {"a3", "o2"}


def test_assemble_oos_flags_and_items() -> None:
    from trafficlaw.eval.qa_test_draft import (
        OOSCategory,
        assemble_oos,
        build_oos_inputs,
        oos_messages,
    )

    cfg = CFG.model_copy(
        update={
            "oos_categories": [
                OOSCategory(name="duong_sat", desc="đường sắt"),
                OOSCategory(name="nuoc_ngoai", desc="nước ngoài"),
            ],
            "oos_calls_per_category": 1,
        }
    )
    inputs = build_oos_inputs(cfg)
    assert [i.sid for i in inputs] == ["O-duong_sat-1", "O-nuoc_ngoai-1"]
    msg = oos_messages(load_prompt(cfg.oos_prompt), inputs[0], cfg)[0]["content"]
    assert "duong_sat" in msg and "$" not in msg
    q1 = "Vé tàu hỏa từ Hà Nội vào Sài Gòn hoàn lại thì bị trừ bao nhiêu phần trăm?"
    parsed = {
        "O-duong_sat-1": {"questions": [{"question": q1, "answer": "Ngoài phạm vi."}]},
        "O-nuoc_ngoai-1": {
            "questions": [
                {"question": "Ở Nhật?", "answer": "Ngoài phạm vi."},
                {"question": q1 + " ạ", "answer": "Ngoài phạm vi."},
            ]
        },
    }
    key = draft_key("fake-model", load_prompt(cfg.prompt), cfg)
    recs = assemble_oos(inputs, parsed, key, cfg, AS_OF, dev_questions=[q1])
    assert [r.sid for r in recs] == ["O-01-duong_sat-1", "O-01-nuoc_ngoai-1", "O-02-nuoc_ngoai-1"]
    assert "gan_trung_dev_oos" in recs[0].flags
    assert any(f.startswith("qua_ngan") for f in recs[1].flags)
    assert "gan_trung" in recs[2].flags
    it = QAItem.model_validate(recs[0].item)
    assert it.question_type == "ngoai_pham_vi" and it.tier is None and not it.gold_units
