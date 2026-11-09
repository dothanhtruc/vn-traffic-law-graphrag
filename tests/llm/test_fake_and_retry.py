from __future__ import annotations

import pytest

from tests.llm.conftest import Answer
from trafficlaw.llm.providers.fake import (
    FakeClient,
    auth_error,
    bad_json,
    ok,
    quota_exhausted,
    rate_limit,
    server_error,
    timeout,
)
from trafficlaw.llm.retry import RetryPolicy
from trafficlaw.llm.types import QuotaExhaustedError

MSG = [{"role": "user", "content": "Mức phạt? Trả lời JSON."}]
GOOD = '{"answer": "Phạt tiền", "citations": ["ND168-2024/D6/K4/a"], "numbers": [800000]}'


# ------------------------------------------------------------------ FakeClient: 5 kịch bản
def test_fake_ok(make_client):
    r = make_client(FakeClient([ok(GOOD)])).generate(MSG, json_schema=Answer)
    assert r.status == "ok" and r.attempts == 1
    assert r.parsed["citations"] == ["ND168-2024/D6/K4/a"]
    assert r.provider == "fake" and r.model_id == "fake-model"


def test_fake_429_then_ok(make_client, clock):
    fake = FakeClient([rate_limit(), rate_limit(), ok(GOOD)])
    r = make_client(fake).generate(MSG, json_schema=Answer)
    assert r.status == "ok" and r.attempts == 3 and fake.n_calls == 3
    assert len(clock.sleeps) == 2


def test_fake_500_six_times_error_after_five_retries(make_client, clock):
    fake = FakeClient([server_error()] * 6 + [ok(GOOD)])
    r = make_client(fake).generate(MSG, json_schema=Answer)
    assert r.status == "error" and "ServerError" in r.error
    assert fake.n_calls == 6 and r.attempts == 6  # 1 + 5 retry
    assert len(clock.sleeps) == 5


def test_fake_quota_raises_and_stops(make_client, clock):
    fake = FakeClient([quota_exhausted(), ok(GOOD)])
    with pytest.raises(QuotaExhaustedError) as ei:
        make_client(fake).generate(MSG)
    assert fake.n_calls == 1 and clock.sleeps == []
    assert "chạy lại" in ei.value.resume_hint


def test_fake_bad_json_repaired(make_client):
    fake = FakeClient([bad_json(), ok(GOOD)])
    r = make_client(fake).generate(MSG, json_schema=Answer)
    assert r.status == "ok" and r.attempts == 2 and r.repair_prompt_hash
    repair = fake.requests[1].messages
    assert repair[-2].role == "assistant" and repair[-2].content == bad_json().text
    assert "không đúng định dạng" in repair[-1].content


def test_timeout_retried_auth_not(make_client):
    r = make_client(FakeClient([timeout(), ok("xin chào")])).generate(MSG)
    assert r.status == "ok" and r.attempts == 2 and r.text == "xin chào" and r.parsed is None
    fake = FakeClient([auth_error(), ok(GOOD)])
    r = make_client(fake).generate(MSG)
    assert r.status == "error" and fake.n_calls == 1 and "AuthError" in r.error


def test_fake_requires_script():
    with pytest.raises(ValueError):
        FakeClient([])
    f = FakeClient([ok("a")], repeat_last=False)
    from trafficlaw.llm.types import LLMRequest, Message

    req = LLMRequest(messages=[Message(role="user", content="x")])
    f.complete(req)
    with pytest.raises(AssertionError):
        f.complete(req)


# ------------------------------------------------------------------ retry policy
def test_retry_after_respected(make_client, clock):
    r = make_client(FakeClient([rate_limit(retry_after=7.0), ok(GOOD)])).generate(MSG)
    assert r.status == "ok"
    assert clock.sleeps[0] >= 7.0


def test_jitter_deterministic_with_seed():
    a = RetryPolicy(seed=1)
    b = RetryPolicy(seed=1)
    c = RetryPolicy(seed=2)
    da = [a.delay(n) for n in range(5)]
    assert da == [b.delay(n) for n in range(5)]
    assert da != [c.delay(n) for n in range(5)]
    # full jitter: 0 ≤ d ≤ min(cap, base·2^n)
    for n, d in enumerate(da):
        assert 0 <= d <= min(60.0, 2**n)


def test_backoff_capped():
    p = RetryPolicy(base_s=1.0, cap_s=3.0, seed=0)
    assert all(p.delay(n) <= 3.0 for n in range(10))


def test_latency_recorded_on_error(clock):
    from trafficlaw.llm.client import LLMClient

    class SlowFail(FakeClient):
        def complete(self, request):
            clock.t += 2.0  # mỗi lượt HTTP mất 2 s
            return super().complete(request)

    c = LLMClient(SlowFail([server_error()]), retry=RetryPolicy(max_retries=2, sleep=clock.sleep),
                  timer=clock)  # fmt: skip
    r = c.generate(MSG)
    assert r.status == "error" and r.attempts == 3 and r.latency_ms == 6000


def test_latency_excludes_backoff(make_client, clock):
    r = make_client(FakeClient([rate_limit(retry_after=30), ok(GOOD)])).generate(MSG)
    assert r.latency_ms == 0  # đồng hồ giả chỉ chạy khi sleep → không tính thời gian chờ
