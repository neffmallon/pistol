#!/usr/bin/env python
"""
The prime factors of 13195 are 5, 7, 13 and 29.

What is the largest prime factor of the number 317584931803?
"""

from math import sqrt
from itertools import takewhile

def primes(n):
    # From python cookbook
    if n==2: return [2]
    elif n<2: return []
    s=range(3,n+1,2)
    mroot = n ** 0.5
    half=(n+1)/2-1
    i=0
    m=3
    while m <= mroot:
        if s[i]:
            j=(m*m-3)/2
            s[j]=0
            while j<half:
                s[j]=0
                j+=m
        i=i+1
        m=2*i+3
    return [2]+[x for x in s if x]

if __name__ == '__main__': 
    n = 317584931803
    imax = int(sqrt(n))

    for i in primes(imax):
        if n % i == 0: print i
