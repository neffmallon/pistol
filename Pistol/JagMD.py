#!/usr/bin/env python
"""\
 Molecular dynamics using Jaguar force calculations
"""

from math import sqrt,pow

# Things you may need to change
input_fname = 'jagmd.in'
output_fname = input_fname.replace('.in','.out')
jag_command = 'jaguar'

# Your input file should look something like this; the atoms go where
#  the %s character is...
jag_template = """\
&gen
igeopt=-1
basis=6-31G**
dftname=b3lyp
&
&zmat
%s
&
"""

# You will need to make sure this is correct:
# Derivation of units for Force constant: (Thanks to Alejandro Strachan)
# We have accel in hartrees/(bohr*g/mol) and we want it in A/ps^2
# hartree/(bohr*g/mol) * 1 bohr/0.52918 A * 627.51 kcal/mol/hartree
#   = 1185.8 kcal/mol/(A*g/mol) = 1185.8 kcal/(A*g) = 1.1858e6 kcal/(A*kg)
#   = 1.1858e6 kcal/(A*kg) * 4.184 J/cal = 4.9615e6 kJ/(A*kg)
#   = 4.9615e9 kg m^2/s^2/(A*kg) = 4.9615e9 m^2/(s^2*A)
#   = 4.9615e29 A/s^2 * s^2/(1e24 ps^2) = 4.9615e5 A/ps^2
fconst = 4.9615e5 # convert hartree/(bohr*g/mol) to A/ps^2

# Jaguar specific stuff:
def write_jagin(filename,atoms):
    atomstr = []
    for (sym,(x,y,z)) in atoms:
        atomstr.append('%s %20.14f %20.14f %20.14f\n' % (sym,x,y,z))
    atomstr = ''.join(atomstr) # Make one string out of the items
    open(filename,'w').write(jag_template % atomstr)
    return

def read_output(filename):
    energy = None
    forces = []
    epat = re.compile('SCFE: SCF energy:')
    fpat = re.compile('forces (hartrees')
    endpat = re.compile('-------')

    file = open(filename)
    while 1:
        line = file.readline()
        if not line: break
        if epat.search(line):
            words = line.split()
            energy = float(words[4])
        elif fpat.search(line):
            forces = []
            for i in range(3): line = file.readline() # skip blank lines
            while 1:
                line = file.readline()
                if not line: break
                if endpat.search(line): break
                words = line.split()
                fxyz = map(float,words[2:5])
                forces.append(fxyz)
    file.close()
    return energy,forces

def JagEF(atoms):
    write_jagin(input_fname,atoms)
    os.system('%s %s' % (jag_command, input_fname))
    return read_output(output_fname)

# End of Jaguar specific stuff

def Dynamics(atoms,EnergyForces,nsteps=1000,Ti=298,dt=1e-3):
    xyz = open('pyqmd.xyz','w')
    dat = open('pyqmd.dat','w')
    set_boltzmann_velocities(atoms,Ti)
    Etot = 0
    for step in range(nsteps):
        append_xyz(xyz,atoms.atuples(),"PQMD %4d  E = %10.4f" % (step,Etot))
        try:
            Ev,F = EnergyForces(atoms)
        except:
            print "Using averaging to try and converge"
            Ev,F = EnergyForces(atoms,0.5)
        set_forces(atoms,F)
        LeapFrogUpdate(atoms,dt)
        #for atom in atoms: flask.bounce(atom)
        Ek = get_kinetic(atoms)
        T = get_temperature(atoms)
        #rescale_velocities(atoms,Ti) # uncomment for iso-kinetics
        Etot = Ev+Ek
        print step*dt,Etot,Ev,Ek,T
        dat.write("%10.4f %10.4f %10.4f %10.4f %10.4f\n" %
                  (step*dt,Etot,Ev,Ek,T))
        dat.flush()
    return

def get_kinetic(atoms):
    sum_mv2 = 0
    for atom in atoms: sum_mv2 += atom.mass()*atom.v0.squared()
    return 0.5*sum_mv2/fconst

# There's a disconnect here, in that the kinetic energy is being
#  computed with v0 (v(t)) and the temperature is being computed
#  at v (v(t+dt/2))
def get_temperature(atoms):
    sum_mv2 = 0
    for atom in atoms: sum_mv2 += atom.mass()*atom.v.squared()
    return 1000*sum_mv2/((3*len(atoms)-6)*Rgas*fconst) 
    
def LeapFrogUpdate(atoms,dt):
    # Leap-frog Verlet dynamics is based on the equations
    #  v(t+dt/2) = v(t-dt/2)+dt*a(t)
    #  r(t+dt) = r(t) + dt*v(t+dt/2)
    # so that the positions, calculated at dt,2dt,3dt, etc.,
    # leap-frog over the velocities, calculated at dt/2,3dt/2,5dt/2...
    for atom in atoms:
        m = atom.mass()
        a = -atom.F*fconst/m        # a = F/m
        vnew = atom.v + dt*a        # v(t+dt/2) = v(t-dt/2) + dt*a
        # Save the current velocity for later calc of T,Ek
        atom.v0 = 0.5*(vnew+atom.v) # v(t) = 0.5*(v(t-dt/2)+v(t+dt/2)
        atom.r += dt*vnew           # r(t+dt) = r(t) + dt*v(t+dt/2)
        atom.v = vnew
    return

def set_forces(atoms,F):
    for i in range(len(atoms)):
        fx,fy,fz = F[i]
        atoms[i].F = Vec3(fx,fy,fz)
    return

def set_boltzmann_velocities(atoms,T):
    from random import gauss,randint
    Eavg = Rgas*T/2000 # kT/2 per degree of freedom (kJ/mol)

    vels = []
    for atom in atoms:
        m = atom.mass()
        vavg = sqrt(2*Eavg*fconst/m)
        
        stdev = 0.01 #I'm setting the std dev wrong here
        atom.v = Vec3(pow(-1,randint(0,1))*gauss(vavg,stdev),
                      pow(-1,randint(0,1))*gauss(vavg,stdev),
                      pow(-1,randint(0,1))*gauss(vavg,stdev))

    subtract_com_velocity(atoms)
    rescale_velocities(atoms,T)
    return

def subtract_com_velocity(atoms):
    vcom = get_vcom(atoms)
    for atom in atoms: atom.v -= vcom
    return

def rescale_velocities(atoms,T):
    Tact = get_temperature(atoms)
    scalef = sqrt(T/Tact)
    for atom in atoms: atom.v *= scalef
    return

def get_vcom(atoms):
    "Compute the Center of Mass Velocity"
    vcom = Vec3()
    totm = 0
    for atom in atoms:
        m = atom.mass()
        vcom += m*atom.v
        totm += m
    return vcom/totm

if __name__ == '__main__':
    from MINDO3 import get_energy_forces
    from Molecule import Molecule
    rdx = Molecule('RDX',filename='/home/rmuller/gallery/rdx.xyz')
    Dynamics(rdx,get_energy_forces,nsteps=3,Ti=4000)
