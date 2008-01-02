"""
The prime 41, can be written as the sum of six consecutive primes:
41 = 2 + 3 + 5 + 7 + 11 + 13

This is the longest sum of consecutive primes that adds to a prime
below one-hundred.

The longest sum of consecutive primes below one-thousand that adds to
a prime, contains 21 terms, and is equal to 953.

Which prime, below one-million, can be written as the sum of the most
consecutive primes?
"""

from Utils import primes
from sets import Set

ps = primes(1000000)
pset = Set(ps)

for n in range(531,551,2):
    for istart in range(len(ps)-n):
        c = sum(ps[istart:istart+n])
        if c in pset:
            print n,c



