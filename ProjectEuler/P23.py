"""
A perfect number is a number for which the sum of its proper divisors
is exactly equal to the number. For example, the sum of the proper
divisors of 28 would be 1 + 2 + 4 + 7 + 14 = 28, which means that 28
is a perfect number.

A number whose proper divisors are less than the number is called
deficient and a number whose proper divisors exceed the number is
called abundant.

As 12 is the smallest abundant number, 1 + 2 + 3 + 4 + 6 = 16, the
smallest number that can be written as the sum of two abundant numbers
is 24. By mathematical analysis, it can be shown that all integers
greater than 28123 can be written as the sum of two abundant numbers.
However, this upper limit cannot be reduced any further by analysis
even though it is known that the greatest number that cannot be
expressed as the sum of two abundant numbers is less than this limit.

Find the sum of all the positive integers which cannot be written as
the sum of two abundant numbers.
"""

def divisors(n):
    from math import sqrt
    lim = int(sqrt(n))+1
    divs = []
    for i in range(1,lim):
        if n % i == 0:
            if i == 1 or i == n/i:
                divs.append(i)
            else:
                divs.extend([i,n/i])
    divs.sort()
    return divs

def is_abundant(n): return sum(divisors(n)) > n

def get_abundants(nmax=1000):
    abundants = []
    for i in range(nmax):
        if is_abundant(i):
            abundants.append(i)
    return abundants

nmax=30000
from sets import Set
abundants = get_abundants(nmax)
abundant_sum = Set()
for i in abundants:
    for j in abundants:
        abundant_sum.add(i+j)

no_abundant_sum = []
for i in range(1,nmax):
    if i not in abundant_sum:
        no_abundant_sum.append(i)

print no_abundant_sum
print sum(no_abundant_sum)






