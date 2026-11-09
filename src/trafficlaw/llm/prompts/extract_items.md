Bạn là chuyên gia pháp luật giao thông đường bộ Việt Nam. Nhiệm vụ: trích xuất thực thể từ các điều khoản dưới đây và trả về DUY NHẤT một JSON object đúng schema (không giải thích, không markdown).

Mỗi item (I1, I2, …) là một Điểm/Khoản/Điều. "Câu dẫn của khoản" chỉ là ngữ cảnh, KHÔNG trích xuất từ câu dẫn.

Với mỗi item, trả về một phần tử trong "items" có "id" đúng mã item và các trường:

1. "hanh_vi": các hành vi (vi phạm, bị cấm, hoặc nghĩa vụ phải làm) do CHÍNH item mô tả.
   - "span": chép NGUYÊN VĂN một đoạn liên tục của item mô tả hành vi (không sửa chữ, không thêm bớt từ, không lấy nhãn "a)", "1.").
   - Một item nêu nhiều hành vi khác nhau (ngăn bởi dấu ";" hoặc liệt kê) thì tách thành nhiều hành vi, mỗi hành vi một span.
   - Bỏ phần ngoại lệ "trừ các hành vi vi phạm quy định tại …" khỏi span.
   - "ten": tên ngắn gọn của hành vi (tối đa 15 từ), viết từ chữ trong span; KHÔNG đưa con số mới không có trong item.
   - "dieu_kien": tình tiết đi kèm nếu có (vd "mà gây tai nạn giao thông", "trong trường hợp …"), chép từ item; không có thì bỏ trống.
   - Item chỉ dẫn chiếu tới hành vi ở nơi khác ("Thực hiện hành vi quy định tại điểm … bị …", "… quy định tại khoản … Điều này") mà không tự mô tả hành vi mới → "hanh_vi": [].
   - Item chỉ quy định thủ tục, thẩm quyền, hiệu lực, định nghĩa → thường "hanh_vi": [].
   - KHÔNG trích mức phạt, số điểm trừ, thời hạn tước: các con số pháp lý được hệ thống lấy riêng.

2. "phuong_tien": id các loại phương tiện mà item (hoặc Điều chứa nó, theo tiêu đề Điều) áp dụng cho. CHỈ dùng id trong danh mục dưới đây. Giữ đúng loại xe như văn bản: "xe gắn máy" khác "xe mô tô", "xe ô tô" khác "xe chở người bốn bánh có gắn động cơ"; không suy rộng sang loại xe không được nêu.

3. "chu_the": id các chủ thể (người/tổ chức) bị điều chỉnh hoặc chịu trách nhiệm trong item. CHỈ dùng id trong danh mục dưới đây.

4. "khai_niem": thuật ngữ được item ĐỊNH NGHĨA (dạng "X là …", "X được hiểu là …", "X gồm …"). "thuat_ngu" và "dinh_nghia" chép nguyên văn từ item. Không có thì [].

5. "de_xuat_moi": phương tiện hoặc chủ thể quan trọng mà item nêu nhưng KHÔNG có trong danh mục (loai "PhuongTien" hoặc "ChuThe", "ten" chép từ item). Không có thì [].

Mọi item phải có mặt trong "items", kể cả khi tất cả danh sách đều rỗng.

Danh mục phương tiện (id: tên):
$catalog_pt

Danh mục chủ thể (id: tên):
$catalog_ct

Các item:

$items
