"""Cấu hình bộ chạy đánh giá M13 (``configs/eval.yaml``)."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field


class RetrieveStage(BaseModel):
    model_config = ConfigDict(extra="forbid")
    configs: list[str] = Field(default_factory=lambda: ["G", "B3", "B1", "B2", "A1", "A2"])
    set: str = "full"


class JudgeConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    model_id: str = "mistral-small-3.2"
    prompt: str = "judge"
    configs: list[str] = Field(default_factory=lambda: ["B0", "B1", "B3", "G", "A2"])
    subset: str = "judge_200"
    max_output_tokens: int = 1024
    output_tokens_estimate: int = 250


class VarianceConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    config: str = "G"
    subset: str = "variance_100"
    seeds: list[int] = Field(default_factory=lambda: [42, 43, 44])


class JudgeCheckConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    n: int = 40
    seed_key: str = "m13_judge_check"
    config: str = "G"


class MetricsConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    k: list[int] = Field(default_factory=lambda: [1, 5, 10, 20])


class StatsConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    bootstrap: int = 1000
    seed: int = 42
    compare_to: str = "G"
    wilcoxon_zero: str = "pratt"
    multiple: str = "holm"


class RegressionConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    config: str = "G"
    subset: str = "regression_100"
    k: int = 5
    max_drop: float = 0.02
    baseline: str = "data/qa/retrieval_baseline_test.json"


class SmokeConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    test: str = "tests/fixtures/eval/smoke_test.jsonl"
    graph_dir: str = "tests/fixtures/mini_graph"
    run_id: str = "smoke"


class EvalConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    run_id: str = "m13-test"
    test: str = "data/qa/test.jsonl"
    subsets: str | None = "data/qa/subsets.json"
    drafts: str | None = "data/qa/test_drafts.jsonl"
    oos: str | None = None
    """Câu ``ngoai_pham_vi`` bổ sung, không qua validator test (tập dev M13c)."""
    answer_config: str = "configs/answer.yaml"
    """Cấu hình sinh câu trả lời (biến thể prompt/τ trên tập dev M13c)."""
    results_dir: str = "results"
    seed: int = 42
    today: date = date(2026, 11, 3)
    generate: dict[str, str] = Field(default_factory=lambda: {"G": "full"})
    retrieve: RetrieveStage = Field(default_factory=RetrieveStage)
    judge: JudgeConfig = Field(default_factory=JudgeConfig)
    variance: VarianceConfig = Field(default_factory=VarianceConfig)
    judge_check: JudgeCheckConfig = Field(default_factory=JudgeCheckConfig)
    metrics: MetricsConfig = Field(default_factory=MetricsConfig)
    stats: StatsConfig = Field(default_factory=StatsConfig)
    regression: RegressionConfig = Field(default_factory=RegressionConfig)
    smoke: SmokeConfig = Field(default_factory=SmokeConfig)
    output_tokens_estimate: int = 350

    def run_dir(self, root: Path, run_id: str | None = None) -> Path:
        return root / self.results_dir / (run_id or self.run_id)


def load_eval_config(path: str | Path) -> EvalConfig:
    return EvalConfig.model_validate(yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {})


__all__ = [
    "EvalConfig",
    "JudgeCheckConfig",
    "JudgeConfig",
    "MetricsConfig",
    "RegressionConfig",
    "RetrieveStage",
    "SmokeConfig",
    "StatsConfig",
    "VarianceConfig",
    "load_eval_config",
]
