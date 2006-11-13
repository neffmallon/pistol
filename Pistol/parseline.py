#!/usr/bin/env python

def parseline(line,format):
    xlat = {'x':None,'s':str,'f':float,'d':int,'i':int}
    result = []
    words = line.split()
    for i in range(len(format)):
        f = format[i]
        trans = xlat.get(f,None)
        if trans: result.append(trans(words[i]))
    if len(result) == 0: return None
    if len(result) == 1: return result[0]
    return result
