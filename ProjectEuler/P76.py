"""
It is possible to write five as a sum in exactly six different ways:

4 + 1
3 + 2
3 + 1 + 1
2 + 2 + 1
2 + 1 + 1 + 1
1 + 1 + 1 + 1 + 1

How many different ways can one hundred be written as a sum of at
least two positive integers?
"""

from math import exp,pi,sqrt

def partition_upper_bound(k):
    """Ramanujan's upper bound for number of partitions of k"""
    return int(exp(pi*sqrt(2.0*k/3.0))/(4.0*k*sqrt(3.0)))

def partitions(n):
    # base case of recursion: zero is the sum of the empty list
    if n == 0:
        yield []
        return
		
    # modify partitions of n-1 to form partitions of n
    for p in partitions(n-1):
        yield [1] + p
        if p and (len(p) < 2 or p[1] > p[0]):
            yield [p[0] + 1] + p[1:]
    return

def next_partition(p):
    "Taken from the perl monks recipe 621859, which I don't understand"
    from copy import copy
    p2 = copy(p)

    # Collect all the trailing 1s
    x = 0
    while p2 and p2[-1] == 1:
        x += p2.pop()
    if not p2: return []

    # Collect 1 from the rightmost remaining element
    p2[-1] -= 1
    x += 1

    while x > p2[-1]:
        p2.append(p2[-1])
        x -= p2[-1]
    p2.append(x)
    return p2

n = 50
p = [n]
npart = 0
while 1:
    #print p
    p = next_partition(p)
    if not p: break
    npart += 1
print npart,upper_bound(n)

    



