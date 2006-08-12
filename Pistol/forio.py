#!/usr/bin/env python
"""\
 forio.py - Fortran Formated IO
 
 Read/write using Fortran format strings. This doesn't handle everything
 but is designed to handle a large subset of the read/write formats found
 in computational chemistry io

 TODO:
 - The subtle differences between FDG are not handled properly. Reading
   is probably fine, but writing is not
"""

import re
from string import strip

fsplit_pat = re.compile("(\d*)([iIfFgdDGaAxX])(\d*)\.?(\d*)")

def double(str): return float(str.replace('d','e'))

readers = {
    'i':int, 'I':int,
    'f':float, 'F':float,
    'd':double, 'D':double,
    'g':double, 'G':double,
    'a':strip, 'A':strip,
    'x':None, 'X':None
    }

writers = {
    'i': "%ii", 'I': "%ii",
    'f': "%i.%if", 'F': "%i.%if",
    'd': "%i.%ie", 'D': "%i.%ie",
    'g': "%i.%ig", 'G': "%i.%ig",
    'a': "-%is", 'A': "-%is"
    }

def int_default(val,default):
    if val: return int(val)
    return default        

def format_parse_one(fterm):
    "Split a fortran format term into its pieces"
    mult,type,width,precision = fsplit_pat.findall(fterm)[0]
    mult = int_default(mult,1)
    width = int_default(width,1)
    precision = int_default(precision,0)
    return mult,type,width,precision

def fortran_format_parse(format):
    "Split a fortran format into its pieces"
    forms = []
    for term in format.split(","):
        mult,type,width,precision = format_parse_one(term)
        for i in range(mult): forms.append((type,width,precision))
    return forms

def read(line,format):
    terms = format.split(',')
    vals = []
    istart = 0
    line_length = len(line)
    for type,width,precision in fortran_format_parse(format):
        iend = istart + width
        if iend > line_length: break
        if readers[type]: vals.append(readers[type](line[istart:iend]))
        istart = iend
    return vals

def write(vals,format):
    line = []
    fformats = fortran_format_parse(format)
    for i in range(len(vals)):
        val = vals[i]
        type,width,precision = fformats.pop(0)
        while 1: # Hack that lets us write lines with "x"'s in them
            if type == 'x' or type == 'X':
                line.append(' '*width)
                type,width,precision = fformats.pop(0)
            else:
                break                
        if precision:
            format = "%" + writers[type] % (width,precision)
        else:
            format = "%" + writers[type] % width
        line.append(format % val)        
    return ''.join(line)

def test():
    print fortran_format_parse("2i5")
    print fortran_format_parse("i5,i5,f10.5")
    vals = read("   1   2   3   4   5   6   7   8",
                "i4,i4,i4,i4,i4,i4,i4")
    print vals
    print write(vals,"7f10.6")

    #Format from Biograf file:
    bgf = "HETATM     1 C1    RES A  444    4.01776   5.51776"\
          "   5.81776 C_R    3 0  0.00000"
    bgf_fmt = "a6,1x,i5,1x,a5,1x,a3,1x,a1,1x,a5,"\
              "3f10.5,1x,a5, i3,i2,1x,f8.5"

    print fortran_format_parse(bgf_fmt)
    print bgf
    vals = read(bgf,bgf_fmt)
    print vals
    print write(vals,bgf_fmt)

    # Examples from Konrad's FortranFormat file:
    print read('   59999','2I4')
    print write([3.1415926, 2.71828],'2D15.5')
    return

if __name__ == '__main__': test()
