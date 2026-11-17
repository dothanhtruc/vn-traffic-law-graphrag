Bạn hỗ trợ một sinh viên luật soạn **bản nháp** câu hỏi kiểm tra cho hệ thống hỏi đáp Luật Giao thông đường bộ Việt Nam. Đợt này cần các câu **nằm ngoài phạm vi dữ liệu**: hệ thống đúng là phải **từ chối** trả lời chúng.

## Phạm vi dữ liệu của hệ thống (câu hỏi KHÔNG được thuộc phạm vi này)

Dữ liệu chỉ gồm văn bản về **giao thông đường bộ Việt Nam** còn hiệu lực đến 03/11/2026: Luật Trật tự, an toàn giao thông đường bộ 2024; Luật Đường bộ 2024; nghị định xử phạt vi phạm hành chính giao thông đường bộ và trừ điểm giấy phép lái xe; quy định về giấy phép lái xe, sát hạch, đào tạo lái xe, đổi giấy phép lái xe (kể cả giấy phép nước ngoài sang Việt Nam); đăng ký xe, biển số; đăng kiểm, kiểm định xe; kinh doanh vận tải đường bộ; tốc độ, khoảng cách; kết cấu hạ tầng, quản lý, bảo trì đường bộ; phí sử dụng đường bộ; tuần tra, kiểm soát; xử lý tai nạn giao thông đường bộ; sức khoẻ người lái xe.

Mọi câu hỏi mà một trong các văn bản trên trả lời được (dù chỉ một phần) đều **không** đạt yêu cầu.

## Nhiệm vụ

Viết **$n câu hỏi khác nhau** thuộc nhóm sau, mỗi câu kèm câu trả lời tham chiếu là **lời từ chối**.

- Nhóm: `$category` — $category_desc
- Người hỏi (vai): $persona
- Kiểu câu: $style

## Quy tắc

1. Tiếng Việt có dấu, lời người dân, theo vai và kiểu câu đã cho; 8 đến 50 từ mỗi câu.
2. Câu hỏi phải **rõ ràng nằm ngoài phạm vi** trên. Có thể nhắc tới xe cộ hay đường sá nếu chủ đề chính vẫn ngoài phạm vi (ví dụ tàu hỏa, tàu thủy, máy bay; luật của nước khác áp dụng ở nước đó; bồi thường dân sự theo hợp đồng).
3. Các câu phải khác nhau về chủ đề, không chỉ khác vài từ.
4. Câu trả lời tham chiếu: 1–2 câu, nói rằng câu hỏi nằm ngoài phạm vi dữ liệu về Luật Giao thông đường bộ Việt Nam và nêu ngắn gọn lý do. Không trả lời nội dung câu hỏi, không nêu con số.

## Định dạng trả lời

Chỉ trả về một đối tượng JSON, không viết gì thêm:

{"questions": [{"question": "...", "answer": "..."}]}
