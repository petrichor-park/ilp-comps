from mip import *
import sys
sys.path.append("libmatch")
from preference_obj import *
from StudentGenerator import *
from is_hrt_matching_stable import *
from summary_statistics import *
from gale_shapley_emulation import *
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from weighted_cs_match import *
import numpy as np
import hospital_resident_matching
sys.path.append("../optimizations")
import hrt_reduced_vars


def basic_graph(summary_statistics):
    '''
    Generate a graph for each item in summary statistics which compares each algorithm run.

    Inputs:
    - summary_statistics: dictionary with algorithm name to list of summary statistics

    Output:
    - a graph for each summary statistic catagory (displayed not saved to file)
    '''

    columns = ['Name', 'percentage_students_matched', 'num_students_matched', 'percent_matched_to_first_choice', 'percent_matched_to_second_choice', 'num_matched_to_first_choice', 'num_matched_to_second_choice', 'percent_seniors_matched', 'percent_juniors_matched', 'percent_sophomores_matched', 'percent_freshman_matched']
    lst = []
    for algorithm in summary_statistics:
        for trial in summary_statistics[algorithm]:
            trial_lst = [algorithm] + list(trial.values())
            lst.append(trial_lst)
    df = pd.DataFrame(lst, columns=columns)
    for y in columns[1:]:
        sns.barplot(x = 'Name',
                y = y,
                data = df,
                estimator=np.mean)
        plt.show()

def stacked_plot(summary_statistics, num_students):
    '''
    Generate a stacked bar graph and save to a file named percentage_matched_stacked.svg.

    Inputs:
    - summary_statistics: dictionary with algorithm name to list of summary statistics
    - number of students that were used in these trials

    Output:
    - a graph
    '''
    columns = ['Name', 'percent_matched_to_first_choice', 'percent_matched_to_second_choice', 'percentage_students_matched']
    lst = []
    for algorithm in summary_statistics:
        for i in range(len(summary_statistics[algorithm])):
            trial = summary_statistics[algorithm][i]
            trial_lst = [algorithm] 
            for item in columns[1:]:
                if item == 'percentage_students_matched':
                    trial_lst.append(summary_statistics[algorithm][i][item]*100 - (summary_statistics[algorithm][i]["percent_matched_to_second_choice"]*100 + summary_statistics[algorithm][i]["percent_matched_to_first_choice"]*100))
                else:
                    trial_lst.append(summary_statistics[algorithm][i][item]*100)
            lst.append(trial_lst)
    df = pd.DataFrame(lst, columns=columns, index = list(summary_statistics.keys()))

    ax = df.plot(kind = 'bar', stacked=True, color = ['#61717a', '#8fb8cf', '#bdd1db'])
    ax.set_xticklabels(ax.get_xticklabels(), fontsize=8, rotation=0)
    plt.xlabel('Name')
    plt.xticks(rotation = 0)
    plt.title('Percentages of ' + str(num_students) +  ' Students matched to Corresponding Choice',  fontsize=12)

    plt.tight_layout()
    print("saving...")
    plt.savefig('./percentage_matched_stacked.svg')
    plt.show()


def weight_statistics(matchings, students, courses):
    '''
    Generate weight statistics given a matching. 

    Inputs:
    - matchings: matching of students to courses
    - students: list of students 
    - courses: list of courses

    Output:
    - Graph of weights in the file weighted_preferences.svg
    '''

    columns = ["Name", "Average Student Weighted Preference"]
    lst = []
    for matching in matchings:
        total = 0
        weight = 0
        for course in matchings[matching]:
            course_obj = list(filter(lambda c: c.name == course, courses))[0]
            for student in matchings[matching][course]:
                total += 1
                weight += list(filter(lambda s: s.name == student, students))[0].weights[course_obj]
        lst.append([matching, weight/total])
    df = pd.DataFrame(lst, columns=columns)
    sns.barplot(x = 'Name',
                y = "Average Student Weighted Preference",
                data = df,
                palette = ['#61717a', '#8fb8cf', '#bdd1db'])
    plt.title("Student's Weighted Preferences by Matching")
    plt.savefig('weighted_preferences.svg')

def generate_weight_statistics():
    '''
    Wrapper method to generate weight statistics for 300 students. 

    Inputs:

    Output:
    - Graph of weights in the file weighted_preferences.svg
    '''
    st = StudentGenerator(5) 
    students, courses = st.generate_students(number_of_students=300)
    weight_statistics({"Gale Shapley Emulation": gs_cs_match(students, courses), "Weighted CS Match": weighted_cs_match(students, courses), "Hospital Residents with Ties": hospital_resident_matching(students, courses)}, students, courses)

def generate_summary_statistics_graph(number_of_students=300,add_ties=False,print_statistics=False):
    '''
    Wrapper method to generate stacked bar graph. 

    Inputs:
    - optional: int representing number of students

    Output:
    - graph in the file percentage_matched_stacked.svg
    '''

    dic = {}
    dic["Gale Shapley Emulation"] = []
    dic["Weighted Stable Matching"] = []
    dic["Basic Hospital Resident Matching"] = []
    dic["Hospital Resident Reduced Variables"] = []
    for i in range(1):
        st = StudentGenerator(i) 
        students, courses = st.generate_students(number_of_students=number_of_students, add_ties=add_ties)
        dic["Gale Shapley Emulation"].append(generate_summary_statistics(gs_cs_match(students, courses), students))
        dic["Weighted Stable Matching"].append(generate_summary_statistics(weighted_cs_match(students, courses), students))
        dic["Basic Hospital Resident Matching"].append(generate_summary_statistics(hospital_resident_matching.hospital_resident_matching(students, courses), students))
        dic["Hospital Resident Reduced Variables"].append(generate_summary_statistics(hrt_reduced_vars.hospital_resident_matching(students, courses), students))
        if print_statistics:
            print(dic['Gale Shapley Emulation'])
            print(dic['Weighted Stable Matching'])
            print(dic['Basic Hospital Resident Matching'])
            print(dic['Hospital Resident Reduced Variables'])
        stacked_plot(dic, number_of_students)