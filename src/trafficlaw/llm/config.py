"""Cấu hình lớp LLM (``configs/llm.yaml``). API key **không** nằm ở đây: chỉ tên biến môi trường."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, Field, model_validator


class ProviderConfig(BaseModel):
    kind: Literal["gemini", "openai_compat"]
    base_url: str
    api_key_env: str
    model_id: str | None = None
    rpm: int | None = None
    tpm: int | None = None
    rpd: int | None = None
    tpd: int | None = None
    timeout_s: float = 60.0
    json_mode: Literal["schema", "object", "none"] = "object"
    reset_utc_offset_h: float = 0.0
    params: dict[str, Any] = Field(default_factory=dict)
    """Ghi đè/bổ sung ``params`` chung cho provider này (vd. ``thinking_budget`` của Gemini)."""
    extra_headers: dict[str, str] = Field(default_factory=dict)
    extra_body: dict[str, Any] = Field(default_factory=dict)


class MainModel(BaseModel):
    """Model **chốt** cho đánh giá + demo (một ``model_id``, không fallback khi đánh giá)."""

    provider: str
    model_id: str | None = None


class RetryConfig(BaseModel):
    max_retries: int = 5
    base_s: float = 1.0
    cap_s: float = 60.0
    seed: int = 42


class LLMConfig(BaseModel):
    main: MainModel
    params: dict[str, Any] = Field(default_factory=lambda: {"temperature": 0})
    providers: dict[str, ProviderConfig]
    fallback_order: list[str] = Field(default_factory=list)
    retry: RetryConfig = Field(default_factory=RetryConfig)
    cache_path: str | None = "data/cache/llm.sqlite"
    usage_db_path: str | None = "data/cache/llm_usage.sqlite"
    repair_prompt: str = "format_repair"

    @model_validator(mode="after")
    def _check(self) -> LLMConfig:
        names = [self.main.provider, *self.fallback_order]
        unknown = [n for n in names if n not in self.providers]
        if unknown:
            raise ValueError(f"provider không có trong providers: {unknown}")
        return self

    def params_for(self, provider: str) -> dict[str, Any]:
        return {**self.params, **self.providers[provider].params}


def load_llm_config(path: str | Path) -> LLMConfig:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    return LLMConfig.model_validate(data)
