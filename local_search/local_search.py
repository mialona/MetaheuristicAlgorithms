from .objective_function import objective_function

def local_search(data, d_head_a, d_head_b, ops_a, ops_b, percent, M3_collision):
    """
    The 'local_search' function performs a local search for solutions exchanging
    one by one the position of the operations within each head.

    Args:
        data: List with the values of the operations.
        d_head_a: List with the solution of operations in head A.
        d_head_b: List with the solution of operations in head B.
        ops_a: List with the id of operations in head A.
        ops_b: List with the id of operations in head B.
        percent: Solution efficiency percentage.
        M3_collision: Minimum distance between heads.

    Returns:
        list_d_head_a: List of lists with the solution of new operations in head A.
        list_d_head_b: List of lists with the solution of new operations in head B.
        list_ops_a: List of lists with the id of new operations in head A.
        list_ops_b: List of lists with the id of new operations in head B.
        list_percent: List with new solutions efficiency percentage.
    """

    # Initialization of solution lists with the given solution as initial
    list_d_head_a = [d_head_a]
    list_d_head_b = [d_head_b]
    list_ops_a = [ops_a]
    list_ops_b = [ops_b]
    list_percents = [percent]

    # If 200% efficiency has been achieved, the function ends
    if(percent < 200):
        # Initialization of auxiliary variables
        found = True
        ops_aux_a = []
        ops_aux_b = []
        ops_best_a = ops_a.copy()
        ops_best_b = ops_b.copy()

        # As long as it finds a better solution, it stays in the loop.
        while(found):
            found = False

            # Exchange of position two consecutive solutions of head A
            for j in range(-1, len(ops_a)-1):
                ops_aux_a = ops_best_a.copy() # The best solution obtained is taken

                # In the first iteration of the loop no swaps are performed
                # Before exchanging, it is checked that there is more than one operation
                if(j > -1 and len(ops_aux_a) > 1):
                    a = ops_aux_a[j]
                    ops_aux_a[j] = ops_aux_a[j+1]
                    ops_aux_a[j+1] = a

                # Exchange of position two consecutive solutions of head B
                for i in range(len(ops_b)-1):
                    ops_aux_b = ops_best_b.copy() # The best solution obtained is taken

                    # Before exchanging, it is checked that there is more than one operation
                    if(len(ops_aux_b) > 1):
                        b = ops_aux_b[i]
                        ops_aux_b[i] = ops_aux_b[i+1]
                        ops_aux_b[i+1] = b

                        # Call to objective function
                        new_percent, d_head_a, d_head_b = objective_function(data, ops_aux_a, ops_aux_b, M3_collision)

                        # If the new efficiency percentage is better than the previous one, the solution obtained is saved in the lists
                        if(new_percent > list_percents[len(list_percents)-1]):
                            list_d_head_a.append(d_head_a)
                            list_d_head_b.append(d_head_b)
                            list_ops_a.append(ops_aux_a)
                            list_ops_b.append(ops_aux_b)
                            list_percents.append(new_percent)

                            found = True # Keep searching

            # The last operations list is assigned as the best
            ops_best_a = list_ops_a[len(list_ops_a)-1].copy()
            ops_best_b = list_ops_b[len(list_ops_b)-1].copy()

    # Return results
    return list_d_head_a, list_d_head_b, list_ops_a, list_ops_b, list_percents