NO_COURSE_PREFERENCE = 'None'

def generate_summary_statistics(matchings, students):
    '''
    Generates summary statistics about a set of matchings of students to courses, including how many students were matched, and to how high of a preference they were matched.

    args:
        matchings (dict): a matching of course names (strings) to the students matched to them (strings, student name)
        students  (list(student)): a list of all students participating in the match
    
    returns:
        summary_statistics (dict): a dict containing several summary statistics about the matching
    '''

    name_to_student = {}
    class_year_counts = {}
    for student in students:
        name_to_student[student.name] = student
        class_year_counts[student.class_year] = class_year_counts.get(student.class_year, 0) + 1
    
    class_years = sorted(class_year_counts.keys())

    matched_students = []
    non_matched_students = []
    matched_to_first_choice = 0
    matched_to_second_choice = 0

    class_year_matching = [0,0,0,0]
    
    for course, course_students in matchings.items():
        if course != NO_COURSE_PREFERENCE:
            for student in course_students:
                matched_students.append(student)
                student_preferences = sorted(name_to_student[student].weights.items(), key=lambda x: x[1], reverse=True)
                # student_preferences = sorted([(c, weight) for c, weight in name_to_student[student].weights.items()], reverse=True)
                if course == student_preferences[0][0].name:
                    matched_to_first_choice += 1
                elif course == student_preferences[1][0].name:
                    matched_to_second_choice += 1
                    student_obj
                student_obj = find_student(student, students)
                class_year_matching[class_years.index(student_obj.class_year)] += 1
        else:
            for student in course_students:
                non_matched_students.append(student)

    
    percentage_students_matched = float(len(matched_students)/len(students))
    num_students_matched = len(matched_students)
    percent_matched_to_first_choice = float(matched_to_first_choice)/len(students)
    percent_matched_to_second_choice = float(matched_to_second_choice)/len(students)

    summary_statistics = {}
    summary_statistics['percentage_students_matched'] = percentage_students_matched
    summary_statistics['num_students_matched'] = num_students_matched
    summary_statistics['percent_matched_to_first_choice'] = percent_matched_to_first_choice
    summary_statistics['percent_matched_to_second_choice'] = percent_matched_to_second_choice
    summary_statistics['num_matched_to_first_choice'] = matched_to_first_choice
    summary_statistics['num_matched_to_second_choice'] = matched_to_second_choice

    summary_statistics['percent_seniors_matched'] = float(class_year_matching[0])/class_year_counts[class_years[0]]
    summary_statistics['percent_juniors_matched'] = float(class_year_matching[1])/class_year_counts[class_years[1]]
    summary_statistics['percent_sophomores_matched'] = float(class_year_matching[2])/class_year_counts[class_years[2]]
    summary_statistics['percent_freshman_matched'] = float(class_year_matching[3])/class_year_counts[class_years[3]]


    return summary_statistics


def find_student(student_name, students):
    for student in students:
        if student.name == student_name:
            return student
    return None