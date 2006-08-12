#!/usr/bin/env python
"""\
 Extract the geometry from a Quest output file in XYZ format

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import sys
from Pistol.SeqQuest import read_output, write_xyz

# To Do:
# Consider using Pistol.XYZ for the write function

VERBOSE=1

for filename in sys.argv[1:]:
    if VERBOSE: print "Converting ",filename
    xyzname = filename.replace('out','xyz')
    results = read_output(filename)
    write_xyz(xyzname,results['geos'])

