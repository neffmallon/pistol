#!/usr/bin/env python
"""\
Let (a, b, c) represent the three sides of a right angle triangle with
integral length sides. It is possible to place four such triangles
together to form a square with length c.

For example, (3, 4, 5) triangles can be placed together to form a 5 by
5 square with a 1 by 1 hole in the middle and it can be seen that the
5 by 5 square can be tiled with twenty-five 1 by 1 squares.

However, if (5, 12, 13) triangles were used then the hole would
measure 7 by 7 and these could not be used to tile the 13 by 13
square.

Given that the perimeter of the right triangle is less than
one-hundred million, how many Pythagorean triangles would allow such a
tiling to take place?
"""

from sets import Set
from Utils import gcd3,issquare,isqrt

def pythag_triples(pmax):
    """
    Set() = pythag_triples(hmax)

    generate all pythagorean triples (a,b,c) where a^2 + b^2 = c^2
    and c < hmax.

    Uses the generator m>n -> a = m^2-n^2, b = 2mn, c = m^2+n^2
        
    """
    hmax = pmax/2
    results =Set()
    for m in range(1,hmax):
        m2 = m*m
        for n in range(1,m):
            n2 = n*n
            if 2*m*(m+n) > pmax: break
            #for l in range(1,hmax):
            for l in range(1,2):
                if 2*l*m*(m+n) > pmax: break
                a = l*(m2-n2)
                b = 2*l*m*n
                c = l*(m2+n2)
                if gcd3(a,b,c) > 1: continue
                if a > b:
                    a,b = b,a
                results.add((a,b,c))
    return results

nsqs = 10**7
sqs = Set(i*i for i in range(1,nsqs))
print "Done with squares calculation"
def issq(n):
    if n < nsqs: return n in sqs
    return issquare(n)

def pythag_neighbor_triples(pmax):
    "Generate all abc pythagorean triplets where b = a+1"
    for a in xrange(2,pmax/4):
        a2 = a*a
        c2 = 2*a2+2*a+1
        c = isqrt(c2)
        if (c*c == c2) and (2*a+c+1 < pmax):
            yield a,a+1,c
    return
            
def main(pmax=10**8):
    n = 0
    trips = pythag_neighbor_triples(pmax)
    for a,b,c in trips:
        p = a+b+c
        n += pmax/p
    print n

# Clearly, if a,b,c satisfy c % (b-a) == 0, then so do la,lb,lc.
# In searching through a,b,c in lowest terms, it seems b=a+1.

if __name__ == '__main__': main()
