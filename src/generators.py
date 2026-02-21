


def filter_by_currency(transactions: list[dict], currency: str) -> iter:
    """
    Генерирует транзакции из списка, у которых валюта операции
    совпадает с указанной.
    """
    for transaction in transactions:
        if transaction.get('operationAmount', {}).get('currency', {}).get('code') == currency:
            yield transaction

def transaction_descriptions(transactions: list[dict]) -> iter:
    """
    Генератор. Принимает список словарей с транзакциями и возвращает описание каждой операции по очереди.
    """
    if not transactions:
        return
    for transaction in transactions:
        yield transaction.get('description')

def card_number_generator(start , stop):
    """Генератор номеров карт формата XXXX XXXX XXXX XXXX в диапазоне start, stop"""
    for number in range(start, stop):
        card_str = str(number).zfill(16)

        formatted_card = f"{card_str[0:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:16]}"

        yield formatted_card 