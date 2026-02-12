import pytest

from src.widget import get_date, mask_account_card


def test_16_digit_card(case_16_digit_card):
    input_val, expected = case_16_digit_card
    assert mask_account_card(input_val) == expected


def test_12_digit_card(case_12_digit_card):
    input_val, expected = case_12_digit_card
    assert mask_account_card(input_val) == expected


def test_only_digits(case_only_digits):
    input_val, expected = case_only_digits
    assert mask_account_card(input_val) == expected


def test_account_ru(case_account_ru):
    input_val, expected = case_account_ru
    assert mask_account_card(input_val) == expected


def test_account_en(case_account_en):
    input_val, expected = case_account_en
    assert mask_account_card(input_val) == expected


def test_short_account(case_short_account):
    input_val, expected = case_short_account
    assert mask_account_card(input_val) == expected


def test_single_digit(case_single_digit):
    input_val, expected = case_single_digit
    assert mask_account_card(input_val) == expected


def test_empty(case_empty):
    input_val, expected = case_empty
    assert mask_account_card(input_val) == expected


def test_non_digits(case_non_digits):
    input_val, expected = case_non_digits
    assert mask_account_card(input_val) == expected


def test_whitespace(case_whitespace):
    input_val, expected = case_whitespace
    assert mask_account_card(input_val) == expected


def test_none_raises_error(case_none):
    with pytest.raises(TypeError):
        mask_account_card(case_none)


def test_standard(date_standard):
    input_val, expected = date_standard
    assert get_date(input_val) == expected


def test_edge_start(date_edge_start):
    input_val, expected = date_edge_start
    assert get_date(input_val) == expected


def test_edge_end(date_edge_end):
    input_val, expected = date_edge_end
    assert get_date(input_val) == expected


def test_leap(date_leap):
    input_val, expected = date_leap
    assert get_date(input_val) == expected


def test_min_year(date_min):
    input_val, expected = date_min
    assert get_date(input_val) == expected


def test_max_year(date_max):
    input_val, expected = date_max
    assert get_date(input_val) == expected
