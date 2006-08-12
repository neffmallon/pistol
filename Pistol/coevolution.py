#!/usr/bin/env python
"""\
 Explore co-evolution models
 Taken from Chapter 7 of Computer Simulations in Mathematica.
"""

from random import random
from Gnuplot import Gnuplot, Data

def frequency(n,least_fit_sites):
    freq = [0]*n
    for site in least_fit_sites:
        freq[site] += 1
    return freq

def coevolution(n=200,nsteps=6000):
    fitness = [random() for i in range(n)]
    least_fit_sites = []

    for step in range(nsteps):
        # Determine the least fit site
        worst = fitness.index(min(fitness))
        left = (worst-1)%n
        right = (worst+1)%n
        # Add that site to the least_fit_sites list
        least_fit_sites.append(worst)
        # Reinitialize the site and its neighbors
        fitness[worst] = random()
        fitness[left] = random()
        fitness[right] = random()

    # Plot how the least fit site changes with time
    p = Gnuplot()
    p.title("Coevolution data for %d steps with %d species" % (nsteps,n))
    p.xlabel("Step")
    d = Data(range(nsteps),least_fit_sites)
    p.plot(d)
    raw_input("press any key to continue")

    # Plot the frequency of the sites in the least_fit_site list:
    p2 = Gnuplot()
    p2.title("Frequency of least fit site")
    d2 = Data(range(n),frequency(n,least_fit_sites))
    p2.plot(d2)
    return

if __name__ == '__main__': coevolution()

