from pulp import *

# creat a LP maximization problem
prob = LpProblem("problem1",LpMinimize)
x1 = LpVariable("x1",lowBound=0) # creat a variable x1>=0
x2 = LpVariable("x2",lowBound=0)

# objective function
prob += 4*x1 + x2
# constraint (只支持大于等于、小于等于、等于约束式)
prob += x1 + 2*x2 <= 4
prob += 4*x1 + 3*x2  >= 6
prob += 3*x1 + x2  == 3

print(prob)  #display the LP problem
prob.writeLP("problem1.lp")
prob.solve()

print("\n","status:",LpStatus[prob.status],"\n")
#show the solution
for v in prob.variables():
    print("\t",v.name,"=",v.varValue,"\n")
print(value(prob.objective))
