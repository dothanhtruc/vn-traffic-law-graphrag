import os
import random

from trafficlaw.utils.seed import set_seed


def test_same_seed_same_sequence() -> None:
    assert set_seed(123) == 123
    a = [random.random() for _ in range(5)]
    set_seed(123)
    b = [random.random() for _ in range(5)]
    set_seed(7)
    c = [random.random() for _ in range(5)]
    assert a == b
    assert a != c
    assert os.environ["PYTHONHASHSEED"] == "7"
