#!/usr/bin/env python
"Playing around with lattice monte carlo"

from random import choice
from numpy import Float, array, zeros,log
from numpy.oldnumeric.linear_algebra import linear_least_squares
from Gnuplot import Gnuplot, Data

s2d = [(1,0),(0,1),(-1,0),(0,-1)]
s3d = [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]

def expfit(xs,ys):
    xs = array(xs)
    ys = array(ys)
    n = len(xs)
    assert n == len(ys)
    a = zeros((n,2),Float)
    b = zeros(n,Float)
    a[:,0] = log(xs)
    b[:] = log(ys)
    a[:,1] = 1.
    d,e,f,g = linear_least_squares(a,b)
    print d
    return
    
          
def step_incr_1d(n): return [choice([-1,1]) for i in range(n)]
def step_incr_2d(n): return [choice(s2d) for i in range(n)]
def step_incr_3d(n): return [choice(s3d) for i in range(n)]

def walk_3d(n):
    results = []
    x,y,z = 0,0,0
    for xi,yi,zi in step_incr_3d(n):
        x += xi
        y += yi
        z += zi
        results.append((x,y,z))
    return results


def walk_2d(n):
    results = []
    x,y = 0,0
    for xs,ys in step_incr_2d(n):
        x += xs
        y += ys
        results.append((x,y))
    return results


def walk_1d(n):
    results = []
    sum = 0
    for step in step_incr_1d(n):
        sum += step
        results.append(sum)
    return results

def main_1d(n=100):
    walk = walk_1d(n)
    xs = range(n)
    ys = walk
    return

def sample_r2_2d(n=1000,trials=1000):
    sum = 0
    for i in range(trials):
        walk = walk_2d(n)
        x,y = walk[-1]
        sum += x*x+y*y
    return sum/float(trials)

def main(nmax=50,ntrials=1000):
    xs = []
    ys = []
    for i in range(10,nmax):
        r2 = sample_r2_2d(i,ntrials)
        xs.append(i)
        ys.append(r2)
    p = biggles.FramedPlot()
    p.add(biggles.Curve(xs,ys))
    p.show()
    expfit(xs,ys)
    return

def sample_r2_3d(n=1000,ntrials=1000):
    sum = 0
    for i in range(ntrials):
        walk = walk_3d(n)
        x,y,z = walk[-1]
        sum += x*x+y*y*z*z
    return sum/float(ntrials)


def main(nmax=100,ntrials=1000):
    xs = []
    ys = []
    for i in range(10,nmax):
        r2 = sample_r2_3d(i,ntrials)
        xs.append(i)
        ys.append(r2)
    p = biggles.FramedPlot()
    p.add(biggles.Curve(xs,ys))
    p.show()

    #p = Gnuplot()
    #p.title("Lattice MC Random Walk 3D")
    #p.xlabel('N')
    #p.ylabel('<r^2>')
    #p('set data style linespoints')
    #d = Data(xs,ys)
    #p.plot(d)

    expfit(xs,ys)
    return

if __name__ == '__main__': main()

    
