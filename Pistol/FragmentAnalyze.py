#!/usr/bin/env python
"""\
NAME
     FragmentAnalyze.py - Code to do fragment analysis.

USAGE
     analyze_pops.py <options> <trajectory file name>

OPTIONS
     -h       Print this help message
     -b #     Use # as the tolerance for bond cutoffs
              Default = 1.15, but should be 1.0 if use_vel=1
     -f #     Use only # frames from the trajectory
     -l a,b,c Use (a,b,c) as the lattice parameters.
              (Don't put any spaces between a,b,c!)
     -v       Use velocity information to determine clustering
              (not yet implemented)
     
     Python version by Richard P. Muller.
     Fortran version shock_ana_pops.f/calc_mols.f by Alejandro Strachan.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import sys
from Numeric import zeros,Float
from math import sqrt

#Data defined here is global
# Conversion from symbols to atomic numbers
sym2no = { 'H' : 1, 'O' : 8, 'N' : 7, 'C' : 6,
           'h' : 1, 'o' : 8, 'n' : 7, 'c' : 6} #or import from Elements.py

# index a species file based on the number of atoms of each element:
# taken from templates file. Of course, this will fail if we have two
# species that have the same elemental signature
species_signature = [
    (0,0,0,2), # O2
    (2,0,0,0), # H2
    (1,0,0,1), # OH
    (2,0,0,2), # HOOH
    (2,0,0,1), # H2O
    (0,0,0,1), # O
    (1,0,0,0), # H
    (1,0,0,2)  # HO2
    ]
species_names = ['O2','H2','OH','HOOH','H2O','O','H','HO2']

# Taken from RPM's Element.py module: incomplete.
mass = [
    0.00,
    1.0008, 4.0026,
    6.941,9.0122,
    10.811,12.011,14.007,15.999,18,998,20.179,
    22.990,24.305,
    26.982,28.086,30.974,32.066,35.453,39.948,
    39.098, 40.078,
    44.9559, 47.867, 50.9415, 51.9961, 54.938, 55.845,
    58.9332, 58.6934, 63.546,65.39,
    69.723, 72.61, 74.9216, 78.96, 79.904, 83.80,
    85.4678, 87.62,
    88.90686, 91.224, 92.90638, 95.94, 98, 101.07,
    102.90550, 106.42, 107.8682, 112.411,
    114.818, 118.710, 121.760, 127.60, 126.90447, 131.29]

def get_dist0(bondtol):
    # bond tolerance: should be 1.15 if distance only analysis, 1.0 if vel/dist 
    # covalent radii. Taken from one of Ale's cov_rad.dat files
    rcovalent = [ None, 0.6555/2, None, None, None, None,
                  1.3931/2, 1.2298/2, 1.1693/2]
    nel = len(rcovalent)

    dist0 = zeros((nel,nel),Float)
    for i in range(nel):
        for j in range(nel):
            if rcovalent[i] and rcovalent[j]:
                dist0[i,j] = rcovalent[i]+rcovalent[j]

    # explicit overwrites here
    dist0[1,8] = dist0[8,1] = 0.86 
    for i in range(nel):
        for j in range(nel):
            dist0[i,j] *= bondtol
    return dist0

def analyze_pops(trjname,use_vel=0,abc=(10.,10.,10.),max_frames=0):
    geos = read_vxyz(trjname)
    if not max_frames: max_frames = len(geos)
    if use_vel: raise "Velocity-based fragments are not implemented yet"

    frag_data = []
    for geo in geos[:max_frames]:
        pops = [0]*len(species_signature)
        frag_data.append(pops)

        frags = calc_frags_distance(geo,abc)

        for frag in frags:
            nH,nC,nN,nO = count_elements(frag)
            if (nH,nC,nN,nO) in species_signature:
                species_index = species_signature.index((nH,nC,nN,nO))
                pops[species_index] += 1

    datfile = open('popul.dat','w')
    datfile.write('# final populations vs time \n')
    datfile.write('# step ')
    for name in species_names:
        datfile.write('%s ' % name)
    datfile.write('\n')
    for i in range(len(frag_data)):
        datfile.write("%d " % i)
        for pop in frag_data[i]:
            datfile.write("%d " % pop)
        datfile.write("\n")
    datfile.close()
    return

def calc_frags_dist_ale(atoms,abc):
    # This is a more literal version of Ale's routine calc_mols.f routine.
    # I'm keeping it here for future reference.
    inew = 0
    icur = 0
    iclus = 0
    nat = len(atoms)
    list2 = [1]*nat
    limlist = [0]*nat
    atmlist = [-1]*nat
    for i1 in range(nat):
        if list2[i1] == 0: continue
        atmlist[inew] = i1
        inew += 1
        list2[i1] = 0 # remove from list
        while icur < len(atmlist) and atmlist[icur] != -1:
            for i2 in range(nat):
                if list2[i2] == 0: continue
                if is_bonded(atoms[atmlist[icur]],atoms[i2],abc):
                    atmlist[inew] = i2
                    list2[i2] = 0
                    inew += 1
            #end for
            icur += 1
        #end while
        limlist[iclus] = icur - 1
        iclus = iclus + 1
    iptr = 0
    frags = []
    for i in limlist:
        frag = []
        for j in range(iptr,i+1):
            frag.append(atoms[atmlist[j]])
        iptr = i+1
        frags.append(frag)
    return frags

def calc_frags_distance(geo,abc):
    frags = []
    while len(geo) > 0:
        atom = geo.pop(0)
        frag = [atom]
        frags.append(frag)
        iptr = 0
        while iptr < len(frag):
            atomi = frag[iptr]
            dellist = []
            for atomj in geo:
                if is_bonded(atomi,atomj,abc):
                    geo.remove(atomj)
                    frag.append(atomj)
            iptr += 1
    return frags

def is_bonded(atomi,atomj,do_vel=0):
    if do_vel: return is_bonded_vel(atomi,atomj)
    return is_bonded_dist(atomi,atomj)

def is_bonded_dist((atnoi,xyzi,vxyzi),(atnoj,xyzj,vxyzj),abc):
    return distance(xyzi,xyzj,abc) < dist0[atnoi,atnoj]

def is_bonded_vel((atnoi,xyzi,vxyzi),(atnoj,xyzj,vxyzj),abc):
    if not is_bonded((atnoi,xyzi,vxyzi),(atnoj,xyzj,vxyzj),abc): return 0
    # now we know that the atoms are close enough to possibly be bonded
    rij = distance(xyzi,xyzj,abc)
    rij0 = dist0[atnoi,atnoj]
    epot = get_morse_pot(atnoi,atnoj,rij,rij0)
    ekin = get_kinetic(atnoi,atnoj,vxyzi,vxyzj)
    return (epot+ekin < 0)

def get_kinetic(atnoi,atnoj,vxyzi,vxyzj):
    mi,mj = mass[atnoi], mass[atnoj]
    vxcm,vycm,vzcm = get_vcm(mi,mj,vxyzi,vxyzj)
    vxi,vyi,vzi = vxyzi
    vxj,vyj,vzj = vxyzj
    ekin = mi*(pow(vxi-vxcm,2) + pow(vyi-vycm,2) + pow(vzi-vzcm,2)) +\
           mj*(pow(vxj-vxcm,2) + pow(vyj-vycm,2) + pow(vzj-vzcm,2))
    ekin = 0.5*ekin/1000# J/mol
    ekin = ekin/1000    # kJ/mol
    ekin = ekin*0.23885 # kcal/mol
    return ekin

def get_morse_pot(atnoi,atnoj,rij,rij0,eps=50.0,ga=25.0):
    rij = max(rij,rij0)
    return eps*(exp(-ga*(rij-rij0)/rij0) - 2*exp(-ga*(rij-rij0)/(2*rij0)))

def distance((xi,yi,zi),(xj,yj,zj),abc):
    dx = adjust_limits(xi-xj,abc[0])
    dy = adjust_limits(yi-yj,abc[1])
    dz = adjust_limits(zi-zj,abc[2])
    return sqrt(dx*dx+dy*dy+dz*dz)

def adjust_limits(d,a):
    if d > a/2.:
        d -= a
    elif d < -a/2.:
        d += a
    return d

def count_elements(fragment):
    nH,nC,nN,nO = 0,0,0,0
    for (atno,xyz,vxyz) in fragment:
        if atno == 1: nH += 1
        elif atno == 6: nC += 1
        elif atno == 7: nN += 1
        elif atno == 8: nO += 1
    return nH,nC,nN,nO

def read_vxyz(filename):
    geos = []
    file = open(filename)
    while 1:
        line = file.readline()
        if not line: break
        nat = int(line.split()[0])
        title = file.readline()
        geo = []
        for i in range(nat):
            line = file.readline()
            words = line.split()
            x,y,z = map(float,words[1:4])
            atno = sym2no[words[0]]
            if 4 < len(words) < 7:
                vx,vy,vz = map(float,words[5:8])
            else:
                vx,vy,vz = (0,0,0)
            geo.append((atno,(x,y,z),(vx,vy,vz)))
        geos.append(geo)
    return geos

def test():
    atoms = [(1,(0,0,0),(0,0,0)),
             (1,(0,0,0.5),(0,0,0)),
             (1,(0,0,5.0),(0,0,0)),
             (1,(0,0,5.5),(0,0,0)),
             (1,(0,0,6.0),(0,0,0)),
             (1,(0,0,3.0),(0,0,0)),
             (1,(0,0,1.5),(0,0,0))]
    frags = calc_frags_distance(atoms,(10,10,10))
    for frag in frags:
        print "New Frag"
        for atom in frag:
            print atom
    return

if __name__ == '__main__':
    import getopt
    global dist0
    if len(sys.argv) < 2:
        print __doc__
        sys.exit()
    opts,args = getopt.getopt(sys.argv[1:],"b:f:hl:vtp")
    bondtol = 1.15
    use_vel = 0
    abc = (10,10,10)
    max_frames = 0
    doprofile = 0
    for (key,val) in opts:
        if key == '-h':
            print __doc__
            sys.exit()
        if key == '-b':
            bondtol = float(val)
        if key == '-f':
            max_frames = int(val)
        if key == '-l':
            abc = eval(val)
        if key == '-v':
            use_vel = 1
            raise "Velocity-based fragments are not implemented yet"
        # undocumented debugging options
        if key == '-t':
            test()
            sys.exit()
        if key == '-p':
            doprofile = 1

    if use_vel: bondtol=1.0 # change if we're using velocities
    
    dist0 = get_dist0(bondtol)
    filename= args[0]
    if doprofile:
        import profile,pstats
        profile.run('analyze_pops(filename,use_vel,abc,max_frames)',
                    'profile.dat')
        prof_dat = pstats.Stats('profile.dat')
        prof_dat.strip_dirs().sort_stats('time').print_stats(8)
    else:
        analyze_pops(filename,use_vel,abc,max_frames)

# For reference, here's the current profiling info
#   ncalls  tottime  cumtime  filename:lineno(function)
#  3450637  223.810  354.130  analyze_pops.py:163(distance)
#  3450637  133.840  487.970  analyze_pops.py:160(is_bonded)
# 10351911  130.320  130.320  analyze_pops.py:169(adjust_limits
#      600   64.410  552.380  analyze_pops.py:143(calc_frags_dis
