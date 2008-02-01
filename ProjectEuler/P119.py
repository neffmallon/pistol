#!/usr/bin/env python

from time import time

def simple_powers_table(nmax=100,pmax=10):
    spt = [[],[1]]
    for i in range(2,nmax):
        spti = [1]
        spt.append(spti)
        p = i
        for j in range(1,pmax):
            spti.append(p)
            p*=i
    return spt

def brute(nmax=10000000,pmax=10):
    index = 1
    for i in range(10,nmax):
        digsum = sum(map(int,str(i)))
        for j in range(1,pmax):
            p = pow(digsum,j)
            if p == i:
                print "(%3d) %d == %d**%d == %d" % (index,i,digsum,j,p)
                index += 1
            if p > i: break
    return

def clever(nmax=100000000):
    spt = simple_powers_table()
    index = 1
    for i in xrange(10,nmax):
        digsum = sum(map(int,str(i)))
        if i in spt[digsum]:
            print "(%3d) %d == %d**x" % (index,i,digsum)
            index += 1
    return

def main():
    t0 = time()
    clever()
    print time()-t0
    return

if __name__ == '__main__': main()


            
