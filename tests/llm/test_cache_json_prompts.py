from __future__ import annotations

import sqlite3

import pytest

from tests.llm.conftest import Answer
from trafficlaw.llm import json_mode
from trafficlaw.llm.cache import LLMCache, cache_key
from trafficlaw.llm.prompt_loader import load_prompt, prompt_hash
from trafficlaw.llm.providers.fake import FakeClient, bad_json, ok, server_error
from trafficlaw.llm.types import FormatError, LLMRequest, LLMResult, Message

GOOD = '{"answer": "Phạt tiền", "citations": ["ND168-2024/D6/K4/a"]}'
MSG = [{"role": "user", "content": "Câu hỏi?"}]


def _req(content="x", **kw) -> LLMRequest:
    return LLMRequest(messages=[Message(role="user", content=content)], **kw)


# ------------------------------------------------------------------ cache
def test_cache_hit_miss(make_client, tmp_path):
    cache = LLMCache(tmp_path / "c.sqlite")
    fake = FakeClient([ok(GOOD)])
    c = make_client(fake, cache=cache)
    r1 = c.generate(MSG, json_schema=Answer)
    r2 = c.generate(MSG, json_schema=Answer)
    assert fake.n_calls == 1
    assert not r1.cached and r2.cached
    assert r2.parsed == r1.parsed and r2.usage == r1.usage and r2.latency_ms == r1.latency_ms
    c.generate(MSG, json_schema=Answer, use_cache=False)
    assert fake.n_calls == 2


def test_cache_key_changes():
    base = cache_key("gemini", "m1", _req(params={"temperature": 0}))
    assert base == cache_key("gemini", "m1", _req(params={"temperature": 0}))
    assert base != cache_key("gemini", "m2", _req(params={"temperature": 0}))
    assert base != cache_key("groq", "m1", _req(params={"temperature": 0}))
    assert base != cache_key("gemini", "m1", _req(params={"temperature": 0.5}))
    assert base != cache_key("gemini", "m1", _req("y", params={"temperature": 0}))
    assert base != cache_key(
        "gemini", "m1", _req(params={"temperature": 0}, json_schema={"type": "object"})
    )
    # NFC: cùng chữ, khác dạng tổ hợp → cùng khoá
    nfd = "Luật"  # "Luật" dạng NFD
    assert cache_key("g", "m", _req(nfd)) == cache_key("g", "m", _req("Luật"))


def test_cache_does_not_store_errors(make_client, tmp_path):
    cache = LLMCache(tmp_path / "c.sqlite")
    c = make_client(FakeClient([server_error()]), cache=cache, max_retries=0)
    assert c.generate(MSG).status == "error"
    c2 = make_client(FakeClient([bad_json(), bad_json()]), cache=cache)
    assert c2.generate(MSG, json_schema=Answer).status == "format_error"
    assert len(cache) == 0
    assert not cache.put("k", LLMResult(model_id="m", provider="p", status="error"))


def test_cache_corrupt_row_is_miss(tmp_path):
    path = tmp_path / "c.sqlite"
    cache = LLMCache(path)
    cache.put("k", LLMResult(model_id="m", provider="p", status="ok", text="a"))
    cache._conn.execute("UPDATE responses SET result_json = '{hỏng' WHERE key='k'")
    assert cache.get("k") is None
    assert len(cache) == 0  # dòng hỏng bị xoá


def test_cache_corrupt_file_recreated(tmp_path):
    path = tmp_path / "c.sqlite"
    path.write_bytes(b"day khong phai sqlite" * 100)
    cache = LLMCache(path)
    assert cache.get("k") is None
    cache.put("k", LLMResult(model_id="m", provider="p", status="ok"))
    assert cache.get("k") is not None
    assert list(tmp_path.glob("c.sqlite.corrupt-*"))
    sqlite3.connect(path).execute("SELECT 1")


# ------------------------------------------------------------------ json_mode
def test_parse_plain_and_fenced():
    assert json_mode.parse('{"a": 1}') == {"a": 1}
    assert json_mode.parse('```json\n{"a": 1}\n```') == {"a": 1}
    assert json_mode.parse('Đây là kết quả:\n```\n{"a": [1, 2]}\n```\nHết.') == {"a": [1, 2]}
    assert json_mode.parse('Kết quả: {"a": "x"} xong') == {"a": "x"}


def test_parse_schema():
    out = json_mode.parse(GOOD, Answer)
    assert out == {"answer": "Phạt tiền", "citations": ["ND168-2024/D6/K4/a"], "numbers": []}
    with pytest.raises(FormatError, match="citations"):
        json_mode.parse('{"answer": "x"}', Answer)
    with pytest.raises(FormatError, match="JSON không hợp lệ"):
        json_mode.parse('{"answer": ')
    with pytest.raises(FormatError, match="object"):
        json_mode.parse("[1, 2]")


def test_wrong_schema_repair_once_then_format_error(make_client):
    fake = FakeClient([ok('{"answer": "x"}'), ok('{"answer": "y"}'), ok(GOOD)])
    r = make_client(fake).generate(MSG, json_schema=Answer)
    assert r.status == "format_error" and fake.n_calls == 2  # đúng 1 lần sửa
    assert r.attempts == 2 and "citations" in r.error and r.text == '{"answer": "y"}'


def test_wrong_schema_repaired(make_client):
    fake = FakeClient([ok('{"answer": "x"}'), ok("```json\n" + GOOD + "\n```")])
    r = make_client(fake).generate(MSG, json_schema=Answer)
    assert r.status == "ok" and r.parsed["answer"] == "Phạt tiền"
    assert r.usage.total_tokens > 0
    # schema trong lời nhắc sửa
    assert '"citations"' in fake.requests[1].messages[-1].content


def test_request_carries_schema(make_client):
    fake = FakeClient([ok(GOOD)])
    make_client(fake).generate(MSG, json_schema=Answer)
    req = fake.requests[0]
    assert req.json_output and req.json_schema["properties"]["citations"]["type"] == "array"
    fake2 = FakeClient([ok("text")])
    make_client(fake2).generate(MSG)
    assert not fake2.requests[0].json_output


# ------------------------------------------------------------------ prompts
def test_prompt_hash_stable():
    p = load_prompt("ping")
    assert p.hash == prompt_hash(p.text) == load_prompt("ping").hash
    assert prompt_hash("a\r\nb") == prompt_hash("a\nb")
    assert prompt_hash("Luật") == prompt_hash("Luật")
    assert prompt_hash("a") != prompt_hash("b")


def test_prompt_render(tmp_path):
    (tmp_path / "t.md").write_bytes('Câu: $q — JSON {"x": 1} giá $$5\r\n'.encode())
    p = load_prompt("t", tmp_path)
    assert p.render(q="Mức phạt?") == 'Câu: Mức phạt? — JSON {"x": 1} giá $5\n'
    with pytest.raises(KeyError):
        p.render()


def test_repair_prompt_exists():
    p = load_prompt("format_repair")
    assert "$error" in p.text and "$schema" in p.text
