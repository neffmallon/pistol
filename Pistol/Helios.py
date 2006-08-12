#!/usr/bin/env python

"""
Helios.py: Solve two-electron atoms using Pekeris techniques

Usage: Helios.py <options>
Options:
 -h     Print this help message
 -n  #  Calculate a maximum order of # (default=5)
 -Z  #  Compute for atomic number # (default=2)
 -s     Perform a singlet state calculation (default)
 -t     Perform a triplet state calculation

Useful references:
'Ground State of Two-Electron Atoms.' C. L. Pekeris. Phys. Rev. 112,
   1649 (1958)

'Some calculations on the ground and lowest-triplet state of helium
  in the fixed-nucleus approximation.' H. Cox, S. J. Smith, B. T.
  Sutcliffe. Phys. Rev. A. 49, 4520 (1994).

 Test values (from Pekeris) for verification.
              Singlet states:
 n  Matrix Size     H-                He
 5    22        0.52763068142   2.90368898612
 9    95        0.52775001651   2.90372338908
 10   125       0.52775061025   2.90372387862
 11   161       0.52775085979   2.90372411115
 12   203       0.52775093560   2.90372422832
 13   252       0.52775097384   2.90372429041
 16   444       0.52775100630   2.90372435622
 19   715       0.52775101339   2.90372437081
 22   1078      0.52775101536   2.90372437476
              Triplet states:
 n  Matrix Size    He
 11   125       2.17522097961
 14   252       2.17522925889
 17   444       2.17522937679


Thanks to Chip Kent, Edward Montgomery, Michael Barnett, and
Robert Forrey for help in getting this working.

Copyright (c) 2003 Richard P. Muller (rmuller@sandia.gov). All rights
reserved. 
"""

from Numeric import zeros,Float,sqrt,matrixmultiply,transpose
from LinearAlgebra import Heigenvectors,Heigenvalues
import sys,getopt


def kval(l,m,n,spin):
    """
       This is from Pekeris, except that the last term of the singlet
       expression corrects a type in Pekeris' paper."""
    w = l+m+n
    lm = l+m
    if spin == 0:
        k = w*(w+2)*(2*w+5)/24. + (1-pow(-1,w))/16. + lm*lm/4. +\
            (1-pow(-1,lm))/8. + l+ 1 + lm/2.
    elif spin == 1:
        # The following was caught by Ed Montgomery, 1/16/00. Note
        # the different sign from the previous expression.
        #k = w*(w+2)*(2*w-1)/24. + (1-pow(-1,w))/16. + l*(m+n) + m
        k = w*(w+2)*(2*w-1)/24. - (1-pow(-1,w))/16. + l*(m+n) + m
    else:
        print "kval: Error -- unknown spin"
        sys.exit()
    # k should now be an integer
    k = int(k)
    return k

def korder(wmax,spin):
    """
    Return a list of tuples with (l,m,n) where:
    l    Exponent of s term
    m    Exponent of t term
    n    Exponent of u term
    """
    klist = []
    if spin == 0:
        for w in range(wmax):
            for l in range(w+1):
                for m in range(w+1):
                    n = w-l-m
                    if n>=0 and l<=m:
                        klist.append((l,m,n))
    elif spin == 1:
        for w in range(wmax):
            for n in range(w):
                for m in range(w+1):
                    l = w-n-m
                    if 0<=l<m:
                        klist.append((l,m,n))
    else:
        print "korder: ERROR improper spin state"
        sys.exit()
    return klist

def hterm(l,m,n,l2,m2,n2):
    """
    Obtain the Pekeris Hamiltonian:
    Hc = ScE
    H = a*Z + b
    S = c
    """
    delta = l2-l, m2-m, n2-n
    if delta == (2,0,0):
        x = 4*(l+1)*(l+2)
        a = -x
        b = 0
        c = x*(1+m+n)
    elif delta == (0,2,0):
        x = 4*(m+1)*(m+2)
        a = -x
        b = 0
        c = x*(1+l+n)
    elif delta == (1,1,0):
        x = 4*(l+1)*(m+1)
        a = -2*x
        b = x
        c = x*(2+l+m)
    elif delta == (1,0,1):
        x = 2*(l+1)*(n+1)
        a = -2*x
        b = x
        c = x*(2+2*m+n)
    elif delta == (0,1,1):
        x = 2*(m+1)*(n+1)
        a = -2*x
        b = x
        c = x*(2+2*l+n)
    elif delta == (0,0,2):
        x = (n+1)*(n+2)
        a = 0
        b = x
        c = 0
    elif delta == (1,0,0):
        x = l+1
        a = 4*x*(4*l+4*m+2*n+7)
        b = x*(-8*m-4*n-6)
        c = -2*x*((m+n)*(4*m+12*l)+n*n+12*l+18*m+15*n+14)
    elif delta == (0,1,0):
        x = m+1
        a = 4*x*(4*l+4*m+2*n+7)
        b = x*(-8*l-4*n-6)
        c = -2*x*((l+n)*(4*l+12*m)+n*n+12*m+18*l+15*n+14)
    elif delta == (0,0,1):
        x = 4*(n+1)
        a = x*(2*l+2*m+2)
        b = x*(-l-m-n-2)
        c = -x*(-l*l-m*m+4*l*m+2*l*n+2*n*m+3*l+3*m+2*n+2)
    elif delta == (0,2,-1):
        x = 4*(m+1)*(m+2)*n
        a = 0
        b = 0
        c = x
    elif delta == (2,0,-1):
        x = 4*(l+1)*(l+2)*n
        a = 0
        b = 0
        c = x
    elif delta == (-1,0,2):
        x = 2*l*(n+1)*(n+2)
        a = 0
        b = 0
        c = x
    elif delta == (0,-1,2):
        x = 2*m*(n+1)*(n+2)
        a = 0
        b = 0
        c = x
    elif delta == (0,0,0):
        a = -4*((l+m)*(6*l+6*m+4*n+12)-4*l*m+4*n+8)
        b = 4*(2*l+1)*(2*m+1)+4*(2*n+1)*(l+m+1)+6*n*n+6*n+2
        c = 4*((l+m)*(10*l*m+10*m*n+10*l*n+10*l+10*m+18*n+4*n*n+16) +\
               l*m*(4-12*n)+8+12*n+4*n*n)
    elif delta == (-1,1,0):
        x = 4*l*(m+1)
        a = -2*x
        b = x
        c = x*(1+l+m)
    elif delta == (1,-1,0):
        x = 4*(l+1)*m
        a = -2*x
        b = x
        c = x*(1+l+m)
    elif delta == (-1,0,1):
        x = 2*l*(n+1)
        a = -2*x
        b = x
        c = x*(2*m-4*l-n)
    elif delta == (0,-1,1):
        x = 2*m*(n+1)
        a = -2*x
        b = x
        c = x*(2*l-4*m-n)
    elif delta == (1,0,-1):
        x = 2*(l+1)*n
        a = -2*x
        b = x
        c = x*(2*m-4*l-n-3)
    elif delta == (0,1,-1):
        x = 2*(m+1)*n
        a = -2*x
        b = x 
        c = x*(2*l-4*m-n-3)
    elif delta == (-1,0,0):
        x = 2*l
        a = x*(8*l+8*m+4*n+6)
        b = -x*(4*m+2*n+3)
        c = -x*((m+n+1)*(12*l+4*m+2)+n+n*n)
    elif delta == (0,-1,0):
        x = 2*m
        a = x*(8*l+8*m+4*n+6)
        b = -x*(4*l+2*n+3)
        c = -x*((l+n+1)*(12*m+4*l+2)+n+n*n)
    elif delta == (0,0,-1):
        x = 4*n
        a = x*(2*l+2*m+2)
        b = -x*(l+m+n+1)
        c = -x*((l+m)*(1+2*n-l-m)+6*l*m+2*n)
    elif delta == (1,0,-2):
        x = 2*n*(n-1)*(l+1)
        a = 0
        b = 0
        c = x
    elif delta == (0,1,-2):
        x = 2*n*(n-1)*(m+1)
        a = 0
        b = 0
        c = x
    elif delta == (-2,0,1):
        x = 4*l*(l-1)*(n+1)
        a = 0
        b = 0
        c = x
    elif delta == (0,-2,1):
        x = 4*m*(m-1)*(n+1)
        a = 0
        b = 0
        c = x
    elif delta == (-2,0,0):
        x = 4*l*(l-1)
        a = -x
        b = 0
        c = x*(1+m+n)
    elif delta == (0,-2,0):
        x = 4*m*(m-1)
        a = -x
        b = 0
        c = x*(1+l+n)
    elif delta == (0,0,-2):
        x = n*(n-1)
        a = 0
        b = x
        c = 0
    elif delta == (-1,-1,0):
        x = 4*l*m
        a = -2*x
        b = x
        c = x*(l+m)
    elif delta == (-1,0,-1):
        x = 2*l*n
        a = -2*x
        b = x
        c = x*(2*m+n+1)
    elif delta == (0,-1,-1):
        x = 2*m*n
        a = -2*x
        b = x
        c = x*(2*l+n+1)
    else:
        a = 0.
        b = 0.
        c = 0.
    return (a,b,c)

def pekeris(Z,wmax,spin):
    """
    Return Pekeris H and S of order n with nuclear charge Z
    write H = a*Z + b.
    """
    klist = korder(wmax,spin)
    N = len(klist)
    H = zeros((N,N),Float)
    S = zeros((N,N),Float)
    for index1 in range(N):
        l,m,n = klist[index1]
        k = kval(l,m,n,spin)
        for index2 in range(N):
            l2,m2,n2 = klist[index2]
            k2 = kval(l2,m2,n2,spin)
            i = k-1
            j = k2-1
            a,b,c = hterm(l,m,n,l2,m2,n2)
            if l == m and l2 == m2:
                a = 0.5*a
                b = 0.5*b
                c = 0.5*c
            elif l == m or l2 == m2:
                pass #do nothing here
            elif spin == 1:
                a2,b2,c2 = hterm(m,l,n,l2,m2,n2)
                a = a - a2
                b = b - b2
                c = c - c2
            elif spin == 0:
                a2,b2,c2 = hterm(m,l,n,l2,m2,n2)
                a = a + a2
                b = b + b2
                c = c + c2
            else:
                print "pekeris: ERROR should not be here"
                sys.exit()
            H[i,j] = a*Z + b
            S[i,j] = c
                
    return (H,S)

def transform(A,B):
    "Similarity transformation: returns (B+)AB"
    C = matrixmultiply(A,B)
    return matrixmultiply(transpose(B),C)

def inv_sqrt(M):
    "Returns the inverse square root of a matrix"
    E,V = Heigenvectors(M)
    n = len(E)
    M = zeros((n,n),Float)
    for i in range(n):
        M[i,i] = 1./sqrt(E[i])
    return transform(M,V)

def two_electron_solve(**kwargs):
    "Solve the Peckeris Hamiltonian for a 2 electron system"

    # keyword arguments
    Z = kwargs.get("Z",2)        # Atomic number (1=H-, 2=He, etc.)
    wmax = kwargs.get("wmax",5)  # Maximum order of matrix
    spin = kwargs.get("spin",0)  # Spin (0=Singlet, 1=Triplet)
    
    H,S = pekeris(Z,wmax,spin)   # get the Ham and Olap matrices
    N = H.shape[0]

    # The next three lines solve the generalized eigenproblem
    X = inv_sqrt(S)
    H = transform(H,X)
    E = Heigenvalues(H)

    # Convert to proper energies:
    for i in range(N): 
        E[i] = -E[i]*E[i]
    print "Energy (h) for order %d: %15.12f" % (N,E[0])
    return E[0]

# Main program starts here:
if __name__ == '__main__':
    opts,args = getopt.getopt(sys.argv[1:],'hn:Z:stp')
    do_profile = 0
    kwargs = {}
    for (key,value) in opts:
        if key == '-h' :
            print __doc__
            sys.exit()
        if key == '-n' : kwargs['wmax'] = int(value)
        if key == '-Z' : kwargs['Z'] = int(value)
        if key == '-t' : kwargs['spin'] = 1
        if key == '-p' : do_profile = 1

    if do_profile:
        import profile,pstats
        profile.run('two_electron_solve(**kwargs)','helios_prof')
        helios_prof = pstats.Stats('helios_prof')
        helios_prof.strip_dirs().sort_stats('time').print_stats(8)
    else:
        two_electron_solve(**kwargs)
