from math import exp
from decimal import Decimal, getcontext   # 'newton_raphson_algorithm' gives a lot of problems

def v(sigma_a,sigma_b,n,j):
    """
    The auxiliary 'v' function computes the Vj value between two permutations.

    Args:
        sigma_a: First permutation.
        sigma_b: Second permutation.
        n: Number of operations.
        j: Number of positions to the right to consider.

    Returns:
        sum: Vj value.
    """

    # Calculation of the permutation pi resulting from the combination of sigma_a and sigma_b
    pi = []
    for i in range(n):
        pi.append(sigma_a[sigma_b[i] - 1])

    # Calculation of the Vj value
    sum = 0
    for i in range(j+1,n):
        if(pi[j] > pi[i]):
            sum = sum + 1

    # Return results
    return sum

def newton_raphson_algorithm(v_j,pre_theta_j,theta_upper,n,j,error_rate):
    """
    The 'newton_raphson_algorithm' function calculates the values of theta_j
    using the Newton Raphson Algorithm.

    Args:
        v_j: Vj value.
        pre_theta_j: Initial value of theta_j.
        theta_upper: Maximum value of theta_j.
        n: Number of operations.
        j: Number of positions to the right to consider.
        error_rate: Error index from which the value of theta_j is considered good.

    Returns:
        theta_j: Vj value.
    """

    # Use of variables with module 'decimal'
    getcontext().prec = 10
    v_j = Decimal(v_j)
    pre_theta_j = Decimal(pre_theta_j)
    theta_upper = Decimal(theta_upper)
    n = Decimal(n)
    j = Decimal(j)
    error_rate = Decimal(error_rate)

    # Newton Raphson Algorithm
    error = error_rate
    while((error >= error_rate) and (pre_theta_j < theta_upper)):
        # Function
        fun = (n-Decimal(1))/(Decimal(exp(pre_theta_j))-Decimal(1)) - (n-j+1)/(Decimal(exp(pre_theta_j*(n-j+Decimal(1))))-Decimal(1)) - v_j

        # Derivative of the function
        der_fun = Decimal(pow(n-j+Decimal(1),2))*Decimal(exp(pre_theta_j*(n-j+Decimal(1))))/Decimal(pow(Decimal(exp(pre_theta_j*(n-j+Decimal(1))))-Decimal(1),2)) - (n-Decimal(1))*Decimal(exp(pre_theta_j))/Decimal(pow(Decimal(exp(pre_theta_j))-1,2))

        # Calculation of the value of theta_j
        theta_j = pre_theta_j - fun/der_fun
        error = abs(theta_j - pre_theta_j)/abs(theta_j)
        pre_theta_j = theta_j

    # Return results
    return float(theta_j)

def spread_parameters(list_sigmas,sigma_0,n):
    """
    The 'spread_parameters' function calculates the value of the spread_parameters.

    Args:
        list_sigmas: List with all the permutations of the current generation.
        sigma_0: Consensus permutation.
        n: Number of operations.

    Returns:
        theta: Spread parameters values.
    """

    # Calculation of the inverse permutation of sigma_0
    inv_sigma_0 = []
    for i in range(n):
        inv_sigma_0.append(sigma_0.index(i + 1) + 1)

    # Calculation of theta values
    theta = []
    for j in range(n-1):
        # Kendall distance calculation
        sum = 0
        for sigma in list_sigmas:
            sum = sum + v(sigma[0],sigma_0,n,j)

        # Calculation of theta_j from the value of v_j
        v_j = sum/len(list_sigmas)
        theta.append(newton_raphson_algorithm(v_j,0.1,10,n,j,0.001)) # Return 'theta_upper' when v_0 = 0

    # Return results
    return theta