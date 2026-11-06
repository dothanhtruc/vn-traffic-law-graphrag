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
  registry/         # documents.yaml (33 văn bản), vbhn_map.yaml
  raw/              # văn bản gốc (Luat/, NghiDinh/, ThongTu/, QuyetDinh/, VBHopNhat/) — KHÔNG sửa, gitignored
  interim/          # <doc_id>.txt sau chuẩn hoá
  processed/        # units.jsonl (bản gốc), unit_versions.jsonl, amendment_todo.csv
  graph/            # nodes.jsonl, edges_struct.jsonl, edges_semantic.jsonl
  qa/               # train.jsonl, val.jsonl, test.jsonl (500 câu, viết tay), gold_extraction.jsonl
  index/            # faiss, bm25 + manifest.json (artifact build, không commit)
src/trafficlaw/
  registry/         # DocumentMeta (pydantic), load + validate
  ingest/           # readers (docx/pdf/html), normalize, structure, amendments
  graph/            # schema, references, extract, store (GraphStore, EmbeddedStore, Neo4jStore)
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

## 8. Schema đồ thị

| Nhãn nút | Thuộc tính chính |
| --- | --- |
| VanBan | `doc_id`, `so_hieu`, `loai`, `co_quan`, `tier`, `hieu_luc_tu`, `hieu_luc_den` |
| Chuong, Dieu, Khoan, Diem | `id`, `title` |
| PhienBan | `unit_id`, `version`, `text`, `effective_from`, `effective_to` |
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
- Mỗi bản ghi lưu: `run_id, git_commit, data_version, model_id, prompt_hash, timestamp, latency_ms, status` (`ok | error | format_error`). `data_version` = hash của `documents.yaml` + `unit_versions.jsonl`.
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
