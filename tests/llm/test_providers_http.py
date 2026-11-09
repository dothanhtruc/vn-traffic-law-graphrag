"""Gemini + OpenAI-compat parse đúng phản hồi mẫu (httpx.MockTransport, không mạng)."""

from __future__ import annotations

import json

import httpx
import pytest

from trafficlaw.llm.providers.gemini import GeminiProvider
from trafficlaw.llm.providers.openai_compat import OpenAICompatProvider
from trafficlaw.llm.types import (
    AuthError,
    BadRequestError,
    LLMRequest,
    LLMTimeoutError,
    Message,
    QuotaExhaustedError,
    RateLimitError,
    ServerError,
)

KEY = "test-key-SECRET-1234567890"
REQ = LLMRequest(
    messages=[
        Message(role="system", content="Bạn là trợ lý luật."),
        Message(role="user", content="Mức phạt?"),
    ],
    params={"temperature": 0, "max_output_tokens": 256, "thinking_budget": 0},
    json_schema={"type": "object", "properties": {"a": {"type": "integer"}}},
    json_output=True,
)


def _mock(status: int, body, headers=None, seen=None):
    def handler(request: httpx.Request) -> httpx.Response:
        if seen is not None:
            seen.append(request)
        content = body if isinstance(body, bytes) else json.dumps(body).encode()
        return httpx.Response(status, content=content, headers=headers or {})

    return httpx.MockTransport(handler)


def _gemini(transport) -> GeminiProvider:
    return GeminiProvider(model_id="gemini-x", api_key=KEY, transport=transport)


def _groq(transport, json_mode="object") -> OpenAICompatProvider:
    return OpenAICompatProvider(
        name="groq",
        model_id="llama-x",
        base_url="https://api.groq.com/openai/v1",
        api_key=KEY,
        json_mode=json_mode,
        transport=transport,
    )


# ------------------------------------------------------------------ Gemini
GEMINI_OK = {
    "candidates": [
        {
            "content": {
                "role": "model",
                "parts": [{"text": "suy nghĩ…", "thought": True}, {"text": '{"a": 1}'}],
            },
            "finishReason": "STOP",
        }
    ],
    "usageMetadata": {
        "promptTokenCount": 12,
        "candidatesTokenCount": 5,
        "thoughtsTokenCount": 3,
        "totalTokenCount": 20,
    },
}


def _gemini_429(quota_id: str, delay: str = "23s") -> dict:
    return {
        "error": {
            "code": 429,
            "message": "You exceeded your current quota.",
            "status": "RESOURCE_EXHAUSTED",
            "details": [
                {
                    "@type": "type.googleapis.com/google.rpc.QuotaFailure",
                    "violations": [{"quotaMetric": "x", "quotaId": quota_id}],
                },
                {"@type": "type.googleapis.com/google.rpc.RetryInfo", "retryDelay": delay},
            ],
        }
    }


def test_gemini_ok_and_request_shape():
    seen: list[httpx.Request] = []
    r = _gemini(_mock(200, GEMINI_OK, seen=seen)).complete(REQ)
    assert r.text == '{"a": 1}' and r.finish_reason == "STOP"
    assert (r.usage.prompt_tokens, r.usage.completion_tokens, r.usage.total_tokens) == (12, 8, 20)
    assert not r.usage.estimated
    req = seen[0]
    assert req.url.path.endswith("/v1beta/models/gemini-x:generateContent")
    assert KEY not in str(req.url) and req.headers["x-goog-api-key"] == KEY
    body = json.loads(req.content)
    assert body["systemInstruction"]["parts"][0]["text"] == "Bạn là trợ lý luật."
    assert body["contents"] == [{"role": "user", "parts": [{"text": "Mức phạt?"}]}]
    gen = body["generationConfig"]
    assert gen["temperature"] == 0 and gen["maxOutputTokens"] == 256
    assert gen["responseMimeType"] == "application/json"
    assert gen["responseJsonSchema"] == REQ.json_schema
    assert gen["thinkingConfig"] == {"thinkingBudget": 0}


def test_gemini_thinking_level():
    seen: list[httpx.Request] = []
    req = REQ.model_copy(update={"params": {"thinking_level": "low"}})
    _gemini(_mock(200, GEMINI_OK, seen=seen)).complete(req)
    gen = json.loads(seen[0].content)["generationConfig"]
    assert gen["thinkingConfig"] == {"thinkingLevel": "low"}


def test_gemini_rate_limit_per_minute():
    t = _mock(429, _gemini_429("GenerateRequestsPerMinutePerProjectPerModel-FreeTier"))
    with pytest.raises(RateLimitError) as ei:
        _gemini(t).complete(REQ)
    assert ei.value.retry_after == 23.0 and ei.value.retryable


def test_gemini_quota_per_day():
    t = _mock(429, _gemini_429("GenerateRequestsPerDayPerProjectPerModel-FreeTier"))
    with pytest.raises(QuotaExhaustedError):
        _gemini(t).complete(REQ)


def test_gemini_errors():
    bad_key = {
        "error": {
            "code": 400,
            "message": "API key not valid.",
            "status": "INVALID_ARGUMENT",
            "details": [
                {"@type": "type.googleapis.com/google.rpc.ErrorInfo", "reason": "API_KEY_INVALID"}
            ],  # fmt: skip
        }
    }
    with pytest.raises(AuthError):
        _gemini(_mock(400, bad_key)).complete(REQ)
    with pytest.raises(ServerError):
        _gemini(_mock(503, {"error": {"code": 503, "message": "overloaded"}})).complete(REQ)
    with pytest.raises(BadRequestError):
        _gemini(_mock(404, {"error": {"code": 404, "message": "model not found"}})).complete(REQ)
    with pytest.raises(BadRequestError, match="SAFETY"):
        _gemini(_mock(200, {"promptFeedback": {"blockReason": "SAFETY"}})).complete(REQ)
    with pytest.raises(ServerError):
        _gemini(_mock(500, b"<html>oops</html>")).complete(REQ)


def test_gemini_missing_usage_is_estimated():
    body = {"candidates": [{"content": {"parts": [{"text": "abcdefgh"}]}, "finishReason": "STOP"}]}
    r = _gemini(_mock(200, body)).complete(REQ)
    assert r.usage.estimated and r.usage.completion_tokens == 2


def test_gemini_list_models_paginates():
    pages = iter(
        [
            {"models": [{"name": "models/a"}], "nextPageToken": "t2"},
            {"models": [{"name": "models/b"}]},
        ]
    )
    t = httpx.MockTransport(lambda req: httpx.Response(200, json=next(pages)))
    assert [m["name"] for m in _gemini(t).list_models()] == ["models/a", "models/b"]


# ------------------------------------------------------------------ OpenAI-compatible
OAI_OK = {
    "choices": [{"message": {"role": "assistant", "content": '{"a": 1}'}, "finish_reason": "stop"}],
    "usage": {"prompt_tokens": 30, "completion_tokens": 7, "total_tokens": 37},
}


def test_openai_ok_and_request_shape():
    seen: list[httpx.Request] = []
    r = _groq(_mock(200, OAI_OK, seen=seen)).complete(REQ)
    assert r.text == '{"a": 1}' and r.usage.total_tokens == 37 and r.finish_reason == "stop"
    req = seen[0]
    assert str(req.url) == "https://api.groq.com/openai/v1/chat/completions"
    assert req.headers["authorization"] == f"Bearer {KEY}"
    body = json.loads(req.content)
    assert body["model"] == "llama-x" and body["temperature"] == 0 and body["max_tokens"] == 256
    assert body["messages"][0] == {"role": "system", "content": "Bạn là trợ lý luật."}
    assert body["response_format"] == {"type": "json_object"}
    assert "thinking_budget" not in body


def test_openai_schema_mode():
    seen: list[httpx.Request] = []
    _groq(_mock(200, OAI_OK, seen=seen), json_mode="schema").complete(REQ)
    rf = json.loads(seen[0].content)["response_format"]
    assert rf["type"] == "json_schema" and rf["json_schema"]["schema"] == REQ.json_schema


def _groq_429(msg: str) -> dict:
    return {"error": {"message": msg, "type": "tokens", "code": "rate_limit_exceeded"}}


def test_openai_rate_limit_retry_after_header_and_message():
    msg = "Rate limit reached on tokens per minute (TPM): Limit 12000. Please try again in 5.5s."
    with pytest.raises(RateLimitError) as ei:
        _groq(_mock(429, _groq_429(msg), headers={"retry-after": "2"})).complete(REQ)
    assert ei.value.retry_after == 2.0
    with pytest.raises(RateLimitError) as ei:
        _groq(_mock(429, _groq_429(msg))).complete(REQ)
    assert ei.value.retry_after == 5.5
    with pytest.raises(RateLimitError) as ei:
        _groq(_mock(429, _groq_429("Please try again in 1m2.5s"))).complete(REQ)
    assert ei.value.retry_after == 62.5


def test_openai_quota_per_day():
    msg = "Rate limit reached on requests per day (RPD): Limit 1000, Used 1000."
    with pytest.raises(QuotaExhaustedError):
        _groq(_mock(429, _groq_429(msg))).complete(REQ)
    orouter = {"error": {"message": "Rate limit exceeded: free-models-per-day. ", "code": 429}}
    with pytest.raises(QuotaExhaustedError):
        _groq(_mock(429, orouter)).complete(REQ)
    with pytest.raises(QuotaExhaustedError):
        _groq(_mock(402, {"error": {"message": "Insufficient credits", "code": 402}})).complete(REQ)


def test_openai_error_in_200_body():
    body = {"error": {"message": "Provider returned error", "code": 502}}
    with pytest.raises(ServerError):
        _groq(_mock(200, body)).complete(REQ)


def test_openai_errors():
    with pytest.raises(AuthError):
        _groq(_mock(401, {"error": {"message": "Invalid API Key"}})).complete(REQ)
    with pytest.raises(ServerError):
        _groq(_mock(500, {"error": {"message": "internal"}})).complete(REQ)
    with pytest.raises(BadRequestError):
        _groq(_mock(400, {"error": {"message": "model decommissioned"}})).complete(REQ)


def test_openai_null_content_and_missing_usage():
    body = {"choices": [{"message": {"content": None}, "finish_reason": "length"}]}
    r = _groq(_mock(200, body)).complete(REQ)
    assert r.text == "" and r.usage.estimated


def test_timeout_mapped_without_url():
    def boom(request):
        raise httpx.ConnectTimeout("timed out", request=request)

    with pytest.raises(LLMTimeoutError) as ei:
        _gemini(httpx.MockTransport(boom)).complete(REQ)
    assert KEY not in str(ei.value) and "googleapis" not in str(ei.value)
    assert ei.value.__cause__ is None and ei.value.__suppress_context__


def test_missing_key_rejected():
    with pytest.raises(AuthError):
        GeminiProvider(model_id="m", api_key="")
    with pytest.raises(AuthError):
        OpenAICompatProvider(name="g", model_id="m", base_url="http://x", api_key="")
