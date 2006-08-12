#!/usr/bin/env python
"""\
 NAME
   qout_md_summary.py - Summarize MD energies and temperatures from Quest MD Run

 USAGE
   qout_md_summary.py <quest output file>

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import re,sys, getopt

def main_gnuplot(file,title=None):
    import Gnuplot
    epat = re.compile('E kin')
    tpat = re.compile('T in')

    epots = []
    etots = []
    temps = []

    for line in open(file):
        if not line: break
        if epat.search(line):
            words = line.split()
            epot,etot = map(float,words[5:7])
            epots.append(epot)
            etots.append(etot)
        elif tpat.search(line):
            words = line.split()
            T = float(words[4])
            temps.append(T)

    indices = range(len(epots))

    g = Gnuplot.Gnuplot()
    if title:
        g.title(title)
    else:
        g.title('Data from MD file %s' % file)
    g.xlabel('step')
    g.ylabel('E (Ry)')
    g('set y2label "Temp (K)"')
    g('set y2tics')
    d1 = Gnuplot.Data(indices,epots,title="Epot",with='lines')
    d2 = Gnuplot.Data(indices,etots,title="Etot",with='lines')
    d3 = Gnuplot.Data(indices,temps,title="Temp",axes="x1y2",with='lines')
    g.plot(d1,d2,d3)
    g('set term png color')
    g('set output \'summary.png\'')
    g.replot()
    g('set term post')
    g('set output \'summary.ps\'')
    g.replot()
    raw_input('press any key to continue')
    return

def main_biggles(file,title=None):
    import biggles
    epat = re.compile('E kin')
    tpat = re.compile('T in')

    epots = []
    etots = []
    temps = []

    for line in open(file):
        if not line: break
        if epat.search(line):
            words = line.split()
            epot,etot = map(float,words[5:7])
            epots.append(epot)
            etots.append(etot)
        elif tpat.search(line):
            words = line.split()
            T = float(words[4])
            temps.append(T)

    if len(epots) < 2:
        print "Not enough points yet"
        return
        
    indices = range(len(epots))


    t = biggles.FramedArray(2,1)
    v_t = biggles.Curve(indices,epots,color='red')
    v_t.label = 'V (h)'
    E_t = biggles.Curve(indices,etots,color='blue')
    E_t.label = 'E (h)'
    t[0,0].add(v_t)
    t[0,0].add(E_t)
    t[0,0].add(biggles.PlotKey(.1,.9,[v_t,E_t]))

    T_t = biggles.Curve(indices,temps,color='green')
    T_t.label = 'T (K)'
    t[1,0].add(T_t)
    t[1,0].add(biggles.PlotKey(.1,.9,[T_t]))
    t.xlabel = 'time step'
    t.title = '$Energy and Temperature vs. time$'
    
    t.show()
    t.write_img(400,400,"summary.png")
    #t.write_eps("summary.eps")
    return

main = main_biggles

if __name__ == '__main__':
    opts,args = getopt.getopt(sys.argv[1:],'t:')
    title = None
    for key,val in opts:
        if key == '-t': title = val
    main(args[0],title)
