#!/usr/bin/env python
"""\
 qhist2xyz.py - Get the xyz coordinates from the history file and convert
   to xyz file format.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import sys
from Pistol.SeqQuest import read_hist,write_xyz

# TO DO:
# Consider using Pistol.XYZ

VERBOSE=1

for filename in sys.argv[1:]:
    if VERBOSE: print "Converting ",filename
    xyzname = filename.replace('hist','xyz')
    results = read_hist(filename)
    write_xyz(xyzname,results['geos'])

    
