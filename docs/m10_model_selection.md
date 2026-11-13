# Chọn model embedding gốc (M10)

Sinh lúc 2026-11-14T00:52:43+07:00 · commit `1a31aed1c8e662a4e65b62d2e8f276e115cfaaee` · 3853 chunk (`catalog sha256 eaff1f5ec42a`) · data_version `f3297e64b9e4`

Tập đo: val (chia theo Điều, câu do mistral-small-3.2 sinh từ chính chunk ⇒ thiên lệch từ vựng, có lợi cho BM25/model bám nguyên văn) và tập con train phân tầng theo tier (seed 42). **Không dùng test.** Chunk đúng = chunk hiệu lực tại as_of chứa gold unit; R@k cấp unit. CI 95% bootstrap 1.000 lần theo câu.
BM25 k1=1.5, b=0.75, bigram=True; RRF k=60, độ sâu 100; top_k 20. Chunk dài: cửa sổ ≤ 512 token, điểm = max.

## val (489 câu, lọc as_of trước khi xếp hạng)

| Hệ thống | R@1 | R@5 | CI 95% R@5 | R@10 | R@20 | MRR@10 | nDCG@10 | R@5 không lọc |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| BM25 (B1) | 60.7 | 86.9 | 84.0–89.8 | 92.6 | 95.7 | 71.8 | 76.9 | 84.0 |
| dense aiteamvn-vi-emb | 60.9 | 86.5 | 83.2–89.6 | 92.0 | 95.3 | 71.4 | 76.4 | 82.6 |
| RRF(BM25 + aiteamvn-vi-emb) | 66.7 | 91.8 | 89.4–94.3 | 95.5 | 97.1 | 77.4 | 81.9 | 89.4 |
| dense bge-m3 | 58.7 | 84.0 | 80.6–87.3 | 90.2 | 93.5 | 69.9 | 74.8 | 80.4 |
| RRF(BM25 + bge-m3) | 65.2 | 88.5 | 85.7–91.2 | 93.0 | 96.1 | 75.6 | 79.9 | 86.5 |
| dense qwen3-emb-0.6b | 58.1 | 82.0 | 78.3–85.5 | 87.9 | 93.7 | 68.4 | 73.2 | 79.3 |
| RRF(BM25 + qwen3-emb-0.6b) | 63.0 | 87.7 | 84.7–90.6 | 93.9 | 96.5 | 74.0 | 78.8 | 85.3 |
| dense me5-large-instruct | 56.0 | 81.0 | 77.3–84.7 | 87.9 | 92.4 | 66.7 | 71.8 | 77.1 |
| RRF(BM25 + me5-large-instruct) | 63.0 | 87.5 | 84.5–90.6 | 93.0 | 96.7 | 74.0 | 78.6 | 85.5 |
| dense qwen3-emb-4b | 64.2 | 88.3 | 85.5–91.2 | 93.9 | 96.9 | 75.0 | 79.6 | 85.9 |
| RRF(BM25 + qwen3-emb-4b) | 67.1 | 91.4 | 88.8–93.9 | 95.1 | 98.0 | 77.6 | 81.9 | 88.8 |

**R@5 theo tier** (số câu trong ngoặc):

| Hệ thống | A (n) | B (n) | C (n) | historical (n) |
| --- | ---: | ---: | ---: | ---: |
| BM25 (B1) | 87.4 (214) | 82.9 (199) | 100.0 (42) | 91.2 (34) |
| dense aiteamvn-vi-emb | 88.8 (214) | 84.9 (199) | 81.0 (42) | 88.2 (34) |
| RRF(BM25 + aiteamvn-vi-emb) | 94.9 (214) | 88.4 (199) | 92.9 (42) | 91.2 (34) |
| dense bge-m3 | 87.4 (214) | 80.9 (199) | 76.2 (42) | 91.2 (34) |
| RRF(BM25 + bge-m3) | 90.7 (214) | 84.9 (199) | 90.5 (42) | 94.1 (34) |
| dense qwen3-emb-0.6b | 84.6 (214) | 77.9 (199) | 83.3 (42) | 88.2 (34) |
| RRF(BM25 + qwen3-emb-0.6b) | 89.7 (214) | 83.4 (199) | 97.6 (42) | 88.2 (34) |
| dense me5-large-instruct | 85.5 (214) | 73.9 (199) | 83.3 (42) | 91.2 (34) |
| RRF(BM25 + me5-large-instruct) | 91.1 (214) | 82.4 (199) | 90.5 (42) | 91.2 (34) |
| dense qwen3-emb-4b | 91.1 (214) | 85.4 (199) | 90.5 (42) | 85.3 (34) |
| RRF(BM25 + qwen3-emb-4b) | 93.9 (214) | 87.9 (199) | 97.6 (42) | 88.2 (34) |

## train_1000 (1000 câu, lọc as_of trước khi xếp hạng)

| Hệ thống | R@1 | R@5 | CI 95% R@5 | R@10 | R@20 | MRR@10 | nDCG@10 | R@5 không lọc |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| BM25 (B1) | 59.8 | 84.9 | 82.8–87.0 | 91.0 | 94.9 | 70.6 | 75.6 | 81.9 |
| dense aiteamvn-vi-emb | 57.4 | 81.7 | 79.3–84.1 | 87.5 | 92.7 | 67.8 | 72.6 | 79.0 |
| RRF(BM25 + aiteamvn-vi-emb) | 65.0 | 86.4 | 84.2–88.5 | 92.4 | 95.8 | 74.6 | 78.9 | 84.9 |
| dense bge-m3 | 53.3 | 80.3 | 77.9–82.7 | 86.8 | 91.3 | 64.8 | 70.2 | 76.5 |
| RRF(BM25 + bge-m3) | 62.6 | 85.5 | 83.4–87.8 | 91.0 | 95.0 | 72.6 | 77.1 | 83.3 |
| dense qwen3-emb-0.6b | 53.7 | 80.2 | 77.7–83.1 | 87.2 | 92.3 | 65.1 | 70.5 | 77.5 |
| RRF(BM25 + qwen3-emb-0.6b) | 62.3 | 86.7 | 84.7–88.7 | 92.3 | 96.0 | 72.7 | 77.5 | 85.0 |
| dense me5-large-instruct | 49.0 | 77.7 | 75.1–80.2 | 84.7 | 89.6 | 60.9 | 66.7 | 74.5 |
| RRF(BM25 + me5-large-instruct) | 60.3 | 85.2 | 83.1–87.3 | 91.5 | 95.2 | 71.4 | 76.3 | 83.4 |
| dense qwen3-emb-4b | 60.3 | 85.9 | 83.9–88.0 | 91.6 | 95.2 | 71.4 | 76.3 | 83.5 |
| RRF(BM25 + qwen3-emb-4b) | 65.5 | 89.1 | 87.3–91.0 | 93.8 | 97.0 | 75.3 | 79.8 | 87.0 |

**R@5 theo tier** (số câu trong ngoặc):

| Hệ thống | A (n) | B (n) | C (n) | historical (n) |
| --- | ---: | ---: | ---: | ---: |
| BM25 (B1) | 86.4 (550) | 83.2 (339) | 87.7 (57) | 77.8 (54) |
| dense aiteamvn-vi-emb | 83.3 (550) | 79.1 (339) | 84.2 (57) | 79.6 (54) |
| RRF(BM25 + aiteamvn-vi-emb) | 87.6 (550) | 83.5 (339) | 87.7 (57) | 90.7 (54) |
| dense bge-m3 | 82.4 (550) | 77.0 (339) | 82.5 (57) | 77.8 (54) |
| RRF(BM25 + bge-m3) | 86.7 (550) | 82.3 (339) | 93.0 (57) | 85.2 (54) |
| dense qwen3-emb-0.6b | 83.1 (550) | 74.6 (339) | 82.5 (57) | 83.3 (54) |
| RRF(BM25 + qwen3-emb-0.6b) | 87.8 (550) | 83.8 (339) | 89.5 (57) | 90.7 (54) |
| dense me5-large-instruct | 79.8 (550) | 74.6 (339) | 78.9 (57) | 74.1 (54) |
| RRF(BM25 + me5-large-instruct) | 86.5 (550) | 82.6 (339) | 89.5 (57) | 83.3 (54) |
| dense qwen3-emb-4b | 87.8 (550) | 82.9 (339) | 87.7 (57) | 83.3 (54) |
| RRF(BM25 + qwen3-emb-4b) | 90.2 (550) | 88.2 (339) | 87.7 (57) | 85.2 (54) |

## Model

| Khoá | HF repo @ revision | Tham số (B) | dim | License | Token/s | VRAM đỉnh (GB) | Chunk tách cửa sổ | Cửa sổ còn bị cắt |
| --- | --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| aiteamvn-vi-emb | `AITeamVN/Vietnamese_Embedding@dea33aa` | 0.57 | 1024 | apache-2.0 | 62533.7 | 1.441 | 144 | 0 |
| bge-m3 | `BAAI/bge-m3@5617a9f` | 0.57 | 1024 | mit | 65509.4 | 1.441 | 144 | 0 |
| qwen3-emb-0.6b | `Qwen/Qwen3-Embedding-0.6B@97b0c61` | 0.6 | 1024 | apache-2.0 | 28684.4 | 2.629 | 214 | 2 |
| me5-large-instruct | `intfloat/multilingual-e5-large-instruct@274baa4` | 0.56 | 1024 | mit | 64725.8 | 2.167 | 144 | 0 |
| qwen3-emb-4b | `Qwen/Qwen3-Embedding-4B@5cf2132` | 4.0 | 2560 | apache-2.0 | 6024.6 | 8.184 | 214 | 2 |
