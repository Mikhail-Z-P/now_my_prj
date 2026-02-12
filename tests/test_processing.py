import pytest
from src.processing import filter_by_state, sort_by_date

def test_filter_by_state_default():
    transactions = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "PENDING"},
        {"id": 3, "state": "EXECUTED"}
    ]
    result = filter_by_state(transactions)
    expected = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 3, "state": "EXECUTED"}
    ]
    assert result == expected

def test_filter_by_state_custom():
    transactions = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "PENDING"},
        {"id": 3, "state": "FAILED"}
    ]
    result = filter_by_state(transactions, state="PENDING")
    expected = [{"id": 2, "state": "PENDING"}]
    assert result == expected


def test_filter_by_state_empty_list():
    result = filter_by_state([])
    assert result == []


def test_filter_by_state_no_matches():
    transactions = [
        {"id": 1, "state": "PENDING"},
        {"id": 2, "state": "FAILED"}
    ]
    result = filter_by_state(transactions, state="EXECUTED")
    assert result == []

def test_filter_by_state_missing_key():
    transactions = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "status": "PENDING"},
        {"id": 3, "state": "EXECUTED"}
    ]
    result = filter_by_state(transactions)
    expected = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 3, "state": "EXECUTED"}
    ]
    assert result == expected

def test_filter_by_state_all_matches():
    transactions = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2, "state": "EXECUTED"},
        {"id": 3, "state": "EXECUTED"}
    ]
    result = filter_by_state(transactions)
    assert result == transactions

def test_filter_by_state_case_sensitive():
    transactions = [
        {"id": 1, "state": "executed"},
        {"id": 2, "state": "EXECUTED"},
        {"id": 3, "state": "Executed"}
    ]
    result = filter_by_state(transactions, state="EXECUTED")
    expected = [{"id": 2, "state": "EXECUTED"}]
    assert result == expected

def test_filter_by_state_non_string_state():
    transactions = [
        {"id": 1, "state": 1},
        {"id": 2, "state": 2}
    ]
    result = filter_by_state(transactions, state=1)
    expected = [{"id": 1, "state": 1}]
    assert result == expected




def test_sort_by_date_ascending():
    """Тест: сортировка по возрастанию даты (sorting=True)."""
    transactions = [
        {"id": 1, "date": "2023-01-15"},
        {"id": 2, "date": "2022-12-01"},
        {"id": 3, "date": "2023-03-10"}
    ]
    result = sort_by_date(transactions, sorting=True)
    expected = [
        {"id": 2, "date": "2022-12-01"},
        {"id": 1, "date": "2023-01-15"},
        {"id": 3, "date": "2023-03-10"}
    ]
    assert result == expected

def test_sort_by_date_descending():
    """Тест: сортировка по убыванию даты (sorting=False)."""
    transactions = [
        {"id": 1, "date": "2023-01-15"},
        {"id": 2, "date": "2022-12-01"},
        {"id": 3, "date": "2023-03-10"}
    ]
    result = sort_by_date(transactions, sorting=False)
    expected = [
        {"id": 3, "date": "2023-03-10"},
        {"id": 1, "date": "2023-01-15"},
        {"id": 2, "date": "2022-12-01"}
    ]
    assert result == expected

def test_sort_by_date_empty_list():
    """Тест: пустой список."""
    result = sort_by_date([])
    assert result == []

def test_sort_by_date_single_element():
    """Тест: список из одного элемента."""
    transactions = [{"id": 1, "date": "2023-01-01"}]
    result = sort_by_date(transactions)
    assert result == transactions

def test_sort_by_date_missing_date_key():
    """Тест: словари без ключа 'date' (должны быть пропущены или вызвать ошибку?)."""
    # Вариант 1: пропускаем словари без 'date'
    transactions = [
        {"id": 1, "date": "2023-01-15"},
        {"id": 2, "amount": 100},  # нет 'date'
        {"id": 3, "date": "2022-12-01"}
    ]
    result = sort_by_date(transactions, sorting=True)
    # Ожидаем, что словари без 'date' исключены
    expected = [
        {"id": 3, "date": "2022-12-01"},
        {"id": 1, "date": "2023-01-15"}
    ]
    assert result == expected

def test_sort_by_date_same_dates():
    """Тест: несколько элементов с одинаковой датой."""
    transactions = [
        {"id": 1, "date": "2023-01-15"},
        {"id": 2, "date": "2023-01-15"},
        {"id": 3, "date": "2022-12-01"}
    ]
    result = sort_by_date(transactions, sorting=True)
    expected = [
        {"id": 3, "date": "2022-12-01"},
        {"id": 1, "date": "2023-01-15"},
        {"id": 2, "date": "2023-01-15"}
    ]
    assert result == expected

def test_sort_by_date_iso_format():
    """Тест: даты в ISO-формате (с временем)."""
    transactions = [
        {"id": 1, "date": "2023-01-15T10:30:00"},
        {"id": 2, "date": "2022-12-01T08:15:00"},
        {"id": 3, "date": "2023-03-10T14:45:00"}
    ]
    result = sort_by_date(transactions, sorting=True)
    expected = [
        {"id": 2, "date": "2022-12-01T08:15:00"},
        {"id": 1, "date": "2023-01-15T10:30:00"},
        {"id": 3, "date": "2023-03-10T14:45:00"}
    ]
    assert result == expected

def test_sort_by_date_original_list_unchanged():
    """Тест: исходный список не изменяется."""
    original_transactions = [
        {"id": 1, "date": "2023-01-15"},
        {"id": 2, "date": "2022-12-01"}
    ]
    sort_by_date(original_transactions, sorting=True)
    assert original_transactions == [
        {"id": 1, "date": "2023-01-15"},
        {"id": 2, "date": "2022-12-01"}
    ]

def test_sort_by_date_non_string_dates():
    """Тест: даты не в строковом формате (например, timestamp)."""
    transactions = [
        {"id": 1, "date": 1673769600},  # Unix timestamp
        {"id": 2, "date": 1669852800},
        {"id": 3, "date": 1681075200}
    ]
    result = sort_by_date(transactions, sorting=True)
    expected = [
        {"id": 2, "date": 1669852800},
        {"id": 1, "date": 1673769600},
        {"id": 3, "date": 1681075200}
    ]
    assert result == expected

def test_sort_by_date_mixed_date_formats():
    """Тест: смешанные форматы дат (строка и число)."""
    transactions = [
        {"id": 1, "date": "2023-01-15"},
        {"id": 2, "date": 1669852800},
        {"id": 3, "date": "2022-12-01"}
    ]
    # Ожидается: сортировка возможна только если все даты одного типа
    # В текущей реализации это вызовет ошибку TypeError
    with pytest.raises(TypeError):
        sort_by_date(transactions, sorting=True)