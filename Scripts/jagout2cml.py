#!/usr/bin/env python
"""\
 Convert Jaguar output to a CML geometry file.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import sys,re
from Pistol import Jaguar,CML

for filename in sys.argv[1:]: 
    geos = Jaguar.read_output(filename)
    CML.write(filename.replace('.out','.cml'),geos)
