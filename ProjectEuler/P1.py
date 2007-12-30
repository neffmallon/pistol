#!/usr/local/bin/python
"""
Problem 1:

If we list all the natural numbers below 10 that are multiples of 3 or 5, we get 3, 5, 6 and 9. The sum of these multiples is 23.

Find the sum of all the multiples of 3 or 5 below 1000.
"""

from sets import Set

maxn = 1000

# All natural numbers below 1000 div 3
n = Set(range(3,maxn,3))

# All natural numbers below 1000 div 5
m = Set(range(5,maxn,5))

u = n | m

print u,sum(u)



