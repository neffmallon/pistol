#!/usr/bin/env python
"""\
NAME
     analyze_pops3.py - Code to do population analysis.

USAGE

     import then run analyze_pops
     or
     analyze_pops3.py <options> <trajectory file name>

OPTIONS
     -h       Print this help message
     -b #     Use # as the tolerance for bond cutoffs
              Default = 1.15, but should be 1.0 if use_vel=1
     -f #     Use only # frames from the trajectory
     -l a,b,c Use (a,b,c) as the lattice parameters.
              (Don't put any spaces between a,b,c!)
     -v       Use velocity information to determine clustering
              (not yet implemented)
     
     Python version edited by Si-ping Han
     Python version by Richard P. Muller.
     Fortran version shock_ana_pops.f/calc_mols.f by Alejandro Strachan.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import sys
from numpy import *
from math import sqrt
import profile
import pstats
import copy

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

bonde = zeros((9,9),Float)
bonde[1,1]=166.5174
bonde[6,6]=150.2857
bonde[8,8]=104.6638
bonde[7,7]=148.3353
bonde[1,6]=167.9626
bonde[6,1]=167.9626
bonde[6,8]=172.2822
bonde[8,6]=172.2822
bonde[6,7]=169.4443
bonde[7,6]=169.4443
bonde[8,7]=150.1943
bonde[7,8]=150.1943
bonde[1,8]=191.7944
bonde[8,1]=191.7944
bonde[1,7]=212.4218
bonde[7,1]=212.4218

rcovalent = [ None, 0.6555/2, None, None, None, None,1.3931/2, 1.2298/2, 1.1693/2]

class pops_atom:
    'Class for storing atom info for population analysis.'
    def __init__(self,num,pos,vel):
        self.number=num
        self.position=array(pos)
        self.velocity=array(vel)
        self.bin=None
        return
    
class pops_bin:
    'Class for grouping atoms for population analysis.'
    def __init__(self,ijk):
        self.atoms=None
        self.ijk=ijk
        ## Stores pointers to the neighboring 26 bins
        self.neighbors=None
        if self.atoms is None:
            self.atoms = []
        if self.neighbors is None:
            self.neighbors = []
        return

    def ret_all_atoms(self):
        atoms=None
        atoms=copy.copy(self.atoms)
        for aneighbor in self.neighbors:
            atoms+=aneighbor.atoms
        return atoms

def add_atom(atm,bin):
    'Adds atom to neighborhood.'
    atm.bin=bin
    bin.atoms.append(atm)
    return

def setup_bins((na,nb,nc)):
    'Sets up the neiborhoods for storing atoms and returns them'
    ## Initialize the bins, tell the bins where it is located in the cell
    aa = []
    for i in range(na):
        bb = []
        for j in range(nb):
            cc = []
            for k in range(nc):
                cc.append(pops_bin(tuple([i,j,k])))
            bb.append(tuple(cc))
        aa.append(tuple(bb))

    ## Make them properly connected, each bin should be connected
    ## to its 26 nearest neighbors.  If bins are on the edges of the
    ## periodic cell, then they should be connected to the bins on the
    ## mirroring edge
    for bb in aa:
        for cc in bb:
            for bin in cc:
                for i in range(-1,2):
                    ii = bin.ijk[0]+i
                    if ii<0 : ii=na-1
                    elif ii==na : ii=0
                    for j in range(-1,2):
                        jj=bin.ijk[1]+j
                        if jj<0 : jj=nb-1
                        elif jj==nb : jj=0
                        for k in range(-1,2):
                            kk=bin.ijk[2]+k
                            if kk<0 : kk=nc-1
                            elif kk==nc : kk=0
                            if tuple([ii,jj,kk])!=bin.ijk:
                                bin.neighbors.append(aa[ii][jj][kk])                            
    return aa

def fill_bins(atoms,bins,xabc,abc):
    '''Put the atoms into the correct partitions.
        atoms = atoms to put in neighborhoods
        neighborhoods = 3 dimensional array of neighbhorhoods
        xabc = (xa,xb,xc); the intervals for each partition
        abc = dimensions of the periodic box'''
    ## Empty the bins
##    bincount=0
##    print bins
    for bb in bins:
        for cc in bb:
            for bin in cc:
                bin.atoms=[]
##                bincount+=1
##    print 'bincount',bincount
    

    ## Fill them in
    for anatom in atoms:
##        if atoms.count(anatom)>1:
##            print ' '
##            print 'Multiple copies of atom in geo.'
##            print 'atom',atom
##            print 'atoms.count(atom)',atoms.count(atom)
##            print ' '
        nn=3*[0]
        pos = copy.copy(anatom.position)
        for i in range(3):
            ## We have to be careful of atoms outside the periodic cell
            if pos[i]<0:
                pos[i]=abc[i]+pos[i]
            elif pos[i]>abc[i]:
                pos[i]=pos[i]-abc[i]
            nn[i]=int(pos[i]/xabc[i])
        nna,nnb,nnc=nn
        add_atom(anatom,bins[nna][nnb][nnc])
    return

def calculate_bin_dimensions(rcovalent,cutoff,(a,b,c)):
    '''Returns the values for the exact dimension of bins and the
    number of bins in each direction.'''
    ## Calculate a value for the approximate dimensions of a bin
    xpartition=(2*max(rcovalent)+cutoff)*1.

    ## Calculate how many bins are needed 
    na = int(a/xpartition)
    nb = int(b/xpartition)
    nc = int(c/xpartition)
    print na,nb,nc
    ## Calculate the exact dimensions of the bins
    xa = a/na
    xb = b/nb
    xc = c/nc
    print xa,xb,xc
    print xpartition

##    if na>=4 and nb>=4 and nc>=4: adj_dim=1
##    else: adj_dim=0
    adj_dim=1

    return (na,nb,nc),(xa,xb,xc),adj_dim

def prof_run(fun,file,n):
    '''Run function fun, put the stats into file and print
    out the stats for the n most time consuming operations.'''
    profile.run(fun,file)
    prof_dat = pstats.Stats(file)
    prof_dat.strip_dirs().sort_stats('time').print_stats(n)
    return

def get_dist0(bondtol):
    # bond tolerance: should be 1.15 if distance only analysis, 1.0 if vel/dist 
    # covalent radii. Taken from one of Ale's cov_rad.dat files
##    rcovalent = [ None, 0.6555/2, None, None, None, None,
##                  1.3931/2, 1.2298/2, 1.1693/2]
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

def analyze_pops(trjname,use_vel=1,abc=(10.,10.,10.),
                 max_frames=0,factor=0.300,ga=25.,
                 T=1000.,cutoffBO=3.0,ipot=2):

    ## Make a table of equilibrium bond distances
    if use_vel:
        dist0=get_dist0(1.0)
    else:
        dist0=get_dist0(1.15)

    ## Calculate the cutoff distance for bond oscillations.
    ## Under the harmonic oscillator approximation, a bond
    ## with order BO will have a maximum vibration given by
    ## SQRT(2*Kb*T/K) where Dreiding assumes that K = 700*BO
    cutoff = 0.00238201*sqrt(T/cutoffBO)
    print cutoff

    ## Read the trajectory file
    geos = read_vxyz(trjname)

    ## Setup the bins
    nabc,xabc,adj_dim=calculate_bin_dimensions(rcovalent,cutoff,abc)
    bins = setup_bins(nabc)

    ## Choose an optimal distance function
##    if adj_dim:
##        dist_func=distance_no_adj_dim
##    else:
##        dist_func=distance_adj_dim
    dist_func=distance_adj_dim

    ## Cycle over desired frames
    if not max_frames: max_frames = len(geos)
    frag_data = []
    unknown=0
    habc=tuple([abc[0]/2.,abc[1]/2.,abc[2]/2.])
    for geo in geos[:max_frames]:
        pops = [0]*len(species_signature)
        frag_data.append(pops)
        
        ## Fill up the bins
        fill_bins(geo,bins,xabc,abc)
        
        ## Calculate the fragments, note that now each atom has a pointer to a specific bin
        frags = calc_frags(use_vel,geo,abc,habc,ga,cutoff,ipot,dist0,factor,dist_func)

        ## Count the fragments, if the fragment isn't in the
        ## species signature, add it to the unknown fragments count
        for frag in frags:
            nH,nC,nN,nO = count_elements(frag)
            if (nH,nC,nN,nO) in species_signature:
                species_index = species_signature.index((nH,nC,nN,nO))
                pops[species_index] += 1
            else:
                unknown+=1
                
    ## Print out the average number of unknowns per frame
    unknown = float(unknown)/float(max_frames)
    print unknown
    
    ## Write out the count
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

def calc_frags(use_vel,geo,abc,habc,ga,cutoff,ipot,dist0,factor,dist_func):
    '''Calculates whether atoms are in a fragment and returns
    a list of lists representing fragments.
        use_vel : boolean, use velocity analysis or not
        geo : ((atno,(x,y,z),(vx,vy,vz)),...)
        abc : dimensions of the periodic box
        ga  : morse parameter
        cutoff : cutoff distance added on to the equilibrium bond distance
        ipot : 0=Real space, 1=LJ12-6, 2=Morse, Ale has optimized Morse
        dist0 : equilibrium bond distance, numeric 2 array
        factor : mulitiplicative factor used to determine potential energy, should be 0.3
        '''
    
    ## There are two different lists here
    ## frags is a list of fragments
    ## frag is the individual fragment under consideration
    frags = []
    while len(geo) > 0:

        ## Pop off an atom to start up a fragment
        atom = geo.pop(0)
        atom.bin.atoms.remove(atom)
##        print 'atom in atom.bin.atoms',atom in atom.bin.atoms
##        for neighbor in atom.bin.neighbors:
##            if atom in neighbor.atoms:
##                print ' '
##                print 'Atom in more than one bin.'
##                print 'neighbor',neighbor
##                print 'neighbor==atom.bin',neighbor==atom.bin
##                print 'atom.position',atom.position
##                print 'atom.bin.ijk',atom.bin.ijk
##                print 'neighbor.ijk',neighbor.ijk
##                print 'len(atom.bin.neighbors)',len(atom.bin.neighbors)
##                print ' '
                
        frag = [atom]   
        frags.append(frag)

        ## Start from the first atom, go through all other atoms
        ## in the geometry to see if they are bonded to that atom
        ## using the "for atomj in geo" block.  If they are bonded
        ## move them from geo to the frag list.  After checking all
        ## atoms, go on to the next atom in the frag list.  Check
        ## until all atoms in the fragment have been check and no new
        ## atoms are added, at which point, the while condition will fail.        
        iptr = 0
        while iptr < len(frag):
            atomi = frag[iptr]
##            print 'atomi',atomi
            for atomj in atomi.bin.ret_all_atoms():
                if is_bonded(use_vel,atomi,atomj,abc,habc,ga,
                             cutoff,ipot,dist0,factor,dist_func):
##                    print 'atomj',atomj
                    geo.remove(atomj)
                    atomj.bin.atoms.remove(atomj)
                    frag.append(atomj)
            iptr += 1
    return frags

def is_bonded(use_vel,atomi,atomj,abc,habc,ga,cutoff,ipot,dist0,factor,dist_func):
    atomii = (atomi.number,atomi.position,atomi.velocity)
    atomjj = (atomj.number,atomj.position,atomj.velocity)
    if use_vel: return is_bonded_vel(atomii,atomjj,abc,habc,ga,
                                     cutoff,ipot,dist0,factor,dist_func)
    return is_bonded_dist(atomii,atomjj,abc,habc,dist0,dist_func)

def is_bonded_dist((atnoi,xyzi,vxyzi),(atnoj,xyzj,vxyzj),abc,habc,dist0,dist_func):
    'Returns 1 if bonded, 0 if not.'
    return dist_func(xyzi,xyzj,abc) < dist0[atnoi,atnoj]

def is_bonded_vel((atnoi,xyzi,vxyzi),(atnoj,xyzj,vxyzj),
                  abc,habc,ga,cutoff,ipot,dist0,factor,dist_func):
    'Returns 1 if bonded, 0 if not.'
    # now we know that the atoms are close enough to possibly be bonded
    rij = dist_func(xyzi,xyzj,habc)
    rij0 = dist0[atnoi,atnoj]
    eps=factor*bonde[atnoi,atnoj]
    if rij<cutoff+rij0:
        if ipot==1:
            epot = get_lj_pot(rij,rij0,eps)
            ekin = get_kinetic(atnoi,atnoj,vxyzi,vxyzj)
        elif ipot==2:
            epot = get_morse_pot(rij,rij0,eps,ga)
            ekin = get_kinetic(atnoi,atnoj,vxyzi,vxyzj)
        return (epot+ekin < 0)
    else: return 0

def get_kinetic(atnoi,atnoj,vxyzi,vxyzj):
    'Returns the kinetic energy in kcals per mole.'
    mi,mj = mass[atnoi], mass[atnoj]
    vcm = get_vcm(mi,mj,vxyzi,vxyzj)
    vi = vxyzi - vcm
    vj = vxyzj - vcm    
    ekin = mi*dot(vi,vi) + mj*dot(vj,vj)
    ekin = 0.5*ekin/1000.00 # J/mol
    ekin = ekin/1000.00     # kJ/mol
    ekin = ekin*0.23885     # kcal/mol
    return ekin

def get_vcm(mi,mj,vxyzi,vxyzj):
    'Returns the center of mass velocity. vxyzi vxyzj need to be numeric arrays.'
    M = mi+mj
    vi = vxyzi
    vj = vxyzj
    return (mi*vi+mj*vj)/M

def get_morse_pot(rij,rij0,eps,ga):
    ##The morse potential does not accurately describe bonding at
    ##rij<rij0
    if rij<rij0:
        rij=rij0
    return eps*(exp(-ga*(rij-rij0)/rij0) - 2.0*exp(-ga*(rij-rij0)/(2.0*rij0)))

def get_generic_pot(rij,rij0):
    if rij<1.35*rij0:
        epot = -1000000.
    else:
        epot = 100
    return epot

def get_lj_pot(rij,rij0,eps=50.0):
    ##The LJ potential does not accurately describe bonding at
    ##rij<rij0
    if rij<rij0:
        rij=rij0
    rr = rij/rij0*0.8908987565
    return 4.0*eps*(rr**12-rr**6)    

def distance_adj_dim((xi,yi,zi),(xj,yj,zj),(ha,hb,hc)):
    'Returns the distance.'
    dx = adjust_limits(xi-xj,ha)
    dy = adjust_limits(yi-yj,hb)
    dz = adjust_limits(zi-zj,hc)
    return sqrt(dx*dx+dy*dy+dz*dz)

def distance_no_adj_dim((xi,yi,zi),(xj,yj,zj),(ha,hb,hc)):
    'Returns the distance.'
    dx = xi-xj
    dy = yi-yj
    dz = zi-zj
    return sqrt(dx*dx+dy*dy+dz*dz)

def adjust_limits(d,a):
    '''Adjusts distance caculates for the dimensions of
    the periodic cell.
        d = calculated distance in a particular dimension
        a = 1/2 length of the cell in that dimension'''
    if d > a:
        d -= a*2.
    elif d < -a:
        d += a*2.
    return d

def count_elements(fragment):
    'Counts the number of atoms in the fragment.'
    nH,nC,nN,nO = 0,0,0,0
    for atom in fragment:
        atno=atom.number
        if atno == 1: nH += 1
        elif atno == 6: nC += 1
        elif atno == 7: nN += 1
        elif atno == 8: nO += 1
    return nH,nC,nN,nO

def read_vxyz(filename):
    'Read the atoms.  Put them into a list of lists.'
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
            geo.append(pops_atom(atno,(x,y,z),(vx,vy,vz)))
        geos.append(geo)
    return geos

def test():
    atoms = [pops_atom(1,(0,0,0),(0,0,0)),
             pops_atom(1,(0,0,0.5),(0,0,0)),
             pops_atom(1,(0,0,5.0),(0,0,0)),
             pops_atom(1,(0,0,5.5),(0,0,0)),
             pops_atom(1,(0,0,6.0),(0,0,0)),
             pops_atom(1,(0,0,3.0),(0,0,0)),
             pops_atom(1,(0,0,1.5),(0,0,0))]
    frags = calc_frags_distance(atoms,(10,10,10))
    for frag in frags:
        print "New Frag"
        for atom in frag:
            print atom
    return

##if __name__ == '__main__':
##    import getopt
##    global dist0
##    if len(sys.argv) < 2:
##        print __doc__
##        sys.exit()
##    opts,args = getopt.getopt(sys.argv[1:],"b:f:hl:vtp")
##    bondtol = 1.15
##    use_vel = 0
##    abc = (10,10,10)
##    max_frames = 0
##    doprofile = 0
##    for (key,val) in opts:
##        if key == '-h':
##            print __doc__
##            sys.exit()
##        if key == '-b':
##            bondtol = float(val)
##        if key == '-f':
##            max_frames = int(val)
##        if key == '-l':
##            abc = eval(val)
##        if key == '-v':
##            use_vel = 1
##            raise "Velocity-based fragments are not implemented yet"
##        # undocumented debugging options
##        if key == '-t':
##            test()
##            sys.exit()
##        if key == '-p':
##            doprofile = 1
##
##    if use_vel: bondtol=1.0 # change if we're using velocities
##    
##    dist0 = get_dist0(bondtol)
##    filename= args[0]
##    if doprofile:
##        import profile,pstats
##        profile.run('analyze_pops(filename,use_vel,abc,max_frames)',
##                    'profile.dat')
##        prof_dat = pstats.Stats('profile.dat')
##        prof_dat.strip_dirs().sort_stats('time').print_stats(8)
##    else:
##        analyze_pops(filename,use_vel,abc,max_frames)

