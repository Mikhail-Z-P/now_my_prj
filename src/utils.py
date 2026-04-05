import json
import os
import logging

from src.external_api import convert_to_rub


def load_transactions(json_path):
    """Загружает список словарей с транзакциями из JSON-файла."""
    try:
        if not os.path.exists(json_path):
            return []

        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data if isinstance(data, list) else []

    except (json.JSONDecodeError, FileNotFoundError, IOError):
        return []


def process_transaction(transaction: dict) -> float:
    """
    Преобразует сумму транзакции в рубли.
    :param transaction: Словарь с ключами 'amount' и 'currency'
    :return: Сумма в рублях (float)
    :raises ValueError: Если валюта не поддерживается или данные некорректны
    """
    if "operationAmount" not in transaction:
        raise ValueError("Транзакция должна содержать поле 'operationAmount'")

    operation_amount = transaction["operationAmount"]

    if "amount" not in operation_amount:
        raise ValueError("Транзакция должна содержать поле 'amount' в operationAmount")
    if "currency" not in operation_amount:
        raise ValueError("Транзакция должна содержать поле 'currency' в operationAmount")

    amount_str = operation_amount["amount"]
    currency_info = operation_amount["currency"]

    if "code" not in currency_info:
        raise ValueError("Поле 'currency' должно содержать ключ 'code'")

    currency_code = currency_info["code"]

    if not isinstance(amount_str, (int, float)):
        try:
            amount = float(amount_str)
        except (ValueError, TypeError):
            raise ValueError(f"Сумма должна быть числом, получено: {type(amount_str)}")
    else:
        amount = amount_str

    currency = currency_code.upper()

    simple_transaction = {"amount": amount, "currency": currency}
    return convert_to_rub(simple_transaction)
