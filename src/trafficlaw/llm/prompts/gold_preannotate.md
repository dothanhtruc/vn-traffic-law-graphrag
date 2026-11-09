Bạn hỗ trợ gán nhãn BẢN NHÁP cho tập vàng trích xuất thực thể từ văn bản pháp luật giao thông đường bộ Việt Nam. Người gán nhãn sẽ sửa lại bản nháp này. Trả về DUY NHẤT một JSON object (không giải thích, không markdown) dạng:

{"entities": [...], "relations": [...]}

Đầu vào là một Khoản (có thể kèm các Điểm). Mỗi dòng có mã unit trong ngoặc vuông, ví dụ [ND168-2024/D6/K1/a].

ENTITIES — mỗi phần tử: {"id": "e1", "type": ..., "unit_id": "<mã unit nêu thực thể>", ...}
- "HanhVi": hành vi do chính unit mô tả. "span" = đoạn NGUYÊN VĂN liên tục của unit; "ten" = tên ngắn (≤ 15 từ); "dieu_kien" nếu có. Một unit nêu nhiều hành vi (ngăn bởi ";") → nhiều HanhVi. Bỏ phần "trừ các hành vi vi phạm quy định tại …". Unit chỉ dẫn chiếu hành vi ở nơi khác ("Thực hiện hành vi quy định tại …") thì KHÔNG tạo HanhVi.
- "CheTai": hình thức xử phạt nêu trong unit. "loai" ∈ {"phat_tien", "canh_cao", "tuoc_quyen", "tich_thu", "dinh_chi"}; phat_tien: "min_vnd", "max_vnd" (số nguyên đồng, vd 400000); tuoc_quyen/dinh_chi: "min_thang", "max_thang", "doi_tuong" (vd "giấy phép lái xe"); tich_thu: "doi_tuong". Chỉ ghi số có trong văn bản.
- "DiemGPLX": "so_diem" (số điểm bị trừ giấy phép lái xe nêu trong unit).
- "BienPhapBoSung": biện pháp khắc phục hậu quả ("buộc …"); "ten" = cụm "buộc …" chép từ unit.
- "KhaiNiem": thuật ngữ được định nghĩa ("X là …"); "ten" = thuật ngữ nguyên văn.
- "PhuongTien": "catalog_id" ∈ danh mục phương tiện bên dưới — loại xe mà unit áp dụng (kể cả theo tiêu đề Điều). "xe gắn máy" khác "xe mô tô".
- "ChuThe": "catalog_id" ∈ danh mục chủ thể bên dưới.

RELATIONS — mỗi phần tử: {"type": ..., "src": ..., "dst": ...}; "src"/"dst" là id entity hoặc "unit:<mã unit>".
- "QUY_DINH_HANH_VI": src "unit:<unit>" → dst HanhVi của unit đó.
- "AP_DUNG_CHO": src "unit:<unit>" → dst PhuongTien/ChuThe.
- "DINH_NGHIA": src "unit:<unit>" → dst KhaiNiem.
- "BI_XU_PHAT": src "unit:<unit hành vi>" → dst CheTai hoặc BienPhapBoSung. Mức phạt ở câu dẫn của Khoản áp cho MỌI Điểm hành vi của Khoản đó. Câu "Thực hiện hành vi quy định tại điểm a khoản 2 … bị …" → src là các unit được dẫn chiếu (viết đủ mã, vd "unit:ND168-2024/D6/K2/a"; "khoản N" có các Điểm → liệt kê từng Điểm nếu biết, không thì "unit:<mã Khoản>").
- "BI_TRU_DIEM": như BI_XU_PHAT, dst là DiemGPLX.

Danh mục phương tiện (id: tên):
$catalog_pt

Danh mục chủ thể (id: tên):
$catalog_ct

Tiêu đề Điều: $dieu_title

Nội dung:
$text
