"""
The radical of n, rad(n), is the product of distinct prime factors of
n. For example, 504 = 2^3 x 3^2 x 7, so rad(504) = 2 x 3 x 7 = 42.

We shall define the triplet of positive integers (a, b, c) to be an
abc-hit if:

   1. GCD(a, b) = GCD(a, c) = GCD(b, c) = 1
   2. a < b
   3. a + b = c
   4. rad(abc) < c

For example, (5, 27, 32) is an abc-hit, because:

   1. GCD(5, 27) = GCD(5, 32) = GCD(27, 32) = 1
   2. 5 < 27
   3. 5 + 27 = 32
   4. rad(4320) = 30 < 32

It turns out that abc-hits are quite rare and there are only
thirty-one abc-hits for c < 1000, with sum c = 12523.

Find sum c for c < 110000.
"""

from Utils import prime_factors,prod,primes,timeit
from Utilsfast import gcd

pfcache = {}
def pffast(a,ps):
    if a in pfcache: return pfcache[a]
    pfa = prime_factors(a,ps)
    pfcache[a] = pfa
    return pfa

def abchits(nmax):
    ps = primes(nmax)
    sumc = 0
    for c in xrange(1,nmax):
        cfactors = [1] + pffast(c,ps)
        for b in xrange(c/2+1,c):
            if gcd(c,b) > 1: continue
            bcfactors = cfactors + pffast(b,ps)
            if prod(bcfactors) > c: continue
            a = c-b
            if gcd(c,a)+gcd(b,a) > 2: continue
            abcfactors = bcfactors + pffast(a,ps)
            if prod(abcfactors) < c:
                sumc += c
                print a,b,c,sumc
    print sumc
    return

def profabc():
    import cProfile,pstats
    cProfile.run('abchits(5000)','prof')
    prof = pstats.Stats('prof')
    prof.strip_dirs().sort_stats('time').print_stats(15)

def main():
    from time import time
    #profabc()
    t0 = time()
    abchits(110000)
    t1 = time()
    print t1-t0

if __name__ == '__main__': main()

