#!/usr/bin/env python
"""\
NAME
     XYZ.py - Read/write XYZ formatted molecular structure files.

DESCRIPTION
     The XYZ.py module contains modules for reading and writing
     XYZ formatted molecular structure files.

FUNCTIONS
     geometries = read(filename):
          Read all of the geometries from filename
     write(filename,geometries):
          Write all of the geometries to filename
     append(file,geometry):
          Write one geometry to the already open file handle

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

from Util import cleansym
from Element import symbol,sym2no

def root(filename):
    filename.replace('.xyz','')
    filename.replace('.xmol','')
    return filename

def read(filename,do_center=0):
    "Read all the frames from an XYZ file. Optionally center each frame"
    file = open(filename)
    geometries = []
    while 1:
        line = file.readline()
        if not line: break
        try:
            nat = int(line.split()[0])
        except:
            break
        title = file.readline()
        atoms = []
        for i in range(nat):
            line = file.readline()
            words = line.split()
            atno = sym2no[cleansym(words[0])]
            x,y,z = map(float,words[1:4])
            atoms.append((atno,(x,y,z)))
        if do_center: atoms = center(atoms)
        geometries.append(atoms)
    return geometries

def write(filename,geometries,title="File written by XYZ.py"):
    "Write a sequence of frames to an XYZ file"
    file = open(filename,'w')
    for atoms in geometries: append(file,atoms,title)
    file.close()
    return

def append(file,atoms,title="File written by XYZ.py"):
    "Write a single geometry to an already open XYZ file handle"
    file.write("%d\n%s\n" % (len(atoms),title))
    for atno,(x,y,z) in atoms:
        file.write("%4s %10.4f %10.4f %10.4f\n"
                   % (symbol[atno],x,y,z))
    return

def center(atoms):
    "Translate molecule to center"
    xc,yc,zc = [0,0,0]
    for atno,(x,y,z) in atoms:
        xc,yc,zc = xc+x,yc+y,zc+z
    nat = float(len(atoms))
    xc,yc,zc = xc/nat,yc/nat,zc/nat

    for i in range(len(atoms)):
        atno,(x,y,z) = atoms[i]
        atoms[i] = atno,(x-xc,y-yc,z-zc)
    return atoms

# I could also put a transformation to inertial coordinates here.

        
