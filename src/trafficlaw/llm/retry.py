"""Retry với backoff mũ + full jitter, tôn trọng ``Retry-After``.

Lần chờ thứ n (n = 0, 1, …): ``max(retry_after, U(0, min(cap, base·2^n)))`` với ``U`` lấy từ
``random.Random(seed)`` riêng (tất định khi cùng seed). Chỉ retry lỗi ``retryable`` (429 theo phút,
5xx, timeout); ``QuotaExhaustedError``, ``AuthError``, ``BadRequestError`` ném ra ngay.
"""

from __future__ import annotations

import logging
import random
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TypeVar

from trafficlaw.llm.types import LLMError, RateLimitError

logger = logging.getLogger(__name__)

T = TypeVar("T")


@dataclass
class RetryPolicy:
    max_retries: int = 5
    base_s: float = 1.0
    cap_s: float = 60.0
    seed: int = 42
    sleep: Callable[[float], None] = time.sleep
    _rng: random.Random = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._rng = random.Random(self.seed)

    def delay(self, n: int, err: LLMError | None = None) -> float:
        jitter = self._rng.uniform(0.0, min(self.cap_s, self.base_s * (2**n)))
        retry_after = err.retry_after if isinstance(err, RateLimitError) else None
        return max(retry_after or 0.0, jitter)


@dataclass
class RetryOutcome:
    attempts: int
    delays: list[float]


def call_with_retry(
    fn: Callable[[], T], policy: RetryPolicy, *, on_attempt: Callable[[], None] | None = None
) -> tuple[T, RetryOutcome]:
    """Gọi ``fn`` tối đa ``1 + max_retries`` lần. Lỗi cuối được ném lại, có ``attempts`` gắn vào.

    ``on_attempt`` chạy trước mỗi lần gọi (vd. ``limiter.acquire``) — có thể ném
    ``QuotaExhaustedError``.
    """
    delays: list[float] = []
    attempt = 0
    while True:
        attempt += 1
        try:
            if on_attempt is not None:
                on_attempt()
            return fn(), RetryOutcome(attempt, delays)
        except LLMError as e:
            e.attempts = attempt  # type: ignore[attr-defined]
            e.delays = delays  # type: ignore[attr-defined]
            if not e.retryable or attempt > policy.max_retries:
                raise
            d = policy.delay(attempt - 1, e)
            delays.append(d)
            logger.warning(
                "%s: %s — thử lại %d/%d sau %.1fs",
                e.provider or "llm",
                type(e).__name__,
                attempt,
                policy.max_retries,
                d,
            )
            policy.sleep(d)
