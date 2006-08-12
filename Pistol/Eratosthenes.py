#!/usr/bin/env python
"""\
 Sieve of Eratosthenes in Python

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

def eratosthenes(max=10000):
    isprime = []
    primes = []
    for i in range(max): isprime.append(1) #Init to true
    
    for i in range(2,max):
        if isprime[i]:
            primes.append(i)
            j = 2*i
            while j < max:
                isprime[j] = 0
                j = j + i
    return primes

def diff_plot():
    from Gnuplot import Gnuplot, Data
    primes = eratosthenes(5000)
    diffs = []
    for i in range(len(primes)-1):
        diffs.append(primes[i+1]-primes[i])
    d = Data(range(len(diffs)),diffs,with='lines')
    diffhist = [0]*(max(diffs)+1)
    for diff in diffs:
        diffhist[diff] += 1
    #d = Data(range(2,len(diffhist),2),
    #         [diffhist[i] for i in range(2,len(diffhist),2)],
    #         with='lines')
    g = Gnuplot()
    g.plot(d)
    raw_input("press any key to continue")

if __name__ == '__main__': #eratosthenes()
    diff_plot()

