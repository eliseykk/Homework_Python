from math import isfinite


def check_numbers(numbers, k):
    if not isfinite(k) or k < 0:
        raise ValueError("k должен быть конечным неотрицательным числом")
    for value in numbers:
        if not isfinite(value):
            raise ValueError("В списке должны быть только конечные числа")


def find_anomalies(numbers, k):
    check_numbers(numbers, k)
    if not numbers:
        return []

    total = 0
    for value in numbers:
        total += value
    mean_value = total / len(numbers)

    total_square = 0
    for value in numbers:
        total_square += (value - mean_value) ** 2
    standard_deviation = (total_square / len(numbers)) ** 0.5

    anomalies = []
    for value in numbers:
        if abs(value - mean_value) > k * standard_deviation:
            anomalies.append(value)
    return anomalies


def find_anomalies_numpy(numbers, k):
    import numpy as np

    check_numbers(numbers, k)
    if not numbers:
        return []

    array = np.array(numbers, dtype=float)
    mean_value = np.mean(array)
    standard_deviation = np.std(array, ddof=0)
    anomalies = []
    for i in range(len(numbers)):
        if abs(array[i] - mean_value) > k * standard_deviation:
            anomalies.append(numbers[i])
    return anomalies


if __name__ == "__main__":
    numbers = [10, 11, 10, 12, 11, 10, 100]
    k = 2
    result = find_anomalies(numbers, k)
    print("Без numpy:", result)
    try:
        result_numpy = find_anomalies_numpy(numbers, k)
    except ImportError:
        print("Для второго варианта установи numpy: python -m pip install numpy")
    else:
        print("С numpy:", result_numpy)
        print("Результаты совпадают:", result == result_numpy)
