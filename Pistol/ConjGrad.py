#!/usr/bin/env python
"""\
 Functional optimization using Conjugate Gradient
"""

from Numeric import *

def mnbrak(ax,bx,func):
    """\
    Bracket the minimum of func, given distinct points ax,bx.
    Return a triplet of points ax,bx,cx where ax < cx < bx,
    and f(cx) < f(ax) and f(cx) < f(bx).

    From NR recipe MNBRAK.

    Works in multidimensions provided ax and bx are numpy arrays
    (and func is a corresponding function of a numpy array).
    """

    gold = 1.618034
    glimit = 100
    tiny=1e-20

    fa = func(ax)
    fb = func(bx)

    if fb > fa: # insure fa > fb
        ax,bx = bx,ax
        fa,fb = fb,fa

    cx = bx+gold*(bx-ax)
    fc = func(cx)

    while fb > fc:
        r = (bx-ax)*(fb-fc)
        q = (bx-cx)*(fb-fa)
        qmr = q-r # check to make sure nonzero
        u = bx-((bx-cx)*q-(bx-ax)*r)/(2*qmr)
        ulim = bx+glimit*(cx-bx)  # furthest point to test

        if (bx-u)*(u-cx) > 0:
            fu = func(u)
            if fu < fc: # min btw b and c
                ax = bx
                fa = fb
                bx = u
                fb = fu
                continue
            elif fu > fb: # min btw a and u
                cx = u
                fc = fu
                continue
            u = cx + gold*(cx-bx) # parabola fit was useless; continue
            fu = func(u)
        elif (cx-u)*(u-ulim) > 0:
            fu = func(u)
            if fu < fc:
                bx = cx
                cx = u
                u = cx + gold*(cx-bx)
                fb = fc
                fc = fu
                fu = func(u)
        elif (u-ulim)*(ulim-cx) > 0:
            u = ulim
            fu = fun(u)
        else:
            u = cx+gold*(cx-bx)
            fu = func(u)
        #end if

        ax,bx,cx = bx,cx,u
        fa,fb,fc = fb,fc,fu
    # end while
    return ax,bx,cx

def brent(ax,bx,cx,func,tol=1e-5):
    a = min(ax,cx)
    b = max(ax,cx)
    v = bx
    w = v
    x = v
    
    

def linmin(x,dir,func):
    """Given a n dimensional vector x and a direction dir, find the
    minimum along dir from x"""

    ax,bx,cx = mnbrak(x,x+dir,func)
    xmin = brent(ax,bx,cx,func)
    return xmin

def testf(x): return 0.5*pow(x-5.,2)
def testf2(x):return 0.5*dot(x,x)

if __name__ == '__main__':

    res = mnbrak(array([0,0]),array([1,1]),testf2)
    print res,map(testf2,res)
    
