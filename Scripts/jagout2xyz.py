#!/usr/bin/env python
"""\
 Convert Jaguar output to XMol XYZ format.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import sys,re
from Pistol import Jaguar,XYZ

for filename in sys.argv[1:]: 
    geos = Jaguar.read_output(filename)
    XYZ.write(filename.replace('.out','.xyz'),geos)
