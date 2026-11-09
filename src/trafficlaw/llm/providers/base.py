"""Interface provider: chỉ HTTP + parse phản hồi, ném lỗi có kiểu (``llm.types``).

Retry, rate limit, cache, JSON mode nằm ở ``llm.client.LLMClient`` — dùng chung cho mọi provider
(kể cả ``FakeClient``), nên test với FakeClient kiểm tra đúng logic chạy thật.
"""

from __future__ import annotations

import json
from typing import Protocol, runtime_checkable

import httpx

from trafficlaw.llm.types import LLMRequest, LLMTimeoutError, ProviderResponse


@runtime_checkable
class Provider(Protocol):
    name: str
    model_id: str

    def complete(self, request: LLMRequest) -> ProviderResponse: ...


def estimate_tokens(text: str) -> int:
    """Ước lượng thô ``len/4`` — chỉ dùng khi API không trả usage hoặc trước khi gọi."""
    return max(1, len(text) // 4) if text else 0


def safe_json(resp: httpx.Response) -> dict:
    try:
        data = resp.json()
    except (json.JSONDecodeError, ValueError):
        return {}
    return data if isinstance(data, dict) else {"_list": data}


def parse_retry_after(value: str | None) -> float | None:
    """Header ``Retry-After`` dạng số giây (dạng ngày HTTP bỏ qua)."""
    if not value:
        return None
    try:
        return max(0.0, float(value.strip()))
    except ValueError:
        return None


def short(text: str, n: int = 300) -> str:
    text = " ".join(text.split())
    return text if len(text) <= n else text[:n] + "…"


def send(client: httpx.Client, method: str, url: str, *, provider: str, **kw) -> httpx.Response:
    """Gửi request; lỗi mạng/timeout → ``LLMTimeoutError`` (không kèm URL/headers trong message)."""
    try:
        return client.request(method, url, **kw)
    except httpx.TimeoutException as e:
        raise LLMTimeoutError(f"timeout ({type(e).__name__})", provider=provider) from None
    except httpx.TransportError as e:
        raise LLMTimeoutError(f"lỗi kết nối ({type(e).__name__})", provider=provider) from None
