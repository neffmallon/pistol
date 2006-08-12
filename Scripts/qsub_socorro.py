#!/usr/bin/env python
"""\
 Put a simple wrapper around a command to run Quest through qsub.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import sys,os,string,getopt
from Pistol.Util import root

filestr = """\
#!/bin/bash
#
#PBS -l walltime=5:0:0
#PBS -l size=%d
#PBS -q default
#PBS -N %s
#
cd %s
/cplant/bin/yod -sz %d /home/rmuller/socorro/src/socorro
"""

def main():
    nproc = 1
    if len(sys.argv)>1:
        opts,args = getopt.getopt(sys.argv[1:],'n')
        for key,val in opts:
            if key == '-n': nproc = int(val)
    
    cwd = os.getcwd()
    name = os.path.split(cwd)[1]
    qname = 'qsub_%s.dat' % name
    file = open(qname,'w')
    file.write(filestr % (nproc,name,cwd,nproc))
    file.close()
    os.system('qsub %s' % qname)

if __name__ == '__main__': main()
