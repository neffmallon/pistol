#!/usr/bin/env python
"""\
 cols2csv.py - Turn a set of space delimited columns into comma delimited
 columns that can be imported into a speadsheet.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import sys
for line in sys.stdin: print ','.join(line.split())

