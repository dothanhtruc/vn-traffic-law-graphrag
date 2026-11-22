# M14 — Fine-tune embedding + reranker

Phiên GPU 11 (22/11/2026, aidev gói Pro RTX 3090, cổng 20121). Mọi con số sinh từ `logs/train/*.jsonl`,
`data/train/*`, `data/index/retrieval_eval_m14.*`, `results/m14-dev/`, `results/m14-test/` (GitHub Release
`m14-finetune-v1`). **Test chỉ đo một lần**, sau khi người dùng duyệt checkpoint (chọn bằng val + dev).

## 1. Dữ liệu

- Câu train M9 (`train.jsonl`, 8.566 câu, `mistral-small-3.2` sinh từ một chunk/câu) → **7.049 câu** sau khi loại
  câu có positive là gold / tổ tiên / con cháu gold của **test** (1.233) hoặc **dev** M13b (292) — người dùng chọn
  18/11/2026. Chunk bị loại vẫn có thể làm negative. Positive = text chunk như lúc lập chỉ mục; chunk > 512 token
  (144/3.853) → cửa sổ của model gốc có nhiều âm tiết chung với câu hỏi nhất.
- **Hard negative** (`scripts.mine_negatives`, `configs/hard_negatives.yaml`, 18 phút GPU): ứng viên = dense gốc
  top-30 + BM25 top-30 + 5 Khoản cùng Điều (lọc hiệu lực tại as_of), trộn vòng tròn, ≤ 20/câu; bỏ chunk ngoài hiệu
  lực / cùng unit / liên quan gold / cùng text; chấm bằng **reranker gốc**, bỏ negative có điểm ≥ điểm positive − 1,0
  (12.498 ứng viên), giữ 7 khó nhất. Kết quả: 48.769 negative (TB 6,9/câu; 22 câu không còn negative); nguồn của
  negative được giữ: dense 41.870 · BM25 37.703 · anh em 11.241 (một chunk có thể đến từ nhiều nguồn).

## 2. Huấn luyện (`src/trafficlaw/train/`, vòng lặp tự viết)

| | Embedding | Reranker |
| --- | --- | --- |
| Gốc | `AITeamVN/Vietnamese_Embedding@dea33aa` | `AITeamVN/Vietnamese_Reranker@f536976` (tokenizer bge-reranker-v2-m3) |
| Loss | MNRL có GradCache (`CachedMultipleNegativesRankingLoss`), scale 20, in-batch + 1 hard negative, batch không trùng chunk/unit | listwise softmax CE trên nhóm 1 positive + 7 negative |
| Batch | 128 (mini-batch 16, không gradient checkpointing) | 16 nhóm × tích luỹ 2 = 32 nhóm/bước (2 nhóm/lượt forward) |
| Lưới (khai báo trước) | lr 1e-5, 2e-5 × 3 epoch (57 bước/epoch), warmup 10% | lr 1e-5, 2e-5 × 2 epoch (220 bước/epoch) |
| VRAM đỉnh | 17,3 GB | 17,4 GB |
| Thời gian/run | 25–27 phút | 50 phút |

- bf16 autocast, trọng số fp32, AdamW (wd 0,01), clip 1,0, seed 42. Checkpoint (model + optimizer + scheduler +
  RNG + bước) mỗi 30/50 bước + cuối epoch, đẩy HF Hub private `<run>-ckpt/last` (luồng nền); resume từ checkpoint cục
  bộ hoặc HF Hub — có test CPU: ngắt giữa chừng rồi chạy tiếp cho trọng số **y hệt** chạy liền (kể cả resume từ HF Hub giả).
- Dry-run: embedder mini-batch 32 không checkpointing → OOM (23,0 GB) ⇒ mini 16 (17,3 GB, 8 s/bước; gradient
  checkpointing 11 GB nhưng 12 s/bước). GradCache cho cùng gradient với mọi mini-batch.
- Không dùng `SentenceTransformerTrainer` (cần `datasets` + `accelerate`; API sentence-transformers 6.3 đổi nhiều) ⇒
  không thêm dependency.

## 3. Chọn checkpoint (val, quy tắc khai báo trước: R@5 → MRR@10 → bước sớm hơn → mục lưới trước)

**Embedding — val dense-only** (489 câu, lọc as_of, cấp unit; CI 95% bootstrap):

| Run | Bước | R@1 | R@5 (CI) | MRR@10 (CI) |
| --- | ---: | ---: | --- | --- |
| gốc | — | 60,9 | 86,5 (83,2–89,6) | 71,4 (68,0–74,9) |
| lr1e5 | 57 / 113 / 169 | 68,1 / 68,3 / 68,7 | 93,3 / 93,3 / 93,3 | 79,0 / 79,4 / 79,4 |
| **lr2e5 ★** | **57** / 113 / 169 | **68,9** / 67,3 / 67,1 | **93,9 (91,6–95,9)** / 93,5 / 93,3 | **79,7 (77,1–82,6)** / 78,7 / 78,4 |

**Reranker — val rerank-only trên pool G cố định của M11:**

| Run | Bước | R@1 | R@5 (CI) | MRR@10 (CI) |
| --- | ---: | ---: | --- | --- |
| gốc | — | 74,4 | 92,8 (90,6–95,1) | 82,1 (79,3–84,9) |
| lr1e5 | 220 / 440 | 81,6 / 81,0 | 94,5 / 94,5 | 87,0 / 86,7 |
| **lr2e5 ★** | **220** / 440 | **79,8** / 80,8 | **94,9 (93,0–96,7)** / 94,5 | **86,2 (83,7–88,7)** / 86,8 |

Chọn: `dothanhtruc/trafficlaw-emb-lr2e5@1ebdce9` (khoá `aiteamvn-vi-emb-ft`), `dothanhtruc/trafficlaw-rerank-lr2e5@65bbe71`
(khoá `aiteamvn-reranker-ft`). Bảng đầy đủ: `data/train/{embedding,reranker}_selection.md`.

## 4. Xác nhận end-to-end (không dùng test)

**Val — truy hồi** (`scripts.retrieve --eval val --out-name retrieval_eval_m14`): G 96,1 R@5 / 86,5 MRR@10;
A1 96,3 / 86,5; A2 94,5 / 79,0; **A3 (gốc) 92,8 / 82,1**; B3 93,0 / 82,2 — A3, B3 trùng đúng số M11.

**Dev M13b** (115 câu = 75 dev + 40 dev_oos; run `m14-dev`): A3 trùng 115/115 câu trả lời của `m13c-dev` (cache).

| Chỉ số | G | A3 | p (McNemar/Wilcoxon) |
| --- | ---: | ---: | ---: |
| Judge: đúng hoàn toàn | 67,0 | 60,9 | 0,167 |
| Đủ con số yêu cầu | 79,3 | 65,5 | 0,125 |
| Citation R | 70,4 | 61,9 | 0,041 |
| Recall@5 | 87,8 | 79,9 | 0,004 |
| Đa bước: ngữ cảnh phủ đủ gold | 56,2 | 37,5 | — |

Người dùng duyệt checkpoint 22/11/2026 → đo test.

## 5. Test cuối (run `m14-test`, 500 câu; G/A1/A2 fine-tune, A3 gốc; B0–B3 chép từ `m13-test-v2`)

| Chỉ số | G (ft) | A3 (gốc) | B3 (gốc) | A1 (ft) | A2 (ft) |
| --- | ---: | ---: | ---: | ---: | ---: |
| Recall@5 | **84,3** | 80,8 | 81,7 | 84,6 | 82,8 |
| MRR@10 | **79,6** | 74,5 | 75,7 | 80,3 | 75,5 |
| Recall@1 | 59,8 | 55,8 | 56,9 | 60,1 | 55,2 |
| Judge: đúng hoàn toàn (judge_200) | 46,8 | 47,8 | 49,3 | — | 47,8 |
| Đủ con số yêu cầu | 58,7 | 64,2 | 66,1 | 64,9 | 59,2 |
| Có trích dẫn tới gold | 74,9 | 76,2 | 76,9 | 83,2 | 73,4 |
| Đúng phiên bản (theo thời điểm) | 84,0 | 93,8 | 86,0 | 90,9 | 71,9 |
| Từ chối nhầm câu có gold | 4,0 | 5,6 | 4,9 | 3,4 | 6,3 |

(A1, A2, A3 tính trên tập con của ma trận M13 — so sánh ghép cặp ở bảng dưới dùng đúng câu chung.)

G so với A3 (ghép cặp, Holm trong từng chỉ số): **Recall@5 +3,6 (CI 1,4…5,8; p Holm 0,004)**, **MRR@10 +5,1
(3,2…7,1; p < 0,001)**; judge đúng hoàn toàn −1,0 (−7,5…6,0; p 1,0), đủ con số −5,8 (p 1,0), trích dẫn tới gold −0,7,
đúng phiên bản −6,2 (n 32; p 1,0) — **không khác biệt có ý nghĩa ở chỉ số câu trả lời**. G so với B3: R@5 +2,6
(p Holm 0,022), MRR@10 +4,0 (p < 0,001); đủ con số −7,4 (p thô 0,049, Holm 0,29). Regression G (regression_100):
77,23% → **81,27%** (`data/qa/retrieval_baseline_test.json` ghi lại).

**Kết luận**: fine-tune cải thiện truy hồi rõ trên val, dev và test; trên test lợi ích đó **không chuyển thành câu trả
lời tốt hơn** (judge, con số ngang A3/B3 trong sai số). Trên dev, câu trả lời có xu hướng tốt hơn nhưng không có ý nghĩa.

## 6. Hạn chế phải nêu

- Val sinh cùng cách với train (Mistral, một chunk/câu, Điều khác nhau) ⇒ lợi ích trên val lạc quan; chọn checkpoint
  trên 3 (embedding) / 2 (reranker) điểm đánh giá × 2 lr ⇒ có thiên lệch chọn lọc nhỏ.
- Câu train có positive trùng gold test/dev đã loại, nhưng train vẫn phủ cùng văn bản/Điều với test.
- Test đã bị nhìn ở M13; M14 không dùng test để chọn gì, và test chỉ đo một lần (run này).
- Dao động theo seed và kiểm định judge không đo lại (dùng số M13: 91,2% câu trả lời giống hệt giữa 3 seed; κ 0,40).
- HF Hub: lịch sử checkpoint trung gian làm đầy 100 GB private ⇒ người dùng đồng ý squash lịch sử `*-ckpt` và xoá blob
  mồ côi (74,9 GB); repo model (bản chọn) không bị đụng. Model private ⇒ người khác tái lập cần quyền truy cập.

## 7. Chi phí

Máy bật ~09:40–14:15 (~4,6 giờ ≈ 78.000 VND ở 17.000 VND/giờ, gồm setup, chờ token HF, tải model). Tính toán chính:
khai thác 0,30 giờ; embedder 0,42 + 0,45 giờ; reranker 0,83 + 0,83 giờ; encode corpus < 1 phút; truy hồi val/dev/test,
sinh + judge dev và test ~1,2 giờ.
