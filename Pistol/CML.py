#!/usr/bin/env python
"""\
 CML.py Utilities for reading (not yet) and writing CML files

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import math
from TupleMath import *
from Pistol.Element import symbol

def matrix2abcabg(lattice):
    la,lb,lc = lattice
    a,b,c = length(la),length(lb),length(lc)
    gamma = math.acos(dot(la,lb)/a/b)*180/math.pi
    beta =  math.acos(dot(la,lc)/a/c)*180/math.pi
    alpha = math.acos(dot(lb,lc)/b/c)*180/math.pi
    return a,b,c,alpha,beta,gamma

def write(fname,geos):
    lines = ["<?xml version=\"1.0\"?>\n"]
    lines += list(geos)
    open(fname,'w').writelines(lines)
    return

def write1(fname,geo,lattice=None):
    # Specialized version that skips lists:
    lines = ["<?xml version=\"1.0\"?>\n"]
    if lattice:
        lines += xmolecule(geo,lattice)
    else:
        lines += molecule(geo)
    open(fname,'w').writelines(lines)
    return

def list(geos):
    lines = ["<list convention=\"JMOL-ANIMATION\">\n"]
    for i in range(len(geos)): lines += molecule(geos[i],i+1)
    lines.append("</list>\n")
    return lines

def xmolecule(geo,lattice=None,id=0):
    "Molecule with an optional lattice"
    lines = []
    lines.append(" <molecule id=\"FRAME%d\">\n" % id )
    if lattice: lines += crystal(lattice)
    lines += atomArray(geo)
    lines.append(" </molecule>\n")
    return lines


# use v 1.0 for now, because of problems with lattice images
#  when using a,b,c,alpha,beta,gamma form
def crystal(lattice): return crystal_v1(lattice)

def crystal_v1(lattice):
    lines = []
    lines.append("    <crystal>\n")
    a,b,c = lattice
    lines.append('      <floatArray convention="PMP" title="a">')
    lines.append('%f %f %f</floatArray>\n' % tuple(a))
    lines.append('      <floatArray convention="PMP" title="b">')
    lines.append('%f %f %f</floatArray>\n' % tuple(b))
    lines.append('      <floatArray convention="PMP" title="c">')
    lines.append('%f %f %f</floatArray>\n' % tuple(c))
    lines.append('    </crystal>\n')
    return lines

def crystal_v2(lattice):
    lines = []
    lines.append("    <crystal>\n")
    la,lb,lc = lattice
    a,b,c,alpha,beta,gamma = matrix2abcabg((la,lb,lc))
    lines.append('      <scalar title="a">%f</scalar>\n' % a)
    lines.append('      <scalar title="b">%f</scalar>\n' % b)
    lines.append('      <scalar title="c">%f</scalar>\n' % c)
    lines.append('      <scalar title="alpha">%f</scalar>\n' % alpha)
    lines.append('      <scalar title="beta">%f</scalar>\n' % beta)
    lines.append('      <scalar title="gamma">%f</scalar>\n' % gamma)
    lines.append('    </crystal>\n')
    return lines

def molecule(geo,id=0):
    lines = []
    lines.append(" <molecule id=\"FRAME%d\">\n" % id )
    lines += atomArray(geo)
    lines.append(" </molecule>\n")
    return lines
    

def atomArray(geo):
    lines = ["  <atomArray>\n"]

    for i in range(len(geo)):
        atno,(x,y,z) = geo[i]
        lines.append(atom(atno,x,y,z,i+1))
    lines.append("  </atomArray>\n")
    return lines

def atom(atno,x,y,z,id=0):
    return '    <atom id="%s%d" elementType="%s" xyz3="%f %f %f"/>\n' %\
           (symbol[atno],id,symbol[atno],x,y,z)


    
