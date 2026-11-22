"""M14: vòng huấn luyện trên CPU với model tí hon — resume (ngắt giữa chừng, cả từ HF Hub giả)
cho kết quả y hệt chạy liền; OOM giảm mini-batch; checkpoint tốt nhất; reranker."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

import pytest

torch = pytest.importorskip("torch")
pytest.importorskip("sentence_transformers")

from trafficlaw.eval.retrieval_eval import EvalQuery  # noqa: E402
from trafficlaw.retrieval.catalog import ChunkCatalog  # noqa: E402
from trafficlaw.retrieval.config import EmbedModelSpec, RerankerSpec  # noqa: E402
from trafficlaw.retrieval.dense import Window  # noqa: E402
from trafficlaw.train.checkpoint import HubSync, latest_checkpoint  # noqa: E402
from trafficlaw.train.config import TrainParams  # noqa: E402
from trafficlaw.train.data import WindowTable, build_examples  # noqa: E402
from trafficlaw.train.embedding import build_embedding_task  # noqa: E402
from trafficlaw.train.loop import ResumeMismatchError, Task, run_loop  # noqa: E402
from trafficlaw.train.reranker import build_reranker_task  # noqa: E402
from trafficlaw.train.run_log import RunLog, read_events  # noqa: E402
from trafficlaw.utils.seed import set_seed  # noqa: E402

from .conftest import AS_OF, item  # noqa: E402

NEGS = {
    "q1": ["VB/D3/K1#2025-01-01", "VB/D2/K2#2025-01-01"],
    "q2": ["VB/D1/K3#2025-01-01"],
    "q3": ["VB/D2/K1#2025-01-01", "VB/D1/K4#2025-01-01"],
    "q4": ["VB/D3/K1#2025-01-01"],
    "q5": ["VB/D1/K1#2025-01-01"],
}


def _examples(catalog: ChunkCatalog):
    items = [
        item("q1", "ô tô chạy quá tốc độ bị phạt bao nhiêu", "VB/D1/K1#2025-01-01", "VB/D1/K1"),
        item("q2", "mô tô vượt đèn đỏ bị phạt", "VB/D1/K2#2026-01-01", "VB/D1/K2"),
        item("q3", "người đi bộ qua đường sai quy định", "VB/D1/K3#2025-01-01", "VB/D1/K3"),
        item("q4", "giấy phép lái xe hạng b cấp cho xe nào", "VB/D2/K1#2025-01-01", "VB/D2/K1"),
        item("q5", "đỗ xe trên vỉa hè có bị phạt không", "VB/D3/K1#2025-01-01", "VB/D3/K1"),
    ]
    return build_examples(items, catalog, WindowTable([]), NEGS, 2)


VAL = [
    EvalQuery("v1", "đỗ xe trên vỉa hè", AS_OF, ("VB/D3/K1",), "A", "muc_phat"),
    EvalQuery("v2", "thời hạn giấy phép lái xe", AS_OF, ("VB/D2/K2",), "A", "khac"),
]
PARAMS = TrainParams(
    epochs=2, lr=1e-3, batch_size=3, mini_batch_size=2, n_neg=1, save_steps=1, log_steps=1,
    warmup_ratio=0.25, dtype="fp32",
)  # fmt: skip


class FakeApi:
    """HfApi giả: lưu thư mục đã đẩy theo (repo, path) trong ``store``."""

    def __init__(self, store: Path) -> None:
        self.store = store
        self.calls: list[tuple[str, str | None, str]] = []
        self.n = 0

    def whoami(self) -> dict[str, str]:
        return {"name": "tester"}

    def create_repo(self, repo: str, **kw: Any) -> None:
        self.calls.append(("create", repo, ""))

    def upload_folder(self, *, repo_id, folder_path, path_in_repo=None, commit_message=""):
        self.n += 1
        dst = self.store / repo_id / (path_in_repo or "_root")
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(folder_path, dst)
        self.calls.append(("upload", repo_id, path_in_repo or ""))
        return type("CI", (), {"oid": f"sha{self.n:03d}"})()

    def snapshot_download(self, *, repo_id, allow_patterns, local_dir):
        src = self.store / repo_id / "last"
        if not src.exists():
            raise FileNotFoundError(repo_id)
        shutil.copytree(src, Path(local_dir) / "last", dirs_exist_ok=True)
        return local_dir


def _emb_task(tiny_st_dir: Path, catalog: ChunkCatalog, params=PARAMS):
    spec = EmbedModelSpec(hf_repo=str(tiny_st_dir), max_seq_length=48)
    ws = [Window(c.chunk_id, 0, c.text, 10, False) for c in catalog.chunks]
    return build_embedding_task(
        spec=spec, examples=_examples(catalog), params=params, device="cpu", windows=ws,
        catalog=catalog, val=VAL, fingerprint={"data": "x", "params": params.model_dump()},
    )  # fmt: skip


def _state(task: Task) -> dict[str, Any]:
    return {k: v.detach().clone() for k, v in task.model.state_dict().items()}


def _run(task, tmp: Path, name: str, hub: HubSync | None = None, **kw):
    hub = hub or HubSync(name, enabled=False)
    return run_loop(
        task, PARAMS, run_dir=tmp / name, log=RunLog(tmp / f"{name}.jsonl"), hub=hub,
        device="cpu", **kw,
    )  # fmt: skip


def test_resume_matches_uninterrupted(tiny_st_dir: Path, catalog: ChunkCatalog, tmp_path: Path):
    set_seed(42)
    a = _emb_task(tiny_st_dir, catalog)
    n = len(a.plan)
    assert n >= 4
    sa = _run(a, tmp_path, "a")
    assert sa["steps"] == n and sa["best_step"] is not None
    final_a = _state(a)

    set_seed(42)
    b1 = _emb_task(tiny_st_dir, catalog)
    assert _run(b1, tmp_path, "b", stop_after=2) == {"stopped_at": 2}
    set_seed(123)  # RNG khác — phải được khôi phục từ checkpoint
    b2 = _emb_task(tiny_st_dir, catalog)
    sb = _run(b2, tmp_path, "b")
    assert sb["steps"] == n
    for k, v in final_a.items():
        assert torch.allclose(v, b2.model.state_dict()[k], atol=1e-6), k
    ev = [e["event"] for e in read_events(tmp_path / "b.jsonl")]
    assert "stopped" in ev and "resume" in ev
    # Đánh giá cuối epoch giống nhau ở hai cách chạy.
    ea = [e["metrics"]["recall@5"] for e in read_events(tmp_path / "a.jsonl", "eval")]
    eb = [e["metrics"]["recall@5"] for e in read_events(tmp_path / "b.jsonl", "eval")]
    assert ea == eb and len(ea) == 2


def test_resume_from_hub_and_push_best(tiny_st_dir: Path, catalog: ChunkCatalog, tmp_path: Path):
    api = FakeApi(tmp_path / "hub")
    set_seed(42)
    t1 = _emb_task(tiny_st_dir, catalog)
    _run(t1, tmp_path, "h", hub=HubSync("run-x", api=api), stop_after=3)
    shutil.rmtree(tmp_path / "h")  # máy thuê bị xoá: chỉ còn HF Hub
    set_seed(7)
    t2 = _emb_task(tiny_st_dir, catalog)
    s = _run(t2, tmp_path, "h", hub=HubSync("run-x", api=api))
    assert s["steps"] == len(t2.plan) and s["best_commit"].startswith("sha")
    ups = [(r, p) for kind, r, p in api.calls if kind == "upload"]
    assert ("tester/run-x-ckpt", "last") in ups
    assert ("tester/run-x", "") in ups and ("tester/run-x-ckpt", "final") in ups
    assert any(e["event"] == "resume" for e in read_events(tmp_path / "h.jsonl"))


def test_resume_refuses_other_params(tiny_st_dir: Path, catalog: ChunkCatalog, tmp_path: Path):
    set_seed(42)
    _run(_emb_task(tiny_st_dir, catalog), tmp_path, "m", stop_after=1)
    other = PARAMS.model_copy(update={"lr": 5e-4})
    with pytest.raises(ResumeMismatchError):
        _run(_emb_task(tiny_st_dir, catalog, other), tmp_path, "m")


def test_oom_halves_micro_batch(tmp_path: Path) -> None:
    lin = torch.nn.Linear(2, 1)
    seen: list[int] = []

    def step(batch, micro, ctx):
        seen.append(micro)
        if len(seen) == 1:
            raise torch.cuda.OutOfMemoryError("giả")
        loss = lin(torch.ones(1, 2)).sum()
        ctx.backward(loss)
        return float(loss.detach())

    task = Task(
        model=lin, plan=[(0, [0]), (0, [1])], step_fn=step, evaluate=None,
        save_model=lambda d: d.mkdir(parents=True, exist_ok=True), load_model=lambda d: None,
        fingerprint={},
    )  # fmt: skip
    s = _run(task, tmp_path, "o")
    assert s["steps"] == 2 and seen == [2, 1, 1]
    oom = read_events(tmp_path / "o.jsonl", "oom")
    assert oom and oom[0]["new_micro"] == 1
    assert latest_checkpoint(tmp_path / "o") is not None


def test_dry_run_max_steps(tiny_st_dir: Path, catalog: ChunkCatalog, tmp_path: Path) -> None:
    set_seed(42)
    s = _run(_emb_task(tiny_st_dir, catalog), tmp_path, "d", max_steps=2)
    assert s["steps"] == 2


def test_reranker_task(tiny_ce_dir: Path, catalog: ChunkCatalog, tmp_path: Path) -> None:
    spec = RerankerSpec(hf_repo=str(tiny_ce_dir), max_length=48)
    pools = {
        "v1": {"pool": ["VB/D3/K1#2025-01-01", "VB/D1/K1#2025-01-01"], "base": {}},
        "v2": {"pool": ["VB/D2/K2#2025-01-01", "VB/D2/K1#2025-01-01"], "base": {}},
    }
    ex = _examples(catalog)
    params = PARAMS.model_copy(update={"n_neg": 2, "batch_size": 2, "grad_accum": 1})
    set_seed(42)
    task = build_reranker_task(
        spec=spec, examples=ex, params=params, device="cpu", catalog=catalog, val=VAL,
        pools=pools, fingerprint={"x": 1},
    )  # fmt: skip
    assert task.info["n_groups"] == 5 and task.info["n_pairs_per_epoch"] == 3 + 2 + 3 + 2 + 2
    s = run_loop(
        task, params, run_dir=tmp_path / "r", log=RunLog(tmp_path / "r.jsonl"),
        hub=HubSync("r", enabled=False), device="cpu",
    )  # fmt: skip
    assert s["steps"] == len(task.plan) == 6
    ev = read_events(tmp_path / "r.jsonl", "eval")
    assert len(ev) == 2 and ev[0]["metrics"]["n_pairs"] == 4
    assert (tmp_path / "r" / "best" / "tokenizer.json").is_file()
