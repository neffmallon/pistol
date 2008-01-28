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
from Utils import issquare

one = Decimal(1)
two = Decimal(2)

def avg(a,b): return (a+b)/two

def sqrt(n,maxiter=100):
    f = one
    for i in range(maxiter):
        f = avg(f,n/f)
    return f

def sum100digits(a):
    s = str(a).replace(".","")[:100]
    return sum(map(int,s))

def main():
    import math
    getcontext().prec=110
    s = 0
    for i in range(2,100):
        if issquare(i): continue
        d = Decimal(i)
        sqrt_i = sqrt(d)
        s += sum100digits(sqrt_i)
    print s

if __name__ == '__main__': main()
