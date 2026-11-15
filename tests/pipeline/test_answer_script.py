"""scripts.answer: tổng hợp chỉ số + render báo cáo từ AnswerResult (không gọi LLM)."""

from __future__ import annotations

import json
from datetime import date

from scripts.answer import render_md, summarize_rows
from tests.pipeline.test_answer import (  # noqa: F401
    K3,
    D,
    Q,
    _actx,
    _client,
    _good_json,
    _ids,
    acfg,
    rctx,
)
from trafficlaw.llm.providers.fake import bad_json, ok
from trafficlaw.pipeline.answer import answer, prepare


def test_summarize_rows(acfg, rctx, mini_store, mini_catalog) -> None:  # noqa: F811
    prep = prepare(Q, D, "G", _actx(acfg, rctx, mini_store, mini_catalog, None))
    sid, fine = _ids(prep)
    client, _ = _client([ok(_good_json(sid, fine)), bad_json(), bad_json()])
    actx = _actx(acfg, rctx, mini_store, mini_catalog, client)
    r1 = answer(Q, D, "G", actx, qid="a")
    r2 = answer("Câu khác về xe?", date(2026, 1, 1), "G", actx, qid="b")
    rep = summarize_rows([r1, r2], {"a": [f"{K3}/a"], "b": []})
    assert rep["status"] == {"ok": 1, "format_error": 1}
    assert rep["format_error_rate"] == 0.5
    assert rep["trich_gold"] == 1.0 and rep["trich_dan"]["hop_le"] == 1.0
    assert rep["con_so"]["cau_dung_ma_so"] == 1.0
    md = render_md(
        {"run_id": "t", "generated_at": "x", "gpu_seconds": 0, "sets": {"val": {"G": rep}}},
        examples=[r1],
    )
    assert "| G | 2 | 1 | 1 | 0 |" in md and "800.000 đồng" in md
    json.dumps(rep, ensure_ascii=False)
