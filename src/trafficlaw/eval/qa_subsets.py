"""M9: tập con cố định của test cho M13 (``qa_tool subsets``) + ``qa_version``.

- Đơn vị lấy mẫu: một câu, hoặc **cả cặp** ``theo_thoi_diem`` (cùng ``pair_id``) — không tách
  cặp. Tầng = ``tier × question_type``; số câu mỗi tầng chia theo tỷ lệ (phần dư lớn nhất).
- Trong mỗi tầng, đơn vị được xếp theo ``sha256(seed:tên_tập:khoá)`` rồi lấy từ đầu ⇒ chạy lại
  trên cùng test cho cùng kết quả; thêm câu mới vào test chỉ làm đổi ít phần tử.
- ``regression_100`` bỏ ``ngoai_pham_vi`` (truy hồi cần ``gold_units``).
- ``subsets.json`` ghi ``test_sha256``; test đổi ⇒ ``stale`` (M13 phải từ chối dùng).
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from trafficlaw.eval.qa_schema import QAItem


@dataclass
class SubsetSpec:
    n: int
    exclude_types: tuple[str, ...] = ()


DEFAULT_SUBSETS: dict[str, SubsetSpec] = {
    "ablation_200": SubsetSpec(200),
    "judge_200": SubsetSpec(200),
    "variance_100": SubsetSpec(100),
    "regression_100": SubsetSpec(100, ("ngoai_pham_vi",)),
}


@dataclass
class Unit:
    key: str
    stratum: str
    qids: list[str] = field(default_factory=list)


def sampling_units(items: Sequence[QAItem]) -> list[Unit]:
    units: dict[str, Unit] = {}
    for it in items:
        key = f"pair:{it.pair_id}" if it.pair_id else f"q:{it.qid}"
        st = f"{it.tier or '-'}|{it.question_type}"
        u = units.setdefault(key, Unit(key, st))
        u.qids.append(it.qid)
    return [units[k] for k in sorted(units)]


def _rank(seed: int, name: str, key: str) -> str:
    return hashlib.sha256(f"{seed}:{name}:{key}".encode()).hexdigest()


def draw(items: Sequence[QAItem], name: str, spec: SubsetSpec, seed: int = 42) -> dict[str, Any]:
    pool = [it for it in items if it.question_type not in spec.exclude_types]
    units = sampling_units(pool)
    total = sum(len(u.qids) for u in units)
    by: dict[str, list[Unit]] = defaultdict(list)
    for u in units:
        by[u.stratum].append(u)
    for k in by:
        by[k].sort(key=lambda u: _rank(seed, name, u.key))
    target = min(spec.n, total)
    # Phân bổ số câu theo tỷ lệ tầng (phần dư lớn nhất), rồi lấy đơn vị theo thứ tự băm.
    size = {k: sum(len(u.qids) for u in v) for k, v in by.items()}
    share = {k: target * size[k] / total for k in by} if total else {}
    quota = {k: math.floor(v) for k, v in share.items()}
    rest = target - sum(quota.values())
    for k in sorted(share, key=lambda k: (-(share[k] - quota[k]), k))[:rest]:
        quota[k] += 1
    chosen: list[str] = []
    by_stratum: dict[str, int] = {}
    for k in sorted(by):
        got = 0
        for u in by[k]:
            if got >= quota[k]:
                break
            chosen += u.qids
            got += len(u.qids)
        by_stratum[k] = got
    return {
        "n": len(chosen),
        "n_target": spec.n,
        "exclude_types": list(spec.exclude_types),
        "by_stratum": dict(sorted(by_stratum.items())),
        "qids": sorted(chosen),
    }


def file_sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else ""


def build_subsets(
    items: Sequence[QAItem],
    test_sha256: str,
    specs: Mapping[str, SubsetSpec] = DEFAULT_SUBSETS,
    seed: int = 42,
) -> dict[str, Any]:
    return {
        "test_sha256": test_sha256,
        "n_test": len(items),
        "seed": seed,
        "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "subsets": {name: draw(items, name, spec, seed) for name, spec in specs.items()},
    }


def subsets_status(subsets_path: Path, test_path: Path) -> str:
    """``missing`` | ``stale`` | ``ok``."""
    if not subsets_path.is_file():
        return "missing"
    cur = json.loads(subsets_path.read_text(encoding="utf-8")).get("test_sha256")
    return "ok" if cur == file_sha256(test_path) else "stale"


def qa_version(paths: Sequence[Path]) -> str:
    """Hash nội dung các file QA (thiếu file → chuỗi rỗng ở vị trí đó)."""
    h = hashlib.sha256()
    for p in paths:
        h.update(p.name.encode())
        h.update(file_sha256(p).encode())
    return h.hexdigest()


def data_version(paths: Sequence[Path]) -> str:
    """CLAUDE.md mục 10: hash ``documents.yaml``, ``unit_versions.jsonl``, ``units_added.jsonl``."""
    return qa_version(paths)


__all__ = [
    "DEFAULT_SUBSETS",
    "SubsetSpec",
    "build_subsets",
    "data_version",
    "draw",
    "file_sha256",
    "qa_version",
    "sampling_units",
    "subsets_status",
]
