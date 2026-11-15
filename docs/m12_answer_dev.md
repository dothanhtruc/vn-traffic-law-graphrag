# M12 — Sinh câu trả lời + verify: kết quả chạy thử (val + dev ngoài phạm vi, KHÔNG dùng test)

Bản commit của `data/answer/dev_eval.md` (run `m12-dev`, 15/11/2026) kèm nhận định. Model sinh
`qwen3-14b-awq` = `Qwen/Qwen3-14B-AWQ@31c69ef` (vLLM 0.33.0, `temperature 0`, `seed 42`,
thinking tắt), truy hồi M11 đọc từ cache (`data/index/retrieval_eval/val/<cấu hình>.jsonl`),
τ = −1,625 (điểm rerank top-1, người dùng duyệt; `data/answer/tau.json`).

## Tóm tắt

- **Ổn định định dạng**: 1.587/1.587 lượt `ok` (val 489 × G/B3/B0 + dev 40 × 3), 0 `format_error`,
  0 `error`. Lượt sửa con số: G 62/489 câu (12,7% câu có vi phạm ở phản hồi đầu → 4,3% sau sửa;
  phần còn lại bị bỏ câu chứa số, 31 câu văn).
- **Không có con số pháp lý nào ngoài bảng con số trong câu trả lời G/B3** (theo bộ dò: chữ số,
  số viết bằng chữ dạng cơ bản, ngày không có căn cứ, mã `{N#}` lạ) — bảo đảm bằng thiết kế, có
  test. B0 (không RAG): 15,3% câu có số không kiểm được.
- **Trích dẫn**: G trích dẫn hợp lệ 94,0% (trong ngữ cảnh + đúng unit + hiệu lực); 81,0% câu G có
  trích dẫn tới unit gold (ngữ cảnh chứa gold 92,8% — trần của truy hồi). B0: 0,4% câu trích tới
  gold, **24,1% trích dẫn bịa** (Điều/Khoản không tồn tại).
- **Từ chối**: dev ngoài phạm vi 40/40 từ chối ở cả G, B3, B0; val G từ chối 3,7% (sai từ chối,
  vì mọi câu val có gold). Hạn chế: 40 câu dev rõ ràng ngoài phạm vi và τ được hiệu chỉnh trên
  chính tập này ⇒ tỷ lệ từ chối lạc quan; tập test (`ngoai_pham_vi` 35 câu người viết) sẽ đo ở M13.
- **G ≈ B3 trên val**: nguồn bổ sung từ đồ thị chỉ có ở 0,05 nguồn/câu (val chủ yếu loại
  `hanh_vi_cam_nghia_vu`/`thu_tuc_tham_quyen`, câu sinh từ một chunk) ⇒ không đo được lợi ích đa
  bước; đánh giá G chính thức ở M13 trên test.
- **VRAM hồ sơ `qwen3-14b-awq-shared`** (vLLM 0,70 + embedder + reranker, một câu online G):
  đỉnh nvidia-smi **19.379 / 24.576 MiB** (torch 2,46 GiB) ⇒ đạt ≤ 22 GB, dùng được cho demo M15.
- **GPU**: pha sinh 1.088 s (~18 phút); cả phiên (setup, truy hồi dev + đo VRAM, sinh) ~45 phút ≈
  13.000 VND (gói Pro).

## Rà tay 30 câu G (`sha256(42:m12_review:qid)`, Claude rà — chờ người dùng xác nhận)

| Tiêu chí | Kết quả |
| --- | --- |
| Ngữ cảnh chứa điều khoản trả lời được | 30/30 |
| Nội dung đúng | 25/30 (sai 1: dùng nhầm khoản; đúng một phần 4) |
| Con số khớp nguyên văn nguồn | 29/30 (1 câu số đúng khoản nhưng sai hành vi) |
| Trích dẫn đúng Khoản/Điểm (câu có trích dẫn) | 19/29 (thừa 3, lệch 3, bị loại hết do verify 2) |

Chi tiết: `data/answer/review.md`.

## Ghi chú tái lập / hạn chế

- Bộ dò số và cách đọc nhãn trích dẫn được tinh chỉnh **sau khi xem kết quả val** (quy tắc chung,
  không nhắm câu cụ thể): bỏ chữ số dính chữ cái (hạng GPLX "A1", "C1E"), số viết bằng chữ phải bắt
  đầu bằng một…mười ("đầu tư đồng bộ" không phải số); nhãn `S#/4`, `S#/2/a`, `S#/K22/5` đọc tương
  đối Điều của nguồn; trích khoản nêu chế tài trong bảng con số (`ok_bang_so`); DAN_CHIEU bổ sung
  chỉ chiều ra. Kết quả `m12-dev` được **dựng lại từ cache LLM** (`--cache-only`, cùng prompt ⇒
  cùng phản hồi); 11 lượt sửa số (G 5, B3 6) có danh sách vi phạm khác lần chạy GPU ⇒ trượt cache ⇒
  ghi `repair_status = error`, áp quy tắc dự phòng (bỏ câu chứa số). Bản chạy GPU gốc giữ ở
  `results/m12-dev-v1/` (Release).
- Bộ dò không bắt: số viết bằng chữ ngoài dạng cơ bản ("hai sát hạch viên" — nguyên văn nguồn);
  năm trong tên luật ("Bộ luật Tố tụng hình sự năm 2015") bị dò nhầm thành ngày không căn cứ.
- LLM đôi khi chép dấu ⟦⟧ của đoạn mô tả trong bảng con số, dùng một mã cho cả hai đầu khung phạt
  (cờ `ma_so_lap`, 6 câu G), hoặc chọn nhầm khoản cùng Điều (chỉ judge ở M13 phát hiện được).
- Val do Mistral sinh từ một chunk ⇒ thiên lệch từ vựng; số tuyệt đối không phản ánh câu hỏi thật.

---


Run `m12-dev` · sinh lúc 2026-11-15T11:20:57+07:00 · tổng thời gian sinh 1088.4 s.

Val không có đáp án vàng ⇒ chỉ đo chỉ số không cần đáp án: **trích gold** = câu `ok` có ít nhất một trích dẫn hợp lệ tới unit gold (hoặc tổ tiên/con cháu); **nguồn có gold** = ngữ cảnh chứa gold; trích dẫn hợp lệ = trong ngữ cảnh + đúng unit + hiệu lực tại as_of. Con số: vi phạm = chữ số/số viết bằng chữ/ngày không có căn cứ hoặc mã `{N#}` lạ trong phản hồi LLM. Độ đúng câu trả lời (LLM judge) là việc của M13.

## val

| Cấu hình | n | ok | format_error | error | từ chối | trích gold | nguồn có gold | trích dẫn hợp lệ | câu dùng mã số | vi phạm trước sửa | sau sửa | câu bị bỏ | token vào/ra TB | latency p50 (ms) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| B0 | 489 | 489 | 0 | 0 | 42.1 | 0.4 | — | 75.9 | — | — | — | — | 484.0/383.2 | 8606 |
| B3 | 489 | 489 | 0 | 0 | 3.1 | 81.8 | 93.0 | 94.9 | 26.4 | 12.1 | 4.7 | 40 | 3285.4/347.4 | 17185 |
| G | 489 | 489 | 0 | 0 | 3.7 | 81.0 | 92.8 | 94.0 | 27.2 | 12.7 | 4.3 | 31 | 3395.1/346.4 | 15768 |

- **B0**: `{"co_theo_cau": {"khong_ton_tai": 95, "so_khong_kiem_duoc": 75, "y_khong_nguon": 16, "van_ban_khong_ro": 6}, "b0": {"so_khong_kiem_duoc_tb": 0.45, "cau_co_so": 0.1534, "trich_dan_bia": 0.2414, "trich_dan_het_hieu_luc": 0.0, "trang_thai_trich_dan": {"ok": 1144, "khong_ton_tai": 343, "van_ban_khong_ro": 21}}, "answer_status": {"answered": 283, "out_of_scope": 50, "insufficient": 156}}`
- **B3**: `{"co_theo_cau": {"diem_khong_ton_tai": 39, "y_khong_nguon": 35, "so_khong_kiem_duoc": 23, "so_khong_thuoc_nguon_trich": 19, "y_rong_sau_loc_so": 17, "khong_con_y_nao": 17, "numbers_khong_khop": 16, "ma_so_lap": 7, "ok_bang_so": 3}, "nguon": {"tb": 4.99, "do_thi_tb": 0.0, "trich_nguon_do_thi": 0.0, "cat_ngan": 9}, "answer_status": {"answered": 474, "insufficient": 14, "out_of_scope": 1}}`
- **G**: `{"co_theo_cau": {"diem_khong_ton_tai": 40, "y_khong_nguon": 36, "so_khong_kiem_duoc": 21, "so_khong_thuoc_nguon_trich": 18, "khong_con_y_nao": 18, "numbers_khong_khop": 16, "y_rong_sau_loc_so": 16, "ma_so_lap": 6, "ok_bang_so": 4, "nguon_ngoai_ngu_canh": 1}, "nguon": {"tb": 5.04, "do_thi_tb": 0.05, "trich_nguon_do_thi": 0.0031, "cat_ngan": 12}, "answer_status": {"answered": 471, "insufficient": 17, "out_of_scope": 1}}`

## dev_oos

| Cấu hình | n | ok | format_error | error | từ chối | trích gold | nguồn có gold | trích dẫn hợp lệ | câu dùng mã số | vi phạm trước sửa | sau sửa | câu bị bỏ | token vào/ra TB | latency p50 (ms) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| B0 | 40 | 40 | 0 | 0 | 100.0 | — | — | — | — | — | — | — | 408.4/39.7 | 860 |
| B3 | 40 | 40 | 0 | 0 | 100.0 | — | — | — | 0.0 | 0.0 | 0.0 | 0 | 3713.2/36.6 | 17960 |
| G | 40 | 40 | 0 | 0 | 100.0 | — | — | — | 0.0 | 0.0 | 0.0 | 0 | 3771.1/36.7 | 18141 |

- **B0**: `{"co_theo_cau": {"y_khong_nguon": 1}, "b0": {"so_khong_kiem_duoc_tb": 0.0, "cau_co_so": 0.0, "trich_dan_bia": null, "trich_dan_het_hieu_luc": null, "trang_thai_trich_dan": {}}, "answer_status": {"out_of_scope": 39, "insufficient": 1}}`
- **B3**: `{"co_theo_cau": {}, "nguon": {"tb": 5.0, "do_thi_tb": 0.0, "trich_nguon_do_thi": null, "cat_ngan": 1}, "answer_status": {"insufficient": 9, "out_of_scope": 31}}`
- **G**: `{"co_theo_cau": {}, "nguon": {"tb": 5.17, "do_thi_tb": 0.17, "trich_nguon_do_thi": null, "cat_ngan": 0}, "answer_status": {"insufficient": 9, "out_of_scope": 31}}`

## VRAM (một câu online, hồ sơ serve + embedder + reranker cùng GPU)

- 2026-11-15T10:47:01+07:00: hồ sơ `shared`, nvidia-smi đỉnh 19379 / 24576 MiB, torch (embedder + reranker) 2.464 GiB, 18.02 s
- 2026-11-15T10:47:50+07:00: hồ sơ `shared`, nvidia-smi đỉnh 17547 / 24576 MiB, torch (embedder + reranker) 1.058 GiB, 8.42 s

## 10 ví dụ G (val, chọn theo `sha256(42:m12_examples:qid)`)

**gen-8657714cd191** · as_of 2026-11-03 · loại `hanh_vi_cam_nghia_vu` · answered · gold `ND165-2024/D48/K5`

> Phụ lục hợp đồng dự án khi mở rộng, nâng cấp đường cao tốc theo hình thức đầu tư công phải cập nhật phương án tài chính dựa trên những yếu tố nào?

Nguồn: S1 `ND165-2024/D48/K5#2025-01-01` (top); S2 `ND165-2024/D48/K6#2025-01-01` (top); S3 `ND165-2024/D48/K3#2025-01-01` (top); S4 `ND165-2024/D46/K2#2026-07-01` (top); S5 `LUAT35-2024/D48/K3#2025-01-01` (top)

```text
- Phụ lục hợp đồng dự án khi mở rộng, nâng cấp đường cao tốc theo hình thức đầu tư công phải cập nhật phương án tài chính dựa trên doanh thu dự án hiện hữu khi thực hiện mở rộng, nâng cấp. [điểm a khoản 5 Điều 48 Nghị định 165/2024/NĐ-CP]
- Phụ lục hợp đồng dự án khi mở rộng, nâng cấp đường cao tốc theo hình thức đầu tư công phải cập nhật phương án tài chính dựa trên điều chỉnh chi phí quản lý, vận hành, bảo trì công trình sau khi mở rộng, nâng cấp. [điểm b khoản 5 Điều 48 Nghị định 165/2024/NĐ-CP]
- Phụ lục hợp đồng dự án khi mở rộng, nâng cấp đường cao tốc theo hình thức đầu tư công phải cập nhật phương án tài chính dựa trên mức giá, phí, thời gian thực hiện hợp đồng được điều chỉnh căn cứ doanh thu, chi phí và các nội dung khác của phương án tài chính. [điểm c khoản 5 Điều 48 Nghị định 165/2024/NĐ-CP]
- Phụ lục hợp đồng dự án khi mở rộng, nâng cấp đường cao tốc theo hình thức đầu tư công phải cập nhật phương án tài chính dựa trên các nội dung cần thiết khác cần sửa đổi do ảnh hưởng của việc mở rộng, nâng cấp đường cao tốc. [điểm d khoản 5 Điều 48 Nghị định 165/2024/NĐ-CP]
Kết luận: Phụ lục hợp đồng dự án khi mở rộng, nâng cấp đường cao tốc theo hình thức đầu tư công phải cập nhật phương án tài chính dựa trên doanh thu, chi phí, mức giá, phí, thời gian thực hiện hợp đồng và các nội dung cần thiết khác do ảnh hưởng của việc mở rộng, nâng cấp.
```

Mã số dùng: — · cờ verify: —

**gen-544ffb636979** · as_of 2026-11-03 · loại `thu_tuc_tham_quyen` · answered · gold `ND165-2024/D17/K2`

> Cần chuẩn bị những gì để xin phép xây dựng đường dây điện dưới 35 KV trên đường bộ?

Nguồn: S1 `LUAT35-2024/D19/K4#2025-01-01` (top); S2 `ND165-2024/D17/K2#2026-07-01` (top); S3 `LUAT35-2024/D17/K5#2025-01-01` (top); S4 `LUAT35-2024/D19/K1#2025-01-01` (top); S5 `LUAT35-2024/D84/K4#2025-01-01` (top)

```text
- Đối với việc thi công xây dựng đường dây tải điện, dây dẫn điện có điện áp từ 35 KV trở xuống, thành phần hồ sơ đề nghị chấp thuận xây dựng được thực hiện đồng thời với hồ sơ cấp giấy phép thi công công trình trên đường bộ đang khai thác. [khoản 2 Điều 17 Nghị định 165/2024/NĐ-CP]
- Thành phần hồ sơ bao gồm: bản chính hoặc biểu mẫu điện tử đơn đề nghị chấp thuận đồng thời với cấp giấy phép thi công công trình trên đường bộ đang khai thác theo quy định tại Mẫu số 02 Phụ lục III kèm theo Nghị định này. [khoản 2 Điều 17 Nghị định 165/2024/NĐ-CP]
- Hồ sơ cần có tài liệu quy định tại điểm b, điểm c và điểm e khoản 1 Điều này và biện pháp thi công, phương án tổ chức giao thông là bản sao hoặc bản sao điện tử. [khoản 2 Điều 17 Nghị định 165/2024/NĐ-CP]
- Đường dây tải điện, dây dẫn điện đi phía trên đường bộ phải đáp ứng quy định về khoảng cách theo phương thẳng đứng tính từ điểm cao nhất của mặt đường bộ tới điểm thấp nhất của đường dây tải điện, dây dẫn điện không nhỏ hơn chiều cao tĩnh không của đường bộ cộng với khoảng cách an toàn phóng điện theo quy định của pháp luật về điện lực. [điểm a khoản 5 Điều 17 Luật Đường bộ (35/2024/QH15)]
- Đường dây tải điện, dây dẫn điện đi phía trên cột đèn chiếu sáng của đường bộ phải bảo đảm khoảng cách theo phương thẳng đứng tính từ điểm cao nhất của cột đèn chiếu sáng tới điểm thấp nhất của đường dây tải điện, dây dẫn điện không nhỏ hơn 02 mét cộng với khoảng cách an toàn phóng điện theo quy định của pháp luật về điện lực. [điểm c khoản 5 Điều 17 Luật Đường bộ (35/2024/QH15)]
Kết luận: Để xin phép xây dựng đường dây điện dưới 35 KV trên đường bộ, cần chuẩn bị hồ sơ theo quy định tại Nghị định 165/2024/NĐ-CP và đảm bảo khoảng cách an toàn theo quy định.
```

Mã số dùng: N3=02 mét [S3] · cờ verify: diem_khong_ton_tai, numbers_khong_khop, y_khong_nguon · đã sửa số

**gen-e2b6ea2b69f4** · as_of 2026-11-03 · loại `thu_tuc_tham_quyen` · answered · gold `ND158-2024/D22/K5`

> Khi đơn vị vận tải không đưa xe vào khai thác trong 60 ngày thì thông báo đăng ký khai thác tuyến có hiệu lực không?

Nguồn: S1 `ND158-2024/D50/K7#2025-01-01` (top); S2 `ND158-2024/D22/K5#2026-08-10` (top); S3 `ND158-2024/D43/K5#2025-01-01` (top); S4 `ND158-2024/D62/K5#2025-01-01` (top); S5 `ND158-2024/D56/K5#2025-01-01` (top)

```text
- Thông báo đăng ký khai thác tuyến hết hiệu lực nếu đơn vị vận tải không đưa phương tiện vào khai thác trong vòng 60 ngày kể từ ngày có hiệu lực. [khoản 7 Điều 50 Nghị định 158/2024/NĐ-CP]
- Thông báo đăng ký khai thác tuyến hết hiệu lực nếu đơn vị vận tải không đưa phương tiện vào khai thác trong vòng 60 ngày kể từ ngày có hiệu lực. [khoản 5 Điều 43 Nghị định 158/2024/NĐ-CP]
- Thông báo đăng ký khai thác tuyến hết hiệu lực nếu đơn vị vận tải không đưa phương tiện vào khai thác trong vòng 60 ngày kể từ ngày có hiệu lực. [khoản 5 Điều 62 Nghị định 158/2024/NĐ-CP]
- Thông báo đăng ký khai thác tuyến hết hiệu lực nếu đơn vị vận tải không đưa phương tiện vào khai thác trong vòng 60 ngày kể từ ngày có hiệu lực. [khoản 5 Điều 56 Nghị định 158/2024/NĐ-CP]
- Thông báo đăng ký khai thác tuyến hết hiệu lực nếu đơn vị vận tải không đưa phương tiện vào khai thác trong vòng 60 ngày kể từ ngày có Thông báo đăng ký khai thác tuyến thành công. [khoản 5 Điều 22 Nghị định 158/2024/NĐ-CP]
- Thông báo đăng ký khai thác tuyến hết hiệu lực nếu đơn vị vận tải không đưa phương tiện vào khai thác trong vòng 60 ngày kể từ ngày có hiệu lực. [khoản 7 Điều 50 Nghị định 158/2024/NĐ-CP]
Kết luận: Thông báo đăng ký khai thác tuyến hết hiệu lực nếu đơn vị vận tải không đưa phương tiện vào khai thác trong vòng 60 ngày kể từ ngày có hiệu lực.
```

Mã số dùng: N1=60 ngày [S1], N4=60 ngày [S3], N5=60 ngày [S4], N6=60 ngày [S5], N3=60 ngày [S2] · cờ verify: —

**gen-03e7c991ee5f** · as_of 2026-11-03 · loại `thu_tuc_tham_quyen` · answered · gold `TT36-2024-BYT/D9/K1`

> Thời hạn sử dụng giấy khám sức khỏe lái xe được quy định theo thông tư nào?

Nguồn: S1 `TT36-2024-BYT/D9/K1#2025-01-01` (top); S2 `TT36-2024-BYT/D9/K3#2025-01-01` (top); S3 `TT36-2024-BYT/D9/K2#2025-01-01` (top); S4 `TT36-2024-BYT/D7/K2#2025-01-01` (top); S5 `TT36-2024-BYT/PL1#2025-01-01#p6` (top)

```text
- Thời hạn sử dụng giấy khám sức khỏe lái xe là 12 tháng kể từ ngày ký kết luận. [Phụ lục 1 Thông tư 36/2024/TT-BYT]
- Giấy khám sức khỏe và sổ khám sức khỏe định kỳ của người lái xe được cấp trước ngày Thông tư này có hiệu lực thi hành được tiếp tục sử dụng theo thời hạn ghi trên giấy khám sức khỏe và sổ khám sức khỏe định kỳ của người lái xe theo quy định tại Thông tư liên tịch số 24/2015/TTLT-BYT-BGTVT. [khoản 1 Điều 9 Thông tư 36/2024/TT-BYT]
- Mẫu giấy khám sức khỏe của người lái xe ban hành tại Thông tư liên tịch số 24/2015/TTLT-BYT-BGTVT được tiếp tục sử dụng và phải tuân thủ hướng dẫn ghi theo quy định tại Phụ lục II ban hành kèm theo Thông tư này. [khoản 2 Điều 9 Thông tư 36/2024/TT-BYT]
- Thông tư liên tịch số 24/2015/TTLT-BYT-BGTVT hết hiệu lực kể từ ngày Thông tư này có hiệu lực thi hành. [khoản 2 Điều 7 Thông tư 36/2024/TT-BYT]
- Mẫu sổ khám sức khỏe định kỳ của người lái xe ban hành tại Thông tư liên tịch số 24/2015/TTLT-BYT-BGTVT bản giấy đã in được tiếp tục sử dụng đến hết ngày 30 tháng 6 năm 2025. [khoản 3 Điều 9 Thông tư 36/2024/TT-BYT]
- Giấy khám sức khỏe này có giá trị sử dụng trong vòng 12 tháng kể từ ngày ký kết luận. [Phụ lục 1 Thông tư 36/2024/TT-BYT]
Kết luận: Thời hạn sử dụng giấy khám sức khỏe lái xe được quy định là 12 tháng theo Thông tư 36/2024/TT-BYT.
```

Mã số dùng: N2=12 tháng [S5] · cờ verify: —

**gen-6907cfaf5cf2** · as_of 2026-11-03 · loại `dinh_nghia` · answered · gold `TT12-2025-BCA/D18/K7`

> Giấy phép lái xe quốc tế có hiệu lực ở Việt Nam nếu có điều ước quốc tế khác quy định gì?

Nguồn: S1 `TT12-2025-BCA/D18/K7#2025-03-01` (top); S2 `LUAT36-2024/D57/K8#2025-01-01` (top); S3 `LUAT36-2024/D57/K6#2025-01-01` (top); S4 `LUAT36-2024/D55/K3#2025-01-01` (top); S5 `TT12-2025-BCA/D3/K5#2025-03-01` (top)

```text
- Giấy phép lái xe quốc tế được sử dụng tại Việt Nam nếu có điều ước quốc tế khác quy định, theo quy định tại S2/a. [điểm a khoản 8 Điều 57 Luật Trật tự, an toàn giao thông đường bộ (36/2024/QH15)]
- Trường hợp điều ước quốc tế mà Việt Nam là thành viên có quy định khác thì áp dụng quy định của điều ước quốc tế đó, theo quy định tại S1/7. [khoản 7 Điều 18 Thông tư 12/2025/TT-BCA]
- Giấy phép lái xe quốc tế do quốc gia là thành viên của Công ước Viên cấp có thời hạn không quá 03 năm kể từ ngày cấp, theo quy định tại S2/a. [điểm a khoản 8 Điều 57 Luật Trật tự, an toàn giao thông đường bộ (36/2024/QH15)]
- Người có giấy phép lái xe quốc tế phải tuân thủ pháp luật về trật tự, an toàn giao thông đường bộ của Việt Nam, theo quy định tại S2/b. [điểm b khoản 8 Điều 57 Luật Trật tự, an toàn giao thông đường bộ (36/2024/QH15)]
- Giấy phép lái xe quốc tế được quy định như một giấy phép lái xe do cơ quan nhà nước có thẩm quyền của quốc gia là thành viên của Công ước Viên cấp theo một mẫu thống nhất, theo quy định tại S2/a. [điểm a khoản 8 Điều 57 Luật Trật tự, an toàn giao thông đường bộ (36/2024/QH15)]
- Giấy phép lái xe quốc tế có giá trị sử dụng trong phạm vi lãnh thổ Việt Nam nếu phù hợp với loại xe được phép điều khiển, theo quy định tại S3/b. [điểm b khoản 6 Điều 57 Luật Trật tự, an toàn giao thông đường bộ (36/2024/QH15)]
Kết luận: Giấy phép lái xe quốc tế có hiệu lực ở Việt Nam nếu có điều ước quốc tế khác quy định, theo quy định tại S2/a và S1/7.
```

Mã số dùng: N1=03 năm [S2] · cờ verify: —

**gen-f552e86e541a** · as_of 2025-06-30 · loại `hanh_vi_cam_nghia_vu` · answered · gold `ND151-2024/D36/K2`

> Các bộ nào phải phối hợp quản lý hoạt động của người nước ngoài và xe nước ngoài tại Việt Nam?

Nguồn: S1 `ND151-2024/D36/K5#2025-01-01` (top); S2 `ND151-2024/D36/K2#2025-01-01` (top); S3 `ND151-2024/D33/K4#2025-01-01` (top); S4 `ND151-2024/D36/K6#2025-01-01` (top); S5 `ND151-2024/D36/K1#2025-01-01` (top)

```text
- Bộ Ngoại giao phải phối hợp quản lý hoạt động của người nước ngoài và xe nước ngoài tại Việt Nam. [khoản 5 Điều 36 Nghị định 151/2024/NĐ-CP]
- Bộ Giao thông vận tải phải phối hợp quản lý hoạt động của người nước ngoài và xe nước ngoài tại Việt Nam. [khoản 5 Điều 36 Nghị định 151/2024/NĐ-CP]
- Bộ Công an phải phối hợp quản lý hoạt động của người nước ngoài và xe nước ngoài tại Việt Nam. [khoản 5 Điều 36 Nghị định 151/2024/NĐ-CP]
- Bộ Quốc phòng phải phối hợp quản lý hoạt động của người nước ngoài và xe nước ngoài tại Việt Nam. [khoản 5 Điều 36 Nghị định 151/2024/NĐ-CP]
- Bộ Tài chính phải phối hợp quản lý hoạt động của người nước ngoài và xe nước ngoài tại Việt Nam. [khoản 5 Điều 36 Nghị định 151/2024/NĐ-CP]
- Bộ Văn hóa, Thể thao và Du lịch phải phối hợp quản lý hoạt động của người nước ngoài và xe nước ngoài tại Việt Nam. [khoản 5 Điều 36 Nghị định 151/2024/NĐ-CP]
Kết luận: Các bộ được nêu rõ trong Nghị định 151/2024/NĐ-CP phải phối hợp quản lý hoạt động của người nước ngoài và xe nước ngoài tại Việt Nam.
```

Mã số dùng: — · cờ verify: —

**gen-3eb7c3d85fad** · as_of 2026-08-09 · loại `thu_tuc_tham_quyen` · answered · gold `ND158-2024/D34/K2`

> Ai được quy định có thẩm quyền gia hạn thời gian lưu hành phương tiện đường bộ trong trường hợp gặp sự cố bất khả kháng?

Nguồn: S1 `ND158-2024/D34/K2#2025-01-01` (top); S2 `ND158-2024/D39/K2#2025-01-01` (top); S3 `ND158-2024/D42/K2#2025-01-01` (top); S4 `ND158-2024/D55/K2#2025-01-01` (top); S5 `ND158-2024/D61/K2#2025-01-01` (top)

```text
- Sở Giao thông vận tải các tỉnh, thành phố trực thuộc trung ương nơi phương tiện gặp sự cố bất khả kháng được quy định có thẩm quyền gia hạn thời gian lưu hành phương tiện đường bộ trong trường hợp gặp sự cố bất khả kháng. [khoản 2 Điều 34 Nghị định 158/2024/NĐ-CP; khoản 2 Điều 39 Nghị định 158/2024/NĐ-CP; khoản 2 Điều 42 Nghị định 158/2024/NĐ-CP; khoản 2 Điều 55 Nghị định 158/2024/NĐ-CP; khoản 2 Điều 61 Nghị định 158/2024/NĐ-CP]
Kết luận: Các nguồn đều quy định rõ thẩm quyền gia hạn thời gian lưu hành phương tiện trong trường hợp gặp sự cố bất khả kháng.
```

Mã số dùng: — · cờ verify: —

**gen-5250b81b38b1** · as_of 2026-11-03 · loại `theo_thoi_diem` · answered · gold `LUAT36-2024/D89/K3`

> Tôi có giấy phép lái xe hạng A1 trước khi Luật Trật tự giao thông có hiệu lực, có thể đổi sang hạng A được không?

Nguồn: S1 `LUAT36-2024/D89/K3#2025-01-01` (top); S2 `LUAT36-2024/D89/K2#2025-01-01` (top); S3 `TT36-2024-BYT/D2/K3#2025-01-01` (top); S4 `TT12-2025-BCA/D21/K1#2025-03-01` (top); S5 `LUAT36-2024/D57/K5#2025-01-01` (top)

```text
- Người có giấy phép lái xe hạng A1 được đổi, cấp lại sang giấy phép lái xe hạng A với điều kiện hạn chế là chỉ được điều khiển xe mô tô hai bánh có dung tích xi-lanh đến dưới 175 cm3 hoặc có công suất động cơ điện đến dưới 14 kW. [điểm a khoản 3 Điều 89 Luật Trật tự, an toàn giao thông đường bộ (36/2024/QH15)]
- Việc đổi giấy phép lái xe hạng A1 sang hạng A được thực hiện theo quy định tại điểm a khoản 3 Điều 89 Luật Trật tự, an toàn giao thông đường bộ. [điểm a khoản 3 Điều 89 Luật Trật tự, an toàn giao thông đường bộ (36/2024/QH15)]
- Người có giấy phép lái xe hạng A1 được tiếp tục điều khiển xe mô tô hai bánh có dung tích xi-lanh từ 50 cm3 đến dưới 175 cm3 hoặc có công suất động cơ điện từ 04 kW đến dưới 14 kW. [điểm a khoản 2 Điều 89 Luật Trật tự, an toàn giao thông đường bộ (36/2024/QH15)]
- Người có giấy phép lái xe hạng A1 được đổi, cấp lại sang giấy phép lái xe hạng A theo quy định tại điểm a khoản 3 Điều 89 Luật Trật tự, an toàn giao thông đường bộ. [điểm a khoản 3 Điều 89 Luật Trật tự, an toàn giao thông đường bộ (36/2024/QH15)]
- Áp dụng tiêu chuẩn sức khỏe Nhóm 1 để khám sức khỏe khi đổi giấy phép lái xe hạng A1 sang hạng A. [khoản 3 Điều 2 Thông tư 36/2024/TT-BYT]
- Giấy phép lái xe hạng A không có thời hạn. [điểm a khoản 5 Điều 57 Luật Trật tự, an toàn giao thông đường bộ (36/2024/QH15)]
Kết luận: Người có giấy phép lái xe hạng A1 trước khi Luật Trật tự, an toàn giao thông đường bộ có hiệu lực có thể đổi sang hạng A theo quy định.
```

Mã số dùng: N1=175 [S1], N2=14 [S1], N5=50 [S2], N6=175 [S2], N7=04 [S2], N8=14 [S2], N14=1 [S3] · cờ verify: —

**gen-58951a64d9a0** · as_of 2026-11-03 · loại `hanh_vi_cam_nghia_vu` · answered · gold `TT73-2024-BCA/D2/K2`

> Ai có quyền tham gia tuần tra giao thông cùng với Cảnh sát giao thông?

Nguồn: S1 `TT73-2024-BCA/D2/K2#2025-01-01` (top); S2 `LUAT36-2024/D65/K3#2025-01-01` (top); S3 `TT73-2024-BCA/D29/K3#2025-01-01` (top); S4 `LUAT36-2024/D65/K5#2025-01-01` (top); S5 `LUAT36-2024/D70/K1#2025-01-01` (top)

```text
- Sĩ quan, hạ sĩ quan nghiệp vụ của lực lượng khác trong Công an nhân dân được huy động tham gia phối hợp với Cảnh sát giao thông thực hiện tuần tra, kiểm soát. [khoản 2 Điều 2 Thông tư 73/2024/TT-BCA]
- Lực lượng, đơn vị khác trong Công an nhân dân được huy động tham gia phối hợp với Cảnh sát giao thông thực hiện tuần tra, kiểm soát trong trường hợp cần thiết. [điểm b khoản 3 Điều 65 Luật Trật tự, an toàn giao thông đường bộ (36/2024/QH15)]
- Cán bộ, chiến sĩ được huy động tham gia phối hợp với Cảnh sát giao thông thực hiện tuần tra, kiểm soát phải được quán triệt, nắm vững các quy định của pháp luật về trật tự, an toàn giao thông đường bộ. [khoản 3 Điều 29 Thông tư 73/2024/TT-BCA]
- Lực lượng khác trong Công an nhân dân tham gia phối hợp với Cảnh sát giao thông thực hiện tuần tra, kiểm soát được trang bị phương tiện, thiết bị kỹ thuật nghiệp vụ, vũ khí, công cụ hỗ trợ phù hợp với nhiệm vụ được giao theo quy định của pháp luật. [khoản 1 Điều 70 Luật Trật tự, an toàn giao thông đường bộ (36/2024/QH15)]
Kết luận: Các lực lượng trong Công an nhân dân được huy động tham gia tuần tra giao thông cùng Cảnh sát giao thông theo quy định pháp luật.
```

Mã số dùng: — · cờ verify: —

**gen-947101987798** · as_of 2026-06-30 · loại `thu_tuc_tham_quyen` · answered · gold `ND165-2024/D31/K3`

> Ai có quyền chấp thuận vị trí và cấp phép thi công đấu nối tạm vào quốc lộ?

Nguồn: S1 `ND165-2024/D31/K3#2025-01-01` (top); S2 `ND165-2024/D18/K2#2025-01-01` (top); S3 `ND165-2024/D31/K4#2025-01-01` (top); S4 `ND165-2024/D29/K5#2025-01-01` (top); S5 `LUAT35-2024/D30/K5#2025-01-01` (top)

```text
- Khu quản lý đường bộ có thẩm quyền chấp thuận vị trí, thiết kế đấu nối tạm và cấp giấy phép thi công vào quốc lộ quy định tại khoản 3 Điều 8 Luật Đường bộ. [điểm a khoản 3 Điều 31 Nghị định 165/2024/NĐ-CP]
- Sở Giao thông vận tải có thẩm quyền chấp thuận vị trí, thiết kế đấu nối tạm và cấp giấy phép thi công vào quốc lộ quy định tại khoản 4 Điều 8 Luật Đường bộ và quốc lộ quy định tại khoản 1 Điều 4, khoản 1 Điều 5 và khoản 1 Điều 6 của Nghị định này; đường tỉnh và đường khác được Ủy ban nhân dân cấp tỉnh giao quản lý. [điểm b khoản 3 Điều 31 Nghị định 165/2024/NĐ-CP]
- Ủy ban nhân dân cấp huyện, Ủy ban nhân dân cấp xã có thẩm quyền chấp thuận vị trí, thiết kế đấu nối tạm và cấp giấy phép thi công vào đường bộ thuộc phạm vi quản lý. [điểm c khoản 3 Điều 31 Nghị định 165/2024/NĐ-CP]
- Cục Đường bộ Việt Nam có thẩm quyền chấp thuận vị trí, thiết kế đấu nối tạm và cấp giấy phép thi công vào quốc lộ quy định tại khoản 3 Điều 8 Luật Đường bộ, trừ trường hợp quy định tại khoản 2 Điều 17 của Nghị định này và điểm d khoản này. [điểm a khoản 2 Điều 18 Nghị định 165/2024/NĐ-CP]
- Sở Giao thông vận tải có thẩm quyền chấp thuận vị trí, thiết kế đấu nối tạm và cấp giấy phép thi công vào quốc lộ quy định tại khoản 4 Điều 8 Luật Đường bộ và quy định tại khoản 1 Điều 4, khoản 1 Điều 5, khoản 1 Điều 6 của Nghị định này; đường khác thuộc phạm vi được giao quản lý, trừ quy định tại điểm d khoản này. [điểm b khoản 2 Điều 18 Nghị định 165/2024/NĐ-CP]
- Ủy ban nhân dân cấp huyện, Ủy ban nhân dân cấp xã có thẩm quyền chấp thuận vị trí, thiết kế đấu nối tạm và cấp giấy phép thi công vào đường thuộc phạm vi quản lý, trừ quy định tại điểm d khoản này. [điểm c khoản 2 Điều 18 Nghị định 165/2024/NĐ-CP]
Kết luận: Các cơ quan có thẩm quyền chấp thuận vị trí và cấp phép thi công đấu nối tạm vào quốc lộ được quy định cụ thể tại các khoản 3, 4, 5 Điều 31 và khoản 2 Điều 18 của Nghị định 165/2024/NĐ-CP.
```

Mã số dùng: — · cờ verify: —

