def get_mask_card_number(bank_card: str) -> str:
    """Функцыя разделяет по блокам четыре цыфры и скрывает цыфры идущие посло 6 и до 4 с конца"""

    count_four = 0
    account = 0
    card_number = ""

    for card in bank_card:
        account += 1
        if account <= 6 or account > 12:
            card_number += card
        elif 12 >= account >= 6:
            card = "*"
            card_number += card
        count_four += 1
        if count_four % 4 == 0 and card != len(bank_card) - 1:
            card_number += " "
    return card_number


def get_mask_account(account_number: str) -> str:
    account = 0
    number = ""

    for i in account_number:
        account += 1
        if account <= 2:
            i = "*"
            number += i
        elif account <= 6 or account > 12:
            number += i
    return number


print(get_mask_account("73654108430135874305"))
