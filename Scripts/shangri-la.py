#!/usr/bin/env python

import os,sys
from pylab import *
from datetime import date

def year_adjust(year):
    if year < 50:
        year += 2000
    elif year < 100:
        year += 1900
    return year

def make_date(datestr):
    month,dom,year = map(int,datestr.split('/'))
    year = year_adjust(year)
    return date(year,month,dom)

def parse(textarea,**opts):
    days = []
    weights = []
    firstdate = None
    for line in textarea.splitlines():
        if not line: continue
        datestr,weight = line.split(',')
        try:
            dateobj = make_date(datestr)
        except:
            continue
        if not firstdate: firstdate = dateobj
        delta = dateobj-firstdate
        days.append(delta.days)
        weights.append(float(weight))
    return days,weights

def parsefile(fname): return parse(open(fname).read())

def main(**opts):
    do_weeklines = opts.get('do_weeklines',True)
    do_dotwlabels = opts.get('do_dotwlabels',False)

    fname = opts.get('fname',None)

    if not fname:
        if len(sys.argv) > 1:
            fname = sys.argv[1]
        elif os.path.exists('/Users/rmuller/Desktop/fm'):
            fname = '/Users/rmuller/Desktop/fm'
        else:
            raise "Can't find an input filename"
    days,weights = parsefile(fname)
        
    
    title("Weight loss under Shangri-La diet")
    xlabel("Days")
    ylabel("Pounds")
    plot(days,weights,'bo-')

    if do_dotwlabels:
        # to label with days of week
        labels = ['S','S','M','T','W','T','F']
        ndays = len(days)
        nweeks = ndays/7 + 1
        labels = (labels * nweeks)[:ndays]
        xticks(days,labels) 

    if do_weeklines:
        for day in days:
            if day > 0 and day % 7 == 0:
                axvline(x=day,color='k')

    show()
    return

if __name__ == '__main__': main()



