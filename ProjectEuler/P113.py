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
from Utils import num_to_digits,ndigits
from itertools import count, islice
    
def myrange(start,stop):
    return islice(count(start),0,stop-start)

def isbouncy(n):
    digits = num_to_digits(n)
    ndig = len(digits)
    increasing = False
    decreasing = False
    for i in range(1,ndig):
        if digits[i-1] < digits[i]:
            increasing = True
        elif digits[i-1] > digits[i]:
            decreasing = True
        if increasing and decreasing: return True
    return False

def report(i,bouncy): print "There are %d not bouncy below %d" % (i-bouncy,i)

def count_below(n=1000000):
    bouncy = 0
    for i in myrange(0,n):
        if isbouncy2(i):
            bouncy += 1
        if i % (n/10) == 0: report(i,bouncy)
    report(n,bouncy)

apat = re.compile('0[1-9]|1[2-9]|2[3-9]|3[4-9]|4[5-9]|5[6-9]|6[7-9]|7[89]|89')
dpat = re.compile('9[0-8]|8[0-7]|7[0-6]|6[0-5]|5[0-4]|4[0-3]|3[0-2]|2[01]|10')

def isbouncy2(n):
    # This is paradoxically much faster than isbouncy()
    sn = str(n)
    if apat.search(sn) and dpat.search(sn): return True
    return False

def count_inf():
    bouncy = 0
    for i in count(100):
        if isbouncy2(i):
            bouncy += 1
        if i % 1000000 == 0: report(i,bouncy)
    return

def notbouncylist(n):
    nbl = []
    for i in xrange(n):
        if not isbouncy2(i):
            nbl.append(i)
    return nbl

def append_ints(i,j): return int(str(i)+str(j))

def combine_nbls(alist,blist):
    nbl = []
    for i in alist:
        for j in blist:
            ij = append_ints(i,j)
            if not isbouncy2(ij):
                nbl.append(ij)
    return nbl

def breedlist():
    nbl_5 = notbouncylist(10**5)
    nbl_10 = combine_nbls(nbl_5,nbl_5)
    print len(nbl_10)

if __name__ == '__main__':
    breedlist()


    
