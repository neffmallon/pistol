#!/usr/bin/env python
"""\
 rereplace.py - Make a series of replacements to a string using
   regular expression matches.
"""

import re

def test():
    string = 'abcdefghijklmnop'
    print string.replace('b*c','XX')
    print re.sub('b*d','XX',string)
    print rereplace([('b*d','XX'),('jkl.*p','')],string)
    print rereplace([('0*0 ','0 ')],'0000 0000 ')
    print rereplace([('-',' -'),('^ *',''),('e -','e-')],'-1234-567e-8')
    return

def rereplace(reps,string):
    for pat,sub in reps: string = re.sub(pat,sub,string)
    return string

if __name__ == '__main__': test()


