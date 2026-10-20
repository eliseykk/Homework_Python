
def chess_matrix(rows, columns, char1, char2):
    matrix = [[0] * columns for _ in range(rows)]
    for row in range(rows):
        for column in range(columns):
            if (row + column) % 2 == 0:
                matrix[row][column] = char1
            else:
                matrix[row][column] = char2
    return matrix
rows, columns = map(int, input("Введите n и m: ").split())
char1, char2 = input("Введите символы через пробел: ").split()
chess_matrix(rows, columns, char1, char2)
