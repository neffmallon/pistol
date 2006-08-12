#!/usr/bin/env python
"""\
 Backup important files in the home directory. This file used to be
 a front end for the Pistol.Backup features, but that turned out to
 be too limited for me, so I've created this routine.
"""

import sys,os,time,getopt

doall = 0

# See if we have command-line arguments
if len(sys.argv) > 1:
    opts,args = getopt.getopt(sys.argv[1:],'a')
    for key,val in opts:
        if key == '-a': doall = 1


Always = ['Documents','emacs','Programs','Public','Python','rpminfo']

Sometimes = ['Classes','Library','PaperArchive','Pictures',
             'Presentations','ThomasFermi',
             'gallery','hedm','hydrogen','porf',]

root = os.path.join("/Volumes/rmuller/rmuller/Mac.Backup",
                    time.strftime('Arch-%Y-%m-%d'))

if not os.path.exists(root): os.makedirs(root)

home = os.environ['HOME']
os.chdir(home)

if doall: Files = Always+Sometimes
else: Files = Always

for file in Files:
    ofname = os.path.join(root,file+".tgz")
    command = 'tar czf %s %s' % (ofname,file)
    if os.path.exists(file):
        os.system(command)
        print command
    else:
        print "\nExpected directory %s doesn't exist" % ifname,
    

