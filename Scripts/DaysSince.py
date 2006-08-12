#!/usr/bin/env python
"Simple one-liner to compute the days since a date in the past"

from time import mktime,time

def days_since():
    mdy = raw_input("Enter date mm/dd/yyyy :")
    month,day,year = map(int,mdy.split('/'))
    if year < 10: year += 2000
    elif year < 100: year += 1900
    elif year < 1900: raise "Can't decipher year %d" % year
    if month > 12 or month < 1: raise "Can't decipher month %d" % month
    if day < 1 or day > 31: raise "Can't decipher day %d" % day
    secs1 = mktime((year,month,day,-1,-1,-1,-1,-1,-1))
    secs2 = time()
    dsecs = secs2-secs1
    print "Days Since = ",int(dsecs/3600/24)
    return

if __name__ == '__main__': days_since()

