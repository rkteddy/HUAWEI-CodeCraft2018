import copy

EPS = 1e-10


class matrix:

    def __init__(self, arg_1, arg_2=0, arg_3=0.0):
        if isinstance(arg_1, list):
            self.rows_ = len(arg_1)
            self.cols_ = len(arg_1[0])
            self.__matrix = arg_1
            self.shape = (self.rows_, self.cols_)
        else:
            if isinstance(arg_1, int) and isinstance(arg_2, int):
                self.rows_ = arg_1
                self.cols_ = arg_2
                self.__matrix = [[arg_3] * arg_2 for i in range(arg_1)]
                self.shape = (arg_1, arg_2)
            else:
                raise TypeError("parameters wrong")

    def __getitem__(self, index):
        if isinstance(index, int):
            return self.__matrix[index]
        elif isinstance(index, tuple):
            return self.__matrix[index[0]][index[1]]

    def __setitem__(self, index, value):
        if isinstance(index, int):
            self.__matrix[index] = copy.deepcopy(value)
        elif isinstance(index, tuple):
            self.__matrix[index[0]][index[1]] = value

    def __add__(self, N):
        assert N.rows_ == self.rows_ and N.cols_ == self.cols_, "dimension not match"
        M = matrix(self.rows_, self.cols_)
        for i in range(self.rows_):
            for j in range(self.cols_):
                M[i, j] = self[i, j] + N[i, j]
        return M

    def __mul__(self, N):
        if isinstance(N, int) or isinstance(N, float):
            M = matrix(self.rows_, self.cols_)
            for i in range(self.rows_):
                for j in range(self.cols_):
                    M[i, j] = self[i, j] * N
        else:
            assert N.rows_ == self.cols_, "dimension not match"
            M = matrix(self.rows_, N.cols_)
            for i in range(self.rows_):
                for j in range(N.cols_):
                    tmp_sum = 0
                    for k in range(self.cols_):
                        tmp_sum += self[i, k] * N[k, j]
                    M[i, j] = tmp_sum
        return M

    def inner_list(self):
        return self.__matrix
