"""M14: dữ liệu huấn luyện — loại câu trùng gold test/dev, cửa sổ, batch không trùng."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from trafficlaw.retrieval.catalog import ChunkCatalog
from trafficlaw.train.data import (
    StaleManifestError,
    WindowTable,
    best_window,
    build_examples,
    check_manifest,
    examples_sha256,
    file_sha256,
    filter_items,
    gold_units_of,
    no_dup_batches,
    plain_batches,
    training_plan,
)

from .conftest import item


def _items():
    return [
        item("q1", "Ô tô chạy quá tốc độ bị phạt bao nhiêu?", "VB/D1/K1#2025-01-01", "VB/D1/K1"),
        item("q2", "Mô tô vượt đèn đỏ bị phạt thế nào?", "VB/D1/K2#2026-01-01", "VB/D1/K2"),
        item("q3", "Người đi bộ qua đường sai quy định?", "VB/D1/K3#2025-01-01", "VB/D1/K3"),
        item("q4", "Giấy phép hạng B cấp cho xe nào?", "VB/D2/K1#2025-01-01", "VB/D2/K1"),
        item("q5", "Đỗ xe trên vỉa hè có bị phạt?", "VB/D3/K1#2025-01-01", "VB/D3/K1"),
        item("q6", "Câu không có chunk", "VB/D9/K1#2025-01-01", "VB/D9/K1"),
    ]


def test_filter_excludes_test_and_dev_gold(catalog: ChunkCatalog) -> None:
    # test gold = Điều 1 (tổ tiên của K1, K2, K3) ; dev gold = Điểm con của D2/K1 (con cháu).
    kept, st = filter_items(_items(), catalog, {"test": {"VB/D1"}, "dev": {"VB/D2/K1/a"}})
    assert [i.qid for i in kept] == ["q5"]
    assert st.n_total == 6 and st.n_no_chunk == 1 and st.n_excluded == 4
    assert st.to_dict()["excluded_by_set"] == {"dev": 1, "test": 3}


def test_filter_unrelated_kept(catalog: ChunkCatalog) -> None:
    kept, st = filter_items(_items()[:5], catalog, {"test": {"VB/D1/K4"}})
    assert len(kept) == 5 and st.n_excluded == 0


def test_check_manifest(tmp_path: Path) -> None:
    t = tmp_path / "test.jsonl"
    t.write_text('{"qid": "a"}\n', encoding="utf-8")
    m = tmp_path / "m.json"
    m.write_text(json.dumps({"test_sha256": file_sha256(t)}), encoding="utf-8")
    assert check_manifest(m, t) == file_sha256(t)
    t.write_text('{"qid": "b"}\n', encoding="utf-8")
    with pytest.raises(StaleManifestError):
        check_manifest(m, t)


def test_gold_units_of_reads_only_gold(tmp_path: Path) -> None:
    p = tmp_path / "x.jsonl"
    p.write_text(
        '{"qid": "1", "question": "?", "gold_units": ["A/D1"]}\n{"qid": "2", "gold_units": []}\n',
        encoding="utf-8",
    )
    assert gold_units_of(p) == {"A/D1"}


def test_best_window_and_table(catalog: ChunkCatalog) -> None:
    ws = ["Điều 1\n1. a\nxe đạp chở người", "Điều 1\n1. a\nđỗ xe vỉa hè"]
    assert best_window("đỗ xe trên vỉa hè", ws) == ws[1]
    assert best_window("không liên quan gì", ws) == ws[0]  # hoà → cửa sổ đầu
    tab = WindowTable(
        [
            {"chunk_id": "VB/D1/K1#2025-01-01", "k": 1, "text": ws[1]},
            {"chunk_id": "VB/D1/K1#2025-01-01", "k": 0, "text": ws[0]},
            {"chunk_id": "VB/D2/K1#2025-01-01", "k": 0, "text": "một cửa sổ"},
        ]
    )
    assert tab.windows("VB/D1/K1#2025-01-01") == ws
    assert tab.text_for("VB/D1/K1#2025-01-01", "vỉa hè", catalog) == ws[1]
    # một cửa sổ → text chunk nguyên vẹn
    assert (
        tab.text_for("VB/D2/K1#2025-01-01", "x", catalog) == catalog.get("VB/D2/K1#2025-01-01").text
    )


def _examples(catalog: ChunkCatalog, n_neg: int = 2):
    negs = {
        "q1": ["VB/D3/K1#2025-01-01", "VB/D2/K2#2025-01-01", "VB/D1/K4#2025-01-01"],
        "q3": ["VB/D1/K1#2025-01-01"],  # positive của q1 ⇒ không được chung batch với q1
        "q4": ["NOT/IN/CATALOG#x", "VB/D2/K2#2025-01-01"],
    }
    return build_examples(_items()[:5], catalog, WindowTable([]), negs, n_neg)


def test_build_examples(catalog: ChunkCatalog) -> None:
    ex = _examples(catalog)
    by = {e.qid: e for e in ex}
    assert by["q1"].neg_ids == ("VB/D3/K1#2025-01-01", "VB/D2/K2#2025-01-01")
    assert by["q4"].neg_ids == ("VB/D2/K2#2025-01-01",)  # chunk lạ bị bỏ
    assert by["q2"].neg_ids == () and by["q2"].pos_unit == "VB/D1/K2"
    assert by["q1"].pos_text == catalog.get("VB/D1/K1#2025-01-01").text
    assert examples_sha256(ex) == examples_sha256(_examples(catalog))
    assert examples_sha256(ex) != examples_sha256(_examples(catalog, n_neg=1))


def test_no_dup_batches(catalog: ChunkCatalog) -> None:
    ex = _examples(catalog)
    for epoch in range(4):
        bs = no_dup_batches(ex, 3, seed=42, epoch=epoch)
        flat = [i for b in bs for i in b]
        assert sorted(flat) == list(range(len(ex)))
        assert all(len(b) <= 3 for b in bs)
        for b in bs:
            ids = [c for i in b for c in (ex[i].pos_id, *ex[i].neg_ids)]
            units = [u for i in b for u in (ex[i].pos_unit, *ex[i].neg_units)]
            assert len(ids) == len(set(ids)) and len(units) == len(set(units))
        assert bs == no_dup_batches(ex, 3, seed=42, epoch=epoch)  # tất định
    # q1 và q3 xung đột (positive của q1 là negative của q3) ⇒ luôn khác batch.
    i1, i3 = [i for i, e in enumerate(ex) if e.qid in ("q1", "q3")]
    for b in no_dup_batches(ex, 5, seed=1, epoch=0):
        assert not (i1 in b and i3 in b)


def test_plain_batches_and_plan() -> None:
    b0 = plain_batches(10, 4, seed=42, epoch=0)
    assert [len(b) for b in b0] == [4, 4, 2]
    assert sorted(i for b in b0 for i in b) == list(range(10))
    assert b0 != plain_batches(10, 4, seed=42, epoch=1)
    plan = training_plan(lambda ep: plain_batches(10, 4, seed=42, epoch=ep), 2)
    assert [ep for ep, _ in plan] == [0, 0, 0, 1, 1, 1]
