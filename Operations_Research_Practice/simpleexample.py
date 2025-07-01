# import numpy as np
#
#
# class Simplex(object):
#     def __init__(self, obj, max_mode=False):  # default is solve min LP, if want to solve max lp,should * -1
#         self.mat, self.max_mode = np.array([[0] + obj]) * (-1 if max_mode else 1), max_mode
#
#     def add_constraint(self, a, b):
#         self.mat = np.vstack([self.mat, [b] + a])
#
#     def _simplex(self, mat, B, m, n):
#         while mat[0, 1:].min() < 0:
#             col = np.where(mat[0, 1:] < 0)[0][0] + 1  # use Bland's method to avoid degeneracy. use mat[0].argmin() ok?
#             row = np.array([mat[i][0] / mat[i][col] if mat[i][col] > 0 else 0x7fffffff for i in
#                             range(1, mat.shape[0])]).argmin() + 1  # find the theta index
#             if mat[row][col] <= 0: return None  # the theta is ∞, the problem is unbounded
#             self._pivot(mat, B, row, col)
#         return mat[0][0] * (1 if self.max_mode else -1), {B[i]: mat[i, 0] for i in range(1, m) if B[i] < n}
#
#     def _pivot(self, mat, B, row, col):
#         mat[row] /= mat[row][col]
#         ids = np.arange(mat.shape[0]) != row
#         mat[ids] -= mat[row] * mat[ids, col:col + 1]  # for each i!= row do: mat[i]= mat[i] - mat[row] * mat[i][col]
#         B[row] = col
#
#     def solve(self):
#         m, n = self.mat.shape  # m - 1 is the number slack variables we should add
#         temp, B = np.vstack([np.zeros((1, m - 1)), np.eye(m - 1)]), list(range(n - 1, n + m - 1))  # add diagonal array
#         mat = self.mat = np.hstack([self.mat, temp])  # combine them!
#         if mat[1:, 0].min() < 0:  # is the initial basic solution feasible?
#             row = mat[1:, 0].argmin() + 1  # find the index of min b
#             temp, mat[0] = np.copy(mat[0]), 0  # set first row value to zero, and store the previous value
#             mat = np.hstack([mat, np.array([1] + [-1] * (m - 1)).reshape((-1, 1))])
#             self._pivot(mat, B, row, mat.shape[1] - 1)
#             if self._simplex(mat, B, m, n)[0] != 0: return None  # the problem has no answer
#
#             if mat.shape[1] - 1 in B:  # if the x0 in B, we should pivot it.
#                 self._pivot(mat, B, B.index(mat.shape[1] - 1), np.where(mat[0, 1:] != 0)[0][0] + 1)
#             self.mat = np.vstack([temp, mat[1:, :-1]])  # recover the first line
#             for i, x in enumerate(B[1:]):
#                 self.mat[0] -= self.mat[0, x] * self.mat[i + 1]
#         return self._simplex(self.mat, B, m, n)


import numpy as np


class Simplex(object):
    def __init__(self, c, A, b):
        # 形式 minf(x)=c.Tx
        # s.t. Ax=b
        self.c = c
        self.A = A
        self.b = b

    def run(self):
        c_shape = self.c.shape
        A_shape = self.A.shape
        b_shape = self.b.shape
        assert c_shape[0] == A_shape[1], "Not Aligned A with C shape"
        assert b_shape[0] == A_shape[0], "Not Aligned A with b shape"

        # 找到初始的B，N等值
        end_index = A_shape[1] - A_shape[0]
        N = self.A[:, 0:end_index]
        N_columns = np.arange(0, end_index)
        c_N = self.c[N_columns, :]
        # 第一个B必须是可逆的矩阵，其实这里应该用算法寻找，但此处省略
        B = self.A[:, end_index:]
        B_columns = np.arange(end_index, A_shape[1])
        c_B = self.c[B_columns, :]

        steps = 0
        while True:
            steps += 1
            print("Steps is {}".format(steps))
            is_optim, B_columns, N_columns = self.main_simplex(B, N, c_B, c_N, self.b, B_columns, N_columns)
            if is_optim:
                break
            else:
                B = self.A[:, B_columns]
                N = self.A[:, N_columns]
                c_B = self.c[B_columns, :]
                c_N = self.c[N_columns, :]

    def main_simplex(self, B, N, c_B, c_N, b, B_columns, N_columns):
        B_inverse = np.linalg.inv(B)
        P = (c_N.T - np.matmul(np.matmul(c_B.T, B_inverse), N)).flatten()
        if P.min() >= 0:
            is_optim = True
            print("Reach Optimization.")
            print("B_columns is {}".format(B_columns))
            print("N_columns is {}".format(sorted(N_columns)))
            best_solution_point = np.matmul(B_inverse, b)
            print("Best Solution Point is {}".format(best_solution_point.flatten()))
            print("Best Value is {}".format(np.matmul(c_B.T, best_solution_point).flatten()[0]))
            print("\n")
            return is_optim, B_columns, N_columns
        else:
            # 入基
            N_i_in = np.argmin(P)
            N_i = N[:, N_i_in].reshape(-1, 1)
            # By=Ni， 求出基
            y = np.matmul(B_inverse, N_i)
            x_B = np.matmul(B_inverse, b)
            N_i_out = self.find_out_base(y, x_B)
            tmp = N_columns[N_i_in]
            N_columns[N_i_in] = B_columns[N_i_out]
            B_columns[N_i_out] = tmp
            is_optim = False

            print("Not Reach Optimization")
            print("In Base is {}".format(tmp))
            print("Out Base is {}".format(N_columns[N_i_in]))   # 此时已经被换过去了
            print("B_columns is {}".format(sorted(B_columns)))
            print("N_columns is {}".format(sorted(N_columns)))
            print("\n")
            return is_optim, B_columns, N_columns

    def find_out_base(self, y, x_B):
        # 找到x_B/y最小且y>0的位置
        index = []
        min_value = []
        for i, value in enumerate(y):
            if value <= 0:
                continue
            else:
                index.append(i)
                min_value.append(x_B[i]/float(value))

        actual_index = index[np.argmin(min_value)]
        return actual_index


if __name__ == "__main__":
    '''
    c = np.array([-20, -30, 0, 0]).reshape(-1, 1)
    A = np.array([[1, 1, 1, 0], [0.1, 0.2, 0, 1]])
    b = np.array([100, 14]).reshape(-1, 1)
    '''
    c = np.array([-4, -1, 0, 0, 0]).reshape(-1, 1)
    A = np.array([[-1, 2, 1, 0, 0], [2, 3, 0, 1, 0], [1, -1, 0, 0, 1]])
    b = np.array([4, 12, 3]).reshape(-1, 1)
    simplex = Simplex(c, A, b)
    simplex.run()

