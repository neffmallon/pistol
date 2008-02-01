#!/usr/bin/env python

from pylab import *

def guess_rem(a):
    a2 = a*a
    if a%2 == 0:
        return a2-2*a
    return a2-a

def trial(amax=40):
    rmaxsum = 0
    for a in range(3,amax+1):
        a2 = a*a
        rmax = 0
        nmax = 0
        for n in range(a2):
            r = (pow(a-1,n)+pow(a+1,n))% a2
            if r > rmax:
                rmax = r
                nmax = n
        if guess_rem(a) != rmax:
            print a,nmax,guess_rem(a),rmax,a2
        rmaxsum += rmax
    return rmaxsum

def clever(amax=1000):
    return sum([guess_rem(a) for a in range(3,amax)])

def main():
    print clever()
    return

if __name__ == '__main__': main()

