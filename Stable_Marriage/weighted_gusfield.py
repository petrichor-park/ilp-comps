# Cecilia Ehrlichman, Fall 2023
# ILP Comps Project

from mip import *
from is_matching_stable import *
from preferences import *
from gale_shapley import *
from direct_inequalities_gusfield import *
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt 

def weighted_stable_matching(man_preferences, man_weighted_preferences, woman_preferences, woman_weighted_preferences):

    men = man_preferences.keys()
    women = woman_preferences.keys()

    # validate there are the same number of men and women
    if not len(men) == len(women):
        return []
    
    n = len(men)
    model = Model()

    # create the variables
    # x[m][w] = 1 represents m and w are married
    # x[m][w] = 0 represents m and w are not married
    x = {}
    for m in men:
        for w in women:
            if not m in x.keys():
                x[m] = {}
                x[m][w] = model.add_var(var_type=BINARY)
            else:
                x[m][w] = model.add_var(var_type=BINARY)

    # w_pref_sets[m][w] are all the men that woman w prefers less m
    w_pref_sets = {}
    # m_pref_sets[m][w] are all the woman that man m prefers to w
    m_pref_sets = {}
    
    for w in women:
        for m in men:
            if not m in w_pref_sets.keys():
                w_pref_sets[m] = {}
            if not m in m_pref_sets.keys():
                m_pref_sets[m] = {}
            # set w_pref_sets to all the men that w prefer to m
            i = woman_preferences[w].index(m)
            w_pref_sets[m][w] = woman_preferences[w][i+1:]
            # set m_pref_set to all the women that m prefer to w
            i = man_preferences[m].index(w)
            m_pref_sets[m][w] = man_preferences[m][:i]

    # each man marries one woman
    for m in men:
        model += xsum(x[m][w] for w in women) == 1

    # each woman marries one man
    for w in women:
        model += xsum(x[m][w] for m in men) == 1
    
    # no blocking pairs
    for w in women:
        for m in men:
            model += xsum(x[m_prime][w] for m_prime in w_pref_sets[m][w]) - xsum(x[m][w_prime] for w_prime in m_pref_sets[m][w]) <= 0
    
    model.objective = xsum(-x[m][w] * woman_weighted_preferences[w][m-1][1] for m in men for w in women)

    model.verbose = False
    model.optimize()
    
    # store the results in a list
    output = []
    for w in women:
        for m in men:
            if x[m][w].x == 1:
                output.append((m, w))
    return output

def generate_random_weights(men, women):
    man_weighted_preferences = {}
    woman_weighted_preferences = {}
    for m in men:
        for w in women:
            if m not in man_weighted_preferences:
                man_weighted_preferences[m] = {}
            if w not in woman_weighted_preferences:
                woman_weighted_preferences[w] = {}
            man_weighted_preferences[m][w] = random.uniform(1, 100)
            woman_weighted_preferences[w][m] = random.uniform(1, 100)
    
    for m in men:
        s = sum(man_weighted_preferences[m].values())
        for w in women:
            man_weighted_preferences[m][w] = man_weighted_preferences[m][w] * 100 / float(s)
    for w in women:
        s = sum(woman_weighted_preferences[w].values())
        for m in men:
            woman_weighted_preferences[w][m] = man_weighted_preferences[w][m] * 100 / float(s)

    for m in men:
        man_weighted_preferences[m] = sorted(man_weighted_preferences[m].items(), key=lambda x:-x[1])
    for w in women:
        woman_weighted_preferences[w] = sorted(woman_weighted_preferences[w].items(), key=lambda x:-x[1])
    
    man_preferences = {}
    woman_preferences = {}

    for m in man_weighted_preferences.keys():
        man_preferences[m] = list(map(lambda x: x[0], man_weighted_preferences[m]))
    for w in woman_weighted_preferences.keys():
        woman_preferences[w] = list(map(lambda x: x[0], man_weighted_preferences[w]))

    return man_weighted_preferences, man_preferences,  woman_weighted_preferences, woman_preferences

if __name__ == "__main__":
    random.seed(1)
    x = []
    y = []
    print("Starting")
    for j in range(1, 100, 5):
        print(j)
        x.append(j)
        men = range(1, j + 1)
        women = range(1, j + 1)
        n = 10
        counter = 0 
        for i in range(n):
            prefs = generate_random_weights(men, women)
            wsm = weighted_stable_matching( prefs[1], prefs[0], prefs[3] , prefs[2])
            osm = stable_matching( prefs[1], prefs[3] , "w")
            if not (is_matching_stable(wsm,  prefs[1], prefs[3]) or is_matching_stable(osm,  prefs[1], prefs[3])):
                print("uh oh")
            if osm == wsm:
                counter += 1
        y.append(counter / float(n))
    data_plot = pd.DataFrame({"Number of Men and Women":x, "Percent of identical matchings between weighted and unweighted":y})
    sns.regplot(x = "Number of Men and Women", y = "Percent of identical matchings between weighted and unweighted", data=data_plot).set(title='Difference Between Weighted and Unweighted Stable Matchings with Optimization for Women\'s Preferences')
    plt.savefig("weighted_vs_unweighted.png")
    print(x, y)