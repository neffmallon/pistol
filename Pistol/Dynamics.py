#!/usr/bin/env python
"""\
 Dynamics.py - Molecular Dynamics

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import biggles
from math import sqrt
from numpy import array,zeros,Float,dot
#from SeqQuest import get_energy_forces

VERBOSE = 0

Rgas = 8.31441 # J/K/mol
ry_per_h = 2.0
kcal_per_h = 627.51
joule_per_cal = 4.184
angstrom_per_bohr = 0.52918

fconst = 1e-4*kcal_per_h*joule_per_cal/ry_per_h/pow(angstrom_per_bohr,2)
tconst = 1e-3*Rgas*ry_per_h/joule_per_cal/kcal_per_h

def Dynamics(atoms,neqsteps,nsteps,dt,T,
             EF,xyzfile=None):
    s = 0
    Ti = T
    time = 0
    ts = []
    Eks = []
    Evs = []
    Ets = []
    Ts = []
    nat = len(atoms)

    for step in range(neqsteps):
        Ev,F = EF(atoms.atuples())
        atoms,Ek = TscaleUpdate(atoms,F,dt,Ti)
        T = Ek2T(Ek,nat)
        Etot = Ev+Ek
        ts.append(time)
        Eks.append(Ek)
        Evs.append(Ev)
        Ets.append(Etot)
        Ts.append(T)
        time += dt
        
    for step in range(nsteps):
        Ev,F = EF(atoms.atuples()) # Harmonic update
        #atoms,Ek = LeapFrogUpdate(atoms,F,dt)
        #atoms,Ek = TscaleUpdate(atoms,F,dt,Ti)
        #atoms,Ek = DampedUpdate(atoms,F,dt,0.99)
        #atoms,Ek = BerendsenUpdate(atoms,F,dt,T,Ti,1.0)
        atoms,Ek,s = HooverUpdate(atoms,F,dt,T,Ti,s,0.1)
        T = Ek2T(Ek,nat)
        Etot = Ev+Ek
        ts.append(time)
        Eks.append(Ek)
        Evs.append(Ev)
        Ets.append(Etot)
        Ts.append(T)
        time += dt

    biggles_summary(ts,Evs,Ets,Eks,Ts)
    return

def biggles_summary(ts,Evs,Ets,Eks,Ts):
    #index = ts
    index = range(len(ts))
    p = biggles.FramedArray(2,1)
    v_t = biggles.Curve(index,Evs,color='red')
    v_t.label = 'Epot'
    E_t = biggles.Curve(index,Ets,color='blue')
    E_t.label = 'Etot'
    p[0,0].add(v_t)
    p[0,0].add(E_t)
    p[0,0].add(biggles.PlotKey(0.1,0.9,[v_t,E_t]))

    T_t = biggles.Curve(index,Ts,color='green')
    T_t.label = 'T'
    p[1,0].add(T_t)
    p[1,0].add(biggles.PlotKey(0.1,0.9,[T_t]))

    p.xlabel = 'Time'
    p.title = 'Energy and Temperature vs. time'

    p.show()
    p.write_img(400,400,"summary.png")
    return

class HarmForce:
    def __init__(self,atoms):
        self.atoms = []
        for atno,(x,y,z) in atoms: self.atoms.append((atno,(x,y,z)))
        return

    def __call__(self,atoms):
        V = 0
        forces = []
        k = 1. # probably a bad choice
        for i in range(len(atoms)):
            atno,(x0,y0,z0) = self.atoms[i]
            atno,(x,y,z) = atoms[i]
            forces.append((-k*(x-x0),-k*(y-y0),-k*(z-z0)))
            V += 0.5*k*(pow(x-x0,2)+pow(y-y0,2)+pow(z-z0,2))
        return V,forces

def squared(a): return dot(a,a)

def LeapFrogUpdate(atoms,Forces,dt):
    nat = len(atoms)
    Ek = 0
    for i in range(nat):
        atom = atoms[i]
        F = array(Forces[i])
        m = atom.mass()

        a = F*fconst/m        # a = F/m
        vnew = atom.v + dt*a  # v(t+dt/2) = v(t-dt/2) + dt*a
        #v0 = 0.5*(vnew+atom.v)# v(t) = 0.5*(v(t-dt/2)+v(t+dt/2)
        v0 = vnew + a*dt/2     # v(t+dt) = v(t+dt/2) + a*dt/2 (For Ekin only)
        atom.r += dt*vnew     # r(t+dt) = r(t) + dt*v(t+dt/2)
        atom.v = vnew
        Ek += 0.5*m*squared(v0)/fconst
    return atoms,Ek

def VelVerletUpdate(atoms,Forces,dt):
    nat = len(atoms)
    Ek = 0
    for i in range(nat):
        atom = atoms[i]
        F = array(Forces[i])
        m = atom.mass()

        # Half-advance the velocities
        a = F*fconst/m        # a = F/m
        atom.v += 0.5*dt*a
        Ek += 0.5*m*squared(atom.v)/fconst

        # In formal Velocity Verlet schemes, the following
        # two steps are actually computed at the beginning
        # of the iteration, before the force calculation. But
        # it shouldn't matter if we put them here:
        atom.r += dt*atom.v + 0.5*dt*dt*a
        # Half-advance the velocities
        atom.v += 0.5*dt*a
    return atoms,Ek

def TscaleUpdate(atoms,Forces,dt,Tgoal):
    atoms,Ek = LeapFrogUpdate(atoms,Forces,dt)
    T = Ek2T(Ek,len(atoms))
    rescale_velocities(atoms,Tgoal,T)
    return atoms,Ek

def DampedUpdate(atoms,Forces,dt,Damping):
    atoms,Ek = LeapFrogUpdate(atoms,Forces,dt)
    T = Ek2T(Ek,len(atoms))
    rescale_velocities(atoms,Damping*T,T)
    return atoms,Ek

def HooverUpdate(atoms,Forces,dt,T,Tgoal,s,xnu=10.):
    nat = len(atoms)
    Ek = 0
    s += xnu*(T-Tgoal)
    for i in range(nat):
        atom = atoms[i]
        F = array(Forces[i])
        m = atom.mass()

        a = F*fconst/m - s*atom.v
        vnew = atom.v + dt*a
        v0 = vnew + a*dt/2
        atom.r += dt*vnew 
        atom.v = vnew
        Ek += 0.5*m*squared(v0)/fconst
    return atoms,Ek,s

def HolianHooverUpdate(atoms,Forces,dt,T,Tgoal,s,xnu=10.):
    nat = len(atoms)
    Ek = 0
    s += dt*xnu*(T/Tgoal-1.)
    for i in range(nat):
        atom = atoms[i]
        F = array(Forces[i])
        m = atom.mass()

        a = F*fconst/m
        fact_num = 1. - 0.5*xnu*s*dt
        fact_denom = 1. + 0.5*xnu*s*dt
        vnew = (atom.v*fact_num + dt*a)/fact_denom
        # Save the current velocity for later calc of T,Ek
        v0 = 0.5*(vnew+atom.v)
        atom.r += dt*vnew     
        atom.v = vnew
        Ek += 0.5*m*squared(vnew)/fconst
        #Ek += 0.5*m*squared(v0)/fconst
    return atoms,Ek,s

def BerendsenUpdate(atoms,Forces,dt,T,Tgoal,tscale=1.0):
    nat = len(atoms)
    Ek = 0
    s = (Tgoal-T)/T/tscale
    for i in range(nat):
        atom = atoms[i]
        F = array(Forces[i])
        m = atom.mass()

        a = F*fconst/m + s*atom.v
        vnew = atom.v + dt*a  # v(t+dt/2) = v(t-dt/2) + dt*a
        # Save the current velocity for later calc of T,Ek
        v0 = 0.5*(vnew+atom.v)# v(t) = 0.5*(v(t-dt/2)+v(t+dt/2)
        atom.r += dt*vnew     # r(t+dt) = r(t) + dt*v(t+dt/2)
        atom.v = vnew
        Ek += 0.5*m*squared(v0)/fconst
    return atoms,Ek

def Ek2T(Ek,nat):
    return 2*Ek/(tconst*(3*nat-6))
    #return 2*Ek/(tconst*3*nat)

def set_boltzmann_velocities(atoms,T):
    from random import gauss,randint
    KE_per_mode = 0.5*T*tconst
    if VERBOSE: print " KE/mode = ",KE_per_mode

    vels = []
    for atom in atoms:
        m = atom.mass()
        
        vavg = sqrt(2*KE_per_mode*fconst/m)
        
        stdev = 0.1*vavg  #I'm setting the std dev wrong here

        atom.v = array([pow(-1,randint(0,1))*gauss(vavg,stdev),
                        pow(-1,randint(0,1))*gauss(vavg,stdev),
                        pow(-1,randint(0,1))*gauss(vavg,stdev)])

    if len(atoms) > 1: subtract_com_velocity(atoms)
    Ek = 0
    for atom in atoms: Ek += 0.5*atom.mass()*squared(atom.v)/fconst

    if len(atoms) == 1:
        # wierd case, since we probably want it to move
        nmodes = 3 
    elif len(atoms) == 2:
        nmodes = 1
    else: # gets the linear case wrong:
        nmodes = 3*len(atoms) - 6
    
    Tcurr = 2*Ek/tconst/nmodes

    rescale_velocities(atoms,T,Tcurr)

    if VERBOSE:
        print "Initializing Temperature. Goal = ",T
        print "                  Intermediate = ",Tcurr
    Ek = 0
    for atom in atoms: Ek += 0.5*atom.mass()*squared(atom.v)/fconst
    Tcurr = 2*Ek/(tconst*(3*len(atoms)-6))
    if VERBOSE:
        print "                         Final = ",Tcurr
    return

def subtract_com_velocity(atoms):
    vcom = get_vcom(atoms)
    for atom in atoms: atom.v -= vcom
    return

def rescale_velocities(atoms,Tdesired,Tact):
    scalef = sqrt(Tdesired/Tact) 
    for atom in atoms: atom.v *= scalef 
    return 

def get_vcom(atoms):
    "Compute the Center of Mass Velocity"
    vcom = zeros(3,Float)
    totm = 0
    for atom in atoms:
        m = atom.mass()
        vcom += m*atom.v
        totm += m
    return vcom/totm

if __name__ == '__main__':
    from Molecule import Molecule
    dmn = Molecule('DMN',
                   [(6,( 0.886026, 2.385603, 2.381127)),
                    (7,( 0.886026, 1.002738, 0.000000)),
                    (6,( 0.886026, 2.385603,-2.381127)),
                    (7,(-0.495094,-1.265835, 0.000000)),
                    (8,(-1.007426,-2.190039, 2.093021)),
                    (8,(-1.007426,-2.190039,-2.093021)),
                    (1,( 1.335454, 1.081991, 3.923211)),
                    (1,( 2.353665, 3.846988, 2.256411)),
                    (1,( 1.335454, 1.081991,-3.923211)),
                    (1,( 2.353665, 3.846988,-2.256411)),
                    (1,(-0.953450, 3.291993, 2.778406)),
                    (1,(-0.953450, 3.291993,-2.778406))])
    T = 20.
    set_boltzmann_velocities(dmn,T)
    EF = HarmForce(dmn.atuples())
    Dynamics(dmn,100,1000,0.1,T,EF)
