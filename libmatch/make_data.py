from StudentGenerator import *
from readwritetool import *

st = StudentGenerator()
students, courses = st.generate_students(number_of_students=100)
export_students(students, 'stud100.csv')#define student csv file name here
export_courses(courses, 'cour100.csv')#define student csv file name here
