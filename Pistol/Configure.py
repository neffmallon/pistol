#!/usr/bin/env python
"""\
 Configure.py - Routines to build simple makefiles
"""

from os.path import splitext
from glob import glob

def Configure(files = None):
    endings = []
    objs = []
    LD = None
    if not files: files = glob('*.f') + glob('*.c') + glob('*.f90') \
                          + glob('*.cpp') + glob('*.CC') + glob(' *.c++')
    for file in files:
        root,ext = splitext(file)
        objs.append(root + '.o')
        if ext not in endings: endings.append(ext)
    print objs, endings
    if '.f' in endings: LD = 'g77'

    lines = []
    if LD: lines.append('LD = %s\n' % LD)
    lines.append('OBJ = ')
    llen = 0
    for oname in objs:
        if llen > 50:
            llen = 0
            lines.append('\\\n\t')
        lines.append(oname)
        lines.append(' ')
        llen += len(oname) + 1
    lines.append('\n')
    lines.append('exe : $(OBJ)\n')
    lines.append('\t$(LD) $^ -o $@\n')
    open('makefile','w').writelines(lines)
    
    return

