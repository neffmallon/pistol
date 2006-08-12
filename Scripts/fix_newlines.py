#!/usr/bin/env python
"""\
NAME
    fix_newlines.py  --  fix the new lines in a file between different
                         conventions (unix, max, windows).

SYNOPSIS
    fix_newlines.py filename [file2 file3 ...]

DESCRIPTION
    Warning: overwrites original file.

    Inputs the file, uses the Python string library to split
    it into lines, and then outputs again. Relies on Python's
    platform localization to do the right thing with newlines,
    which may or may not work
"""

import sys
if len(sys.argv) < 2:
    print __doc__
    sys.exit()

for fname in sys.argv[1:]:
    lines = open(fname).readlines()
    open(fname,'w').writelines(lines)

