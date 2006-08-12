#!/usr/bin/python
"""\
 SeqQuest.py - Library for SeqQuest Runs

 Options:
 -h         Print this help message
 -a  <dir>  Use <dir> as the atom directory
 -c         Don't do a precleaning step before running
 -k         Keep: do not purge the scratch directory after the run
 -r         Randomize the tempdir name (useful if you plan on
            running > 1 quest jobs on a computer)
 -s         Setup only: copy files and links, but don't run
 -x  <exe>  Use <exe> as the seqquest executable
 -v         Verbose mode

 SeqQuest is Copyright (c) Peter A. Schultz

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

# Changelog
#
# 2005-02-28
#      - Updated to do a more intelligent search for atoms
#        (checks to see if the job is PBE or LDA)
#      - Fixed a few problems with missing import modules
#        (should be self-contained now).
#      - Wired all of the defaults to command-line flags

# Todo list:
# - Consider using options dictionaries as a replacement for the long
#   list of arguments in some functions
# - Use os.join to join directories and filenames

import sys,os,re,string,glob
from shutil import copyfile
from random import randint

#------You need to set these variables as appropriate for your system------

username = os.environ['USER']

questdir = '/home/%s/Programs/Quest' % username
default_tempdir = "/tmp/%s" % username
startdir = os.getcwd()

default_atomdir = questdir + '/atoms/library/atoms_default'
lda_atomdir = questdir + '/atoms/library/atoms_lda'
pbe_atomdir = questdir + '/atoms/library/atoms_pbe'
default_seqquestexe = questdir + '/seqquest/obj/lcao.x'

VERBOSE = 0
DO_PRECLEAN = 1
DO_KEEP = 0

# Set DO_RANDOM_TEMPDIR if you plan to run > 1 job per computer, in which
#  case it randomizes the tempdir names so that different jobs don't overwrite
#  each other.
DO_RANDOM_TEMPDIR = 0


#-----------You shouldn't have to change anything below this line------------


# Some general utility functions:
symbol = ['X', 'H', 'He','Li','Be','B', 'C', 'N', 'O', 'F',
          'Ne','Na','Mg','Al','Si','P', 'S', 'Cl','Ar','K',
          'Ca','Sc','Ti','V', 'Cr','Mn','Fe','Co','Ni','Cu',
          'Zn','Ga','Ge','As','Se','Br','Kr','Rb','Sr','Y',
          'Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In',
          'Sn','Sb','Te','I', 'Xe','Cs','Ba','La','Ce','Pr',
          'Nd','Pm','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm',
          'Yb','Lu','Hf','Ta','W', 'Re','Os','Ir','Pt','Au',
          'Hg','Tl','Pb','Bi','Po','At','Rn']

sym2no = {} 
for i in range(len(symbol)): 
    if symbol[i]: 
        sym2no[symbol[i]] = i 
        sym2no[symbol[i].lower()] = i

def cleansym(s):
    """This function strips off the garbage (everything after and including
       the first non-letter) in an element name."""
    import re 
    return re.split('[^a-zA-Z]',s)[0]


def get_energy(filename,geometry,uc,ndims,grid,
               kgrid=None,symops=None, functional='PBE'):
    write_input(filename,geometry,uc,ndims,grid,
                kgrid,symops, functional,force=False)
    results = seqquest(filename)
    return results['energy']

def get_forces(filename,geometry,uc,ndims,grid,
               kgrid=None,symops=None, functional='PBE'):
    write_input(filename,geometry,uc,ndims,grid,
                kgrid,symops, functional)
    results = seqquest(filename)
    return results['forces']

def get_energy_forces(filename,geometry,uc,ndims,grid,
               kgrid=None,symops=None, functional='PBE'):
    write_input(filename,geometry,uc,ndims,grid,
                kgrid,symops, functional)
    results = seqquest(filename)
    return results['energy'],results['forces']

def seqquest(filename,
             atomdir = None,
             seqquestexe=None,
             tempdir=None,
             keep=0,
             do_preclean = DO_PRECLEAN,
             do_random_tempdir = DO_RANDOM_TEMPDIR,
             verbose = VERBOSE):
    
    startdir,atomlist = setup(filename,seqquestexe,tempdir,
                              do_preclean,do_random_tempdir,verbose)
    results = run()
    if not keep: cleanup(atomlist,filename,startdir,verbose)
    return results

def setup(filename,
          atomdir = None,
          seqquestexe = None,
          tempdir=None,
          do_preclean = DO_PRECLEAN,
          do_random_tempdir = DO_RANDOM_TEMPDIR,
          verbose = VERBOSE):

    local_fname = 'lcao.in'

    # Set variables to default values if they're not specified:
    if not tempdir:
        tempdir = default_tempdir
        if do_random_tempdir:
            tempdir = "%s/quest_%d/" % (tempdir,randint(0,100000))
        else:
            tempdir = "%s/quest/" % tempdir
    if not os.path.exists(tempdir):
        try:
            os.mkdir(tempdir)
        except:
            print "Could not create temp directory: %s" % tempdir
            sys.exit()
    
    if not atomdir:
        if functional_is_pbe(filename):
            atomdir = pbe_atomdir
        else:
            atomdir = lda_atomdir

    if not seqquestexe: seqquestexe = default_seqquestexe

    if verbose:
        print "**Entering seqquest module**"
        print " filename =    ",filename
        print " seqquestexe = ",seqquestexe
        print " username =    ",username
        print " startdir =    ",startdir
        print " tempdir =     ",tempdir
        print " atomdir =     ",atomdir

    # Start doing real work:
    os.chdir(tempdir)
    if do_preclean: preclean(verbose)

    try_and_del(local_fname)
    copyfile(startdir + "/" + filename,local_fname)
    atomlist = get_atom_list(local_fname)

    for atom in atomlist:
        copyfile(atomdir + '/' + atom, atom)
    test_and_link(seqquestexe,'seqquest.e')
    return startdir,atomlist

def functional_is_pbe(fname):
    "Return True if the dft functional is pbe or pw91"
    file = open(fname).read()
    return ( ('PBE' in file) or ('pbe' in file) \
             or ('PW91' in file) or ('pw91' in file) )

def run():
    os.system('./seqquest.e > quest.out')
    results = read_output('quest.out')
    return results

def cleanup(atomlist,filename,startdir,verbose=VERBOSE):
    fileroot = string.join(string.split(filename,'.')[:-1],'.')

    dellist = atomlist + ['seqquest.exe'] + glob.glob('lcao*')
    copyfile('quest.out',"%s/%s.out" % (startdir,fileroot))
    copyfile('lcao.hist',"%s/%s.hist" % (startdir,fileroot))
    if verbose: print " Attempting to delete ",dellist
    for file in dellist:
        try_and_del(file)
    os.chdir(startdir)
    return

def preclean(verbose=VERBOSE):
    dellist = glob.glob('lcao*')
    if verbose: print " Attempting to delete ",dellist
    for file in dellist: try_and_del(file)
    return

def get_atom_list(filename):
    "Given a quest input file, return a list of atom files"
    atpat = re.compile('atom file')
    file = open(filename,'r')
    atlist = []
    while 1:
        line = file.readline()
        if not line: break
        if atpat.search(line):
            line = file.readline()
            atlist.append(line.strip())
    file.close()
    return atlist

def test_and_link(src,dest):
    if os.path.exists(dest): os.unlink(dest)
    os.symlink(src,dest)
    return

def try_and_del(filename):
    try: os.unlink(filename)
    except: pass
    return

def run_input(filenames,atomdir=default_atomdir,
              seqquestexe = default_seqquestexe):
    for filename in filenames: seqquest(filename,seqquestexe)

def get_atnos(geometry):
    atnos = []
    for atno,(x,y,z) in geometry:
        if atno not in atnos: atnos.append(atno)
    return atnos

def write_input(filename,geometry,uc,ndims,grid,
                kgrid=None,symops=None, functional='PBE',
                setup=True, iters=True, force=True,
                relax=False, cell=False, post=False,
                lattice_coords=False,
                econv=1e-4,gconv=0.04,
                pressure=0):
    instr = []

    if setup: instr.append('do setup\n')
    else: instr.append('no setup\n')

    if iters: instr.append('do iters\n')
    else: instr.append('no iters\n')
    
    if force: instr.append('do force\n')
    else: instr.append('no force\n')
    
    if relax: instr.append('do relax\n')
    else: instr.append('no relax\n')
    
    if cell: instr.append('do cell\n')
    else: instr.append('no cell\n')
    
    if post: instr.append('do post\n')
    else: instr.append('no post\n')
    
    instr.append('input data\n')
    instr.append('title\n')
    instr.append('%s quest input file\n' % filename)

    if functional:
        instr.append('functional\n')
        instr.append('%s\n' % functional)

    instr.append('lattice dimensionality (2=slab, 3=bulk)\n')
    instr.append(' %d\n' % ndims)
    if lattice_coords:
        instr.append('coordinates\n')
        instr.append('lattice\n')
    instr.append('primitive lattice vectors\n')
    instr.append('%15.12f %15.12f %15.12f\n' % tuple(uc[0]))
    instr.append('%15.12f %15.12f %15.12f\n' % tuple(uc[1]))
    instr.append('%15.12f %15.12f %15.12f\n' % tuple(uc[2]))
    instr.append('points along box sides\n')
    instr.append('%d %d %d\n' % grid)
    atnos = get_atnos(geometry)
    instr.append('atom types\n')
    instr.append('%d\n'% len(atnos))
    for atno in atnos:
        instr.append('atom file\n')
        instr.append('%s.atm\n' % symbol[atno])
    instr.append('number of atoms in unit cell\n')
    instr.append('%d \n' % len(geometry))
    instr.append('atom, type, position vector\n')
    for i in range(len(geometry)):
        atno,(x,y,z) = geometry[i]
        instr.append('%3d %3d %15.12f %15.12f %15.12f\n' %
                     (i+1,atnos.index(atno)+1,x,y,z))
    if kgrid:
        instr.append('kgrid\n')
        instr.append('%d %d %d\n' % kgrid)

    if symops:
        instr.append('symops\n')
        instr.append('%d\n' % len(symops))
        instr.append('definitions sym ops\n')
        for symop in symops:
            instr.append('%4d %9.6f %9.6f %9.6f   %13.10f %13.10f %13.10f\n'
                         % symop)

    instr.append('end setup phase data\n')
    instr.append('run phase data\n')
    instr.append('first iteration number\n')
    instr.append(' 0\n') # hardwired-change
    instr.append('last iteration number\n')
    instr.append('40\n') # hardwired-change
    instr.append('percent blend\n')
    instr.append('0.30\n') # hardwired-change
    instr.append('convergence criterion\n')
    instr.append('%f\n' % econv)
    instr.append('geometry optimization parameters:\n')
    instr.append('gconv\n')
    instr.append('%f\n' % gconv)
    if cell and pressure:
        instr.append('cell_relaxation\n')
        instr.append('pressure\n')
        instr.append('%f\n' % pressure)
        instr.append('end cell\n')
    instr.append('end of run phase data\n')

    file = open(filename,'w')
    file.writelines(instr)
    file.close()
    return 

def read_output(filename):
    enpat = re.compile('FINAL CONVERGED ENERGY')
    forcepat = re.compile('total force contributions')
    newgeopat = re.compile('NEW GEOMETRY')
    fingeopat = re.compile('FINAL GEOMETRY')
    typepat = re.compile('type number, label')
    cellpat = re.compile('UNIT CELL')
    qmdpat = re.compile('\<QMD\>')
    file = open(filename)
    results = {}
    labels = []
    results['energy'] = 0
    results['energies'] = []
    results['geos'] = []
    results['qmd'] = []
    while 1:
        line = file.readline()
        if not line: break
        if enpat.search(line):
            words = string.split(line)
            results['energy'] = float(words[5])
            results['energies'].append(float(words[5]))
        if forcepat.search(line):
            results['forces'] = get_forces(file)
        if newgeopat.search(line) or fingeopat.search(line):
            geo = get_geo(file,labels)
            results['geometry'] = geo
            results['geos'].append(geo)
        if typepat.search(line):
            line = file.readline()
            words = string.split(line)
            labels.append(words[1])
        if cellpat.search(line):
            results['cell'] = get_cell(file)
        if qmdpat.search(line):
            vxyz,temp,tempinit,ekin,epot,etot = read_qmd(file)
            results['qmd'].append((vxyz,temp,tempinit,ekin,epot,etot))
    return results

def read_qmd(file):
    # Line 1: nat
    line = file.readline()
    words = line.split()
    nat = int(words[1])

    # Line 2: temperatures
    line = file.readline()
    words = line.split()
    tempinit,temp = map(float,words[3:5])

    # Line 3: energies
    line = file.readline()
    words = line.split()
    ekin, epot, etot = map(float,words[4:7])

    # Line 4: time step info
    line = file.readline()
    words = line.split()
    istep = int(words[5])
    dt = float(words[6])
    nsteps = int(words[7])
    neqsteps = int(words[8])

    # Line 5: vcomxyz
    line = file.readline()
    words = line.split()
    vcomxzy = map(float,words[4:7])

    # line 6: skip
    line = file.readline()

    # Line 7-end: xyz,vxyz
    vxyz = []
    for i in range(nat):
        line = file.readline()
        words = line.split()
        x,y,z = map(float,words[2:5])
        vx,vy,vz = map(float,words[5:8])
        atno = int(float(words[1]))
        vxyz.append((atno,x,y,z,vx,vy,vz))
    return vxyz,temp,tempinit,ekin,epot,etot    

def get_cell(file): 
    bs = file.readline()
    a = map(float,file.readline().split())
    b = map(float,file.readline().split())
    c = map(float,file.readline().split())
    return a,b,c

def get_forces(file):
    endpat = re.compile('f-defect')
    line = file.readline() # skip atom  x force   y force, etc. line
    forces = []
    while 1:
        line = file.readline()
        if not line: break
        if endpat.search(line): break
        words = string.split(line)
        if not words: break
        forces.append(map(float,words[1:4]))
    return forces

def get_geo(file,labels):
    endpat = re.compile('##############################')
    geo = []
    file.readline() # ship atom, type, line
    while 1:
        line = file.readline()
        if not line: break
        if endpat.search(line): break
        words = string.split(line)
        if not words: break
        type = int(words[1])
        sym = labels[type-1] # "-1" because py arrays start at 0
        atno = sym2no[cleansym(sym)]
        x,y,z = map(float,words[2:5])
        geo.append((atno,(x,y,z)))
    return geo

def read_xyz(filename):
    from Element import sym2no
    file = open(filename)
    geometries = []
    while 1:
        line = file.readline()
        if not line: break
        nat = int(line.split()[0])
        title = file.readline()
        atoms = []
        for i in range(nat):
            line = file.readline()
            words = line.split()
            atno = sym2no[cleansym(words[0])]
            x,y,z = map(float,words[1:])
            atoms.append((atno,(x,y,z)))
        geometries.append(atoms)
    return geometries

def write_vxyz(filename,vxyz,title="File written by SeqQuest.write_vxyz"):
    from Element import symbol
    file = open(filename,'w')
    file.write("%d\n%s\n" % (len(vxyz),title))
    for atno,x,y,z,vx,vy,vz in vxyz:
        file.write("%4s %10.4f %10.4f %10.4f %10.4f %10.4f %10.4f\n"
                   % (symbol[atno],x,y,z,vx,vy,vz))
    file.close()
    return

def write_xyz(filename,geometries,title="File written by SeqQuest.write_xyz"):
    file = open(filename,'w')
    for atoms in geometries: append_xyz(file,atoms,title)
    file.close()
    return

def append_xyz(file,atoms,title="File written by XYZ.py"):
    from Element import symbol
    file.write("%d\n%s\n" % (len(atoms),title))
    for atno,(x,y,z) in atoms:
        file.write("%4s %10.4f %10.4f %10.4f\n"
                   % (symbol[atno],x,y,z))
    file.flush()
    return

def read_hist(filename):
    unitpat = re.compile('@DISTANCE')
    cellpat = re.compile('@CELL')
    natpat = re.compile('@NUMBER OF ATOMS')
    typepat = re.compile('@TYPES')
    geopat = re.compile('@COORDINATES')
    enpat = re.compile('@ESCF')
    forcepat = re.compile('@FORCES')
    fmaxpat = re.compile('@FMAX')
    frmspat = re.compile('@FRMS')

    results = {}
    results['geos'] = []
    results['cells'] = []
    results['energies'] = []
    results['forces'] = []
    results['fmax'] = []
    results['frms'] = []

    file = open(filename)

    while 1:
        line = file.readline()
        if not line: break

        if unitpat.search(line):
            line = file.readline()
            results['units'] = line.strip()
        elif cellpat.search(line):
            line1 = file.readline().split()
            line2 = file.readline().split()
            line3 = file.readline().split()
            cell = [map(float,line1),map(float,line2),map(float,line3)]
            results['cell'] = cell
            results['cells'].append(cell)
        elif natpat.search(line):
            line1 = file.readline().split()
            nat = int(line1[0])
            nlines,rem = divmod(nat,20)
            if rem: nlines += 1
            types = []
            for i in range(nlines):
                line = file.readline()
                words = line.split()
                for word in words: types.append(int(word))
            assert len(types) == nat, 'Not enough types'
            results['types'] = types
        elif typepat.search(line):
            line1 = file.readline().split()
            ntypes = int(line1[0])
            syms = []
            for i in range(ntypes):
                words = file.readline().split()
                syms.append(words[0])
            assert len(syms) == ntypes, 'Not enough syms'
        elif geopat.search(line):
            geo = []
            for i in range(nat):
                line = file.readline().split()
                atno = sym2no[cleansym(syms[types[i]-1])]
                geo.append((atno,map(float,line)))
            results['geo'] = geo # always set to last one
            results['geos'].append(geo)
        elif enpat.search(line):
            line = file.readline().split()
            results['energies'].append(float(line[0]))
        elif forcepat.search(line):
            force = []
            for i in range(nat):
                line = file.readline().split()
                force.append(map(float,line))
            results['forces'].append(force)
        elif fmaxpat.search(line):
            line = file.readline().split()
            results['fmax'].append(float(line[0]))
        elif frmspat.search(line):
            line = file.readline().split()
            results['frms'].append(float(line[0]))
    return results    

CubicSymvecs = [ # fcc, bcc, sc
    (4,    0.0,  0.0,  1.0,    0.0,  0.0,  0.0),
    (3,    1.0,  1.0,  1.0,    0.0,  0.0,  0.0),
    (2,    1.0,  1.0,  0.0,    0.0,  0.0,  0.0),
    (-1,   0.0,  0.0,  0.0,    0.0,  0.0,  0.0)
    ]

TdSymvecs = [ # Sphaelerite zinc-blende, etc.
    (-4,   0.0,  0.0,  1.0,    0.0,  0.0,  0.0),
    (3,    1.0,  1.0,  1.0,    0.0,  0.0,  0.0),
    (-2,   1.0,  1.0,  0.0,    0.0,  0.0,  0.0)
    ]

WurtziteSymvecs = [ # 4-atom hexagonal cell, interstitial-centered 
    (6,    0.0,  0.0,  1.0,    0.0,  0.0,  0.5),
    (-2,   1.0,  0.0,  0.0,    0.0,  0.0,  0.0)
    ]

HCPSymvecs = [ # atom-centered
    (-6,   0.0,   0.0,   1.0,    0.0,  0.0,  0.0),
    (-2,   1.0,   0.0,   0.0,    0.0,  0.0,  0.0),
    (2,    0.0,   1.0,   0.0,    0.0,  0.0,  0.0),
    (-1,   0.0,   0.0,   0.0,    0.3333333333,  0.3333333333,  0.5)
    ]

HCP_interSymvecs = [ # interstitial-centered 
    (6,    0.0,  0.0,  1.0,    0.0,  0.0,  0.5),
    (2,    1.0,  0.0,  0.0,    0.0,  0.0,  0.0),
    (-1,   0.0,  0.0,  0.0,    0.0,  0.0,  0.0)
    ]

BC8Symvecs = [ # BC8 structure, 8-atom cubic cell 
    (2,    1.0,  0.0,  0.0,    0.0,  0.5,  0.0),
    (2,    0.0,  1.0,  0.0,    0.5,  0.5,  0.0),
    (2,    0.0,  0.0,  1.0,    0.5,  0.0,  0.0),
    (3,    1.0,  1.0,  1.0,    0.0,  0.5,  0.0),
    (-1,   0.0,  0.0,  0.0,    0.0,  0.0,  0.0)
    ]

SapphireSymvecs = [ # (Al2O3), two-layer/10-atom rhombohedral cell
    (3,    0.0,  0.0,  1.0,    0.0,  0.0,  0.0),
    (-1,   0.0,  0.0,  1.0,    0.0,  0.0,  0.0)
    ]

kAl2O3Symvecs = [ #  kappa phase alumina, 40-atom orthorhombic 
    (2,    0.0,  0.0,  1.0,    0.0,  0.0,  0.5),
    (-2,   1.0,  0.0,  0.0,    0.5,  0.5,  0.5),
    (-2,   0.0,  1.0,  0.0,    0.5,  0.5,  0.0)
    ]

QuartzSymvecs = [# Alpha-SiO2, 9-atom hexagonal cell, interstitial-centered 
    (3,   0.0,  0.0,  1.0,    0.0,  0.0, -0.333333333333),
    (2,   1.0,  0.0,  0.0,    0.0,  0.0,  0.0)
    ]

    
# ----------------- Executable stuff ----------------------

def main():
    import getopt,sys
    opts,args = getopt.getopt(sys.argv[1:],'ha:x:skcrv')

    seqquestexe = None
    atomdir = None
    dosetup = 0
    keep = DO_KEEP
    do_preclean = DO_PRECLEAN
    do_random_tempdir = DO_RANDOM_TEMPDIR
    verbose = VERBOSE

    for (key,value) in opts:
        if key == '-h':
            print __doc__
            sys.exit()
        elif key == '-a':        atomdir = value
        elif key == '-c':        do_preclean = 0
        elif key == '-k':        keep = 1
        elif key == '-r':        do_random_tempdir = 1
        elif key == '-s':        dosetup = 1
        elif key == '-v':        verbose = 1
        elif key == '-x':        seqquestexe = value

    for filename in args:
        if dosetup:
            startdir,atomlist = setup(filename,atomdir,seqquestexe,
                                      do_preclean, do_random_tempdir,
                                      verbose)
        else:
            results = seqquest(filename,atomdir,seqquestexe,keep,
                                      do_preclean, do_random_tempdir,
                                      verbose)
            print results['energy']
        # endif
    # end for
# end main

if __name__ == '__main__': main()
