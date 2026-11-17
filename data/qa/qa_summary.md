# Bộ dữ liệu hỏi–đáp (M9)

- Cập nhật: 2026-11-17T11:49:17+07:00 · commit `7556932381d91c049a109edbdce681fec29524da-dirty`
- `qa_version` = `23d7ea73f46574a8` (hash test/train/val/subsets) · `data_version` = `f3297e64b9e44855`
- subsets: **missing**

| Split | Dòng | sha256 | Kiểm tra lần cuối | Lỗi | Cảnh báo |
| --- | ---: | --- | --- | ---: | ---: |
| test | 464 | `84d4de5f494a` | 2026-11-17T11:49:17+07:00 | 0 | 15 |
| train | 8,566 | `2068aaef94c4` | 2026-11-10T10:52:32+07:00 | 0 | 0 |
| val | 489 | `51b164307a32` | 2026-11-10T10:52:33+07:00 | 0 | 7 |

## Phân bổ test so với hạn mức

| Loại | Có | Hạn mức |
| --- | ---: | ---: |
| muc_phat | 80 | 80 |
| tru_diem | 29 | 30 |
| bien_phap | 35 | 35 |
| hanh_vi_cam_nghia_vu | 70 | 70 |
| dinh_nghia | 40 | 40 |
| thu_tuc_tham_quyen | 70 | 70 |
| theo_thoi_diem | 50 | 50 |
| da_buoc | 60 | 60 |
| so_sanh | 30 | 30 |
| ngoai_pham_vi | 0 | 35 |

| Tier | Có | Hạn mức |
| --- | ---: | ---: |
| A | 371 | 326 |
| B | 70 | 93 |
| C | 11 | 23 |
| historical | 12 | 23 |

Tier × loại: {"A|bien_phap": 31, "A|da_buoc": 44, "A|dinh_nghia": 33, "A|hanh_vi_cam_nghia_vu": 56, "A|muc_phat": 70, "A|so_sanh": 25, "A|theo_thoi_diem": 24, "A|thu_tuc_tham_quyen": 59, "A|tru_diem": 29, "B|bien_phap": 4, "B|da_buoc": 10, "B|dinh_nghia": 7, "B|hanh_vi_cam_nghia_vu": 8, "B|muc_phat": 10, "B|so_sanh": 5, "B|theo_thoi_diem": 20, "B|thu_tuc_tham_quyen": 6, "C|da_buoc": 3, "C|hanh_vi_cam_nghia_vu": 3, "C|theo_thoi_diem": 2, "C|thu_tuc_tham_quyen": 3, "historical|da_buoc": 3, "historical|hanh_vi_cam_nghia_vu": 3, "historical|theo_thoi_diem": 4, "historical|thu_tuc_tham_quyen": 2}

## train/val

- Dựng 2026-11-10T10:52:29+07:00 bằng `mistral-small-3.2`: train 8,566, val 489; lọc rò rỉ theo test `` — **test đã đổi, chạy `qa_tool build`**
- Xem `data/qa/generate_summary.md`.
