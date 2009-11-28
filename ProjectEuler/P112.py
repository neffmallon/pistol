"""
Working from left-to-right if no digit is exceeded by the digit to its
left it is called an increasing number; for example, 134468.

Similarly if no digit is exceeded by the digit to its right it is
called a decreasing number; for example, 66420.

We shall call a positive integer that is neither increasing nor
decreasing a 'bouncy' number; for example, 155349.

Clearly there cannot be any bouncy numbers below one-hundred, but just
over half of the numbers below one-thousand (525) are bouncy. In fact,
the least number for which the proportion of bouncy numbers first
exceeds 50% is 538.

Surprisingly bouncy number become more and more common and by the time
we reach 21780 the proportion of bouncy numbers is equal to 90%.

Find the least number for which the proportion of bouncy numbers is
exactly 99%.
"""

from Utils import num_to_digits

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

nbouncy = 0
for i in xrange(100,1590000):
    if isbouncy(i):
        nbouncy += 1

    frac = nbouncy*100/i
    if frac == 99:
        print i,nbouncy,frac
        break


