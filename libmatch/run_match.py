from is_hrt_matching_stable import *
from hospital_resident_matching import *
from summary_statistics import *
from readwritetool import *
sys.path.append("../optimizations")
import hrt_reduced_vars

if __name__ == "__main__":
    '''
    Automates import of student and course CSV's, ILP matching, stability checking, and generation of summary statistics

    Args:
        None; string names of input student and course CSV's must be edited in the script (lines 18-19)
              ILP matching algorithm to use must be edited in the script (line 23)
    Returns:
        None; prints summary statistics
    '''
    students_filename = 'students.csv'
    courses_filename = 'courses.csv'
    objects = import_with_obj_refs(students_filename, courses_filename)
    students = objects[0]
    courses = objects[1]
    matching = hrt_reduced_vars.hospital_resident_matching(students, courses)
    
    match_status = check_hrt_matching(matching, students, courses)
    print()
    print("Matching is stable: {}".format(match_status))
    print()

    # for key in matching.keys():
    #     print("{}: {}".format(key, matching[key]))
    # print()

    summary_statistics = generate_summary_statistics(matching, students)
    for metric, value in summary_statistics.items():
        print(metric, value)