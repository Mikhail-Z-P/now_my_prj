import re
from collections import Counter

import pytest

from src.regular_expressions import process_bank_operations, process_bank_search


def process_bank_searchs(datas: list[dict], search: str) -> list[dict]:
    """Принимает список словарей, возвращает отфильтрованный список, где есть строка search"""
    pattern = re.compile(search, re.IGNORECASE)
    filter_lists = []
    for item in datas:
        if pattern.search(str(item["description"])):
            filter_lists.append(item)
    return filter_lists


@pytest.fixture
def sample_transactions():
    """
    Фикстура, предоставляющая тестовые данные для проверки функции process_bank_search.
    Возвращает список словарей с полями 'id' и 'description'.
    """
    return [
        {"id": 1, "description": "Оплата интернета"},
        {"id": 2, "description": "Перевод другу"},
        {"id": 3, "description": "Покупка в магазине"},
        {"id": 4, "description": "Оплата мобильной связи"},
        {"id": 5, "description": "Возврат средств"},
        {"id": 6, "description": "Снятие наличных"},
    ]


def test_process_bank_search_exact_match(sample_transactions):
    """
    Проверяет поиск точного совпадения слова "перевод".
    Ожидаемый результат: должна быть найдена 1 запись с id=2.
    """
    result = process_bank_search(sample_transactions, "перевод")
    assert len(result) == 1
    assert result[0]["id"] == 2


def test_process_bank_search_case_insensitive(sample_transactions):
    """
    Проверяет регистронезависимость поиска.
    Ожидаемый результат: должны быть найдены 2 записи с "оплата" независимо от регистра.
    """
    result_lower = process_bank_search(sample_transactions, "оплата")
    result_upper = process_bank_search(sample_transactions, "ОПЛАТА")

    assert len(result_lower) == 2
    assert len(result_upper) == 2
    assert [item["id"] for item in result_lower] == [item["id"] for item in result_upper]


def test_process_bank_search_nonexistent_term(sample_transactions):
    """
    Проверяет поиск несуществующего термина.
    Ожидаемый результат: пустой список.
    """
    result = process_bank_search(sample_transactions, "несуществующий_термин")
    assert result == [], "Должен вернуться пустой список для несуществующего термина"


def test_process_bank_search_empty_search_string(sample_transactions):
    """
    Проверяет поведение функции при пустой строке поиска.
    Ожидаемый результат: возвращаются все элементы списка.
    """
    result = process_bank_search(sample_transactions, "")
    assert len(result) == len(sample_transactions)
    assert [item["id"] for item in result] == [1, 2, 3, 4, 5, 6]


def test_process_bank_search_empty_list():
    """
    Проверяет работу функции с пустым списком данных.
    Ожидаемый результат: пустой список.
    """
    result = process_bank_search([], "любой_поиск")
    assert result == [], "Функция должна возвращать пустой список для пустого ввода"


def test_process_bank_search_missing_description_key():
    """
    Проверяет обработку случая, когда в словаре отсутствует ключ 'description'.
    Ожидаемый результат: исключение KeyError.
    """
    data = [{"id": 1, "name": "Без описания"}]
    with pytest.raises(KeyError):
        process_bank_search(data, "поиск")


def test_process_bank_search_regex_digits():
    """
    Проверяет работу с регулярными выражениями — поиск цифр в описании.
    Ожидаемый результат: найдены записи с цифрами в описании.
    """
    data = [
        {"id": 1, "description": "Сумма: 100$"},
        {"id": 2, "description": "Скидка: 50%"},
        {"id": 3, "description": "Заказ №123"},
        {"id": 4, "description": "Обычная транзакция"},
    ]
    result = process_bank_search(data, r"\d+")
    result_ids = [item["id"] for item in result]
    assert result_ids == [1, 2, 3], "Должны найти записи с цифрами в описании"


def test_process_bank_search_multiple_occurrences():
    """
    Проверяет случай, когда поисковая строка встречается несколько раз в одном описании.
    Ожидаемый результат: элемент должен быть включён в результат один раз.
    """
    data = [{"id": 1, "description": "Оплата интернета и оплата мобильной связи"}]
    result = process_bank_search(data, "оплата")
    assert len(result) == 1, "Элемент с несколькими совпадениями должен быть включён один раз"
    assert result[0]["id"] == 1


# Тест: большой набор данных
def test_process_bank_search_large_dataset():
    """
    Проверяет производительность функции на большом наборе данных.
    Ожидаемый результат: функция должна обработать данные без ошибок.
    """
    large_data = [{"id": i, "description": f"Транзакция {i} - пример описания"} for i in range(1, 301)]
    result = process_bank_search(large_data, "Транзакция")
    assert len(result) == 300, "Должны быть найдены все 300 транзакций"


def process_bank_operation(datas: list[dict], categories: list) -> dict:
    """Принимает список словарей и список категорий, возвращает словарь с количеством операций по каждой категории."""
    counter = Counter({category: 0 for category in categories})

    for operation in datas:
        description = operation.get("description", "").lower()

        for category in categories:
            if category.lower() in description:
                counter[category] += 1

    return dict(counter)


@pytest.fixture
def bank_operations():
    """Тестовые банковские операции с полем 'description'."""
    return [
        {"description": "Оплата интернета"},
        {"description": "Перевод другу"},
        {"description": "Покупка в магазине электроники"},
        {"description": "Оплата мобильной связи"},
        {"description": "Возврат средств"},
        {"description": "Снятие наличных в банкомате"},
        {"description": "Пополнение счёта"},
        {"description": "Покупка продуктов в супермаркете"},
    ]


def test_process_bank_operations_basic(bank_operations):
    """Базовый тест: поиск категорий 'интернет' и 'покупка'."""
    categories = ["интернет", "покупка"]
    result = process_bank_operations(bank_operations, categories)
    assert result == {"интернет": 1, "покупка": 2}


def test_process_bank_operations_empty_data():
    """Тест с пустым списком данных — должны быть нули для всех категорий."""
    categories = ["интернет", "покупка"]
    result = process_bank_operations([], categories)
    assert result == {"интернет": 0, "покупка": 0}


def test_process_bank_operations_case_insensitivity(bank_operations):
    """Проверка регистронезависимости поиска."""
    categories = ["ПОКУПКА", "ИНТЕРНЕТ"]
    result = process_bank_operations(bank_operations, categories)
    assert result == {"ПОКУПКА": 2, "ИНТЕРНЕТ": 1}


def test_process_bank_operations_nonexistent_category(bank_operations):
    """Поиск несуществующей категории — должен вернуть 0."""
    categories = ["не_существует"]
    result = process_bank_operations(bank_operations, categories)
    assert result == {"не_существует": 0}


def test_process_bank_operations_missing_description():
    """Обработка операций без поля 'description' — пропускаются без ошибки."""
    data = [
        {"description": "Оплата интернета"},
        {"amount": 1000},
        {"description": "Покупка продуктов"},
    ]
    categories = ["интернет", "покупка"]
    result = process_bank_operations(data, categories)
    assert result == {"интернет": 1, "покупка": 1}


def test_process_bank_operations_empty_categories(bank_operations):
    """Пустой список категорий — должен вернуть пустой словарь."""
    result = process_bank_operations(bank_operations, [])
    assert result == {}


def test_process_bank_operations_large_dataset():
    """Производительность на большом наборе данных."""
    large_data = [
        (
            {"description": f"Транзакция {i} - покупка товара"}
            if i % 2 == 0
            else {"description": f"Транзакция {i} - перевод"}
        )
        for i in range(1, 201)
    ]
    categories = ["покупка", "перевод"]
    result = process_bank_operations(large_data, categories)
    assert result["покупка"] == 100
    assert result["перевод"] == 100
