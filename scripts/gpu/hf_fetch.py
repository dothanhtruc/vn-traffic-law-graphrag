"""Tải trọng số HF bằng aria2c vào đúng cấu trúc cache của ``huggingface_hub`` (chạy TRÊN MÁY THUÊ).

Lý do (phiên GPU 7, 17/11/2026): ``huggingface_hub`` (vLLM, sentence-transformers) tải chậm trên
aidev; aria2c 16 kết nối/file tải 13 GB trong ~2 phút. Chỉ dùng thư viện chuẩn (python3 hệ thống).

    python3 hf_fetch.py <repo>@<revision> [--exclude PATTERN ...] [--include PATTERN ...]

- Danh sách file + băm từ ``/api/models/<repo>/revision/<rev>?blobs=true``.
- Blob lưu ở ``~/.cache/huggingface/hub/models--<org>--<name>/blobs/<etag>`` (LFS: sha256; file
  thường: git blob id), symlink ``snapshots/<revision>/<path>`` → blob; file LFS kiểm sha256.
- ``HF_TOKEN`` (nếu có) gửi trong header, không in ra.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

DEFAULT_EXCLUDE = ["onnx/*", "openvino/*", "*.onnx", "original/*", "metal/*", "*.msgpack", "*.h5"]


def api(repo: str, rev: str, token: str | None) -> list[dict]:
    req = urllib.request.Request(
        f"https://huggingface.co/api/models/{repo}/revision/{rev}?blobs=true"
    )
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["siblings"]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("spec", help="<repo>@<revision>")
    ap.add_argument("--exclude", action="append", default=[])
    ap.add_argument("--include", action="append", default=[])
    a = ap.parse_args()
    repo, rev = a.spec.split("@", 1)
    token = os.environ.get("HF_TOKEN") or None
    hub = Path(os.environ.get("HF_HOME", Path.home() / ".cache/huggingface")) / "hub"
    root = hub / ("models--" + repo.replace("/", "--"))
    blobs, snap = root / "blobs", root / "snapshots" / rev
    blobs.mkdir(parents=True, exist_ok=True)
    snap.mkdir(parents=True, exist_ok=True)
    files = []
    sibs = api(repo, rev, token)
    names = {s["rfilename"] for s in sibs}
    for s in sibs:
        f = s["rfilename"]
        if a.include and not any(fnmatch.fnmatch(f, p) for p in a.include):
            continue
        if any(fnmatch.fnmatch(f, p) for p in DEFAULT_EXCLUDE + a.exclude):
            continue
        # .bin trùng với safetensors → bỏ
        if (
            f.endswith(".bin")
            and f.replace("pytorch_model", "model").replace(".bin", ".safetensors") in names
        ):
            continue
        lfs = s.get("lfs") or {}
        etag = lfs.get("sha256") or s["blobId"]
        files.append((f, etag, bool(lfs)))
    todo = [(f, e) for f, e, _ in files if not (blobs / e).is_file()]
    if todo:
        inp = root / "aria2.txt"
        with inp.open("w") as fh:
            for f, e in todo:
                fh.write(
                    f"https://huggingface.co/{repo}/resolve/{rev}/{f}\n  out={e}\n  dir={blobs}\n"
                )
                if token:
                    fh.write(f"  header=Authorization: Bearer {token}\n")
        subprocess.run(
            ["aria2c", "-q", "-c", "-x16", "-s16", "-j4", "--auto-file-renaming=false",
             "--max-tries=5", "-i", str(inp)],
            check=True,
        )  # fmt: skip
        inp.unlink()
    bad = [f for f, e, is_lfs in files if is_lfs and sha256(blobs / e) != e]
    if bad:
        print(f"{repo}: sha256 sai {bad}", file=sys.stderr)
        return 1
    for f, e, _ in files:
        link = snap / f
        link.parent.mkdir(parents=True, exist_ok=True)
        if link.is_symlink() or link.exists():
            link.unlink()
        link.symlink_to(os.path.relpath(blobs / e, link.parent))
    size = sum((blobs / e).stat().st_size for _, e, _ in files)
    print(f"{repo}@{rev[:7]}: {len(files)} file, {size / 2**30:.2f} GiB (tải {len(todo)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
