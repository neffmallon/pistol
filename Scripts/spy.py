#!/usr/bin/env python
"""\
 spy.py: A mimic of the Matlab spy/pcolor functions.

 Usage: spy.py <options> filename

 Options:
 -a    Use absolute values of matrix
 -s    Spy matrix to find sparsity pattern (default)
 -p    Pseudocolor matrix
 -c #  Use # as cutoff fraction for spy function (default=0.5)
 -H #  Create window with a height of # (default=300)
 -W #  Create window with a width of # (default=300)
 
Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""
from numpy import zeros
from Pistol.MatrixViewer import pcolor_matrix_pil, spy_matrix_pil

if __name__ == '__main__':
    import sys,getopt
    opts,args = getopt.getopt(sys.argv[1:],'ahspH:W:c:t')

    function = 'spy'
    height = 300
    width = 300
    cutoff = 0.1
    test = 0
    doabs = 0
    
    for (key,val) in opts:
        if key == '-h':
            print __doc__
            sys.exit()
        if key == '-s':
            function = 'spy'
        if key == '-p':
            function = 'pcolor'
        if key == '-H':
            height = int(val)
        if key == '-W':
            width = int(val)
        if key == '-c':
            cutoff = float(val)
        if key == '-t':
            test = 1
        if key == '-a':
            doabs = 1

    if test:
        import random
        A = zeros((100,100),Float)
        for i in range(100):
            for j in range(100):
                A[i,j] = 0.2*random.random()
        oname = "test.png"
    else:
        fname = args[0]
        oname = fname.replace(".dat",".png")
        A = read_matrix(fname)

    if doabs: A = abs(A)

    if function == 'pcolor':
        pcolor_matrix_pil(A,oname,0,height,width)
    else:
        spy_matrix_pil(A,oname,cutoff,0,height,width)
