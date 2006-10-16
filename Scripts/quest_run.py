#!/usr/bin/env python

import shutil,sys,os

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
