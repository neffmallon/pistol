#!/usr/bin/env python
"""
Problem 124
14 July 2006

The radical of n, rad(n), is the product of distinct prime factors of
n. For example, 504 = 23 * 32 * 7, so rad(504) = 2 * 3 * 7 = 42.

If we calculate rad(n) for 1 <= n <= 10, then sort them on rad(n), and
sorting on n if the radical values are equal, we get: Unsorted
	  	
(deleted table)

Let E(k) be the kth element in the sorted n column; for example, E(4)
= 8 and E(6) = 9.

If rad(n) is sorted for 1 <= n <= 100000, find E(10000).
"""

from sets import Set
from Utils import primes

nmax = 1001000
ps = primes(nmax)
pset = Set(ps)

def isprime(n): return n in pset

def getfactors(n):
   """Return list containing prime factors of a number."""
   if isprime(n) or n==1:
       return [n]
   for i in ps:
       if not n%i: # if goes evenly
           n = n/i
           return [i] + getfactors(n)
   return []

def prod(l): return reduce(lambda x,y: x*y,l)

def rad(n): return prod(Set(getfactors(n)))

def main(nmax=100000):
    results = []
    for i in range(1,nmax+1):
        #print i,rad(i)
        results.append((rad(i),i))
    results.sort()
    print results[3][1],results[5][1]
    print results[9999][1]
    return

if __name__ == '__main__': main()

