from random import getrandbits, shuffle

from .correct_finishing import correct_finishing
from .objective_function import objective_function

def random_individuals(features, data, size):
    """
    The 'random_individuals' function creates a list of random solutions for the
    given operations and features.

    Args:
        features: Dictionary of machine features and extensions values.
        data: List with the values of the operations.
        size: Number of solutions/permutations to create.

    Returns:
        list_sigmas: List with all the permutations of the current generation.
        n: Number of operations.
    """

    # Initialization of result variable
    list_population = []

    while(len(list_population) < size):
        # Initialization of auxiliary variables
        ops_a = []
        ops_b = []
        ops_ab = []

        # Division of operations according to whether only head A, B or both can do them
        for row in data:
            if(row[2] <= features["M2_head_B"]):
                ops_a.append(row[0]) # Only head A
            else:
                if(row[2] >= features["M1_head_A"]):
                    ops_b.append(row[0]) # Only head B
                else:
                    ops_ab.append(row[0]) # Both

        # If there are operations that both can do
        if(ops_ab):
            # The operations that both can do are distributed randomly between them
            for op in ops_ab:
                if(getrandbits(1)):
                    ops_a.append(op)
                else:
                    ops_b.append(op)

            # The operations of each head are randomized
            shuffle(ops_a)
            shuffle(ops_b)

        # Call to finishing correction function
##        ops_a, ops_b = correct_finishing(features, data, ops_a, ops_b)

        # Call to objective function
        percent, d_head_a, d_head_b = objective_function(features, data, ops_a, ops_b)

        # The new individual is added
        list_population.append([ops_a, ops_b, percent])

    # Return results
    return list_population