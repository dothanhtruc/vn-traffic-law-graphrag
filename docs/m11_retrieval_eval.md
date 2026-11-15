# M11 — Đánh giá truy hồi (tóm tắt)

> Bản commit của `data/index/retrieval_eval.md` (sinh bởi `scripts.retrieve --eval val,train_1000 --configs B1,B2,B3,G,A1,A2 --gpu`, phiên GPU 5, 15/11/2026). **Không dùng test.** Chạy lại ở local từ cache (Release `m11-retrieval-v1`) cho ra đúng mọi chỉ số (0 lệch).

## Kết luận chính

- **Rerank** (AITeamVN/Vietnamese_Reranker@f536976, logit thô, cửa sổ ≤ 512 token, điểm = max cửa sổ) là bước tăng lớn nhất: val R@5 86,9 (BM25) / 86,5 (vector) → **93,0** (B3), MRR@10 71,8 → 82,2; train_1000 R@5 84,9 → 89,8.
- **Lọc hiệu lực** (A2 bỏ lọc): 18,9% (val) / 15,8% (train) chunk trong top-5 là trạng thái hết hiệu lực hoặc chưa có hiệu lực; MRR@10 giảm 6,2 / 4,4 điểm, R@1 giảm ~10 / 6 điểm. G và B3 có 0% chunk ngoài hiệu lực.
- **Graph expand** (G so với A1 = B3 + analyzer): đưa ~99% đơn vị liên kết vào pool (từ 26% ở B3), nhưng reranker hiếm khi đẩy chúng vào top-5 vì câu val/train sinh từ một chunk không nhắc nội dung chunk liên kết: R@5 gold 92,8 so với 93,0 (val), 89,4 so với 89,8 (train) — trong CI; liên kết@10 34,2 so với 28,7 (val), 43,3 so với 39,3 (train); chế tài nối `dan_chieu` ở train: liên kết@5 17,3 so với 10,2. Mô phỏng dành 1 chỗ top-5 cho chunk đồ thị: R@5 −1,3 đến −1,8, liên kết@5 +4 đến +10 điểm ⇒ **người dùng chốt giữ rerank tự do** (`reserved_graph_slots: 0`), đánh giá G chính thức ở M13 trên test.
- **Analyzer**: rule chắc chắn cho ~50% câu; 740 câu gọi LLM `qwen3-14b-awq` (1 `format_error` → giữ rule), 135 s GPU.
- **Chi phí**: pha retrieve/rerank 0,20 giờ GPU ≈ 3.440 VND (75.603 cửa sổ, ~174 cửa sổ/s, VRAM đỉnh 1,4 GB); pha analyze ~2 phút; cả phiên (setup bằng `--curl-wheels`, nạp vLLM, sự cố tokenizer reranker) ~1 giờ.
- **Hạn chế**: câu val/train do mistral-small-3.2 sinh từ chính chunk ⇒ thiên lệch từ vựng có lợi cho BM25/rerank và không đo được lợi ích đa bước; số tuyệt đối không phản ánh câu hỏi thật.

---

# Đánh giá truy hồi M11 (val + tập con train — KHÔNG dùng test)

Sinh lúc 2026-11-15T09:48:43+07:00 · commit `a98aa7a2e50db474656d723e505d6ada84cb31a9` · 3853 chunk (catalog `eaff1f5ec42a`) · data_version `f3297e64b9e4` · graph `b1bd47f0fc08`

Embedding: {"aiteamvn-vi-emb": {"hf_repo": "AITeamVN/Vietnamese_Embedding", "revision": "dea33aa1ab339f38d66ae0a40e6c40e0a9249568"}} · reranker: {"aiteamvn-reranker": {"hf_repo": "AITeamVN/Vietnamese_Reranker", "revision": "f536976248403314225d7fdfdbc87f0e9516a54e", "max_length": 512}} · LLM analyzer: `qwen3-14b-awq` (prompt `c01a4f23e8c5`).

Chunk đúng = chunk hiệu lực tại as_of chứa gold unit; R@k cấp unit; CI 95% bootstrap 1.000 lần theo câu (seed 42). **Liên kết@k** = tỷ lệ đơn vị liên kết của gold (Khoản chế tài nối bằng BI_XU_PHAT/BI_TRU_DIEM `dan_chieu`; DAN_CHIEU sang Điều khác) có chunk trong top-k — đo lợi ích graph expand trên câu một chunk; đánh giá G chính thức là việc của M13 trên test. Câu val/train do mistral-small-3.2 sinh từ chính chunk ⇒ thiên lệch từ vựng.

## val (489 câu)

| Cấu hình | R@1 | R@5 | CI R@5 | R@10 | R@20 | MRR@10 | CI MRR | nDCG@10 | Liên kết@5 (n) | Liên kết@10 | Top-5 ngoài hiệu lực | Top-5 chỉ từ đồ thị | Chunk mở rộng/câu |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| B1 | 60.7 | 86.9 | 84.0–89.8 | 92.6 | 95.7 | 71.8 | 68.5–75.3 | 76.9 | 14.1 (74) | 25.7 | 0.0 | 0.0 | 0.0 |
| B2 | 60.9 | 86.5 | 83.2–89.6 | 92.0 | 95.3 | 71.4 | 68.0–74.9 | 76.4 | 22.2 (74) | 28.6 | 0.0 | 0.0 | 0.0 |
| B3 | 74.4 | 93.0 | 90.8–95.3 | 95.7 | 97.1 | 82.2 | 79.4–85.0 | 85.5 | 21.8 (74) | 28.7 | 0.0 | 0.0 | 0.0 |
| G | 74.4 | 92.8 | 90.6–95.1 | 95.3 | 96.7 | 82.1 | 79.3–84.9 | 85.4 | 20.1 (74) | 34.2 | 0.0 | 4.0 | 15.8 |
| A1 | 74.4 | 93.0 | 90.8–95.3 | 95.7 | 97.1 | 82.2 | 79.4–85.0 | 85.5 | 21.8 (74) | 28.7 | 0.0 | 0.0 | 0.0 |
| A2 | 64.2 | 91.8 | 89.2–94.1 | 94.9 | 96.3 | 76.0 | 73.1–79.1 | 80.7 | 13.9 (74) | 29.6 | 18.9 | 3.5 | 17.8 |

**R@5 theo tier** (n):

| Cấu hình | A | B | C | historical |
| --- | ---: | ---: | ---: | ---: |
| B1 | 87.4 (214) | 82.9 (199) | 100.0 (42) | 91.2 (34) |
| B2 | 88.8 (214) | 84.9 (199) | 81.0 (42) | 88.2 (34) |
| B3 | 93.9 (214) | 91.5 (199) | 97.6 (42) | 91.2 (34) |
| G | 93.5 (214) | 91.5 (199) | 97.6 (42) | 91.2 (34) |
| A1 | 93.9 (214) | 91.5 (199) | 97.6 (42) | 91.2 (34) |
| A2 | 92.5 (214) | 89.4 (199) | 97.6 (42) | 94.1 (34) |

**Liên kết theo loại** (top-5: độ phủ, số liên kết):

- B1: che_tai 25.0 (n=4); dan_chieu 7.9 (n=215)
- B2: che_tai 0.0 (n=4); dan_chieu 12.6 (n=215)
- B3: che_tai 0.0 (n=4); dan_chieu 13.5 (n=215)
- G: che_tai 0.0 (n=4); dan_chieu 13.0 (n=215)
- A1: che_tai 0.0 (n=4); dan_chieu 13.5 (n=215)
- A2: che_tai 0.0 (n=4); dan_chieu 8.4 (n=215)

**Analyzer + latency (ms, p50/p95):**

- B1: gọi LLM 0.0% · {'disabled': 249, 'khong_goi': 240} · analyze 0.39/0.52, final_check 0.42/0.48, hybrid 8.0/12.76, total 9.09/13.86
- B2: gọi LLM 0.0% · {'disabled': 249, 'khong_goi': 240} · analyze 0.39/0.54, encode 0.06/0.08, final_check 0.43/0.49, hybrid 4.09/4.88, total 5.22/6.05
- B3: gọi LLM 0.0% · {'disabled': 249, 'khong_goi': 240} · analyze 0.44/0.61, encode 0.08/0.1, final_check 0.49/0.57, hybrid 13.83/18.96, rerank 141.55/211.5, total 156.78/227.14
- G: gọi LLM 50.9% · {'ok': 249, 'khong_goi': 240} · analyze 0.89/1.17, encode 0.08/0.1, expand 5.42/10.76, final_check 0.76/1.15, hybrid 13.69/18.98, rerank 109.32/313.04, total 134.2/346.21
- A1: gọi LLM 50.9% · {'ok': 249, 'khong_goi': 240} · analyze 0.82/1.08, encode 0.06/0.08, final_check 0.44/0.51, hybrid 12.95/17.96, rerank 0.38/0.46, total 14.9/20.03
- A2: gọi LLM 50.9% · {'ok': 249, 'khong_goi': 240} · analyze 0.86/1.17, encode 0.07/0.1, expand 4.83/8.72, hybrid 13.62/18.69, rerank 73.93/206.85, total 93.52/231.71

## train_1000 (1000 câu)

| Cấu hình | R@1 | R@5 | CI R@5 | R@10 | R@20 | MRR@10 | CI MRR | nDCG@10 | Liên kết@5 (n) | Liên kết@10 | Top-5 ngoài hiệu lực | Top-5 chỉ từ đồ thị | Chunk mở rộng/câu |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| B1 | 59.8 | 84.9 | 82.8–87.0 | 91.0 | 94.9 | 70.6 | 68.2–73.1 | 75.6 | 19.7 (185) | 29.2 | 0.0 | 0.0 | 0.0 |
| B2 | 57.4 | 81.7 | 79.3–84.1 | 87.5 | 92.7 | 67.8 | 65.4–70.3 | 72.6 | 22.2 (185) | 33.8 | 0.0 | 0.0 | 0.0 |
| B3 | 67.9 | 89.8 | 88.0–91.7 | 93.7 | 95.8 | 77.4 | 75.3–79.4 | 81.4 | 23.9 (185) | 39.3 | 0.0 | 0.0 | 0.0 |
| G | 67.7 | 89.4 | 87.5–91.3 | 93.6 | 96.0 | 77.2 | 75.1–79.3 | 81.2 | 25.7 (185) | 43.3 | 0.0 | 4.1 | 16.5 |
| A1 | 67.9 | 89.8 | 88.0–91.7 | 93.7 | 95.8 | 77.4 | 75.3–79.4 | 81.4 | 23.9 (185) | 39.3 | 0.0 | 0.0 | 0.0 |
| A2 | 61.5 | 88.0 | 86.1–89.9 | 92.4 | 95.2 | 73.0 | 70.8–75.1 | 77.8 | 22.2 (185) | 38.6 | 15.8 | 4.7 | 18.3 |

**R@5 theo tier** (n):

| Cấu hình | A | B | C | historical |
| --- | ---: | ---: | ---: | ---: |
| B1 | 86.4 (550) | 83.2 (339) | 87.7 (57) | 77.8 (54) |
| B2 | 83.3 (550) | 79.1 (339) | 84.2 (57) | 79.6 (54) |
| B3 | 91.1 (550) | 86.7 (339) | 93.0 (57) | 92.6 (54) |
| G | 90.5 (550) | 86.4 (339) | 93.0 (57) | 92.6 (54) |
| A1 | 91.1 (550) | 86.7 (339) | 93.0 (57) | 92.6 (54) |
| A2 | 88.7 (550) | 85.3 (339) | 93.0 (57) | 92.6 (54) |

**Liên kết theo loại** (top-5: độ phủ, số liên kết):

- B1: che_tai 4.1 (n=98); dan_chieu 11.3 (n=459)
- B2: che_tai 4.1 (n=98); dan_chieu 13.7 (n=459)
- B3: che_tai 10.2 (n=98); dan_chieu 14.8 (n=459)
- G: che_tai 17.3 (n=98); dan_chieu 15.5 (n=459)
- A1: che_tai 10.2 (n=98); dan_chieu 14.8 (n=459)
- A2: che_tai 8.2 (n=98); dan_chieu 13.5 (n=459)

**Analyzer + latency (ms, p50/p95):**

- B1: gọi LLM 0.0% · {'khong_goi': 508, 'disabled': 492} · analyze 0.38/0.51, final_check 0.44/0.51, hybrid 8.04/12.23, total 9.13/13.44
- B2: gọi LLM 0.0% · {'khong_goi': 508, 'disabled': 492} · analyze 0.38/0.51, encode 0.06/0.09, final_check 0.43/0.51, hybrid 4.39/5.36, total 5.48/6.59
- B3: gọi LLM 0.0% · {'khong_goi': 508, 'disabled': 492} · analyze 0.43/0.57, encode 0.08/0.1, final_check 0.5/0.57, hybrid 13.94/18.71, rerank 138.43/216.13, total 154.02/236.93
- G: gọi LLM 49.2% · {'khong_goi': 508, 'ok': 491, 'format_error': 1} · analyze 0.58/1.17, encode 0.08/0.1, expand 5.32/12.08, final_check 0.79/1.14, hybrid 13.56/18.34, rerank 122.34/336.51, total 142.88/363.59
- A1: gọi LLM 49.2% · {'khong_goi': 508, 'ok': 491, 'format_error': 1} · analyze 0.55/1.07, encode 0.07/0.08, final_check 0.45/0.51, hybrid 12.87/17.55, rerank 0.37/0.48, total 14.82/19.64
- A2: gọi LLM 49.2% · {'khong_goi': 508, 'ok': 491, 'format_error': 1} · analyze 0.58/1.15, encode 0.07/0.09, expand 4.64/10.71, hybrid 13.06/18.01, rerank 68.57/230.81, total 87.32/259.67

## Chạy

- Bảng mở rộng: `{"default": {"edge_types": ["DAN_CHIEU"], "hops": 1}, "by_type": {"muc_phat": {"edge_types": ["BI_XU_PHAT", "BI_TRU_DIEM", "DAN_CHIEU"], "hops": 1}, "tru_diem": {"edge_types": ["BI_XU_PHAT", "BI_TRU_DIEM", "DAN_CHIEU"], "hops": 1}, "bien_phap": {"edge_types": ["BI_XU_PHAT", "BI_TRU_DIEM", "DAN_CHIEU"], "hops": 1}, "da_buoc": {"edge_types": ["DAN_CHIEU", "BI_XU_PHAT", "BI_TRU_DIEM", "HUONG_DAN"], "hops": 2}}, "max_chunks": 30, "per_node_max": 5, "reverse_sanctions": true}`
- Rerank: `{"aiteamvn-reranker": {"n_pairs": 170314, "n_cached": 102521, "n_windows": 76579, "n_windows_scored": 75603, "n_truncated": 6, "n_tokens": 17982352, "seconds": 435.214, "n_calls": 4336, "pairs_per_s": 173.7}}`
- Analyzer (pha 1): `[{"phase": "analyze", "model_id": "qwen3-14b-awq", "serve": {"served_model": "qwen3-14b-awq", "hf_repo": "Qwen/Qwen3-14B-AWQ", "revision": "31c69efc29464b6bb0aee1398b5a7b50a99340c3", "quantization": "awq_marlin", "vllm_version": "0.33.0"}, "n_questions": 1489, "statuses": {"rule_chac": 748, "ok": 740, "format_error": 1}, "seconds": 134.5, "git_commit": "e134305cd1324fe54464d7a00dbc5fbaafb1bfe7-dirty", "finished_at": "2026-11-15T09:31:39+07:00"}]`
- GPU: `{"used": true, "name": "NVIDIA GeForce RTX 3090", "peak_vram_gb": 1.409, "torch": "2.15.0+cu132", "wall_hours": 0.2023, "vnd": 3440}` · tổng 728.4 s
