"""M5: bảng tên/số hiệu văn bản."""

from __future__ import annotations

from pathlib import Path

import pytest

from trafficlaw.graph.doc_names import DocNameTable, load_doc_aliases, norm_so_hieu, slug
from trafficlaw.registry.loader import load_registry

REPO_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def names() -> DocNameTable:
    reg = load_registry(REPO_ROOT / "data/registry/documents.yaml")
    return DocNameTable(reg, *load_doc_aliases(REPO_ROOT / "data/registry/doc_aliases.yaml"))


def test_norm_so_hieu_and_slug() -> None:
    assert norm_so_hieu(" 168/2024/nđ-cp") == "168/2024/NĐ-CP"
    assert norm_so_hieu("19/2024/QD-TTg") == "19/2024/QĐ-TTG"
    assert slug("Luật Xử lý vi phạm hành chính") == "LUAT-XU-LY-VI-PHAM-HANH-CHINH"
    assert slug("Luật Đường bộ") == "LUAT-DUONG-BO"


def _one(names: DocNameTable, text: str) -> tuple[str, str | None, str]:
    [m] = names.find_all(text)
    return m.kind, m.doc, m.text


def test_so_hieu(names: DocNameTable) -> None:
    assert _one(names, "theo Nghị định số 168/2024/NĐ-CP ngày 26") == (
        "registry",
        "ND168-2024",
        "Nghị định số 168/2024/NĐ-CP",
    )
    assert _one(names, "Thông tư 24/2023/TT-BCA")[:2] == ("external", "EXT:24/2023/TT-BCA")
    # Số hiệu sau tên quyết định văn bản: luật cũ cùng tên gần đúng → ngoài danh mục.
    assert _one(names, "Luật Giao thông đường bộ số 23/2008/QH12")[1] == "EXT:23/2008/QH12"
    assert _one(names, "Luật Đường bộ số 35/2024/QH15")[1] == "LUAT35-2024"


def test_ten_luat(names: DocNameTable) -> None:
    assert _one(names, "của Luật Trật tự, an toàn giao thông đường bộ;")[1] == "LUAT36-2024"
    assert _one(names, "Căn cứ Luật Trật tự an toàn giao thông đường bộ ngày 27")[1] == (
        "LUAT36-2024"
    )
    assert _one(names, "Luật Xử lý vi phạm hành chính năm 2012")[1] == (
        "EXT:LUAT-XU-LY-VI-PHAM-HANH-CHINH"
    )
    # Tên có "theo" / dấu phẩy: lấy từ external_names, không bị cắt.
    assert _one(names, "Luật Đầu tư theo phương thức đối tác công tư và quy định")[1] == (
        "EXT:LUAT-DAU-TU-THEO-PHUONG-THUC-DOI-TAC-CONG-TU"
    )
    assert _one(names, "Luật Khám bệnh, chữa bệnh (sau đây")[1] == "EXT:LUAT-KHAM-BENH-CHUA-BENH"


def test_tu_dai_nhat_thang(names: DocNameTable) -> None:
    ms = names.find_all("Luật Quy hoạch, Luật Quy hoạch đô thị và nông thôn được")
    assert [m.doc for m in ms] == ["EXT:LUAT-QUY-HOACH", "EXT:LUAT-QUY-HOACH-DO-THI-VA-NONG-THON"]


def test_luat_sua_doi_la_van_ban_rieng(names: DocNameTable) -> None:
    text = (
        "Luật sửa đổi, bổ sung một số điều của Luật Tổ chức Chính phủ và Luật Tổ chức chính "
        "quyền địa phương ngày 22 tháng 11 năm 2019;"
    )
    kind, doc, _ = _one(names, text)
    assert kind == "external"
    assert doc == (
        "EXT:LUAT-SUA-DOI-BO-SUNG-MOT-SO-DIEU-CUA-LUAT-TO-CHUC-CHINH-PHU-VA-LUAT-TO-CHUC-"
        "CHINH-QUYEN-DIA-PHUONG"
    )


def test_khong_nhan(names: DocNameTable) -> None:
    assert names.find_all("theo quy định của luật và Nghị định của Chính phủ") == []
    [m] = names.find_all("của Nghị định này")
    assert m.kind == "self"


def test_alias_sai_doc_id() -> None:
    reg = load_registry(REPO_ROOT / "data/registry/documents.yaml")
    with pytest.raises(ValueError, match="không có trong danh mục"):
        DocNameTable(reg, {"KHONG-CO-2024": ["Luật Gì đó"]})
