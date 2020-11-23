from gurobipy import *
m = Model("mip1")

# Create variables
x = m.addVar(vtype=GRB.BINARY, name='x')
y = m.addVar(vtype=GRB.BINARY, name='y')
z = m.addVar(vtype=GRB.BINARY, name='z')

m.setObjective(x + y + 2*z, GRB.MAXIMIZE)

# Add constraints
m.addConstr(x + 2 * y + 3*z <= 4, "c0")
m.addConstr(x + y >= 1, "c1")

# Solve and print solution
m.optimize()
m.printAttr('X')
