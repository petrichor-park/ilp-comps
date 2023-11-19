from preference_obj import Student, Course
from hospital_resident_matching import create_course_preferences
import random

'''
The state whether Carleton's CS courses are electives or not. Data is from the Carleton CS website. Used in StudentGenerator.py as a global constant.
'''
isCourseElective =  {
    'CS202': False,
    'CS208': False,
    'CS231': True,
    'CS232': True,
    'CS251': False,
    'CS252': False,
    'CS254': False,
    'CS257': False,
    'CS294': True,
    'CS298': True,
    'CS301': True,
    'CS304': True,
    'CS311': True,
    'CS314': True,
    'CS318': True,
    'CS320': True,
    'CS321': True,
    'CS322': True,
    'CS331': True,
    'CS332': True,
    'CS334': True,
    'CS338': True,
    'CS341': True,
    'CS344': True,
    'CS347': True,
    'CS348': True,
    'CS352': True,
    'CS358': True,
    'CS361': True,
    'CS362': True,
}

'''
The CS classes included in Carleton's CS Match for Spring 2023 and their capacities. Used in StudentGenerator.py as a function parameter. Data is obtained from Professor David Musicant.
'''
Sp22Courses = [
    {
        "courseName": 'CS202',
        "capacity": 34
    },
    {
        "courseName": 'CS208',
        "capacity": 34
    },
    {
        "courseName": 'CS251',
        "capacity": 34
    },
    {
        "courseName": 'CS252',
        "capacity": 34
    },
    {
        "courseName": 'CS254',
        "capacity": 34
    },
    {
        "courseName": 'CS257',
        "capacity": 34
    },
    {
        "courseName": 'CS338',
        "capacity": 34
    },
    {
        "courseName": 'CS344',
        "capacity": 34
    },
    {
        "courseName": 'CS352',
        "capacity": 34
    },
]

'''
Summary statistics of Carleton's 2023 CS Match. StudentGenerator.py as a function parameter. Data is obtained from Professor David Musicant.
'''
studentDistribution = {
    'Freshman': {
        'percentage_of_students': 0.159,
        'mean_of_number_of_courses_above_none': 3.736,
    },
    'Sophomore': {
        'percentage_of_students': 0.314,
        'mean_of_number_of_courses_above_none': 4.708,
    },
    'Junior': {
        'percentage_of_students': 0.279,
        'mean_of_number_of_courses_above_none': 3.329,
    },
    'Senior': {
        'percentage_of_students': 0.248,
        'mean_of_number_of_courses_above_none': 2.229,
    },
}

def normalize(weights, noneCourse):
    '''
    Normalizes the weights of a student's preferences so that the sum of weights of selected courses equals to 1. If a course hasn't been chosen, the weights are set to -1. None course is also added to the weights dict with a weight of 0.

    args:
        weights (dict): a dict of Course objects to weights
        noneCourse: a Course object that represents the "None" course
    
    returns:
        weights (dict): a dict of Course objects to weights that have been normalized
    '''
    total = 0
    for course in weights:
        total += weights[course]
    if (total != 0):
        for course in weights:
            weights[course] = weights[course] / total
    for course in weights:
        if weights[course] == 0:
            weights[course] = -1
    # noneCourse = Course(name="None", weights={}, is_elective=True, capacity=100000)
    weights[noneCourse] = 0
    return weights

class StudentGenerator():
    '''
    A class that contains functions to generate student preferences.
    '''

    def __init__(self, seed = 0) -> None:
        random.seed(seed)

    def generate_student_interval(self, student_distribution = studentDistribution):
        '''
        Generates a dict of student type to a dict of start and end interval of the percentage of students that are of that type.

        args:
            student_distribution (dict): a dict of student type to a dict of percentage of students and mean of number of courses above none

        returns:
            student_interval (dict): a dict of student type to a dict of start and end interval of the percentage of students that are of that type
        '''
        student_interval = {}
        prefix_sum = 0
        for student_type, student_info in student_distribution.items():
            student_interval[student_type] = {}
            student_interval[student_type]['start'] = prefix_sum
            prefix_sum += student_info['percentage_of_students']
            student_interval[student_type]['end'] = prefix_sum
        return student_interval
    
    def generate_random_student_type(self, student_interval):
        '''
        Generates a random student type based on the student interval.

        args:
            student_interval (dict): a dict of student type to a dict of start and end interval of the percentage of students that are of that type

        returns:
            student_type (str): a random student type
        '''
            
        random_number = random.uniform(0, 1)
        for student_type, interval in student_interval.items():
            if interval['start'] <= random_number < interval['end']:
                return student_type
        return None

    def add_ties(self, weights):
        '''
        Randomly adds ties to a student's preferences. 50% chance of adding ties when the student has multiple choices.

        args:
            weights (dict): a dict of Course objects to weights

        returns:
            weights (dict): a dict of Course objects to weights that could've been modified to add ties
        '''
        list_selected_courses = []
        for course in weights:
            if (weights[course] != 0):
                list_selected_courses.append(course)
        
        if (len(list_selected_courses) > 1 and (random.uniform(0, 1) < 0.5)):
            random.shuffle(list_selected_courses)
            equal_weight = (weights[list_selected_courses[0]] + weights[list_selected_courses[1]]) / 2
            weights[list_selected_courses[0]] = equal_weight
            weights[list_selected_courses[1]] = equal_weight

    def generate_student_weights(self, student_type, courseObjects, noneCourse, add_ties=False):
        '''
        Generates a dict of Course objects to weights for a student.
        
        args:
            student_type (str): a student type
            courseObjects (list): a list of Course objects
            noneCourse: a Course object that represents the "None" course
            add_ties (bool): whether to add ties or not

        returns:
            studentWeights (dict): a dict of Course objects to weights for a student
        '''

        studentWeights = {}
        p_num_courses_above_none = studentDistribution[student_type]['mean_of_number_of_courses_above_none'] / len(courseObjects)
        added_weight = False
        while (not added_weight):
            for courseObject in courseObjects:
                weight = random.uniform(0, 1)
                if weight > p_num_courses_above_none:
                    studentWeights[courseObject] = 0
                else:
                    added_weight = True
                    studentWeights[courseObject] = weight

        if add_ties:
            self.add_ties(studentWeights)

        studentWeights = normalize(studentWeights, noneCourse)
        return studentWeights

    def student_type_to_year(self, student_type, year):
        '''
        Converts a student type to a class year.
        '''
        if student_type == 'Freshman':
            return year + 4
        elif student_type == 'Sophomore':
            return year + 3
        elif student_type == 'Junior':
            return year + 2
        elif student_type == 'Senior':
            return year + 1
        else:
            return None

    def generate_course_objects(self, list_of_courses = Sp22Courses):
        '''
        Generates a list of Course objects from a list of courses.
        '''

        coursesObjects = []
        for course in list_of_courses:
            courseName = course["courseName"]
            courseCapacity = course["capacity"]
            courseIsElective = isCourseElective[courseName]
            course = Course(name=courseName, weights={}, is_elective=courseIsElective, capacity=courseCapacity)
            # print(course.name)
            coursesObjects.append(course)
        noneCourse = Course(name="None", weights={}, is_elective=True, capacity=100000)
        return (coursesObjects, noneCourse)

    def generate_student_course_history(self, student_type):
        '''
        Generates the number of required and elective courses for a student based on their student class year.
        '''
        num_required_courses = 0
        num_elective_courses = 0

        if student_type == 'Freshman':
            num_elective_courses = random.choice([0, 1])
            num_required_courses = random.choice([0, 1, 2])
        elif student_type == 'Sophomore':
            num_elective_courses = random.choice([0, 1, 2, 4, 5])
            num_required_courses = random.choice([1, 2, 3, 4, 5])
        elif student_type == 'Junior':
            num_elective_courses = random.choice([0, 1, 2, 4, 5, 6])
            num_required_courses = random.choice([3, 4, 5, 6])
        elif student_type == 'Senior':
            num_elective_courses = random.choice([2, 3, 4, 5, 6])
            num_required_courses = random.choice([4, 5, 6])

        return (num_required_courses, num_elective_courses)

    def generate_students(self, number_of_students = 34, list_of_courses = Sp22Courses, student_distribution = studentDistribution, base_year = 2022, add_ties = False):
        '''
        Generates a list of Student objects and a list of Course objects.

        args:
            number_of_students (int): the number of students to generate
            list_of_courses (list): a list of courses. Default is Spring 2022 CS courses
            student_distribution (dict): a dict of student type to a dict of percentage of students and mean of number of courses above none
            base_year (int): the base year of the students
            add_ties (bool): whether to add ties or not
        
        returns:
            students (list): a list of Student objects
            courseObjects (list): a list of Course objects
        '''
        courseObjects, noneCourse = self.generate_course_objects(list_of_courses)
        students = []
        student_interval = self.generate_student_interval(student_distribution)
        for student_id in range(number_of_students):
            studentName = "S" + str(student_id)
            studentType = self.generate_random_student_type(student_interval)
            num_req_courses, num_elec_courses = self.generate_student_course_history(studentType)
            studentWeights = self.generate_student_weights(studentType, courseObjects, noneCourse, add_ties)
            studentYear = self.student_type_to_year(studentType, base_year)
            student = Student(name=studentName, class_year = studentYear, num_required_courses=num_req_courses, num_elective_courses=num_elec_courses, weights=studentWeights)
            students.append(student)
        core_prefs, elective_prefs = create_course_preferences(students)
        
        courseObjects.append(noneCourse)

        for courseObject in courseObjects:
            if courseObject.is_elective:
                courseObject.weights = elective_prefs
            else:
                courseObject.weights = core_prefs

        return students, courseObjects
