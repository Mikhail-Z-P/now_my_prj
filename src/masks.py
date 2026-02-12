import re


def get_mask_card_number(bank_card: str) -> str:
    """Функцыя разделяет каждые четыре цыфры по блокам и скрывает цыфры идущие посло 6 и до 4 с конца"""

    count_four = 0
    account = 0
    card_number = ""

    digits = re.sub(r"\D", "", bank_card)

    for card in digits:
        account += 1
        if account <= 6 or account > len(digits) - 4:
            card_number += card
        else:
            card_number += "*"
        count_four += 1
        if count_four % 4 == 0 and account != len(digits):
            card_number += " "
    if account < 16 or account > 16:
        return ""
    else:
        return str(card_number)


def get_mask_account(account_number: str) -> str:
    """Функцыя оставляет последнии шесть цыфр счета, первые две изменены на звездочки"""

    last_six = account_number[-6:] if account_number else ""
    masked = "**" + last_six[2:] if len(last_six) > 2 else "*" * min(2, len(last_six)) + last_six[2:]
    return masked
