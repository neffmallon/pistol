#!/usr/bin/env python
"""\
It is easily proved that no equilateral triangle exists with integral
length sides and integral area. However, the almost equilateral
triangle 5-5-6 has an area of 12 square units.

We shall define an almost equilateral triangle to be a triangle for
which two sides are equal and the third differs by no more than one
unit.

Find the sum of the perimeters of every almost equilateral triangle
with integral side lengths and area and whose perimeters do not exceed
one billion (1,000,000,000).
"""

from sets import Set
from Utils import isint
from time import time

def heron_area(a,b,c):
    "Area of a triangle with sides a,b,c"
    from math import sqrt
    p = (a+b+c)/2.
    return sqrt(p*(p-a)*(p-b)*(p-c))

def brute1(plimit=1000):
    slimit = plimit/3+1
    sump = 0
    for a in xrange(2,slimit):
        for b in [a-1,a+1]:
            p = 2*a+b
            if p > plimit: break
            area = heron_area(a,a,b)
            if isint(area):
                sump += p
    print sump
    return

def with_triples(pmax = 1000):
    hmax = (pmax+3)/3
    trips = pythag_triples(hmax)
    sump = 0
    for a,b,c in trips:
        if abs(c-2*a) == 1:# or abs(c-2*b) == 1:
            if a%2 == 1 and b%2 == 1: print "Odd area"
            p = 2*c + 2*a
            if p > pmax: continue
            sump += p
            #print a,b,c
        elif abs(c-2*b) == 1:
            # I don't think this can happen
            print "B triangle found"
    #sump for p < 10**5 = 51406
    print "sump for p < %d = %d" % (pmax,sump)
    return

def pythag_triples(hmax):
    """
    Set() = pythag_triples(hmax)

    generate all pythagorean triples (a,b,c) where a^2 + b^2 = c^2
    and c < hmax.

    Uses the generator m>n -> a = m^2-n^2, b = 2mn, c = m^2+n^2
        
    """
    results =Set()
    for m in range(1,hmax):
        m2 = m*m
        for n in range(1,m):
            n2 = n*n
            if m2+n2 > hmax: break
            for l in range(1,hmax):
                if l*(m2+n2) > hmax: break
                a = l*(m2-n2)
                b = 2*l*m*n
                c = l*(m2+n2)
                if a > b:
                    a,b = b,a
                results.add((a,b,c))
    return results

# Brute1 and with_triples give identical energies for the cases
#  that I've tested. Also give very similar times.

def main():
    from time import time
    t0 = time()
    with_triples(50000)
    t1 = time()
    print t1-t0
    brute1(50000)
    print time()-t0
    return

if __name__ == '__main__': main()
