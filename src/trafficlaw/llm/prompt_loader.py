"""Nạp prompt ``llm/prompts/<name>.md``; ``hash`` = sha256 nội dung (NFC, LF) — ghi vào kết quả.

Sửa prompt ⇒ hash mới ⇒ run mới (khoá đánh giá chứa ``prompt_hash``). Biến dạng ``$ten`` /
``${ten}`` (``string.Template``), thiếu biến → ``KeyError``; ``$$`` = dấu ``$``.
"""

from __future__ import annotations

import hashlib
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from string import Template
from typing import Any

PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"


def normalize_prompt(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return unicodedata.normalize("NFC", text)


def prompt_hash(text: str) -> str:
    return hashlib.sha256(normalize_prompt(text).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Prompt:
    name: str
    text: str
    hash: str

    def render(self, **variables: Any) -> str:
        return Template(self.text).substitute({k: str(v) for k, v in variables.items()})


def load_prompt(name: str, prompts_dir: str | Path = PROMPTS_DIR) -> Prompt:
    path = Path(prompts_dir) / f"{name}.md"
    text = normalize_prompt(path.read_text(encoding="utf-8-sig"))
    return Prompt(name=name, text=text, hash=prompt_hash(text))
