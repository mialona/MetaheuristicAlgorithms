from .extensions import *
from .init_solution import *
from .local_search import *
from .exchanges_between_heads import *

def local_search_algorithm(features, data, num_rep, num_exchanges):
    """
    The 'local_search' function manages the iterations of the 'Twin
    Head Machine Optimization Algorithm'.

    Args:
        features: Dictionary of machine features and extensions values ("Xmin",
            "Xmax", "Ymax", "M1_head_A", "M2_head_B", "M3_collision",
            "exten_head_A", "exten_head_B").
        data: List with the values of the operations (columns "ops", "t", "x",
            "y", "seq").
        num_rep: Number of repetitions.
        num_exchanges: Number of exchanges.

    Returns:
        best_head_a: List with the solution of operations in head A (columns
            "ops", "t", "t_start").
        best_head_b: List with the solution of operations in head B (columns
            "ops", "t", "t_start").
        total_historical: List with the percentage historicals.
        best_historical: List with the best historical.
    """

    # Check the number of repetitions and exchanges
    if(num_rep <= 0 or num_exchanges < 0):
        raise Exception("Number of repetitions less than 1 or exchanges less than 0.")

    # Effect of extensions on features
    features = extensions(features)

    # Initialization of result variables
    best_head_a = None
    best_head_b = None
    best_historical = None
    total_historical = []

    # Algorithm iteration loop
    old_percent = 0
    for i in range(num_rep):
        # If 200% efficiency has been achieved, the loop ends
        if(old_percent >= 200):
            break

        # Historical reset
        historical = []

        # Creating an initial solution
        d_head_a, d_head_b, ops_a, ops_b, percent = init_solution(features, data)
        historical.append(percent) # Percentage added to history

        # Local search for the initial solution
        list_d_head_a, list_d_head_b, list_ops_a, list_ops_b, list_percents = local_search(
                data, d_head_a, d_head_b, ops_a, ops_b, percent, features["M3_collision"])
        percent = list_percents[len(list_percents)-1]
        historical.append(percent) # Percentage added to history

        # Algorithm exchange loop
        for j in range(num_exchanges):
            # If 200% efficiency has been achieved, the loop ends
            if(percent >= 200):
                break

            # Exchanges between heads
            d_head_a, d_head_b, ops_a, ops_b, new_percent = exchanges_between_heads(
                    data, list_ops_a[len(list_ops_a)-1],
                    list_ops_b[len(list_ops_b)-1], percent,
                    sum([row[1] for row in list_d_head_a[len(list_d_head_a)-1]]), # Sum of the times of the head A
                    sum([row[1] for row in list_d_head_b[len(list_d_head_b)-1]]), # Sum of the times of the head B
                    features["M1_head_A"], features["M2_head_B"], features["M3_collision"])

            # Local search for the exchanged solution
            if(new_percent > percent):
                list_d_head_a, list_d_head_b, list_ops_a, list_ops_b, list_percents = local_search(
                        data, d_head_a, d_head_b, ops_a, ops_b, new_percent, features["M3_collision"])
                percent = list_percents[len(list_percents)-1]
                historical.append(percent) # Percentage added to history

            j = j + 1

        # Save historical
        total_historical.append(historical)

        # Save best results
        if(percent > old_percent):
            best_head_a = list_d_head_a[len(list_d_head_a)-1]
            best_head_b = list_d_head_b[len(list_d_head_b)-1]
            best_historical = historical.copy()
            old_percent = percent
        i = i + 1

    # Return results
    return best_head_a, best_head_b, total_historical, best_historical