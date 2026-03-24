import json
import os

from src.external_api import convert_to_rub


def load_transactions(json_path):
    """Загружает список словарей с транзакциями из JSON-файла."""
    try:
        if not os.path.exists(json_path):
            return []

        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data if isinstance(data, list) else []

    except (json.JSONDecodeError, IOError):
        return []


def process_transaction(transaction: dict) -> float:
    """
    Преобразует сумму транзакции в рубли.
    :param transaction: Словарь с ключами 'amount' и 'currency'
    :return: Сумма в рублях (float)
    :raises ValueError: Если валюта не поддерживается или данные некорректны
    """
    if "amount" not in transaction or "currency" not in transaction:
        raise ValueError("Транзакция должна содержать поля 'amount' и 'currency'")

        # Проверка типа суммы
    if not isinstance(transaction["amount"], (int, float)):
        raise ValueError(f"Сумма должна быть числом, получено: {type(transaction['amount'])}")

        # Конвертация через API
    return convert_to_rub(transaction)
