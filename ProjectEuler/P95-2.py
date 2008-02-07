#!/usr/bin/env python

from Utils import divisors

def sum_div(n): return sum(divisors(n))

def gen_cycle(n,limit=1000000):
    cycle = []
    while True:
        if n > limit: return []
        if n in cycle: break
        cycle.append(n)
        n = sum_div(n)
    return cycle

def cycle_list(nmax,verbose=False):
    longest = []
    for i in range(2,nmax):
        cycle = gen_cycle(i)
        if not cycle: continue
        if cycle[-1] == 1: continue
        if len(cycle) > len(longest): longest = cycle
        if verbose: print i,cycle
    return longest

#cycle = cycle_list(15000)
#cycle = gen_cycle(14316) # This is the correct answer...
print divisors(1980),sum(divisors(1980))
cycle = gen_cycle(1980)
print cycle
print len(cycle),max(cycle),min(cycle)
