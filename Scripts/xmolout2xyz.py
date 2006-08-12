#!/usr/bin/env python
"""\
 Convert the ReaxFF xmolout output file to a standard xyz file.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

from Pistol.XYZ import read,write

import os

if os.path.exists('xmolout'):
    print "Converting ReaxFF xmolout file to traj.xyz"
    geos = read('xmolout')
    write('traj.xyz',geos)
else:
    print "No ReaxFF trajectory file xmolout found"


