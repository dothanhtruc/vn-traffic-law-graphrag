from __future__ import annotations

import pytest
from pydantic import BaseModel

from trafficlaw.llm.client import LLMClient
from trafficlaw.llm.rate_limiter import RateLimiter
from trafficlaw.llm.retry import RetryPolicy


class FakeClock:
    """Đồng hồ giả: ``sleep`` chỉ cộng thời gian, ghi lại các lần chờ."""

    def __init__(self, t: float = 1000.0, wall: float = 1_793_000_000.0) -> None:
        self.t = t
        self.wall_t = wall
        self.sleeps: list[float] = []

    def __call__(self) -> float:
        return self.t

    def wall(self) -> float:
        return self.wall_t

    def sleep(self, s: float) -> None:
        self.sleeps.append(s)
        self.t += s
        self.wall_t += s


class Answer(BaseModel):
    answer: str
    citations: list[str]
    numbers: list[int] = []


@pytest.fixture
def clock() -> FakeClock:
    return FakeClock()


@pytest.fixture
def make_client(clock: FakeClock):
    def _make(provider, *, cache=None, limiter: RateLimiter | None = None, **retry_kw):
        retry = RetryPolicy(sleep=clock.sleep, **retry_kw)
        return LLMClient(provider, params={"temperature": 0}, retry=retry, cache=cache,
                         limiter=limiter, timer=clock)  # fmt: skip

    return _make
