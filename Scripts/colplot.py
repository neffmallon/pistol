#!/usr/bin/env python
"""
 colplot.py - Plot a data file consisting of separate data in columns.

 Options:
 -h     Print this help file
 -X     Use the first column for the x-axis values. Otherwise the
        data are plotted against the overall index.
 -t str Use str as the title
 -x str Use str as the xlabel
 -y str Use str as the ylabel

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import re,Numeric,sys,getopt

def colplot_gnuplot(fname,xvals,title=None,xlabel=None,ylabel=None):
    import Gnuplot
    skippat = re.compile('^#')
    cols = None

    # reading from stdin isn't working for some reason, I think because
    #  the program relies on the file existing on the disk
    if fname:   file = open(fname)
    else:       file = sys.stdin

    for line in file:
        if not line: break
        if skippat.search(line): continue
        vals = map(float,line.split())
        if not cols:
            cols = []
            for val in vals: cols.append([val])
        else:
            for i in range(len(vals)): cols[i].append(vals[i])

    g = Gnuplot.Gnuplot()
    ncols = len(cols)
    nrows = len(cols[0])
    if xvals:
        x = cols[0]
        ys = range(1,ncols)
    else:
        x = range(1,nrows+1)
        ys = range(ncols)

    ds = []
    for i in ys:
        ds.append(Gnuplot.Data(x[:len(cols[i])],cols[i],with='lines'))

    if not title: title = 'Data from file %s' % fname
    g.title(title)
    if xlabel: g.xlabel(xlabel)
    if ylabel: g.ylabel(ylabel)
    apply(g.plot,ds)
    g('set term png color')
    g('set output \'colplot.png\'')
    g.replot()
    g('set term post')
    g('set output \'colplot.eps\'')
    g.replot()
    raw_input('Press return to continue')
    
    return

def colplot_biggles(fname,xvals,title=None,xlabel=None,ylabel=None):
    import biggles
    
    skippat = re.compile('^#')
    cols = None

    if fname:   file = open(fname)
    else:       file = sys.stdin

    for line in file:
        if not line: break
        if skippat.search(line): continue
        vals = map(float,line.split())
        if not cols:
            cols = []
            for val in vals: cols.append([val])
        else:
            for i in range(len(vals)): cols[i].append(vals[i])

    g = biggles.FramedPlot()
    if title: g.title = title
    if xlabel: g.xlabel = xlabel
    if ylabel: g.ylabel = ylabel
    

    ncols = len(cols)
    nrows = len(cols[0])
    if xvals:
        x = cols[0]
        ys = range(1,ncols)
    else:
        x = range(1,nrows+1)
        ys = range(ncols)

    print x
    print ys

    ds = []
    for i in ys: g.add(biggles.Curve(x,cols[i]))
    g.show()
    g.write_img(400,400,'colplot.png')
    g.write_eps('colplot.eps')

    return

colplot = colplot_biggles

if __name__ == '__main__':
    opts,args = getopt.getopt(sys.argv[1:],'hXt:x:y:')
    xval = 0
    title = None
    xlabel = None
    ylabel = None
    for key,val in opts:
        if key == '-h':
            print __doc__
            sys.exit()
        if key == '-X': xval = 1
        if key == '-t': title = val
        if key == '-x': xlabel = val
        if key == '-y': ylabel = val
        

    if not args:
        colplot(None,xval,title,xlabel,ylabel)
    else:
        for fname in args: colplot(fname,xval,title,xlabel,ylabel)

    
    
