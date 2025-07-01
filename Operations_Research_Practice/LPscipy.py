from scipy.optimize import linprog
import numpy as np

#scipy.optimize.linprog(c, A_ub=None, b_ub=None, A_eq=None, b_eq=None, bounds=None, method='simplex', callback=None, options=None)
# 类似lingo与matlab，固定求最小值
# c（一维阵列）：目标函数的系数
# A_ub（二维数组）：小于某值的约束式系数、b_ub（一维数组）：约束值
# A_eq（二维数组）：等于某值的约束式系数、b_eq（一维数组）：约束值
# bounds : 决策变量（大于零）的约束条件，bounds=[(min, max)，(0, None)]，None代表无约束
# method{‘interior-point’, ‘revised simplex’, ‘simplex’}

c = [4, 1]
Au = [[-4, -3], [1, 2]]
bu = [-6, 4]
Ae = [[3, 1]]
be = [3]
x0_bounds = (0, None)
x1_bounds = (0, None)
res = linprog(c, A_ub=Au, b_ub=bu, A_eq=Ae, b_eq=be, bounds=[x0_bounds, x1_bounds], method='simplex')
print(res)

# fun为目标函数的最优值
# slack为松弛变量
# status表示优化结果状态
# nit 在所有阶段中执行的迭代总数。
# status 表示算法退出状态的整数。
# 0 ：优化成功终止。
# 1 ：达到迭代限制。
# 2 ：问题似乎不可行。
# 3 ：问题似乎是无限的。
# 4 ：遇到数字困难。