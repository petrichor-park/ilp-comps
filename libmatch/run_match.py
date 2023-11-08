from is_hrt_matching_stable import *
from hospital_resident_matching import *
from summary_statistics import *
from readwritetool import *


if __name__ == "__main__":
    students_filename = input('Give the name of the students CSV you want to use: ')
    courses_filename = input('Give the name of the courses CSV you want to use: ')
    objects = import_with_obj_refs(students_filename, courses_filename)
    students = objects[0]
    courses = objects[1]
    matching = hospital_resident_matching(students, courses)
    
    match_status = check_hrt_matching(matching, students, courses)
    print()
    print("Matching is stable: {}".format(match_status))
    print()

    for key in matching.keys():
        print("{}: {}".format(key, matching[key]))
    print()

    summary_statistics = generate_summary_statistics(matching, students)
    for metric, value in summary_statistics.items():
        print(metric, value)