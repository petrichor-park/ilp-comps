# Mary Blanchard, Fall 2023
# ILP Comps Project
# Importing, exporting, and generating preference lists for two groups

from sys import *
import random
import csv


def generate_random_preferences(groupA: list, groupB: list):
    '''Takes in two lists. Generates A's preferences over B. Returns groupA preference list.'''
    if len(groupA) != len(groupB):
        raise Exception("Groups are of different sizes.")
    
    groupA_preferences = {}
    for member in groupA:
        newpreflist = list(groupB)
        random.shuffle(newpreflist)
        groupA_preferences[member] = newpreflist
    
    return groupA_preferences


def generate_random_preferences_both(groupA: list, groupB: list):
    '''Takes in two lists and returns two dictionaries of preference lists.'''
    groupA_preferences = generate_random_preferences(groupA, groupB)
    groupB_preferences = generate_random_preferences(groupB, groupA)

    return groupA_preferences, groupB_preferences


def import_groups(filename: str):
    '''Takes in the filename of a csv, returns two lists.'''
    with open(filename, 'r') as file:
        group_reader = csv.reader(file)
        groupA = group_reader.__next__()
        groupB = group_reader.__next__()
    return groupA, groupB


def import_groups_and_prefs(filename: str):
    '''Takes in the filename of a csv, returns two lists and two dictionaries.'''
    groupA_preferences = {}
    groupB_preferences = {}
    with open(filename, 'r') as file:
        group_reader = csv.reader(file)
        groupA = group_reader.__next__()
        groupB = group_reader.__next__()
        for i in range(len(groupA)):
            member = group_reader.__next__()
            member_pref = group_reader.__next__()
            groupA_preferences[member[0]] = member_pref
        for i in range(len(groupB)):
            member = group_reader.__next__()
            member_pref = group_reader.__next__()
            groupB_preferences[member[0]] = member_pref
    
    return groupA, groupB, groupA_preferences, groupB_preferences


def export_groups_and_prefs(groupA: list, groupB: list, groupA_pref: dict, groupB_pref: dict, filename: str):
    '''Takes in two groups, two dicts, and a destination filename, returns None.'''
    with open(filename, 'x') as file:
        group_writer = csv.writer(file)
        group_writer.writerow(groupA)
        group_writer.writerow(groupB)
        for member in groupA:
            group_writer.writerow([member])
            group_writer.writerow(groupA_pref[member])
        for member in groupB:
            group_writer.writerow([member])
            group_writer.writerow(groupB_pref[member])
    return None