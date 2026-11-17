Bạn hỗ trợ một sinh viên luật soạn **bản nháp** câu hỏi kiểm tra cho hệ thống hỏi đáp Luật Giao thông đường bộ Việt Nam. Người soạn sẽ đọc, sửa hoặc bỏ từng bản nháp của bạn. Bản nháp chỉ hữu ích khi nó **giống câu hỏi của người dân thật** và **đúng tuyệt đối với nguồn** dưới đây.

## Nhiệm vụ

Viết **2 bản nháp khác nhau** cho gợi ý dưới đây. Mỗi bản nháp gồm câu hỏi, đáp án tham chiếu, điều khoản căn cứ và con số bắt buộc. Hai bản nháp phải khác nhau về tình huống và cách hỏi, không chỉ khác vài từ.

- Loại câu: `$question_type` — $type_desc
- Tier văn bản: $tier
- Ngày áp dụng: $as_of
- Người hỏi (vai): $persona
- Kiểu câu: $style

$type_rules

## Nguồn (chỉ được dùng thông tin trong phần này)

$sources

## Con số tìm được bằng rule (chỉ được chọn trong danh sách này)

$numbers

## Quy tắc viết câu hỏi

1. Viết bằng tiếng Việt có dấu, **lời người dân**, theo đúng vai và kiểu câu đã cho. Dùng tình huống cụ thể (tôi / con tôi / công ty tôi…) khi kiểu câu cho phép.
   **Loại xe, chủ thể và hành vi trong câu hỏi phải đúng như nguồn** (nguồn nói ô tô chở khách thì không được hỏi về xe máy). Vai chỉ quyết định giọng hỏi và người kể; nếu vai không hợp với nguồn, giữ đúng nguồn (ví dụ để người đó hỏi giùm người thân).
   Nếu nguồn chỉ dẫn chiếu tới hành vi ở điều khoản khác ("hành vi quy định tại điểm a khoản 7"), hãy mô tả đúng hành vi đó theo phần "Điều khoản được nguồn trên dẫn chiếu tới"; không tự nghĩ ra hành vi.
2. **Không chép từ ngữ của điều luật.** Không có cụm **từ 6 từ liên tiếp trở lên** giống nguồn. Diễn đạt hành vi bằng cách người thường mô tả việc mình làm (ví dụ "chạy xe ra ngoài tuyến được phép", không viết "điều khiển xe hoạt động không đúng tuyến đường").
3. **Không nêu số Điều, Khoản, Điểm** trong câu hỏi. Chỉ nêu tên văn bản khi kiểu câu yêu cầu.
4. Không nêu đáp án hay con số cần hỏi trong câu hỏi. Con số mô tả tình huống (tốc độ, nồng độ cồn, tuổi…) chỉ được dùng khi nó nằm đúng trong phạm vi nguồn quy định.
5. Câu hỏi phải **trả lời được hoàn toàn từ nguồn**. Nếu cần thông tin ngoài nguồn mới trả lời được, hãy viết câu khác.
6. Một câu hỏi chỉ hỏi một việc, trừ khi loại câu yêu cầu nhiều bước hoặc so sánh.
7. Không dùng các cụm "theo quy định trên", "điều này", "văn bản này", "đoạn trên" (người hỏi không nhìn thấy nguồn).
8. Câu hỏi dài từ 8 đến 50 từ.

## Quy tắc viết đáp án tham chiếu

1. Viết từ 1 đến 4 câu. **Câu đầu là kết luận** trả lời thẳng câu hỏi.
2. Nêu **đủ mọi con số** mà câu hỏi cần, đúng nguyên văn nguồn (ví dụ "từ 8.000.000 đồng đến 12.000.000 đồng", "trừ 06 điểm"). **Không viết con số nào không có trong nguồn.**
3. Nêu căn cứ cuối đáp án, dạng "(khoản 3 Điều 28 Nghị định 168/2024/NĐ-CP)".
4. Nếu điều kiện hay ngoại lệ trong nguồn làm thay đổi kết luận, nêu ngắn gọn. Không thêm ý mà câu hỏi không hỏi.
5. Câu hỏi không nói rõ cá nhân hay tổ chức thì đáp án nêu mức của cá nhân, và ghi giả định vào `ghi_chu`.

## Các trường khác

- `gold_units`: tập mã điều khoản **nhỏ nhất đủ để trả lời**, chỉ chọn trong các mã có ở phần Nguồn. Ưu tiên mã Điểm nếu câu hỏi chỉ thuộc một Điểm.
- `required_numbers_idx`: chỉ số (bắt đầu từ 0) của các con số trong danh sách mà đáp án **bắt buộc** phải nêu. Bỏ số mà câu hỏi không hỏi tới.
- `ghi_chu`: giả định đã dùng, chỗ dễ nhầm (ví dụ "xe máy" là xe mô tô hay xe gắn máy).
- `nghi_ngo`: điều bạn không chắc khi đọc nguồn, để người soạn kiểm tra. Để chuỗi rỗng nếu không có.

## Định dạng trả lời

Chỉ trả về một đối tượng JSON, không viết gì thêm:

{"drafts": [{"questions": [{"as_of": "YYYY-MM-DD", "question": "...", "answer": "...", "gold_units": ["..."], "required_numbers_idx": [0]}], "ghi_chu": "...", "nghi_ngo": "..."}, {...}]}

Mảng `questions` có **1 phần tử**, trừ loại `theo_thoi_diem`: loại này có **2 phần tử** (ngày trước mốc, rồi ngày sau mốc).
