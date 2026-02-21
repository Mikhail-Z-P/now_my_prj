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


def test_basic_functionality(valid_range):
    """Проверка базовой работы генератора"""
    start, stop = valid_range
    gen = card_number_generator(start, stop)
    results = list(gen)
    assert len(results) == stop - start
    assert results[0] == "1234 5678 9012 3450"
    assert results[-1] == "1234 5678 9012 3454"

def test_single_number(single_number_range):
    """Проверка генерации одного номера"""
    start, stop = single_number_range
    gen = card_number_generator(start, stop)
    result = list(gen)
    assert result == ["1111 1111 1111 1111"]

def test_zero_start(zero_start_range):
    """Проверка генерации с нулевого значения"""
    start, stop = zero_start_range
    gen = card_number_generator(start, stop)
    results = list(gen)
    assert results == [
        "0000 0000 0000 0000",
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
        "0000 0000 0000 0006",
        "0000 0000 0000 0007",
        "0000 0000 0000 0008",
        "0000 0000 0000 0009"
    ]

@pytest.mark.parametrize("start,stop,expected_count", [
    pytest.param(1234, 1237, 3, id="малый диапазон"),
    pytest.param(9999999999999990, 9999999999999999, 9, id="большой диапазон"),
    pytest.param(0, 1, 1, id="один элемент"),
    pytest.param(1000000000000000, 1000000000000005, 5, id="средний диапазон")
])
def test_parametrized(start, stop, expected_count):
    """Параметризованные тесты"""
    gen = card_number_generator(start, stop)
    results = list(gen)
    assert len(results) == expected_count
    assert all(len(num.replace(" ", "")) == 16 for num in results)
    assert all(len(num.split()) == 4 for num in results)