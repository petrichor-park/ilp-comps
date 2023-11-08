from __future__ import annotations
from sys import *
import csv
from preference_obj import Student, Course
from hospital_resident_matching import create_course_preferences

def export_students(student_list: list[Student], filename: str):
    with open(filename, 'x', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for student in student_list:
            csv_writer.writerow(student.get_iterable())
    return None

def import_students(filename: str) -> list[Student]:
    imported_students = []
    with open(filename, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            s_name = row[0]
            s_weights = eval(row[1])
            s_num_required_courses = int(row[2])
            s_num_elective_courses = int(row[3])
            s_class_year = int(row[4])
            s = Student(s_name, s_weights, s_num_required_courses, s_num_elective_courses, s_class_year)
            imported_students.append(s)
    return imported_students

def export_courses(course_list: list[Course], filename: str):
    with open(filename, 'x', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for course in course_list:
            csv_writer.writerow(course.get_iterable())
    return None

def import_courses(filename: str) -> list[Course]:
    imported_courses = []
    with open(filename, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            c_name = row[0]
            c_weights = eval(row[1])
            c_is_elective = eval(row[2])
            c_capacity = int(row[3])
            c = Course(c_name, c_weights, c_is_elective, c_capacity)
            imported_courses.append(c)
    return imported_courses

def find_course(name: str, courselist: list[Course]) -> Course:
    for course in courselist:
        if course.name == name:
            return course
    return None

def import_with_obj_refs(studentfile: str, coursefile: str) -> (list[Student], list[Course]):
    imported_students = import_students(studentfile)
    imported_courses = import_courses(coursefile)
    for student in imported_students:
        new_weights = {}
        for courseID in student.weights:
            real_course = find_course(courseID, imported_courses)
            new_weights[real_course] = student.weights[courseID]
        student.weights = new_weights
    
    core_prefs, elective_prefs = create_course_preferences(imported_students)    
    for course in imported_courses:
        if course.is_elective:
            course.weights = elective_prefs
        else:
            course.weights = core_prefs

    return imported_students, imported_courses