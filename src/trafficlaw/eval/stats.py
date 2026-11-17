"""Thống kê cho M13 (thuần Python, không scipy — CLAUDE.md mục 10, người dùng chốt 17/11/2026).

- ``bootstrap_mean_ci``: CI 95% (phân vị 2,5 / 97,5) của trung bình, lấy mẫu lại câu có hoàn lại,
  ``n`` lần, ``random.Random(seed)`` — cùng cách với ``retrieval_metrics.bootstrap_ci`` (M10).
  ``bootstrap_diff_ci``: CI của hiệu trung bình **ghép cặp** (cùng câu, cùng chỉ số lấy mẫu).
- ``mcnemar_exact``: McNemar chính xác 2 phía cho chỉ số đúng/sai ghép cặp: chỉ dùng hai ô lệch
  ``b`` (A đúng, B sai) và ``c`` (A sai, B đúng); p = min(1, 2·P[X ≤ min(b, c)]) với
  X ~ Binomial(b + c, 1/2). b + c = 0 ⇒ p = 1.
- ``wilcoxon_signed_rank``: hạng dấu Wilcoxon 2 phía, **Pratt** (hiệu 0 vẫn được xếp hạng rồi bỏ
  khỏi tổng hạng; kỳ vọng/phương sai chỉnh theo Cureton 1967), hiệu chỉnh hạng hoà, xấp xỉ chuẩn
  không hiệu chỉnh liên tục — trùng ``scipy.stats.wilcoxon(zero_method="pratt",
  correction=False, method="approx")``. Thống kê T = min(R+, R−).
- ``holm``: hiệu chỉnh Holm–Bonferroni (p đã chỉnh, giữ thứ tự đầu vào, đơn điệu, ≤ 1).
- ``cohen_kappa``: κ của Cohen cho hai người chấm trên cùng tập mục (nhãn rời rạc).
"""

from __future__ import annotations

import math
import random
from collections import Counter
from collections.abc import Hashable, Sequence
from dataclasses import dataclass


def mean(xs: Sequence[float]) -> float | None:
    return sum(xs) / len(xs) if xs else None


def _percentile_ci(boots: list[float], n: int) -> tuple[float, float]:
    boots.sort()
    return boots[int(0.025 * n)], boots[min(n - 1, int(0.975 * n))]


def bootstrap_mean_ci(
    values: Sequence[float], *, n: int = 1000, seed: int = 42
) -> tuple[float, float] | None:
    if not values:
        return None
    rng = random.Random(seed)
    m = len(values)
    boots = [sum(values[rng.randrange(m)] for _ in range(m)) / m for _ in range(n)]
    return _percentile_ci(boots, n)


def bootstrap_diff_ci(
    a: Sequence[float], b: Sequence[float], *, n: int = 1000, seed: int = 42
) -> tuple[float, float] | None:
    """CI của mean(a − b), ``a``/``b`` ghép theo vị trí (cùng câu)."""
    if len(a) != len(b):
        raise ValueError("a, b phải cùng độ dài (ghép cặp theo câu)")
    return bootstrap_mean_ci([x - y for x, y in zip(a, b, strict=True)], n=n, seed=seed)


# --------------------------------------------------------------------------- McNemar


@dataclass(frozen=True)
class McNemar:
    b: int
    """A đúng, B sai."""
    c: int
    """A sai, B đúng."""
    p: float


def binom_cdf_half(k: int, n: int) -> float:
    """P[X ≤ k], X ~ Binomial(n, 1/2) — tính chính xác bằng số nguyên."""
    if k < 0:
        return 0.0
    if k >= n:
        return 1.0
    s = sum(math.comb(n, i) for i in range(k + 1))
    return s / 2**n


def mcnemar_exact(a: Sequence[bool], b: Sequence[bool]) -> McNemar:
    if len(a) != len(b):
        raise ValueError("a, b phải cùng độ dài (ghép cặp theo câu)")
    bb = sum(1 for x, y in zip(a, b, strict=True) if x and not y)
    cc = sum(1 for x, y in zip(a, b, strict=True) if y and not x)
    nd = bb + cc
    p = 1.0 if nd == 0 else min(1.0, 2.0 * binom_cdf_half(min(bb, cc), nd))
    return McNemar(bb, cc, p)


# --------------------------------------------------------------------------- Wilcoxon


@dataclass(frozen=True)
class Wilcoxon:
    n: int
    """Số cặp (gồm hiệu 0)."""
    n_zero: int
    r_plus: float
    r_minus: float
    statistic: float
    z: float | None
    p: float


def rankdata(xs: Sequence[float]) -> list[float]:
    """Hạng trung bình cho giá trị hoà (1-based)."""
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    ranks = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        r = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[order[k]] = r
        i = j + 1
    return ranks


def norm_sf2(z: float) -> float:
    """P[|Z| ≥ |z|] của phân phối chuẩn tắc."""
    return math.erfc(abs(z) / math.sqrt(2))


def wilcoxon_signed_rank(a: Sequence[float], b: Sequence[float]) -> Wilcoxon:
    if len(a) != len(b):
        raise ValueError("a, b phải cùng độ dài (ghép cặp theo câu)")
    d = [x - y for x, y in zip(a, b, strict=True)]
    n = len(d)
    n_zero = sum(1 for x in d if x == 0)
    if n == 0 or n_zero == n:
        return Wilcoxon(n, n_zero, 0.0, 0.0, 0.0, None, 1.0)
    r = rankdata([abs(x) for x in d])
    r_plus = sum(ri for ri, x in zip(r, d, strict=True) if x > 0)
    r_minus = sum(ri for ri, x in zip(r, d, strict=True) if x < 0)
    t = min(r_plus, r_minus)
    mn = n * (n + 1) / 4 - n_zero * (n_zero + 1) / 4
    se = n * (n + 1) * (2 * n + 1) - n_zero * (n_zero + 1) * (2 * n_zero + 1)
    nonzero = [ri for ri, x in zip(r, d, strict=True) if x != 0]
    for cnt in Counter(nonzero).values():
        if cnt > 1:
            se -= 0.5 * cnt * (cnt * cnt - 1)
    se = math.sqrt(se / 24)
    if se == 0:
        return Wilcoxon(n, n_zero, r_plus, r_minus, t, None, 1.0)
    z = (t - mn) / se
    return Wilcoxon(n, n_zero, r_plus, r_minus, t, z, min(1.0, norm_sf2(z)))


# --------------------------------------------------------------------------- Holm, κ


def holm(pvals: Sequence[float]) -> list[float]:
    m = len(pvals)
    order = sorted(range(m), key=lambda i: pvals[i])
    out = [0.0] * m
    running = 0.0
    for rank, i in enumerate(order):
        adj = min(1.0, (m - rank) * pvals[i])
        running = max(running, adj)
        out[i] = running
    return out


def cohen_kappa(a: Sequence[Hashable], b: Sequence[Hashable]) -> float | None:
    """κ = (p_o − p_e) / (1 − p_e); ``None`` khi rỗng; p_e = 1 ⇒ 1 nếu khớp hết, ngược lại 0."""
    if len(a) != len(b):
        raise ValueError("a, b phải cùng độ dài")
    n = len(a)
    if n == 0:
        return None
    po = sum(1 for x, y in zip(a, b, strict=True) if x == y) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    if pe >= 1.0:
        return 1.0 if po == 1.0 else 0.0
    return (po - pe) / (1 - pe)


__all__ = [
    "McNemar",
    "Wilcoxon",
    "binom_cdf_half",
    "bootstrap_diff_ci",
    "bootstrap_mean_ci",
    "cohen_kappa",
    "holm",
    "mcnemar_exact",
    "mean",
    "norm_sf2",
    "rankdata",
    "wilcoxon_signed_rank",
]
