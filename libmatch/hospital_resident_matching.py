from mip import *
from is_hrt_matching_stable import *
from collections import defaultdict
import sys
#sys.path.append("libmatch")
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
            var = model.add_var(name = resident.name + '-' + hospital.name, var_type = BINARY)
            resident_to_hospital_to_vars[resident][hospital] = var
            all_vars.append(var)
    
    # Want to maximize number of residents matched
    model.objective = maximize(xsum(var for var in all_vars))

    # Each resident can only be matched to one hospital
    for resident in residents:
        model += xsum(resident_to_hospital_to_vars[resident][hospital] for hospital in resident_to_hospital_to_vars[resident].keys()) <= 1
    
    # Each hospital can have up to capacity residents
    for hospital in hospitals:
        model += xsum(resident_to_hospital_to_vars[resident][hospital] for resident in resident_to_hospital_to_vars.keys()) <= hospital.capacity
    
    # Want to ensure stable matchings are made based on rankings
    for resident in residents:
        for hospital in hospitals:
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

            model += (hospital.capacity)*(1-xsum(resident_to_hospital_to_vars[resident][hos] for hos in better_hospitals)) <= xsum(resident_to_hospital_to_vars[res][hospital] for res in better_residents)
    
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


def create_course_preferences(students):
    '''
    Takes in information about students and returns a class preference list based on the student information for core classes and electives.
    
    Args:
        students (list(student)): a list of student classes containing information about students

    Returns:
        core class preferences     (dict): a hashmap where keys are students and values are rank of the student
        elective class preferences (dict): a hashmap where keys are students and values are rank of the student
    '''
    core_class_preferences = {}
    elective_class_preferences = {}

    core_sorting = sorted(students, key=lambda student: student.class_year, reverse=True)
    
    core_class_preferences[core_sorting[0]] = 1
    for i in range(1,len(core_sorting)):
        core_class_preferences[core_sorting[i]] = core_class_preferences[core_sorting[i-1]]
        if core_sorting[i].class_year != core_sorting[i-1].class_year:
            core_class_preferences[core_sorting[i]] += 1
        
    elective_sorting = sorted(students, key=lambda student : (student.class_year, -1*student.num_required_courses, student.num_elective_courses), reverse=True)

    elective_class_preferences[elective_sorting[0]] = 1
    for i in range(1,len(elective_sorting)):
        elective_class_preferences[elective_sorting[i]] = elective_class_preferences[elective_sorting[i-1]]
        curStudentAspects = (elective_sorting[i].class_year, -1*elective_sorting[i].num_required_courses, elective_sorting[i].num_elective_courses)
        prevStudentAspects = (elective_sorting[i-1].class_year, -1*elective_sorting[i-1].num_required_courses, elective_sorting[i-1].num_elective_courses)
        if curStudentAspects != prevStudentAspects:
            elective_class_preferences[elective_sorting[i]] += 1
    
    return core_class_preferences, elective_class_preferences