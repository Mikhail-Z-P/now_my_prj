import csv
import pandas as pd
import json

from dotenv import load_dotenv
from tables_pandas import reading_csv
from src.decorators import log
from src.external_api import convert_to_rub
from src.generators import card_number_generator, filter_by_currency, transaction_descriptions
from src.masks import get_mask_account, get_mask_card_number
from src.processing import filter_by_state, sort_by_date
from src.utils import load_transactions, process_transaction
from src.widget import get_date, mask_account_card
from regular_expressions import process_bank_search, process_bank_operations
load_dotenv()


def start_processing():
    """Основная функция для обработки банковских транзакций."""

    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями")
    print("Выберите необходимый пункт меню:")
    print("""
1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла
""")

    while True:
        number = input("Введите число: ").strip()

        valid_number = {"1", "2", "3"}

        if number in valid_number:
            file_path = ""
            data = None
            try:
                if number == "1":
                    print("Для обработки выбран JSON-файл.")
                    file_path = input("Введите путь к JSON-файлу: ").strip()
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)

                elif number == "2":
                    print("Для обработки выбран CSV-файл.")
                    file_path = input("Введите путь к CSV-файл: ").strip()
                    with open(file_path, 'r', encoding='utf-8') as file:
                        first_line = file.readline()

                        if ';' in first_line:
                            delimiter = ';'
                        elif ',' in first_line:
                            delimiter = ','
                        else:
                            print("Ошибка: Неподдерживаемый формат CSV файла")
                            continue
                        file.seek(0)
                        reader = csv.DictReader(file, delimiter=delimiter)
                        data = list(reader)

                elif number == "3":
                    print("Для обработки выбран XLSX-файл.")
                    file_path = input("Введите путь к XLSX-файл: ").strip()
                    data = pd.read_excel(file_path).to_dict(orient='records')
                break
            except FileNotFoundError:
                print(f"Ошибка: Файл {file_path} не найден")

            except Exception as e:
                print(f"Произошла ошибка при чтении файла: {str(e)}")
        else:
            print("Ошибка! Выберите число из приведенных выше")
    print("""
Введите статус, по которому необходимо выполнить фильтрацию
Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING
""")
    while True:
        number = input("Введите статус: ").upper().strip()
        filtered_data = None

        valid_statuses = {"EXECUTED", "CANCELED", "PENDING"}
        if number in valid_statuses:
            filtered_data = filter_by_state(data, number)

            if number == "EXECUTED":
                print('Операции отфильтрованы по статусу "EXECUTED"')
            elif number == "CANCELED":
                print('Операции отфильтрованы по статусу "CANCELED"')
            elif number == "PENDING":
                print('Операции отфильтрованы по статусу "PENDING"')
            break
        else:
            print("Ошибка! Введите статус из приведенных выше")

    print("Отсортировать операции по дате? Да/Нет")
    while True:
        number = input("Введите да/нет: ").lower().strip()

        statuses = {"да", "нет"}

        if number in statuses:
            if number == "да":
                print('Выбор да')
                filtered_data = sort_by_date(filtered_data)
            elif number == "нет":
                print('Выбор нет')
            break
        else:
            print("Ошибка! Введите да/нет")

    print("Отсортировать по возрастанию или по убыванию?")
    while True:
        number = input("Введите по возрастанию/по убыванию: ").lower().strip()

        statuses = {"по возрастанию", "по убыванию"}

        if number in statuses:
            if number == "по возрастанию":
                print('Выбор по возрастанию')
            elif number == "по убыванию":
                print('Выбор по убыванию')
                filtered_data = sort_by_date(filtered_data, sorting=False)
            break
        else:
            print("Ошибка!")

    print("Выводить только рублевые транзакции? Да/Нет")
    results = []
    while True:
        number = input("Введите Да/Нет: ").lower().strip()
        statuses = {"да", "нет"}

        if number in statuses:
            if number == "да":
                print('Выбор да')
                for transaction in filtered_data:
                    try:
                        rub_amount = process_transaction(transaction)
                        results.append(rub_amount)
                    except ValueError as e:
                        print(f"Ошибка обработки транзакции: {e}")
                        results.append(None)
            elif number == "нет":
                print('Выбор нет')
                results = filtered_data.copy()
            break
        else:
            print("Ошибка! Введите да/нет")

    print("Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
    while True:
        number = input("Введите Да/Нет: ").lower().strip()

        statuses = {"да", "нет"}

        if number in statuses:
            if number == "да":
                print('Выбор да')
                numbers = input("Введите слово: ")
                name_pattern = fr'\b{numbers}\b'
                results = process_bank_search(results, name_pattern)
            elif number == "нет":
                print('Выбор нет"')
            break
        else:
            print("Ошибка! Введите да/нет")

    print("Распечатываю итоговый список транзакций...")
    if not results:
        return print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
    else:
        print(f"Всего банковских операций в выборке: {len(results)}\n")
        for transaction in results:
            try:
                formatted_date = get_date(transaction.get('date', 'N/A'))

                print(f"{formatted_date} {transaction.get('description', 'N/A')}")

                from_card = transaction.get('from', '')
                to_card = transaction.get('to', '')

                if from_card and to_card:
                    masked_from = get_mask_card_number(from_card)
                    masked_to = get_mask_card_number(to_card)
                    print(f"{masked_from} -> {masked_to}")

                amount = transaction.get('amount', 'N/A')
                currency = transaction.get('currency_name', transaction.get('currency_code', 'N/A'))

                if currency == 'RUB':
                    print(f"Сумма: {amount} руб.")
                else:
                    print(f"Сумма: {amount} {currency}")
                print()

            except Exception as e:
                print(f"Ошибка при выводе транзакции: {str(e)}")
                print()




if __name__ == "__main__":
    start_processing()
    trn = [{'id': '3235160', 'state': 'EXECUTED', 'date': '2023-11-12T16:17:52Z', 'amount': '34316',
            'currency_name': 'Euro', 'currency_code': 'EUR', 'from': 'Visa 2336865385909932',
            'to': 'American Express 2266395591845773', 'description': 'Перевод с карты на карту'}]
