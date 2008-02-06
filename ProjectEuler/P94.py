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
from math import sqrt

def heron_area(a,b,c):
    "Area of a triangle with sides a,b,c"
    p = (a+b+c)/2.
    return sqrt(p*(p-a)*(p-b)*(p-c))

def area2(a,b):
    "Area of a triangle with sides a,a,b"
    a2 = a*a
    b2 = b*b
    return b*sqrt(4*a2-b2)/4.

def brute1(plimit=1000):
    slimit = plimit/3+1
    sump = 0
    for a in xrange(2,slimit):
        if a % 10**7 == 0: print "At step ",a
        for b in [a-1,a+1]:
            p = 2*a+b
            if p > plimit: break
            area=area2(a,b)
            if isint(area):
                sump += p
    print "sump for p < %d = %d" % (plimit,sump)
    return

def brute2(plimit=100):
    slimit = plimit/3 + 1
    sump = 0
    for a in xrange(3,slimit):
        if isint(area2(a,a+1)):
            sump += 3*a+1
        elif isint(area2(a,a-1)):
            sump += 3*a-1
    print "sump for p < %d = %d" % (plimit,sump)
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
#  that I've tested. Brute1 is much faster, since it scales linearly
#
#  pmax          sum_p                  time
#  50,000        51,406                 0.0779 sec
#  100,000       51,406                 0.165 sec
#  10**6         1,905,576              2.256 sec
#  10**7         12,405,628,833         23.55 sec
#  10**8         127,140,974,991,072    266.24
#  10**9         312,530,319,954,683,775 2905 2905
# This should be right, but it's wrong.
def main():
    from time import time
    pmax = 10**9
    #t0 = time()
    #brute1(pmax)
    t1 = time()
    #print t1-t0
    brute2(pmax)
    print time()-t1
    return

if __name__ == '__main__': main()
