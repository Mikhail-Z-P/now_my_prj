import json
import os

from src.external_api import get_exchange_rate


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
    amount = transaction.get("amount")
    currency = transaction.get("currency", "").upper()

    if not amount or not currency:
        raise ValueError("Транзакция должна содержать 'amount' и 'currency'")
    if not isinstance(amount, (int, float)):
        raise ValueError(f"Сумма должна быть числом, получено: {type(amount)}")

    if currency == "RUB":
        return float(amount)
    elif currency in ["USD", "EUR"]:
        rate = get_exchange_rate(currency)
        return float(amount) * rate
    else:
        raise ValueError(f"Неподдерживаемая валюта: {currency}")
