from random import sample, choices

def create_data(features, num_ops_a, num_ops_b, is200):
    """
    The 'create_data' function manages the creation of random instances for the
    problem of a double head machine.

    Args:
        features: Dictionary of machine features and extensions values ("Xmin",
            "Xmax", "Ymax", "M1_head_A", "M2_head_B", "M3_collision",
            "exten_head_A", "exten_head_B").
        num_ops_a: Number of operations in the work area of the first head.
        num_ops_b: Number of operations in the work area of the second head.
        is200: Existence of at least one solution with 200% efficiency.

    Returns:
        data: List with the values of the operations (columns "ops", "t", "x",
            "y", "seq").
    """

    # Initiation of the vectors corresponding to each head
    ops_a = list(range(1, num_ops_a + 1)) # Id of the operations of head A
    ops_b = list(range(num_ops_a + 1, num_ops_a + num_ops_b + 1)) # Id of the operations of head B
    t_a = [0]*num_ops_a # Head A times
    t_b = [0]*num_ops_b # Head B times
    x_a = [0]*num_ops_a # X coordinates of head A
    x_b = [0]*num_ops_b # X coordinates of head B
    y_a = [0]*num_ops_a # Y coordinates of head A
    y_b = [0]*num_ops_b # Y coordinates of head B
    seq_a = [0]*num_ops_a # Head A sequences
    seq_b = [0]*num_ops_b # Head B sequences

    ###########################################
    # Generation of time and sequence vectors #
    ###########################################
    possible_times = list(range(10,71)) # Possible times
    num_ops_a_2 = num_ops_a//2 # Integer half of operations of head A
    num_ops_b_2 = num_ops_b//2 # Integer half of operations of head B

    # Head A times and sequences
    for i in range(num_ops_a_2):
        t_a[i] = sample(possible_times, k = 1)[0] # Roughing operations times
        t_a[i + num_ops_a_2] = choices([t_a[i]/2, t_a[i]/2 + 0.5, t_a[i]/2 - 0.5], [0.3,0.4,0.3], k = 1)[0] # Finishing operation times (half of its finishing operation or +/-0.5)
        seq_a[i + num_ops_a_2] = i + 1 # Sequence of finishing operations

    # Times and sequences of the last operation of head A (if num_ops_a odd)
    if(num_ops_a%2 != 0):
        t_a[num_ops_a - 1] = sample(possible_times, k = 1)[0] # Roughing operation time

    # Head B times and sequences
    for i in range(num_ops_b_2):
        t_b[i] = sample(possible_times, k = 1)[0] # Roughing operations times
        t_b[i + num_ops_b_2] = choices([t_b[i]/2, t_b[i]/2 + 0.5, t_b[i]/2 - 0.5], [0.3,0.4,0.3], k = 1)[0] # Finishing operation times (half of its finishing operation or +/-0.5)
        seq_b[i + num_ops_b_2] = i + num_ops_a + 1 # Sequence of finishing operations

    # Times and sequences of the last operation of head B (if num_ops_b odd)
    if(num_ops_b%2 != 0):
        t_b[num_ops_b - 1] = sample(possible_times, k = 1) [0] # Roughing operation time


    # Timing setting for 200% efficiency (is200 true)
    if(is200):
        sum_t_a = sum(t_a) # Sum of head A times
        sum_t_b = sum(t_b) # Sum of head B times
        difference = abs(sum_t_a - sum_t_b) # Difference between the sum of times of the two heads

        # Incorporation of the difference (distributed) between the operations of the head with the smallest sum of times
        if(sum_t_a < sum_t_b):
            for i in range(num_ops_a_2):
                # Two thirds are allocated to roughing operations and one third to finishing operations to maintain the ratio of the time between the heads
                t_a[i] = t_a[i] + (difference*2/3)//num_ops_a_2
                t_a[i + num_ops_a_2] = t_a[i + num_ops_a_2] + (difference/3)//num_ops_a_2

            # The remainders of the integer division are added to the last operation of A
            t_a[num_ops_a - 1] = round(t_a[num_ops_a - 1] + (difference*2/3)%num_ops_a_2 + (difference/3)%num_ops_a_2, 2)
        else:
            for i in range(num_ops_b_2):
                # Two thirds are allocated to roughing operations and one third to finishing operations to maintain the ratio of the time between the heads
                t_b[i] = t_b[i] + (difference*2/3)//num_ops_b_2
                t_b[i + num_ops_b_2] = t_b[i + num_ops_b_2] + (difference/3)//num_ops_b_2

            # The remainders of the integer division are added to the last operation of B
            t_b[num_ops_b - 1] = round(t_b[num_ops_b- 1] + (difference*2/3)%num_ops_b_2 + (difference/3)%num_ops_b_2, 2)


    ################################################
    # Generation of the X and Y coordinate vectors #
    ################################################
    # Creation of start and end time vectors for head A operations
    t_start_a = [0]*num_ops_a # Start times of A
    t_end_a = [t_a[0]]*num_ops_a # End times of A
    for i in range(1, num_ops_a):
        t_start_a[i] = t_start_a[i-1] + t_a[i-1]
        t_end_a[i] = t_end_a[i-1] + t_a[i]

    # Creation of start and end time vectors for head B operations
    t_start_b = [0]*num_ops_b # Start times of B
    t_end_b = [t_b[0]]*num_ops_b # End times of B
    for i in range(1, num_ops_b):
        t_start_b[i] = t_start_b[i-1] + t_b[i-1]
        t_end_b[i] = t_end_b[i-1] + t_b[i]


    # Generation of the X and Y coordinates of head A
    for i in range(num_ops_a_2):
        x_a[i] = sample(range(features["Xmin"], features["M1_head_A"] + 1), k = 1)[0] # Roughing X coordinates
        x_a[i + num_ops_a_2] = x_a[i] # Finish X coordinates

        y_a[i] = sample(range(0, features["Ymax"] + 1), k = 1)[0] # Roughing Y coordinates
        y_a[i + num_ops_a_2] = y_a[i] # Finish Y coordinates

    # X and Y coordinates of the last operation of head A
    if(num_ops_a%2 != 0):
        x_a[num_ops_a - 1] = sample(range(features["Xmin"], features["M1_head_A"] + 1), k = 1)[0] # Roughing X coordinate
        y_a[num_ops_a - 1] = sample(range(0, features["Ymax"] + 1), k = 1)[0] # Roughing Y coordinate


    # Generation of the X and Y coordinates of head B for 200% efficiency (is200 true)
    if(is200):
        # Generation for 200% efficiency (is200 true)
        for i in range(num_ops_b_2):
            # For the generation of the X coordinates, the maximum between:
            # the minimum coordinate of the head of B and the coordinates of the operations of A (plus the minimum
            # distance between heads) that coincide in time with the roughing and finishing operations of B.
            aux = []
            for j in range(num_ops_a):
                if((t_start_a[j] <= t_end_b[i]) & (t_end_a[j] >= t_start_b[i])):
                    aux.append(features["M3_collision"] + x_a[j])

                if((t_start_a[j] <= t_end_b[i + num_ops_b_2]) & (t_end_a[j] >= t_start_b[i + num_ops_b_2])):
                    aux.append(features["M3_collision"] + x_a[j])

            x_b[i] = sample(range(max([features["M2_head_B"]] + aux), features["Xmax"] + 1), k = 1)[0] # Roughing X coordinates
            x_b[i + num_ops_b_2] = x_b[i] # Finish X coordinates

            y_b[i] = sample(range(0, features["Ymax"] + 1), k = 1)[0] # Roughing Y coordinates
            y_b[i + num_ops_b_2] = y_b[i] # Finish Y coordinates

        # X and Y coordinates of the last operation of head B
        if(num_ops_b%2 != 0):
            aux = []
            for j in range(num_ops_a):
                if((t_start_a[j] <= t_end_b[num_ops_b - 1]) & (t_end_a[j] >= t_start_b[num_ops_b - 1])):
                    aux.append(features["M3_collision"] + x_a[j])

            x_b[num_ops_b - 1] = sample(range(max([features["M2_head_B"]] + aux), features["Xmax"] + 1), k = 1)[0] # Roughing X coordinate
            y_b[num_ops_b - 1] = sample(range(0, features["Ymax"] + 1), k = 1)[0] # Roughing Y coordinate

    else:
        # Generation for not necessarily 200% efficiency (is200 false)
        for i in range(num_ops_b_2):
            x_b[i] = sample(range(features["M2_head_B"], features["Xmax"] + 1), k = 1)[0] # Roughing X coordinates
            x_b[i + num_ops_b_2] = x_b[i] # Finish X coordinates

            y_b[i] = sample(range(0, features["Ymax"]), k = 1)[0] # Roughing Y coordinates
            y_b[i + num_ops_b_2] = y_b[i] # Finish Y coordinates

        # X and Y coordinates of the last operation of head B
        if(num_ops_b%2 != 0):
            x_b[num_ops_b - 1] = sample(range(features["M2_head_B"], features["Xmax"] + 1), k = 1)[0] # Roughing X coordinate
            y_b[num_ops_b - 1] = sample(range(0, features["Ymax"]), k = 1)[0] # Roughing Y coordinate


    # Creation of the matrix from the union of the lists of each head
    data = []
    for i in range(num_ops_a):
        data.append([ops_a[i], t_a[i], x_a[i], y_a[i], seq_a[i]])

    for i in range(num_ops_b):
        data.append([ops_b[i], t_b[i], x_b[i], y_b[i], seq_b[i]])

    # Return results
    return data