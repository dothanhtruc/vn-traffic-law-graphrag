"""M16: định dạng số, văn bản mẫu không có số trần, nguồn có truy vết, trích hạn chế."""

from __future__ import annotations

import ast
import re
from collections import Counter
from pathlib import Path

import pytest

from trafficlaw.eval.qa_subsets import data_version
from trafficlaw.report import fmt, sections, texts
from trafficlaw.report.limitations import collect, extract_section, extract_span
from trafficlaw.report.sources import MissingSourceError, SourceStore, parse_specs, plain
from trafficlaw.report.tables import md_table

SRC = Path(__file__).resolve().parents[2] / "src" / "trafficlaw" / "report"

# ------------------------------------------------------------------ định dạng


def test_vn_numbers() -> None:
    assert fmt.vn_int(20129) == "20.129"
    assert fmt.vn_int(None) == "—"
    assert fmt.vn_pct(0.843423) == "84,3"
    assert fmt.vn_pct(0.9975, 2) == "99,75"
    assert fmt.vn_dec(0.8689, 3) == "0,869"
    assert fmt.vn_dec(-1.625, 3) == "−1,625"
    assert fmt.vn_dec(-0.0001, 1) == "0,0"  # không có "−0,0"
    assert fmt.vn_dec(1234567.5, 1) == "1.234.567,5"
    assert fmt.vn_signed_pct(0.0359) == "+3,6"
    assert fmt.vn_signed_pct(-0.0058) == "−0,6"
    assert fmt.vn_ci_pct([0.814, 0.873]) == "81,4…87,3"
    assert fmt.vn_ci_pct([-0.011, 0.006]) == "−1,1…0,6"
    assert fmt.vn_p(0.0004) == "<0,001"
    assert fmt.vn_p(0.0412) == "0,041"
    assert fmt.vn_p(True) == "—"


def test_md_table_shape() -> None:
    out = md_table(["a", "b"], [["x|y", "1"]])
    assert out.splitlines()[1] == "| --- | ---: |"
    assert "x\\|y" in out
    with pytest.raises(ValueError):
        md_table(["a", "b"], [["x"]])


# ------------------------------------------------------------------ không số trần

_ALLOWED_PREV = re.compile(r"[^\W\d]|@|_")


def bare_digits(s: str) -> list[str]:
    """Chữ số không gắn với định danh (``B1``, ``r@5``, ``train_1000``, ``top-5``, ``M1–M3``)."""
    s = re.sub(r"\{[^{}]*\}", "", s)
    bad = []
    for m in re.finditer(r"\d+", s):
        i = m.start()
        prev = s[i - 1] if i else ""
        if prev and _ALLOWED_PREV.match(prev):
            continue
        if prev in "-–" and i >= 2 and re.match(r"[^\W\d]", s[i - 2]):
            continue
        bad.append(s[max(0, i - 15) : m.end() + 5])
    return bad


def test_bare_digit_detector() -> None:
    assert bare_digits("Recall@5, B1, M1–M3, train_1000, top-5, {n}") == []
    assert bare_digits("CI 95%") and bare_digits("ngày 03/11/2026") and bare_digits("0,05")


def test_texts_have_no_bare_digits() -> None:
    bad = {k: b for k, v in texts.TEXT.items() if (b := bare_digits(v))}
    assert bad == {}


def _string_literals(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    spec_nodes = {
        id(n.format_spec)
        for n in ast.walk(tree)
        if isinstance(n, ast.FormattedValue) and n.format_spec
    }
    skip: set[int] = set()
    for n in ast.walk(tree):
        if id(n) in spec_nodes:
            skip |= {id(x) for x in ast.walk(n)}
        # Docstring / chuỗi đứng riêng (chú thích cho người đọc code) không vào báo cáo.
        if isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant):
            skip.add(id(n.value))
    return [
        n.value
        for n in ast.walk(tree)
        if isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in skip
    ]


@pytest.mark.parametrize("name", ["sections.py", "build.py"])
def test_code_strings_have_no_bare_digits(name: str) -> None:
    """Chuỗi trong code ghép báo cáo không được chứa con số gõ tay (trừ docstring)."""
    bad = [(s[:60], b) for s in _string_literals(SRC / name) if (b := bare_digits(s))]
    assert bad == []


def test_t_requires_formatted_strings() -> None:
    with pytest.raises(TypeError):
        texts.t("seed", s=42)
    assert texts.t("seed", s="42") == "seed 42"


# ------------------------------------------------------------------ nguồn


def _store(tmp_path: Path, files: dict[str, str], specs: dict[str, dict]) -> SourceStore:
    for rel, content in files.items():
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    return SourceStore(root=tmp_path, specs=parse_specs(specs, {"run_id": "r1"}))


def test_tracked_records_fields_and_missing(tmp_path: Path) -> None:
    st = _store(
        tmp_path,
        {
            "results/r1/summary.json": '{"a": {"b": 1, "c": [2, 3]}, "d": 4}',
            "log.jsonl": "\n".join(
                ['{"doc_id": "X", "n": 1}', '{"doc_id": "Y", "n": 2}', '{"doc_id": "X", "n": 5}']
            ),
        },
        {
            "s": {"path": "results/{run_id}/summary.json", "kind": "json"},
            "log": {"path": "log.jsonl", "kind": "jsonl", "release": "rel-v1"},
            "gone": {"path": "nope.json", "kind": "json", "release": "rel-v2"},
        },
    )
    s = st.get("s")
    assert s["a"]["b"] == 1
    assert s["a"]["c"][1] == 3
    assert "d" in s  # kiểm tra tồn tại không tính là đọc
    latest = st.latest_by("log", "doc_id")
    assert {k: v["n"] for k, v in latest.items()} == {"X": 5, "Y": 2}
    with pytest.raises(MissingSourceError):
        st.get("gone")
    man = {r["id"]: r for r in st.manifest()}
    assert man["s"]["fields"] == ["a.b", "a.c[1]"]
    assert man["s"]["status"] == "ok" and len(man["s"]["sha256"]) == 64
    assert man["log"]["fields"] == ["[doc_id=X].n", "[doc_id=Y].n"]
    assert man["gone"] == {
        "id": "gone",
        "module": "—",
        "path": "nope.json",
        "release": "rel-v2",
        "status": "missing",
    }
    assert plain(st.get("s")) == {"a": {"b": 1, "c": [2, 3]}, "d": 4}


def test_current_data_version_matches_qa_subsets(tmp_path: Path) -> None:
    files = {
        "data/registry/documents.yaml": "documents: []\n",
        "data/processed/unit_versions.jsonl": '{"x": 1}\n',
        "data/processed/units_added.jsonl": "",
    }
    st = _store(
        tmp_path,
        files,
        {
            "registry": {"path": "data/registry/documents.yaml", "kind": "yaml"},
            "unit_versions": {"path": "data/processed/unit_versions.jsonl", "kind": "hash"},
            "units_added": {"path": "data/processed/units_added.jsonl", "kind": "hash"},
        },
    )
    expected = data_version([tmp_path / p for p in files])
    assert sections.current_data_version(st) == expected


def test_vbhn_rates() -> None:
    c = Counter(
        khop=10,
        chi_khac_dinh_dang=2,
        khac_noi_dung=1,
        thieu_vbhn=1,
        loai_ngoai_danh_muc=7,
        loai_loi_du_lieu=1,
    )
    assert sections.vbhn_rates({"V": c}) == {"V": (12, 14)}


# ------------------------------------------------------------------ hạn chế

DOC = """# Tiêu đề
- Hạn chế: một hai. Artifact ở Release `x`.
**Hạn chế phải nêu**: ba bốn.

## Hạn chế

- Dòng một
  tiếp theo.
- Dòng hai.

## Khác
- không lấy
"""


def test_extract_span_and_section() -> None:
    assert extract_span(DOC, "Hạn chế: một", "hai.") == (2, "Hạn chế: một hai.")
    assert extract_span(DOC, "**Hạn chế phải nêu**") == (3, "**Hạn chế phải nêu**: ba bốn.")
    assert extract_span(DOC, "không có") is None
    assert extract_span(DOC, "Hạn chế") == "trung_lap"
    assert extract_section(DOC, "## Hạn chế") == (5, ["Dòng một tiếp theo.", "Dòng hai."])
    assert extract_section(DOC, "## Không có") is None


def test_collect_reports_not_found() -> None:
    specs = [
        {"module": "M1", "title": "a", "source": "d", "start": "Hạn chế: một", "end": "hai."},
        {"module": "M2", "title": "b", "source": "d", "section": "## Hạn chế"},
        {"module": "M3", "title": "c", "source": "d", "start": "đã bị xoá"},
    ]
    out = collect(specs, {"d": DOC}, {"d": "docs/x.md"})
    assert [x.status for x in out] == ["ok", "ok", "khong_tim_thay"]
    assert out[0].items == ("Hạn chế: một hai.",) and out[0].source == "docs/x.md"
    assert out[1].line == 5 and len(out[1].items) == 2
