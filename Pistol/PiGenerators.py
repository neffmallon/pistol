#!/usr/bin/env python
"""\
 Examples of different ways to compute pi

 Same as Pi.py, but with generators

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""
import os
from math import sqrt

def pi_simple():
    """\
    Generate a simple MC sequence, coming from seeing what fraction of
    random (0,1) points are inside the unit sphere (which should be
    pi/4
    """
    from random import random
    hits = 0
    i = 0
    while True:
        x,y = random(),random()
        if x*x+y*y < 1: hits += 1
        yield 4*hits/(i+1.)
        i += 1
    return

def pi_simple_qr():
    """\
    Generate a simple MC sequence, coming from seeing what fraction of
    random (0,1) points are inside the unit sphere (which should be
    pi/4

    This version uses a Sobol Sequence as a quasi-random sequence
    """
    from Pistol.QuasiRandom import SobolSequence

    qr = SobolSequence(2)
    hits = 0
    i = 0
    while True:
        x,y = qr()
        if x*x+y*y < 1: hits += 1
        yield 4*hits/(i+1.)
        i += 1
    return

def pi_leibniz1():
    """\
    Approximate pi via Leibniz's series:
    pi/4 = sum -1^i/(2*i+1)
    (expansion of arctan(1)
    """
    total = 0
    i = 0
    while True:
        index = 2*i+1.
        total += pow(-1,i)/index
        yield 4*total
        i += 1
    return

def pi_leibniz2():
    """\
    Approximate pi via another of Leibniz's series:
    pi/4 = sum -1^i/(2*i+1)
    """
    total = 0
    i = 0
    while True:
        index = 2*i+1.
        total += pow(-1/3.,i)/index
        yield 2*sqrt(3)*total
        i += 1
    return

def pi_mc_circle():
    "Another way of integrating Leibniz's series"
    from random import random
    total = 0
    i = 0
    while True:
        x = random()
        total += 1/(1.+x*x)
        yield 4*total/(i+1.)
        i += 1
    return

def pi_mc_circle2():
    "Integrate the quarter circle sqrt(1-x^2)"
    from random import random
    total = 0
    i = 0
    while True:
        x = random()
        total += sqrt(1-x*x)
        yield 4*total/(i+1.)
        i += 1
    return

def pi_gauss():
    "Gauss' method, taken from projectpi.sf.net, written by M. Reber"
    a,b = 1.,1/sqrt(2)
    x,y,c = a,a,a/4
    i = 0
    while True:
        y = a
        a = 0.5*(a+b)
        b = sqrt(b*y)
        c = c-x*(a-y)*(a-y)
        x *= 2
        yield (a+b)*(a+b)/4/c
        i += 1
    return

def pi_rama():
    "Ramanujan's series for 1/pi, taken from a javascript app by John Bohr"
    # This is so accurate that it only makes sense to do it with an
    #  arbitrary precision package such as gmpy.
    # With Python floats this essentially hits machine precision at the
    #  first iteration!
    pre = sqrt(8)/float(9801)
    sum = 0
    i = 0
    while True:
        num = fact(4*i)*(1103+26390*i)
        den = pow(fact(i),4)*pow(396,4*i)
        sum += num/den
        yield 1/pre/sum
        i += 1
    return

# The cache makes fact fairly efficient, even in Python
fact_cache = [1,1,2,6,24,120,720,5040]
def fact(n):
    if n < len(fact_cache): return fact_cache[n]
    return n*fact(n-1)

def take(gen,npts):
    for i in range(npts):
        yield gen.next()
    return

def drop(gen,npts):
    for i in range(npts): gen.next()
    return
        

def skip(gen,skip):
    "Skip every *skip* steps and then yield an entry"
    while True:
        drop(gen,skip)
        yield gen.next()

# Reference to all generators:
genfuncs = [
    pi_simple,
    pi_simple_qr,
    pi_leibniz1,
    pi_leibniz2,
    pi_mc_circle,
    pi_mc_circle2,
    pi_gauss,
    pi_rama,
    ]

genfuncs2 = [pi_simple, pi_leibniz1, pi_leibniz2]

def plot_pi_mpl(npts=100,funcs=genfuncs):
    from pylab import plot, title, xlabel, ylabel,savefig,legend,show

    title('Pi computed using different approximations')
    xlabel('Step')
    ylabel(r'$\pi$')

    steps = range(npts)
    for func in funcs: plot(steps,list(take(func(),npts)))

    labels = [func.__name__ for func in funcs]
    legend(labels,shadow=True)
    #savefig('pi')
    #os.system('display pi.png')
    return

def plot_pi_gnuplot(npts=100,funcs=genfuncs):
    from Gnuplot import Gnuplot,Data
    g = Gnuplot()
    g.title("Pi computed using different approximations")
    g("set yrange [2:4]")
    steps = range(npts)
    data = []
    for func in funcs:
        data.append(Data(steps,list(take(func(),npts)),
                         with='lines',title=func.__name__))
    apply(g.plot,data)
    return

def plot_pi_biggles(npts=100,funcs=genfuncs):
    import biggles
    g = biggles.FramedPlot()
    steps = range(npts)
    for func in funcs:
        datum = biggles.Curve(steps,list(take(func(),npts)))
        g.add(datum)
    g.show()
    return

def mpipi(npoints=100,function=pi_simple):
    from random import random,seed
    import mpi
    seed(random()*mpi.rank) # BAD way of doing parallel RNG
    seq = list(take(func(),npts))
    pi = seq[-1]
    pi_sum = mpi.reduce(pi,mpi.SUM)
    if mpi.rank == 0: print pi_sum/float(mpi.size)

if __name__ == '__main__':
    plot_pi_mpl(1000,genfuncs2)


