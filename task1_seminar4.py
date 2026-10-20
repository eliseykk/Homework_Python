with open("text.txt", "r", encoding="utf-8") as file:
    line_counter = 0
    word_counter = 0
    symbol_counter = 0
    max_length_line = 0
    for line in file:
        line_counter += 1
        words = line.split()
        word_counter += len(words)
        symbol_counter += len(line)
        line = line.rstrip("\n")
        max_length_line = max(max_length_line, len(line))
print(f"line_counter: {line_counter}\n"
      f"word_counter: {word_counter}\n"
      f"symbol_counter: {symbol_counter}\n"
      f"max_length_line: {max_length_line}\n")




