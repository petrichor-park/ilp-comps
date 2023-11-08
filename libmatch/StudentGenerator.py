from preference_obj import Student, Course
from hospital_resident_matching import create_course_preferences
import random

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
    total = 0
    for course in weights:
        total += weights[course]
    if (total != 0):
        for course in weights:
            weights[course] = round(weights[course] / total, 3)
    for course in weights:
        if weights[course] == 0:
            weights[course] = -1
    # noneCourse = Course(name="None", weights={}, is_elective=True, capacity=100000)
    weights[noneCourse] = 0
    return weights

class StudentGenerator():
    # TODO: Add option to have ties
    # TODO: Add num_required_courses and num_elective_courses
    def __init__(self, seed = 0) -> None:
        random.seed(seed)

    def generate_student_interval(self, student_distribution = studentDistribution):
        student_interval = {}
        prefix_sum = 0
        for student_type, student_info in student_distribution.items():
            student_interval[student_type] = {}
            student_interval[student_type]['start'] = prefix_sum
            prefix_sum += student_info['percentage_of_students']
            student_interval[student_type]['end'] = prefix_sum
        return student_interval
    
    def generate_random_student_type(self, student_interval):
        random_number = random.uniform(0, 1)
        for student_type, interval in student_interval.items():
            if interval['start'] <= random_number < interval['end']:
                return student_type
        return None

    def generate_student_weights(self, student_type, courseObjects, noneCourse):
        studentWeights = {}
        # print(courseObjects)
        p_num_courses_above_none = studentDistribution[student_type]['mean_of_number_of_courses_above_none'] / len(courseObjects)
        for courseObject in courseObjects:
            weight = random.uniform(0, 1)
            studentWeights[courseObject] = 0 if weight > p_num_courses_above_none else round(weight, 5)
        studentWeights = normalize(studentWeights, noneCourse)
        return studentWeights

    def student_type_to_year(self, student_type, year):
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


    def generate_students(self, number_of_students = 34, list_of_courses = Sp22Courses, student_distribution = studentDistribution, base_year = 2022):
        courseObjects, noneCourse = self.generate_course_objects(list_of_courses)
        students = []
        student_interval = self.generate_student_interval(student_distribution)
        for student_id in range(number_of_students):
            studentName = "S" + str(student_id)
            studentType = self.generate_random_student_type(student_interval)
            num_req_courses, num_elec_courses = self.generate_student_course_history(studentType)
            studentWeights = self.generate_student_weights(studentType, courseObjects, noneCourse)
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
