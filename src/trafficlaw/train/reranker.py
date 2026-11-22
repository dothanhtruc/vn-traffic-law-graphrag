"""Fine-tune reranker (M14): cross-encoder ``AITeamVN/Vietnamese_Reranker`` (ghim revision) bằng
``AutoModelForSequenceClassification`` + tokenizer ``tokenizer.json`` của
``BAAI/bge-reranker-v2-m3`` (như ``retrieval/rerank.py`` — repo reranker chỉ có
``sentencepiece.bpe.model``, trùng sha256), cắt cặp ở ``max_length`` 512 giống lúc suy luận.

Loss listwise (:func:`losses.listwise_loss`): mỗi nhóm = câu hỏi với 1 positive + ``n_neg`` hard
negative (câu không có negative bị bỏ). Một bước tối ưu = ``batch_size`` × ``grad_accum`` nhóm
(CLAUDE.md mục 9: 16 × 2); mỗi lượt forward ``mini_batch_size`` nhóm (OOM → giảm một nửa). Lưu
bằng ``save_pretrained`` (model + tokenizer) ⇒ ``STReranker`` nạp trực tiếp từ HF Hub.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import torch

from trafficlaw.eval.retrieval_eval import EvalQuery
from trafficlaw.retrieval.catalog import ChunkCatalog
from trafficlaw.retrieval.config import RerankerSpec
from trafficlaw.train.config import TrainParams
from trafficlaw.train.data import TrainExample, plain_batches, training_plan
from trafficlaw.train.evaluate import rerank_eval
from trafficlaw.train.loop import StepCtx, Task
from trafficlaw.train.losses import listwise_loss

logger = logging.getLogger(__name__)


def load_cross_encoder(spec: RerankerSpec, device: str) -> tuple[Any, Any]:
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    t = spec.count_tokenizer
    tok = AutoTokenizer.from_pretrained(
        t.hf_repo if t else spec.hf_repo, revision=(t.revision if t else spec.revision)
    )
    model = AutoModelForSequenceClassification.from_pretrained(
        spec.hf_repo, revision=spec.revision, torch_dtype=torch.float32
    ).to(device)
    return model, tok


def groups_of(ex: TrainExample, n_neg: int) -> list[tuple[str, str]]:
    return [(ex.question, ex.pos_text)] + [(ex.question, t) for t in ex.neg_texts[:n_neg]]


def build_reranker_task(
    *,
    spec: RerankerSpec,
    examples: Sequence[TrainExample],
    params: TrainParams,
    device: str,
    catalog: ChunkCatalog | None,
    val: Sequence[EvalQuery],
    pools: Mapping[str, Mapping[str, Any]] | None,
    fingerprint: dict[str, Any],
    model: Any = None,
    tokenizer: Any = None,
    eval_batch: int = 64,
) -> Task:
    if model is None or tokenizer is None:
        model, tokenizer = load_cross_encoder(spec, device)
    if params.gradient_checkpointing:
        model.gradient_checkpointing_enable()
    ex = [e for e in examples if e.neg_texts]
    groups = [groups_of(e, params.n_neg) for e in ex]
    step_groups = params.batch_size * params.grad_accum
    plan = training_plan(
        lambda ep: plain_batches(len(groups), step_groups, seed=params.seed, epoch=ep),
        params.epochs,
    )

    def logits(pairs: Sequence[tuple[str, str]]) -> torch.Tensor:
        enc = tokenizer(
            [p[0] for p in pairs], [p[1] for p in pairs], padding=True, truncation=True,
            max_length=spec.max_length, return_tensors="pt",
        ).to(device)  # fmt: skip
        return model(**enc, return_dict=True).logits.view(-1)

    def step_fn(batch: list[int], micro: int, ctx: StepCtx) -> float:
        total = 0.0
        n = len(batch)
        for i in range(0, n, micro):
            part = [groups[j] for j in batch[i : i + micro]]
            flat = [p for g in part for p in g]
            with ctx.autocast():
                out = logits(flat)
            per = list(out.split([len(g) for g in part]))
            loss = listwise_loss(per) * (len(part) / n)
            ctx.backward(loss)
            total += float(loss.detach())
        return total

    def count_tokens(text: str) -> int:
        return len(tokenizer(text, add_special_tokens=True, truncation=False)["input_ids"])

    def evaluate(ctx: StepCtx) -> dict[str, Any]:
        assert catalog is not None and pools is not None

        def score(pairs: Sequence[tuple[str, str]]) -> list[float]:
            order = sorted(range(len(pairs)), key=lambda i: len(pairs[i][0]) + len(pairs[i][1]))
            out = [0.0] * len(pairs)
            for s in range(0, len(order), eval_batch):
                idx = order[s : s + eval_batch]
                with ctx.autocast():
                    v = logits([pairs[j] for j in idx]).float().cpu().tolist()
                for j, x in zip(idx, v, strict=True):
                    out[j] = float(x)
            return out

        return rerank_eval(
            score, count_tokens, pools, val, catalog, max_length=spec.max_length, seed=params.seed
        )

    def save_model(d: Path) -> None:
        model.save_pretrained(str(d))
        tokenizer.save_pretrained(str(d))

    def load_model(d: Path) -> None:
        from transformers import AutoModelForSequenceClassification

        src = AutoModelForSequenceClassification.from_pretrained(str(d), torch_dtype=torch.float32)
        model.load_state_dict(src.state_dict())

    return Task(
        model=model,
        plan=plan,
        step_fn=step_fn,
        evaluate=evaluate if (catalog is not None and pools and val) else None,
        save_model=save_model,
        load_model=load_model,
        fingerprint=fingerprint,
        info={
            "kind": "reranker",
            "base": f"{spec.hf_repo}@{spec.revision}",
            "n_examples": len(examples),
            "n_groups": len(groups),
            "n_dropped_no_negative": len(examples) - len(ex),
            "n_pairs_per_epoch": sum(len(g) for g in groups),
            "n_batches": len(plan),
        },
    )


__all__ = ["build_reranker_task", "groups_of", "load_cross_encoder"]
