def filter_by_state(list_dictionary, state="EXECUTED") -> list:
    """Функцыя принимает список словарей и возвращяет только соответствующие ключу stat"""

    now_list_dictionary = []

    for dictionary in list_dictionary:
        if dictionary["state"] == state:
            now_list_dictionary.append(dictionary)
    return now_list_dictionary








