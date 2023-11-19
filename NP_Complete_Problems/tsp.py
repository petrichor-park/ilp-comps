from mip import *
from collections import defaultdict

def ilptsp(points):
    '''
    Integer Linear Programming implementation of the Traveling Salesperson Problem

    Args:
        points (list(tuple(int))): a list of (x,y) coordinates that represent the locations of each "city"
    
    Returns:
        None (prints out a list of cities to travel between)
    '''
    #Assumes points are on an (x,y) plane and in such a form
    m = Model(solver_name='GRB')

    pointvariables = {}
    #these two dicts separate variables by inwards edge and outwards edge to set up for the constraints
    edges_by_point_outward = defaultdict(list)
    edges_by_point_inward = defaultdict(list)

    edges = []
    edgevars = []
    for i in range(len(points)-1):
        for j in range(i+1,len(points)):
            edge = ((points[i][0]-points[j][0])**(2)+(points[i][1]-points[j][1])**(2))**(0.5)
            var1 = m.add_var(name=str(points[i])+'-'+str(points[j]),var_type=BINARY)
            var2 = m.add_var(name=str(points[j])+'-'+str(points[i]),var_type=BINARY)

            #structure the variable relations as follows to properly set up constraints
            edges.append(edge)
            edges.append(edge)
            edgevars.append(var1)
            edgevars.append(var2)
            edges_by_point_inward[str(points[i])].append(var2)
            edges_by_point_inward[str(points[j])].append(var1)
            edges_by_point_outward[str(points[i])].append(var1)
            edges_by_point_outward[str(points[j])].append(var2)
        
        pointvariables[str(points[i+1])] = m.add_var(name=str(points[i+1]),var_type=INTEGER)

    
    for point in points:
        m += xsum(1*edges_by_point_outward[str(point)][i] for i in range(len(edges_by_point_outward[str(point)]))) == 1
        m += xsum(1*edges_by_point_inward[str(point)][i] for i in range(len(edges_by_point_inward[str(point)]))) == 1
    
    for var in edgevars: #these next two loops ensure that the final solution contains exactly one full cycle
        if str(points[0]) not in var.name:
            u1 = var.name.split('-')[0]
            u2 = var.name.split('-')[1]
            m += pointvariables[u1]-pointvariables[u2]+(len(points)-1)*var <= len(points)-2
    
    for var in pointvariables.values():
        m += var <= len(points)
        m += var >= 2

    m.objective = minimize(xsum(edges[i]*edgevars[i] for i in range(len(edges)))) #minimize total edge weights

    m.max_gap = 0.025
    status = m.optimize(max_seconds=300)
    if status == OptimizationStatus.OPTIMAL:
        print('optimal solution cost {} found'.format(m.objective_value))
    elif status == OptimizationStatus.FEASIBLE:
        print('sol.cost {} found, best possible: {}'.format(m.objective_value, m.objective_bound))
    elif status == OptimizationStatus.NO_SOLUTION_FOUND:
        print('no feasible solution found, lower bound is: {}'.format(m.objective_bound))
    if status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE:
        print('solution:')
        for v in m.vars:
            if abs(v.x) > 1e-6 and '-' in v.name: # only printing non-zero edges
                print('{} : {}'.format(v.name, v.x))


