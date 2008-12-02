"""
A composite is a number containing at least two prime factors. For
example, 15 = 3 x 5; 9 = 3 x 3; 12 = 2 x 2 x 3.

There are ten composites below thirty containing precisely two, not
necessarily distinct, prime factors: 4, 6, 9, 10, 14, 15, 21, 22, 25,
26.

How many composite integers, n < 10^(8), have precisely two, not
necessarily distinct, prime factors?
"""

from math import sqrt
from sets import Set
from Utils import prime_factors,primes

def prime_factors(n,ps):
    for p in ps:
        if p > n: break
        if n == 1:
            return []
        if n % p == 0:
            return [p] + prime_factors(n/p,ps)
    return []

def main(N=10**6,VERBOSE=True):
    ps = primes(N)
    print "There are %d primes less than %d" % (len(ps),N)
    n2s = 0
    for i in ps:
        for j in ps:
            if j > i: break
            if i*j < N:
                n2s += 1
    print "Total 2-composites below %d = %d" % (N,n2s)
    return

if __name__ == '__main__': main()

# 10**2: 34
# 10**3: 299
# 10**4: 2625
# 10**5: 23378
# 10**6: 
