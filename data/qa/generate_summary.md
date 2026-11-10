# Sinh dữ liệu train/val (M9)

- Dựng lúc 2026-11-10T10:52:29+07:00 · commit `f0bac4e742bdd161b40ac2b5cf5da7145f4cd7d0-dirty` · model `mistral-small-3.2` · prompt `603e12db4b7a` · schema `415b103e5f9f`
- test.jsonl lúc dựng: `` (0 câu) · data_version `f3297e64b9e4`
- Chunk: 3,775 (3,773 text khác nhau), đã sinh 3,773
- Câu thô: 11,319 → train 8,566 (764 Điều) · val 489 (44 Điều)
- Positive thuộc gold_units của test (đánh dấu `in_test_gold`, không loại): 0

## Bị loại

| Lý do | Số |
| --- | ---: |
| chep_nguyen_van | 1,444 |
| hoi_che_tai_khong_co | 164 |
| khong_lien_quan | 26 |
| qua_ngan | 2 |
| so_khong_co_trong_unit | 70 |
| tham_chieu_ngu_canh | 164 |
| trung_lap | 388 |
| trung_trong_chunk | 6 |

## Loại câu

| Loại | train | val |
| --- | ---: | ---: |
| bien_phap | 575 | 29 |
| dinh_nghia | 1,498 | 57 |
| hanh_vi_cam_nghia_vu | 3,043 | 183 |
| khac | 2 | 0 |
| muc_phat | 464 | 17 |
| thu_tuc_tham_quyen | 2,896 | 200 |
| tru_diem | 88 | 3 |

## Tier

| Tier | train | val |
| --- | ---: | ---: |
| A | 4,716 | 214 |
| B | 2,904 | 199 |
| C | 485 | 42 |
| historical | 461 | 34 |

## Lượt gọi LLM (khoá chạy hiện hành)

- Bản ghi theo trạng thái: {'ok': 3773}
- Lượt không cache: 3773 · latency median 5270 ms · max 10056 ms
- Token: {'prompt_tokens': 5019769, 'completion_tokens': 497918, 'total_tokens': 5517687}

- Lần chạy 2026-11-10T10:24:22+07:00: 32 lượt, {'ok': 32}, 11.9 s, workers 16
- Lần chạy 2026-11-10T10:25:38+07:00: 64 lượt, {'ok': 64}, 20.6 s, workers 16
- Lần chạy 2026-11-10T10:26:12+07:00: 3709 lượt, {'ok': 3709}, 1247.0 s, workers 16
