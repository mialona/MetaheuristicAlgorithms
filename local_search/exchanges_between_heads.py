import random as rd

from .objective_function import objective_function
from .correct_finishing import correct_finishing

def exchanges_between_heads(features, data, ops_a, ops_b, percent, sum_head_a, sum_head_b):
    """
    The 'exchanges_between_heads' function exchanges operations randomly between
    head A and B depending on the sum of times of each head.

    Args:
        features: Dictionary of machine features and extensions values ("Xmin",
            "Xmax", "Ymax", "M1_head_A", "M2_head_B", "M3_collision",
            "exten_head_A", "exten_head_B").
        data: List with the values of the operations.
        ops_a: List with the id of operations in head A.
        ops_b: List with the id of operations in head B.
        percent: Solution efficiency percentage.
        sum_head_a: Sum of the times of the head A.
        sum_head_b: Sum of the times of the head B.

    Returns:
        d_head_a: List with the solution of new operations in head A.
        d_head_b: List with the solution of new operations in head B.
        ops_a: List with the id of new operations in head A.
        ops_b: List with the id of new operations in head B.
        percent: New solution efficiency percentage.
    """

    # Copy of the lists of operation ids
    new_ops_a = ops_a.copy()
    new_ops_b = ops_b.copy()

    # Probabilities of exchanging a operation from head A to head B or vice versa
    probability_a = sum_head_a/(sum_head_a + sum_head_b)
    probability_b = sum_head_b/(sum_head_a + sum_head_b)

    # Exchanging operations from head A to head B
    i = 0
    while(i < len(new_ops_a)):
        # Decide if the exchange of this operation will be carried out
        change = rd.choices([False, True], weights=[probability_b,probability_a])[0]

        # Exchange of this operation
        if(change and data[new_ops_a[i]-1][2] > features['M2_head_B']):
            new_ops_b.append(new_ops_a[i])
            new_ops_a.pop(i)
        else:
            i = i + 1 # If the exchange is made, it stays in the same position

    # Exchanging operations from head B to head A
    i = 0
    while(i < len(new_ops_b)):
        # Decide if the exchange of this operation will be carried out
        change = rd.choices([False, True], weights=[probability_a,probability_b])[0]

        # Exchange of this operation
        if(change and data[new_ops_b[i]-1][2] < features['M1_head_A']):
            new_ops_a.append(new_ops_b[i])
            new_ops_b.pop(i)
        else:
            i = i + 1 # If the exchange is made, it stays in the same position

    # Call to finishing correction function
    ops_a, ops_b = correct_finishing(features, data, new_ops_a, new_ops_b)

    # Call to objective function
    percent, d_head_a, d_head_b = objective_function(features, data, ops_a, ops_b)

    # Return results
    return d_head_a, d_head_b, ops_a, ops_b, percent