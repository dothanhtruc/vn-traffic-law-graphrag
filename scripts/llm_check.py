"""M7: kiểm tra provider LLM — có key không, liệt kê model, gọi ping JSON thật.

    uv run python -m scripts.llm_check                       # ping mọi provider có key + model_id
    uv run python -m scripts.llm_check --list-models [--provider gemini] [--all]
    uv run python -m scripts.llm_check --provider groq --model llama-3.3-70b-versatile --n 3

Key đọc từ môi trường / ``.env``; chỉ in **tên** biến, không in giá trị. Ping mặc định không dùng
cache (``--cache`` để dùng). Mã thoát 1 nếu một ping không ``ok`` hoặc trả sai nội dung.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from trafficlaw.llm.client import build_client, has_key, make_provider
from trafficlaw.llm.config import LLMConfig, load_llm_config
from trafficlaw.llm.prompt_loader import load_prompt
from trafficlaw.llm.types import LLMError, QuotaExhaustedError
from trafficlaw.utils.env import load_dotenv
from trafficlaw.utils.logging import setup_logging
from trafficlaw.utils.seed import set_seed

REPO_ROOT = Path(__file__).resolve().parents[1]

# Gemini không dùng (CLAUDE.md mục 2): 1.x, 2.0 Flash-Lite.
_GEMINI_EXCLUDED = re.compile(r"gemini-1\.|gemini-2\.0-flash-lite")


class PingAnswer(BaseModel):
    ok: bool
    echo: str
    sum: int


def _list_models(cfg: LLMConfig, provider: str, show_all: bool) -> list[dict[str, Any]]:
    prov = make_provider(cfg, provider, model_id="(list)")
    models = prov.list_models()  # type: ignore[attr-defined]
    rows: list[dict[str, Any]] = []
    kind = cfg.providers[provider].kind
    for m in models:
        if kind == "gemini":
            if "generateContent" not in (m.get("supportedGenerationMethods") or []):
                continue
            mid = str(m.get("name", "")).removeprefix("models/")
            if not show_all and "gemini" not in mid:
                continue
            rows.append(
                {
                    "id": mid,
                    "name": m.get("displayName"),
                    "in": m.get("inputTokenLimit"),
                    "out": m.get("outputTokenLimit"),
                    "thinking": m.get("thinking"),
                    "excluded": bool(_GEMINI_EXCLUDED.search(mid)),
                }
            )
        elif provider == "openrouter":
            mid = str(m.get("id", ""))
            if not show_all and not mid.endswith(":free"):
                continue
            rows.append({"id": mid, "ctx": m.get("context_length"), "name": m.get("name")})
        else:
            rows.append(
                {
                    "id": m.get("id"),
                    "owner": m.get("owned_by"),
                    "ctx": m.get("context_window"),
                    "active": m.get("active"),
                }
            )
    return sorted(rows, key=lambda r: str(r["id"]))


def _ping(cfg: LLMConfig, provider: str, model_id: str | None, n: int, use_cache: bool) -> bool:
    client = build_client(cfg, provider, model_id=model_id, root=REPO_ROOT, use_cache=use_cache)
    prompt = load_prompt("ping")
    good = True
    lat: list[int] = []
    for i in range(n):
        word, a, b = f"giao-thong-{i}", 17 + i, 25
        msgs = [{"role": "user", "content": prompt.render(word=word, a=a, b=b)}]
        try:
            r = client.generate(msgs, json_schema=PingAnswer, use_cache=use_cache)
        except QuotaExhaustedError as e:
            print(f"  [{provider}] HẾT QUOTA: {e}\n  {e.resume_hint}")
            return False
        correct = r.status == "ok" and r.parsed == {"ok": True, "echo": word, "sum": a + b}
        good &= correct
        lat.append(r.latency_ms)
        print(
            f"  [{provider}:{r.model_id}] #{i + 1} status={r.status} correct={correct} "
            f"attempts={r.attempts} cached={r.cached} latency_ms={r.latency_ms} "
            f"usage={r.usage.prompt_tokens}+{r.usage.completion_tokens}={r.usage.total_tokens}"
            f"{' (ước tính)' if r.usage.estimated else ''}"
        )
        if r.status != "ok" or not correct:
            print(f"    text={r.text[:300]!r} error={r.error}")
    if n > 1:
        print(f"  [{provider}] latency median={statistics.median(lat):.0f} ms, max={max(lat)} ms")
    req, tok = client.limiter.usage_today() if client.limiter else (0, 0)
    print(f"  [{provider}] bộ đếm hôm nay (cục bộ): {req} request, {tok} token")
    return good


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--config", default=str(REPO_ROOT / "configs" / "llm.yaml"))
    ap.add_argument("--provider", action="append", help="lặp lại được; mặc định mọi provider")
    ap.add_argument("--model", help="ghi đè model_id (chỉ khi có đúng một --provider)")
    ap.add_argument("--list-models", action="store_true")
    ap.add_argument("--all", action="store_true", help="--list-models: không lọc")
    ap.add_argument("--json", help="--list-models: ghi danh sách ra file JSON")
    ap.add_argument("--n", type=int, default=1, help="số lượt ping mỗi provider")
    ap.add_argument("--cache", action="store_true", help="ping dùng cache")
    args = ap.parse_args(argv)

    setup_logging("WARNING")
    set_seed()
    load_dotenv(REPO_ROOT / ".env")
    cfg = load_llm_config(args.config)
    providers = args.provider or list(cfg.providers)
    if args.model and len(providers) != 1:
        ap.error("--model cần đúng một --provider")

    print("Key (chỉ tên biến):")
    for p in cfg.providers:
        env = cfg.providers[p].api_key_env
        print(f"  {p:<11} {env:<20} {'có' if has_key(cfg, p) else 'THIẾU'}")
    print(f"Model chính: {cfg.main.provider}:{cfg.main.model_id}")

    ok = True
    listing: dict[str, Any] = {}
    for p in providers:
        if not has_key(cfg, p):
            print(f"\n[{p}] bỏ qua: thiếu {cfg.providers[p].api_key_env}")
            continue
        print(f"\n[{p}]")
        try:
            if args.list_models:
                rows = _list_models(cfg, p, args.all)
                listing[p] = rows
                for r in rows:
                    print("  " + "  ".join(f"{k}={v}" for k, v in r.items()))
                print(f"  ({len(rows)} model)")
                continue
            mid = args.model
            if mid is None and p == cfg.main.provider:
                mid = cfg.main.model_id
            if not (mid or cfg.providers[p].model_id):
                print("  bỏ qua ping: chưa có model_id (dùng --model)")
                continue
            ok &= _ping(cfg, p, mid, args.n, args.cache)
        except LLMError as e:
            print(f"  LỖI {type(e).__name__}: {e}")
            ok = False
    if args.json and listing:
        Path(args.json).write_text(
            json.dumps(listing, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n"
        )
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
