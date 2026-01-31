def filter_by_state(list_dictionary: list, state: str = "EXECUTED") -> list:
    """Функция принимает список словарей и возвращает только соответствующие ключу stat"""

    now_list_dictionary = []

    for dictionary in list_dictionary:
        if dictionary["state"] == state:
            now_list_dictionary.append(dictionary)
    return now_list_dictionary


def sort_by_date(list_dictionary: list, sorting: bool = True) -> list:
    """Функция сортирует список словарей по ключу date"""

    sorted_list = sorted(list_dictionary, key=lambda x: x["date"], reverse=sorting)
    return sorted_list
