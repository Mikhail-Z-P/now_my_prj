
import pytest

@pytest.fixture
def standard_16_digit_cases():
    """Фикстура для теста стандартного 16-значного номера."""
    return [
        {
            "input": "7000792289606361",
            "expected": "7000 79** **** 6361"
        }
    ]

@pytest.fixture
def card_with_spaces_and_dashes_cases():
    """Фикстура для теста номеров с пробелами и дефисами."""
    return [
        {
            "input": "7000 7922-8960-6361",
            "expected": "7000 79** **** 6361"
        },
        {
            "input": "7000-7922 8960 6361",
            "expected": "7000 79** **** 6361"
        }
    ]

@pytest.fixture
def short_card_number_cases():
    """Фикстура для теста коротких номеров (менее 6 цифр)."""
    return [
        {
            "input": "12345",
            "expected": ""
        }
    ]

@pytest.fixture
def long_card_number_cases():
    """Фикстура для теста длинных номеров (более 16 цифр)."""
    return [
        {
            "input": "12345678901234567890",
            "expected": ""
        }
    ]

@pytest.fixture
def empty_string_cases():
    """Фикстура для теста пустой строки."""
    return [
        {
            "input": "",
            "expected": ""
        }
    ]

@pytest.fixture
def whitespace_string_cases():
    """Фикстура для теста строки из пробелов."""
    return [
        {
            "input": "   ",
            "expected": ""
        }
    ]

@pytest.fixture
def no_digits_string_cases():
    """Фикстура для теста строк без цифр."""
    return [
        {
            "input": "abcdefghijklmnop",
            "expected": ""
        },
        {
            "input": "!@#$%^&*()",
            "expected": ""
        }
    ]

@pytest.fixture
def letters_and_digits_cases():
    """Фикстура для теста строк с буквами и цифрами."""
    return [
        {
            "input": "Card1234 5678 90AB 1234",
            "expected": ""
        }
    ]

@pytest.fixture
def special_characters_cases():
    """Фикстура для теста строк со спецсимволами."""
    return [
        {
            "input": "1234\t5678\n9012\3456",
            "expected": ""
        }
    ]

@pytest.fixture
def mask_account_test_cases():
    """Фикстура для тестов маскировки аккаунта. Возвращает список словарей с тестовыми кейсами."""
    return [
        {
            "input": "123456",
            "expected": "**3456",
            "description": "Ровно 6 символов — маскируем первые 2, оставляем последние 4."
        },
        {
            "input": "12345678",
            "expected": "**5678",
            "description": "8 символов — берём последние 6, маскируем первые 2 из них."
        },
        {
            "input": "1234567890",
            "expected": "**7890",
            "description": "10 символов — берём последние 6, маскируем первые 2 из них."
        },
        {
            "input": "12345",
            "expected": "**345",
            "description": "5 символов — маскируем первые 2 из последних 5."
        },
        {
            "input": "1234",
            "expected": "**34",
            "description": "4 символа — маскируем первые 2, оставляем 2."
        },
        {
            "input": "123",
            "expected": "**3",
            "description": "3 символа — маскируем первые 2, остаётся 1."
        },
        {
            "input": "12",
            "expected": "**",
            "description": "2 символа — заменяем оба на '*'."
        },
        {
            "input": "1",
            "expected": "*",
            "description": "1 символ — заменяем его на '*' (т.к. меньше 2)."
        },
        {
            "input": "",
            "expected": "",
            "description": "Пустая строка — возвращаем пустую строку."
        }
    ]


@pytest.fixture
def case_16_digit_card():
    return "4000123456789012", "4000 12** **** 9012"

@pytest.fixture
def case_12_digit_card():
    return "123456789012", ""

@pytest.fixture
def case_only_digits():
    return "1111222233334444", "1111 22** **** 4444"

@pytest.fixture
def case_account_ru():
    return "Счёт 123456789", "Счёт **6789"

@pytest.fixture
def case_account_en():
    return "Счет 987654321", "Счет **4321"

@pytest.fixture
def case_short_account():
    return "Счёт 12345", "Счёт **345"

@pytest.fixture
def case_single_digit():
    return "Счёт 5", "Счёт *"

@pytest.fixture
def case_empty():
    return "", ""

@pytest.fixture
def case_non_digits():
    return "ABC-DEF", ""

@pytest.fixture
def case_whitespace():
    return "   ", ""

@pytest.fixture
def case_none():
    return None

import pytest

@pytest.fixture
def date_standard():
    return "2023-12-25T10:30:00", "25.12.2023"

@pytest.fixture
def date_edge_start():
    return "2023-01-01T00:00:00", "01.01.2023"

@pytest.fixture
def date_edge_end():
    return "2023-12-31T23:59:59", "31.12.2023"

@pytest.fixture
def date_leap():
    return "2024-02-29T12:00:00", "29.02.2024"

@pytest.fixture
def date_single_digit():
    return "2023-01-01T00:00:00", "01.01.2023"


@pytest.fixture
def date_min():
    return "1900-01-01T00:00:00", "01.01.1900"

@pytest.fixture
def date_max():
    return "9999-12-31T23:59:59", "31.12.9999"


@pytest.fixture
def empty_str():
    return ""

@pytest.fixture
def whitespace_str():
    return "   "
