import unicodedata
from datetime import date

import pytest
from pydantic import ValidationError

from trafficlaw.registry.loader import parse_registry
from trafficlaw.registry.schema import DocumentMeta

BASE = {
    "doc_id": "ND168-2024",
    "so_hieu": "168/2024/NĐ-CP",
    "loai": "nghi_dinh",
    "co_quan": "Chính phủ",
    "ngay_ban_hanh": "2024-12-26",
    "hieu_luc_tu": "2025-01-01",
    "tier": "A",
    "source_path": "data/raw/NghiDinh/168.2024.NĐ.CP.doc",
}


def test_parse_minimal() -> None:
    d = DocumentMeta.model_validate(BASE)
    assert d.hieu_luc_tu == date(2025, 1, 1)
    assert d.hieu_luc_den is None
    assert d.relations == ()
    assert d.indexable


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("doc_id", "nd168-2024"),  # chữ thường
        ("doc_id", "ND168/2024"),
        ("loai", "chi_thi"),
        ("tier", "D"),
        ("hieu_luc_tu", "01/01/2025"),  # phải là ISO
    ],
)
def test_invalid_format(field: str, value: str) -> None:
    with pytest.raises(ValidationError):
        DocumentMeta.model_validate({**BASE, field: value})


def test_unknown_field_rejected() -> None:
    with pytest.raises(ValidationError):
        DocumentMeta.model_validate({**BASE, "hieu_luc": "2025-01-01"})


def test_relation_target_format() -> None:
    with pytest.raises(ValidationError):
        DocumentMeta.model_validate(
            {**BASE, "relations": [{"type": "SUA_DOI", "target": "NĐ 100/2019"}]}
        )
    with pytest.raises(ValidationError):
        DocumentMeta.model_validate(
            {**BASE, "relations": [{"type": "DAN_CHIEU", "target": "ND100-2019"}]}
        )


def test_nfc_and_posix_path() -> None:
    nfd = unicodedata.normalize("NFD", "Chính phủ")
    d = DocumentMeta.model_validate(
        {**BASE, "co_quan": nfd, "source_path": "data\\raw\\NghiDinh\\x.doc", "issues": [nfd]}
    )
    assert d.co_quan == unicodedata.normalize("NFC", "Chính phủ")
    assert d.issues == (unicodedata.normalize("NFC", "Chính phủ"),)
    assert d.source_path == "data/raw/NghiDinh/x.doc"


def test_indexable_excludes_vbhn_and_amendments() -> None:
    assert not DocumentMeta.model_validate({**BASE, "is_amendment": True}).indexable
    vbhn = {**BASE, "doc_id": "VBHN55-VPQH", "loai": "vbhn", "tier": "vbhn"}
    assert not DocumentMeta.model_validate(vbhn).indexable


def test_parse_registry_shape() -> None:
    reg = parse_registry({"documents": [BASE]})
    assert len(reg) == 1
    assert "ND168-2024" in reg
    assert reg["ND168-2024"].so_hieu == "168/2024/NĐ-CP"
    with pytest.raises(ValueError):
        parse_registry([BASE])
