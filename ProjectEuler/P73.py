"""
Consider the fraction, n/d, where n and d are positive integers. If nd
and HCF(n,d)=1, it is called a reduced proper fraction.

If we list the set of reduced proper fractions for d 8 in ascending
order of size, we get:

1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, ** 3/8, 2/5, 3/7, ** 1/2, 4/7, 3/5,
5/8, 2/3, 5/7, 3/4, 4/5, 5/6, 6/7, 7/8

It can be seen that there are 3 fractions between 1/3 and 1/2.

How many fractions lie between 1/3 and 1/2 in the sorted set of
reduced proper fractions for d <= 10,000?
"""

from Utils import gcd

dmax = 10000
third = 1/float(3)
half = 0.5
nvals = 0
for d in range(4,dmax+1):
    nmin = d/3
    nmax = d/2+1
    for n in range(nmin,nmax):
        v = n/float(d)
        if third < v < half and gcd(n,d) == 1:
            nvals += 1
print nvals
            
