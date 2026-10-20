def turn_matrix(old_matrix):
    old_rows = len(old_matrix)
    old_cols = len(old_matrix[0])
    new_matrix = [[0 for _ in range(old_rows)] for _ in range(old_cols)]
    for i in range(old_rows):
        for j in range(old_cols):
            new_matrix[j][-i-1] = old_matrix[i][j]
    return new_matrix
matrix = [[1, 2, 3],
          [4, 5, 6]]

def turn_matrix_minus90(old_matrix):
    new_matrix = turn_matrix(old_matrix)
    new_matrix = turn_matrix(new_matrix)
    new_matrix = turn_matrix(new_matrix)
    return new_matrix
print(turn_matrix_minus90(matrix))

