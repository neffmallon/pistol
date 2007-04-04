#!/usr/bin/env python
"""\
NAME
        Jaguar.py - Read the information from a Jaguar calculation.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import sys,re,os
from numpy import *
from Pistol.Util import matrix_symmetrize,cleansym,convert2bohr,translate2com
from Pistol.Element import sym2no

jag_command = '/home/rmuller/Programs/schrodinger/jaguar'

basis_list = ['6-31g**','6-311g**','6-311g**++','sto-3g','cc-pvtz',
              'cc-pvtz(-f)','cc-pvtz(-f)++',
              'lacvp', 'lacvd', 'lav3d','lav3p']

symgeo = re.compile('Symmetrized geometry')
inpgeo = re.compile('Input geometry')
newgeo = re.compile('new geometry')
basisset = re.compile('basis set:')
charge = re.compile('net molecular charge:')
mult = re.compile('multiplicity:')
nbf = re.compile('number of basis functions')
scftype = re.compile('SCF type:')
energy = re.compile('SCFE:')
freqpat = re.compile('^  frequencies ')
etot_pat = re.compile('^etot ')

class JaguarJob:
    def __init__(self,name='jagjob'):
        self.name = name
        self.atomlist = []
        self.hamiltonian = 'hf'
        self.basis_set = '6-31g**'
        self.input_filename = self.name + '.in'
        self.output_filename = self.name + '.out'
        self.restart_filename = self.name + '.01.in'#won't work for some names
        self.sym = 1
        self.unrestricted_spin = 0
        self.gvb_pairs = []
        self.spin_multiplicity = 1
        self.optimize_geometry = 0
        self.plot_section = 0
        self.guess_section = 0
        self.print_flags = []
        self.iopt_flags = []
        self.other_flags = []
        self.opt_flags = []
        self.accurate = 0
        self.charge = 0
        self.iunit = 1
        return

    def set_iunit(self,value): self.iunit = int(value)

    def add_atom(self,atom):
        sym,x,y,z = atom
        x,y,z = map(float,(x,y,z))
        self.atomlist.append((sym,x,y,z))
        return

    def check(self):
        '''Do consistency check of input'''
        return

    def do_optimize_geometry(self):
        self.optimize_geometry = 1
        return

    def do_forces(self):
        self.optimize_geometry = -1
        return

    def print_overlap(self):
        self.print_flags.append(18)
        return

    def set_charge(self,charge):
        self.charge = int(charge)
        return

    def set_spin_multiplicity(self,mult):
        self.spin_multiplicity = int(mult)
        if self.spin_multiplicity <= 0:
            self.spin_multiplicity = 1 #In case someone does something dumb
        return

    def set_accurate_flag(self,flag=1):
        self.accurate = flag
        return

    def set_unrestricted_spin(self):
        self.unrestricted_spin = 1
        return

    def set_opt_flag(self,flag):
        number,value = flag
        self.opt_flags.append((number,value))
        return

    def set_iopt_flag(self,flag):
        number,value = flag
        self.iopt_flags.append((number,value))
        return

    def set_restricted_spin(self):
        self.unrestricted_spin = 0
        return

    def set_basis_set(self,basisname):
        basisname = string.lower(basisname)
        if basisname in basis_list:
            self.basis_set = basisname
        return

    def set_ham_from_string(self,ham):
        if ham == 'hf' or ham == 'b3lyp' or ham == 'pw91' or ham == 'bp86' \
           or ham == 'blyp' or ham == 'b3gga2' or ham == 'halfhalf' \
           or ham == 'lda':
            self.hamiltonian = ham
        elif ham == 'gvb':
            pairlist = [(1,0,1)]
            self.set_gvb_ham(pairlist)
        else:
            raise "Unknown Hamiltonian %s " % ham
        return
        
    def set_gvb_ham(self,pairs):
        self.hamiltonian = 'gvb'
        for (type,i,j) in pairs:
            self.gvb_pairs.append((type,i,j))
        return

    def set_no_sym(self):
        self.sym = 0
        return

    def get_guess_from_restart(self,filename):
        file = open(filename,'r')
        guess_pat = re.compile('&guess')
        end_pat = re.compile('&')
        reading = 0
        for line in file.readlines():
            if reading:
                self.guess_section.append(line)
                if end_pat.search(line):
                    reading = 0
                    break
            if not reading:
                if guess_pat.search(line):
                    reading = 1
                    self.guess_section = []
                    self.guess_section.append(line)
        file.close()
        return

    def add_plot_section(self,orbs,origin,extent,npts):
        self.plot_section = 1
        self.plot_orbs = orbs
        self.plot_origin = origin
        self.plot_extent = extent
        self.plot_npts = npts
        return
                

    def write(self):
        file = open(self.input_filename,'w')
        self.write_gen(file)
        self.write_zmat(file)
        if self.hamiltonian == 'gvb':
            self.write_gvb(file)
        if self.plot_section:
            self.write_plot_section(file)
        if self.guess_section:
            self.write_guess(file)
        file.close()
        return

    def write_plot_section(self,file):
        file.write('&plot\n')
        file.write('iorb1a=%d\niorb2a=%d\n' % self.plot_orbs)
        file.write('origin= %15.6f %15.6f %15.6f\n' % self.plot_origin)
        file.write('extentx= %15.6f %15.6f %15.6f\n' % \
                   (self.plot_extent[0],0.,0.))
        file.write('extenty= %15.6f %15.6f %15.6f\n' % \
                   (0.,self.plot_extent[1],0.))
        file.write('extentz= %15.6f %15.6f %15.6f\n' % \
                   (0.,0.,self.plot_extent[2]))
        file.write('npts= %d %d %d\n' % self.plot_npts)
        file.write('&end\n')
        return

    def write_guess(self,file):
        for line in self.guess_section:
            file.write('%s' % line)
        return

    def write_gvb(self,file):
        file.write('&gvb\n')
        for (type,i,j) in self.gvb_pairs:
            symi,xi,yi,zi = self.atomlist[i]
            symj,xj,yj,zj = self.atomlist[j]
            file.write('%d %s %s\n' % (type,symi,symj))
        file.write('&\n')
        return

    def write_gen(self,file):
        file.write('&gen\n')
        self.hamiltonian = string.lower(self.hamiltonian)
        self.basis_set = string.lower(self.basis_set)

        if self.iunit != 1:
            file.write('iunit=%d\n' % self.iunit)

        if self.unrestricted_spin:
            file.write('iuhf=1\n')

        if self.charge != 0:
            file.write('molchg=%d\n' % self.charge)

        if self.spin_multiplicity != 1:
            file.write('multip=%d\n' % self.spin_multiplicity)

        if self.optimize_geometry != 0:
            file.write('igeopt=%d\n' % self.optimize_geometry)

        if not self.sym:
            file.write('isymm=0\n')

        for i in self.print_flags:
            file.write('ip%d=2\n' % i)

        for (number,value) in self.opt_flags:
            file.write('opt%d=%f\n' % (number,value))
        for (number,value) in self.iopt_flags:
            file.write('iopt%d=%d\n' % (number,value))
        for val in self.other_flags:
            file.write('%s\n' % val)

        if self.hamiltonian == 'hf':
            pass
        elif self.hamiltonian == 'pw91':
            file.write('idft=4441\n')
        elif self.hamiltonian == 'b3lyp':
            file.write('idft=22111\n')
        elif self.hamiltonian == 'lda':
            file.write('idft=101\n')
        elif self.hamiltonian == 'bp86':
            file.write('idft=1311\n')
        elif self.hamiltonian == 'halfhalf':
            file.write('idft=10001\n')
        elif self.hamiltonian == 'b3gga2':
            file.write('idft=24411\n')
        elif self.hamiltonian == 'blyp':
            file.write('idft=2011\n')
        elif self.hamiltonian == 'gvb':
            pass
        else:
            sys.stderr.write('Error: Unknown Hamiltonian type: %s\n'
                             % self.hamiltonian)
            sys.exit()

        if self.basis_set != '6-31g**':
            file.write('basis=%s\n' % self.basis_set)

        if self.accurate:
            file.write('iacc=%d\n' % self.accurate)
            
        file.write('&\n')
        return

    def write_zmat(self,file):
        file.write('&zmat\n')
        for atom in self.atomlist:
            file.write('%s %20.10f %20.10f %20.10f\n' % atom)
        file.write('&\n')
        return

    def run(self):
        self.write()
        #runstr = 'env JAGUAR_HOME=/exec/jaguar/MSC ' \
        #         '$JAGUAR_HOME/jaguar run -w -F %s >& /dev/null' %\
        #         self.input_filename
        runstr = '%s run -w -F %s >& /dev/null' % (jag_command,self.input_filename)
        #runstr = '%s run -w -F %s' % (jag_command,self.input_filename)
        #print 'Exec-ing: %s' % runstr
        os.system(runstr)
        return self.get_energy_from_output()

    def get_energy_from_output(self):
        file = open(self.output_filename,'r')
        energy = 0.
        for line in file.readlines():
            if etot_pat.search(line):
                words = string.split(line)
                energy = float(words[6])
        file.close()
        return energy

    #def get_forces_from_output(self):
    #    file = open(self.output_filename,'r')
    #    forces = []
    #    for line in file.readlines():
    #        if etot_pat.search(line):
    #            words = string.split(line)
    #            energy = float(words[6])
    #    file.close()
    #    return energy

def get_energy_forces(atoms):
    job = JaguarJob()
    for atno,(x,y,z) in atoms:
        job.add_atom((symbol[atno],x,y,z))
    job.do_forces()
    job.run()
    energy = job.get_energy_from_output()
    return energy    

# Misc utilities here
def get_energy_from_output(fname):
    en = 0
    for line in open(fname):
        words = line.split()
        if not words: continue
        if words[0] == 'etot': en = float(words[6])
    return en

def get_overlap_from_output(filename):
    file = open(filename,'r')
    nbf_pattern = re.compile("number of basis functions....")
    olap_pattern = re.compile("^\s*olap\s*$")
    nbf = 0
    while 1:
        line = file.readline()
        if not line: break
        if nbf_pattern.search(line):
            words = string.split(line)
            nbf = int(words[4])
        if olap_pattern.match(line):
            assert nbf > 0, "Must have nbf defined by now!"
            S = zeros((nbf,nbf),Float)
            nread,nlast = divmod(nbf,5)
            for block in range(nread):
                istart = 5*block
                line = file.readline()
                line = file.readline()
                for ibf in range(istart,nbf):
                    line = file.readline()
                    words = string.split(line)
                    for j in range(1,min(5,ibf-istart+1)+1):
                        jbf = istart + j-1
                        S[ibf,jbf] = float(words[j])
            # Now get the last block, if necessary
            istart = 5*nread
            line = file.readline()
            line = file.readline()
            for ibf in range(istart,nbf):
                line = file.readline()
                words = string.split(line)
                for j in range(1,min(nlast,ibf-istart+1)+1):
                    jbf = istart + j-1
                    S[ibf,jbf] = float(words[j])
    file.close()
    S = matrix_symmetrize(S)
    return S

def get_FockCO_from_output(filename):
    file = open(filename,'r')
    nbf_pattern = re.compile("number of basis functions....")
    fock_pattern = re.compile("Fock in CO")
    nbf = 0
    nread = 0
    while 1:
        line = file.readline()
        if not line: break
        if nbf_pattern.search(line):
            words = string.split(line)
            nbf = int(words[4])
        if fock_pattern.search(line):
            assert nbf > 0, "Must have nbf defined by now!"
            F = zeros((nbf,nbf),Float)
            nread,nlast = divmod(nbf,5)
            for block in range(nread):
                istart = 5*block
                line = file.readline()
                line = file.readline()
                for ibf in range(istart,nbf):
                    line = file.readline()
                    words = string.split(line)
                    for j in range(1,min(5,ibf-istart+1)+1):
                        jbf = istart + j-1
                        F[ibf,jbf] = float(words[j])
            # Now get the last block, if necessary
            istart = 5*nread
            line = file.readline()
            line = file.readline()
            for ibf in range(istart,nbf):
                line = file.readline()
                words = string.split(line)
                for j in range(1,min(nlast,ibf-istart+1)+1):
                    jbf = istart + j-1
                    F[ibf,jbf] = float(words[j])
    
    file.close()
    F = matrix_symmetrize(F)
    return F

def get_FockAO_from_output(filename):
    file = open(filename,'r')
    nbf_pattern = re.compile("number of basis functions....")
    fock_pattern = re.compile("Fock in AO")
    nbf = 0
    nread = 0
    while 1:
        line = file.readline()
        if not line: break
        if nbf_pattern.search(line):
            words = string.split(line)
            nbf = int(words[4])
        if fock_pattern.search(line):
            assert nbf > 0, "Must have nbf defined by now!"
            F = zeros((nbf,nbf),Float)
            nread,nlast = divmod(nbf,5)
            for block in range(nread):
                istart = 5*block
                line = file.readline()
                line = file.readline()
                for ibf in range(istart,nbf):
                    line = file.readline()
                    words = string.split(line)
                    for j in range(1,min(5,ibf-istart+1)+1):
                        jbf = istart + j-1
                        F[ibf,jbf] = float(words[j])
            # Now get the last block, if necessary
            istart = 5*nread
            line = file.readline()
            line = file.readline()
            for ibf in range(istart,nbf):
                line = file.readline()
                words = string.split(line)
                for j in range(1,min(nlast,ibf-istart+1)+1):
                    jbf = istart + j-1
                    F[ibf,jbf] = float(words[j])
    
    file.close()
    F = matrix_symmetrize(F)
    return F

def get_restart_orbs(filename):
    "Returns a list of [(orbe,occ,values)] for the guess section"
    file = open(filename,'r')
    start_pattern = re.compile('&guess ')
    orb_pattern = re.compile("Orbital Energy")
    end_pattern = re.compile('&') 
    orbs = []
    started = 0
    while 1:
        line = file.readline()
        if not line:
            break
        if started:
            if end_pattern.search(line):
                started = 0
                break
            if orb_pattern.search(line):
                words = line.split()
                orbe = float(words[3])
                occ = float(words[5])
                orb = []
                orbs.append((orbe,occ,orb))
            else:
                words = string.split(line)
                for word in words:
                    orb.append(float(word))
        else:
            if start_pattern.search(line):
                started = 1
    file.close()
    return orbs

def get_orbital_from_unrestricted_restart(filename):
    file = open(filename,'r')
    start_pattern = re.compile('&guess ')
    alpha_pattern = re.compile("Alpha Orbital Energy")
    beta_pattern  = re.compile("Beta Orbital Energy")
    end_pattern = re.compile('&')
    alpha_skip = re.compile('Alpha Molecular Orbitals')
    beta_skip = re.compile('Beta Molecular Orbitals')
    alpha = []
    beta = []

    started = 0
    while 1:
        line = file.readline()
        if not line:
            break
        if started:
            if alpha_skip.search(line) or beta_skip.search(line):
                continue
            if end_pattern.search(line):
                started = 0
                break
            if alpha_pattern.search(line):
                orb = []
                alpha.append(orb)
            elif beta_pattern.search(line):
                orb = []
                beta.append(orb)
            else:
                words = string.split(line)
                for word in words:
                    orb.append(float(word))
        else:
            if start_pattern.search(line):
                started = 1
    file.close()
    return alpha,beta

def get_orbital_from_restart(filename):
    # Consider including this again
    #print "Warning: this routine is deprecated"
    #print "...use get_restart_orbs"
    file = open(filename,'r')
    start_pattern = re.compile('&guess ')
    orb_pattern = re.compile("Orbital Energy")
    end_pattern = re.compile('&') 
    orbs = []
    started = 0
    while 1:
        line = file.readline()
        if not line:
            break
        if started:
            if end_pattern.search(line):
                started = 0
                break
            if orb_pattern.search(line):
                orb = []
                orbs.append(orb)
            else:
                words = string.split(line)
                for word in words:
                    orb.append(float(word))
        else:
            if start_pattern.search(line):
                started = 1
    file.close()
    return array(orbs)

def read_input(filename):
    file = open(filename,'r')

    # Pre-compile some patterns to make searching faster
    patzmat = re.compile('[\&\$]zmat')
    patgen = re.compile('[\&\$]gen')
    patguess = re.compile('[\&\$]guess')

    guess = []
    geometry = []

    while 1:
        line = file.readline()
        if not line: break
        
        if patzmat.search(line):
            geometry = read_zmat(file)
        if patgen.search(line):
            (charge,spin_multiplicity,basis) = read_gen(file)
        if patguess.search(line):
            guess = read_guess(file)
    file.close()
    return geometry,basis,guess


def read_zmat(file):
    patend = re.compile('[\&\$]')
    geometry = []
    while 1:
        line = file.readline()
        if not line: break
        if patend.search(line): break
        words = string.split(line)
        if len(words) < 4:
            raise "Can't handle zmatrix geometries yet"
        sym = cleansym(words[0])
        atno = sym2no[sym]
        x = float(words[1])
        y = float(words[2])
        z = float(words[3])
        geometry.append((sym,atno,x,y,z))
    return geometry

def read_gen(file):
    patend = re.compile('[\&\$]')
    patmult = re.compile('molchg')
    patbasis = re.compile('basis')
    patcharge = re.compile('molchg')

    charge = 0
    spin_multiplicity = 1
    basis = '6-31g**'
    while 1:
        line = file.readline()
        if not line: break
        if patend.search(line): break

        # Note: the following split won't work if there are
        # spaces before or after the equals sign. Need to figure out
        # a more clever way of doing this.
        if patmult.search(line):
            words = re.split('[\s\=]',line)
            spin_multiplicity = int(words[1])
        if patbasis.search(line):
            words = re.split('[\s\=]',line)
            basis = words[1]
        if patcharge.search(line):
            words = re.split('[\s\=]',line)
            charge = float(words[1])
    return (charge,spin_multiplicity,basis)

def read_guess(file):
    # Simply append the lines to the guess array now; worry about what
    # to do with them later.

    guess = []
    
    patend = re.compile('[\&\$]')
    patorb = re.compile('Orbital Energy')
    energy = 'undefined'
    array = []
    while 1:
        line = file.readline()
        if not line: break
        if patend.search(line): break
        if patorb.search(line):
            if energy != 'undefined':
                # Append the previous orbital
                guess.append((energy,occupation,array))
                array = []
            words = string.split(line)
            energy = float(words[3])
            occupation = float(words[5])
        else:
            coefs = map(float,line.split())
            for coef in coefs: array.append(coef)
            #array.append(line)
    guess.append((energy,occupation,array))
    
    return guess

def write_qmagic(geometry,basis,guess):
    if basis != '6-31g**' and basis != '6-31G**':
        print 'Current basis set is unsupported : ',basis
        sys.exit()

    # Header stuff:
    sys.stdout.write(' ********* QMAGIC Input from JAGUAR OUTPUT ******\n')
    sys.stdout.write(' OUTXX FORMATTED\n')
    sys.stdout.write(' VARIATIONAL\n')
    sys.stdout.write(' RANSEED 12345678\n')
    sys.stdout.write(' PUNCH 0\n')
    sys.stdout.write(' NUMBLK 10\n')
    sys.stdout.write(' BLKTIM 5.00\n')
    sys.stdout.write(' TSTEP 0.5\n')
    sys.stdout.write(' KONORM 1000\n')
    sys.stdout.write(' KONMAX 2000\n')
    sys.stdout.write(' EECF 0.5 0.66\n') #e-e Correlation Function. 

    # Geometry and Basis Set:
    sys.stdout.write(' BASIS\n')
    sys.stdout.write('  6-31G** basis from Jaguar Output\n')
    for atom in geometry:
        sym,atno,x,y,z = atom
        lam = 0.1  # Bad guess at the e-N Jastrow
        nu = 0.1   # Bad guess at the e-N Jastrow
        basis_name = sym+'631G'
        sys.stdout.write('%s %4.1f %10.4f %10.4f %10.4f %10.4f %10.4f\n' %\
              (sym,atno,x,y,z,lam,nu))
        sys.stdout.write('      BASLIB %s\n\n' % basis_name)
    sys.stdout.write(' ENDBASIS\n')

    # Occupations of orbitals; allows for MC-SCF type configs
    sys.stdout.write(' WFN\n')
    sys.stdout.write('1.0 ')
    for orbital in guess:
        energy,occupation,array = orbital
        if occupation == 1.0:
            sys.stdout.write('DOC ')
        elif occupation == 0.5:
            sys.stdout.write('ALP ')
        else:
            break
    sys.stdout.write('\n')
    sys.stdout.write(' ENDWFN\n')

    # The orbitals themselves. Printed in HONDO format, which is a pain
    # in the butt.
    sys.stdout.write(' VECTORS\n')
    iorb = 1
    for orbital in guess:
        iline = 1
        energy, occupation, array = orbital
        orbs = []
        for line in array:
            words = string.split(line)
            for word in words:
                orbs.append(float(word))

        if occupation == 1.0 or occupation == 0.5:
            nbf = len(orbs)
            nlines,nlast = divmod(nbf,5)
            for i in range(nlines):
                ptr = i*5
                ip = i+1
                sys.stdout.write('%2d%3d%15.8E%15.8E%15.8E%15.8E%15.8E\n' %\
                                 (iorb,ip,orbs[ptr],orbs[ptr+1],
                                  orbs[ptr+2],orbs[ptr+3],orbs[ptr+4]))
            # write out the last line:
            if nlast != 0:
                sys.stdout.write('%2d%3d' % (iorb,nlines+1))
                for ibf in range(nlast):
                    ptr = 5*(nlines+1)+ibf
                    sys.stdout.write('%15.8E' % orbs[ptr])
                for ibf in range(nlast,5):
                    sys.stdout.write('%15.8E' % 0.0)
                sys.stdout.write('\n')
            iorb = iorb + 1
                    
    sys.stdout.write(' ENDVECTORS\n')

    sys.stdout.write(' RUN\n')
    sys.stdout.write(' END\n')

def jagin2qmagic(filename):
    geo,basisname,guess = read_input(filename)
    write_qmagic(geo,basisname,guess)
    return

def get_one_geo(file):
    geo = []
    lines2skip = 2
    for i in range(lines2skip): file.readline()
    while 1:
        line = file.readline()
        if not line: break
        words = string.split(line)
        if len(words) < 4: break
        sym = cleansym(words[0])
        x,y,z = float(words[1]),float(words[2]),float(words[3])
        geo.append((sym,x,y,z))
    return geo

def write_gamessin(geo,filename):
    file = open(filename,'w')
    file.write(' $CONTRL SCFTYP=RHF RUNTYP=ENERGY UNITS=ANGSTROM $END\n')
    file.write(' $GUESS  GUESS=HUCKEL $END\n')
    file.write(' $BASIS GBASIS=N31 NGAUSS=6 NPFUNC=1 NDFUNC=1 $END\n')
    file.write(' $DATA\nAutomatically generated by jagout2gamessin.py\n')
    file.write('C1\n')
    for (sym,x,y,z) in geo:
        atno = sym2no[sym]
        file.write('%-8s %d %10.6f %10.6f %10.6f\n' % (sym,atno,x,y,z))
    file.write(' $END\n')
    file.close()
    return

def read_jagout(filename):
    "By default, read only one geometry"
    return read_jagout_onegeo(filename)

def read_jagout_allgeos(filename):
    "Return the all geometries from a Jaguar output file"
    file = open(filename,'r')

    symgeo = re.compile('Symmetrized geometry:')
    inpgeo = re.compile('Input geometry:')
    newgeo = re.compile('new geometry:')
    fingeo = re.compile('final geometry:')
    bs = re.compile('agu')
    etot = re.compile('etot')

    geos = []
    energies = []
    current_energy = 0.0
    while 1:
        line = file.readline()

        if not line: break

        if etot.search(line): current_energy = float(string.split(line)[6])

        if symgeo.search(line) or inpgeo.search(line) or newgeo.search(line):
            geo = get_one_geo(file)
            geos.append(geo)
            energies.append(current_energy)
    file.close()
    return geos

def read_jagout_onegeo(filename):
    "Return the last geometry from a Jaguar output file"
    file = open(filename,'r')

    inpg_pat = re.compile("Input geometry:")
    symg_pat = re.compile("Symmetrized geometry:")
    newg_pat = re.compile("new geometry:")
    fing_pat = re.compile("final geometry:")

    geo = []
    while 1:
        line = file.readline()
        if not line: break
        if inpg_pat.search(line) or symg_pat.search(line) \
           or newg_pat.search(line) or fing_pat.search(line):
            geo = get_one_geo(file)        
    # end of main infinite loop
    file.close()

    return geo #only return the last geometry


def jagout2gamessin(filename):
    outfilename = string.replace(filename,'.out','.inp')
    geo = read_jagout(filename)
    write_gamessin(geo,outfilename)
    return

def jagout2seqquestin(filename):
    geo = read_jagout(filename)
    geo = convert2Bohr(geo)
    geo = translate2COM(geo)
    outfilename = string.replace(filename,'.out','.tape5')
    write_seqquestin(geo,outfilename)
    return

def get_atomtypes(geo):
    atomtypes = []
    for (sym,x,y,z) in geo:
        if sym in atomtypes:
            pass
        else:
            atomtypes.append(sym)
    return atomtypes

def write_seqquestin(geo,filename):
    file = open(filename,'w')
    file.write("do setup\n")
    file.write("do iters\n")
    file.write("no force\n")
    file.write("no relax\n")
    file.write("input data\n")
    file.write("title\n")
    file.write("Generated by jagout2sq.py\n")
    file.write("lattice dimensionality (2=slab, 3=bulk)\n")
    file.write(" 0\n")
    file.write("primitive lattice vectors\n")
    file.write(" 25.0  0.0  0.0\n")
    file.write("  0.0 25.0  0.0\n")
    file.write("  0.0  0.0 25.0\n")
    file.write("points along box sides\n")
    file.write("64 64 64\n")

    atomtypes = get_atomtypes(geo)
    file.write("atom types\n")
    file.write(" %d\n" % len(atomtypes))
    for atomtype in atomtypes:
        file.write("atom file\n")
        file.write("%s.atm\n" % atomtype)

    file.write("number of atoms in unit cell\n")
    file.write(" %d\n" % len(geo))
    file.write("atom, type, position vector\n")

    for i in range(len(geo)):
        sym,x,y,z = geo[i]
        file.write("%d %d %12.6f %12.6f %12.6f\n" %
                   (i+1,atomtypes.index(sym)+1,x,y,z))
    file.write("end setup phase data\n")
    file.write("run phase input data\n")
    file.write("first iteration number\n")
    file.write(" 0\n")
    file.write("last iteration number\n")
    file.write("20\n")
    file.write("percent blend\n")
    file.write("0.30\n")
    file.write("convergence criterion\n")
    file.write("0.00001000\n")
    file.write("geometry optimization parameters:\n")
    file.write("gconv\n")
    file.write("0.0004\n")
    file.write("end of run phase data\n")
    file.close()
    return
        

def jagout2xyz(filename):
    geos = read_jagout_allgeos(filename)
    outfilename = string.replace(filename,'.out','.xyz')
    file = open(outfilename,'w')
    for geo in geos:
        file.write('%d\nMade by jagout2xyz.py\n' % len(geo))
        for atom in geo:
            file.write('%s %12.6f %12.6f %12.6f\n' % atom)
    file.close()
    return
    
def read_output(filename):
    "Get a list of geometries from the jaguar output file"
    file = open(filename,'r')

    geos = []
    while 1:
        line = file.readline()
        if not line: break

        if symgeo.search(line) or inpgeo.search(line):
            geo = getgeo(file)
            geos = [geo] # set as the first geo; overwrite if necessary
        elif newgeo.search(line):
            geo = getgeo(file)
            geos.append(geo)
    return geos

def read_output_as_dict(filename):
    "Get lots of information from jagout and return as a dictionary"
    file = open(filename,'r')
    record = {}
    record['name'] = filename.replace('.out','')
    freqs = []
    while 1:
        line = file.readline()
        if not line: break

        if symgeo.search(line) or inpgeo.search(line):
            geo = getgeo(file)
            record['structure'] = geo
        elif newgeo.search(line):
            geo = getgeo(file)
            if record.has_key('structure'):
                record['input structure'] = record['structure']
            record['structure'] = geo
        elif basisset.search(line):
            record['basis'] = line.split()[2:]
        elif charge.search(line):
            record['charge'] = int(line.split()[3])
        elif mult.search(line):
            record['multiplicity'] = int(line.split()[1])
        elif nbf.search(line):
            record['nbf'] = int(line.split()[4])
        elif scftype.search(line):
            record['scftype'] = ' '.join(line.split()[2:])
        elif energy.search(line):
            record['energy'] = float(line.split()[4])
        elif freqpat.search(line):
            frs = map(float,line.split()[1:])
            freqs += frs
    if record.has_key('energy'): record['energy units'] = 'hartrees'
    if freqs:
        record['freqs'] = freqs
        record['freq_units'] = 'cm^-1'

        # The following is slow, and should be rewritten as a one-pass read through
        #  the output file
        modes = []
        nfreq = len(freqs)
        for i in range(nfreq):
            mode = getmode(i+1,filename)
            modes.append(mode)
        record['modes'] = modes
    return record

def read_plt(filename):
    plt_info = {}
    plot = re.compile('&plot')
    iplot = re.compile('iplot')
    iorb1a = re.compile('iorb1a')
    iorb2a = re.compile('iorb2a')
    iorb1b = re.compile('iorb1b')
    iorb2b = re.compile('iorb2b')
    origin = re.compile('origin')
    extentx = re.compile('extentx')
    extenty = re.compile('extenty')
    extentz = re.compile('extentz')
    npts = re.compile('npts')
    end = re.compile('&end')

    file = open(filename)

    while 1:
        line = file.readline()
        if not line: break
        
        if plot.search(line) or iplot.search(line) or iorb1a.search(line) or \
           iorb2a.search(line) or iorb1b.search(line) or iorb2b.search(line):
            #continue
            pass
        elif origin.search(line):
            plt_info['origin'] = map(float,line.split()[1:4])
        elif extentx.search(line):
            plt_info['xvec'] = map(float,line.split()[1:4])
        elif extenty.search(line):
            plt_info['yvec'] = map(float,line.split()[1:4])
        elif extentz.search(line):
            plt_info['zvec'] = map(float,line.split()[1:4])
        elif npts.search(line):
            nx,ny,nz = map(int,line.split()[1:4])
            plt_info['npts'] = (nx,ny,nz)
        elif end.search(line):
            plt_info['grid'] = get_grid(file,nx,ny,nz)
            break
        else:
            print "Warning: unexpected line"
            print line
    file.close()

    return plt_info

def guess_plot_section():
    "Guess an appropriate $plot section for outputting Jaguar orbitals"
    
    from Constants import bohr2ang
    buffer = 2 #angstrom
    pts_bohr = 4 #RPM changing from 2 to 4 b/c not enough
    atoms = read_output(filename)
    xmin,xmax,ymin,ymax,zmin,zmax = get_bbox(atoms)

    # now convert bbox to bohr
    xmin /= bohr2ang
    ymin /= bohr2ang
    zmin /= bohr2ang
    xmax /= bohr2ang
    ymax /= bohr2ang
    zmax /= bohr2ang
    
    extentx = xmax - xmin
    extenty = ymax - ymin
    extentz = zmax - zmin

    nptsx = int(pts_bohr*extentx)
    nptsy = int(pts_bohr*extenty)
    nptsz = int(pts_bohr*extentz)

    print '&plot'
    print 'iorb1a = ?'
    print 'iorb2a = ?'
    print 'origin = %10.6f %10.6f %10.6f' % (xmin,ymin,zmin)
    print 'extentx = %10.6f %10.6f %10.6f' % (extentx,0,0)
    print 'extenty = %10.6f %10.6f %10.6f' % (0,extenty,0)
    print 'extentz = %10.6f %10.6f %10.6f' % (0,0,extentz)
    print 'npts = %6d %6d %6d ' % (nptsx,nptsy,nptsz)
    print '&'
    return

def get_bbox(atoms,buffer=2):
    big = 1e8
    xmin = ymin = zmin = big
    xmax = ymax = zmax = -big

    for atno,(x,y,z) in atoms[-1]:
        if x < xmin : xmin = x
        if y < ymin : ymin = y
        if z < zmin : zmin = z
        if x > xmax : xmax = x
        if y > ymax : ymax = y
        if z > zmax : zmax = z

    xmin,ymin,zmin = xmin-buffer,ymin-buffer,zmin-buffer
    xmax,ymax,zmax = xmax+buffer,ymax+buffer,zmax+buffer
    return xmin,xmax,ymin,ymax,zmin,zmax

def getgeo(file):
    file.readline()
    file.readline()

    geo = []

    while 1:
        line = file.readline()
        if not line: break
        words = line.split()
        if len(words) < 4: break # Reached the end of atom section
        
        sym = words[0]
        x,y,z = map(float,words[1:4])
        sym = cleansym(sym)
        geo.append((sym2no[sym],(x,y,z)))
    return geo

def get_grid(file,nx,ny,nz):
    from numpy import zeros,Float
    grid = zeros((nx,ny,nz),Float)

    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                grid[i,j,k] = float(file.readline())
    return grid

def cleansym(sym):
    "Strips off everything after the first non-letter in an element name"
    import re
    pat = re.compile('[^a-zA-Z]')
    newsym = pat.split(sym)[0]
    return newsym

def getmode(modenum,filename):
    import re,string
    freq = re.compile('^\s*frequencies')
    freqstart = re.compile('start of program freq')
    file = open(filename,'r')

    while 1:
        line = file.readline()
        if not line:
            break
        elif freqstart.search(line):
            count = 1
        elif freq.search(line):
            words = string.split(line)
            number = len(words) - 1
            if count <= modenum < count + number:
                recnum = modenum - count + 2
                mode = getonemode(recnum,file)
                file.close()
                return mode
            else:
                count = count + number
    print 'Warning: could not find mode number %d' % modenum
    file.close()
    return []

def getonemode(recnum,file):
    import string,re
    mode = []
    red_mass = re.compile('reduc. mass')
    intens = re.compile('intensities')
    symmet = re.compile('symmetries')
    forceconst = re.compile('force const')
    while 1:
        line = file.readline()
        # Skip lines we don't want
        if red_mass.search(line) or intens.search(line) \
           or symmet.search(line) or forceconst.search(line):
            continue
        if not line: break
        words = string.split(line)
        if len(words) < 2: break
        x = float(words[recnum])
        line = file.readline()
        if not line:
            print 'Warning: should not break here!'
            break
        words = string.split(line)
        if len(words) < 2: break
        y = float(words[recnum])
        line = file.readline()
        if not line:
            print 'Warning: should not break here!'
            break
        words = string.split(line)
        if len(words) < 2: break
        z = float(words[recnum])

        mode.append((x,y,z))
    return mode

def demo(sym):
    "Demonstrate the usefulness of the Jaguar module"
    # Start
    job = JaguarJob('water')

    # Set to the Hamiltonian to be Density Functional Theory/B3LYP:
    job.set_ham_from_string('b3lyp') 

    # Add the atoms as symbol, x, y, z. By default, the distances are given
    #  in Angstrom (10^-10 m)
    job.add_atom(('O',0.,0.,0.))
    job.add_atom(('H',0.,0.,1.))
    job.add_atom(('H',0.,1.,0.))
    # here the initial bond angle is defined to be 90 deg, which is wrong...

    #...so optimize the geometry
    job.do_optimize_geometry()

    # run
    energy = job.run()
    print "Energy = ",energy

    # Dump out an XYZ trajectory from this run
    jagout2xyz(job.output_filename)
    return

def get_energy_from_output(filename):
    etotpat = re.compile('etot')
    etot = ''
    file = open(filename,'r')
    for line in file.readlines():
        if etotpat.search(line): etot = float(line.split()[6])
    return etot
    
