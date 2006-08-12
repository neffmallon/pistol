#!/usr/bin/env python
"""\
 Split a SDB trainingset file into its individual structures
 Usage: sdbsplit.py <files>
"""

import sys, re

DEBUG = 1

def sdbsplit(fnames):
    for fname in fnames:
        lines = open(fname).read()
        files = lines.split('@structure')
        if DEBUG: print "Total of %d files found" % len(files)
        for file in files:
            if not file: continue #skip empty string
            name = get_struct_name(file)
            name = name + '.sdb'
            if not name:
                if DEBUG: print "Warning: name = ",name
                continue
            print "Writing file %s" % name
            open(name,'w').write(file)
    return

def get_struct_name(file):
    structpat = re.compile('start struct')
    lines = file.split('\n')
    for i in range(len(lines)):
        line = lines[i]
        if structpat.search(line):
            next = lines[i+1]
            return next.strip()
    else:
        print "Warning, end of file found"
    return None

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print __doc__
        sys.exit()
    sdbsplit(sys.argv[1:])

