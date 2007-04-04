#!/usr/bin/env python
"Compute the DOS from Jaguar eigenvalues"

import sys,re
from math import pow,exp,pi,sqrt
from numpy import arange
from pylab import *


def jaguar_dos(fname,**kwargs):
    do_plot = kwargs.get('do_plot',True)

    # Exponent for Gaussian delta function. 10 works for approximate systems,
    #  1000 works well for resolving the peaks
    GEXP = kwargs.get('GEXP',5.)
    GSPC = kwargs.get('GSPC',0.1)   # Spacing of Gaussians
    
    evs = get_evs(fname)
    gs = []
    mine = min(evs)
    maxe = max(evs)
    ds = []
    xs = arange(mine-5,maxe+5,GSPC)
    for x0 in xs:
        d = 0
        for x in evs:
            d += gaussian(x0,x,GEXP)
        ds.append(d)
    return xs,ds

def gaussian(x0,x,alpha):
    arg = alpha*pow(x-x0,2)
    if arg > 100: return 0
    return sqrt(pi/alpha)*exp(-arg)


def get_evs(fname):
    "Get the orbital energies from Jaguar output"
    orbpat = re.compile('Orbital energies/symmetry label')
    orbpat_nosym = re.compile('Orbital energies:')
    file = open(fname)
    while 1:
        line = file.readline()
        if not line: break
        if orbpat.search(line):
            evs = []
            while 1:
                line = file.readline()
                if not line: break
                words = line.split()
                if not words: break
                for w in words[0:-1:2]: evs.append(float(w))
        if orbpat_nosym.search(line):
            evs = []
            while 1:
                line = file.readline()
                if not line: break
                words = line.split()
                if not words: break
                for w in words: evs.append(float(w))
    return evs

if __name__ == '__main__':
    if len(sys.argv) > 1:
        for fname in sys.argv[1:]:
            xs,ds = jaguar_dos(fname)
            froot = fname.replace('.out','')
            plot(xs,ds,label=froot)
        legend(loc='upper left')
        xlabel("E/h")
        ylabel("Density of states")
        show()



