"""Lớp gọi LLM (M7): providers (Gemini, Groq, OpenRouter, Fake), rate limit, retry, cache, JSON."""

from trafficlaw.llm.client import FallbackClient, LLMClient, build_client, build_fallback_client
from trafficlaw.llm.config import LLMConfig, load_llm_config
from trafficlaw.llm.prompt_loader import Prompt, load_prompt, prompt_hash
from trafficlaw.llm.types import (
    AuthError,
    BadRequestError,
    FormatError,
    LLMError,
    LLMResult,
    LLMTimeoutError,
    Message,
    QuotaExhaustedError,
    RateLimitError,
    ServerError,
    Usage,
)

__all__ = [
    "AuthError",
    "BadRequestError",
    "FallbackClient",
    "FormatError",
    "LLMClient",
    "LLMConfig",
    "LLMError",
    "LLMResult",
    "LLMTimeoutError",
    "Message",
    "Prompt",
    "QuotaExhaustedError",
    "RateLimitError",
    "ServerError",
    "Usage",
    "build_client",
    "build_fallback_client",
    "load_llm_config",
    "load_prompt",
    "prompt_hash",
]
