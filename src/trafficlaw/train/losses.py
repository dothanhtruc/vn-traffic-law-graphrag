"""Loss M14 (torch).

- :func:`cached_mnrl_step` = ``CachedMultipleNegativesRankingLoss`` (GradCache, Gao et al. 2021):
  batch hiệu dụng lớn (128) với bộ nhớ của mini-batch (32). Bước 1: embed mọi mini-batch không
  grad (ghi lại trạng thái RNG để dropout giống hệt); bước 2: loss MNRL trên toàn batch với
  embedding tách rời → grad theo embedding; bước 3: embed lại từng mini-batch có grad (khôi phục
  RNG) và lan truyền ngược ``Σ emb · grad``. Gradient bằng đúng gradient của MNRL trên cả batch
  (có test so với cách tính trực tiếp).
- MNRL: câu hỏi i đối với mọi passage trong batch (positive của mọi câu + mọi hard negative),
  logit = ``scale`` × cosine, nhãn = positive của câu i.
- :func:`listwise_loss`: reranker — softmax cross-entropy trên nhóm (positive ở vị trí 0 + các
  negative), trung bình theo nhóm.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator, Sequence
from contextlib import contextmanager
from typing import Any

import torch
import torch.nn.functional as F  # noqa: N812


class RandState:
    """Trạng thái RNG (CPU + mọi GPU) tại thời điểm tạo; ``restore()`` chạy lại với đúng trạng
    thái đó mà không làm lệch RNG bên ngoài."""

    def __init__(self) -> None:
        self.cpu = torch.get_rng_state()
        self.cuda = torch.cuda.get_rng_state_all() if torch.cuda.is_available() else None

    @contextmanager
    def restore(self) -> Iterator[None]:
        devices = list(range(torch.cuda.device_count())) if self.cuda is not None else []
        with torch.random.fork_rng(devices=devices):
            torch.set_rng_state(self.cpu)
            if self.cuda is not None:
                torch.cuda.set_rng_state_all(self.cuda)
            yield


def mnrl_loss(q: torch.Tensor, p: torch.Tensor, scale: float) -> torch.Tensor:
    """``q`` (n, d), ``p`` (m, d), m ≥ n, ``p[i]`` là positive của ``q[i]``; vector đã chuẩn hoá."""
    logits = scale * (q @ p.T)
    labels = torch.arange(q.shape[0], device=q.device)
    return F.cross_entropy(logits, labels)


def listwise_loss(logits: Sequence[torch.Tensor]) -> torch.Tensor:
    """Mỗi phần tử: logit của một nhóm (positive ở vị trí 0)."""
    losses = [F.cross_entropy(g.view(1, -1).float(), g.new_zeros(1, dtype=torch.long))
              for g in logits]  # fmt: skip
    return torch.stack(losses).mean()


Embed = Callable[[Any], torch.Tensor]
Backward = Callable[[torch.Tensor], None]


def _plain_backward(t: torch.Tensor) -> None:
    t.backward()


def cached_mnrl_step(
    embed: Embed,
    q_batches: Sequence[Any],
    p_batches: Sequence[Any],
    scale: float,
    *,
    backward: Backward = _plain_backward,
) -> float:
    """``q_batches``/``p_batches``: các mini-batch đầu vào của ``embed`` (đã tách); passage xếp
    positive của mọi câu trước (đúng thứ tự câu) rồi tới negative. Gọi backward lên tham số model;
    trả giá trị loss."""
    reps: list[list[torch.Tensor]] = [[], []]
    states: list[list[RandState]] = [[], []]
    with torch.no_grad():
        for side, batches in enumerate((q_batches, p_batches)):
            for f in batches:
                states[side].append(RandState())
                reps[side].append(embed(f).float())
    q = torch.cat(reps[0]).detach().requires_grad_()
    p = torch.cat(reps[1]).detach().requires_grad_()
    loss = mnrl_loss(q, p, scale)
    loss.backward()
    assert q.grad is not None and p.grad is not None
    grads = [
        q.grad.split([r.shape[0] for r in reps[0]]),
        p.grad.split([r.shape[0] for r in reps[1]]),
    ]
    for side, batches in enumerate((q_batches, p_batches)):
        for f, st, g in zip(batches, states[side], grads[side], strict=True):
            with st.restore():
                r = embed(f).float()
            backward((r * g).sum())
    return float(loss.detach())


__all__ = ["RandState", "cached_mnrl_step", "listwise_loss", "mnrl_loss"]
