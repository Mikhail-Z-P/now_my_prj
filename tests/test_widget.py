import pytest
import re
from widget import mask_account_card, get_date

def test_card_normal_16_digits():
    """Тест: стандартная карта 16 цифр — маскирует цыфры с 7 по 12."""
    assert mask_account_card("4000123456789012") == "4000 12** **** 9012"

def test_card_short_12_digits():
    """Тест: карта из 12 цифр """
    assert mask_account_card("123456789012") == ""

def test_card_only_digits():
    """Тест: только цифры — добавляется группировка."""
    assert mask_account_card("1111222233334444") == "1111 22** **** 4444"

def test_account_with_label_ru():
    """Тест: счёт с меткой «Счёт» — маскировка последних 6, первые 2 → *."""
    assert mask_account_card("Счёт 123456789") == "Счёт **6789"

def test_account_with_label_en():
    """Тест: счёт с меткой «Счет» (без ё) — аналогично."""
    assert mask_account_card("Счет 987654321") == "Счет **4321"

def test_account_short_5_digits():
    """Тест: счёт (с меткой) из 5 цифр — маскировка первых 2 из последних 5."""
    assert mask_account_card("Счёт 12345") == "Счёт **345"

def test_account_single_digit():
    """Тест: счёт с 1 цифрой — заменяется на *."""
    assert mask_account_card("Счёт 5") == "Счёт *"

def test_empty_string():
    """Тест: пустая строка — возвращает пустую."""
    assert mask_account_card("") == ""

def test_only_non_digits():
    """Тест: только нецифры — возвращает их без изменений."""
    assert mask_account_card("ABC-DEF") == ""

def test_whitespace_only():
    """Тест: только пробелы — возвращает пробелы."""
    assert mask_account_card("   ") == ""

@pytest.mark.parametrize("input_str,expected", [
    ("4000123456789012", "4000 12** **** 9012"),
    ("Счёт 123456", "Счёт **3456"),
    ("Счет 12", "Счет **"),
    ("Счёт 1", "Счёт *"),
    ("", ""),
    ("ABC", ""),
])
def test_parametrized_cases(input_str, expected):
    """Параметризованные тесты для компактной проверки."""
    assert mask_account_card(input_str) == expected

def test_type_error_if_none():
    """Тест: передача None вызывает TypeError"""
    with pytest.raises(TypeError):
        mask_account_card(None)




