# Rà 99 câu test có nhắc công ty/doanh nghiệp/tổ chức (17/11/2026)

Phạm vi: câu trong `data/qa/test.jsonl` (500 câu, `+reviewed`) có "công ty|doanh nghiệp|tổ chức" trong câu hỏi mà đáp án không có chữ "tổ chức". Claude rà, đối chiếu nguyên văn gold tại `as_of`. Người dùng xác nhận trước khi áp dụng.

Tiêu chí mức phạt tổ chức: quy tắc "tổ chức gấp 2 lần cá nhân" nằm ở Luật Xử lý vi phạm hành chính (**không có trong dữ liệu**) ⇒ chỉ tính sai khi Khoản gold **tự nêu mức tổ chức** và người vi phạm trong câu hỏi là tổ chức.

## Tổng hợp

| Kết luận | Số câu | Ý nghĩa |
| --- | ---: | --- |
| OK | 58 | Câu hỏi + đáp án khớp nguồn (công ty chỉ là bối cảnh, hoặc đáp án đã nêu mức tổ chức) |
| SAI_TO_CHUC | 3 | Tổ chức vi phạm, Khoản nêu mức tổ chức, đáp án nêu mức cá nhân |
| SAI_NOI_DUNG | 26 | Hành vi/chủ thể/khoản lệch nguồn, hoặc đáp án bịa thông tin không có trong nguồn |
| MO_HO | 12 | Câu hỏi khó hiểu, tiền đề vô lý hoặc đáp án không trả lời được câu hỏi |

Nguyên nhân lặp lại:

1. **Vai người hỏi lệch chủ thể của điều khoản**: TT 72/2024-BCA (quy trình nội bộ của Cảnh sát giao thông), ND158 Đ64 (nhiệm vụ cơ quan quản lý) bị hỏi dưới vai "chủ doanh nghiệp vận tải" ⇒ đáp án gán nghĩa vụ của công an cho doanh nghiệp.
2. **Hành vi trong câu hỏi lệch hành vi của Điểm gold** (cùng mức phạt, khác hành vi): bien_phap-013, bien_phap-034, so_sanh-016…
3. **Nhầm điều khoản thẩm quyền xử phạt ("Phạt tiền đến 37.500.000 đồng") với mức phạt**: da_buoc-028, cặp t2-theo_thoi_diem-032.
4. **Đáp án bịa** hồ sơ, thời hạn, hậu quả không có trong nguồn: thu_tuc-051, thu_tuc-052, t2-thu_tuc-019, t2-da_buoc-006.

## Chi tiết câu không đạt (41)

| qid | Kết luận | Lý do |
| --- | --- | --- |
| t-muc_phat-066 | SAI_TO_CHUC | Công ty cho thuê xe không ký hợp đồng: tổ chức 16–20 triệu, đáp án nêu 8–10 triệu (cá nhân) |
| t2-muc_phat-014 | SAI_TO_CHUC | "Công ty tôi chưa có giấy phép đào tạo": tổ chức 30–40 triệu, đáp án nêu 15–20 triệu |
| t3-so_sanh-019 | SAI_TO_CHUC | Chủ xe là công ty: tổ chức 56–60 triệu, đáp án nêu 28–30 triệu |
| t-bien_phap-013 | SAI_NOI_DUNG | Hỏi "không kiểm tra điều kiện xe"; Khoản 3 Đ16 là xe máy chuyên dùng sản xuất/cải tạo trái quy định |
| t-bien_phap-034 | SAI_NOI_DUNG | Hỏi lắp biển quảng cáo; Điểm c là tháo dỡ/di chuyển trái phép công trình đường bộ |
| t-da_buoc-028 | SAI_NOI_DUNG | Lấy thẩm quyền Trưởng Công an xã (phạt đến 37,5 triệu) làm mức phạt; hành vi không liên quan |
| t-da_buoc-034 | SAI_NOI_DUNG | Đáp án bịa yêu cầu về lái xe; nguồn chỉ nói trẻ < 10 tuổi và < 1,35 m không ngồi cùng hàng ghế lái |
| t-da_buoc-044 | SAI_NOI_DUNG | Đ64 K3 ND158 là nhiệm vụ cơ quan quản lý, đáp án gán cho công ty |
| t-hanh_vi_cam_nghia_vu-044 | SAI_NOI_DUNG | Tài xế tự tổ chức buổi học ≠ cơ sở đào tạo người điều khiển xe máy chuyên dùng |
| t-hanh_vi_cam_nghia_vu-051 | SAI_NOI_DUNG | Đáp án "không được đăng ký tuyến chưa công bố" trái với K2 Đ22 (có thủ tục cho tuyến mới) |
| t-hanh_vi_cam_nghia_vu-066 | SAI_NOI_DUNG | Nguồn là nghĩa vụ ("phải đồng bộ NTP"), đáp án nói "được phép"; chủ thể là máy chủ dịch vụ/Cục CSGT |
| t-so_sanh-008 | SAI_NOI_DUNG | K5 Đ12 là người được chở, không phải người lái bám xe; kết luận so sánh tự mâu thuẫn |
| t-so_sanh-016 | SAI_NOI_DUNG | Hỏi nhận hàng ký gửi; Điểm a là không hoàn tiền vé |
| t-thu_tuc_tham_quyen-035 | SAI_NOI_DUNG | Hỏi cấp GPLX mới; Khoản là sát hạch lại do quá hạn/mất |
| t-thu_tuc_tham_quyen-051 | SAI_NOI_DUNG | Gold là thu hồi phù hiệu/giấy phép; đáp án bịa hồ sơ xin cấp |
| t-thu_tuc_tham_quyen-052 | SAI_NOI_DUNG | Gold là đối tượng áp dụng ND165; đáp án bịa thủ tục |
| t-thu_tuc_tham_quyen-066 | SAI_NOI_DUNG | Biểu mẫu TT72 là của Cảnh sát giao thông, không phải doanh nghiệp nộp |
| t-tru_diem-002 | SAI_NOI_DUNG | Trừ điểm K14/a áp cho cá nhân kinh doanh vận tải tự lái, không phải lái xe của công ty |
| t2-bien_phap-004 | SAI_NOI_DUNG | Chủ xe là tổ chức không bị trừ điểm GPLX; đáp án nói "mất điểm" |
| t2-da_buoc-001 | SAI_NOI_DUNG | Đáp án nói "xử phạt theo Luật 36" — Luật không quy định mức phạt |
| t2-da_buoc-006 | SAI_NOI_DUNG | Đáp án bịa hậu quả "thu hồi, phạt tiền" không có trong nguồn |
| t2-da_buoc-047 | SAI_NOI_DUNG | Cập nhật Phần mềm Tổng hợp là việc của công an, không phải chủ doanh nghiệp |
| t2-theo_thoi_diem-032a | SAI_NOI_DUNG | Thẩm quyền (phạt đến 37,5 triệu) bị coi là mức phạt tối đa của công ty (bỏ cả cặp) |
| t2-theo_thoi_diem-032b | SAI_NOI_DUNG | Như trên (60 triệu) |
| t2-thu_tuc_tham_quyen-019 | SAI_NOI_DUNG | Đáp án bịa các bước, thời gian "vài tháng đến một năm" |
| t3-theo_thoi_diem-010a | SAI_NOI_DUNG | Cặp: K3 Đ64 sau mốc nói về Trung tâm quản lý, không còn "camera giám sát hành trình" (bỏ cả cặp) |
| t3-theo_thoi_diem-010b | SAI_NOI_DUNG | Như trên |
| t4-da_buoc-014 | SAI_NOI_DUNG | Báo cáo Cục trưởng/Trưởng phòng là quy trình nội bộ CSGT, không phải nghĩa vụ chủ doanh nghiệp |
| t4-da_buoc-015 | SAI_NOI_DUNG | Như trên |
| t-da_buoc-020 | MO_HO | Không xác định được xe có phải "thông minh"; "cần cấp phép" không có trong nguồn |
| t-da_buoc-031 | MO_HO | Tiền đề vô lý: nhân viên 17 tuổi đã có GPLX hạng B |
| t-dinh_nghia-015 | MO_HO | Câu hỏi vô nghĩa ("tốc độ 80 có được coi là 80"); đáp án không trả lời |
| t-hanh_vi_cam_nghia_vu-006 | MO_HO | Công ty xây đường cao tốc "có được không" — nguồn là điều kiện đầu tư, không trả lời được/không |
| t-muc_phat-024 | MO_HO | Không nêu vượt bao nhiêu km/h; xe máy trên đường cao tốc là hành vi khác |
| t-thu_tuc_tham_quyen-004 | MO_HO | Hỏi hồ sơ, nơi nộp, thời gian; đáp án chỉ nói ngày tiếp nhận |
| t-thu_tuc_tham_quyen-005 | MO_HO | "GPLX quốc tế" không đổi được (nguồn là GPLX nước ngoài) |
| t-thu_tuc_tham_quyen-041 | MO_HO | Đáp án chỉ nhắc đối tượng áp dụng, không trả lời "cần làm gì" |
| t2-bien_phap-016 | MO_HO | Hỏi vượt tốc độ trong khu kinh tế; gold Đ38 là hành vi khác, đáp án điều kiện "nếu tái phạm" |
| t2-bien_phap-018 | MO_HO | Tiền đề "công ty đã bán xe" mà hỏi tịch thu GPLX; biện pháp khắc phục không có trong gold |
| t2-da_buoc-026 | MO_HO | Xe chở khách của công ty "dẫn đường cho cảnh sát" — tiền đề vô lý |
| t2-thu_tuc_tham_quyen-007 | MO_HO | "Mất bao lâu" — đáp án nói "phụ thuộc cơ quan" |

## Câu đạt (58)

11 câu `ngoai_pham_vi`; t-da_buoc-004, -025, -042; t-dinh_nghia-001, -002, -006, -007, -021, -024, -028, -031; t-hanh_vi_cam_nghia_vu-003, -027, -045, -048, -068, -070; t-muc_phat-003, -005, -015, -022, -026, -028, -048, -057, -062, -073, -074; t-so_sanh-007; t-thu_tuc_tham_quyen-006; t-tru_diem-006; t2-dinh_nghia-004, -020, -031; t2-hanh_vi_cam_nghia_vu-030; t2-muc_phat-008; t2-theo_thoi_diem-001a/b, -008a/b, -013a/b, -036a/b; t2-thu_tuc_tham_quyen-008; t3-so_sanh-007, -021.
