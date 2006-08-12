#!/usr/bin/env python
"""\
NAME
     CTAB.py - Read/write CTAB formatted molecular structure files.

DESCRIPTION
     The CTAB.py module contains modules for reading and writing
     CTAB formatted molecular structure files.

FUNCTIONS
     atoms,bonds = read(filename):
          Read the atoms and bonds from filename
     write(filename,atoms,bonds):
          Write all of the atoms and bonds to filename

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

from Pistol.Element import symbol,sym2no

def read(filename):
    file = open(filename)
    atoms = []
    bonds = []
    line = file.readline()
    nat,nbonds = map(int,line.split())
    for i in range(nat):
        line = file.readline()
        words = line.split()
        x,y,z = map(float,words[:3])
        atno = sym2no[words[3]]
        atoms.append((atno,(x,y,z)))
    for i in range(nbonds):
        line = file.readline()
        i,j,order = map(int,line.split())
        bonds.append((i,j)) # ignore the bond order
    return atoms,bonds

def write(filename,atoms,bonds):
    file = open(filename,'w')
    file.write("%d %d\n" % (len(atoms),len(bonds)))
    for atno,(x,y,z) in atoms:
        file.write("%10.4f %10.4f %10.4f %4s\n" %
                   (x,y,z,symbol[atno]))
    for i,j in bonds:
        file.write("%d %d 1\n" % (i,j))
    file.close()
    return
        
