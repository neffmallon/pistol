#!/usr/bin/env python

from pprint import pprint
from sets import Set
from Utils import next_partition,prod

def prodsums(n):
    p = [n]
    results = []
    while True:
        p = next_partition(p)
        if not p:
            break
        if prod(p) == n:
            results.append(p)
    return results

def test1():
    print prodsums(6)

def prodsumrange(nmax=20):
    results = {}
    for i in range(1,nmax+1):
        ps = prodsums(i)
        for p in ps:
            l = len(p)
            if l in results:
                results[l].append(p)
            else:
                results[l] = [p]
    return results

def minprodsums(prodsums):
    mps = [0]*(max(prodsums.keys())+1)
    for l in prodsums:
        s = [sum(p) for p in prodsums[l]]
        mps[l] = min(s)
    return mps

def works_small(nmax=50):
    # This only works for small nmax, say below 50. The number
    #  of partitions grows too quickly beyond that
    results = prodsumrange(nmax)
    mps = minprodsums(results)
    print mps
    print sum(Set(mps[:nmax]))

def main(kmax=30):
    ps = prodsumrange(kmax)
    ks = ps.keys()
    ks.sort()
    for k in ks:
        print k,min([sum(p) for p in ps[k]])

if __name__ == '__main__': main()

