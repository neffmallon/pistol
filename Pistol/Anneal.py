#!/usr/bin/env python
"""\
 Anneal.py - Simple Simulated Annealing in Python

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

from random import random
from math import exp

def Anneal(objective,variator,bounds,Tstep=0.9,NT=100,
           Nsteps=100,Nlimit=10):
    """Multi-dimensional Simulated Annealing Optimization
    objective     A function of (x1,x2,...) , bounded by bounds
    variator      A function to modify the values of (x1,x2,...)
    bounds        List of tuples [(min1,max1),(min2,max2), ...]
    Tstep         Amount to decrease T by each temperature step
    NT            Number of T steps to cycle through
    Nsteps        Number of points to sample at each T step
    Nlimit        Maximum successful changes before continuing
    """

    x = GetStartingValues(bounds) # random point between xmin and xmax
    T = Tstart(x,objective,variator,bounds)

    for i in range(NT):
        Nsucc = 0
        for j in range(Nsteps):
            xnew = variator(x,bounds)
            dE = objective(xnew)-objective(x)
            if dE < 0 or random() < exp(-dE/T):
                x = xnew
                Nsucc += 1
            if Nsucc >= Nlimit: break
        if Nsucc == 0: break # no successes -> converged
        T*= Tstep
    xfinal = x

    return xfinal

def GetStartingValues(bounds):
    "Get random values between the bounds for the functions"
    return [mini+random()*(maxi-mini) for (mini,maxi) in bounds]

def Tstart(x,objective,variator,bounds):
    """Run 10 random variations from the starting guess to obtain   
    an initial temperature""" 
    E0 = objective(x) 
    Es = []
    for i in range(10):
        xnew = variator(x,bounds)
        Es.append(objective(xnew))
    T = 2*max(map(lambda E,E0=E0: abs(E-E0),Es))
    return T

def TestFunc(x):
    from math import cos
    val = 0
    for xi in x: val+= xi*xi-cos(10*xi)
    return val

def SimpleVariator(x,bounds):
    xnew = []
    for i in range(len(x)):
        xmax,xmin = bounds[i]
        var = 0.1*(xmax-xmin)
        xnew.append(x[i] + var*(2*random()-1))
    return xnew

def test():
    val = Anneal(TestFunc,SimpleVariator,[(-5,5)])
    print "Final value ",val,TestFunc(val)

if __name__ == '__main__': test()

        

