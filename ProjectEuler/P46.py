"""
It was proposed by Christian Goldbach that every odd composite number can be written as the sum of a prime and twice a square.

It turns out that the conjecture was false.

What is the smallest odd composite that cannot be written as the sum
of a prime and twice a square?
"""

from Utils import primes
from pprint import pprint

nmax = 100000
ps = primes(nmax)
sqs = [i*i for i in range(1,nmax)]

results = {}
for p in ps:
    for sq in sqs:
        results[p+2*sq] = 1

for i in range(3,nmax,2):
    if i not in results:
        print i,i in ps

