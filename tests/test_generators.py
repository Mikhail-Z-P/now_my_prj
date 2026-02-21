import pytest
from generators import filter_by_currency


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