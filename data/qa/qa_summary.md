# Bộ dữ liệu hỏi–đáp (M9)

- Cập nhật: 2026-11-17T15:48:03+07:00 · commit `9d4456f7429c20613d278b90915acda8a07d1d5d-dirty`
- `qa_version` = `577552bd95231c6f` (hash test/train/val/subsets) · `data_version` = `f3297e64b9e44855`
- subsets: **stale**

| Split | Dòng | sha256 | Kiểm tra lần cuối | Lỗi | Cảnh báo |
| --- | ---: | --- | --- | ---: | ---: |
| test | 340 | `b402c5cf4b0e` | 2026-11-17T15:48:03+07:00 | 0 | 6 |
| train | 8,566 | `cb3084f18748` | 2026-11-17T12:08:57+07:00 | 0 | 0 |
| val | 489 | `3502ccfbd1c9` | 2026-11-17T12:08:58+07:00 | 0 | 7 |

## Phân bổ test so với hạn mức

| Loại | Có | Hạn mức |
| --- | ---: | ---: |
| muc_phat | 65 | 80 |
| tru_diem | 24 | 30 |
| bien_phap | 15 | 35 |
| hanh_vi_cam_nghia_vu | 48 | 70 |
| dinh_nghia | 35 | 40 |
| thu_tuc_tham_quyen | 52 | 70 |
| theo_thoi_diem | 24 | 50 |
| da_buoc | 30 | 60 |
| so_sanh | 12 | 30 |
| ngoai_pham_vi | 35 | 35 |

| Tier | Có | Hạn mức |
| --- | ---: | ---: |
| A | 231 | 326 |
| B | 53 | 93 |
| C | 10 | 23 |
| historical | 11 | 23 |

Tier × loại: {"-|ngoai_pham_vi": 35, "A|bien_phap": 15, "A|da_buoc": 22, "A|dinh_nghia": 26, "A|hanh_vi_cam_nghia_vu": 31, "A|muc_phat": 53, "A|so_sanh": 9, "A|theo_thoi_diem": 16, "A|thu_tuc_tham_quyen": 35, "A|tru_diem": 24, "B|da_buoc": 2, "B|dinh_nghia": 9, "B|hanh_vi_cam_nghia_vu": 9, "B|muc_phat": 12, "B|so_sanh": 3, "B|theo_thoi_diem": 8, "B|thu_tuc_tham_quyen": 10, "C|da_buoc": 2, "C|hanh_vi_cam_nghia_vu": 4, "C|thu_tuc_tham_quyen": 4, "historical|da_buoc": 4, "historical|hanh_vi_cam_nghia_vu": 4, "historical|thu_tuc_tham_quyen": 3}

## train/val

- Dựng 2026-11-17T12:08:34+07:00 bằng `mistral-small-3.2`: train 8,566, val 489; lọc rò rỉ theo test `6f2470990b1f` — **test đã đổi, chạy `qa_tool build`**
- Xem `data/qa/generate_summary.md`.
