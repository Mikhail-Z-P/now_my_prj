def name_list(file_names: str) -> list:
    """ Функцыя убирает лишние знаки припинания и цфры """
    formatted_names_list = list()
    with open('data/' + file_names, encoding='utf-8') as names_file:
        names_list = names_file.read().split()
        for name_item in names_list:
            new_name = ''
            for symbol in name_item:
                if symbol.isalpha():
                    new_name += symbol
            if new_name.isalpha():
                formatted_names_list.append(new_name)
    return formatted_names_list

if __name__ == '__main__':
    cleared_name = name_list('names.txt')
    for i in cleared_name:
        print(i)