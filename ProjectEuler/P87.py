"""
The smallest number expressible as the sum of a prime square, prime cube, and prime fourth power is 28. In fact, there are exactly four numbers below fifty that can be expressed in such a way:

28 = 2**2 + 2**3 + 2**4
33 = 3**2 + 2**3 + 2**4
49 = 5**2 + 2**3 + 2**4
47 = 2**2 + 3**3 + 2**4

How many numbers below fifty million can be expressed as the sum of a prime square, prime cube, and prime fourth power?
"""

from Utils import primes
from sets import Set

nmax = 50000000
ps = primes(nmax)

p2s = []
p3s = []
p4s = []
for p in ps:
    p2 = p*p
    if p2 > nmax: continue
    p2s.append(p2)

    p3 = p2*p
    if p3 > nmax: continue
    p3s.append(p3)

    p4 = p3*p
    if p4 > nmax: continue
    p4s.append(p4)

print len(ps),len(p2s),len(p3s),len(p4s)


results = Set()
for p4 in p4s:
    for p3 in p3s:
        if p3+p4 > nmax: continue
        for p2 in p2s:
            s = p2+p3+p4
            if s > nmax: continue
            results.add(s)
print len(results)
# I got 1097343 for the result: haven't been able to submit to website yet.


