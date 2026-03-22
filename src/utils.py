import json
import os


def load_transactions(json_path):
    """Загружает список словарей с транзакциями из JSON-файла."""
    try:
        if not os.path.exists(json_path):
            return []

        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return data if isinstance(data, list) else []

    except (json.JSONDecodeError, IOError):
        return []

