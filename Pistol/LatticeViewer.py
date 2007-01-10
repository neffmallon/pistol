#!/usr/bin/env python
"""\
 Use the BallStickGtkGL module to view a lattice

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

doTranslate = True # Controls whether to translate to center of lattice

from numpy import array
from Pistol.BallStickGtkGL import BSWindow

def scale_lattice(lattice,factor): return lattice*factor

def atoms2cart(lattice,geo):
    cart_atoms = []
    for sym,(x,y,z) in geo:
        pos = x*lattice[0]+y*lattice[1]+z*lattice[2]
        cart_atoms.append((sym,pos))
    return cart_atoms

def LatticeViewer(lattice,atoms,isCartesian=True):
    if not isCartesian: atoms = atoms2cart(lattice,atoms)
    lx,ly,lz = lattice
    if doTranslate:
        cx,cy,cz = 0.5*(lx+ly+lz)
    else:
        cx,cy,cz = 0,0,0

    o = array([-cx,-cy,-cz])
    gray = (0.5,0.5,0.5)
    red = (1,0,0)
    lines = [
        (tuple(o),tuple(o+lx),gray),
        (tuple(o+lx),tuple(o+lx+ly),gray),
        (tuple(o+lx+ly),tuple(o+ly),gray),
        (tuple(o+ly),tuple(o),gray),
        (tuple(o+lz),tuple(o+lx+lz),gray),
        (tuple(o+lx+lz),tuple(o+lx+ly+lz),gray),
        (tuple(o+lx+ly+lz),tuple(o+ly+lz),gray),
        (tuple(o+ly+lz),tuple(o+lz),gray),
        (tuple(o),tuple(o+lz),gray),
        (tuple(o+lx),tuple(o+lx+lz),gray),
        (tuple(o+lx+ly),tuple(o+lx+ly+lz),gray),
        (tuple(o+ly),tuple(o+ly+lz),gray)]
    spheres = []
    for sym,pos in atoms:
        x,y,z = pos
        x,y,z = x-cx,y-cy,z-cz
        spheres.append(((x,y,z),0.3,red,20,20))
    cyls = []

    bs = BSWindow(spheres,cyls,lines)
    bs.run()
    return
    
