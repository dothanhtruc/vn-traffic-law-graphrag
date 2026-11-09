#!/usr/bin/env bash
# Điều khiển máy GPU thuê (aidev.edu.vn, 1× RTX 3090) từ máy local qua SSH (chạy trong Git Bash).
# Cấu hình: configs/serve.yaml (mục remote + models); alias SSH trong ~/.ssh/config
# (mẫu: scripts/gpu/ssh_config.example). Máy local giữ repo/dữ liệu/kết quả; máy thuê chỉ chạy GPU.
#
#   scripts/gpu/gpu.sh setup                 # cài trên máy thuê: tmux, uv, repo, vLLM, file env
#   scripts/gpu/gpu.sh serve <model>         # chạy vLLM (khoá/tên trong serve.yaml) trong tmux
#   scripts/gpu/gpu.sh stop-serve            # dừng vLLM
#   scripts/gpu/gpu.sh run <tên> -- <lệnh>   # job dài (M10/M14/M17) trong tmux, log logs/<tên>.log
#   scripts/gpu/gpu.sh status                # tmux + GPU
#   scripts/gpu/gpu.sh logs <tên> [N]        # N dòng cuối log (tên = vllm-<model> hoặc job)
#   scripts/gpu/gpu.sh push [đường dẫn…]     # local → máy thuê (mặc định data/processed data/graph)
#   scripts/gpu/gpu.sh pull <đường dẫn…>     # máy thuê → local (vd results/<run_id> data/index)
#   scripts/gpu/gpu.sh stop                  # dừng mọi tmux, nhắc TẮT MÁY trên aidev (hết tính giờ)
#
# Bí mật: LOCAL_LLM_API_KEY và HF_TOKEN đọc từ .env ở local, gửi sang máy thuê qua stdin vào file
# quyền 600 (configs/serve.yaml remote.env_file, biến VLLM_API_KEY/HF_TOKEN); không nằm trong dòng
# lệnh, không in ra màn hình.
set -euo pipefail
cd "$(dirname "$0")/../.."

cfg() { uv run python -m scripts.serve_cmd remote "$1"; }
HOST="$(cfg ssh_host)"
RDIR="$(cfg remote_dir)"
VENV="$(cfg vllm_venv)"
ENVF="$(cfg env_file)"
PORT="$(cfg local_port)"

# ~ ở đầu đường dẫn → $HOME khi chạy trên máy thuê.
rpath() { case "$1" in "~/"*) printf '"$HOME"/%q' "${1#\~/}" ;; *) printf '%q' "$1" ;; esac; }
R_DIR="$(rpath "$RDIR")"
R_VENV="$(rpath "$VENV")"
R_ENVF="$(rpath "$ENVF")"

remote() { ssh "$HOST" "bash -lc $(printf '%q' "$1")"; }

dotenv_get() {  # đọc biến từ .env local (bỏ ngoặc, CR)
    [[ -f .env ]] || return 0
    grep -E "^$1=" .env | tail -n1 | cut -d= -f2- | tr -d '\r' | sed -e 's/^"//' -e 's/"$//' \
        -e "s/^'//" -e "s/'$//"
}

cmd_setup() {
    local key hf repo branch ver
    key="$(dotenv_get LOCAL_LLM_API_KEY)"
    hf="$(dotenv_get HF_TOKEN)"
    if [[ -z "$key" ]]; then
        echo "thiếu LOCAL_LLM_API_KEY trong .env (tạo: openssl rand -hex 24)" >&2
        exit 1
    fi
    repo="$(git remote get-url origin)"
    branch="$(git rev-parse --abbrev-ref HEAD)"
    ver="$(uv run python -c "from trafficlaw.llm.serve import load_serve_config as l; \
print(l('configs/serve.yaml').vllm_version or '')")"
    echo "setup: ${HOST} · repo ${repo}@${branch} · vLLM ${ver:-mới nhất}"
    # File env (quyền 600) — nội dung qua stdin, không qua dòng lệnh.
    printf 'VLLM_API_KEY=%s\nHF_TOKEN=%s\n' "$key" "$hf" |
        ssh "$HOST" "umask 077; mkdir -p \"\$(dirname $R_ENVF)\"; cat > $R_ENVF"
    remote "
        set -euo pipefail
        command -v tmux >/dev/null || { sudo -n apt-get update -qq && sudo -n apt-get install -y -qq tmux; } \
            || apt-get install -y -qq tmux
        command -v uv >/dev/null || curl -LsSf https://astral.sh/uv/install.sh | sh
        export PATH=\"\$HOME/.local/bin:\$PATH\"
        if [ -d $R_DIR/.git ]; then
            git -C $R_DIR fetch -q origin && git -C $R_DIR checkout -q $(printf '%q' "$branch") \
                && git -C $R_DIR pull -q --ff-only
        else
            git clone -q -b $(printf '%q' "$branch") $(printf '%q' "$repo") $R_DIR
        fi
        cd $R_DIR && uv sync -q
        [ -x $R_VENV/bin/python ] || uv venv -q --python 3.12 $R_VENV
        uv pip install -q --python $R_VENV/bin/python $(printf '%q' "vllm${ver:+==$ver}") bitsandbytes
        echo \"vLLM: \$($R_VENV/bin/python -c 'import vllm; print(vllm.__version__)')\"
        nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader
        nvcc --version 2>/dev/null | tail -n1 || true
    "
    echo "setup: xong. Nếu vllm_version trong configs/serve.yaml đang null, ghim phiên bản vừa in."
}

cmd_serve() {
    local model="${1:?cần tên model trong configs/serve.yaml}" script
    script="$(uv run python -m scripts.serve_cmd script "$model")"
    printf '%s\n' "$script" | ssh "$HOST" "mkdir -p \$HOME/.config/graphrag && \
        cat > \$HOME/.config/graphrag/serve.sh && chmod 700 \$HOME/.config/graphrag/serve.sh"
    remote "tmux kill-session -t vllm 2>/dev/null || true; \
        tmux new-session -d -s vllm \$HOME/.config/graphrag/serve.sh"
    echo "serve: đang khởi động ${model} (tải model lần đầu có thể mất vài phút)…"
    remote "for i in \$(seq 1 180); do
            curl -sf http://127.0.0.1:${PORT}/health >/dev/null && { echo 'serve: sẵn sàng'; exit 0; }
            tmux has-session -t vllm 2>/dev/null || { echo 'serve: vLLM đã thoát — xem log' >&2; exit 1; }
            sleep 5
        done; echo 'serve: quá 15 phút chưa sẵn sàng' >&2; exit 1"
    echo "→ mở tunnel (scripts/gpu/tunnel.sh) rồi: uv run python -m scripts.llm_check --provider local"
}

cmd_stop_serve() { remote "tmux kill-session -t vllm 2>/dev/null && echo 'đã dừng vLLM' || echo 'vLLM không chạy'"; }

cmd_run() {
    local name="${1:?cần tên job}"
    shift
    [[ "${1:-}" == "--" ]] && shift
    [[ $# -gt 0 ]] || { echo "cần lệnh sau --" >&2; exit 1; }
    local body
    body="$(printf '%q ' "$@")"
    printf '#!/usr/bin/env bash\nset -o pipefail\nset -a; . %s; set +a\nexport PATH="$HOME/.local/bin:$PATH"\ncd %s\nmkdir -p logs\n%s 2>&1 | tee -a logs/%s.log\necho "[job %s kết thúc: mã ${PIPESTATUS[0]}]" | tee -a logs/%s.log\n' \
        "$R_ENVF" "$R_DIR" "$body" "$name" "$name" "$name" |
        ssh "$HOST" "mkdir -p \$HOME/.config/graphrag && cat > \$HOME/.config/graphrag/job-$name.sh && \
            chmod 700 \$HOME/.config/graphrag/job-$name.sh"
    remote "tmux new-session -d -s job-$name \$HOME/.config/graphrag/job-$name.sh"
    echo "run: job-$name đã chạy trên ${HOST} — xem: scripts/gpu/gpu.sh logs $name"
}

cmd_status() {
    remote "tmux ls 2>/dev/null || echo '(không có tmux session)'; \
        nvidia-smi --query-gpu=name,utilization.gpu,memory.used,memory.total --format=csv,noheader"
}

cmd_logs() {
    local name="${1:?cần tên log}" n="${2:-50}"
    remote "tail -n $n $R_DIR/logs/$name.log"
}

cmd_push() {
    local paths=("$@")
    [[ ${#paths[@]} -gt 0 ]] || paths=(data/processed data/graph)
    echo "push: ${paths[*]} → ${HOST}:${RDIR}"
    tar czf - "${paths[@]}" | ssh "$HOST" "mkdir -p $R_DIR && tar xzf - -C $R_DIR"
}

cmd_pull() {
    [[ $# -gt 0 ]] || { echo "cần đường dẫn (tương đối với ${RDIR})" >&2; exit 1; }
    local q
    q="$(printf '%q ' "$@")"
    echo "pull: ${HOST}:${RDIR}/{$*} → ."
    ssh "$HOST" "cd $R_DIR && tar czf - $q" | tar xzf -
}

cmd_stop() {
    remote "tmux ls 2>/dev/null; tmux kill-server 2>/dev/null || true"
    echo "stop: đã dừng vLLM/job trên ${HOST}."
    echo "      NHỚ TẮT/XOÁ MÁY trên trang aidev.edu.vn để không bị tính giờ."
}

case "${1:-}" in
    setup) cmd_setup ;;
    serve) shift; cmd_serve "$@" ;;
    stop-serve) cmd_stop_serve ;;
    run) shift; cmd_run "$@" ;;
    status) cmd_status ;;
    logs) shift; cmd_logs "$@" ;;
    push) shift; cmd_push "$@" ;;
    pull) shift; cmd_pull "$@" ;;
    stop) cmd_stop ;;
    *) sed -n '2,20p' "$0"; exit 2 ;;
esac
