import itertools

def branch_and_bound(options, bound):
    '''For a given set of options in the form (value, cost), computes the 
    optimal binary combination of options such that the cost does not exceed
    bound. Returns the trivial solution if there is no feasible solution.
    Uses the branch and bound algorithm.'''

    # initialize solution, best_solution, branches
    solution = [None for x in range(len(options))]
    best_solution = [0 for x in range(len(options))], 0, 0
    branches = expand_branches(solution)
    
    # while available branches
    while branches:
        solution = branches.pop(0)

        # compute cost and value
        cost = compute_cost(solution, options)
        value = compute_value(solution, options)

        # if a valid branch
        if (cost <= bound):

            # if value exceeds best found value or values are equal but cost is less
            if (value > best_solution[1] or value == best_solution[1] and cost < best_solution[2]):

                # record solution
                best_solution = solution, value, cost
            
            # and expand branches
            branches.extend(expand_branches(solution))

    # the solution must be feasible
    assert(best_solution[2] <= bound); 

    # replace unexpanded nodes with empty weights
    return [x if x is not None else 0 for x in best_solution[0]], best_solution[1], best_solution[2]

def brute_force(options, bound):
    '''Enumerates all options for a solution. This is slower than the branch
    and bound algorithm and should only be used for testing the validity of
    the output of the branch and bround algorithm.'''
 
    # initialize solution, best_solution, branches
    best_solution = [0 for x in range(len(options))], 0, 0

    # while available branches
    for solution in itertools.product(range(2), repeat=len(options)):

        # compute cost and value
        cost = compute_cost(solution, options)
        value = compute_value(solution, options)

        # if value >= best_solution's value
        if ((cost <= bound and value > best_solution[1]) or (value == best_solution[1] and cost < best_solution[2])):

            # record solution
            best_solution = solution, value, cost

    # the solution must be feasible
    assert(best_solution[2] <= bound)

    return best_solution

# define the cost and value functions
def compute_value(solution, options):
    '''Computes the value function for the given solution.'''
    return sum([options[i][0] for i in range(len(solution)) if solution[i] == 1])

def compute_cost(solution, options):
    '''Computes the cost function for the given solution.'''
    return sum([options[i][1] for i in range(len(solution)) if solution[i] == 1])

def expand_branches(solution):
    '''Expands the next set of branches for the branch and bound problem. 
    Expects unexplored binary nodes to have a value of None. If there are
    no remaining nodes to be explored, returns an empty list.'''
    
    branches = []

    # if there are unexplored nodes
    if (None in solution):

        # expand the node using binary values
        next_node_index = solution.index(None)
        for value in range(2):
            next_node = solution[:]
            next_node[next_node_index] = value
            branches.append(next_node)

    return branches

# a few unit tests
def test():
    tasks = (130,9),(150,12),(190,20),(190,23),(229,27),(290,33),(330,31),(70,9),(330,30),(110,9),(90,6),(310,34),(330,34),(190,22),(230,25),(170,13)
    assert(cmp(branch_and_bound(tasks, 100),brute_force(tasks, 100)))
    assert(cmp(branch_and_bound(tasks, 99),brute_force(tasks, 99)))
    assert(cmp(branch_and_bound(tasks, 98),brute_force(tasks, 98)))
    assert(cmp(branch_and_bound(tasks[0:12], 75),brute_force(tasks[0:12], 75)))
    tasks = (130,9),(150,12),(190,20),(190,23),(229,27),(290,33),(330,31),(70,9),(330,30),(110,9),(90,6),(310,34),(130,9),(150,12),(190,20),(190,23),(229,27),(290,33),(330,31),(70,9),(330,30),(110,9),(90,6),(310,34),= (130,9),(150,12),(190,20),(190,23),(229,27),(290,33),(330,31),(70,9),(330,30),(110,9),(90,6),(310,34),(130,9),(150,12),(190,20),(190,23),(229,27),(290,33),(330,31),(70,9),(330,30),(110,9),(90,6),(310,34)))
    assert(cmp(branch_and_bound(tasks, 150),brute_force(tasks, 150)))

if __name__ == "__main__":
    tasks = (130,9),(150,12),(190,20),(190,23),(229,27),(290,33),(330,31),(70,9),(330,30),(110,9),(90,6),(310,34),(330,34),(190,22),(230,25),(170,13)
    print branch_and_bound(tasks, 100)