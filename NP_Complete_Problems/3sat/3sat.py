from mip import *

def reduce_3sat_to_ilp(clauses):
    m = Model()
    vars = {}
    for row in clauses:
        # Create variables
        for (varname, _) in row:
            if varname not in vars:
                vars[varname] = m.add_var(name=varname, var_type=BINARY)

        # Each row in CNF needs at least one True value;
        # this is encoded by their sum needing to be more than 1.
        # Every row needs to be True;
        # this is encoded by having a constraint for each row (as the ILP must satisfy all of them)
        constrs = []
        for (varname, negate) in row:
            var = vars[varname]
            # (1 - x) swaps 0 and 1, aka negating in this context
            constrs.append((var) if not negate else (1 - var))
        m += xsum(constrs) >= 1

    return m

def parse(s: str):
    out = []
    for line in s.splitlines():
        line = line.strip()
        if line == "": continue
        splitted = line.split(" ")

        clause = []
        for term in splitted:
            term = term.strip()
            if term.startswith("-"):
                clause.append((term[1:], True)) # Negate
            else:
                clause.append((term, False))
        out.append(clause)
    return out

if __name__ == "__main__":
    # Example problem I got off of https://www.cs.ubc.ca/%7Ehoos/SATLIB/benchm.html
    # and then munged into shape using some sed magic
    clauses = """
 4 -18 19
3 18 -5
-5 -8 -15
-20 7 -16
10 -13 -7
-12 -9 17
17 19 5
-16 9 15
11 -5 -14
18 -10 13
-3 11 12
-6 -17 -8
-18 14 1
-19 -15 10
12 18 -19
-8 4 7
-8 -9 4
7 17 -15
12 -7 -14
-10 -11 8
2 -15 -11
9 6 1
-11 20 -17
9 -15 13
12 -7 -17
-18 -2 20
20 12 4
19 11 14
-16 18 -4
-1 -17 -19
-13 15 10
-12 -14 -13
12 -14 -7
-7 16 10
6 10 7
20 14 -16
-19 17 11
-7 1 -20
-5 12 15
-4 -9 -13
12 -11 -7
-5 19 -8
1 16 17
20 -14 -15
13 -4 10
14 7 10
-5 9 20
10 1 -19
-16 -15 -1
16 3 -11
-15 -10 4
4 -15 -3
-10 -16 11
-8 12 -5
14 -6 12
1 6 11
-13 -5 -1
-7 -2 12
1 -20 19
-2 -13 -8
15 18 4
-11 14 9
-6 -15 -2
5 -12 -15
-6 17 5
-13 5 -19
20 -1 14
9 -17 15
-5 19 -18
-12 8 -10
-18 14 -4
15 -9 13
9 -5 -1
10 -19 -14
20 9 4
-9 -2 19
-5 13 -17
2 -10 -18
-18 3 11
7 -9 17
-15 -6 -3
-2 3 -13
12 3 -2
-2 -3 17
20 -15 -16
-5 -17 -19
-20 -18 11
-9 1 -5
-19 9 17
12 -2 17
4 -16 -5
    """
    clauses = parse(clauses)
    m = reduce_3sat_to_ilp(clauses)

    m.optimize()

    vs = [v for v in m.vars]
    vs.sort(key=lambda x: int(x.name))

    for v in vs:
        print(f"{v.name} : {bool(v.x)}")
