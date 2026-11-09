# Tập vàng trích xuất — bản đọc (sinh tự động, sửa trong gold_extraction.jsonl)

## ND168-2024/D10/K2@2026-11-03 · nd168_che_tai · tier A · ĐÃ DUYỆT

Điều: Xử phạt người đi bộ vi phạm quy tắc giao thông đường bộ

```
[ND168-2024/D10/K2] 2. Phạt tiền từ 400.000 đồng đến 600.000 đồng đối với người đi bộ thực hiện một trong các hành vi vi phạm sau đây:
[ND168-2024/D10/K2/a] a) Đi vào đường cao tốc, trừ người phục vụ việc quản lý, bảo trì đường cao tốc;
[ND168-2024/D10/K2/b] b) Mang, vác vật cồng kềnh gây cản trở giao thông;
[ND168-2024/D10/K2/c] c) Đu, bám vào phương tiện giao thông đang chạy.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e4 | CheTai | D10/K2 | {"loai": "phat_tien", "min_vnd": 400000, "max_vnd": 600000} |
| e5 | ChuThe | D10/K2 | {"catalog_id": "CT:nguoi-di-bo"} |
| e1 | HanhVi | D10/K2/a | {"ten": "Đi vào đường cao tốc", "span": "Đi vào đường cao tốc"} |
| e2 | HanhVi | D10/K2/b | {"ten": "Mang, vác vật cồng kềnh gây cản trở giao thông", "span": "Mang, vác vật cồng kềnh gây cản trở giao thông"} |
| e3 | HanhVi | D10/K2/c | {"ten": "Đu, bám vào phương tiện giao thông đang chạy", "span": "Đu, bám vào phương tiện giao thông đang chạy"} |

- QUY_DINH_HANH_VI: unit:ND168-2024/D10/K2/a → e1
- QUY_DINH_HANH_VI: unit:ND168-2024/D10/K2/b → e2
- QUY_DINH_HANH_VI: unit:ND168-2024/D10/K2/c → e3
- BI_XU_PHAT: unit:ND168-2024/D10/K2/a → e4
- BI_XU_PHAT: unit:ND168-2024/D10/K2/b → e4
- BI_XU_PHAT: unit:ND168-2024/D10/K2/c → e4
- AP_DUNG_CHO: unit:ND168-2024/D10/K2 → e5

## ND168-2024/D12/K1@2026-11-03 · nd168_che_tai · tier A · ĐÃ DUYỆT

Điều: Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm khác về quy tắc giao thông đường bộ; sử dụng lòng đường, vỉa hè vào mục đích khác

```
[ND168-2024/D12/K1] 1. Phạt tiền từ 100.000 đồng đến 200.000 đồng đối với người được chở trên xe đạp, xe đạp máy sử dụng ô (dù).
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e1 | HanhVi | D12/K1 | {"ten": "sử dụng ô (dù)", "span": "sử dụng ô (dù)"} |
| e2 | CheTai | D12/K1 | {"loai": "phat_tien", "min_vnd": 100000, "max_vnd": 200000} |
| e3 | PhuongTien | D12/K1 | {"catalog_id": "PT:xe-dap"} |
| e4 | PhuongTien | D12/K1 | {"catalog_id": "PT:xe-dap-may"} |
| e5 | ChuThe | D12/K1 | {"catalog_id": "CT:nguoi-duoc-cho"} |

- QUY_DINH_HANH_VI: unit:ND168-2024/D12/K1 → e1
- BI_XU_PHAT: unit:ND168-2024/D12/K1 → e2
- AP_DUNG_CHO: unit:ND168-2024/D12/K1 → e3
- AP_DUNG_CHO: unit:ND168-2024/D12/K1 → e4
- AP_DUNG_CHO: unit:ND168-2024/D12/K1 → e5

## ND168-2024/D12/K13@2026-11-03 · nd168_che_tai · tier A · ĐÃ DUYỆT

Điều: Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm khác về quy tắc giao thông đường bộ; sử dụng lòng đường, vỉa hè vào mục đích khác

```
[ND168-2024/D12/K13] 13. Phạt tiền từ 30.000.000 đồng đến 32.000.000 đồng đối với cá nhân, từ 60.000.000 đồng đến 64.000.000 đồng đối với tổ chức thực hiện hành vi không khai báo, khai báo gian dối hoặc cung cấp thông tin, tài liệu không đúng sự thật để trốn tránh trách nhiệm khi bị phát hiện vi phạm pháp luật về trật tự, an toàn giao thông đường bộ.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e1 | HanhVi | D12/K13 | {"ten": "không khai báo, khai báo gian dối để trốn tránh trách nhiệm khi bị phát hiện vi phạm", "span": "không khai báo, khai báo gian dối hoặc cung cấp thông tin, tài liệu không đúng sự thật để trốn tránh trách nhiệm khi bị phát hiện vi phạm pháp luật về trật tự, an toàn giao thông đường bộ"} |
| e2 | CheTai | D12/K13 | {"loai": "phat_tien", "min_vnd": 30000000, "max_vnd": 32000000} |
| e3 | CheTai | D12/K13 | {"loai": "phat_tien", "min_vnd": 60000000, "max_vnd": 64000000} |
| e4 | ChuThe | D12/K13 | {"catalog_id": "CT:ca-nhan"} |
| e5 | ChuThe | D12/K13 | {"catalog_id": "CT:to-chuc"} |

- QUY_DINH_HANH_VI: unit:ND168-2024/D12/K13 → e1
- BI_XU_PHAT: unit:ND168-2024/D12/K13 → e2
- BI_XU_PHAT: unit:ND168-2024/D12/K13 → e3
- AP_DUNG_CHO: unit:ND168-2024/D12/K13 → e4
- AP_DUNG_CHO: unit:ND168-2024/D12/K13 → e5

Bản nháp bị bỏ 4 mục:
- span_khong_nguyen_van: {"id": "e1", "type": "HanhVi", "unit_id": "ND168-2024/D12/K13", "ten": "không khai báo, khai báo gian dối hoặc cung cấp thông tin không đúng", "span": "thực hiện hành vi không khai báo, khai báo gian 
- so_lech_regex: {"id": "e3", "type": "CheTai", "unit_id": "ND168-2024/D12/K13", "ten": null, "span": null, "dieu_kien": null, "catalog_id": null, "loai": "phat_tien", "min_vnd": 60000000, "max_vnd": 64000000, "min_th
- dich_khong_hop_le: {"type": "QUY_DINH_HANH_VI", "src": "unit:ND168-2024/D12/K13", "dst": "e1"}
- dich_khong_hop_le: {"type": "BI_XU_PHAT", "src": "unit:ND168-2024/D12/K13", "dst": "e3"}

## ND168-2024/D12/K5@2026-11-03 · nd168_che_tai · tier A · ĐÃ DUYỆT

Điều: Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm khác về quy tắc giao thông đường bộ; sử dụng lòng đường, vỉa hè vào mục đích khác

```
[ND168-2024/D12/K5] 5. Phạt tiền từ 400.000 đồng đến 600.000 đồng đối với người được chở trên xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô, các loại xe tương tự xe gắn máy thực hiện một trong các hành vi vi phạm sau đây:
[ND168-2024/D12/K5/a] a) Bám, kéo, đẩy xe khác, vật khác, dẫn dắt vật nuôi, mang vác vật cồng kềnh, đứng trên yên, giá đèo hàng hoặc ngồi trên tay lái của xe;
[ND168-2024/D12/K5/b] b) Không đội “mũ bảo hiểm cho người đi mô tô, xe máy” hoặc đội “mũ bảo hiểm cho người đi mô tô, xe máy” không cài quai đúng quy cách khi tham gia giao thông trên đường bộ.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e3 | CheTai | D12/K5 | {"loai": "phat_tien", "min_vnd": 400000, "max_vnd": 600000} |
| e4 | PhuongTien | D12/K5 | {"catalog_id": "PT:xe-mo-to"} |
| e5 | PhuongTien | D12/K5 | {"catalog_id": "PT:xe-gan-may"} |
| e6 | PhuongTien | D12/K5 | {"catalog_id": "PT:xe-tuong-tu-xe-mo-to"} |
| e7 | PhuongTien | D12/K5 | {"catalog_id": "PT:xe-tuong-tu-xe-gan-may"} |
| e8 | ChuThe | D12/K5 | {"catalog_id": "CT:nguoi-duoc-cho"} |
| e1 | HanhVi | D12/K5/a | {"ten": "Bám, kéo, đẩy xe khác", "span": "Bám, kéo, đẩy xe khác, vật khác, dẫn dắt vật nuôi, mang vác vật cồng kềnh, đứng trên yên, giá đèo hàng hoặc ngồi trên tay lái của xe"} |
| e2 | HanhVi | D12/K5/b | {"ten": "Không đội mũ bảo hiểm", "span": "Không đội “mũ bảo hiểm cho người đi mô tô, xe máy” hoặc đội “mũ bảo hiểm cho người đi mô tô, xe máy” không cài quai đúng quy cách khi tham gia giao thông trên đường bộ"} |

- QUY_DINH_HANH_VI: unit:ND168-2024/D12/K5/a → e1
- QUY_DINH_HANH_VI: unit:ND168-2024/D12/K5/b → e2
- BI_XU_PHAT: unit:ND168-2024/D12/K5/a → e3
- BI_XU_PHAT: unit:ND168-2024/D12/K5/b → e3
- AP_DUNG_CHO: unit:ND168-2024/D12/K5 → e4
- AP_DUNG_CHO: unit:ND168-2024/D12/K5 → e5
- AP_DUNG_CHO: unit:ND168-2024/D12/K5 → e6
- AP_DUNG_CHO: unit:ND168-2024/D12/K5 → e7
- AP_DUNG_CHO: unit:ND168-2024/D12/K5 → e8

## ND168-2024/D13/K6@2026-11-03 · nd168_che_tai · tier A · ĐÃ DUYỆT

Điều: Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo), xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tư xe ô tô vi phạm quy định về điều kiện của phương tiện khi tham gia giao thông

```
[ND168-2024/D13/K6] 6. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
[ND168-2024/D13/K6/a] a) Sử dụng chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe), giấy chứng nhận, tem kiểm định an toàn kỹ thuật và bảo vệ môi trường không do cơ quan có thẩm quyền cấp hoặc bị tẩy xóa; sử dụng chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe) không đúng số khung, số động cơ (số máy) của xe (kể cả rơ moóc và sơ mi rơ moóc);
[ND168-2024/D13/K6/b] b) Điều khiển xe không có giấy chứng nhận hoặc tem kiểm định an toàn kỹ thuật và bảo vệ môi trường (đối với loại xe có quy định phải kiểm định, trừ xe đăng ký tạm thời) hoặc có nhưng đã hết hiệu lực (hạn sử dụng) từ 01 tháng trở lên (kể cả rơ moóc và sơ mi rơ moóc).
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e10 | PhuongTien | D13/K6 | {"catalog_id": "PT:xe-cho-nguoi-bon-banh-co-gan-dong-co"} |
| e11 | PhuongTien | D13/K6 | {"catalog_id": "PT:xe-cho-hang-bon-banh-co-gan-dong-co"} |
| e12 | PhuongTien | D13/K6 | {"catalog_id": "PT:xe-tuong-tu-xe-o-to"} |
| e4 | CheTai | D13/K6 | {"loai": "phat_tien", "min_vnd": 4000000, "max_vnd": 6000000} |
| e6 | ChuThe | D13/K6 | {"catalog_id": "CT:nguoi-dieu-khien-xe"} |
| e7 | PhuongTien | D13/K6 | {"catalog_id": "PT:xe-o-to"} |
| e8 | PhuongTien | D13/K6 | {"catalog_id": "PT:ro-mooc"} |
| e9 | PhuongTien | D13/K6 | {"catalog_id": "PT:so-mi-ro-mooc"} |
| e1 | HanhVi | D13/K6/a | {"ten": "Sử dụng chứng nhận đăng ký xe không hợp lệ", "span": "Sử dụng chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe), giấy chứng nhận, tem kiểm định an toàn kỹ thuật và bảo vệ môi trường không do cơ quan có thẩm quyền cấp hoặc bị tẩy xóa"} |
| e2 | HanhVi | D13/K6/a | {"ten": "Sử dụng chứng nhận đăng ký xe không đúng số khung, số động cơ", "span": "sử dụng chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe) không đúng số khung, số động cơ (số máy) của xe (kể cả rơ moóc và sơ mi rơ moóc)"} |
| e3 | HanhVi | D13/K6/b | {"ten": "Điều khiển xe không có giấy chứng nhận hoặc tem kiểm định hết hạn", "span": "Điều khiển xe không có giấy chứng nhận hoặc tem kiểm định an toàn kỹ thuật và bảo vệ môi trường (đối với loại xe có quy định phải kiểm định, trừ xe đăng ký tạm thời) hoặc có nhưng đã hết hiệu lực (hạn sử dụng) từ 01 tháng trở lên (kể cả rơ moóc và sơ mi rơ moóc)"} |

- QUY_DINH_HANH_VI: unit:ND168-2024/D13/K6/a → e1
- QUY_DINH_HANH_VI: unit:ND168-2024/D13/K6/a → e2
- QUY_DINH_HANH_VI: unit:ND168-2024/D13/K6/b → e3
- BI_XU_PHAT: unit:ND168-2024/D13/K6/a → e4
- BI_XU_PHAT: unit:ND168-2024/D13/K6/b → e4
- AP_DUNG_CHO: unit:ND168-2024/D13/K6 → e10
- AP_DUNG_CHO: unit:ND168-2024/D13/K6 → e11
- AP_DUNG_CHO: unit:ND168-2024/D13/K6 → e12
- AP_DUNG_CHO: unit:ND168-2024/D13/K6 → e6
- AP_DUNG_CHO: unit:ND168-2024/D13/K6 → e7
- AP_DUNG_CHO: unit:ND168-2024/D13/K6 → e8
- AP_DUNG_CHO: unit:ND168-2024/D13/K6 → e9

## ND168-2024/D13/K8@2026-11-03 · nd168_che_tai · tier A · ĐÃ DUYỆT

Điều: Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo), xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tư xe ô tô vi phạm quy định về điều kiện của phương tiện khi tham gia giao thông

```
[ND168-2024/D13/K8] 8. Phạt tiền từ 20.000.000 đồng đến 26.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
[ND168-2024/D13/K8/a] a) Điều khiển xe gắn biển số không đúng với chứng nhận đăng ký xe hoặc gắn biển số không do cơ quan có thẩm quyền cấp (kể cả rơ moóc và sơ mi rơ moóc);
[ND168-2024/D13/K8/b] b) Điều khiển xe không gắn đủ biển số hoặc gắn biển số không đúng vị trí, không đúng quy cách theo quy định; gắn biển số không rõ chữ, số hoặc sơn, dán lên chữ, số của biển số xe; gắn biển số bị bẻ cong, che lấp, làm thay đổi chữ, số, màu sắc (của chữ, số, nền biển số xe), hình dạng, kích thước của biển số xe; sử dụng chất liệu, vật liệu, thiết bị làm thay đổi khả năng nhận diện thông tin biển số xe của phương tiện, thiết bị kỹ thuật nghiệp vụ (kể cả rơ moóc và sơ mi rơ moóc).
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e10 | PhuongTien | D13/K8 | {"catalog_id": "PT:xe-cho-nguoi-bon-banh-co-gan-dong-co"} |
| e11 | PhuongTien | D13/K8 | {"catalog_id": "PT:xe-cho-hang-bon-banh-co-gan-dong-co"} |
| e12 | PhuongTien | D13/K8 | {"catalog_id": "PT:xe-tuong-tu-xe-o-to"} |
| e13 | ChuThe | D13/K8 | {"catalog_id": "CT:nguoi-dieu-khien-xe"} |
| e6 | CheTai | D13/K8 | {"loai": "phat_tien", "min_vnd": 20000000, "max_vnd": 26000000} |
| e7 | PhuongTien | D13/K8 | {"catalog_id": "PT:xe-o-to"} |
| e8 | PhuongTien | D13/K8 | {"catalog_id": "PT:ro-mooc"} |
| e9 | PhuongTien | D13/K8 | {"catalog_id": "PT:so-mi-ro-mooc"} |
| e1 | HanhVi | D13/K8/a | {"ten": "Điều khiển xe gắn biển số không đúng", "span": "Điều khiển xe gắn biển số không đúng với chứng nhận đăng ký xe hoặc gắn biển số không do cơ quan có thẩm quyền cấp (kể cả rơ moóc và sơ mi rơ moóc)"} |
| e2 | HanhVi | D13/K8/b | {"ten": "Điều khiển xe không gắn đủ biển số", "span": "Điều khiển xe không gắn đủ biển số hoặc gắn biển số không đúng vị trí, không đúng quy cách theo quy định"} |
| e3 | HanhVi | D13/K8/b | {"ten": "gắn biển số không rõ chữ, số", "span": "gắn biển số không rõ chữ, số hoặc sơn, dán lên chữ, số của biển số xe"} |
| e4 | HanhVi | D13/K8/b | {"ten": "gắn biển số bị bẻ cong, che lấp", "span": "gắn biển số bị bẻ cong, che lấp, làm thay đổi chữ, số, màu sắc (của chữ, số, nền biển số xe), hình dạng, kích thước của biển số xe"} |
| e5 | HanhVi | D13/K8/b | {"ten": "sử dụng vật liệu, thiết bị làm thay đổi khả năng nhận diện biển số xe", "span": "sử dụng chất liệu, vật liệu, thiết bị làm thay đổi khả năng nhận diện thông tin biển số xe của phương tiện, thiết bị kỹ thuật nghiệp vụ (kể cả rơ moóc và sơ mi rơ moóc)"} |

- QUY_DINH_HANH_VI: unit:ND168-2024/D13/K8/a → e1
- QUY_DINH_HANH_VI: unit:ND168-2024/D13/K8/b → e2
- QUY_DINH_HANH_VI: unit:ND168-2024/D13/K8/b → e3
- QUY_DINH_HANH_VI: unit:ND168-2024/D13/K8/b → e4
- QUY_DINH_HANH_VI: unit:ND168-2024/D13/K8/b → e5
- BI_XU_PHAT: unit:ND168-2024/D13/K8/a → e6
- BI_XU_PHAT: unit:ND168-2024/D13/K8/b → e6
- AP_DUNG_CHO: unit:ND168-2024/D13/K8 → e10
- AP_DUNG_CHO: unit:ND168-2024/D13/K8 → e11
- AP_DUNG_CHO: unit:ND168-2024/D13/K8 → e12
- AP_DUNG_CHO: unit:ND168-2024/D13/K8 → e13
- AP_DUNG_CHO: unit:ND168-2024/D13/K8 → e7
- AP_DUNG_CHO: unit:ND168-2024/D13/K8 → e8
- AP_DUNG_CHO: unit:ND168-2024/D13/K8 → e9

Bản nháp bị bỏ 2 mục:
- span_khong_nguyen_van: {"id": "e5", "type": "HanhVi", "unit_id": "ND168-2024/D13/K8/b", "ten": "sử dụng chất liệu làm thay đổi khả năng nhận diện biển số", "span": "sử dụng chất liệu, vật liệu, thiết bị làm thay đổi khả năn
- dich_khong_hop_le: {"type": "QUY_DINH_HANH_VI", "src": "unit:ND168-2024/D13/K8/b", "dst": "e5"}

## ND168-2024/D17/K3@2026-11-03 · nd168_che_tai · tier A · ĐÃ DUYỆT

Điều: Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, máy kéo và các loại xe tương tự xe ô tô vi phạm quy định về bảo vệ môi trường khi tham gia giao thông

```
[ND168-2024/D17/K3] 3. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng đối với người điều khiển xe đổ trái phép rác, đất, cát, đá, vật liệu, chất phế thải trong phạm vi đất dành cho đường bộ ở đoạn đường ngoài đô thị.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e1 | HanhVi | D17/K3 | {"ten": "đổ trái phép rác, đất, cát, đá, vật liệu, chất phế thải", "span": "đổ trái phép rác, đất, cát, đá, vật liệu, chất phế thải trong phạm vi đất dành cho đường bộ ở đoạn đường ngoài đô thị"} |
| e2 | CheTai | D17/K3 | {"loai": "phat_tien", "min_vnd": 4000000, "max_vnd": 6000000} |
| e4 | ChuThe | D17/K3 | {"catalog_id": "CT:nguoi-dieu-khien-xe"} |
| e5 | PhuongTien | D17/K3 | {"catalog_id": "PT:xe-o-to"} |
| e6 | PhuongTien | D17/K3 | {"catalog_id": "PT:may-keo"} |
| e7 | PhuongTien | D17/K3 | {"catalog_id": "PT:xe-tuong-tu-xe-o-to"} |

- QUY_DINH_HANH_VI: unit:ND168-2024/D17/K3 → e1
- BI_XU_PHAT: unit:ND168-2024/D17/K3 → e2
- AP_DUNG_CHO: unit:ND168-2024/D17/K3 → e4
- AP_DUNG_CHO: unit:ND168-2024/D17/K3 → e5
- AP_DUNG_CHO: unit:ND168-2024/D17/K3 → e6
- AP_DUNG_CHO: unit:ND168-2024/D17/K3 → e7

## ND168-2024/D17/K4@2026-11-03 · nd168_che_tai · tier A · ĐÃ DUYỆT

Điều: Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, máy kéo và các loại xe tương tự xe ô tô vi phạm quy định về bảo vệ môi trường khi tham gia giao thông

```
[ND168-2024/D17/K4] 4. Phạt tiền từ 10.000.000 đồng đến 15.000.000 đồng đối với người điều khiển xe thực hiện hành vi đổ trái phép rác, đất, cát, đá, vật liệu, chất phế thải ra đường phố.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e1 | HanhVi | D17/K4 | {"ten": "đổ rác, đất, cát, đá, vật liệu, chất phế thải ra đường phố", "span": "đổ trái phép rác, đất, cát, đá, vật liệu, chất phế thải ra đường phố"} |
| e2 | CheTai | D17/K4 | {"loai": "phat_tien", "min_vnd": 10000000, "max_vnd": 15000000} |
| e3 | PhuongTien | D17/K4 | {"catalog_id": "PT:xe-o-to"} |
| e4 | PhuongTien | D17/K4 | {"catalog_id": "PT:may-keo"} |
| e5 | PhuongTien | D17/K4 | {"catalog_id": "PT:xe-tuong-tu-xe-o-to"} |
| e6 | ChuThe | D17/K4 | {"catalog_id": "CT:nguoi-dieu-khien-xe"} |

- QUY_DINH_HANH_VI: unit:ND168-2024/D17/K4 → e1
- BI_XU_PHAT: unit:ND168-2024/D17/K4 → e2
- AP_DUNG_CHO: unit:ND168-2024/D17/K4 → e3
- AP_DUNG_CHO: unit:ND168-2024/D17/K4 → e4
- AP_DUNG_CHO: unit:ND168-2024/D17/K4 → e5
- AP_DUNG_CHO: unit:ND168-2024/D17/K4 → e6

## ND168-2024/D20/K3@2026-11-03 · nd168_che_tai · tier A · ĐÃ DUYỆT

Điều: Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông

```
[ND168-2024/D20/K3] 3. Phạt tiền từ 600.000 đồng đến 800.000 đồng đối với một trong các hành vi vi phạm sau đây:
[ND168-2024/D20/K3/a] a) Không đóng cửa lên xuống khi xe đang chạy;
[ND168-2024/D20/K3/b] b) Để người ngồi trên xe khi xe xuống phà, đang trên phà và khi lên bến (trừ người lái xe, trẻ em, phụ nữ mang thai, người già yếu, người bệnh, người khuyết tật);
[ND168-2024/D20/K3/c] c) Không chạy đúng tuyến đường, lịch trình, hành trình vận tải được phép hoạt động theo quy định;
[ND168-2024/D20/K3/d] d) Để người mắc võng nằm trên xe khi xe đang chạy;
[ND168-2024/D20/K3/đ] đ) Sắp xếp, chằng buộc hành lý, hàng hóa không bảo đảm an toàn; để rơi hành lý, hàng hóa trên xe xuống đường; để hàng hóa trong khoang chở hành khách;
[ND168-2024/D20/K3/e] e) Chở hành lý, hàng hóa vượt quá kích thước bao ngoài của xe;
[ND168-2024/D20/K3/g] g) Điều khiển xe vận tải hành khách không có nhân viên phục vụ trên xe đối với những xe quy định phải có nhân viên phục vụ;
[ND168-2024/D20/K3/h] h) Điều khiển xe ô tô kinh doanh vận tải không có dây đai an toàn tại các vị trí ghế ngồi, giường nằm theo quy định (trừ xe buýt nội tỉnh);
[ND168-2024/D20/K3/i] i) Điều khiển xe ô tô kinh doanh vận tải không có hướng dẫn cho hành khách về an toàn giao thông và thoát hiểm khi xảy ra sự cố trên xe theo quy định;
[ND168-2024/D20/K3/k] k) Điều khiển xe không niêm yết hành trình chạy xe hoặc niêm yết hành trình chạy xe không đúng với hành trình đã được cơ quan có thẩm quyền cấp phép.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| c1 | CheTai | D20/K3 | {"loai": "phat_tien", "min_vnd": 600000, "max_vnd": 800000} |
| ct1 | ChuThe | D20/K3 | {"catalog_id": "CT:nguoi-dieu-khien-xe"} |
| p1 | PhuongTien | D20/K3 | {"catalog_id": "PT:xe-o-to-cho-hanh-khach"} |
| p2 | PhuongTien | D20/K3 | {"catalog_id": "PT:xe-o-to"} |
| p3 | PhuongTien | D20/K3 | {"catalog_id": "PT:xe-o-to-kinh-doanh-van-tai"} |
| e1 | HanhVi | D20/K3/a | {"ten": "Không đóng cửa lên xuống khi xe đang chạy", "span": "Không đóng cửa lên xuống khi xe đang chạy"} |
| e2 | HanhVi | D20/K3/b | {"ten": "Để người ngồi trên xe khi xe xuống phà, đang trên phà và khi lên bến", "span": "Để người ngồi trên xe khi xe xuống phà, đang trên phà và khi lên bến"} |
| e3 | HanhVi | D20/K3/c | {"ten": "Không chạy đúng tuyến đường, lịch trình, hành trình vận tải được phép hoạt động theo quy định", "span": "Không chạy đúng tuyến đường, lịch trình, hành trình vận tải được phép hoạt động theo quy định"} |
| e4 | HanhVi | D20/K3/d | {"ten": "Để người mắc võng nằm trên xe khi xe đang chạy", "span": "Để người mắc võng nằm trên xe khi xe đang chạy"} |
| e7 | HanhVi | D20/K3/e | {"ten": "Chở hành lý, hàng hóa vượt quá kích thước bao ngoài của xe", "span": "Chở hành lý, hàng hóa vượt quá kích thước bao ngoài của xe"} |
| e8 | HanhVi | D20/K3/g | {"ten": "Điều khiển xe vận tải hành khách không có nhân viên phục vụ trên xe đối với những xe quy định phải có nhân viên phục vụ", "span": "Điều khiển xe vận tải hành khách không có nhân viên phục vụ trên xe đối với những xe quy định phải có nhân viên phục vụ"} |
| e9 | HanhVi | D20/K3/h | {"ten": "Điều khiển xe ô tô kinh doanh vận tải không có dây đai an toàn tại các vị trí ghế ngồi, giường nằm theo quy định", "span": "Điều khiển xe ô tô kinh doanh vận tải không có dây đai an toàn tại các vị trí ghế ngồi, giường nằm theo quy định"} |
| e10 | HanhVi | D20/K3/i | {"ten": "Điều khiển xe ô tô kinh doanh vận tải không có hướng dẫn cho hành khách về an toàn giao thông và thoát hiểm khi xảy ra sự cố trên xe theo quy định", "span": "Điều khiển xe ô tô kinh doanh vận tải không có hướng dẫn cho hành khách về an toàn giao thông và thoát hiểm khi xảy ra sự cố trên xe theo quy định"} |
| e11 | HanhVi | D20/K3/k | {"ten": "Điều khiển xe không niêm yết hành trình chạy xe hoặc niêm yết hành trình chạy xe không đúng với hành trình đã được cơ quan có thẩm quyền cấp phép", "span": "Điều khiển xe không niêm yết hành trình chạy xe hoặc niêm yết hành trình chạy xe không đúng với hành trình đã được cơ quan có thẩm quyền cấp phép"} |
| e12 | HanhVi | D20/K3/đ | {"ten": "để hàng hóa trong khoang chở hành khách", "span": "để hàng hóa trong khoang chở hành khách"} |
| e5 | HanhVi | D20/K3/đ | {"ten": "Sắp xếp, chằng buộc hành lý, hàng hóa không bảo đảm an toàn", "span": "Sắp xếp, chằng buộc hành lý, hàng hóa không bảo đảm an toàn"} |
| e6 | HanhVi | D20/K3/đ | {"ten": "để rơi hành lý, hàng hóa trên xe xuống đường", "span": "để rơi hành lý, hàng hóa trên xe xuống đường"} |

- QUY_DINH_HANH_VI: unit:ND168-2024/D20/K3/a → e1
- QUY_DINH_HANH_VI: unit:ND168-2024/D20/K3/b → e2
- QUY_DINH_HANH_VI: unit:ND168-2024/D20/K3/c → e3
- QUY_DINH_HANH_VI: unit:ND168-2024/D20/K3/d → e4
- QUY_DINH_HANH_VI: unit:ND168-2024/D20/K3/e → e7
- QUY_DINH_HANH_VI: unit:ND168-2024/D20/K3/g → e8
- QUY_DINH_HANH_VI: unit:ND168-2024/D20/K3/h → e9
- QUY_DINH_HANH_VI: unit:ND168-2024/D20/K3/i → e10
- QUY_DINH_HANH_VI: unit:ND168-2024/D20/K3/k → e11
- QUY_DINH_HANH_VI: unit:ND168-2024/D20/K3/đ → e12
- QUY_DINH_HANH_VI: unit:ND168-2024/D20/K3/đ → e5
- QUY_DINH_HANH_VI: unit:ND168-2024/D20/K3/đ → e6
- BI_XU_PHAT: unit:ND168-2024/D20/K3/a → c1
- BI_XU_PHAT: unit:ND168-2024/D20/K3/b → c1
- BI_XU_PHAT: unit:ND168-2024/D20/K3/c → c1
- BI_XU_PHAT: unit:ND168-2024/D20/K3/d → c1
- BI_XU_PHAT: unit:ND168-2024/D20/K3/e → c1
- BI_XU_PHAT: unit:ND168-2024/D20/K3/g → c1
- BI_XU_PHAT: unit:ND168-2024/D20/K3/h → c1
- BI_XU_PHAT: unit:ND168-2024/D20/K3/i → c1
- BI_XU_PHAT: unit:ND168-2024/D20/K3/k → c1
- BI_XU_PHAT: unit:ND168-2024/D20/K3/đ → c1
- AP_DUNG_CHO: unit:ND168-2024/D20/K3 → ct1
- AP_DUNG_CHO: unit:ND168-2024/D20/K3 → p1
- AP_DUNG_CHO: unit:ND168-2024/D20/K3 → p2
- AP_DUNG_CHO: unit:ND168-2024/D20/K3 → p3

Bản nháp bị bỏ 6 mục:
- span_khong_nguyen_van: {"id": "e4", "type": "HanhVi", "unit_id": "ND168-2024/D20/K3/d", "ten": "Sắp xếp, chằng buộc hành lý, hàng hóa không bảo đảm an toàn", "span": "Sắp xếp, chằng buộc hành lý, hàng hóa không bảo đảm an t
- span_khong_nguyen_van: {"id": "e5", "type": "HanhVi", "unit_id": "ND168-2024/D20/K3/d", "ten": "để rơi hành lý, hàng hóa trên xe xuống đường", "span": "để rơi hành lý, hàng hóa trên xe xuống đường", "dieu_kien": null, "cata
- span_khong_nguyen_van: {"id": "e6", "type": "HanhVi", "unit_id": "ND168-2024/D20/K3/d", "ten": "để hàng hóa trong khoang chở hành khách", "span": "để hàng hóa trong khoang chở hành khách", "dieu_kien": null, "catalog_id": n
- dich_khong_hop_le: {"type": "QUY_DINH_HANH_VI", "src": "unit:ND168-2024/D20/K3/d", "dst": "e4"}
- dich_khong_hop_le: {"type": "QUY_DINH_HANH_VI", "src": "unit:ND168-2024/D20/K3/d", "dst": "e5"}
- dich_khong_hop_le: {"type": "QUY_DINH_HANH_VI", "src": "unit:ND168-2024/D20/K3/d", "dst": "e6"}

## ND168-2024/D20/K7@2026-11-03 · nd168_che_tai · tier A · ĐÃ DUYỆT

Điều: Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông

```
[ND168-2024/D20/K7] 7. Phạt tiền từ 5.000.000 đồng đến 7.000.000 đồng đối với hành vi vi phạm điều khiển xe chở hành khách không có hoặc không gắn phù hiệu theo quy định hoặc có nhưng đã hết giá trị sử dụng hoặc sử dụng phù hiệu không do cơ quan có thẩm quyền cấp.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e1 | HanhVi | D20/K7 | {"ten": "điều khiển xe chở hành khách không có hoặc không gắn phù hiệu", "span": "điều khiển xe chở hành khách không có hoặc không gắn phù hiệu theo quy định hoặc có nhưng đã hết giá trị sử dụng hoặc sử dụng phù hiệu không do cơ quan có thẩm quyền cấp"} |
| e2 | CheTai | D20/K7 | {"loai": "phat_tien", "min_vnd": 5000000, "max_vnd": 7000000} |
| e3 | PhuongTien | D20/K7 | {"catalog_id": "PT:xe-o-to-cho-hanh-khach"} |
| e4 | ChuThe | D20/K7 | {"catalog_id": "CT:nguoi-dieu-khien-xe"} |

- QUY_DINH_HANH_VI: unit:ND168-2024/D20/K7 → e1
- BI_XU_PHAT: unit:ND168-2024/D20/K7 → e2
- AP_DUNG_CHO: unit:ND168-2024/D20/K7 → e3
- AP_DUNG_CHO: unit:ND168-2024/D20/K7 → e4

## ND168-2024/D23/K5@2026-11-03 · nd168_che_tai · tier A · ĐÃ DUYỆT

Điều: Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển hàng hóa nguy hiểm

```
[ND168-2024/D23/K5] 5. Phạt tiền từ 12.000.000 đồng đến 14.000.000 đồng đối với hành vi vận chuyển hàng hóa nguy hiểm không có giấy phép vận chuyển hàng hóa nguy hiểm hoặc có nhưng hết hiệu lực hoặc không thực hiện đúng quy định trong giấy phép vận chuyển hàng hóa nguy hiểm, trừ các hành vi vi phạm quy định tại điểm a khoản 6 Điều 20 của Nghị định này.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e1 | HanhVi | D23/K5 | {"ten": "vận chuyển hàng hóa nguy hiểm không có giấy phép hoặc hết hiệu lực", "span": "vận chuyển hàng hóa nguy hiểm không có giấy phép vận chuyển hàng hóa nguy hiểm hoặc có nhưng hết hiệu lực hoặc không thực hiện đúng quy định trong giấy phép vận chuyển hàng hóa nguy hiểm"} |
| e2 | CheTai | D23/K5 | {"loai": "phat_tien", "min_vnd": 12000000, "max_vnd": 14000000} |
| e3 | PhuongTien | D23/K5 | {"catalog_id": "PT:xe-o-to"} |
| e4 | ChuThe | D23/K5 | {"catalog_id": "CT:nguoi-dieu-khien-xe"} |

- QUY_DINH_HANH_VI: unit:ND168-2024/D23/K5 → e1
- BI_XU_PHAT: unit:ND168-2024/D23/K5 → e2
- AP_DUNG_CHO: unit:ND168-2024/D23/K5 → e3
- AP_DUNG_CHO: unit:ND168-2024/D23/K5 → e4

## ND168-2024/D24/K2@2026-11-03 · nd168_che_tai · tier A · ĐÃ DUYỆT

Điều: Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển động vật sống, thực phẩm tươi sống

```
[ND168-2024/D24/K2] 2. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với hành vi vi phạm vận chuyển thực phẩm tươi sống không chấp hành quy định về an toàn thực phẩm, vệ sinh dịch tễ, phòng dịch và bảo đảm vệ sinh môi trường theo quy định.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e1 | HanhVi | D24/K2 | {"ten": "vận chuyển thực phẩm tươi sống không chấp hành quy định về an toàn thực phẩm, vệ sinh dịch tễ", "span": "vận chuyển thực phẩm tươi sống không chấp hành quy định về an toàn thực phẩm, vệ sinh dịch tễ, phòng dịch và bảo đảm vệ sinh môi trường"} |
| e2 | CheTai | D24/K2 | {"loai": "phat_tien", "min_vnd": 3000000, "max_vnd": 5000000} |
| e3 | PhuongTien | D24/K2 | {"catalog_id": "PT:xe-o-to"} |
| e4 | ChuThe | D24/K2 | {"catalog_id": "CT:nguoi-dieu-khien-xe"} |

- QUY_DINH_HANH_VI: unit:ND168-2024/D24/K2 → e1
- BI_XU_PHAT: unit:ND168-2024/D24/K2 → e2
- AP_DUNG_CHO: unit:ND168-2024/D24/K2 → e3
- AP_DUNG_CHO: unit:ND168-2024/D24/K2 → e4

## ND168-2024/D26/K5@2026-11-03 · nd168_che_tai · tier A · ĐÃ DUYỆT

Điều: Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ

```
[ND168-2024/D26/K5] 5. Phạt tiền từ 4.000.000 đồng đến 5.000.000 đồng đối với cá nhân, từ 8.000.000 đồng đến 10.000.000 đồng đối với tổ chức xếp hàng hóa lên mỗi xe ô tô (kể cả rơ moóc và sơ mi rơ moóc) vượt quá trọng tải (khối lượng hàng chuyên chở) cho phép tham gia giao thông được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe trên 100%.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e1 | HanhVi | D26/K5 | {"ten": "xếp hàng quá tải", "span": "xếp hàng hóa lên mỗi xe ô tô (kể cả rơ moóc và sơ mi rơ moóc) vượt quá trọng tải (khối lượng hàng chuyên chở) cho phép tham gia giao thông được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe trên 100%"} |
| e2 | CheTai | D26/K5 | {"loai": "phat_tien", "min_vnd": 4000000, "max_vnd": 5000000} |
| e3 | CheTai | D26/K5 | {"loai": "phat_tien", "min_vnd": 8000000, "max_vnd": 10000000} |
| e4 | PhuongTien | D26/K5 | {"catalog_id": "PT:xe-o-to"} |
| e5 | PhuongTien | D26/K5 | {"catalog_id": "PT:ro-mooc"} |
| e6 | PhuongTien | D26/K5 | {"catalog_id": "PT:so-mi-ro-mooc"} |
| e7 | ChuThe | D26/K5 | {"catalog_id": "CT:ca-nhan"} |
| e8 | ChuThe | D26/K5 | {"catalog_id": "CT:to-chuc"} |

- QUY_DINH_HANH_VI: unit:ND168-2024/D26/K5 → e1
- BI_XU_PHAT: unit:ND168-2024/D26/K5 → e2
- BI_XU_PHAT: unit:ND168-2024/D26/K5 → e3
- AP_DUNG_CHO: unit:ND168-2024/D26/K5 → e4
- AP_DUNG_CHO: unit:ND168-2024/D26/K5 → e5
- AP_DUNG_CHO: unit:ND168-2024/D26/K5 → e6
- AP_DUNG_CHO: unit:ND168-2024/D26/K5 → e7
- AP_DUNG_CHO: unit:ND168-2024/D26/K5 → e8

Bản nháp bị bỏ 2 mục:
- so_lech_regex: {"id": "e3", "type": "CheTai", "unit_id": "ND168-2024/D26/K5", "ten": null, "span": null, "dieu_kien": null, "catalog_id": null, "loai": "phat_tien", "min_vnd": 8000000, "max_vnd": 10000000, "min_than
- dich_khong_hop_le: {"type": "BI_XU_PHAT", "src": "unit:ND168-2024/D26/K5", "dst": "e3"}

## ND168-2024/D33/K3@2026-11-03 · nd168_che_tai · tier A · ĐÃ DUYỆT

Điều: Xử phạt hành khách đi xe vi phạm quy định về trật tự, an toàn giao thông

```
[ND168-2024/D33/K3] 3. Phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng đối với hành vi đe dọa, xâm phạm sức khỏe của người khác đi trên xe, lái xe, nhân viên phục vụ trên xe.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e1 | HanhVi | D33/K3 | {"ten": "đe dọa, xâm phạm sức khỏe người khác đi trên xe, lái xe, nhân viên phục vụ", "span": "đe dọa, xâm phạm sức khỏe của người khác đi trên xe, lái xe, nhân viên phục vụ trên xe"} |
| e2 | CheTai | D33/K3 | {"loai": "phat_tien", "min_vnd": 2000000, "max_vnd": 3000000} |
| e3 | ChuThe | D33/K3 | {"catalog_id": "CT:hanh-khach"} |

- QUY_DINH_HANH_VI: unit:ND168-2024/D33/K3 → e1
- BI_XU_PHAT: unit:ND168-2024/D33/K3 → e2
- AP_DUNG_CHO: unit:ND168-2024/D33/K3 → e3

## ND168-2024/D28/K1@2026-11-03 · nd168_che_tai · tier A · ĐÃ DUYỆT

Điều: Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ

```
[ND168-2024/D28/K1] 1. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với hành vi chở quá số người quy định được phép chở của phương tiện.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e1 | HanhVi | D28/K1 | {"ten": "chở quá số người quy định được phép chở", "span": "chở quá số người quy định được phép chở của phương tiện"} |
| e2 | CheTai | D28/K1 | {"loai": "phat_tien", "min_vnd": 1000000, "max_vnd": 2000000} |
| e3 | PhuongTien | D28/K1 | {"catalog_id": "PT:xe-cho-nguoi-bon-banh-co-gan-dong-co"} |
| e4 | PhuongTien | D28/K1 | {"catalog_id": "PT:xe-cho-hang-bon-banh-co-gan-dong-co"} |
| e5 | ChuThe | D28/K1 | {"catalog_id": "CT:nguoi-dieu-khien-xe"} |

- QUY_DINH_HANH_VI: unit:ND168-2024/D28/K1 → e1
- BI_XU_PHAT: unit:ND168-2024/D28/K1 → e2
- AP_DUNG_CHO: unit:ND168-2024/D28/K1 → e3
- AP_DUNG_CHO: unit:ND168-2024/D28/K1 → e4
- AP_DUNG_CHO: unit:ND168-2024/D28/K1 → e5

## ND168-2024/D37/K1@2026-11-03 · nd168_che_tai · tier A · ĐÃ DUYỆT

Điều: Xử phạt người điều khiển phương tiện giao thông cơ giới đường bộ gắn biển số nước ngoài

```
[ND168-2024/D37/K1] 1. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với người điều khiển phương tiện giao thông cơ giới đường bộ gắn biển số nước ngoài thực hiện một trong các hành vi vi phạm sau đây:
[ND168-2024/D37/K1/a] a) Giấy tờ của phương tiện không có bản dịch sang tiếng Anh hoặc tiếng Việt theo quy định;
[ND168-2024/D37/K1/b] b) Điều khiển xe chở hành khách không có danh sách hành khách theo quy định.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e3 | CheTai | D37/K1 | {"loai": "phat_tien", "min_vnd": 1000000, "max_vnd": 2000000} |
| e4 | PhuongTien | D37/K1 | {"catalog_id": "PT:xe-co-gioi"} |
| e5 | ChuThe | D37/K1 | {"catalog_id": "CT:nguoi-dieu-khien-xe"} |
| e1 | HanhVi | D37/K1/a | {"span": "Giấy tờ của phương tiện không có bản dịch sang tiếng Anh hoặc tiếng Việt theo quy định"} |
| e2 | HanhVi | D37/K1/b | {"span": "Điều khiển xe chở hành khách không có danh sách hành khách theo quy định"} |

- QUY_DINH_HANH_VI: unit:ND168-2024/D37/K1/a → e1
- QUY_DINH_HANH_VI: unit:ND168-2024/D37/K1/b → e2
- BI_XU_PHAT: unit:ND168-2024/D37/K1/a → e3
- BI_XU_PHAT: unit:ND168-2024/D37/K1/b → e3
- AP_DUNG_CHO: unit:ND168-2024/D37/K1 → e4
- AP_DUNG_CHO: unit:ND168-2024/D37/K1 → e5

Bản nháp bị bỏ 2 mục:
- ngoai_danh_muc: {"id": "e4", "type": "PhuongTien", "unit_id": "ND168-2024/D37/K1", "ten": null, "span": null, "dieu_kien": null, "catalog_id": "PT:phuong-tien-giao-thong-co-gioi-duong-bo", "loai": null, "min_vnd": nu
- dich_khong_hop_le: {"type": "AP_DUNG_CHO", "src": "unit:ND168-2024/D37/K1", "dst": "e4"}

## ND168-2024/D37/K4@2026-11-03 · nd168_che_tai · tier A · ĐÃ DUYỆT

Điều: Xử phạt người điều khiển phương tiện giao thông cơ giới đường bộ gắn biển số nước ngoài

```
[ND168-2024/D37/K4] 4. Phạt tiền từ 8.000.000 đồng đến 10.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
[ND168-2024/D37/K4/a] a) Điều khiển phương tiện không gắn biển số tạm thời hoặc gắn biển số tạm thời không do cơ quan có thẩm quyền cấp (nếu có quy định phải gắn biển số tạm thời);
[ND168-2024/D37/K4/b] b) Điều khiển xe ô tô có tay lái bên phải tham gia giao thông mà không đi theo đoàn, không có người, phương tiện hỗ trợ, hướng dẫn giao thông theo quy định.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e3 | CheTai | D37/K4 | {"loai": "phat_tien", "min_vnd": 8000000, "max_vnd": 10000000} |
| e4 | PhuongTien | D37/K4 | {"catalog_id": "PT:xe-co-gioi"} |
| e6 | ChuThe | D37/K4 | {"catalog_id": "CT:nguoi-dieu-khien-xe"} |
| e1 | HanhVi | D37/K4/a | {"span": "Điều khiển phương tiện không gắn biển số tạm thời hoặc gắn biển số tạm thời không do cơ quan có thẩm quyền cấp", "dieu_kien": "nếu có quy định phải gắn biển số tạm thời"} |
| e2 | HanhVi | D37/K4/b | {"span": "Điều khiển xe ô tô có tay lái bên phải tham gia giao thông mà không đi theo đoàn, không có người, phương tiện hỗ trợ, hướng dẫn giao thông theo quy định"} |
| e5 | PhuongTien | D37/K4/b | {"catalog_id": "PT:xe-o-to"} |

- QUY_DINH_HANH_VI: unit:ND168-2024/D37/K4/a → e1
- QUY_DINH_HANH_VI: unit:ND168-2024/D37/K4/b → e2
- BI_XU_PHAT: unit:ND168-2024/D37/K4/a → e3
- BI_XU_PHAT: unit:ND168-2024/D37/K4/b → e3
- AP_DUNG_CHO: unit:ND168-2024/D37/K4 → e4
- AP_DUNG_CHO: unit:ND168-2024/D37/K4 → e6
- AP_DUNG_CHO: unit:ND168-2024/D37/K4/b → e5

## ND168-2024/D6/K12@2026-11-03 · nd168_che_tai · tier A · ĐÃ DUYỆT

Điều: Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ

```
[ND168-2024/D6/K12] 12. Phạt tiền từ 40.000.000 đồng đến 50.000.000 đồng đối với người điều khiển xe thực hiện hành vi điều khiển xe lạng lách, đánh võng trên đường bộ; chạy quá tốc độ đuổi nhau trên đường bộ; dùng chân điều khiển vô lăng xe khi xe đang chạy trên đường bộ.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e2 | CheTai | D6/K12 | {"loai": "phat_tien", "min_vnd": 40000000, "max_vnd": 50000000} |
| e3 | PhuongTien | D6/K12 | {"catalog_id": "PT:xe-o-to"} |
| e4 | PhuongTien | D6/K12 | {"catalog_id": "PT:xe-cho-nguoi-bon-banh-co-gan-dong-co"} |
| e5 | PhuongTien | D6/K12 | {"catalog_id": "PT:xe-cho-hang-bon-banh-co-gan-dong-co"} |
| e6 | PhuongTien | D6/K12 | {"catalog_id": "PT:xe-tuong-tu-xe-o-to"} |
| e7 | ChuThe | D6/K12 | {"catalog_id": "CT:nguoi-dieu-khien-xe"} |
| h1 | HanhVi | D6/K12 | {"ten": "điều khiển xe lạng lách, đánh võng", "span": "điều khiển xe lạng lách, đánh võng trên đường bộ"} |
| h2 | HanhVi | D6/K12 | {"ten": "chạy quá tốc độ đuổi nhau", "span": "chạy quá tốc độ đuổi nhau trên đường bộ"} |
| h3 | HanhVi | D6/K12 | {"ten": "dùng chân điều khiển vô lăng xe khi xe đang chạy", "span": "dùng chân điều khiển vô lăng xe khi xe đang chạy trên đường bộ"} |

- QUY_DINH_HANH_VI: unit:ND168-2024/D6/K12 → h1
- QUY_DINH_HANH_VI: unit:ND168-2024/D6/K12 → h2
- QUY_DINH_HANH_VI: unit:ND168-2024/D6/K12 → h3
- BI_XU_PHAT: unit:ND168-2024/D6/K12 → e2
- AP_DUNG_CHO: unit:ND168-2024/D6/K12 → e3
- AP_DUNG_CHO: unit:ND168-2024/D6/K12 → e4
- AP_DUNG_CHO: unit:ND168-2024/D6/K12 → e5
- AP_DUNG_CHO: unit:ND168-2024/D6/K12 → e6
- AP_DUNG_CHO: unit:ND168-2024/D6/K12 → e7

## ND168-2024/D32/K10@2026-11-03 · nd168_che_tai · tier A · ĐÃ DUYỆT

Điều: Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ

```
[ND168-2024/D32/K10] 10. Phạt tiền từ 8.000.000 đồng đến 10.000.000 đồng đối với cá nhân, từ 16.000.000 đồng đến 20.000.000 đồng đối với tổ chức là chủ xe mô tô, xe gắn máy và các loại xe tương tự xe mô tô, các loại xe tương tự xe gắn máy thực hiện hành vi vi phạm giao xe hoặc để cho người không đủ điều kiện theo quy định tại khoản 1 Điều 56 của Luật Trật tự, an toàn giao thông đường bộ điều khiển xe tham gia giao thông (bao gồm cả trường hợp người điều khiển phương tiện có giấy phép lái xe nhưng đang trong thời gian bị tước quyền sử dụng).
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e1 | HanhVi | D32/K10 | {"ten": "giao xe hoặc để người không đủ điều kiện điều khiển xe tham gia giao thông", "span": "giao xe hoặc để cho người không đủ điều kiện theo quy định tại khoản 1 Điều 56 của Luật Trật tự, an toàn giao thông đường bộ điều khiển xe tham gia giao thông", "dieu_kien": "bao gồm cả trường hợp người điều khiển phương tiện có giấy phép lái xe nhưng đang trong thời gian bị tước quyền sử dụng"} |
| e10 | ChuThe | D32/K10 | {"catalog_id": "CT:to-chuc"} |
| e2 | CheTai | D32/K10 | {"loai": "phat_tien", "min_vnd": 8000000, "max_vnd": 10000000} |
| e3 | CheTai | D32/K10 | {"loai": "phat_tien", "min_vnd": 16000000, "max_vnd": 20000000} |
| e4 | PhuongTien | D32/K10 | {"catalog_id": "PT:xe-mo-to"} |
| e5 | PhuongTien | D32/K10 | {"catalog_id": "PT:xe-gan-may"} |
| e6 | PhuongTien | D32/K10 | {"catalog_id": "PT:xe-tuong-tu-xe-mo-to"} |
| e7 | PhuongTien | D32/K10 | {"catalog_id": "PT:xe-tuong-tu-xe-gan-may"} |
| e8 | ChuThe | D32/K10 | {"catalog_id": "CT:chu-xe"} |
| e9 | ChuThe | D32/K10 | {"catalog_id": "CT:ca-nhan"} |

- QUY_DINH_HANH_VI: unit:ND168-2024/D32/K10 → e1
- BI_XU_PHAT: unit:ND168-2024/D32/K10 → e2
- BI_XU_PHAT: unit:ND168-2024/D32/K10 → e3
- AP_DUNG_CHO: unit:ND168-2024/D32/K10 → e10
- AP_DUNG_CHO: unit:ND168-2024/D32/K10 → e4
- AP_DUNG_CHO: unit:ND168-2024/D32/K10 → e5
- AP_DUNG_CHO: unit:ND168-2024/D32/K10 → e6
- AP_DUNG_CHO: unit:ND168-2024/D32/K10 → e7
- AP_DUNG_CHO: unit:ND168-2024/D32/K10 → e8
- AP_DUNG_CHO: unit:ND168-2024/D32/K10 → e9

Bản nháp bị bỏ 2 mục:
- so_lech_regex: {"id": "e3", "type": "CheTai", "unit_id": "ND168-2024/D32/K10", "ten": null, "span": null, "dieu_kien": null, "catalog_id": null, "loai": "phat_tien", "min_vnd": 16000000, "max_vnd": 20000000, "min_th
- dich_khong_hop_le: {"type": "BI_XU_PHAT", "src": "unit:ND168-2024/D32/K10", "dst": "e3"}

## ND168-2024/D32/K3@2026-11-03 · nd168_che_tai · tier A · ĐÃ DUYỆT

Điều: Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ

```
[ND168-2024/D32/K3] 3. Phạt tiền từ 800.000 đồng đến 1.000.000 đồng đối với cá nhân, từ 1.600.000 đồng đến 2.000.000 đồng đối với tổ chức là chủ xe mô tô, xe gắn máy và các loại xe tương tự xe mô tô, các loại xe tương tự xe gắn máy thực hiện một trong các hành vi vi phạm sau đây:
[ND168-2024/D32/K3/a] a) Không làm thủ tục cấp chứng nhận đăng ký xe, biển số xe trong trường hợp thay đổi chủ xe theo quy định;
[ND168-2024/D32/K3/b] b) Không làm thủ tục đổi chứng nhận đăng ký xe, biển số xe theo quy định;
[ND168-2024/D32/K3/c] c) Lắp đặt, sử dụng thiết bị âm thanh, ánh sáng trên xe gây mất trật tự, an toàn giao thông đường bộ.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e10 | ChuThe | D32/K3 | {"catalog_id": "CT:ca-nhan"} |
| e11 | ChuThe | D32/K3 | {"catalog_id": "CT:to-chuc"} |
| e12 | ChuThe | D32/K3 | {"catalog_id": "CT:chu-xe"} |
| e4 | CheTai | D32/K3 | {"loai": "phat_tien", "min_vnd": 800000, "max_vnd": 1000000} |
| e5 | CheTai | D32/K3 | {"loai": "phat_tien", "min_vnd": 1600000, "max_vnd": 2000000} |
| e6 | PhuongTien | D32/K3 | {"catalog_id": "PT:xe-mo-to"} |
| e7 | PhuongTien | D32/K3 | {"catalog_id": "PT:xe-gan-may"} |
| e8 | PhuongTien | D32/K3 | {"catalog_id": "PT:xe-tuong-tu-xe-mo-to"} |
| e9 | PhuongTien | D32/K3 | {"catalog_id": "PT:xe-tuong-tu-xe-gan-may"} |
| e1 | HanhVi | D32/K3/a | {"span": "Không làm thủ tục cấp chứng nhận đăng ký xe, biển số xe trong trường hợp thay đổi chủ xe theo quy định"} |
| e2 | HanhVi | D32/K3/b | {"span": "Không làm thủ tục đổi chứng nhận đăng ký xe, biển số xe theo quy định"} |
| e3 | HanhVi | D32/K3/c | {"span": "Lắp đặt, sử dụng thiết bị âm thanh, ánh sáng trên xe gây mất trật tự, an toàn giao thông đường bộ"} |

- QUY_DINH_HANH_VI: unit:ND168-2024/D32/K3/a → e1
- QUY_DINH_HANH_VI: unit:ND168-2024/D32/K3/b → e2
- QUY_DINH_HANH_VI: unit:ND168-2024/D32/K3/c → e3
- BI_XU_PHAT: unit:ND168-2024/D32/K3/a → e4
- BI_XU_PHAT: unit:ND168-2024/D32/K3/a → e5
- BI_XU_PHAT: unit:ND168-2024/D32/K3/b → e4
- BI_XU_PHAT: unit:ND168-2024/D32/K3/b → e5
- BI_XU_PHAT: unit:ND168-2024/D32/K3/c → e4
- BI_XU_PHAT: unit:ND168-2024/D32/K3/c → e5
- AP_DUNG_CHO: unit:ND168-2024/D32/K3 → e10
- AP_DUNG_CHO: unit:ND168-2024/D32/K3 → e11
- AP_DUNG_CHO: unit:ND168-2024/D32/K3 → e12
- AP_DUNG_CHO: unit:ND168-2024/D32/K3 → e6
- AP_DUNG_CHO: unit:ND168-2024/D32/K3 → e7
- AP_DUNG_CHO: unit:ND168-2024/D32/K3 → e8
- AP_DUNG_CHO: unit:ND168-2024/D32/K3 → e9

Bản nháp bị bỏ 2 mục:
- so_lech_regex: {"id": "e5", "type": "CheTai", "unit_id": "ND168-2024/D32/K3", "ten": null, "span": null, "dieu_kien": null, "catalog_id": null, "loai": "phat_tien", "min_vnd": 1600000, "max_vnd": 2000000, "min_thang
- dich_khong_hop_le: {"type": "BI_XU_PHAT", "src": "unit:ND168-2024/D32/K3", "dst": "e5"}

## ND168-2024/D8/K6@2026-11-03 · nd168_che_tai · tier A · ĐÃ DUYỆT

Điều: Xử phạt người điều khiển xe máy chuyên dùng vi phạm quy tắc giao thông đường bộ

```
[ND168-2024/D8/K6] 6. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
[ND168-2024/D8/K6/a] a) Chạy quá tốc độ quy định trên 20 km/h;
[ND168-2024/D8/K6/b] b) Dừng xe, đỗ xe trên đường cao tốc không đúng nơi quy định; không có báo hiệu bằng đèn khẩn cấp khi gặp sự cố kỹ thuật hoặc bất khả kháng khác buộc phải dừng xe, đỗ xe ở làn dừng xe khẩn cấp hoặc dải dừng xe khẩn cấp trên đường cao tốc; không có báo hiệu bằng đèn khẩn cấp, không đặt biển cảnh báo “Chú ý xe đỗ” (hoặc đèn cảnh báo) về phía sau xe khoảng cách tối thiểu 150 mét khi gặp sự cố kỹ thuật hoặc bất khả kháng khác buộc phải dừng xe, đỗ xe trên một phần làn đường xe chạy trên đường cao tốc;
[ND168-2024/D8/K6/c] c) Điều khiển xe trên đường mà trong máu hoặc hơi thở có nồng độ cồn nhưng chưa vượt quá 50 miligam/100 mililít máu hoặc chưa vượt quá 0,25 miligam/1 lít khí thở;
[ND168-2024/D8/K6/d] d) Đi vào khu vực cấm, đường có biển báo hiệu có nội dung cấm đi vào đối với loại phương tiện đang điều khiển, trừ các hành vi vi phạm quy định tại điểm d khoản 7, điểm đ khoản 9 Điều này và các trường hợp xe ưu tiên đang đi làm nhiệm vụ khẩn cấp theo quy định;
[ND168-2024/D8/K6/đ] đ) Không đi bên phải theo chiều đi của mình; đi không đúng phần đường hoặc làn đường quy định (làn cùng chiều hoặc làn ngược chiều); điều khiển xe đi qua dải phân cách cố định ở giữa hai phần đường xe chạy, trừ các hành vi vi phạm quy định tại điểm e khoản 6, điểm d khoản 7, điểm đ khoản 9 Điều này;
[ND168-2024/D8/K6/e] e) Không tuân thủ các quy định khi vào hoặc ra đường cao tốc; điều khiển xe chạy ở làn dừng xe khẩn cấp hoặc phần lề đường của đường cao tốc; không tuân thủ quy định về khoảng cách an toàn đối với xe chạy liền trước khi chạy trên đường cao tốc;
[ND168-2024/D8/K6/g] g) Không nhường đường hoặc gây cản trở xe được quyền ưu tiên đang phát tín hiệu ưu tiên đi làm nhiệm vụ;
[ND168-2024/D8/K6/h] h) Chuyển làn đường không đúng nơi cho phép hoặc không có tín hiệu báo trước khi chạy trên đường cao tốc hoặc chuyển làn đường không đúng quy định “mỗi lần chuyển làn đường chỉ được phép chuyển sang một làn đường liền kề hoặc chuyển làn đường không bảo đảm khoảng cách an toàn với xe phía trước, xe phía sau, xe hai bên”;
[ND168-2024/D8/K6/i] i) Không giảm tốc độ (hoặc dừng lại) và nhường đường khi điều khiển xe đi từ đường không ưu tiên ra đường ưu tiên, từ đường nhánh ra đường chính.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e10 | CheTai | D8/K6 | {"loai": "phat_tien", "min_vnd": 3000000, "max_vnd": 5000000} |
| e11 | PhuongTien | D8/K6 | {"catalog_id": "PT:xe-may-chuyen-dung"} |
| e12 | ChuThe | D8/K6 | {"catalog_id": "CT:nguoi-dieu-khien-xe"} |
| e1 | HanhVi | D8/K6/a | {"ten": "chạy quá tốc độ quy định trên 20 km/h", "span": "Chạy quá tốc độ quy định trên 20 km/h"} |
| b1 | HanhVi | D8/K6/b | {"ten": "dừng, đỗ xe trên đường cao tốc không đúng nơi quy định", "span": "Dừng xe, đỗ xe trên đường cao tốc không đúng nơi quy định"} |
| b2 | HanhVi | D8/K6/b | {"ten": "không báo hiệu đèn khẩn cấp khi dừng ở làn khẩn cấp cao tốc", "span": "không có báo hiệu bằng đèn khẩn cấp khi gặp sự cố kỹ thuật hoặc bất khả kháng khác buộc phải dừng xe, đỗ xe ở làn dừng xe khẩn cấp hoặc dải dừng xe khẩn cấp trên đường cao tốc"} |
| b3 | HanhVi | D8/K6/b | {"ten": "không báo hiệu, không đặt biển cảnh báo khi dừng trên làn xe chạy cao tốc", "span": "không có báo hiệu bằng đèn khẩn cấp, không đặt biển cảnh báo “Chú ý xe đỗ” (hoặc đèn cảnh báo) về phía sau xe khoảng cách tối thiểu 150 mét khi gặp sự cố kỹ thuật hoặc bất khả kháng khác buộc phải dừng xe, đỗ xe trên một phần làn đường xe chạy trên đường cao tốc"} |
| e3 | HanhVi | D8/K6/c | {"ten": "điều khiển xe có nồng độ cồn chưa vượt mức thấp nhất", "span": "Điều khiển xe trên đường mà trong máu hoặc hơi thở có nồng độ cồn nhưng chưa vượt quá 50 miligam/100 mililít máu hoặc chưa vượt quá 0,25 miligam/1 lít khí thở"} |
| e4 | HanhVi | D8/K6/d | {"ten": "đi vào khu vực cấm, đường cấm", "span": "Đi vào khu vực cấm, đường có biển báo hiệu có nội dung cấm đi vào đối với loại phương tiện đang điều khiển"} |
| g1 | HanhVi | D8/K6/e | {"ten": "không tuân thủ quy định khi vào, ra đường cao tốc", "span": "Không tuân thủ các quy định khi vào hoặc ra đường cao tốc"} |
| g2 | HanhVi | D8/K6/e | {"ten": "chạy ở làn dừng khẩn cấp, lề đường cao tốc", "span": "điều khiển xe chạy ở làn dừng xe khẩn cấp hoặc phần lề đường của đường cao tốc"} |
| g3 | HanhVi | D8/K6/e | {"ten": "không giữ khoảng cách an toàn trên đường cao tốc", "span": "không tuân thủ quy định về khoảng cách an toàn đối với xe chạy liền trước khi chạy trên đường cao tốc"} |
| e7 | HanhVi | D8/K6/g | {"ten": "không nhường đường xe ưu tiên", "span": "Không nhường đường hoặc gây cản trở xe được quyền ưu tiên đang phát tín hiệu ưu tiên đi làm nhiệm vụ"} |
| e8 | HanhVi | D8/K6/h | {"ten": "chuyển làn đường không đúng quy định trên đường cao tốc", "span": "Chuyển làn đường không đúng nơi cho phép hoặc không có tín hiệu báo trước khi chạy trên đường cao tốc hoặc chuyển làn đường không đúng quy định “mỗi lần chuyển làn đường chỉ được phép chuyển sang một làn đường liền kề hoặc chuyển làn đường không bảo đảm khoảng cách an toàn với xe phía trước, xe phía sau, xe hai bên”"} |
| e9 | HanhVi | D8/K6/i | {"ten": "không giảm tốc độ, nhường đường khi ra đường ưu tiên", "span": "Không giảm tốc độ (hoặc dừng lại) và nhường đường khi điều khiển xe đi từ đường không ưu tiên ra đường ưu tiên, từ đường nhánh ra đường chính"} |
| d1 | HanhVi | D8/K6/đ | {"ten": "không đi bên phải theo chiều đi", "span": "Không đi bên phải theo chiều đi của mình"} |
| d2 | HanhVi | D8/K6/đ | {"ten": "đi không đúng phần đường, làn đường", "span": "đi không đúng phần đường hoặc làn đường quy định (làn cùng chiều hoặc làn ngược chiều)"} |
| d3 | HanhVi | D8/K6/đ | {"ten": "đi qua dải phân cách cố định", "span": "điều khiển xe đi qua dải phân cách cố định ở giữa hai phần đường xe chạy"} |

- QUY_DINH_HANH_VI: unit:ND168-2024/D8/K6/a → e1
- QUY_DINH_HANH_VI: unit:ND168-2024/D8/K6/b → b1
- QUY_DINH_HANH_VI: unit:ND168-2024/D8/K6/b → b2
- QUY_DINH_HANH_VI: unit:ND168-2024/D8/K6/b → b3
- QUY_DINH_HANH_VI: unit:ND168-2024/D8/K6/c → e3
- QUY_DINH_HANH_VI: unit:ND168-2024/D8/K6/d → e4
- QUY_DINH_HANH_VI: unit:ND168-2024/D8/K6/e → g1
- QUY_DINH_HANH_VI: unit:ND168-2024/D8/K6/e → g2
- QUY_DINH_HANH_VI: unit:ND168-2024/D8/K6/e → g3
- QUY_DINH_HANH_VI: unit:ND168-2024/D8/K6/g → e7
- QUY_DINH_HANH_VI: unit:ND168-2024/D8/K6/h → e8
- QUY_DINH_HANH_VI: unit:ND168-2024/D8/K6/i → e9
- QUY_DINH_HANH_VI: unit:ND168-2024/D8/K6/đ → d1
- QUY_DINH_HANH_VI: unit:ND168-2024/D8/K6/đ → d2
- QUY_DINH_HANH_VI: unit:ND168-2024/D8/K6/đ → d3
- BI_XU_PHAT: unit:ND168-2024/D8/K6/a → e10
- BI_XU_PHAT: unit:ND168-2024/D8/K6/b → e10
- BI_XU_PHAT: unit:ND168-2024/D8/K6/c → e10
- BI_XU_PHAT: unit:ND168-2024/D8/K6/d → e10
- BI_XU_PHAT: unit:ND168-2024/D8/K6/e → e10
- BI_XU_PHAT: unit:ND168-2024/D8/K6/g → e10
- BI_XU_PHAT: unit:ND168-2024/D8/K6/h → e10
- BI_XU_PHAT: unit:ND168-2024/D8/K6/i → e10
- BI_XU_PHAT: unit:ND168-2024/D8/K6/đ → e10
- AP_DUNG_CHO: unit:ND168-2024/D8/K6 → e11
- AP_DUNG_CHO: unit:ND168-2024/D8/K6 → e12

## ND168-2024/D7/K5@2026-11-03 · nd168_che_tai · tier A · ĐÃ DUYỆT

Điều: Xử phạt, trừ điểm giấy phép lái của người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy vi phạm quy tắc giao thông đường bộ

```
[ND168-2024/D7/K5] 5. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
[ND168-2024/D7/K5/a] a) Điều khiển xe có liên quan trực tiếp đến vụ tai nạn giao thông mà không dừng ngay phương tiện, không giữ nguyên hiện trường, không trợ giúp người bị nạn, trừ hành vi vi phạm quy định tại điểm c khoản 9 Điều này;
[ND168-2024/D7/K5/b] b) Chuyển hướng không nhường quyền đi trước cho: người đi bộ, xe lăn của người khuyết tật qua đường tại nơi có vạch kẻ đường dành cho người đi bộ; xe thô sơ đang đi trên phần đường dành cho xe thô sơ;
[ND168-2024/D7/K5/c] c) Chuyển hướng không nhường đường cho: các xe đi ngược chiều; người đi bộ, xe thô sơ đang qua đường tại nơi không có vạch kẻ đường cho người đi bộ.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| c1 | ChuThe | D7/K5 | {"catalog_id": "CT:nguoi-dieu-khien-xe"} |
| e4 | CheTai | D7/K5 | {"loai": "phat_tien", "min_vnd": 1000000, "max_vnd": 2000000} |
| p1 | PhuongTien | D7/K5 | {"catalog_id": "PT:xe-mo-to"} |
| p2 | PhuongTien | D7/K5 | {"catalog_id": "PT:xe-gan-may"} |
| p3 | PhuongTien | D7/K5 | {"catalog_id": "PT:xe-tuong-tu-xe-mo-to"} |
| p4 | PhuongTien | D7/K5 | {"catalog_id": "PT:xe-tuong-tu-xe-gan-may"} |
| e1 | HanhVi | D7/K5/a | {"ten": "gây tai nạn mà không dừng, không giữ hiện trường, không trợ giúp người bị nạn", "span": "Điều khiển xe có liên quan trực tiếp đến vụ tai nạn giao thông mà không dừng ngay phương tiện, không giữ nguyên hiện trường, không trợ giúp người bị nạn"} |
| e2 | HanhVi | D7/K5/b | {"ten": "chuyển hướng không nhường quyền đi trước cho người đi bộ, xe lăn, xe thô sơ", "span": "Chuyển hướng không nhường quyền đi trước cho: người đi bộ, xe lăn của người khuyết tật qua đường tại nơi có vạch kẻ đường dành cho người đi bộ; xe thô sơ đang đi trên phần đường dành cho xe thô sơ"} |
| e3 | HanhVi | D7/K5/c | {"ten": "chuyển hướng không nhường đường", "span": "Chuyển hướng không nhường đường cho: các xe đi ngược chiều; người đi bộ, xe thô sơ đang qua đường tại nơi không có vạch kẻ đường cho người đi bộ"} |

- QUY_DINH_HANH_VI: unit:ND168-2024/D7/K5/a → e1
- QUY_DINH_HANH_VI: unit:ND168-2024/D7/K5/b → e2
- QUY_DINH_HANH_VI: unit:ND168-2024/D7/K5/c → e3
- BI_XU_PHAT: unit:ND168-2024/D7/K5/a → e4
- BI_XU_PHAT: unit:ND168-2024/D7/K5/b → e4
- BI_XU_PHAT: unit:ND168-2024/D7/K5/c → e4
- AP_DUNG_CHO: unit:ND168-2024/D7/K5 → c1
- AP_DUNG_CHO: unit:ND168-2024/D7/K5 → p1
- AP_DUNG_CHO: unit:ND168-2024/D7/K5 → p2
- AP_DUNG_CHO: unit:ND168-2024/D7/K5 → p3
- AP_DUNG_CHO: unit:ND168-2024/D7/K5 → p4

## ND168-2024/D40/K3@2026-11-03 · nd168_che_tai · tier A · ĐÃ DUYỆT

Điều: Xử phạt các hành vi vi phạm quy định về hoạt động đăng kiểm xe cơ giới, xe máy chuyên dùng, phụ tùng xe cơ giới

```
[ND168-2024/D40/K3] 3. Phạt tiền từ 10.000.000 đồng đến 15.000.000 đồng đối với cơ sở thử nghiệm, chứng nhận xe cơ giới, xe máy chuyên dùng, phụ tùng xe cơ giới trong sản xuất, lắp ráp và nhập khẩu thực hiện một trong các hành vi vi phạm sau đây:
[ND168-2024/D40/K3/a] a) Không thực hiện niêm yết công khai các trình tự, thủ tục thử nghiệm, chứng nhận theo quy định;
[ND168-2024/D40/K3/b] b) Thực hiện việc thử nghiệm, chứng nhận không đúng quy định;
[ND168-2024/D40/K3/c] c) Phân công người không đủ điều kiện thực hiện việc thử nghiệm, chứng nhận;
[ND168-2024/D40/K3/d] đ) Sử dụng thiết bị, dụng cụ không đảm bảo theo quy định của pháp luật về đo lường để kiểm tra, thử nghiệm;
[ND168-2024/D40/K3/đ] đ) Có từ 02 lượt đăng kiểm viên trở lên bị xử phạt theo quy định tại khoản 1 Điều này trong thời hạn 12 tháng tính từ lần bị xử phạt đầu tiên;
[ND168-2024/D40/K3/e] c) Lưu trữ hồ sơ, tài liệu, dữ liệu chứng nhận không đúng quy định.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e7 | CheTai | D40/K3 | {"loai": "phat_tien", "min_vnd": 10000000, "max_vnd": 15000000} |
| e8 | PhuongTien | D40/K3 | {"catalog_id": "PT:xe-co-gioi"} |
| e9 | PhuongTien | D40/K3 | {"catalog_id": "PT:xe-may-chuyen-dung"} |
| e1 | HanhVi | D40/K3/a | {"span": "Không thực hiện niêm yết công khai các trình tự, thủ tục thử nghiệm, chứng nhận theo quy định"} |
| e2 | HanhVi | D40/K3/b | {"span": "Thực hiện việc thử nghiệm, chứng nhận không đúng quy định"} |
| e3 | HanhVi | D40/K3/c | {"span": "Phân công người không đủ điều kiện thực hiện việc thử nghiệm, chứng nhận"} |
| e4 | HanhVi | D40/K3/d | {"span": "Sử dụng thiết bị, dụng cụ không đảm bảo theo quy định của pháp luật về đo lường để kiểm tra, thử nghiệm"} |
| e6 | HanhVi | D40/K3/e | {"span": "Lưu trữ hồ sơ, tài liệu, dữ liệu chứng nhận không đúng quy định"} |
| e5 | HanhVi | D40/K3/đ | {"span": "Có từ 02 lượt đăng kiểm viên trở lên bị xử phạt theo quy định tại khoản 1 Điều này trong thời hạn 12 tháng tính từ lần bị xử phạt đầu tiên"} |

- QUY_DINH_HANH_VI: unit:ND168-2024/D40/K3/a → e1
- QUY_DINH_HANH_VI: unit:ND168-2024/D40/K3/b → e2
- QUY_DINH_HANH_VI: unit:ND168-2024/D40/K3/c → e3
- QUY_DINH_HANH_VI: unit:ND168-2024/D40/K3/d → e4
- QUY_DINH_HANH_VI: unit:ND168-2024/D40/K3/e → e6
- QUY_DINH_HANH_VI: unit:ND168-2024/D40/K3/đ → e5
- BI_XU_PHAT: unit:ND168-2024/D40/K3/a → e7
- BI_XU_PHAT: unit:ND168-2024/D40/K3/b → e7
- BI_XU_PHAT: unit:ND168-2024/D40/K3/c → e7
- BI_XU_PHAT: unit:ND168-2024/D40/K3/d → e7
- BI_XU_PHAT: unit:ND168-2024/D40/K3/e → e7
- BI_XU_PHAT: unit:ND168-2024/D40/K3/đ → e7
- AP_DUNG_CHO: unit:ND168-2024/D40/K3 → e8
- AP_DUNG_CHO: unit:ND168-2024/D40/K3 → e9

Bản nháp bị bỏ 4 mục:
- ngoai_danh_muc: {"id": "e10", "type": "PhuongTien", "unit_id": "ND168-2024/D40/K3", "ten": null, "span": null, "dieu_kien": null, "catalog_id": "PT:phu-tung-xe-co-gioi", "loai": null, "min_vnd": null, "max_vnd": null
- ngoai_danh_muc: {"id": "e11", "type": "ChuThe", "unit_id": "ND168-2024/D40/K3", "ten": null, "span": null, "dieu_kien": null, "catalog_id": "CT:co-so-thu-nghiem-chung-nhan", "loai": null, "min_vnd": null, "max_vnd": 
- dich_khong_hop_le: {"type": "AP_DUNG_CHO", "src": "unit:ND168-2024/D40/K3", "dst": "e10"}
- dich_khong_hop_le: {"type": "AP_DUNG_CHO", "src": "unit:ND168-2024/D40/K3", "dst": "e11"}

## ND168-2024/D16/K5@2026-11-03 · nd168_bo_sung_tru_diem · tier A · ĐÃ DUYỆT

Điều: Xử phạt người điều khiển xe máy chuyên dùng (kể cả rơ moóc được kéo theo) vi phạm quy định về điều kiện của phương tiện khi tham gia giao thông

```
[ND168-2024/D16/K5] 5. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị áp dụng biện pháp khắc phục hậu quả sau đây:
[ND168-2024/D16/K5/a] a) Thực hiện hành vi vi phạm quy định tại điểm b, điểm c, điểm d khoản 1 Điều này buộc lắp đầy đủ thiết bị hoặc thay thế thiết bị đủ tiêu chuẩn, quy chuẩn an toàn kỹ thuật hoặc khôi phục lại tính năng kỹ thuật của thiết bị theo quy định;
[ND168-2024/D16/K5/b] b) Thực hiện hành vi quy định tại điểm đ khoản 2 Điều này buộc nộp lại chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe), giấy chứng nhận, tem kiểm định an toàn kỹ thuật và bảo vệ môi trường bị tẩy xóa.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e3 | ChuThe | D16/K5 | {"catalog_id": "CT:nguoi-dieu-khien-xe"} |
| e4 | PhuongTien | D16/K5 | {"catalog_id": "PT:xe-may-chuyen-dung"} |
| e5 | PhuongTien | D16/K5 | {"catalog_id": "PT:ro-mooc"} |
| e1 | BienPhapBoSung | D16/K5/a | {"ten": "buộc lắp đầy đủ thiết bị hoặc thay thế thiết bị đủ tiêu chuẩn, quy chuẩn an toàn kỹ thuật hoặc khôi phục lại tính năng kỹ thuật của thiết bị theo quy định"} |
| e2 | BienPhapBoSung | D16/K5/b | {"ten": "buộc nộp lại chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe), giấy chứng nhận, tem kiểm định an toàn kỹ thuật và bảo vệ môi trường bị tẩy xóa"} |

- BI_XU_PHAT: unit:ND168-2024/D16/K1/b → e1
- BI_XU_PHAT: unit:ND168-2024/D16/K1/c → e1
- BI_XU_PHAT: unit:ND168-2024/D16/K1/d → e1
- BI_XU_PHAT: unit:ND168-2024/D16/K2/đ → e2
- AP_DUNG_CHO: unit:ND168-2024/D16/K5 → e3
- AP_DUNG_CHO: unit:ND168-2024/D16/K5 → e4
- AP_DUNG_CHO: unit:ND168-2024/D16/K5 → e5

## ND168-2024/D32/K19@2026-11-03 · nd168_bo_sung_tru_diem · tier A · ĐÃ DUYỆT

Điều: Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ

```
[ND168-2024/D32/K19] 19. Ngoài việc bị áp dụng hình thức xử phạt, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị áp dụng các biện pháp khắc phục hậu quả sau đây:
[ND168-2024/D32/K19/a] a) Thực hiện hành vi quy định tại điểm a khoản 1, điểm i khoản 7 Điều này buộc khôi phục lại nhãn hiệu, màu sơn ghi trong chứng nhận đăng ký xe theo quy định;
[ND168-2024/D32/K19/b] b) Thực hiện hành vi quy định tại điểm a khoản 2 Điều này buộc thay thế thiết bị đủ tiêu chuẩn an toàn kỹ thuật theo quy định (lắp đúng loại kính an toàn);
[ND168-2024/D32/K19/c] c) Thực hiện hành vi quy định tại khoản 4, điểm e khoản 9 Điều này buộc thực hiện đúng quy định về biển số xe, quy định về kẻ hoặc dán chữ, số biển số, thông tin trên thành xe, cửa xe;
[ND168-2024/D32/K19/d] d) Thực hiện hành vi quy định tại điểm d khoản 11, điểm h khoản 14, điểm c khoản 16 Điều này buộc khôi phục lại hình dáng, kích thước, tình trạng an toàn kỹ thuật ban đầu của xe và đăng kiểm lại trước khi đưa phương tiện ra tham gia giao thông;
[ND168-2024/D32/K19/đ] đ) Thực hiện hành vi quy định tại điểm e khoản 7, điểm b khoản 11, điểm a khoản 13, khoản 15, điểm b khoản 16 Điều này mà phương tiện đó có thùng xe, khối lượng hàng hóa cho phép chuyên chở không đúng theo quy định hiện hành thì còn bị buộc thực hiện điều chỉnh thùng xe theo đúng quy định hiện hành, đăng kiểm lại và điều chỉnh lại khối lượng hàng hóa cho phép chuyên chở ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường theo quy định hiện hành trước khi đưa phương tiện ra tham gia giao thông;
[ND168-2024/D32/K19/e] e) Thực hiện hành vi vi phạm quy định tại điểm đ, điểm e, điểm g khoản 7; điểm c khoản 9; điểm b, điểm c khoản 11; điểm a, điểm b, điểm c khoản 13; điểm a, điểm b, điểm c, điểm d, điểm đ, điểm e, điểm g khoản 14; khoản 15; điểm a, điểm b khoản 16 Điều này nếu gây hư hại cầu, đường phải khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra;
[ND168-2024/D32/K19/g] g) Thực hiện hành vi vi phạm quy định tại điểm b khoản 3; điểm b, điểm c, điểm h khoản 7; điểm d, điểm đ khoản 8; điểm a khoản 12 Điều này buộc làm thủ tục đổi, thu hồi, cấp mới, cấp chứng nhận đăng ký xe, biển số xe, chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường theo quy định (trừ trường hợp bị tịch thu phương tiện);
[ND168-2024/D32/K19/h] h) Thực hiện hành vi quy định tại điểm c khoản 3, điểm k khoản 7 Điều này buộc tháo dỡ thiết bị âm thanh, ánh sáng lắp đặt trên xe gây mất trật tự, an toàn giao thông đường bộ;
[ND168-2024/D32/K19/i] i) Thực hiện hành vi quy định tại điểm e khoản 8, điểm đ khoản 9 Điều này buộc nộp lại chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe), giấy chứng nhận, tem kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe bị tẩy xóa;
[ND168-2024/D32/K19/k] k) Thực hiện hành vi vi phạm quy định tại điểm l khoản 7 Điều này buộc điều chỉnh lại chỉ số trên đồng hồ báo quãng đường của xe ô tô bị làm sai lệch;
[ND168-2024/D32/K19/l] l) Thực hiện hành vi vi phạm quy định tại điểm o khoản 7, khoản 9a Điều này buộc lắp đặt dụng cụ, thiết bị chuyên dùng để cứu hộ, hỗ trợ cứu hộ, thiết bị giám sát hành trình, thiết bị ghi nhận hình ảnh người lái xe trên xe theo đúng quy định.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| c1 | ChuThe | D32/K19 | {"catalog_id": "CT:ca-nhan"} |
| c2 | ChuThe | D32/K19 | {"catalog_id": "CT:to-chuc"} |
| c3 | ChuThe | D32/K19 | {"catalog_id": "CT:chu-phuong-tien"} |
| e1 | BienPhapBoSung | D32/K19/a | {"ten": "buộc khôi phục lại nhãn hiệu, màu sơn ghi trong chứng nhận đăng ký xe theo quy định"} |
| e2 | BienPhapBoSung | D32/K19/b | {"ten": "buộc thay thế thiết bị đủ tiêu chuẩn an toàn kỹ thuật theo quy định (lắp đúng loại kính an toàn)"} |
| e3 | BienPhapBoSung | D32/K19/c | {"ten": "buộc thực hiện đúng quy định về biển số xe, quy định về kẻ hoặc dán chữ, số biển số, thông tin trên thành xe, cửa xe"} |
| e4 | BienPhapBoSung | D32/K19/d | {"ten": "buộc khôi phục lại hình dáng, kích thước, tình trạng an toàn kỹ thuật ban đầu của xe và đăng kiểm lại trước khi đưa phương tiện ra tham gia giao thông"} |
| e6 | BienPhapBoSung | D32/K19/e | {"ten": "phải khôi phục lại tình trạng ban đầu đã bị thay đổi do vi phạm hành chính gây ra"} |
| e7 | BienPhapBoSung | D32/K19/g | {"ten": "buộc làm thủ tục đổi, thu hồi, cấp mới, cấp chứng nhận đăng ký xe, biển số xe, chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường theo quy định"} |
| e8 | BienPhapBoSung | D32/K19/h | {"ten": "buộc tháo dỡ thiết bị âm thanh, ánh sáng lắp đặt trên xe gây mất trật tự, an toàn giao thông đường bộ"} |
| e9 | BienPhapBoSung | D32/K19/i | {"ten": "buộc nộp lại chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe), giấy chứng nhận, tem kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe bị tẩy xóa"} |
| e10 | BienPhapBoSung | D32/K19/k | {"ten": "buộc điều chỉnh lại chỉ số trên đồng hồ báo quãng đường của xe ô tô bị làm sai lệch"} |
| e11 | BienPhapBoSung | D32/K19/l | {"ten": "buộc lắp đặt dụng cụ, thiết bị chuyên dùng để cứu hộ, hỗ trợ cứu hộ, thiết bị giám sát hành trình, thiết bị ghi nhận hình ảnh người lái xe trên xe theo đúng quy định"} |
| e5 | BienPhapBoSung | D32/K19/đ | {"ten": "buộc thực hiện điều chỉnh thùng xe theo đúng quy định hiện hành, đăng kiểm lại và điều chỉnh lại khối lượng hàng hóa cho phép chuyên chở ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường theo quy định hiện hành trước khi đưa phương tiện ra tham gia giao thông"} |

- BI_XU_PHAT: unit:ND168-2024/D32/K1/a → e1
- BI_XU_PHAT: unit:ND168-2024/D32/K11/b → e5
- BI_XU_PHAT: unit:ND168-2024/D32/K11/b → e6
- BI_XU_PHAT: unit:ND168-2024/D32/K11/c → e6
- BI_XU_PHAT: unit:ND168-2024/D32/K11/d → e4
- BI_XU_PHAT: unit:ND168-2024/D32/K12/a → e7
- BI_XU_PHAT: unit:ND168-2024/D32/K13/a → e5
- BI_XU_PHAT: unit:ND168-2024/D32/K13/a → e6
- BI_XU_PHAT: unit:ND168-2024/D32/K13/b → e6
- BI_XU_PHAT: unit:ND168-2024/D32/K13/c → e6
- BI_XU_PHAT: unit:ND168-2024/D32/K14/a → e6
- BI_XU_PHAT: unit:ND168-2024/D32/K14/b → e6
- BI_XU_PHAT: unit:ND168-2024/D32/K14/c → e6
- BI_XU_PHAT: unit:ND168-2024/D32/K14/d → e6
- BI_XU_PHAT: unit:ND168-2024/D32/K14/e → e6
- BI_XU_PHAT: unit:ND168-2024/D32/K14/g → e6
- BI_XU_PHAT: unit:ND168-2024/D32/K14/h → e4
- BI_XU_PHAT: unit:ND168-2024/D32/K14/đ → e6
- BI_XU_PHAT: unit:ND168-2024/D32/K15 → e5
- BI_XU_PHAT: unit:ND168-2024/D32/K15 → e6
- BI_XU_PHAT: unit:ND168-2024/D32/K16/a → e6
- BI_XU_PHAT: unit:ND168-2024/D32/K16/b → e5
- BI_XU_PHAT: unit:ND168-2024/D32/K16/b → e6
- BI_XU_PHAT: unit:ND168-2024/D32/K16/c → e4
- BI_XU_PHAT: unit:ND168-2024/D32/K2/a → e2
- BI_XU_PHAT: unit:ND168-2024/D32/K3/b → e7
- BI_XU_PHAT: unit:ND168-2024/D32/K3/c → e8
- BI_XU_PHAT: unit:ND168-2024/D32/K4 → e3
- BI_XU_PHAT: unit:ND168-2024/D32/K7/b → e7
- BI_XU_PHAT: unit:ND168-2024/D32/K7/c → e7
- BI_XU_PHAT: unit:ND168-2024/D32/K7/e → e5
- BI_XU_PHAT: unit:ND168-2024/D32/K7/e → e6
- BI_XU_PHAT: unit:ND168-2024/D32/K7/g → e6
- BI_XU_PHAT: unit:ND168-2024/D32/K7/h → e7
- BI_XU_PHAT: unit:ND168-2024/D32/K7/i → e1
- BI_XU_PHAT: unit:ND168-2024/D32/K7/k → e8
- BI_XU_PHAT: unit:ND168-2024/D32/K7/l → e10
- BI_XU_PHAT: unit:ND168-2024/D32/K7/o → e11
- BI_XU_PHAT: unit:ND168-2024/D32/K7/đ → e6
- BI_XU_PHAT: unit:ND168-2024/D32/K8/d → e7
- BI_XU_PHAT: unit:ND168-2024/D32/K8/e → e9
- BI_XU_PHAT: unit:ND168-2024/D32/K8/đ → e7
- BI_XU_PHAT: unit:ND168-2024/D32/K9/c → e6
- BI_XU_PHAT: unit:ND168-2024/D32/K9/e → e3
- BI_XU_PHAT: unit:ND168-2024/D32/K9/đ → e9
- BI_XU_PHAT: unit:ND168-2024/D32/K9a/a → e11
- AP_DUNG_CHO: unit:ND168-2024/D32/K19 → c1
- AP_DUNG_CHO: unit:ND168-2024/D32/K19 → c2
- AP_DUNG_CHO: unit:ND168-2024/D32/K19 → c3

## ND168-2024/D7/K10@2026-11-03 · nd168_che_tai · tier A · ĐÃ DUYỆT

Điều: Xử phạt, trừ điểm giấy phép lái của người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy vi phạm quy tắc giao thông đường bộ

```
[ND168-2024/D7/K10] 10. Phạt tiền từ 10.000.000 đồng đến 14.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
[ND168-2024/D7/K10/a] a) Điều khiển xe không quan sát, giảm tốc độ hoặc dừng lại để bảo đảm an toàn theo quy định mà gây tai nạn giao thông; điều khiển xe chạy quá tốc độ quy định gây tai nạn giao thông; đi vào đường cao tốc, dừng xe, đỗ xe, quay đầu xe, lùi xe, vượt xe, chuyển hướng, chuyển làn đường không đúng quy định gây tai nạn giao thông; không đi đúng phần đường, làn đường, không giữ khoảng cách an toàn giữa hai xe theo quy định gây tai nạn giao thông hoặc đi vào đường có biển báo hiệu có nội dung cấm đi vào đối với loại phương tiện đang điều khiển, đi ngược chiều của đường một chiều, đi ngược chiều trên đường có biển “Cấm đi ngược chiều” gây tai nạn giao thông;
[ND168-2024/D7/K10/b] b) Vi phạm quy định tại một trong các điểm, khoản sau của Điều này mà gây tai nạn giao thông: điểm a, điểm d, điểm đ, điểm g, điểm h, điểm i, điểm k khoản 1; điểm c, điểm đ, điểm g khoản 2; điểm b, điểm e, điểm g, điểm h, điểm k khoản 3; điểm đ khoản 4; điểm c, điểm d khoản 6; điểm c, điểm d, điểm đ khoản 7; điểm a, điểm b, điểm h, điểm k khoản 9 Điều này.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| c1 | ChuThe | D7/K10 | {"catalog_id": "CT:nguoi-dieu-khien-xe"} |
| e5 | CheTai | D7/K10 | {"loai": "phat_tien", "min_vnd": 10000000, "max_vnd": 14000000} |
| p1 | PhuongTien | D7/K10 | {"catalog_id": "PT:xe-mo-to"} |
| p2 | PhuongTien | D7/K10 | {"catalog_id": "PT:xe-gan-may"} |
| p3 | PhuongTien | D7/K10 | {"catalog_id": "PT:xe-tuong-tu-xe-mo-to"} |
| p4 | PhuongTien | D7/K10 | {"catalog_id": "PT:xe-tuong-tu-xe-gan-may"} |
| e1 | HanhVi | D7/K10/a | {"span": "Điều khiển xe không quan sát, giảm tốc độ hoặc dừng lại để bảo đảm an toàn theo quy định mà gây tai nạn giao thông"} |
| e2 | HanhVi | D7/K10/a | {"span": "điều khiển xe chạy quá tốc độ quy định gây tai nạn giao thông"} |
| e3 | HanhVi | D7/K10/a | {"span": "đi vào đường cao tốc, dừng xe, đỗ xe, quay đầu xe, lùi xe, vượt xe, chuyển hướng, chuyển làn đường không đúng quy định gây tai nạn giao thông"} |
| e4 | HanhVi | D7/K10/a | {"span": "không đi đúng phần đường, làn đường, không giữ khoảng cách an toàn giữa hai xe theo quy định gây tai nạn giao thông hoặc đi vào đường có biển báo hiệu có nội dung cấm đi vào đối với loại phương tiện đang điều khiển, đi ngược chiều của đường một chiều, đi ngược chiều trên đường có biển “Cấm đi ngược chiều” gây tai nạn giao thông"} |

- QUY_DINH_HANH_VI: unit:ND168-2024/D7/K10/a → e1
- QUY_DINH_HANH_VI: unit:ND168-2024/D7/K10/a → e2
- QUY_DINH_HANH_VI: unit:ND168-2024/D7/K10/a → e3
- QUY_DINH_HANH_VI: unit:ND168-2024/D7/K10/a → e4
- BI_XU_PHAT: unit:ND168-2024/D7/K10/a → e5
- BI_XU_PHAT: unit:ND168-2024/D7/K10/b → e5
- AP_DUNG_CHO: unit:ND168-2024/D7/K10 → c1
- AP_DUNG_CHO: unit:ND168-2024/D7/K10 → p1
- AP_DUNG_CHO: unit:ND168-2024/D7/K10 → p2
- AP_DUNG_CHO: unit:ND168-2024/D7/K10 → p3
- AP_DUNG_CHO: unit:ND168-2024/D7/K10 → p4

## ND168-2024/D7/K8@2026-11-03 · nd168_che_tai · tier A · ĐÃ DUYỆT

Điều: Xử phạt, trừ điểm giấy phép lái của người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy vi phạm quy tắc giao thông đường bộ

```
[ND168-2024/D7/K8] 8. Phạt tiền từ 6.000.000 đồng đến 8.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
[ND168-2024/D7/K8/a] a) Điều khiển xe chạy quá tốc độ quy định trên 20 km/h;
[ND168-2024/D7/K8/b] b) Điều khiển xe trên đường mà trong máu hoặc hơi thở có nồng độ cồn vượt quá 50 miligam đến 80 miligam/100 mililít máu hoặc vượt quá 0,25 miligam đến 0,4 miligam/1 lít khí thở.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e3 | CheTai | D7/K8 | {"loai": "phat_tien", "min_vnd": 6000000, "max_vnd": 8000000} |
| e4 | PhuongTien | D7/K8 | {"catalog_id": "PT:xe-mo-to"} |
| e5 | PhuongTien | D7/K8 | {"catalog_id": "PT:xe-gan-may"} |
| e6 | PhuongTien | D7/K8 | {"catalog_id": "PT:xe-tuong-tu-xe-mo-to"} |
| e7 | PhuongTien | D7/K8 | {"catalog_id": "PT:xe-tuong-tu-xe-gan-may"} |
| e8 | ChuThe | D7/K8 | {"catalog_id": "CT:nguoi-dieu-khien-xe"} |
| e1 | HanhVi | D7/K8/a | {"span": "Điều khiển xe chạy quá tốc độ quy định trên 20 km/h"} |
| e2 | HanhVi | D7/K8/b | {"span": "Điều khiển xe trên đường mà trong máu hoặc hơi thở có nồng độ cồn vượt quá 50 miligam đến 80 miligam/100 mililít máu hoặc vượt quá 0,25 miligam đến 0,4 miligam/1 lít khí thở"} |

- QUY_DINH_HANH_VI: unit:ND168-2024/D7/K8/a → e1
- QUY_DINH_HANH_VI: unit:ND168-2024/D7/K8/b → e2
- BI_XU_PHAT: unit:ND168-2024/D7/K8/a → e3
- BI_XU_PHAT: unit:ND168-2024/D7/K8/b → e3
- AP_DUNG_CHO: unit:ND168-2024/D7/K8 → e4
- AP_DUNG_CHO: unit:ND168-2024/D7/K8 → e5
- AP_DUNG_CHO: unit:ND168-2024/D7/K8 → e6
- AP_DUNG_CHO: unit:ND168-2024/D7/K8 → e7
- AP_DUNG_CHO: unit:ND168-2024/D7/K8 → e8

## ND168-2024/D20/K9@2026-11-03 · nd168_bo_sung_tru_diem · tier A · ĐÃ DUYỆT

Điều: Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông

```
[ND168-2024/D20/K9] 9. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm quy định tại khoản 7 Điều này bị thu hồi phù hiệu đã hết giá trị sử dụng hoặc phù hiệu không do cơ quan có thẩm quyền cấp.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| c1 | ChuThe | D20/K9 | {"catalog_id": "CT:nguoi-dieu-khien-xe"} |
| p1 | PhuongTien | D20/K9 | {"catalog_id": "PT:xe-o-to-cho-hanh-khach"} |

- AP_DUNG_CHO: unit:ND168-2024/D20/K9 → c1
- AP_DUNG_CHO: unit:ND168-2024/D20/K9 → p1

## ND168-2024/D32/K21@2026-11-03 · nd168_bo_sung_tru_diem · tier A · ĐÃ DUYỆT

Điều: Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ

```
[ND168-2024/D32/K21] 21. Ngoài việc bị áp dụng hình thức xử phạt, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
[ND168-2024/D32/K21/a] a) Thực hiện hành vi quy định tại điểm đ, điểm g, điểm m khoản 7; điểm đ, điểm e khoản 8; điểm b, điểm c, điểm d, điểm đ khoản 9; điểm a, điểm b, điểm đ khoản 11; điểm a khoản 12; điểm c khoản 13; điểm đ, điểm h khoản 14 Điều này trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện còn bị trừ điểm giấy phép lái xe 02 điểm;
[ND168-2024/D32/K21/b] b) Thực hiện hành vi quy định tại điểm e, điểm g khoản 14 Điều này trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện còn bị trừ điểm giấy phép lái xe 03 điểm;
[ND168-2024/D32/K21/c] c) Thực hiện hành vi quy định tại điểm a, điểm b, điểm đ, điểm e khoản 13; điểm a, điểm b, điểm c, điểm d khoản 14; điểm a khoản 16 Điều này trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện còn bị trừ điểm giấy phép lái xe 04 điểm;
[ND168-2024/D32/K21/d] d) Thực hiện hành vi quy định tại khoản 5, khoản 6 Điều này trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện chở vượt trên 50% đến 100% số người quy định được phép chở của phương tiện, còn bị trừ điểm giấy phép lái xe 04 điểm;
[ND168-2024/D32/K21/đ] đ) Thực hiện hành vi quy định tại điểm h khoản 8, điểm b khoản 12 Điều này trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện còn bị trừ điểm giấy phép lái xe 06 điểm;
[ND168-2024/D32/K21/e] e) Thực hiện hành vi quy định tại khoản 15 Điều này trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện còn bị trừ điểm giấy phép lái xe 08 điểm;
[ND168-2024/D32/K21/g] g) Thực hiện hành vi quy định tại điểm d khoản 13, điểm b khoản 16 Điều này trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện còn bị trừ điểm giấy phép lái xe 10 điểm;
[ND168-2024/D32/K21/h] h) Thực hiện hành vi quy định tại khoản 5, khoản 6 Điều này trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện chở vượt trên 100% số người quy định được phép chở của phương tiện còn bị trừ điểm giấy phép lái xe 10 điểm.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| c1 | ChuThe | D32/K21 | {"catalog_id": "CT:chu-phuong-tien"} |
| c2 | ChuThe | D32/K21 | {"catalog_id": "CT:ca-nhan"} |
| c3 | ChuThe | D32/K21 | {"catalog_id": "CT:to-chuc"} |
| d1 | DiemGPLX | D32/K21/a | {"so_diem": 2, "dieu_kien": "trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện"} |
| d2 | DiemGPLX | D32/K21/b | {"so_diem": 3, "dieu_kien": "trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện"} |
| d3 | DiemGPLX | D32/K21/c | {"so_diem": 4, "dieu_kien": "trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện"} |
| d4 | DiemGPLX | D32/K21/d | {"so_diem": 4, "dieu_kien": "trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện chở vượt trên 50% đến 100% số người quy định được phép chở của phương tiện"} |
| d6 | DiemGPLX | D32/K21/e | {"so_diem": 8, "dieu_kien": "trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện"} |
| d7 | DiemGPLX | D32/K21/g | {"so_diem": 10, "dieu_kien": "trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện"} |
| d8 | DiemGPLX | D32/K21/h | {"so_diem": 10, "dieu_kien": "trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện chở vượt trên 100% số người quy định được phép chở của phương tiện"} |
| d5 | DiemGPLX | D32/K21/đ | {"so_diem": 6, "dieu_kien": "trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện"} |

- BI_TRU_DIEM: unit:ND168-2024/D32/K11/a → d1
- BI_TRU_DIEM: unit:ND168-2024/D32/K11/b → d1
- BI_TRU_DIEM: unit:ND168-2024/D32/K11/đ → d1
- BI_TRU_DIEM: unit:ND168-2024/D32/K12/a → d1
- BI_TRU_DIEM: unit:ND168-2024/D32/K12/b → d5
- BI_TRU_DIEM: unit:ND168-2024/D32/K13/a → d3
- BI_TRU_DIEM: unit:ND168-2024/D32/K13/b → d3
- BI_TRU_DIEM: unit:ND168-2024/D32/K13/c → d1
- BI_TRU_DIEM: unit:ND168-2024/D32/K13/d → d7
- BI_TRU_DIEM: unit:ND168-2024/D32/K13/e → d3
- BI_TRU_DIEM: unit:ND168-2024/D32/K13/đ → d3
- BI_TRU_DIEM: unit:ND168-2024/D32/K14/a → d3
- BI_TRU_DIEM: unit:ND168-2024/D32/K14/b → d3
- BI_TRU_DIEM: unit:ND168-2024/D32/K14/c → d3
- BI_TRU_DIEM: unit:ND168-2024/D32/K14/d → d3
- BI_TRU_DIEM: unit:ND168-2024/D32/K14/e → d2
- BI_TRU_DIEM: unit:ND168-2024/D32/K14/g → d2
- BI_TRU_DIEM: unit:ND168-2024/D32/K14/h → d1
- BI_TRU_DIEM: unit:ND168-2024/D32/K14/đ → d1
- BI_TRU_DIEM: unit:ND168-2024/D32/K15 → d6
- BI_TRU_DIEM: unit:ND168-2024/D32/K16/a → d3
- BI_TRU_DIEM: unit:ND168-2024/D32/K16/b → d7
- BI_TRU_DIEM: unit:ND168-2024/D32/K5 → d4
- BI_TRU_DIEM: unit:ND168-2024/D32/K5 → d8
- BI_TRU_DIEM: unit:ND168-2024/D32/K6 → d4
- BI_TRU_DIEM: unit:ND168-2024/D32/K6 → d8
- BI_TRU_DIEM: unit:ND168-2024/D32/K7/g → d1
- BI_TRU_DIEM: unit:ND168-2024/D32/K7/m → d1
- BI_TRU_DIEM: unit:ND168-2024/D32/K7/đ → d1
- BI_TRU_DIEM: unit:ND168-2024/D32/K8/e → d1
- BI_TRU_DIEM: unit:ND168-2024/D32/K8/h → d5
- BI_TRU_DIEM: unit:ND168-2024/D32/K8/đ → d1
- BI_TRU_DIEM: unit:ND168-2024/D32/K9/b → d1
- BI_TRU_DIEM: unit:ND168-2024/D32/K9/c → d1
- BI_TRU_DIEM: unit:ND168-2024/D32/K9/d → d1
- BI_TRU_DIEM: unit:ND168-2024/D32/K9/đ → d1
- AP_DUNG_CHO: unit:ND168-2024/D32/K21 → c1
- AP_DUNG_CHO: unit:ND168-2024/D32/K21 → c2
- AP_DUNG_CHO: unit:ND168-2024/D32/K21 → c3

## ND168-2024/D38/K4@2026-11-03 · nd168_bo_sung_tru_diem · tier A · ĐÃ DUYỆT

Điều: Xử phạt người điều khiển phương tiện đăng ký hoạt động trong Khu kinh tế thương mại đặc biệt, Khu kinh tế cửa khẩu quốc tế

```
[ND168-2024/D38/K4] 4. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm quy định tại khoản 1, khoản 2 Điều này còn bị áp dụng biện pháp khắc phục hậu quả buộc đưa phương tiện quay trở lại Khu kinh tế thương mại đặc biệt, Khu kinh tế cửa khẩu quốc tế.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| b1 | BienPhapBoSung | D38/K4 | {"ten": "buộc đưa phương tiện quay trở lại Khu kinh tế thương mại đặc biệt, Khu kinh tế cửa khẩu quốc tế"} |
| c1 | ChuThe | D38/K4 | {"catalog_id": "CT:nguoi-dieu-khien-xe"} |

- BI_XU_PHAT: unit:ND168-2024/D38/K1/a → b1
- BI_XU_PHAT: unit:ND168-2024/D38/K1/b → b1
- BI_XU_PHAT: unit:ND168-2024/D38/K2/a → b1
- BI_XU_PHAT: unit:ND168-2024/D38/K2/b → b1
- AP_DUNG_CHO: unit:ND168-2024/D38/K4 → c1

## ND168-2024/D38/K5@2026-11-03 · nd168_bo_sung_tru_diem · tier A · ĐÃ DUYỆT

Điều: Xử phạt người điều khiển phương tiện đăng ký hoạt động trong Khu kinh tế thương mại đặc biệt, Khu kinh tế cửa khẩu quốc tế

```
[ND168-2024/D38/K5] 5. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm b khoản 1, điểm b khoản 2 Điều này bị thu hồi phù hiệu đã hết giá trị sử dụng hoặc phù hiệu không do cơ quan có thẩm quyền cấp.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| c1 | ChuThe | D38/K5 | {"catalog_id": "CT:nguoi-dieu-khien-xe"} |

- AP_DUNG_CHO: unit:ND168-2024/D38/K5 → c1

## LUAT35-2024/D2/K1@2026-11-03 · dinh_nghia_luat · tier A · ĐÃ DUYỆT

Điều: Giải thích từ ngữ

```
[LUAT35-2024/D2/K1] 1. Hoạt động đường bộ bao gồm: hoạt động về quy hoạch, đầu tư, xây dựng, quản lý, sử dụng, vận hành, khai thác, bảo trì, bảo vệ kết cấu hạ tầng đường bộ; vận tải đường bộ.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| k1 | KhaiNiem | D2/K1 | {"ten": "Hoạt động đường bộ"} |

- DINH_NGHIA: unit:LUAT35-2024/D2/K1 → k1

## LUAT35-2024/D2/K6@2026-11-03 · dinh_nghia_luat · tier A · ĐÃ DUYỆT

Điều: Giải thích từ ngữ

```
[LUAT35-2024/D2/K6] 6. Cơ quan quản lý đường bộ là cơ quan thuộc Bộ Giao thông vận tải giúp Bộ trưởng Bộ Giao thông vận tải thực hiện chức năng quản lý nhà nước về hoạt động đường bộ; cơ quan chuyên môn thuộc Ủy ban nhân dân cấp tỉnh; cơ quan chuyên môn thuộc Ủy ban nhân dân cấp huyện; Ủy ban nhân dân cấp xã.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e1 | KhaiNiem | D2/K6 | {"ten": "Cơ quan quản lý đường bộ"} |

- DINH_NGHIA: unit:LUAT35-2024/D2/K6 → e1

Bản nháp bị bỏ 1 mục:
- loai_khong_hop_le: {"type": "DINH_NGHI", "src": "unit:LUAT35-2024/D2/K6", "dst": "e1"}

## LUAT35-2024/D2/K5@2026-11-03 · dinh_nghia_luat · tier A · ĐÃ DUYỆT

Điều: Giải thích từ ngữ

```
[LUAT35-2024/D2/K5] 5. Hành lang an toàn đường bộ là dải đất dọc hai bên đất của đường bộ, tính từ mép ngoài phần đất để bảo vệ, bảo trì đường bộ ra hai bên để bảo đảm an toàn giao thông đường bộ, bảo đảm tầm nhìn xe chạy và hạn chế ảnh hưởng đến môi trường xung quanh.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e1 | KhaiNiem | D2/K5 | {"ten": "Hành lang an toàn đường bộ"} |

- DINH_NGHIA: unit:LUAT35-2024/D2/K5 → e1

Bản nháp bị bỏ 1 mục:
- loai_khong_hop_le: {"type": "DINH_NGhia", "src": "unit:LUAT35-2024/D2/K5", "dst": "e1"}

## LUAT35-2024/D2/K7@2026-11-03 · dinh_nghia_luat · tier A · ĐÃ DUYỆT

Điều: Giải thích từ ngữ

```
[LUAT35-2024/D2/K7] 7. Người quản lý, sử dụng đường bộ là chủ sở hữu trực tiếp quản lý, sử dụng, vận hành, khai thác công trình đường bộ hoặc tổ chức, cá nhân được giao quản lý, sử dụng, vận hành, khai thác công trình đường bộ.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e1 | KhaiNiem | D2/K7 | {"ten": "Người quản lý, sử dụng đường bộ"} |

- DINH_NGHIA: unit:LUAT35-2024/D2/K7 → e1

Bản nháp bị bỏ 1 mục:
- loai_khong_hop_le: {"type": "DINH_NGHI", "src": "unit:LUAT35-2024/D2/K7", "dst": "e1"}

## LUAT36-2024/D2/K3@2026-11-03 · dinh_nghia_luat · tier A · ĐÃ DUYỆT

Điều: Giải thích từ ngữ

```
[LUAT36-2024/D2/K3] 3. Phương tiện tham gia giao thông đường bộ là phương tiện giao thông đường bộ tham gia giao thông trên đường bộ.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e1 | KhaiNiem | D2/K3 | {"ten": "Phương tiện tham gia giao thông đường bộ"} |

- DINH_NGHIA: unit:LUAT36-2024/D2/K3 → e1

Bản nháp bị bỏ 1 mục:
- loai_khong_hop_le: {"type": "DINH_NGHI", "src": "unit:LUAT36-2024/D2/K3", "dst": "e1"}

## LUAT36-2024/D2/K5@2026-11-03 · dinh_nghia_luat · tier A · ĐÃ DUYỆT

Điều: Giải thích từ ngữ

```
[LUAT36-2024/D2/K5] 5. Phần đường xe chạy là phần của đường bộ được sử dụng cho phương tiện giao thông đường bộ đi lại.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e1 | KhaiNiem | D2/K5 | {"ten": "Phần đường xe chạy"} |

- DINH_NGHIA: unit:LUAT36-2024/D2/K5 → e1

Bản nháp bị bỏ 1 mục:
- loai_khong_hop_le: {"type": "DINH_NGHI", "src": "unit:LUAT36-2024/D2/K5", "dst": "e1"}

## LUAT36-2024/D2/K12@2026-11-03 · dinh_nghia_luat · tier A · ĐÃ DUYỆT

Điều: Giải thích từ ngữ

```
[LUAT36-2024/D2/K12] 12. Tai nạn giao thông đường bộ là va chạm liên quan đến người, phương tiện khi tham gia giao thông đường bộ, xảy ra ngoài ý muốn của người tham gia giao thông đường bộ, gây thiệt hại đến tính mạng, sức khỏe, tài sản của cá nhân hoặc tài sản của cơ quan, tổ chức.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e1 | KhaiNiem | D2/K12 | {"ten": "Tai nạn giao thông đường bộ"} |

- DINH_NGHIA: unit:LUAT36-2024/D2/K12 → e1

Bản nháp bị bỏ 1 mục:
- loai_khong_hop_le: {"type": "DINH_NGHI", "src": "unit:LUAT36-2024/D2/K12", "dst": "e1"}

## LUAT36-2024/D2/K13@2026-11-03 · dinh_nghia_luat · tier A · ĐÃ DUYỆT

Điều: Giải thích từ ngữ

```
[LUAT36-2024/D2/K13] 13. Thiết bị an toàn cho trẻ em là thiết bị có đủ khả năng bảo đảm an toàn cho trẻ em ở tư thế ngồi hoặc nằm trên xe ô tô, được thiết kế để giảm nguy cơ chấn thương cho người dùng trong trường hợp xảy ra va chạm hoặc xe ô tô giảm tốc độ đột ngột, bằng cách hạn chế sự di chuyển của cơ thể trẻ em.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e1 | KhaiNiem | D2/K13 | {"ten": "Thiết bị an toàn cho trẻ em"} |

- DINH_NGHIA: unit:LUAT36-2024/D2/K13 → e1

Bản nháp bị bỏ 1 mục:
- loai_khong_hop_le: {"type": "DINH_NGHI", "src": "unit:LUAT36-2024/D2/K13", "dst": "e1"}

## TT14-2025-BXD/D23/K3@2026-11-03 · tt_tier_a · tier A · ĐÃ DUYỆT

Điều: Cấp lại chứng chỉ

```
[TT14-2025-BXD/D23/K3] 3. Trình tự thực hiện:
[TT14-2025-BXD/D23/K3/a] a) Cá nhân nộp 01 bộ hồ sơ đến cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ đã cấp chứng chỉ; trường hợp cơ sở bồi dưỡng đã cấp chứng chỉ không còn hoạt động thì cá nhân nộp cho Sở Xây dựng nơi quản lý cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ đã cấp chứng chỉ tại Trung tâm Phục vụ hành chính công cấp tỉnh hoặc cấp xã bằng hình thức trực tiếp hoặc qua dịch vụ bưu chính hoặc qua cổng dịch vụ công quốc gia.
[TT14-2025-BXD/D23/K3/b] b) Cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ hoặc Sở Xây dựng kiểm tra hồ sơ khi tiếp nhận; trường hợp chứng chỉ không thuộc đối tượng được cấp lại hoặc hồ sơ không đúng theo quy định, phải thông báo trực tiếp hoặc bằng văn bản những nội dung cần bổ sung hoặc sửa đổi cho cá nhân trong thời hạn 02 ngày làm việc, kể từ ngày nhận hồ sơ;
[TT14-2025-BXD/D23/K3/c] c) Trong thời hạn 02 ngày làm việc, kể từ ngày nhận đủ hồ sơ hợp lệ, người đứng đầu cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ hoặc Sở Xây dựng cấp lại chứng chỉ; trường hợp không cấp lại chứng chỉ thì phải trả lời bằng văn bản và nêu rõ lý do;
[TT14-2025-BXD/D23/K3/d] d) Việc trả chứng chỉ bản giấy được thực hiện tại cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ; trường hợp trả bản điện tử thì đăng tải trên Hệ thống thông tin chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ tại cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ. Trường hợp do Sở Xây dựng cấp thì trả bản điện tử bằng một trong các hình thức: qua Cổng Dịch vụ công quốc gia hoặc Hệ thống thông tin giải quyết thủ tục hành chính cấp tỉnh hoặc cấp xã; trường hợp cá nhân có nhu cầu nhận bản giấy thì được cấp bổ sung.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| c1 | ChuThe | D23/K3 | {"catalog_id": "CT:ca-nhan"} |

- AP_DUNG_CHO: unit:TT14-2025-BXD/D23/K3 → c1

## LUAT36-2024/D2/K11@2026-11-03 · dinh_nghia_luat · tier A · ĐÃ DUYỆT

Điều: Giải thích từ ngữ

```
[LUAT36-2024/D2/K11] 11. Ùn tắc giao thông đường bộ (sau đây gọi là ùn tắc giao thông) là tình trạng người, phương tiện tham gia giao thông đường bộ bị dồn ứ, di chuyển với tốc độ rất chậm hoặc không thể di chuyển được.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e1 | KhaiNiem | D2/K11 | {"ten": "Ùn tắc giao thông đường bộ"} |

- DINH_NGHIA: unit:LUAT36-2024/D2/K11 → e1

Bản nháp bị bỏ 1 mục:
- loai_khong_hop_le: {"type": "DINH_NGHI", "src": "unit:LUAT36-2024/D2/K11", "dst": "e1"}

## LUAT36-2024/D2/K4@2026-11-03 · dinh_nghia_luat · tier A · ĐÃ DUYỆT

Điều: Giải thích từ ngữ

```
[LUAT36-2024/D2/K4] 4. Đường ưu tiên là đường mà trên đó phương tiện tham gia giao thông đường bộ được các phương tiện tham gia giao thông đường bộ đến từ hướng khác nhường đường khi qua nơi đường giao nhau, được cắm biển báo hiệu đường ưu tiên.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e1 | KhaiNiem | D2/K4 | {"ten": "Đường ưu tiên"} |

- DINH_NGHIA: unit:LUAT36-2024/D2/K4 → e1

Bản nháp bị bỏ 1 mục:
- loai_khong_hop_le: {"type": "DINH_NGHI", "src": "unit:LUAT36-2024/D2/K4", "dst": "e1"}

## TT14-2025-BXD/D30/K2@2026-11-03 · tt_tier_a · tier A · ĐÃ DUYỆT

Điều: Cơ sở đào tạo lái xe

```
[TT14-2025-BXD/D30/K2] 2. Đối với công tác quản lý hệ thống thông tin:
[TT14-2025-BXD/D30/K2/a] a) Đầu tư, bảo trì, nâng cấp Hệ thống thông tin quản lý, giám sát đào tạo lái xe tại cơ sở đào tạo lái xe; tiếp nhận, tổ chức thực hiện phần mềm ứng dụng phục vụ công tác quản lý, giám sát đào tạo lái xe tại cơ sở đào tạo lái xe do Cục Đường bộ Việt Nam chuyển giao và thực hiện truyền đầy đủ dữ liệu quy định tại các điểm a, điểm b, điểm g và điểm h khoản 1 Điều 25 về Sở Xây dựng;
[TT14-2025-BXD/D30/K2/b] b) Vận hành Hệ thống thông tin quản lý, giám sát đào tạo lái xe tại cơ sở đào tạo lái xe theo quy định;
[TT14-2025-BXD/D30/K2/c] c) Tạo lập, đối chiếu, chịu trách nhiệm về tính chính xác của thông tin học viên, quá trình đào tạo, kết quả đào tạo, báo cáo đăng ký khóa đào tạo lái xe theo quy định;
[TT14-2025-BXD/D30/K2/d] d) Lưu trữ đầy đủ các thông tin theo quy định tại khoản 1 Điều 27 Thông tư này và quy định của pháp luật về lưu trữ;
[TT14-2025-BXD/D30/K2/đ] đ) Ban hành quy chế vận hành và bảo đảm an toàn, an ninh thông tin; quy chế sử dụng tài khoản và khai thác dữ liệu đối với hệ thống thông tin của cơ sở đào tạo và các hệ thống thông tin được chia sẻ theo các quy định của pháp luật về công nghệ thông tin và an toàn thông tin mạng;
[TT14-2025-BXD/D30/K2/e] e) Cung cấp dữ liệu trên Hệ thống thông tin quản lý, giám sát đào tạo lái xe tại cơ sở đào tạo lái xe để phục vụ công tác thanh tra, kiểm tra và cung cấp thông tin cho các cơ quan chức năng khi có yêu cầu.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| c1 | ChuThe | D30/K2 | {"catalog_id": "CT:co-so-dao-tao-lai-xe"} |
| h1 | HanhVi | D30/K2/a | {"ten": "đầu tư, bảo trì, nâng cấp hệ thống thông tin quản lý, giám sát đào tạo lái xe", "span": "Đầu tư, bảo trì, nâng cấp Hệ thống thông tin quản lý, giám sát đào tạo lái xe tại cơ sở đào tạo lái xe"} |
| h2 | HanhVi | D30/K2/a | {"ten": "tiếp nhận phần mềm và truyền đầy đủ dữ liệu về Sở Xây dựng", "span": "tiếp nhận, tổ chức thực hiện phần mềm ứng dụng phục vụ công tác quản lý, giám sát đào tạo lái xe tại cơ sở đào tạo lái xe do Cục Đường bộ Việt Nam chuyển giao và thực hiện truyền đầy đủ dữ liệu quy định tại các điểm a, điểm b, điểm g và điểm h khoản 1 Điều 25 về Sở Xây dựng"} |
| h3 | HanhVi | D30/K2/b | {"ten": "vận hành hệ thống thông tin quản lý, giám sát đào tạo lái xe", "span": "Vận hành Hệ thống thông tin quản lý, giám sát đào tạo lái xe tại cơ sở đào tạo lái xe theo quy định"} |
| h4 | HanhVi | D30/K2/c | {"ten": "tạo lập, đối chiếu, chịu trách nhiệm về thông tin học viên, đào tạo", "span": "Tạo lập, đối chiếu, chịu trách nhiệm về tính chính xác của thông tin học viên, quá trình đào tạo, kết quả đào tạo, báo cáo đăng ký khóa đào tạo lái xe theo quy định"} |
| h5 | HanhVi | D30/K2/d | {"ten": "lưu trữ đầy đủ thông tin theo quy định", "span": "Lưu trữ đầy đủ các thông tin theo quy định tại khoản 1 Điều 27 Thông tư này và quy định của pháp luật về lưu trữ"} |
| h7 | HanhVi | D30/K2/e | {"ten": "cung cấp dữ liệu phục vụ thanh tra, kiểm tra", "span": "Cung cấp dữ liệu trên Hệ thống thông tin quản lý, giám sát đào tạo lái xe tại cơ sở đào tạo lái xe để phục vụ công tác thanh tra, kiểm tra và cung cấp thông tin cho các cơ quan chức năng khi có yêu cầu"} |
| h6 | HanhVi | D30/K2/đ | {"ten": "ban hành quy chế vận hành, bảo đảm an toàn thông tin và quy chế sử dụng tài khoản", "span": "Ban hành quy chế vận hành và bảo đảm an toàn, an ninh thông tin; quy chế sử dụng tài khoản và khai thác dữ liệu đối với hệ thống thông tin của cơ sở đào tạo và các hệ thống thông tin được chia sẻ theo các quy định của pháp luật về công nghệ thông tin và an toàn thông tin mạng"} |

- QUY_DINH_HANH_VI: unit:TT14-2025-BXD/D30/K2/a → h1
- QUY_DINH_HANH_VI: unit:TT14-2025-BXD/D30/K2/a → h2
- QUY_DINH_HANH_VI: unit:TT14-2025-BXD/D30/K2/b → h3
- QUY_DINH_HANH_VI: unit:TT14-2025-BXD/D30/K2/c → h4
- QUY_DINH_HANH_VI: unit:TT14-2025-BXD/D30/K2/d → h5
- QUY_DINH_HANH_VI: unit:TT14-2025-BXD/D30/K2/e → h7
- QUY_DINH_HANH_VI: unit:TT14-2025-BXD/D30/K2/đ → h6
- AP_DUNG_CHO: unit:TT14-2025-BXD/D30/K2 → c1

## TT14-2025-BXD/D8/K1@2026-11-03 · tt_tier_a · tier A · ĐÃ DUYỆT

Điều: Tiêu chuẩn của cơ sở đào tạo lái xe mô tô

```
[TT14-2025-BXD/D8/K1] 1. Hệ thống phòng học chuyên môn:
[TT14-2025-BXD/D8/K1/a] a) Phòng học lý thuyết: có các trang thiết bị làm công cụ hỗ trợ việc giảng dạy về nội dung pháp luật giao thông đường bộ, trường hợp các thiết bị công nghệ thông tin chưa mô tả hệ thống báo hiệu đường bộ, sa hình, thì phải có hệ thống tranh vẽ;
[TT14-2025-BXD/D8/K1/b] b) Phòng học kỹ thuật lái xe: có các thiết bị công nghệ thông tin làm công cụ hỗ trợ việc giảng dạy về cấu tạo; trường hợp các thiết bị công nghệ thông tin chưa mô tả thì phải có hệ thống tranh vẽ;
[TT14-2025-BXD/D8/K1/c] c) Phòng học thực tập bảo dưỡng sửa chữa hạng B1: có hệ thống thông gió và chiếu sáng bảo đảm các yêu cầu về an toàn, vệ sinh lao động; nền nhà không gây bụi; có trang bị đồ nghề chuyên dùng để bảo dưỡng sửa chữa; có bàn tháo lắp, bảng, bàn ghế cho giảng dạy, thực tập; có trang bị đồ nghề chuyên dùng để hướng dẫn học viên thực hành tháo lắp lốp, kiểm tra dầu xe;
[TT14-2025-BXD/D8/K1/d] d) Trường hợp cơ sở đào tạo lái xe mô tô đồng thời là cơ sở đào tạo lái xe ô tô thì được phép sử dụng chung các phòng học chuyên môn.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| c1 | ChuThe | D8/K1 | {"catalog_id": "CT:co-so-dao-tao-lai-xe"} |
| p1 | PhuongTien | D8/K1 | {"catalog_id": "PT:xe-mo-to"} |

- AP_DUNG_CHO: unit:TT14-2025-BXD/D8/K1 → c1
- AP_DUNG_CHO: unit:TT14-2025-BXD/D8/K1 → p1

## TT65-2024-BCA/D2/K4@2026-11-03 · tt_tier_a · tier A · ĐÃ DUYỆT

Điều: Đối tượng áp dụng

```
[TT65-2024-BCA/D2/K4] 4. Cơ quan, tổ chức, cá nhân có liên quan đến kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| c1 | ChuThe | D2/K4 | {"catalog_id": "CT:to-chuc"} |
| c2 | ChuThe | D2/K4 | {"catalog_id": "CT:ca-nhan"} |

- AP_DUNG_CHO: unit:TT65-2024-BCA/D2/K4 → c1
- AP_DUNG_CHO: unit:TT65-2024-BCA/D2/K4 → c2

## TT79-2024-BCA/D30/K3@2026-11-03 · tt_tier_a · tier A · ĐÃ DUYỆT

Điều: Quản lý biển số xe trúng đấu giá, sau khi đăng ký xe

```
[TT79-2024-BCA/D30/K3] 3. Trong quá trình sử dụng, nếu chứng nhận đăng ký xe, biển số xe bị hỏng, bị mất; cải tạo xe; thay đổi màu sơn hoặc có nhu cầu đổi chứng nhận đăng ký xe khi thay đổi địa chỉ thì chủ xe làm thủ tục đổi, cấp lại theo quy định.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| c1 | ChuThe | D30/K3 | {"catalog_id": "CT:chu-xe"} |
| h1 | HanhVi | D30/K3 | {"ten": "chủ xe làm thủ tục đổi, cấp lại chứng nhận đăng ký, biển số", "span": "làm thủ tục đổi, cấp lại theo quy định", "dieu_kien": "nếu chứng nhận đăng ký xe, biển số xe bị hỏng, bị mất; cải tạo xe; thay đổi màu sơn hoặc có nhu cầu đổi chứng nhận đăng ký xe khi thay đổi địa chỉ"} |

- QUY_DINH_HANH_VI: unit:TT79-2024-BCA/D30/K3 → h1
- AP_DUNG_CHO: unit:TT79-2024-BCA/D30/K3 → c1

## TT79-2024-BCA/D32/K2@2026-11-03 · tt_tier_a · tier A · ĐÃ DUYỆT

Điều: Giải quyết đăng ký sang tên xe đối với xe đã chuyển quyền sở hữu qua nhiều tổ chức, cá nhân

```
[TT79-2024-BCA/D32/K2] 2. Hồ sơ thu hồi: Thực hiện hồ sơ theo quy định tại khoản 1 Điều 16 Thông tư này.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |


## TT79-2024-BCA/D39/K1@2026-11-03 · tt_tier_a · tier A · ĐÃ DUYỆT

Điều: Điều khoản chuyển tiếp

```
[TT79-2024-BCA/D39/K1] 1. Đối với xe đã đăng ký biển 5 số trước ngày Thông tư này có hiệu lực thi hành mà chưa làm thủ tục thu hồi thì số biển số đó được xác định là biển số định danh của chủ xe, trừ biển số xe có ký hiệu “MK”, “TĐ”, “LD”, “DA”, “MĐ”, “R”, “CT”, “LB”, “CD”.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |


## ND336-2025/D11/K1@2026-11-03 · nd336 · tier B · ĐÃ DUYỆT

Điều: Xử phạt người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ kinh doanh vận tải vi phạm quy định về vận tải đường bộ

```
[ND336-2025/D11/K1] 1. Phạt tiền từ 300.000 đồng đến 500.000 đồng đối với hành vi vi phạm không mặc đồng phục, không đeo thẻ tên của lái xe theo đúng mẫu đơn vị kinh doanh vận tải đã quy định.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| c1 | ChuThe | D11/K1 | {"catalog_id": "CT:nguoi-dieu-khien-xe"} |
| e1 | HanhVi | D11/K1 | {"ten": "không mặc đồng phục, không đeo thẻ tên lái xe", "span": "không mặc đồng phục, không đeo thẻ tên của lái xe theo đúng mẫu đơn vị kinh doanh vận tải đã quy định"} |
| e2 | CheTai | D11/K1 | {"loai": "phat_tien", "min_vnd": 300000, "max_vnd": 500000} |
| e3 | PhuongTien | D11/K1 | {"catalog_id": "PT:xe-o-to-kinh-doanh-van-tai"} |
| p2 | PhuongTien | D11/K1 | {"catalog_id": "PT:xe-cho-nguoi-bon-banh-co-gan-dong-co"} |

- QUY_DINH_HANH_VI: unit:ND336-2025/D11/K1 → e1
- BI_XU_PHAT: unit:ND336-2025/D11/K1 → e2
- AP_DUNG_CHO: unit:ND336-2025/D11/K1 → c1
- AP_DUNG_CHO: unit:ND336-2025/D11/K1 → e3
- AP_DUNG_CHO: unit:ND336-2025/D11/K1 → p2

Bản nháp bị bỏ 2 mục:
- ngoai_danh_muc: {"id": "e4", "type": "ChuThe", "unit_id": "ND336-2025/D11/K1", "ten": null, "span": null, "dieu_kien": null, "catalog_id": "CT:lai-xe", "loai": null, "min_vnd": null, "max_vnd": null, "min_thang": nul
- dich_khong_hop_le: {"type": "AP_DUNG_CHO", "src": "unit:ND336-2025/D11/K1", "dst": "e4"}

## ND336-2025/D20/K1@2026-11-03 · tier_b · tier B · ĐÃ DUYỆT

Điều: Nguyên tắc xác định thẩm quyền xử phạt vi phạm hành chính và áp dụng biện pháp khắc phục hậu quả

```
[ND336-2025/D20/K1] 1. Nguyên tắc xác định thẩm quyền xử phạt vi phạm hành chính và áp dụng biện pháp khắc phục hậu quả trong hoạt động đường bộ thực hiện theo quy định tại Điều 52 của Luật Xử lý vi phạm hành chính, Điều 4 Nghị định số 189/2025/NĐ-CP ngày 01 tháng 7 năm 2025 của Chính phủ quy định chi tiết luật xử lý vi phạm hành chính về thẩm quyền xử phạt vi phạm hành chính.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |


## ND336-2025/D22/K5@2026-11-03 · tier_b · tier B · ĐÃ DUYỆT

Điều: Thủ tục xử phạt, thi hành quyết định xử phạt và biện pháp khắc phục hậu quả

```
[ND336-2025/D22/K5] 5. Trong trường hợp áp dụng biện pháp khắc phục hậu quả buộc nộp lại số lợi bất hợp pháp thì việc xác định số lợi bất hợp pháp được thực hiện như sau:
[ND336-2025/D22/K5/a] a) Số lợi bất hợp pháp do thực hiện hành vi vi phạm hành chính quy định tại điểm c khoản 2 Điều 10 được tính bằng số tiền thu được từ việc nhận tiền mặt của người sử dụng phương tiện giao thông đường bộ;
[ND336-2025/D22/K5/b] b) Số lợi bất hợp pháp có được do thực hiện hành vi vi phạm hành chính quy định tại điểm b khoản 3, điểm c khoản 4 Điều 10 được tính bằng số tiền thu được từ việc thu tiền sử dụng đường bộ trừ đi số tiền theo mức giá đã được cơ quan thẩm quyền chấp thuận bằng văn bản;
[ND336-2025/D22/K5/c] c) Số lợi bất hợp pháp có được do thực hiện hành vi vi phạm hành chính quy định tại điểm d khoản 2 Điều 11, khoản 2 và khoản 3 Điều 13 được tính bằng số tiền thu được từ việc thu tiền vé của hành khách trừ đi giá vé đã được kê khai, niêm yết;
[ND336-2025/D22/K5/d] d) Số lợi bất hợp pháp có được do thực hiện hành vi vi phạm hành chính quy định tại điểm a khoản 2 Điều 12 được tính bằng số tiền thu được của hành khách từ việc bán vé cho hành khách từ chối chuyến đi;
[ND336-2025/D22/K5/đ] đ) Số lợi bất hợp pháp có được do thực hiện hành vi vi phạm hành chính quy định tại điểm g khoản 4 Điều 12 được tính bằng số tiền đã thu của đơn vị kinh doanh vận tải trừ đi số tiền theo giá dịch vụ xe ra, vào bến đã kê khai, công bố;
[ND336-2025/D22/K5/e] e) Số lợi bất hợp pháp có được do thực hiện hành vi vi phạm hành chính quy định tại điểm h khoản 4 Điều 12 được tính bằng số tiền thu của hành khách trừ đi giá vé vận tải hành khách tuyến cố định, giá dịch vụ vận tải hành khách bằng taxi đã kê khai, công bố;
[ND336-2025/D22/K5/g] g) Số lợi bất hợp pháp có được do thực hiện hành vi vi phạm hành chính quy định tại điểm i khoản 4 Điều 12 được tính bằng số tiền phải mua bảo hiểm cho hành khách theo quy định mà đơn vị kinh doanh vận tải đã không mua.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |


## ND336-2025/D7/K3@2026-11-03 · nd336 · tier B · ĐÃ DUYỆT

Điều: Xử phạt hành vi vi phạm quy định về đào tạo thẩm tra viên, điều kiện kinh doanh dịch vụ thẩm tra an toàn giao thông đường bộ

```
[ND336-2025/D7/K3] 3. Phạt tiền từ 20.000.000 đồng đến 30.000.000 đồng đối với tổ chức kinh doanh dịch vụ thẩm tra an toàn giao thông đường bộ thực hiện một trong các hành vi vi phạm sau đây:
[ND336-2025/D7/K3/a] a) Không độc lập với đơn vị thi công, tổ chức tư vấn thiết kế theo quy định;
[ND336-2025/D7/K3/b] b) Sử dụng người không có chứng chỉ thẩm tra viên an toàn giao thông đường bộ hoặc có chứng chỉ nhưng không còn giá trị sử dụng để thẩm tra an toàn giao thông đường bộ;
[ND336-2025/D7/K3/c] c) Không đáp ứng điều kiện về năng lực khi thẩm tra đối với dự án nhóm C, công trình đường bộ đang khai thác theo quy định.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| c1 | ChuThe | D7/K3 | {"catalog_id": "CT:to-chuc"} |
| e4 | CheTai | D7/K3 | {"loai": "phat_tien", "min_vnd": 20000000, "max_vnd": 30000000} |
| e1 | HanhVi | D7/K3/a | {"span": "Không độc lập với đơn vị thi công, tổ chức tư vấn thiết kế theo quy định"} |
| e2 | HanhVi | D7/K3/b | {"span": "Sử dụng người không có chứng chỉ thẩm tra viên an toàn giao thông đường bộ hoặc có chứng chỉ nhưng không còn giá trị sử dụng để thẩm tra an toàn giao thông đường bộ"} |
| e3 | HanhVi | D7/K3/c | {"span": "Không đáp ứng điều kiện về năng lực khi thẩm tra đối với dự án nhóm C, công trình đường bộ đang khai thác theo quy định"} |

- QUY_DINH_HANH_VI: unit:ND336-2025/D7/K3/a → e1
- QUY_DINH_HANH_VI: unit:ND336-2025/D7/K3/b → e2
- QUY_DINH_HANH_VI: unit:ND336-2025/D7/K3/c → e3
- BI_XU_PHAT: unit:ND336-2025/D7/K3/a → e4
- BI_XU_PHAT: unit:ND336-2025/D7/K3/b → e4
- BI_XU_PHAT: unit:ND336-2025/D7/K3/c → e4
- AP_DUNG_CHO: unit:ND336-2025/D7/K3 → c1

Bản nháp bị bỏ 2 mục:
- ngoai_danh_muc: {"id": "e5", "type": "ChuThe", "unit_id": "ND336-2025/D7/K3", "ten": null, "span": null, "dieu_kien": null, "catalog_id": "CT:to-chuc-kinh-doanh-dich-vu-tham-tra-an-toan-giao-thong-duong-bo", "loai": 
- dich_khong_hop_le: {"type": "AP_DUNG_CHO", "src": "unit:ND336-2025/D7/K3", "dst": "e5"}

## ND336-2025/D6/K1@2026-11-03 · tier_b · tier B · ĐÃ DUYỆT

Điều: Xử phạt hành vi vi phạm quy định về quản lý, vận hành, khai thác, bảo trì công trình hạ tầng kỹ thuật sử dụng chung với đường bộ

```
[ND336-2025/D6/K1] 1. Phạt tiền từ 6.000.000 đồng đến 10.000.000 đồng đối với cá nhân, từ 12.000.000 đồng đến 20.000.000 đồng đối với tổ chức thực hiện hành vi vi phạm không bố trí dấu hiệu nhận biết công trình hạ tầng thuộc sở hữu khi lắp đặt vào công trình hạ tầng kỹ thuật sử dụng chung với đường bộ.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| c1 | CheTai | D6/K1 | {"loai": "phat_tien", "min_vnd": 6000000, "max_vnd": 10000000} |
| c2 | CheTai | D6/K1 | {"loai": "phat_tien", "min_vnd": 12000000, "max_vnd": 20000000} |
| e1 | HanhVi | D6/K1 | {"span": "không bố trí dấu hiệu nhận biết công trình hạ tầng thuộc sở hữu khi lắp đặt vào công trình hạ tầng kỹ thuật sử dụng chung với đường bộ"} |
| t1 | ChuThe | D6/K1 | {"catalog_id": "CT:ca-nhan"} |
| t2 | ChuThe | D6/K1 | {"catalog_id": "CT:to-chuc"} |

- QUY_DINH_HANH_VI: unit:ND336-2025/D6/K1 → e1
- BI_XU_PHAT: unit:ND336-2025/D6/K1 → c1
- BI_XU_PHAT: unit:ND336-2025/D6/K1 → c2
- AP_DUNG_CHO: unit:ND336-2025/D6/K1 → t1
- AP_DUNG_CHO: unit:ND336-2025/D6/K1 → t2

Bản nháp bị bỏ 1 mục:
- dich_khong_hop_le: {"type": "BI_XU_PHAT", "src": "unit:ND336-2025/D6/K1", "dst": "e1"}

## ND336-2025/D12/K7@2026-11-03 · nd336 · tier B · ĐÃ DUYỆT

Điều: Xử phạt các hành vi vi phạm quy định về vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ

```
[ND336-2025/D12/K7] 7. Phạt tiền từ 30.000.000 đồng đến 50.000.000 đồng đối với đơn vị cung cấp phần mềm ứng dụng hỗ trợ kết nối vận tải thực hiện một trong các hành vi vi phạm sau đây:
[ND336-2025/D12/K7/a] a) Đơn vị cung cấp phần mềm hỗ trợ kết nối vận tải không thực hiện đúng quy định về cung cấp phần mềm ứng dụng hỗ trợ kết nối vận tải, trừ hành vi vi phạm tại điểm e khoản này;
[ND336-2025/D12/K7/b] b) Đơn vị cung cấp phần mềm hỗ trợ kết nối vận tải không cung cấp cho cơ quan quản lý danh sách các đơn vị kinh doanh vận tải, xe ô tô và lái xe của các đơn vị vận tải hợp tác với đơn vị cung cấp phần mềm ứng dụng hỗ trợ kết nối vận tải hoặc không cung cấp tài khoản truy cập vào phần mềm ứng dụng hỗ trợ kết nối vận tải cho cơ quan quản lý khi có yêu cầu hoặc không thực hiện lưu trữ theo quy định;
[ND336-2025/D12/K7/c] c) Tự ý điều chỉnh giá cước vận tải đã niêm yết hoặc giá trị hợp đồng đã ký kết trên phần mềm;
[ND336-2025/D12/K7/d] d) Cho phép đơn vị kinh doanh vận tải hành khách theo hợp đồng sử dụng phần mềm để xác nhận đặt chỗ cho từng hành khách đi xe, bán vé hoặc thu tiền đối với từng hành khách trái quy định;
[ND336-2025/D12/K7/đ] đ) Không cung cấp cho đơn vị kinh doanh vận tải giao diện và công cụ để thực hiện được việc trực tiếp điều hành phương tiện và lái xe, đàm phán, quyết định giá cước vận tải với hành khách và người thuê vận tải trên phần mềm;
[ND336-2025/D12/K7/e] e) Phần mềm ứng dụng hỗ trợ kết nối vận tải để lái xe phải thực hiện nhiều thao tác nhận chuyến xe khi xe đang di chuyển.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e7 | CheTai | D12/K7 | {"loai": "phat_tien", "min_vnd": 30000000, "max_vnd": 50000000} |
| e1 | HanhVi | D12/K7/a | {"span": "Đơn vị cung cấp phần mềm hỗ trợ kết nối vận tải không thực hiện đúng quy định về cung cấp phần mềm ứng dụng hỗ trợ kết nối vận tải"} |
| e2 | HanhVi | D12/K7/b | {"span": "Đơn vị cung cấp phần mềm hỗ trợ kết nối vận tải không cung cấp cho cơ quan quản lý danh sách các đơn vị kinh doanh vận tải, xe ô tô và lái xe của các đơn vị vận tải hợp tác với đơn vị cung cấp phần mềm ứng dụng hỗ trợ kết nối vận tải hoặc không cung cấp tài khoản truy cập vào phần mềm ứng dụng hỗ trợ kết nối vận tải cho cơ quan quản lý khi có yêu cầu hoặc không thực hiện lưu trữ theo quy định"} |
| e3 | HanhVi | D12/K7/c | {"span": "Tự ý điều chỉnh giá cước vận tải đã niêm yết hoặc giá trị hợp đồng đã ký kết trên phần mềm"} |
| e4 | HanhVi | D12/K7/d | {"span": "Cho phép đơn vị kinh doanh vận tải hành khách theo hợp đồng sử dụng phần mềm để xác nhận đặt chỗ cho từng hành khách đi xe, bán vé hoặc thu tiền đối với từng hành khách trái quy định"} |
| e6 | HanhVi | D12/K7/e | {"span": "Phần mềm ứng dụng hỗ trợ kết nối vận tải để lái xe phải thực hiện nhiều thao tác nhận chuyến xe khi xe đang di chuyển"} |
| e5 | HanhVi | D12/K7/đ | {"span": "Không cung cấp cho đơn vị kinh doanh vận tải giao diện và công cụ để thực hiện được việc trực tiếp điều hành phương tiện và lái xe, đàm phán, quyết định giá cước vận tải với hành khách và người thuê vận tải trên phần mềm"} |

- QUY_DINH_HANH_VI: unit:ND336-2025/D12/K7/a → e1
- QUY_DINH_HANH_VI: unit:ND336-2025/D12/K7/b → e2
- QUY_DINH_HANH_VI: unit:ND336-2025/D12/K7/c → e3
- QUY_DINH_HANH_VI: unit:ND336-2025/D12/K7/d → e4
- QUY_DINH_HANH_VI: unit:ND336-2025/D12/K7/e → e6
- QUY_DINH_HANH_VI: unit:ND336-2025/D12/K7/đ → e5
- BI_XU_PHAT: unit:ND336-2025/D12/K7/a → e7
- BI_XU_PHAT: unit:ND336-2025/D12/K7/b → e7
- BI_XU_PHAT: unit:ND336-2025/D12/K7/c → e7
- BI_XU_PHAT: unit:ND336-2025/D12/K7/d → e7
- BI_XU_PHAT: unit:ND336-2025/D12/K7/e → e7
- BI_XU_PHAT: unit:ND336-2025/D12/K7/đ → e7

## ND336-2025/D9/K4@2026-11-03 · nd336 · tier B · ĐÃ DUYỆT

Điều: Xử phạt các hành vi vi phạm quy định về quản lý, khai thác, bảo trì, bảo vệ kết cấu hạ tầng đường bộ

```
[ND336-2025/D9/K4] 4. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với cá nhân, từ 6.000.000 đồng đến 10.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
[ND336-2025/D9/K4/a] a) Làm hư hỏng hoặc làm mất tác dụng của hệ thống thoát nước đường bộ;
[ND336-2025/D9/K4/b] b) Tự ý tháo dỡ, di chuyển, điều chỉnh, làm hư hỏng, làm sai mục đích sử dụng hoặc làm sai lệch biển báo hiệu, đèn tín hiệu giao thông, rào chắn, cọc tiêu, cột cây số, vạch kẻ đường, tường bảo vệ, hàng rào hộ lan, mốc chỉ giới, cọc mốc giải phóng mặt bằng và các báo hiệu đường bộ khác;
[ND336-2025/D9/K4/c] c) Tự ý đập phá, tháo dỡ bó vỉa hè hoặc sửa chữa, cải tạo vỉa hè trái phép.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| c2 | CheTai | D9/K4 | {"loai": "phat_tien", "min_vnd": 6000000, "max_vnd": 10000000} |
| e4 | CheTai | D9/K4 | {"loai": "phat_tien", "min_vnd": 3000000, "max_vnd": 5000000} |
| e6 | ChuThe | D9/K4 | {"catalog_id": "CT:ca-nhan"} |
| e7 | ChuThe | D9/K4 | {"catalog_id": "CT:to-chuc"} |
| e1 | HanhVi | D9/K4/a | {"span": "Làm hư hỏng hoặc làm mất tác dụng của hệ thống thoát nước đường bộ"} |
| e2 | HanhVi | D9/K4/b | {"span": "Tự ý tháo dỡ, di chuyển, điều chỉnh, làm hư hỏng, làm sai mục đích sử dụng hoặc làm sai lệch biển báo hiệu, đèn tín hiệu giao thông, rào chắn, cọc tiêu, cột cây số, vạch kẻ đường, tường bảo vệ, hàng rào hộ lan, mốc chỉ giới, cọc mốc giải phóng mặt bằng và các báo hiệu đường bộ khác"} |
| e3 | HanhVi | D9/K4/c | {"span": "Tự ý đập phá, tháo dỡ bó vỉa hè hoặc sửa chữa, cải tạo vỉa hè trái phép"} |

- QUY_DINH_HANH_VI: unit:ND336-2025/D9/K4/a → e1
- QUY_DINH_HANH_VI: unit:ND336-2025/D9/K4/b → e2
- QUY_DINH_HANH_VI: unit:ND336-2025/D9/K4/c → e3
- BI_XU_PHAT: unit:ND336-2025/D9/K4/a → c2
- BI_XU_PHAT: unit:ND336-2025/D9/K4/a → e4
- BI_XU_PHAT: unit:ND336-2025/D9/K4/b → c2
- BI_XU_PHAT: unit:ND336-2025/D9/K4/b → e4
- BI_XU_PHAT: unit:ND336-2025/D9/K4/c → c2
- BI_XU_PHAT: unit:ND336-2025/D9/K4/c → e4
- AP_DUNG_CHO: unit:ND336-2025/D9/K4 → e6
- AP_DUNG_CHO: unit:ND336-2025/D9/K4 → e7

Bản nháp bị bỏ 4 mục:
- so_lech_regex: {"id": "e5", "type": "CheTai", "unit_id": "ND336-2025/D9/K4", "ten": null, "span": null, "dieu_kien": null, "catalog_id": null, "loai": "phat_tien", "min_vnd": 6000000, "max_vnd": 10000000, "min_thang
- dich_khong_hop_le: {"type": "BI_XU_PHAT", "src": "unit:ND336-2025/D9/K4/a", "dst": "e5"}
- dich_khong_hop_le: {"type": "BI_XU_PHAT", "src": "unit:ND336-2025/D9/K4/b", "dst": "e5"}
- dich_khong_hop_le: {"type": "BI_XU_PHAT", "src": "unit:ND336-2025/D9/K4/c", "dst": "e5"}

## ND336-2025/D11/K2@2026-11-03 · tier_b · tier B · ĐÃ DUYỆT

Điều: Xử phạt người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ kinh doanh vận tải vi phạm quy định về vận tải đường bộ

```
[ND336-2025/D11/K2] 2. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với việc thực hiện một trong các hành vi vi phạm sau đây:
[ND336-2025/D11/K2/a] a) Điều khiển xe taxi không có đồng hồ tính tiền cước (đối với loại xe đăng ký sử dụng đồng hồ tính tiền) hoặc có nhưng không đúng quy định hoặc có nhưng không sử dụng đồng hồ để tính tiền cước theo yêu cầu của hành khách hoặc can thiệp để điều chỉnh tiền cước hiển thị trên đồng hồ;
[ND336-2025/D11/K2/b] b) Điều khiển xe taxi sử dụng phần mềm tính tiền mà trên xe không có thiết bị để kết nối trực tiếp với hành khách theo quy định;
[ND336-2025/D11/K2/c] c) Điều khiển xe taxi không sử dụng phần mềm tính tiền (đối với loại xe đăng ký sử dụng phần mềm tính tiền) hoặc sử dụng phần mềm tính tiền không bảo đảm các yêu cầu theo quy định;
[ND336-2025/D11/K2/d] d) Điều khiển xe kinh doanh vận tải hành khách theo tuyến cố định thu tiền vé cao hơn giá vé đã kê khai và niêm yết theo quy định.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e5 | CheTai | D11/K2 | {"loai": "phat_tien", "min_vnd": 1000000, "max_vnd": 2000000} |
| e6 | PhuongTien | D11/K2 | {"catalog_id": "PT:xe-o-to-kinh-doanh-van-tai"} |
| e7 | PhuongTien | D11/K2 | {"catalog_id": "PT:xe-cho-nguoi-bon-banh-co-gan-dong-co"} |
| e8 | ChuThe | D11/K2 | {"catalog_id": "CT:nguoi-dieu-khien-xe"} |
| e1 | HanhVi | D11/K2/a | {"span": "Điều khiển xe taxi không có đồng hồ tính tiền cước (đối với loại xe đăng ký sử dụng đồng hồ tính tiền) hoặc có nhưng không đúng quy định hoặc có nhưng không sử dụng đồng hồ để tính tiền cước theo yêu cầu của hành khách hoặc can thiệp để điều chỉnh tiền cước hiển thị trên đồng hồ"} |
| e2 | HanhVi | D11/K2/b | {"span": "Điều khiển xe taxi sử dụng phần mềm tính tiền mà trên xe không có thiết bị để kết nối trực tiếp với hành khách theo quy định"} |
| e3 | HanhVi | D11/K2/c | {"span": "Điều khiển xe taxi không sử dụng phần mềm tính tiền (đối với loại xe đăng ký sử dụng phần mềm tính tiền) hoặc sử dụng phần mềm tính tiền không bảo đảm các yêu cầu theo quy định"} |
| e4 | HanhVi | D11/K2/d | {"span": "Điều khiển xe kinh doanh vận tải hành khách theo tuyến cố định thu tiền vé cao hơn giá vé đã kê khai và niêm yết theo quy định"} |

- QUY_DINH_HANH_VI: unit:ND336-2025/D11/K2/a → e1
- QUY_DINH_HANH_VI: unit:ND336-2025/D11/K2/b → e2
- QUY_DINH_HANH_VI: unit:ND336-2025/D11/K2/c → e3
- QUY_DINH_HANH_VI: unit:ND336-2025/D11/K2/d → e4
- BI_XU_PHAT: unit:ND336-2025/D11/K2/a → e5
- BI_XU_PHAT: unit:ND336-2025/D11/K2/b → e5
- BI_XU_PHAT: unit:ND336-2025/D11/K2/c → e5
- BI_XU_PHAT: unit:ND336-2025/D11/K2/d → e5
- AP_DUNG_CHO: unit:ND336-2025/D11/K2 → e6
- AP_DUNG_CHO: unit:ND336-2025/D11/K2 → e7
- AP_DUNG_CHO: unit:ND336-2025/D11/K2 → e8

## ND336-2025/D5/K2@2026-11-03 · tier_b · tier B · ĐÃ DUYỆT

Điều: Xử phạt các hành vi vi phạm quy định về sử dụng, khai thác trong phạm vi đất dành cho kết cấu hạ tầng đường bộ

```
[ND336-2025/D5/K2] 2. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với cá nhân, từ 2.000.000 đồng đến 4.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
[ND336-2025/D5/K2/a] a) Dựng cổng chào trái phép trong phạm vi đất dành cho kết cấu hạ tầng đường bộ gây ảnh hưởng đến an toàn giao thông đường bộ;
[ND336-2025/D5/K2/b] b) Treo băng rôn trái phép trong phạm vi đất của đường bộ gây ảnh hưởng đến an toàn giao thông đường bộ;
[ND336-2025/D5/K2/c] c) Đặt, treo biển hiệu, bảng quảng cáo trên đất của đường bộ ở đoạn đường ngoài đô thị trừ việc đặt, treo biển hiệu, bảng quảng cáo tại lòng đường và trừ hành vi vi phạm quy định tại điểm a khoản 5 Điều này;
[ND336-2025/D5/K2/d] d) Đổ rác thải ra đường bộ không đúng nơi quy định, trừ hành vi vi phạm quy định tại điểm a khoản 4 Điều này.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| c2 | CheTai | D5/K2 | {"loai": "phat_tien", "min_vnd": 2000000, "max_vnd": 4000000} |
| e5 | CheTai | D5/K2 | {"loai": "phat_tien", "min_vnd": 1000000, "max_vnd": 2000000} |
| e7 | ChuThe | D5/K2 | {"catalog_id": "CT:ca-nhan"} |
| e8 | ChuThe | D5/K2 | {"catalog_id": "CT:to-chuc"} |
| e1 | HanhVi | D5/K2/a | {"span": "Dựng cổng chào trái phép trong phạm vi đất dành cho kết cấu hạ tầng đường bộ gây ảnh hưởng đến an toàn giao thông đường bộ"} |
| e2 | HanhVi | D5/K2/b | {"span": "Treo băng rôn trái phép trong phạm vi đất của đường bộ gây ảnh hưởng đến an toàn giao thông đường bộ"} |
| e3 | HanhVi | D5/K2/c | {"span": "Đặt, treo biển hiệu, bảng quảng cáo trên đất của đường bộ ở đoạn đường ngoài đô thị"} |
| e4 | HanhVi | D5/K2/d | {"span": "Đổ rác thải ra đường bộ không đúng nơi quy định"} |

- QUY_DINH_HANH_VI: unit:ND336-2025/D5/K2/a → e1
- QUY_DINH_HANH_VI: unit:ND336-2025/D5/K2/b → e2
- QUY_DINH_HANH_VI: unit:ND336-2025/D5/K2/c → e3
- QUY_DINH_HANH_VI: unit:ND336-2025/D5/K2/d → e4
- BI_XU_PHAT: unit:ND336-2025/D5/K2/a → c2
- BI_XU_PHAT: unit:ND336-2025/D5/K2/a → e5
- BI_XU_PHAT: unit:ND336-2025/D5/K2/b → c2
- BI_XU_PHAT: unit:ND336-2025/D5/K2/b → e5
- BI_XU_PHAT: unit:ND336-2025/D5/K2/c → c2
- BI_XU_PHAT: unit:ND336-2025/D5/K2/c → e5
- BI_XU_PHAT: unit:ND336-2025/D5/K2/d → c2
- BI_XU_PHAT: unit:ND336-2025/D5/K2/d → e5
- AP_DUNG_CHO: unit:ND336-2025/D5/K2 → e7
- AP_DUNG_CHO: unit:ND336-2025/D5/K2 → e8

Bản nháp bị bỏ 5 mục:
- so_lech_regex: {"id": "e6", "type": "CheTai", "unit_id": "ND336-2025/D5/K2", "ten": null, "span": null, "dieu_kien": null, "catalog_id": null, "loai": "phat_tien", "min_vnd": 2000000, "max_vnd": 4000000, "min_thang"
- dich_khong_hop_le: {"type": "BI_XU_PHAT", "src": "unit:ND336-2025/D5/K2/a", "dst": "e6"}
- dich_khong_hop_le: {"type": "BI_XU_PHAT", "src": "unit:ND336-2025/D5/K2/b", "dst": "e6"}
- dich_khong_hop_le: {"type": "BI_XU_PHAT", "src": "unit:ND336-2025/D5/K2/c", "dst": "e6"}
- dich_khong_hop_le: {"type": "BI_XU_PHAT", "src": "unit:ND336-2025/D5/K2/d", "dst": "e6"}

## ND336-2025/D14/K2@2026-11-03 · nd336 · tier B · ĐÃ DUYỆT

Điều: Xử phạt các hành vi vi phạm về vận tải nội bộ

```
[ND336-2025/D14/K2] 2. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với cá nhân, từ 6.000.000 đồng đến 10.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
[ND336-2025/D14/K2/a] a) Không tổ chức thực hiện hoặc có tổ chức thực hiện nhưng không đầy đủ các nội dung về công tác quản lý an toàn giao thông theo quy định, trừ hành vi vi phạm quy định tại điểm b khoản này;
[ND336-2025/D14/K2/b] b) Không theo dõi, giám sát hoạt động của lái xe, phương tiện trong suốt quá trình hoạt động vận tải nội bộ;
[ND336-2025/D14/K2/c] c) Sử dụng xe ô tô chở người có giường nằm hai tầng để hoạt động trên các tuyến đường cấp V và cấp VI miền núi;
[ND336-2025/D14/K2/d] d) Sử dụng xe vận tải nội bộ để kinh doanh vận tải hành khách, hàng hóa;
[ND336-2025/D14/K2/đ] đ) Sử dụng xe vận tải nội bộ để vận chuyển người, hàng hóa không đúng đối tượng theo quy định;
[ND336-2025/D14/K2/e] e) Sử dụng xe ô tô thuộc sở hữu của thành viên hợp tác xã để vận tải nội bộ mà không có hợp đồng dịch vụ giữa thành viên với hợp tác xã theo quy định hoặc sử dụng xe ô tô không thuộc quyền sở hữu hoặc quyền sử dụng hợp pháp theo quy định.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| c2 | CheTai | D14/K2 | {"loai": "phat_tien", "min_vnd": 6000000, "max_vnd": 10000000} |
| e7 | CheTai | D14/K2 | {"loai": "phat_tien", "min_vnd": 3000000, "max_vnd": 5000000} |
| t1 | ChuThe | D14/K2 | {"catalog_id": "CT:ca-nhan"} |
| t2 | ChuThe | D14/K2 | {"catalog_id": "CT:to-chuc"} |
| e1 | HanhVi | D14/K2/a | {"span": "Không tổ chức thực hiện hoặc có tổ chức thực hiện nhưng không đầy đủ các nội dung về công tác quản lý an toàn giao thông theo quy định"} |
| e2 | HanhVi | D14/K2/b | {"span": "Không theo dõi, giám sát hoạt động của lái xe, phương tiện trong suốt quá trình hoạt động vận tải nội bộ"} |
| e3 | HanhVi | D14/K2/c | {"span": "Sử dụng xe ô tô chở người có giường nằm hai tầng để hoạt động trên các tuyến đường cấp V và cấp VI miền núi"} |
| e4 | HanhVi | D14/K2/d | {"span": "Sử dụng xe vận tải nội bộ để kinh doanh vận tải hành khách, hàng hóa"} |
| e12 | PhuongTien | D14/K2/e | {"catalog_id": "PT:xe-o-to"} |
| e6 | HanhVi | D14/K2/e | {"span": "Sử dụng xe ô tô thuộc sở hữu của thành viên hợp tác xã để vận tải nội bộ mà không có hợp đồng dịch vụ giữa thành viên với hợp tác xã theo quy định hoặc sử dụng xe ô tô không thuộc quyền sở hữu hoặc quyền sử dụng hợp pháp theo quy định"} |
| e5 | HanhVi | D14/K2/đ | {"span": "Sử dụng xe vận tải nội bộ để vận chuyển người, hàng hóa không đúng đối tượng theo quy định"} |

- QUY_DINH_HANH_VI: unit:ND336-2025/D14/K2/a → e1
- QUY_DINH_HANH_VI: unit:ND336-2025/D14/K2/b → e2
- QUY_DINH_HANH_VI: unit:ND336-2025/D14/K2/c → e3
- QUY_DINH_HANH_VI: unit:ND336-2025/D14/K2/d → e4
- QUY_DINH_HANH_VI: unit:ND336-2025/D14/K2/e → e6
- QUY_DINH_HANH_VI: unit:ND336-2025/D14/K2/đ → e5
- BI_XU_PHAT: unit:ND336-2025/D14/K2/a → c2
- BI_XU_PHAT: unit:ND336-2025/D14/K2/a → e7
- BI_XU_PHAT: unit:ND336-2025/D14/K2/b → c2
- BI_XU_PHAT: unit:ND336-2025/D14/K2/b → e7
- BI_XU_PHAT: unit:ND336-2025/D14/K2/c → c2
- BI_XU_PHAT: unit:ND336-2025/D14/K2/c → e7
- BI_XU_PHAT: unit:ND336-2025/D14/K2/d → c2
- BI_XU_PHAT: unit:ND336-2025/D14/K2/d → e7
- BI_XU_PHAT: unit:ND336-2025/D14/K2/e → c2
- BI_XU_PHAT: unit:ND336-2025/D14/K2/e → e7
- BI_XU_PHAT: unit:ND336-2025/D14/K2/đ → c2
- BI_XU_PHAT: unit:ND336-2025/D14/K2/đ → e7
- AP_DUNG_CHO: unit:ND336-2025/D14/K2 → t1
- AP_DUNG_CHO: unit:ND336-2025/D14/K2 → t2
- AP_DUNG_CHO: unit:ND336-2025/D14/K2/e → e12

Bản nháp bị bỏ 8 mục:
- so_lech_regex: {"id": "e8", "type": "CheTai", "unit_id": "ND336-2025/D14/K2", "ten": null, "span": null, "dieu_kien": null, "catalog_id": null, "loai": "phat_tien", "min_vnd": 6000000, "max_vnd": 10000000, "min_than
- ngoai_danh_muc: {"id": "e9", "type": "PhuongTien", "unit_id": "ND336-2025/D14/K2/c", "ten": null, "span": null, "dieu_kien": null, "catalog_id": "PT:xe-o-to-cho-nguoi-co-giuong-nam-hai-tang", "loai": null, "min_vnd":
- ngoai_danh_muc: {"id": "e10", "type": "PhuongTien", "unit_id": "ND336-2025/D14/K2/d", "ten": null, "span": null, "dieu_kien": null, "catalog_id": "PT:xe-van-tai-noi-bo", "loai": null, "min_vnd": null, "max_vnd": null
- ngoai_danh_muc: {"id": "e11", "type": "PhuongTien", "unit_id": "ND336-2025/D14/K2/đ", "ten": null, "span": null, "dieu_kien": null, "catalog_id": "PT:xe-van-tai-noi-bo", "loai": null, "min_vnd": null, "max_vnd": null
- dich_khong_hop_le: {"type": "AP_DUNG_CHO", "src": "unit:ND336-2025/D14/K2", "dst": "e9"}
- dich_khong_hop_le: {"type": "AP_DUNG_CHO", "src": "unit:ND336-2025/D14/K2", "dst": "e10"}
- dich_khong_hop_le: {"type": "AP_DUNG_CHO", "src": "unit:ND336-2025/D14/K2", "dst": "e11"}
- dich_khong_hop_le: {"type": "BI_XU_PHAT", "src": "unit:ND336-2025/D14/K2", "dst": "e8"}

## TT79-2024-BCA/D27/K1@2026-11-03 · tt_tier_a · tier A · ĐÃ DUYỆT

Điều: Trách nhiệm của Công an các đơn vị, địa phương trong việc thu hồi chứng nhận đăng ký xe, biển số xe

```
[TT79-2024-BCA/D27/K1] 1. Trách nhiệm của cơ quan đăng ký xe
[TT79-2024-BCA/D27/K1/a] a) Căn cứ danh sách xe ô tô hết niên hạn sử dụng, xe thải bỏ, xe không được phép lưu hành theo quy định của pháp luật do cơ quan đăng kiểm hoặc cơ quan nhà nước có thẩm quyền cung cấp, cơ quan đăng ký xe phải rà soát, thông báo cho tổ chức, cá nhân có xe để làm thủ tục thu hồi. Trong thời hạn 30 ngày, kể từ ngày thông báo, nếu chủ xe không làm thủ tục thu hồi thì người có thẩm quyền thực hiện thủ tục xử phạt vi phạm hành chính theo quy định;
[TT79-2024-BCA/D27/K1/b] b) Cập nhật thông tin khai báo của chủ xe trên trang thông tin điện tử của Cục Cảnh sát giao thông hoặc cổng dịch vụ công về xe hết niên hạn sử dụng, xe thải bỏ, xe hư hỏng không sử dụng được, cần làm thủ tục thu hồi theo quy định tại Thông tư này;
[TT79-2024-BCA/D27/K1/c] c) Thông báo danh sách xe hết niên hạn sử dụng, xe thải bỏ, xe không được phép lưu hành, xe mất cắp theo quy định của pháp luật cho Công an các đơn vị, địa phương làm nhiệm vụ bảo đảm trật tự, an toàn giao thông biết để phát hiện, xử lý theo quy định của pháp luật và thông báo cho chủ xe qua địa chỉ thư điện tử hoặc qua tin nhắn điện thoại hoặc cổng dịch vụ công;
[TT79-2024-BCA/D27/K1/d] d) Xe đã đăng ký, cấp biển số xe không đúng quy định của pháp luật; xe đã đăng ký nhưng phát hiện hồ sơ xe bị làm giả hoặc có kết luận của cơ quan có thẩm quyền về việc thay đổi trái phép số khung, số máy thì cơ quan đăng ký xe thông báo cho chủ xe biết và tiến hành ra quyết định thu hồi chứng nhận đăng ký xe, biển số xe. Đối với hồ sơ xe có kết luận của cơ quan có thẩm quyền là hồ sơ giả hoặc số máy hoặc số khung bị cắt, hàn, tẩy xóa, đục sửa, đóng lại trái phép thì chuyển cơ quan điều tra làm rõ và xử lý theo quy định của pháp luật.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| e7 | PhuongTien | D27/K1 | {"catalog_id": "PT:xe-o-to"} |
| e1 | HanhVi | D27/K1/a | {"span": "rà soát, thông báo cho tổ chức, cá nhân có xe để làm thủ tục thu hồi", "dieu_kien": "căn cứ danh sách xe ô tô hết niên hạn sử dụng, xe thải bỏ, xe không được phép lưu hành theo quy định của pháp luật do cơ quan đăng kiểm hoặc cơ quan nhà nước có thẩm quyền cung cấp"} |
| e11 | ChuThe | D27/K1/a | {"catalog_id": "CT:nguoi-co-tham-quyen-xu-phat"} |
| e2 | HanhVi | D27/K1/a | {"span": "người có thẩm quyền thực hiện thủ tục xử phạt vi phạm hành chính theo quy định", "dieu_kien": "trong thời hạn 30 ngày, kể từ ngày thông báo, nếu chủ xe không làm thủ tục thu hồi"} |
| e12 | ChuThe | D27/K1/b | {"catalog_id": "CT:chu-xe"} |
| e3 | HanhVi | D27/K1/b | {"span": "Cập nhật thông tin khai báo của chủ xe trên trang thông tin điện tử của Cục Cảnh sát giao thông hoặc cổng dịch vụ công"} |
| e4 | HanhVi | D27/K1/c | {"span": "Thông báo danh sách xe hết niên hạn sử dụng, xe thải bỏ, xe không được phép lưu hành, xe mất cắp theo quy định của pháp luật cho Công an các đơn vị, địa phương làm nhiệm vụ bảo đảm trật tự, an toàn giao thông biết để phát hiện, xử lý theo quy định của pháp luật và thông báo cho chủ xe qua địa chỉ thư điện tử hoặc qua tin nhắn điện thoại hoặc cổng dịch vụ công", "dieu_kien": ""} |
| e14 | ChuThe | D27/K1/d | {"catalog_id": "CT:chu-xe"} |
| e5 | HanhVi | D27/K1/d | {"span": "cơ quan đăng ký xe thông báo cho chủ xe biết và tiến hành ra quyết định thu hồi chứng nhận đăng ký xe, biển số xe", "dieu_kien": "xe đã đăng ký, cấp biển số xe không đúng quy định của pháp luật; xe đã đăng ký nhưng phát hiện hồ sơ xe bị làm giả hoặc có kết luận của cơ quan có thẩm quyền về việc thay đổi trái phép số khung, số máy"} |
| e6 | HanhVi | D27/K1/d | {"span": "chuyển cơ quan điều tra làm rõ và xử lý theo quy định của pháp luật", "dieu_kien": "đối với hồ sơ xe có kết luận của cơ quan có thẩm quyền là hồ sơ giả hoặc số máy hoặc số khung bị cắt, hàn, tẩy xóa, đục sửa, đóng lại trái phép"} |

- QUY_DINH_HANH_VI: unit:TT79-2024-BCA/D27/K1/a → e1
- QUY_DINH_HANH_VI: unit:TT79-2024-BCA/D27/K1/a → e2
- QUY_DINH_HANH_VI: unit:TT79-2024-BCA/D27/K1/b → e3
- QUY_DINH_HANH_VI: unit:TT79-2024-BCA/D27/K1/c → e4
- QUY_DINH_HANH_VI: unit:TT79-2024-BCA/D27/K1/d → e5
- QUY_DINH_HANH_VI: unit:TT79-2024-BCA/D27/K1/d → e6
- AP_DUNG_CHO: unit:TT79-2024-BCA/D27/K1 → e7
- AP_DUNG_CHO: unit:TT79-2024-BCA/D27/K1/a → e11
- AP_DUNG_CHO: unit:TT79-2024-BCA/D27/K1/b → e12
- AP_DUNG_CHO: unit:TT79-2024-BCA/D27/K1/d → e14

Bản nháp bị bỏ 4 mục:
- ngoai_danh_muc: {"id": "e13", "type": "ChuThe", "unit_id": "TT79-2024-BCA/D27/K1/c", "ten": null, "span": null, "dieu_kien": null, "catalog_id": "CT:cong-an-cac-don-vi-dia-phuong", "loai": null, "min_vnd": null, "max
- ngoai_danh_muc: {"id": "e15", "type": "ChuThe", "unit_id": "TT79-2024-BCA/D27/K1/d", "ten": null, "span": null, "dieu_kien": null, "catalog_id": "CT:co-quan-dieu-tra", "loai": null, "min_vnd": null, "max_vnd": null, 
- dich_khong_hop_le: {"type": "AP_DUNG_CHO", "src": "unit:TT79-2024-BCA/D27/K1/c", "dst": "e13"}
- dich_khong_hop_le: {"type": "AP_DUNG_CHO", "src": "unit:TT79-2024-BCA/D27/K1/d", "dst": "e15"}

## ND336-2025/D12/K6@2026-11-03 · tier_b · tier B · ĐÃ DUYỆT

Điều: Xử phạt các hành vi vi phạm quy định về vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ

```
[ND336-2025/D12/K6] 6. Phạt tiền từ 12.000.000 đồng đến 16.000.000 đồng đối với cá nhân, từ 24.000.000 đồng đến 32.000.000 đồng đối với tổ chức kinh doanh vận tải, dịch vụ hỗ trợ vận tải thực hiện một trong các hành vi vi phạm sau đây:
[ND336-2025/D12/K6/a] a) Kinh doanh vận tải bằng xe ô tô, xe bốn bánh có gắn động cơ mà không có giấy phép kinh doanh vận tải theo quy định, trừ hành vi quy định tại điểm i khoản này;
[ND336-2025/D12/K6/b] b) Thực hiện không đúng hình thức kinh doanh đã đăng ký trong giấy phép kinh doanh vận tải;
[ND336-2025/D12/K6/c] c) Thành lập, tổ chức điểm giao dịch đón, trả khách, bốc dỡ hàng hóa trái phép;
[ND336-2025/D12/K6/d] d) Không xây dựng quy trình đảm bảo an toàn giao thông cho xe ra, vào bến hoặc có xây dựng nhưng thực hiện không đúng, không đầy đủ quy trình đảm bảo an toàn giao thông cho xe ra, vào bến; không niêm yết hoặc niêm yết không đầy đủ, chính xác các thông tin tại bến xe theo quy định;
[ND336-2025/D12/K6/đ] đ) Không gửi hóa đơn điện tử, không gửi nội dung tối thiểu của hợp đồng điện tử theo quy định;
[ND336-2025/D12/K6/e] e) Không thực hiện hoặc thực hiện không đầy đủ, không đúng quy định về quản lý, áp dụng thông tin từ phần mềm quản lý bến xe khách;
[ND336-2025/D12/K6/g] g) Sử dụng hợp đồng điện tử không có giao diện phần mềm cung cấp cho hành khách hoặc người thuê vận tải theo quy định hoặc có nhưng giao diện không bảo đảm các yêu cầu theo quy định;
[ND336-2025/D12/K6/h] h) Để tổ chức, cá nhân không có giấy phép kinh doanh vận tải bằng xe ô tô, xe bốn bánh có gắn động cơ điều hành phương tiện và lái xe hoặc quyết định giá cước để vận tải;
[ND336-2025/D12/K6/i] i) Trực tiếp điều hành phương tiện, lái xe hoặc quyết định giá cước vận tải nhưng không có giấy phép kinh doanh vận tải theo quy định;
[ND336-2025/D12/K6/k] k) Không thực hiện lưu trữ hoặc lưu trữ không đúng quy định;
[ND336-2025/D12/K6/l] l) Phần mềm không ghi nhận được đánh giá của khách hàng về chất lượng phục vụ của lái xe hoặc có ghi nhận nhưng không gửi thông tin đến đơn vị kinh doanh vận tải theo quy định.
```

| id | loại | unit | nội dung |
| --- | --- | --- | --- |
| c2 | CheTai | D12/K6 | {"loai": "phat_tien", "min_vnd": 24000000, "max_vnd": 32000000} |
| e1 | CheTai | D12/K6 | {"loai": "phat_tien", "min_vnd": 12000000, "max_vnd": 16000000} |
| e16 | ChuThe | D12/K6 | {"catalog_id": "CT:ca-nhan"} |
| e17 | ChuThe | D12/K6 | {"catalog_id": "CT:to-chuc-kinh-doanh-van-tai"} |
| p3 | PhuongTien | D12/K6 | {"catalog_id": "PT:xe-cho-hang-bon-banh-co-gan-dong-co"} |
| e14 | PhuongTien | D12/K6/a | {"catalog_id": "PT:xe-o-to"} |
| e15 | PhuongTien | D12/K6/a | {"catalog_id": "PT:xe-cho-nguoi-bon-banh-co-gan-dong-co"} |
| e3 | HanhVi | D12/K6/a | {"span": "Kinh doanh vận tải bằng xe ô tô, xe bốn bánh có gắn động cơ mà không có giấy phép kinh doanh vận tải theo quy định"} |
| e4 | HanhVi | D12/K6/b | {"span": "Thực hiện không đúng hình thức kinh doanh đã đăng ký trong giấy phép kinh doanh vận tải"} |
| e5 | HanhVi | D12/K6/c | {"span": "Thành lập, tổ chức điểm giao dịch đón, trả khách, bốc dỡ hàng hóa trái phép"} |
| d1 | HanhVi | D12/K6/d | {"ten": "không xây dựng hoặc thực hiện không đúng quy trình an toàn cho xe ra, vào bến", "span": "Không xây dựng quy trình đảm bảo an toàn giao thông cho xe ra, vào bến hoặc có xây dựng nhưng thực hiện không đúng, không đầy đủ quy trình đảm bảo an toàn giao thông cho xe ra, vào bến"} |
| d2 | HanhVi | D12/K6/d | {"ten": "không niêm yết hoặc niêm yết không đầy đủ thông tin tại bến xe", "span": "không niêm yết hoặc niêm yết không đầy đủ, chính xác các thông tin tại bến xe theo quy định"} |
| e8 | HanhVi | D12/K6/e | {"span": "Không thực hiện hoặc thực hiện không đầy đủ, không đúng quy định về quản lý, áp dụng thông tin từ phần mềm quản lý bến xe khách"} |
| e9 | HanhVi | D12/K6/g | {"span": "Sử dụng hợp đồng điện tử không có giao diện phần mềm cung cấp cho hành khách hoặc người thuê vận tải theo quy định hoặc có nhưng giao diện không bảo đảm các yêu cầu theo quy định"} |
| e10 | HanhVi | D12/K6/h | {"span": "Để tổ chức, cá nhân không có giấy phép kinh doanh vận tải bằng xe ô tô, xe bốn bánh có gắn động cơ điều hành phương tiện và lái xe hoặc quyết định giá cước để vận tải"} |
| e11 | HanhVi | D12/K6/i | {"span": "Trực tiếp điều hành phương tiện, lái xe hoặc quyết định giá cước vận tải nhưng không có giấy phép kinh doanh vận tải theo quy định"} |
| e12 | HanhVi | D12/K6/k | {"span": "Không thực hiện lưu trữ hoặc lưu trữ không đúng quy định"} |
| e13 | HanhVi | D12/K6/l | {"span": "Phần mềm không ghi nhận được đánh giá của khách hàng về chất lượng phục vụ của lái xe hoặc có ghi nhận nhưng không gửi thông tin đến đơn vị kinh doanh vận tải theo quy định"} |
| e7 | HanhVi | D12/K6/đ | {"span": "Không gửi hóa đơn điện tử, không gửi nội dung tối thiểu của hợp đồng điện tử theo quy định"} |

- QUY_DINH_HANH_VI: unit:ND336-2025/D12/K6/a → e3
- QUY_DINH_HANH_VI: unit:ND336-2025/D12/K6/b → e4
- QUY_DINH_HANH_VI: unit:ND336-2025/D12/K6/c → e5
- QUY_DINH_HANH_VI: unit:ND336-2025/D12/K6/d → d1
- QUY_DINH_HANH_VI: unit:ND336-2025/D12/K6/d → d2
- QUY_DINH_HANH_VI: unit:ND336-2025/D12/K6/e → e8
- QUY_DINH_HANH_VI: unit:ND336-2025/D12/K6/g → e9
- QUY_DINH_HANH_VI: unit:ND336-2025/D12/K6/h → e10
- QUY_DINH_HANH_VI: unit:ND336-2025/D12/K6/i → e11
- QUY_DINH_HANH_VI: unit:ND336-2025/D12/K6/k → e12
- QUY_DINH_HANH_VI: unit:ND336-2025/D12/K6/l → e13
- QUY_DINH_HANH_VI: unit:ND336-2025/D12/K6/đ → e7
- BI_XU_PHAT: unit:ND336-2025/D12/K6/a → c2
- BI_XU_PHAT: unit:ND336-2025/D12/K6/a → e1
- BI_XU_PHAT: unit:ND336-2025/D12/K6/b → c2
- BI_XU_PHAT: unit:ND336-2025/D12/K6/b → e1
- BI_XU_PHAT: unit:ND336-2025/D12/K6/c → c2
- BI_XU_PHAT: unit:ND336-2025/D12/K6/c → e1
- BI_XU_PHAT: unit:ND336-2025/D12/K6/d → c2
- BI_XU_PHAT: unit:ND336-2025/D12/K6/d → e1
- BI_XU_PHAT: unit:ND336-2025/D12/K6/e → c2
- BI_XU_PHAT: unit:ND336-2025/D12/K6/e → e1
- BI_XU_PHAT: unit:ND336-2025/D12/K6/g → c2
- BI_XU_PHAT: unit:ND336-2025/D12/K6/g → e1
- BI_XU_PHAT: unit:ND336-2025/D12/K6/h → c2
- BI_XU_PHAT: unit:ND336-2025/D12/K6/h → e1
- BI_XU_PHAT: unit:ND336-2025/D12/K6/i → c2
- BI_XU_PHAT: unit:ND336-2025/D12/K6/i → e1
- BI_XU_PHAT: unit:ND336-2025/D12/K6/k → c2
- BI_XU_PHAT: unit:ND336-2025/D12/K6/k → e1
- BI_XU_PHAT: unit:ND336-2025/D12/K6/l → c2
- BI_XU_PHAT: unit:ND336-2025/D12/K6/l → e1
- BI_XU_PHAT: unit:ND336-2025/D12/K6/đ → c2
- BI_XU_PHAT: unit:ND336-2025/D12/K6/đ → e1
- AP_DUNG_CHO: unit:ND336-2025/D12/K6 → e16
- AP_DUNG_CHO: unit:ND336-2025/D12/K6 → e17
- AP_DUNG_CHO: unit:ND336-2025/D12/K6 → p3
- AP_DUNG_CHO: unit:ND336-2025/D12/K6/a → e14
- AP_DUNG_CHO: unit:ND336-2025/D12/K6/a → e15

Bản nháp bị bỏ 13 mục:
- so_lech_regex: {"id": "e2", "type": "CheTai", "unit_id": "ND336-2025/D12/K6", "ten": null, "span": null, "dieu_kien": null, "catalog_id": null, "loai": "phat_tien", "min_vnd": 24000000, "max_vnd": 32000000, "min_tha
- dich_khong_hop_le: {"type": "BI_XU_PHAT", "src": "unit:ND336-2025/D12/K6", "dst": "e2"}
- dich_khong_hop_le: {"type": "BI_XU_PHAT", "src": "unit:ND336-2025/D12/K6/a", "dst": "e2"}
- dich_khong_hop_le: {"type": "BI_XU_PHAT", "src": "unit:ND336-2025/D12/K6/b", "dst": "e2"}
- dich_khong_hop_le: {"type": "BI_XU_PHAT", "src": "unit:ND336-2025/D12/K6/c", "dst": "e2"}
- dich_khong_hop_le: {"type": "BI_XU_PHAT", "src": "unit:ND336-2025/D12/K6/d", "dst": "e2"}
- dich_khong_hop_le: {"type": "BI_XU_PHAT", "src": "unit:ND336-2025/D12/K6/đ", "dst": "e2"}
- dich_khong_hop_le: {"type": "BI_XU_PHAT", "src": "unit:ND336-2025/D12/K6/e", "dst": "e2"}
- dich_khong_hop_le: {"type": "BI_XU_PHAT", "src": "unit:ND336-2025/D12/K6/g", "dst": "e2"}
- dich_khong_hop_le: {"type": "BI_XU_PHAT", "src": "unit:ND336-2025/D12/K6/h", "dst": "e2"}
- dich_khong_hop_le: {"type": "BI_XU_PHAT", "src": "unit:ND336-2025/D12/K6/i", "dst": "e2"}
- dich_khong_hop_le: {"type": "BI_XU_PHAT", "src": "unit:ND336-2025/D12/K6/k", "dst": "e2"}
- dich_khong_hop_le: {"type": "BI_XU_PHAT", "src": "unit:ND336-2025/D12/K6/l", "dst": "e2"}
