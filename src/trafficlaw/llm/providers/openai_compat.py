"""Provider OpenAI-compatible ``/chat/completions`` (Groq, OpenRouter) qua httpx.

Phân loại lỗi:

- 401/403 → ``AuthError``; 402 (OpenRouter hết credit) → ``QuotaExhaustedError``.
- 429 có dấu hiệu theo ngày ("per day", RPD/TPD, ``free-models-per-day``, "daily") →
  ``QuotaExhaustedError``; còn lại → ``RateLimitError`` với ``retry_after`` từ header
  ``Retry-After`` hoặc câu "try again in 7.66s" (Groq).
- 5xx → ``ServerError``; 4xx khác → ``BadRequestError``.
- OpenRouter đôi khi trả HTTP 200 kèm ``{"error": {"code": 429, …}}`` → phân loại theo ``code``.
"""

from __future__ import annotations

import re
from typing import Any

import httpx

from trafficlaw.llm.providers.base import estimate_tokens, safe_json, send, short
from trafficlaw.llm.providers.base import parse_retry_after as _parse_retry_after
from trafficlaw.llm.types import (
    AuthError,
    BadRequestError,
    LLMError,
    LLMRequest,
    ProviderResponse,
    QuotaExhaustedError,
    RateLimitError,
    ServerError,
    Usage,
)

_DAILY_RE = re.compile(
    r"per[ -]day|\bRPD\b|\bTPD\b|per-day|daily|free-models-per-day", re.IGNORECASE
)
_TRY_AGAIN_RE = re.compile(r"try again in\s+(?:(\d+)m)?\s*([\d.]+)\s*(ms|s)?", re.IGNORECASE)

# params chung → tên tham số OpenAI
_PARAM_MAP = {
    "temperature": "temperature",
    "top_p": "top_p",
    "max_output_tokens": "max_tokens",
    "seed": "seed",
}


def _retry_after_from_message(msg: str) -> float | None:
    m = _TRY_AGAIN_RE.search(msg)
    if not m:
        return None
    minutes = float(m[1]) if m[1] else 0.0
    value = float(m[2])
    if (m[3] or "s").lower() == "ms":
        value /= 1000
    return minutes * 60 + value


def classify_error(
    provider: str, status: int, body: dict[str, Any], headers: httpx.Headers | dict
) -> LLMError:
    err = body.get("error") if isinstance(body.get("error"), dict) else {}
    msg = str(err.get("message") or body.get("message") or "")
    # OpenRouter: chi tiết của provider gốc nằm trong metadata.raw
    raw = (err.get("metadata") or {}).get("raw") if isinstance(err.get("metadata"), dict) else None
    full = f"{msg} {raw or ''}"
    text = f"HTTP {status}: {short(msg) or 'không có message'}"
    if status in (401, 403):
        return AuthError(text, provider=provider, status_code=status)
    if status == 402:
        return QuotaExhaustedError(text, provider=provider, status_code=status)
    if status == 429:
        if _DAILY_RE.search(full):
            return QuotaExhaustedError(text, provider=provider, status_code=status)
        retry_after = _parse_retry_after(headers.get("retry-after")) or _retry_after_from_message(
            full
        )
        return RateLimitError(text, provider=provider, status_code=status, retry_after=retry_after)
    if status >= 500:
        return ServerError(text, provider=provider, status_code=status)
    return BadRequestError(text, provider=provider, status_code=status)


class OpenAICompatProvider:
    """Groq / OpenRouter. ``json_mode``: ``schema`` | ``object`` | ``none``."""

    def __init__(
        self,
        *,
        name: str,
        model_id: str,
        base_url: str,
        api_key: str,
        timeout_s: float = 60.0,
        json_mode: str = "object",
        extra_headers: dict[str, str] | None = None,
        extra_body: dict[str, Any] | None = None,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        if not api_key:
            raise AuthError(f"{name}: thiếu API key", provider=name)
        self.name = name
        self.model_id = model_id
        self.json_mode = json_mode
        self.extra_body = dict(extra_body or {})
        headers = {"Authorization": f"Bearer {api_key}", **(extra_headers or {})}
        self._http = httpx.Client(
            base_url=base_url.rstrip("/") + "/",
            headers=headers,
            timeout=timeout_s,
            transport=transport,
        )

    def __repr__(self) -> str:  # không lộ header/key
        return f"OpenAICompatProvider(name={self.name!r}, model_id={self.model_id!r})"

    def close(self) -> None:
        self._http.close()

    # ------------------------------------------------------------------ request body
    def build_body(self, request: LLMRequest) -> dict[str, Any]:
        body: dict[str, Any] = {
            "model": self.model_id,
            "messages": [{"role": m.role, "content": m.content} for m in request.messages],
        }
        for k, v in request.params.items():
            if k in _PARAM_MAP and v is not None:
                body[_PARAM_MAP[k]] = v
        if request.json_output and self.json_mode != "none":
            if self.json_mode == "schema" and request.json_schema is not None:
                body["response_format"] = {
                    "type": "json_schema",
                    "json_schema": {"name": "response", "schema": request.json_schema},
                }
            else:
                body["response_format"] = {"type": "json_object"}
        body.update(self.extra_body)
        return body

    # ------------------------------------------------------------------ gọi
    def complete(self, request: LLMRequest) -> ProviderResponse:
        resp = send(
            self._http,
            "POST",
            "chat/completions",
            provider=self.name,
            json=self.build_body(request),
        )
        data = safe_json(resp)
        if resp.status_code != 200:
            raise classify_error(self.name, resp.status_code, data, resp.headers)
        if isinstance(data.get("error"), dict) and not data.get("choices"):
            code = data["error"].get("code")
            status = code if isinstance(code, int) else 500
            raise classify_error(self.name, status, data, resp.headers)
        return parse_response(self.name, data, request)

    def list_models(self) -> list[dict[str, Any]]:
        resp = send(self._http, "GET", "models", provider=self.name)
        data = safe_json(resp)
        if resp.status_code != 200:
            raise classify_error(self.name, resp.status_code, data, resp.headers)
        return list(data.get("data") or [])


def parse_response(provider: str, data: dict[str, Any], request: LLMRequest) -> ProviderResponse:
    choices = data.get("choices") or []
    if not choices:
        raise ServerError("phản hồi không có choices", provider=provider)
    choice = choices[0]
    text = (choice.get("message") or {}).get("content") or ""
    u = data.get("usage") or {}
    if u.get("prompt_tokens") is not None:
        usage = Usage(
            prompt_tokens=int(u.get("prompt_tokens") or 0),
            completion_tokens=int(u.get("completion_tokens") or 0),
            total_tokens=int(u.get("total_tokens") or 0),
        )
    else:
        p = sum(estimate_tokens(m.content) for m in request.messages)
        c = estimate_tokens(text)
        usage = Usage(prompt_tokens=p, completion_tokens=c, total_tokens=p + c, estimated=True)
    return ProviderResponse(text=text, usage=usage, finish_reason=choice.get("finish_reason"))
