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
    for i in xrange(100,n):
        if isbouncy(i):
            bouncy += 1
        if i % (n/10) == 0: report(i,bouncy)
    report(n,bouncy)

if __name__ == '__main__':
    count_below(10**10)

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

