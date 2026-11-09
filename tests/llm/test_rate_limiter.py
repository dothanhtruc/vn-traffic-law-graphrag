from __future__ import annotations

import pytest

from trafficlaw.llm.providers.fake import FakeClient, ok, rate_limit
from trafficlaw.llm.rate_limiter import DailyUsageStore, RateLimiter
from trafficlaw.llm.types import QuotaExhaustedError


def _lim(clock, **kw):
    return RateLimiter("p:m", clock=clock, wall=clock.wall, sleep=clock.sleep, **kw)


def test_rpm_blocks_third_request(clock):
    lim = _lim(clock, rpm=2)
    assert lim.acquire() == 0 and lim.acquire() == 0
    waited = lim.acquire()
    assert waited == pytest.approx(30.0)  # 2/phút → 1 request mỗi 30 s
    assert clock.sleeps == [pytest.approx(30.0)]


def test_rpm_refills_over_time(clock):
    lim = _lim(clock, rpm=2)
    lim.acquire()
    lim.acquire()
    clock.t += 60
    assert lim.acquire() == 0


def test_tpm_blocks_and_record_adjusts(clock):
    lim = _lim(clock, tpm=600)  # 10 token/s
    assert lim.acquire(500) == 0
    assert lim.acquire(200) == pytest.approx(10.0)  # thiếu 100 token
    # usage thật lớn hơn ước tính 300 → bucket âm, lần sau chờ lâu hơn
    lim.record(500, 200)
    assert lim.acquire(100) == pytest.approx(40.0)


def test_tpm_request_larger_than_capacity_does_not_deadlock(clock):
    lim = _lim(clock, tpm=100)
    assert lim.acquire(10_000) == 0  # chỉ đòi tối đa dung lượng bucket


def test_rpd_exhausted_raises(clock):
    lim = _lim(clock, rpd=2)
    lim.acquire()
    lim.acquire()
    with pytest.raises(QuotaExhaustedError, match="2/2"):
        lim.acquire()


def test_tpd_exhausted_raises(clock):
    lim = _lim(clock, tpd=1000)
    lim.acquire(900)
    with pytest.raises(QuotaExhaustedError):
        lim.acquire(200)


def test_rpd_persists_across_restart(clock, tmp_path):
    db = tmp_path / "usage.sqlite"
    lim = _lim(clock, rpd=3, store=DailyUsageStore(db))
    lim.acquire(10)
    lim.acquire(10)
    lim.store.close()
    lim2 = _lim(clock, rpd=3, store=DailyUsageStore(db))
    assert lim2.usage_today() == (2, 20)
    lim2.acquire()
    with pytest.raises(QuotaExhaustedError):
        lim2.acquire()


def test_rpd_resets_on_new_quota_day(clock):
    lim = _lim(clock, rpd=1, reset_utc_offset_h=-8)
    clock.wall_t = 1_793_000_000.0 + 2 * 3600  # 2026-10-26 09:33 UTC → ngày quota 26/10 (UTC−8)
    assert lim.day() == "2026-10-26"
    lim.acquire()
    with pytest.raises(QuotaExhaustedError):
        lim.acquire()
    clock.wall_t += 24 * 3600
    assert lim.day() == "2026-10-27"
    lim.acquire()


def test_reset_offset_changes_day(clock):
    clock.wall_t = 1_793_000_000.0 - 4.5 * 3600  # 2026-10-26 03:03 UTC
    assert _lim(clock, reset_utc_offset_h=0).day() == "2026-10-26"
    assert _lim(clock, reset_utc_offset_h=-8).day() == "2026-10-25"


def test_scopes_are_separate(clock):
    store = DailyUsageStore(None)
    a = RateLimiter("gemini:a", rpd=1, store=store, wall=clock.wall)
    b = RateLimiter("gemini:b", rpd=1, store=store, wall=clock.wall)
    a.acquire()
    b.acquire()  # model khác → quota riêng


def test_client_counts_every_sent_request(make_client, clock):
    lim = _lim(clock, rpd=10)
    fake = FakeClient([rate_limit(), ok("x")])
    make_client(fake, limiter=lim).generate([{"role": "user", "content": "abcdabcd"}])
    assert lim.usage_today()[0] == 2  # request bị 429 vẫn tính


def test_client_local_quota_stops_before_sending(make_client, clock):
    lim = _lim(clock, rpd=1)
    fake = FakeClient([ok("x")])
    c = make_client(fake, limiter=lim)
    c.generate([{"role": "user", "content": "a"}])
    with pytest.raises(QuotaExhaustedError):
        c.generate([{"role": "user", "content": "b"}])
    assert fake.n_calls == 1
