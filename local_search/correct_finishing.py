def checking_a(data, op, check, collision_num, ops_a, ops_aux_a, collisions_a, collisions_b):
    """
    The 'checking_a' auxiliary function update variables check and collision_num
    and add the operation to the corresponding list ("ops_aux_a", "collisions_a"
    or "collisions_b").

    Args:
        data: List with the values of the operations.
        op: Operation id to check.
        check: List of operations already checked.
        collision_num: Number of collisions.
        ops_a: List with the id of operations in head A.
        ops_aux_a: List of operations without collisions in head A
        collisions_a: List of operations with collisions in head A
        collisions_b: List of operations with collisions in head B

    Returns:
        check: New list of operations already checked.
        collision_num: New number of collisions.
        ops_aux_a: New list of operations without collisions in head A
        collisions_a: New list of operations with collisions in head A
        collisions_b: New list of operations with collisions in head B
    """

    # It's a finishing operation
    if(data[op][4] != 0):
        # Finishing operation occurs before its corresponding roughing operation
        if(check[data[op][4]-1] != 1):
            collision_num = collision_num + 1 # Update collision_num

            # Its corresponding roughing operation is in head A or head B
            if(data[op][4] in ops_a):
                collisions_a.append(op+1) # Add the operation to the "collisions_a" list
            else:
                collisions_b.append(op+1) # Add the operation to the "collisions_b" list
        else:
            ops_aux_a.append(op+1) # Add the operation to the "ops_aux_a" list

    # It's a roughing operation
    else:
        check[op] = 1 # Update check
        ops_aux_a.append(op+1) # Add the operation to the "ops_aux_a" list

    # Return results
    return check, collision_num, ops_aux_a, collisions_a, collisions_b


def checking_b(data, op, check, collision_num, ops_b, ops_aux_b, collisions_a, collisions_b):
    """
    The 'checking_b' auxiliary function update variables check and collision_num
    and add the operation to the corresponding list ("ops_aux_b", "collisions_a"
    or "collisions_b").

    Args:
        data: List with the values of the operations.
        op: Operation id to check.
        check: List of operations already checked.
        collision_num: Number of collisions.
        ops_b: List with the id of operations in head B.
        ops_aux_b: List of operations without collisions in head B.
        collisions_a: List of operations with collisions in head A.
        collisions_b: List of operations with collisions in head B.

    Returns:
        check: New list of operations already checked.
        collision_num: New number of collisions.
        ops_aux_b: New list of operations without collisions in head B.
        collisions_a: New list of operations with collisions in head A.
        collisions_b: New list of operations with collisions in head B.
    """

    # It's a finishing operation
    if(data[op][4] != 0):
        # Finishing operation occurs before its corresponding roughing operation
        if(check[data[op][4]-1] != 1):
            collision_num = collision_num + 1 # Update collision_num

            # Its corresponding roughing operation is in head A or head B
            if(data[op][4] in ops_b):
                collisions_b.append(op+1) # Add the operation to the "collisions_a" list
            else:
                collisions_a.append(op+1) # Add the operation to the "collisions_b" list
        else:
            ops_aux_b.append(op+1) # Add the operation to the "ops_aux_b" list

    # It's a roughing operation
    else:
        check[op] = 1 # Update check
        ops_aux_b.append(op+1) # Add the operation to the "ops_aux_b" list

    # Return results
    return check, collision_num, ops_aux_b, collisions_a, collisions_b

def correct_finishing(data, ops_a, ops_b, M3_collision):
    """
    The 'correct_finishing' function .

    Args:
        data: List with the values of the operations.
        ops_a: List with the id of operations in head A.
        ops_b: List with the id of operations in head B.
        M3_collision: Minimum distance between heads.

    Returns:
        ops_a: New list with the id of operations in head A.
        ops_b: New list with the id of operations in head B.
    """

    # The loop continues until there are no collisions.
    collision_num = None # Number of collisions
    while(collision_num != 0):
        collision_num = 0

        # Number of operations in each head
        len_ops_a = len(ops_a)
        len_ops_b = len(ops_b)

        # Initialization of auxiliary variables
        check = [0]*len(data) # List of operations already checked
        ops_aux_a = [] # List of operations without collisions in head A
        ops_aux_b = [] # List of operations without collisions in head B
        collisions_a = [] # List of operations with collisions in head A
        collisions_b = [] # List of operations with collisions in head B
        t_a = 0.0 # Current time of head A
        t_b = 0.0 # Current time of head B
        op_a = 0 # Current operation of head A
        op_b = 0 # Current operation of head B

        # Check loop while there are still operations left on both heads
        while(op_a < len_ops_a and op_b < len_ops_b):
            # If both heads start a new operation at the same time
            if(t_a == t_b):
                # If a collision occurs
                if(abs(data[ops_b[op_b]-1][2] - data[ops_a[op_a]-1][2]) < M3_collision):
                    # Call to checking operation head A function
                    check, collision_num, ops_aux_a, collisions_a, collisions_b = checking_a(data, ops_a[op_a]-1, check, collision_num, ops_a, ops_aux_a, collisions_a, collisions_b)

                    # Auxiliary variables are updated
                    t_a = t_a + data[ops_a[op_a]-1][1]
                    t_b = t_b + data[ops_a[op_a]-1][1]
                    op_a = op_a + 1

                # If there is no collision
                else:
                    # Call to checking operation head A function
                    check, collision_num, ops_aux_a, collisions_a, collisions_b = checking_a(data, ops_a[op_a]-1, check, collision_num, ops_a, ops_aux_a, collisions_a, collisions_b)

                    # Call to checking operation head B function
                    check, collision_num, ops_aux_b, collisions_a, collisions_b = checking_b(data, ops_b[op_b]-1, check, collision_num, ops_b, ops_aux_b, collisions_a, collisions_b)

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
                        # Auxiliary variables are updated
                        t_a = t_b

                    # If there is no collision
                    else:
                        # Call to checking operation head A function
                        check, collision_num, ops_aux_a, collisions_a, collisions_b = checking_a(data, ops_a[op_a]-1, check, collision_num, ops_a, ops_aux_a, collisions_a, collisions_b)

                        # Auxiliary variables are updated
                        t_a = t_a + data[ops_a[op_a]-1][1]
                        op_a = op_a + 1

                # If head A was already doing an operation when head B starts a new operation
                else:
                    # If a collision occurs
                    if(abs(data[ops_b[op_b]-1][2] - data[ops_a[op_a-1]-1][2]) < M3_collision):
                        # Auxiliary variables are updated
                        t_b = t_a

                    # If there is no collision
                    else:
                        # Call to checking operation head B function
                        check, collision_num, ops_aux_b, collisions_a, collisions_b = checking_b(data, ops_b[op_b]-1, check, collision_num, ops_b, ops_aux_b, collisions_a, collisions_b)

                        # Auxiliary variables are updated
                        t_b = t_b + data[ops_b[op_b]-1][1]
                        op_b = op_b + 1

        # Check loop while there are still operations left only on head A
        while(op_a < len_ops_a):
            # If there is no collision
            if(t_a >= t_b or not abs(data[ops_b[op_b-1]-1][2] - data[ops_a[op_a]-1][2]) < M3_collision):
                # Call to checking operation head A function
                check, collision_num, ops_aux_a, collisions_a, collisions_b = checking_a(data, ops_a[op_a]-1, check, collision_num, ops_a, ops_aux_a, collisions_a, collisions_b)

                # Auxiliary variables are updated
                t_a = t_a + data[ops_a[op_a]-1][1]
                op_a = op_a + 1

            # If a collision occurs
            else:
                # Auxiliary variables are updated
                t_a = t_b

        # Check loop while there are still operations left only on head B
        while(op_b < len_ops_b):
            # If there is no collision
            if(t_b >= t_a or not abs(data[ops_b[op_b]-1][2] - data[ops_a[op_a-1]-1][2]) < M3_collision):
                # Call to checking operation head B function
                check, collision_num, ops_aux_b, collisions_a, collisions_b = checking_b(data, ops_b[op_b]-1, check, collision_num, ops_b, ops_aux_b, collisions_a, collisions_b)

                # Auxiliary variables are updated
                t_b = t_b + data[ops_b[op_b]-1][1]
                op_b = op_b + 1

            # If a collision occurs
            else:
                # Auxiliary variables are updated
                t_b = t_a

        # Add the operations with collision to the end of the operation lists of each head
        ops_a = ops_aux_a + collisions_a
        ops_b = ops_aux_b + collisions_b

        # If the list of operations of head A is empty, two operations of head B are passed to it
        if(len(ops_a) == 0 and len(ops_b) > 2):
            ops_a = ops_b[0:2]
            ops_b = ops_b[2:len(ops_b)]
            collision_num = None # Finishing operations are corrected again

        # If the list of operations of head A is empty, two operations of head B are passed to it
        if(len(ops_b) == 0 and len(ops_a) > 2):
            ops_b = ops_a[0:2]
            ops_a = ops_a[2:len(ops_a)]
            collision_num = None # Finishing operations are corrected again

    # Return results
    return ops_a, ops_b