#!/usr/bin/env python
"""\
 hpcalc.py - A simple stack-based calculator a la HP

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. See the LICENSE file for licensing details.
"""

import math,sys

# These operations are defined in terms of the active stack

# Binary operations
def plus(stack): stack.append(stack.pop()+stack.pop())
def prod(stack): stack.append(stack.pop()*stack.pop())
# have to get the order right on the following two:
def minus(stack):
    x,y = stack.pop(),stack.pop()
    stack.append(y-x)
def div(stack): 
    x,y = stack.pop(),stack.pop()
    stack.append(y/x)
def pow(stack):
    x,y = stack.pop(),stack.pop()
    stack.append(math.pow(y,x))

# Unary operations
# Use degrees for trigonometric functions
def torad(x): return x*math.pi/180.
def todeg(x): return x*180./math.pi
def sin(stack):  stack.append(math.sin(torad(stack.pop())))
def cos(stack):  stack.append(math.cos(torad(stack.pop())))
def tan(stack):  stack.append(math.tan(torad(stack.pop())))
def asin(stack): stack.append(todeg(math.asin(stack.pop())))
def acos(stack): stack.append(todeg(math.acos(stack.pop())))
def atan(stack): stack.append(todeg(math.atan(stack.pop())))

def exp(stack): stack.append(math.exp(stack.pop))
def sqrt(stack): stack.append(math.sqrt(stack.pop))

# Nonary operations
def exit(stack): sys.exit()

def pprint(stack):
    for i in stack: print "  %f" % i
    return

funcmap = {
    '+' : plus,
    '-' : minus,
    '*' : prod,
    '/' : div,
    'pow' : pow,
    'sin' : sin,
    'cos' : cos,
    'tan' : tan,
    'asin' : asin,
    'acos' : acos,
    'atan' : atan,
    'exp' : exp,
    'sqrt' : sqrt,
    'exit' : exit,
    'x' : exit
    }

def main():
    stack = []
    while 1:
        pprint(stack)
        oper = raw_input('hpc>')
        if oper in funcmap.keys():
            funcmap[oper](stack)
        else:
            stack.append(float(oper))

if __name__ == '__main__': main()
    


