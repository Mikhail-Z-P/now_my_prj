import pytest

from src.widget import get_date, mask_account_card

@pytest.mark.parametrize(
    "case",
    [
        "case_16_digit_card",
        "case_12_digit_card",
        "case_only_digits",
        "case_account_ru",
        "case_account_en",
    ],
    ids=[
        "16-значная карта",
        "12-значная карта",
        "строка из цифр",
        "аккаунт (русифицированный)",
        "аккаунт (англоязычный)",
    ]
)
def test_mask_account_card(case, request):
    """Проверка маскировки аккаунта для разных форматов данных."""
    input_val, expected = request.getfixturevalue(case)
    assert mask_account_card(input_val) == expected

# def test_16_digit_card(case_16_digit_card):
#     """Проверка маскировки 16-значной карты."""
#     input_val, expected = case_16_digit_card
#     assert mask_account_card(input_val) == expected
#
#
# def test_12_digit_card(case_12_digit_card):
#     """Проверка маскировки 12-значной карты."""
#     input_val, expected = case_12_digit_card
#     assert mask_account_card(input_val) == expected
#
#
# def test_only_digits(case_only_digits):
#     """Проверка маскировки строки из одних цифр."""
#     input_val, expected = case_only_digits
#     assert mask_account_card(input_val) == expected
#
#
# def test_account_ru(case_account_ru):
#     """Проверка маскировки аккаунта (русифицированный формат)."""
#     input_val, expected = case_account_ru
#     assert mask_account_card(input_val) == expected
#
#
# def test_account_en(case_account_en):
#     """Проверка маскировки аккаунта (англоязычный формат)."""
#     input_val, expected = case_account_en
#     assert mask_account_card(input_val) == expected


def test_short_account(case_short_account):
    """Проверка маскировки короткого аккаунта."""
    input_val, expected = case_short_account
    assert mask_account_card(input_val) == expected


def test_single_digit(case_single_digit):
    """Проверка маскировки одной цифры."""
    input_val, expected = case_single_digit
    assert mask_account_card(input_val) == expected


def test_empty(case_empty):
    """Проверка обработки пустой строки."""
    input_val, expected = case_empty
    assert mask_account_card(input_val) == expected


def test_non_digits(case_non_digits):
    """Проверка обработки строки с нецифровыми символами."""
    input_val, expected = case_non_digits
    assert mask_account_card(input_val) == expected


def test_whitespace(case_whitespace):
    """Проверка обработки строки, содержащей пробелы."""
    input_val, expected = case_whitespace
    assert mask_account_card(input_val) == expected


def test_none_raises_error(case_none):
    """Проверка выброса TypeError при передаче None."""
    with pytest.raises(TypeError):
        mask_account_card(case_none)


def test_standard(date_standard):
    """Проверка парсинга стандартной даты."""
    input_val, expected = date_standard
    assert get_date(input_val) == expected


def test_edge_start(date_edge_start):
    """Проверка парсинга начальной граничной даты."""
    input_val, expected = date_edge_start
    assert get_date(input_val) == expected


def test_edge_end(date_edge_end):
    """Проверка парсинга конечной граничной даты."""
    input_val, expected = date_edge_end
    assert get_date(input_val) == expected


def test_leap(date_leap):
    """Проверка парсинга даты в високосный год."""
    input_val, expected = date_leap
    assert get_date(input_val) == expected


def test_min_year(date_min):
    """Проверка парсинга даты с минимальным годом."""
    input_val, expected = date_min
    assert get_date(input_val) == expected


def test_max_year(date_max):
    """Проверка парсинга даты с максимальным годом."""
    input_val, expected = date_max
    assert get_date(input_val) == expected
