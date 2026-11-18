"""Tổng hợp + báo cáo theo run của M13 (``summary.{json,md}``). Báo cáo tự động đầy đủ là M16.

Quy tắc:

- Trung bình mỗi chỉ số trên các câu có giá trị (``None`` = không áp dụng); luôn kèm ``n``.
  CI 95% bootstrap (``stats.bootstrap`` lần, ``stats.seed``) theo câu.
- So sánh: ``compare_to`` (G) với từng cấu hình, **chỉ trên câu cả hai đã có giá trị** của chỉ
  số đó. Chỉ số đúng/sai (``BINARY_METRICS``) → McNemar chính xác; còn lại → Wilcoxon Pratt.
  Holm hiệu chỉnh trong **từng chỉ số** (họ = các cấu hình được so với G); báo cả p thô.
- Từ chối: câu **nên từ chối** = ``ngoai_pham_vi`` + câu có gold rỗng (câu "trước mốc" của cặp
  ``theo_thoi_diem``: điều khoản chưa có hiệu lực — sửa M13c 18/11/2026, trước đó bị tính là từ
  chối nhầm). precision = câu nên từ chối bị từ chối / mọi câu bị từ chối (``precision_oos``: chỉ
  tính ``ngoai_pham_vi`` như M13 cũ); recall = câu ``ngoai_pham_vi`` bị từ chối / mọi câu
  ``ngoai_pham_vi``; ``tu_choi_sai`` = câu có gold bị từ chối / mọi câu có gold.
"""

from __future__ import annotations

import statistics
from collections import Counter, defaultdict
from collections.abc import Mapping, Sequence
from typing import Any

from trafficlaw.eval.answer_metrics import BINARY_METRICS, RETRIEVAL_METRICS
from trafficlaw.eval.stats import (
    bootstrap_diff_ci,
    bootstrap_mean_ci,
    holm,
    mcnemar_exact,
    wilcoxon_signed_rank,
)

#: Thứ tự chỉ số trong bảng chính.
MAIN_METRICS = (
    "judge_dung",
    "judge_diem",
    "tu_choi_dung",
    "so_du",
    "so_recall",
    "trich_gold",
    "trich_p",
    "trich_r",
    "hieu_luc_trich",
    "phien_ban_dung",
    "r@1",
    "r@5",
    "r@10",
    "r@20",
    "mrr@10",
    "ndcg@10",
)
BREAKDOWN_METRICS = (
    "judge_dung",
    "tu_choi_dung",
    "so_du",
    "trich_gold",
    "trich_r",
    "phien_ban_dung",
    "r@5",
)
DA_BUOC_METRICS = ("db_top5", "db_ngu_canh", "db_trich", "db_du")
VERIFY_METRICS = ("vp_truoc", "vp_sau", "cau_bo", "trich_bia", "so_tu_do", "hieu_luc_nguon")
COMPARE_METRICS = (
    "judge_dung",
    "judge_diem",
    "tu_choi_dung",
    "so_du",
    "so_recall",
    "trich_gold",
    "trich_r",
    "phien_ban_dung",
    "r@5",
    "mrr@10",
)

LABELS = {
    "judge_dung": "Judge: đúng hoàn toàn",
    "judge_diem": "Judge: điểm TB (0–2)",
    "tu_choi_dung": "Từ chối đúng",
    "so_du": "Đủ con số yêu cầu",
    "so_recall": "Recall con số",
    "trich_gold": "Có trích dẫn tới gold",
    "trich_p": "Citation P",
    "trich_r": "Citation R",
    "hieu_luc_trich": "Trích dẫn còn hiệu lực",
    "phien_ban_dung": "Đúng phiên bản (theo thời điểm)",
    "r@1": "Recall@1",
    "r@5": "Recall@5",
    "r@10": "Recall@10",
    "r@20": "Recall@20",
    "mrr@10": "MRR@10",
    "ndcg@10": "nDCG@10",
    "db_top5": "Đa bước: gold trong top-5",
    "db_ngu_canh": "Đa bước: gold trong ngữ cảnh",
    "db_trich": "Đa bước: gold được trích",
    "db_du": "Đa bước: ngữ cảnh phủ đủ gold",
    "vp_truoc": "Vi phạm số trước sửa (TB/câu)",
    "vp_sau": "Vi phạm số sau sửa (TB/câu)",
    "cau_bo": "Câu văn bị bỏ (TB/câu)",
    "trich_bia": "B0: trích dẫn bịa (TB/câu)",
    "so_tu_do": "B0: số không kiểm được (TB/câu)",
    "hieu_luc_nguon": "Nguồn còn hiệu lực",
}


def metric_values(rows: Sequence[Mapping[str, Any]], m: str) -> list[float]:
    return [float(v) for r in rows if (v := r["metrics"].get(m)) is not None]


def describe(
    rows: Sequence[Mapping[str, Any]],
    metrics: Sequence[str],
    *,
    ci: bool = True,
    n_boot: int = 1000,
    seed: int = 42,
) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for m in metrics:
        vals = metric_values(rows, m)
        if not vals:
            continue
        d: dict[str, Any] = {"n": len(vals), "mean": statistics.fmean(vals)}
        if ci:
            d["ci"] = bootstrap_mean_ci(vals, n=n_boot, seed=seed)
        out[m] = d
    return out


def breakdown(
    rows: Sequence[Mapping[str, Any]], key: str, metrics: Sequence[str]
) -> dict[str, dict[str, dict[str, Any]]]:
    groups: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    for r in rows:
        groups[str(r.get(key) or "—")].append(r)
    return {g: describe(v, metrics, ci=False) for g, v in sorted(groups.items())}


def refusal_stats(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    done = [r for r in rows if r["metrics"].get("tu_choi") is not None]
    oos = [r for r in done if r["question_type"] == "ngoai_pham_vi"]
    empty = [r for r in done if r.get("gold_rong")]
    has_gold = [r for r in done if r["question_type"] != "ngoai_pham_vi" and not r.get("gold_rong")]

    def refused(rs: Sequence[Mapping[str, Any]]) -> int:
        return sum(1 for r in rs if r["metrics"]["tu_choi"] == 1.0)

    n_ref = refused(done)
    tp = refused(oos)
    return {
        "n": len(done),
        "n_ngoai_pham_vi": len(oos),
        "n_gold_rong": len(empty),
        "n_tu_choi": n_ref,
        "precision": (tp + refused(empty)) / n_ref if n_ref else None,
        "precision_oos": tp / n_ref if n_ref else None,
        "recall": tp / len(oos) if oos else None,
        "tu_choi_gold_rong": refused(empty) / len(empty) if empty else None,
        "tu_choi_sai": refused(has_gold) / len(has_gold) if has_gold else None,
    }


def compare(
    base: Sequence[Mapping[str, Any]],
    others: Mapping[str, Sequence[Mapping[str, Any]]],
    metrics: Sequence[str] = COMPARE_METRICS,
    *,
    n_boot: int = 1000,
    seed: int = 42,
) -> dict[str, dict[str, dict[str, Any]]]:
    """``{cfg: {metric: {...}}}``; Holm trong từng chỉ số."""
    bmap = {r["qid"]: r["metrics"] for r in base}
    res: dict[str, dict[str, dict[str, Any]]] = {c: {} for c in others}
    for m in metrics:
        tested: list[tuple[str, float]] = []
        for cfg, rows in others.items():
            pa: list[float] = []
            pb: list[float] = []
            for r in rows:
                a = bmap.get(r["qid"], {}).get(m)
                b = r["metrics"].get(m)
                if a is None or b is None:
                    continue
                pa.append(float(a))
                pb.append(float(b))
            if not pa:
                continue
            d: dict[str, Any] = {
                "n": len(pa),
                "mean_base": statistics.fmean(pa),
                "mean_other": statistics.fmean(pb),
                "diff": statistics.fmean(pa) - statistics.fmean(pb),
                "diff_ci": bootstrap_diff_ci(pa, pb, n=n_boot, seed=seed),
            }
            if m in BINARY_METRICS:
                t = mcnemar_exact([x == 1.0 for x in pa], [x == 1.0 for x in pb])
                d.update(test="mcnemar_exact", b=t.b, c=t.c, p=t.p)
            else:
                w = wilcoxon_signed_rank(pa, pb)
                d.update(test="wilcoxon_pratt", n_zero=w.n_zero, z=w.z, p=w.p)
            res[cfg][m] = d
            tested.append((cfg, d["p"]))
        adj = holm([p for _, p in tested])
        for (cfg, _), pa_ in zip(tested, adj, strict=True):
            res[cfg][m]["p_holm"] = pa_
    return res


DEV_METRICS = (
    "judge_dung",
    "judge_diem",
    "so_du",
    "so_recall",
    "trich_gold",
    "phien_ban_dung",
    "db_top5",
    "db_ngu_canh",
    "db_du",
    "r@5",
    "tu_choi",
    "tu_choi_dung",
    "vp_sau",
    "cau_bo",
)
"""Chỉ số so biến thể trên tập dev (M13c); ``tu_choi`` chỉ tính trên câu trả lời được."""


def compare_runs(
    base: Sequence[Mapping[str, Any]],
    others: Mapping[str, Sequence[Mapping[str, Any]]],
    *,
    question_types: Sequence[str] | None = None,
    metrics: Sequence[str] = DEV_METRICS,
    n_boot: int = 1000,
    seed: int = 42,
) -> dict[str, Any]:
    """So các biến thể (có thể ở lượt chạy khác nhau) với ``base`` trên cùng câu.

    ``tu_choi`` chỉ lấy câu không phải ``ngoai_pham_vi`` (= tỷ lệ từ chối nhầm); ``tu_choi_dung``
    giữ mọi câu. Lọc ``question_types`` trước khi ghép cặp."""

    def keep(rows: Sequence[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
        return [r for r in rows if not question_types or r["question_type"] in question_types]

    def answerable(rows: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
        out = []
        for r in rows:
            m = dict(r["metrics"])
            if r["question_type"] == "ngoai_pham_vi":
                m["tu_choi"] = None
            out.append({**r, "metrics": m})
        return out

    kb = keep(base)
    ko = {k: keep(v) for k, v in others.items()}
    b = answerable(kb)
    o = {k: answerable(v) for k, v in ko.items()}
    present = [m for m in metrics if any(r["metrics"].get(m) is not None for r in b)]
    return {
        "question_types": list(question_types or []),
        "n_base": len(b),
        "describe": {
            name: describe(rows, present, n_boot=n_boot, seed=seed)
            for name, rows in {"base": b, **o}.items()
        },
        "refusal": {name: refusal_stats(rows) for name, rows in {"base": kb, **ko}.items()},
        "compare": compare(b, o, present, n_boot=n_boot, seed=seed),
    }


def render_compare_runs_md(res: Mapping[str, Any], labels: Mapping[str, str]) -> str:
    names = list(res["describe"])
    head = ["Chỉ số"] + [labels.get(n, n) for n in names]
    lines = [
        f"Loại câu: {', '.join(res['question_types']) or 'tất cả'} · n = {res['n_base']}",
        "",
        "| " + " | ".join(head) + " |",
        "|" + "---|" * len(head),
    ]
    metrics = list(res["describe"]["base"])
    for m in metrics:
        cells = [LABELS.get(m, m)]
        for n in names:
            d = res["describe"][n].get(m) or {}
            cell = _cell(d, m, with_ci=False)
            c = res["compare"].get(n, {}).get(m) if n != "base" else None
            if c:
                cell += f" (p {_p(c.get('p'))})"
            cells.append(cell)
        lines.append("| " + " | ".join(cells) + " |")
    lines += ["", "| Từ chối | " + " | ".join(labels.get(n, n) for n in names) + " |"]
    lines.append("|" + "---|" * (len(names) + 1))
    for k in ("precision", "precision_oos", "recall", "tu_choi_gold_rong", "tu_choi_sai"):
        lines.append(f"| {k} | " + " | ".join(_pct(res["refusal"][n].get(k)) for n in names) + " |")
    return "\n".join(lines) + "\n"


def pair_summary(pair_flags: Mapping[str, float]) -> dict[str, Any]:
    vals = list(pair_flags.values())
    return {"n": len(vals), "dung": statistics.fmean(vals) if vals else None}


def variance_summary(
    per_seed: Mapping[int, Sequence[Mapping[str, Any]]],
    answers: Mapping[int, Mapping[str, str]],
    metrics: Sequence[str] = ("tu_choi_dung", "so_du", "so_recall", "trich_gold", "trich_r"),
) -> dict[str, Any]:
    """Trung bình mỗi seed trên **tập câu chung** + độ lệch chuẩn (mẫu) giữa các seed."""
    if not per_seed:
        return {}
    common = set.intersection(*({r["qid"] for r in rows} for rows in per_seed.values()))
    out: dict[str, Any] = {"seeds": sorted(per_seed), "n_common": len(common), "metrics": {}}
    for m in metrics:
        means = {}
        for s, rows in per_seed.items():
            vals = [
                r["metrics"][m]
                for r in rows
                if r["qid"] in common and r["metrics"].get(m) is not None
            ]
            if vals:
                means[s] = statistics.fmean(vals)
        if means:
            out["metrics"][m] = {
                "per_seed": dict(sorted(means.items())),
                "std": statistics.stdev(means.values()) if len(means) > 1 else 0.0,
            }
    if len(answers) > 1:
        same = sum(1 for q in common if len({answers[s].get(q, "") for s in answers}) == 1)
        out["ty_le_cau_tra_loi_giong_het"] = same / len(common) if common else None
    return out


# --------------------------------------------------------------------------- markdown


def _pct(x: Any) -> str:
    return f"{100 * float(x):.1f}" if isinstance(x, (int, float)) else "—"


def _num(x: Any, nd: int = 3) -> str:
    return f"{float(x):.{nd}f}" if isinstance(x, (int, float)) else "—"


def _ci(d: Mapping[str, Any] | None, scale: float = 100.0) -> str:
    if not d or not d.get("ci"):
        return ""
    lo, hi = d["ci"]
    return f" ({scale * lo:.1f}–{scale * hi:.1f})" if scale == 100 else f" ({lo:.2f}–{hi:.2f})"


def _p(x: Any) -> str:
    if not isinstance(x, (int, float)):
        return "—"
    return "<0,001" if x < 0.001 else f"{x:.3f}"


def _cell(d: Mapping[str, Any] | None, m: str, with_ci: bool = True) -> str:
    if not d:
        return "—"
    if m in ("judge_diem",) or m in VERIFY_METRICS and m != "hieu_luc_nguon":
        return f"{d['mean']:.2f}" + (_ci(d, 1.0) if with_ci else "") + f" [{d['n']}]"
    return _pct(d["mean"]) + (_ci(d) if with_ci else "") + f" [{d['n']}]"


def render_summary_md(s: Mapping[str, Any]) -> str:
    cfgs: dict[str, Any] = s["configs"]
    names = list(cfgs)
    md = [
        f"# M13 — kết quả đánh giá run `{s['run_id']}`",
        "",
        f"Sinh lúc {s.get('generated_at')} · commit `{s.get('git_commit')}` · data_version"
        f" `{str(s.get('data_version'))[:12]}` · qa_version `{str(s.get('qa_version'))[:12]}` ·"
        f" test_sha256 `{str(s.get('test_sha256'))[:12]}` · {s.get('n_test')} câu test hợp lệ"
        f" ({len(s.get('invalid') or [])} câu bị loại vì lỗi validator).",
        "",
        "Ô bảng: phần trăm (hoặc trung bình) · (CI 95% bootstrap 1.000 lần) · [n câu có giá trị]."
        " `error` không tính (chưa xong); `format_error` tính là sai.",
        "",
    ]
    if s.get("limitations"):
        md += ["## Hạn chế cần đọc trước", ""] + [f"- {x}" for x in s["limitations"]] + [""]
    md += [
        "## Độ phủ",
        "",
        "| Cấu hình | tập sinh | n_done/n_total | ok | format_error | error | model | prompt |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for c, d in cfgs.items():
        st = d.get("statuses") or {}
        md.append(
            f"| {c} | {d.get('set', '—')} | {d.get('n_done', 0)}/{d.get('n_total', 0)} |"
            f" {st.get('ok', 0)} | {st.get('format_error', 0)} | {st.get('error', 0)} |"
            f" {d.get('model_id') or '—'} | `{str(d.get('prompt_hash') or '—')[:10]}` |"
        )
    md += ["", "## Bảng chính", ""]
    md += ["| Chỉ số | " + " | ".join(names) + " |", "| --- |" + " --- |" * len(names)]
    for m in MAIN_METRICS:
        if not any(m in cfgs[c]["metrics"] for c in names):
            continue
        md.append(
            f"| {LABELS.get(m, m)} | "
            + " | ".join(_cell(cfgs[c]["metrics"].get(m), m) for c in names)
            + " |"
        )
    md.append(
        "| Từ chối: precision / recall / từ chối nhầm câu có gold | "
        + " | ".join(
            f"{_pct(cfgs[c]['refusal'].get('precision'))}"
            f" / {_pct(cfgs[c]['refusal'].get('recall'))}"
            f" / {_pct(cfgs[c]['refusal'].get('tu_choi_sai'))}"
            for c in names
        )
        + " |"
    )
    md.append(
        "| Cặp theo thời điểm đúng | "
        + " | ".join(
            f"{_pct(cfgs[c]['pairs'].get('dung'))} [{cfgs[c]['pairs'].get('n', 0)}]" for c in names
        )
        + " |"
    )
    md += ["", "### Đa bước và verify", ""]
    md += ["| Chỉ số | " + " | ".join(names) + " |", "| --- |" + " --- |" * len(names)]
    for m in DA_BUOC_METRICS + VERIFY_METRICS:
        if not any(m in cfgs[c]["metrics"] for c in names):
            continue
        md.append(
            f"| {LABELS.get(m, m)} | "
            + " | ".join(_cell(cfgs[c]["metrics"].get(m), m) for c in names)
            + " |"
        )
    for key, title in (
        ("by_type", "Theo loại câu hỏi"),
        ("by_tier", "Theo tier văn bản"),
        (
            "by_source",
            "Theo nguồn gốc câu test (`reviewed` = LLM viết, Claude rà đạt; `claude` = Claude sửa)",
        ),
    ):
        md += ["", f"## {title}", ""]
        for m in BREAKDOWN_METRICS:
            groups = sorted({g for c in names for g in cfgs[c].get(key, {})})
            if not any(m in cfgs[c].get(key, {}).get(g, {}) for c in names for g in groups):
                continue
            md += [f"**{LABELS.get(m, m)}**", ""]
            md += ["| Nhóm | " + " | ".join(names) + " |", "| --- |" + " --- |" * len(names)]
            for g in groups:
                md.append(
                    f"| {g} | "
                    + " | ".join(
                        _cell(cfgs[c].get(key, {}).get(g, {}).get(m), m, with_ci=False)
                        for c in names
                    )
                    + " |"
                )
            md.append("")
    comp = s.get("comparisons") or {}
    if comp:
        base = s.get("compare_to", "G")
        md += [
            "",
            f"## So sánh {base} với từng cấu hình (cùng tập câu đã xong)",
            "",
            "Hiệu = TB(" + base + ") − TB(cấu hình), kèm CI 95% bootstrap ghép cặp. Đúng/sai →"
            " McNemar chính xác 2 phía (b = " + base + " đúng/khác sai, c = ngược lại); liên tục →"
            " Wilcoxon hạng dấu (Pratt). p Holm hiệu chỉnh trong từng chỉ số.",
            "",
            "| Cấu hình | Chỉ số | n | "
            + base
            + " | khác | hiệu (CI) | kiểm định | p thô | p Holm |",
            "| --- | --- | ---: | ---: | ---: | --- | --- | ---: | ---: |",
        ]
        for c, ms in comp.items():
            for m, d in ms.items():
                sc = 1.0 if m == "judge_diem" else 100.0
                ci = d.get("diff_ci")
                cis = f" ({sc * ci[0]:.1f}…{sc * ci[1]:.1f})" if ci else ""
                extra = (
                    f"b={d['b']}, c={d['c']}"
                    if d["test"] == "mcnemar_exact"
                    else f"z={_num(d.get('z'), 2)}"
                )
                md.append(
                    f"| {c} | {LABELS.get(m, m)} | {d['n']} | {sc * d['mean_base']:.1f} |"
                    f" {sc * d['mean_other']:.1f} | {sc * d['diff']:+.1f}{cis} |"
                    f" {d['test']} ({extra}) |"
                    f" {_p(d['p'])} | {_p(d.get('p_holm'))} |"
                )
    var = s.get("variance") or {}
    if var.get("metrics"):
        md += [
            "",
            f"## Dao động ({var.get('config')} × {var.get('subset')}, seed {var.get('seeds')},"
            " không cache)",
            "",
            f"Tập câu chung {var.get('n_common')} · tỷ lệ câu trả lời giống hệt giữa các seed"
            f" {_pct(var.get('ty_le_cau_tra_loi_giong_het'))}%. Lưu ý: `temperature 0` (greedy) ⇒"
            " seed gần như không tác động; dao động đo được chủ yếu do batching không tất định của"
            " vLLM.",
            "",
            "| Chỉ số | " + " | ".join(f"seed {x}" for x in var["seeds"]) + " | độ lệch chuẩn |",
            "| --- |" + " ---: |" * (len(var["seeds"]) + 1),
        ]
        for m, d in var["metrics"].items():
            md.append(
                f"| {LABELS.get(m, m)} | "
                + " | ".join(_pct(d["per_seed"].get(x)) for x in var["seeds"])
                + f" | {_pct(d['std'])} |"
            )
    j = s.get("judge") or {}
    if j:
        md += [
            "",
            "## Judge",
            "",
            f"Model `{j.get('model_id')}` (họ `{j.get('family')}`), prompt hash"
            f" `{str(j.get('prompt_hash'))[:10]}`, tập `{j.get('subset')}`. Câu `ngoai_pham_vi`,"
            " câu trả lời `format_error` và câu bị từ chối dù có gold được chấm bằng luật (không"
            " gọi LLM).",
            "",
            "| Cấu hình | chấm LLM | chấm luật | format_error | error | dung ≠ (diem = 2) |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ]
        for c, d in (j.get("configs") or {}).items():
            md.append(
                f"| {c} | {d.get('llm', 0)} | {d.get('rule', 0)} | {d.get('format_error', 0)} |"
                f" {d.get('error', 0)} | {d.get('dung_khong_khop', 0)} |"
            )
    jc = s.get("judge_check") or {}
    if jc:
        md += ["", "## Kiểm định judge (Claude chấm độc lập, người dùng xác nhận)", ""]
        if jc.get("status") != "ok":
            md.append(f"Trạng thái: {jc.get('status')} — {jc.get('note', '')}")
        else:
            md += [
                "| Phần | n | khớp điểm 0/1/2 | κ (0/1/2) | khớp đúng/sai | κ (đúng/sai) |",
                "| --- | ---: | ---: | ---: | ---: | ---: |",
            ]
            for part, d in jc["parts"].items():
                md.append(
                    f"| {part} | {d['n']} | {_pct(d.get('agree'))} | {_num(d.get('kappa'))} |"
                    f" {_pct(d.get('agree_binary'))} | {_num(d.get('kappa_binary'))} |"
                )
            md += ["", jc.get("note", "")]
    if s.get("invalid"):
        md += ["", "## Câu test bị loại (lỗi validator)", ""]
        md += [f"- `{x['qid']}`: {', '.join(x['codes'])}" for x in s["invalid"]]
    return "\n".join(md) + "\n"


def status_counts(answers: Mapping[str, Any]) -> dict[str, int]:
    return dict(Counter(a.status for a in answers.values()))


ALL_METRICS = tuple(dict.fromkeys(MAIN_METRICS + DA_BUOC_METRICS + VERIFY_METRICS))


def config_summary(
    rows: Sequence[Mapping[str, Any]],
    pair_flags: Mapping[str, float],
    *,
    n_boot: int = 1000,
    seed: int = 42,
) -> dict[str, Any]:
    return {
        "metrics": describe(rows, ALL_METRICS, n_boot=n_boot, seed=seed),
        "by_type": breakdown(rows, "question_type", BREAKDOWN_METRICS),
        "by_tier": breakdown(rows, "tier", BREAKDOWN_METRICS),
        "by_source": breakdown(rows, "source_kind", BREAKDOWN_METRICS),
        "refusal": refusal_stats(rows),
        "pairs": pair_summary(pair_flags),
        "n_trich_rong": sum(
            1 for r in rows if r["metrics"].get("n_trich") == 0.0 and r["metrics"].get("ok") == 1.0
        ),
    }


__all__ = [
    "BREAKDOWN_METRICS",
    "COMPARE_METRICS",
    "DA_BUOC_METRICS",
    "LABELS",
    "MAIN_METRICS",
    "RETRIEVAL_METRICS",
    "VERIFY_METRICS",
    "breakdown",
    "compare",
    "describe",
    "metric_values",
    "pair_summary",
    "refusal_stats",
    "render_summary_md",
    "status_counts",
    "variance_summary",
]
