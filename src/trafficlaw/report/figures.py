"""Hình PNG tất định cho báo cáo (matplotlib, nhóm uv ``report``; nhập lười).

Tất định: backend Agg, font DejaVu Sans (đi kèm matplotlib, có dấu tiếng Việt), DPI cố định,
``metadata={"Software": None}`` (không ghi phiên bản/thời gian vào PNG). Dữ liệu vào là số thuần
(đã ``plain``); hàm không đọc file.

Màu: bảng phân loại tham chiếu (slot cố định theo thực thể, không theo hạng), nền sáng (in ấn).
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Any

SERIES = ("#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948")
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
GRID = "#e4e3df"


def available() -> bool:
    try:
        import matplotlib  # noqa: F401
    except ImportError:
        return False
    return True


def _plt() -> Any:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "axes.edgecolor": INK_2,
            "axes.labelcolor": INK_2,
            "axes.titlecolor": INK,
            "axes.titlesize": 10,
            "xtick.color": INK_2,
            "ytick.color": INK_2,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "figure.facecolor": SURFACE,
            "axes.facecolor": SURFACE,
            "savefig.facecolor": SURFACE,
            "legend.frameon": False,
            "path.simplify": False,
            "svg.hashsalt": "trafficlaw",
        }
    )
    return plt


def _save(fig: Any, path: Path, dpi: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=dpi, metadata={"Software": None}, bbox_inches="tight", pad_inches=0.1)
    import matplotlib.pyplot as plt

    plt.close(fig)


def _grid(ax: Any, axis: str = "y") -> None:
    from matplotlib.ticker import FuncFormatter

    ax.grid(axis=axis, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    fmt = FuncFormatter(lambda v, _pos: f"{v:g}".replace("-", "−").replace(".", ","))
    (ax.yaxis if axis == "y" else ax.xaxis).set_major_formatter(fmt)


def _vn(x: float, nd: int = 0) -> str:
    return f"{x:.{nd}f}".replace(".", ",")


def grouped_bars(
    path: Path,
    groups: Sequence[str],
    series: Sequence[dict[str, Any]],
    *,
    ylabel: str,
    title: str,
    dpi: int,
    ylim: tuple[float, float] = (0.0, 100.0),
) -> None:
    """Cột nhóm theo ``groups``; mỗi series ``{label, values, lo, hi}`` (``None`` = không có)."""
    plt = _plt()
    k = len(series)
    width = 0.8 / max(k, 1)
    fig, ax = plt.subplots(figsize=(max(5.0, 0.75 * len(groups) * max(k, 1) + 1.5), 3.4))
    for j, s in enumerate(series):
        xs, ys, err_lo, err_hi = [], [], [], []
        for i, v in enumerate(s["values"]):
            if v is None:
                continue
            xs.append(i + (j - (k - 1) / 2) * width)
            ys.append(v)
            lo, hi = s["lo"][i], s["hi"][i]
            err_lo.append(v - lo if lo is not None else 0.0)
            err_hi.append(hi - v if hi is not None else 0.0)
        ax.bar(
            xs,
            ys,
            width=width * 0.92,
            color=SERIES[j],
            label=s["label"],
            edgecolor=SURFACE,
            linewidth=1.0,
        )
        ax.errorbar(
            xs, ys, yerr=[err_lo, err_hi], fmt="none", ecolor=INK_2, elinewidth=0.9, capsize=2.5
        )
    ax.set_xticks(range(len(groups)), list(groups))
    ax.set_ylim(*ylim)
    ax.set_ylabel(ylabel)
    ax.set_title(title, loc="left")
    _grid(ax)
    if k > 1:
        ax.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0))
    _save(fig, path, dpi)


def forest(
    path: Path,
    panels: Sequence[dict[str, Any]],
    *,
    title: str,
    xlabel: str,
    dpi: int,
    sig_label: str,
    nonsig_label: str,
) -> None:
    """Small multiples: mỗi panel ``{title, rows: [{label, diff, lo, hi, sig}]}``; vạch 0."""
    plt = _plt()
    n = len(panels)
    nrow = max((len(p["rows"]) for p in panels), default=1)
    fig, axes = plt.subplots(1, n, figsize=(3.0 * n + 0.8, 0.42 * nrow + 1.4), sharey=False)
    axes = list(axes) if n > 1 else [axes]
    for ax, p in zip(axes, panels, strict=True):
        rows = p["rows"]
        ys = list(range(len(rows)))[::-1]
        for y, r in zip(ys, rows, strict=True):
            ax.plot(
                [r["lo"], r["hi"]], [y, y], color=SERIES[0], linewidth=2.0, solid_capstyle="round"
            )
            ax.plot(
                [r["diff"]],
                [y],
                marker="o",
                markersize=7,
                markerfacecolor=SERIES[0] if r["sig"] else SURFACE,
                markeredgecolor=SERIES[0],
                markeredgewidth=1.6,
                linestyle="none",
            )
        ax.axvline(0.0, color=INK_2, linewidth=0.8)
        ax.set_yticks(ys, [r["label"] for r in rows])
        ax.set_title(p["title"], loc="left")
        ax.set_xlabel(xlabel)
        _grid(ax, "x")
    h1 = plt.Line2D(
        [],
        [],
        marker="o",
        color=SERIES[0],
        markerfacecolor=SERIES[0],
        linestyle="none",
        label=sig_label,
    )
    h2 = plt.Line2D(
        [],
        [],
        marker="o",
        color=SERIES[0],
        markerfacecolor=SURFACE,
        linestyle="none",
        label=nonsig_label,
    )
    fig.legend(handles=[h1, h2], loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.02))
    fig.suptitle(title, x=0.01, ha="left", color=INK, fontsize=10)
    fig.tight_layout(rect=(0, 0.06, 1, 0.95))
    _save(fig, path, dpi)


def hbars(
    path: Path,
    categories: Sequence[str],
    series: Sequence[dict[str, Any]],
    *,
    xlabel: str,
    title: str,
    dpi: int,
    xlim: tuple[float, float] = (0.0, 100.0),
) -> None:
    """Thanh ngang nhóm theo hạng mục (vd R@5 theo loại câu); series ``{label, values}``."""
    plt = _plt()
    k = len(series)
    h = 0.8 / max(k, 1)
    fig, ax = plt.subplots(figsize=(6.2, 0.32 * len(categories) * k + 1.2))
    for j, s in enumerate(series):
        ys, xs = [], []
        for i, v in enumerate(s["values"]):
            if v is None:
                continue
            ys.append(len(categories) - 1 - i + ((k - 1) / 2 - j) * h)
            xs.append(v)
        ax.barh(
            ys,
            xs,
            height=h * 0.92,
            color=SERIES[j],
            label=s["label"],
            edgecolor=SURFACE,
            linewidth=1.0,
        )
    ax.set_yticks(range(len(categories))[::-1], list(categories))
    ax.set_xlim(*xlim)
    ax.set_xlabel(xlabel)
    ax.set_title(title, loc="left")
    _grid(ax, "x")
    if k > 1:
        ax.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0))
    _save(fig, path, dpi)


def stacked_hbars(
    path: Path,
    categories: Sequence[str],
    stacks: Sequence[dict[str, Any]],
    *,
    xlabel: str,
    title: str,
    dpi: int,
) -> None:
    """Thanh ngang xếp chồng; ``stacks`` ``{label, values}`` theo thứ tự cố định."""
    plt = _plt()
    fig, ax = plt.subplots(figsize=(6.2, 0.36 * len(categories) + 1.2))
    left = [0.0] * len(categories)
    ys = list(range(len(categories)))[::-1]
    for j, s in enumerate(stacks):
        vals = [float(v or 0) for v in s["values"]]
        ax.barh(
            ys,
            vals,
            left=left,
            height=0.7,
            color=SERIES[j],
            label=s["label"],
            edgecolor=SURFACE,
            linewidth=1.5,
        )
        left = [a + b for a, b in zip(left, vals, strict=True)]
    for y, tot in zip(ys, left, strict=True):
        ax.text(tot + 0.8, y, _vn(tot), va="center", color=INK_2, fontsize=8)
    ax.set_yticks(ys, list(categories))
    ax.set_xlabel(xlabel)
    ax.set_title(title, loc="left")
    ax.set_xlim(0, max(left, default=1) * 1.12)
    _grid(ax, "x")
    ax.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0))
    _save(fig, path, dpi)


def step_lines(
    path: Path,
    panels: Sequence[dict[str, Any]],
    *,
    ylabel: str,
    xlabel: str,
    base_label: str,
    title: str,
    dpi: int,
) -> None:
    """Panel ``{title, series: [{label, xs, ys}], base}``: chỉ số val theo bước, vạch model gốc."""
    plt = _plt()
    n = len(panels)
    fig, axes = plt.subplots(1, n, figsize=(3.4 * n + 1.2, 3.0))
    axes = list(axes) if n > 1 else [axes]
    for ax, p in zip(axes, panels, strict=True):
        for j, s in enumerate(p["series"]):
            ax.plot(
                s["xs"],
                s["ys"],
                color=SERIES[j],
                linewidth=2.0,
                marker="o",
                markersize=5,
                label=s["label"],
            )
        if p.get("base") is not None:
            ax.axhline(p["base"], color=INK_2, linewidth=1.0, linestyle="--", label=base_label)
        ax.set_title(p["title"], loc="left")
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        _grid(ax)
        ax.legend(loc="lower right", fontsize=8)
    fig.suptitle(title, x=0.01, ha="left", color=INK, fontsize=10)
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    _save(fig, path, dpi)


__all__ = ["available", "forest", "grouped_bars", "hbars", "stacked_hbars", "step_lines"]
