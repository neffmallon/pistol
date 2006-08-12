#!/usr/bin/env python
"""\
 qhist2cml.py - Get the coordinates from the history file and convert
   to CML file format. This is quite different from the hist2xyz file,
   because I wanted closer integration with Quest.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import sys,re
from Pistol.Element import sym2no,symbol
from Pistol.Util import cleansym
from Pistol.SeqQuest import read_hist

# To Do:
# Consider putting some of these routines into Pistol.CML

VERBOSE=1

def header():
    return ['<?xml version="1.0" ?>\n',
            ' <cml>\n']

def footer(): return [' </cml>\n']

def molecule(geo,lattice=None,id=0):
    lines = []
    lines.append(" <molecule id=\"FRAME%d\">\n" % id )
    if lattice: lines += crystal(lattice)
    lines += atomArray(geo)
    lines.append(" </molecule>\n")
    return lines

def crystal(lattice):
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

def atomArray(geo):
    lines = ["  <atomArray>\n"]

    for i in range(len(geo)):
        atno,(x,y,z) = geo[i]
        lines.append(atom(atno,x,y,z,i+1))
    lines.append("  </atomArray>\n")
    return lines

def atom(atno,x,y,z,id=0):
    # When I used xyz3 rather than x3, y3, z3, Jmol crashed
    return '    <atom id="%s%d" elementType="%s" x3="%f" y3="%f" z3="%f"/>\n' %\
           (symbol[atno],id,symbol[atno],x,y,z)


for filename in sys.argv[1:]:
    cmlname = filename.replace('hist','cml')
    results = read_hist(filename)
    # Get the last geo and cell by default; we can override
    #  with an input flag later.
    geo = results['geo'] 
    lattice = results.get('cell',None)
    lines = header() + molecule(geo,lattice) + footer()
    open(cmlname,'w').writelines(lines)

    
