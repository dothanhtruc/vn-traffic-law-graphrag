#!/usr/bin/env bash
# Điều khiển máy GPU thuê (aidev.edu.vn, 1× RTX 3090) từ máy local qua SSH (chạy trong Git Bash).
# Cấu hình: configs/serve.yaml (mục remote + models); alias SSH trong ~/.ssh/config
# (mẫu: scripts/gpu/ssh_config.example). Máy local giữ repo/dữ liệu/kết quả; máy thuê chỉ chạy GPU.
#
#   scripts/gpu/gpu.sh key init              # tạo SSH key ed25519 (không passphrase), in public key
#   scripts/gpu/gpu.sh key config <host> [port] [user]   # ghi alias SSH vào ~/.ssh/config
#   scripts/gpu/gpu.sh key install           # cài key lên máy thuê (gõ mật khẩu MỘT lần)
#   scripts/gpu/gpu.sh key check             # xác nhận đăng nhập CHỈ bằng key
#   scripts/gpu/gpu.sh key harden            # tắt đăng nhập bằng mật khẩu trên máy thuê
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
# lệnh, không in ra màn hình. Xác thực SSH chỉ bằng key (không passphrase, người dùng chọn
# 09/11/2026); mọi lệnh ssh dưới đây chạy BatchMode nên không bao giờ treo chờ mật khẩu.
# Private key không bao giờ được đọc/in/chép; chỉ in public key.
set -euo pipefail
cd "$(dirname "$0")/../.."

cfg() { uv run python -m scripts.serve_cmd remote "$1"; }
HOST="${GPU_SSH_HOST:-$(cfg ssh_host)}"  # alias SSH (mặc định remote.ssh_host trong serve.yaml)

# Key và file cấu hình SSH (ghi đè được bằng biến môi trường — dùng trong test).
KEY="${GPU_SSH_KEY:-$HOME/.ssh/aidev_ed25519}"
SSH_CONFIG="${GPU_SSH_CONFIG:-$HOME/.ssh/config}"
KNOWN_HOSTS="${GPU_SSH_KNOWN_HOSTS:-$HOME/.ssh/known_hosts}"
SSH=(ssh -o BatchMode=yes -o ConnectTimeout=20)

# ~ ở đầu đường dẫn → $HOME khi chạy trên máy thuê.
rpath() { case "$1" in "~/"*) printf '"$HOME"/%q' "${1#\~/}" ;; *) printf '%q' "$1" ;; esac; }

load_remote_cfg() {  # chỉ các lệnh làm việc với máy thuê mới cần (gọi uv mất vài giây)
    RDIR="$(cfg remote_dir)"
    VENV="$(cfg vllm_venv)"
    ENVF="$(cfg env_file)"
    PORT="$(cfg local_port)"
    R_DIR="$(rpath "$RDIR")"
    R_VENV="$(rpath "$VENV")"
    R_ENVF="$(rpath "$ENVF")"
}

remote() { "${SSH[@]}" "$HOST" "bash -lc $(printf '%q' "$1")"; }

preflight() {  # đăng nhập được bằng key chưa (không hỏi mật khẩu)
    if ! "${SSH[@]}" "$HOST" true 2>/dev/null; then
        echo "không đăng nhập được ${HOST} bằng SSH key — chạy: scripts/gpu/gpu.sh key check" >&2
        exit 1
    fi
}

# --------------------------------------------------------------------------- SSH key

BEGIN_MARK="# >>> graphrag gpu-aidev (scripts/gpu/gpu.sh key config) >>>"
END_MARK="# <<< graphrag gpu-aidev <<<"

key_init() {
    local dir
    dir="$(dirname "$KEY")"
    mkdir -p "$dir"
    chmod 700 "$dir" 2>/dev/null || true
    if [[ -f "$KEY" ]]; then
        echo "key: đã có ${KEY} — giữ nguyên (không ghi đè)"
    else
        ssh-keygen -q -t ed25519 -N "" -C "graphrag-gpu" -f "$KEY"
        echo "key: đã tạo ${KEY} (ed25519, không passphrase)"
    fi
    chmod 600 "$KEY" 2>/dev/null || true
    chmod 644 "$KEY.pub" 2>/dev/null || true
    echo "Public key — dán vào trang quản lý SSH key của aidev TRƯỚC khi tạo máy:"
    cat "$KEY.pub"
}

key_config() {
    local host="${1:?cần host/IP của máy thuê: gpu.sh key config <host> [port] [user]}"
    local port="${2:-22}" user="${3:-root}" idf tmp target
    [[ -f "$KEY" ]] || { echo "chưa có key — chạy: scripts/gpu/gpu.sh key init" >&2; exit 1; }
    case "$KEY" in "$HOME"/*) idf="~${KEY#"$HOME"}" ;; *) idf="$KEY" ;; esac
    mkdir -p "$(dirname "$SSH_CONFIG")"
    touch "$SSH_CONFIG"
    tmp="$(mktemp)"
    # Bỏ khối cũ (giữa hai dòng đánh dấu), giữ nguyên mọi nội dung khác.
    awk -v b="$BEGIN_MARK" -v e="$END_MARK" '$0==b{skip=1;next} $0==e{skip=0;next} !skip' \
        "$SSH_CONFIG" > "$tmp"
    # Khối riêng đặt ĐẦU file: ssh lấy giá trị đầu tiên khớp, tránh bị "Host *" phía sau che.
    {
        printf '%s\n' "$BEGIN_MARK"
        printf 'Host %s\n' "$HOST"
        printf '    HostName %s\n    Port %s\n    User %s\n' "$host" "$port" "$user"
        printf '    IdentityFile %s\n    IdentitiesOnly yes\n' "$idf"
        printf '    PreferredAuthentications publickey\n'
        printf '    ServerAliveInterval 30\n    ServerAliveCountMax 3\n'
        printf '    ExitOnForwardFailure yes\n    StrictHostKeyChecking accept-new\n'
        printf '%s\n' "$END_MARK"
        cat "$tmp"
    } > "$SSH_CONFIG"
    rm -f "$tmp"
    chmod 600 "$SSH_CONFIG" 2>/dev/null || true
    # Máy thuê mới có thể đổi host key cho cùng IP/cổng ⇒ xoá dòng cũ.
    target="$host"
    [[ "$port" == 22 ]] || target="[$host]:$port"
    [[ -f "$KNOWN_HOSTS" ]] && ssh-keygen -R "$target" -f "$KNOWN_HOSTS" >/dev/null 2>&1 || true
    echo "key: ${SSH_CONFIG} — Host ${HOST} → ${user}@${host}:${port} (key ${idf})"
    echo "→ kiểm tra: scripts/gpu/gpu.sh key check"
}

key_install() {
    [[ -f "$KEY.pub" ]] || { echo "chưa có key — chạy: scripts/gpu/gpu.sh key init" >&2; exit 1; }
    echo "key: cài ${KEY}.pub lên ${HOST} — nhập mật khẩu máy thuê MỘT lần nếu được hỏi"
    ssh-copy-id -i "$KEY.pub" -o PreferredAuthentications=password,keyboard-interactive "$HOST"
    key_check
}

key_check() {
    if "${SSH[@]}" -o PasswordAuthentication=no -o KbdInteractiveAuthentication=no "$HOST" \
        'echo "OK: user=$(whoami) host=$(hostname)"; nvidia-smi --query-gpu=name,memory.total \
            --format=csv,noheader 2>/dev/null || echo "(không thấy nvidia-smi)"'; then
        return 0
    fi
    cat >&2 <<HINT
key check: KHÔNG đăng nhập được ${HOST} chỉ bằng SSH key. Kiểm tra:
  1. ~/.ssh/config có khối Host ${HOST} đúng IP/cổng/user (scripts/gpu/gpu.sh key config ...)
  2. public key (${KEY}.pub) đã đăng ký trên trang aidev trước khi tạo máy,
     hoặc cài bằng mật khẩu: scripts/gpu/gpu.sh key install
  3. chi tiết: ssh -v ${HOST} true
HINT
    return 1
}

key_harden() {
    key_check >/dev/null || { echo "key harden: cần key check thành công trước" >&2; exit 1; }
    # Công tắc an toàn: drop-in tự bị gỡ sau 120 giây trừ khi máy local xác nhận đăng nhập
    # bằng key vẫn được (tạo file xác nhận) ⇒ không thể tự khoá mình ngoài.
    remote '
        set -e
        S=""; [ "$(id -u)" = 0 ] || S="sudo -n"
        F=/etc/ssh/sshd_config.d/90-graphrag.conf
        grep -qE "^Include /etc/ssh/sshd_config.d/\*\.conf" /etc/ssh/sshd_config \
            || { echo "sshd_config không Include sshd_config.d — dừng" >&2; exit 1; }
        printf "PasswordAuthentication no\nKbdInteractiveAuthentication no\n" | $S tee $F >/dev/null
        $S sshd -t || { $S rm -f $F; echo "sshd -t lỗi — đã gỡ" >&2; exit 1; }
        reload() { $S systemctl reload ssh 2>/dev/null || $S systemctl reload sshd 2>/dev/null \
            || $S service ssh reload; }
        reload
        rm -f /tmp/graphrag-harden-ok
        nohup sh -c "sleep 120; [ -f /tmp/graphrag-harden-ok ] || { $S rm -f $F; \
            $S systemctl reload ssh 2>/dev/null || $S systemctl reload sshd 2>/dev/null \
            || $S service ssh reload; }" >/dev/null 2>&1 &
        echo "đã tắt đăng nhập bằng mật khẩu (tự hoàn tác sau 120 giây nếu không được xác nhận)"
    '
    if key_check >/dev/null && "${SSH[@]}" "$HOST" 'touch /tmp/graphrag-harden-ok'; then
        echo "key harden: xác nhận — đăng nhập bằng key vẫn được; mật khẩu đã tắt"
    else
        echo "key harden: KHÔNG xác nhận được — cấu hình sẽ tự gỡ sau 120 giây" >&2
        exit 1
    fi
}

cmd_key() {
    case "${1:-}" in
        init) key_init ;;
        config) shift; key_config "$@" ;;
        install) key_install ;;
        check) key_check ;;
        harden) key_harden ;;
        *) echo "gpu.sh key init | config <host> [port] [user] | install | check | harden" >&2
           exit 2 ;;
    esac
}

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
        "${SSH[@]}" "$HOST" "umask 077; mkdir -p \"\$(dirname $R_ENVF)\"; cat > $R_ENVF"
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
    printf '%s\n' "$script" | "${SSH[@]}" "$HOST" "mkdir -p \$HOME/.config/graphrag && \
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
        "${SSH[@]}" "$HOST" "mkdir -p \$HOME/.config/graphrag && cat > \$HOME/.config/graphrag/job-$name.sh && \
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
    tar czf - "${paths[@]}" | "${SSH[@]}" "$HOST" "mkdir -p $R_DIR && tar xzf - -C $R_DIR"
}

cmd_pull() {
    [[ $# -gt 0 ]] || { echo "cần đường dẫn (tương đối với ${RDIR})" >&2; exit 1; }
    local q
    q="$(printf '%q ' "$@")"
    echo "pull: ${HOST}:${RDIR}/{$*} → ."
    "${SSH[@]}" "$HOST" "cd $R_DIR && tar czf - $q" | tar xzf -
}

cmd_stop() {
    remote "tmux ls 2>/dev/null; tmux kill-server 2>/dev/null || true"
    echo "stop: đã dừng vLLM/job trên ${HOST}."
    echo "      NHỚ TẮT/XOÁ MÁY trên trang aidev.edu.vn để không bị tính giờ."
}

case "${1:-}" in
    key) shift; cmd_key "$@"; exit 0 ;;
    setup | serve | stop-serve | run | status | logs | push | pull | stop)
        load_remote_cfg
        preflight ;;
esac

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
    *) sed -n '2,26p' "$0"; exit 2 ;;
esac
