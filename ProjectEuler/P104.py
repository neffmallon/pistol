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

from Utils import fibonacci
from sets import Set

digits = Set('123456789')
# Remove checking for length to save time
#def ispandigital(nstr): return len(nstr) == 9 and Set(nstr) == digits
#def ispandigital(nstr): return Set(nstr) == digits
strdigs = ['1','2','3','4','5','6','7','8','9']
def ispandigital(nstr):
    l = list(nstr)
    l.sort()
    return l == strdigs

# Search got up to i=216812 without finding a solution

f = fibonacci()
nmax = 1000000
for i in xrange(nmax):
    fi = f.next()
    if i < 216811: continue
    fstr = str(fi).replace("L","")
    if not ispandigital(fstr[-9:]): continue
    print "LAST ",i,fstr[-9:]
    if ispandigital(fstr[9:]):
        print "BOTH: ",i,fstr[:9],fstr[-9:]
        break


