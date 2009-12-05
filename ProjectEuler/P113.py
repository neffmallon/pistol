"""
Working from left-to-right if no digit is exceeded by the digit to its
left it is called an increasing number; for example, 134468.

Similarly if no digit is exceeded by the digit to its right it is
called a decreasing number; for example, 66420.

We shall call a positive integer that is neither increasing nor
decreasing a 'bouncy' number; for example, 155349.

As n increases, the proportion of bouncy numbers below n increases
such that there are only 12951 numbers below one-million that are not
bouncy and only 277032 non-bouncy numbers below 10**10.

How many numbers below a googol (10**100) are not bouncy?
"""

import re
from itertools import *
from Utils import prod
    
apat = re.compile('9[0-8]|8[0-7]|7[0-6]|6[0-5]|5[0-4]|4[0-3]|3[0-2]|2[01]|10')
dpat = re.compile('0[1-9]|1[2-9]|2[3-9]|3[4-9]|4[5-9]|5[6-9]|6[7-9]|7[89]|89')
def isasc(n): return not bool(dpat.search(str(n)))
def isdes(n): return not bool(apat.search(str(n)))
def isbouncy(n):
    sn = str(n)
    if apat.search(sn) and dpat.search(sn): return True
    return False
def isnbouncy(i): return not isbouncy(i)

def count_below(n=1000000):
    bouncy = 0
    for i in xrange(1,n):
        if isbouncy(i):
            bouncy += 1
        if i % (n/10) == 0: print i,i-bouncy-1
    print n,n-bouncy

def count_inf():
    bouncy = 0
    for i in count(100):
        if isbouncy(i):
            bouncy += 1
        if i % 1000000 == 0: print i,i-bouncy-1
    return

def notbouncylist(n):
    nbl = []
    for i in xrange(1,n):
        if not isbouncy(i):
            nbl.append(i)
    return nbl

def count_by10s():
    nbt = 0
    for n in xrange(1,10):
        nb = 0
        for i in ifilter(isdes,xrange(10**(n-1),10**n)):
            nb += 1
        nbt += nb
        print "There are %d descend numbers between 10^%d and 10^%d, total %d" % (nb,n-1,n,nbt)
    return

def nasc(d): return prod(xrange(10,10+d))/prod(xrange(1,d+1))-1
def ndes(d): return prod(xrange(9,9+d))/prod(xrange(1,d+1))
def nnb(d): return nasc(d)+ndes(d)-9
def nnbt(d): return sum(nnb(i) for i in xrange(1,d))

if __name__ == '__main__':
    print map(nnbt,xrange(1,20))
    print nnbt(11)
    print nnbt(101)

# ---Range---  Ascend  Descend   Nonbouncy
# 10^0 - 10^1  9       9         9
# 10^1 - 10^2  54      45        90
# 10^2 - 10^3  219     165       375
# 10^3 - 10^4  714     495       1200
# 10^4 - 10^5  2001    1287      3279
# 10^5 - 10^6  5004    3003      7998
# 10^6 - 10^7  11439   6435      17865
