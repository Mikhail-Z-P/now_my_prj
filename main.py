import json
import csv
import pandas as pd
from regular_expressions import process_bank_search
from processing import sort_by_date, filter_by_state
from utils import process_transaction

def start_processing(*args, **kwargs):
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
                        reader = csv.DictReader(file)
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
                for transaction  in filtered_data:
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
    return print(results)





if __name__ == "__main__":
    print(start_processing())
