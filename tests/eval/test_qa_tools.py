"""M9: TF-IDF gần trùng (so với vét cạn), tập con cố định, phiếu viết (tất định, mẫu dòng qua
validator), CLI ``qa_tool`` trên repo tạm."""

from __future__ import annotations

import json
import random
from datetime import date
from pathlib import Path
from typing import Any

import pytest
import yaml

from scripts import qa_tool
from trafficlaw.eval.qa_plan import PlanConfig, allocate, plan_suggestions, render_worksheet
from trafficlaw.eval.qa_schema import QAItem
from trafficlaw.eval.qa_subsets import SubsetSpec, build_subsets, draw, subsets_status
from trafficlaw.eval.qa_validate import Targets, ValidateConfig, validate_items
from trafficlaw.eval.textsim import TfidfSpace, cosine, near_pairs
from trafficlaw.graph.embedded import EmbeddedStore
from trafficlaw.graph.store import GraphEdge, GraphNode

ROOT = Path(__file__).resolve().parents[2]
MINI = ROOT / "tests/fixtures/mini_graph"


@pytest.fixture(scope="module")
def store() -> EmbeddedStore:
    """mini_graph + một CheTai (M8) nêu ở ND168 Đ6 K5, áp cho Điểm a."""
    st = EmbeddedStore.from_dir(MINI)
    k5 = "ND168-2024/D6/K5"
    st.upsert_nodes(
        [
            GraphNode(
                f"CHETAI:{k5}@v0#0",
                "CheTai",
                {
                    "unit_id": k5,
                    "version_id": f"{k5}@v0",
                    "loai": "phat_tien",
                    "min_vnd": 4000000,
                    "max_vnd": 6000000,
                },
            )
        ]
    )
    st.upsert_edges(
        [
            GraphEdge.make(
                "BI_XU_PHAT",
                f"{k5}/a@v0",
                f"CHETAI:{k5}@v0#0",
                {"effective_from": "2025-01-01", "effective_to": None, "nguon": "ke_thua_khoan"},
            )
        ]
    )
    return st


# --------------------------------------------------------------------------- textsim


def test_near_pairs_exact_vs_bruteforce() -> None:
    rng = random.Random(1)
    words = [
        "xe",
        "ô",
        "tô",
        "mô",
        "tô",
        "gắn",
        "máy",
        "phạt",
        "tiền",
        "vượt",
        "đèn",
        "đỏ",
        "tốc",
        "độ",
        "giấy",
        "phép",
        "lái",
        "điểm",
        "trừ",
    ]
    base = [" ".join(rng.choice(words) for _ in range(rng.randint(4, 12))) for _ in range(60)]
    qs = base + [b + " ạ" for b in base[:20]]
    cs = base[10:50] + [b.replace("xe", "xe con") for b in base[:15]]
    got = near_pairs(qs, cs, threshold=0.8, max_postings=3)
    space = TfidfSpace.fit([*qs, *cs])
    qv = [space.vector(t) for t in qs]
    cv = [space.vector(t) for t in cs]
    want = sorted(
        (i, j) for i in range(len(qs)) for j in range(len(cs)) if cosine(qv[i], cv[j]) >= 0.8
    )
    assert [(i, j) for i, j, _ in got] == want and want


def test_near_pairs_same() -> None:
    qs = [
        "Lái ô tô vượt đèn đỏ bị phạt bao nhiêu?",
        "Lái ô tô vượt đèn đỏ bị phạt bao nhiêu ?",
        "Định nghĩa xe gắn máy là gì?",
    ]
    assert [(i, j) for i, j, _ in near_pairs(qs, qs, same=True)] == [(0, 1)]


# --------------------------------------------------------------------------- subsets


def item(i: int, qt: str = "muc_phat", tier: str | None = "A", pair: str | None = None) -> QAItem:
    return QAItem(
        qid=f"t{i:03d}",
        question=f"q{i}",
        as_of=date(2026, 11, 3),
        question_type=qt,
        tier=tier,
        answer="a",
        gold_units=[] if qt == "ngoai_pham_vi" else ["X/D1"],
        pair_id=pair,
    )  # type: ignore[arg-type]


def test_subsets_stratified_stable_pairs() -> None:
    items = [item(i) for i in range(60)] + [item(100 + i, "dinh_nghia", "B") for i in range(20)]
    items += [item(200 + i, "theo_thoi_diem", "A", pair=f"p{i // 2}") for i in range(20)]
    items += [item(300 + i, "ngoai_pham_vi", None) for i in range(10)]
    a = draw(items, "ablation_200", SubsetSpec(55))
    b = draw(list(reversed(items)), "ablation_200", SubsetSpec(55))
    assert a == b  # không phụ thuộc thứ tự file
    assert a["by_stratum"]["A|muc_phat"] == 30 and a["by_stratum"]["B|dinh_nghia"] == 10
    chosen = set(a["qids"])
    for k in range(10):  # cặp không bị tách
        pair = {f"t{200 + 2 * k:03d}", f"t{201 + 2 * k:03d}"}
        assert pair <= chosen or not pair & chosen
    other = draw(items, "judge_200", SubsetSpec(55))
    assert other["qids"] != a["qids"]
    reg = draw(items, "regression_100", SubsetSpec(100, ("ngoai_pham_vi",)))
    assert reg["n"] == 100 and not any(q.startswith("t3") for q in reg["qids"])
    # thêm câu mới chỉ đổi ít phần tử
    c = draw([*items, *[item(400 + i) for i in range(5)]], "ablation_200", SubsetSpec(55))
    assert len(set(c["qids"]) ^ chosen) <= 12


def test_subsets_status(tmp_path: Path) -> None:
    test = tmp_path / "test.jsonl"
    test.write_text("{}\n", encoding="utf-8")
    sub = tmp_path / "subsets.json"
    assert subsets_status(sub, test) == "missing"
    import hashlib

    out = build_subsets([item(1)], hashlib.sha256(test.read_bytes()).hexdigest())
    sub.write_text(json.dumps(out), encoding="utf-8")
    assert subsets_status(sub, test) == "ok"
    test.write_text("{}\n{}\n", encoding="utf-8")
    assert subsets_status(sub, test) == "stale"


# --------------------------------------------------------------------------- phiếu viết


def test_allocate() -> None:
    assert allocate(10, {"A": 7, "B": 2, "C": 1}, {"A": 100, "B": 100, "C": 100}) == {
        "A": 7,
        "B": 2,
        "C": 1,
    }
    assert allocate(10, {"A": 7, "B": 2, "C": 1}, {"A": 3, "B": 100, "C": 0}) == {"A": 3, "B": 7}
    assert sum(allocate(5, {"A": 1, "B": 1, "C": 1}, {"A": 9, "B": 9, "C": 9}).values()) == 5


TARGETS = Targets(
    total=40,
    tier={"A": 70, "B": 20, "C": 5, "historical": 5},
    question_type={
        "muc_phat": 6,
        "tru_diem": 2,
        "hanh_vi_cam_nghia_vu": 4,
        "dinh_nghia": 2,
        "thu_tuc_tham_quyen": 4,
        "theo_thoi_diem": 4,
        "da_buoc": 4,
        "so_sanh": 2,
        "ngoai_pham_vi": 2,
    },
)


def test_plan_deterministic_and_templates_validate(store: EmbeddedStore) -> None:
    cfg = PlanConfig()
    s1, st1 = plan_suggestions(store, TARGETS, cfg)
    s2, _ = plan_suggestions(store, TARGETS, cfg)
    assert [(s.sid, [c.chunk_id for c in s.chunks]) for s in s1] == [
        (s.sid, [c.chunk_id for c in s.chunks]) for s in s2
    ]
    types = {s.qtype for s in s1}
    assert {"muc_phat", "theo_thoi_diem", "da_buoc"} <= types
    text = render_worksheet(s1, store, TARGETS, cfg, st1)
    assert '"question": ""' in text and '"answer": ""' in text  # không sinh câu hỏi/đáp án
    rows: list[dict[str, Any]] = []
    for i, ln in enumerate(x for x in text.split("\n") if x.startswith('{"qid"')):
        r = json.loads(ln)
        nums = " ".join(f"{x['value']:,}".replace(",", ".") for x in r["required_numbers"])
        r.update(
            qid=f"x{i}",
            question=f"Câu số {i} mã {i * 7919} về nội dung {i % 7}",
            answer=f"Đáp án {i}: {nums}",
        )
        rows.append(r)
    res = validate_items(rows, "test", store, ValidateConfig())
    assert res.n_errors == 0, [i for i in res.issues if i.level == "error"][:5]


# --------------------------------------------------------------------------- CLI


def make_root(tmp: Path) -> Path:
    (tmp / "configs").mkdir()
    paths = yaml.safe_load((ROOT / "configs/paths.yaml").read_text(encoding="utf-8"))
    paths["graph_dir"] = str(MINI)
    for k in ("documents", "unit_versions", "units_added"):
        paths[k] = str(tmp / f"{k}.missing")
    (tmp / "configs/paths.yaml").write_text(yaml.safe_dump(paths), encoding="utf-8")
    qa = yaml.safe_load((ROOT / "configs/qa.yaml").read_text(encoding="utf-8"))
    (tmp / "configs/qa.yaml").write_text(yaml.safe_dump(qa, allow_unicode=True), encoding="utf-8")
    return tmp


def test_cli_validate_partial_and_subsets(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = make_root(tmp_path)
    assert (
        qa_tool.main(["--repo-root", str(root), "validate", "--split", "test"]) == 0
    )  # chưa có file
    test = root / "data/qa/test.jsonl"
    test.parent.mkdir(parents=True, exist_ok=True)
    good = {
        "qid": "t1",
        "question": "Lái ô tô vi phạm khoản 5 bị phạt bao nhiêu?",
        "as_of": "2026-11-03",
        "question_type": "muc_phat",
        "tier": "A",
        "answer": "Từ 4.000.000 đồng đến 6.000.000 đồng.",
        "gold_units": ["ND168-2024/D6/K5"],
        "required_numbers": [{"value": 4000000, "unit": "vnd"}],
    }
    test.write_text(json.dumps(good, ensure_ascii=False) + "\n", encoding="utf-8")
    before = test.read_bytes()
    assert qa_tool.main(["--repo-root", str(root), "validate"]) == 0
    assert test.read_bytes() == before  # không sửa test.jsonl
    resolved = (root / "data/processed/qa/test_resolved.jsonl").read_text(encoding="utf-8")
    assert "ND168-2024/D6/K5@v0" in resolved
    assert (root / "data/qa/qa_summary.md").is_file()
    assert qa_tool.main(["--repo-root", str(root), "subsets"]) == 0
    sub = json.loads((root / "data/qa/subsets.json").read_text(encoding="utf-8"))
    assert sub["subsets"]["ablation_200"]["qids"] == ["t1"]
    bad = dict(good, qid="t2", gold_units=["ND168-2024/D6/K99"])
    with test.open("a", encoding="utf-8") as f:
        f.write(json.dumps(bad) + "\n")
    assert qa_tool.main(["--repo-root", str(root), "validate"]) == 1
    out = capsys.readouterr().out
    assert "unit_khong_ton_tai" in out and "2/500" in out
