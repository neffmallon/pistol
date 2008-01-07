"""
It turns out that 12 cm is the smallest length of wire can be bent to
form a right angle triangle in exactly one way, but there are many
more examples.

12 cm: (3,4,5)
24 cm: (6,8,10)
30 cm: (5,12,13)
36 cm: (9,12,15)
40 cm: (8,15,17)
48 cm: (12,16,20)

In contrast, some lengths of wire, like 20 cm, cannot be bent to form
a right angle triangle, and other lengths allow more than one solution
to be found; for example, using 120 cm it is possible to form exactly
three different right angle triangles.

120 cm: (30,40,50), (20,48,52), (24,45,51)

Given that L is the length of the wire, for how many values of L <=
1,000,000 can exactly one right angle triangle be formed?
"""

import psyco; psyco.full()
from time import time
from math import sqrt
from sets import Set

def isint(n): return int(n) == n

def formula(nmax = 100):
    results = {}
    for m in range(1,nmax):
        m2 = m*m
        for n in range(1,m):
            n2 = n*n
            a = m2-n2
            b = 2*m*n
            c = m2+n2
            p = a+b+c
            if p > nmax: continue
            l = [a,b,c]
            l.sort()
            a,b,c = l
            for n in range(1,nmax/p+1):
                if n*p in results:
                    results[n*p].add((n*a,n*b,n*c))
                else:
                    results[n*p] = Set([(n*a,n*b,n*c)])
    return results

def brute(nmax=100):
    from math import sqrt
    results = {}
    for a in range(1,nmax):
        if a % 1000 == 0:
            print "Before step %d in brute()" % a
        a2 = a*a
        for b in range(1,a):
            if a+b > nmax: break
            b2 = b*b
            c = sqrt(a2+b2)
            if a+b+c > nmax: break
            if isint(c):
                c = int(c)
                p = a+b+c
                if p in results:
                    results[p].append((b,a,c))
                else:
                    results[p] = [(b,a,c)]

    return results

# I thought this would be faster, but it was actually slower
def sosfunc(nmax):
    "Compute the sum of squares function"
    sos = {}
    for a in range(1,nmax+1):
        a2 = a**2
        for b in range(1,a):
            b2 = b**2
            c2 = a2+b2
            if c2 in sos:
                sos[c2].append((b,a))
            else:
                sos[c2] = [(b,a)]
    return sos

def using_sos(nmax = 10000):
    sos = sosfunc(nmax)
    results = {}
    for c in range(1,nmax):
        ab = sos.get(c*c,[])
        for a,b in ab:
            p = a+b+c
            if p > nmax: continue
            if p in results:
                results[p].append((a,b,c))
            else:
                results[p] = [(a,b,c)]
    return results

def pdict(results):
    ps = results.keys()
    ps.sort()
    for p in ps:
        print p,results[p]
    return

def nunit(results):
    n = 0
    for p in results:
        if len(results[p]) == 1: n += 1
    return n

# Notes: look at forum for problem 39 for hints
nmax = 5000
t0 = time()
results = brute(nmax)
t1 = time()
#pdict(results)
#print nunit(results)
results = formula(nmax)
t2 = time()
#pdict(results)
#print nunit(results)
print t1-t0,t2-t1


