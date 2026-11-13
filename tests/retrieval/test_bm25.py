"""BM25 (M10): tách từ, điểm so với giá trị tính tay, lưu/nạp, tất định."""

from __future__ import annotations

import math
import unicodedata

import pytest

from trafficlaw.retrieval.bm25 import BM25Index, tokenize


def test_tokenize_nfc_lower_bigram() -> None:
    nfd = unicodedata.normalize("NFD", "Xe Ô tô, xe_máy 1,35 mét")
    assert tokenize(nfd, bigrams=False) == ["xe", "ô", "tô", "xe", "máy", "1", "35", "mét"]
    toks = tokenize(nfd)
    assert toks[:8] == ["xe", "ô", "tô", "xe", "máy", "1", "35", "mét"]
    assert toks[8:] == ["xe_ô", "ô_tô", "tô_xe", "xe_máy", "máy_1", "1_35", "35_mét"]
    # NFC và NFD cho cùng kết quả
    assert tokenize(nfd) == tokenize(unicodedata.normalize("NFC", nfd))


def test_tokenize_empty() -> None:
    assert tokenize("  ,;.  ") == []
    assert tokenize("đ") == ["đ"]


DOCS = [("d1", "a b a"), ("d2", "b c"), ("d3", "c c c d")]


def _hand(query_terms: list[str], doc: list[str], dfs: dict[str, int], n: int, avgdl: float):
    k1, b = 1.5, 0.75
    s = 0.0
    for t in set(query_terms):
        qtf = query_terms.count(t)
        tf = doc.count(t)
        if tf == 0 or t not in dfs:
            continue
        idf = math.log(1 + (n - dfs[t] + 0.5) / (dfs[t] + 0.5))
        s += qtf * idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * len(doc) / avgdl))
    return s


def test_score_matches_hand_computation() -> None:
    idx = BM25Index.build(DOCS, k1=1.5, b=0.75, bigrams=False)
    assert idx.avgdl == pytest.approx(3.0)
    dfs = {"a": 1, "b": 2, "c": 2, "d": 1}
    docs = {i: t.split() for i, (_, t) in enumerate(DOCS)}
    sc = idx.scores("a c")
    assert set(sc) == {0, 1, 2}
    for i, s in sc.items():
        assert s == pytest.approx(_hand(["a", "c"], docs[i], dfs, 3, 3.0))
    # giá trị số cụ thể (tính tay): d1 có "a" tf=2, |d|=3 = avgdl ⇒ idf(a)·2·2.5/3.5
    idf_a = math.log(1 + 2.5 / 1.5)
    assert sc[0] == pytest.approx(idf_a * 2 * 2.5 / 3.5)
    # câu hỏi lặp term ⇒ nhân qtf
    assert idx.scores("a a")[0] == pytest.approx(2 * sc[0])


def test_search_order_ties_and_allowed() -> None:
    idx = BM25Index.build([("z", "x y"), ("a", "x y"), ("m", "q")], bigrams=False)
    hits = idx.search("x", 5)
    assert [h.chunk_id for h in hits] == ["a", "z"]  # đồng điểm → chunk_id
    assert [h.rank for h in hits] == [1, 2]
    assert hits[0].source == "bm25"
    assert [h.chunk_id for h in idx.search("x", 5, allowed={"z", "m"})] == ["z"]
    assert idx.search("không có", 5) == []


def test_save_load_roundtrip(tmp_path) -> None:
    idx = BM25Index.build([(f"c{i}", t) for i, t in enumerate(["xe ô tô", "xe mô tô", "ô tô"])])
    p = tmp_path / "bm25" / "index.json.gz"
    idx.save(p)
    b1 = p.read_bytes()
    back = BM25Index.load(p)
    assert back.params() == idx.params()
    for q in ["xe ô tô", "mô tô", "tô"]:
        assert back.search(q, 3) == idx.search(q, 3)
    idx.save(p)  # byte tất định
    assert p.read_bytes() == b1
