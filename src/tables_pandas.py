import pandas as pd

def reading_csv(file: str) -> list:
    """Функция чтения файла csv"""
    try:
        file_csv  = pd.read_csv(file)
        return file_csv .to_dict('records')
    except FileNotFoundError:
        print(f"Файл не найден: {file}")
        return []
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []

def reading_excel (file: str) -> list:
    """Функция чтения файла csv"""
    try:
        file_excel = pd.read_excel(file)
        return file_excel.to_dict('records')
    except FileNotFoundError:
        print(f"Файл не найден: {file}")
        return []
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []


if __name__ == "__main__":
    # transactions  = reading_csv("../data/transactions.csv")
    # print(transactions[:10])

    transactions = reading_excel("../data/transactions_excel.xlsx")
    print(transactions[:10])