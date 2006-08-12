#!/usr/bin/env python
"""\
 Util.py Miscellaneous Python utility functions

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

def cleansym(s):
    """This function strips off the garbage (everything after and including
       the first non-letter) in an element name."""
    import re 
    return re.split('[^a-zA-Z]',s)[0]

def root(name):
    import os.path
    return os.path.splitext(name)[0]

def extension(name):
    import os.path
    return os.path.splitext(name)[1]

def get_ints(file):
    ints = map(int,file.readline().split())
    if len(ints) == 1: return ints[0]
    return ints

def get_floats(file):
    floats = map(float,file.readline().split())
    if len(floats) == 1: return floats[0]
    return floats

def convert2bohr(geo):
    from Constants import angstrom_to_bohr as ang2bohr
    newgeo = []
    for sym,x,y,z in geo:
        newgeo.append((sym,x*ang2bohr,y*ang2bohr,z*ang2bohr))
    return newgeo

def translate2com(geo):
    from Element import mass,sym2no
    xcom = ycom = zcom = totmass = 0
    for (sym,x,y,z) in geo:
        atno = sym2no[sym]
        atmass = mass[atno]
        xcom = xcom + atmass*x
        ycom = ycom + atmass*y
        zcom = zcom + atmass*z
        totmass = totmass + atmass
    xcom = xcom/totmass
    ycom = ycom/totmass
    zcom = zcom/totmass

    newgeo = []
    for (sym,x,y,z) in geo:
        newgeo.append((sym,x-xcom,y-ycom,z-zcom))
    return newgeo

def is_approx(a,b,delta=0.001):
    return abs(a-b) < delta

def matrix_symmetrize(matrix):
    n,m = matrix.shape
    assert n == m, "Symmetrize only makes sense for square matrices"
    for i in range(n):
        for j in range(i):
            matrix[j,i] = matrix[i,j]
    return matrix

def distance(ri,rj):
    import math
    x = ri[0]-rj[0]
    y = ri[1]-rj[1]
    z = ri[2]-rj[2]
    return math.sqrt(x*x+y*y+z*z)

def frange(start,end=None,inc=1.0):
    "range-like function that accepts float increments. From Cookbook 1.15"
    if end == None:
        end = start + 0.0 # ensures float
        start = 0.0
    assert inc # sanity check

    L = []
    while 1:
        next = start + len(L)*inc
        if inc >0 and next >= end:
            break
        elif inc < 0 and next <= end:
            break
        L.append(next)
    return L


def numpy_io(lines):
    """Simple routine to take a set of data in text output
       form, and do ones best to convert it into a numpy
       array."""
    from Numeric import array
    data = []
    for line in lines:
        words = line.split()
        if not words: continue
        if words[0][0] == '#': continue
        datum = []
        # The following isn't foolproof:
        for word in words: datum.append(eval(word))
        data.append(datum)
    return array(data)

def grepval(file,pats,**opts):
    """Given a list of patterns, find the values associated
       with all re.matches of those patterns.

       If doeval is false, the routine returns the lines that
       match the pattern.

       If doeval is true, each pattern must define one re group,
       which will be eval-ed and returned.
    """
    import re
    # Can call with a filename or a file handle
    if type(file) == type(''): return grepval(open(file),pats,**opts)
    doeval = opts.get('doeval',False)

    patterns = []
    for pat in pats: patterns.append(re.compile(pat))

    val = None
    for line in file:
        for pat in patterns:
            if pat.search(line):
                val = line.strip()
                if doeval:
                    val = pat.search(line).group(1)
                    val = eval(val)
    return val

def test_grepval():
    fname = "/Users/rmuller/Projects/hydrogen/quest_compression/p00.out"
    print grepval(fname,['^\s*TOTAL ENERGY.*=\s*([-\d\.]+)'])

if __name__ == '__main__': test_grepval()

