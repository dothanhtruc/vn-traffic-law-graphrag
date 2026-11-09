"""Provider Gemini qua REST ``v1beta/models/{model}:generateContent`` (httpx, không SDK).

- API key gửi bằng header ``x-goog-api-key`` (không để ``?key=`` trong URL: URL có thể xuất hiện
  trong exception/log).
- Tin nhắn ``system`` → ``systemInstruction``; ``assistant`` → role ``model``.
- JSON: ``responseMimeType=application/json`` + ``responseJsonSchema`` (khi có schema).
- ``thinking_budget`` (Gemini 2.5) / ``thinking_level`` (Gemini 3.x: ``minimal|low|medium|high``)
  (params) → ``thinkingConfig``; bỏ phần ``thought`` khỏi text.
- Lỗi 429 ``RESOURCE_EXHAUSTED``: ``quotaId`` chứa ``PerDay`` → ``QuotaExhaustedError``; còn lại →
  ``RateLimitError`` với ``retry_after`` từ ``RetryInfo.retryDelay``.
  ``API_KEY_INVALID`` → ``AuthError``.
"""

from __future__ import annotations

from typing import Any

import httpx

from trafficlaw.llm.providers.base import estimate_tokens, parse_retry_after, safe_json, send, short
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

_PARAM_MAP = {
    "temperature": "temperature",
    "top_p": "topP",
    "max_output_tokens": "maxOutputTokens",
    "seed": "seed",
}
_OK_FINISH = {None, "STOP", "MAX_TOKENS", "FINISH_REASON_UNSPECIFIED"}


def _duration_s(value: Any) -> float | None:
    """``"23s"`` / ``"1.5s"`` → giây."""
    if not isinstance(value, str) or not value.endswith("s"):
        return None
    try:
        return float(value[:-1])
    except ValueError:
        return None


def classify_error(provider: str, status: int, body: dict[str, Any], headers: Any) -> LLMError:
    err = body.get("error") if isinstance(body.get("error"), dict) else {}
    msg = str(err.get("message") or "")
    details = err.get("details") or []
    quota_ids: list[str] = []
    reasons: list[str] = []
    retry_after: float | None = None
    for d in details if isinstance(details, list) else []:
        if not isinstance(d, dict):
            continue
        typ = str(d.get("@type", ""))
        if typ.endswith("QuotaFailure"):
            for v in d.get("violations") or []:
                quota_ids.append(str(v.get("quotaId", "")))
        elif typ.endswith("RetryInfo"):
            retry_after = _duration_s(d.get("retryDelay"))
        elif typ.endswith("ErrorInfo"):
            reasons.append(str(d.get("reason", "")))
    text = f"HTTP {status} {err.get('status', '')}: {short(msg) or 'không có message'}"
    if status in (401, 403) or "API_KEY_INVALID" in reasons:
        return AuthError(text, provider=provider, status_code=status)
    if status == 429:
        if any("PerDay" in q for q in quota_ids):
            return QuotaExhaustedError(text, provider=provider, status_code=status)
        retry_after = retry_after or parse_retry_after(headers.get("retry-after"))
        return RateLimitError(text, provider=provider, status_code=status, retry_after=retry_after)
    if status >= 500:
        return ServerError(text, provider=provider, status_code=status)
    return BadRequestError(text, provider=provider, status_code=status)


class GeminiProvider:
    def __init__(
        self,
        *,
        model_id: str,
        api_key: str,
        base_url: str = "https://generativelanguage.googleapis.com/v1beta",
        timeout_s: float = 60.0,
        json_mode: str = "schema",
        name: str = "gemini",
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        if not api_key:
            raise AuthError(f"{name}: thiếu API key", provider=name)
        self.name = name
        self.model_id = model_id
        self.json_mode = json_mode
        self._http = httpx.Client(
            base_url=base_url.rstrip("/") + "/",
            headers={"x-goog-api-key": api_key},
            timeout=timeout_s,
            transport=transport,
        )

    def __repr__(self) -> str:
        return f"GeminiProvider(model_id={self.model_id!r})"

    def close(self) -> None:
        self._http.close()

    def build_body(self, request: LLMRequest) -> dict[str, Any]:
        system = [m.content for m in request.messages if m.role == "system"]
        contents = [
            {"role": "model" if m.role == "assistant" else "user", "parts": [{"text": m.content}]}
            for m in request.messages
            if m.role != "system"
        ]
        body: dict[str, Any] = {"contents": contents}
        if system:
            body["systemInstruction"] = {"parts": [{"text": "\n\n".join(system)}]}
        gen: dict[str, Any] = {}
        for k, v in request.params.items():
            if k in _PARAM_MAP and v is not None:
                gen[_PARAM_MAP[k]] = v
        thinking: dict[str, Any] = {}
        if request.params.get("thinking_budget") is not None:
            thinking["thinkingBudget"] = int(request.params["thinking_budget"])
        if request.params.get("thinking_level") is not None:
            thinking["thinkingLevel"] = str(request.params["thinking_level"])
        if thinking:
            gen["thinkingConfig"] = thinking
        if request.json_output and self.json_mode != "none":
            gen["responseMimeType"] = "application/json"
            if self.json_mode == "schema" and request.json_schema is not None:
                gen["responseJsonSchema"] = request.json_schema
        if gen:
            body["generationConfig"] = gen
        return body

    def complete(self, request: LLMRequest) -> ProviderResponse:
        url = f"models/{self.model_id}:generateContent"
        resp = send(self._http, "POST", url, provider=self.name, json=self.build_body(request))
        data = safe_json(resp)
        if resp.status_code != 200:
            raise classify_error(self.name, resp.status_code, data, resp.headers)
        return parse_response(self.name, data, request)

    def list_models(self) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        token: str | None = None
        while True:
            params: dict[str, Any] = {"pageSize": 1000}
            if token:
                params["pageToken"] = token
            resp = send(self._http, "GET", "models", provider=self.name, params=params)
            data = safe_json(resp)
            if resp.status_code != 200:
                raise classify_error(self.name, resp.status_code, data, resp.headers)
            out.extend(data.get("models") or [])
            token = data.get("nextPageToken")
            if not token:
                return out


def parse_response(provider: str, data: dict[str, Any], request: LLMRequest) -> ProviderResponse:
    candidates = data.get("candidates") or []
    if not candidates:
        block = (data.get("promptFeedback") or {}).get("blockReason")
        raise BadRequestError(f"không có candidate (blockReason={block})", provider=provider)
    cand = candidates[0]
    parts = (cand.get("content") or {}).get("parts") or []
    text = "".join(p.get("text", "") for p in parts if isinstance(p, dict) and not p.get("thought"))
    finish = cand.get("finishReason")
    if not text and finish not in _OK_FINISH:
        raise BadRequestError(f"phản hồi rỗng (finishReason={finish})", provider=provider)
    um = data.get("usageMetadata") or {}
    if um.get("promptTokenCount") is not None:
        completion = int(um.get("candidatesTokenCount") or 0) + int(
            um.get("thoughtsTokenCount") or 0
        )
        usage = Usage(
            prompt_tokens=int(um["promptTokenCount"]),
            completion_tokens=completion,
            total_tokens=int(um.get("totalTokenCount") or 0),
        )
    else:
        p = sum(estimate_tokens(m.content) for m in request.messages)
        c = estimate_tokens(text)
        usage = Usage(prompt_tokens=p, completion_tokens=c, total_tokens=p + c, estimated=True)
    return ProviderResponse(text=text, usage=usage, finish_reason=finish)
