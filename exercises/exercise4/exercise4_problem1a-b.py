#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A course example of one-dimensional heat conduction.

KEB-45250
Numerical Techniques for Process Modelling,
Prosessien numeerinen mallinnus

Exercice 4 problem 1a-b

Emphesis on simplisity. Low performance in larger systems.

Created on 2018 Jan 5 

@author: Antti Mikkonen, a.mikkonen@iki.fi
"""
import scipy as sp
from matplotlib import pyplot as plt

##############################################################################

def solver(n, kt, Ac, L, T_A, T_B, q=0):
    
    # Cell size
    dx = L / n
    # Coefficients
    aW = kt/dx*Ac
    aE = kt/dx*Ac
    
    # Source vector
    b = sp.zeros(n)
    # Coefficient matrix
    A = sp.zeros((n,n))

    # Add aW to matrix A
    for k in range(1,n):
        A[k,k]   += aW
        A[k,k-1] += -aW
#    print("A with aW\n", A)
    
    # Add aE to matrix A
    for k in range(n-1):
        A[k,k]   += aE
        A[k,k+1] += -aE
#    print("A with aE\n", A)
    
    # Boundary A on the left
    A[0,0] += kt/(dx/2)*Ac
    b[0]   += kt/(dx/2)*Ac*T_A
    
    # Boundary B on the right
    A[-1,-1] += kt/(dx/2)*Ac
    b[-1]    += kt/(dx/2)*Ac*T_B
    
    # Add heat generation
    b += q*Ac*dx
    
    # Solution
    T = sp.linalg.solve(A,b)
    
    # Post
#    print("A\n", A)
#    print("b\n", b)
#    print("T\n",T)
    
    return T, dx
    
    
def analytical(n, kt, Ac, L, T_A, T_B, q, x):

    return ((T_B-T_A)/L + q/2/kt*(L-x))*x + T_A
    
##############################################################################

if __name__ == "__main__":
    print("START")
    # Number of control volumes
    n = 5
    # Thermal conductivity (W/mK)
    kt = 1000
    # Cross-sectional area (m2)
    Ac = 10e-3
    # Lenght (m)
    L = 0.5
    # Boundary temperatures (C)
    T_A = 100
    T_B = 500
    
    # Volumetric heat power (W/m3)
    q = 5e6 # 25kW
    
    T, dx = solver(n, kt, Ac, L, T_A, T_B, q)
    
    x_exact = sp.linspace(0,L)
    T_exact = analytical(n, kt, Ac, L, T_A, T_B, q, x_exact)
    
    
    # Plot numerical and exact solution
    x = sp.linspace(dx/2,L-dx/2,n)    
    plt.plot(x_exact, T_exact, "r", label="exact")
    plt.plot(x, T, "k--o", label="numerical")
    plt.legend()
    plt.xlim(0,L)
    
    print("END")