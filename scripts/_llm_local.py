"""Phần dùng chung của các script gọi LLM tự host (provider ``local``, vLLM qua SSH tunnel):
chọn model, kiểm tra server trước khi chạy, thông tin tái lập, ước tính giờ GPU."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

from trafficlaw.llm import LLMConfig, LLMError
from trafficlaw.llm.serve import ServeConfig, load_serve_config, probe, run_meta

REPO_ROOT = Path(__file__).resolve().parents[1]


def serve_config(root: Path = REPO_ROOT) -> ServeConfig | None:
    p = root / "configs" / "serve.yaml"
    return load_serve_config(p) if p.is_file() else None


def resolve_model(
    llm_cfg: LLMConfig, provider: str | None, model_id: str | None
) -> tuple[str, str | None]:
    """(provider, model_id): ưu tiên tham số dòng lệnh / config bước, rồi ``main``, rồi model
    mặc định của provider. ``model_id`` có thể ``None`` (chưa chốt)."""
    p = provider or llm_cfg.main.provider
    if p not in llm_cfg.providers:
        raise SystemExit(f"provider '{p}' không có trong configs/llm.yaml")
    if model_id:
        return p, model_id
    if p == llm_cfg.main.provider and llm_cfg.main.model_id:
        return p, llm_cfg.main.model_id
    return p, llm_cfg.providers[p].model_id


def is_local(llm_cfg: LLMConfig, provider: str) -> bool:
    pc = llm_cfg.providers[provider]
    return pc.kind == "openai_compat" and ("127.0.0.1" in pc.base_url or "localhost" in pc.base_url)


def check_local_server(
    llm_cfg: LLMConfig, provider: str, model_id: str, root: Path = REPO_ROOT
) -> dict[str, Any] | None:
    """Server local phải đang phục vụ đúng ``model_id`` (qua tunnel). Trả về ``run_meta`` để ghi
    vào bản ghi; lỗi → in hướng dẫn rồi ``None``."""
    pc = llm_cfg.providers[provider]
    key = os.environ.get(pc.api_key_env, "")
    if not key:
        print(
            f"thiếu {pc.api_key_env} (đặt trong .env, bằng VLLM_API_KEY trên máy thuê)",
            file=sys.stderr,
        )
        return None
    try:
        info = probe(pc.base_url, key)
    except LLMError as e:
        print(f"server local: {e}", file=sys.stderr)
        return None
    served = [m["id"] for m in info["models"]]
    if model_id not in served:
        print(
            f"server local đang phục vụ {served}, không có '{model_id}' — chạy "
            f"scripts/gpu/gpu.sh serve <model> với đúng model",
            file=sys.stderr,
        )
        return None
    scfg = serve_config(root)
    meta = run_meta(scfg, model_id, info) if scfg else {"served_model": model_id, **info}
    if scfg and not meta.get("revision"):
        print(
            f"cảnh báo: '{model_id}' chưa ghim revision trong configs/serve.yaml — chỉ dùng để "
            "chạy thử, không dùng cho run chính thức",
            file=sys.stderr,
        )
    return meta


def family_of(model_id: str | None, root: Path = REPO_ROOT) -> str | None:
    scfg = serve_config(root)
    if not scfg or not model_id:
        return None
    hit = scfg.by_served_name(model_id)
    return hit[1].family if hit else None


__all__ = ["check_local_server", "family_of", "is_local", "resolve_model", "serve_config"]
