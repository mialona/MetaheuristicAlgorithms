from time import time
from random import choice

from .extensions import extensions
from .random_individuals import random_individuals
from .evaluate_individuals import evaluate_individuals
from .select_individuals import select_individuals
from .sigma_0_algorithm import sigma_0_algorithm
from .objective_function import objective_function, max_objective_function
from .spread_parameters import spread_parameters
from .sample_distribution import sample_distribution

def gm_eda(features, data, exploration_rate = 1, max_gen_wo_improvement = 10):
    """
    The 'gm_eda' function manages the execution of the 'Generalized Mallows
    Estimation of Distribution Algorithm'.

    Args:
        features: Dictionary of machine features and extensions values ("Xmin",
            "Xmax", "Ymax", "M1_head_A", "M2_head_B", "M3_collision",
            "exten_head_A", "exten_head_B").
        data: List with the values of the operations (columns "ops", "t", "x",
            "y", "seq").
        exploration_rate: Exploration index that multiplies each of the
            propagation parameters.
        max_gen_wo_improvement: Maximum number of generations in which no
            improvement is achieved.

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

    # Effect of extensions on features
    features = extensions(features)

    # Initialization of auxiliary variables
    historical = []
    num_gen_wo_improvement = 1
    n = len(data)

    # Generate 10*n individuals at random
    list_sigmas = random_individuals(features, data, 10*n)

    # Evaluate the 10*n individuals
    list_sigmas = evaluate_individuals(features, data, list_sigmas, n)

    # Select n individuals
    list_sigmas_se = select_individuals(list_sigmas, n)
    best_ops_a = list_sigmas_se[0][0][0:list_sigmas_se[0][2]]
    best_ops_b = list_sigmas_se[0][0][list_sigmas_se[0][2]:len(list_sigmas_se[0][0])]
    best_percent = list_sigmas_se[0][1]
    historical.append(list_sigmas_se[0][1])

    # Main loop
    time_max = n*4
    start_time = time()
    while((time() - start_time) < time_max):
        # Estimate the consensus ranking
        sigma_0 = sigma_0_algorithm(list_sigmas_se,n)

        # Estimate the spread parameters
        theta = spread_parameters(list_sigmas_se,sigma_0,n)

        # Sample new 10*n − 1 individuals from the probability distribution
        list_sigmas = sample_distribution(data, sigma_0, theta, exploration_rate, n, 10*n - 1, features["M3_collision"])

        # Evaluate and select 10*n individuals
        list_sigmas = evaluate_individuals(features, data, list_sigmas, n)

        # Select n individuals
        list_sigmas_se = select_individuals(list_sigmas + list_sigmas_se, n)
        if(best_percent == list_sigmas_se[0][1]):
            num_gen_wo_improvement = num_gen_wo_improvement + 1
        else:
            best_ops_a = list_sigmas_se[0][0][0:list_sigmas_se[0][2]]
            best_ops_b = list_sigmas_se[0][0][list_sigmas_se[0][2]:len(list_sigmas_se[0][0])]
            best_percent = list_sigmas_se[0][1]
        historical.append(list_sigmas_se[0][1])

        # Restart if the number of generations without improvement is met
        if(num_gen_wo_improvement >= max_gen_wo_improvement):
            num_gen_wo_improvement = 1

            # Generate 10*n individuals at random
            list_sigmas = random_individuals(features, data, 10*n)

            # Evaluate the 10*n individuals
            list_sigmas = evaluate_individuals(features, data, list_sigmas, n)

            # Select n individuals
            list_sigmas_se = select_individuals(list_sigmas, n)

    # Return results
    percent, d_head_a, d_head_b = objective_function(data, best_ops_a, best_ops_b, features["M3_collision"])
    return d_head_a, d_head_b, historical, best_ops_a, best_ops_b, percent