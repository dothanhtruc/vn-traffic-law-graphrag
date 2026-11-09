"""Gọi LLM song song (server vLLM tự host chỉ nhanh khi nhận nhiều request cùng lúc để gộp batch).

``map_parallel(items, fn, workers)`` chạy ``fn`` trên nhiều luồng và **trả kết quả về luồng gọi**
(theo thứ tự hoàn thành) ⇒ việc ghi file (``JsonlWriter``) vẫn chỉ ở một luồng. Số việc đang chạy
giới hạn ở ``2 × workers`` (không xếp hàng cả nghìn lô rồi phải huỷ).

``QuotaExhaustedError`` (gồm hết quota / vượt trần) ở một việc ⇒ ngừng giao việc mới, chờ các
việc đang chạy xong và trả cả kết quả của chúng (không phí lượt đã gọi), rồi trả chính lỗi đó
cho luồng gọi để dừng sạch. Lỗi khác được ném lại như gọi tuần tự.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from typing import TypeVar

from trafficlaw.llm.types import QuotaExhaustedError

T = TypeVar("T")
R = TypeVar("R")


def map_parallel(
    items: Iterable[T], fn: Callable[[T], R], workers: int = 1
) -> Iterator[tuple[T, R | QuotaExhaustedError]]:
    """Yield ``(item, kết quả)``; kết quả là ``QuotaExhaustedError`` khi việc đó gặp hết quota
    (sau đó không còn việc mới nào được giao)."""
    if workers <= 1:
        for x in items:
            try:
                yield x, fn(x)
            except QuotaExhaustedError as e:
                yield x, e
                return
        return
    it = iter(items)
    stop = False
    with ThreadPoolExecutor(max_workers=workers) as ex:
        pending: dict[Future[R], T] = {}

        def refill() -> None:
            while not stop and len(pending) < 2 * workers:
                try:
                    x = next(it)
                except StopIteration:
                    return
                pending[ex.submit(fn, x)] = x

        refill()
        quota: tuple[T, QuotaExhaustedError] | None = None
        while pending:
            done, _ = wait(pending, return_when=FIRST_COMPLETED)
            for f in done:
                x = pending.pop(f)
                try:
                    r = f.result()
                except QuotaExhaustedError as e:
                    stop = True
                    if quota is None:
                        quota = (x, e)
                    continue
                yield x, r
            refill()
        if quota is not None:
            yield quota


__all__ = ["map_parallel"]
