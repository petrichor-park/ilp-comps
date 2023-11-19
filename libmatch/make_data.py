from StudentGenerator import *
from readwritetool import *

'''
    Automates data generation of students and courses and saves them to CSVs.

    Args:
        None; string names of output student and course CSV's must be edited in the script (lines 14-15)
    Returns:
        None
    '''
st = StudentGenerator()
students, courses = st.generate_students(number_of_students=100)
export_students(students, 'stud100.csv')#define student csv file name here
export_courses(courses, 'cour100.csv')#define student csv file name here
