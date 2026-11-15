"""M11: chỉ số độ phủ liên kết (che_tai qua BI_*/dan_chieu, DAN_CHIEU khác Điều)."""

from __future__ import annotations

from datetime import date

from trafficlaw.eval.retrieval_linked import dieu_of, linked_coverage, linked_units

D = date(2026, 1, 1)


def test_dieu_of() -> None:
    assert dieu_of("ND168-2024/D6/K10/a") == "ND168-2024/D6"
    assert dieu_of("LUAT36-2024/D52a/K1") == "LUAT36-2024/D52a"
    assert dieu_of("ND168-2024") is None


def test_linked_units(mini_store) -> None:
    # Đ6 K10 a/b bị trừ điểm theo Đ6 K16 d (dan_chieu); DAN_CHIEU tới K11 cùng Điều → không tính.
    got = linked_units(mini_store, ["ND168-2024/D6/K10"], D)
    assert got.get("ND168-2024/D6/K16/d") == "che_tai"
    assert not any(u.startswith("ND168-2024/D6/K11") for u, k in got.items() if k == "dan_chieu")
    # Đ12 K10 dẫn chiếu sang Điều 6 → dan_chieu.
    got2 = linked_units(mini_store, ["ND168-2024/D12/K10"], D)
    assert {"ND168-2024/D6/K11/b", "ND168-2024/D6/K11/d"} <= {
        u for u, k in got2.items() if k == "dan_chieu"
    }
    # Đích trùng/con cháu của gold bị bỏ.
    assert not any(u.startswith("ND168-2024/D6/K10") for u in got)


def test_linked_coverage(mini_store, mini_catalog) -> None:
    k16 = mini_catalog.chunks_of_unit("ND168-2024/D6/K16", D)
    k10 = mini_catalog.chunks_of_unit("ND168-2024/D6/K10", D)
    hit = linked_coverage(mini_store, mini_catalog, [("q", ["ND168-2024/D6/K10"], D, k10 + k16)])
    miss = linked_coverage(mini_store, mini_catalog, [("q", ["ND168-2024/D6/K10"], D, k10)])
    assert hit["n_cau_co_lien_ket"] == 1 and hit["theo_loai"]["che_tai"]["do_phu"] == 1.0
    assert miss["theo_loai"]["che_tai"]["do_phu"] == 0.0
    none = linked_coverage(mini_store, mini_catalog, [("q", ["ND168-2024/D6/K1"], D, [])])
    assert none["n_cau_co_lien_ket"] in (0, 1)
