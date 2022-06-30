def reduce_population(list_population, size):
    """
    The 'reduce_population' function reduces population size using elitist criteria.

    Args:
        list_population: List with the individuals of the current generation.
        size: Number of individuals of the new generation.

    Returns:
        list_population: List with the individuals of the new generation.
    """

    # Ordering of permutations by objective function value
    list_population.sort(key = lambda individual: individual[2], reverse = True)

    # Return results
    return list_population[0:size]