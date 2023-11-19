from mip import *
from collections import defaultdict
import sys
sys.path.append("libmatch")
from preference_obj import *

def hospital_resident_matching(residents, hospitals, print_matchings=False):
    '''
    Performs an ILP implementation of the hospital resident matching problem with ties

    Args:
        residents (list(student)): a list containing residents (which take the student class) to match to hospitals
        hospitals (list(course)):  a list containing hospitals (which take the course class) to match to residents
    
    Returns:
        A dictionary of hospitals containing the residents matched to them
    '''

    try:
        model = Model(solver_name=CBC)
    except:
        model = Model(solver_name=GRB)
    
    resident_to_hospital_to_vars = {}
    all_vars = []

    for resident in residents:
        resident_to_hospital_to_vars[resident] = {}
        for hospital in hospitals:
            if resident.weights[hospital] >= 0:
                var = model.add_var(name = resident.name + '-' + hospital.name, var_type = BINARY)
            else: #Unsure of why this step is necessary but it prevents any infeasibilities
                var = model.add_var(name = resident.name + '-' + hospital.name, var_type = BINARY, lb=0, ub=0)
            resident_to_hospital_to_vars[resident][hospital] = var
            all_vars.append(var)
    
    # Want to maximize number of residents matched
    model.objective = maximize(xsum(var for var in all_vars))

    # Each resident can only be matched to one hospital
    for resident in residents:
        model += xsum(resident_to_hospital_to_vars[resident][hospital] if resident.weights[hospital] >= 0 else 0 for hospital in resident_to_hospital_to_vars[resident].keys()) <= 1
    
    # Each hospital can have up to capacity residents
    for hospital in hospitals:
        model += xsum(resident_to_hospital_to_vars[resident][hospital] if resident.weights[hospital] >= 0 else 0 for resident in resident_to_hospital_to_vars.keys()) <= hospital.capacity
    
    # Want to ensure stable matchings are made based on rankings
    for resident in residents:
        for hospital in hospitals:
            if resident.weights[hospital] >= 0:
                hospital_rank = resident.weights[hospital]
                resident_rank = hospital.weights[resident]

                better_hospitals = [] # Find hospitals that resident ranks at least as high
                for hos, weight in resident.weights.items():
                    if weight >= hospital_rank:
                        better_hospitals.append(hos)
                
                better_residents = [] # Find residents that hospital finds at least as high
                for res, weight in hospital.weights.items():
                    if weight >= resident_rank:
                        better_residents.append(res)

                # Ensures that each matching is stable: that if a resident is not matched to a hospital it ranks at least as high, then those hospitals are all filled with better students
                model += (hospital.capacity)*(1-xsum(resident_to_hospital_to_vars[resident][hos] for hos in better_hospitals)) <= xsum(resident_to_hospital_to_vars[res][hospital] if res.weights[hospital] >= 0 else 0 for res in better_residents)
    
    model.verbose = False
    model.max_gap = 0.025
    matchings = defaultdict(list)
    status = model.optimize(max_seconds=300)
    if status == OptimizationStatus.OPTIMAL:
        print('optimal solution cost {} found'.format(model.objective_value))
    elif status == OptimizationStatus.FEASIBLE:
        print('sol.cost {} found, best possible: {}'.format(model.objective_value, model.objective_bound))
    elif status == OptimizationStatus.NO_SOLUTION_FOUND:
        print('no feasible solution found, lower bound is: {}'.format(model.objective_bound))
    if status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE:
        print('solution:')
        for v in model.vars:
            if abs(v.x) > 1e-6 and '-' in v.name:
                resident, hospital = v.name.split('-')
                matchings[hospital].append(resident)
                if print_matchings:
                    print('Matching: {} : {}'.format(resident, hospital))
    
    return matchings