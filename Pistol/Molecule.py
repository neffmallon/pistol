#!/usr/bin/env python
"""\
 Molecule.py: Simple class for molecules.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

from Atom import Atom
from Constants import Ang2Bohr, Bohr2Ang

class Molecule:
    def __init__(self,name='molecule',atomlist=None,filename=None,
                 units='Bohr'):
        self.name = name
        self.atoms = []
        self.units = units
        if atomlist and filename:
            raise "Declare atomlist *or* filename, but not both"
        elif atomlist:
            self.add_atuples(atomlist)
        elif filename:
            self.add_xyz_file(filename)
        else:
            raise "Must declare either atomlist or filename"
        return

    def translate(self,pos):
        for atom in self.atoms: atom.translate(pos)
        return
    
    def add_atuple(self,atno,xyz):
        if self.units != 'Bohr': xyz = map(Ang2Bohr,xyz)
        self.atoms.append(Atom(atno,xyz[0],xyz[1],xyz[2]))

    def add_atuples(self,atoms):
        "Add a list of (atno,(x,y,z)) tuples to the atom list"
        for atno,xyz in atoms: self.add_atuple(atno,xyz)
        return

    def atuples(self):
        "Express molecule as a list of (atno,(x,y,z)) tuples"
        atoms = []
        for atom in self.atoms: atoms.append(atom.atuple())
        return atoms

    def atuples_angstrom(self):
        "Express molecule as a list of (atno,(x,y,z)) tuples, R in Angstroms"
        atoms = []
        for atom in self.atoms:
            atno,xyz = atom.atuple()
            xyz = map(Bohr2Ang,xyz)
            atoms.append((atno,xyz))
        return atoms

    def add_xyz_file(self,filename,which_frame=-1):
        "Input atoms from xyz file. By default choose the last frame"
        from IO import read_xyz
        geos = read_xyz(filename)
        self.add_atuples(geos[which_frame])
        return


    # These two overloads let the molecule act as a list of atoms
    def __getitem__(self,i): return self.atoms[i]
    def __len__(self): return len(self.atoms)


