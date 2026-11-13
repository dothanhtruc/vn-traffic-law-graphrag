"""Vector (M10): embedder giả tất định, cửa sổ theo dòng, FAISS (max theo chunk), cache vector."""

from __future__ import annotations

import numpy as np
import pytest

from trafficlaw.retrieval.catalog import Hit
from trafficlaw.retrieval.config import EmbedModelSpec
from trafficlaw.retrieval.dense import (
    FaissIndex,
    HashEmbedder,
    VectorCache,
    cache_key,
    encode_cached,
    split_windows,
)
from trafficlaw.retrieval.fusion import rrf

SPEC = EmbedModelSpec(hf_repo="fake/emb", revision="abc", max_seq_length=12)


def test_hash_embedder_deterministic() -> None:
    e = HashEmbedder(32)
    a = e.encode(["xe ô tô", "xe mô tô", ""])
    b = HashEmbedder(32).encode(["xe ô tô", "xe mô tô", ""])
    assert a.dtype == np.float32 and a.shape == (3, 32)
    assert np.array_equal(a, b)
    assert np.allclose(np.linalg.norm(a, axis=1), 1.0)
    assert e.count_tokens("xe ô tô") == 5


def test_split_windows_by_line() -> None:
    e = HashEmbedder()
    text = "Điều 6. Xử phạt\n1. Phạt tiền đối với:\na) một hai ba\nb) bốn năm sáu\nc) bảy tám"
    # vừa giới hạn → nguyên văn, k = 0
    w = split_windows("c", text, e.count_tokens, 100)
    assert len(w) == 1 and w[0].text == text and not w[0].truncated
    # giới hạn 15 token: phần đầu = 2 dòng đầu (8 âm tiết + 2), mỗi Điểm 4–5 âm tiết
    ws = split_windows("c", text, e.count_tokens, 15)
    assert [x.k for x in ws] == list(range(len(ws)))
    assert len(ws) == 3
    for x in ws:
        assert x.text.startswith("Điều 6. Xử phạt\n1. Phạt tiền đối với:\n")
        assert x.n_tokens <= 15 and not x.truncated
    body = [ln for x in ws for ln in x.text.split("\n")[2:]]
    assert body == text.split("\n")[2:]
    # một dòng quá dài → cửa sổ riêng, đánh dấu còn bị cắt
    long = "Điều 1. T\n1. dẫn\n" + "x " * 30
    ws2 = split_windows("d", long, e.count_tokens, 10)
    assert len(ws2) == 1 and ws2[0].truncated


def test_faiss_search_max_over_windows_and_allowed(tmp_path) -> None:
    e = HashEmbedder(64)
    rows = [("A", 0), ("A", 1), ("B", 0), ("C", 0)]
    texts = ["đèn đỏ vượt", "nồng độ cồn", "mũ bảo hiểm", "tốc độ tối đa"]
    idx = FaissIndex.build(e.encode(texts), rows, "dense:fake")
    q = e.encode(["nồng độ cồn", "mũ bảo hiểm"])
    hits = idx.search(q, 3)
    assert hits[0][0].chunk_id == "A"  # cửa sổ thứ hai của A khớp ⇒ điểm A = max
    assert hits[0][0].score == pytest.approx(1.0, abs=1e-5)
    assert len({h.chunk_id for h in hits[0]}) == len(hits[0])  # mỗi chunk một lần
    assert hits[1][0].chunk_id == "B"
    # allowed chung và theo câu
    assert all(h.chunk_id != "A" for h in idx.search(q, 3, allowed={"B", "C"})[0])
    per = idx.search(q, 3, allowed=[{"C"}, None])
    assert [h.chunk_id for h in per[0]] == ["C"] and per[1][0].chunk_id == "B"
    # lưu / nạp
    idx.save(tmp_path / "f", meta={"x": 1})
    back = FaissIndex.load(tmp_path / "f")
    assert back.rows == rows and back.dim == 64 and back.n_chunks == 3
    assert back.search(q, 3) == hits


def test_vector_cache_resume(tmp_path) -> None:
    e = HashEmbedder(16)
    cache = VectorCache(tmp_path / "v")
    texts = ["một", "hai", "một", "ba"]
    v1, st1 = encode_cached(e, cache, "fake", SPEC, "doc", texts, flush_every=2)
    assert st1.n_texts == 3 and st1.n_encoded == 3 and st1.n_cached == 0
    assert np.array_equal(v1[0], v1[2])
    assert len(list((tmp_path / "v").glob("part-*.npz"))) == 2  # flush mỗi 2 text
    # mở lại (như sau khi bị ngắt): không encode lại
    e2 = HashEmbedder(16)
    cache2 = VectorCache(tmp_path / "v")
    v2, st2 = encode_cached(e2, cache2, "fake", SPEC, "doc", texts + ["bốn"])
    assert st2.n_encoded == 1 and e2.n_encoded == 1
    assert np.array_equal(v2[:4], v1)
    # khoá phụ thuộc prompt + revision
    qp = SPEC.model_copy(update={"query_prompt": "Query: "})
    assert cache_key("fake", qp, "doc", "một") != cache_key("fake", qp, "query", "một")
    other = SPEC.model_copy(update={"revision": "def"})
    assert cache_key("fake", SPEC, "doc", "một") != cache_key("fake", other, "doc", "một")


def test_vector_cache_skips_broken_shard(tmp_path) -> None:
    d = tmp_path / "v"
    cache = VectorCache(d)
    encode_cached(HashEmbedder(8), cache, "fake", SPEC, "doc", ["a", "b"])
    (d / "part-00001.npz").write_bytes(b"hong")
    again = VectorCache(d)
    assert len(again) == 2


def test_rrf_hand() -> None:
    a = [Hit("x", 0, 1, "a"), Hit("y", 0, 2, "a")]
    b = [Hit("y", 0, 1, "b"), Hit("z", 0, 2, "b")]
    got = rrf([a, b], k=60, top_k=3)
    assert [h.chunk_id for h in got] == ["y", "x", "z"]
    assert got[0].score == pytest.approx(1 / 62 + 1 / 61)
    assert got[1].score == pytest.approx(1 / 61) and got[2].score == pytest.approx(1 / 62)
    assert [h.rank for h in got] == [1, 2, 3]
