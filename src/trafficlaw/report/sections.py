"""Các chương của báo cáo M16. Mỗi hàm đọc nguồn qua ``SourceStore`` và trả Markdown.

Quy tắc (kiểm bằng test): mọi con số hiển thị lấy từ nguồn và đi qua ``fmt``; chuỗi trong file này
và ``texts.py`` không có chữ số trần (chỉ định danh như ``B1``, ``M14``, ``r@5``).
"""

from __future__ import annotations

import hashlib
from collections import Counter
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from trafficlaw.eval.report import LABELS
from trafficlaw.registry.loader import parse_registry
from trafficlaw.report import limitations as lim
from trafficlaw.report.fmt import (
    DASH,
    short_hash,
    vn_ci_dec,
    vn_ci_pct,
    vn_dec,
    vn_int,
    vn_p,
    vn_pct,
    vn_signed_pct,
)
from trafficlaw.report.sources import MissingSourceError, SourceStore, plain
from trafficlaw.report.tables import md_table
from trafficlaw.report.texts import t

SCALE_DEC = ("judge_diem", "vp_truoc", "vp_sau", "cau_bo")
"""Chỉ số là trung bình (không phải tỷ lệ) — hiển thị số thập phân, không nhân phần trăm."""


@dataclass
class FigureSpec:
    name: str
    fn: str
    caption: str
    kwargs: dict[str, Any]


@dataclass
class Ctx:
    store: SourceStore
    cfg: Mapping[str, Any]
    figures: list[FigureSpec] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def figure(self, name: str, fn: str, caption: str, **kwargs: Any) -> str:
        self.figures.append(FigureSpec(name, fn, caption, kwargs))
        return f"![{caption}](figures/{name}.png)\n\n*{caption}*"

    @property
    def alpha(self) -> float:
        return float(self.cfg["alpha"])


@dataclass
class Section:
    id: str
    title: str
    body: str


# --------------------------------------------------------------------------- tiện ích


def label(m: str) -> str:
    return LABELS.get(m, m)


def val(d: Mapping[str, Any] | None, m: str, *, ci: bool = True, n: bool = True) -> str:
    """Ô một chỉ số của ``describe``: ``84,3 (81,4…87,3) [446]``."""
    if not d:
        return DASH
    dec = m in SCALE_DEC
    s = vn_dec(d["mean"], 2) if dec else vn_pct(d["mean"])
    if ci and d.get("ci"):
        s += f" ({vn_ci_dec(d['ci']) if dec else vn_ci_pct(d['ci'])})"
    if n:
        s += f" [{vn_int(d['n'])}]"
    return s


def diff_str(m: str, d: Mapping[str, Any]) -> str:
    if m in SCALE_DEC:
        sign = "+" if d["diff"] >= 0 else "−"
        return f"{sign}{vn_dec(abs(d['diff']), 2)} ({vn_ci_dec(d['diff_ci'])})"
    return f"{vn_signed_pct(d['diff'])} ({vn_ci_pct(d['diff_ci'])})"


def check_row(name: str, expected: Any, actual: Any) -> list[str]:
    ok = expected is not None and expected == actual
    return [name, short_hash(expected), short_hash(actual), t("ok") if ok else t("lech")]


def present_configs(cfg: Mapping[str, Any], configs: Mapping[str, Any]) -> list[str]:
    return [c for c in cfg["config_order"] if c in configs]


def _sum_counts(dicts: Sequence[Mapping[str, Any]]) -> Counter[str]:
    c: Counter[str] = Counter()
    for d in dicts:
        for k in d:
            c[str(k)] += int(d[k])
    return c


def current_data_version(st: SourceStore) -> str:
    """Như ``eval.qa_subsets.data_version`` (tên file + sha256), đọc qua ``SourceStore``."""
    h = hashlib.sha256()
    for sid in ("registry", "unit_versions", "units_added"):
        h.update(st.path(sid).name.encode())
        h.update(st.sha256(sid).encode())
    return h.hexdigest()


def vbhn_rates(statuses: Mapping[str, Counter[str]]) -> dict[str, tuple[int, int]]:
    """``vbhn → (khớp, mẫu số)``: mẫu số bỏ ``loai_*``; khớp = ``khop`` + ``chi_khac_dinh_dang``."""
    out = {}
    for v, c in statuses.items():
        so = sum(n for k, n in c.items() if not k.startswith("loai_"))
        out[v] = (c.get("khop", 0) + c.get("chi_khac_dinh_dang", 0), so)
    return out


# --------------------------------------------------------------------------- chương


def sec_overview(ctx: Ctx) -> str:
    st = ctx.store
    s = st.get("summary")
    g = s["configs"]["G"]
    serve = g["serve"]
    test_sha = st.sha256("test")
    parts = [
        t(
            "overview_intro",
            run_id=str(s["run_id"]),
            n_test=vn_int(s["n_test"]),
            n_invalid=vn_int(len(s["invalid"])),
            test_sha=short_hash(s["test_sha256"]),
            data_version=short_hash(s["data_version"]),
            commit=short_hash(s["git_commit"]),
            model=str(g["model_id"]),
            hf_repo=str(serve["hf_repo"]),
            revision=short_hash(serve["revision"], 7),
            vllm=str(serve["vllm_version"]),
            judge=str(s["judge"]["model_id"]),
            judge_family=str(s["judge"]["family"]),
        )
    ]
    m14 = st.get("retrieval_eval_m14")["configs"]
    rows = []
    for c in present_configs(ctx.cfg, s["configs"]):
        info = m14.get(c)
        emb = str(info["dense_key"]) if info else DASH
        rr = str(info["reranker_key"]) if info else DASH
        rows.append([c, str(ctx.cfg["configs"].get(c, "")), emb, rr])
    parts += [
        t("config_table_intro"),
        md_table([t("h_cfg"), t("h_desc"), t("h_emb"), t("h_rerank")], rows, "llll"),
    ]

    # Kiểm tra nhất quán giữa các file nguồn (hash).
    cur_dv = current_data_version(st)
    gr = st.last("graph")
    out_sha = gr["output_sha256"]
    checks = [
        check_row(t("chk_test"), s["test_sha256"], test_sha),
        check_row(t("chk_subsets"), s["test_sha256"], st.get("subsets")["test_sha256"]),
        check_row(t("chk_train"), s["test_sha256"], st.get("train_manifest")["test_sha256"]),
        check_row(t("chk_dv"), s["data_version"], cur_dv),
        check_row(t("chk_graph_hash"), s["graph_data_hash"], st.get("parity")["data_hash"]),
        check_row(t("chk_nodes"), out_sha["nodes.jsonl"], st.sha256("graph_nodes")),
        check_row(
            t("chk_edges_struct"), out_sha["edges_struct.jsonl"], st.sha256("graph_edges_struct")
        ),
        check_row(
            t("chk_edges_legal"), out_sha["edges_legal.jsonl"], st.sha256("graph_edges_legal")
        ),
        check_row(
            t("chk_candidates"),
            st.last("extraction")["candidates_sha256"],
            st.get("extraction_eval")["candidates_sha256"],
        ),
        check_row(t("chk_variance"), s["test_sha256"], st.get("variance_summary")["test_sha256"]),
        check_row(t("chk_dev_dv"), s["data_version"], st.get("dev_summary")["data_version"]),
        check_row(t("chk_baseline"), s["graph_data_hash"], st.get("baseline_g")["graph_data_hash"]),
    ]
    parts += [
        t("checks_intro"),
        md_table([t("h_check"), t("h_expected"), t("h_actual"), t("h_result")], checks, "llll"),
    ]
    return "\n\n".join(parts)


def sec_data(ctx: Ctx) -> str:
    st = ctx.store
    reg = parse_registry(plain(st.get("registry")))
    tiers = Counter(d.tier for d in reg)
    ingest = st.latest_by("ingest", "doc_id")
    status = Counter(str(r["status"]) for r in ingest.values())
    readers = Counter(str(r["reader"]) for r in ingest.values())
    struct = st.latest_by("structure", "doc_id")
    levels = _sum_counts([r["report"]["counts"] for r in struct.values()])
    n_anom = sum(len(r["report"]["anomalies"]) for r in struct.values())
    parts = [
        t(
            "data_intro",
            n_docs=vn_int(len(reg)),
            n_indexable=vn_int(len(reg.indexable())),
            n_amend=vn_int(sum(1 for d in reg if d.is_amendment)),
            n_ingested=vn_int(len(ingest)),
            n_ok=vn_int(status.get("ok", 0)),
            readers=", ".join(f"{k} {vn_int(v)}" for k, v in sorted(readers.items())),
        ),
        md_table(
            [t("h_tier"), t("h_n_docs")],
            [[str(k), vn_int(v)] for k, v in sorted(tiers.items(), key=lambda x: str(x[0]))],
        ),
        t("struct_intro", n_docs=vn_int(len(struct)), n_anom=vn_int(n_anom)),
        md_table(
            [t("h_level"), t("h_n_units")], [[k, vn_int(v)] for k, v in sorted(levels.items())]
        ),
    ]
    return "\n\n".join(parts)


def sec_amend(ctx: Ctx) -> str:
    st = ctx.store
    am = st.latest_by("amendment", "doc_id")
    todos: Counter[str] = Counter()
    for r in am.values():
        for x in r["todos"]:
            todos[str(x["reason"])] += 1
    parts = [
        t(
            "amend_intro",
            n_targets=vn_int(len(am)),
            n_units=vn_int(sum(int(r["n_units"]) for r in am.values())),
            n_versions=vn_int(sum(int(r["n_versions"]) for r in am.values())),
            n_added=vn_int(sum(int(r["n_added"]) for r in am.values())),
            n_todo=vn_int(sum(todos.values())),
        ),
        md_table([t("h_reason"), t("h_n")], [[k, vn_int(v)] for k, v in sorted(todos.items())]),
    ]
    vmap = {str(x["vbhn"]): x for x in st.get("vbhn_map")["vbhn"]}
    by: dict[str, Counter[str]] = {}
    for r in st.rows("vbhn"):
        by.setdefault(str(r["vbhn"]), Counter())[str(r["status"])] += 1
    rows = []
    rates = vbhn_rates(by)
    for v, c in sorted(by.items()):
        khop, so = rates[v]
        info = vmap.get(v)
        rows.append(
            [
                v,
                str(info["base_doc"]) if info else DASH,
                str(info["as_of"]) if info else DASH,
                vn_int(khop),
                vn_int(so),
                vn_pct(khop / so, 2) if so else DASH,
                vn_int(c.get("loai_ngoai_danh_muc", 0) + c.get("loai_loi_du_lieu", 0)),
            ]
        )
    parts += [
        t("vbhn_intro"),
        md_table(
            [
                t("h_vbhn"),
                t("h_base"),
                t("h_as_of"),
                t("h_match"),
                t("h_so"),
                t("h_rate"),
                t("h_excluded"),
            ],
            rows,
            "lllrrrr",
        ),
    ]
    return "\n\n".join(parts)


def sec_graph(ctx: Ctx) -> str:
    st = ctx.store
    gr = st.last("graph")
    ex = st.last("extraction")
    par = st.get("parity")
    parts = [
        t(
            "graph_intro",
            n_nodes=vn_int(gr["n_nodes"]),
            n_edges=vn_int(gr["n_edges"]),
            n_dangling=vn_int(gr["n_dangling"]),
            ref_rate=vn_pct(gr["ref_rate_total"], 2),
            ref_rate_excl=vn_pct(gr["ref_rate_excl_appendix"], 2),
            n_unresolved=vn_int(gr["n_unresolved"]),
            n_uy_quyen=vn_int(gr["n_uy_quyen"]),
        ),
        md_table(
            [t("h_label"), t("h_n")],
            [[k, vn_int(gr["nodes_by_label"][k])] for k in gr["nodes_by_label"]],
        ),
        md_table(
            [t("h_edge"), t("h_n")],
            [[k, vn_int(gr["edges_by_type"][k])] for k in gr["edges_by_type"]],
        ),
        md_table(
            [t("h_unresolved"), t("h_n")],
            [
                [k, vn_int(gr["unresolved_by_reason"][k])]
                for k in sorted(gr["unresolved_by_reason"])
            ],
        ),
        t(
            "semantic_intro",
            n_nodes=vn_int(sum(int(ex["nodes_by_label"][k]) for k in ex["nodes_by_label"])),
            n_edges=vn_int(sum(int(ex["edges_by_type"][k]) for k in ex["edges_by_type"])),
            total_nodes=vn_int(ex["graph_total"]["nodes"]),
            total_edges=vn_int(ex["graph_total"]["edges"]),
        ),
        md_table(
            [t("h_label"), t("h_n")],
            [[k, vn_int(ex["nodes_by_label"][k])] for k in sorted(ex["nodes_by_label"])],
        ),
        md_table(
            [t("h_edge"), t("h_n")],
            [[k, vn_int(ex["edges_by_type"][k])] for k in sorted(ex["edges_by_type"])],
        ),
        t(
            "parity_intro",
            n_ok=vn_int(par["n_ok"]),
            n_checks=vn_int(par["n_checks"]),
            n_units=vn_int(par["n_units"]),
            n_docs=vn_int(par["n_docs"]),
            dates=", ".join(str(x) for x in par["dates"]),
        ),
    ]
    return "\n\n".join(parts)


def sec_extract(ctx: Ctx) -> str:
    st = ctx.store
    ev = st.get("extraction_eval")
    gate = st.get("extract_cfg")["eval"]
    ex = st.last("extraction")
    ov = ev["overall"]
    ci = ev["ci95"]

    def prf(name: str, d: Mapping[str, Any], c: Any, thr: Any) -> list[str]:
        return [
            name,
            vn_dec(d["precision"], 3),
            vn_dec(d["recall"], 3),
            vn_dec(d["f1"], 3),
            vn_ci_dec(c, 3),
            vn_dec(thr, 2),
            t("dat") if d["f1"] >= thr else t("khong_dat"),
        ]

    usage = ex["llm"]["usage"]
    parts = [
        t(
            "extract_intro",
            n_reviewed=vn_int(ev["n_reviewed"]),
            model=str(ex["model_id"]),
            n_items=vn_int(ex["n_items"]),
            n_calls=vn_int(ex["llm"]["n_http_calls"]),
            tok_in=vn_int(usage["prompt_tokens"]),
            tok_out=vn_int(usage["completion_tokens"]),
        ),
        md_table(
            [t("h_part"), "P", "R", "F1", t("h_ci"), t("h_threshold"), t("h_result")],
            [
                prf(t("entity"), ov["entity"], ci["entity_f1"], gate["min_entity_f1"]),
                prf(t("relation"), ov["relation"], ci["relation_f1"], gate["min_relation_f1"]),
            ],
            "lrrrrrl",
        ),
    ]
    for kind in ("entity", "relation"):
        bt = ev["by_type"][kind]
        parts.append(
            md_table(
                [t(kind), "P", "R", "F1", "tp", "fp", "fn"],
                [
                    [
                        k,
                        vn_dec(bt[k]["precision"], 3),
                        vn_dec(bt[k]["recall"], 3),
                        vn_dec(bt[k]["f1"], 3),
                        vn_int(bt[k]["tp"]),
                        vn_int(bt[k]["fp"]),
                        vn_int(bt[k]["fn"]),
                    ]
                    for k in sorted(bt)
                ],
            )
        )
    rej = ex["rejections_by_reason"]
    parts += [
        t("rejected_intro"),
        md_table([t("h_reason"), t("h_n")], [[k, vn_int(rej[k])] for k in sorted(rej)]),
    ]
    return "\n\n".join(parts)


TIER_ORDER = ("A", "B", "C", "historical", "-")


def sec_qa(ctx: Ctx) -> str:
    st = ctx.store
    vt = st.get("validate_test")
    dist = vt["distribution"]
    txt = dist["tier_x_type"]
    types = sorted(dist["question_type"])
    cells: dict[tuple[str, str], int] = {}
    for k in txt:
        tier, qt = str(k).split("|", 1)
        cells[(qt, tier)] = int(txt[k])
    rows = []
    for qt in types:
        rows.append(
            [qt]
            + [vn_int(cells.get((qt, tr), 0)) for tr in TIER_ORDER]
            + [vn_int(dist["question_type"][qt])]
        )
    rows.append(
        [t("tong")]
        + [vn_int(sum(cells.get((q, tr), 0) for q in types)) for tr in TIER_ORDER]
        + [vn_int(dist["n"])]
    )
    de = vt["draft_edit_stats"]
    tm = st.get("train_manifest")
    sub = st.get("subsets")["subsets"]
    fig = ctx.figure(
        "test_distribution",
        "stacked_hbars",
        t("fig_test_dist"),
        categories=types,
        stacks=[
            {
                "label": tr if tr != "-" else t("khong_tier"),
                "values": [cells.get((qt, tr), 0) for qt in types],
            }
            for tr in TIER_ORDER
        ],
        xlabel=t("ax_n_questions"),
        title=t("fig_test_dist"),
    )
    rej = tm["rejected_by_reason"]
    parts = [
        t(
            "qa_intro",
            n_items=vn_int(vt["n_items"]),
            n_errors=vn_int(vt["n_errors"]),
            n_warnings=vn_int(vt["n_warnings"]),
            n_human=vn_int(de["n_human"]),
            n_reviewed=vn_int(de["n_reviewed_unedited"]),
            n_claude=vn_int(de["n_claude_edited"]),
            q_sim=vn_dec(de["question_similarity_mean"], 2),
            gold_changed=vn_pct(de["gold_changed"]),
        ),
        md_table(
            [t("h_type")]
            + [tr if tr != "-" else t("khong_tier") for tr in TIER_ORDER]
            + [t("tong")],
            rows,
        ),
        fig,
        t(
            "train_intro",
            model=str(tm["model_id"]),
            n_chunks=vn_int(tm["n_chunks_done"]),
            n_raw=vn_int(tm["n_questions_raw"]),
            n_train=vn_int(tm["n_train"]),
            n_val=vn_int(tm["n_val"]),
            n_dieu_train=vn_int(tm["n_dieu_train"]),
            n_dieu_val=vn_int(tm["n_dieu_val"]),
            n_rejected=vn_int(sum(int(rej[k]) for k in rej)),
        ),
        md_table([t("h_reason"), t("h_n")], [[k, vn_int(rej[k])] for k in sorted(rej)]),
        t("subsets_intro"),
        md_table(
            [t("h_subset"), t("h_n")], [[k, vn_int(len(sub[k]["qids"]))] for k in sorted(sub)]
        ),
    ]
    return "\n\n".join(parts)


def sec_m10(ctx: Ctx) -> str:
    ms = ctx.store.get("model_selection")
    val = ms["results"]["val"]
    tr = ms["results"]["train_1000"]
    rows = []
    for k in val:
        v = val[k]
        rows.append(
            [
                str(k),
                f"{vn_pct(v['recall@5'])} ({vn_ci_pct(v['recall@5_ci'])})",
                f"{vn_pct(v['mrr@10'])} ({vn_ci_pct(v['mrr@10_ci'])})",
                vn_pct(tr[k]["recall@5"]) if k in tr else DASH,
            ]
        )
    models = ms["models"]
    mrows = [
        [
            k,
            str(models[k]["hf_repo"]),
            vn_dec(models[k]["params_b"], 2),
            vn_dec(models[k]["peak_vram_gb"], 2),
        ]
        for k in models
    ]
    return "\n\n".join(
        [
            t("m10_intro", n=vn_int(val[next(iter(val))]["n"])),
            md_table([t("h_system"), t("h_r5_ci"), t("h_mrr_ci"), t("h_r5_train")], rows, "lrrr"),
            md_table([t("h_model"), t("h_repo"), t("h_params"), t("h_vram")], mrows, "llrr"),
        ]
    )


def _retrieval_rows(sets: Mapping[str, Any], name: str) -> list[list[str]]:
    rows = []
    for c in sets[name]:
        v = sets[name][c]
        lk = v.get("lien_ket@5")
        rows.append(
            [
                str(c),
                vn_int(v["n"]),
                vn_pct(v["recall@1"]),
                f"{vn_pct(v['recall@5'])} ({vn_ci_pct(v['recall@5_ci'])})",
                vn_pct(v["recall@20"]),
                f"{vn_pct(v['mrr@10'])} ({vn_ci_pct(v['mrr@10_ci'])})",
                vn_pct(v["top5_ngoai_hieu_luc"]) if "top5_ngoai_hieu_luc" in v else DASH,
                vn_pct(lk["do_phu"]) if lk else DASH,
            ]
        )
    return rows


RET_HEAD = ("h_cfg", "h_n", "h_r1", "h_r5_ci", "h_r20", "h_mrr_ci", "h_out_of_effect", "h_link5")


def sec_m11(ctx: Ctx) -> str:
    re_ = ctx.store.get("retrieval_eval")
    sets = re_["sets"]
    parts = [t("m11_intro")]
    for name in sets:
        parts += [
            t("set_heading", name=str(name)),
            md_table([t(h) for h in RET_HEAD], _retrieval_rows(sets, name)),
        ]
    return "\n\n".join(parts)


def sec_m12(ctx: Ctx) -> str:
    st = ctx.store
    de = st.get("answer_dev")
    tau = st.get("tau")
    parts = [t("m12_intro", run_id=str(de["run_id"]))]
    for name in de["sets"]:
        rows = []
        for c in de["sets"][name]:
            v = de["sets"][name][c]
            rows.append(
                [
                    str(c),
                    vn_int(v["n"]),
                    vn_pct(v.get("trich_gold")),
                    vn_pct(v.get("nguon_co_gold")),
                    vn_pct(v["trich_dan"].get("hop_le")),
                    vn_pct(v["tu_choi"]),
                ]
            )
        parts += [
            t("set_heading", name=str(name)),
            md_table(
                [
                    t("h_cfg"),
                    t("h_n"),
                    t("h_cite_gold"),
                    t("h_ctx_gold"),
                    t("h_cite_valid"),
                    t("h_refuse"),
                ],
                rows,
            ),
        ]
    parts.append(
        t(
            "tau_intro",
            tau=vn_dec(tau["tau"], 3),
            j=vn_dec(tau["youden_j"], 3),
            n_val=vn_int(tau["n_val"]),
            n_oos=vn_int(tau["n_dev_oos"]),
            config=str(tau["config"]),
        )
    )
    return "\n\n".join(parts)


TEST_RET_METRICS = ("r@1", "r@5", "r@10", "mrr@10", "ndcg@10")
TEST_ANS_METRICS = (
    "judge_dung",
    "judge_diem",
    "so_du",
    "trich_gold",
    "trich_r",
    "phien_ban_dung",
    "tu_choi_dung",
)
TEST_EXTRA_METRICS = (
    "db_top5",
    "db_ngu_canh",
    "db_du",
    "vp_truoc",
    "vp_sau",
    "cau_bo",
    "trich_bia",
    "hieu_luc_trich",
)


def _metric_table(cfgs: Mapping[str, Any], names: Sequence[str], metrics: Sequence[str]) -> str:
    present = [m for m in metrics if any(m in cfgs[c]["metrics"] for c in names)]
    rows = [[c] + [val(cfgs[c]["metrics"].get(m), m) for m in present] for c in names]
    return md_table([t("h_cfg")] + [label(m) for m in present], rows)


def _verdict(d: Mapping[str, Any], alpha: float) -> str:
    p = d.get("p_holm")
    if p is None:
        return DASH
    if p >= alpha:
        return t("khong_y_nghia")
    return t("g_hon") if d["diff"] > 0 else t("g_kem")


def sig_lists(
    comp: Mapping[str, Any], metrics: Sequence[str], alpha: float
) -> tuple[list[str], list[str], list[str]]:
    """(G hơn có ý nghĩa, G kém có ý nghĩa, không có ý nghĩa) — theo p Holm."""
    better, worse, none_ = [], [], []
    for m in metrics:
        if m not in comp:
            continue
        d = comp[m]
        if d["p_holm"] < alpha:
            (better if d["diff"] > 0 else worse).append(m)
        else:
            none_.append(m)
    return better, worse, none_


def _names(ms: Sequence[str]) -> str:
    return ", ".join(label(m) for m in ms) if ms else t("khong_co")


def _verdict_phrase(
    comp: Mapping[str, Any], metrics: Sequence[str], alpha: float, base: str
) -> str:
    b, w, n = sig_lists(comp, metrics, alpha)
    if not (b or w or n):
        return t("seg_na")
    if not (b or w):
        return t("seg_all_none")
    segs = []
    if b:
        segs.append(t("seg_better", base=base, names=_names(b)))
    if w:
        segs.append(t("seg_worse", base=base, names=_names(w)))
    if n:
        segs.append(t("seg_none", names=_names(n)))
    return "; ".join(segs)


def sec_test(ctx: Ctx) -> str:
    st = ctx.store
    s = st.get("summary")
    cfgs = s["configs"]
    names = present_configs(ctx.cfg, cfgs)
    comp = s["comparisons"]
    base = str(s["compare_to"])
    alpha = ctx.alpha
    parts = [t("test_intro", run_id=str(s["run_id"]), base=base, alpha=vn_dec(alpha, 2))]
    if s["limitations"]:
        parts += [t("test_limits_intro")] + ["\n".join(f"- {x}" for x in s["limitations"])]

    # Độ phủ
    cov = []
    for c in names:
        d = cfgs[c]
        stt = d["statuses"]
        cov.append(
            [
                c,
                str(d["set"]),
                f"{vn_int(d['n_done'])}/{vn_int(d['n_total'])}",
                vn_int(stt.get("ok", 0)),
                vn_int(stt.get("format_error", 0)),
                vn_int(stt.get("error", 0)),
            ]
        )
    parts += [
        t("coverage_intro"),
        md_table(
            [t("h_cfg"), t("h_set"), "n_done/n_total", "ok", "format_error", "error"], cov, "llrrrr"
        ),
    ]

    # Kết luận tự động: G so với từng cấu hình.
    ret_m = list(ctx.cfg["retrieval_metrics"])
    ans_m = list(ctx.cfg["answer_metrics"])
    concl = []
    for c in names:
        if c == base or c not in comp:
            continue
        concl.append(
            t(
                "concl_line",
                base=base,
                other=c,
                desc=str(ctx.cfg["configs"].get(c, "")),
                ret=_verdict_phrase(comp[c], ret_m, alpha, base),
                ans=_verdict_phrase(comp[c], ans_m, alpha, base),
            )
        )
    parts += [t("concl_intro", alpha=vn_dec(alpha, 2)), "\n".join(concl)]
    if "A3" in comp:
        b1, w1, _ = sig_lists(comp["A3"], ret_m, alpha)
        b2, w2, n2 = sig_lists(comp["A3"], ans_m, alpha)
        if b1 and not w1 and not b2 and not w2:
            parts.append(t("ft_concl_retrieval_only", ret=_names(b1), ans=_names(n2)))
        else:
            parts.append(
                t(
                    "ft_concl_other",
                    ret=_verdict_phrase(comp["A3"], ret_m, alpha, base),
                    ans=_verdict_phrase(comp["A3"], ans_m, alpha, base),
                )
            )

    # Bảng truy hồi + câu trả lời
    ret_cfgs = [c for c in names if "r@5" in cfgs[c]["metrics"]]
    parts += [t("ret_table_intro"), _metric_table(cfgs, ret_cfgs, TEST_RET_METRICS)]
    groups = ret_cfgs
    parts.append(
        ctx.figure(
            "test_retrieval",
            "grouped_bars",
            t("fig_test_retrieval"),
            groups=groups,
            series=[
                {
                    "label": label(m),
                    "values": [100 * float(cfgs[c]["metrics"][m]["mean"]) for c in groups],
                    "lo": [100 * float(cfgs[c]["metrics"][m]["ci"][0]) for c in groups],
                    "hi": [100 * float(cfgs[c]["metrics"][m]["ci"][1]) for c in groups],
                }
                for m in ("r@5", "mrr@10")
            ],
            ylabel=t("ax_pct"),
            title=t("fig_test_retrieval"),
        )
    )
    parts += [t("ans_table_intro"), _metric_table(cfgs, names, TEST_ANS_METRICS)]
    fig_m = ("judge_dung", "so_du")

    def _m(c: str, m: str, i: int | None) -> float | None:
        d = cfgs[c]["metrics"].get(m)
        if not d:
            return None
        return 100 * float(d["mean"] if i is None else d["ci"][i])

    parts.append(
        ctx.figure(
            "test_answer",
            "grouped_bars",
            t("fig_test_answer"),
            groups=names,
            series=[
                {
                    "label": label(m),
                    "values": [_m(c, m, None) for c in names],
                    "lo": [_m(c, m, 0) for c in names],
                    "hi": [_m(c, m, 1) for c in names],
                }
                for m in fig_m
            ],
            ylabel=t("ax_pct"),
            title=t("fig_test_answer"),
        )
    )
    parts += [t("extra_table_intro"), _metric_table(cfgs, names, TEST_EXTRA_METRICS)]

    # Từ chối
    ref = []
    for c in names:
        r = cfgs[c]["refusal"]
        ref.append(
            [
                c,
                vn_int(r["n_tu_choi"]),
                vn_pct(r["precision"]),
                vn_pct(r["recall"]),
                vn_pct(r["tu_choi_sai"]),
                vn_pct(r["tu_choi_gold_rong"]),
            ]
        )
    parts += [
        t("refusal_intro"),
        md_table(
            [
                t("h_cfg"),
                t("h_n_refused"),
                "precision",
                "recall",
                t("h_refuse_wrong"),
                t("h_refuse_empty"),
            ],
            ref,
        ),
    ]
    pr = [
        [c, f"{vn_pct(cfgs[c]['pairs']['dung'])} [{vn_int(cfgs[c]['pairs']['n'])}]"] for c in names
    ]
    parts += [t("pairs_intro"), md_table([t("h_cfg"), t("h_pairs")], pr)]

    # So sánh chi tiết
    parts.append(t("compare_intro", base=base))
    for m in ctx.cfg["compare_metrics"]:
        rows = []
        for c in names:
            if c not in comp or m not in comp[c]:
                continue
            d = comp[c][m]
            extra = (
                f"b={vn_int(d['b'])}, c={vn_int(d['c'])}"
                if d["test"] == "mcnemar_exact"
                else f"z={vn_dec(d['z'], 2)}"
            )
            mb = vn_dec(d["mean_base"], 2) if m in SCALE_DEC else vn_pct(d["mean_base"])
            mo = vn_dec(d["mean_other"], 2) if m in SCALE_DEC else vn_pct(d["mean_other"])
            rows.append(
                [
                    c,
                    vn_int(d["n"]),
                    mb,
                    mo,
                    diff_str(m, d),
                    f"{d['test']} ({extra})",
                    vn_p(d["p"]),
                    vn_p(d["p_holm"]),
                    _verdict(d, alpha),
                ]
            )
        if rows:
            parts += [
                f"**{label(m)}**",
                md_table(
                    [
                        t("h_cfg"),
                        t("h_n"),
                        base,
                        t("h_other"),
                        t("h_diff"),
                        t("h_test"),
                        t("h_p"),
                        t("h_p_holm"),
                        t("h_verdict"),
                    ],
                    rows,
                    "lrrrrlrrl",
                ),
            ]
    panels = []
    for m in ("r@5", "judge_dung", "so_du"):
        rws = []
        for c in names:
            if c in comp and m in comp[c]:
                d = comp[c][m]
                rws.append(
                    {
                        "label": c,
                        "diff": 100 * float(d["diff"]),
                        "lo": 100 * float(d["diff_ci"][0]),
                        "hi": 100 * float(d["diff_ci"][1]),
                        "sig": float(d["p_holm"]) < alpha,
                    }
                )
        if rws:
            panels.append({"title": label(m), "rows": rws})
    parts.append(
        ctx.figure(
            "test_diff_forest",
            "forest",
            t("fig_forest", base=base),
            panels=panels,
            title=t("fig_forest", base=base),
            xlabel=t("ax_diff", base=base),
            sig_label=t("lg_sig", alpha=vn_dec(alpha, 2)),
            nonsig_label=t("lg_nonsig"),
        )
    )

    # Theo loại câu / tier / nguồn câu
    bcfg = [c for c in ctx.cfg["breakdown_configs"] if c in cfgs]
    for key, title in (
        ("by_type", "by_type_intro"),
        ("by_tier", "by_tier_intro"),
        ("by_source", "by_source_intro"),
    ):
        parts.append(t(title))
        for m in ("r@5", "judge_dung", "so_du", "trich_gold"):
            groups_ = sorted({str(g) for c in bcfg for g in cfgs[c][key]})
            rows = []
            for g in groups_:
                cells = [
                    val(cfgs[c][key][g].get(m) if g in cfgs[c][key] else None, m, ci=False)
                    for c in bcfg
                ]
                if any(x != DASH for x in cells):
                    rows.append([g] + cells)
            if rows:
                parts += [f"**{label(m)}**", md_table([t("h_group")] + bcfg, rows)]
    types = sorted({str(g) for c in bcfg for g in cfgs[c]["by_type"]})
    types = [g for g in types if any("r@5" in cfgs[c]["by_type"].get(g, {}) for c in bcfg)]
    parts.append(
        ctx.figure(
            "test_r5_by_type",
            "hbars",
            t("fig_by_type"),
            categories=types,
            series=[
                {
                    "label": c,
                    "values": [
                        100 * float(cfgs[c]["by_type"][g]["r@5"]["mean"])
                        if g in cfgs[c]["by_type"] and "r@5" in cfgs[c]["by_type"][g]
                        else None
                        for g in types
                    ],
                }
                for c in bcfg
            ],
            xlabel=t("ax_pct"),
            title=t("fig_by_type"),
        )
    )

    # Judge
    j = s["judge"]
    jr = [
        [
            c,
            vn_int(j["configs"][c]["llm"]),
            vn_int(j["configs"][c]["rule"]),
            vn_int(j["configs"][c]["format_error"]),
            vn_int(j["configs"][c]["error"]),
        ]
        for c in names
        if c in j["configs"]
    ]
    parts += [
        t(
            "judge_intro",
            model=str(j["model_id"]),
            family=str(j["family"]),
            subset=str(j["subset"]),
        ),
        md_table([t("h_cfg"), t("h_judge_llm"), t("h_judge_rule"), "format_error", "error"], jr),
    ]
    return "\n\n".join(parts)


def sec_variance(ctx: Ctx) -> str:
    v = ctx.store.get("variance_summary")
    var = v["variance"]
    seeds = [str(x) for x in var["seeds"]]
    rows = []
    for m in var["metrics"]:
        d = var["metrics"][m]
        rows.append([label(m)] + [vn_pct(d["per_seed"][sd]) for sd in seeds] + [vn_pct(d["std"])])
    jc = v["judge_check"]
    parts = [
        t(
            "variance_intro",
            run_id=str(v["run_id"]),
            config=str(var["config"]),
            subset=str(var["subset"]),
            n=vn_int(var["n_common"]),
            same=vn_pct(var["ty_le_cau_tra_loi_giong_het"]),
        ),
        md_table([t("h_metric")] + [t("seed", s=sd) for sd in seeds] + [t("h_std")], rows),
    ]
    if jc["status"] == "ok":
        jrows = [
            [
                p,
                vn_int(jc["parts"][p]["n"]),
                vn_pct(jc["parts"][p]["agree"]),
                vn_dec(jc["parts"][p]["kappa"], 3),
                vn_pct(jc["parts"][p]["agree_binary"]),
                vn_dec(jc["parts"][p]["kappa_binary"], 3),
            ]
            for p in jc["parts"]
        ]
        parts += [
            t("judge_check_intro", n_stale=vn_int(jc["n_stale"])),
            md_table(
                [t("h_part"), t("h_n"), t("h_agree"), "κ", t("h_agree_bin"), t("h_kappa_bin")],
                jrows,
            ),
            str(jc["note"]),
        ]
    else:
        parts.append(t("judge_check_missing", status=str(jc["status"])))
    return "\n\n".join(parts)


def _selection_rows(sel: Mapping[str, Any]) -> list[list[str]]:
    base = sel["base"]
    rows = [
        [
            t("model_goc"),
            DASH,
            DASH,
            f"{vn_pct(base['recall@5'])} ({vn_ci_pct(base['recall@5_ci'])})",
            f"{vn_pct(base['mrr@10'])} ({vn_ci_pct(base['mrr@10_ci'])})",
        ]
    ]
    best = sel["best"]
    for r in sel["rows"]:
        is_best = r["run"] == best["run"] and r["step"] == best["step"]
        rows.append(
            [
                str(r["grid_id"]) + (t("best_mark") if is_best else ""),
                vn_int(r["step"]),
                vn_int(r["epoch"]),
                f"{vn_pct(r['metrics']['recall@5'])} ({vn_ci_pct(r['metrics']['recall@5_ci'])})",
                f"{vn_pct(r['metrics']['mrr@10'])} ({vn_ci_pct(r['metrics']['mrr@10_ci'])})",
            ]
        )
    return rows


def _cost_rows(sels: Mapping[str, Any]) -> list[list[str]]:
    rows = []
    for kind, sel in sels.items():
        seen = set()
        for r in sel["rows"]:
            run = str(r["run"])
            if run in seen:
                continue
            seen.add(run)
            e = r["end"]
            rows.append(
                [
                    kind,
                    run,
                    vn_int(e["steps"]),
                    vn_dec(e["gpu_hours"], 2),
                    vn_int(e["vnd"]),
                    vn_dec(e["peak_vram_gb"], 1),
                ]
            )
    return rows


def _step_series(sel: Mapping[str, Any]) -> list[dict[str, Any]]:
    by: dict[str, tuple[list[float], list[float]]] = {}
    for r in sel["rows"]:
        xs, ys = by.setdefault(str(r["grid_id"]), ([], []))
        xs.append(float(r["step"]))
        ys.append(100 * float(r["metrics"]["recall@5"]))
    return [{"label": k, "xs": v[0], "ys": v[1]} for k, v in sorted(by.items())]


def sec_m14(ctx: Ctx) -> str:
    st = ctx.store
    hn = st.get("hard_negatives")
    emb = st.get("emb_selection")
    rr = st.get("rerank_selection")
    r14 = st.get("retrieval_eval_m14")
    dev = st.get("dev_summary")
    stats = hn["stats"]
    exc = hn["filter"]["excluded_by_set"]
    parts = [
        t(
            "hn_intro",
            n_total=vn_int(hn["filter"]["n_total"]),
            n_kept=vn_int(hn["filter"]["n_kept"]),
            excluded=", ".join(f"{k} {vn_int(exc[k])}" for k in sorted(exc)),
            n_neg=vn_int(stats["n_negatives"]),
            mean_neg=vn_dec(stats["mean_negatives"], 2),
            n_without=vn_int(stats["n_without_negative"]),
        ),
        t(
            "emb_sel_intro",
            repo=str(emb["best"]["repo"]),
            commit=short_hash(emb["best"]["commit"], 7),
        ),
        md_table(
            [t("h_grid"), t("h_step"), t("h_epoch"), t("h_r5_ci"), t("h_mrr_ci")],
            _selection_rows(emb),
            "lrrrr",
        ),
        t("rr_sel_intro", repo=str(rr["best"]["repo"]), commit=short_hash(rr["best"]["commit"], 7)),
        md_table(
            [t("h_grid"), t("h_step"), t("h_epoch"), t("h_r5_ci"), t("h_mrr_ci")],
            _selection_rows(rr),
            "lrrrr",
        ),
        ctx.figure(
            "m14_val_steps",
            "step_lines",
            t("fig_m14_steps"),
            panels=[
                {
                    "title": t("embedder"),
                    "series": _step_series(emb),
                    "base": 100 * float(emb["base"]["recall@5"]),
                },
                {
                    "title": t("reranker"),
                    "series": _step_series(rr),
                    "base": 100 * float(rr["base"]["recall@5"]),
                },
            ],
            ylabel=t("ax_r5"),
            xlabel=t("ax_step"),
            base_label=t("model_goc"),
            title=t("fig_m14_steps"),
        ),
        t("cost_intro"),
        md_table(
            [t("h_kind"), t("h_run"), t("h_steps"), t("h_gpu_hours"), "VND", t("h_vram")],
            _cost_rows({t("embedder"): emb, t("reranker"): rr}),
            "llrrrr",
        ),
        t("m14_val_intro"),
    ]
    sets = r14["sets"]
    for name in sets:
        parts += [
            t("set_heading", name=str(name)),
            md_table([t(h) for h in RET_HEAD], _retrieval_rows(sets, name)),
        ]
    dcomp = dev["comparisons"]
    drows = []
    for c in dcomp:
        for m in dcomp[c]:
            d = dcomp[c][m]
            mb = vn_dec(d["mean_base"], 2) if m in SCALE_DEC else vn_pct(d["mean_base"])
            mo = vn_dec(d["mean_other"], 2) if m in SCALE_DEC else vn_pct(d["mean_other"])
            drows.append(
                [
                    str(c),
                    label(m),
                    vn_int(d["n"]),
                    mb,
                    mo,
                    diff_str(m, d),
                    vn_p(d["p"]),
                    vn_p(d["p_holm"]),
                ]
            )
    parts += [
        t("dev_intro", run_id=str(dev["run_id"]), n=vn_int(dev["n_test"])),
        md_table(
            [
                t("h_cfg"),
                t("h_metric"),
                t("h_n"),
                str(dev["compare_to"]),
                t("h_other"),
                t("h_diff"),
                t("h_p"),
                t("h_p_holm"),
            ],
            drows,
            "llrrrrrr",
        ),
    ]
    return "\n\n".join(parts)


def sec_regression(ctx: Ctx) -> str:
    st = ctx.store
    b = st.get("baseline_bm25")
    g = st.get("baseline_g")
    return t(
        "regression_body",
        bm25_metric=str(b["metric"]),
        bm25_value=vn_pct(b["value"]),
        bm25_n=vn_int(len(b["qids"])),
        bm25_split=str(b["split"]),
        max_drop=vn_pct(b["max_drop"]),
        g_config=str(g["config"]),
        g_subset=str(g["subset"]),
        g_value=vn_pct(g["recall@5"]),
        g_n=vn_int(g["n"]),
    )


def sec_limitations(ctx: Ctx) -> str:
    st = ctx.store
    specs = list(ctx.cfg["limitations"])
    texts: dict[str, str] = {}
    paths: dict[str, str] = {}
    for sp in specs:
        sid = str(sp["source"])
        if sid not in texts:
            try:
                texts[sid] = st.text(sid)
            except MissingSourceError:
                texts[sid] = ""
            paths[sid] = st.specs[sid].path
    parts = [t("limits_intro")]
    for li in lim.collect(specs, texts, paths):
        where = f"{li.source}:{li.line}" if li.line else li.source
        head = f"**{li.module} — {li.title}** (`{where}`)"
        if li.status != "ok":
            parts.append(head + " — " + t("lim_" + li.status))
            continue
        parts.append(head + "\n\n" + "\n".join(f"> - {x}" for x in li.items))
    return "\n\n".join(parts)


def sec_sources(ctx: Ctx) -> str:
    rows = []
    for r in ctx.store.manifest():
        if r["status"] == "missing":
            rows.append(
                [
                    r["id"],
                    r["module"],
                    f"`{r['path']}`",
                    t("thieu"),
                    DASH,
                    str(r["release"] or DASH),
                ]
            )
        else:
            rows.append(
                [
                    r["id"],
                    r["module"],
                    f"`{r['path']}`",
                    f"`{short_hash(r['sha256'])}`",
                    vn_int(len(r["fields"])),
                    str(r["release"] or DASH),
                ]
            )
    return "\n\n".join(
        [
            t("sources_intro"),
            md_table(
                [t("h_id"), t("h_module"), t("h_path"), "sha256", t("h_fields"), t("h_release")],
                rows,
                "llllrl",
            ),
        ]
    )


SECTIONS: tuple[tuple[str, str, Callable[[Ctx], str]], ...] = (
    ("tong_quan", "sec_overview", sec_overview),
    ("du_lieu", "sec_data", sec_data),
    ("sua_doi", "sec_amend", sec_amend),
    ("do_thi", "sec_graph", sec_graph),
    ("trich_xuat", "sec_extract", sec_extract),
    ("bo_qa", "sec_qa", sec_qa),
    ("chon_embedding", "sec_m10", sec_m10),
    ("truy_hoi_val", "sec_m11", sec_m11),
    ("sinh_val", "sec_m12", sec_m12),
    ("danh_gia_test", "sec_test", sec_test),
    ("dao_dong_judge", "sec_variance", sec_variance),
    ("fine_tune", "sec_m14", sec_m14),
    ("regression", "sec_regression", sec_regression),
    ("han_che", "sec_limitations", sec_limitations),
)
"""(id, khoá tiêu đề trong ``texts``, hàm). Chương "Nguồn số liệu" luôn ở cuối (sau khi đọc hết)."""


def build_sections(ctx: Ctx) -> list[Section]:
    out: list[Section] = []
    for sid, title_key, fn in SECTIONS:
        n_fig = len(ctx.figures)
        try:
            body = fn(ctx)
        except MissingSourceError as e:
            del ctx.figures[n_fig:]
            body = t("missing_section", source=e.source_id, path=e.path)
        except (KeyError, IndexError, TypeError) as e:
            # Nguồn có nhưng thiếu trường/sai schema: báo rõ, không tự điền.
            del ctx.figures[n_fig:]
            ctx.errors.append(f"{sid}: {type(e).__name__} {e}")
            body = t("schema_error", error=f"{type(e).__name__}: {e}")
        out.append(Section(sid, t(title_key), body))
    out.append(Section("nguon", t("sec_sources"), sec_sources(ctx)))
    return out


__all__ = ["SECTIONS", "Ctx", "FigureSpec", "Section", "build_sections", "sig_lists", "val"]
