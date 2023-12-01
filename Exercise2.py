import gurobipy as gp
from gurobipy import GRB
import random

n = 10  # number of tasks
p = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]  # processing times
m = 4  # number of machines
T = [[] for _ in range(m)]  # which machine does which task list


# solve the instance using the greedy algorithm
for i in range(n):

    low = float('inf')  # lowest completion time
    machine = 0  # machine with lowest completion time

    for j in range(m):

        total = sum(T[j])  # calculate completion time

        if total < low:

            low = total
            machine = j

    T[machine].append(p[i])  # schedule the task on the machine
print(T)
# calculate the highest completion time
high = 0
machine = 0

for i in range(len(T)):

    total = sum(T[i])

    if total > high:

        machine = i
        high = total

print("Max completion time Greedy: {}".format(high))


# create a large instance that takes at least 5 seconds to run
n = 2000  # number of tasks
p = [random.uniform(0, 10) for _ in range(n)]  # processing times
m = 50  # number of machines
T = [[] for _ in range(m)]  # which machine does which task list


# creating the ILP solver
model = gp.Model("Min Max C")

# Set a time limit of 5 seconds
model.setParam('TimeLimit', 5.0)

# Add decision variables
# Create a 2D binary variable x
x = model.addVars(n, m, vtype=GRB.BINARY, name="x")
# Create the maximum completion time variable z
z = model.addVar(vtype=GRB.CONTINUOUS, name="z")

# Maximum completion time constraint
for j in range(m):
    model.addConstr(gp.quicksum(x[i, j] * p[i] for i in range(n)) <= z)

# Schedule each job constraint
for i in range(n):
    model.addConstr(gp.quicksum(x[i, j] for j in range(m)) == 1)

# Set objective function

model.setObjective(z, sense=GRB.MINIMIZE)
# Optimize the model
model.optimize()
# Check if an optimal solution was found
if model.status == GRB.OPTIMAL:
    # Get the objective value
    objective_value = model.objVal
    print(f"Optimal objective value: {objective_value}")
  
else:
    print("No solution found")
