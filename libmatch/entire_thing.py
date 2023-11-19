from StudentGenerator import *
from readwritetool import *
from is_hrt_matching_stable import *
from hospital_resident_matching import *
from gale_shapley_emulation import *
from summary_statistics import *
from readwritetool import *
from graph import * 

'''
    Automates everything from generation of student and course data to graphing results of the ILP matching.

    Args:
        None; string names of output and input student and course CSV's must be edited in the script (lines 21-24)
              ILP matching algorithm to use must be edited in the script (line 28)
    Returns:
        None; exports graph of summary statistics
    '''
st = StudentGenerator(1)
students, courses = st.generate_students(number_of_students=300, add_ties=True)
export_students(students, 'stud.csv')
export_courses(courses, 'cour.csv')
students_filename = 'stud.csv'
courses_filename = 'cour.csv'
objects = import_with_obj_refs(students_filename, courses_filename)
students = objects[0]
courses = objects[1]
matching = hospital_resident_matching(students, courses)

match_status = check_hrt_matching(matching, students, courses)
print()
print("Matching is stable: {}".format(match_status))
print()

summary_statistics = generate_summary_statistics(matching, students)
for metric, value in summary_statistics.items():
    print(metric, value)

basic_graph(summary_statistics)