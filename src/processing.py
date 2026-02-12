def filter_by_state(list_dictionary: list, state: str = "EXECUTED") -> list:
    """Функция принимает список словарей и возвращает только соответствующие ключу stat"""

    filtered_transactions = []

    for dictionary in list_dictionary:
        if "state" in dictionary and dictionary["state"] == state:
            filtered_transactions .append(dictionary)
    return filtered_transactions


def sort_by_date(list_dictionary: list, sorting: bool = True) -> list:
    """Функция сортирует список словарей по ключу date"""

    filtered = [
        item for item in list_dictionary
        if "date" in item and item["date"] is not None
    ]
    return sorted(filtered, key=lambda x: x["date"], reverse=not sorting)


