import random

def transpose_matrix(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    transposed = [[0] * rows for _ in range(cols)]

    for i in range(rows):
        for j in range(cols):
            transposed[j][i] = matrix[i][j]

    return transposed


n = int(input("Enter number of rows: "))
m = int(input("Enter number of columns: "))

matrix = [[random.randint(1, 9) for _ in range(m)] for _ in range(n)]

print("Original matrix:")
for row in matrix:
    print(row)

result = transpose_matrix(matrix)

print("Transposed matrix:")
for row in result:
    print(row)
