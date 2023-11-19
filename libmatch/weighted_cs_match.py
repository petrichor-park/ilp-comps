# Cecilia Ehrlichman, Fall 2023
# ILP Comps Project
# Based on code written by Hugh 

from mip import *
from collections import defaultdict
import sys
sys.path.append("libmatch")
from preference_obj import *
from StudentGenerator import *
from is_hrt_matching_stable import *

def weighted_cs_match(students, courses):
    '''
    Performs an ILP implementation of the course student matching problem with ties, optimizing to maximize student's preference weights.

    Input:
        students (list(student)): a list containing students (which take the student class) to match to courses
        courses (list(course)):  a list containing courses (which take the course class) to match to students
    
    Returns:
        A dictionary of courses containing the students matched to them
    '''

    try:
        model = Model(solver_name=CBC)
    except:
        model = Model(solver_name=GRB)
    
    student_to_course_to_vars = {}
    all_vars = []

    for student in students:
        student_to_course_to_vars[student] = {}
        for course in courses:
            var = model.add_var(name = student.name + '-' + course.name, var_type = BINARY)
            student_to_course_to_vars[student][course] = var
            all_vars.append(var)
    
    # Maximize number of students matched, then maximize weights
    model.objective = maximize(xsum(list(var * 10000 for var in all_vars) + list(student_to_course_to_vars[s][c] * (s.weights[c]) for s in students for c in courses)))

    # Each student can only be matched to one course
    for student in students:
        model += xsum(student_to_course_to_vars[student][course] for course in student_to_course_to_vars[student].keys()) <= 1
    
    # Each course can have up to capacity students
    for course in courses:
        model += xsum(student_to_course_to_vars[student][course] for student in student_to_course_to_vars.keys()) <= course.capacity

    # Ensure stable matchings are made based on rankings
    for student in students:
        for course in courses:
            course_rank = student.weights[course]
            student_rank = course.weights[student]

            better_courses = [] # Find courses that student ranks at least as high
            for hos, weight in student.weights.items():
                if weight >= course_rank:
                    better_courses.append(hos)
            
            better_students = [] # Find students that course finds at least as high
            for stu, weight in course.weights.items():
                if weight >= student_rank:
                    better_students.append(stu)
            model += (course.capacity)*(1-xsum(student_to_course_to_vars[student][c] for c in better_courses)) <= xsum(student_to_course_to_vars[stu][course] for stu in better_students)
    
    model.verbose = False
    model.max_gap = 0.025
    matchings = defaultdict(list)
    status = model.optimize(max_seconds=300)
    if status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE:
        for v in model.vars:
            if abs(v.x) > 1e-6 and '-' in v.name:
                student, course = v.name.split('-')
                matchings[course].append(student)
    
    return matchings