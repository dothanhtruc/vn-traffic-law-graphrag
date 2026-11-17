# Bộ dữ liệu hỏi–đáp (M9)

- Cập nhật: 2026-11-17T11:28:08+07:00 · commit `1792cd26d80d9550b3effae8b25de50393226abb-dirty`
- `qa_version` = `a23d2cca9725b36a` (hash test/train/val/subsets) · `data_version` = `f3297e64b9e44855`
- subsets: **missing**

| Split | Dòng | sha256 | Kiểm tra lần cuối | Lỗi | Cảnh báo |
| --- | ---: | --- | --- | ---: | ---: |
| test | 273 | `22737d5ebff1` | 2026-11-17T11:28:08+07:00 | 0 | 7 |
| train | 8,566 | `2068aaef94c4` | 2026-11-10T10:52:32+07:00 | 0 | 0 |
| val | 489 | `51b164307a32` | 2026-11-10T10:52:33+07:00 | 0 | 7 |

## Phân bổ test so với hạn mức

| Loại | Có | Hạn mức |
| --- | ---: | ---: |
| muc_phat | 60 | 80 |
| tru_diem | 16 | 30 |
| bien_phap | 21 | 35 |
| hanh_vi_cam_nghia_vu | 51 | 70 |
| dinh_nghia | 21 | 40 |
| thu_tuc_tham_quyen | 41 | 70 |
| theo_thoi_diem | 14 | 50 |
| da_buoc | 35 | 60 |
| so_sanh | 14 | 30 |
| ngoai_pham_vi | 0 | 35 |

| Tier | Có | Hạn mức |
| --- | ---: | ---: |
| A | 215 | 326 |
| B | 44 | 93 |
| C | 7 | 23 |
| historical | 7 | 23 |

Tier × loại: {"A|bien_phap": 18, "A|da_buoc": 26, "A|dinh_nghia": 18, "A|hanh_vi_cam_nghia_vu": 37, "A|muc_phat": 50, "A|so_sanh": 12, "A|theo_thoi_diem": 8, "A|thu_tuc_tham_quyen": 30, "A|tru_diem": 16, "B|bien_phap": 3, "B|da_buoc": 6, "B|dinh_nghia": 3, "B|hanh_vi_cam_nghia_vu": 8, "B|muc_phat": 10, "B|so_sanh": 2, "B|theo_thoi_diem": 6, "B|thu_tuc_tham_quyen": 6, "C|da_buoc": 1, "C|hanh_vi_cam_nghia_vu": 3, "C|thu_tuc_tham_quyen": 3, "historical|da_buoc": 2, "historical|hanh_vi_cam_nghia_vu": 3, "historical|thu_tuc_tham_quyen": 2}

## train/val

- Dựng 2026-11-10T10:52:29+07:00 bằng `mistral-small-3.2`: train 8,566, val 489; lọc rò rỉ theo test `` — **test đã đổi, chạy `qa_tool build`**
- Xem `data/qa/generate_summary.md`.
