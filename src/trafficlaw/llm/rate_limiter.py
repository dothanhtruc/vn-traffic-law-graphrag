"""Rate limiter theo provider/model: token bucket RPM + TPM, bộ đếm RPD/TPD bền trong SQLite.

- **RPM/TPM**: bucket dung lượng = giới hạn/phút, nạp đều ``limit/60`` mỗi giây. ``acquire(est)``
  chờ (bằng ``sleep`` tiêm vào) đến khi đủ 1 request và ``min(est, tpm)`` token, rồi trừ. Sau khi có
  usage thật, ``record(actual, est)`` bù chênh lệch (bucket có thể âm → lần sau chờ lâu hơn).
- **RPD/TPD**: đếm theo "ngày quota" của provider (``reset_utc_offset_h``: Gemini reset 0h giờ
  Thái Bình Dương ≈ UTC−8, bỏ qua giờ mùa hè; Groq/OpenRouter UTC). Đếm **mỗi request đã gửi**
  (kể cả request bị 429) trong bảng ``usage(scope, day, requests, tokens)`` → không vượt quota qua
  nhiều lần chạy. Vượt → ``QuotaExhaustedError`` *trước khi* gửi. Đây chỉ là ước tính phía mình;
  lỗi quota của server vẫn là nguồn quyết định.
"""

from __future__ import annotations

import logging
import threading
import time
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from pathlib import Path

from trafficlaw.llm import _sqlite
from trafficlaw.llm.types import QuotaExhaustedError

logger = logging.getLogger(__name__)

_SCHEMA = """
CREATE TABLE IF NOT EXISTS usage (
    scope TEXT NOT NULL, day TEXT NOT NULL,
    requests INTEGER NOT NULL DEFAULT 0, tokens INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (scope, day)
);
"""


class DailyUsageStore:
    """Bộ đếm request/token theo ``(scope, day)`` trong SQLite (``None`` → chỉ trong bộ nhớ)."""

    def __init__(self, path: str | Path | None) -> None:
        self._conn = _sqlite.connect(path if path is not None else ":memory:", _SCHEMA)
        self._lock = threading.Lock()

    def get(self, scope: str, day: str) -> tuple[int, int]:
        with self._lock:
            row = self._conn.execute(
                "SELECT requests, tokens FROM usage WHERE scope=? AND day=?", (scope, day)
            ).fetchone()
        return (int(row[0]), int(row[1])) if row else (0, 0)

    def add(self, scope: str, day: str, requests: int = 0, tokens: int = 0) -> None:
        with self._lock:
            self._conn.execute(
                "INSERT INTO usage(scope, day, requests, tokens) VALUES (?, ?, ?, ?) "
                "ON CONFLICT(scope, day) DO UPDATE SET requests = requests + excluded.requests, "
                "tokens = tokens + excluded.tokens",
                (scope, day, requests, tokens),
            )

    def close(self) -> None:
        self._conn.close()


class _Bucket:
    def __init__(self, per_minute: float, now: float) -> None:
        self.capacity = float(per_minute)
        self.rate = per_minute / 60.0
        self.level = self.capacity
        self.t = now

    def refill(self, now: float) -> None:
        self.level = min(self.capacity, self.level + (now - self.t) * self.rate)
        self.t = now

    def wait_for(self, amount: float) -> float:
        need = min(amount, self.capacity) - self.level
        return 0.0 if need <= 0 else need / self.rate


class RateLimiter:
    def __init__(
        self,
        scope: str,
        *,
        rpm: int | None = None,
        tpm: int | None = None,
        rpd: int | None = None,
        tpd: int | None = None,
        store: DailyUsageStore | None = None,
        reset_utc_offset_h: float = 0.0,
        clock: Callable[[], float] = time.monotonic,
        wall: Callable[[], float] = time.time,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self.scope = scope
        self.rpm, self.tpm, self.rpd, self.tpd = rpm, tpm, rpd, tpd
        self.store = store or DailyUsageStore(None)
        self.offset = timedelta(hours=reset_utc_offset_h)
        self.clock, self.wall, self.sleep = clock, wall, sleep
        now = clock()
        self._req = _Bucket(rpm, now) if rpm else None
        self._tok = _Bucket(tpm, now) if tpm else None
        self._lock = threading.Lock()

    def day(self) -> str:
        return (datetime.fromtimestamp(self.wall(), UTC) + self.offset).date().isoformat()

    def usage_today(self) -> tuple[int, int]:
        return self.store.get(self.scope, self.day())

    def _check_daily(self, est_tokens: int) -> None:
        day = self.day()
        n_req, n_tok = self.store.get(self.scope, day)
        if self.rpd is not None and n_req + 1 > self.rpd:
            raise QuotaExhaustedError(
                f"{self.scope}: đã dùng {n_req}/{self.rpd} request ngày {day} (bộ đếm cục bộ)",
                provider=self.scope,
            )
        if self.tpd is not None and n_tok + est_tokens > self.tpd:
            raise QuotaExhaustedError(
                f"{self.scope}: đã dùng {n_tok}/{self.tpd} token ngày {day} (bộ đếm cục bộ)",
                provider=self.scope,
            )

    def acquire(self, est_tokens: int = 0) -> float:
        """Chờ đến khi được gửi 1 request ước ``est_tokens`` token. Trả về số giây đã chờ."""
        with self._lock:
            self._check_daily(est_tokens)
            waited = 0.0
            while True:
                now = self.clock()
                wait = 0.0
                for b, amount in ((self._req, 1.0), (self._tok, float(est_tokens))):
                    if b is not None:
                        b.refill(now)
                        wait = max(wait, b.wait_for(amount))
                if wait <= 1e-9:
                    break
                logger.debug("%s: chờ %.2fs (RPM/TPM)", self.scope, wait)
                self.sleep(wait)
                waited += wait
            if self._req is not None:
                self._req.level -= 1.0
            if self._tok is not None:
                self._tok.level -= float(est_tokens)
            self.store.add(self.scope, self.day(), requests=1, tokens=est_tokens)
            return waited

    def record(self, actual_tokens: int, est_tokens: int) -> None:
        """Bù chênh lệch giữa usage thật và ước tính đã trừ lúc ``acquire``."""
        diff = int(actual_tokens) - int(est_tokens)
        if diff == 0:
            return
        with self._lock:
            if self._tok is not None:
                self._tok.level -= diff
            self.store.add(self.scope, self.day(), tokens=diff)
