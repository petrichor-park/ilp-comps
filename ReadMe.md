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
    - knapsack


# Libmatch
This folder contains a library of classes for "preference havers", including students and courses, and all of the code for our ILP matching.

StudentGenerator.py - creates student and course data
entire_thing.py - automates everything from data generation to graphing results
gale_shapley_emulation.py - An emulation of gale-shapley matching using ILP
graph.py - functions for graphing summary statistics from an ILP matching
hospital_resident_matching.py - original ILP matching implementation that can handle preference ties
is_hrt_matching_stable.py - validates stability of a matching
make_data - automation for generating data
preference_obj.py - data structures for students and courses
readwritetool.py - imports and exports student and course data to CSVs
run_match.py - automation of ILP matching and results
summary_statistics.py - creates metrics from a matching
weighted_cs_match.py - ILP matching that uses weighted preferences


# Stable_Marriage
This folder contains the basics for ILP implementations of stable matching.

direct_inequalities_gusfield.py - ILP implementation of the original Gale-Shapley algorithm
gale_shapely.py - original Gale-Shapley algorithm
is_matching_stable.py - checks whether matching is stable
preferences.py - generates data for simple matching 
weighted_gusfield.py -ILP implementation of the original Gale-Shapley algorithm with weighted preferences

# optimizations 
This folder contains optimizations done to the ILP match.

hrt_reduced_vars.py - ILP matching with less variables generated to solve
timing_comparison.py - collects runtime of original ILP matching and ILP matching with reduced variables

# web
This folder contains all of the code for our website.
