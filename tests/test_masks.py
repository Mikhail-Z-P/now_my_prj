from src.masks import get_mask_account, get_mask_card_number
import pytest

@pytest.mark.parametrize(
    "input, expected, desc",
    [
        ("7000792289606361", "7000 79** **** 6361", "16 цифр"),
        ("7000 7922-8960-6361", "7000 79** **** 6361", "с пробелами/дефисами"),
        ("12345", "", "короче 6 цифр"),
        ("12345678901234567890", "", "длиннее 16 цифр"),
    ]
)
def test_mask_card(input, expected, desc):
    result = get_mask_card_number(input)
    assert result == expected, f"{desc}: got '{result}', expected '{expected}'"

# def test_standard_16_digits(standard_16_digit_cases):
#     """Тестируем стандартный 16-значный номер карты."""
#     for case in standard_16_digit_cases:
#         result = get_mask_card_number(case["input"])
#         assert result == case["expected"]
#
#
# def test_card_with_spaces_and_dashes(card_with_spaces_and_dashes_cases):
#     """Тестируем номер с пробелами и дефисами — должны игнорироваться."""
#     for case in card_with_spaces_and_dashes_cases:
#         result = get_mask_card_number(case["input"])
#         assert result == case["expected"]
#
#
# def test_short_card_number(short_card_number_cases):
#     """Тестируем слишком короткий номер (менее 6 цифр)."""
#     for case in short_card_number_cases:
#         result = get_mask_card_number(case["input"])
#         assert result == case["expected"]
#
#
# def test_long_card_number(long_card_number_cases):
#     """Тестируем номер длиннее 16 цифр."""
#     for case in long_card_number_cases:
#         result = get_mask_card_number(case["input"])
#         assert result == case["expected"]


def test_empty_string(empty_string_cases):
    """Тестируем пустую строку."""
    for case in empty_string_cases:
        result = get_mask_card_number(case["input"])
        assert result == case["expected"]


def test_whitespace_string(whitespace_string_cases):
    """Тестируем строку, состоящую только из пробелов."""
    for case in whitespace_string_cases:
        result = get_mask_card_number(case["input"])
        assert result == case["expected"]


def test_string_with_no_digits(no_digits_string_cases):
    """Тестируем строку без цифр (только буквы и спецсимволы)."""
    for case in no_digits_string_cases:
        result = get_mask_card_number(case["input"])
        assert result == case["expected"]


def test_string_with_letters_and_digits(letters_and_digits_cases):
    """Тестируем строку с комбинацией цифр и букв."""
    for case in letters_and_digits_cases:
        result = get_mask_card_number(case["input"])
        assert result == case["expected"]


def test_special_characters(special_characters_cases):
    """Тестируем обработку специальных символов (табуляция, перевод строки)."""
    for case in special_characters_cases:
        result = get_mask_card_number(case["input"])
        assert result == case["expected"]


def test_get_mask_account(mask_account_test_cases):
    """Тестируем функцию get_mask_account для всех кейсов."""
    for case in mask_account_test_cases:
        result = get_mask_account(case["input"])
        assert (
            result == case["expected"]
        ), f"Failed for input '{case['input']}': expected '{case['expected']}', got '{result}'"
        print(f"Passed: {case['description']}")
