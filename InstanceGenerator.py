import random as r
import gurobipy as gp
from gurobipy import GRB


# Instance generator class
class Tasks:
    def __innit__(self):
        self.n = 2000
        self.m = 50
        self.p = [r.uniform(0, 10) if r.random() < 0.5
                  else r.uniform(25, 35) for _ in range(self.n)]
        self.T = [[0 for _ in range(self.n)] for _ in range(self.m)]

    def Greedy(self, stopping_criteria):
        # solve the instance using the greedy algorithm
        for n in range(stopping_criteria):

            low = float('inf')  # lowest completion time
            machine = 0  # machine with lowest completion time
            # check completion time on each machine
            for m in range(self.m):
                # calculate completion time
                total = sum(m * p for m, p in zip(self.T[m], self.p))
                # if its the lowest store the machine number
                if total < low:
                    low = total
                    machine = m

            # schedule the task on the machine
            self.T[machine][n] = 1

    def ILP_solver(self):
        # creating the ilp solver
        model = gp.Model("min max c")
        # set a time limit of 5 seconds
        model.setParam('timelimit', 5.0)
        model.Params.Method = 2
        # create a 2d binary variable x
        x = model.addVars(self.n, self.m, vtype=GRB.BINARY, name="x")
        # create the maximum completion time variable z
        z = model.addVar(vtype=GRB.CONTINUOUS, name="z")

        # maximum completion time constraint
        for j in range(self.m):
            model.addconstr(gp.quicksum(x[i, j] * self.p[i] for
                                        i in range(self.n)) <= z)

        # schedule each job constraint
        for i in range(self.n):
            model.addconstr(gp.quicksum(x[i, j] for j in range(self.m)) == 1)

        # Add the greedy solution as starting values
        for m in range(len(self.T)):
            for n in range(len(self.T[m])):
                x[n, m].Start = self.T[m][n]

        # set objective function
        model.setobjective(z, sense=GRB.MINIMIZE)
        # optimize the model
        model.optimize()
