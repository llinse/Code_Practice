import cvxpy as cvx

x = cvx.Variable(3)
x1 = x[0]
x2 = x[1]
objective = 4*x1+x2
# 约束条件
constraints = [3*x1+x2==3,4*x1+3*x2>=6,x1+2*x2<=4,x1>=0,x2>=0]
# 目标函数
obj = cvx.Minimize(objective)
prob = cvx.Problem(obj,constraints)
# 不同求解器,cvx.CVXOPT,cvx.GUROBI,cvx.MOSEK未安装
solvers = [cvx.SCS]
for solver in solvers:
    prob.solve(solver=solver)
    print("status:",prob.status)
    print("optimal value",prob.value)
    print("optimal var",x.value)

