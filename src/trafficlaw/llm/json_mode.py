"""Parse + validate phản hồi JSON của LLM.

``extract_json``: bỏ khoảng trắng; nếu có khối ```` ```json … ``` ```` lấy nội dung khối đầu tiên;
nếu không phải JSON nguyên vẹn thì lấy đoạn từ ``{`` đầu tiên tới ``}`` cuối cùng. ``parse``:
``json.loads`` rồi validate bằng lớp pydantic (``schema`` là ``BaseModel``) hoặc chỉ kiểm tra là
object (``schema`` là dict / None). Lỗi → ``FormatError`` (``LLMClient`` gọi lại đúng 1 lần với
prompt ``format_repair``; vẫn lỗi → ``status = format_error``).
"""

from __future__ import annotations

import json
import re
from typing import Any

from pydantic import BaseModel, ValidationError

from trafficlaw.llm.types import FormatError

_FENCE_RE = re.compile(r"```(?:json|JSON)?\s*\n?(.*?)```", re.DOTALL)

JsonSchemaArg = type[BaseModel] | dict[str, Any] | None


def schema_dict(schema: JsonSchemaArg) -> dict[str, Any] | None:
    """JSON Schema gửi cho API."""
    if schema is None:
        return None
    if isinstance(schema, dict):
        return schema
    return schema.model_json_schema()


def extract_json(text: str) -> str:
    s = text.strip()
    m = _FENCE_RE.search(s)
    if m:
        s = m[1].strip()
    if s.startswith("{") and s.endswith("}"):
        return s
    i, j = s.find("{"), s.rfind("}")
    if i != -1 and j > i:
        return s[i : j + 1]
    return s


def parse(text: str, schema: JsonSchemaArg = None) -> Any:
    """Trả về dict (schema dict/None) hoặc instance pydantic → ``model_dump`` (dict)."""
    raw = extract_json(text)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise FormatError(f"JSON không hợp lệ: {e.msg} (vị trí {e.pos})") from None
    if not isinstance(data, dict):
        raise FormatError(f"cần JSON object, nhận {type(data).__name__}")
    if isinstance(schema, type) and issubclass(schema, BaseModel):
        try:
            return schema.model_validate(data).model_dump(mode="json")
        except ValidationError as e:
            errs = "; ".join(
                f"{'.'.join(str(x) for x in err['loc']) or '<root>'}: {err['msg']}"
                for err in e.errors()[:5]
            )
            raise FormatError(f"sai schema: {errs}") from None
    return data
