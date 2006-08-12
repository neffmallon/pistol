#!/usr/bin/env python
"""\
 run_seqquest.py - Lightweight interface to the Quest routines

 Options:
 -h         Print this help message
 -a  <dir>  Use <dir> as the directory in which to find the atoms
 -k         Keep: do not purge the scratch directory after the run
 -x  <exe>  Use <exe> as the seqquest executable
 -s         Setup only: copy files and links, but don't run

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

from Pistol.SeqQuest import default_atomdir, default_seqquestexe,\
     seqquest,setup

import getopt,sys

opts,args = getopt.getopt(sys.argv[1:],'ha:x:sk')


atomdir = default_atomdir
seqquestexe = default_seqquestexe
dosetup = 0
keep = 0

for (key,value) in opts:
    if key == '-h':
        print __doc__
        sys.exit()
    elif key == '-a':
        atomdir = value
    elif key == '-x':
        seqquestexe = value
    elif key == '-s': # only do the setup part
        dosetup = 1
    elif key == '-k':
        keep = 1

for filename in args:
    if dosetup:
        startdir,atomlist = setup(filename,atomdir,seqquestexe)
    else:
        results = seqquest(filename,atomdir,seqquestexe,keep=keep)
        print results['energy']
    # endif
# end for

