"""Ghép báo cáo M16: ``report.md`` + ``figures/*.png`` + ``sources.json`` (I/O ở đây).

Tất định: không ghi thời gian; cùng file nguồn + cùng commit ⇒ cùng byte (hình: cùng phiên bản
matplotlib). Không GPU, không mạng, không gọi LLM.
"""

from __future__ import annotations

import hashlib
import json
import logging
import re
import unicodedata
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from trafficlaw.report import figures as figs
from trafficlaw.report.fmt import vn_int, vn_pct
from trafficlaw.report.sections import Ctx, build_sections
from trafficlaw.report.sources import MissingSourceError, SourceStore, parse_specs
from trafficlaw.report.texts import set_defaults, t

log = logging.getLogger(__name__)

CI_LEVEL = 0.95  # mức CI của eval/stats.py (phân vị hai đuôi của bootstrap)


@dataclass
class ReportResult:
    out_dir: Path
    report_path: Path
    figures: list[str]
    skipped_figures: list[str]
    missing: dict[str, str]
    lech: int
    errors: list[str]


def load_config(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _anchor(title: str) -> str:
    s = unicodedata.normalize("NFC", title).lower()
    s = re.sub(r"[^\w\s-]", "", s)
    return re.sub(r"\s+", "-", s.strip())


def build_report(
    root: Path,
    cfg: Mapping[str, Any],
    *,
    run_id: str | None = None,
    out_dir: Path | None = None,
    git_commit: str | None = None,
    draw: bool = True,
) -> ReportResult:
    run_id = run_id or str(cfg["run_id"])
    vars_ = {
        "run_id": run_id,
        "variance_run": str(cfg["variance_run"]),
        "dev_run": str(cfg["dev_run"]),
    }
    store = SourceStore(root=root, specs=parse_specs(cfg["sources"], vars_))
    try:
        stats = store.get("eval_cfg")["stats"]
        n_boot, seed = vn_int(stats["bootstrap"]), str(stats["seed"])
    except MissingSourceError:
        n_boot = seed = "—"
    set_defaults(ci=vn_pct(CI_LEVEL, 0), n_boot=n_boot, seed=seed)

    ctx = Ctx(store=store, cfg=cfg)
    sections = build_sections(ctx)

    out = out_dir or (root / str(cfg["out_dir"]) / run_id)
    fig_dir = out / "figures"
    drawn: list[str] = []
    skipped: list[str] = []
    can_draw = draw and figs.available()
    dpi = int(cfg.get("figure_dpi", 150))
    if fig_dir.is_dir():
        for p in fig_dir.glob("*.png"):
            p.unlink()
    for f in ctx.figures:
        if not can_draw:
            skipped.append(f.name)
            continue
        getattr(figs, f.fn)(fig_dir / f"{f.name}.png", dpi=dpi, **f.kwargs)
        drawn.append(f.name)

    md = [f"# {t('title')}", "", t("preamble", run_id=run_id), ""]
    if skipped:
        md += [
            "> Hình chưa vẽ (thiếu matplotlib — chạy với `uv run --group report`): "
            + ", ".join(f"`{x}`" for x in skipped),
            "",
        ]
    md += [f"## {t('toc')}", ""]
    md += [f"- [{s.title}](#{_anchor(s.title)})" for s in sections] + [""]
    for s in sections:
        md += [f"## {s.title}", "", s.body.strip(), ""]
    text = "\n".join(md).rstrip() + "\n"
    out.mkdir(parents=True, exist_ok=True)
    report_path = out / "report.md"
    report_path.write_text(text, encoding="utf-8", newline="\n")

    lech = text.count(t("lech"))
    manifest = {
        "run_id": run_id,
        "git_commit": git_commit,
        "report_md_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "figures": {
            n: hashlib.sha256((fig_dir / f"{n}.png").read_bytes()).hexdigest() for n in drawn
        },
        "figures_skipped": skipped,
        "matplotlib": _mpl_version() if drawn else None,
        "missing": dict(sorted(store.missing.items())),
        "consistency_mismatches": lech,
        "section_errors": ctx.errors,
        "sources": store.manifest(),
    }
    (out / "sources.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return ReportResult(out, report_path, drawn, skipped, dict(store.missing), lech, ctx.errors)


def _mpl_version() -> str | None:
    try:
        import matplotlib
    except ImportError:  # pragma: no cover
        return None
    return str(matplotlib.__version__)


__all__ = ["CI_LEVEL", "ReportResult", "build_report", "load_config"]
