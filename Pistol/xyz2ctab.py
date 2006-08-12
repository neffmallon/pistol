#!/usr/bin/python
"""\
xyz2ctab Convert an xyz file to a MDL connection table

The molecule data format used here is a simple list of sym,x,y,z tuples

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import string,sys,math
from Pistol.Element import sym2no

bond_distance = [
    1.0, 1.20, 1.40,
    1.82, 1.3725, 0.795, 1.70, 1.55, 1.52, 1.47, 1.54,
    2.27, 2.3, 2.3, 2.30, 2.30, 2.30, 2.30, 1.88]

def distance(at1,at2):
    sym1,x1,y1,z1 = at1
    sym2,x2,y2,z2 = at2
    return math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2)+math.pow(z1-z2,2))

def cutoff_distance(at1,at2):
    sym1,x1,y1,z1 = at1
    sym2,x2,y2,z2 = at2
    an1 = sym2no[sym1]
    an2 = sym2no[sym2]
    return 0.6*(bond_distance[an1]+bond_distance[an2])

def get_bonds(mol):
    bonds = []
    nat = len(mol)
    for i in range(nat):
        for j in range(i):
            rij = distance(mol[i],mol[j])
            rij0 = cutoff_distance(mol[i],mol[j])
            if rij < rij0:
                # CTAB atom numbering starts from 1, not zero
                bonds.append((j+1,i+1))

    return bonds

def read_xyz_file(xyz_filename):
    mol = []
    file = open(xyz_filename,'r')
    lines = file.readlines()
    file.close()
    for line in lines[2:]:
        words = string.split(line)
        sym,x,y,z = words[0],float(words[1]),float(words[2]),float(words[3])
        mol.append((sym,x,y,z))
    return mol

def write_ctab_file(mol,ctab_filename):
    bonds = get_bonds(mol)
    nat = len(mol)
    nbonds = len(bonds)
    file = open(ctab_filename,'w')
    file.write('%i %i\n' % (nat,nbonds))
    for (sym,x,y,z) in mol:
        file.write('%10.4f %10.4f %10.4f %s\n' % (x,y,z,sym))
    for (iat,jat) in bonds:
        file.write('%i %i 1\n' % (iat,jat))
    file.close()
    return
    
def convert(xyz_filename):
    mol = read_xyz_file(xyz_filename)
    ctab_filename = string.replace(xyz_filename,'.xyz','.ctab')
    write_ctab_file(mol,ctab_filename)
    return


if __name__ == '__main__':
    xyz_filename = sys.argv[1]
    convert(xyz_filename)
