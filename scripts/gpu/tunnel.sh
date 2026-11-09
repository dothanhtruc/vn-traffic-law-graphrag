#!/usr/bin/env bash
# Mở SSH tunnel từ máy local tới máy GPU thuê và tự nối lại khi rớt (Windows không có autossh).
#
#   scripts/gpu/tunnel.sh            # vLLM: localhost:8000 → máy thuê 127.0.0.1:8000
#   scripts/gpu/tunnel.sh --demo     # thêm Gradio: localhost:7860 → máy thuê 127.0.0.1:7860
#
# Để chạy trong một cửa sổ Git Bash riêng; Ctrl+C để dừng. Trong lúc tunnel rớt, các job gọi LLM
# tự retry (lỗi kết nối là lỗi tạm thời), lô hết retry ghi `error` và được chạy lại ở lần sau.
set -uo pipefail
cd "$(dirname "$0")/../.."

HOST="$(uv run python -m scripts.serve_cmd remote ssh_host)"
PORT="$(uv run python -m scripts.serve_cmd remote local_port)"
FWD=(-L "${PORT}:127.0.0.1:${PORT}")
if [[ "${1:-}" == "--demo" ]]; then
    FWD+=(-L "7860:127.0.0.1:7860")
fi

trap 'echo; echo "tunnel: dừng"; exit 0' INT TERM
while true; do
    echo "tunnel: $(date '+%H:%M:%S') nối ${HOST} (${FWD[*]})"
    ssh -N -o ExitOnForwardFailure=yes -o ServerAliveInterval=30 -o ServerAliveCountMax=3 \
        "${FWD[@]}" "$HOST"
    echo "tunnel: $(date '+%H:%M:%S') rớt (mã $?) — nối lại sau 5 giây"
    sleep 5
done
