from mip import *
from itertools import *

def find_hamiltonian(edges):
    '''
    Check whether a Hamiltonian Cycle can be found in a graph.

    Args:
        edges (list): A list of tuples representing each edge in the graph

    Returns:
        list of names of variables that solve the ILP or a print statement that says no solution
    '''
    model = Model()
    edge_vars = []
    vertices = make_list_of_vertices(edges)
    vertices_dictionary = {vertex: [] for vertex in vertices}

    #CREATE VARIABLES
    for edge in edges:
        var = model.add_var(var_type=BINARY, name=str(edge))
        edge_vars.append(var)
        vertices_dictionary[edge[0]].append(var)
        vertices_dictionary[edge[1]].append(var)
    
    #CREATE LINEAR CONSTRAINTS
    #cycle constraints
    model += xsum(var for var in edge_vars) == len(vertices)
    for vertex in vertices_dictionary:
        model += xsum(vertices_dictionary[vertex][var] for var in range(len(vertices_dictionary[vertex]))) == 2
    
    #eliminate subcycles
    all_vertices_subsets = make_subsets(vertices)
    for subset_vertices in all_vertices_subsets:
        possible_edges = list(combinations(subset_vertices, 2))
        subset_edges = intersection(possible_edges, edges)
        subset_edges_vars = []
        for edge in subset_edges:
            subset_edges_vars.append(model.var_by_name(str(edge)))
        model += xsum(var for var in subset_edges_vars) <= len(subset_vertices) - 1
        
    #RUN ILP
    model.verbose = False
    status = model.optimize()

    
    if status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE:
        print("Here are the edges included in the Hamiltonian cycle:")
        solution = []
        for var in model.vars:
            if var.x == 1:
                solution.append(var.name)
        return solution
    else:
        return "Sorry, no Hamiltonian cycle exists in this graph."
        
   

def make_list_of_vertices(edges):
    '''
    Extracts the vertices from a graph. 

    Args:
        edges (list): A list of tuples

    Returns:
        set of the vertices from all of the edges 
    '''
    vertices = set()
    for tup in edges:
        vertices.update(tup)
    return list(vertices)


#Adaptation of code from 
#https://stackoverflow.com/questions/20297154/python-create-iterator-through-subsets-of-a-set-for-a-loop
def make_subsets(vertex_list):  
    '''
    Creates all possible subsets of a graph.

    Args:
        edges (set): A list of vertices (int) from a graph

    Returns:
        list of lists representing all unique combinations of the vertices  
    '''
    subsets = [[]]
    for vertex in vertex_list:
        for i in range(len(subsets)):
            subsets += [subsets[i]+[vertex]]
    subsets.pop(0)
    subsets.pop(-1)
    return subsets


def intersection(list1, list2):
    '''
    Finds the edges in a subset that exist in the original graph.

    Args:
        list1 (list): A list of tuples
        list2 (list): A list of tuples
    Returns:
        list of tuples
    '''
    common_edges = []

    for edge in list1:
        if edge in list2:
            common_edges.append(edge)
    return common_edges


def organize_edges(edges):
    '''
    Sorts each tuple by smallest to biggest {ex: (2,1) becomes (1,2)}

    Args:
        edges (list): A list of tuples

    Returns:
        list of tuples
    '''
    organized_edges = [tuple(sorted(t)) for t in edges]
    for tuple_edge in edges:
        organized_edges.append(sorted(tuple_edge))
    return organized_edges


if __name__ == "__main__":
    print()
    print("Need help finding a Hamiltonian cycle in your graph? Let me help!\n")
    print("The edges of the graph should be given in the specified format *ex: (1,2), (2,3), (1,3)*")
    
    #TAKE USER INPUT AND CONVERT GRAPH TO LIST OF TUPLES
    graph_string = input('Provide the edges of your graph here: ')
    graph_tup = list(eval(graph_string))
    formatted_graph_tup = organize_edges(graph_tup)

    hamiltonian_cycle = find_hamiltonian(formatted_graph_tup)

    print()
    print(hamiltonian_cycle)
    print()
