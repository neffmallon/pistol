#!/usr/bin/env python
"""\
 thermo.py Compute thermodynamic properties from frequencies
 Taken from the Jaguar program freq:thermo by Rick Muller

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

from math import sqrt,log,exp

from Pistol.Element import mass
from Pistol.Constants import Kboltz,hartree2kcal,hartree2joule,planck,Clight,bohr2ang

# Misc constants for calculation
Rgas = Kboltz*hartree2kcal*1000.0 # gas constant R = 1.98722 cal/mole/K
Satom = -2.31482    # atomic entropies = -2.31482
Slinear = -6.66401  # entropy correction constant for linear molecule
Snonlin = -7.70118  # entropy correct constant for nonlinear molecule
uterm = planck*Clight*100/(Kboltz*hartree2joule) # conversion fact: hc/k = 1.43877
eigmin = 10.0       #  minimum vibrational eigenvalue (in cm-1) allowed

def get_com(atoms):
    "compute center of mass"
    xcom,ycom,zcom = 0,0,0
    totmass = 0
    for atno,(x,y,z) in atoms:
        wgt = mass[atno]
        totmass += wgt
        xcom += wgt*x
        ycom += wgt*y
        zcom += wgt*z
    xcom = xcom/totmass
    ycom = ycom/totmass
    zcom = zcom/totmass
    return xcom,ycom,zcom
    
def get_inertia(atoms):
    "calculate moments of inertia"
    from numpy import zeros,Float
    from numpy.oldnumeric.linalg import Heigenvalues
    
    xcom,ycom,zcom = get_com(atoms)

    moment = zeros((3,3),Float) #MOI tensor
    totmass = 0
    for atno,(x,y,z) in atoms:
        wgt = mass[atno]
        totmass += wgt
        xc = x-xcom
        yc = y-ycom
        zc = z-zcom
        moment[0,0] += wgt*(yc*yc+zc*zc)
        moment[1,1] += wgt*(xc*xc+zc*zc)
        moment[2,2] += wgt*(xc*xc+yc*yc)
        moment[0,1] -= wgt*xc*yc
        moment[0,2] -= wgt*xc*zc
        moment[1,2] -= wgt*yc*zc
    moment[1,0] = moment[0,1]
    moment[2,0] = moment[0,2]
    moment[2,1] = moment[1,2]

    inertia = Heigenvalues(moment)
    inertia = tuple(inertia)
    print "Moments of inertia (units = amu*ang^2): %8.4f %8.4f %8.4f" %\
          inertia
    return totmass,inertia

def thermo(atoms,freqs,temps=[],pressure=1.0,is_linear=0,rotsymnum=1):
    # pressure in atm
    # rotsymnum  rotational sym number(co is 1,h2 is 2, ch4 is 12)

    totmass,inertia = get_inertia(atoms)
    
    if is_linear: #diatomic or linear polyatomic
        tpower=3.5
        cprt=tpower*Rgas
        #two moments are equal the other is zero
        ribar=(inertia[0]+inertia[1]+inertia[2])*0.5
        srt=Rgas*(1.5*log(totmass)+log(ribar/(rotsymnum*pressure)))+Slinear
    elif len(atoms) == 1: #atom
        tpower=2.5
        cprt=tpower*Rgas
        srt=Rgas*(1.5*log(totmass)-log(pressure))+Satom
    else: #nonlinear polyatomic
        tpower=4.0
        cprt=tpower*Rgas
        ribar=sqrt(inertia[0]*inertia[1]*inertia[2])
        srt=Rgas*(1.5*log(totmass)+log(ribar/(rotsymnum*pressure)))+Snonlin
        print Rgas,totmass,log(totmass)
        print ribar,log(ribar)
        print rotsymnum,pressure
        print Snonlin
    
    # compute zero point energy and count bad vibrations
    zeropt=0.0
    nbad = 0
    for freq in freqs:
        if freq > eigmin:
            zeropt+=freq
        else:
            nbad += 1
    # Convert to kcal/mol
    zeropt=zeropt*0.5*Clight*100.0*planck*hartree2kcal/hartree2joule 

    print "Thermochemical Properties "
    print " pressure: %14.4f atm" % pressure
    print " rotational symmetry number: %5d" % rotsymnum
    if nbad:
        print " vibrational frequencies below %6.1f cm-1 excluded: %5d" %\
              (eigmin,nbad)
    
    print "temp(K)   Cp (cal/mol K)   S (cal/mol K)",\
          "H (kcal/mol)   G(kcal/mol)"

    #write zero temperature results on first line
    
    print " %8.2f  %10.4f  %10.4f  %10.4f  %10.4f" % (0.0,cprt,srt,0.0,0.0)

    for temp in temps:
        if abs(temp) < 1.e-8: break
        cptot=cprt
        htot=cprt*temp
        stot=srt+Rgas*tpower*log(temp)

        #vibration terms
        #eigmin= minimum vibrational eigenvalue (in cm-1)
        for freq in freqs:
            # eig is in cm-1
            # eliminate small and negative vib modes
            u=uterm*freq/temp
            if freq < eigmin:
                exu=1.0
                ht=1.0
                # should include correction based on sound velocity
                stemp=0.0
            elif u < 88.0:
                # normal case
                exu=exp(u)
                ht=u/(exu-1.0)
                stemp=-Rgas*log(1.0-1.0/exu)
            else:
                # overflow regime for exu, no contribution to h,cp,or s
                continue
            rht=Rgas*ht
            htot=htot+temp*rht
            cptot=cptot+ht*rht*exu
            stot=stot+rht+stemp

        # convert h to kcal/mol
        htot=htot*1.0e-3
        gtot=htot-temp*stot*1.0e-3

        print " %8.2f  %10.4f  %10.4f  %10.4f  %10.4f" %\
              (temp,cptot,stot,htot,gtot)
    return

def test():
    # Run the test for ethane.
    # For this molecule Jaguar gives:
    # Thermochemical Properties:
    # pressure:        1.0000 atm
    # rotational symmetry number:    6
    # zero point energy:     48.574 kcal/mol
    # temp(K)   Cp (cal/mol K)   S (cal/mol K)   H (kcal/mol)   G (kcal/mol)
    #     .00           7.9489          7.1350          .0000          .0000
    #  298.15          11.5736         53.9289         2.6956       -13.3833
    #  398.15          14.4094         57.6586         3.9920       -18.9648
    #  498.15          17.3438         61.2056         5.5804       -24.9091
    #  598.15          20.0988         64.6264         7.4545       -31.2017
    #  698.15          22.5999         67.9252         9.5916       -37.8304

    # I get everything right except I don't compute the rotational
    #  symmetry number rotsymnum. I think that my masses are slightly
    #  off from what Jaguar uses as well.
    
    # Jaguar B3LYP/6-31G** minimized geometry:
    ethane = [ (6,(0.0000000000,      0.0000000000,      -.7650027938)),
               (6,(0.0000000000,      0.0000000000,       .7650027938)),
               (1,(1.0198329123,      0.0000000000,     -1.1639186579)),
               (1,(-.5099164561,      -.8832012096,     -1.1639186579)),
               (1,(-.5099164561,       .8832012096,     -1.1639186579)),
               (1,(-1.0198329123,      0.0000000000,      1.1639186579)),
               (1,( .5099164561,       .8832012096,      1.1639186579)),
               (1,( .5099164561,      -.8832012096,      1.1639186579))]
    # Jaguar frequencies:
    freqs = [391.69,921.26,940.71,940.71,1141.21,1141.21,1593.14,
             1625.35,1640.30,1640.30,1660.00,1660.00,3017.63,3127.53,
             3127.53,3134.57,3134.57,3140.39]

    temps = [298.15,398.15,498.15,598.15,698.15]
    
    thermo(ethane,freqs,temps,pressure=1.0,is_linear=0,rotsymnum=6)

if __name__ == '__main__': test()
