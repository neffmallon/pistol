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
import psyco; psyco.full()
from sets import Set
from Utils import isint
from time import time

def heron_area(a,b,c):
    "Area of a triangle with sides a,b,c"
    from math import sqrt
    p = (a+b+c)/2.
    return sqrt(p*(p-a)*(p-b)*(p-c))

def brute1(plimit=20):
    slimit = plimit/3
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

# See formula2() of P75.py
def pythag_triples(hmax):
    "generate all pythagorean triples with hypotenuse < hmax"
    # This is too slow to be practical
    results ={}
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
                if c in results:
                    results[c].add((a,b))
                else:
                    results[c] = Set([(a,b)])
    return results
                

if __name__ == '__main__':
    thou = 1000
    mill = thou*thou
    bill = thou*mill
    t0 = time()
    brute1(bill)
    t1 = time()
    print t1-t0



