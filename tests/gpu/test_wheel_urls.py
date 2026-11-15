"""M11: chọn wheel Linux cp311 x86_64 từ uv.lock cho ``gpu.sh setup --curl-wheels``."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("wheel_urls", ROOT / "scripts/gpu/wheel_urls.py")
assert spec and spec.loader
wu = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wu)

BASE = "https://files.pythonhosted.org/packages/x"
LOCK = {
    "package": [
        {
            "name": "torch",
            "version": "2.15.0",
            "wheels": [
                {
                    "url": f"{BASE}/torch-2.15.0-cp311-cp311-macosx_14_0_arm64.whl",
                    "hash": "sha256:a",
                },
                {
                    "url": f"{BASE}/torch-2.15.0-cp311-cp311-manylinux_2_28_aarch64.whl",
                    "hash": "sha256:b",
                },
                {
                    "url": f"{BASE}/torch-2.15.0-cp311-cp311-manylinux_2_28_x86_64.whl",
                    "hash": "sha256:c",
                },
                {"url": f"{BASE}/torch-2.15.0-cp311-cp311-win_amd64.whl", "hash": "sha256:d"},
            ],
        },
        {
            "name": "Tqdm",
            "version": "4.67.1",
            "wheels": [{"url": f"{BASE}/tqdm-4.67.1-py3-none-any.whl", "hash": "sha256:e"}],
        },
        {"name": "onlysdist", "version": "1.0", "sdist": {"url": "x.tar.gz"}},
        {
            "name": "newglibc",
            "version": "1.0",
            "wheels": [
                {
                    "url": f"{BASE}/newglibc-1.0-cp311-cp311-manylinux_2_41_x86_64.whl",
                    "hash": "sha256:f",
                }
            ],
        },
    ]
}
REQ = """# comment
-e .
torch==2.15.0
tqdm==4.67.1
colorama==0.4.6 ; sys_platform == 'win32'
    # via tqdm
"""


def test_parse_requirements_markers() -> None:
    got = wu.parse_requirements(REQ, wu.LINUX_ENV)
    assert got == [("torch", "2.15.0"), ("tqdm", "4.67.1")]  # colorama chỉ cho Windows


def test_pick_linux_x86_64() -> None:
    got, missing = wu.pick_wheels(LOCK, [("torch", "2.15.0"), ("tqdm", "4.67.1")], wu.target_tags())
    assert [f for _, _, f in got] == [
        "torch-2.15.0-cp311-cp311-manylinux_2_28_x86_64.whl",
        "tqdm-4.67.1-py3-none-any.whl",
    ]
    assert [h for _, h, _ in got] == ["c", "e"] and not missing


def test_missing_reported() -> None:
    _, missing = wu.pick_wheels(
        LOCK, [("onlysdist", "1.0"), ("newglibc", "1.0"), ("khong-co", "9")], wu.target_tags()
    )
    assert len(missing) == 3  # sdist; glibc 2.41 > 2.39 của Ubuntu 24.04; không có trong lock
