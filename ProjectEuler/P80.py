"""
It is well known that if the square root of a natural number is not an
integer, then it is irrational. The decimal expansion of such square
roots is infinite without any repeating pattern at all.

The square root of two is 1.41421356237309504880..., and the digital
sum of the first one hundred decimal digits is 475.

For the first one hundred natural numbers, find the total of the
digital sums of the first one hundred decimal digits for all the
irrational square roots.
"""

from decimal import Decimal,getcontext
from math import sqrt

def avg(a,b): return (a+b)/Decimal(2)

def sqrt(n,maxiter=100):
    f = 1
    for i in range(maxiter):
        f = avg(f,n/f)
    return f

def sum100digits(a):
    div,mod = divmod(a,1)
    smod = str(mod)
    smod = smod.replace("0.","")
    l = map(int,smod)
    return sum(l[:100])
    
d2 = Decimal(2)
getcontext().prec=110
rt2 = sqrt(d2,1000)
print sum100digits(rt2)




