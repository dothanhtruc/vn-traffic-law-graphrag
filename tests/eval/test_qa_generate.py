"""M9: chunk Khoản theo phiên bản, sinh câu hỏi train/val (FakeClient, resume), lọc, chia val
theo Điều, chống rò rỉ."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import date
from pathlib import Path

import pytest

from trafficlaw.eval.qa_generate import (
    GenChunk,
    GenerateConfig,
    build_splits,
    done_chunk_keys,
    filter_questions,
    is_val_dieu,
    pick_as_of,
    run_generate,
    run_key,
    select_chunks,
    unique_chunks,
)
from trafficlaw.eval.qa_schema import QAItem
from trafficlaw.graph.embedded import EmbeddedStore
from trafficlaw.llm import LLMClient, load_prompt
from trafficlaw.llm.providers.fake import FakeClient, quota_exhausted, server_error
from trafficlaw.llm.retry import RetryPolicy
from trafficlaw.llm.types import LLMRequest
from trafficlaw.retrieval.chunking import Chunk, iter_chunks
from trafficlaw.utils.jsonl import read_jsonl

MINI = Path(__file__).resolve().parents[1] / "fixtures/mini_graph"
D6 = "ND168-2024/D6"
CFG = GenerateConfig(model_id="fake-model")


@pytest.fixture(scope="module")
def store() -> EmbeddedStore:
    return EmbeddedStore.from_dir(MINI)


@pytest.fixture(scope="module")
def chunks(store: EmbeddedStore) -> list[GenChunk]:
    return select_chunks(store, ["ND168-2024"])


def client(responder=None, script=None) -> LLMClient:  # type: ignore[no-untyped-def]
    fake = FakeClient(script, responder=responder)
    return LLMClient(fake, retry=RetryPolicy(max_retries=0, sleep=lambda s: None))  # type: ignore[arg-type]


def responder(req: LLMRequest) -> str:
    """3 câu: câu 1 hợp lệ (duy nhất theo chunk, nhãn chữ từ hash), câu 2 có số bịa, câu 3 quá
    ngắn."""
    h = hashlib.sha1(req.messages[-1].content.encode()).hexdigest()[:10]
    tag = "".join("abcdeghikl"[int(c, 16) % 10] for c in h)
    return json.dumps(
        {
            "questions": [
                {
                    "question": f"Người lái xe ô tô gặp trường hợp {tag} thì bị xử lý thế nào?",
                    "question_type": "muc_phat",
                },
                {
                    "question": "Xe ô tô chở 99999 người bị phạt bao nhiêu tiền?",
                    "question_type": "muc_phat",
                },
                {"question": "Phạt sao?", "question_type": "khac"},
            ]
        },
        ensure_ascii=False,
    )


# --------------------------------------------------------------------------- chunk


def test_chunks_follow_versions(store: EmbeddedStore) -> None:
    cs = [c for c in iter_chunks(store, ["ND168-2024"]) if c.unit_id == f"{D6}/K3"]
    # K3: Điểm m có hiệu lực từ 01/01/2026, sửa 15/08/2026; Điểm h sửa 15/08/2026
    assert [(c.effective_from, c.effective_to) for c in cs] == [
        (date(2025, 1, 1), date(2025, 12, 31)),
        (date(2026, 1, 1), date(2026, 8, 14)),
        (date(2026, 8, 15), None),
    ]
    assert all(c.text.startswith("Điều 6.") for c in cs)
    assert "m) Chở trẻ em" not in cs[0].text and "m) Chở trẻ em" in cs[1].text
    assert cs[0].chunk_id == f"{D6}/K3#2025-01-01"
    assert f"{D6}/K3/m@v0" in cs[1].version_ids and f"{D6}/K3/m@v1" in cs[2].version_ids


def test_new_unit_chunk_starts_late(store: EmbeddedStore) -> None:
    cs = [c for c in iter_chunks(store, ["ND168-2024"]) if c.unit_id == f"{D6}/K1a"]
    assert [c.effective_from for c in cs] == [date(2026, 8, 15)]


def test_pick_as_of() -> None:
    def mk(f: date, t: date | None) -> Chunk:
        return Chunk("u#x", "u", "d", "A", "d/D1", "t", "x", f, t, ())

    cut = date(2026, 11, 3)
    assert pick_as_of(mk(date(2025, 1, 1), None), cut) == cut
    assert pick_as_of(mk(date(2025, 1, 1), date(2025, 8, 31)), cut) == date(2025, 8, 31)
    assert pick_as_of(mk(date(2028, 1, 1), None), cut) == date(2028, 1, 1)


# --------------------------------------------------------------------------- lọc


def test_filter_questions(chunks: list[GenChunk]) -> None:
    gc = next(c for c in chunks if c.chunk.unit_id == f"{D6}/K5")
    qs = [
        {
            "question": "1. Lái ô tô vượt đèn đỏ thì bị phạt bao nhiêu tiền?",
            "question_type": "muc_phat",
        },
        {
            "question": "Lái ô tô vượt đèn đỏ thì bị phạt bao nhiêu tiền?",
            "question_type": "muc_phat",
        },
        {"question": "What is the fine for running a red light?", "question_type": "muc_phat"},
        {"question": "Phạt bao nhiêu?", "question_type": "muc_phat"},
        {
            "question": "Mức phạt 4.000.000 đồng áp dụng cho hành vi nào?",
            "question_type": "muc_phat",
        },
        {
            "question": "Mức phạt 7.000.000 đồng áp dụng cho ai khi lái xe?",
            "question_type": "muc_phat",
        },
        {
            "question": "Khoản này quy định mức phạt bao nhiêu đối với ô tô?",
            "question_type": "muc_phat",
        },
        {
            "question": "Nghị định 168 phạt người lái ô tô chạy quá tốc độ bao nhiêu?",
            "question_type": "la",
        },
    ]
    keep, rej = filter_questions(gc, qs, CFG)
    reasons = [r.reason for r in rej]
    assert keep[0] == ("Lái ô tô vượt đèn đỏ thì bị phạt bao nhiêu tiền?", "muc_phat", 0)
    assert reasons == [
        "trung_trong_chunk",
        "khong_phai_tieng_viet",
        "qua_ngan",
        "so_khong_co_trong_unit",
        "tham_chieu_ngu_canh",
    ]
    # số hiệu văn bản (168) được phép; loại câu lạ → khac
    assert keep[-1][1] == "khac" and keep[-1][2] == 7


def test_filter_verbatim(chunks: list[GenChunk]) -> None:
    gc = next(c for c in chunks if c.chunk.unit_id == f"{D6}/K5")
    line = gc.chunk.text.split("\n")[1]
    words = re.sub(r"^\d+\.\s*", "", line).split()[:14]
    keep, rej = filter_questions(
        gc, [{"question": " ".join(words) + "?", "question_type": "khac"}], CFG
    )
    assert not keep and rej[0].reason == "chep_nguyen_van"


def test_val_split_by_dieu_deterministic() -> None:
    ids = [f"DOC/D{i}" for i in range(4000)]
    val = [d for d in ids if is_val_dieu(d, 42, 0.05)]
    assert 0.035 < len(val) / len(ids) < 0.065
    assert val == [d for d in ids if is_val_dieu(d, 42, 0.05)]
    assert val != [d for d in ids if is_val_dieu(d, 7, 0.05)]


# --------------------------------------------------------------------------- chạy + resume


def test_run_resume(tmp_path: Path, chunks: list[GenChunk]) -> None:
    raw = tmp_path / "raw.jsonl"
    c1 = client(responder=responder)
    out = run_generate(chunks, CFG, c1, raw, max_calls=5)
    assert out.n_called == 5 and out.by_status["ok"] == 5
    n_uniq = len(unique_chunks(chunks))
    out2 = run_generate(chunks, CFG, client(responder=responder), raw)
    assert out2.n_todo == n_uniq - 5 and out2.n_called == n_uniq - 5
    out3 = run_generate(chunks, CFG, client(responder=responder), raw)
    assert out3.n_called == 0
    key = run_key("fake-model", load_prompt(CFG.prompt), CFG)
    assert len(done_chunk_keys(raw, key)) == n_uniq
    # khoá chạy khác (n câu đổi ⇒ schema đổi) → chạy lại toàn bộ
    cfg2 = CFG.model_copy(update={"n_questions": 2})
    assert (
        run_generate(chunks, cfg2, client(responder=responder), raw, max_calls=0).n_todo == n_uniq
    )


def test_errors_rerun_format_error_kept(tmp_path: Path, chunks: list[GenChunk]) -> None:
    raw = tmp_path / "raw.jsonl"
    out = run_generate(chunks[:3], CFG, client(script=[server_error()]), raw)
    assert out.by_status["error"] == 3
    bad = client(responder=lambda r: "không phải JSON")
    out = run_generate(chunks[:3], CFG, bad, raw)
    assert out.by_status["format_error"] == 3  # error → chạy lại
    assert run_generate(chunks[:3], CFG, bad, raw).n_called == 0  # format_error giữ (tính là sai)
    out = run_generate(chunks[:3], CFG, client(responder=responder), raw, retry_format_error=True)
    assert out.by_status["ok"] == 3


def test_quota_stops_cleanly(tmp_path: Path, chunks: list[GenChunk]) -> None:
    raw = tmp_path / "raw.jsonl"
    out = run_generate(chunks[:4], CFG, client(script=[quota_exhausted()]), raw)
    assert out.stopped == "quota" and out.n_called == 0
    assert list(read_jsonl(raw)) == []


# --------------------------------------------------------------------------- dựng split


def test_build_splits(tmp_path: Path, store: EmbeddedStore, chunks: list[GenChunk]) -> None:
    raw = tmp_path / "raw.jsonl"
    run_generate(chunks, CFG, client(responder=responder), raw)
    key = run_key("fake-model", load_prompt(CFG.prompt), CFG)
    cfg = CFG.model_copy(update={"val_fraction": 0.5})
    res = build_splits(store, chunks, raw, key, cfg)
    n_uniq = len(unique_chunks(chunks))
    assert len(res.train) + len(res.val) == n_uniq  # mỗi chunk giữ đúng câu 1
    assert res.stats["rejected_by_reason"]["so_khong_co_trong_unit"] == n_uniq
    tr = {x.gold_units[0].split("/")[1] for x in res.train}
    va = {x.gold_units[0].split("/")[1] for x in res.val}
    assert res.val and not tr & va  # chia theo Điều
    x = res.train[0] if res.train else res.val[0]
    assert x.source == "llm:fake-model" and x.chunk_id and x.gold_versions
    assert x.as_of == pick_as_of(
        next(c.chunk for c in chunks if c.chunk.chunk_id == x.chunk_id), cfg.as_of_cutoff
    )
    # build lại cho cùng kết quả
    again = build_splits(store, chunks, raw, key, cfg)
    assert [i.qid for i in again.train] == [i.qid for i in res.train]

    # chống rò rỉ + đánh dấu unit thuộc gold test
    victim = (res.train or res.val)[0]
    test = [
        QAItem(
            qid="t1",
            question=victim.question,
            as_of=date(2026, 11, 3),
            question_type="muc_phat",
            tier="A",
            answer="x",
            gold_units=[f"{D6}/K5/a"],
        )
    ]
    res2 = build_splits(store, chunks, raw, key, cfg, test_items=test)
    assert victim.qid not in {i.qid for i in [*res2.train, *res2.val]}
    assert res2.stats["rejected_by_reason"]["gan_trung_test"] == 1
    flagged = {i.gold_units[0] for i in [*res2.train, *res2.val] if i.in_test_gold}
    assert f"{D6}/K5" in flagged and all(u.startswith(f"{D6}/K5") for u in flagged)
