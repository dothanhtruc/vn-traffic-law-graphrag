"""Smoke M13 (``scripts.eval smoke --fake``, CI): chạy đủ ba giai đoạn trên ~20 câu giả
(``tests/fixtures/eval/smoke_test.jsonl``) với ``mini_graph`` + model giả — không GPU, không mạng.

- Truy hồi: danh mục chunk dựng từ ``mini_graph`` (+ nút ngữ nghĩa M8), ``HashEmbedder`` (vector
  câu hỏi/chunk tính tại chỗ), ``FakeReranker``, analyzer chỉ dùng rule.
- LLM sinh câu trả lời và judge: ``FakeClient`` với hàm phản hồi tất định (trích ``S1``, dùng mã
  ``N1`` nếu có; câu hỏi chứa từ khoá ngoài phạm vi → ``out_of_scope``; judge cho điểm theo băm).
- Tập con dựng lại tại chỗ bằng ``qa_subsets.build_subsets`` (cỡ nhỏ).
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import tempfile
import time
from datetime import date
from pathlib import Path
from typing import Any

from trafficlaw.eval.eval_config import EvalConfig
from trafficlaw.eval.judge import JudgeContext
from trafficlaw.eval.orchestrate import (
    export_judge_check,
    score_all,
    stage_generate,
    stage_judge,
    stage_retrieve,
)
from trafficlaw.eval.qa_schema import QAItem
from trafficlaw.eval.qa_subsets import SubsetSpec, build_subsets, file_sha256
from trafficlaw.eval.runner import load_eval_data
from trafficlaw.graph.embedded import EmbeddedStore
from trafficlaw.llm.client import LLMClient
from trafficlaw.llm.prompt_loader import load_prompt
from trafficlaw.llm.providers.fake import FakeClient
from trafficlaw.llm.retry import RetryPolicy
from trafficlaw.llm.types import LLMRequest
from trafficlaw.pipeline.answer import AnswerConfig, AnswerContext
from trafficlaw.retrieval.analyze import Analyzer
from trafficlaw.retrieval.bm25 import BM25Index
from trafficlaw.retrieval.catalog import ChunkCatalog, build_catalog
from trafficlaw.retrieval.config import RetrievalConfig
from trafficlaw.retrieval.dense import (
    FaissIndex,
    HashEmbedder,
    VectorCache,
    chunk_windows,
    encode_cached,
)
from trafficlaw.retrieval.rerank import FakeReranker
from trafficlaw.retrieval.retrieve import QueryEncoder, RetrievalContext
from trafficlaw.retrieval.retrieve_env import load_analyzer_tables
from trafficlaw.utils.jsonl import read_jsonl

SMOKE_SUBSETS = {
    "ablation_200": SubsetSpec(10),
    "judge_200": SubsetSpec(12),
    "variance_100": SubsetSpec(6),
    "regression_100": SubsetSpec(8, ("ngoai_pham_vi",)),
}
OOS_MARKERS = ("phở", "tàu cá")


def copy_graph(graph_dir: Path, dst: Path) -> Path:
    dst.mkdir(parents=True, exist_ok=True)
    for f in [*graph_dir.glob("*.jsonl"), *(graph_dir / "semantic").glob("*.jsonl")]:
        shutil.copy(f, dst / f.name)
    return dst


def fake_retrieval_context(
    root: Path, rcfg: RetrievalConfig, store: EmbeddedStore, work: Path, today: date
) -> RetrievalContext:
    catalog = ChunkCatalog(build_catalog(store, phu_luc_max_chars=1500))
    key = rcfg.model_key
    assert key is not None
    spec = rcfg.spec(key)
    emb = HashEmbedder()
    ws = chunk_windows([(c.chunk_id, c.text) for c in catalog.chunks], spec, emb.count_tokens)
    vecs, _ = encode_cached(
        emb, VectorCache(work / "vectors" / key), key, spec, "doc", [w.text for w in ws]
    )
    fi = FaissIndex.build(vecs, [(w.chunk_id, w.k) for w in ws], f"dense:{key}")
    rr = FakeReranker()
    return RetrievalContext(
        rcfg,
        catalog=catalog,
        bm25=BM25Index.build([(c.chunk_id, c.text) for c in catalog.chunks]),
        store=store,
        analyzer=Analyzer(load_analyzer_tables(root, rcfg), today=today),
        faiss_loader=lambda k: fi,
        encoder=QueryEncoder(rcfg, lambda k: work / "vectors" / k, lambda k: emb),
        rerank_dir=lambda k: work / "rerank" / k,
        reranker_factory=lambda k: rr,
        meta={"data_version": "smoke", "catalog_sha256": "smoke", "graph_data_hash": "smoke"},
    )


def fake_answer_responder(req: LLMRequest) -> str:
    content = req.messages[-1].content if req.messages else ""
    first = req.messages[0].content if req.messages else ""
    if any(m in first for m in OOS_MARKERS):
        return json.dumps({"status": "out_of_scope", "points": [], "conclusion": "Ngoài phạm vi."})
    if "`van_ban`" in first:  # B0
        body = {
            "status": "answered",
            "points": [
                {
                    "text": "Theo quy định hiện hành.",
                    "citations": [
                        {"van_ban": "168/2024/NĐ-CP", "dieu": "6", "khoan": "3", "diem": "a"}
                    ],
                }
            ],
            "conclusion": "",
        }
        return json.dumps(body, ensure_ascii=False)
    sid = re.search(r"\bS(\d+)\b", first)
    num = re.search(r"\{(N\d+)\}", first)
    text = "Theo quy định của nguồn." + (f" Mức áp dụng: {{{num[1]}}}." if num else "")
    body = {
        "status": "answered" if sid else "insufficient",
        "points": [
            {
                "text": text,
                "sources": [f"S{sid[1]}"] if sid else [],
                "numbers": [num[1]] if num else [],
            }
        ]
        if sid
        else [],
        "conclusion": "",
    }
    del content
    return json.dumps(body, ensure_ascii=False)


def fake_judge_responder(req: LLMRequest) -> str:
    content = req.messages[0].content
    d = int(hashlib.sha256(content.encode("utf-8")).hexdigest(), 16) % 3
    return json.dumps(
        {"diem": d, "dung": d == 2, "thieu": [], "sai": [], "ly_do": "smoke"}, ensure_ascii=False
    )


def _client(responder: Any, model_id: str) -> LLMClient:
    return LLMClient(
        FakeClient(responder=responder, model_id=model_id),
        retry=RetryPolicy(max_retries=0, sleep=lambda s: None),
    )


def run_smoke(
    root: Path,
    ecfg: EvalConfig,
    rcfg: RetrievalConfig,
    acfg: AnswerConfig,
    out_dir: Path | None = None,
    *,
    workers: int = 4,
) -> dict[str, Any]:
    """Chạy cả ba giai đoạn hai lần (lần hai phải không gọi LLM — resume); trả summary."""
    t0 = time.perf_counter()
    work = Path(tempfile.mkdtemp(prefix="m13_smoke_"))
    run_dir = out_dir or (work / "results" / ecfg.smoke.run_id)
    run_dir.mkdir(parents=True, exist_ok=True)
    store = EmbeddedStore.from_dir(copy_graph(root / ecfg.smoke.graph_dir, work / "graph"))
    test_path = root / ecfg.smoke.test
    items = [QAItem.model_validate(r) for r in read_jsonl(test_path)]
    subsets_path = work / "subsets.json"
    subsets_path.write_text(
        json.dumps(build_subsets(items, file_sha256(test_path), SMOKE_SUBSETS), ensure_ascii=False),
        encoding="utf-8",
    )
    data = load_eval_data(test_path, subsets_path, store)
    rctx = fake_retrieval_context(root, rcfg, store, work, ecfg.today)
    ans_client = _client(fake_answer_responder, "fake-qwen")
    actx = AnswerContext(
        acfg,
        store=store,
        catalog=rctx.catalog,
        retrieval=rctx,
        client=ans_client,
        model_id="fake-qwen",
        today=ecfg.today,
        run_id=run_dir.name,
        data_version="smoke",
    )
    jctx = JudgeContext(
        client=_client(fake_judge_responder, "fake-mistral"),
        prompt=load_prompt(ecfg.judge.prompt),
        model_id="fake-mistral",
        run_id=run_dir.name,
        max_output_tokens=ecfg.judge.max_output_tokens,
    )
    calls: list[int] = []
    for _ in range(2):
        stage_retrieve(data, ecfg, rctx, run_dir, use_llm=False)
        stage_generate(data, ecfg, actx, run_dir, workers=workers)
        stage_judge(data, ecfg, jctx, run_dir, workers=workers)
        calls.append(ans_client.provider.n_calls + jctx.client.provider.n_calls)  # type: ignore[attr-defined]
    export_judge_check(data, ecfg, run_dir)
    summary = score_all(
        data,
        ecfg,
        rctx.catalog,
        run_dir,
        rctx.meta,
        judge_model=jctx.model_id,
        judge_prompt_hash=jctx.prompt_hash,
        judge_family="fake",
        extra={"smoke": True},
    )
    summary["smoke_seconds"] = round(time.perf_counter() - t0, 2)
    summary["smoke_llm_calls"] = calls
    summary["run_dir"] = str(run_dir)
    return summary


__all__ = ["fake_answer_responder", "fake_judge_responder", "fake_retrieval_context", "run_smoke"]
