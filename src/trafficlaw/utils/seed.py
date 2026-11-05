"""Cố định seed cho mọi script (tái lập kết quả)."""

from __future__ import annotations

import logging
import os
import random

logger = logging.getLogger(__name__)

DEFAULT_SEED = 42


def set_seed(seed: int = DEFAULT_SEED, *, deterministic_torch: bool = True) -> int:
    """Đặt seed cho ``random``, numpy và torch (nếu đã cài). Trả về seed đã dùng."""
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)
    try:
        import numpy as np
    except ImportError:
        pass
    else:
        np.random.seed(seed)
    try:
        import torch
    except ImportError:
        pass
    else:
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
        if deterministic_torch:
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
    logger.info("Seed = %d", seed)
    return seed
