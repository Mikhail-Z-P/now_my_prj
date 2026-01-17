def get_mask_card_number(bank_card: str) -> str:
    """Функцыя разделяет каждые четыре цыфры по блокам  и скрывает цыфры идущие посло 6 и до 4 с конца"""

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

    return str(card_number)


def get_mask_account(account_number: str) -> str:
    """Функцыя оставляет последнии шесть цыфр счета, первые две изменены на звездочки"""

    account = 0
    number = ""
    reversed_number = account_number[::-1]
    now_nomber = reversed_number[:6]

    for i in now_nomber[::-1]:
        account += 1
        if 6 >= account >= 3:
            number += i
        elif account <= 2:
            i = "*"
            number += i
    return str(number)
