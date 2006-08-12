#!/usr/bin/env python
"""\
 Tex2Img.py  Convert LaTeX equations into a PNG image

 Much credit is due to Nikos Drakos' pstogif.pl
  and John Walker's textogif PERL programs.

 Requirements: ghostscript (gs), pnmcrop, ppmtogif, ee. Has only been
 tested on Linux thus far, and significant hacking is probably
 necessary to run on Windows. Could all probably be rewritten with the
 Python Imaging Library, but I haven't done that yet.

 Version history:
 2/11/02    Version 0.1 written.
 10/12/02   Version 0.2: Put in documentation regarding the
              viewer: ee is a different program under Debian
 
Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import string,os,sys
from Tkinter import *

# This should be a valid viewer command:
VIEWER='display' # ImageMagick's display function
#VIEWER='ee' #Normal electronic eyes command
#VIEWER='eeyes' # Debian's version of ee
#VIEWER='xv' #Some people like xv

VERBOSE=0

header = """\
\documentclass[12pt]{article}
\pagestyle{empty}
\\begin{document}
\\begin{displaymath}
"""

footer = """\
\end{displaymath}
\end{document}
"""

dpi = 150
res = 0.5

class tk_converter:
    def __init__(self):
        self.make_widgets()
        return

    def make_widgets(self):
        self.top = Frame()
        self.top.pack()
        Label(self.top,text="LaTeX 2 GIF").pack(side=TOP)
        self.entry = Entry(self.top,width=20)
        self.entry.pack(side=TOP)
        self.resframe = Frame(self.top).pack(side=TOP)
        Label(self.resframe,text="Size").pack()
        self.size = Entry(self.resframe,width=10)
        self.size.pack()
        self.size.insert(0,'150')
        Label(self.resframe,text="Scaling").pack()
        self.scaling = Entry(self.resframe,width=10)
        self.scaling.pack()
        self.scaling.insert(0,'1')
        self.buttonframe = Frame(self.top).pack(side=TOP)
        self.display = Button(self.buttonframe,text="Display",
                              command=self.convert).pack(side=LEFT)
        self.save = Button(self.buttonframe,text="Save",
                           command=self.save).pack(side=LEFT)
        self.quit = Button(self.buttonframe,text="Quit",
                           command=sys.exit).pack(side=LEFT)
        self.top.mainloop()
        return

    def convert(self):
        size = int(self.size.get())

        scaling = float(self.scaling.get())
        if scaling < 1:
            scaling = 1
        elif scaling > 2:
            scaling = 2

        latexstring = self.entry.get()
        latex2ps(latexstring)
        ps2gif(size,scaling)
        os.system('%s temp.gif' % VIEWER)
        cleanup()
        return

    def save(self):
        from tkFileDialog import asksaveasfilename
        filename = asksaveasfilename(filetypes=[("GIF","*.gif")])
        os.rename('temp.gif',filename)
        return

def latex2ps(latexstring):
    if VERBOSE: print "Translating ", latexstring
    f = open('temp.tex','w')
    f.write('%s' % header)
    f.write('%s\n' % latexstring)
    f.write('%s\n' % footer)
    f.close()

    os.system('latex temp.tex')
    os.system('dvips -f temp.dvi > temp.ps')
    return

def ps2gif(size,scaling=1.):
    ps2ppm(size,scaling)
    ppm2gif(scaling)

def ps2ppm(size,scaling=1.):
    gs = os.popen("gs -q -dNOPAUSE -dNO_PAUSE -sDEVICE=ppmraw -r%d "
                  "-sOutputFile=temp.ppm temp.ps" % int(size*scaling),"w")
    gs.close()
    return

def ppm2gif(scaling=1.):
    invscale = 1.0/scaling
    #os.system("pnmcrop temp.ppm "
    #          "| ppmtogif -interlace -transparent rgb:b2/b2/b2 > temp.gif")
    os.system("pnmcrop temp.ppm | pnmscale %f "
              "| ppmtogif -interlace -transparent rgb:b2/b2/b2 > temp.gif"
              % invscale)
    # This version has optional scaling, but I haven't activated that yet
    #os.system("pnmcrop temp.ppm | pnmgamma 1.0 | ppmdim 0.7 | pnmscale 0.75 "
    #          "| ppmtogif -interlace -transparent rgb:b2/b2/b2 > temp.gif")
    return

def cleanup():
    for filename in ["temp.ppm","temp.aux",
                     "temp.dvi","temp.log","temp.ps","temp.tex"]:
        os.unlink(filename)
    return

def cli_main():
    import getopt
    global VERBOSE
    opts,args = getopt.getopt(sys.argv[1:],'r:hv')

    size=150
    for (key,value) in opts:
        if key == '-h':
            print __doc__
            sys.exit()
        if key == '-r': size = int(value)
        if key == '-v': VERBOSE = 1

    latexstring = string.join(args,' ')
    latex2ps(latexstring)
    ps2gif(size)
    cleanup()
    return
