"""answer() end-to-end với FakeClient (G, B3, B0, A2): ok, sửa số, JSON lỗi → format_error,
500 → error; G/B3 không bao giờ trả số ngoài bảng con số; resume; round-trip JSON; cache demo."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest

from tests.retrieval.conftest import make_ctx
from trafficlaw.llm.client import LLMClient
from trafficlaw.llm.providers.fake import FakeClient, bad_json, ok, server_error
from trafficlaw.llm.retry import RetryPolicy
from trafficlaw.pipeline.answer import (
    AnswerConfig,
    AnswerContext,
    AnswerResult,
    answer,
    load_answer_config,
    prepare,
)
from trafficlaw.pipeline.context import pick_graph_extras, select_sources
from trafficlaw.pipeline.runner import AnswerCache, Query, answer_cached, run_answers
from trafficlaw.retrieval.retrieve import PoolItem, SourceInfo
from trafficlaw.verify.numbers import find_unverified_numbers

ROOT = Path(__file__).resolve().parents[2]
Q = (
    "Người điều khiển xe ô tô chạy quá tốc độ quy định từ 05 km/h đến dưới 10 km/h bị phạt"
    " bao nhiêu?"
)
D = date(2026, 1, 1)
K3 = "ND168-2024/D6/K3"


@pytest.fixture(scope="module")
def rctx(tmp_path_factory, cfg, mini_store, mini_catalog, tables):
    return make_ctx(tmp_path_factory.mktemp("rctx"), cfg, mini_store, mini_catalog, tables)


@pytest.fixture(scope="module")
def acfg() -> AnswerConfig:
    return load_answer_config(ROOT / "configs/answer.yaml")


def _client(steps=None, responder=None) -> tuple[LLMClient, FakeClient]:
    fake = FakeClient(steps, responder=responder, model_id="qwen3-14b-awq")
    return LLMClient(fake, retry=RetryPolicy(max_retries=0, sleep=lambda s: None)), fake


def _actx(acfg, rctx, mini_store, mini_catalog, client) -> AnswerContext:
    return AnswerContext(
        acfg,
        store=mini_store,
        catalog=mini_catalog,
        retrieval=rctx,
        client=client,
        today=date(2026, 11, 3),
        run_id="test",
        data_version="test",
    )


def _ids(prep):
    sid = next(s.sid for s in prep.sources if s.unit_id == K3)
    fine = next(f.id for f in prep.table if f.source == sid and f.kind == "phat_tien")
    return sid, fine


def _assert_only_table_numbers(res: AnswerResult, allowed) -> None:
    text = res.answer
    for n in res.numbers:
        text = text.replace(n.rendered, " ")
    for c in res.citations:
        text = text.replace(c.label or "", " ")
    assert find_unverified_numbers(text, allowed) == [], text


def test_prepare_g_sources_and_table(acfg, rctx, mini_store, mini_catalog) -> None:
    actx = _actx(acfg, rctx, mini_store, mini_catalog, None)
    prep = prepare(Q, D, "G", actx)
    assert prep.retrieval is not None and prep.retrieval.analysis.question_type == "muc_phat"
    sids = [s.sid for s in prep.sources]
    assert sids == [f"S{i}" for i in range(1, len(sids) + 1)]
    assert [s.origin for s in prep.sources[:5]] == ["top"] * min(5, len(sids))
    assert sum(s.origin == "graph" for s in prep.sources) <= 3
    assert all(s.in_effect for s in prep.sources)
    msg = prep.messages[0]["content"]
    assert "Ngày áp dụng: 01/01/2026" in msg and Q in msg
    sid, fine = _ids(prep)
    assert f"{{{fine}}} [{sid}] Phạt tiền: từ 800.000 đồng đến 1.000.000 đồng" in msg


def test_graph_extras_priority(acfg, rctx, mini_store, mini_catalog) -> None:
    r = rctx.retrieve(Q, D, "G")
    top = [h.chunk_id for h in r.hits]
    live = [c.chunk_id for c in mini_catalog.chunks if c.covers(D) and c.chunk_id not in top]
    seed = top[0]

    def item(cid: str, et: str, score: float, s: str = seed) -> PoolItem:
        ch = mini_catalog.get(cid)
        return PoolItem(
            chunk_id=cid,
            unit_id=ch.unit_id,
            effective_from=ch.effective_from,
            effective_to=ch.effective_to,
            sources=[SourceInfo(source="graph", edge_type=et, hop=1, seed=s)],
            rerank_score=score,
        )

    pool = [
        item(live[0], "DAN_CHIEU", 9.0),
        item(live[1], "BI_XU_PHAT", 1.0),
        item(live[2], "BI_TRU_DIEM", 5.0),
        item(live[3], "BI_XU_PHAT", 3.0),
        item(live[4], "BI_XU_PHAT", 8.0, s="khong-thuoc-top"),
    ]
    r2 = r.model_copy(update={"pool": pool})
    got = pick_graph_extras(r2, mini_catalog, mini_store, acfg.context)
    assert got == [(live[3], "BI_XU_PHAT"), (live[1], "BI_XU_PHAT"), (live[2], "BI_TRU_DIEM")]
    # loại câu không thuộc danh sách → không bổ sung
    an = r2.analysis.model_copy(update={"question_type": "dinh_nghia"})
    assert (
        pick_graph_extras(
            r2.model_copy(update={"analysis": an}), mini_catalog, mini_store, acfg.context
        )
        == []
    )
    # ngân sách nhỏ: nguồn top bị cắt theo dòng, nguồn đồ thị bị bỏ
    srcs = select_sources(r2, mini_catalog, mini_store, acfg.context, docs={}, budget=400)
    assert all(s.origin == "top" for s in srcs)
    assert any(s.truncated for s in srcs) or len(srcs) < len(r2.hits)


def test_amendment_note(acfg, rctx, mini_store, mini_catalog) -> None:
    from trafficlaw.pipeline.context import amendment_notes

    units = ["ND168-2024/D6/K3/h", "ND168-2024/D6/K3/m"]
    assert amendment_notes(mini_store, units, date(2026, 7, 1), {}) == []
    notes = amendment_notes(
        mini_store, units, date(2026, 8, 15), {"ND238-2026": {"so_hieu": "238/2026/NĐ-CP"}}
    )
    assert {n.so_hieu for n in notes} == {"238/2026/NĐ-CP"}
    assert {n.effective_from for n in notes} == {date(2026, 8, 15)}


def _good_json(sid: str, fine: str) -> str:
    return json.dumps(
        {
            "status": "answered",
            "points": [
                {
                    "text": "Chạy quá tốc độ từ 05 km/h đến dưới 10 km/h bị phạt tiền {"
                    + fine
                    + "}.",
                    "sources": [f"{sid}/a"],
                    "numbers": [fine],
                }
            ],
            "conclusion": "Mức phạt theo khoản 3 Điều 6 Nghị định 168/2024/NĐ-CP.",
        },
        ensure_ascii=False,
    )


@pytest.mark.parametrize("config", ["G", "B3"])
def test_answer_ok(acfg, rctx, mini_store, mini_catalog, config: str) -> None:
    actx0 = _actx(acfg, rctx, mini_store, mini_catalog, None)
    prep = prepare(Q, D, config, actx0)
    sid, fine = _ids(prep)
    client, fake = _client([ok(_good_json(sid, fine))])
    actx = _actx(acfg, rctx, mini_store, mini_catalog, client)
    res = answer(Q, D, config, actx, qid="q1")
    assert res.status == "ok" and res.answer_status == "answered"
    assert "bị phạt tiền từ 800.000 đồng đến 1.000.000 đồng" in res.answer
    assert "[điểm a khoản 3 Điều 6 Nghị định 168/2024/NĐ-CP]" in res.answer
    assert [c.unit_id for c in res.citations] == [f"{K3}/a"]
    assert [(n.id, n.node_id) for n in res.numbers] == [(fine, "CHETAI:ND168-2024/D6/K3@v0#0")]
    assert res.verify.flags == [] and res.verify.n_violations_before == 0
    assert not res.verify.repaired and res.n_llm_calls == 1 and fake.n_calls == 1
    assert res.validity_filter is True and res.retrieval is not None
    _assert_only_table_numbers(res, prep.allowed)
    # round-trip JSON
    back = AnswerResult.model_validate_json(res.model_dump_json())
    assert back == res


def test_number_repair_success(acfg, rctx, mini_store, mini_catalog) -> None:
    prep = prepare(Q, D, "G", _actx(acfg, rctx, mini_store, mini_catalog, None))
    sid, fine = _ids(prep)
    free = _good_json(sid, fine).replace("{" + fine + "}", "800.000 đồng")
    client, fake = _client([ok(free), ok(_good_json(sid, fine))])
    res = answer(Q, D, "G", _actx(acfg, rctx, mini_store, mini_catalog, client), qid="q2")
    assert res.verify.repaired and res.verify.repair_status == "ok"
    assert res.verify.n_violations_before == 1 and res.verify.n_violations_after_repair == 0
    assert res.n_llm_calls == 2 and fake.n_calls == 2
    assert "«800.000»" in fake.requests[1].messages[-1].content
    assert res.verify.flags == []
    assert "từ 800.000 đồng đến 1.000.000 đồng" in res.answer


def test_number_repair_fails_drops_sentence(acfg, rctx, mini_store, mini_catalog) -> None:
    prep = prepare(Q, D, "G", _actx(acfg, rctx, mini_store, mini_catalog, None))
    sid, fine = _ids(prep)
    body = {
        "status": "answered",
        "points": [
            {"text": "Bị phạt 900.000 đồng. Còn bị trừ hai điểm.", "sources": [sid], "numbers": []},
            {
                "text": "Hành vi bị xử phạt {" + fine + "}. Tước 03 tháng.",
                "sources": [sid],
                "numbers": [fine],
            },
            {"text": "Mã lạ {N999}.", "sources": [sid], "numbers": []},
            {"text": "Không có nguồn hợp lệ.", "sources": ["S99"], "numbers": []},
        ],
        "conclusion": "Tổng cộng 2.000.000 đồng.",
    }
    bad = json.dumps(body, ensure_ascii=False)
    client, _ = _client([ok(bad)])  # lượt sửa trả y hệt
    res = answer(Q, D, "G", _actx(acfg, rctx, mini_store, mini_catalog, client), qid="q3")
    v = res.verify
    assert v.repaired and v.n_violations_before == v.n_violations_after_repair == 5
    assert {
        "so_khong_kiem_duoc",
        "y_rong_sau_loc_so",
        "y_khong_nguon",
        "nguon_ngoai_ngu_canh",
    } <= set(v.flags)
    # "hai điểm" là số viết bằng chữ → cũng bị bỏ; ý 0 và ý 2 rỗng sau lọc
    assert [p.text for p in res.points] == [
        "Hành vi bị xử phạt từ 800.000 đồng đến 1.000.000 đồng."
    ]
    assert v.dropped_sentences == 5 and v.n_points_kept == 1
    assert "2.000.000" not in res.answer and "900.000" not in res.answer and "03" not in res.answer
    _assert_only_table_numbers(res, prep.allowed)


def test_number_from_uncited_source_flagged(acfg, rctx, mini_store, mini_catalog) -> None:
    prep = prepare(Q, D, "G", _actx(acfg, rctx, mini_store, mini_catalog, None))
    sid, fine = _ids(prep)
    other = next(s.sid for s in prep.sources if s.sid != sid)
    js = _good_json(sid, fine).replace(f'"{sid}/a"', f'"{other}"')
    client, _ = _client([ok(js)])
    res = answer(Q, D, "G", _actx(acfg, rctx, mini_store, mini_catalog, client))
    assert "so_khong_thuoc_nguon_trich" in res.verify.flags


def test_format_error_and_error(acfg, rctx, mini_store, mini_catalog) -> None:
    client, fake = _client([bad_json(), bad_json()])
    res = answer(Q, D, "G", _actx(acfg, rctx, mini_store, mini_catalog, client), qid="q4")
    assert res.status == "format_error" and fake.n_calls == 2 and res.answer == ""
    client, _ = _client([server_error()])
    res = answer(Q, D, "G", _actx(acfg, rctx, mini_store, mini_catalog, client), qid="q5")
    assert res.status == "error" and res.error and res.answer_status is None


def test_a2_marks_no_filter(acfg, rctx, mini_store, mini_catalog) -> None:
    js = json.dumps({"status": "insufficient", "points": [], "conclusion": "Không đủ nguồn."})
    client, _ = _client([ok(js)])
    res = answer(Q, D, "A2", _actx(acfg, rctx, mini_store, mini_catalog, client))
    assert res.validity_filter is False and res.retrieval.validity_filter is False
    assert res.answer_status == "insufficient" and res.answer == "Không đủ nguồn."


def test_b0_free_numbers_and_citations(acfg, rctx, mini_store, mini_catalog) -> None:
    body = {
        "status": "answered",
        "points": [
            {
                "text": "Bị phạt từ 800.000 đồng đến 1.000.000 đồng.",
                "citations": [
                    {"van_ban": "168/2024/NĐ-CP", "dieu": "6", "khoan": "3", "diem": "a"},
                    {"van_ban": "168/2024/NĐ-CP", "dieu": "999", "khoan": None, "diem": None},
                ],
            }
        ],
        "conclusion": "",
    }
    client, fake = _client([ok(json.dumps(body, ensure_ascii=False))])
    actx = _actx(acfg, rctx, mini_store, mini_catalog, client)
    res = answer(Q, D, "B0", actx, qid="q6")
    assert res.status == "ok" and res.retrieval is None and res.sources == []
    assert "CÁC NGUỒN" not in fake.requests[0].messages[0].content
    assert res.verify.numbers_verifiable is False and res.verify.n_free_numbers == 2
    assert [c.status for c in res.points[0].citations] == ["ok", "khong_ton_tai"]
    assert res.verify.n_citations == 2 and res.verify.n_citations_valid == 1
    assert "800.000 đồng" in res.answer
    assert actx.prompt_hash("B0") != actx.prompt_hash("G")


def test_resume_and_demo_cache(acfg, rctx, mini_store, mini_catalog, tmp_path) -> None:
    js = json.dumps({"status": "insufficient", "points": [], "conclusion": "Không đủ."})
    client, fake = _client([server_error(), ok(js)])
    actx = _actx(acfg, rctx, mini_store, mini_catalog, client)
    qs = [Query("a", Q, D), Query("b", "Xe gắn máy là gì?", D)]
    out = tmp_path / "answers.jsonl"
    st = run_answers(qs, "G", actx, out)
    assert st.n_written == 2 and st.statuses == {"error": 1, "ok": 1}
    n = fake.n_calls
    st2 = run_answers(qs, "G", actx, out)  # chỉ chạy lại câu lỗi
    assert st2.n_skipped == 1 and st2.n_written == 1 and fake.n_calls == n + 1
    st3 = run_answers(qs, "G", actx, out)
    assert st3.n_skipped == 2 and st3.n_written == 0 and fake.n_calls == n + 1
    # cache demo
    cache = AnswerCache(tmp_path / "demo.jsonl")
    r1, hit1 = answer_cached("  Xe gắn máy LÀ gì? ", D, "G", actx, cache)
    calls = fake.n_calls
    r2, hit2 = answer_cached(
        "xe gắn máy là gì?", D, "G", actx, AnswerCache(tmp_path / "demo.jsonl")
    )
    assert not hit1 and hit2 and fake.n_calls == calls and r2 == r1


def test_dan_chieu_extra_outgoing_only(acfg, rctx, mini_store, mini_catalog) -> None:
    r = rctx.retrieve(Q, D, "G")
    k16 = next(c for c in mini_catalog.chunks if c.unit_id == "ND168-2024/D6/K16" and c.covers(D))
    k3 = next(c for c in mini_catalog.chunks if c.unit_id == K3 and c.covers(D))

    def case(seed, cand):
        hit = r.hits[0].model_copy(update={"chunk_id": seed.chunk_id, "unit_id": seed.unit_id})
        item = PoolItem(
            chunk_id=cand.chunk_id,
            unit_id=cand.unit_id,
            effective_from=cand.effective_from,
            effective_to=cand.effective_to,
            sources=[SourceInfo(source="graph", edge_type="DAN_CHIEU", hop=1, seed=seed.chunk_id)],
            rerank_score=1.0,
        )
        rr = r.model_copy(update={"hits": [hit], "pool": [item]})
        return pick_graph_extras(rr, mini_catalog, mini_store, acfg.context)

    # khoản 16 (trừ điểm) dẫn chiếu tới điểm h, i khoản 3 → giữ
    assert case(k16, k3) == [(k3.chunk_id, "DAN_CHIEU")]
    # chiều vào (khoản 3 được khoản 16 dẫn chiếu) → bỏ
    assert case(k3, k16) == []
    off = acfg.context.model_copy(update={"dan_chieu_outgoing_only": False})
    hit = r.hits[0].model_copy(update={"chunk_id": k3.chunk_id, "unit_id": K3})
    item = PoolItem(
        chunk_id=k16.chunk_id,
        unit_id=k16.unit_id,
        effective_from=k16.effective_from,
        effective_to=k16.effective_to,
        sources=[SourceInfo(source="graph", edge_type="DAN_CHIEU", hop=1, seed=k3.chunk_id)],
    )
    rr = r.model_copy(update={"hits": [hit], "pool": [item]})
    assert pick_graph_extras(rr, mini_catalog, mini_store, off) == [(k16.chunk_id, "DAN_CHIEU")]


def test_compact_units() -> None:
    from trafficlaw.pipeline.context import compact_units

    got = compact_units(["ND168-2024/D6/K3/h", "ND168-2024/D6/K3/i", "ND168-2024/D6/K8"])
    assert got == "điểm h, i khoản 3 Điều 6; khoản 8 Điều 6"


def test_repeated_placeholder_flagged(acfg, rctx, mini_store, mini_catalog) -> None:
    prep = prepare(Q, D, "G", _actx(acfg, rctx, mini_store, mini_catalog, None))
    sid, fine = _ids(prep)
    js = _good_json(sid, fine).replace("{" + fine + "}", "từ {" + fine + "} đến {" + fine + "}")
    client, _ = _client([ok(js)])
    res = answer(Q, D, "G", _actx(acfg, rctx, mini_store, mini_catalog, client))
    assert "ma_so_lap" in res.verify.flags
