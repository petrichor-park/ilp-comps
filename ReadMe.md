# ILP Library
This repository contains a library of files that allow a user to run ILP implementations of stable matching in addition to several known NP-Complete problems.

# NP_Complete_Problems
This folder contains subfolders which in turn contain ILP solutions to NP-Complete problems.
Problems included:
    - 3 SAT
    - Subset sum
    - Travelling salesperson problem
    - Hamiltonian circuit
    - k-clique


# Libmatch
This folder contains a library of classes for "preference havers", including students and courses.

Preference havers have a dictionary of preferences, including weights.

Students have class years, number of courses taken, number of electives taken, and inherit from preference havers.

Courses can either be an elective or a required course, and inherit from preference havers.

By assembling a collection of students and courses, we can then match the students to courses.


# Stable_Marriage

This folder contains the basics for ILP implementations of stable matching.

direct_inequalities_gusfield contains an ILP implentation of the Gale-Shapley stable matching algorithm, that can be given two lists of preference havers which are then matched to each other.

gale_shapley is a pure implementation of Gale-Shapley that matches two preference havers together

hospital_resident_matching is an ILP version of stable matching that allows ties in preference lists and courses to contain multiple students

is_matching_stable assesses a matching and determines whether the matching is stable

