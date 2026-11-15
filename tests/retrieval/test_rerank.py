"""M11: rerank với FakeReranker — điểm chunk = max cửa sổ, cache resume không chấm lại."""

from __future__ import annotations

from pathlib import Path

import pytest

from trafficlaw.retrieval.config import RerankerSpec
from trafficlaw.retrieval.rerank import (
    FakeReranker,
    MissingRerankScoresError,
    RerankCache,
    pair_windows,
    rerank_scores,
)

SPEC = RerankerSpec(hf_repo="x/y", revision="abc", max_length=16, batch_size=4)
LONG = "\n".join(
    [
        "Điều 6. Xử phạt người điều khiển xe ô tô",
        "1. Phạt tiền đối với người điều khiển xe thực hiện một trong các hành vi sau đây:",
        "a) không chấp hành hiệu lệnh của đèn tín hiệu giao thông",
        "b) dừng xe đỗ xe trên đường cao tốc không đúng nơi quy định",
        "c) chở người trên thùng xe trái quy định",
    ]
)


def test_windows_count_question() -> None:
    rr = FakeReranker()
    ws = pair_windows("c1", "đèn tín hiệu", LONG, rr.count_tokens, 40)
    assert len(ws) > 1
    nq = rr.count_tokens("đèn tín hiệu")
    for w in ws:
        assert w.text.startswith(LONG.split("\n")[0] + "\n" + LONG.split("\n")[1])
        assert w.n_tokens == nq + rr.count_tokens(w.text)


def test_score_is_max_window(tmp_path: Path) -> None:
    rr = FakeReranker()
    spec = SPEC.model_copy(update={"max_length": 40})
    q = "không chấp hành hiệu lệnh đèn tín hiệu"
    scores, st = rerank_scores(rr, RerankCache(tmp_path), "fake", spec, q, [("c1", LONG)])
    ws = pair_windows("c1", q, LONG, rr.count_tokens, 40)
    per = rr.score([(q, w.text) for w in ws])
    assert scores["c1"] == max(per)
    assert st.n_windows == len(ws) > 1 and st.n_cached == 0


def test_cache_resume(tmp_path: Path) -> None:
    rr = FakeReranker()
    chunks = [("c1", LONG), ("c2", "Điều 7. Khác\nnội dung ngắn")]
    q = "dừng xe trên đường cao tốc"
    s1, _ = rerank_scores(rr, RerankCache(tmp_path), "fake", SPEC, q, chunks)
    n = rr.n_pairs
    # Mở lại cache (như lần chạy sau): không chấm lại, kết quả y hệt.
    s2, st = rerank_scores(rr, RerankCache(tmp_path), "fake", SPEC, q, chunks)
    assert s1 == s2 and rr.n_pairs == n and st.n_cached == 2
    # Local không có model: đọc được cặp đã chấm, cặp mới → lỗi rõ ràng.
    s3, _ = rerank_scores(None, RerankCache(tmp_path), "fake", SPEC, q, chunks)
    assert s3 == s1
    with pytest.raises(MissingRerankScoresError):
        rerank_scores(None, RerankCache(tmp_path), "fake", SPEC, "câu khác", chunks)


def test_cache_key_has_revision(tmp_path: Path) -> None:
    rr = FakeReranker()
    q = "dừng xe"
    rerank_scores(rr, RerankCache(tmp_path), "fake", SPEC, q, [("c1", LONG)])
    other = SPEC.model_copy(update={"revision": "def"})
    with pytest.raises(MissingRerankScoresError):
        rerank_scores(None, RerankCache(tmp_path), "fake", other, q, [("c1", LONG)])


def test_window_reuse_and_truncated_tail(tmp_path: Path) -> None:
    rr = FakeReranker()
    cache = RerankCache(tmp_path)
    q = "dừng xe"
    rerank_scores(rr, cache, "fake", SPEC, q, [("c1", LONG)])
    n = rr.n_pairs
    # Chunk khác id nhưng cùng text → cùng khoá cặp, không chấm lại.
    rerank_scores(rr, cache, "fake", SPEC, q, [("c9", LONG)])
    assert rr.n_pairs == n
    # Dòng cuối ghi dở bị bỏ khi mở lại.
    with cache.path.open("a", encoding="utf-8") as f:
        f.write('{"pair": "x", "sco')
    assert len(RerankCache(tmp_path)) == len(cache)
