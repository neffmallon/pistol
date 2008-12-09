"""
For a positive integer n, let sigma2(n) be the sum of the squares of
its divisors. For example,

sigma2(10) = 1 + 4 + 25 + 100 = 130.

Find the sum of all n, 0 < n < 64,000,000 such that sigma2(n) is a
perfect square.

"""

from math import sqrt
from Utils import issquare

def ndivisors(n,VERBOSE=False):
    "just count the divisors of n"
    s = 0
    lim = int(sqrt(n)+1)
    for i in xrange(1,lim):
        if n%i == 0:
            if i == n/i:
                s += 1
            else:
                s+=2
    return s

def divisors(n):
    lim = int(sqrt(n)+1)
    for i in xrange(1,lim):
        if n%i == 0:
            if i == n/i:
                yield i
            else:
                yield i
                yield n/i
    return

def sqsum(iterable): return sum(i*i for i in iterable)

sumn = 0
for i in xrange(1,64*10**6):
    if issquare(sqsum(divisors(i))):
        print i,sqsum(divisors(i))
        sumn += i
print "Sum = ",sumn

