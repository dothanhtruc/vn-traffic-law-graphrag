"""Gọi API thật (``-m slow``): mỗi provider có key + model_id một ping JSON. Thiếu key → skip.

Không dùng cache (đo gọi thật), nhưng **có** bộ đếm RPD dùng chung ``data/cache/llm_usage.sqlite``.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import BaseModel

from trafficlaw.llm.client import build_client, has_key
from trafficlaw.llm.config import load_llm_config
from trafficlaw.llm.prompt_loader import load_prompt
from trafficlaw.utils.env import load_dotenv

REPO = Path(__file__).resolve().parents[2]
pytestmark = pytest.mark.slow


class Ping(BaseModel):
    ok: bool
    echo: str
    sum: int


@pytest.mark.parametrize("provider", ["gemini", "groq", "openrouter"])
def test_live_ping(provider: str):
    load_dotenv(REPO / ".env")
    cfg = load_llm_config(REPO / "configs" / "llm.yaml")
    if not has_key(cfg, provider):
        pytest.skip(f"thiếu {cfg.providers[provider].api_key_env}")
    mid = cfg.main.model_id if provider == cfg.main.provider else None
    if not (mid or cfg.providers[provider].model_id):
        pytest.skip(f"{provider}: chưa chốt model_id")
    client = build_client(cfg, provider, root=REPO, use_cache=False)
    msg = load_prompt("ping").render(word="đường-bộ", a=40, b=2)
    r = client.generate([{"role": "user", "content": msg}], json_schema=Ping, use_cache=False)
    assert r.status == "ok", r.error
    assert r.parsed == {"ok": True, "echo": "đường-bộ", "sum": 42}
    assert r.usage.total_tokens > 0 and r.latency_ms > 0
