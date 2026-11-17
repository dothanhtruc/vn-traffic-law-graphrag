# Bản nháp câu test (LLM viết, người dùng sửa)

Model `gpt-oss-20b` · prompt `(nhiều)` · 151/151 gợi ý có nháp · 326 câu nháp.

Cách dùng: với mỗi gợi ý, chọn **tối đa một** bản nháp, sửa câu hỏi + đáp án (bắt buộc — validator báo lỗi `nhap_chua_sua` nếu câu hỏi giữ nguyên), kiểm từng con số với nguồn, rồi chép **dòng JSON đã sửa** vào `data/qa/test.jsonl`. Giữ nguyên `source` và `draft_id` để đo tỷ lệ sửa. Cờ ⚠ là chỗ cần xem kỹ (không phải lỗi chắc chắn).

Câu `ngoai_pham_vi` (35) không có nháp: tự viết tay, `source: human`.

## da_buoc — cần ≥ 2 điều khoản nối bằng dẫn chiếu / chế tài

### WD-da_buoc-002 · tier A · vai: tài xế công nghệ · kiểu: tinh_huong_ban_than · DAN_CHIEU → TT14-2025-BXD/D17

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Thông tư số 14/2025/TT-BXD (Quy định về đào tạo lái xe; bồi dưỡng, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ)
Hiệu lực của trạng thái này: 2025-09-01 → nay
Mã điều khoản dùng được cho gold_units: TT14-2025-BXD/D19/K2

Điều 19. Tổ chức bồi dưỡng kiến thức pháp luật về giao thông đường bộ cho người điều khiển xe máy chuyên dùng tham gia giao thông đường bộ
2. Cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ căn cứ Chương trình đào tạo quy định tại Điều 17 Thông tư này xây dựng tài liệu giảng dạy và nội dung chi tiết chương trình đào tạo.

### Điều khoản được nguồn trên dẫn chiếu tới (TT14-2025-BXD/D17)
Mã điều khoản dùng được cho gold_units: TT14-2025-BXD/D17

Điều 17. Hình thức, chương trình bồi dưỡng kiến thức pháp luật về giao thông đường bộ

### Nguồn 2
Văn bản: Thông tư số 14/2025/TT-BXD (Quy định về đào tạo lái xe; bồi dưỡng, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ)
Hiệu lực của trạng thái này: 2025-09-01 → nay
Mã điều khoản dùng được cho gold_units: TT14-2025-BXD/D17/K1

Điều 17. Hình thức, chương trình bồi dưỡng kiến thức pháp luật về giao thông đường bộ
1. Người tham gia bồi dưỡng kiến thức pháp luật về giao thông đường bộ phải được bồi dưỡng tại cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ.

### Nguồn 3
Văn bản: Thông tư số 14/2025/TT-BXD (Quy định về đào tạo lái xe; bồi dưỡng, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ)
Hiệu lực của trạng thái này: 2025-09-01 → nay
Mã điều khoản dùng được cho gold_units: TT14-2025-BXD/D17/K2

Điều 17. Hình thức, chương trình bồi dưỡng kiến thức pháp luật về giao thông đường bộ
2. Chương trình bồi dưỡng kiến thức pháp luật về giao thông đường bộ:
TT | Nội dung chương trình | Số giờ
1 | Pháp luật về giao thông đường bộ | 12
2 | Quy chuẩn kỹ thuật quốc gia về báo hiệu đường bộ | 5
3 | Quy định về tốc độ và khoảng cách an toàn của xe cơ giới, xe máy chuyên dùng tham gia giao thông trên đường bộ | 3
4 | Quy định về xử lý vi phạm hành chính trong lĩnh vực giao thông đường bộ. | 4
5 | Quy định về cấp đăng ký, biển số; kiểm định xe máy chuyên dùng tham gia giao thông đường bộ | 3
6 | Ôn tập và kiểm tra | 5
Tổng thời gian đào tạo | 32

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là tài xế công nghệ, muốn tham gia bồi dưỡng kiến thức pháp luật, tôi có thể tự chọn cơ sở nào không?
- Đáp: Bạn phải tham gia bồi dưỡng tại một cơ sở được công nhận. Chương trình bồi dưỡng kéo dài 32 giờ, bao gồm 12 giờ về pháp luật, 5 giờ về báo hiệu, 3 giờ về tốc độ, 4 giờ về xử vi phạm, 3 giờ về đăng ký, biển số và kiểm định, và 5 giờ ôn tập.
- ⚠ chi_so_so_sai (0); chep_nguyen_van: “bồi dưỡng kiến thức pháp luật …”
- Ghi chú: Giả định rằng “cơ sở” là cơ sở được công nhận trong quy định.

```json
{"qid": "tD-da_buoc-002", "question": "Tôi là tài xế công nghệ, muốn tham gia bồi dưỡng kiến thức pháp luật, tôi có thể tự chọn cơ sở nào không?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Bạn phải tham gia bồi dưỡng tại một cơ sở được công nhận. Chương trình bồi dưỡng kéo dài 32 giờ, bao gồm 12 giờ về pháp luật, 5 giờ về báo hiệu, 3 giờ về tốc độ, 4 giờ về xử vi phạm, 3 giờ về đăng ký, biển số và kiểm định, và 5 giờ ôn tập.", "gold_units": ["TT14-2025-BXD/D19/K2", "TT14-2025-BXD/D17/K1"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-002:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là tài xế công nghệ, muốn biết thời gian bồi dưỡng cần bao lâu khi tham gia tại cơ sở được phép?
- Đáp: Bạn phải tham gia bồi dưỡng tại một cơ sở được công nhận. Chương trình bồi dưỡng kéo dài 32 giờ, bao gồm 12 giờ về pháp luật, 5 giờ về báo hiệu, 3 giờ về tốc độ, 4 giờ về xử vi phạm, 3 giờ về đăng ký, biển số và kiểm định, và 5 giờ ôn tập.
- ⚠ chi_so_so_sai (0)
- Ghi chú: Giả định rằng “cơ sở” là cơ sở được công nhận trong quy định.

```json
{"qid": "tD-da_buoc-002", "question": "Tôi là tài xế công nghệ, muốn biết thời gian bồi dưỡng cần bao lâu khi tham gia tại cơ sở được phép?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Bạn phải tham gia bồi dưỡng tại một cơ sở được công nhận. Chương trình bồi dưỡng kéo dài 32 giờ, bao gồm 12 giờ về pháp luật, 5 giờ về báo hiệu, 3 giờ về tốc độ, 4 giờ về xử vi phạm, 3 giờ về đăng ký, biển số và kiểm định, và 5 giờ ôn tập.", "gold_units": ["TT14-2025-BXD/D19/K2", "TT14-2025-BXD/D17/K1"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-002:2"}
```

### WD-da_buoc-003 · tier A · vai: tài xế công nghệ · kiểu: tinh_huong_nguoi_khac · DAN_CHIEU → TT65-2024-BCA/D5

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Thông tư số 65/2024/TT-BCA (Quy định kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ để được phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: TT65-2024-BCA/D8/K1

Điều 8. Trách nhiệm của cơ quan có thẩm quyền kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ
1. Bảo đảm điều kiện tổ chức kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ theo quy định tại Điều 5 Thông tư này.

### Điều khoản được nguồn trên dẫn chiếu tới (TT65-2024-BCA/D5)
Mã điều khoản dùng được cho gold_units: TT65-2024-BCA/D5

Điều 5. Bảo đảm điều kiện tổ chức kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ

### Nguồn 2
Văn bản: Thông tư số 65/2024/TT-BCA (Quy định kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ để được phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: TT65-2024-BCA/D5/K1, TT65-2024-BCA/D5/K1/a, TT65-2024-BCA/D5/K1/b, TT65-2024-BCA/D5/K1/c

Điều 5. Bảo đảm điều kiện tổ chức kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ
1. Bảo đảm về cơ sở vật chất, thiết bị thuộc quyền sử dụng của cơ quan có thẩm quyền kiểm tra:
a) Có phòng kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ, được trang bị máy tính, máy in dùng cho cán bộ thực hiện nhiệm vụ kiểm tra và cơ sở vật chất, thiết bị cần thiết trực tiếp phục vụ việc kiểm tra; máy tính để người dự kiểm tra sử dụng có kết nối mạng WAN Bộ Công an đến máy chủ đặt tại Cục Cảnh sát giao thông;
Máy chủ có cài đặt phần mềm kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ được Bộ Công an phê duyệt được kết nối với máy tính tại các điểm kiểm tra và phải bảo đảm an ninh, an toàn dữ liệu các máy tính sử dụng để phục vụ kiểm tra, lưu trữ nhật ký kết nối, chỉnh sửa dữ liệu.
b) Có hệ thống camera giám sát được toàn bộ hình ảnh phòng kiểm tra, có thiết bị lưu trữ dữ liệu hình ảnh camera. Hệ thống camera giám sát phải đảm bảo tính bảo mật, ngăn chặn các truy cập trái phép từ bên ngoài;
c) Trường hợp máy tính tại nơi kiểm tra chưa có kết nối mạng WAN theo quy định tại điểm a khoản 1 Điều này thì cơ quan có thẩm quyền kiểm tra sử dụng thiết bị có chức năng lưu trữ thông tin bảo đảm an ninh, an toàn để lưu trữ thông tin của người dự kiểm tra phục vụ việc tổ chức kiểm tra.

### Nguồn 3
Văn bản: Thông tư số 65/2024/TT-BCA (Quy định kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ để được phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: TT65-2024-BCA/D5/K2

Điều 5. Bảo đảm điều kiện tổ chức kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ
2. Cán bộ được giao nhiệm vụ kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ phải có giấy phép lái xe mô tô hạng A và giấy phép lái xe ô tô, được Cục Cảnh sát giao thông tổ chức tập huấn, cấp thẻ Sát hạch viên.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Công ty tôi muốn tổ chức kiểm tra kiến thức pháp luật, nhưng phòng không có máy tính có kết nối WAN, liệu có được phép thực hiện không?
- Đáp: Không được phép thực hiện nếu phòng không có máy tính có kết nối WAN. Để tổ chức kiểm tra, phòng cần trang bị máy tính, máy in và máy tính dùng cho người dự kiểm tra phải có kết nối mạng WAN Bộ Công an đến máy chủ đặt tại Cục Cảnh sát giao thông.
- ⚠ chep_nguyen_van: “chức kiểm tra kiến thức pháp …”
- Ghi chú: Giả định phòng kiểm tra chưa có máy tính có kết nối WAN.

```json
{"qid": "tD-da_buoc-003", "question": "Công ty tôi muốn tổ chức kiểm tra kiến thức pháp luật, nhưng phòng không có máy tính có kết nối WAN, liệu có được phép thực hiện không?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Không được phép thực hiện nếu phòng không có máy tính có kết nối WAN. Để tổ chức kiểm tra, phòng cần trang bị máy tính, máy in và máy tính dùng cho người dự kiểm tra phải có kết nối mạng WAN Bộ Công an đến máy chủ đặt tại Cục Cảnh sát giao thông.", "gold_units": ["TT65-2024-BCA/D8/K1", "TT65-2024-BCA/D5/K1/a"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-003:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Công ty tôi muốn tổ chức kiểm tra, nhưng nhân viên chỉ có giấy phép lái xe ô tô, không có giấy phép mô tô hạng A, liệu có được phép thực hiện không?
- Đáp: Không được phép thực hiện nếu nhân viên chỉ có giấy phép lái xe ô tô. Để thực hiện kiểm tra, cán bộ phải có giấy phép lái xe mô tô hạng A và giấy phép lái xe ô tô, được Cục Cảnh sát giao thông tổ chức tập huấn, cấp thẻ Sát hạch viên.
- ⚠ chep_nguyen_van: “giấy phép lái xe ô tô …”
- Ghi chú: Giả định nhân viên chỉ có giấy phép ô tô.

```json
{"qid": "tD-da_buoc-003", "question": "Công ty tôi muốn tổ chức kiểm tra, nhưng nhân viên chỉ có giấy phép lái xe ô tô, không có giấy phép mô tô hạng A, liệu có được phép thực hiện không?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Không được phép thực hiện nếu nhân viên chỉ có giấy phép lái xe ô tô. Để thực hiện kiểm tra, cán bộ phải có giấy phép lái xe mô tô hạng A và giấy phép lái xe ô tô, được Cục Cảnh sát giao thông tổ chức tập huấn, cấp thẻ Sát hạch viên.", "gold_units": ["TT65-2024-BCA/D8/K1", "TT65-2024-BCA/D5/K2"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-003:2"}
```

### WD-da_buoc-004 · tier A · vai: sinh viên đi xe máy · kiểu: tinh_huong_ban_than · DAN_CHIEU → TT14-2025-BXD/D25/K1/b

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Thông tư số 14/2025/TT-BXD (Quy định về đào tạo lái xe; bồi dưỡng, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ)
Hiệu lực của trạng thái này: 2026-07-01 → nay
Mã điều khoản dùng được cho gold_units: TT14-2025-BXD/D30/K2, TT14-2025-BXD/D30/K2/a, TT14-2025-BXD/D30/K2/b, TT14-2025-BXD/D30/K2/c, TT14-2025-BXD/D30/K2/d, TT14-2025-BXD/D30/K2/đ, TT14-2025-BXD/D30/K2/e

Điều 30. Cơ sở đào tạo lái xe
2. Đối với công tác quản lý hệ thống thông tin:
a) Đầu tư, bảo trì, nâng cấp Hệ thống thông tin quản lý, giám sát đào tạo lái xe tại cơ sở đào tạo lái xe; tiếp nhận, tổ chức thực hiện phần mềm ứng dụng phục vụ công tác quản lý, giám sát đào tạo lái xe tại cơ sở đào tạo lái xe do Cục Đường bộ Việt Nam chuyển giao và thực hiện truyền đầy đủ dữ liệu quy định tại các điểm a, điểm b, điểm g và điểm h khoản 1 Điều 25 về Sở Xây dựng;
b) Vận hành Hệ thống thông tin quản lý, giám sát đào tạo lái xe tại cơ sở đào tạo lái xe theo quy định;
c) Tạo lập, đối chiếu, chịu trách nhiệm về tính chính xác của thông tin học viên, quá trình đào tạo, kết quả đào tạo, báo cáo đăng ký khóa đào tạo lái xe theo quy định;
d) Lưu trữ đầy đủ các thông tin theo quy định tại khoản 1 Điều 27 Thông tư này và quy định của pháp luật về lưu trữ;
đ) Ban hành quy chế vận hành và bảo đảm an toàn, an ninh thông tin; quy chế sử dụng tài khoản và khai thác dữ liệu đối với hệ thống thông tin của cơ sở đào tạo và các hệ thống thông tin được chia sẻ theo các quy định của pháp luật về công nghệ thông tin và an toàn thông tin mạng;
e) Cung cấp dữ liệu trên Hệ thống thông tin quản lý, giám sát đào tạo lái xe tại cơ sở đào tạo lái xe để phục vụ công tác thanh tra, kiểm tra và cung cấp thông tin cho các cơ quan chức năng khi có yêu cầu.

### Điều khoản được nguồn trên dẫn chiếu tới (TT14-2025-BXD/D25/K1/a)
Mã điều khoản dùng được cho gold_units: TT14-2025-BXD/D25/K1/a

Điều 25. Yêu cầu đối với Hệ thống thông tin về đào tạo lái xe, chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ
1. Hệ thống thông tin quản lý, giám sát đào tạo lái xe tại cơ sở đào tạo lái xe:
a) Quản lý tối thiểu các thông tin của học viên: mã học viên (được tạo lập theo nguyên tắc quy định tại Phụ lục XXVII ban hành kèm theo Thông tư này); họ, tên; số định danh cá nhân; ngày, tháng, năm sinh; quốc tịch; nơi thường trú; số giấy phép lái xe (đối với trường hợp nâng hạng); số giấy xác nhận hoàn thành khóa đào tạo (được tạo lập theo nguyên tắc quy định tại Phụ lục XXVII ban hành kèm theo Thông tư này); khóa đào tạo; hạng xe đào tạo; thời gian lái xe an toàn đối với trường hợp nâng hạng giấy phép lái xe; tên cơ sở đào tạo lái xe; ảnh chân dung;

### Điều khoản được nguồn trên dẫn chiếu tới (TT14-2025-BXD/D25/K1/b)
Mã điều khoản dùng được cho gold_units: TT14-2025-BXD/D25/K1/b

Điều 25. Yêu cầu đối với Hệ thống thông tin về đào tạo lái xe, chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ
1. Hệ thống thông tin quản lý, giám sát đào tạo lái xe tại cơ sở đào tạo lái xe:
b) Quản lý tối thiểu thông tin về khóa đào tạo: số, ngày, tháng, năm báo cáo đăng ký khóa đào tạo lái xe, mã khóa đào tạo lái xe (được tạo lập theo nguyên tắc quy định tại Phụ lục XXVII ban hành kèm theo Thông tư này), hệ đào tạo lái xe (đào tạo mới hoặc nâng hạng), hạng đào tạo lái xe, số lượng học viên, hình thức học của học viên, ngày khai giảng, ngày bế giảng;

### Điều khoản được nguồn trên dẫn chiếu tới (TT14-2025-BXD/D25/K1/g)
Mã điều khoản dùng được cho gold_units: TT14-2025-BXD/D25/K1/g

Điều 25. Yêu cầu đối với Hệ thống thông tin về đào tạo lái xe, chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ
1. Hệ thống thông tin quản lý, giám sát đào tạo lái xe tại cơ sở đào tạo lái xe:
g) Có chức năng lập và cung cấp cho Sở Xây dựng báo cáo đăng ký khóa đào tạo lái xe;

### Nguồn 2
Văn bản: Thông tư số 14/2025/TT-BXD (Quy định về đào tạo lái xe; bồi dưỡng, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ)
Hiệu lực của trạng thái này: 2025-09-01 → nay
Mã điều khoản dùng được cho gold_units: TT14-2025-BXD/D25/K1, TT14-2025-BXD/D25/K1/a, TT14-2025-BXD/D25/K1/b, TT14-2025-BXD/D25/K1/c, TT14-2025-BXD/D25/K1/d, TT14-2025-BXD/D25/K1/đ, TT14-2025-BXD/D25/K1/e, TT14-2025-BXD/D25/K1/g, TT14-2025-BXD/D25/K1/h, TT14-2025-BXD/D25/K1/i, TT14-2025-BXD/D25/K1/k, TT14-2025-BXD/D25/K1/l, TT14-2025-BXD/D25/K1/m

Điều 25. Yêu cầu đối với Hệ thống thông tin về đào tạo lái xe, chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ
1. Hệ thống thông tin quản lý, giám sát đào tạo lái xe tại cơ sở đào tạo lái xe:
a) Quản lý tối thiểu các thông tin của học viên: mã học viên (được tạo lập theo nguyên tắc quy định tại Phụ lục XXVII ban hành kèm theo Thông tư này); họ, tên; số định danh cá nhân; ngày, tháng, năm sinh; quốc tịch; nơi thường trú; số giấy phép lái xe (đối với trường hợp nâng hạng); số giấy xác nhận hoàn thành khóa đào tạo (được tạo lập theo nguyên tắc quy định tại Phụ lục XXVII ban hành kèm theo Thông tư này); khóa đào tạo; hạng xe đào tạo; thời gian lái xe an toàn đối với trường hợp nâng hạng giấy phép lái xe; tên cơ sở đào tạo lái xe; ảnh chân dung;
b) Quản lý tối thiểu thông tin về khóa đào tạo: số, ngày, tháng, năm báo cáo đăng ký khóa đào tạo lái xe, mã khóa đào tạo lái xe (được tạo lập theo nguyên tắc quy định tại Phụ lục XXVII ban hành kèm theo Thông tư này), hệ đào tạo lái xe (đào tạo mới hoặc nâng hạng), hạng đào tạo lái xe, số lượng học viên, hình thức học của học viên, ngày khai giảng, ngày bế giảng;
c) Quản lý tối thiểu các thông tin học lái xe của học viên: kết quả đào tạo (bao gồm kết quả kiểm tra kết thúc nội dung đào tạo lý thuyết và kiểm tra kết thúc nội dung đào tạo thực hành lái xe); dữ liệu DAT; thời gian học lý thuyết môn học pháp luật về giao thông đường bộ; kết quả học thực hành lái xe trên cabin học lái xe;
…

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là học viên muốn đăng ký khóa lái xe máy, hệ thống quản lý tại cơ sở đào tạo cần lưu trữ những thông tin gì về bản thân và khóa học?
- Đáp: Hệ thống phải ghi lại mã học viên, họ tên, số định danh cá nhân, ngày sinh, quốc tịch, nơi thường trú, số giấy phép lái xe (nếu nâng hạng), số giấy xác nhận hoàn thành khóa đào tạo, khóa đào tạo, hạng xe đào tạo, thời gian lái xe an toàn (nếu nâng hạng), tên cơ sở đào tạo và ảnh chân dung. Ngoài ra, hệ thống cũng phải quản lý số, ngày, tháng, năm báo cáo đăng ký khóa, mã khóa đào tạo, hệ đào tạo (mới hoặc nâng hạng), hạng đào tạo, số lượng học viên, hình thức học, ngày khai giảng và ngày bế giảng.
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-da_buoc-004", "question": "Tôi là học viên muốn đăng ký khóa lái xe máy, hệ thống quản lý tại cơ sở đào tạo cần lưu trữ những thông tin gì về bản thân và khóa học?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Hệ thống phải ghi lại mã học viên, họ tên, số định danh cá nhân, ngày sinh, quốc tịch, nơi thường trú, số giấy phép lái xe (nếu nâng hạng), số giấy xác nhận hoàn thành khóa đào tạo, khóa đào tạo, hạng xe đào tạo, thời gian lái xe an toàn (nếu nâng hạng), tên cơ sở đào tạo và ảnh chân dung. Ngoài ra, hệ thống cũng phải quản lý số, ngày, tháng, năm báo cáo đăng ký khóa, mã khóa đào tạo, hệ đào tạo (mới hoặc nâng hạng), hạng đào tạo, số lượng học viên, hình thức học, ngày khai giảng và ngày bế giảng.", "gold_units": ["TT14-2025-BXD/D25/K1/a", "TT14-2025-BXD/D25/K1/b"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-004:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là giảng viên tại một cơ sở đào tạo lái xe, hệ thống quản lý cần lưu trữ những dữ liệu nào về học viên và khóa học để đáp ứng quy định?
- Đáp: Hệ thống phải lưu trữ mã học viên, họ tên, số định danh cá nhân, ngày sinh, quốc tịch, nơi thường trú, số giấy phép lái xe (nếu nâng hạng), số giấy xác nhận hoàn thành khóa đào tạo, khóa đào tạo, hạng xe đào tạo, thời gian lái xe an toàn (nếu nâng hạng), tên cơ sở đào tạo và ảnh chân dung. Đồng thời, cần quản lý số, ngày, tháng, năm báo cáo đăng ký khóa, mã khóa đào tạo, hệ đào tạo (mới hoặc nâng hạng), hạng đào tạo, số lượng học viên, hình thức học, ngày khai giảng và ngày bế giảng.
- ⚠ chep_nguyen_van: “cơ sở đào tạo lái xe …”
- Ghi chú: Giả định rằng cơ sở đào tạo là cơ sở hợp pháp và đã được cấp phép

```json
{"qid": "tD-da_buoc-004", "question": "Tôi là giảng viên tại một cơ sở đào tạo lái xe, hệ thống quản lý cần lưu trữ những dữ liệu nào về học viên và khóa học để đáp ứng quy định?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Hệ thống phải lưu trữ mã học viên, họ tên, số định danh cá nhân, ngày sinh, quốc tịch, nơi thường trú, số giấy phép lái xe (nếu nâng hạng), số giấy xác nhận hoàn thành khóa đào tạo, khóa đào tạo, hạng xe đào tạo, thời gian lái xe an toàn (nếu nâng hạng), tên cơ sở đào tạo và ảnh chân dung. Đồng thời, cần quản lý số, ngày, tháng, năm báo cáo đăng ký khóa, mã khóa đào tạo, hệ đào tạo (mới hoặc nâng hạng), hạng đào tạo, số lượng học viên, hình thức học, ngày khai giảng và ngày bế giảng.", "gold_units": ["TT14-2025-BXD/D25/K1/a", "TT14-2025-BXD/D25/K1/b"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-004:2"}
```

### WD-da_buoc-005 · tier A · vai: người lớn tuổi đi xe đạp điện · kiểu: tinh_huong_ban_than · DAN_CHIEU → TT65-2024-BCA/D4

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Thông tư số 65/2024/TT-BCA (Quy định kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ để được phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: TT65-2024-BCA/D7/K3

Điều 7. Đăng ký, tổ chức kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ
3. Người đăng ký kiểm tra có thể nộp hồ sơ cho cơ quan có thẩm quyền kiểm tra quy định tại Điều 4 Thông tư này tại nơi thường trú, tạm trú, nơi ở hiện tại.
Người có kết quả kiểm tra không đạt yêu cầu có thể đăng ký kiểm tra lại tại cơ quan có thẩm quyền đã tổ chức kiểm tra trước đó hoặc lựa chọn cơ quan có thẩm quyền kiểm tra để đề nghị kiểm tra lại. Trường hợp đề nghị kiểm tra lại, nếu giấy khám sức khỏe còn giá trị sử dụng thì người đăng ký kiểm tra chỉ gửi đơn đề nghị kiểm tra.

### Điều khoản được nguồn trên dẫn chiếu tới (TT65-2024-BCA/D4)
Mã điều khoản dùng được cho gold_units: TT65-2024-BCA/D4

Điều 4. Cơ quan có thẩm quyền kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ
Cơ quan có thẩm quyền kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ:

### Nguồn 2
Văn bản: Thông tư số 65/2024/TT-BCA (Quy định kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ để được phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: TT65-2024-BCA/D4/K1

Điều 4. Cơ quan có thẩm quyền kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ
1. Cục Cảnh sát giao thông.

### Nguồn 3
Văn bản: Thông tư số 65/2024/TT-BCA (Quy định kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ để được phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: TT65-2024-BCA/D4/K2

Điều 4. Cơ quan có thẩm quyền kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ
2. Phòng Cảnh sát giao thông Công an tỉnh, thành phố trực thuộc trung ương.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là người lớn tuổi đi xe đạp điện, muốn đăng ký kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông, tôi phải nộp hồ sơ ở đâu và cơ quan nào có thẩm quyền thực hiện kiểm tra?
- Đáp: Bạn cần nộp hồ sơ đăng ký kiểm tra tại cơ quan có thẩm quyền tại nơi thường trú, tạm trú hoặc nơi ở hiện tại. Cơ quan có thẩm quyền thực hiện kiểm tra là Cục Cảnh sát giao thông. (khoản 3 Điều 7 Thông tư 65/2024/TT-BCA; khoản 1 Điều 4 Thông tư 65/2024/TT-BCA)
- ⚠ chep_nguyen_van: “kiến thức pháp luật về trật …”

```json
{"qid": "tD-da_buoc-005", "question": "Tôi là người lớn tuổi đi xe đạp điện, muốn đăng ký kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông, tôi phải nộp hồ sơ ở đâu và cơ quan nào có thẩm quyền thực hiện kiểm tra?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Bạn cần nộp hồ sơ đăng ký kiểm tra tại cơ quan có thẩm quyền tại nơi thường trú, tạm trú hoặc nơi ở hiện tại. Cơ quan có thẩm quyền thực hiện kiểm tra là Cục Cảnh sát giao thông. (khoản 3 Điều 7 Thông tư 65/2024/TT-BCA; khoản 1 Điều 4 Thông tư 65/2024/TT-BCA)", "gold_units": ["TT65-2024-BCA/D7/K3", "TT65-2024-BCA/D4/K1"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-005:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là người lớn tuổi đi xe đạp điện, muốn đăng ký kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông, tôi phải nộp hồ sơ ở đâu và cơ quan nào có thẩm quyền thực hiện kiểm tra?
- Đáp: Bạn cần nộp hồ sơ đăng ký kiểm tra tại cơ quan có thẩm quyền tại nơi thường trú, tạm trú hoặc nơi ở hiện tại. Cơ quan có thẩm quyền thực hiện kiểm tra là Phòng Cảnh sát giao thông Công an tỉnh, thành phố trực thuộc trung ương. (khoản 3 Điều 7 Thông tư 65/2024/TT-BCA; khoản 2 Điều 4 Thông tư 65/2024/TT-BCA)
- ⚠ chep_nguyen_van: “kiến thức pháp luật về trật …”

```json
{"qid": "tD-da_buoc-005", "question": "Tôi là người lớn tuổi đi xe đạp điện, muốn đăng ký kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông, tôi phải nộp hồ sơ ở đâu và cơ quan nào có thẩm quyền thực hiện kiểm tra?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Bạn cần nộp hồ sơ đăng ký kiểm tra tại cơ quan có thẩm quyền tại nơi thường trú, tạm trú hoặc nơi ở hiện tại. Cơ quan có thẩm quyền thực hiện kiểm tra là Phòng Cảnh sát giao thông Công an tỉnh, thành phố trực thuộc trung ương. (khoản 3 Điều 7 Thông tư 65/2024/TT-BCA; khoản 2 Điều 4 Thông tư 65/2024/TT-BCA)", "gold_units": ["TT65-2024-BCA/D7/K3", "TT65-2024-BCA/D4/K2"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-005:2"}
```

### WD-da_buoc-006 · tier A · vai: người lớn tuổi đi xe đạp điện · kiểu: nhieu_dieu_kien · DAN_CHIEU → LUAT36-2024/D12

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Thông tư số 38/2024/TT-BGTVT (Quy định về tốc độ và khoảng cách an toàn của xe cơ giới, xe máy chuyên dùng tham gia giao thông trên đường bộ)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: TT38-2024-BGTVT/D4/K1

Điều 4. Nguyên tắc chấp hành quy định về tốc độ khai thác và khoảng cách an toàn khi điều khiển phương tiện trên đường bộ
1. Khi tham gia giao thông trên đường bộ, người lái xe, người điều khiển xe máy chuyên dùng phải chấp hành quy định về tốc độ khai thác và khoảng cách an toàn theo quy định tại Điều 12 Luật Trật tự, an toàn giao thông đường bộ.

### Điều khoản được nguồn trên dẫn chiếu tới (LUAT36-2024/D12)
Mã điều khoản dùng được cho gold_units: LUAT36-2024/D12

Điều 12. Chấp hành quy định về tốc độ và khoảng cách giữa các xe

### Nguồn 2
Văn bản: Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: LUAT36-2024/D12/K1

Điều 12. Chấp hành quy định về tốc độ và khoảng cách giữa các xe
1. Người lái xe, người điều khiển xe máy chuyên dùng phải chấp hành quy định về tốc độ, khoảng cách an toàn tối thiểu với xe phía trước cùng làn đường hoặc phần đường.

### Nguồn 3
Văn bản: Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: LUAT36-2024/D12/K2

Điều 12. Chấp hành quy định về tốc độ và khoảng cách giữa các xe
2. Người điều khiển phương tiện tham gia giao thông đường bộ phải bảo đảm tốc độ phù hợp điều kiện của cầu, đường, mật độ giao thông, địa hình, thời tiết và các yếu tố ảnh hưởng khác để bảo đảm an toàn.

### Nguồn 4
Văn bản: Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: LUAT36-2024/D12/K3, LUAT36-2024/D12/K3/a, LUAT36-2024/D12/K3/b, LUAT36-2024/D12/K3/c, LUAT36-2024/D12/K3/d, LUAT36-2024/D12/K3/đ, LUAT36-2024/D12/K3/e, LUAT36-2024/D12/K3/g, LUAT36-2024/D12/K3/h, LUAT36-2024/D12/K3/i, LUAT36-2024/D12/K3/k, LUAT36-2024/D12/K3/l, LUAT36-2024/D12/K3/m, LUAT36-2024/D12/K3/n

Điều 12. Chấp hành quy định về tốc độ và khoảng cách giữa các xe
3. Người điều khiển phương tiện tham gia giao thông đường bộ phải quan sát, giảm tốc độ hoặc dừng lại để bảo đảm an toàn trong các trường hợp sau đây:
a) Tại nơi có vạch kẻ đường hoặc báo hiệu khác dành cho người đi bộ hoặc tại nơi mà người đi bộ, xe lăn của người khuyết tật đang qua đường;
b) Có báo hiệu cảnh báo nguy hiểm hoặc có chướng ngại vật trên đường;
c) Chuyển hướng xe chạy hoặc tầm nhìn bị hạn chế;
d) Nơi đường bộ giao nhau cùng mức với đường bộ, đường bộ giao nhau cùng mức với đường sắt; đường hẹp, đường vòng, đường quanh co, đường đèo, dốc;
đ) Nơi cầu, cống hẹp, đập tràn, đường ngầm, hầm chui, hầm đường bộ;
e) Khu vực có trường học, bệnh viện, bến xe, công trình công cộng tập trung đông người, khu vực đông dân cư, chợ, khu vực đang thi công trên đường bộ, hiện trường vụ tai nạn giao thông đường bộ;
g) Có vật nuôi đi trên đường hoặc chăn thả ở ven đường;
h) Tránh xe đi ngược chiều hoặc khi cho xe đi phía sau vượt; khi có tín hiệu xin đường, tín hiệu khẩn cấp của xe đi cùng chiều phía trước;
i) Điểm dừng xe, đỗ xe trên đường bộ có khách đang lên, xuống xe;
k) Gặp xe vận chuyển hàng siêu trường, siêu trọng, hàng hóa nguy hiểm; đoàn người đi bộ;
l) Gặp xe ưu tiên;
m) Điều kiện trời mưa, gió, sương, khói, bụi, mặt đường trơn trượt, lầy lội, có nhiều đất đá, vật liệu rơi vãi ảnh hưởng đến an toàn giao thông đường bộ;
n) Khu vực đang tổ chức kiểm soát giao thông đường bộ.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là người lớn tuổi, đang đi xe đạp điện trên đường chính, tốc độ 20 km/h và giữ khoảng cách 1,5 m với xe hơi phía trước. Có được phép đi như vậy không?
- Đáp: Bạn có thể đi xe đạp điện với tốc độ 20 km/h và giữ khoảng cách 1,5 m với xe hơi phía trước, vì điều này tuân thủ quy định về tốc độ khai thác và khoảng cách an toàn. Tuy nhiên, bạn vẫn phải đảm bảo tốc độ phù hợp với điều kiện đường và giao thông, đồng thời giữ khoảng cách an toàn tối thiểu với xe phía trước. (Điều 4 Khoản 1 Thông tư 38/2024/TT-BGTVT và Điều 12 Khoản 1 Luật 36/2024/QH15)
- ⚠ so_la: 1.5, 20

```json
{"qid": "tD-da_buoc-006", "question": "Tôi là người lớn tuổi, đang đi xe đạp điện trên đường chính, tốc độ 20 km/h và giữ khoảng cách 1,5 m với xe hơi phía trước. Có được phép đi như vậy không?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Bạn có thể đi xe đạp điện với tốc độ 20 km/h và giữ khoảng cách 1,5 m với xe hơi phía trước, vì điều này tuân thủ quy định về tốc độ khai thác và khoảng cách an toàn. Tuy nhiên, bạn vẫn phải đảm bảo tốc độ phù hợp với điều kiện đường và giao thông, đồng thời giữ khoảng cách an toàn tối thiểu với xe phía trước. (Điều 4 Khoản 1 Thông tư 38/2024/TT-BGTVT và Điều 12 Khoản 1 Luật 36/2024/QH15)", "gold_units": ["TT38-2024-BGTVT/D4/K1", "LUAT36-2024/D12/K1"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-006:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là người lớn tuổi, đang đi xe đạp điện trong khu vực trường học, tốc độ 15 km/h và giữ khoảng cách 1 m với xe tải. Tôi có thể tiếp tục đi không?
- Đáp: Bạn nên giảm tốc độ hoặc dừng lại khi đi qua khu vực trường học, vì điều này yêu cầu quan sát và giảm tốc độ để đảm bảo an toàn. Đồng thời, bạn phải giữ khoảng cách an toàn tối thiểu với xe tải phía trước và tuân thủ tốc độ phù hợp với điều kiện đường. (Điều 12 Khoản 3(a) Luật 36/2024/QH15 và Điều 12 Khoản 1 Luật 36/2024/QH15)

```json
{"qid": "tD-da_buoc-006", "question": "Tôi là người lớn tuổi, đang đi xe đạp điện trong khu vực trường học, tốc độ 15 km/h và giữ khoảng cách 1 m với xe tải. Tôi có thể tiếp tục đi không?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Bạn nên giảm tốc độ hoặc dừng lại khi đi qua khu vực trường học, vì điều này yêu cầu quan sát và giảm tốc độ để đảm bảo an toàn. Đồng thời, bạn phải giữ khoảng cách an toàn tối thiểu với xe tải phía trước và tuân thủ tốc độ phù hợp với điều kiện đường. (Điều 12 Khoản 3(a) Luật 36/2024/QH15 và Điều 12 Khoản 1 Luật 36/2024/QH15)", "gold_units": ["TT38-2024-BGTVT/D4/K1", "LUAT36-2024/D12/K1"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-006:2"}
```

### WD-da_buoc-008 · tier A · vai: cán bộ phường · kiểu: tinh_huong_ban_than · DAN_CHIEU → TT79-2024-BCA/D4

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D20/K3, TT79-2024-BCA/D20/K3/a, TT79-2024-BCA/D20/K3/b

Điều 20. Thủ tục đổi chứng nhận đăng ký xe, biển số xe
3. Đối với trường hợp đổi chứng nhận đăng ký xe khi chủ xe thay đổi trụ sở, nơi cư trú đến địa chỉ mới ngoài phạm vi của cơ quan đăng ký xe đã cấp chứng nhận đăng ký xe đó:
a) Chủ xe nộp chứng nhận đăng ký xe và đơn đề nghị xác nhận hồ sơ xe (theo mẫu ĐKX13 ban hành kèm theo Thông tư này) cho cơ quan đăng ký xe quản lý hồ sơ xe đó để được cấp giấy xác nhận hồ sơ xe;
b) Chủ xe kê khai giấy khai đăng ký xe và nộp giấy xác nhận hồ sơ xe cho cơ quan đăng ký xe tại địa chỉ mới theo quy định tại Điều 4 Thông tư này để đổi chứng nhận đăng ký xe.

### Điều khoản được nguồn trên dẫn chiếu tới (TT79-2024-BCA/D4)
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D4

Điều 4. Cơ quan đăng ký xe

### Nguồn 2
Văn bản: Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)
Hiệu lực của trạng thái này: 2025-01-01 → 2025-02-28
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D4/K3

Điều 4. Cơ quan đăng ký xe
3. Công an cấp huyện đăng ký các loại xe: Xe mô tô đăng ký biển số xe trúng đấu giá; xe ô tô, xe máy chuyên dùng, xe mô tô của tổ chức, cá nhân trong nước có trụ sở, cư trú tại địa phương (trừ các loại xe quy định tại khoản 1, khoản 2, khoản 4 Điều này).

### Nguồn 3
Văn bản: Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D4/K1

Điều 4. Cơ quan đăng ký xe
1. Cục Cảnh sát giao thông đăng ký xe của các đơn vị thuộc cơ quan Bộ Công an; xe ô tô, xe máy chuyên dùng của các cơ quan, tổ chức quy định tại Phụ lục số 01 ban hành kèm theo Thông tư này; xe ô tô của cơ quan đại diện ngoại giao, cơ quan đại diện của tổ chức quốc tế có trụ sở tại thành phố Hà Nội và xe ô tô của người nước ngoài làm việc trong cơ quan đó.

### Điều khoản được nguồn trên dẫn chiếu tới (TT79-2024-BCA/PL1)
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/PL1

PHỤ LỤC 01
CÁC CƠ QUAN, ĐƠN VỊ ĐĂNG KÝ XE Ô TÔ, XE MÁY CHUYÊN DÙNG TẠI CỤC CẢNH SÁT GIAO THÔNG
(Ban hành kèm theo Thông tư số 79/2024/TT-BCA ngày 15/11/2024 của Bộ trưởng Bộ Công an)
STT | TÊN CƠ QUAN, ĐƠN VỊ
1 | Văn phòng và các Ban của Trung ương Đảng
2 | Văn phòng Chủ tịch nước
3 | Văn phòng Quốc hội
4 | Văn phòng các Bộ, cơ quan ngang Bộ, các cơ quan thuộc Chính phủ
5 | Văn phòng cơ quan Trung ương các tổ chức chính trị-xã hội (Mặt trận Tổ quốc Việt Nam, Công đoàn Việt Nam, Đoàn Thanh niên Cộng sản Hồ Chí Minh, Hội Liên hiệp Phụ nữ Việt Nam, Hội Cựu chiến binh Việt Nam, Hội Nông dân Việt Nam
6 | Văn phòng Viện Kiểm sát nhân dân tối cao
7 | Văn phòng Toà án nhân dân tối cao
8 | Văn phòng Kiểm toán Nhà nước

### Nguồn 4
Văn bản: Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)
Hiệu lực của trạng thái này: 2025-03-01 → nay
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D4/K2, TT79-2024-BCA/D4/K2/a, TT79-2024-BCA/D4/K2/b, TT79-2024-BCA/D4/K2/c, TT79-2024-BCA/D4/K2/d

Điều 4. Cơ quan đăng ký xe
2. Phòng Cảnh sát giao thông đăng ký các loại xe sau đây (trừ các loại xe quy định tại khoản 1 Điều này):
a) Xe ô tô, rơmoóc, sơ mi rơmoóc, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ, các loại xe có kết cấu tương tự xe ô tô (sau đây viết gọn là xe ô tô) và xe máy chuyên dùng của tổ chức, cá nhân có trụ sở, cư trú tại quận, thành phố thuộc thành phố trực thuộc Trung ương hoặc tại thành phố, huyện, thị xã thuộc tỉnh nơi Phòng Cảnh sát giao thông đặt trụ sở;
b) Xe ô tô, xe mô tô, xe gắn máy đăng ký gắn biển số xe trúng đấu giá;
c) Xe có nguồn gốc tịch thu, xe mô tô có dung tích xi lanh từ 175 cm3 trở lên;
d) Xe ô tô, xe máy chuyên dùng, xe mô tô, xe gắn máy và các loại xe có kết cấu tương tự xe mô tô (sau đây viết gọn là xe mô tô) của tổ chức, cá nhân nước ngoài.

### Điều khoản được nguồn trên dẫn chiếu tới (TT79-2024-BCA/D4/K1)
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D4/K1

Điều 4. Cơ quan đăng ký xe
1. Cục Cảnh sát giao thông đăng ký xe của các đơn vị thuộc cơ quan Bộ Công an; xe ô tô, xe máy chuyên dùng của các cơ quan, tổ chức quy định tại Phụ lục số 01 ban hành kèm theo Thông tư này; xe ô tô của cơ quan đại diện ngoại giao, cơ quan đại diện của tổ chức quốc tế có trụ sở tại thành phố Hà Nội và xe ô tô của người nước ngoài làm việc trong cơ quan đó.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi vừa chuyển trụ sở công ty sang quận 10, muốn đổi chứng nhận đăng ký xe ô tô của công ty. Tôi cần làm gì để hoàn thành thủ tục này?
- Đáp: Bạn phải nộp chứng nhận đăng ký xe và đơn đề nghị xác nhận hồ sơ xe cho cơ quan đăng ký xe quản lý hồ sơ hiện tại, sau đó kê khai giấy khai đăng ký xe và nộp giấy xác nhận hồ sơ xe cho cơ quan đăng ký xe tại địa chỉ mới để đổi chứng nhận đăng ký xe.
- ⚠ chep_nguyen_van: “đổi chứng nhận đăng ký xe …”

```json
{"qid": "tD-da_buoc-008", "question": "Tôi vừa chuyển trụ sở công ty sang quận 10, muốn đổi chứng nhận đăng ký xe ô tô của công ty. Tôi cần làm gì để hoàn thành thủ tục này?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Bạn phải nộp chứng nhận đăng ký xe và đơn đề nghị xác nhận hồ sơ xe cho cơ quan đăng ký xe quản lý hồ sơ hiện tại, sau đó kê khai giấy khai đăng ký xe và nộp giấy xác nhận hồ sơ xe cho cơ quan đăng ký xe tại địa chỉ mới để đổi chứng nhận đăng ký xe.", "gold_units": ["TT79-2024-BCA/D20/K3", "TT79-2024-BCA/D4"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-008:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Con tôi là chủ sở hữu xe máy chuyên dùng, chúng tôi chuyển trụ sở sang thành phố Hồ Chí Minh. Con tôi muốn đổi chứng nhận đăng ký xe, cần làm gì?
- Đáp: Con bạn phải nộp chứng nhận đăng ký xe và đơn đề nghị xác nhận hồ sơ xe cho cơ quan đăng ký xe quản lý hồ sơ hiện tại, sau đó kê khai giấy khai đăng ký xe và nộp giấy xác nhận hồ sơ xe cho cơ quan đăng ký xe tại địa chỉ mới để đổi chứng nhận đăng ký xe.
- ⚠ chep_nguyen_van: “đổi chứng nhận đăng ký xe …”

```json
{"qid": "tD-da_buoc-008", "question": "Con tôi là chủ sở hữu xe máy chuyên dùng, chúng tôi chuyển trụ sở sang thành phố Hồ Chí Minh. Con tôi muốn đổi chứng nhận đăng ký xe, cần làm gì?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Con bạn phải nộp chứng nhận đăng ký xe và đơn đề nghị xác nhận hồ sơ xe cho cơ quan đăng ký xe quản lý hồ sơ hiện tại, sau đó kê khai giấy khai đăng ký xe và nộp giấy xác nhận hồ sơ xe cho cơ quan đăng ký xe tại địa chỉ mới để đổi chứng nhận đăng ký xe.", "gold_units": ["TT79-2024-BCA/D20/K3", "TT79-2024-BCA/D4"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-008:2"}
```

### WD-da_buoc-010 · tier A · vai: tài xế công nghệ · kiểu: tinh_huong_nguoi_khac · DAN_CHIEU → TT79-2024-BCA/D9

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)
Hiệu lực của trạng thái này: 2025-03-01 → nay
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D21/K2, TT79-2024-BCA/D21/K2/a, TT79-2024-BCA/D21/K2/b

Điều 21. Thủ tục cấp lại chứng nhận đăng ký xe, biển số xe
2. Chủ xe thực hiện dịch vụ công trực tuyến một phần hoặc làm thủ tục trực tiếp tại cơ quan đăng ký xe:
a) Chủ xe kê khai giấy khai đăng ký xe theo quy định tại Điều 9 Thông tư này, nộp hồ sơ theo quy định tại khoản 1 và khoản 2 Điều 19 Thông tư này và nộp lệ phí theo quy định;
b) Sau khi kiểm tra hồ sơ xe đảm bảo hợp lệ, cơ quan đăng ký xe thực hiện cấp lại chứng nhận đăng ký xe, biển số xe theo quy định; chủ xe nhận kết quả đăng ký xe tại cơ quan đăng ký xe hoặc từ dịch vụ bưu chính.

### Điều khoản được nguồn trên dẫn chiếu tới (TT79-2024-BCA/D19/K1)
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D19/K1

Điều 19. Hồ sơ đổi chứng nhận đăng ký xe, biển số xe
1. Giấy khai đăng ký xe.

### Điều khoản được nguồn trên dẫn chiếu tới (TT79-2024-BCA/D19/K2)
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D19/K2

Điều 19. Hồ sơ đổi chứng nhận đăng ký xe, biển số xe
2. Giấy tờ của chủ xe theo quy định tại Điều 10 Thông tư này.

### Điều khoản được nguồn trên dẫn chiếu tới (TT79-2024-BCA/D9)
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D9

Điều 9. Giấy khai đăng ký xe

### Nguồn 2
Văn bản: Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D9/K1

Điều 9. Giấy khai đăng ký xe
1. Trường hợp thực hiện đăng ký xe bằng dịch vụ công trực tuyến một phần: Chủ xe đăng nhập trên cổng dịch vụ công và kê khai chính xác, đầy đủ, trung thực các nội dung quy định trong mẫu giấy khai đăng ký xe, ký số. Trường hợp không có ký số thì chủ xe in giấy khai đăng ký xe từ cổng dịch vụ công, ký, ghi rõ họ, tên và đóng dấu (nếu là cơ quan, tổ chức).

### Nguồn 3
Văn bản: Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D9/K2

Điều 9. Giấy khai đăng ký xe
2. Trường hợp thực hiện đăng ký xe lần đầu bằng dịch vụ công trực tuyến toàn trình: Chủ xe sử dụng tài khoản định danh điện tử mức độ 2 để đăng nhập vào cổng dịch vụ công hoặc ứng dụng định danh quốc gia và kê khai chính xác, đầy đủ, trung thực các nội dung quy định trong mẫu giấy khai đăng ký xe và chủ xe không cần ký.

### Nguồn 4
Văn bản: Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D9/K3

Điều 9. Giấy khai đăng ký xe
3. Trường hợp thực hiện đăng ký xe trực tiếp tại cơ quan đăng ký xe: Chủ xe kê khai chính xác, đầy đủ, trung thực các nội dung quy định trong mẫu giấy khai đăng ký xe.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Anh tôi muốn đổi chứng nhận đăng ký xe, anh ấy đã nộp hồ sơ qua dịch vụ công trực tuyến một phần nhưng chưa nhận được kết quả. Anh ấy cần làm gì để hoàn tất thủ tục?
- Đáp: Anh ấy cần nộp hồ sơ gồm giấy khai đăng ký xe và giấy tờ của chủ xe theo quy định, đồng thời nộp lệ phí. Sau khi hồ sơ được kiểm tra hợp lệ, cơ quan đăng ký xe sẽ cấp lại chứng nhận đăng ký xe và biển số xe. (Điều 21.2.a, b và Điều 19.1, 2 Thông tư 79/2024/TT-BCA)
- ⚠ chep_nguyen_van: “dịch vụ công trực tuyến một …”
- Ghi chú: Giả định anh tôi đã nộp hồ sơ qua dịch vụ công trực tuyến một phần và chưa nhận kết quả

```json
{"qid": "tD-da_buoc-010", "question": "Anh tôi muốn đổi chứng nhận đăng ký xe, anh ấy đã nộp hồ sơ qua dịch vụ công trực tuyến một phần nhưng chưa nhận được kết quả. Anh ấy cần làm gì để hoàn tất thủ tục?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Anh ấy cần nộp hồ sơ gồm giấy khai đăng ký xe và giấy tờ của chủ xe theo quy định, đồng thời nộp lệ phí. Sau khi hồ sơ được kiểm tra hợp lệ, cơ quan đăng ký xe sẽ cấp lại chứng nhận đăng ký xe và biển số xe. (Điều 21.2.a, b và Điều 19.1, 2 Thông tư 79/2024/TT-BCA)", "gold_units": ["TT79-2024-BCA/D21/K2", "TT79-2024-BCA/D19/K1", "TT79-2024-BCA/D19/K2"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-010:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Công ty tôi muốn đăng ký xe mới lần đầu bằng dịch vụ công trực tuyến toàn trình, không cần ký số. Công ty cần làm gì để nhận chứng nhận đăng ký xe?
- Đáp: Công ty cần sử dụng tài khoản định danh điện tử mức độ 2 để đăng nhập vào cổng dịch vụ công, kê khai chính xác, đầy đủ, trung thực các nội dung trong mẫu giấy khai đăng ký xe, không cần ký. Sau đó nộp hồ sơ gồm giấy khai đăng ký xe và giấy tờ của chủ xe, cùng lệ phí. Khi hồ sơ được kiểm tra hợp lệ, cơ quan đăng ký xe cấp lại chứng nhận đăng ký xe và biển số xe. (Điều 9.2 và Điều 21.2.a, b Thông tư 79/2024/TT-BCA)
- ⚠ chep_nguyen_van: “bằng dịch vụ công trực tuyến …”
- Ghi chú: Giả định công ty sử dụng tài khoản định danh điện tử mức độ 2 và đăng ký xe lần đầu qua dịch vụ công trực tuyến toàn trình

```json
{"qid": "tD-da_buoc-010", "question": "Công ty tôi muốn đăng ký xe mới lần đầu bằng dịch vụ công trực tuyến toàn trình, không cần ký số. Công ty cần làm gì để nhận chứng nhận đăng ký xe?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Công ty cần sử dụng tài khoản định danh điện tử mức độ 2 để đăng nhập vào cổng dịch vụ công, kê khai chính xác, đầy đủ, trung thực các nội dung trong mẫu giấy khai đăng ký xe, không cần ký. Sau đó nộp hồ sơ gồm giấy khai đăng ký xe và giấy tờ của chủ xe, cùng lệ phí. Khi hồ sơ được kiểm tra hợp lệ, cơ quan đăng ký xe cấp lại chứng nhận đăng ký xe và biển số xe. (Điều 9.2 và Điều 21.2.a, b Thông tư 79/2024/TT-BCA)", "gold_units": ["TT79-2024-BCA/D9/K2", "TT79-2024-BCA/D21/K2", "TT79-2024-BCA/D19/K1", "TT79-2024-BCA/D19/K2"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-010:2"}
```

### WD-da_buoc-011 · tier A · vai: người lớn tuổi đi xe đạp điện · kiểu: tinh_huong_ban_than · DAN_CHIEU → TT36-2024-BYT/PL1

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Thông tư số 36/2024/TT-BYT (Quy định về tiêu chuẩn sức khỏe, việc khám sức khỏe đối với người lái xe, người điều khiển xe máy chuyên dùng; việc khám sức khỏe định kỳ đối với người hành nghề lái xe ô tô; cơ sở dữ liệu về sức khỏe của người lái xe, người điều khiển xe máy chuyên dùng)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: TT36-2024-BYT/D2/K1

Điều 2. Tiêu chuẩn sức khỏe của người lái xe, người điều khiển xe máy chuyên dùng
1. Tiêu chuẩn sức khỏe của người lái xe, người điều khiển xe máy chuyên dùng quy định tại Phụ lục I ban hành kèm theo Thông tư này.

### Điều khoản được nguồn trên dẫn chiếu tới (TT36-2024-BYT/PL1)
Mã điều khoản dùng được cho gold_units: TT36-2024-BYT/PL1

PHỤ LỤC I
BẢNG TIÊU CHUẨN SỨC KHỎE CỦA NGƯỜI LÁI XE, NGƯỜI ĐIỀU KHIỂN XE MÁY CHUYÊN DÙNG
(Ban hành kèm theo Thông tư số 36/2024/TT-BYT ngày 16 tháng 11 năm 2024 của Bộ trưởng Bộ Y tế)
SỐ TT | CHUYÊN KHOA
Số: ...(1)..../GKSKLX/Mã Cơ sở khám chữa
bệnh/Năm
MẪU GIẤY KHÁM SỨC KHỎE CỦA NGƯỜI LÁI XE, NGƯỜI ĐIỀU KHIỂN XE MÁY CHUYÊN DÙNG
1. Họ và tên (viết chữ in hoa): ………………………………………………..
Ảnh | 2. Giới tính: Nam □ Nữ □
(4x6 cm) đóng dấu giáp | 3. Ngày tháng năm sinh: (Tuổi: ....................................)
lai hoặc Scan ảnh | 4. Số CCCD /CC/Hộ chiếu/Định danh công dân: .......(2) .........................
(ảnh được chụp trên nền | 5. Cấp ngày …/…/…… Tại ........................................................................
trắng trong thời gian | 6. Chỗ ở hiện tại:
không quá 06 (sáu) | ........................................................................................
tháng tính đến ngày nộp | 7. Đề nghị khám sức khỏe để lái xe hạng: ........(3) ....................................
hồ sơ khám sức khỏe) | ........................................................................................................
.............
........................................................................................................
.............
* Lưu ý: Trường hợp đối tượng KSK có CCCD/CC gắn chíp hoặc có số định danh công dân đã thực hiện kết nối với cơ sở dữ liệu quốc gia về dân cư không cần ghi mục 2, mục 5, mục 6
I. TIỀN SỬ BỆNH CỦA ĐỐI TƯỢNG KHÁM SỨC KHỎE
…

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là người lớn tuổi, muốn lái xe máy chuyên dùng, tôi cần biết tiêu chuẩn sức khỏe và mẫu giấy khám sức khỏe là gì?
- Đáp: Bạn cần tuân thủ tiêu chuẩn sức khỏe của người lái xe, người điều khiển xe máy chuyên dùng được quy định tại Phụ lục I của Thông tư số 36/2024/TT-BYT. Mẫu giấy khám sức khỏe bao gồm các thông tin như họ và tên, giới tính, ngày tháng năm sinh, số CCCD/CC/Hộ chiếu, ngày cấp, nơi cấp, chỗ ở hiện tại và đề nghị khám sức khỏe để lái xe hạng. (Phụ lục I Thông tư số 36/2024/TT-BYT)
- Ghi chú: Giả định người hỏi là người lớn tuổi muốn lái xe máy chuyên dùng

```json
{"qid": "tD-da_buoc-011", "question": "Tôi là người lớn tuổi, muốn lái xe máy chuyên dùng, tôi cần biết tiêu chuẩn sức khỏe và mẫu giấy khám sức khỏe là gì?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Bạn cần tuân thủ tiêu chuẩn sức khỏe của người lái xe, người điều khiển xe máy chuyên dùng được quy định tại Phụ lục I của Thông tư số 36/2024/TT-BYT. Mẫu giấy khám sức khỏe bao gồm các thông tin như họ và tên, giới tính, ngày tháng năm sinh, số CCCD/CC/Hộ chiếu, ngày cấp, nơi cấp, chỗ ở hiện tại và đề nghị khám sức khỏe để lái xe hạng. (Phụ lục I Thông tư số 36/2024/TT-BYT)", "gold_units": ["TT36-2024-BYT/D2/K1", "TT36-2024-BYT/PL1"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-011:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là người lớn tuổi, muốn lái xe máy chuyên dùng, tôi muốn biết tiêu chuẩn sức khỏe cần đáp ứng và mẫu giấy khám sức khỏe cần nộp.
- Đáp: Bạn phải đáp ứng tiêu chuẩn sức khỏe của người lái xe, người điều khiển xe máy chuyên dùng theo Phụ lục I của Thông tư số 36/2024/TT-BYT. Mẫu giấy khám sức khỏe bao gồm thông tin cá nhân, giấy tờ tùy thân, nơi cấp, chỗ ở và đề nghị khám sức khỏe để lái xe hạng. (Phụ lục I Thông tư số 36/2024/TT-BYT)
- Ghi chú: Giả định người hỏi là người lớn tuổi muốn lái xe máy chuyên dùng

```json
{"qid": "tD-da_buoc-011", "question": "Tôi là người lớn tuổi, muốn lái xe máy chuyên dùng, tôi muốn biết tiêu chuẩn sức khỏe cần đáp ứng và mẫu giấy khám sức khỏe cần nộp.", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Bạn phải đáp ứng tiêu chuẩn sức khỏe của người lái xe, người điều khiển xe máy chuyên dùng theo Phụ lục I của Thông tư số 36/2024/TT-BYT. Mẫu giấy khám sức khỏe bao gồm thông tin cá nhân, giấy tờ tùy thân, nơi cấp, chỗ ở và đề nghị khám sức khỏe để lái xe hạng. (Phụ lục I Thông tư số 36/2024/TT-BYT)", "gold_units": ["TT36-2024-BYT/D2/K1", "TT36-2024-BYT/PL1"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-011:2"}
```

### WD-da_buoc-016 · tier A · vai: tài xế xe tải · kiểu: tinh_huong_ban_than · DAN_CHIEU → TT12-2025-BCA/D35

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Thông tư số 12/2025/TT-BCA (Quy định về sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế)
Hiệu lực của trạng thái này: 2025-03-01 → nay
Mã điều khoản dùng được cho gold_units: TT12-2025-BCA/D31/K1, TT12-2025-BCA/D31/K1/a, TT12-2025-BCA/D31/K1/b, TT12-2025-BCA/D31/K1/c

Điều 31. Nguyên tắc và hình thức khai thác dữ liệu trên hệ thống thông tin về sát hạch, cấp giấy phép lái xe
1. Nguyên tắc khai thác
a) Việc khai thác dữ liệu sát hạch, cấp giấy phép lái xe thực hiện theo quy định của pháp luật về công nghệ thông tin và an toàn thông tin mạng;
b) Cơ quan quản lý hệ thống thông tin giấy phép lái xe quy định tại Điều 35, Điều 36 của Thông tư này và Công an cấp xã có trách nhiệm bảo vệ thông tin, dữ liệu cá nhân trong cơ sở dữ liệu giấy phép lái xe trên môi trường mạng theo quy định của pháp luật về công nghệ thông tin;
c) Các dịch vụ khai thác thông tin dữ liệu giấy phép lái xe được cung cấp cho cơ quan, tổ chức, cá nhân trên môi trường mạng theo quy định của pháp luật về công nghệ thông tin và an toàn thông tin mạng.

### Điều khoản được nguồn trên dẫn chiếu tới (TT12-2025-BCA/D35)
Mã điều khoản dùng được cho gold_units: TT12-2025-BCA/D35

Điều 35. Trách nhiệm Cục Cảnh sát giao thông

### Điều khoản được nguồn trên dẫn chiếu tới (TT12-2025-BCA/D36)
Mã điều khoản dùng được cho gold_units: TT12-2025-BCA/D36

Điều 36. Trách nhiệm Phòng Cảnh sát giao thông

### Nguồn 2
Văn bản: Thông tư số 12/2025/TT-BCA (Quy định về sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế)
Hiệu lực của trạng thái này: 2025-03-01 → nay
Mã điều khoản dùng được cho gold_units: TT12-2025-BCA/D35/K1, TT12-2025-BCA/D35/K1/a, TT12-2025-BCA/D35/K1/b, TT12-2025-BCA/D35/K1/c, TT12-2025-BCA/D35/K1/d

Điều 35. Trách nhiệm Cục Cảnh sát giao thông
1. Công tác sát hạch lái xe
a) Hướng dẫn chuyên môn, nghiệp vụ đối với công tác xây dựng trung tâm sát hạch lái xe, sát hạch lái xe để thực hiện thống nhất trong phạm vi cả nước;
b) Xây dựng bộ câu hỏi; phần mềm hệ thống thông tin sát hạch, cấp giấy phép lái xe; phần mềm dùng cho sát hạch lý thuyết; phần mềm mô phỏng các tình huống giao thông để phục vụ công tác sát hạch lái xe, hướng dẫn thực hiện thống nhất trong cả nước và chuyển giao cho Phòng Cảnh sát giao thông, trung tâm sát hạch lái xe;
c) Xây dựng chương trình, chỉ đạo, tổ chức tập huấn, cấp thẻ sát hạch viên cho đội ngũ sát hạch viên trong cả nước và lưu trữ hồ sơ sát hạch viên theo quy định;
d) Công bố và cập nhật danh sách các trung tâm sát hạch lái xe được cấp hoặc bị thu hồi giấy phép sát hạch trên trang thông tin điện tử.

### Nguồn 3
Văn bản: Thông tư số 12/2025/TT-BCA (Quy định về sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế)
Hiệu lực của trạng thái này: 2025-03-01 → nay
Mã điều khoản dùng được cho gold_units: TT12-2025-BCA/D35/K2, TT12-2025-BCA/D35/K2/a, TT12-2025-BCA/D35/K2/b, TT12-2025-BCA/D35/K2/c

Điều 35. Trách nhiệm Cục Cảnh sát giao thông
2. Công tác cấp, đổi, cấp lại, thu hồi giấy phép lái xe
a) Hướng dẫn chuyên môn, nghiệp vụ đối với công tác cấp, đổi, cấp lại, thu hồi giấy phép lái xe để thực hiện thống nhất trong phạm vi cả nước;
b) Hướng dẫn và quản lý việc sử dụng phôi giấy phép lái xe;
c) Quản lý dữ liệu tập trung, cấp giấy phép lái xe.

### Nguồn 4
Văn bản: Thông tư số 12/2025/TT-BCA (Quy định về sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế)
Hiệu lực của trạng thái này: 2025-03-01 → nay
Mã điều khoản dùng được cho gold_units: TT12-2025-BCA/D35/K3, TT12-2025-BCA/D35/K3/a, TT12-2025-BCA/D35/K3/b, TT12-2025-BCA/D35/K3/c, TT12-2025-BCA/D35/K3/d, TT12-2025-BCA/D35/K3/đ

Điều 35. Trách nhiệm Cục Cảnh sát giao thông
3. Công tác cấp giấy phép lái xe quốc tế
a) Hướng dẫn chuyên môn, nghiệp vụ đối với công tác cấp IDP để thực hiện thống nhất trong cả nước;
b) Hướng dẫn và quản lý việc sử dụng phôi IDP theo thẩm quyền;
c) Công bố, cập nhật danh sách các nước tham gia Công ước Viên hàng năm theo thông báo chính thức của Liên hợp quốc trên trang thông tin điện tử của Cục Cảnh sát giao thông;
d) Triển khai thực hiện dịch vụ công về cấp IDP;
đ) Quản lý dữ liệu tập trung, cấp giấy phép lái xe.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là tài xế xe tải, khi cần truy cập dữ liệu giấy phép lái xe trên mạng, ai chịu trách nhiệm bảo vệ thông tin cá nhân trong cơ sở dữ liệu?
- Đáp: Khi truy cập dữ liệu giấy phép lái xe trên mạng, Cục Cảnh sát giao thông có trách nhiệm bảo vệ thông tin, dữ liệu cá nhân trong cơ sở dữ liệu, trong khi Phòng Cảnh sát giao thông cũng có trách nhiệm bảo vệ thông tin, dữ liệu cá nhân trong cơ sở dữ liệu trên môi trường mạng. (Điều 35 và Điều 36 Thông tư 12/2025/TT-BCA)
- ⚠ chep_nguyen_van: “cá nhân trong cơ sở dữ …”
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-da_buoc-016", "question": "Tôi là tài xế xe tải, khi cần truy cập dữ liệu giấy phép lái xe trên mạng, ai chịu trách nhiệm bảo vệ thông tin cá nhân trong cơ sở dữ liệu?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Khi truy cập dữ liệu giấy phép lái xe trên mạng, Cục Cảnh sát giao thông có trách nhiệm bảo vệ thông tin, dữ liệu cá nhân trong cơ sở dữ liệu, trong khi Phòng Cảnh sát giao thông cũng có trách nhiệm bảo vệ thông tin, dữ liệu cá nhân trong cơ sở dữ liệu trên môi trường mạng. (Điều 35 và Điều 36 Thông tư 12/2025/TT-BCA)", "gold_units": ["TT12-2025-BCA/D35", "TT12-2025-BCA/D36"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-016:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là tài xế xe tải, khi cần khai thác dữ liệu sát hạch lái xe, ai là cơ quan có thẩm quyền quản lý và bảo vệ dữ liệu?
- Đáp: Cục Cảnh sát giao thông có thẩm quyền quản lý và bảo vệ dữ liệu sát hạch lái xe, trong khi Phòng Cảnh sát giao thông cũng có trách nhiệm bảo vệ dữ liệu trên môi trường mạng. (Điều 35 và Điều 36 Thông tư 12/2025/TT-BCA)
- ⚠ chep_nguyen_van: “khai thác dữ liệu sát hạch …”
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-da_buoc-016", "question": "Tôi là tài xế xe tải, khi cần khai thác dữ liệu sát hạch lái xe, ai là cơ quan có thẩm quyền quản lý và bảo vệ dữ liệu?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Cục Cảnh sát giao thông có thẩm quyền quản lý và bảo vệ dữ liệu sát hạch lái xe, trong khi Phòng Cảnh sát giao thông cũng có trách nhiệm bảo vệ dữ liệu trên môi trường mạng. (Điều 35 và Điều 36 Thông tư 12/2025/TT-BCA)", "gold_units": ["TT12-2025-BCA/D35", "TT12-2025-BCA/D36"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-016:2"}
```

### WD-da_buoc-019 · tier A · vai: tài xế xe tải · kiểu: nhieu_dieu_kien · DAN_CHIEU → TT38-2024-BGTVT/D7

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Thông tư số 38/2024/TT-BGTVT (Quy định về tốc độ và khoảng cách an toàn của xe cơ giới, xe máy chuyên dùng tham gia giao thông trên đường bộ)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: TT38-2024-BGTVT/D6/K1

Điều 6. Tốc độ khai thác tối đa cho phép xe cơ giới tham gia giao thông trên đường bộ (trừ đường cao tốc)
1. Tốc độ khai thác tối đa cho phép xe cơ giới tham gia giao thông trên đường bộ trong khu vực đông dân cư
Bảng 1
Loại xe cơ giới đường bộ | Tốc độ khai thác tối đa (km/h)
Đường đôi; đường một chiều có từ hai làn xe cơ giới trở lên | Đường hai chiều; đường một chiều có một làn xe cơ giới
Các loại xe cơ giới, trừ các xe được quy định tại Điều 7 và Điều 8 Thông tư này | 60 | 50

### Điều khoản được nguồn trên dẫn chiếu tới (TT38-2024-BGTVT/D7)
Mã điều khoản dùng được cho gold_units: TT38-2024-BGTVT/D7

Điều 7. Tốc độ khai thác tối đa cho phép đối với xe máy chuyên dùng, xe gắn máy và các loại xe tương tự tham gia giao thông trên đường bộ (trừ đường cao tốc)
Xe máy chuyên dùng, xe gắn máy và các loại xe tương tự khi tham gia giao thông, tốc độ khai thác tối đa là 40 km/h.

### Điều khoản được nguồn trên dẫn chiếu tới (TT38-2024-BGTVT/D8)
Mã điều khoản dùng được cho gold_units: TT38-2024-BGTVT/D8

Điều 8. Tốc độ khai thác tối đa cho phép đối với xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ tham gia giao thông trên đường bộ (trừ đường cao tốc)

### Nguồn 2
Văn bản: Thông tư số 38/2024/TT-BGTVT (Quy định về tốc độ và khoảng cách an toàn của xe cơ giới, xe máy chuyên dùng tham gia giao thông trên đường bộ)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: TT38-2024-BGTVT/D7

Điều 7. Tốc độ khai thác tối đa cho phép đối với xe máy chuyên dùng, xe gắn máy và các loại xe tương tự tham gia giao thông trên đường bộ (trừ đường cao tốc)
Xe máy chuyên dùng, xe gắn máy và các loại xe tương tự khi tham gia giao thông, tốc độ khai thác tối đa là 40 km/h.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là tài xế xe tải, đang lái xe qua khu dân cư. Tốc độ tối đa cho xe tải là bao nhiêu? Nếu tôi cùng lúc đi xe máy, tốc độ tối đa của xe máy là bao nhiêu?
- Đáp: Tốc độ khai thác tối đa cho xe tải trong khu dân cư là 60 km/h. Tốc độ khai thác tối đa cho xe máy chuyên dùng, xe gắn máy và các loại xe tương tự là 40 km/h.
- ⚠ chi_so_so_sai (0); chi_so_so_sai (1)
- Ghi chú: Giả định xe tải là loại xe cơ giới đường bộ, xe máy là xe gắn máy

```json
{"qid": "tD-da_buoc-019", "question": "Tôi là tài xế xe tải, đang lái xe qua khu dân cư. Tốc độ tối đa cho xe tải là bao nhiêu? Nếu tôi cùng lúc đi xe máy, tốc độ tối đa của xe máy là bao nhiêu?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Tốc độ khai thác tối đa cho xe tải trong khu dân cư là 60 km/h. Tốc độ khai thác tối đa cho xe máy chuyên dùng, xe gắn máy và các loại xe tương tự là 40 km/h.", "gold_units": ["TT38-2024-BGTVT/D6/K1", "TT38-2024-BGTVT/D7"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-019:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi lái xe tải qua đường hai chiều trong khu dân cư, tốc độ tối đa được quy định là bao nhiêu? Nếu tôi muốn đi xe máy cùng lúc, tốc độ tối đa của xe máy là bao nhiêu?
- Đáp: Tốc độ khai thác tối đa cho xe tải trong khu dân cư là 60 km/h. Tốc độ khai thác tối đa cho xe máy chuyên dùng, xe gắn máy và các loại xe tương tự là 40 km/h.
- ⚠ chi_so_so_sai (0); chi_so_so_sai (1)
- Ghi chú: Giả định xe tải là loại xe cơ giới đường bộ, xe máy là xe gắn máy

```json
{"qid": "tD-da_buoc-019", "question": "Tôi lái xe tải qua đường hai chiều trong khu dân cư, tốc độ tối đa được quy định là bao nhiêu? Nếu tôi muốn đi xe máy cùng lúc, tốc độ tối đa của xe máy là bao nhiêu?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Tốc độ khai thác tối đa cho xe tải trong khu dân cư là 60 km/h. Tốc độ khai thác tối đa cho xe máy chuyên dùng, xe gắn máy và các loại xe tương tự là 40 km/h.", "gold_units": ["TT38-2024-BGTVT/D6/K1", "TT38-2024-BGTVT/D7"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-019:2"}
```

### WD-da_buoc-020 · tier A · vai: người mới học lái ô tô · kiểu: neu_van_ban · DAN_CHIEU → TT14-2025-BXD/D25/K4/a

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Thông tư số 14/2025/TT-BXD (Quy định về đào tạo lái xe; bồi dưỡng, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ)
Hiệu lực của trạng thái này: 2026-07-01 → nay
Mã điều khoản dùng được cho gold_units: TT14-2025-BXD/D31/K2, TT14-2025-BXD/D31/K2/a, TT14-2025-BXD/D31/K2/b, TT14-2025-BXD/D31/K2/c, TT14-2025-BXD/D31/K2/d, TT14-2025-BXD/D31/K2/đ, TT14-2025-BXD/D31/K2/e

Điều 31. Cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ
2. Đối với công tác quản lý hệ thống thông tin:
a) Đầu tư, bảo trì, nâng cấp Hệ thống thông tin chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ tại cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ; tiếp nhận, tổ chức thực hiện phần mềm ứng dụng phục vụ công tác quản lý cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ do Cục Đường bộ Việt Nam chuyển giao và thực hiện truyền đầy đủ dữ liệu quy định tại điểm a khoản 4 Điều 25 về Sở Xây dựng;
b) Vận hành Hệ thống thông tin chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ tại cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ theo quy định;
c) Tạo lập, đối chiếu, chịu trách nhiệm về tính chính xác của thông tin học viên, kết quả kiểm tra cấp chứng chỉ theo quy định;
d) Lưu trữ đầy đủ các thông tin theo quy định tại khoản 3 Điều 27 Thông tư này và quy định của pháp luật về lưu trữ;
đ) Ban hành quy chế vận hành và bảo đảm an toàn, an ninh thông tin; quy chế sử dụng tài khoản và khai thác dữ liệu đối với hệ thống thông tin của cơ sở bồi dưỡng và các hệ thống thông tin được chia sẻ theo các quy định của pháp luật về công nghệ thông tin và an toàn thông tin mạng;
e) Cung cấp dữ liệu trên Hệ thống thông tin chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ tại cơ sở bồi dưỡng để phục vụ công tác thanh tra, kiểm tra và cung cấp thông tin cho các cơ quan chức năng khi có yêu cầu.

### Điều khoản được nguồn trên dẫn chiếu tới (TT14-2025-BXD/D25/K4/a)
Mã điều khoản dùng được cho gold_units: TT14-2025-BXD/D25/K4/a

Điều 25. Yêu cầu đối với Hệ thống thông tin về đào tạo lái xe, chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ
4. Hệ thống thông tin chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ tại cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ:
a) Quản lý tối thiểu các thông tin của học viên: họ, tên; ngày, tháng, năm sinh; lớp bồi dưỡng; thời gian hoàn thành lớp bồi dưỡng; kết quả kiểm tra cấp chứng chỉ; ngày đạt kết quả kiểm tra cấp chứng chỉ; số chứng chỉ; ngày cấp chứng chỉ; cơ sở bồi dưỡng và cấp chứng chỉ; ngày cấp lại chứng chỉ; cơ quan cấp lại chứng chỉ;

### Điều khoản được nguồn trên dẫn chiếu tới (TT14-2025-BXD/D27/K3)
Mã điều khoản dùng được cho gold_units: TT14-2025-BXD/D27/K3

Điều 27. Thời gian lưu trữ dữ liệu trên hệ thống thông tin
3. Thời gian lưu trữ dữ liệu tại cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ: dữ liệu về bồi dưỡng, kiểm tra bồi dưỡng kiến thức pháp luật về giao thông đường bộ lưu trữ tối thiểu là 03 năm; dữ liệu cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ lưu trữ tối thiểu là 50 năm.

### Nguồn 2
Văn bản: Thông tư số 14/2025/TT-BXD (Quy định về đào tạo lái xe; bồi dưỡng, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ)
Hiệu lực của trạng thái này: 2025-09-01 → nay
Mã điều khoản dùng được cho gold_units: TT14-2025-BXD/D25/K4, TT14-2025-BXD/D25/K4/a, TT14-2025-BXD/D25/K4/b, TT14-2025-BXD/D25/K4/c, TT14-2025-BXD/D25/K4/d, TT14-2025-BXD/D25/K4/đ, TT14-2025-BXD/D25/K4/e

Điều 25. Yêu cầu đối với Hệ thống thông tin về đào tạo lái xe, chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ
4. Hệ thống thông tin chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ tại cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ:
a) Quản lý tối thiểu các thông tin của học viên: họ, tên; ngày, tháng, năm sinh; lớp bồi dưỡng; thời gian hoàn thành lớp bồi dưỡng; kết quả kiểm tra cấp chứng chỉ; ngày đạt kết quả kiểm tra cấp chứng chỉ; số chứng chỉ; ngày cấp chứng chỉ; cơ sở bồi dưỡng và cấp chứng chỉ; ngày cấp lại chứng chỉ; cơ quan cấp lại chứng chỉ;
b) Có chức năng tạo lớp bồi dưỡng, tạo kỳ kiểm tra, in chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ;
c) Có chức năng cấp, cấp lại chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ;
d) Có chức năng lưu trữ chính xác, đầy đủ các thông tin được quản lý;
đ) Có khả năng kết nối, chia sẻ dữ liệu với Hệ thống thông tin chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ tại Sở Xây dựng và các hệ thống thông tin liên quan;
e) Bảo đảm các quy định về an toàn, an ninh thông tin, an toàn thông tin mạng theo các quy định của pháp luật hiện hành.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Theo Thông tư 14/2025/TT-BXD, khi tôi đăng ký học bồi dưỡng kiến thức pháp luật giao thông, dữ liệu nào cơ sở phải lưu trữ và trong bao lâu?
- Đáp: Cơ sở bồi dưỡng phải lưu trữ đầy đủ thông tin học viên như họ, tên, ngày sinh, lớp bồi dưỡng, thời gian hoàn thành, kết quả kiểm tra, ngày đạt, số chứng chỉ, ngày cấp, cơ sở cấp, ngày cấp lại, cơ quan cấp lại. Thời gian lưu trữ tối thiểu là 3 năm cho dữ liệu bồi dưỡng và kiểm tra, và 50 năm cho dữ liệu cấp chứng chỉ.
- ⚠ chep_nguyen_van: “bồi dưỡng kiến thức pháp luật …”

```json
{"qid": "tD-da_buoc-020", "question": "Theo Thông tư 14/2025/TT-BXD, khi tôi đăng ký học bồi dưỡng kiến thức pháp luật giao thông, dữ liệu nào cơ sở phải lưu trữ và trong bao lâu?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Cơ sở bồi dưỡng phải lưu trữ đầy đủ thông tin học viên như họ, tên, ngày sinh, lớp bồi dưỡng, thời gian hoàn thành, kết quả kiểm tra, ngày đạt, số chứng chỉ, ngày cấp, cơ sở cấp, ngày cấp lại, cơ quan cấp lại. Thời gian lưu trữ tối thiểu là 3 năm cho dữ liệu bồi dưỡng và kiểm tra, và 50 năm cho dữ liệu cấp chứng chỉ.", "gold_units": ["TT14-2025-BXD/D31/K2", "TT14-2025-BXD/D27/K3"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-020:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Nếu tôi muốn biết thời gian lưu trữ dữ liệu học viên sau khi hoàn thành lớp bồi dưỡng theo Thông tư 14/2025/TT-BXD, thì cơ sở phải giữ dữ liệu bao lâu?
- Đáp: Dữ liệu bồi dưỡng và kiểm tra phải được lưu trữ tối thiểu 3 năm, còn dữ liệu cấp chứng chỉ phải lưu trữ tối thiểu 50 năm.
- ⚠ chep_nguyen_van: “thời gian lưu trữ dữ liệu …”

```json
{"qid": "tD-da_buoc-020", "question": "Nếu tôi muốn biết thời gian lưu trữ dữ liệu học viên sau khi hoàn thành lớp bồi dưỡng theo Thông tư 14/2025/TT-BXD, thì cơ sở phải giữ dữ liệu bao lâu?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Dữ liệu bồi dưỡng và kiểm tra phải được lưu trữ tối thiểu 3 năm, còn dữ liệu cấp chứng chỉ phải lưu trữ tối thiểu 50 năm.", "gold_units": ["TT14-2025-BXD/D31/K2", "TT14-2025-BXD/D27/K3"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-020:2"}
```

### WD-da_buoc-021 · tier A · vai: người lớn tuổi đi xe đạp điện · kiểu: nhieu_dieu_kien · DAN_CHIEU → LUAT36-2024/D59/K1

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Thông tư số 12/2025/TT-BCA (Quy định về sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế)
Hiệu lực của trạng thái này: 2025-03-01 → nay
Mã điều khoản dùng được cho gold_units: TT12-2025-BCA/D15/K1

Điều 15. Người dự sát hạch lái xe
1. Đủ tuổi (tính đến ngày dự sát hạch lái xe), sức khỏe theo quy định tại khoản 1, 2 Điều 59 Luật Trật tự, an toàn giao thông đường bộ.

### Điều khoản được nguồn trên dẫn chiếu tới (LUAT36-2024/D59/K1)
Mã điều khoản dùng được cho gold_units: LUAT36-2024/D59/K1

Điều 59. Tuổi, sức khỏe của người điều khiển phương tiện tham gia giao thông đường bộ
1. Độ tuổi của người lái xe, người điều khiển xe máy chuyên dùng được quy định như sau:

### Điều khoản được nguồn trên dẫn chiếu tới (LUAT36-2024/D59/K2)
Mã điều khoản dùng được cho gold_units: LUAT36-2024/D59/K2

Điều 59. Tuổi, sức khỏe của người điều khiển phương tiện tham gia giao thông đường bộ
2. Người điều khiển phương tiện tham gia giao thông đường bộ phải bảo đảm điều kiện sức khỏe phù hợp với từng loại phương tiện được phép điều khiển. Bộ trưởng Bộ Y tế quy định về tiêu chuẩn sức khỏe, việc khám sức khỏe đối với người lái xe, người điều khiển xe máy chuyên dùng; việc khám sức khỏe định kỳ đối với người hành nghề lái xe ô tô; xây dựng cơ sở dữ liệu về sức khỏe của người lái xe, người điều khiển xe máy chuyên dùng.

### Nguồn 2
Văn bản: Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: LUAT36-2024/D59/K1, LUAT36-2024/D59/K1/a, LUAT36-2024/D59/K1/b, LUAT36-2024/D59/K1/c, LUAT36-2024/D59/K1/d, LUAT36-2024/D59/K1/đ, LUAT36-2024/D59/K1/e

Điều 59. Tuổi, sức khỏe của người điều khiển phương tiện tham gia giao thông đường bộ
1. Độ tuổi của người lái xe, người điều khiển xe máy chuyên dùng được quy định như sau:
a) Người đủ 16 tuổi trở lên được điều khiển xe gắn máy;
b) Người đủ 18 tuổi trở lên được cấp giấy phép lái xe hạng A1, A, B1, B, C1, được cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ để điều khiển xe máy chuyên dùng tham gia giao thông đường bộ;
c) Người đủ 21 tuổi trở lên được cấp giấy phép lái xe hạng C, BE;
d) Người đủ 24 tuổi trở lên được cấp giấy phép lái xe hạng D1, D2, C1E, CE;
đ) Người đủ 27 tuổi trở lên được cấp giấy phép lái xe hạng D, D1E, D2E, DE;
e) Tuổi tối đa của người lái xe ô tô chở người (kể cả xe buýt) trên 29 chỗ (không kể chỗ của người lái xe), xe ô tô chở người giường nằm là đủ 57 tuổi đối với nam, đủ 55 tuổi đối với nữ.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi 20 tuổi, muốn tham gia sát hạch lái xe máy gắn máy điện, có đủ điều kiện không?
- Đáp: Bạn đủ điều kiện tham gia sát hạch lái xe máy gắn máy điện vì đã đủ 16 tuổi và đáp ứng điều kiện sức khỏe. (khoản 1 Điều 15 Thông tư 12/2025/TT-BCA; khoản 1 Điều 59 Luật 36/2024/QH15)
- ⚠ chi_so_so_sai (0)
- Ghi chú: Giả định người hỏi là người lớn tuổi đi xe đạp điện

```json
{"qid": "tD-da_buoc-021", "question": "Tôi 20 tuổi, muốn tham gia sát hạch lái xe máy gắn máy điện, có đủ điều kiện không?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Bạn đủ điều kiện tham gia sát hạch lái xe máy gắn máy điện vì đã đủ 16 tuổi và đáp ứng điều kiện sức khỏe. (khoản 1 Điều 15 Thông tư 12/2025/TT-BCA; khoản 1 Điều 59 Luật 36/2024/QH15)", "gold_units": ["TT12-2025-BCA/D15/K1", "LUAT36-2024/D59/K1"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-021:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi 70 tuổi, muốn lái xe máy gắn máy điện, có được phép lái không?
- Đáp: Bạn có thể lái xe máy gắn máy điện vì không có giới hạn tuổi tối đa trong quy định. (khoản 1 Điều 15 Thông tư 12/2025/TT-BCA; khoản 1 Điều 59 Luật 36/2024/QH15)
- ⚠ chi_so_so_sai (0)
- Ghi chú: Giả định người hỏi là người lớn tuổi đi xe đạp điện

```json
{"qid": "tD-da_buoc-021", "question": "Tôi 70 tuổi, muốn lái xe máy gắn máy điện, có được phép lái không?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Bạn có thể lái xe máy gắn máy điện vì không có giới hạn tuổi tối đa trong quy định. (khoản 1 Điều 15 Thông tư 12/2025/TT-BCA; khoản 1 Điều 59 Luật 36/2024/QH15)", "gold_units": ["TT12-2025-BCA/D15/K1", "LUAT36-2024/D59/K1"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-021:2"}
```

### WD-da_buoc-022 · tier A · vai: người mới học lái ô tô · kiểu: nhieu_dieu_kien · DAN_CHIEU → TT79-2024-BCA/D4

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D15/K2

Điều 15. Cấp chứng nhận đăng ký xe, biển số xe trong trường hợp thay đổi chủ xe (sau đây viết gọn là đăng ký sang tên xe)
2. Tổ chức, cá nhân nhận chuyển quyền sở hữu xe làm thủ tục đăng ký sang tên xe tại cơ quan đăng ký xe theo quy định tại Điều 4 Thông tư này.

### Điều khoản được nguồn trên dẫn chiếu tới (TT79-2024-BCA/D4)
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D4

Điều 4. Cơ quan đăng ký xe

### Nguồn 2
Văn bản: Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)
Hiệu lực của trạng thái này: 2025-01-01 → 2025-02-28
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D4/K3

Điều 4. Cơ quan đăng ký xe
3. Công an cấp huyện đăng ký các loại xe: Xe mô tô đăng ký biển số xe trúng đấu giá; xe ô tô, xe máy chuyên dùng, xe mô tô của tổ chức, cá nhân trong nước có trụ sở, cư trú tại địa phương (trừ các loại xe quy định tại khoản 1, khoản 2, khoản 4 Điều này).

### Nguồn 3
Văn bản: Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D4/K1

Điều 4. Cơ quan đăng ký xe
1. Cục Cảnh sát giao thông đăng ký xe của các đơn vị thuộc cơ quan Bộ Công an; xe ô tô, xe máy chuyên dùng của các cơ quan, tổ chức quy định tại Phụ lục số 01 ban hành kèm theo Thông tư này; xe ô tô của cơ quan đại diện ngoại giao, cơ quan đại diện của tổ chức quốc tế có trụ sở tại thành phố Hà Nội và xe ô tô của người nước ngoài làm việc trong cơ quan đó.

### Điều khoản được nguồn trên dẫn chiếu tới (TT79-2024-BCA/PL1)
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/PL1

PHỤ LỤC 01
CÁC CƠ QUAN, ĐƠN VỊ ĐĂNG KÝ XE Ô TÔ, XE MÁY CHUYÊN DÙNG TẠI CỤC CẢNH SÁT GIAO THÔNG
(Ban hành kèm theo Thông tư số 79/2024/TT-BCA ngày 15/11/2024 của Bộ trưởng Bộ Công an)
STT | TÊN CƠ QUAN, ĐƠN VỊ
1 | Văn phòng và các Ban của Trung ương Đảng
2 | Văn phòng Chủ tịch nước
3 | Văn phòng Quốc hội
4 | Văn phòng các Bộ, cơ quan ngang Bộ, các cơ quan thuộc Chính phủ
5 | Văn phòng cơ quan Trung ương các tổ chức chính trị-xã hội (Mặt trận Tổ quốc Việt Nam, Công đoàn Việt Nam, Đoàn Thanh niên Cộng sản Hồ Chí Minh, Hội Liên hiệp Phụ nữ Việt Nam, Hội Cựu chiến binh Việt Nam, Hội Nông dân Việt Nam
6 | Văn phòng Viện Kiểm sát nhân dân tối cao
7 | Văn phòng Toà án nhân dân tối cao
8 | Văn phòng Kiểm toán Nhà nước

### Nguồn 4
Văn bản: Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)
Hiệu lực của trạng thái này: 2025-03-01 → nay
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D4/K2, TT79-2024-BCA/D4/K2/a, TT79-2024-BCA/D4/K2/b, TT79-2024-BCA/D4/K2/c, TT79-2024-BCA/D4/K2/d

Điều 4. Cơ quan đăng ký xe
2. Phòng Cảnh sát giao thông đăng ký các loại xe sau đây (trừ các loại xe quy định tại khoản 1 Điều này):
a) Xe ô tô, rơmoóc, sơ mi rơmoóc, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ, các loại xe có kết cấu tương tự xe ô tô (sau đây viết gọn là xe ô tô) và xe máy chuyên dùng của tổ chức, cá nhân có trụ sở, cư trú tại quận, thành phố thuộc thành phố trực thuộc Trung ương hoặc tại thành phố, huyện, thị xã thuộc tỉnh nơi Phòng Cảnh sát giao thông đặt trụ sở;
b) Xe ô tô, xe mô tô, xe gắn máy đăng ký gắn biển số xe trúng đấu giá;
c) Xe có nguồn gốc tịch thu, xe mô tô có dung tích xi lanh từ 175 cm3 trở lên;
d) Xe ô tô, xe máy chuyên dùng, xe mô tô, xe gắn máy và các loại xe có kết cấu tương tự xe mô tô (sau đây viết gọn là xe mô tô) của tổ chức, cá nhân nước ngoài.

### Điều khoản được nguồn trên dẫn chiếu tới (TT79-2024-BCA/D4/K1)
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D4/K1

Điều 4. Cơ quan đăng ký xe
1. Cục Cảnh sát giao thông đăng ký xe của các đơn vị thuộc cơ quan Bộ Công an; xe ô tô, xe máy chuyên dùng của các cơ quan, tổ chức quy định tại Phụ lục số 01 ban hành kèm theo Thông tư này; xe ô tô của cơ quan đại diện ngoại giao, cơ quan đại diện của tổ chức quốc tế có trụ sở tại thành phố Hà Nội và xe ô tô của người nước ngoài làm việc trong cơ quan đó.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi mới học lái xe và muốn chuyển quyền sở hữu chiếc ô tô sang con gái, tôi cần làm thủ tục ở đâu và phải làm gì?
- Đáp: Bạn phải nộp hồ sơ đăng ký sang tên xe tại cơ quan đăng ký xe theo quy định. Cơ quan đăng ký xe là cơ quan đăng ký xe của cơ quan công an, hoặc phòng Cảnh sát giao thông tùy theo địa phương. (Điều 15, Điều 4 Thông tư 79/2024/TT-BCA)

```json
{"qid": "tD-da_buoc-022", "question": "Tôi mới học lái xe và muốn chuyển quyền sở hữu chiếc ô tô sang con gái, tôi cần làm thủ tục ở đâu và phải làm gì?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Bạn phải nộp hồ sơ đăng ký sang tên xe tại cơ quan đăng ký xe theo quy định. Cơ quan đăng ký xe là cơ quan đăng ký xe của cơ quan công an, hoặc phòng Cảnh sát giao thông tùy theo địa phương. (Điều 15, Điều 4 Thông tư 79/2024/TT-BCA)", "gold_units": ["TT79-2024-BCA/D15/K2", "TT79-2024-BCA/D4"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-022:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Công ty tôi muốn chuyển quyền sở hữu chiếc xe ô tô chuyên dùng sang nhân viên mới, tôi cần làm thủ tục ở đâu và cần chuẩn bị gì?
- Đáp: Bạn phải nộp hồ sơ đăng ký sang tên xe tại cơ quan đăng ký xe theo quy định. Cơ quan đăng ký xe là cơ quan đăng ký xe của cơ quan công an, hoặc phòng Cảnh sát giao thông tùy theo địa phương. (Điều 15, Điều 4 Thông tư 79/2024/TT-BCA)

```json
{"qid": "tD-da_buoc-022", "question": "Công ty tôi muốn chuyển quyền sở hữu chiếc xe ô tô chuyên dùng sang nhân viên mới, tôi cần làm thủ tục ở đâu và cần chuẩn bị gì?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Bạn phải nộp hồ sơ đăng ký sang tên xe tại cơ quan đăng ký xe theo quy định. Cơ quan đăng ký xe là cơ quan đăng ký xe của cơ quan công an, hoặc phòng Cảnh sát giao thông tùy theo địa phương. (Điều 15, Điều 4 Thông tư 79/2024/TT-BCA)", "gold_units": ["TT79-2024-BCA/D15/K2", "TT79-2024-BCA/D4"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-022:2"}
```

### WD-da_buoc-023 · tier A · vai: tài xế xe tải · kiểu: ngan · DAN_CHIEU → TT14-2025-BXD/D25/K5/a

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Thông tư số 14/2025/TT-BXD (Quy định về đào tạo lái xe; bồi dưỡng, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ)
Hiệu lực của trạng thái này: 2026-07-01 → nay
Mã điều khoản dùng được cho gold_units: TT14-2025-BXD/D29/K3, TT14-2025-BXD/D29/K3/a, TT14-2025-BXD/D29/K3/b, TT14-2025-BXD/D29/K3/c, TT14-2025-BXD/D29/K3/d, TT14-2025-BXD/D29/K3/đ, TT14-2025-BXD/D29/K3/e

Điều 29. Sở Xây dựng
3. Đối với công tác quản lý hệ thống thông tin:
a) Đầu tư, bảo trì, nâng cấp Hệ thống thông tin quản lý, giám sát đào tạo lái xe, Hệ thống thông tin chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ tại Sở Xây dựng; tiếp nhận và tổ chức thực hiện phần mềm ứng dụng phục vụ công tác quản lý đào tạo lái xe, phần mềm quản lý cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ tại Sở Xây dựng do Cục Đường bộ Việt Nam chuyển giao trước ngày 01 tháng 7 năm 2026 và thực hiện truyền đầy đủ dữ liệu quy định tại điểm a, điểm b, điểm c, điểm d khoản 2 và điểm a, điểm b, điểm c khoản 5 Điều 25 về Cục Đường bộ Việt Nam từ ngày 01 tháng 7 năm 2026.
b) Vận hành Hệ thống thông tin quản lý, giám sát đào tạo lái xe và Hệ thống thông tin chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ tại Sở Xây dựng theo quy định;
c) Sử dụng các phần mềm trong Hệ thống thông tin quản lý, giám sát đào tạo lái xe tại Sở Xây dựng để tiếp nhận báo cáo đăng ký khóa đào tạo lái xe; kiểm tra đối chiếu các thông tin người học lái xe, quá trình đào tạo, kết quả đào tạo;
d) Sử dụng dữ liệu trên Hệ thống thông tin quản lý, giám sát đào tạo lái xe và Hệ thống thông tin chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ tại Sở Xây dựng, tại cơ sở đào tạo lái xe và tại cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ để phục vụ công tác thanh tra, kiểm tra, cung cấp thông tin cho các cơ quan chức năng khi có yêu cầu;
…

### Điều khoản được nguồn trên dẫn chiếu tới (TT14-2025-BXD/D25/K2/a)
Mã điều khoản dùng được cho gold_units: TT14-2025-BXD/D25/K2/a

Điều 25. Yêu cầu đối với Hệ thống thông tin về đào tạo lái xe, chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ
2. Hệ thống thông tin quản lý, giám sát đào tạo lái xe tại Sở Xây dựng:
a) Tiếp nhận và quản lý thông tin học viên được cấp giấy xác nhận hoàn thành khóa đào tạo lái xe từ các cơ sở đào tạo lái xe, tối thiểu các thông tin quy định tại điểm h khoản 1 Điều này;

### Điều khoản được nguồn trên dẫn chiếu tới (TT14-2025-BXD/D25/K2/b)
Mã điều khoản dùng được cho gold_units: TT14-2025-BXD/D25/K2/b

Điều 25. Yêu cầu đối với Hệ thống thông tin về đào tạo lái xe, chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ
2. Hệ thống thông tin quản lý, giám sát đào tạo lái xe tại Sở Xây dựng:
b) Quản lý tối thiểu thông tin cơ sở đào tạo lái xe: số giấy phép đào tạo; mã số quản lý cơ sở đào tạo lái xe; tên cơ sở đào tạo lái xe; địa chỉ; cơ quan quản lý trực tiếp; hạng được phép đào tạo, lưu lượng được phép đào tạo;

### Điều khoản được nguồn trên dẫn chiếu tới (TT14-2025-BXD/D25/K2/c)
Mã điều khoản dùng được cho gold_units: TT14-2025-BXD/D25/K2/c

Điều 25. Yêu cầu đối với Hệ thống thông tin về đào tạo lái xe, chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ
2. Hệ thống thông tin quản lý, giám sát đào tạo lái xe tại Sở Xây dựng:
c) Quản lý tối thiểu thông tin giáo viên dạy lái xe: số giấy chứng nhận giáo viên dạy thực hành lái xe (nếu có); họ, tên; số định danh cá nhân; ngày, tháng, năm sinh; hạng được phép đào tạo; hình thức tuyển dụng; trình độ văn hóa; trình độ sư phạm; hạng giấy phép lái xe; ngày trúng tuyển; thâm niên dạy lái; môn học giảng dạy;

### Nguồn 2
Văn bản: Thông tư số 14/2025/TT-BXD (Quy định về đào tạo lái xe; bồi dưỡng, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ)
Hiệu lực của trạng thái này: 2025-09-01 → nay
Mã điều khoản dùng được cho gold_units: TT14-2025-BXD/D25/K5, TT14-2025-BXD/D25/K5/a, TT14-2025-BXD/D25/K5/b, TT14-2025-BXD/D25/K5/c, TT14-2025-BXD/D25/K5/d, TT14-2025-BXD/D25/K5/đ

Điều 25. Yêu cầu đối với Hệ thống thông tin về đào tạo lái xe, chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ
5. Hệ thống thông tin chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ tại Sở Xây dựng:
a) Có chức năng tiếp nhận, quản lý và lưu trữ tối thiểu các thông tin quy định tại điểm a khoản 4 Điều này và các thông tin về ngày cấp lại chứng chỉ, cơ quan cấp lại chứng chỉ của từng học viên trong trường hợp Sở Xây dựng là cơ quan cấp lại chứng chỉ;
b) Quản lý tối thiểu thông tin cơ sở đào tạo lái xe ô tô tham gia cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ: số giấy phép đào tạo; mã số quản lý cơ sở đào tạo lái xe; tên cơ sở đào tạo lái xe; địa chỉ; cơ quan quản lý trực tiếp;
c) Quản lý tối thiểu thông tin cơ sở đào tạo người điều khiển xe máy chuyên dùng thực hiện bồi dưỡng, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ: tên cơ sở đào tạo người điều khiển xe máy chuyên dùng; địa chỉ; cơ quan quản lý trực tiếp;
d) Có chức năng cấp lại chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ;
đ) Có chức năng kết nối, chia sẻ dữ liệu với các hệ thống thông tin liên quan.

### Điều khoản được nguồn trên dẫn chiếu tới (TT14-2025-BXD/D25/K4/a)
Mã điều khoản dùng được cho gold_units: TT14-2025-BXD/D25/K4/a

Điều 25. Yêu cầu đối với Hệ thống thông tin về đào tạo lái xe, chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ
4. Hệ thống thông tin chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ tại cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ:
a) Quản lý tối thiểu các thông tin của học viên: họ, tên; ngày, tháng, năm sinh; lớp bồi dưỡng; thời gian hoàn thành lớp bồi dưỡng; kết quả kiểm tra cấp chứng chỉ; ngày đạt kết quả kiểm tra cấp chứng chỉ; số chứng chỉ; ngày cấp chứng chỉ; cơ sở bồi dưỡng và cấp chứng chỉ; ngày cấp lại chứng chỉ; cơ quan cấp lại chứng chỉ;

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là tài xế xe tải, khi đăng ký học lái xe, hệ thống tại Sở Xây dựng có lưu trữ thông tin gì và cần cung cấp thông tin cơ sở đào tạo như thế nào?
- Đáp: Hệ thống tại Sở Xây dựng phải tiếp nhận và quản lý thông tin học viên được cấp giấy xác nhận hoàn thành khóa đào tạo lái xe, bao gồm các thông tin quy định tại điểm h khoản 1. Ngoài ra, hệ thống còn phải quản lý tối thiểu thông tin cơ sở đào tạo lái xe: số giấy phép đào tạo, mã số quản lý, tên, địa chỉ, cơ quan quản lý trực tiếp, hạng được phép đào tạo và lưu lượng được phép đào tạo.
- ⚠ chep_nguyen_van: “thông tin cơ sở đào tạo …”
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-da_buoc-023", "question": "Tôi là tài xế xe tải, khi đăng ký học lái xe, hệ thống tại Sở Xây dựng có lưu trữ thông tin gì và cần cung cấp thông tin cơ sở đào tạo như thế nào?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Hệ thống tại Sở Xây dựng phải tiếp nhận và quản lý thông tin học viên được cấp giấy xác nhận hoàn thành khóa đào tạo lái xe, bao gồm các thông tin quy định tại điểm h khoản 1. Ngoài ra, hệ thống còn phải quản lý tối thiểu thông tin cơ sở đào tạo lái xe: số giấy phép đào tạo, mã số quản lý, tên, địa chỉ, cơ quan quản lý trực tiếp, hạng được phép đào tạo và lưu lượng được phép đào tạo.", "gold_units": ["TT14-2025-BXD/D29/K3", "TT14-2025-BXD/D25/K2/b"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-023:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là tài xế xe tải, khi muốn lấy chứng chỉ bồi dưỡng kiến thức pháp luật, hệ thống tại Sở Xây dựng cần lưu trữ thông tin gì và quản lý thông tin cơ sở đào tạo như thế nào?
- Đáp: Hệ thống tại Sở Xây dựng phải có chức năng tiếp nhận, quản lý và lưu trữ tối thiểu các thông tin quy định tại điểm a khoản 4, cùng với thông tin về ngày cấp lại chứng chỉ và cơ quan cấp lại. Đồng thời, hệ thống phải quản lý tối thiểu thông tin cơ sở đào tạo lái xe ô tô tham gia cấp chứng chỉ, bao gồm số giấy phép đào tạo, mã số quản lý, tên, địa chỉ và cơ quan quản lý trực tiếp.
- ⚠ chep_nguyen_van: “bồi dưỡng kiến thức pháp luật …”
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-da_buoc-023", "question": "Tôi là tài xế xe tải, khi muốn lấy chứng chỉ bồi dưỡng kiến thức pháp luật, hệ thống tại Sở Xây dựng cần lưu trữ thông tin gì và quản lý thông tin cơ sở đào tạo như thế nào?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Hệ thống tại Sở Xây dựng phải có chức năng tiếp nhận, quản lý và lưu trữ tối thiểu các thông tin quy định tại điểm a khoản 4, cùng với thông tin về ngày cấp lại chứng chỉ và cơ quan cấp lại. Đồng thời, hệ thống phải quản lý tối thiểu thông tin cơ sở đào tạo lái xe ô tô tham gia cấp chứng chỉ, bao gồm số giấy phép đào tạo, mã số quản lý, tên, địa chỉ và cơ quan quản lý trực tiếp.", "gold_units": ["TT14-2025-BXD/D29/K3", "TT14-2025-BXD/D25/K5/b"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-023:2"}
```

### WD-da_buoc-024 · tier A · vai: người lớn tuổi đi xe đạp điện · kiểu: tinh_huong_ban_than · DAN_CHIEU → TT65-2024-BCA/D5

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Thông tư số 65/2024/TT-BCA (Quy định kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ để được phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: TT65-2024-BCA/D11/K2, TT65-2024-BCA/D11/K2/a, TT65-2024-BCA/D11/K2/b

Điều 11. Trách nhiệm thi hành
2. Giám đốc Công an tỉnh, thành phố trực thuộc trung ương có trách nhiệm:
a) Định kỳ 06 tháng, 01 năm hoặc đột xuất báo cáo về Bộ Công an (qua Cục Cảnh sát giao thông) kết quả thực hiện kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ thuộc phạm vi quản lý;
b) Tổ chức kiểm tra lưu động kiến thức pháp luật về trật tự, an toàn giao thông đường bộ khi bảo đảm điều kiện tổ chức kiểm tra quy định tại Điều 5 Thông tư này.

### Điều khoản được nguồn trên dẫn chiếu tới (TT65-2024-BCA/D5)
Mã điều khoản dùng được cho gold_units: TT65-2024-BCA/D5

Điều 5. Bảo đảm điều kiện tổ chức kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ

### Nguồn 2
Văn bản: Thông tư số 65/2024/TT-BCA (Quy định kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ để được phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: TT65-2024-BCA/D5/K1, TT65-2024-BCA/D5/K1/a, TT65-2024-BCA/D5/K1/b, TT65-2024-BCA/D5/K1/c

Điều 5. Bảo đảm điều kiện tổ chức kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ
1. Bảo đảm về cơ sở vật chất, thiết bị thuộc quyền sử dụng của cơ quan có thẩm quyền kiểm tra:
a) Có phòng kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ, được trang bị máy tính, máy in dùng cho cán bộ thực hiện nhiệm vụ kiểm tra và cơ sở vật chất, thiết bị cần thiết trực tiếp phục vụ việc kiểm tra; máy tính để người dự kiểm tra sử dụng có kết nối mạng WAN Bộ Công an đến máy chủ đặt tại Cục Cảnh sát giao thông;
Máy chủ có cài đặt phần mềm kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ được Bộ Công an phê duyệt được kết nối với máy tính tại các điểm kiểm tra và phải bảo đảm an ninh, an toàn dữ liệu các máy tính sử dụng để phục vụ kiểm tra, lưu trữ nhật ký kết nối, chỉnh sửa dữ liệu.
b) Có hệ thống camera giám sát được toàn bộ hình ảnh phòng kiểm tra, có thiết bị lưu trữ dữ liệu hình ảnh camera. Hệ thống camera giám sát phải đảm bảo tính bảo mật, ngăn chặn các truy cập trái phép từ bên ngoài;
c) Trường hợp máy tính tại nơi kiểm tra chưa có kết nối mạng WAN theo quy định tại điểm a khoản 1 Điều này thì cơ quan có thẩm quyền kiểm tra sử dụng thiết bị có chức năng lưu trữ thông tin bảo đảm an ninh, an toàn để lưu trữ thông tin của người dự kiểm tra phục vụ việc tổ chức kiểm tra.

### Nguồn 3
Văn bản: Thông tư số 65/2024/TT-BCA (Quy định kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ để được phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: TT65-2024-BCA/D5/K2

Điều 5. Bảo đảm điều kiện tổ chức kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ
2. Cán bộ được giao nhiệm vụ kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ phải có giấy phép lái xe mô tô hạng A và giấy phép lái xe ô tô, được Cục Cảnh sát giao thông tổ chức tập huấn, cấp thẻ Sát hạch viên.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là người lớn tuổi đi xe đạp điện, muốn tham gia kiểm tra kiến thức pháp luật để phục hồi điểm, tôi cần biết những điều kiện nào?
- Đáp: Bạn cần tham gia kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ. Ngoài ra, cán bộ thực hiện kiểm tra phải có giấy phép lái xe mô tô hạng A và giấy phép lái xe ô tô, được Cục Cảnh sát giao thông tổ chức tập huấn, cấp thẻ Sát hạch viên.
- ⚠ chep_nguyen_van: “kiểm tra kiến thức pháp luật …”
- Ghi chú: Không có điều kiện đặc biệt liên quan đến xe đạp điện trong văn bản này.

```json
{"qid": "tD-da_buoc-024", "question": "Tôi là người lớn tuổi đi xe đạp điện, muốn tham gia kiểm tra kiến thức pháp luật để phục hồi điểm, tôi cần biết những điều kiện nào?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Bạn cần tham gia kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ. Ngoài ra, cán bộ thực hiện kiểm tra phải có giấy phép lái xe mô tô hạng A và giấy phép lái xe ô tô, được Cục Cảnh sát giao thông tổ chức tập huấn, cấp thẻ Sát hạch viên.", "gold_units": ["TT65-2024-BCA/D11/K2", "TT65-2024-BCA/D5/K2"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-024:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là người lớn tuổi đi xe đạp điện, muốn biết trách nhiệm của giám đốc công an trong việc tổ chức kiểm tra kiến thức pháp luật?
- Đáp: Giám đốc công an phải định kỳ báo cáo kết quả thực hiện kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ cho Bộ Công an. Đồng thời, cán bộ thực hiện kiểm tra phải có giấy phép lái xe mô tô hạng A và giấy phép lái xe ô tô, được Cục Cảnh sát giao thông tổ chức tập huấn, cấp thẻ Sát hạch viên.
- ⚠ chep_nguyen_van: “chức kiểm tra kiến thức pháp …”
- Ghi chú: Câu hỏi không đề cập đến xe đạp điện trong quy định, chỉ liên quan đến trách nhiệm của giám đốc công an.

```json
{"qid": "tD-da_buoc-024", "question": "Tôi là người lớn tuổi đi xe đạp điện, muốn biết trách nhiệm của giám đốc công an trong việc tổ chức kiểm tra kiến thức pháp luật?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Giám đốc công an phải định kỳ báo cáo kết quả thực hiện kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ cho Bộ Công an. Đồng thời, cán bộ thực hiện kiểm tra phải có giấy phép lái xe mô tô hạng A và giấy phép lái xe ô tô, được Cục Cảnh sát giao thông tổ chức tập huấn, cấp thẻ Sát hạch viên.", "gold_units": ["TT65-2024-BCA/D11/K2", "TT65-2024-BCA/D5/K2"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-024:2"}
```

### WD-da_buoc-026 · tier A · vai: người mới học lái ô tô · kiểu: tinh_huong_ban_than · DAN_CHIEU → LUAT35-2024/D15/K3/c

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Luật Đường bộ số 35/2024/QH15
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: LUAT35-2024/D21/K3, LUAT35-2024/D21/K3/a, LUAT35-2024/D21/K3/b, LUAT35-2024/D21/K3/c

Điều 21. Bảo vệ kết cấu hạ tầng đường bộ
3. Trách nhiệm bảo vệ kết cấu hạ tầng đường bộ quy định như sau:
a) Bộ Giao thông vận tải tổ chức thực hiện bảo vệ kết cấu hạ tầng đường bộ thuộc phạm vi quản lý, trừ quy định tại điểm b khoản này;
b) Ủy ban nhân dân các cấp tổ chức thực hiện bảo vệ kết cấu hạ tầng đường bộ thuộc phạm vi quản lý; phối hợp với người quản lý, sử dụng đường bộ để tuyên truyền, phổ biến pháp luật về bảo vệ kết cấu hạ tầng đường bộ; công bố công khai mốc lộ giới sử dụng đất trong hành lang an toàn đường bộ; kịp thời xử lý trường hợp lấn, chiếm, sử dụng trái phép hành lang an toàn đường bộ, đất của đường bộ;
c) Người quản lý, sử dụng đường bộ có trách nhiệm bảo vệ kết cấu hạ tầng đường bộ thuộc phạm vi quản lý; trường hợp phát hiện công trình bị hư hỏng, nguy cơ gây ra sự cố công trình, nguy cơ mất an toàn giao thông đường bộ thì phải xử lý, sửa chữa, khắc phục kịp thời; công khai về mốc lộ giới hành lang an toàn đường bộ theo quy định tại điểm c khoản 3 Điều 15 của Luật này, báo cáo và yêu cầu Ủy ban nhân dân cấp xã nơi có hành lang an toàn đường bộ bị lấn, chiếm, sử dụng trái phép để xử lý; thực hiện các công việc khác về quản lý, bảo vệ hành lang an toàn đường bộ theo quy định của Luật này, Luật Đất đai và quy định khác của pháp luật có liên quan.

### Điều khoản được nguồn trên dẫn chiếu tới (LUAT35-2024/D15/K3/c)
Mã điều khoản dùng được cho gold_units: LUAT35-2024/D15/K3/c

Điều 15. Hành lang an toàn đường bộ
3. Việc xác định và quản lý mốc lộ giới hành lang an toàn đường bộ được quy định như sau:
c) Cơ quan quản lý đường bộ, người quản lý, sử dụng đường bộ có trách nhiệm công bố công khai mốc lộ giới hành lang an toàn đường bộ; điều chỉnh, bổ sung mốc lộ giới hành lang an toàn đường bộ trong thời gian quản lý, vận hành, khai thác và bảo trì công trình đường bộ;

### Nguồn 2
Văn bản: Luật Đường bộ số 35/2024/QH15
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: LUAT35-2024/D15/K3, LUAT35-2024/D15/K3/a, LUAT35-2024/D15/K3/b, LUAT35-2024/D15/K3/c, LUAT35-2024/D15/K3/d

Điều 15. Hành lang an toàn đường bộ
3. Việc xác định và quản lý mốc lộ giới hành lang an toàn đường bộ được quy định như sau:
a) Mốc lộ giới hành lang an toàn đường bộ được xác định theo quy mô, cấp kỹ thuật, hướng tuyến, phạm vi xây dựng công trình đường bộ;
b) Chủ đầu tư xây dựng công trình đường bộ có trách nhiệm tổ chức thực hiện cắm mốc lộ giới hành lang an toàn đường bộ trong phạm vi dự án đầu tư xây dựng công trình đường bộ; bàn giao cho cơ quan quản lý đường bộ, người quản lý, sử dụng đường bộ;
c) Cơ quan quản lý đường bộ, người quản lý, sử dụng đường bộ có trách nhiệm công bố công khai mốc lộ giới hành lang an toàn đường bộ; điều chỉnh, bổ sung mốc lộ giới hành lang an toàn đường bộ trong thời gian quản lý, vận hành, khai thác và bảo trì công trình đường bộ;
d) Cơ quan quản lý đường bộ, người quản lý, sử dụng đường bộ, Ủy ban nhân dân các cấp có trách nhiệm quản lý mốc lộ giới hành lang an toàn đường bộ theo quy định của Luật này, quy định của pháp luật về đất đai và quy định khác của pháp luật có liên quan.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi mới học lái xe ô tô và vừa đi qua một công trình xây dựng đường, nơi mà không có biển báo giới hạn hành lang an toàn. Tôi muốn biết ai phải chịu trách nhiệm bảo vệ và công bố giới hạn này?
- Đáp: Bạn phải được người quản lý, sử dụng đường bộ thực hiện bảo vệ và công bố công khai mốc lộ giới hành lang an toàn đường bộ. Nếu công trình bị hư hỏng hoặc có nguy cơ gây sự cố, người quản lý phải xử lý, sửa chữa kịp thời và báo cáo Ủy ban nhân dân cấp xã. (Điều 21.3 c, Điều 15.3 c Luật Đường bộ số 35/2024/QH15)

```json
{"qid": "tD-da_buoc-026", "question": "Tôi mới học lái xe ô tô và vừa đi qua một công trình xây dựng đường, nơi mà không có biển báo giới hạn hành lang an toàn. Tôi muốn biết ai phải chịu trách nhiệm bảo vệ và công bố giới hạn này?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Bạn phải được người quản lý, sử dụng đường bộ thực hiện bảo vệ và công bố công khai mốc lộ giới hành lang an toàn đường bộ. Nếu công trình bị hư hỏng hoặc có nguy cơ gây sự cố, người quản lý phải xử lý, sửa chữa kịp thời và báo cáo Ủy ban nhân dân cấp xã. (Điều 21.3 c, Điều 15.3 c Luật Đường bộ số 35/2024/QH15)", "gold_units": ["LUAT35-2024/D21/K3", "LUAT35-2024/D15/K3/c"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-026:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi mới học lái xe ô tô và khi đi qua một đoạn đường đã có biển báo giới hạn hành lang an toàn, nhưng tôi không thấy có người công bố mốc lộ giới. Tôi muốn biết ai có trách nhiệm công bố và điều chỉnh mốc lộ này?
- Đáp: Cơ quan quản lý đường bộ, người quản lý hoặc sử dụng đường bộ có trách nhiệm công bố công khai mốc lộ giới hành lang an toàn đường bộ và điều chỉnh, bổ sung trong thời gian quản lý, vận hành, khai thác và bảo trì công trình đường bộ. (Điều 15.3 c, Điều 21.3 c Luật Đường bộ số 35/2024/QH15)

```json
{"qid": "tD-da_buoc-026", "question": "Tôi mới học lái xe ô tô và khi đi qua một đoạn đường đã có biển báo giới hạn hành lang an toàn, nhưng tôi không thấy có người công bố mốc lộ giới. Tôi muốn biết ai có trách nhiệm công bố và điều chỉnh mốc lộ này?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Cơ quan quản lý đường bộ, người quản lý hoặc sử dụng đường bộ có trách nhiệm công bố công khai mốc lộ giới hành lang an toàn đường bộ và điều chỉnh, bổ sung trong thời gian quản lý, vận hành, khai thác và bảo trì công trình đường bộ. (Điều 15.3 c, Điều 21.3 c Luật Đường bộ số 35/2024/QH15)", "gold_units": ["LUAT35-2024/D21/K3", "LUAT35-2024/D15/K3/c"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-026:2"}
```

### WD-da_buoc-027 · tier A · vai: người lớn tuổi đi xe đạp điện · kiểu: tinh_huong_ban_than · DAN_CHIEU → TT12-2025-BCA/D17/K3

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Thông tư số 12/2025/TT-BCA (Quy định về sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế)
Hiệu lực của trạng thái này: 2025-03-01 → nay
Mã điều khoản dùng được cho gold_units: TT12-2025-BCA/D37/K1, TT12-2025-BCA/D37/K1/a, TT12-2025-BCA/D37/K1/b, TT12-2025-BCA/D37/K1/c, TT12-2025-BCA/D37/K1/d, TT12-2025-BCA/D37/K1/đ, TT12-2025-BCA/D37/K1/e, TT12-2025-BCA/D37/K1/g, TT12-2025-BCA/D37/K1/h

Điều 37. Trách nhiệm Trung tâm sát hạch lái xe
1. Đối với công tác quản lý sát hạch
a) Bảo đảm cơ sở vật chất, trang thiết bị kiểm tra, chấm điểm theo quy định để thực hiện các kỳ sát hạch đạt kết quả chính xác, khách quan; báo cáo về Phòng Cảnh sát giao thông, Cục Cảnh sát giao thông khi thiết bị, phương tiện dùng cho sát hạch hoạt động không chính xác, không ổn định hoặc khi thay đổi thiết bị, phương tiện dùng cho sát hạch để xử lý kịp thời;
b) Phối hợp và tạo mọi điều kiện để học viên đến ôn luyện và các Hội đồng sát hạch tổ chức sát hạch thuận tiện, đúng kế hoạch;
c) Chấp hành và phối hợp với cơ quan có thẩm quyền trong việc kiểm tra trung tâm sát hạch lái xe;
d) Công khai mức thu phí sát hạch và giá các dịch vụ khác trên trang thông tin điện tử của trung tâm sát hạch lái xe;
đ) Bảo đảm an toàn cho các kỳ sát hạch lái xe; phối hợp các đơn vị, cơ quan liên quan giải quyết khi có các vụ việc tai nạn, mất an toàn xảy ra;
e) Công khai lịch sát hạch trên Trang thông tin điện tử của trung tâm sát hạch lái xe, lưu trữ hồ sơ kết quả sát hạch theo quy định tại khoản 3 Điều 17 Thông tư này;
…

### Điều khoản được nguồn trên dẫn chiếu tới (TT12-2025-BCA/D17/K3)
Mã điều khoản dùng được cho gold_units: TT12-2025-BCA/D17/K3

Điều 17. Lưu trữ hồ sơ kết quả sát hạch
3. Trung tâm sát hạch lái xe lưu trữ hồ sơ của kỳ sát hạch bao gồm:

### Nguồn 2
Văn bản: Thông tư số 12/2025/TT-BCA (Quy định về sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế)
Hiệu lực của trạng thái này: 2025-03-01 → nay
Mã điều khoản dùng được cho gold_units: TT12-2025-BCA/D17/K3, TT12-2025-BCA/D17/K3/a, TT12-2025-BCA/D17/K3/b, TT12-2025-BCA/D17/K3/c

Điều 17. Lưu trữ hồ sơ kết quả sát hạch
3. Trung tâm sát hạch lái xe lưu trữ hồ sơ của kỳ sát hạch bao gồm:
a) Các tài liệu quy định tại các điểm a, e, g khoản 1 Điều này;
b) Dữ liệu giám sát sát hạch; dữ liệu kết quả sát hạch lý thuyết, thực hành lái xe trong hình, phần mềm mô phỏng các tình huống giao thông và sát hạch thực hành lái xe trên đường;
c) Danh sách, kết quả sát hạch lái xe trên phần mềm mô phỏng các tình huống giao thông.

### Điều khoản được nguồn trên dẫn chiếu tới (TT12-2025-BCA/D17/K1/a)
Mã điều khoản dùng được cho gold_units: TT12-2025-BCA/D17/K1/a

Điều 17. Lưu trữ hồ sơ kết quả sát hạch
1. Sau mỗi kỳ sát hạch, Phòng Cảnh sát giao thông chịu trách nhiệm lưu trữ hồ sơ của kỳ sát hạch, bao gồm:
a) Quyết định tổ chức kỳ sát hạch lái xe;

### Điều khoản được nguồn trên dẫn chiếu tới (TT12-2025-BCA/D17/K1/e)
Mã điều khoản dùng được cho gold_units: TT12-2025-BCA/D17/K1/e

Điều 17. Lưu trữ hồ sơ kết quả sát hạch
1. Sau mỗi kỳ sát hạch, Phòng Cảnh sát giao thông chịu trách nhiệm lưu trữ hồ sơ của kỳ sát hạch, bao gồm:
e) Biên bản tổng hợp kết quả kỳ sát hạch;

### Điều khoản được nguồn trên dẫn chiếu tới (TT12-2025-BCA/D17/K1/g)
Mã điều khoản dùng được cho gold_units: TT12-2025-BCA/D17/K1/g

Điều 17. Lưu trữ hồ sơ kết quả sát hạch
1. Sau mỗi kỳ sát hạch, Phòng Cảnh sát giao thông chịu trách nhiệm lưu trữ hồ sơ của kỳ sát hạch, bao gồm:
g) Danh sách thí sinh đạt, vắng, trượt các nội dung sát hạch.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là người lớn tuổi đi xe đạp điện, khi tham gia kỳ sát hạch lái xe, tôi có thể yêu cầu trung tâm lưu trữ hồ sơ kết quả của mình không?
- Đáp: Trung tâm sát hạch lái xe phải lưu trữ hồ sơ kết quả kỳ sát hạch, bao gồm dữ liệu và biên bản tổng hợp, theo quy định. Đồng thời, trung tâm có trách nhiệm bảo đảm an toàn và công khai các hồ sơ này. (khoản 3 Điều 17 Thông tư 12/2025/TT-BCA)
- ⚠ chep_nguyen_van: “lưu trữ hồ sơ kết quả …”

```json
{"qid": "tD-da_buoc-027", "question": "Tôi là người lớn tuổi đi xe đạp điện, khi tham gia kỳ sát hạch lái xe, tôi có thể yêu cầu trung tâm lưu trữ hồ sơ kết quả của mình không?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Trung tâm sát hạch lái xe phải lưu trữ hồ sơ kết quả kỳ sát hạch, bao gồm dữ liệu và biên bản tổng hợp, theo quy định. Đồng thời, trung tâm có trách nhiệm bảo đảm an toàn và công khai các hồ sơ này. (khoản 3 Điều 17 Thông tư 12/2025/TT-BCA)", "gold_units": ["TT12-2025-BCA/D37/K1", "TT12-2025-BCA/D17/K3"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-027:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là người lớn tuổi đi xe đạp điện, sau khi hoàn thành kỳ sát hạch, tôi muốn biết trung tâm có phải lưu trữ và công khai hồ sơ kết quả của tôi không?
- Đáp: Trung tâm sát hạch lái xe phải lưu trữ hồ sơ kết quả kỳ sát hạch, bao gồm dữ liệu, biên bản tổng hợp và danh sách thí sinh, và có trách nhiệm công khai các hồ sơ này. (khoản 3 Điều 17 Thông tư 12/2025/TT-BCA)

```json
{"qid": "tD-da_buoc-027", "question": "Tôi là người lớn tuổi đi xe đạp điện, sau khi hoàn thành kỳ sát hạch, tôi muốn biết trung tâm có phải lưu trữ và công khai hồ sơ kết quả của tôi không?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Trung tâm sát hạch lái xe phải lưu trữ hồ sơ kết quả kỳ sát hạch, bao gồm dữ liệu, biên bản tổng hợp và danh sách thí sinh, và có trách nhiệm công khai các hồ sơ này. (khoản 3 Điều 17 Thông tư 12/2025/TT-BCA)", "gold_units": ["TT12-2025-BCA/D37/K1", "TT12-2025-BCA/D17/K3"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-027:2"}
```

### WD-da_buoc-029 · tier A · vai: tài xế xe tải · kiểu: ngan · DAN_CHIEU → TT79-2024-BCA/D9

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D20/K1

Điều 20. Thủ tục đổi chứng nhận đăng ký xe, biển số xe
1. Thực hiện dịch vụ công trực tuyến một phần hoặc làm thủ tục trực tiếp tại cơ quan đăng ký xe: Chủ xe kê khai giấy khai đăng ký xe theo quy định tại Điều 9 Thông tư này, nộp hồ sơ đổi chứng nhận đăng ký xe, biển số xe theo quy định tại Điều 19 Thông tư này và nộp lệ phí theo quy định. Trường hợp xe cải tạo, thay đổi màu sơn, chủ xe phải mang xe đến để kiểm tra.

### Điều khoản được nguồn trên dẫn chiếu tới (TT79-2024-BCA/D19)
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D19

Điều 19. Hồ sơ đổi chứng nhận đăng ký xe, biển số xe

### Điều khoản được nguồn trên dẫn chiếu tới (TT79-2024-BCA/D9)
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D9

Điều 9. Giấy khai đăng ký xe

### Nguồn 2
Văn bản: Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D9/K1

Điều 9. Giấy khai đăng ký xe
1. Trường hợp thực hiện đăng ký xe bằng dịch vụ công trực tuyến một phần: Chủ xe đăng nhập trên cổng dịch vụ công và kê khai chính xác, đầy đủ, trung thực các nội dung quy định trong mẫu giấy khai đăng ký xe, ký số. Trường hợp không có ký số thì chủ xe in giấy khai đăng ký xe từ cổng dịch vụ công, ký, ghi rõ họ, tên và đóng dấu (nếu là cơ quan, tổ chức).

### Nguồn 3
Văn bản: Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D9/K2

Điều 9. Giấy khai đăng ký xe
2. Trường hợp thực hiện đăng ký xe lần đầu bằng dịch vụ công trực tuyến toàn trình: Chủ xe sử dụng tài khoản định danh điện tử mức độ 2 để đăng nhập vào cổng dịch vụ công hoặc ứng dụng định danh quốc gia và kê khai chính xác, đầy đủ, trung thực các nội dung quy định trong mẫu giấy khai đăng ký xe và chủ xe không cần ký.

### Nguồn 4
Văn bản: Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D9/K3

Điều 9. Giấy khai đăng ký xe
3. Trường hợp thực hiện đăng ký xe trực tiếp tại cơ quan đăng ký xe: Chủ xe kê khai chính xác, đầy đủ, trung thực các nội dung quy định trong mẫu giấy khai đăng ký xe.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là tài xế xe tải, muốn đổi chứng nhận đăng ký xe và biển số, làm sao thực hiện thủ tục này?
- Đáp: Bạn cần thực hiện dịch vụ công trực tuyến một phần hoặc làm thủ tục trực tiếp tại cơ quan đăng ký xe, kê khai giấy khai đăng ký xe theo quy định tại Điều 9, nộp hồ sơ đổi chứng nhận đăng ký xe, biển số xe theo quy định tại Điều 19 và nộp lệ phí theo quy định.
- ⚠ chep_nguyen_van: “đổi chứng nhận đăng ký xe …”
- Ghi chú: Giả định xe tải đã được đăng ký trước đó và đang muốn đổi biển số

```json
{"qid": "tD-da_buoc-029", "question": "Tôi là tài xế xe tải, muốn đổi chứng nhận đăng ký xe và biển số, làm sao thực hiện thủ tục này?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Bạn cần thực hiện dịch vụ công trực tuyến một phần hoặc làm thủ tục trực tiếp tại cơ quan đăng ký xe, kê khai giấy khai đăng ký xe theo quy định tại Điều 9, nộp hồ sơ đổi chứng nhận đăng ký xe, biển số xe theo quy định tại Điều 19 và nộp lệ phí theo quy định.", "gold_units": ["TT79-2024-BCA/D20/K1", "TT79-2024-BCA/D19"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-029:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Nếu tôi đăng ký xe lần đầu bằng dịch vụ công trực tuyến toàn trình, tôi cần làm gì và nếu chỉ thực hiện một phần thì cần gì?
- Đáp: Bạn phải sử dụng tài khoản định danh điện tử mức độ 2 để đăng nhập vào cổng dịch vụ công hoặc ứng dụng định danh quốc gia, kê khai chính xác, đầy đủ, trung thực các nội dung quy định trong mẫu giấy khai đăng ký xe và không cần ký. Nếu thực hiện đăng ký bằng dịch vụ công trực tuyến một phần, bạn đăng nhập trên cổng dịch vụ công, kê khai chính xác, đầy đủ, trung thực các nội dung quy định trong mẫu giấy khai đăng ký xe, ký số; nếu không có ký số thì in giấy khai đăng ký xe từ cổng dịch vụ công, ký, ghi rõ họ, tên và đóng dấu (nếu là cơ quan, tổ chức).
- ⚠ chep_nguyen_van: “bằng dịch vụ công trực tuyến …”
- Ghi chú: Giả định tài xế chưa từng đăng ký xe trước đây

```json
{"qid": "tD-da_buoc-029", "question": "Nếu tôi đăng ký xe lần đầu bằng dịch vụ công trực tuyến toàn trình, tôi cần làm gì và nếu chỉ thực hiện một phần thì cần gì?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Bạn phải sử dụng tài khoản định danh điện tử mức độ 2 để đăng nhập vào cổng dịch vụ công hoặc ứng dụng định danh quốc gia, kê khai chính xác, đầy đủ, trung thực các nội dung quy định trong mẫu giấy khai đăng ký xe và không cần ký. Nếu thực hiện đăng ký bằng dịch vụ công trực tuyến một phần, bạn đăng nhập trên cổng dịch vụ công, kê khai chính xác, đầy đủ, trung thực các nội dung quy định trong mẫu giấy khai đăng ký xe, ký số; nếu không có ký số thì in giấy khai đăng ký xe từ cổng dịch vụ công, ký, ghi rõ họ, tên và đóng dấu (nếu là cơ quan, tổ chức).", "gold_units": ["TT79-2024-BCA/D9/K2", "TT79-2024-BCA/D9/K1"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-029:2"}
```

### WD-da_buoc-030 · tier A · vai: tài xế xe tải · kiểu: tinh_huong_nguoi_khac · DAN_CHIEU → TT14-2025-BXD/D17/K2

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Thông tư số 14/2025/TT-BXD (Quy định về đào tạo lái xe; bồi dưỡng, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ)
Hiệu lực của trạng thái này: 2025-09-01 → nay
Mã điều khoản dùng được cho gold_units: TT14-2025-BXD/D19/K4, TT14-2025-BXD/D19/K4/a, TT14-2025-BXD/D19/K4/b

Điều 19. Tổ chức bồi dưỡng kiến thức pháp luật về giao thông đường bộ cho người điều khiển xe máy chuyên dùng tham gia giao thông đường bộ
4. Kiểm tra:
a) Nội dung kiểm tra theo chương trình bồi dưỡng kiến thức pháp luật về giao thông đường bộ quy định tại khoản 2 Điều 17 Thông tư này;
b) Điểm đánh giá kết quả kiểm tra bồi dưỡng kiến thức pháp luật về giao thông đường bộ của học viên theo thang điểm 10 (từ 1 đến 10) do cơ sở bồi dưỡng xây dựng, có tính đến hàng thập phân 1 con số. Điểm kiểm tra từ 5,0 điểm trở lên thì đạt yêu cầu.

### Điều khoản được nguồn trên dẫn chiếu tới (TT14-2025-BXD/D17/K2)
Mã điều khoản dùng được cho gold_units: TT14-2025-BXD/D17/K2

Điều 17. Hình thức, chương trình bồi dưỡng kiến thức pháp luật về giao thông đường bộ
2. Chương trình bồi dưỡng kiến thức pháp luật về giao thông đường bộ:
TT | Nội dung chương trình | Số giờ
1 | Pháp luật về giao thông đường bộ | 12
2 | Quy chuẩn kỹ thuật quốc gia về báo hiệu đường bộ | 5
3 | Quy định về tốc độ và khoảng cách an toàn của xe cơ giới, xe máy chuyên dùng tham gia giao thông trên đường bộ | 3
4 | Quy định về xử lý vi phạm hành chính trong lĩnh vực giao thông đường bộ. | 4
5 | Quy định về cấp đăng ký, biển số; kiểm định xe máy chuyên dùng tham gia giao thông đường bộ | 3
6 | Ôn tập và kiểm tra | 5
Tổng thời gian đào tạo | 32

### Nguồn 2
Văn bản: Thông tư số 14/2025/TT-BXD (Quy định về đào tạo lái xe; bồi dưỡng, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ)
Hiệu lực của trạng thái này: 2025-09-01 → nay
Mã điều khoản dùng được cho gold_units: TT14-2025-BXD/D17/K2

Điều 17. Hình thức, chương trình bồi dưỡng kiến thức pháp luật về giao thông đường bộ
2. Chương trình bồi dưỡng kiến thức pháp luật về giao thông đường bộ:
TT | Nội dung chương trình | Số giờ
1 | Pháp luật về giao thông đường bộ | 12
2 | Quy chuẩn kỹ thuật quốc gia về báo hiệu đường bộ | 5
3 | Quy định về tốc độ và khoảng cách an toàn của xe cơ giới, xe máy chuyên dùng tham gia giao thông trên đường bộ | 3
4 | Quy định về xử lý vi phạm hành chính trong lĩnh vực giao thông đường bộ. | 4
5 | Quy định về cấp đăng ký, biển số; kiểm định xe máy chuyên dùng tham gia giao thông đường bộ | 3
6 | Ôn tập và kiểm tra | 5
Tổng thời gian đào tạo | 32

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Anh tôi là tài xế xe tải, công ty tôi vừa tổ chức buổi bồi dưỡng pháp luật. Anh tôi muốn biết mình cần học bao nhiêu giờ và điểm tối thiểu để được cấp chứng chỉ?
- Đáp: Bạn cần tham gia tổng cộng 32 giờ đào tạo và đạt điểm 5,0 trở lên để được cấp chứng chỉ.
- ⚠ chi_so_so_sai (0); so_la: 0
- Ghi chú: Giả định rằng “điểm tối thiểu” là 5,0 theo quy định.

```json
{"qid": "tD-da_buoc-030", "question": "Anh tôi là tài xế xe tải, công ty tôi vừa tổ chức buổi bồi dưỡng pháp luật. Anh tôi muốn biết mình cần học bao nhiêu giờ và điểm tối thiểu để được cấp chứng chỉ?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Bạn cần tham gia tổng cộng 32 giờ đào tạo và đạt điểm 5,0 trở lên để được cấp chứng chỉ.", "gold_units": ["TT14-2025-BXD/D19/K4", "TT14-2025-BXD/D19/K4/a"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-030:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Công ty tôi đang chuẩn bị tổ chức buổi bồi dưỡng pháp luật cho tài xế xe tải. Tôi muốn biết tổng thời gian đào tạo và điểm đánh giá cần đạt để được cấp chứng chỉ?
- Đáp: Tổng thời gian đào tạo là 32 giờ và điểm đánh giá cần đạt là 5,0 trở lên.
- ⚠ chi_so_so_sai (0)
- Ghi chú: Giả định rằng “điểm đánh giá cần đạt” là 5,0 theo quy định.

```json
{"qid": "tD-da_buoc-030", "question": "Công ty tôi đang chuẩn bị tổ chức buổi bồi dưỡng pháp luật cho tài xế xe tải. Tôi muốn biết tổng thời gian đào tạo và điểm đánh giá cần đạt để được cấp chứng chỉ?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Tổng thời gian đào tạo là 32 giờ và điểm đánh giá cần đạt là 5,0 trở lên.", "gold_units": ["TT14-2025-BXD/D19/K4", "TT14-2025-BXD/D19/K4/a"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-030:2"}
```

### WD-da_buoc-031 · tier A · vai: cán bộ phường · kiểu: tinh_huong_ban_than · DAN_CHIEU → ND168-2024/D42

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D46/K1

Điều 46. Thẩm quyền lập biên bản vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ
1. Các chức danh có thẩm quyền xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ được quy định tại Điều 42, Điều 43 và Điều 44 của Nghị định này.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D42)
Mã điều khoản dùng được cho gold_units: ND168-2024/D42

Điều 42. Thẩm quyền xử phạt của Chủ tịch Ủy ban nhân dân các cấp

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D43)
Mã điều khoản dùng được cho gold_units: ND168-2024/D43

Điều 43. Thẩm quyền xử phạt của Công an nhân dân

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D44)
Mã điều khoản dùng được cho gold_units: ND168-2024/D44

Điều 44. Thẩm quyền xử phạt của Cục trưởng Cục Đường bộ Việt Nam, Trưởng đoàn kiểm tra do Bộ trưởng Bộ Xây dựng thành lập, Giám đốc Sở Xây dựng, Trưởng đoàn kiểm tra do Cục trưởng Cục Đường bộ Việt Nam thành lập và Giám đốc Khu Quản lý đường bộ thuộc Cục Đường bộ Việt Nam

### Nguồn 2
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → 2026-08-14
Mã điều khoản dùng được cho gold_units: ND168-2024/D42/K3

Điều 42. Thẩm quyền xử phạt của Chủ tịch Ủy ban nhân dân các cấp
3. Chủ tịch Ủy ban nhân dân cấp tỉnh có quyền:
a) Phạt cảnh cáo;
b) Phạt tiền đến 75.000.000 đồng;
c) Tước quyền sử dụng giấy phép, chứng chỉ hành nghề có thời hạn hoặc đình chỉ hoạt động có thời hạn;
d) Tịch thu tang vật, phương tiện được sử dụng để vi phạm hành chính;
đ) Áp dụng biện pháp khắc phục hậu quả quy định tại khoản 3 Điều 3 của Nghị định này.

### Nguồn 3
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2026-08-15 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D42/K1, ND168-2024/D42/K1/a, ND168-2024/D42/K1/b, ND168-2024/D42/K1/c, ND168-2024/D42/K1/d, ND168-2024/D42/K1/đ

Điều 42. Thẩm quyền xử phạt của Chủ tịch Ủy ban nhân dân các cấp
1. Chủ tịch Ủy ban nhân dân cấp xã có quyền:
a) Phạt cảnh cáo;
b) Phạt tiền đến 37.500.000 đồng;
c) Tước quyền sử dụng giấy phép, chứng chỉ hành nghề có thời hạn hoặc đình chỉ hoạt động có thời hạn;
d) Tịch thu tang vật, phương tiện vi phạm hành chính;
đ) Áp dụng biện pháp khắc phục hậu quả quy định tại khoản 3 Điều 3 của Nghị định này.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D3/K3)
Mã điều khoản dùng được cho gold_units: ND168-2024/D3/K3

Điều 3. Hình thức xử phạt vi phạm hành chính, biện pháp khắc phục hậu quả; thu hồi giấy phép, chứng chỉ hành nghề
3. Các biện pháp khắc phục hậu quả vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ bao gồm:

### Nguồn 4
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2026-08-15 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D42/K2, ND168-2024/D42/K2/a, ND168-2024/D42/K2/b, ND168-2024/D42/K2/c, ND168-2024/D42/K2/d, ND168-2024/D42/K2/đ

Điều 42. Thẩm quyền xử phạt của Chủ tịch Ủy ban nhân dân các cấp
2. Chủ tịch Ủy ban nhân dân cấp tỉnh có quyền:
a) Phạt cảnh cáo;
b) Phạt tiền đến 75.000.000 đồng;
c) Tước quyền sử dụng giấy phép, chứng chỉ hành nghề có thời hạn hoặc đình chỉ hoạt động có thời hạn;
d) Tịch thu tang vật, phương tiện vi phạm hành chính;
đ) Áp dụng biện pháp khắc phục hậu quả quy định tại khoản 3 Điều 3 của Nghị định này.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D3/K3)
Mã điều khoản dùng được cho gold_units: ND168-2024/D3/K3

Điều 3. Hình thức xử phạt vi phạm hành chính, biện pháp khắc phục hậu quả; thu hồi giấy phép, chứng chỉ hành nghề
3. Các biện pháp khắc phục hậu quả vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ bao gồm:

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là cán bộ phường, vừa ghi nhận một xe ô tô chở khách vượt tốc độ 120 km/h trên đường tỉnh, có thể bị xử phạt như thế nào và ai có thẩm quyền thực hiện?
- Đáp: Theo quy định, Chủ tịch Ủy ban nhân dân cấp xã có quyền phạt tiền đến 37.500.000 đồng và áp dụng biện pháp khắc phục hậu quả. Khi vi phạm tốc độ quá mức, có thể bị phạt tiền tối đa 37.500.000 đồng và thực hiện biện pháp khắc phục hậu quả theo quy định. (Điều 42, Khoản 1; Điều 42, Khoản 1/b; Điều 42, Khoản 1/d)
- ⚠ chi_so_so_sai (0)
- Ghi chú: Giả định xe ô tô chở khách, tốc độ 120 km/h

```json
{"qid": "tD-da_buoc-031", "question": "Tôi là cán bộ phường, vừa ghi nhận một xe ô tô chở khách vượt tốc độ 120 km/h trên đường tỉnh, có thể bị xử phạt như thế nào và ai có thẩm quyền thực hiện?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Theo quy định, Chủ tịch Ủy ban nhân dân cấp xã có quyền phạt tiền đến 37.500.000 đồng và áp dụng biện pháp khắc phục hậu quả. Khi vi phạm tốc độ quá mức, có thể bị phạt tiền tối đa 37.500.000 đồng và thực hiện biện pháp khắc phục hậu quả theo quy định. (Điều 42, Khoản 1; Điều 42, Khoản 1/b; Điều 42, Khoản 1/d)", "gold_units": ["ND168-2024/D42", "ND168-2024/D42/K1/b", "ND168-2024/D42/K1/d"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-031:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là cán bộ phường, ghi nhận một xe tải chở hàng vượt tốc độ 90 km/h trên đường tỉnh, ai có thẩm quyền phạt và mức phạt tối đa là bao nhiêu?
- Đáp: Chủ tịch Ủy ban nhân dân cấp xã có thẩm quyền phạt tiền đến 37.500.000 đồng cho vi phạm tốc độ. (Điều 42, Khoản 1; Điều 42, Khoản 1/b)
- ⚠ chi_so_so_sai (0)
- Ghi chú: Giả định xe tải chở hàng, tốc độ 90 km/h

```json
{"qid": "tD-da_buoc-031", "question": "Tôi là cán bộ phường, ghi nhận một xe tải chở hàng vượt tốc độ 90 km/h trên đường tỉnh, ai có thẩm quyền phạt và mức phạt tối đa là bao nhiêu?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Chủ tịch Ủy ban nhân dân cấp xã có thẩm quyền phạt tiền đến 37.500.000 đồng cho vi phạm tốc độ. (Điều 42, Khoản 1; Điều 42, Khoản 1/b)", "gold_units": ["ND168-2024/D42", "ND168-2024/D42/K1/b"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-031:2"}
```

### WD-da_buoc-032 · tier A · vai: chủ doanh nghiệp vận tải · kiểu: neu_van_ban · DAN_CHIEU → LUAT36-2024/D34/K2

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Thông tư số 53/2024/TT-BGTVT (Quy định về phân loại phương tiện giao thông đường bộ và dấu hiệu nhận biết xe cơ giới sử dụng năng lượng sạch, năng lượng xanh, thân thiện môi trường)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: TT53-2024-BGTVT/D6

Điều 6. Xe thô sơ
Xe thô sơ gồm các loại xe được quy định tại khoản 2 Điều 34 Luật Trật tự, an toàn giao thông đường bộ.

### Điều khoản được nguồn trên dẫn chiếu tới (LUAT36-2024/D34/K2)
Mã điều khoản dùng được cho gold_units: LUAT36-2024/D34/K2

Điều 34. Phân loại phương tiện giao thông đường bộ
2. Xe thô sơ bao gồm:

### Nguồn 2
Văn bản: Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: LUAT36-2024/D34/K2, LUAT36-2024/D34/K2/a, LUAT36-2024/D34/K2/b, LUAT36-2024/D34/K2/c, LUAT36-2024/D34/K2/d, LUAT36-2024/D34/K2/đ, LUAT36-2024/D34/K2/e

Điều 34. Phân loại phương tiện giao thông đường bộ
2. Xe thô sơ bao gồm:
a) Xe đạp là xe có ít nhất hai bánh và vận hành do sức người thông qua bàn đạp hoặc tay quay;
b) Xe đạp máy, gồm cả xe đạp điện, là xe đạp có trợ lực từ động cơ, nguồn động lực từ động cơ bị ngắt khi người lái xe dừng đạp hoặc khi xe đạt tới tốc độ 25 km/h;
c) Xe xích lô;
d) Xe lăn dùng cho người khuyết tật;
đ) Xe vật nuôi kéo;
e) Xe tương tự các loại xe quy định tại khoản này.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Công ty tôi muốn sử dụng xe đạp để vận chuyển hàng hóa trong thành phố, liệu có bị xử phạt không?
- Đáp: Xe đạp được xem là xe thô sơ theo quy định. Việc sử dụng xe đạp để vận chuyển hàng hóa không vi phạm quy định về xe thô sơ. Tuy nhiên, nếu xe đạp không được đăng ký, có thể bị xử phạt theo quy định của Luật Trật tự, an toàn giao thông đường bộ.
- ⚠ da_buoc_it_hon_2_gold

```json
{"qid": "tD-da_buoc-032", "question": "Công ty tôi muốn sử dụng xe đạp để vận chuyển hàng hóa trong thành phố, liệu có bị xử phạt không?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Xe đạp được xem là xe thô sơ theo quy định. Việc sử dụng xe đạp để vận chuyển hàng hóa không vi phạm quy định về xe thô sơ. Tuy nhiên, nếu xe đạp không được đăng ký, có thể bị xử phạt theo quy định của Luật Trật tự, an toàn giao thông đường bộ.", "gold_units": ["LUAT36-2024/D34/K2/a"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-032:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Công ty tôi muốn thuê xe lăn để di chuyển người khuyết tật trong công ty, có cần đăng ký xe lăn không?
- Đáp: Xe lăn được xem là xe thô sơ theo quy định. Việc sử dụng xe lăn không vi phạm quy định về xe thô sơ. Tuy nhiên, nếu xe lăn không được đăng ký, có thể bị xử phạt theo quy định của Luật Trật tự, an toàn giao thông đường bộ.
- ⚠ da_buoc_it_hon_2_gold

```json
{"qid": "tD-da_buoc-032", "question": "Công ty tôi muốn thuê xe lăn để di chuyển người khuyết tật trong công ty, có cần đăng ký xe lăn không?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Xe lăn được xem là xe thô sơ theo quy định. Việc sử dụng xe lăn không vi phạm quy định về xe thô sơ. Tuy nhiên, nếu xe lăn không được đăng ký, có thể bị xử phạt theo quy định của Luật Trật tự, an toàn giao thông đường bộ.", "gold_units": ["LUAT36-2024/D34/K2/d"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-032:2"}
```

### WD-da_buoc-033 · tier A · vai: tài xế xe tải · kiểu: nhieu_dieu_kien · DAN_CHIEU → ND151-2024/PL4

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 151/2024/NĐ-CP (Quy định chi tiết một số điều và biện pháp thi hành Luật Trật tự, an toàn giao thông đường bộ)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND151-2024/D3/K4

Điều 3. Phụ lục kèm theo Nghị định
4. Phụ lục IV: Biểu mẫu liên quan đến chấp thuận doanh nghiệp kinh doanh dịch vụ lữ hành quốc tế của Việt Nam tổ chức cho người nước ngoài đưa xe cơ giới nước ngoài vào Việt Nam du lịch; tổ chức, cá nhân đưa xe ô tô có tay lái ở bên phải vào tham gia giao thông tại Việt Nam không phải mục đích du lịch.

### Điều khoản được nguồn trên dẫn chiếu tới (ND151-2024/PL4)
Mã điều khoản dùng được cho gold_units: ND151-2024/PL4

PHỤ LỤC IV
CÁC BIỂU MẪU LIÊN QUAN ĐẾN VIỆC CHẤP THUẬN DOANH NGHIỆP KINH DOANH DỊCH VỤ LỮ HÀNH QUỐC TẾ CỦA VIỆT NAM TỔ CHỨC CHO NGƯỜI NƯỚC NGOÀI ĐƯA XE CƠ GIỚI NƯỚC NGOÀI VÀO VIỆT NAM DU LỊCH HOẶC TỔ CHỨC, CÁ NHÂN ĐƯA XE Ô TÔ CÓ TAY LÁI Ở BÊN PHẢI VÀO THAM GIA GIAO THÔNG TẠI VIỆT NAM KHÔNG PHẢI MỤC ĐÍCH DU LỊCH
(Kèm theo Nghị định số 236/2026/NĐ-CP ngày 26 tháng 6 năm 2026 của Chính phủ)
Mẫu số 04a | Văn bản đề nghị chấp thuận tổ chức cho người nước ngoài đưa xe cơ giới nước ngoài vào Việt Nam du lịch; đưa xe ô
tô có tay lái ở bên phải vào tham gia giao thông tại Việt Nam không phải mục đích du lịch; thay đổi nội dung,
thông tin so với văn bản đã được chấp thuận
Mẫu số 04b | Văn bản chấp thuận tổ chức cho người nước ngoài đưa xe cơ giới nước ngoài vào Việt Nam du lịch; đưa xe ô tô có tay
lái ở bên phải vào tham gia giao thông tại Việt Nam không phải mục đích du lịch; thay đổi nội dung, thông tin so
với văn bản đã được chấp thuận
Mẫu số 04c | Văn bản đình chỉ hoạt động tổ chức cho người nước ngoài đưa xe cơ giới nước ngoài vào Việt Nam du lịch; đưa xe ô
tô có tay lái ở bên phải vào tham gia giao thông tại Việt Nam không phải mục đích du lịch
Mẫu số 04a. Văn bản đề nghị chấp thuận tổ chức cho người nước ngoài đưa xe cơ giới nước ngoài vào Việt Nam du lịch; đưa xe ô tô có tay lái ở bên phải vào tham gia giao thông tại Việt Nam không phải mục đích du lịch; thay đổi nội dung, thông tin so với văn bản đã được chấp thuận
.....(1)....... | CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
…

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là tài xế xe tải, có xe ô tô có tay lái bên phải muốn đưa vào Việt Nam để tham gia giao thông không phải du lịch. Tôi cần làm gì để được phép?
- Đáp: Bạn cần nộp văn bản đề nghị chấp thuận tổ chức cho người nước ngoài đưa xe cơ giới nước ngoài vào Việt Nam du lịch; đưa xe ô tô có tay lái ở bên phải vào tham gia giao thông tại Việt Nam không phải mục đích du lịch, theo mẫu số 04a của Phụ lục IV Nghị định số 151/2024/NĐ-CP. Sau khi được chấp thuận, xe của bạn sẽ được phép tham gia giao thông tại Việt Nam.
- ⚠ chep_nguyen_van: “xe ô tô có tay lái …”

```json
{"qid": "tD-da_buoc-033", "question": "Tôi là tài xế xe tải, có xe ô tô có tay lái bên phải muốn đưa vào Việt Nam để tham gia giao thông không phải du lịch. Tôi cần làm gì để được phép?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Bạn cần nộp văn bản đề nghị chấp thuận tổ chức cho người nước ngoài đưa xe cơ giới nước ngoài vào Việt Nam du lịch; đưa xe ô tô có tay lái ở bên phải vào tham gia giao thông tại Việt Nam không phải mục đích du lịch, theo mẫu số 04a của Phụ lục IV Nghị định số 151/2024/NĐ-CP. Sau khi được chấp thuận, xe của bạn sẽ được phép tham gia giao thông tại Việt Nam.", "gold_units": ["ND151-2024/D3/K4", "ND151-2024/PL4"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-033:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Nếu công ty tôi muốn tổ chức cho khách nước ngoài đưa xe ô tô có tay lái bên phải vào Việt Nam để tham gia giao thông không phải du lịch, tôi phải chuẩn bị tài liệu gì?
- Đáp: Công ty cần chuẩn bị văn bản chấp thuận tổ chức cho người nước ngoài đưa xe cơ giới nước ngoài vào Việt Nam du lịch; đưa xe ô tô có tay lái ở bên phải vào tham gia giao thông tại Việt Nam không phải mục đích du lịch, theo mẫu số 04b của Phụ lục IV Nghị định số 151/2024/NĐ-CP. Khi được chấp thuận, xe sẽ được phép tham gia giao thông.
- ⚠ chep_nguyen_van: “xe ô tô có tay lái …”

```json
{"qid": "tD-da_buoc-033", "question": "Nếu công ty tôi muốn tổ chức cho khách nước ngoài đưa xe ô tô có tay lái bên phải vào Việt Nam để tham gia giao thông không phải du lịch, tôi phải chuẩn bị tài liệu gì?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Công ty cần chuẩn bị văn bản chấp thuận tổ chức cho người nước ngoài đưa xe cơ giới nước ngoài vào Việt Nam du lịch; đưa xe ô tô có tay lái ở bên phải vào tham gia giao thông tại Việt Nam không phải mục đích du lịch, theo mẫu số 04b của Phụ lục IV Nghị định số 151/2024/NĐ-CP. Khi được chấp thuận, xe sẽ được phép tham gia giao thông.", "gold_units": ["ND151-2024/D3/K4", "ND151-2024/PL4"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-033:2"}
```

### WD-da_buoc-034 · tier A · vai: phụ huynh có con dưới 18 tuổi · kiểu: tinh_huong_ban_than · DAN_CHIEU → ND151-2024/PL4

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 151/2024/NĐ-CP (Quy định chi tiết một số điều và biện pháp thi hành Luật Trật tự, an toàn giao thông đường bộ)
Hiệu lực của trạng thái này: 2026-07-01 → nay
Mã điều khoản dùng được cho gold_units: ND151-2024/D33/K3

Điều 33. Chấp thuận doanh nghiệp kinh doanh dịch vụ lữ hành quốc tế của Việt Nam được tổ chức cho người nước ngoài đưa xe cơ giới nước ngoài vào Việt Nam du lịch hoặc tổ chức, cá nhân đưa xe ô tô có tay lái ở bên phải vào tham gia giao thông tại Việt Nam không phải mục đích du lịch
3. Trường hợp thay đổi nội dung, thông tin tại văn bản đã được chấp thuận trước đó (thay đổi lộ trình, tuyến đường di chuyển, thông tin của người nước ngoài, xe cơ giới nước ngoài hoặc thời gian người nước ngoài, xe cơ giới nước ngoài xuất cảnh chậm so với thời gian đã xác định trong văn bản chấp thuận hoặc quá thời gian lưu trú tối đa tại Việt Nam theo quy định của pháp luật về nhập cảnh, xuất cảnh, quá cảnh, cư trú của người nước ngoài tại Việt Nam) thì doanh nghiệp kinh doanh dịch vụ lữ hành quốc tế của Việt Nam hoặc tổ chức, cá nhân thông báo ngay với cơ quan có thẩm quyền đã cấp phép trước đó qua Ứng dụng giao thông trên thiết bị di động dành cho công dân do Bộ Công an quản lý, vận hành; nêu rõ lý do. Trong thời hạn 02 ngày kể từ ngày gửi thông báo, có bản chính hoặc bản điện tử văn bản theo Mẫu số 04a Phụ lục IV ban hành kèm theo Nghị định này gửi cơ quan có thẩm quyền đã cấp phép trước đó thông qua một trong các hình thức sau: trực tuyến trên Cổng Dịch vụ công quốc gia hoặc Ứng dụng định danh quốc gia; qua dịch vụ bưu chính; nộp trực tiếp.

### Điều khoản được nguồn trên dẫn chiếu tới (ND151-2024/PL4)
Mã điều khoản dùng được cho gold_units: ND151-2024/PL4

PHỤ LỤC IV
CÁC BIỂU MẪU LIÊN QUAN ĐẾN VIỆC CHẤP THUẬN DOANH NGHIỆP KINH DOANH DỊCH VỤ LỮ HÀNH QUỐC TẾ CỦA VIỆT NAM TỔ CHỨC CHO NGƯỜI NƯỚC NGOÀI ĐƯA XE CƠ GIỚI NƯỚC NGOÀI VÀO VIỆT NAM DU LỊCH HOẶC TỔ CHỨC, CÁ NHÂN ĐƯA XE Ô TÔ CÓ TAY LÁI Ở BÊN PHẢI VÀO THAM GIA GIAO THÔNG TẠI VIỆT NAM KHÔNG PHẢI MỤC ĐÍCH DU LỊCH
(Kèm theo Nghị định số 236/2026/NĐ-CP ngày 26 tháng 6 năm 2026 của Chính phủ)
Mẫu số 04a | Văn bản đề nghị chấp thuận tổ chức cho người nước ngoài đưa xe cơ giới nước ngoài vào Việt Nam du lịch; đưa xe ô
tô có tay lái ở bên phải vào tham gia giao thông tại Việt Nam không phải mục đích du lịch; thay đổi nội dung,
thông tin so với văn bản đã được chấp thuận
Mẫu số 04b | Văn bản chấp thuận tổ chức cho người nước ngoài đưa xe cơ giới nước ngoài vào Việt Nam du lịch; đưa xe ô tô có tay
lái ở bên phải vào tham gia giao thông tại Việt Nam không phải mục đích du lịch; thay đổi nội dung, thông tin so
với văn bản đã được chấp thuận
Mẫu số 04c | Văn bản đình chỉ hoạt động tổ chức cho người nước ngoài đưa xe cơ giới nước ngoài vào Việt Nam du lịch; đưa xe ô
tô có tay lái ở bên phải vào tham gia giao thông tại Việt Nam không phải mục đích du lịch
Mẫu số 04a. Văn bản đề nghị chấp thuận tổ chức cho người nước ngoài đưa xe cơ giới nước ngoài vào Việt Nam du lịch; đưa xe ô tô có tay lái ở bên phải vào tham gia giao thông tại Việt Nam không phải mục đích du lịch; thay đổi nội dung, thông tin so với văn bản đã được chấp thuận
.....(1)....... | CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
…

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là phụ huynh có con 15 tuổi, con sẽ tham gia giao thông với xe ô tô có tay lái bên phải của một công ty lữ hành quốc tế. Nếu kế hoạch di chuyển thay đổi, tôi cần làm gì để tuân thủ quy định?
- Đáp: Bạn phải thông báo ngay cho cơ quan có thẩm quyền đã cấp phép trước đó qua Ứng dụng giao thông trên thiết bị di động, nêu rõ lý do. Trong thời hạn 02 ngày kể từ ngày gửi thông báo, bạn phải gửi bản chính hoặc bản điện tử văn bản theo Mẫu số 04a. (Điều 33, Nghị định 151/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “xe ô tô có tay lái …”

```json
{"qid": "tD-da_buoc-034", "question": "Tôi là phụ huynh có con 15 tuổi, con sẽ tham gia giao thông với xe ô tô có tay lái bên phải của một công ty lữ hành quốc tế. Nếu kế hoạch di chuyển thay đổi, tôi cần làm gì để tuân thủ quy định?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Bạn phải thông báo ngay cho cơ quan có thẩm quyền đã cấp phép trước đó qua Ứng dụng giao thông trên thiết bị di động, nêu rõ lý do. Trong thời hạn 02 ngày kể từ ngày gửi thông báo, bạn phải gửi bản chính hoặc bản điện tử văn bản theo Mẫu số 04a. (Điều 33, Nghị định 151/2024/NĐ-CP)", "gold_units": ["ND151-2024/D33/K3", "ND151-2024/PL4"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-034:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Con tôi, 17 tuổi, sẽ lái xe ô tô có tay lái bên phải của một tổ chức lữ hành quốc tế khi tham gia giao thông tại Việt Nam không phải mục đích du lịch. Nếu có thay đổi thông tin về xe hoặc người lái, tôi phải làm gì?
- Đáp: Bạn phải thông báo ngay cho cơ quan có thẩm quyền đã cấp phép trước đó qua Ứng dụng giao thông trên thiết bị di động, nêu rõ lý do. Trong thời hạn 02 ngày kể từ ngày gửi thông báo, bạn phải gửi bản chính hoặc bản điện tử văn bản theo Mẫu số 04a. (Điều 33, Nghị định 151/2024/NĐ-CP)
- ⚠ qua_dai (51 từ); chep_nguyen_van: “gia giao thông tại việt nam …”

```json
{"qid": "tD-da_buoc-034", "question": "Con tôi, 17 tuổi, sẽ lái xe ô tô có tay lái bên phải của một tổ chức lữ hành quốc tế khi tham gia giao thông tại Việt Nam không phải mục đích du lịch. Nếu có thay đổi thông tin về xe hoặc người lái, tôi phải làm gì?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Bạn phải thông báo ngay cho cơ quan có thẩm quyền đã cấp phép trước đó qua Ứng dụng giao thông trên thiết bị di động, nêu rõ lý do. Trong thời hạn 02 ngày kể từ ngày gửi thông báo, bạn phải gửi bản chính hoặc bản điện tử văn bản theo Mẫu số 04a. (Điều 33, Nghị định 151/2024/NĐ-CP)", "gold_units": ["ND151-2024/D33/K3", "ND151-2024/PL4"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-034:2"}
```

### WD-da_buoc-035 · tier A · vai: chủ doanh nghiệp vận tải · kiểu: tinh_huong_ban_than · DAN_CHIEU → TT79-2024-BCA/D17/K1

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D29/K2, TT79-2024-BCA/D29/K2/a, TT79-2024-BCA/D29/K2/b

Điều 29. Thủ tục đăng ký xe
2. Chuyển quyền sở hữu xe không kèm theo biển số xe trúng đấu giá
a) Chủ xe nộp hồ sơ và làm thủ tục thu hồi theo quy định tại khoản 1 Điều 16, khoản 1 Điều 17 Thông tư này;
b) Tổ chức, cá nhân nhận chuyển quyền sở hữu xe nộp hồ sơ và làm thủ tục đăng ký sang tên xe theo quy định tại khoản 2 Điều 16, khoản 2 Điều 17 Thông tư này.

### Điều khoản được nguồn trên dẫn chiếu tới (TT79-2024-BCA/D16/K1)
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D16/K1

Điều 16. Hồ sơ đăng ký sang tên xe
1. Hồ sơ thu hồi

### Điều khoản được nguồn trên dẫn chiếu tới (TT79-2024-BCA/D17/K1)
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D17/K1

Điều 17. Thủ tục đăng ký sang tên xe
1. Thủ tục thu hồi

### Điều khoản được nguồn trên dẫn chiếu tới (TT79-2024-BCA/D16/K2)
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D16/K2

Điều 16. Hồ sơ đăng ký sang tên xe
2. Hồ sơ đăng ký

### Nguồn 2
Văn bản: Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D17/K1, TT79-2024-BCA/D17/K1/a, TT79-2024-BCA/D17/K1/b

Điều 17. Thủ tục đăng ký sang tên xe
1. Thủ tục thu hồi
a) Chủ xe kê khai giấy khai thu hồi chứng nhận đăng ký xe, biển số xe trên cổng dịch vụ công, cung cấp mã hồ sơ đăng ký xe trực tuyến hoặc kê khai giấy khai thu hồi chứng nhận đăng ký xe, biển số xe (theo mẫu ĐKX11 ban hành kèm theo Thông tư này) tại cơ quan đăng ký xe; nộp hồ sơ thu hồi quy định tại khoản 1 Điều 16 Thông tư này và nhận giấy hẹn trả kết quả chứng nhận thu hồi chứng nhận đăng ký xe, biển số xe theo quy định;
b) Sau khi kiểm tra hồ sơ xe hợp lệ, cơ quan đăng ký xe cấp 02 bản chứng nhận thu hồi chứng nhận đăng ký xe, biển số xe theo quy định có dán bản chà số máy, số khung và đóng dấu giáp lai của cơ quan đăng ký xe trên bản chà số máy, số khung xe (01 bản trả cho chủ xe, 01 bản lưu hồ sơ xe). Đối với xe tạm nhập, tái xuất của các đối tượng được hưởng quyền ưu đãi miễn trừ ngoại giao cấp 03 bản chứng nhận thu hồi chứng nhận đăng ký xe, biển số xe (02 bản trả cho chủ xe để nộp cho cơ quan hải quan và cơ quan đăng ký xe, 01 bản lưu hồ sơ xe).
Trường hợp chủ xe có nhu cầu thì được cấp chứng nhận đăng ký xe tạm thời cùng với chứng nhận thu hồi chứng nhận đăng ký xe, biển số xe, không phải có hồ sơ đăng ký xe tạm thời.

### Điều khoản được nguồn trên dẫn chiếu tới (TT79-2024-BCA/D16/K1)
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D16/K1

Điều 16. Hồ sơ đăng ký sang tên xe
1. Hồ sơ thu hồi

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là chủ doanh nghiệp vận tải, muốn chuyển quyền sở hữu xe mà không kèm biển số, cần làm gì để hoàn tất thủ tục?
- Đáp: Bạn phải nộp hồ sơ thu hồi theo quy định tại khoản 1 Điều 16 Thông tư 79/2024/TT-BCA và sau đó nộp hồ sơ đăng ký sang tên xe theo quy định tại khoản 2 Điều 16 Thông tư 79/2024/TT-BCA.

```json
{"qid": "tD-da_buoc-035", "question": "Tôi là chủ doanh nghiệp vận tải, muốn chuyển quyền sở hữu xe mà không kèm biển số, cần làm gì để hoàn tất thủ tục?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Bạn phải nộp hồ sơ thu hồi theo quy định tại khoản 1 Điều 16 Thông tư 79/2024/TT-BCA và sau đó nộp hồ sơ đăng ký sang tên xe theo quy định tại khoản 2 Điều 16 Thông tư 79/2024/TT-BCA.", "gold_units": ["TT79-2024-BCA/D29/K2", "TT79-2024-BCA/D16/K1"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-035:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là chủ doanh nghiệp vận tải, muốn thu hồi chứng nhận đăng ký xe và biển số, các bước cần thực hiện là gì?
- Đáp: Bạn phải kê khai giấy khai thu hồi chứng nhận đăng ký xe, biển số trên cổng dịch vụ công, nộp hồ sơ thu hồi theo khoản 1 Điều 16 Thông tư 79/2024/TT-BCA và nhận giấy hẹn trả kết quả. Sau khi kiểm tra, cơ quan đăng ký xe cấp bản chứng nhận thu hồi.
- ⚠ chep_nguyen_van: “hồi chứng nhận đăng ký xe …”

```json
{"qid": "tD-da_buoc-035", "question": "Tôi là chủ doanh nghiệp vận tải, muốn thu hồi chứng nhận đăng ký xe và biển số, các bước cần thực hiện là gì?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Bạn phải kê khai giấy khai thu hồi chứng nhận đăng ký xe, biển số trên cổng dịch vụ công, nộp hồ sơ thu hồi theo khoản 1 Điều 16 Thông tư 79/2024/TT-BCA và nhận giấy hẹn trả kết quả. Sau khi kiểm tra, cơ quan đăng ký xe cấp bản chứng nhận thu hồi.", "gold_units": ["TT79-2024-BCA/D17/K1", "TT79-2024-BCA/D16/K1"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-035:2"}
```

### WD-da_buoc-036 · tier A · vai: phụ huynh có con dưới 18 tuổi · kiểu: tinh_huong_nguoi_khac · DAN_CHIEU → LUAT36-2024/D37

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: LUAT36-2024/D36/K1

Điều 36. Biển số xe
1. Biển số xe do cơ quan nhà nước có thẩm quyền cấp theo quy định tại Điều 37 và Điều 39 của Luật này; được gắn vào phương tiện giao thông đường bộ theo quy định của Luật này để phục vụ quản lý nhà nước.

### Điều khoản được nguồn trên dẫn chiếu tới (LUAT36-2024/D37)
Mã điều khoản dùng được cho gold_units: LUAT36-2024/D37

Điều 37. Đấu giá biển số xe

### Điều khoản được nguồn trên dẫn chiếu tới (LUAT36-2024/D39)
Mã điều khoản dùng được cho gold_units: LUAT36-2024/D39

Điều 39. Cấp, thu hồi chứng nhận đăng ký xe và biển số xe cơ giới, xe máy chuyên dùng tham gia giao thông đường bộ

### Nguồn 2
Văn bản: Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: LUAT36-2024/D37/K1

Điều 37. Đấu giá biển số xe
1. Biển số xe đưa ra đấu giá là biển số xe ô tô, xe mô tô, xe gắn máy được quy định tại điểm c và điểm d khoản 2 Điều 36 của Luật này, được công khai để tổ chức, cá nhân lựa chọn đăng ký tham gia đấu giá. Biển số xe không được tổ chức, cá nhân lựa chọn để đăng ký tham gia đấu giá được chuyển vào hệ thống đăng ký, quản lý xe để đăng ký theo quy định của pháp luật.

### Điều khoản được nguồn trên dẫn chiếu tới (LUAT36-2024/D36/K2/c)
Mã điều khoản dùng được cho gold_units: LUAT36-2024/D36/K2/c

Điều 36. Biển số xe
2. Biển số xe được phân loại như sau:
c) Biển số xe nền màu vàng, chữ và số màu đen cấp cho xe hoạt động kinh doanh vận tải;

### Điều khoản được nguồn trên dẫn chiếu tới (LUAT36-2024/D36/K2/d)
Mã điều khoản dùng được cho gold_units: LUAT36-2024/D36/K2/d

Điều 36. Biển số xe
2. Biển số xe được phân loại như sau:
d) Biển số xe nền màu trắng, chữ và số màu đen cấp cho xe của các tổ chức, cá nhân trong nước, không thuộc đối tượng quy định tại các điểm a, b và c khoản này;

### Nguồn 3
Văn bản: Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: LUAT36-2024/D37/K2

Điều 37. Đấu giá biển số xe
2. Giá khởi điểm của một biển số xe ô tô đưa ra đấu giá không thấp hơn 40 triệu đồng; giá khởi điểm một biển số xe mô tô, xe gắn máy đưa ra đấu giá không thấp hơn 05 triệu đồng.

### Nguồn 4
Văn bản: Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: LUAT36-2024/D37/K3

Điều 37. Đấu giá biển số xe
3. Tiền đặt trước không thấp hơn giá khởi điểm của loại biển số xe đưa ra đấu giá.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Con tôi muốn đăng ký biển số xe nền màu trắng cho xe của gia đình, anh tôi đã tham gia đấu giá nhưng chưa biết quy trình và hậu quả nếu không đăng ký đúng quy định.
- Đáp: Để đăng ký biển số xe nền màu trắng, con bạn cần tham gia đấu giá theo quy định của Điều 37. Sau khi thắng đấu giá, biển số phải được đăng ký và cấp theo quy định của Điều 39. Nếu không đăng ký đúng quy định, xe sẽ bị thu hồi biển số và không được phép tham gia giao thông.
- ⚠ chep_nguyen_van: “biển số xe nền màu trắng …”

```json
{"qid": "tD-da_buoc-036", "question": "Con tôi muốn đăng ký biển số xe nền màu trắng cho xe của gia đình, anh tôi đã tham gia đấu giá nhưng chưa biết quy trình và hậu quả nếu không đăng ký đúng quy định.", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Để đăng ký biển số xe nền màu trắng, con bạn cần tham gia đấu giá theo quy định của Điều 37. Sau khi thắng đấu giá, biển số phải được đăng ký và cấp theo quy định của Điều 39. Nếu không đăng ký đúng quy định, xe sẽ bị thu hồi biển số và không được phép tham gia giao thông.", "gold_units": ["LUAT36-2024/D37", "LUAT36-2024/D39"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-036:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Công ty tôi muốn mua biển số xe nền màu vàng cho xe vận tải, anh tôi đã tham gia đấu giá nhưng chưa biết mức giá khởi điểm và tiền đặt trước cần nộp.
- Đáp: Mức giá khởi điểm cho biển số xe nền màu vàng (xe hoạt động kinh doanh vận tải) là 40 triệu đồng. Tiền đặt trước phải không thấp hơn giá khởi điểm này.
- ⚠ chi_so_so_sai (0); chi_so_so_sai (1); chep_nguyen_van: “biển số xe nền màu vàng …”

```json
{"qid": "tD-da_buoc-036", "question": "Công ty tôi muốn mua biển số xe nền màu vàng cho xe vận tải, anh tôi đã tham gia đấu giá nhưng chưa biết mức giá khởi điểm và tiền đặt trước cần nộp.", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Mức giá khởi điểm cho biển số xe nền màu vàng (xe hoạt động kinh doanh vận tải) là 40 triệu đồng. Tiền đặt trước phải không thấp hơn giá khởi điểm này.", "gold_units": ["LUAT36-2024/D37/K2", "LUAT36-2024/D37/K3"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-036:2"}
```

### WD-da_buoc-037 · tier A · vai: người mới học lái ô tô · kiểu: tinh_huong_nguoi_khac · DAN_CHIEU → LUAT35-2024/D36

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Luật Đường bộ số 35/2024/QH15
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: LUAT35-2024/D41/K1

Điều 41. Chi phí quản lý, vận hành, khai thác, bảo trì và bảo vệ kết cấu hạ tầng đường bộ
1. Chi phí quản lý, vận hành, khai thác, bảo trì và bảo vệ kết cấu hạ tầng đường bộ gồm chi phí cho các hoạt động quy định tại các điều 21, 35, 36 và 38 của Luật này.

### Điều khoản được nguồn trên dẫn chiếu tới (LUAT35-2024/D21)
Mã điều khoản dùng được cho gold_units: LUAT35-2024/D21

Điều 21. Bảo vệ kết cấu hạ tầng đường bộ

### Điều khoản được nguồn trên dẫn chiếu tới (LUAT35-2024/D35)
Mã điều khoản dùng được cho gold_units: LUAT35-2024/D35

Điều 35. Bảo trì kết cấu hạ tầng đường bộ

### Điều khoản được nguồn trên dẫn chiếu tới (LUAT35-2024/D36)
Mã điều khoản dùng được cho gold_units: LUAT35-2024/D36

Điều 36. Quản lý, vận hành, khai thác kết cấu hạ tầng đường bộ

### Nguồn 2
Văn bản: Luật Đường bộ số 35/2024/QH15
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: LUAT35-2024/D36/K1

Điều 36. Quản lý, vận hành, khai thác kết cấu hạ tầng đường bộ
1. Việc quản lý, vận hành, khai thác kết cấu hạ tầng đường bộ phải bảo đảm hiệu quả, bảo đảm giao thông thông suốt, an toàn và tuân thủ quy định của pháp luật.

### Nguồn 3
Văn bản: Luật Đường bộ số 35/2024/QH15
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: LUAT35-2024/D36/K2, LUAT35-2024/D36/K2/a, LUAT35-2024/D36/K2/b, LUAT35-2024/D36/K2/c, LUAT35-2024/D36/K2/d, LUAT35-2024/D36/K2/đ, LUAT35-2024/D36/K2/e, LUAT35-2024/D36/K2/g

Điều 36. Quản lý, vận hành, khai thác kết cấu hạ tầng đường bộ
2. Nội dung quản lý, vận hành, khai thác kết cấu hạ tầng đường bộ bao gồm:
a) Tiếp nhận công trình, thiết bị lắp đặt vào công trình, hồ sơ hoàn thành công trình sau khi hoàn thành việc đầu tư, xây dựng; lập, bảo quản hồ sơ quản lý kết cấu hạ tầng đường bộ;
b) Tổ chức giao thông theo quy định tại khoản 2 và khoản 3 Điều 25 của Luật này;
c) Bảo vệ kết cấu hạ tầng đường bộ; quản lý, sử dụng đất của đường bộ, hành lang an toàn đường bộ;
d) Quản lý, vận hành, khai thác hệ thống quản lý giao thông thông minh; trung tâm quản lý, điều hành giao thông tuyến đường cao tốc, công trình kiểm soát tải trọng xe, hệ thống thu phí và các thiết bị gắn vào kết cấu hạ tầng đường bộ;
đ) Thu thập, quản lý, sử dụng, vận hành, khai thác và cập nhật hệ thống cơ sở dữ liệu đường bộ;
e) Thực hiện công tác phòng, chống thiên tai trong lĩnh vực đường bộ theo quy định của pháp luật về phòng, chống thiên tai và quy định của Luật này;
g) Thực hiện các công việc khác theo quy định của Luật này, pháp luật về quản lý, sử dụng tài sản công và quy định khác của pháp luật có liên quan.

### Điều khoản được nguồn trên dẫn chiếu tới (LUAT35-2024/D25/K2)
Mã điều khoản dùng được cho gold_units: LUAT35-2024/D25/K2

Điều 25. Tổ chức giao thông
2. Nội dung tổ chức giao thông đường bộ trong giai đoạn thiết kế, thi công xây dựng, quản lý, vận hành, khai thác, sử dụng, bảo trì công trình đường bộ bao gồm:

### Điều khoản được nguồn trên dẫn chiếu tới (LUAT35-2024/D25/K3)
Mã điều khoản dùng được cho gold_units: LUAT35-2024/D25/K3

Điều 25. Tổ chức giao thông
3. Chủ đầu tư dự án đầu tư xây dựng công trình đường bộ, người quản lý, sử dụng đường bộ, tổ chức, cá nhân liên quan có trách nhiệm lắp đặt, điều chỉnh, bổ sung đầy đủ báo hiệu đường bộ, công trình an toàn giao thông đường bộ đối với dự án và tuyến đường thuộc phạm vi quản lý; thực hiện phương án tổ chức giao thông đường cao tốc được phê duyệt.

### Nguồn 4
Văn bản: Luật Đường bộ số 35/2024/QH15
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: LUAT35-2024/D36/K3

Điều 36. Quản lý, vận hành, khai thác kết cấu hạ tầng đường bộ
3. Bộ trưởng Bộ Giao thông vận tải quy định chi tiết Điều này.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Anh tôi đang làm công việc bảo trì đường, anh ấy phải chi trả chi phí quản lý, vận hành, khai thác, bảo trì và bảo vệ kết cấu hạ tầng đường bộ. Anh ấy cũng phải đảm bảo giao thông thông suốt, an toàn và tuân thủ quy định pháp luật. Tôi muốn biết chi phí này bao gồm những hoạt động nào và điều kiện gì để đảm bảo an toàn?
- Đáp: Chi phí quản lý, vận hành, khai thác, bảo trì và bảo vệ kết cấu hạ tầng đường bộ bao gồm chi phí cho các hoạt động quy định tại các điều 21, 35, 36 và 38 của Luật Đường bộ. Việc quản lý, vận hành, khai thác kết cấu hạ tầng đường bộ phải bảo đảm hiệu quả, bảo đảm giao thông thông suốt, an toàn và tuân thủ quy định của pháp luật.
- ⚠ qua_dai (73 từ); chep_nguyen_van: “an toàn và tuân thủ quy …”
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-da_buoc-037", "question": "Anh tôi đang làm công việc bảo trì đường, anh ấy phải chi trả chi phí quản lý, vận hành, khai thác, bảo trì và bảo vệ kết cấu hạ tầng đường bộ. Anh ấy cũng phải đảm bảo giao thông thông suốt, an toàn và tuân thủ quy định pháp luật. Tôi muốn biết chi phí này bao gồm những hoạt động nào và điều kiện gì để đảm bảo an toàn?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Chi phí quản lý, vận hành, khai thác, bảo trì và bảo vệ kết cấu hạ tầng đường bộ bao gồm chi phí cho các hoạt động quy định tại các điều 21, 35, 36 và 38 của Luật Đường bộ. Việc quản lý, vận hành, khai thác kết cấu hạ tầng đường bộ phải bảo đảm hiệu quả, bảo đảm giao thông thông suốt, an toàn và tuân thủ quy định của pháp luật.", "gold_units": ["LUAT35-2024/D41/K1", "LUAT35-2024/D36/K1"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-037:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Công ty tôi đang xây dựng công trình đường cao tốc, chúng tôi cần lắp đặt báo hiệu và điều chỉnh an toàn giao thông. Tôi muốn biết trách nhiệm của chủ đầu tư và người quản lý trong việc lắp đặt báo hiệu, cũng như cách tổ chức giao thông?
- Đáp: Chủ đầu tư dự án đầu tư xây dựng công trình đường bộ, người quản lý, sử dụng đường bộ, tổ chức, cá nhân liên quan có trách nhiệm lắp đặt, điều chỉnh, bổ sung đầy đủ báo hiệu đường bộ, công trình an toàn giao thông đường bộ đối với dự án và tuyến đường thuộc phạm vi quản lý; thực hiện phương án tổ chức giao thông đường cao tốc được phê duyệt. Nội dung quản lý, vận hành, khai thác kết cấu hạ tầng đường bộ bao gồm: a) Tiếp nhận công trình, thiết bị lắp đặt vào công trình, hồ sơ hoàn thành công trình sau khi hoàn thành việc đầu tư, xây dựng; lập, bảo quản hồ sơ quản lý kết cấu hạ tầng đường bộ; b) Tổ chức giao thông theo quy định tại khoản 2 và khoản 3 Điều 25 của Luật này; c) Bảo vệ kết cấu hạ tầng đường bộ; quản lý, sử dụng đất của đường bộ, hành lang an toàn đường bộ; d) Quản lý, vận hành, khai thác hệ thống quản lý giao thông thông minh; trung tâm quản lý, điều hành giao thông tuyến đường cao tốc, công trình kiểm soát tải trọng xe, hệ thống thu phí và các thiết bị gắn vào kết cấu hạ tầng đường bộ; e) Thu thập, quản lý, sử dụng, vận hành, khai thác và cập nhật hệ thống cơ sở dữ liệu đường bộ; f) Thực hiện công tác phòng, chống thiên tai trong lĩnh vực đường bộ theo quy định của pháp luật về phòng, chống thiên tai và quy định của Luật này; g) Thực hiện các công việc khác theo quy định của Luật này, pháp luật về quản lý, sử dụng tài sản công và quy định khác của pháp luật có liên quan.
- ⚠ qua_dai (51 từ)
- Ghi chú: Giả định công ty đang thực hiện dự án xây dựng đường cao tốc

```json
{"qid": "tD-da_buoc-037", "question": "Công ty tôi đang xây dựng công trình đường cao tốc, chúng tôi cần lắp đặt báo hiệu và điều chỉnh an toàn giao thông. Tôi muốn biết trách nhiệm của chủ đầu tư và người quản lý trong việc lắp đặt báo hiệu, cũng như cách tổ chức giao thông?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Chủ đầu tư dự án đầu tư xây dựng công trình đường bộ, người quản lý, sử dụng đường bộ, tổ chức, cá nhân liên quan có trách nhiệm lắp đặt, điều chỉnh, bổ sung đầy đủ báo hiệu đường bộ, công trình an toàn giao thông đường bộ đối với dự án và tuyến đường thuộc phạm vi quản lý; thực hiện phương án tổ chức giao thông đường cao tốc được phê duyệt. Nội dung quản lý, vận hành, khai thác kết cấu hạ tầng đường bộ bao gồm: a) Tiếp nhận công trình, thiết bị lắp đặt vào công trình, hồ sơ hoàn thành công trình sau khi hoàn thành việc đầu tư, xây dựng; lập, bảo quản hồ sơ quản lý kết cấu hạ tầng đường bộ; b) Tổ chức giao thông theo quy định tại khoản 2 và khoản 3 Điều 25 của Luật này; c) Bảo vệ kết cấu hạ tầng đường bộ; quản lý, sử dụng đất của đường bộ, hành lang an toàn đường bộ; d) Quản lý, vận hành, khai thác hệ thống quản lý giao thông thông minh; trung tâm quản lý, điều hành giao thông tuyến đường cao tốc, công trình kiểm soát tải trọng xe, hệ thống thu phí và các thiết bị gắn vào kết cấu hạ tầng đường bộ; e) Thu thập, quản lý, sử dụng, vận hành, khai thác và cập nhật hệ thống cơ sở dữ liệu đường bộ; f) Thực hiện công tác phòng, chống thiên tai trong lĩnh vực đường bộ theo quy định của pháp luật về phòng, chống thiên tai và quy định của Luật này; g) Thực hiện các công việc khác theo quy định của Luật này, pháp luật về quản lý, sử dụng tài sản công và quy định khác của pháp luật có liên quan.", "gold_units": ["LUAT35-2024/D36/K2", "LUAT35-2024/D25/K3"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-037:2"}
```

### WD-da_buoc-041 · tier A · vai: cán bộ phường · kiểu: nhieu_dieu_kien · DAN_CHIEU → ND151-2024/D10/K3

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 151/2024/NĐ-CP (Quy định chi tiết một số điều và biện pháp thi hành Luật Trật tự, an toàn giao thông đường bộ)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND151-2024/D13/K2

Điều 13. Cập nhật thông tin trong Cơ sở dữ liệu về trật tự, an toàn giao thông đường bộ
2. Cơ quan trực tiếp xây dựng, quản lý, vận hành, khai thác, sử dụng cơ sở dữ liệu quy định tại khoản 3 Điều 10 của Nghị định này có trách nhiệm bổ sung, điều chỉnh thông tin trong cơ sở dữ liệu do mình quản lý và đồng bộ với Cơ sở dữ liệu về trật tự, an toàn giao thông đường bộ theo quy định của pháp luật về kết nối và chia sẻ dữ liệu.

### Điều khoản được nguồn trên dẫn chiếu tới (ND151-2024/D10/K3)
Mã điều khoản dùng được cho gold_units: ND151-2024/D10/K3

Điều 10. Xây dựng Cơ sở dữ liệu về trật tự, an toàn giao thông đường bộ và cơ sở dữ liệu chuyên ngành
3. Trách nhiệm xây dựng, quản lý cơ sở dữ liệu chuyên ngành:

### Nguồn 2
Văn bản: Nghị định số 151/2024/NĐ-CP (Quy định chi tiết một số điều và biện pháp thi hành Luật Trật tự, an toàn giao thông đường bộ)
Hiệu lực của trạng thái này: 2026-07-01 → nay
Mã điều khoản dùng được cho gold_units: ND151-2024/D10/K3, ND151-2024/D10/K3/a, ND151-2024/D10/K3/b, ND151-2024/D10/K3/c, ND151-2024/D10/K3/d, ND151-2024/D10/K3/đ

Điều 10. Xây dựng Cơ sở dữ liệu về trật tự, an toàn giao thông đường bộ và cơ sở dữ liệu chuyên ngành
3. Trách nhiệm xây dựng, quản lý cơ sở dữ liệu chuyên ngành:
a) Bộ Công an có trách nhiệm xây dựng, quản lý cơ sở dữ liệu sau đây: Cơ sở dữ liệu về đăng ký, quản lý xe cơ giới, xe máy chuyên dùng (trừ xe quân sự); Cơ sở dữ liệu về xử lý vi phạm hành chính về trật tự, an toàn giao thông đường bộ; Cơ sở dữ liệu về tai nạn giao thông đường bộ; Cơ sở dữ liệu về hành trình của phương tiện giao thông đường bộ, hình ảnh người lái xe (trừ xe quân sự); Cơ sở dữ liệu về quản lý thời gian điều khiển phương tiện của người lái xe (trừ xe quân sự); Cơ sở dữ liệu về đăng kiểm xe cơ giới, xe máy chuyên dùng trong Công an nhân dân; Cơ sở dữ liệu về sát hạch, cấp giấy phép lái xe; Cơ sở dữ liệu về đào tạo lái xe, chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ trong Công an nhân dân; Cơ sở dữ liệu về xe cơ giới nước ngoài do người nước ngoài điều khiển tham gia giao thông tại Việt Nam;
b) Bộ Xây dựng có trách nhiệm xây dựng, quản lý cơ sở dữ liệu sau đây: Cơ sở dữ liệu về đăng kiểm xe cơ giới, xe máy chuyên dùng (trừ xe quân sự, xe công an); Cơ sở dữ liệu về đào tạo lái xe, chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ cho người điều khiển xe máy chuyên dùng (trừ dữ liệu về đào tạo lái xe, chứng chỉ bồi dưỡng kiến thức pháp luật của lực lượng quân đội, công an); Cơ sở dữ liệu về đơn vị kinh doanh vận tải và phù hiệu xe kinh doanh vận tải;
…

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là cán bộ phường, muốn biết khi nào cơ quan quản lý giao thông phải cập nhật thông tin vi phạm vào cơ sở dữ liệu, và trách nhiệm của cơ quan nào trong việc xây dựng cơ sở dữ liệu chuyên ngành liên quan đến vi phạm giao thông?
- Đáp: Cơ quan trực tiếp xây dựng, quản lý, vận hành, khai thác, sử dụng cơ sở dữ liệu phải bổ sung, điều chỉnh thông tin và đồng bộ với Cơ sở dữ liệu về trật tự, an toàn giao thông đường bộ. Ngoài ra, Bộ Công an có trách nhiệm xây dựng và quản lý cơ sở dữ liệu về xử lý vi phạm hành chính về trật tự, an toàn giao thông đường bộ.
- ⚠ qua_dai (51 từ); chep_nguyen_van: “cơ sở dữ liệu chuyên ngành …”
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-da_buoc-041", "question": "Tôi là cán bộ phường, muốn biết khi nào cơ quan quản lý giao thông phải cập nhật thông tin vi phạm vào cơ sở dữ liệu, và trách nhiệm của cơ quan nào trong việc xây dựng cơ sở dữ liệu chuyên ngành liên quan đến vi phạm giao thông?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Cơ quan trực tiếp xây dựng, quản lý, vận hành, khai thác, sử dụng cơ sở dữ liệu phải bổ sung, điều chỉnh thông tin và đồng bộ với Cơ sở dữ liệu về trật tự, an toàn giao thông đường bộ. Ngoài ra, Bộ Công an có trách nhiệm xây dựng và quản lý cơ sở dữ liệu về xử lý vi phạm hành chính về trật tự, an toàn giao thông đường bộ.", "gold_units": ["ND151-2024/D13/K2", "ND151-2024/D10/K3"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-041:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Nếu một cơ quan địa phương muốn cập nhật dữ liệu tai nạn giao thông vào hệ thống, họ cần thực hiện những bước nào và cơ quan nào chịu trách nhiệm xây dựng cơ sở dữ liệu tai nạn?
- Đáp: Cơ quan địa phương phải bổ sung, điều chỉnh thông tin trong cơ sở dữ liệu của mình và đồng bộ với Cơ sở dữ liệu về trật tự, an toàn giao thông đường bộ. Bộ Công an chịu trách nhiệm xây dựng và quản lý cơ sở dữ liệu về tai nạn giao thông đường bộ.
- ⚠ chep_nguyen_van: “xây dựng cơ sở dữ liệu …”
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-da_buoc-041", "question": "Nếu một cơ quan địa phương muốn cập nhật dữ liệu tai nạn giao thông vào hệ thống, họ cần thực hiện những bước nào và cơ quan nào chịu trách nhiệm xây dựng cơ sở dữ liệu tai nạn?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Cơ quan địa phương phải bổ sung, điều chỉnh thông tin trong cơ sở dữ liệu của mình và đồng bộ với Cơ sở dữ liệu về trật tự, an toàn giao thông đường bộ. Bộ Công an chịu trách nhiệm xây dựng và quản lý cơ sở dữ liệu về tai nạn giao thông đường bộ.", "gold_units": ["ND151-2024/D13/K2", "ND151-2024/D10/K3"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-041:2"}
```

### WD-da_buoc-042 · tier A · vai: cán bộ phường · kiểu: tinh_huong_ban_than · DAN_CHIEU → LUAT36-2024/D73/K1

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: LUAT36-2024/D69/K2

Điều 69. Di chuyển phương tiện vi phạm dừng, đỗ trên đường bộ gây cản trở, ùn tắc giao thông hoặc nguy cơ dẫn đến tai nạn giao thông đường bộ
2. Khi người điều khiển phương tiện tham gia giao thông đường bộ hoặc chủ phương tiện giao thông đường bộ có hành vi cản trở, chống đối việc di chuyển phương tiện vi phạm ra khỏi vị trí dừng, đỗ thì Cảnh sát giao thông thực hiện các biện pháp quy định tại khoản 1 Điều 73 của Luật này, nếu người đó vẫn tiếp tục cản trở, chống đối thì Cảnh sát giao thông được cưỡng chế thi hành.

### Điều khoản được nguồn trên dẫn chiếu tới (LUAT36-2024/D73/K1)
Mã điều khoản dùng được cho gold_units: LUAT36-2024/D73/K1

Điều 73. Ngăn chặn hành vi không chấp hành yêu cầu kiểm tra, kiểm soát, cản trở, chống người thi hành công vụ
1. Khi người tham gia giao thông đường bộ không chấp hành yêu cầu kiểm tra, kiểm soát, có hành vi cản trở, chống người thi hành công vụ thì người thi hành công vụ thực hiện các biện pháp sau đây:

### Nguồn 2
Văn bản: Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: LUAT36-2024/D73/K1, LUAT36-2024/D73/K1/a, LUAT36-2024/D73/K1/b, LUAT36-2024/D73/K1/c

Điều 73. Ngăn chặn hành vi không chấp hành yêu cầu kiểm tra, kiểm soát, cản trở, chống người thi hành công vụ
1. Khi người tham gia giao thông đường bộ không chấp hành yêu cầu kiểm tra, kiểm soát, có hành vi cản trở, chống người thi hành công vụ thì người thi hành công vụ thực hiện các biện pháp sau đây:
a) Giải thích cho người vi phạm biết rõ về hành vi không chấp hành yêu cầu kiểm tra, kiểm soát, có hành vi cản trở, chống người thi hành công vụ; quyền và trách nhiệm của người vi phạm; thuyết phục, yêu cầu chấm dứt ngay hành vi vi phạm, chấp hành yêu cầu kiểm tra, kiểm soát;
b) Áp dụng các biện pháp ngăn chặn theo quy định của pháp luật trong trường hợp người vi phạm cản trở, không chấp hành yêu cầu kiểm tra, kiểm soát của người thi hành công vụ;
c) Trường hợp người vi phạm có hành vi chống người thi hành công vụ thì tùy theo tình huống, tính chất, mức độ nguy hiểm của hành vi, người thi hành công vụ được sử dụng vũ lực, công cụ hỗ trợ hoặc vũ khí theo quy định của pháp luật để ngăn chặn hành vi vi phạm và phòng vệ chính đáng.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi thấy một chiếc xe tải đang dừng lại trên đường, gây cản trở giao thông. Nếu chủ xe không dừng lại khi cảnh sát yêu cầu, họ sẽ bị xử lý như thế nào?
- Đáp: Nếu chủ xe không dừng lại khi cảnh sát yêu cầu, cảnh sát sẽ thực hiện các biện pháp quy định tại khoản 1 Điều 73 của Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15. Nếu chủ xe vẫn tiếp tục cản trở, cảnh sát được cưỡng chế thi hành.

```json
{"qid": "tD-da_buoc-042", "question": "Tôi thấy một chiếc xe tải đang dừng lại trên đường, gây cản trở giao thông. Nếu chủ xe không dừng lại khi cảnh sát yêu cầu, họ sẽ bị xử lý như thế nào?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Nếu chủ xe không dừng lại khi cảnh sát yêu cầu, cảnh sát sẽ thực hiện các biện pháp quy định tại khoản 1 Điều 73 của Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15. Nếu chủ xe vẫn tiếp tục cản trở, cảnh sát được cưỡng chế thi hành.", "gold_units": ["LUAT36-2024/D69/K2", "LUAT36-2024/D73/K1"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-042:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi thấy một chiếc xe máy dừng trên đường, gây ùn tắc. Nếu chủ xe không chấp hành yêu cầu của cảnh sát, họ sẽ bị xử lý như thế nào?
- Đáp: Nếu chủ xe không chấp hành yêu cầu của cảnh sát, cảnh sát sẽ thực hiện các biện pháp quy định tại khoản 1 Điều 73 của Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15. Nếu chủ xe vẫn tiếp tục cản trở, cảnh sát được cưỡng chế thi hành.

```json
{"qid": "tD-da_buoc-042", "question": "Tôi thấy một chiếc xe máy dừng trên đường, gây ùn tắc. Nếu chủ xe không chấp hành yêu cầu của cảnh sát, họ sẽ bị xử lý như thế nào?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Nếu chủ xe không chấp hành yêu cầu của cảnh sát, cảnh sát sẽ thực hiện các biện pháp quy định tại khoản 1 Điều 73 của Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15. Nếu chủ xe vẫn tiếp tục cản trở, cảnh sát được cưỡng chế thi hành.", "gold_units": ["LUAT36-2024/D69/K2", "LUAT36-2024/D73/K1"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-042:2"}
```

### WD-da_buoc-043 · tier A · vai: tài xế xe tải · kiểu: ngan · DAN_CHIEU → LUAT36-2024/D13

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: LUAT36-2024/D14/K1

Điều 14. Vượt xe và nhường đường cho xe xin vượt
1. Vượt xe là tình huống giao thông trên đường mà mỗi chiều đường xe chạy chỉ có một làn đường dành cho xe cơ giới, xe đi phía sau di chuyển sang bên trái để di chuyển lên trước xe phía trước.
Trên đường có từ hai làn đường dành cho xe cơ giới cùng chiều trở lên được phân biệt bằng vạch kẻ đường, xe đi phía sau di chuyển lên trước xe phía trước thì áp dụng quy tắc sử dụng làn đường quy định tại Điều 13 của Luật này.

### Điều khoản được nguồn trên dẫn chiếu tới (LUAT36-2024/D13)
Mã điều khoản dùng được cho gold_units: LUAT36-2024/D13

Điều 13. Sử dụng làn đường

### Nguồn 2
Văn bản: Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: LUAT36-2024/D13/K1

Điều 13. Sử dụng làn đường
1. Phương tiện tham gia giao thông đường bộ di chuyển với tốc độ thấp hơn phải đi về bên phải theo chiều đi của mình.

### Nguồn 3
Văn bản: Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: LUAT36-2024/D13/K2

Điều 13. Sử dụng làn đường
2. Trên đường có nhiều làn đường cho xe đi cùng chiều được phân biệt bằng vạch kẻ phân làn đường, người điều khiển phương tiện tham gia giao thông đường bộ phải cho xe đi trong một làn đường và chỉ được chuyển làn đường ở những nơi cho phép; mỗi lần chuyển làn đường chỉ được phép chuyển sang một làn đường liền kề; khi chuyển làn đường phải có tín hiệu báo trước; phải quan sát bảo đảm khoảng cách an toàn với xe phía trước, phía sau và hai bên mới được chuyển làn.

### Nguồn 4
Văn bản: Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: LUAT36-2024/D13/K3

Điều 13. Sử dụng làn đường
3. Trên một chiều đường có vạch kẻ phân làn đường, xe thô sơ phải đi trên làn đường bên phải trong cùng, xe cơ giới, xe máy chuyên dùng đi trên làn đường bên trái.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi đang lái xe tải trên đường một chiều, có xe nhỏ phía sau, có thể vượt qua không? Nếu có, phải làm gì?
- Đáp: Bạn có thể vượt qua xe phía sau khi đường một chiều chỉ có một làn, nhưng phải di chuyển sang bên trái để vượt qua. Khi di chuyển sang bên trái, bạn phải tuân thủ quy tắc sử dụng làn đường, tức là di chuyển về bên phải khi tốc độ thấp hơn. (Điều 14 và Điều 13 Khoản 1 Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15)
- Ghi chú: Giả định xe nhỏ đang di chuyển cùng chiều

```json
{"qid": "tD-da_buoc-043", "question": "Tôi đang lái xe tải trên đường một chiều, có xe nhỏ phía sau, có thể vượt qua không? Nếu có, phải làm gì?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Bạn có thể vượt qua xe phía sau khi đường một chiều chỉ có một làn, nhưng phải di chuyển sang bên trái để vượt qua. Khi di chuyển sang bên trái, bạn phải tuân thủ quy tắc sử dụng làn đường, tức là di chuyển về bên phải khi tốc độ thấp hơn. (Điều 14 và Điều 13 Khoản 1 Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15)", "gold_units": ["LUAT36-2024/D14/K1", "LUAT36-2024/D13/K1"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-043:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi đang lái xe tải trên đường một chiều, có xe nhỏ phía sau, tôi muốn vượt qua nhưng không muốn chuyển sang làn trái, có thể không?
- Đáp: Bạn có thể vượt qua xe phía sau khi đường một chiều chỉ có một làn, nhưng phải di chuyển sang bên trái để vượt qua. Khi di chuyển sang bên trái, bạn phải tuân thủ quy tắc sử dụng làn đường, tức là di chuyển về bên phải khi tốc độ thấp hơn. (Điều 14 và Điều 13 Khoản 1 Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15)
- Ghi chú: Giả định xe nhỏ đang di chuyển cùng chiều

```json
{"qid": "tD-da_buoc-043", "question": "Tôi đang lái xe tải trên đường một chiều, có xe nhỏ phía sau, tôi muốn vượt qua nhưng không muốn chuyển sang làn trái, có thể không?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Bạn có thể vượt qua xe phía sau khi đường một chiều chỉ có một làn, nhưng phải di chuyển sang bên trái để vượt qua. Khi di chuyển sang bên trái, bạn phải tuân thủ quy tắc sử dụng làn đường, tức là di chuyển về bên phải khi tốc độ thấp hơn. (Điều 14 và Điều 13 Khoản 1 Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15)", "gold_units": ["LUAT36-2024/D14/K1", "LUAT36-2024/D13/K1"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-043:2"}
```

### WD-da_buoc-046 · tier A · vai: sinh viên đi xe máy · kiểu: tinh_huong_ban_than · DAN_CHIEU → ND168-2024/D42

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D45/K2

Điều 45. Nguyên tắc xác định thẩm quyền xử phạt vi phạm hành chính và áp dụng biện pháp khắc phục hậu quả
2. Thẩm quyền xử phạt vi phạm hành chính của các chức danh quy định tại Điều 42, Điều 43 và Điều 44 của Nghị định này là thẩm quyền áp dụng đối với một hành vi vi phạm hành chính của cá nhân; trong trường hợp phạt tiền, thẩm quyền xử phạt tổ chức gấp 02 lần thẩm quyền xử phạt cá nhân.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D42)
Mã điều khoản dùng được cho gold_units: ND168-2024/D42

Điều 42. Thẩm quyền xử phạt của Chủ tịch Ủy ban nhân dân các cấp

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D43)
Mã điều khoản dùng được cho gold_units: ND168-2024/D43

Điều 43. Thẩm quyền xử phạt của Công an nhân dân

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D44)
Mã điều khoản dùng được cho gold_units: ND168-2024/D44

Điều 44. Thẩm quyền xử phạt của Cục trưởng Cục Đường bộ Việt Nam, Trưởng đoàn kiểm tra do Bộ trưởng Bộ Xây dựng thành lập, Giám đốc Sở Xây dựng, Trưởng đoàn kiểm tra do Cục trưởng Cục Đường bộ Việt Nam thành lập và Giám đốc Khu Quản lý đường bộ thuộc Cục Đường bộ Việt Nam

### Nguồn 2
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → 2026-08-14
Mã điều khoản dùng được cho gold_units: ND168-2024/D42/K3

Điều 42. Thẩm quyền xử phạt của Chủ tịch Ủy ban nhân dân các cấp
3. Chủ tịch Ủy ban nhân dân cấp tỉnh có quyền:
a) Phạt cảnh cáo;
b) Phạt tiền đến 75.000.000 đồng;
c) Tước quyền sử dụng giấy phép, chứng chỉ hành nghề có thời hạn hoặc đình chỉ hoạt động có thời hạn;
d) Tịch thu tang vật, phương tiện được sử dụng để vi phạm hành chính;
đ) Áp dụng biện pháp khắc phục hậu quả quy định tại khoản 3 Điều 3 của Nghị định này.

### Nguồn 3
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2026-08-15 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D42/K1, ND168-2024/D42/K1/a, ND168-2024/D42/K1/b, ND168-2024/D42/K1/c, ND168-2024/D42/K1/d, ND168-2024/D42/K1/đ

Điều 42. Thẩm quyền xử phạt của Chủ tịch Ủy ban nhân dân các cấp
1. Chủ tịch Ủy ban nhân dân cấp xã có quyền:
a) Phạt cảnh cáo;
b) Phạt tiền đến 37.500.000 đồng;
c) Tước quyền sử dụng giấy phép, chứng chỉ hành nghề có thời hạn hoặc đình chỉ hoạt động có thời hạn;
d) Tịch thu tang vật, phương tiện vi phạm hành chính;
đ) Áp dụng biện pháp khắc phục hậu quả quy định tại khoản 3 Điều 3 của Nghị định này.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D3/K3)
Mã điều khoản dùng được cho gold_units: ND168-2024/D3/K3

Điều 3. Hình thức xử phạt vi phạm hành chính, biện pháp khắc phục hậu quả; thu hồi giấy phép, chứng chỉ hành nghề
3. Các biện pháp khắc phục hậu quả vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ bao gồm:

### Nguồn 4
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2026-08-15 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D42/K2, ND168-2024/D42/K2/a, ND168-2024/D42/K2/b, ND168-2024/D42/K2/c, ND168-2024/D42/K2/d, ND168-2024/D42/K2/đ

Điều 42. Thẩm quyền xử phạt của Chủ tịch Ủy ban nhân dân các cấp
2. Chủ tịch Ủy ban nhân dân cấp tỉnh có quyền:
a) Phạt cảnh cáo;
b) Phạt tiền đến 75.000.000 đồng;
c) Tước quyền sử dụng giấy phép, chứng chỉ hành nghề có thời hạn hoặc đình chỉ hoạt động có thời hạn;
d) Tịch thu tang vật, phương tiện vi phạm hành chính;
đ) Áp dụng biện pháp khắc phục hậu quả quy định tại khoản 3 Điều 3 của Nghị định này.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D3/K3)
Mã điều khoản dùng được cho gold_units: ND168-2024/D3/K3

Điều 3. Hình thức xử phạt vi phạm hành chính, biện pháp khắc phục hậu quả; thu hồi giấy phép, chứng chỉ hành nghề
3. Các biện pháp khắc phục hậu quả vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ bao gồm:

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi bị cảnh sát phạt tiền khi vi phạm giao thông, ai có thẩm quyền xử phạt và mức phạt tối đa là bao nhiêu?
- Đáp: Công an nhân dân có thẩm quyền xử phạt vi phạm hành chính của cá nhân và phạt tiền tối đa 75.000.000 đồng. (Điều 43 và Điều 42 khoản 3 Nghị định 168/2024/NĐ-CP)
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-da_buoc-046", "question": "Tôi bị cảnh sát phạt tiền khi vi phạm giao thông, ai có thẩm quyền xử phạt và mức phạt tối đa là bao nhiêu?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Công an nhân dân có thẩm quyền xử phạt vi phạm hành chính của cá nhân và phạt tiền tối đa 75.000.000 đồng. (Điều 43 và Điều 42 khoản 3 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D43", "ND168-2024/D42/K3"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-046:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi bị cảnh sát phạt tiền và sau đó bị Chủ tịch UBND cấp tỉnh phạt thêm, ai có thẩm quyền xử phạt và mức phạt tối đa là bao nhiêu?
- Đáp: Công an nhân dân có thẩm quyền xử phạt vi phạm hành chính của cá nhân và phạt tiền tối đa 75.000.000 đồng. Chủ tịch UBND cấp tỉnh cũng có thẩm quyền và phạt tiền tối đa 75.000.000 đồng. (Điều 43 và Điều 42 khoản 3 Nghị định 168/2024/NĐ-CP)
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-da_buoc-046", "question": "Tôi bị cảnh sát phạt tiền và sau đó bị Chủ tịch UBND cấp tỉnh phạt thêm, ai có thẩm quyền xử phạt và mức phạt tối đa là bao nhiêu?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Công an nhân dân có thẩm quyền xử phạt vi phạm hành chính của cá nhân và phạt tiền tối đa 75.000.000 đồng. Chủ tịch UBND cấp tỉnh cũng có thẩm quyền và phạt tiền tối đa 75.000.000 đồng. (Điều 43 và Điều 42 khoản 3 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D43", "ND168-2024/D42/K3"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-046:2"}
```

### WD-da_buoc-049 · tier A · vai: sinh viên đi xe máy · kiểu: ngan · DAN_CHIEU → TT12-2025-BCA/D23

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Thông tư số 12/2025/TT-BCA (Quy định về sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế)
Hiệu lực của trạng thái này: 2025-03-01 → nay
Mã điều khoản dùng được cho gold_units: TT12-2025-BCA/D18/K3

Điều 18. Mẫu giấy phép lái xe, sử dụng, quản lý giấy phép lái xe
3. Cá nhân nếu có nhu cầu tích hợp giấy phép lái xe không thời hạn với giấy phép lái xe có thời hạn thì đăng ký vào đề nghị đổi giấy phép lái xe quy định tại Phụ lục XII ban hành kèm theo Thông tư này, làm thủ tục đổi giấy phép lái xe theo quy định tại Điều 21, 22, 23 của Thông tư này.

### Điều khoản được nguồn trên dẫn chiếu tới (TT12-2025-BCA/D21)
Mã điều khoản dùng được cho gold_units: TT12-2025-BCA/D21

Điều 21. Đổi giấy phép lái xe

### Điều khoản được nguồn trên dẫn chiếu tới (TT12-2025-BCA/D22)
Mã điều khoản dùng được cho gold_units: TT12-2025-BCA/D22

Điều 22. Đổi giấy phép lái xe quân sự do Bộ Quốc phòng cấp

### Điều khoản được nguồn trên dẫn chiếu tới (TT12-2025-BCA/D23)
Mã điều khoản dùng được cho gold_units: TT12-2025-BCA/D23

Điều 23. Đổi giấy phép lái xe trong Công an nhân dân

### Nguồn 2
Văn bản: Thông tư số 12/2025/TT-BCA (Quy định về sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế)
Hiệu lực của trạng thái này: 2025-03-01 → nay
Mã điều khoản dùng được cho gold_units: TT12-2025-BCA/D23/K1, TT12-2025-BCA/D23/K1/a, TT12-2025-BCA/D23/K1/b, TT12-2025-BCA/D23/K1/c

Điều 23. Đổi giấy phép lái xe trong Công an nhân dân
1. Yêu cầu đối với việc đổi giấy phép lái xe trong Công an nhân dân khi thôi không còn phục vụ trong lực lượng Công an
a) Người có giấy phép lái xe còn thời hạn sử dụng; bị mất, bị hỏng nhưng vẫn còn thời hạn sử dụng, có thông tin trong hệ thống thông tin giấy phép lái xe tại Cục Cảnh sát giao thông hoặc bảng kê danh sách cấp giấy phép lái xe (sổ quản lý) có nhu cầu được đổi giấy phép lái xe;
b) Người có giấy phép lái xe mô tô bằng vật liệu giấy, không bị tẩy xóa, rách nát, có đủ thông tin trong giấy phép lái xe có nhu cầu được đổi giấy phép lái xe;
c) Không đổi giấy phép lái xe trong trường hợp bị tẩy xóa thông tin; người vi phạm trật tự, an toàn giao thông đường bộ chưa thực hiện xong yêu cầu của cơ quan nhà nước có thẩm quyền về giải quyết, xử lý vụ việc vi phạm hành chính trong lĩnh vực trật tự, an toàn giao thông đường bộ; người không có thông tin trong hệ thống thông tin giấy phép lái xe tại Cục Cảnh sát giao thông hoặc bảng kê danh sách cấp giấy phép lái xe (sổ quản lý).

### Nguồn 3
Văn bản: Thông tư số 12/2025/TT-BCA (Quy định về sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế)
Hiệu lực của trạng thái này: 2025-03-01 → nay
Mã điều khoản dùng được cho gold_units: TT12-2025-BCA/D23/K2, TT12-2025-BCA/D23/K2/a, TT12-2025-BCA/D23/K2/b, TT12-2025-BCA/D23/K2/c, TT12-2025-BCA/D23/K2/d

Điều 23. Đổi giấy phép lái xe trong Công an nhân dân
2. Hồ sơ đổi giấy phép lái xe
a) Đề nghị đổi giấy phép lái xe theo quy định tại Phụ lục XII ban hành kèm theo Thông tư này;
b) Bản sao giấy phép lái xe trong trường hợp không có thông tin trong hệ thống thông tin giấy phép lái xe tại Cục Cảnh sát giao thông hoặc bảng kê danh sách cấp giấy phép lái xe (sổ quản lý); bản cam kết trong trường hợp giấy phép lái xe bị mất;
c) Bản sao giấy tờ chứng minh thôi không còn phục vụ trong lực lượng Công an nhân dân;
d) Giấy khám sức khỏe của người lái xe do cơ sở khám bệnh, chữa bệnh đủ tiêu chuẩn theo quy định của pháp luật về khám bệnh, chữa bệnh cấp còn hiệu lực.

### Nguồn 4
Văn bản: Thông tư số 12/2025/TT-BCA (Quy định về sát hạch, cấp giấy phép lái xe; cấp, sử dụng giấy phép lái xe quốc tế)
Hiệu lực của trạng thái này: 2025-03-01 → nay
Mã điều khoản dùng được cho gold_units: TT12-2025-BCA/D23/K3, TT12-2025-BCA/D23/K3/a, TT12-2025-BCA/D23/K3/b, TT12-2025-BCA/D23/K3/c, TT12-2025-BCA/D23/K3/d

Điều 23. Đổi giấy phép lái xe trong Công an nhân dân
3. Trình tự thực hiện
a) Cá nhân lập 01 bộ hồ sơ theo quy định tại khoản 2 Điều này gửi trực tiếp đến Phòng Cảnh sát giao thông hoặc Công an cấp xã nơi được bố trí điểm tiếp nhận; cá nhân chụp ảnh trực tiếp tại cơ quan tiếp nhận hồ sơ, xuất trình bản chính các giấy tờ quy định tại điểm c khoản 2 Điều này để đối chiếu và phải hoàn thành nghĩa vụ nộp lệ phí khi được tiếp nhận hồ sơ;
b) Phòng Cảnh sát giao thông hoặc Công an cấp xã nơi được bố trí điểm tiếp nhận kiểm tra hồ sơ khi tiếp nhận và tra cứu phần mềm cơ sở dữ liệu về trật tự, an toàn giao thông đường bộ hoặc tra cứu vi phạm của người lái xe thông qua tài khoản định danh điện tử. Trường hợp phát hiện có nghi vấn, Phòng Cảnh sát giao thông có văn bản đề nghị đơn vị cấp giấy phép lái xe xác minh giấy phép lái xe đã cấp theo mẫu số 01 Phụ lục XI ban hành kèm theo Thông tư này, khi chưa có kết quả xác minh giấy phép lái xe thì chưa đổi giấy phép lái xe.
Trường hợp giấy phép lái xe không thuộc đối tượng được đổi thì phải thông báo về việc không tiếp nhận hồ sơ; trường hợp hồ sơ không đúng theo quy định thì hướng dẫn những nội dung cần bổ sung hoặc sửa đổi cho cá nhân trong thời hạn 02 ngày làm việc, kể từ ngày nhận hồ sơ.
Phòng Cảnh sát giao thông hoặc Công an cấp xã nơi được bố trí điểm tiếp nhận nhập thông tin điện tử, in phiếu hẹn trả kết quả;
…

### Điều khoản được nguồn trên dẫn chiếu tới (TT12-2025-BCA/D23/K2)
Mã điều khoản dùng được cho gold_units: TT12-2025-BCA/D23/K2

Điều 23. Đổi giấy phép lái xe trong Công an nhân dân
2. Hồ sơ đổi giấy phép lái xe

### Điều khoản được nguồn trên dẫn chiếu tới (TT12-2025-BCA/D23/K2/c)
Mã điều khoản dùng được cho gold_units: TT12-2025-BCA/D23/K2/c

Điều 23. Đổi giấy phép lái xe trong Công an nhân dân
2. Hồ sơ đổi giấy phép lái xe
c) Bản sao giấy tờ chứng minh thôi không còn phục vụ trong lực lượng Công an nhân dân;

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi muốn đổi giấy phép lái xe mô tô vì đã hết hạn, làm sao để nộp hồ sơ và có thể nhận giấy mới?
- Đáp: Bạn cần nộp đề nghị đổi giấy phép theo mẫu Phụ lục XII, kèm bản sao giấy phép cũ, bản cam kết khi mất, giấy khám sức khỏe, và bản sao giấy tờ chứng minh thôi không còn phục vụ trong lực lượng Công an nhân dân. Sau khi hồ sơ được tiếp nhận, bạn sẽ được thông báo kết quả trong vòng 2 ngày làm việc. (Điều 23, khoản 2, 3 của Thông tư 12/2025/TT-BCA)
- ⚠ chi_so_so_sai (0); chep_nguyen_van: “giấy phép lái xe mô tô …”
- Ghi chú: Giả định người hỏi là người có giấy phép mô tô còn hạn, muốn đổi vì hết hạn

```json
{"qid": "tD-da_buoc-049", "question": "Tôi muốn đổi giấy phép lái xe mô tô vì đã hết hạn, làm sao để nộp hồ sơ và có thể nhận giấy mới?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Bạn cần nộp đề nghị đổi giấy phép theo mẫu Phụ lục XII, kèm bản sao giấy phép cũ, bản cam kết khi mất, giấy khám sức khỏe, và bản sao giấy tờ chứng minh thôi không còn phục vụ trong lực lượng Công an nhân dân. Sau khi hồ sơ được tiếp nhận, bạn sẽ được thông báo kết quả trong vòng 2 ngày làm việc. (Điều 23, khoản 2, 3 của Thông tư 12/2025/TT-BCA)", "gold_units": ["TT12-2025-BCA/D23/K2", "TT12-2025-BCA/D23/K2/c"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-049:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Con tôi vừa thôi công tác trong lực lượng Công an, muốn đổi giấy phép lái xe mô tô, cần chuẩn bị những giấy tờ nào?
- Đáp: Con cần nộp đề nghị đổi giấy phép theo mẫu Phụ lục XII, kèm bản sao giấy phép cũ, bản cam kết khi mất, bản sao giấy tờ chứng minh thôi không còn phục vụ trong lực lượng Công an nhân dân, và giấy khám sức khỏe. Hồ sơ sẽ được kiểm tra và kết quả trả về trong vòng 2 ngày làm việc. (Điều 23, khoản 2, 3 của Thông tư 12/2025/TT-BCA)
- ⚠ chi_so_so_sai (0); chep_nguyen_van: “giấy phép lái xe mô tô …”
- Ghi chú: Giả định con là người có giấy phép mô tô còn hạn, muốn đổi vì thôi công tác

```json
{"qid": "tD-da_buoc-049", "question": "Con tôi vừa thôi công tác trong lực lượng Công an, muốn đổi giấy phép lái xe mô tô, cần chuẩn bị những giấy tờ nào?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Con cần nộp đề nghị đổi giấy phép theo mẫu Phụ lục XII, kèm bản sao giấy phép cũ, bản cam kết khi mất, bản sao giấy tờ chứng minh thôi không còn phục vụ trong lực lượng Công an nhân dân, và giấy khám sức khỏe. Hồ sơ sẽ được kiểm tra và kết quả trả về trong vòng 2 ngày làm việc. (Điều 23, khoản 2, 3 của Thông tư 12/2025/TT-BCA)", "gold_units": ["TT12-2025-BCA/D23/K2", "TT12-2025-BCA/D23/K2/c"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-049:2"}
```

### WD-da_buoc-052 · tier A · vai: cán bộ phường · kiểu: tinh_huong_ban_than · DAN_CHIEU → ND151-2024/PL3

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 151/2024/NĐ-CP (Quy định chi tiết một số điều và biện pháp thi hành Luật Trật tự, an toàn giao thông đường bộ)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND151-2024/D3/K3

Điều 3. Phụ lục kèm theo Nghị định
3. Phụ lục III: Biểu mẫu liên quan đến cấp giấy phép hoạt động phương tiện giao thông thông minh.

### Điều khoản được nguồn trên dẫn chiếu tới (ND151-2024/PL3)
Mã điều khoản dùng được cho gold_units: ND151-2024/PL3

PHỤ LỤC III
BIỂU MẪU LIÊN QUAN ĐẾN CẤP GIẤY PHÉP HOẠT ĐỘNG PHƯƠNG TIỆN GIAO THÔNG THÔNG MINH
(Kèm theo Nghị định số 236/2026/NĐ-CP ngày 26 tháng 6 năm 2026 của Chính phủ)
Mẫu số 03a | Đơn đề nghị cấp/đổi/cấp lại giấy phép hoạt động phương tiện giao thông thông minh
Mẫu số 03b | Giấy phép hoạt động phương tiện giao thông thông minh
Mẫu số 03a. Đơn đề nghị cấp/đổi/cấp lại giấy phép hoạt động phương tiện giao thông thông minh
.....(1)....... | CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM
------- | Độc lập - Tự do - Hạnh phúc
Số: .......... | ............, ngày ... tháng ... năm .....
V/v đề nghị cấp/đổi/cấp lại giấy phép hoạt động
phương tiện giao thông thông minh
Kính gửi: ...........(2)........................
1. Tên chủ sở hữu phương tiện: ........................................
- Địa chỉ:..................................
- Số định danh cá nhân/số hộ chiếu/mã số thuế:..................................cấp ngày.....tháng.... năm ......cơ quan cấp:..................................
- Quốc tịch (đối với cá nhân):..................................
- Điện thoại:.................................. email:..................................
Có phương tiện giao thông thông minh, đặc điểm như sau:
- Biển số:.................................. màu biển số:..................................
- Nhãn hiệu:.................................. số loại:..................................
- Loại xe:.................................. dung tích:..................................
…

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là trưởng phường, muốn đăng ký giấy phép hoạt động phương tiện giao thông thông minh cho xe ô tô chở khách của công ty mình. Tôi cần làm gì và có phải nộp mẫu đơn nào không?
- Đáp: Bạn cần nộp Đơn đề nghị cấp/đổi/cấp lại giấy phép hoạt động phương tiện giao thông thông minh (mẫu số 03a) và kèm theo giấy phép hoạt động phương tiện giao thông thông minh (mẫu số 03b).
- ⚠ chep_nguyen_van: “giấy phép hoạt động phương tiện …”

```json
{"qid": "tD-da_buoc-052", "question": "Tôi là trưởng phường, muốn đăng ký giấy phép hoạt động phương tiện giao thông thông minh cho xe ô tô chở khách của công ty mình. Tôi cần làm gì và có phải nộp mẫu đơn nào không?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Bạn cần nộp Đơn đề nghị cấp/đổi/cấp lại giấy phép hoạt động phương tiện giao thông thông minh (mẫu số 03a) và kèm theo giấy phép hoạt động phương tiện giao thông thông minh (mẫu số 03b).", "gold_units": ["ND151-2024/D3/K3", "ND151-2024/PL3"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-052:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là chủ sở hữu một xe ô tô chở khách, muốn xin cấp giấy phép hoạt động phương tiện giao thông thông minh. Tôi phải điền thông tin gì vào mẫu đơn và cần nộp những tài liệu nào?
- Đáp: Bạn phải điền tên chủ sở hữu, địa chỉ, số định danh cá nhân, quốc tịch, điện thoại, email, biển số xe, màu biển số, nhãn hiệu, số loại, loại xe, dung tích, và các thông tin liên quan. Sau đó nộp mẫu đơn 03a kèm theo mẫu giấy phép 03b.
- ⚠ chep_nguyen_van: “cấp giấy phép hoạt động phương …”

```json
{"qid": "tD-da_buoc-052", "question": "Tôi là chủ sở hữu một xe ô tô chở khách, muốn xin cấp giấy phép hoạt động phương tiện giao thông thông minh. Tôi phải điền thông tin gì vào mẫu đơn và cần nộp những tài liệu nào?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Bạn phải điền tên chủ sở hữu, địa chỉ, số định danh cá nhân, quốc tịch, điện thoại, email, biển số xe, màu biển số, nhãn hiệu, số loại, loại xe, dung tích, và các thông tin liên quan. Sau đó nộp mẫu đơn 03a kèm theo mẫu giấy phép 03b.", "gold_units": ["ND151-2024/D3/K3", "ND151-2024/PL3"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-052:2"}
```

### WD-da_buoc-053 · tier A · vai: tài xế xe tải · kiểu: tinh_huong_ban_than · DAN_CHIEU → LUAT36-2024/D59/K1/b

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Thông tư số 14/2025/TT-BXD (Quy định về đào tạo lái xe; bồi dưỡng, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ)
Hiệu lực của trạng thái này: 2025-09-01 → nay
Mã điều khoản dùng được cho gold_units: TT14-2025-BXD/D19/K1

Điều 19. Tổ chức bồi dưỡng kiến thức pháp luật về giao thông đường bộ cho người điều khiển xe máy chuyên dùng tham gia giao thông đường bộ
1. Báo cáo mở lớp bồi dưỡng kiến thức pháp luật về giao thông đường bộ: cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ tiếp nhận hồ sơ của người tham gia bồi dưỡng đủ điều kiện theo quy định tại điểm b khoản 1, khoản 2 Điều 59 Luật Trật tự, an toàn giao thông đường bộ và thành phần hồ sơ theo quy định tại Điều 20 Thông tư này; lập báo cáo mở lớp bồi dưỡng kiến thức pháp luật về giao thông đường bộ theo mẫu quy định tại Phụ lục XII ban hành kèm theo Thông tư này gửi Sở Xây dựng bằng một trong các hình thức: trực tiếp, dịch vụ bưu chính, trên môi trường điện tử.

### Điều khoản được nguồn trên dẫn chiếu tới (LUAT36-2024/D59/K1/b)
Mã điều khoản dùng được cho gold_units: LUAT36-2024/D59/K1/b

Điều 59. Tuổi, sức khỏe của người điều khiển phương tiện tham gia giao thông đường bộ
1. Độ tuổi của người lái xe, người điều khiển xe máy chuyên dùng được quy định như sau:
b) Người đủ 18 tuổi trở lên được cấp giấy phép lái xe hạng A1, A, B1, B, C1, được cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ để điều khiển xe máy chuyên dùng tham gia giao thông đường bộ;

### Điều khoản được nguồn trên dẫn chiếu tới (LUAT36-2024/D59/K2)
Mã điều khoản dùng được cho gold_units: LUAT36-2024/D59/K2

Điều 59. Tuổi, sức khỏe của người điều khiển phương tiện tham gia giao thông đường bộ
2. Người điều khiển phương tiện tham gia giao thông đường bộ phải bảo đảm điều kiện sức khỏe phù hợp với từng loại phương tiện được phép điều khiển. Bộ trưởng Bộ Y tế quy định về tiêu chuẩn sức khỏe, việc khám sức khỏe đối với người lái xe, người điều khiển xe máy chuyên dùng; việc khám sức khỏe định kỳ đối với người hành nghề lái xe ô tô; xây dựng cơ sở dữ liệu về sức khỏe của người lái xe, người điều khiển xe máy chuyên dùng.

### Điều khoản được nguồn trên dẫn chiếu tới (TT14-2025-BXD/D20)
Mã điều khoản dùng được cho gold_units: TT14-2025-BXD/D20

Điều 20. Hồ sơ của người học
Người tham gia bồi dưỡng kiến thức pháp luật về giao thông đường bộ lập 01 bộ hồ sơ, nộp cho cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ bằng một trong các hình thức: trực tiếp, dịch vụ bưu chính, trên môi trường điện tử. Hồ sơ bao gồm:

### Nguồn 2
Văn bản: Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: LUAT36-2024/D59/K1, LUAT36-2024/D59/K1/a, LUAT36-2024/D59/K1/b, LUAT36-2024/D59/K1/c, LUAT36-2024/D59/K1/d, LUAT36-2024/D59/K1/đ, LUAT36-2024/D59/K1/e

Điều 59. Tuổi, sức khỏe của người điều khiển phương tiện tham gia giao thông đường bộ
1. Độ tuổi của người lái xe, người điều khiển xe máy chuyên dùng được quy định như sau:
a) Người đủ 16 tuổi trở lên được điều khiển xe gắn máy;
b) Người đủ 18 tuổi trở lên được cấp giấy phép lái xe hạng A1, A, B1, B, C1, được cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ để điều khiển xe máy chuyên dùng tham gia giao thông đường bộ;
c) Người đủ 21 tuổi trở lên được cấp giấy phép lái xe hạng C, BE;
d) Người đủ 24 tuổi trở lên được cấp giấy phép lái xe hạng D1, D2, C1E, CE;
đ) Người đủ 27 tuổi trở lên được cấp giấy phép lái xe hạng D, D1E, D2E, DE;
e) Tuổi tối đa của người lái xe ô tô chở người (kể cả xe buýt) trên 29 chỗ (không kể chỗ của người lái xe), xe ô tô chở người giường nằm là đủ 57 tuổi đối với nam, đủ 55 tuổi đối với nữ.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là tài xế xe tải, tôi đã đủ 18 tuổi, có thể đăng ký tham gia lớp bồi dưỡng kiến thức pháp luật về giao thông đường bộ được không?
- Đáp: Bạn có thể đăng ký tham gia lớp bồi dưỡng. Để làm điều này, bạn cần nộp hồ sơ theo mẫu quy định trong Thông tư số 14/2025/TT‑BXD, gồm các giấy tờ cá nhân và chứng minh đủ 18 tuổi. Sau khi hồ sơ được chấp nhận, cơ sở bồi dưỡng sẽ mở lớp và bạn sẽ nhận được chứng chỉ bồi dưỡng.
- ⚠ chep_nguyen_van: “bồi dưỡng kiến thức pháp luật …”
- Ghi chú: Giả định rằng tài xế xe tải đủ 18 tuổi và muốn tham gia bồi dưỡng

```json
{"qid": "tD-da_buoc-053", "question": "Tôi là tài xế xe tải, tôi đã đủ 18 tuổi, có thể đăng ký tham gia lớp bồi dưỡng kiến thức pháp luật về giao thông đường bộ được không?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Bạn có thể đăng ký tham gia lớp bồi dưỡng. Để làm điều này, bạn cần nộp hồ sơ theo mẫu quy định trong Thông tư số 14/2025/TT‑BXD, gồm các giấy tờ cá nhân và chứng minh đủ 18 tuổi. Sau khi hồ sơ được chấp nhận, cơ sở bồi dưỡng sẽ mở lớp và bạn sẽ nhận được chứng chỉ bồi dưỡng.", "gold_units": ["TT14-2025-BXD/D19/K1", "LUAT36-2024/D59/K1/b", "TT14-2025-BXD/D20"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-053:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là tài xế xe tải, tôi muốn tham gia lớp bồi dưỡng kiến thức pháp luật, tôi có cần khám sức khỏe định kỳ trước khi đăng ký không?
- Đáp: Bạn phải đảm bảo điều kiện sức khỏe phù hợp với loại phương tiện mà bạn điều khiển. Theo quy định, người điều khiển xe tải cần được khám sức khỏe định kỳ và có hồ sơ sức khỏe hợp lệ trước khi đăng ký bồi dưỡng. Sau khi có hồ sơ sức khỏe, bạn mới nộp hồ sơ tham gia lớp bồi dưỡng theo Thông tư số 14/2025/TT‑BXD.
- ⚠ chep_nguyen_van: “bồi dưỡng kiến thức pháp luật …”
- Ghi chú: Giả định rằng tài xế xe tải cần khám sức khỏe định kỳ

```json
{"qid": "tD-da_buoc-053", "question": "Tôi là tài xế xe tải, tôi muốn tham gia lớp bồi dưỡng kiến thức pháp luật, tôi có cần khám sức khỏe định kỳ trước khi đăng ký không?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Bạn phải đảm bảo điều kiện sức khỏe phù hợp với loại phương tiện mà bạn điều khiển. Theo quy định, người điều khiển xe tải cần được khám sức khỏe định kỳ và có hồ sơ sức khỏe hợp lệ trước khi đăng ký bồi dưỡng. Sau khi có hồ sơ sức khỏe, bạn mới nộp hồ sơ tham gia lớp bồi dưỡng theo Thông tư số 14/2025/TT‑BXD.", "gold_units": ["LUAT36-2024/D59/K2", "TT14-2025-BXD/D19/K1", "TT14-2025-BXD/D20"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-053:2"}
```

### WD-da_buoc-054 · tier A · vai: người mới học lái ô tô · kiểu: tinh_huong_ban_than · DAN_CHIEU → TT14-2025-BXD/D23/K3/a

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Thông tư số 14/2025/TT-BXD (Quy định về đào tạo lái xe; bồi dưỡng, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ)
Hiệu lực của trạng thái này: 2025-09-01 → nay
Mã điều khoản dùng được cho gold_units: TT14-2025-BXD/D29/K2, TT14-2025-BXD/D29/K2/a, TT14-2025-BXD/D29/K2/b, TT14-2025-BXD/D29/K2/c, TT14-2025-BXD/D29/K2/d

Điều 29. Sở Xây dựng
2. Đối với công tác bồi dưỡng, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ:
a) Cấp lại chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ theo quy định tại điểm a khoản 3 Điều 23 Thông tư này;
b) Thực hiện tiếp nhận, rà soát, kiểm tra và thông báo danh sách cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ hoạt động trên địa bàn quản lý trên trang thông tin điện tử của Sở Xây dựng;
c) Truy cập Hệ thống thông tin chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ tại Sở Xây dựng để quản lý, khai thác dữ liệu chứng chỉ bồi dưỡng pháp luật về giao thông đường bộ của các cơ sở bồi dưỡng thuộc quyền quản lý;
d) Lập Sổ quản lý cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ theo mẫu quy định tại Phụ lục XXIV ban hành kèm theo Thông tư này.

### Điều khoản được nguồn trên dẫn chiếu tới (TT14-2025-BXD/D23/K3/a)
Mã điều khoản dùng được cho gold_units: TT14-2025-BXD/D23/K3/a

Điều 23. Cấp lại chứng chỉ
3. Trình tự thực hiện:
a) Cá nhân nộp 01 bộ hồ sơ đến cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ đã cấp chứng chỉ; trường hợp cơ sở bồi dưỡng đã cấp chứng chỉ không còn hoạt động thì cá nhân nộp cho Sở Xây dựng nơi quản lý cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ đã cấp chứng chỉ tại Trung tâm Phục vụ hành chính công cấp tỉnh hoặc cấp xã bằng hình thức trực tiếp hoặc qua dịch vụ bưu chính hoặc qua cổng dịch vụ công quốc gia.

### Nguồn 2
Văn bản: Thông tư số 14/2025/TT-BXD (Quy định về đào tạo lái xe; bồi dưỡng, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ)
Hiệu lực của trạng thái này: 2026-07-01 → nay
Mã điều khoản dùng được cho gold_units: TT14-2025-BXD/D23/K3, TT14-2025-BXD/D23/K3/a, TT14-2025-BXD/D23/K3/b, TT14-2025-BXD/D23/K3/c, TT14-2025-BXD/D23/K3/d

Điều 23. Cấp lại chứng chỉ
3. Trình tự thực hiện:
a) Cá nhân nộp 01 bộ hồ sơ đến cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ đã cấp chứng chỉ; trường hợp cơ sở bồi dưỡng đã cấp chứng chỉ không còn hoạt động thì cá nhân nộp cho Sở Xây dựng nơi quản lý cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ đã cấp chứng chỉ tại Trung tâm Phục vụ hành chính công cấp tỉnh hoặc cấp xã bằng hình thức trực tiếp hoặc qua dịch vụ bưu chính hoặc qua cổng dịch vụ công quốc gia.
b) Cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ hoặc Sở Xây dựng kiểm tra hồ sơ khi tiếp nhận; trường hợp chứng chỉ không thuộc đối tượng được cấp lại hoặc hồ sơ không đúng theo quy định, phải thông báo trực tiếp hoặc bằng văn bản những nội dung cần bổ sung hoặc sửa đổi cho cá nhân trong thời hạn 02 ngày làm việc, kể từ ngày nhận hồ sơ;
c) Trong thời hạn 02 ngày làm việc, kể từ ngày nhận đủ hồ sơ hợp lệ, người đứng đầu cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ hoặc Sở Xây dựng cấp lại chứng chỉ; trường hợp không cấp lại chứng chỉ thì phải trả lời bằng văn bản và nêu rõ lý do;
d) Việc trả chứng chỉ bản giấy được thực hiện tại cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ; trường hợp trả bản điện tử thì đăng tải trên Hệ thống thông tin chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ tại cơ sở bồi dưỡng kiến thức pháp luật về giao thông đường bộ.
…

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi muốn làm mới chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ, tôi phải nộp hồ sơ ở đâu và sau khi nộp hồ sơ sẽ được làm gì?
- Đáp: Bạn cần nộp một bộ hồ sơ tại cơ sở bồi dưỡng đã cấp chứng chỉ trước đây; nếu cơ sở đã ngừng hoạt động, nộp cho Sở Xây dựng nơi quản lý cơ sở đó tại trung tâm phục vụ hành chính công cấp tỉnh hoặc cấp xã bằng trực tiếp, bưu chính hoặc cổng dịch vụ công quốc gia. Sau khi nhận hồ sơ, cơ sở bồi dưỡng hoặc Sở Xây dựng sẽ kiểm tra hồ sơ; nếu hồ sơ hợp lệ, trong vòng 2 ngày làm việc, người đứng đầu cơ sở hoặc Sở Xây dựng sẽ cấp lại chứng chỉ. Nếu hồ sơ không hợp lệ hoặc chứng chỉ không thuộc đối tượng cấp lại, họ sẽ thông báo nội dung cần bổ sung hoặc sửa đổi trong thời hạn 2 ngày làm việc và sau đó trả lời bằng văn bản nêu rõ lý do.
- ⚠ chep_nguyen_van: “bồi dưỡng kiến thức pháp luật …”
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-da_buoc-054", "question": "Tôi muốn làm mới chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ, tôi phải nộp hồ sơ ở đâu và sau khi nộp hồ sơ sẽ được làm gì?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Bạn cần nộp một bộ hồ sơ tại cơ sở bồi dưỡng đã cấp chứng chỉ trước đây; nếu cơ sở đã ngừng hoạt động, nộp cho Sở Xây dựng nơi quản lý cơ sở đó tại trung tâm phục vụ hành chính công cấp tỉnh hoặc cấp xã bằng trực tiếp, bưu chính hoặc cổng dịch vụ công quốc gia. Sau khi nhận hồ sơ, cơ sở bồi dưỡng hoặc Sở Xây dựng sẽ kiểm tra hồ sơ; nếu hồ sơ hợp lệ, trong vòng 2 ngày làm việc, người đứng đầu cơ sở hoặc Sở Xây dựng sẽ cấp lại chứng chỉ. Nếu hồ sơ không hợp lệ hoặc chứng chỉ không thuộc đối tượng cấp lại, họ sẽ thông báo nội dung cần bổ sung hoặc sửa đổi trong thời hạn 2 ngày làm việc và sau đó trả lời bằng văn bản nêu rõ lý do.", "gold_units": ["TT14-2025-BXD/D23/K3/a", "TT14-2025-BXD/D23/K3/b"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-054:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Nếu cơ sở bồi dưỡng đã cấp chứng chỉ của tôi đã đóng cửa, tôi phải làm gì để nộp hồ sơ làm mới và làm sao để biết được khi nào chứng chỉ sẽ được cấp lại?
- Đáp: Bạn phải nộp một bộ hồ sơ tại Sở Xây dựng nơi quản lý cơ sở bồi dưỡng đã cấp chứng chỉ, tại trung tâm phục vụ hành chính công cấp tỉnh hoặc cấp xã, bằng trực tiếp, bưu chính hoặc qua cổng dịch vụ công quốc gia. Sau khi nhận hồ sơ, cơ sở bồi dưỡng hoặc Sở Xây dựng sẽ kiểm tra; nếu hồ sơ hợp lệ, trong vòng 2 ngày làm việc, họ sẽ cấp lại chứng chỉ. Nếu không, họ sẽ thông báo nội dung cần bổ sung hoặc sửa đổi trong thời hạn 2 ngày làm việc và sau đó trả lời bằng văn bản nêu rõ lý do.
- ⚠ chep_nguyen_van: “bồi dưỡng đã cấp chứng chỉ …”
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-da_buoc-054", "question": "Nếu cơ sở bồi dưỡng đã cấp chứng chỉ của tôi đã đóng cửa, tôi phải làm gì để nộp hồ sơ làm mới và làm sao để biết được khi nào chứng chỉ sẽ được cấp lại?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "A", "answer": "Bạn phải nộp một bộ hồ sơ tại Sở Xây dựng nơi quản lý cơ sở bồi dưỡng đã cấp chứng chỉ, tại trung tâm phục vụ hành chính công cấp tỉnh hoặc cấp xã, bằng trực tiếp, bưu chính hoặc qua cổng dịch vụ công quốc gia. Sau khi nhận hồ sơ, cơ sở bồi dưỡng hoặc Sở Xây dựng sẽ kiểm tra; nếu hồ sơ hợp lệ, trong vòng 2 ngày làm việc, họ sẽ cấp lại chứng chỉ. Nếu không, họ sẽ thông báo nội dung cần bổ sung hoặc sửa đổi trong thời hạn 2 ngày làm việc và sau đó trả lời bằng văn bản nêu rõ lý do.", "gold_units": ["TT14-2025-BXD/D23/K3/a", "TT14-2025-BXD/D23/K3/b"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-054:2"}
```

### WD-da_buoc-057 · tier B · vai: người lớn tuổi đi xe đạp điện · kiểu: tinh_huong_ban_than · DAN_CHIEU → LUAT35-2024/D11/K3

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND165-2024/D69/K4

Điều 69. Quy định chuyển tiếp
4. Việc đổi tên, số hiệu đường bộ không phù hợp với quy định của Nghị định này hoàn thành trước ngày 01 tháng 01 năm 2026, trừ trường hợp quy định tại khoản 3 Điều 11 Luật Đường bộ.

### Điều khoản được nguồn trên dẫn chiếu tới (LUAT35-2024/D11/K3)
Mã điều khoản dùng được cho gold_units: LUAT35-2024/D11/K3

Điều 11. Đặt tên, đổi tên, số hiệu đường bộ
3. Không bắt buộc đặt tên, số hiệu đường bộ đối với đường xã, đường thôn, đường nội bộ, đường chuyên dùng; không bắt buộc đổi tên, số hiệu đường bộ trong trường hợp đường đó đi qua địa bàn được cấp có thẩm quyền quyết định giải thể, nhập, chia, điều chỉnh địa giới hành chính của địa phương.

### Nguồn 2
Văn bản: Luật Đường bộ số 35/2024/QH15
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: LUAT35-2024/D11/K3

Điều 11. Đặt tên, đổi tên, số hiệu đường bộ
3. Không bắt buộc đặt tên, số hiệu đường bộ đối với đường xã, đường thôn, đường nội bộ, đường chuyên dùng; không bắt buộc đổi tên, số hiệu đường bộ trong trường hợp đường đó đi qua địa bàn được cấp có thẩm quyền quyết định giải thể, nhập, chia, điều chỉnh địa giới hành chính của địa phương.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi đang đi xe đạp điện trên đường xã, đường thôn, có tên không? Nếu không, tôi có cần đổi tên đường không?
- Đáp: Bạn không bắt buộc đặt tên, số hiệu đường bộ đối với đường xã, đường thôn, đường nội bộ, đường chuyên dùng. Do đó, bạn không cần phải đổi tên đường. (Điều 11 Khoản 3 Luật Đường bộ số 35/2024/QH15)
- ⚠ da_buoc_it_hon_2_gold

```json
{"qid": "tD-da_buoc-057", "question": "Tôi đang đi xe đạp điện trên đường xã, đường thôn, có tên không? Nếu không, tôi có cần đổi tên đường không?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "B", "answer": "Bạn không bắt buộc đặt tên, số hiệu đường bộ đối với đường xã, đường thôn, đường nội bộ, đường chuyên dùng. Do đó, bạn không cần phải đổi tên đường. (Điều 11 Khoản 3 Luật Đường bộ số 35/2024/QH15)", "gold_units": ["LUAT35-2024/D11/K3"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-057:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi muốn đổi tên đường bộ mà qua địa bàn cấp có thẩm quyền quyết định giải thể, nhập, chia, điều chỉnh địa giới hành chính, có phải thực hiện theo Nghị định 165/2024/NĐ-CP không?
- Đáp: Bạn không bắt buộc đổi tên, số hiệu đường bộ trong trường hợp đường đó đi qua địa bàn được cấp có thẩm quyền quyết định giải thể, nhập, chia, điều chỉnh địa giới hành chính của địa phương. Do đó, việc đổi tên đường không cần thực hiện theo Nghị định 165/2024/NĐ-CP. (Điều 11 Khoản 3 Luật Đường bộ số 35/2024/QH15)
- ⚠ da_buoc_it_hon_2_gold; chep_nguyen_van: “chia điều chỉnh địa giới hành …”

```json
{"qid": "tD-da_buoc-057", "question": "Tôi muốn đổi tên đường bộ mà qua địa bàn cấp có thẩm quyền quyết định giải thể, nhập, chia, điều chỉnh địa giới hành chính, có phải thực hiện theo Nghị định 165/2024/NĐ-CP không?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "B", "answer": "Bạn không bắt buộc đổi tên, số hiệu đường bộ trong trường hợp đường đó đi qua địa bàn được cấp có thẩm quyền quyết định giải thể, nhập, chia, điều chỉnh địa giới hành chính của địa phương. Do đó, việc đổi tên đường không cần thực hiện theo Nghị định 165/2024/NĐ-CP. (Điều 11 Khoản 3 Luật Đường bộ số 35/2024/QH15)", "gold_units": ["LUAT35-2024/D11/K3"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-057:2"}
```

### WD-da_buoc-059 · tier B · vai: tài xế công nghệ · kiểu: neu_van_ban · DAN_CHIEU → ND165-2024/D48

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ)
Hiệu lực của trạng thái này: 2026-07-01 → nay
Mã điều khoản dùng được cho gold_units: ND165-2024/D47/K4

Điều 47. Mở rộng, nâng cấp đường cao tốc hoặc đường bộ đang khai thác nâng cấp thành đường cao tốc trong trường hợp nhà đầu tư hiện hữu đề xuất điều chỉnh dự án
4. Trường hợp thỏa thuận mở rộng, nâng cấp theo phương án điều chỉnh dự án theo khoản 1 Điều này không thành công, cơ quan ký kết hợp đồng thỏa thuận với nhà đầu tư về việc Nhà nước lập dự án mở rộng, nâng cấp đường cao tốc theo hình thức đầu tư công theo quy định tại Điều 48 của Nghị định này.

### Điều khoản được nguồn trên dẫn chiếu tới (ND165-2024/D47/K1)
Mã điều khoản dùng được cho gold_units: ND165-2024/D47/K1

Điều 47. Mở rộng, nâng cấp đường cao tốc hoặc đường bộ đang khai thác nâng cấp thành đường cao tốc trong trường hợp nhà đầu tư hiện hữu đề xuất điều chỉnh dự án
1. Trường hợp thỏa thuận mở rộng, nâng cấp theo phương án nhà đầu tư hiện hữu đề xuất điều chỉnh dự án, nhà đầu tư hiện hữu tổ chức lập hồ sơ điều chỉnh dự án trình cấp có thẩm quyền xem xét. Việc điều chỉnh chủ trương đầu tư, điều chỉnh dự án, phê duyệt thiết kế xây dựng sau thiết kế cơ sở, dự toán, chi phí của nhà đầu tư đề xuất thực hiện theo pháp luật về đầu tư theo phương thức đối tác công tư, pháp luật về xây dựng và pháp luật khác có liên quan.

### Điều khoản được nguồn trên dẫn chiếu tới (ND165-2024/D48)
Mã điều khoản dùng được cho gold_units: ND165-2024/D48

Điều 48. Mở rộng, nâng cấp đường cao tốc trong trường hợp lập dự án đầu tư mở rộng, nâng cấp theo hình thức đầu tư công
Cơ quan ký kết hợp đồng thỏa thuận với nhà đầu tư hiện hữu về việc mở rộng, nâng cấp đường cao tốc theo hình thức đầu tư công theo quy định tại điểm b khoản 2 Điều 48 Luật Đường bộ được thực hiện như sau:

### Nguồn 2
Văn bản: Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND165-2024/D48/K1, ND165-2024/D48/K1/a, ND165-2024/D48/K1/b, ND165-2024/D48/K1/c

Điều 48. Mở rộng, nâng cấp đường cao tốc trong trường hợp lập dự án đầu tư mở rộng, nâng cấp theo hình thức đầu tư công
1. Cơ quan ký kết hợp đồng thỏa thuận với nhà đầu tư hiện hữu sơ bộ các nội dung sau:
a) Nhà đầu tư hiện hữu cam kết phối hợp với các cơ quan, đơn vị có liên quan trong giai đoạn chuẩn bị đầu tư và thực hiện dự án mở rộng, nâng cấp theo hình thức đầu tư công;
b) Phương án để bảo đảm tính đồng bộ về kết cấu hạ tầng trong đầu tư xây dựng công trình; phương án tiếp nhận phần mở rộng, cải tạo, nâng cấp và quản lý, vận hành, bảo trì đồng bộ với dự án PPP sau khi được cơ quan có thẩm quyền bàn giao;
c) Các nội dung cần sửa đổi hợp đồng dự án do ảnh hưởng của việc thực hiện dự án mở rộng, nâng cấp theo hình thức đầu tư công và nhà đầu tư hiện hữu tiếp nhận công trình đã đầu tư mở rộng, nâng cấp để quản lý, vận hành, bảo trì, khai thác.

### Nguồn 3
Văn bản: Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND165-2024/D48/K2, ND165-2024/D48/K2/a, ND165-2024/D48/K2/b

Điều 48. Mở rộng, nâng cấp đường cao tốc trong trường hợp lập dự án đầu tư mở rộng, nâng cấp theo hình thức đầu tư công
2. Chủ đầu tư lập báo cáo nghiên cứu tiền khả thi, báo cáo nghiên cứu khả thi dự án mở rộng, nâng cấp theo quy định pháp luật đầu tư công, pháp luật xây dựng và các nội dung sau:
a) Yêu cầu về kỹ thuật để bảo đảm tính đồng bộ của dự án mở rộng, nâng cấp với dự án đường hiện hữu;
b) Nội dung khác liên quan đến việc thực hiện dự án mở rộng, nâng cấp theo hình thức đầu tư công theo kết quả đàm phán tại khoản 1 Điều này.

### Điều khoản được nguồn trên dẫn chiếu tới (ND165-2024/D48/K1)
Mã điều khoản dùng được cho gold_units: ND165-2024/D48/K1

Điều 48. Mở rộng, nâng cấp đường cao tốc trong trường hợp lập dự án đầu tư mở rộng, nâng cấp theo hình thức đầu tư công
1. Cơ quan ký kết hợp đồng thỏa thuận với nhà đầu tư hiện hữu sơ bộ các nội dung sau:

### Nguồn 4
Văn bản: Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND165-2024/D48/K3

Điều 48. Mở rộng, nâng cấp đường cao tốc trong trường hợp lập dự án đầu tư mở rộng, nâng cấp theo hình thức đầu tư công
3. Việc lập, thẩm định báo cáo nghiên cứu tiền khả thi, quyết định chủ trương đầu tư; lập, thẩm định báo cáo nghiên cứu khả thi, quyết định đầu tư; lựa chọn nhà thầu; triển khai thực hiện hợp đồng dự án thực hiện theo quy định pháp luật đầu tư công, pháp luật đấu thầu, pháp luật xây dựng.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là một công ty xây dựng, muốn mở rộng đường cao tốc hiện có. Nếu thỏa thuận với nhà đầu tư hiện hữu không thành công, tôi có thể làm gì để tiếp tục dự án?
- Đáp: Bạn có thể ký kết hợp đồng thỏa thuận với nhà đầu tư hiện hữu về việc Nhà nước lập dự án mở rộng, nâng cấp đường cao tốc theo hình thức đầu tư công. Điều này được quy định trong Điều 47, khoản 4 của Nghị định 165/2024/NĐ-CP, và được thực hiện theo quy định tại Điều 48 của cùng nghị định.
- ⚠ chi_so_so_sai (0); chep_nguyen_van: “thuận với nhà đầu tư hiện …”
- Ghi chú: Giả định công ty đang tham gia dự án mở rộng đường cao tốc hiện có.

```json
{"qid": "tD-da_buoc-059", "question": "Tôi là một công ty xây dựng, muốn mở rộng đường cao tốc hiện có. Nếu thỏa thuận với nhà đầu tư hiện hữu không thành công, tôi có thể làm gì để tiếp tục dự án?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "B", "answer": "Bạn có thể ký kết hợp đồng thỏa thuận với nhà đầu tư hiện hữu về việc Nhà nước lập dự án mở rộng, nâng cấp đường cao tốc theo hình thức đầu tư công. Điều này được quy định trong Điều 47, khoản 4 của Nghị định 165/2024/NĐ-CP, và được thực hiện theo quy định tại Điều 48 của cùng nghị định.", "gold_units": ["ND165-2024/D47/K4", "ND165-2024/D48/K1"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-059:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Cơ quan ký kết hợp đồng với nhà đầu tư hiện hữu, tôi cần chuẩn bị những nội dung nào trong giai đoạn đầu?
- Đáp: Bạn cần chuẩn bị: a) Cam kết phối hợp với các cơ quan, đơn vị liên quan trong giai đoạn chuẩn bị đầu tư và thực hiện dự án; b) Phương án bảo đảm tính đồng bộ về kết cấu hạ tầng; c) Các nội dung cần sửa đổi hợp đồng dự án do ảnh hưởng của việc thực hiện dự án mở rộng, nâng cấp theo hình thức đầu tư công và nhà đầu tư tiếp nhận công trình đã đầu tư mở rộng, nâng cấp để quản lý, vận hành, bảo trì, khai thác. Điều này được quy định tại Điều 48, khoản 1 của Nghị định 165/2024/NĐ-CP.
- ⚠ chi_so_so_sai (0); chep_nguyen_van: “cơ quan ký kết hợp đồng …”
- Ghi chú: Giả định cơ quan đang ký hợp đồng với nhà đầu tư hiện hữu.

```json
{"qid": "tD-da_buoc-059", "question": "Cơ quan ký kết hợp đồng với nhà đầu tư hiện hữu, tôi cần chuẩn bị những nội dung nào trong giai đoạn đầu?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "B", "answer": "Bạn cần chuẩn bị: a) Cam kết phối hợp với các cơ quan, đơn vị liên quan trong giai đoạn chuẩn bị đầu tư và thực hiện dự án; b) Phương án bảo đảm tính đồng bộ về kết cấu hạ tầng; c) Các nội dung cần sửa đổi hợp đồng dự án do ảnh hưởng của việc thực hiện dự án mở rộng, nâng cấp theo hình thức đầu tư công và nhà đầu tư tiếp nhận công trình đã đầu tư mở rộng, nâng cấp để quản lý, vận hành, bảo trì, khai thác. Điều này được quy định tại Điều 48, khoản 1 của Nghị định 165/2024/NĐ-CP.", "gold_units": ["ND165-2024/D48/K1", "ND165-2024/D48/K2"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-059:2"}
```

### WD-da_buoc-063 · tier B · vai: người lớn tuổi đi xe đạp điện · kiểu: tinh_huong_ban_than · DAN_CHIEU → LUAT35-2024/D25/K2

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND165-2024/D23/K2

Điều 23. Nội dung tổ chức giao thông đường bộ trong giai đoạn lập dự án đầu tư xây dựng, thiết kế công trình đường bộ, trước khi đưa đường bộ đã hoàn thành đầu tư vào khai thác
2. Tổ chức giao thông trong giai đoạn thiết kế công trình đường bộ, bao gồm các nội dung quy định tại khoản 2 Điều 25 Luật Đường bộ và thiết kế chi tiết các loại báo hiệu đường bộ đối với từng đoạn đường, từng nút giao và phải bảo đảm: phù hợp với quy mô, các chỉ tiêu kỹ thuật công trình, từng bộ phận, hạng mục công trình đang đầu tư xây dựng; phù hợp với Quy chuẩn kỹ thuật quốc gia về báo hiệu đường bộ; thiết kế chi tiết các công trình phụ trợ gắn liền với đường bộ, công trình an toàn giao thông, hệ thống quản lý giao thông thông minh, trung tâm quản lý, điều hành giao thông tuyến đường cao tốc, xác định danh mục, quy mô, công suất, tính năng các phương tiện, thiết bị phục vụ quản lý, vận hành, khai thác đường bộ.

### Điều khoản được nguồn trên dẫn chiếu tới (LUAT35-2024/D25/K2)
Mã điều khoản dùng được cho gold_units: LUAT35-2024/D25/K2

Điều 25. Tổ chức giao thông
2. Nội dung tổ chức giao thông đường bộ trong giai đoạn thiết kế, thi công xây dựng, quản lý, vận hành, khai thác, sử dụng, bảo trì công trình đường bộ bao gồm:

### Nguồn 2
Văn bản: Luật Đường bộ số 35/2024/QH15
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: LUAT35-2024/D25/K2, LUAT35-2024/D25/K2/a, LUAT35-2024/D25/K2/b, LUAT35-2024/D25/K2/c, LUAT35-2024/D25/K2/d, LUAT35-2024/D25/K2/đ, LUAT35-2024/D25/K2/e, LUAT35-2024/D25/K2/g, LUAT35-2024/D25/K2/h, LUAT35-2024/D25/K2/i, LUAT35-2024/D25/K2/k

Điều 25. Tổ chức giao thông
2. Nội dung tổ chức giao thông đường bộ trong giai đoạn thiết kế, thi công xây dựng, quản lý, vận hành, khai thác, sử dụng, bảo trì công trình đường bộ bao gồm:
a) Quy định số làn đường, phần đường dành cho xe ô tô và các phương tiện tham gia giao thông đường bộ khác, phần đường dành cho người đi bộ; chiều đi, tốc độ các phương tiện cơ giới tham gia giao thông đường bộ;
b) Tổ chức phân làn, phân luồng trên tuyến đường đang đầu tư xây dựng và tại các tuyến đường bộ kết nối;
c) Quy định giao thông tại các nút giao, vị trí đấu nối với đường khác; quy định về tránh, vượt xe trên đường, các điểm được phép dừng xe, đỗ xe trên đường, vị trí đón, trả khách;
d) Quy định khổ giới hạn và tải trọng cho phép phương tiện tham gia giao thông đường bộ an toàn;
đ) Quy định thời gian cho phép tham gia giao thông; thời gian cho phép đi theo các hướng của đèn tín hiệu giao thông;
e) Quy định thời gian bật, tắt hệ thống chiếu sáng trên đường;
g) Quy định về các trường hợp tạm dừng khai thác một phần hoặc toàn bộ tuyến đường;
h) Khai thác, sử dụng hệ thống quản lý giao thông thông minh, trung tâm quản lý, điều hành giao thông tuyến đường cao tốc và các thiết bị công nghệ khác phục vụ cung cấp thông tin, chỉ dẫn cho người tham gia giao thông đường bộ;
i) Lắp đặt đầy đủ hệ thống báo hiệu đường bộ và thực hiện các công việc cần thiết khác;
k) Phê duyệt phương án tổ chức giao thông đối với đường cao tốc.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là người lớn tuổi, đang đi xe đạp điện trên đoạn đường đang trong giai đoạn thiết kế, tôi có thể dừng xe ở đâu và cần tuân thủ quy định gì?
- Đáp: Bạn chỉ được dừng xe tại những vị trí được quy định trong quy hoạch giao thông, chẳng hạn như các điểm dừng xe, đỗ xe được chỉ định. Ngoài ra, bạn phải tuân thủ các quy định về phân làn, phân luồng, tốc độ và thời gian tham gia giao thông được quy định trong quy hoạch. (Điều 25 Khoản a và Khoản c Luật Đường bộ số 35/2024/QH15; Điều 23 Khoản 2 Nghị định số 165/2024/NĐ-CP)
- Ghi chú: Giả định xe đạp điện được tính là phương tiện tham gia giao thông đường bộ

```json
{"qid": "tD-da_buoc-063", "question": "Tôi là người lớn tuổi, đang đi xe đạp điện trên đoạn đường đang trong giai đoạn thiết kế, tôi có thể dừng xe ở đâu và cần tuân thủ quy định gì?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "B", "answer": "Bạn chỉ được dừng xe tại những vị trí được quy định trong quy hoạch giao thông, chẳng hạn như các điểm dừng xe, đỗ xe được chỉ định. Ngoài ra, bạn phải tuân thủ các quy định về phân làn, phân luồng, tốc độ và thời gian tham gia giao thông được quy định trong quy hoạch. (Điều 25 Khoản a và Khoản c Luật Đường bộ số 35/2024/QH15; Điều 23 Khoản 2 Nghị định số 165/2024/NĐ-CP)", "gold_units": ["ND165-2024/D23/K2", "LUAT35-2024/D25/K2"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-063:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là người lớn tuổi, đang đi xe đạp điện trên đường đang xây dựng, tôi cần biết cách phân làn và giới hạn tốc độ cho xe của mình?
- Đáp: Bạn phải tuân thủ quy định về số làn đường, phần đường dành cho xe ô tô và các phương tiện khác, cũng như phần đường dành cho người đi bộ, được quy định trong quy hoạch. Đối với xe đạp điện, bạn phải đi theo hướng được quy định và tuân thủ giới hạn tốc độ được quy định trong quy hoạch. (Điều 25 Khoản a và Khoản b Luật Đường bộ số 35/2024/QH15; Điều 23 Khoản 2 Nghị định số 165/2024/NĐ-CP)
- Ghi chú: Giả định xe đạp điện được tính là phương tiện tham gia giao thông đường bộ

```json
{"qid": "tD-da_buoc-063", "question": "Tôi là người lớn tuổi, đang đi xe đạp điện trên đường đang xây dựng, tôi cần biết cách phân làn và giới hạn tốc độ cho xe của mình?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "B", "answer": "Bạn phải tuân thủ quy định về số làn đường, phần đường dành cho xe ô tô và các phương tiện khác, cũng như phần đường dành cho người đi bộ, được quy định trong quy hoạch. Đối với xe đạp điện, bạn phải đi theo hướng được quy định và tuân thủ giới hạn tốc độ được quy định trong quy hoạch. (Điều 25 Khoản a và Khoản b Luật Đường bộ số 35/2024/QH15; Điều 23 Khoản 2 Nghị định số 165/2024/NĐ-CP)", "gold_units": ["ND165-2024/D23/K2", "LUAT35-2024/D25/K2"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-063:2"}
```

### WD-da_buoc-064 · tier B · vai: người mới học lái ô tô · kiểu: tinh_huong_nguoi_khac · DAN_CHIEU → LUAT35-2024/D30/K4

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND165-2024/D55/K2

Điều 55. Lộ trình đầu tư xây dựng đối với đường cao tốc chưa đáp ứng tiêu chuẩn, quy chuẩn kỹ thuật theo khoản 1 Điều 45 Luật Đường bộ, đường gom, đường bên, Trung tâm quản lý, điều hành giao thông tuyến đường cao tốc, công trình kiểm soát tải trọng xe, hệ thống thu phí điện tử không dừng
2. Đối với đường gom, đường bên: cơ quan, đơn vị tại khoản 4 Điều 30 Luật Đường bộ tổ chức xây dựng đường gom, đường bên kết nối với đường chính căn cứ nhu cầu, thời điểm kết nối với đường chính theo quy định pháp luật.

### Điều khoản được nguồn trên dẫn chiếu tới (LUAT35-2024/D30/K4)
Mã điều khoản dùng được cho gold_units: LUAT35-2024/D30/K4

Điều 30. Kết nối giao thông đường bộ
4. Trách nhiệm xây dựng đường nhánh, đường gom, đường bên kết nối với đường chính trong từng địa bàn, khu vực được quy định như sau:

### Nguồn 2
Văn bản: Luật Đường bộ số 35/2024/QH15
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: LUAT35-2024/D30/K4, LUAT35-2024/D30/K4/a, LUAT35-2024/D30/K4/b

Điều 30. Kết nối giao thông đường bộ
4. Trách nhiệm xây dựng đường nhánh, đường gom, đường bên kết nối với đường chính trong từng địa bàn, khu vực được quy định như sau:
a) Chủ đầu tư, xây dựng các khu đô thị, khu dân cư, khu thương mại dịch vụ, khu hành chính, nơi làm việc của cơ quan, tổ chức, khu kinh tế, khu công nghiệp, cơ sở sản xuất, kinh doanh, cảng hàng không, bến xe, ga đường sắt, cảng thủy nội địa, bến thủy nội địa, cảng biển, cảng cạn và các đầu mối giao thông khác có trách nhiệm xây dựng đường bộ để kết nối giao thông từ các khu vực, cơ sở này với đường đi qua khu vực, cơ sở;
b) Bộ Giao thông vận tải, Ủy ban nhân dân các cấp đầu tư, xây dựng, nâng cấp, mở rộng, cải tạo đường bộ thuộc phạm vi quản lý kết nối giao thông thuận lợi đến các cảng hàng không, cảng biển, cảng thủy nội địa, bến thủy nội địa, ga đường sắt.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Anh tôi đang xây dựng một khu đô thị mới, muốn kết nối với đường cao tốc, anh có cần đầu tư vào lộ trình xây dựng đường cao tốc chưa đáp ứng tiêu chuẩn hay chỉ cần xây dựng đường gom, đường bên?
- Đáp: Bạn cần đầu tư vào lộ trình đầu tư xây dựng đường cao tốc chưa đáp ứng tiêu chuẩn, đồng thời xây dựng đường gom, đường bên để kết nối với đường chính. Điều 55 Nghị định 165/2024/NĐ-CP quy định về lộ trình đầu tư xây dựng đường cao tốc chưa đáp ứng tiêu chuẩn, và Điều 30 Luật Đường bộ quy định trách nhiệm xây dựng đường gom, đường bên. (Điều 55 Nghị định 165/2024/NĐ-CP; Điều 30 Luật Đường bộ)
- ⚠ chep_nguyen_van: “cao tốc chưa đáp ứng tiêu …”
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-da_buoc-064", "question": "Anh tôi đang xây dựng một khu đô thị mới, muốn kết nối với đường cao tốc, anh có cần đầu tư vào lộ trình xây dựng đường cao tốc chưa đáp ứng tiêu chuẩn hay chỉ cần xây dựng đường gom, đường bên?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "B", "answer": "Bạn cần đầu tư vào lộ trình đầu tư xây dựng đường cao tốc chưa đáp ứng tiêu chuẩn, đồng thời xây dựng đường gom, đường bên để kết nối với đường chính. Điều 55 Nghị định 165/2024/NĐ-CP quy định về lộ trình đầu tư xây dựng đường cao tốc chưa đáp ứng tiêu chuẩn, và Điều 30 Luật Đường bộ quy định trách nhiệm xây dựng đường gom, đường bên. (Điều 55 Nghị định 165/2024/NĐ-CP; Điều 30 Luật Đường bộ)", "gold_units": ["ND165-2024/D55/K2", "LUAT35-2024/D30/K4"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-064:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Công ty tôi đang xây dựng một bến xe, muốn kết nối với đường chính, liệu chúng tôi chỉ cần xây dựng đường bên hay cần đầu tư vào lộ trình xây dựng đường cao tốc chưa đáp ứng tiêu chuẩn?
- Đáp: Bạn cần đầu tư vào lộ trình đầu tư xây dựng đường cao tốc chưa đáp ứng tiêu chuẩn, đồng thời xây dựng đường bên để kết nối với đường chính. Điều 55 Nghị định 165/2024/NĐ-CP quy định về lộ trình đầu tư xây dựng đường cao tốc chưa đáp ứng tiêu chuẩn, và Điều 30 Luật Đường bộ quy định trách nhiệm xây dựng đường bên. (Điều 55 Nghị định 165/2024/NĐ-CP; Điều 30 Luật Đường bộ)
- ⚠ chep_nguyen_van: “cao tốc chưa đáp ứng tiêu …”
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-da_buoc-064", "question": "Công ty tôi đang xây dựng một bến xe, muốn kết nối với đường chính, liệu chúng tôi chỉ cần xây dựng đường bên hay cần đầu tư vào lộ trình xây dựng đường cao tốc chưa đáp ứng tiêu chuẩn?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "B", "answer": "Bạn cần đầu tư vào lộ trình đầu tư xây dựng đường cao tốc chưa đáp ứng tiêu chuẩn, đồng thời xây dựng đường bên để kết nối với đường chính. Điều 55 Nghị định 165/2024/NĐ-CP quy định về lộ trình đầu tư xây dựng đường cao tốc chưa đáp ứng tiêu chuẩn, và Điều 30 Luật Đường bộ quy định trách nhiệm xây dựng đường bên. (Điều 55 Nghị định 165/2024/NĐ-CP; Điều 30 Luật Đường bộ)", "gold_units": ["ND165-2024/D55/K2", "LUAT35-2024/D30/K4"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-064:2"}
```

### WD-da_buoc-070 · tier B · vai: cán bộ phường · kiểu: tinh_huong_ban_than · DAN_CHIEU → ND158-2024/D24/K2/b

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 158/2024/NĐ-CP (Quy định về hoạt động vận tải đường bộ)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND158-2024/D26/K3

Điều 26. Quy định đối với vận tải người nội bộ bằng xe bốn bánh có gắn động cơ
3. Thực hiện quy định tại điểm b khoản 1, điểm b và điểm c khoản 2 Điều 24 Nghị định này.

### Điều khoản được nguồn trên dẫn chiếu tới (ND158-2024/D24/K1/b)
Mã điều khoản dùng được cho gold_units: ND158-2024/D24/K1/b

Điều 24. Quy định đối với vận tải người nội bộ bằng xe ô tô
1. Xe ô tô vận tải người nội bộ
b) Xe ô tô phải được niêm yết (dán cố định) cụm từ “XE NỘI BỘ” làm bằng vật liệu phản quang trên kính phía trước và kính phía sau xe, kích thước tối thiểu của cụm từ “XE NỘI BỘ” là 10 x 35 cm theo Mẫu số 12 Phụ lục XIII kèm theo Nghị định này. Trường hợp niêm yết bằng thiết bị điện tử phải bảo đảm cụm từ “XE NỘI BỘ” luôn được bật sáng và có kích thước tối thiểu là 10 x 35 cm;

### Điều khoản được nguồn trên dẫn chiếu tới (ND158-2024/D24/K2/b)
Mã điều khoản dùng được cho gold_units: ND158-2024/D24/K2/b

Điều 24. Quy định đối với vận tải người nội bộ bằng xe ô tô
2. Đơn vị hoạt động vận tải nội bộ bằng xe ô tô
b) Bảo đảm quy định về thời gian lái xe liên tục, thời gian làm việc trong ngày, thời gian nghỉ của người lái xe theo quy định tại khoản 1 Điều 64 Luật trật tự, an toàn giao thông đường bộ;

### Điều khoản được nguồn trên dẫn chiếu tới (ND158-2024/D24/K2/c)
Mã điều khoản dùng được cho gold_units: ND158-2024/D24/K2/c

Điều 24. Quy định đối với vận tải người nội bộ bằng xe ô tô
2. Đơn vị hoạt động vận tải nội bộ bằng xe ô tô
c) Tổ chức thực hiện bảo đảm công tác quản lý an toàn theo quy định tại khoản 10 Điều 11 Nghị định này;

### Nguồn 2
Văn bản: Nghị định số 158/2024/NĐ-CP (Quy định về hoạt động vận tải đường bộ)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND158-2024/D24/K2, ND158-2024/D24/K2/a, ND158-2024/D24/K2/b, ND158-2024/D24/K2/c, ND158-2024/D24/K2/d, ND158-2024/D24/K2/đ, ND158-2024/D24/K2/e

Điều 24. Quy định đối với vận tải người nội bộ bằng xe ô tô
2. Đơn vị hoạt động vận tải nội bộ bằng xe ô tô
a) Theo dõi, giám sát hoạt động của lái xe và phương tiện trong suốt quá trình hoạt động vận tải nội bộ; thực hiện chế độ bảo dưỡng sửa chữa phương tiện đúng quy định về bảo dưỡng kỹ thuật, sửa chữa phương tiện giao thông xe cơ giới đường bộ; kiểm tra điều kiện an toàn giao thông của xe và lái xe ô tô trước khi thực hiện nhiệm vụ vận chuyển; kiểm tra, giám sát hoạt động của xe ô tô và người lái xe trên hành trình;
b) Bảo đảm quy định về thời gian lái xe liên tục, thời gian làm việc trong ngày, thời gian nghỉ của người lái xe theo quy định tại khoản 1 Điều 64 Luật trật tự, an toàn giao thông đường bộ;
c) Tổ chức thực hiện bảo đảm công tác quản lý an toàn theo quy định tại khoản 10 Điều 11 Nghị định này;
d) Lập, cập nhật đầy đủ các nội dung quy định về quá trình hoạt động của phương tiện và lái xe thuộc đơn vị vào lý lịch phương tiện, lý lịch hành nghề lái xe, thực hiện theo dõi quá trình hoạt động và bảo dưỡng, sửa chữa phương tiện theo quy định về bảo dưỡng kỹ thuật, sửa chữa phương tiện giao thông xe cơ giới đường bộ;
đ) Không sử dụng xe ô tô chở người có giường nằm hai tầng để hoạt động trên các tuyến đường cấp V miền núi, VI miền núi;
…

### Điều khoản được nguồn trên dẫn chiếu tới (LUAT36-2024/D64/K1)
Mã điều khoản dùng được cho gold_units: LUAT36-2024/D64/K1

Điều 64. Thời gian làm việc của người lái xe ô tô kinh doanh vận tải và vận tải nội bộ
1. Thời gian lái xe của người lái xe ô tô không quá 10 giờ trong một ngày và không quá 48 giờ trong một tuần; lái xe liên tục không quá 04 giờ và bảo đảm các quy định có liên quan của Bộ luật Lao động.

### Điều khoản được nguồn trên dẫn chiếu tới (ND158-2024/D11/K10)
Mã điều khoản dùng được cho gold_units: ND158-2024/D11/K10

Điều 11. Quy định về công tác bảo đảm an toàn trong hoạt động vận tải bằng xe ô tô, bằng xe bốn bánh có gắn động cơ
10. Đơn vị hoạt động vận tải nội bộ phải theo dõi, tổng hợp hoạt động của lái xe, xe ô tô, xe bốn bánh có gắn động cơ trong quá trình vận tải cán bộ, công nhân viên, người lao động hoặc trẻ em mầm non, học sinh, sinh viên; vận tải sản phẩm, hàng hóa hoặc trang thiết bị, dụng cụ, nguyên vật liệu, nhiên liệu để phục vụ quá trình sản xuất, tiêu thụ sản phẩm hoặc dịch vụ của đơn vị vận tải nội bộ.
Đơn vị vận tải nội bộ, người lái xe phải bảo đảm tối thiểu công tác quản lý an toàn giao thông trong hoạt động vận tải nội bộ bằng xe ô tô, bằng xe bốn bánh có gắn động cơ theo các nội dung quy định sau:

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi điều hành một công ty vận tải nội bộ bằng xe ô tô, tôi cần dán cụm từ “XE NỘI BỘ” trên kính xe, còn nếu không làm thì sẽ bị xử lý gì?
- Đáp: Bạn phải dán cụm từ “XE NỘI BỘ” trên kính phía trước và phía sau xe, kích thước tối thiểu 10 x 35 cm theo mẫu số 12 Phụ lục XIII. Nếu không thực hiện, bạn sẽ bị xử phạt theo quy định của Nghị định số 158/2024/NĐ-CP.
- ⚠ da_buoc_it_hon_2_gold; chi_so_so_sai (0); chep_nguyen_van: “nội bộ bằng xe ô tô …”
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-da_buoc-070", "question": "Tôi điều hành một công ty vận tải nội bộ bằng xe ô tô, tôi cần dán cụm từ “XE NỘI BỘ” trên kính xe, còn nếu không làm thì sẽ bị xử lý gì?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "B", "answer": "Bạn phải dán cụm từ “XE NỘI BỘ” trên kính phía trước và phía sau xe, kích thước tối thiểu 10 x 35 cm theo mẫu số 12 Phụ lục XIII. Nếu không thực hiện, bạn sẽ bị xử phạt theo quy định của Nghị định số 158/2024/NĐ-CP.", "gold_units": ["ND158-2024/D24/K1/b"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-070:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là chủ đơn vị vận tải nội bộ bằng xe ô tô, tôi muốn biết có phải theo dõi, giám sát lái xe và phương tiện trong suốt quá trình hoạt động không, và nếu không tuân thủ sẽ bị xử lý gì?
- Đáp: Bạn phải theo dõi, giám sát hoạt động của lái xe và phương tiện trong suốt quá trình vận tải nội bộ, thực hiện chế độ bảo dưỡng sửa chữa phương tiện đúng quy định, kiểm tra điều kiện an toàn trước khi thực hiện nhiệm vụ. Nếu không tuân thủ, bạn sẽ bị xử phạt theo quy định của Nghị định số 158/2024/NĐ-CP.
- ⚠ da_buoc_it_hon_2_gold; chi_so_so_sai (0); chep_nguyen_van: “lái xe và phương tiện trong …”
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-da_buoc-070", "question": "Tôi là chủ đơn vị vận tải nội bộ bằng xe ô tô, tôi muốn biết có phải theo dõi, giám sát lái xe và phương tiện trong suốt quá trình hoạt động không, và nếu không tuân thủ sẽ bị xử lý gì?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "B", "answer": "Bạn phải theo dõi, giám sát hoạt động của lái xe và phương tiện trong suốt quá trình vận tải nội bộ, thực hiện chế độ bảo dưỡng sửa chữa phương tiện đúng quy định, kiểm tra điều kiện an toàn trước khi thực hiện nhiệm vụ. Nếu không tuân thủ, bạn sẽ bị xử phạt theo quy định của Nghị định số 158/2024/NĐ-CP.", "gold_units": ["ND158-2024/D24/K2/a"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-070:2"}
```

### WD-da_buoc-071 · tier B · vai: cán bộ phường · kiểu: ngan · DAN_CHIEU → ND165-2024/D32/K1

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND165-2024/D33/K1

Điều 33. Hồ sơ, tài liệu phục vụ thẩm tra, thẩm định an toàn giao thông đường bộ
1. Hồ sơ, tài liệu phục vụ thẩm tra, thẩm định an toàn giao thông đường bộ quy định tại khoản 1 Điều 32 của Nghị định này bao gồm hồ sơ tài liệu để lập, thẩm định dự án đầu tư xây dựng, thiết kế xây dựng công trình đường bộ theo quy định của pháp luật về xây dựng.

### Điều khoản được nguồn trên dẫn chiếu tới (ND165-2024/D32/K1)
Mã điều khoản dùng được cho gold_units: ND165-2024/D32/K1

Điều 32. Thẩm tra, thẩm định an toàn giao thông đường bộ
1. Trong giai đoạn lập dự án đầu tư, thiết kế triển khai sau thiết kế cơ sở, việc thẩm tra, thẩm định an toàn giao thông đường bộ được thực hiện cùng công tác thẩm tra, thẩm định báo cáo nghiên cứu khả thi, thiết kế xây dựng và các quy định sau:

### Nguồn 2
Văn bản: Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ)
Hiệu lực của trạng thái này: 2026-07-01 → nay
Mã điều khoản dùng được cho gold_units: ND165-2024/D32/K1, ND165-2024/D32/K1/a, ND165-2024/D32/K1/b

Điều 32. Thẩm tra, thẩm định an toàn giao thông đường bộ
1. Trong giai đoạn lập dự án đầu tư, thiết kế triển khai sau thiết kế cơ sở, việc thẩm tra, thẩm định an toàn giao thông đường bộ được thực hiện cùng công tác thẩm tra, thẩm định báo cáo nghiên cứu khả thi, thiết kế xây dựng và các quy định sau:
a) Chủ đầu tư dự án có trách nhiệm lựa chọn tổ chức kinh doanh dịch vụ thẩm tra an toàn giao thông đủ điều kiện để thực hiện thẩm tra an toàn giao thông trong giai đoạn lập dự án đầu tư, thiết kế triển khai sau thiết kế cơ sở. Trường hợp thuê tư vấn thẩm tra dự án, thiết kế triển khai sau thiết kế cơ sở mà tư vấn thẩm tra dự án, thiết kế có đủ điều kiện năng lực về thẩm tra an toàn giao thông đường bộ thì có thể được lựa chọn để thực hiện thẩm tra an toàn giao thông dự án, thiết kế triển khai sau thiết kế cơ sở.
b) Người có thẩm quyền quyết định phê duyệt dự án đầu tư, duyệt thiết kế tổ chức thực hiện hoặc giao cơ quan thẩm định dự án, thẩm định thiết kế thực hiện thẩm định an toàn giao thông trên cơ sở báo cáo thẩm tra an toàn giao thông của tổ chức tư vấn thẩm tra an toàn giao thông cùng với công tác thẩm định dự án đầu tư xây dựng công trình đường bộ, thẩm định thiết kế công trình đường bộ triển khai sau thiết kế cơ sở để điều chỉnh, bổ sung các hạng mục liên quan đến an toàn giao thông vào dự án, thiết kế triển khai sau thiết kế cơ sở.
…

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là cán bộ phường, muốn biết khi nào và làm gì để chọn tổ chức thẩm tra an toàn giao thông cho dự án xây dựng đường bộ?
- Đáp: Đầu tiên, chủ đầu tư dự án phải lựa chọn tổ chức kinh doanh dịch vụ thẩm tra an toàn giao thông đủ điều kiện để thực hiện thẩm tra trong giai đoạn lập dự án đầu tư, thiết kế triển khai sau thiết kế cơ sở. Nếu thuê tư vấn thẩm tra, tổ chức tư vấn phải có năng lực thẩm tra an toàn giao thông đường bộ để được lựa chọn thực hiện thẩm tra.
- ⚠ chep_nguyen_van: “thẩm tra an toàn giao thông …”

```json
{"qid": "tD-da_buoc-071", "question": "Tôi là cán bộ phường, muốn biết khi nào và làm gì để chọn tổ chức thẩm tra an toàn giao thông cho dự án xây dựng đường bộ?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "B", "answer": "Đầu tiên, chủ đầu tư dự án phải lựa chọn tổ chức kinh doanh dịch vụ thẩm tra an toàn giao thông đủ điều kiện để thực hiện thẩm tra trong giai đoạn lập dự án đầu tư, thiết kế triển khai sau thiết kế cơ sở. Nếu thuê tư vấn thẩm tra, tổ chức tư vấn phải có năng lực thẩm tra an toàn giao thông đường bộ để được lựa chọn thực hiện thẩm tra.", "gold_units": ["ND165-2024/D32/K1", "ND165-2024/D32/K1/a"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-071:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là cán bộ phường, cần biết ai quyết định phê duyệt dự án và giao thẩm tra an toàn giao thông?
- Đáp: Người có thẩm quyền quyết định phê duyệt dự án đầu tư, duyệt thiết kế tổ chức thực hiện hoặc giao cơ quan thẩm định dự án, thẩm định thiết kế thực hiện thẩm định an toàn giao thông trên cơ sở báo cáo thẩm tra an toàn giao thông của tổ chức tư vấn thẩm tra an toàn giao thông cùng với công tác thẩm định dự án đầu tư xây dựng công trình đường bộ, thẩm định thiết kế công trình đường bộ triển khai sau thiết kế cơ sở.
- ⚠ chep_nguyen_van: “quyết định phê duyệt dự án …”

```json
{"qid": "tD-da_buoc-071", "question": "Tôi là cán bộ phường, cần biết ai quyết định phê duyệt dự án và giao thẩm tra an toàn giao thông?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "B", "answer": "Người có thẩm quyền quyết định phê duyệt dự án đầu tư, duyệt thiết kế tổ chức thực hiện hoặc giao cơ quan thẩm định dự án, thẩm định thiết kế thực hiện thẩm định an toàn giao thông trên cơ sở báo cáo thẩm tra an toàn giao thông của tổ chức tư vấn thẩm tra an toàn giao thông cùng với công tác thẩm định dự án đầu tư xây dựng công trình đường bộ, thẩm định thiết kế công trình đường bộ triển khai sau thiết kế cơ sở.", "gold_units": ["ND165-2024/D32/K1", "ND165-2024/D32/K1/b"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-071:2"}
```

### WD-da_buoc-075 · tier C · vai: người mới học lái ô tô · kiểu: tinh_huong_ban_than · DAN_CHIEU → TT72-2024-BCA/D14

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Thông tư số 72/2024/TT-BCA (Quy định quy trình điều tra, giải quyết tai nạn giao thông đường bộ của Cảnh sát giao thông)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: TT72-2024-BCA/D7/K3

Điều 7. Nội dung điều tra, xác minh tình tiết của vụ tai nạn giao thông đường bộ
3. Biện pháp điều tra, xác minh tình tiết của vụ tai nạn giao thông đường bộ được thực hiện theo các điều 8, 9, 10, 11, 12, 13, 14 và 15 Thông tư này.

### Điều khoản được nguồn trên dẫn chiếu tới (TT72-2024-BCA/D10)
Mã điều khoản dùng được cho gold_units: TT72-2024-BCA/D10

Điều 10. Tạm giữ, xử lý phương tiện, đồ vật, tài liệu, giấy phép, chứng chỉ hành nghề của người điều khiển phương tiện liên quan đến vụ tai nạn giao thông đường bộ để điều tra, xác minh, giải quyết

### Điều khoản được nguồn trên dẫn chiếu tới (TT72-2024-BCA/D11)
Mã điều khoản dùng được cho gold_units: TT72-2024-BCA/D11

Điều 11. Ghi lời khai của người điều khiển phương tiện tham gia giao thông đường bộ, người bị nạn, người chứng kiến và những người có liên quan khác trong vụ tai nạn giao thông đường bộ

### Điều khoản được nguồn trên dẫn chiếu tới (TT72-2024-BCA/D12)
Mã điều khoản dùng được cho gold_units: TT72-2024-BCA/D12

Điều 12. Ghi nhận dấu vết trên thân thể của người bị nạn trong vụ tai nạn giao thông đường bộ

### Nguồn 2
Văn bản: Thông tư số 72/2024/TT-BCA (Quy định quy trình điều tra, giải quyết tai nạn giao thông đường bộ của Cảnh sát giao thông)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: TT72-2024-BCA/D14/K1

Điều 14. Giám định chuyên môn, định giá thiệt hại tài sản
1. Trường hợp cần giám định tỷ lệ tổn thương cơ thể người bị nạn, giám định dấu vết; giám định chuyên môn kỹ thuật phương tiện, cầu, đường, phà, tổ chức giao thông, chất lượng công trình giao thông liên quan trực tiếp đến vụ tai nạn giao thông đường bộ để làm căn cứ giải quyết vụ tai nạn giao thông đường bộ theo quy định tại khoản 1 Điều 59 Luật Xử lý vi phạm hành chính năm 2012 (sửa đổi bổ sung năm 2020), định giá thiệt hại về tài sản thì cán bộ Cảnh sát giao thông được giao nhiệm vụ điều tra, xác minh, giải quyết vụ tai nạn giao thông đường bộ phải báo cáo lãnh đạo có thẩm quyền ra Quyết định trưng cầu giám định, yêu cầu định giá thiệt hại tài sản để yêu cầu, đề nghị cơ quan có chức năng giám định, định giá tài sản theo quy định của pháp luật.

### Nguồn 3
Văn bản: Thông tư số 72/2024/TT-BCA (Quy định quy trình điều tra, giải quyết tai nạn giao thông đường bộ của Cảnh sát giao thông)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: TT72-2024-BCA/D14/K2

Điều 14. Giám định chuyên môn, định giá thiệt hại tài sản
2. Đối với cán bộ Cảnh sát giao thông thuộc Cục Cảnh sát giao thông hoặc Phòng Cảnh sát giao thông Công an cấp tỉnh trong quá trình xác minh, giải quyết các vụ tai nạn giao thông đường bộ theo nhiệm vụ, quyền hạn điều tra của Cơ quan thuộc lực lượng Cảnh sát trong Công an nhân dân được giao nhiệm vụ tiến hành một số hoạt động điều tra xét thấy cần phải thực hiện thủ tục trưng cầu giám định, yêu cầu định giá tài sản khi thuộc một trong các trường hợp quy định tại Điều 205 hoặc Điều 215 Bộ luật Tố tụng hình sự năm 2015 (sửa đổi, bổ sung năm 2021) thì báo cáo Cục trưởng Cục Cảnh sát giao thông hoặc Trưởng phòng Cảnh sát giao thông Công an cấp tỉnh có Công văn đề nghị Cơ quan Cảnh sát điều tra cùng cấp tiến hành trưng cầu giám định, yêu cầu định giá tài sản theo Mẫu số 15/TNĐB ban hành kèm theo Thông tư này. Trong thời hạn 24 giờ kể từ khi ban hành văn bản đề nghị Cơ quan Cảnh sát điều tra ra Quyết định trưng cầu giám định, yêu cầu định giá tài sản thì Cục Cảnh sát giao thông hoặc Phòng Cảnh sát giao thông phải gửi cho Viện kiểm sát cùng cấp với Cơ quan Cảnh sát điều tra được đề nghị.

### Nguồn 4
Văn bản: Thông tư số 72/2024/TT-BCA (Quy định quy trình điều tra, giải quyết tai nạn giao thông đường bộ của Cảnh sát giao thông)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: TT72-2024-BCA/D14/K3

Điều 14. Giám định chuyên môn, định giá thiệt hại tài sản
3. Trường hợp người bị nạn, người đại diện của người bị nạn trong vụ tai nạn giao thông đường bộ từ chối giám định thương tích mà không có lý do bất khả kháng hoặc không do trở ngại khách quan thì vận động, thuyết phục, giải thích quyền và nghĩa vụ của họ theo quy định của pháp luật; nếu họ cương quyết từ chối thì lập biên bản ghi rõ lý do từ chối, có xác nhận của họ và người chứng kiến. Chủ động thu thập hồ sơ, bệnh án tại cơ sở khám bệnh, chữa bệnh để phối hợp với các đơn vị có chức năng giám định qua hồ sơ đối với trường hợp việc yêu cầu người bị nạn trực tiếp đi giám định gặp khó khăn. Nếu người bị nạn, người đại diện của người bị nạn tiếp tục cản trở, chống đối thì tuỳ theo tính chất, mức độ xem xét xử lý theo quy định của pháp luật.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi vừa tham gia tai nạn giao thông, xe của mình bị tạm giữ. Tôi cần biết quy trình tạm giữ xe và cách ghi lời khai của mình khi cảnh sát đến, phải làm gì?
- Đáp: Bạn cần thực hiện biện pháp tạm giữ phương tiện, đồ vật, tài liệu, giấy phép, chứng chỉ hành nghề của người điều khiển phương tiện liên quan đến vụ tai nạn để điều tra, xác minh, giải quyết (Điều 10). Đồng thời, bạn phải ghi lời khai của người điều khiển phương tiện tham gia giao thông đường bộ, người bị nạn, người chứng kiến và những người có liên quan khác trong vụ tai nạn (Điều 11).
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-da_buoc-075", "question": "Tôi vừa tham gia tai nạn giao thông, xe của mình bị tạm giữ. Tôi cần biết quy trình tạm giữ xe và cách ghi lời khai của mình khi cảnh sát đến, phải làm gì?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "C", "answer": "Bạn cần thực hiện biện pháp tạm giữ phương tiện, đồ vật, tài liệu, giấy phép, chứng chỉ hành nghề của người điều khiển phương tiện liên quan đến vụ tai nạn để điều tra, xác minh, giải quyết (Điều 10). Đồng thời, bạn phải ghi lời khai của người điều khiển phương tiện tham gia giao thông đường bộ, người bị nạn, người chứng kiến và những người có liên quan khác trong vụ tai nạn (Điều 11).", "gold_units": ["TT72-2024-BCA/D10", "TT72-2024-BCA/D11"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-075:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Sau khi xe của tôi bị tạm giữ vì tai nạn, tôi muốn nộp lời khai nhưng không biết quy trình. Tôi phải làm gì để ghi lời khai và làm sao để xe được trả lại?
- Đáp: Bạn phải thực hiện biện pháp tạm giữ phương tiện, đồ vật, tài liệu, giấy phép, chứng chỉ hành nghề của người điều khiển phương tiện liên quan đến vụ tai nạn để điều tra, xác minh, giải quyết (Điều 10). Khi đó, bạn cần ghi lời khai của người điều khiển phương tiện tham gia giao thông đường bộ, người bị nạn, người chứng kiến và những người có liên quan khác trong vụ tai nạn (Điều 11). Sau khi hoàn thành các biện pháp điều tra, xe sẽ được trả lại theo quy định của Thông tư 72/2024/TT-BCA.
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-da_buoc-075", "question": "Sau khi xe của tôi bị tạm giữ vì tai nạn, tôi muốn nộp lời khai nhưng không biết quy trình. Tôi phải làm gì để ghi lời khai và làm sao để xe được trả lại?", "as_of": "2026-11-03", "question_type": "da_buoc", "tier": "C", "answer": "Bạn phải thực hiện biện pháp tạm giữ phương tiện, đồ vật, tài liệu, giấy phép, chứng chỉ hành nghề của người điều khiển phương tiện liên quan đến vụ tai nạn để điều tra, xác minh, giải quyết (Điều 10). Khi đó, bạn cần ghi lời khai của người điều khiển phương tiện tham gia giao thông đường bộ, người bị nạn, người chứng kiến và những người có liên quan khác trong vụ tai nạn (Điều 11). Sau khi hoàn thành các biện pháp điều tra, xe sẽ được trả lại theo quy định của Thông tư 72/2024/TT-BCA.", "gold_units": ["TT72-2024-BCA/D10", "TT72-2024-BCA/D11"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-da_buoc-075:2"}
```

## theo_thoi_diem — câu trả lời khác nhau trước/sau một mốc sửa đổi (đi theo cặp)

### WD-theo_thoi_diem-001 · tier A · vai: chủ doanh nghiệp vận tải · kiểu: tinh_huong_nguoi_khac · trước mốc: chưa có hiệu lực

<details><summary>Nguồn và con số</summary>

```text
### Trạng thái trước mốc (áp dụng tại 2024-12-31)
Chưa có hiệu lực (không có phiên bản).

### Trạng thái sau mốc (áp dụng tại 2025-01-01)
Văn bản: Luật Đường bộ số 35/2024/QH15
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: LUAT35-2024/D24/K2

Điều 24. Công trình an toàn giao thông đường bộ
2. Hầm cứu nạn gắn liền với hầm đường bộ, phục vụ việc thoát hiểm, cứu hộ, cứu nạn khi hầm chính xảy ra sự cố hoặc sử dụng trong công tác bảo trì hầm đường bộ. Không sử dụng hầm cứu nạn phục vụ mục đích lưu thông của các phương tiện giao thông;

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2024-12-31): Công ty anh tôi đang chuẩn bị sử dụng hầm cứu nạn gắn liền với hầm đường bộ để lưu thông xe tải trong giờ cao điểm, liệu có quy định nào cấm điều này vào ngày 15/12/2024 không?
- Đáp: Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu
- ⚠ chep_nguyen_van: “cứu nạn gắn liền với hầm …”; tham_chieu_ngu_canh
- Hỏi (2025-01-01): Công ty anh tôi đang chuẩn bị sử dụng hầm cứu nạn gắn liền với hầm đường bộ để lưu thông xe tải trong giờ cao điểm, liệu có quy định nào cấm điều này vào ngày 01/01/2025 không?
- Đáp: Không, hầm cứu nạn không được dùng cho lưu thông phương tiện giao thông. (Điều 24.2 Luật Đường bộ số 35/2024/QH15)
- ⚠ chep_nguyen_van: “cứu nạn gắn liền với hầm …”; tham_chieu_ngu_canh
- Ghi chú: Giả định rằng công ty anh tôi là một doanh nghiệp vận tải chuyên chở hàng hóa

```json
{"qid": "tD-theo_thoi_diem-001a", "question": "Công ty anh tôi đang chuẩn bị sử dụng hầm cứu nạn gắn liền với hầm đường bộ để lưu thông xe tải trong giờ cao điểm, liệu có quy định nào cấm điều này vào ngày 15/12/2024 không?", "as_of": "2024-12-31", "question_type": "theo_thoi_diem", "tier": "A", "answer": "Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu", "gold_units": [], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-001:1a", "pair_id": "pD-001"}
{"qid": "tD-theo_thoi_diem-001b", "question": "Công ty anh tôi đang chuẩn bị sử dụng hầm cứu nạn gắn liền với hầm đường bộ để lưu thông xe tải trong giờ cao điểm, liệu có quy định nào cấm điều này vào ngày 01/01/2025 không?", "as_of": "2025-01-01", "question_type": "theo_thoi_diem", "tier": "A", "answer": "Không, hầm cứu nạn không được dùng cho lưu thông phương tiện giao thông. (Điều 24.2 Luật Đường bộ số 35/2024/QH15)", "gold_units": ["LUAT35-2024/D24/K2"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-001:1b", "pair_id": "pD-001"}
```

**Nháp 2**

- Hỏi (2024-12-31): Công ty tôi muốn dùng hầm cứu nạn gắn liền với hầm đường bộ để thực hiện công tác bảo trì hầm vào ngày 20/12/2024, có quy định nào hạn chế không?
- Đáp: Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu
- ⚠ chep_nguyen_van: “cứu nạn gắn liền với hầm …”
- Hỏi (2025-01-01): Công ty tôi muốn dùng hầm cứu nạn gắn liền với hầm đường bộ để thực hiện công tác bảo trì hầm vào ngày 01/01/2025, có quy định nào hạn chế không?
- Đáp: Không, hầm cứu nạn không được dùng cho lưu thông phương tiện giao thông. (Điều 24.2 Luật Đường bộ số 35/2024/QH15)
- ⚠ chep_nguyen_van: “cứu nạn gắn liền với hầm …”
- Ghi chú: Giả định công ty tôi là một doanh nghiệp vận tải chuyên chở hàng hóa

```json
{"qid": "tD-theo_thoi_diem-001a", "question": "Công ty tôi muốn dùng hầm cứu nạn gắn liền với hầm đường bộ để thực hiện công tác bảo trì hầm vào ngày 20/12/2024, có quy định nào hạn chế không?", "as_of": "2024-12-31", "question_type": "theo_thoi_diem", "tier": "A", "answer": "Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu", "gold_units": [], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-001:2a", "pair_id": "pD-001"}
{"qid": "tD-theo_thoi_diem-001b", "question": "Công ty tôi muốn dùng hầm cứu nạn gắn liền với hầm đường bộ để thực hiện công tác bảo trì hầm vào ngày 01/01/2025, có quy định nào hạn chế không?", "as_of": "2025-01-01", "question_type": "theo_thoi_diem", "tier": "A", "answer": "Không, hầm cứu nạn không được dùng cho lưu thông phương tiện giao thông. (Điều 24.2 Luật Đường bộ số 35/2024/QH15)", "gold_units": ["LUAT35-2024/D24/K2"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-001:2b", "pair_id": "pD-001"}
```

### WD-theo_thoi_diem-002 · tier B · vai: tài xế công nghệ · kiểu: tinh_huong_ban_than · trước mốc: chưa có hiệu lực

<details><summary>Nguồn và con số</summary>

```text
### Trạng thái trước mốc (áp dụng tại 2024-12-31)
Chưa có hiệu lực (không có phiên bản).

### Trạng thái sau mốc (áp dụng tại 2025-01-01)
Văn bản: Thông tư số 73/2024/TT-BCA (Quy định công tác tuần tra, kiểm soát, xử lý vi phạm pháp luật về trật tự, an toàn giao thông đường bộ của Cảnh sát giao thông)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: TT73-2024-BCA/D27/K2

Điều 27. Yêu cầu, nguyên tắc huy động lực lượng khác trong Công an nhân dân
2. Việc huy động lực lượng phải thực hiện bằng Quyết định, Kế hoạch huy động, trong đó phải nêu rõ lực lượng, số lượng cần huy động, thời gian, tuyến, địa bàn huy động, trách nhiệm, nhiệm vụ cụ thể của Cảnh sát giao thông, lực lượng được huy động. Khi hết thời gian huy động ghi trong Quyết định hoặc Kế hoạch huy động mà không có văn bản huy động mới của cấp có thẩm quyền thì lực lượng khác trong Công an nhân dân kết thúc nhiệm vụ được huy động, chuyển sang thực hiện nhiệm vụ thường xuyên.
Việc phối hợp lực lượng phải trên cơ sở chức năng, nhiệm vụ, quyền hạn của lực lượng được huy động, quyết định của cấp có thẩm quyền và phù hợp với thực tế nhiệm vụ.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2024-12-31): Tôi là tài xế công nghệ, muốn biết khi nào có thể yêu cầu huy động lực lượng khác trong Công an để tuần tra?
- Đáp: Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu
- ⚠ chep_nguyen_van: “huy động lực lượng khác trong …”
- Hỏi (2025-01-01): Tôi là tài xế công nghệ, muốn biết khi nào có thể yêu cầu huy động lực lượng khác trong Công an để tuần tra?
- Đáp: Bạn có thể yêu cầu huy động lực lượng khác trong Công an khi có Quyết định, Kế hoạch huy động, trong đó ghi rõ lực lượng, số lượng, thời gian, tuyến, địa bàn, trách nhiệm, nhiệm vụ cụ thể của Cảnh sát giao thông. Khi hết thời gian huy động, lực lượng kết thúc nhiệm vụ và chuyển sang thực hiện nhiệm vụ thường xuyên.
- ⚠ chep_nguyen_van: “huy động lực lượng khác trong …”

```json
{"qid": "tD-theo_thoi_diem-002a", "question": "Tôi là tài xế công nghệ, muốn biết khi nào có thể yêu cầu huy động lực lượng khác trong Công an để tuần tra?", "as_of": "2024-12-31", "question_type": "theo_thoi_diem", "tier": "B", "answer": "Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu", "gold_units": [], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-002:1a", "pair_id": "pD-002"}
{"qid": "tD-theo_thoi_diem-002b", "question": "Tôi là tài xế công nghệ, muốn biết khi nào có thể yêu cầu huy động lực lượng khác trong Công an để tuần tra?", "as_of": "2025-01-01", "question_type": "theo_thoi_diem", "tier": "B", "answer": "Bạn có thể yêu cầu huy động lực lượng khác trong Công an khi có Quyết định, Kế hoạch huy động, trong đó ghi rõ lực lượng, số lượng, thời gian, tuyến, địa bàn, trách nhiệm, nhiệm vụ cụ thể của Cảnh sát giao thông. Khi hết thời gian huy động, lực lượng kết thúc nhiệm vụ và chuyển sang thực hiện nhiệm vụ thường xuyên.", "gold_units": ["TT73-2024-BCA/D27/K2"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-002:1b", "pair_id": "pD-002"}
```

### WD-theo_thoi_diem-003 · tier B · vai: người mới học lái ô tô · kiểu: tinh_huong_ban_than · trước mốc: chưa có hiệu lực

<details><summary>Nguồn và con số</summary>

```text
### Trạng thái trước mốc (áp dụng tại 2024-12-31)
Chưa có hiệu lực (không có phiên bản).

### Trạng thái sau mốc (áp dụng tại 2025-01-01)
Văn bản: Nghị định số 158/2024/NĐ-CP (Quy định về hoạt động vận tải đường bộ)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND158-2024/D58/K1, ND158-2024/D58/K1/a, ND158-2024/D58/K1/b, ND158-2024/D58/K1/c, ND158-2024/D58/K1/d

Điều 58. Thu hồi Giấy phép vận tải đường bộ quốc tế giữa Việt Nam và Campuchia
1. Cơ quan cấp giấy phép thu hồi Giấy phép vận tải đường bộ quốc tế giữa Việt Nam và Campuchia khi đơn vị kinh doanh vận tải vi phạm một trong các trường hợp sau:
a) Kinh doanh loại hình vận tải không đúng theo Giấy phép vận tải đường bộ giữa Việt Nam và Campuchia;
b) Giấy phép kinh doanh vận tải bằng xe ô tô bị cơ quan có thẩm quyền thu hồi;
c) Cơ quan quản lý nhà nước chuyên ngành tại cửa khẩu đề nghị thu hồi vì lý do vi phạm liên quan đến các hoạt động xuất nhập cảnh, xuất nhập khẩu tại cửa khẩu, quy định về quản lý hoạt động ở khu vực cửa khẩu;
d) Chấm dứt hoạt động theo quy định của pháp luật.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2024-12-31): Tôi đang điều hành công ty vận tải, chúng tôi đã nhận giấy phép vận tải quốc tế giữa Việt Nam và Campuchia, nhưng gần đây chúng tôi đã chuyển sang vận chuyển hàng hóa không được phép theo giấy phép. Khi nào giấy phép sẽ bị thu hồi?
- Đáp: Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu.
- ⚠ chep_nguyen_van: “quốc tế giữa việt nam và …”
- Hỏi (2025-01-01): Tôi đang điều hành công ty vận tải, chúng tôi đã nhận giấy phép vận tải quốc tế giữa Việt Nam và Campuchia, nhưng gần đây chúng tôi đã chuyển sang vận chuyển hàng hóa không được phép theo giấy phép. Khi nào giấy phép sẽ bị thu hồi?
- Đáp: Giấy phép vận tải quốc tế giữa Việt Nam và Campuchia sẽ bị thu hồi khi công ty vi phạm một trong các trường hợp quy định, ví dụ như chuyển sang vận chuyển loại hình không đúng theo giấy phép. (Điều 58, Nghị định 158/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “quốc tế giữa việt nam và …”

```json
{"qid": "tD-theo_thoi_diem-003a", "question": "Tôi đang điều hành công ty vận tải, chúng tôi đã nhận giấy phép vận tải quốc tế giữa Việt Nam và Campuchia, nhưng gần đây chúng tôi đã chuyển sang vận chuyển hàng hóa không được phép theo giấy phép. Khi nào giấy phép sẽ bị thu hồi?", "as_of": "2024-12-31", "question_type": "theo_thoi_diem", "tier": "B", "answer": "Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu.", "gold_units": [], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-003:1a", "pair_id": "pD-003"}
{"qid": "tD-theo_thoi_diem-003b", "question": "Tôi đang điều hành công ty vận tải, chúng tôi đã nhận giấy phép vận tải quốc tế giữa Việt Nam và Campuchia, nhưng gần đây chúng tôi đã chuyển sang vận chuyển hàng hóa không được phép theo giấy phép. Khi nào giấy phép sẽ bị thu hồi?", "as_of": "2025-01-01", "question_type": "theo_thoi_diem", "tier": "B", "answer": "Giấy phép vận tải quốc tế giữa Việt Nam và Campuchia sẽ bị thu hồi khi công ty vi phạm một trong các trường hợp quy định, ví dụ như chuyển sang vận chuyển loại hình không đúng theo giấy phép. (Điều 58, Nghị định 158/2024/NĐ-CP)", "gold_units": ["ND158-2024/D58/K1"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-003:1b", "pair_id": "pD-003"}
```

**Nháp 2**

- Hỏi (2024-12-31): Tôi đang điều hành công ty vận tải, chúng tôi đã nhận giấy phép vận tải quốc tế giữa Việt Nam và Campuchia, nhưng gần đây chúng tôi đã chuyển sang vận chuyển hàng hóa không được phép theo giấy phép. Khi nào giấy phép sẽ bị thu hồi?
- Đáp: Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu.
- ⚠ chep_nguyen_van: “quốc tế giữa việt nam và …”
- Hỏi (2025-01-01): Tôi đang điều hành công ty vận tải, chúng tôi đã nhận giấy phép vận tải quốc tế giữa Việt Nam và Campuchia, nhưng gần đây chúng tôi đã chuyển sang vận chuyển hàng hóa không được phép theo giấy phép. Khi nào giấy phép sẽ bị thu hồi?
- Đáp: Giấy phép vận tải quốc tế giữa Việt Nam và Campuchia sẽ bị thu hồi khi công ty vi phạm một trong các trường hợp quy định, ví dụ như chuyển sang vận chuyển loại hình không đúng theo giấy phép. (Điều 58, Nghị định 158/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “quốc tế giữa việt nam và …”

```json
{"qid": "tD-theo_thoi_diem-003a", "question": "Tôi đang điều hành công ty vận tải, chúng tôi đã nhận giấy phép vận tải quốc tế giữa Việt Nam và Campuchia, nhưng gần đây chúng tôi đã chuyển sang vận chuyển hàng hóa không được phép theo giấy phép. Khi nào giấy phép sẽ bị thu hồi?", "as_of": "2024-12-31", "question_type": "theo_thoi_diem", "tier": "B", "answer": "Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu.", "gold_units": [], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-003:2a", "pair_id": "pD-003"}
{"qid": "tD-theo_thoi_diem-003b", "question": "Tôi đang điều hành công ty vận tải, chúng tôi đã nhận giấy phép vận tải quốc tế giữa Việt Nam và Campuchia, nhưng gần đây chúng tôi đã chuyển sang vận chuyển hàng hóa không được phép theo giấy phép. Khi nào giấy phép sẽ bị thu hồi?", "as_of": "2025-01-01", "question_type": "theo_thoi_diem", "tier": "B", "answer": "Giấy phép vận tải quốc tế giữa Việt Nam và Campuchia sẽ bị thu hồi khi công ty vi phạm một trong các trường hợp quy định, ví dụ như chuyển sang vận chuyển loại hình không đúng theo giấy phép. (Điều 58, Nghị định 158/2024/NĐ-CP)", "gold_units": ["ND158-2024/D58/K1"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-003:2b", "pair_id": "pD-003"}
```

### WD-theo_thoi_diem-004 · tier B · vai: phụ huynh có con dưới 18 tuổi · kiểu: tinh_huong_ban_than · trước mốc: chưa có hiệu lực

<details><summary>Nguồn và con số</summary>

```text
### Trạng thái trước mốc (áp dụng tại 2024-12-31)
Chưa có hiệu lực (không có phiên bản).

### Trạng thái sau mốc (áp dụng tại 2025-01-01)
Văn bản: Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ)
Hiệu lực của trạng thái này: 2025-01-01 → 2026-06-30
Mã điều khoản dùng được cho gold_units: ND165-2024/D6/K1

Điều 6. Quản lý quốc lộ đi qua đô thị loại đặc biệt; tuyến, đoạn tuyến quốc lộ không phù hợp quy hoạch được duyệt; tuyến, đoạn tuyến quốc lộ đã có đường tránh thay thế phù hợp với quy hoạch; đường gom, đường bên tách khỏi quốc lộ cho địa phương quản lý
1. Bộ Giao thông vận tải có trách nhiệm tổ chức lập hồ sơ điều chuyển tài sản kết cấu hạ tầng đường bộ các quốc lộ đi qua đô thị loại đặc biệt; tuyến, đoạn tuyến quốc lộ không phù hợp quy hoạch được duyệt; tuyến, đoạn tuyến quốc lộ đã có đường tránh thay thế phù hợp với quy hoạch; đường gom, đường bên tách khỏi quốc lộ và bàn giao cho Ủy ban nhân dân cấp tỉnh quản lý.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2024-12-31): Tôi là phụ huynh có con dưới 18 tuổi, vào ngày 15 tháng 12 năm 2024, tôi muốn biết quy định về việc lập hồ sơ chuyển tài sản hạ tầng quốc lộ đi qua đô thị loại đặc biệt là gì?
- Đáp: Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu.
- ⚠ chep_nguyen_van: “lộ đi qua đô thị loại …”
- Hỏi (2025-01-01): Tôi là phụ huynh có con dưới 18 tuổi, vào ngày 2 tháng 1 năm 2025, tôi muốn biết quy định về việc lập hồ sơ chuyển tài sản hạ tầng quốc lộ đi qua đô thị loại đặc biệt là gì?
- Đáp: Bộ Giao thông vận tải có trách nhiệm tổ chức lập hồ sơ điều chuyển tài sản kết cấu hạ tầng đường bộ các quốc lộ đi qua đô thị loại đặc biệt; tuyến, đoạn tuyến quốc lộ không phù hợp quy hoạch được duyệt; tuyến, đoạn tuyến quốc lộ đã có đường tránh thay thế phù hợp với quy hoạch; đường gom, đường bên tách khỏi quốc lộ và bàn giao cho Ủy ban nhân dân cấp tỉnh quản lý. (ND165-2024/D6/K1)
- ⚠ chep_nguyen_van: “lộ đi qua đô thị loại …”
- Ghi chú: Không có số liệu cần nêu trong câu hỏi

```json
{"qid": "tD-theo_thoi_diem-004a", "question": "Tôi là phụ huynh có con dưới 18 tuổi, vào ngày 15 tháng 12 năm 2024, tôi muốn biết quy định về việc lập hồ sơ chuyển tài sản hạ tầng quốc lộ đi qua đô thị loại đặc biệt là gì?", "as_of": "2024-12-31", "question_type": "theo_thoi_diem", "tier": "B", "answer": "Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu.", "gold_units": [], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-004:1a", "pair_id": "pD-004"}
{"qid": "tD-theo_thoi_diem-004b", "question": "Tôi là phụ huynh có con dưới 18 tuổi, vào ngày 2 tháng 1 năm 2025, tôi muốn biết quy định về việc lập hồ sơ chuyển tài sản hạ tầng quốc lộ đi qua đô thị loại đặc biệt là gì?", "as_of": "2025-01-01", "question_type": "theo_thoi_diem", "tier": "B", "answer": "Bộ Giao thông vận tải có trách nhiệm tổ chức lập hồ sơ điều chuyển tài sản kết cấu hạ tầng đường bộ các quốc lộ đi qua đô thị loại đặc biệt; tuyến, đoạn tuyến quốc lộ không phù hợp quy hoạch được duyệt; tuyến, đoạn tuyến quốc lộ đã có đường tránh thay thế phù hợp với quy hoạch; đường gom, đường bên tách khỏi quốc lộ và bàn giao cho Ủy ban nhân dân cấp tỉnh quản lý. (ND165-2024/D6/K1)", "gold_units": ["ND165-2024/D6/K1"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-004:1b", "pair_id": "pD-004"}
```

### WD-theo_thoi_diem-005 · tier A · vai: phụ huynh có con dưới 18 tuổi · kiểu: tinh_huong_nguoi_khac · trước mốc: chưa có hiệu lực

<details><summary>Nguồn và con số</summary>

```text
### Trạng thái trước mốc (áp dụng tại 2024-12-31)
Chưa có hiệu lực (không có phiên bản).

### Trạng thái sau mốc (áp dụng tại 2025-01-01)
Văn bản: Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: LUAT36-2024/D81/K2

Điều 81. Phát hiện, tiếp nhận, xử lý tin báo tai nạn giao thông đường bộ
2. Cơ quan Công an khi nhận được tin báo vụ tai nạn giao thông đường bộ phải tổ chức ngay lực lượng đến hiện trường thực hiện các biện pháp quy định tại khoản 3 Điều 76 của Luật này và các biện pháp khác để giải quyết vụ tai nạn giao thông đường bộ theo quy định của pháp luật.

### Điều khoản được nguồn trên dẫn chiếu tới (LUAT36-2024/D76/K3)
Mã điều khoản dùng được cho gold_units: LUAT36-2024/D76/K3

Điều 76. Giải quyết tình huống đột xuất gây mất trật tự, an toàn giao thông trên đường bộ
3. Cơ quan Công an, cơ quan quản lý đường bộ khi phát hiện hoặc tiếp nhận thông tin về tình huống quy định tại khoản 1 Điều này, theo chức năng, nhiệm vụ của mình, có trách nhiệm sau đây:

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2024-12-31): Anh tôi đã nghe nói con anh ấy đã tham gia tai nạn giao thông, anh ấy hỏi khi nào cảnh sát sẽ tới hiện trường?
- Đáp: Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu.
- Hỏi (2025-01-01): Anh tôi đã nghe nói con anh ấy đã tham gia tai nạn giao thông, anh ấy hỏi khi nào cảnh sát sẽ tới hiện trường?
- Đáp: Cơ quan Công an khi nhận được tin báo vụ tai nạn giao thông đường bộ phải tổ chức ngay lực lượng đến hiện trường thực hiện các biện pháp quy định tại khoản 3 Điều 76 của Luật này và các biện pháp khác để giải quyết vụ tai nạn giao thông đường bộ theo quy định của pháp luật. (khoản 3 Điều 81 Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15)
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-theo_thoi_diem-005a", "question": "Anh tôi đã nghe nói con anh ấy đã tham gia tai nạn giao thông, anh ấy hỏi khi nào cảnh sát sẽ tới hiện trường?", "as_of": "2024-12-31", "question_type": "theo_thoi_diem", "tier": "A", "answer": "Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu.", "gold_units": [], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-005:1a", "pair_id": "pD-005"}
{"qid": "tD-theo_thoi_diem-005b", "question": "Anh tôi đã nghe nói con anh ấy đã tham gia tai nạn giao thông, anh ấy hỏi khi nào cảnh sát sẽ tới hiện trường?", "as_of": "2025-01-01", "question_type": "theo_thoi_diem", "tier": "A", "answer": "Cơ quan Công an khi nhận được tin báo vụ tai nạn giao thông đường bộ phải tổ chức ngay lực lượng đến hiện trường thực hiện các biện pháp quy định tại khoản 3 Điều 76 của Luật này và các biện pháp khác để giải quyết vụ tai nạn giao thông đường bộ theo quy định của pháp luật. (khoản 3 Điều 81 Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15)", "gold_units": ["LUAT36-2024/D81/K2"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-005:1b", "pair_id": "pD-005"}
```

**Nháp 2**

- Hỏi (2024-12-31): Công ty tôi đã được thông báo rằng một nhân viên trẻ dưới 18 tuổi đã bị tai nạn khi lái xe, công ty hỏi cảnh sát có phải ngay lập tức tới không?
- Đáp: Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu.
- Hỏi (2025-01-01): Công ty tôi đã được thông báo rằng một nhân viên trẻ dưới 18 tuổi đã bị tai nạn khi lái xe, công ty hỏi cảnh sát có phải ngay lập tức tới không?
- Đáp: Cơ quan Công an khi nhận được tin báo vụ tai nạn giao thông đường bộ phải tổ chức ngay lực lượng đến hiện trường thực hiện các biện pháp quy định tại khoản 3 Điều 76 của Luật này và các biện pháp khác để giải quyết vụ tai nạn giao thông đường bộ theo quy định của pháp luật. (khoản 3 Điều 81 Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15)
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-theo_thoi_diem-005a", "question": "Công ty tôi đã được thông báo rằng một nhân viên trẻ dưới 18 tuổi đã bị tai nạn khi lái xe, công ty hỏi cảnh sát có phải ngay lập tức tới không?", "as_of": "2024-12-31", "question_type": "theo_thoi_diem", "tier": "A", "answer": "Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu.", "gold_units": [], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-005:2a", "pair_id": "pD-005"}
{"qid": "tD-theo_thoi_diem-005b", "question": "Công ty tôi đã được thông báo rằng một nhân viên trẻ dưới 18 tuổi đã bị tai nạn khi lái xe, công ty hỏi cảnh sát có phải ngay lập tức tới không?", "as_of": "2025-01-01", "question_type": "theo_thoi_diem", "tier": "A", "answer": "Cơ quan Công an khi nhận được tin báo vụ tai nạn giao thông đường bộ phải tổ chức ngay lực lượng đến hiện trường thực hiện các biện pháp quy định tại khoản 3 Điều 76 của Luật này và các biện pháp khác để giải quyết vụ tai nạn giao thông đường bộ theo quy định của pháp luật. (khoản 3 Điều 81 Luật Trật tự, an toàn giao thông đường bộ số 36/2024/QH15)", "gold_units": ["LUAT36-2024/D81/K2"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-005:2b", "pair_id": "pD-005"}
```

### WD-theo_thoi_diem-006 · tier A · vai: cán bộ phường · kiểu: tinh_huong_nguoi_khac · trước mốc: chưa có hiệu lực

<details><summary>Nguồn và con số</summary>

```text
### Trạng thái trước mốc (áp dụng tại 2024-12-31)
Chưa có hiệu lực (không có phiên bản).

### Trạng thái sau mốc (áp dụng tại 2025-01-01)
Văn bản: Thông tư số 79/2024/TT-BCA (Quy định về cấp, thu hồi chứng nhận đăng ký xe, biển số xe cơ giới, xe máy chuyên dùng)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D32/K4

Điều 32. Giải quyết đăng ký sang tên xe đối với xe đã chuyển quyền sở hữu qua nhiều tổ chức, cá nhân
4. Hồ sơ, thủ tục đăng ký sang tên xe: Thực hiện theo quy định tại khoản 2 Điều 16, khoản 2 Điều 17 Thông tư này.

### Điều khoản được nguồn trên dẫn chiếu tới (TT79-2024-BCA/D16/K2)
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D16/K2

Điều 16. Hồ sơ đăng ký sang tên xe
2. Hồ sơ đăng ký

### Điều khoản được nguồn trên dẫn chiếu tới (TT79-2024-BCA/D17/K2)
Mã điều khoản dùng được cho gold_units: TT79-2024-BCA/D17/K2

Điều 17. Thủ tục đăng ký sang tên xe
2. Thủ tục đăng ký

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2024-12-31): Công ty tôi muốn chuyển quyền sở hữu một chiếc ô tô đã qua nhiều lần chuyển sang tên, tôi cần nộp hồ sơ gì để đăng ký sang tên xe?
- Đáp: Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu
- Hỏi (2025-01-01): Công ty tôi muốn chuyển quyền sở hữu một chiếc ô tô đã qua nhiều lần chuyển sang tên, tôi cần nộp hồ sơ gì để đăng ký sang tên xe?
- Đáp: Công ty cần nộp hồ sơ theo quy định tại khoản 2 Điều 16 và khoản 2 Điều 17 Thông tư số 79/2024/TT-BCA. (khoản 2 Điều 16 và khoản 2 Điều 17 Thông tư 79/2024/TT-BCA)

```json
{"qid": "tD-theo_thoi_diem-006a", "question": "Công ty tôi muốn chuyển quyền sở hữu một chiếc ô tô đã qua nhiều lần chuyển sang tên, tôi cần nộp hồ sơ gì để đăng ký sang tên xe?", "as_of": "2024-12-31", "question_type": "theo_thoi_diem", "tier": "A", "answer": "Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu", "gold_units": [], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-006:1a", "pair_id": "pD-006"}
{"qid": "tD-theo_thoi_diem-006b", "question": "Công ty tôi muốn chuyển quyền sở hữu một chiếc ô tô đã qua nhiều lần chuyển sang tên, tôi cần nộp hồ sơ gì để đăng ký sang tên xe?", "as_of": "2025-01-01", "question_type": "theo_thoi_diem", "tier": "A", "answer": "Công ty cần nộp hồ sơ theo quy định tại khoản 2 Điều 16 và khoản 2 Điều 17 Thông tư số 79/2024/TT-BCA. (khoản 2 Điều 16 và khoản 2 Điều 17 Thông tư 79/2024/TT-BCA)", "gold_units": ["TT79-2024-BCA/D32/K4"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-006:1b", "pair_id": "pD-006"}
```

**Nháp 2**

- Hỏi (2024-12-31): Anh tôi muốn chuyển quyền sở hữu một chiếc ô tô đã qua nhiều lần chuyển sang tên, anh ấy cần nộp hồ sơ gì để đăng ký sang tên xe?
- Đáp: Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu
- Hỏi (2025-01-01): Anh tôi muốn chuyển quyền sở hữu một chiếc ô tô đã qua nhiều lần chuyển sang tên, anh ấy cần nộp hồ sơ gì để đăng ký sang tên xe?
- Đáp: Anh cần nộp hồ sơ theo quy định tại khoản 2 Điều 16 và khoản 2 Điều 17 Thông tư số 79/2024/TT-BCA. (khoản 2 Điều 16 và khoản 2 Điều 17 Thông tư 79/2024/TT-BCA)

```json
{"qid": "tD-theo_thoi_diem-006a", "question": "Anh tôi muốn chuyển quyền sở hữu một chiếc ô tô đã qua nhiều lần chuyển sang tên, anh ấy cần nộp hồ sơ gì để đăng ký sang tên xe?", "as_of": "2024-12-31", "question_type": "theo_thoi_diem", "tier": "A", "answer": "Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu", "gold_units": [], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-006:2a", "pair_id": "pD-006"}
{"qid": "tD-theo_thoi_diem-006b", "question": "Anh tôi muốn chuyển quyền sở hữu một chiếc ô tô đã qua nhiều lần chuyển sang tên, anh ấy cần nộp hồ sơ gì để đăng ký sang tên xe?", "as_of": "2025-01-01", "question_type": "theo_thoi_diem", "tier": "A", "answer": "Anh cần nộp hồ sơ theo quy định tại khoản 2 Điều 16 và khoản 2 Điều 17 Thông tư số 79/2024/TT-BCA. (khoản 2 Điều 16 và khoản 2 Điều 17 Thông tư 79/2024/TT-BCA)", "gold_units": ["TT79-2024-BCA/D32/K4"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-006:2b", "pair_id": "pD-006"}
```

### WD-theo_thoi_diem-007 · tier B · vai: người lớn tuổi đi xe đạp điện · kiểu: tinh_huong_ban_than · trước mốc: chưa có hiệu lực

<details><summary>Nguồn và con số</summary>

```text
### Trạng thái trước mốc (áp dụng tại 2024-12-31)
Chưa có hiệu lực (không có phiên bản).

### Trạng thái sau mốc (áp dụng tại 2025-01-01)
Văn bản: Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ)
Hiệu lực của trạng thái này: 2025-01-01 → 2026-06-30
Mã điều khoản dùng được cho gold_units: ND165-2024/D64/K1, ND165-2024/D64/K1/a, ND165-2024/D64/K1/b, ND165-2024/D64/K1/c, ND165-2024/D64/K1/d

Điều 64. Quy định chung về hệ thống quản lý giao thông thông minh
1. Hệ thống quản lý giao thông thông minh cung cấp các dịch vụ giao thông thông minh sau:
a) Quản lý, giám sát, điều hành giao thông đường bộ;
b) Thanh toán điện tử giao thông đường bộ;
c) Quản lý phương tiện vận tải;
d) Cung cấp thông tin giao thông.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2024-12-31): Tôi muốn biết có thể thanh toán điện tử khi đi xe đạp điện không?
- Đáp: Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu.
- Hỏi (2025-01-01): Tôi muốn biết có thể thanh toán điện tử khi đi xe đạp điện không?
- Đáp: Bạn có thể thanh toán điện tử khi đi xe đạp điện. Điều 64 khoản b của Nghị định 165/2024/NĐ-CP quy định cung cấp dịch vụ thanh toán điện tử giao thông đường bộ.

```json
{"qid": "tD-theo_thoi_diem-007a", "question": "Tôi muốn biết có thể thanh toán điện tử khi đi xe đạp điện không?", "as_of": "2024-12-31", "question_type": "theo_thoi_diem", "tier": "B", "answer": "Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu.", "gold_units": [], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-007:1a", "pair_id": "pD-007"}
{"qid": "tD-theo_thoi_diem-007b", "question": "Tôi muốn biết có thể thanh toán điện tử khi đi xe đạp điện không?", "as_of": "2025-01-01", "question_type": "theo_thoi_diem", "tier": "B", "answer": "Bạn có thể thanh toán điện tử khi đi xe đạp điện. Điều 64 khoản b của Nghị định 165/2024/NĐ-CP quy định cung cấp dịch vụ thanh toán điện tử giao thông đường bộ.", "gold_units": ["ND165-2024/D64/K1/b"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-007:1b", "pair_id": "pD-007"}
```

**Nháp 2**

- Hỏi (2024-12-31): Tôi có thể nhận thông tin giao thông khi đi xe đạp điện không?
- Đáp: Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu.
- Hỏi (2025-01-01): Tôi có thể nhận thông tin giao thông khi đi xe đạp điện không?
- Đáp: Bạn có thể nhận thông tin giao thông khi đi xe đạp điện. Điều 64 khoản d của Nghị định 165/2024/NĐ-CP quy định cung cấp dịch vụ cung cấp thông tin giao thông.

```json
{"qid": "tD-theo_thoi_diem-007a", "question": "Tôi có thể nhận thông tin giao thông khi đi xe đạp điện không?", "as_of": "2024-12-31", "question_type": "theo_thoi_diem", "tier": "B", "answer": "Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu.", "gold_units": [], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-007:2a", "pair_id": "pD-007"}
{"qid": "tD-theo_thoi_diem-007b", "question": "Tôi có thể nhận thông tin giao thông khi đi xe đạp điện không?", "as_of": "2025-01-01", "question_type": "theo_thoi_diem", "tier": "B", "answer": "Bạn có thể nhận thông tin giao thông khi đi xe đạp điện. Điều 64 khoản d của Nghị định 165/2024/NĐ-CP quy định cung cấp dịch vụ cung cấp thông tin giao thông.", "gold_units": ["ND165-2024/D64/K1/d"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-007:2b", "pair_id": "pD-007"}
```

### WD-theo_thoi_diem-008 · tier B · vai: tài xế công nghệ · kiểu: tinh_huong_ban_than

<details><summary>Nguồn và con số</summary>

```text
### Trạng thái trước mốc (áp dụng tại 2026-06-30)
Văn bản: Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ)
Hiệu lực của trạng thái này: 2025-01-01 → 2026-06-30
Mã điều khoản dùng được cho gold_units: ND165-2024/D28/K3

Điều 28. Vị trí nút giao đấu nối đường khác vào đường cao tốc
3. Bộ Giao thông vận tải, Ủy ban nhân dân cấp tỉnh chấp thuận bổ sung vị trí đấu nối với đường cao tốc thuộc phạm vi quản lý đối với trường hợp quy định tại khoản 2 Điều này.

### Điều khoản được nguồn trên dẫn chiếu tới (ND165-2024/D28/K2)
Mã điều khoản dùng được cho gold_units: ND165-2024/D28/K2

Điều 28. Vị trí nút giao đấu nối đường khác vào đường cao tốc
2. Trường hợp bổ sung vị trí nút giao đấu nối đường khác với đường cao tốc ngoài quy định tại khoản 1 Điều này trong giai đoạn đầu tư xây dựng đường cao tốc, giai đoạn khai thác đường cao tốc thì phải bảo đảm:

### Trạng thái sau mốc (áp dụng tại 2026-07-01)
Văn bản: Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ)
Hiệu lực của trạng thái này: 2026-07-01 → nay
Mã điều khoản dùng được cho gold_units: ND165-2024/D28/K3

Điều 28. Vị trí nút giao đấu nối đường khác vào đường cao tốc
3. Bộ Xây dựng, Ủy ban nhân dân cấp tỉnh chấp thuận bổ sung vị trí đấu nối với đường cao tốc thuộc phạm vi quản lý đối với trường hợp quy định tại khoản 2 Điều này.

### Điều khoản được nguồn trên dẫn chiếu tới (ND165-2024/D28/K2)
Mã điều khoản dùng được cho gold_units: ND165-2024/D28/K2

Điều 28. Vị trí nút giao đấu nối đường khác vào đường cao tốc
2. Trường hợp bổ sung vị trí nút giao đấu nối đường khác với đường cao tốc ngoài quy định tại khoản 1 Điều này trong giai đoạn đầu tư xây dựng đường cao tốc, giai đoạn khai thác đường cao tốc thì phải bảo đảm:

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-06-30): Tôi đang lên kế hoạch mở một nút giao giữa đường cao tốc và đường tỉnh lộ, nhưng chưa biết khi nào Bộ Giao thông vận tải, Ủy ban nhân dân cấp tỉnh sẽ phê duyệt?
- Đáp: Bộ Giao thông vận tải, Ủy ban nhân dân cấp tỉnh chấp thuận bổ sung vị trí đấu nối với đường cao tốc thuộc phạm vi quản lý đối với trường hợp quy định tại khoản 2 Điều này.
- ⚠ chep_nguyen_van: “bộ giao thông vận tải ủy …”
- Hỏi (2026-07-01): Tôi đang lên kế hoạch mở một nút giao giữa đường cao tốc và đường tỉnh lộ, nhưng chưa biết khi nào Bộ Xây dựng, Ủy ban nhân dân cấp tỉnh sẽ phê duyệt?
- Đáp: Bộ Xây dựng, Ủy ban nhân dân cấp tỉnh chấp thuận bổ sung vị trí đấu nối với đường cao tốc thuộc phạm vi quản lý đối với trường hợp quy định tại khoản 2 Điều này.
- ⚠ chep_nguyen_van: “bộ xây dựng ủy ban nhân …”

```json
{"qid": "tD-theo_thoi_diem-008a", "question": "Tôi đang lên kế hoạch mở một nút giao giữa đường cao tốc và đường tỉnh lộ, nhưng chưa biết khi nào Bộ Giao thông vận tải, Ủy ban nhân dân cấp tỉnh sẽ phê duyệt?", "as_of": "2026-06-30", "question_type": "theo_thoi_diem", "tier": "B", "answer": "Bộ Giao thông vận tải, Ủy ban nhân dân cấp tỉnh chấp thuận bổ sung vị trí đấu nối với đường cao tốc thuộc phạm vi quản lý đối với trường hợp quy định tại khoản 2 Điều này.", "gold_units": ["ND165-2024/D28/K3"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-008:1a", "pair_id": "pD-008"}
{"qid": "tD-theo_thoi_diem-008b", "question": "Tôi đang lên kế hoạch mở một nút giao giữa đường cao tốc và đường tỉnh lộ, nhưng chưa biết khi nào Bộ Xây dựng, Ủy ban nhân dân cấp tỉnh sẽ phê duyệt?", "as_of": "2026-07-01", "question_type": "theo_thoi_diem", "tier": "B", "answer": "Bộ Xây dựng, Ủy ban nhân dân cấp tỉnh chấp thuận bổ sung vị trí đấu nối với đường cao tốc thuộc phạm vi quản lý đối với trường hợp quy định tại khoản 2 Điều này.", "gold_units": ["ND165-2024/D28/K3"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-008:1b", "pair_id": "pD-008"}
```

**Nháp 2**

- Hỏi (2026-06-30): Tôi muốn xây dựng một nút giao giữa đường cao tốc và đường tỉnh lộ, nhưng chưa biết Bộ Giao thông vận tải, Ủy ban nhân dân cấp tỉnh có phê duyệt chưa?
- Đáp: Bộ Giao thông vận tải, Ủy ban nhân dân cấp tỉnh chấp thuận bổ sung vị trí đấu nối với đường cao tốc thuộc phạm vi quản lý đối với trường hợp quy định tại khoản 2 Điều này.
- ⚠ chep_nguyen_van: “bộ giao thông vận tải ủy …”
- Hỏi (2026-07-01): Tôi muốn xây dựng một nút giao giữa đường cao tốc và đường tỉnh lộ, nhưng chưa biết Bộ Xây dựng, Ủy ban nhân dân cấp tỉnh có phê duyệt chưa?
- Đáp: Bộ Xây dựng, Ủy ban nhân dân cấp tỉnh chấp thuận bổ sung vị trí đấu nối với đường cao tốc thuộc phạm vi quản lý đối với trường hợp quy định tại khoản 2 Điều này.
- ⚠ chep_nguyen_van: “bộ xây dựng ủy ban nhân …”

```json
{"qid": "tD-theo_thoi_diem-008a", "question": "Tôi muốn xây dựng một nút giao giữa đường cao tốc và đường tỉnh lộ, nhưng chưa biết Bộ Giao thông vận tải, Ủy ban nhân dân cấp tỉnh có phê duyệt chưa?", "as_of": "2026-06-30", "question_type": "theo_thoi_diem", "tier": "B", "answer": "Bộ Giao thông vận tải, Ủy ban nhân dân cấp tỉnh chấp thuận bổ sung vị trí đấu nối với đường cao tốc thuộc phạm vi quản lý đối với trường hợp quy định tại khoản 2 Điều này.", "gold_units": ["ND165-2024/D28/K3"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-008:2a", "pair_id": "pD-008"}
{"qid": "tD-theo_thoi_diem-008b", "question": "Tôi muốn xây dựng một nút giao giữa đường cao tốc và đường tỉnh lộ, nhưng chưa biết Bộ Xây dựng, Ủy ban nhân dân cấp tỉnh có phê duyệt chưa?", "as_of": "2026-07-01", "question_type": "theo_thoi_diem", "tier": "B", "answer": "Bộ Xây dựng, Ủy ban nhân dân cấp tỉnh chấp thuận bổ sung vị trí đấu nối với đường cao tốc thuộc phạm vi quản lý đối với trường hợp quy định tại khoản 2 Điều này.", "gold_units": ["ND165-2024/D28/K3"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-008:2b", "pair_id": "pD-008"}
```

### WD-theo_thoi_diem-009 · tier B · vai: sinh viên đi xe máy · kiểu: neu_van_ban

<details><summary>Nguồn và con số</summary>

```text
### Trạng thái trước mốc (áp dụng tại 2026-06-30)
Văn bản: Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ)
Hiệu lực của trạng thái này: 2025-01-01 → 2026-06-30
Mã điều khoản dùng được cho gold_units: ND165-2024/D58/K4

Điều 58. Nguyên tắc xây dựng, cập nhật, quản lý, vận hành, khai thác, sử dụng, bảo trì cơ sở dữ liệu đường bộ
4. Việc xây dựng, quản lý, khai thác, sử dụng cơ sở dữ liệu đường bộ tuân thủ các quy định của Luật Đường bộ, Luật Công nghệ thông tin, Luật An toàn thông tin mạng, Luật An ninh mạng, Luật Giao dịch điện tử; quy định pháp luật về Khung kiến trúc tổng thể quốc gia số và Khung kiến trúc Chính phủ điện tử; quy định về quản lý, kết nối và chia sẻ dữ liệu số của cơ quan nhà nước; quy định về bảo đảm, bảo vệ đời sống riêng tư, bí mật cá nhân và các quy định pháp luật khác có liên quan.

### Trạng thái sau mốc (áp dụng tại 2026-07-01)
Văn bản: Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ)
Hiệu lực của trạng thái này: 2026-07-01 → nay
Mã điều khoản dùng được cho gold_units: ND165-2024/D58/K4

Điều 58. Nguyên tắc xây dựng, cập nhật, quản lý, vận hành, khai thác, sử dụng, bảo trì cơ sở dữ liệu đường bộ
4. Việc xây dựng, quản lý, khai thác, sử dụng cơ sở dữ liệu đường bộ tuân thủ các quy định của Luật Đường bộ, Luật Công nghệ thông tin, Luật An ninh mạng, Luật Giao dịch điện tử; quy định pháp luật về Khung kiến trúc tổng thể quốc gia số và Khung kiến trúc chính phủ số Việt Nam; quy định về quản lý, kết nối và chia sẻ dữ liệu số của cơ quan nhà nước; quy định về bảo đảm, bảo vệ đời sống riêng tư, bí mật cá nhân và các quy định khác của pháp luật có liên quan.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-06-30): Theo Nghị định 165/2024/NĐ-CP, khi xây dựng cơ sở dữ liệu đường bộ, tôi cần tuân thủ những quy định nào về bảo mật thông tin?
- Đáp: Bạn cần tuân thủ Luật Đường bộ, Luật Công nghệ thông tin, Luật An toàn thông tin mạng, Luật An ninh mạng, Luật Giao dịch điện tử, quy định Khung kiến trúc tổng thể quốc gia số, quy định Khung kiến trúc Chính phủ điện tử, quy định quản lý, kết nối và chia sẻ dữ liệu số của cơ quan nhà nước, quy định bảo đảm, bảo vệ đời sống riêng tư, bí mật cá nhân và các quy định pháp luật khác có liên quan. (Điều 58 Khoản 4 Nghị định 165/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “cơ sở dữ liệu đường bộ …”
- Hỏi (2026-07-01): Theo Nghị định 165/2024/NĐ-CP, khi xây dựng cơ sở dữ liệu đường bộ, tôi cần tuân thủ những quy định nào về bảo mật thông tin?
- Đáp: Bạn cần tuân thủ Luật Đường bộ, Luật Công nghệ thông tin, Luật An ninh mạng, Luật Giao dịch điện tử, quy định Khung kiến trúc tổng thể quốc gia số, quy định Khung kiến trúc chính phủ số Việt Nam, quy định quản lý, kết nối và chia sẻ dữ liệu số của cơ quan nhà nước, quy định bảo đảm, bảo vệ đời sống riêng tư, bí mật cá nhân và các quy định khác của pháp luật có liên quan. (Điều 58 Khoản 4 Nghị định 165/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “cơ sở dữ liệu đường bộ …”

```json
{"qid": "tD-theo_thoi_diem-009a", "question": "Theo Nghị định 165/2024/NĐ-CP, khi xây dựng cơ sở dữ liệu đường bộ, tôi cần tuân thủ những quy định nào về bảo mật thông tin?", "as_of": "2026-06-30", "question_type": "theo_thoi_diem", "tier": "B", "answer": "Bạn cần tuân thủ Luật Đường bộ, Luật Công nghệ thông tin, Luật An toàn thông tin mạng, Luật An ninh mạng, Luật Giao dịch điện tử, quy định Khung kiến trúc tổng thể quốc gia số, quy định Khung kiến trúc Chính phủ điện tử, quy định quản lý, kết nối và chia sẻ dữ liệu số của cơ quan nhà nước, quy định bảo đảm, bảo vệ đời sống riêng tư, bí mật cá nhân và các quy định pháp luật khác có liên quan. (Điều 58 Khoản 4 Nghị định 165/2024/NĐ-CP)", "gold_units": ["ND165-2024/D58/K4"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-009:1a", "pair_id": "pD-009"}
{"qid": "tD-theo_thoi_diem-009b", "question": "Theo Nghị định 165/2024/NĐ-CP, khi xây dựng cơ sở dữ liệu đường bộ, tôi cần tuân thủ những quy định nào về bảo mật thông tin?", "as_of": "2026-07-01", "question_type": "theo_thoi_diem", "tier": "B", "answer": "Bạn cần tuân thủ Luật Đường bộ, Luật Công nghệ thông tin, Luật An ninh mạng, Luật Giao dịch điện tử, quy định Khung kiến trúc tổng thể quốc gia số, quy định Khung kiến trúc chính phủ số Việt Nam, quy định quản lý, kết nối và chia sẻ dữ liệu số của cơ quan nhà nước, quy định bảo đảm, bảo vệ đời sống riêng tư, bí mật cá nhân và các quy định khác của pháp luật có liên quan. (Điều 58 Khoản 4 Nghị định 165/2024/NĐ-CP)", "gold_units": ["ND165-2024/D58/K4"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-009:1b", "pair_id": "pD-009"}
```

**Nháp 2**

- Hỏi (2026-06-30): Theo Nghị định 165/2024/NĐ-CP, khi xây dựng cơ sở dữ liệu đường bộ, tôi cần tuân thủ những quy định nào về bảo mật thông tin?
- Đáp: Bạn cần tuân thủ Luật Đường bộ, Luật Công nghệ thông tin, Luật An toàn thông tin mạng, Luật An ninh mạng, Luật Giao dịch điện tử, quy định Khung kiến trúc tổng thể quốc gia số, quy định Khung kiến trúc Chính phủ điện tử, quy định quản lý, kết nối và chia sẻ dữ liệu số của cơ quan nhà nước, quy định bảo đảm, bảo vệ đời sống riêng tư, bí mật cá nhân và các quy định pháp luật khác có liên quan. (Điều 58 Khoản 4 Nghị định 165/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “cơ sở dữ liệu đường bộ …”
- Hỏi (2026-07-01): Theo Nghị định 165/2024/NĐ-CP, khi xây dựng cơ sở dữ liệu đường bộ, tôi cần tuân thủ những quy định nào về bảo mật thông tin?
- Đáp: Bạn cần tuân thủ Luật Đường bộ, Luật Công nghệ thông tin, Luật An ninh mạng, Luật Giao dịch điện tử, quy định Khung kiến trúc tổng thể quốc gia số, quy định Khung kiến trúc chính phủ số Việt Nam, quy định quản lý, kết nối và chia sẻ dữ liệu số của cơ quan nhà nước, quy định bảo đảm, bảo vệ đời sống riêng tư, bí mật cá nhân và các quy định khác của pháp luật có liên quan. (Điều 58 Khoản 4 Nghị định 165/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “cơ sở dữ liệu đường bộ …”

```json
{"qid": "tD-theo_thoi_diem-009a", "question": "Theo Nghị định 165/2024/NĐ-CP, khi xây dựng cơ sở dữ liệu đường bộ, tôi cần tuân thủ những quy định nào về bảo mật thông tin?", "as_of": "2026-06-30", "question_type": "theo_thoi_diem", "tier": "B", "answer": "Bạn cần tuân thủ Luật Đường bộ, Luật Công nghệ thông tin, Luật An toàn thông tin mạng, Luật An ninh mạng, Luật Giao dịch điện tử, quy định Khung kiến trúc tổng thể quốc gia số, quy định Khung kiến trúc Chính phủ điện tử, quy định quản lý, kết nối và chia sẻ dữ liệu số của cơ quan nhà nước, quy định bảo đảm, bảo vệ đời sống riêng tư, bí mật cá nhân và các quy định pháp luật khác có liên quan. (Điều 58 Khoản 4 Nghị định 165/2024/NĐ-CP)", "gold_units": ["ND165-2024/D58/K4"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-009:2a", "pair_id": "pD-009"}
{"qid": "tD-theo_thoi_diem-009b", "question": "Theo Nghị định 165/2024/NĐ-CP, khi xây dựng cơ sở dữ liệu đường bộ, tôi cần tuân thủ những quy định nào về bảo mật thông tin?", "as_of": "2026-07-01", "question_type": "theo_thoi_diem", "tier": "B", "answer": "Bạn cần tuân thủ Luật Đường bộ, Luật Công nghệ thông tin, Luật An ninh mạng, Luật Giao dịch điện tử, quy định Khung kiến trúc tổng thể quốc gia số, quy định Khung kiến trúc chính phủ số Việt Nam, quy định quản lý, kết nối và chia sẻ dữ liệu số của cơ quan nhà nước, quy định bảo đảm, bảo vệ đời sống riêng tư, bí mật cá nhân và các quy định khác của pháp luật có liên quan. (Điều 58 Khoản 4 Nghị định 165/2024/NĐ-CP)", "gold_units": ["ND165-2024/D58/K4"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-009:2b", "pair_id": "pD-009"}
```

### WD-theo_thoi_diem-010 · tier B · vai: người mới học lái ô tô · kiểu: neu_van_ban

<details><summary>Nguồn và con số</summary>

```text
### Trạng thái trước mốc (áp dụng tại 2026-06-30)
Văn bản: Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ)
Hiệu lực của trạng thái này: 2025-01-01 → 2026-06-30
Mã điều khoản dùng được cho gold_units: ND165-2024/D60/K4

Điều 60. Thu thập, cập nhật, điều chỉnh thông tin trong cơ sở dữ liệu đường bộ
4. Thông tin quy định tại khoản 4 Điều 57 của Nghị định này được trích, chọn và đồng bộ hóa từ cơ sở dữ liệu, cơ sở dữ liệu chuyên ngành của Bộ Giao thông vận tải, Bộ Công an, Bộ Quốc phòng, nhà cung cấp dịch vụ thanh toán điện tử giao thông đường bộ và các địa phương.

### Điều khoản được nguồn trên dẫn chiếu tới (ND165-2024/D57/K4)
Mã điều khoản dùng được cho gold_units: ND165-2024/D57/K4

Điều 57. Thông tin trong cơ sở dữ liệu đường bộ
4. Cơ sở dữ liệu thanh toán điện tử giao thông đường bộ bao gồm các thông tin theo quy định tại Phụ lục ban hành kèm theo Nghị định số 119/2024/NĐ-CP ngày 30 tháng 9 năm 2024 của Chính phủ quy định về thanh toán điện tử giao thông đường bộ.

### Trạng thái sau mốc (áp dụng tại 2026-07-01)
Văn bản: Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ)
Hiệu lực của trạng thái này: 2026-07-01 → nay
Mã điều khoản dùng được cho gold_units: ND165-2024/D60/K4

Điều 60. Thu thập, cập nhật, điều chỉnh thông tin trong cơ sở dữ liệu đường bộ
4. Thông tin quy định tại khoản 4 Điều 57 của Nghị định này được trích, chọn và đồng bộ hóa từ cơ sở dữ liệu, cơ sở dữ liệu chuyên ngành của Bộ Xây dựng, Bộ Công an, Bộ Quốc phòng, nhà cung cấp dịch vụ thanh toán điện tử giao thông đường bộ và các địa phương.

### Điều khoản được nguồn trên dẫn chiếu tới (ND165-2024/D57/K4)
Mã điều khoản dùng được cho gold_units: ND165-2024/D57/K4

Điều 57. Thông tin trong cơ sở dữ liệu đường bộ
4. Cơ sở dữ liệu thanh toán điện tử giao thông đường bộ bao gồm các thông tin theo quy định tại Phụ lục ban hành kèm theo Nghị định số 119/2024/NĐ-CP ngày 30 tháng 9 năm 2024 của Chính phủ quy định về thanh toán điện tử giao thông đường bộ.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-06-30): Tôi muốn biết thông tin trong cơ sở dữ liệu thanh toán điện tử giao thông đường bộ được lấy từ đâu?
- Đáp: Thông tin được trích, chọn và đồng bộ hóa từ cơ sở dữ liệu, cơ sở dữ liệu chuyên ngành của Bộ Giao thông vận tải, Bộ Công an, Bộ Quốc phòng, nhà cung cấp dịch vụ thanh toán điện tử giao thông đường bộ và các địa phương.
- ⚠ chep_nguyen_van: “cơ sở dữ liệu thanh toán …”
- Hỏi (2026-07-01): Tôi muốn biết thông tin trong cơ sở dữ liệu thanh toán điện tử giao thông đường bộ được lấy từ đâu?
- Đáp: Thông tin được trích, chọn và đồng bộ hóa từ cơ sở dữ liệu, cơ sở dữ liệu chuyên ngành của Bộ Xây dựng, Bộ Công an, Bộ Quốc phòng, nhà cung cấp dịch vụ thanh toán điện tử giao thông đường bộ và các địa phương.
- ⚠ chep_nguyen_van: “cơ sở dữ liệu thanh toán …”

```json
{"qid": "tD-theo_thoi_diem-010a", "question": "Tôi muốn biết thông tin trong cơ sở dữ liệu thanh toán điện tử giao thông đường bộ được lấy từ đâu?", "as_of": "2026-06-30", "question_type": "theo_thoi_diem", "tier": "B", "answer": "Thông tin được trích, chọn và đồng bộ hóa từ cơ sở dữ liệu, cơ sở dữ liệu chuyên ngành của Bộ Giao thông vận tải, Bộ Công an, Bộ Quốc phòng, nhà cung cấp dịch vụ thanh toán điện tử giao thông đường bộ và các địa phương.", "gold_units": ["ND165-2024/D60/K4"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-010:1a", "pair_id": "pD-010"}
{"qid": "tD-theo_thoi_diem-010b", "question": "Tôi muốn biết thông tin trong cơ sở dữ liệu thanh toán điện tử giao thông đường bộ được lấy từ đâu?", "as_of": "2026-07-01", "question_type": "theo_thoi_diem", "tier": "B", "answer": "Thông tin được trích, chọn và đồng bộ hóa từ cơ sở dữ liệu, cơ sở dữ liệu chuyên ngành của Bộ Xây dựng, Bộ Công an, Bộ Quốc phòng, nhà cung cấp dịch vụ thanh toán điện tử giao thông đường bộ và các địa phương.", "gold_units": ["ND165-2024/D60/K4"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-010:1b", "pair_id": "pD-010"}
```

### WD-theo_thoi_diem-011 · tier B · vai: tài xế xe tải · kiểu: tinh_huong_nguoi_khac

<details><summary>Nguồn và con số</summary>

```text
### Trạng thái trước mốc (áp dụng tại 2026-06-30)
Văn bản: Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ)
Hiệu lực của trạng thái này: 2025-01-01 → 2026-06-30
Mã điều khoản dùng được cho gold_units: ND165-2024/D8/K10

Điều 8. Đặt tên, đổi tên, số hiệu đường bộ
10. Không bắt buộc đặt, đổi tên, số hiệu đường bộ đối với trường hợp quy định tại khoản 3 Điều 11 Luật Đường bộ và các tuyến đường bộ có yêu cầu đặc biệt về bảo đảm quốc phòng, an ninh.

### Điều khoản được nguồn trên dẫn chiếu tới (LUAT35-2024/D11/K3)
Mã điều khoản dùng được cho gold_units: LUAT35-2024/D11/K3

Điều 11. Đặt tên, đổi tên, số hiệu đường bộ
3. Không bắt buộc đặt tên, số hiệu đường bộ đối với đường xã, đường thôn, đường nội bộ, đường chuyên dùng; không bắt buộc đổi tên, số hiệu đường bộ trong trường hợp đường đó đi qua địa bàn được cấp có thẩm quyền quyết định giải thể, nhập, chia, điều chỉnh địa giới hành chính của địa phương.

### Trạng thái sau mốc (áp dụng tại 2026-07-01)
Văn bản: Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ)
Hiệu lực của trạng thái này: 2026-07-01 → nay
Mã điều khoản dùng được cho gold_units: ND165-2024/D8/K10

Điều 8. Đặt tên, đổi tên, số hiệu đường bộ
10. Không bắt buộc đặt, đổi tên, số hiệu đường bộ đối với các trường hợp quy định tại khoản 3 Điều 11 Luật Đường bộ và các tuyến đường bộ có yêu cầu đặc biệt về bảo đảm quốc phòng, an ninh; không bắt buộc đặt số hiệu đường bộ đối với tuyến đường bộ đã có tên, trừ trường hợp đường bộ tham gia vào mạng lưới đường bộ quốc tế và trường hợp điều chỉnh loại đường theo cấp quản lý.

### Điều khoản được nguồn trên dẫn chiếu tới (LUAT35-2024/D11/K3)
Mã điều khoản dùng được cho gold_units: LUAT35-2024/D11/K3

Điều 11. Đặt tên, đổi tên, số hiệu đường bộ
3. Không bắt buộc đặt tên, số hiệu đường bộ đối với đường xã, đường thôn, đường nội bộ, đường chuyên dùng; không bắt buộc đổi tên, số hiệu đường bộ trong trường hợp đường đó đi qua địa bàn được cấp có thẩm quyền quyết định giải thể, nhập, chia, điều chỉnh địa giới hành chính của địa phương.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-06-30): Anh tôi, một tài xế xe tải, lái xe qua một con đường mới được xây dựng, nhưng chưa có biển số hoặc tên đường. Anh ấy có thể tiếp tục lái xe mà không cần đặt tên hay số hiệu cho đường này không?
- Đáp: Không bắt buộc đặt tên, đổi tên, số hiệu đường bộ đối với đường xã, đường thôn, đường nội bộ, đường chuyên dùng; không bắt buộc đổi tên, số hiệu đường bộ trong trường hợp đường đó đi qua địa bàn được cấp có thẩm quyền quyết định giải thể, nhập, chia, điều chỉnh địa giới hành chính của địa phương. (Điều 11 Khoản 3 Luật Đường bộ)
- ⚠ dap_an_cap_giong_nhau
- Hỏi (2026-07-01): Anh tôi, một tài xế xe tải, lái xe qua một con đường mới được xây dựng, nhưng chưa có biển số hoặc tên đường. Anh ấy có thể tiếp tục lái xe mà không cần đặt tên hay số hiệu cho đường này không?
- Đáp: Không bắt buộc đặt tên, đổi tên, số hiệu đường bộ đối với đường xã, đường thôn, đường nội bộ, đường chuyên dùng; không bắt buộc đổi tên, số hiệu đường bộ trong trường hợp đường đó đi qua địa bàn được cấp có thẩm quyền quyết định giải thể, nhập, chia, điều chỉnh địa giới hành chính của địa phương. (Điều 11 Khoản 3 Luật Đường bộ)
- ⚠ dap_an_cap_giong_nhau
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-theo_thoi_diem-011a", "question": "Anh tôi, một tài xế xe tải, lái xe qua một con đường mới được xây dựng, nhưng chưa có biển số hoặc tên đường. Anh ấy có thể tiếp tục lái xe mà không cần đặt tên hay số hiệu cho đường này không?", "as_of": "2026-06-30", "question_type": "theo_thoi_diem", "tier": "B", "answer": "Không bắt buộc đặt tên, đổi tên, số hiệu đường bộ đối với đường xã, đường thôn, đường nội bộ, đường chuyên dùng; không bắt buộc đổi tên, số hiệu đường bộ trong trường hợp đường đó đi qua địa bàn được cấp có thẩm quyền quyết định giải thể, nhập, chia, điều chỉnh địa giới hành chính của địa phương. (Điều 11 Khoản 3 Luật Đường bộ)", "gold_units": ["ND165-2024/D8/K10", "LUAT35-2024/D11/K3"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-011:1a", "pair_id": "pD-011"}
{"qid": "tD-theo_thoi_diem-011b", "question": "Anh tôi, một tài xế xe tải, lái xe qua một con đường mới được xây dựng, nhưng chưa có biển số hoặc tên đường. Anh ấy có thể tiếp tục lái xe mà không cần đặt tên hay số hiệu cho đường này không?", "as_of": "2026-07-01", "question_type": "theo_thoi_diem", "tier": "B", "answer": "Không bắt buộc đặt tên, đổi tên, số hiệu đường bộ đối với đường xã, đường thôn, đường nội bộ, đường chuyên dùng; không bắt buộc đổi tên, số hiệu đường bộ trong trường hợp đường đó đi qua địa bàn được cấp có thẩm quyền quyết định giải thể, nhập, chia, điều chỉnh địa giới hành chính của địa phương. (Điều 11 Khoản 3 Luật Đường bộ)", "gold_units": ["ND165-2024/D8/K10", "LUAT35-2024/D11/K3"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-011:1b", "pair_id": "pD-011"}
```

**Nháp 2**

- Hỏi (2026-06-30): Công ty tôi, một doanh nghiệp vận tải, đang chuẩn bị mở rộng tuyến đường mới qua một khu vực chưa được cấp tên. Liệu công ty có cần phải đặt tên hoặc số hiệu cho tuyến đường này trước khi bắt đầu hoạt động?
- Đáp: Không bắt buộc đặt tên, đổi tên, số hiệu đường bộ đối với đường xã, đường thôn, đường nội bộ, đường chuyên dùng; không bắt buộc đổi tên, số hiệu đường bộ trong trường hợp đường đó đi qua địa bàn được cấp có thẩm quyền quyết định giải thể, nhập, chia, điều chỉnh địa giới hành chính của địa phương. (Điều 11 Khoản 3 Luật Đường bộ)
- ⚠ dap_an_cap_giong_nhau
- Hỏi (2026-07-01): Công ty tôi, một doanh nghiệp vận tải, đang chuẩn bị mở rộng tuyến đường mới qua một khu vực chưa được cấp tên. Liệu công ty có cần phải đặt tên hoặc số hiệu cho tuyến đường này trước khi bắt đầu hoạt động?
- Đáp: Không bắt buộc đặt tên, đổi tên, số hiệu đường bộ đối với đường xã, đường thôn, đường nội bộ, đường chuyên dùng; không bắt buộc đổi tên, số hiệu đường bộ trong trường hợp đường đó đi qua địa bàn được cấp có thẩm quyền quyết định giải thể, nhập, chia, điều chỉnh địa giới hành chính của địa phương. (Điều 11 Khoản 3 Luật Đường bộ)
- ⚠ dap_an_cap_giong_nhau
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-theo_thoi_diem-011a", "question": "Công ty tôi, một doanh nghiệp vận tải, đang chuẩn bị mở rộng tuyến đường mới qua một khu vực chưa được cấp tên. Liệu công ty có cần phải đặt tên hoặc số hiệu cho tuyến đường này trước khi bắt đầu hoạt động?", "as_of": "2026-06-30", "question_type": "theo_thoi_diem", "tier": "B", "answer": "Không bắt buộc đặt tên, đổi tên, số hiệu đường bộ đối với đường xã, đường thôn, đường nội bộ, đường chuyên dùng; không bắt buộc đổi tên, số hiệu đường bộ trong trường hợp đường đó đi qua địa bàn được cấp có thẩm quyền quyết định giải thể, nhập, chia, điều chỉnh địa giới hành chính của địa phương. (Điều 11 Khoản 3 Luật Đường bộ)", "gold_units": ["ND165-2024/D8/K10", "LUAT35-2024/D11/K3"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-011:2a", "pair_id": "pD-011"}
{"qid": "tD-theo_thoi_diem-011b", "question": "Công ty tôi, một doanh nghiệp vận tải, đang chuẩn bị mở rộng tuyến đường mới qua một khu vực chưa được cấp tên. Liệu công ty có cần phải đặt tên hoặc số hiệu cho tuyến đường này trước khi bắt đầu hoạt động?", "as_of": "2026-07-01", "question_type": "theo_thoi_diem", "tier": "B", "answer": "Không bắt buộc đặt tên, đổi tên, số hiệu đường bộ đối với đường xã, đường thôn, đường nội bộ, đường chuyên dùng; không bắt buộc đổi tên, số hiệu đường bộ trong trường hợp đường đó đi qua địa bàn được cấp có thẩm quyền quyết định giải thể, nhập, chia, điều chỉnh địa giới hành chính của địa phương. (Điều 11 Khoản 3 Luật Đường bộ)", "gold_units": ["ND165-2024/D8/K10", "LUAT35-2024/D11/K3"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-011:2b", "pair_id": "pD-011"}
```

### WD-theo_thoi_diem-012 · tier B · vai: chủ doanh nghiệp vận tải · kiểu: neu_van_ban · trước mốc: chưa có hiệu lực

<details><summary>Nguồn và con số</summary>

```text
### Trạng thái trước mốc (áp dụng tại 2026-06-30)
Chưa có hiệu lực (không có phiên bản).

### Trạng thái sau mốc (áp dụng tại 2026-07-01)
Văn bản: Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ)
Hiệu lực của trạng thái này: 2026-07-01 → nay
Mã điều khoản dùng được cho gold_units: ND165-2024/D5/K4, ND165-2024/D5/K4/a, ND165-2024/D5/K4/b

Điều 5. Giao Ủy ban nhân dân cấp tỉnh quản lý quốc lộ để đáp ứng nhu cầu phát triển kinh tế - xã hội, bảo đảm lợi ích quốc gia, quốc phòng, an ninh và khả năng bố trí nguồn lực của địa phương
4. Trách nhiệm của Bộ Xây dựng
a) Bàn giao tuyến, đoạn tuyến quốc lộ và công trình kết cấu hạ tầng thuộc phạm vi dự án để Ủy ban nhân dân cấp tỉnh quản lý sau khi có Quyết định giao Ủy ban nhân dân cấp tỉnh quản lý tuyến, đoạn tuyến quốc lộ;
b) Thực hiện các quy định tại các điểm b khoản 4 Điều 4 Nghị định này đối với quốc lộ giao Ủy ban nhân dân cấp tỉnh quản lý.

### Điều khoản được nguồn trên dẫn chiếu tới (ND165-2024/D4/K4/b)
Mã điều khoản dùng được cho gold_units: ND165-2024/D4/K4/b

Điều 4. Phân cấp quản lý quốc lộ
4. Bộ Xây dựng có trách nhiệm:
b) Kiểm tra, hướng dẫn Ủy ban nhân dân cấp tỉnh thực hiện đầu tư, xây dựng, quản lý, vận hành, khai thác, bảo trì và công tác bảo đảm an toàn giao thông quốc lộ được phân cấp quản lý;

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-06-30): Là chủ doanh nghiệp vận tải, tôi muốn biết trách nhiệm của Bộ Xây dựng khi giao tuyến quốc lộ cho Ủy ban nhân dân cấp tỉnh, theo quy định hiện hành?
- Đáp: Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu.
- ⚠ chep_nguyen_van: “trách nhiệm của bộ xây dựng …”
- Hỏi (2026-07-01): Là chủ doanh nghiệp vận tải, tôi muốn biết trách nhiệm của Bộ Xây dựng khi giao tuyến quốc lộ cho Ủy ban nhân dân cấp tỉnh, theo quy định hiện hành?
- Đáp: Bộ Xây dựng phải kiểm tra, hướng dẫn Ủy ban nhân dân cấp tỉnh thực hiện đầu tư, xây dựng, quản lý, vận hành, khai thác, bảo trì và công tác bảo đảm an toàn giao thông quốc lộ được phân cấp quản lý. (ND165-2024/D5/K4/b)
- ⚠ chep_nguyen_van: “trách nhiệm của bộ xây dựng …”

```json
{"qid": "tD-theo_thoi_diem-012a", "question": "Là chủ doanh nghiệp vận tải, tôi muốn biết trách nhiệm của Bộ Xây dựng khi giao tuyến quốc lộ cho Ủy ban nhân dân cấp tỉnh, theo quy định hiện hành?", "as_of": "2026-06-30", "question_type": "theo_thoi_diem", "tier": "B", "answer": "Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu.", "gold_units": [], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-012:1a", "pair_id": "pD-012"}
{"qid": "tD-theo_thoi_diem-012b", "question": "Là chủ doanh nghiệp vận tải, tôi muốn biết trách nhiệm của Bộ Xây dựng khi giao tuyến quốc lộ cho Ủy ban nhân dân cấp tỉnh, theo quy định hiện hành?", "as_of": "2026-07-01", "question_type": "theo_thoi_diem", "tier": "B", "answer": "Bộ Xây dựng phải kiểm tra, hướng dẫn Ủy ban nhân dân cấp tỉnh thực hiện đầu tư, xây dựng, quản lý, vận hành, khai thác, bảo trì và công tác bảo đảm an toàn giao thông quốc lộ được phân cấp quản lý. (ND165-2024/D5/K4/b)", "gold_units": ["ND165-2024/D5/K4/b"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-012:1b", "pair_id": "pD-012"}
```

### WD-theo_thoi_diem-013 · tier B · vai: sinh viên đi xe máy · kiểu: tinh_huong_nguoi_khac

<details><summary>Nguồn và con số</summary>

```text
### Trạng thái trước mốc (áp dụng tại 2026-06-30)
Văn bản: Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ)
Hiệu lực của trạng thái này: 2025-01-01 → 2026-06-30
Mã điều khoản dùng được cho gold_units: ND165-2024/D47/K2, ND165-2024/D47/K2/a, ND165-2024/D47/K2/b, ND165-2024/D47/K2/c, ND165-2024/D47/K2/d, ND165-2024/D47/K2/đ

Điều 47. Mở rộng, nâng cấp đường cao tốc hoặc đường bộ đang khai thác nâng cấp thành đường cao tốc trong trường hợp nhà đầu tư hiện hữu đề xuất điều chỉnh dự án
2. Căn cứ quyết định phê duyệt dự án điều chỉnh, thiết kế xây dựng sau thiết kế cơ sở, dự toán, cơ quan có thẩm quyền tổ chức lựa chọn nhà đầu tư theo quy định tại điểm b khoản 1 Điều 39 Luật Đầu tư theo phương thức đối tác công tư, trong đó xác định:
a) Yêu cầu về năng lực, kinh nghiệm, tư cách hợp lệ đối với nhà đầu tư hiện hữu để thực hiện việc mở rộng, nâng cấp đường cao tốc theo quy định tại điểm c khoản 1 Điều 67 Nghị định số 35/2021/NĐ-CP ngày 29 tháng 3 năm 2021 của Chính phủ quy định chi tiết và hướng dẫn thi hành Luật Đầu tư theo phương thức đối tác công tư (Nghị định số 35/2021/NĐ-CP);
b) Dự thảo phụ lục hợp đồng để thực hiện việc mở rộng, nâng cấp đường cao tốc được xây dựng theo quy định tại Điều 47 Luật Đầu tư theo phương thức đối tác công tư và hướng dẫn lập hợp đồng mẫu dự án PPP tại Phụ lục VI kèm theo Nghị định số 35/2021/NĐ-CP căn cứ phạm vi công trình mở rộng, nâng cấp;
c) Phương án tài chính cập nhật khi bổ sung công trình mở rộng, nâng cấp được thực hiện theo quy định pháp luật đầu tư theo phương thức đối tác công tư;
d) Quy trình thực hiện lựa chọn nhà đầu tư thực hiện theo quy định tại khoản 2 Điều 37 Nghị định số 35/2021/NĐ-CP;
đ) Hồ sơ theo yêu cầu tại khoản này được cơ quan có thẩm quyền phê duyệt và gửi đến nhà đầu tư hiện hữu.

### Trạng thái sau mốc (áp dụng tại 2026-07-01)
Văn bản: Nghị định số 165/2024/NĐ-CP (Quy định chi tiết, hướng dẫn thi hành một số điều của Luật Đường bộ và Điều 77 Luật Trật tự, an toàn giao thông đường bộ)
Hiệu lực của trạng thái này: 2026-07-01 → nay
Mã điều khoản dùng được cho gold_units: ND165-2024/D47/K2

Điều 47. Mở rộng, nâng cấp đường cao tốc hoặc đường bộ đang khai thác nâng cấp thành đường cao tốc trong trường hợp nhà đầu tư hiện hữu đề xuất điều chỉnh dự án
2. Báo cáo thẩm định nội dung điều chỉnh báo cáo nghiên cứu khả thi gồm nội dung đánh giá về năng lực tài chính của nhà đầu tư, bao gồm khả năng thu xếp vốn chủ sở hữu, khả năng huy động vốn vay, nguồn vốn hợp pháp khác để thực hiện phần mở rộng, nâng cấp. Nhà đầu tư chịu mọi chi phí, rủi ro trong trường hợp hồ sơ điều chỉnh dự án không được cơ quan có thẩm quyền phê duyệt.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-06-30): Anh tôi đang xem xét mở rộng đường cao tốc, anh ấy muốn biết khi nào cần nộp báo cáo thẩm định nội dung điều chỉnh?
- Đáp: Không có quy định yêu cầu nộp báo cáo thẩm định nội dung điều chỉnh tại thời điểm này.
- ⚠ gold_mac_dinh; chep_nguyen_van: “báo cáo thẩm định nội dung …”
- Hỏi (2026-07-01): Anh tôi đang xem xét mở rộng đường cao tốc, anh ấy muốn biết khi nào cần nộp báo cáo thẩm định nội dung điều chỉnh?
- Đáp: Khi dự án điều chỉnh được phê duyệt, anh ấy phải nộp báo cáo thẩm định nội dung điều chỉnh, bao gồm đánh giá năng lực tài chính của nhà đầu tư. (Điều 47, Nghị định 165/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “báo cáo thẩm định nội dung …”
- Ghi chú: Giả định anh tôi là người đầu tư hiện hữu đề xuất điều chỉnh dự án mở rộng đường cao tốc.

```json
{"qid": "tD-theo_thoi_diem-013a", "question": "Anh tôi đang xem xét mở rộng đường cao tốc, anh ấy muốn biết khi nào cần nộp báo cáo thẩm định nội dung điều chỉnh?", "as_of": "2026-06-30", "question_type": "theo_thoi_diem", "tier": "B", "answer": "Không có quy định yêu cầu nộp báo cáo thẩm định nội dung điều chỉnh tại thời điểm này.", "gold_units": ["ND165-2024/D47/K2"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-013:1a", "pair_id": "pD-013"}
{"qid": "tD-theo_thoi_diem-013b", "question": "Anh tôi đang xem xét mở rộng đường cao tốc, anh ấy muốn biết khi nào cần nộp báo cáo thẩm định nội dung điều chỉnh?", "as_of": "2026-07-01", "question_type": "theo_thoi_diem", "tier": "B", "answer": "Khi dự án điều chỉnh được phê duyệt, anh ấy phải nộp báo cáo thẩm định nội dung điều chỉnh, bao gồm đánh giá năng lực tài chính của nhà đầu tư. (Điều 47, Nghị định 165/2024/NĐ-CP)", "gold_units": ["ND165-2024/D47/K2"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-013:1b", "pair_id": "pD-013"}
```

### WD-theo_thoi_diem-014 · tier A · vai: cán bộ phường · kiểu: tinh_huong_ban_than

<details><summary>Nguồn và con số</summary>

```text
### Trạng thái trước mốc (áp dụng tại 2026-08-14)
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → 2026-08-14
Mã điều khoản dùng được cho gold_units: ND168-2024/D41/K2, ND168-2024/D41/K2/a, ND168-2024/D41/K2/b, ND168-2024/D41/K2/c, ND168-2024/D41/K2/d

Điều 41. Phân định thẩm quyền xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ
2. Cảnh sát giao thông trong phạm vi chức năng, nhiệm vụ được giao có thẩm quyền xử phạt đối với các hành vi vi phạm quy định tại các điểm, khoản, điều của Nghị định này như sau:
a) Điều 6, Điều 7, Điều 8, Điều 9, Điều 10, Điều 11, Điều 12, Điều 13, Điều 14, Điều 15, Điều 16, Điều 17, Điều 18, Điều 19, Điều 20, Điều 21, Điều 22, Điều 23, Điều 24, Điều 25, Điều 26, Điều 27, Điều 28, Điều 29, Điều 30, Điều 31, Điều 32, Điều 33, Điều 34, Điều 35, Điều 36;
b) Khoản 1, điểm a khoản 3, điểm b khoản 4, khoản 5 Điều 37;
c) Điều 38;
d) Điểm a, điểm b, điểm c, điểm d, điểm e khoản 1; điểm a khoản 2; điểm a, điểm b, điểm c khoản 3; điểm d khoản 4; khoản 8 Điều 39.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D10)
Mã điều khoản dùng được cho gold_units: ND168-2024/D10

Điều 10. Xử phạt người đi bộ vi phạm quy tắc giao thông đường bộ

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D11)
Mã điều khoản dùng được cho gold_units: ND168-2024/D11

Điều 11. Xử phạt người điều khiển, dẫn dắt vật nuôi, điều khiển xe vật nuôi kéo vi phạm quy tắc giao thông đường bộ

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D12)
Mã điều khoản dùng được cho gold_units: ND168-2024/D12

Điều 12. Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm khác về quy tắc giao thông đường bộ; sử dụng lòng đường, vỉa hè vào mục đích khác

### Trạng thái sau mốc (áp dụng tại 2026-08-15)
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2026-08-15 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D41/K2, ND168-2024/D41/K2/a, ND168-2024/D41/K2/b, ND168-2024/D41/K2/c, ND168-2024/D41/K2/d

Điều 41. Phân định thẩm quyền xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ
2. Cảnh sát giao thông trong phạm vi chức năng, nhiệm vụ được giao có thẩm quyền xử phạt đối với các hành vi vi phạm quy định tại các điểm, khoản, điều của Nghị định này như sau:
a) Điều 6, Điều 7, Điều 8, Điều 9, Điều 10, Điều 11, Điều 12, Điều 13, Điều 14, Điều 15, Điều 16, Điều 17, Điều 18, Điều 19, Điều 20, Điều 21, Điều 22, Điều 23, Điều 24, Điều 25, Điều 26, Điều 27, Điều 28, Điều 29, Điều 30, Điều 31, Điều 32, Điều 33, Điều 34, Điều 35, Điều 36;
b) Khoản 1, điểm a khoản 3, điểm b khoản 4, khoản 5 Điều 37;
c) Điều 38;
d) Điểm a, điểm b, điểm c, điểm d, điểm e khoản 1; điểm a khoản 2; điểm a, điểm b, điểm c, điểm g, điểm h, điểm i, điểm k khoản 3; điểm b, điểm d, điểm i, điểm k khoản 4; điểm đ, điểm e, điểm g, điểm h, điểm i, điểm k khoản 5; khoản 7; khoản 8 Điều 39.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D10)
Mã điều khoản dùng được cho gold_units: ND168-2024/D10

Điều 10. Xử phạt người đi bộ vi phạm quy tắc giao thông đường bộ

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D11)
Mã điều khoản dùng được cho gold_units: ND168-2024/D11

Điều 11. Xử phạt người điều khiển, dẫn dắt vật nuôi, điều khiển xe vật nuôi kéo vi phạm quy tắc giao thông đường bộ

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D12)
Mã điều khoản dùng được cho gold_units: ND168-2024/D12

Điều 12. Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm khác về quy tắc giao thông đường bộ; sử dụng lòng đường, vỉa hè vào mục đích khác

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-08-14): Tôi vừa đi bộ qua vỉa hè vào ban đêm, có bị xử phạt không?
- Đáp: Bạn sẽ bị xử phạt tiền từ 1.000.000 đồng đến 3.000.000 đồng. (Điều 10 Nghị định 168/2024/NĐ-CP)
- ⚠ dap_an_cap_giong_nhau; so_la: 1000000, 3000000
- Hỏi (2026-08-15): Tôi vừa đi bộ qua vỉa hè vào ban đêm, có bị xử phạt không?
- Đáp: Bạn sẽ bị xử phạt tiền từ 1.000.000 đồng đến 3.000.000 đồng. (Điều 10 Nghị định 168/2024/NĐ-CP)
- ⚠ dap_an_cap_giong_nhau; so_la: 1000000, 3000000
- Ghi chú: Không có sự thay đổi trong quy định giữa hai ngày.

```json
{"qid": "tD-theo_thoi_diem-014a", "question": "Tôi vừa đi bộ qua vỉa hè vào ban đêm, có bị xử phạt không?", "as_of": "2026-08-14", "question_type": "theo_thoi_diem", "tier": "A", "answer": "Bạn sẽ bị xử phạt tiền từ 1.000.000 đồng đến 3.000.000 đồng. (Điều 10 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D10"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-014:1a", "pair_id": "pD-014"}
{"qid": "tD-theo_thoi_diem-014b", "question": "Tôi vừa đi bộ qua vỉa hè vào ban đêm, có bị xử phạt không?", "as_of": "2026-08-15", "question_type": "theo_thoi_diem", "tier": "A", "answer": "Bạn sẽ bị xử phạt tiền từ 1.000.000 đồng đến 3.000.000 đồng. (Điều 10 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D10"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-014:1b", "pair_id": "pD-014"}
```

### WD-theo_thoi_diem-015 · tier A · vai: người lớn tuổi đi xe đạp điện · kiểu: tinh_huong_nguoi_khac

<details><summary>Nguồn và con số</summary>

```text
### Trạng thái trước mốc (áp dụng tại 2026-08-14)
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → 2026-08-14
Mã điều khoản dùng được cho gold_units: ND168-2024/D44/K3, ND168-2024/D44/K3/a, ND168-2024/D44/K3/b, ND168-2024/D44/K3/c, ND168-2024/D44/K3/d, ND168-2024/D44/K3/đ

Điều 44. Thẩm quyền xử phạt của Thanh tra chuyên ngành
3. Chánh Thanh tra tỉnh, thành phố trực thuộc trung ương (trong trường hợp không thành lập Thanh tra Sở Giao thông vận tải) có quyền:
a) Phạt cảnh cáo;
b) Phạt tiền đến 52.500.000 đồng;
c) Tước quyền sử dụng giấy phép, chứng chỉ hành nghề có thời hạn hoặc đình chỉ hoạt động có thời hạn;
d) Tịch thu tang vật, phương tiện được sử dụng để vi phạm hành chính có giá trị không vượt quá 105.000.000 đồng;
đ) Áp dụng các biện pháp khắc phục hậu quả quy định tại khoản 3 Điều 3 của Nghị định này.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D3/K3)
Mã điều khoản dùng được cho gold_units: ND168-2024/D3/K3

Điều 3. Hình thức xử phạt vi phạm hành chính, biện pháp khắc phục hậu quả; thu hồi giấy phép, chứng chỉ hành nghề
3. Các biện pháp khắc phục hậu quả vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ bao gồm:

### Trạng thái sau mốc (áp dụng tại 2026-08-15)
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2026-08-15 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D44/K3, ND168-2024/D44/K3/a, ND168-2024/D44/K3/b, ND168-2024/D44/K3/c, ND168-2024/D44/K3/d

Điều 44. Thẩm quyền xử phạt của Thanh tra chuyên ngành
3. Cục trưởng Cục Đường bộ Việt Nam, Trưởng đoàn kiểm tra do Bộ trưởng Bộ Xây dựng thành lập có quyền:
a) Phạt cảnh cáo;
b) Phạt tiền đến 75.000.000 đồng;
c) Tước quyền sử dụng giấy phép có thời hạn hoặc đình chỉ hoạt động có thời hạn;
d) Áp dụng các biện pháp khắc phục hậu quả quy định tại khoản 3 Điều 3 Nghị định này.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D3/K3)
Mã điều khoản dùng được cho gold_units: ND168-2024/D3/K3

Điều 3. Hình thức xử phạt vi phạm hành chính, biện pháp khắc phục hậu quả; thu hồi giấy phép, chứng chỉ hành nghề
3. Các biện pháp khắc phục hậu quả vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ bao gồm:

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-08-14): Anh tôi đang đi xe đạp điện, nếu vi phạm giao thông, mức phạt tiền tối đa là bao nhiêu?
- Đáp: Mức phạt tiền tối đa là 52.500.000 đồng. (Điều 44, Khoản 3 Nghị định 168/2024/NĐ-CP)
- ⚠ chi_so_so_sai (0)
- Hỏi (2026-08-15): Anh tôi đang đi xe đạp điện, nếu vi phạm giao thông, mức phạt tiền tối đa là bao nhiêu?
- Đáp: Mức phạt tiền tối đa là 75.000.000 đồng. (Điều 44, Khoản 3 Nghị định 168/2024/NĐ-CP)
- ⚠ chi_so_so_sai (0)
- Ghi chú: Giả định xe đạp điện được tính là phương tiện giao thông

```json
{"qid": "tD-theo_thoi_diem-015a", "question": "Anh tôi đang đi xe đạp điện, nếu vi phạm giao thông, mức phạt tiền tối đa là bao nhiêu?", "as_of": "2026-08-14", "question_type": "theo_thoi_diem", "tier": "A", "answer": "Mức phạt tiền tối đa là 52.500.000 đồng. (Điều 44, Khoản 3 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D44/K3"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-015:1a", "pair_id": "pD-015"}
{"qid": "tD-theo_thoi_diem-015b", "question": "Anh tôi đang đi xe đạp điện, nếu vi phạm giao thông, mức phạt tiền tối đa là bao nhiêu?", "as_of": "2026-08-15", "question_type": "theo_thoi_diem", "tier": "A", "answer": "Mức phạt tiền tối đa là 75.000.000 đồng. (Điều 44, Khoản 3 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D44/K3"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-015:1b", "pair_id": "pD-015"}
```

### WD-theo_thoi_diem-016 · tier A · vai: tài xế xe tải · kiểu: tinh_huong_ban_than · trước mốc: chưa có hiệu lực

<details><summary>Nguồn và con số</summary>

```text
### Trạng thái trước mốc (áp dụng tại 2026-08-14)
Chưa có hiệu lực (không có phiên bản).

### Trạng thái sau mốc (áp dụng tại 2026-08-15)
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2026-08-15 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D53/K4

Điều 53. Hiệu lực thi hành
4. Quy định xử phạt vi phạm hành chính liên quan đến thiết bị ghi nhận hình ảnh khoang chở khách tại điểm n khoản 5 Điều 20; điểm k, điểm l khoản 7 Điều 26 của Nghị định này có hiệu lực thi hành từ ngày 01 tháng 01 năm 2029 và theo quy định của pháp luật về thiết bị ghi nhận hình ảnh khoang chở khách trên phương tiện giao thông đường bộ.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-08-14): Tôi là tài xế xe tải, có cần lắp thiết bị ghi hình khoang chở hàng không trước ngày 14 tháng 8 năm 2026?
- Đáp: Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu.
- ⚠ dap_an_cap_giong_nhau
- Hỏi (2026-08-15): Tôi là tài xế xe tải, có cần lắp thiết bị ghi hình khoang chở hàng không trước ngày 15 tháng 8 năm 2026?
- Đáp: Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu.
- ⚠ dap_an_cap_giong_nhau; gold_mac_dinh

```json
{"qid": "tD-theo_thoi_diem-016a", "question": "Tôi là tài xế xe tải, có cần lắp thiết bị ghi hình khoang chở hàng không trước ngày 14 tháng 8 năm 2026?", "as_of": "2026-08-14", "question_type": "theo_thoi_diem", "tier": "A", "answer": "Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu.", "gold_units": [], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-016:1a", "pair_id": "pD-016"}
{"qid": "tD-theo_thoi_diem-016b", "question": "Tôi là tài xế xe tải, có cần lắp thiết bị ghi hình khoang chở hàng không trước ngày 15 tháng 8 năm 2026?", "as_of": "2026-08-15", "question_type": "theo_thoi_diem", "tier": "A", "answer": "Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu.", "gold_units": ["ND168-2024/D53/K4"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-016:1b", "pair_id": "pD-016"}
```

**Nháp 2**

- Hỏi (2026-08-14): Tôi là tài xế xe tải, có phải lắp thiết bị ghi hình khoang chở hàng khi vận chuyển hàng hóa nguy hiểm trước ngày 14 tháng 8 năm 2026?
- Đáp: Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu.
- ⚠ dap_an_cap_giong_nhau
- Hỏi (2026-08-15): Tôi là tài xế xe tải, có phải lắp thiết bị ghi hình khoang chở hàng khi vận chuyển hàng hóa nguy hiểm trước ngày 15 tháng 8 năm 2026?
- Đáp: Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu.
- ⚠ dap_an_cap_giong_nhau; gold_mac_dinh

```json
{"qid": "tD-theo_thoi_diem-016a", "question": "Tôi là tài xế xe tải, có phải lắp thiết bị ghi hình khoang chở hàng khi vận chuyển hàng hóa nguy hiểm trước ngày 14 tháng 8 năm 2026?", "as_of": "2026-08-14", "question_type": "theo_thoi_diem", "tier": "A", "answer": "Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu.", "gold_units": [], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-016:2a", "pair_id": "pD-016"}
{"qid": "tD-theo_thoi_diem-016b", "question": "Tôi là tài xế xe tải, có phải lắp thiết bị ghi hình khoang chở hàng khi vận chuyển hàng hóa nguy hiểm trước ngày 15 tháng 8 năm 2026?", "as_of": "2026-08-15", "question_type": "theo_thoi_diem", "tier": "A", "answer": "Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu.", "gold_units": ["ND168-2024/D53/K4"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-016:2b", "pair_id": "pD-016"}
```

### WD-theo_thoi_diem-017 · tier A · vai: sinh viên đi xe máy · kiểu: tinh_huong_ban_than

<details><summary>Nguồn và con số</summary>

```text
### Trạng thái trước mốc (áp dụng tại 2026-08-14)
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → 2026-08-14
Mã điều khoản dùng được cho gold_units: ND168-2024/D41/K5, ND168-2024/D41/K5/a, ND168-2024/D41/K5/b

Điều 41. Phân định thẩm quyền xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ
5. Thanh tra đường bộ, người được giao thực hiện nhiệm vụ thanh tra chuyên ngành đường bộ trong phạm vi chức năng, nhiệm vụ được giao có thẩm quyền xử phạt tại các điểm, khoản, điều của Nghị định này như sau:
a) Khoản 1; điểm a, điểm b, điểm c, điểm d, điểm e khoản 2; khoản 3; khoản 4; khoản 5; điểm a khoản 6; điểm a, điểm d, điểm g, điểm h khoản 7; điểm a, điểm b khoản 8 Điều 26; điểm a khoản 2; điểm i, điểm l khoản 7; điểm b khoản 8; điểm a khoản 9; điểm c khoản 16; điểm a, điểm b khoản 17 Điều 32 khi thực hiện công tác thanh tra, kiểm tra tại đơn vị vận tải, bến xe, bãi đỗ xe, trạm dừng nghỉ, đơn vị thực hiện dịch vụ hỗ trợ vận tải;
b) Điều 39, Điều 40.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D26/K1)
Mã điều khoản dùng được cho gold_units: ND168-2024/D26/K1

Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
1. Phạt tiền từ 500.000 đồng đến 1.000.000 đồng đối với cá nhân, từ 1.000.000 đồng đến 2.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D26/K2/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D26/K2/a

Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
2. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với cá nhân, từ 2.000.000 đồng đến 4.000.000 đồng đối với tổ chức kinh doanh vận tải, dịch vụ hỗ trợ vận tải thực hiện một trong các hành vi vi phạm sau đây:
a) Không đánh số thứ tự ghế ngồi, giường nằm trên xe ô tô chở hành khách theo quy định;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D26/K2/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D26/K2/b

Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
2. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với cá nhân, từ 2.000.000 đồng đến 4.000.000 đồng đối với tổ chức kinh doanh vận tải, dịch vụ hỗ trợ vận tải thực hiện một trong các hành vi vi phạm sau đây:
b) Sử dụng xe ô tô kinh doanh vận tải hành khách theo tuyến cố định, xe ô tô kinh doanh vận tải hành khách bằng xe buýt không có chỗ ưu tiên cho người khuyết tật, người cao tuổi và phụ nữ mang thai theo quy định;

### Trạng thái sau mốc (áp dụng tại 2026-08-15)
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2026-08-15 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D41/K5, ND168-2024/D41/K5/a, ND168-2024/D41/K5/b

Điều 41. Phân định thẩm quyền xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ
5. Cục trưởng Cục Đường bộ Việt Nam, Trưởng đoàn kiểm tra do Bộ trưởng Bộ Xây dựng thành lập, Giám đốc Sở Xây dựng, Trưởng đoàn kiểm tra do Cục trưởng Cục Đường bộ Việt Nam thành lập, Giám đốc Khu Quản lý đường bộ thuộc Cục Đường bộ Việt Nam có thẩm quyền xử phạt tại các điểm, khoản, điều của Nghị định này như sau:
a) Khoản 1; điểm a, điểm b, điểm c, điểm d, điểm e khoản 2; khoản 3; khoản 4; khoản 5; điểm a khoản 6; điểm a, điểm d, điểm e, điểm g, điểm h, điểm i khoản 7; điểm a, điểm b, điểm d khoản 8 Điều 26; điểm a khoản 2; điểm i, điểm l khoản 7; điểm b khoản 8; điểm a, điểm d khoản 9; khoản 9a; điểm e khoản 11; điểm i khoản 14; điểm c khoản 16; điểm a, điểm b khoản 17 Điều 32 khi thực hiện công tác kiểm tra tại đơn vị vận tải, bến xe, bãi đỗ xe, trạm dừng nghỉ, đơn vị thực hiện dịch vụ hỗ trợ vận tải;
b) Khoản 1; khoản 2; điểm a, điểm b, điểm c, điểm d, điểm đ, điểm e khoản 3; điểm a, điểm b, điểm c, điểm d, điểm đ, điểm e, điểm g, điểm h khoản 4; điểm a, điểm b, điểm c, điểm d khoản 5; khoản 6 Điều 39; Điều 40.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D26/K1)
Mã điều khoản dùng được cho gold_units: ND168-2024/D26/K1

Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
1. Phạt tiền từ 500.000 đồng đến 1.000.000 đồng đối với cá nhân, từ 1.000.000 đồng đến 2.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D26/K2/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D26/K2/a

Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
2. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với cá nhân, từ 2.000.000 đồng đến 4.000.000 đồng đối với tổ chức kinh doanh vận tải, dịch vụ hỗ trợ vận tải thực hiện một trong các hành vi vi phạm sau đây:
a) Không đánh số thứ tự ghế ngồi, giường nằm trên xe ô tô chở hành khách theo quy định;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D26/K2/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D26/K2/b

Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
2. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với cá nhân, từ 2.000.000 đồng đến 4.000.000 đồng đối với tổ chức kinh doanh vận tải, dịch vụ hỗ trợ vận tải thực hiện một trong các hành vi vi phạm sau đây:
b) Sử dụng xe ô tô kinh doanh vận tải hành khách theo tuyến cố định, xe ô tô kinh doanh vận tải hành khách bằng xe buýt không có chỗ ưu tiên cho người khuyết tật, người cao tuổi và phụ nữ mang thai theo quy định;

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-08-14): Tôi lái xe ô tô chở khách, nhưng không đánh số ghế, có bị phạt tiền bao nhiêu?
- Đáp: Bạn sẽ bị phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với cá nhân khi không đánh số thứ tự ghế ngồi, giường nằm trên xe ô tô chở hành khách theo quy định.
- ⚠ so_cau_sai (1/2); chi_so_so_sai (0)
- Ghi chú: giả định là cá nhân

```json
{"qid": "tD-theo_thoi_diem-017a", "question": "Tôi lái xe ô tô chở khách, nhưng không đánh số ghế, có bị phạt tiền bao nhiêu?", "as_of": "2026-08-14", "question_type": "theo_thoi_diem", "tier": "A", "answer": "Bạn sẽ bị phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với cá nhân khi không đánh số thứ tự ghế ngồi, giường nằm trên xe ô tô chở hành khách theo quy định.", "gold_units": ["ND168-2024/D26/K2/a"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-017:1a", "pair_id": "pD-017"}
```

**Nháp 2**

- Hỏi (2026-08-14): Tôi lái xe ô tô chở khách, nhưng không có chỗ ưu tiên cho người khuyết tật, người cao tuổi và phụ nữ mang thai, có bị phạt tiền bao nhiêu?
- Đáp: Bạn sẽ bị phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với cá nhân khi sử dụng xe ô tô kinh doanh vận tải hành khách theo tuyến cố định, xe ô tô kinh doanh vận tải hành khách bằng xe buýt không có chỗ ưu tiên cho người khuyết tật, người cao tuổi và phụ nữ mang thai theo quy định.
- ⚠ so_cau_sai (1/2); chi_so_so_sai (0); chep_nguyen_van: “cao tuổi và phụ nữ mang …”
- Ghi chú: giả định là cá nhân

```json
{"qid": "tD-theo_thoi_diem-017a", "question": "Tôi lái xe ô tô chở khách, nhưng không có chỗ ưu tiên cho người khuyết tật, người cao tuổi và phụ nữ mang thai, có bị phạt tiền bao nhiêu?", "as_of": "2026-08-14", "question_type": "theo_thoi_diem", "tier": "A", "answer": "Bạn sẽ bị phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với cá nhân khi sử dụng xe ô tô kinh doanh vận tải hành khách theo tuyến cố định, xe ô tô kinh doanh vận tải hành khách bằng xe buýt không có chỗ ưu tiên cho người khuyết tật, người cao tuổi và phụ nữ mang thai theo quy định.", "gold_units": ["ND168-2024/D26/K2/b"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-017:2a", "pair_id": "pD-017"}
```

### WD-theo_thoi_diem-018 · tier A · vai: người mới học lái ô tô · kiểu: ngan · trước mốc: chưa có hiệu lực

<details><summary>Nguồn và con số</summary>

```text
### Trạng thái trước mốc (áp dụng tại 2026-08-14)
Chưa có hiệu lực (không có phiên bản).

### Trạng thái sau mốc (áp dụng tại 2026-08-15)
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2026-08-15 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D53/K3

Điều 53. Hiệu lực thi hành
3. Quy định xử phạt vi phạm hành chính liên quan đến thiết bị ghi nhận hình ảnh người lái xe đối với xe ô tô kinh doanh vận tải hành khách dưới 08 chỗ (không kể chỗ của người lái xe), xe ô tô kinh doanh vận tải hàng hóa (trừ xe ô tô đầu kéo), xe vận tải nội bộ tại điểm l khoản 5 Điều 20, điểm b khoản 3 Điều 21, điểm b khoản 9a Điều 32 của Nghị định này có hiệu lực thi hành từ ngày 01 tháng 01 năm 2028.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D20/K5/l)
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K5/l

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
5. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
l) Điều khiển xe ô tô chở người từ 08 chỗ trở lên (không kể chỗ của người lái xe) kinh doanh vận tải hành khách không lắp thiết bị ghi nhận hình ảnh người lái xe hoặc có lắp thiết bị ghi nhận hình ảnh người lái xe nhưng không có tác dụng trong quá trình xe tham gia giao thông theo quy định hoặc làm sai lệch dữ liệu của thiết bị ghi nhận hình ảnh người lái xe lắp trên xe ô tô;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D21/K3/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K3/b

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
3. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
b) Điều khiển xe ô tô đầu kéo không lắp thiết bị ghi nhận hình ảnh người lái xe hoặc có lắp thiết bị ghi nhận hình ảnh người lái xe nhưng không có tác dụng trong quá trình xe tham gia giao thông theo quy định hoặc làm sai lệch dữ liệu của thiết bị ghi nhận hình ảnh người lái xe lắp trên xe ô tô.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-08-14): Nếu tôi lái xe ô tô chở khách 8 chỗ trở lên mà không lắp thiết bị ghi hình người lái, tôi sẽ bị phạt tiền bao nhiêu?
- Đáp: Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu.
- Hỏi (2026-08-15): Nếu tôi lái xe ô tô chở khách 8 chỗ trở lên mà không lắp thiết bị ghi hình người lái, tôi sẽ bị phạt tiền bao nhiêu?
- Đáp: Bạn sẽ bị phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng. (Điều 20, Khoản 5, Điểm l Nghị định 168/2024/NĐ-CP)
- ⚠ chi_so_so_sai (0)

```json
{"qid": "tD-theo_thoi_diem-018a", "question": "Nếu tôi lái xe ô tô chở khách 8 chỗ trở lên mà không lắp thiết bị ghi hình người lái, tôi sẽ bị phạt tiền bao nhiêu?", "as_of": "2026-08-14", "question_type": "theo_thoi_diem", "tier": "A", "answer": "Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu.", "gold_units": [], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-018:1a", "pair_id": "pD-018"}
{"qid": "tD-theo_thoi_diem-018b", "question": "Nếu tôi lái xe ô tô chở khách 8 chỗ trở lên mà không lắp thiết bị ghi hình người lái, tôi sẽ bị phạt tiền bao nhiêu?", "as_of": "2026-08-15", "question_type": "theo_thoi_diem", "tier": "A", "answer": "Bạn sẽ bị phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng. (Điều 20, Khoản 5, Điểm l Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D20/K5/l"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-018:1b", "pair_id": "pD-018"}
```

**Nháp 2**

- Hỏi (2026-08-14): Nếu tôi lái xe ô tô tải không lắp thiết bị ghi hình người lái, tôi sẽ bị phạt tiền bao nhiêu?
- Đáp: Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu.
- Hỏi (2026-08-15): Nếu tôi lái xe ô tô tải không lắp thiết bị ghi hình người lái, tôi sẽ bị phạt tiền bao nhiêu?
- Đáp: Bạn sẽ bị phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng. (Điều 21, Khoản 3, Điểm b Nghị định 168/2024/NĐ-CP)
- ⚠ chi_so_so_sai (0)

```json
{"qid": "tD-theo_thoi_diem-018a", "question": "Nếu tôi lái xe ô tô tải không lắp thiết bị ghi hình người lái, tôi sẽ bị phạt tiền bao nhiêu?", "as_of": "2026-08-14", "question_type": "theo_thoi_diem", "tier": "A", "answer": "Chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu.", "gold_units": [], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-018:2a", "pair_id": "pD-018"}
{"qid": "tD-theo_thoi_diem-018b", "question": "Nếu tôi lái xe ô tô tải không lắp thiết bị ghi hình người lái, tôi sẽ bị phạt tiền bao nhiêu?", "as_of": "2026-08-15", "question_type": "theo_thoi_diem", "tier": "A", "answer": "Bạn sẽ bị phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng. (Điều 21, Khoản 3, Điểm b Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D21/K3/b"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-018:2b", "pair_id": "pD-018"}
```

### WD-theo_thoi_diem-019 · tier A · vai: tài xế xe tải · kiểu: tinh_huong_ban_than

<details><summary>Nguồn và con số</summary>

```text
### Trạng thái trước mốc (áp dụng tại 2026-08-14)
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → 2026-08-14
Mã điều khoản dùng được cho gold_units: ND168-2024/D41/K4, ND168-2024/D41/K4/a, ND168-2024/D41/K4/b, ND168-2024/D41/K4/c, ND168-2024/D41/K4/d, ND168-2024/D41/K4/đ, ND168-2024/D41/K4/e, ND168-2024/D41/K4/g, ND168-2024/D41/K4/h, ND168-2024/D41/K4/i, ND168-2024/D41/K4/k, ND168-2024/D41/K4/l, ND168-2024/D41/K4/m

Điều 41. Phân định thẩm quyền xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ
4. Trưởng Công an cấp xã, Trưởng đồn Công an, Trưởng trạm Công an cửa khẩu, khu chế xuất trong phạm vi chức năng, nhiệm vụ được giao có liên quan đến trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ có thẩm quyền xử phạt đối với các hành vi vi phạm quy định tại các điểm, khoản, điều của Nghị định này như sau:
a) Điểm đ khoản 1; điểm d, điểm đ khoản 2; điểm b, điểm d, điểm đ, điểm e, điểm g khoản 3 Điều 6;
b) Điểm d, điểm e, điểm g, điểm i khoản 1; điểm a, điểm d, điểm e, điểm g, điểm h, điểm i, điểm k khoản 2; điểm b, điểm c, điểm e, điểm g, điểm k khoản 3; điểm b, điểm d, điểm đ khoản 4 Điều 7;
c) Khoản 2; điểm b, điểm c khoản 3; điểm c, điểm d, điểm đ, điểm e khoản 4 Điều 8;
d) Điểm a, điểm b, điểm c, điểm d, điểm đ, điểm e, điểm g, điểm h, điểm i, điểm k, điểm l, điểm m, điểm n, điểm o khoản 1; khoản 2; điểm a, điểm b, điểm c khoản 3; điểm d, điểm đ khoản 4 Điều 9;
đ) Khoản 1; điểm b, điểm c khoản 2 Điều 10;
e) Khoản 1, khoản 2 Điều 11;
g) Khoản 1; khoản 2; khoản 3; khoản 5; điểm c, điểm d khoản 6 Điều 12;
h) Điều 15;
i) Khoản 1 Điều 17;
k) Điểm b khoản 3 Điều 20;
l) Khoản 1, khoản 2 Điều 33;
m) Khoản 1 Điều 35.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D6/K1/đ)
Mã điều khoản dùng được cho gold_units: ND168-2024/D6/K1/đ

Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
1. Phạt tiền từ 400.000 đồng đến 600.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
đ) Sử dụng còi trong thời gian từ 22 giờ ngày hôm trước đến 05 giờ ngày hôm sau trong khu đông dân cư, khu vực cơ sở khám bệnh, chữa bệnh, trừ các xe ưu tiên đang đi làm nhiệm vụ theo quy định.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D6/K2/d)
Mã điều khoản dùng được cho gold_units: ND168-2024/D6/K2/d

Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
2. Phạt tiền từ 600.000 đồng đến 800.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
d) Dừng xe, đỗ xe trên phần đường xe chạy ở đoạn đường ngoài đô thị nơi có lề đường rộng; dừng xe, đỗ xe không sát mép đường phía bên phải theo chiều đi ở nơi đường có lề đường hẹp hoặc không có lề đường; dừng xe, đỗ xe ngược với chiều lưu thông của làn đường; dừng xe, đỗ xe trên dải phân cách cố định ở giữa hai phần đường xe chạy; đỗ xe trên dốc không chèn bánh;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D6/K2/đ)
Mã điều khoản dùng được cho gold_units: ND168-2024/D6/K2/đ

Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
2. Phạt tiền từ 600.000 đồng đến 800.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
đ) Dừng xe không sát theo lề đường, vỉa hè phía bên phải theo chiều đi hoặc bánh xe gần nhất cách lề đường, vỉa hè quá 0,25 mét; dừng xe trên đường dành riêng cho xe buýt; dừng xe trên miệng cống thoát nước, miệng hầm của đường điện thoại, điện cao thế, chỗ dành riêng cho xe chữa cháy lấy nước; rời vị trí lái, tắt máy khi dừng xe (trừ trường hợp rời khỏi vị trí lái để đóng, mở cửa xe, xếp dỡ hàng hóa, kiểm tra kỹ thuật xe) hoặc rời vị trí lái khi dừng xe nhưng không sử dụng phanh đỗ xe (hoặc thực hiện biện pháp an toàn khác); dừng xe, đỗ xe không đúng vị trí quy định ở những đoạn có bố trí nơi dừng xe, đỗ xe; dừng xe, đỗ xe trên phần đường dành cho người đi bộ qua đường; dừng xe nơi có biển “Cấm dừng xe và đỗ xe”, trừ hành vi vi phạm quy định tại điểm đ khoản 4, điểm c khoản 7 Điều này.

### Trạng thái sau mốc (áp dụng tại 2026-08-15)
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2026-08-15 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D41/K4, ND168-2024/D41/K4/a, ND168-2024/D41/K4/b, ND168-2024/D41/K4/c, ND168-2024/D41/K4/d, ND168-2024/D41/K4/đ, ND168-2024/D41/K4/e, ND168-2024/D41/K4/g, ND168-2024/D41/K4/h, ND168-2024/D41/K4/i, ND168-2024/D41/K4/k, ND168-2024/D41/K4/k1, ND168-2024/D41/K4/l, ND168-2024/D41/K4/m

Điều 41. Phân định thẩm quyền xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ
4. Trưởng Công an cấp xã, Trưởng đồn Công an, Trưởng trạm Công an cửa khẩu, khu chế xuất trong phạm vi chức năng, nhiệm vụ được giao có liên quan đến trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ có thẩm quyền xử phạt đối với các hành vi vi phạm quy định tại các điểm, khoản, điều của Nghị định này như sau:
a) Điểm đ khoản 1; điểm d, điểm đ khoản 2; điểm b, điểm d, điểm đ, điểm e, điểm g khoản 3 Điều 6;
b) Điểm d, điểm e, điểm g, điểm i khoản 1; điểm a, điểm d, điểm e, điểm g, điểm h, điểm i, điểm k khoản 2; điểm b, điểm c, điểm e, điểm g, điểm k khoản 3; điểm b, điểm d, điểm đ khoản 4 Điều 7;
c) Khoản 2; điểm b, điểm c khoản 3; điểm c, điểm d, điểm đ, điểm e khoản 4 Điều 8;
d) Điểm a, điểm b, điểm c, điểm d, điểm đ, điểm e, điểm g, điểm h, điểm i, điểm k, điểm l, điểm m, điểm n, điểm o khoản 1; khoản 2; điểm a, điểm b, điểm c khoản 3; điểm d, điểm đ khoản 4 Điều 9;
đ) Khoản 1; điểm b, điểm c khoản 2 Điều 10;
e) Khoản 1, khoản 2 Điều 11;
g) Khoản 1; khoản 2; khoản 3; khoản 5; điểm c, điểm d khoản 6 Điều 12;
h) Điều 15;
i) Khoản 1 Điều 17;
k) Điểm b khoản 3 Điều 20;
k1) Điểm a, điểm b khoản 3; điểm b, điểm c, điểm d, điểm h khoản 7; điểm a, điểm c, điểm d khoản 8 Điều 32;
l) Khoản 1, khoản 2 Điều 33;
m) Khoản 1 Điều 35.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D6/K1/đ)
Mã điều khoản dùng được cho gold_units: ND168-2024/D6/K1/đ

Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
1. Phạt tiền từ 400.000 đồng đến 600.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
đ) Sử dụng còi trong thời gian từ 22 giờ ngày hôm trước đến 05 giờ ngày hôm sau trong khu đông dân cư, khu vực cơ sở khám bệnh, chữa bệnh, trừ các xe ưu tiên đang đi làm nhiệm vụ theo quy định.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D6/K2/d)
Mã điều khoản dùng được cho gold_units: ND168-2024/D6/K2/d

Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
2. Phạt tiền từ 600.000 đồng đến 800.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
d) Dừng xe, đỗ xe trên phần đường xe chạy ở đoạn đường ngoài đô thị nơi có lề đường rộng; dừng xe, đỗ xe không sát mép đường phía bên phải theo chiều đi ở nơi đường có lề đường hẹp hoặc không có lề đường; dừng xe, đỗ xe ngược với chiều lưu thông của làn đường; dừng xe, đỗ xe trên dải phân cách cố định ở giữa hai phần đường xe chạy; đỗ xe trên dốc không chèn bánh;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D6/K2/đ)
Mã điều khoản dùng được cho gold_units: ND168-2024/D6/K2/đ

Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
2. Phạt tiền từ 600.000 đồng đến 800.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
đ) Dừng xe không sát theo lề đường, vỉa hè phía bên phải theo chiều đi hoặc bánh xe gần nhất cách lề đường, vỉa hè quá 0,25 mét; dừng xe trên đường dành riêng cho xe buýt; dừng xe trên miệng cống thoát nước, miệng hầm của đường điện thoại, điện cao thế, chỗ dành riêng cho xe chữa cháy lấy nước; rời vị trí lái, tắt máy khi dừng xe (trừ trường hợp rời khỏi vị trí lái để đóng, mở cửa xe, xếp dỡ hàng hóa, kiểm tra kỹ thuật xe) hoặc rời vị trí lái khi dừng xe nhưng không sử dụng phanh đỗ xe (hoặc thực hiện biện pháp an toàn khác); dừng xe, đỗ xe không đúng vị trí quy định ở những đoạn có bố trí nơi dừng xe, đỗ xe; dừng xe, đỗ xe trên phần đường dành cho người đi bộ qua đường; dừng xe nơi có biển “Cấm dừng xe và đỗ xe”, trừ hành vi vi phạm quy định tại điểm đ khoản 4, điểm c khoản 7 Điều này.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2026-08-14): Tôi đã bật còi từ 23h đến 02h trong khu dân cư, có bị phạt không?
- Đáp: Bạn sẽ bị phạt tiền từ 400.000 đồng đến 600.000 đồng vì đã sử dụng còi trong thời gian từ 22 giờ ngày hôm trước đến 05 giờ ngày hôm sau trong khu đông dân cư, khu vực cơ sở khám bệnh, chữa bệnh, trừ các xe ưu tiên đang đi làm nhiệm vụ theo quy định.
- ⚠ dap_an_cap_giong_nhau
- Hỏi (2026-08-15): Tôi đã bật còi từ 23h đến 02h trong khu dân cư, có bị phạt không?
- Đáp: Bạn sẽ bị phạt tiền từ 400.000 đồng đến 600.000 đồng vì đã sử dụng còi trong thời gian từ 22 giờ ngày hôm trước đến 05 giờ ngày hôm sau trong khu đông dân cư, khu vực cơ sở khám bệnh, chữa bệnh, trừ các xe ưu tiên đang đi làm nhiệm vụ theo quy định.
- ⚠ dap_an_cap_giong_nhau

```json
{"qid": "tD-theo_thoi_diem-019a", "question": "Tôi đã bật còi từ 23h đến 02h trong khu dân cư, có bị phạt không?", "as_of": "2026-08-14", "question_type": "theo_thoi_diem", "tier": "A", "answer": "Bạn sẽ bị phạt tiền từ 400.000 đồng đến 600.000 đồng vì đã sử dụng còi trong thời gian từ 22 giờ ngày hôm trước đến 05 giờ ngày hôm sau trong khu đông dân cư, khu vực cơ sở khám bệnh, chữa bệnh, trừ các xe ưu tiên đang đi làm nhiệm vụ theo quy định.", "gold_units": ["ND168-2024/D6/K1/đ"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-019:1a", "pair_id": "pD-019"}
{"qid": "tD-theo_thoi_diem-019b", "question": "Tôi đã bật còi từ 23h đến 02h trong khu dân cư, có bị phạt không?", "as_of": "2026-08-15", "question_type": "theo_thoi_diem", "tier": "A", "answer": "Bạn sẽ bị phạt tiền từ 400.000 đồng đến 600.000 đồng vì đã sử dụng còi trong thời gian từ 22 giờ ngày hôm trước đến 05 giờ ngày hôm sau trong khu đông dân cư, khu vực cơ sở khám bệnh, chữa bệnh, trừ các xe ưu tiên đang đi làm nhiệm vụ theo quy định.", "gold_units": ["ND168-2024/D6/K1/đ"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-019:1b", "pair_id": "pD-019"}
```

**Nháp 2**

- Hỏi (2026-08-14): Tôi đã dừng xe trên dải phân cách giữa hai làn đường vào lúc 10h sáng, có bị phạt không?
- Đáp: Bạn sẽ bị phạt tiền từ 600.000 đồng đến 800.000 đồng vì đã dừng xe, đỗ xe trên dải phân cách cố định ở giữa hai phần đường xe chạy.
- ⚠ dap_an_cap_giong_nhau
- Hỏi (2026-08-15): Tôi đã dừng xe trên dải phân cách giữa hai làn đường vào lúc 10h sáng, có bị phạt không?
- Đáp: Bạn sẽ bị phạt tiền từ 600.000 đồng đến 800.000 đồng vì đã dừng xe, đỗ xe trên dải phân cách cố định ở giữa hai phần đường xe chạy.
- ⚠ dap_an_cap_giong_nhau

```json
{"qid": "tD-theo_thoi_diem-019a", "question": "Tôi đã dừng xe trên dải phân cách giữa hai làn đường vào lúc 10h sáng, có bị phạt không?", "as_of": "2026-08-14", "question_type": "theo_thoi_diem", "tier": "A", "answer": "Bạn sẽ bị phạt tiền từ 600.000 đồng đến 800.000 đồng vì đã dừng xe, đỗ xe trên dải phân cách cố định ở giữa hai phần đường xe chạy.", "gold_units": ["ND168-2024/D6/K2/d"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-019:2a", "pair_id": "pD-019"}
{"qid": "tD-theo_thoi_diem-019b", "question": "Tôi đã dừng xe trên dải phân cách giữa hai làn đường vào lúc 10h sáng, có bị phạt không?", "as_of": "2026-08-15", "question_type": "theo_thoi_diem", "tier": "A", "answer": "Bạn sẽ bị phạt tiền từ 600.000 đồng đến 800.000 đồng vì đã dừng xe, đỗ xe trên dải phân cách cố định ở giữa hai phần đường xe chạy.", "gold_units": ["ND168-2024/D6/K2/d"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-019:2b", "pair_id": "pD-019"}
```

### WD-theo_thoi_diem-020 · tier A · vai: phụ huynh có con dưới 18 tuổi · kiểu: tinh_huong_ban_than · trước mốc: chưa có hiệu lực

<details><summary>Nguồn và con số</summary>

```text
### Trạng thái trước mốc (áp dụng tại 2025-08-31)
Chưa có hiệu lực (không có phiên bản).

### Trạng thái sau mốc (áp dụng tại 2025-09-01)
Văn bản: Thông tư số 14/2025/TT-BXD (Quy định về đào tạo lái xe; bồi dưỡng, kiểm tra, cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ)
Hiệu lực của trạng thái này: 2025-09-01 → nay
Mã điều khoản dùng được cho gold_units: TT14-2025-BXD/D23/K1, TT14-2025-BXD/D23/K1/a, TT14-2025-BXD/D23/K1/b

Điều 23. Cấp lại chứng chỉ
1. Người có chứng chỉ bị hỏng hoặc có sự sai lệch về thông tin có tên trong hồ sơ lưu trữ tại nơi cấp chứng chỉ, sẽ được cấp lại theo số hiệu chứng chỉ đã cấp. Hồ sơ đề nghị cấp lại, bao gồm:
a) Đơn đề nghị cấp lại chứng chỉ theo mẫu quy định tại Phụ lục XVI ban hành kèm theo Thông tư này;
b) 03 ảnh màu kích thước 2x3 cm chụp không quá 06 tháng.

(không có con số nào lấy được bằng rule — required_numbers_idx để rỗng)
```

</details>

**Nháp 1**

- Hỏi (2025-08-31): Tôi muốn cấp lại chứng chỉ lái xe vì bị hỏng, cần chuẩn bị gì vào ngày 30/8/2025?
- Đáp: chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu
- Hỏi (2025-09-01): Tôi muốn cấp lại chứng chỉ lái xe vì bị hỏng, cần chuẩn bị gì vào ngày 2/9/2025?
- Đáp: Bạn cần nộp đơn theo mẫu Phụ lục XVI, kèm 3 ảnh màu 2x3 cm chụp không quá 6 tháng. (TT14-2025-BXD/D23/K1, TT14-2025-BXD/D23/K1/a, TT14-2025-BXD/D23/K1/b)

```json
{"qid": "tD-theo_thoi_diem-020a", "question": "Tôi muốn cấp lại chứng chỉ lái xe vì bị hỏng, cần chuẩn bị gì vào ngày 30/8/2025?", "as_of": "2025-08-31", "question_type": "theo_thoi_diem", "tier": "A", "answer": "chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu", "gold_units": [], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-020:1a", "pair_id": "pD-020"}
{"qid": "tD-theo_thoi_diem-020b", "question": "Tôi muốn cấp lại chứng chỉ lái xe vì bị hỏng, cần chuẩn bị gì vào ngày 2/9/2025?", "as_of": "2025-09-01", "question_type": "theo_thoi_diem", "tier": "A", "answer": "Bạn cần nộp đơn theo mẫu Phụ lục XVI, kèm 3 ảnh màu 2x3 cm chụp không quá 6 tháng. (TT14-2025-BXD/D23/K1, TT14-2025-BXD/D23/K1/a, TT14-2025-BXD/D23/K1/b)", "gold_units": ["TT14-2025-BXD/D23/K1", "TT14-2025-BXD/D23/K1/a", "TT14-2025-BXD/D23/K1/b"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-020:1b", "pair_id": "pD-020"}
```

**Nháp 2**

- Hỏi (2025-08-31): Con tôi muốn lấy lại chứng chỉ lái xe vì bị hỏng, tôi cần làm gì vào ngày 30/8/2025?
- Đáp: chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu
- Hỏi (2025-09-01): Con tôi muốn lấy lại chứng chỉ lái xe vì bị hỏng, tôi cần làm gì vào ngày 2/9/2025?
- Đáp: Bạn cần nộp đơn theo mẫu Phụ lục XVI, kèm 3 ảnh màu 2x3 cm chụp không quá 6 tháng. (TT14-2025-BXD/D23/K1, TT14-2025-BXD/D23/K1/a, TT14-2025-BXD/D23/K1/b)

```json
{"qid": "tD-theo_thoi_diem-020a", "question": "Con tôi muốn lấy lại chứng chỉ lái xe vì bị hỏng, tôi cần làm gì vào ngày 30/8/2025?", "as_of": "2025-08-31", "question_type": "theo_thoi_diem", "tier": "A", "answer": "chưa có quy định có hiệu lực tại thời điểm này trong dữ liệu", "gold_units": [], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-020:2a", "pair_id": "pD-020"}
{"qid": "tD-theo_thoi_diem-020b", "question": "Con tôi muốn lấy lại chứng chỉ lái xe vì bị hỏng, tôi cần làm gì vào ngày 2/9/2025?", "as_of": "2025-09-01", "question_type": "theo_thoi_diem", "tier": "A", "answer": "Bạn cần nộp đơn theo mẫu Phụ lục XVI, kèm 3 ảnh màu 2x3 cm chụp không quá 6 tháng. (TT14-2025-BXD/D23/K1, TT14-2025-BXD/D23/K1/a, TT14-2025-BXD/D23/K1/b)", "gold_units": ["TT14-2025-BXD/D23/K1", "TT14-2025-BXD/D23/K1/a", "TT14-2025-BXD/D23/K1/b"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-theo_thoi_diem-020:2b", "pair_id": "pD-020"}
```

## so_sanh — so sánh giữa loại xe hoặc chủ thể

### WD-so_sanh-001 · tier A · vai: người lớn tuổi đi xe đạp điện · kiểu: tinh_huong_nguoi_khac · cosine TF-IDF 0.43

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D18/K9, ND168-2024/D18/K9/a, ND168-2024/D18/K9/b

Điều 18. Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm quy định về điều kiện của người điều khiển xe cơ giới
9. Phạt tiền từ 18.000.000 đồng đến 20.000.000 đồng đối với người điều khiển xe ô tô và các loại xe tương tự xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ vi phạm một trong các hành vi sau đây:
a) Có giấy phép lái xe nhưng không phù hợp với loại xe đang điều khiển hoặc có giấy phép lái xe nhưng đã hết hạn sử dụng từ 01 năm trở lên;
b) Không có giấy phép lái xe hoặc sử dụng giấy phép lái xe đã bị trừ hết điểm hoặc sử dụng giấy phép lái xe không do cơ quan có thẩm quyền cấp, giấy phép lái xe bị tẩy xóa, giấy phép lái xe không còn hiệu lực.

### Nguồn 2
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D22/K2

Điều 22. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển hàng siêu trường, siêu trọng
2. Phạt tiền từ 8.000.000 đồng đến 10.000.000 đồng đối với hành vi chở hàng siêu trường, siêu trọng có giấy phép lưu hành còn giá trị sử dụng nhưng kích thước bao ngoài của xe (sau khi đã xếp hàng lên xe) vượt quá quy định trong giấy phép lưu hành.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D22/K6/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D22/K6/b

Điều 22. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển hàng siêu trường, siêu trọng
6. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
b) Thực hiện hành vi quy định tại khoản 2, khoản 3 Điều này bị trừ điểm giấy phép lái xe 04 điểm.

[0] 18.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D18/K9)
[1] 20.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D18/K9)
[2] 8.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D22/K2)
[3] 10.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D22/K2)
[4] 04 điểm (số điểm bị trừ, nêu tại ND168-2024/D22/K6/b)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Anh tôi lái xe ô tô nhưng giấy phép hết hạn 2 năm, còn anh ấy chở hàng siêu trọng vượt kích thước. Phạt tiền của hai trường hợp khác nhau bao nhiêu?
- Đáp: Mức phạt tiền khi lái xe ô tô với giấy phép hết hạn là từ 18.000.000 đồng đến 20.000.000 đồng. Khi chở hàng siêu trọng vượt kích thước, mức phạt tiền là từ 8.000.000 đồng đến 10.000.000 đồng.
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-so_sanh-001", "question": "Anh tôi lái xe ô tô nhưng giấy phép hết hạn 2 năm, còn anh ấy chở hàng siêu trọng vượt kích thước. Phạt tiền của hai trường hợp khác nhau bao nhiêu?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Mức phạt tiền khi lái xe ô tô với giấy phép hết hạn là từ 18.000.000 đồng đến 20.000.000 đồng. Khi chở hàng siêu trọng vượt kích thước, mức phạt tiền là từ 8.000.000 đồng đến 10.000.000 đồng.", "gold_units": ["ND168-2024/D18/K9", "ND168-2024/D22/K2"], "required_numbers": [{"value": 18000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}, {"value": 8000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-001:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Công ty tôi vận chuyển hàng siêu trọng vượt giới hạn, trong khi tôi lái xe ô tô với giấy phép hết hạn. So sánh mức phạt tiền và điểm trừ của hai hành vi.
- Đáp: Mức phạt tiền khi lái xe ô tô với giấy phép hết hạn là từ 18.000.000 đồng đến 20.000.000 đồng. Khi chở hàng siêu trọng vượt kích thước, mức phạt tiền là từ 8.000.000 đồng đến 10.000.000 đồng, và người điều khiển bị trừ 04 điểm giấy phép.
- Ghi chú: Giả định người lái xe là cá nhân, công ty là tổ chức

```json
{"qid": "tD-so_sanh-001", "question": "Công ty tôi vận chuyển hàng siêu trọng vượt giới hạn, trong khi tôi lái xe ô tô với giấy phép hết hạn. So sánh mức phạt tiền và điểm trừ của hai hành vi.", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Mức phạt tiền khi lái xe ô tô với giấy phép hết hạn là từ 18.000.000 đồng đến 20.000.000 đồng. Khi chở hàng siêu trọng vượt kích thước, mức phạt tiền là từ 8.000.000 đồng đến 10.000.000 đồng, và người điều khiển bị trừ 04 điểm giấy phép.", "gold_units": ["ND168-2024/D18/K9", "ND168-2024/D22/K2", "ND168-2024/D22/K6/b"], "required_numbers": [{"value": 18000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}, {"value": 8000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}, {"value": 4, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-001:2"}
```

### WD-so_sanh-002 · tier A · vai: phụ huynh có con dưới 18 tuổi · kiểu: tinh_huong_ban_than · cosine TF-IDF 0.56

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K9, ND168-2024/D32/K9/a, ND168-2024/D32/K9/b, ND168-2024/D32/K9/c, ND168-2024/D32/K9/d, ND168-2024/D32/K9/đ, ND168-2024/D32/K9/e

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
9. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng đối với cá nhân, từ 8.000.000 đồng đến 12.000.000 đồng đối với tổ chức là chủ xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ, xe máy chuyên dùng và các loại xe tương tự xe ô tô thực hiện một trong các hành vi vi phạm sau đây:
a) Thuê, mượn linh kiện, phụ kiện của xe ô tô khi kiểm định;
b) Đưa xe cơ giới, xe máy chuyên dùng có giấy chứng nhận hoặc tem kiểm định an toàn kỹ thuật và bảo vệ môi trường (đối với loại xe có quy định phải kiểm định) nhưng đã hết hiệu lực (hạn sử dụng) dưới 01 tháng (kể cả rơ moóc và sơ mi rơ moóc) tham gia giao thông;
c) Giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại khoản 4 Điều 21 của Nghị định này hoặc trực tiếp điều khiển phương tiện thực hiện hành vi vi phạm quy định tại khoản 4 Điều 21 của Nghị định này;
d) Giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm d khoản 6 Điều 20; điểm b khoản 5 Điều 21 của Nghị định này hoặc trực tiếp điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm d khoản 6 Điều 20; điểm b khoản 5 Điều 21 của Nghị định này;
…

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K21/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K21/a

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
21. Ngoài việc bị áp dụng hình thức xử phạt, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
a) Thực hiện hành vi quy định tại điểm đ, điểm g, điểm m khoản 7; điểm đ, điểm e khoản 8; điểm b, điểm c, điểm d, điểm đ khoản 9; điểm a, điểm b, điểm đ khoản 11; điểm a khoản 12; điểm c khoản 13; điểm đ, điểm h khoản 14 Điều này trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện còn bị trừ điểm giấy phép lái xe 02 điểm;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D21/K4)
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K4

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
4. Phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng đối với người điều khiển xe thực hiện hành vi chở hàng vượt quá chiều cao xếp hàng cho phép đối với xe ô tô tải (kể cả rơ moóc và sơ mi rơ moóc).

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D20/K6/d)
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K6/d

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
6. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
d) Điều khiển xe ô tô kinh doanh vận tải, xe vận tải nội bộ quá thời gian quy định tại khoản 1 Điều 64 của Luật Trật tự, an toàn giao thông đường bộ; không thực hiện đúng quy định về thời gian nghỉ giữa hai lần lái xe liên tục của người lái xe;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D21/K5/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K5/b

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
5. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
b) Điều khiển xe ô tô kinh doanh vận tải, xe vận tải nội bộ quá thời gian quy định tại khoản 1 Điều 64 của Luật Trật tự, an toàn giao thông đường bộ; không thực hiện đúng quy định về thời gian nghỉ giữa hai lần lái xe liên tục của người lái xe;

### Nguồn 2
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D40/K2, ND168-2024/D40/K2/a, ND168-2024/D40/K2/b, ND168-2024/D40/K2/c, ND168-2024/D40/K2/d, ND168-2024/D40/K2/đ, ND168-2024/D40/K2/e, ND168-2024/D40/K2/g

Điều 40. Xử phạt các hành vi vi phạm quy định về hoạt động đăng kiểm xe cơ giới, xe máy chuyên dùng, phụ tùng xe cơ giới
2. Phạt tiền từ 10.000.000 đồng đến 15.000.000 đồng đối với cơ sở đăng kiểm thực hiện một trong các hành vi vi phạm sau đây:
a) Không duy trì việc bảo đảm về điều kiện, yêu cầu theo quy định tại Nghị định của Chính phủ quy định về điều kiện kinh doanh dịch vụ kiểm định xe cơ giới; tổ chức, hoạt động của cơ sở đăng kiểm; niên hạn sử dụng của xe cơ giới;
b) Có từ 02 lượt đăng kiểm viên trở lên bị xử phạt theo quy định tại khoản 1 Điều này trong thời hạn 12 tháng tính từ lần vi phạm đầu tiên;
c) Phân công người không đủ điều kiện thực hiện nhiệm vụ của đăng kiểm viên, nhân viên nghiệp vụ;
d) Cấp chứng nhận cải tạo cho xe cơ giới, xe máy chuyên dùng không đúng quy định;
đ) Thực hiện kiểm định đối với phương tiện thuộc trường hợp bị từ chối kiểm định theo quy định;
e) Lưu trữ hồ sơ, tài liệu, dữ liệu kiểm định, cải tạo xe không đúng quy định;
g) Không thực hiện việc cập nhật hồ sơ phương tiện cho xe cơ giới, xe máy chuyên dùng theo quy định.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D40/K6/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D40/K6/b

Điều 40. Xử phạt các hành vi vi phạm quy định về hoạt động đăng kiểm xe cơ giới, xe máy chuyên dùng, phụ tùng xe cơ giới
6. Ngoài việc bị phạt tiền, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị áp dụng hình thức xử phạt bổ sung sau đây:
b) Thực hiện hành vi quy định tại điểm a, điểm b, điểm c, điểm d, điểm g khoản 2; khoản 4 Điều này bị tước quyền sử dụng giấy chứng nhận đủ điều kiện hoạt động kiểm định xe cơ giới từ 01 tháng đến 03 tháng.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D40/K1)
Mã điều khoản dùng được cho gold_units: ND168-2024/D40/K1

Điều 40. Xử phạt các hành vi vi phạm quy định về hoạt động đăng kiểm xe cơ giới, xe máy chuyên dùng, phụ tùng xe cơ giới
1. Phạt tiền từ 8.000.000 đồng đến 10.000.000 đồng đối với cá nhân thực hiện một trong các hành vi vi phạm sau đây:

[0] 4.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D32/K9)
[1] 6.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D32/K9)
[2] 8.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D32/K9)
[3] 12.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D32/K9)
[4] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D32/K21/a)
[5] 10.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D40/K2)
[6] 15.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D40/K2)
[7] 01 tháng (thời hạn tước quyền sử dụng tối thiểu, nêu tại ND168-2024/D40/K6/b)
[8] 03 tháng (thời hạn tước quyền sử dụng tối đa, nêu tại ND168-2024/D40/K6/b)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là phụ huynh, con tôi lái xe ô tô và vi phạm hành vi đưa xe cơ giới có giấy kiểm định hết hạn, còn tôi muốn biết so sánh mức phạt tiền và điểm trừ khi con tôi vi phạm hành vi này so với khi con tôi lái xe tải chở hàng vượt quá chiều cao xếp hàng cho phép.
- Đáp: Nếu con tôi vi phạm hành vi đưa xe cơ giới có giấy kiểm định hết hạn, mức phạt tiền sẽ từ 4.000.000 đồng đến 6.000.000 đồng và bị trừ 02 điểm. Nếu con tôi vi phạm hành vi chở hàng vượt quá chiều cao xếp hàng cho phép, mức phạt tiền sẽ từ 2.000.000 đồng đến 3.000.000 đồng. Do đó, mức phạt tiền và điểm trừ của chủ xe ô tô cao hơn so với người điều khiển xe tải.
- ⚠ qua_dai (63 từ); chep_nguyen_van: “chiều cao xếp hàng cho phép …”
- Ghi chú: Giả định con tôi lái xe ô tô và xe tải trong cùng một trường hợp vi phạm hành vi khác nhau.

```json
{"qid": "tD-so_sanh-002", "question": "Tôi là phụ huynh, con tôi lái xe ô tô và vi phạm hành vi đưa xe cơ giới có giấy kiểm định hết hạn, còn tôi muốn biết so sánh mức phạt tiền và điểm trừ khi con tôi vi phạm hành vi này so với khi con tôi lái xe tải chở hàng vượt quá chiều cao xếp hàng cho phép.", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Nếu con tôi vi phạm hành vi đưa xe cơ giới có giấy kiểm định hết hạn, mức phạt tiền sẽ từ 4.000.000 đồng đến 6.000.000 đồng và bị trừ 02 điểm. Nếu con tôi vi phạm hành vi chở hàng vượt quá chiều cao xếp hàng cho phép, mức phạt tiền sẽ từ 2.000.000 đồng đến 3.000.000 đồng. Do đó, mức phạt tiền và điểm trừ của chủ xe ô tô cao hơn so với người điều khiển xe tải.", "gold_units": ["ND168-2024/D32/K9", "ND168-2024/D21/K4"], "required_numbers": [{"value": 4000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-002:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là phụ huynh, con tôi lái xe ô tô và vi phạm hành vi đưa xe cơ giới có giấy kiểm định hết hạn, còn tôi muốn biết so sánh mức phạt tiền và điểm trừ khi con tôi vi phạm hành vi này so với khi con tôi lái xe tải chở hàng vượt quá chiều cao xếp hàng cho phép.
- Đáp: Nếu con tôi vi phạm hành vi đưa xe cơ giới có giấy kiểm định hết hạn, mức phạt tiền sẽ từ 4.000.000 đồng đến 6.000.000 đồng và bị trừ 02 điểm. Nếu con tôi vi phạm hành vi chở hàng vượt quá chiều cao xếp hàng cho phép, mức phạt tiền sẽ từ 2.000.000 đồng đến 3.000.000 đồng. Do đó, mức phạt tiền và điểm trừ của chủ xe ô tô cao hơn so với người điều khiển xe tải.
- ⚠ qua_dai (63 từ); chep_nguyen_van: “chiều cao xếp hàng cho phép …”
- Ghi chú: Giả định con tôi lái xe ô tô và xe tải trong cùng một trường hợp vi phạm hành vi khác nhau.

```json
{"qid": "tD-so_sanh-002", "question": "Tôi là phụ huynh, con tôi lái xe ô tô và vi phạm hành vi đưa xe cơ giới có giấy kiểm định hết hạn, còn tôi muốn biết so sánh mức phạt tiền và điểm trừ khi con tôi vi phạm hành vi này so với khi con tôi lái xe tải chở hàng vượt quá chiều cao xếp hàng cho phép.", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Nếu con tôi vi phạm hành vi đưa xe cơ giới có giấy kiểm định hết hạn, mức phạt tiền sẽ từ 4.000.000 đồng đến 6.000.000 đồng và bị trừ 02 điểm. Nếu con tôi vi phạm hành vi chở hàng vượt quá chiều cao xếp hàng cho phép, mức phạt tiền sẽ từ 2.000.000 đồng đến 3.000.000 đồng. Do đó, mức phạt tiền và điểm trừ của chủ xe ô tô cao hơn so với người điều khiển xe tải.", "gold_units": ["ND168-2024/D32/K9", "ND168-2024/D21/K4"], "required_numbers": [{"value": 4000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-002:2"}
```

### WD-so_sanh-003 · tier A · vai: người lớn tuổi đi xe đạp điện · kiểu: neu_van_ban · cosine TF-IDF 0.76

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D26/K6, ND168-2024/D26/K6/a, ND168-2024/D26/K6/b, ND168-2024/D26/K6/c, ND168-2024/D26/K6/d

Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
6. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng đối với cá nhân, từ 8.000.000 đồng đến 12.000.000 đồng đối với tổ chức kinh doanh vận tải thực hiện một trong các hành vi vi phạm sau đây:
a) Sử dụng xe vận chuyển động vật sống không có kết cấu phù hợp với loại động vật chuyên chở theo quy định;
b) Sử dụng xe ô tô kinh doanh vận tải chở trẻ em mầm non, học sinh, xe ô tô kinh doanh vận tải kết hợp với hoạt động đưa đón trẻ em mầm non, học sinh không có thiết bị ghi nhận hình ảnh trẻ em mầm non, học sinh hoặc không có thiết bị có chức năng cảnh báo, chống bỏ quên trẻ em trên xe hoặc không có thiết bị ghi nhận hình ảnh trẻ em mầm non, học sinh và thiết bị có chức năng cảnh báo, chống bỏ quên trẻ em trên xe;
c) Sử dụng xe ô tô kinh doanh vận tải chở trẻ em mầm non, học sinh không có màu sơn theo quy định;
d) Sử dụng xe ô tô kinh doanh vận tải chở trẻ em mầm non, học sinh, xe ô tô kinh doanh vận tải kết hợp với hoạt động đưa đón trẻ em mầm non, học sinh không có biển báo dấu hiệu nhận biết là xe chở trẻ em mầm non, học sinh theo quy định.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D26/K14/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D26/K14/a

Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
14. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
a) Thực hiện hành vi quy định tại điểm đ khoản 2; điểm b, điểm c, điểm d khoản 6; điểm b, điểm c, điểm e, điểm i khoản 7 Điều này trong trường hợp cá nhân kinh doanh vận tải là người trực tiếp điều khiển phương tiện còn bị trừ điểm giấy phép lái xe 02 điểm;

### Nguồn 2
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D27/K2

Điều 27. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô kinh doanh vận tải chở trẻ em mầm non, học sinh, xe ô tô kinh doanh vận tải kết hợp với hoạt động đưa đón trẻ em mầm non, học sinh
2. Phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng đối với hành vi điều khiển xe ô tô kinh doanh vận tải chở trẻ em mầm non, học sinh tiểu học, xe ô tô kinh doanh vận tải kết hợp với hoạt động đưa đón trẻ em mầm non, học sinh tiểu học không có hoặc không đủ người quản lý trên mỗi xe ô tô theo quy định tại khoản 3 Điều 46 của Luật Trật tự, an toàn giao thông đường bộ.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D27/K4)
Mã điều khoản dùng được cho gold_units: ND168-2024/D27/K4

Điều 27. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô kinh doanh vận tải chở trẻ em mầm non, học sinh, xe ô tô kinh doanh vận tải kết hợp với hoạt động đưa đón trẻ em mầm non, học sinh
4. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi quy định tại khoản 2, khoản 3 Điều này bị trừ điểm giấy phép lái xe 02 điểm.

### Điều khoản được nguồn trên dẫn chiếu tới (LUAT36-2024/D46/K3)
Mã điều khoản dùng được cho gold_units: LUAT36-2024/D46/K3

Điều 46. Bảo đảm trật tự, an toàn giao thông đường bộ đối với xe ô tô chở trẻ em mầm non, học sinh
3. Khi đưa đón trẻ em mầm non, học sinh tiểu học phải bố trí tối thiểu 01 người quản lý trên mỗi xe ô tô để hướng dẫn, giám sát, duy trì trật tự và bảo đảm an toàn cho trẻ em mầm non, học sinh tiểu học trong suốt chuyến đi. Trường hợp xe từ 29 chỗ trở lên (không kể chỗ của người lái xe) mà chở từ 27 trẻ em mầm non và học sinh tiểu học trở lên phải bố trí tối thiểu 02 người quản lý trên mỗi xe ô tô. Người quản lý, người lái xe có trách nhiệm kiểm tra trẻ em mầm non, học sinh tiểu học khi xuống xe; không được để trẻ em mầm non, học sinh tiểu học trên xe khi người quản lý và người lái xe đã rời xe.

[0] 4.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D26/K6)
[1] 6.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D26/K6)
[2] 8.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D26/K6)
[3] 12.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D26/K6)
[4] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D26/K14/a)
[5] 2.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D27/K2)
[6] 3.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D27/K2)
[7] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D27/K4)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Nếu một cá nhân và một tổ chức kinh doanh vận tải vi phạm việc sử dụng xe vận chuyển động vật sống không có kết cấu phù hợp, mức phạt tiền và điểm trừ sẽ khác nhau như thế nào?
- Đáp: Cá nhân sẽ bị phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng và bị trừ 02 điểm giấy phép lái xe. Tổ chức kinh doanh vận tải sẽ bị phạt tiền từ 8.000.000 đồng đến 12.000.000 đồng và cũng bị trừ 02 điểm giấy phép lái xe. (khoản 6 Điều 26 Nghị định 168/2024/NĐ-CP; khoản 14 Điều 26 Nghị định 168/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “chuyển động vật sống không có …”
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-so_sanh-003", "question": "Nếu một cá nhân và một tổ chức kinh doanh vận tải vi phạm việc sử dụng xe vận chuyển động vật sống không có kết cấu phù hợp, mức phạt tiền và điểm trừ sẽ khác nhau như thế nào?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Cá nhân sẽ bị phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng và bị trừ 02 điểm giấy phép lái xe. Tổ chức kinh doanh vận tải sẽ bị phạt tiền từ 8.000.000 đồng đến 12.000.000 đồng và cũng bị trừ 02 điểm giấy phép lái xe. (khoản 6 Điều 26 Nghị định 168/2024/NĐ-CP; khoản 14 Điều 26 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D26/K6", "ND168-2024/D26/K14/a"], "required_numbers": [{"value": 4000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}, {"value": 8000000, "unit": "vnd"}, {"value": 12000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-003:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Nếu một cá nhân và một tổ chức kinh doanh vận tải vi phạm việc không có thiết bị ghi nhận hình ảnh trẻ em hoặc không có thiết bị cảnh báo, mức phạt tiền và điểm trừ sẽ khác nhau như thế nào?
- Đáp: Cá nhân sẽ bị phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng và bị trừ 02 điểm giấy phép lái xe. Tổ chức kinh doanh vận tải sẽ bị phạt tiền từ 8.000.000 đồng đến 12.000.000 đồng và cũng bị trừ 02 điểm giấy phép lái xe. (khoản 6 Điều 26 Nghị định 168/2024/NĐ-CP; khoản 14 Điều 26 Nghị định 168/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “bị ghi nhận hình ảnh trẻ …”
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-so_sanh-003", "question": "Nếu một cá nhân và một tổ chức kinh doanh vận tải vi phạm việc không có thiết bị ghi nhận hình ảnh trẻ em hoặc không có thiết bị cảnh báo, mức phạt tiền và điểm trừ sẽ khác nhau như thế nào?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Cá nhân sẽ bị phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng và bị trừ 02 điểm giấy phép lái xe. Tổ chức kinh doanh vận tải sẽ bị phạt tiền từ 8.000.000 đồng đến 12.000.000 đồng và cũng bị trừ 02 điểm giấy phép lái xe. (khoản 6 Điều 26 Nghị định 168/2024/NĐ-CP; khoản 14 Điều 26 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D26/K6", "ND168-2024/D26/K14/a"], "required_numbers": [{"value": 4000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}, {"value": 8000000, "unit": "vnd"}, {"value": 12000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-003:2"}
```

### WD-so_sanh-004 · tier B · vai: sinh viên đi xe máy · kiểu: tinh_huong_ban_than · cosine TF-IDF 0.43

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)
Hiệu lực của trạng thái này: 2026-03-01 → nay
Mã điều khoản dùng được cho gold_units: ND336-2025/D7/K2, ND336-2025/D7/K2/a, ND336-2025/D7/K2/b, ND336-2025/D7/K2/c, ND336-2025/D7/K2/d, ND336-2025/D7/K2/đ, ND336-2025/D7/K2/e, ND336-2025/D7/K2/g

Điều 7. Xử phạt hành vi vi phạm quy định về đào tạo thẩm tra viên, điều kiện kinh doanh dịch vụ thẩm tra an toàn giao thông đường bộ
2. Phạt tiền từ 8.000.000 đồng đến 10.000.000 đồng đối với cơ sở đào tạo thẩm tra viên an toàn giao thông đường bộ thực hiện một trong các hành vi vi phạm sau đây:
a) Tuyển sinh, đào tạo học viên không đủ điều kiện tiêu chuẩn theo quy định;
b) Không thông báo kế hoạch đào tạo và danh sách học viên trước khi mở lớp theo quy định;
c) Đào tạo thẩm tra viên an toàn giao thông đường bộ không đúng chương trình khung, kế hoạch đào tạo đã thông báo theo quy định;
d) Công nhận kết quả thi cho người không tham dự thi hoặc không tham dự khóa đào tạo thẩm tra viên an toàn giao thông đường bộ;
đ) Không thành lập hoặc thành lập hội đồng thi không đúng quy định;
e) Không lưu trữ, bảo quản hồ sơ học viên theo quy định, trừ hành vi vi phạm quy định tại điểm g khoản này;
g) Không lập, lưu giữ, bảo quản hồ sơ tài liệu liên quan đến công tác đào tạo theo quy định.

### Nguồn 2
Văn bản: Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)
Hiệu lực của trạng thái này: 2026-03-01 → nay
Mã điều khoản dùng được cho gold_units: ND336-2025/D9/K5, ND336-2025/D9/K5/a, ND336-2025/D9/K5/b, ND336-2025/D9/K5/c, ND336-2025/D9/K5/d, ND336-2025/D9/K5/đ

Điều 9. Xử phạt các hành vi vi phạm quy định về quản lý, khai thác, bảo trì, bảo vệ kết cấu hạ tầng đường bộ
5. Phạt tiền từ 5.000.000 đồng đến 7.000.000 đồng đối với cá nhân, từ 10.000.000 đồng đến 14.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
a) Khoan, đào, xẻ đường, hè phố trái phép;
b) Phá dỡ trái phép, làm hư hỏng công trình phụ trợ gắn liền với đường bộ, cấu kiện, phụ kiện của công trình đường bộ, trừ hành vi vi phạm tại khoản 4; điểm а, điểm c và điểm d khoản này;
c) Tự ý tháo, mở làm hư hỏng nắp cống, nắp ga các công trình ngầm, hệ thống tuy nen trên đường bộ;
d) Nổ mìn hoặc khai thác đất, cát, đá, sỏi, khoáng sản khác làm ảnh hưởng đến an toàn công trình đường bộ;
đ) Không có quy trình vận hành, khai thác, bảo trì đường bộ theo quy định hoặc không thực hiện đầy đủ các nội dung trong quy trình vận hành, khai thác, bảo trì đường bộ đã được phê duyệt.

### Điều khoản được nguồn trên dẫn chiếu tới (ND336-2025/D9/K4)
Mã điều khoản dùng được cho gold_units: ND336-2025/D9/K4

Điều 9. Xử phạt các hành vi vi phạm quy định về quản lý, khai thác, bảo trì, bảo vệ kết cấu hạ tầng đường bộ
4. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với cá nhân, từ 6.000.000 đồng đến 10.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:

[0] 8.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D7/K2)
[1] 10.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D7/K2)
[2] 5.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D9/K5)
[3] 7.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D9/K5)
[4] 10.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D9/K5)
[5] 14.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D9/K5)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là người lái xe máy, vừa nghe nói có những quy định về phạt tiền khi vi phạm quy định đào tạo thẩm tra viên và khi vi phạm quản lý hạ tầng đường bộ. Tôi muốn biết mức phạt tiền tối thiểu và tối đa cho từng trường hợp, và so sánh xem trường hợp nào nặng hơn?
- Đáp: Mức phạt tiền tối thiểu khi vi phạm quy định đào tạo thẩm tra viên là 8.000.000 đồng, tối đa là 10.000.000 đồng. Mức phạt tiền tối thiểu khi vi phạm quản lý hạ tầng đường bộ là 5.000.000 đồng, tối đa là 7.000.000 đồng. Do đó, vi phạm quy định đào tạo thẩm tra viên nặng hơn. (Điều 7, Khoản 2, Nghị định 336/2025/NĐ-CP; Điều 9, Khoản 5, Nghị định 336/2025/NĐ-CP)
- ⚠ qua_dai (60 từ)
- Ghi chú: Giả định người hỏi là cá nhân (người lái xe máy).

```json
{"qid": "tD-so_sanh-004", "question": "Tôi là người lái xe máy, vừa nghe nói có những quy định về phạt tiền khi vi phạm quy định đào tạo thẩm tra viên và khi vi phạm quản lý hạ tầng đường bộ. Tôi muốn biết mức phạt tiền tối thiểu và tối đa cho từng trường hợp, và so sánh xem trường hợp nào nặng hơn?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "B", "answer": "Mức phạt tiền tối thiểu khi vi phạm quy định đào tạo thẩm tra viên là 8.000.000 đồng, tối đa là 10.000.000 đồng. Mức phạt tiền tối thiểu khi vi phạm quản lý hạ tầng đường bộ là 5.000.000 đồng, tối đa là 7.000.000 đồng. Do đó, vi phạm quy định đào tạo thẩm tra viên nặng hơn. (Điều 7, Khoản 2, Nghị định 336/2025/NĐ-CP; Điều 9, Khoản 5, Nghị định 336/2025/NĐ-CP)", "gold_units": ["ND336-2025/D7/K2", "ND336-2025/D9/K5"], "required_numbers": [{"value": 8000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}, {"value": 5000000, "unit": "vnd"}, {"value": 7000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-004:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi đang làm việc trong công ty xây dựng, và muốn biết so sánh mức phạt tiền khi công ty vi phạm quy định đào tạo thẩm tra viên so với khi công ty vi phạm quản lý hạ tầng đường bộ. Mức phạt tối thiểu và tối đa của từng trường hợp là gì, và trường hợp nào nặng hơn?
- Đáp: Mức phạt tiền tối thiểu khi công ty vi phạm quy định đào tạo thẩm tra viên là 8.000.000 đồng, tối đa là 10.000.000 đồng. Mức phạt tiền tối thiểu khi công ty vi phạm quản lý hạ tầng đường bộ là 10.000.000 đồng, tối đa là 14.000.000 đồng. Do đó, vi phạm quản lý hạ tầng đường bộ nặng hơn. (Điều 7, Khoản 2, Nghị định 336/2025/NĐ-CP; Điều 9, Khoản 5, Nghị định 336/2025/NĐ-CP)
- ⚠ qua_dai (61 từ)
- Ghi chú: Giả định người hỏi là tổ chức (công ty).

```json
{"qid": "tD-so_sanh-004", "question": "Tôi đang làm việc trong công ty xây dựng, và muốn biết so sánh mức phạt tiền khi công ty vi phạm quy định đào tạo thẩm tra viên so với khi công ty vi phạm quản lý hạ tầng đường bộ. Mức phạt tối thiểu và tối đa của từng trường hợp là gì, và trường hợp nào nặng hơn?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "B", "answer": "Mức phạt tiền tối thiểu khi công ty vi phạm quy định đào tạo thẩm tra viên là 8.000.000 đồng, tối đa là 10.000.000 đồng. Mức phạt tiền tối thiểu khi công ty vi phạm quản lý hạ tầng đường bộ là 10.000.000 đồng, tối đa là 14.000.000 đồng. Do đó, vi phạm quản lý hạ tầng đường bộ nặng hơn. (Điều 7, Khoản 2, Nghị định 336/2025/NĐ-CP; Điều 9, Khoản 5, Nghị định 336/2025/NĐ-CP)", "gold_units": ["ND336-2025/D7/K2", "ND336-2025/D9/K5"], "required_numbers": [{"value": 8000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}, {"value": 14000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-004:2"}
```

### WD-so_sanh-005 · tier A · vai: tài xế công nghệ · kiểu: ngan · cosine TF-IDF 0.44

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → 2027-12-31
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K3, ND168-2024/D21/K3/a, ND168-2024/D21/K3/b

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
3. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
a) Không sử dụng thẻ nhận dạng lái xe để đăng nhập thông tin theo quy định hoặc sử dụng thẻ nhận dạng lái xe của lái xe khác để đăng nhập thông tin khi điều khiển xe tham gia kinh doanh vận tải hàng hóa;
b) Điều khiển xe ô tô đầu kéo không lắp thiết bị ghi nhận hình ảnh người lái xe hoặc có lắp thiết bị ghi nhận hình ảnh người lái xe nhưng không có tác dụng trong quá trình xe tham gia giao thông theo quy định hoặc làm sai lệch dữ liệu của thiết bị ghi nhận hình ảnh người lái xe lắp trên xe ô tô.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D21/K13/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K13/a

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
13. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
a) Thực hiện hành vi quy định tại điểm b, điểm c, điểm đ khoản 2; điểm a khoản 3; khoản 4; khoản 5; điểm c, điểm d, điểm đ khoản 6 Điều này bị trừ điểm giấy phép lái xe (khi điều khiển xe ô tô) 02 điểm;

### Nguồn 2
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D26/K2, ND168-2024/D26/K2/a, ND168-2024/D26/K2/b, ND168-2024/D26/K2/c, ND168-2024/D26/K2/d, ND168-2024/D26/K2/đ, ND168-2024/D26/K2/e

Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
2. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với cá nhân, từ 2.000.000 đồng đến 4.000.000 đồng đối với tổ chức kinh doanh vận tải, dịch vụ hỗ trợ vận tải thực hiện một trong các hành vi vi phạm sau đây:
a) Không đánh số thứ tự ghế ngồi, giường nằm trên xe ô tô chở hành khách theo quy định;
b) Sử dụng xe ô tô kinh doanh vận tải hành khách theo tuyến cố định, xe ô tô kinh doanh vận tải hành khách bằng xe buýt không có chỗ ưu tiên cho người khuyết tật, người cao tuổi và phụ nữ mang thai theo quy định;
c) Sử dụng xe ô tô kinh doanh vận tải hành khách không có hướng dẫn cho hành khách về an toàn giao thông, thoát hiểm khi xảy ra sự cố trên xe theo quy định;
d) Không bố trí người áp tải trên xe vận chuyển hàng hóa nguy hiểm đối với những trường hợp quy định phải có người áp tải;
đ) Không cấp lệnh vận chuyển, giấy vận tải cho lái xe hoặc cấp lệnh vận chuyển, giấy vận tải nhưng không đúng theo quy định (đối với loại xe quy định phải cấp lệnh vận chuyển, giấy vận tải);
e) Sử dụng xe vận chuyển hàng hóa nguy hiểm mà không làm sạch hoặc không bóc (xóa) biểu trưng nguy hiểm trên phương tiện khi không tiếp tục vận chuyển loại hàng hóa đó.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D26/K12)
Mã điều khoản dùng được cho gold_units: ND168-2024/D26/K12

Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
12. Ngoài việc bị phạt tiền, cá nhân, tổ chức thực hiện hành vi vi phạm quy định tại điểm c khoản 2; điểm a, điểm b, điểm đ, điểm g khoản 4; điểm b, điểm c, điểm d, điểm đ, điểm e, điểm g khoản 7; điểm c khoản 8 Điều này còn bị áp dụng các hình thức xử phạt bổ sung tước quyền sử dụng phù hiệu từ 01 tháng đến 03 tháng (nếu có hoặc đã được cấp) đối với xe vi phạm.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D26/K14/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D26/K14/a

Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
14. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
a) Thực hiện hành vi quy định tại điểm đ khoản 2; điểm b, điểm c, điểm d khoản 6; điểm b, điểm c, điểm e, điểm i khoản 7 Điều này trong trường hợp cá nhân kinh doanh vận tải là người trực tiếp điều khiển phương tiện còn bị trừ điểm giấy phép lái xe 02 điểm;

[0] 1.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D21/K3)
[1] 2.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D21/K3)
[2] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D21/K13/a)
[3] 01 tháng (thời hạn tước quyền sử dụng tối thiểu, nêu tại ND168-2024/D26/K12)
[4] 03 tháng (thời hạn tước quyền sử dụng tối đa, nêu tại ND168-2024/D26/K12)
[5] 1.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D26/K2)
[6] 2.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D26/K2)
[7] 4.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D26/K2)
[8] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D26/K14/a)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Nếu tôi vi phạm không sử dụng thẻ nhận dạng lái xe khi điều khiển xe tải, mức phạt và điểm trừ sẽ như thế nào so với khi tôi không đánh số ghế trên xe ô tô chở hành khách?
- Đáp: Mức phạt tiền là từ 1.000.000 đồng đến 2.000.000 đồng và trừ 02 điểm giấy phép lái xe. Cả hai vi phạm đều có cùng mức phạt và điểm trừ.
- ⚠ chep_nguyen_van: “dụng thẻ nhận dạng lái xe …”
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-so_sanh-005", "question": "Nếu tôi vi phạm không sử dụng thẻ nhận dạng lái xe khi điều khiển xe tải, mức phạt và điểm trừ sẽ như thế nào so với khi tôi không đánh số ghế trên xe ô tô chở hành khách?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Mức phạt tiền là từ 1.000.000 đồng đến 2.000.000 đồng và trừ 02 điểm giấy phép lái xe. Cả hai vi phạm đều có cùng mức phạt và điểm trừ.", "gold_units": ["ND168-2024/D21/K3", "ND168-2024/D26/K2", "ND168-2024/D21/K13/a", "ND168-2024/D26/K12"], "required_numbers": [{"value": 1000000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-005:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Nếu tôi vi phạm không lắp thiết bị ghi hình người lái xe trên xe tải, mức phạt và điểm trừ sẽ như thế nào so với khi tôi không bố trí người áp tải trên xe vận chuyển hàng hóa nguy hiểm?
- Đáp: Mức phạt tiền là từ 1.000.000 đồng đến 2.000.000 đồng và trừ 02 điểm giấy phép lái xe. Cả hai vi phạm đều có cùng mức phạt và điểm trừ.
- ⚠ chep_nguyen_van: “bố trí người áp tải trên …”
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-so_sanh-005", "question": "Nếu tôi vi phạm không lắp thiết bị ghi hình người lái xe trên xe tải, mức phạt và điểm trừ sẽ như thế nào so với khi tôi không bố trí người áp tải trên xe vận chuyển hàng hóa nguy hiểm?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Mức phạt tiền là từ 1.000.000 đồng đến 2.000.000 đồng và trừ 02 điểm giấy phép lái xe. Cả hai vi phạm đều có cùng mức phạt và điểm trừ.", "gold_units": ["ND168-2024/D21/K3", "ND168-2024/D26/K2", "ND168-2024/D21/K13/a", "ND168-2024/D26/K12"], "required_numbers": [{"value": 1000000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-005:2"}
```

### WD-so_sanh-006 · tier A · vai: tài xế công nghệ · kiểu: tinh_huong_nguoi_khac · cosine TF-IDF 0.41

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2026-08-15 → 2027-12-31
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K5, ND168-2024/D20/K5/a, ND168-2024/D20/K5/b, ND168-2024/D20/K5/c, ND168-2024/D20/K5/d, ND168-2024/D20/K5/đ, ND168-2024/D20/K5/e, ND168-2024/D20/K5/g, ND168-2024/D20/K5/h, ND168-2024/D20/K5/i, ND168-2024/D20/K5/k, ND168-2024/D20/K5/l, ND168-2024/D20/K5/m

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
5. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
a) Để người lên, xuống xe khi xe đang chạy;
b) Xếp hành lý, hàng hóa trên xe làm lệch xe;
c) Đón, trả hành khách không đúng nơi quy định trên những tuyến đường đã xác định nơi đón, trả khách hoặc dừng đón, trả hành khách quá thời gian quy định, trừ hành vi vi phạm quy định tại khoản 8 Điều này;
d) Đón, trả hành khách tại nơi cấm dừng, cấm đỗ, nơi đường cong tầm nhìn bị che khuất, trừ hành vi vi phạm quy định tại khoản 8 Điều này;
đ) Điều khiển xe vận tải hành khách theo hợp đồng sử dụng hợp đồng bằng văn bản giấy mà không có hợp đồng vận tải, danh sách hành khách theo quy định; có hợp đồng vận tải nhưng không đúng theo quy định; đón khách, chở người không có tên trong danh sách hành khách theo hợp đồng đã ký;
e) Vận chuyển hành khách theo tuyến cố định không có hoặc không mang theo lệnh vận chuyển hoặc có mang theo lệnh vận chuyển nhưng không ghi đầy đủ thông tin, không có xác nhận của bến xe khách nơi đi, bến xe khách nơi đến theo quy định;
…

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D20/K10/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K10/a

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
10. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
a) Thực hiện hành vi quy định tại điểm c, điểm d, điểm e khoản 3; điểm a, điểm b, điểm c, điểm d, điểm đ, điểm e, điểm g, điểm h, điểm i, điểm k, điểm m khoản 5; khoản 6; khoản 7 Điều này bị trừ điểm giấy phép lái xe 02 điểm;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D20/K8)
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K8

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
8. Phạt tiền từ 10.000.000 đồng đến 12.000.000 đồng đối với người điều khiển xe thực hiện hành vi đón, trả hành khách trên đường cao tốc.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D37/K1/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D37/K1/b

Điều 37. Xử phạt người điều khiển phương tiện giao thông cơ giới đường bộ gắn biển số nước ngoài
1. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với người điều khiển phương tiện giao thông cơ giới đường bộ gắn biển số nước ngoài thực hiện một trong các hành vi vi phạm sau đây:
b) Điều khiển xe chở hành khách không có danh sách hành khách theo quy định.

### Nguồn 2
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D22/K1, ND168-2024/D22/K1/a, ND168-2024/D22/K1/b

Điều 22. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển hàng siêu trường, siêu trọng
1. Phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
a) Chở hàng siêu trường, siêu trọng không có báo hiệu kích thước của hàng theo quy định;
b) Không thực hiện đúng quy định trong giấy phép lưu hành, trừ các hành vi vi phạm quy định tại khoản 2; điểm b, điểm c, điểm d khoản 3 Điều này.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D22/K6/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D22/K6/a

Điều 22. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển hàng siêu trường, siêu trọng
6. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
a) Thực hiện hành vi quy định tại khoản 1 Điều này bị trừ điểm giấy phép lái xe 02 điểm;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D22/K2)
Mã điều khoản dùng được cho gold_units: ND168-2024/D22/K2

Điều 22. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển hàng siêu trường, siêu trọng
2. Phạt tiền từ 8.000.000 đồng đến 10.000.000 đồng đối với hành vi chở hàng siêu trường, siêu trọng có giấy phép lưu hành còn giá trị sử dụng nhưng kích thước bao ngoài của xe (sau khi đã xếp hàng lên xe) vượt quá quy định trong giấy phép lưu hành.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D22/K3/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D22/K3/b

Điều 22. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển hàng siêu trường, siêu trọng
3. Phạt tiền từ 13.000.000 đồng đến 15.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
b) Chở hàng siêu trường, siêu trọng có giấy phép lưu hành còn giá trị sử dụng nhưng tổng trọng lượng (sau khi đã xếp hàng lên xe) vượt quá quy định trong giấy phép lưu hành;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D22/K3/c)
Mã điều khoản dùng được cho gold_units: ND168-2024/D22/K3/c

Điều 22. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển hàng siêu trường, siêu trọng
3. Phạt tiền từ 13.000.000 đồng đến 15.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
c) Chở hàng siêu trường, siêu trọng có giấy phép lưu hành còn giá trị sử dụng nhưng đi không đúng tuyến đường quy định trong giấy phép lưu hành;

[0] 1.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D20/K5)
[1] 2.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D20/K5)
[2] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D20/K10/a)
[3] 2.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D22/K1)
[4] 3.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D22/K1)
[5] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D22/K6/a)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Anh tôi lái xe buýt chở khách, anh ấy hỏi so sánh mức phạt tiền và điểm trừ khi vi phạm quy định bảo đảm trật tự giao thông so với khi chở hàng siêu trường, siêu trọng.
- Đáp: Mức phạt tiền khi vi phạm quy định bảo đảm trật tự giao thông là từ 1.000.000 đồng đến 2.000.000 đồng, trừ 02 điểm. Mức phạt tiền khi chở hàng siêu trường, siêu trọng là từ 2.000.000 đồng đến 3.000.000 đồng, trừ 02 điểm. Do đó, mức phạt tiền cao hơn khi chở hàng siêu trường, siêu trọng, nhưng số điểm trừ là giống nhau.
- ⚠ chep_nguyen_van: “chở hàng siêu trường siêu trọng …”
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-so_sanh-006", "question": "Anh tôi lái xe buýt chở khách, anh ấy hỏi so sánh mức phạt tiền và điểm trừ khi vi phạm quy định bảo đảm trật tự giao thông so với khi chở hàng siêu trường, siêu trọng.", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Mức phạt tiền khi vi phạm quy định bảo đảm trật tự giao thông là từ 1.000.000 đồng đến 2.000.000 đồng, trừ 02 điểm. Mức phạt tiền khi chở hàng siêu trường, siêu trọng là từ 2.000.000 đồng đến 3.000.000 đồng, trừ 02 điểm. Do đó, mức phạt tiền cao hơn khi chở hàng siêu trường, siêu trọng, nhưng số điểm trừ là giống nhau.", "gold_units": ["ND168-2024/D20/K5", "ND168-2024/D20/K10/a", "ND168-2024/D22/K1", "ND168-2024/D22/K6/a"], "required_numbers": [{"value": 1000000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-006:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Công ty tôi vận hành xe buýt thường xuyên, công ty hỏi so sánh mức phạt khi đón, trả hành khách trên đường cao tốc với khi thực hiện trên đường thường.
- Đáp: Mức phạt tiền khi đón, trả hành khách trên đường cao tốc là từ 10.000.000 đồng đến 12.000.000 đồng, trừ 02 điểm. Mức phạt tiền khi thực hiện trên đường thường là từ 1.000.000 đồng đến 2.000.000 đồng, trừ 02 điểm. Vì vậy, mức phạt tiền cao hơn khi thực hiện trên đường cao tốc, nhưng số điểm trừ là giống nhau.
- ⚠ chep_nguyen_van: “hành khách trên đường cao tốc …”
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-so_sanh-006", "question": "Công ty tôi vận hành xe buýt thường xuyên, công ty hỏi so sánh mức phạt khi đón, trả hành khách trên đường cao tốc với khi thực hiện trên đường thường.", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Mức phạt tiền khi đón, trả hành khách trên đường cao tốc là từ 10.000.000 đồng đến 12.000.000 đồng, trừ 02 điểm. Mức phạt tiền khi thực hiện trên đường thường là từ 1.000.000 đồng đến 2.000.000 đồng, trừ 02 điểm. Vì vậy, mức phạt tiền cao hơn khi thực hiện trên đường cao tốc, nhưng số điểm trừ là giống nhau.", "gold_units": ["ND168-2024/D20/K5", "ND168-2024/D20/K8", "ND168-2024/D20/K10/a"], "required_numbers": [{"value": 1000000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-006:2"}
```

### WD-so_sanh-007 · tier A · vai: chủ doanh nghiệp vận tải · kiểu: neu_van_ban · cosine TF-IDF 0.43

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K4

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
4. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng trên mỗi người vượt quá quy định được phép chở của phương tiện nhưng tổng mức phạt tiền tối đa không vượt quá 75.000.000 đồng đối với người điều khiển xe ô tô chở hành khách (kinh doanh vận tải hành khách theo tuyến cố định, hợp đồng) chạy tuyến có cự ly lớn hơn 300 km thực hiện hành vi vi phạm chở quá số người quy định được phép chở của phương tiện.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D20/K10/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K10/b

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
10. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
b) Thực hiện hành vi quy định tại khoản 2, khoản 4 (trường hợp vượt trên 50% đến 100% số người quy định được phép chở của phương tiện) Điều này bị trừ điểm giấy phép lái xe 04 điểm;

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D20/K10/d)
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K10/d

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
10. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
d) Thực hiện hành vi quy định tại khoản 2, khoản 4 (trường hợp vượt trên 100% số người quy định được phép chở của phương tiện) Điều này bị trừ điểm giấy phép lái xe 10 điểm.

### Nguồn 2
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K15

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
15. Phạt tiền từ 30.000.000 đồng đến 40.000.000 đồng đối với cá nhân, từ 60.000.000 đồng đến 80.000.000 đồng đối với tổ chức là chủ xe ô tô, xe máy chuyên dùng và các loại xe tương tự xe ô tô khi giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại khoản 7 Điều 21 của Nghị định này hoặc trực tiếp điều khiển phương tiện thực hiện hành vi vi phạm quy định tại khoản 7 Điều 21 của Nghị định này.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K18/c)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K18/c

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
18. Ngoài việc bị phạt tiền, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị áp dụng các hình thức xử phạt bổ sung như sau:
c) Thực hiện hành vi quy định tại điểm e khoản 7, điểm b khoản 11, điểm a khoản 13, khoản 15, điểm b khoản 16 Điều này mà phương tiện đó có thùng xe, khối lượng hàng hóa cho phép chuyên chở không đúng theo quy định hiện hành thì còn bị tước quyền sử dụng chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường và tem kiểm định của phương tiện từ 01 tháng đến 03 tháng;

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K18/đ)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K18/đ

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
18. Ngoài việc bị phạt tiền, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị áp dụng các hình thức xử phạt bổ sung như sau:
đ) Thực hiện hành vi quy định tại khoản 5, khoản 6 Điều này trong trường hợp chở vượt trên 50% số người quy định được phép chở của phương tiện còn bị tước quyền sử dụng phù hiệu từ 01 tháng đến 03 tháng (nếu có). Thực hiện hành vi quy định tại điểm a, điểm b khoản 11; điểm a, điểm b, điểm c, điểm đ khoản 13; điểm a, điểm b, điểm c, điểm d, điểm đ, điểm e, điểm g khoản 14; khoản 15; khoản 16 Điều này còn bị tước quyền sử dụng phù hiệu từ 01 tháng đến 03 tháng (nếu có),

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K21/e)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K21/e

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
21. Ngoài việc bị áp dụng hình thức xử phạt, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
e) Thực hiện hành vi quy định tại khoản 15 Điều này trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện còn bị trừ điểm giấy phép lái xe 08 điểm;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D21/K7)
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K7

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
7. Phạt tiền từ 7.000.000 đồng đến 8.000.000 đồng đối với một trong các hành vi sau đây:

[0] 1.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D20/K4)
[1] 2.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D20/K4)
[2] 04 điểm (số điểm bị trừ, nêu tại ND168-2024/D20/K10/b)
[3] 10 điểm (số điểm bị trừ, nêu tại ND168-2024/D20/K10/d)
[4] 30.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D32/K15)
[5] 40.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D32/K15)
[6] 60.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D32/K15)
[7] 80.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D32/K15)
[8] 01 tháng (thời hạn tước quyền sử dụng tối thiểu, nêu tại ND168-2024/D32/K18/c)
[9] 03 tháng (thời hạn tước quyền sử dụng tối đa, nêu tại ND168-2024/D32/K18/c)
[10] 01 tháng (thời hạn tước quyền sử dụng tối thiểu, nêu tại ND168-2024/D32/K18/đ)
[11] 03 tháng (thời hạn tước quyền sử dụng tối đa, nêu tại ND168-2024/D32/K18/đ)
[12] 08 điểm (số điểm bị trừ, nêu tại ND168-2024/D32/K21/e)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Nếu công ty tôi chở quá số người quy định trên xe ô tô chở hành khách, mức phạt tiền và trừ điểm của người lái xe và của chủ xe là bao nhiêu? Ai nặng hơn?
- Đáp: Người lái xe bị phạt từ 1.000.000 đồng đến 2.000.000 đồng và trừ 4 điểm hoặc 10 điểm tùy theo mức vượt quá. Chủ xe bị phạt từ 30.000.000 đồng đến 40.000.000 đồng hoặc từ 60.000.000 đồng đến 80.000.000 đồng tùy theo tình huống. Vì mức phạt tiền và điểm trừ của chủ xe lớn hơn, nên nặng hơn người lái xe.
- ⚠ chep_nguyen_van: “chở quá số người quy định …”
- Ghi chú: Giả định rằng chủ xe là tổ chức

```json
{"qid": "tD-so_sanh-007", "question": "Nếu công ty tôi chở quá số người quy định trên xe ô tô chở hành khách, mức phạt tiền và trừ điểm của người lái xe và của chủ xe là bao nhiêu? Ai nặng hơn?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Người lái xe bị phạt từ 1.000.000 đồng đến 2.000.000 đồng và trừ 4 điểm hoặc 10 điểm tùy theo mức vượt quá. Chủ xe bị phạt từ 30.000.000 đồng đến 40.000.000 đồng hoặc từ 60.000.000 đồng đến 80.000.000 đồng tùy theo tình huống. Vì mức phạt tiền và điểm trừ của chủ xe lớn hơn, nên nặng hơn người lái xe.", "gold_units": ["ND168-2024/D20/K4", "ND168-2024/D20/K10/d", "ND168-2024/D32/K15"], "required_numbers": [{"value": 1000000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}, {"value": 4, "unit": "diem"}, {"value": 10, "unit": "diem"}, {"value": 30000000, "unit": "vnd"}, {"value": 40000000, "unit": "vnd"}, {"value": 60000000, "unit": "vnd"}, {"value": 80000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-007:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Nếu công ty tôi chở quá 100% số người quy định trên xe ô tô chở hành khách, mức phạt tiền và trừ điểm của người lái xe và của chủ xe là bao nhiêu? Ai nặng hơn?
- Đáp: Người lái xe bị phạt từ 1.000.000 đồng đến 2.000.000 đồng và trừ 10 điểm. Chủ xe bị phạt từ 30.000.000 đồng đến 40.000.000 đồng hoặc từ 60.000.000 đồng đến 80.000.000 đồng. Vì mức phạt tiền và điểm trừ của chủ xe lớn hơn, nên nặng hơn người lái xe.
- ⚠ chep_nguyen_van: “xe ô tô chở hành khách …”
- Ghi chú: Giả định rằng chủ xe là tổ chức

```json
{"qid": "tD-so_sanh-007", "question": "Nếu công ty tôi chở quá 100% số người quy định trên xe ô tô chở hành khách, mức phạt tiền và trừ điểm của người lái xe và của chủ xe là bao nhiêu? Ai nặng hơn?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Người lái xe bị phạt từ 1.000.000 đồng đến 2.000.000 đồng và trừ 10 điểm. Chủ xe bị phạt từ 30.000.000 đồng đến 40.000.000 đồng hoặc từ 60.000.000 đồng đến 80.000.000 đồng. Vì mức phạt tiền và điểm trừ của chủ xe lớn hơn, nên nặng hơn người lái xe.", "gold_units": ["ND168-2024/D20/K4", "ND168-2024/D20/K10/d", "ND168-2024/D32/K15"], "required_numbers": [{"value": 1000000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}, {"value": 4, "unit": "diem"}, {"value": 10, "unit": "diem"}, {"value": 30000000, "unit": "vnd"}, {"value": 40000000, "unit": "vnd"}, {"value": 60000000, "unit": "vnd"}, {"value": 80000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-007:2"}
```

### WD-so_sanh-008 · tier A · vai: cán bộ phường · kiểu: neu_van_ban · cosine TF-IDF 0.53

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D7/K6, ND168-2024/D7/K6/a, ND168-2024/D7/K6/b, ND168-2024/D7/K6/c, ND168-2024/D7/K6/d

Điều 7. Xử phạt, trừ điểm giấy phép lái của người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy vi phạm quy tắc giao thông đường bộ
6. Phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
a) Điều khiển xe trên đường mà trong máu hoặc hơi thở có nồng độ cồn nhưng chưa vượt quá 50 miligam/100 mililít máu hoặc chưa vượt quá 0,25 miligam/1 lít khí thở;
b) Đi vào khu vực cấm, đường có biển báo hiệu có nội dung cấm đi vào đối với loại phương tiện đang điều khiển, trừ các hành vi vi phạm quy định tại điểm a, điểm b khoản 7 Điều này và các trường hợp xe ưu tiên đang đi làm nhiệm vụ khẩn cấp theo quy định;
c) Không giảm tốc độ (hoặc dừng lại) và nhường đường khi điều khiển xe đi từ đường không ưu tiên ra đường ưu tiên, từ đường nhánh ra đường chính;
d) Không giảm tốc độ và nhường đường cho xe đi đến từ bên phải tại nơi đường giao nhau không có báo hiệu đi theo vòng xuyến; không giảm tốc độ và nhường đường cho xe đi đến từ bên trái tại nơi đường giao nhau có báo hiệu đi theo vòng xuyến.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D7/K13/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D7/K13/a

Điều 7. Xử phạt, trừ điểm giấy phép lái của người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy vi phạm quy tắc giao thông đường bộ
13. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển xe thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
a) Thực hiện hành vi quy định tại điểm b khoản 3; khoản 5; điểm b, điểm c, điểm d khoản 6; điểm a khoản 7 Điều này bị trừ điểm giấy phép lái xe 02 điểm;

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D7/K13/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D7/K13/b

Điều 7. Xử phạt, trừ điểm giấy phép lái của người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy vi phạm quy tắc giao thông đường bộ
13. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển xe thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
b) Thực hiện hành vi quy định tại điểm đ khoản 4; điểm a khoản 6; điểm c, điểm d, điểm đ khoản 7; điểm a khoản 8 Điều này bị trừ điểm giấy phép lái xe 04 điểm;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D7/K7/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D7/K7/a

Điều 7. Xử phạt, trừ điểm giấy phép lái của người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy vi phạm quy tắc giao thông đường bộ
7. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
a) Đi ngược chiều của đường một chiều, đi ngược chiều trên đường có biển “Cấm đi ngược chiều”, trừ hành vi vi phạm quy định tại điểm b khoản này và các trường hợp xe ưu tiên đang đi làm nhiệm vụ khẩn cấp theo quy định; điều khiển xe đi trên vỉa hè, trừ trường hợp điều khiển xe đi qua vỉa hè để vào nhà, cơ quan;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D7/K7/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D7/K7/b

Điều 7. Xử phạt, trừ điểm giấy phép lái của người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy vi phạm quy tắc giao thông đường bộ
7. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
b) Điều khiển xe đi vào đường cao tốc, trừ xe phục vụ việc quản lý, bảo trì đường cao tốc;

### Nguồn 2
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D8/K9, ND168-2024/D8/K9/a, ND168-2024/D8/K9/b, ND168-2024/D8/K9/c, ND168-2024/D8/K9/d, ND168-2024/D8/K9/đ, ND168-2024/D8/K9/e

Điều 8. Xử phạt người điều khiển xe máy chuyên dùng vi phạm quy tắc giao thông đường bộ
9. Phạt tiền từ 18.000.000 đồng đến 20.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
a) Điều khiển xe trên đường mà trong máu hoặc hơi thở có nồng độ cồn vượt quá 80 miligam/100 mililít máu hoặc vượt quá 0,4 miligam/1 lít khí thở;
b) Không chấp hành yêu cầu kiểm tra về nồng độ cồn của người thi hành công vụ;
c) Điều khiển xe trên đường mà trong cơ thể có chất ma túy hoặc chất kích thích khác mà pháp luật cấm sử dụng;
d) Không chấp hành yêu cầu kiểm tra về chất ma túy hoặc chất kích thích khác mà pháp luật cấm sử dụng của người thi hành công vụ;
đ) Lùi xe trên đường cao tốc; đi ngược chiều trên đường cao tốc; quay đầu xe trên đường cao tốc;
e) Vi phạm quy định tại điểm b khoản 8 Điều này mà gây tai nạn giao thông.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D8/K8/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D8/K8/b

Điều 8. Xử phạt người điều khiển xe máy chuyên dùng vi phạm quy tắc giao thông đường bộ
8. Phạt tiền từ 14.000.000 đồng đến 16.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
b) Điều khiển xe máy chuyên dùng có tốc độ thiết kế nhỏ hơn tốc độ tối thiểu quy định đối với đường cao tốc đi vào đường cao tốc, trừ phương tiện, thiết bị phục vụ việc quản lý, bảo trì đường cao tốc;

[0] 2.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D7/K6)
[1] 3.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D7/K6)
[2] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D7/K13/a)
[3] 04 điểm (số điểm bị trừ, nêu tại ND168-2024/D7/K13/b)
[4] 18.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D8/K9)
[5] 20.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D8/K9)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Theo Nghị định 168/2024/NĐ-CP, nếu tôi lái xe máy bình thường với nồng độ cồn 30 mg/100ml và lái xe máy chuyên dùng với nồng độ cồn 90 mg/100ml, mức phạt tiền và điểm trừ sẽ khác nhau không?
- Đáp: Nếu lái xe máy bình thường với nồng độ cồn 30 mg/100ml, mức phạt tiền là từ 2.000.000 đồng đến 3.000.000 đồng và trừ 02 điểm. Nếu lái xe máy chuyên dùng với nồng độ cồn 90 mg/100ml, mức phạt tiền là từ 18.000.000 đồng đến 20.000.000 đồng và trừ 04 điểm. Do đó, người điều khiển xe máy chuyên dùng bị phạt nặng hơn.
- ⚠ so_la: 30, 90
- Ghi chú: Xe máy bình thường là xe mô tô, xe máy chuyên dùng là xe gắn máy chuyên dùng

```json
{"qid": "tD-so_sanh-008", "question": "Theo Nghị định 168/2024/NĐ-CP, nếu tôi lái xe máy bình thường với nồng độ cồn 30 mg/100ml và lái xe máy chuyên dùng với nồng độ cồn 90 mg/100ml, mức phạt tiền và điểm trừ sẽ khác nhau không?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Nếu lái xe máy bình thường với nồng độ cồn 30 mg/100ml, mức phạt tiền là từ 2.000.000 đồng đến 3.000.000 đồng và trừ 02 điểm. Nếu lái xe máy chuyên dùng với nồng độ cồn 90 mg/100ml, mức phạt tiền là từ 18.000.000 đồng đến 20.000.000 đồng và trừ 04 điểm. Do đó, người điều khiển xe máy chuyên dùng bị phạt nặng hơn.", "gold_units": ["ND168-2024/D7/K6", "ND168-2024/D7/K13/a", "ND168-2024/D8/K9", "ND168-2024/D8/K9/a"], "required_numbers": [{"value": 2000000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}, {"value": 4, "unit": "diem"}, {"value": 18000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-008:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Theo Nghị định 168/2024/NĐ-CP, khi lái xe máy bình thường đi ngược chiều đường một chiều và khi lái xe máy chuyên dùng vào đường cao tốc, mức phạt tiền và điểm trừ sẽ khác nhau không?
- Đáp: Lái xe máy bình thường đi ngược chiều đường một chiều bị phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng và trừ 02 điểm. Lái xe máy chuyên dùng vào đường cao tốc bị phạt tiền từ 14.000.000 đồng đến 16.000.000 đồng và trừ 04 điểm. Vì vậy, người điều khiển xe máy chuyên dùng bị phạt nặng hơn.
- Ghi chú: Xe máy bình thường là xe mô tô, xe máy chuyên dùng là xe gắn máy chuyên dùng

```json
{"qid": "tD-so_sanh-008", "question": "Theo Nghị định 168/2024/NĐ-CP, khi lái xe máy bình thường đi ngược chiều đường một chiều và khi lái xe máy chuyên dùng vào đường cao tốc, mức phạt tiền và điểm trừ sẽ khác nhau không?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Lái xe máy bình thường đi ngược chiều đường một chiều bị phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng và trừ 02 điểm. Lái xe máy chuyên dùng vào đường cao tốc bị phạt tiền từ 14.000.000 đồng đến 16.000.000 đồng và trừ 04 điểm. Vì vậy, người điều khiển xe máy chuyên dùng bị phạt nặng hơn.", "gold_units": ["ND168-2024/D7/K7/a", "ND168-2024/D7/K13/a", "ND168-2024/D8/K8/b"], "required_numbers": [{"value": 2000000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}, {"value": 4, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-008:2"}
```

### WD-so_sanh-009 · tier A · vai: phụ huynh có con dưới 18 tuổi · kiểu: tinh_huong_nguoi_khac · cosine TF-IDF 0.71

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K7

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
7. Phạt tiền từ 5.000.000 đồng đến 7.000.000 đồng đối với hành vi vi phạm điều khiển xe chở hành khách không có hoặc không gắn phù hiệu theo quy định hoặc có nhưng đã hết giá trị sử dụng hoặc sử dụng phù hiệu không do cơ quan có thẩm quyền cấp.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D20/K10/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K10/a

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
10. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
a) Thực hiện hành vi quy định tại điểm c, điểm d, điểm e khoản 3; điểm a, điểm b, điểm c, điểm d, điểm đ, điểm e, điểm g, điểm h, điểm i, điểm k, điểm m khoản 5; khoản 6; khoản 7 Điều này bị trừ điểm giấy phép lái xe 02 điểm;

### Nguồn 2
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D28/K2

Điều 28. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ
2. Phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng đối với hành vi điều khiển xe chở người bốn bánh có gắn động cơ kinh doanh vận tải, xe chở hàng bốn bánh có gắn động cơ kinh doanh vận tải không có hoặc không gắn phù hiệu theo quy định hoặc có nhưng đã hết giá trị sử dụng hoặc sử dụng phù hiệu không do cơ quan có thẩm quyền cấp.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D28/K4/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D28/K4/a

Điều 28. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ
4. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
a) Thực hiện hành vi quy định tại khoản 2 Điều này bị trừ điểm giấy phép lái xe 02 điểm;

[0] 5.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D20/K7)
[1] 7.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D20/K7)
[2] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D20/K10/a)
[3] 2.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D28/K2)
[4] 3.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D28/K2)
[5] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D28/K4/a)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Anh tôi đang lái xe ô tô chở hành khách, còn anh bạn của tôi lái xe chở người bốn bánh. Nếu cả hai đều không gắn phù hiệu, mức phạt tiền và điểm trừ của họ có khác nhau không?
- Đáp: Nếu vi phạm không có phù hiệu, người điều khiển xe ô tô chở hành khách bị phạt từ 5.000.000 đồng đến 7.000.000 đồng và trừ 02 điểm. Trong khi đó, người điều khiển xe chở người bốn bánh bị phạt từ 2.000.000 đồng đến 3.000.000 đồng và trừ 02 điểm. Do đó, mức phạt tiền của xe ô tô chở hành khách cao hơn.
- ⚠ chep_nguyen_van: “xe ô tô chở hành khách …”
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-so_sanh-009", "question": "Anh tôi đang lái xe ô tô chở hành khách, còn anh bạn của tôi lái xe chở người bốn bánh. Nếu cả hai đều không gắn phù hiệu, mức phạt tiền và điểm trừ của họ có khác nhau không?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Nếu vi phạm không có phù hiệu, người điều khiển xe ô tô chở hành khách bị phạt từ 5.000.000 đồng đến 7.000.000 đồng và trừ 02 điểm. Trong khi đó, người điều khiển xe chở người bốn bánh bị phạt từ 2.000.000 đồng đến 3.000.000 đồng và trừ 02 điểm. Do đó, mức phạt tiền của xe ô tô chở hành khách cao hơn.", "gold_units": ["ND168-2024/D20/K7", "ND168-2024/D20/K10/a", "ND168-2024/D28/K2", "ND168-2024/D28/K4/a"], "required_numbers": [{"value": 5000000, "unit": "vnd"}, {"value": 7000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}, {"value": 2000000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-009:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Con tôi thường đi học bằng xe chở hành khách, còn anh em của tôi đi bằng xe chở người bốn bánh. Nếu cả hai không gắn phù hiệu, mức phạt tiền và điểm trừ của họ sẽ như thế nào?
- Đáp: Nếu vi phạm không có phù hiệu, người điều khiển xe ô tô chở hành khách bị phạt từ 5.000.000 đồng đến 7.000.000 đồng và trừ 02 điểm. Trong khi đó, người điều khiển xe chở người bốn bánh bị phạt từ 2.000.000 đồng đến 3.000.000 đồng và trừ 02 điểm. Do đó, mức phạt tiền của xe ô tô chở hành khách cao hơn.
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-so_sanh-009", "question": "Con tôi thường đi học bằng xe chở hành khách, còn anh em của tôi đi bằng xe chở người bốn bánh. Nếu cả hai không gắn phù hiệu, mức phạt tiền và điểm trừ của họ sẽ như thế nào?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Nếu vi phạm không có phù hiệu, người điều khiển xe ô tô chở hành khách bị phạt từ 5.000.000 đồng đến 7.000.000 đồng và trừ 02 điểm. Trong khi đó, người điều khiển xe chở người bốn bánh bị phạt từ 2.000.000 đồng đến 3.000.000 đồng và trừ 02 điểm. Do đó, mức phạt tiền của xe ô tô chở hành khách cao hơn.", "gold_units": ["ND168-2024/D20/K7", "ND168-2024/D20/K10/a", "ND168-2024/D28/K2", "ND168-2024/D28/K4/a"], "required_numbers": [{"value": 5000000, "unit": "vnd"}, {"value": 7000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}, {"value": 2000000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-009:2"}
```

### WD-so_sanh-010 · tier A · vai: tài xế công nghệ · kiểu: ngan · cosine TF-IDF 0.40

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K8

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
8. Phạt tiền từ 10.000.000 đồng đến 12.000.000 đồng đối với người điều khiển xe thực hiện hành vi đón, trả hành khách trên đường cao tốc.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D20/K10/c)
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K10/c

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
10. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
c) Thực hiện hành vi vi phạm quy định tại khoản 8, khoản 8a Điều này bị trừ điểm giấy phép lái xe 06 điểm;

### Nguồn 2
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D7/K7, ND168-2024/D7/K7/a, ND168-2024/D7/K7/b, ND168-2024/D7/K7/c, ND168-2024/D7/K7/d, ND168-2024/D7/K7/đ

Điều 7. Xử phạt, trừ điểm giấy phép lái của người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy vi phạm quy tắc giao thông đường bộ
7. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
a) Đi ngược chiều của đường một chiều, đi ngược chiều trên đường có biển “Cấm đi ngược chiều”, trừ hành vi vi phạm quy định tại điểm b khoản này và các trường hợp xe ưu tiên đang đi làm nhiệm vụ khẩn cấp theo quy định; điều khiển xe đi trên vỉa hè, trừ trường hợp điều khiển xe đi qua vỉa hè để vào nhà, cơ quan;
b) Điều khiển xe đi vào đường cao tốc, trừ xe phục vụ việc quản lý, bảo trì đường cao tốc;
c) Không chấp hành hiệu lệnh của đèn tín hiệu giao thông;
d) Không chấp hành hiệu lệnh, hướng dẫn của người điều khiển giao thông hoặc người kiểm soát giao thông;
đ) Không nhường đường hoặc gây cản trở xe được quyền ưu tiên đang phát tín hiệu ưu tiên đi làm nhiệm vụ.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D7/K13/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D7/K13/a

Điều 7. Xử phạt, trừ điểm giấy phép lái của người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy vi phạm quy tắc giao thông đường bộ
13. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển xe thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
a) Thực hiện hành vi quy định tại điểm b khoản 3; khoản 5; điểm b, điểm c, điểm d khoản 6; điểm a khoản 7 Điều này bị trừ điểm giấy phép lái xe 02 điểm;

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D7/K13/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D7/K13/b

Điều 7. Xử phạt, trừ điểm giấy phép lái của người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy vi phạm quy tắc giao thông đường bộ
13. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển xe thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
b) Thực hiện hành vi quy định tại điểm đ khoản 4; điểm a khoản 6; điểm c, điểm d, điểm đ khoản 7; điểm a khoản 8 Điều này bị trừ điểm giấy phép lái xe 04 điểm;

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D7/K13/c)
Mã điều khoản dùng được cho gold_units: ND168-2024/D7/K13/c

Điều 7. Xử phạt, trừ điểm giấy phép lái của người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy vi phạm quy tắc giao thông đường bộ
13. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển xe thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
c) Thực hiện hành vi quy định tại điểm b khoản 7, điểm c khoản 9 Điều này bị trừ điểm giấy phép lái xe 06 điểm;

[0] 10.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D20/K8)
[1] 12.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D20/K8)
[2] 06 điểm (số điểm bị trừ, nêu tại ND168-2024/D20/K10/c)
[3] 4.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D7/K7)
[4] 6.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D7/K7)
[5] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D7/K13/a)
[6] 04 điểm (số điểm bị trừ, nêu tại ND168-2024/D7/K13/b)
[7] 06 điểm (số điểm bị trừ, nêu tại ND168-2024/D7/K13/c)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Nếu tôi lái xe ô tô chở hành khách đón khách trên đường cao tốc, còn tôi lái xe mô tô đi vào đường cao tốc, mức phạt tiền và điểm trừ giấy phép sẽ khác nhau như thế nào?
- Đáp: Lái xe ô tô chở hành khách đón khách trên đường cao tốc bị phạt từ 10.000.000 đồng đến 12.000.000 đồng và trừ 06 điểm. Lái xe mô tô đi vào đường cao tốc bị phạt từ 4.000.000 đồng đến 6.000.000 đồng và trừ 02 điểm. Vì vậy, ô tô chở hành khách bị phạt tiền cao hơn và trừ điểm nhiều hơn so với xe mô tô.
- ⚠ chep_nguyen_van: “xe ô tô chở hành khách …”

```json
{"qid": "tD-so_sanh-010", "question": "Nếu tôi lái xe ô tô chở hành khách đón khách trên đường cao tốc, còn tôi lái xe mô tô đi vào đường cao tốc, mức phạt tiền và điểm trừ giấy phép sẽ khác nhau như thế nào?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Lái xe ô tô chở hành khách đón khách trên đường cao tốc bị phạt từ 10.000.000 đồng đến 12.000.000 đồng và trừ 06 điểm. Lái xe mô tô đi vào đường cao tốc bị phạt từ 4.000.000 đồng đến 6.000.000 đồng và trừ 02 điểm. Vì vậy, ô tô chở hành khách bị phạt tiền cao hơn và trừ điểm nhiều hơn so với xe mô tô.", "gold_units": ["ND168-2024/D20/K8", "ND168-2024/D20/K10/c", "ND168-2024/D7/K7", "ND168-2024/D7/K13/a"], "required_numbers": [{"value": 10000000, "unit": "vnd"}, {"value": 12000000, "unit": "vnd"}, {"value": 6, "unit": "diem"}, {"value": 4000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-010:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Khi tôi lái xe ô tô chở hành khách đón khách trên đường cao tốc và khi tôi lái xe mô tô đi vào đường cao tốc, mức phạt tiền và điểm trừ giấy phép sẽ khác nhau như thế nào?
- Đáp: Lái xe ô tô chở hành khách đón khách trên đường cao tốc bị phạt từ 10.000.000 đồng đến 12.000.000 đồng và trừ 06 điểm. Lái xe mô tô đi vào đường cao tốc bị phạt từ 4.000.000 đồng đến 6.000.000 đồng và trừ 02 điểm. Vì vậy, ô tô chở hành khách bị phạt tiền cao hơn và trừ điểm nhiều hơn so với xe mô tô.
- ⚠ chep_nguyen_van: “xe ô tô chở hành khách …”

```json
{"qid": "tD-so_sanh-010", "question": "Khi tôi lái xe ô tô chở hành khách đón khách trên đường cao tốc và khi tôi lái xe mô tô đi vào đường cao tốc, mức phạt tiền và điểm trừ giấy phép sẽ khác nhau như thế nào?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Lái xe ô tô chở hành khách đón khách trên đường cao tốc bị phạt từ 10.000.000 đồng đến 12.000.000 đồng và trừ 06 điểm. Lái xe mô tô đi vào đường cao tốc bị phạt từ 4.000.000 đồng đến 6.000.000 đồng và trừ 02 điểm. Vì vậy, ô tô chở hành khách bị phạt tiền cao hơn và trừ điểm nhiều hơn so với xe mô tô.", "gold_units": ["ND168-2024/D20/K8", "ND168-2024/D20/K10/c", "ND168-2024/D7/K7", "ND168-2024/D7/K13/a"], "required_numbers": [{"value": 10000000, "unit": "vnd"}, {"value": 12000000, "unit": "vnd"}, {"value": 6, "unit": "diem"}, {"value": 4000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-010:2"}
```

### WD-so_sanh-011 · tier A · vai: tài xế xe tải · kiểu: ngan · cosine TF-IDF 0.55

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D12/K5, ND168-2024/D12/K5/a, ND168-2024/D12/K5/b

Điều 12. Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm khác về quy tắc giao thông đường bộ; sử dụng lòng đường, vỉa hè vào mục đích khác
5. Phạt tiền từ 400.000 đồng đến 600.000 đồng đối với người được chở trên xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô, các loại xe tương tự xe gắn máy thực hiện một trong các hành vi vi phạm sau đây:
a) Bám, kéo, đẩy xe khác, vật khác, dẫn dắt vật nuôi, mang vác vật cồng kềnh, đứng trên yên, giá đèo hàng hoặc ngồi trên tay lái của xe;
b) Không đội “mũ bảo hiểm cho người đi mô tô, xe máy” hoặc đội “mũ bảo hiểm cho người đi mô tô, xe máy” không cài quai đúng quy cách khi tham gia giao thông trên đường bộ.

### Nguồn 2
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K4

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
4. Phạt tiền từ 800.000 đồng đến 1.000.000 đồng đối với cá nhân, từ 1.600.000 đồng đến 2.000.000 đồng đối với tổ chức là chủ xe mô tô, xe gắn máy và các loại xe tương tự xe mô tô, các loại xe tương tự xe gắn máy không thực hiện đúng quy định về biển số, trừ các hành vi vi phạm quy định tại điểm g, điểm h khoản 8 Điều này.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D32/K8/g)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K8/g

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
8. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng đối với cá nhân, từ 8.000.000 đến 12.000.000 đồng đối với tổ chức là chủ xe mô tô, xe gắn máy và các loại xe tương tự xe mô tô, các loại xe tương tự xe gắn máy thực hiện một trong các hành vi vi phạm sau đây:
g) Lắp đặt, sử dụng thiết bị thay đổi biển số trên xe trái quy định;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D32/K8/h)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K8/h

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
8. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng đối với cá nhân, từ 8.000.000 đến 12.000.000 đồng đối với tổ chức là chủ xe mô tô, xe gắn máy và các loại xe tương tự xe mô tô, các loại xe tương tự xe gắn máy thực hiện một trong các hành vi vi phạm sau đây:
h) Đưa phương tiện không gắn biển số (đối với loại xe có quy định phải gắn biển số) tham gia giao thông; đưa phương tiện gắn biển số không đúng với chứng nhận đăng ký xe hoặc gắn biển số không do cơ quan có thẩm quyền cấp tham gia giao thông.

[0] 400.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D12/K5)
[1] 600.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D12/K5)
[2] 800.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D32/K4)
[3] 1.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D32/K4)
[4] 1.600.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D32/K4)
[5] 2.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D32/K4)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): So sánh mức phạt tiền khi tôi lái xe máy không đội mũ bảo hiểm và khi chủ xe máy không gắn biển số đúng quy định.
- Đáp: Nếu tôi lái xe máy không đội mũ bảo hiểm, mức phạt tiền là từ 400.000 đồng đến 600.000 đồng. Nếu chủ xe máy không gắn biển số đúng quy định, mức phạt tiền là từ 800.000 đồng đến 1.000.000 đồng. Do đó, người chủ xe bị phạt nặng hơn.
- Ghi chú: xe máy là xe mô tô

```json
{"qid": "tD-so_sanh-011", "question": "So sánh mức phạt tiền khi tôi lái xe máy không đội mũ bảo hiểm và khi chủ xe máy không gắn biển số đúng quy định.", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Nếu tôi lái xe máy không đội mũ bảo hiểm, mức phạt tiền là từ 400.000 đồng đến 600.000 đồng. Nếu chủ xe máy không gắn biển số đúng quy định, mức phạt tiền là từ 800.000 đồng đến 1.000.000 đồng. Do đó, người chủ xe bị phạt nặng hơn.", "gold_units": ["ND168-2024/D12/K5", "ND168-2024/D32/K4"], "required_numbers": [{"value": 400000, "unit": "vnd"}, {"value": 600000, "unit": "vnd"}, {"value": 800000, "unit": "vnd"}, {"value": 1000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-011:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Nếu tôi lái xe máy không đội mũ bảo hiểm, mức phạt tiền là bao nhiêu? Nếu chủ xe máy không gắn biển số đúng quy định thì mức phạt tiền là bao nhiêu?
- Đáp: Nếu tôi lái xe máy không đội mũ bảo hiểm, mức phạt tiền là từ 400.000 đồng đến 600.000 đồng. Nếu chủ xe máy không gắn biển số đúng quy định, mức phạt tiền là từ 800.000 đồng đến 1.000.000 đồng. Người chủ xe bị phạt nặng hơn.
- Ghi chú: xe máy là xe mô tô

```json
{"qid": "tD-so_sanh-011", "question": "Nếu tôi lái xe máy không đội mũ bảo hiểm, mức phạt tiền là bao nhiêu? Nếu chủ xe máy không gắn biển số đúng quy định thì mức phạt tiền là bao nhiêu?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Nếu tôi lái xe máy không đội mũ bảo hiểm, mức phạt tiền là từ 400.000 đồng đến 600.000 đồng. Nếu chủ xe máy không gắn biển số đúng quy định, mức phạt tiền là từ 800.000 đồng đến 1.000.000 đồng. Người chủ xe bị phạt nặng hơn.", "gold_units": ["ND168-2024/D12/K5", "ND168-2024/D32/K4"], "required_numbers": [{"value": 400000, "unit": "vnd"}, {"value": 600000, "unit": "vnd"}, {"value": 800000, "unit": "vnd"}, {"value": 1000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-011:2"}
```

### WD-so_sanh-012 · tier A · vai: cán bộ phường · kiểu: tinh_huong_ban_than · cosine TF-IDF 0.41

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K6

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
6. Phạt tiền từ 2.000.000 đồng đến 4.000.000 đồng trên mỗi người vượt quá quy định được phép chở của phương tiện nhưng tổng mức phạt tiền tối đa không vượt quá 75.000.000 đồng đối với chủ phương tiện là cá nhân, từ 4.000.000 đồng đến 8.000.000 đồng trên mỗi người vượt quá quy định được phép chở của phương tiện nhưng tổng mức phạt tiền tối đa không vượt quá 150.000.000 đồng đối với chủ phương tiện là tổ chức giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại khoản 4 Điều 20 của Nghị định này hoặc trực tiếp điều khiển phương tiện thực hiện hành vi vi phạm quy định tại khoản 4 Điều 20 của Nghị định này.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K18/đ)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K18/đ

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
18. Ngoài việc bị phạt tiền, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị áp dụng các hình thức xử phạt bổ sung như sau:
đ) Thực hiện hành vi quy định tại khoản 5, khoản 6 Điều này trong trường hợp chở vượt trên 50% số người quy định được phép chở của phương tiện còn bị tước quyền sử dụng phù hiệu từ 01 tháng đến 03 tháng (nếu có). Thực hiện hành vi quy định tại điểm a, điểm b khoản 11; điểm a, điểm b, điểm c, điểm đ khoản 13; điểm a, điểm b, điểm c, điểm d, điểm đ, điểm e, điểm g khoản 14; khoản 15; khoản 16 Điều này còn bị tước quyền sử dụng phù hiệu từ 01 tháng đến 03 tháng (nếu có),

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K21/d)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K21/d

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
21. Ngoài việc bị áp dụng hình thức xử phạt, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
d) Thực hiện hành vi quy định tại khoản 5, khoản 6 Điều này trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện chở vượt trên 50% đến 100% số người quy định được phép chở của phương tiện, còn bị trừ điểm giấy phép lái xe 04 điểm;

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K21/h)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K21/h

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
21. Ngoài việc bị áp dụng hình thức xử phạt, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
h) Thực hiện hành vi quy định tại khoản 5, khoản 6 Điều này trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện chở vượt trên 100% số người quy định được phép chở của phương tiện còn bị trừ điểm giấy phép lái xe 10 điểm.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D20/K4)
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K4

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
4. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng trên mỗi người vượt quá quy định được phép chở của phương tiện nhưng tổng mức phạt tiền tối đa không vượt quá 75.000.000 đồng đối với người điều khiển xe ô tô chở hành khách (kinh doanh vận tải hành khách theo tuyến cố định, hợp đồng) chạy tuyến có cự ly lớn hơn 300 km thực hiện hành vi vi phạm chở quá số người quy định được phép chở của phương tiện.

### Nguồn 2
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D35/K2

Điều 35. Xử phạt, trừ điểm giấy phép lái xe đối với người đua xe trái phép, tổ chức đua xe, xúi giục, cổ vũ đua xe trái phép
2. Phạt tiền từ 40.000.000 đồng đến 50.000.000 đồng đối với cá nhân, từ 80.000.000 đồng đến 100.000.000 đồng đối với tổ chức thực hiện hành vi vi phạm tổ chức đua xe trái phép.

[0] 01 tháng (thời hạn tước quyền sử dụng tối thiểu, nêu tại ND168-2024/D32/K18/đ)
[1] 03 tháng (thời hạn tước quyền sử dụng tối đa, nêu tại ND168-2024/D32/K18/đ)
[2] 2.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D32/K6)
[3] 4.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D32/K6)
[4] 04 điểm (số điểm bị trừ, nêu tại ND168-2024/D32/K21/d)
[5] 10 điểm (số điểm bị trừ, nêu tại ND168-2024/D32/K21/h)
[6] 40.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D35/K2)
[7] 50.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D35/K2)
[8] 80.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D35/K2)
[9] 100.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D35/K2)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là cán bộ phường, khi một xe tải cá nhân chở quá số người quy định và một xe tải công ty chở quá số người quy định, mức phạt tiền và trừ điểm của hai trường hợp này có khác nhau không?
- Đáp: Mức phạt tiền cho người chở quá số người là từ 2.000.000 đồng đến 4.000.000 đồng trên mỗi người vượt quá quy định, tổng mức phạt tối đa 75.000.000 đồng. Mức phạt tiền cho công ty chở quá số người là từ 4.000.000 đồng đến 8.000.000 đồng trên mỗi người vượt quá quy định, tổng mức phạt tối đa 150.000.000 đồng. Nếu người chở vượt quá 50% số người quy định, trừ điểm là 04 điểm. Nếu người chở vượt quá 100% số người quy định, trừ điểm là 10 điểm. (khoản 6, 21 d, h Điều 32 Nghị định 168/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “chở quá số người quy định …”

```json
{"qid": "tD-so_sanh-012", "question": "Tôi là cán bộ phường, khi một xe tải cá nhân chở quá số người quy định và một xe tải công ty chở quá số người quy định, mức phạt tiền và trừ điểm của hai trường hợp này có khác nhau không?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Mức phạt tiền cho người chở quá số người là từ 2.000.000 đồng đến 4.000.000 đồng trên mỗi người vượt quá quy định, tổng mức phạt tối đa 75.000.000 đồng. Mức phạt tiền cho công ty chở quá số người là từ 4.000.000 đồng đến 8.000.000 đồng trên mỗi người vượt quá quy định, tổng mức phạt tối đa 150.000.000 đồng. Nếu người chở vượt quá 50% số người quy định, trừ điểm là 04 điểm. Nếu người chở vượt quá 100% số người quy định, trừ điểm là 10 điểm. (khoản 6, 21 d, h Điều 32 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D32/K6", "ND168-2024/D32/K21/d"], "required_numbers": [{"value": 2000000, "unit": "vnd"}, {"value": 4000000, "unit": "vnd"}, {"value": 4, "unit": "diem"}, {"value": 10, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-012:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là cán bộ phường, khi một cá nhân tổ chức đua xe trái phép và một tổ chức tổ chức đua xe trái phép, mức phạt tiền của hai trường hợp này có khác nhau không?
- Đáp: Mức phạt tiền cho cá nhân tổ chức đua xe trái phép là từ 40.000.000 đồng đến 50.000.000 đồng. Mức phạt tiền cho tổ chức tổ chức đua xe trái phép là từ 80.000.000 đồng đến 100.000.000 đồng. (khoản 2 Điều 35 Nghị định 168/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “tổ chức đua xe trái phép …”

```json
{"qid": "tD-so_sanh-012", "question": "Tôi là cán bộ phường, khi một cá nhân tổ chức đua xe trái phép và một tổ chức tổ chức đua xe trái phép, mức phạt tiền của hai trường hợp này có khác nhau không?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Mức phạt tiền cho cá nhân tổ chức đua xe trái phép là từ 40.000.000 đồng đến 50.000.000 đồng. Mức phạt tiền cho tổ chức tổ chức đua xe trái phép là từ 80.000.000 đồng đến 100.000.000 đồng. (khoản 2 Điều 35 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D35/K2"], "required_numbers": [{"value": 40000000, "unit": "vnd"}, {"value": 50000000, "unit": "vnd"}, {"value": 80000000, "unit": "vnd"}, {"value": 100000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-012:2"}
```

### WD-so_sanh-013 · tier A · vai: phụ huynh có con dưới 18 tuổi · kiểu: ngan · cosine TF-IDF 0.49

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D13/K7, ND168-2024/D13/K7/a, ND168-2024/D13/K7/b

Điều 13. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo), xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tư xe ô tô vi phạm quy định về điều kiện của phương tiện khi tham gia giao thông
7. Phạt tiền từ 10.000.000 đồng đến 12.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
a) Điều khiển xe đăng ký tạm thời, xe có phạm vi hoạt động hạn chế hoạt động quá phạm vi, tuyến đường, thời hạn cho phép;
b) Điều khiển xe (kể cả rơ moóc và sơ mi rơ moóc) không gắn biển số (đối với loại xe có quy định phải gắn biển số).

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D13/K13/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D13/K13/a

Điều 13. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo), xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tư xe ô tô vi phạm quy định về điều kiện của phương tiện khi tham gia giao thông
13. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển xe thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
a) Thực hiện hành vi quy định tại điểm a, điểm b khoản 3; khoản 4; khoản 5; khoản 6; điểm a khoản 7 Điều này bị trừ điểm giấy phép lái xe 02 điểm;

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D13/K13/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D13/K13/b

Điều 13. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo), xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tư xe ô tô vi phạm quy định về điều kiện của phương tiện khi tham gia giao thông
13. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển xe thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
b) Thực hiện hành vi quy định tại điểm b khoản 7, điểm b khoản 8 Điều này bị trừ điểm giấy phép lái xe 06 điểm;

### Nguồn 2
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2026-08-15 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K2, ND168-2024/D21/K2/a, ND168-2024/D21/K2/b, ND168-2024/D21/K2/c, ND168-2024/D21/K2/d, ND168-2024/D21/K2/đ

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
2. Phạt tiền từ 800.000 đồng đến 1.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
a) Điều khiển xe (kể cả rơ moóc và sơ mi rơ moóc) chở hàng vượt trọng tải (khối lượng hàng chuyên chở) cho phép tham gia giao thông được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe trên 10% đến 30% (trừ xe xi téc chở chất lỏng), trên 20% đến 30% đối với xe xi téc chở chất lỏng;
b) Chở hàng trên nóc thùng xe; chở hàng vượt quá bề rộng thùng xe (kể cả bề rộng rơ moóc và sơ mi rơ moóc); chở hàng vượt phía trước, phía sau thùng xe (kể cả rơ moóc và sơ mi rơ moóc) trên 10% chiều dài toàn bộ của xe theo thiết kế được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe, trừ hành vi vi phạm quy định tại điểm d khoản 8 Điều 21 Nghị định này
c) Chở người trên mui xe;
d) Điều khiển xe kéo theo rơ moóc, sơ mi rơ moóc mà khối lượng toàn bộ (bao gồm khối lượng bản thân rơ moóc, sơ mi rơ moóc và khối lượng hàng chuyên chở) của rơ moóc, sơ mi rơ moóc vượt khối lượng cho phép kéo theo được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe trên 10% đến 30%;
…

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D21/K13/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K13/a

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
13. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
a) Thực hiện hành vi quy định tại điểm b, điểm c, điểm đ khoản 2; điểm a khoản 3; khoản 4; khoản 5; điểm c, điểm d, điểm đ khoản 6 Điều này bị trừ điểm giấy phép lái xe (khi điều khiển xe ô tô) 02 điểm;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D21/K8/d)
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K8/d

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
8. Phạt tiền từ 8.000.000 đồng đến 12.000.000 đồng đối với một trong các hành vi sau đây:
d) Chở thiết bị có hình dạng thùng hoặc có hình dạng như công-ten-nơ (không phải công-ten-nơ) vượt quá chiều dài toàn bộ được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của rơ moóc, sơ mi rơ moóc; chở loại hàng không đúng với thông tin ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của rơ moóc, sơ mi rơ moóc;

[0] 10.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D13/K7)
[1] 12.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D13/K7)
[2] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D13/K13/a)
[3] 06 điểm (số điểm bị trừ, nêu tại ND168-2024/D13/K13/b)
[4] 800.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D21/K2)
[5] 1.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D21/K2)
[6] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D21/K13/a)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Là phụ huynh, tôi muốn biết mức phạt và điểm trừ khi con tôi lái xe ô tô đăng ký tạm thời so với khi lái xe tải vượt trọng tải, có khác nhau không?
- Đáp: Nếu lái xe ô tô đăng ký tạm thời, mức phạt tiền từ 10.000.000 đồng đến 12.000.000 đồng và trừ 02 điểm. Nếu lái xe tải vượt trọng tải, mức phạt tiền từ 800.000 đồng đến 1.000.000 đồng và trừ 02 điểm. Vì vậy, mức phạt tiền cao hơn đối với xe ô tô đăng ký tạm thời, còn điểm trừ là giống nhau.
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-so_sanh-013", "question": "Là phụ huynh, tôi muốn biết mức phạt và điểm trừ khi con tôi lái xe ô tô đăng ký tạm thời so với khi lái xe tải vượt trọng tải, có khác nhau không?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Nếu lái xe ô tô đăng ký tạm thời, mức phạt tiền từ 10.000.000 đồng đến 12.000.000 đồng và trừ 02 điểm. Nếu lái xe tải vượt trọng tải, mức phạt tiền từ 800.000 đồng đến 1.000.000 đồng và trừ 02 điểm. Vì vậy, mức phạt tiền cao hơn đối với xe ô tô đăng ký tạm thời, còn điểm trừ là giống nhau.", "gold_units": ["ND168-2024/D13/K7", "ND168-2024/D13/K13/a", "ND168-2024/D21/K2", "ND168-2024/D21/K13/a"], "required_numbers": [{"value": 10000000, "unit": "vnd"}, {"value": 12000000, "unit": "vnd"}, {"value": 800000, "unit": "vnd"}, {"value": 1000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-013:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Là phụ huynh, tôi muốn biết mức phạt và điểm trừ khi con tôi lái xe ô tô không gắn biển số so với khi lái xe tải chở hàng trên nóc thùng, có khác nhau không?
- Đáp: Nếu lái xe ô tô không gắn biển số, mức phạt tiền từ 10.000.000 đồng đến 12.000.000 đồng và trừ 02 điểm. Nếu lái xe tải chở hàng trên nóc thùng, mức phạt tiền từ 800.000 đồng đến 1.000.000 đồng và trừ 02 điểm. Vì vậy, mức phạt tiền cao hơn đối với xe ô tô không gắn biển số, còn điểm trừ là giống nhau.
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-so_sanh-013", "question": "Là phụ huynh, tôi muốn biết mức phạt và điểm trừ khi con tôi lái xe ô tô không gắn biển số so với khi lái xe tải chở hàng trên nóc thùng, có khác nhau không?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Nếu lái xe ô tô không gắn biển số, mức phạt tiền từ 10.000.000 đồng đến 12.000.000 đồng và trừ 02 điểm. Nếu lái xe tải chở hàng trên nóc thùng, mức phạt tiền từ 800.000 đồng đến 1.000.000 đồng và trừ 02 điểm. Vì vậy, mức phạt tiền cao hơn đối với xe ô tô không gắn biển số, còn điểm trừ là giống nhau.", "gold_units": ["ND168-2024/D13/K7", "ND168-2024/D13/K13/a", "ND168-2024/D21/K2", "ND168-2024/D21/K13/a"], "required_numbers": [{"value": 10000000, "unit": "vnd"}, {"value": 12000000, "unit": "vnd"}, {"value": 800000, "unit": "vnd"}, {"value": 1000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-013:2"}
```

### WD-so_sanh-014 · tier B · vai: sinh viên đi xe máy · kiểu: tinh_huong_ban_than · cosine TF-IDF 0.43

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)
Hiệu lực của trạng thái này: 2026-03-01 → nay
Mã điều khoản dùng được cho gold_units: ND336-2025/D12/K5, ND336-2025/D12/K5/a, ND336-2025/D12/K5/b

Điều 12. Xử phạt các hành vi vi phạm quy định về vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
5. Phạt tiền từ 10.000.000 đồng đến 15.000.000 đồng đối với cá nhân, từ 20.000.000 đồng đến 30.000.000 đồng đối với tổ chức kinh doanh vận tải, dịch vụ hỗ trợ vận tải thực hiện một trong các hành vi vi phạm sau đây:
a) Bến xe không kê khai, công bố thông tin về giá dịch vụ xe ra, vào bến xe theo quy định của pháp luật về giá;
b) Không kê khai giá dịch vụ vận tải hành khách tuyến cố định bằng đường bộ, dịch vụ vận tải hành khách bằng taxi theo quy định.

### Nguồn 2
Văn bản: Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)
Hiệu lực của trạng thái này: 2026-03-01 → nay
Mã điều khoản dùng được cho gold_units: ND336-2025/D8/K6

Điều 8. Xử phạt các hành vi vi phạm quy định về thi công trong phạm vi bảo vệ kết cấu hạ tầng đường bộ
6. Phạt tiền từ 15.000.000 đồng đến 20.000.000 đồng đối với cá nhân, từ 30.000.000 đồng đến 40.000.000 đồng đối với tổ chức thực hiện hành vi vi phạm không xây dựng công trình đường bộ để bồi hoàn, thay thế cho phần công trình bị ảnh hưởng hoặc không bồi hoàn kinh phí để xây dựng đoạn đường thay thế theo quy định.

[0] 10.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D12/K5)
[1] 15.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D12/K5)
[2] 20.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D12/K5)
[3] 30.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D12/K5)
[4] 15.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D8/K6)
[5] 20.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D8/K6)
[6] 30.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D8/K6)
[7] 40.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D8/K6)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là một người lái xe máy, tôi muốn biết mức phạt tiền khác nhau giữa cá nhân và công ty khi không công bố giá dịch vụ xe ra vào bến xe theo quy định.
- Đáp: Cá nhân sẽ bị phạt từ 10.000.000 đồng đến 15.000.000 đồng, trong khi công ty sẽ bị phạt từ 20.000.000 đồng đến 30.000.000 đồng. (khoản 5 Điều 12 Nghị định 336/2025/NĐ-CP)
- ⚠ chep_nguyen_van: “dịch vụ xe ra vào bến …”

```json
{"qid": "tD-so_sanh-014", "question": "Tôi là một người lái xe máy, tôi muốn biết mức phạt tiền khác nhau giữa cá nhân và công ty khi không công bố giá dịch vụ xe ra vào bến xe theo quy định.", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "B", "answer": "Cá nhân sẽ bị phạt từ 10.000.000 đồng đến 15.000.000 đồng, trong khi công ty sẽ bị phạt từ 20.000.000 đồng đến 30.000.000 đồng. (khoản 5 Điều 12 Nghị định 336/2025/NĐ-CP)", "gold_units": ["ND336-2025/D12/K5"], "required_numbers": [{"value": 10000000, "unit": "vnd"}, {"value": 15000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}, {"value": 30000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-014:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là một người lái xe máy, tôi muốn biết mức phạt tiền khác nhau giữa cá nhân và công ty khi không xây dựng công trình đường bộ để bồi hoàn hoặc thay thế theo quy định.
- Đáp: Cá nhân sẽ bị phạt từ 15.000.000 đồng đến 20.000.000 đồng, trong khi công ty sẽ bị phạt từ 30.000.000 đồng đến 40.000.000 đồng. (khoản 6 Điều 8 Nghị định 336/2025/NĐ-CP)
- ⚠ chep_nguyen_van: “công trình đường bộ để bồi …”

```json
{"qid": "tD-so_sanh-014", "question": "Tôi là một người lái xe máy, tôi muốn biết mức phạt tiền khác nhau giữa cá nhân và công ty khi không xây dựng công trình đường bộ để bồi hoàn hoặc thay thế theo quy định.", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "B", "answer": "Cá nhân sẽ bị phạt từ 15.000.000 đồng đến 20.000.000 đồng, trong khi công ty sẽ bị phạt từ 30.000.000 đồng đến 40.000.000 đồng. (khoản 6 Điều 8 Nghị định 336/2025/NĐ-CP)", "gold_units": ["ND336-2025/D8/K6"], "required_numbers": [{"value": 15000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}, {"value": 30000000, "unit": "vnd"}, {"value": 40000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-014:2"}
```

### WD-so_sanh-015 · tier A · vai: tài xế công nghệ · kiểu: neu_van_ban · cosine TF-IDF 0.51

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D11/K1, ND168-2024/D11/K1/a, ND168-2024/D11/K1/b, ND168-2024/D11/K1/c, ND168-2024/D11/K1/d, ND168-2024/D11/K1/đ, ND168-2024/D11/K1/e, ND168-2024/D11/K1/g

Điều 11. Xử phạt người điều khiển, dẫn dắt vật nuôi, điều khiển xe vật nuôi kéo vi phạm quy tắc giao thông đường bộ
1. Phạt tiền từ 150.000 đồng đến 250.000 đồng đối với một trong các hành vi vi phạm sau đây:
a) Không nhường đường theo quy định, không báo hiệu bằng tay khi chuyển hướng;
b) Không chấp hành hiệu lệnh hoặc chỉ dẫn của đèn tín hiệu, biển báo hiệu, vạch kẻ đường, trừ hành vi vi phạm quy định tại khoản 3 Điều này;
c) Không đủ dụng cụ đựng chất thải của vật nuôi hoặc không dọn sạch chất thải của vật nuôi thải ra đường, vỉa hè;
d) Để vật nuôi đi trên đường bộ không bảo đảm an toàn cho người, phương tiện đang tham gia giao thông;
đ) Đi dàn hàng ngang từ 02 xe trở lên;
e) Để vật nuôi kéo xe mà không có người điều khiển;
g) Điều khiển xe không có báo hiệu theo quy định.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D11/K3)
Mã điều khoản dùng được cho gold_units: ND168-2024/D11/K3

Điều 11. Xử phạt người điều khiển, dẫn dắt vật nuôi, điều khiển xe vật nuôi kéo vi phạm quy tắc giao thông đường bộ
3. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với người điều khiển, dẫn dắt vật nuôi, điều khiển xe vật nuôi kéo đi vào đường cao tốc.

### Nguồn 2
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2026-08-15 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D8/K6, ND168-2024/D8/K6/a, ND168-2024/D8/K6/b, ND168-2024/D8/K6/c, ND168-2024/D8/K6/d, ND168-2024/D8/K6/đ, ND168-2024/D8/K6/e, ND168-2024/D8/K6/g, ND168-2024/D8/K6/h, ND168-2024/D8/K6/i

Điều 8. Xử phạt người điều khiển xe máy chuyên dùng vi phạm quy tắc giao thông đường bộ
6. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
a) Chạy quá tốc độ quy định trên 20 km/h;
b) Dừng xe, đỗ xe trên đường cao tốc không đúng nơi quy định; không có báo hiệu bằng đèn khẩn cấp khi gặp sự cố kỹ thuật hoặc bất khả kháng khác buộc phải dừng xe, đỗ xe ở làn dừng xe khẩn cấp hoặc dải dừng xe khẩn cấp trên đường cao tốc; không có báo hiệu bằng đèn khẩn cấp, không đặt biển cảnh báo “Chú ý xe đỗ” (hoặc đèn cảnh báo) về phía sau xe khoảng cách tối thiểu 150 mét khi gặp sự cố kỹ thuật hoặc bất khả kháng khác buộc phải dừng xe, đỗ xe trên một phần làn đường xe chạy trên đường cao tốc;
c) Điều khiển xe trên đường mà trong máu hoặc hơi thở có nồng độ cồn nhưng chưa vượt quá 50 miligam/100 mililít máu hoặc chưa vượt quá 0,25 miligam/1 lít khí thở;
d) Đi vào khu vực cấm, đường có biển báo hiệu có nội dung cấm đi vào đối với loại phương tiện đang điều khiển, trừ các hành vi vi phạm quy định tại điểm d khoản 7, điểm đ khoản 9 Điều này và các trường hợp xe ưu tiên đang đi làm nhiệm vụ khẩn cấp theo quy định;
đ) Không đi bên phải theo chiều đi của mình; đi không đúng phần đường hoặc làn đường quy định (làn cùng chiều hoặc làn ngược chiều); điều khiển xe đi qua dải phân cách cố định ở giữa hai phần đường xe chạy, trừ các hành vi vi phạm quy định tại điểm e khoản 6, điểm d khoản 7, điểm đ khoản 9 Điều này;
…

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D8/K7/d)
Mã điều khoản dùng được cho gold_units: ND168-2024/D8/K7/d

Điều 8. Xử phạt người điều khiển xe máy chuyên dùng vi phạm quy tắc giao thông đường bộ
7. Phạt liền từ 6.000.000 đồng đến 8.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
d) Đi ngược chiều của đường một chiều, đi ngược chiều trên đường có biển “Cấm đi ngược chiều”, trừ các hành vi vi phạm quy định tại điểm đ khoản 9 Điều này và các trường hợp xe ưu tiên đang đi làm nhiệm vụ khẩn cấp theo quy định.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D8/K9/đ)
Mã điều khoản dùng được cho gold_units: ND168-2024/D8/K9/đ

Điều 8. Xử phạt người điều khiển xe máy chuyên dùng vi phạm quy tắc giao thông đường bộ
9. Phạt tiền từ 18.000.000 đồng đến 20.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
đ) Lùi xe trên đường cao tốc; đi ngược chiều trên đường cao tốc; quay đầu xe trên đường cao tốc;

[0] 150.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D11/K1)
[1] 250.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D11/K1)
[2] 3.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D8/K6)
[3] 5.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D8/K6)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi lái xe kéo vật nuôi, vi phạm không nhường đường, mức phạt tiền là bao nhiêu? So sánh với xe máy chuyên dùng chạy quá tốc độ 20 km/h trên đường cao tốc.
- Đáp: Mức phạt tiền cho người điều khiển xe kéo vật nuôi khi không nhường đường là từ 150.000 đồng đến 250.000 đồng. Mức phạt tiền cho người điều khiển xe máy chuyên dùng khi chạy quá tốc độ quy định trên 20 km/h là từ 3.000.000 đồng đến 5.000.000 đồng. Do đó, mức phạt tiền của xe máy chuyên dùng cao hơn nhiều so với xe kéo vật nuôi.
- Ghi chú: Giả định xe kéo vật nuôi là xe không có động cơ, xe máy chuyên dùng là xe có động cơ.

```json
{"qid": "tD-so_sanh-015", "question": "Tôi lái xe kéo vật nuôi, vi phạm không nhường đường, mức phạt tiền là bao nhiêu? So sánh với xe máy chuyên dùng chạy quá tốc độ 20 km/h trên đường cao tốc.", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Mức phạt tiền cho người điều khiển xe kéo vật nuôi khi không nhường đường là từ 150.000 đồng đến 250.000 đồng. Mức phạt tiền cho người điều khiển xe máy chuyên dùng khi chạy quá tốc độ quy định trên 20 km/h là từ 3.000.000 đồng đến 5.000.000 đồng. Do đó, mức phạt tiền của xe máy chuyên dùng cao hơn nhiều so với xe kéo vật nuôi.", "gold_units": ["ND168-2024/D11/K1", "ND168-2024/D8/K6"], "required_numbers": [{"value": 150000, "unit": "vnd"}, {"value": 250000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}, {"value": 5000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-015:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi lái xe kéo vật nuôi, vi phạm không nhường đường, mức phạt tiền là bao nhiêu? So sánh với xe máy chuyên dùng dừng xe không đúng nơi quy định trên đường cao tốc.
- Đáp: Mức phạt tiền cho người điều khiển xe kéo vật nuôi khi không nhường đường là từ 150.000 đồng đến 250.000 đồng. Mức phạt tiền cho người điều khiển xe máy chuyên dùng khi dừng xe, đỗ xe trên đường cao tốc không đúng nơi quy định là từ 3.000.000 đồng đến 5.000.000 đồng. Vì vậy, mức phạt tiền của xe máy chuyên dùng lớn hơn nhiều so với xe kéo vật nuôi.
- Ghi chú: Giả định xe kéo vật nuôi là xe không có động cơ, xe máy chuyên dùng là xe có động cơ.

```json
{"qid": "tD-so_sanh-015", "question": "Tôi lái xe kéo vật nuôi, vi phạm không nhường đường, mức phạt tiền là bao nhiêu? So sánh với xe máy chuyên dùng dừng xe không đúng nơi quy định trên đường cao tốc.", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Mức phạt tiền cho người điều khiển xe kéo vật nuôi khi không nhường đường là từ 150.000 đồng đến 250.000 đồng. Mức phạt tiền cho người điều khiển xe máy chuyên dùng khi dừng xe, đỗ xe trên đường cao tốc không đúng nơi quy định là từ 3.000.000 đồng đến 5.000.000 đồng. Vì vậy, mức phạt tiền của xe máy chuyên dùng lớn hơn nhiều so với xe kéo vật nuôi.", "gold_units": ["ND168-2024/D11/K1", "ND168-2024/D8/K6"], "required_numbers": [{"value": 150000, "unit": "vnd"}, {"value": 250000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}, {"value": 5000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-015:2"}
```

### WD-so_sanh-016 · tier A · vai: cán bộ phường · kiểu: ngan · cosine TF-IDF 0.77

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D6/K9, ND168-2024/D6/K9/a, ND168-2024/D6/K9/b, ND168-2024/D6/K9/c, ND168-2024/D6/K9/d

Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
9. Phạt tiền từ 18.000.000 đồng đến 20.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
a) Điều khiển xe trên đường mà trong máu hoặc hơi thở có nồng độ cồn vượt quá 50 miligam đến 80 miligam/100 mililít máu hoặc vượt quá 0,25 miligam đến 0,4 miligam/1 lít khí thở;
b) Không chấp hành hiệu lệnh của đèn tín hiệu giao thông;
c) Không chấp hành hiệu lệnh, hướng dẫn của người điều khiển giao thông hoặc người kiểm soát giao thông;
d) Đi ngược chiều của đường một chiều, đi ngược chiều trên đường có biển "Cấm đi ngược chiều”, trừ các hành vi vi phạm quy định tại điểm đ khoản 11 Điều này và các trường hợp xe ưu tiên đang đi làm nhiệm vụ khẩn cấp theo quy định.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D6/K16/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D6/K16/b

Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
16. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển xe thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
b) Thực hiện hành vi quy định tại điểm h khoản 5; khoản 6; điểm b khoản 7; điểm b, điểm c, điểm d khoản 9 Điều này bị trừ điểm giấy phép lái xe 04 điểm;

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D6/K16/d)
Mã điều khoản dùng được cho gold_units: ND168-2024/D6/K16/d

Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
16. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển xe thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
d) Thực hiện hành vi quy định tại điểm a khoản 9, khoản 10, điểm đ khoản 11 Điều này bị trừ điểm giấy phép lái xe 10 điểm.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D6/K11/đ)
Mã điều khoản dùng được cho gold_units: ND168-2024/D6/K11/đ

Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
11. Phạt tiền từ 30.000.000 đồng đến 40.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
đ) Điều khiển xe đi ngược chiều trên đường cao tốc, lùi xe trên đường cao tốc, quay đầu xe trên đường cao tốc, trừ các xe ưu tiên đang đi làm nhiệm vụ khẩn cấp theo quy định.

### Nguồn 2
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D9/K3, ND168-2024/D9/K3/a, ND168-2024/D9/K3/b, ND168-2024/D9/K3/c, ND168-2024/D9/K3/d

Điều 9. Xử phạt người điều khiển xe đạp, xe đạp máy, người điều khiển xe thô sơ khác vi phạm quy tắc giao thông đường bộ
3. Phạt tiền từ 300.000 đồng đến 400.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
a) Điều khiển xe lạng lách, đánh võng; đuổi nhau trên đường;
b) Đi xe bằng một bánh đối với xe đạp, xe đạp máy; đi xe bằng hai bánh đối với xe xích lô;
c) Đi vào khu vực cấm, đường có biển báo hiệu nội dung cấm đi vào đối với loại phương tiện đang điều khiển; đi ngược chiều đường của đường một chiều, đường có biển “Cấm đi ngược chiều";
d) Điều khiển xe trên đường mà trong máu hoặc hơi thở có nồng độ cồn vượt quá 50 miligam đến 80 miligam/100 mililít máu hoặc vượt quá 0,25 miligam đến 0,4 miligam/1 lít khí thở.

[0] 18.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D6/K9)
[1] 20.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D6/K9)
[2] 04 điểm (số điểm bị trừ, nêu tại ND168-2024/D6/K16/b)
[3] 10 điểm (số điểm bị trừ, nêu tại ND168-2024/D6/K16/d)
[4] 300.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D9/K3)
[5] 400.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D9/K3)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Công ty tôi muốn biết mức phạt và trừ điểm khi lái xe ô tô vượt cồn 60 mg/100ml so với khi lái xe đạp vượt cồn 60 mg/100ml?
- Đáp: Lái xe ô tô vượt cồn 60 mg/100ml bị phạt từ 18.000.000 đồng đến 20.000.000 đồng và trừ 04 điểm giấy phép lái xe. Lái xe đạp vượt cồn 60 mg/100ml bị phạt từ 300.000 đồng đến 400.000 đồng, không trừ điểm. (khoản 9 Điều 6 và khoản 3 Điều 9 Nghị định 168/2024/NĐ-CP)
- ⚠ so_la: 60
- Ghi chú: Giả định mức cồn 60 mg/100ml là trong phạm vi quy định

```json
{"qid": "tD-so_sanh-016", "question": "Công ty tôi muốn biết mức phạt và trừ điểm khi lái xe ô tô vượt cồn 60 mg/100ml so với khi lái xe đạp vượt cồn 60 mg/100ml?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Lái xe ô tô vượt cồn 60 mg/100ml bị phạt từ 18.000.000 đồng đến 20.000.000 đồng và trừ 04 điểm giấy phép lái xe. Lái xe đạp vượt cồn 60 mg/100ml bị phạt từ 300.000 đồng đến 400.000 đồng, không trừ điểm. (khoản 9 Điều 6 và khoản 3 Điều 9 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D6/K9", "ND168-2024/D6/K16/b", "ND168-2024/D9/K3"], "required_numbers": [{"value": 18000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}, {"value": 300000, "unit": "vnd"}, {"value": 400000, "unit": "vnd"}, {"value": 4, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-016:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Nếu tôi lái xe ô tô vượt cồn 70 mg/100ml và lái xe đạp vượt cồn 70 mg/100ml, mức phạt và trừ điểm sẽ như thế nào?
- Đáp: Lái xe ô tô vượt cồn 70 mg/100ml bị phạt từ 18.000.000 đồng đến 20.000.000 đồng và trừ 04 điểm giấy phép lái xe. Lái xe đạp vượt cồn 70 mg/100ml bị phạt từ 300.000 đồng đến 400.000 đồng, không trừ điểm. (khoản 9 Điều 6 và khoản 3 Điều 9 Nghị định 168/2024/NĐ-CP)
- ⚠ so_la: 70
- Ghi chú: Giả định mức cồn 70 mg/100ml là trong phạm vi quy định

```json
{"qid": "tD-so_sanh-016", "question": "Nếu tôi lái xe ô tô vượt cồn 70 mg/100ml và lái xe đạp vượt cồn 70 mg/100ml, mức phạt và trừ điểm sẽ như thế nào?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Lái xe ô tô vượt cồn 70 mg/100ml bị phạt từ 18.000.000 đồng đến 20.000.000 đồng và trừ 04 điểm giấy phép lái xe. Lái xe đạp vượt cồn 70 mg/100ml bị phạt từ 300.000 đồng đến 400.000 đồng, không trừ điểm. (khoản 9 Điều 6 và khoản 3 Điều 9 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D6/K9", "ND168-2024/D6/K16/b", "ND168-2024/D9/K3"], "required_numbers": [{"value": 18000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}, {"value": 300000, "unit": "vnd"}, {"value": 400000, "unit": "vnd"}, {"value": 4, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-016:2"}
```

### WD-so_sanh-017 · tier B · vai: người mới học lái ô tô · kiểu: ngan · cosine TF-IDF 0.50

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)
Hiệu lực của trạng thái này: 2026-03-01 → nay
Mã điều khoản dùng được cho gold_units: ND336-2025/D5/K5, ND336-2025/D5/K5/a, ND336-2025/D5/K5/b, ND336-2025/D5/K5/c, ND336-2025/D5/K5/d

Điều 5. Xử phạt các hành vi vi phạm quy định về sử dụng, khai thác trong phạm vi đất dành cho kết cấu hạ tầng đường bộ
5. Phạt tiền từ 10.000.000 đồng đến 15.000.000 đồng đối với cá nhân, từ 20.000.000 đồng đến 30.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
a) Xây dựng, lắp đặt biển quảng cáo trong phạm vi hành lang an toàn đường bộ mà không có văn bản chấp thuận theo quy định, trừ hành vi vi phạm quy định tại điểm d khoản 6 Điều này;
b) Không thực hiện việc tháo dỡ biển quảng cáo, các bộ phận của biển quảng cáo khi có yêu cầu của cơ quan quản lý đường bộ, người quản lý, sử dụng đường bộ;
c) Không xóa bỏ, đóng điểm đấu nối tạm thời khi hết thời hạn đấu nối tạm;
d) Không hoàn trả nguyên trạng hành lang an toàn đường bộ; không sửa chữa, bổ sung kết cấu hạ tầng đường bộ bị ảnh hưởng do việc thực hiện đấu nối tạm thời.

### Điều khoản được nguồn trên dẫn chiếu tới (ND336-2025/D5/K6/d)
Mã điều khoản dùng được cho gold_units: ND336-2025/D5/K6/d

Điều 5. Xử phạt các hành vi vi phạm quy định về sử dụng, khai thác trong phạm vi đất dành cho kết cấu hạ tầng đường bộ
6. Phạt tiền từ 15.000.000 đồng đến 20.000.000 đồng đối với cá nhân, từ 30.000.000 đồng đến 40.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
d) Xây dựng, lắp đặt biển quảng cáo trong phạm vi hành lang an toàn đường cao tốc.

### Nguồn 2
Văn bản: Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)
Hiệu lực của trạng thái này: 2026-03-01 → nay
Mã điều khoản dùng được cho gold_units: ND336-2025/D6/K1

Điều 6. Xử phạt hành vi vi phạm quy định về quản lý, vận hành, khai thác, bảo trì công trình hạ tầng kỹ thuật sử dụng chung với đường bộ
1. Phạt tiền từ 6.000.000 đồng đến 10.000.000 đồng đối với cá nhân, từ 12.000.000 đồng đến 20.000.000 đồng đối với tổ chức thực hiện hành vi vi phạm không bố trí dấu hiệu nhận biết công trình hạ tầng thuộc sở hữu khi lắp đặt vào công trình hạ tầng kỹ thuật sử dụng chung với đường bộ.

[0] 10.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D5/K5)
[1] 15.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D5/K5)
[2] 20.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D5/K5)
[3] 30.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D5/K5)
[4] 6.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D6/K1)
[5] 10.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D6/K1)
[6] 12.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D6/K1)
[7] 20.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D6/K1)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Nếu tôi xây dựng biển quảng cáo trong hành lang an toàn đường bộ mà không có giấy phép, mức phạt tiền của cá nhân và tổ chức là bao nhiêu?
- Đáp: Cá nhân sẽ bị phạt từ 10.000.000 đồng đến 15.000.000 đồng, trong khi tổ chức sẽ bị phạt từ 20.000.000 đồng đến 30.000.000 đồng. (Điều 5, Khoản a, Nghị định 336/2025/NĐ-CP)
- ⚠ chep_nguyen_van: “an toàn đường bộ mà không …”

```json
{"qid": "tD-so_sanh-017", "question": "Nếu tôi xây dựng biển quảng cáo trong hành lang an toàn đường bộ mà không có giấy phép, mức phạt tiền của cá nhân và tổ chức là bao nhiêu?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "B", "answer": "Cá nhân sẽ bị phạt từ 10.000.000 đồng đến 15.000.000 đồng, trong khi tổ chức sẽ bị phạt từ 20.000.000 đồng đến 30.000.000 đồng. (Điều 5, Khoản a, Nghị định 336/2025/NĐ-CP)", "gold_units": ["ND336-2025/D5/K5"], "required_numbers": [{"value": 10000000, "unit": "vnd"}, {"value": 15000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}, {"value": 30000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-017:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Nếu công ty tôi lắp đặt công trình hạ tầng kỹ thuật chung với đường bộ mà không đặt dấu hiệu nhận biết, mức phạt tiền của cá nhân và tổ chức là bao nhiêu?
- Đáp: Cá nhân sẽ bị phạt từ 6.000.000 đồng đến 10.000.000 đồng, trong khi tổ chức sẽ bị phạt từ 12.000.000 đồng đến 20.000.000 đồng. (Điều 6, Khoản 1, Nghị định 336/2025/NĐ-CP)
- ⚠ chep_nguyen_van: “công trình hạ tầng kỹ thuật …”

```json
{"qid": "tD-so_sanh-017", "question": "Nếu công ty tôi lắp đặt công trình hạ tầng kỹ thuật chung với đường bộ mà không đặt dấu hiệu nhận biết, mức phạt tiền của cá nhân và tổ chức là bao nhiêu?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "B", "answer": "Cá nhân sẽ bị phạt từ 6.000.000 đồng đến 10.000.000 đồng, trong khi tổ chức sẽ bị phạt từ 12.000.000 đồng đến 20.000.000 đồng. (Điều 6, Khoản 1, Nghị định 336/2025/NĐ-CP)", "gold_units": ["ND336-2025/D6/K1"], "required_numbers": [{"value": 6000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}, {"value": 12000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-017:2"}
```

### WD-so_sanh-018 · tier A · vai: chủ doanh nghiệp vận tải · kiểu: tinh_huong_ban_than · cosine TF-IDF 0.46

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K16, ND168-2024/D32/K16/a, ND168-2024/D32/K16/b, ND168-2024/D32/K16/c

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
16. Phạt tiền từ 65.000.000 đồng đến 75.000.000 đồng đối với cá nhân, từ 130.000.000 đồng đến 150.000.000 đồng đối với tổ chức là chủ xe ô tô, xe máy chuyên dùng và các loại xe tương tự xe ô tô khi thực hiện một trong các hành vi vi phạm sau đây:
a) Giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm a khoản 5 Điều 34 của Nghị định này hoặc trực tiếp điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm a khoản 5 Điều 34 của Nghị định này;
b) Giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm a, điểm b khoản 8 Điều 21 của Nghị định này hoặc trực tiếp điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm a, điểm b khoản 8 Điều 21 của Nghị định này;
c) Tự ý thay đổi tổng thành khung, tổng thành máy (động cơ), hệ thống phanh, hệ thống truyền động (truyền lực), hệ thống chuyển động hoặc tự ý cải tạo kết cấu, hình dáng, kích thước của xe không đúng thiết kế của nhà sản xuất hoặc thiết kế trong hồ sơ đã nộp cho cơ quan đăng ký xe hoặc thiết kế cải tạo đã được cơ quan có thẩm quyền phê duyệt; tự ý thay đổi tính năng sử dụng của xe hoặc tự ý lắp đặt thêm cơ cấu nâng hạ thùng xe, nâng hạ công-ten-nơ trên xe (kể cả rơ moóc và sơ mi rơ moóc).

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K18/c)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K18/c

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
18. Ngoài việc bị phạt tiền, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị áp dụng các hình thức xử phạt bổ sung như sau:
c) Thực hiện hành vi quy định tại điểm e khoản 7, điểm b khoản 11, điểm a khoản 13, khoản 15, điểm b khoản 16 Điều này mà phương tiện đó có thùng xe, khối lượng hàng hóa cho phép chuyên chở không đúng theo quy định hiện hành thì còn bị tước quyền sử dụng chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường và tem kiểm định của phương tiện từ 01 tháng đến 03 tháng;

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K18/d)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K18/d

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
18. Ngoài việc bị phạt tiền, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị áp dụng các hình thức xử phạt bổ sung như sau:
d) Thực hiện hành vi quy định tại điểm d khoản 11, điểm h khoản 14, điểm c khoản 16 Điều này bị tước quyền sử dụng chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường và tem kiểm định của phương tiện từ 01 tháng đến 03 tháng;

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K18/đ)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K18/đ

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
18. Ngoài việc bị phạt tiền, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị áp dụng các hình thức xử phạt bổ sung như sau:
đ) Thực hiện hành vi quy định tại khoản 5, khoản 6 Điều này trong trường hợp chở vượt trên 50% số người quy định được phép chở của phương tiện còn bị tước quyền sử dụng phù hiệu từ 01 tháng đến 03 tháng (nếu có). Thực hiện hành vi quy định tại điểm a, điểm b khoản 11; điểm a, điểm b, điểm c, điểm đ khoản 13; điểm a, điểm b, điểm c, điểm d, điểm đ, điểm e, điểm g khoản 14; khoản 15; khoản 16 Điều này còn bị tước quyền sử dụng phù hiệu từ 01 tháng đến 03 tháng (nếu có),

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K21/c)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K21/c

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
21. Ngoài việc bị áp dụng hình thức xử phạt, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
c) Thực hiện hành vi quy định tại điểm a, điểm b, điểm đ, điểm e khoản 13; điểm a, điểm b, điểm c, điểm d khoản 14; điểm a khoản 16 Điều này trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện còn bị trừ điểm giấy phép lái xe 04 điểm;

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K21/g)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K21/g

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
21. Ngoài việc bị áp dụng hình thức xử phạt, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
g) Thực hiện hành vi quy định tại điểm d khoản 13, điểm b khoản 16 Điều này trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện còn bị trừ điểm giấy phép lái xe 10 điểm;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D34/K5/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D34/K5/a

Điều 34. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển quá khổ giới hạn, xe quá tải trọng, xe bánh xích lưu hành đường bộ (kể cả xe ô tô chở hành khách)
5. Phạt tiền từ 40.000.000 đồng đến 50.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
a) Điều khiển xe mà tổng trọng lượng (khối lượng toàn bộ) của xe hoặc tải trọng trục xe (bao gồm cả hàng hóa xếp trên xe, người được chở trên xe) vượt quá tải trọng cho phép của đường bộ trên 50%, trừ trường hợp có giấy phép lưu hành còn giá trị sử dụng;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D21/K8/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K8/a

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
8. Phạt tiền từ 8.000.000 đồng đến 12.000.000 đồng đối với một trong các hành vi sau đây:
a) Điều khiển xe (kể cả rơ moóc và sơ mi rơ moóc) chở hàng vượt trọng tải (khối lượng hàng chuyên chở) cho phép tham gia giao thông được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe trên 150%;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D21/K8/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K8/b

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
8. Phạt tiền từ 8.000.000 đồng đến 12.000.000 đồng đối với một trong các hành vi sau đây:
b) Điều khiển xe kéo theo rơ moóc, sơ mi rơ moóc mà khối lượng toàn bộ (bao gồm khối lượng bản thân rơ moóc, sơ mi rơ moóc và khối lượng hàng chuyên chở) của rơ moóc, sơ mi rơ moóc vượt khối lượng cho phép kéo theo được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe trên 150%;

### Nguồn 2
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D8/K8, ND168-2024/D8/K8/a, ND168-2024/D8/K8/b, ND168-2024/D8/K8/c, ND168-2024/D8/K8/d

Điều 8. Xử phạt người điều khiển xe máy chuyên dùng vi phạm quy tắc giao thông đường bộ
8. Phạt tiền từ 14.000.000 đồng đến 16.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
a) Điều khiển xe không quan sát, giảm tốc độ hoặc dừng lại để bảo đảm an toàn theo quy định mà gây tai nạn giao thông; điều khiển xe chạy quá tốc độ quy định gây tai nạn giao thông; dừng xe, đỗ xe, quay đầu xe, lùi xe, tránh xe, vượt xe, chuyển hướng, chuyển làn đường không đúng quy định gây tai nạn giao thông; mở cửa xe, để cửa xe mở không bảo đảm an toàn gây tai nạn giao thông; không đi đúng phần đường, làn đường, không giữ khoảng cách an toàn giữa hai xe theo quy định gây tai nạn giao thông hoặc đi vào đường có biển báo hiệu có nội dung cấm đi vào đối với loại phương tiện đang điều khiển, đi ngược chiều của đường một chiều, đi ngược chiều trên đường có biển “Cấm đi ngược chiều” gây tai nạn giao thông, trừ các hành vi vi phạm quy định tại điểm b khoản 8, điểm đ khoản 9 Điều này;
b) Điều khiển xe máy chuyên dùng có tốc độ thiết kế nhỏ hơn tốc độ tối thiểu quy định đối với đường cao tốc đi vào đường cao tốc, trừ phương tiện, thiết bị phục vụ việc quản lý, bảo trì đường cao tốc;
c) Gây tai nạn giao thông không dừng ngay phương tiện, không giữ nguyên hiện trường, không trợ giúp người bị nạn, không ở lại hiện trường hoặc không đến trình báo ngay với cơ quan công an, Ủy ban nhân dân nơi gần nhất;
…

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D8/K9/đ)
Mã điều khoản dùng được cho gold_units: ND168-2024/D8/K9/đ

Điều 8. Xử phạt người điều khiển xe máy chuyên dùng vi phạm quy tắc giao thông đường bộ
9. Phạt tiền từ 18.000.000 đồng đến 20.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
đ) Lùi xe trên đường cao tốc; đi ngược chiều trên đường cao tốc; quay đầu xe trên đường cao tốc;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D8/K1/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D8/K1/a

Điều 8. Xử phạt người điều khiển xe máy chuyên dùng vi phạm quy tắc giao thông đường bộ
1. Phạt tiền từ 400.000 đồng đến 600.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
a) Không chấp hành hiệu lệnh, chỉ dẫn của biển báo hiệu, vạch kẻ đường, trừ các hành vi vi phạm quy định tại điểm a, điểm b, điểm c, điểm đ khoản 2; điểm a, điểm d, điểm đ khoản 3; khoản 4; điểm a, điểm c khoản 5; điểm a, điểm b, điểm d, điểm đ, điểm e, điểm i khoản 6; điểm c, điểm d khoản 7; điểm a, điểm b khoản 8; điểm đ khoản 9 Điều này;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D8/K1/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D8/K1/b

Điều 8. Xử phạt người điều khiển xe máy chuyên dùng vi phạm quy tắc giao thông đường bộ
1. Phạt tiền từ 400.000 đồng đến 600.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
b) Không báo hiệu bằng đèn khẩn cấp hoặc không đặt biển cảnh báo “Chú ý xe đỗ” theo quy định trong trường hợp gặp sự cố kỹ thuật (hoặc bất khả kháng khác) buộc phải đỗ xe chiếm một phần đường xe chạy hoặc tại nơi không được phép đỗ xe, trừ hành vi vi phạm quy định tại điểm b khoản 6 Điều này.

[0] 65.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D32/K16)
[1] 75.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D32/K16)
[2] 130.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D32/K16)
[3] 150.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D32/K16)
[4] 01 tháng (thời hạn tước quyền sử dụng tối thiểu, nêu tại ND168-2024/D32/K18/c)
[5] 03 tháng (thời hạn tước quyền sử dụng tối đa, nêu tại ND168-2024/D32/K18/c)
[6] 01 tháng (thời hạn tước quyền sử dụng tối thiểu, nêu tại ND168-2024/D32/K18/d)
[7] 03 tháng (thời hạn tước quyền sử dụng tối đa, nêu tại ND168-2024/D32/K18/d)
[8] 01 tháng (thời hạn tước quyền sử dụng tối thiểu, nêu tại ND168-2024/D32/K18/đ)
[9] 03 tháng (thời hạn tước quyền sử dụng tối đa, nêu tại ND168-2024/D32/K18/đ)
[10] 04 điểm (số điểm bị trừ, nêu tại ND168-2024/D32/K21/c)
[11] 10 điểm (số điểm bị trừ, nêu tại ND168-2024/D32/K21/g)
[12] 14.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D8/K8)
[13] 16.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D8/K8)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là chủ doanh nghiệp vận tải, công ty tôi có một xe ô tô chở khách và một xe máy chuyên dùng. Khi vi phạm hành vi điều khiển xe không quan sát gây tai nạn, mức phạt tiền của hai loại xe này có khác nhau không?
- Đáp: Mức phạt tiền cho xe ô tô chở khách là từ 65.000.000 đồng đến 75.000.000 đồng, trong khi cho xe máy chuyên dùng là từ 14.000.000 đồng đến 16.000.000 đồng. Do đó, xe ô tô chở khách bị phạt tiền nặng hơn.
- ⚠ chep_nguyen_van: “điều khiển xe không quan sát …”
- Ghi chú: Xe ô tô chở khách là loại xe ô tô, xe máy chuyên dùng là loại xe máy.

```json
{"qid": "tD-so_sanh-018", "question": "Tôi là chủ doanh nghiệp vận tải, công ty tôi có một xe ô tô chở khách và một xe máy chuyên dùng. Khi vi phạm hành vi điều khiển xe không quan sát gây tai nạn, mức phạt tiền của hai loại xe này có khác nhau không?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Mức phạt tiền cho xe ô tô chở khách là từ 65.000.000 đồng đến 75.000.000 đồng, trong khi cho xe máy chuyên dùng là từ 14.000.000 đồng đến 16.000.000 đồng. Do đó, xe ô tô chở khách bị phạt tiền nặng hơn.", "gold_units": ["ND168-2024/D32/K16", "ND168-2024/D8/K8"], "required_numbers": [{"value": 65000000, "unit": "vnd"}, {"value": 75000000, "unit": "vnd"}, {"value": 14000000, "unit": "vnd"}, {"value": 16000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-018:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là chủ doanh nghiệp vận tải, công ty tôi có một xe ô tô chở khách và một xe máy chuyên dùng. Khi vi phạm hành vi điều khiển xe quá tốc độ trên đường cao tốc, mức phạt tiền của hai loại xe này có khác nhau không?
- Đáp: Mức phạt tiền cho xe ô tô chở khách là từ 40.000.000 đồng đến 50.000.000 đồng, trong khi cho xe máy chuyên dùng là từ 18.000.000 đồng đến 20.000.000 đồng. Do đó, xe ô tô chở khách bị phạt tiền nặng hơn.
- Ghi chú: Xe ô tô chở khách là loại xe ô tô, xe máy chuyên dùng là loại xe máy.

```json
{"qid": "tD-so_sanh-018", "question": "Tôi là chủ doanh nghiệp vận tải, công ty tôi có một xe ô tô chở khách và một xe máy chuyên dùng. Khi vi phạm hành vi điều khiển xe quá tốc độ trên đường cao tốc, mức phạt tiền của hai loại xe này có khác nhau không?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Mức phạt tiền cho xe ô tô chở khách là từ 40.000.000 đồng đến 50.000.000 đồng, trong khi cho xe máy chuyên dùng là từ 18.000.000 đồng đến 20.000.000 đồng. Do đó, xe ô tô chở khách bị phạt tiền nặng hơn.", "gold_units": ["ND168-2024/D34/K5/a", "ND168-2024/D8/K9/đ"], "required_numbers": [{"value": 1, "unit": "thang"}, {"value": 3, "unit": "thang"}, {"value": 14000000, "unit": "vnd"}, {"value": 16000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-018:2"}
```

### WD-so_sanh-019 · tier B · vai: phụ huynh có con dưới 18 tuổi · kiểu: ngan · cosine TF-IDF 0.47

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)
Hiệu lực của trạng thái này: 2026-03-01 → nay
Mã điều khoản dùng được cho gold_units: ND336-2025/D10/K5, ND336-2025/D10/K5/a, ND336-2025/D10/K5/b, ND336-2025/D10/K5/c, ND336-2025/D10/K5/d, ND336-2025/D10/K5/đ, ND336-2025/D10/K5/e, ND336-2025/D10/K5/g, ND336-2025/D10/K5/h, ND336-2025/D10/K5/i, ND336-2025/D10/K5/k, ND336-2025/D10/K5/l, ND336-2025/D10/K5/m

Điều 10. Xử phạt các hành vi vi phạm về thanh toán điện tử giao thông đường bộ, hoạt động trạm thu phí đường bộ
5. Phạt tiền từ 50.000.000 đồng đến 70.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
a) Không thực hiện đúng quy trình quản lý, vận hành trạm thu phí theo quy định để số lượng xe ô tô xếp hàng chờ trước trạm thu phí trên một làn xe (tính từ cabin thu phí đến xe cuối cùng của hàng xe chờ) từ 750 m trở lên;
b) Không thực hiện đúng quy trình quản lý, vận hành trạm thu phí theo quy định để thời gian đi qua trạm thu phí của một xe ô tô bất kỳ kể từ lúc dừng xe chờ thu phí đến lúc ra khỏi trạm thu phí lớn hơn 15 phút;
c) Không thực hiện đúng quy trình quản lý, vận hành trạm thu phí theo quy định để xảy ra tai nạn giao thông đối với các phương tiện khi phương tiện tham gia giao thông qua trạm thu phí gây hậu quả từ mức nghiêm trọng trở lên;
d) Không xây dựng hoặc xây dựng không đầy đủ quy trình nghiệp vụ quy định thời gian bù trừ, thanh toán, việc tra soát, đối chiếu dữ liệu;
đ) Không thực hiện các quy trình nghiệp vụ do nhà cung cấp dịch vụ thanh toán điện tử giao thông ban hành;
e) Không thực hiện quy trình đối soát; không khắc phục, điều chỉnh các lỗi, sai số phát hiện được thông qua quá trình đối soát;
g) Không thực hiện nhiệm vụ đối soát số liệu thu phí giữa lưu lượng phương tiện thực tế lưu thông với lưu lượng phương tiện thực hiện thu phí của nhà cung cấp dịch vụ thanh toán tiền sử dụng đường bộ theo quy định;
…

### Nguồn 2
Văn bản: Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)
Hiệu lực của trạng thái này: 2026-03-01 → nay
Mã điều khoản dùng được cho gold_units: ND336-2025/D8/K4, ND336-2025/D8/K4/a, ND336-2025/D8/K4/b, ND336-2025/D8/K4/c, ND336-2025/D8/K4/d

Điều 8. Xử phạt các hành vi vi phạm quy định về thi công trong phạm vi bảo vệ kết cấu hạ tầng đường bộ
4. Phạt tiền từ 7.000.000 đồng đến 10.000.000 đồng đối với cá nhân, từ 14.000.000 đồng đến 20.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
a) Thi công trên đường bộ đang khai thác không đặt đèn cảnh báo giao thông và chiếu sáng ban đêm;
b) Thi công trên đường bộ đang khai thác có bố trí báo hiệu, rào chắn tạm thời tại nơi thi công nhưng không đầy đủ theo giấy phép thi công hoặc văn bản chấp thuận của cơ quan có thẩm quyền, trừ hành vi vi phạm quy định tại điểm c khoản 5 Điều này;
c) Thi công công trình trong phạm vi đất dành cho kết cấu hạ tầng đường bộ không có giấy phép thi công hoặc không có văn bản chấp thuận của cơ quan có thẩm quyền theo quy định;
d) Thi công công trình trên đường bộ đang khai thác không đúng giấy phép thi công gây hư hỏng, hủy hoại công trình đường bộ đang khai thác.

### Điều khoản được nguồn trên dẫn chiếu tới (ND336-2025/D8/K5/c)
Mã điều khoản dùng được cho gold_units: ND336-2025/D8/K5/c

Điều 8. Xử phạt các hành vi vi phạm quy định về thi công trong phạm vi bảo vệ kết cấu hạ tầng đường bộ
5. Phạt tiền từ 10.000.000 đồng đến 15.000.000 đồng đối với cá nhân, từ 20.000.000 đồng đến 30.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
c) Thi công trên đường bộ đang khai thác không bố trí báo hiệu, rào chắn tạm thời tại nơi thi công theo giấy phép thi công hoặc văn bản chấp thuận của cơ quan có thẩm quyền;

[0] 50.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D10/K5)
[1] 70.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D10/K5)
[2] 7.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D8/K4)
[3] 10.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D8/K4)
[4] 14.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D8/K4)
[5] 20.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D8/K4)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là phụ huynh, con tôi đang làm việc tại trạm thu phí và trạm có hàng xe chờ trên 750m, mức phạt tiền khác nhau cho tổ chức và cá nhân là bao nhiêu?
- Đáp: Mức phạt tiền cho tổ chức là từ 50.000.000 đồng đến 70.000.000 đồng. Nếu vi phạm là cá nhân thì mức phạt cũng nằm trong cùng khoảng 50.000.000 đồng đến 70.000.000 đồng. Do đó, mức phạt không khác nhau giữa tổ chức và cá nhân trong trường hợp này.
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-so_sanh-019", "question": "Tôi là phụ huynh, con tôi đang làm việc tại trạm thu phí và trạm có hàng xe chờ trên 750m, mức phạt tiền khác nhau cho tổ chức và cá nhân là bao nhiêu?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "B", "answer": "Mức phạt tiền cho tổ chức là từ 50.000.000 đồng đến 70.000.000 đồng. Nếu vi phạm là cá nhân thì mức phạt cũng nằm trong cùng khoảng 50.000.000 đồng đến 70.000.000 đồng. Do đó, mức phạt không khác nhau giữa tổ chức và cá nhân trong trường hợp này.", "gold_units": ["ND336-2025/D10/K5"], "required_numbers": [{"value": 50000000, "unit": "vnd"}, {"value": 70000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-019:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là phụ huynh, con tôi tham gia thi công đường mà không bố trí báo hiệu, rào chắn tạm thời theo giấy phép, mức phạt tiền khác nhau cho cá nhân và tổ chức là bao nhiêu?
- Đáp: Mức phạt tiền cho cá nhân là từ 10.000.000 đồng đến 15.000.000 đồng. Mức phạt tiền cho tổ chức là từ 20.000.000 đồng đến 30.000.000 đồng. Vì vậy, tổ chức bị phạt nặng hơn cá nhân.
- ⚠ chep_nguyen_van: “báo hiệu rào chắn tạm thời …”
- Ghi chú: Giả định con tôi là cá nhân tham gia thi công

```json
{"qid": "tD-so_sanh-019", "question": "Tôi là phụ huynh, con tôi tham gia thi công đường mà không bố trí báo hiệu, rào chắn tạm thời theo giấy phép, mức phạt tiền khác nhau cho cá nhân và tổ chức là bao nhiêu?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "B", "answer": "Mức phạt tiền cho cá nhân là từ 10.000.000 đồng đến 15.000.000 đồng. Mức phạt tiền cho tổ chức là từ 20.000.000 đồng đến 30.000.000 đồng. Vì vậy, tổ chức bị phạt nặng hơn cá nhân.", "gold_units": ["ND336-2025/D8/K5/c"], "required_numbers": [{"value": 10000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-019:2"}
```

### WD-so_sanh-020 · tier B · vai: tài xế công nghệ · kiểu: tinh_huong_ban_than · cosine TF-IDF 0.42

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)
Hiệu lực của trạng thái này: 2026-03-01 → nay
Mã điều khoản dùng được cho gold_units: ND336-2025/D10/K6, ND336-2025/D10/K6/a, ND336-2025/D10/K6/b

Điều 10. Xử phạt các hành vi vi phạm về thanh toán điện tử giao thông đường bộ, hoạt động trạm thu phí đường bộ
6. Phạt tiền từ 80.000.000 đồng đến 100.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
a) Không quản lý số tiền trong tài khoản thu tiền sử dụng đường bộ độc lập và tách biệt với các khoản tiền khác của nhà cung cấp dịch vụ thanh toán tiền sử dụng đường bộ;
b) Sử dụng sai mục đích tiền trong tài khoản thu tiền sử dụng đường bộ.

### Nguồn 2
Văn bản: Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)
Hiệu lực của trạng thái này: 2026-03-01 → nay
Mã điều khoản dùng được cho gold_units: ND336-2025/D8/K5, ND336-2025/D8/K5/a, ND336-2025/D8/K5/b, ND336-2025/D8/K5/c, ND336-2025/D8/K5/d, ND336-2025/D8/K5/đ, ND336-2025/D8/K5/e, ND336-2025/D8/K5/g

Điều 8. Xử phạt các hành vi vi phạm quy định về thi công trong phạm vi bảo vệ kết cấu hạ tầng đường bộ
5. Phạt tiền từ 10.000.000 đồng đến 15.000.000 đồng đối với cá nhân, từ 20.000.000 đồng đến 30.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
a) Thi công công trình trên đường đô thị không thực hiện đúng thời gian theo giấy phép thi công hoặc văn bản chấp thuận;
b) Thi công trên đường bộ đang khai thác không thực hiện đầy đủ biện pháp tổ chức giao thông để xảy ra tai nạn giao thông;
c) Thi công trên đường bộ đang khai thác không bố trí báo hiệu, rào chắn tạm thời tại nơi thi công theo giấy phép thi công hoặc văn bản chấp thuận của cơ quan có thẩm quyền;
d) Không thực hiện việc di dời công trình khi cơ quan quản lý đường bộ có thẩm quyền, người quản lý, sử dụng đường bộ yêu cầu theo quy định;
đ) Không thực hiện việc di dời công trình khi công trình ảnh hưởng đến an toàn giao thông đường bộ, an toàn công trình đường bộ mà không có biện pháp khắc phục;
e) Không bàn giao công trình, hồ sơ hoàn thành công trình, quy trình bảo trì theo quy định sau khi hoàn thành xây dựng công trình đường bộ để bồi hoàn;
g) Không hoàn trả hoặc hoàn trả kết cấu hạ tầng đường bộ bị ảnh hưởng không đáp ứng theo quy định.

[0] 80.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D10/K6)
[1] 100.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D10/K6)
[2] 10.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D8/K5)
[3] 15.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D8/K5)
[4] 20.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D8/K5)
[5] 30.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D8/K5)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là tài xế công nghệ, tôi muốn biết mức phạt tiền khác nhau giữa tổ chức và cá nhân khi vi phạm việc không quản lý tài khoản thu tiền sử dụng đường bộ độc lập và tách biệt với các khoản tiền khác của nhà cung cấp dịch vụ thanh toán tiền sử dụng đường bộ?
- Đáp: Mức phạt tiền đối với tổ chức là từ 80.000.000 đồng đến 100.000.000 đồng, trong khi đối với cá nhân là không áp dụng. (Điều 10, Nghị định 336/2025/NĐ-CP)
- ⚠ qua_dai (58 từ); chep_nguyen_van: “biệt với các khoản tiền khác …”

```json
{"qid": "tD-so_sanh-020", "question": "Tôi là tài xế công nghệ, tôi muốn biết mức phạt tiền khác nhau giữa tổ chức và cá nhân khi vi phạm việc không quản lý tài khoản thu tiền sử dụng đường bộ độc lập và tách biệt với các khoản tiền khác của nhà cung cấp dịch vụ thanh toán tiền sử dụng đường bộ?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "B", "answer": "Mức phạt tiền đối với tổ chức là từ 80.000.000 đồng đến 100.000.000 đồng, trong khi đối với cá nhân là không áp dụng. (Điều 10, Nghị định 336/2025/NĐ-CP)", "gold_units": ["ND336-2025/D10/K6"], "required_numbers": [{"value": 80000000, "unit": "vnd"}, {"value": 100000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-020:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là tài xế công nghệ, tôi muốn biết mức phạt tiền khác nhau giữa tổ chức và cá nhân khi vi phạm việc thi công trên đường bộ đang khai thác mà không thực hiện đầy đủ biện pháp tổ chức giao thông để tránh tai nạn?
- Đáp: Mức phạt tiền đối với cá nhân là từ 10.000.000 đồng đến 15.000.000 đồng, trong khi đối với tổ chức là từ 20.000.000 đồng đến 30.000.000 đồng. (Điều 8, Nghị định 336/2025/NĐ-CP)
- ⚠ chep_nguyen_van: “biện pháp tổ chức giao thông …”

```json
{"qid": "tD-so_sanh-020", "question": "Tôi là tài xế công nghệ, tôi muốn biết mức phạt tiền khác nhau giữa tổ chức và cá nhân khi vi phạm việc thi công trên đường bộ đang khai thác mà không thực hiện đầy đủ biện pháp tổ chức giao thông để tránh tai nạn?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "B", "answer": "Mức phạt tiền đối với cá nhân là từ 10.000.000 đồng đến 15.000.000 đồng, trong khi đối với tổ chức là từ 20.000.000 đồng đến 30.000.000 đồng. (Điều 8, Nghị định 336/2025/NĐ-CP)", "gold_units": ["ND336-2025/D8/K5"], "required_numbers": [{"value": 10000000, "unit": "vnd"}, {"value": 15000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}, {"value": 30000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-020:2"}
```

### WD-so_sanh-021 · tier A · vai: tài xế công nghệ · kiểu: ngan · cosine TF-IDF 0.61

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D26/K10, ND168-2024/D26/K10/a, ND168-2024/D26/K10/b

Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
10. Phạt tiền từ 40.000.000 đồng đến 60.000.000 đồng đối với đơn vị sản xuất, lắp ráp, nhập khẩu thiết bị ghi nhận hình ảnh người lái xe lắp trên xe ô tô, đơn vị cung cấp dịch vụ liên quan đến giám sát hành trình, ghi nhận hình ảnh người lái xe thực hiện một trong các hành vi vi phạm sau đây:
a) Làm sai lệch thông tin, dữ liệu của thiết bị giám sát hành trình của xe ô tô;
b) Làm sai lệch thông tin, dữ liệu của thiết bị ghi nhận hình ảnh người lái xe lắp trên xe ô tô.

### Nguồn 2
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D29/K3

Điều 29. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe cứu hộ giao thông đường bộ
3. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với hành vi vi phạm điều khiển xe ô tô cứu hộ giao thông đường bộ không lắp thiết bị giám sát hành trình hoặc có lắp thiết bị giám sát hành trình nhưng không có tác dụng trong quá trình xe tham gia giao thông theo quy định hoặc làm sai lệch dữ liệu của thiết bị giám sát hành trình lắp trên xe ô tô.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D29/K4)
Mã điều khoản dùng được cho gold_units: ND168-2024/D29/K4

Điều 29. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe cứu hộ giao thông đường bộ
4. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi quy định tại khoản 3, khoản 3a Điều này bị trừ điểm giấy phép lái xe 02 điểm.

[0] 40.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D26/K10)
[1] 60.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D26/K10)
[2] 3.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D29/K3)
[3] 5.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D29/K3)
[4] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D29/K4)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Nếu công ty tôi sản xuất thiết bị ghi hình cho xe ô tô, mức phạt tiền sẽ cao hơn so với khi tôi lái xe cứu hộ không lắp thiết bị giám sát hành trình?
- Đáp: Mức phạt tiền cho đơn vị sản xuất thiết bị ghi hình là từ 40.000.000 đồng đến 60.000.000 đồng, trong khi mức phạt tiền cho người điều khiển xe cứu hộ là từ 3.000.000 đồng đến 5.000.000 đồng. Do đó, phạt tiền của đơn vị sản xuất thiết bị ghi hình cao hơn nhiều.
- ⚠ chep_nguyen_van: “không lắp thiết bị giám sát …”

```json
{"qid": "tD-so_sanh-021", "question": "Nếu công ty tôi sản xuất thiết bị ghi hình cho xe ô tô, mức phạt tiền sẽ cao hơn so với khi tôi lái xe cứu hộ không lắp thiết bị giám sát hành trình?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Mức phạt tiền cho đơn vị sản xuất thiết bị ghi hình là từ 40.000.000 đồng đến 60.000.000 đồng, trong khi mức phạt tiền cho người điều khiển xe cứu hộ là từ 3.000.000 đồng đến 5.000.000 đồng. Do đó, phạt tiền của đơn vị sản xuất thiết bị ghi hình cao hơn nhiều.", "gold_units": ["ND168-2024/D26/K10", "ND168-2024/D29/K3"], "required_numbers": [{"value": 40000000, "unit": "vnd"}, {"value": 60000000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}, {"value": 5000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-021:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi muốn biết mức phạt tiền khác nhau giữa công ty lắp ráp thiết bị ghi hình cho xe ô tô và người lái xe cứu hộ khi không có thiết bị giám sát hành trình.
- Đáp: Mức phạt tiền cho đơn vị lắp ráp thiết bị ghi hình là từ 40.000.000 đồng đến 60.000.000 đồng, trong khi mức phạt tiền cho người điều khiển xe cứu hộ là từ 3.000.000 đồng đến 5.000.000 đồng. Vì vậy, phạt tiền của đơn vị lắp ráp thiết bị ghi hình lớn hơn nhiều.
- ⚠ chep_nguyen_van: “thiết bị giám sát hành trình …”

```json
{"qid": "tD-so_sanh-021", "question": "Tôi muốn biết mức phạt tiền khác nhau giữa công ty lắp ráp thiết bị ghi hình cho xe ô tô và người lái xe cứu hộ khi không có thiết bị giám sát hành trình.", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Mức phạt tiền cho đơn vị lắp ráp thiết bị ghi hình là từ 40.000.000 đồng đến 60.000.000 đồng, trong khi mức phạt tiền cho người điều khiển xe cứu hộ là từ 3.000.000 đồng đến 5.000.000 đồng. Vì vậy, phạt tiền của đơn vị lắp ráp thiết bị ghi hình lớn hơn nhiều.", "gold_units": ["ND168-2024/D26/K10", "ND168-2024/D29/K3"], "required_numbers": [{"value": 40000000, "unit": "vnd"}, {"value": 60000000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}, {"value": 5000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-021:2"}
```

### WD-so_sanh-022 · tier A · vai: người lớn tuổi đi xe đạp điện · kiểu: ngan · cosine TF-IDF 0.51

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2026-08-15 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K14, ND168-2024/D32/K14/a, ND168-2024/D32/K14/b, ND168-2024/D32/K14/c, ND168-2024/D32/K14/d, ND168-2024/D32/K14/đ, ND168-2024/D32/K14/e, ND168-2024/D32/K14/g, ND168-2024/D32/K14/h, ND168-2024/D32/K14/i

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
14. Phạt tiền từ 28.000.000 đồng đến 30.000.000 đồng đối với cá nhân, từ 56.000.000 đồng đến 60.000.000 đồng đối với tổ chức là chủ xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ, xe máy chuyên dùng và các loại xe tương tự xe ô tô thực hiện một trong các hành vi vi phạm sau đây:
a) Giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm a khoản 3 Điều 22 của Nghị định này hoặc trực tiếp điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm a khoản 3 Điều 22 của Nghị định này;
b) Giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm b khoản 3 Điều 22 của Nghị định này hoặc trực tiếp điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm b khoản 3 Điều 22 của Nghị định này;
c) Giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm c khoản 3 Điều 22 của Nghị định này hoặc trực tiếp điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm c khoản 3 Điều 22 của Nghị định này;
…

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K18/d)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K18/d

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
18. Ngoài việc bị phạt tiền, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị áp dụng các hình thức xử phạt bổ sung như sau:
d) Thực hiện hành vi quy định tại điểm d khoản 11, điểm h khoản 14, điểm c khoản 16 Điều này bị tước quyền sử dụng chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường và tem kiểm định của phương tiện từ 01 tháng đến 03 tháng;

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K18/đ)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K18/đ

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
18. Ngoài việc bị phạt tiền, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị áp dụng các hình thức xử phạt bổ sung như sau:
đ) Thực hiện hành vi quy định tại khoản 5, khoản 6 Điều này trong trường hợp chở vượt trên 50% số người quy định được phép chở của phương tiện còn bị tước quyền sử dụng phù hiệu từ 01 tháng đến 03 tháng (nếu có). Thực hiện hành vi quy định tại điểm a, điểm b khoản 11; điểm a, điểm b, điểm c, điểm đ khoản 13; điểm a, điểm b, điểm c, điểm d, điểm đ, điểm e, điểm g khoản 14; khoản 15; khoản 16 Điều này còn bị tước quyền sử dụng phù hiệu từ 01 tháng đến 03 tháng (nếu có),

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K21/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K21/a

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
21. Ngoài việc bị áp dụng hình thức xử phạt, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
a) Thực hiện hành vi quy định tại điểm đ, điểm g, điểm m khoản 7; điểm đ, điểm e khoản 8; điểm b, điểm c, điểm d, điểm đ khoản 9; điểm a, điểm b, điểm đ khoản 11; điểm a khoản 12; điểm c khoản 13; điểm đ, điểm h khoản 14 Điều này trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện còn bị trừ điểm giấy phép lái xe 02 điểm;

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K21/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K21/b

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
21. Ngoài việc bị áp dụng hình thức xử phạt, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
b) Thực hiện hành vi quy định tại điểm e, điểm g khoản 14 Điều này trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện còn bị trừ điểm giấy phép lái xe 03 điểm;

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K21/c)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K21/c

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
21. Ngoài việc bị áp dụng hình thức xử phạt, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
c) Thực hiện hành vi quy định tại điểm a, điểm b, điểm đ, điểm e khoản 13; điểm a, điểm b, điểm c, điểm d khoản 14; điểm a khoản 16 Điều này trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện còn bị trừ điểm giấy phép lái xe 04 điểm;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D22/K3/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D22/K3/a

Điều 22. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển hàng siêu trường, siêu trọng
3. Phạt tiền từ 13.000.000 đồng đến 15.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
a) Chở hàng siêu trường, siêu trọng không có giấy phép lưu hành hoặc có giấy phép lưu hành nhưng đã hết giá trị sử dụng hoặc sử dụng giấy phép lưu hành không do cơ quan có thẩm quyền cấp;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D22/K3/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D22/K3/b

Điều 22. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển hàng siêu trường, siêu trọng
3. Phạt tiền từ 13.000.000 đồng đến 15.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
b) Chở hàng siêu trường, siêu trọng có giấy phép lưu hành còn giá trị sử dụng nhưng tổng trọng lượng (sau khi đã xếp hàng lên xe) vượt quá quy định trong giấy phép lưu hành;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D22/K3/c)
Mã điều khoản dùng được cho gold_units: ND168-2024/D22/K3/c

Điều 22. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển hàng siêu trường, siêu trọng
3. Phạt tiền từ 13.000.000 đồng đến 15.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
c) Chở hàng siêu trường, siêu trọng có giấy phép lưu hành còn giá trị sử dụng nhưng đi không đúng tuyến đường quy định trong giấy phép lưu hành;

### Nguồn 2
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D34/K1

Điều 34. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển quá khổ giới hạn, xe quá tải trọng, xe bánh xích lưu hành đường bộ (kể cả xe ô tô chở hành khách)
1. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với hành vi không thực hiện đúng quy định trong giấy phép lưu hành, trừ các hành vi vi phạm quy định tại điểm a, điểm b khoản 3; điểm b, điểm c khoản 4 Điều này.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D34/K7/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D34/K7/a

Điều 34. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển quá khổ giới hạn, xe quá tải trọng, xe bánh xích lưu hành đường bộ (kể cả xe ô tô chở hành khách)
7. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
a) Thực hiện hành vi quy định tại khoản 1, khoản 3, điểm a khoản 4 Điều này còn bị trừ điểm giấy phép lái xe 02 điểm;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D34/K3/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D34/K3/a

Điều 34. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển quá khổ giới hạn, xe quá tải trọng, xe bánh xích lưu hành đường bộ (kể cả xe ô tô chở hành khách)
3. Phạt tiền từ 8.000.000 đồng đến 10.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
a) Chở hàng vượt khổ giới hạn của xe hoặc của đường bộ ghi trong giấy phép lưu hành;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D34/K3/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D34/K3/b

Điều 34. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển quá khổ giới hạn, xe quá tải trọng, xe bánh xích lưu hành đường bộ (kể cả xe ô tô chở hành khách)
3. Phạt tiền từ 8.000.000 đồng đến 10.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
b) Điều khiển xe bánh xích tham gia giao thông không có giấy phép lưu hành hoặc có giấy phép lưu hành nhưng không còn giá trị sử dụng theo quy định hoặc lưu thông trực tiếp trên đường mà không thực hiện biện pháp bảo vệ đường theo quy định;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D34/K4/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D34/K4/b

Điều 34. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển quá khổ giới hạn, xe quá tải trọng, xe bánh xích lưu hành đường bộ (kể cả xe ô tô chở hành khách)
4. Phạt tiền từ 13.000.000 đồng đến 15.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
b) Điều khiển xe có giấy phép lưu hành còn giá trị sử dụng nhưng tổng trọng lượng (khối lượng toàn bộ) của xe hoặc tải trọng trục xe (bao gồm cả hàng hóa xếp trên xe nếu có) vượt quá quy định trong giấy phép lưu hành;

[0] 28.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D32/K14)
[1] 30.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D32/K14)
[2] 56.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D32/K14)
[3] 60.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D32/K14)
[4] 01 tháng (thời hạn tước quyền sử dụng tối thiểu, nêu tại ND168-2024/D32/K18/d)
[5] 03 tháng (thời hạn tước quyền sử dụng tối đa, nêu tại ND168-2024/D32/K18/d)
[6] 01 tháng (thời hạn tước quyền sử dụng tối thiểu, nêu tại ND168-2024/D32/K18/đ)
[7] 03 tháng (thời hạn tước quyền sử dụng tối đa, nêu tại ND168-2024/D32/K18/đ)
[8] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D32/K21/a)
[9] 03 điểm (số điểm bị trừ, nêu tại ND168-2024/D32/K21/b)
[10] 04 điểm (số điểm bị trừ, nêu tại ND168-2024/D32/K21/c)
[11] 3.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D34/K1)
[12] 5.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D34/K1)
[13] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D34/K7/a)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Nếu tôi vi phạm hành vi tương tự, mức phạt tiền của xe ô tô chở khách và xe máy chuyên dùng là bao nhiêu, và xe nào nặng hơn?
- Đáp: Mức phạt tiền của xe ô tô chở khách là từ 56.000.000 đồng đến 60.000.000 đồng, còn xe máy chuyên dùng là từ 28.000.000 đồng đến 30.000.000 đồng. Xe ô tô chở khách nặng hơn.

```json
{"qid": "tD-so_sanh-022", "question": "Nếu tôi vi phạm hành vi tương tự, mức phạt tiền của xe ô tô chở khách và xe máy chuyên dùng là bao nhiêu, và xe nào nặng hơn?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Mức phạt tiền của xe ô tô chở khách là từ 56.000.000 đồng đến 60.000.000 đồng, còn xe máy chuyên dùng là từ 28.000.000 đồng đến 30.000.000 đồng. Xe ô tô chở khách nặng hơn.", "gold_units": ["ND168-2024/D32/K14"], "required_numbers": [{"value": 28000000, "unit": "vnd"}, {"value": 30000000, "unit": "vnd"}, {"value": 56000000, "unit": "vnd"}, {"value": 60000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-022:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Nếu tôi là cá nhân và công ty tôi vi phạm hành vi này, mức phạt tiền của cá nhân và tổ chức là bao nhiêu, và tổ chức nặng hơn?
- Đáp: Mức phạt tiền của cá nhân là từ 28.000.000 đồng đến 30.000.000 đồng, còn của tổ chức là từ 56.000.000 đồng đến 60.000.000 đồng. Tổ chức nặng hơn.

```json
{"qid": "tD-so_sanh-022", "question": "Nếu tôi là cá nhân và công ty tôi vi phạm hành vi này, mức phạt tiền của cá nhân và tổ chức là bao nhiêu, và tổ chức nặng hơn?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Mức phạt tiền của cá nhân là từ 28.000.000 đồng đến 30.000.000 đồng, còn của tổ chức là từ 56.000.000 đồng đến 60.000.000 đồng. Tổ chức nặng hơn.", "gold_units": ["ND168-2024/D32/K14"], "required_numbers": [{"value": 28000000, "unit": "vnd"}, {"value": 30000000, "unit": "vnd"}, {"value": 56000000, "unit": "vnd"}, {"value": 60000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-022:2"}
```

### WD-so_sanh-023 · tier B · vai: phụ huynh có con dưới 18 tuổi · kiểu: tinh_huong_ban_than · cosine TF-IDF 0.49

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)
Hiệu lực của trạng thái này: 2026-03-01 → nay
Mã điều khoản dùng được cho gold_units: ND336-2025/D12/K4, ND336-2025/D12/K4/a, ND336-2025/D12/K4/b, ND336-2025/D12/K4/c, ND336-2025/D12/K4/d, ND336-2025/D12/K4/đ, ND336-2025/D12/K4/e, ND336-2025/D12/K4/g, ND336-2025/D12/K4/h, ND336-2025/D12/K4/i, ND336-2025/D12/K4/k

Điều 12. Xử phạt các hành vi vi phạm quy định về vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
4. Phạt tiền từ 5.000.000 đồng đến 10.000.000 đồng đối với cá nhân, từ 10.000.000 đồng đến 20.000.000 đồng đối với tổ chức kinh doanh vận tải, dịch vụ hỗ trợ vận tải thực hiện một trong các hành vi vi phạm sau đây:
a) Thực hiện công bố bến xe hàng, trạm dừng nghỉ không đúng quy định; không thực hiện thủ tục công bố lại bến xe khách, bến xe hàng, trạm dừng nghỉ theo quy định;
b) Không có bộ phận quản lý an toàn theo quy định hoặc có nhưng bộ phận này không thực hiện đầy đủ các nhiệm vụ theo quy định;
c) Không lập hoặc có lập nhưng không cập nhật đầy đủ, chính xác lý lịch phương tiện, lý lịch hành nghề của lái xe theo quy định;
d) Sử dụng xe taxi chở hành khách không lắp đồng hồ tính tiền (đối với loại xe đăng ký sử dụng đồng hồ tính tiền) hoặc lắp đồng hồ tính tiền không đúng quy định; không có thiết bị in hóa đơn (phiếu thu tiền) được kết nối với đồng hồ tính tiền theo quy định hoặc có nhưng không sử dụng được hoặc in ra phiếu thu tiền nhưng không có đầy đủ các thông tin theo quy định;
đ) Sử dụng xe taxi chở hành khách mà trên xe không có thiết bị để kết nối trực tiếp với hành khách theo quy định (đối với loại xe đăng ký sử dụng phần mềm tính tiền) hoặc sử dụng phần mềm tính tiền không bảo đảm các yêu cầu theo quy định;
e) Không thực hiện đúng tiêu chuẩn chất lượng dịch vụ vận tải đã công bố;
g) Không thực hiện đúng giá dịch vụ xe ra, vào bến xe đã kê khai, công bố;
…

### Điều khoản nêu chế tài áp cho hành vi trên (ND336-2025/D12/K8/b)
Mã điều khoản dùng được cho gold_units: ND336-2025/D12/K8/b

Điều 12. Xử phạt các hành vi vi phạm quy định về vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
8. Ngoài việc bị phạt tiền, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị áp dụng các hình thức xử phạt bổ sung sau đây:
b) Thực hiện hành vi vi phạm quy định tại điểm b khoản 3; điểm b khoản 4; điểm b, điểm h khoản 6 Điều này bị tước quyền sử dụng giấy phép kinh doanh vận tải từ 01 tháng đến 03 tháng.

### Nguồn 2
Văn bản: Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)
Hiệu lực của trạng thái này: 2026-03-01 → nay
Mã điều khoản dùng được cho gold_units: ND336-2025/D6/K2, ND336-2025/D6/K2/a, ND336-2025/D6/K2/b

Điều 6. Xử phạt hành vi vi phạm quy định về quản lý, vận hành, khai thác, bảo trì công trình hạ tầng kỹ thuật sử dụng chung với đường bộ
2. Phạt tiền từ 10.000.000 đồng đến 15.000.000 đồng đối với cá nhân, từ 20.000.000 đồng đến 30.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
a) Quản lý, vận hành, khai thác, bảo trì công trình hạ tầng kỹ thuật sử dụng chung với đường bộ gây ảnh hưởng đến an toàn công trình đường bộ, an toàn giao thông đường bộ hoặc cản trở công tác vận hành, khai thác, bảo trì công trình đường bộ;
b) Không thực hiện di dời, tháo dỡ công trình hạ tầng kỹ thuật sử dụng chung, công trình lắp đặt trong công trình kỹ thuật sử dụng chung khi có yêu cầu của người quản lý, sử dụng công trình đường bộ để đầu tư, xây dựng, nâng cấp, mở rộng và bảo trì công trình đường bộ.

[0] 5.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D12/K4)
[1] 10.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D12/K4)
[2] 20.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D12/K4)
[3] 01 tháng (thời hạn tước quyền sử dụng tối thiểu, nêu tại ND336-2025/D12/K8/b)
[4] 03 tháng (thời hạn tước quyền sử dụng tối đa, nêu tại ND336-2025/D12/K8/b)
[5] 10.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D6/K2)
[6] 15.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D6/K2)
[7] 20.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D6/K2)
[8] 30.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D6/K2)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là phụ huynh, con tôi thường đi taxi mà không có đồng hồ tính tiền. Tôi muốn biết mức phạt tiền và thời gian tước giấy phép của cá nhân và công ty vận tải khi vi phạm này.
- Đáp: Cá nhân bị phạt từ 5.000.000 đồng đến 10.000.000 đồng, công ty bị phạt từ 10.000.000 đồng đến 20.000.000 đồng. Ngoài ra, cá nhân và công ty có thể bị tước giấy phép kinh doanh từ 1 tháng đến 3 tháng.
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-so_sanh-023", "question": "Tôi là phụ huynh, con tôi thường đi taxi mà không có đồng hồ tính tiền. Tôi muốn biết mức phạt tiền và thời gian tước giấy phép của cá nhân và công ty vận tải khi vi phạm này.", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "B", "answer": "Cá nhân bị phạt từ 5.000.000 đồng đến 10.000.000 đồng, công ty bị phạt từ 10.000.000 đồng đến 20.000.000 đồng. Ngoài ra, cá nhân và công ty có thể bị tước giấy phép kinh doanh từ 1 tháng đến 3 tháng.", "gold_units": ["ND336-2025/D12/K4", "ND336-2025/D12/K8/b"], "required_numbers": [{"value": 5000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}, {"value": 1, "unit": "thang"}, {"value": 3, "unit": "thang"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-023:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là phụ huynh, công ty tôi quản lý công trình hạ tầng trên đường bộ. Tôi muốn biết mức phạt tiền đối với cá nhân và tổ chức khi vi phạm quản lý công trình gây ảnh hưởng an toàn.
- Đáp: Cá nhân bị phạt từ 10.000.000 đồng đến 15.000.000 đồng, công ty bị phạt từ 20.000.000 đồng đến 30.000.000 đồng.
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-so_sanh-023", "question": "Tôi là phụ huynh, công ty tôi quản lý công trình hạ tầng trên đường bộ. Tôi muốn biết mức phạt tiền đối với cá nhân và tổ chức khi vi phạm quản lý công trình gây ảnh hưởng an toàn.", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "B", "answer": "Cá nhân bị phạt từ 10.000.000 đồng đến 15.000.000 đồng, công ty bị phạt từ 20.000.000 đồng đến 30.000.000 đồng.", "gold_units": ["ND336-2025/D6/K2"], "required_numbers": [{"value": 10000000, "unit": "vnd"}, {"value": 15000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}, {"value": 30000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-023:2"}
```

### WD-so_sanh-024 · tier A · vai: cán bộ phường · kiểu: ngan · cosine TF-IDF 0.53

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K3, ND168-2024/D20/K3/a, ND168-2024/D20/K3/b, ND168-2024/D20/K3/c, ND168-2024/D20/K3/d, ND168-2024/D20/K3/đ, ND168-2024/D20/K3/e, ND168-2024/D20/K3/g, ND168-2024/D20/K3/h, ND168-2024/D20/K3/i, ND168-2024/D20/K3/k

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
3. Phạt tiền từ 600.000 đồng đến 800.000 đồng đối với một trong các hành vi vi phạm sau đây:
a) Không đóng cửa lên xuống khi xe đang chạy;
b) Để người ngồi trên xe khi xe xuống phà, đang trên phà và khi lên bến (trừ người lái xe, trẻ em, phụ nữ mang thai, người già yếu, người bệnh, người khuyết tật);
c) Không chạy đúng tuyến đường, lịch trình, hành trình vận tải được phép hoạt động theo quy định;
d) Để người mắc võng nằm trên xe khi xe đang chạy;
đ) Sắp xếp, chằng buộc hành lý, hàng hóa không bảo đảm an toàn; để rơi hành lý, hàng hóa trên xe xuống đường; để hàng hóa trong khoang chở hành khách;
e) Chở hành lý, hàng hóa vượt quá kích thước bao ngoài của xe;
g) Điều khiển xe vận tải hành khách không có nhân viên phục vụ trên xe đối với những xe quy định phải có nhân viên phục vụ;
h) Điều khiển xe ô tô kinh doanh vận tải không có dây đai an toàn tại các vị trí ghế ngồi, giường nằm theo quy định (trừ xe buýt nội tỉnh);
i) Điều khiển xe ô tô kinh doanh vận tải không có hướng dẫn cho hành khách về an toàn giao thông và thoát hiểm khi xảy ra sự cố trên xe theo quy định;
k) Điều khiển xe không niêm yết hành trình chạy xe hoặc niêm yết hành trình chạy xe không đúng với hành trình đã được cơ quan có thẩm quyền cấp phép.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D20/K10/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K10/a

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
10. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
a) Thực hiện hành vi quy định tại điểm c, điểm d, điểm e khoản 3; điểm a, điểm b, điểm c, điểm d, điểm đ, điểm e, điểm g, điểm h, điểm i, điểm k, điểm m khoản 5; khoản 6; khoản 7 Điều này bị trừ điểm giấy phép lái xe 02 điểm;

### Nguồn 2
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2026-08-15 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D26/K8, ND168-2024/D26/K8/a, ND168-2024/D26/K8/b, ND168-2024/D26/K8/c, ND168-2024/D26/K8/d

Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
8. Phạt tiền từ 10.000.000 đồng đến 12.000.000 đồng đối với cá nhân, từ 20.000.000 đồng đến 24.000.000 đồng đối với tổ chức kinh doanh vận tải, dịch vụ hỗ trợ vận tải thực hiện một trong các hành vi vi phạm sau đây:
a) Không tổ chức khám sức khỏe định kỳ cho lái xe theo quy định hoặc có tổ chức khám nhưng không đầy đủ các nội dung theo quy định;
b) Vi phạm quy định về kinh doanh, điều kiện kinh doanh vận tải bằng xe ô tô để xảy ra tai nạn giao thông gây hậu quả từ mức nghiêm trọng trở lên;
c) Sử dụng xe ô tô kinh doanh vận tải để đón, trả khách; nhận, trả hàng trên đường cao tốc.
d) Sử dụng xe ô tô kinh doanh vận tải hành khách theo hợp đồng mà xác nhận đặt chỗ cho từng hành khách đi xe ngoài hợp đồng đã ký kết hoặc bán vé, thu tiền ngoài hợp đồng đã ký kết; ấn định hành trình, lịch trình cố định để phục vụ cho nhiều hành khách hoặc nhiều người thuê vận tải khác nhau.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D26/K12)
Mã điều khoản dùng được cho gold_units: ND168-2024/D26/K12

Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
12. Ngoài việc bị phạt tiền, cá nhân, tổ chức thực hiện hành vi vi phạm quy định tại điểm c khoản 2; điểm a, điểm b, điểm đ, điểm g khoản 4; điểm b, điểm c, điểm d, điểm đ, điểm e, điểm g khoản 7; điểm c khoản 8 Điều này còn bị áp dụng các hình thức xử phạt bổ sung tước quyền sử dụng phù hiệu từ 01 tháng đến 03 tháng (nếu có hoặc đã được cấp) đối với xe vi phạm.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D26/K14/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D26/K14/b

Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
14. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
b) Thực hiện hành vi quy định tại điểm c khoản 8 Điều này trong trường hợp cá nhân kinh doanh vận tải là người trực tiếp điều khiển phương tiện còn bị trừ điểm giấy phép lái xe 06 điểm.

[0] 600.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D20/K3)
[1] 800.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D20/K3)
[2] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D20/K10/a)
[3] 01 tháng (thời hạn tước quyền sử dụng tối thiểu, nêu tại ND168-2024/D26/K12)
[4] 03 tháng (thời hạn tước quyền sử dụng tối đa, nêu tại ND168-2024/D26/K12)
[5] 10.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D26/K8)
[6] 12.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D26/K8)
[7] 20.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D26/K8)
[8] 24.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D26/K8)
[9] 06 điểm (số điểm bị trừ, nêu tại ND168-2024/D26/K14/b)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Công ty tôi muốn biết mức phạt tiền và trừ điểm khi xe ô tô chở hành khách vi phạm hành vi không đóng cửa khi chạy so với xe ô tô kinh doanh vận tải vi phạm không tổ chức khám sức khỏe định kỳ cho lái xe?
- Đáp: Mức phạt tiền cho xe ô tô chở hành khách là từ 600.000 đồng đến 800.000 đồng và trừ 02 điểm. Mức phạt tiền cho xe ô tô kinh doanh vận tải là từ 10.000.000 đồng đến 12.000.000 đồng và trừ 06 điểm.
- ⚠ chep_nguyen_van: “chức khám sức khỏe định kỳ …”
- Ghi chú: Không nhầm lẫn giữa ô tô chở hành khách và xe ô tô kinh doanh vận tải.

```json
{"qid": "tD-so_sanh-024", "question": "Công ty tôi muốn biết mức phạt tiền và trừ điểm khi xe ô tô chở hành khách vi phạm hành vi không đóng cửa khi chạy so với xe ô tô kinh doanh vận tải vi phạm không tổ chức khám sức khỏe định kỳ cho lái xe?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Mức phạt tiền cho xe ô tô chở hành khách là từ 600.000 đồng đến 800.000 đồng và trừ 02 điểm. Mức phạt tiền cho xe ô tô kinh doanh vận tải là từ 10.000.000 đồng đến 12.000.000 đồng và trừ 06 điểm.", "gold_units": ["ND168-2024/D20/K3", "ND168-2024/D20/K10/a", "ND168-2024/D26/K8", "ND168-2024/D26/K14/b"], "required_numbers": [{"value": 600000, "unit": "vnd"}, {"value": 800000, "unit": "vnd"}, {"value": 2, "unit": "diem"}, {"value": 10000000, "unit": "vnd"}, {"value": 12000000, "unit": "vnd"}, {"value": 6, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-024:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Công ty tôi muốn biết mức phạt tiền và trừ điểm khi cá nhân và tổ chức kinh doanh vận tải vi phạm hành vi sử dụng xe ô tô kinh doanh vận tải để đón, trả khách trên đường cao tốc?
- Đáp: Mức phạt tiền cho cá nhân là từ 10.000.000 đồng đến 12.000.000 đồng và trừ 06 điểm. Mức phạt tiền cho tổ chức kinh doanh vận tải là từ 20.000.000 đồng đến 24.000.000 đồng và không trừ điểm.
- ⚠ chep_nguyen_van: “doanh vận tải để đón trả …”
- Ghi chú: Đảm bảo phân biệt cá nhân và tổ chức trong câu hỏi.

```json
{"qid": "tD-so_sanh-024", "question": "Công ty tôi muốn biết mức phạt tiền và trừ điểm khi cá nhân và tổ chức kinh doanh vận tải vi phạm hành vi sử dụng xe ô tô kinh doanh vận tải để đón, trả khách trên đường cao tốc?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Mức phạt tiền cho cá nhân là từ 10.000.000 đồng đến 12.000.000 đồng và trừ 06 điểm. Mức phạt tiền cho tổ chức kinh doanh vận tải là từ 20.000.000 đồng đến 24.000.000 đồng và không trừ điểm.", "gold_units": ["ND168-2024/D26/K8", "ND168-2024/D26/K12", "ND168-2024/D26/K14/b"], "required_numbers": [{"value": 10000000, "unit": "vnd"}, {"value": 12000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}, {"value": 24000000, "unit": "vnd"}, {"value": 6, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-024:2"}
```

### WD-so_sanh-025 · tier A · vai: tài xế xe tải · kiểu: tinh_huong_nguoi_khac · cosine TF-IDF 0.42

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D38/K1, ND168-2024/D38/K1/a, ND168-2024/D38/K1/b

Điều 38. Xử phạt người điều khiển phương tiện đăng ký hoạt động trong Khu kinh tế thương mại đặc biệt, Khu kinh tế cửa khẩu quốc tế
1. Phạt tiền từ 500.000 đồng đến 1.000.000 đồng đối với người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy thực hiện một trong các hành vi vi phạm sau đây:
a) Không có tờ khai phương tiện vận tải đường bộ tạm nhập, tái xuất theo quy định;
b) Điều khiển xe không có phù hiệu kiểm soát theo quy định hoặc có nhưng đã hết giá trị sử dụng hoặc sử dụng phù hiệu không do cơ quan có thẩm quyền cấp.

### Nguồn 2
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D9/K1, ND168-2024/D9/K1/a, ND168-2024/D9/K1/b, ND168-2024/D9/K1/c, ND168-2024/D9/K1/d, ND168-2024/D9/K1/đ, ND168-2024/D9/K1/e, ND168-2024/D9/K1/g, ND168-2024/D9/K1/h, ND168-2024/D9/K1/i, ND168-2024/D9/K1/k, ND168-2024/D9/K1/l, ND168-2024/D9/K1/m, ND168-2024/D9/K1/n, ND168-2024/D9/K1/o, ND168-2024/D9/K1/p

Điều 9. Xử phạt người điều khiển xe đạp, xe đạp máy, người điều khiển xe thô sơ khác vi phạm quy tắc giao thông đường bộ
1. Phạt tiền từ 100.000 đồng đến 200.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
a) Không đi bên phải theo chiều đi của mình, đi không đúng phần đường quy định;
b) Dừng xe đột ngột; chuyển hướng không báo hiệu trước;
c) Không chấp hành hiệu lệnh hoặc chỉ dẫn của biển báo hiệu, vạch kẻ đường, trừ các hành vi vi phạm quy định tại điểm đ khoản 2, điểm c khoản 3 Điều này;
d) Vượt bên phải trong các trường hợp không được phép;
đ) Dừng xe, đỗ xe trên phần đường xe chạy ở đoạn đường ngoài đô thị nơi có lề đường;
e) Chạy trong hầm đường bộ không bật đèn hoặc không có vật phát sáng báo hiệu; dừng xe, đỗ xe trong hầm đường bộ không đúng nơi quy định; quay đầu xe trong hầm đường bộ;
g) Điều khiển xe đạp, xe đạp máy đi dàn hàng ngang từ 03 xe trở lên, xe thô sơ khác đi dàn hàng ngang từ 02 xe trở lên;
h) Người điều khiển xe đạp, xe đạp máy sử dụng ô (dù), dùng tay cầm và sử dụng điện thoại hoặc các thiết bị điện tử khác; chở người ngồi trên xe đạp, xe đạp máy sử dụng ô (dù);
i) Điều khiển xe thô sơ trong thời gian từ 18 giờ ngày hôm trước đến 06 giờ ngày hôm sau không sử dụng đèn hoặc không có báo hiệu ở phía trước và phía sau xe;
k) Để xe ở lòng đường, vỉa hè trái phép; đỗ xe ở lòng đường gây cản trở giao thông, đỗ xe trên cầu gây cản trở giao thông;
…

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D9/K2/đ)
Mã điều khoản dùng được cho gold_units: ND168-2024/D9/K2/đ

Điều 9. Xử phạt người điều khiển xe đạp, xe đạp máy, người điều khiển xe thô sơ khác vi phạm quy tắc giao thông đường bộ
2. Phạt tiền từ 150.000 đồng đến 250.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
đ) Không chấp hành hiệu lệnh của đèn tín hiệu giao thông.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D9/K3/c)
Mã điều khoản dùng được cho gold_units: ND168-2024/D9/K3/c

Điều 9. Xử phạt người điều khiển xe đạp, xe đạp máy, người điều khiển xe thô sơ khác vi phạm quy tắc giao thông đường bộ
3. Phạt tiền từ 300.000 đồng đến 400.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
c) Đi vào khu vực cấm, đường có biển báo hiệu nội dung cấm đi vào đối với loại phương tiện đang điều khiển; đi ngược chiều đường của đường một chiều, đường có biển “Cấm đi ngược chiều";

[0] 500.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D38/K1)
[1] 1.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D38/K1)
[2] 100.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D9/K1)
[3] 200.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D9/K1)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Anh tôi lái xe tải, anh ấy hỏi: anh ta biết được mức phạt tiền khác nhau khi lái xe mô tô và khi lái xe đạp trong khu kinh tế thương mại đặc biệt, phải không?
- Đáp: Mức phạt tiền khi lái xe mô tô là từ 500.000 đồng đến 1.000.000 đồng, còn khi lái xe đạp là từ 100.000 đồng đến 200.000 đồng. Do đó, phạt tiền cho xe mô tô nặng hơn nhiều so với xe đạp.
- ⚠ chep_nguyen_van: “khu kinh tế thương mại đặc …”
- Ghi chú: Xe mô tô và xe gắn máy đều được tính là loại xe mô tô trong quy định.

```json
{"qid": "tD-so_sanh-025", "question": "Anh tôi lái xe tải, anh ấy hỏi: anh ta biết được mức phạt tiền khác nhau khi lái xe mô tô và khi lái xe đạp trong khu kinh tế thương mại đặc biệt, phải không?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Mức phạt tiền khi lái xe mô tô là từ 500.000 đồng đến 1.000.000 đồng, còn khi lái xe đạp là từ 100.000 đồng đến 200.000 đồng. Do đó, phạt tiền cho xe mô tô nặng hơn nhiều so với xe đạp.", "gold_units": ["ND168-2024/D38/K1", "ND168-2024/D9/K1"], "required_numbers": [{"value": 500000, "unit": "vnd"}, {"value": 1000000, "unit": "vnd"}, {"value": 100000, "unit": "vnd"}, {"value": 200000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-025:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Công ty tôi lái xe tải, một đồng nghiệp của chúng tôi hỏi: trong khu kinh tế thương mại đặc biệt, phạt tiền khi điều khiển xe mô tô và khi điều khiển xe đạp có khác nhau không?
- Đáp: Mức phạt tiền khi điều khiển xe mô tô là từ 500.000 đồng đến 1.000.000 đồng, trong khi phạt tiền khi điều khiển xe đạp là từ 100.000 đồng đến 200.000 đồng. Vì vậy, phạt tiền cho xe mô tô cao hơn so với xe đạp.
- ⚠ chep_nguyen_van: “khu kinh tế thương mại đặc …”
- Ghi chú: Xe mô tô và xe gắn máy đều được tính là loại xe mô tô trong quy định.

```json
{"qid": "tD-so_sanh-025", "question": "Công ty tôi lái xe tải, một đồng nghiệp của chúng tôi hỏi: trong khu kinh tế thương mại đặc biệt, phạt tiền khi điều khiển xe mô tô và khi điều khiển xe đạp có khác nhau không?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Mức phạt tiền khi điều khiển xe mô tô là từ 500.000 đồng đến 1.000.000 đồng, trong khi phạt tiền khi điều khiển xe đạp là từ 100.000 đồng đến 200.000 đồng. Vì vậy, phạt tiền cho xe mô tô cao hơn so với xe đạp.", "gold_units": ["ND168-2024/D38/K1", "ND168-2024/D9/K1"], "required_numbers": [{"value": 500000, "unit": "vnd"}, {"value": 1000000, "unit": "vnd"}, {"value": 100000, "unit": "vnd"}, {"value": 200000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-025:2"}
```

### WD-so_sanh-026 · tier A · vai: tài xế công nghệ · kiểu: tinh_huong_ban_than · cosine TF-IDF 0.43

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D12/K2, ND168-2024/D12/K2/a, ND168-2024/D12/K2/b, ND168-2024/D12/K2/c, ND168-2024/D12/K2/d, ND168-2024/D12/K2/đ, ND168-2024/D12/K2/e, ND168-2024/D12/K2/g

Điều 12. Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm khác về quy tắc giao thông đường bộ; sử dụng lòng đường, vỉa hè vào mục đích khác
2. Phạt tiền từ 200.000 đồng đến 250.000 đồng đối với cá nhân thực hiện một trong các hành vi vi phạm sau đây:
a) Tập trung đông người trái phép, nằm, ngồi trên đường bộ gây cản trở giao thông;
b) Đá bóng, đá cầu, chơi cầu lông hoặc các hoạt động thể thao khác trái phép trên đường bộ; sử dụng bàn trượt, pa-tanh, các thiết bị tương tự trên phần đường xe chạy;
c) Điều khiển vật thể bay, tàu bay không người lái, phương tiện bay siêu nhẹ hoạt động trong phạm vi khổ giới hạn đường bộ gây cản trở hoặc nguy cơ mất an toàn cho người, phương tiện tham gia giao thông đường bộ, trừ tàu bay không người lái, phương tiện bay siêu nhẹ được cấp phép bay;
d) Người được chở trên xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy sử dụng ô (dù);
đ) Người được chở trên xe đạp, xe đạp máy bám, kéo, đẩy xe khác, vật khác, mang vác vật cồng kềnh;
e) Bán hàng rong hoặc bán hàng hóa nhỏ lẻ khác trên lòng đường, trên vỉa hè các tuyến phố có quy định cấm bán hàng; trừ các hành vi vi phạm quy định tại khoản 7, khoản 9 Điều này;
g) Phơi thóc, lúa, rơm, rạ, nông, lâm, hải sản trên đường bộ; đặt máy tuốt lúa trên đường bộ.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D12/K7)
Mã điều khoản dùng được cho gold_units: ND168-2024/D12/K7

Điều 12. Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm khác về quy tắc giao thông đường bộ; sử dụng lòng đường, vỉa hè vào mục đích khác
7. Phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng đối với cá nhân, từ 4.000.000 đồng đến 6.000.000 đồng đối với tổ chức thực hiện hành vi sử dụng trái phép lòng đường, vỉa hè để: họp chợ; kinh doanh dịch vụ ăn uống; bày, bán hàng hóa; sửa chữa phương tiện, máy móc, thiết bị; rửa xe; đặt, treo biển hiệu, biển quảng cáo.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D12/K9)
Mã điều khoản dùng được cho gold_units: ND168-2024/D12/K9

Điều 12. Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm khác về quy tắc giao thông đường bộ; sử dụng lòng đường, vỉa hè vào mục đích khác
9. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với cá nhân, từ 6.000.000 đồng đến 10.000.000 đồng đối với tổ chức thực hiện hành vi bày, bán máy móc, thiết bị, vật tư hoặc sản xuất, gia công hàng hóa trên lòng đường, vỉa hè,

### Nguồn 2
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2026-08-15 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K1, ND168-2024/D32/K1/a, ND168-2024/D32/K1/b

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
1. Phạt tiền từ 200.000 đồng đến 300.000 đồng đối với cá nhân, từ 400.000 đồng đến 600.000 đồng đối với tổ chức là chủ xe mô tô, xe gắn máy và các loại xe tương tự xe mô tô, các loại xe tương tự xe gắn máy thực hiện một trong các hành vi vi phạm sau đây:
a) Tự ý thay đổi nhãn hiệu, màu sơn của xe không đúng với chứng nhận đăng ký xe;
b) Đưa phương tiện không có chứng nhận kiểm định khí thải xe mô tô, xe gắn máy hoặc có nhưng đã hết hạn sử dụng hoặc sử dụng chứng nhận kiểm định khí thải xe mô tô, xe gắn máy không do cơ quan có thẩm quyền cấp.

[0] 200.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D12/K2)
[1] 250.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D12/K2)
[2] 200.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D32/K1)
[3] 300.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D32/K1)
[4] 400.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D32/K1)
[5] 600.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D32/K1)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi đang bán hàng rong trên vỉa hè, tôi là cá nhân. Nếu tôi làm như vậy, mức phạt tiền sẽ là bao nhiêu? Nếu công ty tôi làm cùng, mức phạt sẽ khác như thế nào?
- Đáp: Nếu cá nhân bán hàng rong trên vỉa hè, mức phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng. Nếu tổ chức thực hiện cùng hành vi, mức phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng.
- Ghi chú: đã dùng "công ty" để chỉ tổ chức

```json
{"qid": "tD-so_sanh-026", "question": "Tôi đang bán hàng rong trên vỉa hè, tôi là cá nhân. Nếu tôi làm như vậy, mức phạt tiền sẽ là bao nhiêu? Nếu công ty tôi làm cùng, mức phạt sẽ khác như thế nào?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Nếu cá nhân bán hàng rong trên vỉa hè, mức phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng. Nếu tổ chức thực hiện cùng hành vi, mức phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng.", "gold_units": ["ND168-2024/D12/K7"], "required_numbers": [{"value": 200000, "unit": "vnd"}, {"value": 250000, "unit": "vnd"}, {"value": 400000, "unit": "vnd"}, {"value": 600000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-026:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là chủ xe mô tô, tôi tự ý thay đổi màu sơn xe. Phạt tiền sẽ là bao nhiêu? Nếu thay đổi chứng nhận kiểm định khí thải hết hạn, mức phạt sẽ như thế nào?
- Đáp: Nếu cá nhân chủ xe mô tô thay đổi màu sơn, mức phạt tiền từ 200.000 đồng đến 300.000 đồng. Nếu cá nhân chủ xe mô tô vi phạm về chứng nhận kiểm định khí thải hết hạn, mức phạt tiền cũng từ 200.000 đồng đến 300.000 đồng.
- ⚠ chep_nguyen_van: “chứng nhận kiểm định khí thải …”
- Ghi chú: đã dùng "cá nhân" để chỉ chủ xe

```json
{"qid": "tD-so_sanh-026", "question": "Tôi là chủ xe mô tô, tôi tự ý thay đổi màu sơn xe. Phạt tiền sẽ là bao nhiêu? Nếu thay đổi chứng nhận kiểm định khí thải hết hạn, mức phạt sẽ như thế nào?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Nếu cá nhân chủ xe mô tô thay đổi màu sơn, mức phạt tiền từ 200.000 đồng đến 300.000 đồng. Nếu cá nhân chủ xe mô tô vi phạm về chứng nhận kiểm định khí thải hết hạn, mức phạt tiền cũng từ 200.000 đồng đến 300.000 đồng.", "gold_units": ["ND168-2024/D32/K1"], "required_numbers": [{"value": 200000, "unit": "vnd"}, {"value": 300000, "unit": "vnd"}, {"value": 400000, "unit": "vnd"}, {"value": 600000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-026:2"}
```

### WD-so_sanh-027 · tier A · vai: cán bộ phường · kiểu: nhieu_dieu_kien · cosine TF-IDF 0.44

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D18/K7, ND168-2024/D18/K7/a, ND168-2024/D18/K7/b, ND168-2024/D18/K7/c, ND168-2024/D18/K7/d

Điều 18. Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm quy định về điều kiện của người điều khiển xe cơ giới
7. Phạt tiền từ 6.000.000 đồng đến 8.000.000 đồng đối với người điều khiển xe mô tô hai bánh có dung tích xi-lanh trên 125 cm3 trở lên hoặc có công suất động cơ điện trên 11 kW, xe mô tô ba bánh thực hiện một trong các hành vi vi phạm sau đây:
a) Có giấy phép lái xe nhưng không phù hợp với loại xe đang điều khiển;
b) Không có giấy phép lái xe hoặc sử dụng giấy phép lái xe đã bị trừ hết điểm, giấy phép lái xe không do cơ quan có thẩm quyền cấp, giấy phép lái xe bị tẩy xóa, giấy phép lái xe không còn hiệu lực;
c) Có giấy phép lái xe quốc tế do các nước tham gia Công ước của Liên hợp quốc về Giao thông đường bộ năm 1968 cấp (trừ giấy phép lái xe quốc tế do Việt Nam cấp) nhưng không mang theo giấy phép lái xe quốc gia phù hợp với loại xe được phép điều khiển;
d) Sử dụng giấy phép lái xe không hợp lệ (giấy phép lái xe có số phôi ghi ở mặt sau không trùng với số phôi được cấp mới nhất trong hệ thống thông tin quản lý giấy phép lái xe).

### Nguồn 2
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D39/K3, ND168-2024/D39/K3/a, ND168-2024/D39/K3/b, ND168-2024/D39/K3/c, ND168-2024/D39/K3/d, ND168-2024/D39/K3/đ, ND168-2024/D39/K3/e, ND168-2024/D39/K3/g, ND168-2024/D39/K3/h, ND168-2024/D39/K3/i, ND168-2024/D39/K3/k

Điều 39. Xử phạt các hành vi vi phạm quy định về đào tạo, sát hạch lái xe
3. Phạt tiền từ 5.000.000 đồng đến 10.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
a) Cơ sở đào tạo lái xe không bố trí giáo viên dạy thực hành ngồi bên cạnh để bảo trợ tay lái cho học viên thực hành lái xe; bố trí giáo viên không đủ tiêu chuẩn để giảng dạy;
b) Cơ sở đào tạo lái xe sử dụng xe tập lái không có giấy phép xe tập lái hoặc có nhưng hết hạn, không gắn biển xe “Tập lái” trên xe theo quy định, không ghi tên cơ sở đào tạo, số điện thoại ở mặt ngoài hai bên cánh cửa hoặc hai bên thành xe theo quy định;
c) Cơ sở đào tạo lái xe sử dụng xe tập lái không trang bị thêm bộ phận hãm phụ hoặc có nhưng không có tác dụng;
d) Cơ sở đào tạo lái xe tuyển sinh học viên không đủ điều kiện trình độ văn hóa, thời gian lái xe an toàn tương ứng với từng hạng đào tạo; tuyển sinh học viên không đủ hồ sơ theo quy định;
đ) Cơ sở đào tạo lái xe không có đủ số lượng giáo viên dạy thực hành lái xe các hạng để đáp ứng với kế hoạch sử dụng các xe tập lái dùng để đào tạo;
e) Cơ sở đào tạo lái xe không lưu trữ hoặc lưu trữ không đầy đủ hồ sơ theo quy định của 01 khóa đào tạo;
g) Trung tâm sát hạch lái xe không duy trì đủ các điều kiện quy định trong Quy chuẩn kỹ thuật quốc gia về Trung tâm sát hạch lái xe cơ giới đường bộ, trừ các hành vi vi phạm quy định tại khoản 4, khoản 5, khoản 7 Điều này;
h) Trung tâm sát hạch lái xe không lưu trữ hoặc lưu trữ không đầy đủ hồ sơ theo quy định của 01 kỳ sát hạch lái xe;
…

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D39/K9/c)
Mã điều khoản dùng được cho gold_units: ND168-2024/D39/K9/c

Điều 39. Xử phạt các hành vi vi phạm quy định về đào tạo, sát hạch lái xe
9. Ngoài việc bị phạt tiền, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị áp dụng các hình thức xử phạt bổ sung sau đây:
c) Trung tâm sát hạch lái xe thực hiện hành vi quy định tại điểm h khoản 3; điểm i, điểm k khoản 4; điểm đ, điểm e, điểm g, điểm h, điểm i khoản 5 Điều này bị tước quyền sử dụng giấy phép sát hạch từ 01 tháng đến 03 tháng;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D39/K4)
Mã điều khoản dùng được cho gold_units: ND168-2024/D39/K4

Điều 39. Xử phạt các hành vi vi phạm quy định về đào tạo, sát hạch lái xe
4. Phạt tiền từ 10.000.000 đồng đến 20.000.000 đồng đối với cơ sở đào tạo lái xe, trung tâm sát hạch lái xe thực hiện một trong các hành vi vi phạm sau đây:

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D39/K5)
Mã điều khoản dùng được cho gold_units: ND168-2024/D39/K5

Điều 39. Xử phạt các hành vi vi phạm quy định về đào tạo, sát hạch lái xe
5. Phạt tiền từ 20.000.000 đồng đến 30.000.000 đồng đối với cơ sở đào tạo lái xe, trung tâm sát hạch lái xe thực hiện một trong các hành vi vi phạm sau đây:

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D39/K7)
Mã điều khoản dùng được cho gold_units: ND168-2024/D39/K7

Điều 39. Xử phạt các hành vi vi phạm quy định về đào tạo, sát hạch lái xe
7. Phạt tiền từ 40.000.000 đồng đến 50.000.000 đồng đối với trung tâm sát hạch lái xe thực hiện một trong các hành vi vi phạm sau đây:

[0] 6.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D18/K7)
[1] 8.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D18/K7)
[2] 5.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D39/K3)
[3] 10.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D39/K3)
[4] 01 tháng (thời hạn tước quyền sử dụng tối thiểu, nêu tại ND168-2024/D39/K9/c)
[5] 03 tháng (thời hạn tước quyền sử dụng tối đa, nêu tại ND168-2024/D39/K9/c)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là cán bộ phường, muốn biết mức phạt tiền khác nhau khi một người điều khiển xe mô tô có dung tích xi-lanh trên 125 cm3 vi phạm quy định về giấy phép, so với một cơ sở đào tạo lái xe sử dụng xe tập không có giấy phép hợp lệ. Cả hai trường hợp đều xảy ra trong cùng một ngày, tôi cần biết mức phạt tối thiểu và tối đa cho từng bên, và bên nào bị phạt nặng hơn.
- Đáp: Cơ sở đào tạo lái xe bị phạt từ 5.000.000 đồng đến 10.000.000 đồng, trong khi người điều khiển xe mô tô bị phạt từ 6.000.000 đồng đến 8.000.000 đồng. Do đó, cơ sở đào tạo lái xe có mức phạt cao hơn.
- ⚠ qua_dai (84 từ); chep_nguyen_van: “có dung tích xi lanh trên …”
- Ghi chú: Đối tượng so sánh là người điều khiển xe mô tô và cơ sở đào tạo lái xe.

```json
{"qid": "tD-so_sanh-027", "question": "Tôi là cán bộ phường, muốn biết mức phạt tiền khác nhau khi một người điều khiển xe mô tô có dung tích xi-lanh trên 125 cm3 vi phạm quy định về giấy phép, so với một cơ sở đào tạo lái xe sử dụng xe tập không có giấy phép hợp lệ. Cả hai trường hợp đều xảy ra trong cùng một ngày, tôi cần biết mức phạt tối thiểu và tối đa cho từng bên, và bên nào bị phạt nặng hơn.", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Cơ sở đào tạo lái xe bị phạt từ 5.000.000 đồng đến 10.000.000 đồng, trong khi người điều khiển xe mô tô bị phạt từ 6.000.000 đồng đến 8.000.000 đồng. Do đó, cơ sở đào tạo lái xe có mức phạt cao hơn.", "gold_units": ["ND168-2024/D18/K7", "ND168-2024/D39/K3"], "required_numbers": [{"value": 6000000, "unit": "vnd"}, {"value": 8000000, "unit": "vnd"}, {"value": 5000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-027:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Là cán bộ phường, tôi muốn biết sự khác nhau về mức phạt tiền khi một trung tâm sát hạch lái xe thực hiện hành vi không có giấy phép xe tập hợp lệ, so với một người điều khiển xe mô tô có giấy phép không phù hợp với loại xe. Cả hai vi phạm xảy ra cùng ngày, cần biết mức phạt tối thiểu và tối đa cho từng bên, và bên nào nặng hơn.
- Đáp: Trung tâm sát hạch lái xe bị phạt từ 5.000.000 đồng đến 10.000.000 đồng, trong khi người điều khiển xe mô tô bị phạt từ 6.000.000 đồng đến 8.000.000 đồng. Vì mức phạt tối đa của trung tâm sát hạch lớn hơn, nên trung tâm sát hạch có mức phạt nặng hơn.
- ⚠ qua_dai (77 từ); chep_nguyen_van: “hạch lái xe thực hiện hành …”
- Ghi chú: So sánh giữa trung tâm sát hạch và người điều khiển xe mô tô.

```json
{"qid": "tD-so_sanh-027", "question": "Là cán bộ phường, tôi muốn biết sự khác nhau về mức phạt tiền khi một trung tâm sát hạch lái xe thực hiện hành vi không có giấy phép xe tập hợp lệ, so với một người điều khiển xe mô tô có giấy phép không phù hợp với loại xe. Cả hai vi phạm xảy ra cùng ngày, cần biết mức phạt tối thiểu và tối đa cho từng bên, và bên nào nặng hơn.", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Trung tâm sát hạch lái xe bị phạt từ 5.000.000 đồng đến 10.000.000 đồng, trong khi người điều khiển xe mô tô bị phạt từ 6.000.000 đồng đến 8.000.000 đồng. Vì mức phạt tối đa của trung tâm sát hạch lớn hơn, nên trung tâm sát hạch có mức phạt nặng hơn.", "gold_units": ["ND168-2024/D18/K7", "ND168-2024/D39/K3"], "required_numbers": [{"value": 6000000, "unit": "vnd"}, {"value": 8000000, "unit": "vnd"}, {"value": 5000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-027:2"}
```

### WD-so_sanh-028 · tier B · vai: sinh viên đi xe máy · kiểu: ngan · cosine TF-IDF 0.54

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)
Hiệu lực của trạng thái này: 2026-03-01 → nay
Mã điều khoản dùng được cho gold_units: ND336-2025/D11/K2, ND336-2025/D11/K2/a, ND336-2025/D11/K2/b, ND336-2025/D11/K2/c, ND336-2025/D11/K2/d

Điều 11. Xử phạt người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ kinh doanh vận tải vi phạm quy định về vận tải đường bộ
2. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với việc thực hiện một trong các hành vi vi phạm sau đây:
a) Điều khiển xe taxi không có đồng hồ tính tiền cước (đối với loại xe đăng ký sử dụng đồng hồ tính tiền) hoặc có nhưng không đúng quy định hoặc có nhưng không sử dụng đồng hồ để tính tiền cước theo yêu cầu của hành khách hoặc can thiệp để điều chỉnh tiền cước hiển thị trên đồng hồ;
b) Điều khiển xe taxi sử dụng phần mềm tính tiền mà trên xe không có thiết bị để kết nối trực tiếp với hành khách theo quy định;
c) Điều khiển xe taxi không sử dụng phần mềm tính tiền (đối với loại xe đăng ký sử dụng phần mềm tính tiền) hoặc sử dụng phần mềm tính tiền không bảo đảm các yêu cầu theo quy định;
d) Điều khiển xe kinh doanh vận tải hành khách theo tuyến cố định thu tiền vé cao hơn giá vé đã kê khai và niêm yết theo quy định.

### Nguồn 2
Văn bản: Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)
Hiệu lực của trạng thái này: 2026-03-01 → nay
Mã điều khoản dùng được cho gold_units: ND336-2025/D12/K3, ND336-2025/D12/K3/a, ND336-2025/D12/K3/b, ND336-2025/D12/K3/c, ND336-2025/D12/K3/d, ND336-2025/D12/K3/đ, ND336-2025/D12/K3/e, ND336-2025/D12/K3/g, ND336-2025/D12/K3/h, ND336-2025/D12/K3/i, ND336-2025/D12/K3/k, ND336-2025/D12/K3/l

Điều 12. Xử phạt các hành vi vi phạm quy định về vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
3. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với cá nhân, từ 6.000.000 đồng đến 10.000.000 đồng đối với tổ chức kinh doanh vận tải, dịch vụ hỗ trợ vận tải thực hiện một trong các hành vi vi phạm sau đây:
a) Sử dụng xe ô tô chở người từ 08 chỗ (không kể chỗ của người lái xe) trở lên hoặc xe ô tô chở người có thiết kế, cải tạo với số chỗ ít hơn 08 chỗ từ xe ô tô lớn hơn 08 chỗ (không kể chỗ của người lái xe) để kinh doanh vận tải hành khách bằng xe taxi;
b) Không bố trí người trực tiếp điều hành hoạt động vận tải hoặc có bố trí nhưng không đáp ứng đủ điều kiện theo quy định;
c) Sử dụng phương tiện thuộc sở hữu của thành viên hợp tác xã để kinh doanh vận tải bằng xe ô tô, xe bốn bánh có gắn động cơ mà không có hợp đồng dịch vụ giữa thành viên với hợp tác xã theo quy định hoặc sử dụng phương tiện không thuộc quyền sử dụng hợp pháp để kinh doanh vận tải bằng xe ô tô, xe bốn bánh có gắn động cơ;
d) Bến xe không xác nhận hoặc xác nhận không chính xác, đầy đủ các thông tin trong lệnh vận chuyển theo quy định hoặc xác nhận vào lệnh vận chuyển khi xe không có ở bến;
đ) Bến xe cho phương tiện xuất bến không đúng thời gian biểu đồ chạy xe đã được cơ quan quản lý tuyến công bố;
e) Không thực hiện chế độ báo cáo hoạt động kinh doanh vận tải của đơn vị theo quy định;
g) Không xây dựng hoặc không thực hiện các nhiệm vụ bảo đảm an toàn giao thông theo quy định;
…

### Điều khoản nêu chế tài áp cho hành vi trên (ND336-2025/D12/K8/a)
Mã điều khoản dùng được cho gold_units: ND336-2025/D12/K8/a

Điều 12. Xử phạt các hành vi vi phạm quy định về vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
8. Ngoài việc bị phạt tiền, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị áp dụng các hình thức xử phạt bổ sung sau đây:
a) Thực hiện hành vi vi phạm quy định tại điểm a, điểm c khoản 3 Điều này bị tước quyền sử dụng phù hiệu cấp cho xe ô tô tham gia kinh doanh vận tải từ 01 tháng đến 03 tháng (nếu có hoặc đã được cấp) đối với xe vi phạm;

### Điều khoản nêu chế tài áp cho hành vi trên (ND336-2025/D12/K8/b)
Mã điều khoản dùng được cho gold_units: ND336-2025/D12/K8/b

Điều 12. Xử phạt các hành vi vi phạm quy định về vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
8. Ngoài việc bị phạt tiền, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị áp dụng các hình thức xử phạt bổ sung sau đây:
b) Thực hiện hành vi vi phạm quy định tại điểm b khoản 3; điểm b khoản 4; điểm b, điểm h khoản 6 Điều này bị tước quyền sử dụng giấy phép kinh doanh vận tải từ 01 tháng đến 03 tháng.

[0] 1.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D11/K2)
[1] 2.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D11/K2)
[2] 3.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D12/K3)
[3] 5.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D12/K3)
[4] 6.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D12/K3)
[5] 10.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D12/K3)
[6] 01 tháng (thời hạn tước quyền sử dụng tối thiểu, nêu tại ND336-2025/D12/K8/a)
[7] 03 tháng (thời hạn tước quyền sử dụng tối đa, nêu tại ND336-2025/D12/K8/a)
[8] 01 tháng (thời hạn tước quyền sử dụng tối thiểu, nêu tại ND336-2025/D12/K8/b)
[9] 03 tháng (thời hạn tước quyền sử dụng tối đa, nêu tại ND336-2025/D12/K8/b)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi lái xe taxi không có đồng hồ tính tiền, còn bạn lái xe taxi có 8 chỗ trở lên, mức phạt tiền của hai trường hợp này có khác nhau không?
- Đáp: Lái xe taxi không có đồng hồ tính tiền bị phạt từ 1.000.000 đồng đến 2.000.000 đồng. Lái xe taxi có 8 chỗ trở lên bị phạt từ 3.000.000 đồng đến 5.000.000 đồng. Trường hợp có 8 chỗ trở lên nặng hơn.
- ⚠ chep_nguyen_van: “không có đồng hồ tính tiền …”

```json
{"qid": "tD-so_sanh-028", "question": "Tôi lái xe taxi không có đồng hồ tính tiền, còn bạn lái xe taxi có 8 chỗ trở lên, mức phạt tiền của hai trường hợp này có khác nhau không?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "B", "answer": "Lái xe taxi không có đồng hồ tính tiền bị phạt từ 1.000.000 đồng đến 2.000.000 đồng. Lái xe taxi có 8 chỗ trở lên bị phạt từ 3.000.000 đồng đến 5.000.000 đồng. Trường hợp có 8 chỗ trở lên nặng hơn.", "gold_units": ["ND336-2025/D11/K2", "ND336-2025/D12/K3"], "required_numbers": [{"value": 1000000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}, {"value": 5000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-028:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Nếu tôi điều khiển xe taxi sử dụng phần mềm tính tiền mà không có thiết bị kết nối, còn bạn điều khiển xe taxi có 8 chỗ trở lên, mức phạt tiền của hai trường hợp này có khác nhau không?
- Đáp: Lái xe taxi sử dụng phần mềm tính tiền mà không có thiết bị kết nối bị phạt từ 1.000.000 đồng đến 2.000.000 đồng. Lái xe taxi có 8 chỗ trở lên bị phạt từ 3.000.000 đồng đến 5.000.000 đồng. Trường hợp có 8 chỗ trở lên nặng hơn.
- ⚠ chep_nguyen_van: “dụng phần mềm tính tiền mà …”

```json
{"qid": "tD-so_sanh-028", "question": "Nếu tôi điều khiển xe taxi sử dụng phần mềm tính tiền mà không có thiết bị kết nối, còn bạn điều khiển xe taxi có 8 chỗ trở lên, mức phạt tiền của hai trường hợp này có khác nhau không?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "B", "answer": "Lái xe taxi sử dụng phần mềm tính tiền mà không có thiết bị kết nối bị phạt từ 1.000.000 đồng đến 2.000.000 đồng. Lái xe taxi có 8 chỗ trở lên bị phạt từ 3.000.000 đồng đến 5.000.000 đồng. Trường hợp có 8 chỗ trở lên nặng hơn.", "gold_units": ["ND336-2025/D11/K2", "ND336-2025/D12/K3"], "required_numbers": [{"value": 1000000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}, {"value": 5000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-028:2"}
```

### WD-so_sanh-029 · tier A · vai: tài xế xe tải · kiểu: tinh_huong_ban_than · cosine TF-IDF 0.67

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D12/K10

Điều 12. Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm khác về quy tắc giao thông đường bộ; sử dụng lòng đường, vỉa hè vào mục đích khác
10. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng đối với cá nhân, từ 8.000.000 đồng đến 12.000.000 đồng đối với tổ chức thực hiện hành vi không chấp hành yêu cầu kiểm tra, kiểm soát của người thi hành công vụ về bảo đảm trật tự, an toàn giao thông đường bộ, trừ các hành vi vi phạm quy định tại điểm b, điểm d khoản 11 Điều 6; điểm đ, điểm g khoản 9 Điều 7; điểm b, điểm d khoản 9 Điều 8; điểm c khoản 4 Điều 9; điểm b khoản 5 Điều 34 của Nghị định này.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D34/K5/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D34/K5/b

Điều 34. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển quá khổ giới hạn, xe quá tải trọng, xe bánh xích lưu hành đường bộ (kể cả xe ô tô chở hành khách)
5. Phạt tiền từ 40.000.000 đồng đến 50.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
b) Không chấp hành yêu cầu kiểm tra về trọng tải, tải trọng, khổ giới hạn xe, vận chuyển hàng siêu trường, siêu trọng của người thi hành công vụ; chuyển tải hoặc dùng các thủ đoạn khác để trốn tránh việc phát hiện xe chở quá tải, quá khổ.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D6/K11/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D6/K11/b

Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
11. Phạt tiền từ 30.000.000 đồng đến 40.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
b) Không chấp hành yêu cầu kiểm tra về nồng độ cồn của người thi hành công vụ;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D6/K11/d)
Mã điều khoản dùng được cho gold_units: ND168-2024/D6/K11/d

Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
11. Phạt tiền từ 30.000.000 đồng đến 40.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
d) Không chấp hành yêu cầu kiểm tra về chất ma túy hoặc chất kích thích khác mà pháp luật cấm sử dụng của người thi hành công vụ;

### Nguồn 2
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D6/K10, ND168-2024/D6/K10/a, ND168-2024/D6/K10/b

Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
10. Phạt tiền từ 20.000.000 đồng đến 22.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
a) Điều khiển xe không quan sát, giảm tốc độ hoặc dừng lại để bảo đảm an toàn theo quy định mà gây tai nạn giao thông; điều khiển xe chạy quá tốc độ quy định gây tai nạn giao thông; dừng xe, đỗ xe, quay đầu xe, lùi xe, tránh xe, vượt xe, chuyển hướng, chuyển làn đường không đúng quy định gây tai nạn giao thông; không đi đúng phần đường, làn đường, không giữ khoảng cách an toàn giữa hai xe theo quy định gây tai nạn giao thông hoặc đi vào đường có biển báo hiệu có nội dung cấm đi vào đối với loại phương tiện đang điều khiển gây tai nạn giao thông, trừ các hành vi vi phạm quy định tại điểm đ khoản 11 Điều này;
b) Vi phạm quy định tại một trong các điểm, khoản sau của Điều này mà gây tai nạn giao thông: điểm a, điểm b, điểm c, điểm d, điểm đ khoản 1; điểm c khoản 2; điểm b, điểm g, điểm h, điểm n, điểm o, điểm p, khoản 3; điểm a, điểm c, điểm d khoản 4; điểm c, điểm d, điểm e, điểm h, điểm n, điểm o, điểm q khoản 5; điểm b khoản 7; điểm b, điểm c, điểm d khoản 9 Điều này.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D6/K16/d)
Mã điều khoản dùng được cho gold_units: ND168-2024/D6/K16/d

Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
16. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển xe thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
d) Thực hiện hành vi quy định tại điểm a khoản 9, khoản 10, điểm đ khoản 11 Điều này bị trừ điểm giấy phép lái xe 10 điểm.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D6/K11/đ)
Mã điều khoản dùng được cho gold_units: ND168-2024/D6/K11/đ

Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
11. Phạt tiền từ 30.000.000 đồng đến 40.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
đ) Điều khiển xe đi ngược chiều trên đường cao tốc, lùi xe trên đường cao tốc, quay đầu xe trên đường cao tốc, trừ các xe ưu tiên đang đi làm nhiệm vụ khẩn cấp theo quy định.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D6/K1/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D6/K1/a

Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
1. Phạt tiền từ 400.000 đồng đến 600.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
a) Không chấp hành hiệu lệnh, chỉ dẫn của biển báo hiệu, vạch kẻ đường, trừ các hành vi vi phạm quy định tại điểm a, điểm c, điểm d, điểm đ khoản 2; điểm a, điểm d, điểm đ, điểm e, điểm n, điểm o khoản 3; điểm a, điểm b, điểm đ, điểm e, điểm i, điểm k, điểm l khoản 4; điểm a, điểm b, điểm c, điểm d, điểm đ, điểm i, điểm k khoản 5; điểm a khoản 6; khoản 7; điểm b, điểm d khoản 9; điểm a khoản 10; điểm đ khoản 11 Điều này;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D6/K1/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D6/K1/b

Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
1. Phạt tiền từ 400.000 đồng đến 600.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
b) Khi ra, vào vị trí dừng xe, đỗ xe không có tín hiệu báo cho người điều khiển phương tiện khác biết;

[0] 4.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D12/K10)
[1] 6.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D12/K10)
[2] 8.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D12/K10)
[3] 12.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D12/K10)
[4] 20.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D6/K10)
[5] 22.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D6/K10)
[6] 10 điểm (số điểm bị trừ, nêu tại ND168-2024/D6/K16/d)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là tài xế xe tải, khi không chấp hành yêu cầu kiểm tra trọng tải, tôi bị phạt bao nhiêu tiền và so sánh với mức phạt khi không chấp hành yêu cầu kiểm tra nồng độ cồn của người điều khiển xe ô tô?
- Đáp: Bạn sẽ bị phạt từ 40.000.000 đồng đến 50.000.000 đồng khi không chấp hành yêu cầu kiểm tra trọng tải, trong khi khi không chấp hành yêu cầu kiểm tra nồng độ cồn của người điều khiển xe ô tô, mức phạt là từ 30.000.000 đồng đến 40.000.000 đồng. Do đó, phạt tiền khi không chấp hành kiểm tra trọng tải lớn hơn.
- ⚠ chep_nguyen_van: “chấp hành yêu cầu kiểm tra …”
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-so_sanh-029", "question": "Tôi là tài xế xe tải, khi không chấp hành yêu cầu kiểm tra trọng tải, tôi bị phạt bao nhiêu tiền và so sánh với mức phạt khi không chấp hành yêu cầu kiểm tra nồng độ cồn của người điều khiển xe ô tô?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Bạn sẽ bị phạt từ 40.000.000 đồng đến 50.000.000 đồng khi không chấp hành yêu cầu kiểm tra trọng tải, trong khi khi không chấp hành yêu cầu kiểm tra nồng độ cồn của người điều khiển xe ô tô, mức phạt là từ 30.000.000 đồng đến 40.000.000 đồng. Do đó, phạt tiền khi không chấp hành kiểm tra trọng tải lớn hơn.", "gold_units": ["ND168-2024/D34/K5/b", "ND168-2024/D6/K11/b"], "required_numbers": [{"value": 4000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}, {"value": 8000000, "unit": "vnd"}, {"value": 12000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}, {"value": 22000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-029:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là tài xế xe tải, khi không chấp hành yêu cầu kiểm tra trọng tải, tôi bị trừ bao nhiêu điểm giấy phép, và so sánh với số điểm bị trừ khi điều khiển xe ô tô đi ngược chiều trên đường cao tốc?
- Đáp: Bạn sẽ bị trừ 10 điểm giấy phép khi không chấp hành yêu cầu kiểm tra trọng tải. Khi điều khiển xe ô tô đi ngược chiều trên đường cao tốc, mức trừ điểm là 10 điểm. Hai trường hợp đều trừ 10 điểm, nên không có sự khác nhau.
- ⚠ chep_nguyen_van: “chấp hành yêu cầu kiểm tra …”
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-so_sanh-029", "question": "Tôi là tài xế xe tải, khi không chấp hành yêu cầu kiểm tra trọng tải, tôi bị trừ bao nhiêu điểm giấy phép, và so sánh với số điểm bị trừ khi điều khiển xe ô tô đi ngược chiều trên đường cao tốc?", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Bạn sẽ bị trừ 10 điểm giấy phép khi không chấp hành yêu cầu kiểm tra trọng tải. Khi điều khiển xe ô tô đi ngược chiều trên đường cao tốc, mức trừ điểm là 10 điểm. Hai trường hợp đều trừ 10 điểm, nên không có sự khác nhau.", "gold_units": ["ND168-2024/D34/K5/b", "ND168-2024/D6/K11/đ"], "required_numbers": [{"value": 10, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-029:2"}
```

### WD-so_sanh-030 · tier A · vai: sinh viên đi xe máy · kiểu: tinh_huong_ban_than · cosine TF-IDF 0.48

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2026-08-15 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K8a

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
8a. Phạt tiền từ 12.000.000 đồng đến 14.000.000 đồng đối với người điều khiển xe ô tô không kinh doanh vận tải hành khách nhưng cho người có thu tiền hoặc ký hợp đồng, nhận đặt chỗ để chở người trên xe.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D20/K10/c)
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K10/c

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
10. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
c) Thực hiện hành vi vi phạm quy định tại khoản 8, khoản 8a Điều này bị trừ điểm giấy phép lái xe 06 điểm;

### Nguồn 2
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2026-08-15 → 2028-12-31
Mã điều khoản dùng được cho gold_units: ND168-2024/D26/K7, ND168-2024/D26/K7/a, ND168-2024/D26/K7/b, ND168-2024/D26/K7/c, ND168-2024/D26/K7/d, ND168-2024/D26/K7/đ, ND168-2024/D26/K7/e, ND168-2024/D26/K7/g, ND168-2024/D26/K7/h, ND168-2024/D26/K7/i

Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
7. Phạt tiền từ 5.000.000 đồng đến 6.000.000 đồng đối với cá nhân, từ 10.000.000 đồng đến 12.000.000 đồng đối với tổ chức kinh doanh vận tải, dịch vụ hỗ trợ vận tải thực hiện một trong các hành vi vi phạm sau đây:
a) Không thực hiện việc cung cấp, cập nhật, truyền, lưu trữ, quản lý thông tin, dữ liệu từ thiết bị giám sát hành trình theo quy định;
b) Không thực hiện đúng nội dung thông tin đã niêm yết trên xe theo quy định;
c) Sử dụng phương tiện kinh doanh vận tải không lắp thiết bị giám sát hành trình của xe (đối với hình thức kinh doanh vận tải có quy định phương tiện phải lắp thiết bị) hoặc lắp thiết bị nhưng thiết bị không hoạt động, không đúng quy chuẩn theo quy định hoặc làm sai lệch dữ liệu của thiết bị giám sát hành trình của xe ô tô;
d) Sử dụng xe trung chuyển chở hành khách không đúng quy định;
đ) Sử dụng lái xe điều khiển xe khách giường nằm hai tầng, xe ô tô đưa đón trẻ em mầm non, học sinh chưa đủ số năm kinh nghiệm theo quy định;
…

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D26/K12)
Mã điều khoản dùng được cho gold_units: ND168-2024/D26/K12

Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
12. Ngoài việc bị phạt tiền, cá nhân, tổ chức thực hiện hành vi vi phạm quy định tại điểm c khoản 2; điểm a, điểm b, điểm đ, điểm g khoản 4; điểm b, điểm c, điểm d, điểm đ, điểm e, điểm g khoản 7; điểm c khoản 8 Điều này còn bị áp dụng các hình thức xử phạt bổ sung tước quyền sử dụng phù hiệu từ 01 tháng đến 03 tháng (nếu có hoặc đã được cấp) đối với xe vi phạm.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D26/K14/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D26/K14/a

Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
14. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
a) Thực hiện hành vi quy định tại điểm đ khoản 2; điểm b, điểm c, điểm d khoản 6; điểm b, điểm c, điểm e, điểm i khoản 7 Điều này trong trường hợp cá nhân kinh doanh vận tải là người trực tiếp điều khiển phương tiện còn bị trừ điểm giấy phép lái xe 02 điểm;

[0] 12.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D20/K8a)
[1] 14.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D20/K8a)
[2] 06 điểm (số điểm bị trừ, nêu tại ND168-2024/D20/K10/c)
[3] 01 tháng (thời hạn tước quyền sử dụng tối thiểu, nêu tại ND168-2024/D26/K12)
[4] 03 tháng (thời hạn tước quyền sử dụng tối đa, nêu tại ND168-2024/D26/K12)
[5] 5.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D26/K7)
[6] 6.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D26/K7)
[7] 10.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D26/K7)
[8] 12.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D26/K7)
[9] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D26/K14/a)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là sinh viên đi xe máy, nhưng muốn biết so sánh mức phạt tiền và trừ điểm giữa người lái xe ô tô không kinh doanh vận tải nhưng thu tiền và người lái xe ô tô kinh doanh vận tải không lắp thiết bị giám sát hành trình.
- Đáp: Người lái xe ô tô không kinh doanh vận tải nhưng thu tiền sẽ bị phạt tiền từ 12.000.000 đồng đến 14.000.000 đồng và trừ 06 điểm giấy phép lái xe. Người lái xe ô tô kinh doanh vận tải không lắp thiết bị giám sát hành trình sẽ bị phạt tiền từ 5.000.000 đồng đến 12.000.000 đồng và tước quyền sử dụng xe từ 01 tháng đến 03 tháng. Mức phạt tiền và trừ điểm của người lái xe ô tô không kinh doanh vận tải nhưng thu tiền nặng hơn.
- ⚠ chep_nguyen_van: “doanh vận tải không lắp thiết …”
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-so_sanh-030", "question": "Tôi là sinh viên đi xe máy, nhưng muốn biết so sánh mức phạt tiền và trừ điểm giữa người lái xe ô tô không kinh doanh vận tải nhưng thu tiền và người lái xe ô tô kinh doanh vận tải không lắp thiết bị giám sát hành trình.", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Người lái xe ô tô không kinh doanh vận tải nhưng thu tiền sẽ bị phạt tiền từ 12.000.000 đồng đến 14.000.000 đồng và trừ 06 điểm giấy phép lái xe. Người lái xe ô tô kinh doanh vận tải không lắp thiết bị giám sát hành trình sẽ bị phạt tiền từ 5.000.000 đồng đến 12.000.000 đồng và tước quyền sử dụng xe từ 01 tháng đến 03 tháng. Mức phạt tiền và trừ điểm của người lái xe ô tô không kinh doanh vận tải nhưng thu tiền nặng hơn.", "gold_units": ["ND168-2024/D20/K8a", "ND168-2024/D20/K10/c", "ND168-2024/D26/K7", "ND168-2024/D26/K12"], "required_numbers": [{"value": 12000000, "unit": "vnd"}, {"value": 14000000, "unit": "vnd"}, {"value": 6, "unit": "diem"}, {"value": 1, "unit": "thang"}, {"value": 3, "unit": "thang"}, {"value": 5000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-030:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là sinh viên đi xe máy, muốn biết so sánh mức phạt tiền, trừ điểm và tước quyền sử dụng giữa người lái xe ô tô không kinh doanh vận tải nhưng thu tiền và người lái xe ô tô kinh doanh vận tải nhưng không lắp thiết bị giám sát hành trình.
- Đáp: Người lái xe ô tô không kinh doanh vận tải nhưng thu tiền sẽ bị phạt tiền từ 12.000.000 đồng đến 14.000.000 đồng và trừ 06 điểm giấy phép lái xe. Người lái xe ô tô kinh doanh vận tải nhưng không lắp thiết bị giám sát hành trình sẽ bị phạt tiền từ 5.000.000 đồng đến 12.000.000 đồng, trừ 02 điểm giấy phép lái xe và tước quyền sử dụng xe từ 01 tháng đến 03 tháng. Mức phạt tiền và trừ điểm của người lái xe ô tô không kinh doanh vận tải nhưng thu tiền nặng hơn.
- ⚠ qua_dai (54 từ); chep_nguyen_van: “không lắp thiết bị giám sát …”
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-so_sanh-030", "question": "Tôi là sinh viên đi xe máy, muốn biết so sánh mức phạt tiền, trừ điểm và tước quyền sử dụng giữa người lái xe ô tô không kinh doanh vận tải nhưng thu tiền và người lái xe ô tô kinh doanh vận tải nhưng không lắp thiết bị giám sát hành trình.", "as_of": "2026-11-03", "question_type": "so_sanh", "tier": "A", "answer": "Người lái xe ô tô không kinh doanh vận tải nhưng thu tiền sẽ bị phạt tiền từ 12.000.000 đồng đến 14.000.000 đồng và trừ 06 điểm giấy phép lái xe. Người lái xe ô tô kinh doanh vận tải nhưng không lắp thiết bị giám sát hành trình sẽ bị phạt tiền từ 5.000.000 đồng đến 12.000.000 đồng, trừ 02 điểm giấy phép lái xe và tước quyền sử dụng xe từ 01 tháng đến 03 tháng. Mức phạt tiền và trừ điểm của người lái xe ô tô không kinh doanh vận tải nhưng thu tiền nặng hơn.", "gold_units": ["ND168-2024/D20/K8a", "ND168-2024/D20/K10/c", "ND168-2024/D26/K7", "ND168-2024/D26/K12", "ND168-2024/D26/K14/a"], "required_numbers": [{"value": 12000000, "unit": "vnd"}, {"value": 14000000, "unit": "vnd"}, {"value": 6, "unit": "diem"}, {"value": 1, "unit": "thang"}, {"value": 3, "unit": "thang"}, {"value": 5000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-so_sanh-030:2"}
```

## muc_phat — mức phạt tiền / phạt cảnh cáo cho một hành vi

### WD-muc_phat-001 · tier A · vai: người mới học lái ô tô · kiểu: ngan

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2026-08-15 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K1, ND168-2024/D32/K1/a, ND168-2024/D32/K1/b

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
1. Phạt tiền từ 200.000 đồng đến 300.000 đồng đối với cá nhân, từ 400.000 đồng đến 600.000 đồng đối với tổ chức là chủ xe mô tô, xe gắn máy và các loại xe tương tự xe mô tô, các loại xe tương tự xe gắn máy thực hiện một trong các hành vi vi phạm sau đây:
a) Tự ý thay đổi nhãn hiệu, màu sơn của xe không đúng với chứng nhận đăng ký xe;
b) Đưa phương tiện không có chứng nhận kiểm định khí thải xe mô tô, xe gắn máy hoặc có nhưng đã hết hạn sử dụng hoặc sử dụng chứng nhận kiểm định khí thải xe mô tô, xe gắn máy không do cơ quan có thẩm quyền cấp.

[0] 200.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D32/K1)
[1] 300.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D32/K1)
[2] 400.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D32/K1)
[3] 600.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D32/K1)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Nếu tôi thay màu sơn xe máy mà không có giấy chứng nhận, mức phạt tiền là bao nhiêu?
- Đáp: Mức phạt tiền là từ 200.000 đồng đến 300.000 đồng.
- Ghi chú: Giả định xe máy là mô tô

```json
{"qid": "tD-muc_phat-001", "question": "Nếu tôi thay màu sơn xe máy mà không có giấy chứng nhận, mức phạt tiền là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Mức phạt tiền là từ 200.000 đồng đến 300.000 đồng.", "gold_units": ["ND168-2024/D32/K1"], "required_numbers": [{"value": 200000, "unit": "vnd"}, {"value": 300000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-001:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Khi tôi dùng giấy kiểm định khí thải đã hết hạn cho xe máy, tôi phải trả phạt tiền bao nhiêu?
- Đáp: Mức phạt tiền là từ 200.000 đồng đến 300.000 đồng.
- Ghi chú: Giả định xe máy là mô tô

```json
{"qid": "tD-muc_phat-001", "question": "Khi tôi dùng giấy kiểm định khí thải đã hết hạn cho xe máy, tôi phải trả phạt tiền bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Mức phạt tiền là từ 200.000 đồng đến 300.000 đồng.", "gold_units": ["ND168-2024/D32/K1"], "required_numbers": [{"value": 200000, "unit": "vnd"}, {"value": 300000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-001:2"}
```

### WD-muc_phat-002 · tier A · vai: cán bộ phường · kiểu: neu_van_ban

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D12/K6, ND168-2024/D12/K6/a, ND168-2024/D12/K6/b, ND168-2024/D12/K6/c, ND168-2024/D12/K6/d

Điều 12. Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm khác về quy tắc giao thông đường bộ; sử dụng lòng đường, vỉa hè vào mục đích khác
6. Phạt tiền từ 500.000 đồng đến 1.000.000 đồng đối với cá nhân, từ 1.000.000 đồng đến 2.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
a) Khi có điều kiện mà cố ý không cứu giúp người bị tai nạn giao thông đường bộ;
b) Lợi dụng việc xảy ra tai nạn giao thông đường bộ để hành hung, đe dọa, xúi giục, gây sức ép, làm mất trật tự, cản trở việc xử lý tai nạn giao thông đường bộ;
c) Cản trở người, phương tiện tham gia giao thông trên đường bộ; ném gạch, đất, đá, cát hoặc vật thể khác vào người, phương tiện đang tham gia giao thông trên đường bộ;
d) Chiếm dụng dải phân cách giữa của đường đôi làm nơi: bày, bán hàng hóa; để vật liệu xây dựng; để xe, trông, giữ xe.

[0] 500.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D12/K6)
[1] 1.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D12/K6)
[2] 2.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D12/K6)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Theo Nghị định 168/2024/NĐ-CP, nếu tôi không cứu giúp người bị tai nạn giao thông, mức phạt tiền là bao nhiêu?
- Đáp: Phạt tiền từ 500.000 đồng đến 1.000.000 đồng đối với cá nhân.
- ⚠ chep_nguyen_van: “cứu giúp người bị tai nạn …”

```json
{"qid": "tD-muc_phat-002", "question": "Theo Nghị định 168/2024/NĐ-CP, nếu tôi không cứu giúp người bị tai nạn giao thông, mức phạt tiền là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Phạt tiền từ 500.000 đồng đến 1.000.000 đồng đối với cá nhân.", "gold_units": ["ND168-2024/D12/K6"], "required_numbers": [{"value": 500000, "unit": "vnd"}, {"value": 1000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-002:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Theo Nghị định 168/2024/NĐ-CP, công ty tôi chiếm dụng dải phân cách đường để bán hàng, phạt tiền là bao nhiêu?
- Đáp: Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với tổ chức.

```json
{"qid": "tD-muc_phat-002", "question": "Theo Nghị định 168/2024/NĐ-CP, công ty tôi chiếm dụng dải phân cách đường để bán hàng, phạt tiền là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với tổ chức.", "gold_units": ["ND168-2024/D12/K6"], "required_numbers": [{"value": 1000000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-002:2"}
```

### WD-muc_phat-003 · tier A · vai: tài xế công nghệ · kiểu: tinh_huong_ban_than

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D39/K6

Điều 39. Xử phạt các hành vi vi phạm quy định về đào tạo, sát hạch lái xe
6. Phạt tiền từ 15.000.000 đồng đến 20.000.000 đồng đối với cá nhân, từ 30.000.000 đồng đến 40.000.000 đồng đối với tổ chức thực hiện hành vi tổ chức tuyển sinh, đào tạo lái xe mà không có giấy phép đào tạo lái xe.

[0] 15.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D39/K6)
[1] 20.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D39/K6)
[2] 30.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D39/K6)
[3] 40.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D39/K6)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là tài xế công nghệ, vừa tổ chức một lớp học lái xe cho những người mới bắt đầu mà không có giấy phép đào tạo. Mức phạt tiền mà tôi phải chịu là bao nhiêu?
- Đáp: Bạn sẽ bị phạt tiền từ 15.000.000 đồng đến 20.000.000 đồng. (Điều 39, Khoản 6 Nghị định 168/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “không có giấy phép đào tạo …”

```json
{"qid": "tD-muc_phat-003", "question": "Tôi là tài xế công nghệ, vừa tổ chức một lớp học lái xe cho những người mới bắt đầu mà không có giấy phép đào tạo. Mức phạt tiền mà tôi phải chịu là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Bạn sẽ bị phạt tiền từ 15.000.000 đồng đến 20.000.000 đồng. (Điều 39, Khoản 6 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D39/K6"], "required_numbers": [{"value": 15000000, "unit": "vnd"}, {"value": 20000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-003:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Công ty tôi đã tổ chức một khóa đào tạo lái xe cho nhân viên mà không có giấy phép đào tạo. Phạt tiền mà công ty phải chịu là bao nhiêu?
- Đáp: Công ty sẽ bị phạt tiền từ 30.000.000 đồng đến 40.000.000 đồng. (Điều 39, Khoản 6 Nghị định 168/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “không có giấy phép đào tạo …”

```json
{"qid": "tD-muc_phat-003", "question": "Công ty tôi đã tổ chức một khóa đào tạo lái xe cho nhân viên mà không có giấy phép đào tạo. Phạt tiền mà công ty phải chịu là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Công ty sẽ bị phạt tiền từ 30.000.000 đồng đến 40.000.000 đồng. (Điều 39, Khoản 6 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D39/K6"], "required_numbers": [{"value": 30000000, "unit": "vnd"}, {"value": 40000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-003:2"}
```

### WD-muc_phat-004 · tier A · vai: cán bộ phường · kiểu: tinh_huong_ban_than

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D26/K9, ND168-2024/D26/K9/a, ND168-2024/D26/K9/b

Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
9. Phạt tiền từ 20.000.000 đồng đến 40.000.000 đồng đối với đơn vị sản xuất, lắp ráp, nhập khẩu thiết bị giám sát hành trình của xe ô tô, đơn vị cung cấp dịch vụ liên quan đến giám sát hành trình, ghi nhận hình ảnh người lái xe thực hiện một trong các hành vi sau:
a) Đơn vị sản xuất, lắp ráp, nhập khẩu thiết bị giám sát hành trình của xe ô tô không có nhân sự cho từng vị trí công việc theo quy định;
b) Đơn vị sản xuất, lắp ráp, nhập khẩu thiết bị giám sát hành trình của xe ô tô không báo cáo về việc cập nhật, thay đổi phần mềm của thiết bị theo quy định.

[0] 20.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D26/K9)
[1] 40.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D26/K9)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là chủ doanh nghiệp sản xuất thiết bị giám sát hành trình cho xe ô tô, nhưng chưa bố trí nhân sự cho từng vị trí công việc theo quy định. Mức phạt tiền mà công ty tôi phải chịu là bao nhiêu?
- Đáp: Công ty bạn sẽ bị phạt tiền từ 20.000.000 đồng đến 40.000.000 đồng. (khoản 9 Điều 26 Nghị định 168/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “cho từng vị trí công việc …”
- Ghi chú: Giả định công ty là đơn vị sản xuất, không có nhân sự cho từng vị trí công việc.

```json
{"qid": "tD-muc_phat-004", "question": "Tôi là chủ doanh nghiệp sản xuất thiết bị giám sát hành trình cho xe ô tô, nhưng chưa bố trí nhân sự cho từng vị trí công việc theo quy định. Mức phạt tiền mà công ty tôi phải chịu là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Công ty bạn sẽ bị phạt tiền từ 20.000.000 đồng đến 40.000.000 đồng. (khoản 9 Điều 26 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D26/K9"], "required_numbers": [{"value": 20000000, "unit": "vnd"}, {"value": 40000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-004:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là chủ doanh nghiệp cung cấp thiết bị giám sát hành trình cho xe ô tô, nhưng chưa báo cáo việc cập nhật, thay đổi phần mềm của thiết bị theo quy định. Phạt tiền mà công ty tôi phải chịu là bao nhiêu?
- Đáp: Công ty bạn sẽ bị phạt tiền từ 20.000.000 đồng đến 40.000.000 đồng. (khoản 9 Điều 26 Nghị định 168/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “cập nhật thay đổi phần mềm …”
- Ghi chú: Giả định công ty là đơn vị cung cấp dịch vụ liên quan đến giám sát hành trình, chưa báo cáo cập nhật phần mềm.

```json
{"qid": "tD-muc_phat-004", "question": "Tôi là chủ doanh nghiệp cung cấp thiết bị giám sát hành trình cho xe ô tô, nhưng chưa báo cáo việc cập nhật, thay đổi phần mềm của thiết bị theo quy định. Phạt tiền mà công ty tôi phải chịu là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Công ty bạn sẽ bị phạt tiền từ 20.000.000 đồng đến 40.000.000 đồng. (khoản 9 Điều 26 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D26/K9"], "required_numbers": [{"value": 20000000, "unit": "vnd"}, {"value": 40000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-004:2"}
```

### WD-muc_phat-005 · tier A · vai: cán bộ phường · kiểu: tinh_huong_nguoi_khac

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D8/K2, ND168-2024/D8/K2/a, ND168-2024/D8/K2/b, ND168-2024/D8/K2/c, ND168-2024/D8/K2/d, ND168-2024/D8/K2/đ

Điều 8. Xử phạt người điều khiển xe máy chuyên dùng vi phạm quy tắc giao thông đường bộ
2. Phạt tiền từ 600.000 đồng đến 800.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
a) Dừng xe, đỗ xe trên phần đường xe chạy ở đoạn đường ngoài đô thị nơi có lề đường rộng; dừng xe, đỗ xe không sát mép đường phía bên phải theo chiều đi ở nơi đường có lề đường hẹp hoặc không có lề đường; dừng xe, đỗ xe ngược với chiều lưu thông của làn đường; dừng xe, đỗ xe trên dải phân cách cố định ở giữa hai phần đường xe chạy; dừng xe, đỗ xe không đúng vị trí quy định ở những đoạn đường đã có bố trí nơi dừng xe, đỗ xe; đỗ xe trên dốc không chèn bánh; dừng xe nơi có biển “Cấm dừng xe và đỗ xe”; đỗ xe nơi có biển “Cấm đỗ xe” hoặc biển “Cấm dừng xe và đỗ xe”, trừ hành vi vi phạm quy định tại điểm b khoản 6 Điều này;
…

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D8/K6/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D8/K6/b

Điều 8. Xử phạt người điều khiển xe máy chuyên dùng vi phạm quy tắc giao thông đường bộ
6. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
b) Dừng xe, đỗ xe trên đường cao tốc không đúng nơi quy định; không có báo hiệu bằng đèn khẩn cấp khi gặp sự cố kỹ thuật hoặc bất khả kháng khác buộc phải dừng xe, đỗ xe ở làn dừng xe khẩn cấp hoặc dải dừng xe khẩn cấp trên đường cao tốc; không có báo hiệu bằng đèn khẩn cấp, không đặt biển cảnh báo “Chú ý xe đỗ” (hoặc đèn cảnh báo) về phía sau xe khoảng cách tối thiểu 150 mét khi gặp sự cố kỹ thuật hoặc bất khả kháng khác buộc phải dừng xe, đỗ xe trên một phần làn đường xe chạy trên đường cao tốc;

[0] 600.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D8/K2)
[1] 800.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D8/K2)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Công ty tôi đang vận chuyển hàng hóa, một nhân viên đã dừng xe máy của mình trên lề đường rộng, không sát mép bên phải, trong khu vực ngoài đô thị. Tôi muốn biết mức phạt tiền mà anh ấy phải chịu?
- Đáp: Nhân viên sẽ bị phạt tiền từ 600.000 đồng đến 800.000 đồng. (Điều 8, Khoản 2 Nghị định 168/2024/NĐ-CP)

```json
{"qid": "tD-muc_phat-005", "question": "Công ty tôi đang vận chuyển hàng hóa, một nhân viên đã dừng xe máy của mình trên lề đường rộng, không sát mép bên phải, trong khu vực ngoài đô thị. Tôi muốn biết mức phạt tiền mà anh ấy phải chịu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Nhân viên sẽ bị phạt tiền từ 600.000 đồng đến 800.000 đồng. (Điều 8, Khoản 2 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D8/K2"], "required_numbers": [{"value": 600000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-005:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Anh tôi lái xe máy chuyên dùng dừng xe trên dải dừng xe khẩn cấp của đường cao tốc khi gặp sự cố kỹ thuật, không bật đèn khẩn cấp. Anh ấy đang lo lắng về mức phạt tiền. Bạn có thể cho biết?
- Đáp: Anh sẽ bị phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng. (Điều 8, Khoản 6 b Nghị định 168/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “khi gặp sự cố kỹ thuật …”

```json
{"qid": "tD-muc_phat-005", "question": "Anh tôi lái xe máy chuyên dùng dừng xe trên dải dừng xe khẩn cấp của đường cao tốc khi gặp sự cố kỹ thuật, không bật đèn khẩn cấp. Anh ấy đang lo lắng về mức phạt tiền. Bạn có thể cho biết?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Anh sẽ bị phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng. (Điều 8, Khoản 6 b Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D8/K6/b"], "required_numbers": [{"value": 600000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-005:2"}
```

### WD-muc_phat-006 · tier A · vai: phụ huynh có con dưới 18 tuổi · kiểu: tinh_huong_ban_than

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2026-08-15 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D8/K6, ND168-2024/D8/K6/a, ND168-2024/D8/K6/b, ND168-2024/D8/K6/c, ND168-2024/D8/K6/d, ND168-2024/D8/K6/đ, ND168-2024/D8/K6/e, ND168-2024/D8/K6/g, ND168-2024/D8/K6/h, ND168-2024/D8/K6/i

Điều 8. Xử phạt người điều khiển xe máy chuyên dùng vi phạm quy tắc giao thông đường bộ
6. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
a) Chạy quá tốc độ quy định trên 20 km/h;
b) Dừng xe, đỗ xe trên đường cao tốc không đúng nơi quy định; không có báo hiệu bằng đèn khẩn cấp khi gặp sự cố kỹ thuật hoặc bất khả kháng khác buộc phải dừng xe, đỗ xe ở làn dừng xe khẩn cấp hoặc dải dừng xe khẩn cấp trên đường cao tốc; không có báo hiệu bằng đèn khẩn cấp, không đặt biển cảnh báo “Chú ý xe đỗ” (hoặc đèn cảnh báo) về phía sau xe khoảng cách tối thiểu 150 mét khi gặp sự cố kỹ thuật hoặc bất khả kháng khác buộc phải dừng xe, đỗ xe trên một phần làn đường xe chạy trên đường cao tốc;
c) Điều khiển xe trên đường mà trong máu hoặc hơi thở có nồng độ cồn nhưng chưa vượt quá 50 miligam/100 mililít máu hoặc chưa vượt quá 0,25 miligam/1 lít khí thở;
d) Đi vào khu vực cấm, đường có biển báo hiệu có nội dung cấm đi vào đối với loại phương tiện đang điều khiển, trừ các hành vi vi phạm quy định tại điểm d khoản 7, điểm đ khoản 9 Điều này và các trường hợp xe ưu tiên đang đi làm nhiệm vụ khẩn cấp theo quy định;
đ) Không đi bên phải theo chiều đi của mình; đi không đúng phần đường hoặc làn đường quy định (làn cùng chiều hoặc làn ngược chiều); điều khiển xe đi qua dải phân cách cố định ở giữa hai phần đường xe chạy, trừ các hành vi vi phạm quy định tại điểm e khoản 6, điểm d khoản 7, điểm đ khoản 9 Điều này;
…

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D8/K7/d)
Mã điều khoản dùng được cho gold_units: ND168-2024/D8/K7/d

Điều 8. Xử phạt người điều khiển xe máy chuyên dùng vi phạm quy tắc giao thông đường bộ
7. Phạt liền từ 6.000.000 đồng đến 8.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
d) Đi ngược chiều của đường một chiều, đi ngược chiều trên đường có biển “Cấm đi ngược chiều”, trừ các hành vi vi phạm quy định tại điểm đ khoản 9 Điều này và các trường hợp xe ưu tiên đang đi làm nhiệm vụ khẩn cấp theo quy định.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D8/K9/đ)
Mã điều khoản dùng được cho gold_units: ND168-2024/D8/K9/đ

Điều 8. Xử phạt người điều khiển xe máy chuyên dùng vi phạm quy tắc giao thông đường bộ
9. Phạt tiền từ 18.000.000 đồng đến 20.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
đ) Lùi xe trên đường cao tốc; đi ngược chiều trên đường cao tốc; quay đầu xe trên đường cao tốc;

[0] 3.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D8/K6)
[1] 5.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D8/K6)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi đang lái xe máy chuyên dùng trên đường cao tốc, tốc độ của tôi vượt quá giới hạn quy định hơn 20 km/h. Tôi sẽ bị phạt tiền bao nhiêu?
- Đáp: Bạn sẽ bị phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng. (Điều 8, Khoản 6, Nghị định 168/2024/NĐ-CP)
- Ghi chú: Xe máy chuyên dùng

```json
{"qid": "tD-muc_phat-006", "question": "Tôi đang lái xe máy chuyên dùng trên đường cao tốc, tốc độ của tôi vượt quá giới hạn quy định hơn 20 km/h. Tôi sẽ bị phạt tiền bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Bạn sẽ bị phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng. (Điều 8, Khoản 6, Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D8/K6"], "required_numbers": [{"value": 3000000, "unit": "vnd"}, {"value": 5000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-006:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi lái xe máy chuyên dùng trên đường một chiều, nhưng lại đi ngược chiều khi có biển “Cấm đi ngược chiều”. Tôi sẽ bị phạt tiền bao nhiêu?
- Đáp: Bạn sẽ bị phạt tiền từ 6.000.000 đồng đến 8.000.000 đồng. (Điều 8, Khoản 7, Nghị định 168/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “có biển cấm đi ngược chiều …”
- Ghi chú: Xe máy chuyên dùng

```json
{"qid": "tD-muc_phat-006", "question": "Tôi lái xe máy chuyên dùng trên đường một chiều, nhưng lại đi ngược chiều khi có biển “Cấm đi ngược chiều”. Tôi sẽ bị phạt tiền bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Bạn sẽ bị phạt tiền từ 6.000.000 đồng đến 8.000.000 đồng. (Điều 8, Khoản 7, Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D8/K7/d"], "required_numbers": [], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-006:2"}
```

### WD-muc_phat-007 · tier A · vai: sinh viên đi xe máy · kiểu: tinh_huong_ban_than

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K3, ND168-2024/D20/K3/a, ND168-2024/D20/K3/b, ND168-2024/D20/K3/c, ND168-2024/D20/K3/d, ND168-2024/D20/K3/đ, ND168-2024/D20/K3/e, ND168-2024/D20/K3/g, ND168-2024/D20/K3/h, ND168-2024/D20/K3/i, ND168-2024/D20/K3/k

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
3. Phạt tiền từ 600.000 đồng đến 800.000 đồng đối với một trong các hành vi vi phạm sau đây:
a) Không đóng cửa lên xuống khi xe đang chạy;
b) Để người ngồi trên xe khi xe xuống phà, đang trên phà và khi lên bến (trừ người lái xe, trẻ em, phụ nữ mang thai, người già yếu, người bệnh, người khuyết tật);
c) Không chạy đúng tuyến đường, lịch trình, hành trình vận tải được phép hoạt động theo quy định;
d) Để người mắc võng nằm trên xe khi xe đang chạy;
đ) Sắp xếp, chằng buộc hành lý, hàng hóa không bảo đảm an toàn; để rơi hành lý, hàng hóa trên xe xuống đường; để hàng hóa trong khoang chở hành khách;
e) Chở hành lý, hàng hóa vượt quá kích thước bao ngoài của xe;
g) Điều khiển xe vận tải hành khách không có nhân viên phục vụ trên xe đối với những xe quy định phải có nhân viên phục vụ;
h) Điều khiển xe ô tô kinh doanh vận tải không có dây đai an toàn tại các vị trí ghế ngồi, giường nằm theo quy định (trừ xe buýt nội tỉnh);
i) Điều khiển xe ô tô kinh doanh vận tải không có hướng dẫn cho hành khách về an toàn giao thông và thoát hiểm khi xảy ra sự cố trên xe theo quy định;
k) Điều khiển xe không niêm yết hành trình chạy xe hoặc niêm yết hành trình chạy xe không đúng với hành trình đã được cơ quan có thẩm quyền cấp phép.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D20/K10/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K10/a

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
10. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
a) Thực hiện hành vi quy định tại điểm c, điểm d, điểm e khoản 3; điểm a, điểm b, điểm c, điểm d, điểm đ, điểm e, điểm g, điểm h, điểm i, điểm k, điểm m khoản 5; khoản 6; khoản 7 Điều này bị trừ điểm giấy phép lái xe 02 điểm;

[0] 600.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D20/K3)
[1] 800.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D20/K3)
[2] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D20/K10/a)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là sinh viên, đang lái xe ô tô chở hành khách, và trong lúc di chuyển tôi quên đóng cửa xe. Mức phạt tiền và số điểm bị trừ là bao nhiêu?
- Đáp: Bạn sẽ bị phạt tiền từ 600.000 đồng đến 800.000 đồng và bị trừ 02 điểm giấy phép lái xe. (Điều 20 Khoản 3 và Khoản 10 Điều 20 Nghị định 168/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “xe ô tô chở hành khách …”
- Ghi chú: Giả định người lái xe là sinh viên, nhưng vẫn lái xe ô tô chở hành khách để phù hợp với quy định nguồn.

```json
{"qid": "tD-muc_phat-007", "question": "Tôi là sinh viên, đang lái xe ô tô chở hành khách, và trong lúc di chuyển tôi quên đóng cửa xe. Mức phạt tiền và số điểm bị trừ là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Bạn sẽ bị phạt tiền từ 600.000 đồng đến 800.000 đồng và bị trừ 02 điểm giấy phép lái xe. (Điều 20 Khoản 3 và Khoản 10 Điều 20 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D20/K3", "ND168-2024/D20/K10/a"], "required_numbers": [{"value": 600000, "unit": "vnd"}, {"value": 800000, "unit": "vnd"}, {"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-007:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là sinh viên, đang lái xe ô tô chở hành khách, và khi xe đang trên cạn, tôi để một người ngồi trên xe mà không được phép. Phạt tiền và điểm trừ là bao nhiêu?
- Đáp: Bạn sẽ bị phạt tiền từ 600.000 đồng đến 800.000 đồng và bị trừ 02 điểm giấy phép lái xe. (Điều 20 Khoản 3 và Khoản 10 Điều 20 Nghị định 168/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “xe ô tô chở hành khách …”
- Ghi chú: Giả định người lái xe là sinh viên, nhưng vẫn lái xe ô tô chở hành khách để phù hợp với quy định nguồn.

```json
{"qid": "tD-muc_phat-007", "question": "Tôi là sinh viên, đang lái xe ô tô chở hành khách, và khi xe đang trên cạn, tôi để một người ngồi trên xe mà không được phép. Phạt tiền và điểm trừ là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Bạn sẽ bị phạt tiền từ 600.000 đồng đến 800.000 đồng và bị trừ 02 điểm giấy phép lái xe. (Điều 20 Khoản 3 và Khoản 10 Điều 20 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D20/K3", "ND168-2024/D20/K10/a"], "required_numbers": [{"value": 600000, "unit": "vnd"}, {"value": 800000, "unit": "vnd"}, {"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-007:2"}
```

### WD-muc_phat-008 · tier A · vai: tài xế công nghệ · kiểu: ngan

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D22/K1, ND168-2024/D22/K1/a, ND168-2024/D22/K1/b

Điều 22. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển hàng siêu trường, siêu trọng
1. Phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
a) Chở hàng siêu trường, siêu trọng không có báo hiệu kích thước của hàng theo quy định;
b) Không thực hiện đúng quy định trong giấy phép lưu hành, trừ các hành vi vi phạm quy định tại khoản 2; điểm b, điểm c, điểm d khoản 3 Điều này.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D22/K6/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D22/K6/a

Điều 22. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển hàng siêu trường, siêu trọng
6. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
a) Thực hiện hành vi quy định tại khoản 1 Điều này bị trừ điểm giấy phép lái xe 02 điểm;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D22/K2)
Mã điều khoản dùng được cho gold_units: ND168-2024/D22/K2

Điều 22. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển hàng siêu trường, siêu trọng
2. Phạt tiền từ 8.000.000 đồng đến 10.000.000 đồng đối với hành vi chở hàng siêu trường, siêu trọng có giấy phép lưu hành còn giá trị sử dụng nhưng kích thước bao ngoài của xe (sau khi đã xếp hàng lên xe) vượt quá quy định trong giấy phép lưu hành.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D22/K3/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D22/K3/b

Điều 22. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển hàng siêu trường, siêu trọng
3. Phạt tiền từ 13.000.000 đồng đến 15.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
b) Chở hàng siêu trường, siêu trọng có giấy phép lưu hành còn giá trị sử dụng nhưng tổng trọng lượng (sau khi đã xếp hàng lên xe) vượt quá quy định trong giấy phép lưu hành;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D22/K3/c)
Mã điều khoản dùng được cho gold_units: ND168-2024/D22/K3/c

Điều 22. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển hàng siêu trường, siêu trọng
3. Phạt tiền từ 13.000.000 đồng đến 15.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
c) Chở hàng siêu trường, siêu trọng có giấy phép lưu hành còn giá trị sử dụng nhưng đi không đúng tuyến đường quy định trong giấy phép lưu hành;

[0] 2.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D22/K1)
[1] 3.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D22/K1)
[2] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D22/K6/a)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi đang vận chuyển hàng siêu trọng mà không treo biển kích thước, mức phạt tiền sẽ là bao nhiêu?
- Đáp: Bạn sẽ bị phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng. (Điều 22 Khoản 1 Nghị định 168/2024/NĐ-CP)

```json
{"qid": "tD-muc_phat-008", "question": "Tôi đang vận chuyển hàng siêu trọng mà không treo biển kích thước, mức phạt tiền sẽ là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Bạn sẽ bị phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng. (Điều 22 Khoản 1 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D22/K1"], "required_numbers": [{"value": 2000000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-008:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Nếu tôi chở hàng siêu trọng mà không treo biển kích thước, tôi sẽ mất bao nhiêu điểm giấy phép lái xe?
- Đáp: Bạn sẽ bị trừ 02 điểm giấy phép lái xe. (Điều 22 Khoản 6 Nghị định 168/2024/NĐ-CP)

```json
{"qid": "tD-muc_phat-008", "question": "Nếu tôi chở hàng siêu trọng mà không treo biển kích thước, tôi sẽ mất bao nhiêu điểm giấy phép lái xe?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Bạn sẽ bị trừ 02 điểm giấy phép lái xe. (Điều 22 Khoản 6 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D22/K6/a"], "required_numbers": [{"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-008:2"}
```

### WD-muc_phat-009 · tier A · vai: sinh viên đi xe máy · kiểu: tinh_huong_ban_than

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K7

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
7. Phạt tiền từ 5.000.000 đồng đến 7.000.000 đồng đối với hành vi vi phạm điều khiển xe chở hành khách không có hoặc không gắn phù hiệu theo quy định hoặc có nhưng đã hết giá trị sử dụng hoặc sử dụng phù hiệu không do cơ quan có thẩm quyền cấp.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D20/K10/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K10/a

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
10. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
a) Thực hiện hành vi quy định tại điểm c, điểm d, điểm e khoản 3; điểm a, điểm b, điểm c, điểm d, điểm đ, điểm e, điểm g, điểm h, điểm i, điểm k, điểm m khoản 5; khoản 6; khoản 7 Điều này bị trừ điểm giấy phép lái xe 02 điểm;

[0] 5.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D20/K7)
[1] 7.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D20/K7)
[2] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D20/K10/a)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi lái xe ô tô chở hành khách mà không có biển hiệu hoặc biển hiệu hết hạn, tôi sẽ bị phạt tiền bao nhiêu và mất bao nhiêu điểm?
- Đáp: Bạn sẽ bị phạt tiền từ 5.000.000 đồng đến 7.000.000 đồng và bị trừ 02 điểm.
- ⚠ chep_nguyen_van: “xe ô tô chở hành khách …”
- Ghi chú: Xe là ô tô chở hành khách, không phải xe máy

```json
{"qid": "tD-muc_phat-009", "question": "Tôi lái xe ô tô chở hành khách mà không có biển hiệu hoặc biển hiệu hết hạn, tôi sẽ bị phạt tiền bao nhiêu và mất bao nhiêu điểm?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Bạn sẽ bị phạt tiền từ 5.000.000 đồng đến 7.000.000 đồng và bị trừ 02 điểm.", "gold_units": ["ND168-2024/D20/K7", "ND168-2024/D20/K10/a"], "required_numbers": [{"value": 5000000, "unit": "vnd"}, {"value": 7000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-009:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi lái xe ô tô chở hành khách mà biển hiệu đã hết hạn, mức phạt tiền và điểm trừ là bao nhiêu?
- Đáp: Bạn sẽ bị phạt tiền từ 5.000.000 đồng đến 7.000.000 đồng và bị trừ 02 điểm.
- ⚠ chep_nguyen_van: “xe ô tô chở hành khách …”
- Ghi chú: Xe là ô tô chở hành khách, không phải xe máy

```json
{"qid": "tD-muc_phat-009", "question": "Tôi lái xe ô tô chở hành khách mà biển hiệu đã hết hạn, mức phạt tiền và điểm trừ là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Bạn sẽ bị phạt tiền từ 5.000.000 đồng đến 7.000.000 đồng và bị trừ 02 điểm.", "gold_units": ["ND168-2024/D20/K7", "ND168-2024/D20/K10/a"], "required_numbers": [{"value": 5000000, "unit": "vnd"}, {"value": 7000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-009:2"}
```

### WD-muc_phat-010 · tier A · vai: sinh viên đi xe máy · kiểu: tinh_huong_nguoi_khac

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2026-08-15 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K2, ND168-2024/D21/K2/a, ND168-2024/D21/K2/b, ND168-2024/D21/K2/c, ND168-2024/D21/K2/d, ND168-2024/D21/K2/đ

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
2. Phạt tiền từ 800.000 đồng đến 1.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
a) Điều khiển xe (kể cả rơ moóc và sơ mi rơ moóc) chở hàng vượt trọng tải (khối lượng hàng chuyên chở) cho phép tham gia giao thông được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe trên 10% đến 30% (trừ xe xi téc chở chất lỏng), trên 20% đến 30% đối với xe xi téc chở chất lỏng;
b) Chở hàng trên nóc thùng xe; chở hàng vượt quá bề rộng thùng xe (kể cả bề rộng rơ moóc và sơ mi rơ moóc); chở hàng vượt phía trước, phía sau thùng xe (kể cả rơ moóc và sơ mi rơ moóc) trên 10% chiều dài toàn bộ của xe theo thiết kế được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe, trừ hành vi vi phạm quy định tại điểm d khoản 8 Điều 21 Nghị định này
c) Chở người trên mui xe;
d) Điều khiển xe kéo theo rơ moóc, sơ mi rơ moóc mà khối lượng toàn bộ (bao gồm khối lượng bản thân rơ moóc, sơ mi rơ moóc và khối lượng hàng chuyên chở) của rơ moóc, sơ mi rơ moóc vượt khối lượng cho phép kéo theo được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe trên 10% đến 30%;
…

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D21/K13/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K13/a

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
13. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
a) Thực hiện hành vi quy định tại điểm b, điểm c, điểm đ khoản 2; điểm a khoản 3; khoản 4; khoản 5; điểm c, điểm d, điểm đ khoản 6 Điều này bị trừ điểm giấy phép lái xe (khi điều khiển xe ô tô) 02 điểm;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D21/K8/d)
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K8/d

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
8. Phạt tiền từ 8.000.000 đồng đến 12.000.000 đồng đối với một trong các hành vi sau đây:
d) Chở thiết bị có hình dạng thùng hoặc có hình dạng như công-ten-nơ (không phải công-ten-nơ) vượt quá chiều dài toàn bộ được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của rơ moóc, sơ mi rơ moóc; chở loại hàng không đúng với thông tin ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của rơ moóc, sơ mi rơ moóc;

[0] 800.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D21/K2)
[1] 1.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D21/K2)
[2] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D21/K13/a)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Anh tôi lái xe tải chở hàng trên thùng xe, vượt 15% chiều dài thùng. Tôi muốn biết mức phạt tiền và điểm bị trừ?
- Đáp: Mức phạt tiền là từ 800.000 đồng đến 1.000.000 đồng và người điều khiển bị trừ 02 điểm giấy phép lái xe.

```json
{"qid": "tD-muc_phat-010", "question": "Anh tôi lái xe tải chở hàng trên thùng xe, vượt 15% chiều dài thùng. Tôi muốn biết mức phạt tiền và điểm bị trừ?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Mức phạt tiền là từ 800.000 đồng đến 1.000.000 đồng và người điều khiển bị trừ 02 điểm giấy phép lái xe.", "gold_units": ["ND168-2024/D21/K2", "ND168-2024/D21/K13/a"], "required_numbers": [{"value": 800000, "unit": "vnd"}, {"value": 1000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-010:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Công ty tôi thuê xe tải chở hàng vượt trọng tải 12%. Tôi muốn biết mức phạt tiền và điểm bị trừ?
- Đáp: Mức phạt tiền là từ 800.000 đồng đến 1.000.000 đồng và người điều khiển bị trừ 02 điểm giấy phép lái xe.

```json
{"qid": "tD-muc_phat-010", "question": "Công ty tôi thuê xe tải chở hàng vượt trọng tải 12%. Tôi muốn biết mức phạt tiền và điểm bị trừ?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Mức phạt tiền là từ 800.000 đồng đến 1.000.000 đồng và người điều khiển bị trừ 02 điểm giấy phép lái xe.", "gold_units": ["ND168-2024/D21/K2", "ND168-2024/D21/K13/a"], "required_numbers": [{"value": 800000, "unit": "vnd"}, {"value": 1000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-010:2"}
```

### WD-muc_phat-011 · tier A · vai: chủ doanh nghiệp vận tải · kiểu: neu_van_ban

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K9, ND168-2024/D32/K9/a, ND168-2024/D32/K9/b, ND168-2024/D32/K9/c, ND168-2024/D32/K9/d, ND168-2024/D32/K9/đ, ND168-2024/D32/K9/e

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
9. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng đối với cá nhân, từ 8.000.000 đồng đến 12.000.000 đồng đối với tổ chức là chủ xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ, xe máy chuyên dùng và các loại xe tương tự xe ô tô thực hiện một trong các hành vi vi phạm sau đây:
a) Thuê, mượn linh kiện, phụ kiện của xe ô tô khi kiểm định;
b) Đưa xe cơ giới, xe máy chuyên dùng có giấy chứng nhận hoặc tem kiểm định an toàn kỹ thuật và bảo vệ môi trường (đối với loại xe có quy định phải kiểm định) nhưng đã hết hiệu lực (hạn sử dụng) dưới 01 tháng (kể cả rơ moóc và sơ mi rơ moóc) tham gia giao thông;
c) Giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại khoản 4 Điều 21 của Nghị định này hoặc trực tiếp điều khiển phương tiện thực hiện hành vi vi phạm quy định tại khoản 4 Điều 21 của Nghị định này;
d) Giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm d khoản 6 Điều 20; điểm b khoản 5 Điều 21 của Nghị định này hoặc trực tiếp điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm d khoản 6 Điều 20; điểm b khoản 5 Điều 21 của Nghị định này;
…

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K21/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K21/a

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
21. Ngoài việc bị áp dụng hình thức xử phạt, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
a) Thực hiện hành vi quy định tại điểm đ, điểm g, điểm m khoản 7; điểm đ, điểm e khoản 8; điểm b, điểm c, điểm d, điểm đ khoản 9; điểm a, điểm b, điểm đ khoản 11; điểm a khoản 12; điểm c khoản 13; điểm đ, điểm h khoản 14 Điều này trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện còn bị trừ điểm giấy phép lái xe 02 điểm;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D21/K4)
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K4

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
4. Phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng đối với người điều khiển xe thực hiện hành vi chở hàng vượt quá chiều cao xếp hàng cho phép đối với xe ô tô tải (kể cả rơ moóc và sơ mi rơ moóc).

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D20/K6/d)
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K6/d

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
6. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
d) Điều khiển xe ô tô kinh doanh vận tải, xe vận tải nội bộ quá thời gian quy định tại khoản 1 Điều 64 của Luật Trật tự, an toàn giao thông đường bộ; không thực hiện đúng quy định về thời gian nghỉ giữa hai lần lái xe liên tục của người lái xe;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D21/K5/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K5/b

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
5. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
b) Điều khiển xe ô tô kinh doanh vận tải, xe vận tải nội bộ quá thời gian quy định tại khoản 1 Điều 64 của Luật Trật tự, an toàn giao thông đường bộ; không thực hiện đúng quy định về thời gian nghỉ giữa hai lần lái xe liên tục của người lái xe;

[0] 4.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D32/K9)
[1] 6.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D32/K9)
[2] 8.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D32/K9)
[3] 12.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D32/K9)
[4] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D32/K21/a)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là chủ doanh nghiệp vận tải, một xe ô tô chở khách của công ty tôi đã có giấy kiểm định an toàn kỹ thuật hết hạn 20 ngày trước khi tham gia giao thông. Nếu bị phát hiện, mức phạt tiền và trừ điểm sẽ là bao nhiêu?
- Đáp: Nếu vi phạm, mức phạt tiền sẽ từ 8.000.000 đồng đến 12.000.000 đồng và trừ 02 điểm giấy phép lái xe.
- ⚠ chep_nguyen_van: “kiểm định an toàn kỹ thuật …”
- Ghi chú: đối tượng là xe ô tô chở khách

```json
{"qid": "tD-muc_phat-011", "question": "Tôi là chủ doanh nghiệp vận tải, một xe ô tô chở khách của công ty tôi đã có giấy kiểm định an toàn kỹ thuật hết hạn 20 ngày trước khi tham gia giao thông. Nếu bị phát hiện, mức phạt tiền và trừ điểm sẽ là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Nếu vi phạm, mức phạt tiền sẽ từ 8.000.000 đồng đến 12.000.000 đồng và trừ 02 điểm giấy phép lái xe.", "gold_units": ["ND168-2024/D32/K9"], "required_numbers": [{"value": 8000000, "unit": "vnd"}, {"value": 12000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-011:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là chủ doanh nghiệp vận tải, trong quá trình kiểm định, nhân viên của tôi đã thuê một bộ phận phụ kiện của xe ô tô để kiểm tra. Nếu bị xử phạt, mức phạt tiền và trừ điểm sẽ là bao nhiêu?
- Đáp: Nếu vi phạm, mức phạt tiền sẽ từ 8.000.000 đồng đến 12.000.000 đồng và trừ 02 điểm giấy phép lái xe.
- ⚠ chep_nguyen_van: “phụ kiện của xe ô tô …”
- Ghi chú: đối tượng là xe ô tô chở khách

```json
{"qid": "tD-muc_phat-011", "question": "Tôi là chủ doanh nghiệp vận tải, trong quá trình kiểm định, nhân viên của tôi đã thuê một bộ phận phụ kiện của xe ô tô để kiểm tra. Nếu bị xử phạt, mức phạt tiền và trừ điểm sẽ là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Nếu vi phạm, mức phạt tiền sẽ từ 8.000.000 đồng đến 12.000.000 đồng và trừ 02 điểm giấy phép lái xe.", "gold_units": ["ND168-2024/D32/K9"], "required_numbers": [{"value": 8000000, "unit": "vnd"}, {"value": 12000000, "unit": "vnd"}, {"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-011:2"}
```

### WD-muc_phat-012 · tier A · vai: phụ huynh có con dưới 18 tuổi · kiểu: ngan

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D8/K5, ND168-2024/D8/K5/a, ND168-2024/D8/K5/b, ND168-2024/D8/K5/c, ND168-2024/D8/K5/d, ND168-2024/D8/K5/đ, ND168-2024/D8/K5/e

Điều 8. Xử phạt người điều khiển xe máy chuyên dùng vi phạm quy tắc giao thông đường bộ
5. Phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
a) Lùi xe, quay đầu xe trong hầm đường bộ;
b) Không thực hiện biện pháp bảo đảm an toàn theo quy định khi phương tiện bị hư hỏng trên đoạn đường bộ giao nhau cùng mức với đường sắt;
c) Dừng xe, đỗ xe trong hầm đường bộ không đúng nơi quy định; không có báo hiệu bằng đèn khẩn cấp, không đặt biển cảnh báo “Chú ý xe đỗ” (hoặc đèn cảnh báo) về phía sau xe khoảng cách đảm bảo an toàn khi dừng xe, đỗ xe trong hầm đường bộ trong trường hợp gặp sự cố kỹ thuật hoặc bất khả kháng khác buộc phải dừng xe, đỗ xe;
d) Điều khiển xe có liên quan trực tiếp đến vụ tai nạn giao thông mà không dừng ngay phương tiện, không giữ nguyên hiện trường, không trợ giúp người bị nạn, trừ hành vi vi phạm quy định tại điểm c khoản 8 Điều này;
đ) Chuyển hướng không nhường quyền đi trước cho: người đi bộ, xe lăn của người khuyết tật qua đường tại nơi có vạch kẻ đường dành cho người đi bộ; xe thô sơ đang đi trên phần đường dành cho xe thô sơ;
e) Chuyển hướng không nhường đường cho: các xe đi ngược chiều; người đi bộ, xe thô sơ đang qua đường tại nơi không có vạch kẻ đường cho người đi bộ.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D8/K8/c)
Mã điều khoản dùng được cho gold_units: ND168-2024/D8/K8/c

Điều 8. Xử phạt người điều khiển xe máy chuyên dùng vi phạm quy tắc giao thông đường bộ
8. Phạt tiền từ 14.000.000 đồng đến 16.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
c) Gây tai nạn giao thông không dừng ngay phương tiện, không giữ nguyên hiện trường, không trợ giúp người bị nạn, không ở lại hiện trường hoặc không đến trình báo ngay với cơ quan công an, Ủy ban nhân dân nơi gần nhất;

[0] 2.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D8/K5)
[1] 3.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D8/K5)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Con tôi đang lái xe máy và dừng lại trong hầm đường bộ mà không bật đèn khẩn cấp hay đặt biển cảnh báo, tôi muốn biết mức phạt tiền mà anh ta phải chịu?
- Đáp: Nếu người điều khiển xe máy thực hiện hành vi này, mức phạt tiền sẽ từ 2.000.000 đồng đến 3.000.000 đồng. (Điều 8, Khoản 5, Nghị định 168/2024/NĐ-CP)
- Ghi chú: Giả định con tôi là người điều khiển xe máy, mức phạt không thay đổi vì tuổi dưới 18.

```json
{"qid": "tD-muc_phat-012", "question": "Con tôi đang lái xe máy và dừng lại trong hầm đường bộ mà không bật đèn khẩn cấp hay đặt biển cảnh báo, tôi muốn biết mức phạt tiền mà anh ta phải chịu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Nếu người điều khiển xe máy thực hiện hành vi này, mức phạt tiền sẽ từ 2.000.000 đồng đến 3.000.000 đồng. (Điều 8, Khoản 5, Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D8/K5"], "required_numbers": [{"value": 2000000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-012:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Con tôi lái xe máy lùi xe trong hầm đường bộ mà không có biện pháp bảo đảm an toàn, tôi muốn biết mức phạt tiền mà anh ta phải chịu?
- Đáp: Nếu người điều khiển xe máy thực hiện hành vi này, mức phạt tiền sẽ từ 2.000.000 đồng đến 3.000.000 đồng. (Điều 8, Khoản 5, Nghị định 168/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “biện pháp bảo đảm an toàn …”
- Ghi chú: Giả định con tôi là người điều khiển xe máy, mức phạt không thay đổi vì tuổi dưới 18.

```json
{"qid": "tD-muc_phat-012", "question": "Con tôi lái xe máy lùi xe trong hầm đường bộ mà không có biện pháp bảo đảm an toàn, tôi muốn biết mức phạt tiền mà anh ta phải chịu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Nếu người điều khiển xe máy thực hiện hành vi này, mức phạt tiền sẽ từ 2.000.000 đồng đến 3.000.000 đồng. (Điều 8, Khoản 5, Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D8/K5"], "required_numbers": [{"value": 2000000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-012:2"}
```

### WD-muc_phat-013 · tier A · vai: cán bộ phường · kiểu: tinh_huong_ban_than

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K2

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
2. Phạt tiền từ 400.000 đồng đến 600.000 đồng trên mỗi người vượt quá quy định được phép chở của phương tiện nhưng tổng mức phạt tiền tối đa không vượt quá 75.000.000 đồng đối với người điều khiển xe ô tô chở hành khách, ô tô chở người (trừ xe buýt) thực hiện hành vi vi phạm chở quá số người quy định được phép chở của phương tiện, trừ các hành vi vi phạm quy định tại khoản 4 Điều này.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D20/K10/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K10/b

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
10. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
b) Thực hiện hành vi quy định tại khoản 2, khoản 4 (trường hợp vượt trên 50% đến 100% số người quy định được phép chở của phương tiện) Điều này bị trừ điểm giấy phép lái xe 04 điểm;

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D20/K10/d)
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K10/d

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
10. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
d) Thực hiện hành vi quy định tại khoản 2, khoản 4 (trường hợp vượt trên 100% số người quy định được phép chở của phương tiện) Điều này bị trừ điểm giấy phép lái xe 10 điểm.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D20/K4)
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K4

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
4. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng trên mỗi người vượt quá quy định được phép chở của phương tiện nhưng tổng mức phạt tiền tối đa không vượt quá 75.000.000 đồng đối với người điều khiển xe ô tô chở hành khách (kinh doanh vận tải hành khách theo tuyến cố định, hợp đồng) chạy tuyến có cự ly lớn hơn 300 km thực hiện hành vi vi phạm chở quá số người quy định được phép chở của phương tiện.

[0] 400.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D20/K2)
[1] 600.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D20/K2)
[2] 04 điểm (số điểm bị trừ, nêu tại ND168-2024/D20/K10/b)
[3] 10 điểm (số điểm bị trừ, nêu tại ND168-2024/D20/K10/d)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là cán bộ phường, hôm nay thấy một xe buýt chở 12 hành khách trong khi chỉ được phép chở 10. Mức phạt tiền và điểm trừ mà người điều khiển xe phải chịu là bao nhiêu?
- Đáp: Người điều khiển xe buýt sẽ bị phạt tiền từ 400.000 đồng đến 600.000 đồng và bị trừ 04 điểm giấy phép lái xe. (Điều 20 Khoản 2 và Khoản 10 b Nghị định 168/2024/NĐ-CP)
- Ghi chú: Giả định xe buýt có công suất 10 hành khách

```json
{"qid": "tD-muc_phat-013", "question": "Tôi là cán bộ phường, hôm nay thấy một xe buýt chở 12 hành khách trong khi chỉ được phép chở 10. Mức phạt tiền và điểm trừ mà người điều khiển xe phải chịu là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Người điều khiển xe buýt sẽ bị phạt tiền từ 400.000 đồng đến 600.000 đồng và bị trừ 04 điểm giấy phép lái xe. (Điều 20 Khoản 2 và Khoản 10 b Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D20/K2", "ND168-2024/D20/K10/b"], "required_numbers": [{"value": 400000, "unit": "vnd"}, {"value": 600000, "unit": "vnd"}, {"value": 4, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-013:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là cán bộ phường, hôm nay thấy một xe buýt chở 15 hành khách trong khi chỉ được phép chở 10. Mức phạt tiền và điểm trừ mà người điều khiển xe phải chịu là bao nhiêu?
- Đáp: Người điều khiển xe buýt sẽ bị phạt tiền từ 400.000 đồng đến 600.000 đồng và bị trừ 10 điểm giấy phép lái xe. (Điều 20 Khoản 2 và Khoản 10 d Nghị định 168/2024/NĐ-CP)
- Ghi chú: Giả định xe buýt có công suất 10 hành khách

```json
{"qid": "tD-muc_phat-013", "question": "Tôi là cán bộ phường, hôm nay thấy một xe buýt chở 15 hành khách trong khi chỉ được phép chở 10. Mức phạt tiền và điểm trừ mà người điều khiển xe phải chịu là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Người điều khiển xe buýt sẽ bị phạt tiền từ 400.000 đồng đến 600.000 đồng và bị trừ 10 điểm giấy phép lái xe. (Điều 20 Khoản 2 và Khoản 10 d Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D20/K2", "ND168-2024/D20/K10/d"], "required_numbers": [{"value": 400000, "unit": "vnd"}, {"value": 600000, "unit": "vnd"}, {"value": 10, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-013:2"}
```

### WD-muc_phat-014 · tier A · vai: sinh viên đi xe máy · kiểu: tinh_huong_ban_than

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D15/K1

Điều 15. Xử phạt người điều khiển xe thô sơ vi phạm quy định về điều kiện của phương tiện khi tham gia giao thông
1. Phạt tiền từ 100.000 đồng đến 200.000 đồng đối với hành vi điều khiển xe không có bộ phận phát âm thanh cảnh báo (còi, chuông); không có đèn chiếu sáng hoặc tấm phản quang phía trước; không có đèn tín hiệu hoặc tấm phản quang phía sau xe (đối với loại xe quy định phải có bộ phận này).

[0] 100.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D15/K1)
[1] 200.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D15/K1)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi đang lái xe máy không có còi, đèn pha hay đèn hậu, có bị phạt tiền không?
- Đáp: Bạn sẽ bị phạt tiền từ 100.000 đồng đến 200.000 đồng. (Điều 15 Nghị định 168/2024/NĐ-CP)
- Ghi chú: Xe máy là xe gắn máy

```json
{"qid": "tD-muc_phat-014", "question": "Tôi đang lái xe máy không có còi, đèn pha hay đèn hậu, có bị phạt tiền không?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Bạn sẽ bị phạt tiền từ 100.000 đồng đến 200.000 đồng. (Điều 15 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D15/K1"], "required_numbers": [{"value": 100000, "unit": "vnd"}, {"value": 200000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-014:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi đi xe máy vào ban đêm mà không bật đèn pha, có bị phạt không?
- Đáp: Bạn sẽ bị phạt tiền từ 100.000 đồng đến 200.000 đồng. (Điều 15 Nghị định 168/2024/NĐ-CP)
- Ghi chú: Xe máy là xe gắn máy

```json
{"qid": "tD-muc_phat-014", "question": "Tôi đi xe máy vào ban đêm mà không bật đèn pha, có bị phạt không?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Bạn sẽ bị phạt tiền từ 100.000 đồng đến 200.000 đồng. (Điều 15 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D15/K1"], "required_numbers": [{"value": 100000, "unit": "vnd"}, {"value": 200000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-014:2"}
```

### WD-muc_phat-015 · tier A · vai: người mới học lái ô tô · kiểu: tinh_huong_nguoi_khac

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D33/K3

Điều 33. Xử phạt hành khách đi xe vi phạm quy định về trật tự, an toàn giao thông
3. Phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng đối với hành vi đe dọa, xâm phạm sức khỏe của người khác đi trên xe, lái xe, nhân viên phục vụ trên xe.

[0] 2.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D33/K3)
[1] 3.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D33/K3)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Anh tôi lái xe đưa khách, trong lúc di chuyển anh ta đã đe dọa một hành khách, anh ta muốn biết mức phạt tiền mà anh ta phải chịu?
- Đáp: Nếu vi phạm hành vi đe dọa, người vi phạm phải chịu phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng. (Điều 33, Khoản 3 Nghị định 168/2024/NĐ-CP)

```json
{"qid": "tD-muc_phat-015", "question": "Anh tôi lái xe đưa khách, trong lúc di chuyển anh ta đã đe dọa một hành khách, anh ta muốn biết mức phạt tiền mà anh ta phải chịu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Nếu vi phạm hành vi đe dọa, người vi phạm phải chịu phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng. (Điều 33, Khoản 3 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D33/K3"], "required_numbers": [{"value": 2000000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-015:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Công ty tôi có một xe buýt chở nhân viên, trong một chuyến đi, một nhân viên lái xe đã đe dọa một hành khách, tôi muốn biết mức phạt tiền mà anh ta phải chịu?
- Đáp: Nếu vi phạm hành vi đe dọa, người vi phạm phải chịu phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng. (Điều 33, Khoản 3 Nghị định 168/2024/NĐ-CP)

```json
{"qid": "tD-muc_phat-015", "question": "Công ty tôi có một xe buýt chở nhân viên, trong một chuyến đi, một nhân viên lái xe đã đe dọa một hành khách, tôi muốn biết mức phạt tiền mà anh ta phải chịu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Nếu vi phạm hành vi đe dọa, người vi phạm phải chịu phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng. (Điều 33, Khoản 3 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D33/K3"], "required_numbers": [{"value": 2000000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-015:2"}
```

### WD-muc_phat-016 · tier A · vai: phụ huynh có con dưới 18 tuổi · kiểu: tinh_huong_nguoi_khac

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D26/K10, ND168-2024/D26/K10/a, ND168-2024/D26/K10/b

Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
10. Phạt tiền từ 40.000.000 đồng đến 60.000.000 đồng đối với đơn vị sản xuất, lắp ráp, nhập khẩu thiết bị ghi nhận hình ảnh người lái xe lắp trên xe ô tô, đơn vị cung cấp dịch vụ liên quan đến giám sát hành trình, ghi nhận hình ảnh người lái xe thực hiện một trong các hành vi vi phạm sau đây:
a) Làm sai lệch thông tin, dữ liệu của thiết bị giám sát hành trình của xe ô tô;
b) Làm sai lệch thông tin, dữ liệu của thiết bị ghi nhận hình ảnh người lái xe lắp trên xe ô tô.

[0] 40.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D26/K10)
[1] 60.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D26/K10)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Anh tôi là một công ty lắp ráp xe ô tô, và chúng tôi đã ghi hình sai lệch dữ liệu của thiết bị giám sát hành trình. Mức phạt tiền mà công ty phải chịu là bao nhiêu?
- Đáp: Công ty sẽ bị phạt tiền từ 40.000.000 đồng đến 60.000.000 đồng.
- ⚠ chep_nguyen_van: “của thiết bị giám sát hành …”

```json
{"qid": "tD-muc_phat-016", "question": "Anh tôi là một công ty lắp ráp xe ô tô, và chúng tôi đã ghi hình sai lệch dữ liệu của thiết bị giám sát hành trình. Mức phạt tiền mà công ty phải chịu là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Công ty sẽ bị phạt tiền từ 40.000.000 đồng đến 60.000.000 đồng.", "gold_units": ["ND168-2024/D26/K10"], "required_numbers": [{"value": 40000000, "unit": "vnd"}, {"value": 60000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-016:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Con tôi đang lái xe ô tô, và công ty ghi hình người lái đã làm sai lệch dữ liệu của thiết bị ghi nhận hình ảnh. Mức phạt tiền mà công ty phải chịu là bao nhiêu?
- Đáp: Công ty sẽ bị phạt tiền từ 40.000.000 đồng đến 60.000.000 đồng.
- ⚠ chep_nguyen_van: “của thiết bị ghi nhận hình …”

```json
{"qid": "tD-muc_phat-016", "question": "Con tôi đang lái xe ô tô, và công ty ghi hình người lái đã làm sai lệch dữ liệu của thiết bị ghi nhận hình ảnh. Mức phạt tiền mà công ty phải chịu là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Công ty sẽ bị phạt tiền từ 40.000.000 đồng đến 60.000.000 đồng.", "gold_units": ["ND168-2024/D26/K10"], "required_numbers": [{"value": 40000000, "unit": "vnd"}, {"value": 60000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-016:2"}
```

### WD-muc_phat-017 · tier A · vai: tài xế công nghệ · kiểu: neu_van_ban

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2026-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D27/K1, ND168-2024/D27/K1/a, ND168-2024/D27/K1/b, ND168-2024/D27/K1/c

Điều 27. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô kinh doanh vận tải chở trẻ em mầm non, học sinh, xe ô tô kinh doanh vận tải kết hợp với hoạt động đưa đón trẻ em mầm non, học sinh
1. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với người điều khiển xe ô tô kinh doanh vận tải chở trẻ em mầm non, học sinh, xe ô tô kinh doanh vận tải kết hợp với hoạt động đưa đón trẻ em mầm non, học sinh thực hiện một trong các hành vi vi phạm sau đây:
a) Không hướng dẫn trẻ em mầm non, học sinh ngồi đúng vị trí quy định trong xe;
b) Điều khiển xe ô tô kinh doanh vận tải chở trẻ em mầm non, học sinh tiểu học, xe ô tô kinh doanh vận tải kết hợp với hoạt động đưa đón trẻ em mầm non, học sinh tiểu học không có dây đai an toàn phù hợp với lứa tuổi hoặc không có ghế ngồi phù hợp với lứa tuổi theo quy định;
c) Điều khiển xe không lắp thiết bị ghi nhận hình ảnh người lái xe hoặc có lắp thiết bị ghi nhận hình ảnh người lái xe nhưng không có tác dụng trong quá trình xe tham gia giao thông theo quy định hoặc làm sai lệch dữ liệu của thiết bị ghi nhận hình ảnh người lái xe lắp trên xe ô tô.

[0] 1.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D27/K1)
[1] 2.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D27/K1)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là tài xế xe ô tô kinh doanh vận tải chở trẻ em mầm non, hôm nay tôi không lắp dây an toàn cho các bé. Theo Nghị định 168/2024/NĐ-CP, mức phạt tiền sẽ là bao nhiêu?
- Đáp: Bạn sẽ bị phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng.
- ⚠ chep_nguyen_van: “doanh vận tải chở trẻ em …”
- Ghi chú: Không đề cập đến tên điều khoản trong câu hỏi

```json
{"qid": "tD-muc_phat-017", "question": "Tôi là tài xế xe ô tô kinh doanh vận tải chở trẻ em mầm non, hôm nay tôi không lắp dây an toàn cho các bé. Theo Nghị định 168/2024/NĐ-CP, mức phạt tiền sẽ là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Bạn sẽ bị phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng.", "gold_units": ["ND168-2024/D27/K1"], "required_numbers": [{"value": 1000000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-017:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi lái xe ô tô kinh doanh vận tải chở học sinh, nhưng quên hướng dẫn các em ngồi đúng chỗ. Theo Nghị định 168/2024/NĐ-CP, tôi sẽ bị phạt tiền bao nhiêu?
- Đáp: Bạn sẽ bị phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng.
- ⚠ chep_nguyen_van: “tô kinh doanh vận tải chở …”
- Ghi chú: Không đề cập đến tên điều khoản trong câu hỏi

```json
{"qid": "tD-muc_phat-017", "question": "Tôi lái xe ô tô kinh doanh vận tải chở học sinh, nhưng quên hướng dẫn các em ngồi đúng chỗ. Theo Nghị định 168/2024/NĐ-CP, tôi sẽ bị phạt tiền bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Bạn sẽ bị phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng.", "gold_units": ["ND168-2024/D27/K1"], "required_numbers": [{"value": 1000000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-017:2"}
```

### WD-muc_phat-018 · tier A · vai: chủ doanh nghiệp vận tải · kiểu: neu_van_ban

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D9/K1, ND168-2024/D9/K1/a, ND168-2024/D9/K1/b, ND168-2024/D9/K1/c, ND168-2024/D9/K1/d, ND168-2024/D9/K1/đ, ND168-2024/D9/K1/e, ND168-2024/D9/K1/g, ND168-2024/D9/K1/h, ND168-2024/D9/K1/i, ND168-2024/D9/K1/k, ND168-2024/D9/K1/l, ND168-2024/D9/K1/m, ND168-2024/D9/K1/n, ND168-2024/D9/K1/o, ND168-2024/D9/K1/p

Điều 9. Xử phạt người điều khiển xe đạp, xe đạp máy, người điều khiển xe thô sơ khác vi phạm quy tắc giao thông đường bộ
1. Phạt tiền từ 100.000 đồng đến 200.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
a) Không đi bên phải theo chiều đi của mình, đi không đúng phần đường quy định;
b) Dừng xe đột ngột; chuyển hướng không báo hiệu trước;
c) Không chấp hành hiệu lệnh hoặc chỉ dẫn của biển báo hiệu, vạch kẻ đường, trừ các hành vi vi phạm quy định tại điểm đ khoản 2, điểm c khoản 3 Điều này;
d) Vượt bên phải trong các trường hợp không được phép;
đ) Dừng xe, đỗ xe trên phần đường xe chạy ở đoạn đường ngoài đô thị nơi có lề đường;
e) Chạy trong hầm đường bộ không bật đèn hoặc không có vật phát sáng báo hiệu; dừng xe, đỗ xe trong hầm đường bộ không đúng nơi quy định; quay đầu xe trong hầm đường bộ;
g) Điều khiển xe đạp, xe đạp máy đi dàn hàng ngang từ 03 xe trở lên, xe thô sơ khác đi dàn hàng ngang từ 02 xe trở lên;
h) Người điều khiển xe đạp, xe đạp máy sử dụng ô (dù), dùng tay cầm và sử dụng điện thoại hoặc các thiết bị điện tử khác; chở người ngồi trên xe đạp, xe đạp máy sử dụng ô (dù);
i) Điều khiển xe thô sơ trong thời gian từ 18 giờ ngày hôm trước đến 06 giờ ngày hôm sau không sử dụng đèn hoặc không có báo hiệu ở phía trước và phía sau xe;
k) Để xe ở lòng đường, vỉa hè trái phép; đỗ xe ở lòng đường gây cản trở giao thông, đỗ xe trên cầu gây cản trở giao thông;
…

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D9/K2/đ)
Mã điều khoản dùng được cho gold_units: ND168-2024/D9/K2/đ

Điều 9. Xử phạt người điều khiển xe đạp, xe đạp máy, người điều khiển xe thô sơ khác vi phạm quy tắc giao thông đường bộ
2. Phạt tiền từ 150.000 đồng đến 250.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
đ) Không chấp hành hiệu lệnh của đèn tín hiệu giao thông.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D9/K3/c)
Mã điều khoản dùng được cho gold_units: ND168-2024/D9/K3/c

Điều 9. Xử phạt người điều khiển xe đạp, xe đạp máy, người điều khiển xe thô sơ khác vi phạm quy tắc giao thông đường bộ
3. Phạt tiền từ 300.000 đồng đến 400.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
c) Đi vào khu vực cấm, đường có biển báo hiệu nội dung cấm đi vào đối với loại phương tiện đang điều khiển; đi ngược chiều đường của đường một chiều, đường có biển “Cấm đi ngược chiều";

[0] 100.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D9/K1)
[1] 200.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D9/K1)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Theo Nghị định 168/2024/NĐ-CP, nếu một lái xe của công ty tôi không đi bên phải theo chiều đi của mình, mức phạt tiền là bao nhiêu?
- Đáp: Mức phạt tiền là từ 100.000 đồng đến 200.000 đồng.
- ⚠ chep_nguyen_van: “bên phải theo chiều đi của …”

```json
{"qid": "tD-muc_phat-018", "question": "Theo Nghị định 168/2024/NĐ-CP, nếu một lái xe của công ty tôi không đi bên phải theo chiều đi của mình, mức phạt tiền là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Mức phạt tiền là từ 100.000 đồng đến 200.000 đồng.", "gold_units": ["ND168-2024/D9/K1"], "required_numbers": [{"value": 100000, "unit": "vnd"}, {"value": 200000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-018:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Theo Nghị định 168/2024/NĐ-CP, nếu một lái xe của công ty tôi dừng xe trên lề đường ngoài đô thị, mức phạt tiền là bao nhiêu?
- Đáp: Mức phạt tiền là từ 100.000 đồng đến 200.000 đồng.

```json
{"qid": "tD-muc_phat-018", "question": "Theo Nghị định 168/2024/NĐ-CP, nếu một lái xe của công ty tôi dừng xe trên lề đường ngoài đô thị, mức phạt tiền là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Mức phạt tiền là từ 100.000 đồng đến 200.000 đồng.", "gold_units": ["ND168-2024/D9/K1"], "required_numbers": [{"value": 100000, "unit": "vnd"}, {"value": 200000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-018:2"}
```

### WD-muc_phat-019 · tier A · vai: sinh viên đi xe máy · kiểu: neu_van_ban

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K4

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
4. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng trên mỗi người vượt quá quy định được phép chở của phương tiện nhưng tổng mức phạt tiền tối đa không vượt quá 75.000.000 đồng đối với người điều khiển xe ô tô chở hành khách (kinh doanh vận tải hành khách theo tuyến cố định, hợp đồng) chạy tuyến có cự ly lớn hơn 300 km thực hiện hành vi vi phạm chở quá số người quy định được phép chở của phương tiện.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D20/K10/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K10/b

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
10. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
b) Thực hiện hành vi quy định tại khoản 2, khoản 4 (trường hợp vượt trên 50% đến 100% số người quy định được phép chở của phương tiện) Điều này bị trừ điểm giấy phép lái xe 04 điểm;

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D20/K10/d)
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K10/d

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
10. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
d) Thực hiện hành vi quy định tại khoản 2, khoản 4 (trường hợp vượt trên 100% số người quy định được phép chở của phương tiện) Điều này bị trừ điểm giấy phép lái xe 10 điểm.

[0] 1.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D20/K4)
[1] 2.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D20/K4)
[2] 04 điểm (số điểm bị trừ, nêu tại ND168-2024/D20/K10/b)
[3] 10 điểm (số điểm bị trừ, nêu tại ND168-2024/D20/K10/d)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Theo Nghị định 168/2024/NĐ-CP, nếu một xe ô tô chở hành khách vượt quá số người quy định được phép chở, mức phạt tiền mà người điều khiển phải chịu là bao nhiêu?
- Đáp: Mức phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng trên mỗi người vượt quá quy định được phép chở, với tổng mức phạt tối đa không vượt quá 75.000.000 đồng đối với người điều khiển xe ô tô chở hành khách kinh doanh vận tải hành khách theo tuyến cố định, hợp đồng chạy tuyến có cự ly lớn hơn 300 km.
- ⚠ chep_nguyen_van: “người quy định được phép chở …”

```json
{"qid": "tD-muc_phat-019", "question": "Theo Nghị định 168/2024/NĐ-CP, nếu một xe ô tô chở hành khách vượt quá số người quy định được phép chở, mức phạt tiền mà người điều khiển phải chịu là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Mức phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng trên mỗi người vượt quá quy định được phép chở, với tổng mức phạt tối đa không vượt quá 75.000.000 đồng đối với người điều khiển xe ô tô chở hành khách kinh doanh vận tải hành khách theo tuyến cố định, hợp đồng chạy tuyến có cự ly lớn hơn 300 km.", "gold_units": ["ND168-2024/D20/K4"], "required_numbers": [{"value": 1000000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-019:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Nếu một xe ô tô chở hành khách chạy trên tuyến có cự ly lớn hơn 300 km và chở quá số người quy định, mức phạt tiền mà người điều khiển phải chịu theo Nghị định 168/2024/NĐ-CP là bao nhiêu?
- Đáp: Mức phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng trên mỗi người vượt quá quy định được phép chở, với tổng mức phạt tối đa không vượt quá 75.000.000 đồng đối với người điều khiển xe ô tô chở hành khách kinh doanh vận tải hành khách theo tuyến cố định, hợp đồng chạy tuyến có cự ly lớn hơn 300 km.
- ⚠ chep_nguyen_van: “chở quá số người quy định …”

```json
{"qid": "tD-muc_phat-019", "question": "Nếu một xe ô tô chở hành khách chạy trên tuyến có cự ly lớn hơn 300 km và chở quá số người quy định, mức phạt tiền mà người điều khiển phải chịu theo Nghị định 168/2024/NĐ-CP là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Mức phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng trên mỗi người vượt quá quy định được phép chở, với tổng mức phạt tối đa không vượt quá 75.000.000 đồng đối với người điều khiển xe ô tô chở hành khách kinh doanh vận tải hành khách theo tuyến cố định, hợp đồng chạy tuyến có cự ly lớn hơn 300 km.", "gold_units": ["ND168-2024/D20/K4"], "required_numbers": [{"value": 1000000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-019:2"}
```

### WD-muc_phat-020 · tier A · vai: phụ huynh có con dưới 18 tuổi · kiểu: tinh_huong_nguoi_khac

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D34/K1

Điều 34. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển quá khổ giới hạn, xe quá tải trọng, xe bánh xích lưu hành đường bộ (kể cả xe ô tô chở hành khách)
1. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với hành vi không thực hiện đúng quy định trong giấy phép lưu hành, trừ các hành vi vi phạm quy định tại điểm a, điểm b khoản 3; điểm b, điểm c khoản 4 Điều này.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D34/K7/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D34/K7/a

Điều 34. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển quá khổ giới hạn, xe quá tải trọng, xe bánh xích lưu hành đường bộ (kể cả xe ô tô chở hành khách)
7. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
a) Thực hiện hành vi quy định tại khoản 1, khoản 3, điểm a khoản 4 Điều này còn bị trừ điểm giấy phép lái xe 02 điểm;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D34/K3/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D34/K3/a

Điều 34. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển quá khổ giới hạn, xe quá tải trọng, xe bánh xích lưu hành đường bộ (kể cả xe ô tô chở hành khách)
3. Phạt tiền từ 8.000.000 đồng đến 10.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
a) Chở hàng vượt khổ giới hạn của xe hoặc của đường bộ ghi trong giấy phép lưu hành;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D34/K3/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D34/K3/b

Điều 34. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển quá khổ giới hạn, xe quá tải trọng, xe bánh xích lưu hành đường bộ (kể cả xe ô tô chở hành khách)
3. Phạt tiền từ 8.000.000 đồng đến 10.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
b) Điều khiển xe bánh xích tham gia giao thông không có giấy phép lưu hành hoặc có giấy phép lưu hành nhưng không còn giá trị sử dụng theo quy định hoặc lưu thông trực tiếp trên đường mà không thực hiện biện pháp bảo vệ đường theo quy định;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D34/K4/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D34/K4/b

Điều 34. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển quá khổ giới hạn, xe quá tải trọng, xe bánh xích lưu hành đường bộ (kể cả xe ô tô chở hành khách)
4. Phạt tiền từ 13.000.000 đồng đến 15.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
b) Điều khiển xe có giấy phép lưu hành còn giá trị sử dụng nhưng tổng trọng lượng (khối lượng toàn bộ) của xe hoặc tải trọng trục xe (bao gồm cả hàng hóa xếp trên xe nếu có) vượt quá quy định trong giấy phép lưu hành;

[0] 3.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D34/K1)
[1] 5.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D34/K1)
[2] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D34/K7/a)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Anh tôi thấy xe buýt của công ty bên cạnh đang chở hàng vượt giới hạn, anh có thể cho biết mức phạt tiền mà người điều khiển phải chịu không?
- Đáp: Người điều khiển sẽ bị phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng. (Điều 34 Khoản 1 Nghị định 168/2024/NĐ-CP)
- Ghi chú: Không đề cập đến điểm, khoản hay số điểm trừ.

```json
{"qid": "tD-muc_phat-020", "question": "Anh tôi thấy xe buýt của công ty bên cạnh đang chở hàng vượt giới hạn, anh có thể cho biết mức phạt tiền mà người điều khiển phải chịu không?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Người điều khiển sẽ bị phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng. (Điều 34 Khoản 1 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D34/K1"], "required_numbers": [{"value": 3000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-020:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Con tôi nghe rằng một chiếc xe tải đã vượt quá trọng lượng quy định khi chở hàng, anh có thể cho biết mức phạt tiền mà người lái xe phải chịu được không?
- Đáp: Người lái xe sẽ bị phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng. (Điều 34 Khoản 1 Nghị định 168/2024/NĐ-CP)
- Ghi chú: Không đề cập đến điểm, khoản hay số điểm trừ.

```json
{"qid": "tD-muc_phat-020", "question": "Con tôi nghe rằng một chiếc xe tải đã vượt quá trọng lượng quy định khi chở hàng, anh có thể cho biết mức phạt tiền mà người lái xe phải chịu được không?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Người lái xe sẽ bị phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng. (Điều 34 Khoản 1 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D34/K1"], "required_numbers": [{"value": 3000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-020:2"}
```

### WD-muc_phat-021 · tier A · vai: chủ doanh nghiệp vận tải · kiểu: ngan

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D6/K10, ND168-2024/D6/K10/a, ND168-2024/D6/K10/b

Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
10. Phạt tiền từ 20.000.000 đồng đến 22.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
a) Điều khiển xe không quan sát, giảm tốc độ hoặc dừng lại để bảo đảm an toàn theo quy định mà gây tai nạn giao thông; điều khiển xe chạy quá tốc độ quy định gây tai nạn giao thông; dừng xe, đỗ xe, quay đầu xe, lùi xe, tránh xe, vượt xe, chuyển hướng, chuyển làn đường không đúng quy định gây tai nạn giao thông; không đi đúng phần đường, làn đường, không giữ khoảng cách an toàn giữa hai xe theo quy định gây tai nạn giao thông hoặc đi vào đường có biển báo hiệu có nội dung cấm đi vào đối với loại phương tiện đang điều khiển gây tai nạn giao thông, trừ các hành vi vi phạm quy định tại điểm đ khoản 11 Điều này;
b) Vi phạm quy định tại một trong các điểm, khoản sau của Điều này mà gây tai nạn giao thông: điểm a, điểm b, điểm c, điểm d, điểm đ khoản 1; điểm c khoản 2; điểm b, điểm g, điểm h, điểm n, điểm o, điểm p, khoản 3; điểm a, điểm c, điểm d khoản 4; điểm c, điểm d, điểm e, điểm h, điểm n, điểm o, điểm q khoản 5; điểm b khoản 7; điểm b, điểm c, điểm d khoản 9 Điều này.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D6/K16/d)
Mã điều khoản dùng được cho gold_units: ND168-2024/D6/K16/d

Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
16. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển xe thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
d) Thực hiện hành vi quy định tại điểm a khoản 9, khoản 10, điểm đ khoản 11 Điều này bị trừ điểm giấy phép lái xe 10 điểm.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D6/K11/đ)
Mã điều khoản dùng được cho gold_units: ND168-2024/D6/K11/đ

Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
11. Phạt tiền từ 30.000.000 đồng đến 40.000.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
đ) Điều khiển xe đi ngược chiều trên đường cao tốc, lùi xe trên đường cao tốc, quay đầu xe trên đường cao tốc, trừ các xe ưu tiên đang đi làm nhiệm vụ khẩn cấp theo quy định.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D6/K1/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D6/K1/a

Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
1. Phạt tiền từ 400.000 đồng đến 600.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
a) Không chấp hành hiệu lệnh, chỉ dẫn của biển báo hiệu, vạch kẻ đường, trừ các hành vi vi phạm quy định tại điểm a, điểm c, điểm d, điểm đ khoản 2; điểm a, điểm d, điểm đ, điểm e, điểm n, điểm o khoản 3; điểm a, điểm b, điểm đ, điểm e, điểm i, điểm k, điểm l khoản 4; điểm a, điểm b, điểm c, điểm d, điểm đ, điểm i, điểm k khoản 5; điểm a khoản 6; khoản 7; điểm b, điểm d khoản 9; điểm a khoản 10; điểm đ khoản 11 Điều này;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D6/K1/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D6/K1/b

Điều 6. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tự xe ô tô vi phạm quy tắc giao thông đường bộ
1. Phạt tiền từ 400.000 đồng đến 600.000 đồng đối với người điều khiển xe thực hiện một trong các hành vi vi phạm sau đây:
b) Khi ra, vào vị trí dừng xe, đỗ xe không có tín hiệu báo cho người điều khiển phương tiện khác biết;

[0] 20.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D6/K10)
[1] 22.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D6/K10)
[2] 10 điểm (số điểm bị trừ, nêu tại ND168-2024/D6/K16/d)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Công ty tôi thuê một xe ô tô chở khách, và trong một chuyến đi, tài xế đã vượt tốc độ quy định trên đường cao tốc, gây ra tai nạn giao thông. Tôi muốn biết mức phạt tiền và điểm trừ mà tài xế sẽ phải chịu?
- Đáp: Tài xế sẽ bị phạt tiền từ 20.000.000 đồng đến 22.000.000 đồng và bị trừ 10 điểm giấy phép lái xe. (Điều 6, Khoản 10 và Khoản 16 d của Nghị định 168/2024/NĐ-CP)
- Ghi chú: Giả định tài xế là người điều khiển xe ô tô chở khách, vi phạm tốc độ quy định gây tai nạn giao thông.

```json
{"qid": "tD-muc_phat-021", "question": "Công ty tôi thuê một xe ô tô chở khách, và trong một chuyến đi, tài xế đã vượt tốc độ quy định trên đường cao tốc, gây ra tai nạn giao thông. Tôi muốn biết mức phạt tiền và điểm trừ mà tài xế sẽ phải chịu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Tài xế sẽ bị phạt tiền từ 20.000.000 đồng đến 22.000.000 đồng và bị trừ 10 điểm giấy phép lái xe. (Điều 6, Khoản 10 và Khoản 16 d của Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D6/K10", "ND168-2024/D6/K16/d"], "required_numbers": [{"value": 20000000, "unit": "vnd"}, {"value": 22000000, "unit": "vnd"}, {"value": 10, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-021:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Công ty tôi thuê một xe ô tô chở hàng, và trong một chuyến giao hàng, tài xế đã không giữ khoảng cách an toàn với xe phía trước, dẫn đến va chạm và gây tai nạn. Tôi muốn biết mức phạt tiền và điểm trừ mà tài xế sẽ phải chịu?
- Đáp: Tài xế sẽ bị phạt tiền từ 20.000.000 đồng đến 22.000.000 đồng và bị trừ 10 điểm giấy phép lái xe. (Điều 6, Khoản 10 và Khoản 16 d của Nghị định 168/2024/NĐ-CP)
- ⚠ qua_dai (52 từ); chep_nguyen_van: “không giữ khoảng cách an toàn …”
- Ghi chú: Giả định tài xế là người điều khiển xe ô tô chở hàng, vi phạm giữ khoảng cách an toàn gây tai nạn giao thông.

```json
{"qid": "tD-muc_phat-021", "question": "Công ty tôi thuê một xe ô tô chở hàng, và trong một chuyến giao hàng, tài xế đã không giữ khoảng cách an toàn với xe phía trước, dẫn đến va chạm và gây tai nạn. Tôi muốn biết mức phạt tiền và điểm trừ mà tài xế sẽ phải chịu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Tài xế sẽ bị phạt tiền từ 20.000.000 đồng đến 22.000.000 đồng và bị trừ 10 điểm giấy phép lái xe. (Điều 6, Khoản 10 và Khoản 16 d của Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D6/K10", "ND168-2024/D6/K16/d"], "required_numbers": [{"value": 20000000, "unit": "vnd"}, {"value": 22000000, "unit": "vnd"}, {"value": 10, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-021:2"}
```

### WD-muc_phat-022 · tier A · vai: cán bộ phường · kiểu: neu_van_ban

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D14/K2, ND168-2024/D14/K2/a, ND168-2024/D14/K2/b, ND168-2024/D14/K2/c, ND168-2024/D14/K2/d, ND168-2024/D14/K2/đ

Điều 14. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy vi phạm quy định về điều kiện của phương tiện khi tham gia giao thông
2. Phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
a) Điều khiển xe không có chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe) hoặc sử dụng chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe) đã hết hạn sử dụng, hết hiệu lực;
…

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D14/K8/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D14/K8/a

Điều 14. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy vi phạm quy định về điều kiện của phương tiện khi tham gia giao thông
8. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển xe thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
a) Thực hiện hành vi quy định tại điểm a, điểm b, điểm c khoản 2 Điều này bị trừ điểm giấy phép lái xe 02 điểm;

[0] 2.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D14/K2)
[1] 3.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D14/K2)
[2] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D14/K8/a)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Theo Nghị định 168/2024/NĐ-CP, nếu tôi điều khiển xe máy mà không có chứng nhận đăng ký xe, mức phạt tiền là bao nhiêu?
- Đáp: Mức phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng.
- ⚠ chep_nguyen_van: “có chứng nhận đăng ký xe …”

```json
{"qid": "tD-muc_phat-022", "question": "Theo Nghị định 168/2024/NĐ-CP, nếu tôi điều khiển xe máy mà không có chứng nhận đăng ký xe, mức phạt tiền là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Mức phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng.", "gold_units": ["ND168-2024/D14/K2"], "required_numbers": [{"value": 2000000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-022:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Theo Nghị định 168/2024/NĐ-CP, khi điều khiển xe máy có chứng nhận đăng ký hết hạn, tôi sẽ bị trừ bao nhiêu điểm?
- Đáp: Trừ 02 điểm.

```json
{"qid": "tD-muc_phat-022", "question": "Theo Nghị định 168/2024/NĐ-CP, khi điều khiển xe máy có chứng nhận đăng ký hết hạn, tôi sẽ bị trừ bao nhiêu điểm?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Trừ 02 điểm.", "gold_units": ["ND168-2024/D14/K8/a"], "required_numbers": [{"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-022:2"}
```

### WD-muc_phat-023 · tier A · vai: cán bộ phường · kiểu: ngan

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2026-08-15 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D26/K1, ND168-2024/D26/K1/a, ND168-2024/D26/K1/b

Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
1. Phạt tiền từ 500.000 đồng đến 1.000.000 đồng đối với cá nhân, từ 1.000.000 đồng đến 2.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
a) Xếp hàng hóa lên mỗi xe ô tô (kể cả rơ moóc và sơ mi rơ moóc) vượt quá trọng tải (khối lượng hàng chuyên chở) cho phép tham gia giao thông được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe trên 10% đến 50% (trừ xe xi téc chở chất lỏng), trên 20% đến 50% đối với xe xi téc chở chất lỏng;
b) Xếp hàng hóa lên xe ô tô mà không ký xác nhận việc xếp hàng hóa vào giấy vận tải theo quy định.

[0] 500.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D26/K1)
[1] 1.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D26/K1)
[2] 2.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D26/K1)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Công ty tôi đã xếp hàng hóa lên xe ô tô vượt quá trọng tải 30% mà không ký xác nhận, mức phạt tiền là bao nhiêu?
- Đáp: Phạt tiền từ 500.000 đồng đến 1.000.000 đồng.
- ⚠ chep_nguyen_van: “hàng hóa lên xe ô tô …”

```json
{"qid": "tD-muc_phat-023", "question": "Công ty tôi đã xếp hàng hóa lên xe ô tô vượt quá trọng tải 30% mà không ký xác nhận, mức phạt tiền là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Phạt tiền từ 500.000 đồng đến 1.000.000 đồng.", "gold_units": ["ND168-2024/D26/K1"], "required_numbers": [{"value": 500000, "unit": "vnd"}, {"value": 1000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-023:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi đã xếp hàng hóa lên xe ô tô mà không ký xác nhận, mức phạt tiền là bao nhiêu?
- Đáp: Phạt tiền từ 500.000 đồng đến 1.000.000 đồng.
- ⚠ chep_nguyen_van: “hàng hóa lên xe ô tô …”

```json
{"qid": "tD-muc_phat-023", "question": "Tôi đã xếp hàng hóa lên xe ô tô mà không ký xác nhận, mức phạt tiền là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Phạt tiền từ 500.000 đồng đến 1.000.000 đồng.", "gold_units": ["ND168-2024/D26/K1"], "required_numbers": [{"value": 500000, "unit": "vnd"}, {"value": 1000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-023:2"}
```

### WD-muc_phat-024 · tier A · vai: cán bộ phường · kiểu: ngan

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D24/K1

Điều 24. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển động vật sống, thực phẩm tươi sống
1. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với hành vi vi phạm vận chuyển động vật sống, thực phẩm tươi sống không mang đủ giấy tờ theo quy định (đối với loại động vật sống, thực phẩm tươi sống khi vận chuyển phải có giấy tờ).

[0] 1.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D24/K1)
[1] 2.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D24/K1)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi lái xe ô tô chở con bò mà không có giấy tờ, mức phạt tiền là bao nhiêu?
- Đáp: Bạn sẽ bị phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng. (Điều 24 Nghị định 168/2024/NĐ-CP)

```json
{"qid": "tD-muc_phat-024", "question": "Tôi lái xe ô tô chở con bò mà không có giấy tờ, mức phạt tiền là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Bạn sẽ bị phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng. (Điều 24 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D24/K1"], "required_numbers": [{"value": 1000000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-024:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Công ty tôi vận chuyển thực phẩm tươi sống mà không có giấy tờ, mức phạt tiền là bao nhiêu?
- Đáp: Bạn sẽ bị phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng. (Điều 24 Nghị định 168/2024/NĐ-CP)

```json
{"qid": "tD-muc_phat-024", "question": "Công ty tôi vận chuyển thực phẩm tươi sống mà không có giấy tờ, mức phạt tiền là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Bạn sẽ bị phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng. (Điều 24 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D24/K1"], "required_numbers": [{"value": 1000000, "unit": "vnd"}, {"value": 2000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-024:2"}
```

### WD-muc_phat-025 · tier A · vai: cán bộ phường · kiểu: ngan

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2026-08-15 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K8, ND168-2024/D21/K8/a, ND168-2024/D21/K8/b, ND168-2024/D21/K8/c, ND168-2024/D21/K8/d, ND168-2024/D21/K8/đ, ND168-2024/D21/K8/e

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
8. Phạt tiền từ 8.000.000 đồng đến 12.000.000 đồng đối với một trong các hành vi sau đây:
a) Điều khiển xe (kể cả rơ moóc và sơ mi rơ moóc) chở hàng vượt trọng tải (khối lượng hàng chuyên chở) cho phép tham gia giao thông được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe trên 150%;
b) Điều khiển xe kéo theo rơ moóc, sơ mi rơ moóc mà khối lượng toàn bộ (bao gồm khối lượng bản thân rơ moóc, sơ mi rơ moóc và khối lượng hàng chuyên chở) của rơ moóc, sơ mi rơ moóc vượt khối lượng cho phép kéo theo được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe trên 150%;
c) Chở công-ten-nơ trên xe (kể cả sơ mi rơ moóc) không bảo đảm quy chuẩn, tiêu chuẩn kỹ thuật của công-ten-nơ theo quy định;
d) Chở thiết bị có hình dạng thùng hoặc có hình dạng như công-ten-nơ (không phải công-ten-nơ) vượt quá chiều dài toàn bộ được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của rơ moóc, sơ mi rơ moóc; chở loại hàng không đúng với thông tin ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của rơ moóc, sơ mi rơ moóc;
…

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D21/K13/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K13/b

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
13. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
b) Thực hiện hành vi quy định tại điểm a, điểm b khoản 6; điểm c, điểm d, điểm đ khoản 8; khoản 10 Điều này bị trừ điểm giấy phép lái xe 04 điểm;

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D21/K13/đ)
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K13/đ

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
13. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
đ) Thực hiện hành vi quy định tại điểm a, điểm b khoản 8; khoản 11 Điều này bị trừ điểm giấy phép lái xe 10 điểm.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D21/K10)
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K10

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
10. Phạt tiền từ 18.000.000 đồng đến 22.000.000 đồng đối với một trong các hành vi vi phạm sau đây:

[0] 8.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D21/K8)
[1] 12.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D21/K8)
[2] 04 điểm (số điểm bị trừ, nêu tại ND168-2024/D21/K13/b)
[3] 10 điểm (số điểm bị trừ, nêu tại ND168-2024/D21/K13/đ)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi lái xe tải kéo rơ moóc, chở hàng vượt trọng tải cho phép 20% hơn, tôi sẽ bị phạt tiền và trừ điểm bao nhiêu?
- Đáp: Bạn sẽ bị phạt tiền từ 8.000.000 đồng đến 12.000.000 đồng và bị trừ 04 điểm giấy phép lái xe.
- ⚠ chep_nguyen_van: “moóc chở hàng vượt trọng tải …”
- Ghi chú: Giả định xe tải có rơ moóc, chở hàng vượt trọng tải 20%

```json
{"qid": "tD-muc_phat-025", "question": "Tôi lái xe tải kéo rơ moóc, chở hàng vượt trọng tải cho phép 20% hơn, tôi sẽ bị phạt tiền và trừ điểm bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Bạn sẽ bị phạt tiền từ 8.000.000 đồng đến 12.000.000 đồng và bị trừ 04 điểm giấy phép lái xe.", "gold_units": ["ND168-2024/D21/K8", "ND168-2024/D21/K13/b"], "required_numbers": [{"value": 8000000, "unit": "vnd"}, {"value": 12000000, "unit": "vnd"}, {"value": 4, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-025:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi lái xe tải kéo rơ moóc, khối lượng toàn bộ (xe + rơ moóc + hàng) vượt giới hạn 20%, tôi sẽ bị phạt tiền và trừ điểm bao nhiêu?
- Đáp: Bạn sẽ bị phạt tiền từ 8.000.000 đồng đến 12.000.000 đồng và bị trừ 04 điểm giấy phép lái xe.
- Ghi chú: Giả định xe tải có rơ moóc, khối lượng toàn bộ vượt giới hạn 20%

```json
{"qid": "tD-muc_phat-025", "question": "Tôi lái xe tải kéo rơ moóc, khối lượng toàn bộ (xe + rơ moóc + hàng) vượt giới hạn 20%, tôi sẽ bị phạt tiền và trừ điểm bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Bạn sẽ bị phạt tiền từ 8.000.000 đồng đến 12.000.000 đồng và bị trừ 04 điểm giấy phép lái xe.", "gold_units": ["ND168-2024/D21/K8", "ND168-2024/D21/K13/b"], "required_numbers": [{"value": 8000000, "unit": "vnd"}, {"value": 12000000, "unit": "vnd"}, {"value": 4, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-025:2"}
```

### WD-muc_phat-026 · tier A · vai: cán bộ phường · kiểu: tinh_huong_nguoi_khac

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D12/K1

Điều 12. Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm khác về quy tắc giao thông đường bộ; sử dụng lòng đường, vỉa hè vào mục đích khác
1. Phạt tiền từ 100.000 đồng đến 200.000 đồng đối với người được chở trên xe đạp, xe đạp máy sử dụng ô (dù).

[0] 100.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D12/K1)
[1] 200.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D12/K1)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Cán bộ phường: Anh tôi đã thuê một chiếc xe đạp máy có ô để chở khách, anh ấy sẽ bị phạt tiền bao nhiêu?
- Đáp: Người được chở trên xe đạp, xe đạp máy sử dụng ô sẽ bị phạt tiền từ 100.000 đồng đến 200.000 đồng.
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-muc_phat-026", "question": "Cán bộ phường: Anh tôi đã thuê một chiếc xe đạp máy có ô để chở khách, anh ấy sẽ bị phạt tiền bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Người được chở trên xe đạp, xe đạp máy sử dụng ô sẽ bị phạt tiền từ 100.000 đồng đến 200.000 đồng.", "gold_units": ["ND168-2024/D12/K1"], "required_numbers": [{"value": 100000, "unit": "vnd"}, {"value": 200000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-026:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Cán bộ phường: Tôi nghe có người dùng xe đạp máy có ô để chở khách, họ sẽ bị phạt tiền bao nhiêu?
- Đáp: Người được chở trên xe đạp, xe đạp máy sử dụng ô sẽ bị phạt tiền từ 100.000 đồng đến 200.000 đồng.
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-muc_phat-026", "question": "Cán bộ phường: Tôi nghe có người dùng xe đạp máy có ô để chở khách, họ sẽ bị phạt tiền bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Người được chở trên xe đạp, xe đạp máy sử dụng ô sẽ bị phạt tiền từ 100.000 đồng đến 200.000 đồng.", "gold_units": ["ND168-2024/D12/K1"], "required_numbers": [{"value": 100000, "unit": "vnd"}, {"value": 200000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-026:2"}
```

### WD-muc_phat-027 · tier A · vai: phụ huynh có con dưới 18 tuổi · kiểu: tinh_huong_ban_than

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K4

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
4. Phạt tiền từ 800.000 đồng đến 1.000.000 đồng đối với cá nhân, từ 1.600.000 đồng đến 2.000.000 đồng đối với tổ chức là chủ xe mô tô, xe gắn máy và các loại xe tương tự xe mô tô, các loại xe tương tự xe gắn máy không thực hiện đúng quy định về biển số, trừ các hành vi vi phạm quy định tại điểm g, điểm h khoản 8 Điều này.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D32/K8/g)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K8/g

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
8. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng đối với cá nhân, từ 8.000.000 đến 12.000.000 đồng đối với tổ chức là chủ xe mô tô, xe gắn máy và các loại xe tương tự xe mô tô, các loại xe tương tự xe gắn máy thực hiện một trong các hành vi vi phạm sau đây:
g) Lắp đặt, sử dụng thiết bị thay đổi biển số trên xe trái quy định;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D32/K8/h)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K8/h

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
8. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng đối với cá nhân, từ 8.000.000 đến 12.000.000 đồng đối với tổ chức là chủ xe mô tô, xe gắn máy và các loại xe tương tự xe mô tô, các loại xe tương tự xe gắn máy thực hiện một trong các hành vi vi phạm sau đây:
h) Đưa phương tiện không gắn biển số (đối với loại xe có quy định phải gắn biển số) tham gia giao thông; đưa phương tiện gắn biển số không đúng với chứng nhận đăng ký xe hoặc gắn biển số không do cơ quan có thẩm quyền cấp tham gia giao thông.

[0] 800.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D32/K4)
[1] 1.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D32/K4)
[2] 1.600.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D32/K4)
[3] 2.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D32/K4)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi có con 15 tuổi, anh ấy lái xe máy mà không gắn biển số, tôi muốn biết mức phạt tiền mà chủ xe phải chịu?
- Đáp: Mức phạt tiền là từ 800.000 đồng đến 1.000.000 đồng. (Điều 32 Khoản 4 Nghị định 168/2024/NĐ-CP)
- Ghi chú: giả định xe máy là xe mô tô

```json
{"qid": "tD-muc_phat-027", "question": "Tôi có con 15 tuổi, anh ấy lái xe máy mà không gắn biển số, tôi muốn biết mức phạt tiền mà chủ xe phải chịu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Mức phạt tiền là từ 800.000 đồng đến 1.000.000 đồng. (Điều 32 Khoản 4 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D32/K4"], "required_numbers": [{"value": 800000, "unit": "vnd"}, {"value": 1000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-027:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi có con 16 tuổi, anh ấy lái xe máy mà gắn biển số không khớp với giấy đăng ký, tôi muốn biết mức phạt tiền mà chủ xe phải chịu?
- Đáp: Mức phạt tiền là từ 800.000 đồng đến 1.000.000 đồng. (Điều 32 Khoản 4 Nghị định 168/2024/NĐ-CP)
- Ghi chú: giả định xe máy là xe mô tô

```json
{"qid": "tD-muc_phat-027", "question": "Tôi có con 16 tuổi, anh ấy lái xe máy mà gắn biển số không khớp với giấy đăng ký, tôi muốn biết mức phạt tiền mà chủ xe phải chịu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Mức phạt tiền là từ 800.000 đồng đến 1.000.000 đồng. (Điều 32 Khoản 4 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D32/K4"], "required_numbers": [{"value": 800000, "unit": "vnd"}, {"value": 1000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-027:2"}
```

### WD-muc_phat-028 · tier A · vai: tài xế xe tải · kiểu: ngan

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D33/K1, ND168-2024/D33/K1/a, ND168-2024/D33/K1/b

Điều 33. Xử phạt hành khách đi xe vi phạm quy định về trật tự, an toàn giao thông
1. Phạt tiền từ 100.000 đồng đến 200.000 đồng đối với một trong các hành vi vi phạm sau đây:
a) Không chấp hành hướng dẫn của lái xe, nhân viên phục vụ trên xe về các quy định bảo đảm trật tự, an toàn giao thông;
b) Gây mất trật tự trên xe.

[0] 100.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D33/K1)
[1] 200.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D33/K1)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Nếu hành khách trên xe tải của tôi không nghe lời khi tôi dừng xe, họ sẽ bị phạt tiền bao nhiêu?
- Đáp: Phạt tiền từ 100.000 đồng đến 200.000 đồng.

```json
{"qid": "tD-muc_phat-028", "question": "Nếu hành khách trên xe tải của tôi không nghe lời khi tôi dừng xe, họ sẽ bị phạt tiền bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Phạt tiền từ 100.000 đồng đến 200.000 đồng.", "gold_units": ["ND168-2024/D33/K1"], "required_numbers": [{"value": 100000, "unit": "vnd"}, {"value": 200000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-028:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Nếu hành khách trên xe tải của tôi gây mất trật tự khi đang di chuyển, mức phạt tiền là bao nhiêu?
- Đáp: Phạt tiền từ 100.000 đồng đến 200.000 đồng.

```json
{"qid": "tD-muc_phat-028", "question": "Nếu hành khách trên xe tải của tôi gây mất trật tự khi đang di chuyển, mức phạt tiền là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Phạt tiền từ 100.000 đồng đến 200.000 đồng.", "gold_units": ["ND168-2024/D33/K1"], "required_numbers": [{"value": 100000, "unit": "vnd"}, {"value": 200000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-028:2"}
```

### WD-muc_phat-029 · tier A · vai: chủ doanh nghiệp vận tải · kiểu: tinh_huong_ban_than

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D12/K5, ND168-2024/D12/K5/a, ND168-2024/D12/K5/b

Điều 12. Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm khác về quy tắc giao thông đường bộ; sử dụng lòng đường, vỉa hè vào mục đích khác
5. Phạt tiền từ 400.000 đồng đến 600.000 đồng đối với người được chở trên xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô, các loại xe tương tự xe gắn máy thực hiện một trong các hành vi vi phạm sau đây:
a) Bám, kéo, đẩy xe khác, vật khác, dẫn dắt vật nuôi, mang vác vật cồng kềnh, đứng trên yên, giá đèo hàng hoặc ngồi trên tay lái của xe;
b) Không đội “mũ bảo hiểm cho người đi mô tô, xe máy” hoặc đội “mũ bảo hiểm cho người đi mô tô, xe máy” không cài quai đúng quy cách khi tham gia giao thông trên đường bộ.

[0] 400.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D12/K5)
[1] 600.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D12/K5)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi đang điều hành công ty vận tải, một khách hàng trên xe máy của tôi không đội mũ bảo hiểm đúng cách. Tôi cần biết mức phạt tiền mà người vi phạm phải chịu?
- Đáp: Người vi phạm phải chịu phạt tiền từ 400.000 đồng đến 600.000 đồng. (khoản 5 Điều 12 Nghị định 168/2024/NĐ-CP)
- Ghi chú: Giả định người vi phạm là hành khách trên xe máy

```json
{"qid": "tD-muc_phat-029", "question": "Tôi đang điều hành công ty vận tải, một khách hàng trên xe máy của tôi không đội mũ bảo hiểm đúng cách. Tôi cần biết mức phạt tiền mà người vi phạm phải chịu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Người vi phạm phải chịu phạt tiền từ 400.000 đồng đến 600.000 đồng. (khoản 5 Điều 12 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D12/K5"], "required_numbers": [{"value": 400000, "unit": "vnd"}, {"value": 600000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-029:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là chủ doanh nghiệp vận tải, một hành khách trên xe máy của tôi đã ngồi trên tay lái của người lái. Tôi muốn biết mức phạt tiền mà người vi phạm phải chịu?
- Đáp: Người vi phạm phải chịu phạt tiền từ 400.000 đồng đến 600.000 đồng. (khoản 5 Điều 12 Nghị định 168/2024/NĐ-CP)
- Ghi chú: Giả định người vi phạm là hành khách trên xe máy

```json
{"qid": "tD-muc_phat-029", "question": "Tôi là chủ doanh nghiệp vận tải, một hành khách trên xe máy của tôi đã ngồi trên tay lái của người lái. Tôi muốn biết mức phạt tiền mà người vi phạm phải chịu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Người vi phạm phải chịu phạt tiền từ 400.000 đồng đến 600.000 đồng. (khoản 5 Điều 12 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D12/K5"], "required_numbers": [{"value": 400000, "unit": "vnd"}, {"value": 600000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-029:2"}
```

### WD-muc_phat-030 · tier A · vai: phụ huynh có con dưới 18 tuổi · kiểu: tinh_huong_nguoi_khac

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2026-08-15 → 2027-12-31
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K9a, ND168-2024/D32/K9a/a

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
9a. Phạt tiền từ 5.000.000 đồng đến 6.000.000 đồng đối với cá nhân, từ 10.000.000 đồng đến 12.000.000 đồng đối với tổ chức là chủ xe ô tô đầu kéo, xe vận tải nội bộ thực hiện một trong các hành vi vi phạm sau đây:
a) Đưa xe không lắp thiết bị giám sát hành trình của xe hoặc có lắp thiết bị giám sát hành trình nhưng không hoạt động, không đúng quy chuẩn theo quy định hoặc làm sai lệch dữ liệu của thiết bị giám sát hành trình của xe ô tô;

[0] 5.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D32/K9a)
[1] 6.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D32/K9a)
[2] 10.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D32/K9a)
[3] 12.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D32/K9a)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Anh tôi lái xe ô tô đầu kéo, không lắp thiết bị giám sát hành trình, bị cảnh sát hỏi, mức phạt tiền là bao nhiêu?
- Đáp: Mức phạt tiền là từ 5.000.000 đồng đến 6.000.000 đồng. (khoản 9a Điều 32 Nghị định 168/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “không lắp thiết bị giám sát …”
- Ghi chú: Giả định là cá nhân lái xe

```json
{"qid": "tD-muc_phat-030", "question": "Anh tôi lái xe ô tô đầu kéo, không lắp thiết bị giám sát hành trình, bị cảnh sát hỏi, mức phạt tiền là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Mức phạt tiền là từ 5.000.000 đồng đến 6.000.000 đồng. (khoản 9a Điều 32 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D32/K9a"], "required_numbers": [{"value": 5000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-030:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Công ty tôi thuê xe ô tô đầu kéo để vận chuyển hàng, nhưng không lắp thiết bị giám sát hành trình, nếu bị xử phạt thì mức tiền là bao nhiêu?
- Đáp: Mức phạt tiền là từ 10.000.000 đồng đến 12.000.000 đồng. (khoản 9a Điều 32 Nghị định 168/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “không lắp thiết bị giám sát …”
- Ghi chú: Giả định là tổ chức thuê xe

```json
{"qid": "tD-muc_phat-030", "question": "Công ty tôi thuê xe ô tô đầu kéo để vận chuyển hàng, nhưng không lắp thiết bị giám sát hành trình, nếu bị xử phạt thì mức tiền là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Mức phạt tiền là từ 10.000.000 đồng đến 12.000.000 đồng. (khoản 9a Điều 32 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D32/K9a"], "required_numbers": [{"value": 10000000, "unit": "vnd"}, {"value": 12000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-030:2"}
```

### WD-muc_phat-031 · tier A · vai: tài xế xe tải · kiểu: tinh_huong_nguoi_khac

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D12/K13

Điều 12. Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm khác về quy tắc giao thông đường bộ; sử dụng lòng đường, vỉa hè vào mục đích khác
13. Phạt tiền từ 30.000.000 đồng đến 32.000.000 đồng đối với cá nhân, từ 60.000.000 đồng đến 64.000.000 đồng đối với tổ chức thực hiện hành vi không khai báo, khai báo gian dối hoặc cung cấp thông tin, tài liệu không đúng sự thật để trốn tránh trách nhiệm khi bị phát hiện vi phạm pháp luật về trật tự, an toàn giao thông đường bộ.

[0] 30.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D12/K13)
[1] 32.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D12/K13)
[2] 60.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D12/K13)
[3] 64.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D12/K13)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Anh tôi, một tài xế xe tải, đã bị cảnh sát hỏi về việc không khai báo thông tin khi kiểm tra lô hàng. Anh ấy cho rằng mình không có lỗi, nhưng cảnh sát lại nghi ngờ có gian dối. Anh ấy muốn biết mức phạt tiền mà anh ấy có thể phải chịu nếu bị xác định vi phạm.
- Đáp: Nếu vi phạm, mức phạt tiền sẽ từ 30.000.000 đồng đến 32.000.000 đồng. (khoản 13 Điều 12 Nghị định 168/2024/NĐ-CP)
- ⚠ qua_dai (61 từ)

```json
{"qid": "tD-muc_phat-031", "question": "Anh tôi, một tài xế xe tải, đã bị cảnh sát hỏi về việc không khai báo thông tin khi kiểm tra lô hàng. Anh ấy cho rằng mình không có lỗi, nhưng cảnh sát lại nghi ngờ có gian dối. Anh ấy muốn biết mức phạt tiền mà anh ấy có thể phải chịu nếu bị xác định vi phạm.", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Nếu vi phạm, mức phạt tiền sẽ từ 30.000.000 đồng đến 32.000.000 đồng. (khoản 13 Điều 12 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D12/K13"], "required_numbers": [{"value": 30000000, "unit": "vnd"}, {"value": 32000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-031:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Công ty tôi đang vận chuyển hàng hóa bằng xe tải và một nhân viên đã cung cấp tài liệu sai lệch cho cảnh sát khi kiểm tra. Công ty muốn biết mức phạt tiền mà họ có thể phải chịu nếu bị phát hiện vi phạm.
- Đáp: Nếu vi phạm, mức phạt tiền sẽ từ 60.000.000 đồng đến 64.000.000 đồng. (khoản 13 Điều 12 Nghị định 168/2024/NĐ-CP)

```json
{"qid": "tD-muc_phat-031", "question": "Công ty tôi đang vận chuyển hàng hóa bằng xe tải và một nhân viên đã cung cấp tài liệu sai lệch cho cảnh sát khi kiểm tra. Công ty muốn biết mức phạt tiền mà họ có thể phải chịu nếu bị phát hiện vi phạm.", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Nếu vi phạm, mức phạt tiền sẽ từ 60.000.000 đồng đến 64.000.000 đồng. (khoản 13 Điều 12 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D12/K13"], "required_numbers": [{"value": 60000000, "unit": "vnd"}, {"value": 64000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-031:2"}
```

### WD-muc_phat-032 · tier A · vai: sinh viên đi xe máy · kiểu: tinh_huong_ban_than

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D39/K1, ND168-2024/D39/K1/a, ND168-2024/D39/K1/b, ND168-2024/D39/K1/c, ND168-2024/D39/K1/d, ND168-2024/D39/K1/đ, ND168-2024/D39/K1/e

Điều 39. Xử phạt các hành vi vi phạm quy định về đào tạo, sát hạch lái xe
1. Phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng đối với giáo viên dạy lái xe thực hiện một trong các hành vi vi phạm sau đây:
a) Giáo viên dạy thực hành để học viên không có phù hiệu “Học viên tập lái xe” lái xe tập lái hoặc có phù hiệu nhưng không đeo khi lái xe tập lái;
b) Giáo viên dạy thực hành chở người, hàng trên xe tập lái trái quy định;
c) Giáo viên dạy thực hành chạy không đúng tuyến đường trong giấy phép xe tập lái; không ngồi bên cạnh để bảo trợ tay lái cho học viên thực hành lái xe (kể cả trong sân tập lái và ngoài đường giao thông công cộng);
d) Không đeo phù hiệu “Giáo viên dạy lái xe” khi giảng dạy;
đ) Không có giáo án của môn học được phân công giảng dạy theo quy định hoặc có giáo án nhưng không phù hợp với môn được phân công giảng dạy;
e) Giáo viên dạy thực hành không mang theo giấy phép xe tập lái hoặc mang theo giấy phép xe tập lái đã hết giá trị sử dụng.

[0] 2.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D39/K1)
[1] 3.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D39/K1)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi học lái xe máy, giáo viên dạy thực hành không đeo biển hiệu 'Giáo viên dạy lái xe', tôi bị phạt bao nhiêu?
- Đáp: Bạn sẽ bị phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng. (khoản 1 Điều 39 Nghị định 168/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “giáo viên dạy thực hành không …”
- Ghi chú: giáo viên dạy thực hành không đeo biển hiệu

```json
{"qid": "tD-muc_phat-032", "question": "Tôi học lái xe máy, giáo viên dạy thực hành không đeo biển hiệu 'Giáo viên dạy lái xe', tôi bị phạt bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Bạn sẽ bị phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng. (khoản 1 Điều 39 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D39/K1/d"], "required_numbers": [{"value": 2000000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-032:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi học lái xe máy, giáo viên dạy thực hành không có giáo án phù hợp, tôi bị phạt bao nhiêu?
- Đáp: Bạn sẽ bị phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng. (khoản 1 Điều 39 Nghị định 168/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “giáo viên dạy thực hành không …”
- Ghi chú: giáo viên dạy thực hành không có giáo án

```json
{"qid": "tD-muc_phat-032", "question": "Tôi học lái xe máy, giáo viên dạy thực hành không có giáo án phù hợp, tôi bị phạt bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "A", "answer": "Bạn sẽ bị phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng. (khoản 1 Điều 39 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D39/K1/đ"], "required_numbers": [{"value": 2000000, "unit": "vnd"}, {"value": 3000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-032:2"}
```

### WD-muc_phat-033 · tier B · vai: chủ doanh nghiệp vận tải · kiểu: tinh_huong_nguoi_khac

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)
Hiệu lực của trạng thái này: 2026-03-01 → nay
Mã điều khoản dùng được cho gold_units: ND336-2025/D10/K6, ND336-2025/D10/K6/a, ND336-2025/D10/K6/b

Điều 10. Xử phạt các hành vi vi phạm về thanh toán điện tử giao thông đường bộ, hoạt động trạm thu phí đường bộ
6. Phạt tiền từ 80.000.000 đồng đến 100.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
a) Không quản lý số tiền trong tài khoản thu tiền sử dụng đường bộ độc lập và tách biệt với các khoản tiền khác của nhà cung cấp dịch vụ thanh toán tiền sử dụng đường bộ;
b) Sử dụng sai mục đích tiền trong tài khoản thu tiền sử dụng đường bộ.

[0] 80.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D10/K6)
[1] 100.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D10/K6)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Anh tôi, công ty cạnh tôi, vừa bị cảnh sát kiểm tra tài khoản thu phí đường bộ và phát hiện rằng họ đã dùng tiền trong tài khoản này cho các chi phí khác ngoài phí giao thông. Anh tôi muốn biết mức phạt tiền mà công ty đó phải chịu?
- Đáp: Công ty sẽ bị phạt tiền từ 80.000.000 đồng đến 100.000.000 đồng. (Điều 10, khoản 6, Nghị định 336/2025/NĐ-CP)
- ⚠ qua_dai (52 từ); tham_chieu_ngu_canh

```json
{"qid": "tD-muc_phat-033", "question": "Anh tôi, công ty cạnh tôi, vừa bị cảnh sát kiểm tra tài khoản thu phí đường bộ và phát hiện rằng họ đã dùng tiền trong tài khoản này cho các chi phí khác ngoài phí giao thông. Anh tôi muốn biết mức phạt tiền mà công ty đó phải chịu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "B", "answer": "Công ty sẽ bị phạt tiền từ 80.000.000 đồng đến 100.000.000 đồng. (Điều 10, khoản 6, Nghị định 336/2025/NĐ-CP)", "gold_units": ["ND336-2025/D10/K6"], "required_numbers": [{"value": 80000000, "unit": "vnd"}, {"value": 100000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-033:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Công ty tôi đang quản lý tài khoản thu phí đường bộ, nhưng một nhân viên đã chuyển một phần tiền thu được sang tài khoản cá nhân của mình. Tôi muốn biết mức phạt tiền mà công ty sẽ phải chịu vì hành vi này.
- Đáp: Công ty sẽ bị phạt tiền từ 80.000.000 đồng đến 100.000.000 đồng. (Điều 10, khoản 6, Nghị định 336/2025/NĐ-CP)

```json
{"qid": "tD-muc_phat-033", "question": "Công ty tôi đang quản lý tài khoản thu phí đường bộ, nhưng một nhân viên đã chuyển một phần tiền thu được sang tài khoản cá nhân của mình. Tôi muốn biết mức phạt tiền mà công ty sẽ phải chịu vì hành vi này.", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "B", "answer": "Công ty sẽ bị phạt tiền từ 80.000.000 đồng đến 100.000.000 đồng. (Điều 10, khoản 6, Nghị định 336/2025/NĐ-CP)", "gold_units": ["ND336-2025/D10/K6"], "required_numbers": [{"value": 80000000, "unit": "vnd"}, {"value": 100000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-033:2"}
```

### WD-muc_phat-034 · tier B · vai: phụ huynh có con dưới 18 tuổi · kiểu: neu_van_ban

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)
Hiệu lực của trạng thái này: 2026-03-01 → nay
Mã điều khoản dùng được cho gold_units: ND336-2025/D5/K5, ND336-2025/D5/K5/a, ND336-2025/D5/K5/b, ND336-2025/D5/K5/c, ND336-2025/D5/K5/d

Điều 5. Xử phạt các hành vi vi phạm quy định về sử dụng, khai thác trong phạm vi đất dành cho kết cấu hạ tầng đường bộ
5. Phạt tiền từ 10.000.000 đồng đến 15.000.000 đồng đối với cá nhân, từ 20.000.000 đồng đến 30.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
a) Xây dựng, lắp đặt biển quảng cáo trong phạm vi hành lang an toàn đường bộ mà không có văn bản chấp thuận theo quy định, trừ hành vi vi phạm quy định tại điểm d khoản 6 Điều này;
b) Không thực hiện việc tháo dỡ biển quảng cáo, các bộ phận của biển quảng cáo khi có yêu cầu của cơ quan quản lý đường bộ, người quản lý, sử dụng đường bộ;
c) Không xóa bỏ, đóng điểm đấu nối tạm thời khi hết thời hạn đấu nối tạm;
d) Không hoàn trả nguyên trạng hành lang an toàn đường bộ; không sửa chữa, bổ sung kết cấu hạ tầng đường bộ bị ảnh hưởng do việc thực hiện đấu nối tạm thời.

### Điều khoản được nguồn trên dẫn chiếu tới (ND336-2025/D5/K6/d)
Mã điều khoản dùng được cho gold_units: ND336-2025/D5/K6/d

Điều 5. Xử phạt các hành vi vi phạm quy định về sử dụng, khai thác trong phạm vi đất dành cho kết cấu hạ tầng đường bộ
6. Phạt tiền từ 15.000.000 đồng đến 20.000.000 đồng đối với cá nhân, từ 30.000.000 đồng đến 40.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
d) Xây dựng, lắp đặt biển quảng cáo trong phạm vi hành lang an toàn đường cao tốc.

[0] 10.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D5/K5)
[1] 15.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D5/K5)
[2] 20.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D5/K5)
[3] 30.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D5/K5)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Con tôi đang học lái xe và tôi thấy một biển quảng cáo được đặt trên hành lang an toàn của một đường cao tốc mà không có giấy phép. Nếu người xây dựng không được phép, mức phạt tiền mà họ phải chịu là bao nhiêu?
- Đáp: Mức phạt tiền sẽ từ 10.000.000 đồng đến 15.000.000 đồng cho cá nhân. (Điều 5, Khoản 5, Điểm a Nghị định 336/2025/NĐ-CP)

```json
{"qid": "tD-muc_phat-034", "question": "Con tôi đang học lái xe và tôi thấy một biển quảng cáo được đặt trên hành lang an toàn của một đường cao tốc mà không có giấy phép. Nếu người xây dựng không được phép, mức phạt tiền mà họ phải chịu là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "B", "answer": "Mức phạt tiền sẽ từ 10.000.000 đồng đến 15.000.000 đồng cho cá nhân. (Điều 5, Khoản 5, Điểm a Nghị định 336/2025/NĐ-CP)", "gold_units": ["ND336-2025/D5/K5/a"], "required_numbers": [{"value": 10000000, "unit": "vnd"}, {"value": 15000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-034:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Nếu một công ty xây dựng lắp đặt biển quảng cáo trên hành lang an toàn của đường cao tốc mà không có văn bản chấp thuận, họ sẽ bị phạt tiền bao nhiêu?
- Đáp: Mức phạt tiền sẽ từ 20.000.000 đồng đến 30.000.000 đồng cho tổ chức. (Điều 5, Khoản 5, Điểm a Nghị định 336/2025/NĐ-CP)
- ⚠ chep_nguyen_van: “dựng lắp đặt biển quảng cáo …”

```json
{"qid": "tD-muc_phat-034", "question": "Nếu một công ty xây dựng lắp đặt biển quảng cáo trên hành lang an toàn của đường cao tốc mà không có văn bản chấp thuận, họ sẽ bị phạt tiền bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "B", "answer": "Mức phạt tiền sẽ từ 20.000.000 đồng đến 30.000.000 đồng cho tổ chức. (Điều 5, Khoản 5, Điểm a Nghị định 336/2025/NĐ-CP)", "gold_units": ["ND336-2025/D5/K5/a"], "required_numbers": [{"value": 20000000, "unit": "vnd"}, {"value": 30000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-034:2"}
```

### WD-muc_phat-035 · tier B · vai: phụ huynh có con dưới 18 tuổi · kiểu: tinh_huong_nguoi_khac

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)
Hiệu lực của trạng thái này: 2026-03-01 → nay
Mã điều khoản dùng được cho gold_units: ND336-2025/D12/K5, ND336-2025/D12/K5/a, ND336-2025/D12/K5/b

Điều 12. Xử phạt các hành vi vi phạm quy định về vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
5. Phạt tiền từ 10.000.000 đồng đến 15.000.000 đồng đối với cá nhân, từ 20.000.000 đồng đến 30.000.000 đồng đối với tổ chức kinh doanh vận tải, dịch vụ hỗ trợ vận tải thực hiện một trong các hành vi vi phạm sau đây:
a) Bến xe không kê khai, công bố thông tin về giá dịch vụ xe ra, vào bến xe theo quy định của pháp luật về giá;
b) Không kê khai giá dịch vụ vận tải hành khách tuyến cố định bằng đường bộ, dịch vụ vận tải hành khách bằng taxi theo quy định.

[0] 10.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D12/K5)
[1] 15.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D12/K5)
[2] 20.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D12/K5)
[3] 30.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D12/K5)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Anh tôi đang làm việc tại một bến xe, và anh ấy nói rằng bến không công bố giá cước cho khách hàng. Tôi muốn biết mức phạt tiền mà cơ quan có thể áp dụng cho trường hợp này.
- Đáp: Mức phạt tiền có thể từ 10.000.000 đồng đến 15.000.000 đồng. (Điều 12, khoản 5, điểm a Nghị định 336/2025/NĐ-CP)

```json
{"qid": "tD-muc_phat-035", "question": "Anh tôi đang làm việc tại một bến xe, và anh ấy nói rằng bến không công bố giá cước cho khách hàng. Tôi muốn biết mức phạt tiền mà cơ quan có thể áp dụng cho trường hợp này.", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "B", "answer": "Mức phạt tiền có thể từ 10.000.000 đồng đến 15.000.000 đồng. (Điều 12, khoản 5, điểm a Nghị định 336/2025/NĐ-CP)", "gold_units": ["ND336-2025/D12/K5"], "required_numbers": [{"value": 10000000, "unit": "vnd"}, {"value": 15000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-035:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Con tôi thường đi taxi, và anh lái xe nói rằng anh không ghi lại giá cước cố định cho tuyến đường. Tôi muốn biết mức phạt tiền mà cơ quan có thể áp dụng cho hành vi này.
- Đáp: Mức phạt tiền có thể từ 20.000.000 đồng đến 30.000.000 đồng. (Điều 12, khoản 5, điểm b Nghị định 336/2025/NĐ-CP)

```json
{"qid": "tD-muc_phat-035", "question": "Con tôi thường đi taxi, và anh lái xe nói rằng anh không ghi lại giá cước cố định cho tuyến đường. Tôi muốn biết mức phạt tiền mà cơ quan có thể áp dụng cho hành vi này.", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "B", "answer": "Mức phạt tiền có thể từ 20.000.000 đồng đến 30.000.000 đồng. (Điều 12, khoản 5, điểm b Nghị định 336/2025/NĐ-CP)", "gold_units": ["ND336-2025/D12/K5"], "required_numbers": [{"value": 20000000, "unit": "vnd"}, {"value": 30000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-035:2"}
```

### WD-muc_phat-036 · tier B · vai: người mới học lái ô tô · kiểu: ngan

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)
Hiệu lực của trạng thái này: 2026-03-01 → nay
Mã điều khoản dùng được cho gold_units: ND336-2025/D8/K2, ND336-2025/D8/K2/a, ND336-2025/D8/K2/b, ND336-2025/D8/K2/c

Điều 8. Xử phạt các hành vi vi phạm quy định về thi công trong phạm vi bảo vệ kết cấu hạ tầng đường bộ
2. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với cá nhân, từ 6.000.000 đồng đến 10.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
a) Thi công công trình trong phạm vi đất dành cho kết cấu hạ tầng đường bộ không thực hiện đúng biện pháp tổ chức giao thông trong hồ sơ kèm theo giấy phép thi công hoặc văn bản chấp thuận của cơ quan có thẩm quyền, trừ hành vi vi phạm quy định tại khoản 1; điểm b, điểm c khoản này; điểm a, điểm b khoản 3; điểm a, điểm b, điểm d khoản 4; điểm a, điểm b, điểm c khoản 5 Điều này;
b) Để vật liệu, đất đá, phương tiện thi công ngoài phạm vi thi công gây cản trở giao thông;
c) Không thu dọn ngay các biển báo hiệu, rào chắn, phương tiện, vật dụng thi công, các vật liệu tại phần đất của đường bộ, hành lang an toàn đường bộ theo nguyên trạng khi thi công xong.

### Điều khoản được nguồn trên dẫn chiếu tới (ND336-2025/D8/K1)
Mã điều khoản dùng được cho gold_units: ND336-2025/D8/K1

Điều 8. Xử phạt các hành vi vi phạm quy định về thi công trong phạm vi bảo vệ kết cấu hạ tầng đường bộ
1. Phạt tiền từ 1.000.000 đồng đến 3.000.000 đồng đối với cá nhân, từ 2.000.000 đồng đến 6.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:

### Điều khoản được nguồn trên dẫn chiếu tới (ND336-2025/D8/K3/a)
Mã điều khoản dùng được cho gold_units: ND336-2025/D8/K3/a

Điều 8. Xử phạt các hành vi vi phạm quy định về thi công trong phạm vi bảo vệ kết cấu hạ tầng đường bộ
3. Phạt tiền từ 5.000.000 đồng đến 7.000.000 đồng đối với cá nhân, từ 10.000.000 đồng đến 14.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
a) Thi công trên đường bộ đang khai thác không thực hiện đúng, đầy đủ biện pháp tổ chức giao thông để xảy ra ùn tắc giao thông;

### Điều khoản được nguồn trên dẫn chiếu tới (ND336-2025/D8/K3/b)
Mã điều khoản dùng được cho gold_units: ND336-2025/D8/K3/b

Điều 8. Xử phạt các hành vi vi phạm quy định về thi công trong phạm vi bảo vệ kết cấu hạ tầng đường bộ
3. Phạt tiền từ 5.000.000 đồng đến 7.000.000 đồng đối với cá nhân, từ 10.000.000 đồng đến 14.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
b) Không bố trí người cảnh báo, hướng dẫn giao thông khi thi công công trình trên đường bộ đang khai thác theo quy định;

[0] 3.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D8/K2)
[1] 5.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D8/K2)
[2] 6.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D8/K2)
[3] 10.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D8/K2)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi mới học lái xe, khi tham gia công trường xây dựng đường, nếu không thực hiện đúng biện pháp tổ chức giao thông, tôi sẽ bị phạt tiền bao nhiêu?
- Đáp: Bạn sẽ bị phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng. (Điều 8, Khoản 2 Nghị định 336/2025/NĐ-CP)
- ⚠ chep_nguyen_van: “biện pháp tổ chức giao thông …”

```json
{"qid": "tD-muc_phat-036", "question": "Tôi mới học lái xe, khi tham gia công trường xây dựng đường, nếu không thực hiện đúng biện pháp tổ chức giao thông, tôi sẽ bị phạt tiền bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "B", "answer": "Bạn sẽ bị phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng. (Điều 8, Khoản 2 Nghị định 336/2025/NĐ-CP)", "gold_units": ["ND336-2025/D8/K2"], "required_numbers": [{"value": 3000000, "unit": "vnd"}, {"value": 5000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-036:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Nếu tôi là một công ty xây dựng và không bố trí người cảnh báo khi thi công trên đường đang khai thác, mức phạt tiền sẽ là bao nhiêu?
- Đáp: Công ty sẽ bị phạt tiền từ 10.000.000 đồng đến 14.000.000 đồng. (Điều 8, Khoản 3b Nghị định 336/2025/NĐ-CP)
- ⚠ chep_nguyen_van: “không bố trí người cảnh báo …”

```json
{"qid": "tD-muc_phat-036", "question": "Nếu tôi là một công ty xây dựng và không bố trí người cảnh báo khi thi công trên đường đang khai thác, mức phạt tiền sẽ là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "B", "answer": "Công ty sẽ bị phạt tiền từ 10.000.000 đồng đến 14.000.000 đồng. (Điều 8, Khoản 3b Nghị định 336/2025/NĐ-CP)", "gold_units": ["ND336-2025/D8/K3/b"], "required_numbers": [{"value": 6000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-036:2"}
```

### WD-muc_phat-037 · tier B · vai: chủ doanh nghiệp vận tải · kiểu: tinh_huong_ban_than

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)
Hiệu lực của trạng thái này: 2026-03-01 → nay
Mã điều khoản dùng được cho gold_units: ND336-2025/D10/K5, ND336-2025/D10/K5/a, ND336-2025/D10/K5/b, ND336-2025/D10/K5/c, ND336-2025/D10/K5/d, ND336-2025/D10/K5/đ, ND336-2025/D10/K5/e, ND336-2025/D10/K5/g, ND336-2025/D10/K5/h, ND336-2025/D10/K5/i, ND336-2025/D10/K5/k, ND336-2025/D10/K5/l, ND336-2025/D10/K5/m

Điều 10. Xử phạt các hành vi vi phạm về thanh toán điện tử giao thông đường bộ, hoạt động trạm thu phí đường bộ
5. Phạt tiền từ 50.000.000 đồng đến 70.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
a) Không thực hiện đúng quy trình quản lý, vận hành trạm thu phí theo quy định để số lượng xe ô tô xếp hàng chờ trước trạm thu phí trên một làn xe (tính từ cabin thu phí đến xe cuối cùng của hàng xe chờ) từ 750 m trở lên;
b) Không thực hiện đúng quy trình quản lý, vận hành trạm thu phí theo quy định để thời gian đi qua trạm thu phí của một xe ô tô bất kỳ kể từ lúc dừng xe chờ thu phí đến lúc ra khỏi trạm thu phí lớn hơn 15 phút;
c) Không thực hiện đúng quy trình quản lý, vận hành trạm thu phí theo quy định để xảy ra tai nạn giao thông đối với các phương tiện khi phương tiện tham gia giao thông qua trạm thu phí gây hậu quả từ mức nghiêm trọng trở lên;
d) Không xây dựng hoặc xây dựng không đầy đủ quy trình nghiệp vụ quy định thời gian bù trừ, thanh toán, việc tra soát, đối chiếu dữ liệu;
đ) Không thực hiện các quy trình nghiệp vụ do nhà cung cấp dịch vụ thanh toán điện tử giao thông ban hành;
e) Không thực hiện quy trình đối soát; không khắc phục, điều chỉnh các lỗi, sai số phát hiện được thông qua quá trình đối soát;
g) Không thực hiện nhiệm vụ đối soát số liệu thu phí giữa lưu lượng phương tiện thực tế lưu thông với lưu lượng phương tiện thực hiện thu phí của nhà cung cấp dịch vụ thanh toán tiền sử dụng đường bộ theo quy định;
…

[0] 50.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D10/K5)
[1] 70.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D10/K5)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là chủ doanh nghiệp vận tải, trạm thu phí của công ty tôi thường có hàng xe chờ dài hơn 750 mét. Nếu trạm không thực hiện đúng quy trình quản lý, tôi sẽ bị phạt tiền bao nhiêu?
- Đáp: Bạn sẽ bị phạt tiền từ 50.000.000 đồng đến 70.000.000 đồng. (Điều 10, khoản 5, điểm a Nghị định 336/2025/NĐ-CP)
- ⚠ chep_nguyen_van: “hiện đúng quy trình quản lý …”
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-muc_phat-037", "question": "Tôi là chủ doanh nghiệp vận tải, trạm thu phí của công ty tôi thường có hàng xe chờ dài hơn 750 mét. Nếu trạm không thực hiện đúng quy trình quản lý, tôi sẽ bị phạt tiền bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "B", "answer": "Bạn sẽ bị phạt tiền từ 50.000.000 đồng đến 70.000.000 đồng. (Điều 10, khoản 5, điểm a Nghị định 336/2025/NĐ-CP)", "gold_units": ["ND336-2025/D10/K5"], "required_numbers": [{"value": 50000000, "unit": "vnd"}, {"value": 70000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-037:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là chủ doanh nghiệp vận tải, khi xe khách dừng chờ thu phí, thời gian chờ vượt quá 15 phút. Nếu trạm không thực hiện đúng quy trình, mức phạt tiền sẽ là bao nhiêu?
- Đáp: Bạn sẽ bị phạt tiền từ 50.000.000 đồng đến 70.000.000 đồng. (Điều 10, khoản 5, điểm b Nghị định 336/2025/NĐ-CP)
- ⚠ chep_nguyen_van: “không thực hiện đúng quy trình …”
- Ghi chú: Không có giả định đặc biệt

```json
{"qid": "tD-muc_phat-037", "question": "Tôi là chủ doanh nghiệp vận tải, khi xe khách dừng chờ thu phí, thời gian chờ vượt quá 15 phút. Nếu trạm không thực hiện đúng quy trình, mức phạt tiền sẽ là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "B", "answer": "Bạn sẽ bị phạt tiền từ 50.000.000 đồng đến 70.000.000 đồng. (Điều 10, khoản 5, điểm b Nghị định 336/2025/NĐ-CP)", "gold_units": ["ND336-2025/D10/K5"], "required_numbers": [{"value": 50000000, "unit": "vnd"}, {"value": 70000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-037:2"}
```

### WD-muc_phat-038 · tier B · vai: tài xế xe tải · kiểu: tinh_huong_ban_than

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)
Hiệu lực của trạng thái này: 2026-03-01 → nay
Mã điều khoản dùng được cho gold_units: ND336-2025/D12/K6, ND336-2025/D12/K6/a, ND336-2025/D12/K6/b, ND336-2025/D12/K6/c, ND336-2025/D12/K6/d, ND336-2025/D12/K6/đ, ND336-2025/D12/K6/e, ND336-2025/D12/K6/g, ND336-2025/D12/K6/h, ND336-2025/D12/K6/i, ND336-2025/D12/K6/k, ND336-2025/D12/K6/l

Điều 12. Xử phạt các hành vi vi phạm quy định về vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
6. Phạt tiền từ 12.000.000 đồng đến 16.000.000 đồng đối với cá nhân, từ 24.000.000 đồng đến 32.000.000 đồng đối với tổ chức kinh doanh vận tải, dịch vụ hỗ trợ vận tải thực hiện một trong các hành vi vi phạm sau đây:
a) Kinh doanh vận tải bằng xe ô tô, xe bốn bánh có gắn động cơ mà không có giấy phép kinh doanh vận tải theo quy định, trừ hành vi quy định tại điểm i khoản này;
b) Thực hiện không đúng hình thức kinh doanh đã đăng ký trong giấy phép kinh doanh vận tải;
c) Thành lập, tổ chức điểm giao dịch đón, trả khách, bốc dỡ hàng hóa trái phép;
d) Không xây dựng quy trình đảm bảo an toàn giao thông cho xe ra, vào bến hoặc có xây dựng nhưng thực hiện không đúng, không đầy đủ quy trình đảm bảo an toàn giao thông cho xe ra, vào bến; không niêm yết hoặc niêm yết không đầy đủ, chính xác các thông tin tại bến xe theo quy định;
đ) Không gửi hóa đơn điện tử, không gửi nội dung tối thiểu của hợp đồng điện tử theo quy định;
e) Không thực hiện hoặc thực hiện không đầy đủ, không đúng quy định về quản lý, áp dụng thông tin từ phần mềm quản lý bến xe khách;
g) Sử dụng hợp đồng điện tử không có giao diện phần mềm cung cấp cho hành khách hoặc người thuê vận tải theo quy định hoặc có nhưng giao diện không bảo đảm các yêu cầu theo quy định;
…

### Điều khoản nêu chế tài áp cho hành vi trên (ND336-2025/D12/K8/b)
Mã điều khoản dùng được cho gold_units: ND336-2025/D12/K8/b

Điều 12. Xử phạt các hành vi vi phạm quy định về vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
8. Ngoài việc bị phạt tiền, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị áp dụng các hình thức xử phạt bổ sung sau đây:
b) Thực hiện hành vi vi phạm quy định tại điểm b khoản 3; điểm b khoản 4; điểm b, điểm h khoản 6 Điều này bị tước quyền sử dụng giấy phép kinh doanh vận tải từ 01 tháng đến 03 tháng.

[0] 12.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D12/K6)
[1] 16.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D12/K6)
[2] 24.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D12/K6)
[3] 32.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D12/K6)
[4] 01 tháng (thời hạn tước quyền sử dụng tối thiểu, nêu tại ND336-2025/D12/K8/b)
[5] 03 tháng (thời hạn tước quyền sử dụng tối đa, nêu tại ND336-2025/D12/K8/b)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là tài xế xe tải, nhưng lại không có giấy phép kinh doanh vận tải khi đưa hàng đi. Mức phạt tiền mà tôi phải chịu là bao nhiêu?
- Đáp: Bạn sẽ bị phạt tiền từ 12.000.000 đồng đến 16.000.000 đồng. (Điều 12, khoản 6, Nghị định 336/2025/NĐ-CP)
- ⚠ chep_nguyen_van: “có giấy phép kinh doanh vận …”

```json
{"qid": "tD-muc_phat-038", "question": "Tôi là tài xế xe tải, nhưng lại không có giấy phép kinh doanh vận tải khi đưa hàng đi. Mức phạt tiền mà tôi phải chịu là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "B", "answer": "Bạn sẽ bị phạt tiền từ 12.000.000 đồng đến 16.000.000 đồng. (Điều 12, khoản 6, Nghị định 336/2025/NĐ-CP)", "gold_units": ["ND336-2025/D12/K6"], "required_numbers": [{"value": 12000000, "unit": "vnd"}, {"value": 16000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-038:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là tài xế xe tải, nhưng lại không xây dựng quy trình đảm bảo an toàn giao thông khi xe ra vào bến, và không ghi đầy đủ thông tin tại bến. Tôi sẽ bị phạt tiền và mất giấy phép như thế nào?
- Đáp: Bạn sẽ bị phạt tiền từ 12.000.000 đồng đến 16.000.000 đồng và bị tước quyền sử dụng giấy phép kinh doanh vận tải trong thời hạn từ 01 tháng đến 03 tháng. (Điều 12, khoản 6 và khoản 8, điểm b, Nghị định 336/2025/NĐ-CP)
- ⚠ chep_nguyen_van: “dựng quy trình đảm bảo an …”

```json
{"qid": "tD-muc_phat-038", "question": "Tôi là tài xế xe tải, nhưng lại không xây dựng quy trình đảm bảo an toàn giao thông khi xe ra vào bến, và không ghi đầy đủ thông tin tại bến. Tôi sẽ bị phạt tiền và mất giấy phép như thế nào?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "B", "answer": "Bạn sẽ bị phạt tiền từ 12.000.000 đồng đến 16.000.000 đồng và bị tước quyền sử dụng giấy phép kinh doanh vận tải trong thời hạn từ 01 tháng đến 03 tháng. (Điều 12, khoản 6 và khoản 8, điểm b, Nghị định 336/2025/NĐ-CP)", "gold_units": ["ND336-2025/D12/K6", "ND336-2025/D12/K8/b"], "required_numbers": [{"value": 12000000, "unit": "vnd"}, {"value": 16000000, "unit": "vnd"}, {"value": 1, "unit": "thang"}, {"value": 3, "unit": "thang"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-038:2"}
```

### WD-muc_phat-039 · tier B · vai: sinh viên đi xe máy · kiểu: tinh_huong_ban_than

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)
Hiệu lực của trạng thái này: 2026-03-01 → nay
Mã điều khoản dùng được cho gold_units: ND336-2025/D6/K1

Điều 6. Xử phạt hành vi vi phạm quy định về quản lý, vận hành, khai thác, bảo trì công trình hạ tầng kỹ thuật sử dụng chung với đường bộ
1. Phạt tiền từ 6.000.000 đồng đến 10.000.000 đồng đối với cá nhân, từ 12.000.000 đồng đến 20.000.000 đồng đối với tổ chức thực hiện hành vi vi phạm không bố trí dấu hiệu nhận biết công trình hạ tầng thuộc sở hữu khi lắp đặt vào công trình hạ tầng kỹ thuật sử dụng chung với đường bộ.

[0] 6.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D6/K1)
[1] 10.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D6/K1)
[2] 12.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D6/K1)
[3] 20.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D6/K1)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi vừa lắp một biển báo mới trên một công trình hạ tầng kỹ thuật chung với đường bộ nhưng quên đặt dấu hiệu nhận biết công trình, tôi sẽ bị phạt tiền bao nhiêu?
- Đáp: Bạn sẽ bị phạt tiền từ 6.000.000 đồng đến 10.000.000 đồng. (Điều 6, Nghị định 336/2025/NĐ-CP)
- ⚠ chep_nguyen_van: “công trình hạ tầng kỹ thuật …”
- Ghi chú: đi xe máy

```json
{"qid": "tD-muc_phat-039", "question": "Tôi vừa lắp một biển báo mới trên một công trình hạ tầng kỹ thuật chung với đường bộ nhưng quên đặt dấu hiệu nhận biết công trình, tôi sẽ bị phạt tiền bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "B", "answer": "Bạn sẽ bị phạt tiền từ 6.000.000 đồng đến 10.000.000 đồng. (Điều 6, Nghị định 336/2025/NĐ-CP)", "gold_units": ["ND336-2025/D6/K1"], "required_numbers": [{"value": 6000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-039:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Công ty tôi vừa lắp một biển báo mới trên công trình hạ tầng kỹ thuật chung với đường bộ mà không đặt dấu hiệu nhận biết, mức phạt tiền sẽ là bao nhiêu?
- Đáp: Bạn sẽ bị phạt tiền từ 6.000.000 đồng đến 10.000.000 đồng. (Điều 6, Nghị định 336/2025/NĐ-CP)
- ⚠ chep_nguyen_van: “công trình hạ tầng kỹ thuật …”
- Ghi chú: đi xe máy

```json
{"qid": "tD-muc_phat-039", "question": "Công ty tôi vừa lắp một biển báo mới trên công trình hạ tầng kỹ thuật chung với đường bộ mà không đặt dấu hiệu nhận biết, mức phạt tiền sẽ là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "B", "answer": "Bạn sẽ bị phạt tiền từ 6.000.000 đồng đến 10.000.000 đồng. (Điều 6, Nghị định 336/2025/NĐ-CP)", "gold_units": ["ND336-2025/D6/K1"], "required_numbers": [{"value": 6000000, "unit": "vnd"}, {"value": 10000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-039:2"}
```

### WD-muc_phat-040 · tier B · vai: tài xế công nghệ · kiểu: tinh_huong_ban_than

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 336/2025/NĐ-CP (Quy định xử phạt vi phạm hành chính trong hoạt động đường bộ)
Hiệu lực của trạng thái này: 2026-03-01 → nay
Mã điều khoản dùng được cho gold_units: ND336-2025/D7/K4

Điều 7. Xử phạt hành vi vi phạm quy định về đào tạo thẩm tra viên, điều kiện kinh doanh dịch vụ thẩm tra an toàn giao thông đường bộ
4. Phạt tiền từ 30.000.000 đồng đến 40.000.000 đồng đối với tổ chức kinh doanh dịch vụ thẩm tra an toàn giao thông đường bộ thực hiện hành vi vi phạm không đáp ứng điều kiện về năng lực khi thẩm tra đối với dự án quan trọng quốc gia, dự án nhóm A, nhóm B theo quy định.

### Điều khoản nêu chế tài áp cho hành vi trên (ND336-2025/D7/K5/b)
Mã điều khoản dùng được cho gold_units: ND336-2025/D7/K5/b

Điều 7. Xử phạt hành vi vi phạm quy định về đào tạo thẩm tra viên, điều kiện kinh doanh dịch vụ thẩm tra an toàn giao thông đường bộ
5. Ngoài việc bị phạt tiền, tổ chức thực hiện hành vi vi phạm còn bị áp dụng hình thức xử phạt bổ sung:
b) Tổ chức kinh doanh dịch vụ thẩm tra an toàn giao thông đường bộ thực hiện hành vi vi phạm quy định tại khoản 3, khoản 4 Điều này còn bị đình chỉ hoạt động thẩm tra an toàn giao thông đường bộ từ 01 tháng đến 03 tháng.

[0] 30.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND336-2025/D7/K4)
[1] 40.000.000 đồng (mức phạt tiền tối đa, nêu tại ND336-2025/D7/K4)
[2] 01 tháng (thời hạn đình chỉ tối thiểu, nêu tại ND336-2025/D7/K5/b)
[3] 03 tháng (thời hạn đình chỉ tối đa, nêu tại ND336-2025/D7/K5/b)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi điều hành một công ty cung cấp dịch vụ thẩm tra an toàn giao thông, nhưng chúng tôi không đáp ứng đủ năng lực khi thẩm tra một dự án quan trọng quốc gia. Mức phạt tiền và thời gian đình chỉ hoạt động sẽ là bao nhiêu?
- Đáp: Bạn sẽ bị phạt tiền từ 30.000.000 đồng đến 40.000.000 đồng và bị đình chỉ hoạt động thẩm tra an toàn giao thông từ 01 tháng đến 03 tháng.
- ⚠ chep_nguyen_van: “dịch vụ thẩm tra an toàn …”

```json
{"qid": "tD-muc_phat-040", "question": "Tôi điều hành một công ty cung cấp dịch vụ thẩm tra an toàn giao thông, nhưng chúng tôi không đáp ứng đủ năng lực khi thẩm tra một dự án quan trọng quốc gia. Mức phạt tiền và thời gian đình chỉ hoạt động sẽ là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "B", "answer": "Bạn sẽ bị phạt tiền từ 30.000.000 đồng đến 40.000.000 đồng và bị đình chỉ hoạt động thẩm tra an toàn giao thông từ 01 tháng đến 03 tháng.", "gold_units": ["ND336-2025/D7/K4", "ND336-2025/D7/K5/b"], "required_numbers": [{"value": 30000000, "unit": "vnd"}, {"value": 40000000, "unit": "vnd"}, {"value": 1, "unit": "thang"}, {"value": 3, "unit": "thang"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-040:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là chủ doanh nghiệp thẩm tra an toàn giao thông, và chúng tôi đã thực hiện thẩm tra một dự án nhóm A mà không đáp ứng điều kiện năng lực. Tôi cần biết mức phạt tiền và thời hạn đình chỉ hoạt động là bao nhiêu?
- Đáp: Bạn sẽ bị phạt tiền từ 30.000.000 đồng đến 40.000.000 đồng và bị đình chỉ hoạt động thẩm tra an toàn giao thông từ 01 tháng đến 03 tháng.
- ⚠ chep_nguyen_van: “thẩm tra an toàn giao thông …”

```json
{"qid": "tD-muc_phat-040", "question": "Tôi là chủ doanh nghiệp thẩm tra an toàn giao thông, và chúng tôi đã thực hiện thẩm tra một dự án nhóm A mà không đáp ứng điều kiện năng lực. Tôi cần biết mức phạt tiền và thời hạn đình chỉ hoạt động là bao nhiêu?", "as_of": "2026-11-03", "question_type": "muc_phat", "tier": "B", "answer": "Bạn sẽ bị phạt tiền từ 30.000.000 đồng đến 40.000.000 đồng và bị đình chỉ hoạt động thẩm tra an toàn giao thông từ 01 tháng đến 03 tháng.", "gold_units": ["ND336-2025/D7/K4", "ND336-2025/D7/K5/b"], "required_numbers": [{"value": 30000000, "unit": "vnd"}, {"value": 40000000, "unit": "vnd"}, {"value": 1, "unit": "thang"}, {"value": 3, "unit": "thang"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-muc_phat-040:2"}
```

## tru_diem — số điểm bị trừ trên giấy phép lái xe

### WD-tru_diem-001 · tier A · vai: chủ doanh nghiệp vận tải · kiểu: tinh_huong_nguoi_khac

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D14/K2, ND168-2024/D14/K2/a, ND168-2024/D14/K2/b, ND168-2024/D14/K2/c, ND168-2024/D14/K2/d, ND168-2024/D14/K2/đ

Điều 14. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy vi phạm quy định về điều kiện của phương tiện khi tham gia giao thông
2. Phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
a) Điều khiển xe không có chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe) hoặc sử dụng chứng nhận đăng ký xe (hoặc bản sao chứng nhận đăng ký xe có chứng thực kèm theo bản gốc giấy biên nhận của tổ chức tín dụng, chi nhánh ngân hàng nước ngoài trong trường hợp tổ chức tín dụng, chi nhánh ngân hàng nước ngoài giữ bản gốc chứng nhận đăng ký xe) đã hết hạn sử dụng, hết hiệu lực;
…

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D14/K8/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D14/K8/a

Điều 14. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe mô tô, xe gắn máy, các loại xe tương tự xe mô tô và các loại xe tương tự xe gắn máy vi phạm quy định về điều kiện của phương tiện khi tham gia giao thông
8. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển xe thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
a) Thực hiện hành vi quy định tại điểm a, điểm b, điểm c khoản 2 Điều này bị trừ điểm giấy phép lái xe 02 điểm;

[0] 2.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D14/K2)
[1] 3.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D14/K2)
[2] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D14/K8/a)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Công ty tôi vừa nhận được một báo cáo rằng một lái xe của chúng tôi đã lái xe máy mà không có giấy đăng ký hợp lệ, và tôi muốn biết số điểm bị trừ trên giấy phép lái xe của người đó.
- Đáp: Người lái xe bị trừ 02 điểm. (Điều 14, Khoản 8, Nghị định 168/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “giấy phép lái xe của người …”
- Ghi chú: Điểm trừ áp dụng cho người điều khiển xe máy, xe gắn máy.

```json
{"qid": "tD-tru_diem-001", "question": "Công ty tôi vừa nhận được một báo cáo rằng một lái xe của chúng tôi đã lái xe máy mà không có giấy đăng ký hợp lệ, và tôi muốn biết số điểm bị trừ trên giấy phép lái xe của người đó.", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Người lái xe bị trừ 02 điểm. (Điều 14, Khoản 8, Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D14/K8/a"], "required_numbers": [{"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-001:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Công ty tôi đang xem xét một trường hợp khi một lái xe của đối tác đã lái xe máy mà không có chứng nhận đăng ký hợp lệ, tôi muốn biết số điểm bị trừ trên giấy phép lái xe của người đó.
- Đáp: Người lái xe bị trừ 02 điểm. (Điều 14, Khoản 8, Nghị định 168/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “giấy phép lái xe của người …”
- Ghi chú: Điểm trừ áp dụng cho người điều khiển xe máy, xe gắn máy.

```json
{"qid": "tD-tru_diem-001", "question": "Công ty tôi đang xem xét một trường hợp khi một lái xe của đối tác đã lái xe máy mà không có chứng nhận đăng ký hợp lệ, tôi muốn biết số điểm bị trừ trên giấy phép lái xe của người đó.", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Người lái xe bị trừ 02 điểm. (Điều 14, Khoản 8, Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D14/K8/a"], "required_numbers": [{"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-001:2"}
```

### WD-tru_diem-002 · tier A · vai: cán bộ phường · kiểu: tinh_huong_ban_than

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D23/K3

Điều 23. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển hàng hóa nguy hiểm
3. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng đối với hành vi vận chuyển hàng nguy hiểm mà xe ô tô không dán nhãn, biểu trưng nhận diện hàng hóa nguy hiểm; xe ô tô không lắp đèn hoặc tín hiệu cảnh báo theo quy định.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D23/K7/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D23/K7/a

Điều 23. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển hàng hóa nguy hiểm
7. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
a) Thực hiện hành vi quy định tại khoản 3, khoản 4 Điều này bị trừ điểm giấy phép lái xe 02 điểm;

[0] 4.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D23/K3)
[1] 6.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D23/K3)
[2] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D23/K7/a)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi vừa giao hàng hóa nguy hiểm bằng ô tô mà không dán nhãn, không lắp đèn cảnh báo, và muốn biết số điểm giấy phép sẽ bị trừ khi bị xử phạt?
- Đáp: Bạn sẽ bị trừ 02 điểm trên giấy phép lái xe. (Điều 23 Khoản 7(a) Nghị định 168/2024/NĐ-CP)

```json
{"qid": "tD-tru_diem-002", "question": "Tôi vừa giao hàng hóa nguy hiểm bằng ô tô mà không dán nhãn, không lắp đèn cảnh báo, và muốn biết số điểm giấy phép sẽ bị trừ khi bị xử phạt?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Bạn sẽ bị trừ 02 điểm trên giấy phép lái xe. (Điều 23 Khoản 7(a) Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D23/K7/a"], "required_numbers": [{"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-002:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Khi tôi vận chuyển hàng hóa nguy hiểm bằng ô tô mà không dán nhãn và không lắp đèn cảnh báo, tôi cần biết số điểm bị trừ trên giấy phép lái xe là bao nhiêu?
- Đáp: Bạn sẽ bị trừ 02 điểm trên giấy phép lái xe. (Điều 23 Khoản 7(a) Nghị định 168/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “vận chuyển hàng hóa nguy hiểm …”

```json
{"qid": "tD-tru_diem-002", "question": "Khi tôi vận chuyển hàng hóa nguy hiểm bằng ô tô mà không dán nhãn và không lắp đèn cảnh báo, tôi cần biết số điểm bị trừ trên giấy phép lái xe là bao nhiêu?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Bạn sẽ bị trừ 02 điểm trên giấy phép lái xe. (Điều 23 Khoản 7(a) Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D23/K7/a"], "required_numbers": [{"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-002:2"}
```

### WD-tru_diem-003 · tier A · vai: người lớn tuổi đi xe đạp điện · kiểu: tinh_huong_ban_than

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K6

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
6. Phạt tiền từ 2.000.000 đồng đến 4.000.000 đồng trên mỗi người vượt quá quy định được phép chở của phương tiện nhưng tổng mức phạt tiền tối đa không vượt quá 75.000.000 đồng đối với chủ phương tiện là cá nhân, từ 4.000.000 đồng đến 8.000.000 đồng trên mỗi người vượt quá quy định được phép chở của phương tiện nhưng tổng mức phạt tiền tối đa không vượt quá 150.000.000 đồng đối với chủ phương tiện là tổ chức giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại khoản 4 Điều 20 của Nghị định này hoặc trực tiếp điều khiển phương tiện thực hiện hành vi vi phạm quy định tại khoản 4 Điều 20 của Nghị định này.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K18/đ)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K18/đ

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
18. Ngoài việc bị phạt tiền, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị áp dụng các hình thức xử phạt bổ sung như sau:
đ) Thực hiện hành vi quy định tại khoản 5, khoản 6 Điều này trong trường hợp chở vượt trên 50% số người quy định được phép chở của phương tiện còn bị tước quyền sử dụng phù hiệu từ 01 tháng đến 03 tháng (nếu có). Thực hiện hành vi quy định tại điểm a, điểm b khoản 11; điểm a, điểm b, điểm c, điểm đ khoản 13; điểm a, điểm b, điểm c, điểm d, điểm đ, điểm e, điểm g khoản 14; khoản 15; khoản 16 Điều này còn bị tước quyền sử dụng phù hiệu từ 01 tháng đến 03 tháng (nếu có),

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K21/d)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K21/d

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
21. Ngoài việc bị áp dụng hình thức xử phạt, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
d) Thực hiện hành vi quy định tại khoản 5, khoản 6 Điều này trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện chở vượt trên 50% đến 100% số người quy định được phép chở của phương tiện, còn bị trừ điểm giấy phép lái xe 04 điểm;

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K21/h)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K21/h

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
21. Ngoài việc bị áp dụng hình thức xử phạt, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
h) Thực hiện hành vi quy định tại khoản 5, khoản 6 Điều này trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện chở vượt trên 100% số người quy định được phép chở của phương tiện còn bị trừ điểm giấy phép lái xe 10 điểm.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D20/K4)
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K4

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
4. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng trên mỗi người vượt quá quy định được phép chở của phương tiện nhưng tổng mức phạt tiền tối đa không vượt quá 75.000.000 đồng đối với người điều khiển xe ô tô chở hành khách (kinh doanh vận tải hành khách theo tuyến cố định, hợp đồng) chạy tuyến có cự ly lớn hơn 300 km thực hiện hành vi vi phạm chở quá số người quy định được phép chở của phương tiện.

[0] 01 tháng (thời hạn tước quyền sử dụng tối thiểu, nêu tại ND168-2024/D32/K18/đ)
[1] 03 tháng (thời hạn tước quyền sử dụng tối đa, nêu tại ND168-2024/D32/K18/đ)
[2] 2.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D32/K6)
[3] 4.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D32/K6)
[4] 04 điểm (số điểm bị trừ, nêu tại ND168-2024/D32/K21/d)
[5] 10 điểm (số điểm bị trừ, nêu tại ND168-2024/D32/K21/h)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi đang lái xe máy điện và đã mang 3 người cùng đi, có bị trừ điểm không?
- Đáp: Bạn sẽ bị trừ 04 điểm. (khoản d Điều 21 Điều 32 Nghị định 168/2024/NĐ-CP)

```json
{"qid": "tD-tru_diem-003", "question": "Tôi đang lái xe máy điện và đã mang 3 người cùng đi, có bị trừ điểm không?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Bạn sẽ bị trừ 04 điểm. (khoản d Điều 21 Điều 32 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D32/K21/d"], "required_numbers": [{"value": 4, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-003:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi lái ô tô chở 5 hành khách, có bị trừ điểm không?
- Đáp: Bạn sẽ bị trừ 04 điểm. (khoản d Điều 21 Điều 32 Nghị định 168/2024/NĐ-CP)

```json
{"qid": "tD-tru_diem-003", "question": "Tôi lái ô tô chở 5 hành khách, có bị trừ điểm không?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Bạn sẽ bị trừ 04 điểm. (khoản d Điều 21 Điều 32 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D32/K21/d"], "required_numbers": [{"value": 4, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-003:2"}
```

### WD-tru_diem-004 · tier A · vai: tài xế công nghệ · kiểu: ngan

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K2

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
2. Phạt tiền từ 400.000 đồng đến 600.000 đồng trên mỗi người vượt quá quy định được phép chở của phương tiện nhưng tổng mức phạt tiền tối đa không vượt quá 75.000.000 đồng đối với người điều khiển xe ô tô chở hành khách, ô tô chở người (trừ xe buýt) thực hiện hành vi vi phạm chở quá số người quy định được phép chở của phương tiện, trừ các hành vi vi phạm quy định tại khoản 4 Điều này.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D20/K10/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K10/b

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
10. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
b) Thực hiện hành vi quy định tại khoản 2, khoản 4 (trường hợp vượt trên 50% đến 100% số người quy định được phép chở của phương tiện) Điều này bị trừ điểm giấy phép lái xe 04 điểm;

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D20/K10/d)
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K10/d

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
10. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
d) Thực hiện hành vi quy định tại khoản 2, khoản 4 (trường hợp vượt trên 100% số người quy định được phép chở của phương tiện) Điều này bị trừ điểm giấy phép lái xe 10 điểm.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D20/K4)
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K4

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
4. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng trên mỗi người vượt quá quy định được phép chở của phương tiện nhưng tổng mức phạt tiền tối đa không vượt quá 75.000.000 đồng đối với người điều khiển xe ô tô chở hành khách (kinh doanh vận tải hành khách theo tuyến cố định, hợp đồng) chạy tuyến có cự ly lớn hơn 300 km thực hiện hành vi vi phạm chở quá số người quy định được phép chở của phương tiện.

[0] 400.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D20/K2)
[1] 600.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D20/K2)
[2] 04 điểm (số điểm bị trừ, nêu tại ND168-2024/D20/K10/b)
[3] 10 điểm (số điểm bị trừ, nêu tại ND168-2024/D20/K10/d)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi lái xe ô tô chở khách, có 12 người trên xe, giới hạn 8 người. Tôi bị trừ bao nhiêu điểm giấy phép?
- Đáp: Bạn sẽ bị trừ 04 điểm giấy phép lái xe. Điều này được quy định trong Điều 20, khoản 10, điểm b của Nghị định 168/2024/NĐ-CP.

```json
{"qid": "tD-tru_diem-004", "question": "Tôi lái xe ô tô chở khách, có 12 người trên xe, giới hạn 8 người. Tôi bị trừ bao nhiêu điểm giấy phép?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Bạn sẽ bị trừ 04 điểm giấy phép lái xe. Điều này được quy định trong Điều 20, khoản 10, điểm b của Nghị định 168/2024/NĐ-CP.", "gold_units": ["ND168-2024/D20/K10/b"], "required_numbers": [{"value": 4, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-004:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi lái xe ô tô chở khách, có 20 người trên xe, giới hạn 8 người. Tôi bị trừ bao nhiêu điểm giấy phép?
- Đáp: Bạn sẽ bị trừ 10 điểm giấy phép lái xe. Điều này được quy định trong Điều 20, khoản 10, điểm d của Nghị định 168/2024/NĐ-CP.

```json
{"qid": "tD-tru_diem-004", "question": "Tôi lái xe ô tô chở khách, có 20 người trên xe, giới hạn 8 người. Tôi bị trừ bao nhiêu điểm giấy phép?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Bạn sẽ bị trừ 10 điểm giấy phép lái xe. Điều này được quy định trong Điều 20, khoản 10, điểm d của Nghị định 168/2024/NĐ-CP.", "gold_units": ["ND168-2024/D20/K10/d"], "required_numbers": [{"value": 10, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-004:2"}
```

### WD-tru_diem-005 · tier A · vai: cán bộ phường · kiểu: ngan

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K16, ND168-2024/D32/K16/a, ND168-2024/D32/K16/b, ND168-2024/D32/K16/c

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
16. Phạt tiền từ 65.000.000 đồng đến 75.000.000 đồng đối với cá nhân, từ 130.000.000 đồng đến 150.000.000 đồng đối với tổ chức là chủ xe ô tô, xe máy chuyên dùng và các loại xe tương tự xe ô tô khi thực hiện một trong các hành vi vi phạm sau đây:
a) Giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm a khoản 5 Điều 34 của Nghị định này hoặc trực tiếp điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm a khoản 5 Điều 34 của Nghị định này;
b) Giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm a, điểm b khoản 8 Điều 21 của Nghị định này hoặc trực tiếp điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm a, điểm b khoản 8 Điều 21 của Nghị định này;
c) Tự ý thay đổi tổng thành khung, tổng thành máy (động cơ), hệ thống phanh, hệ thống truyền động (truyền lực), hệ thống chuyển động hoặc tự ý cải tạo kết cấu, hình dáng, kích thước của xe không đúng thiết kế của nhà sản xuất hoặc thiết kế trong hồ sơ đã nộp cho cơ quan đăng ký xe hoặc thiết kế cải tạo đã được cơ quan có thẩm quyền phê duyệt; tự ý thay đổi tính năng sử dụng của xe hoặc tự ý lắp đặt thêm cơ cấu nâng hạ thùng xe, nâng hạ công-ten-nơ trên xe (kể cả rơ moóc và sơ mi rơ moóc).

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K18/c)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K18/c

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
18. Ngoài việc bị phạt tiền, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị áp dụng các hình thức xử phạt bổ sung như sau:
c) Thực hiện hành vi quy định tại điểm e khoản 7, điểm b khoản 11, điểm a khoản 13, khoản 15, điểm b khoản 16 Điều này mà phương tiện đó có thùng xe, khối lượng hàng hóa cho phép chuyên chở không đúng theo quy định hiện hành thì còn bị tước quyền sử dụng chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường và tem kiểm định của phương tiện từ 01 tháng đến 03 tháng;

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K18/d)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K18/d

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
18. Ngoài việc bị phạt tiền, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị áp dụng các hình thức xử phạt bổ sung như sau:
d) Thực hiện hành vi quy định tại điểm d khoản 11, điểm h khoản 14, điểm c khoản 16 Điều này bị tước quyền sử dụng chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường và tem kiểm định của phương tiện từ 01 tháng đến 03 tháng;

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K18/đ)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K18/đ

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
18. Ngoài việc bị phạt tiền, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị áp dụng các hình thức xử phạt bổ sung như sau:
đ) Thực hiện hành vi quy định tại khoản 5, khoản 6 Điều này trong trường hợp chở vượt trên 50% số người quy định được phép chở của phương tiện còn bị tước quyền sử dụng phù hiệu từ 01 tháng đến 03 tháng (nếu có). Thực hiện hành vi quy định tại điểm a, điểm b khoản 11; điểm a, điểm b, điểm c, điểm đ khoản 13; điểm a, điểm b, điểm c, điểm d, điểm đ, điểm e, điểm g khoản 14; khoản 15; khoản 16 Điều này còn bị tước quyền sử dụng phù hiệu từ 01 tháng đến 03 tháng (nếu có),

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K21/c)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K21/c

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
21. Ngoài việc bị áp dụng hình thức xử phạt, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
c) Thực hiện hành vi quy định tại điểm a, điểm b, điểm đ, điểm e khoản 13; điểm a, điểm b, điểm c, điểm d khoản 14; điểm a khoản 16 Điều này trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện còn bị trừ điểm giấy phép lái xe 04 điểm;

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K21/g)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K21/g

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
21. Ngoài việc bị áp dụng hình thức xử phạt, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
g) Thực hiện hành vi quy định tại điểm d khoản 13, điểm b khoản 16 Điều này trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện còn bị trừ điểm giấy phép lái xe 10 điểm;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D34/K5/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D34/K5/a

Điều 34. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển quá khổ giới hạn, xe quá tải trọng, xe bánh xích lưu hành đường bộ (kể cả xe ô tô chở hành khách)
5. Phạt tiền từ 40.000.000 đồng đến 50.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
a) Điều khiển xe mà tổng trọng lượng (khối lượng toàn bộ) của xe hoặc tải trọng trục xe (bao gồm cả hàng hóa xếp trên xe, người được chở trên xe) vượt quá tải trọng cho phép của đường bộ trên 50%, trừ trường hợp có giấy phép lưu hành còn giá trị sử dụng;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D21/K8/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K8/a

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
8. Phạt tiền từ 8.000.000 đồng đến 12.000.000 đồng đối với một trong các hành vi sau đây:
a) Điều khiển xe (kể cả rơ moóc và sơ mi rơ moóc) chở hàng vượt trọng tải (khối lượng hàng chuyên chở) cho phép tham gia giao thông được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe trên 150%;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D21/K8/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K8/b

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
8. Phạt tiền từ 8.000.000 đồng đến 12.000.000 đồng đối với một trong các hành vi sau đây:
b) Điều khiển xe kéo theo rơ moóc, sơ mi rơ moóc mà khối lượng toàn bộ (bao gồm khối lượng bản thân rơ moóc, sơ mi rơ moóc và khối lượng hàng chuyên chở) của rơ moóc, sơ mi rơ moóc vượt khối lượng cho phép kéo theo được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe trên 150%;

[0] 65.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D32/K16)
[1] 75.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D32/K16)
[2] 130.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D32/K16)
[3] 150.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D32/K16)
[4] 01 tháng (thời hạn tước quyền sử dụng tối thiểu, nêu tại ND168-2024/D32/K18/c)
[5] 03 tháng (thời hạn tước quyền sử dụng tối đa, nêu tại ND168-2024/D32/K18/c)
[6] 01 tháng (thời hạn tước quyền sử dụng tối thiểu, nêu tại ND168-2024/D32/K18/d)
[7] 03 tháng (thời hạn tước quyền sử dụng tối đa, nêu tại ND168-2024/D32/K18/d)
[8] 01 tháng (thời hạn tước quyền sử dụng tối thiểu, nêu tại ND168-2024/D32/K18/đ)
[9] 03 tháng (thời hạn tước quyền sử dụng tối đa, nêu tại ND168-2024/D32/K18/đ)
[10] 04 điểm (số điểm bị trừ, nêu tại ND168-2024/D32/K21/c)
[11] 10 điểm (số điểm bị trừ, nêu tại ND168-2024/D32/K21/g)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Nếu tôi điều khiển xe ô tô tải chở hàng vượt trọng tải, có bao nhiêu điểm bị trừ trên giấy phép lái xe?
- Đáp: Bạn sẽ bị trừ 04 điểm trên giấy phép lái xe. (khoản 3 Điều 32 Nghị định 168/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “điều khiển xe ô tô tải …”
- Ghi chú: Giả định là người điều khiển trực tiếp xe ô tô tải chở hàng vượt trọng tải

```json
{"qid": "tD-tru_diem-005", "question": "Nếu tôi điều khiển xe ô tô tải chở hàng vượt trọng tải, có bao nhiêu điểm bị trừ trên giấy phép lái xe?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Bạn sẽ bị trừ 04 điểm trên giấy phép lái xe. (khoản 3 Điều 32 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D32/K21/c"], "required_numbers": [{"value": 4, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-005:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Nếu tôi điều khiển xe ô tô tải chở hàng vượt trọng tải và đồng thời kéo rơ moóc vượt khối lượng cho phép, có bao nhiêu điểm bị trừ?
- Đáp: Bạn sẽ bị trừ 10 điểm trên giấy phép lái xe. (khoản 3 Điều 32 Nghị định 168/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “moóc vượt khối lượng cho phép …”
- Ghi chú: Giả định là người điều khiển trực tiếp xe ô tô tải chở hàng vượt trọng tải và kéo rơ moóc vượt khối lượng cho phép

```json
{"qid": "tD-tru_diem-005", "question": "Nếu tôi điều khiển xe ô tô tải chở hàng vượt trọng tải và đồng thời kéo rơ moóc vượt khối lượng cho phép, có bao nhiêu điểm bị trừ?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Bạn sẽ bị trừ 10 điểm trên giấy phép lái xe. (khoản 3 Điều 32 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D32/K21/g"], "required_numbers": [{"value": 10, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-005:2"}
```

### WD-tru_diem-006 · tier A · vai: tài xế công nghệ · kiểu: tinh_huong_ban_than

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → 2027-12-31
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K3, ND168-2024/D21/K3/a, ND168-2024/D21/K3/b

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
3. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
a) Không sử dụng thẻ nhận dạng lái xe để đăng nhập thông tin theo quy định hoặc sử dụng thẻ nhận dạng lái xe của lái xe khác để đăng nhập thông tin khi điều khiển xe tham gia kinh doanh vận tải hàng hóa;
b) Điều khiển xe ô tô đầu kéo không lắp thiết bị ghi nhận hình ảnh người lái xe hoặc có lắp thiết bị ghi nhận hình ảnh người lái xe nhưng không có tác dụng trong quá trình xe tham gia giao thông theo quy định hoặc làm sai lệch dữ liệu của thiết bị ghi nhận hình ảnh người lái xe lắp trên xe ô tô.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D21/K13/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K13/a

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
13. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
a) Thực hiện hành vi quy định tại điểm b, điểm c, điểm đ khoản 2; điểm a khoản 3; khoản 4; khoản 5; điểm c, điểm d, điểm đ khoản 6 Điều này bị trừ điểm giấy phép lái xe (khi điều khiển xe ô tô) 02 điểm;

[0] 1.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D21/K3)
[1] 2.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D21/K3)
[2] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D21/K13/a)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi vừa điều khiển xe tải chở hàng và không lắp thiết bị ghi hình người lái, làm sao điểm giấy phép của tôi bị trừ?
- Đáp: Bạn sẽ bị trừ 02 điểm trên giấy phép lái xe. (Điều 21, Khoản 13, Nghị định 168/2024/NĐ-CP)

```json
{"qid": "tD-tru_diem-006", "question": "Tôi vừa điều khiển xe tải chở hàng và không lắp thiết bị ghi hình người lái, làm sao điểm giấy phép của tôi bị trừ?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Bạn sẽ bị trừ 02 điểm trên giấy phép lái xe. (Điều 21, Khoản 13, Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D21/K13/a"], "required_numbers": [{"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-006:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Trong lúc vận chuyển hàng hóa, tôi quên lắp camera ghi hình người lái, điểm giấy phép của mình sẽ bị trừ bao nhiêu?
- Đáp: Bạn sẽ bị trừ 02 điểm trên giấy phép lái xe. (Điều 21, Khoản 13, Nghị định 168/2024/NĐ-CP)

```json
{"qid": "tD-tru_diem-006", "question": "Trong lúc vận chuyển hàng hóa, tôi quên lắp camera ghi hình người lái, điểm giấy phép của mình sẽ bị trừ bao nhiêu?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Bạn sẽ bị trừ 02 điểm trên giấy phép lái xe. (Điều 21, Khoản 13, Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D21/K13/a"], "required_numbers": [{"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-006:2"}
```

### WD-tru_diem-007 · tier A · vai: sinh viên đi xe máy · kiểu: ngan

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K9

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
9. Phạt tiền từ 10.000.000 đồng đến 12.000.000 đồng đối với người điều khiển xe thực hiện hành vi nhận, trả hàng trên đường cao tốc.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D21/K13/c)
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K13/c

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
13. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
c) Thực hiện hành vi quy định tại khoản 9 Điều này bị trừ điểm giấy phép lái xe 06 điểm;

[0] 10.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D21/K9)
[1] 12.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D21/K9)
[2] 06 điểm (số điểm bị trừ, nêu tại ND168-2024/D21/K13/c)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Nếu tôi lái xe tải và dừng lại nhận hàng trên đường cao tốc, số điểm trên giấy phép sẽ bị trừ là bao nhiêu?
- Đáp: Bạn sẽ bị trừ 06 điểm trên giấy phép lái xe. (Điều 21, khoản 13c Nghị định 168/2024/NĐ-CP)
- Ghi chú: Giả định người lái xe là người điều khiển xe tải, không phải xe máy.

```json
{"qid": "tD-tru_diem-007", "question": "Nếu tôi lái xe tải và dừng lại nhận hàng trên đường cao tốc, số điểm trên giấy phép sẽ bị trừ là bao nhiêu?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Bạn sẽ bị trừ 06 điểm trên giấy phép lái xe. (Điều 21, khoản 13c Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D21/K13/c"], "required_numbers": [{"value": 6, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-007:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Khi một người điều khiển xe tải dừng lại để trả hàng trên đường cao tốc, điểm trên giấy phép của họ bị trừ bao nhiêu?
- Đáp: Số điểm bị trừ là 06 điểm. (Điều 21, khoản 13c Nghị định 168/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “trả hàng trên đường cao tốc …”
- Ghi chú: Giả định người điều khiển xe tải, không phải xe máy.

```json
{"qid": "tD-tru_diem-007", "question": "Khi một người điều khiển xe tải dừng lại để trả hàng trên đường cao tốc, điểm trên giấy phép của họ bị trừ bao nhiêu?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Số điểm bị trừ là 06 điểm. (Điều 21, khoản 13c Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D21/K13/c"], "required_numbers": [{"value": 6, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-007:2"}
```

### WD-tru_diem-008 · tier A · vai: cán bộ phường · kiểu: tinh_huong_ban_than

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K9, ND168-2024/D32/K9/a, ND168-2024/D32/K9/b, ND168-2024/D32/K9/c, ND168-2024/D32/K9/d, ND168-2024/D32/K9/đ, ND168-2024/D32/K9/e

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
9. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng đối với cá nhân, từ 8.000.000 đồng đến 12.000.000 đồng đối với tổ chức là chủ xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ, xe máy chuyên dùng và các loại xe tương tự xe ô tô thực hiện một trong các hành vi vi phạm sau đây:
a) Thuê, mượn linh kiện, phụ kiện của xe ô tô khi kiểm định;
b) Đưa xe cơ giới, xe máy chuyên dùng có giấy chứng nhận hoặc tem kiểm định an toàn kỹ thuật và bảo vệ môi trường (đối với loại xe có quy định phải kiểm định) nhưng đã hết hiệu lực (hạn sử dụng) dưới 01 tháng (kể cả rơ moóc và sơ mi rơ moóc) tham gia giao thông;
c) Giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại khoản 4 Điều 21 của Nghị định này hoặc trực tiếp điều khiển phương tiện thực hiện hành vi vi phạm quy định tại khoản 4 Điều 21 của Nghị định này;
d) Giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm d khoản 6 Điều 20; điểm b khoản 5 Điều 21 của Nghị định này hoặc trực tiếp điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm d khoản 6 Điều 20; điểm b khoản 5 Điều 21 của Nghị định này;
…

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K21/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K21/a

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
21. Ngoài việc bị áp dụng hình thức xử phạt, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
a) Thực hiện hành vi quy định tại điểm đ, điểm g, điểm m khoản 7; điểm đ, điểm e khoản 8; điểm b, điểm c, điểm d, điểm đ khoản 9; điểm a, điểm b, điểm đ khoản 11; điểm a khoản 12; điểm c khoản 13; điểm đ, điểm h khoản 14 Điều này trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện còn bị trừ điểm giấy phép lái xe 02 điểm;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D21/K4)
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K4

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
4. Phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng đối với người điều khiển xe thực hiện hành vi chở hàng vượt quá chiều cao xếp hàng cho phép đối với xe ô tô tải (kể cả rơ moóc và sơ mi rơ moóc).

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D20/K6/d)
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K6/d

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
6. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
d) Điều khiển xe ô tô kinh doanh vận tải, xe vận tải nội bộ quá thời gian quy định tại khoản 1 Điều 64 của Luật Trật tự, an toàn giao thông đường bộ; không thực hiện đúng quy định về thời gian nghỉ giữa hai lần lái xe liên tục của người lái xe;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D21/K5/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K5/b

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
5. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
b) Điều khiển xe ô tô kinh doanh vận tải, xe vận tải nội bộ quá thời gian quy định tại khoản 1 Điều 64 của Luật Trật tự, an toàn giao thông đường bộ; không thực hiện đúng quy định về thời gian nghỉ giữa hai lần lái xe liên tục của người lái xe;

[0] 4.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D32/K9)
[1] 6.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D32/K9)
[2] 8.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D32/K9)
[3] 12.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D32/K9)
[4] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D32/K21/a)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi lái xe ô tô đã hết hiệu lực kiểm định 20 ngày trước khi tham gia giao thông, tôi bị trừ bao nhiêu điểm?
- Đáp: Bạn sẽ bị trừ 02 điểm. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng.

```json
{"qid": "tD-tru_diem-008", "question": "Tôi lái xe ô tô đã hết hiệu lực kiểm định 20 ngày trước khi tham gia giao thông, tôi bị trừ bao nhiêu điểm?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Bạn sẽ bị trừ 02 điểm. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng.", "gold_units": ["ND168-2024/D32/K21/a", "ND168-2024/D32/K9"], "required_numbers": [{"value": 2, "unit": "diem"}, {"value": 4000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-008:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi đã thuê linh kiện xe trong quá trình kiểm định, tôi bị trừ bao nhiêu điểm?
- Đáp: Bạn sẽ bị trừ 02 điểm. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng.

```json
{"qid": "tD-tru_diem-008", "question": "Tôi đã thuê linh kiện xe trong quá trình kiểm định, tôi bị trừ bao nhiêu điểm?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Bạn sẽ bị trừ 02 điểm. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng.", "gold_units": ["ND168-2024/D32/K21/a", "ND168-2024/D32/K9"], "required_numbers": [{"value": 2, "unit": "diem"}, {"value": 4000000, "unit": "vnd"}, {"value": 6000000, "unit": "vnd"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-008:2"}
```

### WD-tru_diem-009 · tier A · vai: sinh viên đi xe máy · kiểu: nhieu_dieu_kien

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D12/K11, ND168-2024/D12/K11/a, ND168-2024/D12/K11/b, ND168-2024/D12/K11/c

Điều 12. Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm khác về quy tắc giao thông đường bộ; sử dụng lòng đường, vỉa hè vào mục đích khác
11. Phạt tiền từ 6.000.000 đồng đến 8.000.000 đồng đối với cá nhân thực hiện một trong các hành vi vi phạm sau đây:
a) Đặt, để chướng ngại vật, vật cản khác trái phép trên đường bộ; đổ chất gây trơn trượt trên đường bộ; đổ, xả thải, làm rơi vãi hóa chất, chất thải gây mất an toàn giao thông đường bộ;
b) Xâm phạm tính mạng, sức khỏe, tài sản của người bị nạn, người gây tai nạn giao thông đường bộ hoặc người giúp đỡ, cứu chữa, đưa người bị nạn đi cấp cứu;
c) Hủy hoại, làm hư hỏng, làm mất tác dụng thiết bị điều khiển, giám sát giao thông đường bộ, thiết bị thông minh hỗ trợ chỉ huy, điều khiển giao thông đường bộ.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D12/K17)
Mã điều khoản dùng được cho gold_units: ND168-2024/D12/K17

Điều 12. Xử phạt, trừ điểm giấy phép lái xe các hành vi vi phạm khác về quy tắc giao thông đường bộ; sử dụng lòng đường, vỉa hè vào mục đích khác
17. Ngoài việc bị áp dụng hình thức xử phạt, cá nhân thực hiện hành vi quy định tại điểm a, điểm b khoản 11 Điều này nếu là người điều khiển phương tiện bị trừ điểm giấy phép lái xe 02 điểm.

[0] 6.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D12/K11)
[1] 8.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D12/K11)
[2] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D12/K17)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi vừa dừng xe máy trên vỉa hè để lấy điện thoại, nhưng lại để một chai nước vỡ trên đường, khiến người đi bộ có thể trượt. Tôi bị trừ bao nhiêu điểm trên giấy phép lái xe?
- Đáp: Bạn sẽ bị trừ 02 điểm trên giấy phép lái xe. Điều này được quy định trong Nghị định 168/2024/NĐ-CP, Điều 12, Khoản 17.
- Ghi chú: Giả định người dùng là người điều khiển xe máy

```json
{"qid": "tD-tru_diem-009", "question": "Tôi vừa dừng xe máy trên vỉa hè để lấy điện thoại, nhưng lại để một chai nước vỡ trên đường, khiến người đi bộ có thể trượt. Tôi bị trừ bao nhiêu điểm trên giấy phép lái xe?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Bạn sẽ bị trừ 02 điểm trên giấy phép lái xe. Điều này được quy định trong Nghị định 168/2024/NĐ-CP, Điều 12, Khoản 17.", "gold_units": ["ND168-2024/D12/K17"], "required_numbers": [{"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-009:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Sau khi đỗ xe máy vào vỉa hè, tôi vô tình để một miếng vải rơi trên đường, gây nguy hiểm cho người đi bộ. Tôi sẽ mất bao nhiêu điểm trên giấy phép lái xe?
- Đáp: Bạn sẽ bị trừ 02 điểm trên giấy phép lái xe. Điều này được quy định trong Nghị định 168/2024/NĐ-CP, Điều 12, Khoản 17.
- Ghi chú: Giả định người dùng là người điều khiển xe máy

```json
{"qid": "tD-tru_diem-009", "question": "Sau khi đỗ xe máy vào vỉa hè, tôi vô tình để một miếng vải rơi trên đường, gây nguy hiểm cho người đi bộ. Tôi sẽ mất bao nhiêu điểm trên giấy phép lái xe?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Bạn sẽ bị trừ 02 điểm trên giấy phép lái xe. Điều này được quy định trong Nghị định 168/2024/NĐ-CP, Điều 12, Khoản 17.", "gold_units": ["ND168-2024/D12/K17"], "required_numbers": [{"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-009:2"}
```

### WD-tru_diem-010 · tier A · vai: sinh viên đi xe máy · kiểu: tinh_huong_ban_than

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D26/K14, ND168-2024/D26/K14/a, ND168-2024/D26/K14/b

Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
14. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
a) Thực hiện hành vi quy định tại điểm đ khoản 2; điểm b, điểm c, điểm d khoản 6; điểm b, điểm c, điểm e, điểm i khoản 7 Điều này trong trường hợp cá nhân kinh doanh vận tải là người trực tiếp điều khiển phương tiện còn bị trừ điểm giấy phép lái xe 02 điểm;
b) Thực hiện hành vi quy định tại điểm c khoản 8 Điều này trong trường hợp cá nhân kinh doanh vận tải là người trực tiếp điều khiển phương tiện còn bị trừ điểm giấy phép lái xe 06 điểm.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D26/K2/đ)
Mã điều khoản dùng được cho gold_units: ND168-2024/D26/K2/đ

Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
2. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với cá nhân, từ 2.000.000 đồng đến 4.000.000 đồng đối với tổ chức kinh doanh vận tải, dịch vụ hỗ trợ vận tải thực hiện một trong các hành vi vi phạm sau đây:
đ) Không cấp lệnh vận chuyển, giấy vận tải cho lái xe hoặc cấp lệnh vận chuyển, giấy vận tải nhưng không đúng theo quy định (đối với loại xe quy định phải cấp lệnh vận chuyển, giấy vận tải);

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D26/K6/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D26/K6/b

Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
6. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng đối với cá nhân, từ 8.000.000 đồng đến 12.000.000 đồng đối với tổ chức kinh doanh vận tải thực hiện một trong các hành vi vi phạm sau đây:
b) Sử dụng xe ô tô kinh doanh vận tải chở trẻ em mầm non, học sinh, xe ô tô kinh doanh vận tải kết hợp với hoạt động đưa đón trẻ em mầm non, học sinh không có thiết bị ghi nhận hình ảnh trẻ em mầm non, học sinh hoặc không có thiết bị có chức năng cảnh báo, chống bỏ quên trẻ em trên xe hoặc không có thiết bị ghi nhận hình ảnh trẻ em mầm non, học sinh và thiết bị có chức năng cảnh báo, chống bỏ quên trẻ em trên xe;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D26/K6/c)
Mã điều khoản dùng được cho gold_units: ND168-2024/D26/K6/c

Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
6. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng đối với cá nhân, từ 8.000.000 đồng đến 12.000.000 đồng đối với tổ chức kinh doanh vận tải thực hiện một trong các hành vi vi phạm sau đây:
c) Sử dụng xe ô tô kinh doanh vận tải chở trẻ em mầm non, học sinh không có màu sơn theo quy định;

[0] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D26/K14/a)
[1] 06 điểm (số điểm bị trừ, nêu tại ND168-2024/D26/K14/b)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là tài xế xe máy taxi, hôm nay tôi quên cấp lệnh vận chuyển cho khách, có bị trừ bao nhiêu điểm?
- Đáp: Bạn sẽ bị trừ 06 điểm trên giấy phép lái xe. Theo Nghị định 168/2024/NĐ-CP, điều 26 khoản 14 b) quy định rằng khi người điều khiển phương tiện thực hiện hành vi quy định tại điểm c khoản 8 và là người trực tiếp điều khiển phương tiện trong kinh doanh vận tải, thì bị trừ 06 điểm.
- Ghi chú: giả định tài xế xe máy taxi là người kinh doanh vận tải

```json
{"qid": "tD-tru_diem-010", "question": "Tôi là tài xế xe máy taxi, hôm nay tôi quên cấp lệnh vận chuyển cho khách, có bị trừ bao nhiêu điểm?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Bạn sẽ bị trừ 06 điểm trên giấy phép lái xe. Theo Nghị định 168/2024/NĐ-CP, điều 26 khoản 14 b) quy định rằng khi người điều khiển phương tiện thực hiện hành vi quy định tại điểm c khoản 8 và là người trực tiếp điều khiển phương tiện trong kinh doanh vận tải, thì bị trừ 06 điểm.", "gold_units": ["ND168-2024/D26/K14/b"], "required_numbers": [{"value": 6, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-010:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là tài xế xe máy taxi, khi tôi không cấp lệnh vận chuyển cho khách, có bị trừ bao nhiêu điểm?
- Đáp: Bạn sẽ bị trừ 06 điểm trên giấy phép lái xe. Theo Nghị định 168/2024/NĐ-CP, điều 26 khoản 14 b) quy định rằng khi người điều khiển phương tiện thực hiện hành vi quy định tại điểm c khoản 8 và là người trực tiếp điều khiển phương tiện trong kinh doanh vận tải, thì bị trừ 06 điểm.
- Ghi chú: giả định tài xế xe máy taxi là người kinh doanh vận tải

```json
{"qid": "tD-tru_diem-010", "question": "Tôi là tài xế xe máy taxi, khi tôi không cấp lệnh vận chuyển cho khách, có bị trừ bao nhiêu điểm?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Bạn sẽ bị trừ 06 điểm trên giấy phép lái xe. Theo Nghị định 168/2024/NĐ-CP, điều 26 khoản 14 b) quy định rằng khi người điều khiển phương tiện thực hiện hành vi quy định tại điểm c khoản 8 và là người trực tiếp điều khiển phương tiện trong kinh doanh vận tải, thì bị trừ 06 điểm.", "gold_units": ["ND168-2024/D26/K14/b"], "required_numbers": [{"value": 6, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-010:2"}
```

### WD-tru_diem-011 · tier A · vai: người mới học lái ô tô · kiểu: tinh_huong_nguoi_khac

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2026-08-15 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K14, ND168-2024/D32/K14/a, ND168-2024/D32/K14/b, ND168-2024/D32/K14/c, ND168-2024/D32/K14/d, ND168-2024/D32/K14/đ, ND168-2024/D32/K14/e, ND168-2024/D32/K14/g, ND168-2024/D32/K14/h, ND168-2024/D32/K14/i

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
14. Phạt tiền từ 28.000.000 đồng đến 30.000.000 đồng đối với cá nhân, từ 56.000.000 đồng đến 60.000.000 đồng đối với tổ chức là chủ xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ, xe máy chuyên dùng và các loại xe tương tự xe ô tô thực hiện một trong các hành vi vi phạm sau đây:
a) Giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm a khoản 3 Điều 22 của Nghị định này hoặc trực tiếp điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm a khoản 3 Điều 22 của Nghị định này;
b) Giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm b khoản 3 Điều 22 của Nghị định này hoặc trực tiếp điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm b khoản 3 Điều 22 của Nghị định này;
c) Giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm c khoản 3 Điều 22 của Nghị định này hoặc trực tiếp điều khiển phương tiện thực hiện hành vi vi phạm quy định tại điểm c khoản 3 Điều 22 của Nghị định này;
…

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K18/d)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K18/d

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
18. Ngoài việc bị phạt tiền, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị áp dụng các hình thức xử phạt bổ sung như sau:
d) Thực hiện hành vi quy định tại điểm d khoản 11, điểm h khoản 14, điểm c khoản 16 Điều này bị tước quyền sử dụng chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường và tem kiểm định của phương tiện từ 01 tháng đến 03 tháng;

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K18/đ)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K18/đ

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
18. Ngoài việc bị phạt tiền, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị áp dụng các hình thức xử phạt bổ sung như sau:
đ) Thực hiện hành vi quy định tại khoản 5, khoản 6 Điều này trong trường hợp chở vượt trên 50% số người quy định được phép chở của phương tiện còn bị tước quyền sử dụng phù hiệu từ 01 tháng đến 03 tháng (nếu có). Thực hiện hành vi quy định tại điểm a, điểm b khoản 11; điểm a, điểm b, điểm c, điểm đ khoản 13; điểm a, điểm b, điểm c, điểm d, điểm đ, điểm e, điểm g khoản 14; khoản 15; khoản 16 Điều này còn bị tước quyền sử dụng phù hiệu từ 01 tháng đến 03 tháng (nếu có),

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K21/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K21/a

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
21. Ngoài việc bị áp dụng hình thức xử phạt, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
a) Thực hiện hành vi quy định tại điểm đ, điểm g, điểm m khoản 7; điểm đ, điểm e khoản 8; điểm b, điểm c, điểm d, điểm đ khoản 9; điểm a, điểm b, điểm đ khoản 11; điểm a khoản 12; điểm c khoản 13; điểm đ, điểm h khoản 14 Điều này trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện còn bị trừ điểm giấy phép lái xe 02 điểm;

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K21/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K21/b

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
21. Ngoài việc bị áp dụng hình thức xử phạt, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
b) Thực hiện hành vi quy định tại điểm e, điểm g khoản 14 Điều này trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện còn bị trừ điểm giấy phép lái xe 03 điểm;

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K21/c)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K21/c

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
21. Ngoài việc bị áp dụng hình thức xử phạt, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
c) Thực hiện hành vi quy định tại điểm a, điểm b, điểm đ, điểm e khoản 13; điểm a, điểm b, điểm c, điểm d khoản 14; điểm a khoản 16 Điều này trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện còn bị trừ điểm giấy phép lái xe 04 điểm;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D22/K3/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D22/K3/a

Điều 22. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển hàng siêu trường, siêu trọng
3. Phạt tiền từ 13.000.000 đồng đến 15.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
a) Chở hàng siêu trường, siêu trọng không có giấy phép lưu hành hoặc có giấy phép lưu hành nhưng đã hết giá trị sử dụng hoặc sử dụng giấy phép lưu hành không do cơ quan có thẩm quyền cấp;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D22/K3/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D22/K3/b

Điều 22. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển hàng siêu trường, siêu trọng
3. Phạt tiền từ 13.000.000 đồng đến 15.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
b) Chở hàng siêu trường, siêu trọng có giấy phép lưu hành còn giá trị sử dụng nhưng tổng trọng lượng (sau khi đã xếp hàng lên xe) vượt quá quy định trong giấy phép lưu hành;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D22/K3/c)
Mã điều khoản dùng được cho gold_units: ND168-2024/D22/K3/c

Điều 22. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển hàng siêu trường, siêu trọng
3. Phạt tiền từ 13.000.000 đồng đến 15.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
c) Chở hàng siêu trường, siêu trọng có giấy phép lưu hành còn giá trị sử dụng nhưng đi không đúng tuyến đường quy định trong giấy phép lưu hành;

[0] 28.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D32/K14)
[1] 30.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D32/K14)
[2] 56.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D32/K14)
[3] 60.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D32/K14)
[4] 01 tháng (thời hạn tước quyền sử dụng tối thiểu, nêu tại ND168-2024/D32/K18/d)
[5] 03 tháng (thời hạn tước quyền sử dụng tối đa, nêu tại ND168-2024/D32/K18/d)
[6] 01 tháng (thời hạn tước quyền sử dụng tối thiểu, nêu tại ND168-2024/D32/K18/đ)
[7] 03 tháng (thời hạn tước quyền sử dụng tối đa, nêu tại ND168-2024/D32/K18/đ)
[8] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D32/K21/a)
[9] 03 điểm (số điểm bị trừ, nêu tại ND168-2024/D32/K21/b)
[10] 04 điểm (số điểm bị trừ, nêu tại ND168-2024/D32/K21/c)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Anh tôi lái xe ô tô chở 6 người trong khi xe chỉ được phép chở 4, anh ấy bị trừ bao nhiêu điểm trên giấy phép?
- Đáp: Anh tôi bị trừ 02 điểm trên giấy phép lái xe.
- Ghi chú: đi xe chở khách vượt quá số người quy định

```json
{"qid": "tD-tru_diem-011", "question": "Anh tôi lái xe ô tô chở 6 người trong khi xe chỉ được phép chở 4, anh ấy bị trừ bao nhiêu điểm trên giấy phép?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Anh tôi bị trừ 02 điểm trên giấy phép lái xe.", "gold_units": ["ND168-2024/D32/K21/a"], "required_numbers": [{"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-011:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Công ty tôi đã chở hàng siêu trọng vượt trọng lượng quy định, nhân viên lái xe bị trừ bao nhiêu điểm trên giấy phép?
- Đáp: Nhân viên bị trừ 03 điểm trên giấy phép lái xe.
- Ghi chú: chở hàng siêu trọng vượt trọng lượng

```json
{"qid": "tD-tru_diem-011", "question": "Công ty tôi đã chở hàng siêu trọng vượt trọng lượng quy định, nhân viên lái xe bị trừ bao nhiêu điểm trên giấy phép?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Nhân viên bị trừ 03 điểm trên giấy phép lái xe.", "gold_units": ["ND168-2024/D32/K21/b"], "required_numbers": [{"value": 3, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-011:2"}
```

### WD-tru_diem-012 · tier A · vai: người mới học lái ô tô · kiểu: nhieu_dieu_kien

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D28/K2

Điều 28. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ
2. Phạt tiền từ 2.000.000 đồng đến 3.000.000 đồng đối với hành vi điều khiển xe chở người bốn bánh có gắn động cơ kinh doanh vận tải, xe chở hàng bốn bánh có gắn động cơ kinh doanh vận tải không có hoặc không gắn phù hiệu theo quy định hoặc có nhưng đã hết giá trị sử dụng hoặc sử dụng phù hiệu không do cơ quan có thẩm quyền cấp.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D28/K4/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D28/K4/a

Điều 28. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ
4. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
a) Thực hiện hành vi quy định tại khoản 2 Điều này bị trừ điểm giấy phép lái xe 02 điểm;

[0] 2.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D28/K2)
[1] 3.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D28/K2)
[2] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D28/K4/a)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi mới học lái ô tô, hôm nay tôi lái xe chở khách nhưng chưa gắn biển hiệu hợp lệ. Nếu bị phát hiện, số điểm trên giấy phép sẽ bị trừ bao nhiêu?
- Đáp: Số điểm trên giấy phép sẽ bị trừ 02 điểm.

```json
{"qid": "tD-tru_diem-012", "question": "Tôi mới học lái ô tô, hôm nay tôi lái xe chở khách nhưng chưa gắn biển hiệu hợp lệ. Nếu bị phát hiện, số điểm trên giấy phép sẽ bị trừ bao nhiêu?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Số điểm trên giấy phép sẽ bị trừ 02 điểm.", "gold_units": ["ND168-2024/D28/K4/a"], "required_numbers": [{"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-012:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Công ty tôi thuê một lái xe chở hàng, xe không có biển hiệu hợp lệ. Khi bị xử phạt, điểm trên giấy phép của người lái sẽ bị trừ bao nhiêu?
- Đáp: Số điểm trên giấy phép sẽ bị trừ 02 điểm.

```json
{"qid": "tD-tru_diem-012", "question": "Công ty tôi thuê một lái xe chở hàng, xe không có biển hiệu hợp lệ. Khi bị xử phạt, điểm trên giấy phép của người lái sẽ bị trừ bao nhiêu?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Số điểm trên giấy phép sẽ bị trừ 02 điểm.", "gold_units": ["ND168-2024/D28/K4/a"], "required_numbers": [{"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-012:2"}
```

### WD-tru_diem-013 · tier A · vai: chủ doanh nghiệp vận tải · kiểu: tinh_huong_nguoi_khac

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K15

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
15. Phạt tiền từ 30.000.000 đồng đến 40.000.000 đồng đối với cá nhân, từ 60.000.000 đồng đến 80.000.000 đồng đối với tổ chức là chủ xe ô tô, xe máy chuyên dùng và các loại xe tương tự xe ô tô khi giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại khoản 7 Điều 21 của Nghị định này hoặc trực tiếp điều khiển phương tiện thực hiện hành vi vi phạm quy định tại khoản 7 Điều 21 của Nghị định này.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K18/c)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K18/c

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
18. Ngoài việc bị phạt tiền, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị áp dụng các hình thức xử phạt bổ sung như sau:
c) Thực hiện hành vi quy định tại điểm e khoản 7, điểm b khoản 11, điểm a khoản 13, khoản 15, điểm b khoản 16 Điều này mà phương tiện đó có thùng xe, khối lượng hàng hóa cho phép chuyên chở không đúng theo quy định hiện hành thì còn bị tước quyền sử dụng chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường và tem kiểm định của phương tiện từ 01 tháng đến 03 tháng;

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K18/đ)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K18/đ

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
18. Ngoài việc bị phạt tiền, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị áp dụng các hình thức xử phạt bổ sung như sau:
đ) Thực hiện hành vi quy định tại khoản 5, khoản 6 Điều này trong trường hợp chở vượt trên 50% số người quy định được phép chở của phương tiện còn bị tước quyền sử dụng phù hiệu từ 01 tháng đến 03 tháng (nếu có). Thực hiện hành vi quy định tại điểm a, điểm b khoản 11; điểm a, điểm b, điểm c, điểm đ khoản 13; điểm a, điểm b, điểm c, điểm d, điểm đ, điểm e, điểm g khoản 14; khoản 15; khoản 16 Điều này còn bị tước quyền sử dụng phù hiệu từ 01 tháng đến 03 tháng (nếu có),

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K21/e)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K21/e

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
21. Ngoài việc bị áp dụng hình thức xử phạt, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
e) Thực hiện hành vi quy định tại khoản 15 Điều này trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện còn bị trừ điểm giấy phép lái xe 08 điểm;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D21/K7)
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K7

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
7. Phạt tiền từ 7.000.000 đồng đến 8.000.000 đồng đối với một trong các hành vi sau đây:

[0] 30.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D32/K15)
[1] 40.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D32/K15)
[2] 60.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D32/K15)
[3] 80.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D32/K15)
[4] 01 tháng (thời hạn tước quyền sử dụng tối thiểu, nêu tại ND168-2024/D32/K18/c)
[5] 03 tháng (thời hạn tước quyền sử dụng tối đa, nêu tại ND168-2024/D32/K18/c)
[6] 01 tháng (thời hạn tước quyền sử dụng tối thiểu, nêu tại ND168-2024/D32/K18/đ)
[7] 03 tháng (thời hạn tước quyền sử dụng tối đa, nêu tại ND168-2024/D32/K18/đ)
[8] 08 điểm (số điểm bị trừ, nêu tại ND168-2024/D32/K21/e)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Công ty tôi có một lái xe đã chở quá 50% số người quy định được phép chở, và người đó còn trực tiếp điều khiển xe khi vi phạm. Tôi muốn biết số điểm bị trừ trên giấy phép lái xe của người đó là bao nhiêu?
- Đáp: Số điểm bị trừ là 08 điểm. (khoản e Điều 32 Nghị định 168/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “50 số người quy định được …”

```json
{"qid": "tD-tru_diem-013", "question": "Công ty tôi có một lái xe đã chở quá 50% số người quy định được phép chở, và người đó còn trực tiếp điều khiển xe khi vi phạm. Tôi muốn biết số điểm bị trừ trên giấy phép lái xe của người đó là bao nhiêu?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Số điểm bị trừ là 08 điểm. (khoản e Điều 32 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D32/K21/e"], "required_numbers": [{"value": 8, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-013:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Anh tôi, người điều khiển xe của công ty, đã vi phạm quy định tại khoản 15 của Nghị định 168/2024/NĐ-CP khi trực tiếp điều khiển xe. Anh ấy muốn biết số điểm bị trừ trên giấy phép lái xe là bao nhiêu?
- Đáp: Số điểm bị trừ là 08 điểm. (khoản e Điều 32 Nghị định 168/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “vi phạm quy định tại khoản …”; neu_dieu_khoan

```json
{"qid": "tD-tru_diem-013", "question": "Anh tôi, người điều khiển xe của công ty, đã vi phạm quy định tại khoản 15 của Nghị định 168/2024/NĐ-CP khi trực tiếp điều khiển xe. Anh ấy muốn biết số điểm bị trừ trên giấy phép lái xe là bao nhiêu?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Số điểm bị trừ là 08 điểm. (khoản e Điều 32 Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D32/K21/e"], "required_numbers": [{"value": 8, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-013:2"}
```

### WD-tru_diem-014 · tier A · vai: cán bộ phường · kiểu: neu_van_ban

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D22/K3, ND168-2024/D22/K3/a, ND168-2024/D22/K3/b, ND168-2024/D22/K3/c, ND168-2024/D22/K3/d

Điều 22. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển hàng siêu trường, siêu trọng
3. Phạt tiền từ 13.000.000 đồng đến 15.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
a) Chở hàng siêu trường, siêu trọng không có giấy phép lưu hành hoặc có giấy phép lưu hành nhưng đã hết giá trị sử dụng hoặc sử dụng giấy phép lưu hành không do cơ quan có thẩm quyền cấp;
b) Chở hàng siêu trường, siêu trọng có giấy phép lưu hành còn giá trị sử dụng nhưng tổng trọng lượng (sau khi đã xếp hàng lên xe) vượt quá quy định trong giấy phép lưu hành;
c) Chở hàng siêu trường, siêu trọng có giấy phép lưu hành còn giá trị sử dụng nhưng đi không đúng tuyến đường quy định trong giấy phép lưu hành;
d) Chở hàng siêu trường, siêu trọng có giấy phép lưu hành còn giá trị sử dụng nhưng chở không đúng loại hàng quy định trong giấy phép lưu hành.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D22/K6/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D22/K6/b

Điều 22. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển hàng siêu trường, siêu trọng
6. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
b) Thực hiện hành vi quy định tại khoản 2, khoản 3 Điều này bị trừ điểm giấy phép lái xe 04 điểm.

[0] 13.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D22/K3)
[1] 15.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D22/K3)
[2] 04 điểm (số điểm bị trừ, nêu tại ND168-2024/D22/K6/b)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi đang vận chuyển hàng siêu trọng, nhưng đã vượt quá trọng lượng quy định trong giấy phép lưu hành. Theo Nghị định 168/2024/NĐ-CP, tôi bị trừ bao nhiêu điểm?
- Đáp: Bạn sẽ bị trừ 04 điểm. (điều 22, khoản 6, Nghị định 168/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “quy định trong giấy phép lưu …”

```json
{"qid": "tD-tru_diem-014", "question": "Tôi đang vận chuyển hàng siêu trọng, nhưng đã vượt quá trọng lượng quy định trong giấy phép lưu hành. Theo Nghị định 168/2024/NĐ-CP, tôi bị trừ bao nhiêu điểm?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Bạn sẽ bị trừ 04 điểm. (điều 22, khoản 6, Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D22/K6/b"], "required_numbers": [{"value": 4, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-014:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi đang chở hàng siêu trường, siêu trọng nhưng không có giấy phép lưu hành. Theo Nghị định 168/2024/NĐ-CP, tôi bị trừ bao nhiêu điểm?
- Đáp: Bạn sẽ bị trừ 04 điểm. (điều 22, khoản 6, Nghị định 168/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “chở hàng siêu trường siêu trọng …”

```json
{"qid": "tD-tru_diem-014", "question": "Tôi đang chở hàng siêu trường, siêu trọng nhưng không có giấy phép lưu hành. Theo Nghị định 168/2024/NĐ-CP, tôi bị trừ bao nhiêu điểm?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Bạn sẽ bị trừ 04 điểm. (điều 22, khoản 6, Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D22/K6/b"], "required_numbers": [{"value": 4, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-014:2"}
```

### WD-tru_diem-015 · tier A · vai: tài xế xe tải · kiểu: tinh_huong_ban_than

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2026-08-15 → 2027-12-31
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K5, ND168-2024/D20/K5/a, ND168-2024/D20/K5/b, ND168-2024/D20/K5/c, ND168-2024/D20/K5/d, ND168-2024/D20/K5/đ, ND168-2024/D20/K5/e, ND168-2024/D20/K5/g, ND168-2024/D20/K5/h, ND168-2024/D20/K5/i, ND168-2024/D20/K5/k, ND168-2024/D20/K5/l, ND168-2024/D20/K5/m

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
5. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
a) Để người lên, xuống xe khi xe đang chạy;
b) Xếp hành lý, hàng hóa trên xe làm lệch xe;
c) Đón, trả hành khách không đúng nơi quy định trên những tuyến đường đã xác định nơi đón, trả khách hoặc dừng đón, trả hành khách quá thời gian quy định, trừ hành vi vi phạm quy định tại khoản 8 Điều này;
d) Đón, trả hành khách tại nơi cấm dừng, cấm đỗ, nơi đường cong tầm nhìn bị che khuất, trừ hành vi vi phạm quy định tại khoản 8 Điều này;
đ) Điều khiển xe vận tải hành khách theo hợp đồng sử dụng hợp đồng bằng văn bản giấy mà không có hợp đồng vận tải, danh sách hành khách theo quy định; có hợp đồng vận tải nhưng không đúng theo quy định; đón khách, chở người không có tên trong danh sách hành khách theo hợp đồng đã ký;
e) Vận chuyển hành khách theo tuyến cố định không có hoặc không mang theo lệnh vận chuyển hoặc có mang theo lệnh vận chuyển nhưng không ghi đầy đủ thông tin, không có xác nhận của bến xe khách nơi đi, bến xe khách nơi đến theo quy định;
…

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D20/K10/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K10/a

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
10. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
a) Thực hiện hành vi quy định tại điểm c, điểm d, điểm e khoản 3; điểm a, điểm b, điểm c, điểm d, điểm đ, điểm e, điểm g, điểm h, điểm i, điểm k, điểm m khoản 5; khoản 6; khoản 7 Điều này bị trừ điểm giấy phép lái xe 02 điểm;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D20/K8)
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K8

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
8. Phạt tiền từ 10.000.000 đồng đến 12.000.000 đồng đối với người điều khiển xe thực hiện hành vi đón, trả hành khách trên đường cao tốc.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D37/K1/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D37/K1/b

Điều 37. Xử phạt người điều khiển phương tiện giao thông cơ giới đường bộ gắn biển số nước ngoài
1. Phạt tiền từ 1.000.000 đồng đến 2.000.000 đồng đối với người điều khiển phương tiện giao thông cơ giới đường bộ gắn biển số nước ngoài thực hiện một trong các hành vi vi phạm sau đây:
b) Điều khiển xe chở hành khách không có danh sách hành khách theo quy định.

[0] 1.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D20/K5)
[1] 2.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D20/K5)
[2] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D20/K10/a)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi đang lái xe tải, khi đang xếp hàng hóa lên xe, hàng đã lệch và làm xe nghiêng. Tôi bị trừ bao nhiêu điểm trên giấy phép lái xe?
- Đáp: Bạn sẽ bị trừ 02 điểm trên giấy phép lái xe. (Điều 20, Khoản 10, Nghị định 168/2024/NĐ-CP)

```json
{"qid": "tD-tru_diem-015", "question": "Tôi đang lái xe tải, khi đang xếp hàng hóa lên xe, hàng đã lệch và làm xe nghiêng. Tôi bị trừ bao nhiêu điểm trên giấy phép lái xe?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Bạn sẽ bị trừ 02 điểm trên giấy phép lái xe. (Điều 20, Khoản 10, Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D20/K10/a"], "required_numbers": [{"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-015:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi lái xe tải trên đường cao tốc, dừng lại để đón hành khách tại một điểm không được phép dừng. Tôi bị trừ bao nhiêu điểm trên giấy phép lái xe?
- Đáp: Bạn sẽ bị trừ 02 điểm trên giấy phép lái xe. (Điều 20, Khoản 10, Nghị định 168/2024/NĐ-CP)

```json
{"qid": "tD-tru_diem-015", "question": "Tôi lái xe tải trên đường cao tốc, dừng lại để đón hành khách tại một điểm không được phép dừng. Tôi bị trừ bao nhiêu điểm trên giấy phép lái xe?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Bạn sẽ bị trừ 02 điểm trên giấy phép lái xe. (Điều 20, Khoản 10, Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D20/K10/a"], "required_numbers": [{"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-015:2"}
```

### WD-tru_diem-016 · tier A · vai: phụ huynh có con dưới 18 tuổi · kiểu: tinh_huong_ban_than

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D23/K5

Điều 23. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển hàng hóa nguy hiểm
5. Phạt tiền từ 12.000.000 đồng đến 14.000.000 đồng đối với hành vi vận chuyển hàng hóa nguy hiểm không có giấy phép vận chuyển hàng hóa nguy hiểm hoặc có nhưng hết hiệu lực hoặc không thực hiện đúng quy định trong giấy phép vận chuyển hàng hóa nguy hiểm, trừ các hành vi vi phạm quy định tại điểm a khoản 6 Điều 20 của Nghị định này.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D23/K7/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D23/K7/b

Điều 23. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô thực hiện hành vi vi phạm quy định về vận chuyển hàng hóa nguy hiểm
7. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
b) Thực hiện hành vi quy định tại khoản 5 Điều này bị trừ điểm giấy phép lái xe 04 điểm.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D20/K6/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K6/a

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
6. Phạt tiền từ 3.000.000 đồng đến 5.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
a) Vận chuyển hàng hóa nguy hiểm, hàng độc hại, dễ cháy, dễ nổ, động vật, hàng có mùi hôi thối hoặc hàng hóa khác ảnh hưởng đến sức khỏe của hành khách trên xe;

[0] 12.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D23/K5)
[1] 14.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D23/K5)
[2] 04 điểm (số điểm bị trừ, nêu tại ND168-2024/D23/K7/b)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Con tôi đang lái xe ô tô chở hàng, nhưng chưa có giấy phép vận chuyển hàng hóa nguy hiểm. Tôi muốn biết số điểm sẽ bị trừ trên giấy phép lái xe của mình?
- Đáp: Bạn sẽ bị trừ 04 điểm trên giấy phép lái xe.
- ⚠ chep_nguyen_van: “có giấy phép vận chuyển hàng …”

```json
{"qid": "tD-tru_diem-016", "question": "Con tôi đang lái xe ô tô chở hàng, nhưng chưa có giấy phép vận chuyển hàng hóa nguy hiểm. Tôi muốn biết số điểm sẽ bị trừ trên giấy phép lái xe của mình?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Bạn sẽ bị trừ 04 điểm trên giấy phép lái xe.", "gold_units": ["ND168-2024/D23/K7/b"], "required_numbers": [{"value": 4, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-016:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi đang chuẩn bị vận chuyển hàng hóa dễ cháy bằng xe ô tô, nhưng chưa có giấy phép. Tôi cần biết có bị trừ bao nhiêu điểm trên giấy phép lái xe không?
- Đáp: Bạn sẽ bị trừ 04 điểm trên giấy phép lái xe.

```json
{"qid": "tD-tru_diem-016", "question": "Tôi đang chuẩn bị vận chuyển hàng hóa dễ cháy bằng xe ô tô, nhưng chưa có giấy phép. Tôi cần biết có bị trừ bao nhiêu điểm trên giấy phép lái xe không?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Bạn sẽ bị trừ 04 điểm trên giấy phép lái xe.", "gold_units": ["ND168-2024/D23/K7/b"], "required_numbers": [{"value": 4, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-016:2"}
```

### WD-tru_diem-017 · tier A · vai: chủ doanh nghiệp vận tải · kiểu: tinh_huong_ban_than

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2026-08-15 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K8, ND168-2024/D21/K8/a, ND168-2024/D21/K8/b, ND168-2024/D21/K8/c, ND168-2024/D21/K8/d, ND168-2024/D21/K8/đ, ND168-2024/D21/K8/e

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
8. Phạt tiền từ 8.000.000 đồng đến 12.000.000 đồng đối với một trong các hành vi sau đây:
a) Điều khiển xe (kể cả rơ moóc và sơ mi rơ moóc) chở hàng vượt trọng tải (khối lượng hàng chuyên chở) cho phép tham gia giao thông được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe trên 150%;
b) Điều khiển xe kéo theo rơ moóc, sơ mi rơ moóc mà khối lượng toàn bộ (bao gồm khối lượng bản thân rơ moóc, sơ mi rơ moóc và khối lượng hàng chuyên chở) của rơ moóc, sơ mi rơ moóc vượt khối lượng cho phép kéo theo được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe trên 150%;
c) Chở công-ten-nơ trên xe (kể cả sơ mi rơ moóc) không bảo đảm quy chuẩn, tiêu chuẩn kỹ thuật của công-ten-nơ theo quy định;
d) Chở thiết bị có hình dạng thùng hoặc có hình dạng như công-ten-nơ (không phải công-ten-nơ) vượt quá chiều dài toàn bộ được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của rơ moóc, sơ mi rơ moóc; chở loại hàng không đúng với thông tin ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của rơ moóc, sơ mi rơ moóc;
…

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D21/K13/b)
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K13/b

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
13. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
b) Thực hiện hành vi quy định tại điểm a, điểm b khoản 6; điểm c, điểm d, điểm đ khoản 8; khoản 10 Điều này bị trừ điểm giấy phép lái xe 04 điểm;

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D21/K13/đ)
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K13/đ

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
13. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
đ) Thực hiện hành vi quy định tại điểm a, điểm b khoản 8; khoản 11 Điều này bị trừ điểm giấy phép lái xe 10 điểm.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D21/K10)
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K10

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
10. Phạt tiền từ 18.000.000 đồng đến 22.000.000 đồng đối với một trong các hành vi vi phạm sau đây:

[0] 8.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D21/K8)
[1] 12.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D21/K8)
[2] 04 điểm (số điểm bị trừ, nêu tại ND168-2024/D21/K13/b)
[3] 10 điểm (số điểm bị trừ, nêu tại ND168-2024/D21/K13/đ)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi điều khiển xe tải kéo rơ moóc, chở hàng vượt trọng tải 160% so với quy định. Tôi bị trừ bao nhiêu điểm trên giấy phép lái xe?
- Đáp: Bạn sẽ bị trừ 04 điểm trên giấy phép lái xe. (Điều 21, Khoản 13, Nghị định 168/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “moóc chở hàng vượt trọng tải …”

```json
{"qid": "tD-tru_diem-017", "question": "Tôi điều khiển xe tải kéo rơ moóc, chở hàng vượt trọng tải 160% so với quy định. Tôi bị trừ bao nhiêu điểm trên giấy phép lái xe?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Bạn sẽ bị trừ 04 điểm trên giấy phép lái xe. (Điều 21, Khoản 13, Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D21/K13/b"], "required_numbers": [{"value": 4, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-017:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi điều khiển xe tải kéo rơ moóc, chở hàng không đúng thông tin trong chứng nhận, vượt chiều dài quy định. Tôi bị trừ bao nhiêu điểm?
- Đáp: Bạn sẽ bị trừ 10 điểm trên giấy phép lái xe. (Điều 21, Khoản 13, Nghị định 168/2024/NĐ-CP)

```json
{"qid": "tD-tru_diem-017", "question": "Tôi điều khiển xe tải kéo rơ moóc, chở hàng không đúng thông tin trong chứng nhận, vượt chiều dài quy định. Tôi bị trừ bao nhiêu điểm?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Bạn sẽ bị trừ 10 điểm trên giấy phép lái xe. (Điều 21, Khoản 13, Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D21/K13/đ"], "required_numbers": [{"value": 10, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-017:2"}
```

### WD-tru_diem-018 · tier A · vai: chủ doanh nghiệp vận tải · kiểu: tinh_huong_ban_than

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D26/K6, ND168-2024/D26/K6/a, ND168-2024/D26/K6/b, ND168-2024/D26/K6/c, ND168-2024/D26/K6/d

Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
6. Phạt tiền từ 4.000.000 đồng đến 6.000.000 đồng đối với cá nhân, từ 8.000.000 đồng đến 12.000.000 đồng đối với tổ chức kinh doanh vận tải thực hiện một trong các hành vi vi phạm sau đây:
a) Sử dụng xe vận chuyển động vật sống không có kết cấu phù hợp với loại động vật chuyên chở theo quy định;
b) Sử dụng xe ô tô kinh doanh vận tải chở trẻ em mầm non, học sinh, xe ô tô kinh doanh vận tải kết hợp với hoạt động đưa đón trẻ em mầm non, học sinh không có thiết bị ghi nhận hình ảnh trẻ em mầm non, học sinh hoặc không có thiết bị có chức năng cảnh báo, chống bỏ quên trẻ em trên xe hoặc không có thiết bị ghi nhận hình ảnh trẻ em mầm non, học sinh và thiết bị có chức năng cảnh báo, chống bỏ quên trẻ em trên xe;
c) Sử dụng xe ô tô kinh doanh vận tải chở trẻ em mầm non, học sinh không có màu sơn theo quy định;
d) Sử dụng xe ô tô kinh doanh vận tải chở trẻ em mầm non, học sinh, xe ô tô kinh doanh vận tải kết hợp với hoạt động đưa đón trẻ em mầm non, học sinh không có biển báo dấu hiệu nhận biết là xe chở trẻ em mầm non, học sinh theo quy định.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D26/K14/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D26/K14/a

Điều 26. Xử phạt các hành vi vi phạm quy định về trật tự, an toàn giao thông đường bộ trong vận tải đường bộ, dịch vụ hỗ trợ vận tải đường bộ
14. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
a) Thực hiện hành vi quy định tại điểm đ khoản 2; điểm b, điểm c, điểm d khoản 6; điểm b, điểm c, điểm e, điểm i khoản 7 Điều này trong trường hợp cá nhân kinh doanh vận tải là người trực tiếp điều khiển phương tiện còn bị trừ điểm giấy phép lái xe 02 điểm;

[0] 4.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D26/K6)
[1] 6.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D26/K6)
[2] 8.000.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D26/K6)
[3] 12.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D26/K6)
[4] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D26/K14/a)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi là chủ doanh nghiệp vận tải, một trong các xe của chúng tôi đã chở động vật sống mà không có cấu kiện phù hợp. Tôi bị trừ bao nhiêu điểm trên giấy phép lái xe?
- Đáp: Bạn sẽ bị trừ 02 điểm trên giấy phép lái xe.

```json
{"qid": "tD-tru_diem-018", "question": "Tôi là chủ doanh nghiệp vận tải, một trong các xe của chúng tôi đã chở động vật sống mà không có cấu kiện phù hợp. Tôi bị trừ bao nhiêu điểm trên giấy phép lái xe?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Bạn sẽ bị trừ 02 điểm trên giấy phép lái xe.", "gold_units": ["ND168-2024/D26/K14/a"], "required_numbers": [{"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-018:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi là chủ doanh nghiệp vận tải, một xe của tôi đã chở trẻ em mà không có thiết bị ghi hình hoặc cảnh báo. Tôi bị trừ bao nhiêu điểm trên giấy phép lái xe?
- Đáp: Bạn sẽ bị trừ 02 điểm trên giấy phép lái xe.

```json
{"qid": "tD-tru_diem-018", "question": "Tôi là chủ doanh nghiệp vận tải, một xe của tôi đã chở trẻ em mà không có thiết bị ghi hình hoặc cảnh báo. Tôi bị trừ bao nhiêu điểm trên giấy phép lái xe?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Bạn sẽ bị trừ 02 điểm trên giấy phép lái xe.", "gold_units": ["ND168-2024/D26/K14/a"], "required_numbers": [{"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-018:2"}
```

### WD-tru_diem-019 · tier A · vai: tài xế công nghệ · kiểu: tinh_huong_ban_than

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2025-01-01 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K5

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
5. Phạt tiền từ 800.000 đồng đến 1.200.000 đồng trên mỗi người vượt quá quy định được phép chở của phương tiện nhưng tổng mức phạt tiền tối đa không vượt quá 75.000.000 đồng đối với chủ phương tiện là cá nhân, từ 1.600.000 đồng đến 2.400.000 đồng trên mỗi người vượt quá quy định được phép chở của phương tiện nhưng tổng mức phạt tiền tối đa không vượt quá 150.000.000 đồng đối với chủ phương tiện là tổ chức giao phương tiện hoặc để cho người làm công, người đại diện điều khiển phương tiện thực hiện hành vi vi phạm quy định tại khoản 2 Điều 20 của Nghị định này hoặc trực tiếp điều khiển phương tiện thực hiện hành vi vi phạm quy định tại khoản 2 Điều 20 của Nghị định này.

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K18/đ)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K18/đ

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
18. Ngoài việc bị phạt tiền, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị áp dụng các hình thức xử phạt bổ sung như sau:
đ) Thực hiện hành vi quy định tại khoản 5, khoản 6 Điều này trong trường hợp chở vượt trên 50% số người quy định được phép chở của phương tiện còn bị tước quyền sử dụng phù hiệu từ 01 tháng đến 03 tháng (nếu có). Thực hiện hành vi quy định tại điểm a, điểm b khoản 11; điểm a, điểm b, điểm c, điểm đ khoản 13; điểm a, điểm b, điểm c, điểm d, điểm đ, điểm e, điểm g khoản 14; khoản 15; khoản 16 Điều này còn bị tước quyền sử dụng phù hiệu từ 01 tháng đến 03 tháng (nếu có),

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K21/d)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K21/d

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
21. Ngoài việc bị áp dụng hình thức xử phạt, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
d) Thực hiện hành vi quy định tại khoản 5, khoản 6 Điều này trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện chở vượt trên 50% đến 100% số người quy định được phép chở của phương tiện, còn bị trừ điểm giấy phép lái xe 04 điểm;

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D32/K21/h)
Mã điều khoản dùng được cho gold_units: ND168-2024/D32/K21/h

Điều 32. Xử phạt, trừ điểm giấy phép lái xe đối với chủ phương tiện vi phạm quy định liên quan đến giao thông đường bộ
21. Ngoài việc bị áp dụng hình thức xử phạt, cá nhân, tổ chức thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
h) Thực hiện hành vi quy định tại khoản 5, khoản 6 Điều này trong trường hợp chủ phương tiện là người trực tiếp điều khiển phương tiện chở vượt trên 100% số người quy định được phép chở của phương tiện còn bị trừ điểm giấy phép lái xe 10 điểm.

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D20/K2)
Mã điều khoản dùng được cho gold_units: ND168-2024/D20/K2

Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
2. Phạt tiền từ 400.000 đồng đến 600.000 đồng trên mỗi người vượt quá quy định được phép chở của phương tiện nhưng tổng mức phạt tiền tối đa không vượt quá 75.000.000 đồng đối với người điều khiển xe ô tô chở hành khách, ô tô chở người (trừ xe buýt) thực hiện hành vi vi phạm chở quá số người quy định được phép chở của phương tiện, trừ các hành vi vi phạm quy định tại khoản 4 Điều này.

[0] 01 tháng (thời hạn tước quyền sử dụng tối thiểu, nêu tại ND168-2024/D32/K18/đ)
[1] 03 tháng (thời hạn tước quyền sử dụng tối đa, nêu tại ND168-2024/D32/K18/đ)
[2] 800.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D32/K5)
[3] 1.200.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D32/K5)
[4] 04 điểm (số điểm bị trừ, nêu tại ND168-2024/D32/K21/d)
[5] 10 điểm (số điểm bị trừ, nêu tại ND168-2024/D32/K21/h)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi vừa lái xe chở khách và đã vượt quá 50% số người quy định được phép chở. Tôi bị trừ bao nhiêu điểm?
- Đáp: Bạn sẽ bị trừ 04 điểm. (điều 32, khoản 21, điểm d, Nghị định 168/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “50 số người quy định được …”

```json
{"qid": "tD-tru_diem-019", "question": "Tôi vừa lái xe chở khách và đã vượt quá 50% số người quy định được phép chở. Tôi bị trừ bao nhiêu điểm?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Bạn sẽ bị trừ 04 điểm. (điều 32, khoản 21, điểm d, Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D32/K21/d"], "required_numbers": [{"value": 4, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-019:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Tôi điều khiển xe chở khách vượt quá 100% số người quy định được phép chở. Số điểm bị trừ là bao nhiêu?
- Đáp: Bạn sẽ bị trừ 10 điểm. (điều 32, khoản 21, điểm h, Nghị định 168/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “100 số người quy định được …”

```json
{"qid": "tD-tru_diem-019", "question": "Tôi điều khiển xe chở khách vượt quá 100% số người quy định được phép chở. Số điểm bị trừ là bao nhiêu?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Bạn sẽ bị trừ 10 điểm. (điều 32, khoản 21, điểm h, Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D32/K21/h"], "required_numbers": [{"value": 10, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-019:2"}
```

### WD-tru_diem-020 · tier A · vai: người mới học lái ô tô · kiểu: tinh_huong_ban_than

<details><summary>Nguồn và con số</summary>

```text
### Nguồn 1
Văn bản: Nghị định số 168/2024/NĐ-CP (Quy định xử phạt vi phạm hành chính về trật tự, an toàn giao thông trong lĩnh vực giao thông đường bộ; trừ điểm, phục hồi điểm giấy phép lái xe)
Hiệu lực của trạng thái này: 2026-08-15 → nay
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K2, ND168-2024/D21/K2/a, ND168-2024/D21/K2/b, ND168-2024/D21/K2/c, ND168-2024/D21/K2/d, ND168-2024/D21/K2/đ

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
2. Phạt tiền từ 800.000 đồng đến 1.000.000 đồng đối với một trong các hành vi vi phạm sau đây:
a) Điều khiển xe (kể cả rơ moóc và sơ mi rơ moóc) chở hàng vượt trọng tải (khối lượng hàng chuyên chở) cho phép tham gia giao thông được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe trên 10% đến 30% (trừ xe xi téc chở chất lỏng), trên 20% đến 30% đối với xe xi téc chở chất lỏng;
b) Chở hàng trên nóc thùng xe; chở hàng vượt quá bề rộng thùng xe (kể cả bề rộng rơ moóc và sơ mi rơ moóc); chở hàng vượt phía trước, phía sau thùng xe (kể cả rơ moóc và sơ mi rơ moóc) trên 10% chiều dài toàn bộ của xe theo thiết kế được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe, trừ hành vi vi phạm quy định tại điểm d khoản 8 Điều 21 Nghị định này
c) Chở người trên mui xe;
d) Điều khiển xe kéo theo rơ moóc, sơ mi rơ moóc mà khối lượng toàn bộ (bao gồm khối lượng bản thân rơ moóc, sơ mi rơ moóc và khối lượng hàng chuyên chở) của rơ moóc, sơ mi rơ moóc vượt khối lượng cho phép kéo theo được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của xe trên 10% đến 30%;
…

### Điều khoản nêu chế tài áp cho hành vi trên (ND168-2024/D21/K13/a)
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K13/a

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
13. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển phương tiện thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
a) Thực hiện hành vi quy định tại điểm b, điểm c, điểm đ khoản 2; điểm a khoản 3; khoản 4; khoản 5; điểm c, điểm d, điểm đ khoản 6 Điều này bị trừ điểm giấy phép lái xe (khi điều khiển xe ô tô) 02 điểm;

### Điều khoản được nguồn trên dẫn chiếu tới (ND168-2024/D21/K8/d)
Mã điều khoản dùng được cho gold_units: ND168-2024/D21/K8/d

Điều 21. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô tải, máy kéo (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo) và các loại xe tương tự xe ô tô vận chuyển hàng hóa vi phạm quy định về bảo đảm trật tự, an toàn giao thông đường bộ với xe ô tô vận chuyển hàng hóa
8. Phạt tiền từ 8.000.000 đồng đến 12.000.000 đồng đối với một trong các hành vi sau đây:
d) Chở thiết bị có hình dạng thùng hoặc có hình dạng như công-ten-nơ (không phải công-ten-nơ) vượt quá chiều dài toàn bộ được ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của rơ moóc, sơ mi rơ moóc; chở loại hàng không đúng với thông tin ghi trong chứng nhận kiểm định an toàn kỹ thuật và bảo vệ môi trường của rơ moóc, sơ mi rơ moóc;

[0] 800.000 đồng (mức phạt tiền tối thiểu, nêu tại ND168-2024/D21/K2)
[1] 1.000.000 đồng (mức phạt tiền tối đa, nêu tại ND168-2024/D21/K2)
[2] 02 điểm (số điểm bị trừ, nêu tại ND168-2024/D21/K13/a)
```

</details>

**Nháp 1**

- Hỏi (2026-11-03): Tôi vừa lái xe tải chở hàng và phát hiện rằng trọng tải vượt quá giới hạn cho phép, sau khi bị cảnh sát dừng, tôi muốn biết số điểm bị trừ trên giấy phép lái xe của mình là bao nhiêu?
- Đáp: Bạn sẽ bị trừ 02 điểm trên giấy phép lái xe. (Điều 21, Khoản 13, Nghị định 168/2024/NĐ-CP)

```json
{"qid": "tD-tru_diem-020", "question": "Tôi vừa lái xe tải chở hàng và phát hiện rằng trọng tải vượt quá giới hạn cho phép, sau khi bị cảnh sát dừng, tôi muốn biết số điểm bị trừ trên giấy phép lái xe của mình là bao nhiêu?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Bạn sẽ bị trừ 02 điểm trên giấy phép lái xe. (Điều 21, Khoản 13, Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D21/K13/a"], "required_numbers": [{"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-020:1"}
```

**Nháp 2**

- Hỏi (2026-11-03): Trong lúc lái xe tải, tôi đã chở hàng trên nóc thùng xe và bị cảnh sát dừng, tôi muốn biết số điểm bị trừ trên giấy phép lái xe của mình là bao nhiêu?
- Đáp: Bạn sẽ bị trừ 02 điểm trên giấy phép lái xe. (Điều 21, Khoản 13, Nghị định 168/2024/NĐ-CP)
- ⚠ chep_nguyen_van: “chở hàng trên nóc thùng xe …”

```json
{"qid": "tD-tru_diem-020", "question": "Trong lúc lái xe tải, tôi đã chở hàng trên nóc thùng xe và bị cảnh sát dừng, tôi muốn biết số điểm bị trừ trên giấy phép lái xe của mình là bao nhiêu?", "as_of": "2026-11-03", "question_type": "tru_diem", "tier": "A", "answer": "Bạn sẽ bị trừ 02 điểm trên giấy phép lái xe. (Điều 21, Khoản 13, Nghị định 168/2024/NĐ-CP)", "gold_units": ["ND168-2024/D21/K13/a"], "required_numbers": [{"value": 2, "unit": "diem"}], "source": "llm:gpt-oss-20b+human", "draft_id": "WD-tru_diem-020:2"}
```

## ngoai_pham_vi — câu ngoài phạm vi (LLM viết theo nhóm chủ đề)

Kiểm kỹ: câu phải thật sự nằm ngoài dữ liệu (không văn bản nào trong danh mục trả lời).

