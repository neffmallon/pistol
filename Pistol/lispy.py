#!/usr/bin/env python
"""\
 lispy - a simple LISP evaluator in Python. Currently only evaluates
 lisp trees, but will be extended to include lambdas, defines,
 variables, etc.
"""

import math

# Types
inttype = type(0)
floattype = type(1.)
listtype = type([])

# Utilities
def split(list): return list[0],list[1:]
def numeric_type(arg): return (type(arg) == inttype or type(arg) == floattype)
def empty(arg): return (arg == [] or arg == ())

def list_type(arg): return type(arg) == listtype

# Basic operators
def plus(a,b): return teval(a)+teval(b)
def minus(a,b): return teval(a)-teval(b)
def prod(a,b): return teval(a)*teval(b)
def div(a,b): return teval(a)/teval(b)
def sqrt(a): return math.sqrt(teval(a))
def exp(a): return math.exp(teval(a))

def vplus(*args): # for arbitrary elements
    if empty(args): return 0
    head,tail = split(args)
    return head + apply(plus,tail)

def teval(arg): # Evaluate lisp operator trees
    if numeric_type(arg): return arg
    elif empty(arg): return 0
    head, tail = split(arg)
    return apply(head,tail)

def test():
    # 1+1=2
    print teval([plus,1,1])
    # Pythagorean theorem; works for tuples and lists
    print teval([sqrt, [plus, (prod,3,3), [prod,4,4]]])

if __name__ == '__main__': test()
