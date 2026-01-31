def summ(a, b):
    return a + b

def main():
    d = summ(1, 4)
print(main)

if __name__ == '__main__':
    print("Check", summ(4,5),"==", 9 )


def lists(list_1: list, list_2: list) -> list:
    """функцыя которая находит пересечения между двумя списками"""

    return list(set(list_1).intersection(list_2))


def is_palindrome(num):
    """Функция проверяет, является ли число палиндромом"""
    return str(num) == str(num)[::-1]


def not_is_list(list_1: list[int], list_2: list[int]) -> list[int]:
    """Функцыя возвращяет список в котором не повторяющиеся числа"""
    nom = []

    for lists in list_1:
        if lists not in list_2:
            nom.append(lists)
    for lists in list_2:
        if lists not in list_1:
            nom.append(lists)
    return nom

    # return list(set(list_1) - set(list_2)) + list(set(list_2) - set(list_1))


def circle_area(r: float) -> float:
    """Подсчет площяди окружности"""
    pi = 3.14
    return pi * r**2


def format_description(r: float, area: float) :
    """Форматированный вывод информации об окружности"""
    return "Radius is " + str(r) + "; area is " + str(round(area, 2))


def get_circle_info(r: float) -> None:
    """Получение информации об окружности"""
    area = circle_area(r)
    description = format_description(r, area)
    print(description)
