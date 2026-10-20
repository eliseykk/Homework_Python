min_value = float("inf")
max_value = float("-inf")
with open("numbers.txt", "r", encoding="utf-8") as file:
    counter = 0
    total = 0
    for line in file:
        try:
            number = int(line)
        except ValueError:
            continue
        else:
            min_value = min(min_value, number)
            max_value = max(max_value, number)
            total += number
            counter += 1
    if counter != 0:
        mean_value = total / counter
with open("result.txt", "w", encoding="utf-8") as file:
    if counter != 0:
        file.write(f"Среднее арифметическое: {mean_value}\n")
        file.write(f"Минимальное значение: {min_value}\n")
        file.write(f"Максимальное значение: {max_value}\n")
    else:
        file.write("НЕТ КОРРЕКТНЫХ ЧИСЕЛ")


