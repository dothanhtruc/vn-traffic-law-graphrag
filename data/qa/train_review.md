# Rà tay câu hỏi train (M9)

50 câu (xếp hạng sha256(seed:qid), seed 42) / 8,566 câu train · `train.jsonl` sha256 `2068aaef94c4`.

Tiêu chí: **Đ** = chunk trả lời được câu hỏi (positive đúng); **T** = câu tự nhiên, tự đứng được, không chép nguyên văn; **L** = loại câu đúng. Ghi ✓/✗ và nhận xét.

## Kết quả rà (Claude, 10/11/2026 — chờ người dùng xác nhận)

| Tiêu chí | Đạt |
| --- | ---: |
| Đ — positive đúng (chunk trả lời được câu hỏi) | 46/50 (92%) |
| T — câu tự nhiên, tự đứng được | 48/50 (96%) |
| L — nhãn loại câu đúng | 33/50 (66%) |

- Nhãn `question_type` của câu sinh chỉ để thống kê (Mistral hay gán `dinh_nghia`/`hanh_vi_cam_nghia_vu` cho câu thủ tục); không dùng khi fine-tune embedding/reranker.
- Lỗi positive còn lại: câu hỏi quá chung hoặc hỏi khía cạnh mà Khoản kề bên trả lời rõ hơn — không lọc được bằng rule; M14 nên dùng hard negative cùng Điều cẩn thận (câu có thể có nhiều positive hợp lệ).
- Quá trình: vòng 1 (mẫu ngẫu nhiên khác, 50 câu) Đ 45/50 · T 45/50 · L 32/50 → thêm lọc “Thông tư/Nghị định/Luật này”, bỏ số Khoản khỏi số được phép, đổi cách chọn mẫu sang xếp hạng băm; vòng 2 Đ 44/50 → thêm lọc `hoi_che_tai_khong_co` (hỏi trừ điểm/mức phạt mà chunk không có), 3 câu sai bị loại, 3 câu mới vào mẫu; vòng 3 (bảng này).

## 1. `gen-0219c7b15c85` · dinh_nghia · tier A · `TT79-2024-BCA/D12/K2#2025-01-01`

**Câu hỏi:** Có phải chứng từ tài chính của xe cũng được công nhận quyền sở hữu hợp pháp không?

> Điều 12. Chứng nhận quyền sở hữu hợp pháp
> 2. Quyết định của cơ quan có thẩm quyền hoặc văn bản chuyển nhượng, trao đổi, tặng cho, để thừa kế xe, chứng từ tài chính của xe theo quy định của pháp luật.

- Đ: ✓ · T: ✓ · L: ✗ · Nhận xét: loại đúng: thu_tuc_tham_quyen

## 2. `gen-04fb6393de9d` · hanh_vi_cam_nghia_vu · tier B · `ND336-2025/D25/K1#2026-03-01`

**Câu hỏi:** Là người dân, tôi muốn biết Nghị định số 336/2025/NĐ-CP đã bãi bỏ những điều nào của Nghị định số 100/2019/NĐ-CP về giao thông?

> Điều 25. Bãi bỏ một số điều, khoản, điểm của Nghị định số 100/2019/NĐ-CP ngày 30 tháng 12 năm 2019 của Chính phủ quy định xử phạt vi phạm hành chính trong lĩnh vực giao thông đường bộ và đường sắt được sửa đổi, bổ sung bởi Nghị định số 123/2021/NĐ-CP ngày 28 tháng 12 năm 2021 của Chính phủ, Nghị định số 168/2024/NĐ-CP ngày 26 tháng 12 năm 2024 của Chính phủ.
> 1. Bãi bỏ điểm a, b, d và điểm đ khoản 2; điểm b, c, d và điểm e khoản 3; khoản 4; điểm a, b khoản 5; điểm a, b, c, d, đ và điểm h khoản 6; điểm b khoản 8; khoản 9, 10 Điều 12.

- Đ: ✓ · T: ✗ · L: ✗ · Nhận xét: câu gượng (“Là người dân, tôi muốn biết…”), hỏi về văn bản bãi bỏ

## 3. `gen-0bc4edb2f46c` · thu_tuc_tham_quyen · tier A · `TT12-2025-BCA/D7/K1#2025-03-01`

**Câu hỏi:** Ai có quyền cấp thẻ sát hạch viên cho sĩ quan Công an?

> Điều 7. Tiêu chuẩn sát hạch viên, thư ký Hội đồng sát hạch
> 1. Tiêu chuẩn của sát hạch viên thuộc lực lượng Công an nhân dân
> a) Là sĩ quan thuộc lực lượng Công an nhân dân;
> b) Có giấy phép lái xe tương ứng với hạng xe sát hạch từ 03 năm trở lên, còn điểm, còn hiệu lực;
> c) Đã được Cục Cảnh sát giao thông tập huấn về nghiệp vụ sát hạch, kiểm tra đạt yêu cầu và cấp thẻ sát hạch viên. Thẻ sát hạch viên có thời hạn tối đa 03 năm và không quá thời hạn hiệu lực của giấy phép lái xe tương ứng hạng xe sát hạch của sát hạch viên.

- Đ: ✓ · T: ✓ · L: ✓ · Nhận xét: —

## 4. `gen-0e187cc99adb` · muc_phat · tier B · `ND336-2025/D10/K3#2026-03-01`

**Câu hỏi:** Ai bị phạt tiền nếu không phát hành chứng từ thu tiền đúng giá trị tại trạm thu phí?

> Điều 10. Xử phạt các hành vi vi phạm về thanh toán điện tử giao thông đường bộ, hoạt động trạm thu phí đường bộ
> 3. Phạt tiền từ 10.000.000 đồng đến 20.000.000 đồng đối với cá nhân, từ 20.000.000 đồng đến 40.000.000 đồng đối với tổ chức thực hiện một trong các hành vi vi phạm sau đây:
> a) Không thực hiện đúng quy trình quản lý, vận hành trạm thu phí theo quy định để xảy ra tai nạn giao thông đối với các phương tiện khi phương tiện tham gia giao thông qua trạm thu phí, trừ hành vi vi phạm quy định tại điểm c khoản 5 Điều này;
> b) Phát hành chứng từ thu tiền sử dụng đường bộ không đúng đối tượng, đúng giá trị cho từng đối tượng phải trả tại trạm thu phí;
> c) Xâm nhập hoặc tìm cách xâm nhập hệ thống thanh toán điện tử giao thông đường bộ;
> d) Phá hoại, đánh cắp dữ liệu hệ thống thanh toán điện tử giao thông đường bộ;
> đ) Làm thay đổi trái phép chương trình phần mềm, dữ liệu điện tử sử dụng trong …

- Đ: ✓ · T: ✓ · L: ✓ · Nhận xét: —

## 5. `gen-11526471f761` · hanh_vi_cam_nghia_vu · tier A · `LUAT35-2024/D18/K5#2025-01-01`

**Câu hỏi:** Khi lắp đặt biển tuyên truyền chính trị trên đường bộ, cần đáp ứng yêu cầu nào?

> Điều 18. Xây dựng, lắp đặt biển quảng cáo, biển thông tin cổ động, tuyên truyền chính trị trong phạm vi bảo vệ kết cấu hạ tầng đường bộ
> 5. Việc xây dựng, lắp đặt biển thông tin cổ động, tuyên truyền chính trị phải đáp ứng yêu cầu quy định tại khoản 2, khoản 3, điểm b và điểm c khoản 4 Điều này.

- Đ: ✓ · T: ✓ · L: ✓ · Nhận xét: chunk dẫn chiếu khoản khác cho chi tiết yêu cầu

## 6. `gen-12f7692f1482` · hanh_vi_cam_nghia_vu · tier A · `LUAT36-2024/D82/K5#2025-01-01`

**Câu hỏi:** Khi xảy ra tai nạn giao thông với hàng hóa nguy hiểm, cơ quan Công an phải tổ chức gì để đảm bảo an toàn giao thông?

> Điều 82. Cứu nạn, cứu hộ khi xảy ra vụ tai nạn giao thông đường bộ
> 5. Trường hợp tai nạn giao thông đường bộ liên quan đến phương tiện giao thông đường bộ chở hàng hóa nguy hiểm, cơ quan Công an chủ trì giải quyết vụ việc phải thông báo ngay cho đơn vị chức năng về giải quyết hóa chất độc hại, vật liệu cháy, nổ; phong tỏa hiện trường nơi xảy ra tai nạn giao thông đường bộ; tổ chức phân luồng giao thông, cấm người, phương tiện đi vào khu vực tai nạn.

- Đ: ✓ · T: ✓ · L: ✓ · Nhận xét: —

## 7. `gen-1927703dd866` · hanh_vi_cam_nghia_vu · tier B · `ND158-2024/D70/K2#2025-01-01`

**Câu hỏi:** Dữ liệu nào phải được chia sẻ giữa các bộ để quản lý vận tải đường bộ?

> Điều 70. Bộ Tài chính
> 2. Hướng dẫn việc thực hiện kết nối dữ liệu hóa đơn điện tử, hợp đồng vận tải điện tử, vé điện tử của các loại hình kinh doanh vận tải hành khách và hàng hóa bằng xe ô tô, bằng xe bốn bánh có gắn động cơ chia sẻ thông tin cho Bộ Giao thông vận tải để phối hợp quản lý.

- Đ: ✓ · T: ✓ · L: ✗ · Nhận xét: positive yếu (Bộ Tài chính hướng dẫn kết nối dữ liệu); loại: thu_tuc

## 8. `gen-263a314e5755` · dinh_nghia · tier A · `LUAT36-2024/D37/K2#2025-01-01`

**Câu hỏi:** Giá khởi điểm đấu giá biển số xe ô tô là bao nhiêu?

> Điều 37. Đấu giá biển số xe
> 2. Giá khởi điểm của một biển số xe ô tô đưa ra đấu giá không thấp hơn 40 triệu đồng; giá khởi điểm một biển số xe mô tô, xe gắn máy đưa ra đấu giá không thấp hơn 05 triệu đồng.

- Đ: ✓ · T: ✓ · L: ✗ · Nhận xét: loại: khac

## 9. `gen-26ceba2dc49b` · thu_tuc_tham_quyen · tier A · `TT79-2024-BCA/D8/K1#2025-01-01`

**Câu hỏi:** Làm sao để cấp mới chứng nhận đăng ký xe và biển số xe cơ giới?

> Điều 8. Hồ sơ cấp mới chứng nhận đăng ký xe, biển số xe
> 1. Giấy khai đăng ký xe.

- Đ: ✓ · T: ✓ · L: ✓ · Nhận xét: chunk chỉ là 1 thành phần hồ sơ

## 10. `gen-2a19fb2d9cbb` · hanh_vi_cam_nghia_vu · tier B · `ND158-2024/D42/K1#2025-01-01`

**Câu hỏi:** Phương tiện của Lào và Campuchia quá hạn lưu hành ở Việt Nam được gia hạn được không?

> Điều 42. Gia hạn thời gian lưu hành tại Việt Nam cho phương tiện của Lào, Campuchia
> 1. Đối tượng: phương tiện của Lào, Campuchia quá thời gian lưu hành tại Việt Nam quy định tại giấy phép liên vận trong trường hợp bất khả kháng được gia hạn 01 lần với thời gian không quá 10 ngày.

- Đ: ✓ · T: ✓ · L: ✗ · Nhận xét: loại: thu_tuc

## 11. `gen-2ac579e5b077` · thu_tuc_tham_quyen · tier A · `TT65-2024-BCA/D7/K3#2025-01-01`

**Câu hỏi:** Khi kiểm tra lại, cần nộp gì nếu giấy khám sức khỏe còn hiệu lực?

> Điều 7. Đăng ký, tổ chức kiểm tra kiến thức pháp luật về trật tự, an toàn giao thông đường bộ
> 3. Người đăng ký kiểm tra có thể nộp hồ sơ cho cơ quan có thẩm quyền kiểm tra quy định tại Điều 4 Thông tư này tại nơi thường trú, tạm trú, nơi ở hiện tại.
> Người có kết quả kiểm tra không đạt yêu cầu có thể đăng ký kiểm tra lại tại cơ quan có thẩm quyền đã tổ chức kiểm tra trước đó hoặc lựa chọn cơ quan có thẩm quyền kiểm tra để đề nghị kiểm tra lại. Trường hợp đề nghị kiểm tra lại, nếu giấy khám sức khỏe còn giá trị sử dụng thì người đăng ký kiểm tra chỉ gửi đơn đề nghị kiểm tra.

- Đ: ✓ · T: ✓ · L: ✓ · Nhận xét: —

## 12. `gen-2ce303aacd22` · dinh_nghia · tier B · `ND158-2024/D4/K5#2025-01-01`

**Câu hỏi:** Xe trung chuyển hành khách được phép chở tối đa bao nhiêu người không kể chỗ lái xe?

> Điều 4. Kinh doanh vận tải hành khách bằng xe ô tô theo tuyến cố định
> 5. Xe ô tô sử dụng để vận tải trung chuyển hành khách
> a) Sử dụng xe ô tô chở người đến 29 chỗ (không kể chỗ của người lái xe);
> b) Phải có phù hiệu “XE TRUNG CHUYỂN” theo Mẫu số 02 Phụ lục XIII kèm theo Nghị định này và được dán cố định tại góc trên bên phải ngay sát phía dưới vị trí của Tem kiểm định, mặt trong kính chắn gió phía trước của xe; phải được niêm yết đầy đủ các thông tin trên xe;
> c) Chỉ được hoạt động vận tải trung chuyển hành khách trong phạm vi địa bàn địa phương (cấp tỉnh) nơi cấp phù hiệu “XE TRUNG CHUYỂN”.

- Đ: ✓ · T: ✓ · L: ✗ · Nhận xét: loại: khac

## 13. `gen-2d1bd9d71f19` · dinh_nghia · tier A · `TT38-2024-BGTVT/D5/K5#2025-01-01`

**Câu hỏi:** Điều 5 của Thông tư số 38/2024/TT-BGTVT nói về gì về tốc độ thiết kế đường giao thông nông thôn?

> Điều 5. Tốc độ thiết kế của đường bộ
> 5. Tốc độ thiết kế đường giao thông nông thôn được xác định theo Tiêu chuẩn quốc gia TCVN 10380:2014 Đường giao thông nông thôn - Yêu cầu thiết kế.

- Đ: ✓ · T: ✗ · L: ✗ · Nhận xét: hỏi “Điều 5 … nói về gì” — không tự nhiên

## 14. `gen-2d33660455a5` · thu_tuc_tham_quyen · tier B · `ND165-2024/D60/K1#2025-01-01`

**Câu hỏi:** Ai có trách nhiệm cung cấp thông tin cho cơ sở dữ liệu đường bộ?

> Điều 60. Thu thập, cập nhật, điều chỉnh thông tin trong cơ sở dữ liệu đường bộ
> 1. Thông tin quy định tại khoản 1 Điều 57 của Nghị định này được trích, chọn và đồng bộ hóa từ cơ sở dữ liệu, cơ sở dữ liệu chuyên ngành của Bộ Giao thông vận tải, Bộ Kế hoạch và Đầu tư.

- Đ: ✓ · T: ✓ · L: ✓ · Nhận xét: —

## 15. `gen-339495d739fc` · hanh_vi_cam_nghia_vu · tier A · `TT38-2024-BGTVT/D10/K4#2025-01-01`

**Câu hỏi:** Tốc độ khai thác trên đường cấp IV, cấp V, cấp VI được quy định khi nào?

> Điều 10. Đặt biển báo tốc độ khai thác
> 4. Cơ quan quản lý đường bộ có thẩm quyền quy định tại khoản 3 Điều này chủ trì, phối hợp với lực lượng cảnh sát giao thông trên tuyến, Ủy ban nhân cấp huyện nơi có đoạn đường cần đặt biển báo tốc độ cho phép để xem xét, quyết định tốc độ khai thác cho phép và tổ chức thực hiện đặt biển báo tốc độ trong các trường hợp sau:
> a) Đường bộ đang khai thác nằm trong khu vực đông dân cư có điều kiện bất lợi (đường một chiều hoặc đường hai chiều có tổng bề rộng phần xe chạy nhỏ hơn 3,0m và tập trung công trình hạ tầng liên tiếp, sát mép phần xe chạy, tầm nhìn hạn chế).
> b) Đường bộ đang khai thác nằm ngoài khu vực đông dân cư thuộc các đoạn đường cấp IV, cấp V, cấp VI và các đoạn đường theo cấp kỹ thuật quy định tại điểm d khoản 2 Điều 10 Luật Đường bộ, có điều kiện bất lợi, tiềm ẩn nguy cơ xảy ra mất an toàn giao thông (bán kính đường cong nhỏ, đường cong …

- Đ: ✓ · T: ✓ · L: ✗ · Nhận xét: loại: thu_tuc

## 16. `gen-3726dce8c564` · dinh_nghia · tier historical · `TT35-2024-BGTVT/D3/K1#2025-01-01`

**Câu hỏi:** Theo Thông tư 35/2024, thời gian lái xe an toàn có liên quan đến việc tránh tai nạn nào?

> Điều 3. Giải thích từ ngữ
> 1. Thời gian lái xe an toàn là thời gian người có giấy phép lái xe có hiệu lực, không để xảy ra tai nạn giao thông đường bộ gây hậu quả nghiêm trọng hoặc đặc biệt nghiêm trọng.

- Đ: ✓ · T: ✓ · L: ✓ · Nhận xét: tier historical (TT35)

## 17. `gen-384297434291` · hanh_vi_cam_nghia_vu · tier A · `TT79-2024-BCA/D12/K1#2025-01-01`

**Câu hỏi:** Có thể dùng hóa đơn giấy để chứng nhận quyền sở hữu xe không?

> Điều 12. Chứng nhận quyền sở hữu hợp pháp
> 1. Dữ liệu hóa đơn điện tử được hệ thống đăng ký, quản lý xe tiếp nhận từ cổng dịch vụ công hoặc cơ sở dữ liệu của cơ quan quản lý thuế. Trường hợp xe chưa có dữ liệu hoá đơn điện tử thì phải có hóa đơn giấy hoặc hóa đơn được chuyển đổi từ hóa đơn điện tử sang hóa đơn giấy theo quy định của pháp luật.

- Đ: ✓ · T: ✓ · L: ✗ · Nhận xét: loại: thu_tuc

## 18. `gen-43ba67b338d6` · dinh_nghia · tier B · `TT69-2024-BCA/D9/K1#2025-01-01`

**Câu hỏi:** Hệ thống đèn tín hiệu giao thông phải đáp ứng yêu cầu nào về quản lý và điều hành?

> Điều 9. Quản lý, vận hành, khai thác hệ thống đèn tín hiệu giao thông đường bộ
> 1. Hệ thống đèn tín hiệu giao thông đường bộ phải được kết nối dữ liệu với Trung tâm chỉ huy giao thông để đáp ứng các yêu cầu về quản lý, điều hành, chỉ huy, chỉ đạo và thống kê trong công tác bảo đảm trật tự, an toàn giao thông.

- Đ: ✓ · T: ✓ · L: ✗ · Nhận xét: loại: hanh_vi_cam_nghia_vu

## 19. `gen-49635942b082` · bien_phap · tier B · `TT69-2024-BCA/D7/K6#2025-01-01`

**Câu hỏi:** Thông tư số 69/2024/TT-BCA quy định mẫu nào cho động tác báo hiệu xe bên phải đi nhanh hơn?

> Điều 7. Các biểu mẫu trong công tác chỉ huy, điều khiển giao thông đường bộ
> 6. Mẫu động tác báo hiệu bên phải đi nhanh hơn (mẫu số 06).

- Đ: ✓ · T: ✓ · L: ✗ · Nhận xét: loại: khac (không phải biện pháp)

## 20. `gen-4b646b484634` · dinh_nghia · tier A · `ND151-2024/D11/K6#2025-01-01`

**Câu hỏi:** Chứng chỉ bồi dưỡng kiến thức pháp luật giao thông chứa những thông tin nào?

> Điều 11. Thông tin trong Cơ sở dữ liệu về trật tự, an toàn giao thông đường bộ
> 6. Thông tin về đào tạo, sát hạch, cấp giấy phép lái xe; chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ:
> a) Họ, tên; số định danh cá nhân; ngày, tháng, năm sinh; quốc tịch; nơi cư trú; số giấy phép lái xe; xác nhận hoàn thành khóa đào tạo; cơ sở đào tạo lái xe; hạng xe đào tạo; khoá đào tạo; ngày, tháng, năm trúng tuyển; cơ quan sát hạch; địa điểm tổ chức sát hạch (trung tâm sát hạch hoặc sân tập lái dùng để sát hạch); ngày, tháng, năm cấp, đổi, cấp lại giấy phép lái xe; cơ quan cấp, đổi, cấp lại giấy phép lái xe; hạng giấy phép lái xe; thời hạn sử dụng của giấy phép lái xe; số phôi giấy phép lái xe;
> b) Họ, tên; ngày, tháng, năm sinh; khóa đào tạo; thời gian hoàn thành khóa học; kết quả kiểm tra cấp chứng chỉ; ngày, tháng, năm đạt kết quả kiểm tra cấp chứng chỉ; số chứng chỉ; ngày, tháng, năm …

- Đ: ✓ · T: ✓ · L: ✓ · Nhận xét: —

## 21. `gen-4d7366ebfb42` · thu_tuc_tham_quyen · tier B · `ND165-2024/D47/K3#2026-07-01`

**Câu hỏi:** Khi mở rộng hoặc nâng cấp đường cao tốc, cơ quan nào có quyền ký kết hợp đồng sau khi dự án được điều chỉnh?

> Điều 47. Mở rộng, nâng cấp đường cao tốc hoặc đường bộ đang khai thác nâng cấp thành đường cao tốc trong trường hợp nhà đầu tư hiện hữu đề xuất điều chỉnh dự án
> 3. Căn cứ quyết định phê duyệt điều chỉnh dự án, cơ quan ký kết hợp đồng tổ chức đàm phán, sửa đổi hợp đồng theo pháp luật về đầu tư theo phương thức đối tác công tư.

- Đ: ✓ · T: ✓ · L: ✓ · Nhận xét: —

## 22. `gen-4f701a068960` · thu_tuc_tham_quyen · tier B · `ND165-2024/D21/K3#2025-01-01`

**Câu hỏi:** Có bao nhiêu bộ hồ sơ cần chuẩn bị khi xin phép sử dụng lòng đường và vỉa hè?

> Điều 21. Sử dụng tạm thời lòng đường, vỉa hè vào mục đích khác
> 3. Thành phần hồ sơ đề nghị sử dụng lòng đường, vỉa hè vào mục đích khác bao gồm:
> a) Văn bản đề nghị cấp phép sử dụng tạm thời lòng đường, vỉa hè vào mục đích khác (bản chính) theo Mẫu số 01 Phụ lục IV kèm theo Nghị định này;
> b) Phương án sử dụng tạm thời lòng đường vỉa hè vào mục đích khác, phương án tổ chức giao thông (bản chính hoặc bản sao có chứng thực) quy định tại khoản 2 Điều này;
> c) Số lượng hồ sơ: 01 bộ.

- Đ: ✓ · T: ✓ · L: ✓ · Nhận xét: —

## 23. `gen-544b64f1ef41` · thu_tuc_tham_quyen · tier B · `TT73-2024-BCA/D10/K4#2025-01-01`

**Câu hỏi:** Kế hoạch tuần tra của các tổ Cảnh sát giao thông được phê duyệt bởi ai?

> Điều 10. Xây dựng, ban hành kế hoạch tuần tra, kiểm soát
> 4. Đội trưởng các Đội: Đội Cảnh sát giao thông đường bộ cao tốc; Đội Cảnh sát giao thông; Đội Cảnh sát giao thông đường bộ; Đội Tuần tra, dẫn đoàn; Đội Cảnh sát giao thông, trật tự; Trạm trưởng Trạm Cảnh sát giao thông xây dựng kế hoạch công tác tuần và phê duyệt kế hoạch tuần tra, kiểm soát cho các Tổ Cảnh sát giao thông trực thuộc (theo mẫu quy định của Bộ Công an).

- Đ: ✓ · T: ✓ · L: ✓ · Nhận xét: —

## 24. `gen-551fc21f859c` · dinh_nghia · tier A · `ND151-2024/D11/K8#2026-07-01`

**Câu hỏi:** Thông tin về xe ô tô bao gồm những gì trong cơ sở dữ liệu?

> Điều 11. Thông tin trong Cơ sở dữ liệu về trật tự, an toàn giao thông đường bộ
> 8. Thông tin về bảo hiểm bắt buộc trách nhiệm dân sự của chủ xe cơ giới, xe máy chuyên dùng:
> a) Thông tin về chủ sở hữu xe cơ giới, xe máy chuyên dùng:
> Đối với cá nhân: họ, tên; ngày, tháng, năm sinh; giới tính; số định danh cá nhân; số điện thoại (nếu có); quốc tịch; nơi thường trú; nơi tạm trú, nơi ở hiện tại, địa chỉ đăng ký xe.
> Đối với tổ chức: tên tổ chức; tên người đại diện hợp pháp; địa chỉ; mã số thuế hoặc quyết định thành lập hoặc số định danh của tổ chức (nếu có); số điện thoại;
> b) Thông tin về xe cơ giới: biển số xe hoặc số khung, số máy, loại xe, trọng tải (đối với xe ô tô), số chỗ ngồi (đối với xe ô tô), mục đích sử dụng xe (đối với xe ô tô), nhãn hiệu, dung tích, màu sơn, năm sản xuất;
> c) Thông tin về doanh nghiệp bảo hiểm: tên, địa chỉ, số điện thoại đường dây nóng;
> d) Mức trách nhiệm bảo hiểm …

- Đ: ✗ · T: ✓ · L: ✓ · Nhận xét: câu quá chung; Khoản 8 là thông tin bảo hiểm, positive hợp lý hơn là Khoản 1

## 25. `gen-57716e3a6aa7` · thu_tuc_tham_quyen · tier C · `TT72-2024-BCA/D15/K1#2025-01-01`

**Câu hỏi:** Cần chuẩn bị gì để dựng lại hiện trường vụ tai nạn giao thông?

> Điều 15. Dựng lại hiện trường vụ tai nạn giao thông đường bộ
> 1. Trong quá trình điều tra, xác minh vụ tai nạn giao thông đường bộ, nếu có căn cứ xác định hiện trường bị xáo trộn, hiện trường giả hoặc xét thấy cần thiết cho việc điều tra, xác minh, giải quyết vụ tai nạn giao thông đường bộ thì tổ chức dựng lại hiện trường vụ tai nạn giao thông đường bộ để điều tra, xác minh. Việc dựng lại hiện trường phải có Kế hoạch dựng lại hiện trường theo Mẫu số 16/TNĐB ban hành kèm theo Thông tư này và được lãnh đạo có thẩm quyền phê duyệt.

- Đ: ✓ · T: ✓ · L: ✓ · Nhận xét: —

## 26. `gen-5a902a58f90c` · hanh_vi_cam_nghia_vu · tier B · `TT52-2024-BGTVT/D4/K7#2025-01-01`

**Câu hỏi:** Xe mô tô và xe gắn máy cần phải có camera ghi hình phía trước thôi phải không?

> Điều 4. Yêu cầu kỹ thuật chung
> 7. Xe ô tô, xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ, xe máy chuyên dùng (trừ rơ moóc, sơ mi rơ moóc được kéo bởi máy kéo), xe mô tô, gắn máy phải được trang bị thiết bị theo dõi hành trình đảm bảo ghi nhận được hành trình xe chạy, tốc độ xe chạy; camera hành trình đảm bảo ghi nhận hình ảnh phía trước và phía sau xe khi lưu thông trên đường (trừ xe mô tô, xe gắn máy camera hành trình đảm bảo ghi nhận hình ảnh phía trước xe). Các thiết bị này phải được hoạt động trong toàn bộ thời gian xe chạy thử trên đường.

- Đ: ✓ · T: ✓ · L: ✓ · Nhận xét: —

## 27. `gen-5fed386383a3` · muc_phat · tier B · `ND336-2025/D7/K2#2026-03-01`

**Câu hỏi:** Cơ sở đào tạo thẩm tra viên không lưu trữ hồ sơ học viên sẽ bị phạt bao nhiêu tiền?

> Điều 7. Xử phạt hành vi vi phạm quy định về đào tạo thẩm tra viên, điều kiện kinh doanh dịch vụ thẩm tra an toàn giao thông đường bộ
> 2. Phạt tiền từ 8.000.000 đồng đến 10.000.000 đồng đối với cơ sở đào tạo thẩm tra viên an toàn giao thông đường bộ thực hiện một trong các hành vi vi phạm sau đây:
> a) Tuyển sinh, đào tạo học viên không đủ điều kiện tiêu chuẩn theo quy định;
> b) Không thông báo kế hoạch đào tạo và danh sách học viên trước khi mở lớp theo quy định;
> c) Đào tạo thẩm tra viên an toàn giao thông đường bộ không đúng chương trình khung, kế hoạch đào tạo đã thông báo theo quy định;
> d) Công nhận kết quả thi cho người không tham dự thi hoặc không tham dự khóa đào tạo thẩm tra viên an toàn giao thông đường bộ;
> đ) Không thành lập hoặc thành lập hội đồng thi không đúng quy định;
> e) Không lưu trữ, bảo quản hồ sơ học viên theo quy định, trừ hành vi vi phạm quy định tại điểm g khoản này;
> g) …

- Đ: ✓ · T: ✓ · L: ✓ · Nhận xét: —

## 28. `gen-60f42b81c277` · thu_tuc_tham_quyen · tier A · `TT79-2024-BCA/D4/K6#2025-01-01`

**Câu hỏi:** Cơ quan đăng ký xe có trách nhiệm gì về thủ tục đăng ký xe?

> Điều 4. Cơ quan đăng ký xe
> 6. Cơ quan đăng ký xe có trách nhiệm bảo đảm cơ sở vật chất, bố trí địa điểm thuận tiện để tiếp nhận, giải quyết hồ sơ, thủ tục đăng ký xe. Địa điểm đăng ký xe phải có sơ đồ chỉ dẫn, thời gian làm việc, biển chức danh của cán bộ đăng ký xe, có chỗ ngồi, chỗ để xe, có hòm thư góp ý và niêm yết công khai các quy định về thủ tục đăng ký xe, lệ phí đăng ký xe.

- Đ: ✓ · T: ✓ · L: ✓ · Nhận xét: —

## 29. `gen-61ccd6bbad1f` · hanh_vi_cam_nghia_vu · tier B · `ND165-2024/D36/K1#2025-01-01`

**Câu hỏi:** Cơ sở đào tạo thẩm tra viên giao thông cần có những thiết bị âm thanh nào?

> Điều 36. Điều kiện của cơ sở kinh doanh đào tạo thẩm tra viên an toàn giao thông đường bộ
> 1. Về cơ sở vật chất
> a) Bảo đảm phòng học có diện tích tối thiểu đạt 1,5 m2/chỗ học, có thiết bị âm thanh, nghe nhìn, gồm: màn chiếu, máy chiếu, máy vi tính, bộ tăng âm, micro kèm loa;
> b) Phương tiện, thiết bị phục vụ giảng dạy và học tập ngoài hiện trường, tối thiểu có: 50 áo phản quang, 01 máy đo độ phản quang của biển báo hoặc sơn kẻ đường.

- Đ: ✓ · T: ✓ · L: ✗ · Nhận xét: loại: thu_tuc (điều kiện)

## 30. `gen-6353fd87517b` · muc_phat · tier A · `ND168-2024/D20/K3#2025-01-01`

**Câu hỏi:** Tôi lái xe khách không đóng cửa lên xuống khi chạy, bị phạt bao nhiêu tiền?

> Điều 20. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô chở hành khách, ô tô chở người và các loại xe tương tự xe ô tô chở hành khách vi phạm quy định về bảo đảm trật trị, an toàn giao thông
> 3. Phạt tiền từ 600.000 đồng đến 800.000 đồng đối với một trong các hành vi vi phạm sau đây:
> a) Không đóng cửa lên xuống khi xe đang chạy;
> b) Để người ngồi trên xe khi xe xuống phà, đang trên phà và khi lên bến (trừ người lái xe, trẻ em, phụ nữ mang thai, người già yếu, người bệnh, người khuyết tật);
> c) Không chạy đúng tuyến đường, lịch trình, hành trình vận tải được phép hoạt động theo quy định;
> d) Để người mắc võng nằm trên xe khi xe đang chạy;
> đ) Sắp xếp, chằng buộc hành lý, hàng hóa không bảo đảm an toàn; để rơi hành lý, hàng hóa trên xe xuống đường; để hàng hóa trong khoang chở hành khách;
> e) Chở hành lý, hàng hóa vượt quá kích thước bao ngoài của xe;
> g) Điều khiển xe vận tải …

- Đ: ✓ · T: ✓ · L: ✓ · Nhận xét: —

## 31. `gen-7505d0516f7c` · dinh_nghia · tier A · `LUAT35-2024/D56/K8#2025-01-01`

**Câu hỏi:** Xe buýt công cộng phải có bao nhiêu chỗ ngồi trở lên để vận chuyển hành khách?

> Điều 56. Hoạt động vận tải đường bộ
> 8. Kinh doanh vận tải hành khách công cộng bằng xe buýt là loại hình kinh doanh vận tải hành khách sử dụng xe ô tô chở người từ 08 chỗ trở lên (không kể chỗ của người lái xe) để vận tải hành khách, có xác định điểm đầu, điểm cuối, các điểm dừng xe để đón, trả khách với lịch trình, hành trình xác định; bao gồm tuyến xe buýt nội tỉnh, tuyến xe buýt liên tỉnh, cụ thể như sau:
> a) Tuyến xe buýt nội tỉnh là tuyến xe buýt có phạm vi hoạt động trên địa bàn của một tỉnh, thành phố trực thuộc trung ương;
> b) Tuyến xe buýt liên tỉnh là tuyến xe buýt có phạm vi hoạt động trên địa bàn từ 02 tỉnh, thành phố trực thuộc trung ương trở lên.

- Đ: ✓ · T: ✓ · L: ✗ · Nhận xét: loại: khac

## 32. `gen-79d5a4d268a6` · thu_tuc_tham_quyen · tier A · `LUAT35-2024/D52/K4#2025-01-01`

**Câu hỏi:** Ai có quyền xác định vị trí và quy mô của trạm dừng nghỉ?

> Điều 52. Trạm dừng nghỉ, điểm dừng xe, đỗ xe
> 4. Vị trí, quy mô trạm dừng nghỉ, điểm dừng xe, đỗ xe được xác định khi lập dự án, thiết kế xây dựng.

- Đ: ✗ · T: ✓ · L: ✓ · Nhận xét: hỏi “ai”, chunk chỉ nêu “khi lập dự án”

## 33. `gen-82a51661cefb` · hanh_vi_cam_nghia_vu · tier historical · `TT35-2024-BGTVT/D43/K3#2025-01-01`

**Câu hỏi:** Giấy phép lái xe quốc gia không được cơ quan có thẩm quyền cấp thì có được cấp giấy phép lái xe quốc tế không?

> Điều 43. Cấp giấy phép lái xe quốc tế
> 3. Không cấp IDP đối với các trường hợp sau đây:
> a) Giấy phép lái xe quốc gia bị tẩy xóa không còn đủ các thông tin cần thiết hoặc có sự khác biệt về nhận dạng;
> b) Giấy phép lái xe quốc gia không do cơ quan có thẩm quyền cấp theo quy định.

- Đ: ✓ · T: ✓ · L: ✓ · Nhận xét: —

## 34. `gen-84186ee26162` · hanh_vi_cam_nghia_vu · tier A · `LUAT35-2024/D30/K3#2025-01-01`

**Câu hỏi:** Khi kết nối đường nhánh vào đường chính, cần đáp ứng những tiêu chí nào về thiết kế và xây dựng?

> Điều 30. Kết nối giao thông đường bộ
> 3. Việc kết nối đường nhánh vào đường chính và giữa các tuyến đường với nhau, được thực hiện tại vị trí đấu nối và phải bảo đảm các yêu cầu sau đây:
> a) Vị trí đấu nối được thiết kế, xây dựng tuân thủ quy chuẩn, tiêu chuẩn kỹ thuật; phù hợp với cấp đường và bảo đảm an toàn giao thông, năng lực thông hành của tuyến đường;
> b) Trường hợp đấu nối đường khác với đường cao tốc, ngoài việc thực hiện quy định tại điểm a và điểm c khoản này, khoảng cách giữa các vị trí đấu nối phải tuân thủ quy chuẩn, tiêu chuẩn kỹ thuật về thiết kế đường cao tốc;
> c) Việc kết nối giao thông đường bộ thực hiện theo quy định của Chính phủ.

- Đ: ✓ · T: ✓ · L: ✓ · Nhận xét: —

## 35. `gen-9efb73a3fa1f` · dinh_nghia · tier A · `ND151-2024/D11/K2#2025-01-01`

**Câu hỏi:** Xe cơ giới và xe máy chuyên dùng phải ghi lại những thông số kỹ thuật nào khi đăng kiểm?

> Điều 11. Thông tin trong Cơ sở dữ liệu về trật tự, an toàn giao thông đường bộ
> 2. Thông tin về đăng kiểm xe cơ giới, xe máy chuyên dùng:
> a) Thông số kỹ thuật của xe: loại xe; nhãn hiệu; số loại; màu sơn; số máy; số khung; số chỗ ngồi; số chỗ đứng; số chỗ nằm; khối lượng hàng cho phép chở; khối lượng toàn bộ; khối lượng kéo theo, khối lượng bản thân; dung tích xi lanh; công suất; loại năng lượng; năm sản xuất; nước sản xuất; chiều dài cơ sở; kích thước bao; kích thước thùng; công thức bánh xe; vết bánh xe; số lượng lốp, kích cỡ lốp và các thông số kỹ thuật khác của xe; thông tin của xe trước và sau cải tạo;
> b) Thông tin quản lý đăng kiểm: biển số xe; màu biển số; số, ngày, tháng, năm cấp, cơ quan cấp chứng nhận đăng ký xe (nếu có); số, ngày, tháng, năm cấp, cơ quan cấp chứng nhận chất lượng an toàn kỹ thuật và bảo vệ môi trường xe sản xuất, lắp ráp, nhập khẩu, cải tạo; số, ngày, tháng, …

- Đ: ✓ · T: ✓ · L: ✗ · Nhận xét: loại: khac

## 36. `gen-a7cc423354ac` · dinh_nghia · tier historical · `TT35-2024-BGTVT/D3/K9#2025-01-01`

**Câu hỏi:** Giấy phép lái xe và chứng chỉ bồi dưỡng kiến thức pháp luật được quản lý thông tin như nào?

> Điều 3. Giải thích từ ngữ
> 9. Hệ thống thông tin về đào tạo, sát hạch, cấp giấy phép lái xe, chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ là tập hợp phần cứng, đường truyền và phần mềm phục vụ công tác quản lý thông tin về đào tạo, sát hạch, cấp giấy phép lái xe, chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ; bao gồm: Hệ thống thông tin đào tạo lái xe, hệ thống thông tin sát hạch lái xe, hệ thống thông tin giấy phép lái xe và hệ thống thông tin cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ.

- Đ: ✓ · T: ✓ · L: ✓ · Nhận xét: —

## 37. `gen-aaeb66e8fed9` · muc_phat · tier B · `ND336-2025/D7/K2#2026-03-01`

**Câu hỏi:** Mức phạt tiền cho cơ sở đào tạo thẩm tra viên tuyển sinh học viên không đủ điều kiện là bao nhiêu?

> Điều 7. Xử phạt hành vi vi phạm quy định về đào tạo thẩm tra viên, điều kiện kinh doanh dịch vụ thẩm tra an toàn giao thông đường bộ
> 2. Phạt tiền từ 8.000.000 đồng đến 10.000.000 đồng đối với cơ sở đào tạo thẩm tra viên an toàn giao thông đường bộ thực hiện một trong các hành vi vi phạm sau đây:
> a) Tuyển sinh, đào tạo học viên không đủ điều kiện tiêu chuẩn theo quy định;
> b) Không thông báo kế hoạch đào tạo và danh sách học viên trước khi mở lớp theo quy định;
> c) Đào tạo thẩm tra viên an toàn giao thông đường bộ không đúng chương trình khung, kế hoạch đào tạo đã thông báo theo quy định;
> d) Công nhận kết quả thi cho người không tham dự thi hoặc không tham dự khóa đào tạo thẩm tra viên an toàn giao thông đường bộ;
> đ) Không thành lập hoặc thành lập hội đồng thi không đúng quy định;
> e) Không lưu trữ, bảo quản hồ sơ học viên theo quy định, trừ hành vi vi phạm quy định tại điểm g khoản này;
> g) …

- Đ: ✓ · T: ✓ · L: ✓ · Nhận xét: —

## 38. `gen-b0564380505b` · dinh_nghia · tier A · `LUAT36-2024/D71/K2#2025-01-01`

**Câu hỏi:** Hệ thống giám sát giao thông đường bộ có bao gồm những gì?

> Điều 71. Hệ thống giám sát bảo đảm an ninh, trật tự, an toàn giao thông đường bộ; hệ thống quản lý dữ liệu thiết bị giám sát hành trình và thiết bị ghi nhận hình ảnh người lái xe; hệ thống thiết bị kỹ thuật nghiệp vụ kiểm tra tải trọng xe cơ giới
> 2. Hệ thống quản lý dữ liệu thiết bị giám sát hành trình và thiết bị ghi nhận hình ảnh người lái xe dùng để ghi, lưu trữ, truyền phát thông tin, dữ liệu về hành trình của phương tiện tham gia giao thông đường bộ và hình ảnh của người lái xe, phục vụ công tác bảo đảm an ninh, trật tự, an toàn giao thông đường bộ và xử lý hành vi vi phạm pháp luật, quản lý nhà nước về vận tải đường bộ; do lực lượng Cảnh sát giao thông quản lý, vận hành, sử dụng; được kết nối, chia sẻ với cơ quan quản lý đường bộ và các cơ quan liên quan.

- Đ: ✗ · T: ✓ · L: ✓ · Nhận xét: Khoản 2 là hệ thống dữ liệu giám sát hành trình; câu hỏi hợp Khoản 1

## 39. `gen-b9336333c20d` · hanh_vi_cam_nghia_vu · tier A · `ND151-2024/D19/K2#2025-01-01`

**Câu hỏi:** Xe cứu thương đi cấp cứu được phép dùng tín hiệu gì?

> Điều 19. Tín hiệu, yêu cầu kỹ thuật đối với thiết bị phát tín hiệu của xe ưu tiên
> 2. Tín hiệu được sử dụng đối với thiết bị phát tín hiệu của xe ưu tiên:
> a) Tín hiệu xe chữa cháy của Cảnh sát phòng cháy, chữa cháy và cứu nạn, cứu hộ và xe chữa cháy của các lực lượng khác được huy động đi làm nhiệm vụ chữa cháy bao gồm: tín hiệu đèn nhấp nháy màu đỏ, tín hiệu còi ưu tiên;
> b) Tín hiệu xe của lực lượng quân sự đi làm nhiệm vụ khẩn cấp bao gồm: tín hiệu đèn nhấp nháy màu đỏ, tín hiệu còi ưu tiên, cờ hiệu quân sự;
> c) Tín hiệu xe của lực lượng công an, xe của lực lượng kiểm sát đi làm nhiệm vụ khẩn cấp bao gồm: tín hiệu đèn nhấp nháy màu xanh và đỏ, tín hiệu còi ưu tiên;
> d) Tín hiệu xe Cảnh sát giao thông dẫn đường bao gồm: tín hiệu đèn nhấp nháy màu xanh và đỏ, tín hiệu còi ưu tiên, cờ hiệu công an;
> đ) Tín hiệu xe cứu thương đi làm nhiệm vụ cấp cứu bao gồm: tín hiệu đèn; nhấp nháy màu đỏ, …

- Đ: ✓ · T: ✓ · L: ✓ · Nhận xét: xe cứu thương nằm ở điểm sau của Khoản (đoạn trích bị cắt)

## 40. `gen-c5fdda6b119c` · hanh_vi_cam_nghia_vu · tier C · `TT83-2024-BCA/D7/K1#2025-01-01`

**Câu hỏi:** Thông tin từ hệ thống giám sát giao thông có thể được sử dụng để xử lý những loại vi phạm nào?

> Điều 7. Khai thác, sử dụng hệ thống giám sát giao thông
> 1. Đơn vị quản lý, vận hành hệ thống giám sát giao thông thực hiện khai thác, sử dụng thông tin, dữ liệu của hệ thống giám sát giao thông phục vụ giám sát tình hình an ninh, trật tự, an toàn giao thông đường bộ; phát hiện, xử lý vi phạm pháp luật về trật tự, an toàn giao thông đường bộ và vi phạm pháp luật khác theo quy định của pháp luật.

- Đ: ✓ · T: ✓ · L: ✓ · Nhận xét: —

## 41. `gen-ce886352a8c3` · hanh_vi_cam_nghia_vu · tier B · `ND165-2024/D52a/K1#2026-07-01`

**Câu hỏi:** Ai được hưởng lợi từ việc đầu tư mở rộng trạm dừng nghỉ theo Nghị định 165/2024/NĐ-CP?

> Điều 52a. Đầu tư mở rộng trạm dừng nghỉ đã ký hợp đồng kinh doanh, khai thác
> 1. Việc đầu tư mở rộng trạm dừng nghỉ nhằm hoàn thiện hệ thống kết cấu hạ tầng, đáp ứng nhu cầu sử dụng dịch vụ của người và phương tiện tham gia giao thông.

- Đ: ✓ · T: ✓ · L: ✓ · Nhận xét: positive yếu

## 42. `gen-cfed5618f873` · thu_tuc_tham_quyen · tier A · `TT79-2024-BCA/D9/K1#2025-01-01`

**Câu hỏi:** Nếu chủ xe không có ký số, phải làm sao với giấy khai đăng ký xe?

> Điều 9. Giấy khai đăng ký xe
> 1. Trường hợp thực hiện đăng ký xe bằng dịch vụ công trực tuyến một phần: Chủ xe đăng nhập trên cổng dịch vụ công và kê khai chính xác, đầy đủ, trung thực các nội dung quy định trong mẫu giấy khai đăng ký xe, ký số. Trường hợp không có ký số thì chủ xe in giấy khai đăng ký xe từ cổng dịch vụ công, ký, ghi rõ họ, tên và đóng dấu (nếu là cơ quan, tổ chức).

- Đ: ✓ · T: ✓ · L: ✓ · Nhận xét: —

## 43. `gen-d28b4062efc6` · thu_tuc_tham_quyen · tier A · `TT36-2024-BYT/D7/K1#2025-01-01`

**Câu hỏi:** Thông tư số 36/2024/TT-BYT có hiệu lực từ ngày nào?

> Điều 7. Hiệu lực thi hành
> 1. Thông tư này có hiệu lực kể từ ngày 01 tháng 01 năm 2025.

- Đ: ✓ · T: ✓ · L: ✗ · Nhận xét: loại: khac

## 44. `gen-d6103cba5dfd` · thu_tuc_tham_quyen · tier C · `TT71-2024-BCA/D9/K3#2025-01-01`

**Câu hỏi:** Cơ quan nào chịu trách nhiệm cung cấp tài khoản truyền dữ liệu cho các chủ phương tiện?

> Điều 9. Trách nhiệm của Cục Cảnh sát giao thông
> 3. Cung cấp tài khoản truyền dữ liệu cho các tổ chức, cá nhân kinh doanh vận tải bằng xe ô tô và các chủ phương tiện theo quy định phải lắp thiết bị giám sát hành trình, thiết bị ghi nhận hình ảnh người lái xe hoặc đơn vị cung cấp dịch vụ được ủy quyền.

- Đ: ✓ · T: ✓ · L: ✓ · Nhận xét: —

## 45. `gen-d6cf517676af` · tru_diem · tier A · `ND168-2024/D13/K13#2025-01-01`

**Câu hỏi:** Lái xe ô tô vi phạm điều kiện phương tiện giao thông bị trừ bao nhiêu điểm giấy phép?

> Điều 13. Xử phạt, trừ điểm giấy phép lái xe của người điều khiển xe ô tô (bao gồm cả rơ moóc hoặc sơ mi rơ moóc được kéo theo), xe chở người bốn bánh có gắn động cơ, xe chở hàng bốn bánh có gắn động cơ và các loại xe tương tư xe ô tô vi phạm quy định về điều kiện của phương tiện khi tham gia giao thông
> 13. Ngoài việc bị áp dụng hình thức xử phạt, người điều khiển xe thực hiện hành vi vi phạm còn bị trừ điểm giấy phép lái xe như sau:
> a) Thực hiện hành vi quy định tại điểm a, điểm b khoản 3; khoản 4; khoản 5; khoản 6; điểm a khoản 7 Điều này bị trừ điểm giấy phép lái xe 02 điểm;
> b) Thực hiện hành vi quy định tại điểm b khoản 7, điểm b khoản 8 Điều này bị trừ điểm giấy phép lái xe 06 điểm;
> c) Thực hiện hành vi quy định tại điểm a khoản 8 Điều này bị trừ điểm giấy phép lái xe 10 điểm.

- Đ: ✓ · T: ✓ · L: ✓ · Nhận xét: —

## 46. `gen-db2754129c39` · hanh_vi_cam_nghia_vu · tier B · `ND158-2024/D23/K11#2025-01-01`

**Câu hỏi:** Khi bị thu hồi phù hiệu, đơn vị vận tải phải dừng hoạt động kinh doanh xe ô tô trong bao lâu?

> Điều 23. Quy định về quản lý sử dụng, cấp, cấp lại và thu hồi phù hiệu
> 11. Sở Giao thông vận tải
> a) Ban hành quyết định và thu hồi phù hiệu do cơ quan mình cấp đối với đơn vị kinh doanh vận tải bị thu hồi phù hiệu theo quy định tại khoản 10 Điều này, điểm d khoản 7 Điều 21 của Nghị định này;
> b) Trong thời gian 02 ngày kể từ ngày ban hành quyết định, Sở Giao thông vận tải phải đăng quyết định thu hồi trên Trang thông tin điện tử của Sở; cập nhật các phù hiệu bị thu hồi vào Cơ sở dữ liệu cấp phép hoạt động vận tải;
> c) Khi cơ quan cấp phù hiệu ban hành quyết định thu hồi, trong thời hạn 10 ngày kể từ ngày ký, đơn vị kinh doanh vận tải phải dừng hoạt động kinh doanh vận tải đối với xe ô tô, xe bốn bánh có gắn động cơ bị thu hồi đồng thời nộp lại phù hiệu cho cơ quan cấp.
> Trường hợp đơn vị kinh doanh vận tải nộp lại phù hiệu theo quy định theo quyết định thu hồi, Sở Giao thông vận tải không …

- Đ: ✓ · T: ✓ · L: ✓ · Nhận xét: —

## 47. `gen-dce7ca2a74dd` · dinh_nghia · tier A · `ND151-2024/D11/K1#2025-01-01`

**Câu hỏi:** Cơ quan cấp chứng nhận đăng ký xe phải ghi rõ những thông tin nào?

> Điều 11. Thông tin trong Cơ sở dữ liệu về trật tự, an toàn giao thông đường bộ
> 1. Thông tin về đăng ký, quản lý xe cơ giới, xe máy chuyên dùng:
> a) Thông tin về chủ sở hữu xe cơ giới, xe máy chuyên dùng:
> Đối với cá nhân: họ, tên; ngày, tháng, năm sinh; giới tính; số định danh cá nhân; số điện thoại (nếu có); quốc tịch; nơi thường trú; nơi tạm trú, nơi ở hiện tại, địa chỉ đăng ký xe.
> Đối với tổ chức: tên tổ chức; tên người đại diện hợp pháp; địa chỉ; mã số thuế hoặc quyết định thành lập hoặc số định danh của tổ chức (nếu có); số điện thoại;
> b) Thông tin về phương tiện theo quy định tại điểm a khoản 2 Điều này;
> c) Thông tin về đăng ký, quản lý xe: biển số xe; màu biển số xe; số, ngày, tháng, năm cấp, cơ quan cấp chứng nhận đăng ký xe; thời hạn đăng ký xe; trạng thái đăng ký xe; trạng thái xe; số, ngày, tháng, năm cấp, cơ quan cấp chứng nhận nguồn gốc xe; số, ngày, tháng, năm cấp, cơ quan …

- Đ: ✗ · T: ✓ · L: ✓ · Nhận xét: hỏi thông tin ghi trên chứng nhận; chunk là thông tin trong CSDL

## 48. `gen-e1fe5006d5df` · bien_phap · tier B · `ND158-2024/D23/K10#2025-01-01`

**Câu hỏi:** Khi xe vi phạm tốc độ bao nhiêu lần trên 1000 km thì bị thu hồi phù hiệu?

> Điều 23. Quy định về quản lý sử dụng, cấp, cấp lại và thu hồi phù hiệu
> 10. Đơn vị kinh doanh vận tải bị thu hồi phù hiệu một trong các trường hợp sau đây:
> a) Thu hồi phù hiệu đối với tất cả xe ô tô, xe bốn bánh có gắn động cơ của đơn vị kinh doanh vận tải khi đơn vị kinh doanh vận tải bị cơ quan có thẩm quyền áp dụng hình thức xử phạt tước quyền sử dụng Giấy phép kinh doanh vận tải;
> b) Thu hồi phù hiệu của các xe ô tô kinh doanh vận tải theo tuyến cố định khi đơn vị kinh doanh vận tải không hoạt động kinh doanh vận tải trên tuyến trong thời gian 60 ngày liên tục;
> c) Thu hồi phù hiệu của phương tiện vi phạm 01 tháng đối với trường hợp khi trích xuất dữ liệu từ thiết bị giám sát hành trình của mỗi phương tiện trong 01 tháng cho thấy có từ 05 lần vi phạm tốc độ/1000 km xe chạy (không tính các trường hợp vi phạm tốc độ từ 05 km/h trở xuống);
> d) Thu hồi phù hiệu của phương tiện vi phạm 01 …

- Đ: ✓ · T: ✓ · L: ✗ · Nhận xét: loại: thu_tuc

## 49. `gen-f9c11bb370e5` · bien_phap · tier A · `TT14-2025-BXD/D29/K3#2026-07-01`

**Câu hỏi:** Hệ thống thông tin nào được vận hành bởi Sở Xây dựng theo quy định?

> Điều 29. Sở Xây dựng
> 3. Đối với công tác quản lý hệ thống thông tin:
> a) Đầu tư, bảo trì, nâng cấp Hệ thống thông tin quản lý, giám sát đào tạo lái xe, Hệ thống thông tin chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ tại Sở Xây dựng; tiếp nhận và tổ chức thực hiện phần mềm ứng dụng phục vụ công tác quản lý đào tạo lái xe, phần mềm quản lý cấp chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ tại Sở Xây dựng do Cục Đường bộ Việt Nam chuyển giao trước ngày 01 tháng 7 năm 2026 và thực hiện truyền đầy đủ dữ liệu quy định tại điểm a, điểm b, điểm c, điểm d khoản 2 và điểm a, điểm b, điểm c khoản 5 Điều 25 về Cục Đường bộ Việt Nam từ ngày 01 tháng 7 năm 2026.
> b) Vận hành Hệ thống thông tin quản lý, giám sát đào tạo lái xe và Hệ thống thông tin chứng chỉ bồi dưỡng kiến thức pháp luật về giao thông đường bộ tại Sở Xây dựng theo quy định;
> c) Sử dụng các phần mềm …

- Đ: ✓ · T: ✓ · L: ✗ · Nhận xét: loại: thu_tuc

## 50. `gen-ffa2e72810d6` · dinh_nghia · tier A · `TT14-2025-BXD/D3/K2#2025-09-01`

**Câu hỏi:** Dữ liệu DAT bao gồm những thông tin gì về học viên lái xe?

> Điều 3. Giải thích từ ngữ
> 2. Dữ liệu DAT là tập hợp các thông tin về định danh và quá trình học thực hành lái xe trên đường của học viên, được truyền từ thiết bị DAT lắp trên xe ô tô tập lái để tập lái xe trên đường về máy chủ của cơ sở đào tạo lái xe.

- Đ: ✓ · T: ✓ · L: ✓ · Nhận xét: —
