"""
The first two consecutive numbers to have two distinct prime factors
are:

14 = 2 7
15 = 3 5

The first three consecutive numbers to have three distinct prime
factors are:

644 = 2^2 7 23
645 = 3 5 43
646 = 2 17 19.

Find the first four consecutive integers to have four distinct primes
factors. What is the first of these numbers?
"""
from Utils import primes,unique
from pprint import pprint
from sets import Set

nmax = 1000000
ps = primes(nmax)
pset = Set(ps)

def getfactors(n):
   """Return list containing prime factors of a number."""
   if isprime(n) or n==1:
       return [n]
   for i in ps:
       if not n%i: # if goes evenly
           n = n/i
           return [i] + getfactors(n)
   return None

def isprime(n): return n in pset

def nfactors(n,m=3): return len(unique(getfactors(n))) >= m

#three_factor_list = [i for i in range(1,nmax) if nfactors(i,3)]
#for i in range(len(three_factor_list)-3):
#    f1,f2,f3 = three_factor_list[i:i+3]
#    if f3-f1 == 2: print f1,f2,f3

four_factor_list = [i for i in range(1,nmax) if nfactors(i,4)]
for i in range(len(four_factor_list)-4):
    f1,f2,f3,f4 = four_factor_list[i:i+4]
    if f4-f1 == 3: print f1,f2,f3,f4

    


