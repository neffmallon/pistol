#!/usr/bin/env python
"""
DVR/Laguerre.py - DVR based on Laguerre polynomials.
Thanks to Viktor Szalay for help with the derivations.
"""

from numpy import zeros,sqrt,array,diag,exp
from numpy.linalg import eigh
from scipy.special.orthogonal import la_roots
from pylab import plot,show,legend

def Laguerre_S(i,j,x):
    Sij = 0
    N = len(x)
    xi = x[i]
    xj = x[j]
    for k in range(N):
        if k == i or k == j: continue
        xk = x[k]
        Sij += sqrt(xi*xj)/(xk*(xk-xi)*(xk-xj))
    return Sij

def RadialKinetic_BH0(N,L):
    # Baye + Heenen eq 3.17
    a = 2*L+2
    x,w = la_roots(N,a)
    x = x.real
    T = zeros((N,N),'d')
    for i in range(N):
        xi = x[i]
        Sii = Laguerre_S(i,i,x)
        T[i,i] = 0.25*pow((a+1.)/xi,2)+Sii
        for j in range(i):
            xj = x[j]
            Sij = Laguerre_S(i,j,x)
            T[i,j] = T[j,i] = pow(-1,i-j)*(0.5*(a+1.)*(xi+xj)/pow(xi*xj,1.5)
                                           +Sij)
    return x,0.5*T

# Commented out, because it doesn't work:
# def RadialKinetic_BH1(N,L):
#     # Baye + Heenen eq 3.27
#     a = L+0.5
#     #a = 2*L+2.5
#     x,w = la_roots(N,a)
#     x = sqrt(x.real)
#     T = zeros((N,N),'d')
#     for i in range(N):
#         xi = x[i]
#         xi2 = xi*xi
#         T[i,i] = (2./3.)*(a+2.0*N+1.0+(a*a-1)/xi2 - 0.5*xi2)
#         for j in range(i):
#             xj = x[j]
#             xj2 = xj*xj
#             T[i,j] = T[j,i] = pow(-1,i-j)*8*xi*xj/(xi2-xj2)
#     return x,0.5*T
# def RadialKinetic(N,L):
#     "Approximate second derivative in Laguerre DVR. See Szalay Table III"
#     alpha = 2*L+2
#     q,w = la_roots(N,alpha)
#     q = q.real
#     T = zeros((N,N),'d')
#     for j in range(N):
#          qj = q[j]
#          for k in range(N):
#              qk = q[k]
#              if k == j:
#                  T[j,j] = 1/float(12) - (2.0*N+1.0+alpha)/(6.0*qj) \
#                           + (alpha*alpha + 8.0)/(12.0*qj*qj)
#              else:
#                  T[j,k] = T[k,j] = (-3.0*qj+qk)*sqrt(qk/qj)/(qj*pow(qj-qk,2))
#     return q,-0.5*T
# def RadialKinetic2(N,L):
#     "Exact form of second derivative in Laguerre DVR. See Szalay Table III"
#     alpha = 2*L+2
#     q,w = la_roots(N,alpha)
#     q = q.real
#     T = zeros((N,N),'d')
#     for j in range(N):
#          qj = q[j]
#          for k in range(N):
#              qk = q[k]
#              if k == j:
#                  T[j,j] = 1/float(12) \
#                           + (6*alpha*N/(1+alpha)+2*alpha*alpha
#                              +(4*N+3)*alpha-4*N-2)\
#                             / (12*(1-alpha)*qj) \
#                             + (alpha*alpha + 6*alpha + 8.0)/(12.0*qj*qj)
#              else:
#                  T[j,k] = T[k,j] = 0.5/sqrt(qj*qk)*(
#                      -(qj+qk)/pow(qj-qk,2) + 0.5/(1-alpha) + N/(1-alpha*alpha)
#                      - 0.5/qj - 0.5/qk )
#     return q,-0.5*T

def RadialKinetic(N,L,h=1.0):
    T = zeros((N,N),'d')
    a = 2*L+2
    h2 = h*h
    #q = Points(N)
    q,w = la_roots(N,a)
    q = q.real
    for i in range(N):
        for j in range(N):
            if i == j:
                T[i,i] = p2jj(N,a,q[i])-L*(L+1)*qm2jj(N,a,q[i])
            else:
                T[i,j] = pow(-1,i+j)*(p2jk(N,a,q[i],q[j])\
                                      -L*(L+1)*qm2jk(N,a,q[i],q[j]))
    return -0.5*T/h2

def Points(N,L=0):
    "This is equivalent to la_roots(N,2*L+2)[0].real"
    a = 2*L+2
    Qmat = zeros((N,N),'d')
    for i in range(N):
        Qmat[i,i] = 2*i+a+1
        if i < N-1:
            # This won't work for non-integer a:
            #  -sqrt(n*(n+a))
            Qmat[i+1,i] = Qmat[i,i+1] = -sqrt((i+1)*(i+a+1))
    Q,U = eigh(Qmat)
    #print Q
    #print la_roots(N,a)[0].real
    return Q,U

def p2jj(N,a,qj):
    "Diagonal element of the second derivative operator"
    a = float(a)
    a2 = a*a
    a3 = a2*a
    val = 1.0/12.0 + (2.0-5*a2-a+4.0*N-2.0*a3-6.0*N*a-4.0*N*a2) \
          /(12.0*qj*(a2-1.0)) \
          + (a2+6.0*a+8.0)/(12.0*qj*qj)
    return val

def p2jk(N,a,qj,qk):
    "Off diagonal element of the second derivative operator"
    a = float(a)
    a2 = a*a
    a3 = a2*a
    sqjk = sqrt(qj*qk)
    val = -a*(2.0*N+a+1.0)/((a2-1.0)*4.0*sqjk) \
          + (3.0*a-2.0)*(qj+qk)/(4.0*(a-1)*sqjk*qj*qk) \
          - (qj+qk)/(sqjk*pow(qj-qk,2))
    return val

def qm2jj(N,a,qj):
    "Diagonal elements of 1/q^2"
    a2 = a*a
    val = (2*N+a+1)/(a*(a2-1)*qj) + (a+2)/(a*qj*qj)
    return val

def qm2jk(N,a,qj,qk):
    "Off-diagonal elements of 1/q^2"
    a2 = a*a
    sqjk = sqrt(qj*qk)
    val = (2*N+a+1)/(a*(a2-1)*sqjk) - (qj+qk)/((a-1)*a*qj*qk*sqjk)
    return val

def Sincresults(n,L):
    from Sinc import RadialKinetic
    Rmax = 20.0
    dr = Rmax/float(n)
    R = [float(i+1)*dr for i in range(n)]
    H = RadialKinetic(n,dr) + diag([-1/r + 0.5*L*(L+1)/(r*r) for r in R]) 
    E,U = eigh(H)
    return R,E,U

def Vmat(N,L):
    q = la_roots(N,2*L+2)[0].real
    return diag([-1/qi for qi in q])

def Htest(N=64,L=1):
    T = RadialKinetic(N,L)
    qbh,Tbh = RadialKinetic_BH0(N,L)

    V = Vmat(N,L)

    R,E,U = Sincresults(N,L)
    print "sinc"
    print E[:4]
    R = array(R)
    dr = R[1]-R[0]
    #plot(U[:,0]/sqrt(R*R*dr),label='sinc')
    #plot(U[:,0],label='sinc')

    # Weight matrix? Doesn't work yet
    #R = la_roots(N,2*L+2)[0].real
    #dr = []
    #Rcurr = 0
    #for Ri in R:
    #    dr.append(Ri-Rcurr)
    #    Rcurr = Ri
    #dr = array(dr)

    # Attempt to generate the Cristoffel weights directly. Didn't work:
    #from scipy.special.orthogonal import genlaguerre
    #xs = la_roots(N,2*L+2)[0].real
    #a = 2*L+2
    #lanm = genlaguerre(N-1,a)
    #fi = array([-(N+a)*pow(xi,a-1)*exp(-xi)*lanm(xi) for xi in xs])
    #wts = 1/(xs*fi*fi)

    for kin,lab in [(T,'sz'),(Tbh,'bh')]:
        H = kin + V
        E,U = eigh(H)
        print lab
        print E[:4]
    return

def basis(i,L):
    "Gen Laguerre basis function with weight"
    from scipy.special.orthogonal import genlaguerre
    a = 2*L+2
    lan = genlaguerre(i,a)
    def f(x): return pow(x,a)*exp(-x)*lan(x)
    return f

def Ptest(N=8,L=0):
    Q,U = Points(N,L)
    Qp,Up = Points(N-1,L)
    f = basis(0,L)
    plot(Q,f(Q),label='anal')
    plot(Q,U[:,0],label='0')
    plot(Q,U[:,1])
    plot(Q,U[:,2])
    #plot(Qp,Up[:,-1])
    legend()
    show()
    
if __name__ == '__main__': Ptest()
