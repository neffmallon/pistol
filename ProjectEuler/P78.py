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

def get_rama_ests(nmax=10000):
    results = []
    for j in range(50,nmax):
        e = partition_upper_bound(j)
        r,rem = divmod(e,1000000)
        if rem < 2000: results.append((rem,j,e))
    results.sort()
    return results

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

if __name__ == '__main__':
    guesses = get_rama_ests()
    # returned: [2394, 5872, 5161, 2256, 6402, 6879, 1844,
    #            5254, 2062, 4641, 5926, 6774, 3906, 6510]
    # as good candidates
    for rem,b,est in guesses[:5]:
        print rem,b,est
        np = count_partitions(b)
        print "\t\t\t",np
    
