import numpy as np


# TODO: В дальнейшем написать блок по задачам теорвера


class ProblemGenerator:

    def __init__(self, tier_param):

        self._tier = tier_param % 4  # TODO: 0-3

        self._types = {'algebra': ['det', 'eig', 'rank'],
                       'geometry': ['dot', 'vector_prod', 'norm']}

        self._curr_type = list(self._types.keys())[np.random.randint(0, len(self._types))]

    def _generator(self):

        task = getattr(self, '_' +
                       self._types[self._curr_type][np.random.randint(0, len(self._types[self._curr_type]))] +
                       '_' + self._curr_type + '_task')

        return task()

    def _det_algebra_task(self):

        length = elements = 2 + self._tier

        matrix = np.random.randint(-elements, elements, (length, length))

        task = 'Вычислить определитель матрицы:\n{}'.format(matrix)

        answer = int(round(np.linalg.det(matrix)))

        return task, [answer]

    def _eig_algebra_task(self):

        length, elements = 2 + self._tier, 1 + self._tier

        matrix = np.random.randint(-elements, elements, (length, length))

        matrix = 0.5 * (matrix + np.transpose(matrix))

        task = 'Вычислить собственные числа матрицы:\n(Округлить до сотых)\n{}'.format(matrix)

        eigenvalues = np.linalg.eigvals(matrix)

        answer = [round(ans, 2) for ans in eigenvalues]

        return task, list(answer)

    def _rank_algebra_task(self):

        length, elements = max(2, 1 + self._tier), 2 + self._tier

        matrix = np.random.randint(-elements, elements, (length, length))

        task = 'Найти ранг матрицы:\n{}'.format(matrix)

        answer = np.linalg.matrix_rank(matrix)

        return task, [answer]

    def _dot_geometry_task(self):

        value = 2 * (2 ** self._tier)

        length = 2 ** self._tier

        vector1, vector2 = np.random.randint(0, value, length), np.random.randint(0, value, length)

        task = 'Вычислить скалярное произведение векторов:\nv = {}\nu = {}'.format(vector1, vector2)

        answer = np.vdot(vector1, vector2)

        return task, [answer]

    def _vector_prod_geometry_task(self):

        value = 2 + 2 * self._tier

        vector1, vector2 = np.random.randint(-value, value, 3), np.random.randint(-value, value, 3)

        task = 'Вычислить векторное произведение векторов:\nv = {}\nu = {}'.format(vector1, vector2)

        answer = np.cross(vector1, vector2)

        return task, list(answer)

    def _norm_geometry_task(self):

        value = 2 + 2 ** self._tier

        length = 2 ** self._tier

        vector = np.random.randint(-value, value, length)

        task = 'Вычислить норму вектора:\n(Округлить до сотых)\nv = {}'.format(vector)

        answer = round(np.linalg.norm(vector), 2)

        return task, [answer]

    @property
    def get_task(self):

        return self._generator()
