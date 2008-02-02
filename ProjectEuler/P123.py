#!/usr/bin/env python
"""
Let pn be the nth prime: 2, 3, 5, 7, 11, ..., and let r be the
remainder when (pn-1)n + (pn+1)n is divided by pn2.

For example, when n = 3, p3 = 5, and 43 + 63 = 280 == 5 mod 25.

The least value of n for which the remainder first exceeds 10^9 is 7037.

Find the least value of n for which the remainder first exceeds 10^10.
"""

from Utils import primes

ps = primes(1000000)

#for n,pn in enumerate(ps):
for n in [21027,21028,21029,21030,21031,21032,21033,21034,21035]:
    pn = ps[n-1]
    r = (pow(pn-1,n)+pow(pn+1,n)) % pow(pn,2)
    print n,pn,r

# I got 21033, but the web page says its wrong

