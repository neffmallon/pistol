#!/usr/bin/env python

"""\
 AlkaneBuilder.py - build unbranched alkanes
 
  Alkane builder takes a single argument (the number of units)
  and outputs an xyz file containing the coordinates of an alkane
  of that length
"""

# Parameters obtained by B3LYP/6-31G** calculations 
xh = 0.6
yh = 0.65
yh2 = 0.6
zh = 0.88
xc = 1.3
yc = 1.0

def C(atoms,x,y,z):
    atoms.append(('C',x,y,z))
    return atoms

def H(atoms,x,y,z):
    atoms.append(('H',x,y,z))
    return atoms

def methyl_start(atoms,x):
    atoms = C(atoms,x,0,0)
    atoms = H(atoms,x-xh,yh2,0)
    atoms = H(atoms,x,-yh,zh)
    atoms = H(atoms,x,-yh,-zh)
    return atoms

def methyl_end(atoms,x):
    atoms = C(atoms,x,yc,0)
    atoms = H(atoms,x+xh,yc-yh2,0)
    atoms = H(atoms,x,yc+yh,zh)
    atoms = H(atoms,x,yc+yh,-zh)
    return atoms

def ethyl(atoms,x):
    atoms = C(atoms,x,yc,0)
    atoms = H(atoms,x,yc+yh,zh)
    atoms = H(atoms,x,yc+yh,-zh)
    atoms = C(atoms,x+xc,0,0)
    atoms = H(atoms,x+xc,-yh,zh)
    atoms = H(atoms,x+xc,-yh,-zh)
    return atoms

def xyz_repr(atoms):
    str = '%d\n\n' % len(atoms)
    for atom in atoms:
        str = str + "%-3s %10.4f %10.4f %10.4f\n" % atom
    return str

# This program builds a long chain of alkanes

def alkanebuilder(nunits):
    root = 'alkane' + `nunits`
    outfile = root + '.xyz'

    x0 = 0

    atoms = []

    nc = 0
    nh = 0
    atoms = methyl_start(atoms,x0)
    nc += 1
    nh += 3
    x0 = x0 + xc
    for i in range(nunits):
        atoms = ethyl(atoms,x0)
        x0 = x0 + 2*xc
        nc +=2
        nh +=4

    atoms = methyl_end(atoms,x0)
    nc += 1
    nh += 3

    return atoms

if __name__ == '__main__':
    print alkanebuilder(3)

