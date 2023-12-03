import random as r


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
        self.Applicants = [r.uniform(1,  self.U) for _ in range(10)]

    def Hire_Value(self,  value) -> float:
        return float(value) / max(self.Applicants)


# Greedy strategy based on averages
Result_Sum = 0
eps = 10000
Average_Multiplier = [5, 4, 3, 2, 1, 0.75, 0.5, 0.25, 0.125, 0.0075]
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

        # Compare applicant value with its multiplier value
        # If good enough we hire
        elif Applicant > Average * Average_Multiplier[Count-1]:
            # We take the applicant
            Sum += newGame.Hire_Value(Applicant)
            nr_hired += 1

        Count += 1
        Average_Sum += Applicant
        Average = Average_Sum / Count
    Result_Sum += Sum / nr_hired

#testcomment22
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


# Parameters
alpha = 0.1


# Q-Learning Strategy
Result_Sum = 0
# Create the Q-table
Q = [[float(0) for _ in range(i+1)] for i in range(10)]
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
            break
        Count += 1
    Result_Sum += Sum


print("Q-Learning result: {}".format(Result_Sum/eps))
print(Q)
