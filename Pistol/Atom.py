#!/usr/bin/env python
"""\
 Atom.py: Simple class for atoms.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

# My goal is to keep everything generic,i.e. not specific to
#  MINDO, HF, DFT, etc.

from Element import mass
from Numeric import array

# Careful about units! I'm not doing anything about them here;
#  whatever you store you get back.

class Atom:
    def __init__(self,atno,x,y,z):
        self.atno = atno
        self.r = array([x,y,z])
        return

    def mass(self): return mass[self.atno]
    def pos(self): return self.r.tuple()
    def atuple(self): return (self.atno,self.r)
    def translate(self,pos): self.r += pos


