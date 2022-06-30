def extend_population(list_population, list_decendents):
    """
    The 'extend_population' function adds the newly created individuals to the
    current generation.

    Args:
        list_population: List with the individuals of the current generation.
        list_decendents: List with the new individuals.

    Returns:
        list_population: Augmented list with the individuals of the current generation.
    """

    # Return the union of the list of new descendants to the generation list
    return list_population + list_decendents