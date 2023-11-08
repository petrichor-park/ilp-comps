from mip import *

print("Beginning...")

vertices = [0, 1, 2, 3, 4, 5]
edges = [(0, 2), (0, 4), (0, 5), (1, 4), (1, 5), (2, 4), (4, 5), (3, 2), (2, 5)]
graph = (vertices, edges)

#vertices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
#edges = [(0, 2), (0, 4), (0, 5), (1, 4), (1, 5), (2, 4), (4, 5), (3, 2), (2, 5), (15, 30), (30, 29), (29, 6), (30, 6), (6, 18), (18, 17), (14, 1), (1, 19), (1, 9), (9, 29), (29, 12), (15, 12), (12, 26), (12, 25), (12, 10), (12, 16), (16, 30), (30, 8), (8, 16), (16, 28), (7, 16), (16, 13), (13, 3), (3, 27), (27, 26), (25, 26), (26, 24), (11, 25), (0, 23), (22, 11), (11, 0), (11, 10), (10, 9), (9, 4), (4, 21), (21, 19), (19, 9), (9, 21), (21, 20), (20, 9), (9, 5), (5, 12), (12, 2), (2, 11), (11, 23), (23, 2), (2, 22), (22, 5), (5, 29), (29, 1), (1, 17), (17, 14), (14, 6), (6, 29), (29, 15), (15, 5), (5, 26), (26, 13), (13, 24), (24, 11), (11, 14), (14, 13), (13, 20), (20, 28), (28, 18), (18, 29), (29, 22), (22, 8), (8, 26), (26, 9), (9, 2), (2, 14), (14, 13), (13, 25), (25, 0), (0, 7)]
#graph = (vertices, edges)

k = 3

m = Model()

v = [m.add_var(var_type = BINARY) for i in range(len(vertices))]

for i in range(len(vertices)):
    for j in range(len(vertices)):
        if i == j:
            continue
        elif (i, j) not in edges and (j, i) not in edges:
            m += v[i] + v[j] <= 1

m += xsum(v[i] for i in range(len(v))) == k

m.objective = maximize(xsum(v[i] for i in range(len(v))))

status = m.optimize(max_seconds=15)
if status == OptimizationStatus.OPTIMAL:
    print('optimal solution cost {} found'.format(m.objective_value))
elif status == OptimizationStatus.FEASIBLE:
    print('sol.cost {} found, best possible: {}'.format(m.objective_value, m.objective_bound))
elif status == OptimizationStatus.NO_SOLUTION_FOUND:
    print('no feasible solution found, lower bound is: {}'.format(m.objective_bound))
elif status == OptimizationStatus.UNBOUNDED:
    print('unbounded input')
if status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE:
    print('solution:')
    for v in m.vars:
       if abs(v.x) > 1e-6: # only printing non-zeros
          print('{} : {}'.format(v.name, v.x))

    if m.num_solutions > 0:
        print("solutions found:", m.num_solutions)
        #for i in range(m.num_solutions):
        #    print("Solution {}: ".format(i), newline="")
        #    for v in m

print("Success! Terminating.")