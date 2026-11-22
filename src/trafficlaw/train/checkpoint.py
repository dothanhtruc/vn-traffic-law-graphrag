"""Checkpoint + HF Hub cho M14 (CLAUDE.md mục 9: model + optimizer + scheduler + RNG + step, đẩy HF
Hub private, luôn thử resume).

Bố cục cục bộ ``<output_dir>/<run>/``::

    ckpt-<step>/model/            trọng số (định dạng của model cuối: sentence-transformers / HF)
    ckpt-<step>/optimizer.pt      AdamW
    ckpt-<step>/scheduler.pt      LambdaLR (warmup + giảm tuyến tính)
    ckpt-<step>/scaler.pt         GradScaler (chỉ khi fp16)
    ckpt-<step>/rng.pt            random, numpy, torch CPU, mọi GPU
    ckpt-<step>/trainer_state.json  step, mini-batch, best, hash tham số + dữ liệu
    best/                         trọng số checkpoint tốt nhất theo val

HF Hub (namespace = ``whoami`` lúc chạy, không ghi vào repo): ``<ns>/<run>-ckpt`` — thư mục
``last/`` = checkpoint mới nhất (đẩy luồng nền), ``final/`` = trọng số cuối; ``<ns>/<run>`` —
trọng số tốt nhất ở gốc repo (commit sha ⇒ ``revision`` ghim trong ``retrieval.yaml``).
"""

from __future__ import annotations

import json
import logging
import random
import shutil
from collections.abc import Callable
from concurrent.futures import Future, ThreadPoolExecutor
from pathlib import Path
from typing import Any

import numpy as np
import torch

logger = logging.getLogger(__name__)

STATE = "trainer_state.json"


def save_checkpoint(
    run_dir: Path,
    step: int,
    *,
    save_model: Callable[[Path], None],
    optimizer: Any,
    scheduler: Any,
    scaler: Any | None,
    state: dict[str, Any],
) -> Path:
    """Ghi vào thư mục tạm rồi đổi tên (không bao giờ có checkpoint ghi dở mang tên thật)."""
    final = run_dir / f"ckpt-{step:06d}"
    tmp = run_dir / f".tmp-ckpt-{step:06d}"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True)
    save_model(tmp / "model")
    torch.save(optimizer.state_dict(), tmp / "optimizer.pt")
    torch.save(scheduler.state_dict(), tmp / "scheduler.pt")
    if scaler is not None:
        torch.save(scaler.state_dict(), tmp / "scaler.pt")
    rng = {
        "python": random.getstate(),
        "numpy": np.random.get_state(),
        "torch": torch.get_rng_state(),
        "cuda": torch.cuda.get_rng_state_all() if torch.cuda.is_available() else None,
    }
    torch.save(rng, tmp / "rng.pt")
    (tmp / STATE).write_text(
        json.dumps({**state, "step": step}, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    if final.exists():
        shutil.rmtree(final)
    tmp.rename(final)
    return final


def latest_checkpoint(run_dir: Path) -> Path | None:
    cands = sorted(p for p in run_dir.glob("ckpt-*") if (p / STATE).is_file())
    return cands[-1] if cands else None


def read_state(ckpt: Path) -> dict[str, Any]:
    return json.loads((ckpt / STATE).read_text(encoding="utf-8"))


def load_checkpoint(
    ckpt: Path, *, load_model: Callable[[Path], None], optimizer: Any, scheduler: Any,
    scaler: Any | None,
) -> dict[str, Any]:  # fmt: skip
    load_model(ckpt / "model")
    optimizer.load_state_dict(torch.load(ckpt / "optimizer.pt", weights_only=False))
    scheduler.load_state_dict(torch.load(ckpt / "scheduler.pt", weights_only=False))
    if scaler is not None and (ckpt / "scaler.pt").is_file():
        scaler.load_state_dict(torch.load(ckpt / "scaler.pt", weights_only=False))
    rng = torch.load(ckpt / "rng.pt", weights_only=False)
    random.setstate(rng["python"])
    np.random.set_state(rng["numpy"])
    torch.set_rng_state(rng["torch"])
    if rng.get("cuda") is not None and torch.cuda.is_available():
        torch.cuda.set_rng_state_all(rng["cuda"])
    return read_state(ckpt)


def prune_checkpoints(run_dir: Path, keep: int = 2, protect: Path | None = None) -> None:
    cands = sorted(p for p in run_dir.glob("ckpt-*") if (p / STATE).is_file())
    for p in cands[:-keep] if keep > 0 else cands:
        if protect is not None and p.resolve() == protect.resolve():
            continue
        shutil.rmtree(p, ignore_errors=True)


def _err(e: Exception) -> str:
    """Mô tả lỗi ngắn (dòng đầu thông điệp; không chứa token)."""
    first = (str(e).strip().splitlines() or [""])[0]
    return f"{type(e).__name__}: {first[:200]}"


class HubSync:
    """Đẩy/kéo HF Hub. ``api`` = ``huggingface_hub.HfApi`` (token đọc từ ``HF_TOKEN``, không in);
    test truyền api giả. ``enabled=False`` → mọi thao tác là no-op."""

    def __init__(
        self,
        run_name: str,
        *,
        enabled: bool = True,
        private: bool = True,
        push_checkpoints: bool = True,
        api: Any = None,
    ) -> None:
        self.run_name = run_name
        self.enabled = enabled
        self.private = private
        self.push_checkpoints = push_checkpoints
        self._api = api
        self._ns: str | None = None
        self._pool = ThreadPoolExecutor(max_workers=1) if enabled else None
        self._future: Future | None = None
        self.uploading: Path | None = None
        self._created: set[str] = set()
        self.last_error: str | None = None

    @property
    def api(self) -> Any:
        if self._api is None:
            from huggingface_hub import HfApi

            self._api = HfApi()
        return self._api

    @property
    def namespace(self) -> str:
        if self._ns is None:
            self._ns = str(self.api.whoami()["name"])
        return self._ns

    @property
    def model_repo(self) -> str:
        return f"{self.namespace}/{self.run_name}"

    @property
    def ckpt_repo(self) -> str:
        return f"{self.namespace}/{self.run_name}-ckpt"

    def _ensure(self, repo: str) -> None:
        if repo not in self._created:
            self.api.create_repo(repo, private=self.private, exist_ok=True)
            self._created.add(repo)

    def busy(self) -> bool:
        return self._future is not None and not self._future.done()

    def push_checkpoint(self, ckpt: Path, step: int) -> bool:
        """Đẩy nền ``ckpt`` vào ``<run>-ckpt/last``; lần trước chưa xong → bỏ qua (trả False)."""
        if not (self.enabled and self.push_checkpoints):
            return False
        if self.busy():
            return False
        self.wait()
        try:
            self._ensure(self.ckpt_repo)
        except Exception as e:  # token thiếu quyền / mạng: huấn luyện vẫn tiếp tục
            self.last_error = _err(e)
            logger.warning("HF Hub: không tạo được repo checkpoint — %s", self.last_error)
            return False
        self.uploading = ckpt
        assert self._pool is not None
        self._future = self._pool.submit(
            self.api.upload_folder,
            repo_id=self.ckpt_repo,
            folder_path=str(ckpt),
            path_in_repo="last",
            commit_message=f"checkpoint step {step}",
        )
        return True

    def wait(self) -> Any:
        """Chờ lần đẩy nền đang chạy; lỗi đẩy chỉ ghi log (không dừng huấn luyện)."""
        if self._future is None:
            return None
        try:
            return self._future.result()
        except Exception as e:  # mạng/HF lỗi: checkpoint cục bộ vẫn còn
            self.last_error = _err(e)
            logger.warning("Đẩy checkpoint lên HF Hub lỗi: %s", self.last_error)
            return None
        finally:
            self._future = None
            self.uploading = None

    def push_model(self, folder: Path, message: str, *, repo: str | None = None,
                   path_in_repo: str | None = None) -> str | None:  # fmt: skip
        """Đẩy đồng bộ; trả commit sha (``None`` khi tắt)."""
        if not self.enabled:
            return None
        repo = repo or self.model_repo
        self._ensure(repo)
        info = self.api.upload_folder(
            repo_id=repo, folder_path=str(folder), path_in_repo=path_in_repo,
            commit_message=message,
        )  # fmt: skip
        return str(getattr(info, "oid", None) or "") or None

    def fetch_last(self, dest: Path) -> Path | None:
        """Kéo ``<run>-ckpt/last`` về ``dest/last`` (repo chưa có → ``None``)."""
        if not self.enabled:
            return None
        try:
            self.api.snapshot_download(
                repo_id=self.ckpt_repo, allow_patterns=["last/*", "last/**"], local_dir=str(dest)
            )
        except Exception as e:  # repo chưa tồn tại / chưa có checkpoint
            logger.info("Không có checkpoint trên HF Hub (%s)", type(e).__name__)
            return None
        last = dest / "last"
        return last if (last / STATE).is_file() else None

    def close(self) -> None:
        self.wait()
        if self._pool is not None:
            self._pool.shutdown(wait=True)


__all__ = [
    "HubSync",
    "STATE",
    "latest_checkpoint",
    "load_checkpoint",
    "prune_checkpoints",
    "read_state",
    "save_checkpoint",
]
