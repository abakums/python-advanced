import numpy as np


class Matrix:
    def __init__(self, matrix):
        # преобразуем данные в список при необходимости (и при такой возможности)
        if isinstance(matrix, np.ndarray):
            self.matrix = matrix.tolist()
        elif isinstance(matrix, list):
            self.matrix = matrix
        else:
            raise ValueError("Incorrect input matrix type")

        self.rows = len(self.matrix)
        self.cols = len(self.matrix[0])

    def __add__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions for addition")

        result = []
        for i in range(self.rows):
            row = [self.matrix[i][j] + other.matrix[i][j] for j in range(self.cols)]
            result.append(row)

        return Matrix(result)

    def __mul__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions for multiplication")

        result = []
        for i in range(self.rows):
            row = [self.matrix[i][j] * other.matrix[i][j] for j in range(self.cols)]
            result.append(row)

        return Matrix(result)

    def __matmul__(self, other):
        if self.cols != other.rows:
            raise ValueError("Number of columns in the first matrix must be equal to the number of rows in the second matrix for matrix multiplication")

        result = []
        for i in range(self.rows):
            row = []
            for j in range(other.cols):
                val = sum(self.matrix[i][k] * other.matrix[k][j] for k in range(self.cols))
                row.append(val)
            result.append(row)

        return Matrix(result)


if __name__ == "__main__":
    np.random.seed(0)
    a = np.random.randint(0, 10, (10, 10))
    b = np.random.randint(0, 10, (10, 10))

    # Генерация двух матриц
    matrix1 = Matrix(a)
    matrix2 = Matrix(b)

    # Выполнение операций
    result_add = matrix1 + matrix2
    result_mul = matrix1 * matrix2
    result_matmul = matrix1 @ matrix2

    # Запись результатов в текстовые файлы
    np.savetxt('./artifacts/3_1/matrix+.txt', result_add.matrix, fmt='%d')
    np.savetxt('./artifacts/3_1/matrix*.txt', result_mul.matrix, fmt='%d')
    np.savetxt('./artifacts/3_1/matrix@.txt', result_matmul.matrix, fmt='%d')

    # для сравнения с numpy сделаем те же самые встроенные действия над матрицами
    # и проверим корректность работы нашей реализации
    result_add = a + b
    result_mul = a * b
    result_matmul = a @ b

    np.savetxt('./artifacts/3_1/matrix_numpy+.txt', result_add, fmt='%d')
    np.savetxt('./artifacts/3_1/matrix_numpy*.txt', result_mul, fmt='%d')
    np.savetxt('./artifacts/3_1/matrix_numpy@.txt', result_matmul, fmt='%d')
