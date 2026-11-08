# CLAUDE.md — VN Traffic Law Graph RAG (DATN)

Hướng dẫn cho Claude Code khi làm việc trong repo này. Đọc hết file trước khi sửa code.

## 1. Dự án là gì

Hệ thống hỏi đáp **Luật Giao thông đường bộ Việt Nam** dựa trên **Graph RAG**: trả lời câu hỏi tiếng Việt, mỗi ý có trích dẫn tới Điều/Khoản/Điểm, có xét **hiệu lực điều khoản theo ngày áp dụng** (kể cả sau các lần sửa đổi).

- Dữ liệu: **33 văn bản** = 36 văn bản của bản tổng hợp Phase 2 (tra cứu 03/11/2026) bỏ Luật 26/2001, Luật 23/2008, NĐ 100/2019 (đã hết hiệu lực, không dùng). Danh mục chuẩn: `data/registry/documents.yaml`.
- Văn bản trục: Luật TTATGTĐB 36/2024/QH15, Luật Đường bộ 35/2024/QH15, NĐ 168/2024/NĐ-CP (xử phạt, trừ điểm GPLX). Nhiều văn bản trục đã bị sửa đổi trong 2025–2026 → nội dung điều khoản được lưu **theo phiên bản thời gian**.
- Mốc chốt dữ liệu: **03/11/2026**. Văn bản ban hành sau mốc chỉ nhập nếu sửa văn bản mức A.
- Đây là đồ án tốt nghiệp: **số liệu đánh giá phải tái lập được** là ưu tiên hàng đầu.
- Kế hoạch chia thành 18 module (M0–M17), xem mục 15. Mỗi phiên Claude Code chỉ làm **một** module.

## 2. Ràng buộc bắt buộc (không được vi phạm)

1. **GPU đơn, ưu tiên 16 GB VRAM** (Kaggle 1×T4/P100, RunPod RTX A4000). Không dùng DDP/multi-GPU, không viết code giả định > 16 GB. T4 không có bf16 → tự chọn `fp16` khi `torch.cuda.is_bf16_supported()` là False.
2. **Chỉ fine-tune embedding và reranker** trên GPU. Fine-tune LLM 3–4B (QLoRA) là thí nghiệm phụ (M17), nằm trong `experiments/`, pipeline chính không được import từ đó.
3. **LLM sinh câu trả lời = API miễn phí** (Gemini Flash/Flash-Lite → Groq → OpenRouter `:free`). Không dùng Gemini 1.x, 2.0 Flash-Lite (đã ngừng). Model chính được **chốt một `model_id`** trong `configs/llm.yaml`, dùng chung cho đánh giá và demo.
4. **Demo chi phí 0 đồng**: Hugging Face Space (Gradio, ZeroGPU), Neo4j AuraDB Free (≤ 200k nút / 400k quan hệ) hoặc đồ thị nhúng, chỉ mục FAISS build sẵn.
5. **Mọi job dài phải resume được** (parse hàng loạt, trích xuất LLM, training, đánh giá). Dừng giữa chừng không được mất kết quả đã có.
6. **Con số pháp lý (mức phạt, điểm trừ, thời hạn) không để LLM tự sinh**: lấy từ thuộc tính nút `CheTai`/`DiemGPLX` và kiểm tra lại sau khi sinh (`verify/`).
7. **Hiệu lực luôn tính theo phiên bản điều khoản**, không theo văn bản: một văn bản có thể còn hiệu lực trong khi vài Khoản của nó đã bị sửa, bãi bỏ hoặc có ngày hiệu lực riêng.

## 3. Kiến trúc

```
OFFLINE (chạy 1 lần)                          ONLINE (mỗi câu hỏi)
registry (documents.yaml)                      question (+ ngày áp dụng, mặc định hôm nay)
  → ingest: đọc, chuẩn hoá NFC                   → analyze: thực thể, loại xe, loại câu hỏi, ngày
  → structure: Phần/Chương/Mục/Điều/Khoản/Điểm   → hybrid retrieve: vector + BM25, RRF, top-20
  → amendments: áp sửa đổi → unit_versions       → graph expand: DAN_CHIEU, BI_XU_PHAT, BI_TRU_DIEM, HUONG_DAN (1–2 hop)
     (đối chiếu VBHN ≥ 95%)                       → rerank + lọc phiên bản theo as_of → top-5
  → references: dẫn chiếu (regex)                → LLM API (JSON: answer, citations, numbers)
  → extract: thực thể (LLM, mức A/B)             → verify: con số + trích dẫn
  → graph store + index (FAISS, BM25)            → UI Gradio
```

## 4. Cấu trúc thư mục

```
configs/            # YAML: paths, retrieval (B1..B3, G, A1..A3), llm, train_*, eval
data/
  registry/         # documents.yaml (33 văn bản), vbhn_map.yaml, label_overrides.yaml, amendment_overrides.yaml, doc_aliases.yaml (M5)
  raw/              # văn bản gốc (Luat/, NghiDinh/, ThongTu/, QuyetDinh/, VBHopNhat/) — KHÔNG sửa, gitignored
  interim/          # <doc_id>.txt sau chuẩn hoá
  processed/        # units.jsonl (bản gốc), unit_versions.jsonl, units_added.jsonl, amendment_todo.csv, vbhn_compare.jsonl
  graph/            # nodes.jsonl, edges_struct.jsonl, edges_legal.jsonl (M5), edges_semantic.jsonl (M8), unresolved.jsonl, graph_report.jsonl, graph_summary.md, review_sample.md
  qa/               # train.jsonl, val.jsonl, test.jsonl (500 câu, viết tay), gold_extraction.jsonl
  index/            # faiss, bm25 + manifest.json (artifact build, không commit)
src/trafficlaw/
  registry/         # DocumentMeta (pydantic), load + validate
  ingest/           # readers (docx/pdf/html), normalize, structure, amendments
  graph/            # schema, doc_names, references, build, pipeline (M5); extract, store (GraphStore, EmbeddedStore, Neo4jStore)
  retrieval/        # chunking, bm25, dense, analyze, hybrid, graph_expand, validity_filter, rerank
  llm/              # providers/, rate_limiter, cache, prompts/
  pipeline/         # answer.py: ghép các bước online
  verify/           # numbers.py, citations.py
  eval/             # metrics, runners, judge, stats
  train/            # hard_negatives, embedding, reranker
  utils/            # ids, dates, jsonl (append + resume), seed, logging
app/                # Gradio app cho HF Space (app.py, requirements.txt riêng)
experiments/        # M17: LLM QLoRA, notebook Kaggle
scripts/            # entrypoint CLI mỏng gọi vào src/
tests/              # pytest; tests/fixtures/ chứa trích đoạn văn bản thật, nhỏ
results/            # output đánh giá theo run_id
```

## 5. Lệnh thường dùng

Python 3.11, quản lý môi trường bằng `uv`.

```bash
uv sync
uv run ruff check . && uv run ruff format .
uv run pytest -q                                   # không cần GPU, không gọi API thật
uv run pytest -q -m "not slow and not gpu"

uv run python -m scripts.validate_registry         # M1: kiểm tra danh mục văn bản
uv run python -m scripts.ingest                    # M2–M3: raw → interim → units.jsonl
uv run python -m scripts.apply_amendments          # M4: units → unit_versions.jsonl
uv run python -m scripts.compare_vbhn              # M4: đối chiếu với VBHN, in tỷ lệ khớp
uv run python -m scripts.build_graph               # M5–M6, M8 (+ --load-neo4j, --extract)
uv run python -m scripts.eval_extraction           # M8: P/R/F1 trên gold_extraction.jsonl
uv run python -m scripts.build_index               # M10
uv run python -m scripts.train_embedding --config configs/train_embedding.yaml [--dry-run]
uv run python -m scripts.train_reranker  --config configs/train_reranker.yaml  [--dry-run]
uv run python -m scripts.eval retrieve --config configs/eval.yaml   # stage 1, không gọi API
uv run python -m scripts.eval generate --config configs/eval.yaml   # stage 2, gọi API, resume được
uv run python -m scripts.eval score    --config configs/eval.yaml   # stage 3
uv run python -m scripts.eval smoke [--fake]                        # 20 câu
uv run python -m scripts.report --run-id <run_id>                   # M16
uv run python app/app.py                                            # demo local
```

Nếu một script chưa tồn tại, tạo nó theo đúng tên trên thay vì đặt tên khác.

## 6. Danh mục văn bản và mức ưu tiên

`data/registry/documents.yaml`, mỗi mục là một `DocumentMeta`: `doc_id, so_hieu, loai, co_quan, ngay_ban_hanh, hieu_luc_tu, hieu_luc_den, tier, relations[], source_path, notes`.

| tier | Văn bản | Xử lý |
| --- | --- | --- |
| `A` | Luật 36/2024, Luật 35/2024, NĐ 168/2024, NĐ 151/2024, TT 38/2024, TT 53/2024, TT 65/2024, TT 79/2024, TT 12/2025-BCA, TT 14/2025-BXD, TT 36/2024-BYT + các văn bản sửa đổi của chúng | Cấu trúc + dẫn chiếu + trích xuất thực thể đầy đủ |
| `B` | NĐ 165/2024, NĐ 158/2024, NĐ 336/2025, NĐ 130/2024, TT 52/2024, TT 69/2024, TT 73/2024, TT 13/2025-BCA, QĐ 19/2024 + văn bản sửa đổi | Cấu trúc + dẫn chiếu; trích xuất chỉ điều có chế tài/định nghĩa |
| `C` | TT 71/2024, TT 72/2024, TT 83/2024 | Chỉ cấu trúc + chỉ mục |
| `historical` | TT 35/2024-BGTVT | Cấu trúc + THAY_THE, cho câu hỏi theo thời điểm |
| `vbhn` | 55/VBHN-VPQH, 144/2026/VBHN-LQ-VPQH, 65/2026/VBHN-NĐ-BXD | **Không đưa vào chỉ mục/đồ thị**; chỉ dùng để đối chiếu |

Văn bản sửa đổi (NĐ 184/2025, 236/2026, 238/2026, 241/2026, 218/2026, TT 13/2025, TT 17/2026) **không được chỉ mục như văn bản độc lập**: nội dung của chúng đi vào phiên bản mới của điều khoản bị sửa.

**Vấn đề dữ liệu đã biết** (validator phải báo, không tự sửa, không tự điền):
- **Không dùng** Luật 26/2001, Luật 23/2008, NĐ 100/2019 (đã hết hiệu lực; quyết định người dùng 05/11/2026): không có trong danh mục, không tạo quan hệ tới chúng; chỉ nhắc trong `notes` của văn bản thay thế/sửa đổi chúng.
- Bản chưa ghi số/ngày ký: TT 52/2024, TT 14/2025-BXD, VBHN 55. VBHN 65 có số/ngày nhưng điền bằng lớp chữ riêng, nên text không chứa nguyên chuỗi số hiệu. Với cả 4 văn bản, M2 chỉ báo warning khi không thấy số hiệu trong text.
- TT 13/2025-BCA sửa cả văn bản đường sắt, đường thủy → chỉ nhập phần sửa văn bản đường bộ.
- Đã giải quyết (05/11/2026): ngày của NĐ 218/2026, TT 71/72/73/2024, TT 12/2025-BCA điền theo văn bản gốc; 144/2026/VBHN-LQ-VPQH đã xác minh là VBHN Luật Đường bộ.
- Đã giải quyết (06/11/2026): VBHN 65/2026 ngày xác thực **27/08/2026** theo file gốc (số "65", ngày "27" tháng "8" điền vào mẫu; chữ ký số 28/08/2026), thay ngày quy ước 01/08/2026.

**Quy ước danh mục** (M1, `src/trafficlaw/registry/`):
- Ngày/số hiệu chỉ điền khi có căn cứ: văn bản ở `data/raw/`, hoặc bản tổng hợp `data/raw/TongHopThongTinDataset_Phase2.docx` (ghi "Nguồn: … Phase 2, mục N" trong `notes`). Không suy ngày từ văn bản khác (vd. không lấy ngày hết hiệu lực của luật cũ làm ngày hiệu lực của luật mới).
- `relations` đi **từ** văn bản chứa nó **tới** `target` (cấp văn bản; cấp Khoản/Điểm làm ở M5). Thay thế/bãi bỏ `toan_bo` từ ngày D ⇒ đích có `hieu_luc_den = D − 1` (validator kiểm tra).
- `is_amendment: true` = văn bản sửa đổi, mang tier của văn bản bị sửa, không chỉ mục độc lập. `DocumentMeta.indexable` loại VBHN và văn bản sửa đổi.
- `issues`: vấn đề máy không tự phát hiện được, validator in ra ở mức `info`. Mức `error` làm script thoát mã 1; `warning` (thiếu dữ liệu) chỉ chặn khi `--strict`.
- 144/2026/VBHN-LQ-VPQH đã mở file xác minh: là VBHN **Luật Đường bộ 35/2024**; VBHN 55 là Luật 36/2024.

**Quy ước đọc + chuẩn hoá** (M2, `src/trafficlaw/ingest/`, `configs/ingest.yaml`):
- Mọi văn bản có `source_path` (kể cả VBHN, văn bản sửa đổi) → `data/interim/<doc_id>.txt`: UTF-8, LF, NFC, kết thúc bằng `\n`. `scripts.ingest --stage normalize [--doc-id ID] [--force]`.
- Reader theo đuôi file: `.docx` → python-docx, duyệt `body` theo thứ tự (`w:p`/`w:tbl` xen kẽ), bảng mỗi hàng 1 dòng `ô | ô` (bỏ ô tiếp nối của gộp dọc), các đoạn trong một ô nối bằng dấu cách. `.doc` → `antiword -m UTF-8.txt -w 0` qua file tạm tên ASCII (antiword trên Windows lỗi với đường dẫn có dấu; CI cài `antiword` bằng apt); byte 0xC2 lẻ (NBSP bị antiword cắt) → dấu cách, ghi vào warnings. `.pdf` → PyMuPDF (không dùng pypdf: tách ký tự); trung bình < 50 ký tự/trang → `ScannedPdfError` (status `scanned`, không OCR).
- **Chú thích** (VBHN): tham chiếu trong thân → `[^N]` (docx: `w:footnoteReference`; PDF: chữ số superscript/cỡ nhỏ), nội dung → dòng riêng `[^N] …` đặt **ngay sau đoạn** chứa tham chiếu. M3 phải bỏ qua dòng `[^N]` và chấp nhận dạng `18.[^6]`, `c)[^3]`.
- Chỉ với PDF: bỏ dòng số trang (dòng đầu/cuối trang khớp số thứ tự trang ± độ lệch chung của văn bản) và dòng chữ ký số; nối dòng in bị ngắt, trừ trước `Điều N.`, `N.`, `a)`/`đ)`, tiêu đề Chương/Mục/Phần/Phụ lục (phần sau số thứ tự không có chữ thường), `[^N]`, gạch đầu dòng, dòng toàn chữ hoa; sau `.` không nối; sau `:`/`;` chỉ nối khi dòng sau bắt đầu bằng chữ thường.
- Không xoá U+FFFD hay ký tự symbol-font (Private Use); chỉ đếm vào manifest.
- Manifest `data/interim/manifest.jsonl` (append-only; bản ghi mới nhất của mỗi `doc_id` là hiện hành): `doc_id, source_path, source_sha256, output_path, reader, n_pages, n_chars, n_dieu_headings, has_dieu_1, n_replacement_chars, n_symbol_chars, single_char_ratio, so_hieu_found, so_hieu_required, warnings, status (ok|error|scanned), error, ingested_at, git_commit`. Resume theo `(doc_id, source_sha256)` của bản ghi `ok` + file interim còn tồn tại — khoá không chứa phiên bản code, nên **sửa reader/normalize thì chạy lại với `--force`**. Bảng tổng hợp: `data/interim/ingest_summary.md`.
- Script thoát mã 1 nếu có văn bản không `ok`, hoặc không thấy số hiệu trong text ở văn bản ngoài `so_hieu_unsigned` (TT 14/2025, TT 52/2024, VBHN 55, VBHN 65 — chỉ warning).
- `single_char_ratio` không tính nhãn Điểm ("điểm a, b") và "ô" (ô tô); ngưỡng cảnh báo 0,05.
- Ghi chú cho M3: `n_dieu_headings` đếm cả "Điều N." trong phụ lục/mẫu (TT 79/2024 có 6 tiêu đề "Điều 1–3." trong mẫu Quyết định); phần thân văn bản dừng ở "Nơi nhận" / phụ lục.
- `.docx`: đánh số tự động của Word (`w:numPr` gắn trực tiếp vào đoạn, `word/numbering.xml`) được in thành nhãn như Word hiển thị (`"1. "`, `"a) "`; lowerLetter là a…z, không có "đ"); bullet → không nhãn. Bổ sung ở M3 (TT38 có 40 Khoản/Điểm đánh số tự động, TT12 3, TT14 1). `.doc` (antiword) không áp dụng.

**Quy ước tách cấu trúc** (M3, `src/trafficlaw/ingest/structure.py`, `structure_pipeline.py`):
- `scripts.ingest --stage structure [--doc-id ID] [--force]`: mọi văn bản có manifest `ok` (kể cả VBHN, văn bản sửa đổi) → `data/processed/units.jsonl` + `structure_report.jsonl` (append-only, bản ghi mới nhất là hiện hành) + `structure_summary.md`. Resume theo `(doc_id, interim_sha256, overrides_sha256)` (sửa override của văn bản nào thì văn bản đó tự chạy lại); khoá không chứa phiên bản parser ⇒ **sửa parser thì chạy lại với `--force`**. Xử lý lại một văn bản thì xoá unit cũ của nó trước (không bao giờ trùng unit). Thoát mã 1 nếu lỗi, số Điều/Điều cuối lệch `expected_dieu` (`configs/ingest.yaml`), trích dẫn chưa đóng, hoặc có mục sửa nhãn không áp dụng được.
- Mỗi văn bản có unit `van_ban` (mã = `doc_id`, text = phần mở đầu/căn cứ). `text` giữ nguyên nhãn (`"Điều 9. …"`, `"1. …"`, `"a) …"`), chỉ phần riêng của unit; bỏ dòng trống. `title` chỉ có ở Điều/khung/Phụ lục, đã bỏ `[^N]`.
- Tiêu đề khung phải có số thứ tự (`Chương II`, `Mục 1. TÊN`, `Phần I`; La Mã → số Ả Rập); tên = các dòng chữ hoa liền sau (ND165 "PHẦN ĐẤT…" là tên Chương III, không phải cấp Phần). Khung, Điều, Khoản, Điểm đều kiểm tra thứ tự: Điều chặt (n+1, hoặc cùng số + chữ: 52 → 52a); Khoản/Điểm cho thiếu **đúng một** mục (lỗi đánh số trong bản gốc: TT12 Đ3 3→5, TT79 Đ34 n→p) → vẫn tạo unit + anomaly `*_gap`; trùng/lùi/nhảy xa → không tạo unit, ghép vào text unit đang mở + anomaly `*_out_of_sequence`. Mục đầu tiên có thể là mục bổ sung (`1a`, `a1`). Bảng chữ cái Điểm: a b c d đ e g h i k l m n o p q r s t u v x y.
- Trích dẫn (chỉ sau Điều đầu tiên): dòng bắt đầu bằng `“`/`"` mở khối; quét từng ký tự — `“` mở, `”` đóng, `"` đóng nếu đang mở, ngược lại mở (chịu được ngoặc gõ lẫn `“…"`, `"…”`); ngoặc cong mở giữa dòng chưa đóng cũng mở khối. Dòng trong khối thuộc text của unit đang mở, không tạo unit. Gặp `Nơi nhận`/câu thông qua khi ngoặc chưa đóng → đóng cưỡng bức + anomaly.
- Điểm dừng phần thân (sau Điều đầu tiên, ngoài trích dẫn, kể cả dòng bảng): `Nơi nhận`, `Luật này (đã) được Quốc hội…`, dòng chữ ký (`TM.`/`KT.`/`Q.`/`TL.`/CHỦ TỊCH/THỦ TƯỚNG/BỘ TRƯỞNG/VĂN PHÒNG QUỐC HỘI…), tiêu đề Phụ lục. Sau điểm dừng không nhận Điều/Khoản/Điểm.
- Phụ lục: dòng đúng dạng `PHỤ LỤC|Phụ lục [SỐ] [<La Mã>|<số>][[^N]]` (sau điểm dừng) mở 1 unit `phu_luc` nguyên văn tới Phụ lục kế tiếp; không số → đánh theo thứ tự xuất hiện; trùng số → `PL<n>-2`, `-3`. Dòng giữa điểm dừng và Phụ lục đầu tiên (chữ ký, Nơi nhận, biểu mẫu không có tiêu đề Phụ lục — TT79 373 dòng) bị bỏ, đếm ở `n_dropped_lines`.
- **Sửa nhãn thủ công** (`data/registry/label_overrides.yaml`, người dùng quyết định 07/11/2026): chỉ cho nhãn Khoản/Điểm ghi sai trong bản gốc, mỗi mục có `unit_id` đúng, `label_in_source`, `text_starts_with` (đầu câu sau nhãn), `reason`, `evidence` (căn cứ kiểm chứng được: dẫn chiếu trong văn bản, thứ tự chữ cái). Chỉ đổi số hiệu/mã unit; `text` giữ nguyên văn, unit có `label_in_source`. Áp trước khi kiểm tra thứ tự; mục không khớp đúng một dòng trong đúng Điều/Khoản cha → `overrides_unapplied`, script thoát mã 1. Hiện có 4 mục, đều thuộc ND168 (file `.doc` gốc ghi "đ)" thay "d)"): Đ16 K2 d (căn cứ: dẫn chiếu "điểm d/điểm đ khoản 2 Điều này" trong chính Điều 16), Đ39 K9 d, Đ40 K3 d và e (căn cứ: thứ tự chữ cái).
- Vấn đề dữ liệu đã biết (M3 báo, không sửa): ND151 không có dòng tiêu đề Phụ lục II (nội dung nằm trong PL1); TT69 Đ4 dòng "1. Yêu cầu" dính vào tiêu đề Điều (antiword) → Điểm a, b nằm thẳng dưới Điều, Khoản 2 là `khoan_gap`; VBHN55 phần cuối Đ89 (khoản 4–7) lỗi font trong PDF; VBHN65 chú thích `[^1]`/`[^2]` tràn vào phần mở đầu và Đ1 K7 (PDF); ND238 Đ8 K3 và ND241 Đ10 có trích dẫn thiếu ngoặc mở trong bản gốc (nội dung ghép vào Khoản chứa nó).

## 7. Đơn vị pháp lý và phiên bản

**Mã định danh** (ổn định, dùng làm khóa ở mọi nơi), tạo và parse trong `utils/ids.py`:

```
<MaVB>/D<dieu>/K<khoan>/<diem>     ví dụ: ND168-2024/D6/K4/a
MaVB: LUAT36-2024, LUAT35-2024, ND168-2024, ND238-2026, ND100-2019,
      TT38-2024-BGTVT, TT12-2025-BCA, TT14-2025-BXD, QD19-2024-TTG, VBHN55-VPQH ...
Khung (M3): <MaVB>[/P<phan>][/C<chuong>][/M<muc>]   ví dụ: TT35-2024-BGTVT/P2/C1, ND168-2024/C2/M1
Phụ lục:    <MaVB>/PL<n>[-k]                         ví dụ: TT53-2024-BGTVT/PL1, ND184-2025/PL1-2
```

- Chương đánh số lại trong mỗi Phần (TT35), Mục trong mỗi Chương ⇒ mã khung là đường dẫn đầy đủ; số La Mã đổi sang số Ả Rập. Mã Điều **không** chứa khung (`LUAT36-2024/D9`); `parent_id` của Điều = Chương/Mục sâu nhất chứa nó (hoặc văn bản), lưu trong unit, không suy ra từ mã (`utils.ids.parent_id` của Điều trả về văn bản).
- `units.jsonl` (bản gốc khi ban hành): `id, doc_id, level (van_ban|phan|chuong|muc|dieu|khoan|diem|phu_luc), number, title, text, parent_id, source_path, footnotes, line_start, label_in_source`. `footnotes: {N: nội dung}` = các chú thích VBHN có `[^N]` trong `text` của unit (dấu `[^N]` giữ trong text; dòng `[^N] …` không thuộc text của unit nào). `line_start` = dòng (1-based) trong `data/interim/<doc_id>.txt`. `label_in_source` = nhãn ghi trong bản gốc khi số hiệu đã sửa thủ công (null nếu không sửa).
- `unit_versions.jsonl`: `unit_id, version, text, effective_from, effective_to, status (active|amended|repealed), source_unit_id` — `source_unit_id` là điều khoản của văn bản gây ra phiên bản này (null với bản gốc).
- Hàm chuẩn: `get_version(unit_id, as_of) -> UnitVersion | None`. Mọi chỗ cần nội dung điều khoản đều đi qua hàm này.
- Hiệu lực đặc biệt phải biểu diễn ở cấp Khoản/Điểm: ví dụ theo khoản 2 Điều 53 NĐ 168/2024, điểm m khoản 3 Điều 6, điểm e khoản 4 Điều 26, điểm b khoản 1 Điều 27 có hiệu lực từ 01/01/2026; TT 35/2024 bị thay thế một phần bởi TT 12/2025-BCA (01/03/2025), phần còn lại bởi TT 14/2025-BXD (01/09/2025).
- Các mốc sửa đổi dùng trong test: 01/01/2025, 01/01/2026, 01/07/2026, 15/08/2026.
- Ngày dùng `datetime.date`, lưu ISO `YYYY-MM-DD`; `effective_to = null` nghĩa là còn hiệu lực.
- Khoảng hiệu lực `[effective_from, effective_to]` **bao gồm cả hai đầu**: phiên bản bị thay từ ngày D có `effective_to = D − 1`. `effective_from = null` (thiếu ngày) → không coi là có hiệu lực. Dùng `utils/dates.in_effect`, `day_before`.
- Cú pháp mã định danh (`utils/ids.py`): số Điều/Khoản `\d+[a-z]?` (Điều 6a bổ sung); Điểm `[a-zđ]\d*` (a, đ, a1, đ1); Điều không chia Khoản cho phép Điểm nằm thẳng dưới Điều (`LUAT36-2024/D3/b`).
- Job resume được: đọc `done_keys(path, key_fields)` rồi ghi bằng `JsonlWriter` (flush từng dòng). Khi mở lại file, dòng cuối bị cắt dở do crash được tự động cắt bỏ.
- Văn bản luôn chuẩn hoá Unicode **NFC** trước khi xử lý/so khớp.
- Chunk = 1 phiên bản Khoản (kèm các Điểm), tiền tố bằng tiêu đề Điều. Không cắt theo số token cố định.

**Áp sửa đổi** (`ingest/amendments.py`): nhận diện các mẫu "Sửa đổi, bổ sung khoản … Điều … như sau:", "Bổ sung điểm … vào khoản …", "Bãi bỏ …", "Thay thế cụm từ …". Mẫu không chắc chắn → ghi `amendment_todo.csv`, **không đoán**. Sau khi áp, `compare_vbhn` phải đạt ≥ 95% Khoản khớp với VBHN cho Luật 35, Luật 36, NĐ 165.

**Quy ước áp sửa đổi** (M4, `src/trafficlaw/ingest/`: `refs.py`, `amendments.py`, `effect.py`, `versioning.py`, `versions.py`, `vbhn.py`, `amendment_pipeline.py`):
- `scripts.apply_amendments [--doc-id ID] [--force]`: mỗi văn bản đích (`DocumentMeta.indexable`, gồm cả `historical`) → phiên bản của **mọi** unit (kể cả không bị sửa: `version=0`) trong `unit_versions.jsonl`, unit bổ sung trong `units_added.jsonl`, report `amendment_report.jsonl` (append-only) + `amendment_summary.md`; `amendment_todo.csv` (cột `doc_id, unit_id, source_unit_id, reason, detail`, UTF-8 BOM) sinh lại từ report mới nhất mỗi lần chạy. Resume theo `(doc_id, input_sha256)` = hash unit của đích + văn bản sửa nó + VBHN của nó + mục danh mục, `vbhn_map`, `amendment_overrides` liên quan; khoá không chứa phiên bản code ⇒ **sửa code M4 thì chạy lại với `--force`**. Xử lý lại một đích thì xoá bản ghi cũ của nó trước. Thoát mã 1 nếu đích lỗi hoặc mục sửa nhãn không áp được (todo không làm thất bại).
- **Unit bổ sung** (`units_added.jsonl`, người dùng chốt 08/11/2026): cùng schema `Unit` (`line_start = null`, `source_path` = file văn bản sửa đổi) + `after_id`/`before_id` (vị trí theo "vào sau/trước"; cả hai null → cuối) + `source_unit_id`. Module sau dựng cây bằng `units.jsonl` + `units_added.jsonl` (`vbhn.unit_tree`). Script kiểm tra mọi `unit_id` trong `unit_versions` có trong một trong hai file.
- **Văn bản đích của mỗi Điều sửa đổi**: số hiệu trong tiêu đề Điều khớp một đích `SUA_DOI`; không nêu số hiệu → đích duy nhất của văn bản; số hiệu ngoài danh mục → bỏ cả Điều, todo `ngoai_danh_muc` (ND184 Đ3–26, TT13 Đ1–5, 7, 8, 13).
- **Kế thừa ngữ cảnh**: câu dẫn của nhóm (unit có con là câu sửa đổi, không có khối nội dung) chỉ đặt ngữ cảnh: "…một số điểm, khoản của Điều 6" → Điều 6; "…một số điểm của khoản 5" → khoản 5; "Sửa đổi, bổ sung điểm a, điểm c và điểm e khoản 1" → khoản 1. Câu con lấy Điều/Khoản còn thiếu từ ngữ cảnh. Thân Điều có dòng câu sửa đổi riêng (TT13 Đ6) → tiêu đề Điều là ngữ cảnh.
- **Mẫu câu** (`amendments.parse_sentence`, theo thứ tự): cụm từ (`Thay thế cụm từ A bằng cụm từ B tại LOC` / `… A tại LOC bằng … B`; `Bỏ|Bãi bỏ cụm từ A tại LOC[, cụm từ B tại LOC2]`; `Bổ sung cụm từ A vào sau|trước cụm từ B tại LOC`) → Mẫu số (todo `mau_phu_luc`) → `Thay thế Phụ lục X … bằng Phụ lục Y kèm theo … này` / `Bổ sung Phụ lục X vào … bằng Phụ lục Y …` → `Bãi bỏ các điều, khoản, điểm, cụm từ sau của … số X: a; b; …` (tách theo `;`) → `Bãi bỏ REFS` → `Sửa đổi(, bổ sung) [tên] REFS` (dạng "một số … của Điều N" kèm toàn văn Điều N → thay cả Điều) → `Bổ sung REFS [vào (sau|trước) X]`. Câu khác, dẫn chiếu không đọc được (`refs.RefError`: "đoạn thứ hai", "Nghị định này" trong câu sửa văn bản khác) → todo `mau_khong_ro`.
- **Dẫn chiếu** (`refs.parse_refs`): đơn vị lớn đứng sau áp cho đơn vị nhỏ đứng trước ("điểm a khoản 1, khoản 3 Điều 6" → K1/a, K3 của Điều 6); `;` kết thúc một nhóm; mục thiếu Điều/Khoản lấy ngữ cảnh; "Nghị định số X" gán văn bản, phần mô tả sau bị bỏ; chữ lạ → `RefError`. M5 dùng lại hàm này.
- **Khối nội dung**: dòng sau câu dẫn (hoặc phần sau "như sau:" cùng dòng); bỏ ngoặc mở khối đầu dòng và ngoặc đóng khối cuối dòng, giữ ngoặc trong câu. Tách theo **nhãn của đích, đúng thứ tự** (đích khoản 2, 3 → khối bắt đầu `2.` rồi `3.`); không khớp → todo `nhan_khong_khop` (TT17 Đ2 K2, ND218 Đ8 K1: khối chỉ có Điểm, không có câu dẫn Khoản). Trong khối, Khoản/Điểm con tách bằng nhãn có kiểm tra thứ tự như M3.
- **Sửa nhãn trong khối nội dung** (`data/registry/amendment_overrides.yaml`, `label_fixes`): như `label_overrides` của M3 (đúng một dòng, có `reason` + `evidence`). Hiện có 1 mục (người dùng xác nhận 08/11/2026): ND241 Đ24 K1 ghi "d)" cho điểm đ (câu dẫn nêu "điểm đ", Điều 64 K1 ND165 đã có a–d, VBHN65 ghi đ).
- **Quy tắc phiên bản** (`versioning.build_versions`, hàm thuần): bản gốc `version=0` từ ngày hiệu lực riêng (unit hoặc tổ tiên gần nhất) hoặc `hieu_luc_tu`. Chỉ dẫn gom theo ngày D, áp theo (D, thứ tự trong văn bản sửa đổi); hết ngày D, unit đổi text/trạng thái → đóng bản cũ (`effective_to = D − 1`, `status = amended`), mở bản mới từ D (`source_unit_id` = thao tác cuối trong ngày); không đổi text → không có bản mới. Bãi bỏ → bản `repealed` (text rỗng) cho unit và mọi unit con. Thay cả Điều/Khoản: con chỉ có ở bản cũ → bãi bỏ, chỉ có ở bản mới → unit bổ sung. Bổ sung unit đã có và còn hiệu lực → todo `dich_da_ton_tai`. Cụm từ: tìm trong đích + cây con ("tên" → chỉ dòng đầu của đích), không phân biệt khoảng trắng và gạch nối `-–—`; không thấy thì thử không phân biệt hoa/thường; vẫn không thấy → todo `khong_tim_thay_cum_tu`, trừ khi đích đã được **chính văn bản sửa đổi đó** viết lại/bãi bỏ trước đó trong cùng ngày và cụm từ có ở bản trước (ghi `superseded` trong report, không phải lỗi; 19 chỉ dẫn, đều ND218 Đ38). `get_version` trả `None` cho unit bị bãi bỏ (`include_repealed=True` để lấy bản ghi `repealed`).
- **Hiệu lực riêng** (`effect.parse_effects`, Điều có tiêu đề chứa "hiệu lực"/"thi hành"): câu `<REFS> của <Luật|Nghị định|Thông tư> này có hiệu lực (thi hành) (kể) từ ngày D` kết thúc ngay sau ngày → áp cho REFS và cây con. Câu chung `… này có hiệu lực … từ ngày D[, trừ …| và thay thế …]` đối chiếu `hieu_luc_tu` (lệch → cảnh báo). Câu có mô tả phạm vi ("Quy định xử phạt … liên quan đến … tại …", "và theo quy định của pháp luật …", "theo quy định của pháp luật bảo vệ môi trường") → todo `hieu_luc_khong_ro`, không áp. Hiện áp: LUAT36 Đ10 K3 (01/01/2026); LUAT35 Đ42 K2 a,b, Đ43, Đ50, Đ84 K1 (01/10/2024); ND168 Đ6 K3 m, Đ26 K4 e, Đ27 K1 b (01/01/2026). Chỉ dẫn sửa Điều hiệu lực của đích → áp text, ghi todo `hieu_luc_sua_doi` (ngày riêng mới không tự áp). Câu hiệu lực có mô tả phạm vi mà người dùng duyệt → `effect_overrides` trong `amendment_overrides.yaml` (`unit_id` = Khoản hiệu lực, `source_unit_id` = chỉ dẫn đưa nó vào): dẫn chiếu + ngày đọc tự động từ câu (`effect.parse_accepted_clause`, lấy cụm sau chữ "tại" cuối cùng); phiên bản do văn bản sửa đổi đó tạo cho unit được dẫn chiếu (và cây con) bắt đầu từ ngày riêng, bản trước kéo dài tới ngày − 1 (`versioning.Delay`); phần điều kiện sau ngày ("và theo quy định của pháp luật …") → todo `hieu_luc_khong_ro`. Hiện có (người dùng duyệt 08/11/2026): ND238 Đ18 → ND168 Đ53 K3 (Đ20 K5 l, Đ21 K3 b, Đ32 K9a b từ 01/01/2028) và K4 (Đ20 K5 n, Đ26 K7 k, l từ 01/01/2029).
- **Bãi bỏ/thay thế toàn bộ** (`relations` `toan_bo`): mọi unit của đích → `repealed` từ ngày đó; TT35/2024 hết hiệu lực từ 01/09/2025 (TT14/2025). Thay thế một phần không ghi rõ điều khoản (TT12/2025 → TT35, 01/03/2025) → todo `thay_the_mot_phan`, **không biểu diễn ở cấp Khoản** (quyết định 07/11/2026).
- **Văn bản sửa đổi ngoài danh mục** (Luật 118/2025, Luật 24/2026/QH16, NĐ 243/2025; quyết định 07/11/2026): **bỏ qua, chỉ báo**. Unit bị chúng sửa (đọc từ chú thích VBHN) → todo `ngoai_danh_muc` với mã unit gốc; không tạo phiên bản từ text VBHN. Hệ quả đã chấp nhận: phiên bản Luật 35/36 từ 01/07/2026 (và Luật 35 từ 01/03/2027) **lỗi thời** ở các Khoản đó (Luật 36: 45 todo, Luật 35: 40 todo).
- Văn bản sửa chính văn bản sửa đổi (ND236 Đ16 K5 bãi bỏ K3–K4 Đ27 ND184) → todo `sua_van_ban_sua_doi`. Sửa Mẫu trong Phụ lục → `mau_phu_luc` (Mẫu không có unit riêng). ND158, ND165, TT14 không có unit Phụ lục (M3), TT17 không có Phụ lục trong file nguồn → thay/bổ sung Phụ lục → `khong_tim_thay_phu_luc`.

**Đối chiếu VBHN** (M4, `scripts.compare_vbhn`, `data/registry/vbhn_map.yaml`):
- `vbhn_map.yaml`: mỗi VBHN → `base_doc`, `as_of` (01/07/2026 cho cả 3), `out_of_registry_sources`, `known_issues` (mã unit VBHN lỗi dữ liệu M2/M3), `crosscheck_source`, `min_match_rate` (0,95). Mã ánh xạ thẳng `VBHN55-VPQH/D9/K18` ↔ `LUAT36-2024/D9/K18`.
- Đơn vị so = Khoản còn nội dung (Điều không chia Khoản → cả Điều), so **cây con** (Khoản + Điểm) của phiên bản tại `as_of`. **Khớp = bằng nhau sau chuẩn hoá mạnh** (người dùng chốt 08/11/2026): NFC, bỏ `[^N]` và nhãn, chữ thường, thống nhất kiểu bỏ dấu ("hoá"/"hóa", "thuỷ"/"thủy"), chỉ giữ chữ và số. Khớp chia `khop` (bằng nhau cả sau chuẩn hoá nhẹ) / `chi_khac_dinh_dang`; tỷ lệ `difflib` chỉ để chẩn đoán. Unit VBHN chỉ ghi "(được bãi bỏ)" = không có unit.
- Loại khỏi mẫu số: Khoản có chú thích nguồn ngoài danh mục (chú thích cấp Điều → mọi Khoản của Điều) → `loai_ngoai_danh_muc`; `known_issues` → `loai_loi_du_lieu`. Thiếu một bên (`thieu_vbhn`/`thieu_goc`) tính là lệch.
- Kiểm tra chéo (`crosscheck_source`, VBHN65 ↔ NĐ 241): mọi chú thích nguồn đó (trừ chú thích Mẫu, và Phụ lục khi văn bản gốc không có unit Phụ lục) phải có một phiên bản của unit hoặc unit con với `source_unit_id` thuộc văn bản nguồn và `effective_from` = ngày trong chú thích. Thoát mã 1 nếu tỷ lệ < ngưỡng hoặc kiểm tra chéo không đạt.
- Kết quả 08/11/2026: VBHN55↔LUAT36 396/397 (99,75%), VBHN144↔LUAT35 344/344 (100%), VBHN65↔ND165 293/308 (95,13%), chéo ND241 94/94 (bỏ 23 Mẫu/Phụ lục). 15 Khoản lệch của ND165 không do áp sửa đổi: lỗi chữ PDF của VBHN65 ("đau tư", "càn thiết", "mơ rộng"), lỗi chữ trong ND241 ("VNelD", "d" thay "đ"), VBHN tự biên tập ("Bộ Xây dựng, Bộ Xây dựng" gộp một; thay "Bộ Giao thông vận tải" ở chỗ ND241 không liệt kê; dính chữ ký).

## 8. Schema đồ thị

| Nhãn nút | Thuộc tính chính |
| --- | --- |
| VanBan | `doc_id`, `so_hieu`, `ten`, `loai`, `co_quan`, `tier`, `hieu_luc_tu`, `hieu_luc_den`, `is_amendment`, `indexable` |
| VanBanNgoai | `id` (`EXT:…`), `so_hieu`, `ten`, `loai`, `n_refs` — văn bản ngoài danh mục, không nội dung |
| Phan, Chuong, Muc, Dieu, Khoan, Diem, PhuLuc | `id`, `doc_id`, `level`, `number`, `title`, `uy_quyen` (nếu có), `bo_sung`/`source_unit_id` (unit bổ sung) |
| PhienBan | `unit_id`, `version`, `text`, `effective_from`, `effective_to`, `status`, `source_unit_id` |
| HanhVi, ChuThe, PhuongTien, KhaiNiem | `id`, `name`, `aliases` |
| CheTai | `min_vnd`, `max_vnd`, `loai` (phạt tiền, tước GPLX…) |
| DiemGPLX | `so_diem` |
| BienPhapBoSung | `name`, `thoi_han` |

Quan hệ: `THUOC, KE_TIEP, CO_PHIEN_BAN` (cấu trúc) · `SUA_DOI, THAY_THE, BAI_BO, HUONG_DAN, DAN_CHIEU, HOP_NHAT` (pháp lý, có `effective_from/to`, nối tới đúng Khoản/Điểm) · `QUY_DINH_HANH_VI, AP_DUNG_CHO, BI_XU_PHAT, BI_TRU_DIEM, DINH_NGHIA` (ngữ nghĩa, gắn vào PhienBan).

- Quan hệ cấu trúc, sửa đổi, dẫn chiếu: trích bằng **rule/regex**, không dùng LLM.
- Thực thể ngữ nghĩa: LLM trích theo JSON schema (pydantic), chỉ cho tier A (đầy đủ) và B (có chọn lọc); chỉ đưa vào đồ thị khi F1 thực thể ≥ 0,85, F1 quan hệ ≥ 0,80 trên `gold_extraction.jsonl`. Mức phạt/số điểm trích ra phải khớp regex trên văn bản gốc, lệch thì loại.
- "xe gắn máy" ≠ "xe mô tô": giữ đúng định nghĩa trong luật, không gộp đồng nghĩa tùy tiện.
- Mọi truy vấn lấy điều khoản phải nhận `as_of` và trả về phiên bản đúng ngày.
- Code đồ thị đi qua interface `GraphStore` với `EmbeddedStore` (NetworkX) và `Neo4jStore`; cùng truy vấn phải cho cùng kết quả. Test dùng `EmbeddedStore`.
- Cơ quan ban hành chỉ là thuộc tính; không suy luận quan hệ thay thế từ việc đổi bộ (GTVT → Xây dựng/Công an).

**Quy ước đồ thị** (M5, `src/trafficlaw/graph/`: `doc_names.py`, `references.py`, `build.py`, `pipeline.py`, `schema.py`; người dùng chốt 08/11/2026):
- `scripts.build_graph [--force]` → `data/graph/`: `nodes.jsonl` (`{id, label, props}`), `edges_struct.jsonl` + `edges_legal.jsonl` (`{type, src, dst, props}`), `unresolved.jsonl` (dẫn chiếu không phân giải: `reason` = `loi_doc` | `dich_khong_ton_tai` | `phu_luc_khong_co_unit` | `huong_dan_*`), `graph_report.jsonl` (append-only), `graph_summary.md`, `review_sample.md` (50 DAN_CHIEU phân tầng theo văn bản, seed 42, + toàn bộ HUONG_DAN để rà tay). Resume theo hash nội dung `units.jsonl`, `unit_versions.jsonl`, `units_added.jsonl`, `documents.yaml`, `doc_aliases.yaml` + hash file đầu ra; khoá không chứa phiên bản code ⇒ **sửa code M5 thì chạy lại với `--force`**. Đầu ra đã sắp xếp, tất định. Thoát mã 1 nếu có cạnh treo, phiên bản không có unit, hoặc vượt 200k nút / 400k cạnh. `--load-neo4j` (M6), `--extract` (M8) chưa có.
- **Mã nút**: VanBan = `doc_id` (unit `van_ban` gộp vào nút này); unit = `unit_id`; PhienBan = `<unit_id>@v<version>`; VanBanNgoai = `EXT:<số hiệu chuẩn hoá>` (`EXT:135/2021/NĐ-CP`) hoặc `EXT:<TEN-KHONG-DAU>` (`EXT:LUAT-XU-LY-VI-PHAM-HANH-CHINH`).
- **Nút**: mọi văn bản danh mục → VanBan (`is_amendment`, `indexable`); **văn bản sửa đổi và VBHN chỉ có nút VanBan** (không unit, không PhienBan, không vào chỉ mục). Unit của văn bản `indexable` + `units_added` → nút theo cấp (unit bổ sung có `bo_sung`, `source_unit_id`). Văn bản ngoài danh mục được nhắc → VanBanNgoai (không nội dung; cạnh tới nó chỉ ở cấp văn bản, cụm Điều/Khoản giữ trong `props.target_ref`). Văn bản **không dùng** (`excluded` trong `doc_aliases.yaml`: Luật 26/2001, Luật 23/2008, NĐ 100/2019, "Luật Giao thông đường bộ") được nhận diện (để dẫn chiếu trong cây con "Sửa đổi … NĐ 100/2019" không bị gán nhầm) nhưng **không để dấu vết**: không nút, không cạnh, không bộ đếm trong báo cáo (quyết định 08/11/2026); cụm tới chúng tính là đọc được.
- **THUOC** con → `parent_id` (không có → văn bản); **KE_TIEP** anh em liền nhau theo `versions.unit_tree` (gồm unit bổ sung theo `after_id`/`before_id`; hàm chuyển từ `vbhn.py`, vẫn import được từ đó); **CO_PHIEN_BAN** unit → PhienBan.
- **SUA_DOI / BAI_BO cấp unit**: mỗi phiên bản `version > 0` có `source_unit_id` → cạnh từ VanBan văn bản sửa đổi tới unit (`effective_from` = ngày phiên bản, `source_unit_id`, `version`, `thao_tac` = `sua_doi` | `bo_sung` | `bai_bo`; `repealed` → BAI_BO). Cha có phiên bản cùng `source_unit_id` + cùng ngày → bỏ cạnh của con (thay cả Khoản). Bãi bỏ/thay thế **toàn bộ** (`relations` `toan_bo`, TT14 → TT35) → chỉ cạnh cấp văn bản. Mọi `relations` của danh mục (SUA_DOI, BAI_BO, THAY_THE, HOP_NHAT) → cạnh cấp văn bản `props.cap = "van_ban"`.
- **DAN_CHIEU** đi từ **PhienBan** (text đổi theo phiên bản), `effective_from/to` của phiên bản nguồn, `pham_vi` = `noi_bo` | `van_ban_khac` | `ngoai`, `can_cu` (dòng "Căn cứ …" của phần mở đầu — **không** là HUONG_DAN), `span`. Dẫn chiếu tới chính unit nguồn ("khoản này") hoặc tổ tiên ("Điều này" trong một Khoản) **vẫn tạo cạnh**, có `props.quan_he = chinh_unit | to_tien` (cạnh khác không có thuộc tính này; quyết định 08/11/2026). Phiên bản `repealed` không có cạnh.
- **Tìm span** (`references.find_spans`): neo `điểm <nhãn>` / `khoản <số>` / `Điều <số>` / `Phụ lục <số>` / `Mẫu số N` (chỉ khi ngay sau là `Phụ lục <số>`) / `điểm|khoản|Điều này` — **bắt buộc có số/nhãn hoặc "này"** ("Điều khiển", "điểm kiểm tra", "trừ điểm giấy phép" không phải neo; "thời/địa/đặc… điểm này" bị loại). Mở rộng qua: neo liền sau (khoảng trắng: "điểm b khoản 5 Điều 6"); dấu nối `, ; và hoặc` / `đến|tới` + neo hoặc số/nhãn trần **cùng loại** (nhãn sau "điểm", số sau "khoản/Điều" — "và y tế" không bị nuốt); ngoặc đơn chứa dẫn chiếu ("Điều 13 (điểm a khoản 4; …)") hoặc ngoặc giải thích khi cụm còn tiếp sau ngoặc; từ nối `của|tại|thuộc|quy định tại|(ban hành) kèm theo` + neo/tên văn bản; tên văn bản kết thúc span. "Điều/khoản/điểm này" kết thúc span. Đọc span bằng `ingest.refs.parse_refs` (M4, không đổi) sau khi: thay "… này" bằng số của unit nguồn, khai triển khoảng ("khoản 1 đến khoản 3"), `;` → `,` (Điều cuối áp cho mọi nhóm), "Điều N (REFS)" → "REFS Điều N", bỏ ngoặc khác (gồm "(trừ …)"). Mẫu → Phụ lục chứa nó. Dẫn chiếu tới Chương/Mục (10 chỗ) chưa xử lý.
- **Ngữ cảnh**: mục thiếu Điều/Khoản lấy Điều/Khoản chứa unit nguồn (mã unit), chỉ khi span không nêu văn bản khác (nêu văn bản khác mà thiếu Điều → `loi_doc`). **Phạm vi văn bản** (`references.header_scope`): dòng bắt đầu "Sửa đổi|Bổ sung|Bãi bỏ|Thay thế … của|tại <văn bản khác>" → dẫn chiếu không nêu văn bản trong **cây con và chính unit đó** thuộc văn bản kia (ND168 Đ52 → NĐ 100/2019; LUAT35 Đ84 K3/K4 → luật được sửa); Điều 1 "… quy định chi tiết … <đúng một văn bản> … bao gồm:" → cây con thuộc văn bản được hướng dẫn (ND151 Đ1). Trong phạm vi văn bản khác, "Điều/khoản này" → `loi_doc`.
- **Bảng tên** (`doc_names.DocNameTable`, `data/registry/doc_aliases.yaml`): số hiệu so với `so_hieu` danh mục sau chuẩn hoá (chữ hoa, `ND`→`NĐ`); tên chỉ cho Luật/Bộ luật/Pháp lệnh (chữ đầu viết hoa): `ten` của Luật trong danh mục + `aliases` + `external_names`, khớp không phân biệt hoa/thường, **tên dài nhất thắng**; không có → cắt tự động tới dấu câu/từ chức năng (`ngày, năm, số, và, theo, …`). Số hiệu sau tên quyết định văn bản ("Luật Giao thông đường bộ số 23/2008/QH12"). "Luật sửa đổi, bổ sung một số điều của Luật X (và Luật Y)" → một VanBanNgoai riêng. Tên luật ngoài danh mục có dấu phẩy/"và"/"theo"/"điều" phải thêm vào `external_names` (nếu không sẽ bị cắt ngắn); nối dòng bị ngắt giữa tên (dòng sau viết thường).
- **HUONG_DAN** (chỉ nghị định/thông tư/quyết định `indexable`): dòng của unit `van_ban` hoặc Điều 1 có "quy định chi tiết" / "hướng dẫn thi hành|thực hiện", **không** bắt đầu bằng "Căn cứ", và trước cụm đó không nhắc văn bản khác (nếu có thì đó là trích yếu của văn bản được nhắc, vd ND158 Đ7 K8) → VanBan → văn bản được nhắc sau cụm (`cap = van_ban`) + unit cụ thể nếu nêu (`cap = unit`, "Điều 77 Luật …"); cộng danh sách dưới Điều 1 có phạm vi `huong_dan` (ND151 "1. Điều 6 về …"). `effective_from/to` = hiệu lực văn bản hướng dẫn. Câu ủy quyền trong Luật ("Chính phủ quy định chi tiết khoản 2 Điều này") **không** tạo HUONG_DAN → `props.uy_quyen = [{co_quan, source_unit_id}]` trên unit được dẫn chiếu.
- Kết quả 08/11/2026: 20.129 nút (VanBan 33, VanBanNgoai 137, Dieu 815, Khoan 3.328, Diem 4.873, PhuLuc 9, PhienBan 10.767), 31.771 cạnh (THUOC 9.192, KE_TIEP 6.991, CO_PHIEN_BAN 10.767, DAN_CHIEU 4.133 — gồm 4 `chinh_unit`, 43 `to_tien`, SUA_DOI 630, BAI_BO 43, HUONG_DAN 11, HOP_NHAT 3, THAY_THE 1), 0 cạnh treo, 52 `uy_quyen`; span phân giải 83,49%, **99,55% nếu bỏ span tới Phụ lục chưa có unit** (388 span — M3 chỉ tách Phụ lục có dòng tiêu đề đúng mẫu: ND158, ND165, TT12, TT14, TT35… thiếu); rà tay 50 DAN_CHIEU: 50/50 đúng (Claude rà, chờ người dùng xác nhận). Vấn đề đã biết: TT35 ghi số La Mã sai ("Phụ lục XXXXI") → 6 `loi_doc`; ND151 Đ38 K2 c (danh sách bãi bỏ của văn bản khác, không nêu văn bản trong câu) → 3 `dich_khong_ton_tai`.

## 9. Huấn luyện (GPU đơn 16 GB)

- Embedding gốc: `AITeamVN/Vietnamese_Embedding` (BGE-M3). Reranker gốc: `AITeamVN/Vietnamese_Reranker` hoặc `BAAI/bge-reranker-v2-m3`.
- Mặc định: `max_seq_length=512`, gradient checkpointing bật, `CachedMultipleNegativesRankingLoss` (mini-batch 16, batch hiệu dụng 128); reranker batch 8 + grad accumulation 4.
- Hard negatives tính trước bằng `train/hard_negatives.py` (Khoản "anh em" trên đồ thị + BM25 top-k sai), lưu file; không tính trong vòng train.
- Checkpoint mỗi 200 bước (model + optimizer + scheduler + RNG + step), đẩy lên HF Hub private; luôn thử `resume_from_checkpoint` khi khởi động.
- Có cờ `--dry-run` (20 bước, dữ liệu nhỏ, in VRAM đỉnh). Bắt CUDA OOM → giảm batch một nửa, ghi log, chạy tiếp.
- Ghi `torch.cuda.max_memory_allocated()`, giờ GPU, chi phí ước tính vào log mỗi run (W&B hoặc MLflow). Mục tiêu VRAM đỉnh ≤ 15 GB.
- Tham số qua YAML trong `configs/`, không hard-code.

## 10. Đánh giá — tái lập và chống gián đoạn

Ba giai đoạn độc lập: `retrieve` (không gọi API) → `generate` (API) → `score`.

- Output **JSONL append, flush sau từng câu**. Khóa: `(config_name, question_id, model_id, prompt_hash)`. Chạy lại thì bỏ qua bản ghi đã có. Dùng `utils/jsonl.py`.
- Mỗi bản ghi lưu: `run_id, git_commit, data_version, model_id, prompt_hash, timestamp, latency_ms, status` (`ok | error | format_error`). `data_version` = hash của `documents.yaml` + `unit_versions.jsonl` + `units_added.jsonl`.
- `error` (hết retry) **không tính là sai**; báo cáo luôn kèm độ phủ `n_done/n_total`, chỉ so cấu hình trên cùng tập câu đã xong. `format_error` tính là sai, thống kê riêng.
- Gọi LLM: `temperature=0`, trả JSON `{answer, citations[], numbers[]}`; parse lỗi → gọi lại 1 lần với lời nhắc sửa định dạng.
- Cache API theo `hash(model_id, prompt, params)` trong `llm/cache.py` (SQLite).
- Rate limiter token-bucket theo RPM/TPM từng provider (`configs/llm.yaml`); 429/5xx → backoff mũ có jitter, tối đa 5 lần; hết quota ngày → dừng sạch, in hướng dẫn chạy tiếp.
- Ngân sách lượt gọi ~3.800: sinh G/B3/B0 × 500; B1, B2, A1–A3 × 200 (tập con phân tầng); judge 5 cấu hình × 200; đo dao động 100 × 3.
- Chỉ số tất định (Recall@k, MRR@10, nDCG@10, độ phủ đa bước, độ đúng hiệu lực, khớp con số, citation P/R, từ chối đúng) tính offline. LLM judge chỉ cho độ đúng câu trả lời, trên tập con 200 câu, **khác provider với model sinh**.
- Báo cáo kết quả theo **loại câu hỏi** và theo **tier văn bản**.
- Thống kê: bootstrap 1.000 lần cho CI 95%; McNemar (đúng/sai), Wilcoxon (điểm liên tục).
- Cấu hình: B0 (không RAG), B1 (BM25), B2 (vector gốc), B3 (hybrid + rerank), G (Graph RAG đầy đủ), A1–A3 (G bỏ lần lượt: graph expand · lọc hiệu lực · embedding/reranker fine-tune), A4 phụ (LLM 3–4B fine-tune).

**Tập test** (`data/qa/test.jsonl`, 500 câu, viết tay):
- Phân bổ tier: A ~70%, B ~20%, C ~5%, historical ~5% (historical chỉ còn TT 35/2024-BGTVT; 5% dư chuyển sang B).
- Câu hỏi theo thời điểm bám 4 mốc ở mục 7; mỗi câu loại này có hai ngày hỏi (trước và sau mốc).
- Mỗi câu: `question, as_of, question_type, tier, answer, gold_units, required_numbers`. Validator kiểm tra mọi `gold_units` tồn tại và có phiên bản hiệu lực tại `as_of`.
- **Không bao giờ dùng để train, sinh dữ liệu, hay chỉnh prompt.** Kiểm tra trùng gần (cosine > 0,9) với train. Claude không sinh câu hỏi test — chỉ viết công cụ.

## 11. LLM providers

- Interface chung `LLMClient.generate(messages, *, json_schema=None) -> LLMResult` trong `llm/providers/`; có `FakeClient` cấu hình được chuỗi phản hồi (ok / 429 / 500 / quota_exhausted / JSON lỗi) cho test.
- Fallback khi demo: Gemini → Groq → OpenRouter `:free`. Trong đánh giá **không fallback**: một run chỉ dùng một `model_id`; lỗi thì ghi `error`.
- API key chỉ đọc từ biến môi trường (`GEMINI_API_KEY`, `GROQ_API_KEY`, `OPENROUTER_API_KEY`); `.env` trong `.gitignore`. Không bao giờ in key ra log.
- Prompt nằm trong `llm/prompts/*.md`, được hash để ghi vào kết quả. Sửa prompt = run mới.
- Job trích xuất (M8) và sinh dữ liệu (M9) phải in ước tính số lượt gọi trước khi chạy và chạy theo lô, resume được.

## 12. Demo (`app/`)

- Gradio trên HF Space ZeroGPU: chỉ encode câu hỏi/rerank nằm trong hàm `@spaces.GPU`; còn lại chạy CPU. Chạy local được khi không có package `spaces` (decorator no-op).
- UI: chat, trích dẫn bấm được để xem nguyên văn đúng phiên bản, bảng nguồn (điều khoản, điểm, trạng thái hiệu lực, văn bản sửa đổi nếu có), đồ thị con, ô "Áp dụng tại ngày", câu hỏi mẫu, nút đánh giá, ghi chú "dữ liệu cập nhật đến 03/11/2026", lưu ý "thông tin tham khảo, không thay thế tư vấn pháp lý", nhắc không nhập thông tin cá nhân.
- Hiển thị model đang trả lời; cache câu trả lời theo câu hỏi đã chuẩn hoá; báo người dùng khi sắp hết quota.
- `app/requirements.txt` tối giản (không torch training, không peft).

## 13. Kiểm thử

- Unit test bắt buộc: registry validator, parser cấu trúc (số Điều khớp điều cuối của từng văn bản; Điểm đ/đă; Điều không chia Khoản), áp sửa đổi, `get_version` ở 4 mốc ngày, `ids`, dẫn chiếu regex, lọc hiệu lực, chuẩn hoá thực thể, `jsonl` resume, metrics (so với giá trị tính tay), verify con số.
- Fixture lấy từ trích đoạn văn bản thật (ví dụ Luật 36/2024 Điều 9, NĐ 168/2024 Điều 6, TT 38/2024 Điều 7, một đoạn sửa đổi của NĐ 238/2026).
- Test không gọi mạng: LLM dùng `FakeClient`; đồ thị dùng `EmbeddedStore`.
- Đánh dấu `@pytest.mark.slow` (model thật, Neo4j thật, API thật) và `@pytest.mark.gpu` (cần CUDA).
- CI: ruff + pytest `-m "not slow and not gpu"` + `eval smoke --fake`.
- Regression: chặn merge nếu Recall@5 trên tập 100 câu cố định (chỉ truy hồi) giảm > 2 điểm %.

## 14. Phong cách code

- Type hints đầy đủ; dữ liệu giữa các module dùng `pydantic` model và file JSONL/YAML có schema — module sau đọc file đầu ra của module trước, không import nội bộ của nó.
- Hàm thuần, dễ test; I/O (file, API, Neo4j) đẩy ra rìa.
- Logging bằng `logging` (không `print` trong `src/`). Docstring/comment có thể tiếng Việt; tên biến/hàm tiếng Anh; nhãn đồ thị giữ tiếng Việt không dấu như mục 8.
- Seed cố định qua `utils/seed.py` ở đầu mọi script.
- Thay đổi nhỏ, có test đi kèm. Không thêm dependency khi chưa cần; nếu thêm, ghi lý do trong commit.

## 15. Module và cách làm việc

| Mã | Module | Phụ thuộc |
| --- | --- | --- |
| M0 | Khung repo, `utils/` | — |
| M1 | Danh mục văn bản + validator | M0 |
| M2 | Đọc, chuẩn hoá văn bản | M1 |
| M3 | Parser cấu trúc → `units.jsonl` | M2 |
| M4 | Áp sửa đổi → `unit_versions.jsonl`, đối chiếu VBHN | M3 |
| M5 | Dẫn chiếu, quan hệ cấu trúc | M4 |
| M6 | GraphStore (Embedded + Neo4j) | M5 |
| M7 | Lớp gọi LLM (providers, rate limit, cache, retry) | M0 |
| M8 | Trích xuất thực thể | M4, M6, M7 |
| M9 | Công cụ bộ dữ liệu hỏi–đáp | M4, M7 |
| M10 | Chỉ mục BM25 + vector | M4 |
| M11 | Truy hồi Graph RAG (`retrieve()`) | M6, M8, M10 |
| M12 | Sinh câu trả lời + verify (`pipeline/answer.py`) | M7, M11 |
| M13 | Bộ chạy đánh giá | M9, M11, M12 |
| M14 | Fine-tune embedding + reranker | M9, M10, M13 |
| M15 | Demo Gradio / HF Space | M6, M12, M14 |
| M16 | Báo cáo tự động + regression CI | M13 |
| M17 | (Phụ) Fine-tune LLM 3–4B | M13, M14 |

Quy trình mỗi module: một nhánh `mXX-<ten>` → plan (liệt kê file, interface, test) → viết test từ tiêu chí xong → code đến khi `pytest` và `ruff` sạch → chạy trên dữ liệu thật, ghi số liệu chính vào mô tả PR → commit. Không bắt đầu module khi module phụ thuộc chưa đạt tiêu chí xong. Thêm quy ước mới phát sinh vào file này.

Git/GitHub (repo public `vn-traffic-law-graphrag`):
- Push nhánh `mXX-<ten>` sau mỗi commit đã sạch `ruff` + `pytest` (sao lưu, CI chạy mỗi lần push).
- Chỉ merge vào `main` khi module đạt tiêu chí xong: PR `mXX-<ten>` → `main`, CI xanh, dùng **merge commit** (không squash). Module sau tách nhánh từ `main` mới nhất.
- Không commit tới thẳng `main`; không force-push nhánh đã có PR.
- Email commit dùng địa chỉ noreply của GitHub (repo public).

Logic pháp lý (regex sửa đổi, lọc hiệu lực, đối chiếu con số) phải được giải thích rõ trong PR để người dùng đọc lại — đây là chỗ sai khó phát hiện nhất.

## 16. Không được làm

- Không sửa file trong `data/raw/`; không sửa `data/qa/test.jsonl` trừ khi người dùng yêu cầu rõ.
- Không tự điền ngày hiệu lực, số hiệu hay nội dung văn bản còn thiếu — để null và báo.
- Không đưa VBHN hay văn bản sửa đổi vào chỉ mục như văn bản độc lập.
- Không để LLM tự điền con số pháp lý vào câu trả lời mà không qua `verify/`.
- Không thêm code yêu cầu > 16 GB VRAM hay nhiều GPU.
- Không dùng API trả phí hoặc model đã ngừng.
- Không commit artifact lớn (checkpoint, index, file > 50 MB) — dùng HF Hub.
- Không bịa số liệu đánh giá trong README/báo cáo: mọi con số phải sinh từ `results/<run_id>/`.
