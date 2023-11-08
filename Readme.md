# ILP Library
This repository contains a library of files that allow a user to run ILP implementations of stable matching in addition to several known NP-Complete problems.

# NP_Complete_Problems

This folder contains a bunch of ILP-based implementations of famous NP-complete problems.

Problems included:

- 3-SAT
- Subset sum
- Travelling salesperson problem
- Hamiltonian circuit
- k-clique


# Libmatch

This is where the main code of our project lives. It is in two main parts: generation and serialization
of fake student preference data, and several ILP-based Match solvers that take in student preferences
and return matches.

Theoretically, if this were to ever be used by the CS department, they would ignore the generation
code and just give the algorithms what the real students actually chose. (Because we were unable to
get real preference lists for privacy reasons, we had to generate our own.)

Files for generating fake data:

- `StudentGenerator.py` generates the fake data. It generates a corpus of fake students, with their
grades, class preferences, and other information, and corpus of classes based on hard-coded class size
information.
- `readwritetool.py` is a utility file that reads and writes student and course information from csv files.
- `make_data.py` is a small "glue" file that just generates data with `StudentGenerator` and stores it
to a csv file with `readwritetool`.

Files for solving the Match:

- `preference_obj.py` defines the `PreferenceHaver` class, and its two subclasses `Student` and `Course`.
- `gale_shapley_emulation.py`, `hospital_resident_matching.py`, and `weighted_cs_match.py` are three
different ILP-based ways to solve the Match. 
- `is_hrt_stable.py` has a function to check if a hospital resident matching-style Match has any unstable
matchings, as a debugging tool.
- `run_match.py` is a command-line tool that runs the Match on the given CSV files. It's currently hard-coded
to use the HRT-based algorithm, but we frequently switched algorithms through development.
- `summary_statistics.py` calculates some statistics about a Match result, like the number of students
matched to their first course.
- `graph.py` uses matplotlib to display the `summary_statistics` as graphs.

# Stable_Marriage

This folder contains our earlier experiments into using ILP for stable matching.

- `direct_inequalities_gusfield` contains an ILP implementation of the basic Gale-Shapley stable matching
algorithm.
- `gale_shapley` is a more standard implementation of the Gale-Shapley algorithm.
- `hospital_resident_matching` is an ILP version of stable matching that allows ties in preference lists
and courses to contain multiple students, based on the hospital resident matching problem.
- `is_matching_stable` assesses a matching and determines whether the matching is stable.

# Optimizations

This folder implements the HRT-based ILP solver but more aggressively removes constraints that aren't
relevant before inserting them into the model. As it turns out, this also fixed a bug with the original
HRT solver. The version in libmatch is based on this.
