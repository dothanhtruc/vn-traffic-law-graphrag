"""Rerank (M11): cross-encoder chấm cặp (câu hỏi, chunk), cache điểm append-only.

- **Cửa sổ**: chunk mà cặp (câu hỏi + chunk, gồm token đặc biệt) vượt ``max_length`` (512) được
  tách bằng :func:`trafficlaw.retrieval.dense.split_windows` của M10 (theo dòng, lặp lại tiêu đề
  Điều + câu dẫn Khoản); **điểm chunk = max cửa sổ**. Token đếm bằng ``count_tokenizer`` cố định
  (``tokenizers``) ⇒ local (``--dry-run``) và máy thuê tách giống hệt nhau. Với XLM-R, cặp
  ``<s> q </s></s> p </s>`` có đúng ``count(q) + count(p)`` token (mỗi lần đếm gồm 2 token đặc
  biệt).
- **Cache** (``data/index/rerank/<key>/scores.jsonl``): mỗi dòng một cặp (câu hỏi, chunk), khoá
  ``sha256([key, hf_repo, revision, max_length, sha256(NFC câu hỏi), sha256(NFC text chunk)])``,
  kèm điểm từng cửa sổ (khoá cửa sổ = như trên với ``sha256(text cửa sổ)``). Đọc lại theo khoá
  cặp ⇒ chạy lại ở local không cần tokenizer hay GPU; cửa sổ đã chấm được dùng lại khi chunk khác
  có cùng cửa sổ. Dòng cuối ghi dở bị bỏ (``utils.jsonl``).
- Điểm = logit thô của model (không sigmoid — đơn điệu, không đổi thứ hạng).

Module này **không import torch**; :class:`STReranker` import lười (torch, transformers) trong
``__init__``.
"""

from __future__ import annotations

import hashlib
import json
import logging
import math
import time
import unicodedata
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

from trafficlaw.retrieval.bm25 import tokenize
from trafficlaw.retrieval.config import RerankerSpec
from trafficlaw.retrieval.dense import Window, split_windows
from trafficlaw.utils.jsonl import JsonlWriter, read_jsonl

logger = logging.getLogger(__name__)


class Reranker(Protocol):
    def count_tokens(self, text: str) -> int:
        """Token của một đoạn (gồm token đặc biệt), không cắt."""
        ...

    def score(self, pairs: Sequence[tuple[str, str]], *, batch_size: int = 32) -> list[float]: ...


class FakeReranker:
    """Reranker giả tất định cho test: điểm = số âm tiết chung (câu hỏi, đoạn) / √(độ dài đoạn);
    token = số âm tiết + 2."""

    def __init__(self) -> None:
        self.calls = 0
        self.n_pairs = 0

    def count_tokens(self, text: str) -> int:
        return len(tokenize(text, bigrams=False)) + 2

    def score(self, pairs: Sequence[tuple[str, str]], *, batch_size: int = 32) -> list[float]:
        self.calls += 1
        self.n_pairs += len(pairs)
        out = []
        for q, p in pairs:
            qs, ps = set(tokenize(q, bigrams=False)), tokenize(p, bigrams=False)
            out.append(round(sum(1 for t in set(ps) if t in qs) / math.sqrt(len(ps) + 1), 6))
        return out


class TokenizerCounter:
    """Đếm token bằng ``tokenizer.json`` (thư viện ``tokenizers``, không cần torch)."""

    def __init__(self, hf_repo: str, revision: str | None) -> None:
        from tokenizers import Tokenizer

        self.tok = Tokenizer.from_pretrained(hf_repo, revision=revision or "main")
        self.tok.no_truncation()

    def count_tokens(self, text: str) -> int:
        return len(self.tok.encode(text).ids)


def make_counter(spec: RerankerSpec) -> TokenizerCounter:
    t = spec.count_tokenizer
    return (
        TokenizerCounter(t.hf_repo, t.revision)
        if t
        else TokenizerCounter(spec.hf_repo, spec.revision)
    )


class STReranker:
    """Cross-encoder bằng ``transformers`` (như README của AITeamVN/Vietnamese_Reranker):
    ``AutoModelForSequenceClassification`` ghim revision, điểm = logit thô, bf16 (lùi fp16 khi GPU
    không hỗ trợ), cắt ``max_length``. CUDA OOM → giảm batch một nửa.

    Tokenizer = ``count_tokenizer`` (``tokenizer.json`` nhanh): repo reranker chỉ có
    ``sentencepiece.bpe.model`` (cần gói ``sentencepiece`` — không cài), và file đó trùng sha256
    với model gốc ``BAAI/bge-reranker-v2-m3`` (kiểm 15/11/2026), cùng ``special_tokens_map.json``
    ⇒ tokenizer nhanh của model gốc tương đương. Model và bộ tách cửa sổ dùng cùng tokenizer."""

    def __init__(self, spec: RerankerSpec, *, device: str | None = None) -> None:
        import torch
        from transformers import AutoModelForSequenceClassification, AutoTokenizer

        self.torch = torch
        self.spec = spec
        dev = device or ("cuda" if torch.cuda.is_available() else "cpu")
        dtype: Any = torch.float32
        if dev == "cuda" and spec.dtype == "bf16":
            dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
        self.dtype_name = str(dtype).removeprefix("torch.")
        t = spec.count_tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            t.hf_repo if t else spec.hf_repo, revision=(t.revision if t else spec.revision)
        )
        self.model = AutoModelForSequenceClassification.from_pretrained(
            spec.hf_repo, revision=spec.revision, torch_dtype=dtype
        ).to(dev)
        self.model.eval()
        self.device = dev
        self.counter = make_counter(spec)

    def count_tokens(self, text: str) -> int:
        return self.counter.count_tokens(text)

    def model_count_tokens(self, text: str) -> int:
        return len(self.tokenizer(text, add_special_tokens=True, truncation=False)["input_ids"])

    def _batch(self, pairs: Sequence[tuple[str, str]]) -> list[float]:
        enc = self.tokenizer(
            [p[0] for p in pairs],
            [p[1] for p in pairs],
            padding=True,
            truncation=True,
            max_length=self.spec.max_length,
            return_tensors="pt",
        ).to(self.device)
        with self.torch.inference_mode():
            logits = self.model(**enc, return_dict=True).logits.view(-1).float()
        return [float(x) for x in logits.cpu().tolist()]

    def score(self, pairs: Sequence[tuple[str, str]], *, batch_size: int = 32) -> list[float]:
        # Xếp theo độ dài để giảm padding; trả theo thứ tự đầu vào.
        order = sorted(range(len(pairs)), key=lambda i: len(pairs[i][0]) + len(pairs[i][1]))
        out: list[float] = [0.0] * len(pairs)
        bs = batch_size
        i = 0
        while i < len(order):
            idx = order[i : i + bs]
            try:
                vals = self._batch([pairs[j] for j in idx])
            except self.torch.cuda.OutOfMemoryError:
                if bs <= 1:
                    raise
                self.torch.cuda.empty_cache()
                bs = max(1, bs // 2)
                logger.warning("CUDA OOM (rerank) → giảm batch còn %d", bs)
                continue
            for j, v in zip(idx, vals, strict=True):
                out[j] = v
            i += len(idx)
        return out

    def peak_vram_gb(self) -> float | None:
        if self.device != "cuda":
            return None
        return round(self.torch.cuda.max_memory_allocated() / 2**30, 3)


# --- cửa sổ + cache --------------------------------------------------------------------------


def _h(text: str) -> str:
    return hashlib.sha256(unicodedata.normalize("NFC", text).encode()).hexdigest()


def pair_windows(
    chunk_id: str, question: str, text: str, count: Any, max_length: int
) -> list[Window]:
    """Cửa sổ của chunk cho một câu hỏi: ``n_tokens`` = token của cặp."""
    nq = count(question)
    return split_windows(chunk_id, text, lambda t: nq + count(t), max_length)


@dataclass
class RerankStats:
    n_pairs: int = 0
    n_cached: int = 0
    n_windows: int = 0
    n_windows_scored: int = 0
    n_truncated: int = 0
    n_tokens: int = 0
    seconds: float = 0.0
    n_calls: int = 0

    def add(self, o: RerankStats) -> None:
        for f in self.__dataclass_fields__:
            setattr(self, f, getattr(self, f) + getattr(o, f))

    def to_dict(self) -> dict[str, Any]:
        d = {f: getattr(self, f) for f in self.__dataclass_fields__}
        d["seconds"] = round(self.seconds, 3)
        d["pairs_per_s"] = round(self.n_windows_scored / self.seconds, 1) if self.seconds else None
        return d


class MissingRerankScoresError(RuntimeError):
    """Cặp chưa có điểm trong cache và không có model (chạy trên máy thuê với ``--gpu``)."""


@dataclass
class RerankCache:
    root: Path
    _pairs: dict[str, dict[str, Any]] = field(default_factory=dict)
    _windows: dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.root = Path(self.root)
        for r in read_jsonl(self.path):
            self._index(r)

    @property
    def path(self) -> Path:
        return self.root / "scores.jsonl"

    def _index(self, r: dict[str, Any]) -> None:
        self._pairs[str(r["pair"])] = r
        for w in r.get("windows", []):
            self._windows[str(w["key"])] = float(w["score"])

    def __len__(self) -> int:
        return len(self._pairs)

    def get(self, pair_key: str) -> dict[str, Any] | None:
        return self._pairs.get(pair_key)

    def window(self, key: str) -> float | None:
        return self._windows.get(key)

    def put_many(self, rows: Sequence[dict[str, Any]]) -> None:
        if not rows:
            return
        with JsonlWriter(self.path) as w:
            for r in rows:
                w.write(r)
                self._index(r)


def _key(model_key: str, spec: RerankerSpec, q_sha: str, text_sha: str) -> str:
    raw = [model_key, spec.hf_repo, spec.revision, spec.max_length, q_sha, text_sha]
    return hashlib.sha256(json.dumps(raw).encode()).hexdigest()


def pair_key(model_key: str, spec: RerankerSpec, question: str, chunk_text: str) -> str:
    return _key(model_key, spec, _h(question), _h(chunk_text))


def rerank_scores(
    reranker: Reranker | None,
    cache: RerankCache,
    model_key: str,
    spec: RerankerSpec,
    question: str,
    chunks: Sequence[tuple[str, str]],
) -> tuple[dict[str, float], RerankStats]:
    """Điểm của từng chunk ``[(chunk_id, text)]`` cho ``question``; chỉ chấm cửa sổ chưa có."""
    st = RerankStats(n_pairs=len(chunks))
    scores: dict[str, float] = {}
    todo: list[tuple[str, str, str]] = []
    for cid, text in chunks:
        pk = pair_key(model_key, spec, question, text)
        row = cache.get(pk)
        if row is not None:
            scores[cid] = float(row["score"])
            st.n_cached += 1
        else:
            todo.append((cid, text, pk))
    if not todo:
        return scores, st
    if reranker is None:
        raise MissingRerankScoresError(
            f"{model_key}: {len(todo)} cặp chưa có điểm — chạy trên máy thuê với --gpu"
        )
    q_sha = _h(question)
    plan: list[tuple[str, str, list[tuple[Window, str]]]] = []
    need: dict[str, str] = {}
    for cid, text, pk in todo:
        ws = pair_windows(cid, question, text, reranker.count_tokens, spec.max_length)
        items = [(w, _key(model_key, spec, q_sha, _h(w.text))) for w in ws]
        plan.append((cid, pk, items))
        st.n_windows += len(ws)
        st.n_truncated += sum(1 for w in ws if w.truncated)
        for w, wk in items:
            if cache.window(wk) is None and wk not in need:
                need[wk] = w.text
                st.n_tokens += min(w.n_tokens, spec.max_length)
    got: dict[str, float] = {}
    if need:
        keys = list(need)
        t0 = time.perf_counter()
        vals = reranker.score([(question, need[k]) for k in keys], batch_size=spec.batch_size)
        st.seconds += time.perf_counter() - t0
        st.n_calls += 1
        st.n_windows_scored += len(keys)
        got = dict(zip(keys, vals, strict=True))
    rows = []
    for cid, pk, items in plan:
        wrows = []
        for w, wk in items:
            s = got[wk] if wk in got else cache.window(wk)
            assert s is not None
            wrows.append(
                {"key": wk, "k": w.k, "n_tokens": w.n_tokens, "truncated": w.truncated, "score": s}
            )
        best = max(r["score"] for r in wrows)
        scores[cid] = best
        rows.append({"pair": pk, "chunk_id": cid, "score": best, "windows": wrows})
    cache.put_many(rows)
    return scores, st


__all__ = [
    "FakeReranker",
    "MissingRerankScoresError",
    "RerankCache",
    "RerankStats",
    "Reranker",
    "STReranker",
    "TokenizerCounter",
    "make_counter",
    "pair_key",
    "pair_windows",
    "rerank_scores",
]
