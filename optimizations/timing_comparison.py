import sys
import os
sys.path.append("../libmatch")
from is_hrt_matching_stable import *
import hospital_resident_matching
import hrt_reduced_vars
from summary_statistics import *
from StudentGenerator import *
from readwritetool import *
from time import monotonic

NUMBERS_OF_STUDENTS_TO_TEST = [100,150,200,250,300]


if __name__ == '__main__':

    timing = {}
    for i in NUMBERS_OF_STUDENTS_TO_TEST:
        st = StudentGenerator() 
        students, courses = st.generate_students(number_of_students=i)

        timing[i] = {}

        timing[i]['regular'] = {}
        timing[i]['reduced'] = {}
        
        timing[i]['regular']['time'] = 0

        # Find and store timings and statistics for the regular version of the hrt
        for j in range(30):
            start = monotonic()
            matching = hospital_resident_matching.hospital_resident_matching(students, courses)
            end = monotonic()

            timing[i]['regular']['time'] += end-start

        timing[i]['regular']['time'] /= 30 #average timing results
        match_status = check_hrt_matching(matching, students, courses) #check for stability
        timing[i]['regular']['stability'] = match_status

        regular_summary = generate_summary_statistics(matching, students)

        # Find and store timings and statistics for the reduced version of the hrt
        timing[i]['reduced']['time'] = 0
        for j in range(30):
            start = monotonic()
            matching = hrt_reduced_vars.hospital_resident_matching(students, courses)
            end = monotonic()

            timing[i]['reduced']['time'] += end-start

        timing[i]['reduced']['time'] /= 30 #average timing results
        match_status = check_hrt_matching(matching, students, courses) #check for stability
        timing[i]['reduced']['stability'] = match_status

        reduced_summary = generate_summary_statistics(matching, students)

        timing[i]['regular_summary'] = regular_summary
        timing[i]['reduced_summary'] = reduced_summary
    
    for i in NUMBERS_OF_STUDENTS_TO_TEST:
        print("Matchings for {} students:".format(i))
        print("Timing: ")
        print("Regular HRT: {} seconds".format(timing[i]['regular']['time']))
        print("Reduced HRT: {} seconds".format(timing[i]['reduced']['time']))
        print('Stability: ')
        print("Regular HRT: {}".format(timing[i]['regular']['stability']))
        print("Reduced HRT: {}".format(timing[i]['reduced']['stability']))

        regular_summary = timing[i]['regular_summary']
        reduced_summary = timing[i]['reduced_summary']

        if regular_summary == reduced_summary:
            print('Matchings were similar for both algorithms')
        else:
            print('WARNING: Matchings were not similar for both algorithms')
            for key, value in regular_summary.items(): #Find the nonequal summary statistics values
                if value != reduced_summary[key]:
                    print("The values of {} do not match: Regular: {}, Reduced: {}".format(key, value, reduced_summary[key]))

        print()
    





