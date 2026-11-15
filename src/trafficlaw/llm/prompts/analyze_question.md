Bạn phân tích một câu hỏi tiếng Việt về pháp luật giao thông đường bộ Việt Nam để hệ thống tra cứu điều khoản. Chỉ trả về một đối tượng JSON đúng schema, không giải thích.

Điền các trường:

1. `as_of`: ngày áp dụng `YYYY-MM-DD` mà câu hỏi muốn hỏi, suy ra từ cụm thời gian trong câu (kể cả cụm tương đối như "năm ngoái", "trước khi Nghị định 168 có hiệu lực") so với ngày tham chiếu. "trước ngày D" là ngày D − 1. Câu hỏi không nói thời điểm, hoặc không suy ra được chắc chắn → `null`.
2. `vehicle_ids`: các loại phương tiện câu hỏi nhắc tới, **chỉ** chọn id trong danh mục phương tiện bên dưới. Không gộp các loại khác nhau: "xe gắn máy" khác "xe mô tô"; "xe máy" trong lời nói thường có thể là xe mô tô hoặc xe gắn máy — chọn cả hai nếu câu không nói rõ. Không có loại nào phù hợp → `[]`.
3. `subject_ids`: chủ thể (người, tổ chức, cơ quan) câu hỏi nhắc tới, **chỉ** chọn id trong danh mục chủ thể bên dưới. Không có → `[]`.
4. `question_type`: đúng một giá trị trong: $types.
   - `muc_phat`: hỏi mức phạt tiền/cảnh cáo; `tru_diem`: hỏi trừ/phục hồi điểm giấy phép lái xe; `bien_phap`: hỏi tước giấy phép, tịch thu, biện pháp khắc phục hậu quả;
   - `hanh_vi_cam_nghia_vu`: hỏi hành vi bị cấm, việc phải làm, điều kiện; `dinh_nghia`: hỏi một khái niệm là gì; `thu_tuc_tham_quyen`: hỏi thủ tục, hồ sơ, cơ quan/người có thẩm quyền;
   - `theo_thoi_diem`: hỏi quy định áp dụng tại một thời điểm cụ thể hoặc thay đổi theo thời gian; `da_buoc`: cần ghép nhiều điều khoản (vd hành vi ở một điều, mức phạt ở điều khác); `so_sanh`: so sánh hai quy định; `ngoai_pham_vi`: không thuộc pháp luật giao thông đường bộ.
5. `doc_hints`: mã văn bản (`doc_id` bên dưới) mà câu hỏi nêu tên hoặc số hiệu. Không nêu → `[]`.

Không trả lời câu hỏi, không nêu mức phạt, số điểm, thời hạn hay bất kỳ con số pháp lý nào.

Danh mục phương tiện:
$vehicles

Danh mục chủ thể:
$subjects

Văn bản (doc_id: số hiệu):
$docs

Ngày tham chiếu (hôm nay hoặc ngày người dùng chọn): $ref_date
Câu hỏi: $question
