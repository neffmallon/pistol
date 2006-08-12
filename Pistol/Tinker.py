#!/usr/bin/env python
"Utilities for the tinker program"

from math import pow,sqrt
from Pistol.Element import sym2no,radius,symbol

def read_tinker_xyzs(files):
    geos = []
    for file in files:
        geo = read_tinker_xyz(file)
        geos.append(geo)
    return geos

def read_tinker_xyz(fname):
    lines = open(fname).readlines()
    nat = int(lines[0].split()[0])
    geo = []
    for i in range(nat):
        line = lines[1+i]
        words = line.split()
        atno = sym2no[words[1]]
        x,y,z = map(float,words[2:5])
        geo.append((atno,(x,y,z)))
    return geo

def distance(at1,at2):
    atno1,(x1,y1,z1) = at1
    atno2,(x2,y2,z2) = at2
    return sqrt(pow(x1-x2,2)+pow(y1-y2,2)+pow(z1-z2,2))

def cutoff_distance(at1,at2):
    atno1,(x1,y1,z1) = at1
    atno2,(x2,y2,z2) = at2
    return 0.6*(radius[atno1]+radius[atno2])

def get_bonds(mol):
    bonds = []
    nat = len(mol)
    for i in range(nat):
        bondlist = []
        bonds.append(bondlist)
        for j in range(nat):
            if i==j: continue
            rij = distance(mol[i],mol[j])
            rij0 = cutoff_distance(mol[i],mol[j])
            if rij < rij0:
                # CTAB atom numbering starts from 1, not zero
                bondlist.append(j)
    return bonds

def write_tinker_xyz(mol,tinker_filename):
    bonds = get_bonds(mol)
    nat = len(mol)
    nbonds = len(bonds)
    file = open(tinker_filename,'w')
    file.write('%i %i\n' % (nat,nbonds))
    for i in range(len(mol)):
        atno,(x,y,z)  = mol[i]
        file.write('%4d %3s %10.4f %10.4f %10.4f ? '
                   % (i+1,symbol[atno],x,y,z))
        for j in bonds[i]: file.write(' %3d' % (j+1))
        file.write('\n')
    file.close()
    return
    
