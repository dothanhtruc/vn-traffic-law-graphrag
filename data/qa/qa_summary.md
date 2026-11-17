# Bộ dữ liệu hỏi–đáp (M9)

- Cập nhật: 2026-11-17T12:17:57+07:00 · commit `f3d762528e28420eddfe3d3cad0649695feedc5e-dirty`
- `qa_version` = `37af4714b512df81` (hash test/train/val/subsets) · `data_version` = `f3297e64b9e44855`
- subsets: **stale**

| Split | Dòng | sha256 | Kiểm tra lần cuối | Lỗi | Cảnh báo |
| --- | ---: | --- | --- | ---: | ---: |
| test | 493 | `bb011dd4897d` | 2026-11-17T12:17:57+07:00 | 0 | 14 |
| train | 8,566 | `cb3084f18748` | 2026-11-17T12:08:57+07:00 | 0 | 0 |
| val | 489 | `3502ccfbd1c9` | 2026-11-17T12:08:58+07:00 | 0 | 7 |

## Phân bổ test so với hạn mức

| Loại | Có | Hạn mức |
| --- | ---: | ---: |
| muc_phat | 80 | 80 |
| tru_diem | 30 | 30 |
| bien_phap | 31 | 35 |
| hanh_vi_cam_nghia_vu | 70 | 70 |
| dinh_nghia | 40 | 40 |
| thu_tuc_tham_quyen | 70 | 70 |
| theo_thoi_diem | 48 | 50 |
| da_buoc | 60 | 60 |
| so_sanh | 29 | 30 |
| ngoai_pham_vi | 35 | 35 |

| Tier | Có | Hạn mức |
| --- | ---: | ---: |
| A | 327 | 326 |
| B | 87 | 93 |
| C | 22 | 23 |
| historical | 22 | 23 |

Tier × loại: {"-|ngoai_pham_vi": 35, "A|bien_phap": 27, "A|da_buoc": 38, "A|dinh_nghia": 30, "A|hanh_vi_cam_nghia_vu": 42, "A|muc_phat": 65, "A|so_sanh": 25, "A|theo_thoi_diem": 22, "A|thu_tuc_tham_quyen": 48, "A|tru_diem": 30, "B|bien_phap": 4, "B|da_buoc": 14, "B|dinh_nghia": 10, "B|hanh_vi_cam_nghia_vu": 13, "B|muc_phat": 15, "B|so_sanh": 4, "B|theo_thoi_diem": 20, "B|thu_tuc_tham_quyen": 7, "C|da_buoc": 3, "C|hanh_vi_cam_nghia_vu": 9, "C|theo_thoi_diem": 2, "C|thu_tuc_tham_quyen": 8, "historical|da_buoc": 5, "historical|hanh_vi_cam_nghia_vu": 6, "historical|theo_thoi_diem": 4, "historical|thu_tuc_tham_quyen": 7}

## train/val

- Dựng 2026-11-17T12:08:34+07:00 bằng `mistral-small-3.2`: train 8,566, val 489; lọc rò rỉ theo test `6f2470990b1f` — **test đã đổi, chạy `qa_tool build`**
- Xem `data/qa/generate_summary.md`.
