"""JSONL append-only, flush từng dòng, hỗ trợ resume cho job dài.

Mẫu dùng cho job resume được::

    done = done_keys(out, ["config_name", "question_id", "model_id", "prompt_hash"])
    with JsonlWriter(out) as w:
        for q in questions:
            if key(q) in done:
                continue
            w.write(run(q))
"""

from __future__ import annotations

import json
import logging
import os
import tempfile
from collections.abc import Callable, Iterable, Iterator, Sequence
from datetime import date, datetime
from pathlib import Path
from types import TracebackType
from typing import Any

from pydantic import BaseModel

logger = logging.getLogger(__name__)

Record = dict[str, Any] | BaseModel


def _default(o: Any) -> Any:
    if isinstance(o, (date, datetime)):
        return o.isoformat()
    if isinstance(o, BaseModel):
        return o.model_dump(mode="json")
    if isinstance(o, Path):
        return o.as_posix()
    if isinstance(o, (set, frozenset)):
        return sorted(o)
    raise TypeError(f"Không serialize được kiểu {type(o).__name__}")


def dumps(record: Record) -> str:
    """Một bản ghi → một dòng JSON (UTF-8, giữ tiếng Việt, không xuống dòng)."""
    if isinstance(record, BaseModel):
        record = record.model_dump(mode="json")
    return json.dumps(record, ensure_ascii=False, default=_default)


class JsonlWriter:
    """Mở file một lần ở chế độ append; mỗi ``write`` ghi một dòng rồi flush."""

    def __init__(self, path: str | Path, *, fsync: bool = False) -> None:
        self.path = Path(path)
        self.fsync = fsync
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._repair_tail()
        self._fh = self.path.open("a", encoding="utf-8", newline="\n")

    def _repair_tail(self) -> None:
        """Chuẩn bị file để ghi tiếp sau khi lần chạy trước bị ngắt.

        Dòng cuối không có ``\\n``: nếu là JSON hợp lệ thì thêm ``\\n``; nếu bị cắt dở
        thì cắt bỏ (bản ghi chưa hoàn chỉnh, ``read_jsonl`` vốn đã bỏ qua nó).
        """
        if not self.path.exists() or self.path.stat().st_size == 0:
            return
        with self.path.open("r+b") as f:
            f.seek(-1, os.SEEK_END)
            if f.read(1) == b"\n":
                return
            f.seek(0)
            data = f.read()
            cut = data.rfind(b"\n") + 1
            tail = data[cut:]
            try:
                json.loads(tail.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                logger.warning(
                    "Cắt bỏ dòng cuối bị cắt dở trong %s (%d byte)", self.path, len(tail)
                )
                f.truncate(cut)
            else:
                f.seek(0, os.SEEK_END)
                f.write(b"\n")

    def write(self, record: Record) -> None:
        self._fh.write(dumps(record) + "\n")
        self._fh.flush()
        if self.fsync:
            os.fsync(self._fh.fileno())

    def close(self) -> None:
        if not self._fh.closed:
            self._fh.close()

    def __enter__(self) -> JsonlWriter:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close()


def append_jsonl(path: str | Path, record: Record, *, fsync: bool = False) -> None:
    """Ghi thêm một bản ghi vào cuối file (tự tạo thư mục cha)."""
    with JsonlWriter(path, fsync=fsync) as w:
        w.write(record)


def read_jsonl(path: str | Path) -> Iterator[dict[str, Any]]:
    """Đọc từng bản ghi.

    - File chưa tồn tại → không có bản ghi.
    - Dòng trống bị bỏ qua.
    - Dòng hỏng *ở cuối file* (job bị ngắt khi đang ghi) → bỏ qua, log warning.
    - Dòng hỏng ở giữa file → ``ValueError`` (dữ liệu hỏng thật, không im lặng bỏ qua).
    """
    path = Path(path)
    if not path.exists():
        return
    with path.open("r", encoding="utf-8") as f:
        lines = f.read().split("\n")
    # Vị trí dòng không rỗng cuối cùng.
    last = max((i for i, ln in enumerate(lines) if ln.strip()), default=-1)
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        try:
            yield json.loads(line)
        except json.JSONDecodeError as e:
            if i == last:
                logger.warning("Bỏ qua dòng cuối bị cắt dở trong %s (dòng %d)", path, i + 1)
                return
            raise ValueError(f"JSON hỏng ở {path}:{i + 1}: {e}") from e


def done_keys(
    path: str | Path,
    key_fields: Sequence[str],
    *,
    where: Callable[[dict[str, Any]], bool] | None = None,
) -> set[tuple[Any, ...]]:
    """Tập khóa ``tuple(record[f] for f in key_fields)`` của các bản ghi đã có.

    ``where`` (tuỳ chọn) lọc bản ghi được tính là "đã xong".
    Bản ghi thiếu trường khóa bị bỏ qua kèm warning.
    """
    keys: set[tuple[Any, ...]] = set()
    missing = 0
    for rec in read_jsonl(path):
        if where is not None and not where(rec):
            continue
        try:
            keys.add(tuple(rec[f] for f in key_fields))
        except KeyError:
            missing += 1
    if missing:
        logger.warning("%d bản ghi trong %s thiếu trường khóa %s", missing, path, list(key_fields))
    return keys


def write_jsonl(path: str | Path, records: Iterable[Record]) -> int:
    """Ghi đè toàn bộ file một cách atomic (file tạm + ``os.replace``). Trả về số bản ghi."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    n = 0
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            for rec in records:
                f.write(dumps(rec) + "\n")
                n += 1
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise
    return n
