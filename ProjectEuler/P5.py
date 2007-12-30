"""
2520 is the smallest number that can be divided by each of the numbers
from 1 to 10 without any remainder.

What is the smallest number that is evenly divisible by all of the
numbers from 1 to 20?
"""

def gcd(a,b):
    if b==0: return a
    return gcd(b, a%b)

def lcm(a,b):
    return a*b/gcd(a,b)

sm = 1
for i in range(2,21):
    sm = lcm(i,sm)
    print i,sm
