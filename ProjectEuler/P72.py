"""
Consider the fraction, n/d, where n and d are positive integers. If nd
and HCF(n,d)=1, it is called a reduced proper fraction.

If we list the set of reduced proper fractions for d 8 in ascending
order of size, we get:

1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5, 5/8,
2/3, 5/7, 3/4, 4/5, 5/6, 6/7, 7/8

It can be seen that there are 21 elements in this set.

How many elements would be contained in the set of reduced proper
fractions for d 1,000,000?
"""

from Utils import gcd

# this is the naive way
#nmax = 1000000
#nfrac = 0
#for d in range(1,nmax+1):
#    for n in range(1,d):
#        if gcd(n,d) == 1: nfrac += 1

from Utils import primes,unique
from sets import Set

nmax = 10000000
ps = primes(nmax)
pset = Set(ps)

def ispermutation(a,b):
    return sortcopy(num_to_digits(a)) == sortcopy(num_to_digits(b))

def isprime(n): return n in pset

def getfactors(n):
   """Return list containing prime factors of a number."""
   if isprime(n) or n==1:
       return [n]
   for i in ps:
       if not n%i: # if goes evenly
           n = n/i
           return [i] + getfactors(n)
   return None

def phi(n):
    "Euler's Totient Function"
    product=n
    for i in unique(getfactors(n)):
        product *= (1-1.0/i)
    return int(product)

nmax = 1000000
nfrac = 0
for d in range(1,nmax+1):
    nfrac += phi(d)
print nfrac

        
