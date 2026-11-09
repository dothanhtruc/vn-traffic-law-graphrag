"""Provider: Gemini (REST generateContent), OpenAI-compatible (Groq, OpenRouter), FakeClient."""

from trafficlaw.llm.providers.base import Provider
from trafficlaw.llm.providers.fake import FakeClient

__all__ = ["FakeClient", "Provider"]
