# Bộ dữ liệu hỏi–đáp (M9)

- Cập nhật: 2026-11-17T12:04:17+07:00 · commit `e1a18a1d813fb9fbeb7315856411c841c3235bdb-dirty`
- `qa_version` = `3ec030271183e98d` (hash test/train/val/subsets) · `data_version` = `f3297e64b9e44855`
- subsets: **missing**

| Split | Dòng | sha256 | Kiểm tra lần cuối | Lỗi | Cảnh báo |
| --- | ---: | --- | --- | ---: | ---: |
| test | 500 | `e2dae2b1b412` | 2026-11-17T12:04:17+07:00 | 0 | 15 |
| train | 8,566 | `2068aaef94c4` | 2026-11-10T10:52:32+07:00 | 0 | 0 |
| val | 489 | `51b164307a32` | 2026-11-10T10:52:33+07:00 | 0 | 7 |

## Phân bổ test so với hạn mức

| Loại | Có | Hạn mức |
| --- | ---: | ---: |
| muc_phat | 80 | 80 |
| tru_diem | 30 | 30 |
| bien_phap | 35 | 35 |
| hanh_vi_cam_nghia_vu | 70 | 70 |
| dinh_nghia | 40 | 40 |
| thu_tuc_tham_quyen | 70 | 70 |
| theo_thoi_diem | 50 | 50 |
| da_buoc | 60 | 60 |
| so_sanh | 30 | 30 |
| ngoai_pham_vi | 35 | 35 |

| Tier | Có | Hạn mức |
| --- | ---: | ---: |
| A | 329 | 326 |
| B | 90 | 93 |
| C | 23 | 23 |
| historical | 23 | 23 |

Tier × loại: {"-|ngoai_pham_vi": 35, "A|bien_phap": 30, "A|da_buoc": 39, "A|dinh_nghia": 31, "A|hanh_vi_cam_nghia_vu": 42, "A|muc_phat": 64, "A|so_sanh": 25, "A|theo_thoi_diem": 22, "A|thu_tuc_tham_quyen": 46, "A|tru_diem": 30, "B|bien_phap": 5, "B|da_buoc": 10, "B|dinh_nghia": 9, "B|hanh_vi_cam_nghia_vu": 14, "B|muc_phat": 16, "B|so_sanh": 5, "B|theo_thoi_diem": 22, "B|thu_tuc_tham_quyen": 9, "C|da_buoc": 6, "C|hanh_vi_cam_nghia_vu": 7, "C|theo_thoi_diem": 2, "C|thu_tuc_tham_quyen": 8, "historical|da_buoc": 5, "historical|hanh_vi_cam_nghia_vu": 7, "historical|theo_thoi_diem": 4, "historical|thu_tuc_tham_quyen": 7}

## train/val

- Dựng 2026-11-10T10:52:29+07:00 bằng `mistral-small-3.2`: train 8,566, val 489; lọc rò rỉ theo test `` — **test đã đổi, chạy `qa_tool build`**
- Xem `data/qa/generate_summary.md`.
