"""
The arithmetic sequence, 1487, 4817, 8147, in which each of the terms
increases by 3330, is unusual in two ways: (i) each of the three terms
are prime, and, (ii) each of the 4-digit numbers are permutations of
one another.

There are no arithmetic sequences made up of three 1-, 2-, or 3-digit
primes, exhibiting this property, but there is one other 4-digit
increasing sequence.

What 12-digit number do you form by concatenating the three terms in
this sequence?
"""

from Utils import primes
from sets import Set

def isperm(a,b):
    as = str(a)
    bs = str(b)
    return len(as) == len(bs) and Set(as) == Set(bs)

p4s = [p for p in primes(10000) if p > 1000]
p4set = Set(p4s)

n = len(p4s)

for i in range(n):
    pi = p4s[i]
    for j in range(i):
        pj = p4s[j]
        if not isperm(pi,pj): continue
        d = pi-pj
        if pi + d in p4set and isperm(pi,pi+d): print pj,pi,pi+d

        
