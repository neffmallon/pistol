#!/usr/bin/env python
"""\
 Utilities for reading/writing Socorro files

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

from Pistol.Element import sym2no,symbol,symlower
from Numeric import array

def guess_symbol(msym):
    if msym.lower() in symlower:
        return msym
    if len(msym) > 1 and msym[:2].lower() in symlower:
        return msym[:2]
    if len(msym) > 0 and msym[:1].lower() in symlower:
        return msym[:1]
    return 'Du' # punt: dummy atom

def write_crystal(title,lattice,geo,ascale=1):
    val = ["%s\n" % title,
           "%15.10f\n" % ascale,
           "%15.10f %15.10f %15.10f\n" % lattice[0],
           "%15.10f %15.10f %15.10f\n" % lattice[1],
           "%15.10f %15.10f %15.10f\n" % lattice[2],
           "lattice\n",
           " %d\n" % len(geo)]
    for sym,(x,y,z) in geo: # These must be in lattice coords for now
        val.append("%8s %15.10f %15.10f %15.10f\n" % (sym,x,y,z))
    return ''.join(val)

def read_crystal(fname):
    file = open(fname)
    title = file.readline().strip()
    ascale = float(file.readline().split()[0])
    ax,ay,az = map(float,file.readline().split())
    bx,by,bz = map(float,file.readline().split())
    cx,cy,cz = map(float,file.readline().split())
    type = file.readline().strip()
    if type != 'lattice': raise "Cartesian atoms not supported yet"
    nat = int(file.readline().split()[0])
    geo = []
    for i in range(nat):
        words = file.readline().split()
        sym = words[0]
        sym = guess_symbol(sym)
        atno = sym2no[sym]
        x,y,z = map(float,words[1:])
        geo.append((atno,(x,y,z)))
    file.close()

    lattice = array([[ax,ay,az],[bx,by,bz],[cx,cy,cz]])
    return lattice,geo,ascale

def scale_lattice(lattice,factor): return lattice*factor

def atoms2cart(lattice,geo):
    cart_atoms = []
    for sym,(x,y,z) in geo:
        pos = x*lattice[0]+y*lattice[1]+z*lattice[2]
        cart_atoms.append((sym,pos))
    return cart_atoms
    
