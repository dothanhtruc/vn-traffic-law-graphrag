# Phiếu viết tập test (M9)

Phiếu này chỉ **gợi ý điều khoản** để bạn viết câu hỏi; công cụ không viết câu hỏi hay đáp án. Mỗi câu bạn viết là một dòng JSON trong `data/qa/test.jsonl` (mẫu dưới mỗi gợi ý đã điền sẵn `gold_units` và con số lấy bằng rule — sửa/bỏ tuỳ câu bạn viết). Kiểm tra bằng `uv run python -m scripts.qa_tool validate --split test`.

- Ngày áp dụng mặc định: 2026-11-03 (mốc chốt dữ liệu) · seed 42 · 3,389 chunk hiệu lực.
- Trường: `qid` (duy nhất, vd `t-0001`), `question`, `as_of`, `question_type`, `tier`, `answer`, `gold_units`, `required_numbers` (`{value, unit, unit_id?}`; unit ∈ vnd, diem, thang, ngay, nam, gio, km_h, km, m, tan, cho, phan_tram, mg, khac), `pair_id` (cặp theo_thoi_diem), `notes`. `source` mặc định `human`.
- Con số trong `required_numbers` phải có trong text phiên bản tại `as_of` hoặc là thuộc tính chế tài của đồ thị; validator báo lỗi nếu không.
- `theo_thoi_diem`: viết **hai** câu cùng `pair_id`, một ngày trước và một ngày sau mốc; đáp án phải khác nhau.
- `ngoai_pham_vi`: `gold_units` rỗng, `tier` null; câu hỏi nằm ngoài dữ liệu (lĩnh vực khác, văn bản không có trong danh mục, …) — hệ thống phải từ chối.

## Hạn mức

| Loại | Hạn mức | Mô tả | Số gợi ý |
| --- | ---: | --- | ---: |
| muc_phat | 80 | mức phạt tiền / phạt cảnh cáo cho một hành vi | 80 |
| tru_diem | 30 | số điểm bị trừ trên giấy phép lái xe | 30 |
| bien_phap | 35 | tước quyền sử dụng giấy phép, tịch thu, biện pháp khắc phục hậu quả | 35 |
| hanh_vi_cam_nghia_vu | 70 | hành vi bị cấm / nghĩa vụ, quy tắc phải tuân thủ | 70 |
| dinh_nghia | 40 | khái niệm, thuật ngữ được giải thích | 40 |
| thu_tuc_tham_quyen | 70 | thủ tục, hồ sơ, điều kiện, thẩm quyền, cơ quan có trách nhiệm | 70 |
| theo_thoi_diem | 50 | câu trả lời khác nhau trước/sau một mốc sửa đổi (đi theo cặp) | 25 |
| da_buoc | 60 | cần ≥ 2 điều khoản nối bằng dẫn chiếu / chế tài | 60 |
| so_sanh | 30 | so sánh giữa loại xe hoặc chủ thể | 22 |
| ngoai_pham_vi | 35 | ngoài phạm vi dữ liệu — hệ thống phải từ chối | 0 |

Tier (câu có tier; `ngoai_pham_vi` không tính): A ≈ 326, B ≈ 93, C ≈ 23, historical ≈ 23

Kho ứng viên theo loại × tier: muc_phat {'A': 191, 'B': 45}; tru_diem {'A': 72}; bien_phap {'A': 75, 'B': 20}; hanh_vi_cam_nghia_vu {'A': 1042, 'B': 315, 'C': 75, 'historical': 54}; dinh_nghia {'A': 104, 'B': 34}; thu_tuc_tham_quyen {'A': 897, 'B': 649, 'C': 113, 'historical': 178}; theo_thoi_diem {'2025-01-01': 2661, '2026-01-01': 2, '2026-07-01': 158, '2026-08-15': 43, 'khac': 543}; da_buoc {'A': 252, 'B': 195, 'C': 18, 'historical': 41}; so_sanh {'pairs': 81}

## muc_phat — mức phạt tiền / phạt cảnh cáo cho một hành vi

### W-muc_phat-001 · tier A · ND168-2024/D28/K3

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D28/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 28. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ
> 3. Phạt tiền từ 8.000.000 đồng đến 12.000.000 đồng đối với hành vi điều khiển xe hoạt động không đúng tuyến đường, lịch trình, thời gian được phép hoạt động hoặc phạm vi hoạt động theo quy định, trừ hành vi vi phạm quy định tại điểm b khoản 7 Điều 6 của Nghị định này.

- CheTai phat_tien: 8.000.000–12.000.000 đồng (nêu tại ND168-2024/D28/K3)
- DiemGPLX: trừ 6 điểm (nêu tại ND168-2024/D28/K4/b)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D28/K3"], "required_numbers": [{"value": 8000000, "unit": "vnd"}, {"value": 12000000, "unit": "vnd"}, {"value": 6, "unit": "diem"}]}
```

### W-muc_phat-002 · tier A · ND168-2024/D12/K8

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D12/K8#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 12. Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm khác về quy tắc giao thông đường bộ; sử dụng lòng đường, vỉa hè vào mục đích khác
> 8. Phạt tiền từ 2.000.000 đồng đến 4.000.000 đồng đối với cá nhân, từ 4.000.000 đồng đến 8.000.000 đồng đối với tổ chức cố ý thay đổi, xóa dấu vết hiện trường vụ tai nạn giao thông, trừ các hành vi vi phạm quy định tại điểm g khoản 4, khoản 8 Điều 6; điểm b khoản 5, điểm c khoản 9 Điều 7; điểm d khoản 5, điểm c khoản 8 Điều 8; điểm a khoản 4 Điều 9 của Nghị định này.

- CheTai phat_tien: 2.000.000–4.000.000 đồng (nêu tại ND168-2024/D12/K8)
- CheTai phat_tien: 4.000.000–8.000.000 đồng (nêu tại ND168-2024/D12/K8)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D12/K8"], "required_numbers": [{"value": 2000000, "unit": "vnd"}, {"value": 4000000, "unit": "vnd"}, {"value": 8000000, "unit": "vnd"}]}
```

### W-muc_phat-003 · tier A · ND168-2024/D37/K2

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D37/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 37. Xử phạt người điều khiển phương tiện giao thông cơ giới đường bộ gắn biển số nước ngoài
> 2. Phạt tiền từ 2.000.000 đồng đến 4.000.000 đồng đối với hành vi điều khiển xe tham gia giao thông tại Việt Nam không có văn bản chấp thuận hoặc cấp phép của cơ quan có thẩm quyền cấp theo quy định (đối với loại xe tham gia giao thông tại Việt Nam có quy định phải được chấp thuận hoặc cấp phép).

- BienPhapBoSung: buộc tái xuất phương tiện khỏi Việt Nam (nêu tại ND168-2024/D37/K7)
- CheTai phat_tien: 2.000.000–4.000.000 đồng (nêu tại ND168-2024/D37/K2)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D37/K2"], "required_numbers": [{"value": 2000000, "unit": "vnd"}, {"value": 4000000, "unit": "vnd"}]}
```

### W-muc_phat-004 · tier A · ND168-2024/D26/K11

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D26/K11#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
> 11. Phạt tiền từ 40.000.000 đồng đến 50.000.000 đồng đối với cá nhân, từ 80.000.000 đồng đến 100.000.000 đồng đối với tổ chức kinh doanh vận tải, dịch vụ hỗ trợ vận tải tái phạm hành vi quy định tại điểm a, điểm h, điểm l khoản 7 Điều này.

- BienPhapBoSung: buộc cung cấp, cập nhật, truyền dẫn, lưu trữ, quản lý thông tin, dữ liệu thu thập từ thiết bị giám sát hành trình, thiết bị ghi nhận hình ảnh người lái xe, thiết bị ghi nhận hình ảnh khoang chở khách lắp trên xe ô tô theo quy định (nêu tại ND168-2024/D26/K13/d)
- CheTai phat_tien: 40.000.000–50.000.000 đồng (nêu tại ND168-2024/D26/K11)
- CheTai phat_tien: 80.000.000–100.000.000 đồng (nêu tại ND168-2024/D26/K11)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D26/K11"], "required_numbers": [{"value": 40000000, "unit": "vnd"}, {"value": 50000000, "unit": "vnd"}, {"value": 80000000, "unit": "vnd"}, {"value": 100000000, "unit": "vnd"}]}
```

### W-muc_phat-005 · tier A · ND168-2024/D40/K3

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D40/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 40. Xử phạt các hành vi vi phạm quy định về hoạt động đăng kiểm xe cơ giới, xe máy chuyên dùng, phụ tùng xe cơ giới
> 3. Phạt tiền từ 10.000.000 đồng đến 15.000.000 đồng đối với cơ sở thử nghiệm, chứng nhận xe cơ giới, xe máy chuyên dùng, phụ tùng xe cơ giới trong sản xuất, lắp ráp và nhập khẩu thực hiện một trong các hành vi vi phạm sau đây:
> a) Không thực hiện niêm yết công khai các trình tự, thủ tục thử nghiệm, chứng nhận theo quy định;
> b) Thực hiện việc thử nghiệm, chứng nhận không đúng quy định;
> c) Phân công người không đủ điều kiện thực hiện việc thử nghiệm, chứng nhận;
> đ) Sử dụng thiết bị, dụng cụ không đảm bảo theo quy định của pháp luật về đo lường để kiểm tra, thử nghiệm;
> đ) Có từ 02 lượt đăng kiểm viên trở lên bị xử phạt theo quy định tại khoản 1 Điều này trong thời hạn 12 tháng tính từ lần bị xử phạt đầu tiên;
> c) Lưu trữ hồ sơ, tài liệu, dữ liệu chứng nhận không đúng quy định.

- CheTai phat_tien: 10.000.000–15.000.000 đồng (nêu tại ND168-2024/D40/K3)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D40/K3"], "required_numbers": [{"value": 10000000, "unit": "vnd"}, {"value": 15000000, "unit": "vnd"}]}
```

### W-muc_phat-006 · tier A · ND168-2024/D6/K1a

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D6/K1a#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
> 1a. Phạt cảnh cáo đối với người điều khiển xe ô tô thực hiện hành vi chở trẻ em dưới 10 tuổi và chiều cao dưới 1,35 mét trên xe mà không sử dụng thiết bị an toàn phù hợp cho trẻ em theo quy định (trừ xe ô tô kinh doanh vận tải hành khách).

- CheTai canh_cao:  (nêu tại ND168-2024/D6/K1a)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D6/K1a"], "required_numbers": []}
```

### W-muc_phat-007 · tier A · ND168-2024/D16/K2

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D16/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 16. Xử phạt người điều khiển xe máy chuyên dùng (kể cả rơ moóc được kéo theo) vi phạm quy định về điều kiện của phương tiện khi tham gia giao thông
> 2. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe hoạt động không đúng phạm vi quy định;
> b) Điều khiển xe không có giấy chứng nhận hoặc tem kiểm định an toàn kỹ thuật và bảo vệ môi trường (đối với loại xe có quy định phải kiểm định, trừ xe đăng ký tạm thời) hoặc có nhưng đã hết hiệu lực (hạn sử dụng) từ 01 tháng trở lên (kể cả rơ moóc);
> c) Điều khiển xe không có chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe) hoặc sử dụng chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe) đã hết hạn sử dụng, hết hiệu lực (kể cả rơ moóc);
> đ) Điều khiển xe gắn biển số không …

- BienPhapBoSung: buộc nộp lại chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe), giấy chứng nhận, tem kiểm định an toàn kỹ thuật và bảo vệ môi trường bị tẩy xóa (nêu tại ND168-2024/D16/K5/b)
- CheTai phat_tien: 1.000.000–2.000.000 đồng (nêu tại ND168-2024/D16/K2)
- CheTai tich_thu: biển số xe (nêu tại ND168-2024/D16/K4/a)
- CheTai tich_thu: phương tiện (nêu tại ND168-2024/D16/K4/b)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D16/K2"], "required_numbers": [{"value": 1000000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}]}
```

### W-muc_phat-008 · tier A · ND168-2024/D20/K8

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D20/K8#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
> 8. Phạt tiền từ 10.000.000 đồng đến 12.000.000 đồng đối với người điều khiển xe thực hiện hành vi đón, trả hành khách trên đường cao tốc.

- CheTai phat_tien: 10.000.000–12.000.000 đồng (nêu tại ND168-2024/D20/K8)
- DiemGPLX: trừ 6 điểm (nêu tại ND168-2024/D20/K10/c)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D20/K8"], "required_numbers": [{"value": 10000000, "unit": "vnd"}, {"value": 12000000, "unit": "vnd"}, {"value": 6, "unit": "diem"}]}
```

### W-muc_phat-009 · tier A · ND168-2024/D18/K1

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D18/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 18. Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm quy định về điều kiện của người điều khiển xe cơ giới
> 1. Phạt cảnh cáo người từ đủ 14 tuổi đến dưới 16 tuổi điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy hoặc điều khiển xe ô tô, điều khiển xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô.

- CheTai canh_cao:  (nêu tại ND168-2024/D18/K1)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D18/K1"], "required_numbers": []}
```

### W-muc_phat-010 · tier A · ND168-2024/D7/K2

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D7/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 7. Xử phạt, trừ điểm giấy phép lái của người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy vi phạm quy tắc giao thông đường bộ
> 2. Phạt tiền từ 400.000 đồng đến 600.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Dừng xe, đỗ xe trên phần đường xe chạy ở đoạn đường ngoài đô thị nơi có lề đường;
> b) Điều khiển xe chạy quá tốc độ quy định từ 05 km/h đến dưới 10 km/h;
> c) Điều khiển xe chạy tốc độ thấp mà không đi bên phải phần đường xe chạy gây cản trở giao thông;
> d) Dừng xe, đỗ xe ở lòng đường gây cản trở giao thông; tụ tập từ 03 xe trở lên ở lòng đường, trong hầm đường bộ; đỗ, để xe ở lòng đường, vỉa hè trái phép;
> đ) Xe không được quyền ưu tiên lắp đặt, sử dụng thiết bị phát tín hiệu của xe được quyền ưu tiên;
> e) Dừng xe, đỗ xe trên điểm đón, trả khách, nơi đường bộ giao nhau, trên phần đường dành cho người đi bộ qua đường; dừng xe nơi có biển “Cấm dừng xe và đỗ xe”; đỗ xe tại nơi có biển “Cấm đỗ xe” hoặc biển “Cấm dừng xe và đỗ xe”; không tuân thủ các quy định về dừng xe, đỗ xe tại nơi đường bộ giao nhau cùng mức với đường sắt; dừng xe, đỗ xe trong phạm vi hành lang an toàn giao thông …

- CheTai tich_thu: thiết bị phát tín hiệu ưu tiên lắp đặt, sử dụng trái quy định (nêu tại ND168-2024/D7/K12/a)
- CheTai phat_tien: 400.000–600.000 đồng (nêu tại ND168-2024/D7/K2)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D7/K2"], "required_numbers": [{"value": 400000, "unit": "vnd"}, {"value": 600000, "unit": "vnd"}]}
```

### W-muc_phat-011 · tier A · ND168-2024/D20/K1

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D20/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
> 1. Phạt tiền từ 100.000 đồng đến 200.000 đồng đối với hành vi vi phạm: không hướng dẫn hành khách đứng, nằm, ngồi đúng vị trí quy định trong xe.

- CheTai phat_tien: 100.000–200.000 đồng (nêu tại ND168-2024/D20/K1)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D20/K1"], "required_numbers": [{"value": 100000, "unit": "vnd"}, {"value": 200000, "unit": "vnd"}]}
```

### W-muc_phat-012 · tier A · ND168-2024/D32/K14

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D32/K14#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
> 14. Phạt tiền từ 28.000.000 đồng đến 30.000.000 đồng đối với cá nhân, từ 56.000.000 đồng đến 60.000.000 đồng đối với tổ chức là chủ xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ, xe máy chuyên dùng và các loại xe tương tự xe ô tô thực hiện một trong các hành vi vi phạm sau đây:
> a) Giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm a khoản 3 Điều 22 của Nghị định này hoặc trực tiếp điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm a khoản 3 Điều 22 của Nghị định này;
> b) Giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm b khoản 3 Điều 22 của Nghị định này hoặc trực tiếp điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm b khoản 3 Điều 22 của Nghị định này;
> c) Giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm c khoản 3 Điều 22 của Nghị định này hoặc trực tiếp điều khiển …

- BienPhapBoSung: buộc khôi phục lại hình dáng, kích thước, tình trạng an toàn kỹ thuật ban đầu của xe và đăng kiểm lại trước khi đưa phương tiện ra tham gia giao thông (nêu tại ND168-2024/D32/K19/d)
- BienPhapBoSung: phải khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND168-2024/D32/K19/e)
- CheTai phat_tien: 28.000.000–30.000.000 đồng (nêu tại ND168-2024/D32/K14)
- CheTai phat_tien: 56.000.000–60.000.000 đồng (nêu tại ND168-2024/D32/K14)
- CheTai tuoc_quyen: 1–3 tháng chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường và tem kiểm định của phương tiện (nêu tại ND168-2024/D32/K18/d)
- CheTai tuoc_quyen: 1–3 tháng phù hiệu (nêu tại ND168-2024/D32/K18/đ)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D32/K21/a)
- DiemGPLX: trừ 3 điểm (nêu tại ND168-2024/D32/K21/b)
- DiemGPLX: trừ 4 điểm (nêu tại ND168-2024/D32/K21/c)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D32/K14"], "required_numbers": [{"value": 28000000, "unit": "vnd"}, {"value": 30000000, "unit": "vnd"}, {"value": 56000000, "unit": "vnd"}, {"value": 60000000, "unit": "vnd"}, {"value": 1, "unit": "thang"}, {"value": 3, "unit": "thang"}, {"value": 2, "unit": "diem"}, {"value": 3, "unit": "diem"}, {"value": 4, "unit": "diem"}]}
```

### W-muc_phat-013 · tier A · ND168-2024/D8/K8

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D8/K8#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 8. Xử phạt người điều khiển xe máy chuyên dùng vi phạm quy tắc giao thông đường bộ
> 8. Phạt tiền từ 14.000.000 đồng đến 16.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe không quan sát, giảm tốc độ hoặc dừng lại để bảo đảm an toàn theo quy định mà gây tai nạn giao thông; điều khiển xe chạy quá tốc độ quy định gây tai nạn giao thông; dừng xe, đỗ xe, quay đầu xe, lùi xe, tránh xe, vượt xe, chuyển hướng, chuyển làn đường không đúng quy định gây tai nạn giao thông; mở cửa xe, để cửa xe mở không bảo đảm an toàn gây tai nạn giao thông; không đi đúng phần đường, làn đường, không giữ khoảng cách an toàn giữa hai xe theo quy định gây tai nạn giao thông hoặc đi vào đường có biển báo hiệu có nội dung cấm đi vào đối với loại phương tiện đang điều khiển, đi ngược chiều của đường một chiều, đi ngược chiều trên đường có biển “Cấm đi ngược chiều” gây tai nạn giao thông, trừ các hành vi vi phạm quy định tại điểm b khoản 8, điểm đ khoản 9 Điều này;
> b) Điều khiển xe máy chuyên dùng có tốc độ thiết kế nhỏ hơn tốc độ tối thiểu quy định đối với đường cao tốc đi vào đường cao tốc, trừ phương tiện, thiết bị phục vụ việc quản lý, bảo trì …

- CheTai phat_tien: 14.000.000–16.000.000 đồng (nêu tại ND168-2024/D8/K8)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D8/K8"], "required_numbers": [{"value": 14000000, "unit": "vnd"}, {"value": 16000000, "unit": "vnd"}]}
```

### W-muc_phat-014 · tier A · ND168-2024/D15/K2

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D15/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 15. Xử phạt người điều khiển xe thô sơ vi phạm quy định về điều kiện của phương tiện khi tham gia giao thông
> 2. Phạt tiền từ 300.000 đồng đến 400.000 đồng đối với hành vi điều khiển xe không có hệ thống (bộ phận) hãm hoặc có nhưng không có hiệu lực (đối với loại xe quy định phải có hệ thống (bộ phận) này).

- CheTai phat_tien: 300.000–400.000 đồng (nêu tại ND168-2024/D15/K2)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D15/K2"], "required_numbers": [{"value": 300000, "unit": "vnd"}, {"value": 400000, "unit": "vnd"}]}
```

### W-muc_phat-015 · tier A · ND168-2024/D13/K4

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D13/K4#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 13. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo), xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tư xe ô tô vi phạm quy định về điều kiện của phương tiện khi tham gia giao thông
> 4. Phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe không có chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe) hoặc sử dụng chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe) đã hết hạn sử dụng, hết hiệu lực (kể cả rơ moóc và sơ mi rơ moóc);
> b) Điều khiển xe ô tô tải (kể cả rơ moóc và sơ mi rơ moóc) có kích thước thùng xe không đúng với thông số kỹ thuật được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo …

- BienPhapBoSung: buộc lắp đầy đủ thiết bị hoặc thay thế thiết bị đủ tiêu chuẩn, quy chuẩn an toàn kỹ thuật hoặc khôi phục lại tính năng kỹ thuật của thiết bị theo quy định (nêu tại ND168-2024/D13/K11/a)
- BienPhapBoSung: buộc thực hiện đúng quy định về biển số hoặc khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND168-2024/D13/K11/a)
- BienPhapBoSung: buộc khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND168-2024/D13/K11/c)
- CheTai tich_thu: phương tiện (nêu tại ND168-2024/D13/K10/b)
- CheTai phat_tien: 2.000.000–3.000.000 đồng (nêu tại ND168-2024/D13/K4)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D13/K13/a)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D13/K4"], "required_numbers": [{"value": 2000000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}]}
```

### W-muc_phat-016 · tier A · ND168-2024/D32/K6

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D32/K6#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
> 6. Phạt tiền từ 2.000.000 đồng đến 4.000.000 đồng trên mỗi người vượt quá quy định được phép chở của phương tiện nhưng tổng mức phạt tiền tối đa không vượt quá 75.000.000 đồng đối với chủ phương tiện là cá nhân, từ 4.000.000 đồng đến 8.000.000 đồng trên mỗi người vượt quá quy định được phép chở của phương tiện nhưng tổng mức phạt tiền tối đa không vượt quá 150.000.000 đồng đối với chủ phương tiện là tổ chức giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại khoản 4 Điều 20 của Nghị định này hoặc trực tiếp điều khiển phương tiện thực hiện hành vi vi phạm quy định tại khoản 4 Điều 20 của Nghị định này.

- CheTai tuoc_quyen: 1–3 tháng phù hiệu (nêu tại ND168-2024/D32/K18/đ)
- CheTai phat_tien: 2.000.000–4.000.000 đồng (nêu tại ND168-2024/D32/K6)
- DiemGPLX: trừ 4 điểm (nêu tại ND168-2024/D32/K21/d)
- DiemGPLX: trừ 10 điểm (nêu tại ND168-2024/D32/K21/h)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D32/K6"], "required_numbers": [{"value": 1, "unit": "thang"}, {"value": 3, "unit": "thang"}, {"value": 2000000, "unit": "vnd"}, {"value": 4000000, "unit": "vnd"}, {"value": 4, "unit": "diem"}, {"value": 10, "unit": "diem"}]}
```

### W-muc_phat-017 · tier A · ND168-2024/D23/K2

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D23/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 23. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển hàng hóa nguy hiểm
> 2. Phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng đối với hành vi vận chuyển hàng hóa nguy hiểm mà không mang theo hồ sơ vận chuyển hàng hóa nguy hiểm do người thuê vận tải cung cấp theo quy định, giấy chứng nhận hoàn thành chương trình tập huấn an toàn hàng hóa nguy hiểm phù hợp với loại, nhóm hàng hóa nguy hiểm đang vận chuyển (nếu có).

- CheTai phat_tien: 2.000.000–3.000.000 đồng (nêu tại ND168-2024/D23/K2)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D23/K2"], "required_numbers": [{"value": 2000000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}]}
```

### W-muc_phat-018 · tier A · ND168-2024/D26/K3

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D26/K3#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
> 3. Phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng đối với cá nhân, từ 4.000.000 đồng đến 6.000.000 đồng đối với tổ chức thực hiện hành vi vi phạm xếp hàng hóa lên mỗi xe ô tô (kể cả rơ moóc và sơ mi rơ moóc) vượt quá trọng tải (khối lượng hàng chuyên chở) cho phép tham gia giao thông được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe trên 50% đến 100%.

- CheTai phat_tien: 2.000.000–3.000.000 đồng (nêu tại ND168-2024/D26/K3)
- CheTai phat_tien: 4.000.000–6.000.000 đồng (nêu tại ND168-2024/D26/K3)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D26/K3"], "required_numbers": [{"value": 2000000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}, {"value": 4000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}]}
```

### W-muc_phat-019 · tier A · ND168-2024/D37/K1

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D37/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 37. Xử phạt người điều khiển phương tiện giao thông cơ giới đường bộ gắn biển số nước ngoài
> 1. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với người điều khiển phương tiện giao thông cơ giới đường bộ gắn biển số nước ngoài thực hiện một trong các hành vi vi phạm sau đây:
> a) Giấy tờ của phương tiện không có bản dịch sang tiếng Anh hoặc tiếng Việt theo quy định;
> b) Điều khiển xe chở hành khách không có danh sách hành khách theo quy định.

- CheTai phat_tien: 1.000.000–2.000.000 đồng (nêu tại ND168-2024/D37/K1)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D37/K1"], "required_numbers": [{"value": 1000000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}]}
```

### W-muc_phat-020 · tier A · ND168-2024/D17/K2

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D17/K2#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 17. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, máy kéo và các loại xe tương tự xe ô tô vi phạm quy định về bảo vệ môi trường khi tham gia giao thông
> 2. Phạt tiền từ 2.000.000 đồng đến 4.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Chở vật liệu xây dựng, đất đá, phế thải, hàng rời mà không che đậy; làm rơi vãi hàng hóa, vật liệu xây dựng, đất đá, phế thải, bùn, hàng rời xuống đường; chở hàng hoặc chất thải để nước chảy xuống đường;
> b) Lôi kéo bùn, đất, cát, nguyên liệu, vật liệu hoặc chất phế thải khác ra đường bộ gây mất an toàn giao thông.

- CheTai phat_tien: 2.000.000–4.000.000 đồng (nêu tại ND168-2024/D17/K2)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D17/K2"], "required_numbers": [{"value": 2000000, "unit": "vnd"}, {"value": 4000000, "unit": "vnd"}]}
```

### W-muc_phat-021 · tier A · ND168-2024/D6/K10

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D6/K10#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
> 10. Phạt tiền từ 20.000.000 đồng đến 22.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe không quan sát, giảm tốc độ hoặc dừng lại để bảo đảm an toàn theo quy định mà gây tai nạn giao thông; điều khiển xe chạy quá tốc độ quy định gây tai nạn giao thông; dừng xe, đỗ xe, quay đầu xe, lùi xe, tránh xe, vượt xe, chuyển hướng, chuyển làn đường không đúng quy định gây tai nạn giao thông; không đi đúng phần đường, làn đường, không giữ khoảng cách an toàn giữa hai xe theo quy định gây tai nạn giao thông hoặc đi vào đường có biển báo hiệu có nội dung cấm đi vào đối với loại phương tiện đang điều khiển gây tai nạn giao thông, trừ các hành vi vi phạm quy định tại điểm đ khoản 11 Điều này;
> b) Vi phạm quy định tại một trong các điểm, khoản sau của Điều này mà gây tai nạn giao thông: điểm a, điểm b, điểm c, điểm d, điểm đ khoản 1; điểm c khoản 2; điểm b, điểm g, điểm h, điểm n, điểm o, điểm p, khoản 3; điểm a, điểm c, điểm d …

- CheTai phat_tien: 20.000.000–22.000.000 đồng (nêu tại ND168-2024/D6/K10)
- DiemGPLX: trừ 10 điểm (nêu tại ND168-2024/D6/K16/d)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D6/K10"], "required_numbers": [{"value": 20000000, "unit": "vnd"}, {"value": 22000000, "unit": "vnd"}, {"value": 10, "unit": "diem"}]}
```

### W-muc_phat-022 · tier A · ND168-2024/D40/K5

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D40/K5#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 40. Xử phạt các hành vi vi phạm quy định về hoạt động đăng kiểm xe cơ giới, xe máy chuyên dùng, phụ tùng xe cơ giới
> 5. Phạt tiền từ 16.000.000 đồng đến 20.000.000 đồng đối với cơ sở sản xuất, lắp ráp, cơ sở nhập khẩu, cơ sở bảo hành, bảo dưỡng hoặc tổ chức, cá nhân được ủy quyền thực hiện một trong các hành vi vi phạm sau đây:
> a) Sử dụng, cung cấp hồ sơ, tài liệu giả để thực hiện việc kiểm tra, chứng nhận, thử nghiệm nhưng chưa đến mức bị truy cứu trách nhiệm hình sự;
> b) Sử dụng thiết bị, dụng cụ không đảm bảo theo quy định của pháp luật về đo lường để kiểm tra chất lượng xuất xưởng xe cơ giới, xe máy chuyên dùng, phụ tùng xe cơ giới.

- CheTai phat_tien: 16.000.000–20.000.000 đồng (nêu tại ND168-2024/D40/K5)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D40/K5"], "required_numbers": [{"value": 16000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}]}
```

### W-muc_phat-023 · tier A · ND168-2024/D32/K7

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D32/K7#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
> 7. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng đối với cá nhân, từ 8.000.000 đồng đến 12.000.000 đồng đối với tổ chức là chủ xe ô tô (kể cả rơ moóc và sơ mi rơ moóc), xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ, xe máy chuyên dùng và các loại xe tương tự xe ô tô thực hiện một trong các hành vi vi phạm sau đây:
> a) Tẩy xóa, sửa chữa hoặc giả mạo hồ sơ đăng ký xe nhưng chưa đến mức truy cứu trách nhiệm hình sự;
> b) Không làm thủ tục thu hồi chứng nhận đăng ký xe; biển số xe; theo quy định;
> c) Không làm thủ tục đổi chứng nhận đăng ký xe, biển số xe theo quy định;
> d) Khai báo không đúng sự thật hoặc sử dụng các giấy tờ, tài liệu giả để được cấp lại biển số xe, chứng nhận đăng ký xe, nhưng chưa đến mức bị truy cứu trách nhiệm hình sự;
> đ) Giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm e khoản 3; điểm i khoản 5 Điều 20 của Nghị định này hoặc trực tiếp điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm e khoản 3; điểm i khoản 5 Điều 20 của Nghị …

- BienPhapBoSung: buộc khôi phục lại nhãn hiệu, màu sơn ghi trong chứng nhận đăng ký xe theo quy định (nêu tại ND168-2024/D32/K19/a)
- BienPhapBoSung: phải khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND168-2024/D32/K19/e)
- BienPhapBoSung: buộc làm thủ tục đổi, thu hồi, cấp mới, cấp chứng nhận đăng ký xe, biển số xe, chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường theo quy định (trừ trường hợp bị tịch thu phương tiện) (nêu tại ND168-2024/D32/K19/g)
- BienPhapBoSung: buộc tháo dỡ thiết bị âm thanh, ánh sáng lắp đặt trên xe gây mất trật tự, an toàn giao thông đường bộ (nêu tại ND168-2024/D32/K19/h)
- BienPhapBoSung: buộc điều chỉnh lại chỉ số trên đồng hồ báo quãng đường của xe ô tô bị làm sai lệch (nêu tại ND168-2024/D32/K19/k)
- BienPhapBoSung: buộc lắp đặt dụng cụ, thiết bị chuyên dùng để cứu hộ, hỗ trợ cứu hộ, thiết bị giám sát hành trình, thiết bị ghi nhận hình ảnh người lái xe trên xe theo đúng quy định (nêu tại ND168-2024/D32/K19/l)
- BienPhapBoSung: buộc thực hiện điều chỉnh thùng xe theo đúng quy định hiện hành, đăng kiểm lại và điều chỉnh lại khối lượng hàng hóa cho phép chuyên chở ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường theo quy định hiện hành trước khi đưa phương tiện ra tham gia giao thông (nêu tại ND168-2024/D32/K19/đ)
- CheTai tuoc_quyen: 1–3 tháng chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường và tem kiểm định của phương tiện (nêu tại ND168-2024/D32/K18/c)
- CheTai tich_thu: phương tiện) (nêu tại ND168-2024/D32/K19/g)
- CheTai phat_tien: 4.000.000–6.000.000 đồng (nêu tại ND168-2024/D32/K7)
- CheTai phat_tien: 8.000.000–12.000.000 đồng (nêu tại ND168-2024/D32/K7)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D32/K21/a)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D32/K7"], "required_numbers": [{"value": 1, "unit": "thang"}, {"value": 3, "unit": "thang"}, {"value": 4000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}, {"value": 8000000, "unit": "vnd"}, {"value": 12000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}]}
```

### W-muc_phat-024 · tier A · ND168-2024/D7/K8

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D7/K8#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 7. Xử phạt, trừ điểm giấy phép lái của người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy vi phạm quy tắc giao thông đường bộ
> 8. Phạt tiền từ 6.000.000 đồng đến 8.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe chạy quá tốc độ quy định trên 20 km/h;
> b) Điều khiển xe trên đường mà trong máu hoặc hơi thở có nồng độ cồn vượt quá 50 miligam đến 80 miligam/100 mililít máu hoặc vượt quá 0,25 miligam đến 0,4 miligam/1 lít khí thở.

- CheTai phat_tien: 6.000.000–8.000.000 đồng (nêu tại ND168-2024/D7/K8)
- DiemGPLX: trừ 4 điểm (nêu tại ND168-2024/D7/K13/b)
- DiemGPLX: trừ 10 điểm (nêu tại ND168-2024/D7/K13/d)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D7/K8"], "required_numbers": [{"value": 6000000, "unit": "vnd"}, {"value": 8000000, "unit": "vnd"}, {"value": 4, "unit": "diem"}, {"value": 10, "unit": "diem"}]}
```

### W-muc_phat-025 · tier A · ND168-2024/D13/K3

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D13/K3#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 13. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo), xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tư xe ô tô vi phạm quy định về điều kiện của phương tiện khi tham gia giao thông
> 3. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe lắp thêm đèn phía trước, phía sau, trên nóc, dưới gầm, một hoặc cả hai bên thành xe, trừ đèn sương mù dạng rời được lấp theo quy định;
> b) Điều khiển xe có hệ thống chuyển hướng của xe không đúng tiêu chuẩn an toàn kỹ thuật;
> c) Điều khiển xe không lắp đủ bánh lốp hoặc lắp bánh lốp không đúng kích cỡ hoặc không bảo đảm tiêu chuẩn kỹ thuật (kể cả rơ moóc và sơ mi rơ moóc);
> d) Điều khiển xe ô tô kinh doanh vận tải hành khách lắp thêm hoặc tháo bớt ghế, giường nằm hoặc có kích thước khoang chở hành lý (hầm xe) không đúng với thông số kỹ thuật được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe.

- BienPhapBoSung: buộc lắp đầy đủ thiết bị hoặc thay thế thiết bị đủ tiêu chuẩn, quy chuẩn an toàn kỹ thuật hoặc khôi phục lại tính năng kỹ thuật của thiết bị theo quy định (nêu tại ND168-2024/D13/K11/a)
- BienPhapBoSung: buộc thực hiện đúng quy định về biển số hoặc khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND168-2024/D13/K11/a)
- BienPhapBoSung: buộc lắp đầy đủ thiết bị hoặc khôi phục lại tính năng kỹ thuật của thiết bị theo quy định, tháo bỏ những thiết bị lắp thêm không đúng quy định (nêu tại ND168-2024/D13/K11/b)
- CheTai phat_tien: 1.000.000–2.000.000 đồng (nêu tại ND168-2024/D13/K3)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D13/K13/a)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D13/K3"], "required_numbers": [{"value": 1000000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}]}
```

### W-muc_phat-026 · tier A · ND168-2024/D39/K2

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D39/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 39. Xử phạt các hành vi vi phạm quy định về đào tạo, sát hạch lái xe
> 2. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với cơ sở đào tạo lái xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Sử dụng xe tập lái không có mui che mưa, nắng; không có ghế ngồi gắn chắc chắn trên thùng xe cho người học theo quy định;
> b) Không thực hiện việc ký hợp đồng đào tạo, thanh lý hợp đồng đào tạo với người học lái xe theo quy định; có ký hợp đồng đào tạo, thanh lý hợp đồng đào tạo nhưng không do người học lái xe trực tiếp ký;
> c) Không công khai quy chế tuyển sinh, quản lý đào tạo và mức thu học phí theo quy định;

- CheTai phat_tien: 3.000.000–5.000.000 đồng (nêu tại ND168-2024/D39/K2)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D39/K2"], "required_numbers": [{"value": 3000000, "unit": "vnd"}, {"value": 5000000, "unit": "vnd"}]}
```

### W-muc_phat-027 · tier A · ND168-2024/D37/K3

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D37/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 37. Xử phạt người điều khiển phương tiện giao thông cơ giới đường bộ gắn biển số nước ngoài
> 3. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Điều khiển phương tiện không gắn ký hiệu phân biệt quốc gia theo quy định;
> b) Điều khiển phương tiện không có giấy phép liên vận, giấy phép vận tải đường bộ quốc tế theo quy định hoặc có nhưng đã hết giá trị sử dụng;
> c) Vận chuyển hành khách hoặc hàng hóa không đúng với quy định tại các điều ước quốc tế mà Việt Nam đã ký kết, trừ các hành vi vi phạm quy định tại khoản 1, khoản 4, khoản 5, khoản 6 Điều này.

- BienPhapBoSung: buộc tái xuất phương tiện khỏi Việt Nam (nêu tại ND168-2024/D37/K7)
- CheTai phat_tien: 3.000.000–5.000.000 đồng (nêu tại ND168-2024/D37/K3)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D37/K3"], "required_numbers": [{"value": 3000000, "unit": "vnd"}, {"value": 5000000, "unit": "vnd"}]}
```

### W-muc_phat-028 · tier A · ND168-2024/D31/K2

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D31/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 31. Xử phạt hành vi sản xuất, lắp ráp trái phép phương tiện giao thông cơ giới đường bộ; sản xuất, mua, bán biển số xe trái phép
> 2. Phạt tiền từ 40.000.000 đồng đến 50.000.000 đồng đối với cá nhân, từ 80.000.000 đồng đến 100.000.000 đồng đối với tổ chức thực hiện hành vi sản xuất biển số trái phép hoặc sản xuất, lắp ráp trái phép phương tiện giao thông cơ giới đường bộ.

- BienPhapBoSung: buộc nộp lại số lợi bất hợp pháp có được do thực hiện vi phạm hành chính (nêu tại ND168-2024/D31/K4)
- CheTai phat_tien: 40.000.000–50.000.000 đồng (nêu tại ND168-2024/D31/K2)
- CheTai phat_tien: 80.000.000–100.000.000 đồng (nêu tại ND168-2024/D31/K2)
- CheTai tich_thu: biển số, phương tiện sản xuất, lắp ráp trái phép (nêu tại ND168-2024/D31/K3)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D31/K2"], "required_numbers": [{"value": 40000000, "unit": "vnd"}, {"value": 50000000, "unit": "vnd"}, {"value": 80000000, "unit": "vnd"}, {"value": 100000000, "unit": "vnd"}]}
```

### W-muc_phat-029 · tier A · ND168-2024/D12/K12

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D12/K12#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 12. Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm khác về quy tắc giao thông đường bộ; sử dụng lòng đường, vỉa hè vào mục đích khác
> 12. Phạt tiền từ 10.000.000 đồng đến 15.000.000 đồng đối với cá nhân, từ 20.000.000 đồng đến 30.000.000 đồng đối với tổ chức thực hiện hành vi sử dụng tạm thời lòng đường, vỉa hè vào mục đích khác (theo quy định phải có giấy phép) mà không có giấy phép hoặc có giấy phép nhưng đã hết giá trị sử dụng hoặc thực hiện không đúng nội dung ghi trong giấy phép.

- BienPhapBoSung: buộc khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND168-2024/D12/K16/b)
- CheTai phat_tien: 10.000.000–15.000.000 đồng (nêu tại ND168-2024/D12/K12)
- CheTai phat_tien: 20.000.000–30.000.000 đồng (nêu tại ND168-2024/D12/K12)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D12/K12"], "required_numbers": [{"value": 10000000, "unit": "vnd"}, {"value": 15000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}, {"value": 30000000, "unit": "vnd"}]}
```

### W-muc_phat-030 · tier A · ND168-2024/D14/K3

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D14/K3#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 14. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy vi phạm quy định về điều kiện của phương tiện khi tham gia giao thông
> 3. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe không gắn biển số (đối với loại xe có quy định phải gắn biển số); gắn biển số không đúng với chứng nhận đăng ký xe hoặc gắn biển số không do cơ quan có thẩm quyền cấp;
> b) Điều khiển xe gắn biển số không đúng vị trí, không đúng quy cách theo quy định; gắn biển số không rõ chữ, số hoặc sơn, dán lên chữ, số của biển số xe; gắn biển số bị bẻ cong, che lấp, làm thay đổi chữ, số, màu sắc (của chữ, số, nền biển số xe), hình dạng, kích thước của biển số xe; sử dụng chất liệu, vật liệu, thiết bị làm thay đổi khả năng nhận diện thông tin biển số xe của phương tiện, thiết bị kỹ thuật nghiệp vụ.

- CheTai phat_tien: 4.000.000–6.000.000 đồng (nêu tại ND168-2024/D14/K3)
- CheTai tich_thu: biển số xe (nêu tại ND168-2024/D14/K5/a)
- DiemGPLX: trừ 6 điểm (nêu tại ND168-2024/D14/K8/b)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D14/K3"], "required_numbers": [{"value": 4000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}, {"value": 6, "unit": "diem"}]}
```

### W-muc_phat-031 · tier A · ND168-2024/D6/K3

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D6/K3#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
> 3. Phạt tiền từ 800.000 đồng đến 1.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe chạy quá tốc độ quy định từ 05 km/h đến dưới 10 km/h;
> b) Sử dụng còi, rú ga liên tục; sử dụng còi hơi, sử dụng đèn chiếu xa khi gặp người đi bộ qua đường hoặc khi đi trên đoạn đường qua khu dân cư có hệ thống chiếu sáng đang hoạt động hoặc khi gặp xe đi ngược chiều (trừ trường hợp dải phân cách có khả năng chống chói) hoặc khi chuyển hướng xe tại nơi đường giao nhau, trừ các xe ưu tiên đang đi làm nhiệm vụ theo quy định;
> c) Chuyển hướng không quan sát hoặc không bảo đảm khoảng cách an toàn với xe phía sau hoặc không giảm tốc độ hoặc không có tín hiệu báo hướng rẽ hoặc có tín hiệu báo hướng rẽ nhưng không sử dụng liên tục trong quá trình chuyển hướng (trừ trường hợp điều khiển xe đi theo hướng cong của đoạn đường bộ ở nơi đường không giao nhau cùng mức);
> d) Không tuân thủ các quy định về dừng xe, đỗ xe tại nơi đường bộ giao nhau …

- CheTai phat_tien: 800.000–1.000.000 đồng (nêu tại ND168-2024/D6/K3)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D6/K16/a)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D6/K3"], "required_numbers": [{"value": 800000, "unit": "vnd"}, {"value": 1000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}]}
```

### W-muc_phat-032 · tier A · ND168-2024/D6/K9

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D6/K9#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
> 9. Phạt tiền từ 18.000.000 đồng đến 20.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe trên đường mà trong máu hoặc hơi thở có nồng độ cồn vượt quá 50 miligam đến 80 miligam/100 mililít máu hoặc vượt quá 0,25 miligam đến 0,4 miligam/1 lít khí thở;
> b) Không chấp hành hiệu lệnh của đèn tín hiệu giao thông;
> c) Không chấp hành hiệu lệnh, hướng dẫn của người điều khiển giao thông hoặc người kiểm soát giao thông;
> d) Đi ngược chiều của đường một chiều, đi ngược chiều trên đường có biển "Cấm đi ngược chiều”, trừ các hành vi vi phạm quy định tại điểm đ khoản 11 Điều này và các trường hợp xe ưu tiên đang đi làm nhiệm vụ khẩn cấp theo quy định.

- CheTai phat_tien: 18.000.000–20.000.000 đồng (nêu tại ND168-2024/D6/K9)
- DiemGPLX: trừ 4 điểm (nêu tại ND168-2024/D6/K16/b)
- DiemGPLX: trừ 10 điểm (nêu tại ND168-2024/D6/K16/d)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D6/K9"], "required_numbers": [{"value": 18000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}, {"value": 4, "unit": "diem"}, {"value": 10, "unit": "diem"}]}
```

### W-muc_phat-033 · tier A · ND168-2024/D18/K7

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D18/K7#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 18. Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm quy định về điều kiện của người điều khiển xe cơ giới
> 7. Phạt tiền từ 6.000.000 đồng đến 8.000.000 đồng đối với người điều khiển xe mô tô hai bánh có dung tích xi-lanh trên 125 cm3 trở lên hoặc có công suất động cơ điện trên 11 kW, xe mô tô ba bánh thực hiện một trong các hành vi vi phạm sau đây:
> a) Có giấy phép lái xe nhưng không phù hợp với loại xe đang điều khiển;
> b) Không có giấy phép lái xe hoặc sử dụng giấy phép lái xe đã bị trừ hết điểm, giấy phép lái xe không do cơ quan có thẩm quyền cấp, giấy phép lái xe bị tẩy xóa, giấy phép lái xe không còn hiệu lực;
> c) Có giấy phép lái xe quốc tế do các nước tham gia Công ước của Liên hợp quốc về Giao thông đường bộ năm 1968 cấp (trừ giấy phép lái xe quốc tế do Việt Nam cấp) nhưng không mang theo giấy phép lái xe quốc gia phù hợp với loại xe được phép điều khiển;
> d) Sử dụng giấy phép lái xe không hợp lệ (giấy phép lái xe có số phôi ghi ở mặt sau không trùng với số phôi được cấp mới nhất trong hệ thống thông tin quản lý giấy phép lái xe).

- BienPhapBoSung: buộc nộp lại giấy phép lái xe bị tẩy xóa (nêu tại ND168-2024/D18/K10)
- CheTai phat_tien: 6.000.000–8.000.000 đồng (nêu tại ND168-2024/D18/K7)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D18/K7"], "required_numbers": [{"value": 6000000, "unit": "vnd"}, {"value": 8000000, "unit": "vnd"}]}
```

### W-muc_phat-034 · tier A · ND168-2024/D21/K4

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D21/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
> 4. Phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng đối với người điều khiển xe thực hiện hành vi chở hàng vượt quá chiều cao xếp hàng cho phép đối với xe ô tô tải (kể cả rơ moóc và sơ mi rơ moóc).

- CheTai phat_tien: 2.000.000–3.000.000 đồng (nêu tại ND168-2024/D21/K4)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D21/K13/a)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D21/K4"], "required_numbers": [{"value": 2000000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}]}
```

### W-muc_phat-035 · tier A · ND168-2024/D8/K2

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D8/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 8. Xử phạt người điều khiển xe máy chuyên dùng vi phạm quy tắc giao thông đường bộ
> 2. Phạt tiền từ 600.000 đồng đến 800.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Dừng xe, đỗ xe trên phần đường xe chạy ở đoạn đường ngoài đô thị nơi có lề đường rộng; dừng xe, đỗ xe không sát mép đường phía bên phải theo chiều đi ở nơi đường có lề đường hẹp hoặc không có lề đường; dừng xe, đỗ xe ngược với chiều lưu thông của làn đường; dừng xe, đỗ xe trên dải phân cách cố định ở giữa hai phần đường xe chạy; dừng xe, đỗ xe không đúng vị trí quy định ở những đoạn đường đã có bố trí nơi dừng xe, đỗ xe; đỗ xe trên dốc không chèn bánh; dừng xe nơi có biển “Cấm dừng xe và đỗ xe”; đỗ xe nơi có biển “Cấm đỗ xe” hoặc biển “Cấm dừng xe và đỗ xe”, trừ hành vi vi phạm quy định tại điểm b khoản 6 Điều này;
> b) Dừng xe, đỗ xe tại các vị trí: bên trái đường một chiều hoặc bên trái (theo hướng lưu thông) của đường đôi; trên đoạn đường cong hoặc gần đầu dốc nơi tầm nhìn bị che khuất; trên cầu (trừ trường hợp tổ chức giao thông cho phép), gầm cầu vượt (trừ những nơi cho phép dừng xe, đỗ xe), song song với một xe khác đang dừng, đỗ; nơi đường bộ giao nhau hoặc trong …

- CheTai phat_tien: 600.000–800.000 đồng (nêu tại ND168-2024/D8/K2)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D8/K2"], "required_numbers": [{"value": 600000, "unit": "vnd"}, {"value": 800000, "unit": "vnd"}]}
```

### W-muc_phat-036 · tier A · ND168-2024/D7/K1

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D7/K1#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 7. Xử phạt, trừ điểm giấy phép lái của người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy vi phạm quy tắc giao thông đường bộ
> 1. Phạt tiền từ 200.000 đồng đến 400.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Không chấp hành hiệu lệnh, chỉ dẫn của biển báo hiệu, vạch kẻ đường, trừ các hành vi vi phạm quy định tại điểm b, điểm d, điểm e khoản 2; điểm a, điểm c, điểm d, điểm h khoản 3; điểm a, điểm b, điểm c, điểm d khoản 4; điểm b, điểm d khoản 6; điểm a, điểm b, điểm c khoản 7; điểm a khoản 8; điểm b khoản 9; điểm a khoản 10 Điều này;
> b) Không có tín hiệu trước khi vượt hoặc có tín hiệu vượt xe nhưng không sử dụng trong suốt quá trình vượt xe;
> c) Lùi xe mô tô ba bánh không quan sát hai bên, phía sau xe hoặc không có tín hiệu lùi xe;
> d) Chở người ngồi trên xe sử dụng ô (dù);
> đ) Không tuân thủ các quy định về nhường đường tại nơi đường giao nhau, trừ các hành vi vi phạm quy định tại điểm c, điểm d khoản 6 Điều này;
> e) Chuyển làn đường không đúng nơi cho phép hoặc không có tín hiệu báo trước hoặc chuyển làn đường không đúng quy định “mỗi lần chuyển làn đường chỉ được phép chuyển sang …

- CheTai phat_tien: 200.000–400.000 đồng (nêu tại ND168-2024/D7/K1)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D7/K1"], "required_numbers": [{"value": 200000, "unit": "vnd"}, {"value": 400000, "unit": "vnd"}]}
```

### W-muc_phat-037 · tier A · ND168-2024/D8/K9

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D8/K9#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 8. Xử phạt người điều khiển xe máy chuyên dùng vi phạm quy tắc giao thông đường bộ
> 9. Phạt tiền từ 18.000.000 đồng đến 20.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe trên đường mà trong máu hoặc hơi thở có nồng độ cồn vượt quá 80 miligam/100 mililít máu hoặc vượt quá 0,4 miligam/1 lít khí thở;
> b) Không chấp hành yêu cầu kiểm tra về nồng độ cồn của người thi hành công vụ;
> c) Điều khiển xe trên đường mà trong cơ thể có chất ma túy hoặc chất kích thích khác mà pháp luật cấm sử dụng;
> d) Không chấp hành yêu cầu kiểm tra về chất ma túy hoặc chất kích thích khác mà pháp luật cấm sử dụng của người thi hành công vụ;
> đ) Lùi xe trên đường cao tốc; đi ngược chiều trên đường cao tốc; quay đầu xe trên đường cao tốc;
> e) Vi phạm quy định tại điểm b khoản 8 Điều này mà gây tai nạn giao thông.

- CheTai phat_tien: 18.000.000–20.000.000 đồng (nêu tại ND168-2024/D8/K9)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D8/K9"], "required_numbers": [{"value": 18000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}]}
```

### W-muc_phat-038 · tier A · ND168-2024/D40/K2

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D40/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 40. Xử phạt các hành vi vi phạm quy định về hoạt động đăng kiểm xe cơ giới, xe máy chuyên dùng, phụ tùng xe cơ giới
> 2. Phạt tiền từ 10.000.000 đồng đến 15.000.000 đồng đối với cơ sở đăng kiểm thực hiện một trong các hành vi vi phạm sau đây:
> a) Không duy trì việc bảo đảm về điều kiện, yêu cầu theo quy định tại Nghị định của Chính phủ quy định về điều kiện kinh doanh dịch vụ kiểm định xe cơ giới; tổ chức, hoạt động của cơ sở đăng kiểm; niên hạn sử dụng của xe cơ giới;
> b) Có từ 02 lượt đăng kiểm viên trở lên bị xử phạt theo quy định tại khoản 1 Điều này trong thời hạn 12 tháng tính từ lần vi phạm đầu tiên;
> c) Phân công người không đủ điều kiện thực hiện nhiệm vụ của đăng kiểm viên, nhân viên nghiệp vụ;
> d) Cấp chứng nhận cải tạo cho xe cơ giới, xe máy chuyên dùng không đúng quy định;
> đ) Thực hiện kiểm định đối với phương tiện thuộc trường hợp bị từ chối kiểm định theo quy định;
> e) Lưu trữ hồ sơ, tài liệu, dữ liệu kiểm định, cải tạo xe không đúng quy định;
> g) Không thực hiện việc cập nhật hồ sơ phương tiện cho xe cơ giới, xe máy chuyên dùng theo quy định.

- CheTai phat_tien: 10.000.000–15.000.000 đồng (nêu tại ND168-2024/D40/K2)
- CheTai tuoc_quyen: 1–3 tháng giấy chứng nhận đủ điều kiện hoạt động kiểm định xe cơ giới (nêu tại ND168-2024/D40/K6/b)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D40/K2"], "required_numbers": [{"value": 10000000, "unit": "vnd"}, {"value": 15000000, "unit": "vnd"}, {"value": 1, "unit": "thang"}, {"value": 3, "unit": "thang"}]}
```

### W-muc_phat-039 · tier A · ND168-2024/D37/K4

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D37/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 37. Xử phạt người điều khiển phương tiện giao thông cơ giới đường bộ gắn biển số nước ngoài
> 4. Phạt tiền từ 8.000.000 đồng đến 10.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Điều khiển phương tiện không gắn biển số tạm thời hoặc gắn biển số tạm thời không do cơ quan có thẩm quyền cấp (nếu có quy định phải gắn biển số tạm thời);
> b) Điều khiển xe ô tô có tay lái bên phải tham gia giao thông mà không đi theo đoàn, không có người, phương tiện hỗ trợ, hướng dẫn giao thông theo quy định.

- BienPhapBoSung: buộc tái xuất phương tiện khỏi Việt Nam (nêu tại ND168-2024/D37/K7)
- CheTai phat_tien: 8.000.000–10.000.000 đồng (nêu tại ND168-2024/D37/K4)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D37/K4"], "required_numbers": [{"value": 8000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}]}
```

### W-muc_phat-040 · tier A · ND168-2024/D27/K3

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D27/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 27. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô kinh doanh vận tải chở trẻ em mầm non, học sinh, xe ô tô kinh doanh vận tải kết hợp với hoạt động đưa đón trẻ em mầm non, học sinh
> 3. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với người điều khiển xe ô tô kinh doanh vận tải chở trẻ em mầm non, học sinh, xe ô tô kinh doanh vận tải kết hợp với hoạt động đưa đón trẻ em mầm non, học sinh thực hiện một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe không có thiết bị giám sát hành trình hoặc có lắp thiết bị giám sát hành trình nhưng không có tác dụng trong quá trình xe tham gia giao thông theo quy định hoặc làm sai lệch dữ liệu của thiết bị giám sát hành trình lắp trên xe ô tô;
> b) Điều khiển xe không có thiết bị ghi nhận hình ảnh trẻ em mầm non, học sinh hoặc không có thiết bị có chức năng cảnh báo, chống bỏ quên trẻ em trên xe hoặc không có thiết bị ghi nhận hình ảnh trẻ em mầm non, học sinh và thiết bị có chức năng cảnh báo, chống bỏ quên trẻ em trên xe;
> c) Điều khiển xe ô tô kinh doanh vận tải chở trẻ em mầm non, học sinh không có màu sơn theo quy định;
> d) Điều khiển xe ô tô kinh doanh vận tải chở trẻ em mầm non, học sinh, xe ô tô kinh doanh vận …

- CheTai phat_tien: 3.000.000–5.000.000 đồng (nêu tại ND168-2024/D27/K3)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D27/K4)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D27/K3"], "required_numbers": [{"value": 3000000, "unit": "vnd"}, {"value": 5000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}]}
```

### W-muc_phat-041 · tier A · ND168-2024/D23/K1

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D23/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 23. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển hàng hóa nguy hiểm
> 1. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với hành vi vận chuyển hàng hóa nguy hiểm mà không làm sạch hoặc không bóc (xóa) biểu trưng nguy hiểm trên phương tiện khi không tiếp tục vận chuyển loại hàng hóa đó.

- CheTai phat_tien: 1.000.000–2.000.000 đồng (nêu tại ND168-2024/D23/K1)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D23/K1"], "required_numbers": [{"value": 1000000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}]}
```

### W-muc_phat-042 · tier A · ND168-2024/D7/K3

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D7/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 7. Xử phạt, trừ điểm giấy phép lái của người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy vi phạm quy tắc giao thông đường bộ
> 3. Phạt tiền từ 600.000 đồng đến 800.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Chuyển hướng không quan sát hoặc không bảo đảm khoảng cách an toàn với xe phía sau hoặc không giảm tốc độ hoặc không có tín hiệu báo hướng rẽ hoặc có tín hiệu báo hướng rẽ nhưng không sử dụng liên tục trong quá trình chuyển hướng (trừ trường hợp điều khiển xe đi theo hướng cong của đoạn đường bộ ở nơi đường không giao nhau cùng mức); điều khiển xe rẽ trái tại nơi có biển báo hiệu có nội dung cấm rẽ trái đối với loại phương tiện đang điều khiển; điều khiển xe rẽ phải tại nơi có biển báo hiệu có nội dung cấm rẽ phải đối với loại phương tiện đang điều khiển;
> b) Chở theo từ 03 người trở lên trên xe;
> c) Dừng xe, đỗ xe trên cầu;
> d) Điều khiển xe không đi bên phải theo chiều đi của mình; đi không đúng phần đường, làn đường quy định (làn cùng chiều hoặc làn ngược chiều); điều khiển xe đi qua dải phân cách cố định ở giữa hai phần đường xe chạy;
> đ) Vượt bên phải trong trường hợp không …

- CheTai phat_tien: 600.000–800.000 đồng (nêu tại ND168-2024/D7/K3)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D7/K13/a)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D7/K3"], "required_numbers": [{"value": 600000, "unit": "vnd"}, {"value": 800000, "unit": "vnd"}, {"value": 2, "unit": "diem"}]}
```

### W-muc_phat-043 · tier A · ND168-2024/D26/K2

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D26/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
> 2. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với cá nhân, từ 2.000.000 đồng đến 4.000.000 đồng đối với tổ chức kinh doanh vận tải, dịch vụ hỗ trợ vận tải thực hiện một trong các hành vi vi phạm sau đây:
> a) Không đánh số thứ tự ghế ngồi, giường nằm trên xe ô tô chở hành khách theo quy định;
> b) Sử dụng xe ô tô kinh doanh vận tải hành khách theo tuyến cố định, xe ô tô kinh doanh vận tải hành khách bằng xe buýt không có chỗ ưu tiên cho người khuyết tật, người cao tuổi và phụ nữ mang thai theo quy định;
> c) Sử dụng xe ô tô kinh doanh vận tải hành khách không có hướng dẫn cho hành khách về an toàn giao thông, thoát hiểm khi xảy ra sự cố trên xe theo quy định;
> d) Không bố trí người áp tải trên xe vận chuyển hàng hóa nguy hiểm đối với những trường hợp quy định phải có người áp tải;
> đ) Không cấp lệnh vận chuyển, giấy vận tải cho lái xe hoặc cấp lệnh vận chuyển, giấy vận tải nhưng không đúng theo quy định (đối với loại xe quy định phải cấp lệnh vận chuyển, giấy vận tải);
> e) Sử dụng xe vận chuyển hàng hóa nguy hiểm mà không làm sạch hoặc không …

- CheTai tuoc_quyen: 1–3 tháng phù hiệu (nêu tại ND168-2024/D26/K12)
- CheTai phat_tien: 1.000.000–2.000.000 đồng (nêu tại ND168-2024/D26/K2)
- CheTai phat_tien: 2.000.000–4.000.000 đồng (nêu tại ND168-2024/D26/K2)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D26/K14/a)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D26/K2"], "required_numbers": [{"value": 1, "unit": "thang"}, {"value": 3, "unit": "thang"}, {"value": 1000000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}, {"value": 4000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}]}
```

### W-muc_phat-044 · tier A · ND168-2024/D39/K4

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D39/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 39. Xử phạt các hành vi vi phạm quy định về đào tạo, sát hạch lái xe
> 4. Phạt tiền từ 10.000.000 đồng đến 20.000.000 đồng đối với cơ sở đào tạo lái xe, trung tâm sát hạch lái xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Cơ sở đào tạo lái xe tổ chức tuyển sinh, đào tạo vượt quá lưu lượng quy định trong giấy phép đào tạo lái xe;
> b) Cơ sở đào tạo lái xe tổ chức đào tạo lái xe ngoài địa điểm được ghi trong giấy phép đào tạo lái xe:
> c) Cơ sở đào tạo lái xe không lưu trữ hoặc lưu trữ không đầy đủ hồ sơ theo quy định của 02 khóa đào tạo trở lên;
> d) Cơ sở đào tạo lái xe bố trí học viên tập lái trên xe tập lái vượt quá số lượng quy định;
> đ) Cơ sở đào tạo lái xe không có đủ hệ thống phòng học; phòng học không đủ trang thiết bị, mô hình học cụ;
> e) Cơ sở đào tạo lái xe không có đủ sân tập lái hoặc sân tập lái không đủ điều kiện theo quy định;
> g) Cơ sở đào tạo lái xe không có đủ số lượng xe tập lái các hạng để đáp ứng với lưu lượng đào tạo thực tế tại các thời điểm hoặc sử dụng xe tập lái không đúng hạng để dạy thực hành lái xe;
> h) Cơ sở đào tạo lái xe không có đủ thiết bị giám sát thời gian học lý thuyết, thời gian, quãng đường học thực hành lái xe của học viên hoặc có các thiết …

- CheTai phat_tien: 10.000.000–20.000.000 đồng (nêu tại ND168-2024/D39/K4)
- CheTai tuoc_quyen: 1–3 tháng giấy phép sát hạch (nêu tại ND168-2024/D39/K9/c)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D39/K4"], "required_numbers": [{"value": 10000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}, {"value": 1, "unit": "thang"}, {"value": 3, "unit": "thang"}]}
```

### W-muc_phat-045 · tier A · ND168-2024/D21/K11

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D21/K11#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
> 11. Phạt tiền từ 30.000.000 đồng đến 35.000.000 đồng đối với hành vi vi phạm quy định tại khoản 1, điểm đ khoản 8, khoản 10 Điều này mà gây tai nạn giao thông.

- CheTai phat_tien: 30.000.000–35.000.000 đồng (nêu tại ND168-2024/D21/K11)
- DiemGPLX: trừ 10 điểm (nêu tại ND168-2024/D21/K13/đ)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D21/K11"], "required_numbers": [{"value": 30000000, "unit": "vnd"}, {"value": 35000000, "unit": "vnd"}, {"value": 10, "unit": "diem"}]}
```

### W-muc_phat-046 · tier A · ND168-2024/D39/K5

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D39/K5#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 39. Xử phạt các hành vi vi phạm quy định về đào tạo, sát hạch lái xe
> 5. Phạt tiền từ 20.000.000 đồng đến 30.000.000 đồng đối với cơ sở đào tạo lái xe, trung tâm sát hạch lái xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Cơ sở đào tạo lái xe tổ chức tuyển sinh, đào tạo không đúng hạng giấy phép lái xe được phép đào tạo;
> b) Cơ sở đào tạo lái xe đào tạo không đúng nội dung, chương trình, giáo trình theo quy định;
> c) Cơ sở đào tạo lái xe xét hoàn thành khóa đào tạo hoặc cấp chứng chỉ sơ cấp hoặc cấp chứng chỉ đào tạo cho học viên sai quy định;
> d) Cơ sở đào tạo lái xe sử dụng biện pháp kỹ thuật, trang thiết bị ngoại vi, các biện pháp khác để can thiệp vào quá trình hoạt động làm sai lệch dữ liệu của thiết bị giám sát thời gian học lý thuyết, thời gian, quãng đường học thực hành lái xe;
> đ) Trung tâm sát hạch lái xe không lắp đủ camera giám sát phòng sát hạch lý thuyết, mô phỏng các tình huống giao thông, sân sát hạch theo quy định hoặc có lắp camera giám sát nhưng không hoạt động theo quy định;
> e) Trung tâm sát hạch lái xe có trên 50% số xe sát hạch lái xe trong tỉnh được cấp phép không bảo đảm điều, kiện để sát hạch theo quy định;
> g) Trung tâm sát hạch lái xe có trên 50% …

- CheTai phat_tien: 20.000.000–30.000.000 đồng (nêu tại ND168-2024/D39/K5)
- CheTai tuoc_quyen: 1–3 tháng giấy phép sát hạch (nêu tại ND168-2024/D39/K9/c)
- CheTai tuoc_quyen: 2–4 tháng giấy phép sát hạch (nêu tại ND168-2024/D39/K9/d)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D39/K5"], "required_numbers": [{"value": 20000000, "unit": "vnd"}, {"value": 30000000, "unit": "vnd"}, {"value": 1, "unit": "thang"}, {"value": 3, "unit": "thang"}, {"value": 2, "unit": "thang"}, {"value": 4, "unit": "thang"}]}
```

### W-muc_phat-047 · tier A · ND168-2024/D12/K11

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D12/K11#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 12. Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm khác về quy tắc giao thông đường bộ; sử dụng lòng đường, vỉa hè vào mục đích khác
> 11. Phạt tiền từ 6.000.000 đồng đến 8.000.000 đồng đối với cá nhân thực hiện một trong các hành vi vi phạm sau đây:
> a) Đặt, để chướng ngại vật, vật cản khác trái phép trên đường bộ; đổ chất gây trơn trượt trên đường bộ; đổ, xả thải, làm rơi vãi hóa chất, chất thải gây mất an toàn giao thông đường bộ;
> b) Xâm phạm tính mạng, sức khỏe, tài sản của người bị nạn, người gây tai nạn giao thông đường bộ hoặc người giúp đỡ, cứu chữa, đưa người bị nạn đi cấp cứu;
> c) Hủy hoại, làm hư hỏng, làm mất tác dụng thiết bị điều khiển, giám sát giao thông đường bộ, thiết bị thông minh hỗ trợ chỉ huy, điều khiển giao thông đường bộ.

- CheTai phat_tien: 6.000.000–8.000.000 đồng (nêu tại ND168-2024/D12/K11)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D12/K17)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D12/K11"], "required_numbers": [{"value": 6000000, "unit": "vnd"}, {"value": 8000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}]}
```

### W-muc_phat-048 · tier A · ND168-2024/D18/K4

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D18/K4#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 18. Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm quy định về điều kiện của người điều khiển xe cơ giới
> 4. Phạt tiền từ 400.000 đồng đến 600.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Người từ đủ 16 tuổi đến dưới 18 tuổi điều khiển xe mô tô và các loại xe tương tự xe mô tô;
> b) Người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô kinh doanh vận tải không mang theo chứng nhận bảo hiểm bắt buộc trách nhiệm dân sự của chủ xe cơ giới còn hiệu lực;
> c) Người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô không có chứng nhận bảo hiểm bắt buộc trách nhiệm dân sự của chủ xe cơ giới còn hiệu lực.

- CheTai phat_tien: 400.000–600.000 đồng (nêu tại ND168-2024/D18/K4)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D18/K4"], "required_numbers": [{"value": 400000, "unit": "vnd"}, {"value": 600000, "unit": "vnd"}]}
```

### W-muc_phat-049 · tier A · ND168-2024/D20/K6

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D20/K6#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
> 6. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Vận chuyển hàng hóa nguy hiểm, hàng độc hại, dễ cháy, dễ nổ, động vật, hàng có mùi hôi thối hoặc hàng hóa khác ảnh hưởng đến sức khỏe của hành khách trên xe;
> b) Chở người trên mui xe, trong khoang chở hành lý của xe;
> c) Đe dọa, xúc phạm, tranh giành, lôi kéo hành khách; đe dọa, cưỡng ép hành khách sử dụng dịch vụ ngoài ý muốn; chuyển tải, xuống khách hoặc các hành vi khác nhằm trốn tránh phát hiện xe chở quá tải, quá số người theo quy định của pháp luật;
> d) Điều khiển xe ô tô kinh doanh vận tải, xe vận tải nội bộ quá thời gian quy định tại khoản 1 Điều 64 của Luật Trật tự, an toàn giao thông đường bộ; không thực hiện đúng quy định về thời gian nghỉ giữa hai lần lái xe liên tục của người lái xe;
> đ) Điều khiển xe kinh doanh vận tải hành khách, xe vận tải nội bộ không lắp thiết bị giám sát hành trình của xe theo quy định hoặc có lắp thiết bị giám sát hành trình của xe nhưng thiết …

- CheTai phat_tien: 3.000.000–5.000.000 đồng (nêu tại ND168-2024/D20/K6)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D20/K10/a)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D20/K6"], "required_numbers": [{"value": 3000000, "unit": "vnd"}, {"value": 5000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}]}
```

### W-muc_phat-050 · tier A · ND168-2024/D29/K3a

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D29/K3a#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 29. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe cứu hộ giao thông đường bộ
> 3a. Phạt tiền từ 5.000.000 đồng đến 10.000.000 đồng đối với một trong các hành vi sau đây:
> a) Điều khiển xe ô tô cứu hộ giao thông đường bộ chở xe được cứu hộ mà vượt quá khối lượng cho phép chuyên chở của xe cứu hộ; kéo theo xe được cứu hộ mà vượt quá khối lượng cho phép kéo theo của xe cứu hộ được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe;
> b) Điều khiển xe ô tô cứu hộ giao thông đường bộ kéo theo xe không đúng đối tượng được cứu hộ theo quy định tại khoản 1 Điều 54 Luật Trật tự, an toàn giao thông đường bộ.

- CheTai phat_tien: 5.000.000–10.000.000 đồng (nêu tại ND168-2024/D29/K3a)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D29/K4)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D29/K3a"], "required_numbers": [{"value": 5000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}]}
```

### W-muc_phat-051 · tier A · ND168-2024/D26/K9

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D26/K9#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
> 9. Phạt tiền từ 20.000.000 đồng đến 40.000.000 đồng đối với đơn vị sản xuất, lắp ráp, nhập khẩu thiết bị giám sát hành trình của xe ô tô, đơn vị cung cấp dịch vụ liên quan đến giám sát hành trình, ghi nhận hình ảnh người lái xe thực hiện một trong các hành vi sau:
> a) Đơn vị sản xuất, lắp ráp, nhập khẩu thiết bị giám sát hành trình của xe ô tô không có nhân sự cho từng vị trí công việc theo quy định;
> b) Đơn vị sản xuất, lắp ráp, nhập khẩu thiết bị giám sát hành trình của xe ô tô không báo cáo về việc cập nhật, thay đổi phần mềm của thiết bị theo quy định.

- CheTai phat_tien: 20.000.000–40.000.000 đồng (nêu tại ND168-2024/D26/K9)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D26/K9"], "required_numbers": [{"value": 20000000, "unit": "vnd"}, {"value": 40000000, "unit": "vnd"}]}
```

### W-muc_phat-052 · tier A · ND168-2024/D22/K2

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D22/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 22. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển hàng siêu trường, siêu trọng
> 2. Phạt tiền từ 8.000.000 đồng đến 10.000.000 đồng đối với hành vi chở hàng siêu trường, siêu trọng có giấy phép lưu hành còn giá trị sử dụng nhưng kích thước bao ngoài của xe (sau khi đã xếp hàng lên xe) vượt quá quy định trong giấy phép lưu hành.

- BienPhapBoSung: buộc khôi phục lại tình trạng ban đầu đã bị thay đổi do hành vi vi phạm hành chính gây ra (nêu tại ND168-2024/D22/K4)
- CheTai phat_tien: 8.000.000–10.000.000 đồng (nêu tại ND168-2024/D22/K2)
- DiemGPLX: trừ 4 điểm (nêu tại ND168-2024/D22/K6/b)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D22/K2"], "required_numbers": [{"value": 8000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}, {"value": 4, "unit": "diem"}]}
```

### W-muc_phat-053 · tier A · ND168-2024/D9/K2

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D9/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 9. Xử phạt người điều khiển xe đạp, xe đạp máy, người điều khiển xe thô sơ khác vi phạm quy tắc giao thông đường bộ
> 2. Phạt tiền từ 150.000 đồng đến 250.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe đạp, xe đạp máy buông cả hai tay; chuyển hướng đột ngột trước đầu xe cơ giới đang chạy; dùng chân điều khiển xe đạp, xe đạp máy;
> b) Không chấp hành hiệu lệnh, chỉ dẫn của người điều khiển giao thông hoặc người kiểm soát giao thông;
> c) Người đang điều khiển xe hoặc chở người ngồi trên xe bám, kéo, đẩy xe khác, vật khác, mang vác vật cồng kềnh; điều khiển xe kéo theo xe khác, vật khác;
> d) Không nhường đường cho xe xin vượt khi có đủ điều kiện an toàn hoặc gây cản trở đối với xe cơ giới xin vượt, gây cản trở xe ưu tiên;
> đ) Không chấp hành hiệu lệnh của đèn tín hiệu giao thông.

- CheTai phat_tien: 150.000–250.000 đồng (nêu tại ND168-2024/D9/K2)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D9/K2"], "required_numbers": [{"value": 150000, "unit": "vnd"}, {"value": 250000, "unit": "vnd"}]}
```

### W-muc_phat-054 · tier A · ND168-2024/D6/K8

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D6/K8#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
> 8. Phạt tiền từ 16.000.000 đồng đến 18.000.000 đồng đối với người điều khiển xe thực hiện hành vi vi phạm gây tai nạn giao thông không dừng ngay phương tiện, không giữ nguyên hiện trường, không trợ giúp người bị nạn, không ở lại hiện trường hoặc không đến trình báo ngay với cơ quan công an, Ủy ban nhân dân nơi gần nhất.

- CheTai phat_tien: 16.000.000–18.000.000 đồng (nêu tại ND168-2024/D6/K8)
- DiemGPLX: trừ 6 điểm (nêu tại ND168-2024/D6/K16/c)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D6/K8"], "required_numbers": [{"value": 16000000, "unit": "vnd"}, {"value": 18000000, "unit": "vnd"}, {"value": 6, "unit": "diem"}]}
```

### W-muc_phat-055 · tier A · ND168-2024/D23/K4

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D23/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 23. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển hàng hóa nguy hiểm
> 4. Phạt tiền từ 6.000.000 đồng đến 8.000.000 đồng đối với hành vi vận chuyển hàng hóa nguy hiểm là thuốc nổ, khí đốt, xăng, dầu và các chất dễ cháy, nổ, chất rắn khử nhạy khác đi qua các công trình hầm có chiều dài từ 100 mét trở lên.

- BienPhapBoSung: buộc thực hiện các biện pháp khắc phục tình trạng ô nhiễm môi trường do vi phạm hành chính gây ra (nêu tại ND168-2024/D23/K6)
- CheTai phat_tien: 6.000.000–8.000.000 đồng (nêu tại ND168-2024/D23/K4)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D23/K7/a)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D23/K4"], "required_numbers": [{"value": 6000000, "unit": "vnd"}, {"value": 8000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}]}
```

### W-muc_phat-056 · tier A · ND168-2024/D7/K7

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D7/K7#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 7. Xử phạt, trừ điểm giấy phép lái của người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy vi phạm quy tắc giao thông đường bộ
> 7. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Đi ngược chiều của đường một chiều, đi ngược chiều trên đường có biển “Cấm đi ngược chiều”, trừ hành vi vi phạm quy định tại điểm b khoản này và các trường hợp xe ưu tiên đang đi làm nhiệm vụ khẩn cấp theo quy định; điều khiển xe đi trên vỉa hè, trừ trường hợp điều khiển xe đi qua vỉa hè để vào nhà, cơ quan;
> b) Điều khiển xe đi vào đường cao tốc, trừ xe phục vụ việc quản lý, bảo trì đường cao tốc;
> c) Không chấp hành hiệu lệnh của đèn tín hiệu giao thông;
> d) Không chấp hành hiệu lệnh, hướng dẫn của người điều khiển giao thông hoặc người kiểm soát giao thông;
> đ) Không nhường đường hoặc gây cản trở xe được quyền ưu tiên đang phát tín hiệu ưu tiên đi làm nhiệm vụ.

- CheTai phat_tien: 4.000.000–6.000.000 đồng (nêu tại ND168-2024/D7/K7)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D7/K13/a)
- DiemGPLX: trừ 4 điểm (nêu tại ND168-2024/D7/K13/b)
- DiemGPLX: trừ 6 điểm (nêu tại ND168-2024/D7/K13/c)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D7/K7"], "required_numbers": [{"value": 4000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}, {"value": 4, "unit": "diem"}, {"value": 6, "unit": "diem"}]}
```

### W-muc_phat-057 · tier A · ND168-2024/D6/K6

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D6/K6#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
> 6. Phạt tiền từ 6.000.000 đồng đến 8.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe chạy quá tốc độ quy định trên 20 km/h đến 35 km/h;
> b) Không nhường đường hoặc gây cản trở xe được quyền ưu tiên đang phát tín hiệu ưu tiên đi làm nhiệm vụ;
> c) Điều khiển xe trên đường mà trong máu hoặc hơi thở có nồng độ cồn nhưng chưa vượt quá 50 miligam/100 mililít máu hoặc chưa vượt quá 0,25 miligam/1 lít khí thở;
> d) Điều khiển xe đi trên vỉa hè, trừ trường hợp điều khiển xe đi qua vỉa hè để vào nhà, cơ quan.

- CheTai phat_tien: 6.000.000–8.000.000 đồng (nêu tại ND168-2024/D6/K6)
- DiemGPLX: trừ 4 điểm (nêu tại ND168-2024/D6/K16/b)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D6/K6"], "required_numbers": [{"value": 6000000, "unit": "vnd"}, {"value": 8000000, "unit": "vnd"}, {"value": 4, "unit": "diem"}]}
```

### W-muc_phat-058 · tier A · ND168-2024/D13/K2

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D13/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 13. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo), xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tư xe ô tô vi phạm quy định về điều kiện của phương tiện khi tham gia giao thông
> 2. Phạt tiền từ 400.000 đồng đến 600.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe không có đủ đèn chiếu sáng, đèn soi biển số, đèn báo hãm, đèn tín hiệu, cần gạt nước, gương chiếu hậu, dây đai an toàn, dụng cụ thoát hiểm, thiết bị chữa cháy, đồng hồ báo áp lực hơi, đồng hồ báo tốc độ của xe hoặc có những thiết bị đó nhưng không có tác dụng, không đúng tiêu chuẩn thiết kế (đối với loại xe được quy định phải có những thiết bị đó), trừ các hành vi vi phạm quy định tại điểm h khoản 3 Điều 20, điểm d khoản 4 Điều 26 của Nghị định này;
> b) Điều khiển xe không có còi hoặc có nhưng còi không có tác dụng;
> c) Điều khiển xe không có bộ phận giảm thanh, giảm khói hoặc có nhưng không có tác dụng, không bảo đảm quy chuẩn môi trường về khí thải, tiếng ồn.

- BienPhapBoSung: buộc lắp đầy đủ thiết bị hoặc thay thế thiết bị đủ tiêu chuẩn, quy chuẩn an toàn kỹ thuật hoặc khôi phục lại tính năng kỹ thuật của thiết bị theo quy định (nêu tại ND168-2024/D13/K11/a)
- BienPhapBoSung: buộc thực hiện đúng quy định về biển số hoặc khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND168-2024/D13/K11/a)
- CheTai phat_tien: 400.000–600.000 đồng (nêu tại ND168-2024/D13/K2)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D13/K2"], "required_numbers": [{"value": 400000, "unit": "vnd"}, {"value": 600000, "unit": "vnd"}]}
```

### W-muc_phat-059 · tier A · ND168-2024/D38/K1

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D38/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 38. Xử phạt người điều khiển phương tiện đăng ký hoạt động trong Khu kinh tế thương mại đặc biệt, Khu kinh tế cửa khẩu quốc tế
> 1. Phạt tiền từ 500.000 đồng đến 1.000.000 đồng đối với người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy thực hiện một trong các hành vi vi phạm sau đây:
> a) Không có tờ khai phương tiện vận tải đường bộ tạm nhập, tái xuất theo quy định;
> b) Điều khiển xe không có phù hiệu kiểm soát theo quy định hoặc có nhưng đã hết giá trị sử dụng hoặc sử dụng phù hiệu không do cơ quan có thẩm quyền cấp.

- BienPhapBoSung: buộc đưa phương tiện quay trở lại Khu kinh tế thương mại đặc biệt, Khu kinh tế cửa khẩu quốc tế (nêu tại ND168-2024/D38/K4)
- CheTai phat_tien: 500.000–1.000.000 đồng (nêu tại ND168-2024/D38/K1)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D38/K1"], "required_numbers": [{"value": 500000, "unit": "vnd"}, {"value": 1000000, "unit": "vnd"}]}
```

### W-muc_phat-060 · tier A · ND168-2024/D6/K7

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D6/K7#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
> 7. Phạt tiền từ 12.000.000 đồng đến 14.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe chạy quá tốc độ quy định trên 35 km/h;
> b) Điều khiển xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ đi vào đường cao tốc;
> c) Dừng xe, đỗ xe trên đường cao tốc không đúng nơi quy định; không có báo hiệu bằng đèn khẩn cấp khi gặp sự cố kỹ thuật hoặc bất khả kháng khác buộc phải dừng xe, đỗ xe ở làn dừng xe khẩn cấp hoặc dải dừng xe khẩn cấp trên đường cao tốc; không có báo hiệu bằng đèn khẩn cấp, không đặt biển cảnh báo “Chú ý xe đỗ” (hoặc đèn cảnh báo) về phía sau xe khoảng cách tối thiểu 150 mét khi dừng xe, đỗ xe trong trường hợp gặp sự cố kỹ thuật hoặc bất khả kháng khác buộc phải dừng xe, đỗ xe trên một phần làn đường xe chạy trên đường cao tốc.

- CheTai phat_tien: 12.000.000–14.000.000 đồng (nêu tại ND168-2024/D6/K7)
- DiemGPLX: trừ 4 điểm (nêu tại ND168-2024/D6/K16/b)
- DiemGPLX: trừ 6 điểm (nêu tại ND168-2024/D6/K16/c)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D6/K7"], "required_numbers": [{"value": 12000000, "unit": "vnd"}, {"value": 14000000, "unit": "vnd"}, {"value": 4, "unit": "diem"}, {"value": 6, "unit": "diem"}]}
```

### W-muc_phat-061 · tier A · ND168-2024/D6/K13

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D6/K13#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
> 13. Phạt tiền từ 50.000.000 đồng đến 70.000.000 đồng đối với người điều khiển xe thực hiện hành vi vi phạm quy định tại khoản 12 Điều này mà gây tai nạn giao thông.

- CheTai phat_tien: 50.000.000–70.000.000 đồng (nêu tại ND168-2024/D6/K13)
- CheTai tuoc_quyen: 22–24 tháng giấy phép lái xe (nêu tại ND168-2024/D6/K15/c)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D6/K13"], "required_numbers": [{"value": 50000000, "unit": "vnd"}, {"value": 70000000, "unit": "vnd"}, {"value": 22, "unit": "thang"}, {"value": 24, "unit": "thang"}]}
```

### W-muc_phat-062 · tier A · ND168-2024/D29/K1

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D29/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 29. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe cứu hộ giao thông đường bộ
> 1. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với hành vi vi phạm điều khiển xe ô tô cứu hộ giao thông đường bộ không lắp thiết bị ghi nhận hình ảnh người lái xe hoặc có lắp thiết bị ghi nhận hình ảnh người lái xe nhưng không có tác dụng trong quá trình xe tham gia giao thông theo quy định hoặc làm sai lệch dữ liệu của thiết bị ghi nhận hình ảnh người lái xe lắp trên xe ô tô.

- CheTai phat_tien: 1.000.000–2.000.000 đồng (nêu tại ND168-2024/D29/K1)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D29/K1"], "required_numbers": [{"value": 1000000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}]}
```

### W-muc_phat-063 · tier A · ND168-2024/D21/K10

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D21/K10#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
> 10. Phạt tiền từ 18.000.000 đồng đến 22.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Vận chuyển hàng hóa là phương tiện vận tải, máy móc, thiết bị kỹ thuật, hàng dạng trụ không chằng buộc hoặc chằng buộc không theo quy định (trừ việc vận chuyển máy móc khổ lớn (quá khổ) trên phương tiện chuyên dùng và phải có giấy phép lưu hành trên đường bộ);
> b) Chở công-ten-nơ trên xe (kể cả sơ mi rơ moóc) mà không sử dụng cơ cấu khoá hãm công-ten-nơ với xe hoặc có sử dụng cơ cấu khoá hãm nhưng công-ten- nơ vẫn bị xê dịch trong quá trình vận chuyển.

- CheTai phat_tien: 18.000.000–22.000.000 đồng (nêu tại ND168-2024/D21/K10)
- DiemGPLX: trừ 4 điểm (nêu tại ND168-2024/D21/K13/b)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D21/K10"], "required_numbers": [{"value": 18000000, "unit": "vnd"}, {"value": 22000000, "unit": "vnd"}, {"value": 4, "unit": "diem"}]}
```

### W-muc_phat-064 · tier B · ND336-2025/D10/K3

Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)

`ND336-2025/D10/K3#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 10. Xử phạt các hành vi vi phạm về thanh toán điện tử giao thông đường bộ, hoạt động trạm thu phí đường bộ
> 3. Phạt tiền từ 10.000.000 đồng đến 20.000.000 đồng đối với cá nhân, từ 20.000.000 đồng đến 40.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
> a) Không thực hiện đúng quy trình quản lý, vận hành trạm thu phí theo quy định để xảy ra tai nạn giao thông đối với các phương tiện khi phương tiện tham gia giao thông qua trạm thu phí, trừ hành vi vi phạm quy định tại điểm c khoản 5 Điều này;
> b) Phát hành chứng từ thu tiền sử dụng đường bộ không đúng đối tượng, đúng giá trị cho từng đối tượng phải trả tại trạm thu phí;
> c) Xâm nhập hoặc tìm cách xâm nhập hệ thống thanh toán điện tử giao thông đường bộ;
> d) Phá hoại, đánh cắp dữ liệu hệ thống thanh toán điện tử giao thông đường bộ;
> đ) Làm thay đổi trái phép chương trình phần mềm, dữ liệu điện tử sử dụng trong thanh toán điện tử giao thông đường bộ.

- BienPhapBoSung: buộc nộp lại số lợi bất hợp pháp (nếu có) có được do thực hiện vi phạm hành chính (nêu tại ND336-2025/D10/K7/a)
- BienPhapBoSung: buộc khôi phục lại tình trạng ban đầu đã bị thay đổi do hành vi vi phạm hành chính gây ra (nêu tại ND336-2025/D10/K7/b)
- CheTai phat_tien: 10.000.000–20.000.000 đồng (nêu tại ND336-2025/D10/K3)
- CheTai phat_tien: 20.000.000–40.000.000 đồng (nêu tại ND336-2025/D10/K3)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "B", "answer": "", "gold_units": ["ND336-2025/D10/K3"], "required_numbers": [{"value": 10000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}, {"value": 40000000, "unit": "vnd"}]}
```

### W-muc_phat-065 · tier B · ND336-2025/D9/K1

Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)

`ND336-2025/D9/K1#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 9. Xử phạt các hành vi vi phạm quy định về quản lý, khai thác, bảo trì, bảo vệ kết cấu hạ tầng đường bộ
> 1. Cảnh cáo hoặc phạt tiền từ 100.000 đồng đến 200.000 đồng đối với cá nhân thực hiện một trong các hành vi vi phạm sau đây:
> a) Chăn thả gia súc ở mái đường;
> b) Buộc gia súc vào cọc tiêu, biển báo, rào chắn, các công trình phụ trợ của kết cấu hạ tầng đường bộ.

- CheTai phat_tien: 100.000–200.000 đồng (nêu tại ND336-2025/D9/K1)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "B", "answer": "", "gold_units": ["ND336-2025/D9/K1"], "required_numbers": [{"value": 100000, "unit": "vnd"}, {"value": 200000, "unit": "vnd"}]}
```

### W-muc_phat-066 · tier B · ND336-2025/D15/K1

Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)

`ND336-2025/D15/K1#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 15. Xử phạt hành vi vi phạm về dịch vụ cho thuê phương tiện
> 1. Phạt tiền từ 8.000.000 đồng đến 10.000.000 đồng đối với cá nhân, từ 16.000.000 đồng đến 20.000.000 đồng đối với tổ chức kinh doanh dịch vụ cho thuê phương tiện thực hiện hành vi vi phạm không ký kết hợp đồng cho thuê phương tiện để tự lái với người thuê.

- CheTai phat_tien: 8.000.000–10.000.000 đồng (nêu tại ND336-2025/D15/K1)
- CheTai phat_tien: 16.000.000–20.000.000 đồng (nêu tại ND336-2025/D15/K1)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "B", "answer": "", "gold_units": ["ND336-2025/D15/K1"], "required_numbers": [{"value": 8000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}, {"value": 16000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}]}
```

### W-muc_phat-067 · tier B · ND336-2025/D12/K4

Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)

`ND336-2025/D12/K4#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 12. Xử phạt các hành vi vi phạm quy định về vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
> 4. Phạt tiền từ 5.000.000 đồng đến 10.000.000 đồng đối với cá nhân, từ 10.000.000 đồng đến 20.000.000 đồng đối với tổ chức kinh doanh vận tải, dịch vụ hỗ trợ vận tải thực hiện một trong các hành vi vi phạm sau đây:
> a) Thực hiện công bố bến xe hàng, trạm dừng nghỉ không đúng quy định; không thực hiện thủ tục công bố lại bến xe khách, bến xe hàng, trạm dừng nghỉ theo quy định;
> b) Không có bộ phận quản lý an toàn theo quy định hoặc có nhưng bộ phận này không thực hiện đầy đủ các nhiệm vụ theo quy định;
> c) Không lập hoặc có lập nhưng không cập nhật đầy đủ, chính xác lý lịch phương tiện, lý lịch hành nghề của lái xe theo quy định;
> d) Sử dụng xe taxi chở hành khách không lắp đồng hồ tính tiền (đối với loại xe đăng ký sử dụng đồng hồ tính tiền) hoặc lắp đồng hồ tính tiền không đúng quy định; không có thiết bị in hóa đơn (phiếu thu tiền) được kết nối với đồng hồ tính tiền theo quy định hoặc có nhưng không sử dụng được hoặc in ra phiếu thu tiền nhưng không có đầy đủ các thông tin theo quy định;
> đ) Sử dụng xe taxi chở hành khách mà trên xe không có thiết bị để kết nối trực tiếp với hành khách …

- CheTai phat_tien: 5.000.000–10.000.000 đồng (nêu tại ND336-2025/D12/K4)
- CheTai phat_tien: 10.000.000–20.000.000 đồng (nêu tại ND336-2025/D12/K4)
- CheTai tuoc_quyen: 1–3 tháng giấy phép kinh doanh vận tải (nêu tại ND336-2025/D12/K8/b)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "B", "answer": "", "gold_units": ["ND336-2025/D12/K4"], "required_numbers": [{"value": 5000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}, {"value": 1, "unit": "thang"}, {"value": 3, "unit": "thang"}]}
```

### W-muc_phat-068 · tier B · ND336-2025/D7/K1

Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)

`ND336-2025/D7/K1#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 7. Xử phạt hành vi vi phạm quy định về đào tạo thẩm tra viên, điều kiện kinh doanh dịch vụ thẩm tra an toàn giao thông đường bộ
> 1. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng đối với cơ sở đào tạo thẩm tra viên an toàn giao thông đường bộ thực hiện một trong các hành vi vi phạm sau đây:
> a) Không có đủ thiết bị nghe, nhìn theo quy định;
> b) Không có đủ máy tính, thiết bị đo độ phản quang của báo hiệu đường bộ theo quy định;
> c) Không có số giảng viên cơ hữu đảm nhận giảng dạy theo quy định;
> d) Sử dụng giảng viên tham gia giảng dạy không đáp ứng điều kiện về tiêu chuẩn theo quy định.

- CheTai phat_tien: 4.000.000–6.000.000 đồng (nêu tại ND336-2025/D7/K1)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "B", "answer": "", "gold_units": ["ND336-2025/D7/K1"], "required_numbers": [{"value": 4000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}]}
```

### W-muc_phat-069 · tier B · ND336-2025/D10/K1

Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)

`ND336-2025/D10/K1#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 10. Xử phạt các hành vi vi phạm về thanh toán điện tử giao thông đường bộ, hoạt động trạm thu phí đường bộ
> 1. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với cá nhân, từ 6.000.000 đồng đến 10.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
> a) Tự ý chuyển thẻ đầu cuối từ phương tiện này sang phương tiện khác;
> b) Phá hủy, làm giả, xoá dữ liệu hoặc can thiệp nội dung thẻ đầu cuối;
> c) Mở hoặc duy trì tài khoản giao thông nặc danh, mạo danh.

- CheTai phat_tien: 3.000.000–5.000.000 đồng (nêu tại ND336-2025/D10/K1)
- CheTai phat_tien: 6.000.000–10.000.000 đồng (nêu tại ND336-2025/D10/K1)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "B", "answer": "", "gold_units": ["ND336-2025/D10/K1"], "required_numbers": [{"value": 3000000, "unit": "vnd"}, {"value": 5000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}]}
```

### W-muc_phat-070 · tier B · ND336-2025/D5/K4

Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)

`ND336-2025/D5/K4#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 5. Xử phạt các hành vi vi phạm quy định về sử dụng, khai thác trong phạm vi đất dành cho kết cấu hạ tầng đường bộ
> 4. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng đối với cá nhân, từ 8.000.000 đồng đến 10.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
> a) Đổ, để trái phép vật liệu, chất phế thải trong hành lang an toàn đường bộ;
> b) Tự ý đào, đắp, san, lấp mặt bằng trong phạm vi đất dành cho kết cấu hạ tầng đường bộ;
> c) Tự ý gắn, treo, lắp đặt, để vào công trình báo hiệu đường bộ nội dung không liên quan tới ý nghĩa, mục đích của báo hiệu đường bộ, làm sai lệch hoặc mất tác dụng của báo hiệu đường bộ;
> d) Dựng rạp, lều quán, công trình khác trái phép trong khu vực đô thị tại hầm đường bộ, cầu vượt, hầm cho người đi bộ, gầm cầu vượt, trừ hành vi vi phạm quy định tại điểm a khoản 6 Điều này;
> đ) Không dành lối thoát nước thích hợp hoặc cản trở, ngăn chặn hệ thống thoát nước từ công trình thuộc kết cấu hạ tầng đường bộ theo quy định;
> e) Phá dỡ biển quảng cáo, các bộ phận của biển quảng cáo làm ảnh hưởng đến kết cấu hạ tầng đường bộ.

- BienPhapBoSung: buộc thu dọn rác thải, chất phế thải, vật liệu (nêu tại ND336-2025/D5/K7/d)
- BienPhapBoSung: buộc khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND336-2025/D5/K7/e)
- BienPhapBoSung: buộc tháo dỡ vật gắn, treo, lắp vào công trình báo hiệu đường bộ và khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND336-2025/D5/K7/g)
- BienPhapBoSung: buộc phá dỡ công trình, phần công trình xây dựng không có giấy phép hoặc xây dựng không đúng với giấy phép và khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND336-2025/D5/K7/đ)
- CheTai phat_tien: 4.000.000–6.000.000 đồng (nêu tại ND336-2025/D5/K4)
- CheTai phat_tien: 8.000.000–10.000.000 đồng (nêu tại ND336-2025/D5/K4)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "B", "answer": "", "gold_units": ["ND336-2025/D5/K4"], "required_numbers": [{"value": 4000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}, {"value": 8000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}]}
```

### W-muc_phat-071 · tier B · ND336-2025/D8/K5

Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)

`ND336-2025/D8/K5#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 8. Xử phạt các hành vi vi phạm quy định về thi công trong phạm vi bảo vệ kết cấu hạ tầng đường bộ
> 5. Phạt tiền từ 10.000.000 đồng đến 15.000.000 đồng đối với cá nhân, từ 20.000.000 đồng đến 30.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
> a) Thi công công trình trên đường đô thị không thực hiện đúng thời gian theo giấy phép thi công hoặc văn bản chấp thuận;
> b) Thi công trên đường bộ đang khai thác không thực hiện đầy đủ biện pháp tổ chức giao thông để xảy ra tai nạn giao thông;
> c) Thi công trên đường bộ đang khai thác không bố trí báo hiệu, rào chắn tạm thời tại nơi thi công theo giấy phép thi công hoặc văn bản chấp thuận của cơ quan có thẩm quyền;
> d) Không thực hiện việc di dời công trình khi cơ quan quản lý đường bộ có thẩm quyền, người quản lý, sử dụng đường bộ yêu cầu theo quy định;
> đ) Không thực hiện việc di dời công trình khi công trình ảnh hưởng đến an toàn giao thông đường bộ, an toàn công trình đường bộ mà không có biện pháp khắc phục;
> e) Không bàn giao công trình, hồ sơ hoàn thành công trình, quy trình bảo trì theo quy định sau khi hoàn thành xây dựng công trình đường bộ để bồi hoàn;
> g) Không hoàn trả hoặc hoàn trả kết cấu hạ tầng …

- CheTai phat_tien: 10.000.000–15.000.000 đồng (nêu tại ND336-2025/D8/K5)
- CheTai phat_tien: 20.000.000–30.000.000 đồng (nêu tại ND336-2025/D8/K5)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "B", "answer": "", "gold_units": ["ND336-2025/D8/K5"], "required_numbers": [{"value": 10000000, "unit": "vnd"}, {"value": 15000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}, {"value": 30000000, "unit": "vnd"}]}
```

### W-muc_phat-072 · tier B · ND336-2025/D8/K4

Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)

`ND336-2025/D8/K4#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 8. Xử phạt các hành vi vi phạm quy định về thi công trong phạm vi bảo vệ kết cấu hạ tầng đường bộ
> 4. Phạt tiền từ 7.000.000 đồng đến 10.000.000 đồng đối với cá nhân, từ 14.000.000 đồng đến 20.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
> a) Thi công trên đường bộ đang khai thác không đặt đèn cảnh báo giao thông và chiếu sáng ban đêm;
> b) Thi công trên đường bộ đang khai thác có bố trí báo hiệu, rào chắn tạm thời tại nơi thi công nhưng không đầy đủ theo giấy phép thi công hoặc văn bản chấp thuận của cơ quan có thẩm quyền, trừ hành vi vi phạm quy định tại điểm c khoản 5 Điều này;
> c) Thi công công trình trong phạm vi đất dành cho kết cấu hạ tầng đường bộ không có giấy phép thi công hoặc không có văn bản chấp thuận của cơ quan có thẩm quyền theo quy định;
> d) Thi công công trình trên đường bộ đang khai thác không đúng giấy phép thi công gây hư hỏng, hủy hoại công trình đường bộ đang khai thác.

- BienPhapBoSung: buộc phá dỡ công trình, phần công trình xây dựng không có giấy phép hoặc xây dựng không đúng với giấy phép và khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND336-2025/D8/K8/b)
- CheTai phat_tien: 7.000.000–10.000.000 đồng (nêu tại ND336-2025/D8/K4)
- CheTai phat_tien: 14.000.000–20.000.000 đồng (nêu tại ND336-2025/D8/K4)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "B", "answer": "", "gold_units": ["ND336-2025/D8/K4"], "required_numbers": [{"value": 7000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}, {"value": 14000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}]}
```

### W-muc_phat-073 · tier B · ND336-2025/D7/K3

Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)

`ND336-2025/D7/K3#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 7. Xử phạt hành vi vi phạm quy định về đào tạo thẩm tra viên, điều kiện kinh doanh dịch vụ thẩm tra an toàn giao thông đường bộ
> 3. Phạt tiền từ 20.000.000 đồng đến 30.000.000 đồng đối với tổ chức kinh doanh dịch vụ thẩm tra an toàn giao thông đường bộ thực hiện một trong các hành vi vi phạm sau đây:
> a) Không độc lập với đơn vị thi công, tổ chức tư vấn thiết kế theo quy định;
> b) Sử dụng người không có chứng chỉ thẩm tra viên an toàn giao thông đường bộ hoặc có chứng chỉ nhưng không còn giá trị sử dụng để thẩm tra an toàn giao thông đường bộ;
> c) Không đáp ứng điều kiện về năng lực khi thẩm tra đối với dự án nhóm C, công trình đường bộ đang khai thác theo quy định.

- CheTai phat_tien: 20.000.000–30.000.000 đồng (nêu tại ND336-2025/D7/K3)
- CheTai dinh_chi: 1–3 tháng thẩm tra an toàn giao thông đường bộ (nêu tại ND336-2025/D7/K5/b)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "B", "answer": "", "gold_units": ["ND336-2025/D7/K3"], "required_numbers": [{"value": 20000000, "unit": "vnd"}, {"value": 30000000, "unit": "vnd"}, {"value": 1, "unit": "thang"}, {"value": 3, "unit": "thang"}]}
```

### W-muc_phat-074 · tier B · ND336-2025/D10/K4

Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)

`ND336-2025/D10/K4#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 10. Xử phạt các hành vi vi phạm về thanh toán điện tử giao thông đường bộ, hoạt động trạm thu phí đường bộ
> 4. Phạt tiền từ 30.000.000 đồng đến 50.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
> a) Không thực hiện báo cáo doanh thu hoặc báo cáo không đầy đủ, không đúng thời gian theo quy định;
> b) Không thực hiện công khai số thu hàng ngày, số tiền các phương tiện còn nợ tại từng trạm thu phí;
> c) Thay đổi mức thu tiền sử dụng đường bộ khi chưa có chấp thuận bằng văn bản của cơ quan nhà nước có thẩm quyền;
> d) Không thực hiện việc bảo trì tài sản của trạm thu phí; tự ý tháo dỡ, thanh lý, nhượng bán tài sản của trạm thu phí; không thực hiện việc hiệu chuẩn, kiểm định đối với nhóm thiết bị cần phải thực hiện công tác hiệu chuẩn, kiểm định theo quy định.

- BienPhapBoSung: buộc nộp lại số lợi bất hợp pháp (nếu có) có được do thực hiện vi phạm hành chính (nêu tại ND336-2025/D10/K7/a)
- CheTai phat_tien: 30.000.000–50.000.000 đồng (nêu tại ND336-2025/D10/K4)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "B", "answer": "", "gold_units": ["ND336-2025/D10/K4"], "required_numbers": [{"value": 30000000, "unit": "vnd"}, {"value": 50000000, "unit": "vnd"}]}
```

### W-muc_phat-075 · tier B · ND336-2025/D9/K4

Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)

`ND336-2025/D9/K4#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 9. Xử phạt các hành vi vi phạm quy định về quản lý, khai thác, bảo trì, bảo vệ kết cấu hạ tầng đường bộ
> 4. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với cá nhân, từ 6.000.000 đồng đến 10.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
> a) Làm hư hỏng hoặc làm mất tác dụng của hệ thống thoát nước đường bộ;
> b) Tự ý tháo dỡ, di chuyển, điều chỉnh, làm hư hỏng, làm sai mục đích sử dụng hoặc làm sai lệch biển báo hiệu, đèn tín hiệu giao thông, rào chắn, cọc tiêu, cột cây số, vạch kẻ đường, tường bảo vệ, hàng rào hộ lan, mốc chỉ giới, cọc mốc giải phóng mặt bằng và các báo hiệu đường bộ khác;
> c) Tự ý đập phá, tháo dỡ bó vỉa hè hoặc sửa chữa, cải tạo vỉa hè trái phép.

- BienPhapBoSung: buộc khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND336-2025/D9/K6/b)
- CheTai phat_tien: 3.000.000–5.000.000 đồng (nêu tại ND336-2025/D9/K4)
- CheTai phat_tien: 6.000.000–10.000.000 đồng (nêu tại ND336-2025/D9/K4)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "B", "answer": "", "gold_units": ["ND336-2025/D9/K4"], "required_numbers": [{"value": 3000000, "unit": "vnd"}, {"value": 5000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}]}
```

### W-muc_phat-076 · tier B · ND336-2025/D12/K1

Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)

`ND336-2025/D12/K1#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 12. Xử phạt các hành vi vi phạm quy định về vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
> 1. Phạt tiền từ 500.000 đồng đến 1.000.000 đồng đối với cá nhân, từ 1.000.000 đồng đến 2.000.000 đồng đối với tổ chức thực hiện hành vi vi phạm không niêm yết nội quy, giá dịch vụ, tên và số điện thoại cơ quan quản lý nhà nước có thẩm quyền tại bãi đỗ xe theo quy định.

- CheTai phat_tien: 500.000–1.000.000 đồng (nêu tại ND336-2025/D12/K1)
- CheTai phat_tien: 1.000.000–2.000.000 đồng (nêu tại ND336-2025/D12/K1)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "B", "answer": "", "gold_units": ["ND336-2025/D12/K1"], "required_numbers": [{"value": 500000, "unit": "vnd"}, {"value": 1000000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}]}
```

### W-muc_phat-077 · tier B · ND336-2025/D9/K3

Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)

`ND336-2025/D9/K3#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 9. Xử phạt các hành vi vi phạm quy định về quản lý, khai thác, bảo trì, bảo vệ kết cấu hạ tầng đường bộ
> 3. Phạt tiền từ 6.000.000 đồng đến 8.000.000 đồng đối với tổ chức được giao quản lý, khai thác, bảo trì kết cấu hạ tầng giao thông đường bộ thực hiện một trong các hành vi vi phạm sau đây:
> a) Không bổ sung hoặc sửa chữa kịp thời theo quy định biển báo nguy hiểm, biển báo cấm, biển hiệu lệnh đã bị mất, bị hư hỏng mất tác dụng; không có biện pháp khắc phục kịp thời theo quy định các hư hỏng của công trình đường bộ gây mất an toàn giao thông;
> b) Không phát hiện hoặc không có biện pháp ngăn chặn, báo cáo kịp thời các hành vi lấn chiếm, sử dụng trái phép đất hành lang an toàn giao thông đường bộ, đất của đường bộ;
> c) Không cắm cột thủy chí ở hai đầu đường tràn, ngầm;
> d) Không có biện pháp cảnh báo, điều tiết giao thông hoặc không có biện pháp ngăn chặn phương tiện qua đoạn đường bị ngập nước sâu và lưu tốc dòng chảy mạnh.

- BienPhapBoSung: buộc bổ sung, sửa chữa các biển báo hiệu bị mất, bị hư hỏng (nêu tại ND336-2025/D9/K6/a)
- CheTai phat_tien: 6.000.000–8.000.000 đồng (nêu tại ND336-2025/D9/K3)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "B", "answer": "", "gold_units": ["ND336-2025/D9/K3"], "required_numbers": [{"value": 6000000, "unit": "vnd"}, {"value": 8000000, "unit": "vnd"}]}
```

### W-muc_phat-078 · tier B · ND336-2025/D14/K2

Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)

`ND336-2025/D14/K2#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 14. Xử phạt các hành vi vi phạm về vận tải nội bộ
> 2. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với cá nhân, từ 6.000.000 đồng đến 10.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
> a) Không tổ chức thực hiện hoặc có tổ chức thực hiện nhưng không đầy đủ các nội dung về công tác quản lý an toàn giao thông theo quy định, trừ hành vi vi phạm quy định tại điểm b khoản này;
> b) Không theo dõi, giám sát hoạt động của lái xe, phương tiện trong suốt quá trình hoạt động vận tải nội bộ;
> c) Sử dụng xe ô tô chở người có giường nằm hai tầng để hoạt động trên các tuyến đường cấp V và cấp VI miền núi;
> d) Sử dụng xe vận tải nội bộ để kinh doanh vận tải hành khách, hàng hóa;
> đ) Sử dụng xe vận tải nội bộ để vận chuyển người, hàng hóa không đúng đối tượng theo quy định;
> e) Sử dụng xe ô tô thuộc sở hữu của thành viên hợp tác xã để vận tải nội bộ mà không có hợp đồng dịch vụ giữa thành viên với hợp tác xã theo quy định hoặc sử dụng xe ô tô không thuộc quyền sở hữu hoặc quyền sử dụng hợp pháp theo quy định.

- CheTai phat_tien: 3.000.000–5.000.000 đồng (nêu tại ND336-2025/D14/K2)
- CheTai phat_tien: 6.000.000–10.000.000 đồng (nêu tại ND336-2025/D14/K2)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "B", "answer": "", "gold_units": ["ND336-2025/D14/K2"], "required_numbers": [{"value": 3000000, "unit": "vnd"}, {"value": 5000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}]}
```

### W-muc_phat-079 · tier B · ND336-2025/D5/K5

Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)

`ND336-2025/D5/K5#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 5. Xử phạt các hành vi vi phạm quy định về sử dụng, khai thác trong phạm vi đất dành cho kết cấu hạ tầng đường bộ
> 5. Phạt tiền từ 10.000.000 đồng đến 15.000.000 đồng đối với cá nhân, từ 20.000.000 đồng đến 30.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
> a) Xây dựng, lắp đặt biển quảng cáo trong phạm vi hành lang an toàn đường bộ mà không có văn bản chấp thuận theo quy định, trừ hành vi vi phạm quy định tại điểm d khoản 6 Điều này;
> b) Không thực hiện việc tháo dỡ biển quảng cáo, các bộ phận của biển quảng cáo khi có yêu cầu của cơ quan quản lý đường bộ, người quản lý, sử dụng đường bộ;
> c) Không xóa bỏ, đóng điểm đấu nối tạm thời khi hết thời hạn đấu nối tạm;
> d) Không hoàn trả nguyên trạng hành lang an toàn đường bộ; không sửa chữa, bổ sung kết cấu hạ tầng đường bộ bị ảnh hưởng do việc thực hiện đấu nối tạm thời.

- BienPhapBoSung: buộc phá dỡ công trình, phần công trình xây dựng không có giấy phép hoặc xây dựng không đúng với giấy phép và khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND336-2025/D5/K7/đ)
- CheTai phat_tien: 10.000.000–15.000.000 đồng (nêu tại ND336-2025/D5/K5)
- CheTai phat_tien: 20.000.000–30.000.000 đồng (nêu tại ND336-2025/D5/K5)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "B", "answer": "", "gold_units": ["ND336-2025/D5/K5"], "required_numbers": [{"value": 10000000, "unit": "vnd"}, {"value": 15000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}, {"value": 30000000, "unit": "vnd"}]}
```

### W-muc_phat-080 · tier B · ND336-2025/D15/K3

Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)

`ND336-2025/D15/K3#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 15. Xử phạt hành vi vi phạm về dịch vụ cho thuê phương tiện
> 3. Phạt tiền từ 28.000.000 đồng đến 30.000.000 đồng đối với cá nhân, từ 56.000.000 đồng đến 60.000.000 đồng đối với tổ chức kinh doanh dịch vụ cho thuê phương tiện thực hiện hành vi vi phạm cho thuê phương tiện khi người thuê phương tiện để tự lái không có giấy phép lái xe đang còn điểm, còn hiệu lực phù hợp với loại xe cho thuê.

- CheTai phat_tien: 28.000.000–30.000.000 đồng (nêu tại ND336-2025/D15/K3)
- CheTai phat_tien: 56.000.000–60.000.000 đồng (nêu tại ND336-2025/D15/K3)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "B", "answer": "", "gold_units": ["ND336-2025/D15/K3"], "required_numbers": [{"value": 28000000, "unit": "vnd"}, {"value": 30000000, "unit": "vnd"}, {"value": 56000000, "unit": "vnd"}, {"value": 60000000, "unit": "vnd"}]}
```

## tru_diem — số điểm bị trừ trên giấy phép lái xe

### W-tru_diem-001 · tier A · ND168-2024/D13/K7

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D13/K7#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 13. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo), xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tư xe ô tô vi phạm quy định về điều kiện của phương tiện khi tham gia giao thông
> 7. Phạt tiền từ 10.000.000 đồng đến 12.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe đăng ký tạm thời, xe có phạm vi hoạt động hạn chế hoạt động quá phạm vi, tuyến đường, thời hạn cho phép;
> b) Điều khiển xe (kể cả rơ moóc và sơ mi rơ moóc) không gắn biển số (đối với loại xe có quy định phải gắn biển số).

- CheTai phat_tien: 10.000.000–12.000.000 đồng (nêu tại ND168-2024/D13/K7)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D13/K13/a)
- DiemGPLX: trừ 6 điểm (nêu tại ND168-2024/D13/K13/b)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D13/K7"], "required_numbers": [{"value": 10000000, "unit": "vnd"}, {"value": 12000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}, {"value": 6, "unit": "diem"}]}
```

### W-tru_diem-002 · tier A · ND168-2024/D26/K14

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D26/K14#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
> 14. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
> a) Thực hiện hành vi quy định tại điểm đ khoản 2; điểm b, điểm c, điểm d khoản 6; điểm b, điểm c, điểm e, điểm i khoản 7 Điều này trong trường hợp cá nhân kinh doanh vận tải là người trực tiếp điều khiển phương tiện còn bị trừ điểm giấy phép lái xe 02 điểm;
> b) Thực hiện hành vi quy định tại điểm c khoản 8 Điều này trong trường hợp cá nhân kinh doanh vận tải là người trực tiếp điều khiển phương tiện còn bị trừ điểm giấy phép lái xe 06 điểm.

- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D26/K14/a)
- DiemGPLX: trừ 6 điểm (nêu tại ND168-2024/D26/K14/b)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D26/K14"], "required_numbers": [{"value": 2, "unit": "diem"}, {"value": 6, "unit": "diem"}]}
```

### W-tru_diem-003 · tier A · ND168-2024/D6/K4

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D6/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
> 4. Phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe không đủ điều kiện đã thu phí theo hình thức điện tử tự động không dừng (xe không gắn thẻ đầu cuối) đi vào làn đường dành riêng thu phí theo hình thức điện tử tự động không dừng tại các trạm thu phí;
> b) Dừng xe, đỗ xe tại vị trí: bên trái đường một chiều hoặc bên trái (theo hướng lưu thông) của đường đôi; trên đoạn đường cong hoặc gần đầu dốc nơi tầm nhìn bị che khuất; trên cầu (trừ trường hợp tổ chức giao thông cho phép), gầm cầu vượt (trừ những nơi cho phép dừng xe, đỗ xe), song song với một xe khác đang dừng, đỗ, trừ hành vi vi phạm quy định tại điểm c khoản 7 Điều này;
> c) Không thực hiện biện pháp bảo đảm an toàn theo quy định khi xe ô tô bị hư hỏng ngay tại nơi đường bộ giao nhau cùng mức với đường sắt;
> d) Không nhường đường cho xe xin vượt khi có đủ điều kiện an toàn;
> đ) Lùi xe, quay đầu xe trong hầm đường bộ; dừng xe, đỗ …

- CheTai phat_tien: 2.000.000–3.000.000 đồng (nêu tại ND168-2024/D6/K4)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D6/K16/a)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D6/K4"], "required_numbers": [{"value": 2000000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}]}
```

### W-tru_diem-004 · tier A · ND168-2024/D14/K8

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D14/K8#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 14. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy vi phạm quy định về điều kiện của phương tiện khi tham gia giao thông
> 8. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển xe thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
> a) Thực hiện hành vi quy định tại điểm a, điểm b, điểm c khoản 2 Điều này bị trừ điểm giấy phép lái xe 02 điểm;
> b) Thực hiện hành vi quy định tại khoản 3 Điều này bị trừ điểm giấy phép lái xe 06 điểm.

- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D14/K8/a)
- DiemGPLX: trừ 6 điểm (nêu tại ND168-2024/D14/K8/b)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D14/K8"], "required_numbers": [{"value": 2, "unit": "diem"}, {"value": 6, "unit": "diem"}]}
```

### W-tru_diem-005 · tier A · ND168-2024/D34/K5

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D34/K5#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 34. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển quá khổ giới hạn, xe quá tải trọng, xe bánh xích lưu hành đường bộ (kể cả xe ô tô chở hành khách)
> 5. Phạt tiền từ 40.000.000 đồng đến 50.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe mà tổng trọng lượng (khối lượng toàn bộ) của xe hoặc tải trọng trục xe (bao gồm cả hàng hóa xếp trên xe, người được chở trên xe) vượt quá tải trọng cho phép của đường bộ trên 50%, trừ trường hợp có giấy phép lưu hành còn giá trị sử dụng;
> b) Không chấp hành yêu cầu kiểm tra về trọng tải, tải trọng, khổ giới hạn xe, vận chuyển hàng siêu trường, siêu trọng của người thi hành công vụ; chuyển tải hoặc dùng các thủ đoạn khác để trốn tránh việc phát hiện xe chở quá tải, quá khổ.

- BienPhapBoSung: buộc khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND168-2024/D34/K6)
- CheTai phat_tien: 40.000.000–50.000.000 đồng (nêu tại ND168-2024/D34/K5)
- DiemGPLX: trừ 4 điểm (nêu tại ND168-2024/D34/K7/c)
- DiemGPLX: trừ 10 điểm (nêu tại ND168-2024/D34/K7/d)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D34/K5"], "required_numbers": [{"value": 40000000, "unit": "vnd"}, {"value": 50000000, "unit": "vnd"}, {"value": 4, "unit": "diem"}, {"value": 10, "unit": "diem"}]}
```

### W-tru_diem-006 · tier A · ND168-2024/D21/K9

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D21/K9#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
> 9. Phạt tiền từ 10.000.000 đồng đến 12.000.000 đồng đối với người điều khiển xe thực hiện hành vi nhận, trả hàng trên đường cao tốc.

- CheTai phat_tien: 10.000.000–12.000.000 đồng (nêu tại ND168-2024/D21/K9)
- DiemGPLX: trừ 6 điểm (nêu tại ND168-2024/D21/K13/c)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D21/K9"], "required_numbers": [{"value": 10000000, "unit": "vnd"}, {"value": 12000000, "unit": "vnd"}, {"value": 6, "unit": "diem"}]}
```

### W-tru_diem-007 · tier A · ND168-2024/D22/K6

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D22/K6#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 22. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển hàng siêu trường, siêu trọng
> 6. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
> a) Thực hiện hành vi quy định tại khoản 1 Điều này bị trừ điểm giấy phép lái xe 02 điểm;
> b) Thực hiện hành vi quy định tại khoản 2, khoản 3 Điều này bị trừ điểm giấy phép lái xe 04 điểm.

- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D22/K6/a)
- DiemGPLX: trừ 4 điểm (nêu tại ND168-2024/D22/K6/b)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D22/K6"], "required_numbers": [{"value": 2, "unit": "diem"}, {"value": 4, "unit": "diem"}]}
```

### W-tru_diem-008 · tier A · ND168-2024/D21/K8

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D21/K8#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
> 8. Phạt tiền từ 8.000.000 đồng đến 12.000.000 đồng đối với một trong các hành vi sau đây:
> a) Điều khiển xe (kể cả rơ moóc và sơ mi rơ moóc) chở hàng vượt trọng tải (khối lượng hàng chuyên chở) cho phép tham gia giao thông được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe trên 150%;
> b) Điều khiển xe kéo theo rơ moóc, sơ mi rơ moóc mà khối lượng toàn bộ (bao gồm khối lượng bản thân rơ moóc, sơ mi rơ moóc và khối lượng hàng chuyên chở) của rơ moóc, sơ mi rơ moóc vượt khối lượng cho phép kéo theo được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe trên 150%;
> c) Chở công-ten-nơ trên xe (kể cả sơ mi rơ moóc) không bảo đảm quy chuẩn, tiêu chuẩn kỹ thuật của công-ten-nơ theo quy định;
> d) Chở thiết bị có hình dạng thùng hoặc có hình dạng như công-ten-nơ (không phải công-ten-nơ) vượt quá chiều dài toàn bộ được ghi trong chứng nhận kiểm định an toàn …

- CheTai phat_tien: 8.000.000–12.000.000 đồng (nêu tại ND168-2024/D21/K8)
- DiemGPLX: trừ 4 điểm (nêu tại ND168-2024/D21/K13/b)
- DiemGPLX: trừ 10 điểm (nêu tại ND168-2024/D21/K13/đ)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D21/K8"], "required_numbers": [{"value": 8000000, "unit": "vnd"}, {"value": 12000000, "unit": "vnd"}, {"value": 4, "unit": "diem"}, {"value": 10, "unit": "diem"}]}
```

### W-tru_diem-009 · tier A · ND168-2024/D13/K13

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D13/K13#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 13. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo), xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tư xe ô tô vi phạm quy định về điều kiện của phương tiện khi tham gia giao thông
> 13. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển xe thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
> a) Thực hiện hành vi quy định tại điểm a, điểm b khoản 3; khoản 4; khoản 5; khoản 6; điểm a khoản 7 Điều này bị trừ điểm giấy phép lái xe 02 điểm;
> b) Thực hiện hành vi quy định tại điểm b khoản 7, điểm b khoản 8 Điều này bị trừ điểm giấy phép lái xe 06 điểm;
> c) Thực hiện hành vi quy định tại điểm a khoản 8 Điều này bị trừ điểm giấy phép lái xe 10 điểm.

- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D13/K13/a)
- DiemGPLX: trừ 6 điểm (nêu tại ND168-2024/D13/K13/b)
- DiemGPLX: trừ 10 điểm (nêu tại ND168-2024/D13/K13/c)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D13/K13"], "required_numbers": [{"value": 2, "unit": "diem"}, {"value": 6, "unit": "diem"}, {"value": 10, "unit": "diem"}]}
```

### W-tru_diem-010 · tier A · ND168-2024/D27/K4

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D27/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 27. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô kinh doanh vận tải chở trẻ em mầm non, học sinh, xe ô tô kinh doanh vận tải kết hợp với hoạt động đưa đón trẻ em mầm non, học sinh
> 4. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi quy định tại khoản 2, khoản 3 Điều này bị trừ điểm giấy phép lái xe 02 điểm.

- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D27/K4)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D27/K4"], "required_numbers": [{"value": 2, "unit": "diem"}]}
```

### W-tru_diem-011 · tier A · ND168-2024/D34/K1

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D34/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 34. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển quá khổ giới hạn, xe quá tải trọng, xe bánh xích lưu hành đường bộ (kể cả xe ô tô chở hành khách)
> 1. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với hành vi không thực hiện đúng quy định trong giấy phép lưu hành, trừ các hành vi vi phạm quy định tại điểm a, điểm b khoản 3; điểm b, điểm c khoản 4 Điều này.

- BienPhapBoSung: buộc khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND168-2024/D34/K6)
- CheTai phat_tien: 3.000.000–5.000.000 đồng (nêu tại ND168-2024/D34/K1)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D34/K7/a)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D34/K1"], "required_numbers": [{"value": 3000000, "unit": "vnd"}, {"value": 5000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}]}
```

### W-tru_diem-012 · tier A · ND168-2024/D32/K21

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D32/K21#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
> 21. Ngoài việc bị áp dụng hình thức xử phạt, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
> a) Thực hiện hành vi quy định tại điểm đ, điểm g, điểm m khoản 7; điểm đ, điểm e khoản 8; điểm b, điểm c, điểm d, điểm đ khoản 9; điểm a, điểm b, điểm đ khoản 11; điểm a khoản 12; điểm c khoản 13; điểm đ, điểm h khoản 14 Điều này trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện còn bị trừ điểm giấy phép lái xe 02 điểm;
> b) Thực hiện hành vi quy định tại điểm e, điểm g khoản 14 Điều này trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện còn bị trừ điểm giấy phép lái xe 03 điểm;
> c) Thực hiện hành vi quy định tại điểm a, điểm b, điểm đ, điểm e khoản 13; điểm a, điểm b, điểm c, điểm d khoản 14; điểm a khoản 16 Điều này trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện còn bị trừ điểm giấy phép lái xe 04 điểm;
> d) Thực hiện hành vi quy định tại khoản 5, khoản 6 Điều này trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện chở vượt trên 50% đến 100% …

- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D32/K21/a)
- DiemGPLX: trừ 3 điểm (nêu tại ND168-2024/D32/K21/b)
- DiemGPLX: trừ 4 điểm (nêu tại ND168-2024/D32/K21/c)
- DiemGPLX: trừ 4 điểm (nêu tại ND168-2024/D32/K21/d)
- DiemGPLX: trừ 8 điểm (nêu tại ND168-2024/D32/K21/e)
- DiemGPLX: trừ 10 điểm (nêu tại ND168-2024/D32/K21/g)
- DiemGPLX: trừ 10 điểm (nêu tại ND168-2024/D32/K21/h)
- DiemGPLX: trừ 6 điểm (nêu tại ND168-2024/D32/K21/đ)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D32/K21"], "required_numbers": [{"value": 2, "unit": "diem"}, {"value": 3, "unit": "diem"}, {"value": 4, "unit": "diem"}, {"value": 8, "unit": "diem"}, {"value": 10, "unit": "diem"}, {"value": 6, "unit": "diem"}]}
```

### W-tru_diem-013 · tier A · ND168-2024/D27/K2

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D27/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 27. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô kinh doanh vận tải chở trẻ em mầm non, học sinh, xe ô tô kinh doanh vận tải kết hợp với hoạt động đưa đón trẻ em mầm non, học sinh
> 2. Phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng đối với hành vi điều khiển xe ô tô kinh doanh vận tải chở trẻ em mầm non, học sinh tiểu học, xe ô tô kinh doanh vận tải kết hợp với hoạt động đưa đón trẻ em mầm non, học sinh tiểu học không có hoặc không đủ người quản lý trên mỗi xe ô tô theo quy định tại khoản 3 Điều 46 của Luật Trật tự, an toàn giao thông đường bộ.

- CheTai phat_tien: 2.000.000–3.000.000 đồng (nêu tại ND168-2024/D27/K2)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D27/K4)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D27/K2"], "required_numbers": [{"value": 2000000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}]}
```

### W-tru_diem-014 · tier A · ND168-2024/D25/K1

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D25/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 25. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe vệ sinh môi trường, xe ô tô chở phế thải thực hiện hành vi vi phạm quy định về hoạt động vận tải trong đô thị
> 1. Phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng đối với hành vi điều khiển xe không chạy đúng tuyến, phạm vi, thời gian quy định.

- CheTai phat_tien: 2.000.000–3.000.000 đồng (nêu tại ND168-2024/D25/K1)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D25/K2)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D25/K1"], "required_numbers": [{"value": 2000000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}]}
```

### W-tru_diem-015 · tier A · ND168-2024/D20/K3

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D20/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
> 3. Phạt tiền từ 600.000 đồng đến 800.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Không đóng cửa lên xuống khi xe đang chạy;
> b) Để người ngồi trên xe khi xe xuống phà, đang trên phà và khi lên bến (trừ người lái xe, trẻ em, phụ nữ mang thai, người già yếu, người bệnh, người khuyết tật);
> c) Không chạy đúng tuyến đường, lịch trình, hành trình vận tải được phép hoạt động theo quy định;
> d) Để người mắc võng nằm trên xe khi xe đang chạy;
> đ) Sắp xếp, chằng buộc hành lý, hàng hóa không bảo đảm an toàn; để rơi hành lý, hàng hóa trên xe xuống đường; để hàng hóa trong khoang chở hành khách;
> e) Chở hành lý, hàng hóa vượt quá kích thước bao ngoài của xe;
> g) Điều khiển xe vận tải hành khách không có nhân viên phục vụ trên xe đối với những xe quy định phải có nhân viên phục vụ;
> h) Điều khiển xe ô tô kinh doanh vận tải không có dây đai an toàn tại các vị trí ghế ngồi, giường nằm theo quy định (trừ xe buýt nội tỉnh);
> i) Điều khiển xe ô tô kinh doanh vận tải không có hướng dẫn …

- CheTai phat_tien: 600.000–800.000 đồng (nêu tại ND168-2024/D20/K3)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D20/K10/a)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D20/K3"], "required_numbers": [{"value": 600000, "unit": "vnd"}, {"value": 800000, "unit": "vnd"}, {"value": 2, "unit": "diem"}]}
```

### W-tru_diem-016 · tier A · ND168-2024/D26/K7

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D26/K7#2026-08-15` · hiệu lực 2026-08-15 → 2028-12-31

> Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
> 7. Phạt tiền từ 5.000.000 đồng đến 6.000.000 đồng đối với cá nhân, từ 10.000.000 đồng đến 12.000.000 đồng đối với tổ chức kinh doanh vận tải, dịch vụ hỗ trợ vận tải thực hiện một trong các hành vi vi phạm sau đây:
> a) Không thực hiện việc cung cấp, cập nhật, truyền, lưu trữ, quản lý thông tin, dữ liệu từ thiết bị giám sát hành trình theo quy định;
> b) Không thực hiện đúng nội dung thông tin đã niêm yết trên xe theo quy định;
> c) Sử dụng phương tiện kinh doanh vận tải không lắp thiết bị giám sát hành trình của xe (đối với hình thức kinh doanh vận tải có quy định phương tiện phải lắp thiết bị) hoặc lắp thiết bị nhưng thiết bị không hoạt động, không đúng quy chuẩn theo quy định hoặc làm sai lệch dữ liệu của thiết bị giám sát hành trình của xe ô tô;
> d) Sử dụng xe trung chuyển chở hành khách không đúng quy định;
> đ) Sử dụng lái xe điều khiển xe khách giường nằm hai tầng, xe ô tô đưa đón trẻ em mầm non, học sinh chưa đủ số năm kinh nghiệm theo quy định;
> e) Sử dụng xe kinh doanh vận tải hành khách theo hợp đồng mà trên xe không có hợp đồng vận tải, …

- BienPhapBoSung: buộc lắp đặt thiết bị giám sát hành trình, thiết bị ghi nhận hình ảnh người lái xe, thiết bị ghi nhận hình ảnh khoang chở khách, dây đai an toàn, ghế ngồi cho trẻ em mầm non, học sinh tiểu học trên xe theo đúng quy định (nêu tại ND168-2024/D26/K13/c)
- BienPhapBoSung: buộc cung cấp, cập nhật, truyền dẫn, lưu trữ, quản lý thông tin, dữ liệu thu thập từ thiết bị giám sát hành trình, thiết bị ghi nhận hình ảnh người lái xe, thiết bị ghi nhận hình ảnh khoang chở khách lắp trên xe ô tô theo quy định (nêu tại ND168-2024/D26/K13/d)
- CheTai tuoc_quyen: 1–3 tháng phù hiệu (nêu tại ND168-2024/D26/K12)
- CheTai phat_tien: 5.000.000–6.000.000 đồng (nêu tại ND168-2024/D26/K7)
- CheTai phat_tien: 10.000.000–12.000.000 đồng (nêu tại ND168-2024/D26/K7)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D26/K14/a)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D26/K7"], "required_numbers": [{"value": 1, "unit": "thang"}, {"value": 3, "unit": "thang"}, {"value": 5000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}, {"value": 12000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}]}
```

### W-tru_diem-017 · tier A · ND168-2024/D22/K3

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D22/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 22. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển hàng siêu trường, siêu trọng
> 3. Phạt tiền từ 13.000.000 đồng đến 15.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Chở hàng siêu trường, siêu trọng không có giấy phép lưu hành hoặc có giấy phép lưu hành nhưng đã hết giá trị sử dụng hoặc sử dụng giấy phép lưu hành không do cơ quan có thẩm quyền cấp;
> b) Chở hàng siêu trường, siêu trọng có giấy phép lưu hành còn giá trị sử dụng nhưng tổng trọng lượng (sau khi đã xếp hàng lên xe) vượt quá quy định trong giấy phép lưu hành;
> c) Chở hàng siêu trường, siêu trọng có giấy phép lưu hành còn giá trị sử dụng nhưng đi không đúng tuyến đường quy định trong giấy phép lưu hành;
> d) Chở hàng siêu trường, siêu trọng có giấy phép lưu hành còn giá trị sử dụng nhưng chở không đúng loại hàng quy định trong giấy phép lưu hành.

- BienPhapBoSung: buộc khôi phục lại tình trạng ban đầu đã bị thay đổi do hành vi vi phạm hành chính gây ra (nêu tại ND168-2024/D22/K4)
- CheTai phat_tien: 13.000.000–15.000.000 đồng (nêu tại ND168-2024/D22/K3)
- DiemGPLX: trừ 4 điểm (nêu tại ND168-2024/D22/K6/b)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D22/K3"], "required_numbers": [{"value": 13000000, "unit": "vnd"}, {"value": 15000000, "unit": "vnd"}, {"value": 4, "unit": "diem"}]}
```

### W-tru_diem-018 · tier A · ND168-2024/D22/K1

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D22/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 22. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển hàng siêu trường, siêu trọng
> 1. Phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Chở hàng siêu trường, siêu trọng không có báo hiệu kích thước của hàng theo quy định;
> b) Không thực hiện đúng quy định trong giấy phép lưu hành, trừ các hành vi vi phạm quy định tại khoản 2; điểm b, điểm c, điểm d khoản 3 Điều này.

- BienPhapBoSung: buộc khôi phục lại tình trạng ban đầu đã bị thay đổi do hành vi vi phạm hành chính gây ra (nêu tại ND168-2024/D22/K4)
- CheTai phat_tien: 2.000.000–3.000.000 đồng (nêu tại ND168-2024/D22/K1)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D22/K6/a)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D22/K1"], "required_numbers": [{"value": 2000000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}]}
```

### W-tru_diem-019 · tier A · ND168-2024/D7/K5

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D7/K5#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 7. Xử phạt, trừ điểm giấy phép lái của người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy vi phạm quy tắc giao thông đường bộ
> 5. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe có liên quan trực tiếp đến vụ tai nạn giao thông mà không dừng ngay phương tiện, không giữ nguyên hiện trường, không trợ giúp người bị nạn, trừ hành vi vi phạm quy định tại điểm c khoản 9 Điều này;
> b) Chuyển hướng không nhường quyền đi trước cho: người đi bộ, xe lăn của người khuyết tật qua đường tại nơi có vạch kẻ đường dành cho người đi bộ; xe thô sơ đang đi trên phần đường dành cho xe thô sơ;
> c) Chuyển hướng không nhường đường cho: các xe đi ngược chiều; người đi bộ, xe thô sơ đang qua đường tại nơi không có vạch kẻ đường cho người đi bộ.

- CheTai phat_tien: 1.000.000–2.000.000 đồng (nêu tại ND168-2024/D7/K5)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D7/K13/a)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D7/K5"], "required_numbers": [{"value": 1000000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}]}
```

### W-tru_diem-020 · tier A · ND168-2024/D21/K6

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D21/K6#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
> 6. Phạt tiền từ 5.000.000 đồng đến 7.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe (kể cả rơ moóc và sơ mi rơ moóc) chở hàng vượt trọng tải (khối lượng hàng chuyên chở) cho phép tham gia giao thông được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe trên 50% đến 100%;
> b) Điều khiển xe kéo theo rơ moóc, sơ mi rơ moóc mà khối lượng toàn bộ (bao gồm khối lượng bản thân rơ moóc, sơ mi rơ moóc và khối lượng hàng chuyên chở) của rơ moóc, sơ mi rơ moóc vượt khối lượng cho phép kéo theo được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe trên 50% đến 100%;
> c) Điều khiển xe không có hoặc không gắn phù hiệu theo quy định (đối với loại xe có quy định phải gắn phù hiệu) hoặc có phù hiệu nhưng đã hết giá trị sử dụng hoặc sử dụng phù hiệu không do cơ quan có thẩm quyền cấp;
> d) Điều khiển xe chở hàng trong đô thị không chạy …

- CheTai phat_tien: 5.000.000–7.000.000 đồng (nêu tại ND168-2024/D21/K6)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D21/K13/a)
- DiemGPLX: trừ 4 điểm (nêu tại ND168-2024/D21/K13/b)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D21/K6"], "required_numbers": [{"value": 5000000, "unit": "vnd"}, {"value": 7000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}, {"value": 4, "unit": "diem"}]}
```

### W-tru_diem-021 · tier A · ND168-2024/D17/K5

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D17/K5#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 17. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, máy kéo và các loại xe tương tự xe ô tô vi phạm quy định về bảo vệ môi trường khi tham gia giao thông
> 5. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện (khi điều khiển xe ô tô) thực hiện hành vi vi phạm quy định tại khoản 3, khoản 4 Điều này còn bị trừ điểm giấy phép lái xe 02 điểm.

- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D17/K5)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D17/K5"], "required_numbers": [{"value": 2, "unit": "diem"}]}
```

### W-tru_diem-022 · tier A · ND168-2024/D20/K8a

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D20/K8a#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
> 8a. Phạt tiền từ 12.000.000 đồng đến 14.000.000 đồng đối với người điều khiển xe ô tô không kinh doanh vận tải hành khách nhưng cho người có thu tiền hoặc ký hợp đồng, nhận đặt chỗ để chở người trên xe.

- CheTai phat_tien: 12.000.000–14.000.000 đồng (nêu tại ND168-2024/D20/K8a)
- DiemGPLX: trừ 6 điểm (nêu tại ND168-2024/D20/K10/c)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D20/K8a"], "required_numbers": [{"value": 12000000, "unit": "vnd"}, {"value": 14000000, "unit": "vnd"}, {"value": 6, "unit": "diem"}]}
```

### W-tru_diem-023 · tier A · ND168-2024/D25/K2

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D25/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 25. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe vệ sinh môi trường, xe ô tô chở phế thải thực hiện hành vi vi phạm quy định về hoạt động vận tải trong đô thị
> 2. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm quy định tại khoản 1 Điều này còn bị trừ điểm giấy phép lái xe 02 điểm.

- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D25/K2)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D25/K2"], "required_numbers": [{"value": 2, "unit": "diem"}]}
```

### W-tru_diem-024 · tier A · ND168-2024/D17/K4

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D17/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 17. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, máy kéo và các loại xe tương tự xe ô tô vi phạm quy định về bảo vệ môi trường khi tham gia giao thông
> 4. Phạt tiền từ 10.000.000 đồng đến 15.000.000 đồng đối với người điều khiển xe thực hiện hành vi đổ trái phép rác, đất, cát, đá, vật liệu, chất phế thải ra đường phố.

- CheTai phat_tien: 10.000.000–15.000.000 đồng (nêu tại ND168-2024/D17/K4)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D17/K5)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D17/K4"], "required_numbers": [{"value": 10000000, "unit": "vnd"}, {"value": 15000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}]}
```

### W-tru_diem-025 · tier A · ND168-2024/D32/K15

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D32/K15#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
> 15. Phạt tiền từ 30.000.000 đồng đến 40.000.000 đồng đối với cá nhân, từ 60.000.000 đồng đến 80.000.000 đồng đối với tổ chức là chủ xe ô tô, xe máy chuyên dùng và các loại xe tương tự xe ô tô khi giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại khoản 7 Điều 21 của Nghị định này hoặc trực tiếp điều khiển phương tiện thực hiện hành vi vi phạm quy định tại khoản 7 Điều 21 của Nghị định này.

- BienPhapBoSung: phải khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND168-2024/D32/K19/e)
- BienPhapBoSung: buộc thực hiện điều chỉnh thùng xe theo đúng quy định hiện hành, đăng kiểm lại và điều chỉnh lại khối lượng hàng hóa cho phép chuyên chở ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường theo quy định hiện hành trước khi đưa phương tiện ra tham gia giao thông (nêu tại ND168-2024/D32/K19/đ)
- CheTai phat_tien: 30.000.000–40.000.000 đồng (nêu tại ND168-2024/D32/K15)
- CheTai phat_tien: 60.000.000–80.000.000 đồng (nêu tại ND168-2024/D32/K15)
- CheTai tuoc_quyen: 1–3 tháng chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường và tem kiểm định của phương tiện (nêu tại ND168-2024/D32/K18/c)
- CheTai tuoc_quyen: 1–3 tháng phù hiệu (nêu tại ND168-2024/D32/K18/đ)
- DiemGPLX: trừ 8 điểm (nêu tại ND168-2024/D32/K21/e)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D32/K15"], "required_numbers": [{"value": 30000000, "unit": "vnd"}, {"value": 40000000, "unit": "vnd"}, {"value": 60000000, "unit": "vnd"}, {"value": 80000000, "unit": "vnd"}, {"value": 1, "unit": "thang"}, {"value": 3, "unit": "thang"}, {"value": 8, "unit": "diem"}]}
```

### W-tru_diem-026 · tier A · ND168-2024/D29/K4

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D29/K4#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 29. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe cứu hộ giao thông đường bộ
> 4. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi quy định tại khoản 3, khoản 3a Điều này bị trừ điểm giấy phép lái xe 02 điểm.

- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D29/K4)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D29/K4"], "required_numbers": [{"value": 2, "unit": "diem"}]}
```

### W-tru_diem-027 · tier A · ND168-2024/D32/K9

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D32/K9#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
> 9. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng đối với cá nhân, từ 8.000.000 đồng đến 12.000.000 đồng đối với tổ chức là chủ xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ, xe máy chuyên dùng và các loại xe tương tự xe ô tô thực hiện một trong các hành vi vi phạm sau đây:
> a) Thuê, mượn linh kiện, phụ kiện của xe ô tô khi kiểm định;
> b) Đưa xe cơ giới, xe máy chuyên dùng có giấy chứng nhận hoặc tem kiểm định an toàn kỹ thuật và bảo vệ môi trường (đối với loại xe có quy định phải kiểm định) nhưng đã hết hiệu lực (hạn sử dụng) dưới 01 tháng (kể cả rơ moóc và sơ mi rơ moóc) tham gia giao thông;
> c) Giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại khoản 4 Điều 21 của Nghị định này hoặc trực tiếp điều khiển phương tiện thực hiện hành vi vi phạm quy định tại khoản 4 Điều 21 của Nghị định này;
> d) Giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm d khoản 6 Điều 20; điểm b khoản 5 Điều 21 …

- BienPhapBoSung: buộc thực hiện đúng quy định về biển số xe, quy định về kẻ hoặc dán chữ, số biển số, thông tin trên thành xe, cửa xe (nêu tại ND168-2024/D32/K19/c)
- BienPhapBoSung: phải khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND168-2024/D32/K19/e)
- BienPhapBoSung: buộc nộp lại chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe), giấy chứng nhận, tem kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe bị tẩy xóa (nêu tại ND168-2024/D32/K19/i)
- CheTai tich_thu: phương tiện (nêu tại ND168-2024/D32/K18/b)
- CheTai phat_tien: 4.000.000–6.000.000 đồng (nêu tại ND168-2024/D32/K9)
- CheTai phat_tien: 8.000.000–12.000.000 đồng (nêu tại ND168-2024/D32/K9)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D32/K21/a)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D32/K9"], "required_numbers": [{"value": 4000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}, {"value": 8000000, "unit": "vnd"}, {"value": 12000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}]}
```

### W-tru_diem-028 · tier A · ND168-2024/D7/K4

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D7/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 7. Xử phạt, trừ điểm giấy phép lái của người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy vi phạm quy tắc giao thông đường bộ
> 4. Phạt tiền từ 800.000 đồng đến 1.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe chạy quá tốc độ quy định từ 10 km/h đến 20 km/h;
> b) Dừng xe, đỗ xe trong hầm đường bộ không đúng nơi quy định;
> c) Vượt xe trong những trường hợp không được vượt, vượt xe tại đoạn đường có biển báo hiệu có nội dung cấm vượt đối với loại phương tiện đang điều khiển, trừ các hành vi vi phạm quy định tại điểm đ khoản 3 Điều này;
> d) Quay đầu xe trong hầm đường bộ;
> đ) Người đang điều khiển xe sử dụng ô (dù), thiết bị âm thanh (trừ thiết bị trợ thính), dùng tay cầm và sử dụng điện thoại hoặc các thiết bị điện tử khác.

- CheTai phat_tien: 800.000–1.000.000 đồng (nêu tại ND168-2024/D7/K4)
- DiemGPLX: trừ 4 điểm (nêu tại ND168-2024/D7/K13/b)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D7/K4"], "required_numbers": [{"value": 800000, "unit": "vnd"}, {"value": 1000000, "unit": "vnd"}, {"value": 4, "unit": "diem"}]}
```

### W-tru_diem-029 · tier A · ND168-2024/D21/K13

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D21/K13#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
> 13. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
> a) Thực hiện hành vi quy định tại điểm b, điểm c, điểm đ khoản 2; điểm a khoản 3; khoản 4; khoản 5; điểm c, điểm d, điểm đ khoản 6 Điều này bị trừ điểm giấy phép lái xe (khi điều khiển xe ô tô) 02 điểm;
> b) Thực hiện hành vi quy định tại điểm a, điểm b khoản 6; điểm c, điểm d, điểm đ khoản 8; khoản 10 Điều này bị trừ điểm giấy phép lái xe 04 điểm;
> c) Thực hiện hành vi quy định tại khoản 9 Điều này bị trừ điểm giấy phép lái xe 06 điểm;
> d) Thực hiện hành vi quy định tại khoản 7 Điều này bị trừ điểm giấy phép lái xe 08 điểm;
> đ) Thực hiện hành vi quy định tại điểm a, điểm b khoản 8; khoản 11 Điều này bị trừ điểm giấy phép lái xe 10 điểm.

- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D21/K13/a)
- DiemGPLX: trừ 4 điểm (nêu tại ND168-2024/D21/K13/b)
- DiemGPLX: trừ 6 điểm (nêu tại ND168-2024/D21/K13/c)
- DiemGPLX: trừ 8 điểm (nêu tại ND168-2024/D21/K13/d)
- DiemGPLX: trừ 10 điểm (nêu tại ND168-2024/D21/K13/đ)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D21/K13"], "required_numbers": [{"value": 2, "unit": "diem"}, {"value": 4, "unit": "diem"}, {"value": 6, "unit": "diem"}, {"value": 8, "unit": "diem"}, {"value": 10, "unit": "diem"}]}
```

### W-tru_diem-030 · tier A · ND168-2024/D21/K3

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D21/K3#2025-01-01` · hiệu lực 2025-01-01 → 2027-12-31

> Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
> 3. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Không sử dụng thẻ nhận dạng lái xe để đăng nhập thông tin theo quy định hoặc sử dụng thẻ nhận dạng lái xe của lái xe khác để đăng nhập thông tin khi điều khiển xe tham gia kinh doanh vận tải hàng hóa;
> b) Điều khiển xe ô tô đầu kéo không lắp thiết bị ghi nhận hình ảnh người lái xe hoặc có lắp thiết bị ghi nhận hình ảnh người lái xe nhưng không có tác dụng trong quá trình xe tham gia giao thông theo quy định hoặc làm sai lệch dữ liệu của thiết bị ghi nhận hình ảnh người lái xe lắp trên xe ô tô.

- CheTai phat_tien: 1.000.000–2.000.000 đồng (nêu tại ND168-2024/D21/K3)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D21/K13/a)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D21/K3"], "required_numbers": [{"value": 1000000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}]}
```

## bien_phap — tước quyền sử dụng giấy phép, tịch thu, biện pháp khắc phục hậu quả

### W-bien_phap-001 · tier A · ND168-2024/D26/K8

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D26/K8#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
> 8. Phạt tiền từ 10.000.000 đồng đến 12.000.000 đồng đối với cá nhân, từ 20.000.000 đồng đến 24.000.000 đồng đối với tổ chức kinh doanh vận tải, dịch vụ hỗ trợ vận tải thực hiện một trong các hành vi vi phạm sau đây:
> a) Không tổ chức khám sức khỏe định kỳ cho lái xe theo quy định hoặc có tổ chức khám nhưng không đầy đủ các nội dung theo quy định;
> b) Vi phạm quy định về kinh doanh, điều kiện kinh doanh vận tải bằng xe ô tô để xảy ra tai nạn giao thông gây hậu quả từ mức nghiêm trọng trở lên;
> c) Sử dụng xe ô tô kinh doanh vận tải để đón, trả khách; nhận, trả hàng trên đường cao tốc.
> d) Sử dụng xe ô tô kinh doanh vận tải hành khách theo hợp đồng mà xác nhận đặt chỗ cho từng hành khách đi xe ngoài hợp đồng đã ký kết hoặc bán vé, thu tiền ngoài hợp đồng đã ký kết; ấn định hành trình, lịch trình cố định để phục vụ cho nhiều hành khách hoặc nhiều người thuê vận tải khác nhau.

- BienPhapBoSung: buộc tổ chức tập huấn, hướng dẫn nghiệp vụ, quy trình hoặc tổ chức khám sức khỏe định kỳ cho lái xe và nhân viên phục vụ trên xe theo quy định (nêu tại ND168-2024/D26/K13/b)
- CheTai tuoc_quyen: 1–3 tháng phù hiệu (nêu tại ND168-2024/D26/K12)
- CheTai phat_tien: 10.000.000–12.000.000 đồng (nêu tại ND168-2024/D26/K8)
- CheTai phat_tien: 20.000.000–24.000.000 đồng (nêu tại ND168-2024/D26/K8)
- DiemGPLX: trừ 6 điểm (nêu tại ND168-2024/D26/K14/b)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D26/K8"], "required_numbers": [{"value": 1, "unit": "thang"}, {"value": 3, "unit": "thang"}, {"value": 10000000, "unit": "vnd"}, {"value": 12000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}, {"value": 24000000, "unit": "vnd"}, {"value": 6, "unit": "diem"}]}
```

### W-bien_phap-002 · tier A · ND168-2024/D13/K9

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D13/K9#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 13. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo), xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tư xe ô tô vi phạm quy định về điều kiện của phương tiện khi tham gia giao thông
> 9. Tịch thu phương tiện đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe quá niên hạn sử dụng tham gia giao thông, trừ hành vi quy định tại điểm c khoản 5 Điều này;
> b) Điều khiển loại xe sản xuất, lắp ráp trái quy định tham gia giao thông (bao gồm cả xe công nông thuộc diện bị đình chỉ tham gia giao thông, rơ moóc và sơ mi rơ moóc được kéo theo).

- CheTai tich_thu: phương tiện (nêu tại ND168-2024/D13/K9)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D13/K9"], "required_numbers": []}
```

### W-bien_phap-003 · tier A · ND168-2024/D12/K15

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D12/K15#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 12. Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm khác về quy tắc giao thông đường bộ; sử dụng lòng đường, vỉa hè vào mục đích khác
> 15. Ngoài việc bị phạt tiền, cá nhân thực hiện hành vi quy định tại khoản 14 Điều này nếu là người điều khiển phương tiện còn bị áp dụng hình thức xử phạt bổ sung tước quyền sử dụng giấy phép lát xe từ 22 tháng đến 24 tháng.

- CheTai tuoc_quyen: 22–24 tháng giấy phép lát xe (nêu tại ND168-2024/D12/K15)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D12/K15"], "required_numbers": [{"value": 22, "unit": "thang"}, {"value": 24, "unit": "thang"}]}
```

### W-bien_phap-004 · tier A · ND168-2024/D32/K4

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D32/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
> 4. Phạt tiền từ 800.000 đồng đến 1.000.000 đồng đối với cá nhân, từ 1.600.000 đồng đến 2.000.000 đồng đối với tổ chức là chủ xe mô tô, xe gắn máy và các loại xe tương tự xe mô tô, các loại xe tương tự xe gắn máy không thực hiện đúng quy định về biển số, trừ các hành vi vi phạm quy định tại điểm g, điểm h khoản 8 Điều này.

- BienPhapBoSung: buộc thực hiện đúng quy định về biển số xe, quy định về kẻ hoặc dán chữ, số biển số, thông tin trên thành xe, cửa xe (nêu tại ND168-2024/D32/K19/c)
- CheTai phat_tien: 800.000–1.000.000 đồng (nêu tại ND168-2024/D32/K4)
- CheTai phat_tien: 1.600.000–2.000.000 đồng (nêu tại ND168-2024/D32/K4)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D32/K4"], "required_numbers": [{"value": 800000, "unit": "vnd"}, {"value": 1000000, "unit": "vnd"}, {"value": 1600000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}]}
```

### W-bien_phap-005 · tier A · ND168-2024/D31/K4

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D31/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 31. Xử phạt hành vi sản xuất, lắp ráp trái phép phương tiện giao thông cơ giới đường bộ; sản xuất, mua, bán biển số xe trái phép
> 4. Ngoài việc bị áp dụng hình thức xử phạt, cá nhân, tổ chức thực hiện hành vi quy định tại khoản 1, khoản 2 Điều này còn bị áp dụng biện pháp khắc phục hậu quả buộc nộp lại số lợi bất hợp pháp có được do thực hiện vi phạm hành chính.

- BienPhapBoSung: buộc nộp lại số lợi bất hợp pháp có được do thực hiện vi phạm hành chính (nêu tại ND168-2024/D31/K4)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D31/K4"], "required_numbers": []}
```

### W-bien_phap-006 · tier A · ND168-2024/D14/K1

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D14/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 14. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy vi phạm quy định về điều kiện của phương tiện khi tham gia giao thông
> 1. Phạt tiền từ 400.000 đồng đến 600.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe không có còi; đèn soi biển số; đèn báo hãm; gương chiếu hậu bên trái người điều khiển hoặc có nhưng không có tác dụng;
> b) Điều khiển xe không có đèn tín hiệu hoặc có nhưng không có tác dụng;
> c) Điều khiển xe không có đèn chiếu sáng gần, xa hoặc có nhưng không có tác dụng, không đúng tiêu chuẩn thiết kế;
> d) Điều khiển xe không có hệ thống hãm hoặc có nhưng không có tác dụng, không bảo đảm tiêu chuẩn kỹ thuật;
> đ) Điều khiển xe lắp đèn chiếu sáng về phía sau xe.

- BienPhapBoSung: buộc thay thế thiết bị đủ tiêu chuẩn an toàn kỹ thuật hoặc khôi phục tính năng kỹ thuật của thiết bị theo quy định (nêu tại ND168-2024/D14/K6/a)
- CheTai phat_tien: 400.000–600.000 đồng (nêu tại ND168-2024/D14/K1)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D14/K1"], "required_numbers": [{"value": 400000, "unit": "vnd"}, {"value": 600000, "unit": "vnd"}]}
```

### W-bien_phap-007 · tier A · ND168-2024/D26/K13

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D26/K13#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
> 13. Ngoài việc bị áp dụng hình thức xử phạt, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị áp dụng các biện pháp khắc phục hậu quả sau đây:
> a) Thực hiện hành vi quy định tại điểm a khoản 4 Điều này buộc cấp thẻ nhận dạng lái xe cho lái xe theo quy định;
> b) Thực hiện hành vi quy định tại điểm b, điểm c, điểm d khoản 4; điểm a khoản 8 Điều này buộc tổ chức tập huấn, hướng dẫn nghiệp vụ, quy trình hoặc tổ chức khám sức khỏe định kỳ cho lái xe và nhân viên phục vụ trên xe theo quy định;
> c) Thực hiện hành vi quy định tại điểm đ, điểm e khoản 4; điểm c, điểm g, điểm k khoản 7 Điều này buộc lắp đặt thiết bị giám sát hành trình, thiết bị ghi nhận hình ảnh người lái xe, thiết bị ghi nhận hình ảnh khoang chở khách, dây đai an toàn, ghế ngồi cho trẻ em mầm non, học sinh tiểu học trên xe theo đúng quy định;
> d) Thực hiện hành vi quy định tại điểm a, điểm h, điểm l khoản 7; khoản 11 Điều này buộc cung cấp, cập nhật, truyền dẫn, lưu trữ, quản lý thông tin, dữ liệu thu thập từ thiết bị giám sát hành trình, thiết bị ghi nhận hình ảnh người lái xe, thiết …

- BienPhapBoSung: buộc cấp thẻ nhận dạng lái xe cho lái xe theo quy định (nêu tại ND168-2024/D26/K13/a)
- BienPhapBoSung: buộc tổ chức tập huấn, hướng dẫn nghiệp vụ, quy trình hoặc tổ chức khám sức khỏe định kỳ cho lái xe và nhân viên phục vụ trên xe theo quy định (nêu tại ND168-2024/D26/K13/b)
- BienPhapBoSung: buộc lắp đặt thiết bị giám sát hành trình, thiết bị ghi nhận hình ảnh người lái xe, thiết bị ghi nhận hình ảnh khoang chở khách, dây đai an toàn, ghế ngồi cho trẻ em mầm non, học sinh tiểu học trên xe theo đúng quy định (nêu tại ND168-2024/D26/K13/c)
- BienPhapBoSung: buộc cung cấp, cập nhật, truyền dẫn, lưu trữ, quản lý thông tin, dữ liệu thu thập từ thiết bị giám sát hành trình, thiết bị ghi nhận hình ảnh người lái xe, thiết bị ghi nhận hình ảnh khoang chở khách lắp trên xe ô tô theo quy định (nêu tại ND168-2024/D26/K13/d)
- BienPhapBoSung: buộc thực hiện đúng quy định về màu sơn, biển báo dấu hiệu nhận biết của xe (nêu tại ND168-2024/D26/K13/đ)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D26/K13"], "required_numbers": []}
```

### W-bien_phap-008 · tier A · ND168-2024/D32/K18

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D32/K18#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
> 18. Ngoài việc bị phạt tiền, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị áp dụng các hình thức xử phạt bổ sung như sau:
> a) Thực hiện hành vi quy định tại điểm g, điểm h khoản 8; điểm c khoản 12; điểm d khoản 13 Điều này bị tịch thu biển số; tịch thu biển số, thiết bị thay đổi biển số;
> b) Thực hiện hành vi quy định tại điểm đ, điểm e khoản 8; điểm đ khoản 9; điểm a khoản 12 Điều này trong trường hợp không có chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe) hoặc có chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe) nhưng không do cơ quan có thẩm quyền cấp, không đúng số khung, số động cơ (số máy) của xe hoặc bị tẩy xóa (kể cả rơ moóc và sơ mi rơ moóc) …

- CheTai tich_thu: biển số (nêu tại ND168-2024/D32/K18/a)
- CheTai tich_thu: biển số, thiết bị thay đổi biển số (nêu tại ND168-2024/D32/K18/a)
- CheTai tich_thu: phương tiện (nêu tại ND168-2024/D32/K18/b)
- CheTai tuoc_quyen: 1–3 tháng chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường và tem kiểm định của phương tiện (nêu tại ND168-2024/D32/K18/c)
- CheTai tuoc_quyen: 1–3 tháng chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường và tem kiểm định của phương tiện (nêu tại ND168-2024/D32/K18/d)
- CheTai tuoc_quyen: 1–3 tháng phù hiệu (nêu tại ND168-2024/D32/K18/đ)
- CheTai tuoc_quyen: 1–3 tháng phù hiệu (nêu tại ND168-2024/D32/K18/đ)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D32/K18"], "required_numbers": [{"value": 1, "unit": "thang"}, {"value": 3, "unit": "thang"}]}
```

### W-bien_phap-009 · tier A · ND168-2024/D32/K2

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D32/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
> 2. Phạt tiền từ 300.000 đồng đến 400.000 đồng đối với cá nhân, từ 600.000 đồng đến 800.000 đồng đối với tổ chức là chủ xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ, xe máy chuyên dùng và các loại xe tương tự xe ô tô thực hiện một trong các hành vi vi phạm sau đây:
> a) Lắp kính chắn gió, kính cửa của xe không phải là loại kính an toàn;
> b) Không làm thủ tục khai báo với cơ quan đăng ký xe theo quy định trước khi cải tạo xe (đối với loại xe có quy định phải làm thủ tục khai báo).

- BienPhapBoSung: buộc thay thế thiết bị đủ tiêu chuẩn an toàn kỹ thuật theo quy định (lắp đúng loại kính an toàn) (nêu tại ND168-2024/D32/K19/b)
- CheTai phat_tien: 300.000–400.000 đồng (nêu tại ND168-2024/D32/K2)
- CheTai phat_tien: 600.000–800.000 đồng (nêu tại ND168-2024/D32/K2)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D32/K2"], "required_numbers": [{"value": 300000, "unit": "vnd"}, {"value": 400000, "unit": "vnd"}, {"value": 600000, "unit": "vnd"}, {"value": 800000, "unit": "vnd"}]}
```

### W-bien_phap-010 · tier A · ND168-2024/D33/K4

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D33/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 33. Xử phạt hành khách đi xe vi phạm quy định về trật tự, an toàn giao thông
> 4. Ngoài việc bị phạt tiền, người thực hiện hành vi vi phạm quy định tại điểm a khoản 2 Điều này còn bị áp dụng hình thức xử phạt bổ sung tịch thu hóa chất độc hại, chất dễ cháy, nổ, hàng nguy hiểm, hàng cấm lưu thông mang theo trên xe chở khách.

- CheTai tich_thu: hóa chất độc hại, chất dễ cháy, nổ, hàng nguy hiểm, hàng cấm lưu thông mang theo trên xe chở khách (nêu tại ND168-2024/D33/K4)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D33/K4"], "required_numbers": []}
```

### W-bien_phap-011 · tier A · ND168-2024/D16/K5

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D16/K5#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 16. Xử phạt người điều khiển xe máy chuyên dùng (kể cả rơ moóc được kéo theo) vi phạm quy định về điều kiện của phương tiện khi tham gia giao thông
> 5. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị áp dụng biện pháp khắc phục hậu quả sau đây:
> a) Thực hiện hành vi vi phạm quy định tại điểm b, điểm c, điểm d khoản 1 Điều này buộc lắp đầy đủ thiết bị hoặc thay thế thiết bị đủ tiêu chuẩn, quy chuẩn an toàn kỹ thuật hoặc khôi phục lại tính năng kỹ thuật của thiết bị theo quy định;
> b) Thực hiện hành vi quy định tại điểm đ khoản 2 Điều này buộc nộp lại chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe), giấy chứng nhận, tem kiểm định an toàn kỹ thuật và bảo vệ môi trường bị tẩy xóa.

- BienPhapBoSung: buộc lắp đầy đủ thiết bị hoặc thay thế thiết bị đủ tiêu chuẩn, quy chuẩn an toàn kỹ thuật hoặc khôi phục lại tính năng kỹ thuật của thiết bị theo quy định (nêu tại ND168-2024/D16/K5/a)
- BienPhapBoSung: buộc nộp lại chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe), giấy chứng nhận, tem kiểm định an toàn kỹ thuật và bảo vệ môi trường bị tẩy xóa (nêu tại ND168-2024/D16/K5/b)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D16/K5"], "required_numbers": []}
```

### W-bien_phap-012 · tier A · ND168-2024/D32/K9a

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D32/K9a#2026-08-15` · hiệu lực 2026-08-15 → 2027-12-31

> Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
> 9a. Phạt tiền từ 5.000.000 đồng đến 6.000.000 đồng đối với cá nhân, từ 10.000.000 đồng đến 12.000.000 đồng đối với tổ chức là chủ xe ô tô đầu kéo, xe vận tải nội bộ thực hiện một trong các hành vi vi phạm sau đây:
> a) Đưa xe không lắp thiết bị giám sát hành trình của xe hoặc có lắp thiết bị giám sát hành trình nhưng không hoạt động, không đúng quy chuẩn theo quy định hoặc làm sai lệch dữ liệu của thiết bị giám sát hành trình của xe ô tô;

- BienPhapBoSung: buộc lắp đặt dụng cụ, thiết bị chuyên dùng để cứu hộ, hỗ trợ cứu hộ, thiết bị giám sát hành trình, thiết bị ghi nhận hình ảnh người lái xe trên xe theo đúng quy định (nêu tại ND168-2024/D32/K19/l)
- CheTai phat_tien: 5.000.000–6.000.000 đồng (nêu tại ND168-2024/D32/K9a)
- CheTai phat_tien: 10.000.000–12.000.000 đồng (nêu tại ND168-2024/D32/K9a)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D32/K9a"], "required_numbers": [{"value": 5000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}, {"value": 12000000, "unit": "vnd"}]}
```

### W-bien_phap-013 · tier A · ND168-2024/D16/K3

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D16/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 16. Xử phạt người điều khiển xe máy chuyên dùng (kể cả rơ moóc được kéo theo) vi phạm quy định về điều kiện của phương tiện khi tham gia giao thông
> 3. Tịch thu phương tiện đối với hành vi điều khiển xe máy chuyên dùng sản xuất, lắp ráp hoặc cải tạo trái quy định tham gia giao thông.

- CheTai tich_thu: phương tiện (nêu tại ND168-2024/D16/K3)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D16/K3"], "required_numbers": []}
```

### W-bien_phap-014 · tier A · ND168-2024/D12/K3

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D12/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 12. Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm khác về quy tắc giao thông đường bộ; sử dụng lòng đường, vỉa hè vào mục đích khác
> 3. Phạt tiền từ 250.000 đồng đến 350.000 đồng đối với cá nhân, từ 500.000 đồng đến 700.000 đồng đối với tổ chức để vật che khuất biển báo hiệu đường bộ, đèn tín hiệu giao thông.

- BienPhapBoSung: buộc phá dỡ các vật che khuất biển báo hiệu đường bộ, đèn tín hiệu giao thông (nêu tại ND168-2024/D12/K16/a)
- CheTai phat_tien: 250.000–350.000 đồng (nêu tại ND168-2024/D12/K3)
- CheTai phat_tien: 500.000–700.000 đồng (nêu tại ND168-2024/D12/K3)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D12/K3"], "required_numbers": [{"value": 250000, "unit": "vnd"}, {"value": 350000, "unit": "vnd"}, {"value": 500000, "unit": "vnd"}, {"value": 700000, "unit": "vnd"}]}
```

### W-bien_phap-015 · tier A · ND168-2024/D6/K11

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D6/K11#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
> 11. Phạt tiền từ 30.000.000 đồng đến 40.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe trên đường mà trong máu hoặc hơi thở có nồng độ cồn vượt quá 80 miligam/100 mililít máu hoặc vượt quá 0,4 miligam/1 lít khí thở;
> b) Không chấp hành yêu cầu kiểm tra về nồng độ cồn của người thi hành công vụ;
> c) Điều khiển xe trên đường mà trong cơ thể có chất ma túy hoặc chất kích thích khác mà pháp luật cấm sử dụng;
> d) Không chấp hành yêu cầu kiểm tra về chất ma túy hoặc chất kích thích khác mà pháp luật cấm sử dụng của người thi hành công vụ;
> đ) Điều khiển xe đi ngược chiều trên đường cao tốc, lùi xe trên đường cao tốc, quay đầu xe trên đường cao tốc, trừ các xe ưu tiên đang đi làm nhiệm vụ khẩn cấp theo quy định.

- CheTai phat_tien: 30.000.000–40.000.000 đồng (nêu tại ND168-2024/D6/K11)
- CheTai tuoc_quyen: 22–24 tháng giấy phép lái xe (nêu tại ND168-2024/D6/K15/c)
- DiemGPLX: trừ 10 điểm (nêu tại ND168-2024/D6/K16/d)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D6/K11"], "required_numbers": [{"value": 30000000, "unit": "vnd"}, {"value": 40000000, "unit": "vnd"}, {"value": 22, "unit": "thang"}, {"value": 24, "unit": "thang"}, {"value": 10, "unit": "diem"}]}
```

### W-bien_phap-016 · tier A · ND168-2024/D18/K9

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D18/K9#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 18. Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm quy định về điều kiện của người điều khiển xe cơ giới
> 9. Phạt tiền từ 18.000.000 đồng đến 20.000.000 đồng đối với người điều khiển xe ô tô và các loại xe tương tự xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ vi phạm một trong các hành vi sau đây:
> a) Có giấy phép lái xe nhưng không phù hợp với loại xe đang điều khiển hoặc có giấy phép lái xe nhưng đã hết hạn sử dụng từ 01 năm trở lên;
> b) Không có giấy phép lái xe hoặc sử dụng giấy phép lái xe đã bị trừ hết điểm hoặc sử dụng giấy phép lái xe không do cơ quan có thẩm quyền cấp, giấy phép lái xe bị tẩy xóa, giấy phép lái xe không còn hiệu lực.

- BienPhapBoSung: buộc nộp lại giấy phép lái xe bị tẩy xóa (nêu tại ND168-2024/D18/K10)
- CheTai phat_tien: 18.000.000–20.000.000 đồng (nêu tại ND168-2024/D18/K9)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D18/K9"], "required_numbers": [{"value": 18000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}]}
```

### W-bien_phap-017 · tier A · ND168-2024/D13/K1

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D13/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 13. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo), xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tư xe ô tô vi phạm quy định về điều kiện của phương tiện khi tham gia giao thông
> 1. Phạt tiền từ 200.000 đồng đến 400.000 đồng đối với hành vi điều khiển xe không có kính chắn gió hoặc có nhưng vỡ không có tác dụng (đối với xe có thiết kế lắp kính chắn gió).

- BienPhapBoSung: buộc lắp đầy đủ thiết bị hoặc thay thế thiết bị đủ tiêu chuẩn, quy chuẩn an toàn kỹ thuật hoặc khôi phục lại tính năng kỹ thuật của thiết bị theo quy định (nêu tại ND168-2024/D13/K11/a)
- BienPhapBoSung: buộc thực hiện đúng quy định về biển số hoặc khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND168-2024/D13/K11/a)
- CheTai phat_tien: 200.000–400.000 đồng (nêu tại ND168-2024/D13/K1)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D13/K1"], "required_numbers": [{"value": 200000, "unit": "vnd"}, {"value": 400000, "unit": "vnd"}]}
```

### W-bien_phap-018 · tier A · ND168-2024/D26/K4

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D26/K4#2026-01-01` · hiệu lực 2026-01-01 → nay

> Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
> 4. Phạt tiền từ 3.000.000 đồng đến 4.000.000 đồng đối với cá nhân, từ 6.000.000 đồng đến 8.000.000 đồng đối với tổ chức kinh doanh vận tải, dịch vụ hỗ trợ vận tải thực hiện một trong các hành vi vi phạm sau đây:
> a) Không cấp thẻ nhận dạng lái xe cho lái xe theo quy định;
> b) Sử dụng lái xe, nhân viên phục vụ trên xe để tham gia kinh doanh vận tải bằng xe ô tô mà không được tập huấn, hướng dẫn về nghiệp vụ vận tải hành khách và an toàn giao thông theo quy định (đối với hình thức kinh doanh vận tải có quy định lái xe, nhân viên phục vụ trên xe phải được tập huấn, hướng dẫn nghiệp vụ), trừ các hành vi vi phạm quy định tại điểm c, điểm d khoản này;
> c) Sử dụng lái xe, người quản lý trên xe để tham gia kinh doanh vận tải bằng xe ô tô mà không được hướng dẫn về quy trình bảo đảm an toàn khi đưa đón trẻ em mầm non, học sinh;
> d) Sử dụng lái xe, người áp tải vận chuyển hàng hóa nguy hiểm mà không được tập huấn về vận chuyển hàng hóa nguy hiểm;
> đ) Sử dụng xe ô tô kinh doanh vận tải hành khách không có dây đai an toàn tại các vị trí ghế ngồi, giường nằm …

- BienPhapBoSung: buộc cấp thẻ nhận dạng lái xe cho lái xe theo quy định (nêu tại ND168-2024/D26/K13/a)
- BienPhapBoSung: buộc tổ chức tập huấn, hướng dẫn nghiệp vụ, quy trình hoặc tổ chức khám sức khỏe định kỳ cho lái xe và nhân viên phục vụ trên xe theo quy định (nêu tại ND168-2024/D26/K13/b)
- BienPhapBoSung: buộc lắp đặt thiết bị giám sát hành trình, thiết bị ghi nhận hình ảnh người lái xe, thiết bị ghi nhận hình ảnh khoang chở khách, dây đai an toàn, ghế ngồi cho trẻ em mầm non, học sinh tiểu học trên xe theo đúng quy định (nêu tại ND168-2024/D26/K13/c)
- CheTai tuoc_quyen: 1–3 tháng phù hiệu (nêu tại ND168-2024/D26/K12)
- CheTai phat_tien: 3.000.000–4.000.000 đồng (nêu tại ND168-2024/D26/K4)
- CheTai phat_tien: 6.000.000–8.000.000 đồng (nêu tại ND168-2024/D26/K4)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D26/K4"], "required_numbers": [{"value": 1, "unit": "thang"}, {"value": 3, "unit": "thang"}, {"value": 3000000, "unit": "vnd"}, {"value": 4000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}, {"value": 8000000, "unit": "vnd"}]}
```

### W-bien_phap-019 · tier A · ND168-2024/D32/K16

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D32/K16#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
> 16. Phạt tiền từ 65.000.000 đồng đến 75.000.000 đồng đối với cá nhân, từ 130.000.000 đồng đến 150.000.000 đồng đối với tổ chức là chủ xe ô tô, xe máy chuyên dùng và các loại xe tương tự xe ô tô khi thực hiện một trong các hành vi vi phạm sau đây:
> a) Giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm a khoản 5 Điều 34 của Nghị định này hoặc trực tiếp điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm a khoản 5 Điều 34 của Nghị định này;
> b) Giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm a, điểm b khoản 8 Điều 21 của Nghị định này hoặc trực tiếp điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm a, điểm b khoản 8 Điều 21 của Nghị định này;
> c) Tự ý thay đổi tổng thành khung, tổng thành máy (động cơ), hệ thống phanh, hệ thống truyền động (truyền lực), hệ thống chuyển động hoặc tự ý cải tạo kết cấu, hình dáng, kích thước của xe không đúng thiết kế của nhà sản xuất hoặc thiết kế trong …

- BienPhapBoSung: buộc khôi phục lại hình dáng, kích thước, tình trạng an toàn kỹ thuật ban đầu của xe và đăng kiểm lại trước khi đưa phương tiện ra tham gia giao thông (nêu tại ND168-2024/D32/K19/d)
- BienPhapBoSung: phải khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND168-2024/D32/K19/e)
- BienPhapBoSung: buộc thực hiện điều chỉnh thùng xe theo đúng quy định hiện hành, đăng kiểm lại và điều chỉnh lại khối lượng hàng hóa cho phép chuyên chở ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường theo quy định hiện hành trước khi đưa phương tiện ra tham gia giao thông (nêu tại ND168-2024/D32/K19/đ)
- CheTai phat_tien: 65.000.000–75.000.000 đồng (nêu tại ND168-2024/D32/K16)
- CheTai phat_tien: 130.000.000–150.000.000 đồng (nêu tại ND168-2024/D32/K16)
- CheTai tuoc_quyen: 1–3 tháng chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường và tem kiểm định của phương tiện (nêu tại ND168-2024/D32/K18/c)
- CheTai tuoc_quyen: 1–3 tháng chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường và tem kiểm định của phương tiện (nêu tại ND168-2024/D32/K18/d)
- CheTai tuoc_quyen: 1–3 tháng phù hiệu (nêu tại ND168-2024/D32/K18/đ)
- DiemGPLX: trừ 4 điểm (nêu tại ND168-2024/D32/K21/c)
- DiemGPLX: trừ 10 điểm (nêu tại ND168-2024/D32/K21/g)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D32/K16"], "required_numbers": [{"value": 65000000, "unit": "vnd"}, {"value": 75000000, "unit": "vnd"}, {"value": 130000000, "unit": "vnd"}, {"value": 150000000, "unit": "vnd"}, {"value": 1, "unit": "thang"}, {"value": 3, "unit": "thang"}, {"value": 4, "unit": "diem"}, {"value": 10, "unit": "diem"}]}
```

### W-bien_phap-020 · tier A · ND168-2024/D39/K7

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D39/K7#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 39. Xử phạt các hành vi vi phạm quy định về đào tạo, sát hạch lái xe
> 7. Phạt tiền từ 40.000.000 đồng đến 50.000.000 đồng đối với trung tâm sát hạch lái xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Tự ý thay đổi hoặc sử dụng phần mềm sát hạch, thiết bị chấm điểm, xe sát hạch khi chưa được sự chấp thuận của cơ quan quản lý nhà nước có thẩm quyền;
> b) Sử dụng máy tính trong phòng sát hạch lý thuyết kết nối với đường truyền ra ngoài phòng thi trái quy định;
> c) Cố tình để phương tiện, trang thiết bị chấm điểm hoạt động không chính xác trong kỳ sát hạch; để các dấu hiệu, ký hiệu trái quy định trên sân sát hạch, xe sát hạch trong kỳ sát hạch.

- CheTai phat_tien: 40.000.000–50.000.000 đồng (nêu tại ND168-2024/D39/K7)
- CheTai tuoc_quyen: 2–4 tháng giấy phép sát hạch (nêu tại ND168-2024/D39/K9/d)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D39/K7"], "required_numbers": [{"value": 40000000, "unit": "vnd"}, {"value": 50000000, "unit": "vnd"}, {"value": 2, "unit": "thang"}, {"value": 4, "unit": "thang"}]}
```

### W-bien_phap-021 · tier A · ND168-2024/D34/K3

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D34/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 34. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển quá khổ giới hạn, xe quá tải trọng, xe bánh xích lưu hành đường bộ (kể cả xe ô tô chở hành khách)
> 3. Phạt tiền từ 8.000.000 đồng đến 10.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Chở hàng vượt khổ giới hạn của xe hoặc của đường bộ ghi trong giấy phép lưu hành;
> b) Điều khiển xe bánh xích tham gia giao thông không có giấy phép lưu hành hoặc có giấy phép lưu hành nhưng không còn giá trị sử dụng theo quy định hoặc lưu thông trực tiếp trên đường mà không thực hiện biện pháp bảo vệ đường theo quy định;
> c) Điều khiển xe có kích thước bao ngoài vượt quá khép giới hạn của đường bộ hoặc chở hàng vượt khổ giới hạn của đường bộ hoặc chở hàng vượt quá kích thước giới hạn xếp hàng hóa của xe tham gia giao thông, trừ trường hợp có giấy phép lưu hành còn giá trị sử dụng;
> d) Điều khiển xe có kích thước bao ngoài vượt quá kích thước giới hạn cho phép của xe theo quy định, trừ trường hợp có giấy phép lưu hành còn giá trị sử dụng.

- BienPhapBoSung: buộc khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND168-2024/D34/K6)
- CheTai phat_tien: 8.000.000–10.000.000 đồng (nêu tại ND168-2024/D34/K3)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D34/K7/a)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D34/K3"], "required_numbers": [{"value": 8000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}]}
```

### W-bien_phap-022 · tier A · ND168-2024/D32/K11

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D32/K11#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
> 11. Phạt tiền từ 10.000.000 đồng đến 12.000.000 đồng đối với cá nhân, từ 20.000.000 đồng đến 24.000.000 đồng đối với tổ chức là chủ xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ, xe máy chuyên dùng và các loại xe tương tự xe ô tô thực hiện một trong các hành vi vi phạm sau đây:
> a) Đưa xe cơ giới, xe máy chuyên dùng không có giấy chứng nhận hoặc tem kiểm định an toàn kỹ thuật và bảo vệ môi trường (đối với loại xe có quy định phải kiểm định) hoặc có nhưng đã hết hiệu lực (hạn sử dụng) từ 01 tháng trở lên (kể cả rơ moóc và sơ mi rơ moóc) tham gia giao thông;
> b) Giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm a, điểm d khoản 5 Điều 21 của Nghị định này hoặc trực tiếp điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm a, điểm d khoản 5 Điều 21 của Nghị định này;
> c) Giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại khoản 2 Điều 34 của Nghị định này hoặc trực tiếp điều …

- BienPhapBoSung: buộc khôi phục lại hình dáng, kích thước, tình trạng an toàn kỹ thuật ban đầu của xe và đăng kiểm lại trước khi đưa phương tiện ra tham gia giao thông (nêu tại ND168-2024/D32/K19/d)
- BienPhapBoSung: phải khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND168-2024/D32/K19/e)
- BienPhapBoSung: buộc thực hiện điều chỉnh thùng xe theo đúng quy định hiện hành, đăng kiểm lại và điều chỉnh lại khối lượng hàng hóa cho phép chuyên chở ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường theo quy định hiện hành trước khi đưa phương tiện ra tham gia giao thông (nêu tại ND168-2024/D32/K19/đ)
- CheTai phat_tien: 10.000.000–12.000.000 đồng (nêu tại ND168-2024/D32/K11)
- CheTai phat_tien: 20.000.000–24.000.000 đồng (nêu tại ND168-2024/D32/K11)
- CheTai tuoc_quyen: 1–3 tháng chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường và tem kiểm định của phương tiện (nêu tại ND168-2024/D32/K18/c)
- CheTai tuoc_quyen: 1–3 tháng chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường và tem kiểm định của phương tiện (nêu tại ND168-2024/D32/K18/d)
- CheTai tuoc_quyen: 1–3 tháng phù hiệu (nêu tại ND168-2024/D32/K18/đ)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D32/K21/a)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D32/K11"], "required_numbers": [{"value": 10000000, "unit": "vnd"}, {"value": 12000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}, {"value": 24000000, "unit": "vnd"}, {"value": 1, "unit": "thang"}, {"value": 3, "unit": "thang"}, {"value": 2, "unit": "diem"}]}
```

### W-bien_phap-023 · tier A · ND168-2024/D32/K12

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D32/K12#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
> 12. Phạt tiền từ 16.000.000 đồng đến 18.000.000 đồng đối với cá nhân, từ 32.000.000 đồng đến 36.000.000 đồng đối với tổ chức là chủ xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ, xe máy chuyên dùng và các loại xe tương tự xe ô tô, phương tiện giao thông thông minh thực hiện một trong các hành vi vi phạm sau đây:
> a) Đưa phương tiện không có chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe) tham gia giao thông hoặc có nhưng đã hết hạn sử dụng, hết hiệu lực; đưa phương tiện có chứng nhận đăng ký xe tạm thời, phương tiện có phạm vi hoạt động hạn chế tham gia giao thông quá thời hạn, tuyến đường, phạm vi cho phép;
> b) Đưa phương tiện không gắn biển số (đối với loại xe có quy định phải gắn biển số) tham gia giao thông;
> c) Lắp đặt, sử dụng thiết bị thay đổi biển số trên xe trái quy định (kể cả rơ moóc và sơ mi rơ moóc);
> d) Đưa …

- BienPhapBoSung: buộc làm thủ tục đổi, thu hồi, cấp mới, cấp chứng nhận đăng ký xe, biển số xe, chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường theo quy định (trừ trường hợp bị tịch thu phương tiện) (nêu tại ND168-2024/D32/K19/g)
- CheTai phat_tien: 16.000.000–18.000.000 đồng (nêu tại ND168-2024/D32/K12)
- CheTai phat_tien: 32.000.000–36.000.000 đồng (nêu tại ND168-2024/D32/K12)
- CheTai tich_thu: biển số (nêu tại ND168-2024/D32/K18/a)
- CheTai tich_thu: biển số, thiết bị thay đổi biển số (nêu tại ND168-2024/D32/K18/a)
- CheTai tich_thu: phương tiện (nêu tại ND168-2024/D32/K18/b)
- CheTai tich_thu: phương tiện) (nêu tại ND168-2024/D32/K19/g)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D32/K21/a)
- DiemGPLX: trừ 6 điểm (nêu tại ND168-2024/D32/K21/đ)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D32/K12"], "required_numbers": [{"value": 16000000, "unit": "vnd"}, {"value": 18000000, "unit": "vnd"}, {"value": 32000000, "unit": "vnd"}, {"value": 36000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}, {"value": 6, "unit": "diem"}]}
```

### W-bien_phap-024 · tier A · ND168-2024/D13/K8

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D13/K8#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 13. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo), xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tư xe ô tô vi phạm quy định về điều kiện của phương tiện khi tham gia giao thông
> 8. Phạt tiền từ 20.000.000 đồng đến 26.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe gắn biển số không đúng với chứng nhận đăng ký xe hoặc gắn biển số không do cơ quan có thẩm quyền cấp (kể cả rơ moóc và sơ mi rơ moóc);
> b) Điều khiển xe không gắn đủ biển số hoặc gắn biển số không đúng vị trí, không đúng quy cách theo quy định; gắn biển số không rõ chữ, số hoặc sơn, dán lên chữ, số của biển số xe; gắn biển số bị bẻ cong, che lấp, làm thay đổi chữ, số, màu sắc (của chữ, số, nền biển số xe), hình dạng, kích thước của biển số xe; sử dụng chất liệu, vật liệu, thiết bị làm thay đổi khả năng nhận diện thông tin biển số xe của phương tiện, thiết bị kỹ thuật nghiệp vụ (kể cả rơ moóc và sơ mi rơ moóc).

- BienPhapBoSung: buộc lắp đầy đủ thiết bị hoặc thay thế thiết bị đủ tiêu chuẩn, quy chuẩn an toàn kỹ thuật hoặc khôi phục lại tính năng kỹ thuật của thiết bị theo quy định (nêu tại ND168-2024/D13/K11/a)
- BienPhapBoSung: buộc thực hiện đúng quy định về biển số hoặc khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND168-2024/D13/K11/a)
- CheTai tich_thu: biển số xe (nêu tại ND168-2024/D13/K10/a)
- CheTai phat_tien: 20.000.000–26.000.000 đồng (nêu tại ND168-2024/D13/K8)
- DiemGPLX: trừ 6 điểm (nêu tại ND168-2024/D13/K13/b)
- DiemGPLX: trừ 10 điểm (nêu tại ND168-2024/D13/K13/c)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D13/K8"], "required_numbers": [{"value": 20000000, "unit": "vnd"}, {"value": 26000000, "unit": "vnd"}, {"value": 6, "unit": "diem"}, {"value": 10, "unit": "diem"}]}
```

### W-bien_phap-025 · tier A · ND168-2024/D31/K1

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D31/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 31. Xử phạt hành vi sản xuất, lắp ráp trái phép phương tiện giao thông cơ giới đường bộ; sản xuất, mua, bán biển số xe trái phép
> 1. Phạt tiền từ 10.000.000 đồng đến 12.000.000 đồng đối với cá nhân, từ 20.000.000 đồng đến 24.000.000 đồng đối với tổ chức thực hiện hành vi mua, bán biển số xe không phải là biển số do cơ quan nhà nước có thẩm quyền sản xuất hoặc không được cơ quan nhà nước có thẩm quyền cho phép.

- BienPhapBoSung: buộc nộp lại số lợi bất hợp pháp có được do thực hiện vi phạm hành chính (nêu tại ND168-2024/D31/K4)
- CheTai phat_tien: 10.000.000–12.000.000 đồng (nêu tại ND168-2024/D31/K1)
- CheTai phat_tien: 20.000.000–24.000.000 đồng (nêu tại ND168-2024/D31/K1)
- CheTai tich_thu: biển số, phương tiện sản xuất, lắp ráp trái phép (nêu tại ND168-2024/D31/K3)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D31/K1"], "required_numbers": [{"value": 10000000, "unit": "vnd"}, {"value": 12000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}, {"value": 24000000, "unit": "vnd"}]}
```

### W-bien_phap-026 · tier A · ND168-2024/D7/K9

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D7/K9#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 7. Xử phạt, trừ điểm giấy phép lái của người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy vi phạm quy tắc giao thông đường bộ
> 9. Phạt tiền từ 8.000.000 đồng đến 10.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe lạng lách, đánh võng trên đường bộ; sử dụng chân chống hoặc vật khác quệt xuống đường khi xe đang chạy;
> b) Điều khiển xe thành nhóm từ 02 xe trở lên chạy quá tốc độ quy định;
> c) Gây tai nạn giao thông không dừng ngay phương tiện, không giữ nguyên hiện trường, không trợ giúp người bị nạn, không ở lại hiện trường hoặc không đến trình báo ngay với cơ quan công an, Ủy ban nhân dân nơi gần nhất;
> d) Điều khiển xe trên đường mà trong máu hoặc hơi thở có nồng độ cồn vượt quá 80 miligam/100 mililít máu hoặc vượt quá 0,4 miligam/1 lít khí thở;
> đ) Không chấp hành yêu cầu kiểm tra về nồng độ cồn của người thi hành công vụ;
> e) Điều khiển xe trên đường mà trong cơ thể có chất ma túy hoặc chất kích thích khác mà pháp luật cấm sử dụng;
> g) Không chấp hành yêu cầu kiểm tra về chất ma túy hoặc chất kích thích khác mà pháp luật cấm sử dụng của người thi hành công vụ;
> h) Ngồi …

- CheTai tuoc_quyen: 10–12 tháng giấy phép lái xe (nêu tại ND168-2024/D7/K12/b)
- CheTai tuoc_quyen: 22–24 tháng giấy phép lái xe (nêu tại ND168-2024/D7/K12/c)
- CheTai phat_tien: 8.000.000–10.000.000 đồng (nêu tại ND168-2024/D7/K9)
- DiemGPLX: trừ 6 điểm (nêu tại ND168-2024/D7/K13/c)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D7/K9"], "required_numbers": [{"value": 10, "unit": "thang"}, {"value": 12, "unit": "thang"}, {"value": 22, "unit": "thang"}, {"value": 24, "unit": "thang"}, {"value": 8000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}, {"value": 6, "unit": "diem"}]}
```

### W-bien_phap-027 · tier A · ND168-2024/D31/K3

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D31/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 31. Xử phạt hành vi sản xuất, lắp ráp trái phép phương tiện giao thông cơ giới đường bộ; sản xuất, mua, bán biển số xe trái phép
> 3. Ngoài việc bị phạt tiền, cá nhân, tổ chức thực hiện hành vi vi phạm quy định tại khoản 1, khoản 2 Điều này còn bị áp dụng hình thức xử phạt bổ sung tịch thu biển số, phương tiện sản xuất, lắp ráp trái phép.

- CheTai tich_thu: biển số, phương tiện sản xuất, lắp ráp trái phép (nêu tại ND168-2024/D31/K3)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D31/K3"], "required_numbers": []}
```

### W-bien_phap-028 · tier A · ND168-2024/D12/K16

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D12/K16#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 12. Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm khác về quy tắc giao thông đường bộ; sử dụng lòng đường, vỉa hè vào mục đích khác
> 16. Ngoài việc bị áp dụng hình thức xử phạt, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị áp dụng các biện pháp khắc phục hậu quả sau đây:
> a) Thực hiện hành vi quy định tại khoản 3 Điều này buộc phá dỡ các vật che khuất biển báo hiệu đường bộ, đèn tín hiệu giao thông;
> b) Thực hiện hành vi quy định tại khoản 12 Điều này buộc khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra.

- BienPhapBoSung: buộc phá dỡ các vật che khuất biển báo hiệu đường bộ, đèn tín hiệu giao thông (nêu tại ND168-2024/D12/K16/a)
- BienPhapBoSung: buộc khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND168-2024/D12/K16/b)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D12/K16"], "required_numbers": []}
```

### W-bien_phap-029 · tier B · ND336-2025/D12/K6

Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)

`ND336-2025/D12/K6#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 12. Xử phạt các hành vi vi phạm quy định về vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
> 6. Phạt tiền từ 12.000.000 đồng đến 16.000.000 đồng đối với cá nhân, từ 24.000.000 đồng đến 32.000.000 đồng đối với tổ chức kinh doanh vận tải, dịch vụ hỗ trợ vận tải thực hiện một trong các hành vi vi phạm sau đây:
> a) Kinh doanh vận tải bằng xe ô tô, xe bốn bánh có gắn động cơ mà không có giấy phép kinh doanh vận tải theo quy định, trừ hành vi quy định tại điểm i khoản này;
> b) Thực hiện không đúng hình thức kinh doanh đã đăng ký trong giấy phép kinh doanh vận tải;
> c) Thành lập, tổ chức điểm giao dịch đón, trả khách, bốc dỡ hàng hóa trái phép;
> d) Không xây dựng quy trình đảm bảo an toàn giao thông cho xe ra, vào bến hoặc có xây dựng nhưng thực hiện không đúng, không đầy đủ quy trình đảm bảo an toàn giao thông cho xe ra, vào bến; không niêm yết hoặc niêm yết không đầy đủ, chính xác các thông tin tại bến xe theo quy định;
> đ) Không gửi hóa đơn điện tử, không gửi nội dung tối thiểu của hợp đồng điện tử theo quy định;
> e) Không thực hiện hoặc thực hiện không đầy đủ, không đúng quy định về quản lý, áp dụng thông tin từ phần mềm quản lý bến xe khách;
> g) Sử dụng hợp đồng điện tử không có giao …

- CheTai phat_tien: 12.000.000–16.000.000 đồng (nêu tại ND336-2025/D12/K6)
- CheTai phat_tien: 24.000.000–32.000.000 đồng (nêu tại ND336-2025/D12/K6)
- CheTai tuoc_quyen: 1–3 tháng giấy phép kinh doanh vận tải (nêu tại ND336-2025/D12/K8/b)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "B", "answer": "", "gold_units": ["ND336-2025/D12/K6"], "required_numbers": [{"value": 12000000, "unit": "vnd"}, {"value": 16000000, "unit": "vnd"}, {"value": 24000000, "unit": "vnd"}, {"value": 32000000, "unit": "vnd"}, {"value": 1, "unit": "thang"}, {"value": 3, "unit": "thang"}]}
```

### W-bien_phap-030 · tier B · ND336-2025/D5/K7

Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)

`ND336-2025/D5/K7#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 5. Xử phạt các hành vi vi phạm quy định về sử dụng, khai thác trong phạm vi đất dành cho kết cấu hạ tầng đường bộ
> 7. Ngoài việc bị áp dụng hình thức xử phạt, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị áp dụng các biện pháp khắc phục hậu quả sau đây:
> a) Thực hiện hành vi vi phạm quy định tại khoản 1 Điều này buộc di dời cây trồng che khuất tầm nhìn của người điều khiển phương tiện, biển báo hiệu đường bộ;
> b) Thực hiện hành vi vi phạm quy định tại điểm a khoản 2 Điều này buộc phá dỡ công trình, phần công trình xây dựng không có giấy phép và khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra;
> c) Thực hiện hành vi vi phạm quy định tại điểm b, điểm c khoản 2 Điều này buộc thu dọn băng rôn, biển hiệu, bảng quảng cáo;
> d) Thực hiện hành vi vi phạm quy định tại điểm d khoản 2, điểm a khoản 4 Điều này buộc thu dọn rác thải, chất phế thải, vật liệu;
> đ) Thực hiện hành vi vi phạm quy định tại khoản 3, điểm d khoản 4; điểm a khoản 5; điểm a, điểm b, điểm d khoản 6 Điều này buộc phá dỡ công trình, phần công trình xây dựng không có giấy phép hoặc xây dựng không đúng với giấy phép và khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây …

- BienPhapBoSung: buộc di dời cây trồng che khuất tầm nhìn của người điều khiển phương tiện, biển báo hiệu đường bộ (nêu tại ND336-2025/D5/K7/a)
- BienPhapBoSung: buộc phá dỡ công trình, phần công trình xây dựng không có giấy phép và khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND336-2025/D5/K7/b)
- BienPhapBoSung: buộc thu dọn băng rôn, biển hiệu, bảng quảng cáo (nêu tại ND336-2025/D5/K7/c)
- BienPhapBoSung: buộc thu dọn rác thải, chất phế thải, vật liệu (nêu tại ND336-2025/D5/K7/d)
- BienPhapBoSung: buộc khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND336-2025/D5/K7/e)
- BienPhapBoSung: buộc tháo dỡ vật gắn, treo, lắp vào công trình báo hiệu đường bộ và khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND336-2025/D5/K7/g)
- BienPhapBoSung: buộc phá dỡ công trình, phần công trình xây dựng không có giấy phép hoặc xây dựng không đúng với giấy phép và khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND336-2025/D5/K7/đ)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "B", "answer": "", "gold_units": ["ND336-2025/D5/K7"], "required_numbers": []}
```

### W-bien_phap-031 · tier B · ND336-2025/D8/K8

Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)

`ND336-2025/D8/K8#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 8. Xử phạt các hành vi vi phạm quy định về thi công trong phạm vi bảo vệ kết cấu hạ tầng đường bộ
> 8. Ngoài việc bị áp dụng hình thức xử phạt, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị áp dụng các biện pháp khắc phục hậu quả sau đây:
> a) Thực hiện hành vi vi phạm quy định tại điểm b, điểm c khoản 2 Điều này buộc thu dọn phương tiện, vật tư, vật liệu, đất đá, hàng hóa, máy móc, thiết bị, các loại vật dụng, vật cản khác;
> b) Thực hiện hành vi vi phạm quy định tại điểm c, điểm d khoản 4 Điều này buộc phá dỡ công trình, phần công trình xây dựng không có giấy phép hoặc xây dựng không đúng với giấy phép và khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra.

- BienPhapBoSung: buộc thu dọn phương tiện, vật tư, vật liệu, đất đá, hàng hóa, máy móc, thiết bị, các loại vật dụng, vật cản khác (nêu tại ND336-2025/D8/K8/a)
- BienPhapBoSung: buộc phá dỡ công trình, phần công trình xây dựng không có giấy phép hoặc xây dựng không đúng với giấy phép và khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND336-2025/D8/K8/b)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "B", "answer": "", "gold_units": ["ND336-2025/D8/K8"], "required_numbers": []}
```

### W-bien_phap-032 · tier B · ND336-2025/D5/K2

Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)

`ND336-2025/D5/K2#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 5. Xử phạt các hành vi vi phạm quy định về sử dụng, khai thác trong phạm vi đất dành cho kết cấu hạ tầng đường bộ
> 2. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với cá nhân, từ 2.000.000 đồng đến 4.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
> a) Dựng cổng chào trái phép trong phạm vi đất dành cho kết cấu hạ tầng đường bộ gây ảnh hưởng đến an toàn giao thông đường bộ;
> b) Treo băng rôn trái phép trong phạm vi đất của đường bộ gây ảnh hưởng đến an toàn giao thông đường bộ;
> c) Đặt, treo biển hiệu, bảng quảng cáo trên đất của đường bộ ở đoạn đường ngoài đô thị trừ việc đặt, treo biển hiệu, bảng quảng cáo tại lòng đường và trừ hành vi vi phạm quy định tại điểm a khoản 5 Điều này;
> d) Đổ rác thải ra đường bộ không đúng nơi quy định, trừ hành vi vi phạm quy định tại điểm a khoản 4 Điều này.

- BienPhapBoSung: buộc phá dỡ công trình, phần công trình xây dựng không có giấy phép và khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND336-2025/D5/K7/b)
- BienPhapBoSung: buộc thu dọn băng rôn, biển hiệu, bảng quảng cáo (nêu tại ND336-2025/D5/K7/c)
- BienPhapBoSung: buộc thu dọn rác thải, chất phế thải, vật liệu (nêu tại ND336-2025/D5/K7/d)
- CheTai phat_tien: 1.000.000–2.000.000 đồng (nêu tại ND336-2025/D5/K2)
- CheTai phat_tien: 2.000.000–4.000.000 đồng (nêu tại ND336-2025/D5/K2)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "B", "answer": "", "gold_units": ["ND336-2025/D5/K2"], "required_numbers": [{"value": 1000000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}, {"value": 4000000, "unit": "vnd"}]}
```

### W-bien_phap-033 · tier B · ND336-2025/D5/K1

Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)

`ND336-2025/D5/K1#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 5. Xử phạt các hành vi vi phạm quy định về sử dụng, khai thác trong phạm vi đất dành cho kết cấu hạ tầng đường bộ
> 1. Phạt tiền từ 500.000 đồng đến 1.000.000 đồng đối với cá nhân, từ 1.000.000 đồng đến 2.000.000 đồng đối với tổ chức thực hiện hành vi vi phạm trồng cây trong phạm vi hành lang an toàn đường bộ làm che khuất tầm nhìn của người điều khiển phương tiện giao thông hoặc che lấp báo hiệu đường bộ, trừ hành vi vi phạm quy định tại điểm c khoản 4 Điều này.

- BienPhapBoSung: buộc di dời cây trồng che khuất tầm nhìn của người điều khiển phương tiện, biển báo hiệu đường bộ (nêu tại ND336-2025/D5/K7/a)
- CheTai phat_tien: 500.000–1.000.000 đồng (nêu tại ND336-2025/D5/K1)
- CheTai phat_tien: 1.000.000–2.000.000 đồng (nêu tại ND336-2025/D5/K1)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "B", "answer": "", "gold_units": ["ND336-2025/D5/K1"], "required_numbers": [{"value": 500000, "unit": "vnd"}, {"value": 1000000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}]}
```

### W-bien_phap-034 · tier B · ND336-2025/D5/K6

Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)

`ND336-2025/D5/K6#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 5. Xử phạt các hành vi vi phạm quy định về sử dụng, khai thác trong phạm vi đất dành cho kết cấu hạ tầng đường bộ
> 6. Phạt tiền từ 15.000.000 đồng đến 20.000.000 đồng đối với cá nhân, từ 30.000.000 đồng đến 40.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
> a) Chiếm dụng đất của đường bộ hoặc đất hành lang an toàn đường bộ để xây dựng nhà ở;
> b) Đấu nối trái phép vào đường chính, đường nhánh;
> c) Tháo dỡ, di chuyển trái phép hoặc làm sai lệch công trình đường bộ;
> d) Xây dựng, lắp đặt biển quảng cáo trong phạm vi hành lang an toàn đường cao tốc.

- BienPhapBoSung: buộc khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND336-2025/D5/K7/e)
- BienPhapBoSung: buộc phá dỡ công trình, phần công trình xây dựng không có giấy phép hoặc xây dựng không đúng với giấy phép và khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND336-2025/D5/K7/đ)
- CheTai phat_tien: 15.000.000–20.000.000 đồng (nêu tại ND336-2025/D5/K6)
- CheTai phat_tien: 30.000.000–40.000.000 đồng (nêu tại ND336-2025/D5/K6)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "B", "answer": "", "gold_units": ["ND336-2025/D5/K6"], "required_numbers": [{"value": 15000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}, {"value": 30000000, "unit": "vnd"}, {"value": 40000000, "unit": "vnd"}]}
```

### W-bien_phap-035 · tier B · ND336-2025/D10/K2

Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)

`ND336-2025/D10/K2#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 10. Xử phạt các hành vi vi phạm về thanh toán điện tử giao thông đường bộ, hoạt động trạm thu phí đường bộ
> 2. Phạt tiền từ 10.000.000 đồng đến 20.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
> a) Không thực hiện công khai, niêm yết công khai tại trạm thu phí theo quy định;
> b) Tổ chức bán vé, soát vé không kịp thời, sách nhiễu đối với người mua vé; không bán đầy đủ hoặc hạn chế, giới hạn thời gian bán các loại vé tháng, vé quý theo quy định;
> c) Nhận tiền mặt của người sử dụng phương tiện giao thông đường bộ mà không giao vé hoặc giao vé không đúng chủng loại phương tiện lưu thông qua trạm thu phí;
> d) Không thực hiện đúng quy trình nghiệp vụ để phương tiện giao thông đường bộ (đối tượng phải mua vé) không có vé đi qua trạm thu phí.

- BienPhapBoSung: buộc nộp lại số lợi bất hợp pháp (nếu có) có được do thực hiện vi phạm hành chính (nêu tại ND336-2025/D10/K7/a)
- CheTai phat_tien: 10.000.000–20.000.000 đồng (nêu tại ND336-2025/D10/K2)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "bien_phap", "tier": "B", "answer": "", "gold_units": ["ND336-2025/D10/K2"], "required_numbers": [{"value": 10000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}]}
```

## hanh_vi_cam_nghia_vu — hành vi bị cấm / nghĩa vụ, quy tắc phải tuân thủ

### W-hanh_vi_cam_nghia_vu-001 · tier A · LUAT36-2024/D57/K8

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D57/K8#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 57. Giấy phép lái xe
> 8. Giấy phép lái xe quốc tế được quy định như sau:
> a) Giấy phép lái xe quốc tế là giấy phép lái xe do cơ quan nhà nước có thẩm quyền của quốc gia là thành viên của Công ước Viên cấp theo một mẫu thống nhất; có thời hạn không quá 03 năm kể từ ngày cấp và phải phù hợp với thời hạn còn hiệu lực của giấy phép lái xe quốc gia;
> b) Người có giấy phép lái xe quốc tế do quốc gia là thành viên của Công ước Viên cấp khi lái xe tham gia giao thông đường bộ trên lãnh thổ Việt Nam phải mang theo giấy phép lái xe quốc tế và giấy phép lái xe quốc gia được cấp phù hợp với hạng xe điều khiển, còn thời hạn sử dụng; phải tuân thủ pháp luật về trật tự, an toàn giao thông đường bộ của Việt Nam;
> c) Người có giấy phép lái xe quốc tế vi phạm pháp luật về trật tự, an toàn giao thông đường bộ của Việt Nam mà bị tước quyền sử dụng giấy phép lái xe có thời hạn thì thời gian bị tước quyền sử dụng không quá thời gian người lái xe được phép cư trú tại lãnh thổ Việt Nam;
> d) Người Việt Nam hoặc người nước ngoài có thẻ thường trú hoặc thẻ tạm trú tại Việt Nam có giấy phép lái xe do Việt Nam hoặc quốc gia là thành viên của điều ước quốc tế mà nước Cộng hòa xã hội chủ nghĩa Việt Nam là thành …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D57/K8"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-002 · tier A · TT12-2025-BCA/D31/K2

Thông tư số 12/2025/TT-BCA (Quy định về sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế)

`TT12-2025-BCA/D31/K2#2025-03-01` · hiệu lực 2025-03-01 → nay

> Điều 31. Nguyên tắc và hình thức khai thác dữ liệu trên hệ thống thông tin về sát hạch, cấp giấy phép lái xe
> 2. Hình thức khai thác
> a) Khai thác trực tiếp: Cơ quan, tổ chức, cá nhân được khai thác dữ liệu giấy phép lái xe trực tiếp từ trang thông tin điện tử giấy phép lái xe theo quy định về cấp độ bảo mật và phân quyền sử dụng, khai thác dữ liệu giấy phép lái xe;
> b) Khai thác gián tiếp: Cơ quan, tổ chức, cá nhân có nhu cầu khai thác dữ liệu giấy phép lái xe cung cấp thông tin lấy từ cơ sở dữ liệu giấy phép lái xe, bao gồm: các thông tin ghi trên giấy phép lái xe (trường hợp có yêu cầu của cơ quan có thẩm quyền, ngoài thông tin in trên giấy phép lái xe còn được cung cấp thêm thông tin về đào tạo, sát hạch, vi phạm pháp luật giao thông đường bộ).


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["TT12-2025-BCA/D31/K2"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-003 · tier A · TT14-2025-BXD/D13/K3

Thông tư số 14/2025/TT-BXD (Quy định về đào tạo lái xe; bồi dưỡng, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ)

`TT14-2025-BXD/D13/K3#2025-09-01` · hiệu lực 2025-09-01 → nay

> Điều 13. Yêu cầu đối với người học lái xe
> 3. Người đã có giấy phép lái xe hạng B chuyển số tự động được đăng ký học để cấp mới giấy phép lái xe hạng B chuyển số cơ khí (số sàn), người đã có giấy phép lái xe hạng B được đăng ký học để cấp mới giấy phép lái xe hạng C1 theo quy định tại Điều 6 Thông tư này; hồ sơ của người học lái xe thực hiện theo quy định tại khoản 1 Điều 14 Thông tư này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["TT14-2025-BXD/D13/K3"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-004 · tier A · TT79-2024-BCA/D5/K2

Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)

`TT79-2024-BCA/D5/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 5. Trách nhiệm của cơ quan đăng ký xe và cán bộ đăng ký xe
> 2. Tiếp nhận, kiểm tra hồ sơ xe, kiểm tra thực tế xe, chà số máy, số khung xe và thực hiện số hóa hồ sơ xe lên hệ thống đăng ký, quản lý xe.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["TT79-2024-BCA/D5/K2"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-005 · tier A · LUAT36-2024/D52/K2

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D52/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 52. Bảo đảm trật tự, an toàn giao thông đường bộ đối với xe quá khổ giới hạn, xe quá tải trọng, xe bánh xích lưu hành trên đường bộ
> 2. Xe quá tải trọng bao gồm:
> a) Xe cơ giới, xe máy chuyên dùng có khối lượng toàn bộ vượt quá khối lượng cho phép của xe hoặc vượt quá tải trọng của đường bộ;
> b) Xe cơ giới, xe máy chuyên dùng có khối lượng toàn bộ phân bổ lên trục xe, cụm trục xe vượt quá tải trọng của trục xe, cụm trục xe hoặc vượt quá tải trọng của đường bộ.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D52/K2"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-006 · tier A · LUAT35-2024/D47/K4

Luật Đường bộ số 35/2024/QH15

`LUAT35-2024/D47/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 47. Đầu tư, xây dựng, phát triển đường cao tốc
> 4. Việc đầu tư đường cao tốc qua đô thị phải phù hợp với quy hoạch đô thị và quy định của pháp luật có liên quan; có giải pháp phù hợp để phát triển không gian, kết nối giao thông khu vực hai bên đường, bảo đảm môi trường.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["LUAT35-2024/D47/K4"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-007 · tier A · LUAT36-2024/D23/K3

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D23/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 23. Qua phà, qua cầu phao
> 3. Khi qua phà, phải chấp hành quy định sau đây:
> a) Khi xe xuống phà, đang ở trên phà và khi lên bến, mọi người không được ở trên xe, trừ người lái xe, người điều khiển xe máy chuyên dùng, trẻ em, phụ nữ mang thai, người già yếu, người khuyết tật, người bệnh;
> b) Khi xuống phà, xe cơ giới, xe máy chuyên dùng xuống trước, xe thô sơ, người đi bộ xuống sau; khi lên bến, người đi bộ lên trước, các phương tiện giao thông đường bộ lên sau theo hướng dẫn của người điều khiển giao thông.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D23/K3"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-008 · tier A · LUAT36-2024/D50/K1

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D50/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 50. Bảo đảm trật tự, an toàn giao thông đường bộ đối với phương tiện giao thông đường bộ vận chuyển động vật sống, thực phẩm tươi sống
> 1. Việc vận chuyển động vật sống phải bảo đảm các yêu cầu sau đây:
> a) Người lái xe phải mang đủ giấy tờ theo quy định của pháp luật;
> b) Phương tiện vận chuyển phải có kết cấu phù hợp với loại động vật chuyên chở;
> c) Trong quá trình vận chuyển phải chấp hành các quy định của pháp luật về trật tự, an toàn giao thông đường bộ, vệ sinh dịch tễ, phòng dịch và bảo đảm vệ sinh môi trường.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D50/K1"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-009 · tier A · LUAT35-2024/D35/K6

Luật Đường bộ số 35/2024/QH15

`LUAT35-2024/D35/K6#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 35. Bảo trì kết cấu hạ tầng đường bộ
> 6. Việc sửa chữa kết cấu hạ tầng đường bộ phải bảo đảm quy chuẩn, tiêu chuẩn kỹ thuật, đáp ứng lưu lượng, tải trọng khai thác và tuân thủ quy định của pháp luật về xây dựng, pháp luật về phòng, chống thiên tai và quy định của Luật này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["LUAT35-2024/D35/K6"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-010 · tier A · LUAT36-2024/D60/K5

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D60/K5#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 60. Đào tạo lái xe
> 5. Giấy phép lái xe các hạng C, D1, D2, D, BE, C1E, CE, D1E, D2E, DE phải được đào tạo bằng hình thức đào tạo nâng hạng theo các điều kiện quy định tại khoản 3 và khoản 4 Điều này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D60/K5"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-011 · tier A · LUAT35-2024/D18/K5

Luật Đường bộ số 35/2024/QH15

`LUAT35-2024/D18/K5#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 18. Xây dựng, lắp đặt biển quảng cáo, biển thông tin cổ động, tuyên truyền chính trị trong phạm vi bảo vệ kết cấu hạ tầng đường bộ
> 5. Việc xây dựng, lắp đặt biển thông tin cổ động, tuyên truyền chính trị phải đáp ứng yêu cầu quy định tại khoản 2, khoản 3, điểm b và điểm c khoản 4 Điều này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["LUAT35-2024/D18/K5"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-012 · tier A · TT12-2025-BCA/D9/K2

Thông tư số 12/2025/TT-BCA (Quy định về sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế)

`TT12-2025-BCA/D9/K2#2025-03-01` · hiệu lực 2025-03-01 → nay

> Điều 9. Chuẩn bị kỳ sát hạch
> 2. Kiểm tra hồ sơ
> a) Khi tiếp nhận hồ sơ đề nghị sát hạch cấp giấy phép lái xe, Phòng Cảnh sát giao thông kiểm tra, đối chiếu điều kiện của người dự sát hạch theo quy định tại Điều 15 và Điều 16 Thông tư này; duyệt hồ sơ thí sinh dự sát hạch, lập biên bản kiểm tra hồ sơ theo quy định tại mẫu số 01 Phụ lục VIII ban hành kèm theo Thông tư này và thông báo thời gian, địa điểm tổ chức kỳ sát hạch cho người nộp hồ sơ; báo cáo Giám đốc Công an cấp tỉnh ban hành quyết định tổ chức kỳ sát hạch lái xe; đối với hồ sơ không hợp lệ thì thông báo và hướng dẫn người nộp hồ sơ hoàn thiện theo quy định;
> b) Trường hợp người dự sát hạch giấy phép lái xe hạng A1 là người dân tộc thiểu số không biết đọc, viết tiếng Việt, hồ sơ dự sát hạch phải có xác nhận của Ủy ban nhân dân cấp xã về việc người dân tộc thiểu số không biết đọc, viết tiếng Việt;
> c) Trường hợp người không đạt kết quả sát hạch, có nhu cầu đăng ký sát hạch lại, Phòng Cảnh sát giao thông kiểm tra, đối chiếu với biên bản xác nhận vắng, trượt của Hội đồng sát hạch kỳ trước, trường hợp không có tên thì không được tham dự sát hạch lại.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["TT12-2025-BCA/D9/K2"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-013 · tier A · LUAT35-2024/D72/K3

Luật Đường bộ số 35/2024/QH15

`LUAT35-2024/D72/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 72. Dịch vụ bến xe, trạm dừng nghỉ
> 3. Đơn vị kinh doanh dịch vụ bến xe khách có quyền, nghĩa vụ sau đây:
> a) Sắp xếp xe ô tô có đủ điều kiện kinh doanh vận tải vào bến đón, trả khách;
> b) Cho thuê nơi bán vé hoặc tổ chức bán vé cho hành khách theo hợp đồng với đơn vị kinh doanh vận tải;
> c) Kê khai, niêm yết, công bố thông tin về giá dịch vụ xe ra, vào bến xe khách theo quy định của pháp luật về giá.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["LUAT35-2024/D72/K3"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-014 · tier A · TT12-2025-BCA/D39/K1

Thông tư số 12/2025/TT-BCA (Quy định về sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế)

`TT12-2025-BCA/D39/K1#2025-03-01` · hiệu lực 2025-03-01 → nay

> Điều 39. Trách nhiệm thi hành
> 1. Cục trưởng Cục Cảnh sát giao thông có trách nhiệm theo dõi, đôn đốc, kiểm tra, hướng dẫn việc tổ chức thực hiện Thông tư này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["TT12-2025-BCA/D39/K1"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-015 · tier A · TT38-2024-BGTVT/D8/K1

Thông tư số 38/2024/TT-BGTVT (Quy định về tốc độ và khoảng cách an toàn của xe cơ giới, xe máy chuyên dùng tham gia giao thông trên đường bộ)

`TT38-2024-BGTVT/D8/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 8. Tốc độ khai thác tối đa cho phép đối với xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ tham gia giao thông trên đường bộ (trừ đường cao tốc)
> 1. Xe chở người bốn bánh có gắn động cơ khi tham gia giao thông trong phạm vi và thời gian cho phép hoạt động, tốc độ khai thác tối đa là 30 km/h.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["TT38-2024-BGTVT/D8/K1"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-016 · tier A · TT14-2025-BXD/D4/K2

Thông tư số 14/2025/TT-BXD (Quy định về đào tạo lái xe; bồi dưỡng, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ)

`TT14-2025-BXD/D4/K2#2025-09-01` · hiệu lực 2025-09-01 → nay

> Điều 4. Hình thức đào tạo
> 2. Người có nhu cầu được đào tạo để cấp giấy phép lái xe các hạng B, C1, C, D1, D2, D, BE, C1E, CE, D1E, D2E và DE:
> a) Đối với nội dung học lý thuyết phải học đủ chương trình đào tạo theo quy định tại Thông tư này và được lựa chọn một trong các hình thức học sau: tập trung tại cơ sở đào tạo lái xe hoặc đào tạo từ xa, tự học có hướng dẫn theo quy định của Chính phủ về hoạt động đào tạo lái xe;
> b) Đối với nội dung học thực hành lái xe: theo hình thức tập trung tại cơ sở đào tạo lái xe.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["TT14-2025-BXD/D4/K2"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-017 · tier A · TT79-2024-BCA/D6/K3

Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)

`TT79-2024-BCA/D6/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 6. Trách nhiệm của chủ xe
> 3. Trường hợp làm thủ tục cấp mới chứng nhận đăng ký xe, biển số xe của công dân Việt Nam cho xe sản xuất, lắp ráp và xe nhập khẩu bằng dịch vụ công trực tuyến toàn trình, chủ xe sử dụng tài khoản định danh điện tử mức độ 2 kê khai, nộp hồ sơ qua cổng dịch vụ công hoặc Ứng dụng định danh quốc gia, không phải đưa xe đến để kiểm tra, khi nhận kết quả phải nộp phiếu kiểm tra chất lượng xuất xưởng có dán bản chà số máy, số khung của xe được đóng dấu giáp lai của cơ sở sản xuất xe (đối với xe sản xuất lắp ráp) hoặc giấy chứng nhận chất lượng an toàn kỹ thuật và bảo vệ môi trường xe nhập khẩu hoặc thông báo miễn kiểm tra chất lượng an toàn kỹ thuật và bảo vệ môi trường xe nhập khẩu có dán bản chà số máy, số khung của xe được đóng dấu giáp lai của đơn vị nhập khẩu xe (đối với xe nhập khẩu) cho cơ quan đăng ký xe.
> Trường hợp không có bản giấy thì nộp bản in từ hệ thống cơ sở dữ liệu điện tử phiếu kiểm tra chất lượng xuất xưởng có dán bản chà số máy, số khung xe đóng dấu giáp lai của cơ sở sản xuất xe (đối với xe sản xuất lắp ráp) hoặc chứng nhận chất lượng an toàn kỹ thuật và bảo vệ môi trường đối với xe nhập khẩu hoặc thông báo miễn kiểm tra chất lượng an …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["TT79-2024-BCA/D6/K3"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-018 · tier A · LUAT35-2024/D20/K3

Luật Đường bộ số 35/2024/QH15

`LUAT35-2024/D20/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 20. Xây dựng, quản lý, vận hành, khai thác, bảo trì công trình hạ tầng kỹ thuật sử dụng chung với đường bộ
> 3. Xây dựng công trình hạ tầng kỹ thuật sử dụng chung với đường bộ được thực hiện đối với các trường hợp sau đây:
> a) Đầu tư xây dựng đường đô thị phải kết hợp với bố trí, xây dựng công trình hạ tầng kỹ thuật sử dụng chung để bảo đảm tính đồng bộ nhằm tiết kiệm tài nguyên đất, tiết kiệm chi phí đầu tư, xây dựng, bảo đảm cảnh quan và môi trường, nâng cao hiệu quả khai thác các công trình và bảo đảm trật tự, an toàn giao thông đường bộ trong giai đoạn vận hành, khai thác, sử dụng đường đô thị;
> b) Đầu tư xây dựng cầu đường bộ phải thiết kế, bố trí vị trí để lắp đặt đường dây thông tin, viễn thông, đường ống cấp nước, đường dây tải điện, dây dẫn điện, trừ dây dẫn điện cao thế và dây dẫn điện không có bộ phận cách điện;
> c) Đầu tư xây dựng hầm đường bộ phải thiết kế, lắp đặt cống cáp, hào hoặc tuy nen kỹ thuật để bố trí, lắp đặt hệ thống phòng cháy, chữa cháy, đường ống cấp nước, thoát nước và các công trình quy định tại điểm b khoản này;
> d) Trường hợp cần thiết khác.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["LUAT35-2024/D20/K3"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-019 · tier A · LUAT36-2024/D84/K1

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D84/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 84. Thống kê tai nạn giao thông đường bộ
> 1. Thông tin về tai nạn giao thông đường bộ phải được thống kê chính xác, đầy đủ, kịp thời; kết quả thống kê, tổng hợp về tai nạn giao thông đường bộ phục vụ nghiên cứu, đề ra các giải pháp phòng ngừa tai nạn giao thông đường bộ.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D84/K1"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-020 · tier A · TT14-2025-BXD/D24/K1

Thông tư số 14/2025/TT-BXD (Quy định về đào tạo lái xe; bồi dưỡng, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ)

`TT14-2025-BXD/D24/K1#2025-09-01` · hiệu lực 2025-09-01 → nay

> Điều 24. In, quản lý chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ
> 1. Cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ in, quản lý chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ để thực hiện cấp mới, cấp lại chứng chỉ như sau:
> a) Căn cứ mẫu chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ quy định tại Phụ lục XV ban hành kèm theo Thông tư này, cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ thiết kế mẫu phôi chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ, kèm theo lô gô (nếu có) của cơ sở mình;
> b) Người đứng đầu cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ phê duyệt mẫu phôi chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ của cơ sở mình và gửi về Sở Xây dựng, cơ quan công an cấp tỉnh, thành phố trực thuộc Trung ương nơi đóng trụ sở chính để báo cáo; chịu trách nhiệm quản lý phôi chứng chỉ của cơ sở mình;
> c) Việc in phôi chứng chỉ phải bảo đảm chặt chẽ, an toàn, bảo mật và phải được lập sổ quản lý.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["TT14-2025-BXD/D24/K1"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-021 · tier A · TT79-2024-BCA/D35/K1

Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)

`TT79-2024-BCA/D35/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 35. Thời hạn sử dụng chứng nhận đăng ký xe
> 1. Chứng nhận đăng ký xe ô tô tải, ô tô khách, xe cải tạo được ghi theo niên hạn sử dụng theo quy định của pháp luật.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["TT79-2024-BCA/D35/K1"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-022 · tier A · ND151-2024/D30/K1

Nghị định số 151/2024/NĐ-CP (Quy định chi tiết một số điều và biện pháp thi hành Luật Trật tự, an toàn giao thông đường bộ)

`ND151-2024/D30/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 30. Màu sơn của xe ô tô kinh doanh vận tải chở trẻ em mầm non, học sinh
> 1. Xe ô tô kinh doanh vận tải chở trẻ em mầm non, học sinh quy định tại điểm a khoản 1 Điều 46 Luật Trật tự, an toàn giao thông đường bộ phải được sơn màu vàng đậm phủ bên ngoài thân xe; mặt trước và hai cạnh bên xe phía trên cửa sổ phải có biển báo dấu hiệu nhận biết là xe chuyên dùng chở trẻ em mầm non, học sinh.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["ND151-2024/D30/K1"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-023 · tier A · TT12-2025-BCA/D38/K3

Thông tư số 12/2025/TT-BCA (Quy định về sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế)

`TT12-2025-BCA/D38/K3#2025-03-01` · hiệu lực 2025-03-01 → nay

> Điều 38. Hiệu lực thi hành và quy định chuyển tiếp
> 3. Người vắng, trượt trong các kỳ sát hạch trước ngày Thông tư này có hiệu lực được bảo lưu kết quả những nội dung đã sát hạch đạt để đăng ký sát hạch lái xe sau ngày Thông tư này có hiệu lực và được cấp giấy phép lái xe theo hạng giấy phép lái xe đổi, cấp lại quy định tại khoản 3 Điều 89 Luật Trật tự, an toàn giao thông đường bộ.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["TT12-2025-BCA/D38/K3"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-024 · tier A · LUAT36-2024/D66/K4

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D66/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 66. Căn cứ dừng phương tiện tham gia giao thông đường bộ để kiểm tra, kiểm soát
> 4. Có tin báo, tố giác, phản ánh, kiến nghị, đề nghị của cơ quan, tổ chức, cá nhân về tội phạm, hành vi vi phạm pháp luật khác.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D66/K4"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-025 · tier A · LUAT35-2024/D21/K5

Luật Đường bộ số 35/2024/QH15

`LUAT35-2024/D21/K5#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 21. Bảo vệ kết cấu hạ tầng đường bộ
> 5. Chính phủ quy định chi tiết Điều này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["LUAT35-2024/D21/K5"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-026 · tier A · TT12-2025-BCA/D36/K5

Thông tư số 12/2025/TT-BCA (Quy định về sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế)

`TT12-2025-BCA/D36/K5#2025-03-01` · hiệu lực 2025-03-01 → nay

> Điều 36. Trách nhiệm Phòng Cảnh sát giao thông
> 5. Kiểm tra định kỳ hoặc đột xuất về công tác tiếp nhận hồ sơ đổi, cấp lại giấy phép lái xe tại Công an cấp xã nơi được bố trí điểm tiếp nhận.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["TT12-2025-BCA/D36/K5"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-027 · tier A · LUAT36-2024/D44/K2

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D44/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 44. Bảo đảm trật tự, an toàn giao thông đường bộ đối với phương tiện vận tải đường bộ trong đô thị
> 2. Xe taxi đón, trả hành khách theo thỏa thuận giữa hành khách và người lái xe nhưng phải chấp hành các quy định của pháp luật về trật tự, an toàn giao thông đường bộ khi đón, trả hành khách.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D44/K2"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-028 · tier A · TT12-2025-BCA/D8/K5

Thông tư số 12/2025/TT-BCA (Quy định về sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế)

`TT12-2025-BCA/D8/K5#2025-03-01` · hiệu lực 2025-03-01 → nay

> Điều 8. Tập huấn, kiểm tra và cấp, đổi, cấp lại, thu hồi thẻ sát hạch viên thuộc lực lượng Công an nhân dân
> 5. Cán bộ hướng dẫn tập huấn và kiểm tra là cán bộ thuộc Cục Cảnh sát giao thông được giao nhiệm vụ quản lý sát hạch, cấp giấy phép lái xe.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["TT12-2025-BCA/D8/K5"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-029 · tier A · ND168-2024/D48/K4

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D48/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 48. Tạm giữ phương tiện, giấy tờ có liên quan đến người điều khiển và phương tiện vi phạm
> 4. Khi phương tiện bị tạm giữ theo quy định tại khoản 1, khoản 2, khoản 3 Điều này, chủ phương tiện phải chịu mọi chi phí (nếu có) cho việc sử dụng phương tiện khác thay thế để vận chuyển người, hàng hóa được chở trên phương tiện bị tạm giữ.
> Trường hợp khi tạm giữ phương tiện vi phạm hành chính nhưng người điều khiển phương tiện, chủ phương tiện không có mặt tại nơi xảy ra vi phạm hoặc có mặt nhưng không chấp hành yêu cầu của người có thẩm quyền tạm giữ hoặc không đáp ứng yêu cầu, điều kiện theo quy định để điều khiển phương tiện hoặc phương tiện không bảo đảm chất lượng an toàn kỹ thuật và bảo vệ môi trường theo quy định thì người có thẩm quyền tạm giữ thực hiện việc di chuyển phương tiện vi phạm về nơi tạm giữ theo quy định; nếu không đủ điều kiện thực hiện thì người có thẩm quyền tạm giữ được thuê tổ chức, cá nhân thực hiện việc di chuyển phương tiện đó. Người điều khiển phương tiện hoặc chủ phương tiện vi phạm phải trả chi phí cho việc thuê di chuyển phương tiện đó về nơi tạm giữ.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D48/K4"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-030 · tier A · LUAT35-2024/D22/K3

Luật Đường bộ số 35/2024/QH15

`LUAT35-2024/D22/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 22. Công trình phụ trợ gắn liền với đường bộ; phương tiện, thiết bị phục vụ quản lý, vận hành, khai thác đường bộ
> 3. Đường bộ đang khai thác phải được điều chỉnh, bổ sung công trình phụ trợ, phương tiện, thiết bị quy định tại khoản 1 và khoản 2 Điều này để việc quản lý, vận hành, khai thác, sử dụng công trình đường bộ bảo đảm an toàn giao thông đường bộ, an toàn công trình.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["LUAT35-2024/D22/K3"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-031 · tier A · LUAT35-2024/D59/K3

Luật Đường bộ số 35/2024/QH15

`LUAT35-2024/D59/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 59. Quyền và nghĩa vụ của người lái xe, nhân viên phục vụ trên xe ô tô kinh doanh vận tải hành khách
> 3. Không được từ chối vận tải hành khách, trừ lý do quy định tại khoản 1 Điều này; không được gây khó khăn đối với hành khách là người cao tuổi, người khuyết tật, trẻ em, phụ nữ mang thai; không được chuyển hành khách sang phương tiện khác khi chưa được sự đồng ý của hành khách, trừ trường hợp bất khả kháng.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["LUAT35-2024/D59/K3"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-032 · tier A · TT12-2025-BCA/D4/K3

Thông tư số 12/2025/TT-BCA (Quy định về sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế)

`TT12-2025-BCA/D4/K3#2025-03-01` · hiệu lực 2025-03-01 → nay

> Điều 4. Hình thức, nội dung và quy trình sát hạch lái xe
> 3. Sát hạch thực hành lái xe trên đường
> a) Đối với các hạng B, C1, C, D1, D2, D
> Thực hiện sát hạch bằng phương pháp sử dụng thiết bị chấm điểm tự động, có một sát hạch viên ngồi trên xe sát hạch. Người dự sát hạch điều khiển xe ô tô sát hạch, xử lý các tình huống trên đường giao thông và thực hiện theo hiệu lệnh của sát hạch viên;
> b) Đối với các hạng BE, C1E, CE, D1E, D2E, DE
> Thực hiện sát hạch bằng phương pháp chấm điểm trực tiếp, có một sát hạch viên ngồi trên xe sát hạch.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["TT12-2025-BCA/D4/K3"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-033 · tier A · LUAT36-2024/D22/K1

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D22/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 22. Nhường đường tại nơi đường giao nhau
> 1. Tại nơi đường giao nhau giữa đường không ưu tiên với đường ưu tiên hoặc giữa đường nhánh với đường chính thì xe đi từ đường không ưu tiên hoặc đường nhánh phải nhường đường cho xe đi trên đường ưu tiên hoặc đường chính từ bất kỳ hướng nào tới;


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D22/K1"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-034 · tier A · TT12-2025-BCA/D30/K3

Thông tư số 12/2025/TT-BCA (Quy định về sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế)

`TT12-2025-BCA/D30/K3#2025-03-01` · hiệu lực 2025-03-01 → nay

> Điều 30. Yêu cầu đối với hệ thống thông tin về sát hạch, cấp giấy phép lái xe
> 3. Hệ thống thông tin về sát hạch, cấp giấy phép lái xe tại Cục Cảnh sát giao thông
> a) Quản lý tối thiểu các thông tin: số giấy phép lái xe; xác nhận hoàn thành khóa đào tạo; họ, tên; số định danh cá nhân; ngày, tháng, năm sinh; quốc tịch; nơi cư trú; cơ sở đào tạo lái xe; hạng xe đào tạo; khoá đào tạo; ngày đạt kết quả sát hạch; cơ quan sát hạch; địa điểm tổ chức sát hạch (trung tâm sát hạch lái xe hoặc sân tập lái dùng để sát hạch); ngày cấp, đổi, cấp lại giấy phép lái xe; cơ quan cấp, đổi, cấp lại giấy phép lái xe; hạng giấy phép lái xe; ngày hết hạn; số phôi giấy phép lái xe;
> b) Có khả năng tiếp nhận các thông tin tại điểm a khoản này từ hệ thống thông tin giấy phép lái xe tại Phòng Cảnh sát giao thông; tra cứu thông tin giấy phép lái xe, thực hiện các nghiệp vụ về sát hạch cấp giấy phép lái xe trên trang thông tin điện tử; lưu trữ chính xác, đầy đủ các thông tin được quản lý;
> c) Có chức năng cấp giấy phép lái xe quốc tế theo quy định tại khoản 1 và khoản 2 Điều 28 Thông tư này; thu hồi giấy phép lái xe;
> d) Có khả năng kết nối, chia sẻ dữ liệu với cổng dịch vụ công quốc gia, cổng dịch vụ công của các …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["TT12-2025-BCA/D30/K3"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-035 · tier A · LUAT36-2024/D36/K3

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D36/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 36. Biển số xe
> 3. Biển số xe được quản lý theo mã định danh, trừ biển số xe quy định tại điểm b khoản 2 Điều này. Việc quản lý biển số xe theo mã định danh được quy định như sau:
> a) Biển số xe được cấp và quản lý theo mã định danh của chủ xe là cá nhân, tổ chức; trường hợp tổ chức chưa có mã định danh thì quản lý theo mã số thuế, quyết định thành lập hoặc giấy tờ tương đương;
> b) Trường hợp xe hết niên hạn sử dụng, hư hỏng không sử dụng được hoặc chuyển quyền sở hữu xe, chủ xe được giữ lại số biển số xe trong thời hạn 05 năm để đăng ký cho xe khác thuộc sở hữu của mình; quá thời hạn nêu trên, số biển số xe đó bị cơ quan đăng ký xe thu hồi, nhập vào kho biển số xe để đăng ký, cấp cho tổ chức, cá nhân khác, trừ trường hợp chuyển nhượng, trao đổi, tặng cho, để thừa kế xe gắn với biển số xe trúng đấu giá;
> c) Trường hợp chủ xe có thay đổi thông tin về trụ sở, nơi thường trú, tạm trú thì được giữ lại số biển số xe định danh.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D36/K3"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-036 · tier A · TT65-2024-BCA/D8/K1

Thông tư số 65/2024/TT-BCA (Quy định kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ để được phục hồi điểm giấy phép lái xe)

`TT65-2024-BCA/D8/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 8. Trách nhiệm của cơ quan có thẩm quyền kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ
> 1. Bảo đảm điều kiện tổ chức kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ theo quy định tại Điều 5 Thông tư này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["TT65-2024-BCA/D8/K1"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-037 · tier A · LUAT35-2024/D57/K2

Luật Đường bộ số 35/2024/QH15

`LUAT35-2024/D57/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 57. Vận tải hành khách bằng xe ô tô
> 2. Việc vận tải hành khách bằng xe ô tô phải thực hiện quy định tại Điều 56 của Luật này và thực hiện đầy đủ các yêu cầu, điều kiện về bảo đảm trật tự, an toàn giao thông đường bộ theo quy định của pháp luật về trật tự, an toàn giao thông đường bộ.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["LUAT35-2024/D57/K2"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-038 · tier A · TT79-2024-BCA/D37/K2

Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)

`TT79-2024-BCA/D37/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 37. Quy định về biển số xe
> 2. Ký hiệu, seri biển số, kích thước của chữ và số trên biển số đăng ký các loại xe thực hiện theo quy định tại các Phụ lục số 02, 03 và 04 ban hành kèm theo Thông tư này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["TT79-2024-BCA/D37/K2"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-039 · tier A · ND151-2024/D18/K2

Nghị định số 151/2024/NĐ-CP (Quy định chi tiết một số điều và biện pháp thi hành Luật Trật tự, an toàn giao thông đường bộ)

`ND151-2024/D18/K2#2025-01-01` · hiệu lực 2025-01-01 → 2026-06-30

> Điều 18. Xe được lắp đặt, sử dụng thiết bị phát tín hiệu của xe ưu tiên
> 2. Xe của lực lượng quân sự đi làm nhiệm vụ khẩn cấp bao gồm: xe quân sự đi thực hiện nhiệm vụ chỉ huy chữa cháy, cứu nạn, cứu hộ, chỉ huy tác chiến, thông tin làm nhiệm vụ hoả tốc, chỉ huy đoàn hành quân, xe làm nhiệm vụ kiểm soát quân sự, kiểm tra xe quân sự, bảo vệ đoàn; xe thực hiện nhiệm vụ bắt, khám xét hoặc thực hiện hoạt động điều tra khác, áp giải bị can, bị cáo, phạm nhân; tham gia phòng, chống khủng bố.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-06-30", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["ND151-2024/D18/K2"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-040 · tier A · ND151-2024/D34/K3

Nghị định số 151/2024/NĐ-CP (Quy định chi tiết một số điều và biện pháp thi hành Luật Trật tự, an toàn giao thông đường bộ)

`ND151-2024/D34/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 34. Người nước ngoài điều khiển xe cơ giới nước ngoài khi tham gia giao thông tại Việt Nam
> 3. Khi điều khiển xe cơ giới nước ngoài tham gia giao thông, người nước ngoài phải chấp hành đúng quy định của pháp luật về trật tự, an toàn giao thông đường bộ của Việt Nam; mang theo và xuất trình khi cơ quan có thẩm quyền yêu cầu các giấy tờ sau:
> a) Hộ chiếu hoặc giấy tờ có giá trị đi lại quốc tế, giấy tờ liên quan đến cư trú tại Việt Nam;
> b) Giấy phép lái xe phù hợp với loại xe được phép điều khiển, có giá trị sử dụng trong phạm vi lãnh thổ Việt Nam và còn hiệu lực;
> c) Giấy chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường đối với xe cơ giới hoặc giấy tờ tương đương do cơ quan có thẩm quyền của quốc gia đăng ký xe cấp còn hiệu lực (đối với xe ô tô);
> d) Giấy đăng ký xe do cơ quan có thẩm quyền của quốc gia đăng ký xe cấp và còn hiệu lực;
> đ) Giấy chứng nhận bảo hiểm trách nhiệm dân sự của chủ xe cơ giới có giá trị tại Việt Nam;
> e) Tờ khai hải quan phương tiện vận tải đường bộ tạm nhập, tái xuất.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["ND151-2024/D34/K3"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-041 · tier A · TT79-2024-BCA/D40/K3

Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)

`TT79-2024-BCA/D40/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 40. Trách nhiệm thi hành
> 3. Trong quá trình triển khai thực hiện Thông tư này, nếu có khó khăn, vướng mắc, Công an các đơn vị, địa phương báo cáo,về Bộ Công an (qua Cục Cảnh sát giao thông) để có hướng dẫn kịp thời./.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["TT79-2024-BCA/D40/K3"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-042 · tier A · TT36-2024-BYT/D9/K2

Thông tư số 36/2024/TT-BYT (Quy định về tiêu chuẩn sức khỏe, việc khám sức khỏe đối với người lái xe, người điều khiển xe máy chuyên dùng; việc khám sức khỏe định kỳ đối với người hành nghề lái xe ô tô; cơ sở dữ liệu về sức khỏe của người lái xe, người điều khiển xe máy chuyên dùng)

`TT36-2024-BYT/D9/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 9. Điều khoản chuyển tiếp
> 2. Mẫu giấy khám sức khỏe của người lái xe ban hành tại Thông tư liên tịch số 24/2015/TTLT-BYT-BGTVT ngày 28 tháng 8 năm 2015 của Bộ trưởng Bộ Y tế và Bộ trưởng Bộ Giao thông vận tải quy định về tiêu chuẩn sức khỏe của người lái xe, việc khám sức khỏe định kỳ đối với người lái xe ô tô và quy định về cơ sở y tế khám sức khỏe cho người lái xe bản giấy đã in, được tiếp tục sử dụng và phải tuân thủ hướng dẫn ghi theo quy định tại Phụ lục II ban hành kèm theo Thông tư này. Trường hợp cơ sở in mới giấy khám sức khỏe phải tuân thủ mẫu theo quy định tại Phụ lục II ban hành kèm theo Thông tư này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["TT36-2024-BYT/D9/K2"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-043 · tier A · LUAT36-2024/D45/K2

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D45/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 45. Bảo đảm trật tự, an toàn giao thông đường bộ đối với xe ô tô vận chuyển hành khách
> 2. Người lái xe, nhân viên phục vụ trên xe ô tô vận chuyển hành khách có trách nhiệm sau đây:
> a) Thực hiện quy định tại khoản 1 Điều này;
> b) Trước khi cho xe khởi hành phải kiểm tra các điều kiện bảo đảm an toàn của xe, hướng dẫn cho hành khách về an toàn giao thông đường bộ và thoát hiểm khi gặp sự cố;
> c) Hướng dẫn, yêu cầu, kiểm tra người trên xe thực hiện quy định tại khoản 2 Điều 10 của Luật này;
> d) Kiểm tra việc sắp xếp, chằng buộc hành lý, hàng hóa bảo đảm an toàn;
> đ) Giữ gìn trật tự, vệ sinh trong xe;
> e) Phối hợp thực hiện các nhiệm vụ khác theo yêu cầu của cơ quan Công an trong công tác bảo vệ an ninh quốc gia, bảo đảm trật tự, an toàn xã hội;
> g) Thực hiện các quy tắc giao thông đường bộ khác quy định tại Chương II của Luật này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D45/K2"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-044 · tier A · TT14-2025-BXD/D18

Thông tư số 14/2025/TT-BXD (Quy định về đào tạo lái xe; bồi dưỡng, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ)

`TT14-2025-BXD/D18#2025-09-01` · hiệu lực 2025-09-01 → nay

> Điều 18. Tiêu chuẩn của cơ sở đào tạo người điều khiển xe máy chuyên dùng thực hiện bồi dưỡng, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ
> Cơ sở đào tạo người điều khiển xe máy chuyên dùng thực hiện bồi dưỡng, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ phải có phòng học lý thuyết, có tài liệu giảng dạy, sa hình và hệ thống biển báo hiệu giao thông đường bộ theo quy định.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["TT14-2025-BXD/D18"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-045 · tier A · LUAT36-2024/D23/K4

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D23/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 23. Qua phà, qua cầu phao
> 4. Khi qua cầu phao, phải chấp hành quy định sau đây:
> a) Xe cơ giới, xe máy chuyên dùng phải đi theo một hàng theo chiều di chuyển, không gây cản trở người, phương tiện đi ngược chiều;
> b) Xe thô sơ, người đi bộ phải đi sát về phía bên phải theo chiều đi của mình, không gây cản trở xe cơ giới, xe máy chuyên dùng;
> c) Xe cơ giới, xe máy chuyên dùng, xe thô sơ, người đi bộ phải tuân thủ hướng dẫn của người điều khiển giao thông.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D23/K4"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-046 · tier A · LUAT36-2024/D9/K1

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D9/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 9. Các hành vi bị nghiêm cấm
> 1. Điều khiển xe cơ giới tham gia giao thông đường bộ không có giấy phép lái xe theo quy định của pháp luật; điều khiển xe máy chuyên dùng tham gia giao thông đường bộ không có giấy phép lái xe hoặc chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ, bằng hoặc chứng chỉ điều khiển xe máy chuyên dùng.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D9/K1"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-047 · tier A · TT79-2024-BCA/D9/K3

Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)

`TT79-2024-BCA/D9/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 9. Giấy khai đăng ký xe
> 3. Trường hợp thực hiện đăng ký xe trực tiếp tại cơ quan đăng ký xe: Chủ xe kê khai chính xác, đầy đủ, trung thực các nội dung quy định trong mẫu giấy khai đăng ký xe.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["TT79-2024-BCA/D9/K3"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-048 · tier A · LUAT35-2024/D34/K2

Luật Đường bộ số 35/2024/QH15

`LUAT35-2024/D34/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 34. Thi công xây dựng công trình thủy lợi, thủy điện trong phạm vi bảo vệ công trình đường bộ đang khai thác
> 2. Khi thi công xây dựng công trình thủy lợi, thủy điện giao cắt với đường bộ đang khai thác phải thực hiện quy định tại khoản 1 Điều này và các quy định sau đây:
> a) Vị trí xây dựng không ảnh hưởng đến vận hành, khai thác và hoạt động bình thường của các công trình đường bộ hiện có, trừ quy định tại điểm d khoản này;
> b) Thực hiện biện pháp bảo đảm an toàn cho công trình đường bộ hiện có, công trình liền kề, bảo đảm giao thông thông suốt, an toàn và bảo vệ môi trường; bảo đảm các quy định về tĩnh không của đường bộ, phạm vi bảo vệ trên không, phạm vi bảo vệ bên dưới của công trình đường bộ;
> c) Không được làm xói lở mố, trụ cầu, tường chắn bảo vệ công trình đường bộ khi nạo vét và thi công trên sông, kênh, mương trong phạm vi bảo vệ kết cấu hạ tầng đường bộ;
> d) Trước khi xây dựng công trình thủy lợi, thủy điện cắt ngang, chồng lấn lên vị trí đường bộ hoặc ảnh hưởng đến công trình đường bộ đang khai thác, chủ đầu tư dự án xây dựng công trình thủy lợi, thủy điện phải xây dựng công trình đường bộ để bồi hoàn, thay thế cho phần công trình đường bộ bị ảnh hưởng hoặc bồi hoàn …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["LUAT35-2024/D34/K2"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-049 · tier A · TT12-2025-BCA/D12/K1

Thông tư số 12/2025/TT-BCA (Quy định về sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế)

`TT12-2025-BCA/D12/K1#2025-03-01` · hiệu lực 2025-03-01 → nay

> Điều 12. Công nhận kết quả sát hạch
> 1. Xét công nhận kết quả sát hạch đối với thí sinh dự sát hạch lái xe hạng A1, A và B1
> a) Thí sinh đạt nội dung sát hạch lý thuyết và thực hành lái xe trong hình thì được công nhận đạt kết quả kỳ sát hạch;
> b) Thí sinh không đạt nội dung sát hạch lý thuyết thì được tiếp tục dự nội dung sát hạch thực hành lái xe trong hình;
> c) Thí sinh đạt một trong các nội dung sát hạch lý thuyết hoặc thực hành lái xe trong hình thì được bảo lưu kết quả nội dung sát hạch đã đạt trong thời gian 01 năm kể từ ngày đạt kết quả sát hạch; nếu có nhu cầu dự sát hạch phải có tên trong biên bản xác nhận vắng, trượt của Hội đồng sát hạch kỳ trước và giấy khám sức khỏe của người lái xe còn hiệu lực hoặc có tên trong hệ thống thông tin sát hạch lái xe.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["TT12-2025-BCA/D12/K1"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-050 · tier A · LUAT36-2024/D57/K2

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D57/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 57. Giấy phép lái xe
> 2. Người khuyết tật điều khiển xe mô tô ba bánh dùng cho người khuyết tật được cấp giấy phép lái xe hạng A1.
> Người khuyết tật điều khiển xe ô tô số tự động có kết cấu phù hợp với tình trạng khuyết tật thì được cấp giấy phép lái xe hạng B.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D57/K2"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-051 · tier B · ND158-2024/D22/K2

Nghị định số 158/2024/NĐ-CP (Quy định về hoạt động vận tải đường bộ)

`ND158-2024/D22/K2#2026-08-10` · hiệu lực 2026-08-10 → nay

> Điều 22. Quy trình đăng ký, ngừng khai thác, thu hồi đăng ký khai thác tuyến vận tải hành khách cố định
> 2. Đối với các tuyến vận tải hành khách cố định điều chỉnh, bổ sung (tuyến đã công bố) hoặc tuyến mới (tuyến chưa được công bố)
> a) Đối với tuyến vận tải hành khách cố định điều chỉnh, bổ sung (tuyến đã công bố), đơn vị kinh doanh vận tải theo tuyến cố định có nhu cầu đăng ký khai thác các giờ xe chạy (nốt xe) còn trống hoặc điều chỉnh, bổ sung hành trình tuyến hoặc điều chỉnh thời gian giãn cách giữa các chuyến xe liền kề (tăng hoặc giảm thời gian giãn cách) hoặc điều chỉnh lưu lượng (tăng số chuyến so với số chuyến xe đã công bố) xây dựng phương án khai thác tuyến gửi về Sở Xây dựng (nơi đơn vị kinh doanh vận tải đặt trụ sở chính hoặc trụ sở chi nhánh) để đăng ký khai thác tuyến theo quy định và Sở Xây dựng đầu tuyến bên kia để phối hợp quản lý.
> Đối với tuyến mới (tuyến chưa được công bố), đơn vị kinh doanh vận tải có văn bản trao đổi hoặc biên bản thống nhất với bến xe hai đầu tuyến. Trong thời gian 05 ngày làm việc kể từ ngày nhận được văn bản của đơn vị kinh doanh vận tải, bến xe phải có văn bản trao đổi hoặc biên bản thống nhất với đơn vị kinh doanh vận tải; trường hợp …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "B", "answer": "", "gold_units": ["ND158-2024/D22/K2"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-052 · tier B · ND336-2025/D18/K2

Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)

`ND336-2025/D18/K2#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 18. Thẩm quyền xử phạt của Công an nhân dân
> 2. Thủ trưởng đơn vị Cảnh sát cơ động cấp đại đội có quyền:
> a) Phạt cảnh cáo;
> b) Phạt tiền đến 15.000.000 đồng;
> c) Áp dụng biện pháp khắc phục hậu quả quy định tại Điều 3 của Nghị định này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "B", "answer": "", "gold_units": ["ND336-2025/D18/K2"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-053 · tier B · TT73-2024-BCA/D20/K1

Thông tư số 73/2024/TT-BCA (Quy định công tác tuần tra, kiểm soát, xử lý vi phạm pháp luật về trật tự, an toàn giao thông đường bộ của Cảnh sát giao thông)

`TT73-2024-BCA/D20/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 20. Ghi Sổ kế hoạch và nhật ký tuần tra, kiểm soát giao thông đường bộ
> 1. Khi giải quyết xong từng vụ việc phải ghi ngay vào Sổ kế hoạch và nhật ký tuần tra, kiểm soát giao thông đường bộ (ghi ngắn gọn, rõ ràng và liên tục theo thứ tự thời gian).


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "B", "answer": "", "gold_units": ["TT73-2024-BCA/D20/K1"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-054 · tier B · ND165-2024/D55/K4

Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ)

`ND165-2024/D55/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 55. Lộ trình đầu tư xây dựng đối với đường cao tốc chưa đáp ứng tiêu chuẩn, quy chuẩn kỹ thuật theo khoản 1 Điều 45 Luật Đường bộ, đường gom, đường bên, Trung tâm quản lý, điều hành giao thông tuyến đường cao tốc, công trình kiểm soát tải trọng xe, hệ thống thu phí điện tử không dừng
> 4. Đối với hệ thống thu phí điện tử không dừng
> a) Đối với dự án đường bộ cao tốc do Nhà nước đại diện chủ sở hữu và trực tiếp quản lý, khai thác phải hoàn thiện hệ thống thu phí điện tử không dừng trước khi thu phí;
> b) Đối với dự án đường bộ cao tốc đầu tư theo phương thức đối tác công tư, việc thanh toán tiền sử dụng đường bộ phải thực hiện theo hình thức điện tử không dừng.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "B", "answer": "", "gold_units": ["ND165-2024/D55/K4"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-055 · tier B · ND165-2024/D30/K1

Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ)

`ND165-2024/D30/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 30. Trách nhiệm tổ chức thực hiện xây dựng nút giao đấu nối, đóng điểm đấu nối
> 1. Việc thực hiện xây dựng nút giao đấu nối trong dự án đầu tư xây dựng mới, nâng cấp, cải tạo quốc lộ và đường cao tốc với đường khác được thực hiện theo dự án đầu tư xây dựng đường bộ được cấp có thẩm quyền phê duyệt và phải thực hiện các quy định tại khoản 2 và khoản 4 Điều 27 của Nghị định này, quy định của pháp luật về đường bộ và pháp luật về xây dựng.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "B", "answer": "", "gold_units": ["ND165-2024/D30/K1"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-056 · tier B · ND165-2024/D54/K2

Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ)

`ND165-2024/D54/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 54. Bảo trì công trình đường cao tốc
> 2. Trước khi hết thời hạn khai thác, sử dụng các bộ phận, hạng mục công trình thuộc kết cấu hạ tầng đường cao tốc, báo hiệu đường bộ, thiết bị lắp đặt vào kết cấu hạ tầng đường cao tốc hoặc đã khai thác, sử dụng quá số lần, tần suất quy định của nhà sản xuất, người quản lý, sử dụng đường cao tốc phải tổ chức thực hiện kiểm tra, kiểm định xác định lại chất lượng và tình trạng công trình, thiết bị lắp đặt vào công trình và xử lý như sau:
> a) Trường hợp bảo đảm chất lượng và an toàn thì được tiếp tục sử dụng;
> b) Trường hợp không bảo đảm chất lượng và an toàn thì phải có phương án sửa chữa, thay thế.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "B", "answer": "", "gold_units": ["ND165-2024/D54/K2"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-057 · tier B · ND158-2024/D53/K3

Nghị định số 158/2024/NĐ-CP (Quy định về hoạt động vận tải đường bộ)

`ND158-2024/D53/K3#2026-08-10` · hiệu lực 2026-08-10 → nay

> Điều 53. Cấp, cấp lại Giấy phép liên vận giữa Việt Nam và Lào
> 3. Thành phần hồ sơ đề nghị cấp, cấp lại giấy phép đối với phương tiện phi thương mại và phương tiện phục vụ các công trình, dự án hoặc hoạt động kinh doanh của doanh nghiệp trên lãnh thổ Lào
> a) Giấy đề nghị cấp, cấp lại giấy phép theo Mẫu số 05 Phụ lục XI kèm theo Nghị định này;
> b) Trường hợp phương tiện không thuộc quyền sở hữu của tổ chức, cá nhân phải xuất trình bản sao hoặc bản sao điện tử hợp đồng thuê phương tiện;
> c) Bản sao hoặc bản sao điện tử Quyết định cử đi công tác của cơ quan có thẩm quyền (đối với trường hợp xe công vụ và xe của các cơ quan ngoại giao, tổ chức quốc tế đi công tác);
> d) Bản sao hoặc bản sao điện tử của: hợp đồng hoặc tài liệu chứng minh tổ chức, đơn vị đang thực hiện công trình, dự án hoặc hoạt động kinh doanh trên lãnh thổ Lào (đối với tổ chức, đơn vị phục vụ các công trình, dự án hoặc hoạt động kinh doanh trên lãnh thổ Lào) kèm bản dịch hợp đồng hoặc tài liệu ra tiếng Việt được chứng thực hoặc chứng nhận bởi cơ quan công chứng đối với trường hợp hợp đồng, tài liệu bằng tiếng nước ngoài.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "B", "answer": "", "gold_units": ["ND158-2024/D53/K3"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-058 · tier B · TT73-2024-BCA/D29/K3

Thông tư số 73/2024/TT-BCA (Quy định công tác tuần tra, kiểm soát, xử lý vi phạm pháp luật về trật tự, an toàn giao thông đường bộ của Cảnh sát giao thông)

`TT73-2024-BCA/D29/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 29. Thẩm quyền huy động, lực lượng được huy động và điều kiện của cán bộ, chiến sĩ được huy động
> 3. Điều kiện đối với cán bộ, chiến sĩ được huy động
> Cán bộ, chiến sĩ được huy động tham gia phối hợp với Cảnh sát giao thông thực hiện tuần tra, kiểm soát phải được quán triệt, nắm vững các quy định của pháp luật về trật tự, an toàn giao thông đường bộ, quy định về xử phạt vi phạm hành chính về trật tự, an toàn giao thông đường bộ và quy định về tuần tra, kiểm soát giao thông đường bộ.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "B", "answer": "", "gold_units": ["TT73-2024-BCA/D29/K3"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-059 · tier B · ND158-2024/D62/K7

Nghị định số 158/2024/NĐ-CP (Quy định về hoạt động vận tải đường bộ)

`ND158-2024/D62/K7#2025-01-01` · hiệu lực 2025-01-01 → 2026-08-09

> Điều 62. Quy trình đăng ký, ngừng khai thác tuyến, bổ sung hoặc thay thế phương tiện khai thác tuyến vận tải hành khách cố định giữa Việt Nam và Campuchia
> 7. Phương tiện khai thác tuyến vận tải hành khách cố định bằng xe ô tô giữa Việt Nam và Campuchia phải có lệnh vận chuyển. Lệnh vận chuyển cấp cho từng chuyến xe lượt đi và lượt về (trường hợp chuyến xe thực hiện trong nhiều ngày), cấp hàng ngày (trường hợp trong ngày thực hiện nhiều chuyến). Lệnh vận chuyển do đơn vị kinh doanh vận tải tự in theo Mẫu số 12 Phụ lục XII kèm theo Nghị định này. Lệnh vận chuyển phải được đánh số thứ tự theo năm để quản lý.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-08-09", "question_type": "hanh_vi_cam_nghia_vu", "tier": "B", "answer": "", "gold_units": ["ND158-2024/D62/K7"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-060 · tier B · ND158-2024/D22/K8

Nghị định số 158/2024/NĐ-CP (Quy định về hoạt động vận tải đường bộ)

`ND158-2024/D22/K8#2026-08-10` · hiệu lực 2026-08-10 → nay

> Điều 22. Quy trình đăng ký, ngừng khai thác, thu hồi đăng ký khai thác tuyến vận tải hành khách cố định
> 8. Sở Xây dựng nơi phát hành Thông báo đăng ký khai thác tuyến thành công thực hiện thu hồi Thông báo đăng ký khai thác tuyến đối với chuyến xe đang khai thác theo trình tự sau đây:
> a) Ban hành quyết định thu hồi. Trường hợp tuyến đăng ký khai thác chỉ có 01 chuyến xe hoặc toàn bộ các chuyến xe của tuyến đều thực hiện dưới 70% tổng số chuyến xe đã đăng ký thì thực hiện thu hồi Thông báo đăng ký khai thác tuyến thành công và thu hồi phù hiệu đã cấp cho phương tiện hoạt động trên tuyến;
> b) Gửi quyết định thu hồi cho đơn vị kinh doanh vận tải, bến xe khách hai đầu tuyến, Sở Xây dựng đầu tuyến bên kia và phải đăng tải thông tin trên Trang thông tin điện tử của Sở Xây dựng;
> c) Trong thời gian 02 ngày làm việc kể từ ngày ban hành quyết định thu hồi, thực hiện cập nhật thông tin giờ xuất bến của chuyến xe đã thu hồi vào Cơ sở dữ liệu cấp phép hoạt động vận tải của Bộ Xây dựng làm cơ sở cho các đơn vị kinh doanh vận tải khác đăng ký khai thác tuyến theo quy định của Nghị định này;
> d) Trong thời gian 30 ngày kể từ ngày quyết định thu hồi có hiệu lực thi hành, đơn vị kinh doanh vận tải bị …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "B", "answer": "", "gold_units": ["ND158-2024/D22/K8"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-061 · tier B · TT52-2024-BGTVT/D6/K1

Thông tư số 52/2024/TT-BGTVT (Quy định về yêu cầu kỹ thuật đối với xe cơ giới, xe máy chuyên dùng thuộc đối tượng nghiên cứu phát triển có nhu cầu tham gia giao thông đường bộ)

`TT52-2024-BGTVT/D6/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 6. Trách nhiệm của các cơ quan, tổ chức
> 1. Trách nhiệm của cơ sở nghiên cứu phát triển:
> a) Chịu trách nhiệm bảo đảm chất lượng an toàn kỹ thuật và bảo vệ môi trường đối với xe nghiên cứu phát triển trong suốt quá trình sản xuất, lắp ráp, kiểm tra chất lượng xuất xưởng, chạy thử trên đường;
> b) Chịu trách nhiệm về tính trung thực của: tài liệu thiết kế xe; kết quả kiểm tra chất lượng xuất xưởng, nội dung in trên Phiếu kiểm tra chất lượng xuất xưởng; kết quả kiểm tra, đánh giá tình trạng của xe trước khi đưa xe chạy thử trên đường, trong các kỳ bảo dưỡng; nguồn gốc, xuất xứ của xe; phụ tùng sử dụng để sản xuất, lắp ráp xe;
> c) Chịu các chi phí và trách nhiệm pháp lý đối với các vấn đề phát sinh trong quá trình chạy thử trên đường;
> d) Cung cấp thông tin về kết quả kiểm tra chất lượng xuất xưởng của xe nghiên cứu phát triển đến Cục Đăng kiểm Việt Nam;
> đ) Khi bảo dưỡng định kỳ, cơ sở nghiên cứu phát triển phải kiểm tra và đảm bảo tình trạng của các tổng thành, hệ thống gồm: động cơ, lái, phanh, treo, vành, lốp xe, đèn chiếu sáng, tín hiệu hoạt động bình thường. Chu kỳ bảo dưỡng định kỳ theo quy định của cơ sở sản xuất xe nhưng không được dài hơn chu kỳ bảo dưỡng đối với xe cùng …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "B", "answer": "", "gold_units": ["TT52-2024-BGTVT/D6/K1"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-062 · tier B · ND158-2024/D62/K10

Nghị định số 158/2024/NĐ-CP (Quy định về hoạt động vận tải đường bộ)

`ND158-2024/D62/K10#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 62. Quy trình đăng ký, ngừng khai thác tuyến, bổ sung hoặc thay thế phương tiện khai thác tuyến vận tải hành khách cố định giữa Việt Nam và Campuchia
> 10. Điều chỉnh tần suất chạy xe trên tuyến
> a) Trước khi điều chỉnh tần suất chạy trên tuyến ít nhất 10 ngày, đơn vị kinh doanh vận tải phải thông báo bằng văn bản theo Mẫu số 15 Phụ lục XII kèm theo Nghị định này cho cơ quan có thẩm quyền, bến xe đầu tuyến phía Việt Nam;
> b) Chậm nhất 02 ngày làm việc, kể từ ngày nhận văn bản đề nghị, cơ quan có thẩm quyền ra văn bản thông báo điều chỉnh tần suất chạy xe trên tuyến theo Mẫu số 16 Phụ lục XII kèm theo Nghị định này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "B", "answer": "", "gold_units": ["ND158-2024/D62/K10"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-063 · tier B · ND165-2024/D28/K5

Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ)

`ND165-2024/D28/K5#2026-07-01` · hiệu lực 2026-07-01 → nay

> Điều 28. Vị trí nút giao đấu nối đường khác vào đường cao tốc
> 5. Cơ quan có thẩm quyền giải quyết thủ tục hành chính quy định tại khoản 3 Điều này thực hiện tiếp nhận, kiểm tra hồ sơ và xử lý như sau:
> a) Đối với trường hợp nộp trực tiếp, sau khi kiểm tra thành phần hồ sơ, nếu đúng quy định thì tiếp nhận hồ sơ và viết phiếu hẹn trả kết quả; hướng dẫn tổ chức, cá nhân hoàn thiện hồ sơ đối với trường hợp không đủ thành phần hồ sơ;
> b) Đối với trường hợp nộp gián tiếp, trong phạm vi 02 ngày làm việc kể từ ngày nhận được hồ sơ, kiểm tra thành phần hồ sơ, nếu không đủ thành phần hồ sơ có văn bản thông báo đến tổ chức, cá nhân để bổ sung, hoàn thiện;
> c) Trường hợp phải lấy ý kiến của các cơ quan thì sau 02 ngày làm việc kể từ ngày nhận đủ thành phần hồ sơ, cơ quan có thẩm quyền giải quyết thủ tục hành chính tiến hành lấy ý kiến. Cơ quan, tổ chức được lấy ý kiến có trách nhiệm trả lời Bộ Giao thông vận tải hoặc Ủy ban nhân dân cấp tỉnh trong thời hạn không quá 07 ngày làm việc, kể từ ngày nhận được đề nghị của cơ quan có thẩm quyền.
> d) Trong thời hạn không quá 05 ngày làm việc kể từ khi nhận được hồ sơ đề nghị hoặc 07 ngày sau khi nhận được ý kiến của các cơ quan (đối với trường hợp phải …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "B", "answer": "", "gold_units": ["ND165-2024/D28/K5"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-064 · tier B · ND165-2024/D31/K2

Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ)

`ND165-2024/D31/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 31. Đấu nối tạm thời có thời hạn vào quốc lộ, đường địa phương đang khai thác
> 2. Hết thời hạn đấu nối tạm, chủ đầu tư dự án, tổ chức, cá nhân đề nghị đấu nối tạm phải thực hiện và tự chịu trách nhiệm chi phí thực hiện các công việc sau:
> a) Xóa bỏ, đóng điểm đấu nối tạm thời;
> b) Hoàn trả nguyên trạng hành lang an toàn đường bộ; sửa chữa, bổ sung kết cấu hạ tầng đường bộ bị ảnh hưởng do việc thực hiện đấu nối tạm thời.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "B", "answer": "", "gold_units": ["ND165-2024/D31/K2"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-065 · tier C · TT72-2024-BCA/D4/K4

Thông tư số 72/2024/TT-BCA (Quy định quy trình điều tra, giải quyết tai nạn giao thông đường bộ của Cảnh sát giao thông)

`TT72-2024-BCA/D4/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 4. Tổ chức tiếp nhận tin báo về tai nạn giao thông đường bộ
> 4. Tiếp nhận tin báo về tai nạn giao thông đường bộ tại trụ sở đơn vị
> Cán bộ trực ban tiếp nhận tin báo về tai nạn giao thông đường bộ phải hỏi rõ các thông tin sau:
> a) Họ tên, địa chỉ, số điện thoại (nếu có) của người báo tin;
> b) Thời gian nhận tin báo, thời gian, địa điểm xảy ra vụ tai nạn giao thông đường bộ;
> c) Thiệt hại ban đầu về người: số người chết, số người bị thương (nếu có);
> d) Thông tin phương tiện (biển số, loại phương tiện, đặc điểm khác nếu có), thiệt hại về phương tiện đường bộ, công trình giao thông đường bộ và tài sản khác (nếu có);
> đ) Họ tên, địa chỉ, số điện thoại của những người liên quan hoặc người biết về vụ tai nạn giao thông đường bộ xảy ra (nếu có);
> e) Trường hợp vụ tai nạn giao thông đường bộ có người điều khiển phương tiện bỏ chạy thì phải hỏi rõ thông tin về đặc điểm phương tiện (biển số, màu sắc, chủng loại, nhãn hiệu), hướng di chuyển của phương tiện, đặc điểm của người điều khiển phương tiện;
> g) Những thông tin khác về vụ tai nạn giao thông đường bộ.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "C", "answer": "", "gold_units": ["TT72-2024-BCA/D4/K4"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-066 · tier C · TT71-2024-BCA/D6/K3

Thông tư số 71/2024/TT-BCA (Quy định quản lý, vận hành, sử dụng hệ thống quản lý dữ liệu thiết bị giám sát hành trình và thiết bị ghi nhận hình ảnh người lái xe)

`TT71-2024-BCA/D6/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 6. Hệ thống dữ liệu thiết bị giám sát hành trình và thiết bị ghi nhận hình ảnh người lái xe
> 3. Máy chủ dịch vụ và máy chủ của Cục Cảnh sát giao thông tham gia việc truyền, nhận dữ liệu hành trình, dữ liệu hình ảnh người lái xe phải được đồng bộ hóa với thời gian chuẩn quốc gia theo chuẩn NTP (Network Time Protocol).


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "C", "answer": "", "gold_units": ["TT71-2024-BCA/D6/K3"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-067 · tier C · TT72-2024-BCA/D15/K3

Thông tư số 72/2024/TT-BCA (Quy định quy trình điều tra, giải quyết tai nạn giao thông đường bộ của Cảnh sát giao thông)

`TT72-2024-BCA/D15/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 15. Dựng lại hiện trường vụ tai nạn giao thông đường bộ
> 3. Kết thúc dựng lại hiện trường vụ tai nạn giao thông đường bộ phải lập Biên bản khám nghiệm hiện trường dựng lại, vẽ Sơ đồ hiện trường vụ tai nạn giao thông đường bộ được dựng lại; những người tham gia dựng lại hiện trường ký, ghi rõ họ, tên vào biên bản và sơ đồ.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "hanh_vi_cam_nghia_vu", "tier": "C", "answer": "", "gold_units": ["TT72-2024-BCA/D15/K3"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-068 · tier historical · TT35-2024-BGTVT/D53/K3

Thông tư số 35/2024/TT-BGTVT (Quy định về đào tạo, sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế; đào tạo, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ)

`TT35-2024-BGTVT/D53/K3#2025-01-01` · hiệu lực 2025-01-01 → 2025-08-31

> Điều 53. Cấp lại chứng chỉ
> 3. Trình tự thực hiện:
> a) Cá nhân nộp 01 bộ hồ sơ đến cơ sở đào tạo lái xe ô tô hoặc cơ sở đào tạo người điều khiển xe máy chuyên dùng đã cấp chứng chỉ; trường hợp cơ sở đào tạo đã cấp chứng chỉ không còn hoạt động thì nộp tại Sở Giao thông vận tải nơi quản lý cơ sở cấp chứng chỉ;
> b) Cơ sở đào tạo lái xe ô tô hoặc cơ sở đào tạo người điều khiển xe máy chuyên dùng hoặc Sở Giao thông vận tải kiểm tra hồ sơ khi tiếp nhận; trường hợp chứng chỉ không thuộc đối tượng được cấp lại hoặc hồ sơ không đúng theo quy định, phải thông báo trực tiếp hoặc bằng văn bản những nội dung cần bổ sung hoặc sửa đổi cho cá nhân trong thời hạn 02 ngày làm việc, kể từ ngày nhận hồ sơ;
> c) Trong thời hạn 03 ngày làm việc, kể từ ngày nhận đủ hồ sơ hợp lệ, người đứng đầu cơ sở đào tạo lái xe ô tô hoặc cơ sở đào tạo người điều khiển xe máy chuyên dùng hoặc Sở Giao thông vận tải cấp lại chứng chỉ; trường hợp không cấp lại chứng chỉ thì phải trả lời bằng văn bản và nêu rõ lý do;
> d) Việc trả giấy phép lái xe được thực hiện tại cơ sở đào tạo lái xe ô tô hoặc cơ sở đào tạo người điều khiển xe máy chuyên dùng hoặc cơ quan tiếp nhận hồ sơ hoặc thông qua dịch vụ bưu chính theo yêu cầu của cá …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2025-08-31", "question_type": "hanh_vi_cam_nghia_vu", "tier": "historical", "answer": "", "gold_units": ["TT35-2024-BGTVT/D53/K3"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-069 · tier historical · TT35-2024-BGTVT/D7/K3

Thông tư số 35/2024/TT-BGTVT (Quy định về đào tạo, sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế; đào tạo, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ)

`TT35-2024-BGTVT/D7/K3#2025-01-01` · hiệu lực 2025-01-01 → 2025-08-31

> Điều 7. Đào tạo lái xe các hạng B, C1
> 3. Báo cáo đăng ký sát hạch Cơ sở đào tạo lái xe tiếp nhận hồ sơ của người học lái xe đảm bảo đủ điều kiện và thành phần hồ sơ theo quy định tại Điều 14, Điều 15 Thông tư này; lập báo cáo đăng ký sát hạch (báo cáo 1) gửi Sở Giao thông vận tải bằng một trong các hình thức: trực tiếp, dịch vụ bưu chính, trên môi trường điện tử đồng thời truyền dữ liệu qua hệ thống thông tin giấy phép lái xe:
> a) Đào tạo lái xe các hạng B, C1: cơ sở đào tạo lái xe lập báo cáo đăng ký sát hạch lái xe, danh sách học viên (báo cáo 1), kế hoạch đào tạo theo quy định tại Mẫu số 01, Mẫu số 02, Mẫu số 04 Phụ lục IV ban hành kèm theo Thông tư này gửi Sở Giao thông vận tải; báo cáo phải có dấu giáp lai của cơ sở đào tạo lái xe;
> b) Báo cáo 1 các hạng B, C1 không quá 07 ngày làm việc sau khai giảng; Thủ trưởng đơn vị được Sở Giao thông vận tải giao nhiệm vụ quản lý sát hạch, cấp giấy phép lái xe kiểm tra, ký tên vào từng trang (bao gồm tất cả các trang của báo cáo 1).


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2025-08-31", "question_type": "hanh_vi_cam_nghia_vu", "tier": "historical", "answer": "", "gold_units": ["TT35-2024-BGTVT/D7/K3"], "required_numbers": []}
```

### W-hanh_vi_cam_nghia_vu-070 · tier historical · TT35-2024-BGTVT/D22/K2

Thông tư số 35/2024/TT-BGTVT (Quy định về đào tạo, sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế; đào tạo, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ)

`TT35-2024-BGTVT/D22/K2#2025-01-01` · hiệu lực 2025-01-01 → 2025-08-31

> Điều 22. Chuẩn bị kỳ sát hạch
> 2. Đối với kỳ sát hạch lái xe các hạng B1, B, C1, C, D1, D2, D, BE, C1E,
> CE, D1E, D2E, DE
> a) Tiếp nhận báo cáo đề nghị tổ chức sát hạch lái xe kèm danh sách thí sinh dự sát hạch (báo cáo 2) của cơ sở đào tạo lái xe theo quy định tại Mẫu số 08, Mẫu số 09 Phụ lục XX ban hành kèm theo Thông tư này; báo cáo 2 gửi qua dịch vụ bưu chính và truyền dữ liệu về hệ thống thông tin đào tạo lái xe tại Sở Giao thông vận tải trước kỳ sát hạch 07 ngày làm việc;
> b) Kiểm tra điều kiện và hồ sơ của người dự sát hạch để cấp giấy phép lái xe các hạng B1, B, C1, C, D1, D2, D, BE, C1E, CE, D1E, D2E, DE theo quy định tại Điều 28 và Điều 29 Thông tư này và người dự sát hạch phải có tên trong danh sách học viên (báo cáo 1);
> c) Xác minh giấy phép lái xe đã cấp (đối với trường hợp nâng hạng giấy phép lái xe);
> d) Người được giao nhiệm vụ kiểm tra, duyệt hồ sơ thí sinh dự sát hạch lập biên bản kiểm tra hồ sơ theo quy định tại Mẫu số 01 Phụ lục XX ban hành kèm theo Thông tư này;
> đ) Căn cứ danh sách hồ sơ thí sinh dự sát hạch hợp lệ kèm theo Biên bản kiểm tra hồ sơ và điều kiện dự thi của thí sinh dự sát hạch lái xe theo quy định tại Mẫu số 01 Phụ lục XX ban hành kèm theo Thông tư …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2025-08-31", "question_type": "hanh_vi_cam_nghia_vu", "tier": "historical", "answer": "", "gold_units": ["TT35-2024-BGTVT/D22/K2"], "required_numbers": []}
```

## dinh_nghia — khái niệm, thuật ngữ được giải thích

### W-dinh_nghia-001 · tier A · LUAT35-2024/D68/K1

Luật Đường bộ số 35/2024/QH15

`LUAT35-2024/D68/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 68. Hàng hoá ký gửi
> 1. Hàng hoá ký gửi là hàng hoá gửi theo xe ô tô kinh doanh vận tải hành khách mà người gửi không đi cùng trên xe, được thực hiện theo thỏa thuận giữa người kinh doanh vận tải và người gửi hàng.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "A", "answer": "", "gold_units": ["LUAT35-2024/D68/K1"], "required_numbers": []}
```

### W-dinh_nghia-002 · tier A · TT53-2024-BGTVT/D3/K5

Thông tư số 53/2024/TT-BGTVT (Quy định về phân loại phương tiện giao thông đường bộ và dấu hiệu nhận biết xe cơ giới sử dụng năng lượng sạch, năng lượng xanh, thân thiện môi trường)

`TT53-2024-BGTVT/D3/K5#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 3. Giải thích từ ngữ
> 5. Xe hybrid điện (HEV - Hybrid electric vehicle) là xe cơ giới được dẫn động bằng hệ thống truyền động hybrid điện (bao gồm cả xe sử dụng nhiên liệu tiêu thụ chỉ để nạp điện cho thiết bị tích trữ điện năng), gồm có:
> a) Xe hybrid điện nhẹ (MHEV - Mild hybrid electric vehicle) là xe hybrid điện; động cơ (mô-tơ) điện có chức năng hỗ trợ động cơ đốt trong khởi động, hỗ trợ tăng tốc, phanh tái tạo và cung cấp năng lượng cho hệ thống phụ trợ. Xe không có khả năng nạp điện được từ nguồn điện bên ngoài;
> b) Xe hybrid điện hoàn toàn (FHEV- Full hybrid electric vehicle hoặc SHEV - Strong hybrid electric vehicle) là xe hybrid điện có khả năng di chuyển hoàn toàn chỉ bằng năng lượng điện trong những điều kiện nhất định (như bắt đầu di chuyển từ trạng thái đứng yên, di chuyển ở tốc độ thấp...). Xe không có khả năng nạp điện được từ nguồn điện bên ngoài;
> c) Xe hybrid nạp điện ngoài (PHEV - Plug-in hybrid electric vehicle) là xe hybrid điện có khả năng nạp điện được từ nguồn điện bên ngoài.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "A", "answer": "", "gold_units": ["TT53-2024-BGTVT/D3/K5"], "required_numbers": []}
```

### W-dinh_nghia-003 · tier A · TT14-2025-BXD/D3/K2

Thông tư số 14/2025/TT-BXD (Quy định về đào tạo lái xe; bồi dưỡng, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ)

`TT14-2025-BXD/D3/K2#2025-09-01` · hiệu lực 2025-09-01 → nay

> Điều 3. Giải thích từ ngữ
> 2. Dữ liệu DAT là tập hợp các thông tin về định danh và quá trình học thực hành lái xe trên đường của học viên, được truyền từ thiết bị DAT lắp trên xe ô tô tập lái để tập lái xe trên đường về máy chủ của cơ sở đào tạo lái xe.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "A", "answer": "", "gold_units": ["TT14-2025-BXD/D3/K2"], "required_numbers": []}
```

### W-dinh_nghia-004 · tier A · LUAT35-2024/D2/K6

Luật Đường bộ số 35/2024/QH15

`LUAT35-2024/D2/K6#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 2. Giải thích từ ngữ
> 6. Cơ quan quản lý đường bộ là cơ quan thuộc Bộ Giao thông vận tải giúp Bộ trưởng Bộ Giao thông vận tải thực hiện chức năng quản lý nhà nước về hoạt động đường bộ; cơ quan chuyên môn thuộc Ủy ban nhân dân cấp tỉnh; cơ quan chuyên môn thuộc Ủy ban nhân dân cấp huyện; Ủy ban nhân dân cấp xã.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "A", "answer": "", "gold_units": ["LUAT35-2024/D2/K6"], "required_numbers": []}
```

### W-dinh_nghia-005 · tier A · LUAT35-2024/D9/K4

Luật Đường bộ số 35/2024/QH15

`LUAT35-2024/D9/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 9. Phân loại đường bộ theo chức năng phục vụ
> 4. Đường bên là đường được xây dựng bên cạnh các đoạn đường chính để ngăn cách giao thông khu vực hai bên đường với đường chính. Đường bên được tách khỏi đường chính hoặc ngăn cách với đường chính bằng dải phân cách, tường bảo vệ, rào chắn.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "A", "answer": "", "gold_units": ["LUAT35-2024/D9/K4"], "required_numbers": []}
```

### W-dinh_nghia-006 · tier A · TT53-2024-BGTVT/D3/K2

Thông tư số 53/2024/TT-BGTVT (Quy định về phân loại phương tiện giao thông đường bộ và dấu hiệu nhận biết xe cơ giới sử dụng năng lượng sạch, năng lượng xanh, thân thiện môi trường)

`TT53-2024-BGTVT/D3/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 3. Giải thích từ ngữ
> 2. Xe thuần điện (PEV - Pure electric vehicle hoặc BEV - Battery electric vehicle) là xe cơ giới sử dụng hệ thống truyền động điện;


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "A", "answer": "", "gold_units": ["TT53-2024-BGTVT/D3/K2"], "required_numbers": []}
```

### W-dinh_nghia-007 · tier A · LUAT35-2024/D43/K2

Luật Đường bộ số 35/2024/QH15

`LUAT35-2024/D43/K2#2024-10-01` · hiệu lực 2024-10-01 → nay

> Điều 43. Thanh toán điện tử giao thông đường bộ
> 2. Tài khoản giao thông là tài khoản mở cho chủ phương tiện giao thông đường bộ và kết nối với phương tiện thanh toán hợp pháp để thực hiện thanh toán không dùng tiền mặt theo quy định của pháp luật về ngân hàng.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "A", "answer": "", "gold_units": ["LUAT35-2024/D43/K2"], "required_numbers": []}
```

### W-dinh_nghia-008 · tier A · TT38-2024-BGTVT/D5/K1

Thông tư số 38/2024/TT-BGTVT (Quy định về tốc độ và khoảng cách an toàn của xe cơ giới, xe máy chuyên dùng tham gia giao thông trên đường bộ)

`TT38-2024-BGTVT/D5/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 5. Tốc độ thiết kế của đường bộ
> 1. Tốc độ thiết kế của đường bộ là giá trị vận tốc được dùng để tính toán các chỉ tiêu kỹ thuật của đường bộ. Tốc độ thiết kế của đường bộ được xác định trong giai đoạn đầu tư xây dựng, nâng cấp, cải tạo đường bộ nhằm bảo đảm cho phương tiện di chuyển an toàn; được quyết định theo cấp kỹ thuật của đường bộ và điều kiện địa hình.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "A", "answer": "", "gold_units": ["TT38-2024-BGTVT/D5/K1"], "required_numbers": []}
```

### W-dinh_nghia-009 · tier A · LUAT35-2024/D27/K1

Luật Đường bộ số 35/2024/QH15

`LUAT35-2024/D27/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 27. Tải trọng và khổ giới hạn của đường bộ
> 1. Tải trọng của đường bộ là khả năng chịu tải khai thác của đường bộ để bảo đảm khai thác an toàn và tuổi thọ công trình đường bộ.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "A", "answer": "", "gold_units": ["LUAT35-2024/D27/K1"], "required_numbers": []}
```

### W-dinh_nghia-010 · tier A · TT12-2025-BCA/D26/K1

Thông tư số 12/2025/TT-BCA (Quy định về sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế)

`TT12-2025-BCA/D26/K1#2025-03-01` · hiệu lực 2025-03-01 → nay

> Điều 26. Mẫu giấy phép lái xe quốc tế
> 1. IDP là một quyển sổ có kích thước A6 (148 mm x 105 mm), có ký hiệu bảo mật, bìa màu xám, những trang giấy bên trong màu trắng theo mẫu quy định tại Phụ lục XV ban hành kèm theo Thông tư này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "A", "answer": "", "gold_units": ["TT12-2025-BCA/D26/K1"], "required_numbers": []}
```

### W-dinh_nghia-011 · tier A · TT65-2024-BCA/D3

Thông tư số 65/2024/TT-BCA (Quy định kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ để được phục hồi điểm giấy phép lái xe)

`TT65-2024-BCA/D3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 3. Người được tham gia kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ
> Người được tham gia kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ là người có giấy phép lái xe bị trừ hết điểm.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "A", "answer": "", "gold_units": ["TT65-2024-BCA/D3"], "required_numbers": []}
```

### W-dinh_nghia-012 · tier A · LUAT36-2024/D54/K1

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D54/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 54. Bảo đảm trật tự, an toàn giao thông đường bộ đối với xe cứu hộ giao thông đường bộ
> 1. Xe cứu hộ giao thông đường bộ là xe ô tô chuyên dùng có trang bị dụng cụ, thiết bị dùng để cứu hộ, hỗ trợ di chuyển hoặc chuyên chở các phương tiện giao thông đường bộ bị hư hỏng, bị sự cố.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D54/K1"], "required_numbers": []}
```

### W-dinh_nghia-013 · tier A · LUAT35-2024/D71

Luật Đường bộ số 35/2024/QH15

`LUAT35-2024/D71#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 71. Dịch vụ hỗ trợ vận tải đường bộ
> Dịch vụ hỗ trợ vận tải đường bộ bao gồm: kinh doanh dịch vụ bến xe, trạm dừng nghỉ, bãi đỗ xe, đại lý vận tải hàng hóa, đại lý bán vé, dịch vụ thu gom hàng, dịch vụ chuyển tải, dịch vụ kho bãi hàng hoá, dịch vụ xếp, dỡ hàng hoá trên phương tiện tham gia giao thông đường bộ, dịch vụ cho thuê phương tiện giao thông cơ giới đường bộ, dịch vụ cứu hộ giao thông đường bộ, dịch vụ phần mềm hỗ trợ kết nối vận tải bằng xe ô tô.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "A", "answer": "", "gold_units": ["LUAT35-2024/D71"], "required_numbers": []}
```

### W-dinh_nghia-014 · tier A · LUAT36-2024/D34/K4

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D34/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 34. Phân loại phương tiện giao thông đường bộ
> 4. Phương tiện giao thông thông minh là xe cơ giới cho phép tự động hóa một phần hoặc toàn bộ hoạt động điều khiển phương tiện, xác định lộ trình và xử lý tình huống khi tham gia giao thông đường bộ.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D34/K4"], "required_numbers": []}
```

### W-dinh_nghia-015 · tier A · TT38-2024-BGTVT/D5/K3

Thông tư số 38/2024/TT-BGTVT (Quy định về tốc độ và khoảng cách an toàn của xe cơ giới, xe máy chuyên dùng tham gia giao thông trên đường bộ)

`TT38-2024-BGTVT/D5/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 5. Tốc độ thiết kế của đường bộ
> 3. Tốc độ thiết kế đường bộ được xác định theo Tiêu chuẩn quốc gia TCVN 4054: 2005 Đường ô tô - Yêu cầu thiết kế.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "A", "answer": "", "gold_units": ["TT38-2024-BGTVT/D5/K3"], "required_numbers": []}
```

### W-dinh_nghia-016 · tier A · LUAT36-2024/D2/K7

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D2/K7#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 2. Giải thích từ ngữ
> 7. Cải tạo xe (sau đây gọi là cải tạo) là việc thay đổi đặc điểm của xe đã được cấp đăng ký xe, biển số xe hoặc xe đã qua sử dụng được nhập khẩu dẫn đến thay đổi về kiểu loại xe theo quy định của cơ quan có thẩm quyền.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D2/K7"], "required_numbers": []}
```

### W-dinh_nghia-017 · tier A · TT53-2024-BGTVT/D8/K2

Thông tư số 53/2024/TT-BGTVT (Quy định về phân loại phương tiện giao thông đường bộ và dấu hiệu nhận biết xe cơ giới sử dụng năng lượng sạch, năng lượng xanh, thân thiện môi trường)

`TT53-2024-BGTVT/D8/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 8. Phương tiện giao thông thông minh
> 2. Xe cơ giới cho phép tự động hóa toàn phần hoạt động điều khiển phương tiện, xác định lộ trình và xử lý tình huống khi tham gia giao thông đường bộ là các xe thuộc cấp độ 4 (Level or Category 4) hoặc cấp độ 5 (Level or Category 5) được phân loại và định nghĩa trong tiêu chuẩn ISO/SAE PAS 22736:2021 Phân loại và định nghĩa đối với các thuật ngữ liên quan đến hệ thống tự lái của xe cơ giới (Taxonomy and definitions for terms related to driving automation systems for on-road motor vehicles).


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "A", "answer": "", "gold_units": ["TT53-2024-BGTVT/D8/K2"], "required_numbers": []}
```

### W-dinh_nghia-018 · tier A · LUAT36-2024/D34/K5

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D34/K5#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 34. Phân loại phương tiện giao thông đường bộ
> 5. Xe tương tự các loại xe cơ giới, xe thô sơ được quản lý, sử dụng theo quy định đối với loại xe cơ giới, xe thô sơ đó.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D34/K5"], "required_numbers": []}
```

### W-dinh_nghia-019 · tier A · TT12-2025-BCA/D3/K5

Thông tư số 12/2025/TT-BCA (Quy định về sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế)

`TT12-2025-BCA/D3/K5#2025-03-01` · hiệu lực 2025-03-01 → nay

> Điều 3. Giải thích từ ngữ
> 5. Giấy phép lái xe quốc tế là giấy phép lái xe có tên tiếng Anh là International Driving Permit, sau đây gọi tắt là IDP.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "A", "answer": "", "gold_units": ["TT12-2025-BCA/D3/K5"], "required_numbers": []}
```

### W-dinh_nghia-020 · tier A · LUAT36-2024/D15/K1

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D15/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 15. Chuyển hướng xe
> 1. Chuyển hướng xe là tình huống giao thông mà xe rẽ trái hoặc rẽ phải hoặc quay đầu xe.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D15/K1"], "required_numbers": []}
```

### W-dinh_nghia-021 · tier A · TT53-2024-BGTVT/D3/K1

Thông tư số 53/2024/TT-BGTVT (Quy định về phân loại phương tiện giao thông đường bộ và dấu hiệu nhận biết xe cơ giới sử dụng năng lượng sạch, năng lượng xanh, thân thiện môi trường)

`TT53-2024-BGTVT/D3/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 3. Giải thích từ ngữ
> 1. Hệ thống truyền động điện (Electric powertrain) là hệ thống bao gồm một hoặc nhiều: thiết bị tích trữ điện năng (ắc quy, pin, bánh đà điện cơ hoặc siêu tụ); thiết bị ổn định điện năng; thiết bị điện được sử dụng để chuyển đổi điện năng tích trữ thành cơ năng truyền tới các bánh xe làm nguồn động lực cho xe chuyển động;


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "A", "answer": "", "gold_units": ["TT53-2024-BGTVT/D3/K1"], "required_numbers": []}
```

### W-dinh_nghia-022 · tier A · TT14-2025-BXD/D3/K5

Thông tư số 14/2025/TT-BXD (Quy định về đào tạo lái xe; bồi dưỡng, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ)

`TT14-2025-BXD/D3/K5#2025-09-01` · hiệu lực 2025-09-01 → nay

> Điều 3. Giải thích từ ngữ
> 5. Hệ thống thông tin về đào tạo lái xe, chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ là tập hợp phần cứng, phần mềm hệ thống, phần mềm ứng dụng, cơ sở dữ liệu và đường truyền phục vụ công tác quản lý thông tin về đào tạo lái xe, chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ, bao gồm: Hệ thống thông tin quản lý, giám sát đào tạo lái xe và Hệ thống thông tin chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "A", "answer": "", "gold_units": ["TT14-2025-BXD/D3/K5"], "required_numbers": []}
```

### W-dinh_nghia-023 · tier A · TT38-2024-BGTVT/D5/K5

Thông tư số 38/2024/TT-BGTVT (Quy định về tốc độ và khoảng cách an toàn của xe cơ giới, xe máy chuyên dùng tham gia giao thông trên đường bộ)

`TT38-2024-BGTVT/D5/K5#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 5. Tốc độ thiết kế của đường bộ
> 5. Tốc độ thiết kế đường giao thông nông thôn được xác định theo Tiêu chuẩn quốc gia TCVN 10380:2014 Đường giao thông nông thôn - Yêu cầu thiết kế.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "A", "answer": "", "gold_units": ["TT38-2024-BGTVT/D5/K5"], "required_numbers": []}
```

### W-dinh_nghia-024 · tier A · LUAT36-2024/D63/K1

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D63/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 63. Đào tạo, kiểm tra cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ cho người điều khiển xe máy chuyên dùng
> 1. Chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ là giấy chứng nhận cấp cho người có đủ điều kiện theo quy định của pháp luật để điều khiển xe máy chuyên dùng tham gia giao thông đường bộ.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D63/K1"], "required_numbers": []}
```

### W-dinh_nghia-025 · tier A · TT12-2025-BCA/D3/K1

Thông tư số 12/2025/TT-BCA (Quy định về sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế)

`TT12-2025-BCA/D3/K1#2025-03-01` · hiệu lực 2025-03-01 → nay

> Điều 3. Giải thích từ ngữ
> 1. Số phôi giấy phép lái xe là mã số do nhà sản xuất phôi ghi ở mặt sau của giấy phép lái xe, bao gồm 02 chữ cái và các số phía sau.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "A", "answer": "", "gold_units": ["TT12-2025-BCA/D3/K1"], "required_numbers": []}
```

### W-dinh_nghia-026 · tier A · LUAT36-2024/D74/K1

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D74/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 74. Chỉ huy, điều khiển giao thông đường bộ
> 1. Chỉ huy giao thông đường bộ là tổng hợp các hoạt động thu thập, phân tích, đánh giá các yếu tố có liên quan để đưa ra các giải pháp điều hành hoạt động giao thông đường bộ trật tự, an toàn, thông suốt, được thực hiện thông qua người có thẩm quyền chỉ huy giao thông; trung tâm chỉ huy giao thông; thiết bị thông minh hỗ trợ chỉ huy, điều khiển giao thông đường bộ.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D74/K1"], "required_numbers": []}
```

### W-dinh_nghia-027 · tier A · LUAT36-2024/D71/K1

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D71/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 71. Hệ thống giám sát bảo đảm an ninh, trật tự, an toàn giao thông đường bộ; hệ thống quản lý dữ liệu thiết bị giám sát hành trình và thiết bị ghi nhận hình ảnh người lái xe; hệ thống thiết bị kỹ thuật nghiệp vụ kiểm tra tải trọng xe cơ giới
> 1. Hệ thống giám sát bảo đảm an ninh, trật tự, an toàn giao thông đường bộ được quy định như sau:
> a) Hệ thống giám sát bảo đảm an ninh, trật tự, an toàn giao thông đường bộ là hệ thống thu thập tín hiệu, dữ liệu, âm thanh, hình ảnh về hành trình của phương tiện tham gia giao thông đường bộ, tình trạng giao thông và các dữ liệu liên quan khác được xây dựng, lắp đặt trên các tuyến giao thông đường bộ theo quy chuẩn kỹ thuật quốc gia để giám sát tình hình an ninh, trật tự, an toàn giao thông đường bộ; phát hiện vi phạm pháp luật về trật tự, an toàn giao thông đường bộ và vi phạm pháp luật khác;
> b) Việc xây dựng, quản lý, vận hành, sử dụng hệ thống giám sát bảo đảm an ninh, trật tự, an toàn giao thông đường bộ phải tuân thủ đúng quy trình, quy tắc, bảo đảm hoạt động liên tục và kết nối với Trung tâm chỉ huy giao thông;
> c) Dữ liệu thu thập được từ hệ thống giám sát bảo đảm an ninh, trật tự, an toàn giao thông đường bộ phải được quản lý theo …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D71/K1"], "required_numbers": []}
```

### W-dinh_nghia-028 · tier A · LUAT35-2024/D9/K2

Luật Đường bộ số 35/2024/QH15

`LUAT35-2024/D9/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 9. Phân loại đường bộ theo chức năng phục vụ
> 2. Đường nhánh là đường nối vào đường chính, có chức năng kết nối giao thông các khu vực hai bên đường chính; kết nối giao thông từ đường gom vào đường chính thông qua nút giao.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "A", "answer": "", "gold_units": ["LUAT35-2024/D9/K2"], "required_numbers": []}
```

### W-dinh_nghia-029 · tier A · LUAT35-2024/D9/K6

Luật Đường bộ số 35/2024/QH15

`LUAT35-2024/D9/K6#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 9. Phân loại đường bộ theo chức năng phục vụ
> 6. Đường nội bộ là đường trong phạm vi khu chung cư, đô thị, công nghiệp, kinh tế, thương mại - dịch vụ, các cơ quan, tổ chức, đơn vị khác và chỉ phục vụ các đối tượng được phép vào, ra bên trong phạm vi các khu vực quy định tại khoản này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "A", "answer": "", "gold_units": ["LUAT35-2024/D9/K6"], "required_numbers": []}
```

### W-dinh_nghia-030 · tier A · LUAT36-2024/D2/K5

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D2/K5#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 2. Giải thích từ ngữ
> 5. Phần đường xe chạy là phần của đường bộ được sử dụng cho phương tiện giao thông đường bộ đi lại.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D2/K5"], "required_numbers": []}
```

### W-dinh_nghia-031 · tier A · LUAT36-2024/D2/K11

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D2/K11#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 2. Giải thích từ ngữ
> 11. Ùn tắc giao thông đường bộ (sau đây gọi là ùn tắc giao thông) là tình trạng người, phương tiện tham gia giao thông đường bộ bị dồn ứ, di chuyển với tốc độ rất chậm hoặc không thể di chuyển được.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D2/K11"], "required_numbers": []}
```

### W-dinh_nghia-032 · tier A · TT38-2024-BGTVT/D3/K1

Thông tư số 38/2024/TT-BGTVT (Quy định về tốc độ và khoảng cách an toàn của xe cơ giới, xe máy chuyên dùng tham gia giao thông trên đường bộ)

`TT38-2024-BGTVT/D3/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 3. Giải thích từ ngữ
> 1. Đường bộ trong khu đông dân cư là đoạn đường bộ nằm trong khu vực nội thành phố, nội thị xã, nội thị trấn và những đoạn đường có đông dân cư sinh sống sát dọc theo đường, được xác định bằng biển báo “Bắt đầu khu đông dân cư” và biển báo “Hết khu đông dân cư”.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "A", "answer": "", "gold_units": ["TT38-2024-BGTVT/D3/K1"], "required_numbers": []}
```

### W-dinh_nghia-033 · tier B · QD19-2024-TTG/D3/K3

Quyết định số 19/2024/QĐ-TTg (Quy định lộ trình áp dụng mức tiêu chuẩn khí thải đối với xe cơ giới nhập khẩu và sản xuất, lắp ráp)

`QD19-2024-TTG/D3/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 3. Giải thích từ ngữ
> 3. Mức tiêu chuẩn khí thải bằng “0” quy định tại Quyết định này là mức thể hiện khí thải phát sinh từ động cơ của xe cơ giới không có các chất gây ô nhiễm đã được quy định giới hạn trong các mức tiêu chuẩn khí thải nêu tại khoản 1, khoản 2 của Điều này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "B", "answer": "", "gold_units": ["QD19-2024-TTG/D3/K3"], "required_numbers": []}
```

### W-dinh_nghia-034 · tier B · ND158-2024/D3/K15

Nghị định số 158/2024/NĐ-CP (Quy định về hoạt động vận tải đường bộ)

`ND158-2024/D3/K15#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 3. Giải thích từ ngữ
> 15. Đơn vị kinh doanh vận tải bao gồm: doanh nghiệp được cấp Giấy chứng nhận đăng ký doanh nghiệp và được cấp Giấy phép kinh doanh vận tải; tổ hợp tác, hợp tác xã, liên hiệp hợp tác xã có Giấy chứng nhận đăng ký hợp tác xã hoặc Giấy chứng nhận đăng ký tổ hợp tác và được cấp Giấy phép kinh doanh vận tải; hộ kinh doanh đã được cấp Giấy chứng nhận đăng ký hộ kinh doanh và được cấp Giấy phép kinh doanh vận tải. Đối với vận tải đường bộ quốc tế, đơn vị kinh doanh vận tải bao gồm: doanh nghiệp được cấp Giấy chứng nhận đăng ký doanh nghiệp và được cấp Giấy phép kinh doanh vận tải; tổ hợp tác, hợp tác xã, liên hiệp hợp tác xã có Giấy chứng nhận đăng ký hợp tác xã hoặc Giấy chứng nhận đăng ký tổ hợp tác và được cấp Giấy phép kinh doanh vận tải.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "B", "answer": "", "gold_units": ["ND158-2024/D3/K15"], "required_numbers": []}
```

### W-dinh_nghia-035 · tier B · TT52-2024-BGTVT/D3/K4

Thông tư số 52/2024/TT-BGTVT (Quy định về yêu cầu kỹ thuật đối với xe cơ giới, xe máy chuyên dùng thuộc đối tượng nghiên cứu phát triển có nhu cầu tham gia giao thông đường bộ)

`TT52-2024-BGTVT/D3/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 3. Giải thích từ ngữ
> 4. Phụ tùng chưa qua sử dụng là các tổng thành, hệ thống, chi tiết của xe chưa được sử dụng để sản xuất, lắp ráp xe hoặc sử dụng với bất kỳ mục đích nào khác.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "B", "answer": "", "gold_units": ["TT52-2024-BGTVT/D3/K4"], "required_numbers": []}
```

### W-dinh_nghia-036 · tier B · ND158-2024/D3/K3

Nghị định số 158/2024/NĐ-CP (Quy định về hoạt động vận tải đường bộ)

`ND158-2024/D3/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 3. Giải thích từ ngữ
> 3. Trọng tải thiết kế của xe ô tô là số người và khối lượng hàng hóa tối đa mà xe ô tô đó được chở theo quy định của nhà sản xuất.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "B", "answer": "", "gold_units": ["ND158-2024/D3/K3"], "required_numbers": []}
```

### W-dinh_nghia-037 · tier B · ND158-2024/D3/K8

Nghị định số 158/2024/NĐ-CP (Quy định về hoạt động vận tải đường bộ)

`ND158-2024/D3/K8#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 3. Giải thích từ ngữ
> 8. Bộ phận quản lý an toàn của đơn vị kinh doanh vận tải là bộ phận do đơn vị kinh doanh vận tải thành lập để thực hiện nhiệm vụ theo dõi, giám sát và quản lý hoạt động của lái xe, phương tiện nhằm bảo đảm an toàn giao thông trong suốt quá trình hoạt động kinh doanh vận tải.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "B", "answer": "", "gold_units": ["ND158-2024/D3/K8"], "required_numbers": []}
```

### W-dinh_nghia-038 · tier B · ND130-2024/D7/K4

Nghị định số 130/2024/NĐ-CP (Quy định về thu phí sử dụng đường bộ cao tốc đối với phương tiện lưu thông trên tuyến đường bộ cao tốc thuộc sở hữu toàn dân do nhà nước đại diện chủ sở hữu và trực tiếp quản lý, khai thác)

`ND130-2024/D7/K4#2024-10-10` · hiệu lực 2024-10-10 → nay

> Điều 7. Cơ quan quản lý thu phí, nhà cung cấp dịch vụ thanh toán tiền sử dụng đường bộ, đơn vị vận hành thu, cơ quan nhượng quyền thu phí, tổ chức nhận nhượng quyền thu phí sử dụng đường bộ cao tốc
> 4. Cơ quan nhượng quyền thu phí sử dụng đường bộ cao tốc là cơ quan quản lý đường bộ được giao ký hợp đồng nhượng quyền thu phí sử dụng đường bộ cao tốc.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "B", "answer": "", "gold_units": ["ND130-2024/D7/K4"], "required_numbers": []}
```

### W-dinh_nghia-039 · tier B · TT52-2024-BGTVT/D3/K6

Thông tư số 52/2024/TT-BGTVT (Quy định về yêu cầu kỹ thuật đối với xe cơ giới, xe máy chuyên dùng thuộc đối tượng nghiên cứu phát triển có nhu cầu tham gia giao thông đường bộ)

`TT52-2024-BGTVT/D3/K6#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 3. Giải thích từ ngữ
> 6. Kiểm tra chất lượng xuất xưởng là việc cơ sở nghiên cứu phát triển kiểm tra các hệ thống an toàn kỹ thuật của xe nghiên cứu phát triển theo tiêu chuẩn của nhà sản xuất.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "B", "answer": "", "gold_units": ["TT52-2024-BGTVT/D3/K6"], "required_numbers": []}
```

### W-dinh_nghia-040 · tier B · ND158-2024/D3/K4

Nghị định số 158/2024/NĐ-CP (Quy định về hoạt động vận tải đường bộ)

`ND158-2024/D3/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 3. Giải thích từ ngữ
> 4. Giờ xuất bến của từng chuyến xe là mốc thời gian để xác định thời điểm xe phải rời khỏi bến xe khách.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "dinh_nghia", "tier": "B", "answer": "", "gold_units": ["ND158-2024/D3/K4"], "required_numbers": []}
```

## thu_tuc_tham_quyen — thủ tục, hồ sơ, điều kiện, thẩm quyền, cơ quan có trách nhiệm

### W-thu_tuc_tham_quyen-001 · tier A · LUAT35-2024/D83/K2

Luật Đường bộ số 35/2024/QH15

`LUAT35-2024/D83/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 83. Thanh tra đường bộ
> 2. Thanh tra, kiểm tra, xử lý vi phạm pháp luật về hoạt động đào tạo, sát hạch, cấp giấy phép lái xe cơ giới đường bộ, hoạt động kiểm định an toàn kỹ thuật và bảo vệ môi trường đối với xe cơ giới, trừ hoạt động đào tạo, sát hạch, cấp giấy phép lái xe, kiểm định an toàn kỹ thuật và bảo vệ môi trường đối với xe của lực lượng Quân đội nhân dân, Công an nhân dân làm nhiệm vụ quốc phòng, an ninh theo quy định của pháp luật về trật tự, an toàn giao thông đường bộ;


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["LUAT35-2024/D83/K2"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-002 · tier A · ND151-2024/D13/K2

Nghị định số 151/2024/NĐ-CP (Quy định chi tiết một số điều và biện pháp thi hành Luật Trật tự, an toàn giao thông đường bộ)

`ND151-2024/D13/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 13. Cập nhật thông tin trong Cơ sở dữ liệu về trật tự, an toàn giao thông đường bộ
> 2. Cơ quan trực tiếp xây dựng, quản lý, vận hành, khai thác, sử dụng cơ sở dữ liệu quy định tại khoản 3 Điều 10 của Nghị định này có trách nhiệm bổ sung, điều chỉnh thông tin trong cơ sở dữ liệu do mình quản lý và đồng bộ với Cơ sở dữ liệu về trật tự, an toàn giao thông đường bộ theo quy định của pháp luật về kết nối và chia sẻ dữ liệu.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["ND151-2024/D13/K2"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-003 · tier A · TT12-2025-BCA/D17/K2

Thông tư số 12/2025/TT-BCA (Quy định về sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế)

`TT12-2025-BCA/D17/K2#2025-03-01` · hiệu lực 2025-03-01 → nay

> Điều 17. Lưu trữ hồ sơ kết quả sát hạch
> 2. Trường hợp cơ sở đào tạo lái xe có sân tập lái dùng để thực hiện sát hạch lái xe mô tô phải lưu trữ dữ liệu giám sát sát hạch; dữ liệu kết quả sát hạch lý thuyết, thực hành lái xe trong hình với thời hạn 03 năm, trừ sân tập lái quy định tại khoản 2 Điều 5 Thông tư này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["TT12-2025-BCA/D17/K2"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-004 · tier A · TT79-2024-BCA/D5/K1

Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)

`TT79-2024-BCA/D5/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 5. Trách nhiệm của cơ quan đăng ký xe và cán bộ đăng ký xe
> 1. Cơ quan đăng ký xe phải tổ chức tiếp nhận hồ sơ đăng ký xe các ngày làm việc trong tuần. Trường hợp cần thiết, Giám đốc Công an cấp tỉnh quyết định và thông báo công khai việc tổ chức tiếp nhận đăng ký xe ngoài giờ làm việc, ngày nghỉ, ngày lễ. Bố trí cán bộ đăng ký xe thường xuyên kiểm tra hệ thống đăng ký, quản lý xe, tiếp nhận hồ sơ để đảm bảo giải quyết đăng ký xe đúng thời gian theo quy định.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["TT79-2024-BCA/D5/K1"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-005 · tier A · TT12-2025-BCA/D24/K2

Thông tư số 12/2025/TT-BCA (Quy định về sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế)

`TT12-2025-BCA/D24/K2#2025-03-01` · hiệu lực 2025-03-01 → nay

> Điều 24. Đổi giấy phép lái xe của nước ngoài
> 2. Hồ sơ bao gồm:
> a) Đề nghị đổi giấy phép lái xe (đối với người Việt Nam theo mẫu quy định tại Phụ lục XII, đối với người nước ngoài theo mẫu quy định tại Phụ lục XIII ban hành kèm theo Thông tư này);
> b) Bản dịch giấy phép lái xe nước ngoài ra tiếng Việt được bảo chứng chất lượng dịch thuật của cơ quan Công chứng tại Việt Nam, cơ quan đại diện Việt Nam ở nước ngoài mà người dịch làm việc, đóng dấu giáp lai với bản sao giấy phép lái xe;
> c) Giấy khám sức khỏe của người lái xe do cơ sở khám bệnh, chữa bệnh đủ tiêu chuẩn theo quy định của pháp luật về khám bệnh, chữa bệnh cấp còn hiệu lực (trừ người nước ngoài đổi giấy phép lái xe theo thời hạn ghi trong thị thực nhập cảnh hoặc thẻ tạm trú);
> d) Bản sao hoặc bản sao điện tử được chứng thực từ bản chính hoặc bản sao điện tử được cấp từ sổ gốc của một trong các giấy tờ: giấy chứng minh thư ngoại giao, giấy chứng minh thư công vụ, thẻ tạm trú hoặc thẻ thường trú với thời gian từ 03 tháng trở lên.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["TT12-2025-BCA/D24/K2"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-006 · tier A · ND151-2024/D1/K4

Nghị định số 151/2024/NĐ-CP (Quy định chi tiết một số điều và biện pháp thi hành Luật Trật tự, an toàn giao thông đường bộ)

`ND151-2024/D1/K4#2026-07-01` · hiệu lực 2026-07-01 → nay

> Điều 1. Phạm vi điều chỉnh
> 4. Khoản 5 Điều 35 về lắp thiết bị giám sát hành trình đối với xe ô tô kinh doanh vận tải xe vận tải nội bộ; lắp thiết bị giám sát hành trình và thiết bị ghi nhận hình ảnh người lái xe đối với xe ô tô chở người từ 08 chỗ trở lên (không kể chỗ của người lái xe) kinh doanh vận tải, xe ô tô đầu kéo, xe cứu thương, xe cứu hộ giao thông đường bộ; cấp phép hoạt động đối với phương tiện giao thông thông minh; điều kiện hoạt động của xe thô sơ.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["ND151-2024/D1/K4"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-007 · tier A · TT79-2024-BCA/D8/K5

Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)

`TT79-2024-BCA/D8/K5#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 8. Hồ sơ cấp mới chứng nhận đăng ký xe, biển số xe
> 5. Chứng từ hoàn thành nghĩa vụ tài chính.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["TT79-2024-BCA/D8/K5"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-008 · tier A · ND168-2024/D51/K3

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D51/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 51. Thẩm quyền, trình tự, thủ tục phục hồi điểm giấy phép lái xe
> 3. Trình tự, thủ tục phục hồi điểm giấy phép lái xe đối với trường hợp giấy phép lái xe bị trừ hết điểm
> a) Sau khi người có giấy phép lái xe bị trừ hết điểm tham gia kiểm tra nội dung kiến thức pháp luật về trật tự, an toàn giao thông đường bộ và đạt yêu cầu, kết quả kiểm tra được cập nhật vào phần mềm kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ và đồng bộ dữ liệu với Cơ sở dữ liệu về xử lý vi phạm hành chính về trật tự, an toàn giao thông đường bộ, dữ liệu điểm giấy phép lái xe sẽ được phục hồi đủ 12 điểm và cập nhật tự động trong Cơ sở dữ liệu về xử lý vi phạm hành chính về trật tự, an toàn giao thông đường bộ;
> b) Ngay sau khi dữ liệu điểm giấy phép lái xe được phục hồi đủ 12 điểm thì người có thẩm quyền quy định tại điểm b khoản 1 Điều này thông báo cho người được phục hồi điểm giấy phép lái xe biết việc phục hồi điểm;
> c) Việc thông báo phục hồi điểm giấy phép lái xe thực hiện bằng văn bản theo mẫu quy định của Bộ trưởng Bộ Công an và được giao trực tiếp hoặc gửi qua dịch vụ bưu chính hoặc thực hiện thông báo bằng phương thức điện tử thông qua tài khoản của công dân đăng ký trên Cổng …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D51/K3"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-009 · tier A · ND151-2024/D11/K8

Nghị định số 151/2024/NĐ-CP (Quy định chi tiết một số điều và biện pháp thi hành Luật Trật tự, an toàn giao thông đường bộ)

`ND151-2024/D11/K8#2026-07-01` · hiệu lực 2026-07-01 → nay

> Điều 11. Thông tin trong Cơ sở dữ liệu về trật tự, an toàn giao thông đường bộ
> 8. Thông tin về bảo hiểm bắt buộc trách nhiệm dân sự của chủ xe cơ giới, xe máy chuyên dùng:
> a) Thông tin về chủ sở hữu xe cơ giới, xe máy chuyên dùng:
> Đối với cá nhân: họ, tên; ngày, tháng, năm sinh; giới tính; số định danh cá nhân; số điện thoại (nếu có); quốc tịch; nơi thường trú; nơi tạm trú, nơi ở hiện tại, địa chỉ đăng ký xe.
> Đối với tổ chức: tên tổ chức; tên người đại diện hợp pháp; địa chỉ; mã số thuế hoặc quyết định thành lập hoặc số định danh của tổ chức (nếu có); số điện thoại;
> b) Thông tin về xe cơ giới: biển số xe hoặc số khung, số máy, loại xe, trọng tải (đối với xe ô tô), số chỗ ngồi (đối với xe ô tô), mục đích sử dụng xe (đối với xe ô tô), nhãn hiệu, dung tích, màu sơn, năm sản xuất;
> c) Thông tin về doanh nghiệp bảo hiểm: tên, địa chỉ, số điện thoại đường dây nóng;
> d) Mức trách nhiệm bảo hiểm dân sự đối với bên thứ ba và hành khách;
> đ) Trách nhiệm của chủ xe cơ giới, người lái xe khi xảy ra tai nạn;
> e) Thời hạn bảo hiểm, số giấy chứng nhận bảo hiểm, phí bảo hiểm, thời hạn thanh toán phí bảo hiểm, ngày, tháng, năm cấp đơn, nơi cấp đơn, người cấp đơn (nếu có);
> g) Thông tin bồi thường bảo …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["ND151-2024/D11/K8"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-010 · tier A · LUAT35-2024/D50/K2

Luật Đường bộ số 35/2024/QH15

`LUAT35-2024/D50/K2#2024-10-01` · hiệu lực 2024-10-01 → nay

> Điều 50. Phí sử dụng đường cao tốc
> 2. Quản lý, sử dụng các nguồn thu từ phí sử dụng đường cao tốc được quy định như sau:
> a) Cơ quan quản lý đường bộ tổ chức khai thác tài sản nộp số phí thu được vào ngân sách nhà nước theo quy định của pháp luật về phí và lệ phí;
> b) Tổ chức nhận nhượng quyền thu phí, nhượng quyền kinh doanh - quản lý nộp số tiền nhận nhượng quyền vào ngân sách nhà nước; số tiền phí thu được trong thời gian thực hiện hợp đồng chuyển nhượng không phải nộp ngân sách nhà nước, trừ phần doanh thu phải chia sẻ cho Nhà nước theo quy định của pháp luật.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["LUAT35-2024/D50/K2"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-011 · tier A · TT79-2024-BCA/D21/K1

Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)

`TT79-2024-BCA/D21/K1#2025-03-01` · hiệu lực 2025-03-01 → nay

> Điều 21. Thủ tục cấp lại chứng nhận đăng ký xe, biển số xe
> 1. Chủ xe thực hiện dịch vụ công trực tuyến toàn trình đối với trường hợp cấp lại chứng nhận đăng ký xe, cấp lại biển số xe (trừ trường hợp xe đã đăng ký biển 3 số hoặc biển 4 số):
> a) Chủ xe kê khai giấy khai đăng ký xe theo quy định tại Điều 9 Thông tư này, nộp bản chà số máy, số khung của xe qua dịch vụ bưu chính cho cơ quan đăng ký xe;
> b) Sau khi kiểm tra hồ sơ xe đảm bảo hợp lệ, cơ quan đăng ký xe gửi thông báo cho chủ xe để nộp lệ phí đăng ký xe, phí dịch vụ bưu chính trên cổng dịch vụ công để trả kết quả đăng ký xe theo quy định;
> c) Chủ xe nhận chứng nhận đăng ký xe hoặc biển số xe theo quy định từ dịch vụ bưu chính.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["TT79-2024-BCA/D21/K1"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-012 · tier A · ND151-2024/D6/K3

Nghị định số 151/2024/NĐ-CP (Quy định chi tiết một số điều và biện pháp thi hành Luật Trật tự, an toàn giao thông đường bộ)

`ND151-2024/D6/K3#2025-01-01` · hiệu lực 2025-01-01 → 2025-06-30

> Điều 6. Trách nhiệm hướng dẫn kỹ năng lái xe gắn máy an toàn cho học sinh
> 3. Bộ Lao động - Thương binh và Xã hội chủ trì, chỉ đạo cơ quan quản lý cơ sở giáo dục nghề nghiệp chuẩn bị cơ sở vật chất, phương tiện xe gắn máy để phối hợp với lực lượng Cảnh sát giao thông tổ chức hướng dẫn kỹ năng lái xe gắn máy an toàn.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2025-06-30", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["ND151-2024/D6/K3"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-013 · tier A · LUAT36-2024/D52/K3

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D52/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 52. Bảo đảm trật tự, an toàn giao thông đường bộ đối với xe quá khổ giới hạn, xe quá tải trọng, xe bánh xích lưu hành trên đường bộ
> 3. Xe quá khổ giới hạn, xe quá tải trọng, xe bánh xích được cấp giấy phép lưu hành xe trên đường bộ trong các trường hợp sau đây:
> a) Lưu hành xe quá khổ giới hạn quy định tại điểm a và điểm b khoản 1 Điều này không chở hàng hóa, xe có khối lượng bản thân của xe quá tải trọng của đường bộ không chở hàng hóa, xe bánh xích từ nơi sản xuất, ga, cảng và các địa điểm nhập khẩu, sửa chữa, bảo trì đến nơi sử dụng phương tiện và ngược lại hoặc giữa các địa điểm sử dụng phương tiện;
> b) Lưu hành xe quá khổ giới hạn, xe quá tải trọng để chở hàng hóa trên đường bộ trong các trường hợp: phục vụ nhiệm vụ quốc phòng, an ninh; phòng, chống, khắc phục hậu quả thiên tai; thực hiện nhiệm vụ trong trường hợp khẩn cấp; chở hàng siêu trường, siêu trọng khi các phương thức vận chuyển hàng hoá bằng đường sắt, đường thuỷ nội địa, hàng không, hàng hải không phù hợp hoặc phải kết hợp phương thức vận tải đường bộ với phương thức vận tải khác;
> c) Lưu hành xe quá khổ giới hạn cho phép của xe để chở xe ô tô chở người đến 08 chỗ (không kể chỗ của người lái xe), xe ô tô tải và ô …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D52/K3"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-014 · tier A · ND168-2024/D41/K4

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D41/K4#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 41. Phân định thẩm quyền xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ
> 4. Trưởng Công an cấp xã, Trưởng đồn Công an, Trưởng trạm Công an cửa khẩu, khu chế xuất trong phạm vi chức năng, nhiệm vụ được giao có liên quan đến trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ có thẩm quyền xử phạt đối với các hành vi vi phạm quy định tại các điểm, khoản, điều của Nghị định này như sau:
> a) Điểm đ khoản 1; điểm d, điểm đ khoản 2; điểm b, điểm d, điểm đ, điểm e, điểm g khoản 3 Điều 6;
> b) Điểm d, điểm e, điểm g, điểm i khoản 1; điểm a, điểm d, điểm e, điểm g, điểm h, điểm i, điểm k khoản 2; điểm b, điểm c, điểm e, điểm g, điểm k khoản 3; điểm b, điểm d, điểm đ khoản 4 Điều 7;
> c) Khoản 2; điểm b, điểm c khoản 3; điểm c, điểm d, điểm đ, điểm e khoản 4 Điều 8;
> d) Điểm a, điểm b, điểm c, điểm d, điểm đ, điểm e, điểm g, điểm h, điểm i, điểm k, điểm l, điểm m, điểm n, điểm o khoản 1; khoản 2; điểm a, điểm b, điểm c khoản 3; điểm d, điểm đ khoản 4 Điều 9;
> đ) Khoản 1; điểm b, điểm c khoản 2 Điều 10;
> e) Khoản 1, khoản 2 Điều 11;
> g) Khoản 1; khoản 2; khoản 3; khoản 5; điểm c, điểm d khoản 6 Điều 12;
> h) Điều 15;
> i) Khoản 1 Điều 17;
> k) …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D41/K4"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-015 · tier A · LUAT36-2024/D4/K5

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D4/K5#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 4. Chính sách của Nhà nước về trật tự, an toàn giao thông đường bộ
> 5. Cơ quan, tổ chức, cá nhân tham gia phối hợp, cộng tác, hỗ trợ, giúp đỡ cơ quan nhà nước thực hiện nhiệm vụ bảo đảm trật tự, an toàn giao thông đường bộ, có thành tích thì được khen thưởng, bị thiệt hại về tài sản thì được đền bù; người bị tổn hại về danh dự, nhân phẩm thì được khôi phục; người bị thương, bị tổn hại về sức khỏe, tính mạng thì bản thân, gia đình được hưởng chế độ, chính sách theo quy định của pháp luật.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D4/K5"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-016 · tier A · LUAT36-2024/D66/K2

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D66/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 66. Căn cứ dừng phương tiện tham gia giao thông đường bộ để kiểm tra, kiểm soát
> 2. Thực hiện theo mệnh lệnh, kế hoạch tuần tra, kiểm soát của cấp có thẩm quyền để phát hiện hành vi vi phạm pháp luật về trật tự, an toàn giao thông đường bộ mà buộc phải dừng phương tiện để kiểm tra, kiểm soát mới phát hiện được;


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D66/K2"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-017 · tier A · TT65-2024-BCA/D11/K2

Thông tư số 65/2024/TT-BCA (Quy định kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ để được phục hồi điểm giấy phép lái xe)

`TT65-2024-BCA/D11/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 11. Trách nhiệm thi hành
> 2. Giám đốc Công an tỉnh, thành phố trực thuộc trung ương có trách nhiệm:
> a) Định kỳ 06 tháng, 01 năm hoặc đột xuất báo cáo về Bộ Công an (qua Cục Cảnh sát giao thông) kết quả thực hiện kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ thuộc phạm vi quản lý;
> b) Tổ chức kiểm tra lưu động kiến thức pháp luật về trật tự, an toàn giao thông đường bộ khi bảo đảm điều kiện tổ chức kiểm tra quy định tại Điều 5 Thông tư này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["TT65-2024-BCA/D11/K2"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-018 · tier A · ND168-2024/D3/K4

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)

`ND168-2024/D3/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 3. Hình thức xử phạt vi phạm hành chính, biện pháp khắc phục hậu quả; thu hồi giấy phép, chứng chỉ hành nghề
> 4. Thủ tục thi hành biện pháp khắc phục hậu quả buộc nộp lại giấy phép, chứng chỉ hành nghề bị tẩy xóa, sửa chữa làm sai lệch nội dung; thu hồi giấy phép, chứng chỉ hành nghề đã hết giá trị sử dụng hoặc không do cơ quan có thẩm quyền cấp
> a) Cá nhân, tổ chức vi phạm có trách nhiệm thi hành biện pháp khắc phục hậu quả buộc nộp lại giấy phép, chứng chỉ hành nghề bị tẩy xóa, sửa chữa làm sai lệch nội dung gồm: giấy phép lái xe; chứng nhận đăng ký xe; bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe; giấy chứng nhận, tem kiểm định an toàn kỹ thuật và bảo vệ môi trường của phương tiện bị tẩy xóa, sửa chữa làm sai lệch nội dung thực hiện theo quy định tại Điều 85 của Luật Xử lý vi phạm hành chính.
> Người có thẩm quyền ra quyết định thi hành biện pháp khắc phục hậu quả chuyển giấy phép, chứng chỉ hành nghề bị tẩy xóa, sửa chữa làm sai lệch nội dung cho cơ quan, người có thẩm quyền đã cấp giấy phép, …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D3/K4"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-019 · tier A · LUAT35-2024/D65/K2

Luật Đường bộ số 35/2024/QH15

`LUAT35-2024/D65/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 65. Vận tải hành khách, hàng hóa bằng xe thô sơ, xe gắn máy, xe mô tô hai bánh, xe mô tô ba bánh
> 2. Tổ chức, cá nhân cung cấp dịch vụ phần mềm hỗ trợ kết nối vận tải bằng xe thô sơ, xe gắn máy, xe mô tô hai bánh, xe mô tô ba bánh phải chấp hành quy định tại Điều 80 của Luật này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["LUAT35-2024/D65/K2"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-020 · tier A · TT79-2024-BCA/D28/K2

Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)

`TT79-2024-BCA/D28/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 28. Hồ sơ đăng ký, cấp biển số xe trúng đấu giá
> 2. Đối với xe đã đăng ký thuộc quyền sở hữu của tổ chức, cá nhân trúng đấu giá
> a) Giấy khai đăng ký xe;
> b) Chứng nhận đăng ký xe và biển số xe;
> c) Quyết định xác nhận biển số xe trúng đấu giá do Cục Cảnh sát giao thông cấp, còn thời hạn sử dụng; trường hợp quá thời hạn thì phải có thêm quyết định gia hạn thời hạn đăng ký biển số xe trúng đấu giá do Cục Cảnh sát giao thông cấp;
> d) Giấy xác nhận hồ sơ xe của cơ quan đăng ký xe đang quản lý hồ sơ xe (đối với trường hợp cơ quan thực hiện đăng ký, cấp biển số trúng đấu giá khác cơ quan đang quản lý hồ sơ xe).


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["TT79-2024-BCA/D28/K2"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-021 · tier A · ND151-2024/D20/K2

Nghị định số 151/2024/NĐ-CP (Quy định chi tiết một số điều và biện pháp thi hành Luật Trật tự, an toàn giao thông đường bộ)

`ND151-2024/D20/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 20. Hồ sơ đề nghị cấp mới, cấp lại giấy phép sử dụng thiết bị phát tín hiệu của xe ưu tiên
> 2. Đối với xe cứu thương chỉ được cấp giấy phép sử dụng thiết bị phát tín hiệu của xe ưu tiên khi bảo đảm quy định về tiêu chuẩn và sử dụng xe cứu thương theo quy định của Bộ trưởng Bộ Y tế.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["ND151-2024/D20/K2"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-022 · tier A · LUAT35-2024/D39/K2

Luật Đường bộ số 35/2024/QH15

`LUAT35-2024/D39/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 39. Bến xe, bãi đỗ xe, trạm dừng nghỉ, điểm dừng xe, trạm thu phí đường bộ, công trình kiểm soát tải trọng xe trên đường bộ
> 2. Điểm dừng xe được quy định như sau:
> a) Điểm dừng xe trong đô thị và trong các khu dân cư, cơ quan, tổ chức nhằm đáp ứng nhu cầu dừng xe phục vụ giao thông đô thị và các khu vực, địa điểm này;
> b) Điểm dừng xe trong phạm vi đường bộ được bố trí tại một số vị trí nhất định dành cho xe ô tô để đón, trả khách;
> c) Đối với các đường ngoài đô thị được đầu tư, xây dựng mới hoặc nâng cấp, mở rộng, cải tạo thì điểm dừng xe phải được xây dựng ngoài phạm vi đường bộ.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["LUAT35-2024/D39/K2"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-023 · tier A · TT79-2024-BCA/D24/K4

Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)

`TT79-2024-BCA/D24/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 24. Thời hạn có giá trị của chứng nhận đăng ký xe tạm thời
> 4. Khi thực hiện gia hạn, chủ xe kê khai giấy khai đăng ký xe tạm thời trên cổng dịch vụ công hoặc trực tiếp tại cơ quan đăng ký xe.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["TT79-2024-BCA/D24/K4"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-024 · tier A · LUAT35-2024/D48/K2

Luật Đường bộ số 35/2024/QH15

`LUAT35-2024/D48/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 48. Mở rộng, nâng cấp đường cao tốc hoặc đường bộ đang khai thác nâng cấp thành đường cao tốc
> 2. Đối với dự án đã được đầu tư theo phương thức đối tác công tư đang trong giai đoạn thực hiện hợp đồng dự án, cơ quan ký kết hợp đồng thỏa thuận với nhà đầu tư về việc mở rộng, nâng cấp đường cao tốc hoặc đường bộ đang khai thác nâng cấp thành đường cao tốc theo một trong các phương án sau đây:
> a) Nhà đầu tư đề xuất điều chỉnh dự án đầu tư để mở rộng, nâng cấp;
> b) Nhà nước tổ chức lập dự án đầu tư mở rộng, nâng cấp theo phương thức đối tác công tư hoặc đầu tư công, trừ trường hợp trùng lặp với dự án đầu tư theo phương thức đối tác công tư đã có quyết định chủ trương đầu tư hoặc quyết định dự án hoặc trùng lặp với dự án đầu tư công đã có quyết định chủ trương đầu tư hoặc đã có quyết định đầu tư theo quy định của pháp luật về đầu tư theo phương thức đối tác công tư, pháp luật về đầu tư công.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["LUAT35-2024/D48/K2"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-025 · tier A · TT65-2024-BCA/D6/K1

Thông tư số 65/2024/TT-BCA (Quy định kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ để được phục hồi điểm giấy phép lái xe)

`TT65-2024-BCA/D6/K1#2025-03-01` · hiệu lực 2025-03-01 → nay

> Điều 6. Nội dung, phương pháp, thời gian, kết cấu bài kiểm tra, kết quả kiểm tra đạt yêu cầu
> 1. Nội dung kiểm tra, bao gồm:
> a) Kiểm tra lý thuyết kiến thức pháp luật về trật tự, an toàn giao thông đường bộ được thực hiện theo bộ câu hỏi lý thuyết dùng cho sát hạch, cấp giấy phép lái xe cơ giới đường bộ do Cục Cảnh sát giao thông xây dựng và ban hành (sau đây viết gọn là kiểm tra lý thuyết kiến thức pháp luật);
> b) Kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ theo mô phỏng các tình huống giao thông trên máy tính do Bộ Công an phê duyệt, ban hành (sau đây viết gọn là kiểm tra kiến thức pháp luật theo mô phỏng).


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["TT65-2024-BCA/D6/K1"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-026 · tier A · LUAT36-2024/D65/K5

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D65/K5#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 65. Hoạt động tuần tra, kiểm soát về trật tự, an toàn giao thông đường bộ
> 5. Quyền hạn của Cảnh sát giao thông khi thực hiện tuần tra, kiểm soát bao gồm:
> a) Dừng phương tiện tham gia giao thông đường bộ theo quy định tại Điều 66 của Luật này để kiểm tra việc chấp hành các quy định về quy tắc giao thông đường bộ; điều kiện của phương tiện tham gia giao thông đường bộ; điều kiện của người điều khiển phương tiện tham gia giao thông đường bộ; các quy định về bảo đảm trật tự, an toàn giao thông đường bộ theo quy định của Luật này và quy định khác của pháp luật có liên quan;
> b) Xử lý vi phạm hành chính về trật tự, an toàn giao thông đường bộ và vi phạm pháp luật khác theo quy định của pháp luật;
> c) Huy động người, phương tiện, thiết bị dân sự trong trường hợp cấp bách; di chuyển phương tiện vi phạm dừng, đỗ trên đường bộ gây cản trở, ùn tắc giao thông hoặc nguy cơ dẫn đến tai nạn giao thông đường bộ theo quy định tại Điều 68 và Điều 69 của Luật này;
> d) Vận hành, sử dụng hệ thống, phương tiện, thiết bị, dữ liệu theo quy định tại các khoản 1, 2, 3 và 4 Điều 67 của Luật này và vũ khí, công cụ hỗ trợ theo quy định tại Điều 70 của Luật này;
> đ) Quyền hạn khác theo quy định của Luật Công …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D65/K5"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-027 · tier A · LUAT36-2024/D6/K2

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D6/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 6. Giáo dục kiến thức pháp luật về trật tự, an toàn giao thông đường bộ
> 2. Lực lượng Cảnh sát giao thông có trách nhiệm chủ trì, phối hợp với cơ quan quản lý trường trung học phổ thông, cơ sở giáo dục nghề nghiệp tổ chức hướng dẫn kỹ năng lái xe gắn máy an toàn cho học sinh tại cơ sở giáo dục đó.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D6/K2"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-028 · tier A · TT79-2024-BCA/D39/K1

Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)

`TT79-2024-BCA/D39/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 39. Điều khoản chuyển tiếp
> 1. Đối với xe đã đăng ký biển 5 số trước ngày Thông tư này có hiệu lực thi hành mà chưa làm thủ tục thu hồi thì số biển số đó được xác định là biển số định danh của chủ xe, trừ biển số xe có ký hiệu “MK”, “TĐ”, “LD”, “DA”, “MĐ”, “R”, “CT”, “LB”, “CD”.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["TT79-2024-BCA/D39/K1"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-029 · tier A · TT12-2025-BCA/D32/K1

Thông tư số 12/2025/TT-BCA (Quy định về sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế)

`TT12-2025-BCA/D32/K1#2025-03-01` · hiệu lực 2025-03-01 → nay

> Điều 32. Thời gian lưu trữ dữ liệu trên hệ thống thông tin
> 1. Thời gian lưu trữ dữ liệu về sát hạch lái xe tại trung tâm sát hạch lái xe tối thiểu là 05 năm.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["TT12-2025-BCA/D32/K1"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-030 · tier A · ND151-2024/D32/K5

Nghị định số 151/2024/NĐ-CP (Quy định chi tiết một số điều và biện pháp thi hành Luật Trật tự, an toàn giao thông đường bộ)

`ND151-2024/D32/K5#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 32. Xe cơ giới nước ngoài và người nước ngoài điều khiển phương tiện tham gia giao thông tại Việt Nam
> 5. Điều kiện đối với người nước ngoài điều khiển xe cơ giới nước ngoài tham gia giao thông tại Việt Nam:
> a) Có hộ chiếu, thị thực hoặc giấy tờ có giá trị đi lại quốc tế, giấy tờ có giá trị cư trú tại Việt Nam, trừ trường hợp được miễn thị thực và không thuộc trường hợp chưa cho nhập cảnh theo quy định của pháp luật về nhập cảnh, xuất cảnh, quá cảnh, cư trú của người nước ngoài tại Việt Nam.
> Trường hợp người nước ngoài nhập cảnh theo diện đơn phương miễn thị thực thì hộ chiếu phải còn thời hạn sử dụng ít nhất 06 tháng; người nước ngoài sử dụng thị thực điện tử phải nhập cảnh qua các cửa khẩu quốc tế do Chính phủ quyết định theo quy định của pháp luật về nhập cảnh, xuất cảnh, quá cảnh, cư trú của người nước ngoài tại Việt Nam;
> b) Có giấy phép lái xe phù hợp với loại xe được phép điều khiển, có giá trị sử dụng trong phạm vi lãnh thổ Việt Nam và còn hiệu lực.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["ND151-2024/D32/K5"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-031 · tier A · LUAT36-2024/D46/K5

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D46/K5#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 46. Bảo đảm trật tự, an toàn giao thông đường bộ đối với xe ô tô chở trẻ em mầm non, học sinh
> 5. Cơ sở giáo dục phải xây dựng quy trình bảo đảm an toàn khi đưa đón trẻ em mầm non, học sinh; hướng dẫn cho lái xe và người quản lý trẻ em mầm non, học sinh nắm vững và thực hiện đúng quy trình; chịu trách nhiệm bảo đảm trật tự, an toàn giao thông đường bộ khi tổ chức đưa đón trẻ em mầm non, học sinh của cơ sở giáo dục đó.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D46/K5"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-032 · tier A · LUAT35-2024/D47/K5

Luật Đường bộ số 35/2024/QH15

`LUAT35-2024/D47/K5#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 47. Đầu tư, xây dựng, phát triển đường cao tốc
> 5. Cấp quyết định đầu tư được phê duyệt, phê duyệt điều chỉnh tiểu dự án, dự án thành phần trong trường hợp kinh phí các tiểu dự án, dự án thành phần có sự thay đổi so với sơ bộ tổng mức đầu tư của tiểu dự án, dự án thành phần được duyệt nhưng không vượt sơ bộ tổng mức đầu tư của toàn bộ dự án đã được quyết định chủ trương đầu tư.
> Trường hợp quyết định tách dự án thành các tiểu dự án, dự án thành phần, cấp quyết định chủ trương đầu tư quyết định việc giao cho một cơ quan chủ trì chịu trách nhiệm tổ chức thực hiện dự án bảo đảm tính tổng thể, đồng bộ toàn dự án; chịu trách nhiệm rà soát, điều hòa, cân đối và thống nhất điều chỉnh tổng mức đầu tư giữa các tiểu dự án, dự án thành phần, bảo đảm không vượt sơ bộ tổng mức đầu tư của toàn bộ dự án đã được quyết định chủ trương đầu tư.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["LUAT35-2024/D47/K5"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-033 · tier A · LUAT35-2024/D29/K2

Luật Đường bộ số 35/2024/QH15

`LUAT35-2024/D29/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 29. Thẩm tra, thẩm định an toàn giao thông đường bộ
> 2. Thẩm tra an toàn giao thông đường bộ là việc tổ chức kinh doanh dịch vụ thẩm tra an toàn giao thông nghiên cứu, phân tích thiết kế cơ sở, thiết kế triển khai sau thiết kế cơ sở, báo cáo kinh tế - kỹ thuật xây dựng công trình, hồ sơ hoàn thành công trình, hồ sơ quản lý tuyến đường, nguyên nhân các vụ tai nạn giao thông và tiến hành kiểm tra hiện trường để phát hiện các khả năng tiềm ẩn tai nạn giao thông hoặc đánh giá nguyên nhân gây tai nạn giao thông để đề xuất giải pháp khắc phục nhằm bảo đảm giao thông trên tuyến thông suốt, an toàn.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["LUAT35-2024/D29/K2"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-034 · tier A · TT79-2024-BCA/D15/K1

Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)

`TT79-2024-BCA/D15/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 15. Cấp chứng nhận đăng ký xe, biển số xe trong trường hợp thay đổi chủ xe (sau đây viết gọn là đăng ký sang tên xe)
> 1. Khi chuyển quyền sở hữu xe, chủ xe phải làm thủ tục thu hồi tại cơ quan đăng ký xe nơi chủ xe có trụ sở, cư trú theo quy định tại Điều 4 Thông tư này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["TT79-2024-BCA/D15/K1"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-035 · tier A · TT12-2025-BCA/D16/K3

Thông tư số 12/2025/TT-BCA (Quy định về sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế)

`TT12-2025-BCA/D16/K3#2025-03-01` · hiệu lực 2025-03-01 → nay

> Điều 16. Hồ sơ dự sát hạch lái xe
> 3. Hồ sơ đề nghị sát hạch cấp giấy phép lái xe do quá thời hạn sử dụng, do giấy phép lái xe mất và quá thời hạn sử dụng của cá nhân nộp tại Phòng Cảnh sát giao thông
> a) Đề nghị sát hạch để cấp giấy phép lái xe theo quy định tại Phụ lục I ban hành kèm theo Thông tư này;
> b) Bản sao hoặc bản sao điện tử được chứng thực từ bản chính hoặc bản sao điện tử được cấp từ sổ gốc một trong các giấy tờ sau: thẻ tạm trú, thẻ thường trú, chứng minh thư ngoại giao, chứng minh thư công vụ (đối với người nước ngoài);
> c) Giấy phép lái xe quân sự do Bộ Quốc phòng cấp hoặc xác nhận của cơ quan đã cấp đối với trường hợp mất giấy phép lái xe (đối với giấy phép lái xe quân sự do Bộ Quốc phòng cấp);
> d) Giấy khám sức khoẻ của người lái xe do cơ sở khám bệnh, chữa bệnh đủ tiêu chuẩn theo quy định của pháp luật về khám bệnh, chữa bệnh cấp còn hiệu lực;
> đ) Bản sao giấy tờ chứng minh thôi không còn phục vụ trong lực lượng Quân đội nhân dân, Công an nhân dân (đối với trường hợp giấy phép lái xe quân sự do Bộ Quốc phòng cấp, giấy phép lái xe trong Công an nhân dân).


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["TT12-2025-BCA/D16/K3"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-036 · tier A · TT14-2025-BXD/D21/K3

Thông tư số 14/2025/TT-BXD (Quy định về đào tạo lái xe; bồi dưỡng, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ)

`TT14-2025-BXD/D21/K3#2025-09-01` · hiệu lực 2025-09-01 → nay

> Điều 21. Lưu trữ hồ sơ kết quả kiểm tra
> 3. Thời gian lưu trữ tài liệu:
> a) Không thời hạn đối với Sổ cấp chứng chỉ;
> b) 02 năm đối với tài liệu quy định tại điểm a, điểm b, điểm c khoản 1 Điều này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["TT14-2025-BXD/D21/K3"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-037 · tier A · LUAT36-2024/D7/K1

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D7/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 7. Cơ sở dữ liệu về trật tự, an toàn giao thông đường bộ
> 1. Cơ sở dữ liệu về trật tự, an toàn giao thông đường bộ bao gồm:
> a) Cơ sở dữ liệu về đăng ký, quản lý xe cơ giới, xe máy chuyên dùng;
> b) Cơ sở dữ liệu về đăng kiểm xe cơ giới, xe máy chuyên dùng;
> c) Cơ sở dữ liệu về đào tạo, sát hạch, cấp giấy phép lái xe, chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ;
> d) Cơ sở dữ liệu về người điều khiển xe cơ giới, xe máy chuyên dùng;
> đ) Cơ sở dữ liệu về bảo hiểm của chủ xe cơ giới, xe máy chuyên dùng;
> e) Cơ sở dữ liệu về xử lý vi phạm hành chính về trật tự, an toàn giao thông đường bộ;
> g) Cơ sở dữ liệu về tai nạn giao thông đường bộ;
> h) Cơ sở dữ liệu về hành trình của phương tiện giao thông đường bộ, hình ảnh người lái xe theo quy định của Luật này;
> i) Cơ sở dữ liệu về quản lý thời gian điều khiển phương tiện của người lái xe theo quy định của Luật này;
> k) Cơ sở dữ liệu khác liên quan đến công tác bảo đảm trật tự, an toàn giao thông đường bộ.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D7/K1"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-038 · tier A · ND151-2024/D24/K3

Nghị định số 151/2024/NĐ-CP (Quy định chi tiết một số điều và biện pháp thi hành Luật Trật tự, an toàn giao thông đường bộ)

`ND151-2024/D24/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 24. Trách nhiệm quản lý, sử dụng thiết bị phát tín hiệu của xe ưu tiên
> 3. Cơ quan, tổ chức được cấp giấy phép sử dụng thiết bị phát tín hiệu của xe ưu tiên định kỳ hằng năm (trước ngày 15 tháng 12) thống kê gửi cơ quan có thẩm quyền đã cấp giấy phép sử dụng trước đó về thực trạng quản lý, sử dụng thiết bị phát tín hiệu của xe ưu tiên theo Mẫu số 02d Phụ lục II kèm theo Nghị định này để quản lý.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["ND151-2024/D24/K3"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-039 · tier A · TT79-2024-BCA/D37/K1

Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)

`TT79-2024-BCA/D37/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 37. Quy định về biển số xe
> 1. Biển số xe thực hiện theo Quy chuẩn kỹ thuật quốc gia do Bộ Công an ban hành. Đối với biển số xe đăng ký tạm thời quy định tại Phụ lục số 02 ban hành kèm theo Thông tư này được in trên giấy.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["TT79-2024-BCA/D37/K1"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-040 · tier A · LUAT36-2024/D44/K5

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D44/K5#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 44. Bảo đảm trật tự, an toàn giao thông đường bộ đối với phương tiện vận tải đường bộ trong đô thị
> 5. Ủy ban nhân dân cấp tỉnh quy định về hoạt động vận tải đường bộ trong đô thị và tỷ lệ phương tiện vận chuyển hành khách công cộng có thiết bị hỗ trợ cho người khuyết tật trong đô thị.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D44/K5"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-041 · tier A · ND151-2024/D2

Nghị định số 151/2024/NĐ-CP (Quy định chi tiết một số điều và biện pháp thi hành Luật Trật tự, an toàn giao thông đường bộ)

`ND151-2024/D2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 2. Đối tượng áp dụng
> Nghị định này áp dụng đối với cơ quan, tổ chức, cá nhân trong nước và nước ngoài liên quan đến trật tự, an toàn giao thông đường bộ trên lãnh thổ nước Cộng hòa xã hội chủ nghĩa Việt Nam.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["ND151-2024/D2"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-042 · tier A · TT65-2024-BCA/D5/K2

Thông tư số 65/2024/TT-BCA (Quy định kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ để được phục hồi điểm giấy phép lái xe)

`TT65-2024-BCA/D5/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 5. Bảo đảm điều kiện tổ chức kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ
> 2. Cán bộ được giao nhiệm vụ kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ phải có giấy phép lái xe mô tô hạng A và giấy phép lái xe ô tô, được Cục Cảnh sát giao thông tổ chức tập huấn, cấp thẻ Sát hạch viên.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["TT65-2024-BCA/D5/K2"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-043 · tier A · TT12-2025-BCA/D19/K2

Thông tư số 12/2025/TT-BCA (Quy định về sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế)

`TT12-2025-BCA/D19/K2#2025-03-01` · hiệu lực 2025-03-01 → nay

> Điều 19. Cấp giấy phép lái xe
> 2. Việc cấp giấy phép lái xe cho người có giấy phép lái xe ô tô các hạng mà quá thời hạn sử dụng; mất giấy phép lái xe ô tô và giấy phép lái xe đó quá thời hạn sử dụng bao gồm cả người có giấy phép lái xe quân sự do Bộ Quốc phòng cấp, giấy phép lái xe trong Công an nhân dân khi thôi không còn làm nhiệm vụ quốc phòng, an ninh thực hiện như sau:
> a) Người có giấy phép lái xe thuộc các trường hợp trên phải có tên trong hệ thống thông tin giấy phép lái xe tại Cục Cảnh sát giao thông hoặc bảng kê danh sách cấp giấy phép lái xe (sổ quản lý), trường hợp giấy phép lái xe quân sự do Bộ Quốc phòng cấp mất giấy phép lái xe phải có xác nhận của cơ quan đã cấp thì phải dự sát hạch các nội dung sau đây:
> Trường hợp giấy phép lái xe quá thời hạn sử dụng dưới 01 tháng kể từ ngày hết hạn mà người có giấy phép lái xe không thể thực hiện được thủ tục đổi giấy phép lái xe do ốm đau, thiên tai, hỏa hoạn, dịch bệnh thì người đó không phải sát hạch lý thuyết để cấp giấy phép lái xe.
> Trường hợp giấy phép lái xe quá thời hạn sử dụng dưới 01 năm kể từ ngày hết hạn thì phải sát hạch lý thuyết theo quy định tại điểm a khoản 1 Điều 4 Thông tư này để cấp giấy phép lái xe.
> Trường hợp …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["TT12-2025-BCA/D19/K2"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-044 · tier A · LUAT36-2024/D61/K2

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D61/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 61. Sát hạch lái xe
> 2. Nội dung sát hạch lái xe phải phù hợp với hạng giấy phép lái xe và chương trình đào tạo lái xe.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D61/K2"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-045 · tier A · TT14-2025-BXD/D30/K2

Thông tư số 14/2025/TT-BXD (Quy định về đào tạo lái xe; bồi dưỡng, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ)

`TT14-2025-BXD/D30/K2#2026-07-01` · hiệu lực 2026-07-01 → nay

> Điều 30. Cơ sở đào tạo lái xe
> 2. Đối với công tác quản lý hệ thống thông tin:
> a) Đầu tư, bảo trì, nâng cấp Hệ thống thông tin quản lý, giám sát đào tạo lái xe tại cơ sở đào tạo lái xe; tiếp nhận, tổ chức thực hiện phần mềm ứng dụng phục vụ công tác quản lý, giám sát đào tạo lái xe tại cơ sở đào tạo lái xe do Cục Đường bộ Việt Nam chuyển giao và thực hiện truyền đầy đủ dữ liệu quy định tại các điểm a, điểm b, điểm g và điểm h khoản 1 Điều 25 về Sở Xây dựng;
> b) Vận hành Hệ thống thông tin quản lý, giám sát đào tạo lái xe tại cơ sở đào tạo lái xe theo quy định;
> c) Tạo lập, đối chiếu, chịu trách nhiệm về tính chính xác của thông tin học viên, quá trình đào tạo, kết quả đào tạo, báo cáo đăng ký khóa đào tạo lái xe theo quy định;
> d) Lưu trữ đầy đủ các thông tin theo quy định tại khoản 1 Điều 27 Thông tư này và quy định của pháp luật về lưu trữ;
> đ) Ban hành quy chế vận hành và bảo đảm an toàn, an ninh thông tin; quy chế sử dụng tài khoản và khai thác dữ liệu đối với hệ thống thông tin của cơ sở đào tạo và các hệ thống thông tin được chia sẻ theo các quy định của pháp luật về công nghệ thông tin và an toàn thông tin mạng;
> e) Cung cấp dữ liệu trên Hệ thống thông tin quản lý, giám sát đào …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["TT14-2025-BXD/D30/K2"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-046 · tier A · LUAT36-2024/D83/K3

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15

`LUAT36-2024/D83/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 83. Điều tra, giải quyết tai nạn giao thông đường bộ
> 3. Kết luận vụ tai nạn giao thông đường bộ phải xác định diễn biến, hậu quả thiệt hại, nguyên nhân, lỗi và điều kiện liên quan trực tiếp đến vụ tai nạn giao thông đường bộ; đề xuất xử lý vụ tai nạn giao thông đường bộ; kiến nghị cơ quan, tổ chức, cá nhân khắc phục khi phát hiện sơ hở, thiếu sót nhằm bảo đảm trật tự, an toàn giao thông đường bộ.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D83/K3"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-047 · tier A · TT79-2024-BCA/D33/K14

Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)

`TT79-2024-BCA/D33/K14#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 33. Giải quyết một số trường hợp khi đăng ký, cấp biển số xe
> 14. Đăng ký xe có nguồn gốc bị tịch thu theo quy định của pháp luật
> a) Đối với xe đã đăng ký bị tịch thu thì khi đăng ký không phải làm thủ tục thu hồi nhưng sau khi giải quyết đăng ký xe tịch thu, cơ quan đăng ký xe gửi thông báo cho cơ quan quản lý xe đó biết để hủy hồ sơ;
> b) Trường hợp quyết định tịch thu không ghi đặc điểm xe thì phải có biên bản tịch thu do người có thẩm quyền tịch thu ký, trong đó phải ghi đầy đủ các đặc điểm xe theo quy định tại điểm a khoản 3 Điều 11 Thông tư này;
> c) Trường hợp quyết định tịch thu hoặc biên bản tịch thu không ghi đầy đủ đặc điểm xe; xe không nguyên chiếc, tổng thành máy, tổng thành khung không cùng kiểu loại thì không giải quyết đăng ký xe.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["TT79-2024-BCA/D33/K14"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-048 · tier A · ND151-2024/D22/K4

Nghị định số 151/2024/NĐ-CP (Quy định chi tiết một số điều và biện pháp thi hành Luật Trật tự, an toàn giao thông đường bộ)

`ND151-2024/D22/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 22. Giấy phép sử dụng thiết bị phát tín hiệu của xe ưu tiên
> 4. Cơ quan, tổ chức đã được cấp giấy phép sử dụng thiết bị phát tín hiệu của xe ưu tiên có trách nhiệm giao nộp giấy phép thuộc trường hợp bị thu hồi quy định tại khoản 3 Điều này cho cơ quan có thẩm quyền đã cấp trước đó để thu hồi.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["ND151-2024/D22/K4"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-049 · tier A · LUAT35-2024/D38/K2

Luật Đường bộ số 35/2024/QH15

`LUAT35-2024/D38/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 38. Phòng, chống, khắc phục hậu quả thiên tai trong lĩnh vực đường bộ
> 2. Việc thực hiện phòng, chống, khắc phục hậu quả thiên tai và tìm kiếm cứu nạn đối với các tuyến đường đã đưa vào khai thác, sử dụng thực hiện theo quy định của pháp luật về phòng, chống thiên tai, quy định khác của pháp luật có liên quan và các quy định sau đây:
> a) Bộ Giao thông vận tải, Ủy ban nhân dân các cấp tổ chức thực hiện công tác phòng, chống, khắc phục hậu quả thiên tai và tìm kiếm cứu nạn đối với đường bộ thuộc phạm vi quản lý;
> b) Người quản lý, sử dụng đường bộ có trách nhiệm thực hiện phòng, chống, khắc phục hậu quả thiên tai đối với đường bộ được giao quản lý, tham gia công tác tìm kiếm cứu nạn; sửa chữa, khắc phục ngay hư hỏng công trình đường bộ đối với các trường hợp không bảo đảm an toàn cho người, phương tiện tham gia giao thông đường bộ; khắc phục nguy cơ sập đổ công trình đường bộ, công trình liền kề; tham gia công tác cứu nạn, cứu hộ;
> c) Cơ quan, tổ chức, cá nhân có liên quan tham gia phòng, chống, khắc phục hậu quả thiên tai và tìm kiếm cứu nạn.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["LUAT35-2024/D38/K2"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-050 · tier A · TT79-2024-BCA/D30/K2

Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)

`TT79-2024-BCA/D30/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 30. Quản lý biển số xe trúng đấu giá, sau khi đăng ký xe
> 2. Khi chủ xe làm thủ tục thu hồi đăng ký, biển số trúng đấu giá (trừ trường hợp chuyển quyền sở hữu xe kèm theo biển số trúng đấu giá) thì số biển số trúng đấu giá được cơ quan đăng ký xe giữ lại và cấp khi chủ xe đăng ký xe khác (chưa có biển số) thuộc sở hữu của mình.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "A", "answer": "", "gold_units": ["TT79-2024-BCA/D30/K2"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-051 · tier B · ND158-2024/D23/K11

Nghị định số 158/2024/NĐ-CP (Quy định về hoạt động vận tải đường bộ)

`ND158-2024/D23/K11#2026-08-10` · hiệu lực 2026-08-10 → nay

> Điều 23. Quy định về quản lý sử dụng, cấp, cấp lại và thu hồi phù hiệu
> 11. Sở Xây dựng
> a) Ban hành quyết định thu hồi phù hiệu do cơ quan mình cấp đối với đơn vị kinh doanh vận tải bị thu hồi phù hiệu theo quy định tại khoản 10 Điều này, điểm d khoản 7 Điều 21 của Nghị định này;
> b) Gửi quyết định thu hồi phù hiệu cho đơn vị kinh doanh vận tải. Trong thời gian 02 ngày kể từ ngày ban hành quyết định, Sở Xây dựng đăng tải quyết định thu hồi trên Trang thông tin điện tử của Sở; cập nhật trạng thái các phù hiệu bị thu hồi vào Cơ sở dữ liệu cấp phép hoạt động vận tải.
> Từ ngày 15 tháng 9 năm 2026, thực hiện gửi quyết định thu hồi phù hiệu đến đơn vị kinh doanh vận tải theo hình thức trực tuyến;
> c) Khi cơ quan cấp phù hiệu ban hành quyết định thu hồi, trong thời hạn 10 ngày kể từ ngày ký, đơn vị kinh doanh vận tải phải dừng hoạt động kinh doanh vận tải đối với xe ô tô, xe bốn bánh có gắn động cơ bị thu hồi;
> d) Chưa giải quyết cấp mới, cấp lại phù hiệu đối với đơn vị kinh doanh vận tải vi phạm quy định bị thu hồi phù hiệu nhưng không chấp hành quyết định thu hồi phù hiệu; sau khi đơn vị kinh doanh vận tải chấp hành xong quyết định thu hồi phù hiệu, cơ quan cấp phù hiệu thực hiện giải quyết …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "B", "answer": "", "gold_units": ["ND158-2024/D23/K11"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-052 · tier B · ND165-2024/D2

Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ)

`ND165-2024/D2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 2. Đối tượng áp dụng
> Nghị định này áp dụng đối với cơ quan, tổ chức, cá nhân liên quan đến hoạt động quy hoạch, đầu tư, xây dựng, quản lý, vận hành, khai thác, sử dụng, bảo trì, bảo vệ kết cấu hạ tầng đường bộ, thẩm tra, thẩm định an toàn giao thông đường bộ, cơ sở dữ liệu đường bộ và giao thông thông minh.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "B", "answer": "", "gold_units": ["ND165-2024/D2"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-053 · tier B · TT73-2024-BCA/D5/K3

Thông tư số 73/2024/TT-BCA (Quy định công tác tuần tra, kiểm soát, xử lý vi phạm pháp luật về trật tự, an toàn giao thông đường bộ của Cảnh sát giao thông)

`TT73-2024-BCA/D5/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 5. Kiểm soát thông qua hệ thống, phương tiện, thiết bị, cơ sở dữ liệu về trật tự, an toàn giao thông đường bộ
> 3. Kiểm soát thông qua tiếp nhận dữ liệu thu thập được từ công trình kiểm soát tải trọng xe
> a) Đơn vị Cảnh sát giao thông theo tuyến, địa bàn được phân công tuần tra, kiểm soát, có trách nhiệm phối hợp tiếp nhận dữ liệu thu thập từ công trình kiểm soát tải trọng xe được lắp đặt trên tuyến, địa bàn theo quy định của Luật Đường bộ, Luật Trật tự, an toàn giao thông đường bộ để kiểm soát, phát hiện và xử lý các hành vi vi phạm pháp luật về trật tự, an toàn giao thông đường bộ, tải trọng xe, các hành vi vi phạm pháp luật khác;
> b) Kết quả, dữ liệu thu thập được từ công trình kiểm soát tải trọng xe để phát hiện, xử lý vi phạm tuân thủ theo quy định của pháp luật xử lý vi phạm hành chính, Nghị định số 135/2021/NĐ-CP và quy định khác của pháp luật có liên quan;
> c) Trình tự phát hiện, xử lý kết quả thu thập được từ công trình kiểm soát tải trọng xe được thực hiện theo quy định tại Điều 15 và Điều 26 Thông tư này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "B", "answer": "", "gold_units": ["TT73-2024-BCA/D5/K3"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-054 · tier B · TT69-2024-BCA/D8/K2

Thông tư số 69/2024/TT-BCA (Quy định về chỉ huy, điều khiển giao thông đường bộ của Cảnh sát giao thông)

`TT69-2024-BCA/D8/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 8. Phân công, phân cấp trong công tác chỉ huy, điều khiển giao thông đường bộ
> 2. Cục Cảnh sát giao thông tổ chức thực hiện công tác chỉ huy, điều khiển giao thông đường bộ trên các tuyến cao tốc được giao quản lý; chỉ đạo triển khai công tác chỉ huy, điều khiển giao thông đường bộ, phối hợp phân luồng giao thông tại các tuyến giao thông đường bộ trên phạm vi toàn quốc khi xảy ra các tình huống giao thông phức tạp có liên quan đến nhiều địa phương hoặc yêu cầu khác về bảo đảm an ninh, trật tự.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "B", "answer": "", "gold_units": ["TT69-2024-BCA/D8/K2"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-055 · tier B · ND165-2024/D4/K7

Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ)

`ND165-2024/D4/K7#2026-07-01` · hiệu lực 2026-07-01 → nay

> Điều 4. Phân cấp quản lý quốc lộ
> 7. Quốc lộ phân cấp cho Ủy ban nhân dân cấp tỉnh quản lý phải thực hiện điều chuyển tài sản kết cấu hạ tầng đường bộ theo quy định của pháp luật về quản lý, sử dụng tài sản công.
> Đối với trường hợp quy định tại khoản 6 Điều này, việc điều chuyển tài sản kết cấu hạ tầng đường bộ từ Ủy ban nhân dân cấp tỉnh về Bộ Xây dựng để quản lý được thực hiện sau khi Bộ Xây dựng có quyết định tiếp nhận lại quốc lộ đã phân cấp.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "B", "answer": "", "gold_units": ["ND165-2024/D4/K7"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-056 · tier B · ND165-2024/D24/K3

Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ)

`ND165-2024/D24/K3#2026-07-01` · hiệu lực 2026-07-01 → nay

> Điều 24. Tổ chức giao thông đường bộ trong giai đoạn quản lý, vận hành, khai thác, sử dụng công trình đường bộ
> 3. Cục Đường bộ Việt Nam, Sở Xây dựng, Ủy ban nhân dân cấp xã có trách nhiệm:
> a) Tổ chức thực hiện các quy định tại khoản 1 Điều này đối với đường bộ được giao quản lý;
> b) Phối hợp, lấy ý kiến của Cơ quan Cảnh sát giao thông được giao điều khiển giao thông đường bộ đối với các trường hợp xử lý các bất cập về tổ chức giao thông, các vị trí ùn tắc giao thông đối với đường cao tốc, đường cấp I, cấp II, đường phố chính đô thị, cầu và hầm đường bộ cấp đặc biệt, cấp I, cấp II và các trường hợp cần thiết;
> c) Thực hiện phương án tổ chức giao thông đường cao tốc đã được phê duyệt;
> d) Hướng dẫn, kiểm tra người quản lý, sử dụng đường bộ thực hiện quy định tại khoản 4 Điều này; yêu cầu khắc phục tồn tại về tổ chức giao thông; xử lý hoặc kiến nghị cấp có thẩm quyền xử lý vi phạm về tổ chức giao thông.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "B", "answer": "", "gold_units": ["ND165-2024/D24/K3"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-057 · tier B · ND158-2024/D70/K1

Nghị định số 158/2024/NĐ-CP (Quy định về hoạt động vận tải đường bộ)

`ND158-2024/D70/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 70. Bộ Tài chính
> 1. Hướng dẫn đơn vị cung cấp phần mềm, đơn vị kinh doanh vận tải để thực hiện hợp đồng điện tử đối với việc cung cấp thông tin điện tử bảo đảm quản lý chặt chẽ và thực hiện đầy đủ nghĩa vụ thuế.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "B", "answer": "", "gold_units": ["ND158-2024/D70/K1"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-058 · tier B · ND158-2024/D49/K3

Nghị định số 158/2024/NĐ-CP (Quy định về hoạt động vận tải đường bộ)

`ND158-2024/D49/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 49. Gia hạn thời gian lưu hành tại Việt Nam cho phương tiện của Trung Quốc
> 3. Thành phần hồ sơ
> a) Giấy đề nghị gia hạn thời gian lưu hành của phương tiện tại Việt Nam theo Mẫu số 12 Phụ lục X kèm theo Nghị định này;
> b) Giấy phép vận tải đường bộ quốc tế giữa Việt Nam và Trung Quốc (bản chính).


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "B", "answer": "", "gold_units": ["ND158-2024/D49/K3"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-059 · tier B · ND158-2024/D47/K1

Nghị định số 158/2024/NĐ-CP (Quy định về hoạt động vận tải đường bộ)

`ND158-2024/D47/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 47. Cấp Giấy phép vận tải đường bộ quốc tế giữa Việt Nam và Trung Quốc loại D cho phương tiện của Trung Quốc
> 1. Giấy phép vận tải loại D do cơ quan quản lý có thẩm quyền của Việt Nam cấp cho phương tiện của Trung Quốc trên cơ sở Giấy giới thiệu của cơ quan có thẩm quyền phía Trung Quốc.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "B", "answer": "", "gold_units": ["ND158-2024/D47/K1"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-060 · tier B · ND158-2024/D54/K1

Nghị định số 158/2024/NĐ-CP (Quy định về hoạt động vận tải đường bộ)

`ND158-2024/D54/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 54. Thu hồi Giấy phép liên vận giữa Việt Nam và Lào
> 1. Cơ quan cấp giấy phép thu hồi Giấy phép liên vận giữa Việt Nam và Lào khi có vi phạm một trong các trường hợp sau:
> a) Không thực hiện đúng các nội dung ghi trong giấy phép liên vận khi thực hiện hoạt động vận tải liên vận giữa Việt Nam và Lào;
> b) Giấy phép kinh doanh vận tải bằng xe ô tô hoặc Giấy phép vận tải đường bộ quốc tế giữa Việt Nam và Lào hoặc phù hiệu của phương tiện bị cơ quan có thẩm quyền thu hồi (chỉ áp dụng đối với Giấy phép liên vận giữa Việt Nam và Lào cấp cho phương tiện thương mại);
> c) Phương tiện quá thời hạn tái nhập vào Việt Nam theo quy định, ngoại trừ trường hợp bị thiên tai, tai nạn hoặc lý do bất khả kháng;
> d) Cung cấp bản sao không đúng với bản chính hoặc thông tin sai lệch trong hồ sơ đề nghị cấp Giấy phép liên vận giữa Việt Nam và Lào hoặc có hành vi gian dối để được cấp Giấy phép liên vận giữa Việt Nam và Lào.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "B", "answer": "", "gold_units": ["ND158-2024/D54/K1"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-061 · tier B · ND165-2024/D21/K7

Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ)

`ND165-2024/D21/K7#2026-07-01` · hiệu lực 2026-07-01 → nay

> Điều 21. Sử dụng tạm thời lòng đường, vỉa hè vào mục đích khác
> 7. Trách nhiệm của cơ quan chấp thuận sử dụng tạm thời lòng đường, vỉa hè vào mục đích khác giao thông
> a) Gửi văn bản cấp phép sử dụng tạm thời lòng đường, vỉa hè vào mục đích khác cho Cảnh sát giao thông hoặc Cơ quan công an làm nhiệm vụ bảo đảm trật tự, an toàn giao thông trên tuyến đường;
> b) Hướng dẫn, kiểm tra, xử lý tổ chức, cá nhân sử dụng lòng đường, vỉa hè vào mục đích khác đối với các việc: bảo đảm giao thông, an toàn giao thông; quản lý, sử dụng tài sản kết cấu hạ tầng đường bộ; xử lý vi phạm hành chính theo quy định của pháp luật;
> c) Phối hợp với lực lượng Cảnh sát giao thông, Công an làm nhiệm vụ trên tuyến, Ủy ban nhân dân cấp xã và người quản lý, sử dụng đường bộ trong công tác bảo đảm an toàn giao thông và các công việc cần thiết khác;


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "B", "answer": "", "gold_units": ["ND165-2024/D21/K7"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-062 · tier B · ND158-2024/D61/K2

Nghị định số 158/2024/NĐ-CP (Quy định về hoạt động vận tải đường bộ)

`ND158-2024/D61/K2#2026-08-10` · hiệu lực 2026-08-10 → nay

> Điều 61. Gia hạn thời gian lưu hành tại Việt Nam cho phương tiện của Campuchia
> 2. Thẩm quyền gia hạn: Sở Xây dựng các tỉnh, thành phố trực thuộc trung ương nơi phương tiện gặp sự cố bất khả kháng.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "B", "answer": "", "gold_units": ["ND158-2024/D61/K2"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-063 · tier B · TT52-2024-BGTVT/D3/K8

Thông tư số 52/2024/TT-BGTVT (Quy định về yêu cầu kỹ thuật đối với xe cơ giới, xe máy chuyên dùng thuộc đối tượng nghiên cứu phát triển có nhu cầu tham gia giao thông đường bộ)

`TT52-2024-BGTVT/D3/K8#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 3. Giải thích từ ngữ
> 8. Tải trọng giả là tải trọng giả lập, sử dụng để kiểm tra khả năng chịu tải và hoạt động của xe trong các điều kiện khác nhau, nhằm mục đích đánh giá về chất lượng an toàn kỹ thuật và hiệu quả của xe, bao gồm: khối bê tông, khối hoặc tấm kim loại, thùng nước, bao cát, thiết bị mô phỏng tải trọng.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "B", "answer": "", "gold_units": ["TT52-2024-BGTVT/D3/K8"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-064 · tier B · ND158-2024/D11/K7

Nghị định số 158/2024/NĐ-CP (Quy định về hoạt động vận tải đường bộ)

`ND158-2024/D11/K7#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 11. Quy định về công tác bảo đảm an toàn trong hoạt động vận tải bằng xe ô tô, bằng xe bốn bánh có gắn động cơ
> 7. Khi xe đang hoạt động trên đường
> a) Bộ phận quản lý an toàn giao thông hoặc người được giao nhiệm vụ quản lý an toàn giao thông trong đơn vị kinh doanh vận tải thực hiện các nhiệm vụ: thông qua dữ liệu từ thiết bị giám sát hành trình, khi phát hiện lái xe vi phạm quá thời gian lái xe liên tục, quá thời gian lái xe trong ngày, chạy sai hành trình, thiết bị giám sát hành trình không hoạt động thì kịp thời thông tin cho lái xe yêu cầu điều chỉnh, kịp thời khắc phục các sai phạm;
> b) Người lái xe phải chấp hành nghiêm các quy định về an toàn giao thông trong quá trình điều khiển phương tiện để vận chuyển hành khách, hàng hóa, chấp hành quy định về thời gian lái xe liên tục, thời gian lái xe trong một ngày, trong một tuần, quy định về tốc độ, hành trình chạy xe, thiết bị giám sát hành trình, thiết bị ghi nhận hình ảnh người lái xe (đối với loại phương tiện phải lắp) bảo đảm luôn hoạt động; báo cáo ngay thời gian, địa điểm và nguyên nhân khi xảy ra sự cố mất an toàn giao thông để đơn vị có biện pháp xử lý kịp thời.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "B", "answer": "", "gold_units": ["ND158-2024/D11/K7"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-065 · tier C · TT72-2024-BCA/D17/K2

Thông tư số 72/2024/TT-BCA (Quy định quy trình điều tra, giải quyết tai nạn giao thông đường bộ của Cảnh sát giao thông)

`TT72-2024-BCA/D17/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 17. Thời hạn điều tra, xác minh, giải quyết vụ tai nạn giao thông đường bộ
> 2. Vụ tai nạn giao thông đường bộ quy định tại điểm b khoản 8 Điều 6 Thông tư này hoặc trong quá trình điều tra, xác minh giải quyết vụ tai nạn giao thông đường bộ quy định tại điểm c khoản 8 Điều 6 Thông tư này nếu phát hiện có dấu hiệu tội phạm, thì Cục Cảnh sát giao thông hoặc Phòng Cảnh sát giao thông Công an cấp tỉnh thực hiện xác minh giải quyết theo thời hạn quy định tại khoản 1, khoản 2 Điều 147 Bộ luật Tố tụng hình sự năm 2015 (sửa đổi bổ sung năm 2021) và Điều 9, Điều 11 Thông tư liên tịch số 01/2017/TTLT-BCA-BQP-BTC-BNN&PTNT-VKSNDTC ngày 29 tháng 12 năm 2017 của Bộ Công an, Bộ Quốc phòng, Bộ Tài chính, Bộ Nông nghiệp và Phát triển nông thôn, Viện kiểm sát nhân dân tối cao quy định về việc phối hợp giữa các cơ quan có thẩm quyền trong việc thực hiện một số quy định của Bộ luật Tố tụng hình sự năm 2015 về tiếp nhận, giải quyết tố giác, tin báo về tội phạm, kiến nghị khởi tố (sửa đổi, bổ sung một số điều năm 2021) và Điều 12 Thông tư số 28/2020/TT-BCA ngày 26 tháng 3 năm 2020 của Bộ trưởng Bộ Công an quy định trình tự, thủ tục tiếp nhận, phân loại, xử lý, giải quyết tố giác, tin báo về tội …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "C", "answer": "", "gold_units": ["TT72-2024-BCA/D17/K2"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-066 · tier C · TT72-2024-BCA/D21/K2

Thông tư số 72/2024/TT-BCA (Quy định quy trình điều tra, giải quyết tai nạn giao thông đường bộ của Cảnh sát giao thông)

`TT72-2024-BCA/D21/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 21. Các biểu mẫu sử dụng trong công tác điều tra, xác minh, giải quyết tai nạn giao thông đường bộ của Cảnh sát giao thông
> 2. Điều tra, xác minh, giải quyết vụ tai nạn giao thông đường bộ theo thủ tục hành chính thì sử dụng biểu mẫu ban hành kèm theo Nghị định số 118/2021/NĐ-CP và các biểu mẫu quy định tại khoản 3 Điều này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "C", "answer": "", "gold_units": ["TT72-2024-BCA/D21/K2"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-067 · tier C · TT72-2024-BCA/D18/K6

Thông tư số 72/2024/TT-BCA (Quy định quy trình điều tra, giải quyết tai nạn giao thông đường bộ của Cảnh sát giao thông)

`TT72-2024-BCA/D18/K6#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 18. Giải quyết vụ tai nạn giao thông đường bộ theo thủ tục hành chính
> 6. Cán bộ cảnh sát giao thông khi đến hiện trường thực hiện nhiệm vụ điều tra, xác minh, giải quyết vụ tai nạn giao thông đường bộ không có hậu quả thiệt hại về sức khỏe, tính mạng của người, chỉ có thiệt hại không đáng kể về tài sản (vụ va chạm giao thông) mà các bên liên quan trong vụ tai nạn có đề nghị cho thỏa thuận dân sự tại hiện trường thì cán bộ được phân công tiến hành giải quyết theo các bước như sau:
> a) Thực hiện các nội dung quy định tại các khoản 1, 2 Điều 7; các khoản 3, 4, 5, 6 và 7 Điều 8; các Điều 9; Điều 10; khoản 1, 2 Điều 11; Điều 13 Thông tư này;
> b) Căn cứ nội dung đơn yêu cầu giải quyết vụ va chạm giao thông cán bộ được phân công giải quyết vụ tai nạn giao thông đường bộ lập biên bản làm việc với các bên liên quan đến vụ tai nạn giao thông đường bộ;
> c) Trong thời gian 07 ngày làm việc cán bộ được phân công giải quyết báo cáo kết quả điều tra và đề xuất giải quyết vụ tai nạn giao thông đường bộ theo Mẫu số 10/TNĐB ban hành kèm theo Thông tư này đến lãnh đạo có thẩm quyền ra Thông báo kết quả điều tra, xác minh, giải quyết vụ tai nạn giao thông đường bộ theo Mẫu số 13/TNĐB ban hành kèm …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "thu_tuc_tham_quyen", "tier": "C", "answer": "", "gold_units": ["TT72-2024-BCA/D18/K6"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-068 · tier historical · TT35-2024-BGTVT/D19/K1

Thông tư số 35/2024/TT-BGTVT (Quy định về đào tạo, sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế; đào tạo, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ)

`TT35-2024-BGTVT/D19/K1#2025-01-01` · hiệu lực 2025-01-01 → 2025-08-31

> Điều 19. Hội đồng sát hạch
> 1. Hội đồng sát hạch do Sở Giao thông vận tải thành lập.
> a) Hội đồng làm việc phải có tối thiểu 2/3 số thành viên tham dự, quyết định theo đa số; trường hợp các thành viên trong hội đồng có ý kiến ngang nhau thì thực hiện theo kết luận của Chủ tịch hội đồng;
> b) Hội đồng sát hạch tự giải thể khi kết thúc kỳ sát hạch.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2025-08-31", "question_type": "thu_tuc_tham_quyen", "tier": "historical", "answer": "", "gold_units": ["TT35-2024-BGTVT/D19/K1"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-069 · tier historical · TT35-2024-BGTVT/D30/K2

Thông tư số 35/2024/TT-BGTVT (Quy định về đào tạo, sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế; đào tạo, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ)

`TT35-2024-BGTVT/D30/K2#2025-01-01` · hiệu lực 2025-01-01 → 2025-08-31

> Điều 30. Lưu trữ hồ sơ kết quả sát hạch
> 2. Cơ sở đào tạo lái xe lưu trữ hồ sơ của kỳ sát hạch bao gồm:
> a) Tài liệu tại các điểm a, b, c, d, g, h, i, k khoản 1 Điều này;
> b) Lưu trữ, bảo quản bài sát hạch lý thuyết, bài sát hạch lái xe trên phần mềm mô phỏng các tình huống giao thông, biên bản sát hạch thực hành lái xe trong hình của từng kỳ sát hạch có đầy đủ chữ kỹ của thí sinh và sát hạch viên;
> c) Lưu trữ, bảo quản biên bản sát hạch thực hành lái xe trên đường của từng kỳ sát hạch, gồm: chữ ký của thí sinh tại phiếu kết quả sát hạch thực hành lái xe trên đường được in từ thiết bị chấm điểm tự động trên ô tô sát hạch thực hành lái xe trên đường hoặc biên bản sát hạch thực hành lái xe trên đường có chữ ký của sát hạch viên;
> d) Trường hợp cơ sở đào tạo lái xe có sân tập lái dùng để thực hiện sát hạch lái xe mô tô phải lưu trữ dữ liệu giám sát sát hạch; dữ liệu kết quả sát hạch lý thuyết, thực hành lái xe trong hình với thời hạn 03 năm.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2025-08-31", "question_type": "thu_tuc_tham_quyen", "tier": "historical", "answer": "", "gold_units": ["TT35-2024-BGTVT/D30/K2"], "required_numbers": []}
```

### W-thu_tuc_tham_quyen-070 · tier historical · TT35-2024-BGTVT/D36/K3

Thông tư số 35/2024/TT-BGTVT (Quy định về đào tạo, sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế; đào tạo, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ)

`TT35-2024-BGTVT/D36/K3#2025-01-01` · hiệu lực 2025-01-01 → 2025-08-31

> Điều 36. Đổi giấy phép lái xe do ngành Giao thông vận tải cấp
> 3. Trình tự thực hiện
> a) Cá nhân lập 01 bộ hồ sơ theo quy định tại khoản 2 Điều này gửi trực tiếp hoặc qua hệ thống dịch vụ công trực tuyến đến Sở Giao thông vận tải.
> Trường hợp nộp hồ sơ trực tiếp cá nhân phải chụp ảnh trực tiếp tại cơ quan cấp giấy phép lái xe và phải hoàn thành nghĩa vụ nộp lệ phí khi được tiếp nhận hồ sơ.
> Trường hợp nộp hồ sơ qua hệ thống dịch vụ công trực tuyến, cá nhân kê khai theo hướng dẫn, phải chịu trách nhiệm về tính chính xác, tính hợp pháp của nội dung đã kê khai và phải hoàn thành nghĩa vụ nộp lệ phí cấp giấy phép lái xe thông qua chức năng thanh toán của hệ thống dịch vụ công trực tuyến theo quy định và nộp phí sử dụng dịch vụ khác theo nhu cầu của cá nhân; khi nhận giấy phép lái xe, phải nộp lại giấy phép lái xe cũ để lưu hồ sơ;
> b) Sở Giao thông vận tải kiểm tra hồ sơ khi tiếp nhận, tra cứu phần mềm quản lý vi phạm của hệ thống thông tin về đào tạo, sát hạch, cấp giấy phép lái xe, chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ, truy cập phần mềm cơ sở dữ liệu về trật tự, an toàn giao thông đường bộ của ngành Công an hoặc tra cứu vi phạm của người lái xe thông qua tài …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2025-08-31", "question_type": "thu_tuc_tham_quyen", "tier": "historical", "answer": "", "gold_units": ["TT35-2024-BGTVT/D36/K3"], "required_numbers": []}
```

## theo_thoi_diem — câu trả lời khác nhau trước/sau một mốc sửa đổi (đi theo cặp)

### W-theo_thoi_diem-001 · tier A · LUAT35-2024/D35/K4

Luật Đường bộ số 35/2024/QH15 · trước mốc: chưa có hiệu lực · ngày đổi 2025-01-01

**Trước mốc (2024-12-31)**: chưa có hiệu lực (không có phiên bản).

**Sau mốc (2025-01-01)** · chunk `LUAT35-2024/D35/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 35. Bảo trì kết cấu hạ tầng đường bộ
> 4. Sửa chữa định kỳ bao gồm:
> a) Sửa chữa khiếm khuyết, hư hỏng công trình, hạng mục công trình, thiết bị, thay thế bộ phận công trình, thiết bị lắp đặt vào công trình bị hư hỏng được thực hiện định kỳ về thời hạn hoặc tần suất khai thác, sử dụng theo quy chuẩn, tiêu chuẩn kỹ thuật, quy trình bảo trì kết cấu hạ tầng đường bộ;
> b) Bổ sung báo hiệu đường bộ, công trình an toàn giao thông đường bộ và các hạng mục công trình, thiết bị công trình khác để bảo đảm giao thông an toàn, thông suốt và cải thiện tình trạng kỹ thuật của công trình đang khai thác;
> c) Sửa chữa, nâng cấp kho chứa trang thiết bị, vật tư dự phòng trong lĩnh vực đường bộ; mua sắm bổ sung vật tư dự phòng phục vụ công tác phòng, chống, khắc phục hậu quả thiên tai và tìm kiếm cứu nạn;
> d) Sửa chữa, nâng cấp hệ thống quản lý giao thông thông minh; trung tâm quản lý, điều hành giao thông tuyến đường cao tốc; phương tiện, thiết bị, hệ thống công nghệ phục vụ công tác quản lý, vận hành, khai thác, bảo trì công trình đường bộ; hệ thống quản lý, vận hành giao thông đường bộ; hệ thống thu phí; công trình kiểm soát tải trọng xe.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2024-12-31", "question_type": "theo_thoi_diem", "tier": "A", "answer": "", "gold_units": [], "required_numbers": [], "pair_id": "p-001"}
{"qid": "", "question": "", "as_of": "2025-01-01", "question_type": "theo_thoi_diem", "tier": "A", "answer": "", "gold_units": ["LUAT35-2024/D35/K4"], "required_numbers": [], "pair_id": "p-001"}
```

### W-theo_thoi_diem-002 · tier B · ND165-2024/D7/K1

Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ) · trước mốc: chưa có hiệu lực · ngày đổi 2025-01-01

**Trước mốc (2024-12-31)**: chưa có hiệu lực (không có phiên bản).

**Sau mốc (2025-01-01)** · chunk `ND165-2024/D7/K1#2025-01-01` · hiệu lực 2025-01-01 → 2026-06-30

> Điều 7. Điều chỉnh loại đường theo cấp quản lý
> 1. Bộ Giao thông vận tải quyết định điều chỉnh quốc lộ thành đường địa phương; đường địa phương và đường khác thành quốc lộ đối với các trường hợp sau:
> a) Tuyến, đoạn tuyến quốc lộ điều chỉnh thành đường địa phương đối với các trường hợp: không có trong quy hoạch mạng lưới đường bộ, quy hoạch kết cấu hạ tầng đường bộ được Thủ tướng Chính phủ phê duyệt, trừ trường hợp quốc lộ có yêu cầu đặc biệt về bảo đảm quốc phòng, an ninh; đã đầu tư xây dựng tuyến tránh thay thế phù hợp với quy hoạch mạng lưới đường bộ, quy hoạch kết cấu hạ tầng đường bộ được Thủ tướng Chính phủ phê duyệt;
> b) Tuyến, đoạn tuyến đường địa phương và đường bộ khác có trong quy hoạch mạng lưới đường bộ, quy hoạch kết cấu hạ tầng đường bộ được Thủ tướng Chính phủ phê duyệt thì điều chỉnh thành quốc lộ.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2024-12-31", "question_type": "theo_thoi_diem", "tier": "B", "answer": "", "gold_units": [], "required_numbers": [], "pair_id": "p-002"}
{"qid": "", "question": "", "as_of": "2025-01-01", "question_type": "theo_thoi_diem", "tier": "B", "answer": "", "gold_units": ["ND165-2024/D7/K1"], "required_numbers": [], "pair_id": "p-002"}
```

### W-theo_thoi_diem-003 · tier historical · TT35-2024-BGTVT/D66/K2

Thông tư số 35/2024/TT-BGTVT (Quy định về đào tạo, sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế; đào tạo, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ) · trước mốc: chưa có hiệu lực · ngày đổi 2025-01-01

**Trước mốc (2024-12-31)**: chưa có hiệu lực (không có phiên bản).

**Sau mốc (2025-01-01)** · chunk `TT35-2024-BGTVT/D66/K2#2025-01-01` · hiệu lực 2025-01-01 → 2025-08-31

> Điều 66. Hiệu lực thi hành
> 2. Thông tư này bãi bỏ các Thông tư:
> a) Thông tư số 06/2011/TT-BGTVT ngày 07 tháng 3 năm 2011 của Bộ trưởng Bộ Giao thông vận tải quy định về bồi dưỡng kiến thức pháp luật về giao thông đường bộ cho người điều khiển xe máy chuyên dùng tham gia giao thông đường bộ;
> b) Thông tư số 07/2013/TT- BGTVT ngày 03 tháng 5 năm 2013 của Bộ trưởng Bộ Giao thông vận tải quy định về quản lý, vận hành và khai thác hệ thống thông tin giấy phép lái xe;
> c) Thông tư số 29/2015/TT-BGTVT ngày 06 tháng 7 năm 2015 của Bộ trưởng Bộ Giao thông vận tải ban hành Thông tư quy định về cấp, sử dụng giấy phép lái xe quốc tế;
> d) Thông tư số 12/2017/TT-BGTVT ngày 15 tháng 4 năm 2017 của Bộ trưởng Bộ Giao thông vận tải quy định về đào tạo, sát hạch, cấp giấy phép lái xe cơ giới đường bộ;
> đ) Thông tư số 38/2019/TT-BGTVT ngày 08 tháng 10 năm 2019 của Bộ trưởng Bộ Giao thông vận tải sửa đổi, bổ sung một số điều Thông tư số 12/2017/TT-BGTVT ngày 15 tháng 4 năm 2017 của Bộ trưởng Bộ Giao thông vận tải quy định về đào tạo, sát hạch, cấp giấy phép lái xe cơ giới đường bộ;
> e) Thông tư số 01/2021/TT-BGTVT ngày 27 tháng 01 năm 2021 của Bộ trưởng Bộ Giao thông vận tải sửa đổi, bổ sung một số điều …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2024-12-31", "question_type": "theo_thoi_diem", "tier": "historical", "answer": "", "gold_units": [], "required_numbers": [], "pair_id": "p-003"}
{"qid": "", "question": "", "as_of": "2025-01-01", "question_type": "theo_thoi_diem", "tier": "historical", "answer": "", "gold_units": ["TT35-2024-BGTVT/D66/K2"], "required_numbers": [], "pair_id": "p-003"}
```

### W-theo_thoi_diem-004 · tier B · ND158-2024/D11/K9

Nghị định số 158/2024/NĐ-CP (Quy định về hoạt động vận tải đường bộ) · trước mốc: chưa có hiệu lực · ngày đổi 2025-01-01

**Trước mốc (2024-12-31)**: chưa có hiệu lực (không có phiên bản).

**Sau mốc (2025-01-01)** · chunk `ND158-2024/D11/K9#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 11. Quy định về công tác bảo đảm an toàn trong hoạt động vận tải bằng xe ô tô, bằng xe bốn bánh có gắn động cơ
> 9. Theo định kỳ tháng, quý, năm, bộ phận (cán bộ quản lý do đơn vị phân công) quản lý an toàn phải thực hiện các nhiệm vụ sau:
> a) Thống kê số vụ, nguyên nhân, mức độ tai nạn giao thông đã xảy ra của từng người lái xe và của toàn đơn vị;
> b) Xây dựng và thực hiện phương án xử lý khi xảy ra sự cố gây mất an toàn giao thông trong quá trình kinh doanh vận tải;
> c) Tổ chức đánh giá, rút kinh nghiệm đối với toàn bộ người lái xe của đơn vị sau khi xảy ra tai nạn giao thông từ nghiêm trọng trở lên trong quá trình kinh doanh vận tải;
> d) Phối hợp với các bộ phận nghiệp vụ của đơn vị để tổ chức tập huấn nghiệp vụ vận tải cho toàn bộ người lái xe của đơn vị theo quy định;
> đ) Lưu trữ hồ sơ, sổ sách ghi chép bằng bản giấy hoặc lưu trên phần mềm kết quả thực hiện các nhiệm vụ theo quy định tại khoản 2, khoản 3, và điểm a khoản 7 Điều này. Thời gian lưu trữ tối thiểu 03 năm.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2024-12-31", "question_type": "theo_thoi_diem", "tier": "B", "answer": "", "gold_units": [], "required_numbers": [], "pair_id": "p-004"}
{"qid": "", "question": "", "as_of": "2025-01-01", "question_type": "theo_thoi_diem", "tier": "B", "answer": "", "gold_units": ["ND158-2024/D11/K9"], "required_numbers": [], "pair_id": "p-004"}
```

### W-theo_thoi_diem-005 · tier A · TT36-2024-BYT/D9/K1

Thông tư số 36/2024/TT-BYT (Quy định về tiêu chuẩn sức khỏe, việc khám sức khỏe đối với người lái xe, người điều khiển xe máy chuyên dùng; việc khám sức khỏe định kỳ đối với người hành nghề lái xe ô tô; cơ sở dữ liệu về sức khỏe của người lái xe, người điều khiển xe máy chuyên dùng) · trước mốc: chưa có hiệu lực · ngày đổi 2025-01-01

**Trước mốc (2024-12-31)**: chưa có hiệu lực (không có phiên bản).

**Sau mốc (2025-01-01)** · chunk `TT36-2024-BYT/D9/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 9. Điều khoản chuyển tiếp
> 1. Giấy khám sức khỏe và sổ khám sức khỏe định kỳ của người lái xe được cấp trước ngày Thông tư này có hiệu lực thi hành được tiếp tục sử dụng theo thời hạn ghi trên giấy khám sức khỏe và sổ khám sức khỏe định kỳ của người lái xe theo quy định tại Thông tư liên tịch số 24/2015/TTLT-BYT-BGTVT ngày 28 tháng 8 năm 2015 của Bộ trưởng Bộ Y tế và Bộ trưởng Bộ Giao thông vận tải quy định về tiêu chuẩn sức khỏe của người lái xe, việc khám sức khỏe định kỳ đối với người lái xe ô tô và quy định về cơ sở y tế khám sức khỏe cho người lái xe.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2024-12-31", "question_type": "theo_thoi_diem", "tier": "A", "answer": "", "gold_units": [], "required_numbers": [], "pair_id": "p-005"}
{"qid": "", "question": "", "as_of": "2025-01-01", "question_type": "theo_thoi_diem", "tier": "A", "answer": "", "gold_units": ["TT36-2024-BYT/D9/K1"], "required_numbers": [], "pair_id": "p-005"}
```

### W-theo_thoi_diem-006 · tier B · TT69-2024-BCA/D7/K10

Thông tư số 69/2024/TT-BCA (Quy định về chỉ huy, điều khiển giao thông đường bộ của Cảnh sát giao thông) · trước mốc: chưa có hiệu lực · ngày đổi 2025-01-01

**Trước mốc (2024-12-31)**: chưa có hiệu lực (không có phiên bản).

**Sau mốc (2025-01-01)** · chunk `TT69-2024-BCA/D7/K10#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 7. Các biểu mẫu trong công tác chỉ huy, điều khiển giao thông đường bộ
> 10. Mẫu động tác báo hiệu bên phải dừng lại (mẫu số 10).


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2024-12-31", "question_type": "theo_thoi_diem", "tier": "B", "answer": "", "gold_units": [], "required_numbers": [], "pair_id": "p-006"}
{"qid": "", "question": "", "as_of": "2025-01-01", "question_type": "theo_thoi_diem", "tier": "B", "answer": "", "gold_units": ["TT69-2024-BCA/D7/K10"], "required_numbers": [], "pair_id": "p-006"}
```

### W-theo_thoi_diem-007 · tier A · LUAT35-2024/D58/K2

Luật Đường bộ số 35/2024/QH15 · trước mốc: chưa có hiệu lực · ngày đổi 2025-01-01

**Trước mốc (2024-12-31)**: chưa có hiệu lực (không có phiên bản).

**Sau mốc (2025-01-01)** · chunk `LUAT35-2024/D58/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 58. Quyền và nghĩa vụ của đơn vị kinh doanh vận tải hành khách bằng xe ô tô
> 2. Đơn vị kinh doanh vận tải hành khách bằng xe ô tô có các nghĩa vụ sau đây:
> a) Chấp hành và thực hiện đầy đủ quy định về kinh doanh, điều kiện kinh doanh vận tải bằng xe ô tô, cam kết về chất lượng vận tải, hợp đồng vận tải;
> b) Mua bảo hiểm cho hành khách; phí bảo hiểm được tính vào giá vé, giá trị hợp đồng vận tải;
> c) Thực hiện kê khai giá theo quy định của pháp luật về giá; cung cấp vé, chứng từ thu tiền vận tải;
> d) Bồi thường thiệt hại do người lao động, người đại diện của đơn vị kinh doanh vận tải hành khách bằng xe ô tô gây ra trong quá trình vận tải theo quy định của pháp luật;
> đ) Thực hiện việc miễn giảm giá vé đối với người cao tuổi, người khuyết tật và các đối tượng chính sách khác theo quy định của pháp luật;
> e) Không được để tổ chức, cá nhân không có giấy phép kinh doanh vận tải bằng xe ô tô loại hình vận tải hành khách thực hiện điều hành phương tiện và lái xe hoặc quyết định giá cước để vận tải hành khách;
> g) Không được sử dụng người không có giấy phép lái xe hoặc có giấy phép lái xe nhưng không phù hợp với loại xe, người có giấy phép lái xe bị trừ hết điểm, người đang bị tước hoặc bị …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2024-12-31", "question_type": "theo_thoi_diem", "tier": "A", "answer": "", "gold_units": [], "required_numbers": [], "pair_id": "p-007"}
{"qid": "", "question": "", "as_of": "2025-01-01", "question_type": "theo_thoi_diem", "tier": "A", "answer": "", "gold_units": ["LUAT35-2024/D58/K2"], "required_numbers": [], "pair_id": "p-007"}
```

### W-theo_thoi_diem-008 · tier A · LUAT36-2024/D33/K4

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15 · trước mốc: chưa có hiệu lực · ngày đổi 2025-01-01

**Trước mốc (2024-12-31)**: chưa có hiệu lực (không có phiên bản).

**Sau mốc (2025-01-01)** · chunk `LUAT36-2024/D33/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 33. Người lái xe, người được chở, hàng hóa xếp trên xe mô tô, xe gắn máy
> 4. Người được chở trên xe mô tô hai bánh, xe mô tô ba bánh, xe gắn máy khi tham gia giao thông đường bộ không được thực hiện các hành vi sau đây:
> a) Mang, vác vật cồng kềnh;
> b) Sử dụng ô;
> c) Bám, kéo hoặc đẩy các phương tiện khác;
> d) Đứng trên yên, giá đèo hàng hoặc ngồi trên tay lái;
> đ) Hành vi khác gây mất trật tự, an toàn giao thông đường bộ.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2024-12-31", "question_type": "theo_thoi_diem", "tier": "A", "answer": "", "gold_units": [], "required_numbers": [], "pair_id": "p-008"}
{"qid": "", "question": "", "as_of": "2025-01-01", "question_type": "theo_thoi_diem", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D33/K4"], "required_numbers": [], "pair_id": "p-008"}
```

### W-theo_thoi_diem-009 · tier A · LUAT36-2024/D10/K3

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15 · trước mốc: chưa có hiệu lực · ngày đổi 2026-01-01

**Trước mốc (2025-12-31)**: chưa có hiệu lực (không có phiên bản).

**Sau mốc (2026-01-01)** · chunk `LUAT36-2024/D10/K3#2026-01-01` · hiệu lực 2026-01-01 → nay

> Điều 10. Quy tắc chung
> 3. Khi chở trẻ em dưới 10 tuổi và chiều cao dưới 1,35 mét trên xe ô tô không được cho trẻ em ngồi cùng hàng ghế với người lái xe, trừ loại xe ô tô chỉ có một hàng ghế; người lái xe phải sử dụng, hướng dẫn sử dụng thiết bị an toàn phù hợp cho trẻ em.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2025-12-31", "question_type": "theo_thoi_diem", "tier": "A", "answer": "", "gold_units": [], "required_numbers": [], "pair_id": "p-009"}
{"qid": "", "question": "", "as_of": "2026-01-01", "question_type": "theo_thoi_diem", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D10/K3"], "required_numbers": [], "pair_id": "p-009"}
```

### W-theo_thoi_diem-010 · tier A · ND168-2024/D27/K1

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · ngày đổi 2026-01-01

**Trước mốc (2025-12-31)** · chunk `ND168-2024/D27/K1#2025-01-01` · hiệu lực 2025-01-01 → 2025-12-31

> Điều 27. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô kinh doanh vận tải chở trẻ em mầm non, học sinh, xe ô tô kinh doanh vận tải kết hợp với hoạt động đưa đón trẻ em mầm non, học sinh
> 1. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với người điều khiển xe ô tô kinh doanh vận tải chở trẻ em mầm non, học sinh, xe ô tô kinh doanh vận tải kết hợp với hoạt động đưa đón trẻ em mầm non, học sinh thực hiện một trong các hành vi vi phạm sau đây:
> a) Không hướng dẫn trẻ em mầm non, học sinh ngồi đúng vị trí quy định trong xe;
> c) Điều khiển xe không lắp thiết bị ghi nhận hình ảnh người lái xe hoặc có lắp thiết bị ghi nhận hình ảnh người lái xe nhưng không có tác dụng trong quá trình xe tham gia giao thông theo quy định hoặc làm sai lệch dữ liệu của thiết bị ghi nhận hình ảnh người lái xe lắp trên xe ô tô.

- CheTai phat_tien: 1.000.000–2.000.000 đồng (nêu tại ND168-2024/D27/K1)

**Sau mốc (2026-01-01)** · chunk `ND168-2024/D27/K1#2026-01-01` · hiệu lực 2026-01-01 → nay

> Điều 27. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô kinh doanh vận tải chở trẻ em mầm non, học sinh, xe ô tô kinh doanh vận tải kết hợp với hoạt động đưa đón trẻ em mầm non, học sinh
> 1. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với người điều khiển xe ô tô kinh doanh vận tải chở trẻ em mầm non, học sinh, xe ô tô kinh doanh vận tải kết hợp với hoạt động đưa đón trẻ em mầm non, học sinh thực hiện một trong các hành vi vi phạm sau đây:
> a) Không hướng dẫn trẻ em mầm non, học sinh ngồi đúng vị trí quy định trong xe;
> b) Điều khiển xe ô tô kinh doanh vận tải chở trẻ em mầm non, học sinh tiểu học, xe ô tô kinh doanh vận tải kết hợp với hoạt động đưa đón trẻ em mầm non, học sinh tiểu học không có dây đai an toàn phù hợp với lứa tuổi hoặc không có ghế ngồi phù hợp với lứa tuổi theo quy định;
> c) Điều khiển xe không lắp thiết bị ghi nhận hình ảnh người lái xe hoặc có lắp thiết bị ghi nhận hình ảnh người lái xe nhưng không có tác dụng trong quá trình xe tham gia giao thông theo quy định hoặc làm sai lệch dữ liệu của thiết bị ghi nhận hình ảnh người lái xe lắp trên xe ô tô.

- CheTai phat_tien: 1.000.000–2.000.000 đồng (nêu tại ND168-2024/D27/K1)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2025-12-31", "question_type": "theo_thoi_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D27/K1"], "required_numbers": [], "pair_id": "p-010"}
{"qid": "", "question": "", "as_of": "2026-01-01", "question_type": "theo_thoi_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D27/K1"], "required_numbers": [], "pair_id": "p-010"}
```

### W-theo_thoi_diem-011 · tier B · ND165-2024/D20/K3

Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ) · ngày đổi 2026-07-01

**Trước mốc (2026-06-30)** · chunk `ND165-2024/D20/K3#2025-01-01` · hiệu lực 2025-01-01 → 2026-06-30

> Điều 20. Bảo vệ kết cấu hạ tầng đường bộ
> 3. Bộ Giao thông vận tải tổ chức thực hiện bảo vệ kết cấu hạ tầng đường bộ quy định tại khoản 1 và khoản 2 Điều này đối với quốc lộ quy định tại khoản 3 Điều 8 Luật Đường bộ và kết cấu hạ tầng đường bộ khác thuộc phạm vi quản lý.


**Sau mốc (2026-07-01)** · chunk `ND165-2024/D20/K3#2026-07-01` · hiệu lực 2026-07-01 → nay

> Điều 20. Bảo vệ kết cấu hạ tầng đường bộ
> 3. Bộ Xây dựng tổ chức thực hiện bảo vệ kết cấu hạ tầng đường bộ quy định tại khoản 1 và khoản 2 Điều này đối với quốc lộ quy định tại khoản 3 Điều 8 Luật Đường bộ và kết cấu hạ tầng đường bộ khác thuộc phạm vi quản lý.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-06-30", "question_type": "theo_thoi_diem", "tier": "B", "answer": "", "gold_units": ["ND165-2024/D20/K3"], "required_numbers": [], "pair_id": "p-011"}
{"qid": "", "question": "", "as_of": "2026-07-01", "question_type": "theo_thoi_diem", "tier": "B", "answer": "", "gold_units": ["ND165-2024/D20/K3"], "required_numbers": [], "pair_id": "p-011"}
```

### W-theo_thoi_diem-012 · tier B · ND165-2024/D5/K5

Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ) · trước mốc: chưa có hiệu lực · ngày đổi 2026-07-01

**Trước mốc (2026-06-30)**: chưa có hiệu lực (không có phiên bản).

**Sau mốc (2026-07-01)** · chunk `ND165-2024/D5/K5#2026-07-01` · hiệu lực 2026-07-01 → nay

> Điều 5. Giao Ủy ban nhân dân cấp tỉnh quản lý quốc lộ để đáp ứng nhu cầu phát triển kinh tế - xã hội, bảo đảm lợi ích quốc gia, quốc phòng, an ninh và khả năng bố trí nguồn lực của địa phương
> 5. Nguồn vốn để đầu tư, xây dựng, quản lý quốc lộ giao Ủy ban nhân dân cấp tỉnh theo quy định tại khoản 5 Điều 4 Nghị định này.
> Ủy ban nhân dân cấp tỉnh có trách nhiệm bố trí ngân sách địa phương và các nguồn lực bảo đảm việc thực hiện đầu tư xây dựng, quản lý quốc lộ được giao quản lý.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-06-30", "question_type": "theo_thoi_diem", "tier": "B", "answer": "", "gold_units": [], "required_numbers": [], "pair_id": "p-012"}
{"qid": "", "question": "", "as_of": "2026-07-01", "question_type": "theo_thoi_diem", "tier": "B", "answer": "", "gold_units": ["ND165-2024/D5/K5"], "required_numbers": [], "pair_id": "p-012"}
```

### W-theo_thoi_diem-013 · tier B · ND165-2024/D60/K3

Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ) · ngày đổi 2026-07-01

**Trước mốc (2026-06-30)** · chunk `ND165-2024/D60/K3#2025-01-01` · hiệu lực 2025-01-01 → 2026-06-30

> Điều 60. Thu thập, cập nhật, điều chỉnh thông tin trong cơ sở dữ liệu đường bộ
> 3. Thông tin quy định tại khoản 3 Điều 57 của Nghị định này được trích, chọn và đồng bộ hóa từ cơ sở dữ liệu, cơ sở dữ liệu chuyên ngành của Bộ Giao thông vận tải và các địa phương.


**Sau mốc (2026-07-01)** · chunk `ND165-2024/D60/K3#2026-07-01` · hiệu lực 2026-07-01 → nay

> Điều 60. Thu thập, cập nhật, điều chỉnh thông tin trong cơ sở dữ liệu đường bộ
> 3. Thông tin quy định tại khoản 3 Điều 57 của Nghị định này được trích, chọn và đồng bộ hóa từ cơ sở dữ liệu, cơ sở dữ liệu chuyên ngành của Bộ Xây dựng và các địa phương.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-06-30", "question_type": "theo_thoi_diem", "tier": "B", "answer": "", "gold_units": ["ND165-2024/D60/K3"], "required_numbers": [], "pair_id": "p-013"}
{"qid": "", "question": "", "as_of": "2026-07-01", "question_type": "theo_thoi_diem", "tier": "B", "answer": "", "gold_units": ["ND165-2024/D60/K3"], "required_numbers": [], "pair_id": "p-013"}
```

### W-theo_thoi_diem-014 · tier A · TT14-2025-BXD/D28/K1

Thông tư số 14/2025/TT-BXD (Quy định về đào tạo lái xe; bồi dưỡng, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ) · ngày đổi 2026-07-01

**Trước mốc (2026-06-30)** · chunk `TT14-2025-BXD/D28/K1#2025-09-01` · hiệu lực 2025-09-01 → 2026-06-30

> Điều 28. Cục Đường bộ Việt Nam
> 1. Đối với công tác đào tạo lái xe, bồi dưỡng kiến thức pháp luật về giao thông đường bộ:
> a) Tổ chức tập huấn, hướng dẫn nghiệp vụ về hoạt động đào tạo lái xe, bồi dưỡng kiến thức pháp luật về giao thông đường bộ;
> b) Ứng dụng công nghệ thông tin trong công tác quản lý đào tạo lái xe, bồi dưỡng kiến thức pháp luật về giao thông đường bộ;
> c) Công bố và thực hiện cập nhật danh sách các cơ sở đào tạo lái xe ô tô được cấp hoặc bị thu hồi giấy phép đào tạo lái xe trên trang thông tin điện tử.


**Sau mốc (2026-07-01)** · chunk `TT14-2025-BXD/D28/K1#2026-07-01` · hiệu lực 2026-07-01 → nay

> Điều 28. Cục Đường bộ Việt Nam
> 1. Đối với công tác đào tạo lái xe, bồi dưỡng kiến thức pháp luật về giao thông đường bộ:
> a) Tổ chức tập huấn, hướng dẫn nghiệp vụ về hoạt động đào tạo lái xe, bồi dưỡng kiến thức pháp luật về giao thông đường bộ;
> b) Ứng dụng công nghệ thông tin trong công tác quản lý đào tạo lái xe, bồi dưỡng kiến thức pháp luật về giao thông đường bộ;
> c) Công bố và thực hiện cập nhật danh sách các cơ sở đào tạo lái xe ô tô được cấp hoặc bị thu hồi giấy phép đào tạo lái xe trên trang thông tin điện tử.
> d) Định kỳ hàng năm, rà soát để cập nhật, bổ sung và công bố danh mục, dấu hiệu nhận biết và phương án xử lý các tình huống giao thông.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-06-30", "question_type": "theo_thoi_diem", "tier": "A", "answer": "", "gold_units": ["TT14-2025-BXD/D28/K1"], "required_numbers": [], "pair_id": "p-014"}
{"qid": "", "question": "", "as_of": "2026-07-01", "question_type": "theo_thoi_diem", "tier": "A", "answer": "", "gold_units": ["TT14-2025-BXD/D28/K1"], "required_numbers": [], "pair_id": "p-014"}
```

### W-theo_thoi_diem-015 · tier B · ND165-2024/D46/K6

Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ) · ngày đổi 2026-07-01

**Trước mốc (2026-06-30)** · chunk `ND165-2024/D46/K6#2025-01-01` · hiệu lực 2025-01-01 → 2026-06-30

> Điều 46. Mở rộng, nâng cấp đường cao tốc trong trường hợp lập dự án đầu tư mở rộng, nâng cấp để đấu thầu lựa chọn nhà đầu tư theo phương thức đối tác công tư
> 6. Trường hợp thỏa thuận mở rộng, nâng cấp theo phương án lập dự án đầu tư theo phương thức đối tác công tư để đấu thầu lựa chọn nhà đầu tư mở rộng, nâng cấp theo khoản 1 Điều này không thành công, cơ quan ký kết hợp đồng thỏa thuận với nhà đầu tư về việc nhà đầu tư hiện hữu đề xuất điều chỉnh dự án theo quy định tại Điều 47 của Nghị định này.


**Sau mốc (2026-07-01)** · chunk `ND165-2024/D46/K6#2026-07-01` · hiệu lực 2026-07-01 → nay

> Điều 46. Mở rộng, nâng cấp đường cao tốc trong trường hợp lập dự án đầu tư mở rộng, nâng cấp để đấu thầu lựa chọn nhà đầu tư theo phương thức đối tác công tư
> 6. Trường hợp cơ quan ký kết hợp đồng không thỏa thuận được với nhà đầu tư hiện hữu đối với các nội dung quy định tại khoản 1 Điều này, cơ quan ký kết hợp đồng thỏa thuận với nhà đầu tư về việc nhà đầu tư hiện hữu đề xuất điều chỉnh dự án hiện hữu theo quy định tại Điều 47 của Nghị định này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-06-30", "question_type": "theo_thoi_diem", "tier": "B", "answer": "", "gold_units": ["ND165-2024/D46/K6"], "required_numbers": [], "pair_id": "p-015"}
{"qid": "", "question": "", "as_of": "2026-07-01", "question_type": "theo_thoi_diem", "tier": "B", "answer": "", "gold_units": ["ND165-2024/D46/K6"], "required_numbers": [], "pair_id": "p-015"}
```

### W-theo_thoi_diem-016 · tier B · ND165-2024/D4/K1

Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ) · ngày đổi 2026-07-01

**Trước mốc (2026-06-30)** · chunk `ND165-2024/D4/K1#2025-01-01` · hiệu lực 2025-01-01 → 2026-06-30

> Điều 4. Phân cấp quản lý quốc lộ
> 1. Phân cấp để Ủy ban nhân dân cấp tỉnh quản lý quốc lộ bao gồm:
> a) Quốc lộ trên địa bàn tỉnh, thành phố trực thuộc trung ương, trừ quốc lộ quy định tại khoản 2 Điều này;
> b) Các công trình, hạng mục thuộc kết cấu hạ tầng đường bộ gắn với quốc lộ được phân cấp (nhà hạt quản lý đường bộ, công trình kiểm soát tải trọng xe, đất của đường bộ, hành lang an toàn đường bộ và các hạng mục khác thuộc kết cấu hạ tầng đường bộ);
> c) Các công trình cầu, hầm, bến phà nằm trên địa bàn hai tỉnh, thành phố trực thuộc trung ương, Bộ Giao thông vận tải lấy ý kiến Ủy ban nhân dân cấp tỉnh có liên quan, trước khi quyết định một Ủy ban nhân dân cấp tỉnh được phân cấp quản lý công trình này.


**Sau mốc (2026-07-01)** · chunk `ND165-2024/D4/K1#2026-07-01` · hiệu lực 2026-07-01 → nay

> Điều 4. Phân cấp quản lý quốc lộ
> 1. Các tuyến đường quốc lộ thuộc quy hoạch mạng lưới đường bộ được phân cấp để Ủy ban nhân dân cấp tỉnh quản lý, bao gồm:
> a) Quốc lộ trên địa bàn tỉnh, thành phố trực thuộc trung ương, trừ quốc lộ quy định tại khoản 2 Điều này và Điều 6 Nghị định này;
> b) Các công trình, hạng mục thuộc kết cấu hạ tầng đường bộ gắn với quốc lộ phân cấp quy định tại điểm a và điểm c khoản này;
> c) Các công trình cầu, hầm, bến phà của tuyến đường quy định tại điểm a khoản này nằm trên địa bàn hai tỉnh, thành phố trực thuộc trung ương, Bộ Xây dựng lấy ý kiến Ủy ban nhân dân cấp tỉnh có liên quan, trước khi quyết định một Ủy ban nhân dân cấp tỉnh quản lý công trình.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-06-30", "question_type": "theo_thoi_diem", "tier": "B", "answer": "", "gold_units": ["ND165-2024/D4/K1"], "required_numbers": [], "pair_id": "p-016"}
{"qid": "", "question": "", "as_of": "2026-07-01", "question_type": "theo_thoi_diem", "tier": "B", "answer": "", "gold_units": ["ND165-2024/D4/K1"], "required_numbers": [], "pair_id": "p-016"}
```

### W-theo_thoi_diem-017 · tier B · ND165-2024/D32/K1

Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ) · ngày đổi 2026-07-01

**Trước mốc (2026-06-30)** · chunk `ND165-2024/D32/K1#2025-01-01` · hiệu lực 2025-01-01 → 2026-06-30

> Điều 32. Thẩm tra, thẩm định an toàn giao thông đường bộ
> 1. Trong giai đoạn lập dự án đầu tư, thiết kế triển khai sau thiết kế cơ sở, việc thẩm tra, thẩm định an toàn giao thông đường bộ được thực hiện cùng công tác thẩm tra, thẩm định báo cáo nghiên cứu khả thi, thiết kế xây dựng và các quy định sau:
> a) Chủ đầu tư dự án có trách nhiệm lựa chọn tổ chức kinh doanh dịch vụ thẩm tra an toàn giao thông đủ điều kiện để thực hiện thẩm tra an toàn giao thông trong giai đoạn lập dự án đầu tư, thiết kế triển khai sau thiết kế cơ sở. Trường hợp thuê tư vấn thẩm tra dự án, thiết kế triển khai sau thiết kế cơ sở mà tư vấn thẩm tra dự án, thiết kế có đủ điều kiện năng lực về thẩm tra an toàn giao thông đường bộ thì có thể được lựa chọn để thực hiện thẩm tra an toàn giao thông dự án, thiết kế triển khai sau thiết kế cơ sở.
> b) Người có thẩm quyền quyết định phê duyệt dự án đầu tư, duyệt thiết kế thực hiện thẩm định an toàn giao thông trên cơ sở báo cáo thẩm tra an toàn giao thông của tổ chức tư vấn thẩm tra an toàn giao thông cùng với công tác thẩm định dự án đầu tư xây dựng công trình đường bộ, thẩm định thiết kế công trình đường bộ triển khai sau thiết kế cơ sở để điều chỉnh, bổ sung các hạng …


**Sau mốc (2026-07-01)** · chunk `ND165-2024/D32/K1#2026-07-01` · hiệu lực 2026-07-01 → nay

> Điều 32. Thẩm tra, thẩm định an toàn giao thông đường bộ
> 1. Trong giai đoạn lập dự án đầu tư, thiết kế triển khai sau thiết kế cơ sở, việc thẩm tra, thẩm định an toàn giao thông đường bộ được thực hiện cùng công tác thẩm tra, thẩm định báo cáo nghiên cứu khả thi, thiết kế xây dựng và các quy định sau:
> a) Chủ đầu tư dự án có trách nhiệm lựa chọn tổ chức kinh doanh dịch vụ thẩm tra an toàn giao thông đủ điều kiện để thực hiện thẩm tra an toàn giao thông trong giai đoạn lập dự án đầu tư, thiết kế triển khai sau thiết kế cơ sở. Trường hợp thuê tư vấn thẩm tra dự án, thiết kế triển khai sau thiết kế cơ sở mà tư vấn thẩm tra dự án, thiết kế có đủ điều kiện năng lực về thẩm tra an toàn giao thông đường bộ thì có thể được lựa chọn để thực hiện thẩm tra an toàn giao thông dự án, thiết kế triển khai sau thiết kế cơ sở.
> b) Người có thẩm quyền quyết định phê duyệt dự án đầu tư, duyệt thiết kế tổ chức thực hiện hoặc giao cơ quan thẩm định dự án, thẩm định thiết kế thực hiện thẩm định an toàn giao thông trên cơ sở báo cáo thẩm tra an toàn giao thông của tổ chức tư vấn thẩm tra an toàn giao thông cùng với công tác thẩm định dự án đầu tư xây dựng công trình đường bộ, thẩm định thiết kế công trình …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-06-30", "question_type": "theo_thoi_diem", "tier": "B", "answer": "", "gold_units": ["ND165-2024/D32/K1"], "required_numbers": [], "pair_id": "p-017"}
{"qid": "", "question": "", "as_of": "2026-07-01", "question_type": "theo_thoi_diem", "tier": "B", "answer": "", "gold_units": ["ND165-2024/D32/K1"], "required_numbers": [], "pair_id": "p-017"}
```

### W-theo_thoi_diem-018 · tier A · ND168-2024/D14/K6

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · ngày đổi 2026-08-15

**Trước mốc (2026-08-14)** · chunk `ND168-2024/D14/K6#2025-01-01` · hiệu lực 2025-01-01 → 2026-08-14

> Điều 14. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy vi phạm quy định về điều kiện của phương tiện khi tham gia giao thông
> 6. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển xe thực hiện hành vi vi phạm còn bị áp dụng các biện pháp khắc phục hậu quả sau đây:
> a) Thực hiện hành vi quy định tại điểm đ khoản 2 Điều này buộc thay thế thiết bị đủ tiêu chuẩn an toàn kỹ thuật hoặc khôi phục tính năng kỹ thuật của thiết bị theo quy định;
> b) Thực hiện hành vi quy định tại điểm b khoản 2 Điều này buộc nộp lại chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe) đã bị tẩy xóa.

- BienPhapBoSung: buộc thay thế thiết bị đủ tiêu chuẩn an toàn kỹ thuật hoặc khôi phục tính năng kỹ thuật của thiết bị theo quy định (nêu tại ND168-2024/D14/K6/a)
- BienPhapBoSung: buộc nộp lại chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe) đã bị tẩy xóa (nêu tại ND168-2024/D14/K6/b)

**Sau mốc (2026-08-15)** · chunk `ND168-2024/D14/K6#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 14. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy vi phạm quy định về điều kiện của phương tiện khi tham gia giao thông
> 6. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển xe thực hiện hành vi vi phạm còn bị áp dụng các biện pháp khắc phục hậu quả sau đây:
> a) Thực hiện hành vi quy định tại khoản 1; điểm d, điểm đ khoản 2 Điều này buộc thay thế thiết bị đủ tiêu chuẩn an toàn kỹ thuật hoặc khôi phục tính năng kỹ thuật của thiết bị theo quy định;
> b) Thực hiện hành vi quy định tại điểm b khoản 2 Điều này buộc nộp lại chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe) đã bị tẩy xóa.

- BienPhapBoSung: buộc thay thế thiết bị đủ tiêu chuẩn an toàn kỹ thuật hoặc khôi phục tính năng kỹ thuật của thiết bị theo quy định (nêu tại ND168-2024/D14/K6/a)
- BienPhapBoSung: buộc nộp lại chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe) đã bị tẩy xóa (nêu tại ND168-2024/D14/K6/b)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-08-14", "question_type": "theo_thoi_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D14/K6"], "required_numbers": [], "pair_id": "p-018"}
{"qid": "", "question": "", "as_of": "2026-08-15", "question_type": "theo_thoi_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D14/K6"], "required_numbers": [], "pair_id": "p-018"}
```

### W-theo_thoi_diem-019 · tier A · ND168-2024/D47/K5

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · ngày đổi 2026-08-15

**Trước mốc (2026-08-14)** · chunk `ND168-2024/D47/K5#2025-01-01` · hiệu lực 2025-01-01 → 2026-08-14

> Điều 47. Thủ tục xử phạt, nguyên tắc xử phạt đối với chủ phương tiện, người điều khiển phương tiện vi phạm quy định liên quan đến trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ
> 5. Đối với các hành vi vi phạm quy định về sử dụng lòng đường, vỉa hè vào mục đích khác, bảo vệ môi trường, chở người vượt quá quy định được phép chở của phương tiện, vi phạm quy định về tải trọng, khổ giới hạn của phương tiện, của đường bộ vi phạm về chằng buộc vận chuyển hàng hóa quy định tại Điều 12, Điều 17, Điều 20, Điều 21, Điều 26, Điều 32, Điều 34 của Nghị định này, người điều khiển phương tiện, chủ phương tiện, đơn vị kinh doanh vận tải, dịch vụ hỗ trợ vận tải, cá nhân, tổ chức vi phạm, xếp hàng lên xe ô tô thì buộc chấm dứt hành vi vi phạm theo quy định cụ thể sau đây:
> a) Thực hiện hành vi vi phạm quy định tại điểm g khoản 2; khoản 7; khoản 9; điểm a khoản 11; điểm b khoản 14 Điều 12 thì buộc thu dọn thóc, lúa, rơm, rạ, nông, lâm, hải sản, máy tuốt lúa trên đường bộ; thu dọn chướng ngại vật, vật cản khác, vật sắc nhọn, chất gây trơn trượt trên đường bộ, hàng hóa, vật tư, hóa chất, chất thải; thu dọn phương tiện, máy móc, thiết bị, biển hiệu, biển quảng cáo theo hướng dẫn của lực …


**Sau mốc (2026-08-15)** · chunk `ND168-2024/D47/K5#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 47. Thủ tục xử phạt, nguyên tắc xử phạt đối với chủ phương tiện, người điều khiển phương tiện vi phạm quy định liên quan đến trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ
> 5. Đối với các hành vi vi phạm quy định về sử dụng lòng đường, vỉa hè vào mục đích khác, bảo vệ môi trường, chở người vượt quá quy định được phép chở của phương tiện, vi phạm quy định về tải trọng, khổ giới hạn của phương tiện, của đường bộ vi phạm về chằng buộc vận chuyển hàng hóa quy định tại Điều 12, Điều 17, Điều 20, Điều 21, Điều 26, Điều 32, Điều 34 của Nghị định này, người điều khiển phương tiện, chủ phương tiện, đơn vị kinh doanh vận tải, dịch vụ hỗ trợ vận tải, cá nhân, tổ chức vi phạm, xếp hàng lên xe ô tô thì buộc chấm dứt hành vi vi phạm theo quy định cụ thể sau đây:
> a) Thực hiện hành vi vi phạm quy định tại điểm g khoản 2; khoản 7; khoản 9; điểm a khoản 11; điểm b khoản 14 Điều 12 thì buộc thu dọn thóc, lúa, rơm, rạ, nông, lâm, hải sản, máy tuốt lúa trên đường bộ; thu dọn chướng ngại vật, vật cản khác, vật sắc nhọn, chất gây trơn trượt trên đường bộ, hàng hóa, vật tư, hóa chất, chất thải; thu dọn phương tiện, máy móc, thiết bị, biển hiệu, biển quảng cáo theo hướng dẫn của lực …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-08-14", "question_type": "theo_thoi_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D47/K5"], "required_numbers": [], "pair_id": "p-019"}
{"qid": "", "question": "", "as_of": "2026-08-15", "question_type": "theo_thoi_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D47/K5"], "required_numbers": [], "pair_id": "p-019"}
```

### W-theo_thoi_diem-020 · tier A · ND168-2024/D46/K2

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · ngày đổi 2026-08-15

**Trước mốc (2026-08-14)** · chunk `ND168-2024/D46/K2#2025-01-01` · hiệu lực 2025-01-01 → 2026-08-14

> Điều 46. Thẩm quyền lập biên bản vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ
> 2. Công chức thuộc Thanh tra Sở Giao thông vận tải đang thi hành công vụ, nhiệm vụ có thẩm quyền lập biên bản đối với các hành vi vi phạm xảy ra trong phạm vi địa bàn quản lý của Thanh tra Sở Giao thông vận tải.


**Sau mốc (2026-08-15)** · chunk `ND168-2024/D46/K2#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 46. Thẩm quyền lập biên bản vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ
> 2. Công chức, viên chức đang thi hành công vụ, nhiệm vụ có thẩm quyền lập biên bản vi phạm hành chính đối với các hành vi vi phạm.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-08-14", "question_type": "theo_thoi_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D46/K2"], "required_numbers": [], "pair_id": "p-020"}
{"qid": "", "question": "", "as_of": "2026-08-15", "question_type": "theo_thoi_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D46/K2"], "required_numbers": [], "pair_id": "p-020"}
```

### W-theo_thoi_diem-021 · tier A · ND168-2024/D3/K3

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · ngày đổi 2026-08-15

**Trước mốc (2026-08-14)** · chunk `ND168-2024/D3/K3#2025-01-01` · hiệu lực 2025-01-01 → 2026-08-14

> Điều 3. Hình thức xử phạt vi phạm hành chính, biện pháp khắc phục hậu quả; thu hồi giấy phép, chứng chỉ hành nghề
> 3. Các biện pháp khắc phục hậu quả vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ bao gồm:
> a) Buộc khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra, trừ các biện pháp khắc phục hậu quả quy định tại điểm e, điểm n, điểm p khoản này;
> b) Buộc thực hiện biện pháp khắc phục tình trạng ô nhiễm môi trường do vi phạm hành chính gây ra;
> c) Buộc tái xuất phương tiện khỏi Việt Nam;
> d) Buộc nộp lại số lợi bất hợp pháp có được do thực hiện vi phạm hành chính;
> đ) Buộc phá dỡ các vật che khuất biển báo hiệu đường bộ, đèn tín hiệu giao thông;
> e) Buộc lắp đầy đủ thiết bị hoặc thay thế thiết bị đủ tiêu chuẩn, quy chuẩn an toàn kỹ thuật hoặc khôi phục lại tính năng kỹ thuật của phương tiện, thiết bị theo quy định hoặc tháo bỏ những thiết bị lắp thêm không đúng quy định;
> g) Buộc cấp thẻ nhận dạng lái xe cho lái xe theo quy định;
> h) Buộc tổ chức tập huấn, hướng dẫn nghiệp vụ, quy trình hoặc tổ chức khám sức khỏe định kỳ cho lái xe và nhân viên phục vụ trên xe theo quy định;
> i) Buộc lắp đặt thiết bị giám sát hành trình, thiết …


**Sau mốc (2026-08-15)** · chunk `ND168-2024/D3/K3#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 3. Hình thức xử phạt vi phạm hành chính, biện pháp khắc phục hậu quả; thu hồi giấy phép, chứng chỉ hành nghề
> 3. Các biện pháp khắc phục hậu quả vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ bao gồm:
> a) Buộc khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra, trừ các biện pháp khắc phục hậu quả quy định tại điểm e, điểm n, điểm p khoản này;
> b) Buộc thực hiện biện pháp khắc phục tình trạng ô nhiễm môi trường do vi phạm hành chính gây ra;
> c) Buộc tái xuất phương tiện khỏi Việt Nam;
> d) Buộc nộp lại số lợi bất hợp pháp có được do thực hiện vi phạm hành chính;
> đ) Buộc phá dỡ các vật che khuất biển báo hiệu đường bộ, đèn tín hiệu giao thông;
> e) Buộc lắp đầy đủ thiết bị hoặc thay thế thiết bị đủ tiêu chuẩn, quy chuẩn an toàn kỹ thuật hoặc khôi phục lại tính năng kỹ thuật của phương tiện, thiết bị theo quy định hoặc tháo bỏ những thiết bị lắp thêm không đúng quy định;
> g) Buộc cấp thẻ nhận dạng lái xe cho lái xe theo quy định;
> h) Buộc tổ chức tập huấn, hướng dẫn nghiệp vụ, quy trình hoặc tổ chức khám sức khỏe định kỳ cho lái xe và nhân viên phục vụ trên xe theo quy định;
> i) Buộc lắp đặt thiết bị giám sát hành trình, thiết …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-08-14", "question_type": "theo_thoi_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D3/K3"], "required_numbers": [], "pair_id": "p-021"}
{"qid": "", "question": "", "as_of": "2026-08-15", "question_type": "theo_thoi_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D3/K3"], "required_numbers": [], "pair_id": "p-021"}
```

### W-theo_thoi_diem-022 · tier A · ND168-2024/D44/K3

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · ngày đổi 2026-08-15

**Trước mốc (2026-08-14)** · chunk `ND168-2024/D44/K3#2025-01-01` · hiệu lực 2025-01-01 → 2026-08-14

> Điều 44. Thẩm quyền xử phạt của Thanh tra chuyên ngành
> 3. Chánh Thanh tra tỉnh, thành phố trực thuộc trung ương (trong trường hợp không thành lập Thanh tra Sở Giao thông vận tải) có quyền:
> a) Phạt cảnh cáo;
> b) Phạt tiền đến 52.500.000 đồng;
> c) Tước quyền sử dụng giấy phép, chứng chỉ hành nghề có thời hạn hoặc đình chỉ hoạt động có thời hạn;
> d) Tịch thu tang vật, phương tiện được sử dụng để vi phạm hành chính có giá trị không vượt quá 105.000.000 đồng;
> đ) Áp dụng các biện pháp khắc phục hậu quả quy định tại khoản 3 Điều 3 của Nghị định này.


**Sau mốc (2026-08-15)** · chunk `ND168-2024/D44/K3#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 44. Thẩm quyền xử phạt của Thanh tra chuyên ngành
> 3. Cục trưởng Cục Đường bộ Việt Nam, Trưởng đoàn kiểm tra do Bộ trưởng Bộ Xây dựng thành lập có quyền:
> a) Phạt cảnh cáo;
> b) Phạt tiền đến 75.000.000 đồng;
> c) Tước quyền sử dụng giấy phép có thời hạn hoặc đình chỉ hoạt động có thời hạn;
> d) Áp dụng các biện pháp khắc phục hậu quả quy định tại khoản 3 Điều 3 Nghị định này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-08-14", "question_type": "theo_thoi_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D44/K3"], "required_numbers": [], "pair_id": "p-022"}
{"qid": "", "question": "", "as_of": "2026-08-15", "question_type": "theo_thoi_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D44/K3"], "required_numbers": [], "pair_id": "p-022"}
```

### W-theo_thoi_diem-023 · tier A · ND168-2024/D26/K1

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · ngày đổi 2026-08-15

**Trước mốc (2026-08-14)** · chunk `ND168-2024/D26/K1#2025-01-01` · hiệu lực 2025-01-01 → 2026-08-14

> Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
> 1. Phạt tiền từ 500.000 đồng đến 1.000.000 đồng đối với cá nhân, từ 1.000.000 đồng đến 2.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
> a) Xếp hàng hóa lên mỗi xe ô tô (kể cả rơ moóc và sơ mi rơ moóc) vượt quá trọng tải (khối lượng hàng chuyên chở) cho phép tham gia giao thông được ghi trong giấy chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe trên 10% đến 50% (trừ xe xi téc chở chất lỏng), trên 20% đến 50% đối với xe xi téc chở chất lỏng;
> b) Xếp hàng hóa lên xe ô tô mà không ký xác nhận việc xếp hàng hóa vào giấy vận tải theo quy định.

- CheTai phat_tien: 500.000–1.000.000 đồng (nêu tại ND168-2024/D26/K1)
- CheTai phat_tien: 1.000.000–2.000.000 đồng (nêu tại ND168-2024/D26/K1)

**Sau mốc (2026-08-15)** · chunk `ND168-2024/D26/K1#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
> 1. Phạt tiền từ 500.000 đồng đến 1.000.000 đồng đối với cá nhân, từ 1.000.000 đồng đến 2.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
> a) Xếp hàng hóa lên mỗi xe ô tô (kể cả rơ moóc và sơ mi rơ moóc) vượt quá trọng tải (khối lượng hàng chuyên chở) cho phép tham gia giao thông được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe trên 10% đến 50% (trừ xe xi téc chở chất lỏng), trên 20% đến 50% đối với xe xi téc chở chất lỏng;
> b) Xếp hàng hóa lên xe ô tô mà không ký xác nhận việc xếp hàng hóa vào giấy vận tải theo quy định.

- CheTai phat_tien: 500.000–1.000.000 đồng (nêu tại ND168-2024/D26/K1)
- CheTai phat_tien: 1.000.000–2.000.000 đồng (nêu tại ND168-2024/D26/K1)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-08-14", "question_type": "theo_thoi_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D26/K1"], "required_numbers": [], "pair_id": "p-023"}
{"qid": "", "question": "", "as_of": "2026-08-15", "question_type": "theo_thoi_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D26/K1"], "required_numbers": [], "pair_id": "p-023"}
```

### W-theo_thoi_diem-024 · tier A · ND168-2024/D8/K6

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · ngày đổi 2026-08-15

**Trước mốc (2026-08-14)** · chunk `ND168-2024/D8/K6#2025-01-01` · hiệu lực 2025-01-01 → 2026-08-14

> Điều 8. Xử phạt người điều khiển xe máy chuyên dùng vi phạm quy tắc giao thông đường bộ
> 6. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Chạy quá tốc độ quy định trên 20 km/h;
> b) Dừng xe, đỗ xe trên đường cao tốc không đúng nơi quy định; không có báo hiệu bằng đèn khẩn cấp khi gặp sự cố kỹ thuật hoặc bất khả kháng khác buộc phải dừng xe, đỗ xe ở làn dừng xe khẩn cấp trên đường cao tốc; không có báo hiệu bằng đèn khẩn cấp, không đặt biển cảnh báo “Chú ý xe đỗ” (hoặc đèn cảnh báo) về phía sau xe khoảng cách tối thiểu 150 mét khi gặp sự cố kỹ thuật hoặc bất khả kháng khác buộc phải dừng xe, đỗ xe trên một phần làn đường xe chạy trên đường cao tốc;
> c) Điều khiển xe trên đường mà trong máu hoặc hơi thở có nồng độ cồn nhưng chưa vượt quá 50 miligam/100 mililít máu hoặc chưa vượt quá 0,25 miligam/1 lít khí thở;
> d) Đi vào khu vực cấm, đường có biển báo hiệu có nội dung cấm đi vào đối với loại phương tiện đang điều khiển, trừ các hành vi vi phạm quy định tại điểm d khoản 7, điểm đ khoản 9 Điều này và các trường hợp xe ưu tiên đang đi làm nhiệm vụ khẩn cấp theo quy định;
> đ) Không đi bên phải theo chiều đi của …

- CheTai phat_tien: 3.000.000–5.000.000 đồng (nêu tại ND168-2024/D8/K6)

**Sau mốc (2026-08-15)** · chunk `ND168-2024/D8/K6#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 8. Xử phạt người điều khiển xe máy chuyên dùng vi phạm quy tắc giao thông đường bộ
> 6. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Chạy quá tốc độ quy định trên 20 km/h;
> b) Dừng xe, đỗ xe trên đường cao tốc không đúng nơi quy định; không có báo hiệu bằng đèn khẩn cấp khi gặp sự cố kỹ thuật hoặc bất khả kháng khác buộc phải dừng xe, đỗ xe ở làn dừng xe khẩn cấp hoặc dải dừng xe khẩn cấp trên đường cao tốc; không có báo hiệu bằng đèn khẩn cấp, không đặt biển cảnh báo “Chú ý xe đỗ” (hoặc đèn cảnh báo) về phía sau xe khoảng cách tối thiểu 150 mét khi gặp sự cố kỹ thuật hoặc bất khả kháng khác buộc phải dừng xe, đỗ xe trên một phần làn đường xe chạy trên đường cao tốc;
> c) Điều khiển xe trên đường mà trong máu hoặc hơi thở có nồng độ cồn nhưng chưa vượt quá 50 miligam/100 mililít máu hoặc chưa vượt quá 0,25 miligam/1 lít khí thở;
> d) Đi vào khu vực cấm, đường có biển báo hiệu có nội dung cấm đi vào đối với loại phương tiện đang điều khiển, trừ các hành vi vi phạm quy định tại điểm d khoản 7, điểm đ khoản 9 Điều này và các trường hợp xe ưu tiên đang đi làm nhiệm vụ khẩn cấp theo quy định;
> đ) Không đi …

- CheTai phat_tien: 3.000.000–5.000.000 đồng (nêu tại ND168-2024/D8/K6)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-08-14", "question_type": "theo_thoi_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D8/K6"], "required_numbers": [], "pair_id": "p-024"}
{"qid": "", "question": "", "as_of": "2026-08-15", "question_type": "theo_thoi_diem", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D8/K6"], "required_numbers": [], "pair_id": "p-024"}
```

### W-theo_thoi_diem-025 · tier B · ND130-2024/D9/K2

Nghị định số 130/2024/NĐ-CP (Quy định về thu phí sử dụng đường bộ cao tốc đối với phương tiện lưu thông trên tuyến đường bộ cao tốc thuộc sở hữu toàn dân do nhà nước đại diện chủ sở hữu và trực tiếp quản lý, khai thác) · trước mốc: chưa có hiệu lực · ngày đổi 2024-10-10

**Trước mốc (2024-10-09)**: chưa có hiệu lực (không có phiên bản).

**Sau mốc (2024-10-10)** · chunk `ND130-2024/D9/K2#2024-10-10` · hiệu lực 2024-10-10 → nay

> Điều 9. Phí, mức phí sử dụng đường cao tốc thuộc phạm vi quản lý của Bộ Giao thông vận tải
> 2. Mức phí sử dụng đường bộ cao tốc thu đối với phương tiện lưu thông trên tuyến đường bộ cao tốc thuộc phạm vi quản lý của Bộ Giao thông vận tải quy định tại Phụ lục kèm theo Nghị định này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2024-10-09", "question_type": "theo_thoi_diem", "tier": "B", "answer": "", "gold_units": [], "required_numbers": [], "pair_id": "p-025"}
{"qid": "", "question": "", "as_of": "2024-10-10", "question_type": "theo_thoi_diem", "tier": "B", "answer": "", "gold_units": ["ND130-2024/D9/K2"], "required_numbers": [], "pair_id": "p-025"}
```

## da_buoc — cần ≥ 2 điều khoản nối bằng dẫn chiếu / chế tài

### W-da_buoc-001 · tier A · LUAT36-2024/D39/K6

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15 · DAN_CHIEU → LUAT36-2024/D39/K6/a

`TT79-2024-BCA/D26/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 26. Thủ tục thu hồi chứng nhận đăng ký xe, biển số xe
> 2. Thực hiện thu hồi chứng nhận đăng ký xe, biển số xe bằng dịch vụ công trực tuyến một phần hoặc làm thủ tục trực tiếp tại cơ quan đăng ký xe
> a) Chủ xe kê khai giấy khai thu hồi chứng nhận đăng ký xe, biển số xe trên cổng dịch vụ công hoặc kê khai trực tiếp tại cơ quan đăng ký xe, nộp hồ sơ thu hồi theo quy định tại Điều 25 Thông tư này và nhận giấy hẹn trả kết quả theo quy định;
> b) Sau khi tiếp nhận, kiểm tra hồ sơ bảo đảm hợp lệ, cơ quan đăng ký xe cấp 02 bản chứng nhận thu hồi chứng nhận đăng ký xe, biển số xe theo quy định (01 bản trả cho chủ xe; 01 bản lưu hồ sơ xe). Đối với xe tạm nhập, tái xuất của các đối tượng được hưởng quyền ưu đãi miễn trừ ngoại giao cấp 03 bản chứng nhận thu hồi chứng nhận đăng ký xe, biển số xe (02 bản trả cho chủ xe để nộp cho cơ quan hải quan và cơ quan đăng ký xe, 01 bản lưu hồ sơ xe).
> Trường hợp thu hồi theo quy định tại điểm a, điểm b khoản 6 Điều 39 Luật Trật tự, an toàn giao thông đường bộ thì chứng nhận thu hồi chứng nhận đăng ký xe, biển số xe có dán bản chà số máy, số khung và đóng dấu giáp lai của cơ quan đăng ký xe trên bản chà số máy, số khung xe.


`LUAT36-2024/D39/K6#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 39. Cấp, thu hồi chứng nhận đăng ký xe và biển số xe cơ giới, xe máy chuyên dùng tham gia giao thông đường bộ
> 6. Các trường hợp thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng bao gồm:
> a) Chuyển quyền sở hữu xe; trường hợp chuyển nhượng, trao đổi, tặng cho, để thừa kế xe gắn với biển số xe trúng đấu giá thì chỉ thu hồi chứng nhận đăng ký xe;
> b) Xe nhập khẩu được miễn thuế hoặc xe tạm nhập của cơ quan, tổ chức, cá nhân nước ngoài mà tái xuất, chuyển quyền sở hữu hoặc tiêu hủy; xe hết thời hạn đăng ký tại các khu kinh tế - thương mại đặc biệt, khu kinh tế cửa khẩu quốc tế;
> c) Xe đã đăng ký nhưng phát hiện hồ sơ xe bị làm giả hoặc có kết luận của cơ quan có thẩm quyền về việc thay đổi trái phép số khung, số máy; xe tháo máy để đăng ký sử dụng cho xe khác;
> d) Xe cơ giới hết niên hạn sử dụng, hư hỏng không sử dụng được;
> đ) Xe bị thải bỏ, bị mất không tìm được và chủ xe đề nghị thu hồi chứng nhận đăng ký xe, biển số xe;
> e) Việc cấp đăng ký, cấp biển số xe không đúng quy định của pháp luật.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["TT79-2024-BCA/D26/K2", "LUAT36-2024/D39/K6"], "required_numbers": []}
```

### W-da_buoc-002 · tier A · TT79-2024-BCA/D10/K3

Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng) · DAN_CHIEU → TT79-2024-BCA/D10

`TT79-2024-BCA/D16/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 16. Hồ sơ đăng ký sang tên xe
> 1. Hồ sơ thu hồi
> a) Giấy khai thu hồi chứng nhận đăng ký xe, biển số xe;
> b) Giấy tờ của chủ xe theo quy định tại Điều 10 Thông tư này;
> c) 02 bản chà số máy, số khung của xe;
> d) Bản sao chứng từ chuyển quyền sở hữu xe theo quy định;
> đ) Chứng nhận đăng ký xe, biển số xe; trường hợp mất chứng nhận đăng ký xe hoặc mất biển số xe thì phải ghi rõ lý do trong giấy khai thu hồi chứng nhận đăng ký xe, biển số xe.
> Trong thời gian chờ nhận kết quả thu hồi, chủ xe được giữ lại biển số xe để sử dụng và phải nộp lại khi nhận chứng nhận thu hồi; trường hợp chủ xe không nộp lại biển số xe thì cơ quan đăng ký xe hủy kết quả và yêu cầu chủ xe làm lại thủ tục thu hồi trong trường hợp mất biển số xe theo quy định.


`TT79-2024-BCA/D10/K1#2025-03-01` · hiệu lực 2025-03-01 → nay

> Điều 10. Giấy tờ của chủ xe
> 1. Chủ xe là người Việt Nam: Sử dụng tài khoản định danh điện tử mức độ 2 để thực hiện đăng ký xe trên cổng dịch vụ công hoặc ứng dụng định danh quốc gia hoặc xuất trình căn cước hoặc thẻ căn cước công dân, hộ chiếu;
> Đối với lực lượng vũ trang: Xuất trình giấy chứng minh Công an nhân dân hoặc chứng minh Quân đội nhân dân hoặc giấy xác nhận của thủ trưởng cơ quan, đơn vị công tác từ cấp trung đoàn, phòng, hoặc tương đương trở lên (trường hợp chưa được cấp giấy chứng minh của lực lượng vũ trang).


`TT79-2024-BCA/D10/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 10. Giấy tờ của chủ xe
> 2. Chủ xe là người nước ngoài
> a) Chủ xe là thành viên cơ quan đại diện ngoại giao, cơ quan lãnh sự, cơ quan đại diện của tổ chức quốc tế tại Việt Nam: Xuất trình chứng minh thư ngoại giao, chứng minh thư công vụ, chứng minh thư lãnh sự, chứng minh thư lãnh sự danh dự, chứng minh thư (phổ thông), còn giá trị sử dụng và nộp giấy giới thiệu của Cục Lễ tân Nhà nước, Bộ Ngoại giao hoặc Sở Ngoại vụ;
> b) Trường hợp chủ xe là người nước ngoài sinh sống và làm việc tại Việt Nam (trừ đối tượng quy định tại điểm a Khoản này): Xuất trình thẻ thường trú hoặc thẻ tạm trú (còn thời hạn cư trú tại Việt Nam từ 06 tháng trở lên).


`TT79-2024-BCA/D10/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 10. Giấy tờ của chủ xe
> 3. Chủ xe là tổ chức
> a) Chủ xe là tổ chức (trừ đối tượng quy định tại điểm b khoản 3 Điều này): Sử dụng tài khoản định danh điện tử mức độ 2 để thực hiện thủ tục đăng ký xe trên cổng dịch vụ công; trường hợp tổ chức chưa được cấp tài khoản định danh điện tử mức độ 2 thì xuất trình thông báo mã số thuế hoặc quyết định thành lập.
> Trường hợp xe hoạt động kinh doanh vận tải bằng ô tô thì phải có thêm bản sao giấy phép kinh doanh vận tải bằng ô tô do Sở Giao thông vận tải cấp kèm theo bản chính để đối chiếu; trường hợp xe của tổ chức, cá nhân khác thì phải có hợp đồng thuê phương tiện hoặc hợp đồng hợp tác kinh doanh hoặc hợp đồng dịch vụ.
> Trường hợp xe của doanh nghiệp quân đội phải có Giấy giới thiệu của Cục Xe - Máy, Bộ Quốc phòng;
> b) Chủ xe là cơ quan đại diện ngoại giao, cơ quan lãnh sự và cơ quan đại diện của tổ chức quốc tế tại Việt Nam: Giấy giới thiệu của Cục Lễ tân Nhà nước, Bộ Ngoại giao hoặc Sở Ngoại vụ;
> c) Người được cơ quan, tổ chức giới thiệu đi làm thủ tục thì phải nộp giấy tờ của chủ xe theo quy định và xuất trình giấy tờ tùy thân theo quy định tại khoản 1, khoản 2 Điều này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["TT79-2024-BCA/D16/K1", "TT79-2024-BCA/D10"], "required_numbers": []}
```

### W-da_buoc-003 · tier A · ND151-2024/D19/K1

Nghị định số 151/2024/NĐ-CP (Quy định chi tiết một số điều và biện pháp thi hành Luật Trật tự, an toàn giao thông đường bộ) · DAN_CHIEU → ND151-2024/PL1

`ND151-2024/D19/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 19. Tín hiệu, yêu cầu kỹ thuật đối với thiết bị phát tín hiệu của xe ưu tiên
> 1. Tín hiệu, yêu cầu kỹ thuật đối với thiết bị phát tín hiệu của xe ưu tiên bao gồm:
> a) Đối với đèn phát tín hiệu ưu tiên, tín hiệu được sử dụng: đèn nhấp nháy màu đỏ, đèn nhấp nháy màu xanh, đèn nhấp nháy màu xanh và đỏ theo yêu cầu kỹ thuật quy định tại Phụ lục I kèm theo Nghị định này;
> b) Đối với còi phát tín hiệu ưu tiên, tín hiệu được sử dụng theo yêu cầu kỹ thuật quy định tại Phụ lục I kèm theo Nghị định này;
> c) Đối với cờ hiệu ưu tiên, yêu cầu kỹ thuật thực hiện theo quy định tại Phụ lục I kèm theo Nghị định này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["ND151-2024/D19/K1", "ND151-2024/PL1"], "required_numbers": []}
```

### W-da_buoc-004 · tier A · TT79-2024-BCA/D17/K2

Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng) · DAN_CHIEU → TT79-2024-BCA/D17

`TT79-2024-BCA/D33/K12#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 33. Giải quyết một số trường hợp khi đăng ký, cấp biển số xe
> 12. Xe đã đăng ký của các doanh nghiệp đã giải thể nay thanh lý tài sản thì người mua xe thực hiện đăng ký sang tên xe theo quy định tại Điều 16 và Điều 17 Thông tư này, kèm theo:
> a) Chứng nhận đăng ký xe;
> b) Quyết định giải thể của cấp có thẩm quyền hoặc bản sao quyết định thu hồi giấy chứng nhận đăng ký doanh nghiệp.


`TT79-2024-BCA/D17/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 17. Thủ tục đăng ký sang tên xe
> 1. Thủ tục thu hồi
> a) Chủ xe kê khai giấy khai thu hồi chứng nhận đăng ký xe, biển số xe trên cổng dịch vụ công, cung cấp mã hồ sơ đăng ký xe trực tuyến hoặc kê khai giấy khai thu hồi chứng nhận đăng ký xe, biển số xe (theo mẫu ĐKX11 ban hành kèm theo Thông tư này) tại cơ quan đăng ký xe; nộp hồ sơ thu hồi quy định tại khoản 1 Điều 16 Thông tư này và nhận giấy hẹn trả kết quả chứng nhận thu hồi chứng nhận đăng ký xe, biển số xe theo quy định;
> b) Sau khi kiểm tra hồ sơ xe hợp lệ, cơ quan đăng ký xe cấp 02 bản chứng nhận thu hồi chứng nhận đăng ký xe, biển số xe theo quy định có dán bản chà số máy, số khung và đóng dấu giáp lai của cơ quan đăng ký xe trên bản chà số máy, số khung xe (01 bản trả cho chủ xe, 01 bản lưu hồ sơ xe). Đối với xe tạm nhập, tái xuất của các đối tượng được hưởng quyền ưu đãi miễn trừ ngoại giao cấp 03 bản chứng nhận thu hồi chứng nhận đăng ký xe, biển số xe (02 bản trả cho chủ xe để nộp cho cơ quan hải quan và cơ quan đăng ký xe, 01 bản lưu hồ sơ xe).
> Trường hợp chủ xe có nhu cầu thì được cấp chứng nhận đăng ký xe tạm thời cùng với chứng nhận thu hồi chứng nhận đăng ký xe, biển số xe, không phải có hồ sơ đăng ký xe tạm …


`TT79-2024-BCA/D17/K2#2025-03-01` · hiệu lực 2025-03-01 → nay

> Điều 17. Thủ tục đăng ký sang tên xe
> 2. Thủ tục đăng ký
> a) Tổ chức, cá nhân nhận chuyển quyền sở hữu xe kê khai giấy khai đăng ký xe theo quy định tại Điều 9 Thông tư này; đưa xe đến để kiểm tra và nộp hồ sơ theo quy định tại khoản 2 Điều 16 Thông tư này;
> b) Sau khi kiểm tra hồ sơ xe, thực tế xe đảm bảo hợp lệ thì được cơ quan đăng ký xe cấp chứng nhận đăng ký xe, biển số xe theo quy định tại điểm b khoản 2 Điều 14 Thông tư này;
> c) Nhận giấy hẹn trả kết quả, nộp lệ phí đăng ký xe và nhận biển số xe (trường hợp được cấp biển số xe theo quy định tại điểm c khoản 2 Điều 14 Thông tư này); trường hợp chủ xe có nhu cầu nhận trả kết quả đăng ký xe qua dịch vụ bưu chính thì đăng ký với đơn vị dịch vụ bưu chính;
> d) Nhận chứng nhận đăng ký xe tại cơ quan đăng ký xe hoặc từ đơn vị dịch vụ bưu chính.
> Trường hợp biển số xe đã được cấp là biển 3 số hoặc biển 4 số thì đổi sang biển số định danh theo quy định tại Thông tư này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["TT79-2024-BCA/D33/K12", "TT79-2024-BCA/D17"], "required_numbers": []}
```

### W-da_buoc-005 · tier A · ND151-2024/D25a/K1

Nghị định số 151/2024/NĐ-CP (Quy định chi tiết một số điều và biện pháp thi hành Luật Trật tự, an toàn giao thông đường bộ) · DAN_CHIEU → ND151-2024/PL3

`ND151-2024/D25a/K1#2026-07-01` · hiệu lực 2026-07-01 → nay

> Điều 25a. Trình tự, thủ tục cấp phép hoạt động phương tiện giao thông thông minh
> 1. Trình tự, thủ tục cấp phép hoạt động:
> a) Cơ quan, tổ chức, cá nhân là chủ sở hữu phương tiện chuẩn bị 01 bộ hồ sơ quy định tại khoản 2 Điều 25 Nghị định này và nộp cho cơ quan có thẩm quyền cấp phép hoạt động thông qua một trong các hình thức sau: nộp trực tuyến trên Cổng Dịch vụ công quốc gia hoặc Ứng dụng định danh quốc gia, qua dịch vụ bưu chính; nộp trực tiếp;
> b) Cơ quan cấp phép có trách nhiệm tiếp nhận, kiểm tra hồ sơ. Đối với hồ sơ, văn bản không đủ điều kiện cấp phép thì gửi thông báo đến tài khoản của cơ quan, tổ chức trên Cổng Dịch vụ công quốc gia, Ứng dụng định danh quốc gia hoặc có Phiếu yêu cầu bổ sung, hoàn thiện hồ sơ, Phiếu từ chối giải quyết hồ sơ thủ tục hành chính, nêu rõ lý do theo quy định.
> Trường hợp hồ sơ, văn bản nộp trực tiếp đủ điều kiện cấp phép thì tiếp nhận và lập Giấy tiếp nhận hồ sơ và hẹn trả kết quả;
> c) Trong thời hạn 05 ngày làm việc kể từ ngày tiếp nhận hồ sơ, cơ quan cấp phép có trách nhiệm cấp giấy phép hoạt động theo Mẫu số 03b Phụ lục III ban hành kèm theo Nghị định này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["ND151-2024/D25a/K1", "ND151-2024/PL3"], "required_numbers": []}
```

### W-da_buoc-006 · tier A · ND168-2024/D20/K6

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · DAN_CHIEU → ND168-2024/D20/K6/a

`ND168-2024/D23/K5#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 23. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển hàng hóa nguy hiểm
> 5. Phạt tiền từ 12.000.000 đồng đến 14.000.000 đồng đối với hành vi vận chuyển hàng hóa nguy hiểm không có giấy phép vận chuyển hàng hóa nguy hiểm hoặc có nhưng hết hiệu lực hoặc không thực hiện đúng quy định trong giấy phép vận chuyển hàng hóa nguy hiểm, trừ các hành vi vi phạm quy định tại điểm a khoản 6 Điều 20 của Nghị định này.

- BienPhapBoSung: buộc thực hiện các biện pháp khắc phục tình trạng ô nhiễm môi trường do vi phạm hành chính gây ra (nêu tại ND168-2024/D23/K6)
- CheTai phat_tien: 12.000.000–14.000.000 đồng (nêu tại ND168-2024/D23/K5)
- DiemGPLX: trừ 4 điểm (nêu tại ND168-2024/D23/K7/b)

`ND168-2024/D20/K6#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
> 6. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Vận chuyển hàng hóa nguy hiểm, hàng độc hại, dễ cháy, dễ nổ, động vật, hàng có mùi hôi thối hoặc hàng hóa khác ảnh hưởng đến sức khỏe của hành khách trên xe;
> b) Chở người trên mui xe, trong khoang chở hành lý của xe;
> c) Đe dọa, xúc phạm, tranh giành, lôi kéo hành khách; đe dọa, cưỡng ép hành khách sử dụng dịch vụ ngoài ý muốn; chuyển tải, xuống khách hoặc các hành vi khác nhằm trốn tránh phát hiện xe chở quá tải, quá số người theo quy định của pháp luật;
> d) Điều khiển xe ô tô kinh doanh vận tải, xe vận tải nội bộ quá thời gian quy định tại khoản 1 Điều 64 của Luật Trật tự, an toàn giao thông đường bộ; không thực hiện đúng quy định về thời gian nghỉ giữa hai lần lái xe liên tục của người lái xe;
> đ) Điều khiển xe kinh doanh vận tải hành khách, xe vận tải nội bộ không lắp thiết bị giám sát hành trình của xe theo quy định hoặc có lắp thiết bị giám sát hành trình của xe nhưng thiết …

- CheTai phat_tien: 3.000.000–5.000.000 đồng (nêu tại ND168-2024/D20/K6)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D20/K10/a)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D23/K5", "ND168-2024/D20/K6"], "required_numbers": [{"value": 12000000, "unit": "vnd"}, {"value": 14000000, "unit": "vnd"}, {"value": 4, "unit": "diem"}, {"value": 3000000, "unit": "vnd"}, {"value": 5000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}]}
```

### W-da_buoc-007 · tier A · TT79-2024-BCA/D8/K3

Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng) · DAN_CHIEU → TT79-2024-BCA/D8

`TT79-2024-BCA/D28/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 28. Hồ sơ đăng ký, cấp biển số xe trúng đấu giá
> 1. Đối với xe chưa đăng ký
> a) Giấy tờ đăng ký xe theo quy định tại Điều 8 Thông tư này;
> b) Quyết định xác nhận biển số xe trúng đấu giá do Cục Cảnh sát giao thông cấp, còn thời hạn sử dụng; trường hợp quá thời hạn thì phải có thêm Quyết định gia hạn thời hạn đăng ký biển số xe trúng đấu giá do Cục Cảnh sát giao thông cấp.


`TT79-2024-BCA/D8/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 8. Hồ sơ cấp mới chứng nhận đăng ký xe, biển số xe
> 1. Giấy khai đăng ký xe.


`TT79-2024-BCA/D8/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 8. Hồ sơ cấp mới chứng nhận đăng ký xe, biển số xe
> 2. Giấy tờ của chủ xe.


`TT79-2024-BCA/D8/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 8. Hồ sơ cấp mới chứng nhận đăng ký xe, biển số xe
> 3. Chứng nhận nguồn gốc xe.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["TT79-2024-BCA/D28/K1", "TT79-2024-BCA/D8"], "required_numbers": []}
```

### W-da_buoc-008 · tier A · ND151-2024/D32/K2

Nghị định số 151/2024/NĐ-CP (Quy định chi tiết một số điều và biện pháp thi hành Luật Trật tự, an toàn giao thông đường bộ) · DAN_CHIEU → ND151-2024/D32/K2

`ND151-2024/D33/K2#2026-07-01` · hiệu lực 2026-07-01 → nay

> Điều 33. Chấp thuận doanh nghiệp kinh doanh dịch vụ lữ hành quốc tế của Việt Nam được tổ chức cho người nước ngoài đưa xe cơ giới nước ngoài vào Việt Nam du lịch hoặc tổ chức, cá nhân đưa xe ô tô có tay lái ở bên phải vào tham gia giao thông tại Việt Nam không phải mục đích du lịch
> 2. Tổ chức, cá nhân theo quy định tại khoản 2 Điều 32 của Nghị định này gửi 01 bộ hồ sơ đến Cục Cảnh sát giao thông, Bộ Công an thông qua một trong các hình thức sau: trực tuyến trên Cổng Dịch vụ công quốc gia hoặc Ứng dụng định danh quốc gia; qua dịch vụ bưu chính; nộp trực tiếp. Hồ sơ bao gồm:
> a) Công hàm của cơ quan đại diện ngoại giao, cơ quan lãnh sự hoặc cơ quan đại diện của tổ chức quốc tế liên Chính phủ tại Việt Nam, nêu rõ lý do, mục đích cho phương tiện tham gia giao thông tại Việt Nam;
> b) Bản chính hoặc bản điện tử văn bản đề nghị chấp thuận kèm theo danh sách người điều khiển và thông tin về xe cơ giới theo Mẫu số 04a Phụ lục IV ban hành kèm theo Nghị định này.


`ND151-2024/D32/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 32. Xe cơ giới nước ngoài và người nước ngoài điều khiển phương tiện tham gia giao thông tại Việt Nam
> 2. Xe ô tô của người nước ngoài có tay lái ở bên phải tham gia giao thông tại Việt Nam không phải mục đích du lịch là xe ô tô chở người.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["ND151-2024/D33/K2", "ND151-2024/D32/K2"], "required_numbers": []}
```

### W-da_buoc-009 · tier A · LUAT36-2024/D64/K1

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15 · DAN_CHIEU → LUAT36-2024/D64/K1

`ND168-2024/D21/K5#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
> 5. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe (kể cả rơ moóc và sơ mi rơ moóc) chở hàng vượt trọng tải (khối lượng hàng chuyên chở) cho phép tham gia giao thông được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe trên 30% đến 50%;
> b) Điều khiển xe ô tô kinh doanh vận tải, xe vận tải nội bộ quá thời gian quy định tại khoản 1 Điều 64 của Luật Trật tự, an toàn giao thông đường bộ; không thực hiện đúng quy định về thời gian nghỉ giữa hai lần lái xe liên tục của người lái xe;
> c) Điều khiển xe ô tô kinh doanh vận tải, xe ô tô đầu kéo, xe vận tải nội bộ không lắp thiết bị giám sát hành trình hoặc có lắp thiết bị giám sát hành trình nhưng không có tác dụng trong quá trình xe tham gia giao thông theo quy định hoặc làm sai lệch dữ liệu của thiết bị giám sát hành trình lắp trên xe ô tô;".
> d) Điều khiển xe kéo …

- CheTai phat_tien: 3.000.000–5.000.000 đồng (nêu tại ND168-2024/D21/K5)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D21/K13/a)

`LUAT36-2024/D64/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 64. Thời gian làm việc của người lái xe ô tô kinh doanh vận tải và vận tải nội bộ
> 1. Thời gian lái xe của người lái xe ô tô không quá 10 giờ trong một ngày và không quá 48 giờ trong một tuần; lái xe liên tục không quá 04 giờ và bảo đảm các quy định có liên quan của Bộ luật Lao động.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D21/K5", "LUAT36-2024/D64/K1"], "required_numbers": [{"value": 3000000, "unit": "vnd"}, {"value": 5000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}]}
```

### W-da_buoc-010 · tier A · ND168-2024/D42/K2

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · DAN_CHIEU → ND168-2024/D42

`ND168-2024/D45/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 45. Nguyên tắc xác định thẩm quyền xử phạt vi phạm hành chính và áp dụng biện pháp khắc phục hậu quả
> 2. Thẩm quyền xử phạt vi phạm hành chính của các chức danh quy định tại Điều 42, Điều 43 và Điều 44 của Nghị định này là thẩm quyền áp dụng đối với một hành vi vi phạm hành chính của cá nhân; trong trường hợp phạt tiền, thẩm quyền xử phạt tổ chức gấp 02 lần thẩm quyền xử phạt cá nhân.


`ND168-2024/D42/K3#2025-01-01` · hiệu lực 2025-01-01 → 2026-08-14

> Điều 42. Thẩm quyền xử phạt của Chủ tịch Ủy ban nhân dân các cấp
> 3. Chủ tịch Ủy ban nhân dân cấp tỉnh có quyền:
> a) Phạt cảnh cáo;
> b) Phạt tiền đến 75.000.000 đồng;
> c) Tước quyền sử dụng giấy phép, chứng chỉ hành nghề có thời hạn hoặc đình chỉ hoạt động có thời hạn;
> d) Tịch thu tang vật, phương tiện được sử dụng để vi phạm hành chính;
> đ) Áp dụng biện pháp khắc phục hậu quả quy định tại khoản 3 Điều 3 của Nghị định này.


`ND168-2024/D42/K1#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 42. Thẩm quyền xử phạt của Chủ tịch Ủy ban nhân dân các cấp
> 1. Chủ tịch Ủy ban nhân dân cấp xã có quyền:
> a) Phạt cảnh cáo;
> b) Phạt tiền đến 37.500.000 đồng;
> c) Tước quyền sử dụng giấy phép, chứng chỉ hành nghề có thời hạn hoặc đình chỉ hoạt động có thời hạn;
> d) Tịch thu tang vật, phương tiện vi phạm hành chính;
> đ) Áp dụng biện pháp khắc phục hậu quả quy định tại khoản 3 Điều 3 của Nghị định này.


`ND168-2024/D42/K2#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 42. Thẩm quyền xử phạt của Chủ tịch Ủy ban nhân dân các cấp
> 2. Chủ tịch Ủy ban nhân dân cấp tỉnh có quyền:
> a) Phạt cảnh cáo;
> b) Phạt tiền đến 75.000.000 đồng;
> c) Tước quyền sử dụng giấy phép, chứng chỉ hành nghề có thời hạn hoặc đình chỉ hoạt động có thời hạn;
> d) Tịch thu tang vật, phương tiện vi phạm hành chính;
> đ) Áp dụng biện pháp khắc phục hậu quả quy định tại khoản 3 Điều 3 của Nghị định này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D45/K2", "ND168-2024/D42"], "required_numbers": []}
```

### W-da_buoc-011 · tier A · ND168-2024/D13/K11

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · BI_XU_PHAT → ND168-2024/D13/K11/a

`ND168-2024/D13/K5#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 13. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo), xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tư xe ô tô vi phạm quy định về điều kiện của phương tiện khi tham gia giao thông
> 5. Phạt tiền từ 3.000.000 đồng đến 4.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe có giấy chứng nhận hoặc tem kiểm định an toàn kỹ thuật và bảo vệ môi trường nhưng đã hết hiệu lực (hạn sử dụng) dưới 01 tháng (kể cả rơ moóc và sơ mi rơ moóc);
> b) Điều khiển xe không đủ hệ thống hàm hoặc có đủ hệ thống hãm nhưng không có tác dụng, không đúng tiêu chuẩn an toàn kỹ thuật (kể cả rơ moóc và sơ mi rơ moóc);
> c) Điều khiển xe kinh doanh vận tải có niên hạn sử dụng không bảo đảm điều kiện của hình thức kinh doanh đã đăng ký;
> d) Điều khiển xe lắp đặt, sử dụng còi vượt quá âm lượng theo quy định.

- BienPhapBoSung: buộc lắp đầy đủ thiết bị hoặc thay thế thiết bị đủ tiêu chuẩn, quy chuẩn an toàn kỹ thuật hoặc khôi phục lại tính năng kỹ thuật của thiết bị theo quy định (nêu tại ND168-2024/D13/K11/a)
- BienPhapBoSung: buộc thực hiện đúng quy định về biển số hoặc khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND168-2024/D13/K11/a)
- CheTai phat_tien: 3.000.000–4.000.000 đồng (nêu tại ND168-2024/D13/K5)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D13/K13/a)

`ND168-2024/D13/K11#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 13. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo), xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tư xe ô tô vi phạm quy định về điều kiện của phương tiện khi tham gia giao thông
> 11. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển xe thực hiện hành vi vi phạm còn bị áp dụng các biện pháp khắc phục hậu quả sau đây:
> a) Thực hiện hành vi quy định tại khoản 1; khoản 2; điểm b, điểm c khoản 3; điểm b khoản 4; điểm b, điểm d khoản 5; điểm b khoản 8 Điều này buộc lắp đầy đủ thiết bị hoặc thay thế thiết bị đủ tiêu chuẩn, quy chuẩn an toàn kỹ thuật hoặc khôi phục lại tính năng kỹ thuật của thiết bị theo quy định; buộc thực hiện đúng quy định về biển số hoặc khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra;
> b) Thực hiện hành vi quy định tại điểm a, điểm d khoản 3 Điều này buộc lắp đầy đủ thiết bị hoặc khôi phục lại tính năng kỹ thuật của thiết bị theo quy định, tháo bỏ những thiết bị lắp thêm không đúng quy định;
> c) Thực hiện hành vi quy định tại điểm c khoản 4 Điều này buộc khôi phục lại tình trạng ban đầu đã bị thay đổi do vi …

- BienPhapBoSung: buộc lắp đầy đủ thiết bị hoặc thay thế thiết bị đủ tiêu chuẩn, quy chuẩn an toàn kỹ thuật hoặc khôi phục lại tính năng kỹ thuật của thiết bị theo quy định (nêu tại ND168-2024/D13/K11/a)
- BienPhapBoSung: buộc thực hiện đúng quy định về biển số hoặc khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND168-2024/D13/K11/a)
- BienPhapBoSung: buộc lắp đầy đủ thiết bị hoặc khôi phục lại tính năng kỹ thuật của thiết bị theo quy định, tháo bỏ những thiết bị lắp thêm không đúng quy định (nêu tại ND168-2024/D13/K11/b)
- BienPhapBoSung: buộc khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND168-2024/D13/K11/c)
- BienPhapBoSung: buộc nộp lại chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe), giấy chứng nhận, tem kiểm định an toàn kỹ thuật và bảo vệ môi trường, chứng nhận đăng ký xe bị tẩy xóa (nêu tại ND168-2024/D13/K11/d)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D13/K5", "ND168-2024/D13/K11"], "required_numbers": [{"value": 3000000, "unit": "vnd"}, {"value": 4000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}]}
```

### W-da_buoc-012 · tier A · ND168-2024/D36/K2

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · DAN_CHIEU → ND168-2024/D36

`ND168-2024/D41/K2#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 41. Phân định thẩm quyền xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ
> 2. Cảnh sát giao thông trong phạm vi chức năng, nhiệm vụ được giao có thẩm quyền xử phạt đối với các hành vi vi phạm quy định tại các điểm, khoản, điều của Nghị định này như sau:
> a) Điều 6, Điều 7, Điều 8, Điều 9, Điều 10, Điều 11, Điều 12, Điều 13, Điều 14, Điều 15, Điều 16, Điều 17, Điều 18, Điều 19, Điều 20, Điều 21, Điều 22, Điều 23, Điều 24, Điều 25, Điều 26, Điều 27, Điều 28, Điều 29, Điều 30, Điều 31, Điều 32, Điều 33, Điều 34, Điều 35, Điều 36;
> b) Khoản 1, điểm a khoản 3, điểm b khoản 4, khoản 5 Điều 37;
> c) Điều 38;
> d) Điểm a, điểm b, điểm c, điểm d, điểm e khoản 1; điểm a khoản 2; điểm a, điểm b, điểm c, điểm g, điểm h, điểm i, điểm k khoản 3; điểm b, điểm d, điểm i, điểm k khoản 4; điểm đ, điểm e, điểm g, điểm h, điểm i, điểm k khoản 5; khoản 7; khoản 8 Điều 39.


`ND168-2024/D36/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 36. Xử phạt người điều khiển xe mô tô, xe gắn máy, xe thô sơ thực hiện hành vi vi phạm vận chuyển hành khách, hàng hóa
> 1. Phạt tiền từ 300.000 đồng đến 400.000 đồng đối với người điều khiển phương tiện thực hiện một trong các hành vi vi phạm sau đây:
> a) Vận chuyển hàng hóa mà sắp xếp, chằng buộc hàng hóa không bảo đảm an toàn hoặc gây nguy hiểm cho người, phương tiện tham gia giao thông;
> b) Vận chuyển hàng hóa trên xe gây cản trở tầm nhìn của người lái xe hoặc che khuất đèn, biển số xe (đối với loại xe có đèn, biển số xe); để rơi hàng hóa xuống đường.

- CheTai phat_tien: 300.000–400.000 đồng (nêu tại ND168-2024/D36/K1)

`ND168-2024/D36/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 36. Xử phạt người điều khiển xe mô tô, xe gắn máy, xe thô sơ thực hiện hành vi vi phạm vận chuyển hành khách, hàng hóa
> 2. Phạt tiền từ 400.000 đồng đến 600.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Chở hành lý, hàng hóa vượt quá khối lượng cho phép của xe;
> b) Chở hành lý, hàng hóa vượt quá khổ giới hạn cho phép của xe;
> c) Vận chuyển hàng rời, vật liệu xây dựng, phế thải để rơi vãi xuống đường hoặc gây ra tiếng ồn, bụi bẩn;
> d) Vận chuyển hàng hóa vượt phía trước, phía sau xe mà không có báo hiệu màu đỏ tại điểm đầu và điểm cuối cùng của hàng hóa khi xe hoạt động ban ngày; vận chuyển hàng hóa vượt phía trước, phía sau xe mà không có đèn hoặc báo hiệu khi xe hoạt động vào ban đêm hoặc khi trời tối.

- CheTai phat_tien: 400.000–600.000 đồng (nêu tại ND168-2024/D36/K2)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D41/K2", "ND168-2024/D36"], "required_numbers": [{"value": 300000, "unit": "vnd"}, {"value": 400000, "unit": "vnd"}, {"value": 600000, "unit": "vnd"}]}
```

### W-da_buoc-013 · tier A · LUAT35-2024/D17/K3

Luật Đường bộ số 35/2024/QH15 · DAN_CHIEU → LUAT35-2024/D17

`LUAT35-2024/D19/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 19. Xây dựng, lắp đặt công trình hạ tầng trong phạm vi bảo vệ kết cấu hạ tầng đường bộ
> 4. Đường dây tải điện, dây dẫn điện, đường dây thông tin, viễn thông xây dựng bên trên đường bộ không cần có văn bản chấp thuận của cơ quan quản lý đường bộ có thẩm quyền khi đáp ứng các quy định sau đây:
> a) Cột công trình hạ tầng nằm ngoài hành lang an toàn đường bộ;
> b) Chiều cao đường dây đi bên trên đường bộ đáp ứng quy định tại Điều 17 của Luật này;
> c) Đường dây không ảnh hưởng đến an toàn trong vận hành, khai thác công trình đường bộ.


`LUAT35-2024/D17/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 17. Phạm vi bảo vệ trên không và phía dưới đường bộ
> 1. Phạm vi bảo vệ trên không của phần đường theo phương thẳng đứng không thấp hơn chiều cao tĩnh không của đường. Đối với đoạn đường có dự phòng chiều cao tăng cường lớp mặt đường, chiều cao bù lún và các trường hợp cần dự phòng tôn cao mặt đường thì phải cộng chiều cao này với chiều cao tĩnh không.


`LUAT35-2024/D17/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 17. Phạm vi bảo vệ trên không và phía dưới đường bộ
> 2. Phạm vi bảo vệ trên không của cầu đường bộ được quy định như sau:
> a) Phạm vi bảo vệ trên không của cầu đường bộ tính từ điểm cao nhất của kết cấu trên các mặt cắt ngang cầu trở lên theo phương thẳng đứng là 02 mét nhưng không thấp hơn chiều cao tĩnh không quy định tại khoản 1 Điều này;
> b) Cầu đường bộ xây dựng vượt đường sắt, đường bộ khác phải bảo đảm tĩnh không của đường sắt, đường bộ bên dưới;
> c) Cầu đường bộ xây dựng trên khu vực có hoạt động giao thông đường thủy nội địa, giao thông hàng hải phải bảo đảm khổ thông thuyền cho tàu, thuyền lưu thông an toàn theo quy định của pháp luật về đường thủy nội địa và pháp luật về hàng hải.


`LUAT35-2024/D17/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 17. Phạm vi bảo vệ trên không và phía dưới đường bộ
> 3. Phạm vi bảo vệ công trình hầm đường bộ được xác định từ các bộ phận kết cấu của hầm đường bộ ra xung quanh đủ để bảo đảm an toàn đối với công trình, thiết bị lắp đặt vào công trình, an toàn trong vận hành, khai thác, sử dụng và bảo đảm tuổi thọ công trình theo thiết kế; phạm vi bảo vệ bên ngoài của hầm đường bộ là khoảng không đủ để bảo đảm an toàn cho vận hành, khai thác và sử dụng hầm đường bộ và các thiết bị của hầm đường bộ.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["LUAT35-2024/D19/K4", "LUAT35-2024/D17"], "required_numbers": []}
```

### W-da_buoc-014 · tier A · ND168-2024/D32/K18

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · BI_XU_PHAT → ND168-2024/D32/K18/b

`ND168-2024/D32/K8#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
> 8. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng đối với cá nhân, từ 8.000.000 đến 12.000.000 đồng đối với tổ chức là chủ xe mô tô, xe gắn máy và các loại xe tương tự xe mô tô, các loại xe tương tự xe gắn máy thực hiện một trong các hành vi vi phạm sau đây:
> a) Tẩy xóa, sửa chữa hoặc giả mạo hồ sơ đăng ký xe nhưng chưa đến mức truy cứu trách nhiệm hình sự;
> b) Tự ý thay đổi khung, máy, hình dáng, kích thước, đặc tính của xe;
> c) Khai báo không đúng sự thật hoặc sử dụng các giấy tờ, tài liệu giả để được cấp lại biển số xe, chứng nhận đăng ký xe nhưng chưa đến mức bị truy cứu trách nhiệm hình sự;
> d) Không làm thủ tục thu hồi chứng nhận đăng ký xe, biển số xe theo quy định;
> đ) Đưa phương tiện không có chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe) tham gia giao thông hoặc có nhưng đã hết hạn sử dụng, hết hiệu lực; đưa phương tiện có chứng nhận đăng ký xe tạm …

- BienPhapBoSung: buộc làm thủ tục đổi, thu hồi, cấp mới, cấp chứng nhận đăng ký xe, biển số xe, chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường theo quy định (trừ trường hợp bị tịch thu phương tiện) (nêu tại ND168-2024/D32/K19/g)
- BienPhapBoSung: buộc nộp lại chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe), giấy chứng nhận, tem kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe bị tẩy xóa (nêu tại ND168-2024/D32/K19/i)
- CheTai tich_thu: biển số (nêu tại ND168-2024/D32/K18/a)
- CheTai tich_thu: biển số, thiết bị thay đổi biển số (nêu tại ND168-2024/D32/K18/a)
- CheTai tich_thu: phương tiện (nêu tại ND168-2024/D32/K18/b)
- CheTai tich_thu: phương tiện) (nêu tại ND168-2024/D32/K19/g)
- CheTai phat_tien: 4.000.000–6.000.000 đồng (nêu tại ND168-2024/D32/K8)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D32/K21/a)
- DiemGPLX: trừ 6 điểm (nêu tại ND168-2024/D32/K21/đ)

`ND168-2024/D32/K18#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
> 18. Ngoài việc bị phạt tiền, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị áp dụng các hình thức xử phạt bổ sung như sau:
> a) Thực hiện hành vi quy định tại điểm g, điểm h khoản 8; điểm c khoản 12; điểm d khoản 13 Điều này bị tịch thu biển số; tịch thu biển số, thiết bị thay đổi biển số;
> b) Thực hiện hành vi quy định tại điểm đ, điểm e khoản 8; điểm đ khoản 9; điểm a khoản 12 Điều này trong trường hợp không có chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe) hoặc có chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe) nhưng không do cơ quan có thẩm quyền cấp, không đúng số khung, số động cơ (số máy) của xe hoặc bị tẩy xóa (kể cả rơ moóc và sơ mi rơ moóc) …

- CheTai tich_thu: biển số (nêu tại ND168-2024/D32/K18/a)
- CheTai tich_thu: biển số, thiết bị thay đổi biển số (nêu tại ND168-2024/D32/K18/a)
- CheTai tich_thu: phương tiện (nêu tại ND168-2024/D32/K18/b)
- CheTai tuoc_quyen: 1–3 tháng chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường và tem kiểm định của phương tiện (nêu tại ND168-2024/D32/K18/c)
- CheTai tuoc_quyen: 1–3 tháng chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường và tem kiểm định của phương tiện (nêu tại ND168-2024/D32/K18/d)
- CheTai tuoc_quyen: 1–3 tháng phù hiệu (nêu tại ND168-2024/D32/K18/đ)
- CheTai tuoc_quyen: 1–3 tháng phù hiệu (nêu tại ND168-2024/D32/K18/đ)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D32/K8", "ND168-2024/D32/K18"], "required_numbers": [{"value": 4000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}, {"value": 6, "unit": "diem"}, {"value": 1, "unit": "thang"}, {"value": 3, "unit": "thang"}]}
```

### W-da_buoc-015 · tier A · TT14-2025-BXD/D10/K3

Thông tư số 14/2025/TT-BXD (Quy định về đào tạo lái xe; bồi dưỡng, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ) · DAN_CHIEU → TT14-2025-BXD/D10

`TT14-2025-BXD/D9/K1#2025-09-01` · hiệu lực 2025-09-01 → nay

> Điều 9. Tài liệu phục vụ đào tạo và quản lý đào tạo của cơ sở đào tạo lái xe
> 1. Giáo trình đào tạo lái xe phù hợp với chương trình khung đào tạo lái xe quy định tại Phụ lục I ban hành kèm theo Thông tư này; cơ sở đào tạo lái xe thực hiện việc biên soạn, thẩm định, ban hành giáo trình đào tạo theo trình tự quy định tại Điều 10 Thông tư này.


`TT14-2025-BXD/D10/K1#2025-09-01` · hiệu lực 2025-09-01 → nay

> Điều 10. Trình tự biên soạn, thẩm định ban hành giáo trình và chương trình đào tạo
> 1. Biên soạn giáo trình đào tạo, chương trình chi tiết.


`TT14-2025-BXD/D10/K2#2025-09-01` · hiệu lực 2025-09-01 → nay

> Điều 10. Trình tự biên soạn, thẩm định ban hành giáo trình và chương trình đào tạo
> 2. Thẩm định giáo trình đào tạo, chương trình chi tiết.


`TT14-2025-BXD/D10/K3#2025-09-01` · hiệu lực 2025-09-01 → nay

> Điều 10. Trình tự biên soạn, thẩm định ban hành giáo trình và chương trình đào tạo
> 3. Ban hành giáo trình đào tạo, chương trình chi tiết.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["TT14-2025-BXD/D9/K1", "TT14-2025-BXD/D10"], "required_numbers": []}
```

### W-da_buoc-016 · tier A · LUAT35-2024/D45/K1

Luật Đường bộ số 35/2024/QH15 · DAN_CHIEU → LUAT35-2024/D45/K1

`LUAT35-2024/D50/K3#2024-10-01` · hiệu lực 2024-10-01 → nay

> Điều 50. Phí sử dụng đường cao tốc
> 3. Chính phủ quy định về điều kiện, thời điểm thực hiện việc thu phí sử dụng đường cao tốc; việc thu phí sử dụng đường cao tốc đối với đường cao tốc thuộc trường hợp quy định tại khoản 1 Điều này mà chưa đáp ứng quy định tại khoản 1 Điều 45 và khoản 2 Điều 47 của Luật này.


`LUAT35-2024/D45/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 45. Quy chuẩn, tiêu chuẩn kỹ thuật, ứng dụng khoa học và công nghệ đối với đường cao tốc
> 1. Đường cao tốc được thiết kế theo quy chuẩn, tiêu chuẩn kỹ thuật về đường cao tốc và các quy chuẩn, tiêu chuẩn kỹ thuật khác có liên quan.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["LUAT35-2024/D50/K3", "LUAT35-2024/D45/K1"], "required_numbers": []}
```

### W-da_buoc-017 · tier A · ND168-2024/D34/K6

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · BI_XU_PHAT → ND168-2024/D34/K6

`ND168-2024/D34/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 34. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển quá khổ giới hạn, xe quá tải trọng, xe bánh xích lưu hành đường bộ (kể cả xe ô tô chở hành khách)
> 2. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng đối với hành vi điều khiển xe mà tổng trọng lượng (khối lượng toàn bộ) của xe vượt quá tải trọng cho phép của đường bộ trên 10% đến 20%, trừ trường hợp có giấy phép lưu hành còn giá trị sử dụng.

- BienPhapBoSung: buộc khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND168-2024/D34/K6)
- CheTai phat_tien: 4.000.000–6.000.000 đồng (nêu tại ND168-2024/D34/K2)

`ND168-2024/D34/K6#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 34. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển quá khổ giới hạn, xe quá tải trọng, xe bánh xích lưu hành đường bộ (kể cả xe ô tô chở hành khách)
> 6. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm quy định tại khoản 1, khoản 2, khoản 3, khoản 4, khoản 5 Điều này nếu gây hư hại cầu, đường còn bị áp dụng biện pháp khắc phục hậu quả buộc khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra.

- BienPhapBoSung: buộc khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND168-2024/D34/K6)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D34/K2", "ND168-2024/D34/K6"], "required_numbers": [{"value": 4000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}]}
```

### W-da_buoc-018 · tier A · LUAT36-2024/D34/K2

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15 · DAN_CHIEU → LUAT36-2024/D34/K2

`TT53-2024-BGTVT/D6#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 6. Xe thô sơ
> Xe thô sơ gồm các loại xe được quy định tại khoản 2 Điều 34 Luật Trật tự, an toàn giao thông đường bộ.


`LUAT36-2024/D34/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 34. Phân loại phương tiện giao thông đường bộ
> 2. Xe thô sơ bao gồm:
> a) Xe đạp là xe có ít nhất hai bánh và vận hành do sức người thông qua bàn đạp hoặc tay quay;
> b) Xe đạp máy, gồm cả xe đạp điện, là xe đạp có trợ lực từ động cơ, nguồn động lực từ động cơ bị ngắt khi người lái xe dừng đạp hoặc khi xe đạt tới tốc độ 25 km/h;
> c) Xe xích lô;
> d) Xe lăn dùng cho người khuyết tật;
> đ) Xe vật nuôi kéo;
> e) Xe tương tự các loại xe quy định tại khoản này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["TT53-2024-BGTVT/D6", "LUAT36-2024/D34/K2"], "required_numbers": []}
```

### W-da_buoc-019 · tier A · LUAT36-2024/D57/K1

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15 · DAN_CHIEU → LUAT36-2024/D57/K1/c

`TT14-2025-BXD/D8/K2#2025-09-01` · hiệu lực 2025-09-01 → nay

> Điều 8. Tiêu chuẩn của cơ sở đào tạo lái xe mô tô
> 2. Xe tập lái: phù hợp với các hạng xe quy định tại điểm a, điểm b, điểm c khoản 1 Điều 57 Luật Trật tự, an toàn giao thông đường bộ.


`LUAT36-2024/D57/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 57. Giấy phép lái xe
> 1. Giấy phép lái xe bao gồm các hạng sau đây:
> a) Hạng A1 cấp cho người lái xe mô tô hai bánh có dung tích xi-lanh đến 125 cm3 hoặc có công suất động cơ điện đến 11 kW;
> b) Hạng A cấp cho người lái xe mô tô hai bánh có dung tích xi-lanh trên 125 cm3 hoặc có công suất động cơ điện trên 11 kW và các loại xe quy định cho giấy phép lái xe hạng A1;
> c) Hạng B1 cấp cho người lái xe mô tô ba bánh và các loại xe quy định cho giấy phép lái xe hạng A1;
> d) Hạng B cấp cho người lái xe ô tô chở người đến 08 chỗ (không kể chỗ của người lái xe); xe ô tô tải và ô tô chuyên dùng có khối lượng toàn bộ theo thiết kế đến 3.500 kg; các loại xe ô tô quy định cho giấy phép lái xe hạng B kéo rơ moóc có khối lượng toàn bộ theo thiết kế đến 750 kg;
> đ) Hạng C1 cấp cho người lái xe ô tô tải và ô tô chuyên dùng có khối lượng toàn bộ theo thiết kế trên 3.500 kg đến 7.500 kg; các loại xe ô tô tải quy định cho giấy phép lái xe hạng C1 kéo rơ moóc có khối lượng toàn bộ theo thiết kế đến 750 kg; các loại xe quy định cho giấy phép lái xe hạng B;
> e) Hạng C cấp cho người lái xe ô tô tải và ô tô chuyên dùng có khối lượng toàn bộ theo thiết kế trên 7.500 kg; các loại xe ô tô tải quy định cho giấy …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["TT14-2025-BXD/D8/K2", "LUAT36-2024/D57/K1"], "required_numbers": []}
```

### W-da_buoc-020 · tier A · LUAT36-2024/D34/K4

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15 · DAN_CHIEU → LUAT36-2024/D34/K4

`ND151-2024/D25/K1#2025-07-01` · hiệu lực 2025-07-01 → 2026-06-30

> Điều 25. Cấp phép hoạt động đối với phương tiện giao thông thông minh
> 1. Phương tiện giao thông thông minh là xe cơ giới quy định tại khoản 4 Điều 34 Luật Trật tự, an toàn giao thông đường bộ.
> Việc phân loại phương tiện giao thông thông minh cho phép tự động hóa một phần hoặc toàn bộ, chứng nhận chất lượng an toàn kỹ thuật và bảo vệ môi trường đối với phương tiện giao thông thông minh thực hiện theo quy định của Bộ trưởng Bộ Xây dựng.


`LUAT36-2024/D34/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 34. Phân loại phương tiện giao thông đường bộ
> 4. Phương tiện giao thông thông minh là xe cơ giới cho phép tự động hóa một phần hoặc toàn bộ hoạt động điều khiển phương tiện, xác định lộ trình và xử lý tình huống khi tham gia giao thông đường bộ.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-06-30", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["ND151-2024/D25/K1", "LUAT36-2024/D34/K4"], "required_numbers": []}
```

### W-da_buoc-021 · tier A · ND168-2024/D33/K4

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · BI_XU_PHAT → ND168-2024/D33/K4

`ND168-2024/D33/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 33. Xử phạt hành khách đi xe vi phạm quy định về trật tự, an toàn giao thông
> 2. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Mang hóa chất độc hại, chất dễ cháy, nổ, hàng nguy hiểm hoặc hàng cấm lưu thông trên xe chở khách;
> b) Đu, bám vào thành xe; đứng, ngồi, nằm trên mui xe, nóc xe, trong khoang chở hành lý; tự ý mở cửa xe hoặc có hành vi khác không bảo đảm an toàn khi xe đang chạy.

- CheTai phat_tien: 1.000.000–2.000.000 đồng (nêu tại ND168-2024/D33/K2)
- CheTai tich_thu: hóa chất độc hại, chất dễ cháy, nổ, hàng nguy hiểm, hàng cấm lưu thông mang theo trên xe chở khách (nêu tại ND168-2024/D33/K4)

`ND168-2024/D33/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 33. Xử phạt hành khách đi xe vi phạm quy định về trật tự, an toàn giao thông
> 4. Ngoài việc bị phạt tiền, người thực hiện hành vi vi phạm quy định tại điểm a khoản 2 Điều này còn bị áp dụng hình thức xử phạt bổ sung tịch thu hóa chất độc hại, chất dễ cháy, nổ, hàng nguy hiểm, hàng cấm lưu thông mang theo trên xe chở khách.

- CheTai tich_thu: hóa chất độc hại, chất dễ cháy, nổ, hàng nguy hiểm, hàng cấm lưu thông mang theo trên xe chở khách (nêu tại ND168-2024/D33/K4)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D33/K2", "ND168-2024/D33/K4"], "required_numbers": [{"value": 1000000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}]}
```

### W-da_buoc-022 · tier A · ND151-2024/D27/K1

Nghị định số 151/2024/NĐ-CP (Quy định chi tiết một số điều và biện pháp thi hành Luật Trật tự, an toàn giao thông đường bộ) · DAN_CHIEU → ND151-2024/D27/K1

`ND151-2024/D38/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 38. Hiệu lực thi hành
> 2. Kể từ ngày Nghị định này có hiệu lực thi hành, bãi bỏ các văn bản, điều, khoản trong các văn bản và các quy định sau đây:
> a) Nghị định số 109/2009/NĐ-CP ngày 01 tháng 12 năm 2009 của Chính phủ quy định tín hiệu của xe được quyền ưu tiên, Nghị định số 30/2024/NĐ-CP ngày 07 tháng 3 năm 2024 của Chính phủ quy định về quản lý phương tiện giao thông cơ giới đường bộ đăng ký tại nước ngoài, do người nước ngoài đưa vào Việt Nam du lịch, Nghị định số 80/2009/NĐ-CP ngày 01 tháng 10 năm 2009 của Chính phủ quy định xe ô tô của người nước ngoài đăng ký tại nước ngoài có tay lái bên phải tham gia giao thông tại Việt Nam;
> b) Điều 12, khoản 2 Điều 13, khoản 2 Điều 14, khoản 13 Điều 22, khoản 9 Điều 23, khoản 3 Điều 26, khoản 5, khoản 8 Điều 34 Nghị định số 10/2020/NĐ-CP ngày 17 tháng 01 năm 2020 của Chính phủ quy định về kinh doanh và điều kiện kinh doanh vận tải bằng xe ô tô (đã được sửa đổi, bổ sung tại Nghị định số 47/2022/NĐ-CP ngày 19 tháng 7 năm 2022 của Chính phủ, Nghị định số 41/2024/NĐ-CP ngày 16 tháng 4 năm 2024 của Chính phủ);
> c) Cụm từ “Thiết bị giám sát hành trình của xe ô tô” quy định tại khoản 4, cụm từ “Cung cấp, quản lý và sử dụng dữ liệu từ thiết …


`ND151-2024/D27/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 27. Thiết bị giám sát hành trình lắp trên xe ô tô kinh doanh vận tải, xe ô tô đầu kéo, xe cứu thương, xe cứu hộ giao thông đường bộ
> 1. Xe ô tô kinh doanh vận tải, xe ô tô đầu kéo, xe cứu thương, xe cứu hộ giao thông đường bộ phải lắp thiết bị giám sát hành trình bảo đảm yêu cầu kỹ thuật theo quy định của Quy chuẩn kỹ thuật quốc gia về thiết bị giám sát hành trình và thiết bị ghi nhận hình ảnh người lái xe.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["ND151-2024/D38/K2", "ND151-2024/D27/K1"], "required_numbers": []}
```

### W-da_buoc-023 · tier A · ND168-2024/D6/K15

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · BI_XU_PHAT → ND168-2024/D6/K15/b

`ND168-2024/D6/K12#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
> 12. Phạt tiền từ 40.000.000 đồng đến 50.000.000 đồng đối với người điều khiển xe thực hiện hành vi điều khiển xe lạng lách, đánh võng trên đường bộ; chạy quá tốc độ đuổi nhau trên đường bộ; dùng chân điều khiển vô lăng xe khi xe đang chạy trên đường bộ.

- CheTai phat_tien: 40.000.000–50.000.000 đồng (nêu tại ND168-2024/D6/K12)
- CheTai tuoc_quyen: 10–12 tháng giấy phép lái xe (nêu tại ND168-2024/D6/K15/b)

`ND168-2024/D6/K15#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
> 15. Ngoài việc bị phạt tiền, người điều khiển xe thực hiện hành vi vi phạm còn bị áp dụng các hình thức xử phạt bổ sung sau đây:
> a) Thực hiện hành vi quy định tại điểm e khoản 5 Điều này còn bị tịch thu thiết bị phát tín hiệu ưu tiên lắp đặt, sử dụng trái quy định;
> b) Thực hiện hành vi quy định tại khoản 12 Điều này bị tước quyền sử dụng giấy phép lái xe từ 10 tháng đến 12 tháng;
> c) Thực hiện hành vi quy định tại điểm a, điểm b, điểm c, điểm d khoản 11; khoản 13; khoản 14 Điều này bị tước quyền sử dụng giấy phép lái xe từ 22 tháng đến 24 tháng.

- CheTai tich_thu: thiết bị phát tín hiệu ưu tiên lắp đặt, sử dụng trái quy định (nêu tại ND168-2024/D6/K15/a)
- CheTai tuoc_quyen: 10–12 tháng giấy phép lái xe (nêu tại ND168-2024/D6/K15/b)
- CheTai tuoc_quyen: 22–24 tháng giấy phép lái xe (nêu tại ND168-2024/D6/K15/c)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D6/K12", "ND168-2024/D6/K15"], "required_numbers": [{"value": 40000000, "unit": "vnd"}, {"value": 50000000, "unit": "vnd"}, {"value": 10, "unit": "thang"}, {"value": 12, "unit": "thang"}, {"value": 22, "unit": "thang"}, {"value": 24, "unit": "thang"}]}
```

### W-da_buoc-024 · tier A · LUAT36-2024/D59/K1

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15 · DAN_CHIEU → LUAT36-2024/D59/K1/a

`LUAT36-2024/D56/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 56. Điều kiện của người điều khiển phương tiện tham gia giao thông đường bộ
> 4. Người lái xe gắn máy tham gia giao thông đường bộ phải hiểu biết quy tắc giao thông đường bộ, có kỹ năng điều khiển phương tiện; đủ điều kiện về độ tuổi, sức khỏe theo quy định tại điểm a khoản 1 và khoản 2 Điều 59 của Luật này.


`LUAT36-2024/D59/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 59. Tuổi, sức khỏe của người điều khiển phương tiện tham gia giao thông đường bộ
> 1. Độ tuổi của người lái xe, người điều khiển xe máy chuyên dùng được quy định như sau:
> a) Người đủ 16 tuổi trở lên được điều khiển xe gắn máy;
> b) Người đủ 18 tuổi trở lên được cấp giấy phép lái xe hạng A1, A, B1, B, C1, được cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ để điều khiển xe máy chuyên dùng tham gia giao thông đường bộ;
> c) Người đủ 21 tuổi trở lên được cấp giấy phép lái xe hạng C, BE;
> d) Người đủ 24 tuổi trở lên được cấp giấy phép lái xe hạng D1, D2, C1E, CE;
> đ) Người đủ 27 tuổi trở lên được cấp giấy phép lái xe hạng D, D1E, D2E, DE;
> e) Tuổi tối đa của người lái xe ô tô chở người (kể cả xe buýt) trên 29 chỗ (không kể chỗ của người lái xe), xe ô tô chở người giường nằm là đủ 57 tuổi đối với nam, đủ 55 tuổi đối với nữ.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D56/K4", "LUAT36-2024/D59/K1"], "required_numbers": []}
```

### W-da_buoc-025 · tier A · TT79-2024-BCA/D26/K2

Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng) · DAN_CHIEU → TT79-2024-BCA/D26

`TT79-2024-BCA/D33/K16#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 33. Giải quyết một số trường hợp khi đăng ký, cấp biển số xe
> 16. Xe tạm nhập, xe của dự án chưa hết hạn, chuyển nhượng tại Việt Nam
> a) Chủ xe làm thủ tục thu hồi tại cơ quan đăng ký xe theo quy định tại Điều 26 Thông tư này; sau đó đến cơ quan hải quan để làm thủ tục chuyển nhượng, nộp thuế theo quy định và nộp lại hồ sơ chuyển nhượng, chứng từ nộp lệ phí trước bạ xe cho cơ quan đăng ký xe để làm thủ tục đăng ký sang tên xe theo quy định;
> b) Trường hợp xe được cơ quan hải quan truy thu thuế hoặc cơ quan chức năng của Bộ Tài chính trả lời bằng văn bản không phải truy thu thuế thì được đăng ký sang tên xe, lưu văn bản đó vào hồ sơ xe.


`TT79-2024-BCA/D26/K1#2025-03-01` · hiệu lực 2025-03-01 → nay

> Điều 26. Thủ tục thu hồi chứng nhận đăng ký xe, biển số xe
> 1. Thực hiện thu hồi chứng nhận đăng ký xe, biển số xe bằng dịch vụ công trực tuyến toàn trình đối với xe cơ giới hết niên hạn sử dụng, hư hỏng không sử dụng được; xe bị thải bỏ, bị mất không tìm được và chủ xe đề nghị thu hồi chứng nhận đăng ký xe, biển số xe
> a) Chủ xe kê khai giấy khai thu hồi chứng nhận đăng ký xe, biển số xe trên cổng dịch vụ công và nộp chứng nhận đăng ký xe, biển số xe cho cơ quan đăng ký xe thông qua dịch vụ bưu chính;
> b) Sau khi tiếp nhận, kiểm tra hồ sơ bảo đảm hợp lệ, cơ quan đăng ký xe cấp chứng nhận thu hồi chứng nhận đăng ký xe, biển số xe, ký số và trả kết quả cho chủ xe trên cổng dịch vụ công.


`TT79-2024-BCA/D26/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 26. Thủ tục thu hồi chứng nhận đăng ký xe, biển số xe
> 2. Thực hiện thu hồi chứng nhận đăng ký xe, biển số xe bằng dịch vụ công trực tuyến một phần hoặc làm thủ tục trực tiếp tại cơ quan đăng ký xe
> a) Chủ xe kê khai giấy khai thu hồi chứng nhận đăng ký xe, biển số xe trên cổng dịch vụ công hoặc kê khai trực tiếp tại cơ quan đăng ký xe, nộp hồ sơ thu hồi theo quy định tại Điều 25 Thông tư này và nhận giấy hẹn trả kết quả theo quy định;
> b) Sau khi tiếp nhận, kiểm tra hồ sơ bảo đảm hợp lệ, cơ quan đăng ký xe cấp 02 bản chứng nhận thu hồi chứng nhận đăng ký xe, biển số xe theo quy định (01 bản trả cho chủ xe; 01 bản lưu hồ sơ xe). Đối với xe tạm nhập, tái xuất của các đối tượng được hưởng quyền ưu đãi miễn trừ ngoại giao cấp 03 bản chứng nhận thu hồi chứng nhận đăng ký xe, biển số xe (02 bản trả cho chủ xe để nộp cho cơ quan hải quan và cơ quan đăng ký xe, 01 bản lưu hồ sơ xe).
> Trường hợp thu hồi theo quy định tại điểm a, điểm b khoản 6 Điều 39 Luật Trật tự, an toàn giao thông đường bộ thì chứng nhận thu hồi chứng nhận đăng ký xe, biển số xe có dán bản chà số máy, số khung và đóng dấu giáp lai của cơ quan đăng ký xe trên bản chà số máy, số khung xe.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["TT79-2024-BCA/D33/K16", "TT79-2024-BCA/D26"], "required_numbers": []}
```

### W-da_buoc-026 · tier A · TT79-2024-BCA/D9/K3

Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng) · DAN_CHIEU → TT79-2024-BCA/D9

`TT79-2024-BCA/D21/K2#2025-03-01` · hiệu lực 2025-03-01 → nay

> Điều 21. Thủ tục cấp lại chứng nhận đăng ký xe, biển số xe
> 2. Chủ xe thực hiện dịch vụ công trực tuyến một phần hoặc làm thủ tục trực tiếp tại cơ quan đăng ký xe:
> a) Chủ xe kê khai giấy khai đăng ký xe theo quy định tại Điều 9 Thông tư này, nộp hồ sơ theo quy định tại khoản 1 và khoản 2 Điều 19 Thông tư này và nộp lệ phí theo quy định;
> b) Sau khi kiểm tra hồ sơ xe đảm bảo hợp lệ, cơ quan đăng ký xe thực hiện cấp lại chứng nhận đăng ký xe, biển số xe theo quy định; chủ xe nhận kết quả đăng ký xe tại cơ quan đăng ký xe hoặc từ dịch vụ bưu chính.


`TT79-2024-BCA/D9/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 9. Giấy khai đăng ký xe
> 1. Trường hợp thực hiện đăng ký xe bằng dịch vụ công trực tuyến một phần: Chủ xe đăng nhập trên cổng dịch vụ công và kê khai chính xác, đầy đủ, trung thực các nội dung quy định trong mẫu giấy khai đăng ký xe, ký số. Trường hợp không có ký số thì chủ xe in giấy khai đăng ký xe từ cổng dịch vụ công, ký, ghi rõ họ, tên và đóng dấu (nếu là cơ quan, tổ chức).


`TT79-2024-BCA/D9/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 9. Giấy khai đăng ký xe
> 2. Trường hợp thực hiện đăng ký xe lần đầu bằng dịch vụ công trực tuyến toàn trình: Chủ xe sử dụng tài khoản định danh điện tử mức độ 2 để đăng nhập vào cổng dịch vụ công hoặc ứng dụng định danh quốc gia và kê khai chính xác, đầy đủ, trung thực các nội dung quy định trong mẫu giấy khai đăng ký xe và chủ xe không cần ký.


`TT79-2024-BCA/D9/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 9. Giấy khai đăng ký xe
> 3. Trường hợp thực hiện đăng ký xe trực tiếp tại cơ quan đăng ký xe: Chủ xe kê khai chính xác, đầy đủ, trung thực các nội dung quy định trong mẫu giấy khai đăng ký xe.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["TT79-2024-BCA/D21/K2", "TT79-2024-BCA/D9"], "required_numbers": []}
```

### W-da_buoc-027 · tier A · TT14-2025-BXD/D13/K3

Thông tư số 14/2025/TT-BXD (Quy định về đào tạo lái xe; bồi dưỡng, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ) · DAN_CHIEU → TT14-2025-BXD/D13

`TT14-2025-BXD/D6/K3#2025-09-01` · hiệu lực 2025-09-01 → nay

> Điều 6. Đào tạo lái xe các hạng B, C1
> 3. Báo cáo đăng ký khóa đào tạo lái xe:
> a) Cơ sở đào tạo lái xe tiếp nhận hồ sơ của người học lái xe bảo đảm đủ điều kiện và thành phần hồ sơ theo quy định tại Điều 13, Điều 14 Thông tư này; lập báo cáo đăng ký khóa đào tạo lái xe kèm theo danh sách học viên và kế hoạch đào tạo theo quy định tại Mẫu số 01, Mẫu số 02, Mẫu số 03 Phụ lục III ban hành kèm theo Thông tư này gửi Sở Xây dựng bằng một trong các hình thức: trực tiếp, dịch vụ bưu chính, trên môi trường điện tử; đồng thời truyền dữ liệu qua Hệ thống thông tin quản lý, giám sát đào tạo lái xe;
> b) Báo cáo đăng ký khóa đào tạo lái xe, danh sách học viên, kế hoạch đào tạo phải có dấu giáp lai của cơ sở đào tạo lái xe và gửi đến Sở Xây dựng không quá 07 ngày làm việc kể từ ngày khai giảng; Thủ trưởng đơn vị được Sở Xây dựng giao nhiệm vụ quản lý đào tạo lái xe kiểm tra, ký tên vào từng trang (trừ hình thức tiếp nhận báo cáo trên môi trường điện tử).


`TT14-2025-BXD/D13/K1#2025-09-01` · hiệu lực 2025-09-01 → nay

> Điều 13. Yêu cầu đối với người học lái xe
> 1. Là công dân Việt Nam, người nước ngoài được phép cư trú hoặc đang làm việc, học tập tại Việt Nam.


`TT14-2025-BXD/D13/K2#2026-07-01` · hiệu lực 2026-07-01 → nay

> Điều 13. Yêu cầu đối với người học lái xe
> 2. Người học lái xe để nâng hạng giấy phép lái xe phải đáp ứng theo quy định tại khoản 4 Điều 60 Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15; trong đó, thời gian lái xe an toàn cho từng hạng giấy phép lái xe được quy định cụ thể như sau:
> a) Hạng B lên C1, B lên C, B lên D1, B lên BE, C1 lên C, C1 lên D1, C1 lên D2, C1 lên C1E, C lên D1, C lên D2, D1 lên D2, D1 lên D, D1 lên D1E, D2 lên D, D2 lên D2E, D lên CE, D lên DE: thời gian lái xe an toàn từ 02 năm trở lên;
> b) Hạng B lên D2, D1 lên CE, D2 lên CE, C lên CE, C lên D: thời gian lái xe an toàn từ 03 năm trở lên.


`TT14-2025-BXD/D13/K3#2025-09-01` · hiệu lực 2025-09-01 → nay

> Điều 13. Yêu cầu đối với người học lái xe
> 3. Người đã có giấy phép lái xe hạng B chuyển số tự động được đăng ký học để cấp mới giấy phép lái xe hạng B chuyển số cơ khí (số sàn), người đã có giấy phép lái xe hạng B được đăng ký học để cấp mới giấy phép lái xe hạng C1 theo quy định tại Điều 6 Thông tư này; hồ sơ của người học lái xe thực hiện theo quy định tại khoản 1 Điều 14 Thông tư này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["TT14-2025-BXD/D6/K3", "TT14-2025-BXD/D13"], "required_numbers": []}
```

### W-da_buoc-028 · tier A · ND168-2024/D3/K3

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · DAN_CHIEU → ND168-2024/D3/K3

`ND168-2024/D43/K4#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 43. Thẩm quyền xử phạt của Công an nhân dân
> 4. Trưởng Công an cấp xã có quyền:
> a) Phạt cảnh cáo;
> b) Phạt tiền đến 37.500.000 đồng;
> c) Tước quyền sử dụng giấy phép, chứng chỉ hành nghề có thời hạn hoặc đình chỉ hoạt động có thời hạn;
> d) Tịch thu tang vật, phương tiện vi phạm hành chính;
> đ) Áp dụng biện pháp khắc phục hậu quả quy định tại khoản 3 Điều 3 của Nghị định này.


`ND168-2024/D3/K3#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 3. Hình thức xử phạt vi phạm hành chính, biện pháp khắc phục hậu quả; thu hồi giấy phép, chứng chỉ hành nghề
> 3. Các biện pháp khắc phục hậu quả vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ bao gồm:
> a) Buộc khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra, trừ các biện pháp khắc phục hậu quả quy định tại điểm e, điểm n, điểm p khoản này;
> b) Buộc thực hiện biện pháp khắc phục tình trạng ô nhiễm môi trường do vi phạm hành chính gây ra;
> c) Buộc tái xuất phương tiện khỏi Việt Nam;
> d) Buộc nộp lại số lợi bất hợp pháp có được do thực hiện vi phạm hành chính;
> đ) Buộc phá dỡ các vật che khuất biển báo hiệu đường bộ, đèn tín hiệu giao thông;
> e) Buộc lắp đầy đủ thiết bị hoặc thay thế thiết bị đủ tiêu chuẩn, quy chuẩn an toàn kỹ thuật hoặc khôi phục lại tính năng kỹ thuật của phương tiện, thiết bị theo quy định hoặc tháo bỏ những thiết bị lắp thêm không đúng quy định;
> g) Buộc cấp thẻ nhận dạng lái xe cho lái xe theo quy định;
> h) Buộc tổ chức tập huấn, hướng dẫn nghiệp vụ, quy trình hoặc tổ chức khám sức khỏe định kỳ cho lái xe và nhân viên phục vụ trên xe theo quy định;
> i) Buộc lắp đặt thiết bị giám sát hành trình, thiết …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D43/K4", "ND168-2024/D3/K3"], "required_numbers": []}
```

### W-da_buoc-029 · tier A · ND168-2024/D3/K3

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · DAN_CHIEU → ND168-2024/D3/K3

`ND168-2024/D43/K3#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 43. Thẩm quyền xử phạt của Công an nhân dân
> 3. Trưởng đồn Công an, Thủ trưởng đơn vị Cảnh sát cơ động cấp tiểu đoàn, Trưởng trạm, Đội trưởng có quyền:
> a) Phạt cảnh cáo;
> b) Phạt tiền đến 22.500.000 đồng;
> c) Tước quyền sử dụng giấy phép, chứng chỉ hành nghề có thời hạn hoặc đình chỉ hoạt động có thời hạn;
> d) Tịch thu tang vật, phương tiện vi phạm hành chính có giá trị không vượt quá 45.000.000 đồng;
> đ) Áp dụng biện pháp khắc phục hậu quả quy định tại khoản 3 Điều 3 (trừ điểm c khoản 3 Điều 3) của Nghị định này.


`ND168-2024/D3/K3#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 3. Hình thức xử phạt vi phạm hành chính, biện pháp khắc phục hậu quả; thu hồi giấy phép, chứng chỉ hành nghề
> 3. Các biện pháp khắc phục hậu quả vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ bao gồm:
> a) Buộc khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra, trừ các biện pháp khắc phục hậu quả quy định tại điểm e, điểm n, điểm p khoản này;
> b) Buộc thực hiện biện pháp khắc phục tình trạng ô nhiễm môi trường do vi phạm hành chính gây ra;
> c) Buộc tái xuất phương tiện khỏi Việt Nam;
> d) Buộc nộp lại số lợi bất hợp pháp có được do thực hiện vi phạm hành chính;
> đ) Buộc phá dỡ các vật che khuất biển báo hiệu đường bộ, đèn tín hiệu giao thông;
> e) Buộc lắp đầy đủ thiết bị hoặc thay thế thiết bị đủ tiêu chuẩn, quy chuẩn an toàn kỹ thuật hoặc khôi phục lại tính năng kỹ thuật của phương tiện, thiết bị theo quy định hoặc tháo bỏ những thiết bị lắp thêm không đúng quy định;
> g) Buộc cấp thẻ nhận dạng lái xe cho lái xe theo quy định;
> h) Buộc tổ chức tập huấn, hướng dẫn nghiệp vụ, quy trình hoặc tổ chức khám sức khỏe định kỳ cho lái xe và nhân viên phục vụ trên xe theo quy định;
> i) Buộc lắp đặt thiết bị giám sát hành trình, thiết …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D43/K3", "ND168-2024/D3/K3"], "required_numbers": []}
```

### W-da_buoc-030 · tier A · TT14-2025-BXD/D23/K3

Thông tư số 14/2025/TT-BXD (Quy định về đào tạo lái xe; bồi dưỡng, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ) · DAN_CHIEU → TT14-2025-BXD/D23/K3/a

`TT14-2025-BXD/D29/K2#2025-09-01` · hiệu lực 2025-09-01 → nay

> Điều 29. Sở Xây dựng
> 2. Đối với công tác bồi dưỡng, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ:
> a) Cấp lại chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ theo quy định tại điểm a khoản 3 Điều 23 Thông tư này;
> b) Thực hiện tiếp nhận, rà soát, kiểm tra và thông báo danh sách cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ hoạt động trên địa bàn quản lý trên trang thông tin điện tử của Sở Xây dựng;
> c) Truy cập Hệ thống thông tin chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ tại Sở Xây dựng để quản lý, khai thác dữ liệu chứng chỉ bồi dưỡng pháp luật về giao thông đường bộ của các cơ sở bồi dưỡng thuộc quyền quản lý;
> d) Lập Sổ quản lý cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ theo mẫu quy định tại Phụ lục XXIV ban hành kèm theo Thông tư này.


`TT14-2025-BXD/D23/K3#2026-07-01` · hiệu lực 2026-07-01 → nay

> Điều 23. Cấp lại chứng chỉ
> 3. Trình tự thực hiện:
> a) Cá nhân nộp 01 bộ hồ sơ đến cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ đã cấp chứng chỉ; trường hợp cơ sở bồi dưỡng đã cấp chứng chỉ không còn hoạt động thì cá nhân nộp cho Sở Xây dựng nơi quản lý cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ đã cấp chứng chỉ tại Trung tâm Phục vụ hành chính công cấp tỉnh hoặc cấp xã bằng hình thức trực tiếp hoặc qua dịch vụ bưu chính hoặc qua cổng dịch vụ công quốc gia.
> b) Cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ hoặc Sở Xây dựng kiểm tra hồ sơ khi tiếp nhận; trường hợp chứng chỉ không thuộc đối tượng được cấp lại hoặc hồ sơ không đúng theo quy định, phải thông báo trực tiếp hoặc bằng văn bản những nội dung cần bổ sung hoặc sửa đổi cho cá nhân trong thời hạn 02 ngày làm việc, kể từ ngày nhận hồ sơ;
> c) Trong thời hạn 02 ngày làm việc, kể từ ngày nhận đủ hồ sơ hợp lệ, người đứng đầu cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ hoặc Sở Xây dựng cấp lại chứng chỉ; trường hợp không cấp lại chứng chỉ thì phải trả lời bằng văn bản và nêu rõ lý do;
> d) Việc trả chứng chỉ bản giấy được thực hiện tại cơ sở bồi dưỡng kiến thức pháp luật về giao …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["TT14-2025-BXD/D29/K2", "TT14-2025-BXD/D23/K3"], "required_numbers": []}
```

### W-da_buoc-031 · tier A · TT14-2025-BXD/D13/K3

Thông tư số 14/2025/TT-BXD (Quy định về đào tạo lái xe; bồi dưỡng, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ) · DAN_CHIEU → TT14-2025-BXD/D13

`TT14-2025-BXD/D7/K3#2025-09-01` · hiệu lực 2025-09-01 → nay

> Điều 7. Đào tạo nâng hạng giấy phép lái xe
> 3. Báo cáo đăng ký khóa đào tạo lái xe:
> a) Cơ sở đào tạo lái xe tiếp nhận hồ sơ của người học lái xe bảo đảm đủ điều kiện và thành phần hồ sơ theo quy định tại Điều 13, Điều 14 Thông tư này; lập báo cáo đăng ký khóa đào tạo lái xe kèm theo danh sách học viên và kế hoạch đào tạo theo quy định tại Mẫu số 01, Mẫu số 02, Mẫu số 03 Phụ lục III ban hành kèm theo Thông tư này gửi Sở Xây dựng bằng một trong các hình thức: trực tiếp, dịch vụ bưu chính, trên môi trường điện tử; đồng thời truyền dữ liệu qua Hệ thống thông tin quản lý, giám sát đào tạo lái xe;
> b) Báo cáo đăng ký khóa đào tạo lái xe, danh sách học viên, kế hoạch đào tạo phải có dấu giáp lai của cơ sở đào tạo lái xe và gửi đến Sở Xây dựng không quá 07 ngày làm việc kể từ ngày khai giảng; Thủ trưởng đơn vị được Sở Xây dựng giao nhiệm vụ quản lý đào tạo lái xe kiểm tra, ký tên vào từng trang (trừ hình thức tiếp nhận báo cáo trên môi trường điện tử).


`TT14-2025-BXD/D13/K1#2025-09-01` · hiệu lực 2025-09-01 → nay

> Điều 13. Yêu cầu đối với người học lái xe
> 1. Là công dân Việt Nam, người nước ngoài được phép cư trú hoặc đang làm việc, học tập tại Việt Nam.


`TT14-2025-BXD/D13/K2#2026-07-01` · hiệu lực 2026-07-01 → nay

> Điều 13. Yêu cầu đối với người học lái xe
> 2. Người học lái xe để nâng hạng giấy phép lái xe phải đáp ứng theo quy định tại khoản 4 Điều 60 Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15; trong đó, thời gian lái xe an toàn cho từng hạng giấy phép lái xe được quy định cụ thể như sau:
> a) Hạng B lên C1, B lên C, B lên D1, B lên BE, C1 lên C, C1 lên D1, C1 lên D2, C1 lên C1E, C lên D1, C lên D2, D1 lên D2, D1 lên D, D1 lên D1E, D2 lên D, D2 lên D2E, D lên CE, D lên DE: thời gian lái xe an toàn từ 02 năm trở lên;
> b) Hạng B lên D2, D1 lên CE, D2 lên CE, C lên CE, C lên D: thời gian lái xe an toàn từ 03 năm trở lên.


`TT14-2025-BXD/D13/K3#2025-09-01` · hiệu lực 2025-09-01 → nay

> Điều 13. Yêu cầu đối với người học lái xe
> 3. Người đã có giấy phép lái xe hạng B chuyển số tự động được đăng ký học để cấp mới giấy phép lái xe hạng B chuyển số cơ khí (số sàn), người đã có giấy phép lái xe hạng B được đăng ký học để cấp mới giấy phép lái xe hạng C1 theo quy định tại Điều 6 Thông tư này; hồ sơ của người học lái xe thực hiện theo quy định tại khoản 1 Điều 14 Thông tư này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["TT14-2025-BXD/D7/K3", "TT14-2025-BXD/D13"], "required_numbers": []}
```

### W-da_buoc-032 · tier A · LUAT35-2024/D15/K3

Luật Đường bộ số 35/2024/QH15 · DAN_CHIEU → LUAT35-2024/D15/K3/c

`LUAT35-2024/D21/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 21. Bảo vệ kết cấu hạ tầng đường bộ
> 3. Trách nhiệm bảo vệ kết cấu hạ tầng đường bộ quy định như sau:
> a) Bộ Giao thông vận tải tổ chức thực hiện bảo vệ kết cấu hạ tầng đường bộ thuộc phạm vi quản lý, trừ quy định tại điểm b khoản này;
> b) Ủy ban nhân dân các cấp tổ chức thực hiện bảo vệ kết cấu hạ tầng đường bộ thuộc phạm vi quản lý; phối hợp với người quản lý, sử dụng đường bộ để tuyên truyền, phổ biến pháp luật về bảo vệ kết cấu hạ tầng đường bộ; công bố công khai mốc lộ giới sử dụng đất trong hành lang an toàn đường bộ; kịp thời xử lý trường hợp lấn, chiếm, sử dụng trái phép hành lang an toàn đường bộ, đất của đường bộ;
> c) Người quản lý, sử dụng đường bộ có trách nhiệm bảo vệ kết cấu hạ tầng đường bộ thuộc phạm vi quản lý; trường hợp phát hiện công trình bị hư hỏng, nguy cơ gây ra sự cố công trình, nguy cơ mất an toàn giao thông đường bộ thì phải xử lý, sửa chữa, khắc phục kịp thời; công khai về mốc lộ giới hành lang an toàn đường bộ theo quy định tại điểm c khoản 3 Điều 15 của Luật này, báo cáo và yêu cầu Ủy ban nhân dân cấp xã nơi có hành lang an toàn đường bộ bị lấn, chiếm, sử dụng trái phép để xử lý; thực hiện các công việc khác về quản lý, bảo vệ hành lang an toàn đường …


`LUAT35-2024/D15/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 15. Hành lang an toàn đường bộ
> 3. Việc xác định và quản lý mốc lộ giới hành lang an toàn đường bộ được quy định như sau:
> a) Mốc lộ giới hành lang an toàn đường bộ được xác định theo quy mô, cấp kỹ thuật, hướng tuyến, phạm vi xây dựng công trình đường bộ;
> b) Chủ đầu tư xây dựng công trình đường bộ có trách nhiệm tổ chức thực hiện cắm mốc lộ giới hành lang an toàn đường bộ trong phạm vi dự án đầu tư xây dựng công trình đường bộ; bàn giao cho cơ quan quản lý đường bộ, người quản lý, sử dụng đường bộ;
> c) Cơ quan quản lý đường bộ, người quản lý, sử dụng đường bộ có trách nhiệm công bố công khai mốc lộ giới hành lang an toàn đường bộ; điều chỉnh, bổ sung mốc lộ giới hành lang an toàn đường bộ trong thời gian quản lý, vận hành, khai thác và bảo trì công trình đường bộ;
> d) Cơ quan quản lý đường bộ, người quản lý, sử dụng đường bộ, Ủy ban nhân dân các cấp có trách nhiệm quản lý mốc lộ giới hành lang an toàn đường bộ theo quy định của Luật này, quy định của pháp luật về đất đai và quy định khác của pháp luật có liên quan.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["LUAT35-2024/D21/K3", "LUAT35-2024/D15/K3"], "required_numbers": []}
```

### W-da_buoc-033 · tier A · ND168-2024/D6/K15

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · BI_XU_PHAT → ND168-2024/D6/K15/a

`ND168-2024/D6/K5#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
> 5. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Vượt xe trong những trường hợp không được vượt, vượt xe tại đoạn đường có biển báo hiệu có nội dung cấm vượt (đối với loại phương tiện đang điều khiển); không có tín hiệu trước khi vượt hoặc có tín hiệu vượt xe nhưng không sử dụng trong suốt quá trình vượt xe; vượt bên phải xe khác trong trường hợp không được phép;
> b) Điều khiển xe không đi bên phải theo chiều đi của mình; đi không đúng phần đường hoặc làn đường quy định (làn cùng chiều hoặc làn ngược chiều) trừ hành vi quy định tại điểm a khoản 4 Điều này; điều khiển xe đi qua dải phân cách cố định ở giữa hai phần đường xe chạy;
> c) Tránh xe đi ngược chiều không đúng quy định (trừ hành vi vi phạm sử dụng đèn chiếu xa khi tránh xe đi ngược chiều quy định tại điểm b khoản 3 Điều này); không nhường đường cho xe đi ngược chiều theo quy định tại nơi đường hẹp, đường dốc, nơi có chướng ngại vật;
> d) …

- CheTai tich_thu: thiết bị phát tín hiệu ưu tiên lắp đặt, sử dụng trái quy định (nêu tại ND168-2024/D6/K15/a)
- CheTai phat_tien: 4.000.000–6.000.000 đồng (nêu tại ND168-2024/D6/K5)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D6/K16/a)
- DiemGPLX: trừ 4 điểm (nêu tại ND168-2024/D6/K16/b)
- DiemGPLX: trừ 6 điểm (nêu tại ND168-2024/D6/K16/c)

`ND168-2024/D6/K15#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
> 15. Ngoài việc bị phạt tiền, người điều khiển xe thực hiện hành vi vi phạm còn bị áp dụng các hình thức xử phạt bổ sung sau đây:
> a) Thực hiện hành vi quy định tại điểm e khoản 5 Điều này còn bị tịch thu thiết bị phát tín hiệu ưu tiên lắp đặt, sử dụng trái quy định;
> b) Thực hiện hành vi quy định tại khoản 12 Điều này bị tước quyền sử dụng giấy phép lái xe từ 10 tháng đến 12 tháng;
> c) Thực hiện hành vi quy định tại điểm a, điểm b, điểm c, điểm d khoản 11; khoản 13; khoản 14 Điều này bị tước quyền sử dụng giấy phép lái xe từ 22 tháng đến 24 tháng.

- CheTai tich_thu: thiết bị phát tín hiệu ưu tiên lắp đặt, sử dụng trái quy định (nêu tại ND168-2024/D6/K15/a)
- CheTai tuoc_quyen: 10–12 tháng giấy phép lái xe (nêu tại ND168-2024/D6/K15/b)
- CheTai tuoc_quyen: 22–24 tháng giấy phép lái xe (nêu tại ND168-2024/D6/K15/c)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D6/K5", "ND168-2024/D6/K15"], "required_numbers": [{"value": 4000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}, {"value": 4, "unit": "diem"}, {"value": 6, "unit": "diem"}, {"value": 10, "unit": "thang"}, {"value": 12, "unit": "thang"}, {"value": 22, "unit": "thang"}, {"value": 24, "unit": "thang"}]}
```

### W-da_buoc-034 · tier A · LUAT36-2024/D10/K3

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15 · DAN_CHIEU → LUAT36-2024/D10/K3

`LUAT36-2024/D87/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 87. Trách nhiệm quản lý nhà nước về trật tự, an toàn giao thông đường bộ
> 3. Bộ Giao thông vận tải thực hiện quản lý nhà nước về đào tạo, sát hạch, cấp giấy phép lái xe; chất lượng an toàn kỹ thuật và bảo vệ môi trường của xe cơ giới, xe máy chuyên dùng, phụ tùng xe cơ giới và nhiệm vụ quản lý khác theo quy định của Luật này; ban hành quy chuẩn kỹ thuật quốc gia về thiết bị an toàn cho trẻ em quy định tại khoản 3 Điều 10 của Luật này.


`LUAT36-2024/D10/K3#2026-01-01` · hiệu lực 2026-01-01 → nay

> Điều 10. Quy tắc chung
> 3. Khi chở trẻ em dưới 10 tuổi và chiều cao dưới 1,35 mét trên xe ô tô không được cho trẻ em ngồi cùng hàng ghế với người lái xe, trừ loại xe ô tô chỉ có một hàng ghế; người lái xe phải sử dụng, hướng dẫn sử dụng thiết bị an toàn phù hợp cho trẻ em.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D87/K3", "LUAT36-2024/D10/K3"], "required_numbers": []}
```

### W-da_buoc-035 · tier A · LUAT36-2024/D62/K5

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15 · DAN_CHIEU → LUAT36-2024/D62/K5

`LUAT36-2024/D57/K7#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 57. Giấy phép lái xe
> 7. Giấy phép lái xe không có hiệu lực trong các trường hợp sau đây:
> a) Giấy phép lái xe hết thời hạn sử dụng;
> b) Giấy phép lái xe bị thu hồi theo quy định tại khoản 5 Điều 62 của Luật này.


`LUAT36-2024/D62/K5#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 62. Cấp, đổi, cấp lại và thu hồi giấy phép lái xe
> 5. Giấy phép lái xe bị thu hồi khi thuộc một trong các trường hợp sau đây:
> a) Người được cấp giấy phép lái xe không đủ điều kiện sức khỏe theo kết luận của cơ sở khám bệnh, chữa bệnh đối với từng hạng giấy phép lái xe;
> b) Giấy phép lái xe được cấp sai quy định;
> c) Giấy phép lái xe đã quá thời hạn tạm giữ hoặc hết thời hiệu thi hành quyết định xử phạt vi phạm hành chính theo quy định của pháp luật về xử lý vi phạm hành chính nếu người vi phạm không đến nhận mà không có lý do chính đáng.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D57/K7", "LUAT36-2024/D62/K5"], "required_numbers": []}
```

### W-da_buoc-036 · tier A · TT12-2025-BCA/D13/K2

Thông tư số 12/2025/TT-BCA (Quy định về sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế) · DAN_CHIEU → TT12-2025-BCA/D13/K2/a

`TT12-2025-BCA/D4/K2#2025-03-01` · hiệu lực 2025-03-01 → nay

> Điều 4. Hình thức, nội dung và quy trình sát hạch lái xe
> 2. Sát hạch thực hành lái xe trong hình
> a) Đối với hạng A1, A
> Thực hiện sát hạch bằng phương pháp chấm điểm trực tiếp kết hợp thiết bị chấm điểm tự động, trừ trường hợp quy định tại khoản 2 Điều 5 Thông tư này. Người dự sát hạch phải điều khiển xe mô tô qua 04 bài sát hạch: đi theo hình số 8, qua vạch đường thẳng, qua đường có vạch cản, qua đường gồ ghề;
> b) Đối với hạng B1
> Thực hiện sát hạch bằng phương pháp chấm điểm trực tiếp, sát hạch viên không ngồi trên xe sát hạch. Người dự sát hạch phải điều khiển xe tiến qua hình chữ chi và lùi theo hướng ngược lại;
> c) Đối với các hạng B, C1, C, D1, D2, D
> Thực hiện sát hạch bằng phương pháp sử dụng thiết bị chấm điểm tự động; không có sát hạch viên ngồi trên xe sát hạch, trừ trường hợp quy định tại điểm a khoản 2 Điều 13 Thông tư này.
> Người dự sát hạch phải điều khiển xe qua các bài sát hạch đã bố trí tại trung tâm sát hạch lái xe gồm: xuất phát, dừng xe nhường đường cho người đi bộ, dừng và khởi hành xe trên dốc, qua vệt bánh xe và đường vòng vuông góc, qua ngã tư có đèn tín hiệu điều khiển giao thông, qua đường vòng quanh co, ghép xe vào nơi đỗ (hạng B và C1 thực hiện ghép xe dọc; …


`TT12-2025-BCA/D13/K2#2025-03-01` · hiệu lực 2025-03-01 → nay

> Điều 13. Sát hạch lái xe đối với người khuyết tật
> 2. Sát hạch để cấp giấy phép lái xe hạng B số tự động
> a) Sát hạch để cấp giấy phép lái xe hạng B số tự động cho người khuyết tật bàn chân phải hoặc bàn tay phải hoặc bàn tay trái: thí sinh thực hiện đủ nội dung và quy trình sát hạch quy định tại Điều 4 Thông tư này; sát hạch tại trung tâm sát hạch lái xe, có hai sát hạch viên ngồi trên xe chấm điểm trực tiếp nội dung sát hạch lái xe trong hình và trên đường;
> b) Sát hạch để cấp giấy phép lái xe hạng B số tự động cho người khuyết tật, trừ người khuyết tật bàn chân phải hoặc bàn tay phải hoặc bàn tay trái: thí sinh thực hiện đủ nội dung và quy trình sát hạch quy định tại Điều 4 Thông tư này; sát hạch tại trung tâm sát hạch lái xe.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["TT12-2025-BCA/D4/K2", "TT12-2025-BCA/D13/K2"], "required_numbers": []}
```

### W-da_buoc-037 · tier A · ND168-2024/D34/K6

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · BI_XU_PHAT → ND168-2024/D34/K6

`ND168-2024/D34/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 34. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển quá khổ giới hạn, xe quá tải trọng, xe bánh xích lưu hành đường bộ (kể cả xe ô tô chở hành khách)
> 4. Phạt tiền từ 13.000.000 đồng đến 15.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe mà tổng trọng lượng (khối lượng toàn bộ) của xe hoặc tải trọng trục xe (bao gồm cả hàng hóa xếp trên xe, người được chở trên xe) vượt quá tải trọng cho phép của đường bộ trên 20% đến 50%, trừ trường hợp có giấy phép lưu hành còn giá trị sử dụng;
> b) Điều khiển xe có giấy phép lưu hành còn giá trị sử dụng nhưng tổng trọng lượng (khối lượng toàn bộ) của xe hoặc tải trọng trục xe (bao gồm cả hàng hóa xếp trên xe nếu có) vượt quá quy định trong giấy phép lưu hành;
> c) Điều khiển xe có giấy phép lưu hành còn giá trị sử dụng nhưng đi không đúng tuyến đường quy định trong giấy phép lưu hành.

- BienPhapBoSung: buộc khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND168-2024/D34/K6)
- CheTai phat_tien: 13.000.000–15.000.000 đồng (nêu tại ND168-2024/D34/K4)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D34/K7/a)
- DiemGPLX: trừ 3 điểm (nêu tại ND168-2024/D34/K7/b)

`ND168-2024/D34/K6#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 34. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển quá khổ giới hạn, xe quá tải trọng, xe bánh xích lưu hành đường bộ (kể cả xe ô tô chở hành khách)
> 6. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm quy định tại khoản 1, khoản 2, khoản 3, khoản 4, khoản 5 Điều này nếu gây hư hại cầu, đường còn bị áp dụng biện pháp khắc phục hậu quả buộc khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra.

- BienPhapBoSung: buộc khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND168-2024/D34/K6)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D34/K4", "ND168-2024/D34/K6"], "required_numbers": [{"value": 13000000, "unit": "vnd"}, {"value": 15000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}, {"value": 3, "unit": "diem"}]}
```

### W-da_buoc-038 · tier A · LUAT36-2024/D39/K5

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15 · DAN_CHIEU → LUAT36-2024/D39/K5/c

`TT79-2024-BCA/D22/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 22. Hồ sơ đăng ký xe tạm thời
> 3. Chứng nhận nguồn gốc xe, gồm một trong các giấy tờ sau:
> a) Dữ liệu điện tử phiếu kiểm tra chất lượng xuất xưởng hoặc dữ liệu điện tử chứng nhận an toàn kỹ thuật bảo vệ môi trường xe nhập khẩu hoặc bản phô tô phiếu kiểm tra chất lượng xuất xưởng hoặc bản phô tô giấy chứng nhận an toàn kỹ thuật bảo vệ môi trường xe nhập khẩu (trường hợp xe di chuyển từ nhà máy đến kho, cảng hoặc từ kho, cảng, nhà máy, đại lý bán xe đến nơi đăng ký xe hoặc về các đại lý, kho lưu trữ khác theo quy định tại điểm a khoản 5 Điều 39 Luật Trật tự, an toàn giao thông đường bộ);
> b) Phiếu kiểm tra chất lượng xuất xưởng đối với xe thuộc đối tượng nghiên cứu phát triển có nhu cầu tham gia giao thông đường bộ theo quy định (trường hợp xe chạy thử nghiệm thuộc đối tượng nghiên cứu phát triển có nhu cầu tham gia giao thông đường bộ theo quy định tại điểm c khoản 5 Điều 39 Luật Trật tự, an toàn giao thông đường bộ).
> c) Văn bản của cơ quan có thẩm quyền cho phép tham gia giao thông, kèm theo danh sách xe và bản phô tô chứng nhận đăng ký xe của nước sở tại (trường hợp xe đăng ký ở nước ngoài được cơ quan thẩm quyền cho phép bao gồm cả xe có tay lái bên phải (tay lái nghịch) vào …


`LUAT36-2024/D39/K5#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 39. Cấp, thu hồi chứng nhận đăng ký xe và biển số xe cơ giới, xe máy chuyên dùng tham gia giao thông đường bộ
> 5. Xe cơ giới, xe máy chuyên dùng được cấp biển số xe và đăng ký tạm thời trong các trường hợp sau đây:
> a) Đã có chứng nhận chất lượng an toàn kỹ thuật và bảo vệ môi trường, phiếu kiểm tra chất lượng xuất xưởng xe cơ giới, xe máy chuyên dùng để di chuyển từ nhà máy đến kho, cảng hoặc từ kho, cảng, nhà máy, đại lý bán xe đến nơi đăng ký xe hoặc về các đại lý, kho lưu trữ khác;
> b) Xe làm thủ tục thu hồi để tái xuất hoặc chuyển quyền sở hữu; xe phục vụ các sự kiện do Đảng, Nhà nước tổ chức; xe đăng ký ở nước ngoài được cơ quan thẩm quyền cho phép bao gồm cả xe có tay lái bên phải (tay lái nghịch) vào Việt Nam quá cảnh, tạm nhập, tái xuất có thời hạn để tham dự hội nghị, hội chợ, triển lãm, thể dục, thể thao, du lịch; trừ trường hợp xe không phải cấp biển số xe tạm thời theo điều ước quốc tế mà nước Cộng hòa xã hội chủ nghĩa Việt Nam là thành viên và trường hợp quy định tại Điều 55 của Luật này;
> c) Xe chạy thử nghiệm thuộc đối tượng nghiên cứu phát triển có nhu cầu tham gia giao thông đường bộ đáp ứng quy định tại điểm h khoản 5 Điều 42 của Luật này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["TT79-2024-BCA/D22/K3", "LUAT36-2024/D39/K5"], "required_numbers": []}
```

### W-da_buoc-039 · tier A · ND151-2024/D11/K10

Nghị định số 151/2024/NĐ-CP (Quy định chi tiết một số điều và biện pháp thi hành Luật Trật tự, an toàn giao thông đường bộ) · DAN_CHIEU → ND151-2024/D11

`ND151-2024/D14/K1#2026-07-01` · hiệu lực 2026-07-01 → nay

> Điều 14. Kết nối, chia sẻ, khai thác, sử dụng Cơ sở dữ liệu về trật tự, an toàn giao thông đường bộ
> 1. Việc kết nối, chia sẻ thông tin giữa Cơ sở dữ liệu về trật tự, an toàn giao thông đường bộ với các cơ sở dữ liệu chuyên ngành và các cơ sở dữ liệu khác được thực hiện theo quy định của Luật Trật tự, an toàn giao thông đường bộ và quy định của Chính phủ về quản lý, kết nối và chia sẻ dữ liệu số trong cơ quan nhà nước và các quy định khác có liên quan. Các bộ, ngành thực hiện kết nối, chia sẻ thông tin với Cơ sở dữ liệu về trật tự, an toàn giao thông đường bộ thống nhất danh mục các trường dữ liệu chi tiết dựa trên thông tin quy định tại Điều 11 Nghị định này.


`ND151-2024/D11/K7#2025-01-01` · hiệu lực 2025-01-01 → 2026-06-30

> Điều 11. Thông tin trong Cơ sở dữ liệu về trật tự, an toàn giao thông đường bộ
> 7. Thông tin về người điều khiển xe cơ giới, xe máy chuyên dùng: họ, tên; số định danh cá nhân; ngày, tháng, năm sinh; quốc tịch; nơi cư trú; số giấy phép lái xe, hạng giấy phép lái xe, cơ quan cấp giấy phép lái xe, số chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ, cơ sở đào tạo và cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ; thông tin về kết quả khám sức khỏe của người điều khiển phương tiện.


`ND151-2024/D11/K1#2026-07-01` · hiệu lực 2026-07-01 → nay

> Điều 11. Thông tin trong Cơ sở dữ liệu về trật tự, an toàn giao thông đường bộ
> 1. Thông tin về đăng ký, quản lý xe cơ giới, xe máy chuyên dùng:
> a) Thông tin về chủ sở hữu xe cơ giới, xe máy chuyên dùng:
> Đối với cá nhân: họ, tên; ngày, tháng, năm sinh; giới tính; số định danh cá nhân; số điện thoại (nếu có); quốc tịch; nơi thường trú; nơi tạm trú, nơi ở hiện tại, địa chỉ đăng ký xe.
> Đối với tổ chức: tên tổ chức; tên người đại diện hợp pháp; địa chỉ; mã số thuế hoặc quyết định thành lập hoặc số định danh của tổ chức (nếu có); số điện thoại; loại hình doanh nghiệp; tình trạng hoạt động;
> b) Thông tin về phương tiện theo quy định tại điểm a khoản 2 Điều này;
> c) Thông tin về đăng ký, quản lý xe: biển số xe; màu biển số xe; số, ngày, tháng, năm cấp, cơ quan cấp chứng nhận đăng ký xe; thời hạn đăng ký xe; trạng thái đăng ký xe; trạng thái xe; số, ngày, tháng, năm cấp, cơ quan cấp chứng nhận nguồn gốc xe; số, ngày, tháng, năm cấp, cơ quan cấp chứng nhận quyền sở hữu; số, ngày, tháng, năm cấp, cơ quan cấp chứng từ lệ phí trước bạ, số tiền lệ phí trước bạ; loại xe ưu tiên, thiết bị phát tín hiệu ưu tiên, màu của tín hiệu đèn ưu tiên, số, thời hạn sử dụng giấy phép, cơ quan cấp giấy phép sử …


`ND151-2024/D11/K10#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 11. Thông tin trong Cơ sở dữ liệu về trật tự, an toàn giao thông đường bộ
> 10. Thông tin về hành trình của phương tiện giao thông đường bộ, hình ảnh người lái xe:
> a) Thông tin về phương tiện: biển số xe, loại xe, màu sơn, nhãn hiệu, số loại, năm sản xuất; số, ngày, tháng, năm cấp, ngày, tháng, năm hết hạn của giấy chứng nhận kiểm định; thông tin về đơn vị kinh doanh vận tải, đơn vị cứu thương, cứu hộ giao thông, chủ xe;
> b) Thông tin về hành trình: thời gian hành trình; lộ trình; tốc độ; quãng đường; vị trí phương tiện;
> c) Thông tin về người lái xe: họ, tên; ngày, tháng, năm sinh; địa chỉ; giấy phép lái xe; dữ liệu hình ảnh người lái xe; lịch sử vi phạm của người lái xe;
> d) Thông tin về hành vi vi phạm giao thông, tai nạn giao thông; biện pháp xử lý.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["ND151-2024/D14/K1", "ND151-2024/D11"], "required_numbers": []}
```

### W-da_buoc-040 · tier A · TT79-2024-BCA/D16/K2

Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng) · DAN_CHIEU → TT79-2024-BCA/D16

`TT79-2024-BCA/D33/K9#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 33. Giải quyết một số trường hợp khi đăng ký, cấp biển số xe
> 9. Xe đã đăng ký của các dự án viện trợ của nước ngoài khi hết hạn, bàn giao cho phía Việt Nam thì hồ sơ đăng ký sang tên xe thực hiện quy định tại Điều 16 Thông tư này, kèm theo:
> a) Quyết định xác lập quyền sở hữu toàn dân đối với xe đó (đối với các cơ quan Trung ương là văn bản của Thủ trưởng cấp Bộ, đối với các cơ quan địa phương là văn bản của Chủ tịch Ủy ban nhân dân cấp tỉnh) và biên bản bàn giao tiếp nhận tài sản từ nhà tài trợ;
> b) Trường hợp xe viện trợ của dự án khi hết hạn, muốn bán phải có quyết định xử lý tài sản của cấp có thẩm quyền.


`TT79-2024-BCA/D16/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 16. Hồ sơ đăng ký sang tên xe
> 1. Hồ sơ thu hồi
> a) Giấy khai thu hồi chứng nhận đăng ký xe, biển số xe;
> b) Giấy tờ của chủ xe theo quy định tại Điều 10 Thông tư này;
> c) 02 bản chà số máy, số khung của xe;
> d) Bản sao chứng từ chuyển quyền sở hữu xe theo quy định;
> đ) Chứng nhận đăng ký xe, biển số xe; trường hợp mất chứng nhận đăng ký xe hoặc mất biển số xe thì phải ghi rõ lý do trong giấy khai thu hồi chứng nhận đăng ký xe, biển số xe.
> Trong thời gian chờ nhận kết quả thu hồi, chủ xe được giữ lại biển số xe để sử dụng và phải nộp lại khi nhận chứng nhận thu hồi; trường hợp chủ xe không nộp lại biển số xe thì cơ quan đăng ký xe hủy kết quả và yêu cầu chủ xe làm lại thủ tục thu hồi trong trường hợp mất biển số xe theo quy định.


`TT79-2024-BCA/D16/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 16. Hồ sơ đăng ký sang tên xe
> 2. Hồ sơ đăng ký
> a) Giấy khai đăng ký xe;
> b) Giấy tờ của chủ xe quy định;
> c) Chứng từ chuyển quyền sở hữu xe theo quy định;
> d) Chứng từ lệ phí trước bạ xe theo quy định;
> đ) Chứng nhận thu hồi chứng nhận đăng ký xe, biển số xe.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["TT79-2024-BCA/D33/K9", "TT79-2024-BCA/D16"], "required_numbers": []}
```

### W-da_buoc-041 · tier A · TT79-2024-BCA/D16/K2

Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng) · DAN_CHIEU → TT79-2024-BCA/D16

`TT79-2024-BCA/D33/K7#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 33. Giải quyết một số trường hợp khi đăng ký, cấp biển số xe
> 7. Xe có quyết định bán để bảo đảm thi hành án hoặc thu hồi nợ
> a) Xe có hồ sơ gốc hợp lệ, giấy tờ chứng minh quyền sở hữu xe hợp pháp của người có xe bị xử lý tài sản thì giải quyết đăng ký xe. Trường hợp xe chưa rõ nguồn gốc hoặc không có giấy tờ chứng minh quyền sở hữu xe hợp pháp của người bị xử lý tài sản thì không tiếp nhận giải quyết đăng ký xe mà phải hướng dẫn chủ xe đến nơi đã ra quyết định bán đấu giá để giải quyết;
> b) Xe do cơ quan Thi hành án có quyết định bán để bảo đảm thi hành án thì hồ sơ đăng ký xe gồm có: Bản sao quyết định của Toà án hoặc trích lục bản án hoặc quyết định thi hành án của cơ quan Thi hành án dân sự có thẩm quyền, giấy tờ thu tiền hoặc biên bản bàn giao tài sản.
> Trường hợp xe chưa đăng ký thì bổ sung hồ sơ đăng ký theo quy định tại Điều 8 Thông tư này.
> Trường hợp xe đã đăng ký thì người mua xe thực hiện thu hồi chứng nhận đăng ký xe, biển số xe theo quy định tại Điều 16 Thông tư này (nếu không còn chứng nhận đăng ký xe thì phải có văn bản xác nhận của cơ quan thi hành án) và nộp bổ sung hồ sơ đăng ký xe gồm: Giấy khai đăng ký xe, giấy tờ của chủ xe theo quy định tại Điều 10 Thông tư …


`TT79-2024-BCA/D16/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 16. Hồ sơ đăng ký sang tên xe
> 1. Hồ sơ thu hồi
> a) Giấy khai thu hồi chứng nhận đăng ký xe, biển số xe;
> b) Giấy tờ của chủ xe theo quy định tại Điều 10 Thông tư này;
> c) 02 bản chà số máy, số khung của xe;
> d) Bản sao chứng từ chuyển quyền sở hữu xe theo quy định;
> đ) Chứng nhận đăng ký xe, biển số xe; trường hợp mất chứng nhận đăng ký xe hoặc mất biển số xe thì phải ghi rõ lý do trong giấy khai thu hồi chứng nhận đăng ký xe, biển số xe.
> Trong thời gian chờ nhận kết quả thu hồi, chủ xe được giữ lại biển số xe để sử dụng và phải nộp lại khi nhận chứng nhận thu hồi; trường hợp chủ xe không nộp lại biển số xe thì cơ quan đăng ký xe hủy kết quả và yêu cầu chủ xe làm lại thủ tục thu hồi trong trường hợp mất biển số xe theo quy định.


`TT79-2024-BCA/D16/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 16. Hồ sơ đăng ký sang tên xe
> 2. Hồ sơ đăng ký
> a) Giấy khai đăng ký xe;
> b) Giấy tờ của chủ xe quy định;
> c) Chứng từ chuyển quyền sở hữu xe theo quy định;
> d) Chứng từ lệ phí trước bạ xe theo quy định;
> đ) Chứng nhận thu hồi chứng nhận đăng ký xe, biển số xe.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["TT79-2024-BCA/D33/K7", "TT79-2024-BCA/D16"], "required_numbers": []}
```

### W-da_buoc-042 · tier A · LUAT36-2024/D53/K3

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15 · DAN_CHIEU → LUAT36-2024/D53

`LUAT36-2024/D52/K5#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 52. Bảo đảm trật tự, an toàn giao thông đường bộ đối với xe quá khổ giới hạn, xe quá tải trọng, xe bánh xích lưu hành trên đường bộ
> 5. Cơ quan quản lý đường bộ có thẩm quyền cấp giấy phép lưu hành xe quá khổ giới hạn, xe quá tải trọng, xe bánh xích lưu hành trên đường bộ; trường hợp vận chuyển hàng siêu trường, siêu trọng thì việc cấp giấy phép thực hiện theo quy định tại Điều 53 của Luật này; cơ quan, tổ chức được giao trực tiếp quản lý công trình đường bộ thuộc trường hợp phải gia cường quy định tại điểm a khoản 4 Điều này thực hiện việc chấp thuận phương án khảo sát, thiết kế, gia cường công trình đường bộ.


`LUAT36-2024/D53/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 53. Bảo đảm trật tự, an toàn giao thông đường bộ đối với xe vận chuyển hàng siêu trường, siêu trọng
> 1. Hàng siêu trường, siêu trọng là hàng không thể chia nhỏ, tháo rời, khi vận chuyển trên đường bộ làm cho phương tiện hoặc tổ hợp phương tiện bị vượt quá giới hạn cho phép tham gia giao thông đường bộ về kích thước, khối lượng theo quy định của pháp luật.


`LUAT36-2024/D53/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 53. Bảo đảm trật tự, an toàn giao thông đường bộ đối với xe vận chuyển hàng siêu trường, siêu trọng
> 2. Xe vận chuyển hàng siêu trường, siêu trọng phải phù hợp với loại hàng, kích thước, khối lượng của hàng và phải có giấy phép lưu hành xe do cơ quan quản lý đường bộ có thẩm quyền cấp.


`LUAT36-2024/D53/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 53. Bảo đảm trật tự, an toàn giao thông đường bộ đối với xe vận chuyển hàng siêu trường, siêu trọng
> 3. Xe vận chuyển hàng siêu trường, siêu trọng được phép ghép, nối thành tổ hợp nhiều xe gồm xe ô tô đầu kéo, xe ô tô kéo rơ moóc để kéo hoặc vừa kéo vừa đẩy các rơ moóc, sơ mi rơ moóc chuyên dùng, rơ moóc kiểu mô đun, bao gồm cả trường hợp ghép nối thông qua hàng được chở.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "", "gold_units": ["LUAT36-2024/D52/K5", "LUAT36-2024/D53"], "required_numbers": []}
```

### W-da_buoc-043 · tier B · LUAT36-2024/D73/K2

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15 · DAN_CHIEU → LUAT36-2024/D73

`TT69-2024-BCA/D22#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 22. Giải quyết một số trường hợp khác
> Người lái xe không chấp hành hiệu lệnh dừng xe, bỏ chạy; người vi phạm không chấp hành yêu cầu kiểm soát, xúi giục lôi kéo người khác cản trở người thi hành công vụ; người vi phạm có hành vi lăng mạ, đe dọa, cản trở, xô đẩy người thi hành công vụ; người vi phạm không chấp hành việc kiểm soát, yêu cầu được xem kế hoạch tuần tra, kiểm soát, xem thiết bị sử dụng để phát hiện vi phạm; ghi hình, ghi âm lại hoạt động của Cảnh sát giao thông đang thực hiện nhiệm vụ; người vi phạm lợi dụng mạng xã hội để cung cấp, chia sẻ thông tin giả mạo, thông tin sai sự thật, xuyên tạc, vu khống, xúc phạm uy tín của lực lượng Cảnh sát giao thông, danh dự, nhân phẩm của cá nhân cán bộ, chiến sĩ trong khi thực hiện nhiệm vụ tuần tra, kiểm soát, xử lý vi phạm; người lái xe điều khiển xe đâm vào người thi hành công vụ; người lái xe dùng vũ lực, vũ khí, vật nguy hiểm chống người thi hành công vụ; trường hợp phạm tội quả tang, người có mặt trên xe vận chuyển vật, hàng hóa vi phạm, có dấu hiệu tội phạm; giải quyết vụ việc liên quan đến người nước ngoài, xe của người nước ngoài vi phạm trật tự, an toàn giao thông hoặc các hành vi vi phạm pháp luật khác thì Cảnh sát …


`LUAT36-2024/D73/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 73. Ngăn chặn hành vi không chấp hành yêu cầu kiểm tra, kiểm soát, cản trở, chống người thi hành công vụ
> 1. Khi người tham gia giao thông đường bộ không chấp hành yêu cầu kiểm tra, kiểm soát, có hành vi cản trở, chống người thi hành công vụ thì người thi hành công vụ thực hiện các biện pháp sau đây:
> a) Giải thích cho người vi phạm biết rõ về hành vi không chấp hành yêu cầu kiểm tra, kiểm soát, có hành vi cản trở, chống người thi hành công vụ; quyền và trách nhiệm của người vi phạm; thuyết phục, yêu cầu chấm dứt ngay hành vi vi phạm, chấp hành yêu cầu kiểm tra, kiểm soát;
> b) Áp dụng các biện pháp ngăn chặn theo quy định của pháp luật trong trường hợp người vi phạm cản trở, không chấp hành yêu cầu kiểm tra, kiểm soát của người thi hành công vụ;
> c) Trường hợp người vi phạm có hành vi chống người thi hành công vụ thì tùy theo tình huống, tính chất, mức độ nguy hiểm của hành vi, người thi hành công vụ được sử dụng vũ lực, công cụ hỗ trợ hoặc vũ khí theo quy định của pháp luật để ngăn chặn hành vi vi phạm và phòng vệ chính đáng.


`LUAT36-2024/D73/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 73. Ngăn chặn hành vi không chấp hành yêu cầu kiểm tra, kiểm soát, cản trở, chống người thi hành công vụ
> 2. Trường hợp người điều khiển phương tiện tham gia giao thông đường bộ không chấp hành tín hiệu, hiệu lệnh dừng phương tiện và bỏ chạy thì người thi hành công vụ được thực hiện quyền truy đuổi để ngăn chặn và xử lý hành vi vi phạm.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "B", "answer": "", "gold_units": ["TT69-2024-BCA/D22", "LUAT36-2024/D73"], "required_numbers": []}
```

### W-da_buoc-044 · tier B · ND158-2024/D75/K2

Nghị định số 158/2024/NĐ-CP (Quy định về hoạt động vận tải đường bộ) · DAN_CHIEU → ND158-2024/D75

`ND158-2024/D64/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 64. Bộ Giao thông vận tải
> 3. Tổ chức thực hiện ứng dụng công nghệ thông tin trong công tác quản lý hoạt động kinh doanh vận tải bằng xe ô tô; công bố cấu trúc thông tin, thiết bị, trình tự kiểm tra thông tin của mã QR trên phù hiệu, Giấy phép kinh doanh vận tải; quản lý và hướng dẫn đơn vị cung cấp phần mềm ứng dụng hỗ trợ kết nối vận tải quy định tại Điều 75 của Nghị định này.


`ND158-2024/D75/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 75. Đơn vị cung cấp phần mềm ứng dụng hỗ trợ kết nối vận tải
> 1. Đơn vị cung cấp phần mềm ứng dụng hỗ trợ kết nối vận tải (không trực tiếp điều hành phương tiện, lái xe; không quyết định giá cước vận tải) phải chấp hành các quy định theo pháp luật về giao dịch điện tử, các pháp luật khác có liên quan và phải đáp ứng các yêu cầu sau:
> a) Ghi nhận yêu cầu vận chuyển của khách hàng và chuyển yêu cầu vận chuyển đến đơn vị kinh doanh vận tải đang tham gia trong phần mềm ứng dụng hỗ trợ kết nối vận tải;
> b) Thực hiện vai trò là đơn vị trung gian để xác nhận thực hiện đúng các nội dung đã thỏa thuận giữa đơn vị kinh doanh vận tải với khách hàng, trong đó bảo đảm thực hiện đúng giá cước vận tải đã niêm yết hoặc giá trị hợp đồng đã ký kết; phần mềm ứng dụng hỗ trợ kết nối vận tải cho đơn vị kinh doanh vận tải hành khách bằng xe taxi phải bảo đảm bảo tuân thủ theo quy định tại điểm c khoản 4 Điều 6 của Nghị định này; phần mềm ứng dụng hỗ trợ kết nối vận tải cho đơn vị kinh doanh vận tải hành khách theo hợp đồng phải bảo đảm tuân thủ theo quy định tại điểm a khoản 2 Điều 17 của Nghị định này;
> c) Ghi nhận đánh giá của khách hàng về chất lượng phục vụ của lái xe để thông tin đến đơn vị kinh …


`ND158-2024/D75/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 75. Đơn vị cung cấp phần mềm ứng dụng hỗ trợ kết nối vận tải
> 2. Trường hợp đơn vị cung cấp phần mềm ứng dụng hỗ trợ kết nối vận tải có thực hiện ít nhất một trong các công đoạn chính của hoạt động vận tải (trực tiếp điều hành phương tiện, lái xe hoặc quyết định giá cước vận tải) để vận chuyển hành khách, hàng hóa trên đường bộ nhằm mục đích sinh lợi phải thực hiện các quy định về kinh doanh và điều kiện kinh doanh vận tải bằng xe ô tô theo quy định của Nghị định này, các quy định của pháp luật về giao dịch điện tử, các pháp luật khác có liên quan và phải đáp ứng các yêu cầu theo quy định tại điểm c, điểm d, điểm e, điểm i, điểm k khoản 1 Điều này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "B", "answer": "", "gold_units": ["ND158-2024/D64/K3", "ND158-2024/D75"], "required_numbers": []}
```

### W-da_buoc-045 · tier B · ND336-2025/D13/K4

Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ) · BI_XU_PHAT → ND336-2025/D13/K4

`ND336-2025/D13/K3#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 13. Xử phạt nhân viên phục vụ trên xe buýt, xe vận chuyển hành khách theo tuyến cố định, xe vận chuyển hành khách theo hợp đồng
> 3. Phạt tiền từ 300.000 đồng đến 400.000 đồng đối với nhân viên phục vụ trên xe vận chuyển hành khách theo tuyến cố định thực hiện hành vi vi phạm: thu tiền vé nhưng không trao vé cho hành khách (vé giấy hoặc vé điện tử); thu tiền vé cao hơn quy định.

- BienPhapBoSung: buộc nộp lại số lợi bất hợp pháp có được do thực hiện vi phạm hành chính (nêu tại ND336-2025/D13/K4)
- CheTai phat_tien: 300.000–400.000 đồng (nêu tại ND336-2025/D13/K3)

`ND336-2025/D13/K4#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 13. Xử phạt nhân viên phục vụ trên xe buýt, xe vận chuyển hành khách theo tuyến cố định, xe vận chuyển hành khách theo hợp đồng
> 4. Ngoài việc bị áp dụng hình thức xử phạt, người thực hiện hành vi vi phạm quy định tại khoản 2, khoản 3 Điều này còn bị áp dụng biện pháp khắc phục hậu quả: buộc nộp lại số lợi bất hợp pháp có được do thực hiện vi phạm hành chính.

- BienPhapBoSung: buộc nộp lại số lợi bất hợp pháp có được do thực hiện vi phạm hành chính (nêu tại ND336-2025/D13/K4)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "B", "answer": "", "gold_units": ["ND336-2025/D13/K3", "ND336-2025/D13/K4"], "required_numbers": [{"value": 300000, "unit": "vnd"}, {"value": 400000, "unit": "vnd"}]}
```

### W-da_buoc-046 · tier B · ND158-2024/D6/K8

Nghị định số 158/2024/NĐ-CP (Quy định về hoạt động vận tải đường bộ) · DAN_CHIEU → ND158-2024/D6/K8

`ND158-2024/D73/K1#2026-08-10` · hiệu lực 2026-08-10 → nay

> Điều 73. Ủy ban nhân dân cấp tỉnh
> 1. Chỉ đạo các cơ quan chức năng của địa phương thực hiện:
> a) Quản lý hoạt động vận tải bằng xe ô tô, bằng xe bốn bánh có gắn động cơ theo quy định của Nghị định này và các quy định khác của pháp luật có liên quan;
> b) Xây dựng kế hoạch phát triển và quản lý phương tiện kinh doanh vận tải bảo đảm phù hợp với nhu cầu đi lại của người dân và thực trạng kết cấu hạ tầng giao thông trên địa bàn. Xác định số lượng xe bốn bánh có gắn động cơ kinh doanh vận tải hành khách phù hợp với thực trạng kết cấu hạ tầng giao thông trên địa bàn;
> c) Xây dựng và công bố: danh mục mạng lưới tuyến xe buýt nội tỉnh và liên tỉnh; các khu vực dừng đỗ phục vụ cho phương tiện kinh doanh vận tải đón, trả khách trên địa bàn;
> đ) Xây dựng các vị trí đón, trả khách cho xe taxi, xe buýt theo quy định tại khoản 5 Điều 5, khoản 8 Điều 6 của Nghị định này;
> e) Tổ chức và quản lý các vị trí đỗ cho xe hợp đồng trong khu vực nội thành, nội thị thuộc các đô thị;
> g) Thông báo vị trí bến xe hàng tại địa bàn;
> h) Xây dựng và quản lý điểm đỗ taxi công cộng trên địa bàn;
> i) Tiếp tục thực hiện các tuyến vận tải hành khách cố định nội tỉnh, liên tỉnh đã công bố trước ngày Nghị định này có hiệu lực …


`ND158-2024/D6/K8#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 6. Kinh doanh vận tải hành khách bằng xe taxi
> 8. Xe taxi được ưu tiên bố trí nơi dừng, đỗ để đón, trả khách tại các bến xe, nhà ga, sân bay, bến cảng, khu du lịch, điểm du lịch, cơ sở lưu trú du lịch, điểm tham quan du lịch, địa điểm văn hóa, thể thao, trung tâm thương mại; được ưu tiên hoạt động khi tổ chức giao thông tại đô thị.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "B", "answer": "", "gold_units": ["ND158-2024/D73/K1", "ND158-2024/D6/K8"], "required_numbers": []}
```

### W-da_buoc-047 · tier B · TT73-2024-BCA/D24/K3

Thông tư số 73/2024/TT-BCA (Quy định công tác tuần tra, kiểm soát, xử lý vi phạm pháp luật về trật tự, an toàn giao thông đường bộ của Cảnh sát giao thông) · DAN_CHIEU → TT73-2024-BCA/D24

`TT73-2024-BCA/D5/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 5. Kiểm soát thông qua hệ thống, phương tiện, thiết bị, cơ sở dữ liệu về trật tự, an toàn giao thông đường bộ
> 2. Kiểm soát thông qua sử dụng các phương tiện, thiết bị kỹ thuật nghiệp vụ, thiết bị thông minh hỗ trợ chỉ huy, điều khiển giao thông đường bộ; khai thác dữ liệu từ thiết bị giám sát hành trình, thiết bị ghi nhận hình ảnh người lái xe, cơ sở dữ liệu về trật tự, an toàn giao thông đường bộ
> a) Đơn vị Cảnh sát giao thông sử dụng các phương tiện, thiết bị kỹ thuật nghiệp vụ (bao gồm cả hệ thống thiết bị kỹ thuật nghiệp vụ kiểm tra tải trọng xe cơ giới), thiết bị thông minh hỗ trợ chỉ huy, điều khiển giao thông đường bộ; khai thác dữ liệu từ thiết bị giám sát hành trình, thiết bị ghi nhận hình ảnh người lái xe, cơ sở dữ liệu về trật tự, an toàn giao thông đường bộ để kiểm soát, phát hiện và xử lý các hành vi vi phạm pháp luật về trật tự, an toàn giao thông đường bộ, các hành vi vi phạm pháp luật khác theo quy định;
> b) Kết quả, dữ liệu thu thập được từ phương tiện, thiết bị, cơ sở dữ liệu quy định tại điểm a khoản này để phát hiện, xử lý vi phạm tuân thủ theo quy định của pháp luật xử lý vi phạm hành chính, Nghị định số 135/2021/NĐ-CP, quy định về quy chuẩn, việc quản lý, …


`TT73-2024-BCA/D24/K1#2025-03-01` · hiệu lực 2025-03-01 → nay

> Điều 24. Trình tự xử lý kết quả thu thập được bằng phương tiện, thiết bị kỹ thuật nghiệp vụ đối với trường hợp vi phạm nhưng không dừng được phương tiện giao thông để kiểm soát, xử lý vi phạm
> 1. Trong thời hạn 10 ngày kể từ ngày phát hiện hành vi vi phạm, người có thẩm quyền xử phạt của cơ quan Công an nơi phát hiện vi phạm hành chính thực hiện như sau:
> a) Xác định thông tin về phương tiện giao thông, chủ phương tiện, tổ chức, cá nhân có liên quan đến vi phạm hành chính thông qua cơ quan đăng ký xe, Cơ sở dữ liệu quốc gia về dân cư, cơ quan, tổ chức khác có liên quan;
> b) Trường hợp chủ phương tiện, tổ chức, cá nhân có liên quan đến vi phạm hành chính không cư trú, đóng trụ sở tại địa bàn cấp huyện nơi cơ quan Công an đã phát hiện vi phạm hành chính, nếu xác định vi phạm hành chính đó thuộc thẩm quyền xử phạt của Trưởng Công an xã, phường, thị trấn, Đồn Công an ở huyện nơi không có đơn vị hành chính cấp xã (sau đây gọi chung là Trưởng Công an cấp xã) thì chuyển kết quả thu thập được bằng phương tiện, thiết bị kỹ thuật nghiệp vụ đến Công an xã, phường, thị trấn, Đồn Công an ở huyện nơi không có đơn vị hành chính cấp xã (sau đây gọi chung là Công an cấp xã) nơi chủ phương tiện, tổ …


`TT73-2024-BCA/D24/K2#2025-03-01` · hiệu lực 2025-03-01 → nay

> Điều 24. Trình tự xử lý kết quả thu thập được bằng phương tiện, thiết bị kỹ thuật nghiệp vụ đối với trường hợp vi phạm nhưng không dừng được phương tiện giao thông để kiểm soát, xử lý vi phạm
> 2. Khi chủ phương tiện, tổ chức, cá nhân có liên quan đến vi phạm hành chính đến cơ quan Công an để giải quyết vụ việc vi phạm thì người có thẩm quyền xử phạt vi phạm hành chính của cơ quan Công an nơi phát hiện vi phạm hoặc Trưởng Công an cấp xã, Trưởng phòng Cảnh sát giao thông tiến hành giải quyết, xử lý vụ việc vi phạm theo quy định tại khoản 1 Điều 15 Nghị định số 135/2021/NĐ-CP.


`TT73-2024-BCA/D24/K3#2025-03-01` · hiệu lực 2025-03-01 → nay

> Điều 24. Trình tự xử lý kết quả thu thập được bằng phương tiện, thiết bị kỹ thuật nghiệp vụ đối với trường hợp vi phạm nhưng không dừng được phương tiện giao thông để kiểm soát, xử lý vi phạm
> 3. Trường hợp vụ việc vi phạm do Công an cấp xã, Phòng Cảnh sát giao thông giải quyết, xử lý thì phải thông báo ngay (trên cơ sở dữ liệu xử lý vi phạm hành chính) kết quả giải quyết, xử lý vụ việc cho cơ quan Công an nơi phát hiện vi phạm. Đồng thời, cập nhật trạng thái đã giải quyết, xử lý vụ việc trên Trang thông tin điện tử của Cục Cảnh sát giao thông; gỡ bỏ trạng thái đã gửi thông báo cảnh báo trên cơ sở dữ liệu xử lý vi phạm hành chính và gửi ngay thông báo kết thúc cảnh báo phương tiện giao thông vi phạm cho cơ quan Đăng kiểm, cơ quan đăng ký xe (nếu đã có thông tin cảnh báo từ cơ quan Công an nơi phát hiện vi phạm đối với vụ việc quy định tại khoản 5 Điều này).


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "B", "answer": "", "gold_units": ["TT73-2024-BCA/D5/K2", "TT73-2024-BCA/D24"], "required_numbers": []}
```

### W-da_buoc-048 · tier B · LUAT35-2024/D29/K2

Luật Đường bộ số 35/2024/QH15 · DAN_CHIEU → LUAT35-2024/D29/K2

`ND165-2024/D32/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 32. Thẩm tra, thẩm định an toàn giao thông đường bộ
> 4. Tổ chức tư vấn thẩm tra an toàn giao thông có trách nhiệm thực hiện thẩm tra an toàn giao thông đường bộ theo quy định tại khoản 2 Điều 29 Luật Đường bộ, chịu trách nhiệm về kết quả thẩm tra; phát hiện các khả năng xảy ra tai nạn giao thông, đánh giá các yếu tố là nguyên nhân tai nạn giao thông, đề xuất giải pháp khắc phục nhằm bảo đảm giao thông trên đường bộ thông suốt, an toàn; lập báo cáo thẩm tra an toàn giao thông đường bộ gửi tổ chức, cá nhân có trách nhiệm thẩm định an toàn giao thông.


`LUAT35-2024/D29/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 29. Thẩm tra, thẩm định an toàn giao thông đường bộ
> 2. Thẩm tra an toàn giao thông đường bộ là việc tổ chức kinh doanh dịch vụ thẩm tra an toàn giao thông nghiên cứu, phân tích thiết kế cơ sở, thiết kế triển khai sau thiết kế cơ sở, báo cáo kinh tế - kỹ thuật xây dựng công trình, hồ sơ hoàn thành công trình, hồ sơ quản lý tuyến đường, nguyên nhân các vụ tai nạn giao thông và tiến hành kiểm tra hiện trường để phát hiện các khả năng tiềm ẩn tai nạn giao thông hoặc đánh giá nguyên nhân gây tai nạn giao thông để đề xuất giải pháp khắc phục nhằm bảo đảm giao thông trên tuyến thông suốt, an toàn.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "B", "answer": "", "gold_units": ["ND165-2024/D32/K4", "LUAT35-2024/D29/K2"], "required_numbers": []}
```

### W-da_buoc-049 · tier B · ND336-2025/D19/K1

Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ) · DAN_CHIEU → ND336-2025/D19/K1

`ND336-2025/D21/K3#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 21. Thẩm quyền lập biên bản vi phạm hành chính
> 3. Chức danh quy định tại khoản 1 Điều 19 có thẩm quyền lập biên bản vi phạm hành chính đối với các hành vi vi phạm được phân định tại khoản 9 Điều 16 của Nghị định này;


`ND336-2025/D19/K1#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 19. Thẩm quyền xử phạt của Cục trưởng Cục Đường bộ Việt Nam, Trưởng đoàn kiểm tra do Bộ trưởng Bộ Xây dựng thành lập, Giám đốc Sở Xây dựng, Trưởng đoàn kiểm tra do Cục trưởng Cục Đường bộ Việt Nam thành lập và Giám đốc Khu Quản lý đường bộ thuộc Cục Đường bộ Việt Nam
> 1. Giám đốc Khu Quản lý đường bộ thuộc Cục Đường bộ Việt Nam có quyền:
> a) Phạt cảnh cáo;
> b) Phạt tiền đến 37.500.000 đồng;
> c) Tước quyền sử dụng giấy phép có thời hạn hoặc đình chỉ hoạt động có thời hạn;
> d) Áp dụng các các biện pháp khắc phục hậu quả quy định tại Điều 3 Nghị định này.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "B", "answer": "", "gold_units": ["ND336-2025/D21/K3", "ND336-2025/D19/K1"], "required_numbers": []}
```

### W-da_buoc-050 · tier B · ND165-2024/D39/K1

Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ) · DAN_CHIEU → ND165-2024/D39/K1

`ND165-2024/D40/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 40. Cấp đổi chứng chỉ thẩm tra viên an toàn giao thông đường bộ
> 3. Cá nhân có nhu cầu cấp đổi chứng chỉ nộp hồ sơ theo một trong các hình thức trực tiếp, thông qua dịch vụ bưu chính hoặc trực tuyến tại cổng dịch vụ công đến Cục Đường bộ Việt Nam. Cục Đường bộ Việt Nam thực hiện tiếp nhận, kiểm tra hồ sơ và xử lý như sau:
> a) Đối với trường hợp nộp trực tiếp, sau khi kiểm tra thành phần hồ sơ, nếu đúng quy định thì tiếp nhận hồ sơ và viết phiếu hẹn trả kết quả; hướng dẫn cá nhân hoàn thiện hồ sơ đối với trường hợp không đủ thành phần hồ sơ;
> b) Đối với trường hợp nộp gián tiếp, trong phạm vi 02 ngày làm việc kể từ ngày nhận được hồ sơ, kiểm tra thành phần hồ sơ, nếu không đủ thành phần hồ sơ có văn bản thông báo đến cá nhân để bổ sung, hoàn thiện;
> c) Trong thời hạn 07 ngày làm việc kể từ khi nhận đủ hồ sơ theo quy định, cơ quan có thẩm quyền giải quyết thủ tục hành chính tiến hành thẩm định hồ sơ, nếu đủ điều kiện, cấp đổi chứng chỉ thẩm tra viên an toàn giao thông theo mẫu quy định tại khoản 1 Điều 39 của Nghị định này. Trường hợp không cấp chứng chỉ, phải có văn bản trả lời và nêu rõ lý do.


`ND165-2024/D39/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 39. Cấp chứng chỉ thẩm tra viên an toàn giao thông đường bộ
> 1. Chứng chỉ thẩm tra viên an toàn giao thông đường bộ (sau đây gọi là chứng chỉ) được Cục Đường bộ Việt Nam cấp và quản lý thống nhất trong phạm vi cả nước; mẫu chứng chỉ theo quy định tại Mẫu số 03 Phụ lục VIII kèm theo Nghị định này và có thời hạn 05 năm kể từ ngày cấp.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "B", "answer": "", "gold_units": ["ND165-2024/D40/K3", "ND165-2024/D39/K1"], "required_numbers": []}
```

### W-da_buoc-051 · tier B · ND165-2024/D27/K7

Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ) · DAN_CHIEU → ND165-2024/D27/K7

`ND165-2024/D29/K8#2026-07-01` · hiệu lực 2026-07-01 → nay

> Điều 29. Đấu nối đối với trường hợp kết nối với đường bộ không có trong các quy hoạch
> 8. Ủy ban nhân dân cấp tỉnh quyết định, tổ chức đấu nối đường địa phương thuộc phạm vi quản lý; tổ chức đóng nút giao hiện hữu đấu nối vào quốc lộ đối với các trường hợp: đã có nút giao thay thế; đã hoàn thành xây dựng đường bên, đường gom để việc đấu nối vào quốc lộ thông qua đường bên, đường gom; nút giao hiện hữu là điểm hay xảy ra tai nạn giao thông mà không được khắc phục, nút giao không bảo đảm khoảng cách, trừ trường hợp quy định tại khoản 7 Điều 27 Nghị định này.


`ND165-2024/D27/K7#2026-07-01` · hiệu lực 2026-07-01 → nay

> Điều 27. Kết nối giao thông các tuyến đường bộ
> 7. Trường hợp nút giao đấu nối các khu vực dân cư, cơ quan, tổ chức, cơ sở dịch vụ, sản xuất kinh doanh, các địa điểm khác đấu nối trực tiếp vào quốc lộ và đường chính đi qua khu vực, địa bàn mà tại các vị trí này, Ủy ban nhân dân các cấp, cơ quan, tổ chức quy định tại khoản 5 Điều này chưa xây dựng đường bên, đường gom, đường nhánh để gom các phương tiện tham gia giao thông thì được phép tồn tại nút giao hiện hữu cho đến khi có đường gom, đường bên, đường nhánh với điều kiện nút giao đó phải bảo đảm an toàn giao thông. Trường hợp nút giao đấu nối không bảo đảm an toàn giao thông theo quy chuẩn kỹ thuật quốc gia, tiêu chuẩn quốc gia thì phải khắc phục theo các quy chuẩn, tiêu chuẩn để bảo đảm an toàn giao thông.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "B", "answer": "", "gold_units": ["ND165-2024/D29/K8", "ND165-2024/D27/K7"], "required_numbers": []}
```

### W-da_buoc-052 · tier B · LUAT35-2024/D56/K9

Luật Đường bộ số 35/2024/QH15 · DAN_CHIEU → LUAT35-2024/D56/K9

`ND158-2024/D6/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 6. Kinh doanh vận tải hành khách bằng xe taxi
> 2. Xe ô tô kinh doanh vận tải hành khách bằng taxi
> a) Xe ô tô phải bảo đảm đúng theo quy định tại khoản 9 Điều 56 Luật Đường bộ;
> b) Phải có phù hiệu “XE TAXI” theo Mẫu số 04 Phụ lục XIII kèm theo Nghị định này và được dán cố định tại góc trên bên phải ngay sát phía dưới vị trí của Tem kiểm định, mặt trong kính chắn gió phía trước của xe; phải được niêm yết đầy đủ các thông tin trên xe theo quy định;
> c) Phải được niêm yết (dán cố định) cụm từ “XE TAXI” làm bằng vật liệu phản quang trên kính phía trước và kính phía sau xe với kích thước tối thiểu của cụm từ “XE TAXI” là 06 x 20 cm theo Mẫu số 05 Phụ lục XIII kèm theo Nghị định này. Trường hợp niêm yết bằng thiết bị điện tử phải bảo đảm cụm từ “XE TAXI” luôn được bật sáng và có kích thước tối thiểu là 06 x 20 cm.
> Được quyền lựa chọn gắn hộp đèn với chữ “TAXI” cố định trên nóc xe với kích thước tối thiểu là 12 x 30 cm. Trường hợp lựa chọn gắn hộp đèn với chữ “TAXI” cố định trên nóc xe thì không phải niêm yết (dán cố định) cụm từ “XE TAXI” trên kính phía trước và kính phía sau xe.


`LUAT35-2024/D56/K9#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 56. Hoạt động vận tải đường bộ
> 9. Kinh doanh vận tải hành khách bằng xe taxi là loại hình kinh doanh vận tải hành khách sử dụng xe ô tô chở người dưới 08 chỗ (không kể chỗ của người lái xe) để thực hiện vận tải theo yêu cầu của hành khách; tiền cước chuyến đi do hành khách lựa chọn theo một trong các phương thức sau đây:
> a) Tiền cước được tính thông qua đồng hồ tính tiền;
> b) Tiền cước được tính qua phần mềm tính tiền có kết nối trực tiếp với hành khách thông qua phương tiện điện tử;
> c) Tiền cước theo thoả thuận với đơn vị kinh doanh vận tải.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "B", "answer": "", "gold_units": ["ND158-2024/D6/K2", "LUAT35-2024/D56/K9"], "required_numbers": []}
```

### W-da_buoc-053 · tier B · ND336-2025/D3/K3

Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ) · DAN_CHIEU → ND336-2025/D3

`ND336-2025/D18/K4#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 18. Thẩm quyền xử phạt của Công an nhân dân
> 4. Trưởng Công an cấp xã có quyền:
> a) Phạt cảnh cáo;
> b) Phạt tiền đến 37.500.000 đồng;
> c) Tước quyền sử dụng giấy phép có thời hạn hoặc đình chỉ hoạt động có thời hạn;
> d) Áp dụng biện pháp khắc phục hậu quả quy định tại Điều 3 của Nghị định này.


`ND336-2025/D3/K1#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 3. Mức phạt tiền, hình thức xử phạt vi phạm hành chính, biện pháp khắc phục hậu quả và nguyên tắc áp dụng
> 1. Mức phạt tiền tối đa trong hoạt động đường bộ thuộc lĩnh vực giao thông đường bộ đối với cá nhân là 75.000.000 đồng và đối với tổ chức là 150.000.000 đồng.


`ND336-2025/D3/K2#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 3. Mức phạt tiền, hình thức xử phạt vi phạm hành chính, biện pháp khắc phục hậu quả và nguyên tắc áp dụng
> 2. Hình thức xử phạt chính
> a) Cảnh cáo;
> b) Phạt tiền.


`ND336-2025/D3/K3#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 3. Mức phạt tiền, hình thức xử phạt vi phạm hành chính, biện pháp khắc phục hậu quả và nguyên tắc áp dụng
> 3. Hình thức xử phạt bổ sung
> a) Đình chỉ việc tổ chức đào tạo;
> b) Đình chỉ hoạt động thi công;
> c) Tước quyền sử dụng phù hiệu cấp cho xe ô tô tham gia kinh doanh vận tải;
> d) Tước quyền sử dụng giấy phép kinh doanh vận tải.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "B", "answer": "", "gold_units": ["ND336-2025/D18/K4", "ND336-2025/D3"], "required_numbers": []}
```

### W-da_buoc-054 · tier B · ND158-2024/D17/K2

Nghị định số 158/2024/NĐ-CP (Quy định về hoạt động vận tải đường bộ) · DAN_CHIEU → ND158-2024/D17/K2/a

`ND158-2024/D75/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 75. Đơn vị cung cấp phần mềm ứng dụng hỗ trợ kết nối vận tải
> 1. Đơn vị cung cấp phần mềm ứng dụng hỗ trợ kết nối vận tải (không trực tiếp điều hành phương tiện, lái xe; không quyết định giá cước vận tải) phải chấp hành các quy định theo pháp luật về giao dịch điện tử, các pháp luật khác có liên quan và phải đáp ứng các yêu cầu sau:
> a) Ghi nhận yêu cầu vận chuyển của khách hàng và chuyển yêu cầu vận chuyển đến đơn vị kinh doanh vận tải đang tham gia trong phần mềm ứng dụng hỗ trợ kết nối vận tải;
> b) Thực hiện vai trò là đơn vị trung gian để xác nhận thực hiện đúng các nội dung đã thỏa thuận giữa đơn vị kinh doanh vận tải với khách hàng, trong đó bảo đảm thực hiện đúng giá cước vận tải đã niêm yết hoặc giá trị hợp đồng đã ký kết; phần mềm ứng dụng hỗ trợ kết nối vận tải cho đơn vị kinh doanh vận tải hành khách bằng xe taxi phải bảo đảm bảo tuân thủ theo quy định tại điểm c khoản 4 Điều 6 của Nghị định này; phần mềm ứng dụng hỗ trợ kết nối vận tải cho đơn vị kinh doanh vận tải hành khách theo hợp đồng phải bảo đảm tuân thủ theo quy định tại điểm a khoản 2 Điều 17 của Nghị định này;
> c) Ghi nhận đánh giá của khách hàng về chất lượng phục vụ của lái xe để thông tin đến đơn vị kinh …


`ND158-2024/D17/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 17. Quy định chung về Hợp đồng vận tải
> 2. Hợp đồng vận tải hành khách, hàng hóa (bao gồm hợp đồng văn bản giấy hoặc hợp đồng điện tử) phải có đầy đủ các nội dung tối thiểu sau:
> a) Thông tin về đơn vị kinh doanh vận tải ký hợp đồng: tên, địa chỉ, điện thoại, mã số thuế, người đại diện ký hợp đồng (tên, số định danh cá nhân (số căn cước công dân));
> b) Thông tin về hành khách hoặc người thuê vận tải (tổ chức hoặc cá nhân): tên, số định danh cá nhân (số căn cước công dân), địa chỉ, số điện thoại;
> c) Thông tin về thực hiện hợp đồng: thời gian bắt đầu thực hiện (ngày, giờ) và kết thúc hợp đồng; địa chỉ điểm đầu, địa chỉ điểm cuối và các điểm đón, trả khách (hoặc xếp, dỡ hàng hóa) trên hành trình vận chuyển; cự ly của hành trình vận chuyển (km); số lượng khách (hoặc khối lượng hàng hóa vận chuyển);
> d) Thông tin về giá trị hợp đồng và phương thức thanh toán;
> đ) Quy định về trách nhiệm của các bên tham gia thực hiện hợp đồng vận chuyển, trong đó thể hiện việc thực hiện nghĩa vụ thuế đối với nhà nước; quyền, nghĩa vụ của bên vận chuyển, hành khách hoặc người thuê vận tải; số điện thoại liên hệ tiếp nhận giải quyết phản ánh, khiếu nại, tố cáo của hành khách; cam kết trách nhiệm thực …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "B", "answer": "", "gold_units": ["ND158-2024/D75/K1", "ND158-2024/D17/K2"], "required_numbers": []}
```

### W-da_buoc-055 · tier C · TT72-2024-BCA/D6/K8

Thông tư số 72/2024/TT-BCA (Quy định quy trình điều tra, giải quyết tai nạn giao thông đường bộ của Cảnh sát giao thông) · DAN_CHIEU → TT72-2024-BCA/D6/K8/a

`TT72-2024-BCA/D8/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 8. Khám nghiệm hiện trường vụ tai nạn giao thông đường bộ
> 1. Việc khám nghiệm hiện trường đối với những vụ tai nạn giao thông đường bộ có một trong các dấu hiệu quy định tại điểm a, b khoản 8 Điều 6 Thông tư này thì được thực hiện theo quy định của pháp luật tố tụng hình sự.


`TT72-2024-BCA/D6/K8#2025-03-01` · hiệu lực 2025-03-01 → nay

> Điều 6. Giải quyết ban đầu khi cán bộ Cảnh sát giao thông làm nhiệm vụ tuần tra, kiểm soát phát hiện vụ tai nạn giao thông đường bộ hoặc được phân công đến hiện trường vụ tai nạn giao thông đường bộ
> 8. Khi thực hiện nhiệm vụ theo quy định tại các khoản 1, 2, 3, 4, 5, 6 và 7 Điều này
> a) Nếu phát hiện vụ tai nạn giao thông đường bộ có một trong các dấu hiệu về hậu quả: có người chết tại hiện trường, chết trên đường đi cấp cứu, đang cấp cứu mà chết, có nguy cơ chết; có người bị thương dập, nát, đứt, rời tay, chân; chấn thương sọ não; có từ 03 người trở lên bị thương gãy tay, chân trở lên hoặc có căn cứ xác định tổn hại cho sức khỏe với tỷ lệ tổn thương cơ thể từ 61% trở lên hoặc có căn cứ xác định thiệt hại tài sản từ 100 triệu đồng trở lên thì thực hiện như sau:
> Đối với cán bộ Cục Cảnh sát giao thông thì báo cáo Cục trưởng, cán bộ Phòng Cảnh sát giao thông Công an cấp tỉnh thì báo cáo Trưởng phòng để chuyển ngay cho Cơ quan Cảnh sát điều tra Công an cấp tỉnh có thẩm quyền điều tra, giải quyết;;
> b) Trường hợp vụ tai nạn giao thông đường bộ không thuộc điểm a Khoản này mà thuộc trách nhiệm điều tra giải quyết của Cục Cảnh sát giao thông và Phòng Cảnh sát giao thông Công an cấp tỉnh …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "C", "answer": "", "gold_units": ["TT72-2024-BCA/D8/K1", "TT72-2024-BCA/D6/K8"], "required_numbers": []}
```

### W-da_buoc-056 · tier C · TT72-2024-BCA/D5/K4

Thông tư số 72/2024/TT-BCA (Quy định quy trình điều tra, giải quyết tai nạn giao thông đường bộ của Cảnh sát giao thông) · DAN_CHIEU → TT72-2024-BCA/D5/K4

`TT72-2024-BCA/D20/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 20. Kiểm tra công tác điều tra, xác minh, giải quyết tai nạn giao thông đường bộ
> 2. Khi xảy ra vụ tai nạn giao thông đường bộ theo quy định tại khoản 4 Điều 5 Thông tư này hoặc theo chỉ đạo của lãnh đạo Bộ Công an, Cục Cảnh sát giao thông có trách nhiệm phối hợp với các đơn vị có liên quan và Công an địa phương nơi xảy ra vụ tai nạn giao thông đường bộ tiến hành kiểm tra công tác đảm bảo trật tự, an toàn giao thông để đánh giá nguyên nhân, xem xét trách nhiệm của cá nhân, tổ chức có liên quan để xảy ra vụ tai nạn giao thông đường bộ.


`TT72-2024-BCA/D5/K4#2025-03-01` · hiệu lực 2025-03-01 → nay

> Điều 5. Xử lý tin báo về tai nạn giao thông đường bộ
> 4. Trường hợp vụ tai nạn giao thông đường bộ có tình tiết phức tạp; làm chết từ 03 người trở lên; gây ùn tắc giao thông kéo dài liên tuyến, liên địa bàn, liên tỉnh; gây thảm họa hoặc cần thiết phải có sự phối hợp cứu nạn, cứu hộ, điều tiết, giải quyết ùn tắc giao thông của Công an nhiều tỉnh, thành phố trực thuộc Trung ương thì cơ quan, đơn vị nhận được tin báo vụ tai nạn giao thông đường bộ xử lý như sau:
> a) Vụ tai nạn giao thông đường bộ xảy ra trên tuyến do Cục Cảnh sát giao thông làm nhiệm vụ tuần tra, kiểm soát, xử lý vi phạm phải thông báo Giám đốc Công an cấp tỉnh, nơi xảy ra vụ tai nạn giao thông phối hợp giải quyết;
> b) Vụ tai nạn giao thông đường bộ xảy ra trên tuyến tuần tra, kiểm soát, xử lý vi phạm của Phòng Cảnh sát giao thông Công an cấp tỉnh phải báo cáo ngay Giám đốc Công an cấp tỉnh (qua Phòng Tham mưu) và báo cáo Bộ Công an (qua Cục Cảnh sát giao thông) để chỉ đạo giải quyết;;


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "C", "answer": "", "gold_units": ["TT72-2024-BCA/D20/K2", "TT72-2024-BCA/D5/K4"], "required_numbers": []}
```

### W-da_buoc-057 · tier C · LUAT36-2024/D83/K3

Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15 · DAN_CHIEU → LUAT36-2024/D83

`TT72-2024-BCA/D3/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 3. Tiêu chuẩn của cán bộ Cảnh sát giao thông làm nhiệm vụ điều tra, xác minh, giải quyết tai nạn giao thông đường bộ và phân công cán bộ điều tra, xác minh, giải quyết vụ tai nạn giao thông đường bộ
> 2. Phân công cán bộ điều tra, xác minh, giải quyết vụ tai nạn giao thông đường bộ
> a) Khi phân công cán bộ thụ lý điều tra, xác minh, giải quyết vụ tai nạn giao thông đường bộ phải có ít nhất 01 cán bộ thụ lý chính. Cán bộ thụ lý chính chịu trách nhiệm chung, cán bộ hỗ trợ (nếu có) chịu trách nhiệm đối với các nhiệm vụ được phân công;
> b) Cán bộ được phân công thụ lý điều tra, xác minh, giải quyết vụ tai nạn giao thông đường bộ thực hiện theo quy định tại Điều 83 Luật Trật tự an toàn giao thông đường bộ năm 2024, Thông tư này và các quy định của pháp luật khác có liên quan đến hoạt động điều tra, xác minh, giải quyết tai nạn giao thông đường bộ.


`LUAT36-2024/D83/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 83. Điều tra, giải quyết tai nạn giao thông đường bộ
> 1. Nguyên tắc điều tra, giải quyết tai nạn giao thông đường bộ được quy định như sau:
> a) Tất cả các vụ tai nạn giao thông đường bộ xảy ra phải được điều tra, giải quyết nhanh chóng, kịp thời, chính xác, khách quan, đúng quy định của pháp luật;
> b) Người gây tai nạn giao thông đường bộ thì tùy theo tính chất, mức độ vi phạm có thể bị xử lý vi phạm hành chính hoặc bị truy cứu trách nhiệm hình sự, nếu gây thiệt hại thì phải bồi thường theo quy định của pháp luật;
> c) Các tổ chức, cá nhân liên quan đến vụ tai nạn giao thông đường bộ có trách nhiệm phối hợp giải quyết;
> d) Không được lợi dụng, lạm dụng công tác điều tra, giải quyết tai nạn giao thông đường bộ để xâm phạm lợi ích của Nhà nước, quyền, lợi ích hợp pháp của tổ chức, cá nhân;
> đ) Đối với vụ tai nạn giao thông đường bộ liên quan đến người và phương tiện của cơ quan đại diện ngoại giao, cơ quan lãnh sự, cơ quan đại diện của tổ chức quốc tế tại Việt Nam thì thực hiện theo quy định của Luật này, pháp luật về quyền ưu đãi, miễn trừ ngoại giao và điều ước quốc tế có liên quan mà nước Cộng hòa xã hội chủ nghĩa Việt Nam là thành viên.


`LUAT36-2024/D83/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 83. Điều tra, giải quyết tai nạn giao thông đường bộ
> 2. Đối với tai nạn giao thông đường bộ có dấu hiệu tội phạm, việc điều tra, giải quyết thực hiện theo quy định của pháp luật về hình sự và pháp luật về tố tụng hình sự. Đối với tai nạn giao thông đường bộ chưa xác định có dấu hiệu tội phạm, nội dung điều tra, giải quyết tai nạn giao thông đường bộ bao gồm:
> a) Kiểm tra nồng độ cồn, chất ma túy, các chất kích thích khác mà pháp luật cấm sử dụng đối với người điều khiển phương tiện tham gia giao thông đường bộ liên quan đến tai nạn giao thông đường bộ;
> b) Khám nghiệm hiện trường, phương tiện, tử thi, công trình đường bộ liên quan trực tiếp đến vụ tai nạn giao thông đường bộ; thu thập thông tin, dữ liệu; xác định hậu quả thiệt hại về người và tài sản do tai nạn giao thông đường bộ gây ra;
> c) Tạm giữ phương tiện, đồ vật, tài liệu, giấy phép, chứng chỉ hành nghề của người điều khiển, phương tiện tham gia giao thông đường bộ;
> d) Ghi lời khai của những người điều khiển phương tiện tham gia giao thông đường bộ, người bị nạn, người làm chứng và những người có liên quan khác trong vụ tai nạn giao thông đường bộ;
> đ) Xem xét dấu vết trên thân thể người bị nạn; kiểm tra, xác minh điều …


`LUAT36-2024/D83/K3#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 83. Điều tra, giải quyết tai nạn giao thông đường bộ
> 3. Kết luận vụ tai nạn giao thông đường bộ phải xác định diễn biến, hậu quả thiệt hại, nguyên nhân, lỗi và điều kiện liên quan trực tiếp đến vụ tai nạn giao thông đường bộ; đề xuất xử lý vụ tai nạn giao thông đường bộ; kiến nghị cơ quan, tổ chức, cá nhân khắc phục khi phát hiện sơ hở, thiếu sót nhằm bảo đảm trật tự, an toàn giao thông đường bộ.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "C", "answer": "", "gold_units": ["TT72-2024-BCA/D3/K2", "LUAT36-2024/D83"], "required_numbers": []}
```

### W-da_buoc-058 · tier historical · TT35-2024-BGTVT/D43/K1

Thông tư số 35/2024/TT-BGTVT (Quy định về đào tạo, sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế; đào tạo, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ) · DAN_CHIEU → TT35-2024-BGTVT/D43/K1

`TT35-2024-BGTVT/D54/K6#2025-01-01` · hiệu lực 2025-01-01 → 2025-08-31

> Điều 54. Yêu cầu đối với Hệ thống thông tin về đào tạo, sát hạch, cấp giấy phép lái xe, chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ
> 6. Hệ thống thông tin giấy phép lái xe tại Cục Đường bộ Việt Nam
> a) Quản lý tối thiểu các thông tin: số giấy phép lái xe; xác nhận hoàn thành khóa đào tạo; họ, tên; số định danh cá nhân; ngày, tháng, năm sinh; quốc tịch; nơi cư trú; cơ sở đào tạo lái xe; hạng xe đào tạo; khoá đào tạo; ngày trúng tuyển; cơ quan sát hạch; địa điểm tổ chức sát hạch (trung tâm sát hạch lái xe hoặc sân tập lái dùng để sát hạch); ngày cấp, đổi, cấp lại giấy phép lái xe; cơ quan cấp, đổi, cấp lại giấy phép lái xe; hạng giấy phép lái xe; ngày hết hạn; số phôi giấy phép lái xe;
> b) Có khả năng tiếp nhận các thông tin tại điểm a khoản này từ hệ thống thông tin giấy phép lái xe tại Sở Giao thông vận tải;
> c) Có chức năng cấp giấy phép lái xe quốc tế theo quy định tại khoản 1 và khoản 2 Điều 43 Thông tư này;
> d) Có chức năng thu hồi giấy phép lái xe;
> đ) Có khả năng tra cứu thông tin giấy phép lái xe, thực hiện các nghiệp vụ về công tác đào tạo, sát hạch cấp giấy phép lái xe trên trang thông tin điện tử;
> e) Có khả năng kết nối, chia sẻ dữ liệu với cổng dịch vụ công …


`TT35-2024-BGTVT/D43/K1#2025-01-01` · hiệu lực 2025-01-01 → 2025-08-31

> Điều 43. Cấp giấy phép lái xe quốc tế
> 1. Đối với người Việt Nam, người nước ngoài có thẻ thường trú hoặc thẻ tạm trú tại Việt Nam, có giấy phép lái xe quốc gia do Việt Nam cấp bằng vật liệu PET. còn giá trị sử dụng, thực hiện như sau:
> a) Hồ sơ cấp IDP Đơn đề nghị cấp IDP theo mẫu quy định tại Phụ lục XXX kèm theo Thông tư này;
> b) Trình tự cấp IDP:
> Cá nhân khi nộp hồ sơ đề nghị trực tiếp tại Cục Đường bộ Việt Nam hoặc Sở Giao thông vận tải, phải xuất trình bản chính giấy phép lái xe quốc gia do Việt Nam cấp, hộ chiếu, thẻ thường trú (đối với người nước ngoài) để thực hiện kiểm tra tính chính xác, hợp pháp của việc cấp IDP và phải hoàn thành nghĩa vụ nộp lệ phí khi được tiếp nhận hồ sơ theo quy định; khi nộp đơn qua hệ thống dịch vụ công trực tuyến, cá nhân kê khai theo hướng dẫn và phải chịu trách nhiệm về tính chính xác, tính hợp pháp của nội dung đã kê khai, phải hoàn thành nghĩa vụ nộp lệ phí thông qua chức năng thanh toán lệ phí của hệ thống dịch vụ công trực tuyến và nộp phí sử dụng dịch vụ khác theo nhu cầu của cá nhân.
> Trường hợp đơn đề nghị không đúng theo quy định, cơ quan tiếp nhận đơn có trách nhiệm thông báo trực tiếp hoặc bằng văn bản hoặc qua hệ thống dịch vụ công …


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2025-08-31", "question_type": "da_buoc", "tier": "historical", "answer": "", "gold_units": ["TT35-2024-BGTVT/D54/K6", "TT35-2024-BGTVT/D43/K1"], "required_numbers": []}
```

### W-da_buoc-059 · tier historical · TT35-2024-BGTVT/D57/K1

Thông tư số 35/2024/TT-BGTVT (Quy định về đào tạo, sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế; đào tạo, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ) · DAN_CHIEU → TT35-2024-BGTVT/D57/K1

`TT35-2024-BGTVT/D63/K2#2025-01-01` · hiệu lực 2025-01-01 → 2025-08-31

> Điều 63. Cơ sở đào tạo
> 2. Đối với công tác quản lý hệ thống thông tin
> a) Đầu tư, bảo trì, nâng cấp trang thiết bị phần cứng, phần mềm hệ thống và mạng truyền số liệu của hệ thống thông tin đào tạo lái xe đặt tại cơ sở đào tạo lái xe;
> b) Tiếp nhận và tổ chức thực hiện phần mềm nghiệp vụ trong hệ thống thông tin đào tạo lái xe tại cơ sở đào tạo lái xe do Cục Đường bộ Việt Nam chuyển giao Tạo lập, đối chiếu, chịu trách nhiệm về tính chính xác của thông tin học viên, quá trình đào tạo, kết quả đào tạo, báo cáo 1, báo cáo 2 theo quy định. Tiếp nhận thông tin kết quả sát hạch lái xe của học viên đào tạo tại cơ sở của mình để quản lý và tổ chức cho học viên sát hạch lại theo quy định;
> c) Chịu trách nhiệm về tính chính xác, hợp pháp của các hồ sơ điện tử gửi hoặc truyền dữ liệu đến Sở Giao thông vận tải và Cục Đường bộ Việt Nam;
> d) Lưu trữ đầy đủ các thông tin theo quy định tại khoản 1 Điều 57 Thông tư này;
> đ) Ban hành quy chế đảm bảo an toàn an ninh thông tin, quy chế sử dụng phần cứng, phần mềm, tài khoản để đảm bảo sử dụng hệ thống thông tin an toàn, hiệu quả;
> e) Khai thác dữ liệu trên hệ thống thông tin được cài đặt, chuyển giao tại cơ sở đào tạo lái xe để phục vụ công tác thanh tra, …


`TT35-2024-BGTVT/D57/K1#2025-01-01` · hiệu lực 2025-01-01 → 2025-08-31

> Điều 57. Thời gian lưu trữ dữ liệu trên hệ thống thông tin
> 1. Thời gian lưu trữ dữ liệu về đào tạo và sát hạch cấp giấy phép lái xe tại cơ sở đào tạo lái xe và trung tâm sát hạch lái xe tối thiểu là 05 năm.


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2025-08-31", "question_type": "da_buoc", "tier": "historical", "answer": "", "gold_units": ["TT35-2024-BGTVT/D63/K2", "TT35-2024-BGTVT/D57/K1"], "required_numbers": []}
```

### W-da_buoc-060 · tier historical · TT35-2024-BGTVT/D15/K1

Thông tư số 35/2024/TT-BGTVT (Quy định về đào tạo, sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế; đào tạo, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ) · DAN_CHIEU → TT35-2024-BGTVT/D15/K1

`TT35-2024-BGTVT/D14/K3#2025-01-01` · hiệu lực 2025-01-01 → 2025-08-31

> Điều 14. Yêu cầu đối với người học lái xe
> 3. Người đã có giấy phép lái xe hạng B số tự động được đăng ký học để cấp mới giấy phép lái xe hạng B số cơ khí (số sàn), người đã có giấy phép lái xe hạng B được đăng ký học để cấp mới giấy phép lái xe hạng C1 và phải học đủ nội dung chương trình đào tạo lái xe theo quy định, hồ sơ của người học lái xe thực hiện theo quy định tại khoản 1 Điều 15 Thông tư này; trường hợp đạt kết quả sát hạch, cơ quan tổ chức sát hạch có văn bản đề nghị cơ quan đã cấp giấy phép xe cắt góc giấy phép lái xe cũ và có văn bản đề nghị Cục Đường bộ Việt Nam xóa số quản lý giấy phép lái xe đã cấp.


`TT35-2024-BGTVT/D15/K1#2025-01-01` · hiệu lực 2025-01-01 → 2025-08-31

> Điều 15. Hồ sơ của người học lái xe
> 1. Người học lái xe lần đầu lập 01 bộ hồ sơ, nộp trực tiếp tại cơ sở đào tạo và chụp ảnh trực tiếp lưu trữ trong cơ sở dữ liệu giấy phép lái xe. Hồ sơ bao gồm:
> a) Đơn đề nghị học, sát hạch để cấp giấy phép lái xe theo mẫu quy định tại Phụ lục XI ban hành kèm theo Thông tư này;
> b) Bản sao hoặc bản sao điện tử được chứng thực từ bản chính hoặc bản sao điện tử được cấp từ sổ gốc một trong các giấy tờ sau: thẻ tạm trú, thẻ thường trú, chứng minh thư ngoại giao, chứng minh thư công vụ (đối với người nước ngoài).


Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2025-08-31", "question_type": "da_buoc", "tier": "historical", "answer": "", "gold_units": ["TT35-2024-BGTVT/D14/K3", "TT35-2024-BGTVT/D15/K1"], "required_numbers": []}
```

## so_sanh — so sánh giữa loại xe hoặc chủ thể

### W-so_sanh-001 · tier A · ND168-2024/D32/K5

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · cosine TF-IDF 0.57

`ND168-2024/D28/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 28. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ
> 1. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với hành vi chở quá số người quy định được phép chở của phương tiện.

- CheTai phat_tien: 1.000.000–2.000.000 đồng (nêu tại ND168-2024/D28/K1)

`ND168-2024/D32/K5#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
> 5. Phạt tiền từ 800.000 đồng đến 1.200.000 đồng trên mỗi người vượt quá quy định được phép chở của phương tiện nhưng tổng mức phạt tiền tối đa không vượt quá 75.000.000 đồng đối với chủ phương tiện là cá nhân, từ 1.600.000 đồng đến 2.400.000 đồng trên mỗi người vượt quá quy định được phép chở của phương tiện nhưng tổng mức phạt tiền tối đa không vượt quá 150.000.000 đồng đối với chủ phương tiện là tổ chức giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại khoản 2 Điều 20 của Nghị định này hoặc trực tiếp điều khiển phương tiện thực hiện hành vi vi phạm quy định tại khoản 2 Điều 20 của Nghị định này.

- CheTai tuoc_quyen: 1–3 tháng phù hiệu (nêu tại ND168-2024/D32/K18/đ)
- CheTai phat_tien: 800.000–1.200.000 đồng (nêu tại ND168-2024/D32/K5)
- DiemGPLX: trừ 4 điểm (nêu tại ND168-2024/D32/K21/d)
- DiemGPLX: trừ 10 điểm (nêu tại ND168-2024/D32/K21/h)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D28/K1", "ND168-2024/D32/K5"], "required_numbers": [{"value": 1000000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}, {"value": 1, "unit": "thang"}, {"value": 3, "unit": "thang"}, {"value": 800000, "unit": "vnd"}, {"value": 1200000, "unit": "vnd"}, {"value": 4, "unit": "diem"}, {"value": 10, "unit": "diem"}]}
```

### W-so_sanh-002 · tier A · ND168-2024/D30/K1

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · cosine TF-IDF 0.76

`ND168-2024/D26/K10#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
> 10. Phạt tiền từ 40.000.000 đồng đến 60.000.000 đồng đối với đơn vị sản xuất, lắp ráp, nhập khẩu thiết bị ghi nhận hình ảnh người lái xe lắp trên xe ô tô, đơn vị cung cấp dịch vụ liên quan đến giám sát hành trình, ghi nhận hình ảnh người lái xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Làm sai lệch thông tin, dữ liệu của thiết bị giám sát hành trình của xe ô tô;
> b) Làm sai lệch thông tin, dữ liệu của thiết bị ghi nhận hình ảnh người lái xe lắp trên xe ô tô.

- CheTai phat_tien: 40.000.000–60.000.000 đồng (nêu tại ND168-2024/D26/K10)

`ND168-2024/D30/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 30. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe cứu thương
> 1. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với hành vi vi phạm điều khiển xe ô tô cứu thương không lắp thiết bị ghi nhận hình ảnh người lái xe hoặc có lắp thiết bị ghi nhận hình ảnh người lái xe nhưng không có tác dụng trong quá trình xe tham gia giao thông theo quy định hoặc làm sai lệch dữ liệu của thiết bị ghi nhận hình ảnh người lái xe lắp trên xe ô tô.

- CheTai phat_tien: 1.000.000–2.000.000 đồng (nêu tại ND168-2024/D30/K1)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D26/K10", "ND168-2024/D30/K1"], "required_numbers": [{"value": 40000000, "unit": "vnd"}, {"value": 60000000, "unit": "vnd"}, {"value": 1000000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}]}
```

### W-so_sanh-003 · tier B · ND336-2025/D8/K6

Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ) · cosine TF-IDF 0.51

`ND336-2025/D6/K2#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 6. Xử phạt hành vi vi phạm quy định về quản lý, vận hành, khai thác, bảo trì công trình hạ tầng kỹ thuật sử dụng chung với đường bộ
> 2. Phạt tiền từ 10.000.000 đồng đến 15.000.000 đồng đối với cá nhân, từ 20.000.000 đồng đến 30.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
> a) Quản lý, vận hành, khai thác, bảo trì công trình hạ tầng kỹ thuật sử dụng chung với đường bộ gây ảnh hưởng đến an toàn công trình đường bộ, an toàn giao thông đường bộ hoặc cản trở công tác vận hành, khai thác, bảo trì công trình đường bộ;
> b) Không thực hiện di dời, tháo dỡ công trình hạ tầng kỹ thuật sử dụng chung, công trình lắp đặt trong công trình kỹ thuật sử dụng chung khi có yêu cầu của người quản lý, sử dụng công trình đường bộ để đầu tư, xây dựng, nâng cấp, mở rộng và bảo trì công trình đường bộ.

- CheTai phat_tien: 10.000.000–15.000.000 đồng (nêu tại ND336-2025/D6/K2)
- CheTai phat_tien: 20.000.000–30.000.000 đồng (nêu tại ND336-2025/D6/K2)

`ND336-2025/D8/K6#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 8. Xử phạt các hành vi vi phạm quy định về thi công trong phạm vi bảo vệ kết cấu hạ tầng đường bộ
> 6. Phạt tiền từ 15.000.000 đồng đến 20.000.000 đồng đối với cá nhân, từ 30.000.000 đồng đến 40.000.000 đồng đối với tổ chức thực hiện hành vi vi phạm không xây dựng công trình đường bộ để bồi hoàn, thay thế cho phần công trình bị ảnh hưởng hoặc không bồi hoàn kinh phí để xây dựng đoạn đường thay thế theo quy định.

- CheTai phat_tien: 15.000.000–20.000.000 đồng (nêu tại ND336-2025/D8/K6)
- CheTai phat_tien: 30.000.000–40.000.000 đồng (nêu tại ND336-2025/D8/K6)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "B", "answer": "", "gold_units": ["ND336-2025/D6/K2", "ND336-2025/D8/K6"], "required_numbers": [{"value": 10000000, "unit": "vnd"}, {"value": 15000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}, {"value": 30000000, "unit": "vnd"}, {"value": 40000000, "unit": "vnd"}]}
```

### W-so_sanh-004 · tier B · ND336-2025/D9/K5

Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ) · cosine TF-IDF 0.54

`ND336-2025/D8/K2#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 8. Xử phạt các hành vi vi phạm quy định về thi công trong phạm vi bảo vệ kết cấu hạ tầng đường bộ
> 2. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với cá nhân, từ 6.000.000 đồng đến 10.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
> a) Thi công công trình trong phạm vi đất dành cho kết cấu hạ tầng đường bộ không thực hiện đúng biện pháp tổ chức giao thông trong hồ sơ kèm theo giấy phép thi công hoặc văn bản chấp thuận của cơ quan có thẩm quyền, trừ hành vi vi phạm quy định tại khoản 1; điểm b, điểm c khoản này; điểm a, điểm b khoản 3; điểm a, điểm b, điểm d khoản 4; điểm a, điểm b, điểm c khoản 5 Điều này;
> b) Để vật liệu, đất đá, phương tiện thi công ngoài phạm vi thi công gây cản trở giao thông;
> c) Không thu dọn ngay các biển báo hiệu, rào chắn, phương tiện, vật dụng thi công, các vật liệu tại phần đất của đường bộ, hành lang an toàn đường bộ theo nguyên trạng khi thi công xong.

- BienPhapBoSung: buộc thu dọn phương tiện, vật tư, vật liệu, đất đá, hàng hóa, máy móc, thiết bị, các loại vật dụng, vật cản khác (nêu tại ND336-2025/D8/K8/a)
- CheTai phat_tien: 3.000.000–5.000.000 đồng (nêu tại ND336-2025/D8/K2)
- CheTai phat_tien: 6.000.000–10.000.000 đồng (nêu tại ND336-2025/D8/K2)

`ND336-2025/D9/K5#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 9. Xử phạt các hành vi vi phạm quy định về quản lý, khai thác, bảo trì, bảo vệ kết cấu hạ tầng đường bộ
> 5. Phạt tiền từ 5.000.000 đồng đến 7.000.000 đồng đối với cá nhân, từ 10.000.000 đồng đến 14.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
> a) Khoan, đào, xẻ đường, hè phố trái phép;
> b) Phá dỡ trái phép, làm hư hỏng công trình phụ trợ gắn liền với đường bộ, cấu kiện, phụ kiện của công trình đường bộ, trừ hành vi vi phạm tại khoản 4; điểm а, điểm c và điểm d khoản này;
> c) Tự ý tháo, mở làm hư hỏng nắp cống, nắp ga các công trình ngầm, hệ thống tuy nen trên đường bộ;
> d) Nổ mìn hoặc khai thác đất, cát, đá, sỏi, khoáng sản khác làm ảnh hưởng đến an toàn công trình đường bộ;
> đ) Không có quy trình vận hành, khai thác, bảo trì đường bộ theo quy định hoặc không thực hiện đầy đủ các nội dung trong quy trình vận hành, khai thác, bảo trì đường bộ đã được phê duyệt.

- BienPhapBoSung: buộc khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra (nêu tại ND336-2025/D9/K6/b)
- CheTai phat_tien: 5.000.000–7.000.000 đồng (nêu tại ND336-2025/D9/K5)
- CheTai phat_tien: 10.000.000–14.000.000 đồng (nêu tại ND336-2025/D9/K5)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "B", "answer": "", "gold_units": ["ND336-2025/D8/K2", "ND336-2025/D9/K5"], "required_numbers": [{"value": 3000000, "unit": "vnd"}, {"value": 5000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}, {"value": 7000000, "unit": "vnd"}, {"value": 14000000, "unit": "vnd"}]}
```

### W-so_sanh-005 · tier A · ND168-2024/D7/K10

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · cosine TF-IDF 0.64

`ND168-2024/D12/K10#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 12. Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm khác về quy tắc giao thông đường bộ; sử dụng lòng đường, vỉa hè vào mục đích khác
> 10. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng đối với cá nhân, từ 8.000.000 đồng đến 12.000.000 đồng đối với tổ chức thực hiện hành vi không chấp hành yêu cầu kiểm tra, kiểm soát của người thi hành công vụ về bảo đảm trật tự, an toàn giao thông đường bộ, trừ các hành vi vi phạm quy định tại điểm b, điểm d khoản 11 Điều 6; điểm đ, điểm g khoản 9 Điều 7; điểm b, điểm d khoản 9 Điều 8; điểm c khoản 4 Điều 9; điểm b khoản 5 Điều 34 của Nghị định này.

- CheTai phat_tien: 4.000.000–6.000.000 đồng (nêu tại ND168-2024/D12/K10)
- CheTai phat_tien: 8.000.000–12.000.000 đồng (nêu tại ND168-2024/D12/K10)

`ND168-2024/D7/K10#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 7. Xử phạt, trừ điểm giấy phép lái của người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy vi phạm quy tắc giao thông đường bộ
> 10. Phạt tiền từ 10.000.000 đồng đến 14.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe không quan sát, giảm tốc độ hoặc dừng lại để bảo đảm an toàn theo quy định mà gây tai nạn giao thông; điều khiển xe chạy quá tốc độ quy định gây tai nạn giao thông; đi vào đường cao tốc, dừng xe, đỗ xe, quay đầu xe, lùi xe, vượt xe, chuyển hướng, chuyển làn đường không đúng quy định gây tai nạn giao thông; không đi đúng phần đường, làn đường, không giữ khoảng cách an toàn giữa hai xe theo quy định gây tai nạn giao thông hoặc đi vào đường có biển báo hiệu có nội dung cấm đi vào đối với loại phương tiện đang điều khiển, đi ngược chiều của đường một chiều, đi ngược chiều trên đường có biển “Cấm đi ngược chiều” gây tai nạn giao thông;
> b) Vi phạm quy định tại một trong các điểm, khoản sau của Điều này mà gây tai nạn giao thông: điểm a, điểm d, điểm đ, điểm g, điểm h, điểm i, điểm k khoản 1; điểm c, điểm đ, điểm g khoản 2; điểm b, điểm e, điểm g, điểm h, điểm k …

- CheTai phat_tien: 10.000.000–14.000.000 đồng (nêu tại ND168-2024/D7/K10)
- DiemGPLX: trừ 10 điểm (nêu tại ND168-2024/D7/K13/d)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D12/K10", "ND168-2024/D7/K10"], "required_numbers": [{"value": 4000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}, {"value": 8000000, "unit": "vnd"}, {"value": 12000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}, {"value": 14000000, "unit": "vnd"}, {"value": 10, "unit": "diem"}]}
```

### W-so_sanh-006 · tier A · ND168-2024/D8/K5

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · cosine TF-IDF 0.69

`ND168-2024/D6/K2#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
> 2. Phạt tiền từ 600.000 đồng đến 800.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Chuyển làn đường không đúng nơi cho phép hoặc không có tín hiệu báo trước hoặc chuyển làn đường không đúng quy định “mỗi lần chuyển làn đường chỉ được phép chuyển sang một làn đường liền kề hoặc chuyển làn đường không bảo đảm khoảng cách an toàn với xe phía trước, xe phía sau, xe hai bên”, trừ các hành vi vi phạm quy định tại điểm g khoản 5 Điều này;
> b) Chở người trên buồng lái quá số lượng quy định;
> c) Không tuân thủ các quy định về nhường đường tại nơi đường bộ giao nhau, trừ các hành vi vi phạm quy định tại điểm n, điểm o khoản 5 Điều này;
> d) Dừng xe, đỗ xe trên phần đường xe chạy ở đoạn đường ngoài đô thị nơi có lề đường rộng; dừng xe, đỗ xe không sát mép đường phía bên phải theo chiều đi ở nơi đường có lề đường hẹp hoặc không có lề đường; dừng xe, đỗ xe ngược với chiều lưu thông của làn đường; dừng xe, đỗ xe trên dải phân cách cố định ở giữa …

- CheTai phat_tien: 600.000–800.000 đồng (nêu tại ND168-2024/D6/K2)

`ND168-2024/D8/K5#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 8. Xử phạt người điều khiển xe máy chuyên dùng vi phạm quy tắc giao thông đường bộ
> 5. Phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Lùi xe, quay đầu xe trong hầm đường bộ;
> b) Không thực hiện biện pháp bảo đảm an toàn theo quy định khi phương tiện bị hư hỏng trên đoạn đường bộ giao nhau cùng mức với đường sắt;
> c) Dừng xe, đỗ xe trong hầm đường bộ không đúng nơi quy định; không có báo hiệu bằng đèn khẩn cấp, không đặt biển cảnh báo “Chú ý xe đỗ” (hoặc đèn cảnh báo) về phía sau xe khoảng cách đảm bảo an toàn khi dừng xe, đỗ xe trong hầm đường bộ trong trường hợp gặp sự cố kỹ thuật hoặc bất khả kháng khác buộc phải dừng xe, đỗ xe;
> d) Điều khiển xe có liên quan trực tiếp đến vụ tai nạn giao thông mà không dừng ngay phương tiện, không giữ nguyên hiện trường, không trợ giúp người bị nạn, trừ hành vi vi phạm quy định tại điểm c khoản 8 Điều này;
> đ) Chuyển hướng không nhường quyền đi trước cho: người đi bộ, xe lăn của người khuyết tật qua đường tại nơi có vạch kẻ đường dành cho người đi bộ; xe thô sơ đang đi trên phần đường dành cho xe thô sơ;
> e) Chuyển hướng không nhường đường cho: các xe đi ngược chiều; …

- CheTai phat_tien: 2.000.000–3.000.000 đồng (nêu tại ND168-2024/D8/K5)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D6/K2", "ND168-2024/D8/K5"], "required_numbers": [{"value": 600000, "unit": "vnd"}, {"value": 800000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}]}
```

### W-so_sanh-007 · tier A · ND168-2024/D35/K2

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · cosine TF-IDF 0.56

`ND168-2024/D12/K9#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 12. Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm khác về quy tắc giao thông đường bộ; sử dụng lòng đường, vỉa hè vào mục đích khác
> 9. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với cá nhân, từ 6.000.000 đồng đến 10.000.000 đồng đối với tổ chức thực hiện hành vi bày, bán máy móc, thiết bị, vật tư hoặc sản xuất, gia công hàng hóa trên lòng đường, vỉa hè,

- CheTai phat_tien: 3.000.000–5.000.000 đồng (nêu tại ND168-2024/D12/K9)
- CheTai phat_tien: 6.000.000–10.000.000 đồng (nêu tại ND168-2024/D12/K9)

`ND168-2024/D35/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 35. Xử phạt, trừ điểm giấy phép lái xe đối với người đua xe trái phép, tổ chức đua xe, xúi giục, cổ vũ đua xe trái phép
> 2. Phạt tiền từ 40.000.000 đồng đến 50.000.000 đồng đối với cá nhân, từ 80.000.000 đồng đến 100.000.000 đồng đối với tổ chức thực hiện hành vi vi phạm tổ chức đua xe trái phép.

- CheTai phat_tien: 40.000.000–50.000.000 đồng (nêu tại ND168-2024/D35/K2)
- CheTai phat_tien: 80.000.000–100.000.000 đồng (nêu tại ND168-2024/D35/K2)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D12/K9", "ND168-2024/D35/K2"], "required_numbers": [{"value": 3000000, "unit": "vnd"}, {"value": 5000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}, {"value": 40000000, "unit": "vnd"}, {"value": 50000000, "unit": "vnd"}, {"value": 80000000, "unit": "vnd"}, {"value": 100000000, "unit": "vnd"}]}
```

### W-so_sanh-008 · tier A · ND168-2024/D32/K1

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · cosine TF-IDF 0.57

`ND168-2024/D12/K5#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 12. Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm khác về quy tắc giao thông đường bộ; sử dụng lòng đường, vỉa hè vào mục đích khác
> 5. Phạt tiền từ 400.000 đồng đến 600.000 đồng đối với người được chở trên xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô, các loại xe tương tự xe gắn máy thực hiện một trong các hành vi vi phạm sau đây:
> a) Bám, kéo, đẩy xe khác, vật khác, dẫn dắt vật nuôi, mang vác vật cồng kềnh, đứng trên yên, giá đèo hàng hoặc ngồi trên tay lái của xe;
> b) Không đội “mũ bảo hiểm cho người đi mô tô, xe máy” hoặc đội “mũ bảo hiểm cho người đi mô tô, xe máy” không cài quai đúng quy cách khi tham gia giao thông trên đường bộ.

- CheTai phat_tien: 400.000–600.000 đồng (nêu tại ND168-2024/D12/K5)

`ND168-2024/D32/K1#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
> 1. Phạt tiền từ 200.000 đồng đến 300.000 đồng đối với cá nhân, từ 400.000 đồng đến 600.000 đồng đối với tổ chức là chủ xe mô tô, xe gắn máy và các loại xe tương tự xe mô tô, các loại xe tương tự xe gắn máy thực hiện một trong các hành vi vi phạm sau đây:
> a) Tự ý thay đổi nhãn hiệu, màu sơn của xe không đúng với chứng nhận đăng ký xe;
> b) Đưa phương tiện không có chứng nhận kiểm định khí thải xe mô tô, xe gắn máy hoặc có nhưng đã hết hạn sử dụng hoặc sử dụng chứng nhận kiểm định khí thải xe mô tô, xe gắn máy không do cơ quan có thẩm quyền cấp.

- BienPhapBoSung: buộc khôi phục lại nhãn hiệu, màu sơn ghi trong chứng nhận đăng ký xe theo quy định (nêu tại ND168-2024/D32/K19/a)
- CheTai phat_tien: 200.000–300.000 đồng (nêu tại ND168-2024/D32/K1)
- CheTai phat_tien: 400.000–600.000 đồng (nêu tại ND168-2024/D32/K1)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D12/K5", "ND168-2024/D32/K1"], "required_numbers": [{"value": 400000, "unit": "vnd"}, {"value": 600000, "unit": "vnd"}, {"value": 200000, "unit": "vnd"}, {"value": 300000, "unit": "vnd"}]}
```

### W-so_sanh-009 · tier A · ND168-2024/D19/K2

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · cosine TF-IDF 0.75

`ND168-2024/D18/K5#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 18. Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm quy định về điều kiện của người điều khiển xe cơ giới
> 5. Phạt tiền từ 2.000.000 đồng đến 4.000.000 đồng đối với người điều khiển xe mô tô hai bánh có dung tích xi-lanh đến 125 cm3 hoặc có công suất động cơ điện đến 11 kW và các loại xe tương tự xe mô tô thực hiện một trong các hành vi vi phạm sau đây:
> a) Không có giấy phép lái xe hoặc sử dụng giấy phép lái xe đã bị trừ hết điểm hoặc sử dụng giấy phép lái xe không do cơ quan có thẩm quyền cấp, giấy phép lái xe bị tẩy xóa, giấy phép lái xe không còn hiệu lực, giấy phép lái xe không phù hợp với loại xe đang điều khiển;
> b) Có giấy phép lái xe quốc tế do các nước tham gia Công ước của Liên hợp quốc về Giao thông đường bộ năm 1968 cấp (trừ giấy phép lái xe quốc tế do Việt Nam cấp) nhưng không mang theo giấy phép lái xe quốc gia phù hợp với loại xe được phép điều khiển;
> c) Sử dụng giấy phép lái xe không hợp lệ (giấy phép lái xe có số phôi ghi ở mặt sau không trùng với số phôi được cấp mới nhất trong hệ thống thông tin quản lý giấy phép lái xe).

- BienPhapBoSung: buộc nộp lại giấy phép lái xe bị tẩy xóa (nêu tại ND168-2024/D18/K10)
- CheTai phat_tien: 2.000.000–4.000.000 đồng (nêu tại ND168-2024/D18/K5)

`ND168-2024/D19/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 19. Xử phạt các hành vi vi phạm quy định về điều kiện của người điều khiển xe máy chuyên dùng
> 2. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng đối với người điều khiển xe máy chuyên dùng không có bằng (hoặc chứng chỉ) điều khiển xe máy chuyên dùng, không có giấy phép lái xe (hoặc sử dụng giấy phép lái xe đã bị trừ hết điểm, giấy phép lái xe không do cơ quan có thẩm quyền cấp, giấy phép lái xe bị tẩy xóa, giấy phép lái xe không còn hiệu lực) hoặc không có chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ.

- CheTai phat_tien: 4.000.000–6.000.000 đồng (nêu tại ND168-2024/D19/K2)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D18/K5", "ND168-2024/D19/K2"], "required_numbers": [{"value": 2000000, "unit": "vnd"}, {"value": 4000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}]}
```

### W-so_sanh-010 · tier A · ND168-2024/D18/K2

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · cosine TF-IDF 0.56

`ND168-2024/D13/K6#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 13. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo), xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tư xe ô tô vi phạm quy định về điều kiện của phương tiện khi tham gia giao thông
> 6. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Sử dụng chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe), giấy chứng nhận, tem kiểm định an toàn kỹ thuật và bảo vệ môi trường không do cơ quan có thẩm quyền cấp hoặc bị tẩy xóa; sử dụng chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe) không đúng số khung, số động cơ (số máy) của xe (kể cả rơ moóc và sơ mi rơ moóc);
> b) Điều khiển xe không có giấy chứng nhận hoặc tem kiểm …

- BienPhapBoSung: buộc nộp lại chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe), giấy chứng nhận, tem kiểm định an toàn kỹ thuật và bảo vệ môi trường, chứng nhận đăng ký xe bị tẩy xóa (nêu tại ND168-2024/D13/K11/d)
- CheTai tich_thu: phương tiện (nêu tại ND168-2024/D13/K10/b)
- CheTai phat_tien: 4.000.000–6.000.000 đồng (nêu tại ND168-2024/D13/K6)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D13/K13/a)

`ND168-2024/D18/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 18. Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm quy định về điều kiện của người điều khiển xe cơ giới
> 2. Phạt tiền từ 200.000 đồng đến 300.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy kinh doanh vận tải không mang theo chứng nhận bảo hiểm bắt buộc trách nhiệm dân sự của chủ xe cơ giới còn hiệu lực;
> b) Người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy không có chứng nhận bảo hiểm bắt buộc trách nhiệm dân sự của chủ xe cơ giới còn hiệu lực;
> c) Người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy kinh doanh vận tải không mang theo chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe);
> d) Người điều khiển xe mô tô và các loại xe tương tự xe mô tô kinh doanh vận tải không mang theo giấy phép lái xe trừ hành vi vi phạm quy định tại điểm b khoản 5, điểm …

- CheTai phat_tien: 200.000–300.000 đồng (nêu tại ND168-2024/D18/K2)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D13/K6", "ND168-2024/D18/K2"], "required_numbers": [{"value": 4000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}, {"value": 200000, "unit": "vnd"}, {"value": 300000, "unit": "vnd"}]}
```

### W-so_sanh-011 · tier A · ND168-2024/D9/K1

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · cosine TF-IDF 0.62

`ND168-2024/D8/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 8. Xử phạt người điều khiển xe máy chuyên dùng vi phạm quy tắc giao thông đường bộ
> 4. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Chạy quá tốc độ quy định từ 10 km/h đến 20 km/h;
> b) Chạy xe trong hầm đường bộ không sử dụng đèn chiếu sáng gần;
> c) Không tuân thủ các quy định về dừng xe, đỗ xe tại nơi đường bộ giao nhau cùng mức với đường sắt; dừng xe, đỗ xe trong phạm vi bảo vệ công trình đường sắt, phạm vi an toàn của đường sắt;
> d) Quay đầu xe tại nơi đường bộ giao nhau cùng mức với đường sắt; quay đầu xe tại nơi đường hẹp, đường dốc, đoạn đường cong tầm nhìn bị che khuất, nơi có biển báo hiệu có nội dung cấm quay đầu đối với loại phương tiện đang điều khiển; điều khiển xe rẽ trái tại nơi có biển báo hiệu có nội dung cấm rẽ trái đối với loại phương tiện đang điều khiển; điều khiển xe rẽ phải tại nơi có biển báo hiệu có nội dung cấm rẽ phải đối với loại phương tiện đang điều khiển;
> đ) Quay đầu xe ở phần đường dành cho người đi bộ qua đường, trên cầu, đầu cầu, ngầm, gầm cầu vượt, trừ khi có hiệu lệnh của người điều khiển giao thông hoặc chỉ dẫn của biển báo hiệu tạm thời hoặc tổ chức giao thông …

- CheTai phat_tien: 1.000.000–2.000.000 đồng (nêu tại ND168-2024/D8/K4)

`ND168-2024/D9/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 9. Xử phạt người điều khiển xe đạp, xe đạp máy, người điều khiển xe thô sơ khác vi phạm quy tắc giao thông đường bộ
> 1. Phạt tiền từ 100.000 đồng đến 200.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Không đi bên phải theo chiều đi của mình, đi không đúng phần đường quy định;
> b) Dừng xe đột ngột; chuyển hướng không báo hiệu trước;
> c) Không chấp hành hiệu lệnh hoặc chỉ dẫn của biển báo hiệu, vạch kẻ đường, trừ các hành vi vi phạm quy định tại điểm đ khoản 2, điểm c khoản 3 Điều này;
> d) Vượt bên phải trong các trường hợp không được phép;
> đ) Dừng xe, đỗ xe trên phần đường xe chạy ở đoạn đường ngoài đô thị nơi có lề đường;
> e) Chạy trong hầm đường bộ không bật đèn hoặc không có vật phát sáng báo hiệu; dừng xe, đỗ xe trong hầm đường bộ không đúng nơi quy định; quay đầu xe trong hầm đường bộ;
> g) Điều khiển xe đạp, xe đạp máy đi dàn hàng ngang từ 03 xe trở lên, xe thô sơ khác đi dàn hàng ngang từ 02 xe trở lên;
> h) Người điều khiển xe đạp, xe đạp máy sử dụng ô (dù), dùng tay cầm và sử dụng điện thoại hoặc các thiết bị điện tử khác; chở người ngồi trên xe đạp, xe đạp máy sử dụng ô (dù);
> i) Điều khiển xe thô sơ trong thời gian từ 18 giờ ngày hôm …

- CheTai phat_tien: 100.000–200.000 đồng (nêu tại ND168-2024/D9/K1)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D8/K4", "ND168-2024/D9/K1"], "required_numbers": [{"value": 1000000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}, {"value": 100000, "unit": "vnd"}, {"value": 200000, "unit": "vnd"}]}
```

### W-so_sanh-012 · tier A · ND168-2024/D18/K3

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · cosine TF-IDF 0.59

`ND168-2024/D14/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 14. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy vi phạm quy định về điều kiện của phương tiện khi tham gia giao thông
> 2. Phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe không có chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe) hoặc sử dụng chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe) đã hết hạn sử dụng, hết hiệu lực;
> b) Sử dụng chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe) bị tẩy xóa; sử dụng …

- BienPhapBoSung: buộc thay thế thiết bị đủ tiêu chuẩn an toàn kỹ thuật hoặc khôi phục tính năng kỹ thuật của thiết bị theo quy định (nêu tại ND168-2024/D14/K6/a)
- BienPhapBoSung: buộc nộp lại chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe) đã bị tẩy xóa (nêu tại ND168-2024/D14/K6/b)
- CheTai phat_tien: 2.000.000–3.000.000 đồng (nêu tại ND168-2024/D14/K2)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D14/K8/a)

`ND168-2024/D18/K3#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 18. Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm quy định về điều kiện của người điều khiển xe cơ giới
> 3. Phạt tiền từ 300.000 đồng đến 400.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô kinh doanh vận tải không mang theo giấy phép lái xe, trừ hành vi vi phạm quy định tại điểm c khoản 8 Điều này;
> b) Người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ, rơ moóc, sơ mi rơ moóc và các loại xe tương tự xe ô tô kinh doanh vận tải không mang theo chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe);
> c) Người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ, rơ moóc, sơ mi rơ moóc và các loại xe tương tự xe ô tô kinh doanh vận tải không mang theo chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường đối với loại xe có quy định phải …

- CheTai phat_tien: 300.000–400.000 đồng (nêu tại ND168-2024/D18/K3)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D14/K2", "ND168-2024/D18/K3"], "required_numbers": [{"value": 2000000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}, {"value": 300000, "unit": "vnd"}, {"value": 400000, "unit": "vnd"}]}
```

### W-so_sanh-013 · tier A · ND168-2024/D11/K2

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · cosine TF-IDF 0.61

`ND168-2024/D10/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 10. Xử phạt người đi bộ vi phạm quy tắc giao thông đường bộ
> 1. Phạt tiền từ 150.000 đồng đến 250.000 đồng đối với người đi bộ thực hiện một trong các hành vi vi phạm sau đây:
> a) Không đi đúng phần đường quy định; vượt qua dải phân cách; đi qua đường không đúng nơi quy định; đi qua đường không có tín hiệu bằng tay theo quy định;
> b) Không chấp hành hiệu lệnh hoặc chỉ dẫn của đèn tín hiệu, biển báo hiệu, vạch kẻ đường, trừ hành vi vi phạm quy định tại điểm a khoản 2 Điều này;
> c) Không chấp hành hiệu lệnh, hướng dẫn của người điều khiển giao thông hoặc người kiểm soát giao thông.

- CheTai phat_tien: 150.000–250.000 đồng (nêu tại ND168-2024/D10/K1)

`ND168-2024/D11/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 11. Xử phạt người điều khiển, dẫn dắt vật nuôi, điều khiển xe vật nuôi kéo vi phạm quy tắc giao thông đường bộ
> 2. Phạt tiền từ 400.000 đồng đến 600.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Không chấp hành hiệu lệnh, hướng dẫn của người điều khiển giao thông hoặc người kiểm soát giao thông;
> b) Dẫn dắt vật nuôi chạy theo khi đang điều khiển hoặc ngồi trên phương tiện giao thông đường bộ;
> c) Điều khiển, dẫn dắt vật nuôi đi không đúng phần đường quy định, đi vào đường cấm, khu vực cấm, đi vào phần đường của xe cơ giới.

- CheTai phat_tien: 400.000–600.000 đồng (nêu tại ND168-2024/D11/K2)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D10/K1", "ND168-2024/D11/K2"], "required_numbers": [{"value": 150000, "unit": "vnd"}, {"value": 250000, "unit": "vnd"}, {"value": 400000, "unit": "vnd"}, {"value": 600000, "unit": "vnd"}]}
```

### W-so_sanh-014 · tier B · ND336-2025/D8/K1

Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ) · cosine TF-IDF 0.52

`ND336-2025/D6/K1#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 6. Xử phạt hành vi vi phạm quy định về quản lý, vận hành, khai thác, bảo trì công trình hạ tầng kỹ thuật sử dụng chung với đường bộ
> 1. Phạt tiền từ 6.000.000 đồng đến 10.000.000 đồng đối với cá nhân, từ 12.000.000 đồng đến 20.000.000 đồng đối với tổ chức thực hiện hành vi vi phạm không bố trí dấu hiệu nhận biết công trình hạ tầng thuộc sở hữu khi lắp đặt vào công trình hạ tầng kỹ thuật sử dụng chung với đường bộ.

- CheTai phat_tien: 6.000.000–10.000.000 đồng (nêu tại ND336-2025/D6/K1)
- CheTai phat_tien: 12.000.000–20.000.000 đồng (nêu tại ND336-2025/D6/K1)

`ND336-2025/D8/K1#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 8. Xử phạt các hành vi vi phạm quy định về thi công trong phạm vi bảo vệ kết cấu hạ tầng đường bộ
> 1. Phạt tiền từ 1.000.000 đồng đến 3.000.000 đồng đối với cá nhân, từ 2.000.000 đồng đến 6.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
> a) Thi công trên đường bộ đang khai thác không lắp thiết bị cảnh báo trên phương tiện, máy móc thi công;
> b) Không gửi biện pháp bảo đảm an toàn giao thông, an toàn công trình (biện pháp tổ chức giao thông) trước khi thi công trên đường bộ đang khai thác đến cơ quan quản lý đường bộ đối với trường hợp không phải cấp giấy phép thi công.

- CheTai phat_tien: 1.000.000–3.000.000 đồng (nêu tại ND336-2025/D8/K1)
- CheTai phat_tien: 2.000.000–6.000.000 đồng (nêu tại ND336-2025/D8/K1)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "B", "answer": "", "gold_units": ["ND336-2025/D6/K1", "ND336-2025/D8/K1"], "required_numbers": [{"value": 6000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}, {"value": 12000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}, {"value": 1000000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}]}
```

### W-so_sanh-015 · tier A · ND168-2024/D28/K2

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · cosine TF-IDF 0.70

`ND168-2024/D20/K7#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
> 7. Phạt tiền từ 5.000.000 đồng đến 7.000.000 đồng đối với hành vi vi phạm điều khiển xe chở hành khách không có hoặc không gắn phù hiệu theo quy định hoặc có nhưng đã hết giá trị sử dụng hoặc sử dụng phù hiệu không do cơ quan có thẩm quyền cấp.

- CheTai phat_tien: 5.000.000–7.000.000 đồng (nêu tại ND168-2024/D20/K7)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D20/K10/a)

`ND168-2024/D28/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 28. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ
> 2. Phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng đối với hành vi điều khiển xe chở người bốn bánh có gắn động cơ kinh doanh vận tải, xe chở hàng bốn bánh có gắn động cơ kinh doanh vận tải không có hoặc không gắn phù hiệu theo quy định hoặc có nhưng đã hết giá trị sử dụng hoặc sử dụng phù hiệu không do cơ quan có thẩm quyền cấp.

- CheTai phat_tien: 2.000.000–3.000.000 đồng (nêu tại ND168-2024/D28/K2)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D28/K4/a)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D20/K7", "ND168-2024/D28/K2"], "required_numbers": [{"value": 5000000, "unit": "vnd"}, {"value": 7000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}, {"value": 2000000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}]}
```

### W-so_sanh-016 · tier B · ND336-2025/D12/K2

Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ) · cosine TF-IDF 0.51

`ND336-2025/D10/K5#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 10. Xử phạt các hành vi vi phạm về thanh toán điện tử giao thông đường bộ, hoạt động trạm thu phí đường bộ
> 5. Phạt tiền từ 50.000.000 đồng đến 70.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
> a) Không thực hiện đúng quy trình quản lý, vận hành trạm thu phí theo quy định để số lượng xe ô tô xếp hàng chờ trước trạm thu phí trên một làn xe (tính từ cabin thu phí đến xe cuối cùng của hàng xe chờ) từ 750 m trở lên;
> b) Không thực hiện đúng quy trình quản lý, vận hành trạm thu phí theo quy định để thời gian đi qua trạm thu phí của một xe ô tô bất kỳ kể từ lúc dừng xe chờ thu phí đến lúc ra khỏi trạm thu phí lớn hơn 15 phút;
> c) Không thực hiện đúng quy trình quản lý, vận hành trạm thu phí theo quy định để xảy ra tai nạn giao thông đối với các phương tiện khi phương tiện tham gia giao thông qua trạm thu phí gây hậu quả từ mức nghiêm trọng trở lên;
> d) Không xây dựng hoặc xây dựng không đầy đủ quy trình nghiệp vụ quy định thời gian bù trừ, thanh toán, việc tra soát, đối chiếu dữ liệu;
> đ) Không thực hiện các quy trình nghiệp vụ do nhà cung cấp dịch vụ thanh toán điện tử giao thông ban hành;
> e) Không thực hiện quy trình đối soát; không khắc phục, điều chỉnh …

- CheTai phat_tien: 50.000.000–70.000.000 đồng (nêu tại ND336-2025/D10/K5)

`ND336-2025/D12/K2#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 12. Xử phạt các hành vi vi phạm quy định về vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
> 2. Phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng đối với cá nhân, từ 4.000.000 đồng đến 6.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
> a) Không thanh toán tiền vé cho hành khách đã mua vé nhưng từ chối chuyến đi trước khi xe khởi hành theo quy định đối với tuyến cố định;
> b) Không thực hiện đúng quy định về dán, thu hồi phù hiệu cấp cho xe ô tô tham gia kinh doanh vận tải;
> c) Không bố trí nhân sự thực hiện theo dõi, giám sát hoạt động của lái xe, phương tiện trong suốt quá trình tham gia kinh doanh vận tải theo quy định;
> d) Tiếp nhận, vận chuyển hàng hóa ký gửi không đúng quy định;
> đ) Không thực hiện việc miễn giảm giá vé đối với người cao tuổi, người khuyết tật và các đối tượng chính sách khác theo quy định;
> e) Không có hợp đồng đại lý bán vé với đơn vị kinh doanh vận tải hành khách bằng xe buýt, đơn vị kinh doanh vận tải theo tuyến cố định theo quy định.

- CheTai phat_tien: 2.000.000–3.000.000 đồng (nêu tại ND336-2025/D12/K2)
- CheTai phat_tien: 4.000.000–6.000.000 đồng (nêu tại ND336-2025/D12/K2)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "B", "answer": "", "gold_units": ["ND336-2025/D10/K5", "ND336-2025/D12/K2"], "required_numbers": [{"value": 50000000, "unit": "vnd"}, {"value": 70000000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}, {"value": 4000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}]}
```

### W-so_sanh-017 · tier A · ND168-2024/D9/K5

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · cosine TF-IDF 0.69

`ND168-2024/D10/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 10. Xử phạt người đi bộ vi phạm quy tắc giao thông đường bộ
> 2. Phạt tiền từ 400.000 đồng đến 600.000 đồng đối với người đi bộ thực hiện một trong các hành vi vi phạm sau đây:
> a) Đi vào đường cao tốc, trừ người phục vụ việc quản lý, bảo trì đường cao tốc;
> b) Mang, vác vật cồng kềnh gây cản trở giao thông;
> c) Đu, bám vào phương tiện giao thông đang chạy.

- CheTai phat_tien: 400.000–600.000 đồng (nêu tại ND168-2024/D10/K2)

`ND168-2024/D9/K5#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 9. Xử phạt người điều khiển xe đạp, xe đạp máy, người điều khiển xe thô sơ khác vi phạm quy tắc giao thông đường bộ
> 5. Phạt tiền từ 800.000 đồng đến 1.200.000 đồng đối với người điều khiển xe đi vào đường cao tốc, trừ phương tiện phục vụ việc quản lý, bảo trì đường cao tốc.

- CheTai phat_tien: 800.000–1.200.000 đồng (nêu tại ND168-2024/D9/K5)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D10/K2", "ND168-2024/D9/K5"], "required_numbers": [{"value": 400000, "unit": "vnd"}, {"value": 600000, "unit": "vnd"}, {"value": 800000, "unit": "vnd"}, {"value": 1200000, "unit": "vnd"}]}
```

### W-so_sanh-018 · tier A · ND168-2024/D26/K5

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · cosine TF-IDF 0.71

`ND168-2024/D21/K2#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
> 2. Phạt tiền từ 800.000 đồng đến 1.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe (kể cả rơ moóc và sơ mi rơ moóc) chở hàng vượt trọng tải (khối lượng hàng chuyên chở) cho phép tham gia giao thông được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe trên 10% đến 30% (trừ xe xi téc chở chất lỏng), trên 20% đến 30% đối với xe xi téc chở chất lỏng;
> b) Chở hàng trên nóc thùng xe; chở hàng vượt quá bề rộng thùng xe (kể cả bề rộng rơ moóc và sơ mi rơ moóc); chở hàng vượt phía trước, phía sau thùng xe (kể cả rơ moóc và sơ mi rơ moóc) trên 10% chiều dài toàn bộ của xe theo thiết kế được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe, trừ hành vi vi phạm quy định tại điểm d khoản 8 Điều 21 Nghị định này
> c) Chở người trên mui xe;
> d) Điều khiển xe kéo theo rơ moóc, sơ mi rơ moóc mà khối lượng toàn bộ (bao gồm khối lượng …

- CheTai phat_tien: 800.000–1.000.000 đồng (nêu tại ND168-2024/D21/K2)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D21/K13/a)

`ND168-2024/D26/K5#2026-08-15` · hiệu lực 2026-08-15 → nay

> Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
> 5. Phạt tiền từ 4.000.000 đồng đến 5.000.000 đồng đối với cá nhân, từ 8.000.000 đồng đến 10.000.000 đồng đối với tổ chức xếp hàng hóa lên mỗi xe ô tô (kể cả rơ moóc và sơ mi rơ moóc) vượt quá trọng tải (khối lượng hàng chuyên chở) cho phép tham gia giao thông được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe trên 100%.

- CheTai phat_tien: 4.000.000–5.000.000 đồng (nêu tại ND168-2024/D26/K5)
- CheTai phat_tien: 8.000.000–10.000.000 đồng (nêu tại ND168-2024/D26/K5)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D21/K2", "ND168-2024/D26/K5"], "required_numbers": [{"value": 800000, "unit": "vnd"}, {"value": 1000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}, {"value": 4000000, "unit": "vnd"}, {"value": 5000000, "unit": "vnd"}, {"value": 8000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}]}
```

### W-so_sanh-019 · tier A · ND168-2024/D8/K1

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · cosine TF-IDF 0.92

`ND168-2024/D6/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
> 1. Phạt tiền từ 400.000 đồng đến 600.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Không chấp hành hiệu lệnh, chỉ dẫn của biển báo hiệu, vạch kẻ đường, trừ các hành vi vi phạm quy định tại điểm a, điểm c, điểm d, điểm đ khoản 2; điểm a, điểm d, điểm đ, điểm e, điểm n, điểm o khoản 3; điểm a, điểm b, điểm đ, điểm e, điểm i, điểm k, điểm l khoản 4; điểm a, điểm b, điểm c, điểm d, điểm đ, điểm i, điểm k khoản 5; điểm a khoản 6; khoản 7; điểm b, điểm d khoản 9; điểm a khoản 10; điểm đ khoản 11 Điều này;
> b) Khi ra, vào vị trí dừng xe, đỗ xe không có tín hiệu báo cho người điều khiển phương tiện khác biết;
> c) Không báo hiệu bằng đèn khẩn cấp hoặc không đặt biển cảnh báo “Chú ý xe đỗ” theo quy định trong trường hợp gặp sự cố kỹ thuật (hoặc bất khả kháng khác) buộc phải đỗ xe chiếm một phần đường xe chạy hoặc tại nơi không được phép đỗ xe, trừ hành vi vi phạm quy định tại điểm c khoản 7 Điều này;
> d) Không gắn biển báo hiệu ở phía trước …

- CheTai phat_tien: 400.000–600.000 đồng (nêu tại ND168-2024/D6/K1)

`ND168-2024/D8/K1#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 8. Xử phạt người điều khiển xe máy chuyên dùng vi phạm quy tắc giao thông đường bộ
> 1. Phạt tiền từ 400.000 đồng đến 600.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Không chấp hành hiệu lệnh, chỉ dẫn của biển báo hiệu, vạch kẻ đường, trừ các hành vi vi phạm quy định tại điểm a, điểm b, điểm c, điểm đ khoản 2; điểm a, điểm d, điểm đ khoản 3; khoản 4; điểm a, điểm c khoản 5; điểm a, điểm b, điểm d, điểm đ, điểm e, điểm i khoản 6; điểm c, điểm d khoản 7; điểm a, điểm b khoản 8; điểm đ khoản 9 Điều này;
> b) Không báo hiệu bằng đèn khẩn cấp hoặc không đặt biển cảnh báo “Chú ý xe đỗ” theo quy định trong trường hợp gặp sự cố kỹ thuật (hoặc bất khả kháng khác) buộc phải đỗ xe chiếm một phần đường xe chạy hoặc tại nơi không được phép đỗ xe, trừ hành vi vi phạm quy định tại điểm b khoản 6 Điều này.

- CheTai phat_tien: 400.000–600.000 đồng (nêu tại ND168-2024/D8/K1)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D6/K1", "ND168-2024/D8/K1"], "required_numbers": [{"value": 400000, "unit": "vnd"}, {"value": 600000, "unit": "vnd"}]}
```

### W-so_sanh-020 · tier A · ND168-2024/D32/K10

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · cosine TF-IDF 0.50

`ND168-2024/D12/K2#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 12. Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm khác về quy tắc giao thông đường bộ; sử dụng lòng đường, vỉa hè vào mục đích khác
> 2. Phạt tiền từ 200.000 đồng đến 250.000 đồng đối với cá nhân thực hiện một trong các hành vi vi phạm sau đây:
> a) Tập trung đông người trái phép, nằm, ngồi trên đường bộ gây cản trở giao thông;
> b) Đá bóng, đá cầu, chơi cầu lông hoặc các hoạt động thể thao khác trái phép trên đường bộ; sử dụng bàn trượt, pa-tanh, các thiết bị tương tự trên phần đường xe chạy;
> c) Điều khiển vật thể bay, tàu bay không người lái, phương tiện bay siêu nhẹ hoạt động trong phạm vi khổ giới hạn đường bộ gây cản trở hoặc nguy cơ mất an toàn cho người, phương tiện tham gia giao thông đường bộ, trừ tàu bay không người lái, phương tiện bay siêu nhẹ được cấp phép bay;
> d) Người được chở trên xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy sử dụng ô (dù);
> đ) Người được chở trên xe đạp, xe đạp máy bám, kéo, đẩy xe khác, vật khác, mang vác vật cồng kềnh;
> e) Bán hàng rong hoặc bán hàng hóa nhỏ lẻ khác trên lòng đường, trên vỉa hè các tuyến phố có quy định cấm bán hàng; trừ các hành vi vi phạm quy định tại khoản 7, khoản 9 Điều …

- CheTai phat_tien: 200.000–250.000 đồng (nêu tại ND168-2024/D12/K2)

`ND168-2024/D32/K10#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
> 10. Phạt tiền từ 8.000.000 đồng đến 10.000.000 đồng đối với cá nhân, từ 16.000.000 đồng đến 20.000.000 đồng đối với tổ chức là chủ xe mô tô, xe gắn máy và các loại xe tương tự xe mô tô, các loại xe tương tự xe gắn máy thực hiện hành vi vi phạm giao xe hoặc để cho người không đủ điều kiện theo quy định tại khoản 1 Điều 56 của Luật Trật tự, an toàn giao thông đường bộ điều khiển xe tham gia giao thông (bao gồm cả trường hợp người điều khiển phương tiện có giấy phép lái xe nhưng đang trong thời gian bị tước quyền sử dụng).

- CheTai phat_tien: 8.000.000–10.000.000 đồng (nêu tại ND168-2024/D32/K10)
- CheTai phat_tien: 16.000.000–20.000.000 đồng (nêu tại ND168-2024/D32/K10)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D12/K2", "ND168-2024/D32/K10"], "required_numbers": [{"value": 200000, "unit": "vnd"}, {"value": 250000, "unit": "vnd"}, {"value": 8000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}, {"value": 16000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}]}
```

### W-so_sanh-021 · tier B · ND336-2025/D12/K3

Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ) · cosine TF-IDF 0.52

`ND336-2025/D11/K2#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 11. Xử phạt người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ kinh doanh vận tải vi phạm quy định về vận tải đường bộ
> 2. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với việc thực hiện một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe taxi không có đồng hồ tính tiền cước (đối với loại xe đăng ký sử dụng đồng hồ tính tiền) hoặc có nhưng không đúng quy định hoặc có nhưng không sử dụng đồng hồ để tính tiền cước theo yêu cầu của hành khách hoặc can thiệp để điều chỉnh tiền cước hiển thị trên đồng hồ;
> b) Điều khiển xe taxi sử dụng phần mềm tính tiền mà trên xe không có thiết bị để kết nối trực tiếp với hành khách theo quy định;
> c) Điều khiển xe taxi không sử dụng phần mềm tính tiền (đối với loại xe đăng ký sử dụng phần mềm tính tiền) hoặc sử dụng phần mềm tính tiền không bảo đảm các yêu cầu theo quy định;
> d) Điều khiển xe kinh doanh vận tải hành khách theo tuyến cố định thu tiền vé cao hơn giá vé đã kê khai và niêm yết theo quy định.

- CheTai phat_tien: 1.000.000–2.000.000 đồng (nêu tại ND336-2025/D11/K2)

`ND336-2025/D12/K3#2026-03-01` · hiệu lực 2026-03-01 → nay

> Điều 12. Xử phạt các hành vi vi phạm quy định về vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
> 3. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với cá nhân, từ 6.000.000 đồng đến 10.000.000 đồng đối với tổ chức kinh doanh vận tải, dịch vụ hỗ trợ vận tải thực hiện một trong các hành vi vi phạm sau đây:
> a) Sử dụng xe ô tô chở người từ 08 chỗ (không kể chỗ của người lái xe) trở lên hoặc xe ô tô chở người có thiết kế, cải tạo với số chỗ ít hơn 08 chỗ từ xe ô tô lớn hơn 08 chỗ (không kể chỗ của người lái xe) để kinh doanh vận tải hành khách bằng xe taxi;
> b) Không bố trí người trực tiếp điều hành hoạt động vận tải hoặc có bố trí nhưng không đáp ứng đủ điều kiện theo quy định;
> c) Sử dụng phương tiện thuộc sở hữu của thành viên hợp tác xã để kinh doanh vận tải bằng xe ô tô, xe bốn bánh có gắn động cơ mà không có hợp đồng dịch vụ giữa thành viên với hợp tác xã theo quy định hoặc sử dụng phương tiện không thuộc quyền sử dụng hợp pháp để kinh doanh vận tải bằng xe ô tô, xe bốn bánh có gắn động cơ;
> d) Bến xe không xác nhận hoặc xác nhận không chính xác, đầy đủ các thông tin trong lệnh vận chuyển theo quy định hoặc xác nhận vào lệnh vận chuyển khi xe không có ở bến;
> đ) Bến xe cho …

- CheTai phat_tien: 3.000.000–5.000.000 đồng (nêu tại ND336-2025/D12/K3)
- CheTai phat_tien: 6.000.000–10.000.000 đồng (nêu tại ND336-2025/D12/K3)
- CheTai tuoc_quyen: 1–3 tháng phù hiệu cấp cho xe ô tô tham gia kinh doanh vận tải (nêu tại ND336-2025/D12/K8/a)
- CheTai tuoc_quyen: 1–3 tháng giấy phép kinh doanh vận tải (nêu tại ND336-2025/D12/K8/b)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "B", "answer": "", "gold_units": ["ND336-2025/D11/K2", "ND336-2025/D12/K3"], "required_numbers": [{"value": 1000000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}, {"value": 5000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}, {"value": 1, "unit": "thang"}, {"value": 3, "unit": "thang"}]}
```

### W-so_sanh-022 · tier A · ND168-2024/D9/K4

Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe) · cosine TF-IDF 0.51

`ND168-2024/D7/K6#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 7. Xử phạt, trừ điểm giấy phép lái của người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy vi phạm quy tắc giao thông đường bộ
> 6. Phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Điều khiển xe trên đường mà trong máu hoặc hơi thở có nồng độ cồn nhưng chưa vượt quá 50 miligam/100 mililít máu hoặc chưa vượt quá 0,25 miligam/1 lít khí thở;
> b) Đi vào khu vực cấm, đường có biển báo hiệu có nội dung cấm đi vào đối với loại phương tiện đang điều khiển, trừ các hành vi vi phạm quy định tại điểm a, điểm b khoản 7 Điều này và các trường hợp xe ưu tiên đang đi làm nhiệm vụ khẩn cấp theo quy định;
> c) Không giảm tốc độ (hoặc dừng lại) và nhường đường khi điều khiển xe đi từ đường không ưu tiên ra đường ưu tiên, từ đường nhánh ra đường chính;
> d) Không giảm tốc độ và nhường đường cho xe đi đến từ bên phải tại nơi đường giao nhau không có báo hiệu đi theo vòng xuyến; không giảm tốc độ và nhường đường cho xe đi đến từ bên trái tại nơi đường giao nhau có báo hiệu đi theo vòng xuyến.

- CheTai phat_tien: 2.000.000–3.000.000 đồng (nêu tại ND168-2024/D7/K6)
- DiemGPLX: trừ 2 điểm (nêu tại ND168-2024/D7/K13/a)
- DiemGPLX: trừ 4 điểm (nêu tại ND168-2024/D7/K13/b)

`ND168-2024/D9/K4#2025-01-01` · hiệu lực 2025-01-01 → nay

> Điều 9. Xử phạt người điều khiển xe đạp, xe đạp máy, người điều khiển xe thô sơ khác vi phạm quy tắc giao thông đường bộ
> 4. Phạt tiền từ 400.000 đồng đến 600.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
> a) Gây tai nạn giao thông không dừng ngay phương tiện, không giữ nguyên hiện trường, không trợ giúp người bị nạn, không ở lại hiện trường hoặc không đến trình báo ngay với cơ quan công an, Ủy ban nhân dân nơi gần nhất;
> b) Điều khiển xe trên đường mà trong máu hoặc hơi thở có nồng độ cồn vượt quá 80 miligam/100 mililít máu hoặc vượt quá 0,4 miligam/1 lít khí thở;
> c) Không chấp hành yêu cầu kiểm tra về nồng độ cồn của người thi hành công vụ;
> d) Người điều khiển xe đạp máy không đội “mũ bảo hiểm cho người đi mô tô, xe máy” hoặc đội “mũ bảo hiểm cho người đi mô tô, xe máy” không cài quai đúng quy cách khi tham gia giao thông trên đường bộ;
> đ) Chở người ngồi trên xe đạp máy không đội “mũ bảo hiểm cho người đi mô tô, xe máy” hoặc đội “mũ bảo hiểm cho người đi mô tô, xe máy” không cài quai đúng quy cách, trừ trường hợp chở người bệnh đi cấp cứu, trẻ em dưới 06 tuổi, áp giải người có hành vi vi phạm pháp luật.

- CheTai phat_tien: 400.000–600.000 đồng (nêu tại ND168-2024/D9/K4)

Mẫu dòng:

```json
{"qid": "", "question": "", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "", "gold_units": ["ND168-2024/D7/K6", "ND168-2024/D9/K4"], "required_numbers": [{"value": 2000000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}, {"value": 4, "unit": "diem"}, {"value": 400000, "unit": "vnd"}, {"value": 600000, "unit": "vnd"}]}
```

