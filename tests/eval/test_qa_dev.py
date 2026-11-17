"""M13b: chế độ tập dev của qa_tool — đường dẫn tách khỏi test, hạn mức dev, quan hệ unit."""

from __future__ import annotations

from pathlib import Path

from scripts.qa_tool import QAEnv, _related

ROOT = Path(__file__).resolve().parents[2]


def test_use_dev_remaps_paths_and_quota() -> None:
    env = QAEnv(ROOT)
    main_test = env.p("test")
    main_total = env.targets.total
    env.use_dev()
    assert env.is_dev
    assert env.p("test").name == "dev_multi.jsonl" and env.p("test_main") == main_test
    for k in ("drafts", "drafts_md", "test_review", "test_edits", "draft_dir", "validate_dir"):
        assert "dev" in env.p(k).name, k
    quota = env.cfg["dev"]["quota"]
    assert env.targets.question_type == quota and env.targets.total == sum(quota.values())
    assert env.cfg["targets_main"]["total"] == main_total
    assert env.cfg["dev"]["exclude_level"]["default"] == "dieu"


def test_related_units() -> None:
    assert _related("ND168-2024/D6/K3", "ND168-2024/D6/K3/a")
    assert _related("ND168-2024/D6/K3/a", "ND168-2024/D6/K3")
    assert not _related("ND168-2024/D6/K3", "ND168-2024/D6/K30")
    assert not _related("ND168-2024/D6/K1", "ND168-2024/D6/K3")
