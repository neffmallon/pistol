"""
145 is a curious number, as 1! + 4! + 5! = 1 + 24 + 120 = 145.

Find the sum of all numbers which are equal to the sum of the
factorial of their digits.
"""

def factorial(n):
    if n == 0:
        return 1
    return n*factorial(n-1)

def num_to_digits(n): return map(int,str(n))
def fact_sum(n): return sum([factorial(i) for i in num_to_digits(n)])

nmax = 1000000
for i in range(3,nmax):
    if fact_sum(i) == i: print i

    

