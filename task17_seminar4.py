
with open("task17.txt", "r", encoding="utf-8") as file:
    total = 0
    min_value = float("inf")
    max_value = float("-inf")
    count = 0
    mean_value = 0
    for line in file:
        try:
            value = int(line)
        except ValueError:
            continue
        total += value
        min_value = min(value, min_value)
        max_value = max(value, max_value)
        count += 1
    if count != 0:
        mean_value = total / count
if count != 0:
    print(f"total: {total}, min: {min_value}, max: {max_value}, count: {count}, mean: {mean_value}")
else:
    print("Нет корректных чисел")
