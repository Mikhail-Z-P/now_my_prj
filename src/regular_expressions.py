import re

def process_bank_search(datas:list[dict], search:str)->list[dict]:
    """Принимает список словарей, возвращает отфильтрованный список, где есть строка search"""
    pattern = re.compile(search, re.IGNORECASE)
    filter_lists = []
    for item in datas:
        if pattern.search(str(item['description'])):
            filter_lists.append(item)
    return filter_lists


def process_bank_operations(datas:list[dict], categories:list)->dict:































datas = [
    {"name": "Sberbank", "city": "Moscow", "rating": 4.8},
    {"name": "VTB Bank", "city": "Saint Petersburg", "rating": 4.5},
    {"name": "Alfa-Bank", "city": "Moscow", "rating": 4.7},
    {"name": "Tinkoff", "city": "Online", "rating": 4.9}
]
filter_lists = process_bank_search(data, "bank")
print(filter_lists)