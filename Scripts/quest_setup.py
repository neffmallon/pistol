#!/usr/bin/env python

import shutil,sys,os

# Setup directories
home = os.environ['HOME']
quest_home = os.path.join(home,'Programs/Quest/')
quest_exe_dir = os.path.join(quest_home,'seqquest/obj')
quest_atom_dir = os.path.join(quest_home,'atoms/library')
quest_lda_dir = os.path.join(quest_atom_dir,'atoms_lda')
quest_pbe_dir = os.path.join(quest_atom_dir,'atoms_pbe')
quest_exe = os.path.join(quest_exe_dir,'lcao.x')
    
def get_functional(fname):
    file = open(fname)
    functional = 'lda'
    while 1:
        line = file.readline()
        if not line: break
        line = line.strip()

        if line.startswith('functional'):
            functional = file.readline().strip().lower()
    return functional

def get_atom_files(fname):
    file = open(fname)
    atom_files = []
    while 1:
        line = file.readline()
        if not line: break
        line = line.strip().lower()
        if line.startswith('atom file'):
            atom_files.append(file.readline().strip())
    return atom_files

def main(fname=None,test=True):
    # Copy input file and executable
    if not fname: fname = sys.argv[1]
    if not test:
        if fname != 'lcao.in' :
            shutil.copyfile(fname,'lcao.in')
        if not os.path.exists('lcao.x'):
            shutil.copyfile(quest_exe,'lcao.x')

    # Get atom files
    functional = get_functional(fname)
    atom_files = get_atom_files(fname)
    print functional,atom_files
    if functional == 'pbe':
        atom_search_dir = quest_pbe_dir
    else:
        atom_search_dir = quest_lda_dir
    for atom_file in atom_files:
        target = os.path.join(atom_search_dir,atom_file)
        if os.path.exists(target):
            shutil.copyfile(target,atom_file)
        else:
            print "Can't find %s in %s; please copy by hand" % \
                  (atom_file,atom_search_dir)
    return
    
if __name__ == '__main__': main(quest_home+"/seqquest/WaterCells/pos_16_rho0p75.in")
