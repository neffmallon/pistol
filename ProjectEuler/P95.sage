#!/usr/bin/env sage

def sum_div(n):
    if n == 1: return 1
    return sum(n.divisors())-n
def is_perfect(n): return sum_div(n) == n

def gen_cycle(n,limit=1000000):
    cycle = []
    while 1:
        if n > limit: break
        if n in cycle: break
        cycle.append(n)
        n = sum_div(n)
    return cycle

