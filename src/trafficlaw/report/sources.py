"""Nguồn số liệu của báo cáo: đọc file kết quả có sẵn, ghi sha256 và **từng trường đã đọc**.

Mỗi giá trị lấy ra đi qua ``Tracked`` (proxy chỉ đọc của dict/list JSON): khi một giá trị vô hướng
được lấy ra, đường dẫn của nó (``configs.G.metrics.r@5.mean``) được ghi vào ``SourceStore.used``.
``sources.json`` liệt kê các đường dẫn này ⇒ mỗi con số trong báo cáo truy được về file + trường.

File thiếu → ``MissingSourceError`` (phần báo cáo dùng nó ghi "thiếu nguồn", không tự điền).
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

KINDS = ("json", "jsonl", "jsonl_first", "yaml", "text", "hash")


class MissingSourceError(Exception):
    def __init__(self, source_id: str, path: str) -> None:
        super().__init__(f"thiếu nguồn `{source_id}`: {path}")
        self.source_id = source_id
        self.path = path


@dataclass(frozen=True)
class SourceSpec:
    id: str
    path: str
    kind: str
    module: str = "—"
    release: str | None = None


def parse_specs(
    raw: Mapping[str, Mapping[str, Any]], vars_: Mapping[str, str]
) -> dict[str, SourceSpec]:
    out: dict[str, SourceSpec] = {}
    for sid, d in raw.items():
        kind = str(d["kind"])
        if kind not in KINDS:
            raise ValueError(f"nguồn {sid}: kind {kind!r} không hợp lệ")
        out[sid] = SourceSpec(
            id=sid,
            path=str(d["path"]).format(**vars_),
            kind=kind,
            module=str(d.get("module", "—")),
            release=d.get("release"),
        )
    return out


def _fmt_key(k: Any) -> str:
    return str(k)


class Tracked(Mapping[str, Any]):
    """Proxy chỉ đọc của một dict JSON; ghi đường dẫn mỗi giá trị vô hướng được lấy ra."""

    __slots__ = ("_d", "_path", "_rec")

    def __init__(self, d: Mapping[str, Any], path: str, rec: set[str]) -> None:
        self._d = d
        self._path = path
        self._rec = rec

    def _child(self, k: Any, v: Any) -> Any:
        p = f"{self._path}.{_fmt_key(k)}" if self._path else _fmt_key(k)
        return wrap(v, p, self._rec)

    def __getitem__(self, k: str) -> Any:
        return self._child(k, self._d[k])

    def __contains__(self, k: object) -> bool:
        return k in self._d

    def __iter__(self) -> Iterator[str]:
        return iter(self._d)

    def __len__(self) -> int:
        return len(self._d)

    def __repr__(self) -> str:  # pragma: no cover - gỡ lỗi
        return f"Tracked({self._path!r})"


class TrackedList(Sequence[Any]):
    __slots__ = ("_l", "_path", "_rec")

    def __init__(self, items: Sequence[Any], path: str, rec: set[str]) -> None:
        self._l = items
        self._path = path
        self._rec = rec

    def __getitem__(self, i: Any) -> Any:  # type: ignore[override]
        if isinstance(i, slice):
            return [self[j] for j in range(*i.indices(len(self._l)))]
        return wrap(self._l[i], f"{self._path}[{i}]", self._rec)

    def __len__(self) -> int:
        return len(self._l)


def wrap(v: Any, path: str, rec: set[str]) -> Any:
    if isinstance(v, Mapping):
        return Tracked(v, path, rec)
    if isinstance(v, list):
        return TrackedList(v, path, rec)
    rec.add(path)
    return v


def plain(v: Any) -> Any:
    """Bỏ proxy (ghi mọi lá là đã dùng) — cho dữ liệu chuyển sang hàm vẽ hình."""
    if isinstance(v, Tracked):
        return {k: plain(v[k]) for k in v}
    if isinstance(v, TrackedList):
        return [plain(v[i]) for i in range(len(v))]
    return v


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


@dataclass
class SourceStore:
    root: Path
    specs: dict[str, SourceSpec]
    used: dict[str, set[str]] = field(default_factory=dict)
    missing: dict[str, str] = field(default_factory=dict)
    _cache: dict[str, Any] = field(default_factory=dict)
    _hash: dict[str, tuple[str, int]] = field(default_factory=dict)

    def path(self, sid: str) -> Path:
        return self.root / self.specs[sid].path

    def exists(self, sid: str) -> bool:
        return self.path(sid).is_file()

    def _rec(self, sid: str) -> set[str]:
        return self.used.setdefault(sid, set())

    def _load(self, sid: str) -> Any:
        if sid in self._cache:
            return self._cache[sid]
        spec = self.specs[sid]
        p = self.path(sid)
        if not p.is_file():
            self.missing[sid] = spec.path
            raise MissingSourceError(sid, spec.path)
        self._hash[sid] = (sha256_file(p), p.stat().st_size)
        text = p.read_text(encoding="utf-8") if spec.kind != "hash" else ""
        if spec.kind == "json":
            data: Any = json.loads(text)
        elif spec.kind == "yaml":
            data = yaml.safe_load(text)
        elif spec.kind == "jsonl":
            data = [json.loads(x) for x in text.splitlines() if x.strip()]
        elif spec.kind == "jsonl_first":
            first = next((x for x in text.splitlines() if x.strip()), None)
            data = json.loads(first) if first else {}
        else:  # text, hash
            data = text
        self._cache[sid] = data
        return data

    # ------------------------------------------------------------------ truy cập
    def get(self, sid: str) -> Any:
        """Dữ liệu (đã bọc ``Tracked``) của nguồn JSON/YAML/JSONL."""
        data = self._load(sid)
        if self.specs[sid].kind in ("text", "hash"):
            self._rec(sid).add("(toàn văn)" if self.specs[sid].kind == "text" else "(sha256)")
            return data
        return wrap(data, "", self._rec(sid))

    def text(self, sid: str) -> str:
        data = self._load(sid)
        self._rec(sid).add("(toàn văn)")
        return str(data)

    def sha256(self, sid: str) -> str:
        self._load(sid)
        self._rec(sid).add("(sha256)")
        return self._hash[sid][0]

    def last(self, sid: str) -> Tracked:
        """Bản ghi cuối của JSONL append-only (bản ghi hiện hành)."""
        rows = self._load(sid)
        if not rows:
            raise MissingSourceError(sid, self.specs[sid].path + " (rỗng)")
        return wrap(rows[-1], f"[{len(rows) - 1}]", self._rec(sid))

    def latest_by(self, sid: str, key: str) -> dict[str, Tracked]:
        """JSONL append-only: bản ghi mới nhất của mỗi giá trị ``key`` (thứ tự theo khoá)."""
        rows = self._load(sid)
        latest: dict[str, int] = {}
        for i, r in enumerate(rows):
            latest[str(r.get(key))] = i
        rec = self._rec(sid)
        return {k: wrap(rows[i], f"[{key}={k}]", rec) for k, i in sorted(latest.items())}

    def rows(self, sid: str) -> TrackedList:
        return wrap(self._load(sid), "", self._rec(sid))

    # ------------------------------------------------------------------ manifest
    def manifest(self) -> list[dict[str, Any]]:
        """Danh sách nguồn (đã đọc hoặc thiếu) cho ``sources.json`` — tất định, không thời gian."""
        out = []
        for sid, spec in self.specs.items():
            if sid not in self._hash and sid not in self.missing:
                continue
            row: dict[str, Any] = {
                "id": sid,
                "module": spec.module,
                "path": spec.path,
                "release": spec.release,
            }
            if sid in self.missing:
                row["status"] = "missing"
            else:
                sha, size = self._hash[sid]
                row.update(
                    status="ok", sha256=sha, bytes=size, fields=sorted(self.used.get(sid, ()))
                )
            out.append(row)
        return out


__all__ = [
    "MissingSourceError",
    "SourceSpec",
    "SourceStore",
    "Tracked",
    "TrackedList",
    "parse_specs",
    "plain",
    "sha256_file",
    "wrap",
]
