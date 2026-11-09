"""``LLMClient``: provider + cache + rate limiter + retry + JSON mode; ``FallbackClient`` (demo).

Luồng ``generate``:

1. Cache (khoá ``cache.cache_key``) trúng → trả kết quả gốc với ``cached=True``.
2. Mỗi lượt HTTP: ``limiter.acquire(ước tính token prompt)`` (RPM/TPM chờ; RPD/TPD hết →
   ``QuotaExhaustedError``), rồi ``provider.complete``; lỗi 429/5xx/timeout → backoff (``retry``).
3. Có yêu cầu JSON: parse/validate (``json_mode``); lỗi → gọi lại **đúng 1 lần** với hội thoại
   + phản hồi lỗi + prompt ``format_repair``; vẫn lỗi → ``status = format_error``.
4. ``ok`` → lưu cache; ``limiter.record`` bù usage thật.

``generate`` không ném lỗi, trừ ``QuotaExhaustedError`` (job phải dừng sạch rồi chạy lại sau):
hết retry / lỗi khác → ``LLMResult(status="error")``. ``latency_ms`` = tổng thời gian trong các
lượt HTTP (không gồm thời gian chờ rate limit/backoff); ``usage`` = tổng usage các lượt thành công.

``FallbackClient`` chỉ dùng cho demo: thử lần lượt các client (Gemini → Groq → OpenRouter), trả kết
quả ``ok`` đầu tiên kèm ``fallback_from``. Đánh giá **không** dùng fallback.
"""

from __future__ import annotations

import json
import logging
import os
import time
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import Any

import httpx

from trafficlaw.llm import json_mode
from trafficlaw.llm.cache import LLMCache, cache_key
from trafficlaw.llm.config import LLMConfig
from trafficlaw.llm.prompt_loader import Prompt, load_prompt
from trafficlaw.llm.providers.base import Provider, estimate_tokens
from trafficlaw.llm.rate_limiter import DailyUsageStore, RateLimiter
from trafficlaw.llm.retry import RetryPolicy, call_with_retry
from trafficlaw.llm.types import (
    AuthError,
    FormatError,
    LLMError,
    LLMRequest,
    LLMResult,
    Message,
    ProviderResponse,
    QuotaExhaustedError,
    Usage,
)

logger = logging.getLogger(__name__)

MessageLike = Message | dict[str, str]


def to_messages(messages: Sequence[MessageLike]) -> list[Message]:
    return [m if isinstance(m, Message) else Message.model_validate(m) for m in messages]


def _add_usage(a: Usage, b: Usage) -> Usage:
    return Usage(
        prompt_tokens=a.prompt_tokens + b.prompt_tokens,
        completion_tokens=a.completion_tokens + b.completion_tokens,
        total_tokens=a.total_tokens + b.total_tokens,
        estimated=a.estimated or b.estimated,
    )


class LLMClient:
    def __init__(
        self,
        provider: Provider,
        *,
        params: dict[str, Any] | None = None,
        limiter: RateLimiter | None = None,
        retry: RetryPolicy | None = None,
        cache: LLMCache | None = None,
        repair_prompt: Prompt | None = None,
        timer: Callable[[], float] = time.perf_counter,
    ) -> None:
        self.provider = provider
        self.params = dict(params or {})
        self.limiter = limiter
        self.retry = retry or RetryPolicy()
        self.cache = cache
        self.repair_prompt = repair_prompt or load_prompt("format_repair")
        self.timer = timer

    @property
    def model_id(self) -> str:
        return self.provider.model_id

    @property
    def provider_name(self) -> str:
        return self.provider.name

    def __repr__(self) -> str:
        return f"LLMClient({self.provider_name}:{self.model_id})"

    # ------------------------------------------------------------------ một lượt (có retry)
    def _call(self, request: LLMRequest) -> tuple[ProviderResponse, int, float]:
        est = sum(estimate_tokens(m.content) for m in request.messages)
        elapsed = [0.0]

        def attempt() -> ProviderResponse:
            t0 = self.timer()
            try:
                return self.provider.complete(request)
            finally:
                elapsed[0] += self.timer() - t0

        on_attempt = (lambda: self.limiter.acquire(est)) if self.limiter else None
        try:
            resp, outcome = call_with_retry(attempt, self.retry, on_attempt=on_attempt)
        except LLMError as e:
            e.elapsed = elapsed[0]  # type: ignore[attr-defined]
            raise
        if self.limiter is not None:
            self.limiter.record(resp.usage.total_tokens, est)
        return resp, outcome.attempts, elapsed[0]

    # ------------------------------------------------------------------ API chính
    def generate(
        self,
        messages: Sequence[MessageLike],
        *,
        json_schema: json_mode.JsonSchemaArg = None,
        json_output: bool | None = None,
        params: dict[str, Any] | None = None,
        use_cache: bool = True,
    ) -> LLMResult:
        """``json_schema``: lớp pydantic (validate đầy đủ) hoặc dict JSON Schema (chỉ gửi API,
        kiểm tra là object). ``json_output`` mặc định = có ``json_schema``."""
        msgs = to_messages(messages)
        want_json = json_schema is not None if json_output is None else json_output
        request = LLMRequest(
            messages=msgs,
            params={**self.params, **(params or {})},
            json_schema=json_mode.schema_dict(json_schema),
            json_output=want_json,
        )
        key = cache_key(self.provider_name, self.model_id, request)
        if self.cache is not None and use_cache:
            hit = self.cache.get(key)
            if hit is not None:
                return hit

        base = {"model_id": self.model_id, "provider": self.provider_name}
        attempts = 0
        latency = 0.0
        usage = Usage()
        try:
            resp, n, dt = self._call(request)
            attempts, latency, usage = n, dt, resp.usage
            text, parsed, status, error, repair_hash = resp.text, None, "ok", None, None
            if want_json:
                try:
                    parsed = json_mode.parse(resp.text, json_schema)
                except FormatError as fe:
                    logger.warning("%r: lỗi định dạng (%s) → gọi lại sửa định dạng", self, fe)
                    repair_hash = self.repair_prompt.hash
                    repair_req = request.model_copy(
                        update={"messages": [*msgs, *self._repair_messages(resp.text, fe, request)]}
                    )
                    resp2, n2, dt2 = self._call(repair_req)
                    attempts += n2
                    latency += dt2
                    usage = _add_usage(usage, resp2.usage)
                    text = resp2.text
                    try:
                        parsed = json_mode.parse(resp2.text, json_schema)
                    except FormatError as fe2:
                        status, error = "format_error", str(fe2)
            result = LLMResult(
                **base,
                text=text,
                parsed=parsed,
                usage=usage,
                latency_ms=round(latency * 1000),
                status=status,
                attempts=attempts,
                error=error,
                repair_prompt_hash=repair_hash,
            )
        except QuotaExhaustedError as e:
            logger.error("%r: %s. %s", self, e, e.resume_hint)
            raise
        except LLMError as e:
            attempts += getattr(e, "attempts", 1)
            latency += getattr(e, "elapsed", 0.0)
            result = LLMResult(
                **base,
                usage=usage,
                latency_ms=round(latency * 1000),
                status="error",
                attempts=attempts,
                error=f"{type(e).__name__}: {e}",
            )
            logger.warning("%r: lỗi sau %d lượt: %s", self, attempts, result.error)
        if self.cache is not None and result.status == "ok":
            self.cache.put(key, result)
        return result

    def _repair_messages(
        self, bad_text: str, err: FormatError, request: LLMRequest
    ) -> list[Message]:
        schema = request.json_schema or {"type": "object"}
        prompt = self.repair_prompt.render(
            error=str(err), schema=json.dumps(schema, ensure_ascii=False, indent=2)
        )
        return [Message(role="assistant", content=bad_text), Message(role="user", content=prompt)]


class FallbackClient:
    """Chỉ cho demo: thử lần lượt; kết quả ghi rõ provider/model đã trả lời + ``fallback_from``."""

    def __init__(self, clients: Sequence[LLMClient]) -> None:
        if not clients:
            raise ValueError("FallbackClient cần ít nhất một client")
        self.clients = list(clients)

    def generate(self, messages: Sequence[MessageLike], **kw: Any) -> LLMResult:
        tried: list[str] = []
        last: LLMResult | None = None
        for c in self.clients:
            name = f"{c.provider_name}:{c.model_id}"
            try:
                r = c.generate(messages, **kw)
            except QuotaExhaustedError as e:
                tried.append(name)
                last = LLMResult(
                    model_id=c.model_id,
                    provider=c.provider_name,
                    status="error",
                    error=f"QuotaExhaustedError: {e}",
                )
                continue
            if r.status == "ok":
                if tried:
                    logger.info("fallback: %s trả lời (sau %s)", name, ", ".join(tried))
                return r.model_copy(update={"fallback_from": tried})
            tried.append(name)
            last = r
        assert last is not None
        return last.model_copy(update={"fallback_from": tried[:-1]})


# --------------------------------------------------------------------------- dựng từ config


class _Shared:
    """Cache + bộ đếm ngày dùng chung giữa các client dựng từ cùng config."""

    def __init__(self, cfg: LLMConfig, root: Path, use_cache: bool) -> None:
        self.cache = LLMCache(root / cfg.cache_path) if (use_cache and cfg.cache_path) else None
        self.usage = DailyUsageStore(root / cfg.usage_db_path if cfg.usage_db_path else None)


def has_key(cfg: LLMConfig, provider: str) -> bool:
    return bool(os.environ.get(cfg.providers[provider].api_key_env))


def make_provider(
    cfg: LLMConfig,
    provider: str,
    model_id: str | None = None,
    *,
    transport: httpx.BaseTransport | None = None,
) -> Provider:
    from trafficlaw.llm.providers.gemini import GeminiProvider
    from trafficlaw.llm.providers.openai_compat import OpenAICompatProvider

    pc = cfg.providers[provider]
    mid = model_id or pc.model_id
    if not mid:
        raise ValueError(f"{provider}: chưa chốt model_id trong configs/llm.yaml")
    key = os.environ.get(pc.api_key_env, "")
    if not key:
        raise AuthError(f"{provider}: thiếu biến môi trường {pc.api_key_env}", provider=provider)
    common = {"model_id": mid, "api_key": key, "base_url": pc.base_url}
    common |= {"timeout_s": pc.timeout_s, "json_mode": pc.json_mode, "transport": transport}
    if pc.kind == "gemini":
        return GeminiProvider(name=provider, **common)
    return OpenAICompatProvider(
        name=provider, extra_headers=pc.extra_headers, extra_body=pc.extra_body, **common
    )


def build_client(
    cfg: LLMConfig,
    provider: str | None = None,
    *,
    model_id: str | None = None,
    root: str | Path = ".",
    use_cache: bool = True,
    transport: httpx.BaseTransport | None = None,
    sleep: Callable[[float], None] = time.sleep,
    _shared: _Shared | None = None,
) -> LLMClient:
    """Client cho ``provider`` (mặc định ``main``: dùng ``main.model_id``)."""
    name = provider or cfg.main.provider
    if model_id is None and name == cfg.main.provider:
        model_id = cfg.main.model_id
    shared = _shared or _Shared(cfg, Path(root), use_cache)
    prov = make_provider(cfg, name, model_id, transport=transport)
    pc = cfg.providers[name]
    limiter = RateLimiter(
        f"{name}:{prov.model_id}",
        rpm=pc.rpm,
        tpm=pc.tpm,
        rpd=pc.rpd,
        tpd=pc.tpd,
        store=shared.usage,
        reset_utc_offset_h=pc.reset_utc_offset_h,
        sleep=sleep,
    )
    r = cfg.retry
    retry = RetryPolicy(r.max_retries, r.base_s, r.cap_s, r.seed, sleep=sleep)
    return LLMClient(
        prov,
        params=cfg.params_for(name),
        limiter=limiter,
        retry=retry,
        cache=shared.cache,
        repair_prompt=load_prompt(cfg.repair_prompt),
    )


def build_fallback_client(
    cfg: LLMConfig, *, root: str | Path = ".", use_cache: bool = True, **kw: Any
) -> FallbackClient:
    """Demo: client main trước, rồi các provider trong ``fallback_order`` có key."""
    shared = _Shared(cfg, Path(root), use_cache)
    clients = (
        [build_client(cfg, root=root, _shared=shared, **kw)]
        if has_key(cfg, cfg.main.provider)
        else []
    )
    for name in cfg.fallback_order:
        if name != cfg.main.provider and has_key(cfg, name):
            clients.append(build_client(cfg, name, root=root, _shared=shared, **kw))
    return FallbackClient(clients)
