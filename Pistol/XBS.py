#!/usr/bin/python
"""\
xbs.py Convert a number of file formats to the XBS format
and view the structure in the XBS program.

XBS is an x-based molecule viewer, much like xmol, but with
distributable source code. This is a python script to run
xbs for a variety of input types on the MSC machines.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

#Set 'xbsname' to be the command that executes the xbs program
xbsname = '/source/xbsa/bin/xbsa.iris'

import getopt,string,sys,os,re

def writebs(mol,file):
    atnolist = []
    for atom in mol:
        atno,x,y,z = atom
        file.write('atom    %s   %f  %f  %f\n' % (symbol[atno],x,y,z))
        if atno not in atnolist:
            atnolist.append(atno)
    file.write('\n')
    for atno in atnolist:
        file.write('spec   %s  %f   %f  %f %f \n' % \
                   (symbol[atno],rvdw[atno],
                    rint[atno],gint[atno],bint[atno]))
    file.write('\n')
    for i in range(len(atnolist)):
        for j in range(i+1):
            ati = atnolist[i]
            atj = atnolist[j]
            rcovij = 0.5*(rcov[ati]+rcov[atj])
            file.write('bonds  %s  %s  0.0  %f  0.109  0.50\n' % \
                       (symbol[ati],symbol[atj],rcovij))
    file.write('tmat 1.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 1.0\n')
    file.write('dist 12.00\n')
    file.write('inc  5.00\n') 
    file.write('scale 30.00\n') 
    file.write('rfac 1.00\n')
    file.write('bfac 1.00\n')
    file.write('pos 0.00 0.00\n')
    file.write('switches 1 0 1 0 0 1 1 2 0\n')
    return

def writemv(mol,file):
    file.write("frame\n")
    for atom in mol:
        atno,x,y,z = atom
        file.write("%f %f %f\n" % (x,y,z))
    return

def readxyz(filename,bsfilename,mvname):
    file = open(filename,'r')
    bsfile = open(bsfilename,'w')
    mvfile = open(mvname,'w')
    gotgeo = 0
    while 1:
        line = file.readline()
        if not line: break
        words = string.split(line)
        if len(words) < 1: break
        nat = int(words[0])
        line = file.readline()
        if not line: break
        mol = readonexyz(nat,file)
        if gotgeo == 0:
            writebs(mol,bsfile)
            gotgeo = 1
        else:
            writemv(mol,mvfile)
    bsfile.close()
    mvfile.close()
    file.close()
    
    return

def readonexyz(nat,file):
    mol = []
    for i in range(nat):
        line = file.readline()
        if not line: break
        words = string.split(line)
        sym = words[0]
        x = float(words[1])
        y = float(words[2])
        z = float(words[3])
        atno = sym2no[sym]
        mol.append((atno,x,y,z))
    return mol

def readjagin(filename,bsfilename,mvname):
    # only gets xyz coordinates for now; later
    # modify to get zmatrices
    # However, this can read multiple geometries in a file
    file = open(filename,'r')
    bsfile = open(bsfilename,'w')
    mvfile = open(mvname,'w')
    pattern = re.compile('zmat')
    gotgeo = 0
    while 1:
        line = file.readline()
        if not line:break
        if pattern.search(line):
            mol = readonejagin(file)
            if gotgeo == 0:
                writebs(mol,bsfile)
                gotgeo = 1
            else:
                writemv(mol,mvfile)
    bsfile.close()
    mvfile.close()
    file.close()
    return

def readonejagin(file):
    mol = []
    while 1:
        line = file.readline()
        if not line:break
        words = string.split(line)
        if len(words) < 4: break
        sym,x,y,z = string.split(line)
        sym = cleansym(sym)
        x = float(x)
        y = float(y)
        z = float(z)
        atno = sym2no[sym]
        mol.append((atno,x,y,z))
    return mol
            
def readjagout(filename,bsfilename,mvname):
    file = open(filename,'r')
    bsfile = open(bsfilename,'w')
    mvfile = open(mvname,'w')
    pattern = re.compile('[new|Input|Symmetrized] geometry')
    skippat1 = re.compile('Transition vector is product')
    gotgeo = 0
    while 1:
        line = file.readline()
        if not line: break
        if skippat1.search(line):
            continue
        if pattern.search(line):
            file.readline()
            file.readline()
            mol = readonejagout(file)
            if gotgeo == 0:
                writebs(mol,bsfile)
                gotgeo = 1
            else:
                writemv(mol,mvfile)
    file.close()
    bsfile.close()
    mvfile.close()
    return

def readonejagout(file):
    mol = []
    while 1:
        line = file.readline()
        if not line: break
        words = string.split(line)
        if len(words) < 4: break
        sym, x, y, z = words
        x = float(x)
        y = float(y)
        z = float(z)
        sym = cleansym(sym)
        atno = sym2no[sym]
        mol.append((atno,x,y,z))
    return mol

def readbgf(filename,bsfilename):
    # Doesn't handle crystals yet.
    file = open(filename,'r')
    bsfile = open(bsfilename,'w')
    mol = []
    pattern = re.compile('HETATM')
    for line in file.readlines():
        if pattern.search(line):
            words = string.split(line)
            sym = cleansym(words[2])
            atno = sym2no[sym]
            x = float(words[6])
            y = float(words[7])
            z = float(words[8])
            mol.append((atno,x,y,z))
    file.close()
    writebs(mol,bsfile)
    bsfile.close()
    return

def cleansym(sym):
    # This function strips off the garbage (everything after and including
    # the first non-letter) in an element name.
    import re
    pat = re.compile('[^a-zA-Z]')
    newsym = pat.split(sym)[0]
    return newsym

if len(sys.argv) < 2:
    help()

opts,args = getopt.getopt(sys.argv[1:],'h')

for opt in opts:
    key,value = opt
    if key == '-h': help()

#
#
# Data structures from Element.py
#
#

symbol = [
    'X',
    'H','He','Li','Be','B','C','N','O','F','Ne',
    'Na','Mg','Al','Si','P','S','Cl','Ar',
    'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe',
    'Co', 'Ni', 'Cu', 'Zn',
    'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr',
    'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru',
    'Rh', 'Pd', 'Ag', 'Cd',
    'In', 'Sn', 'Sb', 'Te', 'I', 'Xe',
    'Cs', 'Ba','La','Ce','Pr','Nd','Pm','Sm','Eu','Gd','Tb','Dy',
    'Ho','Er','Tm','Yb','Lu','Hf','Ta','W','Re','Os','Ir','Pt',
    'Au','Hg','Tl']

rint = [
    0.973,
    0.973, 0.944,
    0.698, 0.675, 0.000, 0.184, 0.000, 1.000, 0.933, 0.850,
    0.941, 0.133, 0.184, 0.933, 1.000, 0.678, 0.000, 0.005,
    0.941, 0.133, 0.184, 0.933, 1.000, 0.678, 0.000, 0.005,
    0.941, 0.133, 0.184, 0.933, 1.000, 0.678, 0.000, 0.005,
    0.941, 0.133, 0.184, 0.933, 1.000, 0.678, 0.000, 0.005,
    0.941, 0.133, 0.184, 0.933, 1.000, 0.678, 0.000, 0.005,
    0.941, 0.133, 0.184, 0.933, 1.000, 0.678, 0.000, 0.005,
    0.941, 0.133, 0.184, 0.933, 1.000, 0.678, 0.000, 0.005,
    0.941, 0.133, 0.184, 0.933, 1.000, 0.678, 0.000, 0.005,
    0.941, 0.133, 0.184, 0.933, 1.000, 0.678, 0.000, 0.005,
    0.941, 0.133, 0.184, 0.933, 1.000, 0.678, 0.000, 0.005
    ]

gint = [
    0.844,
    0.973, 0.900,
    0.133, 0.133, 0.392, 0.310, 0.000, 0.000, 0.910, 0.777,
    0.973, 0.545, 0.310, 0.910, 0.647, 1.000, 0.392, 0.500,
    0.973, 0.545, 0.310, 0.910, 0.647, 1.000, 0.392, 0.500,
    0.973, 0.545, 0.310, 0.910, 0.647, 1.000, 0.392, 0.500,
    0.973, 0.545, 0.310, 0.910, 0.647, 1.000, 0.392, 0.500,
    0.973, 0.545, 0.310, 0.910, 0.647, 1.000, 0.392, 0.500,
    0.973, 0.545, 0.310, 0.910, 0.647, 1.000, 0.392, 0.500,
    0.973, 0.545, 0.310, 0.910, 0.647, 1.000, 0.392, 0.500,
    0.973, 0.545, 0.310, 0.910, 0.647, 1.000, 0.392, 0.500,
    0.973, 0.545, 0.310, 0.910, 0.647, 1.000, 0.392, 0.500,
    0.973, 0.545, 0.310, 0.910, 0.647, 1.000, 0.392, 0.500,
    0.973, 0.545, 0.310, 0.910, 0.647, 1.000, 0.392, 0.500,
    0.973, 0.545, 0.310, 0.910, 0.647, 1.000, 0.392, 0.500
    ]

bint = [
    1.0,
    1.0, 1.0,
    0.000, 0.000, 0.000, 0.310, 1.000, 0.000, 0.667, 0.600,
    1.000, 0.133, 0.310, 0.310, 0.667, 0.000, 0.184, 0.200,
    1.000, 0.133, 0.310, 0.310, 0.667, 0.000, 0.184, 0.200,
    1.000, 0.133, 0.310, 0.310, 0.667, 0.000, 0.184, 0.200,
    1.000, 0.133, 0.310, 0.310, 0.667, 0.000, 0.184, 0.200,
    1.000, 0.133, 0.310, 0.310, 0.667, 0.000, 0.184, 0.200,
    1.000, 0.133, 0.310, 0.310, 0.667, 0.000, 0.184, 0.200,
    1.000, 0.133, 0.310, 0.310, 0.667, 0.000, 0.184, 0.200,
    1.000, 0.133, 0.310, 0.310, 0.667, 0.000, 0.184, 0.200,
    1.000, 0.133, 0.310, 0.310, 0.667, 0.000, 0.184, 0.200,
    1.000, 0.133, 0.310, 0.310, 0.667, 0.000, 0.184, 0.200,
    1.000, 0.133, 0.310, 0.310, 0.667, 0.000, 0.184, 0.200,
    1.000, 0.133, 0.310, 0.310, 0.667, 0.000, 0.184, 0.200,
    1.000, 0.133, 0.310, 0.310, 0.667, 0.000, 0.184, 0.200
    ]

rcov = [
    1.25,
    1.25, 1.25,
    1.86, 1.86, 1.86, 1.65, 1.50, 1.35, 1.40, 1.40,
    2.2, 2.2, 2.2, 2.2, 2.2, 2.2, 2.2, 2.2,
    2.2, 2.2, 2.2, 2.2, 2.2, 2.2, 2.2, 2.2,
    2.2, 2.2, 2.2, 2.2, 2.2, 2.2, 2.2, 2.2,
    2.2, 2.2, 2.2, 2.2, 2.2, 2.2, 2.2, 2.2,
    3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0,
    3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0,
    3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0,
    3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0,
    3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0,
    3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0,
    3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0,
    3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0,
    3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0,
    3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0,
    3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0
    ]

rvdw = [
    0.24,
    0.24, 0.24,
    0.93, 0.93, 0.62, 0.58, 0.56, 0.55, 0.54, 0.54,
    1.16, 1.02, 0.89, 0.87, 0.80, 0.77, 0.74, 0.74,
    1.16, 1.02, 0.89, 0.87, 0.80, 0.77, 0.74, 0.74,
    1.16, 1.02, 0.89, 0.87, 0.80, 0.77, 0.74, 0.74,
    1.16, 1.02, 0.89, 0.87, 0.80, 0.77, 0.74, 0.74,
    1.16, 1.02, 0.89, 0.87, 0.80, 0.77, 0.74, 0.74,
    1.16, 1.02, 0.89, 0.87, 0.80, 0.77, 0.74, 0.74,
    1.16, 1.02, 0.89, 0.87, 0.80, 0.77, 0.74, 0.74,
    1.16, 1.02, 0.89, 0.87, 0.80, 0.77, 0.74, 0.74,
    1.16, 1.02, 0.89, 0.87, 0.80, 0.77, 0.74, 0.74,
    1.16, 1.02, 0.89, 0.87, 0.80, 0.77, 0.74, 0.74,
    1.16, 1.02, 0.89, 0.87, 0.80, 0.77, 0.74, 0.74,
    1.16, 1.02, 0.89, 0.87, 0.80, 0.77, 0.74, 0.74
    ]

sym2no = {
    'X' : 0,
    'H'  : 1,
    'He' : 2,
    'Li' : 3,
    'Be' : 4,
    'B'  : 5,
    'C'  : 6,
    'N'  : 7,
    'O'  : 8,
    'F'  : 9,
    'Ne' : 10,
    'Na' : 11,
    'Mg' : 12,
    'Al' : 13,
    'Si' : 14,
    'P'  : 15,
    'S'  : 16,
    'Cl' : 17,
    'Ar' : 18,
    'K'  : 19,
    'Ca' : 20,
    'Sc' : 21,
    'Ti' : 22,
    'V'  : 23,
    'Cr' : 24,
    'Mn' : 25,
    'Fe' : 26,
    'Ga' : 31,
    'Ru' : 44,
    'Ag' : 47,
    'In' : 49,
    'Sn' : 50,
    'Sb' : 51,
    'Te' : 52,
    'I'  : 53,
    'Xe' : 54,
    'Cs' : 55,
    'Ba' : 56,
    'La' : 57,
    'Ce' : 58,
    'Pr' : 59,
    'Nd' : 60,
    'Pm' : 61,
    'Sm' : 62,
    'Eu' : 63,
    'Gd' : 64,
    'Tb' : 65,
    'Dy' : 66,
    'Ho' : 67,
    'Er' : 68,
    'Tm' : 69,
    'Yb' : 70,
    'Lu' : 71,
    'Hf' : 72,
    'Ta' : 73,
    'W'  : 74,
    'Re' : 75,
    'Os' : 76,
    'Ir' : 77,
    'Pt' : 78,
    'x' : 0,
    'h'  : 1,
    'he' : 2,
    'li' : 3,
    'be' : 4,
    'b'  : 5,
    'c'  : 6,
    'n'  : 7,
    'o'  : 8,
    'f'  : 9,
    'ne' : 10,
    'na' : 11,
    'mg' : 12,
    'al' : 13,
    'si' : 14,
    'p'  : 15,
    's'  : 16,
    'cl' : 17,
    'ar' : 18,
    'k'  : 19,
    'ca' : 20,
    'sc' : 21,
    'ti' : 22,
    'v'  : 23,
    'cr' : 24,
    'mn' : 25,
    'fe' : 26,
    'ga' : 31,
    'ru' : 44,
    'ag' : 47,
    'in' : 49,
    'sn' : 50,
    'sb' : 51,
    'te' : 52,
    'i'  : 53,
    'xe' : 54,
    'cs' : 55,
    'ba' : 56,
    'la' : 57,
    'ce' : 58,
    'pr' : 59,
    'nd' : 60,
    'pm' : 61,
    'sm' : 62,
    'eu' : 63,
    'gd' : 64,
    'tb' : 65,
    'dy' : 66,
    'ho' : 67,
    'er' : 68,
    'tm' : 69,
    'yb' : 70,
    'lu' : 71,
    'hf' : 72,
    'ta' : 73,
    'w'  : 74,
    're' : 75,
    'os' : 76,
    'ir' : 77,
    'pt' : 78}
    
filename = args[0] # Later modify to have support for multiple files

# divide the file name into a root and an extension:
words = string.split(filename,'.')
root = ''
for word in words[:-1]:
    root = root + word

ext = words[-1]
bsname = root + '.bs'
mvname = root + '.mv'
if ext == 'xyz' or ext == 'vxyz':
    readxyz(filename,bsname,mvname)
elif ext == 'in':  # Assuming that *.in implies jaguar input
    readjagin(filename,bsname,mvname)
elif ext == 'out': # Assuming that *.out implies jaguar output
    readjagout(filename,bsname,mvname)
elif ext == 'bgf':
    readbgf(filename,bsname)
elif ext == 'bs':
    pass
else:
    print 'Extension "%s" not recognized'
    sys.exit()

os.system('%s %s\n' % (xbsname,bsname))

