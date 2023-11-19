# Cecilia Ehrlichman, Fall 2023
# ILP Comps Project

from mip import *
from is_matching_stable import *
from preferences import *
from gale_shapley import *

def stable_matching(man_preferences, woman_preferences, optimize = None):
    '''
        Returns a matching given preferences for men and women.

        Inputs:
        - man_preferences: a dictionary storing a woman to her list of preferences
        - woman_preferences: a dictionary storing a man to his list of preferences

        Returns:
        - a list of tuples representing (m, w) pairs
    '''
    
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
            w_pref_sets[m][w] = woman_preferences[w][i+1:]
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

    if optimize == 'm':
        model.objective = xsum(x[m][w] * man_preferences[m].index(w) for m in men for w in women)
    elif optimize == "w":
        model.objective = xsum(x[m][w] * woman_preferences[w].index(m) for m in men for w in women)

    if optimize == 'm':
        model.objective = xsum(x[m][w] * man_preferences[m].index(w) for m in men for w in women)
    elif optimize == "w":
        model.objective = xsum(x[m][w] * woman_preferences[w].index(m) for m in men for w in women)

    model.verbose = False
    model.optimize()
    
    
    # store the results in a list
    output = []
    for w in women:
        for m in men:
            if x[m][w].x == 1:
                output.append((m, w))
    return output