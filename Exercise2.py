import gurobipy as gp
import math
from gurobipy import GRB
import random as r
from InstanceGenerator import Tasks
from tqdm import tqdm

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
p = [r.uniform(0, 10) for _ in range(n)]  # processing times
p.sort()
m = 50  # number of machines

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
# Get the objective value
objective_value = model.objVal
print(f"Optimal objective value: {objective_value}")

# start the Q-learnign using new Instances
# 10 starting positiion with two options each
Q = [[float(0), float(0)] for _ in range(10)]
eps = 1000
alpha = 1
e = 0.1
selected = [float(0) for _ in range(10)]
for _ in tqdm(range(eps)):
    random = r.random()
    random2 = r.random()
    # Create a new instance
    newInstance = Tasks(2000, 50, random)
    # calculate the starting state
    state = int(math.floor(random * 10))
    # Have to take a random choise, so we dont stick to the first option
    if random2 < eps:
        p = r.random()
        # take each option with the same probability
        if p <= 0.5:
            newInstance.Greedy(50)
            result = newInstance.ILP_solver()
            Q[state][0] += result / (selected[state] + 1)
            selected[state] += 1
        else:
            newInstance.Greedy(200)
            result = newInstance.ILP_solver()
            Q[state][1] += result / (selected[state] + 1)
            selected[state] += 1
    # Take the highest state value
    else:
        if Q[state][0] <= Q[state][1]:
            newInstance.Greedy(50)
            result = newInstance.ILP_solver()
            Q[state][0] += result / (selected[state] + 1)
            selected[state] += 1
        else:
            newInstance.Greedy(200)
            result = newInstance.ILP_solver()
            Q[state][1] += result / (selected[state] + 1)
            selected[state] += 1

print(Q)
