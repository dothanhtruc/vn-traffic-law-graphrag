"""M8: chọn item, gom lô + dedupe, schema LLM, hậu kiểm, resume, dừng sạch khi hết quota,
dựng ứng viên, cổng publish — không gọi mạng (FakeClient)."""

from __future__ import annotations

import json
import re
from collections.abc import Callable
from pathlib import Path

import pytest

from trafficlaw.graph.embedded import EmbeddedStore
from trafficlaw.graph.extract import (
    BatchConfig,
    Catalog,
    CatalogEntry,
    ExtractConfig,
    Item,
    batch_schema,
    item_key,
    make_batches,
    select_items,
    validate_item_output,
)
from trafficlaw.graph.extract_pipeline import (
    ExtractPaths,
    assemble,
    candidates_sha256,
    done_item_keys,
    publish,
    run_llm,
)
from trafficlaw.llm import LLMClient, LLMTimeoutError, QuotaExhaustedError
from trafficlaw.llm.providers.fake import FakeClient
from trafficlaw.llm.retry import RetryPolicy
from trafficlaw.llm.types import LLMRequest, ProviderResponse, Usage
from trafficlaw.utils.jsonl import read_jsonl

MINI = Path(__file__).resolve().parents[1] / "fixtures/mini_graph"
D6 = "ND168-2024/D6"
CAT = Catalog(
    approved=True,
    phuong_tien=[
        CatalogEntry(id="PT:xe-o-to", name="xe ô tô"),
        CatalogEntry(id="PT:xe-gan-may", name="xe gắn máy"),
    ],
    chu_the=[CatalogEntry(id="CT:nguoi-dieu-khien-xe", name="người điều khiển xe")],
)
CFG = ExtractConfig(batch=BatchConfig(max_items=8, max_chars=6000))
LABEL_RE = re.compile(r"^(?:[a-zđ]\d*\)|\d+[a-z]?\.)\s*")


@pytest.fixture(scope="module")
def store() -> EmbeddedStore:
    return EmbeddedStore.from_dir(MINI)


def responder(req: LLMRequest) -> str:
    """Phản hồi giả: mỗi item một HanhVi = 6 từ đầu của item (nguyên văn), PT xe ô tô, và một
    id ngoài danh mục ở item đầu (để kiểm tra hậu kiểm)."""
    content = req.messages[-1].content
    blocks = re.findall(r"### (I\d+) — (\S+)\n(.+)", content)
    items = []
    for i, (iid, _uid, text) in enumerate(blocks):
        words = LABEL_RE.sub("", text).split()[:6]
        items.append(
            {
                "id": iid,
                "hanh_vi": [{"span": " ".join(words), "ten": " ".join(words[:4])}] if words else [],
                "phuong_tien": ["PT:xe-o-to"] + (["PT:khong-co"] if i == 0 else []),
                "chu_the": ["CT:nguoi-dieu-khien-xe"],
            }
        )
    return json.dumps({"items": items}, ensure_ascii=False)


def make_client(provider: object) -> LLMClient:
    return LLMClient(provider, retry=RetryPolicy(sleep=lambda s: None))  # type: ignore[arg-type]


def paths(tmp: Path) -> ExtractPaths:
    return ExtractPaths(graph_dir=tmp / "graph", out_dir=tmp / "out", catalog=tmp / "cat.yaml")


# --------------------------------------------------------------------------- chọn item / lô


def test_select_items_leaves_with_context(store: EmbeddedStore) -> None:
    items = select_items(store, CFG, ["ND168-2024"])
    by = {i.version_id: i for i in items}
    a = by[f"{D6}/K1/a@v0"]
    assert a.parent_text and a.parent_text.startswith("1. Phạt tiền từ 400.000 đồng")
    assert a.dieu_title.startswith("Xử phạt, trừ điểm giấy phép lái xe")
    assert f"{D6}/K1@v0" not in by  # Khoản có Điểm: câu dẫn chỉ là ngữ cảnh
    assert f"{D6}/K13@v0" in by  # Khoản không có Điểm là item
    m0, m1 = by[f"{D6}/K3/m@v0"], by[f"{D6}/K3/m@v1"]
    assert m0.key != m1.key  # text khác ⇒ hai lượt trích
    assert all(i.dieu_id.startswith("ND168-2024/D") for i in items)


def _item(key: str, dieu: str = "X/D1", n: int = 10) -> Item:
    return Item(key, key, "X", "A", dieu, "t", None, "x" * n, "2025-01-01", None, key)


def test_make_batches_groups_by_dieu_and_dedupes() -> None:
    its = [_item("a"), _item("b"), _item("a"), _item("c", "X/D2"), _item("d"), _item("e")]
    cfg = BatchConfig(group_by="dieu", max_items=2, max_chars=10_000)
    bs = make_batches(its, cfg)
    assert [(b.batch_id, b.keys) for b in bs] == [
        ("X/D1#0", ["a", "b"]),
        ("X/D1#1", ["d", "e"]),
        ("X/D2#0", ["c"]),
    ]
    assert [
        b.keys
        for b in make_batches(its, cfg.model_copy(update={"max_items": 20}), skip_keys={"a", "d"})
    ] == [
        ["b", "e"],
        ["c"],
    ]
    big = make_batches(
        [_item("p", n=50), _item("q", n=50)],
        BatchConfig(group_by="dieu", max_items=9, max_chars=60),
    )
    assert [b.keys for b in big] == [["p"], ["q"]]


def test_make_batches_groups_many_dieu_per_doc() -> None:
    """Mặc định gom nhiều Điều cùng văn bản vào một lượt (quota 20 lượt/ngày)."""
    its = [_item("a"), _item("b", "X/D2"), _item("c", "X/D3")]
    other = Item("z", "z", "Y", "A", "Y/D1", "t", None, "x", "2025-01-01", None, "z")
    bs = make_batches([*its, other], BatchConfig())
    assert [(b.batch_id, b.group_id, b.keys) for b in bs] == [
        ("X#0", "X", ["a", "b", "c"]),
        ("Y#0", "Y", ["z"]),
    ]
    two = make_batches(its, BatchConfig(max_items=2))
    assert [b.keys for b in two] == [["a", "b"], ["c"]]


def test_render_items_prints_each_dieu_title(store: EmbeddedStore) -> None:
    from trafficlaw.graph.extract import render_items

    items = select_items(store, CFG, ["ND168-2024"])
    (b, *_) = make_batches(items, BatchConfig(max_items=500, max_chars=10**7))
    txt = render_items(b)
    dieus = sorted({i.dieu_id for i in b.items})
    assert len(dieus) >= 2  # mini_graph: ND168 Đ6 + Đ12
    for d in dieus:
        assert txt.count(f"({d})") == 1
    assert txt.count("### I") == len(b.items)


def test_item_key_nfc() -> None:
    nfd = "Xe gắn máy".encode().decode()
    import unicodedata

    assert item_key("t", None, unicodedata.normalize("NFD", nfd)) == item_key("t", None, nfd)


def test_batch_schema_enum_and_inline() -> None:
    s = batch_schema(CAT).model_json_schema()
    txt = json.dumps(s)
    assert "$ref" not in txt and "$defs" not in txt
    item = s["properties"]["items"]["items"]["properties"]
    assert item["phuong_tien"]["items"]["enum"] == ["PT:xe-o-to", "PT:xe-gan-may"]
    assert item["chu_the"]["items"]["enum"] == ["CT:nguoi-dieu-khien-xe"]


def test_validate_item_output_rejects() -> None:
    it = Item(
        "v",
        "U/D1/K1/a",
        "U",
        "A",
        "U/D1",
        "t",
        None,
        "a) Điều khiển xe chạy quá tốc độ quy định từ 05 km/h đến dưới 10 km/h;",
        "2025-01-01",
        None,
        "k",
    )
    out = {
        "hanh_vi": [
            {"span": "Điều khiển xe chạy quá  tốc độ quy định", "ten": "chạy quá tốc độ"},
            {"span": "vượt đèn đỏ", "ten": "vượt đèn đỏ"},
            {"span": "chạy quá tốc độ quy định", "ten": "quá tốc độ 20 km/h"},
        ],
        "phuong_tien": ["PT:xe-gan-may", "PT:xe-mo-to"],
        "chu_the": [],
    }
    res, rej = validate_item_output(it, out, CAT)
    assert [h["span"] for h in res.hanh_vi] == ["Điều khiển xe chạy quá tốc độ quy định"]
    assert res.phuong_tien == ["PT:xe-gan-may"]
    assert sorted(r.reason for r in rej) == [
        "ngoai_danh_muc",
        "so_lech_van_ban",
        "span_khong_nguyen_van",
    ]


# --------------------------------------------------------------------------- chạy + resume


def test_run_resume_and_assemble(tmp_path: Path, store: EmbeddedStore) -> None:
    p = paths(tmp_path)
    fake = FakeClient(responder=responder)
    client = make_client(fake)
    o1 = run_llm(store, CFG, CAT, client, p, doc_ids=["ND168-2024"], max_calls=2)
    assert o1.n_called == 2 and o1.n_todo_batches > 2
    # giả lập crash khi đang ghi: dòng cuối bị cắt dở
    with p.raw.open("ab") as f:
        f.write(b'{"batch_id": "cut')
    o2 = run_llm(store, CFG, CAT, client, p, doc_ids=["ND168-2024"])
    assert o2.n_called == o1.n_todo_batches - 2
    calls = fake.n_calls
    o3 = run_llm(store, CFG, CAT, client, p, doc_ids=["ND168-2024"])
    assert o3.n_called == 0 and fake.n_calls == calls  # chạy lại không gọi lại
    recs = list(read_jsonl(p.raw))
    assert len(recs) == o1.n_todo_batches and {r["status"] for r in recs} == {"ok"}
    assert {"usage", "latency_ms", "attempts", "cached", "prompt_hash", "schema_hash"} <= set(
        recs[0]
    )

    rec = assemble(store, CFG, CAT, p, model_id="fake-model", doc_ids=["ND168-2024"])
    assert rec["coverage"]["total"]["done"] == rec["coverage"]["total"]["total"]
    nodes = {n["id"]: n for n in read_jsonl(p.cand_nodes)}
    hv = nodes[f"HV:{D6}/K1/a@v0#0"]
    assert hv["label"] == "HanhVi" and hv["props"]["span"].startswith("Không chấp hành hiệu lệnh")
    edges = list(read_jsonl(p.cand_edges))
    ap = [e for e in edges if e["type"] == "AP_DUNG_CHO" and e["src"] == f"{D6}/K1/a@v0"]
    assert {e["dst"] for e in ap} == {"PT:xe-o-to", "CT:nguoi-dieu-khien-xe"}
    assert "PhuongTien:ngoai_danh_muc" in rec["rejections_by_reason"]
    assert p.summary.is_file() and len(list(read_jsonl(p.report))) == 1
    assert rec["nodes_by_label"]["DiemGPLX"] == 4


class QuotaAfter:
    """Provider giả: trả lời ``n`` lượt rồi báo hết quota ngày."""

    name = "fake"
    model_id = "fake-model"

    def __init__(self, n: int, fn: Callable[[LLMRequest], str]) -> None:
        self.n, self.fn, self.calls = n, fn, 0

    def complete(self, request: LLMRequest) -> ProviderResponse:
        self.calls += 1
        if self.calls > self.n:
            raise QuotaExhaustedError("HTTP 429 per day (fake)", provider="fake", status_code=429)
        return ProviderResponse(text=self.fn(request), usage=Usage(total_tokens=10))


def test_quota_exhausted_stops_cleanly(tmp_path: Path, store: EmbeddedStore) -> None:
    p = paths(tmp_path)
    o = run_llm(
        store,
        CFG,
        CAT,
        make_client(QuotaAfter(1, responder)),
        p,
        doc_ids=["ND168-2024"],
        resume_cmd="uv run python -m scripts.build_graph --extract --doc-id ND168-2024",
    )
    assert o.stopped == "quota" and o.n_called == 1
    assert "scripts.build_graph --extract --doc-id ND168-2024" in o.hint
    assert len(list(read_jsonl(p.raw))) == 1
    o2 = run_llm(
        store, CFG, CAT, make_client(FakeClient(responder=responder)), p, doc_ids=["ND168-2024"]
    )
    assert o2.stopped is None and o2.n_called == o.n_todo_batches - 1


def test_error_is_retried_format_error_is_not(tmp_path: Path, store: EmbeddedStore) -> None:
    from trafficlaw.graph.extract_pipeline import run_key
    from trafficlaw.llm import load_prompt

    p = paths(tmp_path)
    bad = FakeClient(responder=lambda r: "không phải JSON")
    o = run_llm(store, CFG, CAT, make_client(bad), p, doc_ids=["ND168-2024"], max_calls=1)
    assert o.by_status["format_error"] == 1
    key = run_key("fake-model", load_prompt(CFG.llm.prompt), CAT)
    assert len(done_item_keys(p.raw, key)) > 0
    assert done_item_keys(p.raw, key, retry_format_error=True) == set()


def test_catalog_change_invalidates_resume(tmp_path: Path, store: EmbeddedStore) -> None:
    """Sửa danh mục ⇒ schema đổi ⇒ khoá resume đổi ⇒ lô đã chạy với danh mục cũ không dùng lại."""
    p = paths(tmp_path)

    def todo(cat: Catalog, n: int | None) -> int:
        c = make_client(FakeClient(responder=responder))
        return run_llm(store, CFG, cat, c, p, doc_ids=["ND168-2024"], max_calls=n).n_todo_batches

    total = todo(CAT, 1)  # chạy 1 lô với danh mục cũ
    assert todo(CAT, 0) == total - 1
    assert todo(CAT.model_copy(update={"chu_the": []}), 0) == total


# --------------------------------------------------------------------------- publish


def test_publish_gate(tmp_path: Path, store: EmbeddedStore) -> None:
    p = paths(tmp_path)
    assemble(store, CFG, CAT, p, model_id="fake-model", doc_ids=["ND168-2024"])
    rp = tmp_path / "eval.json"
    kw = {"min_entity_f1": 0.85, "min_relation_f1": 0.80}
    assert not publish(p, rp, **kw).ok
    good = {
        "candidates_sha256": candidates_sha256(p),
        "n_reviewed": 3,
        "overall": {"entity": {"f1": 0.9}, "relation": {"f1": 0.85}},
    }
    rp.write_text(json.dumps({**good, "candidates_sha256": "khac"}), encoding="utf-8")
    assert "không phải của bản ứng viên" in publish(p, rp, **kw).message
    rp.write_text(
        json.dumps({**good, "overall": {"entity": {"f1": 0.9}, "relation": {"f1": 0.7}}}),
        encoding="utf-8",
    )
    assert "chưa đạt" in publish(p, rp, **kw).message
    assert not p.sem_nodes.exists()
    rp.write_text(json.dumps(good), encoding="utf-8")
    assert publish(p, rp, **kw).ok
    assert p.sem_nodes.read_bytes() == p.cand_nodes.read_bytes()
    assert p.sem_edges.read_bytes() == p.cand_edges.read_bytes()


# --------------------------------------------------------------------------- tự host: song song


def _records(p: ExtractPaths) -> dict[str, object]:
    return {r["batch_key"]: (r["status"], r["parsed"]) for r in read_jsonl(p.raw)}


def test_workers_same_result_as_sequential(tmp_path: Path, store: EmbeddedStore) -> None:
    p1, p4 = paths(tmp_path / "w1"), paths(tmp_path / "w4")
    o1 = run_llm(
        store, CFG, CAT, make_client(FakeClient(responder=responder)), p1, doc_ids=["ND168-2024"]
    )
    o4 = run_llm(
        store,
        CFG,
        CAT,
        make_client(FakeClient(responder=responder)),
        p4,
        doc_ids=["ND168-2024"],
        workers=4,
    )
    assert o1.n_called == o4.n_called == o1.n_todo_batches
    assert _records(p1) == _records(p4)


class FlakyConnection:
    """Provider giả: request chứa ``marker`` mất kết nối (như tunnel SSH rớt) khi ``down``."""

    name = "local"
    model_id = "fake-model"

    def __init__(self, marker: str) -> None:
        self.marker, self.down, self.calls = marker, True, 0

    def complete(self, request: LLMRequest) -> ProviderResponse:
        self.calls += 1
        if self.down and self.marker in request.messages[-1].content:
            raise LLMTimeoutError("lỗi kết nối (ConnectError)", provider="local")
        return ProviderResponse(text=responder(request), usage=Usage(total_tokens=10))


def test_connection_loss_then_rerun_only_failed(tmp_path: Path, store: EmbeddedStore) -> None:
    p = paths(tmp_path)
    prov = FlakyConnection(f"{D6}/K1/a\n")  # lô chứa Điểm a khoản 1 Điều 6
    meta = {"served_model": "fake-model", "revision": "r1", "vllm_version": "0.0.test"}
    o = run_llm(
        store, CFG, CAT, make_client(prov), p, doc_ids=["ND168-2024"], workers=4, run_meta=meta
    )
    assert o.stopped is None and o.by_status["error"] == 1  # hết retry → ghi error, không dừng
    assert o.by_status["ok"] == o.n_todo_batches - 1
    recs = list(read_jsonl(p.raw))
    assert all(r["serve"] == meta for r in recs)
    prov.down = False
    calls = prov.calls
    o2 = run_llm(store, CFG, CAT, make_client(prov), p, doc_ids=["ND168-2024"], workers=4)
    assert o2.n_todo_batches == 1 and o2.by_status["ok"] == 1  # chỉ lô lỗi được gọi lại
    assert prov.calls == calls + 1


def test_quota_with_workers_keeps_finished(tmp_path: Path, store: EmbeddedStore) -> None:
    p = paths(tmp_path)
    o = run_llm(
        store, CFG, CAT, make_client(QuotaAfter(3, responder)), p, doc_ids=["ND168-2024"], workers=4
    )
    assert o.stopped == "quota"
    n = len(list(read_jsonl(p.raw)))
    assert n == o.n_called >= 3
    o2 = run_llm(
        store,
        CFG,
        CAT,
        make_client(FakeClient(responder=responder)),
        p,
        doc_ids=["ND168-2024"],
        workers=4,
    )
    assert o2.n_todo_batches == o.n_todo_batches - n


def test_output_tokens_per_item_calibration(tmp_path: Path) -> None:
    from trafficlaw.graph.extract_pipeline import output_tokens_per_item
    from trafficlaw.utils.jsonl import write_jsonl

    raw = tmp_path / "raw.jsonl"
    assert output_tokens_per_item(raw) == 200  # chưa có bản ghi → mặc định
    write_jsonl(
        raw,
        [
            {
                "status": "ok",
                "cached": False,
                "item_keys": ["k"] * 10,
                "usage": {"completion_tokens": 1500},
            },
            {
                "status": "ok",
                "cached": False,
                "item_keys": ["k"] * 10,
                "usage": {"completion_tokens": 2500},
            },
            {
                "status": "ok",
                "cached": True,
                "item_keys": ["k"] * 10,
                "usage": {"completion_tokens": 99999},
            },
            {"status": "error", "item_keys": ["k"] * 10, "usage": {"completion_tokens": 7}},
        ],
    )
    assert output_tokens_per_item(raw) == pytest.approx(200.0)  # (1500+2500)/20


def test_postfilter_reference_only_exception_and_generic_pt() -> None:
    it = Item(
        "v",
        "U/D1/K2/a",
        "U",
        "A",
        "U/D1",
        "t",
        None,
        "a) Đi vào đường cao tốc, trừ người phục vụ việc quản lý, bảo trì đường cao tốc; "
        "Thực hiện hành vi quy định tại khoản 12 Điều này bị tước quyền sử dụng giấy phép.",
        "2025-01-01",
        None,
        "k",
    )
    cat = CAT.model_copy(
        update={
            "phuong_tien": [
                *CAT.phuong_tien,
                CatalogEntry(
                    id="PT:phuong-tien-giao-thong-duong-bo", name="phương tiện giao thông đường bộ"
                ),
            ]
        }
    )
    out = {
        "hanh_vi": [
            {
                "span": "Đi vào đường cao tốc, trừ người phục vụ việc quản lý, bảo trì "
                "đường cao tốc",
                "ten": "đi vào cao tốc",
            },
            {"span": "Thực hiện hành vi quy định tại khoản 12 Điều này", "ten": "x"},
        ],
        "phuong_tien": ["PT:phuong-tien-giao-thong-duong-bo", "PT:xe-o-to"],
    }
    res, rej = validate_item_output(it, out, cat)
    assert [h["span"] for h in res.hanh_vi] == ["Đi vào đường cao tốc"]  # cắt ngoại lệ
    assert res.phuong_tien == ["PT:xe-o-to"]  # bỏ mục chung chung khi có loại cụ thể
    assert sorted(r.reason for r in rej) == ["chi_dan_chieu", "pt_chung_chung"]
    only_generic, _ = validate_item_output(
        it, {"phuong_tien": ["PT:phuong-tien-giao-thong-duong-bo"]}, cat
    )
    assert only_generic.phuong_tien == [
        "PT:phuong-tien-giao-thong-duong-bo"
    ]  # không có gì cụ thể hơn


def test_postfilter_definition_article_drops_pt_ct() -> None:
    """Quy tắc 10 của hướng dẫn gán nhãn: Điều "Giải thích từ ngữ" chỉ có KhaiNiem."""
    it = Item(
        "v",
        "U/D2/K3",
        "U",
        "A",
        "U/D2",
        "Điều 2. Giải thích từ ngữ",
        None,
        "3. Xe ô tô là phương tiện có từ bốn bánh trở lên.",
        "2025-01-01",
        None,
        "k",
    )
    out = {"phuong_tien": ["PT:xe-o-to"], "chu_the": []}
    res, rej = validate_item_output(it, out, CAT)
    assert res.phuong_tien == [] and res.chu_the == []
    assert [r.reason for r in rej] == ["dieu_dinh_nghia"]
    other = Item(
        *[*it.__dict__.values()][:5], "Điều 5. Quy tắc chung", *[*it.__dict__.values()][6:]
    )
    kept, _ = validate_item_output(other, out, CAT)
    assert kept.phuong_tien == ["PT:xe-o-to"]
