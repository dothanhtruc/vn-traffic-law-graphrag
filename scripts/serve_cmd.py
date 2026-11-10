"""Helper cho ``scripts/gpu/*.sh``: đọc ``configs/serve.yaml`` (bash không tự đọc YAML).

uv run python -m scripts.serve_cmd remote ssh_host   # in một trường của mục remote
uv run python -m scripts.serve_cmd script <model>    # script bash chạy vLLM trên máy thuê
uv run python -m scripts.serve_cmd list              # liệt kê model (khoá, tên, họ, vai trò)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from trafficlaw.llm.serve import load_serve_config, remote_serve_script

REPO_ROOT = Path(__file__).resolve().parents[1]


def emit(text: str) -> None:
    """Ghi byte thô: trên Windows stdout văn bản đổi LF thành CRLF, làm hỏng bash ở máy thuê."""
    sys.stdout.buffer.write(text.encode("utf-8"))
    sys.stdout.buffer.flush()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("command", choices=["remote", "script", "list"])
    ap.add_argument("arg", nargs="?")
    ap.add_argument("--config", type=Path, default=REPO_ROOT / "configs" / "serve.yaml")
    args = ap.parse_args(argv)
    cfg = load_serve_config(args.config)
    if args.command == "remote":
        if not args.arg or args.arg not in type(cfg.remote).model_fields:
            print(f"trường remote không hợp lệ: {args.arg}", file=sys.stderr)
            return 2
        emit(f"{getattr(cfg.remote, args.arg)}\n")
    elif args.command == "script":
        if not args.arg:
            print("cần tên model (khoá hoặc served_model_name)", file=sys.stderr)
            return 2
        try:
            emit(remote_serve_script(cfg, args.arg))
        except KeyError as e:
            print(e, file=sys.stderr)
            return 2
    else:
        for k, m in cfg.models.items():
            rev = m.revision or "CHƯA GHIM"
            emit(f"{k}\t{m.served_model_name}\t{m.family}\t{m.role}\t{m.hf_repo}@{rev}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
