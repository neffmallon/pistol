"""
Problem 58 

Starting with 1 and spiralling anticlockwise in the following way, a
square spiral with side length 7 is formed.

37 36 35 34 33 32 31 
38 17 16 15 14 13 30 
39 18  5  4  3 12 29 
40 19  6  1  2 11 28 
41 20  7  8  9 10 27 
42 21 22 23 24 25 26 
43 44 45 46 47 48 49 

It is interesting to note that the odd squares lie along the bottom
right diagonal, but what is more interesting is that 8 out of the 13
numbers lying along both diagonals are prime; that is, a ratio of 8/13
\approx 62%.

If one complete new layer is wrapped around the spiral above, a square
spiral with side length 9 will be formed. If this process is
continued, what is the side length of the square spiral for which the
ratio of primes along both diagonals first falls below 10%?
"""

import psyco; psyco.full()
from Utils import spiral_matrix,primes,spiral
from MillerRabin import isprime
from sets import Set

def percent_diagonals_prime(m):
    n = m.shape[0]
    ps = primes(n*n)
    pset = Set(ps)
    ntot = 2*n-1
    nprime = 0
    for i in range(n):
        if m[i,i] in pset:
            nprime += 1
        if m[i,-(i+1)] in pset:
            nprime += 1
    return nprime/float(ntot)

def brute(nmax=101):
    m = spiral_matrix(nmax)
    print percent_diagonals_prime(m)
    return

def generator(nmax=101):
    # The following step is the killer: I can't generate enough primes
    # in memory. The GMPY out of core prime routine would probably
    # work here.
    s = spiral()
    ij = 1
    ndiag = 0
    nprime = 0
    #for i in xrange(nmax*nmax):
    i = 0
    while 1:
        i += 1
        x,y = s.next()
        if x==y or x==-y:
            ndiag += 1
            if isprime(ij): nprime += 1
            pct = nprime/float(ndiag)
            print "%3d %3d %3d %5d %.2f" % (i+1,x,y,ij,round(pct,3))
            if i > 100 and pct < 0.1: break
        ij += 1
    return

def prime_test(nmax):
    # Make sure that Miller Rabin agrees with Sieve test
    ps = Set(primes(nmax))
    def isprime2(n): return n in ps
    for i in range(nmax):
        if isprime2(i) != isprime(i): print i, isprime(i),isprime2(i)
    print "Completed prime test through %d" % nmax
    return
        

if __name__ == '__main__':
    #brute(101)
    generator(100001)

