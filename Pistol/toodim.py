#!/usr/bin/env python
"""\
 tools for toy 2-dimensional simulations of atomic-ish systems
"""

from random import random
from numpy import array,Float,zeros

class Universe:
    def __init__(self,atoms=[]):
        self.atoms = atoms
        return

    def add_atom(self,atom): self.atoms.append(atom)
    def add_atoms(self,atoms): self.atoms.extend(atoms)
    def atomstrs(self): return "\n".join([atom.str() for atom in self.atoms])

    def dump(self,fname='uni.xyz'):
        file = open(fname,'w')
        for x,y in self.xylist():
            file.write("1  %10.4f %10.4f %10.4f\n" % (x,y,0))
        file.close()
        return

    def initvel(self):
        for atom in self.atoms: atom.initvel()
        return

    def xlist(self): return [atom.pos[0] for atom in self.atoms]
    def ylist(self): return [atom.pos[1] for atom in self.atoms]
    def xylist(self): return [atom.pos[:2] for atom in self.atoms]

class Atom:
    def __init__(self,pos):
        self.pos = pos
        # Morse-potential terms: E = D*[1-exp(a*(r-r0))]**2
        self.r0 = 1
        self.alpha = 1
        return
    
    def str(self): return "%10.4f %10.4f" % (self.pos[0],self.pos[1])
    def initvel(self,vmax=1):
        self.vel = array([(2*random()-1)*vmax,(2*random()-1)*vmax],Float)
        return


def main():
    nat = 20
    uni = Universe()
    size = 10

    # add atoms
    for i in range(nat):
        xy = array([size*random(),size*random()],Float)
        uni.add_atom(Atom(xy))

    uni.dump()
    uni.initvel()

if __name__ == '__main__': main()



