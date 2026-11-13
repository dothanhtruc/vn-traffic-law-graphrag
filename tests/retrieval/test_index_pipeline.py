"""Manifest + resume (M10): hash đổi → dựng lại; cache vector không encode lại; FAISS kiểm khớp."""

from __future__ import annotations

from pathlib import Path

import pytest

from trafficlaw.graph.embedded import EmbeddedStore
from trafficlaw.retrieval.catalog import ChunkCatalog
from trafficlaw.retrieval.config import EmbedModelSpec, RetrievalConfig
from trafficlaw.retrieval.dense import HashEmbedder
from trafficlaw.retrieval.index_pipeline import (
    IndexPaths,
    MissingVectorsError,
    finalize_manifest,
    query_vectors,
    read_manifest,
    step_bm25,
    step_catalog,
    step_encode,
    step_faiss,
)

MINI = Path(__file__).resolve().parents[1] / "fixtures/mini_graph"
INPUTS = {"data_version": "dv1", "graph_data_hash": "gh1"}


@pytest.fixture(scope="module")
def mini() -> EmbeddedStore:
    return EmbeddedStore.from_dir(MINI)


def _cfg(**kw) -> RetrievalConfig:
    return RetrievalConfig(
        models={"fake": EmbedModelSpec(hf_repo="fake/emb", revision="r1", max_seq_length=64)},
        candidates=["fake"],
        **kw,
    )


def test_catalog_and_bm25_rebuild_on_hash_change(mini, tmp_path) -> None:
    paths = IndexPaths(tmp_path / "index")
    cfg = _cfg()
    calls = []

    def factory():
        calls.append(1)
        return mini

    man: dict = {}
    cat, rebuilt = step_catalog(factory, cfg, paths, INPUTS, man)
    assert rebuilt and len(calls) == 1 and len(cat) == 32
    _, rb = step_bm25(cat, cfg, paths, man)
    assert rb
    finalize_manifest(paths, man, git_commit="abc")
    m = read_manifest(paths)
    assert m["n_chunks"] == 32 and m["data_version"] == "dv1" and m["git_commit"] == "abc"
    assert m["catalog"]["by_kind_tier"] == {"khoan": {"A": 32}}

    # cùng đầu vào → không dựng lại
    man2 = read_manifest(paths)
    cat2, rebuilt2 = step_catalog(factory, cfg, paths, INPUTS, man2)
    assert not rebuilt2 and len(calls) == 1 and len(cat2) == 32
    assert step_bm25(cat2, cfg, paths, man2)[1] is False
    # tham số BM25 đổi → dựng lại BM25
    cfg_b = _cfg(bm25={"k1": 1.2, "b": 0.75, "bigrams": True})
    assert step_bm25(cat2, cfg_b, paths, man2)[1] is True
    # data_version đổi → dựng lại danh mục
    _, r3 = step_catalog(factory, cfg, paths, {**INPUTS, "data_version": "dv2"}, man2)
    assert r3 and len(calls) == 2
    # cấu hình chunk đổi → dựng lại
    _, r4 = step_catalog(factory, _cfg(phu_luc_max_chars=900), paths, INPUTS, man2)
    assert r4
    # --force
    _, r5 = step_catalog(factory, _cfg(phu_luc_max_chars=900), paths, INPUTS, man2, force=True)
    assert r5
    # chunks.jsonl bị sửa tay → hash lệch → dựng lại
    paths.chunks.write_text(paths.chunks.read_text("utf-8") + "\n", encoding="utf-8")
    _, r6 = step_catalog(factory, _cfg(phu_luc_max_chars=900), paths, INPUTS, man2)
    assert r6


def test_encode_resume_and_faiss(mini, tmp_path) -> None:
    paths = IndexPaths(tmp_path / "index")
    cfg = _cfg()
    man: dict = {}
    cat, _ = step_catalog(lambda: mini, cfg, paths, INPUTS, man)
    with pytest.raises(MissingVectorsError):
        step_faiss("fake", cat, cfg, paths, man)

    e = HashEmbedder(32)
    qs = ["mức phạt khi chở trẻ em", "giấy phép lái xe"]
    rec = step_encode(e, "fake", cat, qs, cfg, paths)
    assert rec["windows"]["n_chunks"] == 32
    assert rec["windows"]["n_windowed"] > 0  # max_seq_length 64 ⇒ có chunk tách cửa sổ
    assert rec["doc"]["n_encoded"] == rec["doc"]["n_texts"] > 0  # lần đầu: encode mọi text
    n_first = e.n_encoded
    # chạy lại: không encode lại gì
    e2 = HashEmbedder(32)
    rec2 = step_encode(e2, "fake", cat, qs, cfg, paths)
    assert e2.n_encoded == 0 and rec2["total"]["n_encoded"] == 0 and n_first > 0
    assert len(paths.runs("fake").read_text("utf-8").splitlines()) == 2

    idx, built = step_faiss("fake", cat, cfg, paths, man)
    assert built and idx.n_chunks == 32 and idx.dim == 32
    assert step_faiss("fake", cat, cfg, paths, man)[1] is False
    # đổi revision → dựng lại (và thiếu vector vì khoá cache đổi)
    cfg_r2 = RetrievalConfig(
        models={"fake": EmbedModelSpec(hf_repo="fake/emb", revision="r2", max_seq_length=64)}
    )
    with pytest.raises(MissingVectorsError):
        step_faiss("fake", cat, cfg_r2, paths, man)

    # tìm kiếm thật bằng vector câu hỏi trong cache
    qv = query_vectors(paths, "fake", cfg, qs)
    hits = idx.search(qv, 5, allowed=cat.ids_at(__import__("datetime").date(2026, 11, 3)))
    assert len(hits) == 2 and all(len(h) == 5 for h in hits)
    with pytest.raises(MissingVectorsError):
        query_vectors(paths, "fake", cfg, ["câu chưa encode"])

    # danh mục đổi text → cửa sổ lệch → phải encode lại
    changed = ChunkCatalog(
        [c.model_copy(update={"text": c.text + " sửa"}) if i == 0 else c
         for i, c in enumerate(cat.chunks)]
    )  # fmt: skip
    with pytest.raises(MissingVectorsError):
        step_faiss("fake", changed, cfg, paths, man, force=True)
