#!/usr/bin/python
"""\
xyz2jag.py Convert a simple xyz file to a basic jaguar input file

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import sys,string 

def xyz2jag(filename):
    atoms = read_xyz(filename)
    fileoutname = string.replace(filename,'.xyz','.in')
    write_jagin_file(fileoutname,atoms)
    return

def read_xyz(filename):
    "Reads the first geometry from an XYZ file"
    file = open(filename,'r')
    line = file.readline()
    nat = int(string.split(line)[0])
    line = file.readline()
    atoms = []
    for i in range(nat):
        line = file.readline()
        words = string.split(line)
        sym,x,y,z = words[0],float(words[1]),float(words[2]),\
                    float(words[3])
        atoms.append((sym,x,y,z))
    return atoms

def write_jagin_file(filename,atoms):
    file = open(filename,'w')
    # gen section
    file.write("&gen\n")
    file.write("idft=22111\n")
    file.write("basis=6-31G**\n")
    file.write("&\n")
    # zmat section
    file.write("&zmat\n")
    for atom in atoms:
        file.write("%s %15.10f %15.10f %15.10f\n" % atom)
    file.write("&\n")

if __name__ == '__main__':
    for filename in sys.argv[1:]:
        print "Converting %s" % filename
        xyz2jag(filename)

