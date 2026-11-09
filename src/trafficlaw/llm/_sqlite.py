"""Mở SQLite chịu lỗi: file hỏng (không phải database) → đổi tên ``.corrupt-<ts>`` rồi tạo mới."""

from __future__ import annotations

import logging
import sqlite3
import time
from pathlib import Path

logger = logging.getLogger(__name__)


def connect(path: str | Path, schema: str) -> sqlite3.Connection:
    """Kết nối (``check_same_thread=False``; người gọi tự giữ lock) và tạo bảng theo ``schema``."""
    p = Path(path)
    if str(p) != ":memory:":
        p.parent.mkdir(parents=True, exist_ok=True)
    try:
        conn = _open(p, schema)
    except sqlite3.DatabaseError as e:
        if str(p) == ":memory:":
            raise
        bad = p.with_name(f"{p.name}.corrupt-{int(time.time())}")
        logger.warning("SQLite %s hỏng (%s) → đổi tên %s, tạo mới", p, e, bad.name)
        p.replace(bad)
        conn = _open(p, schema)
    return conn


def _open(p: Path, schema: str) -> sqlite3.Connection:
    conn = sqlite3.connect(str(p), check_same_thread=False, isolation_level=None)
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.executescript(schema)
        conn.execute("PRAGMA quick_check").fetchone()
    except sqlite3.DatabaseError:
        conn.close()
        raise
    return conn
