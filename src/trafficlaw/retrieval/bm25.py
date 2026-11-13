"""BM25 Okapi tự cài (M10), thuần Python, tất định.

**Tách từ** (:func:`tokenize`): NFC, chữ thường, âm tiết = chuỗi chữ/số liên tiếp (``[^\\W_]+``)
cộng bigram âm tiết liền kề (``"xe_ô"``, ``"ô_tô"``) khi ``bigrams=True``. Không tách từ tiếng Việt
bằng từ điển (không thêm dependency); bigram bắt được phần lớn từ ghép hai âm tiết.

**Điểm** (Robertson/Lucene, IDF không âm)::

    idf(t)     = ln(1 + (N − df + 0,5) / (df + 0,5))
    score(q,d) = Σ_{t ∈ q} qtf(t) · idf(t) · tf·(k1 + 1) / (tf + k1·(1 − b + b·|d|/avgdl))

``qtf`` = số lần ``t`` xuất hiện trong câu hỏi (tương đương cộng theo từng token của câu hỏi).
Đồng điểm → ``chunk_id`` tăng dần.

Lưu: JSON nén gzip, có ``format`` (đổi cách lưu ⇒ tăng :data:`FORMAT`).
"""

from __future__ import annotations

import gzip
import heapq
import json
import math
import re
import unicodedata
from collections import Counter
from collections.abc import Collection, Sequence
from pathlib import Path
from typing import Any

from trafficlaw.retrieval.catalog import Hit

FORMAT = "bm25-1"
_SYL = re.compile(r"[^\W_]+")


def tokenize(text: str, *, bigrams: bool = True) -> list[str]:
    syl = _SYL.findall(unicodedata.normalize("NFC", text).lower())
    if not bigrams:
        return syl
    return syl + [f"{a}_{b}" for a, b in zip(syl, syl[1:], strict=False)]


class BM25Index:
    def __init__(
        self,
        ids: Sequence[str],
        doc_len: Sequence[int],
        postings: dict[str, list[tuple[int, int]]],
        *,
        k1: float,
        b: float,
        bigrams: bool,
    ) -> None:
        self.ids = list(ids)
        self.doc_len = list(doc_len)
        self.postings = postings
        self.k1 = k1
        self.b = b
        self.bigrams = bigrams
        n = len(self.ids)
        self.avgdl = (sum(self.doc_len) / n) if n else 0.0
        self.idf = {
            t: math.log(1.0 + (n - len(p) + 0.5) / (len(p) + 0.5)) for t, p in postings.items()
        }

    # --- dựng / lưu ---
    @classmethod
    def build(
        cls,
        docs: Sequence[tuple[str, str]],
        *,
        k1: float = 1.5,
        b: float = 0.75,
        bigrams: bool = True,
    ) -> BM25Index:
        """``docs`` = [(chunk_id, text)] theo thứ tự danh mục."""
        postings: dict[str, list[tuple[int, int]]] = {}
        lens: list[int] = []
        for i, (_, text) in enumerate(docs):
            toks = tokenize(text, bigrams=bigrams)
            lens.append(len(toks))
            for t, tf in sorted(Counter(toks).items()):
                postings.setdefault(t, []).append((i, tf))
        return cls(
            [d for d, _ in docs], lens, dict(sorted(postings.items())), k1=k1, b=b, bigrams=bigrams
        )

    def params(self) -> dict[str, Any]:
        return {"k1": self.k1, "b": self.b, "bigrams": self.bigrams}

    def save(self, path: str | Path) -> None:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        obj = {
            "format": FORMAT,
            "params": self.params(),
            "ids": self.ids,
            "doc_len": self.doc_len,
            "postings": {t: [list(x) for x in v] for t, v in self.postings.items()},
        }
        tmp = p.with_suffix(p.suffix + ".tmp")
        # mtime=0 ⇒ byte gzip tất định (hash ổn định giữa các lần dựng).
        with tmp.open("wb") as raw, gzip.GzipFile(fileobj=raw, mode="wb", mtime=0) as gz:
            gz.write(json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode())
        tmp.replace(p)

    @classmethod
    def load(cls, path: str | Path) -> BM25Index:
        with gzip.open(path, "rb") as f:
            obj = json.loads(f.read().decode())
        if obj.get("format") != FORMAT:
            raise ValueError(f"BM25: định dạng {obj.get('format')!r} ≠ {FORMAT!r} — dựng lại")
        prm = obj["params"]
        return cls(
            obj["ids"],
            obj["doc_len"],
            {t: [(int(a), int(c)) for a, c in v] for t, v in obj["postings"].items()},
            k1=float(prm["k1"]),
            b=float(prm["b"]),
            bigrams=bool(prm["bigrams"]),
        )

    # --- truy vấn ---
    def scores(self, query: str) -> dict[int, float]:
        """Điểm mọi tài liệu có ít nhất một term của câu hỏi (chỉ số tài liệu → điểm)."""
        acc: dict[int, float] = {}
        k1, b, avg = self.k1, self.b, self.avgdl or 1.0
        for t, qtf in sorted(Counter(tokenize(query, bigrams=self.bigrams)).items()):
            post = self.postings.get(t)
            if not post:
                continue
            w = qtf * self.idf[t]
            for i, tf in post:
                norm = k1 * (1.0 - b + b * self.doc_len[i] / avg)
                acc[i] = acc.get(i, 0.0) + w * tf * (k1 + 1.0) / (tf + norm)
        return acc

    def search(
        self, query: str, top_k: int = 20, *, allowed: Collection[str] | None = None
    ) -> list[Hit]:
        """Top-k theo điểm giảm dần (đồng điểm → ``chunk_id``). ``allowed`` (vd. chunk hiệu lực
        tại ``as_of``) lọc **trước** khi xếp hạng. Tài liệu điểm 0 không được trả."""
        cand = (
            (-s, self.ids[i])
            for i, s in self.scores(query).items()
            if allowed is None or self.ids[i] in allowed
        )
        best = heapq.nsmallest(top_k, cand)
        return [Hit(cid, -neg, r, "bm25") for r, (neg, cid) in enumerate(best, 1)]


__all__ = ["FORMAT", "BM25Index", "tokenize"]
