"""
n! means n  (n  1)  ...  3  2  1

Find the sum of the digits in the number 100!
"""

def factorial(n):
    if n < 0: raise ValueError
    if n ==0: return 1
    if n == 1: return 1
    if n == 2: return 2
    p = 1
    for i in range(2,n+1):
        p *= i
    return p

def int_to_intlist(i):
    s = str(i)
    stringlist = list(s)
    return map(int,stringlist)

if __name__ == '__main__':
    n = 100
    f = factorial(n)
    print f
    
    print sum(int_to_intlist(f))

