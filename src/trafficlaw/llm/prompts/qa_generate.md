Bạn giúp xây dựng dữ liệu huấn luyện cho hệ thống tìm kiếm văn bản pháp luật giao thông đường bộ Việt Nam. Đọc đoạn văn bản pháp luật bên dưới và viết $n câu hỏi khác nhau mà một NGƯỜI DÂN có thể gõ vào ô tìm kiếm, sao cho đoạn văn bản này chứa câu trả lời.

Yêu cầu:
1. Chỉ hỏi điều mà CHÍNH đoạn văn bản này trả lời được. Không hỏi về nội dung không có trong đoạn (dù liên quan đến giao thông); đoạn càng ngắn, câu hỏi càng phải bám sát đúng nội dung đoạn.
2. Viết bằng tiếng Việt tự nhiên, như người dân hỏi, mỗi câu 8–35 từ. KHÔNG chép nguyên câu của văn bản; diễn đạt lại bằng lời thường.
3. Mỗi câu hỏi phải tự đứng được, không nhắc "điều này", "khoản này", "đoạn trên", "văn bản này", không hỏi "Điều N nói về gì". Có thể nêu tên văn bản nếu tự nhiên, nhưng không bắt buộc.
4. Chỉ dùng con số (mức tiền, số điểm, số tháng, tốc độ, số chỗ…) có trong đoạn văn bản; không bịa thêm số. Câu hỏi không cần chứa đáp án.
5. Các câu hỏi nên hỏi những khía cạnh khác nhau của đoạn văn bản (hành vi, đối tượng, mức xử phạt, điều kiện, thủ tục, cơ quan…), tránh lặp ý.
6. Gán mỗi câu một loại trong danh sách:
$types

Văn bản: $doc

Đoạn văn bản:
$text

Trả về DUY NHẤT một JSON object (không giải thích, không markdown) dạng:
{"questions": [{"question": "...", "question_type": "..."}]}
