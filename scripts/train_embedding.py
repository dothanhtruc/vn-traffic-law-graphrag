"""M14: fine-tune embedding — xem `scripts/_train_cli.py` (--estimate | --dry-run --grid-id G |
--grid-id G | --report). Cấu hình `configs/train_embedding.yaml`; CLAUDE.md mục 9."""

from __future__ import annotations

import sys

from scripts._train_cli import main

if __name__ == "__main__":
    sys.exit(main("embedding", "configs/train_embedding.yaml"))
