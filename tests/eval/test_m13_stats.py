"""M13 thống kê: so với giá trị tính tay."""

from __future__ import annotations

import math

import pytest

from trafficlaw.eval.stats import (
    binom_cdf_half,
    bootstrap_diff_ci,
    bootstrap_mean_ci,
    cohen_kappa,
    holm,
    mcnemar_exact,
    rankdata,
    wilcoxon_signed_rank,
)


def test_binom_cdf_half() -> None:
    assert binom_cdf_half(1, 4) == pytest.approx(5 / 16)
    assert binom_cdf_half(0, 5) == pytest.approx(1 / 32)
    assert binom_cdf_half(-1, 3) == 0.0 and binom_cdf_half(3, 3) == 1.0


def test_mcnemar_exact_hand_values() -> None:
    # b = 3 (A đúng, B sai), c = 1 ⇒ p = 2·P[X ≤ 1], X ~ Bin(4, ½) = 2·5/16 = 0,625
    a = [True, True, True, False, False, True]
    b = [False, False, False, True, False, True]
    t = mcnemar_exact(a, b)
    assert (t.b, t.c) == (3, 1) and t.p == pytest.approx(0.625)
    # b = 0, c = 5 ⇒ p = 2/32
    t2 = mcnemar_exact([False] * 5, [True] * 5)
    assert (t2.b, t2.c) == (0, 5) and t2.p == pytest.approx(0.0625)
    # không lệch ⇒ p = 1; b = c ⇒ p = min(1, …) = 1
    assert mcnemar_exact([True, False], [True, False]).p == 1.0
    assert mcnemar_exact([True, False], [False, True]).p == 1.0


def test_rankdata_ties() -> None:
    assert rankdata([0, 1, 2, 3, 3]) == [1, 2, 3, 4.5, 4.5]
    assert rankdata([5, 5, 5]) == [2, 2, 2]


def test_wilcoxon_pratt_hand_values() -> None:
    # d = a − b = [0, 1, −2, 3, 3]; |d| xếp hạng gồm cả số 0: 1, 2, 3, 4,5, 4,5
    # R+ = 2 + 4,5 + 4,5 = 11; R− = 3; T = 3
    # Pratt: mn = 5·6/4 − 1·2/4 = 7; var·24 = 5·6·11 − 1·2·3 − ½·2·(4 − 1) = 321
    a = [1.0, 2.0, 0.0, 5.0, 4.0]
    b = [1.0, 1.0, 2.0, 2.0, 1.0]
    w = wilcoxon_signed_rank(a, b)
    assert (w.n, w.n_zero, w.r_plus, w.r_minus, w.statistic) == (5, 1, 11, 3, 3)
    z = (3 - 7) / math.sqrt(321 / 24)
    assert w.z == pytest.approx(z)
    assert w.p == pytest.approx(math.erfc(abs(z) / math.sqrt(2)))
    assert w.p == pytest.approx(0.2741, abs=1e-3)


def test_wilcoxon_degenerate() -> None:
    assert wilcoxon_signed_rank([1, 2], [1, 2]).p == 1.0
    assert wilcoxon_signed_rank([], []).p == 1.0
    with pytest.raises(ValueError):
        wilcoxon_signed_rank([1], [1, 2])


def test_holm_hand_values() -> None:
    # sắp: 0,01·3 = 0,03; 0,03·2 = 0,06; 0,04·1 = 0,04 → đơn điệu 0,06
    assert holm([0.01, 0.04, 0.03]) == pytest.approx([0.03, 0.06, 0.06])
    assert holm([0.5, 0.9]) == pytest.approx([1.0, 1.0])
    assert holm([]) == []


def test_cohen_kappa_hand_values() -> None:
    # p_o = 3/4; p_e = (2·1 + 2·3)/16 = 1/2 ⇒ κ = 0,5
    assert cohen_kappa([1, 1, 0, 0], [1, 0, 0, 0]) == pytest.approx(0.5)
    assert cohen_kappa([0, 1, 2], [0, 1, 2]) == pytest.approx(1.0)
    assert cohen_kappa([2, 2], [2, 2]) == 1.0
    assert cohen_kappa([], []) is None


def test_bootstrap() -> None:
    assert bootstrap_mean_ci([0.5] * 10) == (0.5, 0.5)
    lo, hi = bootstrap_mean_ci([0.0, 1.0] * 50) or (0, 0)
    assert lo < 0.5 < hi
    assert bootstrap_mean_ci([0.0, 1.0] * 50) == bootstrap_mean_ci([0.0, 1.0] * 50)  # tất định
    assert bootstrap_diff_ci([1.0] * 5, [0.0] * 5) == (1.0, 1.0)
    assert bootstrap_mean_ci([]) is None
