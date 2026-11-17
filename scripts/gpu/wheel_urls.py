"""Danh sách wheel Linux (URL + sha256) cho ``gpu.sh setup --curl-wheels`` (M11).

Sự cố 14/11/2026 (M10): ``uv sync`` trên máy aidev tải wheel PyPI chỉ ~1 MB/s trong khi ``curl``
cùng CDN đạt 67 MB/s. Cách xử lý cố định: lấy đúng các gói ``uv export`` chọn (đã ghim trong
``uv.lock``), chọn wheel hợp với máy thuê (CPython 3.11, manylinux x86_64, glibc ≤ 2.39 của Ubuntu
24.04), in ``url<TAB>sha256<TAB>tên file`` để máy thuê tải song song bằng ``curl``, kiểm sha256 rồi
``uv pip install --no-index --no-deps``.

    uv run python scripts/gpu/wheel_urls.py --group embed > wheels.tsv

Thoát mã 1 nếu có gói không có wheel phù hợp (chỉ có sdist) — khi đó dùng ``uv sync`` thường.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import tomllib
from collections.abc import Iterable, Sequence
from pathlib import Path

from packaging.markers import Marker
from packaging.requirements import Requirement
from packaging.tags import Tag, compatible_tags, cpython_tags
from packaging.utils import canonicalize_name, parse_wheel_filename

ROOT = Path(__file__).resolve().parents[2]
LINUX_ENV = {
    "implementation_name": "cpython",
    "platform_python_implementation": "CPython",
    "platform_machine": "x86_64",
    "platform_system": "Linux",
    "sys_platform": "linux",
    "os_name": "posix",
    "python_version": "3.11",
    "python_full_version": "3.11.13",
    "platform_release": "",
    "platform_version": "",
    "implementation_version": "3.11.13",
    "extra": "",
}


def target_tags(py: tuple[int, int] = (3, 11), glibc_max: int = 39) -> list[Tag]:
    plats = [f"manylinux_2_{m}_x86_64" for m in range(glibc_max, 4, -1)]
    plats += ["manylinux2014_x86_64", "manylinux2010_x86_64", "manylinux1_x86_64", "linux_x86_64"]
    return [*cpython_tags(py, platforms=plats), *compatible_tags(py, platforms=plats)]


def parse_requirements(text: str, env: dict[str, str]) -> list[tuple[str, str]]:
    """(tên chuẩn hoá, phiên bản) của các dòng ``tên==phiên bản [; marker]`` áp dụng cho ``env``;
    bỏ ``-e .`` (chính dự án) và comment."""
    out: list[tuple[str, str]] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith(("#", "-e", "--")):
            continue
        req = Requirement(line.split(" \\")[0])
        if req.marker is not None and not Marker(str(req.marker)).evaluate(env):
            continue
        spec = next(iter(req.specifier), None)
        if spec is None or spec.operator != "==":
            raise ValueError(f"dòng không ghim phiên bản: {line}")
        out.append((canonicalize_name(req.name), spec.version))
    return out


def pick_wheels(
    lock: dict, pkgs: Iterable[tuple[str, str]], tags: Sequence[Tag]
) -> tuple[list[tuple[str, str, str]], list[str]]:
    """((url, sha256, file)…, gói thiếu wheel). Ưu tiên tag đứng trước trong ``tags``."""
    rank = {t: i for i, t in enumerate(tags)}
    index = {(canonicalize_name(p["name"]), p["version"]): p for p in lock.get("package", [])}
    got: list[tuple[str, str, str]] = []
    missing: list[str] = []
    for name, ver in pkgs:
        p = index.get((name, ver))
        if p is None:
            missing.append(f"{name}=={ver} (không có trong uv.lock)")
            continue
        best: tuple[int, str, str, str] | None = None
        for w in p.get("wheels", []):
            fn = w["url"].rsplit("/", 1)[-1]
            _, _, _, wtags = parse_wheel_filename(fn)
            r = min((rank[t] for t in wtags if t in rank), default=None)
            if r is not None and (best is None or r < best[0]):
                best = (r, w["url"], w["hash"].removeprefix("sha256:"), fn)
        if best is None:
            missing.append(f"{name}=={ver}")
        else:
            got.append(best[1:])
    return got, missing


def pypi_lock(pkgs: Iterable[tuple[str, str]], workers: int = 16) -> dict:
    """``{package: [{name, version, wheels: [{url, hash}]}]}`` dựng từ PyPI JSON API (cùng dạng
    ``uv.lock`` để dùng lại ``pick_wheels``). Gọi từ máy local (mạng tới PyPI bình thường)."""
    from concurrent.futures import ThreadPoolExecutor

    import httpx

    def one(nv: tuple[str, str]) -> dict:
        name, ver = nv
        r = httpx.get(f"https://pypi.org/pypi/{name}/{ver}/json", timeout=60, follow_redirects=True)
        r.raise_for_status()
        files = r.json().get("urls") or []
        wheels = [
            {"url": f["url"], "hash": "sha256:" + f["digests"]["sha256"]}
            for f in files
            if f.get("packagetype") == "bdist_wheel"
        ]
        return {"name": name, "version": ver, "wheels": wheels}

    with ThreadPoolExecutor(workers) as ex:
        return {"package": list(ex.map(one, list(pkgs)))}


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--group", action="append", default=[], help="nhóm dependency (lặp được)")
    ap.add_argument("--requirements", type=Path, help="dùng file này thay vì chạy uv export")
    ap.add_argument("--lock", type=Path, default=ROOT / "uv.lock")
    ap.add_argument("--python", default="3.11", help="phiên bản CPython đích (venv vLLM: 3.12)")
    ap.add_argument(
        "--pypi",
        action="store_true",
        help="lấy URL + sha256 từ PyPI JSON thay vì uv.lock (dùng với --requirements do "
        "`uv pip compile --python-platform x86_64-manylinux_2_39` sinh — venv vLLM)",
    )
    args = ap.parse_args(argv)
    if args.requirements:
        text = args.requirements.read_text(encoding="utf-8")
    else:
        cmd = ["uv", "export", "--format", "requirements-txt", "--no-hashes", "--frozen"]
        for g in args.group:
            cmd += ["--group", g]
        text = subprocess.run(cmd, cwd=ROOT, check=True, capture_output=True, text=True).stdout
    major, minor = (int(x) for x in args.python.split(".")[:2])
    env = dict(
        LINUX_ENV,
        python_version=f"{major}.{minor}",
        python_full_version=f"{major}.{minor}.0",
        implementation_version=f"{major}.{minor}.0",
    )
    pkgs = parse_requirements(text, env)
    lock = pypi_lock(pkgs) if args.pypi else tomllib.loads(args.lock.read_text(encoding="utf-8"))
    got, missing = pick_wheels(lock, pkgs, target_tags((major, minor)))
    if missing:
        print(
            f"không có wheel Linux cp{major}{minor} x86_64: " + ", ".join(missing), file=sys.stderr
        )
        return 1
    sys.stdout.buffer.write("".join(f"{u}\t{h}\t{f}\n" for u, h, f in got).encode())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
