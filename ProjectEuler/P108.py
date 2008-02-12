#!/usr/bin/env python
"""
In the following equation x, y, and n are positive integers.
1/x + 1/y = 1/n

For n = 4 there are exactly three distinct solutions:
1/5 + 1/20 = 1/4
1/6 + 1/12 = 1/4
1/8+1/8 = 1/4

What is the least value of n for which the number of distinct
solutions exceeds one-thousand?
"""

from time import time
from pprint import pprint
from math import sqrt
from Utils import Rational,divisors

def brute(nmax = 50000):
    # 10,000 only lead to items that had 58 solutions (1/840),
    #  so I have to find a smarter method
    results = {}
    for i in range(1,nmax+1):
        ri = Rational(1,i)
        for j in range(1,i+1):
            rj = Rational(1,j)
            rs = ri.add(rj).inverse()
            if rs.isint():
                n = rs.int()
                if n in results:
                    results[n].append((i,j))
                else:
                    results[n] = [(i,j)]
    return results

def brute2(nmax=500):
    results = {}
    for n in range(1,nmax+1):
        for x in range(n+1,2*n+1):
            y = x*n/(x-n)
            if n*(x+y) == x*y:
                v = results.setdefault(n,[])
                v.append((x,y))
    return results

def clever(nmax):
    results = {}
    for a in xrange(2,nmax):
        for b in xrange(1,nmax):
            x = a*b
            y = a*(a-1)*b
            n = b*(a-1)
            r = results.setdefault(n,[])
            r.append((x,y))
    return results

def brian_forum_nsols(n):
    return sum(1 for x in range(n+1, n*2+1) if ((n*x) % (x-n)==0))
 
def brian_forum_solution():
    f = 2*3*5*7*11*13
    for i in xrange(f,f*17,f):
        if brian_forum_nsols(i)>=1000:
            print i
            break

def main(nmax=10000):
    for i in range(1,20):
        print i,brian_forum_nsols(i),len(divisors(i))
    return

# The correct answer is 180180. Don't know how I got that one, but evidently
# I solved it. One of the postings in the forum cited the Sloane page:
# http://www.research.att.com/~njas/sequences/A018892

if __name__ == '__main__': main()
