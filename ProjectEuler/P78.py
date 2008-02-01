"""
Problem 78

Let p(n) represent the number of different ways in which n coins can
be separated into piles. For example, five coins can separated into
piles in exactly seven different ways, so p(5)=7.

Find the least value of n for which p(n) is divisible by one million. 

OOOOO 
OOOO   O 
OOO   OO 
OOO   O   O 
OO   OO   O 
OO   O   O   O 
O   O   O   O   O 
"""

import psyco; psyco.full()
from pprint import pprint
from Utils import partition_upper_bound,count_partitions
from itertools import count,islice,izip

def get_rama_ests(nmax=10000):
    results = []
    for j in range(50,nmax):
        e = partition_upper_bound(j)
        r,rem = divmod(e,1000000)
        if rem < 100: results.append((rem,j,e))
    results.sort()
    return results

def get_rama_ests_mod5(nmax=10000):
    for j in range(4,nmax,5):
        e = partition_upper_bound(j)
        if e % 10000 == 0:
            print j,e
    return

def incr_partitions(p1s):
    """Given the partitions of p(n-1), generate the partitions of p(n).
    This generates the partitions in the reverse of the order I like,
    but it isn't that big of a deal.
    """
    ps = []
    for p in p1s:
        ps.append([1]+p)
        if p and (len(p) == 1 or p[1] > p[0]):
            ps.append([p[0]+1]+p[1:])
    return ps

def brute():
    # Got up to i=125 without a solution
    for i in range(69,200):
        np = count_partitions(i)
        print i,np
        if np % 1000000 == 0: break

# Hint:
# The function [14974+i*15625] yields numbers whose partions
# p(n) = 0 (mod 5**6), which is a prerequisite for being divisible
# by (10**6).

def pent_indices(n=0):
    for i in count(n):
        yield i
        if i > 0: yield -i
    return

def pentagonal():
    indices = pent_indices(1) # Skip the 0 term
    for i in indices:
        yield i*(3*i-1)/2
    return

def part_signs():
    for i in count():
        sign = pow(-1,i)
        yield sign
        yield sign
    return

partitionsp = [1, 1, 2, 3, 5, 7, 11, 15, 22, 30, 42, 56, 77,
               101, 135, 176, 231, 297, 385, 490, 627, 792, 1002,
               1255, 1575, 1958, 2436, 3010, 3718, 4565, 5604, 6842,
               8349, 10143, 12310, 14883, 17977, 21637, 26015, 31185,
               37338, 44583, 53174, 63261, 75175, 89134]

def npart(n):
    """\
    MacMahon's recurrence relationship for Partitions:
     P(n) = P(n-1)+P(n-2)-P(n-5)-P(n-7)+P(n-12)+P(n-15)-...
    This works, but isn't as fast as it could be:
    """
    if n < len(partitionsp): return partitionsp[n]
    if n == 0: return 1
    total = 0
    for sign,k in izip(part_signs(),pentagonal()):
        if k > n: break
        total += sign*npart(n-k)
    return total

def main():
    #guesses = get_rama_ests(30000)
    # returned: [2394, 5872, 5161, 2256, 6402, 6879, 1844,
    #            5254, 2062, 4641, 5926, 6774, 3906, 6510]
    # as good candidates
    # Using rem<100 as the filter yielded
    # [2394,5872,17445,23071]
    #print guesses
    #for rem,b,est in guesses[2:]:
    #    print rem,b,est
    #    np = count_partitions(b)
    #    print "\t\t\t",np
    print npart(100)
    return

if __name__ == '__main__': main()
    
