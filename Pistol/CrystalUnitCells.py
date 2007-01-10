#!/usr/bin/env python
"""\
NAME
    CrystalUnitCells.py - Module for forming and manipulating unit cells

DESCRIPTION
    Get atom lists corresponding to simple unit cells.

    This is *not* the correct way to write this module. The right way
    would be to keep the lattice and the basis separate, and to be able
    to multiply the two together. I have written this module in a much
    simpler fashion so that it could be implemented easily.

    This module also contains data for a few elements and AB type
    structures.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

# Changelog
#  7/2003      Original version
#  10/17/2003  Modified atom positions to be in fractional coordinates

import math
from Element import mass

rt3 = math.sqrt(3)

# These should all be replaced by Numpy routines
def norm(vec): return math.sqrt(dot(vec,vec))
def dot(vec1,vec2): return vec1[0]*vec2[0]+vec1[1]*vec2[1]+vec1[2]*vec2[2]
def cross(vec1,vec2):
    return (vec1[1]*vec2[2]-vec1[2]*vec2[1],
            vec1[2]*vec2[0]-vec1[0]*vec2[2],
            vec1[0]*vec2[1]-vec1[1]*vec2[0])

class UC: # primitive class for unit cells
    def scale(self,factor):
        for i in range(len(self.atoms)):
            atno,(x,y,z) = self.atoms[i]
            self.atoms[i] = atno,(x*factor,y*factor,z*factor)
        for i in range(3):
            a,b,c = self.uc_vecs[i]
            self.uc_vecs[i] = a*factor,b*factor,c*factor
        return

    def density(self): return self.mass()/self.volume() # wierd units, perhaps

    def mass(self):
        ucmass = 0
        for atno,xyz in self.atoms: ucmass += mass[atno]
        return ucmass

    def nat(self): return len(self.atoms)

    def cart_atoms(self):
        (ax,ay,az),(bx,by,bz),(cx,cy,cz) = self.uc_vecs
        atoms = []
        for i in range(self.nat()):
            atno,(fa,fb,fc) = self.frac_atom(i)
            x = fa*ax + fb*bx + fc*cx
            y = fa*ay + fb*by + fc*cy
            z = fa*az + fb*bz + fc*cz
            atoms.append((atno,(x,y,z)))
        return atoms

    def cart_atom(self,i):
        (ax,ay,az),(bx,by,bz),(cx,cy,cz) = self.uc_vecs
        atno,(fa,fb,fc) = self.frac_atom(i)
        x = fa*ax + fb*bx + fc*cx
        y = fa*ay + fb*by + fc*cy
        z = fa*az + fb*bz + fc*cz
        return atno,(x,y,z)

    def frac_atoms(self): return self.atoms
    def frac_atom(self,i): return self.atoms[i]
    
    def volume(self):
        a,b,c = self.uc_vecs
        return abs(dot(a,cross(b,c)))

    def abcabg(self):
        "Return UC in terms of A,B,C, alpha, beta, gamma"
        la,lb,lc = self.uc_vecs
        a,b,c = length(la),length(lb),length(lc)
        gamma = math.acos(dot(la,lb)/a/b)*180/math.pi
        beta =  math.acos(dot(la,lc)/a/c)*180/math.pi
        alpha = math.acos(dot(lb,lc)/b/c)*180/math.pi
        return a,b,c,alpha,beta,gamma

    def tocml(self,filename='cryst.cml'):
        "Output UC in CML"
        from CML import write1
        atoms = self.cart_atoms()
        write1(filename,atoms,self.uc_vecs)
        return

    def __str__(self):
        val = []
        for i in self.uc_vecs:
            val.append("%10.4f %10.4f %10.4f\n" % i)
        val.append("\n")
        for i in range(len(self.atoms)):
            atno,(x,y,z) = self.cart_atom(i)
            val.append("%5d %10.4f %10.4f %10.4f\n" % (atno,x,y,z))
        return "".join(val)

class SC(UC): # Ah
    def __init__(self,atno,a=1.0):
        self.atoms = [(atno,(0,0,0))]
        self.uc_vecs = [(a,0,0),(0,a,0),(0,0,a)]
        return

class FCC(UC): #A1
    def __init__(self,atno,a=1.0):
        self.atoms = [(atno,(0,0,0)),(atno,(0.5,0.5,0)),
                      (atno,(0.5,0,0.5)),(atno,(0,0.5,0.5))]
        self.uc_vecs = [(a,0,0),(0,a,0),(0,0,a)]
        return

class BCC(UC): #A2
    def __init__(self,atno,a=1.0):
        self.atoms = [(atno,(0,0,0)),(atno,(0.5,0.5,0.5))]
        self.uc_vecs = [(a,0,0),(0,a,0),(0,0,a)]
        return

class HCP(UC): #A3
    def __init__(self,atno,a=1.0,c_a=1.63):
        self.atoms = [(atno,(0,0,0)),(atno,(1./3.,1./3.,0.5))]
        self.uc_vecs = [(a,0,0),
                        (a/2,rt3*a/2,0),
                        (0,0,c_a*a)]
        return

class Diamond(UC): #A4
    def __init__(self,atno,a=1.0):
        self.atoms = [(atno,(0,0,0)),(atno,(0.5,0.5,0)),
                      (atno,(0.5,0,0.5)),(atno,(0,0.5,0.5)),
                      (atno,(0.25,0.25,0.25)),(atno,(0.75,0.75,0.25)),
                      (atno,(0.75,0.25,0.75)),(atno,(0.25,0.75,0.75))]
        self.uc_vecs = [(a,0,0),(0,a,0),(0,0,a)]
        return

class bTin(UC): # A5
    def __init__(self,atno,a=1.0,c_a=0.2727):
        self.atoms = [(atno,(-0.125,-0.375,0.25)),(atno,(0.125,0.375,-0.25))]
        self.uc_vec = [(a,0,0),(0,a,0),(0.5,0.5,c_a*a)]
        return

class Graphite(UC): #A9
    def __init__(self,atno,a=1.0,c_a=1.63):
        self.atoms=[(atno,(0,0,0)),
                    (atno,(0,0,0.5)),
                    (atno,(1./3.,2./3.,0)),
                    (atno,(2./3.,1./3.,0.5))]
        self.uc_vecs=[(a/2,-rt3*a/2.,0),
                      (a/2,rt3*a/2.,0),
                      (0,0,a*c_a)]
        return

class Hexagonal(UC): #Af
    def __init__(self,atno,a=1.,c_a=1.63):
        self.atoms = [(atno,(0,0,0))]
        self.uc_vecs = [(a/2,-rt3*a/2,0),
                        (a/2,rt3*a/2,0),
                        (0,0,c_a*a)]
        return

class NaCl(UC): #B1
    def __init__(self,atno1,atno2,a=1.0):
        self.uc_vecs = [(a,0,0),(0,a,0),(0,0,a)]
        self.atoms = [(atno1,(0,0,0)),(atno1,(0.5,0.5,0)),
                      (atno1,(0.5,0,0.5)),(atno1,(0,0.5,0.5)),
                      (atno2,(0.5,0.5,0.5)),(atno2,(0,0,0.5)),
                      (atno2,(0,0.5,0)),(atno2,(0.5,0,0))]
        return
    
class CsCl(UC): #B2
    def __init__(self,atno1,atno2,a=1.0):
        self.uc_vecs = [(a,0,0),(0,a,0),(0,0,a)]
        self.atoms = [(atno1,(0,0,0)),(atno2,(0.5,0.5,0.5))]
        return
    
class CubicZincBlende(UC): #B3, Sphaelerite
    def __init__(self,atno1,atno2,a=1.0):
        self.uc_vecs = [(a,0,0),(0,a,0),(0,0,a)]
        self.atoms = [(atno1,(0,0,0)),(atno1,(0.5,0.5,0)),
                      (atno1,(0.5,0,0.5)),(atno1,(0,0.5,0.5)),
                      (atno2,(0.25,0.25,0.25)),(atno2,(0.75,0.75,0.25)),
                      (atno2,(0.75,0.25,0.75)),(atno2,(0.25,0.75,0.75))]
        return

# This has not been sufficiently tested:
# class Supercell:
#     def __init__(self,primitive,vecs=(1,1,1)):
#         self.atoms = []
#         ax,ay,az = primitive.uc_vecs[0]
#         bx,by,bz = primitive.uc_vecs[1]
#         cx,cy,cz = primitive.uc_vecs[2]
#         for i in range(vecs[0]):
#             for j in range(vecs[1]):
#                 for k in range(vecs[2]):
#                     for atno,(x,y,z) in primitive.atoms:
#                         xnew = x + i*ax + j*bx + k*cx
#                         ynew = y + i*ay + j*by + k*cy
#                         znew = z + i*az + j*bz + k*cz
#                         self.atoms.append((atno,(xnew,ynew,znew)))
#         i,j,k = vecs
#         self.uc_vecs = [(i*ax,i*ay,i*az),(j*bx,j*by,j*bz),(k*cx,k*cy,k*cz)]
#         return

# Structures that have yet to be implemented:
class A15(UC): pass #A15 or Cr3Si
class HexagonalZincBlend(UC): pass #B4, Wurtzite
class CaF2(UC): pass #C1

# Define some simple elemental structures. Values from Kittel chap 1
# distances in Angstrom. To convert to bohr, use job.scale(1./0.529)
he = HCP(2,3.57,1.633)
li = BCC(3,3.491)
be = HCP(4,2.27,1.58)
c = Diamond(6,3.567)
ne = FCC(10,4.46)
na = BCC(11,4.225)
mg = HCP(12,3.21,1.623)
al = FCC(13,4.05)
si = Diamond(14,5.43)
ar = FCC(18,5.31)
k = BCC(19,5.225)
ca = FCC(20,5.58)
sc = HCP(21,3.31,1.592)
ti = HCP(22,2.95,1.586)
v = BCC(23,3.03)
cr = BCC(24,2.88)
fe = BCC(26,2.87)
co = HCP(27,2.51,1.62)
ni = FCC(28,3.52)
cu = FCC(29,3.61)
zn = HCP(30,2.66,1.86) # c/a looks large?
ge = Diamond(32,5.658)
kr = FCC(36,5.64)
rb = BCC(37,5.585)
sr = FCC(38,6.08)
y = HCP(39,3.65,1.57)
zr = HCP(40,3.23,1.59)
nb = BCC(41,3.30)
mo = BCC(42,3.15)
tc = HCP(43,2.74,1.606)
ru = HCP(44,2.71,1.579)
rh = FCC(45,3.80)
pd = FCC(46,3.89)
ag = FCC(47,4.09)
cd = HCP(48,2.98,1.886)
xe = FCC(54,6.13)
cs = BCC(55,6.045)
ba = BCC(56,5.02)
ce = FCC(58,5.16)
eu = BCC(63,4.58)
gd = HCP(64,3.63,1.592)
tb = HCP(65,3.60,1.583)
dy = HCP(66,3.59,1.574)
ho = HCP(67,3.58,1.570)
er = HCP(68,3.56,1.570)
tm = HCP(69,3.54,1.571)
yb = FCC(70,5.48)
lu = HCP(71,3.50,1.586)
hf = HCP(72,3.19,1.583)
ta = BCC(73,3.30)
w = BCC(74,3.16)
re = HCP(75,2.76,1.616)
os = HCP(76,2.74,1.577)
ir = FCC(77,3.84)
pt = FCC(78,3.92)
au = FCC(79,4.08)
tl = HCP(81,3.46,1.595)
pb = FCC(82,4.95)
po = SC(84,3.34)
ac = FCC(89,5.31)
th = FCC(90,5.08)

# simple AB structures, also from Kittel ch 1
lih = NaCl(3,1,4.08)
mgo = NaCl(12,8,4.20)
mno = NaCl(25,8,4.43)
nacl = NaCl(11,17,5.63)
agbr = NaCl(47,35,5.77)
pbs = NaCl(82,16,5.92)
kcl = NaCl(19,17,6.29)
kbr = NaCl(19,35,6.59)

becu = CsCl(4,29,2.70)
alni = CsCl(13,28,2.88)
cuzn = CsCl(29,30,2.94) # beta brass
cupd = CsCl(29,46,2.99)
agmg = CsCl(47,12,3.28)
lihg = CsCl(3,80,3.29)
tlbr = CsCl(81,35,3.97)
cscl = CsCl(55,17,4.11)
tli = CsCl(81,53,4.20)

cuf = CubicZincBlende(29,9,4.26)
sic = CubicZincBlende(14,6,4.35)
cucl = CubicZincBlende(29,17,5.41)
zns = CubicZincBlende(30,16,5.41)
alp = CubicZincBlende(13,16,5.45)
gap = CubicZincBlende(31,15,5.45)
znse = CubicZincBlende(30,34,5.65)
gaas = CubicZincBlende(31,33,5.65)
alas = CubicZincBlende(13,33,5.66)
cds = CubicZincBlende(48,16,5.82)
insb = CubicZincBlende(49,51,6.46)
agi = CubicZincBlende(47,53,6.47)

if __name__ == '__main__':
    graphite = Graphite(6,2.45)
    graphite.tocml('bs.cml')
