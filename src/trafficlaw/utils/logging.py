"""Cấu hình logging chung; tự che API key trong mọi log record."""

from __future__ import annotations

import logging
import os
from pathlib import Path

SECRET_ENV_VARS: tuple[str, ...] = (
    "GEMINI_API_KEY",
    "GROQ_API_KEY",
    "OPENROUTER_API_KEY",
    "NEO4J_PASSWORD",
)
MASK = "***"
_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"
_HANDLER_ATTR = "_trafficlaw_handler"


class SecretRedactFilter(logging.Filter):
    """Thay giá trị các biến môi trường bí mật bằng ``***`` trong message đã format."""

    def __init__(self, env_vars: tuple[str, ...] = SECRET_ENV_VARS) -> None:
        super().__init__()
        self.env_vars = env_vars

    def _secrets(self) -> list[str]:
        # Đọc lại env mỗi lần: key có thể được nạp sau khi cấu hình logging.
        return [v for name in self.env_vars if (v := os.environ.get(name)) and len(v) >= 4]

    def filter(self, record: logging.LogRecord) -> bool:
        secrets = self._secrets()
        if not secrets:
            return True
        msg = record.getMessage()
        redacted = msg
        for s in secrets:
            redacted = redacted.replace(s, MASK)
        if redacted != msg:
            record.msg = redacted
            record.args = None
        return True


def setup_logging(level: int | str = "INFO", log_file: str | Path | None = None) -> None:
    """Cấu hình root logger (gọi nhiều lần không nhân đôi handler)."""
    root = logging.getLogger()
    root.setLevel(level)
    for h in list(root.handlers):
        if getattr(h, _HANDLER_ATTR, False):
            root.removeHandler(h)
            h.close()

    handlers: list[logging.Handler] = [logging.StreamHandler()]
    if log_file is not None:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))
    for h in handlers:
        h.setFormatter(logging.Formatter(_FORMAT))
        h.addFilter(SecretRedactFilter())
        setattr(h, _HANDLER_ATTR, True)
        root.addHandler(h)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
