# Rà toàn bộ câu test nháp (17/11/2026)

Claude rà từng câu so với nguyên văn gold tại `as_of` (kể cả điều khoản được dẫn chiếu khi cần); người dùng xác nhận trước khi dùng. Kết quả từng câu: `data/qa/test_review.jsonl`.

| Loại | Đã rà | OK | SAI_NOI_DUNG | MO_HO | SAI_TO_CHUC | Tỷ lệ đạt |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| bien_phap | 36 | 12 | 19 | 5 | 0 | 33% |
| da_buoc | 71 | 25 | 21 | 25 | 0 | 35% |
| dinh_nghia | 41 | 27 | 8 | 6 | 0 | 66% |
| hanh_vi_cam_nghia_vu | 74 | 31 | 29 | 14 | 0 | 42% |
| muc_phat | 83 | 47 | 25 | 9 | 2 | 57% |
| ngoai_pham_vi | 35 | 35 | 0 | 0 | 0 | 100% |
| so_sanh | 32 | 12 | 16 | 3 | 1 | 38% |
| theo_thoi_diem | 52 | 20 | 18 | 14 | 0 | 38% |
| thu_tuc_tham_quyen | 79 | 25 | 34 | 20 | 0 | 32% |
| tru_diem | 31 | 17 | 6 | 8 | 0 | 55% |
| **Tổng** | 534 | 251 | 176 | 104 | 3 | 47% |

## Lỗi hệ thống của nháp (gpt-oss-20b)

1. **Gán nghĩa vụ của cơ quan nhà nước/CSGT/đơn vị kinh doanh cho người hỏi** (TT72, TT73, ND165, ND158, ND336 phần tổ chức) — nhóm lớn nhất.
2. **Lấy điều khoản thẩm quyền xử phạt ('phạt tiền đến X') làm mức phạt** (ND168 Đ41–Đ45, ND336 Đ17–Đ20).
3. **Hành vi trong câu hỏi lệch Điểm gold** (cùng mức phạt, khác hành vi) và **sai Điều theo loại xe** (Đ6 ô tô, Đ7 mô tô, Đ8 máy kéo/XMCD, Đ9 xe đạp/thô sơ).
4. **Trừ điểm sai**: nói 'trừ điểm' khi điểm đó không nằm trong danh sách của khoản trừ điểm, hoặc sai số điểm (02/04/06/10).
5. **Đáp án bịa** hồ sơ, thời hạn, cơ quan ('Sở GTVT') không có trong nguồn.
6. **Tiền đề vô lý** do vai người hỏi (trẻ 12 tuổi lái xe, tài xế công nghệ tham gia dự án PPP…).

