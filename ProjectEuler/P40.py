"""
An irrational decimal fraction is created by concatenating the
positive integers:

0.123456789101112131415161718192021...

It can be seen that the 12th digit of the fractional part is 1.

If dn represents the nth digit of the fractional part, find the value
of the following expression.

d1 * d10 * d100 * d1000 * d10000 * d100000 * d1000000
"""

def num_to_digits(n): return map(int,str(n))
def prod(l):
    p = 1
    for i in l:
        p *= i
    return p

digits = []
for i in range(1,200000):
    digits.extend(num_to_digits(i))
print len(digits)," total digits"
a = [digits[0],digits[9],digits[99],digits[999],
       digits[9999],digits[99999],digits[999999]]
print a,prod(a)

