import logging
from datetime import date
from pathlib import Path

import pytest
from pydantic import BaseModel

from trafficlaw.utils.jsonl import JsonlWriter, append_jsonl, done_keys, read_jsonl, write_jsonl

KEY = ["config_name", "question_id", "model_id", "prompt_hash"]


def _rec(qid: str, status: str = "ok", config: str = "G") -> dict:
    return {
        "config_name": config,
        "question_id": qid,
        "model_id": "gemini-x",
        "prompt_hash": "abc",
        "status": status,
        "answer": "Phạt tiền từ 800.000 đồng",
    }


def test_append_and_read_vietnamese(tmp_path: Path) -> None:
    p = tmp_path / "sub" / "out.jsonl"
    append_jsonl(p, _rec("q1"))
    append_jsonl(p, _rec("q2"))
    rows = list(read_jsonl(p))
    assert [r["question_id"] for r in rows] == ["q1", "q2"]
    assert rows[0]["answer"] == "Phạt tiền từ 800.000 đồng"
    assert "Phạt" in p.read_text(encoding="utf-8")  # ensure_ascii=False


def test_writer_flushes_each_line(tmp_path: Path) -> None:
    p = tmp_path / "out.jsonl"
    with JsonlWriter(p) as w:
        w.write(_rec("q1"))
        # File vẫn đang mở: đọc từ handle khác phải thấy ngay dòng vừa ghi.
        assert [r["question_id"] for r in read_jsonl(p)] == ["q1"]
        w.write(_rec("q2"))
        assert len(list(read_jsonl(p))) == 2


def test_missing_file_is_empty(tmp_path: Path) -> None:
    assert list(read_jsonl(tmp_path / "nope.jsonl")) == []
    assert done_keys(tmp_path / "nope.jsonl", KEY) == set()


def test_truncated_last_line_skipped(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    p = tmp_path / "out.jsonl"
    append_jsonl(p, _rec("q1"))
    with p.open("a", encoding="utf-8") as f:
        f.write('{"config_name": "G", "question_id": "q2", "ans')  # bị ngắt giữa chừng
    with caplog.at_level(logging.WARNING):
        rows = list(read_jsonl(p))
    assert [r["question_id"] for r in rows] == ["q1"]
    assert "cắt dở" in caplog.text

    # Ghi tiếp sau crash: dòng cắt dở bị cắt bỏ, file đọc lại sạch.
    append_jsonl(p, _rec("q2"))
    assert [r["question_id"] for r in read_jsonl(p)] == ["q1", "q2"]


def test_valid_last_line_without_newline_kept(tmp_path: Path) -> None:
    p = tmp_path / "out.jsonl"
    p.write_text('{"a": 1}', encoding="utf-8")
    append_jsonl(p, {"a": 2})
    assert list(read_jsonl(p)) == [{"a": 1}, {"a": 2}]


def test_corrupt_middle_line_raises(tmp_path: Path) -> None:
    p = tmp_path / "out.jsonl"
    p.write_text('{"a": 1}\nnot json\n{"a": 2}\n', encoding="utf-8")
    with pytest.raises(ValueError, match="out.jsonl:2"):
        list(read_jsonl(p))


def test_done_keys_multi_field_and_where(tmp_path: Path) -> None:
    p = tmp_path / "out.jsonl"
    for r in [_rec("q1"), _rec("q2", status="error"), _rec("q1", config="B3")]:
        append_jsonl(p, r)
    append_jsonl(p, {"question_id": "q9"})  # thiếu trường khóa
    keys = done_keys(p, KEY)
    assert keys == {
        ("G", "q1", "gemini-x", "abc"),
        ("G", "q2", "gemini-x", "abc"),
        ("B3", "q1", "gemini-x", "abc"),
    }
    ok_only = done_keys(p, KEY, where=lambda r: r.get("status") != "error")
    assert ("G", "q2", "gemini-x", "abc") not in ok_only
    assert len(ok_only) == 2


def test_resume_does_not_duplicate(tmp_path: Path) -> None:
    p = tmp_path / "out.jsonl"
    questions = ["q1", "q2", "q3", "q4"]

    def run(stop_after: int | None) -> int:
        done = done_keys(p, KEY)
        n = 0
        with JsonlWriter(p) as w:
            for q in questions:
                rec = _rec(q)
                if tuple(rec[k] for k in KEY) in done:
                    continue
                if stop_after is not None and n == stop_after:
                    return n  # mô phỏng bị dừng giữa chừng
                w.write(rec)
                n += 1
        return n

    assert run(stop_after=2) == 2
    assert run(stop_after=None) == 2
    assert run(stop_after=None) == 0
    assert [r["question_id"] for r in read_jsonl(p)] == questions


class _Item(BaseModel):
    unit_id: str
    effective_from: date
    effective_to: date | None = None


def test_pydantic_and_dates(tmp_path: Path) -> None:
    p = tmp_path / "out.jsonl"
    append_jsonl(p, _Item(unit_id="ND168-2024/D6/K4/a", effective_from=date(2025, 1, 1)))
    append_jsonl(p, {"d": date(2026, 1, 1), "s": {"b", "a"}})
    rows = list(read_jsonl(p))
    assert rows[0] == {
        "unit_id": "ND168-2024/D6/K4/a",
        "effective_from": "2025-01-01",
        "effective_to": None,
    }
    assert rows[1] == {"d": "2026-01-01", "s": ["a", "b"]}


def test_write_jsonl_atomic_overwrite(tmp_path: Path) -> None:
    p = tmp_path / "units.jsonl"
    assert write_jsonl(p, [{"i": i} for i in range(3)]) == 3
    assert write_jsonl(p, [{"i": 9}]) == 1
    assert list(read_jsonl(p)) == [{"i": 9}]

    def boom():
        yield {"i": 1}
        raise RuntimeError("stop")

    with pytest.raises(RuntimeError):
        write_jsonl(p, boom())
    assert list(read_jsonl(p)) == [{"i": 9}]  # file cũ còn nguyên
    assert [f.name for f in tmp_path.iterdir()] == ["units.jsonl"]  # không sót file tạm
