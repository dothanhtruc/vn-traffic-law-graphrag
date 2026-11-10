"""``scripts/gpu/gpu.sh key …``: tạo SSH key, ghi alias vào ``~/.ssh/config``, kiểm tra đăng nhập
bằng key — chạy trên thư mục tạm, không đụng ``~/.ssh`` thật, không kết nối mạng (ssh giả)."""

from __future__ import annotations

import os
import shutil
import stat
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
GPU_SH = REPO / "scripts" / "gpu" / "gpu.sh"


def _bash() -> str | None:
    b = shutil.which("bash")
    # Trên Windows, bash.exe trong System32 là WSL — không dùng được với đường dẫn Windows.
    if b is None or "system32" in b.lower():
        return None
    return b


BASH = _bash()
pytestmark = pytest.mark.skipif(
    BASH is None or shutil.which("ssh-keygen") is None, reason="cần bash + ssh-keygen"
)


def _posix(p: Path) -> str:
    """Đường dẫn dạng bash hiểu được (Git Bash: C:\\x → /c/x)."""
    s = str(p)
    if os.name == "nt" and len(s) > 1 and s[1] == ":":
        return "/" + s[0].lower() + s[2:].replace("\\", "/")
    return s


def run(tmp: Path, *args: str, path_prefix: Path | None = None) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env.update(
        GPU_SSH_HOST="gpu-test",
        GPU_SSH_KEY=_posix(tmp / "ssh" / "aidev_ed25519"),
        GPU_SSH_CONFIG=_posix(tmp / "ssh" / "config"),
        GPU_SSH_KNOWN_HOSTS=_posix(tmp / "ssh" / "known_hosts"),
    )
    if path_prefix is not None:
        env["PATH"] = _posix(path_prefix) + os.pathsep + env["PATH"]
    assert BASH is not None
    return subprocess.run(
        [BASH, _posix(GPU_SH), *args],
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=120,
    )


def test_key_init_creates_key_once(tmp_path: Path) -> None:
    r = run(tmp_path, "key", "init")
    assert r.returncode == 0, r.stderr
    key, pub = tmp_path / "ssh" / "aidev_ed25519", tmp_path / "ssh" / "aidev_ed25519.pub"
    assert key.is_file() and pub.is_file()
    assert pub.read_text().startswith("ssh-ed25519 ") and "graphrag-gpu" in pub.read_text()
    assert pub.read_text().strip() in r.stdout  # in public key để dán lên aidev
    assert "PRIVATE KEY" not in r.stdout + r.stderr  # không bao giờ in private key
    if os.name != "nt":
        assert stat.S_IMODE(key.stat().st_mode) == 0o600
    before = key.read_bytes()
    r2 = run(tmp_path, "key", "init")
    assert r2.returncode == 0 and "giữ nguyên" in r2.stdout
    assert key.read_bytes() == before  # không ghi đè key đã có


def test_key_config_idempotent_and_keeps_other_entries(tmp_path: Path) -> None:
    assert run(tmp_path, "key", "init").returncode == 0
    cfg = tmp_path / "ssh" / "config"
    cfg.write_text("Host github.com\n    User git\n", encoding="utf-8")
    r = run(tmp_path, "key", "config", "203.0.113.10", "2222", "ubuntu")
    assert r.returncode == 0, r.stderr
    r = run(tmp_path, "key", "config", "203.0.113.20")  # máy thuê mới: thay khối cũ
    assert r.returncode == 0, r.stderr
    text = cfg.read_text(encoding="utf-8")
    assert text.count("Host gpu-test") == 1
    assert text.count(">>> graphrag gpu-aidev") == 1
    assert "HostName 203.0.113.20" in text and "203.0.113.10" not in text
    assert "Port 22\n" in text and "User root" in text  # mặc định khi không truyền
    assert "IdentitiesOnly yes" in text and "PreferredAuthentications publickey" in text
    assert "Host github.com\n    User git" in text  # nội dung khác giữ nguyên
    assert text.index("Host gpu-test") < text.index("Host github.com")  # khối riêng ở đầu


def test_key_config_requires_key(tmp_path: Path) -> None:
    r = run(tmp_path, "key", "config", "203.0.113.10")
    assert r.returncode != 0 and "key init" in r.stderr


def test_key_check_failure_prints_guidance(tmp_path: Path) -> None:
    fake = tmp_path / "bin"
    fake.mkdir()
    ssh = fake / "ssh"
    ssh.write_bytes(b"#!/usr/bin/env bash\necho 'Permission denied (publickey).' >&2\nexit 255\n")
    ssh.chmod(0o755)
    r = run(tmp_path, "key", "check", path_prefix=fake)
    assert r.returncode != 0
    assert "KHÔNG đăng nhập được gpu-test" in r.stderr and "key install" in r.stderr


def test_remote_commands_refuse_without_key_login(tmp_path: Path) -> None:
    """Lệnh làm việc với máy thuê dừng ngay (preflight BatchMode) thay vì treo chờ mật khẩu."""
    fake = tmp_path / "bin"
    fake.mkdir()
    (fake / "ssh").write_bytes(b"#!/usr/bin/env bash\nexit 255\n")
    (fake / "ssh").chmod(0o755)
    r = run(tmp_path, "status", path_prefix=fake)
    assert r.returncode == 1 and "key check" in r.stderr
