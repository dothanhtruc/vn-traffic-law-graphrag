"""Đọc file ``.env`` (KEY=VALUE) vào ``os.environ`` — không thêm dependency ``python-dotenv``.

Chỉ hỗ trợ cú pháp đơn giản: dòng trống / ``#`` bỏ qua, ``export KEY=VALUE`` được chấp nhận,
giá trị có thể bọc trong ``'…'`` hoặc ``"…"``. Biến đã có trong môi trường **không bị ghi đè**
(trừ khi ``override=True``). Không bao giờ log giá trị.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

_LINE_RE = re.compile(r"^(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$")


def parse_dotenv(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        m = _LINE_RE.match(line)
        if not m:
            continue
        key, val = m[1], m[2].strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in "'\"":
            val = val[1:-1]
        else:
            val = re.sub(r"\s+#.*$", "", val)
        out[key] = val
    return out


def load_dotenv(path: str | Path = ".env", *, override: bool = False) -> list[str]:
    """Nạp ``path`` (không có file → không làm gì). Trả về tên các biến đã đặt."""
    p = Path(path)
    if not p.is_file():
        return []
    loaded: list[str] = []
    for key, val in parse_dotenv(p.read_text(encoding="utf-8-sig")).items():
        if override or key not in os.environ:
            os.environ[key] = val
            loaded.append(key)
    return loaded
