#!/usr/bin/env python

from time import time

def simple_powers_table(nmax=100,pmax=10):
    spt = [[],[1]]
    for i in xrange(2,nmax):
        spti = [1]
        spt.append(spti)
        p = i
        for j in xrange(1,pmax):
            spti.append(p)
            p*=i
    return spt

def clever(nmax=100):
    from itertools import count
    spt = simple_powers_table(200,20)
    index = 1
    for i in count(10):
        digsum = sum(map(int,str(i)))
        if i % digsum > 0: continue
        if i % digsum**2 > 0: continue
        if i in spt[digsum]:
            print "(%3d) %d == %d**%d" % (index,i,digsum,spt[digsum].index(i))
            index += 1
    return

def brute(nmax=10000000,pmax=10):
    index = 1
    for i in xrange(10,nmax):
        digsum = sum(map(int,str(i)))
        if i % digsum > 0: continue
        for j in range(1,pmax):
            p = pow(digsum,j)
            if p == i:
                print "(%3d) %d == %d**%d == %d" % (index,i,digsum,j,p)
                index += 1
            if p > i: break
    return

def digsum(i): return sum(map(int,str(i)))

def clever2(nmax=200,pmax=20):
    results = []
    for i in xrange(2,nmax):
        p = i
        for j in xrange(1,pmax):
            if p>10 and digsum(p) == i:
                results.append(p)
            p*=i
    results.sort()
    for i,p in enumerate(results[:40]):
        print i+1,p
    return 


# Here's what I've found so far:
# (  1) 81 == 9**2
# (  2) 512 == 8**3
# (  3) 2401 == 7**4
# (  4) 4913 == 17**3
# (  5) 5832 == 18**3
# (  6) 17576 == 26**3
# (  7) 19683 == 27**3
# (  8) 234256 == 22**4
# (  9) 390625 == 25**4
# ( 10) 614656 == 28**4
# ( 11) 1679616 == 36**4
# ( 12) 17210368 == 28**5
# ( 13) 34012224 == 18**6
# ( 14) 52521875 == 35**5
# ( 15) 60466176 == 36**5
# ( 16) 205962976 == 46**5
# ( 17) 612,220,032 == 18**7

def main():
    t0 = time()
    nmax=1000000000
    #brute(nmax)
    clever2()
    print time()-t0
    return

if __name__ == '__main__': main()


            
