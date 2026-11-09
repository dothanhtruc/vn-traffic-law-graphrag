"""Kiểu dữ liệu chung của lớp LLM (M7): tin nhắn, request, kết quả, lỗi có kiểu.

Không lớp nào ở đây chứa API key: key chỉ nằm trong provider (đọc từ môi trường), không vào
request, kết quả, cache hay thông điệp lỗi.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

Role = Literal["system", "user", "assistant"]
Status = Literal["ok", "error", "format_error"]


class Message(BaseModel):
    model_config = ConfigDict(frozen=True)

    role: Role
    content: str


class Usage(BaseModel):
    """Số token. ``estimated=True`` khi API không trả usage (ước bằng ``len(text)/4``)."""

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    estimated: bool = False


class LLMRequest(BaseModel):
    """Một lượt gọi provider (đã ghép params mặc định)."""

    messages: list[Message]
    params: dict[str, Any] = Field(default_factory=dict)
    json_schema: dict[str, Any] | None = None
    """JSON Schema gửi kèm cho API (nếu provider hỗ trợ); validate thật làm ở ``json_mode``."""
    json_output: bool = False
    """Yêu cầu provider trả JSON (``response_format``/``responseMimeType``)."""


class ProviderResponse(BaseModel):
    text: str
    usage: Usage
    finish_reason: str | None = None


class LLMResult(BaseModel):
    """Kết quả một lời gọi ``LLMClient.generate`` — đủ trường để ghi vào bản ghi đánh giá."""

    text: str = ""
    parsed: Any = None
    model_id: str
    provider: str
    usage: Usage = Field(default_factory=Usage)
    latency_ms: int = 0
    status: Status
    attempts: int = 0
    """Số lượt HTTP đã gửi (gồm retry và lượt sửa định dạng)."""
    cached: bool = False
    error: str | None = None
    repair_prompt_hash: str | None = None
    """Hash prompt sửa định dạng khi đã phải gọi lại để sửa JSON."""
    fallback_from: list[str] = Field(default_factory=list)
    """Chỉ FallbackClient (demo): các ``provider:model_id`` đã thử và thất bại trước."""


# --------------------------------------------------------------------------------------- lỗi


class LLMError(Exception):
    """Gốc mọi lỗi của lớp LLM. ``retryable`` quyết định có backoff hay không."""

    retryable: bool = False

    def __init__(self, message: str, *, provider: str = "", status_code: int | None = None):
        super().__init__(message)
        self.provider = provider
        self.status_code = status_code


class RateLimitError(LLMError):
    """429 theo phút (RPM/TPM). ``retry_after`` (giây) nếu server gợi ý."""

    retryable = True

    def __init__(self, message: str, *, retry_after: float | None = None, **kw: Any):
        super().__init__(message, **kw)
        self.retry_after = retry_after


class ServerError(LLMError):
    """5xx."""

    retryable = True


class LLMTimeoutError(LLMError):
    """Hết thời gian chờ / lỗi kết nối."""

    retryable = True


class QuotaExhaustedError(LLMError):
    """Hết quota theo ngày (server báo, hoặc bộ đếm RPD/TPD cục bộ). Job phải dừng sạch."""

    def __init__(self, message: str, *, resume_hint: str = "", **kw: Any):
        super().__init__(message, **kw)
        self.resume_hint = resume_hint or (
            "Hết quota ngày: dừng job, chạy lại đúng lệnh sau khi quota reset — "
            "bản ghi đã có được bỏ qua (resume)."
        )


class AuthError(LLMError):
    """401/403 hoặc thiếu key."""


class BadRequestError(LLMError):
    """4xx khác (model không tồn tại, request sai)."""


class FormatError(LLMError):
    """Phản hồi không parse/validate được theo schema."""
