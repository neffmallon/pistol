#!/usr/bin/env python
"""
The binomial coefficients nCk can be arranged in triangular form,
	Pascal's triangle, like this: 1 1 1 1 2 1 1 3 3 1 1 4 6 4 1 1
	5 10 10 5 1 1 6 15 20 15 6 1 1 7 21 35 35 21 7 1 .........

It can be seen that the first eight rows of Pascal's triangle contain
twelve distinct numbers: 1, 2, 3, 4, 5, 6, 7, 10, 15, 20, 21 and 35.

A positive integer n is called squarefree if no square of a prime
divides n. Of the twelve distinct numbers in the first eight rows of
Pascal's triangle, all except 4 and 20 are squarefree. The sum of the
distinct squarefree numbers in the first eight rows is 105.

Find the sum of the distinct squarefree numbers in the first 51 rows
of Pascal's triangle.
"""

from math import sqrt

def gen_pascal_row_fast(n):
    el = 1
    yield el
    for m in range(1,n+1):
        el = (el*(n-m+1))/m
        yield el
    return

def unique_pascal_numbers(nrows=8):
    from sets import Set
    unique = Set()
    for i in xrange(nrows):
        for j in gen_pascal_row_fast(i):
            unique.add(j)
    return unique

def squarefree(i):
    imax = int(sqrt(i))+1
    for j in range(2,imax):
        if i%(j*j) == 0: return False
    return True

def main(nrows = 51):
    print sum(i for i in unique_pascal_numbers(nrows) if squarefree(i))
    return

if __name__ == '__main__': main()

    
