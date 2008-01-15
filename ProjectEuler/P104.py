"""
The Fibonacci sequence is defined by the recurrence relation:

    Fn = Fn1 + Fn2, where F1 = 1 and F2 = 1.

It turns out that F541, which contains 113 digits, is the first
Fibonacci number for which the last nine digits are 1-9 pandigital
(contain all the digits 1 to 9, but not necessarily in order). And
F2749, which contains 575 digits, is the first Fibonacci number for
which the first nine digits are 1-9 pandigital.

Given that Fk is the first Fibonacci number for which the first nine
digits AND the last nine digits are 1-9 pandigital, find k.
"""

import psyco; psyco.full()

from Utils import fibonacci
from sets import Set
from time import time

# Remove checking for length to save time
digits = Set('123456789')
strdigs = ['1','2','3','4','5','6','7','8','9']
def ispandigital4(nstr):
    sstr = Set(nstr)
    return (len(sstr) == 9) and ("0" not in sstr)
def ispandigital3(nstr):
    return len(nstr) == 9 and Set(nstr) == digits
def ispandigital2(nstr):
    return Set(nstr) == digits
def ispandigital(nstr):
    l = list(nstr)
    l.sort()
    return l == strdigs

# Search got up to i=494672 without finding a solution
f = fibonacci()
t0 = time()
nmax = 10000
for i in xrange(nmax):
    fi = f.next()
    fstr = str(fi).replace("L","")
    if not ispandigital4(fstr[-9:]): continue
    print "LAST ",i,fstr[-9:]
    if ispandigital(fstr[9:]):
        print "BOTH: ",i,fstr[:9],fstr[-9:]
        break
t1 = time()
print t1-t0
# Time to search through 10,000 fibs:
#ispandigital   7.8 sec, 7.8 with psyco
#ispandigital2  7.9 sec, 7.8 with psyco
#ispandigital3  7.9 sec, 7.9 with psyco
#ispandigital4  7.8 sec, 7.8 with psyco
