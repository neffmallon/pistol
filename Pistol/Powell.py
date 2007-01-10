#!/usr/bin/env python
"Powell's multidimensional minimization without derivatives"
# This doesn't work in multidimensions

from numpy import zeros,array,Float,identity
from copy import copy
from math import sqrt

VERBOSE = 0
DEFTOL = 1e-8     # Default tolerance for minimization
GOLD = 1.618304   # Golden mean ratio
CGOLD = 0.3819660
GLIMIT = 10.      # Limit of how far out to go
TINY = 1e-20      # Smallest denominator
MAXITERS = 100    # Maximum iterations

def Powell(func,point,disp=0.5,tol=DEFTOL):
    point = array(point,Float) # Make sure numpy array
    N = len(point)
    xi = identity(N,Float)
    #xi = array([[1.,1.],[1.,-1.]],Float)
    fret = func(point)
    print "evaluating func at point: ",point,fret
    pt = copy(point)
    for iter in range(MAXITERS):
        fp = fret
        ibig = 0
        delta = 0
        for i in range(N): # Minimize along each direction in xi
            xit = xi[i,:]
            print "minimizing along ",xit
            print "guess points: ",point, point+disp*xit
            fptt = fret
            point,fret = line_minimization(func,point,point+disp*xit)
            print "Found optimum at ",point
            if (fptt - fret) > delta:
                delta = fptt - fret
                ibig = i
        if 2*(fp-fret) <= tol*(abs(fp)+abs(fret))+TINY: break

        # construct extrapolated point
        ptt = 2*point - pt
        xit = point - pt
        pt = point
        fptt = func(ptt)
        if fptt < fp:
            t = 2*(fp-2*fret+fptt)*sqrt(fp-fret-delta)-delta*sqrt(fp-fptt)
            if t < 0:
                point, fret = line_minimization(func,point,point+disp*xit)
                xi[ibig,:] = xi[N-1,:]
                xi[N-1,:] = xit
    else:
        print "Warning: MAXITERS exceeded in Powell"
    #end for
    print "Powell converged after ",iter," iterations"
    return point,fret

def line_minimization(func,xa,xb,tol=DEFTOL):
    """Minimize function *func* along the line between *xa* and *xb*
    to within a tolerance of *tol*."""

    # Find three points xa,xb,xc that bracket the minimum of func
    xa,xb,xc = bracket_minimum(func,xa,xb,tol)

    print "Minimum bracketed by ",xa,xb,xc

    # Now use Brent's method to find the minimum
    #xa,fa = brent_minimize(func,xa,xb,xc,tol)
    # Or the golden section search
    xa,fa = golden_minimize(func,xa,xb,xc,tol)
    # I prefer the golden section search because I trust the
    #  algorithm more. It's also more stable for a wierd function.

    return xa,fa

def sign(a,b):
    "Sign of *b* times magnitude of *a*."
    if b < 0: return -abs(a)
    return abs(a)

def golden_minimize(func,xa,xb,xc,tol=DEFTOL):
    """Given three points *xa*, *xb*, and *xc* that bracket the minimum,
    find the minimum of function *func* via a Golden section search."""
    R = 0.61803399
    C = 1-R
    x0 = xa
    x3 = xc

    if abs(xc-xb) > abs(xb-xa):
        x1,x2 = xb,xb + C*(xc-xb)
    else:
        x2,x1 = xb,xb - C*(xb-xa)

    f1 = func(x1)
    f2 = func(x2)

    for iter in range(MAXITERS):
        if VERBOSE:
            print "Step ",iter," in golden minimization"
            print (x1,x2),(f1,f2)
        if abs(x3-x0) < tol*(abs(x1)+abs(x2)): break
        if f2 < f1:
            x0,x1,x2 = x1,x2,R*x1+C*x3
            f0,f1,f2 = f1,f2,func(x2)
        else:
            x3,x2,x1 = x2,x1,R*x2+C*x0
            f3,f2,f1 = f2,f1,func(x1)
    else:
        print "Warning: MAXITERS exceeded in golden_minimize"
    #end for
    print "Golden section search converged in ",iter," iterations"
    if f1 < f2: return x1,f1
    return x2,f2

def brent_minimize(func,xa,xb,xc,tol=DEFTOL):
    """Given three points *xa*, *xb*, and *xc* that bracket the minimum,
    find the minimum of function *func* via Brent's method."""

    a = min(xa,xc)
    b = max(xa,xc)
    v = xb
    w = v
    x = v
    e = 0.
    fx = func(x)
    fv = fx
    fw = fx
    for iter in range(MAXITERS):
        xm = 0.5*(a+b)
        tol1 = tol*abs(x)+tol # using zeps
        tol2 = 2*tol1
        if abs(x-xm) < tol2-0.5*(b-a): break
        if abs(e) > tol1:
            r = (x-w)*(fx-fv)
            q = (x-v)*(fx-fw)
            p = (x-v)*q-(x-w)*r
            q = 2*(q-r)
            if q > 0: p = -p
            q = abs(q)
            etemp = e
            e = d
            if abs(p) < abs(0.5*q*etemp) and \
               p > q*(a-x) and p < q*(b-x):
                d = p/q
                u = x+d
        if x <= xm:
            e = a - x
        else:
            e = b-x
        d = CGOLD*e
        if abs(d) >= tol1:
            u = x+d
        else:
            u = x+sign(tol1,d)
        fu = func(u)
        if fu <= fx:
            if u >= x:
                a = x
            else:
                b = x
            v = w
            fv = fw
            w = x
            fw = fx
            x = u
            fx = fu
        else:
            if u < x:
                a = u
            else:
                b = u
            if fu <= fw or w == x:
                v = w
                fv = fw
                w = u
                fw = fu
            elif fu <= fv or v == x or v == w:
                v = u
                fv = fu
    else:
        print "Warning: MAXITERS exceeded in brent_minimize"
    print "Brent converged in ",iter," iterations"
    return x,fx
    
def bracket_minimum(func,xa,xb,tol=DEFTOL):
    """Numerical Recipes algorithm for bracketing the minimum of function
    *func* along the line between *xa* and *xb*."""

    VERBOSE = 1
    fa = func(xa)
    fb = func(xb)
    if fb > fa: # Swap a & b so that we're moving downhill from a->b
        xa,xb = xb,xa
        fa,fb = fb,fa
    xc = xb + GOLD*(xb-xa)
    fc = func(xc)
    if VERBOSE: print "Bracket init points ",xa,fa,xb,fb,xc,fc
    for iter in range(MAXITERS):
        if VERBOSE:
            print "Step ",iter," in bracketing"
            print (xa,xb,xc),(fa,fb,fc)
        r = (xb-xa)*(fb-fc)
        q = (xb-xc)*(fb-fa)
        print "R,Q = ",r,q,q-r
        u = xb - ((xb-xc)*q - (xb-xa)*r)/(2.*sign(max(abs(q-r),TINY),q-r))
        ulim = xb + GLIMIT*(xc-xb)
        print "testing point ",u,func(u)

        if (xb-u)*(u-xc) > 0: # u btw b and c
            fu = func(u)
            if fu < fc: return xb,u,xc  
            elif fu > fb: return xa, xb, u
            u = xc + GOLD*(xc-xb)
        elif (xc-u)*(u-ulim) > 0: # u btw c and ulim
            fu = func(u)
            if fu < fc:
                xb,xc = xc,u
                u = xc + GOLD*(xc-xb)
                fb,fc = fc,fu
                fu = func(u)
        elif (u-ulim)*(ulim-xc) > 0: # limit u to max value
            u = ulim
            fu = func(u)
        else: # reject u
            u = xc + GOLD*(xc-xb)
            fu = func(u)
        xa,xb,xc = xb,xc,u
        fa,fb,fc = fb,fc,fu
    else:
        print "Warning: MAXITERS exceeded in bracket_minimum!"
    #end for
    return xa,xb,xc # consider returning none here?

def test_func(point): return point*point + 5.0
def test_bracket(): print bracket_minimum(test_func,5.0,11.0)
def test_linemin(): print line_minimization(test_func,5.0,11.0)

#This is a very hard function to optimize:
#def testfunc2d(point):
#    x,y = map(float,point)
#    return (1.5-x*(1-y))**2 + (2.25-x*(1-y*y))**2 + (2.625-x*(1-y**3))**2

def testfunc2d(point):
    x,y = map(float,point)
    return 25.0 + x*x + y*y

def test_powell():
    print Powell(testfunc2d,(9.0,7.0))

if __name__ == '__main__':
    #test_bracket()
    #test_linemin()
    test_powell()


