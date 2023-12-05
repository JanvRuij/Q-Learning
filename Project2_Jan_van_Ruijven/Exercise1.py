import random as r
import matplotlib.pyplot as plt

# Function to see how much better the applicant is compared to others
def Index(list, Applicant):
    count = 0
    for j in range(len(list)):
        if list[j] > Applicant:
            count += 1
    return count


# Class to generate new games and get the results
class SecretaryGame:
    def __init__(self) -> None:
        self.U = r.uniform(1,  10000)
        self.Applicants = [r.uniform(1,  self.U) for _ in range(12)]

    def Hire_Value(self,  value) -> float:
        return float(value) / max(self.Applicants)


# Greedy strategy based on averages
Result_Sum = 0
eps = 100000
Average_Multiplier = [5, 4, 3, 2, 1.5, 1.25, 1.2, 1.15, 1.1, 1.05, 1, 1]
for j in range(eps):
    newGame = SecretaryGame()
    Average = 0
    Average_Sum = 0
    Sum = 0
    Count = 1
    nr_hired = 0
    for Applicant in newGame.Applicants:
        # Never hire the first applicant
        if Count == 1:
            pass

        # Compare app  licant value with its multiplier value
        # If good enough we hire
        elif Applicant > Average * Average_Multiplier[Count-1]:
            # We take the applicant
            Sum += newGame.Hire_Value(Applicant)
            nr_hired += 1

        Count += 1
        Average_Sum += Applicant
        Average = Average_Sum / Count
    if nr_hired != 0:
        Result_Sum += Sum / nr_hired

print("Greedy average value strategy result: {}".format(Result_Sum/eps))

# Greedy highest value strategy
Result_Sum = 0
for j in range(eps):
    newGame = SecretaryGame()
    highest = 0
    Sum = 0
    Count = 1
    nr_hired = 0
    for Applicant in newGame.Applicants:
        # Never hire the first applicant
        if Count == 1:
            pass

        # Compare applicant value with the highest value
        # If good enough we hire
        elif Applicant > highest:
            # We take the applicant
            Sum += newGame.Hire_Value(Applicant)
            nr_hired += 1
        Count += 1

        # Keep track of highest value
        if Applicant > highest:
            highest = Applicant

    if nr_hired != 0:
        Result_Sum += Sum / nr_hired

print("Greedy highest value strategy result: {}".format(Result_Sum/eps))


# Q-Learning Strategy
# Create the Q-table
Q = [[float(0) for _ in range(i+1)] for i in range(12)]
alpha_values = [i / 100 for i in range(20)]
result_values = []
for alpha in range(0, 20):
    alpha = alpha / 100
    Result_Sum = 0
    for j in range(eps):
        newGame = SecretaryGame()
        Count = 0
        Sum = 0
        nr_hired = 0
        Seen_Candidates = []
        for Applicant in newGame.Applicants:
            if Seen_Candidates == []:
                Seen_Candidates.append(Applicant)
                Count += 1
                continue
            Seen_Candidates.append(Applicant)
            index = Index(Seen_Candidates,  Applicant)
            # Compare candidate value with Q-table
            # If candidate is good enough we hire
            if Applicant/max(Seen_Candidates) > Q[Count][index]:
                value = newGame.Hire_Value(Applicant)
                Sum += value
                nr_hired += 1
                Q[Count][index] = Q[Count][index]*(1-alpha) + value * alpha
            Count += 1
        if nr_hired != 0:
            Result_Sum += Sum/nr_hired
    print("Q-Learning result for alpha {}: {}".format(alpha, Result_Sum/eps))
    result_values.append(Result_Sum/eps)

plt.plot(alpha_values, result_values, marker='o', linestyle='-')
plt.title('Q-learning Results vs Alpha')
plt.xlabel('Alpha')
plt.ylabel('Q-learning Results')
plt.grid(True)
plt.show()

