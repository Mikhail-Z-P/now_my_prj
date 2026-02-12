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




def test_get_date_standard_format():
    """Тестирует преобразование стандартной даты (ISO формат)."""
    input_date = "2023-12-25T10:30:00"
    expected_output = "25.12.2023"
    assert get_date(input_date) == expected_output

def test_get_date_edge_cases():
    """Тестирует крайние случаи (например, начало и конец года)."""
    # Начало года
    input_date_start = "2023-01-01T00:00:00"
    expected_output_start = "01.01.2023"
    assert get_date(input_date_start) == expected_output_start

    # Конец года
    input_date_end = "2023-12-31T23:59:59"
    expected_output_end = "31.12.2023"
    assert get_date(input_date_end) == expected_output_end

def test_get_date_leap_year():
    """Тестирует работу с високосным годом."""
    input_date_leap = "2024-02-29T12:00:00"  # 29 февраля — существует только в високосном году
    expected_output_leap = "29.02.2024"
    assert get_date(input_date_leap) == expected_output_leap

def test_get_date_single_digit_days_and_months():
    """Тестирует обработку однозначных дней и месяцев (например, 01.01.2023)."""
    input_date = "2023-01-01T00:00:00"
    expected_output = "01.01.2023"
    assert get_date(input_date) == expected_output

def test_get_date_boundary_values():
    """Тестирует граничные значения (например, минимальные и максимальные годы)."""
    # Минимальный год (для примера)
    input_date_min = "1900-01-01T00:00:00"
    expected_output_min = "01.01.1900"
    assert get_date(input_date_min) == expected_output_min

    # Максимальный год (для примера)
    input_date_max = "9999-12-31T23:59:59"
    expected_output_max = "31.12.9999"
    assert get_date(input_date_max) == expected_output_max

def test_get_date_empty_string():
    """Проверяет обработку пустой строки."""
    with pytest.raises(ValueError):
        get_date("")

def test_get_date_whitespace_string():
    """Проверяет обработку строки, состоящей только из пробелов."""
    with pytest.raises(ValueError):
        get_date("   ")