#!/usr/bin/env python
"""
"""

import psyco; psyco.full()

from Utils import factorial, num_to_digits
from sets import Set

def sumOfFactDigits(n): return sum(map(factorial,num_to_digits(n)))

def factCycle(n,maxiter=1000):
    terms = Set()
    for i in range(maxiter):
        terms.add(n)
        n = sumOfFactDigits(n)
        if n in terms: break
    else:
        raise "maxiter %d reached in factCycle" % maxiter
    return len(terms)

nmax = 1000000
long_seqs = []
for i in range(nmax):
    nterms = factCycle(i)
    if nterms >= 60: long_seqs.append(i)

print len(long_seqs),long_seqs
# gives 402 entries >= 60 below 1 000 000




    
