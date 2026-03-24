import os
import requests

API_KEY = os.environ.get("EXCHANGE_RATES_API_KEY")
API_URL = "https://api.apilayer.com/exchangerates_data/convert"

def convert_to_rub(transaction: dict) -> float:
    """
    Конвертирует сумму транзакции в рубли через API.

    :param transaction: словарь с полями 'amount' (число) и 'currency' (строка)
    :return: сумма в рублях (float)
    """
    amount = transaction["amount"]
    currency = transaction["currency"].upper()

    if currency == "RUB":
        return float(amount)

    if currency not in ["USD", "EUR"]:
        raise ValueError(f"Неподдерживаемая валюта: {currency}")

    # Параметры запроса к API
    params = {
        "from": currency,
        "to": "RUB",
        "amount": amount
    }
    headers = {
        "apikey": API_KEY
    }

    response = requests.get(API_URL, headers=headers, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    return float(data["result"])
