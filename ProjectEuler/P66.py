"""
Consider quadratic Diophantine equations of the form:

x^2 - Dy^2 = 1

For example, when D=13, the minimal solution in x is 649^2 - 13*180^2
= 1.

It can be assumed that there are no solutions in positive integers
when D is square.

By finding minimal solutions in x for D = {2, 3, 5, 6, 7}, we obtain
the following:

3^2 - 2*2^2 = 1
2^2 - 3*1^2 = 1
9^2 - 5*4^2 = 1
5^2 - 6*2^2 = 1
8^2 - 7*3^2 = 1

Hence, by considering minimal solutions in x for D<=7, the largest x
is obtained when D=5.

Find the value of D<=1000 in minimal solutions of x for which the
largest value of x is obtained.
"""

import psyco; psyco.full()

from math import sqrt
from Utils import sqrtcf

def issquare(n): return isint(sqrt(n))
def isint(n): return int(n) == n

def find_solutions(Ds,maxit):
    results = []
    unfound = []
    for D in Ds:
        if issquare(D): continue
        for x in xrange(2,maxit):
            y = sqrt((x*x-1)/float(D))
            if isint(y):
                results.append((D,x,int(y)))
                break
        else:
            unfound.append(D)
    return results,unfound

def sort_results(results):
    temp = [(x,D,y) for (D,x,y) in results]
    temp.sort()
    return [(D,x,y) for (x,D,y) in temp]

def print_results(results):
    results = sort_results(results)
    for D,x,y in results:
        print "%d^2 - %d x %d^2 = 1" % (x,D,y)
    D,x,y = results[-1]
    print "Maximum x value of %d obtained when D=%d" % (x,D)
    return

def xy_from_cf(a):
    r = len(a)
    p = [a[0]]
    q = [1]
    if r > 1:
        p.append(a[0]*a[1]+1)
        q.append(a[1])
        a.append(a[1])
    #if r == 2: return p[-1],q[-1]
    for i in range(2,2*r+2):
        p.append(a[i]*p[i-1]+p[i-2])
        q.append(a[i]*q[i-1]+q[i-2])
        a.append(a[i])
    return p,q
    
def cf_solution(nmax=14):
    results = []
    for D in range(2,nmax):
        if issquare(D): continue
        cf = sqrtcf(D)
        r = len(cf)
        p,q = xy_from_cf(cf)
        xs,ys = 0,0
        # There's supposed to be a way to get the x,y values for the
        # Pell equation from the even/odd value of r, but I can't
        # get this to work. But the brute method does work:
        for x,y in zip(p,q):
            if x*x-D*y*y-1 == 0:
                xs,ys = x,y
                break
        if not x:
            print "No solution for ",D
        results.append((xs,D))
    results.sort()
    print results[-10:]
    return

if __name__=='__main__': cf_solution(1000)
# Gives the correct solution of 61!
