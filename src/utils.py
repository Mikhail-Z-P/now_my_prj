import json
import logging
import os

from src.external_api import convert_to_rub

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
logs_dir = os.path.join(root_dir, "logs")

if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

utils_logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("../logs/utils.log", mode="w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)

utils_logger.addHandler(file_handler)
utils_logger.setLevel(logging.DEBUG)


def load_transactions(json_path):
    """Загружает список словарей с транзакциями из JSON-файла."""
    utils_logger.debug(f"Начало работы: загрузка файла {json_path}")
    try:
        if not os.path.exists(json_path):
            utils_logger.error(f"Файл не найден: {json_path}")
            return []

        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        utils_logger.error(f"Данные загружены, проверка типа: {isinstance(data, list)}")
        return data if isinstance(data, list) else []

    except (json.JSONDecodeError, FileNotFoundError, IOError) as e:
        utils_logger.error(f"Произошла ошибка при загрузке файла {json_path}: {str(e)}")
        return []


def process_transaction(transaction: dict) -> float:
    """
    Преобразует сумму транзакции в рубли.
    :param transaction: Словарь с ключами 'amount' и 'currency'
    :return: Сумма в рублях (float)
    :raises ValueError: Если валюта не поддерживается или данные некорректны
    """
    utils_logger.debug(f"Начало обработки транзакции: {transaction}")

    if "operationAmount" not in transaction:
        utils_logger.error("В транзакции отсутствует ключ 'operationAmount'")
        raise ValueError("Транзакция должна содержать поле 'operationAmount'")

    operation_amount = transaction["operationAmount"]

    if "amount" not in operation_amount:
        utils_logger.error("В operationAmount отсутствует ключ 'amount'")
        raise ValueError("Транзакция должна содержать поле 'amount' в operationAmount")
    if "currency" not in operation_amount:
        utils_logger.error("В operationAmount отсутствует ключ 'currency'")
        raise ValueError("Транзакция должна содержать поле 'currency' в operationAmount")

    amount_str = operation_amount["amount"]
    currency_info = operation_amount["currency"]

    if "code" not in currency_info:
        utils_logger.error("В currency_info отсутствует код валюты")
        raise ValueError("Поле 'currency' должно содержать ключ 'code'")

    currency_code = currency_info["code"]

    if not isinstance(amount_str, (int, float)):
        try:
            amount = float(amount_str)
        except (ValueError, TypeError):
            utils_logger.error(f"Не удалось преобразовать сумму {amount_str} в число")
            raise ValueError(f"Сумма должна быть числом, получено: {type(amount_str)}")
    else:
        amount = amount_str

    currency = currency_code.upper()

    simple_transaction = {"amount": amount, "currency": currency}
    utils_logger.info(f"Подготовлен объект для конвертации: {simple_transaction}")
    return convert_to_rub(simple_transaction)
