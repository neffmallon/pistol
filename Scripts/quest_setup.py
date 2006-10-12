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

def main(fname=None):
    # Copy input file and executable
    if not fname: fname = sys.argv[1]
    if fname != 'lcao.in' :
        print "Copyring input file from %s to lcao.in" % fname
        shutil.copy(fname,'lcao.in')
    print "Copying quest executable from %s to lcao.x" % quest_exe
    shutil.copy(quest_exe,'lcao.x')

    # Get atom files
    functional = get_functional(fname)
    atom_files = get_atom_files(fname)
    if functional == 'pbe':
        atom_search_dir = quest_pbe_dir
    else:
        atom_search_dir = quest_lda_dir
    for atom_file in atom_files:
        target = os.path.join(atom_search_dir,atom_file)
        print "Searching for %s in %s" % (atom_file,atom_search_dir)
        if os.path.exists(target):
            print "     found!"
            shutil.copy(target,atom_file)
        else:
            print "     not found; please copy by hand"
    return
    
if __name__ == '__main__': main()
