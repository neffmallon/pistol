#!/usr/bin/env python
"Compute the DOS from Jaguar eigenvalues"

import sys,re
from math import pow,exp,pi,sqrt
from numpy import arange

# Exponent for Gaussian delta function. 10 works for approximate systems,
#  1000 works well for resolving the peaks
GEXP = 10.0     
GSPC = 0.1        # Spacing of Gaussians

def jaguar_dos(fname):
    do_plot = 1
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

    if do_plot:
        import biggles
        p = biggles.FramedPlot()
        c = biggles.Curve(xs,ds,color='red')
        p.add(c)
        p.title = 'Jaguar density of states'
        p.xlabel = 'Energy (h)'
        p.show()
        p.write_img(400,400,'jaguar_dos.png')
    else:
        for i in range(len(xs)): print xs[i],ds[i]
    return
    
    return

def gaussian(x0,x,alpha): return sqrt(pi/alpha)*exp(-alpha*pow(x-x0,2))


def get_evs(fname):
    "Get the orbital energies from Jaguar output"
    orbpat = re.compile('Orbital energies/symmetry label')
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
    return evs

if __name__ == '__main__':
    if len(sys.argv) > 1: jaguar_dos(sys.argv[1])



