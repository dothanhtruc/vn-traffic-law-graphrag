"""Thông tin git để ghi vào output (tái lập kết quả)."""

from __future__ import annotations

import subprocess
from functools import cache
from pathlib import Path


@cache
def git_commit(repo_root: str | Path = ".") -> str | None:
    """SHA commit hiện tại, thêm ``-dirty`` nếu cây làm việc có thay đổi chưa commit.

    Trả về ``None`` khi không phải repo git hoặc không có lệnh ``git``.
    """
    try:
        sha = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        dirty = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=no"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None
    return f"{sha}-dirty" if dirty else sha
