from .extensions import *
from .random_individuals import *
from .select_fathers import *
from .produce_individuals import *
from .extend_population import *
from .reduce_population import *

def genetic_algorithm(features, data, num_rep, prob_mut):
    """
    The 'gm_eda' function manages the execution of the 'Generalized Mallows
    Estimation of Distribution Algorithm'.

    Args:
        features: Dictionary of machine features and extensions values ("Xmin",
            "Xmax", "Ymax", "M1_head_A", "M2_head_B", "M3_collision",
            "exten_head_A", "exten_head_B").
        data: List with the values of the operations (columns "ops", "t", "x",
            "y", "seq").
        num_rep: Number of repetitions.
        prob_mut: Probability of making a mutation.

    Returns:
        d_head_a: List with the solution of operations in head A (columns
            "ops", "t", "t_start").
        d_head_b: List with the solution of operations in head B (columns
            "ops", "t", "t_start").
        historical: List with the percentage historicals.
        best_ops_a: List with the operations in head A in the order of the
            solution.
        best_ops_b: List with the operations in head B in the order of the
            solution.
    """

    historical = []
    size = 4*len(data)

    # Check the number of repetitions and mutation probability
    if(num_rep <= 0 or prob_mut < 0 or prob_mut > 1):
        raise Exception("Number of repetitions less than 1 or mutation probability between 0 and 1.")

    # Generate individuals at random
    list_population = random_individuals(features, data, size)
    list_population.sort(key = lambda individual: individual[2], reverse = True)
    historical.append(list_population[0][2])

    # Main loop
    for i in range(num_rep):
        # Select fathers
        list_fathers = select_fathers(list_population, size)

        # Produce decendents
        list_decendents = produce_individuals(features, data, list_fathers, size, prob_mut)

        # Extend population
        list_population = extend_population(list_population, list_decendents)

        # Reduce population
        list_population = reduce_population(list_population, size)
        historical.append(list_population[0][2])

    # Return results
    percent, d_head_a, d_head_b = objective_function(features, data, list_population[0][0], list_population[0][1])
    return d_head_a, d_head_b, historical, list_population[0][0], list_population[0][1], percent