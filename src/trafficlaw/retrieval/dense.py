"""Truy hồi vector (M10): protocol ``Embedder``, cắt cửa sổ, cache vector, ``FaissIndex``.

- Vector luôn chuẩn hoá L2, ``float32``; FAISS ``IndexFlatIP`` (tìm chính xác, cosine).
- **Chunk dài** (người dùng chốt 13/11/2026): chunk vượt ``max_seq_length`` token (tính cả prompt
  và token đặc biệt) được tách theo **ranh giới dòng** thành các cửa sổ, mỗi cửa sổ lặp lại phần
  đầu (tiêu đề Điều + câu dẫn Khoản). Mỗi cửa sổ là một dòng FAISS trỏ về cùng ``chunk_id``; điểm
  chunk = **max** các cửa sổ.
- **Cache vector** theo
  ``sha256([model_key, hf_repo, revision, max_seq_length, prompt, NFC(text)])``
  thành các shard ``.npz`` append-only ⇒ dừng giữa chừng không mất phần đã encode, không encode lại.

Module này **không import torch**; embedder thật nằm ở :mod:`trafficlaw.retrieval.st_embedder`.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
import unicodedata
from collections.abc import Callable, Collection, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

import numpy as np

from trafficlaw.retrieval.bm25 import tokenize
from trafficlaw.retrieval.catalog import Hit
from trafficlaw.retrieval.config import EmbedModelSpec

logger = logging.getLogger(__name__)


class Embedder(Protocol):
    """Embedder: nhận text **đã gắn prompt**, trả ma trận ``(n, dim)`` float32 chuẩn hoá L2."""

    @property
    def dim(self) -> int: ...

    def count_tokens(self, text: str) -> int:
        """Số token (gồm token đặc biệt), không cắt."""
        ...

    def encode(self, texts: Sequence[str], *, batch_size: int = 32) -> np.ndarray: ...


def l2_normalize(m: np.ndarray) -> np.ndarray:
    m = np.asarray(m, dtype=np.float32)
    n = np.linalg.norm(m, axis=1, keepdims=True)
    n[n == 0] = 1.0
    return (m / n).astype(np.float32)


class HashEmbedder:
    """Embedder giả cho test: túi âm tiết băm vào ``dim`` chiều (sha1, tất định), chuẩn hoá L2.
    Token = số âm tiết + 2 (CLS/SEP)."""

    def __init__(self, dim: int = 64) -> None:
        self._dim = dim
        self.calls = 0
        self.n_encoded = 0

    @property
    def dim(self) -> int:
        return self._dim

    def count_tokens(self, text: str) -> int:
        return len(tokenize(text, bigrams=False)) + 2

    def encode(self, texts: Sequence[str], *, batch_size: int = 32) -> np.ndarray:
        self.calls += 1
        self.n_encoded += len(texts)
        out = np.zeros((len(texts), self._dim), dtype=np.float32)
        for i, t in enumerate(texts):
            for tok in tokenize(t, bigrams=False):
                h = int.from_bytes(hashlib.sha1(tok.encode()).digest()[:4], "big")
                out[i, h % self._dim] += 1.0
            if not out[i].any():
                out[i, 0] = 1.0
        return l2_normalize(out)


# --- Cửa sổ ----------------------------------------------------------------------------------


@dataclass(frozen=True)
class Window:
    chunk_id: str
    k: int
    text: str
    """Text cửa sổ (chưa gắn prompt)."""
    n_tokens: int
    """Token của ``prompt + text`` (gồm token đặc biệt)."""
    truncated: bool
    """Vẫn vượt giới hạn (một dòng quá dài) ⇒ model sẽ cắt."""


def split_windows(
    chunk_id: str, text: str, count: Callable[[str], int], max_tokens: int
) -> list[Window]:
    """Chunk vừa ``max_tokens`` → một cửa sổ ``k=0`` (nguyên text). Ngược lại: phần đầu = dòng
    tiêu đề + dòng kế (câu dẫn Khoản / dòng đầu thân), các dòng còn lại gom tham lam sao cho
    ``count(phần đầu + nhóm)`` ≤ ``max_tokens``; không cắt giữa dòng."""
    n = count(text)
    if n <= max_tokens:
        return [Window(chunk_id, 0, text, n, False)]
    lines = text.split("\n")
    head = lines[:2] if len(lines) > 2 else lines[:1]
    rest = lines[len(head) :]
    if not rest:
        return [Window(chunk_id, 0, text, n, True)]
    groups: list[list[str]] = []
    cur: list[str] = []
    for line in rest:
        if cur and count("\n".join([*head, *cur, line])) > max_tokens:
            groups.append(cur)
            cur = []
        cur.append(line)
    groups.append(cur)
    out = []
    for k, g in enumerate(groups):
        t = "\n".join([*head, *g])
        c = count(t)
        out.append(Window(chunk_id, k, t, c, c > max_tokens))
    return out


def chunk_windows(
    chunks: Sequence[tuple[str, str]], spec: EmbedModelSpec, count_tokens: Callable[[str], int]
) -> list[Window]:
    """Cửa sổ của mọi chunk ``[(chunk_id, text)]`` (token tính cả ``doc_prompt``)."""
    p = spec.doc_prompt
    out: list[Window] = []
    for cid, text in chunks:
        out.extend(split_windows(cid, text, lambda t: count_tokens(p + t), spec.max_seq_length))
    return out


# --- Cache vector ----------------------------------------------------------------------------


def cache_key(model_key: str, spec: EmbedModelSpec, kind: str, text: str) -> str:
    raw = [
        model_key,
        spec.hf_repo,
        spec.revision,
        spec.max_seq_length,
        spec.prompt(kind),
        unicodedata.normalize("NFC", text),
    ]
    return hashlib.sha256(json.dumps(raw, ensure_ascii=False).encode()).hexdigest()


class VectorCache:
    """Shard ``part-NNNNN.npz`` (``keys``, ``vecs``) trong ``root``; đọc hết khi mở."""

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self._rows: dict[str, np.ndarray] = {}
        self._pending: dict[str, np.ndarray] = {}
        self._n_shards = 0
        for f in sorted(self.root.glob("part-*.npz")):
            try:
                with np.load(f, allow_pickle=False) as z:
                    for k, v in zip(z["keys"].tolist(), z["vecs"], strict=True):
                        self._rows[str(k)] = v.astype(np.float32)
            except (OSError, ValueError, KeyError) as e:  # shard hỏng (ghi dở) → bỏ, ghi lại sau
                logger.warning("Bỏ shard cache hỏng %s: %s", f.name, e)
                continue
            self._n_shards = max(self._n_shards, int(f.stem.split("-")[1]) + 1)

    def __contains__(self, key: str) -> bool:
        return key in self._rows or key in self._pending

    def __len__(self) -> int:
        return len(self._rows) + len(self._pending)

    def get(self, key: str) -> np.ndarray:
        return self._rows[key] if key in self._rows else self._pending[key]

    def add(self, keys: Sequence[str], vecs: np.ndarray) -> None:
        for k, v in zip(keys, vecs, strict=True):
            self._pending[k] = np.asarray(v, dtype=np.float32)

    def flush(self) -> None:
        if not self._pending:
            return
        keys = sorted(self._pending)
        vecs = np.stack([self._pending[k] for k in keys]).astype(np.float32)
        name = f"part-{self._n_shards:05d}.npz"
        tmp = self.root / (name + ".tmp")
        with tmp.open("wb") as f:
            np.savez(f, keys=np.array(keys), vecs=vecs)
        tmp.replace(self.root / name)
        self._n_shards += 1
        self._rows.update(self._pending)
        self._pending = {}


@dataclass
class EncodeStats:
    n_texts: int = 0
    n_cached: int = 0
    n_encoded: int = 0
    n_tokens: int = 0
    seconds: float = 0.0
    batches: list[int] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        tps = self.n_tokens / self.seconds if self.seconds else None
        return {
            "n_texts": self.n_texts,
            "n_cached": self.n_cached,
            "n_encoded": self.n_encoded,
            "n_tokens": self.n_tokens,
            "seconds": round(self.seconds, 3),
            "tokens_per_s": round(tps, 1) if tps else None,
        }


def encode_cached(
    embedder: Embedder,
    cache: VectorCache,
    model_key: str,
    spec: EmbedModelSpec,
    kind: str,
    texts: Sequence[str],
    *,
    flush_every: int = 512,
    batch_size: int | None = None,
) -> tuple[np.ndarray, EncodeStats]:
    """Vector của ``texts`` (thứ tự đầu vào); chỉ encode text chưa có trong cache, flush mỗi
    ``flush_every`` text. Text trùng encode một lần."""
    prompt = spec.prompt(kind)
    keys = [cache_key(model_key, spec, kind, t) for t in texts]
    todo: dict[str, str] = {}
    for k, t in zip(keys, texts, strict=True):
        if k not in cache and k not in todo:
            todo[k] = t
    st = EncodeStats(n_texts=len(set(keys)), n_cached=len(set(keys)) - len(todo))
    items = list(todo.items())
    bs = batch_size or spec.batch_size
    for i in range(0, len(items), flush_every):
        part = items[i : i + flush_every]
        payload = [prompt + t for _, t in part]
        t0 = time.perf_counter()
        vecs = embedder.encode(payload, batch_size=bs)
        st.seconds += time.perf_counter() - t0
        st.n_tokens += sum(min(embedder.count_tokens(x), spec.max_seq_length) for x in payload)
        if vecs.shape != (len(part), embedder.dim):
            raise ValueError(f"encode trả {vecs.shape}, cần {(len(part), embedder.dim)}")
        cache.add([k for k, _ in part], l2_normalize(vecs))
        cache.flush()
        st.n_encoded += len(part)
        logger.info("%s/%s: %d/%d text", model_key, kind, st.n_encoded, len(items))
    out = np.stack([cache.get(k) for k in keys]) if keys else np.zeros((0, embedder.dim))
    return out.astype(np.float32), st


# --- FAISS -----------------------------------------------------------------------------------


class FaissIndex:
    """``IndexFlatIP`` trên vector chuẩn hoá L2; mỗi dòng ↔ (``chunk_id``, cửa sổ ``k``)."""

    FORMAT = "faiss-flatip-1"

    def __init__(self, index: Any, rows: Sequence[tuple[str, int]], source: str) -> None:
        self.index = index
        self.rows = list(rows)
        self.source = source

    @classmethod
    def build(cls, vecs: np.ndarray, rows: Sequence[tuple[str, int]], source: str) -> FaissIndex:
        import faiss

        if len(rows) != vecs.shape[0]:
            raise ValueError("số dòng vector ≠ số dòng mã")
        idx = faiss.IndexFlatIP(int(vecs.shape[1]))
        idx.add(l2_normalize(vecs))
        return cls(idx, rows, source)

    @property
    def dim(self) -> int:
        return int(self.index.d)

    @property
    def n_chunks(self) -> int:
        return len({c for c, _ in self.rows})

    def save(self, d: str | Path, meta: dict[str, Any] | None = None) -> None:
        import faiss

        p = Path(d)
        p.mkdir(parents=True, exist_ok=True)
        # serialize_index → bytes, tự ghi (tránh đường dẫn không ASCII trên Windows).
        (p / "index.faiss.tmp").write_bytes(faiss.serialize_index(self.index).tobytes())
        (p / "index.faiss.tmp").replace(p / "index.faiss")
        (p / "ids.json").write_text(
            json.dumps([[c, k] for c, k in self.rows], ensure_ascii=False), encoding="utf-8"
        )
        m = {"format": self.FORMAT, "source": self.source, "dim": self.dim, **(meta or {})}
        m.update({"n_rows": len(self.rows), "n_chunks": self.n_chunks})
        (p / "meta.json").write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, d: str | Path) -> FaissIndex:
        import faiss

        p = Path(d)
        meta = json.loads((p / "meta.json").read_text(encoding="utf-8"))
        if meta.get("format") != cls.FORMAT:
            raise ValueError(f"FAISS: định dạng {meta.get('format')!r} — dựng lại")
        idx = faiss.deserialize_index(np.frombuffer((p / "index.faiss").read_bytes(), np.uint8))
        rows = [(str(c), int(k)) for c, k in json.loads((p / "ids.json").read_text("utf-8"))]
        return cls(idx, rows, str(meta["source"]))

    def search(
        self,
        qvecs: np.ndarray,
        top_k: int = 20,
        *,
        allowed: Sequence[Collection[str] | None] | Collection[str] | None = None,
    ) -> list[list[Hit]]:
        """Mỗi câu hỏi → top-k chunk (điểm = max cửa sổ; đồng điểm → ``chunk_id``). ``allowed``
        (một tập cho mọi câu, hoặc danh sách theo câu) lọc **trước** khi lấy top-k."""
        q = l2_normalize(np.atleast_2d(qvecs))
        n = len(self.rows)
        if n == 0:
            return [[] for _ in range(len(q))]
        scores, idx = self.index.search(q, n)
        per_q: list[Collection[str] | None]
        if allowed is None or isinstance(allowed, (set, frozenset)):
            per_q = [allowed] * len(q)  # type: ignore[list-item]
        else:
            per_q = list(allowed)  # type: ignore[arg-type]
        out: list[list[Hit]] = []
        for qi in range(len(q)):
            best: dict[str, float] = {}
            ok = per_q[qi]
            for s, r in zip(scores[qi].tolist(), idx[qi].tolist(), strict=True):
                if r < 0:
                    continue
                cid = self.rows[r][0]
                if ok is not None and cid not in ok:
                    continue
                if cid not in best or s > best[cid]:
                    best[cid] = s
            ranked = sorted(best.items(), key=lambda x: (-x[1], x[0]))[:top_k]
            out.append([Hit(c, float(s), i, self.source) for i, (c, s) in enumerate(ranked, 1)])
        return out


__all__ = [
    "EncodeStats",
    "Embedder",
    "FaissIndex",
    "HashEmbedder",
    "VectorCache",
    "Window",
    "cache_key",
    "chunk_windows",
    "encode_cached",
    "l2_normalize",
    "split_windows",
]
