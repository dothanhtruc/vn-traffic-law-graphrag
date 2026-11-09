"""Gọi song song (``map_parallel``) và cấu hình model tự host (``configs/serve.yaml``)."""

from __future__ import annotations

import threading
import time
from pathlib import Path

import httpx
import pytest

from trafficlaw.llm import LLMTimeoutError, QuotaExhaustedError, load_llm_config
from trafficlaw.llm.parallel import map_parallel
from trafficlaw.llm.serve import (
    ServeConfig,
    ServeModel,
    gpu_hours,
    load_serve_config,
    probe,
    remote_serve_script,
    run_meta,
    vllm_args,
)

REPO = Path(__file__).resolve().parents[2]


# --------------------------------------------------------------------------- map_parallel


@pytest.mark.parametrize("workers", [1, 4])
def test_map_parallel_same_results(workers: int) -> None:
    got = dict(map_parallel(range(20), lambda x: x * x, workers))
    assert got == {x: x * x for x in range(20)}


def test_map_parallel_runs_concurrently() -> None:
    active = 0
    peak = 0
    lock = threading.Lock()

    def fn(x: int) -> int:
        nonlocal active, peak
        with lock:
            active += 1
            peak = max(peak, active)
        time.sleep(0.02)
        with lock:
            active -= 1
        return x

    list(map_parallel(range(12), fn, 4))
    assert 2 <= peak <= 4


@pytest.mark.parametrize("workers", [1, 4])
def test_map_parallel_quota_stops_cleanly(workers: int) -> None:
    started: list[int] = []
    lock = threading.Lock()

    def fn(x: int) -> int:
        with lock:
            started.append(x)
        if x == 5:
            raise QuotaExhaustedError("hết quota (giả)")
        time.sleep(0.005)
        return x

    out = list(map_parallel(range(100), fn, workers))
    *ok, last = out
    assert isinstance(last[1], QuotaExhaustedError) and last[0] == 5
    assert all(not isinstance(r, Exception) for _, r in ok)
    # mọi việc đã bắt đầu (trừ việc lỗi) đều được trả kết quả — không mất lượt đã gọi
    assert sorted(x for x, _ in ok) == sorted(x for x in started if x != 5)
    assert len(started) <= 5 + 2 * workers + 1  # không giao thêm việc sau khi hết quota


def test_map_parallel_other_errors_propagate() -> None:
    def fn(x: int) -> int:
        raise ValueError("lỗi khác")

    with pytest.raises(ValueError):
        list(map_parallel(range(3), fn, 2))


# --------------------------------------------------------------------------- serve.yaml


def test_repo_serve_config_valid() -> None:
    cfg = load_serve_config(REPO / "configs" / "serve.yaml")
    assert cfg.remote.ssh_host and cfg.remote.price_vnd_per_hour > 0
    fams = {m.family for m in cfg.models.values()}
    assert len(fams) >= 2  # cần ít nhất hai họ: model chính ≠ họ model gán nháp/judge
    llm = load_llm_config(REPO / "configs" / "llm.yaml")
    local = llm.providers["local"]
    assert local.kind == "openai_compat" and local.json_mode == "schema"
    assert "127.0.0.1" in local.base_url  # chỉ qua SSH tunnel
    assert llm.main.provider == "local" and llm.fallback_order == []


def _model(**kw: object) -> ServeModel:
    base = {"hf_repo": "Org/Model-7B-AWQ", "served_model_name": "m7", "family": "x"}
    return ServeModel.model_validate({**base, **kw})


def test_vllm_args_local_only_and_no_key() -> None:
    args = vllm_args(_model(revision="abc123", quantization="awq_marlin"))
    s = " ".join(args)
    assert args[:2] == ["serve", "Org/Model-7B-AWQ"]
    assert "--host 127.0.0.1" in s and "--revision abc123" in s and "--seed 42" in s
    assert "--enable-prefix-caching" in s and "--quantization awq_marlin" in s
    assert "api-key" not in s  # key lấy từ VLLM_API_KEY trong env_file, không qua dòng lệnh


def test_remote_script_quotes_home_and_has_no_cr() -> None:
    cfg = ServeConfig(models={"a": _model(extra_args=["--max-num-seqs", "64"])})
    sc = remote_serve_script(cfg, "m7")
    assert "\r" not in sc and sc.startswith("#!/usr/bin/env bash\n")
    assert '. "$HOME"/.config/graphrag/env' in sc
    assert '"$HOME"/.venvs/vllm/bin/vllm serve Org/Model-7B-AWQ' in sc
    assert "--max-num-seqs 64" in sc
    with pytest.raises(KeyError):
        remote_serve_script(cfg, "khong-co")


def test_duplicate_served_name_rejected() -> None:
    with pytest.raises(ValueError):
        ServeConfig(models={"a": _model(), "b": _model()})


def test_gpu_hours_and_meta() -> None:
    cfg = ServeConfig(models={"a": _model(prefill_tps=3600.0, decode_tps=360.0, revision="r1")})
    h, vnd = gpu_hours(cfg, "m7", prompt_tokens=3600 * 3600, output_tokens=360 * 3600)
    assert h == pytest.approx(2.0) and vnd == 30_000  # 15.000 VND/giờ
    h2, _ = gpu_hours(cfg, "khac", prompt_tokens=4000 * 3600, output_tokens=0)
    assert h2 == pytest.approx(1.0)  # model lạ → tốc độ mặc định
    meta = run_meta(cfg, "m7", {"vllm_version": "0.0.test"})
    assert meta == {
        "served_model": "m7",
        "hf_repo": "Org/Model-7B-AWQ",
        "revision": "r1",
        "quantization": None,
        "vllm_version": "0.0.test",
    }


def test_probe_connection_error_mentions_tunnel(monkeypatch: pytest.MonkeyPatch) -> None:
    def boom(*a: object, **k: object) -> httpx.Response:
        raise httpx.ConnectError("refused")

    monkeypatch.setattr(httpx.Client, "get", boom)
    with pytest.raises(LLMTimeoutError, match="tunnel SSH"):
        probe("http://127.0.0.1:8000/v1", "k")


def test_probe_reads_models_and_version(monkeypatch: pytest.MonkeyPatch) -> None:
    seen: list[str] = []

    def get(self: httpx.Client, url: str, **k: object) -> httpx.Response:
        seen.append(url)
        req = httpx.Request("GET", url)
        if url.endswith("/models"):
            body = {"data": [{"id": "m7", "root": "Org/Model-7B-AWQ", "max_model_len": 16384}]}
            return httpx.Response(200, json=body, request=req)
        return httpx.Response(200, json={"version": "0.0.test"}, request=req)

    monkeypatch.setattr(httpx.Client, "get", get)
    info = probe("http://127.0.0.1:8000/v1", "k")
    assert info["vllm_version"] == "0.0.test" and info["models"][0]["id"] == "m7"
    assert seen == ["http://127.0.0.1:8000/v1/models", "http://127.0.0.1:8000/version"]
