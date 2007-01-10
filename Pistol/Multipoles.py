#!/usr/bin/env python
"""\
NAME
    Multipoles.py - Functions for fitting and evaluating multipole potentials.

AUTHOR
    Richard P. Muller, email: rpm@wag.caltech.edu

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

from numpy import zeros,Float,dot
from math import sqrt

# Simple utilities
def distance(xyzi,xyzj): return sqrt(l2(xyzi-xyzj))
def l2(xyz): return dot(xyz,xyz)

# These are the basic multipole expansion functions:
def fit_charge(points):
    qtot = 0
    for qi,xyzi in points: qtot += qi
    return qtot

def fit_dipole(xyz,points):
    "Determine dipole moment around center xyzc"
    mu = zeros(3,Float)
    for qi, xyzi in points: mu += qi*(xyz-xyzi)
    return mu

def fit_quadrupole(xyz,points):
    "Determine quadrupole moment around xyzc"
    quad = zeros((3,3),Float)
    for qi,xyzi in points:
        dxyz = xyz-xyzi
        r2 = l2(dxyz)
        for i in range(3):
            for j in range(3):
                quad[i,j] += 3*qi*dxyz[i]*dxyz[j]/2
                if i==j: quad[i,j] -= qi*r2/2
    return quad

def fit_octapole(xyz,points):
    "Determine octapole moment around xyzc"
    octa = zeros((3,3,3),Float)
    for qi,xyzi in points:
        dxyz = xyz-xyzi
        r2 = l2(dxyz)
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    octa[i,j,k] = 5*qi*dxyz[i]*dxyz[j]*dxyz[k]/2
                    if j==k: octa[i,j,k] -= qi*dxyz[i]*r2/2
                    if i==k: octa[i,j,k] -= qi*dxyz[j]*r2/2
                    if i==j: octa[i,j,k] -= qi*dxyz[k]*r2/2
    return octa

def full_potential(xyz,points):
    "Compute the potential at ref due to charges at points"
    pot = 0
    for qi,xyzi in points: pot += charge_potential(xyz,qi,xyzi)
    return pot

def charge_potential(xyz,qi,xyzi):
    "Trivial, I realize, but included for completeness"
    return qi/distance(xyz,xyzi)

def dipole_potential(xyz,dipi,xyzi):
    "Compute the potential at ref due to a dipole at xyzc"
    dxyz = xyzi-xyz
    r2 = l2(dxyz)
    r = sqrt(r2)
    r3 = r2*r
    pot = 0
    for i in range(3):
        pot += dipi[i]*dxyz[i]/r3
    return pot

def quadrupole_potential(xyz,quadi,xyzi):
    "Compute the potential at ref due to a quadrupole at xyzc"
    dxyz = xyzi-xyz
    r2 = l2(dxyz)
    r = sqrt(r2)
    r5 = r2*r2*r
    pot = 0
    for i in range(3):
        for j in range(3):
            pot += quadi[i,j]*dxyz[i]*dxyz[j]/r5
    return pot

def octapole_potential(xyz,octi,xyzi):
    "Compute the potential at ref to to an octapole at xyzc"
    dxyz = xyzi-xyz
    r2 = l2(dxyz)
    r = sqrt(r2)
    r7 = pow(r,7)
    pot = 0
    for i in range(3):
        for j in range(3):
            for k in range(3):
                pot += octi[i,j,k]*dxyz[i]*dxyz[j]*dxyz[k]/r7
    return pot    

