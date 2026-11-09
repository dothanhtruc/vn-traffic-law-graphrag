"""Cache phản hồi LLM trong SQLite (stdlib ``sqlite3``).

Khoá = ``sha256(canonical_json({provider, model_id, messages (NFC), params, json_schema}))`` — đổi
model, tham số, prompt hay schema đều ra khoá mới. **Chỉ lưu kết quả ``ok``** (không lưu
``error``/``format_error``), kèm usage + latency của lần gọi gốc để số liệu đánh giá tái lập được
khi chạy lại (kết quả trả từ cache có ``cached=True``). Không lưu API key: key không nằm trong
request.

Chịu lỗi: dòng hỏng (JSON lỗi / không khớp schema) → coi như trượt, xoá dòng, warning; file không
phải database → đổi tên ``.corrupt-<ts>`` rồi tạo mới.
"""

from __future__ import annotations

import hashlib
import json
import logging
import threading
import time
import unicodedata
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from trafficlaw.llm import _sqlite
from trafficlaw.llm.types import LLMRequest, LLMResult

logger = logging.getLogger(__name__)

_SCHEMA = """
CREATE TABLE IF NOT EXISTS responses (
    key TEXT PRIMARY KEY, model_id TEXT NOT NULL, provider TEXT NOT NULL,
    result_json TEXT NOT NULL, created_at REAL NOT NULL
);
"""


def canonical_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def cache_key(provider: str, model_id: str, request: LLMRequest) -> str:
    payload = {
        "provider": provider,
        "model_id": model_id,
        "messages": [
            {"role": m.role, "content": unicodedata.normalize("NFC", m.content)}
            for m in request.messages
        ],
        "params": request.params,
        "json_schema": request.json_schema,
        "json_output": request.json_output,
    }
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


class LLMCache:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self._conn = _sqlite.connect(self.path, _SCHEMA)
        self._lock = threading.Lock()

    def get(self, key: str) -> LLMResult | None:
        with self._lock:
            row = self._conn.execute(
                "SELECT result_json FROM responses WHERE key=?", (key,)
            ).fetchone()
        if row is None:
            return None
        try:
            result = LLMResult.model_validate_json(row[0])
        except (ValidationError, ValueError) as e:
            logger.warning("cache: dòng %s… hỏng (%s) → bỏ", key[:12], type(e).__name__)
            self.delete(key)
            return None
        if result.status != "ok":
            self.delete(key)
            return None
        return result.model_copy(update={"cached": True})

    def put(self, key: str, result: LLMResult) -> bool:
        if result.status != "ok":
            return False
        data = result.model_copy(update={"cached": False}).model_dump_json()
        with self._lock:
            self._conn.execute(
                "INSERT OR REPLACE INTO responses(key, model_id, provider, result_json, created_at)"
                " VALUES (?, ?, ?, ?, ?)",
                (key, result.model_id, result.provider, data, time.time()),
            )
        return True

    def delete(self, key: str) -> None:
        with self._lock:
            self._conn.execute("DELETE FROM responses WHERE key=?", (key,))

    def __len__(self) -> int:
        with self._lock:
            return int(self._conn.execute("SELECT COUNT(*) FROM responses").fetchone()[0])

    def close(self) -> None:
        self._conn.close()
