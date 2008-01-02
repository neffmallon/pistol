"""
Euler's Totient function, phi(n) [sometimes called the phi function], is
used to determine the number of numbers less than n which are
relatively prime to n. For example, as 1, 2, 4, 5, 7, and 8, are all
less than nine and relatively prime to nine, phi(9)=6.

Interestingly, phi(87109)=79180, and it can be seen that 87109 is a
permutation of 79180.

Find the value of n, below ten million, for which phi(n) is a
permutation of n and the ratio n/phi(n) produces a minimum.
"""

from Utils import gcd,primes,unique,num_to_digits,sortcopy
from sets import Set
from pprint import pprint

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

results = []
for i in range(1000000,nmax):
    phii = phi(i)
    if ispermutation(i,phii):
        results.append((i/float(phii),i,phii))
        if i/float(phii) > 4.5: print i/float(phii),i
results.sort()
pprint(results[:100])
