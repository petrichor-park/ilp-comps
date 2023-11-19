from mip import *

def knapsack(items, max_weight):
    m = Model() 
    variables = [m.add_var(var_type=BINARY) for item in items]
    m.objective = maximize(xsum(variables[i] * items[i]["value"] for i in range(len(items))))
    m += xsum(variables[i] * items[i]["weight"] for i in range(len(items))) <= max_weight
    m.optimize()
    selected = [items[i] for i in range(len(items)) if variables[i].x > 0.5]
    return selected

print("Enter the weights of the items in the set:")
weights = [int(x) for x in input().split()]
print("Enter the values of the items in the set:")
values = [int(x) for x in input().split()]

items = [{"weight": weight, "value": value} for weight, value in zip(weights, values)]

print("Enter the capacity (maximum weight) of the knapsack:")
max_weight = int(input())

selected_items = knapsack(items, max_weight)

print("--------------------")
print("{} items selected:".format(len(selected_items)))
print("Total weight: {}".format(sum(item["weight"] for item in selected_items)))
print("Total value: {}".format(sum(item["value"] for item in selected_items)))

for index, item in enumerate(selected_items):
    print("Item {} has weight {} and value {}".format(index, item["weight"], item["value"]))
    

    


