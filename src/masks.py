import re
import logging
import os

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
logs_dir = os.path.join(root_dir, 'logs')

if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

masks_logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('../logs/masks.log', encoding="utf-8")
file_formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
masks_logger.addHandler(file_handler)
masks_logger.setLevel(logging.INFO)


def get_mask_card_number(bank_card: str) -> str:
    """Функцыя разделяет каждые четыре цыфры по блокам и скрывает цыфры идущие посло 6 и до 4 с конца"""

    masks_logger.debug(f"Начало обработки номера карты: {bank_card}")

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
    if account != 16:
        masks_logger.warning(f"Длина номера не равна 16 цифрам: {account}. Возвращаем пустую строку.")
        return ""
    else:
        masks_logger.info(f"Обработка завершена успешно. Замаскированный номер: {card_number}")
        return str(card_number)


def get_mask_account(account_number: str) -> str:
    """Функцыя оставляет последнии шесть цыфр счета, первые две изменены на звездочки"""

    masks_logger.debug(f"Начало обработки. Переданный номер счёта: '{account_number}'")

    last_six = account_number[-6:] if account_number else ""
    masked = "**" + last_six[2:] if len(last_six) > 2 else "*" * min(2, len(last_six)) + last_six[2:]

    masks_logger.info(f"Обработка завершена. Возвращаемое значение: '{masked}'")
    return masked
