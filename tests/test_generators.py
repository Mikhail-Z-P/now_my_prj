import pytest
from generators import filter_by_currency, transaction_descriptions, card_number_generator



@pytest.mark.parametrize("currency,expected_ids", [
    ("USD", [1, 3]),
    ("EUR", [2]),
    ("RUB", []),
])


def test_filter_by_currency_parametrized(sample_transactions, currency, expected_ids):
    """Тест фильтрации с разными валютами через параметризацию."""
    result = list(filter_by_currency(sample_transactions, currency))
    result_ids = [t["id"] for t in result]
    assert result_ids == expected_ids


def test_empty_transactions(empty_transactions):
    """Тест с пустым списком транзакций."""
    result = list(filter_by_currency(empty_transactions, "USD"))
    assert result == []


def test_transaction_without_currency_field(sample_transactions):
    """Тест транзакции без поля currency."""
    # Транзакция с id=4 не имеет поля currency — не должна попасть в результат для любой валюты
    result = list(filter_by_currency(sample_transactions, "USD"))
    result_ids = [t["id"] for t in result]
    assert 4 not in result_ids


def test_missing_operation_amount():
    """Тест транзакции без operationAmount."""
    transactions = [{"id": 1}]  # нет operationAmount
    result = list(filter_by_currency(transactions, "USD"))
    assert result == []


def test_basic_functionality(transactions_with_descriptions):
    """Проверка базовой работы генератора"""
    gen = transaction_descriptions(transactions_with_descriptions)
    results = list(gen)
    assert results == [
        "Перевод организации",
        "Снятие наличных",
        "Пополнение счета"
    ]

def test_missing_descriptions(transactions_without_descriptions):
    """Проверка транзакций без описаний"""
    gen = transaction_descriptions(transactions_without_descriptions)
    results = list(gen)
    assert results == [None, None, None]

def test_empty_transactions(empty_transactions):
    """Проверка пустого списка"""
    gen = transaction_descriptions(empty_transactions)
    assert list(gen) == []

@pytest.mark.parametrize("transactions,expected", [
    pytest.param(
        [{"description": "Оплата услуг"}],
        ["Оплата услуг"],
        id="один элемент"
    ),
    pytest.param(
        [{"description": "Покупка"}, {"description": "Продажа"}],
        ["Покупка", "Продажа"],
        id="несколько элементов"
    ),
    pytest.param(
        [],
        [],
        id="пустой список"
    )
])
def test_parametrized(transactions, expected):
    """Параметризованные тесты"""
    gen = transaction_descriptions(transactions)
    assert list(gen) == expected


