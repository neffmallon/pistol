"""
A number chain is created by continuously adding the square of the digits in a number to form a new number until it has been seen before.

For example,

44 32 13 10 1 1
85 89 145 42 20 4 16 37 58 89

Therefore any chain that arrives at 1 or 89 will become stuck in an endless loop. What is most amazing is that EVERY starting number will eventually arrive at 1 or 89.

How many starting numbers below ten million will arrive at 89?
"""

import psyco; psyco.full()

def num_to_digits(n): return map(int,str(n))
def square(n): return n*n

def num_chain_result(n,max_iter=100000):
    for i in range(max_iter):
        n = sum([square(i) for i in num_to_digits(n)])
        if n == 1: return 1
        elif n == 89: return 89
    raise "Too many iters"


n89 = 0
for i in range(1,10000000):
    result = num_chain_result(i)
    if i%1000 == 0: print i," terminates in ",result
    if result == 89:
        n89 += 1
print n89

    
