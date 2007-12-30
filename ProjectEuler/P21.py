"""
Let d(n) be defined as the sum of proper divisors of n (numbers less
than n which divide evenly into n). If d(a) = b and d(b) = a, where a
b, then a and b are an amicable pair and each of a and b are called
amicable numbers.

For example, the proper divisors of 220 are 1, 2, 4, 5, 10, 11, 20,
22, 44, 55 and 110; therefore d(220) = 284. The proper divisors of 284
are 1, 2, 4, 71 and 142; so d(284) = 220.

Evaluate the sum of all the amicable numbers under 10000.
"""

def divisors(n):
    from math import sqrt
    lim = int(sqrt(n))+1
    divs = []
    for i in range(1,lim):
        if n % i == 0:
            if i > 1:
                divs.extend([i,n/i])
            else:
                divs.append(i)
    divs.sort()
    return divs

def d(n): return sum(divisors(n))

vals = []
for i in range(10000):
    if i == d(d(i)) and i != d(i):
        print i,d(i),d(d(i))
        vals.append(i)
print vals,sum(vals)
        
