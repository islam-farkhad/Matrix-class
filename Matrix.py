from copy import deepcopy


class MatrixError(BaseException):
    def __init__(self, first_matrix, second_matrix):
        self.matrix1 = first_matrix
        self.matrix2 = second_matrix


class Matrix:
    def __init__(self, list_of_lists):
        self.matrix = deepcopy(list_of_lists)
        self.rows_qty = len(list_of_lists)
        self.columns_qty = len(list_of_lists[0])

    def __str__(self):
        strings_of_matrix = []
        for sublist in self.matrix:
            sublist = map(str, sublist)
            strings_of_matrix.append('\t'.join(sublist))
        matrix_ = '\n'.join(strings_of_matrix)
        return matrix_

    def size(self):
        return self.rows_qty, self.columns_qty

    def __add__(self, other):
        if self.rows_qty == other.row_qty and \
                self.columns_qty == other.column_qty:
            result = Matrix(self.matrix)
            for i in range(self.rows_qty):
                for j in range(self.columns_qty):
                    result[i][j] += other[i][j]
            return result
        else:
            raise MatrixError(self, other)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            new_matrix = Matrix(self.matrix)
            for i in range(self.rows_qty):
                for j in range(self.columns_qty):
                    new_matrix[i][j] *= other
            return new_matrix

        elif isinstance(other, Matrix):
            if self.columns_qty == other.rows_qty:
                new_matrix = [[0 for j in range(other.columns_qty)]
                              for i in range(self.rows_qty)]
                for i in range(self.rows_qty):
                    for j in range(other.columns_qty):
                        current_sum = 0
                        for k in range(self.columns_qty):
                            current_sum += \
                                self.matrix[i][k] * other.matrix[k][j]
                        new_matrix[i][j] = current_sum
                return Matrix(new_matrix)
            else:
                raise MatrixError(self, other)
        else:
            raise Exception

    def __rmul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return self.__mul__(other)

        raise Exception

    def __getitem__(self, row):
        return self.matrix[row]

    def __setitem__(self, i, j, value):
        self.matrix[i][j] = value

    def transpose(self):
        self.matrix = list(zip(*self.matrix))
        return self

    @staticmethod
    def transposed(self):
        return Matrix(list(zip(*self.matrix)))


class SquareMatrix(Matrix):

    def __pow__(self, degree):
        result = Matrix(self.matrix)
        temp = Matrix(self.matrix)

        for i in range(result.rows_qty):
            for j in range(result.columns_qty):
                if i == j:
                    result[i][j] = 1
                else:
                    result[i][j] = 0

        while degree != 0:

            if degree % 2 != 0:
                result *= temp
                degree -= 1

            else:
                temp *= temp
                degree //= 2

        return result

    def solve(self, b):
        def e1(a, b, i, j, coefficient):
            a[i] = [a[i][k] + a[j][k] * coefficient for k in range(len(a[i]))]
            b[i] += b[j] * coefficient

        def e2(a, b, i, j):
            a[i], a[j] = a[j], a[i]
            b[i], b[j] = b[j], b[i]

        def e3(a, b, i, coefficient):
            a[i] = [a[i][j] * coefficient for j in range(len(a[i]))]
            b[i] *= coefficient

        def make_stepped(a, b):
            for column in range(len(a[0])):
                leading_row_for_column = column
                for i in range(column, len(a)):
                    if abs(a[i][column]) > \
                            abs(a[leading_row_for_column][column]):
                        leading_row_for_column = i

                if a[leading_row_for_column][column] == 0:
                    raise ZeroDivisionError

                e2(a, b, leading_row_for_column, column)
                e3(a, b, column, 1 / a[column][column])
                for row in range(column + 1, len(a)):
                    e1(a, b, row, column, -a[row][column])

            for column in range(len(a) - 1, -1, -1):
                for row in range(column):
                    e1(a, b, row, column, -a[row][column])
            return a, b

        matrix_copy = deepcopy(self.matrix)
        answer = b.copy()
        make_stepped(matrix_copy, answer)

        return Matrix(matrix_copy), answer


# Example
m = SquareMatrix([[5, 4, 3],
                  [2, 8, 16],
                  [7, -10, 25],
                  ])

a = 5 * m
print(a)
print(m)
print('----------')
b = [3, 24, 50]
print(*b)
a, ans = m.solve(b)
print('----------')
print(*ans)
print('----------')

c = Matrix([[1, 0, 0, 0, 0, 0, 0, 0]])
b = Matrix([[1], [0], [0], [0], [0], [0], [0], [0]])
print(c * b)
print('----------')
print(b * c)
