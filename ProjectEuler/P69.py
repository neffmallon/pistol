"""
Euler's Totient function, phi(n) [sometimes called the phi function],
is used to determine the number of numbers less than n which are
relatively prime to n. For example, as 1, 2, 4, 5, 7, and 8, are all
less than nine and relatively prime to nine, phi(9)=6.

n 	Relatively Prime 	phi(n) 	n/phi(n)
2 	1 	        1 	2
3 	1,2 	        2 	1.5
4 	1,3 	        2 	2
5 	1,2,3,4 	4 	1.25
6 	1,5 	        2 	3
7 	1,2,3,4,5,6 	6 	1.1666...
8 	1,3,5,7 	4 	2
9 	1,2,4,5,7,8 	6 	1.5
10 	1,3,7,9 	4 	2.5

It can be seen that n=6 produces a maximum n/phi(n) for n 10.

Find the value of n 1,000,000 for which n/phi(n) is a maximum.
"""

from time import time
from pprint import pprint
from Utils import gcd,primes,unique
from sets import Set

nmax = 1000000
ps = primes(nmax)
pset = Set(ps)

def isprime(n): return n in pset

#def isrelprime(a,b):
#    return len(Set(getfactors(a)) ^ Set(getfactors(b))) > 0
# This is slightly faster:
def isrelprime(a,b):
    return gcd(a,b) > 1

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

def main():
    results = []
    for n in range(2,nmax+1):
        #relprimes = []
        #for m in range(1,n):
        #    if gcd(n,m) == 1:
        #        relprimes.append(m)
        val = n/float(phi(n))
        if val > 4:
            results.append((val,n))
        if val > 5:
            print val,n
    results.sort()
    pprint(results[-20:])
    return

if __name__ == '__main__':
    main()
