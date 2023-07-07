import matplotlib.pyplot as plt
import numpy as np
import sklearn
from sklearn.linear_model import LinearRegression

file = open('survey.txt', 'r')

data = file.readlines()

print(data)

empty = [0 for i in range(100)]
# FIRST: God, THEN: ETs

LIST = {"male", "female", "other",
             "no-college", "some-college", "college-degree", "adv-degree",
             "less-18", "18-24", "25-34", "35-49", "50-65", "great-65",
        "EVERYONE"}

info = {}

for item in LIST:
    info[item] = empty[:]

raw_numbers = {}
for item in LIST:
    raw_numbers[item] = [[], []]
    
ets_ = []
god_ = []
for i in range(10):
    for j in range(10):
        ets_.append(i+1)
        god_.append(j+1)
'''
ETS: 1 1 1 1 ...
GOD: 1 2 3 4 ...

so to get to (E, G), use E * 10 + G
'''

for i in range(len(data)):
    age = data[i]
    if age.startswith('age group'):
        gender = data[i+1]
        god = data[i+2]
        educ = data[i+3]
        ets = data[i+4]

        if god[8:]:
            godnum = int(god[8:])
            etsnum = int(ets[8:])

            agegr = age[10:-1]
            gendergr = gender[7:-1]
            educgr = educ[10:-1]

            index_to_hit = (etsnum-1) * 10 + (godnum - 1)

            for item in {agegr, gendergr, educgr}:
                if item:
                    info[item][index_to_hit] += 25
                    raw_numbers[item][0] += [etsnum]
                    raw_numbers[item][1] += [godnum]
                    
            raw_numbers["EVERYONE"][0] += [etsnum]
            raw_numbers["EVERYONE"][1] += [godnum]
            info["EVERYONE"][index_to_hit] += 25

cat = { "Gender": ['male', 'female', 'other'],
        "Education": ['no-college', "some-college", "college-degree", "adv-degree"],
        "Age": ["less-18", "18-24", "25-34", "35-49", "50-65", "great-65"]}

for item in LIST:
    category = ""
    for c in cat:
        if item in cat[c]:
            category = c

    '''
    x_ets = raw_numbers[item][0]
    y_god = raw_numbers[item][1]
    slope, intercept = np.polyfit(x_ets, y_god, 1)

    print(np.corrcoef(x_ets, y_god)[0,1])

    start = 1
    end = 10
    line1 = np.array([start, end])
    line2 = np.array([intercept + start * slope, intercept + end * slope])

    plt.clf()
    plt.figure(figsize=(6, 6))
    plt.plot(line1, line2)

    plt.scatter(ets_, god_, s=info[item])
    plt.xlabel("Belief in ETs")
    plt.ylabel("Belief in God")
    title_ = "EVERYONE" if item == "EVERYONE" else f"{category} {item}"
    plt.title(f"Belief in God vs ETs, {title_} (sample size {len(x_ets)})")
    plt.savefig(f"{title_}.png")
    '''

    choice = raw_numbers[item][1] # 1 for God, 0 for ETs
    plt.clf()
    plt.hist(choice)
    plt.xlabel("Belief in God (1 = weakest, 10 = strongest)")
    plt.ylabel("Number of Respondents")
    title_ = "EVERYONE" if item == "EVERYONE" else f"{category} {item}"
    plt.title(f"Belief in God, {title_} (sample size {len(choice)})")
    plt.savefig(f"God {title_}.png")
    
