import numpy as np


class Matrix(np.lib.mixins.NDArrayOperatorsMixin):
    def __init__(self, matrix):
        self._matrix = self.prepare_matrix_to_list(matrix)

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

    def __str__(self):
        # может быть костыльно и замудрено, но выводит красиво :)
        def transfer(i: int):
            i = str(i)
            return " " * (1 + (3 - len(i))) + i + " "

        max_count_in_row = max(len(i) for i in self.matrix)
        result = []
        for i in self.matrix:
            result.append(f"{'-' * (1 + max_count_in_row * 6)}\n")
            result.append("|")
            result.append("|".join(map(transfer, i)))
            result.append("|\n")

        result.append("-" * (1 + max_count_in_row * 6))
        return "".join(result)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.rows}, {self.cols}, {self.matrix})"

    def save_to_file(self, filename):
        np.savetxt(filename, self.matrix, fmt='%d')

    @staticmethod
    def prepare_matrix_to_list(matrix):
        # преобразуем данные в список при необходимости (и при такой возможности)
        if isinstance(matrix, np.ndarray):
            return matrix.tolist()
        elif isinstance(matrix, list):
            return matrix
        else:
            raise ValueError("Incorrect input matrix type")

    @property
    def matrix(self):
        return self._matrix

    @matrix.setter
    def matrix(self, new_matrix):
        self._matrix = self.prepare_matrix_to_list(new_matrix)

    # для rows и cols нужно только getter, так как они напрямую зависят от хранимой матрицы
    @property
    def rows(self):
        return len(self.matrix)

    @property
    def cols(self):
        return len(self.matrix[0])


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

    # Запись результатов в текстовые файлы реализованным методом
    result_add.save_to_file('./artifacts/3_2/matrix+.txt')
    result_mul.save_to_file('./artifacts/3_2/matrix*.txt')
    result_matmul.save_to_file('./artifacts/3_2/matrix@.txt')

    # для сравнения с numpy сделаем те же самые встроенные действия над матрицами
    # и проверим корректность работы нашей реализации
    result_add = a + b
    result_mul = a * b
    result_matmul = a @ b

    np.savetxt('./artifacts/3_2/matrix_numpy+.txt', result_add, fmt='%d')
    np.savetxt('./artifacts/3_2/matrix_numpy*.txt', result_mul, fmt='%d')
    np.savetxt('./artifacts/3_2/matrix_numpy@.txt', result_matmul, fmt='%d')
