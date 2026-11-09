"""``FakeClient``: provider giả cho test/smoke, phát lần lượt một kịch bản phản hồi.

Ví dụ::

    fake = FakeClient([rate_limit(retry_after=2), server_error(), ok('{"answer": "x"}')])
    client = LLMClient(fake, ...)   # retry/limiter/cache/json_mode chạy như với provider thật

Bước: ``ok`` · ``rate_limit`` (429) · ``server_error`` (500) · ``quota_exhausted`` · ``bad_json``
(text không phải JSON) · ``timeout`` · ``auth_error``. Hết kịch bản → lặp bước cuối
(``repeat_last=True``) hoặc ``AssertionError``. Có thể truyền ``responder(request) -> str``
thay kịch bản.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass

from trafficlaw.llm.providers.base import estimate_tokens
from trafficlaw.llm.types import (
    AuthError,
    LLMRequest,
    LLMTimeoutError,
    ProviderResponse,
    QuotaExhaustedError,
    RateLimitError,
    ServerError,
    Usage,
)


@dataclass(frozen=True)
class FakeStep:
    kind: str
    text: str = ""
    retry_after: float | None = None
    usage: Usage | None = None


def ok(text: str, usage: Usage | None = None) -> FakeStep:
    return FakeStep("ok", text=text, usage=usage)


def bad_json(text: str = '{"answer": "thiếu ngoặc') -> FakeStep:
    return FakeStep("ok", text=text)


def rate_limit(retry_after: float | None = None) -> FakeStep:
    return FakeStep("rate_limit", retry_after=retry_after)


def server_error() -> FakeStep:
    return FakeStep("server_error")


def quota_exhausted() -> FakeStep:
    return FakeStep("quota")


def timeout() -> FakeStep:
    return FakeStep("timeout")


def auth_error() -> FakeStep:
    return FakeStep("auth")


class FakeClient:
    def __init__(
        self,
        script: Sequence[FakeStep] | None = None,
        *,
        responder: Callable[[LLMRequest], str] | None = None,
        name: str = "fake",
        model_id: str = "fake-model",
        repeat_last: bool = True,
    ) -> None:
        if not script and responder is None:
            raise ValueError("FakeClient cần script hoặc responder")
        self.name = name
        self.model_id = model_id
        self.script = list(script or [])
        self.responder = responder
        self.repeat_last = repeat_last
        self.requests: list[LLMRequest] = []
        self._i = 0

    @property
    def n_calls(self) -> int:
        return len(self.requests)

    def _next(self, request: LLMRequest) -> FakeStep:
        if self.responder is not None:
            return ok(self.responder(request))
        if self._i < len(self.script):
            step = self.script[self._i]
            self._i += 1
            return step
        if self.repeat_last:
            return self.script[-1]
        raise AssertionError("FakeClient: hết kịch bản")

    def complete(self, request: LLMRequest) -> ProviderResponse:
        self.requests.append(request)
        step = self._next(request)
        p = self.name
        if step.kind == "rate_limit":
            raise RateLimitError(
                "HTTP 429 (fake)", provider=p, status_code=429, retry_after=step.retry_after
            )
        if step.kind == "server_error":
            raise ServerError("HTTP 500 (fake)", provider=p, status_code=500)
        if step.kind == "quota":
            raise QuotaExhaustedError("HTTP 429 quota/ngày (fake)", provider=p, status_code=429)
        if step.kind == "timeout":
            raise LLMTimeoutError("timeout (fake)", provider=p)
        if step.kind == "auth":
            raise AuthError("HTTP 401 (fake)", provider=p, status_code=401)
        usage = step.usage
        if usage is None:
            pt = sum(estimate_tokens(m.content) for m in request.messages)
            ct = estimate_tokens(step.text)
            usage = Usage(prompt_tokens=pt, completion_tokens=ct, total_tokens=pt + ct)
        return ProviderResponse(text=step.text, usage=usage, finish_reason="stop")
