"""build_client từ config, FallbackClient, và key không lọt vào log/cache/exception/kết quả."""

from __future__ import annotations

import json
import logging
from pathlib import Path

import httpx
import pytest

from tests.llm.conftest import Answer
from trafficlaw.llm.client import FallbackClient, build_client, build_fallback_client
from trafficlaw.llm.config import LLMConfig, load_llm_config
from trafficlaw.llm.providers.fake import FakeClient, ok, quota_exhausted, server_error
from trafficlaw.llm.types import AuthError, QuotaExhaustedError
from trafficlaw.utils.logging import SecretRedactFilter

REPO = Path(__file__).resolve().parents[2]
KEY = "AIzaFAKE-secret-key-0123456789abcdef"
GOOD = '{"answer": "Phạt tiền", "citations": ["ND168-2024/D6/K4/a"]}'
MSG = [{"role": "user", "content": "Mức phạt? Trả lời JSON."}]


def _cfg(tmp_path: Path) -> LLMConfig:
    cfg = load_llm_config(REPO / "configs" / "llm.yaml")
    for p in cfg.providers.values():
        p.model_id = "test-model"
    cfg.main.model_id = "main-model"  # khác providers.gemini.model_id: main phải thắng
    cfg.cache_path = str(tmp_path / "cache.sqlite")
    cfg.usage_db_path = str(tmp_path / "usage.sqlite")
    return cfg


def test_repo_config_valid():
    cfg = load_llm_config(REPO / "configs" / "llm.yaml")
    assert cfg.params["temperature"] == 0
    assert cfg.main.provider in cfg.providers
    assert set(cfg.fallback_order) <= set(cfg.providers)
    for p in cfg.providers.values():
        assert p.api_key_env.endswith("_API_KEY")  # chỉ tên biến, không key


def test_config_rejects_unknown_provider():
    with pytest.raises(ValueError):
        LLMConfig.model_validate({"main": {"provider": "x"}, "providers": {}})


def _gemini_transport(seen: list[httpx.Request], status: int = 200):
    body = {
        "candidates": [{"content": {"parts": [{"text": GOOD}]}, "finishReason": "STOP"}],
        "usageMetadata": {"promptTokenCount": 9, "candidatesTokenCount": 4, "totalTokenCount": 13},
    }
    err = {"error": {"code": 500, "message": "boom", "status": "INTERNAL"}}

    def handler(req: httpx.Request) -> httpx.Response:
        seen.append(req)
        return httpx.Response(status, json=body if status == 200 else err)

    return httpx.MockTransport(handler)


def test_build_client_main_uses_main_model(tmp_path, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", KEY)
    cfg = _cfg(tmp_path)
    seen: list[httpx.Request] = []
    c = build_client(cfg, transport=_gemini_transport(seen), sleep=lambda s: None)
    assert c.model_id == "main-model" and c.provider_name == "gemini"
    r = c.generate(MSG, json_schema=Answer)
    assert r.status == "ok" and r.usage.total_tokens == 13
    assert "main-model:generateContent" in seen[0].url.path
    assert c.limiter.usage_today() == (1, 13)


def test_missing_key(tmp_path, monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    with pytest.raises(AuthError, match="GROQ_API_KEY"):
        build_client(_cfg(tmp_path), "groq")


def test_key_never_leaks(tmp_path, monkeypatch, caplog):
    """Chạy cả luồng (ok, lỗi 500 + retry) rồi tìm key trong log, cache, usage db, kết quả."""
    monkeypatch.setenv("GEMINI_API_KEY", KEY)
    cfg = _cfg(tmp_path)
    caplog.set_level(logging.DEBUG)
    caplog.handler.addFilter(SecretRedactFilter())
    seen: list[httpx.Request] = []
    good = build_client(cfg, root=tmp_path, transport=_gemini_transport(seen), sleep=lambda s: 0)
    r_ok = good.generate(MSG, json_schema=Answer)
    bad = build_client(
        cfg, root=tmp_path, transport=_gemini_transport(seen, 500), sleep=lambda s: None
    )
    r_err = bad.generate([{"role": "user", "content": "khác"}])
    assert r_ok.status == "ok" and r_err.status == "error" and r_err.attempts == 6
    # một log cố tình chứa key → phải bị che
    logging.getLogger("trafficlaw.test").warning("key=%s", KEY)

    texts = [
        caplog.text,
        "\n".join(r.getMessage() for r in caplog.records),
        r_ok.model_dump_json(),
        r_err.model_dump_json(),
        repr(good),
        repr(good.provider),
    ]
    for f in tmp_path.glob("*.sqlite*"):
        texts.append(f.read_bytes().decode("utf-8", "ignore"))
    for t in texts:
        assert KEY not in t
    assert all(KEY not in str(req.url) for req in seen)


def test_key_not_in_exception(tmp_path, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", KEY)

    def boom(req):
        raise httpx.ConnectError(f"cannot connect {req.url}", request=req)

    c = build_client(_cfg(tmp_path), transport=httpx.MockTransport(boom), sleep=lambda s: None)
    r = c.generate(MSG)
    assert r.status == "error" and KEY not in (r.error or "")


# ------------------------------------------------------------------ fallback (demo)
def test_fallback_records_answering_model(make_client):
    a = make_client(FakeClient([server_error()], name="gemini", model_id="g"), max_retries=0)
    b = make_client(FakeClient([quota_exhausted()], name="groq", model_id="q"))
    c = make_client(FakeClient([ok(GOOD)], name="openrouter", model_id="o:free"))
    r = FallbackClient([a, b, c]).generate(MSG, json_schema=Answer)
    assert r.status == "ok" and r.provider == "openrouter" and r.model_id == "o:free"
    assert r.fallback_from == ["gemini:g", "groq:q"]


def test_fallback_first_ok_no_fallback(make_client):
    a = make_client(FakeClient([ok(GOOD)], name="gemini", model_id="g"))
    b = make_client(FakeClient([ok(GOOD)], name="groq", model_id="q"))
    r = FallbackClient([a, b]).generate(MSG)
    assert r.provider == "gemini" and r.fallback_from == [] and b.provider.n_calls == 0


def test_fallback_all_fail_returns_error(make_client):
    a = make_client(FakeClient([quota_exhausted()], name="gemini", model_id="g"))
    b = make_client(FakeClient([server_error()], name="groq", model_id="q"), max_retries=0)
    r = FallbackClient([a, b]).generate(MSG)
    assert r.status == "error" and r.provider == "groq" and r.fallback_from == ["gemini:g"]


def test_eval_client_does_not_fallback(make_client):
    a = make_client(FakeClient([quota_exhausted()], name="gemini", model_id="g"))
    with pytest.raises(QuotaExhaustedError):
        a.generate(MSG)


def test_build_fallback_client_skips_missing_keys(tmp_path, monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", KEY)
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    monkeypatch.setenv("OPENROUTER_API_KEY", KEY + "x")
    fb = build_fallback_client(_cfg(tmp_path), root=tmp_path)
    assert [c.provider_name for c in fb.clients] == ["gemini", "openrouter"]
    # cache + bộ đếm dùng chung
    assert fb.clients[0].cache is fb.clients[1].cache


def test_result_json_roundtrip(make_client):
    r = make_client(FakeClient([ok(GOOD)])).generate(MSG, json_schema=Answer)
    d = json.loads(r.model_dump_json())
    assert {"model_id", "provider", "status", "latency_ms", "attempts", "usage"} <= set(d)
