def max_combo_val(sequence: list):
    max_combo = 0
    current_combo = 0
    current_value = sequence[0]
    max_combo_value = sequence[0]
    for element in sequence:
        if element == current_value:
            current_combo += 1
            if current_combo > max_combo:
                max_combo = current_combo
                max_combo_value = element
        else:
            current_combo = 1
            current_value = element
    return (max_combo, max_combo_value)
sequence = [1, 1, 1, 2, 2, 3, 3, 3, 3]
print(max_combo_val(sequence)[0])

