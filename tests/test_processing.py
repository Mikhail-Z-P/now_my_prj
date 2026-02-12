import pytest

from src.processing import filter_by_state, sort_by_date


def test_default(trans_default):
    transactions, expected = trans_default
    assert filter_by_state(transactions) == expected


def test_custom(trans_custom):
    transactions, expected = trans_custom
    assert filter_by_state(transactions, state="PENDING") == expected


def test_empty(empty_trans):
    transactions, expected = empty_trans
    assert filter_by_state(transactions) == expected


def test_no_match(trans_no_match):
    transactions, expected = trans_no_match
    assert filter_by_state(transactions, state="EXECUTED") == expected


def test_missing_key(trans_missing_key):
    transactions, expected = trans_missing_key
    assert filter_by_state(transactions) == expected


def test_all_match(trans_all_match):
    transactions, expected = trans_all_match
    assert filter_by_state(transactions) == expected


def test_case_sensitive(trans_case_sensitive):
    transactions, expected = trans_case_sensitive
    assert filter_by_state(transactions, state="EXECUTED") == expected


def test_non_string(trans_non_string):
    transactions, expected = trans_non_string
    assert filter_by_state(transactions, state=1) == expected


def test_asc(data_asc):
    inp, exp = data_asc
    assert sort_by_date(inp, sorting=True) == exp


def test_desc(data_desc):
    inp, exp = data_desc
    assert sort_by_date(inp, sorting=False) == exp


def test_single(single):
    inp, exp = single
    assert sort_by_date(inp) == exp


def test_missing(missing_date):
    inp, exp = missing_date
    assert sort_by_date(inp, sorting=True) == exp


def test_same(same_dates):
    inp, exp = same_dates
    assert sort_by_date(inp, sorting=True) == exp


def test_iso(iso_dates):
    inp, exp = iso_dates
    assert sort_by_date(inp, sorting=True) == exp


def test_orig(orig):
    orig_copy = orig.copy()
    sort_by_date(orig_copy, sorting=True)
    assert orig_copy == orig


def test_num(num_dates):
    inp, exp = num_dates
    assert sort_by_date(inp, sorting=True) == exp


def test_mixed(mixed):
    with pytest.raises(TypeError):
        sort_by_date(mixed, sorting=True)
