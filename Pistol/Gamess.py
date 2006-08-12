#!/usr/bin/env python
"""\
gamess.py: Run a gamess job

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import sys,os,glob,string,re
from shutil import copyfile
from Numeric import *

gamess_exe = "/ul/rpm/prog/gamess98/source/gamess.e"
scratch_dir = '/temp1/rpm'

VERBOSE = 1

env_variables = [
    ("IRCDATA", ".irc"),
    ("INPUT", ".F05"),
    ("PUNCH", ".dat"),
    ("AOINTS", ".F08"),
    ("MOINTS", ".F09"),
    ("DICTNRY", ".F10"),
    ("DRTFILE", ".F11"),
    ("CIVECTR", ".F12"),
    ("CASINTS", ".F13"),
    ("CIINTS", ".F14"),
    ("WORK15", ".F15"),
    ("WORK16", ".F16"),
    ("CSFSAVE", ".F17"),
    ("FOCKDER", ".F18"),
    ("DASORT", ".F20"),
    ("DFTINTS", ".F21"),
    ("JKFILE", ".F23"),
    ("ORDINT", ".F24"),
    ("EFPIND", ".F25"),
    ("PCMDATA", ".F26"),
    ("PCMINTS", ".F27"),
    ("DAFL30", ".F30"),
    ("MCQD50", ".F50"),
    ("MCQD51", ".F51"),
    ("MCQD52", ".F52"),
    ("MCQD53", ".F53"),
    ("MCQD54", ".F54"),
    ("MCQD55", ".F55"),
    ("MCQD56", ".F56"),
    ("MCQD57", ".F57"),
    ("MCQD58", ".F58"),
    ("MCQD59", ".F59"),
    ("MCQD60", ".F60"),
    ("MCQD61", ".F61"),
    ("MCQD62", ".F62"),
    ("MCQD63", ".F63"),
    ("MCQD64", ".F64")
    ]

def clean_scratch(scratch_dir,jobroot):
    del_list = glob.glob(scratch_dir + '/' + jobroot + '.*')
    for file in del_list:
        try_and_del(file)
    return    

def set_env_variables(scratch_dir,jobroot):
    for (name,ext) in env_variables:
        os.environ[name] = scratch_dir + "/" + jobroot + ext
    return

def try_and_del(file):
    if os.path.exists(file):
        os.unlink(file)
    return

def root(namestring):
    return os.path.splitext(namestring)[0]

def gamess(jobname):
    # Make sure scratch directory exists
    if VERBOSE:
        print "Gamess run driven by gamess.py"
        print "Scratch: ",scratch_dir
        print "Exec:    ",gamess_exe
    
    if os.path.exists(scratch_dir):
        pass
    else:
        try:
            mkdir(scratch_dir)
        except:
            print "%s doesn't exist, and can't be made" % scratch_dir
            sys.exit()

    if VERBOSE: print "Disk setup done"

    jobroot = root(jobname)
    # clean up the scratch directory before running; might want to
    #  make a way to override this later for restarting
    clean_scratch(scratch_dir,jobroot)
    copyfile(jobname,os.path.join(scratch_dir,jobroot+".F05"))
    set_env_variables(scratch_dir,jobroot)

    if VERBOSE: print "Setup done"

    # now execute GAMESS.
    os.system("%s > %s" % (gamess_exe,jobroot + ".out"))
    if VERBOSE: print "Execution done"

    datfile = jobroot + '.dat'

    # Copy the datfile back to the home directory
    copyfile(os.path.join(scratch_dir,datfile),datfile)

    # clean up the scratch directory
    #clean_scratch(scratch_dir,jobroot)
    return

def get_orbital_from_restart(filename):
    from Numeric import zeros,Float
    file = open(filename,'r')
    start_pattern = re.compile('\$VEC')
    end_pattern = re.compile('\$END') 
    orbs = []
    started = 0
    current_orbital_number = 0
    while 1:
        line = file.readline()
        if not line:
            break
        if started:
            if end_pattern.search(line):
                started = 0
                break
            words = string.split(line)
            iorb = eval(words[0])
            # test for new orbital
            if iorb != current_orbital_number:
                orb = []
                orbs.append(orb)
                current_orbital_number = iorb
            linefrag = line[5:]
            nwords = len(linefrag)/15
            for i in range(nwords):
                wordstart = i*15
                word = linefrag[wordstart:wordstart+15]
                orb.append(eval(word))
        else:
            if start_pattern.search(line):
                started = 1
    file.close()
    return array(orbs)

def get_overlap_from_output(filename):
    from Numeric import zeros,Float
    from Util import matrix_symmetrize
    file = open(filename,'r')
    nbf_pattern = re.compile("TOTAL NUMBER OF BASIS FUNCTIONS")
    olap_pattern = re.compile("OVERLAP MATRIX")
    nbf = 0
    while 1:
        line = file.readline()
        if not line: break
        if nbf_pattern.search(line):
            words = string.split(line)
            nbf = eval(words[6])
        if olap_pattern.search(line):
            assert nbf > 0, "Must have nbf defined by now!"
            S = zeros((nbf,nbf),Float)
            nread,nlast = divmod(nbf,5)
            for block in range(nread):
                istart = 5*block
                line = file.readline()
                line = file.readline()
                line = file.readline()
                for ibf in range(istart,nbf):
                    line = file.readline()
                    words = string.split(line)
                    for j in range(4,4+min(5,ibf-istart+1)):
                        jbf = istart + j-4
                        S[ibf,jbf] = eval(words[j])
            # Now get the last block, if necessary
            istart = 5*nread
            line = file.readline()
            line = file.readline()
            for ibf in range(istart,nbf):
                line = file.readline()
                words = string.split(line)
                for j in range(4,4+min(nlast,ibf-istart+1)):
                    jbf = istart + j-4
                    S[ibf,jbf] = eval(words[j])
    file.close()
    S = matrix_symmetrize(S)
    return S

class GamessJob:
    def __init__(self,name='gamessjob'):
        self.name = name
        self.atomlist = []
        self.hamiltonian = 'hf'
        self.basis_set = '6-31g**'
        self.input_filename = self.name + '.inp'
        self.output_filename = self.name + '.out'
        self.restart_filename = self.name + '.dat'
        self.unrestricted_spin = 0
        self.spin_multiplicity = 1
        self.optimize_geometry = 0
        self.units = 0 # Default, angstrom
        self.charge = 0

    def set_bohr(self): self.units = 1     # input file in bohr/au
    def set_angstrom(self): self.units = 0 # input file in angstroms

    def add_atom(self,atom):
        self.atomlist.append(atom)
        return

    def do_optimize_geometry(self):
        self.optimize_geometry = 1
        return

    def set_spin_multiplicity(self,mult):
        self.spin_multiplicity = int(mult)
        if self.spin_multiplicity <= 0:
            self.spin_multiplicity = 1 #In case someone does something dumb
        return

    def set_unrestricted_spin(self):
        self.unrestricted_spin = 1
        return

    def set_basis_set(self,basisname):
        basisname = string.lower(basisname)
        self.basis_set = basisname
        return

    def set_charge(self,charge):
        self.charge = int(charge)
        return

    def set_no_sym(self):
        "Null function, since by default the GAMESS jobs have no symemtry"
        return

    def set_iopt_flag(self,val):
        "Null function, since GAMESS jobs have no iopt flags"
        return

    def print_overlap(self):
        "Null function, since by default the GAMESS jobs print the overlap"
        return

    def get_guess_from_restart(self,filename):
        return

    def write(self):
        file = open(self.input_filename,'w')
        self.write_control(file)
        self.write_basis(file)
        self.write_guess(file)
        self.write_data(file)
        file.close()
        return

    def write_control(self,file):
        file.write(' $CONTRL ')

        if self.spin_multiplicity:
            if self.unrestricted_spin:
                file.write('SCFTYP=UHF ')
            else:
                file.write('SCFTYP=ROHF ')
            file.write('MULT=%d ' % self.spin_multiplicity)
        else:
            file.write('SCFTYP=RHF ')

        if self.optimize_geometry:
            file.write('RUNTYP=OPTMIZE ')
        else:
            file.write('RUNTYP=ENERGY ')

        if self.charge != 0: file.write('ICHARG=%d ' % self.charge)

        file.write('$END\n $CONTRL ')

        if self.units == 1: 
            file.write('UNITS=BOHR ')
        else:
            file.write('UNITS=ANGSTROM ')

        file.write('COORD=CART NPRINT=3 ')
        file.write('$END\n')
        return

    def write_basis(self,file):
        file.write(' $BASIS ')
        if string.lower(self.basis_set) == '6-31g**' :
            file.write('GBASIS=N31 NGAUSS=6 NDFUNC=1 NPFUNC=1 ')
        else:
            print "Warning: unsupported basis: ", self.basis_set
            sys.exit()
        file.write('$END\n')
        return

    def write_guess(self,file):
        file.write(' $GUESS GUESS=HUCKEL $END\n')
        return

    def write_data(self,file):
        from Util import cleansym
        from Element import sym2no
        file.write(' $DATA\n')
        file.write('%s GAMESS job generated automatically by gamess.py\n'
                   % self.name)
        file.write('C1\n')
        for atom in self.atomlist:
            name,x,y,z = atom
            sym = cleansym(name)
            atno = sym2no[sym]
            file.write('%s %5.1f %12.6f %12.6f %12.6f\n' %\
                       (name,atno,x,y,z))
        file.write(' $END\n')
        return

    def run(self):
        self.write()
        gamess(self.input_filename)
        return self.get_energy_from_output()

    def get_energy_from_output(self):
        etot_pat = re.compile(" FINAL ENERGY IS")
        file = open(self.output_filename,'r')
        energy = 0.
        for line in file.readlines():
            if etot_pat.search(line):
                words = string.split(line)
                energy = eval(words[3])
        file.close()
        return energy    


if __name__ == '__main__':
    for jobname in sys.argv[1:]:
        gamess(jobname)
