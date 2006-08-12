#!/usr/bin/env python
"""\
 Backup.py - Back up one directory tree to another

 This does not delete any files, or alter the src tree in any way,
 it merely insures that the dest tree has everything in it that the
 src tree does.

 If the file ~/.do_backup_skip_dirs exists, the program will attempt
 to load directory trees to skip into a skip_list. If directories
 are encountered during the backup that match a directory in this
 list, the entire tree will be skipped. This is useful for ignoring
 internet cache files and the like.

 The program writes all log information to ~/.do_backup_log. If
 this file cannot be created with write access, the program prints
 logfile information to sys.stdout.

 See also: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/191017

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import os,shutil,sys
VERBOSE = 1

# consider oppening 'append', if you want to save old logfiles.
try:
    logfile = open(os.path.expanduser('~/.do_backup_log'),'w')
except:
    # fallback to stdout if for some reason you can't create the logfile
    logfile = sys.stdout

skip_dirs = []
if os.path.exists(os.path.expanduser('~/.do_backup_skip_dirs')):
    logfile.write('Loading information from skip_dirs:\n')
    for line in open(os.path.expanduser('~/.do_backup_skip_dirs')):
        dirname = line.strip()
        logfile.write("Adding file %s to skip_dirs\n" % dirname)
        skip_dirs.append(dirname)

# getmtime returns the seconds from the epoch when the file was last
#  accessed, hence the larger value corresponds to the newer file.
def isnewer(a,b): return os.path.getmtime(a) > os.path.getmtime(b)

def backup(source,dest):
    if not os.path.exists(dest):
        if VERBOSE: logfile.write("Creating %s \n" % dest)
        os.mkdir(dest)
    if source in skip_dirs:
        logfile.write("Skipping directory tree %s\n" % source)
        return
    for file in os.listdir(source):
        abssource = os.path.abspath(os.path.join(source,file))
        absdest = os.path.abspath(os.path.join(dest,file))
        if os.path.isfile(abssource):
            # check mtimes and copy if needed
            if not os.path.exists(absdest) or isnewer(abssource,absdest):
                if VERBOSE:
                    logfile.write("Copying %s -> %s \n" % (abssource,absdest))
                shutil.copy(abssource,absdest)
        elif os.path.isdir(abssource):
            # check to make sure directory exists first
            if not os.path.exists(absdest):
                os.mkdir(absdest)
                if VERBOSE: logfile.write("Creating %s \n" % absdest)
            backup(abssource,absdest)
        else:
            # I don't think we should ever be here, but
            #  just in case...
            # We actually end up here for symlinks, but I haven't decided
            #  what do to with them. Oddly enough, symlinks to directories
            #  are actually followed, which makes it easy to create
            #  infinite loops via:
            #  % ln -s ./ dirname
            #  and since "dirname" now points to itself, it will be
            #  followed. I'm going to need to treat this situation
            #  explicitly. Right now I just manually delete the
            #  symlinks that point to themselves.
            if VERBOSE:
                logfile.write("Unhandled file type (probably symlink): %s\n" %\
                              abssource)
    return

        
        
