from random import choices, randrange, getrandbits

from .correct_finishing import correct_finishing
from .objective_function import objective_function

def order_crossover(father_1, father_2):
    """
    The 'order_crossover' function performs the crossover operator based on order.

    Args:
        father_1: First father.
        father_2: Second father.

    Returns:
        decendent_1: First decendent.
        decendent_2: Second decendent.
    """

    # Indexes of cuts of the head A
    a_1 = randrange(0, min(len(father_1[0]), len(father_2[0])))
    a_2 = randrange(0, min(len(father_1[0]), len(father_2[0])))
    if(a_1 > a_2):
        aux = a_1
        a_1 = a_2
        a_2 = aux

    # Indexes of cuts of the head B
    b_1 = randrange(0, min(len(father_1[1]), len(father_2[1])))
    b_2 = randrange(0, min(len(father_1[1]), len(father_2[1])))
    if(b_1 > b_2):
        aux = b_1
        b_1 = b_2
        b_2 = aux

    # Cuts
    cut_1_a = father_1[0][a_1:a_2]
    cut_1_b = father_1[1][b_1:b_2]
    cut_2_a = father_2[0][a_1:a_2]
    cut_2_b = father_2[1][b_1:b_2]

    # Operations from parent 2 to add to decendent 1
    add_1_a = []
    aux_1 = cut_1_a + cut_1_b
    for op in father_2[0]:
        if(op not in aux_1):
            add_1_a.append(op)

    add_1_b = []
    for op in father_2[1]:
        if(op not in aux_1):
            add_1_b.append(op)

    # Create decendent 1
    if(a_1 > len(add_1_a)):
        op_1_a = add_1_a + cut_1_a
    else:
        op_1_a = add_1_a[0:a_1] + cut_1_a + add_1_a[a_1:len(add_1_a)]

    if(b_1 > len(add_1_b)):
        op_1_b = add_1_b + cut_1_b
    else:
        op_1_b = add_1_b[0:b_1] + cut_1_b + add_1_b[b_1:len(add_1_b)]

    decendent_1 = [op_1_a, op_1_b]

    # Operations from parent 1 to add to decendent 2
    add_2_a = []
    aux_2 = cut_2_a + cut_2_b
    for op in father_1[0]:
        if(op not in aux_2):
            add_2_a.append(op)

    add_2_b = []
    for op in father_1[1]:
        if(op not in aux_2):
            add_2_b.append(op)

    # Create decendent 2
    if(a_2 > len(add_2_a)):
        op_2_a = add_2_a + cut_2_a
    else:
        op_2_a = add_2_a[0:a_2] + cut_2_a + add_2_a[a_2:len(add_2_a)]

    if(b_2 > len(add_2_b)):
        op_2_b = add_2_b + cut_2_b
    else:
        op_2_b = add_2_b[0:b_2] + cut_2_b + add_2_b[b_2:len(add_2_b)]

    decendent_2 = [op_2_a, op_2_b]

    # Return results
    return decendent_1, decendent_2

def insertion_mutation(decendent):
    """
    The 'order_crossover' function performs the mutation operator in a decendent.

    Args:
        decendent: Original individual.

    Returns:
        decendent: Mutated individual.
    """

    # Operation selected to mutate
    op = randrange(1, len(decendent[0]) + len(decendent[1]))

    # Seletion of the selected operation
    if(op in decendent[0]):
        decendent[0].remove(op)
    else:
        decendent[1].remove(op)

    # Insertion of the selected operation
    if(getrandbits(1)):
        decendent[0].insert(randrange(0, len(decendent[0])), op)
    else:
        decendent[1].insert(randrange(0, len(decendent[1])), op)

    # Return results
    return decendent

def produce_individuals(features, data, list_fathers, size, prob_mut):
    """
    The 'produce_individuals' function generates new individuals from the parents
    using the crossover and mutation operators.

    Args:
        features: Dictionary of machine features and extensions values ("Xmin",
            "Xmax", "Ymax", "M1_head_A", "M2_head_B", "M3_collision",
            "exten_head_A", "exten_head_B").
        data: List with the values of the operations (columns "ops", "t", "x",
            "y", "seq").
        list_fathers: List with the individuals chosen as parents.
        size: Number of individuals of the generation.
        prob_mut: Probability of making a mutation.

    Returns:
        list_decendents: List with the new individuals.
    """

    # Initialization of result variable
    list_decendents = []

    for i in range(size//2):
        # Initialization of auxiliary variables
        # Crossover with order
        decendent_1, decendent_2 = order_crossover(list_fathers[0], list_fathers[1])

        # Insertion mutation
        if(choices([0, 1], weights=[1 - prob_mut, prob_mut])[0]):
            decendent_1 = insertion_mutation(decendent_1)

        if(choices([0, 1], weights=[1 - prob_mut, prob_mut])[0]):
            decendent_2 = insertion_mutation(decendent_2)

        # Call to finishing correction function
##        decendent_1[0], decendent_1[1] = correct_finishing(features, data, decendent_1[0], decendent_1[1])
##        decendent_2[0], decendent_2[1] = correct_finishing(features, data, decendent_2[0], decendent_2[1])

        # Call to objective function
        percent_1, d_head_a_1, d_head_b_1 = objective_function(features, data, decendent_1[0], decendent_1[1])
        percent_2, d_head_a_2, d_head_b_2 = objective_function(features, data, decendent_2[0], decendent_2[1])

        # The new individuals are added
        list_decendents.append([decendent_1[0], decendent_1[1], percent_1])
        list_decendents.append([decendent_2[0], decendent_2[1], percent_2])

    # Return results
    return list_decendents