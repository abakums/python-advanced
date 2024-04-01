import numpy as np


def cached_matrix_product(method):
    # в теории можно было бы сделать кэш и в виде глобальной переменной, и в виде записи в global(), но в данном
    # случае не вижу смысла (нет особого смысла давать доступ к кэшу из каждой функции и из любого места
    # программы)
    cache = {}

    def wrapper(self, other):
        # одно допущение: если ключ -- это кортеж из хэшей, то при коллизии срабатывает кеш и для второго
        # произведения считается некорректное произведение; если брать в качестве ключей кортеж из самих
        # матриц -- для второго произведения не срабатывает взятие из кэша и результат считается корректно.
        # это логично, так как если брать hash -- он везде одинаковый для моей хэш функции,
        # если брать сами матрицы, то A != C
        key = (hash(self), hash(other))
        # key = (self, other)
        if key in cache:
            print("Взяли из кэша")
            return cache[key]
        else:
            result = method(self, other)
            cache[key] = result
            return result

    return wrapper


class MatrixHashMixin:
    def __hash__(self):
        """Простейшая хэш-функция на основе суммы элементов матрицы"""
        hash_val = sum(sum(row) for row in self.matrix)
        return hash(hash_val)

    # в задании не просилось, но решил сделать __eq__ и __ne__, чтобы в assert проверить корректность условий для коллизии
    def __eq__(self, other):
        """ Определяем семантику равентсва (оператор ==)"""
        if not isinstance(other, self.__class__):
            return False
        return self.matrix == other.matrix

    def __ne__(self, other):
        """ Определяем семантику неравентсва (оператор !=)"""
        if not isinstance(other, self.__class__):
            return False
        return self.matrix != other.matrix


class Matrix(MatrixHashMixin, np.lib.mixins.NDArrayOperatorsMixin):
    def __init__(self, matrix):
        self._matrix = self.prepare_matrix_to_list(matrix)
        self._rows = len(self._matrix)
        self._cols = len(self._matrix[0])

    def __add__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions for addition")

        result = []
        for i in range(self.rows):
            row = [self.matrix[i][j] + other.matrix[i][j] for j in range(self.cols)]
            result.append(row)

        return Matrix(result)

    @cached_matrix_product
    def __mul__(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions for multiplication")

        result = []
        for i in range(self.rows):
            row = [self.matrix[i][j] * other.matrix[i][j] for j in range(self.cols)]
            result.append(row)

        return Matrix(result)

    @cached_matrix_product
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
    # np.random.seed(0)
    # a = np.random.randint(0, 10, (10, 10))
    # b = np.random.randint(0, 10, (10, 10))

    matrix1 = Matrix([[10, 20], [30, 40]])
    matrix2 = Matrix([[50, 60], [70, 80]])
    matrix3 = Matrix([[10, 20], [30, 40]])
    matrix4 = Matrix([[50, 60], [70, 80]])

    # с print'ами проверил работу кэша (что он берется корректно и тогда, когда есть в словаре); стоит отметить,
    # что словарь с кэшем разный для разных операций: для __mul__ свой, для __matmul__ -- свой
    mul1 = matrix1 * matrix2
    mul2 = matrix3 * matrix4

    matmul1 = matrix1 @ matrix2
    matmul2 = matrix3 @ matrix4

    a = Matrix([[1, 2], [3, 4]])
    b = Matrix([[5, 6], [7, 8]])
    d = Matrix([[5, 6], [7, 8]])  # == b
    c = Matrix([[0, 3], [1, 6]])
    a.save_to_file("./artifacts/3_3/A.txt")
    b.save_to_file("./artifacts/3_3/B.txt")
    c.save_to_file("./artifacts/3_3/C.txt")
    d.save_to_file("./artifacts/3_3/D.txt")

    assert hash(a) == hash(c)
    assert a != c
    assert b == d
    # матрицы проходят условия из задания

    ab = a @ b
    cd = c @ d

    print(ab != cd)
    print(hash(ab), hash(cd))
