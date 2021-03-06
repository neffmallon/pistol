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

def main(fname=None):
    # Consider running quest_setup here
    if not fname: fname = sys.argv[1]
    if fname.endswith('.in'):
        oname = fname.replace('.in','.out')
        hname = fname.replace('.in','.hist')
    else:
        oname = fname + ".out"
        hname = fname + ".hist"

        
    os.system('./lcao.x >& %s' % oname)
    if os.path.exists('lcao.hist'):
        shutil.copy("lcao.hist",hname)
    # Consider running quest_cleanup here
    return
    
if __name__ == '__main__': main()
