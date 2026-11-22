"""Fixture M14: danh mục chunk nhỏ tự dựng + model XLM-R tí hon (CPU, không tải mạng)."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from trafficlaw.eval.qa_schema import QAItem
from trafficlaw.retrieval.catalog import ChunkCatalog, ChunkRecord

D0 = date(2025, 1, 1)
D1 = date(2026, 1, 1)
AS_OF = date(2026, 11, 3)


def chunk(cid: str, unit: str, text: str, frm: date = D0, to: date | None = None) -> ChunkRecord:
    parts = unit.split("/")
    return ChunkRecord(
        chunk_id=cid,
        kind="khoan",
        unit_id=unit,
        doc_id=parts[0],
        tier="A",
        dieu_id="/".join(parts[:2]),
        title=text.split("\n")[0],
        text=text,
        effective_from=frm,
        effective_to=to,
        version_ids=(f"{unit}@v0",),
    )


T1, T2, T3 = "Điều 1. Tốc độ\n", "Điều 2. Giấy phép\n", "Điều 3. Đỗ xe\n"
CHUNKS = [
    chunk("VB/D1/K1#2025-01-01", "VB/D1/K1", T1 + "1. Xe ô tô chạy quá tốc độ bị phạt tiền."),
    chunk("VB/D1/K2#2025-01-01", "VB/D1/K2", T1 + "2. Xe mô tô vượt đèn đỏ bị phạt.",
          to=date(2025, 12, 31)),
    chunk("VB/D1/K2#2026-01-01", "VB/D1/K2", T1 + "2. Xe mô tô vượt đèn đỏ bị phạt nặng.", D1),
    chunk("VB/D1/K3#2025-01-01", "VB/D1/K3", T1 + "3. Người đi bộ qua đường sai quy định."),
    chunk("VB/D1/K4#2025-01-01", "VB/D1/K4", T1 + "4. Xe đạp chở quá số người."),
    chunk("VB/D2/K1#2025-01-01", "VB/D2/K1", T2 + "1. Giấy phép lái xe hạng B cấp cho ô tô."),
    chunk("VB/D2/K2#2025-01-01", "VB/D2/K2", T2 + "2. Thời hạn giấy phép lái xe là mười năm."),
    chunk("VB/D3/K1#2025-01-01", "VB/D3/K1", T3 + "1. Đỗ xe trên vỉa hè bị phạt tiền."),
    # Cùng text với VB/D1/K1 (kiểm loại negative "trung_text").
    chunk("VB/D3/K2#2025-01-01", "VB/D3/K2", T1 + "1. Xe ô tô chạy quá tốc độ bị phạt tiền."),
]  # fmt: skip


@pytest.fixture()
def catalog() -> ChunkCatalog:
    return ChunkCatalog(CHUNKS)


def item(qid: str, q: str, cid: str, gold: str, as_of: date = AS_OF) -> QAItem:
    return QAItem(
        qid=qid,
        question=q,
        as_of=as_of,
        question_type="muc_phat",
        tier="A",
        gold_units=[gold],
        source="llm:test",
        chunk_id=cid,
        in_test_gold=False,
    )


# --- model tí hon (torch) ---------------------------------------------------------------------

WORDS = [
    "xe",
    "ô",
    "tô",
    "mô",
    "chạy",
    "quá",
    "tốc",
    "độ",
    "bị",
    "phạt",
    "tiền",
    "vượt",
    "đèn",
    "đỏ",
    "nặng",
    "người",
    "đi",
    "bộ",
    "qua",
    "đường",
    "sai",
    "quy",
    "định",
    "đạp",
    "chở",
    "số",
    "giấy",
    "phép",
    "lái",
    "hạng",
    "b",
    "cấp",
    "cho",
    "thời",
    "hạn",
    "là",
    "mười",
    "năm",
    "đỗ",
    "trên",
    "vỉa",
    "hè",
    "điều",
    "1",
    "2",
    "3",
    "4",
    "bao",
    "nhiêu",
    "nào",
    "gì",
    "có",
    "không",
]


def tiny_tokenizer():
    from tokenizers import Tokenizer, models, normalizers, pre_tokenizers, processors
    from transformers import PreTrainedTokenizerFast

    vocab = {"<s>": 0, "<pad>": 1, "</s>": 2, "<unk>": 3}
    for w in dict.fromkeys(WORDS):
        vocab[w] = len(vocab)
    tk = Tokenizer(models.WordLevel(vocab, unk_token="<unk>"))
    tk.normalizer = normalizers.Lowercase()
    tk.pre_tokenizer = pre_tokenizers.Whitespace()
    tk.post_processor = processors.RobertaProcessing(("</s>", 2), ("<s>", 0))
    return PreTrainedTokenizerFast(
        tokenizer_object=tk, bos_token="<s>", eos_token="</s>", pad_token="<pad>",
        unk_token="<unk>", cls_token="<s>", sep_token="</s>", model_max_length=64,
    )  # fmt: skip


def tiny_config(n_vocab: int, **kw):
    from transformers import XLMRobertaConfig

    return XLMRobertaConfig(
        vocab_size=n_vocab, hidden_size=16, num_hidden_layers=2, num_attention_heads=2,
        intermediate_size=32, max_position_embeddings=80, pad_token_id=1,
        hidden_dropout_prob=0.1, attention_probs_dropout_prob=0.1, **kw,
    )  # fmt: skip


@pytest.fixture(scope="session")
def tiny_st_dir(tmp_path_factory: pytest.TempPathFactory) -> Path:
    pytest.importorskip("torch")
    pytest.importorskip("sentence_transformers")
    import torch
    from sentence_transformers import SentenceTransformer
    from sentence_transformers.sentence_transformer import modules as M  # noqa: N812
    from transformers import XLMRobertaModel

    torch.manual_seed(0)
    raw = tmp_path_factory.mktemp("tiny_raw")
    tok = tiny_tokenizer()
    XLMRobertaModel(tiny_config(len(tok))).save_pretrained(raw)
    tok.save_pretrained(raw)
    tr = M.Transformer(str(raw), max_seq_length=48)
    m = SentenceTransformer(
        modules=[tr, M.Pooling(tr.get_embedding_dimension(), "cls"), M.Normalize()]
    )
    out = tmp_path_factory.mktemp("tiny_st")
    m.save(str(out), create_model_card=False)
    return out


@pytest.fixture(scope="session")
def tiny_ce_dir(tmp_path_factory: pytest.TempPathFactory) -> Path:
    pytest.importorskip("torch")
    pytest.importorskip("transformers")
    import torch
    from transformers import XLMRobertaForSequenceClassification

    torch.manual_seed(0)
    out = tmp_path_factory.mktemp("tiny_ce")
    tok = tiny_tokenizer()
    XLMRobertaForSequenceClassification(tiny_config(len(tok), num_labels=1)).save_pretrained(out)
    tok.save_pretrained(out)
    return out
