"""
A Pythagorean triplet is a set of three natural numbers, abc, for which,
a**2 + b**2 = c**2

For example, 3**2 + 4**2 = 9 + 16 = 25 = 5**2.

There exists exactly one Pythagorean triplet for which a + b + c = 1000.
Find the product abc.
"""
from math import sqrt
from pprint import pprint

def make_triplets(n):
    trips = []
    for b in range(1,n):
        b2 = b*b
        for a in range(1,b):
            c2 = a*a+b2
            c,rem = divmod(sqrt(c2),1)
            if rem == 0: trips.append((a,b,int(c)))
    return trips

trips = make_triplets(500)

for abc in trips:
    if sum(abc) == 1000:
        a,b,c = abc
        print a,b,c,a*b*c
