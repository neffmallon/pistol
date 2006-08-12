#!/usr/bin/env python
"""\
 Wrapper around qsub to make commands easier to execute

 Usage: qsub.py [options] command

 Options:
 -h      Print this help message
 -n  X   Run job on X processors (default=1)
 -N  X   Give job the name X
 -t  X   Limit run time to X hrs (default=2)
 -y      Prepend command with a call to yod
"""

import os,getopt,sys

template = """\
#!/bin/bash
#
#PBS -l walltime=%d:0:0
#PBS -l size=%d
#PBS -q default
#PBS -N %s
#
cd %s
%s
"""

yodcmd = '/cplant/bin/yod'
fname = 'qsub.dat'

def qsubstr(name,cmd,hrs,nproc,dir):
    return template % (hrs,nproc,name,dir,cmd)


def main():
    opts,args = getopt.getopt(sys.argv[1:],'hn:N:t:y')

    doyod = 0
    nproc = 1
    dir = os.getcwd()
    hrs = 2
    name = 'qsub_rpm'

    for key,value in opts:
        if key == '-h':
            print __doc__
            sys.exit()
        elif key == '-n': nproc = int(value)
        elif key == '-N': name = value
        elif key == '-y': doyod = 1
        elif key == '-t': hrs = int(value)

    cmd = args[0]

    if doyod: cmd = "%s -sz %d %s" % (yodcmd,nproc,cmd)

    qstr = qsubstr(name,cmd,hrs,nproc,dir)
    file = open(fname,'w').write(qstr)
    os.system('qsub %s' % fname)
    return    

if __name__ == '__main__': main()

