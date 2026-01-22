import re

def mask_account_card(account_number: str) -> str:
    """
    Функция маскирует номер карты или счёта.
    - Для карт: скрывает цифры с 7-й по предпоследние 4, группирует по 4 символа.
    - Для счетов: оставляет последние 6 цифр, первые две заменяет на *.
    """
    score_resul = ""
    is_card = "Счёт" not in account_number and "Счет" not in account_number

    if is_card:
        for i in account_number:
            if not i.isdigit():
                score_resul += i

        count_four = 0
        account = 0
        card_number = ""

        digits = re.sub(r'\D', '', account_number)

        for card in digits:
            account += 1
            if account <= 6 or account > len(digits) - 4:
                card_number += card
            else:
                card_number += "*"
            count_four += 1
            if count_four % 4 == 0 and account != len(digits):
                card_number += " "
        score_resul += card_number
        return score_resul
    else:
        for i in account_number:
            if not i.isdigit():
                score_resul += i

        digits = re.sub(r'\D', '', account_number)

        account = 0
        number = ""
        reversed_number = digits[::-1]
        now_nomber = reversed_number[:6]

        for i in now_nomber[::-1]:
            account += 1
            if account <= 2:
                number += "*"
            else:
                number += i
        score_resul += number
    return score_resul
