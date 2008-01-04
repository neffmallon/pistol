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

from Utils import num_to_digits,ndigits

def increasing(n):
    d = num_to_digits(n)
    for i in range(len(d)-1):
        if d[i] > d[i+1]: return False
    return True

def decreasing(n):
    d = num_to_digits(n)
    for i in range(len(d)-1):
        if d[i] < d[i+1]: return False
    return True

def brute(dmax = 7):
    nnb = [0,9] # 1-9 are not bouncy
    for d in range(2,dmax):
        print "%d-digit numbers" % d
        nnb.append(0)
        for i in range(10**(d-1),10**d):
            if increasing(i) or decreasing(i): nnb[d] += 1
        print "    %d are not bouncy" % nnb[d]
    print "for the numbers below 10**%d, %d are not bouncy" % (dmax,sum(nnb))
    return

# (1-digit numbers
#     9 are not bouncy)
# 2-digit numbers
#     90 are not bouncy
# 3-digit numbers
#     375 are not bouncy
# 4-digit numbers
#     1200 are not bouncy
# 5-digit numbers
#     3279 are not bouncy
# 6-digit numbers
#     7998 are not bouncy
# for the numbers below 10000000, 12942 are not bouncy

