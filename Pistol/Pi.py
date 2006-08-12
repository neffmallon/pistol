#!/usr/bin/env python
"""\
 Examples of different ways to compute pi

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

from math import sqrt

def pi_simple(npts=100):
    """\
    Generate a simple MC sequence, coming from seeing what fraction of
    random (0,1) points are inside the unit sphere (which should be
    pi/4
    """
    from random import random
    hits = 0
    data = []
    for i in range(npts):
        x,y = random(),random()
        if x*x+y*y < 1: hits += 1
        data.append(4*hits/(i+1.))
    return data

def pi_simple_qr(npts=100):
    """\
    Generate a simple MC sequence, coming from seeing what fraction of
    random (0,1) points are inside the unit sphere (which should be
    pi/4

    This version uses a Sobol Sequence as a quasi-random sequence
    """
    from Pistol.QuasiRandom import SobolSequence

    qr = SobolSequence(2)
    hits = 0
    data = []
    for i in range(npts):
        x,y = qr()
        if x*x+y*y < 1: hits += 1
        data.append(4*hits/(i+1.))
    return data

def pi_leibniz1(npts=100):
    """\
    Approximate pi via Leibniz's series:
    pi/4 = sum -1^i/(2*i+1)
    (expansion of arctan(1)
    """
    total = 0
    data = []
    for i in range(npts):
        index = 2*i+1.
        total += pow(-1,i)/index
        data.append(4*total)
    return data

def pi_leibniz2(npts=100):
    """\
    Approximate pi via another of Leibniz's series:
    pi/4 = sum -1^i/(2*i+1)
    """
    total = 0
    data =  []
    for i in range(npts):
        index = 2*i+1.
        total += pow(-1/3.,i)/index
        data.append(2*sqrt(3)*total)
    return data

def pi_mc_circle(npts=100):
    "Another way of integrating Leibniz's series"
    from random import random
    total = 0
    data = []
    for i in range(npts):
        x = random()
        total += 1/(1.+x*x)
        data.append(4*total/(i+1.))
    return data

def pi_mc_circle2(npts=100):
    "Integrate the quarter circle sqrt(1-x^2)"
    from random import random
    total = 0
    data = []
    for i in range(npts):
        x = random()
        total += sqrt(1-x*x)
        data.append(4*total/(i+1.))
    return data

def pi_gauss(npts=100):
    "Gauss' method, taken from projectpi.sf.net, written by M. Reber"
    a,b = 1.,1/sqrt(2)
    x,y,c = a,a,a/4
    data = []
    for i in range(npts):
        y = a
        a = 0.5*(a+b)
        b = sqrt(b*y)
        c = c-x*(a-y)*(a-y)
        x *= 2
        data.append((a+b)*(a+b)/4/c)
    return data

def pi_rama(npts=100):
    "Ramanujan's series for 1/pi, taken from a javascript app by John Bohr"
    # This is so accurate that it only makes sense to do it with an
    #  arbitrary precision package such as gmpy.
    # With Python floats this essentially hits machine precision at the
    #  first iteration!
    pre = sqrt(8)/float(9801)
    data = []
    sum = 0
    for i in range(npts):
        num = fact(4*i)*(1103+26390*i)
        den = pow(fact(i),4)*pow(396,4*i)
        sum +=num/den
        data.append(1/pre/sum)
    return data

# The cache makes fact  fairly efficient, even in Python
fact_cache = [1,1,2,6,24,120,720,5040]
def fact(n):
    if n < len(fact_cache): return fact_cache[n]
    return n*fact(n-1)

def plot_pi_mpl(npts=100):
    from pylab import plot, title, xlabel, ylabel, savefig,legend,semilogx

    title('Pi computed using different approximations')
    xlabel('Step')
    ylabel('Value of pi')

    steps = range(npts)

    plotter = plot
    #plotter = semilogx
    for func in sequences:
        plotter(steps,func(npts))

    labels = [func.__name__ for func in sequences]
    legend(labels,shadow=True)
    savefig('pi')
    return

def plot_pi_gnuplot(npts=100):
    from Gnuplot import Gnuplot,Data
    g = Gnuplot()
    g.title("Pi computed using different approximations")
    g("set yrange [2:4]")
    steps = range(npts)
    data = []
    for func in sequences:
        data.append(Data(steps,func(npts),with='lines',title=func.__name__))
    apply(g.plot,data)
    return

def plot_pi_biggles(npts=100):
    import biggles
    g = biggles.FramedPlot()
    steps = range(npts)
    for func in sequences:
        datum = biggles.Curve(steps,func(npts))
        g.add(datum)
    g.show()
    return

def mpipi(npoints=100,function=pi_simple):
    from random import random,seed
    import mpi
    seed(random()*mpi.rank) # BAD way of doing parallel RNG
    seq = function(npts)
    pi = seq[-1]
    pi_sum = mpi.reduce(pi,mpi.SUM)
    if mpi.rank == 0: print pi_sum/float(mpi.size)

# Reference to all sequences:
sequences = [
    pi_simple,
    pi_simple_qr,
    pi_leibniz1,
    pi_leibniz2,
    pi_mc_circle,
    pi_mc_circle2,
    pi_gauss,
    pi_rama,
    ]

if __name__ == '__main__': plot_pi_mpl(15)
