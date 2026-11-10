"""M9: độ giống câu hỏi bằng TF-IDF n-gram ký tự (không cần GPU, không thêm dependency).

Dùng để: phát hiện câu gần trùng trong một split và chống rò rỉ train/val ↔ test (cosine > 0,9;
quyết định người dùng 10/11/2026 — kiểm lại bằng embedding ở M10/M14).

Đặc trưng: n-gram ký tự (mặc định 3) trên chuỗi đã chuẩn hoá (NFC, chữ thường, chỉ giữ chữ/số,
gộp khoảng trắng, đệm một dấu cách hai đầu); trọng số ``tf · idf`` với
``idf = ln((1 + N) / (1 + df)) + 1`` (IDF tính trên toàn bộ văn bản đưa vào), chuẩn hoá L2.

``near_pairs`` cho kết quả **chính xác** (không xấp xỉ): đặc trưng phổ biến (``df`` lớn) bị bỏ
khỏi bước dò ứng viên, phần đóng góp của chúng bị chặn trên bằng Cauchy–Schwarz
``‖q_F‖·‖c_F‖``; cặp nào cận trên còn ≥ ngưỡng thì mới tính cosine đầy đủ.
"""

from __future__ import annotations

import math
import re
import unicodedata
from collections import Counter
from collections.abc import Sequence
from dataclasses import dataclass

_NON_WORD = re.compile(r"[^\w]+")


def normalize(text: str) -> str:
    s = unicodedata.normalize("NFC", text).lower()
    return _NON_WORD.sub(" ", s).strip()


def ngrams(text: str, n: int = 3) -> Counter[str]:
    s = f" {normalize(text)} "
    if len(s) <= n:
        return Counter([s])
    return Counter(s[i : i + n] for i in range(len(s) - n + 1))


Vec = dict[str, float]


@dataclass
class TfidfSpace:
    idf: dict[str, float]
    n: int = 3

    @classmethod
    def fit(cls, texts: Sequence[str], n: int = 3) -> TfidfSpace:
        df: Counter[str] = Counter()
        for t in texts:
            df.update(set(ngrams(t, n)))
        total = len(texts)
        idf = {g: math.log((1 + total) / (1 + c)) + 1.0 for g, c in df.items()}
        return cls(idf=idf, n=n)

    def vector(self, text: str) -> Vec:
        tf = ngrams(text, self.n)
        default = math.log(1 + len(self.idf)) + 1.0
        v = {g: c * self.idf.get(g, default) for g, c in tf.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        return {g: x / norm for g, x in v.items()}


def cosine(a: Vec, b: Vec) -> float:
    if len(a) > len(b):
        a, b = b, a
    return sum(x * b.get(g, 0.0) for g, x in a.items())


def near_pairs(
    queries: Sequence[str],
    corpus: Sequence[str],
    *,
    threshold: float = 0.9,
    n: int = 3,
    same: bool = False,
    max_postings: int | None = None,
) -> list[tuple[int, int, float]]:
    """Mọi cặp ``(i_query, j_corpus, cosine)`` có cosine ≥ ``threshold``, sắp theo (i, j).

    ``same=True``: ``queries`` và ``corpus`` là một danh sách → chỉ trả cặp ``i < j``.
    IDF tính trên ``queries ∪ corpus`` (hoặc một lần khi ``same``).
    """
    if not queries or not corpus:
        return []
    space = TfidfSpace.fit(list(queries) if same else [*queries, *corpus], n=n)
    qv = [space.vector(t) for t in queries]
    cv = qv if same else [space.vector(t) for t in corpus]
    cap = max_postings if max_postings is not None else max(16, len(cv) // 20)

    df: Counter[str] = Counter()
    for v in cv:
        df.update(v.keys())
    frequent = {g for g, c in df.items() if c > cap}
    postings: dict[str, list[tuple[int, float]]] = {}
    for j, v in enumerate(cv):
        for g, x in v.items():
            if g not in frequent:
                postings.setdefault(g, []).append((j, x))
    c_freq_norm = [math.sqrt(sum(x * x for g, x in v.items() if g in frequent)) for v in cv]

    out: list[tuple[int, int, float]] = []
    for i, q in enumerate(qv):
        partial: dict[int, float] = {}
        q_freq = 0.0
        for g, x in q.items():
            if g in frequent:
                q_freq += x * x
                continue
            for j, y in postings.get(g, ()):
                partial[j] = partial.get(j, 0.0) + x * y
        q_freq = math.sqrt(q_freq)
        # Ứng viên: có chung đặc trưng hiếm, hoặc chỉ chung đặc trưng phổ biến nhưng cận trên đủ.
        if q_freq > 0:
            for j, cf in enumerate(c_freq_norm):
                if j not in partial and q_freq * cf >= threshold:
                    partial[j] = 0.0
        for j, p in partial.items():
            if same and j <= i:
                continue
            if p + q_freq * c_freq_norm[j] < threshold - 1e-12:
                continue
            s = cosine(q, cv[j])
            if s >= threshold:
                out.append((i, j, round(s, 6)))
    return sorted(out)


def max_similarity(
    queries: Sequence[str], corpus: Sequence[str], *, threshold: float = 0.9, n: int = 3
) -> dict[int, tuple[int, float]]:
    """Với mỗi query có cặp ≥ ngưỡng: (chỉ số corpus giống nhất, cosine)."""
    best: dict[int, tuple[int, float]] = {}
    for i, j, s in near_pairs(queries, corpus, threshold=threshold, n=n):
        if i not in best or s > best[i][1]:
            best[i] = (j, s)
    return best


__all__ = ["TfidfSpace", "cosine", "max_similarity", "near_pairs", "ngrams", "normalize"]
