def find_similar_strings(strings):
    min_difference = None
    first_string = None
    second_string = None

    for i in range(len(strings)):
        for j in range(i + 1, len(strings)):
            if len(strings[i]) != len(strings[j]):
                continue
            difference = 0
            for position in range(len(strings[i])):
                if strings[i][position] != strings[j][position]:
                    difference += 1
            if min_difference is None or difference < min_difference:
                min_difference = difference
                first_string = strings[i]
                second_string = strings[j]

    if min_difference is None:
        return None
    return first_string, second_string, min_difference


if __name__ == "__main__":
    strings = ["abcdef", "abcxef", "hello", "world", "abcxyz"]
    result = find_similar_strings(strings)
    if result is None:
        print("Нет двух строк одинаковой длины")
    else:
        first_string, second_string, difference = result
        print("Первая строка:", first_string)
        print("Вторая строка:", second_string)
        print("Количество различий:", difference)
