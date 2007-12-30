"""
The Fibonacci sequence is defined by the recurrence relation:

    Fn = Fn1 + Fn2, where F1 = 1 and F2 = 1.

Hence the first 12 terms will be:

    F1 = 1
    F2 = 1
    F3 = 2
    F4 = 3
    F5 = 5
    F6 = 8
    F7 = 13
    F8 = 21
    F9 = 34
    F10 = 55
    F11 = 89
    F12 = 144

The 12th term, F12, is the first term to contain three digits.

What is the first term in the Fibonacci sequence to contain 1000 digits?
"""

from itertools import takewhile

def fib_gen():
    yield 0
    yield 1
    n1,n2 = 0,1
    while 1:
        n1,n2 = n2,n1+n2
        yield n2
    return

    
def ndigits(n): return len(str(n))

f = fib_gen()
for i in range(10000):
    val = f.next()
    print i,ndigits(val)
    if ndigits(val) == 1000: break


