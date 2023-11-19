NO_COURSE_PREFERENCE = 'None'

def generate_summary_statistics(matchings, students):
    '''
    Generates summary statistics about a set of matchings of students to courses, including how many students were matched, and to how high of a preference they were matched.

    Args:
        matchings (dict): a matching of course names (strings) to the students matched to them (strings, student name)
        students  (list(student)): a list of all students participating in the match
    
    Returns:
        summary_statistics (dict): a dict containing several summary statistics about the matching
    '''

    name_to_student = {}
    class_year_counts = {}
    for student in students:
        name_to_student[student.name] = student
        class_year_counts[student.class_year] = class_year_counts.get(student.class_year, 0) + 1
    
    class_years = sorted(class_year_counts.keys())

    matched_students = []
    matched_to_first_choice = 0
    matched_to_second_choice = 0

    class_year_matching = [0,0,0,0] # Should be exactly 4 years
    
    for course, course_students in matchings.items():
        if course != NO_COURSE_PREFERENCE:
            for student in course_students:
                matched_students.append(student)
                student_preferences = sorted(name_to_student[student].weights.items(), key=lambda x: x[1], reverse=True)
                first_preferences = set() # Accounts for the fact that there can be multiple first choices or second choices
                second_preferences = set()

                first_weight = student_preferences[0][1]
                second_weight = -1
                for other_course, weight in student_preferences:
                    if weight == first_weight:
                        first_preferences.add(other_course.name)
                    elif second_weight == -1 or weight == second_weight:
                        second_preferences.add(other_course.name)
                        second_weight = weight
                    else:
                        break
                # The above code creates the buckets for the first and second choices (highest weights and second highest weight)

                if course in first_preferences:
                    matched_to_first_choice += 1
                elif len(first_preferences) == 1 and course in second_preferences:
                    matched_to_second_choice += 1
                student_obj = find_student(student, students)
                class_year_matching[class_years.index(student_obj.class_year)] += 1 # Want to increment the class year

    
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