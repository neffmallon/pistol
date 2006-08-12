#!/usr/bin/env python
"""\
 Do a quick cleanup of a Quest directory

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""


import glob,os

files = glob.glob('lcao.*') + glob.glob('core.*')
for name in ['lcao.x','lcao.in','lcao.vxyz']:
    if name in files: files.remove(name)

for file in files: os.unlink(file)
