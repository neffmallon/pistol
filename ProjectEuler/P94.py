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

from Utils import isint

def heron_area(a,b,c):
    from math import sqrt
    p = (a+b+c)/2.
    return sqrt(p*(p-a)*(p-b)*(p-c))
    

def main(plimit=20):
    slimit = plimit/3
    sump = 0
    for a in xrange(1,slimit):
        if a == 1:
            choices = [a+1]
        else:
            choices = [a-1,a+1]
        for b in choices:
            p = 2*a+b
            if p > plimit: continue
            area = heron_area(a,a,b)
            if area == 0: continue
            if isint(area):
                sump += p
    print sump
    return


if __name__ == '__main__': main(1000000000)

