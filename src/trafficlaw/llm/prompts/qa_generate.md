Bạn giúp xây dựng dữ liệu huấn luyện cho hệ thống tìm kiếm văn bản pháp luật giao thông đường bộ Việt Nam. Đọc đoạn văn bản pháp luật bên dưới và viết $n câu hỏi khác nhau mà một NGƯỜI DÂN có thể gõ vào ô tìm kiếm, sao cho đoạn văn bản này chứa câu trả lời.

Yêu cầu:
1. Viết bằng tiếng Việt tự nhiên, như người dân hỏi (ví dụ "Đi xe máy không đội mũ bảo hiểm bị phạt bao nhiêu?"), mỗi câu 8–35 từ. KHÔNG chép nguyên câu của văn bản; diễn đạt lại bằng lời thường.
2. Mỗi câu hỏi phải tự đứng được, không nhắc "điều này", "khoản này", "đoạn trên", "văn bản này". Có thể nêu tên văn bản nếu tự nhiên, nhưng không bắt buộc.
3. Chỉ dùng con số (mức tiền, số điểm, số tháng, tốc độ, số chỗ…) có trong đoạn văn bản; không bịa thêm số. Câu hỏi không cần chứa đáp án.
4. Các câu hỏi nên hỏi những khía cạnh khác nhau của đoạn văn bản (hành vi, đối tượng, mức xử phạt, điều kiện, thủ tục, cơ quan…), tránh lặp ý.
5. Gán mỗi câu một loại trong danh sách:
$types

Văn bản: $doc

Đoạn văn bản:
$text

Trả về DUY NHẤT một JSON object (không giải thích, không markdown) dạng:
{"questions": [{"question": "...", "question_type": "..."}]}
