# Bộ dữ liệu hỏi–đáp (M9)

- Cập nhật: 2026-11-17T16:14:31+07:00 · commit `28856bc67f44b75d6e57e6d86af31a5fac16afde-dirty`
- `qa_version` = `11d6d36ce4beb66a` (hash test/train/val/subsets) · `data_version` = `f3297e64b9e44855`
- subsets: **ok**

| Split | Dòng | sha256 | Kiểm tra lần cuối | Lỗi | Cảnh báo |
| --- | ---: | --- | --- | ---: | ---: |
| test | 500 | `9a9b8113cffc` | 2026-11-17T16:14:28+07:00 | 0 | 23 |
| train | 8,566 | `f69eb662e962` | 2026-11-17T16:14:31+07:00 | 0 | 0 |
| val | 489 | `9042a9de49f0` | 2026-11-17T16:14:31+07:00 | 0 | 7 |

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
| A | 306 | 326 |
| B | 105 | 93 |
| C | 27 | 23 |
| historical | 27 | 23 |

Tier × loại: {"-|ngoai_pham_vi": 35, "A|bien_phap": 31, "A|da_buoc": 38, "A|dinh_nghia": 29, "A|hanh_vi_cam_nghia_vu": 33, "A|muc_phat": 61, "A|so_sanh": 25, "A|theo_thoi_diem": 24, "A|thu_tuc_tham_quyen": 35, "A|tru_diem": 30, "B|bien_phap": 4, "B|da_buoc": 12, "B|dinh_nghia": 11, "B|hanh_vi_cam_nghia_vu": 18, "B|muc_phat": 19, "B|so_sanh": 5, "B|theo_thoi_diem": 20, "B|thu_tuc_tham_quyen": 16, "C|da_buoc": 5, "C|hanh_vi_cam_nghia_vu": 10, "C|theo_thoi_diem": 2, "C|thu_tuc_tham_quyen": 10, "historical|da_buoc": 5, "historical|hanh_vi_cam_nghia_vu": 9, "historical|theo_thoi_diem": 4, "historical|thu_tuc_tham_quyen": 9}

## train/val

- Dựng 2026-11-17T16:14:20+07:00 bằng `mistral-small-3.2`: train 8,566, val 489; lọc rò rỉ theo test `9a9b8113cffc`
- Xem `data/qa/generate_summary.md`.
