import re
from collections import Counter

def process_bank_search(datas:list[dict], search:str)->list[dict]:
    """Принимает список словарей, возвращает отфильтрованный список, где есть строка search"""
    pattern = re.compile(search, re.IGNORECASE)
    filter_lists = []
    for item in datas:
        if pattern.search(str(item['description'])):
            filter_lists.append(item)
    return filter_lists


def process_bank_operations(datas:list[dict], categories:list)->dict:
    """Принимает список словарей, и список категорий, возвращяет """
    counter = Counter({category: 0 for category in categories})

    for operation in datas:
        description = operation.get("description", "").lower()

        for category in categories:
            if category.lower() in description:
                counter[category] += 1

    return dict(counter)




























