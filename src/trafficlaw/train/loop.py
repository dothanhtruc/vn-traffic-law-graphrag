"""Vòng huấn luyện chung cho embedder và reranker (M14, torch, GPU đơn).

- AdamW (không weight decay cho bias/LayerNorm) + LambdaLR warmup tuyến tính rồi giảm tuyến tính.
- Trộn độ chính xác: trọng số fp32, autocast bf16 (GPU không hỗ trợ bf16 → fp16 + GradScaler);
  CPU (test) → fp32.
- Kế hoạch bước tính trước cho mọi epoch (``data.training_plan``, tất định theo seed) ⇒ resume
  bỏ qua đúng số batch đã chạy.
- CUDA OOM → giảm mini-batch một nửa (batch hiệu dụng không đổi), ghi log, chạy lại đúng bước.
- Đánh giá val cuối mỗi epoch (+ mỗi ``eval_steps``); checkpoint mỗi ``save_steps`` và cuối
  epoch, đẩy HF Hub (luồng nền). Checkpoint tốt nhất theo :func:`evaluate.selection_key` (so sánh
  chặt ⇒ hoà giữ bản sớm hơn) lưu ``best/``, cuối run đẩy lên repo model.
"""

from __future__ import annotations

import contextlib
import logging
import shutil
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import torch

from trafficlaw.train.checkpoint import (
    HubSync,
    latest_checkpoint,
    load_checkpoint,
    prune_checkpoints,
    read_state,
    save_checkpoint,
)
from trafficlaw.train.config import TrainParams
from trafficlaw.train.evaluate import selection_key
from trafficlaw.train.run_log import RunLog, gpu_cost

logger = logging.getLogger(__name__)


class ResumeMismatchError(RuntimeError):
    """Checkpoint có sẵn được tạo với tham số/dữ liệu khác."""


@dataclass
class StepCtx:
    device: str
    amp_dtype: torch.dtype | None
    scaler: Any | None

    def autocast(self) -> contextlib.AbstractContextManager:
        if self.amp_dtype is None:
            return contextlib.nullcontext()
        return torch.autocast(device_type="cuda", dtype=self.amp_dtype)

    def backward(self, t: torch.Tensor) -> None:
        if self.scaler is not None:
            self.scaler.scale(t).backward()
        else:
            t.backward()


@dataclass
class Task:
    model: torch.nn.Module
    plan: list[tuple[int, list[int]]]
    step_fn: Callable[[list[int], int, StepCtx], float]
    """(chỉ số ví dụ của batch, mini-batch, ctx) → loss; tự gọi backward."""
    evaluate: Callable[[StepCtx], dict[str, Any]] | None
    save_model: Callable[[Path], None]
    load_model: Callable[[Path], None]
    fingerprint: dict[str, Any]
    info: dict[str, Any] = field(default_factory=dict)


def amp_dtype_for(device: str, want: str) -> torch.dtype | None:
    if device != "cuda" or want == "fp32":
        return None
    return torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16


def param_groups(model: torch.nn.Module, weight_decay: float) -> list[dict[str, Any]]:
    decay, no_decay = [], []
    for n, p in model.named_parameters():
        if not p.requires_grad:
            continue
        low = n.lower()
        (no_decay if ("bias" in low or "norm" in low) else decay).append(p)
    return [
        {"params": decay, "weight_decay": weight_decay},
        {"params": no_decay, "weight_decay": 0.0},
    ]


def linear_schedule(warmup: int, total: int) -> Callable[[int], float]:
    def f(s: int) -> float:
        if warmup > 0 and s < warmup:
            return (s + 1) / warmup
        return max(0.0, (total - s) / max(1, total - warmup))

    return f


def _is_epoch_end(plan: list[tuple[int, list[int]]], i: int) -> bool:
    return i == len(plan) - 1 or plan[i + 1][0] != plan[i][0]


def _peak_gb() -> float | None:
    if not torch.cuda.is_available():
        return None
    return round(torch.cuda.max_memory_allocated() / 2**30, 3)


def run_loop(
    task: Task,
    params: TrainParams,
    *,
    run_dir: Path,
    log: RunLog,
    hub: HubSync,
    device: str,
    max_steps: int | None = None,
    stop_after: int | None = None,
    push_best: bool = True,
    price_vnd_per_hour: float = 17_000,
) -> dict[str, Any]:
    """Huấn luyện tới hết ``task.plan`` (hoặc ``max_steps`` — dry-run). ``stop_after`` dừng sau
    N bước của lần chạy này (mô phỏng máy bị tắt, chỉ dùng trong test)."""
    t_start = time.perf_counter()
    run_dir.mkdir(parents=True, exist_ok=True)
    plan = task.plan if max_steps is None else task.plan[:max_steps]
    total = len(plan)
    model = task.model
    amp = amp_dtype_for(device, params.dtype)
    scaler = torch.amp.GradScaler("cuda") if amp == torch.float16 else None
    ctx = StepCtx(device=device, amp_dtype=amp, scaler=scaler)
    opt = torch.optim.AdamW(param_groups(model, params.weight_decay), lr=params.lr)
    warm = int(round(params.warmup_ratio * total))
    sched = torch.optim.lr_scheduler.LambdaLR(opt, linear_schedule(warm, total))
    fp = {**task.fingerprint, "total_steps": total}
    state: dict[str, Any] = {
        "fingerprint": fp,
        "micro": params.mini_batch_size,
        "best": None,
        "best_step": None,
        "evals": [],
    }
    step = 0
    ck = latest_checkpoint(run_dir) or hub.fetch_last(run_dir / "hub")
    if ck is not None:
        prev = read_state(ck)
        if prev.get("fingerprint") != fp:
            raise ResumeMismatchError(
                f"{ck} tạo với tham số/dữ liệu khác — xoá thư mục run hoặc đổi tên run"
            )
        state = load_checkpoint(
            ck, load_model=task.load_model, optimizer=opt, scheduler=sched, scaler=scaler
        )
        step = int(state.pop("step"))
        if state.get("best_step") is not None and not (run_dir / "best").is_dir():
            log.event("best_lost", best_step=state["best_step"])
            state["best"], state["best_step"] = None, None
        log.event("resume", step=step, checkpoint=str(ck))
    model.train()
    log.event(
        "start",
        step=step,
        total_steps=total,
        warmup_steps=warm,
        params=params.model_dump(),
        amp=str(amp),
        device=device,
        **task.info,
    )
    if params.eval_at_start and step == 0 and task.evaluate is not None:
        log.event("eval", step=0, metrics=_evaluate(task, model, ctx))

    def evaluate_now(s: int) -> None:
        if task.evaluate is None:
            return
        m = _evaluate(task, model, ctx)
        state["evals"].append({"step": s, "metrics": m})
        log.event("eval", step=s, epoch=plan[s - 1][0], metrics=m)
        if state["best"] is None or selection_key(m) > selection_key(state["best"]):
            tmp, dst = run_dir / ".tmp-best", run_dir / "best"
            if tmp.exists():
                shutil.rmtree(tmp)
            task.save_model(tmp)
            if dst.exists():
                shutil.rmtree(dst)
            tmp.rename(dst)
            state["best"], state["best_step"] = m, s
            log.event("best", step=s, metrics=m)

    def checkpoint_now(s: int) -> None:
        t0 = time.perf_counter()
        p = save_checkpoint(
            run_dir, s, save_model=task.save_model, optimizer=opt, scheduler=sched,
            scaler=scaler, state=state,
        )  # fmt: skip
        started = hub.push_checkpoint(p, s)
        prune_checkpoints(run_dir, keep=2, protect=hub.uploading)
        log.event(
            "checkpoint", step=s, path=str(p), save_s=round(time.perf_counter() - t0, 2),
            hub_push=started, hub_busy=hub.busy(), hub_error=hub.last_error,
        )  # fmt: skip

    n_run = 0
    losses: list[float] = []
    while step < total:
        if stop_after is not None and n_run >= stop_after:
            log.event("stopped", step=step)
            hub.close()
            return {"stopped_at": step}
        _, batch = plan[step]
        while True:
            try:
                opt.zero_grad(set_to_none=True)
                loss = task.step_fn(batch, int(state["micro"]), ctx)
                break
            except torch.cuda.OutOfMemoryError:
                if state["micro"] <= 1:
                    raise
                opt.zero_grad(set_to_none=True)
                torch.cuda.empty_cache()
                state["micro"] = max(1, int(state["micro"]) // 2)
                log.event("oom", step=step, new_micro=state["micro"], peak_vram_gb=_peak_gb())
                if torch.cuda.is_available():
                    torch.cuda.reset_peak_memory_stats()
        if scaler is not None:
            scaler.unscale_(opt)
        gn = torch.nn.utils.clip_grad_norm_(model.parameters(), params.max_grad_norm)
        if scaler is not None:
            scaler.step(opt)
            scaler.update()
        else:
            opt.step()
        sched.step()
        step += 1
        n_run += 1
        losses.append(loss)
        if step % params.log_steps == 0 or step == total:
            log.event(
                "step", step=step, loss=round(sum(losses) / len(losses), 5),
                lr=sched.get_last_lr()[0], grad_norm=round(float(gn), 4),
                micro=state["micro"], peak_vram_gb=_peak_gb(),
            )  # fmt: skip
            losses = []
        i = step - 1
        epoch_end = _is_epoch_end(plan, i)
        if epoch_end or (params.eval_steps and step % params.eval_steps == 0):
            evaluate_now(step)
        if epoch_end or step % params.save_steps == 0:
            checkpoint_now(step)
    hub.wait()
    best_commit = None
    if push_best and state["best_step"] is not None and (run_dir / "best").is_dir():
        t0 = time.perf_counter()
        try:
            best_commit = hub.push_model(run_dir / "best", f"best step {state['best_step']}")
        except Exception as e:  # giữ bản cục bộ, đẩy lại sau (scripts --push-best)
            log.event("hub_error", what="best", error=f"{type(e).__name__}")
            best_commit = None
        log.event(
            "hub", what="best", step=state["best_step"], commit=best_commit,
            repo=hub.model_repo if hub.enabled else None,
            seconds=round(time.perf_counter() - t0, 1),
        )  # fmt: skip
        last = latest_checkpoint(run_dir)
        if last is not None and hub.enabled and best_commit is not None:
            c = hub.push_model(last / "model", f"final step {step}", repo=hub.ckpt_repo,
                               path_in_repo="final")  # fmt: skip
            log.event("hub", what="final", step=step, commit=c)
    hub.close()
    secs = time.perf_counter() - t_start
    summary = {
        "steps": step,
        "best_step": state["best_step"],
        "best": state["best"],
        "best_commit": best_commit,
        "peak_vram_gb": _peak_gb(),
        "seconds": round(secs, 1),
        **gpu_cost(secs, price_vnd_per_hour),
    }
    log.event("end", **summary)
    return summary


def _evaluate(task: Task, model: torch.nn.Module, ctx: StepCtx) -> dict[str, Any]:
    assert task.evaluate is not None
    model.eval()
    t0 = time.perf_counter()
    try:
        with torch.inference_mode():
            m = task.evaluate(ctx)
    finally:
        model.train()
    m["eval_s"] = round(time.perf_counter() - t0, 1)
    return m


__all__ = [
    "ResumeMismatchError",
    "StepCtx",
    "Task",
    "amp_dtype_for",
    "linear_schedule",
    "param_groups",
    "run_loop",
]
