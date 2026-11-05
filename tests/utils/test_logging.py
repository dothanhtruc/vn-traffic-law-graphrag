import logging
from pathlib import Path

import pytest

from trafficlaw.utils.logging import SecretRedactFilter, setup_logging


def test_redacts_secret(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "AIzaSECRET123")
    record = logging.LogRecord(
        "x", logging.INFO, __file__, 1, "key=%s url=%s", ("AIzaSECRET123", "u"), None
    )
    assert SecretRedactFilter().filter(record)
    assert record.getMessage() == "key=*** url=u"


def test_setup_logging_file_and_idempotent(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GROQ_API_KEY", "gsk_topsecret")
    log_file = tmp_path / "logs" / "run.log"
    root = logging.getLogger()
    before = list(root.handlers)
    try:
        setup_logging("INFO", log_file)
        setup_logging("INFO", log_file)
        ours = [h for h in root.handlers if h not in before]
        assert len(ours) == 2  # stream + file, không nhân đôi
        logging.getLogger("trafficlaw.test").info("gọi API với key gsk_topsecret")
        for h in ours:
            h.flush()
        text = log_file.read_text(encoding="utf-8")
        assert "gsk_topsecret" not in text
        assert "gọi API với key ***" in text
    finally:
        for h in list(root.handlers):
            if h not in before:
                root.removeHandler(h)
                h.close()
