#!/usr/bin/python
"""\
Convert an XYZ file to a XTL file.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import string,sys


def cleansym(s):
    """This function strips off the garbage (everything after and including
       the first non-letter) in an element name."""
    import re 
    return re.split('[^a-zA-Z]',s)[0]

def write_xtl(uc,atoms,xtl_name):
    xtl_file = open(xtl_name,'w')
    xtl_file.write("XTLGRF 200\n")
    if uc:
        xtl_file.write("PERIOD 111\n")
        xtl_file.write("AXES ZYX\n")
        xtl_file.write("SGNAME P 1\n")
        xtl_file.write("CRYSTX  %10.5f %10.5f %10.5f %10.5f %10.5f %10.5f\n"
                       % tuple(uc))
    xtl_file.write("FORMAT ATOM   (a6,1x,i5,1x,a5,1x,a3,1x,a1,")
    xtl_file.write("1x,a5,3f10.5,1x,a5, i3,i2,1x,f8.5)\n")
    i = 0
    for atom in atoms:
        i = i+1
        sym,x,y,z = atom
        ff_type = sym
        q1 = q2 = 0
        chg = 0.
        xtl_file.write("%6s %5d %-5s %3s %1s %4s %10.5f%10.5f%10.5f " %
                   ("HETATM",i,sym,"RES","A","444",x,y,z))
        xtl_file.write("%-5s%3d%2d %8.5f\n" % (ff_type,q1,q2,chg))
    xtl_file.write("END\n")                   
    xtl_file.close()

def read_uxyz(xyz_name):
    'Takes the last unit cell and structure from an xyz file'
    xyz_file = open(xyz_name,'r')
    while 1:
        line = xyz_file.readline()
        if not line: break
        words = string.split(line)
        if not words: break
        nat = int(words[0])
        title = xyz_file.readline()
        if title[:4] == 'CELL':
            uc = map(float,string.split(title)[1:])
        else:
            uc = None
        atoms = []
        for i in range(nat):
            line = xyz_file.readline()
            words = string.split(line)
            sym = words[0]
            sym = cleansym(sym)
            x,y,z = float(words[1]),float(words[2]),float(words[3])
            atoms.append((sym,x,y,z))

    xyz_file.close()
    return uc,atoms


def main(xyz_name):
    xtl_name = string.replace(xyz_name,'.xyz','.xtl')
    uc,atoms = read_uxyz(xyz_name)
    write_xtl(uc,atoms,xtl_name)
    return

if __name__ == '__main__':
    xyz_name = sys.argv[1]
    main(xyz_name)

