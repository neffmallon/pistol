#!/usr/bin/env python

import os
from pylab import *
from datetime import date

data = """\
#Date        Pounds
5/6/2006  ,    180
5/7/2006  ,    178
5/8/2006  ,    176
5/9/2006  ,    175
5/10/2006 ,    174
5/11/2006 ,    174
5/12/2006 ,    173
5/13/2006 ,    174
5/14/2006 ,    174
5/15/2006 ,    175
5/16/2006 ,    175
5/17/2006 ,    172
5/18/2006 ,    170
5/19/2006 ,    170
5/20/2006 ,    170
5/21/2006 ,    173
5/22/2006 ,    174
5/23/2006 ,    170
5/24/2006 ,    169
5/25/2006 ,    168
5/26/2006 ,    167
5/27/2006 ,    167
5/28/2006 ,    168
5/29/2006 ,    169
5/30/2006 ,    170
5/31/2006 ,    167
6/1/2006  ,    166
6/2/2006  ,    165
6/3/2006  ,    163
6/4/2006  ,    163
6/5/2006  ,    163
6/6/2006  ,    162
6/7/2006  ,    162
6/8/2006  ,    162
6/9/2006  ,    162
6/10/2006 ,    160
6/11/2006 ,    160
6/12/2006 ,    159
6/13/2006 ,    158
6/14/2006 ,    157
6/15/2006 ,    156
6/16/2006 ,    155
6/17/2006 ,    155
6/18/2006 ,    155
6/19/2006 ,    155
6/20/2006 ,    155
6/21/2006 ,    155
6/22/2006 ,    156
6/23/2006 ,    156
6/24/2006 ,    155
6/25/2006 ,    157
6/26/2006 ,    157
6/27/2006 ,    158
6/28/2006 ,    155
6/29/2006 ,    156
6/30/2006 ,    159
7/1/2006  ,    159
7/3/2006  ,    161
7/4/2006  ,    159
7/5/2006  ,    157
7/6/2006  ,    155
7/7/2006  ,    155
7/8/2006  ,    155
7/9/2006  ,    155
7/10/2006 ,    155
7/11/2006 ,    154
7/12/2006 ,    154
7/13/2006 ,    153
7/14/2006 ,    152
7/15/2006 ,    154
7/16/2006 ,    152
7/17/2006 ,    153
7/18/2006 ,    152
7/19/2006 ,    152
7/20/2006 ,    152
7/21/2006 ,    152
7/22/2006 ,    153
7/23/2006 ,    152
7/24/2006 ,    154
7/25/2006 ,    153
7/26/2006 ,    150
7/27/2006 ,    150
7/28/2006 ,    150
7/29/2006 ,    150
7/30/2006 ,    154
7/31/2006 ,    154
8/1/2006  ,    152
8/2/2006  ,    152
8/3/2006  ,    151
8/4/2006  ,    150
8/5/2006  ,    154
8/6/2006  ,    154
8/7/2006  ,    154
8/8/2006  ,    152
8/9/2006  ,    150
8/10/2006 ,    150
8/11/2006 ,    149
"""

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

    if fname:
        days,weights = parsefile(fname)
    else:
        days,weights = parse(data)
    
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

if __name__ == '__main__': main(fname="/Users/rmuller/Desktop/shangrila.csv")



