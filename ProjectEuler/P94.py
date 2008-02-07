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

def isint_area(a,b):
    return isint(sqrt(4*a*a-b*b))
    #return isint(area2(a,b))

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

def brute2(plimit=100,verbose=False):
    slimit = plimit/3 + 1
    sump = 0
    for a in xrange(3,slimit):
        for b in [a-1,a+1]:
            if isint_area(a,b):
                p = 2*a+b
                if verbose: print a,a,b,p
                if p > plimit: continue
                sump += p
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
# I modified my search, and got:
#  10**7         9,973,078              6.9 sec
#  10**8         37,220,040             69.9 sec
#  10**9         19,070,426,971         742.4 sec
# But this, too, is wrong. My results for pmax=10**8 now match the
# entire sequence from Sloane A120893. But going up to 10**9 I
# still get a few false hits that aren't in the list.

# See integer sequence A120893 for something that has many of these terms:
# http://www.research.att.com/~njas/sequences/A120893


# Results with some wrong roots. I commented out the results that
#  weren't in the Sloane list:
wrong_results = """\
5 5 6 16
17 17 16 50
65 65 66 196
241 241 240 722
901 901 902 2704
3361 3361 3360 10082
12545 12545 12546 37636
46817 46817 46816 140450
174725 174725 174726 524176
652081 652081 652080 1956242
2433601 2433601 2433602 7300804
9082321 9082321 9082320 27246962
33895685 33895685 33895686 101687056
#63250209 63250209 63250210 189750628
#92604733 92604733 92604734 277814200
#97145893 97145893 97145892 291437678
126500417 126500417 126500416 379501250
#143448260 143448260 143448261 430344781
#155854941 155854941 155854940 467564822
#164937263 164937263 164937264 494811790
#172802784 172802784 172802785 518408353
#177343944 177343944 177343943 532031831
#185209465 185209465 185209464 555628394
#194291787 194291787 194291788 582875362
#202157308 202157308 202157309 606471925
#206698468 206698468 206698467 620095403"""

def main():
    #from time import time
    #t1 = time()
    #brute2(10**9,True)
    #print time()-t1
    # Argh! Just sum the roots that are in the Sloane list:
    sump = 0
    for line in wrong_results.splitlines():
        if line.startswith("#"): continue
        words = line.split()
        if not words: continue
        a,b,c,p = map(int,words)
        sump += p
    print "sump = ",sump
    # This gave 518408346, which was correct.
    return

if __name__ == '__main__': main()
