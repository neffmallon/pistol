#!/usr/bin/env python
"Makes a DOT graph diagram out of a fortran call tree"

import sys,re

def fcall(files):
    progpat = re.compile('\s*program\s*(\w+)\s*.*',re.I)
    subpat = re.compile('\s*subroutine\s*(\w+)\s*\(.*',re.I)
    callpat = re.compile('\s*call\s*(\w+)\s*\(.*',re.I)
    ftree = {}
    for file in files:
        progname = None
        callname = None
        for line in open(file):
            if subpat.match(line):
                progname = subpat.match(line).groups()[0]
            if callpat.match(line):
                callname = callpat.match(line).groups()[0]
                if progname:
                    if not ftree.has_key(progname):
                        ftree[progname] = {}
                    if not ftree[progname].has_key(callname):
                        ftree[progname][callname] = 1
            if progpat.match(line): 
                progname = progpat.match(line).groups()[0]

    print "digraph ftree {"
    for progname in ftree.keys():
        for callname in ftree[progname].keys():
            print "     \"%s\" -> \"%s\";" % (progname,callname)
    print "}"
    return

if __name__ == '__main__': fcall(sys.argv[1:])
        
