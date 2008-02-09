#!/usr/bin/env python

from pprint import pprint
from sets import Set
from math import sqrt
from Utils import next_partition,prod

defrange = range(10)

def ntuples(n,set=defrange):
    res = []
    if n <= 1: return [[i] for i in set]
    for tup in ntuples(n-1,set):
        for i in set:
            res.append(tup+[i])
    return res

def ntuples2(n,kmax):
    if n <= 1: return [[i] for i in range(2,kmax)]
    res = []
    for tup in ntuples2(n-1,kmax):
        p = prod(tup)
        istart = tup[-1]
        for i in range(istart,kmax/p):
            res.append(tup + [i])
    return res

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
    

def brute(kmax=100):
    # This seems like a good approach, but I need a general way of
    # generating n-tuples
    results = [None]*kmax
    # look for pairs first
    for i in range(2,kmax):
        for j in range(i,kmax/i):
            s = i+j
            p = i*j
            diff = p-s
            index = diff+2 # pairs go with 2
            if not results[index] or p < prod(results[index]):
                results[index] = (i,j)
    # Find triples now
    for i in range(2,kmax):
        for j in range(i,kmax/i):
            for k in range(j,kmax/(i*j)):
                s = i+j+k
                p = i*j*k
                diff = p-s
                index = diff+3
                if not results[index] or p < prod(results[index]):
                    results[index] = (i,j,k)
    # Find quartets
    for i in range(2,kmax):
        for j in range(i,kmax/i):
            for k in range(j,kmax/(i*j)):
                for l in range(k,kmax/(i*j*k)):
                    s = i+j+k+l
                    p = i*j*k*l
                    diff = p-s
                    index = diff+4
                    if not results[index] or p < prod(results[index]):
                        results[index] = (i,j,k,l)
    print results

def brute2(kmax=100,tmax=4):
    # This seems like a good approach, but I need a general way of
    # generating n-tuples
    results = [None]*kmax
    for tlength in range(2,tmax+1):
        for tup in ntuples2(tlength,kmax):
            s = sum(tup)
            p = prod(tup)
            diff = p-s
            index = diff + tlength
            if not results[index] or p < prod(results[index]):
                results[index] = tup
    return results

def test_tuples():
    kmax = 100
    print ntuples2(4,100)
    for i in range(2,kmax):
        for j in range(i,kmax/i):
            for k in range(j,kmax/(i*j)):
                for l in range(k,kmax/(i*j*k)):
                    print [i,j,k,l],

def main():
    kmax = 12000
    expansion = 10
    maxtup = 100
    results = brute2(kmax*expansion,maxtup)
    print results[2:(kmax+1)]
    p = [prod(tup) for tup in results[2:(kmax+1)]]
    print p
    print sum(Set(p))

if __name__ == '__main__': main()

