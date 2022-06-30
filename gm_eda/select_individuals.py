def select_individuals(list_sigmas, size):
    """
    The 'select_individuals' function reduces population size using elitist criteria.

    Args:
        list_sigmas: List with all the permutations of the current generation.
        size: Number of solutions/permutations of the new generation.

    Returns:
        list_sigmas_se: List with all the permutations of the new generation.
    """

    # Ordering of permutations by objective function value
    list_sigmas.sort(key = lambda sigma: sigma[1], reverse = True)

    # Return results
    return list_sigmas[0:size]