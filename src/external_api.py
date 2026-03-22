import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("EXCHANGE_RATES_API_KEY")
API_URL = "https://api.exchangerate-api.com/v4/latest/RUB"


def get_exchange_rate(currency: str) -> float:
    """
    Получает текущий курс валюты относительно рубля.
    :param currency: Код валюты (например, 'USD', 'EUR')
    :return: Курс валюты в рублях (float)
    """
    try:
        response = requests.get(API_URL, params={"access_key": API_KEY})
        response.raise_for_status()
        data = response.json()
        return data["rates"][currency]
    except (requests.RequestException, KeyError) as e:
        print(f"Ошибка при получении курса валюты {currency}: {e}")
        return 1.0
