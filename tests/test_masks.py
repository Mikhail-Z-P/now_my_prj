import pytest
from src.masks import get_mask_card_number, get_mask_account

def test_standard_16_digits():
    """Тестируем стандартный 16-значный номер карты."""
    result = get_mask_card_number("7000792289606361")
    assert result == "7000 79** **** 6361"

def test_card_with_spaces_and_dashes():
    """Тестируем номер с пробелами и дефисами — должны игнорироваться."""
    result1 = get_mask_card_number("7000 7922-8960-6361")
    result2 = get_mask_card_number("7000-7922 8960 6361")
    assert result1 == "7000 79** **** 6361"
    assert result2 == "7000 79** **** 6361"

def test_short_card_number():
    """Тестируем слишком короткий номер (менее 6 цифр)."""
    result = get_mask_card_number("12345")
    assert result == ""

def test_long_card_number():
    """Тестируем номер длиннее 16 цифр."""
    result = get_mask_card_number("12345678901234567890")
    assert result == ""

def test_empty_string():
    """Тестируем пустую строку."""
    result = get_mask_card_number("")
    assert result == ""

def test_whitespace_string():
    """Тестируем строку, состоящую только из пробелов."""
    result = get_mask_card_number("   ")
    assert result == ""

def test_string_with_no_digits():
    """Тестируем строку без цифр (только буквы и спецсимволы)."""
    result1 = get_mask_card_number("abcdefghijklmnop")
    result2 = get_mask_card_number("!@#$%^&*()")
    assert result1 == ""
    assert result2 == ""

def test_string_with_letters_and_digits():
    """Тестируем строку с комбинацией цифр и букв."""
    result = get_mask_card_number("Card1234 5678 90AB 1234")
    assert result == ""

def test_special_characters():
    """Тестируем обработку специальных символов (табуляция, перевод строки)."""
    result = get_mask_card_number("1234\t5678\n9012\3456")
    assert result == ""




