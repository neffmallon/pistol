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
    increasing = True
    decreasing = True
    for i in range(1,ndig):
        if digits[i] < digits[i-1]:
            increasing = False
            break
    for i in range(1,ndig):
        if digits[i] > digits[i-1]:
            decreasing = False
            break
    return not (increasing or decreasing)

bouncy = []
for i in range(100,1590000):
    if isbouncy(i):
        bouncy.append(i)
    if i > 1580000 :
        frac = len(bouncy)/float(i)
        print i,frac

