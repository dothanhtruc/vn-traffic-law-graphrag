"""Model tự host (vLLM trên GPU thuê, gọi qua SSH tunnel): cấu hình ``configs/serve.yaml``, dựng
lệnh ``vllm serve``, thăm dò server, ước tính giờ GPU.

Mọi model của dự án tự host (quyết định 09/11/2026). Mỗi mục trong ``models`` ghim
``hf_repo`` + ``revision`` (commit) + lượng tử hoá; ``served_model_name`` là ``model_id`` mà
lớp LLM gửi lên (provider ``local``). Server chỉ nghe ``127.0.0.1`` trên máy thuê; máy local
gọi qua ``ssh -L``. API key của server đọc từ biến ``VLLM_API_KEY`` trên máy thuê (không nằm trong
dòng lệnh) và bằng ``LOCAL_LLM_API_KEY`` ở máy local.
"""

from __future__ import annotations

import shlex
from pathlib import Path
from typing import Any

import httpx
import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator

from trafficlaw.llm.types import LLMTimeoutError


class RemoteConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    ssh_host: str = "gpu-aidev"
    """Alias trong ``~/.ssh/config`` của người dùng (host/IP/key không nằm trong repo)."""
    remote_dir: str = "~/GraphRAG"
    vllm_venv: str = "~/.venvs/vllm"
    env_file: str = "~/.config/graphrag/env"
    """File quyền 600 trên máy thuê chứa ``VLLM_API_KEY``, ``HF_TOKEN`` (ghi bằng stdin)."""
    local_port: int = 8000
    price_vnd_per_hour: int = 15_000


class ServeModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
    hf_repo: str
    revision: str | None = None
    """Commit HF ghim để tái lập; ``null`` chỉ chấp nhận khi thử nghiệm chọn model."""
    served_model_name: str
    quantization: str | None = None
    dtype: str = "auto"
    max_model_len: int = 16384
    gpu_memory_utilization: float = 0.90
    port: int = 8000
    extra_args: list[str] = Field(default_factory=list)
    role: str = "candidate"
    """``main`` | ``annotator`` | ``judge`` | ``candidate``."""
    family: str
    """Họ model (vd ``qwen``): model gán nháp/judge phải khác họ với model chính."""
    prefill_tps: float | None = None
    decode_tps: float | None = None
    """Token/giây gộp đo được trên 3090 (null → dùng giá trị mặc định thận trọng)."""


class ServeConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    vllm_version: str | None = None
    remote: RemoteConfig = Field(default_factory=RemoteConfig)
    default_prefill_tps: float = 4000.0
    default_decode_tps: float = 400.0
    models: dict[str, ServeModel] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _unique_names(self) -> ServeConfig:
        names = [m.served_model_name for m in self.models.values()]
        dup = sorted({n for n in names if names.count(n) > 1})
        if dup:
            raise ValueError(f"served_model_name trùng: {dup}")
        return self

    def by_served_name(self, name: str) -> tuple[str, ServeModel] | None:
        for k, m in self.models.items():
            if m.served_model_name == name:
                return k, m
        return None

    def get(self, key_or_name: str) -> tuple[str, ServeModel]:
        if key_or_name in self.models:
            return key_or_name, self.models[key_or_name]
        hit = self.by_served_name(key_or_name)
        if hit is None:
            raise KeyError(f"không có model '{key_or_name}' trong configs/serve.yaml")
        return hit


def load_serve_config(path: str | Path) -> ServeConfig:
    return ServeConfig.model_validate(yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {})


def vllm_args(m: ServeModel) -> list[str]:
    """Đối số ``vllm serve`` (không có API key — server đọc ``VLLM_API_KEY`` từ môi trường)."""
    args = [
        "serve",
        m.hf_repo,
        "--served-model-name",
        m.served_model_name,
        "--host",
        "127.0.0.1",
        "--port",
        str(m.port),
        "--dtype",
        m.dtype,
        "--max-model-len",
        str(m.max_model_len),
        "--gpu-memory-utilization",
        str(m.gpu_memory_utilization),
        "--enable-prefix-caching",
        "--seed",
        "42",
    ]
    if m.revision:
        args += ["--revision", m.revision]
    if m.quantization:
        args += ["--quantization", m.quantization]
    return args + list(m.extra_args)


def shell_path(p: str) -> str:
    """Đường dẫn cho bash: ``~/x y`` → ``"$HOME"/'x y'`` (giữ mở rộng thư mục nhà, vẫn quote)."""
    if p.startswith("~/"):
        return '"$HOME"/' + shlex.quote(p[2:])
    return shlex.quote(p)


def remote_serve_script(cfg: ServeConfig, key: str) -> str:
    """Script bash chạy trên máy thuê (trong tmux): nạp env (key, HF token), chạy vLLM, log ra
    ``<remote_dir>/logs/vllm-<key>.log``."""
    _, m = cfg.get(key)
    r = cfg.remote
    cmd = shell_path(f"{r.vllm_venv}/bin/vllm") + " " + shlex.join(vllm_args(m))
    return "\n".join(
        [
            "#!/usr/bin/env bash",
            "set -euo pipefail",
            f"set -a; . {shell_path(r.env_file)}; set +a",
            # venv vLLM vào PATH: Triton/torch.compile gọi `ninja` của venv lúc khởi động.
            f'export PATH={shell_path(r.vllm_venv + "/bin")}:"$PATH"',
            f"mkdir -p {shell_path(r.remote_dir + '/logs')}",
            f"{cmd} 2>&1 | tee -a {shell_path(f'{r.remote_dir}/logs/vllm-{key}.log')}",
            "",
        ]
    )


def probe(base_url: str, api_key: str, *, timeout_s: float = 10.0) -> dict[str, Any]:
    """``/v1/models`` + ``/version`` của server vLLM. Không kết nối được → ``LLMTimeoutError``
    (thường là tunnel chưa mở hoặc server chưa chạy)."""
    root = base_url.rstrip("/")
    headers = {"Authorization": f"Bearer {api_key}"}
    try:
        with httpx.Client(timeout=timeout_s, headers=headers) as c:
            models = c.get(f"{root}/models")
            models.raise_for_status()
            ver_url = root.rsplit("/v1", 1)[0] + "/version"
            ver = c.get(ver_url)
            version = ver.json().get("version") if ver.status_code == 200 else None
    except httpx.TransportError as e:
        raise LLMTimeoutError(
            f"không kết nối được {root} ({type(e).__name__}) — tunnel SSH chưa mở hoặc vLLM "
            "chưa chạy (scripts/gpu/tunnel.sh, scripts/gpu/gpu.sh serve <model>)",
            provider="local",
        ) from None
    data = models.json().get("data") or []
    return {
        "models": [
            {"id": d.get("id"), "root": d.get("root"), "max_model_len": d.get("max_model_len")}
            for d in data
        ],
        "vllm_version": version,
    }


def run_meta(cfg: ServeConfig, served_name: str, probed: dict[str, Any] | None) -> dict[str, Any]:
    """Thông tin tái lập ghi vào mỗi bản ghi kết quả."""
    hit = cfg.by_served_name(served_name)
    m = hit[1] if hit else None
    return {
        "served_model": served_name,
        "hf_repo": m.hf_repo if m else None,
        "revision": m.revision if m else None,
        "quantization": m.quantization if m else None,
        "vllm_version": (probed or {}).get("vllm_version") or cfg.vllm_version,
    }


def gpu_hours(
    cfg: ServeConfig, served_name: str | None, prompt_tokens: int, output_tokens: int
) -> tuple[float, int]:
    """(giờ GPU, VND) ước tính = prefill + decode theo token/giây gộp (đo được hoặc mặc định)."""
    hit = cfg.by_served_name(served_name) if served_name else None
    m = hit[1] if hit else None
    pre = (m.prefill_tps if m and m.prefill_tps else None) or cfg.default_prefill_tps
    dec = (m.decode_tps if m and m.decode_tps else None) or cfg.default_decode_tps
    hours = (prompt_tokens / pre + output_tokens / dec) / 3600
    return hours, round(hours * cfg.remote.price_vnd_per_hour)


__all__ = [
    "RemoteConfig",
    "ServeConfig",
    "ServeModel",
    "gpu_hours",
    "load_serve_config",
    "probe",
    "remote_serve_script",
    "run_meta",
    "vllm_args",
]
