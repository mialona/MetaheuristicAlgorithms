def checking(data, op, check, collision_num):
    """
    The 'checking' auxiliary function update variables check and collision_num.

    Args:
        data: List with the values of the operations.
        op: Operation id to check.
        check: List of operations already checked.
        collision_num: Number of collisions.

    Returns:
        check: New list of operations already checked.
        collision_num: New number of collisions.
    """

    # A collision occurs if a finishing operation occurs before its corresponding roughing operation
    if(data[op][4] != 0):
        if(check[data[op][4]-1] != 1):
            collision_num = collision_num + 1 # Update collision_num
    else:
        check[op] = 1 # Update check

    # Return results
    return check, collision_num

def objective_function(data, ops_a, ops_b, M3_collision):
    """
    The 'objective_function' function calculates the efficiency percentage value
    for the given solution (0-100 for solutions with collisions and 100-200 for
    viable solutions) and the lists with the solution of operations in each head
    (with wait operations = -1).

    Args:
        data: List with the values of the operations.
        ops_a: List with the id of operations in head A.
        ops_b: List with the id of operations in head B.
        M3_collision: Minimum distance between heads.

    Returns:
        percent: Solution efficiency percentage.
        d_head_a: List with the solution of operations in head A.
        d_head_b: List with the solution of operations in head B.
    """

    # Calculation of the sum of total time without wait operations
    sum_without_dead_time = 0
    for row in data:
        sum_without_dead_time = sum_without_dead_time + row[1]

    # Number of operations in each head
    len_ops_a = len(ops_a)
    len_ops_b = len(ops_b)

    # Initialization of result variables
    d_head_a = []
    d_head_b = []

    # Initialization of auxiliary variables
    check = [0]*len(data) # List of operations already checked
    t_a = 0.0 # Current time of head A
    t_b = 0.0 # Current time of head B
    op_a = 0 # Current operation of head A
    op_b = 0 # Current operation of head B
    collision_num = 0 # Number of collisions

    # Check loop while there are still operations left on both heads
    while(op_a < len_ops_a and op_b < len_ops_b):
        # If both heads start a new operation at the same time
        if(t_a == t_b):
            # If a collision occurs
            if(abs(data[ops_b[op_b]-1][2] - data[ops_a[op_a]-1][2]) < M3_collision):
                # Operation added to head A (always predominates)
                d_head_a.append([ops_a[op_a], data[ops_a[op_a]-1][1], t_a])
                check, collision_num = checking(data, ops_a[op_a]-1, check, collision_num)

                # Operation -1 on head B until the operation of head A is finished
                d_head_b.append([-1, data[ops_a[op_a]-1][1], t_b])

                # Auxiliary variables are updated
                t_a = t_a + data[ops_a[op_a]-1][1]
                t_b = t_b + data[ops_a[op_a]-1][1]
                op_a = op_a + 1

            # If there is no collision
            else:
                # Operation added to head A
                d_head_a.append([ops_a[op_a], data[ops_a[op_a]-1][1], t_a])
                check, collision_num = checking(data, ops_a[op_a]-1, check, collision_num)

                # Operation added to head B
                d_head_b.append([ops_b[op_b], data[ops_b[op_b]-1][1], t_b])
                check, collision_num = checking(data, ops_b[op_b]-1, check, collision_num)

                # Auxiliary variables are updated
                t_a = t_a + data[ops_a[op_a]-1][1]
                t_b = t_b + data[ops_b[op_b]-1][1]
                op_a = op_a + 1
                op_b = op_b + 1
        else:
            # If head B was already doing an operation when head A starts a new operation
            if(t_a < t_b):
                # If a collision occurs
                if(abs(data[ops_b[op_b-1]-1][2] - data[ops_a[op_a]-1][2]) < M3_collision):
                    # Operation -1 on head A until the operation of head B is finished
                    d_head_a.append([-1, t_b-t_a, t_a])
                    t_a = t_b

                # If there is no collision
                else:
                    # Operation added to head A
                    d_head_a.append([ops_a[op_a], data[ops_a[op_a]-1][1], t_a])

                    # Auxiliary variables are updated
                    check, collision_num = checking(data, ops_a[op_a]-1, check, collision_num)
                    t_a = t_a + data[ops_a[op_a]-1][1]
                    op_a = op_a + 1

            # If head A was already doing an operation when head B starts a new operation
            else:
                # If a collision occurs
                if(abs(data[ops_b[op_b]-1][2] - data[ops_a[op_a-1]-1][2]) < M3_collision):
                    # Operation -1 on head B until the operation of head A is finished
                    d_head_b.append([-1, t_a-t_b, t_b])
                    t_b = t_a

                # If there is no collision
                else:
                    # Operation added to head B
                    d_head_b.append([ops_b[op_b], data[ops_b[op_b]-1][1], t_b])

                    # Auxiliary variables are updated
                    check, collision_num = checking(data, ops_b[op_b]-1, check, collision_num)
                    t_b = t_b + data[ops_b[op_b]-1][1]
                    op_b = op_b + 1

    # Check loop while there are still operations left only on head A
    while(op_a < len_ops_a):
        # If there is no collision
        if(t_a >= t_b or not abs(data[ops_b[op_b-1]-1][2] - data[ops_a[op_a]-1][2]) < M3_collision):
            # Operation added to head A
            d_head_a.append([ops_a[op_a], data[ops_a[op_a]-1][1], t_a])

            # Auxiliary variables are updated
            check, collision_num = checking(data, ops_a[op_a]-1, check, collision_num)
            t_a = t_a + data[ops_a[op_a]-1][1]
            op_a = op_a + 1

        # If a collision occurs
        else:
            # Operation -1 on head A until the operation of head B is finished
            d_head_a.append([-1, t_b-t_a, t_a])
            t_a = t_b

    # Check loop while there are still operations left only on head B
    while(op_b < len_ops_b):
        # If there is no collision
        if(t_b >= t_a or not abs(data[ops_b[op_b]-1][2] - data[ops_a[op_a-1]-1][2]) < M3_collision):
            # Operation added to head B
            d_head_b.append([ops_b[op_b], data[ops_b[op_b]-1][1], t_b])

            # Auxiliary variables are updated
            check, collision_num = checking(data, ops_b[op_b]-1, check, collision_num)
            t_b = t_b + data[ops_b[op_b]-1][1]
            op_b = op_b + 1

        # If a collision occurs
        else:
            # Operation -1 on head B until the operation of head A is finished
            d_head_b.append([-1, t_a-t_b, t_b])
            t_b = t_a

    # Calculation of the percentage of efficiency
    percent = (sum_without_dead_time*100)/(max(t_a,t_b) + collision_num*10000.0)

    # Return results
    return percent, d_head_a, d_head_b