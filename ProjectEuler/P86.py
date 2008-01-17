#!/usr/bin/env python
'''
A spider, S, sits in one corner of a cuboid room, measuring 6 by 5 by
3, and a fly, F, sits in the opposite corner. By travelling on the
surfaces of the room the shortest "straight line" distance from S to F
is 10 and the path is shown on the diagram.

However, there are up to three "shortest" path candidates for any
given cuboid and the shortest route is not always integer.

By considering all cuboid rooms up to a maximum size of M by M by M,
there are exactly 2060 cuboids for which the shortest distance is
integer when M=100, and this is the least value of M for which the
number of solutions first exceeds two thousand; the number of
solutions is 1975 when M=99.

Find the least value of M such that the number of solutions first
exceeds one million.
'''

from Utils import isint
from math import sqrt

def shortest(A,B,C):
    '''
    Six differences, of which I believe only three are unique
    xy = D(000,Ay0)+D(Ay0,ABC) = min(Am0)
    yx = D(000,xB0)+D(xB0,ABC) = min(mB0)
    xz = D(000,A0z)+D(A0z,ABC) = min(A0m)
    zx = D(000,x0C)+D(x0C,ABC) = min(m0C)
    yz = D(000,0Bz)+D(0Bz,ABC) = min(0Bm)
    zy = D(000,0yC)+D(0yC,ABC) = min(0yC)
    '''
    #return min(sqrt((A+C)**2 + B**2),
    #           sqrt((A+B)**2 + C**2),
    #           sqrt((B+C)**2 + A**2))
    # Assuming A>B>C:
    return sqrt((B+C)**2+A**2)

def test1():
    print shortest(6,5,3) # Should be 10
    return

def calc_nint(M=100):
    nint = 0
    for A in range(1,M+1):
        for B in range(1,A+1):
            for C in range(1,B+1):
                d = shortest(A,B,C)
                if isint(d): nint+=1
    print "For M=%d, # integral solutions = %d" % (M,nint)
    return nint

def test2():
    calc_nint(99)
    calc_nint(100)
    return

if __name__ == '__main__':
    #test2()
    calc_nint(2000)
# For M=99, # integral solutions = 1975
# For M=100, # integral solutions = 2060
# For M=200, # integral solutions = 9???
# For M=1000, # integral solutions = 281334

