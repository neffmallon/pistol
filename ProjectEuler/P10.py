"""
The sum of the primes below 10 is 2 + 3 + 5 + 7 = 17.

Find the sum of all the primes below one million.
"""

from P3 import primes

#n = 1000000
n = 1000000
p = primes(n)
print sum(p)

