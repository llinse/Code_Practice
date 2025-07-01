from gurobipy import *

try:
    # Create a new model
    m = Model("mip1")

    # Create variables
    x1 = m.addVar(vtype=GRB.BINARY, name="x1")
    x2 = m.addVar(vtype=GRB.BINARY, name="x2")

    # Set objective
    m.setObjective(4*x1 + x2, GRB.MINIMIZE)

    # Add constraint
    m.addConstr(3*x1+x2==4, "c0")
    m.addConstr(4*x1+3*x2>=6, "c1")
    m.addConstr(x1+2*x2<=4, "c2")

    m.optimize()

    for v in m.getVars():
        print('%s %g' % (v.varName, v.x))

    print('Obj: %g' % m.objVal)

except GurobiError as e:
    print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
    print('Encountered an attribute error')


