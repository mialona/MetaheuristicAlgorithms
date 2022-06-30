import random as rd

from .objective_function import objective_function
from .correct_finishing import correct_finishing

def init_solution(features, data):
    """
    The 'init_solution' function creates an initial random solution for the
    given operations and features.

    Args:
        features: Dictionary of machine features and extensions values.
        data: List with the values of the operations.

    Returns:
        d_head_a: List with the solution of operations in head A.
        d_head_b: List with the solution of operations in head B.
        ops_a: List with the id of operations in head A.
        ops_b: List with the id of operations in head B.
        percent: Solution efficiency percentage.
    """

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
            if(rd.getrandbits(1)):
                ops_a.append(op)
            else:
                ops_b.append(op)

        # The operations of each head are randomized
        rd.shuffle(ops_a)
        rd.shuffle(ops_b)

    # Call to finishing correction function
    ops_a, ops_b = correct_finishing(data, ops_a, ops_b, features["M3_collision"])

    # Call to objective function
    percent, d_head_a, d_head_b = objective_function(data, ops_a, ops_b, features["M3_collision"])

    # Return results
    return d_head_a, d_head_b, ops_a, ops_b, percent