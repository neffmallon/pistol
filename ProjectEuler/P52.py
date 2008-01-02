"""
It can be seen that the number, 125874, and its double, 251748,
contain exactly the same digits, but in a different order.

Find the smallest positive integer, x, such that 2x, 3x, 4x, 5x, and
6x, contain the same digits.
"""

def num_to_digits(n): return map(int,str(n))

nmax = 1000000
for x in range(1,nmax):
    digits = num_to_digits(2*x)
    digits.sort()
    result = True
    for i in range(3,7):
        newdigits = num_to_digits(i*x)
        newdigits.sort()
        if newdigits != digits:
            result = False
            break
    if result: print x

        


