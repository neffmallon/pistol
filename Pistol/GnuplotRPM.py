#!/usr/bin/env python
"""\
GnuplotRPM.py  Rick's version of the Gnuplot module to work on all
platforms. There are occasional differences from the Harvard version.

This was a version of a Gnuplot driver that I wrote because originally
the standard (now at http://gnuplot-py.sf.net) driver wasn't robust
enough. This has been corrected, and this code is only included for
reference.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import os,sys

class Gnuplot:
    def __init__(self):
        if sys.path == 'win32':
            self.path_to_gnuplot = "C:\\Gnuplot3.7\\wgnuplot.exe"
        else: #add additional options later
            self.path_to_gnuplot = "gnuplot"
        self.option_list = ["set nokey"]
        self.post_option_list = []
        self.cols = [(1,2)]
        self.gnu_filename = "gnuplot.gnu"
        self.dat_filename = "gnuplot.dat"
        return

    def __call__(self,option_str):
        self.option_list.append(option_str)
        return

    def scrub(self):
        "Delete temporary files"
        os.unlink(self.gnu_filename)
        os.unlink(self.dat_filename)
        return

    def ps_hardcopy(self,filename):
        self.post_option_list.append("set term post")
        self.post_option_list.append("set output %s" % filename)
        self.post_option_list.append("replot")
        return
    
    def gif_hardcopy(self,filename):
        self.post_option_list.append("set term gif")
        self.post_option_list.append("set output '%s'" % filename)
        self.post_option_list.append("replot")
        return
    
    def title(self,title_str):
        self.option_list.append("set title '%s'" % title_str)
        return
    
    def xlabel(self,xlabel_str):
        self.option_list.append("set xlabel '%s'" % xlabel_str)
        return

    def ylabel(self,ylabel_str):
        self.option_list.append("set ylabel '%s'" % ylabel_str)
        return

    def set_cols(self,col_list):
        "Define the columns to plot; think about labeling later"
        self.cols = col_list
        return

    def plot(self,data_list):
        "2d plot. Columns defined in self.cols."
        self.write_gnufile()
        self.write_datfile(data_list)
        os.system("%s %s" % (self.path_to_gnuplot, self.gnu_filename))
        return
    
    def write_gnufile(self):
        gnufile = open(self.gnu_filename,'w')
        for str in self.option_list:
            gnufile.write(str + '\n')
        gnufile.write("plot ")
        for col in self.cols:
            gnufile.write("'%s' using %d:%d" %
                          (self.dat_filename,col[0],col[1]))
            if col != self.cols[-1]:
                gnufile.write(", ")
            else:
                gnufile.write("\n")
        gnufile.write("pause -1\n")
        for str in self.post_option_list:
            gnufile.write(str + '\n')
        gnufile.close()
        return

    def write_datfile(self,data_list):
        datfile = open(self.dat_filename,'w')
        for datum in data_list:
            for dat in datum:
                datfile.write("%f " % dat)
            datfile.write("\n")
        datfile.close()
        return

if __name__ == '__main__':
    g = Gnuplot()
    g.title("Test Plot")
    g("set data style linespoints")
    g.plot([(0,1.),(1,2.),(2,3.),(3,2.),(4,2.),(5,1.)])
    
