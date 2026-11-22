"""Log huấn luyện M14: JSONL cục bộ ``logs/train/<run>.jsonl`` (người dùng chọn 18/11/2026 — không
W&B/MLflow). Mỗi dòng một sự kiện ``{event, ts, elapsed_s, …}``:

- ``start``: tham số, commit, sha256 dữ liệu, GPU, torch, dtype, số bước;
- ``step``: loss, lr, mini-batch hiện hành (mỗi ``log_steps``);
- ``eval``: chỉ số val; ``best``: checkpoint tốt nhất mới;
- ``checkpoint`` / ``hub``: lưu, đẩy HF Hub (giây, commit sha);
- ``oom``: giảm mini-batch; ``resume``; ``end``: VRAM đỉnh, giờ GPU, VND.

File append (resume nối tiếp); dòng hỏng do mất điện bị cắt bởi ``JsonlWriter``.
"""

from __future__ import annotations

import time
from datetime import datetime
from pathlib import Path
from typing import Any

from trafficlaw.utils.jsonl import JsonlWriter, read_jsonl


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


class RunLog:
    def __init__(self, path: str | Path, *, echo: Any = None) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.t0 = time.perf_counter()
        self.echo = echo

    def event(self, event: str, **data: Any) -> dict[str, Any]:
        rec = {
            "event": event,
            "ts": now_iso(),
            "elapsed_s": round(time.perf_counter() - self.t0, 2),
            **data,
        }
        with JsonlWriter(self.path) as w:
            w.write(rec)
        if self.echo is not None:
            self.echo(rec)
        return rec


def read_events(path: str | Path, event: str | None = None) -> list[dict[str, Any]]:
    p = Path(path)
    if not p.is_file():
        return []
    return [r for r in read_jsonl(p) if event is None or r.get("event") == event]


def gpu_cost(seconds: float, price_vnd_per_hour: float) -> dict[str, float]:
    h = seconds / 3600
    return {"gpu_hours": round(h, 4), "vnd": round(h * price_vnd_per_hour)}


__all__ = ["RunLog", "gpu_cost", "now_iso", "read_events"]
