"""
Consider the fraction, n/d, where n and d are positive integers. If nd
and HCF(n,d)=1, it is called a reduced proper fraction.

If we list the set of reduced proper fractions for d<=8 in ascending
order of size, we get:

1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5, 5/8,
2/3, 5/7, 3/4, 4/5, 5/6, 6/7, 7/8

It can be seen that 2/5 is the fraction immediately to the left of 3/7.

By listing the set of reduced proper fractions for d <= 1,000,000 in
ascending order of size, find the numerator of the fraction
immediately to the left of 3/7.
"""
import psyco; psyco.full()

import math
from Utils import farey,gcd
# Doesn't work:
#print farey(2.999999999999999999999999999999999999999999999998/7,1000000)

results = []
dmax = 1000000
threesevenths = 3/7.
for d in range(999000,1000001):
    start = int(math.floor(0.4285*d))
    fd = float(d)
    for n in range(start,d):
        f = n/fd
        if f > threesevenths: break
        if gcd(n,d) == 1:
            results.append((f,n,d))
    if d % 100 == 0:
        results.sort()
        results = results[-20:]
        print "current results at %d" % d
        print results

    


            
            
