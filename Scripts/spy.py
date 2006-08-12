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
from Numeric import *
from Pistol.MatrixViewer import MatrixViewer

def round(x): return int(x+0.5)

def root(namestring):
    import string
    words = string.split(namestring,'.')
    if len(words) < 1:
        return ''
    root = words[0]
    for i in range(1,len(words)-1):
        root = root + '.' + words[i]
    return root

def get_color(a,cmin,cmax):
    # rewritten to use recipe 9.10 from the Python Cookbook
    import math
    try: a = float(a-cmin)/(cmax-cmin)
    except ZeroDivisionError: a=0.5 # cmax == cmin
    blue = min((max((4*(0.75-a),0.)),1.))
    red = min((max((4*(a-0.25),0.)),1.))
    green = min((max((4*math.fabs(a-0.5)-1.,0)),1.))
    return '#%1x%1x%1x' % (int(15*red),int(15*green),int(15*blue))

def get_extrema(A):
    n,m = A.shape
    BIG = 10000.0
    max = -BIG
    min = BIG
    for i in range(n):
        for j in range(m):
            if A[i,j] < min:
                min = A[i,j]
            elif A[i,j] > max:
                max = A[i,j]
    return min,max

def read_matrix(filename):
    file = open(filename)
    line = file.readline()

    words = line.split()
    if len(words) == 1:
        n = m = int(words[0])
    elif len(words) == 2:
        n,m = map(int,words)
    else:
        raise "Matrix file %s in wrong format" % filename
    
    A = zeros((n,m),Float)
    for i in range(n):
        line = file.readline()
        vals = map(float,line.split())
        for j in range(m):
            A[i,j] = vals[j]
    file.close()
    return A

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
        mv = MatrixViewer(height,width,'test.ps')
        A = zeros((100,100),Float)
        for i in range(100):
            for j in range(100):
                A[i,j] = 0.2*random.random()
    else:
        filename = args[0]
        mv = MatrixViewer(height,width,root(filename)+'.ps')
        A = read_matrix(filename)

    if doabs: A = abs(A)

    if function == 'pcolor':
        mv.pcolor(A)
    else:
        mv.spy(A,cutoff)
