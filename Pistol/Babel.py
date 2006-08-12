#!/usr/bin/env python
"""\
NAME
   babel.py - Python front-end to OpenBabel library

SYNOPSIS
   babel.py ifilename ofilename
   babel.py -ifmt ifilename -ofmt ofilename

DESCRIPTION
   Use the OpenBabel library for file conversions. The python wrapper
   uses the file extension of the inputfile and outputfile as the
   keys to select the formats used.

   This program is currently a pretty brain-dead wrapper around the
   executable call. Later revisions will use a SWIG-wrapped library
   instead.

   There are two ways to call babel.py:

   babel.py ifilename ofilename
   babel.py -ifmt ifilename -ofmt ofilename

   If only ifilename and ofilename are supplied, the program gets
   the input and output formats from the extensions of ifilename and
   ofilename, respectively. Otherwise, the formats must be explicitly
   specified via -i and -o flags.

   You must choose one of these or the other, you can't mix styles.   

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import os,sys
babel_command = 'babel'

def exec_open_babel(ifmt,ifilename,ofmt,ofilename):
    os.system("%s -i%s %s -o%s %s" % (babel_command,ifmt,ifilename,
                                      ofmt,ofilename))
    return

def exec_open_babel_help():
    # Run the babel command without arguments to flag the help printout
    os.system("%s " % babel_command)
    return

def parse_input_line():
    if len(sys.argv) == 3:
        # assume: babel.py ifile.ifmt ofile.ofmt
        ifilename = sys.argv[1]
        ofilename = sys.argv[2]
        ifmt = os.path.splitext(ifilename)[1].replace('.','')
        ofmt = os.path.splitext(ofilename)[1].replace('.','')
    elif len(sys.argv) == 5:
        # assume: babel.py -ifmt ifile -ofmt ofile
        ifilename = sys.argv[2]
        ofilename = sys.argv[4]
        ifmt = sys.argv[1]
        ofmt = sys.argv[2]
    else:
        exec_open_babel_help()
        sys.exit()
    exec_open_babel(ifmt,ifilename,ofmt,ofilename)
    return

if __name__ == '__main__': parse_input_line()

    
