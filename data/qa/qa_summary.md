# Bộ dữ liệu hỏi–đáp (M9)

- Cập nhật: 2026-11-10T10:53:38+07:00 · commit `f0bac4e742bdd161b40ac2b5cf5da7145f4cd7d0-dirty`
- `qa_version` = `692d8987a07f8aab` (hash test/train/val/subsets) · `data_version` = `f3297e64b9e44855`
- subsets: **missing**

| Split | Dòng | sha256 | Kiểm tra lần cuối | Lỗi | Cảnh báo |
| --- | ---: | --- | --- | ---: | ---: |
| test | 0 | `` | 2026-11-10T10:52:32+07:00 | 0 | 0 |
| train | 8,566 | `2068aaef94c4` | 2026-11-10T10:52:32+07:00 | 0 | 0 |
| val | 489 | `51b164307a32` | 2026-11-10T10:52:33+07:00 | 0 | 7 |

## Phân bổ test so với hạn mức

| Loại | Có | Hạn mức |
| --- | ---: | ---: |
| muc_phat | 0 | 80 |
| tru_diem | 0 | 30 |
| bien_phap | 0 | 35 |
| hanh_vi_cam_nghia_vu | 0 | 70 |
| dinh_nghia | 0 | 40 |
| thu_tuc_tham_quyen | 0 | 70 |
| theo_thoi_diem | 0 | 50 |
| da_buoc | 0 | 60 |
| so_sanh | 0 | 30 |
| ngoai_pham_vi | 0 | 35 |

| Tier | Có | Hạn mức |
| --- | ---: | ---: |
| A | 0 | 326 |
| B | 0 | 93 |
| C | 0 | 23 |
| historical | 0 | 23 |

Tier × loại: {}

## train/val

- Dựng 2026-11-10T10:52:29+07:00 bằng `mistral-small-3.2`: train 8,566, val 489; lọc rò rỉ theo test ``
- Xem `data/qa/generate_summary.md`.
