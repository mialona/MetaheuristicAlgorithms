from random import randrange

def select_fathers(list_population, size):
    """
    The 'select_fathers' function chooses the parents of the future new descendants
    through a random tournament of size 2.

    Args:
        list_population: List with the individuals of the current generation.
        size: Number of individuals of the new generation.

    Returns:
        list_fathers: List with the individuals chosen as parents.
    """

    # List of fathers
    list_fathers = []

    # Random tournament (size 2)
    for i in range(size):
        candidate_1 = list_population[randrange(0, size)]
        candidate_2 = list_population[randrange(0, size)]

        # The winning candidate is added to the list of fathers
        if(candidate_1[2] > candidate_2[2]):
            list_fathers.append(candidate_1)
        else:
            list_fathers.append(candidate_2)

    # Return results
    return list_fathers