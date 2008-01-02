"""
Euler published the remarkable quadratic formula:

n^2 + n + 41

It turns out that the formula will produce 40 primes for the
consecutive values n = 0 to 39. However, when n = 40, 402 + 40 + 41 =
40(40 + 1) + 41 is divisible by 41, and certainly when n = 41, 41^2 +
41 + 41 is clearly divisible by 41.

Using computers, the incredible formula n^2 - 79n + 1601 was
discovered, which produces 80 primes for the consecutive values n = 0
to 79. The product of the coefficients, 79 and 1601, is 126479.

Considering quadratics of the form:

    n^2 + an + b, where |a| < 1000 and |b| < 1000

    where |n| is the modulus/absolute value of n
    e.g. |11| = 11 and |4| = 4

Find the product of the coefficients, a and b, for the quadratic
expression that produces the maximum number of primes for consecutive
values of n, starting with n = 0.
"""

from Utils import primes
from sets import Set
from pprint import pprint

ps = primes(1000)
bpset = Set(primes(1000000))

def plist(a,b):
    def f(n): return n*n+a*n+b
    for i in range(100):
        if abs(f(i)) not in bpset: return i-1
    raise "too many iters in plist"

tuplist = []
for b in ps:
    for a in range(-999,1000):
        if (a+b+1 in bpset) and (4+2*a+b in bpset) and (9+3*a+b in bpset):
        #if (a+b+1 in bpset) and (4+2*a+b in bpset) :
        #if (a+b+1 in bpset):
            tuplist.append((a,b))

print len(tuplist)

lenlist = []
for a,b in tuplist:
    n = plist(a,b)
    lenlist.append((n,a,b))
lenlist.sort()
pprint(lenlist)




