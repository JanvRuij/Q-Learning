import random as r
import numpy as np
import gurobipy as gp
from gurobipy import GRB


# Instance generator class
class Tasks:
    def __init__(self, n, m, random):
        self.n = n
        self.m = m
        self.p = np.array([r.uniform(0, 10) if r.random() < random
                           else r.uniform(500, 600) for _ in range(n)])
        self.T = np.zeros((m, n), dtype=int)

    def Greedy(self, stopping_criteria):
        self.p[::-1].sort()  # Sort along axis 0

        # solve the instance using the greedy algorithm
        for n in range(stopping_criteria):
            low = float('inf')  # lowest completion time
            machine = 0  # machine with lowest completion time
            # check completion time on each machine
            for m in range(self.m):
                # calculate completion time
                total = np.dot(self.T[m], self.p)
                # if it's the lowest, store the machine number
                if total < low:
                    low = total
                    machine = m
            # schedule the task on the machine
            self.T[machine][n] = 1

    def ILP_solver(self):
        # creating the ILP solver
        model = gp.Model("min max c")
        # set parameters
        model.setParam('OutputFlag', 0)
        model.setParam('timelimit', 5.0)
        model.Params.Method = 2
        # create a 2d binary variable x
        x = model.addVars(self.n, self.m, vtype=GRB.BINARY, name="x")
        # create the maximum completion time variable z
        z = model.addVar(vtype=GRB.CONTINUOUS, name="z")

        # maximum completion time constraint
        for j in range(self.m):
            model.addConstr(gp.quicksum(x[i, j] * self.p[i] for i in range(self.n)) <= z)
        # schedule each job constraint
        for i in range(self.n):
            model.addConstr(gp.quicksum(x[i, j] for j in range(self.m)) == 1)

        # Add the greedy solution as starting values
        for m in range(len(self.T)):
            for n in range(len(self.T[m])):
                x[n, m].Start = self.T[m][n]

        # set objective function
        model.setObjective(z, sense=GRB.MINIMIZE)
        # optimize the model
        model.optimize()
        # we want to minimize the gap
        return model.MIPGap
