#!/usr/bin/python
"""\
Convert an XYZ file to a BGF file.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import string,sys
from Util import cleansym

def write_bgf(atoms,bgf_name):
    bgf_file = open(bgf_name,'w')
    bgf_file.write("BIOGRF 200\n")
    bgf_file.write("FORMAT ATOM   (a6,1x,i5,1x,a5,1x,a3,1x,a1,")
    bgf_file.write("1x,a5,3f10.5,1x,a5, i3,i2,1x,f8.5)\n")
    i = 0
    for atom in atoms:
        i = i+1
        sym,x,y,z = atom
        ff_type = sym
        q1 = q2 = 0
        chg = 0.
        bgf_file.write("%6s %5d %-5s %3s %1s %4s %10.5f%10.5f%10.5f " %
                   ("HETATM",i,sym,"RES","A","444",x,y,z))
        bgf_file.write("%-5s%3d%2d %8.5f\n" % (ff_type,q1,q2,chg))
    bgf_file.write("END\n")                   
    bgf_file.close()

def read_xyz(xyz_name):
    'Takes the last structure from an xyz file'
    xyz_file = open(xyz_name,'r')
    while 1:
        line = xyz_file.readline()
        if not line: break
        words = string.split(line)
        if not words: break
        nat = int(words[0])
        title = xyz_file.readline()
        atoms = []
        for i in range(nat):
            line = xyz_file.readline()
            words = string.split(line)
            sym = words[0]
            sym = cleansym(sym)
            x,y,z = float(words[1]),float(words[2]),float(words[3])
            atoms.append((sym,x,y,z))

    xyz_file.close()
    return atoms


def main(xyz_name):
    bgf_name = string.replace(xyz_name,'xyz','bgf')
    atoms = read_xyz(xyz_name)
    write_bgf(atoms,bgf_name)
    return



if __name__ == '__main__':
    xyz_name = sys.argv[1]
    main(xyz_name)

