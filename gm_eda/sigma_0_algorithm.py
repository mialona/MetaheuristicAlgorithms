from numpy import argsort

def sigma_0_algorithm(list_sigmas,n):
    """
    The 'sigma_0_algorithm' function computes the consensus permutation using
    the Consensus Permutation Calculation Algorithm.

    Args:
        list_sigmas: List with all the permutations of the current generation.
        n: Number of operations.

    Returns:
        sigma_0: Consensus permutation.
    """

    # Calculation of the frequency matrix
    frec = []
    for i in range(n):
        aux_list = []
        for j in range(n):
            sum = 0
            for row in list_sigmas:
                if(i + 1 == row[0][j]):
                    sum = sum + 1

            aux_list.append(sum/n)

        frec.append(aux_list)

    # Consensus Permutation Calculation Algorithm
    not_visited_i = list(range(n))
    not_visited_j = list(range(n))
    sigma_0 = [0]*n
    for k in range(n):
        max = 0
        i_max = None
        j_max = None

        # Calculation of the maximum frequency value in the rows and columns that
        # remain to be used in the matrix
        for i in not_visited_i:
            for j in not_visited_j:
                if(max <= frec[i][j]):
                    max = frec[i][j]
                    i_max = i
                    j_max = j

        # Assignment of consensus permutation values
        sigma_0[j_max] = i_max + 1

        # The rows and columns of the maximum frequency value are marked as used
        not_visited_i.remove(i_max)
        not_visited_j.remove(j_max)

    # Return results
    return sigma_0