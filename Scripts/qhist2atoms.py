#!/usr/bin/env python
"""\
 Convert the atoms in a Quest .hist file to an atom list for an input file.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import sys
from Pistol.SeqQuest import read_hist
from Pistol.Util import toBohr3

def qhist2atoms(fname):
    results = read_hist(fname)
    types = results['types']
    atoms = results['geo']

    for i in range(len(atoms)):
        atno,xyz = atoms[i]
        x,y,z = toBohr3(xyz) #since hist uses Angstroms, convert to Bohr
        print "%5d %5d %15.9f %15.9f %15.9f" % (i+1,types[i],x,y,z)
    return

if __name__ == '__main__': qhist2atoms(sys.argv[1])
