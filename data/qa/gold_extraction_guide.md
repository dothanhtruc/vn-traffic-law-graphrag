# Hướng dẫn gán nhãn tập vàng trích xuất (M8)

File cần sửa: `data/qa/gold_extraction.jsonl` (mỗi dòng là một Khoản, kèm các Điểm của nó, tại ngày `as_of`). Bản dễ đọc: `data/qa/gold_extraction_review.md` (sinh lại bằng `uv run python -m scripts.extraction_gold review`, **không sửa file .md**).

Bản nháp do model `llm:<model_id>` (Groq, khác model trích xuất) gán. Việc của người gán nhãn: sửa `entities` / `relations` cho đúng, rồi đặt `"reviewed": true` (có thể ghi `"reviewer"` và `"notes"`). **Không sửa** `draft` (bản sao nháp để đo tỷ lệ sửa), `units`, `text`, `gold_id`.

Sau khi sửa: `uv run python -m scripts.extraction_gold validate` phải không còn lỗi. `scripts.eval_extraction` chỉ chấm các bản ghi `reviewed: true`.

## Nguyên tắc chung

- Chỉ gán những gì **văn bản nói**, không suy luận thêm. Mỗi thực thể gắn với `unit_id` của Khoản/Điểm **nêu** nó.
- Con số (tiền, tháng, điểm) chép đúng như văn bản: `400.000 đồng` → `400000`; `02 điểm` → `2`.
- Không gộp đồng nghĩa: "xe gắn máy" ≠ "xe mô tô"; "xe ô tô" ≠ "xe chở người bốn bánh có gắn động cơ".
- Không chỉnh nhãn để khớp đầu ra của hệ thống. Không dùng tập vàng để sửa prompt theo từng mục.

## Thực thể (`entities`)

Mỗi mục: `{"id": "e1", "type": ..., "unit_id": "<mã unit>", ...}`; `id` không trùng trong bản ghi.

| type | Khi nào | Trường bắt buộc |
| --- | --- | --- |
| `HanhVi` | Hành vi (vi phạm, bị cấm, nghĩa vụ) do **chính unit mô tả** | `span` = đoạn **nguyên văn liên tục** của unit; `ten` = tên ngắn; `dieu_kien` nếu có |
| `CheTai` | Hình thức xử phạt nêu trong unit | `loai` ∈ `phat_tien`, `canh_cao`, `tuoc_quyen`, `tich_thu`, `dinh_chi`; `phat_tien`: `min_vnd`, `max_vnd`; `tuoc_quyen`/`dinh_chi`: `min_thang`, `max_thang`, `doi_tuong`; `tich_thu`: `doi_tuong` |
| `DiemGPLX` | "bị trừ điểm giấy phép lái xe NN điểm" | `so_diem` |
| `BienPhapBoSung` | Biện pháp khắc phục hậu quả "buộc …" | `ten` = cụm "buộc …" chép từ unit |
| `KhaiNiem` | Thuật ngữ được định nghĩa ("X là …", "X gồm …") | `ten` = thuật ngữ nguyên văn |
| `PhuongTien` | Loại xe mà unit áp dụng (kể cả qua tiêu đề Điều) | `catalog_id` trong `data/registry/extract_catalog.yaml` |
| `ChuThe` | Chủ thể bị điều chỉnh/chịu trách nhiệm | `catalog_id` trong danh mục |

Chi tiết:

1. **HanhVi**
   - Một Điểm nêu nhiều hành vi khác nhau (ngăn bởi ";" hoặc liệt kê) → **tách thành nhiều HanhVi**, mỗi cái một `span`. Ví dụ ND168 Đ6 K12: "lạng lách, đánh võng trên đường bộ" / "chạy quá tốc độ đuổi nhau trên đường bộ" / "dùng chân điều khiển vô lăng xe khi xe đang chạy trên đường bộ".
   - `span` bỏ nhãn ("a)", "1."), bỏ cụm ngoại lệ "trừ các hành vi vi phạm quy định tại …".
   - Unit chỉ **dẫn chiếu** hành vi ở chỗ khác ("Thực hiện hành vi quy định tại điểm … bị …") → **không** tạo HanhVi; chỉ tạo CheTai/DiemGPLX/BienPhapBoSung và quan hệ tới unit được dẫn chiếu.
   - Câu dẫn của Khoản ("Phạt tiền … đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:") không phải HanhVi.
   - Khi chấm, HanhVi khớp nếu cùng unit và token-F1 của `span` ≥ 0,5. Vì vậy chọn span **đủ ý**, không cần chính xác từng chữ ở hai đầu.
2. **CheTai**: mức phạt nêu ở câu dẫn Khoản gắn `unit_id` = Khoản. "Phạt cảnh cáo hoặc phạt tiền từ …" → hai CheTai.
3. **PhuongTien / ChuThe**: chọn mục **cụ thể nhất** có trong danh mục, đúng như chữ trong văn bản/tiêu đề Điều. Mục không có trong danh mục → ghi vào `notes`, không tự thêm id. Được chấm ở **cấp Khoản** (mỗi `catalog_id` tính một lần cho cả bản ghi, không xét gắn vào Khoản hay Điểm nào), nên chỉ cần gán mỗi loại một lần, ở unit nào cũng được.
4. **KhaiNiem**: chỉ thuật ngữ được định nghĩa trong chính unit; tên gọi tắt "(sau đây gọi là …)" không phải thực thể riêng.

## Quan hệ (`relations`)

Mỗi mục: `{"type": ..., "src": "unit:<mã unit>", "dst": "<id thực thể>"}`. `src` luôn là unit (có thể thuộc Khoản khác, khi được dẫn chiếu).

| type | src | dst |
| --- | --- | --- |
| `QUY_DINH_HANH_VI` | unit mô tả hành vi | HanhVi |
| `AP_DUNG_CHO` | unit | PhuongTien / ChuThe |
| `DINH_NGHIA` | unit định nghĩa | KhaiNiem |
| `BI_XU_PHAT` | **unit hành vi** bị xử phạt | CheTai / BienPhapBoSung |
| `BI_TRU_DIEM` | **unit hành vi** bị trừ điểm | DiemGPLX |

- Mức phạt ở câu dẫn Khoản → `BI_XU_PHAT` từ **mỗi Điểm hành vi** của Khoản đó (không từ chính Khoản).
- "Thực hiện hành vi quy định tại điểm h khoản 5; khoản 6 … bị trừ … 04 điểm" → `BI_TRU_DIEM` từ `unit:…/K5/h` và từ **từng Điểm** của khoản 6 (`unit:…/K6/a`, `unit:…/K6/b`, …); khoản không có Điểm → `unit:<mã Khoản>`.
- Khoản không có Điểm tự nêu cả hành vi lẫn mức phạt → `src` là chính Khoản.
- Quan hệ được gán ở bản ghi chứa **thực thể đích** (CheTai/DiemGPLX ở Khoản nào thì quan hệ tới nó nằm ở bản ghi Khoản đó).

## Ví dụ (ND168 Đ6 K16, rút gọn)

```json
"entities": [
  {"id": "e1", "type": "DiemGPLX", "unit_id": "ND168-2024/D6/K16/b", "so_diem": 4}
],
"relations": [
  {"type": "BI_TRU_DIEM", "src": "unit:ND168-2024/D6/K5/h", "dst": "e1"},
  {"type": "BI_TRU_DIEM", "src": "unit:ND168-2024/D6/K6/a", "dst": "e1"}
]
```

## Hạn chế cần nêu trong đồ án

Nhãn vàng được sửa từ bản nháp của LLM, nên có thể bị neo theo bản nháp. `scripts.extraction_gold diff` (và `eval_extraction`) báo tỷ lệ người sửa (thực thể thêm/xoá/đổi, quan hệ thêm/xoá) để định lượng hạn chế này.
