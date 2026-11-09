"""Nạp cấu hình/đường dẫn dùng chung cho các script M8 (``build_graph --extract``,
``extraction_gold``, ``eval_extraction``)."""

from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Any

import yaml

from trafficlaw.graph.embedded import EmbeddedStore
from trafficlaw.graph.extract import Catalog, ExtractConfig
from trafficlaw.graph.extract_pipeline import ExtractPaths, load_catalog


def _yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


@dataclass
class ExtractEnv:
    root: Path

    @cached_property
    def paths_cfg(self) -> dict[str, Any]:
        return _yaml(self.root / "configs" / "paths.yaml")

    @cached_property
    def raw_cfg(self) -> dict[str, Any]:
        return _yaml(self.root / self.paths_cfg.get("extract_config", "configs/extract.yaml"))

    @cached_property
    def cfg(self) -> ExtractConfig:
        return ExtractConfig.model_validate(self.raw_cfg)

    @cached_property
    def paths(self) -> ExtractPaths:
        return ExtractPaths(
            graph_dir=self.root / self.paths_cfg["graph_dir"],
            out_dir=self.root / self.raw_cfg.get("out_dir", "data/processed/extraction"),
            catalog=self.root
            / self.raw_cfg.get("catalog_path", "data/registry/extract_catalog.yaml"),
        )

    @cached_property
    def store(self) -> EmbeddedStore:
        """Đồ thị M5 (chỉ 3 file cấu trúc/pháp lý — không gồm file ngữ nghĩa đã publish)."""
        return EmbeddedStore.from_dir_base(self.paths.graph_dir)

    def catalog(self) -> Catalog | None:
        return load_catalog(self.paths.catalog)

    @property
    def gold(self) -> dict[str, Any]:
        return self.raw_cfg.get("gold") or {}

    @property
    def eval(self) -> dict[str, Any]:
        return self.raw_cfg.get("eval") or {}

    def p(self, rel: str) -> Path:
        return self.root / rel

    @property
    def llm_config_path(self) -> Path:
        return self.root / self.paths_cfg.get("llm_config", "configs/llm.yaml")


__all__ = ["ExtractEnv"]
