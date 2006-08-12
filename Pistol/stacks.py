#!/usr/bin/env python

from random import shuffle

def reduce(plates):
    n = len(plates)
    n2,rem = divmod(n,2)
    if rem: raise "This only works for even sized stacks of plates"
    reduced = []
    for i in range(n2):
        reduced.append( plates[2*i]+plates[2*i+1] )
    return reduced

def ordered(plates):
    reduced = reduce(plates)
    return not (0 in reduced or 2 in reduced)

def create_all_possible(nplates,ntries=10000):
    nplates2,rem = divmod(nplates,2)
    if rem: raise "This only works for even sized stacks of plates"
    ntot = 0
    plates = {}

    for i in range(ntries):
        a = range(nplates)
        shuffle(a)
        guess = a[:nplates2]
        guess.sort()
        plates[tuple(guess)] = 1
    items = plates.keys()
    items.sort()
    plates = []
    for i in items:
        z = [0]*nplates
        for j in i: z[j] = 1
        plates.append(z)
    return plates

def test():
    nplates = 12
    plates = create_all_possible(nplates)
    
    ngood = 0
    for plate in plates:
        if ordered(plate): ngood += 1
    print ngood, len(plates),ngood/float(len(plates))

if __name__ == '__main__': test()

        
