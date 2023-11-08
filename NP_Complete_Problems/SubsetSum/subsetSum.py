from mip import *
import random

def subsetSum(set, target):
    '''
        Returns a subset of the input set which sums to target.

        Inputs:
        - set: a list of integers
        - target: an integer

        Returns:
        - a list which is a subset of set which sums to target
        '''
    n = len(set)
    m = Model()

    x = [ m.add_var(var_type=BINARY) for i in range(n) ]

    # the items which are used must sum to target
    m += xsum(x[i] * set[i] for i in range(n)) == target

    # at least one item must be used
    m += xsum(x[i] for i in range(n)) >= 1

    m.verbose = False
    m.optimize()
    subset = []

    # determine which items are in the subsetr
    for i in range(len(m.vars)):
        if m.vars[i].x == 1:
            subset.append(set[i])
    return subset

def randomSubsetSum(set_min, set_max, set_length, target_min, target_max):
    set = [random.randrange(set_min, set_max, 1) for _ in range(set_length)]
    target = random.randrange(target_min, target_max, 1)
    print(set)
    return set, target, subsetSum(set, target)

if __name__ == "__main__":
    print()
    print("Welcome to ILP subset sum, your friendly subset sum solver.")
    print("Would you like to make your own set and target manually or generate one randomly? (m/r)")
    answer = input()
    sum = None
    set = None
    target = None
    if answer == 'm':
        print("I'm so glad you decided to be creative!!")
        print("Please enter your set separated by spaces:")
        set = list(map(int, input().split(" ")))
        print("Thanks!!")
        print()
        print("Please enter your target value:")
        target = int(input())
        print()
        sum = subsetSum(set, target)
    else:
        print("I'm so glad you're leaving things to chance!")
        print("Please type the min and max values I can include in the set separated by a space:")
        set_min_max = input().split(" ")
        while not len(set_min_max) == 2:
            print("Please try again:")
            set_min_max = input().split(" ")
        print("How many items would you like in the set?")
        length = int(input())
        print("Amazing! Now please enter the min and max possible values for the target separated by a space:")
        target_min_max = input().split(" ")
        while not len(target_min_max) == 2:
            print("Please try again:")
            target_min_max = input().split(" ")
        output = randomSubsetSum(int(set_min_max[0]), int(set_min_max[1]), length, int(target_min_max[0]), int(target_min_max[1]))
        set = output[0]
        target = output[1]
        sum = output[2]
    if len(sum) > 0:
            print("There is a subset of", set, "which sums to", target)
            print("One such subset is", sum)
    else:
        print("There is no subset of", set, "which sums to", target)
        