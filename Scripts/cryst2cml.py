#!/usr/bin/env python
"""\
 cryst2cml.py - Convert a socorro crystal file to cml format.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import sys
from Pistol.Socorro import read_crystal,atoms2cart,scale_lattice
from Pistol.CML import write1
from Pistol.Constants import bohr2ang

def cryst2cml(fname):
    lattice,geo,ascale = read_crystal(fname)
    lattice = scale_lattice(lattice,bohr2ang*ascale)
    geo = atoms2cart(lattice,geo)
    write1(fname+'.cml',geo,lattice)
    return

if __name__ == '__main__':
    for fname in sys.argv[1:]: cryst2cml(fname)


