#!/usr/bin/env python
"""\
 colfilter.py - select only certain columns from the output

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import sys

start = None
stop = None

if len(sys.argv) > 1: start = int(sys.argv[1])
if len(sys.argv) > 2: stop = int(sys.argv[2])

# yuk: can I reuse code a bit more?
if start and stop:
    for line in sys.stdin: print ' '.join(line.split()[start:stop])
elif start:
    for line in sys.stdin: print ' '.join(line.split()[start:])
else:
    for line in sys.stdin: print ' '.join(line.split())
    

