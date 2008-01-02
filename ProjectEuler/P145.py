"""
Some positive integers n have the property that the sum [ n +
reverse(n) ] consists entirely of odd (decimal) digits. For instance,
36 + 63 = 99 and 409 + 904 = 1313. We will call such numbers
reversible; so 36, 63, 409, and 904 are reversible. Leading zeroes are
not allowed in either n or reverse(n).

There are 120 reversible numbers below one-thousand.

How many reversible numbers are there below one-billion (10^9)?
"""

from Utils import num_to_digits,digits_to_num
from sets import Set

nmax = 1000000000

oddset = Set([1,3,5,7,9])

def odd_revsum(n):
    d = num_to_digits(n)
    d.reverse()
    if d[0] == 0: return False
    m = digits_to_num(d)
    mn = m+n
    val = True
    for d in num_to_digits(mn):
        if d not in oddset: return False
    return True

nrev = 0
for i in xrange(nmax):
    if odd_revsum(i):
        nrev += 1
    if i%1000000 == 0:
        print i,nrev
print nrev

