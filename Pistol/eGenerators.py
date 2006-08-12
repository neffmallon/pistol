#!/usr/bin/env python

import os
fact_cache = [1,1,2,6,24,120,720,5040]

def fact(i):
    if i < len(fact_cache):
        return fact_cache[i]
    return i*fact(i-1)

def eGenerator(MAXPTS=None):
    i = 0
    e = 0
    while True:
        if MAXPTS and i >= MAXPTS: break
        e += 1./fact(i)
        yield e
        i += 1
    return

def sequence(gen,npts): return [gen.next() for i in range(npts)]

def plot_e(npts=100):
    from pylab import plot, title, xlabel, ylabel, savefig,legend,semilogx

    xlabel('Step')
    ylabel('Value of e')

    steps = range(npts)

    plot(steps,sequence(eGenerator(),npts))
    savefig('pi')
    os.system('display pi.png')
    return
        
if __name__ == '__main__':
    print sequence(eGenerator(),20)
    #plot_e(20)
