from math import exp
from random import choices, randrange

from .correct_finishing import correct_finishing

def meila_algorithm(v,n):
    """
    The 'meila_algorithm' function computes the inverted permutation pi from the
    values of V(pi).

    Args:
        v: List with the valeues of V(pi).
        n: Number of operations.

    Returns:
        inv_pi: Inverted permutation pi.
    """

    inv_pi = [n]
    for j in range(n-1,0,-1):
        # Inserting the values of the inverted permutation pi
        inv_pi.insert(v[j - 1],j)

    # Return results
    return inv_pi

def sample_distribution(features, data, sigma_0, theta, exploration_rate, n, size):
    """
    The 'meila_algorithm' function computes the inverted permutation pi from the
    values of V(pi).

    Args:
        features: Dictionary of machine features and extensions values.
        data: List with the values of the operations (columns "ops", "t", "x",
            "y", "seq").
        sigma_0: Consensus ranking.
        theta: Spread parameters.
        exploration_rate: Exploration index that multiplies each of the
            propagation parameters.
        n: Number of operations.
        size: Number of solutions/permutations of the new generation.
        M3_collision: Minimum distance between heads.

    Returns:
        list_sigmas: List with all the permutations of the new generation.
    """

    list_sigmas = []
    while(len(list_sigmas) < size):
        # Create list 'v'
        v = []
        for j in range(1, n):
            # Exploration rate
            theta_j = theta[j - 1]/exploration_rate

            # Psi calculation
            psi_j = (1-exp(-theta_j*(n-j+1)))/(1-exp(-theta_j))

            # Possible 'r_j's and their probability according to the distribution
            set_r_j = list(range(n - j + 1))
            prob_r_j = []
            for k in range(len(set_r_j)):
                prob_r_j.append(exp(-theta_j*set_r_j[k])/psi_j)

            # Selection of a 'r_j'
            v.append(choices(set_r_j,prob_r_j,k=1)[0])

        # Meila's algorithm
        inv_pi = meila_algorithm(v,n)

        # Inverting
        inverted = []
        for i in range(n):
            inverted.append(inv_pi.index(i + 1) + 1)

        # Composing
        composed = []
        for i in range(n):
            composed.append(inverted[sigma_0[i] - 1])

        # Call to finishing correction function
        random_int = randrange(len(composed)//3, (2*len(composed))//3)
        ops_a, ops_b = correct_finishing(features, data, composed[0:random_int], composed[random_int:len(composed)])

        # Add to list
        list_sigmas.append([composed])

    # Return results
    return list_sigmas