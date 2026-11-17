# Bộ dữ liệu hỏi–đáp (M9)

- Cập nhật: 2026-11-17T11:40:25+07:00 · commit `1715e4028324aedf2932361dd388ca48eab808b9-dirty`
- `qa_version` = `14030bf711637376` (hash test/train/val/subsets) · `data_version` = `f3297e64b9e44855`
- subsets: **missing**

| Split | Dòng | sha256 | Kiểm tra lần cuối | Lỗi | Cảnh báo |
| --- | ---: | --- | --- | ---: | ---: |
| test | 427 | `1334304fffbb` | 2026-11-17T11:40:25+07:00 | 0 | 13 |
| train | 8,566 | `2068aaef94c4` | 2026-11-10T10:52:32+07:00 | 0 | 0 |
| val | 489 | `51b164307a32` | 2026-11-10T10:52:33+07:00 | 0 | 7 |

## Phân bổ test so với hạn mức

| Loại | Có | Hạn mức |
| --- | ---: | ---: |
| muc_phat | 80 | 80 |
| tru_diem | 21 | 30 |
| bien_phap | 35 | 35 |
| hanh_vi_cam_nghia_vu | 70 | 70 |
| dinh_nghia | 38 | 40 |
| thu_tuc_tham_quyen | 70 | 70 |
| theo_thoi_diem | 40 | 50 |
| da_buoc | 59 | 60 |
| so_sanh | 14 | 30 |
| ngoai_pham_vi | 0 | 35 |

| Tier | Có | Hạn mức |
| --- | ---: | ---: |
| A | 345 | 326 |
| B | 63 | 93 |
| C | 11 | 23 |
| historical | 8 | 23 |

Tier × loại: {"A|bien_phap": 31, "A|da_buoc": 43, "A|dinh_nghia": 31, "A|hanh_vi_cam_nghia_vu": 56, "A|muc_phat": 70, "A|so_sanh": 12, "A|theo_thoi_diem": 22, "A|thu_tuc_tham_quyen": 59, "A|tru_diem": 21, "B|bien_phap": 4, "B|da_buoc": 10, "B|dinh_nghia": 7, "B|hanh_vi_cam_nghia_vu": 8, "B|muc_phat": 10, "B|so_sanh": 2, "B|theo_thoi_diem": 16, "B|thu_tuc_tham_quyen": 6, "C|da_buoc": 3, "C|hanh_vi_cam_nghia_vu": 3, "C|theo_thoi_diem": 2, "C|thu_tuc_tham_quyen": 3, "historical|da_buoc": 3, "historical|hanh_vi_cam_nghia_vu": 3, "historical|thu_tuc_tham_quyen": 2}

## train/val

- Dựng 2026-11-10T10:52:29+07:00 bằng `mistral-small-3.2`: train 8,566, val 489; lọc rò rỉ theo test `` — **test đã đổi, chạy `qa_tool build`**
- Xem `data/qa/generate_summary.md`.
