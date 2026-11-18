"""M14: fine-tune reranker — xem `scripts/_train_cli.py` (--estimate | --dry-run --grid-id G |
--grid-id G | --report). Cấu hình `configs/train_reranker.yaml`; CLAUDE.md mục 9."""

from __future__ import annotations

import sys

from scripts._train_cli import main

if __name__ == "__main__":
    sys.exit(main("reranker", "configs/train_reranker.yaml"))
