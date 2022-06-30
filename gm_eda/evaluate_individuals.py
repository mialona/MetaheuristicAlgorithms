from .objective_function import max_objective_function

def evaluate_individuals(features, data, list_sigmas, n):
    """
    The 'evaluate_individuals' function computes the objective function value
    of each permutation of the current generation.

    Args:
        features: Dictionary of machine features and extensions values ("Xmin",
            "Xmax", "Ymax", "M1_head_A", "M2_head_B", "M3_collision",
            "exten_head_A", "exten_head_B").
        data: List with the values of the operations (columns "ops", "t", "x",
            "y", "seq").
        list_sigmas: List with all the permutations of the current generation.
        n: Number of operations.

    Returns:
        list_sigmas: List with all the permutations of the current generation.
    """

    for row in list_sigmas:
        # Calculation of the objective function value
        max_percent, max_ops_a, max_ops_b = max_objective_function(data, row[0], features["M3_collision"])

        # The best percentage and the cut-off point are added to the permutation
        row.append(max_percent)
        row.append(len(max_ops_a))

    # Return results
    return list_sigmas