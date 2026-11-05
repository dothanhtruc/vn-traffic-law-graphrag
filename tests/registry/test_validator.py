from datetime import date
from pathlib import Path
from typing import Any

from trafficlaw.registry.loader import Registry, parse_registry
from trafficlaw.registry.validator import Issue, count_by_level, validate_registry


def doc(doc_id: str = "ND168-2024", **kw: Any) -> dict[str, Any]:
    num, year = doc_id[2:].split("-")[:2]
    base: dict[str, Any] = {
        "doc_id": doc_id,
        "so_hieu": f"{num}/{year}/NĐ-CP",
        "loai": "nghi_dinh",
        "co_quan": "Chính phủ",
        "ngay_ban_hanh": "2024-12-26",
        "hieu_luc_tu": "2025-01-01",
        "tier": "A",
        "source_path": f"data/raw/NghiDinh/{num}.doc",
    }
    return {**base, **kw}


def reg(*docs: dict[str, Any]) -> Registry:
    return parse_registry({"documents": list(docs)})


def codes(issues: list[Issue], level: str | None = None) -> set[tuple[str, str]]:
    return {(i.code, i.doc_id) for i in issues if level is None or i.level == level}


def test_clean_registry_has_no_issues() -> None:
    assert validate_registry(reg(doc(), doc("ND151-2024"))) == []


def test_duplicates() -> None:
    issues = validate_registry(reg(doc(), doc()))
    assert ("DUP_DOC_ID", "ND168-2024") in codes(issues, "error")
    assert ("DUP_SO_HIEU", "ND168-2024") in codes(issues, "error")


def test_duplicate_so_hieu_between_vbhn() -> None:
    # Vấn đề đã biết: một số hiệu VBHN ghi cho cả hai luật.
    v1 = doc(
        "VBHN144-2026-LQ-VPQH",
        so_hieu="144/2026/VBHN-LQ-VPQH",
        loai="vbhn",
        tier="vbhn",
        relations=[{"type": "HOP_NHAT", "target": "ND168-2024"}],
    )
    v2 = {**v1, "doc_id": "VBHN144-2026-VPQH"}
    issues = validate_registry(reg(doc(), v1, v2))
    assert ("DUP_SO_HIEU", "VBHN144-2026-LQ-VPQH") in codes(issues, "error")
    assert ("DUP_SO_HIEU", "VBHN144-2026-VPQH") in codes(issues, "error")


def test_so_hieu_mismatch() -> None:
    issues = validate_registry(reg(doc(so_hieu="186/2024/NĐ-CP")))
    assert ("SO_HIEU_MISMATCH", "ND168-2024") in codes(issues, "error")
    issues = validate_registry(reg(doc(so_hieu="168/2025/NĐ-CP")))
    assert ("SO_HIEU_MISMATCH", "ND168-2024") in codes(issues, "error")


def test_missing_data_are_warnings_not_filled() -> None:
    d = doc(ngay_ban_hanh=None, hieu_luc_tu=None, so_hieu=None, source_path=None)
    r = reg(d)
    issues = validate_registry(r)
    assert codes(issues) == {
        ("MISSING_NGAY_BAN_HANH", "ND168-2024"),
        ("MISSING_HIEU_LUC_TU", "ND168-2024"),
        ("MISSING_SO_HIEU", "ND168-2024"),
        ("MISSING_SOURCE", "ND168-2024"),
    }
    assert count_by_level(issues) == {"error": 0, "warning": 4, "info": 0}
    # Validator không sửa dữ liệu.
    assert r["ND168-2024"].ngay_ban_hanh is None
    assert r["ND168-2024"].hieu_luc_tu is None


def test_date_order() -> None:
    issues = validate_registry(reg(doc(hieu_luc_tu="2024-01-01")))
    assert ("DATE_ORDER", "ND168-2024") in codes(issues, "error")
    issues = validate_registry(reg(doc(hieu_luc_den="2024-12-31")))
    assert ("DATE_ORDER", "ND168-2024") in codes(issues, "error")


def test_expired_must_be_historical() -> None:
    d = doc(hieu_luc_den="2025-08-31")
    assert ("EXPIRED_NOT_HISTORICAL", "ND168-2024") in codes(validate_registry(reg(d)), "warning")
    assert validate_registry(reg(doc(hieu_luc_den="2025-08-31", tier="historical"))) == []


def test_loai_tier_consistency() -> None:
    issues = validate_registry(reg(doc(loai="vbhn")))
    assert ("LOAI_TIER", "ND168-2024") in codes(issues, "error")


def test_source_outside_raw() -> None:
    issues = validate_registry(reg(doc(source_path="data/interim/ND168-2024.txt")))
    assert ("SOURCE_OUTSIDE_RAW", "ND168-2024") in codes(issues, "error")


def test_source_file_check(tmp_path: Path) -> None:
    (tmp_path / "data/raw/NghiDinh").mkdir(parents=True)
    (tmp_path / "data/raw/NghiDinh/168.doc").write_bytes(b"x")
    r = reg(doc(), doc("ND151-2024"))
    issues = validate_registry(r, repo_root=tmp_path)
    assert codes(issues) == {("SOURCE_NOT_FOUND", "ND151-2024")}
    # Không truyền repo_root → không kiểm tra file (dùng cho CI, data/raw không commit).
    assert validate_registry(r) == []


def test_relation_target_must_exist_and_not_self() -> None:
    d = doc(
        relations=[
            {"type": "SUA_DOI", "target": "ND100-2019", "effective_from": "2025-01-01"},
            {"type": "SUA_DOI", "target": "ND168-2024", "effective_from": "2025-01-01"},
        ]
    )
    issues = validate_registry(reg(d))
    assert ("REL_TARGET", "ND168-2024") in codes(issues, "error")
    assert ("REL_SELF", "ND168-2024") in codes(issues, "error")


def test_relation_date_rules() -> None:
    target = doc("ND100-2019", tier="historical", hieu_luc_tu="2020-01-01", ngay_ban_hanh=None)
    no_date = doc(relations=[{"type": "SUA_DOI", "target": "ND100-2019"}])
    issues = validate_registry(reg(no_date, target))
    assert ("REL_NO_DATE", "ND168-2024") in codes(issues, "warning")

    early = doc(
        relations=[{"type": "SUA_DOI", "target": "ND100-2019", "effective_from": "2024-06-01"}]
    )
    issues = validate_registry(reg(early, target))
    assert ("REL_DATE", "ND168-2024") in codes(issues, "error")


def test_full_replacement_sets_target_end() -> None:
    """Bãi bỏ toàn bộ từ D → văn bản đích phải có hieu_luc_den = D − 1."""
    rel = [
        {
            "type": "BAI_BO",
            "target": "ND100-2019",
            "scope": "toan_bo",
            "effective_from": "2025-09-01",
        }
    ]
    ok = doc("ND100-2019", tier="historical", hieu_luc_den="2025-08-31")
    assert validate_registry(reg(doc(relations=rel), ok)) == []

    wrong = {**ok, "hieu_luc_den": "2025-09-01"}
    issues = validate_registry(reg(doc(relations=rel), wrong))
    assert ("TARGET_END_MISMATCH", "ND168-2024") in codes(issues, "error")

    missing = {**ok, "hieu_luc_den": None}
    issues = validate_registry(reg(doc(relations=rel), missing))
    assert ("TARGET_NO_END", "ND168-2024") in codes(issues, "warning")

    # Thay thế một phần không đòi văn bản đích hết hiệu lực.
    partial = [{**rel[0], "scope": "mot_phan"}]
    assert validate_registry(reg(doc(relations=partial), missing)) == []


def test_vbhn_rules() -> None:
    base = doc("VBHN55-VPQH", so_hieu="55/VBHN-VPQH", loai="vbhn", tier="vbhn", hieu_luc_tu=None)
    none = validate_registry(reg(doc(), base))
    assert ("VBHN_TARGET", "VBHN55-VPQH") in codes(none, "error")

    ok = {**base, "relations": [{"type": "HOP_NHAT", "target": "ND168-2024"}]}
    assert validate_registry(reg(doc(), ok)) == []  # VBHN không cần hieu_luc_tu

    extra = {
        **base,
        "relations": [
            {"type": "HOP_NHAT", "target": "ND168-2024"},
            {"type": "SUA_DOI", "target": "ND168-2024", "effective_from": "2025-01-01"},
        ],
    }
    assert ("VBHN_RELATION", "VBHN55-VPQH") in codes(validate_registry(reg(doc(), extra)))

    non_vbhn = doc("ND151-2024", relations=[{"type": "HOP_NHAT", "target": "ND168-2024"}])
    assert ("VBHN_RELATION", "ND151-2024") in codes(validate_registry(reg(doc(), non_vbhn)))

    points_to_vbhn = doc(
        "ND151-2024",
        relations=[{"type": "SUA_DOI", "target": "VBHN55-VPQH", "effective_from": "2025-01-01"}],
    )
    assert ("REL_TARGET", "ND151-2024") in codes(validate_registry(reg(doc(), ok, points_to_vbhn)))


def test_amendment_rules() -> None:
    target = doc("ND158-2024", tier="B")
    no_target = doc(
        "ND218-2026",
        tier="B",
        is_amendment=True,
        ngay_ban_hanh="2026-06-19",
        hieu_luc_tu="2026-08-10",
    )
    assert ("AMEND_NO_TARGET", "ND218-2026") in codes(validate_registry(reg(target, no_target)))

    rel = [{"type": "SUA_DOI", "target": "ND158-2024", "effective_from": "2026-08-10"}]
    ok = {**no_target, "relations": rel}
    assert validate_registry(reg(target, ok)) == []

    wrong_tier = {**ok, "tier": "A"}
    assert ("AMEND_TIER", "ND218-2026") in codes(validate_registry(reg(target, wrong_tier)))


def test_after_cutoff_only_if_amending_tier_a() -> None:
    cutoff = date(2026, 11, 3)
    a = doc("ND168-2024")
    late = doc("ND300-2026", ngay_ban_hanh="2026-11-20", hieu_luc_tu="2027-01-01")
    issues = validate_registry(reg(a, late), cutoff=cutoff)
    assert ("AFTER_CUTOFF", "ND300-2026") in codes(issues, "error")

    rel = [{"type": "SUA_DOI", "target": "ND168-2024", "effective_from": "2027-01-01"}]
    late_amend = {**late, "is_amendment": True, "relations": rel}
    assert validate_registry(reg(a, late_amend), cutoff=cutoff) == []

    b = doc("ND158-2024", tier="B")
    late_b = {**late_amend, "tier": "B", "relations": [{**rel[0], "target": "ND158-2024"}]}
    issues = validate_registry(reg(b, late_b), cutoff=cutoff)
    assert ("AFTER_CUTOFF", "ND300-2026") in codes(issues, "error")


def test_known_issues_reported_as_info() -> None:
    issues = validate_registry(reg(doc(issues=["sửa cả văn bản đường sắt"])))
    assert [(i.level, i.message) for i in issues] == [("info", "sửa cả văn bản đường sắt")]
