"""M4: đối chiếu phiên bản điều khoản với VBHN, in tỷ lệ Khoản khớp.

    uv run python -m scripts.compare_vbhn [--vbhn ID ...] [--repo-root PATH]

Đọc ``units.jsonl``, ``unit_versions.jsonl``, ``units_added.jsonl`` và ``vbhn_map.yaml``; ghi
``vbhn_compare.jsonl`` (một dòng mỗi Khoản) + ``vbhn_compare_summary.md`` (ghi đè mỗi lần chạy,
việc so chỉ mất vài giây). Khớp = bằng nhau sau chuẩn hoá mạnh (chỉ giữ chữ và số).

Mã thoát 1 nếu tỷ lệ khớp của một VBHN < ``min_match_rate`` hoặc kiểm tra chéo
(``crosscheck_source``) có chú thích không ứng với phiên bản cùng ngày.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import yaml

from trafficlaw.ingest.amendment_pipeline import load_units
from trafficlaw.ingest.vbhn import EXCLUDED, CompareResult, compare_vbhn, load_vbhn_map
from trafficlaw.ingest.versions import AddedUnit, VersionStore
from trafficlaw.registry.loader import load_registry
from trafficlaw.utils.jsonl import read_jsonl, write_jsonl
from trafficlaw.utils.logging import setup_logging
from trafficlaw.utils.seed import set_seed

REPO_ROOT = Path(__file__).resolve().parents[1]
_STATUSES = (
    "khop",
    "chi_khac_dinh_dang",
    "khac_noi_dung",
    "thieu_vbhn",
    "thieu_goc",
    "loai_ngoai_danh_muc",
    "loai_loi_du_lieu",
)


def _load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def summary_markdown(results: list[tuple[str, str, CompareResult, float]]) -> str:
    head = (
        "| VBHN | văn bản gốc | as_of | " + " | ".join(_STATUSES) + " | so | khớp | tỷ lệ | chéo |"
    )
    lines = [head, "|" + "---|" * (len(_STATUSES) + 8)]
    for vb, base, r, _min in results:
        cross = (
            f"{r.crosscheck_checked - len(r.crosscheck_failures)}/{r.crosscheck_checked}"
            f" (bỏ {r.crosscheck_skipped})"
            if r.crosscheck_checked or r.crosscheck_skipped
            else "—"
        )
        lines.append(
            f"| {vb} | {base[0]} | {base[1]} | "
            + " | ".join(str(r.count(s)) for s in _STATUSES)
            + f" | {r.n_compared} | {r.n_match} | {r.match_rate:.2%} | {cross} |"
        )
    lines.append(
        "\n`so` = Khoản đưa vào tỷ lệ (bỏ `loai_*`); `khớp` = `khop` + `chi_khac_dinh_dang`; "
        "`chéo` = chú thích nguồn trong danh mục có phiên bản cùng ngày "
        "(bỏ: chú thích Mẫu/Phụ lục không có unit gốc)."
    )
    for vb, _base, r, _min in results:
        bad = [x for x in r.rows if x.status in ("khac_noi_dung", "thieu_vbhn", "thieu_goc")]
        if bad:
            lines.append(f"\n### {vb}: Khoản lệch\n")
            lines.append("| unit | trạng thái | ratio |\n|---|---|---:|")
            lines += [
                f"| {x.unit_id} | {x.status} | {x.ratio if x.ratio is not None else ''} |"
                for x in bad
            ]
        if r.crosscheck_failures:
            lines.append(f"\n### {vb}: kiểm tra chéo không đạt\n")
            lines += [f"- {f}" for f in r.crosscheck_failures]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--vbhn", action="append", default=None, help="chỉ so VBHN này")
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT, help=argparse.SUPPRESS)
    args = ap.parse_args(argv)
    set_seed()
    setup_logging("WARNING")
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="replace")

    root: Path = args.repo_root
    paths = _load_yaml(REPO_ROOT / "configs" / "paths.yaml")
    registry = load_registry(root / paths["documents"])
    so_hieu = {(d.so_hieu or "").upper(): d.doc_id for d in registry if d.so_hieu}
    entries = load_vbhn_map(root / paths["vbhn_map"])
    if args.vbhn:
        entries = [e for e in entries if e.vbhn in set(args.vbhn)]
    units = load_units(root / paths["units"])
    store = VersionStore.load(root / paths["unit_versions"])
    added = [AddedUnit.model_validate(r) for r in read_jsonl(root / paths["units_added"])]

    results: list[tuple[str, str, CompareResult, float]] = []
    rows: list[Any] = []
    bad = False
    for e in entries:
        r = compare_vbhn(
            e,
            units.get(e.vbhn, []),
            units.get(e.base_doc, []),
            [a for a in added if a.doc_id == e.base_doc],
            store,
            so_hieu,
        )
        results.append((e.vbhn, (e.base_doc, e.as_of), r, e.min_match_rate))  # type: ignore[arg-type]
        rows.extend(r.rows)
        n_excl = sum(r.count(s) for s in EXCLUDED)
        ok = r.match_rate >= e.min_match_rate and not r.crosscheck_failures
        bad |= not ok
        print(
            f"{e.vbhn:<22} ↔ {e.base_doc:<12} @ {e.as_of}: khớp {r.n_match}/{r.n_compared} "
            f"= {r.match_rate:.2%} (loại {n_excl})"
            + (
                f"  · chéo {r.crosscheck_checked - len(r.crosscheck_failures)}"
                f"/{r.crosscheck_checked}"
                if r.crosscheck_checked
                else ""
            )
            + ("" if ok else "  <-- KHÔNG ĐẠT")
        )
    write_jsonl(root / paths["vbhn_compare"], rows)
    summary = root / paths["vbhn_compare_summary"]
    summary.write_text(summary_markdown(results), encoding="utf-8", newline="\n")
    print(f"bảng tổng hợp: {summary}")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
