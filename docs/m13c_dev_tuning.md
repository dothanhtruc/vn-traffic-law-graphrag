# M13c — chỉnh graph expand, từ chối, prompt sửa số trên tập dev

Run `m13c-dev` (+ `m13c-dev-<biến thể>`), 18/11/2026. **Không dùng test.** Tập: `data/qa/dev_multi.jsonl` (75 câu: đa bước 32, theo thời điểm 20 = 10 cặp, mức phạt 13, so sánh 6, trừ điểm 4) + `data/qa/dev_out_of_scope.jsonl` (40 câu ngoài phạm vi Claude viết ở M12 — đã dùng hiệu chỉnh τ ⇒ recall từ chối trên tập này lạc quan, chỉ so tương đối). Cấu hình: `configs/eval_dev.yaml`, `configs/dev_tuning/`. So sánh: `scripts.eval compare-runs` (ghép cặp theo câu; McNemar chính xác / Wilcoxon Pratt, **p thô**, không Holm). Ô bảng: phần trăm (hoặc trung bình) [n câu có giá trị].

## Kết luận

- **Không đổi cấu hình nào.** Không biến thể nào tốt hơn G rõ ràng trên dev theo tiêu chí khai báo trước (graph expand: "đủ các bước" + judge trên câu đa bước, không làm judge toàn tập giảm > 2 điểm %; từ chối: giảm từ chối nhầm, recall ngoài phạm vi ≥ 95%; sửa số: vi phạm còn lại, câu bị bỏ, đủ con số, judge).
- **Graph expand có tác dụng ở pool, mất ở rerank**: với câu đa bước, gold có trong pool 100% (A1 không expand: 97,9%), 84,9% gold đến được từ đồ thị (XG_all2: 92,2%); nhưng chỉ 68,8% gold vào top-5 và ngữ cảnh — như A1. Nút thắt là reranker xếp chunk liên kết thấp và **analyzer không gán `da_buoc` cho câu đa bước nào** (32 câu → thu_tuc_tham_quyen 12, hanh_vi_cam_nghia_vu 13, dinh_nghia 3, bien_phap 2, …) ⇒ chunk đồ thị bổ sung vào ngữ cảnh (chỉ bật cho mức phạt/trừ điểm/biện pháp/đa bước) gần như không dùng.
- **Biến thể hậu kiểm** `ctx_all` (thêm sau khi thấy điều trên — không khai báo trước): bật chunk đồ thị bổ sung cho mọi loại câu ⇒ gold trong ngữ cảnh đa bước 68,8 → 75,0% (p thô 0,046), ngữ cảnh phủ đủ gold 37,5 → 50,0% (p 0,125), nhưng judge **không đổi** (đa bước 1,16 → 1,16) ⇒ LLM chưa tận dụng được nguồn thêm. Không áp dụng; ghi lại làm hướng cải tiến (phân loại câu đa bước, rerank có tính liên kết).
- **Từ chối**: trên dev G từ chối nhầm câu có gold chỉ 3,0% (2/67). Phần lớn "từ chối nhầm" ở M13 là **lỗi cách tính** — câu "trước mốc" gold rỗng mà hệ thống từ chối (đúng) bị tính là sai. Đã sửa chỉ số (`report.refusal_stats`, `answer_metrics.tu_choi_dung`) và chấm lại `m13-test-v2` (G precision 43,0 → 64,6%, từ chối nhầm câu có gold 6,3%). `refusal_v2` bớt 1 câu từ chối nhầm nhưng mất 1 câu ngoài phạm vi (recall 97,5%) và thêm câu văn bị bỏ ⇒ không đổi. `no_tau` (bỏ lưu ý τ): kết quả y hệt G.
- **Prompt sửa số M12 vs v2**: trên dev, v2 (hiện hành) không kém M12 — đủ con số 65,5 vs 62,1%, câu văn bị bỏ 0,03 vs 0,06/câu, judge 60,9 vs 61,7% (p = 1). Suy giảm thấy ở test v2 không tái hiện trên dev ⇒ **giữ v2**.

## Biến thể

| Tên | Thay đổi so với G | Khai báo |
|---|---|---|
| A1 | không graph expand | trước |
| XG_r1 | 1 chỗ trong top-5 dành cho chunk chỉ đến từ đồ thị | trước |
| XG_all2 | mọi loại câu dùng bảng expand đa bước (DAN_CHIEU, BI_XU_PHAT, BI_TRU_DIEM, HUONG_DAN; 2 hop) | trước |
| XG_all2_r1 | XG_all2 + XG_r1 | trước |
| ctx5 | `context.max_graph_extra` 5 (thay 3) | trước |
| ctx_all / ctx_all5 | chunk đồ thị bổ sung cho mọi loại câu (3 / 5 chunk) | **sau khi xem dev** |
| refusal_v2 | prompt `answer_refusal_v2.md`: chỉ `insufficient` khi không nguồn nào liên quan; trả lời được một phần thì `answered` | trước |
| no_tau | `refusal.tau = null` (không thêm lưu ý nguồn ít liên quan) | trước |
| repair_m12 | prompt sửa số bản M12 (`answer_number_repair_m12.md`) | trước |

## Graph expand và ngữ cảnh

Loại câu: tất cả · n = 115

| Chỉ số | G | A1 | XG_r1 | XG_all2 | XG_all2_r1 | ctx5 | ctx_all | ctx_all5 |
|---|---|---|---|---|---|---|---|---|
| Judge: đúng hoàn toàn | 60.9 [115] | 61.7 [115] (p 1.000) | 65.2 [115] (p 0.267) | 61.7 [115] (p 1.000) | 61.7 [115] (p 1.000) | 60.9 [115] (p 1.000) | 60.9 [115] (p 1.000) | 60.9 [115] (p 1.000) |
| Judge: điểm TB (0–2) | 1.51 [115] | 1.53 [115] (p 0.560) | 1.56 [115] (p 0.311) | 1.53 [115] (p 0.157) | 1.52 [115] (p 0.985) | 1.51 [115] (p 1.000) | 1.51 [115] (p 0.571) | 1.51 [115] (p 0.571) |
| Đủ con số yêu cầu | 65.5 [29] | 69.0 [29] (p 1.000) | 72.4 [29] (p 0.625) | 65.5 [29] (p 1.000) | 69.0 [29] (p 1.000) | 65.5 [29] (p 1.000) | 65.5 [29] (p 1.000) | 65.5 [29] (p 1.000) |
| Recall con số | 73.0 [29] | 74.7 [29] (p 0.317) | 77.0 [29] (p 0.336) | 73.0 [29] (p 1.000) | 73.0 [29] (p 1.000) | 73.0 [29] (p 1.000) | 73.0 [29] (p 1.000) | 73.0 [29] (p 1.000) |
| Có trích dẫn tới gold | 77.6 [67] | 77.6 [67] (p 1.000) | 79.1 [67] (p 1.000) | 82.1 [67] (p 0.375) | 82.1 [67] (p 0.375) | 77.6 [67] (p 1.000) | 79.1 [67] (p 1.000) | 79.1 [67] (p 1.000) |
| Đúng phiên bản (theo thời điểm) | 90.0 [20] | 90.0 [20] (p 1.000) | 95.0 [20] (p 1.000) | 90.0 [20] (p 1.000) | 95.0 [20] (p 1.000) | 90.0 [20] (p 1.000) | 95.0 [20] (p 1.000) | 95.0 [20] (p 1.000) |
| Đa bước: gold trong top-5 | 68.8 [32] | 70.3 [32] (p 0.317) | 68.8 [32] (p 1.000) | 68.8 [32] (p 1.000) | 68.8 [32] (p 1.000) | 68.8 [32] (p 1.000) | 68.8 [32] (p 1.000) | 68.8 [32] (p 1.000) |
| Đa bước: gold trong ngữ cảnh | 68.8 [32] | 70.3 [32] (p 0.317) | 68.8 [32] (p 1.000) | 68.8 [32] (p 1.000) | 68.8 [32] (p 1.000) | 68.8 [32] (p 1.000) | 75.0 [32] (p 0.046) | 75.0 [32] (p 0.046) |
| Đa bước: ngữ cảnh phủ đủ gold | 37.5 [32] | 40.6 [32] (p 1.000) | 37.5 [32] (p 1.000) | 37.5 [32] (p 1.000) | 37.5 [32] (p 1.000) | 37.5 [32] (p 1.000) | 50.0 [32] (p 0.125) | 50.0 [32] (p 0.125) |
| Recall@5 | 79.9 [67] | 81.3 [67] (p 0.157) | 78.4 [67] (p 0.414) | 79.9 [67] (p 1.000) | 78.4 [67] (p 0.414) | 79.9 [67] (p 1.000) | 79.9 [67] (p 1.000) | 79.9 [67] (p 1.000) |
| tu_choi | 10.7 [75] | 9.3 [75] (p 0.317) | 9.3 [75] (p 0.317) | 10.7 [75] (p 1.000) | 9.3 [75] (p 0.317) | 10.7 [75] (p 1.000) | 10.7 [75] (p 1.000) | 10.7 [75] (p 1.000) |
| Từ chối đúng | 98.1 [107] | 99.1 [107] (p 1.000) | 99.1 [107] (p 1.000) | 98.1 [107] (p 1.000) | 99.1 [107] (p 1.000) | 98.1 [107] (p 1.000) | 98.1 [107] (p 1.000) | 98.1 [107] (p 1.000) |
| Vi phạm số sau sửa (TB/câu) | 0.06 [115] | 0.04 [115] (p 0.317) | 0.07 [115] (p 0.317) | 0.10 [115] (p 0.317) | 0.07 [115] (p 0.317) | 0.06 [115] (p 1.000) | 0.08 [115] (p 0.157) | 0.10 [115] (p 0.083) |
| Câu văn bị bỏ (TB/câu) | 0.03 [115] | 0.03 [115] (p 1.000) | 0.04 [115] (p 0.317) | 0.07 [115] (p 0.317) | 0.04 [115] (p 0.317) | 0.03 [115] (p 1.000) | 0.05 [115] (p 0.157) | 0.08 [115] (p 0.083) |

| Từ chối | G | A1 | XG_r1 | XG_all2 | XG_all2_r1 | ctx5 | ctx_all | ctx_all5 |
|---|---|---|---|---|---|---|---|---|
| precision | 95.8 | 97.9 | 97.9 | 95.8 | 97.9 | 95.8 | 95.8 | 95.8 |
| precision_oos | 83.3 | 85.1 | 85.1 | 83.3 | 85.1 | 83.3 | 83.3 | 83.3 |
| recall | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 | 100.0 |
| tu_choi_gold_rong | 75.0 | 75.0 | 75.0 | 75.0 | 75.0 | 75.0 | 75.0 | 75.0 |
| tu_choi_sai | 3.0 | 1.5 | 1.5 | 3.0 | 1.5 | 3.0 | 3.0 | 3.0 |

Loại câu: da_buoc · n = 32

| Chỉ số | G | A1 | XG_r1 | XG_all2 | XG_all2_r1 | ctx5 | ctx_all | ctx_all5 |
|---|---|---|---|---|---|---|---|---|
| Judge: đúng hoàn toàn | 21.9 [32] | 21.9 [32] (p 1.000) | 25.0 [32] (p 1.000) | 21.9 [32] (p 1.000) | 21.9 [32] (p 1.000) | 21.9 [32] (p 1.000) | 21.9 [32] (p 1.000) | 21.9 [32] (p 1.000) |
| Judge: điểm TB (0–2) | 1.16 [32] | 1.16 [32] (p 1.000) | 1.22 [32] (p 0.527) | 1.16 [32] (p 1.000) | 1.19 [32] (p 0.739) | 1.16 [32] (p 1.000) | 1.16 [32] (p 0.589) | 1.16 [32] (p 0.589) |
| Đủ con số yêu cầu | 66.7 [6] | 66.7 [6] (p 1.000) | 83.3 [6] (p 1.000) | 66.7 [6] (p 1.000) | 83.3 [6] (p 1.000) | 66.7 [6] (p 1.000) | 66.7 [6] (p 1.000) | 66.7 [6] (p 1.000) |
| Recall con số | 72.2 [6] | 72.2 [6] (p 1.000) | 88.9 [6] (p 0.317) | 72.2 [6] (p 1.000) | 88.9 [6] (p 0.317) | 72.2 [6] (p 1.000) | 72.2 [6] (p 1.000) | 72.2 [6] (p 1.000) |
| Có trích dẫn tới gold | 84.4 [32] | 84.4 [32] (p 1.000) | 90.6 [32] (p 0.500) | 84.4 [32] (p 1.000) | 90.6 [32] (p 0.500) | 84.4 [32] (p 1.000) | 84.4 [32] (p 1.000) | 84.4 [32] (p 1.000) |
| Đa bước: gold trong top-5 | 68.8 [32] | 70.3 [32] (p 0.317) | 68.8 [32] (p 1.000) | 68.8 [32] (p 1.000) | 68.8 [32] (p 1.000) | 68.8 [32] (p 1.000) | 68.8 [32] (p 1.000) | 68.8 [32] (p 1.000) |
| Đa bước: gold trong ngữ cảnh | 68.8 [32] | 70.3 [32] (p 0.317) | 68.8 [32] (p 1.000) | 68.8 [32] (p 1.000) | 68.8 [32] (p 1.000) | 68.8 [32] (p 1.000) | 75.0 [32] (p 0.046) | 75.0 [32] (p 0.046) |
| Đa bước: ngữ cảnh phủ đủ gold | 37.5 [32] | 40.6 [32] (p 1.000) | 37.5 [32] (p 1.000) | 37.5 [32] (p 1.000) | 37.5 [32] (p 1.000) | 37.5 [32] (p 1.000) | 50.0 [32] (p 0.125) | 50.0 [32] (p 0.125) |
| Recall@5 | 68.8 [32] | 70.3 [32] (p 0.317) | 68.8 [32] (p 1.000) | 68.8 [32] (p 1.000) | 68.8 [32] (p 1.000) | 68.8 [32] (p 1.000) | 68.8 [32] (p 1.000) | 68.8 [32] (p 1.000) |
| tu_choi | 0.0 [32] | 0.0 [32] (p 1.000) | 0.0 [32] (p 1.000) | 0.0 [32] (p 1.000) | 0.0 [32] (p 1.000) | 0.0 [32] (p 1.000) | 0.0 [32] (p 1.000) | 0.0 [32] (p 1.000) |
| Từ chối đúng | 100.0 [32] | 100.0 [32] (p 1.000) | 100.0 [32] (p 1.000) | 100.0 [32] (p 1.000) | 100.0 [32] (p 1.000) | 100.0 [32] (p 1.000) | 100.0 [32] (p 1.000) | 100.0 [32] (p 1.000) |
| Vi phạm số sau sửa (TB/câu) | 0.09 [32] | 0.03 [32] (p 0.317) | 0.12 [32] (p 0.317) | 0.09 [32] (p 1.000) | 0.12 [32] (p 0.317) | 0.09 [32] (p 1.000) | 0.12 [32] (p 0.317) | 0.12 [32] (p 0.317) |
| Câu văn bị bỏ (TB/câu) | 0.03 [32] | 0.03 [32] (p 1.000) | 0.06 [32] (p 0.317) | 0.03 [32] (p 1.000) | 0.06 [32] (p 0.317) | 0.03 [32] (p 1.000) | 0.06 [32] (p 0.317) | 0.06 [32] (p 0.317) |

| Từ chối | G | A1 | XG_r1 | XG_all2 | XG_all2_r1 | ctx5 | ctx_all | ctx_all5 |
|---|---|---|---|---|---|---|---|---|
| precision | — | — | — | — | — | — | — | — |
| precision_oos | — | — | — | — | — | — | — | — |
| recall | — | — | — | — | — | — | — | — |
| tu_choi_gold_rong | — | — | — | — | — | — | — | — |
| tu_choi_sai | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

## Từ chối và prompt sửa số

Loại câu: tất cả · n = 115

| Chỉ số | G | refusal_v2 | no_tau | repair_m12 |
|---|---|---|---|---|
| Judge: đúng hoàn toàn | 60.9 [115] | 63.5 [115] (p 0.508) | 60.9 [115] (p 1.000) | 61.7 [115] (p 1.000) |
| Judge: điểm TB (0–2) | 1.51 [115] | 1.52 [115] (p 0.386) | 1.51 [115] (p 1.000) | 1.52 [115] (p 0.317) |
| Đủ con số yêu cầu | 65.5 [29] | 65.5 [29] (p 1.000) | 65.5 [29] (p 1.000) | 62.1 [29] (p 1.000) |
| Recall con số | 73.0 [29] | 73.0 [29] (p 1.000) | 73.0 [29] (p 1.000) | 69.5 [29] (p 0.317) |
| Có trích dẫn tới gold | 77.6 [67] | 77.6 [67] (p 1.000) | 77.6 [67] (p 1.000) | 76.1 [67] (p 1.000) |
| Đúng phiên bản (theo thời điểm) | 90.0 [20] | 90.0 [20] (p 1.000) | 90.0 [20] (p 1.000) | 90.0 [20] (p 1.000) |
| Đa bước: gold trong top-5 | 68.8 [32] | 68.8 [32] (p 1.000) | 68.8 [32] (p 1.000) | 68.8 [32] (p 1.000) |
| Đa bước: gold trong ngữ cảnh | 68.8 [32] | 68.8 [32] (p 1.000) | 68.8 [32] (p 1.000) | 68.8 [32] (p 1.000) |
| Đa bước: ngữ cảnh phủ đủ gold | 37.5 [32] | 37.5 [32] (p 1.000) | 37.5 [32] (p 1.000) | 37.5 [32] (p 1.000) |
| Recall@5 | 79.9 [67] | 79.9 [67] (p 1.000) | 79.9 [67] (p 1.000) | 79.9 [67] (p 1.000) |
| tu_choi | 10.7 [75] | 9.3 [75] (p 0.317) | 10.7 [75] (p 1.000) | 10.7 [75] (p 1.000) |
| Từ chối đúng | 98.1 [107] | 98.1 [107] (p 1.000) | 98.1 [107] (p 1.000) | 98.1 [107] (p 1.000) |
| Vi phạm số sau sửa (TB/câu) | 0.06 [115] | 0.10 [115] (p 0.986) | 0.06 [115] (p 1.000) | 0.07 [115] (p 0.993) |
| Câu văn bị bỏ (TB/câu) | 0.03 [115] | 0.08 [115] (p 0.557) | 0.03 [115] (p 1.000) | 0.06 [115] (p 0.157) |

| Từ chối | G | refusal_v2 | no_tau | repair_m12 |
|---|---|---|---|---|
| precision | 95.8 | 97.8 | 95.8 | 95.8 |
| precision_oos | 83.3 | 84.8 | 83.3 | 83.3 |
| recall | 100.0 | 97.5 | 100.0 | 100.0 |
| tu_choi_gold_rong | 75.0 | 75.0 | 75.0 | 75.0 |
| tu_choi_sai | 3.0 | 1.5 | 3.0 | 3.0 |

Loại câu: theo_thoi_diem · n = 20

| Chỉ số | G | refusal_v2 | no_tau | repair_m12 |
|---|---|---|---|---|
| Judge: đúng hoàn toàn | 60.0 [20] | 65.0 [20] (p 1.000) | 60.0 [20] (p 1.000) | 60.0 [20] (p 1.000) |
| Judge: điểm TB (0–2) | 1.45 [20] | 1.50 [20] (p 0.317) | 1.45 [20] (p 1.000) | 1.45 [20] (p 1.000) |
| Có trích dẫn tới gold | 83.3 [12] | 83.3 [12] (p 1.000) | 83.3 [12] (p 1.000) | 83.3 [12] (p 1.000) |
| Đúng phiên bản (theo thời điểm) | 90.0 [20] | 90.0 [20] (p 1.000) | 90.0 [20] (p 1.000) | 90.0 [20] (p 1.000) |
| Recall@5 | 91.7 [12] | 91.7 [12] (p 1.000) | 91.7 [12] (p 1.000) | 91.7 [12] (p 1.000) |
| tu_choi | 35.0 [20] | 35.0 [20] (p 1.000) | 35.0 [20] (p 1.000) | 35.0 [20] (p 1.000) |
| Từ chối đúng | 91.7 [12] | 91.7 [12] (p 1.000) | 91.7 [12] (p 1.000) | 91.7 [12] (p 1.000) |
| Vi phạm số sau sửa (TB/câu) | 0.00 [20] | 0.00 [20] (p 1.000) | 0.00 [20] (p 1.000) | 0.00 [20] (p 1.000) |
| Câu văn bị bỏ (TB/câu) | 0.00 [20] | 0.00 [20] (p 1.000) | 0.00 [20] (p 1.000) | 0.00 [20] (p 1.000) |

| Từ chối | G | refusal_v2 | no_tau | repair_m12 |
|---|---|---|---|---|
| precision | 85.7 | 85.7 | 85.7 | 85.7 |
| precision_oos | 0.0 | 0.0 | 0.0 | 0.0 |
| recall | — | — | — | — |
| tu_choi_gold_rong | 75.0 | 75.0 | 75.0 | 75.0 |
| tu_choi_sai | 8.3 | 8.3 | 8.3 | 8.3 |

Loại câu: muc_phat, tru_diem, so_sanh · n = 23

| Chỉ số | G | refusal_v2 | no_tau | repair_m12 |
|---|---|---|---|---|
| Judge: đúng hoàn toàn | 47.8 [23] | 43.5 [23] (p 1.000) | 47.8 [23] (p 1.000) | 52.2 [23] (p 1.000) |
| Judge: điểm TB (0–2) | 1.22 [23] | 1.13 [23] (p 0.625) | 1.22 [23] (p 1.000) | 1.26 [23] (p 0.317) |
| Đủ con số yêu cầu | 65.2 [23] | 65.2 [23] (p 1.000) | 65.2 [23] (p 1.000) | 60.9 [23] (p 1.000) |
| Recall con số | 73.2 [23] | 73.2 [23] (p 1.000) | 73.2 [23] (p 1.000) | 68.8 [23] (p 0.317) |
| Có trích dẫn tới gold | 65.2 [23] | 65.2 [23] (p 1.000) | 65.2 [23] (p 1.000) | 60.9 [23] (p 1.000) |
| Recall@5 | 89.1 [23] | 89.1 [23] (p 1.000) | 89.1 [23] (p 1.000) | 89.1 [23] (p 1.000) |
| tu_choi | 4.3 [23] | 0.0 [23] (p 0.317) | 4.3 [23] (p 1.000) | 4.3 [23] (p 1.000) |
| Từ chối đúng | 95.7 [23] | 100.0 [23] (p 1.000) | 95.7 [23] (p 1.000) | 95.7 [23] (p 1.000) |
| Vi phạm số sau sửa (TB/câu) | 0.17 [23] | 0.26 [23] (p 0.975) | 0.17 [23] (p 1.000) | 0.26 [23] (p 0.546) |
| Câu văn bị bỏ (TB/câu) | 0.13 [23] | 0.26 [23] (p 0.975) | 0.13 [23] (p 1.000) | 0.26 [23] (p 0.157) |

| Từ chối | G | refusal_v2 | no_tau | repair_m12 |
|---|---|---|---|---|
| precision | 0.0 | — | 0.0 | 0.0 |
| precision_oos | 0.0 | — | 0.0 | 0.0 |
| recall | — | — | — | — |
| tu_choi_gold_rong | — | — | — | — |
| tu_choi_sai | 4.3 | 0.0 | 4.3 | 4.3 |

## Phiên GPU 10 (18/11/2026)

aidev gói Pro, cổng 20161, RTX 3090, vLLM 0.33.0 (venv vLLM + trọng số tải bằng aria2c, `hf_fetch.py`, ~10 phút dựng máy). Analyzer 74/115 câu gọi LLM (12 s); truy hồi `--gpu` 5 cấu hình × 115 câu; sinh 9 lượt chạy × 115 câu = 1.035 lượt `qwen3-14b-awq` (0 lỗi); judge `mistral-small-3.2` 9 × 75 lượt LLM + câu ngoài phạm vi chấm luật. Máy bật ~45 phút ≈ 13.000 VND. Dry-run ước 0,7 giờ GPU tính toán.

## Hạn chế

- Dev nhỏ (32 câu đa bước, 75 câu có đáp án) ⇒ chênh lệch vài câu không phân biệt được; 81% câu dev do Claude sửa từ nháp.
- p thô, nhiều biến thể ⇒ p 0,046 của `ctx_all` không còn ý nghĩa sau hiệu chỉnh bội; biến thể đó lại được thêm sau khi xem dev.
- Sửa chỉ số từ chối được phát hiện trên dev nhưng áp lên cả số test đã báo (chỉ đổi cách tính, không đổi hệ thống).
