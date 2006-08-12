#!/usr/bin/env python
"""\
 Run a ReaxFF MD Simulation

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
 """

import sys
from Pistol.ReaxFF import run
apply(run,sys.argv[1:])


