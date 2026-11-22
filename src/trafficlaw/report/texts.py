"""Văn bản mẫu của báo cáo. **Không chữ số trần**: mọi số vào qua ``{chỗ giữ chỗ}`` (đã định dạng
bằng ``fmt``); chỉ cho phép định danh có chữ số (``B1``, ``M14``, ``r@5``, ``train_1000``).

``t(key, **vals)``: mọi giá trị phải là chuỗi (ép người gọi định dạng số trước).
Biến chung (``ci``, ``n_boot``, ``seed``) đặt bằng ``set_defaults`` từ file cấu hình.
"""

from __future__ import annotations

from typing import Any

_DEFAULTS: dict[str, str] = {}


def set_defaults(**vals: str) -> None:
    for k, v in vals.items():
        if not isinstance(v, str):
            raise TypeError(f"giá trị mặc định {k} phải là chuỗi")
    _DEFAULTS.update(vals)


def t(key: str, **vals: Any) -> str:
    for k, v in vals.items():
        if not isinstance(v, str):
            raise TypeError(f"t({key!r}): {k} phải là chuỗi đã định dạng, nhận {type(v).__name__}")
    return TEXT[key].format_map({**_DEFAULTS, **vals})


TEXT: dict[str, str] = {
    # ---------------------------------------------------------------- chung
    "title": "Báo cáo kết quả — hỏi đáp Luật Giao thông đường bộ bằng Graph RAG",
    "preamble": (
        "Báo cáo sinh tự động bằng `scripts.report` (run `{run_id}`) chỉ từ các file kết quả có"
        " sẵn — không chạy GPU, không gọi LLM. Mọi con số lấy từ file nguồn liệt kê ở chương"
        " *Nguồn số liệu* (đường dẫn + sha256; `sources.json` ghi thêm từng trường đã đọc). Số"
        " thập phân dùng dấu phẩy. Ô bảng dạng `giá trị (CI) [n]`: phần trăm hoặc trung bình, CI"
        " {ci}% bootstrap {n_boot} lần (seed {seed}) theo câu, n = số câu có giá trị."
    ),
    "toc": "Mục lục",
    "ok": "✓ khớp",
    "lech": "✗ lệch",
    "dat": "✓ đạt",
    "khong_dat": "✗ không đạt",
    "tong": "Tổng",
    "khong_tier": "không tier",
    "khong_co": "không có",
    "thieu": "**thiếu**",
    "model_goc": "model gốc",
    "best_mark": " (chọn)",
    "embedder": "Embedding",
    "reranker": "Reranker",
    "entity": "Thực thể",
    "relation": "Quan hệ",
    "seed": "seed {s}",
    "set_heading": "Tập `{name}`:",
    "missing_section": (
        "**Thiếu nguồn** `{source}` (`{path}`) — chương này không sinh được. Khôi phục file từ"
        " GitHub Release tương ứng (chương *Nguồn số liệu*) rồi chạy lại; báo cáo không tự điền."
    ),
    "schema_error": (
        "**Lỗi đọc nguồn** (`{error}`): file nguồn thiếu trường hoặc sai schema — chương này"
        " không sinh được; báo cáo không tự điền."
    ),
    # ---------------------------------------------------------------- tiêu đề chương
    "sec_overview": "Tổng quan và kiểm tra nhất quán",
    "sec_data": "Dữ liệu: danh mục, đọc và tách cấu trúc (M1–M3)",
    "sec_amend": "Áp sửa đổi và đối chiếu VBHN (M4)",
    "sec_graph": "Đồ thị tri thức (M5, M6, M8)",
    "sec_extract": "Trích xuất thực thể (M8)",
    "sec_qa": "Bộ dữ liệu hỏi–đáp (M9)",
    "sec_m10": "Chọn model embedding (M10, tập val)",
    "sec_m11": "Truy hồi trên val (M11, model gốc)",
    "sec_m12": "Sinh câu trả lời trên val (M12)",
    "sec_test": "Đánh giá cuối trên tập test (M13, M14)",
    "sec_variance": "Dao động theo seed và kiểm định judge (M13)",
    "sec_m14": "Fine-tune embedding và reranker (M14)",
    "sec_regression": "Regression",
    "sec_limitations": "Hạn chế",
    "sec_sources": "Nguồn số liệu",
    # ---------------------------------------------------------------- tổng quan
    "overview_intro": (
        "Run chính thức `{run_id}`: {n_test} câu test hợp lệ ({n_invalid} câu bị loại vì lỗi"
        " validator), test_sha256 `{test_sha}`, data_version `{data_version}`, commit"
        " `{commit}`. LLM sinh `{model}` = `{hf_repo}@{revision}` (vLLM {vllm}), cùng một model"
        " cho mọi cấu hình. Judge `{judge}` (họ `{judge_family}`, khác họ model sinh)."
    ),
    "config_table_intro": "Cấu hình (embedding/reranker theo kết quả val M14):",
    "checks_intro": (
        "Kiểm tra nhất quán (hash ghi trong kết quả so với file hiện có). Dòng *lệch* nghĩa là"
        " file đã đổi sau khi chạy đánh giá ⇒ số trong báo cáo có thể không khớp dữ liệu hiện tại."
    ),
    "chk_test": "test.jsonl = test của run",
    "chk_subsets": "subsets.json dựng từ test của run",
    "chk_train": "train_manifest dựng với test của run",
    "chk_dv": "data_version hiện tại = của run",
    "chk_graph_hash": "graph_data_hash của run = store_parity",
    "chk_nodes": "nodes.jsonl = graph_report",
    "chk_edges_struct": "edges_struct.jsonl = graph_report",
    "chk_edges_legal": "edges_legal.jsonl = graph_report",
    "chk_candidates": "ứng viên trích xuất = ứng viên được chấm",
    "chk_variance": "run dao động/judge cùng test",
    "chk_dev_dv": "run dev cùng data_version",
    "chk_baseline": "baseline regression G cùng đồ thị",
    # ---------------------------------------------------------------- M1–M3
    "data_intro": (
        "Danh mục có {n_docs} văn bản; {n_indexable} văn bản được chỉ mục độc lập, {n_amend} văn"
        " bản sửa đổi (nội dung đi vào phiên bản điều khoản). Đã đọc + chuẩn hoá {n_ingested}"
        " văn bản ({n_ok} trạng thái ok; reader: {readers}). Theo tier:"
    ),
    "struct_intro": (
        "Tách cấu trúc {n_docs} văn bản (gồm VBHN và văn bản sửa đổi); {n_anom} bất thường được"
        " ghi nhận (không tự sửa). Số unit theo cấp:"
    ),
    # ---------------------------------------------------------------- M4
    "amend_intro": (
        "Áp sửa đổi cho {n_targets} văn bản đích: {n_units} unit, {n_versions} phiên bản, {n_added}"
        " unit bổ sung. {n_todo} chỉ dẫn không áp tự động (ghi `amendment_todo.csv`, không đoán),"
        " theo lý do:"
    ),
    "vbhn_intro": (
        "Đối chiếu với VBHN tại ngày hợp nhất: khớp = bằng nhau sau chuẩn hoá mạnh (gồm"
        " `chi_khac_dinh_dang`); mẫu số bỏ Khoản có nguồn ngoài danh mục hoặc lỗi dữ liệu đã biết."
    ),
    # ---------------------------------------------------------------- M5/M6/M8
    "graph_intro": (
        "Đồ thị cấu trúc + pháp lý: {n_nodes} nút, {n_edges} cạnh, {n_dangling} cạnh treo. Span"
        " dẫn chiếu phân giải {ref_rate}% ({ref_rate_excl}% nếu bỏ span tới Phụ lục chưa có"
        " unit); {n_unresolved} span không phân giải; {n_uy_quyen} câu ủy quyền."
    ),
    "semantic_intro": (
        "Lớp ngữ nghĩa (M8, chỉ nạp khi đạt ngưỡng F1): {n_nodes} nút, {n_edges} cạnh ⇒ tổng đồ"
        " thị {total_nodes} nút, {total_edges} cạnh."
    ),
    "parity_intro": (
        "EmbeddedStore ↔ Neo4jStore (M6): {n_ok}/{n_checks} truy vấn khớp ({n_units} unit,"
        " {n_docs} văn bản × các mốc {dates})."
    ),
    # ---------------------------------------------------------------- M8
    "extract_intro": (
        "Chấm trên {n_reviewed} bản ghi tập vàng đã duyệt. LLM `{model}`: {n_items} item,"
        " {n_calls} lượt gọi, {tok_in} token vào / {tok_out} token ra. Con số pháp lý lấy bằng"
        " regex, không từ LLM."
    ),
    "rejected_intro": "Mục bị hậu kiểm loại (ghi `rejected.jsonl`):",
    # ---------------------------------------------------------------- M9
    "qa_intro": (
        "Tập test {n_items} câu, validator {n_errors} lỗi / {n_warnings} cảnh báo. Nguồn gốc:"
        " {n_human} câu người viết, {n_reviewed} câu LLM viết được Claude rà đạt (`+reviewed`),"
        " {n_claude} câu Claude sửa từ nháp (`+claude`; độ giống câu hỏi với nháp trung bình"
        " {q_sim}, đổi gold {gold_changed}%). Phân bổ loại câu × tier:"
    ),
    "fig_test_dist": "Phân bổ câu test theo loại câu và tier",
    "ax_n_questions": "Số câu",
    "train_intro": (
        "Train/val sinh bằng `{model}` từ {n_chunks} chunk: {n_raw} câu thô → {n_train} câu train"
        " ({n_dieu_train} Điều) + {n_val} câu val ({n_dieu_val} Điều, chia theo Điều);"
        " {n_rejected} câu bị lọc:"
    ),
    "subsets_intro": "Tập con của test (đơn vị lấy mẫu gồm cả cặp theo thời điểm):",
    # ---------------------------------------------------------------- M10
    "m10_intro": (
        "Chọn model trên val ({n} câu; không dùng test). Recall@5 lọc theo ngày áp dụng trước khi"
        " xếp hạng; cột cuối là tập con train_1000 (chỉ kiểm ổn định)."
    ),
    # ---------------------------------------------------------------- M11
    "m11_intro": (
        "Truy hồi trên câu sinh (không dùng test), model gốc. Liên kết@5 = độ phủ đơn vị liên kết"
        " qua đồ thị (Khoản chế tài, đích dẫn chiếu ở Điều khác) trong top-5."
    ),
    # ---------------------------------------------------------------- M12
    "m12_intro": (
        "Sinh câu trả lời trên val và câu ngoài phạm vi của dev (run `{run_id}`), trước khi có"
        " test."
    ),
    "tau_intro": (
        "Ngưỡng τ = {tau} (Youden J {j}) hiệu chỉnh trên điểm rerank top-1 của {config}: {n_val}"
        " câu val vs {n_oos} câu ngoài phạm vi dev."
    ),
    # ---------------------------------------------------------------- test
    "test_intro": (
        "Run `{run_id}`. So sánh {base} với từng cấu hình trên **cùng tập câu cả hai đã có giá"
        " trị**; đúng/sai → McNemar chính xác, liên tục → Wilcoxon (Pratt); Holm trong từng chỉ"
        " số. *Có ý nghĩa* = p Holm < {alpha}."
    ),
    "test_limits_intro": "Hạn chế ghi trong kết quả của run (nguyên văn `summary.json`):",
    "coverage_intro": "Độ phủ (`error` không tính là sai; `format_error` tính là sai):",
    "concl_intro": (
        "**Kết luận sinh từ kiểm định** (p Holm < {alpha}; chỉ số truy hồi và câu trả lời theo"
        " `configs/report.yaml`):"
    ),
    "concl_line": "- {base} vs {other} ({desc}) — *truy hồi*: {ret}. *Câu trả lời*: {ans}.",
    "seg_better": "{base} hơn có ý nghĩa ở {names}",
    "seg_worse": "{base} **kém** có ý nghĩa ở {names}",
    "seg_none": "không khác biệt có ý nghĩa ở {names}",
    "seg_all_none": "không khác biệt có ý nghĩa ở chỉ số nào",
    "seg_na": "không áp dụng",
    "ft_concl_retrieval_only": (
        "**Fine-tune (G vs A3, cùng hệ thống, chỉ khác embedding/reranker)**: cải thiện truy hồi"
        " có ý nghĩa ({ret}) nhưng **không** cải thiện có ý nghĩa chỉ số câu trả lời nào ({ans})"
        " ⇒ trên test, truy hồi tốt hơn chưa chuyển thành câu trả lời tốt hơn."
    ),
    "ft_concl_other": (
        "**Fine-tune (G vs A3, cùng hệ thống, chỉ khác embedding/reranker)** — truy hồi: {ret}."
        " Câu trả lời: {ans}."
    ),
    "ret_table_intro": "Truy hồi trên test (câu có gold; B0 không truy hồi):",
    "fig_test_retrieval": "Truy hồi trên test theo cấu hình (thanh lỗi: CI bootstrap)",
    "ax_pct": "%",
    "ans_table_intro": (
        "Câu trả lời trên test. Judge chỉ chấm tập con judge_200; B2/A1 sinh trên ablation_200 ⇒"
        " n khác nhau giữa cấu hình (so sánh dùng câu chung, bảng dưới)."
    ),
    "fig_test_answer": "Câu trả lời trên test theo cấu hình (thanh lỗi: CI bootstrap)",
    "extra_table_intro": "Đa bước, verify con số và hiệu lực trích dẫn:",
    "refusal_intro": (
        "Từ chối: precision tính cả câu gold rỗng (câu trước mốc của cặp theo thời điểm) là nên"
        " từ chối; recall trên câu ngoai_pham_vi; từ chối nhầm = câu có gold bị từ chối."
    ),
    "pairs_intro": "Cặp theo thời điểm đúng (hai câu đúng và hai câu trả lời khác nhau):",
    "compare_intro": (
        "So sánh chi tiết: hiệu = TB({base}) − TB(khác), kèm CI bootstrap ghép cặp; McNemar: b ="
        " {base} đúng/khác sai, c = ngược lại."
    ),
    "khong_y_nghia": "không có ý nghĩa",
    "g_hon": "G hơn",
    "g_kem": "G kém",
    "fig_forest": "Hiệu {base} − cấu hình khác trên test (CI bootstrap ghép cặp)",
    "ax_diff": "điểm %",
    "lg_sig": "p Holm < {alpha}",
    "lg_nonsig": "không có ý nghĩa",
    "by_type_intro": "Theo loại câu hỏi (không CI; n nhỏ ở nhiều nhóm):",
    "by_tier_intro": "Theo tier văn bản:",
    "by_source_intro": (
        "Theo nguồn gốc câu test (`reviewed` = LLM viết, Claude rà đạt; `claude` = Claude sửa):"
    ),
    "fig_by_type": "Recall@5 trên test theo loại câu",
    "judge_intro": (
        "Judge `{model}` (họ `{family}`) trên `{subset}`; câu ngoai_pham_vi, câu trả lời"
        " format_error và câu từ chối dù có gold chấm bằng luật (không gọi LLM):"
    ),
    # ---------------------------------------------------------------- dao động / judge
    "variance_intro": (
        "Từ run `{run_id}` (m14-test không đo lại): {config} × {subset}, sinh lại không cache"
        " với từng seed; tập câu chung {n}; câu trả lời giống hệt giữa các seed {same}%."
    ),
    "judge_check_intro": (
        "Kiểm định judge: Claude chấm độc lập theo cùng rubric, người dùng xác nhận; nhãn của câu"
        " trả lời đã đổi bị bỏ ({n_stale} câu)."
    ),
    "judge_check_missing": "Kiểm định judge chưa có (trạng thái `{status}`).",
    # ---------------------------------------------------------------- M14
    "hn_intro": (
        "Dữ liệu huấn luyện: {n_kept}/{n_total} câu train (loại câu có positive liên quan gold:"
        " {excluded}); {n_neg} hard negative (trung bình {mean_neg}/câu; {n_without} câu không có)."
    ),
    "emb_sel_intro": (
        "Embedding — val dense-only theo từng điểm đánh giá; bản chọn `{repo}@{commit}`:"
    ),
    "rr_sel_intro": ("Reranker — val rerank-only trên pool G cố định; bản chọn `{repo}@{commit}`:"),
    "fig_m14_steps": "Recall@5 trên val theo bước huấn luyện",
    "ax_r5": "Recall@5 (%)",
    "ax_step": "bước",
    "cost_intro": "Chi phí từng run (log huấn luyện):",
    "m14_val_intro": "Truy hồi đầy đủ trên val sau fine-tune (G/A1/A2 fine-tune, A3/B3 gốc):",
    "dev_intro": (
        "Tập dev đa bước/theo thời điểm (run `{run_id}`, {n} câu; dùng chọn cấu hình, không báo"
        " như kết quả chính):"
    ),
    # ---------------------------------------------------------------- regression
    "regression_body": (
        "CI chặn merge khi {bm25_metric} BM25 trên {bm25_n} câu `{bm25_split}` cố định giảm quá"
        " {max_drop} điểm % so với baseline {bm25_value}% (`tests/retrieval/test_regression.py`)."
        " Regression của {g_config} trên `{g_subset}` (baseline {g_value}%, {g_n} câu có gold) chạy"
        " **thủ công** bằng `scripts.eval regression` vì cần cache vector/rerank của model"
        " fine-tune (không commit) — người dùng chọn giữ thủ công ở M16."
    ),
    # ---------------------------------------------------------------- hạn chế
    "limits_intro": (
        "Trích **nguyên văn** từ CLAUDE.md và docs (danh sách trong `configs/report.yaml`; báo"
        " cáo không diễn giải thêm). Các con số trong đoạn trích là số đã ghi trong nguồn đó."
    ),
    "lim_khong_tim_thay": "**không tìm thấy đoạn trích trong nguồn** (nguồn đã đổi).",
    "lim_trung_lap": "**đoạn mở đầu xuất hiện nhiều lần trong nguồn** (phải làm rõ).",
    # ---------------------------------------------------------------- nguồn
    "sources_intro": (
        "Mọi file đã đọc để sinh báo cáo. `sources.json` có sha256 đầy đủ và danh sách trường đã"
        " đọc (cột *trường*). File **thiếu** → chương dùng nó ghi *thiếu nguồn*; khôi phục từ"
        " Release ghi ở cột cuối."
    ),
    # ---------------------------------------------------------------- tiêu đề cột
    "h_cfg": "Cấu hình",
    "h_desc": "Mô tả",
    "h_emb": "Embedding",
    "h_rerank": "Reranker",
    "h_check": "Kiểm tra",
    "h_expected": "Kỳ vọng",
    "h_actual": "Thực tế",
    "h_result": "Kết quả",
    "h_tier": "Tier",
    "h_n_docs": "Số văn bản",
    "h_level": "Cấp",
    "h_n_units": "Số unit",
    "h_reason": "Lý do",
    "h_n": "n",
    "h_vbhn": "VBHN",
    "h_base": "Văn bản gốc",
    "h_as_of": "Ngày",
    "h_match": "Khớp",
    "h_so": "Mẫu số",
    "h_rate": "Tỷ lệ (%)",
    "h_excluded": "Bị loại",
    "h_label": "Nhãn nút",
    "h_edge": "Loại cạnh",
    "h_unresolved": "Không phân giải",
    "h_part": "Phần",
    "h_ci": "CI F1",
    "h_threshold": "Ngưỡng",
    "h_type": "Loại câu",
    "h_subset": "Tập con",
    "h_system": "Hệ thống",
    "h_r1": "R@1",
    "h_r5_ci": "R@5 (CI)",
    "h_r20": "R@20",
    "h_mrr_ci": "MRR@10 (CI)",
    "h_r5_train": "R@5 train_1000",
    "h_model": "Model",
    "h_repo": "HF repo",
    "h_params": "Tham số (tỷ)",
    "h_vram": "VRAM đỉnh (GB)",
    "h_out_of_effect": "Top-5 ngoài hiệu lực",
    "h_link5": "Liên kết@5",
    "h_cite_gold": "Trích dẫn tới gold",
    "h_ctx_gold": "Ngữ cảnh chứa gold",
    "h_cite_valid": "Trích dẫn hợp lệ",
    "h_refuse": "Từ chối",
    "h_set": "Tập sinh",
    "h_n_refused": "Số câu từ chối",
    "h_refuse_wrong": "Từ chối nhầm câu có gold",
    "h_refuse_empty": "Từ chối câu gold rỗng",
    "h_pairs": "Cặp đúng [n cặp]",
    "h_other": "Khác",
    "h_diff": "Hiệu (CI)",
    "h_test": "Kiểm định",
    "h_p": "p thô",
    "h_p_holm": "p Holm",
    "h_verdict": "Kết luận",
    "h_group": "Nhóm",
    "h_judge_llm": "Chấm LLM",
    "h_judge_rule": "Chấm luật",
    "h_metric": "Chỉ số",
    "h_std": "Độ lệch chuẩn",
    "h_agree": "Khớp điểm",
    "h_agree_bin": "Khớp đúng/sai",
    "h_kappa_bin": "κ đúng/sai",
    "h_grid": "Mục lưới",
    "h_step": "Bước",
    "h_epoch": "Epoch",
    "h_kind": "Loại",
    "h_run": "Run",
    "h_steps": "Số bước",
    "h_gpu_hours": "Giờ GPU",
    "h_id": "id",
    "h_module": "Module",
    "h_path": "Đường dẫn",
    "h_fields": "Trường",
    "h_release": "Release",
}

__all__ = ["TEXT", "set_defaults", "t"]
