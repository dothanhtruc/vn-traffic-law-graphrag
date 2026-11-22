"""M14: loss — GradCache cho cùng gradient với MNRL tính trực tiếp (kể cả dropout); listwise."""

from __future__ import annotations

import math

import pytest

torch = pytest.importorskip("torch")

from trafficlaw.train.losses import (  # noqa: E402
    RandState,
    cached_mnrl_step,
    listwise_loss,
    mnrl_loss,
)


class Enc(torch.nn.Module):
    def __init__(self) -> None:
        super().__init__()
        torch.manual_seed(0)
        self.lin = torch.nn.Linear(6, 4)
        self.drop = torch.nn.Dropout(0.3)

    def forward(self, x):
        return torch.nn.functional.normalize(self.drop(self.lin(x)), dim=-1)


def test_cached_equals_direct_with_dropout() -> None:
    torch.manual_seed(1)
    q, p = torch.randn(8, 6), torch.randn(12, 6)  # 8 positive + 4 negative
    m = Enc()
    m.train()

    torch.manual_seed(7)
    st = RandState()
    loss_c = cached_mnrl_step(m, list(q.split(3)), list(p.split(5)), 20.0)
    g_cached = [x.grad.clone() for x in m.parameters()]

    m.zero_grad()
    # Tính trực tiếp với đúng dropout mask: chạy lại theo đúng thứ tự RNG của bước 1.
    with st.restore():
        reps_q = [m(x) for x in q.split(3)]
        reps_p = [m(x) for x in p.split(5)]
    loss_d = mnrl_loss(torch.cat(reps_q), torch.cat(reps_p), 20.0)
    loss_d.backward()
    assert loss_c == pytest.approx(float(loss_d.detach()), rel=1e-5)
    for a, b in zip(g_cached, (x.grad for x in m.parameters()), strict=True):
        assert torch.allclose(a, b, atol=1e-5)


def test_randstate_restore_does_not_shift_outer_rng() -> None:
    torch.manual_seed(3)
    st = RandState()
    a = torch.rand(3)
    with st.restore():
        b = torch.rand(3)
    c = torch.rand(3)
    torch.manual_seed(3)
    torch.rand(3)
    assert torch.equal(a, b) and torch.equal(c, torch.rand(3))


def test_mnrl_perfect_and_listwise() -> None:
    e = torch.eye(3)
    assert float(mnrl_loss(e, e, 20.0)) < 1e-6
    lg = [torch.tensor([5.0, 0.0, 0.0]), torch.tensor([0.0, 0.0])]
    exp = (-math.log(math.exp(5) / (math.exp(5) + 2)) + math.log(2)) / 2
    assert float(listwise_loss(lg)) == pytest.approx(exp, rel=1e-5)
