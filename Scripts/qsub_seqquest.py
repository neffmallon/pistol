#!/usr/bin/env python
"""\
 Put a simple wrapper around a command to run through qsub.
"""

import sys,os,string,getopt
from Quest.Util import root

filestr = """\
#!/bin/bash
#
#PBS -l walltime=5:0:0
#PBS -l size=1
#PBS -q default
#PBS -N %s
#
cd %s
/home/rmuller/cplant/bin/run_seqquest.py %s
"""

def main():
    cwd = os.getcwd()
    for fname in sys.argv[1:]:
        fname_root = root(fname)
        qname = 'qsub_%s.dat' % fname_root
        file = open(qname,'w')
        file.write(filestr % (fname_root,cwd,fname))
        file.close()
        os.system('qsub %s' % qname)

if __name__ == '__main__': main()
